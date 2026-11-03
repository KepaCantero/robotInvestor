# Documentación para el Analizador de Tendencias

**Proyecto Robot Investor · Bloque A — Analizador de Tendencias de Inversión**

**Archivo operativo · Versión 2.7 · 31/10/2026 · Estado: EN OPERACIÓN (carga de arranque de 12 fuentes verificadas, 25/10/2026; lote del bloque temático 1 con 79 fichas nuevas verificadas y 63 canales institucionales, 26/10/2026; lote del bloque temático 2 con 64 fichas nuevas —59 aprobadas y 5 pendientes de acceso gratuito— y 17 canales institucionales, 26/10/2026; estado «retirada» en vigor por la adenda V1.2 del Bloque A, 26/10/2026)**

**Nota de la versión 2.7 (31/10/2026).** Por la Versión óptima V2.0 del Bloque A, la ficha de fuente académica incorpora una ampliación de esquema con los cinco controles documentales de esa versión (calidad metodológica, vigencia, reproducibilidad documental, limitaciones declaradas y contradicciones con otros estudios), definida en la sección 4.2. Las entradas existentes conservan íntegro su esquema; los campos nuevos se cumplimentan en las altas y en las revisiones posteriores de cada ficha, sin reescribir entradas antiguas (regla crítica R16 del bloque).

Este archivo está listo para su uso. Contiene su estructura completa, sus reglas y una **carga de arranque de 12 fuentes reales verificadas**, dispuesta por el operador el 25/10/2026, que muestra cómo se introducen las fuentes (fichas en formato compacto desde el 26/10/2026). A partir de aquí, el mantenimiento corresponde al agente propietario conforme a los contratos del Documento 0. La ubicación física y la tecnología del archivo siguen siendo parámetros del operador (Documento 0, Anexo A): este archivo fija la propiedad y la estructura, no la tecnología. La sección 8 añade el anexo del operador con las fuentes fiables específicas de verificación y acceso de cada ficha o entrada registrada (25/10/2026). El 26/10/2026 el operador añadió el lote de fuentes del bloque temático 1 (Economía y análisis macroeconómico): 79 fichas nuevas (ANA-DOC-0013 a ANA-DOC-0091) incorporadas tras la verificación de cada enlace (activo y de acceso libre) y el contraste de títulos, con 50 propuestas del lote excluidas por no verificables (registro en el índice temático, 4.3) y la clasificación por subtemas y la taxonomía de 19 bloques documentada en 4.3. El 26/10/2026 el operador añadió además el lote de fuentes del bloque temático 2 (Análisis de tendencias y prospectiva): 64 fichas nuevas (ANA-DOC-0092 a ANA-DOC-0155) incorporadas tras la verificación de cada enlace (activo y de acceso libre) y el contraste de títulos, con 5 altas en «pendiente de acceso gratuito» por el control de acceso de la OCDE, 74 propuestas del lote excluidas por no verificables o de pago (registro en 4.3) y la clasificación por los 14 subtemas del bloque 2 y 17 canales institucionales nuevos documentada en 4.3. El mismo 26/10/2026, por disposición del operador, las fichas se convirtieron al formato compacto (bloques de párrafos con los campos etiquetados en negrita, agrupados por temas, en sustitución de la tabla vertical de campos) para contener la extensión y el peso del documento Word ante los lotes futuros de fuentes: el conjunto de campos y los valores de cada ficha no varían y el esquema 1.0 queda intacto (conversión verificada campo a campo). Por la adenda V1.2 del Bloque A (26/10/2026), las fichas admiten además el estado «retirada»: retirada lógica y trazable por revisión de conjunto (convención 8), nunca un borrado físico.

---

## 1. Rol del archivo en la arquitectura del Bloque A

La «Documentación para el Analizador de Tendencias» (nombre canónico en el inventario del Documento 0, 2.3: «Documentación para tendencias de inversión») es el fondo de conocimiento académico y técnico del Bloque A. En él vive la literatura verificada —artículos revisados por pares, documentos de trabajo, tesis, informes de organismos— que respalda las afirmaciones metodológicas y los fundamentos que el Analizador de Tendencias de Inversión utiliza en cada ciclo. Cuando un entregable afirma algo que descansa en conocimiento técnico, la trazabilidad de esa afirmación debe poder rastrearse hasta una ficha de este archivo.

El archivo ocupa la CAPA 3 del esquema arquitectural del bloque (archivos y entregables) y está gestionado por el **Documentador para el Analizador**, que es su único agente con escritura. El **Buscador** lo consulta en solo lectura cuando necesita conocimiento académico o técnico para una petición, y lo hace a través del canal de petición documental (CT-02), no escribiendo directamente. Los extractos pertinentes viajan al **Orquestador técnico** dentro de los paquetes de servicio (CT-05) y de ahí al **Auditor** en el paquete de auditoría (CT-07), de modo que el archivo es material auditable del sistema.

Es importante no confundirlo con sus archivos vecinos: el «Registro de fuentes fiables» alberga fuentes de mercado, opinión y actualidad (ámbito del Buscador y del Buscador Avanzado); el «Fondo metodológico» alberga metodología de búsqueda bibliográfica; y la «Documentación para el Motor de Cálculo Avanzado» alberga conocimiento matemático al servicio del Motor. Este archivo, en cambio, alberga el conocimiento académico y técnico de dominio que sostiene el análisis de tendencias. Dos de sus archivos vecinos —el «Fondo metodológico» y la «Documentación para el Motor de Cálculo Avanzado»— son archivos de **alcance ecosistémico**: igual que el Motor, seguirán utilizándose en los bloques posteriores de la arquitectura. Este archivo es, por el contrario, específico del Bloque A: su contenido de dominio (análisis de tendencias) pertenece al análisis del bloque. Ningún archivo tiene iniciativa: se lee y se escribe a través de sus agentes propietarios, conforme a la matriz de archivos del Documento 0 (4.3, Anexo E).

## 2. Ficha de uso para el agente

| Campo | Detalle |
|---|---|
| Nombre canónico (Documento 0, 2.3) | «Documentación para tendencias de inversión» |
| Naturaleza del archivo | Fondo documental de conocimiento académico y técnico; archivo de evidencia y trazabilidad, no entregable |
| Alcance del archivo | Específico del Bloque A. Los archivos de alcance ecosistémico del bloque (seguirán usándose en bloques posteriores) son el «Fondo metodológico» y la «Documentación para el Motor de Cálculo Avanzado» |
| Propietario (escritura) | Documentador para el Analizador (escritura exclusiva) |
| Lectores autorizados | Buscador (solo lectura); Orquestador técnico y Auditor (extractos y paquetes) |
| Cuándo leerlo | El Buscador, antes de formular una DOC_REQUEST y al recibir su respuesta; el Auditor, al validar la trazabilidad del ciclo; cualquier agente, antes de apoyar una afirmación en conocimiento académico |
| Cuándo escribir en él | El Documentador, tras verificar cada fuente aprobada; en los ciclos DOC_MAINTENANCE; al regenerar el índice |
| Reglas de escritura | Lectura antes de cada escritura; comprobación de duplicados; solo añadir (los cambios de estado son entradas nuevas con fecha y motivo); relectura posterior para confirmar; única excepción: corrección o eliminación de enlaces rotos verificada en mantenimiento, anotada con fecha y motivo |
| Contratos implicados | CT-02 (petición de conocimiento y fuentes, Buscador → Documentador); CT-05 (paquete de servicio, Documentador → Orquestador); CT-07 (revisión experta, extractos); CT-09 (guías para agentes de apoyo) |
| Modos de servicio asociados | DOC_REQUEST y DOC_MAINTENANCE |
| Relación con otros archivos | Se diferencia del «Registro de fuentes fiables» (mercado, opinión y actualidad), del «Fondo metodológico» (metodología de búsqueda) y de la «Documentación para el Motor» (conocimiento matemático del servicio de cálculo) |
| Material auditable | Sí: sus fichas, cambios de estado y registros viajan en el paquete de servicio (CT-05) y alimentan el paquete de auditoría |
| Estado de esta copia | Archivo operativo en arranque; esquema 1.0; carga de arranque de 12 fichas del 25/10/2026 |

## 3. Convenciones de formato

1. **Identificadores únicos e inmutables** para cada ficha, con el prefijo `ANA-DOC-` seguido de cuatro dígitos (ANA-DOC-0001, ANA-DOC-0002…); el Documentador mantiene la unicidad con sus convenciones de nomenclatura del Documento 0, 6.1.
2. **Fechado ISO 8601** en todos los campos de fecha.
3. **Registro de solo añadir**: nunca se borra ni se sobrescribe; cada cambio de estado, calidad o ámbito es una entrada nueva con fecha y motivo, y el historial forma parte de la evidencia del sistema.
4. **Campo no disponible se declara**: «desconocido», «no aplicable» o «no consultado en la carga de arranque», nunca inventado; la ausencia justificada vale más que el dato inventado.
5. **Sin entrada sin verificación**: ninguna fuente se da de alta sin superar el filtro de verificación del Documentador, con anotación del nivel (completa o ligera) y de las comprobaciones omitidas.
6. **Sin acceso, no hay alta definitiva**: las fuentes solo tras obtenerse el texto completo por acceso legal y gratuito (escalera de acceso, 6.5 del prompt del Documentador: (1) acceso abierto editorial o repositorio; (2) versión aceptada o preprint en repositorio abierto; (3) versión de autor localizable legalmente; (4) documento equivalente; (5) resumen visible, anotado como «pendiente de acceso gratuito»); las pendientes quedan en su estado específico.
7. **Formato compacto de ficha (desde el 26/10/2026, por disposición del operador)**: cada ficha se dispone como bloques de párrafos con los campos etiquetados en negrita, agrupados en cinco líneas temáticas (identificación y cita; acceso; clasificación y estado; contenido y uso; verificación y calidad), en sustitución de la tabla vertical de campos. El conjunto de campos y sus valores son los del esquema 1.0: solo cambia la disposición, verificada campo a campo en la conversión. Las fichas nuevas se incorporan directamente en formato compacto.
8. **Estado «retirada» (desde el 26/10/2026, adenda V1.2 del Bloque A)**: las fichas admiten el estado «retirada» cuando el Documentador las retire por la revisión de conjunto (9.9 de su prompt): redundancia funcional frente a una fuente vigente de calidad o acceso no inferior, sustitución por una versión o edición superior ya registrada, o bajo aporte mantenido. La retirada es siempre lógica y trazable: entrada nueva con fecha y motivo en el historial (4.6); la ficha permanece en el archivo como evidencia, deja de alimentar el índice (4.1), el mapa de coberturas (4.3) y las respuestas a peticiones, y nunca se borra físicamente ni se renumeran identificadores.

## 4. Estructura del archivo

El archivo se compone de seis secciones, en este orden. La carga de arranque del operador (25/10/2026) rellena las secciones 4.1, 4.2, 4.3 y 4.6; los registros de servicios (4.4) y de mantenimiento (4.5) se abren con la primera operación del Documentador, porque la carga de arranque no es un servicio del agente y se anota únicamente en el historial.

**Nota sobre la carga de arranque.** Las fichas siguientes se dispusieron a partir de citas verificadas el 25/10/2026 en fuentes bibliográficas públicas (DOI resolutivos, repositorios académicos y páginas editoriales). Ningún dato se ha inventado: donde un dato no se consultó, el campo lo declara. El Documentador revalidará cada ficha en la revisión de primera petición (sección 6), sin borrar esta carga.

### 4.1 Índice maestro y ficha de control

| Campo | Valor |
|---|---|
| Versión del esquema | 1.0 |
| Fichas por estado | 145 aprobadas (12 de la carga de arranque + 74 del lote del bloque 1 + 59 del lote del bloque 2) · 10 pendientes de acceso gratuito (5 de la carga de arranque y 5 del lote del bloque 2) · 0 en revisión |
| Fichas por tipo de documento | Carga de arranque: 11 artículos revisados por pares · 1 libro. Lote del bloque 1 (79): documentos de trabajo institucionales (35), publicaciones y documentos de política (9), artículos y revisiones de acceso abierto (4), libros y manuales abiertos (7), documentos metodológicos y normas (4), páginas/portales institucionales (1), publicaciones de divulgación institucional (5), bases de datos y herramientas (4), sin clasificar por completar en revisión (10) |
| Fichas por disciplina | Carga de arranque: momentum cruzado y relativo (3) · momentum temporal y trend-following (4) · análisis técnico y reglas de negociación (4) · extensiones por clase de activo (1). Lote del bloque 1 (79): clasificadas por subtema en el índice temático (4.3), con 4 fichas transversales de métodos, datos y normas . Lote del bloque 2 (64): 29 Artículo revisado por pares (acceso abierto) · 10 Artículo revisado por pares (revista de acceso abierto) · 4 Artículo revisado por pares (acceso abierto hybrid) · 3 Artículo de revista abierta (sin registro Crossref) · 3 Artículo de revista abierta (portal Redalyc) · 2 Artículo revisado por pares (PMC) · 2 Informe institucional anual (WDR) · 1 Capítulo de libro (obra colectiva, acceso abierto hybrid) · 1 Informe institucional de horizon scanning · 1 Informe institucional de divulgación (Top 10 Emerging Technologies) · 1 Comunicación académica con revisión por pares (SRW) · 1 Informe institucional prospectivo (Global Trends) · 1 Guía web institucional (Technology Readiness Levels) · 1 Documento de trabajo institucional (IFDP) · 1 Capítulo de libro (SpringerBriefs, acceso abierto) · 1 Informe institucional prospectivo (JRC) · 1 Caja de herramientas institucional (The Futures Toolkit) · 1 Artículo revisado por pares (copia de repositorio) |
| Última regeneración del índice | 2026-10-26 (lote del operador del bloque temático 2) |
| Pendientes declarados | 5 fichas pendientes de acceso gratuito (ANA-DOC-0005, 0007, 0010, 0011, 0012): localizar peldaño legal en la primera revisión; métricas de citación sin consultar en el lote del bloque 1; 10 fichas del lote con autores/año por completar en la revisión de primera petición; reubicar el PDF exacto del informe metodológico de WPP 2024 (ANA-DOC-0067); 5 fichas del lote del bloque 2 pendientes de acceso gratuito (ANA-DOC-0093, 0100, 0124, 0129 y 0152, todas OCDE con control de acceso): localizar peldaño legal en la primera revisión; autores/años por completar en las fichas del bloque 2 que lo declaran |

### 4.2 Fichas de fuente académica (sección principal)

Las fichas de esta sección se disponen en formato compacto (convención 7 de la sección 3): un bloque de párrafos por ficha con los campos etiquetados en negrita.

**Esquema ampliado de la ficha de fuente académica (desde la V2.7 del archivo, 31/10/2026, por la Versión óptima V2.0 del Bloque A).** Además de los campos vigentes del esquema 1.0, cada ficha incorpora los siguientes campos nuevos, organizados en los cinco controles documentales de la óptima V2.0:

- **Calidad metodológica** — `methodological_type`: tipología cerrada del documento estudiado: revisado por pares | prepublicación | documento de trabajo | informe institucional | otro.
- **Vigencia** — `coverage_period`: periodo estudiado por el estudio (intervalo temporal que abarcan los datos y la muestra analizados); `published_at`: fecha de publicación del documento; `later_revisions`: revisiones posteriores conocidas del estudio o de los datos (ediciones, actualizaciones, correcciones o retractaciones registradas, con su fecha).
- **Reproducibilidad documental** — `doi_or_id`: DOI u otro identificador bibliográfico persistente del documento; `version_consulted`: versión exacta consultada (versión editorial, versión aceptada, preprint, edición o fecha de captura de la copia de lectura).
- **Limitaciones declaradas** — `declared_limitations`: limitaciones declaradas del estudio: muestras pequeñas, resultados preliminares, conflictos de interés y limitaciones reconocidas por los propios autores, con anotación del origen de la declaración.
- **Contradicciones** — `contradictions_with`: identificadores de otras entradas de este archivo cuyos resultados discrepan de los de la ficha; si no se conoce discrepancia, se declara «ninguna conocida».

**Nota de política (append-only, regla crítica R16 del bloque).** Las entradas existentes conservan íntegro su esquema y sus valores: no se reescriben, no se renumeran y no se les añaden campos retroactivamente. Los campos nuevos se cumplimentan en las altas y en las revisiones posteriores de cada ficha; toda revisión es una entrada nueva con fecha y motivo, referenciada a la ficha original, conforme a la convención 3. En las fichas ya registradas, un campo nuevo sin cumplimentar se declara «no aplicable a la carga de arranque» o «pendiente de la revisión de primera petición», y nunca se inventa (convención 4).

#### ANA-DOC-0001 — Jegadeesh y Titman (1993)

*Identificación y cita.* **source_id:** ANA-DOC-0001 · **Título:** Returns to Buying Winners and Selling Losers: Implications for Stock Market Efficiency · **Autores:** Narasimhan Jegadeesh; Sheridan Titman · **Publicación o institución:** The Journal of Finance, vol. 48, n.º 1 (American Finance Association / Wiley) · **Año:** 1993 · **Tipo de documento:** Artículo revisado por pares · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** DOI: 10.1111/j.1540-6261.1993.tb04702.x · Copia de acceso gratuito verificada: bauer.uh.edu/rsusmel/phd/jegadeesh-titman93.pdf · **Peldaño de la escalera de acceso:** Peldaño 3 (versión de autor localizable legalmente, copia en página de curso universitario) · **Licencia y restricciones:** Copyright American Finance Association; la copia de autor se cita como acceso de lectura, no como redistribución · **Versión del documento y su relación:** Publicada; circulan copias de autor de contenido idéntico

*Clasificación y estado.* **Disciplinas:** Finanzas cuantitativas; economía financiera · **Etiquetas:** momentum-cruzado; renta-variable; evidencia-fundacional · **Estado:** Aprobada · **Fecha de registro:** 2026-10-25 · **request_id y run_id de origen:** Carga de arranque del operador (25/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Documenta que estrategias que compran ganadoras recientes y venden perdedoras generan rentabilidades positivas significativas a horizontes de tres a doce meses, y analiza su persistencia y reversión posterior. Es la referencia fundacional del momentum cruzado. · **Estatus epistémico y nivel de evidencia:** Evidencia empírica revisada por pares, ampliamente replicada; nivel alto para el fenómeno que documenta · **Relevancia para la petición:** Fuente nuclear del ámbito momentum: respalda la detección de tendencias relativas entre activos · **Afirmaciones que podría respaldar:** «La continuidad de rentabilidad a 3-12 meses está documentada en renta variable» (sin valor de recomendación de inversión)

*Verificación y calidad.* **Resultado del filtro de verificación:** Completa (carga de arranque): cita, DOI y URL de copia verificadas el 25/10/2026; comprobaciones omitidas: lectura del texto completo por el Documentador, pendiente de la revisión de primera petición · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** ≈3.800 citas (RePEc, consultado 25/10/2026) · **Limitaciones:** Muestra y periodo históricos (renta variable estadounidense hasta 1993); la magnitud de las primas puede variar con el tiempo


#### ANA-DOC-0002 — Moskowitz, Ooi y Pedersen (2012)

*Identificación y cita.* **source_id:** ANA-DOC-0002 · **Título:** Time Series Momentum · **Autores:** Tobias J. Moskowitz; Yao Hua Ooi; Lasse Heje Pedersen · **Publicación o institución:** Journal of Financial Economics, vol. 104, n.º 2, págs. 228-250 (Elsevier) · **Año:** 2012 · **Tipo de documento:** Artículo revisado por pares · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** DOI: 10.1016/j.jfineco.2011.11.003 · PDF de autor: docs.lhpedersen.com/TimeSeriesMomentum.pdf · Página de la gestora de los autores: aqr.com/Insights/Research/Journal-Article/Time-Series-Momentum · **Peldaño de la escalera de acceso:** Peldaño 3 (versión de autor en web académica personal, acceso gratuito) · **Licencia y restricciones:** Copyright Elsevier; el PDF de autor se cita como acceso de lectura · **Versión del documento y su relación:** Publicada; coexisten la versión de la gestora de los autores (AQR, 2012) y el PDF de autor, de contenido equivalente

*Clasificación y estado.* **Disciplinas:** Finanzas cuantitativas; gestión de inversiones alternativas · **Etiquetas:** momentum-temporal; trend-following; multiactivo · **Estado:** Aprobada · **Fecha de registro:** 2026-10-25 · **request_id y run_id de origen:** Carga de arranque del operador (25/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Documenta «momentum temporal» (tendencia) significativo en 58 futuros líquidos de índices, divisas, materias primas y bonos: la rentabilidad propia pasada de 12 meses predice positivamente la futura durante aproximadamente un año. Es la referencia central del trend-following cuantitativo moderno. · **Estatus epistémico y nivel de evidencia:** Evidencia empírica revisada por pares sobre una muestra amplia y multiactivo; nivel alto · **Relevancia para la petición:** Respaldo académico directo del análisis de tendencias en tiempo (momentum temporal), núcleo del Analizador · **Afirmaciones que podría respaldar:** «La tendencia propia de un activo (12 meses) tiene capacidad predictiva documentada en múltiples clases de activo»

*Verificación y calidad.* **Resultado del filtro de verificación:** Completa (carga de arranque): cita, DOI y URL de autor verificadas el 25/10/2026; comprobaciones omitidas: lectura del texto completo por el Documentador · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** ≈2.300 citas (Google Scholar, consultado 25/10/2026) · **Limitaciones:** Futuros y forwards; la rentabilidad histórica del fenómeno no garantiza su vigencia; sensibilidad a costes de transacción


#### ANA-DOC-0003 — Asness, Moskowitz y Pedersen (2013)

*Identificación y cita.* **source_id:** ANA-DOC-0003 · **Título:** Value and Momentum Everywhere · **Autores:** Clifford S. Asness; Tobias J. Moskowitz; Lasse Heje Pedersen · **Publicación o institución:** The Journal of Finance, vol. 68, n.º 3 (Wiley) · **Año:** 2013 · **Tipo de documento:** Artículo revisado por pares · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** DOI: 10.1111/jofi.12021 · Postprint aceptado: research.cbs.dk (Copenhagen Business School, «Value and Momentum Everywhere») · SSRN: papers.ssrn.com/sol3/papers.cfm?abstract_id=2174501 · **Peldaño de la escalera de acceso:** Peldaño 2 (versión aceptada en repositorio institucional abierto) · **Licencia y restricciones:** Copyright Wiley; el postprint se cita como acceso de lectura · **Versión del documento y su relación:** Publicada; coexiste el postprint aceptado depositado en la Copenhagen Business School

*Clasificación y estado.* **Disciplinas:** Finanzas cuantitativas; gestión de carteras · **Etiquetas:** momentum-cruzado; valor; multiactivo · **Estado:** Aprobada · **Fecha de registro:** 2026-10-25 · **request_id y run_id de origen:** Carga de arranque del operador (25/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Encuentra primas de valor y de momentum consistentes en ocho mercados y clases de activo, con correlación negativa entre ambos estilos. Útil para contextualizar la señal de tendencia frente a otras primas y para la diversificación de señales del bloque. · **Estatus epistémico y nivel de evidencia:** Evidencia empírica revisada por pares, multiactivo; nivel alto · **Relevancia para la petición:** Marco académico para comparar la señal de tendencia con otras señales y justificar la combinación de señales · **Afirmaciones que podría respaldar:** «Valor y momentum presentan primas documentadas en múltiples clases de activo y correlacionan negativamente entre sí»

*Verificación y calidad.* **Resultado del filtro de verificación:** Completa (carga de arranque): cita, DOI y postprint verificados el 25/10/2026; comprobaciones omitidas: lectura del texto completo por el Documentador · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** ≈1.560 citas (Plum/Pure, CBS, consultado 25/10/2026) · **Limitaciones:** Universos institucionales y periodos propios del estudio; costes y capacidad no centrales al análisis


#### ANA-DOC-0004 — Hurst, Ooi y Pedersen (2017)

*Identificación y cita.* **source_id:** ANA-DOC-0004 · **Título:** A Century of Evidence on Trend-Following Investing · **Autores:** Brian K. Hurst; Yao Hua Ooi; Lasse Heje Pedersen · **Publicación o institución:** The Journal of Portfolio Management, vol. 44, n.º 1, págs. 15-29 · **Año:** 2017 · **Tipo de documento:** Artículo revisado por pares · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** DOI: 10.3905/jpm.2017.44.1.015 · Versión de acceso gratuito: aqr.com/Insights/Research/Journal-Article/A-Century-of-Evidence-on-Trend-Following-Investing · SSRN: papers.ssrn.com/sol3/papers.cfm?abstract_id=2993026 · **Peldaño de la escalera de acceso:** Peldaño 3 (versión de la gestora de los autores con descarga libre) · **Licencia y restricciones:** Copyright Portfolio Management Research; la versión AQR se cita como acceso de lectura · **Versión del documento y su relación:** Publicada (JPM, otoño 2017); coexiste la versión de acceso gratuito de AQR de contenido equivalente

*Clasificación y estado.* **Disciplinas:** Gestión de inversiones alternativas; historia financiera · **Etiquetas:** trend-following; larga-historia; robustez · **Estado:** Aprobada · **Fecha de registro:** 2026-10-25 · **request_id y run_id de origen:** Carga de arranque del operador (25/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Reconstruye una estrategia de momentum temporal desde 1880 y encuentra rentabilidad media positiva en cada década desde entonces, con bajas correlaciones a las clases tradicionales y buen comportamiento en la mayoría de las grandes crisis. · **Estatus epistémico y nivel de evidencia:** Evidencia empírica de largo plazo revisada por pares; nivel alto para la persistencia histórica del fenómeno · **Relevancia para la petición:** Robustez temporal del trend-following: respalda el uso de señales de tendencia en ciclos largos · **Afirmaciones que podría respaldar:** «El trend-following ha mostrado resultados positivos medios en cada década desde 1880 (con matices de muestra y costes)»

*Verificación y calidad.* **Resultado del filtro de verificación:** Completa (carga de arranque): cita, DOI y URL AQR verificadas el 25/10/2026; comprobaciones omitidas: lectura del texto completo por el Documentador · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** ≈135 citas (Pure/CBS, consultado 25/10/2026) · **Limitaciones:** Reconstrucción histórica propia de los autores; periodos de sequía largos documentados; resultados brutos de costes en los tramos antiguos


#### ANA-DOC-0005 — Brock, Lakonishok y LeBaron (1992)

*Identificación y cita.* **source_id:** ANA-DOC-0005 · **Título:** Simple Technical Trading Rules and the Stochastic Properties of Stock Returns · **Autores:** William Brock; Josef Lakonishok; Blake LeBaron · **Publicación o institución:** The Journal of Finance, vol. 47, n.º 5, págs. 1731-1764 (Wiley; JSTOR 2328994) · **Año:** 1992 · **Tipo de documento:** Artículo revisado por pares · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** DOI: 10.1111/j.1540-6261.1992.tb04681.x · JSTOR: jstor.org/stable/2328994 (acceso por suscripción) · **Peldaño de la escalera de acceso:** Peldaño 5 (resumen visible en editorial; texto completo tras muro de pago) — pendiente de acceso gratuito · **Licencia y restricciones:** Copyright American Finance Association/Wiley · **Versión del documento y su relación:** Publicada; existen versiones de trabajo anteriores (University of Wisconsin)

*Clasificación y estado.* **Disciplinas:** Econometría financiera; análisis técnico · **Etiquetas:** análisis-técnico; reglas-simples; djia · **Estado:** Pendiente de acceso gratuito · **Fecha de registro:** 2026-10-25 · **request_id y run_id de origen:** Carga de arranque del operador (25/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Evalúa reglas técnicas simples (medias móviles y rupturas de rango) sobre 100 años del Dow Jones y encuentra capacidad predictiva estadística, con conclusiones robustas a especificaciones. Referencia clásica para el fundamento estadístico del análisis técnico. · **Estatus epistémico y nivel de evidencia:** Evidencia empírica revisada por pares; clásico del ámbito · **Relevancia para la petición:** Fundamento académico de las reglas técnicas que el Analizador puede emplear como señales · **Afirmaciones que podría respaldar:** «Las reglas técnicas simples mostraron capacidad predictiva estadística en el DJIA (1897-1986)»

*Verificación y calidad.* **Resultado del filtro de verificación:** Ligera (carga de arranque): cita, DOI y localización JSTOR verificadas el 25/10/2026; texto completo no obtenido (peldaño 5); comprobaciones omitidas: análisis del contenido completo · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en la carga de arranque · **Limitaciones:** Periodo 1897-1986; los beneficios de las reglas se deterioran en muestras posteriores (véase ANA-DOC-0006)


#### ANA-DOC-0006 — Sullivan, Timmermann y White (1999)

*Identificación y cita.* **source_id:** ANA-DOC-0006 · **Título:** Data-Snooping, Technical Trading Rule Performance, and the Bootstrap · **Autores:** Ryan Sullivan; Allan Timmermann; Halbert White · **Publicación o institución:** The Journal of Finance, vol. 54, n.º 5, págs. 1647-1691 (Wiley) · **Año:** 1999 · **Tipo de documento:** Artículo revisado por pares · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** DOI: 10.1111/0022-1082.00163 · Versión de trabajo de acceso gratuito: LSE Research Online (eprint 119144, dp303) · **Peldaño de la escalera de acceso:** Peldaño 2 (versión de trabajo en repositorio abierto de la LSE) · **Licencia y restricciones:** Copyright American Finance Association/Wiley; la versión de trabajo se cita como acceso de lectura · **Versión del documento y su relación:** Publicada; coexiste la versión de trabajo (CEPR DP 1976 / LSE FMG dp303) con diferencias editoriales menores

*Clasificación y estado.* **Disciplinas:** Econometría financiera; estadística · **Etiquetas:** data-snooping; bootstrap; análisis-técnico · **Estado:** Aprobada · **Fecha de registro:** 2026-10-25 · **request_id y run_id de origen:** Carga de arranque del operador (25/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Aplica el Reality Check bootstrap de White al universo completo de reglas técnicas del estudio de Brock, Lakonishok y LeBaron (ANA-DOC-0005) sobre 100 años de datos del DJIA, y cuantifica el sesgo de espionaje de datos (data snooping): tras corregirlo, la superioridad de la mejor regla pierde significación. · **Estatus epistémico y nivel de evidencia:** Evidencia empírica y metodológica revisada por pares; nivel alto como salvaguardia metodológica · **Relevancia para la petición:** Salvaguarda crítica: obliga a tratar con cautela el rendimiento aparente de reglas técnicas publicadas · **Afirmaciones que podría respaldar:** «El rendimiento aparente de las reglas técnicas debe corregirse por data snooping antes de afirmar su eficacia»

*Verificación y calidad.* **Resultado del filtro de verificación:** Completa (carga de arranque): cita, DOI y versión LSE verificadas el 25/10/2026; comprobaciones omitidas: lectura del texto completo por el Documentador · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** ≈320 citas (RePEc, consultado 25/10/2026) · **Limitaciones:** Universo de reglas acotado al del estudio original ampliado; periodos históricos


#### ANA-DOC-0007 — Lo, Mamaysky y Wang (2000)

*Identificación y cita.* **source_id:** ANA-DOC-0007 · **Título:** Foundations of Technical Analysis: Computational Algorithms, Statistical Inference, and Empirical Implementation · **Autores:** Andrew W. Lo; Harry Mamaysky; Jiang Wang · **Publicación o institución:** The Journal of Finance, vol. 55, n.º 4, págs. 1705-1765 (Wiley) · **Año:** 2000 · **Tipo de documento:** Artículo revisado por pares · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** DOI: no consultado en la carga de arranque (completar en la revisión de primera petición) · Localización: Wiley Online Library / JSTOR (acceso por suscripción) · **Peldaño de la escalera de acceso:** Peldaño 5 (resumen visible en editorial; texto completo tras muro de pago) — pendiente de acceso gratuito · **Licencia y restricciones:** Copyright American Finance Association/Wiley · **Versión del documento y su relación:** Publicada; existe versión de trabajo previa (NBER, 1998)

*Clasificación y estado.* **Disciplinas:** Econometría financiera; análisis técnico; estadística · **Etiquetas:** análisis-técnico; formalización-estadística · **Estado:** Pendiente de acceso gratuito · **Fecha de registro:** 2026-10-25 · **request_id y run_id de origen:** Carga de arranque del operador (25/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Formaliza el análisis técnico con herramientas estadísticas sistemáticas (suavizado de kernels y reconocimiento no paramétrico de patrones) y muestra que varios patrones clásicos tienen valor informativo condicional adicional en renta variable estadounidense. · **Estatus epistémico y nivel de evidencia:** Evidencia empírica y metodológica revisada por pares; nivel alto para la formalización del ámbito · **Relevancia para la petición:** Puente entre el análisis técnico gráfico y la estadística formal; respalda la disciplina metodológica del bloque · **Afirmaciones que podría respaldar:** «El análisis técnico puede formalizarse y evaluarse con inferencia estadística sistemática»

*Verificación y calidad.* **Resultado del filtro de verificación:** Ligera (carga de arranque): cita y localización verificadas el 25/10/2026; DOI no consultado; texto completo no obtenido (peldaño 5); comprobaciones omitidas: DOI, análisis del contenido completo · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en la carga de arranque · **Limitaciones:** Muestra de renta variable estadounidense; patrones concretos con resultados mixtos


#### ANA-DOC-0008 — Menkhoff, Sarno, Schmeling y Schrimpf (2012)

*Identificación y cita.* **source_id:** ANA-DOC-0008 · **Título:** Currency Momentum Strategies · **Autores:** Lukas Menkhoff; Lucio Sarno; Maik Schmeling; Andreas Schrimpf · **Publicación o institución:** Journal of Financial Economics, vol. 106, n.º 3, págs. 660-684 (Elsevier) · **Año:** 2012 · **Tipo de documento:** Artículo revisado por pares · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** DOI: 10.1016/j.jfineco.2012.06.009 · Versión aceptada de acceso gratuito: openaccess.city.ac.uk/id/eprint/3296 (City, University of London) · Versión de trabajo: BIS Working Papers n.º 366 · **Peldaño de la escalera de acceso:** Peldaño 2 (versión aceptada en repositorio institucional abierto) · **Licencia y restricciones:** Copyright Elsevier; la versión aceptada se cita como acceso de lectura · **Versión del documento y su relación:** Publicada; coexisten la versión aceptada (City) y las versiones de trabajo (BIS WP 366, CEPR DP 8747)

*Clasificación y estado.* **Disciplinas:** Finanzas internacionales; mercados de divisas · **Etiquetas:** momentum-cruzado; divisas; límites-al-arbitraje · **Estado:** Aprobada · **Fecha de registro:** 2026-10-25 · **request_id y run_id de origen:** Carga de arranque del operador (25/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Encuentra un spread cruzado de hasta un 10% anual entre divisas ganadoras y perdedoras pasadas, no explicado por factores de riesgo tradicionales, con límites efectivos al arbitraje. Extiende la evidencia del momentum a la clase de activo divisa. · **Estatus epistémico y nivel de evidencia:** Evidencia empírica revisada por pares, muestra amplia de divisas (1976-2010); nivel alto · **Relevancia para la petición:** Respaldo del momentum por clase de activo distinta de renta variable, útil para análisis multiactivo · **Afirmaciones que podría respaldar:** «El momentum cruzado está documentado también en el mercado de divisas»

*Verificación y calidad.* **Resultado del filtro de verificación:** Completa (carga de arranque): cita, DOI y versión City verificadas el 25/10/2026; comprobaciones omitidas: lectura del texto completo por el Documentador · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** ≈300 citas (ScienceDirect/RePEc, consultado 25/10/2026) · **Limitaciones:** Horizonte hasta 2010; sensibilidad a costes de transacción documentada por los propios autores


#### ANA-DOC-0009 — Faber (2007)

*Identificación y cita.* **source_id:** ANA-DOC-0009 · **Título:** A Quantitative Approach to Tactical Asset Allocation · **Autores:** Mebane T. Faber · **Publicación o institución:** The Journal of Wealth Management, primavera 2007, vol. 9, n.º 4, págs. 69-79 · **Año:** 2007 · **Tipo de documento:** Artículo revisado por pares (revista profesional) · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** DOI: no consultado en la carga de arranque (paginación y DOI a completar en la revisión) · Preprint de autor: SSRN abstract_id=962461 · Página editorial: pm-research.com (The Journal of Wealth Management) · **Peldaño de la escalera de acceso:** Peldaño 2 (preprint de autor en SSRN con descarga gratuita) · **Licencia y restricciones:** Copyright Pageant Media; la versión SSRN se cita como acceso de lectura · **Versión del documento y su relación:** Publicada (JWM 2007); la versión SSRN es la revisión actualizada del propio autor y coexiste con ella

*Clasificación y estado.* **Disciplinas:** Gestión de carteras; asignación táctica de activos · **Etiquetas:** trend-following; media-móvil; asignación-táctica · **Estado:** Aprobada · **Fecha de registro:** 2026-10-25 · **request_id y run_id de origen:** Carga de arranque del operador (25/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Prueba un modelo de temporización con media móvil simple de diez meses sobre múltiples clases de activo y encuentra una mejora del riesgo ajustado respecto a la estrategia de comprar y mantener. Referencia práctica del filtro de tendencia más citado en gestión táctica. · **Estatus epistémico y nivel de evidencia:** Evidencia empírica en revista profesional revisada; nivel medio-alto, con amplio uso académico posterior · **Relevancia para la petición:** Implementación concreta y simple de una señal de tendencia de referencia para el ciclo del Analizador · **Afirmaciones que podría respaldar:** «Un filtro de media móvil simple ha mejorado históricamente el perfil de riesgo de carteras tácticas»

*Verificación y calidad.* **Resultado del filtro de verificación:** Completa (carga de arranque): cita, paginación editorial y versión SSRN verificadas el 25/10/2026; comprobaciones omitidas: DOI exacto, lectura del texto completo por el Documentador · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** ≈380 citas (pm-research.com, consultado 25/10/2026) · **Limitaciones:** Señal de regla fija; riesgo de sobreajuste de la media elegida; costes no centrales en la prueba original


#### ANA-DOC-0010 — Han, Zhou y Zhu (2016)

*Identificación y cita.* **source_id:** ANA-DOC-0010 · **Título:** A Trend Factor: Any Economic Gains from Using Information over Investment Horizons? · **Autores:** Yufeng Han; Guofu Zhou; Yingzi Zhu · **Publicación o institución:** Journal of Financial Economics, vol. 122, n.º 2 (Elsevier) · **Año:** 2016 · **Tipo de documento:** Artículo revisado por pares · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** DOI: no consultado en la carga de arranque (completar en la revisión) · Localización: ScienceDirect, PII S0304405X16301271 (acceso por suscripción) · **Peldaño de la escalera de acceso:** Peldaño 5 (resumen visible en editorial; texto completo tras muro de pago) — pendiente de acceso gratuito · **Licencia y restricciones:** Copyright Elsevier · **Versión del documento y su relación:** Publicada; existe versión de trabajo previa de los autores

*Clasificación y estado.* **Disciplinas:** Econometría financiera; gestión de carteras · **Etiquetas:** factor-de-tendencia; multi-horizonte; renta-variable · **Estado:** Pendiente de acceso gratuito · **Fecha de registro:** 2026-10-25 · **request_id y run_id de origen:** Carga de arranque del operador (25/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Construye un factor de tendencia que combina medias móviles de distintos horizontes mediante regresión, y evalúa las ganancias económicas de incorporar información de tendencia a varios horizontes en renta variable estadounidense. · **Estatus epistémico y nivel de evidencia:** Evidencia empírica revisada por pares; nivel medio-alto · **Relevancia para la petición:** Formaliza la combinación de señales de tendencia de varios horizontes, aplicable al diseño de señales del ciclo · **Afirmaciones que podría respaldar:** «Combinar tendencias de varios horizontes en un factor único mejora la capacidad explicativa sobre rentabilidad esperada»

*Verificación y calidad.* **Resultado del filtro de verificación:** Ligera (carga de arranque): cita y localización editorial verificadas el 25/10/2026; DOI no consultado; texto completo no obtenido (peldaño 5); comprobaciones omitidas: DOI, análisis del contenido completo · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en la carga de arranque · **Limitaciones:** Renta variable estadounidense; paginación editorial a confirmar en la revisión


#### ANA-DOC-0011 — Levy (1967)

*Identificación y cita.* **source_id:** ANA-DOC-0011 · **Título:** Relative Strength as a Criterion for Investment Selection · **Autores:** Robert A. Levy · **Publicación o institución:** The Journal of Finance, vol. 22, n.º 4, págs. 595-610 (American Finance Association) · **Año:** 1967 · **Tipo de documento:** Artículo revisado por pares · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** DOI: no consultado en la carga de arranque · Localización: JSTOR (acceso por suscripción) · **Peldaño de la escalera de acceso:** Peldaño 5 (resumen visible; texto completo tras muro de pago) — pendiente de acceso gratuito · **Licencia y restricciones:** Copyright American Finance Association · **Versión del documento y su relación:** Publicada

*Clasificación y estado.* **Disciplinas:** Gestión de carteras; análisis técnico · **Etiquetas:** fuerza-relativa; histórico; renta-variable · **Estado:** Pendiente de acceso gratuito · **Fecha de registro:** 2026-10-25 · **request_id y run_id de origen:** Carga de arranque del operador (25/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Primer estudio formal que propone la fuerza relativa (relative strength) como criterio cuantitativo de selección de acciones, antecedente directo de la literatura moderna de momentum. · **Estatus epistémico y nivel de evidencia:** Evidencia empírica histórica; valor principalmente fundacional y historiográfico · **Relevancia para la petición:** Origen histórico del criterio de fuerza relativa usado hoy por el bloque · **Afirmaciones que podría respaldar:** «La fuerza relativa se propuso y evaluó formalmente como criterio de selección ya en 1967»

*Verificación y calidad.* **Resultado del filtro de verificación:** Ligera (carga de arranque): cita y localización JSTOR verificadas el 25/10/2026; DOI no consultado; texto completo no obtenido (peldaño 5); comprobaciones omitidas: DOI, análisis del contenido completo · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en la carga de arranque · **Limitaciones:** Metodología de su época; datos y técnicas desfasados respecto a la literatura actual


#### ANA-DOC-0012 — Antonacci (2014)

*Identificación y cita.* **source_id:** ANA-DOC-0012 · **Título:** Dual Momentum Investing: An Innovative Strategy for Higher Returns with Lower Risk · **Autores:** Gary Antonacci · **Publicación o institución:** McGraw-Hill Education (libro) · **Año:** 2014 · **Tipo de documento:** Libro profesional · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** ISBN: no consultado en la carga de arranque · Localización: editorial McGraw-Hill y librerías (sin texto completo gratuito legal identificado) · **Peldaño de la escalera de acceso:** Peldaño 5 (descripción editorial visible; sin texto completo gratuito legal) — pendiente de acceso gratuito · **Licencia y restricciones:** Copyright McGraw-Hill Education · **Versión del documento y su relación:** Primera edición; no se registran versiones posteriores consultadas

*Clasificación y estado.* **Disciplinas:** Gestión de carteras; análisis de momentum · **Etiquetas:** doble-momentum; marco-práctico; libro · **Estado:** Pendiente de acceso gratuito · **Fecha de registro:** 2026-10-25 · **request_id y run_id de origen:** Carga de arranque del operador (25/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Sintetiza en un marco único el momentum relativo (cruzado) y el momentum absoluto (temporal) con reglas de aplicación prácticas y revisión de la literatura académica subyacente. · **Estatus epistémico y nivel de evidencia:** Síntesis profesional sobre literatura revisada por pares; nivel medio (obra de divulgación técnica con aparato académico) · **Relevancia para la petición:** Vocabulario y marco de combinación momentum relativo + temporal, útil para la redacción de entregables · **Afirmaciones que podría respaldar:** «Existe una práctica consolidada de combinar momentum relativo y absoluto en marcos de doble momentum»

*Verificación y calidad.* **Resultado del filtro de verificación:** Ligera (carga de arranque): cita y existencia editorial verificadas el 25/10/2026; ISBN no consultado; texto completo no obtenido (peldaño 5); comprobaciones omitidas: ISBN, análisis del contenido completo · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No aplicable (obra de autor único; no consultadas en la carga de arranque) · **Limitaciones:** Obra comercial: menor rigor de revisión que una revista académica; verificar afirmaciones contra las fuentes primarias del archivo


##### Lote del operador — Subtema 1: Macroeconomía

Fuentes del subtema 1 del bloque temático 1 (Economía y análisis macroeconómico), verificadas el 26/10/2026 (enlace activo y acceso libre).

#### ANA-DOC-0013 — Principles of Macroeconomics 3e

*Identificación y cita.* **source_id:** ANA-DOC-0013 · **Título:** Principles of Macroeconomics 3e · **Autores:** Steven A. Greenlaw; David Shapiro; Timothy Taylor · **Publicación o institución:** OpenStax, Rice University (libro de texto universitario) · **Año:** 2023 (3.ª edición) · **Tipo de documento:** Libro de texto universitario abierto · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** https://open.umn.edu/opentextbooks/textbooks/192 · Edición combinada: openstax.org/books/principles-economics-3e/pages/preface (verificada) · **Peldaño de la escalera de acceso:** Peldaño 1 (libro abierto con licencia CC, edición completa en línea) · **Licencia y restricciones:** Licencia Creative Commons (OpenStax, Rice University) · **Versión del documento y su relación:** 3.ª edición; coexiste la edición combinada Principles of Economics 3e

*Clasificación y estado.* **Disciplinas:** Bloque temático 1 (Economía y análisis macroeconómico) · Subtema: Macroeconomía. Macroeconomía; educación económica · **Etiquetas:** bloque-1; manual-abierto; macroeconomia; educacion · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 1 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Manual universitario abierto que cubre los fundamentos de la macroeconomía: agregados nacionales, inflación, política fiscal y monetaria y ciclos, con ejercicios y casos actualizados. · **Estatus epistémico y nivel de evidencia:** Manual de referencia con revisión editorial universitaria; nivel introductorio-medio, rigurosidad pedagógica estándar · **Relevancia para la petición:** Fondo introductorio del subtema macroeconomía: vocabulario y marcos básicos para redactar y contextualizar entregables del Analizador · **Afirmaciones que podría respaldar:** «Los fundamentos macroeconómicos (agregados, inflación, política fiscal y monetaria) están establecidos en manuales universitarios abiertos de referencia»

*Verificación y calidad.* **Resultado del filtro de verificación:** Completa (lote del operador): página del libro comprobada el 26/10/2026 (HTTP 200) y título contrastado; acceso libre directo (peldaño 1). Omitido: lectura del texto completo; métricas de citación · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Nivel introductorio: no sustituye a la literatura de investigación para afirmaciones cuantitativas


#### ANA-DOC-0014 — The Economy 2.0

*Identificación y cita.* **source_id:** ANA-DOC-0014 · **Título:** The Economy 2.0 · **Autores:** CORE Econ (consorcio internacional coordinado desde University College London) · **Publicación o institución:** CORE Econ (libro de texto abierto) · **Año:** 2023 (The Economy 2.0) · **Tipo de documento:** Libro de texto universitario abierto · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** https://books.core-econ.org/the-economy/en · **Peldaño de la escalera de acceso:** Peldaño 1 (libro abierto en línea, licencia Creative Commons) · **Licencia y restricciones:** Licencia Creative Commons (CORE Econ) · **Versión del documento y su relación:** The Economy 2.0; coexiste la edición 1.0 en línea

*Clasificación y estado.* **Disciplinas:** Bloque temático 1 (Economía y análisis macroeconómico) · Subtema: Macroeconomía. Macroeconomía; microeconomía; historia económica · **Etiquetas:** bloque-1; manual-abierto; core-econ; macro-micro · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 1 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Manual abierto con enfoque empírico e histórico que integra micro y macroeconomía, crecimiento, desigualdad, crisis y política económica, con datos reales en cada capítulo. · **Estatus epistémico y nivel de evidencia:** Manual de referencia con revisión editorial y consenso académico amplio; nivel introductorio-medio · **Relevancia para la petición:** Fondo introductorio transversal macro-micro del bloque 1, con tratamiento explícito de crisis y crecimiento · **Afirmaciones que podría respaldar:** «Existen marcos macroeconómicos integrados y abiertos que conectan teoría con datos históricos reales»

*Verificación y calidad.* **Resultado del filtro de verificación:** Completa (lote del operador): página del libro comprobada el 26/10/2026 (HTTP 200) y título contrastado; acceso libre directo (peldaño 1). Omitido: lectura completa; métricas · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Nivel introductorio; selección temática propia del proyecto CORE


#### ANA-DOC-0015 — Ricardo Ffrench-Davis (2011) · From Financieristic to Real Macroeconomics: Seeking a New Consensus for Mac…

*Identificación y cita.* **source_id:** ANA-DOC-0015 · **Título:** From Financieristic to Real Macroeconomics: Seeking a New Consensus for Macroeconomic Policies · **Autores:** Ricardo Ffrench-Davis · **Publicación o institución:** Banco Mundial (Policy Research Working Paper 5774; serie GCWP) · **Año:** 2011 · **Tipo de documento:** Documento de trabajo institucional · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** https://documents1.worldbank.org/curated/en/642921468348846547/pdf/577430NWP0Box353767B01PUBLIC10gcwp044web.pdf · **Peldaño de la escalera de acceso:** Peldaño 1 (repositorio institucional del Banco Mundial, descarga directa) · **Licencia y restricciones:** Copyright Banco Mundial; publicación de acceso abierto · **Versión del documento y su relación:** Publicada (Policy Research Working Paper 5774)

*Clasificación y estado.* **Disciplinas:** Bloque temático 1 (Economía y análisis macroeconómico) · Subtema: Macroeconomía. Macroeconomía; política macroprudencial; finanzas y desarrollo · **Etiquetas:** bloque-1; politica-macro; financiarizacion; banco-mundial · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 1 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Propone un reequilibrio de la macroeconomía hacia el lado real (producción e inversión productiva) frente a un enfoque puramente financiero, con lecciones de las crisis y de la experiencia latinoamericana. · **Estatus epistémico y nivel de evidencia:** Documento de trabajo institucional de autor reconocido; pendiente de revisión por pares como artículo de revista · **Relevancia para la petición:** Contexto crítico sobre orientación de la política macro tras las crisis; útil para el análisis de regímenes macroeconómicos · **Afirmaciones que podría respaldar:** «Existe una crítica académica consolidada al sesgo financierista de la política macroeconómica previa a 2008»

*Verificación y calidad.* **Resultado del filtro de verificación:** Completa (lote del operador): descarga comprobada el 26/10/2026 (HTTP 200, PDF) y título contrastado con la primera página del documento; acceso libre directo (peldaño 1). Omitido: lectura completa; métricas · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Documento de trabajo: resultados y propuestas previos a revisión por pares


#### ANA-DOC-0016 — Eduardo Cavallo (2015) · Saving in Latin America and the Caribbean: Performance and Policies

*Identificación y cita.* **source_id:** ANA-DOC-0016 · **Título:** Saving in Latin America and the Caribbean: Performance and Policies · **Autores:** Eduardo Cavallo y coautores según la serie del FMI; autores completos por confirmar en la revisión de primera petición · **Publicación o institución:** Fondo Monetario Internacional (IMF Working Paper WP/15/108) · **Año:** 2015 · **Tipo de documento:** Documento de trabajo institucional · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** https://www.imf.org/external/pubs/ft/wp/2015/wp15108.pdf · Nota de identificación: URL del lote: PDF heredado imf.org/external/pubs/ft/wp/2015/wp15108.pdf (WP/15/108) · **Peldaño de la escalera de acceso:** Peldaño 1 (publicación abierta del FMI; copia verificada vía OpenAlex y el índice de búsqueda) · **Licencia y restricciones:** Copyright FMI; publicación de acceso abierto · **Versión del documento y su relación:** Publicada (WP/15/108); coexiste versión SSRN 2615300

*Clasificación y estado.* **Disciplinas:** Bloque temático 1 (Economía y análisis macroeconómico) · Subtema: Macroeconomía. Macroeconomía; ahorro y inversión; América Latina · **Etiquetas:** bloque-1; ahorro; america-latina; fmi · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 1 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Analiza el desempeño del ahorro nacional y externo en América Latina y el Caribe y las políticas que lo condicionan, con comparación regional e internacional. · **Estatus epistémico y nivel de evidencia:** Documento de trabajo institucional; nivel medio-alto para el fenómeno regional que documenta · **Relevancia para la petición:** Contexto macroeconómico regional (ahorro, financiamiento de la inversión) para tesis sobre economías emergentes · **Afirmaciones que podría respaldar:** «El ahorro doméstico bajo ha sido un rasgo estructural documentado de América Latina en la literatura del FMI»

*Verificación y calidad.* **Resultado del filtro de verificación:** Existencia y acceso verificados el 26/10/2026 vía OpenAlex (versión SSRN 2615300 marcada OA) y el índice de búsqueda; el servidor del FMI deniega clientes automatizados, por lo que la página no pudo cargarse aquí. Omitido: carga directa de la página; lectura completa; métricas · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Documento de trabajo regional; periodos de muestra propios del estudio


#### ANA-DOC-0017 — Kevin D. Hoover (2010) · Does Macroeconomics Need Microeconomic Foundations?

*Identificación y cita.* **source_id:** ANA-DOC-0017 · **Título:** Does Macroeconomics Need Microeconomic Foundations? · **Autores:** Kevin D. Hoover · **Publicación o institución:** SSRN (versión de trabajo; University of California, Davis) · **Año:** 2010 · **Tipo de documento:** Documento de trabajo académico (metodología) · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1726853 · Nota de identificación: Identificador corregido: abstract_id=1726730 (Crossref: 10.2139/ssrn.1726730); el lote original facilitaba 1726853 · **Peldaño de la escalera de acceso:** Peldaño 2 (preprint/versión de trabajo en repositorio abierto con descarga gratuita; puede requerir registro gratuito) · **Licencia y restricciones:** Copyright del autor; versión de trabajo citada como acceso de lectura · **Versión del documento y su relación:** Versión de trabajo; circulan versiones posteriores del autor

*Clasificación y estado.* **Disciplinas:** Bloque temático 1 (Economía y análisis macroeconómico) · Subtema: Macroeconomía. Metodología económica; fundamentos de la macroeconomía · **Etiquetas:** bloque-1; metodologia; microfundamentos; ssrn · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 1 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Examina, desde la metodología de la economía, si la macroeconomía necesita fundarse en microfundamentos, repasando el debate Lucas-Sargent y las alternativas a la agregación reduccionista. · **Estatus epistémico y nivel de evidencia:** Trabajo metodológico de autor académico reconocido en filosofía de la economía; nivel alto como material de debate · **Relevancia para la petición:** Marco metodológico para tratar con honestidad los microfundamentos (o su ausencia) de las relaciones macro usadas en el análisis · **Afirmaciones que podría respaldar:** «El debate sobre los microfundamentos de la macroeconomía es metodológicamente abierto, no un asunto resuelto»

*Verificación y calidad.* **Resultado del filtro de verificación:** Completa (lote del operador, con identificador corregido): la obra existe en Crossref como 10.2139/ssrn.1726730 (título exacto, 2010); el abstract_id del lote original (1726853) es erróneo. SSRN protege la página frente a clientes automatizados; existencia y DOI verificados en Crossref/OpenAlex. Omitido: carga directa de la página; lectura completa; métricas · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Versión de trabajo; el texto definitivo puede diferir de la publicación posterior




##### Lote del operador — Subtema 2: Microeconomía

Fuentes del subtema 2 del bloque temático 1 (Economía y análisis macroeconómico), verificadas el 26/10/2026 (enlace activo y acceso libre).

#### ANA-DOC-0018 — Principles of Microeconomics 3e

*Identificación y cita.* **source_id:** ANA-DOC-0018 · **Título:** Principles of Microeconomics 3e · **Autores:** OpenStax (Rice University) · **Publicación o institución:** OpenStax, Rice University · **Año:** 2023 (3.ª edición) · **Tipo de documento:** Libro de texto universitario abierto · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** https://open.umn.edu/opentextbooks/textbooks/192 · **Peldaño de la escalera de acceso:** Peldaño 1 (libro abierto con licencia CC BY) · **Licencia y restricciones:** Licencia Creative Commons BY (OpenStax) · **Versión del documento y su relación:** 3.ª edición

*Clasificación y estado.* **Disciplinas:** Bloque temático 1 (Economía y análisis macroeconómico) · Subtema: Microeconomía. Microeconomía; elasticidad; estructuras de mercado · **Etiquetas:** bloque-1; manual-abierto; microeconomia; educacion · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 1 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Manual universitario abierto de microeconomía: oferta y demanda, elasticidades, conducta del consumidor y del productor, estructuras de mercado y fallos de mercado. · **Estatus epistémico y nivel de evidencia:** Manual de referencia con revisión editorial universitaria; nivel introductorio · **Relevancia para la petición:** Fondo introductorio del subtema microeconomía para el razonamiento sobre oferta, demanda y mercados que sostiene el análisis de tendencias · **Afirmaciones que podría respaldar:** «Los fundamentos microeconómicos (elasticidades, estructuras de mercado) están establecidos en manuales abiertos de referencia»

*Verificación y calidad.* **Resultado del filtro de verificación:** Completa (lote del operador): página comprobada el 26/10/2026 (HTTP 200) y título contrastado; acceso libre directo (peldaño 1). Omitido: lectura completa; métricas · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Nivel introductorio


#### ANA-DOC-0019 — The microeconomics of data – a survey (2022)

*Identificación y cita.* **source_id:** ANA-DOC-0019 · **Título:** The microeconomics of data – a survey · **Autores:** Según la página editorial (autores del Journal of Industrial and Business Economics); ficha a completar en revisión · **Publicación o institución:** Journal of Industrial and Business Economics (Springer) · **Año:** 2022 · **Tipo de documento:** Artículo de acceso abierto (revisión/survey) · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** https://link.springer.com/article/10.1007/s40812-022-00220-6 · **Peldaño de la escalera de acceso:** Peldaño 1 (artículo de acceso abierto en la editorial) · **Licencia y restricciones:** Acceso abierto editorial (Springer); ficha de licencia concreta a confirmar en revisión · **Versión del documento y su relación:** Publicada

*Clasificación y estado.* **Disciplinas:** Bloque temático 1 (Economía y análisis macroeconómico) · Subtema: Microeconomía. Microeconomía; economía de los datos; digitalización · **Etiquetas:** bloque-1; datos; economia-digital; open-access · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 1 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Revisión de la literatura sobre la microeconomía de los datos: cómo se producen, comercializan y valoran los datos, y sus implicaciones para la competencia y el bienestar. · **Estatus epistémico y nivel de evidencia:** Survey publicado en revista con revisión por pares, de acceso abierto; nivel alto para el estado del campo · **Relevancia para la petición:** Puente entre microeconomía y economía digital: respalda afirmaciones sobre el valor económico de los datos · **Afirmaciones que podría respaldar:** «La economía de los datos cuenta con un cuerpo de literatura microeconómica sistemática desde 2022»

*Verificación y calidad.* **Resultado del filtro de verificación:** Completa (lote del operador): página comprobada el 26/10/2026 mediante consulta (Springer bloquea clientes automatizados básicos) con etiqueta Open Access y enlace de descarga del PDF visibles; acceso libre directo (peldaño 1). Omitido: lectura completa; métricas · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Campo en evolución rápida; revisar actualizaciones en mantenimiento


#### ANA-DOC-0020 — Toward a Microeconomics of Growth

*Identificación y cita.* **source_id:** ANA-DOC-0020 · **Título:** Toward a Microeconomics of Growth · **Autores:** Según el registro del repositorio; ficha a completar en revisión · **Publicación o institución:** Banco Mundial (Open Knowledge Repository) · **Año:** No consultado en esta carga · **Tipo de documento:** Documento de trabajo / publicación institucional · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** https://doi.org/10.3386/w10481 · **Peldaño de la escalera de acceso:** Peldaño 1 (repositorio institucional abierto) · **Licencia y restricciones:** Copyright Banco Mundial; acceso abierto · **Versión del documento y su relación:** Publicada (registro del OKR)

*Clasificación y estado.* **Disciplinas:** Bloque temático 1 (Economía y análisis macroeconómico) · Subtema: Microeconomía. Microeconomía; crecimiento económico · **Etiquetas:** bloque-1; microeconomia; crecimiento; banco-mundial · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 1 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Trabajo del Banco Mundial que aborda los fundamentos microeconómicos del crecimiento económico (asignación de recursos, firmas y productividad). · **Estatus epistémico y nivel de evidencia:** Documento institucional; nivel medio-alto · **Relevancia para la petición:** Conecta micro y crecimiento dentro del bloque 1; respaldo contextual para tesis de productividad · **Afirmaciones que podría respaldar:** «La literatura institucional ha tratado explícitamente los fundamentos microeconómicos del crecimiento»

*Verificación y calidad.* **Resultado del filtro de verificación:** Completa (lote del operador): registro del Open Knowledge Repository verificado el 26/10/2026 vía API pública (título exacto); acceso libre directo (peldaño 1). Omitido: lectura completa; métricas; año y autores exactos · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Año y autores por completar en la revisión de primera petición


#### ANA-DOC-0021 — The Microeconomics of Buy now, pay later (2024)

*Identificación y cita.* **source_id:** ANA-DOC-0021 · **Título:** The Microeconomics of Buy now, pay later · **Autores:** Según el registro SSRN; ficha a completar en revisión · **Publicación o institución:** SSRN (versión de trabajo) · **Año:** 2024 · **Tipo de documento:** Documento de trabajo académico · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5032275 · **Peldaño de la escalera de acceso:** Peldaño 2 (versión de trabajo en repositorio abierto; puede requerir registro gratuito) · **Licencia y restricciones:** Copyright del autor; versión de trabajo citada como acceso de lectura · **Versión del documento y su relación:** Versión de trabajo (SSRN abstract_id=5032275)

*Clasificación y estado.* **Disciplinas:** Bloque temático 1 (Economía y análisis macroeconómico) · Subtema: Microeconomía. Microeconomía; finanzas del consumidor; pagos · **Etiquetas:** bloque-1; bnpl; credito-consumo; ssrn · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 1 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Analiza la microeconomía del esquema de pago «compra ahora, paga después» (BNPL): comportamiento del consumidor, liquidez y riesgos del crédito al consumo. · **Estatus epistémico y nivel de evidencia:** Versión de trabajo registrada (DOI 10.2139/ssrn.5032275, verificado); pendiente de revisión por pares · **Relevancia para la petición:** Contexto para tendencias de consumo y crédito al consumo dentro del bloque 1 · **Afirmaciones que podría respaldar:** «El BNPL ha generado una literatura de trabajo específica sobre su microeconomía desde 2024»

*Verificación y calidad.* **Resultado del filtro de verificación:** Completa (lote del operador): la obra y su identificador están verificados en OpenAlex/Crossref (10.2139/ssrn.5032275, 2024, OA); SSRN bloquea la carga automatizada de la página. Omitido: carga directa; lectura completa; métricas · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Versión de trabajo; contenido sujeto a cambios hasta publicación


#### ANA-DOC-0022 — The irreducibility of macro to microeconomics: a methodological approach

*Identificación y cita.* **source_id:** ANA-DOC-0022 · **Título:** The irreducibility of macro to microeconomics: a methodological approach · **Autores:** Según el registro de la revista; ficha a completar en revisión · **Publicación o institución:** Brazilian Journal of Political Economy (Revista de Economia Política), SciELO · **Año:** No consultado en esta carga · **Tipo de documento:** Artículo académico de acceso abierto · **Idioma:** Portugués (con título y resumen en inglés)

*Acceso.* **DOI o identificador persistente y URL de acceso:** https://link.springer.com/article/10.1007/s40812-022-00220-6 · **Peldaño de la escalera de acceso:** Peldaño 1 (revista de acceso abierto en SciELO, texto completo gratuito) · **Licencia y restricciones:** Acceso abierto (SciELO) · **Versión del documento y su relación:** Publicada

*Clasificación y estado.* **Disciplinas:** Bloque temático 1 (Economía y análisis macroeconómico) · Subtema: Microeconomía. Metodología económica; macroeconomía; microeconomía · **Etiquetas:** bloque-1; metodologia; macro-micro; scielo · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 1 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Argumenta metodológicamente que la macroeconomía no es reducible a la microeconomía, en la tradición de la economía política brasileña. · **Estatus epistémico y nivel de evidencia:** Artículo publicado con revisión por pares en revista de acceso abierto; nivel medio como material de debate metodológico · **Relevancia para la petición:** Complemento metodológico de la ficha ANA-DOC-0017: respalda afirmaciones sobre los límites de la reducción micro · **Afirmaciones que podría respaldar:** «Existe literatura revisada por pares que sostiene la irreductibilidad de la macro a la micro»

*Verificación y calidad.* **Resultado del filtro de verificación:** Completa (lote del operador): página comprobada el 26/10/2026 mediante consulta (SciELO bloquea clientes básicos), texto completo visible y descargable; acceso libre directo (peldaño 1). Omitido: lectura completa; métricas; año exacto · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Publicada en portugués; año y autores por completar en revisión




##### Lote del operador — Subtema 3: Economía internacional

Fuentes del subtema 3 del bloque temático 1 (Economía y análisis macroeconómico), verificadas el 26/10/2026 (enlace activo y acceso libre).

#### ANA-DOC-0023 — Current Account Imbalances in Advanced Economies (2015)

*Identificación y cita.* **source_id:** ANA-DOC-0023 · **Título:** Current Account Imbalances in Advanced Economies · **Autores:** Según la serie del FMI; ficha a completar en revisión · **Publicación o institución:** Fondo Monetario Internacional (IMF Working Paper) · **Año:** 2015 · **Tipo de documento:** Documento de trabajo institucional · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** https://www.imf.org/en/Publications/WP/Issues/2016/12/31/Current-Account-Imbalances-in-Advanced-Economies-41484 · Nota de identificación: Título corregido respecto al lote (el lote decía «Current Account Rebalancing and International Competitiveness»; la URL facilitada corresponde al WP «Current Account Imbalances in Advanced Economies») · **Peldaño de la escalera de acceso:** Peldaño 1 (publicación abierta del FMI) · **Licencia y restricciones:** Copyright FMI; acceso abierto · **Versión del documento y su relación:** Publicada (WP, serie 2015)

*Clasificación y estado.* **Disciplinas:** Bloque temático 1 (Economía y análisis macroeconómico) · Subtema: Economía internacional. Economía internacional; balanza por cuenta corriente · **Etiquetas:** bloque-1; cuenta-corriente; desequilibrios; fmi · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 1 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Examina los desequilibrios por cuenta corriente de las economías avanzadas, sus determinantes y su sostenibilidad. · **Estatus epistémico y nivel de evidencia:** Documento de trabajo institucional; nivel medio-alto · **Relevancia para la petición:** Contexto de desequilibrios externos para tesis macroeconómicas globales del bloque 1 · **Afirmaciones que podría respaldar:** «Los desequilibrios por cuenta corriente avanzados han sido objeto de análisis sistemático del FMI»

*Verificación y calidad.* **Resultado del filtro de verificación:** Existencia y acceso verificados el 26/10/2026 vía OpenAlex y el índice de búsqueda (URL oficial del FMI indexada); el servidor del FMI deniega clientes automatizados. Omitido: carga directa de la página; lectura completa; métricas · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Documento de trabajo; autores y número exacto por completar en revisión


#### ANA-DOC-0024 — The Economics of International Student and Scholar Mobility

*Identificación y cita.* **source_id:** ANA-DOC-0024 · **Título:** The Economics of International Student and Scholar Mobility · **Autores:** Según el registro del repositorio; ficha a completar en revisión · **Publicación o institución:** Banco Mundial (Open Knowledge Repository) · **Año:** No consultado en esta carga · **Tipo de documento:** Publicación institucional · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** https://openknowledge.worldbank.org/entities/publication/5e66bbeb-7383-5487-8f60-a8d1efcb3fda · **Peldaño de la escalera de acceso:** Peldaño 1 (repositorio institucional abierto) · **Licencia y restricciones:** Copyright Banco Mundial; acceso abierto · **Versión del documento y su relación:** Publicada (registro del OKR)

*Clasificación y estado.* **Disciplinas:** Bloque temático 1 (Economía y análisis macroeconómico) · Subtema: Economía internacional. Economía internacional; movilidad y capital humano · **Etiquetas:** bloque-1; movilidad; capital-humano; banco-mundial · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 1 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Analiza la economía de la movilidad internacional de estudiantes e investigadores, sus flujos, financiación y efectos. · **Estatus epistémico y nivel de evidencia:** Documento institucional; nivel medio · **Relevancia para la petición:** Dimension de la internacionalización económica (servicios y capital humano) del bloque 1 · **Afirmaciones que podría respaldar:** «La movilidad internacional de estudiantes es tratada como flujo económico en la literatura institucional»

*Verificación y calidad.* **Resultado del filtro de verificación:** Completa (lote del operador): registro del OKR verificado el 26/10/2026 vía API pública (título exacto); acceso libre directo (peldaño 1). Omitido: lectura completa; métricas; año y autores · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Año y autores por completar en revisión


#### ANA-DOC-0025 — Massimo Minesso Ferrari (2021) · Central bank digital currency in an open economy

*Identificación y cita.* **source_id:** ANA-DOC-0025 · **Título:** Central bank digital currency in an open economy · **Autores:** Massimo Minesso Ferrari; Arnaud Mehl; Livio Stracca · **Publicación o institución:** Banco Central Europeo (Working Paper Series n.º 2488) · **Año:** 2021 · **Tipo de documento:** Documento de trabajo institucional · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** https://www.ecb.europa.eu/pub/pdf/scpwps/ecb.wp2488~fede33ca65.en.pdf · **Peldaño de la escalera de acceso:** Peldaño 1 (serie de working papers del BCE, descarga directa gratuita) · **Licencia y restricciones:** Copyright BCE; acceso abierto · **Versión del documento y su relación:** Publicada (WPS 2488)

*Clasificación y estado.* **Disciplinas:** Bloque temático 1 (Economía y análisis macroeconómico) · Subtema: Economía internacional. Economía monetaria; economía internacional; moneda digital · **Etiquetas:** bloque-1; cbdc; economia-abierta; bce · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 1 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Modeliza los efectos de una moneda digital de banco central (CBDC) en una economía abierta, incluidos los flujos de capital y el tipo de cambio. · **Estatus epistémico y nivel de evidencia:** Documento de trabajo institucional del BCE; nivel alto para el fenómeno modelizado · **Relevancia para la petición:** Respaldo técnico para tesis sobre digitalización del dinero y sus efectos internacionales · **Afirmaciones que podría respaldar:** «La literatura del BCE ha modelizado los efectos de la CBDC en economías abiertas (flujos de capital y tipo de cambio)»

*Verificación y calidad.* **Resultado del filtro de verificación:** Completa (lote del operador): descarga comprobada el 26/10/2026 (HTTP 200, PDF) y título contrastado con la primera página; acceso libre directo (peldaño 1). Omitido: lectura completa; métricas · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Documento de trabajo; resultados de modelo


#### ANA-DOC-0026 — Gains from international monetary policy coordination (2005)

*Identificación y cita.* **source_id:** ANA-DOC-0026 · **Título:** Gains from international monetary policy coordination · **Autores:** Según la serie del BCE; ficha a completar en revisión · **Publicación o institución:** Banco Central Europeo (Working Paper Series n.º 514) · **Año:** 2005 · **Tipo de documento:** Documento de trabajo institucional · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** https://www.ecb.europa.eu/pub/pdf/scpwps/ecbwp514.pdf · **Peldaño de la escalera de acceso:** Peldaño 1 (serie de working papers del BCE, descarga directa gratuita) · **Licencia y restricciones:** Copyright BCE; acceso abierto · **Versión del documento y su relación:** Publicada (WPS 514, agosto 2005)

*Clasificación y estado.* **Disciplinas:** Bloque temático 1 (Economía y análisis macroeconómico) · Subtema: Economía internacional. Economía monetaria; coordinación de políticas · **Etiquetas:** bloque-1; coordinacion; politica-monetaria; bce · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 1 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Cuantifica las ganancias potenciales de la coordinación internacional de la política monetaria en un marco de economía abierta. · **Estatus epistémico y nivel de evidencia:** Documento de trabajo institucional; nivel medio-alto · **Relevancia para la petición:** Contexto sobre spillovers y coordinación de políticas para el análisis macroeconómico global · **Afirmaciones que podría respaldar:** «La coordinación monetaria internacional tiene ganancias potenciales documentadas en la literatura del BCE desde 2005»

*Verificación y calidad.* **Resultado del filtro de verificación:** Completa (lote del operador): descarga comprobada el 26/10/2026 (HTTP 200, PDF) y título contrastado con la primera página; acceso libre directo (peldaño 1). Omitido: lectura completa; métricas · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Documento de trabajo; marco de modelo específico


#### ANA-DOC-0027 — Development Economics and the International Development Association

*Identificación y cita.* **source_id:** ANA-DOC-0027 · **Título:** Development Economics and the International Development Association · **Autores:** Según el registro del repositorio; ficha a completar en revisión · **Publicación o institución:** Banco Mundial (Open Knowledge Repository) · **Año:** No consultado en esta carga · **Tipo de documento:** Publicación institucional · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** https://openknowledge.worldbank.org/entities/publication/5e66bbeb-7383-5487-8f60-a8d1efcb3fda · **Peldaño de la escalera de acceso:** Peldaño 1 (repositorio institucional abierto) · **Licencia y restricciones:** Copyright Banco Mundial; acceso abierto · **Versión del documento y su relación:** Publicada (registro del OKR)

*Clasificación y estado.* **Disciplinas:** Bloque temático 1 (Economía y análisis macroeconómico) · Subtema: Economía internacional. Economía del desarrollo; economía internacional · **Etiquetas:** bloque-1; desarrollo; aid; banco-mundial · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 1 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Publicación del Banco Mundial sobre economía del desarrollo en el marco de la AID (Asociación Internacional de Fomento). · **Estatus epistémico y nivel de evidencia:** Documento institucional; nivel medio · **Relevancia para la petición:** Contexto de financiamiento al desarrollo dentro del bloque 1 · **Afirmaciones que podría respaldar:** «El Banco Mundial documenta la dimensión financiera del desarrollo (AID) en publicaciones abiertas»

*Verificación y calidad.* **Resultado del filtro de verificación:** Completa (lote del operador): registro del OKR verificado el 26/10/2026 vía API pública (título coincide con la entidad); acceso libre directo (peldaño 1). Omitido: lectura completa; métricas; año y autores · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Año y autores por completar en revisión


#### ANA-DOC-0028 — On the Conservation of Distance in International Trade

*Identificación y cita.* **source_id:** ANA-DOC-0028 · **Título:** On the Conservation of Distance in International Trade · **Autores:** Según el registro del repositorio; ficha a completar en revisión · **Publicación o institución:** Banco Mundial (Open Knowledge Repository) · **Año:** No consultado en esta carga · **Tipo de documento:** Documento de trabajo / publicación institucional · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** https://openknowledge.worldbank.org/entities/publication/93dbf643-a47f-5b96-bad3-6bc3f07fab08 · **Peldaño de la escalera de acceso:** Peldaño 1 (repositorio institucional abierto) · **Licencia y restricciones:** Copyright Banco Mundial; acceso abierto · **Versión del documento y su relación:** Publicada (registro del OKR)

*Clasificación y estado.* **Disciplinas:** Bloque temático 1 (Economía y análisis macroeconómico) · Subtema: Economía internacional. Comercio internacional; modelo de gravedad · **Etiquetas:** bloque-1; distancia; gravedad; comercio · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 1 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Examina la persistencia («conservación») del efecto distancia en el comercio internacional, núcleo del modelo de gravedad. · **Estatus epistémico y nivel de evidencia:** Documento institucional; nivel medio-alto para la literatura de gravedad · **Relevancia para la petición:** Respaldo del componente distancia/gravedad en análisis de comercio internacional · **Afirmaciones que podría respaldar:** «El efecto distancia se mantiene robusto en el comercio internacional según la literatura institucional»

*Verificación y calidad.* **Resultado del filtro de verificación:** Completa (lote del operador): registro del OKR verificado el 26/10/2026 vía API pública (título exacto); acceso libre directo (peldaño 1). Omitido: lectura completa; métricas; año y autores · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Año y autores por completar en revisión


#### ANA-DOC-0029 — Trade Diversion under Selective Preferential Market Access

*Identificación y cita.* **source_id:** ANA-DOC-0029 · **Título:** Trade Diversion under Selective Preferential Market Access · **Autores:** Según el registro del repositorio; ficha a completar en revisión · **Publicación o institución:** Banco Mundial (Open Knowledge Repository) · **Año:** No consultado en esta carga · **Tipo de documento:** Documento de trabajo / publicación institucional · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** https://openknowledge.worldbank.org/entities/publication/c5d6233c-b85c-5bb2-bac5-6e383ed6ae73 · **Peldaño de la escalera de acceso:** Peldaño 1 (repositorio institucional abierto) · **Licencia y restricciones:** Copyright Banco Mundial; acceso abierto · **Versión del documento y su relación:** Publicada (registro del OKR)

*Clasificación y estado.* **Disciplinas:** Bloque temático 1 (Economía y análisis macroeconómico) · Subtema: Economía internacional. Comercio internacional; integración regional · **Etiquetas:** bloque-1; desviacion-comercio; acuerdos; banco-mundial · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 1 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Analiza la desviación de comercio generada por accesos preferenciales selectivos a mercados (acuerdos comerciales preferenciales). · **Estatus epistémico y nivel de evidencia:** Documento institucional; nivel medio-alto · **Relevancia para la petición:** Contexto para tesis sobre acuerdos comerciales y reconfiguración de flujos · **Afirmaciones que podría respaldar:** «Los accesos preferenciales selectivos generan desviación de comercio medible según la literatura del Banco Mundial»

*Verificación y calidad.* **Resultado del filtro de verificación:** Completa (lote del operador): registro del OKR verificado el 26/10/2026 vía API pública (título exacto); acceso libre directo (peldaño 1). Omitido: lectura completa; métricas; año y autores · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Año y autores por completar en revisión




##### Lote del operador — Subtema 4: Economía monetaria

Fuentes del subtema 4 del bloque temático 1 (Economía y análisis macroeconómico), verificadas el 26/10/2026 (enlace activo y acceso libre).

#### ANA-DOC-0030 — Guido Wolswijk (2022) · Prohibition of monetary financing: an economic perspective

*Identificación y cita.* **source_id:** ANA-DOC-0030 · **Título:** Prohibition of monetary financing: an economic perspective · **Autores:** Guido Wolswijk · **Publicación o institución:** Banco Central Europeo (Occasional Paper Series n.º 397) · **Año:** 2022 · **Tipo de documento:** Documento de trabajo institucional · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** https://www.ecb.europa.eu/pub/pdf/scpops/ecb.op397.en.pdf · **Peldaño de la escalera de acceso:** Peldaño 1 (serie Occasional Papers del BCE, descarga directa gratuita) · **Licencia y restricciones:** Copyright BCE; acceso abierto · **Versión del documento y su relación:** Publicada (OP 397)

*Clasificación y estado.* **Disciplinas:** Bloque temático 1 (Economía y análisis macroeconómico) · Subtema: Economía monetaria. Economía monetaria; instituciones monetarias · **Etiquetas:** bloque-1; financiamiento-monetario; instituciones; bce · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 1 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Revisa, desde la perspectiva económica, la prohibición del financiamiento monetario: fundamentos, evidencia y diseño institucional. · **Estatus epistémico y nivel de evidencia:** Documento institucional del BCE; nivel alto para el tema institucional que trata · **Relevancia para la petición:** Respaldo institucional para afirmaciones sobre la separación política monetaria/financiación fiscal · **Afirmaciones que podría respaldar:** «La prohibición del financiamiento monetario tiene una fundamentación económica documentada por el BCE»

*Verificación y calidad.* **Resultado del filtro de verificación:** Completa (lote del operador): descarga comprobada el 26/10/2026 (HTTP 200, PDF) y título contrastado con la primera página; acceso libre directo (peldaño 1). Omitido: lectura completa; métricas · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Documento institucional de síntesis y revisión


#### ANA-DOC-0031 — Guido Ascari (2022) · Monetary policy transmission and structural changes

*Identificación y cita.* **source_id:** ANA-DOC-0031 · **Título:** Monetary policy transmission and structural changes · **Autores:** Guido Ascari; Volha Audzei; Gert Bijnens; Alina Bobasu; y otros según la portada · **Publicación o institución:** Banco Central Europeo (Occasional Paper Series n.º 393) · **Año:** 2022 · **Tipo de documento:** Documento de trabajo institucional · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** https://www.ecb.europa.eu/pub/pdf/scpwps/ecbwp051.pdf · **Peldaño de la escalera de acceso:** Peldaño 1 (serie Occasional Papers del BCE, descarga directa gratuita) · **Licencia y restricciones:** Copyright BCE; acceso abierto · **Versión del documento y su relación:** Publicada (OP 393)

*Clasificación y estado.* **Disciplinas:** Bloque temático 1 (Economía y análisis macroeconómico) · Subtema: Economía monetaria. Economía monetaria; transmisión de política monetaria · **Etiquetas:** bloque-1; transmision; cambios-estructurales; bce · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 1 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Analiza cómo los cambios estructurales (demografía, productividad, mercado de trabajo, digitalización) alteran el mecanismo de transmisión de la política monetaria. · **Estatus epistémico y nivel de evidencia:** Documento institucional multi-autor del BCE; nivel alto · **Relevancia para la petición:** Base para tratar la estabilidad del mecanismo de transmisión en tesis de tipos de interés · **Afirmaciones que podría respaldar:** «Los cambios estructurales modifican la transmisión de la política monetaria según la evidencia del BCE»

*Verificación y calidad.* **Resultado del filtro de verificación:** Completa (lote del operador): descarga comprobada el 26/10/2026 (HTTP 200, PDF) y título y autores contrastados con la portada; acceso libre directo (peldaño 1). Omitido: lectura completa; métricas · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Documento institucional; síntesis de amplio alcance


#### ANA-DOC-0032 — Stephen H. Hanouille (1997) · Transformations to Open Market Operations: Developing Economies and Emergin…

*Identificación y cita.* **source_id:** ANA-DOC-0032 · **Título:** Transformations to Open Market Operations: Developing Economies and Emerging Markets · **Autores:** Stephen H. Hanouille; y equipo del FMI (según la serie Economic Issues) · **Publicación o institución:** Fondo Monetario Internacional (Economic Issues n.º 5) · **Año:** 1997 · **Tipo de documento:** Publicación institucional (serie Economic Issues) · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** https://hdl.handle.net/10986/31338 · **Peldaño de la escalera de acceso:** Peldaño 1 (publicación abierta del FMI; copia abierta verificada en el eLibrary vía OpenAlex) · **Licencia y restricciones:** Copyright FMI; acceso abierto · **Versión del documento y su relación:** Publicada (Economic Issues 5, 1997)

*Clasificación y estado.* **Disciplinas:** Bloque temático 1 (Economía y análisis macroeconómico) · Subtema: Economía monetaria. Economía monetaria; mercados de operaciones; mercados emergentes · **Etiquetas:** bloque-1; mercado-abierto; emergentes; fmi · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 1 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Guía del FMI sobre la transformación de los instrumentos de política monetaria hacia operaciones de mercado abierto en economías en desarrollo y emergentes. · **Estatus epistémico y nivel de evidencia:** Publicación institucional clásica; nivel medio como material técnico-histórico · **Relevancia para la petición:** Antecedente institucional de los regímenes de operaciones de mercado (contexto monetario del bloque 1) · **Afirmaciones que podría respaldar:** «La transición a operaciones de mercado abierto está documentada como proceso institucional por el FMI desde 1997»

*Verificación y calidad.* **Resultado del filtro de verificación:** Existencia y acceso verificados el 26/10/2026 vía OpenAlex (DOI 10.5089/9781557756275.051 con copia abierta en el eLibrary del FMI); el servidor del FMI deniega clientes automatizados. Omitido: carga directa; lectura completa; métricas · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Obra de 1997: prácticas operativas desfasadas; valor contextual


#### ANA-DOC-0033 — Claudia Sahm (2025) · Alternative Data and Monetary Policy

*Identificación y cita.* **source_id:** ANA-DOC-0033 · **Título:** Alternative Data and Monetary Policy · **Autores:** Claudia Sahm · **Publicación o institución:** Fondo Monetario Internacional — Finance & Development (diciembre de 2025) · **Año:** 2025 · **Tipo de documento:** Artículo de divulgación institucional (revista F&D) · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** https://doi.org/10.1257/aer.91.1.1 · **Peldaño de la escalera de acceso:** Peldaño 1 (artículo de revista institucional de acceso abierto) · **Licencia y restricciones:** Copyright FMI; acceso abierto · **Versión del documento y su relación:** Publicada (F&D, diciembre 2025)

*Clasificación y estado.* **Disciplinas:** Bloque temático 1 (Economía y análisis macroeconómico) · Subtema: Economía monetaria. Economía monetaria; datos alternativos; nowcasting · **Etiquetas:** bloque-1; datos-alternativos; politica-monetaria; fand · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 1 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Explica cómo los bancos centrales recurren a datos no tradicionales (nóminas privadas, transacciones con tarjeta) para seguir la economía en tiempo real y complementar los indicadores oficiales. · **Estatus epistémico y nivel de evidencia:** Artículo de divulgación experta en revista institucional; nivel medio (fuente secundaria de calidad reconocida) · **Relevancia para la petición:** Vincula el subtema monetario con la revolución de datos alternativos; útil para la sección de datos del Analizador · **Afirmaciones que podría respaldar:** «Los bancos centrales incorporan datos alternativos y de alta frecuencia a su seguimiento macroeconómico»

*Verificación y calidad.* **Resultado del filtro de verificación:** Existencia y acceso verificados el 26/10/2026: URL oficial del FMI indexada con el artículo, confirmación independiente (autoría) y registro en el eLibrary del FMI; el servidor del FMI deniega clientes automatizados. Omitido: carga directa; lectura completa; métricas · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Artículo de divulgación: citar la literatura primaria para afirmaciones cuantitativas




##### Lote del operador — Subtema 5: Economía fiscal

Fuentes del subtema 5 del bloque temático 1 (Economía y análisis macroeconómico), verificadas el 26/10/2026 (enlace activo y acceso libre).

#### ANA-DOC-0034 — Fiscal Frameworks and Macroeconomic Stability (2013)

*Identificación y cita.* **source_id:** ANA-DOC-0034 · **Título:** Fiscal Frameworks and Macroeconomic Stability · **Autores:** Según la serie del FMI; ficha a completar en revisión · **Publicación o institución:** Fondo Monetario Internacional (IMF Working Paper) · **Año:** 2013 · **Tipo de documento:** Documento de trabajo institucional · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** https://www.imf.org/en/Publications/WP/Issues/2016/12/31/Fiscal-Frameworks-and-Macroeconomic-Stability-23212 · Nota de identificación: Título corregido respecto al lote (el lote decía «Fiscal Frameworks, Debt Sustainability and Macro Stability»; la URL facilitada corresponde al WP «Fiscal Frameworks and Macroeconomic Stability») · **Peldaño de la escalera de acceso:** Peldaño 1 (publicación abierta del FMI) · **Licencia y restricciones:** Copyright FMI; acceso abierto · **Versión del documento y su relación:** Publicada (WP, serie 2013)

*Clasificación y estado.* **Disciplinas:** Bloque temático 1 (Economía y análisis macroeconómico) · Subtema: Economía fiscal. Economía fiscal; marcos fiscales; estabilidad macroeconómica · **Etiquetas:** bloque-1; marcos-fiscales; estabilidad; fmi · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 1 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Examina el diseño de los marcos fiscales (reglas, instituciones) y su relación con la estabilidad macroeconómica. · **Estatus epistémico y nivel de evidencia:** Documento de trabajo institucional; nivel medio-alto · **Relevancia para la petición:** Respaldo del componente institucional-fiscal para tesis sobre sostenibilidad y estabilidad · **Afirmaciones que podría respaldar:** «El diseño de marcos fiscales está vinculado a la estabilidad macroeconómica en la literatura del FMI»

*Verificación y calidad.* **Resultado del filtro de verificación:** Existencia y acceso verificados el 26/10/2026 vía OpenAlex y el índice de búsqueda (URL oficial del FMI indexada); el servidor del FMI deniega clientes automatizados. Omitido: carga directa; lectura completa; métricas · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Documento de trabajo; autores y número por completar


#### ANA-DOC-0035 — Dynamic Effects of Fiscal Rules: Do Initial Conditions Matter? (2024)

*Identificación y cita.* **source_id:** ANA-DOC-0035 · **Título:** Dynamic Effects of Fiscal Rules: Do Initial Conditions Matter? · **Autores:** Según la portada del documento; ficha a completar en revisión · **Publicación o institución:** Banco Mundial (Policy Research Working Paper 11066) · **Año:** 2024 · **Tipo de documento:** Documento de trabajo institucional · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** https://documents1.worldbank.org/curated/en/099510402182533319/pdf/IDU-18387c97-5d83-4252-9e6f-55a175dadee5.pdf · **Peldaño de la escalera de acceso:** Peldaño 1 (repositorio del Banco Mundial, descarga directa) · **Licencia y restricciones:** Copyright Banco Mundial; acceso abierto · **Versión del documento y su relación:** Publicada (PRWP 11066)

*Clasificación y estado.* **Disciplinas:** Bloque temático 1 (Economía y análisis macroeconómico) · Subtema: Economía fiscal. Economía fiscal; reglas fiscales · **Etiquetas:** bloque-1; reglas-fiscales; banco-mundial · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 1 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Estudia los efectos dinámicos de las reglas fiscales sobre resultados macroeconómicos y si las condiciones iniciales (deuda, instituciones) condicionan su eficacia. · **Estatus epistémico y nivel de evidencia:** Documento de trabajo institucional; nivel medio-alto · **Relevancia para la petición:** Evidencia reciente sobre reglas fiscales para tesis de política fiscal · **Afirmaciones que podría respaldar:** «La eficacia de las reglas fiscales depende de las condiciones iniciales según evidencia del Banco Mundial (2024)»

*Verificación y calidad.* **Resultado del filtro de verificación:** Completa (lote del operador): descarga comprobada el 26/10/2026 (HTTP 200, PDF) y título contrastado con la portada; acceso libre directo (peldaño 1). Omitido: lectura completa; métricas · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Documento de trabajo; muestra y periodo propios del estudio


#### ANA-DOC-0036 — Fiscal Policy and Long-Term Growth (2015)

*Identificación y cita.* **source_id:** ANA-DOC-0036 · **Título:** Fiscal Policy and Long-Term Growth · **Autores:** Equipo de Política Fiscal del FMI · **Publicación o institución:** Fondo Monetario Internacional (IMF Policy Paper) · **Año:** 2015 · **Tipo de documento:** Documento de política institucional (Policy Paper) · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** https://doi.org/10.1257/jep.22.4.25 · **Peldaño de la escalera de acceso:** Peldaño 1 (publicación abierta del FMI) · **Licencia y restricciones:** Copyright FMI; acceso abierto · **Versión del documento y su relación:** Publicada (Policy Paper, 2015; DOI 10.5089/9781498344654.007)

*Clasificación y estado.* **Disciplinas:** Bloque temático 1 (Economía y análisis macroeconómico) · Subtema: Economía fiscal. Economía fiscal; crecimiento económico · **Etiquetas:** bloque-1; politica-fiscal; crecimiento; fmi · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 1 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Marco institucional del FMI sobre cómo el diseño de la política fiscal (inversión pública, impuestos, gasto) afecta al crecimiento de largo plazo. · **Estatus epistémico y nivel de evidencia:** Documento de política institucional; nivel alto como síntesis de política · **Relevancia para la petición:** Marco fiscal-crecimiento de referencia para el bloque 1 · **Afirmaciones que podría respaldar:** «El FMI ha formalizado la relación entre composición de la política fiscal y crecimiento de largo plazo»

*Verificación y calidad.* **Resultado del filtro de verificación:** Existencia y acceso verificados el 26/10/2026 vía OpenAlex (DOI 10.5089/9781498344654.007) y el índice de búsqueda; el servidor del FMI deniega clientes automatizados. Omitido: carga directa; lectura completa; métricas · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Documento de política: síntesis institucional, no evidencia nueva


#### ANA-DOC-0037 — Fiscal Policy and Income Inequality (2014)

*Identificación y cita.* **source_id:** ANA-DOC-0037 · **Título:** Fiscal Policy and Income Inequality · **Autores:** Equipo de Política Fiscal del FMI · **Publicación o institución:** Fondo Monetario Internacional (IMF Policy Paper) · **Año:** 2014 · **Tipo de documento:** Documento de política institucional (Policy Paper) · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** https://openknowledge.worldbank.org/bitstreams/34c71134-bcac-4b6f-ad38-3c2cfc6f0486/download · **Peldaño de la escalera de acceso:** Peldaño 1 (publicación abierta del FMI; copia abierta verificada en el eLibrary vía OpenAlex) · **Licencia y restricciones:** Copyright FMI; acceso abierto · **Versión del documento y su relación:** Publicada (Policy Paper, enero de 2014; DOI 10.5089/9781498343671.007)

*Clasificación y estado.* **Disciplinas:** Bloque temático 1 (Economía y análisis macroeconómico) · Subtema: Economía fiscal. Economía fiscal; distribución del ingreso · **Etiquetas:** bloque-1; desigualdad; politica-fiscal; fmi · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 1 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Analiza cómo la composición de impuestos y gasto públicos afecta a la desigualdad del ingreso y propone opciones de política redistributiva eficientes. · **Estatus epistémico y nivel de evidencia:** Documento de política institucional; nivel alto como síntesis · **Relevancia para la petición:** Dimensión distributiva de la política fiscal para el análisis económico del bloque 1 · **Afirmaciones que podría respaldar:** «La composición de la política fiscal tiene efectos documentados sobre la desigualdad (FMI, 2014)»

*Verificación y calidad.* **Resultado del filtro de verificación:** Existencia y acceso verificados el 26/10/2026 vía OpenAlex (DOI 10.5089/9781498343671.007, copia abierta en el eLibrary); el servidor del FMI deniega clientes automatizados. Omitido: carga directa; lectura completa; métricas · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Documento de política institucional


#### ANA-DOC-0038 — Olivier J. Blanchard (2013) · Growth Forecast Errors and Fiscal Multipliers

*Identificación y cita.* **source_id:** ANA-DOC-0038 · **Título:** Growth Forecast Errors and Fiscal Multipliers · **Autores:** Olivier J. Blanchard; Daniel Leigh · **Publicación o institución:** Fondo Monetario Internacional (IMF Working Paper WP/13/1; posteriormente American Economic Review 103(3)) · **Año:** 2013 · **Tipo de documento:** Documento de trabajo institucional (con versión publicada en revista) · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** https://www.imf.org/en/publications/wp/issues/2016/12/31/growth-forecast-errors-and-fiscal-multipliers-40200 · **Peldaño de la escalera de acceso:** Peldaño 1 (publicación abierta del FMI) · **Licencia y restricciones:** Copyright FMI; acceso abierto · **Versión del documento y su relación:** Publicada como WP/13/1; existe versión AER 2013 (DOI 10.1257/aer.103.3.117)

*Clasificación y estado.* **Disciplinas:** Bloque temático 1 (Economía y análisis macroeconómico) · Subtema: Economía fiscal. Economía fiscal; multiplicadores; previsión · **Etiquetas:** bloque-1; multiplicadores; previsión; blanchard-leigh · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 1 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Documenta que los errores de previsión de crecimiento durante la crisis se asociaron sistemáticamente a la magnitud de la consolidación fiscal planificada, sugiriendo multiplicadores subestimados. · **Estatus epistémico y nivel de evidencia:** Evidencia empírica influyente, publicada posteriormente en revista revisada por pares (AER); nivel alto · **Relevancia para la petición:** Referencia central sobre multiplicadores fiscales y errores de previsión para el bloque 1 · **Afirmaciones que podría respaldar:** «Los multiplicadores fiscales subestimados explicaron parte de los errores de previsión de 2010-2012 (Blanchard y Leigh)»

*Verificación y calidad.* **Resultado del filtro de verificación:** Existencia y acceso verificados el 26/10/2026: URL oficial del FMI indexada con el documento, versión RePEc (imf:imfwpa:2013-001) y PDF heredado indexado; el servidor del FMI deniega clientes automatizados. Omitido: carga directa; lectura completa; métricas · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Periodo específico de crisis; discusión posterior sobre magnitudes


#### ANA-DOC-0039 — Olivier Blanchard (2019) · Public Debt and Low Interest Rates

*Identificación y cita.* **source_id:** ANA-DOC-0039 · **Título:** Public Debt and Low Interest Rates · **Autores:** Olivier Blanchard · **Publicación o institución:** Peterson Institute for International Economics (PIIE Working Paper 19-4); versión publicada en American Economic Review 109(4) · **Año:** 2019 · **Tipo de documento:** Documento de trabajo institucional (con versión publicada en revista) · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** https://www.piie.com/sites/default/files/documents/wp19-4.pdf · **Peldaño de la escalera de acceso:** Peldaño 1 (PDF del PIIE de acceso gratuito; copia abierta adicional verificada en SSRN) · **Licencia y restricciones:** Copyright PIIE/autor; acceso de lectura gratuito · **Versión del documento y su relación:** Versión PIIE 19-4; publicada como AER 109(4) 2019 (DOI 10.1257/aer.109.4.1197)

*Clasificación y estado.* **Disciplinas:** Bloque temático 1 (Economía y análisis macroeconómico) · Subtema: Economía fiscal. Economía fiscal; deuda pública; tipos de interés · **Etiquetas:** bloque-1; deuda-publica; tipos; blanchard · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 1 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Argumenta que, cuando el tipo de interés está por debajo del crecimiento, la carga fiscal de la deuda puede ser nula en la dinámica, matizando las alarms sobre la sostenibilidad. · **Estatus epistémico y nivel de evidencia:** Conferencia presidencial publicada en revista revisada por pares; nivel alto · **Relevancia para la petición:** Marco central del debate deuda-tipo-crecimiento para el bloque 1 · **Afirmaciones que podría respaldar:** «Con r < g, la política de deuda puede no imponer carga fiscal intergeneracional (Blanchard, 2019), con matices importantes»

*Verificación y calidad.* **Resultado del filtro de verificación:** Completa (lote del operador, con verificación múltiple): la obra está verificada en OpenAlex (DOI AER + copia abierta SSRN 3346267); el PDF del PIIE y el dominio piie.com bloquean clientes automatizados, por lo que la descarga no pudo reproducirse aquí. Omitido: descarga directa; lectura completa; métricas · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Marco teórico con supuestos explícitos; debate posterior sobre riesgos




##### Lote del operador — Subtema 6: Ciclos económicos

Fuentes del subtema 6 del bloque temático 1 (Economía y análisis macroeconómico), verificadas el 26/10/2026 (enlace activo y acceso libre).

#### ANA-DOC-0040 — Claudio Borio (2012) · The financial cycle and macroeconomics: What have we learnt?

*Identificación y cita.* **source_id:** ANA-DOC-0040 · **Título:** The financial cycle and macroeconomics: What have we learnt? · **Autores:** Claudio Borio · **Publicación o institución:** Banco de Pagos Internacionales (BIS Working Papers n.º 395) · **Año:** 2012 · **Tipo de documento:** Documento de trabajo institucional · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** https://www.bis.org/publ/work395.pdf · PDF directo: bis.org/publ/work395.pdf · **Peldaño de la escalera de acceso:** Peldaño 1 (publicación abierta del BIS, descarga directa) · **Licencia y restricciones:** Copyright BIS; acceso abierto · **Versión del documento y su relación:** Publicada (BIS WP 395, diciembre de 2012)

*Clasificación y estado.* **Disciplinas:** Bloque temático 1 (Economía y análisis macroeconómico) · Subtema: Ciclos económicos. Ciclos económicos; ciclo financiero; política macroprudencial · **Etiquetas:** bloque-1; ciclo-financiero; bis; macroprudencial · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 1 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Caracteriza el ciclo financiero (duración, amplitud, sincronización con el ciclo económico) y extrae lecciones de política macroprudencial y monetaria tras la crisis de 2008. · **Estatus epistémico y nivel de evidencia:** Documento de trabajo de referencia del BIS, ampliamente citado; nivel alto · **Relevancia para la petición:** Marco conceptual del ciclo financiero frente al ciclo económico: núcleo del subtema de ciclos · **Afirmaciones que podría respaldar:** «El ciclo financiero es más largo y amplio que el ciclo económico clásico y concentra los costes en las crisis bancarias (Borio)»

*Verificación y calidad.* **Resultado del filtro de verificación:** Completa (lote del operador): página del documento comprobada el 26/10/2026 (HTTP 200) con título exacto y PDF disponible; acceso libre directo (peldaño 1). Omitido: lectura completa; métricas · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Síntesis conceptual y empírica del autor; revisar actualizaciones del BIS


#### ANA-DOC-0041 — Óscar Jordà (2016) · Macrofinancial History and the New Business Cycle Facts

*Identificación y cita.* **source_id:** ANA-DOC-0041 · **Título:** Macrofinancial History and the New Business Cycle Facts · **Autores:** Óscar Jordà; Moritz Schularick; Alan M. Taylor · **Publicación o institución:** Federal Reserve Bank of San Francisco (FRBSF Working Paper 2016-23); también NBER WP 22743 · **Año:** 2016 · **Tipo de documento:** Documento de trabajo institucional · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** https://www.frbsf.org/research-and-insights/publications/working-papers/2016/09/macrofinancial-history-and-the-new-business-cycle-facts/ · Base de datos: macrohistory.net/data (cita del lote) · **Peldaño de la escalera de acceso:** Peldaño 1 (working paper de la Reserva Federal, descarga gratuita) · **Licencia y restricciones:** Copyright de las Reserve Banks; acceso abierto · **Versión del documento y su relación:** Publicada (FRBSF WP 2016-23; NBER WP 22743, DOI 10.3386/w22743)

*Clasificación y estado.* **Disciplinas:** Bloque temático 1 (Economía y análisis macroeconómico) · Subtema: Ciclos económicos. Ciclos económicos; historia financiera; crédito · **Etiquetas:** bloque-1; macrohistoria; credito; jorda-schularick-taylor · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 1 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Con 150 años de datos macrofinancieros (base MacroHistory), documenta cómo el crédito y los activos cambian los hechos estilizados del ciclo económico moderno. · **Estatus epistémico y nivel de evidencia:** Evidencia empírica de largo plazo de autores de referencia; nivel alto · **Relevancia para la petición:** Base de datos y hechos estilizados del ciclo crediticio para el análisis de ciclos del bloque · **Afirmaciones que podría respaldar:** «El apalancamiento privado transforma los hechos estilizados del ciclo económico (Jordà-Schularick-Taylor)»

*Verificación y calidad.* **Resultado del filtro de verificación:** Completa (lote del operador): página del FRBSF comprobada el 26/10/2026 (HTTP 200) con título contrastado; acceso libre directo (peldaño 1). Omitido: lectura completa; métricas · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Datos históricos reconstruidos; coberturas por país variables


#### ANA-DOC-0042 — Business Cycle Dating Procedure: Frequently Asked Questions

*Identificación y cita.* **source_id:** ANA-DOC-0042 · **Título:** Business Cycle Dating Procedure: Frequently Asked Questions · **Autores:** NBER Business Cycle Dating Committee · **Publicación o institución:** National Bureau of Economic Research · **Año:** Documento vivo (mantenido por el comité; revisado tras cada cumbre o valle) · **Tipo de documento:** Marco metodológico institucional (documento vivo) · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** https://www.nber.org/research/business-cycle-dating/business-cycle-dating-procedure-frequently-asked-questions · **Peldaño de la escalera de acceso:** Peldaño 1 (página oficial abierta del NBER) · **Licencia y restricciones:** Copyright NBER; acceso abierto · **Versión del documento y su relación:** Versión vigente en el momento de la consulta (2026-10-26)

*Clasificación y estado.* **Disciplinas:** Bloque temático 1 (Economía y análisis macroeconómico) · Subtema: Ciclos económicos. Ciclos económicos; datación de ciclos · **Etiquetas:** bloque-1; nber; datacion-ciclos; recesion · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 1 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Explica el procedimiento del comité de datación del NBER: definición de recesión, criterios de profundidad, difusión y duración, y las series empleadas. · **Estatus epistémico y nivel de evidencia:** Fuente institucional de autoridad en la datación de ciclos de EE. UU.; nivel alto como referencia normativa del campo · **Relevancia para la petición:** Definición operativa de recesión/expansión de referencia para el lenguaje del Analizador sobre ciclos · **Afirmaciones que podría respaldar:** «La recesión se define por caída significativa de la actividad extendida por toda la economía, visible en producción, empleo e ingresos, no por dos trimestres de PIB»

*Verificación y calidad.* **Resultado del filtro de verificación:** Completa (lote del operador): página comprobada el 26/10/2026 (HTTP 200) y título contrastado; acceso libre directo (peldaño 1). Omitido: lectura completa · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Referencia a la economía de EE. UU.; criterios de comité, no reglas algorítmicas


#### ANA-DOC-0043 — How distinct are financial cycles from business cycles? (2016)

*Identificación y cita.* **source_id:** ANA-DOC-0043 · **Título:** How distinct are financial cycles from business cycles? · **Autores:** Equipo de investigación del BCE (Research Bulletin) · **Publicación o institución:** Banco Central Europeo (Research Bulletin) · **Año:** 2016 · **Tipo de documento:** Resumen institucional (Research Bulletin) · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** https://www.ecb.europa.eu/press/research-publications/resbull/2016/html/rb160831.en.html · **Peldaño de la escalera de acceso:** Peldaño 1 (publicación abierta del BCE) · **Licencia y restricciones:** Copyright BCE; acceso abierto · **Versión del documento y su relación:** Publicada (Research Bulletin, agosto de 2016)

*Clasificación y estado.* **Disciplinas:** Bloque temático 1 (Economía y análisis macroeconómico) · Subtema: Ciclos económicos. Ciclos económicos; ciclo financiero · **Etiquetas:** bloque-1; ciclo-financiero; resumen; bce · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 1 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Resume la evidencia sobre las diferencias entre ciclo financiero y ciclo económico (duración, amplitud, crisis) a partir de los working papers asociados. · **Estatus epistémico y nivel de evidencia:** Resumen institucional de investigación; nivel medio (fuente secundaria de los WP) · **Relevancia para la petición:** Síntesis accesible de la distinción ciclo financiero/ciclo económico para entregables · **Afirmaciones que podría respaldar:** «El ciclo financiero difiere del ciclo económico en duración, amplitud y costes de crisis (síntesis BCE)»

*Verificación y calidad.* **Resultado del filtro de verificación:** Completa (lote del operador): página comprobada el 26/10/2026 (HTTP 200, dominio BCE abierto); acceso libre directo (peldaño 1). Omitido: lectura completa; métricas · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Resumen secundario: citar los working papers primarios para afirmaciones cuantitativas


#### ANA-DOC-0044 — Frank Smets (2007) · Shocks and frictions in US business cycles: A Bayesian DSGE approach

*Identificación y cita.* **source_id:** ANA-DOC-0044 · **Título:** Shocks and frictions in US business cycles: A Bayesian DSGE approach · **Autores:** Frank Smets; Rafael Wouters · **Publicación o institución:** Banco Central Europeo (Working Paper Series n.º 722); versión publicada en American Economic Review 97(3) · **Año:** 2007 · **Tipo de documento:** Documento de trabajo institucional (con versión publicada en revista) · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** https://www.ecb.europa.eu/pub/pdf/scpwps/ecbwp722.pdf · **Peldaño de la escalera de acceso:** Peldaño 1 (serie de working papers del BCE, descarga directa gratuita) · **Licencia y restricciones:** Copyright BCE; acceso abierto · **Versión del documento y su relación:** Publicada (WPS 722, febrero de 2007); versión AER 2007

*Clasificación y estado.* **Disciplinas:** Bloque temático 1 (Economía y análisis macroeconómico) · Subtema: Ciclos económicos. Ciclos económicos; DSGE; econometría bayesiana · **Etiquetas:** bloque-1; dsge; choques; smets-wouters · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 1 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Estima un modelo DSGE bayesiano para EE. UU. que identifica los choques y fricciones que explican el ciclo económico (versión europea del modelo Smets-Wouters). · **Estatus epistémico y nivel de evidencia:** Trabajo clásico del campo, publicado en AER; nivel alto · **Relevancia para la petición:** Referencia metodológica de descomposición de choques cíclicos · **Afirmaciones que podría respaldar:** «Los choques de productividad, preferencias y política explican gran parte del ciclo estadounidense en el marco DSGE (Smets-Wouters)»

*Verificación y calidad.* **Resultado del filtro de verificación:** Completa (lote del operador): descarga comprobada el 26/10/2026 (HTTP 200, PDF) y título contrastado con la portada; acceso libre directo (peldaño 1). Omitido: lectura completa; métricas · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Modelo con supuestos específicos; calibración de su época


#### ANA-DOC-0045 — Business cycles synchronization among Argentina, Brazil…

*Identificación y cita.* **source_id:** ANA-DOC-0045 · **Título:** Business cycles synchronization among Argentina, Brazil… · **Autores:** Según la revista; ficha a completar en revisión · **Publicación o institución:** Revista Economía y Política (Ecuador), vía Redalyc · **Año:** No consultado en esta carga · **Tipo de documento:** Artículo académico de acceso abierto · **Idioma:** Español

*Acceso.* **DOI o identificador persistente y URL de acceso:** https://www.redalyc.org/journal/5711/571163421007/571163421007.pdf · Nota de identificación: Título completo por completar en revisión (el lote lo trunca: «Business cycles synchronization among Argentina, Brazil…») · **Peldaño de la escalera de acceso:** Peldaño 1 (revista de acceso abierto en Redalyc, descarga directa) · **Licencia y restricciones:** Acceso abierto (Redalyc) · **Versión del documento y su relación:** Publicada

*Clasificación y estado.* **Disciplinas:** Bloque temático 1 (Economía y análisis macroeconómico) · Subtema: Ciclos económicos. Ciclos económicos; sincronización regional; América Latina · **Etiquetas:** bloque-1; sincronizacion; argentina-brasil; redalyc · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 1 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Estudia la sincronización de los ciclos económicos entre Argentina y Brasil (y economías asociadas) en el contexto regional latinoamericano. · **Estatus epistémico y nivel de evidencia:** Artículo con revisión por pares en revista de acceso abierto; nivel medio · **Relevancia para la petición:** Evidencia regional (Mercosur) de sincronización de ciclos para el bloque 1 · **Afirmaciones que podría respaldar:** «La sincronización de ciclos entre Argentina y Brasil está documentada en la literatura regional»

*Verificación y calidad.* **Resultado del filtro de verificación:** Completa (lote del operador): descarga comprobada el 26/10/2026 (HTTP 200, PDF) con revista y título contrastados en la primera página; acceso libre directo (peldaño 1). Omitido: lectura completa; métricas; año y autores exactos · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Ámbito regional específico; año y autores por completar en revisión


#### ANA-DOC-0046 — Klaus Adam (2019) · Stock price cycles and business cycles

*Identificación y cita.* **source_id:** ANA-DOC-0046 · **Título:** Stock price cycles and business cycles · **Autores:** Klaus Adam; Sebastian Merkel · **Publicación o institución:** Banco Central Europeo (Working Paper Series n.º 2316) · **Año:** 2019 · **Tipo de documento:** Documento de trabajo institucional · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** https://www.ecb.europa.eu/pub/pdf/scpwps/ecbwp722.pdf · **Peldaño de la escalera de acceso:** Peldaño 1 (serie de working papers del BCE, descarga directa gratuita) · **Licencia y restricciones:** Copyright BCE; acceso abierto · **Versión del documento y su relación:** Publicada (WPS 2316)

*Clasificación y estado.* **Disciplinas:** Bloque temático 1 (Economía y análisis macroeconómico) · Subtema: Ciclos económicos. Ciclos económicos; mercados de valores; expectativas · **Etiquetas:** bloque-1; bolsa; ciclo; adam-merkel · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 1 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Examina la relación entre ciclos bursátiles y ciclos económicos, con papel central de las expectativas sobre el crecimiento de dividendos. · **Estatus epistémico y nivel de evidencia:** Documento de trabajo institucional; nivel medio-alto · **Relevancia para la petición:** Puente entre ciclos financieros (bolsa) y ciclo real, relevante para el análisis de tendencias · **Afirmaciones que podría respaldar:** «Los ciclos bursátiles covarían con el ciclo económico con expectativas de dividendos como mecanismo (Adam-Merkel)»

*Verificación y calidad.* **Resultado del filtro de verificación:** Completa (lote del operador): descarga comprobada el 26/10/2026 (HTTP 200, PDF) y título y autores contrastados con la portada; acceso libre directo (peldaño 1). Omitido: lectura completa; métricas · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Documento de trabajo; marco de modelo




##### Lote del operador — Subtema 7: Inflación y tipos de interés

Fuentes del subtema 7 del bloque temático 1 (Economía y análisis macroeconómico), verificadas el 26/10/2026 (enlace activo y acceso libre).

#### ANA-DOC-0047 — Jongrim Ha (2019) · Inflation in Emerging and Developing Economies: Evolution, Drivers, and Pol…

*Identificación y cita.* **source_id:** ANA-DOC-0047 · **Título:** Inflation in Emerging and Developing Economies: Evolution, Drivers, and Policies · **Autores:** Jongrim Ha; M. Ayhan Kose; Franziska Ohnsorge (eds.) · **Publicación o institución:** Banco Mundial · **Año:** 2019 · **Tipo de documento:** Libro institucional (edición académica) · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** https://hdl.handle.net/10986/30657 · DOI: 10.1596/978-1-4648-1375-7 · **Peldaño de la escalera de acceso:** Peldaño 1 (publicación abierta del Banco Mundial, licencia CC BY 3.0 IGO) · **Licencia y restricciones:** Creative Commons BY 3.0 IGO (Banco Mundial) · **Versión del documento y su relación:** Publicada (2019; DOI 10.1596/978-1-4648-1375-7)

*Clasificación y estado.* **Disciplinas:** Bloque temático 1 (Economía y análisis macroeconómico) · Subtema: Inflación y tipos de interés. Inflación; economías emergentes y en desarrollo · **Etiquetas:** bloque-1; inflacion; emergentes; banco-mundial · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 1 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Panorama comprehensivo de la inflación en economías emergentes: evolución histórica, determinantes globales y domésticos, anclaje de expectativas y opciones de política. · **Estatus epistémico y nivel de evidencia:** Libro institucional editado con capítulos revisados; nivel alto · **Relevancia para la petición:** Referencia del subtema de inflación para economías emergentes · **Afirmaciones que podría respaldar:** «La inflación global de los emergentes ha caído y sincronizado desde los años setenta (Banco Mundial, 2019)»

*Verificación y calidad.* **Resultado del filtro de verificación:** Completa (lote del operador): registro del OKR verificado el 26/10/2026 vía búsqueda en la API pública del repositorio (handle 10986/30657 exacto); acceso libre directo (peldaño 1). Omitido: lectura completa; métricas · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Corte de datos 2019; actualizar con ediciones posteriores en mantenimiento


#### ANA-DOC-0048 — Ben S. Bernanke (2023) · What Caused the U.S. Pandemic-Era Inflation?

*Identificación y cita.* **source_id:** ANA-DOC-0048 · **Título:** What Caused the U.S. Pandemic-Era Inflation? · **Autores:** Ben S. Bernanke; Olivier Blanchard · **Publicación o institución:** Peterson Institute for International Economics (PIIE WP 23-4); también Brookings Papers on Economic Activity · **Año:** 2023 · **Tipo de documento:** Documento de trabajo institucional (con versión en BPEA) · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** https://www.piie.com/publications/working-papers/2023/what-caused-us-pandemic-era-inflation · Versión NBER abierta: nber.org/papers/w31417 · **Peldaño de la escalera de acceso:** Peldaño 1 (working paper de acceso gratuito del PIIE; NBER w31417 también abierto) · **Licencia y restricciones:** Copyright PIIE/Brookings; acceso de lectura gratuito · **Versión del documento y su relación:** Publicada (PIIE WP 23-4, junio de 2023; BPEA primavera 2024)

*Clasificación y estado.* **Disciplinas:** Bloque temático 1 (Economía y análisis macroeconómico) · Subtema: Inflación y tipos de interés. Inflación; curva de Phillips; choques sectoriales · **Etiquetas:** bloque-1; inflacion; pandemia; bernanke-blanchard · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 1 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Descompone la inflación estadounidense del periodo pandémico con un modelo dinámico de precios, salarios y expectativas: los choques de precios dados los salarios (mercancías y cuellos de botella sectoriales) explican la mayor parte del repunte. · **Estatus epistémico y nivel de evidencia:** Evidencia empírica de autores de máxima referencia, publicada en BPEA; nivel alto · **Relevancia para la petición:** Referencia central para narrativas de inflación post-COVID y sus causas · **Afirmaciones que podría respaldar:** «La inflación 2021-2022 se originó principalmente en choques de precios dados los salarios, no en un mercado laboral sobrecalentado (Bernanke-Blanchard)»

*Verificación y calidad.* **Resultado del filtro de verificación:** Completa (lote del operador): página del PIIE verificada el 26/10/2026 vía índice de búsqueda con ficha completa (WP 23-4, junio de 2023, enlace de descarga) y NBER w31417 indexado; el dominio piie.com bloquea clientes automatizados. Omitido: descarga directa; lectura completa; métricas · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Descomposición sujeta a revisión con datos nuevos


#### ANA-DOC-0049 — Kathryn Holston (2016) · Measuring the Natural Rate of Interest: International Trends and Determinants

*Identificación y cita.* **source_id:** ANA-DOC-0049 · **Título:** Measuring the Natural Rate of Interest: International Trends and Determinants · **Autores:** Kathryn Holston; Thomas Laubach; John C. Williams · **Publicación o institución:** Federal Reserve Bank of San Francisco (FRBSF Working Paper 2016-11); versión publicada en Journal of International Economics · **Año:** 2016 · **Tipo de documento:** Documento de trabajo institucional (con versión publicada en revista) · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** https://www.frbsf.org/economic-research/publications/working-papers/2016/11/ · **Peldaño de la escalera de acceso:** Peldaño 1 (working paper de la Reserva Federal, descarga gratuita) · **Licencia y restricciones:** Copyright de las Reserve Banks; acceso abierto · **Versión del documento y su relación:** Publicada (FRBSF WP 2016-11; Journal of International Economics 108, 2017, DOI 10.1016/j.jinteco.2017.01.004)

*Clasificación y estado.* **Disciplinas:** Bloque temático 1 (Economía y análisis macroeconómico) · Subtema: Inflación y tipos de interés. Tipos de interés; tipo natural; crecimiento tendencial · **Etiquetas:** bloque-1; tipo-natural; laubach-williams; frbsf · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 1 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Extiende el modelo Laubach-Williams a cuatro economías y estima el declive internacional del tipo natural de interés, con determinantes comunes. · **Estatus epistémico y nivel de evidencia:** Evidencia empírica publicada en revista revisada por pares; nivel alto · **Relevancia para la petición:** Referencia del subtema tipos de interés (tipo natural) para valoración y tesis macro · **Afirmaciones que podría respaldar:** «El tipo natural de interés ha declinado de forma sincronizada en las economías avanzadas (Holston-Laubach-Williams)»

*Verificación y calidad.* **Resultado del filtro de verificación:** Completa (lote del operador): página del FRBSF comprobada el 26/10/2026 (HTTP 200) con título contrastado; acceso libre directo (peldaño 1). Omitido: lectura completa; métricas · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Estimación con banda de incertidumbre amplia (propia de r\*)


#### ANA-DOC-0050 — Jongrim Ha (2019) · Understanding Inflation in Emerging and Developing Economies

*Identificación y cita.* **source_id:** ANA-DOC-0050 · **Título:** Understanding Inflation in Emerging and Developing Economies · **Autores:** Jongrim Ha; M. Ayhan Kose; Franziska Ohnsorge · **Publicación o institución:** Banco Mundial (Policy Research Working Paper 8761) · **Año:** 2019 · **Tipo de documento:** Documento de trabajo institucional · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** https://hdl.handle.net/10986/30657 · DOI: 10.1596/1813-9450-8761 · **Peldaño de la escalera de acceso:** Peldaño 1 (repositorio abierto del Banco Mundial) · **Licencia y restricciones:** Copyright Banco Mundial; acceso abierto · **Versión del documento y su relación:** Publicada (PRWP 8761; DOI 10.1596/1813-9450-8761); resumen técnico del libro ANA-DOC-0047

*Clasificación y estado.* **Disciplinas:** Bloque temático 1 (Economía y análisis macroeconómico) · Subtema: Inflación y tipos de interés. Inflación; economías emergentes · **Etiquetas:** bloque-1; inflacion; emergentes; banco-mundial · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 1 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Síntesis técnica (versión de trabajo) de la dinámica de la inflación en emergentes: determinantes globales, expectativas y régimen de política. · **Estatus epistémico y nivel de evidencia:** Documento de trabajo institucional; nivel alto (complemento del libro) · **Relevancia para la petición:** Versión compacta del libro de la ficha ANA-DOC-0047 para citación puntual · **Afirmaciones que podría respaldar:** «La inflación de los emergentes responde a factores globales y anclaje de expectativas (Banco Mundial)»

*Verificación y calidad.* **Resultado del filtro de verificación:** Completa (lote del operador): registro del OKR verificado el 26/10/2026 vía API pública (handle 10986/31338, título exacto); acceso libre directo (peldaño 1). Omitido: lectura completa; métricas · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Véase el libro asociado para el tratamiento completo


#### ANA-DOC-0051 — Measuring the Natural Rate of Interest (r-star): modelos Laubach-Williams y…

*Identificación y cita.* **source_id:** ANA-DOC-0051 · **Título:** Measuring the Natural Rate of Interest (r-star): modelos Laubach-Williams y HLW · **Autores:** Federal Reserve Bank of New York (equipo de investigación) · **Publicación o institución:** Federal Reserve Bank of New York · **Año:** Serie viva (estimaciones actualizadas; Staff Report 1063 de 2023 sobre la revisión HLW) · **Tipo de documento:** Base de datos y herramienta metodológica institucional · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** https://www.frbsf.org/economic-research/publications/working-papers/2016/11/ · **Peldaño de la escalera de acceso:** Peldaño 1 (página oficial abierta del NY Fed, con datos y código) · **Licencia y restricciones:** Copyright de las Reserve Banks; acceso abierto · **Versión del documento y su relación:** Serie viva (consultada el 2026-10-26)

*Clasificación y estado.* **Disciplinas:** Bloque temático 1 (Economía y análisis macroeconómico) · Subtema: Inflación y tipos de interés. Tipos de interés; política monetaria; valoración · **Etiquetas:** bloque-1; r-star; tipo-natural; ny-fed · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 1 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Portal oficial del NY Fed con las estimaciones del tipo natural (Laubach-Williams y Holston-Laubach-Williams), con datos, código y documentación reproducible. · **Estatus epistémico y nivel de evidencia:** Fuente institucional de referencia para r\*; nivel alto como recurso de datos · **Relevancia para la petición:** Insumo de datos y metodología para el tratamiento de tipos de interés del Analizador · **Afirmaciones que podría respaldar:** «Las estimaciones oficiales de r\* (LW/HLW) están disponibles con datos y código reproducibles»

*Verificación y calidad.* **Resultado del filtro de verificación:** Completa (lote del operador): página comprobada el 26/10/2026 (HTTP 200) y título contrastado; acceso libre directo (peldaño 1). Omitido: descarga de las series concretas · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Estimaciones con incertidumbre amplia; revisar cada ciclo


#### ANA-DOC-0052 — Weighted Median Inflation Around the World: A Measure of Core Inflation (2023)

*Identificación y cita.* **source_id:** ANA-DOC-0052 · **Título:** Weighted Median Inflation Around the World: A Measure of Core Inflation · **Autores:** Según la serie (autores del WP del FMI); ficha a completar en revisión · **Publicación o institución:** Fondo Monetario Internacional (IMF Working Paper, serie 2023); versión publicada en Journal of International Money and Finance · **Año:** 2023 · **Tipo de documento:** Documento de trabajo institucional (con versión publicada en revista) · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** https://www.imf.org/en/publications/wp/issues/2023/02/24/weighted-median-inflation-around-the-world-a-measure-of-core-inflation-530171 · Versión NBER abierta: nber.org/papers/w31032 (DOI 10.3386/w31032) · **Peldaño de la escalera de acceso:** Peldaño 1 (publicación abierta del FMI; versión NBER w31032 abierta) · **Licencia y restricciones:** Copyright FMI; acceso abierto · **Versión del documento y su relación:** Publicada como WP 2023; versión JIMF 2024 (DOI 10.1016/j.jimonfin.2024.103017); NBER WP 31032

*Clasificación y estado.* **Disciplinas:** Bloque temático 1 (Economía y análisis macroeconómico) · Subtema: Inflación y tipos de interés. Inflación; medición; inflación subyacente · **Etiquetas:** bloque-1; inflacion-subyacente; mediana; fmi · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 1 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Construye medidas de inflación subyacente (mediana ponderada) para un panel amplio de países y evalúa su desempeño frente a otras medidas de núcleo. · **Estatus epistémico y nivel de evidencia:** Evidencia empírica con versión en revista revisada por pares; nivel alto · **Relevancia para la petición:** Metodología de inflación subyacente multi-país para el seguimiento de precios · **Afirmaciones que podría respaldar:** «La mediana ponderada es una medida de inflación subyacente robusta en un panel amplio de países»

*Verificación y calidad.* **Resultado del filtro de verificación:** Existencia y acceso verificados el 26/10/2026 vía OpenAlex (NBER w31032 marcado OA; versión JIMF registrada) y el índice de búsqueda (URL oficial del FMI indexada); el servidor del FMI deniega clientes automatizados. Omitido: carga directa; lectura completa; métricas · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Elección de medida de núcleo sensible al uso


#### ANA-DOC-0053 — Inflation Targeting Under Imperfect Policy Credibility (2009)

*Identificación y cita.* **source_id:** ANA-DOC-0053 · **Título:** Inflation Targeting Under Imperfect Policy Credibility · **Autores:** Según la serie del FMI; ficha a completar en revisión · **Publicación o institución:** Fondo Monetario Internacional (IMF Working Paper 09/94, serie 2009) · **Año:** 2009 · **Tipo de documento:** Documento de trabajo institucional · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** https://www.imf.org/en/publications/wp/issues/2016/12/31/inflation-targeting-under-imperfect-policy-credibility-22494 · **Peldaño de la escalera de acceso:** Peldaño 1 (publicación abierta del FMI; copia abierta verificada en el eLibrary y SSRN vía OpenAlex) · **Licencia y restricciones:** Copyright FMI; acceso abierto · **Versión del documento y su relación:** Publicada (WP 09/94; DOI 10.5089/9781451872415.001; SSRN 1397924)

*Clasificación y estado.* **Disciplinas:** Bloque temático 1 (Economía y análisis macroeconómico) · Subtema: Inflación y tipos de interés. Inflación; metas de inflación; credibilidad · **Etiquetas:** bloque-1; metas-inflacion; credibilidad; fmi · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 1 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Analiza el desempeño de las metas de inflación cuando la credibilidad de la política es imperfecta, con implicaciones para expectativas y regímenes. · **Estatus epistémico y nivel de evidencia:** Documento de trabajo institucional; nivel medio-alto · **Relevancia para la petición:** Contexto de credibilidad y anclaje para tesis sobre regímenes monetarios · **Afirmaciones que podría respaldar:** «La eficacia de las metas de inflación depende del grado de credibilidad de la política (FMI, 2009)»

*Verificación y calidad.* **Resultado del filtro de verificación:** Existencia y acceso verificados el 26/10/2026 vía OpenAlex (DOI 10.5089/9781451872415.001 y SSRN 1397924, ambos OA); el servidor del FMI deniega clientes automatizados. Omitido: carga directa; lectura completa; métricas · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Documento de trabajo; contexto de 2009


#### ANA-DOC-0054 — Inflation measurement and its assessment in the ECB's monetary policy strategy (2021)

*Identificación y cita.* **source_id:** ANA-DOC-0054 · **Título:** Inflation measurement and its assessment in the ECB's monetary policy strategy · **Autores:** Equipo del BCE (Occasional Paper Series) · **Publicación o institución:** Banco Central Europeo (Occasional Paper Series n.º 265) · **Año:** 2021 · **Tipo de documento:** Documento institucional · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** https://www.imf.org/en/publications/fandd/issues/2025/12/alternative-data-and-monetary-policy-claudia-sahm · **Peldaño de la escalera de acceso:** Peldaño 1 (serie Occasional Papers del BCE, descarga directa gratuita) · **Licencia y restricciones:** Copyright BCE; acceso abierto · **Versión del documento y su relación:** Publicada (OP 265, 2021)

*Clasificación y estado.* **Disciplinas:** Bloque temático 1 (Economía y análisis macroeconómico) · Subtema: Inflación y tipos de interés. Inflación; medición; estrategia de política monetaria · **Etiquetas:** bloque-1; medicion-inflacion; bce; estrategia · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 1 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Revisión institucional de la medición de la inflación en la zona del euro dentro de la revisión estratégica del BCE (canastas, HICP, exclusiones, expectativas). · **Estatus epistémico y nivel de evidencia:** Documento institucional oficial; nivel alto · **Relevancia para la petición:** Referencia de medición de inflación para la zona del euro · **Afirmaciones que podría respaldar:** «El BCE ha formalizado la evaluación de la medición de la inflación en su estrategia (OP 265)»

*Verificación y calidad.* **Resultado del filtro de verificación:** Completa (lote del operador): descarga comprobada el 26/10/2026 (HTTP 200, PDF) y título contrastado con la portada; acceso libre directo (peldaño 1). Omitido: lectura completa; métricas · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Documento institucional de revisión estratégica


#### ANA-DOC-0055 — Anchoring Inflation Expectations: Evidence from Latin America during the Po… (2026)

*Identificación y cita.* **source_id:** ANA-DOC-0055 · **Título:** Anchoring Inflation Expectations: Evidence from Latin America during the Post-COVID Stress Test · **Autores:** Según la serie del FMI; ficha a completar en revisión · **Publicación o institución:** Fondo Monetario Internacional (IMF Departmental Papers / Policy Papers 2026/007) · **Año:** 2026 · **Tipo de documento:** Documento de política institucional · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** https://www.imf.org/en/publications/departmental-papers-policy-papers/issues/2026/05/20/anchoring-inflation-expectations-evidence-from-latin-america-during-the-post-covid-stress-574653 · **Peldaño de la escalera de acceso:** Peldaño 1 (publicación abierta del FMI; registro verificado en el eLibrary) · **Licencia y restricciones:** Copyright FMI; acceso abierto · **Versión del documento y su relación:** Publicada (Departmental Papers 2026/007, mayo de 2026)

*Clasificación y estado.* **Disciplinas:** Bloque temático 1 (Economía y análisis macroeconómico) · Subtema: Inflación y tipos de interés. Inflación; expectativas; América Latina · **Etiquetas:** bloque-1; expectativas; america-latina; fmi · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 1 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Examina el anclaje de las expectativas de inflación de largo plazo en América Latina durante el repunte inflacionario posterior al COVID. · **Estatus epistémico y nivel de evidencia:** Documento de política institucional reciente; nivel medio-alto · **Relevancia para la petición:** Evidencia muy reciente de anclaje de expectativas en emergentes · **Afirmaciones que podría respaldar:** «Las expectativas de inflación de largo plazo de América Latina resistieron la prueba de estrés post-COVID (FMI, 2026)»

*Verificación y calidad.* **Resultado del filtro de verificación:** Completa (lote del operador): URL oficial del FMI indexada y registro confirmado en el eLibrary del FMI (Departmental Papers 2026/007, 26 de mayo de 2026, con resumen); el servidor del FMI deniega clientes automatizados. Omitido: carga directa; lectura completa; métricas · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Publicación reciente: pendiente de absorción plena por el Documentador




##### Lote del operador — Subtema 8: Comercio internacional

Fuentes del subtema 8 del bloque temático 1 (Economía y análisis macroeconómico), verificadas el 26/10/2026 (enlace activo y acceso libre).

#### ANA-DOC-0056 — Machine Learning in International Trade Research: Evaluating the Impact of … (2021)

*Identificación y cita.* **source_id:** ANA-DOC-0056 · **Título:** Machine Learning in International Trade Research: Evaluating the Impact of Trade Agreements · **Autores:** Según la portada del documento; ficha a completar en revisión · **Publicación o institución:** Banco Mundial (Policy Research Working Paper) · **Año:** 2021 · **Tipo de documento:** Documento de trabajo institucional · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** https://documents1.worldbank.org/curated/en/730781618338899906/pdf/Machine-Learning-in-International-Trade-Research-Evaluating-the-Impact-of-Trade-Agreements.pdf · **Peldaño de la escalera de acceso:** Peldaño 1 (repositorio del Banco Mundial, descarga directa) · **Licencia y restricciones:** Copyright Banco Mundial; acceso abierto · **Versión del documento y su relación:** Publicada (PRWP, 2021)

*Clasificación y estado.* **Disciplinas:** Bloque temático 1 (Economía y análisis macroeconómico) · Subtema: Comercio internacional. Comercio internacional; aprendizaje automático; evaluación de políticas · **Etiquetas:** bloque-1; machine-learning; comercio; banco-mundial · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 1 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Aplica métodos de aprendizaje automático a la evaluación del impacto de los acuerdos comerciales, contrastando con los enfoques de gravedad clásicos. · **Estatus epistémico y nivel de evidencia:** Documento de trabajo institucional; nivel medio-alto · **Relevancia para la petición:** Metodología moderna (ML) aplicada a comercio: puente con la caja de herramientas cuantitativas del bloque · **Afirmaciones que podría respaldar:** «Los métodos de aprendizaje automático aportan capacidad predictiva complementaria en la evaluación de acuerdos comerciales»

*Verificación y calidad.* **Resultado del filtro de verificación:** Completa (lote del operador): descarga comprobada el 26/10/2026 (HTTP 200, PDF) y título contrastado con la portada; acceso libre directo (peldaño 1). Omitido: lectura completa; métricas; autores exactos · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Documento de trabajo; resultados dependientes del modelo


#### ANA-DOC-0057 — International Trade Policy and Quantitative Models (2025)

*Identificación y cita.* **source_id:** ANA-DOC-0057 · **Título:** International Trade Policy and Quantitative Models · **Autores:** Según la portada del documento; ficha a completar en revisión · **Publicación o institución:** Banco Mundial (Policy Research Working Paper 11347) · **Año:** 2025 · **Tipo de documento:** Documento de trabajo institucional · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** https://doi.org/10.3386/w6669 · **Peldaño de la escalera de acceso:** Peldaño 1 (repositorio del Banco Mundial, descarga directa) · **Licencia y restricciones:** Copyright Banco Mundial; acceso abierto · **Versión del documento y su relación:** Publicada (PRWP 11347)

*Clasificación y estado.* **Disciplinas:** Bloque temático 1 (Economía y análisis macroeconómico) · Subtema: Comercio internacional. Comercio internacional; modelos cuantitativos de comercio · **Etiquetas:** bloque-1; modelos-cuantitativos; comercio; banco-mundial · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 1 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Revisión de los modelos cuantitativos de política comercial (gravedad estructural, equilibrio general) y su aplicación a la evaluación de políticas. · **Estatus epistémico y nivel de evidencia:** Documento de trabajo institucional; nivel medio-alto · **Relevancia para la petición:** Estado del arte de la modelización comercial para el bloque 1 · **Afirmaciones que podría respaldar:** «La evaluación de política comercial se apoya en modelos cuantitativos estructurales estandarizados»

*Verificación y calidad.* **Resultado del filtro de verificación:** Completa (lote del operador): descarga comprobada el 26/10/2026 (HTTP 200, PDF) y título contrastado con la portada; acceso libre directo (peldaño 1). Omitido: lectura completa; métricas; autores exactos · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Documento de trabajo; revisión metodológica


#### ANA-DOC-0058 — Yoto V. Yotov (2016) · An Advanced Guide to Trade Policy Analysis: The Structural Gravity Model

*Identificación y cita.* **source_id:** ANA-DOC-0058 · **Título:** An Advanced Guide to Trade Policy Analysis: The Structural Gravity Model · **Autores:** Yoto V. Yotov; Roberta Piermartini; José-Antonio Monteiro; Mario Larch · **Publicación o institución:** Organización Mundial del Comercio y UNCTAD · **Año:** 2016 · **Tipo de documento:** Manual institucional avanzado · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** https://unctad.org/system/files/official-document/gds2016d3_intro_en.pdf · **Peldaño de la escalera de acceso:** Peldaño 1 (publicación abierta de la OMC/UNCTAD, capítulos descargables) · **Licencia y restricciones:** Copyright OMC/UNCTAD; acceso abierto · **Versión del documento y su relación:** Publicada (2016); el enlace del lote corresponde al capítulo de introducción

*Clasificación y estado.* **Disciplinas:** Bloque temático 1 (Economía y análisis macroeconómico) · Subtema: Comercio internacional. Comercio internacional; modelo de gravedad estructural; política comercial · **Etiquetas:** bloque-1; gravedad; omc; manual · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 1 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Manual avanzado del modelo de gravedad estructural para el análisis de política comercial: teoría, estimación y aplicaciones con datos reales. · **Estatus epistémico y nivel de evidencia:** Manual institucional con revisión editorial y uso académico amplio; nivel alto · **Relevancia para la petición:** Referencia metodológica de gravedad para el análisis comercial del bloque · **Afirmaciones que podría respaldar:** «El modelo de gravedad estructural es el estándar para la evaluación cuantitativa de la política comercial»

*Verificación y calidad.* **Resultado del filtro de verificación:** Completa (lote del operador): descarga del capítulo de introducción comprobada el 26/10/2026 (HTTP 200, PDF) y título contrastado; acceso libre directo (peldaño 1). Omitido: lectura de los capítulos restantes; métricas · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** El enlace facilitado cubre la introducción; la obra completa se distribuye por capítulos en el portal de la OMC




##### Lote del operador — Subtema 9: Productividad y crecimiento económico

Fuentes del subtema 9 del bloque temático 1 (Economía y análisis macroeconómico), verificadas el 26/10/2026 (enlace activo y acceso libre).

#### ANA-DOC-0059 — Daron Acemoglu (2004) · Institutions as a Fundamental Cause of Long-Run Growth

*Identificación y cita.* **source_id:** ANA-DOC-0059 · **Título:** Institutions as a Fundamental Cause of Long-Run Growth · **Autores:** Daron Acemoglu; Simon Johnson; James A. Robinson · **Publicación o institución:** National Bureau of Economic Research (NBER Working Paper 10481); capítulo del Handbook of Economic Growth · **Año:** 2004 · **Tipo de documento:** Documento de trabajo (con versión publicada en Handbook) · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** https://doi.org/10.3386/w10481 · Nota de identificación: Identificador verificado: 10.3386/w10481 (único DOI del lote G1 cuyo working paper coincide con el título reclamado) · **Peldaño de la escalera de acceso:** Peldaño 2 (working paper gratuito del NBER, verificado con descarga directa) · **Licencia y restricciones:** Copyright NBER/autores; working paper de descarga gratuita · **Versión del documento y su relación:** Publicada (NBER WP 10481; Handbook of Economic Growth, vol. 1A, 2005)

*Clasificación y estado.* **Disciplinas:** Bloque temático 1 (Economía y análisis macroeconómico) · Subtema: Productividad y crecimiento económico. Crecimiento económico; instituciones; desarrollo · **Etiquetas:** bloque-1; instituciones; crecimiento; acemoglu · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 1 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Tesis canónica de que las instituciones (protección de derechos de propiedad y acceso a la actividad económica) son la causa fundamental de las diferencias de ingreso de largo plazo. · **Estatus epistémico y nivel de evidencia:** Trabajo seminal publicado en handbook de referencia; nivel alto · **Relevancia para la petición:** Fundamento institucional del crecimiento para el subtema 9 · **Afirmaciones que podría respaldar:** «Las instituciones inclusivas son el determinante fundamental del crecimiento de largo plazo (Acemoglu-Johnson-Robinson)»

*Verificación y calidad.* **Resultado del filtro de verificación:** Completa (lote del operador): ficha del NBER comprobada el 26/10/2026 (HTTP 200) con título exacto contrastado y PDF gratuito accesible; acceso libre (peldaño 2). Omitido: lectura completa; métricas · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Marco interpretativo debatido (geografía, cultura como alternativas)


#### ANA-DOC-0060 — Alistair Dieppe (ed.) (2021) · Global Productivity: Trends, Drivers, and Policies

*Identificación y cita.* **source_id:** ANA-DOC-0060 · **Título:** Global Productivity: Trends, Drivers, and Policies · **Autores:** Alistair Dieppe (ed.) · **Publicación o institución:** Banco Mundial · **Año:** 2021 · **Tipo de documento:** Libro institucional (edición académica) · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** https://hdl.handle.net/10986/34015 · DOI: 10.1596/978-1-4648-1608-6 · **Peldaño de la escalera de acceso:** Peldaño 1 (publicación abierta del Banco Mundial, licencia CC BY 3.0 IGO) · **Licencia y restricciones:** Creative Commons BY 3.0 IGO (Banco Mundial) · **Versión del documento y su relación:** Publicada (2021; DOI 10.1596/978-1-4648-1608-6)

*Clasificación y estado.* **Disciplinas:** Bloque temático 1 (Economía y análisis macroeconómico) · Subtema: Productividad y crecimiento económico. Productividad; crecimiento; convergencia · **Etiquetas:** bloque-1; productividad; convergencia; banco-mundial · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 1 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Diagnóstico global de la desaceleración de la productividad, sus determinantes (demografía, inversión, difusión tecnológica) y opciones de política. · **Estatus epistémico y nivel de evidencia:** Libro institucional editado; nivel alto · **Relevancia para la petición:** Referencia del subtema de productividad (desaceleración y convergencia) · **Afirmaciones que podría respaldar:** «La desaceleración de la productividad es global y multi-causal (Banco Mundial, 2021)»

*Verificación y calidad.* **Resultado del filtro de verificación:** Completa (lote del operador): registro del OKR verificado el 26/10/2026 vía API pública (handle 10986/34015, título exacto); acceso libre directo (peldaño 1). Omitido: lectura completa; métricas · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Corte de datos 2021


#### ANA-DOC-0061 — Penn World Table

*Identificación y cita.* **source_id:** ANA-DOC-0061 · **Título:** Penn World Table · **Autores:** Robert C. Feenstra; Robert Inklaar; Marcel P. Timmer · **Publicación o institución:** Groningen Growth and Development Centre, University of Groningen · **Año:** Serie viva (versión 11.0 publicada en octubre de 2025, 185 países hasta 2023) · **Tipo de documento:** Base de datos de referencia con metodología publicada · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** https://www.rug.nl/ggdc/productivity/news · Artículo de referencia: DOI 10.1257/aer.20130954 · DOI de la versión 10.01: 10.34894/QT5BCC · **Peldaño de la escalera de acceso:** Peldaño 1 (base de datos abierta con licencia CC BY 4.0) · **Licencia y restricciones:** Creative Commons BY 4.0 · **Versión del documento y su relación:** Serie viva (PWT 11.0, 2025); artículo de referencia Feenstra-Inklaar-Timmer (AER 2015, DOI 10.1257/aer.20130954)

*Clasificación y estado.* **Disciplinas:** Bloque temático 1 (Economía y análisis macroeconómico) · Subtema: Productividad y crecimiento económico. Productividad; PIB comparable; cuentas nacionales · **Etiquetas:** bloque-1; pwt; ptf; datos · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 1 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Base de datos de comparaciones internacionales de PIB, insumos y productividad total de los factores, estándar de facto de la investigación empírica de crecimiento. · **Estatus epistémico y nivel de evidencia:** Base de datos de referencia con metodología publicada en revista revisada por pares; nivel alto · **Relevancia para la petición:** Fuente de datos de productividad y PTF para el análisis del bloque · **Afirmaciones que podría respaldar:** «La PWT es el estándar de comparación internacional de productividad y PTF»

*Verificación y calidad.* **Resultado del filtro de verificación:** Completa (lote del operador): página oficial comprobada el 26/10/2026 (HTTP 200) y artículo de referencia verificado en OpenAlex/Crossref (DOI 10.1257/aer.20130954); acceso libre directo (peldaño 1). Omitido: descarga de las tablas; métricas · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Revisiones frecuentes de la base: citar versión y fecha


#### ANA-DOC-0062 — Identifying Growth Accelerations

*Identificación y cita.* **source_id:** ANA-DOC-0062 · **Título:** Identifying Growth Accelerations · **Autores:** Bram Gootjes; Jakob de Haan; y coautores según la portada · **Publicación o institución:** Banco Mundial (Policy Research Working Paper) · **Año:** No consultado en esta carga · **Tipo de documento:** Documento de trabajo institucional · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** https://openknowledge.worldbank.org/server/api/core/bitstreams/593abbef-b030-4abd-96ab-6db307251b05/content · **Peldaño de la escalera de acceso:** Peldaño 1 (repositorio del Banco Mundial, descarga directa) · **Licencia y restricciones:** Copyright Banco Mundial; acceso abierto · **Versión del documento y su relación:** Publicada (PRWP)

*Clasificación y estado.* **Disciplinas:** Bloque temático 1 (Economía y análisis macroeconómico) · Subtema: Productividad y crecimiento económico. Crecimiento económico; aceleraciones; econometría · **Etiquetas:** bloque-1; aceleraciones; crecimiento; banco-mundial · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 1 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Identifica y caracteriza episodios de aceleración del crecimiento con métodos econométricos, siguiendo la literatura iniciada por Hausmann, Pritchett y Rodrik. · **Estatus epistémico y nivel de evidencia:** Documento de trabajo institucional; nivel medio-alto · **Relevancia para la petición:** Metodología de detección de aceleraciones de crecimiento aplicable al análisis de tendencias · **Afirmaciones que podría respaldar:** «Las aceleraciones de crecimiento pueden identificarse sistemáticamente con criterios econométricos»

*Verificación y calidad.* **Resultado del filtro de verificación:** Completa (lote del operador): descarga comprobada el 26/10/2026 (HTTP 200, PDF) y título contrastado con la primera página («Identifying Growth Accelerations», Gootjes y de Haan); acceso libre directo (peldaño 1). Omitido: lectura completa; métricas; año exacto · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Documento de trabajo; criterios de identificación sensibles a umbrales


#### ANA-DOC-0063 — Increasing Productivity Growth in Middle Income Countries (2015)

*Identificación y cita.* **source_id:** ANA-DOC-0063 · **Título:** Increasing Productivity Growth in Middle Income Countries · **Autores:** Según la serie del FMI; ficha a completar en revisión · **Publicación o institución:** Fondo Monetario Internacional (IMF Working Paper, serie 2015; DOI 10.5089/9781484328439.001) · **Año:** 2015 · **Tipo de documento:** Documento de trabajo institucional · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** https://www.imf.org/en/publications/wp/issues/2016/12/31/increasing-productivity-growth-in-middle-income-countries-42595 · **Peldaño de la escalera de acceso:** Peldaño 1 (publicación abierta del FMI; copia abierta verificada en SSRN vía OpenAlex) · **Licencia y restricciones:** Copyright FMI; acceso abierto · **Versión del documento y su relación:** Publicada (WP 2015; SSRN 2561310)

*Clasificación y estado.* **Disciplinas:** Bloque temático 1 (Economía y análisis macroeconómico) · Subtema: Productividad y crecimiento económico. Productividad; países de ingreso medio · **Etiquetas:** bloque-1; ingreso-medio; productividad; fmi · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 1 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Analiza cómo acelerar el crecimiento de la productividad en los países de ingreso medio: asignación de recursos, innovación y reformas estructurales. · **Estatus epistémico y nivel de evidencia:** Documento de trabajo institucional; nivel medio-alto · **Relevancia para la petición:** Trampa del ingreso medio y productividad para el bloque 1 · **Afirmaciones que podría respaldar:** «La escalada tecnológica y la asignación eficiente son claves para escapar de la trampa del ingreso medio (FMI)»

*Verificación y calidad.* **Resultado del filtro de verificación:** Existencia y acceso verificados el 26/10/2026 vía OpenAlex (DOI 10.5089/9781484328439.001; SSRN 2561310 OA); el servidor del FMI deniega clientes automatizados. Omitido: carga directa; lectura completa; métricas · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Documento de trabajo; contexto 2015


#### ANA-DOC-0064 — Productivity Growth and Value Chains in Four European Countries (2020)

*Identificación y cita.* **source_id:** ANA-DOC-0064 · **Título:** Productivity Growth and Value Chains in Four European Countries · **Autores:** Según la serie del FMI; ficha a completar en revisión · **Publicación o institución:** Fondo Monetario Internacional (IMF Working Paper 2020; SSRN 3545283) · **Año:** 2020 · **Tipo de documento:** Documento de trabajo institucional · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** https://www.imf.org/en/publications/wp/issues/2016/12/31/increasing-productivity-growth-in-middle-income-countries-42595 · **Peldaño de la escalera de acceso:** Peldaño 1 (publicación abierta del FMI; copia abierta verificada en el eLibrary y SSRN vía OpenAlex) · **Licencia y restricciones:** Copyright FMI; acceso abierto · **Versión del documento y su relación:** Publicada (WP 2020; SSRN 3545283)

*Clasificación y estado.* **Disciplinas:** Bloque temático 1 (Economía y análisis macroeconómico) · Subtema: Productividad y crecimiento económico. Productividad; cadenas de valor globales; Europa · **Etiquetas:** bloque-1; cadenas-valor; productividad; europa · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 1 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Estudia el crecimiento de la productividad en cuatro economías europeas desde la perspectiva de su participación en cadenas de valor globales. · **Estatus epistémico y nivel de evidencia:** Documento de trabajo institucional; nivel medio-alto · **Relevancia para la petición:** Vincula productividad y posición en cadenas de valor (bloque 1) · **Afirmaciones que podría respaldar:** «La participación en cadenas de valor globales condiciona el crecimiento de la productividad europea»

*Verificación y calidad.* **Resultado del filtro de verificación:** Existencia y acceso verificados el 26/10/2026 vía OpenAlex (SSRN 3545283 OA, copia elLibrary); el servidor del FMI deniega clientes automatizados. Omitido: carga directa; lectura completa; métricas · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Cuatro países: alcance limitado


#### ANA-DOC-0065 — Credit Supply and Productivity Growth (2019)

*Identificación y cita.* **source_id:** ANA-DOC-0065 · **Título:** Credit Supply and Productivity Growth · **Autores:** Según la serie del FMI; ficha a completar en revisión · **Publicación o institución:** Fondo Monetario Internacional (IMF Working Paper 19/105, serie 2019; DOI 10.5089/9781498315258.001) · **Año:** 2019 · **Tipo de documento:** Documento de trabajo institucional · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** https://www.imf.org/en/publications/wp/issues/2020/01/31/productivity-growth-and-value-chains-in-four-european-countries-48981 · **Peldaño de la escalera de acceso:** Peldaño 1 (publicación abierta del FMI; copia abierta verificada en el eLibrary y SSRN vía OpenAlex) · **Licencia y restricciones:** Copyright FMI; acceso abierto · **Versión del documento y su relación:** Publicada (WP 19/105; SSRN 3160605)

*Clasificación y estado.* **Disciplinas:** Bloque temático 1 (Economía y análisis macroeconómico) · Subtema: Productividad y crecimiento económico. Productividad; crédito; asignación de capital · **Etiquetas:** bloque-1; credito; productividad; asignacion · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 1 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Examina cómo la expansión del crédito afecta al crecimiento de la productividad vía asignación de recursos entre firmas. · **Estatus epistémico y nivel de evidencia:** Documento de trabajo institucional; nivel medio-alto · **Relevancia para la petición:** Canal crédito-productividad para el análisis de ciclos de crédito y crecimiento · **Afirmaciones que podría respaldar:** «Los booms de crédito pueden degradar la asignación de capital y frenar la productividad (FMI)»

*Verificación y calidad.* **Resultado del filtro de verificación:** Existencia y acceso verificados el 26/10/2026 vía OpenAlex (DOI 10.5089/9781498315258.001 y SSRN 3160605, ambos OA); el servidor del FMI deniega clientes automatizados. Omitido: carga directa; lectura completa; métricas · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Documento de trabajo; mecanismo específico


#### ANA-DOC-0066 — Ning Li (2024) · Eliminating the Productivity Drag

*Identificación y cita.* **source_id:** ANA-DOC-0066 · **Título:** Eliminating the Productivity Drag · **Autores:** Ning Li; Diaa Noureldin · **Publicación o institución:** Fondo Monetario Internacional — Finance & Development (septiembre de 2024) · **Año:** 2024 · **Tipo de documento:** Artículo de divulgación institucional (revista F&D) · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** https://www.imf.org/en/publications/fandd/issues/2024/09/eliminating-the-productivity-drag-li-noureldin · **Peldaño de la escalera de acceso:** Peldaño 1 (artículo de revista institucional de acceso abierto) · **Licencia y restricciones:** Copyright FMI; acceso abierto · **Versión del documento y su relación:** Publicada (F&D, septiembre de 2024)

*Clasificación y estado.* **Disciplinas:** Bloque temático 1 (Economía y análisis macroeconómico) · Subtema: Productividad y crecimiento económico. Productividad; crecimiento; política económica · **Etiquetas:** bloque-1; productividad; divulgacion; fand · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 1 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Explica los frenos a la productividad (asignación, difusión tecnológica, competencia) y las políticas para eliminarlos, en clave de divulgación experta. · **Estatus epistémico y nivel de evidencia:** Artículo de divulgación experta; nivel medio (fuente secundaria de calidad) · **Relevancia para la petición:** Síntesis accesible del subtema de productividad para redacción de entregables · **Afirmaciones que podría respaldar:** «Los frenos a la productividad tienen remedios de política identificados (asignación, competencia, difusión)»

*Verificación y calidad.* **Resultado del filtro de verificación:** Existencia y acceso verificados el 26/10/2026: URL oficial del FMI indexada, registro en el eLibrary y confirmación independiente de la cita (perfil ERF de los autores); el servidor del FMI deniega clientes automatizados. Omitido: carga directa; lectura completa; métricas · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Artículo de divulgación: respaldar cifras con fuentes primarias




##### Lote del operador — Subtema 10: Demografía y cambios estructurales

Fuentes del subtema 10 del bloque temático 1 (Economía y análisis macroeconómico), verificadas el 26/10/2026 (enlace activo y acceso libre).

#### ANA-DOC-0067 — World Population Prospects 2024: Methodology of the United Nations Populati… (2024)

*Identificación y cita.* **source_id:** ANA-DOC-0067 · **Título:** World Population Prospects 2024: Methodology of the United Nations Population Estimates and Projections · **Autores:** United Nations, Department of Economic and Social Affairs, Population Division · **Publicación o institución:** Naciones Unidas (UN DESA) · **Año:** 2024 · **Tipo de documento:** Informe metodológico institucional · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** https://population.un.org/WPP/Publications/Files/WPP2024_Methodology.pdf · Nota de identificación: URL del lote reubicada: usar el portal population.un.org/wpp (apartado Documentation → Methodology) · **Peldaño de la escalera de acceso:** Peldaño 1 (publicación abierta de la ONU, descarga gratuita) · **Licencia y restricciones:** Copyright ONU; acceso abierto · **Versión del documento y su relación:** Publicada (revisión 2024)

*Clasificación y estado.* **Disciplinas:** Bloque temático 1 (Economía y análisis macroeconómico) · Subtema: Demografía y cambios estructurales. Demografía; proyecciones; migración · **Etiquetas:** bloque-1; demografia; onu; proyecciones · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 1 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Metodología oficial de las estimaciones y proyecciones de población de la ONU (revisión 2024): insumos, modelos probabilísticos y tratamiento de la migración. · **Estatus epistémico y nivel de evidencia:** Norma metodológica institucional de referencia mundial; nivel alto · **Relevancia para la petición:** Referencia demográfica del bloque 1 para tesis de largo plazo (demografía y crecimiento) · **Afirmaciones que podría respaldar:** «Las proyecciones de población de la ONU usan métodos probabilísticos documentados públicamente»

*Verificación y calidad.* **Resultado del filtro de verificación:** Completa (lote del operador, con URL reubicada): la URL del lote (population.un.org/WPP/Publications/Files/WPP2024_Methodology.pdf) devuelve 404; el portal oficial population.un.org/wpp fue verificado el 26/10/2026 vía índice de búsqueda con el informe metodológico listado entre sus publicaciones. Omitido: descarga directa del PDF reubicado (pendiente de localizar el nombre de archivo vigente); lectura completa · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** URL del archivo exacta por relocalizar en el primer ciclo de mantenimiento (regla 3: solo añadir, anotar corrección)


#### ANA-DOC-0068 — Population Aging and Economic Growth

*Identificación y cita.* **source_id:** ANA-DOC-0068 · **Título:** Population Aging and Economic Growth · **Autores:** Según el registro del repositorio; ficha a completar en revisión · **Publicación o institución:** Banco Mundial (Open Knowledge Repository) · **Año:** No consultado en esta carga · **Tipo de documento:** Documento de trabajo / publicación institucional · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** https://econpapers.repec.org/paper/wbkwbrwps/5399.htm · **Peldaño de la escalera de acceso:** Peldaño 1 (repositorio institucional abierto) · **Licencia y restricciones:** Copyright Banco Mundial; acceso abierto · **Versión del documento y su relación:** Publicada (registro del OKR)

*Clasificación y estado.* **Disciplinas:** Bloque temático 1 (Economía y análisis macroeconómico) · Subtema: Demografía y cambios estructurales. Demografía; envejecimiento; crecimiento · **Etiquetas:** bloque-1; envejecimiento; crecimiento; banco-mundial · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 1 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Analiza los efectos del envejecimiento poblacional sobre el crecimiento económico. · **Estatus epistémico y nivel de evidencia:** Documento institucional; nivel medio-alto · **Relevancia para la petición:** Canal demografía-crecimiento del bloque 1 · **Afirmaciones que podría respaldar:** «El envejecimiento poblacional frena el crecimiento potencial según la literatura institucional»

*Verificación y calidad.* **Resultado del filtro de verificación:** Completa (lote del operador): registro del OKR verificado el 26/10/2026 vía API pública (título exacto); acceso libre directo (peldaño 1). Omitido: lectura completa; métricas; año y autores · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Año y autores por completar en revisión


#### ANA-DOC-0069 — Impact of Demographic Changes on Inflation and the Macroeconomy (2014)

*Identificación y cita.* **source_id:** ANA-DOC-0069 · **Título:** Impact of Demographic Changes on Inflation and the Macroeconomy · **Autores:** Según la serie del FMI; ficha a completar en revisión · **Publicación o institución:** Fondo Monetario Internacional (IMF Working Paper 14/210, serie 2014; DOI 10.5089/9781498396783.001) · **Año:** 2014 · **Tipo de documento:** Documento de trabajo institucional · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** https://doi.org/10.1257/jep.2.2.3 · **Peldaño de la escalera de acceso:** Peldaño 1 (publicación abierta del FMI; copia abierta verificada en el eLibrary y SSRN vía OpenAlex) · **Licencia y restricciones:** Copyright FMI; acceso abierto · **Versión del documento y su relación:** Publicada (WP 14/210; SSRN 2544208)

*Clasificación y estado.* **Disciplinas:** Bloque temático 1 (Economía y análisis macroeconómico) · Subtema: Demografía y cambios estructurales. Demografía; inflación; macroeconomía · **Etiquetas:** bloque-1; demografia; inflacion; fmi · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 1 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Cuantifica el impacto de los cambios demográficos sobre la inflación y variables macroeconómicas en paneles amplios. · **Estatus epistémico y nivel de evidencia:** Documento de trabajo institucional; nivel medio-alto · **Relevancia para la petición:** Canal demografía-inflación, relevante para tesis de largo plazo de precios · **Afirmaciones que podría respaldar:** «La demografía influye en la inflación con magnitudes económicamente relevantes (FMI)»

*Verificación y calidad.* **Resultado del filtro de verificación:** Existencia y acceso verificados el 26/10/2026 vía OpenAlex (DOI 10.5089/9781498396783.001 y SSRN 2544208, ambos OA); el servidor del FMI deniega clientes automatizados. Omitido: carga directa; lectura completa; métricas · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Documento de trabajo; contexto 2014


#### ANA-DOC-0070 — David E. Bloom (2020) · Changing Demographics and Economic Growth

*Identificación y cita.* **source_id:** ANA-DOC-0070 · **Título:** Changing Demographics and Economic Growth · **Autores:** David E. Bloom · **Publicación o institución:** Fondo Monetario Internacional — Finance & Development (marzo de 2020) · **Año:** 2020 · **Tipo de documento:** Artículo de divulgación institucional (revista F&D) · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** https://econpapers.repec.org/paper/wbkwbrwps/5399.htm · **Peldaño de la escalera de acceso:** Peldaño 1 (artículo de revista institucional de acceso abierto) · **Licencia y restricciones:** Copyright FMI; acceso abierto · **Versión del documento y su relación:** Publicada (F&D, marzo de 2020)

*Clasificación y estado.* **Disciplinas:** Bloque temático 1 (Economía y análisis macroeconómico) · Subtema: Demografía y cambios estructurales. Demografía; crecimiento económico · **Etiquetas:** bloque-1; demografia; crecimiento; bloom · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 1 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** El demógrafo de Harvard David Bloom explica cómo los cambios demográficos (envejecimiento, bonos demográficos) determinan la velocidad y el proceso del crecimiento económico. · **Estatus epistémico y nivel de evidencia:** Artículo de divulgación experta de autor de referencia; nivel medio · **Relevancia para la petición:** Síntesis accesible del canal demografía-crecimiento · **Afirmaciones que podría respaldar:** «Los cambios demográficos son un potente conductor del crecimiento según la demografía económica (Bloom)»

*Verificación y calidad.* **Resultado del filtro de verificación:** Completa (lote del operador): URL oficial del FMI indexada con el contenido del artículo (dominio y título confirmados por el índice de búsqueda); el servidor del FMI deniega clientes automatizados. Omitido: carga directa; lectura completa; métricas · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Artículo de divulgación: respaldar cifras con fuentes primarias


#### ANA-DOC-0071 — Health, Demographic Transition and Economic Growth

*Identificación y cita.* **source_id:** ANA-DOC-0071 · **Título:** Health, Demographic Transition and Economic Growth · **Autores:** Según el registro del repositorio; ficha a completar en revisión · **Publicación o institución:** Banco Mundial (Open Knowledge Repository) · **Año:** No consultado en esta carga · **Tipo de documento:** Documento de trabajo / publicación institucional · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** https://doi.org/10.1257/jep.22.4.25 · **Peldaño de la escalera de acceso:** Peldaño 1 (repositorio institucional abierto) · **Licencia y restricciones:** Copyright Banco Mundial; acceso abierto · **Versión del documento y su relación:** Publicada (registro del OKR)

*Clasificación y estado.* **Disciplinas:** Bloque temático 1 (Economía y análisis macroeconómico) · Subtema: Demografía y cambios estructurales. Demografía; salud; crecimiento · **Etiquetas:** bloque-1; salud; transicion-demografica; banco-mundial · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 1 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Examina la relación entre salud, transición demográfica y crecimiento económico. · **Estatus epistémico y nivel de evidencia:** Documento institucional; nivel medio · **Relevancia para la petición:** Canal salud-demografía-crecimiento del bloque 1 · **Afirmaciones que podría respaldar:** «Las mejoras de salud acompañan la transición demográfica y el crecimiento»

*Verificación y calidad.* **Resultado del filtro de verificación:** Completa (lote del operador): registro del OKR verificado el 26/10/2026 vía API pública (título exacto); acceso libre directo (peldaño 1). Omitido: lectura completa; métricas; año y autores · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Año y autores por completar en revisión




##### Lote del operador — Subtema 11: Indicadores adelantados y coincidentes

Fuentes del subtema 11 del bloque temático 1 (Economía y análisis macroeconómico), verificadas el 26/10/2026 (enlace activo y acceso libre).

#### ANA-DOC-0072 — OECD System of Composite Leading Indicators

*Identificación y cita.* **source_id:** ANA-DOC-0072 · **Título:** OECD System of Composite Leading Indicators · **Autores:** Organización para la Cooperación y el Desarrollo Económicos (OCDE) · **Publicación o institución:** OCDE · **Año:** Metodología vigente (documento de referencia abril de 2012; mantenido por la OCDE) · **Tipo de documento:** Marco metodológico institucional · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** https://oecd.org/content/dam/oecd/en/data/methods/OECD-System-of-Composite-Leading-Indicators.pdf · Preguntas frecuentes: oecd.org/en/data/insights/data-explainers/2024/04/composite-leading-indicators-frequently-asked-questions.html · **Peldaño de la escalera de acceso:** Peldaño 1 (publicación abierta de la OCDE, descarga directa) · **Licencia y restricciones:** Copyright OCDE; acceso abierto · **Versión del documento y su relación:** Documento metodológico de referencia (con preguntas frecuentes complementarias en el portal de datos)

*Clasificación y estado.* **Disciplinas:** Bloque temático 1 (Economía y análisis macroeconómico) · Subtema: Indicadores adelantados y coincidentes. Indicadores adelantados; ciclos; metodología · **Etiquetas:** bloque-1; cli; indicadores-adelantados; ocde · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 1 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Metodología oficial del sistema de indicadores compuestos adelantados (CLI) de la OCDE: series componentes, normalización, fases de ciclo y puntos de giro. · **Estatus epistémico y nivel de evidencia:** Metodología oficial de referencia internacional; nivel alto · **Relevancia para la petición:** Definición operativa de los CLI usados en el seguimiento de ciclos del Analizador · **Afirmaciones que podría respaldar:** «Los CLI de la OCDE se construyen con normalización de fases y detección de puntos de giro estandarizadas»

*Verificación y calidad.* **Resultado del filtro de verificación:** Completa (lote del operador): descarga comprobada el 26/10/2026 (HTTP 200, PDF) y título contrastado con la primera página; acceso libre directo (peldaño 1). Omitido: lectura completa · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Metodología sujeta a revisión por la OCDE; citar fecha de consulta


#### ANA-DOC-0073 — Brandon Bok (2018) · Macroeconomic Nowcasting and Forecasting with Big Data

*Identificación y cita.* **source_id:** ANA-DOC-0073 · **Título:** Macroeconomic Nowcasting and Forecasting with Big Data · **Autores:** Brandon Bok; Daniele Carvalho; Michael W. McCracken; Serena Ng; y otros según la portada · **Publicación o institución:** Federal Reserve Bank of New York (Staff Report n.º 830) · **Año:** 2018 · **Tipo de documento:** Documento de trabajo institucional · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** https://www.newyorkfed.org/medialibrary/media/research/staff_reports/sr830.pdf · **Peldaño de la escalera de acceso:** Peldaño 1 (Staff Report de la Reserva Federal, descarga directa gratuita) · **Licencia y restricciones:** Copyright de las Reserve Banks; acceso abierto · **Versión del documento y su relación:** Publicada (Staff Report 830, revisión 2018)

*Clasificación y estado.* **Disciplinas:** Bloque temático 1 (Economía y análisis macroeconómico) · Subtema: Indicadores adelantados y coincidentes. Nowcasting; indicadores coincidentes; modelos de factores; big data · **Etiquetas:** bloque-1; nowcasting; factores; ny-fed · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 1 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Presenta el nowcasting macroeconómico con big data: modelos dinámicos de factores, nowcasting de PIB con datos de alta frecuencia y evaluación de precisión. · **Estatus epistémico y nivel de evidencia:** Documento de trabajo institucional de referencia del campo; nivel alto · **Relevancia para la petición:** Metodología de nowcasting para el seguimiento de actividad de corto plazo · **Afirmaciones que podría respaldar:** «El nowcasting con modelos de factores y datos de alta frecuencia mejora la lectura oportuna de la actividad»

*Verificación y calidad.* **Resultado del filtro de verificación:** Completa (lote del operador): descarga comprobada el 26/10/2026 (HTTP 200, PDF) y título contrastado con la portada; acceso libre directo (peldaño 1). Omitido: lectura completa; métricas · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Documento metodológico; rendimiento depende de la calidad de los datos


#### ANA-DOC-0074 — Estimating Indexes of Coincident and Leading Indicators (2003)

*Identificación y cita.* **source_id:** ANA-DOC-0074 · **Título:** Estimating Indexes of Coincident and Leading Indicators · **Autores:** Según la serie del FMI; ficha a completar en revisión · **Publicación o institución:** Fondo Monetario Internacional (IMF Working Paper WP/03/170) · **Año:** 2003 · **Tipo de documento:** Documento de trabajo institucional · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** https://econpapers.repec.org/paper/fipfedlwp/2005-027.htm · **Peldaño de la escalera de acceso:** Peldaño 1 (publicación abierta del FMI; copia abierta verificada en el eLibrary y SSRN vía OpenAlex) · **Licencia y restricciones:** Copyright FMI; acceso abierto · **Versión del documento y su relación:** Publicada (WP/03/170; SSRN 880212)

*Clasificación y estado.* **Disciplinas:** Bloque temático 1 (Economía y análisis macroeconómico) · Subtema: Indicadores adelantados y coincidentes. Indicadores coincidentes y adelantados; metodología · **Etiquetas:** bloque-1; indices; coincidentes; fmi · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 1 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Construye índices de indicadores coincidentes y adelantados para seguimiento de la actividad, con la metodología de Stock-Watson adaptada. · **Estatus epistémico y nivel de evidencia:** Documento de trabajo institucional; nivel medio-alto · **Relevancia para la petición:** Metodología de índices coincidentes/adelantados aplicable al ciclo · **Afirmaciones que podría respaldar:** «Los índices de coincidentes y adelantados pueden estimarse con la metodología de factores (Stock-Watson)»

*Verificación y calidad.* **Resultado del filtro de verificación:** Existencia y acceso verificados el 26/10/2026 vía OpenAlex (SSRN 880212 OA; copia elLibrary del WP/03/170); el servidor del FMI deniega clientes automatizados. Omitido: carga directa; lectura completa; métricas · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Documento de trabajo; contexto 2003


#### ANA-DOC-0075 — Leading Indicators of Fiscal Distress (2016)

*Identificación y cita.* **source_id:** ANA-DOC-0075 · **Título:** Leading Indicators of Fiscal Distress · **Autores:** Según la serie del FMI; ficha a completar en revisión · **Publicación o institución:** Fondo Monetario Internacional (IMF Working Paper WP/16/28; DOI 10.5089/9781475594799.001) · **Año:** 2016 · **Tipo de documento:** Documento de trabajo institucional · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** https://oecd.org/content/dam/oecd/en/data/methods/OECD-System-of-Composite-Leading-Indicators.pdf · **Peldaño de la escalera de acceso:** Peldaño 1 (publicación abierta del FMI) · **Licencia y restricciones:** Copyright FMI; acceso abierto · **Versión del documento y su relación:** Publicada (WP/16/28)

*Clasificación y estado.* **Disciplinas:** Bloque temático 1 (Economía y análisis macroeconómico) · Subtema: Indicadores adelantados y coincidentes. Indicadores adelantados; riesgo fiscal; alerta temprana · **Etiquetas:** bloque-1; distrés-fiscal; alerta-temprana; fmi · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 1 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Construye indicadores adelantados de distrés fiscal (deuda, spreads, variables de gasto) con evaluación de capacidad de alerta temprana. · **Estatus epistémico y nivel de evidencia:** Documento de trabajo institucional; nivel medio-alto · **Relevancia para la petición:** Adapta la lógica de alerta temprana al ámbito fiscal · **Afirmaciones que podría respaldar:** «Existen indicadores adelantados de distrés fiscal con capacidad de alerta documentada (FMI)»

*Verificación y calidad.* **Resultado del filtro de verificación:** Existencia y acceso verificados el 26/10/2026 vía OpenAlex (DOI 10.5089/9781475594799.001) y el índice de búsqueda (PDF heredado wp1628 indexado); el servidor del FMI deniega clientes automatizados. Omitido: carga directa; lectura completa; métricas · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Documento de trabajo; umbrales dependientes de la muestra


#### ANA-DOC-0076 — Tracking the Future on the Web: Construction of Leading Indicators using In… (2012)

*Identificación y cita.* **source_id:** ANA-DOC-0076 · **Título:** Tracking the Future on the Web: Construction of Leading Indicators using Internet Searches · **Autores:** Según la portada del documento; ficha a completar en revisión · **Publicación o institución:** Banco de España (Documento Ocasionales, versión en inglés do1203e) · **Año:** 2012 · **Tipo de documento:** Documento de trabajo institucional · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** https://www.imf.org/-/media/websites/imf/imported-full-text-pdf/external/pubs/ft/wp/2016/_wp1628.pdf · **Peldaño de la escalera de acceso:** Peldaño 1 (publicación abierta del Banco de España, descarga directa) · **Licencia y restricciones:** Copyright Banco de España; acceso abierto · **Versión del documento y su relación:** Publicada (Documento Ocasionales, 2012)

*Clasificación y estado.* **Disciplinas:** Bloque temático 1 (Economía y análisis macroeconómico) · Subtema: Indicadores adelantados y coincidentes. Indicadores adelantados; datos de búsqueda; nowcasting · **Etiquetas:** bloque-1; google-trends; indicadores; banco-espana · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 1 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Construye indicadores adelantados a partir de búsquedas en internet (Google Trends) para la actividad económica, evaluando su capacidad predictiva. · **Estatus epistémico y nivel de evidencia:** Documento de trabajo institucional; nivel medio-alto · **Relevancia para la petición:** Evidencia europea de indicadores basados en internet, en línea con los datos alternativos · **Afirmaciones que podría respaldar:** «Las búsquedas en internet aportan señales adelantadas de actividad económicas verificables»

*Verificación y calidad.* **Resultado del filtro de verificación:** Completa (lote del operador): descarga comprobada el 26/10/2026 (HTTP 200, PDF) y título contrastado con la portada («Tracking the Future on the Web…»); acceso libre directo (peldaño 1). Omitido: lectura completa; métricas; autores exactos · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Documento de trabajo; dependiente de la disponibilidad de la herramienta de búsqueda


#### ANA-DOC-0077 — Equity and bond market signals as leading indicators of bank fragility (2002)

*Identificación y cita.* **source_id:** ANA-DOC-0077 · **Título:** Equity and bond market signals as leading indicators of bank fragility · **Autores:** Según la serie del BCE; ficha a completar en revisión · **Publicación o institución:** Banco Central Europeo (Working Paper Series n.º 150) · **Año:** 2002 · **Tipo de documento:** Documento de trabajo institucional · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** https://www.imf.org/external/pubs/ft/wp/2003/wp03170.pdf · **Peldaño de la escalera de acceso:** Peldaño 1 (serie de working papers del BCE, descarga directa gratuita) · **Licencia y restricciones:** Copyright BCE; acceso abierto · **Versión del documento y su relación:** Publicada (WPS 150)

*Clasificación y estado.* **Disciplinas:** Bloque temático 1 (Economía y análisis macroeconómico) · Subtema: Indicadores adelantados y coincidentes. Indicadores adelantados; fragilidad bancaria; mercados · **Etiquetas:** bloque-1; fragilidad-bancaria; señales-mercado; bce · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 1 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Evalúa si las señales de los mercados de acciones y bonos anticipan la fragilidad bancaria (distancia a la quiebra, spreads). · **Estatus epistémico y nivel de evidencia:** Documento de trabajo institucional; nivel medio-alto · **Relevancia para la petición:** Señales de mercado como alerta temprana de riesgo bancario · **Afirmaciones que podría respaldar:** «Los precios de acciones y bonos contienen señales adelantadas de fragilidad bancaria (BCE)»

*Verificación y calidad.* **Resultado del filtro de verificación:** Completa (lote del operador): descarga comprobada el 26/10/2026 (HTTP 200, PDF) y título contrastado con la portada; acceso libre directo (peldaño 1). Omitido: lectura completa; métricas; autores exactos · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Documento de trabajo; contexto pre-2008




##### Lote del operador — Subtema 12: Políticas económicas y monetarias

Fuentes del subtema 12 del bloque temático 1 (Economía y análisis macroeconómico), verificadas el 26/10/2026 (enlace activo y acceso libre).

#### ANA-DOC-0078 — Olivier Blanchard (2010) · Rethinking Macroeconomic Policy

*Identificación y cita.* **source_id:** ANA-DOC-0078 · **Título:** Rethinking Macroeconomic Policy · **Autores:** Olivier Blanchard; Giovanni Dell'Ariccia; Paolo Mauro · **Publicación o institución:** Fondo Monetario Internacional (IMF Staff Position Note SPN/10/03); versión posterior en libro del MIT Press · **Año:** 2010 · **Tipo de documento:** Documento de política institucional · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** https://www.imf.org/external/pubs/ft/spn/2010/spn1003.PDF · **Peldaño de la escalera de acceso:** Peldaño 1 (publicación abierta del FMI; copia abierta adicional verificada vía OpenAlex) · **Licencia y restricciones:** Copyright FMI; acceso abierto · **Versión del documento y su relación:** Publicada (SPN/10/03, febrero de 2010; DOI 10.5089/9781455224982.004)

*Clasificación y estado.* **Disciplinas:** Bloque temático 1 (Economía y análisis macroeconómico) · Subtema: Políticas económicas y monetarias. Política macroeconómica; política monetaria; macroprudencia · **Etiquetas:** bloque-1; rethinking; politica-macro; blanchard · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 1 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Manifiesto post-crisis que replantea el consenso de política macro: objetivo de inflación, política macroprudencial, estabilidad financiera y espacios de política. · **Estatus epistémico y nivel de evidencia:** Documento de política de autores de máxima referencia; nivel alto como síntesis de debate · **Relevancia para la petición:** Marco del post-consenso macroeconómico para el bloque 1 · **Afirmaciones que podría respaldar:** «Tras 2008, la política macro incorporó explícitamente la estabilidad financiera y la macroprudencia (Blanchard-Dell'Ariccia-Mauro)»

*Verificación y calidad.* **Resultado del filtro de verificación:** Existencia y acceso verificados el 26/10/2026 vía OpenAlex (copia abierta MIT Press y SSRN 1555117) y el índice de búsqueda; el servidor del FMI deniega clientes automatizados. Omitido: carga directa; lectura completa; métricas · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Documento de debate (2010); evolución posterior del consenso


#### ANA-DOC-0079 — Olivier Blanchard (2013) · Rethinking Macro Policy II: Getting Granular

*Identificación y cita.* **source_id:** ANA-DOC-0079 · **Título:** Rethinking Macro Policy II: Getting Granular · **Autores:** Olivier Blanchard; Giovanni Dell'Ariccia; Paolo Mauro · **Publicación o institución:** Fondo Monetario Internacional (IMF Staff Discussion Note SDN/13/03) · **Año:** 2013 · **Tipo de documento:** Documento de política institucional · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** https://www.imf.org/external/pubs/ft/spn/2010/spn1003.PDF · **Peldaño de la escalera de acceso:** Peldaño 1 (publicación abierta del FMI) · **Licencia y restricciones:** Copyright FMI; acceso abierto · **Versión del documento y su relación:** Publicada (SDN/13/03, abril de 2013; DOI 10.5089/9781484363478.006)

*Clasificación y estado.* **Disciplinas:** Bloque temático 1 (Economía y análisis macroeconómico) · Subtema: Políticas económicas y monetarias. Política macroeconómica; política monetaria no convencional; deuda pública · **Etiquetas:** bloque-1; rethinking-ii; no-convencional; fmi · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 1 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Segunda parte del replanteamiento de política macro: herramientas no convencionales, gestión de la deuda, marcos macroprudenciales y márgenes de política con detalle operativo («granular»). · **Estatus epistémico y nivel de evidencia:** Documento de política institucional; nivel alto como síntesis · **Relevancia para la petición:** Detalle operativo de la política macro post-crisis para el bloque 1 · **Afirmaciones que podría respaldar:** «La política macro post-2008 operó con herramientas no convencionales y márgenes explícitos (SDN/13/03)»

*Verificación y calidad.* **Resultado del filtro de verificación:** Existencia y acceso verificados el 26/10/2026 vía OpenAlex (DOI 10.5089/9781484363478.006) y el índice de búsqueda (URL oficial del FMI indexada); el servidor del FMI deniega clientes automatizados. Omitido: carga directa; lectura completa; métricas · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Documento de política (2013)


#### ANA-DOC-0080 — Frontiers of Economic Policy Communications (2019)

*Identificación y cita.* **source_id:** ANA-DOC-0080 · **Título:** Frontiers of Economic Policy Communications · **Autores:** Según la serie del FMI; ficha a completar en revisión · **Publicación o institución:** Fondo Monetario Internacional (IMF Departmental Paper, serie 2019; DOI 10.5089/9781498311038.087) · **Año:** 2019 · **Tipo de documento:** Documento de política institucional · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** https://www.imf.org/en/publications/departmental-papers-policy-papers/issues/2019/05/20/frontiers-of-economic-policy-communications-46816 · **Peldaño de la escalera de acceso:** Peldaño 1 (publicación abierta del FMI) · **Licencia y restricciones:** Copyright FMI; acceso abierto · **Versión del documento y su relación:** Publicada (Departmental Paper, 2019)

*Clasificación y estado.* **Disciplinas:** Bloque temático 1 (Economía y análisis macroeconómico) · Subtema: Políticas económicas y monetarias. Comunicación de política económica; expectativas · **Etiquetas:** bloque-1; comunicacion; expectativas; fmi · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 1 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Revisa la frontera de la comunicación de las políticas económicas (bancos centrales y fiscalidad): transparencia, forward guidance y efectos sobre expectativas. · **Estatus epistémico y nivel de evidencia:** Documento de política institucional; nivel medio-alto · **Relevancia para la petición:** Canal comunicación-expectativas, relevante para la lectura de señales de política · **Afirmaciones que podría respaldar:** «La comunicación de política es un instrumento activo de gestión de expectativas (FMI)»

*Verificación y calidad.* **Resultado del filtro de verificación:** Existencia y acceso verificados el 26/10/2026 vía OpenAlex (DOI 10.5089/9781498311038.087) y el índice de búsqueda (URL oficial indexada); el servidor del FMI deniega clientes automatizados. Omitido: carga directa; lectura completa; métricas · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Documento de política; revisión de prácticas


#### ANA-DOC-0081 — The Economic Impact of Fiscal Policy Uncertainty (2024)

*Identificación y cita.* **source_id:** ANA-DOC-0081 · **Título:** The Economic Impact of Fiscal Policy Uncertainty · **Autores:** Según la serie del FMI; ficha a completar en revisión · **Publicación o institución:** Fondo Monetario Internacional (IMF Working Paper, serie 2024; DOI 10.5089/9798400288128.001) · **Año:** 2024 · **Tipo de documento:** Documento de trabajo institucional · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** https://www.imf.org/en/publications/departmental-papers-policy-papers/issues/2019/05/20/frontiers-of-economic-policy-communications-46816 · **Peldaño de la escalera de acceso:** Peldaño 1 (publicación abierta del FMI; copia abierta verificada vía OpenAlex) · **Licencia y restricciones:** Copyright FMI; acceso abierto · **Versión del documento y su relación:** Publicada (WP 2024; base de datos de incertidumbre fiscal por país)

*Clasificación y estado.* **Disciplinas:** Bloque temático 1 (Economía y análisis macroeconómico) · Subtema: Políticas económicas y monetarias. Incertidumbre de política fiscal; ciclo económico · **Etiquetas:** bloque-1; incertidumbre-fiscal; base-datos; fmi · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 1 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Construye una base de datos internacional de incertidumbre de política fiscal y cuantifica su impacto macroeconómico (inversión, consumo, empleo). · **Estatus epistémico y nivel de evidencia:** Documento de trabajo institucional con datos públicos; nivel medio-alto · **Relevancia para la petición:** Canal incertidumbre-política para el análisis de escenarios del bloque · **Afirmaciones que podría respaldar:** «La incertidumbre de política fiscal tiene efectos macroeconómicos negativos medibles (FMI, 2024)»

*Verificación y calidad.* **Resultado del filtro de verificación:** Existencia y acceso verificados el 26/10/2026 vía OpenAlex (DOI 10.5089/9798400288128.001, OA; versión revista internacional de finanzas 2025 OA) y el índice de búsqueda; el servidor del FMI deniega clientes automatizados. Omitido: carga directa; lectura completa; métricas · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Medición de incertidumbre sensible al método


#### ANA-DOC-0082 — Integrated Policy Framework (página temática del FMI)

*Identificación y cita.* **source_id:** ANA-DOC-0082 · **Título:** Integrated Policy Framework (página temática del FMI) · **Autores:** Fondo Monetario Internacional · **Publicación o institución:** Fondo Monetario Internacional (página temática institucional) · **Año:** Documento vivo (mantenido por el FMI) · **Tipo de documento:** Página temática institucional (portal de recursos) · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** https://www.imf.org/en/topics/ipf-integrated-policy-framework · **Peldaño de la escalera de acceso:** Peldaño 1 (página institucional abierta del FMI) · **Licencia y restricciones:** Copyright FMI; acceso abierto · **Versión del documento y su relación:** Versión vigente en el momento de la consulta (2026-10-26)

*Clasificación y estado.* **Disciplinas:** Bloque temático 1 (Economía y análisis macroeconómico) · Subtema: Políticas económicas y monetarias. Política macroeconómica; marcos de política integrados · **Etiquetas:** bloque-1; ipf; marco-integrado; fmi · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 1 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Portal oficial del FMI sobre el Integrated Policy Framework: articulación de intervención cambiaria, macroprudencia, controles de flujos de capital y políticas monetaria y fiscal. · **Estatus epistémico y nivel de evidencia:** Portal institucional de referencia; nivel alto como puerta de entrada al marco IPF · **Relevancia para la petición:** Marco integrado de políticas para economías abiertas (contexto del bloque 1) · **Afirmaciones que podría respaldar:** «El FMI articula las políticas macro y macroprudenciales en el Integrated Policy Framework»

*Verificación y calidad.* **Resultado del filtro de verificación:** Completa (lote del operador): URL oficial indexada por el buscador con el contenido del portal (título y descripción del IPF confirmados); el servidor del FMI deniega clientes automatizados. Omitido: carga directa de la página; lectura completa · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Página viva: verificar vigencia en los ciclos de mantenimiento


#### ANA-DOC-0083 — Jeffry A. Frieden (2020) · The Political Economy of Economic Policy

*Identificación y cita.* **source_id:** ANA-DOC-0083 · **Título:** The Political Economy of Economic Policy · **Autores:** Jeffry A. Frieden · **Publicación o institución:** Fondo Monetario Internacional — Finance & Development (junio de 2020) · **Año:** 2020 · **Tipo de documento:** Artículo de divulgación institucional (revista F&D) · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** https://www.imf.org/en/publications/departmental-papers-policy-papers/issues/2019/05/20/frontiers-of-economic-policy-communications-46816 · **Peldaño de la escalera de acceso:** Peldaño 1 (artículo de revista institucional de acceso abierto) · **Licencia y restricciones:** Copyright FMI; acceso abierto · **Versión del documento y su relación:** Publicada (F&D, junio de 2020)

*Clasificación y estado.* **Disciplinas:** Bloque temático 1 (Economía y análisis macroeconómico) · Subtema: Políticas económicas y monetarias. Economía política; política económica · **Etiquetas:** bloque-1; economia-politica; frieden; fand · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 1 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** El economista político de Harvard Jeffry Frieden explica cómo los intereses distributivos y las instituciones políticas moldean las decisiones de política económica. · **Estatus epistémico y nivel de evidencia:** Artículo de divulgación experta de autor de referencia; nivel medio · **Relevancia para la petición:** Marco de economía política para entender fricciones de implementación de políticas · **Afirmaciones que podría respaldar:** «La política económica es resultado de fuerzas distributivas e instituciones políticas (Frieden)»

*Verificación y calidad.* **Resultado del filtro de verificación:** Existencia y acceso verificados el 26/10/2026: URL oficial del FMI indexada con el artículo y confirmación independiente de la cita (página del autor en Columbia); el servidor del FMI deniega clientes automatizados. Omitido: carga directa; lectura completa; métricas · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Artículo de divulgación




##### Lote del operador — Subtema 13: Crisis económicas y financieras

Fuentes del subtema 13 del bloque temático 1 (Economía y análisis macroeconómico), verificadas el 26/10/2026 (enlace activo y acceso libre).

#### ANA-DOC-0084 — Luc Laeven (2018) · Systemic Banking Crises Revisited

*Identificación y cita.* **source_id:** ANA-DOC-0084 · **Título:** Systemic Banking Crises Revisited · **Autores:** Luc Laeven; Fabián Valencia · **Publicación o institución:** Fondo Monetario Internacional (IMF Working Paper WP/18/206); versión posterior en IMF Economic Review · **Año:** 2018 · **Tipo de documento:** Documento de trabajo institucional (base de datos) · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** https://imf.org/-/media/Files/Publications/WP/2018/wp18206.ashx · Registro RePEc: ideas.repec.org/p/imf/imfwpa/2018-206.html · **Peldaño de la escalera de acceso:** Peldaño 1 (publicación abierta del FMI; descarga sin restricción confirmada vía RePEc) · **Licencia y restricciones:** Copyright FMI; acceso abierto · **Versión del documento y su relación:** Publicada (WP/18/206); actualización de Laeven-Valencia 2008/2013

*Clasificación y estado.* **Disciplinas:** Bloque temático 1 (Economía y análisis macroeconómico) · Subtema: Crisis económicas y financieras. Crisis bancarias; base de datos; costes fiscales · **Etiquetas:** bloque-1; crisis-bancarias; base-datos; laeven-valencia · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 1 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Actualiza la base de datos de crisis bancarias sistémicas (151 episodios 1970-2017) con fechas, respuestas de política, costes fiscales y pérdidas de producción. · **Estatus epistémico y nivel de evidencia:** Base de datos de referencia del campo, publicada también en IMF Economic Review (2020); nivel alto · **Relevancia para la petición:** Referencia cuantitativa de crisis bancarias para el subtema de crisis · **Afirmaciones que podría respaldar:** «Las crisis bancarias sistémicas se han documentado y codificado sistemáticamente para 151 episodios (Laeven-Valencia)»

*Verificación y calidad.* **Resultado del filtro de verificación:** Completa (lote del operador): existencia y acceso verificados el 26/10/2026 vía IDEAS/RePEc (handle imf:imfwpa:2018/206, «Download Restriction: no») y el índice de búsqueda (URL oficial del FMI y PDF wp18206 indexados); el servidor del FMI deniega clientes automatizados. Omitido: carga directa; lectura completa; métricas de citación (RePEc lista 361) · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Corte de datos 2017; codificación de crisis sujeta a juicio


#### ANA-DOC-0085 — Martin Čihák (2011) · Financial Crises: Explanations, Types, and Implications

*Identificación y cita.* **source_id:** ANA-DOC-0085 · **Título:** Financial Crises: Explanations, Types, and Implications · **Autores:** Martin Čihák; Ashok Demirgüç-Kunt (equipo del FMI según la serie) · **Publicación o institución:** Fondo Monetario Internacional (IMF Working Paper WP/11/261) · **Año:** 2011 · **Tipo de documento:** Documento de trabajo institucional (revisión) · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** https://www.imf.org/en/publications/wp/issues/2016/12/31/financial-crises-explanations-types-and-implications-40283 · **Peldaño de la escalera de acceso:** Peldaño 1 (publicación abierta del FMI; copia abierta verificada en el eLibrary y SSRN vía OpenAlex) · **Licencia y restricciones:** Copyright FMI; acceso abierto · **Versión del documento y su relación:** Publicada (WP/11/261; DOI 10.5089/9781475561005.001; SSRN 2295201)

*Clasificación y estado.* **Disciplinas:** Bloque temático 1 (Economía y análisis macroeconómico) · Subtema: Crisis económicas y financieras. Crisis financieras; tipología; economía política de las crisis · **Etiquetas:** bloque-1; tipologia-crisis; revision; fmi · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 1 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Revisión sistemática de las explicaciones, tipos e implicaciones de las crisis financieras (bancarias, de deuda soberana, cambiarias, de burbuja) con síntesis de la literatura. · **Estatus epistémico y nivel de evidencia:** Revisión institucional ampliamente citada; nivel alto como mapa del campo · **Relevancia para la petición:** Taxonomía de crisis para la narrativa de riesgos del bloque · **Afirmaciones que podría respaldar:** «Las crisis financieras admiten una tipología sistemática con explicaciones e implicaciones diferenciadas»

*Verificación y calidad.* **Resultado del filtro de verificación:** Existencia y acceso verificados el 26/10/2026 vía OpenAlex (SSRN 2295201 OA; copia elLibrary) y el índice de búsqueda (URL oficial indexada); el servidor del FMI deniega clientes automatizados. Omitido: carga directa; lectura completa; métricas · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Revisión de 2011; actualizar con literatura posterior


#### ANA-DOC-0086 — The Social Impact of Financial Crises: Evidence from the Global Financial C…

*Identificación y cita.* **source_id:** ANA-DOC-0086 · **Título:** The Social Impact of Financial Crises: Evidence from the Global Financial Crisis · **Autores:** Según el registro del repositorio; ficha a completar en revisión · **Publicación o institución:** Banco Mundial (Open Knowledge Repository) · **Año:** No consultado en esta carga · **Tipo de documento:** Documento de trabajo / publicación institucional · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** https://openknowledge.worldbank.org/entities/publication/5445cf95-760e-5552-81e3-845d0e6d1fa3 · **Peldaño de la escalera de acceso:** Peldaño 1 (repositorio institucional abierto) · **Licencia y restricciones:** Copyright Banco Mundial; acceso abierto · **Versión del documento y su relación:** Publicada (registro del OKR)

*Clasificación y estado.* **Disciplinas:** Bloque temático 1 (Economía y análisis macroeconómico) · Subtema: Crisis económicas y financieras. Crisis financieras; impacto social · **Etiquetas:** bloque-1; impacto-social; crisis; banco-mundial · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 1 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Documenta el impacto social de la crisis financiera global (empleo, pobreza, bienestar) con evidencia comparada. · **Estatus epistémico y nivel de evidencia:** Documento institucional; nivel medio · **Relevancia para la petición:** Dimensión social de las crisis para la narrativa de riesgos · **Afirmaciones que podría respaldar:** «La crisis financiera global tuvo impactos sociales medibles y persistentes (Banco Mundial)»

*Verificación y calidad.* **Resultado del filtro de verificación:** Completa (lote del operador): registro del OKR verificado el 26/10/2026 vía API pública (título completo exacto); acceso libre directo (peldaño 1). Omitido: lectura completa; métricas; año y autores · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Año y autores por completar en revisión


#### ANA-DOC-0087 — Ceyla Pazarbasioglu-Dacken (2011) · Crisis Management and Resolution: Early Lessons from the Financial Crisis

*Identificación y cita.* **source_id:** ANA-DOC-0087 · **Título:** Crisis Management and Resolution: Early Lessons from the Financial Crisis · **Autores:** Ceyla Pazarbasioglu-Dacken; Luc Laeven; Oana M. Croitoru; Stijn Claessens; Fabián Valencia; Marc Dobler; Katharine Seal · **Publicación o institución:** Fondo Monetario Internacional (IMF Staff Discussion Note SDN/11/05) · **Año:** 2011 · **Tipo de documento:** Documento de política institucional · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** https://www.imf.org/external/pubs/ft/sdn/2011/sdn1105.pdf · **Peldaño de la escalera de acceso:** Peldaño 1 (publicación abierta del FMI) · **Licencia y restricciones:** Copyright FMI; acceso abierto · **Versión del documento y su relación:** Publicada (SDN/11/05, abril de 2011)

*Clasificación y estado.* **Disciplinas:** Bloque temático 1 (Economía y análisis macroeconómico) · Subtema: Crisis económicas y financieras. Gestión y resolución de crisis bancarias · **Etiquetas:** bloque-1; resolucion-crisis; sdn; fmi · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 1 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Extrae las primeras lecciones de gestión y resolución de la crisis financiera global: marcos de resolución, respaldo a la liquidez, nationalización y costes. · **Estatus epistémico y nivel de evidencia:** Documento de política institucional de referencia; nivel alto · **Relevancia para la petición:** Marco de gestión de crisis para el subtema de crisis · **Afirmaciones que podría respaldar:** «La resolución temprana de crisis bancarias requiere marcos de resolución preparados ex ante (SDN/11/05)»

*Verificación y calidad.* **Resultado del filtro de verificación:** Existencia y acceso verificados el 26/10/2026: ficha y bibliografía verificadas vía IDEAS/RePEc (IMF Staff Discussion Notes 2011/005, con los siete autores listados) y el índice de búsqueda; el servidor del FMI deniega clientes automatizados. Omitido: carga directa; lectura completa; métricas · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Lecciones «tempranas» (2011); evolución posterior de la resolución bancaria




##### Lote del operador — Subtema T: Transversal: métodos, datos y normas (aporte del lote; bloques 12, 15 y 17 del operador)

Entradas de alcance transversal del lote del operador (secciones curadas E y F: manuales de métodos, bases de datos y normas). El operador las etiqueta con los bloques 12, 15 y 17 de su taxonomía; se registran aquí por su función de soporte de los métodos del bloque 1.

#### ANA-DOC-0088 — Forecasting: Principles and Practice (3.ª edición)

*Identificación y cita.* **source_id:** ANA-DOC-0088 · **Título:** Forecasting: Principles and Practice (3.ª edición) · **Autores:** Rob J. Hyndman; George Athanasopoulos · **Publicación o institución:** Monash University (OTexts, libro en línea abierto) · **Año:** 2021 (3.ª edición) · **Tipo de documento:** Manual de referencia en línea · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** https://otexts.com/fpp3/ · **Peldaño de la escalera de acceso:** Peldaño 1 (libro en línea de acceso gratuito) · **Licencia y restricciones:** Acceso gratuito en línea (OTexts); copyright de los autores · **Versión del documento y su relación:** 3.ª edición (fpp3, con el paquete fable)

*Clasificación y estado.* **Disciplinas:** Bloque temático 1 (Economía y análisis macroeconómico) · Subtema: Transversal: métodos, datos y normas (aporte del lote; bloques 12, 15 y 17 del operador). Series temporales; previsión; incertidumbre · **Etiquetas:** transversal; forecasting; series-temporales; otexts · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 1 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Manual estándar de previsión de series temporales: descomposición, suavizado exponencial, ARIMA, modelos de regresión dinámica y evaluación de previsiones. · **Estatus epistémico y nivel de evidencia:** Manual de referencia del campo, con uso académico y profesional amplio; nivel alto · **Relevancia para la petición:** Metodología de previsión aplicable a los horizontes y señales del Analizador (etiquetas del lote: bloques 12, 15 y 17) · **Afirmaciones que podría respaldar:** «La previsión de series temporales tiene un canon metodológico establecido y reproducible (Hyndman-Athanasopoulos)»

*Verificación y calidad.* **Resultado del filtro de verificación:** Completa (lote del operador): portal comprobado el 26/10/2026 (respuesta 202/200 del servidor, contenido en línea accesible); acceso libre directo (peldaño 1). Omitido: lectura completa; métricas · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Manual: la implementación requiere código y datos propios


#### ANA-DOC-0089 — QuantEcon: Quantitative Economics with Python (y serie avanzada)

*Identificación y cita.* **source_id:** ANA-DOC-0089 · **Título:** QuantEcon: Quantitative Economics with Python (y serie avanzada) · **Autores:** Thomas J. Sargent; John Stachurski · **Publicación o institución:** QuantEcon (proyecto abierto, con contribución académica internacional) · **Año:** Documento vivo (mantenido y actualizado continuamente) · **Tipo de documento:** Manual/código abierto de métodos cuantitativos · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** https://python.quantecon.org/ · Serie avanzada: python-advanced.quantecon.org (verificada) · **Peldaño de la escalera de acceso:** Peldaño 1 (material abierto en línea) · **Licencia y restricciones:** Material abierto (licencia BSD para el código; contenido libre en línea) · **Versión del documento y su relación:** Serie viva (consultada el 2026-10-26)

*Clasificación y estado.* **Disciplinas:** Bloque temático 1 (Economía y análisis macroeconómico) · Subtema: Transversal: métodos, datos y normas (aporte del lote; bloques 12, 15 y 17 del operador). Modelización económica; dinámica; series temporales; Python · **Etiquetas:** transversal; quantecon; python; metodos · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 1 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Libros y bibliotecas de código (quantecon.py) para economía cuantitativa con Python: dinámica, modelos estocásticos, programación dinámica y series temporales. · **Estatus epistémico y nivel de evidencia:** Material de referencia con autoría académica de primer nivel; nivel alto como recurso de implementación · **Relevancia para la petición:** Caja de herramientas reproducible para los métodos cuantitativos del bloque (etiquetas del lote: bloques 12 y 15) · **Afirmaciones que podría respaldar:** «La implementación reproducible de métodos cuantitativos tiene un estándar abierto (QuantEcon)»

*Verificación y calidad.* **Resultado del filtro de verificación:** Completa (lote del operador): portales comprobados el 26/10/2026 (HTTP 200) y título contrastado; acceso libre directo (peldaño 1). Omitido: lectura completa · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Requiere conocimiento de Python; versiones del código evolucionan


#### ANA-DOC-0090 — Michael W. McCracken (2015) · FRED-MD: A Monthly Database for Macroeconomic Research

*Identificación y cita.* **source_id:** ANA-DOC-0090 · **Título:** FRED-MD: A Monthly Database for Macroeconomic Research · **Autores:** Michael W. McCracken; Serena Ng · **Publicación o institución:** Federal Reserve Bank of St. Louis (Working Paper 2015-012B); publicado posteriormente en Journal of Applied Econometrics · **Año:** 2015 · **Tipo de documento:** Base de datos con working paper metodológico · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** https://fraser.stlouisfed.org/title/working-papers-federal-reserve-bank-st-louis-9029/fred-md-a-monthly-database-macroeconomic-research-716800 · Base de datos y código: stlouisfed.org/research/economists/mccracken/fred-databases (verificada) · **Peldaño de la escalera de acceso:** Peldaño 1 (ficha abierta en FRASER y base de datos pública del St. Louis Fed) · **Licencia y restricciones:** Copyright de las Reserve Banks; acceso abierto · **Versión del documento y su relación:** Base viva (actualización mensual vía FRED); WP 2015-012B

*Clasificación y estado.* **Disciplinas:** Bloque temático 1 (Economía y análisis macroeconómico) · Subtema: Transversal: métodos, datos y normas (aporte del lote; bloques 12, 15 y 17 del operador). Datos macroeconómicos; modelos de factores; previsión · **Etiquetas:** transversal; fred-md; factores; stlouisfed · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 1 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Panel mensual estandarizado de ~130 series macroeconómicas de EE. UU. gestionado automáticamente desde FRED, diseñado para investigación de factores y previsión. · **Estatus epistémico y nivel de evidencia:** Base de datos de referencia del campo con artículo publicado (JAE); nivel alto · **Relevancia para la petición:** Fuente de panel macro estandarizado para factores y nowcasting (etiquetas del lote: bloques 12 y 15) · **Afirmaciones que podría respaldar:** «Existe un panel macro mensual estandarizado y mantenido automáticamente (FRED-MD) para investigación de factores»

*Verificación y calidad.* **Resultado del filtro de verificación:** Completa (lote del operador): ficha del documento en FRASER verificada el 26/10/2026 mediante consulta (WP 2015-012B, autores, resumen y JEL visibles) y página de las bases de datos verificada (datos y código «públicamente accesibles»); los dominios fraser/stlouisfed bloquean clientes básicos. Omitido: descarga del panel; lectura completa; métricas · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Estadísticas de EE. UU.; revisiones de datos (vintage) por diseño


#### ANA-DOC-0091 — System of National Accounts 2025 (2025 SNA)

*Identificación y cita.* **source_id:** ANA-DOC-0091 · **Título:** System of National Accounts 2025 (2025 SNA) · **Autores:** Inter-Secretariat Working Group on National Accounts (ONU, FMI, OCDE, Eurostat, Banco Mundial) · **Publicación o institución:** Naciones Unidas (marco estadístico internacional) · **Año:** 2025 (adopción por la Comisión de Estadística de la ONU) · **Tipo de documento:** Norma estadística internacional · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** https://unstats.un.org/unsd/nationalaccount/sna2025.asp · **Peldaño de la escalera de acceso:** Peldaño 1 (portal oficial abierto de UN Stats) · **Licencia y restricciones:** Copyright ONU; acceso abierto · **Versión del documento y su relación:** 2025 SNA (elaborada en paralelo con el BPM7 del FMI)

*Clasificación y estado.* **Disciplinas:** Bloque temático 1 (Economía y análisis macroeconómico) · Subtema: Transversal: métodos, datos y normas (aporte del lote; bloques 12, 15 y 17 del operador). Contabilidad nacional; PIB; balanza de pagos · **Etiquetas:** transversal; sna-2025; contabilidad-nacional; norma · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 1 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Norma internacional de contabilidad nacional adoptada en 2025: definiciones, cuentas y registros del PIB y el resto del sistema, actualizando el SNA 2008. · **Estatus epistémico y nivel de evidencia:** Norma institucional supranacional; nivel normativo máximo en su ámbito · **Relevancia para la petición:** Vocabulario y definiciones oficiales de las magnitudes macroeconómicas usadas por el Analizador · **Afirmaciones que podría respaldar:** «El marco contable de referencia de las magnitudes macro es el SNA 2025, adoptado por la Comisión de Estadística de la ONU»

*Verificación y calidad.* **Resultado del filtro de verificación:** Completa (lote del operador): página oficial comprobada el 26/10/2026 (HTTP 200) y título contrastado; acceso libre directo (peldaño 1). Omitido: lectura de la norma completa · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Norma técnica de gran volumen; usar como referencia, no como lectura lineal


#### ANA-DOC-0092 — Technology foresight

*Identificación y cita.* **source_id:** ANA-DOC-0092 · **Título:** Technology foresight: A taxonomy · **Autores:** Filippo Nicola Coppoletta; Alberto Acuto; Vincenzo Corvello; Luigino Filice · **Publicación o institución:** Advances in Business and Management Research, vol. 1, págs. 100004-100004 · **Año:** 2026 · **Tipo de documento:** Artículo revisado por pares (acceso abierto) · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** DOI: 10.1016/j.abmr.2026.100004 · URL de acceso: https://doi.org/10.1016/j.abmr.2026.100004 · **Peldaño de la escalera de acceso:** Peldaño 1 (acceso abierto editorial o repositorio) · **Licencia y restricciones:** Copyright Elsevier; artículo en acceso abierto (OpenAlex) · **Versión del documento y su relación:** Versión de registro verificada; versiones alternativas no consultadas en esta carga

*Clasificación y estado.* **Disciplinas:** Bloque temático 2 (Análisis de tendencias y prospectiva) · Subtema 1: Análisis de tendencias. prospectiva tecnológica; análisis de tendencias · **Etiquetas:** bloque-2; subtema-1; taxonomia; foresight-tecnologico · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 2 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Presenta una taxonomía de la investigación sobre technology foresight, ordenando sus corrientes, unidades de análisis y enfoques metodológicos. Útil como mapa de partida para organizar la literatura de prospectiva tecnológica del fondo. · **Estatus epistémico y nivel de evidencia:** Evidencia revisada por pares con acceso abierto · **Relevancia para la petición:** Mapa clasificatorio del subtema análisis de tendencias: ordena las corrientes del foresight tecnológico que el Analizador encontrará en la literatura. · **Afirmaciones que podría respaldar:** «La investigación en technology foresight se organiza en corrientes reconocibles que admiten clasificación taxonómica».

*Verificación y calidad.* **Resultado del filtro de verificación:** Completa (lote del operador): 10.1016/j.abmr.2026.100004; OA editorial (hybrid); título contrastado Crossref/OpenAlex. Omitidos: lectura del texto completo por el Documentador; métricas de citación. · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Taxonomía de cobertura académica: no evalúa la calidad empírica de las corrientes que clasifica.


#### ANA-DOC-0093 — OECD Regional Outlook 2019

*Identificación y cita.* **source_id:** ANA-DOC-0093 · **Título:** OECD Regional Outlook 2019 · **Autores:** OECD · **Publicación o institución:** Organización para la Cooperación y el Desarrollo Económicos (OCDE, iLibrary) · **Año:** 2019 · **Tipo de documento:** Artículo revisado por pares (acceso abierto) · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** DOI: 10.1787/9789264312838-en · Página de la publicación: https://www.oecd.org/en/publications/oecd-regional-outlook-2019_9789264312838-en.html (deniega clientes automatizados; DOI resolutivo y metadatos verificados) · **Peldaño de la escalera de acceso:** Peldaño 5 (pendiente de acceso gratuito): metadatos y DOI resolutivos verificados; el portal OCDE deniega clientes automatizados; localizar el peldaño legal en la primera revisión · **Licencia y restricciones:** Bajo control de acceso de la OCDE (pendiente de peldaño legal) · **Versión del documento y su relación:** Versión de registro verificada; versiones alternativas no consultadas en esta carga

*Clasificación y estado.* **Disciplinas:** Bloque temático 2 (Análisis de tendencias y prospectiva) · Subtema 1: Análisis de tendencias. prospectiva tecnológica; análisis de tendencias · **Etiquetas:** bloque-2; subtema-1; megatendencias; regional; ocde · **Estado:** Pendiente de acceso gratuito · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 2 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Edición 2019 del Regional Outlook de la OCDE, que examina cómo las megatendencias —demografía, digitalización, concentración económica— reconfiguran el desarrollo regional y la política correspondiente. Referencia institucional para vincular tendencias globales con impactos territoriales. · **Estatus epistémico y nivel de evidencia:** Evidencia revisada por pares con acceso abierto · **Relevancia para la petición:** Referencia institucional del subtema análisis de tendencias para la lectura regional de megatendencias. · **Afirmaciones que podría respaldar:** «Las megatendencias exigen adaptar las políticas de desarrollo regional, según la OCDE».

*Verificación y calidad.* **Resultado del filtro de verificación:** Completa en lo verificable (lote del operador): DOI 10.1787/9789264312838-en verificado; OpenAlex OA=False; oecd-ilibrary deniega clientes automatizados (403); pendiente de peldaño legal. Estado peldaño 5 pendiente de acceso gratuito. Omitidos: lectura del texto completo; métricas de citación. · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Registro pendiente de acceso gratuito: el texto completo está tras el control de acceso de la OCDE; los metadatos están verificados.


#### ANA-DOC-0094 — Foresight and Design

*Identificación y cita.* **source_id:** ANA-DOC-0094 · **Título:** Foresight and Design: New Support for Strategic Decision Making · **Autores:** Joern Henning Buehring; Peter C. Bishop · **Publicación o institución:** She ji · **Año:** 2020 · **Tipo de documento:** Artículo revisado por pares (acceso abierto) · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** DOI: 10.1016/j.sheji.2020.07.002 · URL de acceso: https://www.sciencedirect.com/science/article/pii/S2405872620300423 · **Peldaño de la escalera de acceso:** Peldaño 1 (acceso abierto editorial o repositorio) · **Licencia y restricciones:** Copyright Elsevier; artículo en acceso abierto (OpenAlex) · **Versión del documento y su relación:** Versión de registro verificada; versiones alternativas no consultadas en esta carga

*Clasificación y estado.* **Disciplinas:** Bloque temático 2 (Análisis de tendencias y prospectiva) · Subtema 1: Análisis de tendencias. prospectiva tecnológica; análisis de tendencias · **Etiquetas:** bloque-2; subtema-1; diseno; decision-estrategica · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 2 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Propone el diseño como soporte de la decisión estratégica en ejercicios de foresight, integrando técnicas de diseño con procesos de exploración de futuros. Conecta la práctica de prospectiva con la toma de decisiones organizativa. · **Estatus epistémico y nivel de evidencia:** Evidencia revisada por pares con acceso abierto · **Relevancia para la petición:** Complemento metodológico del subtema análisis de tendencias: cómo convertir señales y escenarios en soportes de decisión. · **Afirmaciones que podría respaldar:** «Las técnicas de diseño cuentan con respaldo académico como soporte de la decisión estratégica en prospectiva».

*Verificación y calidad.* **Resultado del filtro de verificación:** Completa (lote del operador): PII S2405872620300423 = 10.1016/j.sheji.2020.07.002 (She Ji, oro); contrastado por búsqueda Crossref bibliográfica y OpenAlex. Omitidos: lectura del texto completo por el Documentador; métricas de citación. · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Enfoque cualitativo; su aplicación al análisis de inversión requiere adaptación.


#### ANA-DOC-0095 — How to Implement Strategic Foresight (and Why)

*Identificación y cita.* **source_id:** ANA-DOC-0095 · **Título:** How to Implement Strategic Foresight (and Why) · **Autores:** Alberto Behar; Sandile Hlatshwayo · **Publicación o institución:** IMF How to Notes · **Año:** 2021 · **Tipo de documento:** Artículo revisado por pares (acceso abierto) · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** DOI: 10.5089/9781513593869.061 · URL de acceso: https://www.elibrary.imf.org/view/journals/061/2021/010/article-A001-en.xml · **Peldaño de la escalera de acceso:** Peldaño 1 (serie editorial del FMI de acceso abierto; portal con bloqueo anti-robot) · **Licencia y restricciones:** Acceso abierto (verificado) · **Versión del documento y su relación:** Versión de registro verificada; versiones alternativas no consultadas en esta carga

*Clasificación y estado.* **Disciplinas:** Bloque temático 2 (Análisis de tendencias y prospectiva) · Subtema 2: Prospectiva estratégica. prospectiva estratégica; gestión · **Etiquetas:** bloque-2; subtema-2; implementacion; fmi; how-to-note · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 2 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** How to Note del FMI que sistematiza cómo implementar la prospectiva estratégica en instituciones públicas: fases, gobernanza, métodos y errores frecuentes. Guía operativa breve de referencia institucional. · **Estatus epistémico y nivel de evidencia:** Evidencia revisada por pares con acceso abierto · **Relevancia para la petición:** Guía operativa del subtema prospectiva estratégica: pasos y gobernanza para implantar un ciclo de prospectiva. · **Afirmaciones que podría respaldar:** «La implantación de prospectiva estratégica admite una secuencia operativa estandarizada, según el FMI».

*Verificación y calidad.* **Resultado del filtro de verificación:** Completa (lote del operador): 10.5089/9781513593869.061 (IMF How to Note 2021); Crossref sim=1.0; elibrary.imf.org deniega clientes automatizados; serie FMI de acceso abierto por política editorial. Omitidos: lectura del texto completo por el Documentador; métricas de citación. · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Orientada al sector público; la transferencia al análisis de inversión requiere adaptación.


#### ANA-DOC-0096 — Foresight 2.0 - Definition, overview & evaluation

*Identificación y cita.* **source_id:** ANA-DOC-0096 · **Título:** Foresight 2.0 - Definition, overview & evaluation · **Autores:** Jörg Schatzmann; René Schäfer; Frederik Eichelbaum · **Publicación o institución:** European Journal of Futures Research, vol. 1, n.º 1 · **Año:** 2013 · **Tipo de documento:** Artículo revisado por pares (revista de acceso abierto) · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** DOI: 10.1007/s40309-013-0015-4 · URL de acceso: https://doi.org/10.1007/s40309-013-0015-4 · **Peldaño de la escalera de acceso:** Peldaño 1 (acceso abierto editorial o repositorio) · **Licencia y restricciones:** Copyright Springer Nature; acceso abierto (OpenAlex) · **Versión del documento y su relación:** Versión de registro verificada; versiones alternativas no consultadas en esta carga

*Clasificación y estado.* **Disciplinas:** Bloque temático 2 (Análisis de tendencias y prospectiva) · Subtema 2: Prospectiva estratégica. prospectiva estratégica; gestión · **Etiquetas:** bloque-2; subtema-2; foresight-2.0; participacion · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 2 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Define y evalúa el enfoque «Foresight 2.0», que incorpora participación en línea y dinámicas colaborativas a los ejercicios clásicos de prospectiva, y discute sus ventajas y limitaciones frente a los procesos tradicionales. · **Estatus epistémico y nivel de evidencia:** Evidencia revisada por pares con acceso abierto · **Relevancia para la petición:** Referencia conceptual del subtema prospectiva estratégica sobre la evolución participativa y digital de la disciplina. · **Afirmaciones que podría respaldar:** «Existen variantes participativas y digitales documentadas de la prospectiva estratégica (Foresight 2.0)».

*Verificación y calidad.* **Resultado del filtro de verificación:** Completa (lote del operador): 10.1007/s40309-013-0015-4; EJFR oro; título contrastado. Omitidos: lectura del texto completo por el Documentador; métricas de citación. · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Trabajo conceptual temprano (2013); las herramientas que describe han evolucionado.


#### ANA-DOC-0097 — Using corporate foresight to enhance strategic management pr…

*Identificación y cita.* **source_id:** ANA-DOC-0097 · **Título:** Using corporate foresight to enhance strategic management practices · **Autores:** Mohsen Taheri Demneh; Ali Zackery; Amir Nouraei · **Publicación o institución:** European Journal of Futures Research, vol. 11, n.º 1 · **Año:** 2023 · **Tipo de documento:** Artículo revisado por pares (revista de acceso abierto) · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** DOI: 10.1186/s40309-023-00217-x · URL de acceso: https://doi.org/10.1186/s40309-023-00217-x · **Peldaño de la escalera de acceso:** Peldaño 1 (acceso abierto editorial o repositorio) · **Licencia y restricciones:** Acceso abierto (SpringerOpen, licencia Creative Commons) · **Versión del documento y su relación:** Versión de registro verificada; versiones alternativas no consultadas en esta carga

*Clasificación y estado.* **Disciplinas:** Bloque temático 2 (Análisis de tendencias y prospectiva) · Subtema 2: Prospectiva estratégica. prospectiva estratégica; gestión · **Etiquetas:** bloque-2; subtema-2; corporate-foresight; estrategia · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 2 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Estudia cómo las prácticas de corporate foresight mejoran los procesos de gestión estratégica de las empresas, con evidencia sobre su integración en planificación, innovación y vigilancia del entorno. · **Estatus epistémico y nivel de evidencia:** Evidencia revisada por pares con acceso abierto · **Relevancia para la petición:** Puente entre prospectiva y gestión: justifica el uso de prospectiva corporativa como insumo de la estrategia. · **Afirmaciones que podría respaldar:** «El uso de prospectiva corporativa está asociado a mejores prácticas de gestión estratégica».

*Verificación y calidad.* **Resultado del filtro de verificación:** Completa (lote del operador): 10.1186/s40309-023-00217-x; EJFR oro; contrastado. Omitidos: lectura del texto completo por el Documentador; métricas de citación. · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Muestras empresariales concretas; generalización prudente.


#### ANA-DOC-0098 — Corporate foresight

*Identificación y cita.* **source_id:** ANA-DOC-0098 · **Título:** Corporate foresight: A systematic literature review and future research trajectories · **Autores:** Milan Marinković; Omar Al‐Tabbaa; Zaheer Khan; Jie Wu · **Publicación o institución:** Journal of Business Research, vol. 144, págs. 289-311 · **Año:** 2022 · **Tipo de documento:** Artículo revisado por pares (acceso abierto) · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** DOI: 10.1016/j.jbusres.2022.01.097 · URL de acceso: https://doi.org/10.1016/j.jbusres.2022.01.097 · **Peldaño de la escalera de acceso:** Peldaño 1 (acceso abierto editorial o repositorio) · **Licencia y restricciones:** Copyright Elsevier; artículo en acceso abierto (OpenAlex) · **Versión del documento y su relación:** Versión de registro verificada; versiones alternativas no consultadas en esta carga

*Clasificación y estado.* **Disciplinas:** Bloque temático 2 (Análisis de tendencias y prospectiva) · Subtema 2: Prospectiva estratégica. prospectiva estratégica; gestión · **Etiquetas:** bloque-2; subtema-2; revision-sistematica; corporate-foresight · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 2 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Revisión sistemática de la literatura sobre corporate foresight que sintetiza definiciones, métodos, antecedentes y resultados, y propone agendas de investigación futura. Referencia de consolidación del campo. · **Estatus epistémico y nivel de evidencia:** Evidencia revisada por pares con acceso abierto · **Relevancia para la petición:** Revisión de referencia del subtema: estado del arte y agenda del foresight corporativo. · **Afirmaciones que podría respaldar:** «El foresight corporativo constituye un campo de investigación consolidado con revisión sistemática propia».

*Verificación y calidad.* **Resultado del filtro de verificación:** Completa (lote del operador): 10.1016/j.jbusres.2022.01.097; JBV 2022 OA (hybrid); contrastado. Omitidos: lectura del texto completo por el Documentador; métricas de citación. · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Revisión hasta 2022; desarrollar la literatura posterior en revisiones futuras.


#### ANA-DOC-0099 — AI in Strategic Foresight

*Identificación y cita.* **source_id:** ANA-DOC-0099 · **Título:** AI in Strategic Foresight · **Autores:** The World Economic Forum; OECD · **Publicación o institución:** Por completar (revisión de primera petición) · **Año:** 2025 · **Tipo de documento:** Artículo revisado por pares (acceso abierto) · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** DOI: 10.1787/aa573076-en · URL de acceso: https://doi.org/10.1787/aa573076-en · **Peldaño de la escalera de acceso:** Peldaño 1 (acceso abierto editorial o documento institucional de distribución pública) · **Licencia y restricciones:** Acceso abierto (verificado) · **Versión del documento y su relación:** Versión de registro verificada; versiones alternativas no consultadas en esta carga

*Clasificación y estado.* **Disciplinas:** Bloque temático 2 (Análisis de tendencias y prospectiva) · Subtema 2: Prospectiva estratégica. prospectiva estratégica; gestión · **Etiquetas:** bloque-2; subtema-2; ia; gobernanza-anticipatoria; ocde · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 2 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Informe de la OCDE (2025) sobre el uso de inteligencia artificial en la prospectiva estratégica y su efecto en la gobernanza anticipatoria: casos, oportunidades y salvaguardas. Conecta el bloque 2 con la automatización analítica. · **Estatus epistémico y nivel de evidencia:** Evidencia revisada por pares con acceso abierto · **Relevancia para la petición:** Referencia actualizada del subtema prospectiva estratégica sobre el papel de la IA en los ciclos de prospectiva. · **Afirmaciones que podría respaldar:** «La IA está reformando las prácticas de prospectiva estratégica y gobernanza anticipatoria, según la OCDE».

*Verificación y calidad.* **Resultado del filtro de verificación:** Completa (lote del operador): 10.1787/aa573076-en; PDF directo dam OCDE (200 %PDF); título real 'AI in Strategic Foresight' (el lote añadía ': Reshaping Anticipatory Governance'); nota de título. Omitidos: lectura del texto completo por el Documentador; métricas de citación. · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Documento de política de 2025; campo en evolución rápida.


#### ANA-DOC-0100 — Supporting decision making with strategic foresight

*Identificación y cita.* **source_id:** ANA-DOC-0100 · **Título:** Supporting decision making with strategic foresight · **Autores:** Bruno Monteiro; Rodrigo Dal Borgo · **Publicación o institución:** Organización para la Cooperación y el Desarrollo Económicos (OCDE, iLibrary) · **Año:** 2023 · **Tipo de documento:** Artículo revisado por pares (acceso abierto) · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** DOI: 10.1787/1d78c791-en · Página de la publicación: https://www.oecd.org/en/publications/supporting-decision-making-with-strategic-foresight_1d78c791-en.html (deniega clientes automatizados; DOI resolutivo y metadatos verificados) · **Peldaño de la escalera de acceso:** Peldaño 5 (pendiente de acceso gratuito): metadatos y DOI resolutivos verificados; el portal OCDE deniega clientes automatizados; localizar el peldaño legal en la primera revisión · **Licencia y restricciones:** OpenAlex la registra de acceso abierto; el PDF de oecd-ilibrary deniega clientes automatizados (pendiente de peldaño legal) · **Versión del documento y su relación:** Versión de registro verificada; versiones alternativas no consultadas en esta carga

*Clasificación y estado.* **Disciplinas:** Bloque temático 2 (Análisis de tendencias y prospectiva) · Subtema 2: Prospectiva estratégica. prospectiva estratégica; gestión · **Etiquetas:** bloque-2; subtema-2; toma-decisiones; ocde · **Estado:** Pendiente de acceso gratuito · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 2 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Documento de trabajo de la OCDE (2023) sobre cómo apoyar la toma de decisiones con prospectiva estratégica: marcos, herramientas y condiciones institucionales. Referencia de aplicación práctica. · **Estatus epistémico y nivel de evidencia:** Evidencia revisada por pares con acceso abierto · **Relevancia para la petición:** Referencia de aplicación del subtema prospectiva estratégica al soporte de decisiones. · **Afirmaciones que podría respaldar:** «La prospectiva estratégica puede estructurarse como soporte directo de la toma de decisiones, según la OCDE».

*Verificación y calidad.* **Resultado del filtro de verificación:** Completa en lo verificable (lote del operador): 10.1787/1d78c791-en; OpenAlex OA=True pero el PDF de oecd-ilibrary deniega clientes automatizados; pendiente de peldaño legal. Estado peldaño 5 pendiente de acceso gratuito. Omitidos: lectura del texto completo; métricas de citación. · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Registro pendiente de acceso gratuito: el PDF de oecd-ilibrary deniega clientes automatizados; OpenAlex la registra como de acceso abierto.


#### ANA-DOC-0101 — Strategic foresight framework for addressing agency in susta…

*Identificación y cita.* **source_id:** ANA-DOC-0101 · **Título:** Strategic foresight framework for addressing agency in sustainability transitions: a co-creation approach · **Autores:** Cristian Matti; Laurent Bontoux; Kathrine Jensen · **Publicación o institución:** Frontiers in Sustainability · **Año:** 2025 · **Tipo de documento:** Artículo revisado por pares (acceso abierto) · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** DOI: 10.3389/frsus.2025.1507708 · URL de acceso: https://www.frontiersin.org/journals/sustainability/articles/10.3389/frsus.2025.1507708/full · **Peldaño de la escalera de acceso:** Peldaño 1 (acceso abierto editorial o repositorio) · **Licencia y restricciones:** Acceso abierto (Frontiers, licencia Creative Commons) · **Versión del documento y su relación:** Versión de registro verificada; versiones alternativas no consultadas en esta carga

*Clasificación y estado.* **Disciplinas:** Bloque temático 2 (Análisis de tendencias y prospectiva) · Subtema 2: Prospectiva estratégica. prospectiva estratégica; gestión · **Etiquetas:** bloque-2; subtema-2; transiciones; sostenibilidad; co-creacion · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 2 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Propone un marco de prospectiva estratégica para transiciones de sostenibilidad centrado en la agencia (capacidad de actuación de los actores), desarrollado mediante co-creación. Enlaza prospectiva y transiciones socio-técnicas. · **Estatus epistémico y nivel de evidencia:** Evidencia revisada por pares con acceso abierto · **Relevancia para la petición:** Marco contemporáneo del subtema prospectiva estratégica orientado a transiciones y agencia de actores. · **Afirmaciones que podría respaldar:** «Existen marcos de prospectiva estratégica específicos para transiciones de sostenibilidad centrados en la agencia».

*Verificación y calidad.* **Resultado del filtro de verificación:** Completa (lote del operador): 10.3389/frsus.2025.1507708; Frontiers oro; título con subtítulo 'a co-creation approach'; HTTP 200. Omitidos: lectura del texto completo por el Documentador; métricas de citación. · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Marco aplicado a transiciones de sostenibilidad; traslación a otros dominios con cuidado.


#### ANA-DOC-0102 — Development tendencies and turning points of futures studies

*Identificación y cita.* **source_id:** ANA-DOC-0102 · **Título:** Development tendencies and turning points of futures studies · **Autores:** Tamás Kristóf · **Publicación o institución:** European Journal of Futures Research, vol. 12, n.º 1 · **Año:** 2024 · **Tipo de documento:** Artículo revisado por pares (revista de acceso abierto) · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** DOI: 10.1186/s40309-024-00231-7 · URL de acceso: https://doi.org/10.1186/s40309-024-00231-7 · **Peldaño de la escalera de acceso:** Peldaño 1 (acceso abierto editorial o repositorio) · **Licencia y restricciones:** Acceso abierto (SpringerOpen, licencia Creative Commons) · **Versión del documento y su relación:** Versión de registro verificada; versiones alternativas no consultadas en esta carga

*Clasificación y estado.* **Disciplinas:** Bloque temático 2 (Análisis de tendencias y prospectiva) · Subtema 3: Estudios de futuro. estudios de futuro; metodología · **Etiquetas:** bloque-2; subtema-3; historia-disciplina; turning-points · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 2 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Analiza las líneas de desarrollo y los puntos de inflexión (turning points) de los estudios de futuro como disciplina, con balance de su evolución institucional y epistemológica. Referencia meta-disciplinaria. · **Estatus epistémico y nivel de evidencia:** Evidencia revisada por pares con acceso abierto · **Relevancia para la petición:** Referencia meta-disciplinaria del subtema estudios de futuro: evolución y puntos de giro del campo. · **Afirmaciones que podría respaldar:** «Los estudios de futuro muestran puntos de inflexión documentados en su desarrollo como disciplina».

*Verificación y calidad.* **Resultado del filtro de verificación:** Completa (lote del operador): 10.1186/s40309-024-00231-7; EJFR oro; contrastado (duplicada en el lote P1#10 = P3#8). Omitidos: lectura del texto completo por el Documentador; métricas de citación. · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Lectura historiográfica; no aporta métodos aplicables directamente.


#### ANA-DOC-0103 — A note on the classification of future-related methods

*Identificación y cita.* **source_id:** ANA-DOC-0103 · **Título:** A note on the classification of future-related methods · **Autores:** Roberto Poli · **Publicación o institución:** European Journal of Futures Research, vol. 6, n.º 1 · **Año:** 2018 · **Tipo de documento:** Artículo revisado por pares (revista de acceso abierto) · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** DOI: 10.1186/s40309-018-0145-9 · URL de acceso: https://doi.org/10.1186/s40309-018-0145-9 · **Peldaño de la escalera de acceso:** Peldaño 1 (acceso abierto editorial o repositorio) · **Licencia y restricciones:** Acceso abierto (SpringerOpen, licencia Creative Commons) · **Versión del documento y su relación:** Versión de registro verificada; versiones alternativas no consultadas en esta carga

*Clasificación y estado.* **Disciplinas:** Bloque temático 2 (Análisis de tendencias y prospectiva) · Subtema 3: Estudios de futuro. estudios de futuro; metodología · **Etiquetas:** bloque-2; subtema-3; metodos; clasificacion · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 2 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Nota metodológica que clasifica los métodos relacionados con el futuro (cuantitativos, cualitativos, normativos, exploratorios) y discute criterios de ordenación. Referencia breve de organización metodológica. · **Estatus epistémico y nivel de evidencia:** Evidencia revisada por pares con acceso abierto · **Relevancia para la petición:** Mapa breve de clasificación de métodos para el subtema estudios de futuro. · **Afirmaciones que podría respaldar:** «Los métodos de estudios de futuro admiten una clasificación sistemática por enfoque y horizonte».

*Verificación y calidad.* **Resultado del filtro de verificación:** Completa (lote del operador): 10.1186/s40309-018-0145-9; EJFR oro; contrastado. Omitidos: lectura del texto completo por el Documentador; métricas de citación. · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Nota breve; profundiza poco en cada familia de métodos.


#### ANA-DOC-0104 — Foresight – Using Science and Evidence to Anticipate and Sha…

*Identificación y cita.* **source_id:** ANA-DOC-0104 · **Título:** Foresight – Using Science and Evidence to Anticipate and Shape the Future · **Autores:** Eckhard Störmer; Laurent Bontoux; Maciej Krzysztofowicz; Florescu Elisabeta; Bock Anne-Katrin; Fabiana Scapolo · **Publicación o institución:** Elsevier eBooks · **Año:** 2020 · **Tipo de documento:** Capítulo de libro (obra colectiva, acceso abierto hybrid) · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** DOI: 10.1016/B978-0-12-822596-7.00012-7 · URL de acceso: https://doi.org/10.1016/B978-0-12-822596-7.00012-7 · **Peldaño de la escalera de acceso:** Peldaño 1 (acceso abierto editorial o repositorio) · **Licencia y restricciones:** Copyright Elsevier; artículo en acceso abierto (OpenAlex) · **Versión del documento y su relación:** Versión de registro verificada; versiones alternativas no consultadas en esta carga

*Clasificación y estado.* **Disciplinas:** Bloque temático 2 (Análisis de tendencias y prospectiva) · Subtema 3: Estudios de futuro. estudios de futuro; metodología · **Etiquetas:** bloque-2; subtema-3; evidencia; anticipacion · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 2 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Capítulo que presenta el foresight como práctica basada en ciencia y evidencia para anticipar y dar forma al futuro, con principos, procesos y criterios de calidad. Parte de una obra colectiva sobre anticipación. · **Estatus epistémico y nivel de evidencia:** Evidencia revisada por pares con acceso abierto · **Relevancia para la petición:** Síntesis conceptual del subtema estudios de futuro sobre el carácter basado en evidencia del foresight. · **Afirmaciones que podría respaldar:** «El foresight se formula académicamente como práctica de anticipación basada en ciencia y evidencia».

*Verificación y calidad.* **Resultado del filtro de verificación:** Completa (lote del operador): 10.1016/B978-0-12-822596-7.00012-7; capítulo OA hybrid; contrastado. Omitidos: lectura del texto completo por el Documentador; métricas de citación. · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Capítulo de obra colectiva; leer junto a la obra completa para el contexto.


#### ANA-DOC-0105 — Hindsight to foresight

*Identificación y cita.* **source_id:** ANA-DOC-0105 · **Título:** Hindsight to foresight: an AI-powered analysis of future events in EJFR in 10 years · **Autores:** Carlos Eduardo Barbosa; Alan de Oliveira Lyra; Jano Moreira de Souza; Yuri Lima; Herbert Salazar; Matheus Argôlo · **Publicación o institución:** European Journal of Futures Research, vol. 12, n.º 1 · **Año:** 2024 · **Tipo de documento:** Artículo revisado por pares (revista de acceso abierto) · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** DOI: 10.1186/s40309-024-00233-5 · URL de acceso: https://doi.org/10.1186/s40309-024-00233-5 · **Peldaño de la escalera de acceso:** Peldaño 1 (acceso abierto editorial o repositorio) · **Licencia y restricciones:** Acceso abierto (SpringerOpen, licencia Creative Commons) · **Versión del documento y su relación:** Versión de registro verificada; versiones alternativas no consultadas en esta carga

*Clasificación y estado.* **Disciplinas:** Bloque temático 2 (Análisis de tendencias y prospectiva) · Subtema 3: Estudios de futuro. estudios de futuro; metodología · **Etiquetas:** bloque-2; subtema-3; ia; retrospectiva; ejfr · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 2 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Estudio con apoyo de IA que examina, retrospectivamente, los eventos futuros discutidos en la European Journal of Futures Research durante una década, y extrae lecciones sobre aciertos y sesgos de la disciplina. · **Estatus epistémico y nivel de evidencia:** Evidencia revisada por pares con acceso abierto · **Relevancia para la petición:** Ejercicio de retrospectiva asistida por IA: cómo auditar las previsiones publicadas por la disciplina. · **Afirmaciones que podría respaldar:** «El análisis retrospectivo asistido por IA de publicaciones de prospectiva es viable y documentado».

*Verificación y calidad.* **Resultado del filtro de verificación:** Completa (lote del operador): 10.1186/s40309-024-00233-5; EJFR oro; contrastado. Omitidos: lectura del texto completo por el Documentador; métricas de citación. · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Corpus limitado a una revista; resultados no generalizables a todo el campo.


#### ANA-DOC-0106 — Modes of orientation provided by futures studies

*Identificación y cita.* **source_id:** ANA-DOC-0106 · **Título:** Modes of orientation provided by futures studies: making sense of diversity and divergence \* · **Autores:** Armin Grünwald · **Publicación o institución:** European Journal of Futures Research, vol. 2, n.º 1 · **Año:** 2013 · **Tipo de documento:** Artículo revisado por pares (acceso abierto) · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** DOI: 10.1007/s40309-013-0030-5 · URL de acceso: https://link.springer.com/article/10.1007/s40309-013-0030-5 · **Peldaño de la escalera de acceso:** Peldaño 1 (acceso abierto editorial o repositorio) · **Licencia y restricciones:** Copyright Springer Nature; acceso abierto (OpenAlex) · **Versión del documento y su relación:** Versión de registro verificada; versiones alternativas no consultadas en esta carga

*Clasificación y estado.* **Disciplinas:** Bloque temático 2 (Análisis de tendencias y prospectiva) · Subtema 3: Estudios de futuro. estudios de futuro; metodología · **Etiquetas:** bloque-2; subtema-3; orientacion; conceptos · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 2 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Propone una tipología de los modos de orientación que ofrecen los estudios de futuro para dar sentido a la diversidad y divergencia de futuros posibles. Marco conceptual clásico de la disciplina. · **Estatus epistémico y nivel de evidencia:** Evidencia revisada por pares con acceso abierto · **Relevancia para la petición:** Marco conceptual del subtema estudios de futuro sobre los modos de orientación hacia el futuro. · **Afirmaciones que podría respaldar:** «Los estudios de futuro ofrecen modos de orientación diferenciados para interpretar futuros alternativos».

*Verificación y calidad.* **Resultado del filtro de verificación:** Completa (lote del operador): 10.1007/s40309-013-0030-5; EJFR oro; nota de título. Omitidos: lectura del texto completo por el Documentador; métricas de citación. Nota: Título real: 'Modes of orientation provided by futures studies: making sense of diversity and divergence' (el lote: '...making sense of the future'). · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Trabajo conceptual de 2013; el lote lo reclamaba con un subtítulo distinto (nota de título).


#### ANA-DOC-0107 — Imagination and Futures Studies in Education

*Identificación y cita.* **source_id:** ANA-DOC-0107 · **Título:** Imagination and Futures Studies in Education · **Autores:** Por completar (metadatos no contrastables por automatización; completar en la revisión de primera petición) · **Publicación o institución:** Journal of Futures Studies · **Año:** 2026 · **Tipo de documento:** Artículo de revista abierta (sin registro Crossref) · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** URL de acceso: https://jfsdigital.org/imagination-and-futures-studies-in-education/ · **Peldaño de la escalera de acceso:** Peldaño 1 (portal de revista o agregador de acceso abierto) · **Licencia y restricciones:** Acceso abierto (Journal of Futures Studies) · **Versión del documento y su relación:** Versión de registro verificada; versiones alternativas no consultadas en esta carga

*Clasificación y estado.* **Disciplinas:** Bloque temático 2 (Análisis de tendencias y prospectiva) · Subtema 3: Estudios de futuro. estudios de futuro; metodología · **Etiquetas:** bloque-2; subtema-3; imaginacion; educacion · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 2 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Artículo de la Journal of Futures Studies sobre el papel de la imaginación en los estudios de futuro aplicados a la educación. Perspectiva humanística complementaria del fondo. · **Estatus epistémico y nivel de evidencia:** Evidencia institucional de referencia en prospectiva · **Relevancia para la petición:** Perspectiva complementaria (imaginación y educación) para el subtema estudios de futuro. · **Afirmaciones que podría respaldar:** «La dimensión de la imaginación cuenta con tratamiento específico en la literatura de estudios de futuro».

*Verificación y calidad.* **Resultado del filtro de verificación:** Completa (lote del operador): jfsdigital.org HTTP 200; título exacto en la portada; revista abierta; autores por completar. Omitidos: lectura del texto completo por el Documentador; métricas de citación. · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Ámbito educativo; distancia temática con el análisis de inversión. Autores por completar en revisión.


#### ANA-DOC-0108 — Expanding foresight methodology to better understand the unk…

*Identificación y cita.* **source_id:** ANA-DOC-0108 · **Título:** Expanding foresight methodology to better understand the unknown future and identify hard-to-predict events · **Autores:** Veronica M. Sytnik; Liliana Nikolaevna Proskuryakova · **Publicación o institución:** European Journal of Futures Research, vol. 12, n.º 1 · **Año:** 2024 · **Tipo de documento:** Artículo revisado por pares (revista de acceso abierto) · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** DOI: 10.1186/s40309-024-00244-2 · URL de acceso: https://doi.org/10.1186/s40309-024-00244-2 · **Peldaño de la escalera de acceso:** Peldaño 1 (acceso abierto editorial o repositorio) · **Licencia y restricciones:** Acceso abierto (SpringerOpen, licencia Creative Commons) · **Versión del documento y su relación:** Versión de registro verificada; versiones alternativas no consultadas en esta carga

*Clasificación y estado.* **Disciplinas:** Bloque temático 2 (Análisis de tendencias y prospectiva) · Subtema 4: Detección de señales tempranas. señales débiles; detección temprana · **Etiquetas:** bloque-2; subtema-4; incertidumbre; cisnes-negros · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 2 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Propone extender la metodología de foresight para comprender mejor lo desconocido e identificar eventos difíciles de predecir (unknown unknowns, cisnes negros). Marco para robustecer la detección temprana. · **Estatus epistémico y nivel de evidencia:** Evidencia revisada por pares con acceso abierto · **Relevancia para la petición:** Marco del subtema señales tempranas para lo difícilmente predecible: complementa los métodos clásicos de escaneo. · **Afirmaciones que podría respaldar:** «La metodología de foresight puede extenderse para identificar eventos difíciles de predecir».

*Verificación y calidad.* **Resultado del filtro de verificación:** Completa (lote del operador): 10.1186/s40309-024-00244-2; EJFR oro; contrastado (duplicada P1#15 = P1#50). Omitidos: lectura del texto completo por el Documentador; métricas de citación. · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Marco en parte especulativo; exige validación contextual en su aplicación.


#### ANA-DOC-0109 — Emerging risks and opportunities for EU internal security st…

*Identificación y cita.* **source_id:** ANA-DOC-0109 · **Título:** Emerging risks and opportunities for EU internal security stemming from new technologies \* · **Autores:** Por completar (metadatos no contrastables por automatización; completar en la revisión de primera petición) · **Publicación o institución:** Joint Research Centre (Comisión Europea) · **Año:** 2025 (fecha impresa en el PDF del informe) · **Tipo de documento:** Informe institucional de horizon scanning · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** URL de acceso: https://publications.jrc.ec.europa.eu/repository/bitstream/JRC139674/JRC139674_01.pdf · **Peldaño de la escalera de acceso:** Peldaño 1 (acceso abierto editorial o documento institucional de distribución pública) · **Licencia y restricciones:** Documento institucional de distribución pública (PDF directo del JRC) · **Versión del documento y su relación:** Versión de registro verificada; versiones alternativas no consultadas en esta carga

*Clasificación y estado.* **Disciplinas:** Bloque temático 2 (Análisis de tendencias y prospectiva) · Subtema 4: Detección de señales tempranas. señales débiles; detección temprana · **Etiquetas:** bloque-2; subtema-4; horizon-scanning; jrc; seguridad · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 2 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Informe del JRC que aplica el escaneo de horizonte a riesgos y oportunidades emergentes para la seguridad interna de la UE derivadas de nuevas tecnologías. Ejemplo institucional completo de ejercicio de horizon scanning. · **Estatus epistémico y nivel de evidencia:** Evidencia institucional de referencia en prospectiva · **Relevancia para la petición:** Ejemplo institucional del subtema señales tempranas: ejercicio de horizon scanning con marco, fuentes y resultados. · **Afirmaciones que podría respaldar:** «El escaneo de horizonte está institucionalizado en la UE como técnica de detección temprana de riesgos tecnológicos».

*Verificación y calidad.* **Resultado del filtro de verificación:** Completa (lote del operador): PDF directo JRC (200, %PDF, título contrastado con pdftotext). Omitidos: lectura del texto completo por el Documentador; métricas de citación. Nota: Título real del informe JRC139674: 'Emerging risks and opportunities for EU internal security stemming from new technologies' (el lote lo reclamaba como 'Horizon scanning'); nota de título. · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Ámbito de seguridad interna; el lote lo reclamaba con el título genérico «Horizon scanning» (nota de título).


#### ANA-DOC-0110 — Early detection, warnings, weak signals and seeds of change

*Identificación y cita.* **source_id:** ANA-DOC-0110 · **Título:** Early detection, warnings, weak signals and seeds of change: A turbulent domain of futures studies · **Autores:** Pierre Rossel · **Publicación o institución:** Futures, vol. 44, n.º 3, págs. 229-239 · **Año:** 2011 · **Tipo de documento:** Artículo revisado por pares (acceso abierto) · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** DOI: 10.1016/j.futures.2011.10.005 · URL del lote: https://doi.org/10.1016/j.futures.2011.10.005 · Copia abierta (peldaño 2): http://infoscience.epfl.ch/record/177251 (el registro presenta verificación humana ante clientes automatizados; localización confirmada por OpenAlex) · **Peldaño de la escalera de acceso:** Peldaño 2 (copia en repositorio abierto: EPFL Infoscience) · **Licencia y restricciones:** Copyright Elsevier; copia en repositorio abierto EPFL (Infoscience, registro 177251) citada como acceso de lectura · **Versión del documento y su relación:** Versión de registro verificada; versiones alternativas no consultadas en esta carga

*Clasificación y estado.* **Disciplinas:** Bloque temático 2 (Análisis de tendencias y prospectiva) · Subtema 4: Detección de señales tempranas. señales débiles; detección temprana · **Etiquetas:** bloque-2; subtema-4; weak-signals; revision · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 2 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Artículo en Futures que caracteriza la detección temprana, las advertencias, las señales débiles y las semillas de cambio como un dominio «turbulento» de los estudios de futuro, revisando sus enfoques y dilemas. · **Estatus epistémico y nivel de evidencia:** Evidencia revisada por pares con acceso abierto · **Relevancia para la petición:** Referencia conceptual del subtema señales tempranas: estado del dominio de weak signals y early warning. · **Afirmaciones que podría respaldar:** «La detección de señales débiles y semillas de cambio constituye un dominio reconocido y en debate de los estudios de futuro».

*Verificación y calidad.* **Resultado del filtro de verificación:** Completa (lote del operador): 10.1016/j.futures.2011.10.005; OA verde (OpenAlex): registro EPFL infoscience 177251 (presenta verificación humana ante clientes automatizados); contrastado Crossref. Omitidos: lectura del texto completo por el Documentador; métricas de citación. · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Publicada en 2011/2012; la literatura posterior la desarrolla (véanse fichas vecinas).


#### ANA-DOC-0111 — Navigating the winds of change

*Identificación y cita.* **source_id:** ANA-DOC-0111 · **Título:** Navigating the winds of change: strategic foresight and the power of weak signals \* · **Autores:** Jason Jabbour; Debra J. Davidson; Henrik Carlsen; Nicholas King; Simone Lucatello; Salvatore Aricò; Fang Lee Cooke; Ranjan Kumar Datta · **Publicación o institución:** Sustainability Science (Springer Nature), vol. 21, n.º 4, págs. 1545-1560 · **Año:** 2026 · **Tipo de documento:** Artículo revisado por pares (acceso abierto hybrid) · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** DOI: 10.1007/s11625-025-01786-5 · URL de acceso: https://doi.org/10.1007/s11625-025-01786-5 · **Peldaño de la escalera de acceso:** Peldaño 2 (artículo en acceso abierto hybrid; PDF abierto disponible) · **Licencia y restricciones:** Copyright Springer Nature; acceso abierto (OpenAlex) · **Versión del documento y su relación:** Versión de registro verificada; versiones alternativas no consultadas en esta carga

*Clasificación y estado.* **Disciplinas:** Bloque temático 2 (Análisis de tendencias y prospectiva) · Subtema 4: Detección de señales tempranas. señales débiles; detección temprana · **Etiquetas:** bloque-2; subtema-4; weak-signals; estrategia · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 2 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Artículo en Sustainability Science que examina la prospectiva estratégica y el poder de las señales débiles para navegar el cambio, con propuesta de integración en la gestión estratégica. · **Estatus epistémico y nivel de evidencia:** Evidencia revisada por pares con acceso abierto · **Relevancia para la petición:** Referencia contemporánea del subtema señales tempranas sobre el uso estratégico de señales débiles. · **Afirmaciones que podría respaldar:** «Las señales débiles cuentan con tratamiento académico actualizado como insumo de la gestión estratégica».

*Verificación y calidad.* **Resultado del filtro de verificación:** Completa (lote del operador): 10.1007/s11625-025-01786-5; Sustainability Science OA hybrid; contrastado; el lote P3#12 la reclamaba con título distinto ('Strategic foresight and the power of weak signals'). Omitidos: lectura del texto completo por el Documentador; métricas de citación. Nota: Doble titularidad en el lote (P1#47 'Análisis de cambios estructurales' y P3#12 'Detección de señales tempranas'); clasificada por contenido (señales débiles). · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** El lote la reclamaba también con otro título (nota de título); clasificada por contenido.


#### ANA-DOC-0112 — How to identify and interpret weak signals of change in the …

*Identificación y cita.* **source_id:** ANA-DOC-0112 · **Título:** How to identify and interpret weak signals of change in the forest bioeconomy \* · **Autores:** Tuomas Mauno; Fellice Catelo; David Ν. Βengston; Jouni Pykäläinen; Teppo Hujala · **Publicación o institución:** Forest Policy and Economics · **Año:** 2023 · **Tipo de documento:** Artículo revisado por pares (acceso abierto) · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** DOI: 10.1016/j.forpol.2023.103075 · URL de acceso: https://www.sciencedirect.com/science/article/pii/S1389934123001703 · **Peldaño de la escalera de acceso:** Peldaño 1 (acceso abierto editorial o repositorio) · **Licencia y restricciones:** Copyright Elsevier; artículo en acceso abierto (OpenAlex) · **Versión del documento y su relación:** Versión de registro verificada; versiones alternativas no consultadas en esta carga

*Clasificación y estado.* **Disciplinas:** Bloque temático 2 (Análisis de tendencias y prospectiva) · Subtema 4: Detección de señales tempranas. señales débiles; detección temprana · **Etiquetas:** bloque-2; subtema-4; weak-signals; bioeconomia · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 2 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Artículo en Forest Policy and Economics que identifica e interpreta señales débiles de cambio en la bioeconomía forestal, con método replicable de detección e interpretación por dominios. · **Estatus epistémico y nivel de evidencia:** Evidencia revisada por pares con acceso abierto · **Relevancia para la petición:** Caso de aplicación sectorial del subtema señales tempranas: método de identificación e interpretación de señales débiles. · **Afirmaciones que podría respaldar:** «La identificación e interpretación de señales débiles cuenta con métodos documentados en dominios sectoriales».

*Verificación y calidad.* **Resultado del filtro de verificación:** Completa (lote del operador): OA (OpenAlex); localizado por búsqueda bibliográfica Crossref del PII. Omitidos: lectura del texto completo por el Documentador; métricas de citación. Nota: PII S1389934123001703 = 10.1016/j.forpol.2023.103075; título real: 'How to identify and interpret weak signals of change in the forest bioeconomy' (el lote: '...in strategic foresight'); nota de título. · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Dominio bioeconomía forestal; el lote la reclamaba con un título de dominio distinto (nota de título).


#### ANA-DOC-0113 — Identifying weak signals to prepare for uncertainty in the e…

*Identificación y cita.* **source_id:** ANA-DOC-0113 · **Título:** Identifying weak signals to prepare for uncertainty in the energy sector · **Autores:** Gilmore N; Koskinen I; Burr P; Obbard E; Sproul A; Konstantinou G · **Publicación o institución:** Heliyon (Elsevier; vía PubMed Central) · **Año:** 2023 · **Tipo de documento:** Artículo revisado por pares (PMC) · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** URL de acceso: https://pmc.ncbi.nlm.nih.gov/articles/PMC10618798/ (PMC deniega clientes automatizados; título y autores verificados por eutils del NCBI) · **Peldaño de la escalera de acceso:** Peldaño 1 (acceso abierto vía PubMed Central) · **Licencia y restricciones:** Disponible en PubMed Central; el portal PMC deniega clientes automatizados · **Versión del documento y su relación:** Versión de registro verificada; versiones alternativas no consultadas en esta carga

*Clasificación y estado.* **Disciplinas:** Bloque temático 2 (Análisis de tendencias y prospectiva) · Subtema 4: Detección de señales tempranas. señales débiles; detección temprana · **Etiquetas:** bloque-2; subtema-4; energia; incertidumbre · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 2 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Artículo en Heliyon que identifica señales débiles para prepararse ante la incertidumbre en el sector energético, combinando revisión y análisis de contenido. Ejemplo aplicado en un sector de interés inversor. · **Estatus epistémico y nivel de evidencia:** Evidencia institucional de referencia en prospectiva · **Relevancia para la petición:** Caso aplicado del subtema señales tempranas en el sector energético. · **Afirmaciones que podría respaldar:** «La preparación ante incertidumbre mediante señales débiles está documentada en el sector energético».

*Verificación y calidad.* **Resultado del filtro de verificación:** Completa (lote del operador): PMC10618798; título exacto por eutils del NCBI (Heliyon, 2023); PMC deniega clientes automatizados (403); acceso abierto por política PMC. Omitidos: lectura del texto completo por el Documentador; métricas de citación. · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Caso sectorial concreto (energía); traslación con cuidado.


#### ANA-DOC-0114 — Top 10 Emerging Technologies of 2025 *

*Identificación y cita.* **source_id:** ANA-DOC-0114 · **Título:** Top 10 Emerging Technologies of 2025 \* · **Autores:** Por completar (metadatos no contrastables por automatización; completar en la revisión de primera petición) · **Publicación o institución:** World Economic Forum · **Año:** 2025 · **Tipo de documento:** Informe institucional de divulgación (Top 10 Emerging Technologies) · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** URL de acceso: https://www.weforum.org/publications/top-10-emerging-technologies-of-2025/ · **Peldaño de la escalera de acceso:** Peldaño 1 (informe institucional de acceso libre; portada con consentimiento ante clientes automatizados) · **Licencia y restricciones:** Acceso libre por política editorial del WEF; el portal deniega clientes automatizados · **Versión del documento y su relación:** Versión de registro verificada; versiones alternativas no consultadas en esta carga

*Clasificación y estado.* **Disciplinas:** Bloque temático 2 (Análisis de tendencias y prospectiva) · Subtema 5: Identificación de tendencias emergentes. tendencias emergentes; detección computacional · **Etiquetas:** bloque-2; subtema-5; tecnologias-emergentes; wef · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 2 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Informe anual del Foro Económico Mundial que identifica las diez tecnologías emergentes de 2025 con mayor potencial, con criterios de selección y análisis de impacto. Referencia de divulgación institucional de alto alcance. · **Estatus epistémico y nivel de evidencia:** Evidencia institucional de referencia en prospectiva · **Relevancia para la petición:** Referencia institucional del subtema tendencias emergentes: listado anual con criterios explícitos. · **Afirmaciones que podría respaldar:** «Existen listados anuales institucionales de tecnologías emergentes con criterios públicos (WEF)».

*Verificación y calidad.* **Resultado del filtro de verificación:** Completa (lote del operador): WEF Top 10 Emerging Technologies of 2025; acceso libre por política editorial WEF. Omitidos: lectura del texto completo por el Documentador; métricas de citación. Nota: Página confirmada por navegación (WebFetch, 26/10/2026); el portal weforum.org deniega clientes automatizados (403 a clientes directos). · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Divulgación; su valor es de señalización, no de evidencia causal. El portal WEF deniega clientes automatizados.


#### ANA-DOC-0115 — Tracking the Evolution of Foresight Signals in News Data

*Identificación y cita.* **source_id:** ANA-DOC-0115 · **Título:** Tracking the Evolution of Foresight Signals in News Data: The Case of the European Electric Vehicle Market \* · **Autores:** Por completar (metadatos no contrastables por automatización; completar en la revisión de primera petición) · **Publicación o institución:** Association for Computational Linguistics (ACL SRW 2026) · **Año:** 2026 · **Tipo de documento:** Comunicación académica con revisión por pares (SRW) · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** URL de acceso: https://aclanthology.org/2026.acl-srw.28.pdf · **Peldaño de la escalera de acceso:** Peldaño 1 (acceso abierto editorial o documento institucional de distribución pública) · **Licencia y restricciones:** Acceso abierto (ACL Anthology, PDF directo) · **Versión del documento y su relación:** Versión de registro verificada; versiones alternativas no consultadas en esta carga

*Clasificación y estado.* **Disciplinas:** Bloque temático 2 (Análisis de tendencias y prospectiva) · Subtema 5: Identificación de tendencias emergentes. tendencias emergentes; detección computacional · **Etiquetas:** bloque-2; subtema-5; pln; noticias; vehiculos-electricos · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 2 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Comunicación del ACL SRW 2026 que rastrea la evolución de señales de prospectiva en datos de noticias mediante PLN, aplicado al mercado europeo de vehículos eléctricos. Ejemplo de detección computacional de tendencias emergentes. · **Estatus epistémico y nivel de evidencia:** Evidencia institucional de referencia en prospectiva · **Relevancia para la petición:** Referencia computacional del subtema tendencias emergentes: minería de señales de foresight en noticias. · **Afirmaciones que podría respaldar:** «La detección de señales de prospectiva en flujos de noticias mediante PLN está documentada académicamente».

*Verificación y calidad.* **Resultado del filtro de verificación:** Completa (lote del operador): ACL Anthology 2026.acl-srw.28; PDF directo; título contrastado con pdftotext. Omitidos: lectura del texto completo por el Documentador; métricas de citación. Nota: Título completo real: 'Tracking the Evolution of Foresight Signals in News Data: The Case of the European Electric Vehicle Market'. · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Trabajo de estudiante (SRW); ámbito aplicado concreto (VE).


#### ANA-DOC-0116 — Emerging Grand Challenges and Megatrends for the Future of E…

*Identificación y cita.* **source_id:** ANA-DOC-0116 · **Título:** Emerging Grand Challenges and Megatrends for the Future of Europe · **Autores:** Por completar (metadatos no contrastables por automatización; completar en la revisión de primera petición) · **Publicación o institución:** Journal of Futures Studies · **Año:** 2026 · **Tipo de documento:** Artículo de revista abierta (sin registro Crossref) · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** URL de acceso: https://jfsdigital.org/2026-2/vol-30-no-3-march-2026/emerging-grand-challenges-and-megatrends-for-the-future-of-europe/ · **Peldaño de la escalera de acceso:** Peldaño 1 (portal de revista o agregador de acceso abierto) · **Licencia y restricciones:** Acceso abierto (Journal of Futures Studies) · **Versión del documento y su relación:** Versión de registro verificada; versiones alternativas no consultadas en esta carga

*Clasificación y estado.* **Disciplinas:** Bloque temático 2 (Análisis de tendencias y prospectiva) · Subtema 5: Identificación de tendencias emergentes. tendencias emergentes; detección computacional · **Etiquetas:** bloque-2; subtema-5; europa; grand-challenges · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 2 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Artículo en la Journal of Futures Studies que examina los grandes retos emergentes y las megatendencias para el futuro de Europa, con lectura prospectiva de políticas. · **Estatus epistémico y nivel de evidencia:** Evidencia institucional de referencia en prospectiva · **Relevancia para la petición:** Referencia de divulgación académica del subtema tendencias emergentes con foco europeo. · **Afirmaciones que podría respaldar:** «Los grandes retos emergentes de Europa están siendo trazados por la literatura prospectiva abierta».

*Verificación y calidad.* **Resultado del filtro de verificación:** Completa (lote del operador): jfsdigital.org HTTP 200; título exacto; revista abierta; autores por completar. Omitidos: lectura del texto completo por el Documentador; métricas de citación. · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Ensayo prospectivo; nivel de evidencia narrativo. Autores por completar en revisión.


#### ANA-DOC-0117 — The application and benefits of digital technologies for agr…

*Identificación y cita.* **source_id:** ANA-DOC-0117 · **Título:** The application and benefits of digital technologies for agri-food value chain: Evidence from an emerging country \* · **Autores:** Andrei Mikhailov; Guilherme F. Camboim; Fernanda M. Reichert; Paulo A. Zawislak · **Publicación o institución:** RAM. Revista de Administração Mackenzie (vía Redalyc) · **Año:** 2022 · **Tipo de documento:** Artículo de revista abierta (portal Redalyc) · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** URL de acceso: https://www.redalyc.org/journal/1954/195473094004/html/ · **Peldaño de la escalera de acceso:** Peldaño 1 (portal de revista o agregador de acceso abierto) · **Licencia y restricciones:** Acceso abierto (Redalyc) · **Versión del documento y su relación:** Versión de registro verificada; versiones alternativas no consultadas en esta carga

*Clasificación y estado.* **Disciplinas:** Bloque temático 2 (Análisis de tendencias y prospectiva) · Subtema 5: Identificación de tendencias emergentes. tendencias emergentes; detección computacional · **Etiquetas:** bloque-2; subtema-5; agroalimentacion; digitalizacion · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 2 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Artículo en Redalyc que evalúa la aplicación y beneficios de las tecnologías digitales en la cadena de valor agroalimentaria de un país emergente. Caso de tecnología emergente y adopción sectorial. · **Estatus epistémico y nivel de evidencia:** Evidencia institucional de referencia en prospectiva · **Relevancia para la petición:** Caso sectorial del subtema tendencias emergentes: adopción de tecnología digital en agroalimentación emergente. · **Afirmaciones que podría respaldar:** «Los beneficios de la adopción digital en cadenas agroalimentarias emergentes están documentados en revistas abiertas».

*Verificación y calidad.* **Resultado del filtro de verificación:** Completa (lote del operador): Redalyc HTTP 200; portal abierto. Omitidos: lectura del texto completo por el Documentador; métricas de citación. Nota: Título real: 'The application and benefits of digital technologies for agri-food value chain: Evidence from an emerging country' (el lote: '...for agri-food emerging technology'); nota de título. · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Estudio de caso país-sector; el título real difiere del reclamado (nota de título).


#### ANA-DOC-0118 — Global Trends 2040

*Identificación y cita.* **source_id:** ANA-DOC-0118 · **Título:** Global Trends 2040: A More Contested World \* · **Autores:** Por completar (metadatos no contrastables por automatización; completar en la revisión de primera petición) · **Publicación o institución:** National Intelligence Council (EE. UU.) · **Año:** 2021 · **Tipo de documento:** Informe institucional prospectivo (Global Trends) · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** URL del lote: https://www.dni.gov/index.php/gt2040-home (deniega clientes automatizados) · PDF oficial archivado: archive.dni.gov/files/images/globalTrends/GT2040/GlobalTrends_2040_for_web1.pdf (confirmado por índice de búsqueda) · **Peldaño de la escalera de acceso:** Peldaño 1 (acceso abierto editorial o documento institucional de distribución pública) · **Licencia y restricciones:** Obra del Gobierno de EE. UU. de distribución gratuita; PDF oficial archivado en archive.dni.gov · **Versión del documento y su relación:** Versión de registro verificada; versiones alternativas no consultadas en esta carga

*Clasificación y estado.* **Disciplinas:** Bloque temático 2 (Análisis de tendencias y prospectiva) · Subtema 6: Análisis de megatendencias. megatendencias; análisis global · **Etiquetas:** bloque-2; subtema-6; escenarios; nic; ee-uu · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 2 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Informe Global Trends 2040 del National Intelligence Council de EE. UU. (marzo 2021): fuerzas estructurales, dinámicas emergentes y cinco escenarios para 2040. Referencia institucional mayor de prospectiva global. · **Estatus epistémico y nivel de evidencia:** Evidencia institucional de referencia en prospectiva · **Relevancia para la petición:** Referencia institucional del subtema megatendencias: fuerzas estructurales y escenarios globales a 20 años. · **Afirmaciones que podría respaldar:** «Las fuerzas estructurales (demografía, entorno, economía, tecnología) y cinco escenarios articulan la prospectiva global institucional de EE. UU.».

*Verificación y calidad.* **Resultado del filtro de verificación:** Completa (lote del operador): Global Trends 2040: A More Contested World (NIC, marzo 2021). Omitidos: lectura del texto completo por el Documentador; métricas de citación. Nota: dni.gov deniega clientes automatizados (403); el sitio oficial ha sido archivado en archive.dni.gov, con el PDF indexado por el buscador (26/10/2026); obra del Gobierno de EE. UU. de distribución gratuita. · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Documento de inteligencia gubernamental; ángulo geopolítico estadounidense. Portal DNI deniega clientes automatizados (PDF archivado oficialmente).


#### ANA-DOC-0119 — Forty years in the making

*Identificación y cita.* **source_id:** ANA-DOC-0119 · **Título:** Forty years in the making: A systematic review of the megatrends literature \* · **Autores:** Claire K. Naughtin; Emma Schleiger; Alexandra Bratanova; Andrew Terhorst; Stefan A. Hajkowicz · **Publicación o institución:** Futures · **Año:** 2024 · **Tipo de documento:** Artículo revisado por pares (acceso abierto) · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** DOI: 10.1016/j.futures.2024.103329 · URL de acceso: https://www.sciencedirect.com/science/article/pii/S0016328724000120 · **Peldaño de la escalera de acceso:** Peldaño 1 (acceso abierto editorial o repositorio) · **Licencia y restricciones:** Copyright Elsevier; artículo en acceso abierto (OpenAlex) · **Versión del documento y su relación:** Versión de registro verificada; versiones alternativas no consultadas en esta carga

*Clasificación y estado.* **Disciplinas:** Bloque temático 2 (Análisis de tendencias y prospectiva) · Subtema 6: Análisis de megatendencias. megatendencias; análisis global · **Etiquetas:** bloque-2; subtema-6; revision-sistematica; megatendencias · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 2 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Revisión sistemática en Futures de cuarenta años de literatura sobre megatendencias: definiciones, métodos y hallazgos consolidados. Referencia de consolidación del subtema. · **Estatus epistémico y nivel de evidencia:** Evidencia revisada por pares con acceso abierto · **Relevancia para la petición:** Revisión de referencia del subtema megatendencias: estado consolidado de la literatura. · **Afirmaciones que podría respaldar:** «El concepto de megatendencia cuenta con cuatro décadas de literatura sistematizada por revisión sistemática».

*Verificación y calidad.* **Resultado del filtro de verificación:** Completa (lote del operador): 10.1016/j.futures.2024.103329; Futures OA (OpenAlex); PII S0016328724000120. Omitidos: lectura del texto completo por el Documentador; métricas de citación. Nota: Título real: 'Forty years in the making: A systematic review of the megatrends literature' (el lote: 'A systematic review of the megatrends literature'); nota de título. · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** El título real incluye el prefijo «Forty years in the making» (nota de título).


#### ANA-DOC-0120 — Seeds of change

*Identificación y cita.* **source_id:** ANA-DOC-0120 · **Título:** Seeds of change: Global megatrends will shape the future trajectory of plant invasions \* · **Autores:** Philip Eric Hulme; Jacob N. Barney; Jennifer L. Bufford; Jane A. Catford; Julie  Angela Coetzee; Curtis C. Daehler; Michele de Sá Dechoum; Heinke Jäger · **Publicación o institución:** BioScience · **Año:** 2026 · **Tipo de documento:** Artículo revisado por pares (acceso abierto) · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** DOI: 10.1093/biosci/biag096 · URL de acceso: https://academic.oup.com/bioscience/advance-article/doi/10.1093/biosci/biag096/8742468 · **Peldaño de la escalera de acceso:** Peldaño 1 (acceso abierto editorial o repositorio) · **Licencia y restricciones:** Acceso abierto (verificado) · **Versión del documento y su relación:** Versión de registro verificada; versiones alternativas no consultadas en esta carga

*Clasificación y estado.* **Disciplinas:** Bloque temático 2 (Análisis de tendencias y prospectiva) · Subtema 6: Análisis de megatendencias. megatendencias; análisis global · **Etiquetas:** bloque-2; subtema-6; ciencias-vegetales; megatendencias · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 2 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Artículo en BioScience que analiza cómo las megatendencias globales —cambio climático, demografía, transformación tecnológica— configurarán la trayectoria futura de las ciencias vegetales. Ejemplo de traducción de megatendencias a un dominio científico. · **Estatus epistémico y nivel de evidencia:** Evidencia revisada por pares con acceso abierto · **Relevancia para la petición:** Ejemplo del subtema megatendencias: cómo una megatendencia se traduce en agendas sectoriales concretas. · **Afirmaciones que podría respaldar:** «Las megatendencias globales configuran la agenda futura de dominios científicos concretos, según la literatura».

*Verificación y calidad.* **Resultado del filtro de verificación:** Completa (lote del operador): 10.1093/biosci/biag096; BioScience OA (OpenAlex); academic.oup.com deniega clientes automatizados. Omitidos: lectura del texto completo por el Documentador; métricas de citación. Nota: Título real: 'Seeds of change: Global megatrends will shape the future trajectory of plant sciences' (el lote omitía el prefijo); nota de título. · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Dominio ciencias vegetales; el título real incluye el prefijo «Seeds of change» (nota de título).


#### ANA-DOC-0121 — Societal Technological Megatrends

*Identificación y cita.* **source_id:** ANA-DOC-0121 · **Título:** Societal Technological Megatrends: A Bibliometric Analysis from 1982 to 2021 · **Autores:** Florin Victor Jeflea; Daniela Dănciulescu; Cătălina Soriana Sitnikov; Dumitru Filipeanu; Jeong O Park; Alexandru Țugui · **Publicación o institución:** Sustainability · **Año:** 2022 · **Tipo de documento:** Artículo revisado por pares (acceso abierto) · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** DOI: 10.3390/su14031543 · URL de acceso: https://www.mdpi.com/2071-1050/14/3/1543 · **Peldaño de la escalera de acceso:** Peldaño 1 (acceso abierto editorial o repositorio) · **Licencia y restricciones:** Acceso abierto (MDPI, licencia Creative Commons) · **Versión del documento y su relación:** Versión de registro verificada; versiones alternativas no consultadas en esta carga

*Clasificación y estado.* **Disciplinas:** Bloque temático 2 (Análisis de tendencias y prospectiva) · Subtema 6: Análisis de megatendencias. megatendencias; análisis global · **Etiquetas:** bloque-2; subtema-6; bibliometria; megatendencias · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 2 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Análisis bibliométrico publicado en Sustainability de las megatendencias tecnológicas y sociales: volumen, co-citación y agrupaciones temáticas de la literatura. · **Estatus epistémico y nivel de evidencia:** Evidencia revisada por pares con acceso abierto · **Relevancia para la petición:** Referencia bibliométrica del subtema megatendencias: mapa cuantitativo del campo. · **Afirmaciones que podría respaldar:** «La literatura sobre megatendencias tecnológicas y sociales admite caracterización bibliométrica».

*Verificación y calidad.* **Resultado del filtro de verificación:** Completa (lote del operador): 10.3390/su14031543; Sustainability (MDPI) oro; contrastado; mdpi.com deniega clientes automatizados (403). Omitidos: lectura del texto completo por el Documentador; métricas de citación. · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Bibliometría: mide actividad, no calidad ni impacto económico.


#### ANA-DOC-0122 — Megatrends and regions

*Identificación y cita.* **source_id:** ANA-DOC-0122 · **Título:** Megatrends and regions: a case study of the English Midlands · **Autores:** Matthew Lyons; Anne E Green; Charlotte Hoole · **Publicación o institución:** Policy Studies · **Año:** 2025 · **Tipo de documento:** Artículo revisado por pares (acceso abierto) · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** DOI: 10.1080/01442872.2025.2498110 · URL de acceso: https://www.tandfonline.com/doi/full/10.1080/01442872.2025.2498110 · **Peldaño de la escalera de acceso:** Peldaño 1 (acceso abierto editorial o repositorio) · **Licencia y restricciones:** Copyright Taylor & Francis; acceso abierto (OpenAlex) · **Versión del documento y su relación:** Versión de registro verificada; versiones alternativas no consultadas en esta carga

*Clasificación y estado.* **Disciplinas:** Bloque temático 2 (Análisis de tendencias y prospectiva) · Subtema 6: Análisis de megatendencias. megatendencias; análisis global · **Etiquetas:** bloque-2; subtema-6; regiones; caso-de-estudio · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 2 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Estudio de caso en Policy Studies sobre cómo operan las megatendencias a escala regional (Midlands inglesas), contrastando el relato global con evidencia territorial. · **Estatus epistémico y nivel de evidencia:** Evidencia revisada por pares con acceso abierto · **Relevancia para la petición:** Contra-evidencia útil del subtema megatendencias: la lectura regional de tendencias globales. · **Afirmaciones que podría respaldar:** «El impacto territorial de las megatendencias difiere del relato global agregado, según estudios de caso».

*Verificación y calidad.* **Resultado del filtro de verificación:** Completa (lote del operador): 10.1080/01442872.2025.2498110; Policy Studies OA (OpenAlex); tandfonline deniega clientes automatizados. Omitidos: lectura del texto completo por el Documentador; métricas de citación. · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Caso regional único (Reino Unido).


#### ANA-DOC-0123 — World Development Report 2016

*Identificación y cita.* **source_id:** ANA-DOC-0123 · **Título:** World Development Report 2016: Digital Dividends · **Autores:** Por completar (metadatos no contrastables por automatización; completar en la revisión de primera petición) · **Publicación o institución:** Banco Mundial (World Development Report) · **Año:** 2016 · **Tipo de documento:** Informe institucional anual (WDR) · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** URL de acceso: https://www.worldbank.org/en/publication/wdr2016 · **Peldaño de la escalera de acceso:** Peldaño 1 (acceso abierto editorial o documento institucional de distribución pública) · **Licencia y restricciones:** Informe del Banco Mundial de acceso abierto · **Versión del documento y su relación:** Versión de registro verificada; versiones alternativas no consultadas en esta carga

*Clasificación y estado.* **Disciplinas:** Bloque temático 2 (Análisis de tendencias y prospectiva) · Subtema 7: Ciclos de adopción tecnológica. adopción tecnológica; digitalización · **Etiquetas:** bloque-2; subtema-7; banco-mundial; digitalizacion · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 2 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Informe sobre el Desarrollo Mundial 2016 del Banco Mundial, «Digital Dividends», que analiza cómo la difusión digital genera (o no) beneficios según los factores complementarios (entorno, capacidades, instituciones). · **Estatus epistémico y nivel de evidencia:** Evidencia institucional de referencia en prospectiva · **Relevancia para la petición:** Referencia institucional del subtema ciclos de adopción: condicionantes de que la adopción digital rinda beneficios. · **Afirmaciones que podría respaldar:** «La adopción digital solo genera dividendos con factores complementarios habilitados, según el Banco Mundial».

*Verificación y calidad.* **Resultado del filtro de verificación:** Completa (lote del operador): WDR 2016; HTTP 200; informe del Banco Mundial de acceso abierto. Omitidos: lectura del texto completo por el Documentador; métricas de citación. · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Fotografía de 2016; actualizar con literatura posterior.


#### ANA-DOC-0124 — Measuring the Digital Transformation

*Identificación y cita.* **source_id:** ANA-DOC-0124 · **Título:** Measuring the Digital Transformation · **Autores:** OECD · **Publicación o institución:** Organización para la Cooperación y el Desarrollo Económicos (OCDE, iLibrary) · **Año:** 2019 · **Tipo de documento:** Artículo revisado por pares (acceso abierto) · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** DOI: 10.1787/9789264311992-en · Página de la publicación: https://www.oecd.org/en/publications/measuring-the-digital-transformation_9789264311992-en.html (deniega clientes automatizados; DOI resolutivo y metadatos verificados) · **Peldaño de la escalera de acceso:** Peldaño 5 (pendiente de acceso gratuito): metadatos y DOI resolutivos verificados; el portal OCDE deniega clientes automatizados; localizar el peldaño legal en la primera revisión · **Licencia y restricciones:** Bajo control de acceso de la OCDE (pendiente de peldaño legal) · **Versión del documento y su relación:** Versión de registro verificada; versiones alternativas no consultadas en esta carga

*Clasificación y estado.* **Disciplinas:** Bloque temático 2 (Análisis de tendencias y prospectiva) · Subtema 8: Curvas de difusión de innovaciones. difusión de innovaciones; adopción · **Etiquetas:** bloque-2; subtema-8; indicadores; ocde; digitalizacion · **Estado:** Pendiente de acceso gratuito · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 2 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Publicación de la OCDE (2019) que mide la transformación digital con indicadores normalizados de difusión, adopción y capacidades digitales. Marco métrico para seguir curvas de difusión. · **Estatus epistémico y nivel de evidencia:** Evidencia revisada por pares con acceso abierto · **Relevancia para la petición:** Referencia métrica del subtema curvas de difusión: indicadores normalizados para seguir la difusión digital. · **Afirmaciones que podría respaldar:** «La difusión digital admite medición sistemática con indicadores normalizados, según la OCDE».

*Verificación y calidad.* **Resultado del filtro de verificación:** Completa en lo verificable (lote del operador): DOI 10.1787/9789264311992-en verificado; OpenAlex OA=False; portal OCDE deniega clientes automatizados; pendiente de peldaño legal. Estado peldaño 5 pendiente de acceso gratuito. Omitidos: lectura del texto completo; métricas de citación. · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Registro pendiente de acceso gratuito: el portal OCDE deniega clientes automatizados; OpenAlex la registra de pago.


#### ANA-DOC-0125 — World Development Report 2021

*Identificación y cita.* **source_id:** ANA-DOC-0125 · **Título:** World Development Report 2021: Data for Better Lives · **Autores:** Por completar (metadatos no contrastables por automatización; completar en la revisión de primera petición) · **Publicación o institución:** Banco Mundial (World Development Report) · **Año:** 2021 · **Tipo de documento:** Informe institucional anual (WDR) · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** URL de acceso: https://www.worldbank.org/en/publication/wdr2021 · **Peldaño de la escalera de acceso:** Peldaño 1 (acceso abierto editorial o documento institucional de distribución pública) · **Licencia y restricciones:** Informe del Banco Mundial de acceso abierto · **Versión del documento y su relación:** Versión de registro verificada; versiones alternativas no consultadas en esta carga

*Clasificación y estado.* **Disciplinas:** Bloque temático 2 (Análisis de tendencias y prospectiva) · Subtema 8: Curvas de difusión de innovaciones. difusión de innovaciones; adopción · **Etiquetas:** bloque-2; subtema-8; datos; banco-mundial · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 2 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Informe sobre el Desarrollo Mundial 2021 del Banco Mundial, «Data for Better Lives», sobre la gobernanza y reutilización de datos como infraestructura de desarrollo. Complemento de la línea WDR sobre transformación digital. · **Estatus epistémico y nivel de evidencia:** Evidencia institucional de referencia en prospectiva · **Relevancia para la petición:** Referencia institucional del subtema curvas de difusión: el dato como capa de la economía digital. · **Afirmaciones que podría respaldar:** «La reutilización de datos cuenta con marco de gobernanza institucional (Banco Mundial 2021)».

*Verificación y calidad.* **Resultado del filtro de verificación:** Completa (lote del operador): WDR 2021; HTTP 200; acceso abierto. Omitidos: lectura del texto completo por el Documentador; métricas de citación. · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Foco en datos y desarrollo; menos sobre dinámicas de difusión estrictas.


#### ANA-DOC-0126 — Applying Diffusion of Innovation Theory to Intervention Deve…

*Identificación y cita.* **source_id:** ANA-DOC-0126 · **Título:** Applying Diffusion of Innovation Theory to Intervention Development · **Autores:** Dearing JW · **Publicación o institución:** Research on Social Work Practice (SAGE; vía PubMed Central) · **Año:** 2009 · **Tipo de documento:** Artículo revisado por pares (PMC) · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** URL de acceso: https://pmc.ncbi.nlm.nih.gov/articles/PMC2957672/ (PMC deniega clientes automatizados; título y autores verificados por eutils del NCBI) · **Peldaño de la escalera de acceso:** Peldaño 1 (acceso abierto vía PubMed Central) · **Licencia y restricciones:** Disponible en PubMed Central; el portal PMC deniega clientes automatizados · **Versión del documento y su relación:** Versión de registro verificada; versiones alternativas no consultadas en esta carga

*Clasificación y estado.* **Disciplinas:** Bloque temático 2 (Análisis de tendencias y prospectiva) · Subtema 8: Curvas de difusión de innovaciones. difusión de innovaciones; adopción · **Etiquetas:** bloque-2; subtema-8; rogers; intervenciones · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 2 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Artículo en Research on Social Work Practice que aplica la teoría de la difusión de innovaciones al desarrollo de intervenciones, con la correspondencia entre atributos de Rogers y fases de adopción. · **Estatus epistémico y nivel de evidencia:** Evidencia institucional de referencia en prospectiva · **Relevancia para la petición:** Aplicación de la teoría de difusión de Rogers del subtema curvas de difusión a un ciclo de intervención. · **Afirmaciones que podría respaldar:** «La teoría de la difusión de innovaciones se aplica operativamente al diseño de intervenciones».

*Verificación y calidad.* **Resultado del filtro de verificación:** Completa (lote del operador): PMC2957672; título exacto por eutils (Research on Social Work Practice, 2009); PMC deniega clientes automatizados; acceso abierto. Omitidos: lectura del texto completo por el Documentador; métricas de citación. · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Ámbito de trabajo social; traslación de dominio al análisis de adopción tecnológica.


#### ANA-DOC-0127 — Diffusion of Innovation in Technological Platforms

*Identificación y cita.* **source_id:** ANA-DOC-0127 · **Título:** Diffusion of Innovation in Technological Platforms: The Uber Case \* · **Autores:** Wilquer Silvano de Souza Ferreira; Glaucia Maria Vasconcellos Vale; Victor Silva Corrêa · **Publicación o institución:** BAR - Brazilian Administration Review (vía Redalyc) · **Año:** 2022 · **Tipo de documento:** Artículo de revista abierta (portal Redalyc) · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** URL de acceso: https://www.redalyc.org/journal/841/84172397003/html/ · **Peldaño de la escalera de acceso:** Peldaño 1 (portal de revista o agregador de acceso abierto) · **Licencia y restricciones:** Acceso abierto (Redalyc) · **Versión del documento y su relación:** Versión de registro verificada; versiones alternativas no consultadas en esta carga

*Clasificación y estado.* **Disciplinas:** Bloque temático 2 (Análisis de tendencias y prospectiva) · Subtema 8: Curvas de difusión de innovaciones. difusión de innovaciones; adopción · **Etiquetas:** bloque-2; subtema-8; plataformas; caso-de-estudio · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 2 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Estudio de caso en Redalyc sobre la difusión de la innovación en plataformas tecnológicas, tomando Uber como caso de dinámicas de adopción de plataformas. · **Estatus epistémico y nivel de evidencia:** Evidencia institucional de referencia en prospectiva · **Relevancia para la petición:** Caso de plataforma del subtema curvas de difusión: adopción en mercados de plataformas. · **Afirmaciones que podría respaldar:** «La difusión de innovaciones en plataformas digitales cuenta con estudios de caso documentados».

*Verificación y calidad.* **Resultado del filtro de verificación:** Completa (lote del operador): Redalyc HTTP 200; portal abierto; autores por completar. Omitidos: lectura del texto completo por el Documentador; métricas de citación. Nota: Título real completo: 'Diffusion of Innovation in Technological Platforms: The Uber Case' (el lote omitía el caso de estudio); nota de título. · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Caso único (Uber); generalización limitada. Autores por completar en revisión.


#### ANA-DOC-0128 — Technology Readiness Levels (TRL)

*Identificación y cita.* **source_id:** ANA-DOC-0128 · **Título:** Technology Readiness Levels (TRL) · **Autores:** Por completar (metadatos no contrastables por automatización; completar en la revisión de primera petición) · **Publicación o institución:** Comisión Europea (Euraxess) · **Año:** no aplicable (recurso web vigente; consultado el 26/10/2026) · **Tipo de documento:** Guía web institucional (Technology Readiness Levels) · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** URL de acceso: https://euraxess.ec.europa.eu/career-development/researchers/manual-scientific-entrepreneurship/major-steps/trl · **Peldaño de la escalera de acceso:** Peldaño 1 (acceso abierto editorial o documento institucional de distribución pública) · **Licencia y restricciones:** Página institucional abierta de la Comisión Europea · **Versión del documento y su relación:** Versión de registro verificada; versiones alternativas no consultadas en esta carga

*Clasificación y estado.* **Disciplinas:** Bloque temático 2 (Análisis de tendencias y prospectiva) · Subtema 9: Ciclos de madurez industrial. ciclos de vida industrial; madurez tecnológica · **Etiquetas:** bloque-2; subtema-9; trl; comision-europea · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 2 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Guía institucional de la Comisión Europea (Euraxess) sobre los Technology Readiness Levels: definición de los nueve niveles y su uso en financiaciación y gestión de la madurez tecnológica. · **Estatus epistémico y nivel de evidencia:** Evidencia institucional de referencia en prospectiva · **Relevancia para la petición:** Referencia normativa práctica del subtema madurez industrial: la escala TRL de la UE. · **Afirmaciones que podría respaldar:** «La escala TRL es el estándar institucional europeo para graduar la madurez tecnológica».

*Verificación y calidad.* **Resultado del filtro de verificación:** Completa (lote del operador): Página TRL de euraxess (Comisión Europea); HTTP 200; recurso institucional abierto. Omitidos: lectura del texto completo por el Documentador; métricas de citación. · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Guía de aplicación de financiación; no sustituye a la literatura académica de ciclos de industria.


#### ANA-DOC-0129 — Oslo Manual 2018 *

*Identificación y cita.* **source_id:** ANA-DOC-0129 · **Título:** Oslo Manual 2018 \* · **Autores:** OECD; Eurostat · **Publicación o institución:** Organización para la Cooperación y el Desarrollo Económicos / Eurostat · **Año:** 2018 · **Tipo de documento:** Artículo revisado por pares (acceso abierto) · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** DOI: 10.1787/9789264304604-en · Página de la publicación: https://doi.org/10.1787/9789264304604-en (deniega clientes automatizados; DOI resolutivo y metadatos verificados) · **Peldaño de la escalera de acceso:** Peldaño 5 (pendiente de acceso gratuito): metadatos y DOI resolutivos verificados; el portal OCDE deniega clientes automatizados; localizar el peldaño legal en la primera revisión · **Licencia y restricciones:** Bajo control de acceso de la OCDE (pendiente de peldaño legal) · **Versión del documento y su relación:** Versión de registro verificada; versiones alternativas no consultadas en esta carga

*Clasificación y estado.* **Disciplinas:** Bloque temático 2 (Análisis de tendencias y prospectiva) · Subtema 9: Ciclos de madurez industrial. ciclos de vida industrial; madurez tecnológica · **Etiquetas:** bloque-2; subtema-9; norma; ocde; innovacion · **Estado:** Pendiente de acceso gratuito · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 2 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Manual de Oslo (4.ª edición, 2018), estándar OCDE/Eurostat para medir la innovación: definiciones, tipos de innovación y reglas de recogida de datos. Norma de referencia internacional. · **Estatus epistémico y nivel de evidencia:** Evidencia revisada por pares con acceso abierto · **Relevancia para la petición:** Norma estadística del subtema madurez industrial: cómo se mide la innovación de forma comparable. · **Afirmaciones que podría respaldar:** «La medición de la innovación sigue una norma internacional (Manual de Oslo 2018)».

*Verificación y calidad.* **Resultado del filtro de verificación:** Completa en lo verificable (lote del operador): DOI 10.1787/9789264304604-en verificado; OpenAlex OA=False; portal OCDE deniega clientes automatizados; pendiente de peldaño legal. Estado peldaño 5 pendiente de acceso gratuito. Omitidos: lectura del texto completo; métricas de citación. Nota: Título editorial 'Oslo Manual 2018' con subtítulo 'Guidelines for Collecting, Reporting and Using Data on Innovation' (el juez automático marcó NO COINCIDE por el subtítulo; se considera la misma obra). · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Registro pendiente de acceso gratuito: el texto completo está bajo control de acceso de la OCDE.


#### ANA-DOC-0130 — Innovation and firm survival over the industry life cycle

*Identificación y cita.* **source_id:** ANA-DOC-0130 · **Título:** Innovation and firm survival over the industry life cycle · **Autores:** Ann Hipp; Martin Kalthaus · **Publicación o institución:** Small Business Economics, vol. 66, n.º 3, págs. 1233-1262 · **Año:** 2026 · **Tipo de documento:** Artículo revisado por pares (acceso abierto hybrid) · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** DOI: 10.1007/s11187-025-01139-7 · URL de acceso: https://link.springer.com/article/10.1007/s11187-025-01139-7 · **Peldaño de la escalera de acceso:** Peldaño 1 (acceso abierto editorial o documento institucional de distribución pública) · **Licencia y restricciones:** Copyright Springer Nature; acceso abierto (OpenAlex) · **Versión del documento y su relación:** Versión de registro verificada; versiones alternativas no consultadas en esta carga

*Clasificación y estado.* **Disciplinas:** Bloque temático 2 (Análisis de tendencias y prospectiva) · Subtema 9: Ciclos de madurez industrial. ciclos de vida industrial; madurez tecnológica · **Etiquetas:** bloque-2; subtema-9; supervivencia; ciclo-de-vida · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 2 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Artículo en Small Business Economics (2026) que estudia la innovación y la supervivencia empresarial a lo largo del ciclo de vida de la industria, con evidencia longitudinal. · **Estatus epistémico y nivel de evidencia:** Evidencia revisada por pares con acceso abierto · **Relevancia para la petición:** Evidencia académica actualizada del subtema madurez industrial: innovación y supervivencia por fase de ciclo. · **Afirmaciones que podría respaldar:** «La relación entre innovación y supervivencia empresarial varía según la fase del ciclo de vida de la industria».

*Verificación y calidad.* **Resultado del filtro de verificación:** Completa (lote del operador): 10.1007/s11187-025-01139-7; Small Business Economics OA; PDF directo en link.springer.com/content/pdf; contrastado. Omitidos: lectura del texto completo por el Documentador; métricas de citación. · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Muestra y periodo propios del estudio.


#### ANA-DOC-0131 — Industry Life Cycle, CEO Functional Background and Corporate…

*Identificación y cita.* **source_id:** ANA-DOC-0131 · **Título:** Industry Life Cycle, CEO Functional Background and Corporate Sustainable Development: Evidence from Listed Companies in China \* · **Autores:** Yi Feng; Ya Liu · **Publicación o institución:** Sustainability · **Año:** 2023 · **Tipo de documento:** Artículo revisado por pares (acceso abierto) · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** DOI: 10.3390/su15032071 · URL de acceso: https://www.mdpi.com/2071-1050/15/3/2071 · **Peldaño de la escalera de acceso:** Peldaño 1 (acceso abierto editorial o repositorio) · **Licencia y restricciones:** Acceso abierto (MDPI, licencia Creative Commons) · **Versión del documento y su relación:** Versión de registro verificada; versiones alternativas no consultadas en esta carga

*Clasificación y estado.* **Disciplinas:** Bloque temático 2 (Análisis de tendencias y prospectiva) · Subtema 9: Ciclos de madurez industrial. ciclos de vida industrial; madurez tecnológica · **Etiquetas:** bloque-2; subtema-9; ceo; desempeno · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 2 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Artículo en Sustainability que examina ciclo de vida de la industria, formación del consejero delegado y desempeño corporativo (en su dimensión de sostenibilidad). · **Estatus epistémico y nivel de evidencia:** Evidencia revisada por pares con acceso abierto · **Relevancia para la petición:** Referencia del subtema madurez industrial sobre cómo la fase del ciclo moldea el equipo directivo y el desempeño. · **Afirmaciones que podría respaldar:** «La fase del ciclo de vida industrial se asocia al perfil funcional del CEO y al desempeño corporativo».

*Verificación y calidad.* **Resultado del filtro de verificación:** Completa (lote del operador): 10.3390/su15032071; Sustainability (MDPI) oro; contrastado. Omitidos: lectura del texto completo por el Documentador; métricas de citación. Nota: Título real: 'Industry Life Cycle, CEO Functional Background and Corporate Sustainability Performance' (el lote: '...and Firm Performance'); nota de título. · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** El título real difiere del reclamado en su parte final (nota de título).


#### ANA-DOC-0132 — Disruptive innovation from a process view

*Identificación y cita.* **source_id:** ANA-DOC-0132 · **Título:** Disruptive innovation from a process view: A systematic literature review · **Autores:** Neele Petzold; Lina Acevedo Landinez; Thomas Baaken · **Publicación o institución:** Creativity and Innovation Management, vol. 28, n.º 2, págs. 157-174 · **Año:** 2019 · **Tipo de documento:** Artículo revisado por pares (acceso abierto) · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** DOI: 10.1111/caim.12313 · URL de acceso: https://doi.org/10.1111/caim.12313 · **Peldaño de la escalera de acceso:** Peldaño 1 (acceso abierto editorial o repositorio) · **Licencia y restricciones:** Copyright Wiley; acceso abierto (OpenAlex) · **Versión del documento y su relación:** Versión de registro verificada; versiones alternativas no consultadas en esta carga

*Clasificación y estado.* **Disciplinas:** Bloque temático 2 (Análisis de tendencias y prospectiva) · Subtema 10: Análisis de disrupciones. disrupción; innovación · **Etiquetas:** bloque-2; subtema-10; revision-sistematica; disrupcion · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 2 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Revisión sistemática en Creativity and Innovation Management que analiza la innovación disruptiva desde una perspectiva de proceso, ordenando la literatura posterior a Christensen. · **Estatus epistémico y nivel de evidencia:** Evidencia revisada por pares con acceso abierto · **Relevancia para la petición:** Revisión del subtema disrupciones: el proceso disruptivo más allá del caso fundacional. · **Afirmaciones que podría respaldar:** «La innovación disruptiva cuenta con literatura de proceso sistematizada por revisión sistemática».

*Verificación y calidad.* **Resultado del filtro de verificación:** Completa (lote del operador): 10.1111/caim.12313; Creativity and Innovation Management OA (OpenAlex); wiley deniega clientes automatizados. Omitidos: lectura del texto completo por el Documentador; métricas de citación. · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Foco conceptual de gestión; no aporta señales de mercado.


#### ANA-DOC-0133 — Innovation signals

*Identificación y cita.* **source_id:** ANA-DOC-0133 · **Título:** Innovation signals: leveraging machine learning to separate noise from news · **Autores:** Christian Mühlroth; Laura Kölbl; Michael Grottke · **Publicación o institución:** Scientometrics, vol. 128, n.º 5, págs. 2649-2676 · **Año:** 2023 · **Tipo de documento:** Artículo revisado por pares (acceso abierto hybrid) · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** DOI: 10.1007/s11192-023-04672-y · URL de acceso: https://doi.org/10.1007/s11192-023-04672-y · **Peldaño de la escalera de acceso:** Peldaño 1 (acceso abierto editorial o repositorio) · **Licencia y restricciones:** Copyright Springer Nature; acceso abierto (OpenAlex) · **Versión del documento y su relación:** Versión de registro verificada; versiones alternativas no consultadas en esta carga

*Clasificación y estado.* **Disciplinas:** Bloque temático 2 (Análisis de tendencias y prospectiva) · Subtema 10: Análisis de disrupciones. disrupción; innovación · **Etiquetas:** bloque-2; subtema-10; ml; senal-ruido · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 2 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Artículo en Scientometrics que aprovecha aprendizaje automático para separar señal de ruido en flujos de innovación (papers, patentes, noticias), con validación empírica. · **Estatus epistémico y nivel de evidencia:** Evidencia revisada por pares con acceso abierto · **Relevancia para la petición:** Referencia computacional del subtema disrupciones y de la separación señal/ruido de la novedad. · **Afirmaciones que podría respaldar:** «El aprendizaje automático puede separar señales de innovación del ruido informativo, con validación documentada».

*Verificación y calidad.* **Resultado del filtro de verificación:** Completa (lote del operador): 10.1007/s11192-023-04672-y; Scientometrics OA hybrid; contrastado. Omitidos: lectura del texto completo por el Documentador; métricas de citación. · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Método dependiente del corpus y del idioma.


#### ANA-DOC-0134 — Disruptive Technological Innovations as New Opportunities fo…

*Identificación y cita.* **source_id:** ANA-DOC-0134 · **Título:** Disruptive Technological Innovations as New Opportunities for Mature Industrial Clusters. The Case of Digital Printing Innovation \* · **Autores:** Francesc Xavier Molina-Morales; Luís Martínez-Cháfer; David Valiente-Bordanova · **Publicación o institución:** Investigaciones Regionales - Journal of Regional Research (vía Redalyc) · **Año:** 2017 · **Tipo de documento:** Artículo de revista abierta (portal Redalyc) · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** URL de acceso: https://www.redalyc.org/journal/289/28966569003/html/ · **Peldaño de la escalera de acceso:** Peldaño 1 (portal de revista o agregador de acceso abierto) · **Licencia y restricciones:** Acceso abierto (Redalyc) · **Versión del documento y su relación:** Versión de registro verificada; versiones alternativas no consultadas en esta carga

*Clasificación y estado.* **Disciplinas:** Bloque temático 2 (Análisis de tendencias y prospectiva) · Subtema 10: Análisis de disrupciones. disrupción; innovación · **Etiquetas:** bloque-2; subtema-10; incumbentes; caso-de-estudio · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 2 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Estudio en Redalyc sobre innovaciones tecnológicas disruptivas como nuevas oportunidades para conglomerados industriales maduros, con el caso de la innovación en impresión digital. · **Estatus epistémico y nivel de evidencia:** Evidencia institucional de referencia en prospectiva · **Relevancia para la petición:** Caso del subtema disrupciones: cómo la disrupción abre oportunidades a incumbentes maduros. · **Afirmaciones que podría respaldar:** «La disrupción tecnológica puede crear oportunidades para conglomerados industriales maduros, según evidencia de caso».

*Verificación y calidad.* **Resultado del filtro de verificación:** Completa (lote del operador): Redalyc HTTP 200; portal abierto; autores por completar. Omitidos: lectura del texto completo por el Documentador; métricas de citación. Nota: Título real completo: 'Disruptive Technological Innovations as New Opportunities for Mature Industrial Clusters. The Case of Digital Printing Innovation' (el lote lo truncaba); nota de título. · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Caso sectorial (impresión digital). Autores por completar en revisión.


#### ANA-DOC-0135 — Technological disruption and democracy in the twenty-first c…

*Identificación y cita.* **source_id:** ANA-DOC-0135 · **Título:** Technological disruption and democracy in the twenty-first century · **Autores:** Felipe Arocena; Sebastián Sansone; Nicolás Enrique Prada Álvarez · **Publicación o institución:** European Journal of Futures Research, vol. 10, n.º 1 · **Año:** 2022 · **Tipo de documento:** Artículo revisado por pares (revista de acceso abierto) · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** DOI: 10.1186/s40309-022-00189-4 · URL de acceso: https://link.springer.com/article/10.1186/s40309-022-00189-4 · **Peldaño de la escalera de acceso:** Peldaño 1 (acceso abierto editorial o repositorio) · **Licencia y restricciones:** Acceso abierto (SpringerOpen, licencia Creative Commons) · **Versión del documento y su relación:** Versión de registro verificada; versiones alternativas no consultadas en esta carga

*Clasificación y estado.* **Disciplinas:** Bloque temático 2 (Análisis de tendencias y prospectiva) · Subtema 10: Análisis de disrupciones. disrupción; innovación · **Etiquetas:** bloque-2; subtema-10; democracia; disrupcion · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 2 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Artículo en la European Journal of Futures Research que examina la disrupción tecnológica y la democracia en el siglo XXI, con el marco de los estudios de futuro. · **Estatus epistémico y nivel de evidencia:** Evidencia revisada por pares con acceso abierto · **Relevancia para la petición:** Lectura de fondo del subtema disrupciones sobre sus efectos institucionales y políticos. · **Afirmaciones que podría respaldar:** «La disrupción tecnológica tiene efectos institucionales y democráticos documentados en la literatura prospectiva».

*Verificación y calidad.* **Resultado del filtro de verificación:** Completa (lote del operador): 10.1186/s40309-022-00189-4; EJFR oro; título exacto; PDF abierto en springeropen. Omitidos: lectura del texto completo por el Documentador; métricas de citación. · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Ángulo socio-político; distancia con el análisis financiero.


#### ANA-DOC-0136 — What are socially disruptive technologies?

*Identificación y cita.* **source_id:** ANA-DOC-0136 · **Título:** What are socially disruptive technologies? · **Autores:** Jeroen K. G. Hopster · **Publicación o institución:** Technology in Society · **Año:** 2021 · **Tipo de documento:** Artículo revisado por pares (acceso abierto) · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** DOI: 10.1016/j.techsoc.2021.101750 · URL de acceso: https://www.sciencedirect.com/science/article/pii/S0160791X21002256 · **Peldaño de la escalera de acceso:** Peldaño 1 (acceso abierto editorial o repositorio) · **Licencia y restricciones:** Copyright Elsevier; artículo en acceso abierto (OpenAlex) · **Versión del documento y su relación:** Versión de registro verificada; versiones alternativas no consultadas en esta carga

*Clasificación y estado.* **Disciplinas:** Bloque temático 2 (Análisis de tendencias y prospectiva) · Subtema 10: Análisis de disrupciones. disrupción; innovación · **Etiquetas:** bloque-2; subtema-10; disrupcion-social; definicion · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 2 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Artículo en Technology in Society que define qué son las tecnologías socialmente disruptivas, con criterios operativos de disrupción social diferenciados de la disrupción de mercado. · **Estatus epistémico y nivel de evidencia:** Evidencia revisada por pares con acceso abierto · **Relevancia para la petición:** Definición operativa del subtema disrupciones para distinguir disrupción social y de mercado. · **Afirmaciones que podría respaldar:** «La disrupción social de una tecnología admite criterios operativos diferenciados de la disrupción comercial».

*Verificación y calidad.* **Resultado del filtro de verificación:** Completa (lote del operador): PII S0160791X21002256 = 10.1016/j.techsoc.2021.101750; Technology in Society OA; localizado por búsqueda bibliográfica Crossref; sim=1.0. Omitidos: lectura del texto completo por el Documentador; métricas de citación. · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Marco conceptual; aplicación a carteras indirecta.


#### ANA-DOC-0137 — Participatory foresight and reflexive innovation

*Identificación y cita.* **source_id:** ANA-DOC-0137 · **Título:** Participatory foresight and reflexive innovation: setting policy goals and developing strategies in a bottom-up, mission-oriented, sustainable way \* · **Autores:** Aaron B. Rosa; Simone Kimpeler; Elna Schirrmeister; Philine Warnke · **Publicación o institución:** European Journal of Futures Research, vol. 9, n.º 1 · **Año:** 2021 · **Tipo de documento:** Artículo revisado por pares (revista de acceso abierto) · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** DOI: 10.1186/s40309-021-00171-6 · URL de acceso: https://link.springer.com/article/10.1186/s40309-021-00171-6 · **Peldaño de la escalera de acceso:** Peldaño 1 (acceso abierto editorial o repositorio) · **Licencia y restricciones:** Acceso abierto (SpringerOpen, licencia Creative Commons) · **Versión del documento y su relación:** Versión de registro verificada; versiones alternativas no consultadas en esta carga

*Clasificación y estado.* **Disciplinas:** Bloque temático 2 (Análisis de tendencias y prospectiva) · Subtema 11: Análisis de cambios estructurales. cambio estructural; economía del desarrollo · **Etiquetas:** bloque-2; subtema-11; participativo; misiones · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 2 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Artículo en la European Journal of Futures Research sobre foresight participativo e innovación reflexiva para fijar objetivos de política y desarrollar estrategias de cambio estructural de forma ascendente y orientada a misiones. · **Estatus epistémico y nivel de evidencia:** Evidencia revisada por pares con acceso abierto · **Relevancia para la petición:** Referencia del subtema cambios estructurales sobre participacion y misiones en el cambio estructural. · **Afirmaciones que podría respaldar:** «El foresight participativo está documentado como instrumento para orientar el cambio estructural mediante misiones».

*Verificación y calidad.* **Resultado del filtro de verificación:** Completa (lote del operador): 10.1186/s40309-021-00171-6; EJFR oro; contrastado. Omitidos: lectura del texto completo por el Documentador; métricas de citación. Nota: Título real completo: '...setting policy goals and developing strategies in a bottom-up, mission-oriented, sustainable way' (el lote lo truncaba). · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Ámbito de política pública.


#### ANA-DOC-0138 — From shock response to structural change

*Identificación y cita.* **source_id:** ANA-DOC-0138 · **Título:** From shock response to structural change: linking the dimensions of regional resilience \* · **Autores:** Ilona Bartuševičienė; Kristina Matuzevičiūtė; Irma Šileikienė; Greta Mockevičienė; Irmantas Pilypas; Mindaugas Butkus · **Publicación o institución:** Regional Studies Regional Science · **Año:** 2026 · **Tipo de documento:** Artículo revisado por pares (acceso abierto) · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** DOI: 10.1080/21681376.2026.2712167 · URL de acceso: https://www.tandfonline.com/doi/full/10.1080/21681376.2026.2712167 · **Peldaño de la escalera de acceso:** Peldaño 1 (acceso abierto editorial o repositorio) · **Licencia y restricciones:** Copyright Taylor & Francis; acceso abierto (OpenAlex) · **Versión del documento y su relación:** Versión de registro verificada; versiones alternativas no consultadas en esta carga

*Clasificación y estado.* **Disciplinas:** Bloque temático 2 (Análisis de tendencias y prospectiva) · Subtema 11: Análisis de cambios estructurales. cambio estructural; economía del desarrollo · **Etiquetas:** bloque-2; subtema-11; resiliencia; regional · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 2 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Artículo en Regional Studies, Regional Science (2026) que enlaza la respuesta a choques con el cambio estructural, desarrollando las dimensiones de la resiliencia económica regional. · **Estatus epistémico y nivel de evidencia:** Evidencia revisada por pares con acceso abierto · **Relevancia para la petición:** Referencia actualizada del subtema cambios estructurales: resiliencia regional y transformación post-choque. · **Afirmaciones que podría respaldar:** «La respuesta a choques se vincula con el cambio estructural regional a través de dimensiones de resiliencia documentadas».

*Verificación y calidad.* **Resultado del filtro de verificación:** Completa (lote del operador): 10.1080/21681376.2026.2712167; Regional Studies, Regional Science OA (OpenAlex). Omitidos: lectura del texto completo por el Documentador; métricas de citación. Nota: Título real: 'From shock response to structural change: linking the dimensions of resilience...' (el lote: '...regional economic resilience'); nota de título. · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Escalón regional; el título real difiere del reclamado (nota de título).


#### ANA-DOC-0139 — A North-South Model of Structural Change and Growth

*Identificación y cita.* **source_id:** ANA-DOC-0139 · **Título:** A North-South Model of Structural Change and Growth · **Autores:** Por completar (metadatos no contrastables por automatización; completar en la revisión de primera petición) · **Publicación o institución:** Board of Governors of the Federal Reserve System (IFDP n.º 1367) · **Año:** 2022 · **Tipo de documento:** Documento de trabajo institucional (IFDP) · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** URL de acceso: https://www.federalreserve.gov/econres/ifdp/files/ifdp1367.pdf · **Peldaño de la escalera de acceso:** Peldaño 1 (acceso abierto editorial o documento institucional de distribución pública) · **Licencia y restricciones:** Documento de trabajo de la Reserva Federal de distribución pública (PDF directo) · **Versión del documento y su relación:** Versión de registro verificada; versiones alternativas no consultadas en esta carga

*Clasificación y estado.* **Disciplinas:** Bloque temático 2 (Análisis de tendencias y prospectiva) · Subtema 11: Análisis de cambios estructurales. cambio estructural; economía del desarrollo · **Etiquetas:** bloque-2; subtema-11; modelo; norte-sur; fed · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 2 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Documento de trabajo IFDP 1367 de la Reserva Federal (dic. 2022; Aristizabal-Ramirez, Leahy y Tesar) que modeliza el cambio estructural y el crecimiento en un modelo Norte-Sur. · **Estatus epistémico y nivel de evidencia:** Evidencia institucional de referencia en prospectiva · **Relevancia para la petición:** Modelo cuantitativo del subtema cambios estructurales: structural change y crecimiento con asimetrías Norte-Sur. · **Afirmaciones que podría respaldar:** «El cambio estructural y el crecimiento admiten modelización formal en marcos Norte-Sur».

*Verificación y calidad.* **Resultado del filtro de verificación:** Completa (lote del operador): IFDP 1367 (dic. 2022); título exacto contrastado con pdftotext (Aristizabal-Ramirez, Leahy y Tesar); PDF directo federalreserve.gov. Omitidos: lectura del texto completo por el Documentador; métricas de citación. · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Modelo teórico con calibración; supuestos simplificadores.


#### ANA-DOC-0140 — Positive tipping points in a rapidly warming world

*Identificación y cita.* **source_id:** ANA-DOC-0140 · **Título:** Positive tipping points in a rapidly warming world · **Autores:** Joan David Tàbara; Niki Frantzeskaki; Katharina Hölscher; Simona Pedde; Kasper I. Kok; Francesco Lamperti; Jens Hesselbjerg Christensen; Jill Jäger · **Publicación o institución:** Current Opinion in Environmental Sustainability · **Año:** 2018 · **Tipo de documento:** Artículo revisado por pares (acceso abierto) · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** DOI: 10.1016/j.cosust.2018.01.012 · URL de acceso: https://www.sciencedirect.com/science/article/pii/S1877343517300854 · **Peldaño de la escalera de acceso:** Peldaño 1 (acceso abierto editorial o repositorio) · **Licencia y restricciones:** Copyright Elsevier; artículo en acceso abierto (OpenAlex) · **Versión del documento y su relación:** Versión de registro verificada; versiones alternativas no consultadas en esta carga

*Clasificación y estado.* **Disciplinas:** Bloque temático 2 (Análisis de tendencias y prospectiva) · Subtema 12: Detección de puntos de inflexión. puntos de inflexión; sistemas complejos · **Etiquetas:** bloque-2; subtema-12; tipping-points; sostenibilidad · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 2 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Artículo en Current Opinion in Environmental Sustainability sobre los puntos de inflexión positivos en un mundo en calentamiento rápido: condiciones para que sistemas socio-ecológicos basculen hacia estados deseados. · **Estatus epistémico y nivel de evidencia:** Evidencia revisada por pares con acceso abierto · **Relevancia para la petición:** Referencia fundacional reciente del subtema puntos de inflexión (sentido positivo). · **Afirmaciones que podría respaldar:** «Existen puntos de inflexión positivos documentados en sistemas socio-ecológicos».

*Verificación y calidad.* **Resultado del filtro de verificación:** Completa (lote del operador): PII S1877343517300854 = 10.1016/j.cosust.2018.01.012; Current Opinion in Environmental Sustainability OA; sim=1.0 en búsqueda bibliográfica. Omitidos: lectura del texto completo por el Documentador; métricas de citación. · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Dominio climático-ecológico; traslación conceptual al análisis de mercados.


#### ANA-DOC-0141 — Integrating tipping point concepts across diverse systems

*Identificación y cita.* **source_id:** ANA-DOC-0141 · **Título:** Integrating tipping point concepts across diverse systems · **Autores:** Jesse F. Abrams; Laura Maureen Pereira; Viktoria Spaiser; Nico Wunderling; Sebastián Villasante; Joan David Tàbara; Reinette Biggs; David I. Armstrong McKay · **Publicación o institución:** Communications Sustainability · **Año:** 2026 · **Tipo de documento:** Artículo revisado por pares (acceso abierto) · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** DOI: 10.1038/s44458-026-00063-5 · URL de acceso: https://www.nature.com/articles/s44458-026-00063-5 · **Peldaño de la escalera de acceso:** Peldaño 1 (acceso abierto editorial o repositorio) · **Licencia y restricciones:** Copyright Springer Nature; acceso abierto (OpenAlex) · **Versión del documento y su relación:** Versión de registro verificada; versiones alternativas no consultadas en esta carga

*Clasificación y estado.* **Disciplinas:** Bloque temático 2 (Análisis de tendencias y prospectiva) · Subtema 12: Detección de puntos de inflexión. puntos de inflexión; sistemas complejos · **Etiquetas:** bloque-2; subtema-12; integracion; multidominio · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 2 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Artículo en Communications Sustainability (2026) que integra los conceptos de punto de inflexión entre sistemas diversos (clima, ecosistemas, sociedades, economía), con taxonomía comparada. · **Estatus epistémico y nivel de evidencia:** Evidencia revisada por pares con acceso abierto · **Relevancia para la petición:** Referencia integradora del subtema puntos de inflexión: comparación de conceptos entre dominios. · **Afirmaciones que podría respaldar:** «Los conceptos de punto de inflexión admiten integración y comparación entre sistemas diversos».

*Verificación y calidad.* **Resultado del filtro de verificación:** Completa (lote del operador): 10.1038/s44458-026-00063-5; Communications Sustainability (Nature Portfolio) OA; título exacto; PDF abierto. Omitidos: lectura del texto completo por el Documentador; métricas de citación. · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Artículo muy reciente (2026); en consolidación de citación.


#### ANA-DOC-0142 — Tipping positive change

*Identificación y cita.* **source_id:** ANA-DOC-0142 · **Título:** Tipping positive change · **Autores:** Timothy M. Lenton · **Publicación o institución:** Philosophical Transactions of the Royal Society B Biological Sciences · **Año:** 2020 · **Tipo de documento:** Artículo revisado por pares (acceso abierto) · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** DOI: 10.1098/rstb.2019.0123 · URL de acceso: https://royalsocietypublishing.org/rstb/article/375/1794/20190123/30609 · **Peldaño de la escalera de acceso:** Peldaño 2 (copia abierta en PubMed Central, PMC7017777) · **Licencia y restricciones:** Copyright The Royal Society; copia abierta en PubMed Central · **Versión del documento y su relación:** Versión de registro verificada; versiones alternativas no consultadas en esta carga

*Clasificación y estado.* **Disciplinas:** Bloque temático 2 (Análisis de tendencias y prospectiva) · Subtema 12: Detección de puntos de inflexión. puntos de inflexión; sistemas complejos · **Etiquetas:** bloque-2; subtema-12; retroalimentacion; royal-society · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 2 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Número temático de Philosophical Transactions de la Royal Society con el artículo «Tipping positive change»: mecanismos de retroalimentación que pueden acelerar transiciones positivas. · **Estatus epistémico y nivel de evidencia:** Evidencia revisada por pares con acceso abierto · **Relevancia para la petición:** Referencia de alto nivel del subtema puntos de inflexión sobre retroalimentaciones de cambio positivo. · **Afirmaciones que podría respaldar:** «Las retroalimentaciones que aceleran el cambio positivo están documentadas en la literatura de la Royal Society».

*Verificación y calidad.* **Resultado del filtro de verificación:** Completa (lote del operador): 10.1098/rstb.2019.0123; Philosophical Transactions B 2020; OA verde con copia en PMC7017777 (OpenAlex); royalsocietypublishing deniega clientes automatizados. Omitidos: lectura del texto completo por el Documentador; métricas de citación. · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Enfoque socio-ecológico; copia abierta en PMC (peldaño 2).


#### ANA-DOC-0143 — Defining tipping points for social-ecological systems schola…

*Identificación y cita.* **source_id:** ANA-DOC-0143 · **Título:** Defining tipping points for social-ecological systems scholarship—an interdisciplinary literature review · **Autores:** Manjana Milkoreit; Jennifer Hodbod; Jacopo Alessandro Baggio; Karina Benessaiah; Rafael Calderón-Contreras; Jonathan F. Donges; Jean‐Denis Mathias; Juan Rocha · **Publicación o institución:** Environmental Research Letters · **Año:** 2018 · **Tipo de documento:** Artículo revisado por pares (acceso abierto) · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** DOI: 10.1088/1748-9326/aaaa75 · URL de acceso: https://iopscience.iop.org/article/10.1088/1748-9326/aaaa75/pdf · **Peldaño de la escalera de acceso:** Peldaño 1 (acceso abierto editorial o documento institucional de distribución pública) · **Licencia y restricciones:** Copyright IOP Publishing; acceso abierto (OpenAlex) · **Versión del documento y su relación:** Versión de registro verificada; versiones alternativas no consultadas en esta carga

*Clasificación y estado.* **Disciplinas:** Bloque temático 2 (Análisis de tendencias y prospectiva) · Subtema 12: Detección de puntos de inflexión. puntos de inflexión; sistemas complejos · **Etiquetas:** bloque-2; subtema-12; definicion; interdisciplinar · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 2 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Artículo en Environmental Research Letters que define los puntos de inflexión para la beca de sistemas socio-ecológicos, a partir de una revisión interdisciplinar. · **Estatus epistémico y nivel de evidencia:** Evidencia revisada por pares con acceso abierto · **Relevancia para la petición:** Definición operativa del subtema puntos de inflexión: criterios y terminología consensuada. · **Afirmaciones que podría respaldar:** «El concepto de punto de inflexión cuenta con definición operativa consensuada en la literatura interdisciplinar».

*Verificación y calidad.* **Resultado del filtro de verificación:** Completa (lote del operador): 10.1088/1748-9326/aaaa75; Environmental Research Letters 2018; OA con PDF directo en iopscience (HTTP 200); título real con subtítulo 'an interdisciplinary literature review'. Omitidos: lectura del texto completo por el Documentador; métricas de citación. · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Terminología de sistemas socio-ecológicos; adaptar al contexto financiero.


#### ANA-DOC-0144 — Why converging technologies need converging international re…

*Identificación y cita.* **source_id:** ANA-DOC-0144 · **Título:** Why converging technologies need converging international regulation \* · **Autores:** Dirk Helbing; Marcello Ienca · **Publicación o institución:** Ethics and Information Technology, vol. 26, n.º 1 · **Año:** 2024 · **Tipo de documento:** Artículo revisado por pares (acceso abierto hybrid) · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** DOI: 10.1007/s10676-024-09756-8 · URL de acceso: https://link.springer.com/article/10.1007/s10676-024-09756-8 · **Peldaño de la escalera de acceso:** Peldaño 1 (acceso abierto editorial o repositorio) · **Licencia y restricciones:** Copyright Springer Nature; acceso abierto (OpenAlex) · **Versión del documento y su relación:** Versión de registro verificada; versiones alternativas no consultadas en esta carga

*Clasificación y estado.* **Disciplinas:** Bloque temático 2 (Análisis de tendencias y prospectiva) · Subtema 13: Análisis de convergencia tecnológica. convergencia tecnológica; bibliometría · **Etiquetas:** bloque-2; subtema-13; regulacion; nbic · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 2 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Artículo en Ethics and Information Technology que argumenta por qué las tecnologías convergentes exigen regulación internacional convergente, con análisis de gobernanza de NBIC. · **Estatus epistémico y nivel de evidencia:** Evidencia revisada por pares con acceso abierto · **Relevancia para la petición:** Referencia de gobernanza del subtema convergencia tecnológica. · **Afirmaciones que podría respaldar:** «La convergencia tecnológica plantea demandas de regulación internacional convergente, según la literatura».

*Verificación y calidad.* **Resultado del filtro de verificación:** Completa (lote del operador): 10.1007/s10676-024-09756-8; Ethics and Information Technology OA; PDF directo. Omitidos: lectura del texto completo por el Documentador; métricas de citación. Nota: Título real: 'Why converging technologies need converging international regulation' (el lote: '...international governance'); nota de título. · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Foco normativo; el título real dice «regulation», no «governance» (nota de título).


#### ANA-DOC-0145 — Measuring Technological Convergence in Encryption Technologi…

*Identificación y cita.* **source_id:** ANA-DOC-0145 · **Título:** Measuring Technological Convergence in Encryption Technologies with Proximity Indices: A Text Mining and Bibliometric Analysis using OpenAlex \* · **Autores:** Alessandro Tavazzi; Dimitri Percia David; Julian Jang-Jaccard; Alain Mermoud · **Publicación o institución:** Por completar (revisión de primera petición) · **Año:** Por completar (revisión de primera petición) · **Tipo de documento:** Artículo revisado por pares (acceso abierto) · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** DOI: arXiv:2403.01601 · URL de acceso: https://arxiv.org/abs/2403.01601 · **Peldaño de la escalera de acceso:** Peldaño 1 (preprint en arXiv) · **Licencia y restricciones:** Acceso abierto (verificado) · **Versión del documento y su relación:** Versión de registro verificada; versiones alternativas no consultadas en esta carga

*Clasificación y estado.* **Disciplinas:** Bloque temático 2 (Análisis de tendencias y prospectiva) · Subtema 13: Análisis de convergencia tecnológica. convergencia tecnológica; bibliometría · **Etiquetas:** bloque-2; subtema-13; arxiv; proximidad; cifrado · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 2 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Preprint de arXiv que mide la convergencia tecnológica en tecnologías de cifrado mediante índices de proximidad y análisis bibliométrico con OpenAlex (minería de texto). · **Estatus epistémico y nivel de evidencia:** Evidencia revisada por pares con acceso abierto · **Relevancia para la petición:** Referencia métrica del subtema convergencia: índices de proximidad sobre datos bibliométricos. · **Afirmaciones que podría respaldar:** «La convergencia tecnológica admite medición cuantitativa mediante índices de proximidad sobre datos bibliométricos».

*Verificación y calidad.* **Resultado del filtro de verificación:** Completa (lote del operador): arXiv 2403.01601; título contrastado con la API de arXiv; acceso abierto. Omitidos: lectura del texto completo por el Documentador; métricas de citación. Nota: Título real: 'Measuring Technological Convergence in Encryption Technologies with Proximity Indices: A Text Mining and Bibliometric Analysis using OpenAlex' (el lote generalizaba el subtítulo); nota de título. · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Preprint (revisión por pares según el destino final); dominio de cifrado. Título real más específico que el reclamado (nota de título).


#### ANA-DOC-0146 — Research on the Evolution of Textile Technological Convergen…

*Identificación y cita.* **source_id:** ANA-DOC-0146 · **Título:** Research on the Evolution of Textile Technological Convergence · **Autores:** Por completar (metadatos no contrastables por automatización; completar en la revisión de primera petición) · **Publicación o institución:** Por completar (revisión de primera petición) · **Año:** 2022 · **Tipo de documento:** Artículo revisado por pares (acceso abierto) · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** DOI: 10.3390/su13052447 · URL de acceso: https://www.mdpi.com/2071-1050/13/5/2447 · **Peldaño de la escalera de acceso:** Peldaño 1 (acceso abierto editorial o repositorio) · **Licencia y restricciones:** Acceso abierto (MDPI, licencia Creative Commons) · **Versión del documento y su relación:** Versión de registro verificada; versiones alternativas no consultadas en esta carga

*Clasificación y estado.* **Disciplinas:** Bloque temático 2 (Análisis de tendencias y prospectiva) · Subtema 13: Análisis de convergencia tecnológica. convergencia tecnológica; bibliometría · **Etiquetas:** bloque-2; subtema-13; textil; patentes · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 2 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Artículo en Sustainability sobre la evolución de la convergencia tecnológica en el sector textil, con análisis de patentes y literatura. · **Estatus epistémico y nivel de evidencia:** Evidencia revisada por pares con acceso abierto · **Relevancia para la petición:** Caso sectorial del subtema convergencia tecnológica (textil). · **Afirmaciones que podría respaldar:** «La convergencia tecnológica está documentada en industrias tradicionales como la textil».

*Verificación y calidad.* **Resultado del filtro de verificación:** Completa (lote del operador): 10.3390/su13052447; Sustainability (MDPI) oro; contrastado. Omitidos: lectura del texto completo por el Documentador; métricas de citación. · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Caso sectorial concreto.


#### ANA-DOC-0147 — Empirical Analysis of Technological Convergence in the Europ…

*Identificación y cita.* **source_id:** ANA-DOC-0147 · **Título:** Empirical Analysis of Technological Convergence in the European Regional Area · **Autores:** Tomasz Kijek; Arkadiusz Kijek; Anna Matras-Bolibok · **Publicación o institución:** SpringerBriefs in regional science · **Año:** 2023 · **Tipo de documento:** Capítulo de libro (SpringerBriefs, acceso abierto) · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** DOI: 10.1007/978-3-031-24531-2_4 · URL de acceso: https://link.springer.com/chapter/10.1007/978-3-031-24531-2_4 · **Peldaño de la escalera de acceso:** Peldaño 1 (acceso abierto editorial o documento institucional de distribución pública) · **Licencia y restricciones:** Copyright Springer Nature; acceso abierto (OpenAlex) · **Versión del documento y su relación:** Versión de registro verificada; versiones alternativas no consultadas en esta carga

*Clasificación y estado.* **Disciplinas:** Bloque temático 2 (Análisis de tendencias y prospectiva) · Subtema 13: Análisis de convergencia tecnológica. convergencia tecnológica; bibliometría · **Etiquetas:** bloque-2; subtema-13; europa; regional; empirico · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 2 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Capítulo en SpringerBriefs in Regional Science (2023) con análisis empírico de la convergencia tecnológica en el espacio regional europeo. · **Estatus epistémico y nivel de evidencia:** Evidencia revisada por pares con acceso abierto · **Relevancia para la petición:** Evidencia empírica regional del subtema convergencia tecnológica (UE). · **Afirmaciones que podría respaldar:** «La convergencia tecnológica muestra patrones empíricos medibles en las regiones europeas».

*Verificación y calidad.* **Resultado del filtro de verificación:** Completa (lote del operador): 10.1007/978-3-031-24531-2_4; SpringerBriefs in Regional Science 2023; OA con PDF directo en link.springer.com/content/pdf; contrastado. Omitidos: lectura del texto completo por el Documentador; métricas de citación. · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Capítulo de breve; alcance regional.


#### ANA-DOC-0148 — The Future of Customs in the EU 2040 *

*Identificación y cita.* **source_id:** ANA-DOC-0148 · **Título:** The Future of Customs in the EU 2040 \* · **Autores:** Por completar (metadatos no contrastables por automatización; completar en la revisión de primera petición) · **Publicación o institución:** Joint Research Centre (Comisión Europea) · **Año:** Por completar (revisión de primera petición) · **Tipo de documento:** Informe institucional prospectivo (JRC) · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** URL de acceso: https://publications.jrc.ec.europa.eu/repository/bitstream/JRC121859/the_future_of_customs_in_the_eu_2040_report_final2_online_1.pdf · **Peldaño de la escalera de acceso:** Peldaño 1 (acceso abierto editorial o documento institucional de distribución pública) · **Licencia y restricciones:** Documento institucional de distribución pública (PDF directo del JRC) · **Versión del documento y su relación:** Versión de registro verificada; versiones alternativas no consultadas en esta carga

*Clasificación y estado.* **Disciplinas:** Bloque temático 2 (Análisis de tendencias y prospectiva) · Subtema 14: Análisis de escenarios futuros. escenarios; planificación prospectiva · **Etiquetas:** bloque-2; subtema-14; jrc; escenarios; aduana · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 2 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Informe del JRC (2021) «The Future of Customs in the EU 2040»: escenarios prospectivos sobre el futuro de la unión aduanera europea, con metodología de escenarios completa. · **Estatus epistémico y nivel de evidencia:** Evidencia institucional de referencia en prospectiva · **Relevancia para la petición:** Ejemplo institucional completo del subtema escenarios futuros: marco, construcción y uso de escenarios. · **Afirmaciones que podría respaldar:** «La UE construye escenarios formales a horizonte 2040 para políticas específicas (aduana)».

*Verificación y calidad.* **Resultado del filtro de verificación:** Completa (lote del operador): PDF directo JRC121859 (200, %PDF); título contrastado con pdftotext ('The Future of Customs in the EU 2040'). Omitidos: lectura del texto completo por el Documentador; métricas de citación. Nota: El lote lo listaba en los subtemas 1, 4 y 14; clasificado por contenido (escenarios prospectivos de la UE). · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Dominio aduanero; el lote lo listaba en tres subtemas distintos (nota de clasificación).


#### ANA-DOC-0149 — The Futures Toolkit

*Identificación y cita.* **source_id:** ANA-DOC-0149 · **Título:** The Futures Toolkit: Tools for Futures Thinking and Foresight Across UK Government · **Autores:** Por completar (metadatos no contrastables por automatización; completar en la revisión de primera petición) · **Publicación o institución:** Gobierno del Reino Unido (GOV.UK) · **Año:** Por completar (revisión de primera petición) · **Tipo de documento:** Caja de herramientas institucional (The Futures Toolkit) · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** URL de acceso: https://www.gov.uk/government/publications/futures-toolkit-for-policy-makers-and-analysts · **Peldaño de la escalera de acceso:** Peldaño 1 (acceso abierto editorial o documento institucional de distribución pública) · **Licencia y restricciones:** Documento público del Gobierno del Reino Unido (Open Government Licence) · **Versión del documento y su relación:** Versión de registro verificada; versiones alternativas no consultadas en esta carga

*Clasificación y estado.* **Disciplinas:** Bloque temático 2 (Análisis de tendencias y prospectiva) · Subtema 14: Análisis de escenarios futuros. escenarios; planificación prospectiva · **Etiquetas:** bloque-2; subtema-14; herramientas; reino-unido · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 2 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Futures Toolkit del Gobierno del Reino Unido: colección de herramientas de pensamiento de futuro y prospectiva para responsables políticos y analistas, con fichas de método y casos. · **Estatus epistémico y nivel de evidencia:** Evidencia institucional de referencia en prospectiva · **Relevancia para la petición:** Caja de herramientas institucional del subtema escenarios futuros: métodos paso a paso. · **Afirmaciones que podría respaldar:** «Los gobiernos disponen de cajas de herramientas prospectivas públicas y estructuradas (Reino Unido)».

*Verificación y calidad.* **Resultado del filtro de verificación:** Completa (lote del operador): Página oficial de la publicación en gov.uk; HTTP 200; herramienta del Gobierno del Reino Unido de acceso abierto (duplicada P1#24 = P1#64). Omitidos: lectura del texto completo por el Documentador; métricas de citación. · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Herramientas de política; adaptar formatos al ciclo del Analizador.


#### ANA-DOC-0150 — Scenarios in the strategy process

*Identificación y cita.* **source_id:** ANA-DOC-0150 · **Título:** Scenarios in the strategy process: a framework of affordances and constraints \* · **Autores:** Victor Tiberius · **Publicación o institución:** European Journal of Futures Research, vol. 7, n.º 1 · **Año:** 2019 · **Tipo de documento:** Artículo revisado por pares (revista de acceso abierto) · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** DOI: 10.1186/s40309-019-0160-5 · URL de acceso: https://doi.org/10.1186/s40309-019-0160-5 · **Peldaño de la escalera de acceso:** Peldaño 1 (acceso abierto editorial o repositorio) · **Licencia y restricciones:** Acceso abierto (SpringerOpen, licencia Creative Commons) · **Versión del documento y su relación:** Versión de registro verificada; versiones alternativas no consultadas en esta carga

*Clasificación y estado.* **Disciplinas:** Bloque temático 2 (Análisis de tendencias y prospectiva) · Subtema 14: Análisis de escenarios futuros. escenarios; planificación prospectiva · **Etiquetas:** bloque-2; subtema-14; metodos; estrategia · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 2 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Artículo en la European Journal of Futures Research que analiza los escenarios en el proceso estratégico con un marco de affordances y restricciones de los métodos de escenarios. · **Estatus epistémico y nivel de evidencia:** Evidencia revisada por pares con acceso abierto · **Relevancia para la petición:** Marco del subtema escenarios sobre qué habilita y limita cada método de escenarios. · **Afirmaciones que podría respaldar:** «Los métodos de escenarios presentan affordances y restricciones sistematizables en el proceso estratégico».

*Verificación y calidad.* **Resultado del filtro de verificación:** Completa (lote del operador): 10.1186/s40309-019-0160-5; EJFR oro; contrastado (duplicada P1#44 = P1#61). Omitidos: lectura del texto completo por el Documentador; métricas de citación. Nota: El lote lo listaba también en disrupciones (P1#44); clasificado por contenido (escenarios). · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Marco conceptual; el lote lo listaba también en disrupciones (nota de clasificación).


#### ANA-DOC-0151 — A systematic review of foresight methods used in the formula…

*Identificación y cita.* **source_id:** ANA-DOC-0151 · **Título:** A systematic review of foresight methods used in the formulation of futures scenarios: evidence from articles indexed in scopus and web of science (2014–2023) · **Autores:** Pedro León Cruz Aguilar; Javier Enrique Medina Vásquez; Olga Patricia Marín Arroyave · **Publicación o institución:** European Journal of Futures Research, vol. 14, n.º 1 · **Año:** 2026 · **Tipo de documento:** Artículo revisado por pares (revista de acceso abierto) · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** DOI: 10.1186/s40309-026-00298-4 · URL de acceso: https://doi.org/10.1186/s40309-026-00298-4 · **Peldaño de la escalera de acceso:** Peldaño 1 (acceso abierto editorial o repositorio) · **Licencia y restricciones:** Acceso abierto (SpringerOpen, licencia Creative Commons) · **Versión del documento y su relación:** Versión de registro verificada; versiones alternativas no consultadas en esta carga

*Clasificación y estado.* **Disciplinas:** Bloque temático 2 (Análisis de tendencias y prospectiva) · Subtema 14: Análisis de escenarios futuros. escenarios; planificación prospectiva · **Etiquetas:** bloque-2; subtema-14; revision-sistematica; metodos · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 2 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Revisión sistemática (2026) en la European Journal of Futures Research de los métodos de foresight empleados en la formulación de escenarios de futuro. · **Estatus epistémico y nivel de evidencia:** Evidencia revisada por pares con acceso abierto · **Relevancia para la petición:** Revisión de referencia del subtema escenarios: qué métodos se usan y con qué calidad. · **Afirmaciones que podría respaldar:** «Los métodos de formulación de escenarios están sistematizados por revisión sistemática de la literatura».

*Verificación y calidad.* **Resultado del filtro de verificación:** Completa (lote del operador): 10.1186/s40309-026-00298-4; EJFR oro 2026; contrastado; OA de la revista SpringerOpen (duplicada P1#46 = P1#60). Omitidos: lectura del texto completo por el Documentador; métricas de citación. · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Artículo muy reciente; en consolidación de citación.


#### ANA-DOC-0152 — Foresight Toolkit for Resilient Public Policy

*Identificación y cita.* **source_id:** ANA-DOC-0152 · **Título:** Foresight Toolkit for Resilient Public Policy · **Autores:** OECD · **Publicación o institución:** Organización para la Cooperación y el Desarrollo Económicos (OCDE, iLibrary) · **Año:** 2025 · **Tipo de documento:** Artículo revisado por pares (acceso abierto) · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** DOI: 10.1787/bcdd9304-en · Página de la publicación: https://www.oecd.org/en/publications/foresight-toolkit-for-resilient-public-policy_bcdd9304-en.html (deniega clientes automatizados; DOI resolutivo y metadatos verificados) · **Peldaño de la escalera de acceso:** Peldaño 5 (pendiente de acceso gratuito): metadatos y DOI resolutivos verificados; el portal OCDE deniega clientes automatizados; localizar el peldaño legal en la primera revisión · **Licencia y restricciones:** Bajo control de acceso de la OCDE (pendiente de peldaño legal) · **Versión del documento y su relación:** Versión de registro verificada; versiones alternativas no consultadas en esta carga

*Clasificación y estado.* **Disciplinas:** Bloque temático 2 (Análisis de tendencias y prospectiva) · Subtema 14: Análisis de escenarios futuros. escenarios; planificación prospectiva · **Etiquetas:** bloque-2; subtema-14; herramientas; ocde; resiliencia · **Estado:** Pendiente de acceso gratuito · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 2 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Toolkit de la OCDE (2025) para política pública resiliente: herramientas de prospectiva estratégica aplicadas a la resiliencia de políticas públicas. · **Estatus epistémico y nivel de evidencia:** Evidencia revisada por pares con acceso abierto · **Relevancia para la petición:** Caja de herramientas OCDE del subtema escenarios futuros. · **Afirmaciones que podría respaldar:** «La OCDE publica toolkits de prospectiva estratégica para política pública resiliente».

*Verificación y calidad.* **Resultado del filtro de verificación:** Completa en lo verificable (lote del operador): DOI 10.1787/bcdd9304-en verificado (2025); OpenAlex OA=False; oecd-ilibrary deniega clientes automatizados; pendiente de peldaño legal; distinta de la Futures Toolkit del Reino Unido. Estado peldaño 5 pendiente de acceso gratuito. Omitidos: lectura del texto completo; métricas de citación. · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Registro pendiente de acceso gratuito: oecd-ilibrary deniega clientes automatizados; distinta de la Futures Toolkit del Reino Unido.


#### ANA-DOC-0153 — Sharpening the Tools of Foresight Analysis and Scenario Plan…

*Identificación y cita.* **source_id:** ANA-DOC-0153 · **Título:** Sharpening the Tools of Foresight Analysis and Scenario Planning Through Engagement With Critical Security Studies \* · **Autores:** Michael P.A. Murphy; Andrew Heffernan · **Publicación o institución:** Alternatives Global Local Political · **Año:** 2026 · **Tipo de documento:** Artículo revisado por pares (acceso abierto) · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** DOI: 10.1177/03043754261435074 · URL de acceso: https://journals.sagepub.com/doi/10.1177/03043754261435074 · **Peldaño de la escalera de acceso:** Peldaño 1 (acceso abierto editorial o repositorio) · **Licencia y restricciones:** Copyright SAGE; acceso abierto (OpenAlex) · **Versión del documento y su relación:** Versión de registro verificada; versiones alternativas no consultadas en esta carga

*Clasificación y estado.* **Disciplinas:** Bloque temático 2 (Análisis de tendencias y prospectiva) · Subtema 14: Análisis de escenarios futuros. escenarios; planificación prospectiva · **Etiquetas:** bloque-2; subtema-14; critica; seguridad · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 2 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Artículo en Alternatives: Global, Local, Political (2026) que afina las herramientas de análisis de prospectiva y planificación por escenarios mediante su diálogo con los estudios críticos de seguridad. · **Estatus epistémico y nivel de evidencia:** Evidencia revisada por pares con acceso abierto · **Relevancia para la petición:** Referencia crítica del subtema escenarios sobre límites y supuestos de las herramientas. · **Afirmaciones que podría respaldar:** «Las herramientas de planificación por escenarios se benefician del escrutinio crítico de sus supuestos».

*Verificación y calidad.* **Resultado del filtro de verificación:** Completa (lote del operador): 10.1177/03043754261435074; Alternatives: Global, Local, Political 2026; OA (OpenAlex); sagepub deniega clientes automatizados. Omitidos: lectura del texto completo por el Documentador; métricas de citación. Nota: Título real: 'Sharpening the Tools of Foresight Analysis and Scenario Planning Through Engagement With Critical Security Studies' (el lote omitía el complemento final); nota de título. · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Ángulo de estudios de seguridad; el título real incluye el complemento final (nota de título).


#### ANA-DOC-0154 — Strategic Foresight and Barriers

*Identificación y cita.* **source_id:** ANA-DOC-0154 · **Título:** Strategic Foresight and Barriers: The Application of Scenario Planning in SMEs · **Autores:** Por completar (metadatos no contrastables por automatización; completar en la revisión de primera petición) · **Publicación o institución:** Journal of Futures Studies · **Año:** 2024 · **Tipo de documento:** Artículo de revista abierta (sin registro Crossref) · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** URL de acceso: https://jfsdigital.org/articles-and-essays/2024-2/vol-29-no-2-december-2024/strategic-foresight-and-barriers-the-application-of-scenario-planning-in-smes/ · **Peldaño de la escalera de acceso:** Peldaño 1 (portal de revista o agregador de acceso abierto) · **Licencia y restricciones:** Acceso abierto (Journal of Futures Studies) · **Versión del documento y su relación:** Versión de registro verificada; versiones alternativas no consultadas en esta carga

*Clasificación y estado.* **Disciplinas:** Bloque temático 2 (Análisis de tendencias y prospectiva) · Subtema 14: Análisis de escenarios futuros. escenarios; planificación prospectiva · **Etiquetas:** bloque-2; subtema-14; pymes; barreras · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 2 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Artículo en la Journal of Futures Studies (2024) sobre las barreras de la prospectiva estratégica y la aplicación de la planificación por escenarios en pymes. · **Estatus epistémico y nivel de evidencia:** Evidencia institucional de referencia en prospectiva · **Relevancia para la petición:** Evidencia del subtema escenarios en pymes: barreras prácticas de adopción. · **Afirmaciones que podría respaldar:** «La adopción de planificación por escenarios en pymes enfrenta barreras documentadas».

*Verificación y calidad.* **Resultado del filtro de verificación:** Completa (lote del operador): jfsdigital.org HTTP 200; título exacto; revista abierta; autores por completar. Omitidos: lectura del texto completo por el Documentador; métricas de citación. · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Pymes; revista abierta sin registro Crossref. Autores por completar en revisión.


#### ANA-DOC-0155 — Scenario planning

*Identificación y cita.* **source_id:** ANA-DOC-0155 · **Título:** Scenario planning: Reflecting on cases of actionable knowledge · **Autores:** John Oliver · **Publicación o institución:** Foresight Science (Wiley) · **Año:** 2023 · **Tipo de documento:** Artículo revisado por pares (copia de repositorio) · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** URL de acceso: https://eprints.bournemouth.ac.uk/38771/7/Futures%20%20%20Foresight%20Science%20-%202023%20-%20Oliver%20-%20Scenario%20planning%20%20Reflecting%20on%20cases%20of%20actionable%20knowledge.pdf · **Peldaño de la escalera de acceso:** Peldaño 2 (copia en repositorio institucional abierto) · **Licencia y restricciones:** Copyright Wiley; copia en repositorio institucional abierto (Bournemouth) citada como acceso de lectura · **Versión del documento y su relación:** Versión de registro verificada; versiones alternativas no consultadas en esta carga

*Clasificación y estado.* **Disciplinas:** Bloque temático 2 (Análisis de tendencias y prospectiva) · Subtema 14: Análisis de escenarios futuros. escenarios; planificación prospectiva · **Etiquetas:** bloque-2; subtema-14; accionable; casos · **Estado:** Aprobada · **Fecha de registro:** 2026-10-26 · **request_id y run_id de origen:** Lote de fuentes del operador — bloque temático 2 (26/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Artículo «Scenario planning: Reflecting on cases of actionable knowledge» (Foresight Science, 2023) que reflexiona sobre casos de conocimiento accionable derivado de la planificación por escenarios. · **Estatus epistémico y nivel de evidencia:** Evidencia institucional de referencia en prospectiva · **Relevancia para la petición:** Referencia del subtema escenarios sobre el paso de escenario a acción. · **Afirmaciones que podría respaldar:** «La planificación por escenarios genera conocimiento accionable documentado en casos analizados».

*Verificación y calidad.* **Resultado del filtro de verificación:** Completa (lote del operador): Repositorio eprints.bournemouth.ac.uk; PDF directo; título contrastado con pdftotext (Foresight Science, DOI 10.1002/ffo2.164). Omitidos: lectura del texto completo por el Documentador; métricas de citación. · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Métricas de citación, si se consultaron:** No consultadas en esta carga · **Limitaciones:** Artículo de reflexión; copia del repositorio de Bournemouth (peldaño 1).


### 4.3 Índice temático y mapa de coberturas

| Ámbito | Fuentes disponibles | Cobertura | Última revisión | Carencias detectadas | Prioridades propuestas |
|---|---|---|---|---|---|
| Momentum cruzado y relativo | ANA-DOC-0001, 0003, 0008, 0011 | Parcial | 2026-10-25 | Falta literatura de consolidación post-2010 y de mercados emergentes | Alta de una revisión sistemática del momentum |
| Momentum temporal y trend-following | ANA-DOC-0002, 0004, 0009, 0012 | Buena | 2026-10-25 | Falta literatura sobre costes y capacidad de las estrategias | Alta de un estudio de implementación y costes |
| Análisis técnico y reglas de negociación | ANA-DOC-0005, 0006, 0007, 0010 | Parcial | 2026-10-25 | Dos de las cuatro fichas pendientes de acceso gratuito (0005, 0007) | Resolver el acceso legal de las pendientes |
| Fundamentos estadísticos y salvaguardas | ANA-DOC-0006, 0007 | Parcial | 2026-10-25 | Falta literatura sobre sesgos de selección y múltiple contraste | Alta de una referencia sobre corrección por múltiple contraste |

| Bloque 1 · Subtema 1: Macroeconomía | ANA-DOC-0013 a ANA-DOC-0017 (5) | Nueva (lote del operador, 26/10/2026) | 2026-10-26 | Sin uso en operación; absorción en la revisión de primera petición | Verificación de autores/años pendientes en 10 fichas |
| Bloque 1 · Subtema 2: Microeconomía | ANA-DOC-0018 a ANA-DOC-0022 (5) | Nueva (lote del operador, 26/10/2026) | 2026-10-26 | Sin uso en operación; absorción en la revisión de primera petición | Verificación de autores/años pendientes en 10 fichas |
| Bloque 1 · Subtema 3: Economía internacional | ANA-DOC-0023 a ANA-DOC-0029 (7) | Nueva (lote del operador, 26/10/2026) | 2026-10-26 | Sin uso en operación; absorción en la revisión de primera petición | Verificación de autores/años pendientes en 10 fichas |
| Bloque 1 · Subtema 4: Economía monetaria | ANA-DOC-0030 a ANA-DOC-0033 (4) | Nueva (lote del operador, 26/10/2026) | 2026-10-26 | Sin uso en operación; absorción en la revisión de primera petición | Verificación de autores/años pendientes en 10 fichas |
| Bloque 1 · Subtema 5: Economía fiscal | ANA-DOC-0034 a ANA-DOC-0039 (6) | Nueva (lote del operador, 26/10/2026) | 2026-10-26 | Sin uso en operación; absorción en la revisión de primera petición | Verificación de autores/años pendientes en 10 fichas |
| Bloque 1 · Subtema 6: Ciclos económicos | ANA-DOC-0040 a ANA-DOC-0046 (7) | Nueva (lote del operador, 26/10/2026) | 2026-10-26 | Sin uso en operación; absorción en la revisión de primera petición | Verificación de autores/años pendientes en 10 fichas |
| Bloque 1 · Subtema 7: Inflación y tipos de interés | ANA-DOC-0047 a ANA-DOC-0055 (9) | Nueva (lote del operador, 26/10/2026) | 2026-10-26 | Sin uso en operación; absorción en la revisión de primera petición | Verificación de autores/años pendientes en 10 fichas |
| Bloque 1 · Subtema 8: Comercio internacional | ANA-DOC-0056 a ANA-DOC-0058 (3) | Nueva (lote del operador, 26/10/2026) | 2026-10-26 | Sin uso en operación; absorción en la revisión de primera petición | Verificación de autores/años pendientes en 10 fichas |
| Bloque 1 · Subtema 9: Productividad y crecimiento económico | ANA-DOC-0059 a ANA-DOC-0066 (8) | Nueva (lote del operador, 26/10/2026) | 2026-10-26 | Sin uso en operación; absorción en la revisión de primera petición | Verificación de autores/años pendientes en 10 fichas |
| Bloque 1 · Subtema 10: Demografía y cambios estructurales | ANA-DOC-0067 a ANA-DOC-0071 (5) | Nueva (lote del operador, 26/10/2026) | 2026-10-26 | Sin uso en operación; absorción en la revisión de primera petición | Verificación de autores/años pendientes en 10 fichas |
| Bloque 1 · Subtema 11: Indicadores adelantados y coincidentes | ANA-DOC-0072 a ANA-DOC-0077 (6) | Nueva (lote del operador, 26/10/2026) | 2026-10-26 | Sin uso en operación; absorción en la revisión de primera petición | Verificación de autores/años pendientes en 10 fichas |
| Bloque 1 · Subtema 12: Políticas económicas y monetarias | ANA-DOC-0078 a ANA-DOC-0083 (6) | Nueva (lote del operador, 26/10/2026) | 2026-10-26 | Sin uso en operación; absorción en la revisión de primera petición | Verificación de autores/años pendientes en 10 fichas |
| Bloque 1 · Subtema 13: Crisis económicas y financieras | ANA-DOC-0084 a ANA-DOC-0087 (4) | Nueva (lote del operador, 26/10/2026) | 2026-10-26 | Sin uso en operación; absorción en la revisión de primera petición | Verificación de autores/años pendientes en 10 fichas |
| Bloque 1 · Subtema T: Transversal: métodos, datos y normas (aporte del lote; bloques 12, 15 y 17 del operador) | ANA-DOC-0088 a ANA-DOC-0091 (4) | Nueva (lote del operador, 26/10/2026) | 2026-10-26 | Sin uso en operación; absorción en la revisión de primera petición | Verificación de autores/años pendientes en 10 fichas |
| Bloque 1 · Canales institucionales por subtema | 63 canales (tabla siguiente) | Nueva (lote del operador, 26/10/2026) | 2026-10-26 | Los portales del FMI deniegan clientes automatizados | Confirmar vigencia en los ciclos de mantenimiento |
| Bloque 2 · Subtema 1: Análisis de tendencias | ANA-DOC-0092 a ANA-DOC-0094 (3) (1 pendiente de acceso gratuito) | Nueva (lote del operador, 26/10/2026) | 2026-10-26 | Sin uso en operación; absorción en la revisión de primera petición | Autores/años por completar donde proceda; portales OCDE con control de acceso |
| Bloque 2 · Subtema 2: Prospectiva estratégica | ANA-DOC-0095 a ANA-DOC-0101 (7) (1 pendiente de acceso gratuito) | Nueva (lote del operador, 26/10/2026) | 2026-10-26 | Sin uso en operación; absorción en la revisión de primera petición | Autores/años por completar donde proceda; portales OCDE con control de acceso |
| Bloque 2 · Subtema 3: Estudios de futuro | ANA-DOC-0102 a ANA-DOC-0107 (6) | Nueva (lote del operador, 26/10/2026) | 2026-10-26 | Sin uso en operación; absorción en la revisión de primera petición | Autores/años por completar donde proceda; portales OCDE con control de acceso |
| Bloque 2 · Subtema 4: Detección de señales tempranas | ANA-DOC-0108 a ANA-DOC-0113 (6) | Nueva (lote del operador, 26/10/2026) | 2026-10-26 | Sin uso en operación; absorción en la revisión de primera petición | Autores/años por completar donde proceda; portales OCDE con control de acceso |
| Bloque 2 · Subtema 5: Identificación de tendencias emergentes | ANA-DOC-0114 a ANA-DOC-0117 (4) | Nueva (lote del operador, 26/10/2026) | 2026-10-26 | Sin uso en operación; absorción en la revisión de primera petición | Autores/años por completar donde proceda; portales OCDE con control de acceso |
| Bloque 2 · Subtema 6: Análisis de megatendencias | ANA-DOC-0118 a ANA-DOC-0122 (5) | Nueva (lote del operador, 26/10/2026) | 2026-10-26 | Sin uso en operación; absorción en la revisión de primera petición | Autores/años por completar donde proceda; portales OCDE con control de acceso |
| Bloque 2 · Subtema 7: Ciclos de adopción tecnológica | ANA-DOC-0123 (1) | Nueva (lote del operador, 26/10/2026) | 2026-10-26 | Sin uso en operación; absorción en la revisión de primera petición | Autores/años por completar donde proceda; portales OCDE con control de acceso |
| Bloque 2 · Subtema 8: Curvas de difusión de innovaciones | ANA-DOC-0124 a ANA-DOC-0127 (4) (1 pendiente de acceso gratuito) | Nueva (lote del operador, 26/10/2026) | 2026-10-26 | Sin uso en operación; absorción en la revisión de primera petición | Autores/años por completar donde proceda; portales OCDE con control de acceso |
| Bloque 2 · Subtema 9: Ciclos de madurez industrial | ANA-DOC-0128 a ANA-DOC-0131 (4) (1 pendiente de acceso gratuito) | Nueva (lote del operador, 26/10/2026) | 2026-10-26 | Sin uso en operación; absorción en la revisión de primera petición | Autores/años por completar donde proceda; portales OCDE con control de acceso |
| Bloque 2 · Subtema 10: Análisis de disrupciones | ANA-DOC-0132 a ANA-DOC-0136 (5) | Nueva (lote del operador, 26/10/2026) | 2026-10-26 | Sin uso en operación; absorción en la revisión de primera petición | Autores/años por completar donde proceda; portales OCDE con control de acceso |
| Bloque 2 · Subtema 11: Análisis de cambios estructurales | ANA-DOC-0137 a ANA-DOC-0139 (3) | Nueva (lote del operador, 26/10/2026) | 2026-10-26 | Sin uso en operación; absorción en la revisión de primera petición | Autores/años por completar donde proceda; portales OCDE con control de acceso |
| Bloque 2 · Subtema 12: Detección de puntos de inflexión | ANA-DOC-0140 a ANA-DOC-0143 (4) | Nueva (lote del operador, 26/10/2026) | 2026-10-26 | Sin uso en operación; absorción en la revisión de primera petición | Autores/años por completar donde proceda; portales OCDE con control de acceso |
| Bloque 2 · Subtema 13: Análisis de convergencia tecnológica | ANA-DOC-0144 a ANA-DOC-0147 (4) | Nueva (lote del operador, 26/10/2026) | 2026-10-26 | Sin uso en operación; absorción en la revisión de primera petición | Autores/años por completar donde proceda; portales OCDE con control de acceso |
| Bloque 2 · Subtema 14: Análisis de escenarios futuros | ANA-DOC-0148 a ANA-DOC-0155 (8) (1 pendiente de acceso gratuito) | Nueva (lote del operador, 26/10/2026) | 2026-10-26 | Sin uso en operación; absorción en la revisión de primera petición | Autores/años por completar donde proceda; portales OCDE con control de acceso |
| Bloque 2 · Canales institucionales por subtema | 17 canales (tabla siguiente) | Nueva (lote del operador, 26/10/2026) | 2026-10-26 | Los portales OCDE, WEF y UNEP deniegan clientes automatizados | Confirmar vigencia en los ciclos de mantenimiento |


#### Canales institucionales del lote del operador, por subtema (26/10/2026)

El lote del operador incluía también una lista de canales institucionales por subtema (63 entradas tras desduplicar 10: ocho con URL genérica que no corresponde al recurso titulado, una revista por suscripción excluida por la regla de acceso y una obra ya registrada como ficha con URL de portada errónea). Cada canal se comprobó el 26/10/2026; los portales del FMI deniegan clientes automatizados y se confirman por índice de búsqueda con acceso abierto por política editorial. Los canales que remiten a obras ya registradas como fichas se marcan para no duplicar.

| Subtema | Canal | URL | Verificación (26/10/2026) |
|---|---|---|---|
| 1 | Principles of Macroeconomics 3e (OpenStax) | https://openstax.org/details/books/principles-macroeconomics-3e/ | Obra ya registrada como ficha ANA-DOC-0013; no se duplica |
| 1 | The Economy 2.0: Macroeconomics (CORE Econ) | https://books.core-econ.org/the-economy/macroeconomics/ | Obra ya registrada como ficha ANA-DOC-0014; no se duplica |
| 1 | The Economy 1.0 (CORE Econ) | https://www.core-econ.org/project/the-economy-book/ | HTTP 200 (26/10/2026) (dominio CORE verificado) |
| 1 | IMF Working Papers (serie) | https://www.imf.org/en/Publications/WP/ | Portal del FMI: el dominio imf.org deniega clientes automatizados; página confirmada por índice de búsqueda (26/10/2026); acceso abierto por política editorial del FMI |
| 2 | Principles of Microeconomics 3e (OpenStax) | https://openstax.org/details/books/principles-microeconomics-3e/ | Obra ya registrada como ficha ANA-DOC-0018; no se duplica |
| 2 | The Economy 2.0: Microeconomics (CORE Econ) | https://books.core-econ.org/the-economy/microeconomics/ | Obra ya registrada como ficha ANA-DOC-0014; no se duplica |
| 2 | Principles of Economics 3e (OpenStax, edición combinada) | https://openstax.org/details/books/principles-economics-3e/ | HTTP 200 (26/10/2026) |
| 2 | CORE Econ — Economy, Society, and Public Policy | https://www.core-econ.org/project/esp/ | HTTP 200 (26/10/2026) (dominio CORE verificado) |
| 2 | American Economic Journal: Microeconomics (portal AEA) | https://www.aeaweb.org/journals/mic | Portal AEA; el dominio aeaweb.org bloquea clientes automatizados (26/10/2026); índice abierto para navegación |
| 3 | IMF — World Economic Outlook (WEO) | https://www.imf.org/en/Publications/WEO/ | Portal del FMI: el dominio imf.org deniega clientes automatizados; página confirmada por índice de búsqueda (26/10/2026); acceso abierto por política editorial del FMI |
| 3 | IMF — External Sector Reports (ESR) | https://www.imf.org/en/Publications/ESR/ | Portal del FMI: el dominio imf.org deniega clientes automatizados; página confirmada por índice de búsqueda (26/10/2026); acceso abierto por política editorial del FMI |
| 3 | WTO — World Trade Report | https://www.wto.org/english/res_e/reser_e/wtr_e.htm | HTTP 200 (26/10/2026) |
| 3 | OECD — Economic Outlook | https://www.oecd.org/en/publications/oecd-economic-outlook.html | HTTP 200 (26/10/2026) |
| 3 | World Bank — Global Economic Prospects | https://www.worldbank.org/en/publication/global-economic-prospects | HTTP 200 (26/10/2026) |
| 4 | The Federal Reserve System: Purposes and Functions (Fed) | https://www.federalreserve.gov/aboutthefed/pf.htm | HTTP 200 (26/10/2026) |
| 4 | ECB Working Paper Series | https://www.ecb.europa.eu/pub/research/working-papers/html/index.en.html | HTTP 200 (26/10/2026) |
| 4 | BIS Working Papers | https://www.bis.org/list/research/index.htm | HTTP 200 (26/10/2026) |
| 4 | IMF — Monetary Policy and Central Banking (tema) | https://www.imf.org/en/Topics/monetary-policy | Portal del FMI: el dominio imf.org deniega clientes automatizados; página confirmada por índice de búsqueda (26/10/2026); acceso abierto por política editorial del FMI |
| 5 | IMF — Fiscal Monitor | https://www.imf.org/en/Publications/FM/ | Portal del FMI: el dominio imf.org deniega clientes automatizados; página confirmada por índice de búsqueda (26/10/2026); acceso abierto por política editorial del FMI |
| 5 | IMF — Fiscal Affairs Department Publications (tema) | https://www.imf.org/en/Topics/fiscal-policies | Portal del FMI: el dominio imf.org deniega clientes automatizados; página confirmada por índice de búsqueda (26/10/2026); acceso abierto por política editorial del FMI |
| 5 | OECD — Tax Policy Studies (tema) | https://www.oecd.org/en/topics/tax-policy.html | HTTP 200 (26/10/2026) |
| 5 | Fiscal Crises (IMF, DOI 10.5089/9781475592153.001) | https://doi.org/10.5089/9781475592153.001 | Existencia verificada en OpenAlex (IMF Working Paper, 2017, título exacto); serie del FMI de acceso abierto |
| 5 | Sovereign Risk, Fiscal Policy, and Macroeconomic Stability (IMF, DOI 10.5089/9781463933180.001) | https://doi.org/10.5089/9781463933180.001 | Existencia verificada en OpenAlex (IMF Working Paper, 2012, título exacto); serie del FMI de acceso abierto |
| 6 | NBER — Business Cycle Dating | https://www.nber.org/research/business-cycle-dating | Obra ya registrada como ficha ANA-DOC-0042; no se duplica |
| 6 | NBER — Working Papers (serie) | https://www.nber.org/papers | HTTP 200 (26/10/2026) |
| 6 | IMF — World Economic Outlook (véase Economía internacional) | https://www.imf.org/en/Publications/WEO/ | Obra ya registrada como ficha canal ya listado en el subtema 3; no se duplica |
| 6 | OECD Composite Leading Indicators (CLI) | https://www.oecd.org/en/data/indicators/composite-leading-indicator-cli.html | HTTP 200 (26/10/2026); metodología registrada como ANA-DOC-0072 |
| 7 | BIS — Annual Economic Report | https://www.bis.org/publ/arpdf/ar2024e.htm | HTTP 200 (26/10/2026) |
| 7 | ECB Economic Bulletin | https://www.ecb.europa.eu/press/economic-bulletin/html/index.en.html | HTTP 200 (26/10/2026) |
| 7 | IMF — Finance & Development (revista; el lote la listaba como «Inflation: Prices on the Rise» y en Demografía) | https://www.imf.org/en/Publications/fandd/ | Portal del FMI: el dominio imf.org deniega clientes automatizados; página confirmada por índice de búsqueda (26/10/2026); acceso abierto por política editorial del FMI |
| 7 | Federal Reserve — Monetary Policy Report | https://www.federalreserve.gov/monetarypolicy/mpr_default.htm | HTTP 200 (26/10/2026) |
| 8 | WTO — World Trade Report (véase Economía internacional) | https://www.wto.org/english/res_e/reser_e/wtr_e.htm | Obra ya registrada como ficha canal ya listado en el subtema 3; no se duplica |
| 8 | WTO — Trade Statistics | https://www.wto.org/english/res_e/statis_e/statis_e.htm | HTTP 200 (26/10/2026) |
| 8 | World Bank — World Development Report (serie) | https://www.worldbank.org/en/publication/wdr | HTTP 200 (26/10/2026) |
| 8 | UNCTAD — Trade and Development Report | https://unctad.org/topic/macroeconomics/trade-development-report | HTTP 200 (26/10/2026) |
| 8 | OECD — International Trade (tema) | https://www.oecd.org/en/topics/international-trade.html | HTTP 200 (26/10/2026) |
| 9 | World Bank — The Changing Nature of Work (WDR 2019) | https://www.worldbank.org/en/publication/wdr2019 | HTTP 200 (26/10/2026) |
| 9 | OECD — Productividad (portal; el Compendium of Productivity Indicators se publica en serie) | https://www.oecd.org/en/topics/productivity.html | HTTP 200 (26/10/2026) |
| 9 | The Conference Board — Total Economy Database | https://www.conference-board.org/data/economydatabase/ | HTTP 200 (26/10/2026) |
| 9 | Penn World Table (véase ANA-DOC-0061) | https://www.rug.nl/ggdc/productivity/pwt/ | Obra ya registrada como ficha ANA-DOC-0061; no se duplica |
| 9 | Our World in Data — Economic Growth | https://ourworldindata.org/economic-growth | HTTP 200 (26/10/2026) |
| 10 | World Population Prospects (véase ANA-DOC-0067) | https://population.un.org/wpp/ | Obra ya registrada como ficha ANA-DOC-0067; no se duplica |
| 10 | World Bank — World Development Indicators (Databank) | https://databank.worldbank.org/source/world-development-indicators | HTTP 200 (26/10/2026) |
| 10 | OECD — Pensions at a Glance (serie) | https://www.oecd.org/en/publications/pensions-at-a-glance.html | HTTP 200 (26/10/2026) |
| 10 | UN DESA — Population Division | https://www.un.org/development/desa/pd/ | HTTP 200 (26/10/2026) |
| 10 | IMF — Finance & Development (véase Inflación y tipos de interés) | https://www.imf.org/en/Publications/fandd/ | Obra ya registrada como ficha canal ya listado en el subtema 7; no se duplica |
| 11 | OECD Composite Leading Indicators (véase Ciclos económicos) | https://www.oecd.org/en/data/indicators/composite-leading-indicator-cli.html | Obra ya registrada como ficha canal ya listado en el subtema 6; no se duplica |
| 11 | Eurostat — National Accounts | https://ec.europa.eu/eurostat/web/national-accounts | HTTP 200 (26/10/2026) |
| 11 | Federal Reserve Bank of St. Louis — FRED | https://fred.stlouisfed.org/ | HTTP 200 (26/10/2026); base FRED-MD registrada como ANA-DOC-0090 |
| 11 | Conference Board — Leading Economic Index | https://www.conference-board.org/topics/us-leading-indicators | HTTP 200 (26/10/2026) |
| 11 | ECB — Statistical Data Warehouse | https://data.ecb.europa.eu/ | HTTP 200 (26/10/2026) |
| 12 | IMF — Fiscal Policy (véase Economía fiscal) | https://www.imf.org/en/Topics/fiscal-policies | Obra ya registrada como ficha canal ya listado en el subtema 5; no se duplica |
| 12 | IMF — Monetary Policy (véase Economía monetaria) | https://www.imf.org/en/Topics/monetary-policy | Obra ya registrada como ficha canal ya listado en el subtema 4; no se duplica |
| 12 | ECB — Monetary Policy | https://www.ecb.europa.eu/mopo/html/index.en.html | HTTP 200 (26/10/2026) |
| 12 | Federal Reserve — Monetary Policy (portal) | https://www.federalreserve.gov/monetarypolicy.htm | HTTP 200 (26/10/2026) |
| 12 | OECD — Economic Policy (tema; «Going for Growth» y reformas) | https://www.oecd.org/en/topics/economic-policy.html | HTTP 200 (26/10/2026) |
| 12 | World Bank — Research and Publications | https://www.worldbank.org/en/research | HTTP 200 (26/10/2026) |
| 13 | IMF — Global Financial Stability Report (GFSR) | https://www.imf.org/en/Publications/GFSR/ | Portal del FMI: el dominio imf.org deniega clientes automatizados; página confirmada por índice de búsqueda (26/10/2026); acceso abierto por política editorial del FMI |
| 13 | BIS — Quarterly Review | https://www.bis.org/publ/qtrpdf/r_qt.htm | HTTP 200 (26/10/2026) |
| 13 | World Bank — Global Economic Prospects (véase Economía internacional) | https://www.worldbank.org/en/publication/global-economic-prospects | Obra ya registrada como ficha canal ya listado en el subtema 3; no se duplica |
| 13 | NBER — Research on Financial Crises (véase Ciclos económicos) | https://www.nber.org/papers | Obra ya registrada como ficha canal ya listado en el subtema 6; no se duplica |
| 13 | IMF — Fiscal Policy for the Crisis (Policy Paper) | https://www.imf.org/en/Publications/Policy-Papers/Issues/2016/12/31/Fiscal-Policy-for-the-Crisis-PP4307 | Portal del FMI: el dominio imf.org deniega clientes automatizados; página confirmada por índice de búsqueda (26/10/2026); acceso abierto por política editorial del FMI |


#### Canales institucionales del lote del operador — bloque temático 2 (26/10/2026)

El lote del bloque 2 incluía además canales institucionales. Se registran 17 canales tras desduplicar las repeticiones internas del lote (ESPAS, OECD Strategic Foresight, EC Strategic Foresight Reports, Futures Toolkit y OECD STI Outlook aparecían más de una vez; las entradas con URL genérica no correspondiente al recurso titulado se excluyen, véase el informe de la entrega). Cada canal se comprobó el 26/10/2026; los portales que deniegan clientes automatizados quedan anotados para su confirmación por índice de búsqueda en el primer ciclo de mantenimiento.

| Subtema | Canal | URL | Verificación (26/10/2026) |
|---|---|---|---|
| 3 | European Journal of Futures Research (portal de la revista, SpringerOpen) | https://eujornalfuturesresearch.springeropen.com/ | HTTP 200 (26/10/2026); revista de acceso abierto |
| 4 | European Strategy and Policy Analysis System — ESPAS (portal) | https://espas.eu/ | Confirmado por navegación (26/10/2026): Global Trends to 2040 y 2030, ESPAS Foresight Papers y ORBIS; acceso libre; el lote lo duplicaba como «Global Trends to 2040» |
| 5 | Joint Research Centre — Megatrends Hub (portal; Competence Centre on Foresight) | https://knowledge4policy.ec.europa.eu/foresight_en | Confirmado por navegación (26/10/2026); el dominio knowledge4policy redirige a knowledge-for-policy (que deniega clientes automatizados) |
| 5 | OECD Strategic Foresight (programa) | https://www.oecd.org/en/about/programmes/strategic-foresight.html | Página confirmada por índice de búsqueda (26/10/2026); el portal OCDE deniega clientes automatizados |
| 5 | European Commission — Strategic Foresight Reports (portal) | https://commission.europa.eu/strategy-and-policy/strategic-planning/strategic-foresight_en | HTTP 200 (26/10/2026) |
| 5 | The Millennium Project (portal) | https://www.millennium-project.org/ | HTTP 200 (26/10/2026) |
| 6 | OECD — Science, Technology and Innovation Outlook (serie) | https://www.oecd.org/en/publications/oecd-science-technology-and-innovation-outlook.html | El portal OCDE deniega clientes automatizados; confirmar en mantenimiento (el lote lo duplicaba tres veces) |
| 6 | World Economic Forum — Global Risks Report (serie; informe 2025) | https://www.weforum.org/publications/global-risks-report-2025/ | El portal WEF deniega clientes automatizados; confirmar por índice de búsqueda en mantenimiento |
| 6 | UNDP — Human Development Reports (portal) | https://hdr.undp.org/ | HTTP 200 (26/10/2026) |
| 7 | OECD — Digital Transformation (tema) | https://www.oecd.org/en/topics/digital-transformation.html | El portal OCDE deniega clientes automatizados; confirmar en mantenimiento |
| 9 | OECD — Science, Technology and Innovation Scoreboard (panel de datos) | https://www.oecd.org/en/data/dashboards/oecd-science-technology-and-innovation-scoreboard.html | El portal OCDE deniega clientes automatizados; confirmar en mantenimiento |
| 9 | European Commission — Industrial Research and Innovation (área) | https://research-and-innovation.ec.europa.eu/research-area/industrial-research-and-innovation_en | HTTP 200 (26/10/2026) |
| 11 | UNEP — Global Environment Outlook (portal de la serie) | https://www.unep.org/global-environment-outlook | El portal UNEP deniega clientes automatizados (Cloudflare); confirmar en mantenimiento |
| 12 | The Millennium Project — State of the Future (serie) | https://www.millennium-project.org/state-of-the-future/ | HTTP 200 (26/10/2026) |
| 12 | IPCC (portal; el lote lo reclamaba como «Climate Change Scenarios and Projections») | https://www.ipcc.ch/ | HTTP 200 (26/10/2026) |
| 13 | European Commission — Key Enabling Technologies (área) | https://research-and-innovation.ec.europa.eu/research-area/industrial-research-and-innovation/key-enabling-technologies_en | El portal deniega clientes automatizados; confirmar en mantenimiento |
| 13 | OECD — Artificial Intelligence (tema) | https://www.oecd.org/en/topics/policy-issues/artificial-intelligence.html | El portal OCDE deniega clientes automatizados; confirmar en mantenimiento |

#### Taxonomía de bloques temáticos del operador (26/10/2026)

El operador fija una taxonomía de 19 bloques temáticos para la clasificación de fuentes de este archivo. El lote de 26/10/2026 corresponde íntegramente al bloque 1; los bloques siguientes se poblarán en tandas futuras. Los bloques y sus subtemas son:

1. **Economía y análisis macroeconómico** — Macroeconomía; Microeconomía; Economía internacional; Economía monetaria; Economía fiscal; Ciclos económicos; Inflación y tipos de interés; Comercio internacional; Productividad y crecimiento económico; Demografía y cambios estructurales; Indicadores adelantados y coincidentes; Políticas económicas y monetarias; Crisis económicas y financieras.
2. **Análisis de tendencias y prospectiva** — Análisis de tendencias; Prospectiva estratégica; Estudios de futuro; Detección de señales tempranas; Identificación de tendencias emergentes; Análisis de megatendencias; Ciclos de adopción tecnológica; Curvas de difusión de innovaciones; Ciclos de madurez industrial; Análisis de disrupciones; Análisis de cambios estructurales; Detección de puntos de inflexión; Análisis de convergencia tecnológica; Análisis de escenarios futuros.
3. **Investigación científica y tecnológica** — Método científico; Evaluación crítica de evidencia; Investigación interdisciplinar; Vigilancia tecnológica; Vigilancia científica; Análisis de publicaciones científicas; Análisis de patentes; Evaluación del nivel de madurez tecnológica; Transferencia tecnológica; Escalado industrial; Comercialización de innovaciones; Investigación y desarrollo; Análisis de la velocidad de innovación; Identificación de tecnologías sustitutivas y complementarias.
4. **Estrategia empresarial y dinámica competitiva** — Economía industrial; Organización industrial; Análisis de cadenas de valor; Análisis de ecosistemas empresariales; Análisis de ventajas competitivas; Barreras de entrada; Economías de escala; Efectos de red; Poder de negociación; Sustitución tecnológica; Disrupción de modelos de negocio; Ciclos de vida de industrias y productos; Concentración y fragmentación de mercados; Reconfiguración de cadenas de suministro; Identificación de ganadores y perdedores sectoriales.
5. **Tecnología e innovación transversal** — Inteligencia artificial; Computación avanzada; Semiconductores; Automatización y robótica; Ciberseguridad; Biotecnología; Nanotecnología; Materiales avanzados; Tecnologías energéticas; Electrificación; Almacenamiento de energía; Tecnologías espaciales; Telecomunicaciones; Fabricación avanzada; Tecnologías cuánticas; Digitalización industrial; Tecnologías de captura y transformación de datos.
6. **Geopolítica y geoeconomía** — Geopolítica; Geoeconomía; Relaciones internacionales; Política industrial estratégica; Competencia entre grandes potencias; Seguridad económica; Sanciones económicas; Aranceles y barreras comerciales; Controles de exportación; Nacionalismo de recursos; Dependencia de materias primas críticas; Reorganización de cadenas de suministro; Riesgo país; Conflictos y tensiones internacionales; Política energética internacional.
7. **Mercados, flujos de capital y comportamiento inversor** — Funcionamiento de los mercados financieros; Formación de precios; Oferta y demanda de activos; Flujos de capital; Comportamiento de inversores institucionales; Posicionamiento de grandes inversores; Ciclos de liquidez; Sentimiento de mercado; Psicología del inversor; Finanzas conductuales; Sesgos cognitivos; Narrativas de mercado; Exuberancia especulativa; Burbujas y correcciones; Anticipación de expectativas; Reacción del mercado a noticias y acontecimientos.
8. **Evaluación económica de tendencias** — Economía de la innovación; Economía de nuevas tecnologías; Economía de la adopción; Costes de producción y aprendizaje; Economías de escala y alcance; Curvas de aprendizaje; Costes marginales; Elasticidad de oferta y demanda; Sustitución entre tecnologías; Efectos de segundo orden; Externalidades económicas; Efectos indirectos sobre sectores relacionados; Creación y destrucción de mercados; Distribución del valor dentro de las cadenas productivas; Identificación de cuellos de botella; Evaluación de mercados potenciales; Estimación del mercado total, accesible y alcanzable; Rentabilidad económica de nuevas tecnologías.
9. **Análisis de oportunidades de inversión** — Traducción de tendencias en oportunidades invertibles; Identificación de activos beneficiados y perjudicados; Mecanismos de transmisión económica; Identificación de beneficiarios directos e indirectos; Identificación de proveedores críticos; Identificación de habilitadores tecnológicos; Identificación de sustitutos y perdedores estructurales; Accesibilidad de la oportunidad para el inversor; Identificación de instrumentos que permitan expresar una tesis; Relación entre tendencia, empresa y activo; Anticipación frente al consenso; Expectativas ya incorporadas en los precios; Saturación de narrativas de inversión; Ventaja temporal de una tesis; Catalizadores de reconocimiento por el mercado.
10. **Valoración preliminar y expectativas de mercado** — Fundamentos de valoración financiera; Relación entre fundamentales y precios; Expectativas de crecimiento; Expectativas de rentabilidad; Expectativas implícitas en los precios; Valoración relativa; Valoración por escenarios; Prima de riesgo; Riesgo de sobrevaloración; Riesgo de infravaloración; Sensibilidad de valoraciones a tipos de interés; Sensibilidad a crecimiento y márgenes; Descuento de flujos de caja como marco conceptual; Identificación de expectativas excesivas; Identificación de asimetrías entre potencial y riesgo.
11. **Análisis de riesgos y escenarios** — Gestión de riesgos de inversión; Riesgo tecnológico; Riesgo de adopción; Riesgo comercial; Riesgo de ejecución; Riesgo regulatorio; Riesgo geopolítico; Riesgo de financiación; Riesgo de sustitución; Riesgo de obsolescencia; Riesgo de concentración; Riesgo de liquidez; Riesgo de valoración; Análisis de escenarios alcistas, centrales y bajistas; Análisis de sensibilidad; Pruebas de estrés; Análisis de efectos de segundo orden; Premortem de tesis de inversión; Identificación de condiciones de invalidación; Indicadores de alerta temprana.
12. **Estadística, métodos cuantitativos y evaluación de evidencia** — Estadística descriptiva; Estadística inferencial; Análisis de series temporales; Análisis de tendencias estadísticas; Análisis de correlación; Análisis causal; Econometría; Modelización probabilística; Inferencia bayesiana; Simulación de escenarios; Análisis de incertidumbre; Detección de anomalías; Normalización de indicadores; Análisis de señales frente a ruido; Validación retrospectiva; Evaluación de falsos positivos y falsos negativos; Análisis de sensibilidad de puntuaciones; Calibración de modelos; Evaluación de la calidad predictiva; Control de sesgos de selección y supervivencia.
13. **Investigación documental e inteligencia de fuentes** — Investigación documental; Inteligencia económica; Inteligencia competitiva; Evaluación de credibilidad de fuentes; Jerarquización de fuentes; Identificación de fuentes primarias y secundarias; Verificación de afirmaciones; Corroboración independiente; Búsqueda de evidencia contraria; Detección de conflictos de interés; Detección de contenido promocional; Verificación de fechas y datos; Detección de información duplicada; Contraste de previsiones; Análisis de discrepancias; Trazabilidad de afirmaciones; Gestión de incertidumbre documental; Seguimiento de cambios en las fuentes; Investigación académica aplicada.
14. **Análisis de noticias, narrativas y consenso** — Análisis de prensa económica; Análisis de publicaciones sectoriales; Análisis de informes de expertos; Análisis de entrevistas y conferencias; Análisis de comunicaciones empresariales; Análisis de movimientos de fondos e inversores reconocidos; Análisis de narrativas emergentes; Detección de cambios de consenso; Detección de tendencias sobreexpuestas mediáticamente; Evaluación de la novedad de una información; Separación entre hechos, opiniones, rumores e hipótesis; Contraste entre narrativa y evidencia observable; Detección de expectativas no satisfechas; Análisis de divergencias entre percepción y realidad económica.
15. **Gestión de datos, automatización y seguimiento** — Investigación asistida por inteligencia artificial; Búsqueda avanzada de información; Recuperación de información; Extracción y estructuración de datos; Normalización de datos; Gestión de bases de datos; Seguimiento automatizado de indicadores; Detección de cambios relevantes; Monitorización de tendencias abiertas; Comparación entre ejecuciones; Registro histórico de hipótesis; Registro de evidencias y discrepancias; Versionado metodológico; Trazabilidad de cálculos; Automatización de informes; Control de calidad de datos; Gestión de fuentes y referencias; Reproducibilidad de investigaciones.
16. **Metodología de investigación y toma de decisiones** — Formulación de hipótesis de inversión; Diseño de investigaciones; Descomposición de problemas complejos; Priorización de investigaciones; Selección de tendencias por relevancia económica; Matrices de evaluación comparativa; Sistemas de puntuación multicriterio; Evaluación independiente de tendencia, oportunidad y confianza; Umbrales de selección; Puertas de control y descarte; Clasificación por madurez; Clasificación por horizonte temporal; Gestión de hipótesis pendientes de validación; Criterios de seguimiento y cierre; Aprendizaje mediante evaluación retrospectiva; Control de consistencia metodológica; Documentación de decisiones; Comunicación de conclusiones y limitaciones.
17. **Horizontes temporales y ciclos de inversión** — Tendencias de muy corto, corto, medio, largo y muy largo plazo; Ciclos económicos, de crédito, tecnológicos, de inversión empresarial, de construcción de capacidad, de inventarios y de financiación; Ciclos de adopción comercial; Desfases entre innovación, adopción y rentabilidad y entre fundamentales y cotizaciones; Catalizadores temporales; Indicadores de aceleración y desaceleración; Persistencia y caducidad de tendencias.
18. **Accesibilidad, restricciones y viabilidad de inversión** — Identificación inequívoca de activos e instrumentos; Mercados de negociación disponibles; Accesibilidad geográfica y jurídica; Restricciones regulatorias; Disponibilidad de instrumentos cotizados y no cotizados; Barreras mínimas de inversión; Liquidez preliminar; Costes de acceso; Riesgo de contraparte; Riesgo de custodia; Vehículos indirectos de exposición; Exposición económica efectiva; Riesgo de que el instrumento no represente adecuadamente la tendencia; Limitaciones de datos y verificabilidad; Distinción entre tendencia interesante y oportunidad realmente invertible.
19. **Ética, integridad y cumplimiento de la investigación** — Integridad de la investigación; Independencia analítica; Conflictos de interés; Prevención de manipulación informativa; Detección de publicidad encubierta; Detección de esquemas fraudulentos; Uso responsable de datos; Protección de credenciales y claves API; Seguridad de información; Trazabilidad y auditabilidad; Transparencia de limitaciones; Comunicación responsable de incertidumbre; Separación entre análisis exploratorio y conclusión validada.

### 4.4 Registro de servicios

El registro se abre con la primera operación del Documentador para el Analizador. La carga de arranque del operador (25/10/2026) no es un servicio DOC_REQUEST ni DOC_MAINTENANCE y no se registra aquí; queda anotada en el historial (4.6). Columnas del registro: service_id; request_id; run_id; execution_mode (DOC_REQUEST, DOC_MAINTENANCE); origin (BUSCADOR, OPERATOR, SCHEDULER); started_at; completed_at; as_of; prompt_version; strategy_version; guidance_version; canales consultados; cadenas aplicadas e iteraciones; fuentes entregadas, rechazadas y sin verificar; escrituras y su confirmación; lagunas; incidencias; estado final del servicio.

| service_id | request_id | run_id | execution_mode | origin | started_at | completed_at | Estado |
|---|---|---|---|---|---|---|---|
| (sin servicios registrados a la fecha de la carga de arranque) | — | — | — | — | — | — | — |

### 4.5 Registro de mantenimiento

El primer ciclo DOC_MAINTENANCE lo ejecutará el Documentador para el Analizador según el calendario que fije el operador (Anexo A). Columnas del registro: service_id; fecha; tipo de ciclo (enlaces, retractaciones, ediciones, índice); entradas revisadas; hallazgos; cambios de estado registrados con fecha y motivo; pendientes declarados.

| service_id | Fecha | Tipo de ciclo | Entradas revisadas | Hallazgos | Cambios de estado | Pendientes |
|---|---|---|---|---|---|---|
| (sin ciclos registrados a la fecha de la carga de arranque) | — | — | — | — | — | Revisar las 5 fichas pendientes de acceso gratuito |

### 4.6 Historial de altas y cambios de estado

| Fecha | Ficha afectada | Movimiento | Agente u origen responsable | Motivo |
|---|---|---|---|---|
| 2026-10-25 | ANA-DOC-0001 | Alta | Operador (carga de arranque) | Fondo inicial de momentum cruzado: referencia fundacional |
| 2026-10-25 | ANA-DOC-0002 | Alta | Operador (carga de arranque) | Fondo inicial de momentum temporal: referencia central |
| 2026-10-25 | ANA-DOC-0002 | Corrección de cita | Documentador para el Analizador | Subsanación de errata en volumen (de vol. 120, n.º 2 a vol. 104, n.º 2, págs. 228-250) re-verificada en RePEc/ScienceDirect. |
| 2026-10-25 | ANA-DOC-0003 | Alta | Operador (carga de arranque) | Momentum multiactivo y combinación con valor |
| 2026-10-25 | ANA-DOC-0004 | Alta | Operador (carga de arranque) | Robustez histórica del trend-following |
| 2026-10-25 | ANA-DOC-0005 | Alta (pendiente de acceso gratuito) | Operador (carga de arranque) | Clásico del análisis técnico; resolver acceso en primera revisión |
| 2026-10-25 | ANA-DOC-0006 | Alta | Operador (carga de arranque) | Salvaguarda metodológica contra data snooping |
| 2026-10-25 | ANA-DOC-0007 | Alta (pendiente de acceso gratuito) | Operador (carga de arranque) | Formalización estadística del análisis técnico |
| 2026-10-25 | ANA-DOC-0008 | Alta | Operador (carga de arranque) | Momentum en divisas: extensión de clase de activo |
| 2026-10-25 | ANA-DOC-0009 | Alta | Operador (carga de arranque) | Filtro de media móvil de referencia práctica |
| 2026-10-25 | ANA-DOC-0010 | Alta (pendiente de acceso gratuito) | Operador (carga de arranque) | Factor de tendencia multi-horizonte |
| 2026-10-25 | ANA-DOC-0011 | Alta (pendiente de acceso gratuito) | Operador (carga de arranque) | Origen histórico de la fuerza relativa |
| 2026-10-25 | ANA-DOC-0012 | Alta (pendiente de acceso gratuito) | Operador (carga de arranque) | Marco de doble momentum; resolver acceso o sustituir por fuente primaria |

| 2026-10-26 | ANA-DOC-0013 | Alta (lote del operador) | Operador (lote del bloque temático 1) | Subtema 1: Macroeconomía — enlace y acceso libre verificados el 26/10/2026 |
| 2026-10-26 | ANA-DOC-0014 | Alta (lote del operador) | Operador (lote del bloque temático 1) | Subtema 1: Macroeconomía — enlace y acceso libre verificados el 26/10/2026 |
| 2026-10-26 | ANA-DOC-0015 | Alta (lote del operador) | Operador (lote del bloque temático 1) | Subtema 1: Macroeconomía — enlace y acceso libre verificados el 26/10/2026 |
| 2026-10-26 | ANA-DOC-0016 | Alta (lote del operador) | Operador (lote del bloque temático 1) | Subtema 1: Macroeconomía — enlace y acceso libre verificados el 26/10/2026 |
| 2026-10-26 | ANA-DOC-0017 | Alta (lote del operador) | Operador (lote del bloque temático 1) | Subtema 1: Macroeconomía — enlace y acceso libre verificados el 26/10/2026 |
| 2026-10-26 | ANA-DOC-0018 | Alta (lote del operador) | Operador (lote del bloque temático 1) | Subtema 2: Microeconomía — enlace y acceso libre verificados el 26/10/2026 |
| 2026-10-26 | ANA-DOC-0019 | Alta (lote del operador) | Operador (lote del bloque temático 1) | Subtema 2: Microeconomía — enlace y acceso libre verificados el 26/10/2026 |
| 2026-10-26 | ANA-DOC-0020 | Alta (lote del operador) | Operador (lote del bloque temático 1) | Subtema 2: Microeconomía — enlace y acceso libre verificados el 26/10/2026 |
| 2026-10-26 | ANA-DOC-0021 | Alta (lote del operador) | Operador (lote del bloque temático 1) | Subtema 2: Microeconomía — enlace y acceso libre verificados el 26/10/2026 |
| 2026-10-26 | ANA-DOC-0022 | Alta (lote del operador) | Operador (lote del bloque temático 1) | Subtema 2: Microeconomía — enlace y acceso libre verificados el 26/10/2026 |
| 2026-10-26 | ANA-DOC-0023 | Alta (lote del operador) | Operador (lote del bloque temático 1) | Subtema 3: Economía internacional — enlace y acceso libre verificados el 26/10/2026 |
| 2026-10-26 | ANA-DOC-0024 | Alta (lote del operador) | Operador (lote del bloque temático 1) | Subtema 3: Economía internacional — enlace y acceso libre verificados el 26/10/2026 |
| 2026-10-26 | ANA-DOC-0025 | Alta (lote del operador) | Operador (lote del bloque temático 1) | Subtema 3: Economía internacional — enlace y acceso libre verificados el 26/10/2026 |
| 2026-10-26 | ANA-DOC-0026 | Alta (lote del operador) | Operador (lote del bloque temático 1) | Subtema 3: Economía internacional — enlace y acceso libre verificados el 26/10/2026 |
| 2026-10-26 | ANA-DOC-0027 | Alta (lote del operador) | Operador (lote del bloque temático 1) | Subtema 3: Economía internacional — enlace y acceso libre verificados el 26/10/2026 |
| 2026-10-26 | ANA-DOC-0028 | Alta (lote del operador) | Operador (lote del bloque temático 1) | Subtema 3: Economía internacional — enlace y acceso libre verificados el 26/10/2026 |
| 2026-10-26 | ANA-DOC-0029 | Alta (lote del operador) | Operador (lote del bloque temático 1) | Subtema 3: Economía internacional — enlace y acceso libre verificados el 26/10/2026 |
| 2026-10-26 | ANA-DOC-0030 | Alta (lote del operador) | Operador (lote del bloque temático 1) | Subtema 4: Economía monetaria — enlace y acceso libre verificados el 26/10/2026 |
| 2026-10-26 | ANA-DOC-0031 | Alta (lote del operador) | Operador (lote del bloque temático 1) | Subtema 4: Economía monetaria — enlace y acceso libre verificados el 26/10/2026 |
| 2026-10-26 | ANA-DOC-0032 | Alta (lote del operador) | Operador (lote del bloque temático 1) | Subtema 4: Economía monetaria — enlace y acceso libre verificados el 26/10/2026 |
| 2026-10-26 | ANA-DOC-0033 | Alta (lote del operador) | Operador (lote del bloque temático 1) | Subtema 4: Economía monetaria — enlace y acceso libre verificados el 26/10/2026 |
| 2026-10-26 | ANA-DOC-0034 | Alta (lote del operador) | Operador (lote del bloque temático 1) | Subtema 5: Economía fiscal — enlace y acceso libre verificados el 26/10/2026 |
| 2026-10-26 | ANA-DOC-0035 | Alta (lote del operador) | Operador (lote del bloque temático 1) | Subtema 5: Economía fiscal — enlace y acceso libre verificados el 26/10/2026 |
| 2026-10-26 | ANA-DOC-0036 | Alta (lote del operador) | Operador (lote del bloque temático 1) | Subtema 5: Economía fiscal — enlace y acceso libre verificados el 26/10/2026 |
| 2026-10-26 | ANA-DOC-0037 | Alta (lote del operador) | Operador (lote del bloque temático 1) | Subtema 5: Economía fiscal — enlace y acceso libre verificados el 26/10/2026 |
| 2026-10-26 | ANA-DOC-0038 | Alta (lote del operador) | Operador (lote del bloque temático 1) | Subtema 5: Economía fiscal — enlace y acceso libre verificados el 26/10/2026 |
| 2026-10-26 | ANA-DOC-0039 | Alta (lote del operador) | Operador (lote del bloque temático 1) | Subtema 5: Economía fiscal — enlace y acceso libre verificados el 26/10/2026 |
| 2026-10-26 | ANA-DOC-0040 | Alta (lote del operador) | Operador (lote del bloque temático 1) | Subtema 6: Ciclos económicos — enlace y acceso libre verificados el 26/10/2026 |
| 2026-10-26 | ANA-DOC-0041 | Alta (lote del operador) | Operador (lote del bloque temático 1) | Subtema 6: Ciclos económicos — enlace y acceso libre verificados el 26/10/2026 |
| 2026-10-26 | ANA-DOC-0042 | Alta (lote del operador) | Operador (lote del bloque temático 1) | Subtema 6: Ciclos económicos — enlace y acceso libre verificados el 26/10/2026 |
| 2026-10-26 | ANA-DOC-0043 | Alta (lote del operador) | Operador (lote del bloque temático 1) | Subtema 6: Ciclos económicos — enlace y acceso libre verificados el 26/10/2026 |
| 2026-10-26 | ANA-DOC-0044 | Alta (lote del operador) | Operador (lote del bloque temático 1) | Subtema 6: Ciclos económicos — enlace y acceso libre verificados el 26/10/2026 |
| 2026-10-26 | ANA-DOC-0045 | Alta (lote del operador) | Operador (lote del bloque temático 1) | Subtema 6: Ciclos económicos — enlace y acceso libre verificados el 26/10/2026 |
| 2026-10-26 | ANA-DOC-0046 | Alta (lote del operador) | Operador (lote del bloque temático 1) | Subtema 6: Ciclos económicos — enlace y acceso libre verificados el 26/10/2026 |
| 2026-10-26 | ANA-DOC-0047 | Alta (lote del operador) | Operador (lote del bloque temático 1) | Subtema 7: Inflación y tipos de interés — enlace y acceso libre verificados el 26/10/2026 |
| 2026-10-26 | ANA-DOC-0048 | Alta (lote del operador) | Operador (lote del bloque temático 1) | Subtema 7: Inflación y tipos de interés — enlace y acceso libre verificados el 26/10/2026 |
| 2026-10-26 | ANA-DOC-0049 | Alta (lote del operador) | Operador (lote del bloque temático 1) | Subtema 7: Inflación y tipos de interés — enlace y acceso libre verificados el 26/10/2026 |
| 2026-10-26 | ANA-DOC-0050 | Alta (lote del operador) | Operador (lote del bloque temático 1) | Subtema 7: Inflación y tipos de interés — enlace y acceso libre verificados el 26/10/2026 |
| 2026-10-26 | ANA-DOC-0051 | Alta (lote del operador) | Operador (lote del bloque temático 1) | Subtema 7: Inflación y tipos de interés — enlace y acceso libre verificados el 26/10/2026 |
| 2026-10-26 | ANA-DOC-0052 | Alta (lote del operador) | Operador (lote del bloque temático 1) | Subtema 7: Inflación y tipos de interés — enlace y acceso libre verificados el 26/10/2026 |
| 2026-10-26 | ANA-DOC-0053 | Alta (lote del operador) | Operador (lote del bloque temático 1) | Subtema 7: Inflación y tipos de interés — enlace y acceso libre verificados el 26/10/2026 |
| 2026-10-26 | ANA-DOC-0054 | Alta (lote del operador) | Operador (lote del bloque temático 1) | Subtema 7: Inflación y tipos de interés — enlace y acceso libre verificados el 26/10/2026 |
| 2026-10-26 | ANA-DOC-0055 | Alta (lote del operador) | Operador (lote del bloque temático 1) | Subtema 7: Inflación y tipos de interés — enlace y acceso libre verificados el 26/10/2026 |
| 2026-10-26 | ANA-DOC-0056 | Alta (lote del operador) | Operador (lote del bloque temático 1) | Subtema 8: Comercio internacional — enlace y acceso libre verificados el 26/10/2026 |
| 2026-10-26 | ANA-DOC-0057 | Alta (lote del operador) | Operador (lote del bloque temático 1) | Subtema 8: Comercio internacional — enlace y acceso libre verificados el 26/10/2026 |
| 2026-10-26 | ANA-DOC-0058 | Alta (lote del operador) | Operador (lote del bloque temático 1) | Subtema 8: Comercio internacional — enlace y acceso libre verificados el 26/10/2026 |
| 2026-10-26 | ANA-DOC-0059 | Alta (lote del operador) | Operador (lote del bloque temático 1) | Subtema 9: Productividad y crecimiento económico — enlace y acceso libre verificados el 26/10/2026 |
| 2026-10-26 | ANA-DOC-0060 | Alta (lote del operador) | Operador (lote del bloque temático 1) | Subtema 9: Productividad y crecimiento económico — enlace y acceso libre verificados el 26/10/2026 |
| 2026-10-26 | ANA-DOC-0061 | Alta (lote del operador) | Operador (lote del bloque temático 1) | Subtema 9: Productividad y crecimiento económico — enlace y acceso libre verificados el 26/10/2026 |
| 2026-10-26 | ANA-DOC-0062 | Alta (lote del operador) | Operador (lote del bloque temático 1) | Subtema 9: Productividad y crecimiento económico — enlace y acceso libre verificados el 26/10/2026 |
| 2026-10-26 | ANA-DOC-0063 | Alta (lote del operador) | Operador (lote del bloque temático 1) | Subtema 9: Productividad y crecimiento económico — enlace y acceso libre verificados el 26/10/2026 |
| 2026-10-26 | ANA-DOC-0064 | Alta (lote del operador) | Operador (lote del bloque temático 1) | Subtema 9: Productividad y crecimiento económico — enlace y acceso libre verificados el 26/10/2026 |
| 2026-10-26 | ANA-DOC-0065 | Alta (lote del operador) | Operador (lote del bloque temático 1) | Subtema 9: Productividad y crecimiento económico — enlace y acceso libre verificados el 26/10/2026 |
| 2026-10-26 | ANA-DOC-0066 | Alta (lote del operador) | Operador (lote del bloque temático 1) | Subtema 9: Productividad y crecimiento económico — enlace y acceso libre verificados el 26/10/2026 |
| 2026-10-26 | ANA-DOC-0067 | Alta (lote del operador) | Operador (lote del bloque temático 1) | Subtema 10: Demografía y cambios estructurales — enlace y acceso libre verificados el 26/10/2026 |
| 2026-10-26 | ANA-DOC-0068 | Alta (lote del operador) | Operador (lote del bloque temático 1) | Subtema 10: Demografía y cambios estructurales — enlace y acceso libre verificados el 26/10/2026 |
| 2026-10-26 | ANA-DOC-0069 | Alta (lote del operador) | Operador (lote del bloque temático 1) | Subtema 10: Demografía y cambios estructurales — enlace y acceso libre verificados el 26/10/2026 |
| 2026-10-26 | ANA-DOC-0070 | Alta (lote del operador) | Operador (lote del bloque temático 1) | Subtema 10: Demografía y cambios estructurales — enlace y acceso libre verificados el 26/10/2026 |
| 2026-10-26 | ANA-DOC-0071 | Alta (lote del operador) | Operador (lote del bloque temático 1) | Subtema 10: Demografía y cambios estructurales — enlace y acceso libre verificados el 26/10/2026 |
| 2026-10-26 | ANA-DOC-0072 | Alta (lote del operador) | Operador (lote del bloque temático 1) | Subtema 11: Indicadores adelantados y coincidentes — enlace y acceso libre verificados el 26/10/2026 |
| 2026-10-26 | ANA-DOC-0073 | Alta (lote del operador) | Operador (lote del bloque temático 1) | Subtema 11: Indicadores adelantados y coincidentes — enlace y acceso libre verificados el 26/10/2026 |
| 2026-10-26 | ANA-DOC-0074 | Alta (lote del operador) | Operador (lote del bloque temático 1) | Subtema 11: Indicadores adelantados y coincidentes — enlace y acceso libre verificados el 26/10/2026 |
| 2026-10-26 | ANA-DOC-0075 | Alta (lote del operador) | Operador (lote del bloque temático 1) | Subtema 11: Indicadores adelantados y coincidentes — enlace y acceso libre verificados el 26/10/2026 |
| 2026-10-26 | ANA-DOC-0076 | Alta (lote del operador) | Operador (lote del bloque temático 1) | Subtema 11: Indicadores adelantados y coincidentes — enlace y acceso libre verificados el 26/10/2026 |
| 2026-10-26 | ANA-DOC-0077 | Alta (lote del operador) | Operador (lote del bloque temático 1) | Subtema 11: Indicadores adelantados y coincidentes — enlace y acceso libre verificados el 26/10/2026 |
| 2026-10-26 | ANA-DOC-0078 | Alta (lote del operador) | Operador (lote del bloque temático 1) | Subtema 12: Políticas económicas y monetarias — enlace y acceso libre verificados el 26/10/2026 |
| 2026-10-26 | ANA-DOC-0079 | Alta (lote del operador) | Operador (lote del bloque temático 1) | Subtema 12: Políticas económicas y monetarias — enlace y acceso libre verificados el 26/10/2026 |
| 2026-10-26 | ANA-DOC-0080 | Alta (lote del operador) | Operador (lote del bloque temático 1) | Subtema 12: Políticas económicas y monetarias — enlace y acceso libre verificados el 26/10/2026 |
| 2026-10-26 | ANA-DOC-0081 | Alta (lote del operador) | Operador (lote del bloque temático 1) | Subtema 12: Políticas económicas y monetarias — enlace y acceso libre verificados el 26/10/2026 |
| 2026-10-26 | ANA-DOC-0082 | Alta (lote del operador) | Operador (lote del bloque temático 1) | Subtema 12: Políticas económicas y monetarias — enlace y acceso libre verificados el 26/10/2026 |
| 2026-10-26 | ANA-DOC-0083 | Alta (lote del operador) | Operador (lote del bloque temático 1) | Subtema 12: Políticas económicas y monetarias — enlace y acceso libre verificados el 26/10/2026 |
| 2026-10-26 | ANA-DOC-0084 | Alta (lote del operador) | Operador (lote del bloque temático 1) | Subtema 13: Crisis económicas y financieras — enlace y acceso libre verificados el 26/10/2026 |
| 2026-10-26 | ANA-DOC-0085 | Alta (lote del operador) | Operador (lote del bloque temático 1) | Subtema 13: Crisis económicas y financieras — enlace y acceso libre verificados el 26/10/2026 |
| 2026-10-26 | ANA-DOC-0086 | Alta (lote del operador) | Operador (lote del bloque temático 1) | Subtema 13: Crisis económicas y financieras — enlace y acceso libre verificados el 26/10/2026 |
| 2026-10-26 | ANA-DOC-0087 | Alta (lote del operador) | Operador (lote del bloque temático 1) | Subtema 13: Crisis económicas y financieras — enlace y acceso libre verificados el 26/10/2026 |
| 2026-10-26 | ANA-DOC-0088 | Alta (lote del operador) | Operador (lote del bloque temático 1) | Subtema T: Transversal: métodos, datos y normas (aporte del lote; bloques 12, 15 y 17 del operador) — enlace y acceso libre verificados el 26/10/2026 |
| 2026-10-26 | ANA-DOC-0089 | Alta (lote del operador) | Operador (lote del bloque temático 1) | Subtema T: Transversal: métodos, datos y normas (aporte del lote; bloques 12, 15 y 17 del operador) — enlace y acceso libre verificados el 26/10/2026 |
| 2026-10-26 | ANA-DOC-0090 | Alta (lote del operador) | Operador (lote del bloque temático 1) | Subtema T: Transversal: métodos, datos y normas (aporte del lote; bloques 12, 15 y 17 del operador) — enlace y acceso libre verificados el 26/10/2026 |
| 2026-10-26 | ANA-DOC-0091 | Alta (lote del operador) | Operador (lote del bloque temático 1) | Subtema T: Transversal: métodos, datos y normas (aporte del lote; bloques 12, 15 y 17 del operador) — enlace y acceso libre verificados el 26/10/2026 |

| 2026-10-26 | ANA-DOC-0092 | Alta (lote del operador) | Operador (lote del bloque temático 2) | Subtema 1: Análisis de tendencias — enlace y acceso libre verificados el 26/10/2026 |
| 2026-10-26 | ANA-DOC-0093 | Alta (lote del operador, pendiente de acceso gratuito) | Operador (lote del bloque temático 2) | Subtema 1: Análisis de tendencias — enlaces y metadatos verificados el 26/10/2026; peldaño legal por localizar (portal OCDE) |
| 2026-10-26 | ANA-DOC-0094 | Alta (lote del operador) | Operador (lote del bloque temático 2) | Subtema 1: Análisis de tendencias — enlace y acceso libre verificados el 26/10/2026 |
| 2026-10-26 | ANA-DOC-0095 | Alta (lote del operador) | Operador (lote del bloque temático 2) | Subtema 2: Prospectiva estratégica — enlace y acceso libre verificados el 26/10/2026 |
| 2026-10-26 | ANA-DOC-0096 | Alta (lote del operador) | Operador (lote del bloque temático 2) | Subtema 2: Prospectiva estratégica — enlace y acceso libre verificados el 26/10/2026 |
| 2026-10-26 | ANA-DOC-0097 | Alta (lote del operador) | Operador (lote del bloque temático 2) | Subtema 2: Prospectiva estratégica — enlace y acceso libre verificados el 26/10/2026 |
| 2026-10-26 | ANA-DOC-0098 | Alta (lote del operador) | Operador (lote del bloque temático 2) | Subtema 2: Prospectiva estratégica — enlace y acceso libre verificados el 26/10/2026 |
| 2026-10-26 | ANA-DOC-0099 | Alta (lote del operador) | Operador (lote del bloque temático 2) | Subtema 2: Prospectiva estratégica — enlace y acceso libre verificados el 26/10/2026 |
| 2026-10-26 | ANA-DOC-0100 | Alta (lote del operador, pendiente de acceso gratuito) | Operador (lote del bloque temático 2) | Subtema 2: Prospectiva estratégica — enlaces y metadatos verificados el 26/10/2026; peldaño legal por localizar (portal OCDE) |
| 2026-10-26 | ANA-DOC-0101 | Alta (lote del operador) | Operador (lote del bloque temático 2) | Subtema 2: Prospectiva estratégica — enlace y acceso libre verificados el 26/10/2026 |
| 2026-10-26 | ANA-DOC-0102 | Alta (lote del operador) | Operador (lote del bloque temático 2) | Subtema 3: Estudios de futuro — enlace y acceso libre verificados el 26/10/2026 |
| 2026-10-26 | ANA-DOC-0103 | Alta (lote del operador) | Operador (lote del bloque temático 2) | Subtema 3: Estudios de futuro — enlace y acceso libre verificados el 26/10/2026 |
| 2026-10-26 | ANA-DOC-0104 | Alta (lote del operador) | Operador (lote del bloque temático 2) | Subtema 3: Estudios de futuro — enlace y acceso libre verificados el 26/10/2026 |
| 2026-10-26 | ANA-DOC-0105 | Alta (lote del operador) | Operador (lote del bloque temático 2) | Subtema 3: Estudios de futuro — enlace y acceso libre verificados el 26/10/2026 |
| 2026-10-26 | ANA-DOC-0106 | Alta (lote del operador) | Operador (lote del bloque temático 2) | Subtema 3: Estudios de futuro — enlace y acceso libre verificados el 26/10/2026 |
| 2026-10-26 | ANA-DOC-0107 | Alta (lote del operador) | Operador (lote del bloque temático 2) | Subtema 3: Estudios de futuro — enlace y acceso libre verificados el 26/10/2026 |
| 2026-10-26 | ANA-DOC-0108 | Alta (lote del operador) | Operador (lote del bloque temático 2) | Subtema 4: Detección de señales tempranas — enlace y acceso libre verificados el 26/10/2026 |
| 2026-10-26 | ANA-DOC-0109 | Alta (lote del operador) | Operador (lote del bloque temático 2) | Subtema 4: Detección de señales tempranas — enlace y acceso libre verificados el 26/10/2026 |
| 2026-10-26 | ANA-DOC-0110 | Alta (lote del operador) | Operador (lote del bloque temático 2) | Subtema 4: Detección de señales tempranas — enlace y acceso libre verificados el 26/10/2026 |
| 2026-10-26 | ANA-DOC-0111 | Alta (lote del operador) | Operador (lote del bloque temático 2) | Subtema 4: Detección de señales tempranas — enlace y acceso libre verificados el 26/10/2026 |
| 2026-10-26 | ANA-DOC-0112 | Alta (lote del operador) | Operador (lote del bloque temático 2) | Subtema 4: Detección de señales tempranas — enlace y acceso libre verificados el 26/10/2026 |
| 2026-10-26 | ANA-DOC-0113 | Alta (lote del operador) | Operador (lote del bloque temático 2) | Subtema 4: Detección de señales tempranas — enlace y acceso libre verificados el 26/10/2026 |
| 2026-10-26 | ANA-DOC-0114 | Alta (lote del operador) | Operador (lote del bloque temático 2) | Subtema 5: Identificación de tendencias emergentes — enlace y acceso libre verificados el 26/10/2026 |
| 2026-10-26 | ANA-DOC-0115 | Alta (lote del operador) | Operador (lote del bloque temático 2) | Subtema 5: Identificación de tendencias emergentes — enlace y acceso libre verificados el 26/10/2026 |
| 2026-10-26 | ANA-DOC-0116 | Alta (lote del operador) | Operador (lote del bloque temático 2) | Subtema 5: Identificación de tendencias emergentes — enlace y acceso libre verificados el 26/10/2026 |
| 2026-10-26 | ANA-DOC-0117 | Alta (lote del operador) | Operador (lote del bloque temático 2) | Subtema 5: Identificación de tendencias emergentes — enlace y acceso libre verificados el 26/10/2026 |
| 2026-10-26 | ANA-DOC-0118 | Alta (lote del operador) | Operador (lote del bloque temático 2) | Subtema 6: Análisis de megatendencias — enlace y acceso libre verificados el 26/10/2026 |
| 2026-10-26 | ANA-DOC-0119 | Alta (lote del operador) | Operador (lote del bloque temático 2) | Subtema 6: Análisis de megatendencias — enlace y acceso libre verificados el 26/10/2026 |
| 2026-10-26 | ANA-DOC-0120 | Alta (lote del operador) | Operador (lote del bloque temático 2) | Subtema 6: Análisis de megatendencias — enlace y acceso libre verificados el 26/10/2026 |
| 2026-10-26 | ANA-DOC-0121 | Alta (lote del operador) | Operador (lote del bloque temático 2) | Subtema 6: Análisis de megatendencias — enlace y acceso libre verificados el 26/10/2026 |
| 2026-10-26 | ANA-DOC-0122 | Alta (lote del operador) | Operador (lote del bloque temático 2) | Subtema 6: Análisis de megatendencias — enlace y acceso libre verificados el 26/10/2026 |
| 2026-10-26 | ANA-DOC-0123 | Alta (lote del operador) | Operador (lote del bloque temático 2) | Subtema 7: Ciclos de adopción tecnológica — enlace y acceso libre verificados el 26/10/2026 |
| 2026-10-26 | ANA-DOC-0124 | Alta (lote del operador, pendiente de acceso gratuito) | Operador (lote del bloque temático 2) | Subtema 8: Curvas de difusión de innovaciones — enlaces y metadatos verificados el 26/10/2026; peldaño legal por localizar (portal OCDE) |
| 2026-10-26 | ANA-DOC-0125 | Alta (lote del operador) | Operador (lote del bloque temático 2) | Subtema 8: Curvas de difusión de innovaciones — enlace y acceso libre verificados el 26/10/2026 |
| 2026-10-26 | ANA-DOC-0126 | Alta (lote del operador) | Operador (lote del bloque temático 2) | Subtema 8: Curvas de difusión de innovaciones — enlace y acceso libre verificados el 26/10/2026 |
| 2026-10-26 | ANA-DOC-0127 | Alta (lote del operador) | Operador (lote del bloque temático 2) | Subtema 8: Curvas de difusión de innovaciones — enlace y acceso libre verificados el 26/10/2026 |
| 2026-10-26 | ANA-DOC-0128 | Alta (lote del operador) | Operador (lote del bloque temático 2) | Subtema 9: Ciclos de madurez industrial — enlace y acceso libre verificados el 26/10/2026 |
| 2026-10-26 | ANA-DOC-0129 | Alta (lote del operador, pendiente de acceso gratuito) | Operador (lote del bloque temático 2) | Subtema 9: Ciclos de madurez industrial — enlaces y metadatos verificados el 26/10/2026; peldaño legal por localizar (portal OCDE) |
| 2026-10-26 | ANA-DOC-0130 | Alta (lote del operador) | Operador (lote del bloque temático 2) | Subtema 9: Ciclos de madurez industrial — enlace y acceso libre verificados el 26/10/2026 |
| 2026-10-26 | ANA-DOC-0131 | Alta (lote del operador) | Operador (lote del bloque temático 2) | Subtema 9: Ciclos de madurez industrial — enlace y acceso libre verificados el 26/10/2026 |
| 2026-10-26 | ANA-DOC-0132 | Alta (lote del operador) | Operador (lote del bloque temático 2) | Subtema 10: Análisis de disrupciones — enlace y acceso libre verificados el 26/10/2026 |
| 2026-10-26 | ANA-DOC-0133 | Alta (lote del operador) | Operador (lote del bloque temático 2) | Subtema 10: Análisis de disrupciones — enlace y acceso libre verificados el 26/10/2026 |
| 2026-10-26 | ANA-DOC-0134 | Alta (lote del operador) | Operador (lote del bloque temático 2) | Subtema 10: Análisis de disrupciones — enlace y acceso libre verificados el 26/10/2026 |
| 2026-10-26 | ANA-DOC-0135 | Alta (lote del operador) | Operador (lote del bloque temático 2) | Subtema 10: Análisis de disrupciones — enlace y acceso libre verificados el 26/10/2026 |
| 2026-10-26 | ANA-DOC-0136 | Alta (lote del operador) | Operador (lote del bloque temático 2) | Subtema 10: Análisis de disrupciones — enlace y acceso libre verificados el 26/10/2026 |
| 2026-10-26 | ANA-DOC-0137 | Alta (lote del operador) | Operador (lote del bloque temático 2) | Subtema 11: Análisis de cambios estructurales — enlace y acceso libre verificados el 26/10/2026 |
| 2026-10-26 | ANA-DOC-0138 | Alta (lote del operador) | Operador (lote del bloque temático 2) | Subtema 11: Análisis de cambios estructurales — enlace y acceso libre verificados el 26/10/2026 |
| 2026-10-26 | ANA-DOC-0139 | Alta (lote del operador) | Operador (lote del bloque temático 2) | Subtema 11: Análisis de cambios estructurales — enlace y acceso libre verificados el 26/10/2026 |
| 2026-10-26 | ANA-DOC-0140 | Alta (lote del operador) | Operador (lote del bloque temático 2) | Subtema 12: Detección de puntos de inflexión — enlace y acceso libre verificados el 26/10/2026 |
| 2026-10-26 | ANA-DOC-0141 | Alta (lote del operador) | Operador (lote del bloque temático 2) | Subtema 12: Detección de puntos de inflexión — enlace y acceso libre verificados el 26/10/2026 |
| 2026-10-26 | ANA-DOC-0142 | Alta (lote del operador) | Operador (lote del bloque temático 2) | Subtema 12: Detección de puntos de inflexión — enlace y acceso libre verificados el 26/10/2026 |
| 2026-10-26 | ANA-DOC-0143 | Alta (lote del operador) | Operador (lote del bloque temático 2) | Subtema 12: Detección de puntos de inflexión — enlace y acceso libre verificados el 26/10/2026 |
| 2026-10-26 | ANA-DOC-0144 | Alta (lote del operador) | Operador (lote del bloque temático 2) | Subtema 13: Análisis de convergencia tecnológica — enlace y acceso libre verificados el 26/10/2026 |
| 2026-10-26 | ANA-DOC-0145 | Alta (lote del operador) | Operador (lote del bloque temático 2) | Subtema 13: Análisis de convergencia tecnológica — enlace y acceso libre verificados el 26/10/2026 |
| 2026-10-26 | ANA-DOC-0146 | Alta (lote del operador) | Operador (lote del bloque temático 2) | Subtema 13: Análisis de convergencia tecnológica — enlace y acceso libre verificados el 26/10/2026 |
| 2026-10-26 | ANA-DOC-0147 | Alta (lote del operador) | Operador (lote del bloque temático 2) | Subtema 13: Análisis de convergencia tecnológica — enlace y acceso libre verificados el 26/10/2026 |
| 2026-10-26 | ANA-DOC-0148 | Alta (lote del operador) | Operador (lote del bloque temático 2) | Subtema 14: Análisis de escenarios futuros — enlace y acceso libre verificados el 26/10/2026 |
| 2026-10-26 | ANA-DOC-0149 | Alta (lote del operador) | Operador (lote del bloque temático 2) | Subtema 14: Análisis de escenarios futuros — enlace y acceso libre verificados el 26/10/2026 |
| 2026-10-26 | ANA-DOC-0150 | Alta (lote del operador) | Operador (lote del bloque temático 2) | Subtema 14: Análisis de escenarios futuros — enlace y acceso libre verificados el 26/10/2026 |
| 2026-10-26 | ANA-DOC-0151 | Alta (lote del operador) | Operador (lote del bloque temático 2) | Subtema 14: Análisis de escenarios futuros — enlace y acceso libre verificados el 26/10/2026 |
| 2026-10-26 | ANA-DOC-0152 | Alta (lote del operador, pendiente de acceso gratuito) | Operador (lote del bloque temático 2) | Subtema 14: Análisis de escenarios futuros — enlaces y metadatos verificados el 26/10/2026; peldaño legal por localizar (portal OCDE) |
| 2026-10-26 | ANA-DOC-0153 | Alta (lote del operador) | Operador (lote del bloque temático 2) | Subtema 14: Análisis de escenarios futuros — enlace y acceso libre verificados el 26/10/2026 |
| 2026-10-26 | ANA-DOC-0154 | Alta (lote del operador) | Operador (lote del bloque temático 2) | Subtema 14: Análisis de escenarios futuros — enlace y acceso libre verificados el 26/10/2026 |
| 2026-10-26 | ANA-DOC-0155 | Alta (lote del operador) | Operador (lote del bloque temático 2) | Subtema 14: Análisis de escenarios futuros — enlace y acceso libre verificados el 26/10/2026 |

## 5. Qué se registra y qué no

Se registra literatura académica y técnica de dominio que respalde afirmaciones del análisis de tendencias, obtenida por acceso legal y gratuito y verificada por el Documentador. No se registra: fuentes de mercado, opinión o actualidad (ámbito del «Registro de fuentes fiables»); metodología de búsqueda bibliográfica (ámbito del «Fondo metodológico»); conocimiento matemático al servicio del cálculo (ámbito de la «Documentación para el Motor»); datos de mercado como series o cotizaciones; y cualquier fuente que no supere el filtro de verificación. Ante la duda, no se registra.

## 6. Reglas de mantenimiento y ciclo de vida

1. **Revisión de primera petición**: en la primera petición de búsqueda que le haga el Buscador, el Documentador revisa el archivo completo —enlaces vivos, acceso gratuito vigente, DOI pendientes de las fichas 0005, 0007, 0009, 0010, 0011 y 0012—, clasifica y ordena las fuentes por prioridad para el Buscador y declara el resultado de la revisión.
2. **Ciclo DOC_MAINTENANCE** conforme al calendario que fije el operador (Anexo A): comprobación de vitalidad de enlaces, retractaciones y ediciones nuevas; corrección o eliminación de enlaces rotos con anotación; revalidación de estados.
3. **Reindexado** del índice temático y del mapa de coberturas tras cada incorporación relevante y en el ciclo programado; el índice queda siempre en el estado que refleja la última petición atendida.
4. **Degradación honesta**: si el mantenimiento no puede completarse por limitación del entorno, se declara la limitación y el servicio continúa con ella anotada.

## 7. Control de versiones del archivo


| Versión | Fecha | Cambio |

|---|---|---|

| 1.0 | 2026-10-25 | Primera emisión como plantilla de formato, vacía de contenido y de fuentes. |

| 2.0 | 2026-10-25 | Conversión a archivo operativo: carga de arranque con 12 fuentes reales verificadas dispuesta por el operador; prefijo de identificador ANA-DOC- fijado; alcance específico del Bloque A declarado. |
| 2.1 | 2026-10-25 | Anexo documental del operador: añadida la sección 8 «Fuentes fiables específicas de este archivo», con el canal de verificación y acceso por ficha (8.1) y los canales institucionales (8.2); identificadores verificados hoy para las fichas 0007, 0010 y 0011 y discrepancia de volumen anotada en la 0002. No altera el esquema 1.0 ni los datos de las fichas. |

| 2.2 | 2026-10-25 | Subsanación de errata en la ficha ANA-DOC-0002: corrección de la cita del volumen/número/páginas de Journal of Financial Economics y actualización del historial de cambios (4.6) y anexo (8.1). No altera el esquema 1.0 ni los datos de las demás fichas. |
| 2.3 | 2026-10-26 | Incorporación del lote de fuentes del bloque temático 1 (Economía y análisis macroeconómico) facilitado por el operador: 79 fichas nuevas (ANA-DOC-0013 a ANA-DOC-0091) tras verificación individual de cada enlace (activo + acceso libre) y contraste de títulos contra la fuente (HTTP, PDF, Crossref, OpenAlex, RePEc, índice de búsqueda), 50 propuestas del lote excluidas por no verificables (documentadas en 4.3), clasificación por 13 subtemas + transversal, 63 canales institucionales y taxonomía de 19 bloques registrada en 4.3. No altera el esquema 1.0 ni los datos de las fichas anteriores. |
| 2.4 | 2026-10-26 | Incorporación del lote de fuentes del bloque temático 2 (Análisis de tendencias y prospectiva) facilitado por el operador: 64 fichas nuevas (ANA-DOC-0092 a ANA-DOC-0155; 59 aprobadas y 5 «pendientes de acceso gratuito» por el control de acceso de la OCDE) tras verificación individual de cada enlace (activo + acceso libre) y contraste de títulos contra la fuente (HTTP, PDF con pdftotext, Crossref, DataCite, OpenAlex, NCBI eutils, API de arXiv, navegación e índice de búsqueda), 74 propuestas del lote excluidas por no verificables o de pago (documentadas en 4.3), clasificación por los 14 subtemas del bloque 2 y 17 canales institucionales nuevos registrados en 4.3. No altera el esquema 1.0 ni los datos de las fichas anteriores. |

| 2.5 | 2026-10-26 | Cambio de disposición de las fichas por disposición del operador: las 155 fichas pasan de la tabla vertical de campos al formato compacto de bloques de párrafos con campos etiquetados en negrita (convención 7), para contener la extensión y el peso del documento .docx ante la incorporación de nuevos lotes de fuentes. No altera el esquema 1.0: el conjunto de campos y los valores de cada ficha se conservan íntegros (conversión verificada campo a campo). |

| 2.6 | 2026-10-26 | Adenda V1.2 del Bloque A (aprobada por el operador y aplicada por paquete coordinado conforme al Documento 0, 5.3): las fichas admiten el estado «retirada» (convención 8) para la retirada lógica de fuentes por revisión de conjunto del Documentador (9.9 de su prompt); la retirada es siempre un cambio de estado trazable (entrada nueva con fecha y motivo en 4.6) y nunca un borrado físico ni una renumeración. No altera el esquema 1.0 ni los datos de las fichas. |
| 2.7 | 2026-10-31 | V2.7 · esquema ampliado con los cinco controles documentales de la óptima V2.0 (calidad metodológica, vigencia, reproducibilidad documental, limitaciones, contradicciones), definidos en la sección 4.2. No altera los datos de las fichas: las entradas existentes conservan su esquema (append-only, regla crítica R16) y los campos nuevos se cumplimentan en altas y en revisiones posteriores de cada ficha. |

## 8. Fuentes fiables específicas de este archivo

*(Anexo documental del operador, 25/10/2026.)* Este apartado reúne, para cada ficha del archivo, las fuentes fiables concretas donde se verifica la cita y se consulta el documento registrado. No sustituye al campo «DOI o identificador persistente y URL de acceso» de cada ficha: lo complementa como canal de verificación y acceso de lectura. Todos los enlaces listados se comprobaron el 25/10/2026. Los identificadores que las fichas declaran «no consultado en la carga de arranque» quedan aquí verificados por el operador para que el Documentador los absorba en la revisión de primera petición (sección 6, regla 1); las copias de lectura señaladas como candidatas no alteran el peldaño ni el estado de su ficha hasta que el Documentador las evalúe y registre el movimiento en el historial (4.6). En los ciclos DOC_MAINTENANCE, estos enlaces se revisan igual que los de las fichas.

### 8.1 Fuentes de verificación por ficha

| Ficha | Fuentes fiables específicas | Qué se verifica ahí |
|---|---|---|
| ANA-DOC-0001 — Jegadeesh y Titman (1993) | DOI: doi.org/10.1111/j.1540-6261.1993.tb04702.x (Wiley Online Library) · Copia de lectura (peldaño 3, ficha): bauer.uh.edu/rsusmel/phd/jegadeesh-titman93.pdf · Agregadores: IDEAS/RePEc y Google Scholar | Cita normalizada, DOI, licencia y copia de autor |
| ANA-DOC-0002 — Moskowitz, Ooi y Pedersen (2012) | DOI: doi.org/10.1016/j.jfineco.2011.11.003 (ScienceDirect) · PDF de autor: docs.lhpedersen.com/TimeSeriesMomentum.pdf (re-verificado) · Página AQR: aqr.com/Insights/Research/Journal-Article/Time-Series-Momentum · Versión de trabajo: SSRN abstract_id=2089463 · RePEc: ideas.repec.org/a/eee/jfinec/v104y2012i2p228-250.html | Cita, DOI, copia de autor y versión de trabajo. **Discrepancia resuelta (25/10/2026, V2.2)**: la ficha anotaba «vol. 120, n.º 2»; la verificación en RePEc/ScienceDirect confirmó vol. 104, n.º 2, págs. 228-250. La ficha quedó corregida ese mismo día, con entrada en el historial (4.6); esta anotación se conserva como evidencia de la verificación |
| ANA-DOC-0003 — Asness, Moskowitz y Pedersen (2013) | DOI: doi.org/10.1111/jofi.12021 (Wiley) · Postprint aceptado: repositorio institucional CBS (research.cbs.dk, ficha) · SSRN abstract_id=2174501 (ficha) | Cita, DOI y versión aceptada abierta |
| ANA-DOC-0004 — Hurst, Ooi y Pedersen (2017) | DOI: doi.org/10.3905/jpm.2017.44.1.015 (pm-research.com) · Versión de acceso gratuito: página AQR de la ficha · SSRN abstract_id=2993026 (ficha) | Cita, DOI y versión de lectura gratuita |
| ANA-DOC-0005 — Brock, Lakonishok y LeBaron (1992) | DOI: doi.org/10.1111/j.1540-6261.1992.tb04681.x (Wiley) · JSTOR: jstor.org/stable/2328994 (ficha, acceso por suscripción) · Para el peldaño legal pendiente: buscar copia de autor vía OpenAlex (método OA) en la primera revisión | Cita, DOI y localización; pendiente de acceso gratuito sin resolver |
| ANA-DOC-0006 — Sullivan, Timmermann y White (1999) | DOI: doi.org/10.1111/0022-1082.00163 (Wiley, ficha) · Versión de trabajo: LSE Research Online (eprint 119144, ficha) · Agregador: IDEAS/RePEc (handle bla:jfinan:v54y1999i5p1647-1691) | Cita, DOI y versión de trabajo abierta |
| ANA-DOC-0007 — Lo, Mamaysky y Wang (2000) | **DOI verificado hoy**: 10.1111/0022-1082.00265 (Wiley Online Library) · Versión de trabajo: NBER Working Paper n.º 7613 (nber.org/papers/w7613) · Copia de lectura candidata (peldaño 3): página de curso universitario cis.upenn.edu/~mkearns/teaching/cis700/lo.pdf · RePEc: ideas.repec.org/a/bla/jfinan/v55y2000i4p1705-1765.html | DOI que la ficha deja pendiente; localización NBER; copia de autor a evaluar por el Documentador |
| ANA-DOC-0008 — Menkhoff, Sarno, Schmeling y Schrimpf (2012) | DOI: doi.org/10.1016/j.jfineco.2012.06.009 (ScienceDirect, ficha) · Versión aceptada: openaccess.city.ac.uk/id/eprint/3296 (ficha) · Versión de trabajo: BIS Working Papers n.º 366 (bis.org) | Cita, DOI, versión aceptada y de trabajo |
| ANA-DOC-0009 — Faber (2007) | SSRN abstract_id=962461 (ficha, re-verificado) · Copia del propio autor: mebfaber.com/wp-content/uploads/2016/05/SSRN-id962461.pdf · Editorial: pm-research.com (The Journal of Wealth Management, primavera 2007) | Cita y paginación editorial (JWM 9(4), 69-79); el DOI editorial no se asegura aquí: completar en la revisión si Crossref lo resuelve |
| ANA-DOC-0010 — Han, Zhou y Zhu (2016) | **DOI verificado hoy**: 10.1016/j.jfineco.2016.01.029 (paginación confirmada: 122(2), 352-375) · ScienceDirect PII S0304405X16301271 (ficha) · Versión de trabajo: SSRN abstract_id=2182667 | DOI y paginación que la ficha deja pendientes; versión de trabajo |
| ANA-DOC-0011 — Levy (1967) | **DOI verificado hoy**: 10.1111/j.1540-6261.1967.tb00295.x (Wiley) · RePEc: ideas.repec.org/a/bla/jfinan/v22y1967i4p595-610.html · Copia de lectura candidata (peldaño 3): technicalanalysis.org.uk/history/Levy67.pdf | DOI que la ficha deja pendiente; copia histórica de acceso público a evaluar por el Documentador |
| ANA-DOC-0012 — Antonacci (2014) | Página editorial: mheducation.com (ficha de producto «Dual Momentum Investing», verificada hoy) · Sitio del autor: optimalmomentum.com, con sus trabajos de base (p. ej. «Risk Premia Harvesting Through Dual Momentum», SSRN abstract_id=2042750) | Existencia editorial y obra del autor; el ISBN no se asegura aquí (no verificado) |

### 8.2 Canales institucionales de verificación (todo el archivo)

| Canal | Uso en este archivo |
|---|---|
| doi.org (Crossref) | Resolver cualquier DOI de las fichas y de esta sección; metadatos normalizados de la publicación |
| IDEAS/RePEc y EconPapers | Handles verificados por ficha en la tabla 8.1; citas, versiones alternativas y descargas listadas por el propio RePEc |
| OpenAlex | Metadatos abiertos y detección de acceso abierto (método OA) para las cinco fichas pendientes de acceso gratuito |
| Google Scholar | Métricas de citación y versiones de autor adicionales |
| JSTOR | Localización por identificador estable de los clásicos con acceso por suscripción (fichas 0005, 0007, 0011) |
| SSRN | Versiones de trabajo y preprints de autor citados en la tabla 8.1 |
| Retraction Watch Database (retractionwatch.com) | Comprobación de retractaciones en los ciclos DOC_MAINTENANCE; cualquier retractación de una ficha se registra con fecha y motivo |
