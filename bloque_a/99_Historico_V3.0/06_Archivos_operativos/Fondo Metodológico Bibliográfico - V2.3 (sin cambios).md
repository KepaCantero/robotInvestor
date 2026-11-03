# Fondo Metodológico Bibliográfico

**Proyecto Robot Investor · Bloque A — Analizador de Tendencias de Inversión · Ecosistema Robot Investor**

**Archivo operativo · Versión 2.3 · 26/10/2026 · Estado: EN OPERACIÓN (carga de arranque de 10 entradas de corpus y 4 criterios destilados, 25/10/2026; estado «descartada» precisado por la adenda V1.2 del Bloque A, 26/10/2026)**

Este archivo está listo para su uso. Contiene su estructura completa, sus reglas y una **carga de arranque de 10 entradas de corpus reales verificadas y 4 criterios destilados**, dispuesta por el operador el 25/10/2026, que muestra cómo se introducen las fuentes y cómo se destilan criterios a partir de ellas (entradas y criterios en formato compacto desde el 26/10/2026). A partir de aquí, el mantenimiento corresponde al agente propietario conforme a los contratos del Documento 0. La ubicación física y la tecnología del archivo siguen siendo parámetros del operador (Documento 0, Anexo A): este archivo fija la propiedad y la estructura, no la tecnología. La sección 8 añade el anexo del operador con las fuentes fiables específicas de verificación y acceso de cada ficha o entrada registrada (25/10/2026). El 26/10/2026, por disposición del operador, las entradas de corpus y los criterios destilados se convirtieron al formato compacto (bloques de párrafos con los campos etiquetados en negrita, en sustitución de la tabla vertical de campos) para contener la extensión y el peso del documento Word ante nuevas altas: el conjunto de campos y los valores no varían (conversión verificada campo a campo). Por la adenda V1.2 del Bloque A (26/10/2026), el criterio del estado «descartada» de las entradas de corpus queda precisado (convención 9): bajo aporte relativo o sustitución, con salida siempre lógica y trazable, nunca un borrado.

---

## 1. Rol del archivo en la arquitectura del Bloque A

El «Fondo Metodológico Bibliográfico» (nombre canónico en el inventario del Documento 0, 2.3: «Fondo metodológico de búsqueda bibliográfica») es el archivo del Bloque A que mejora, con evidencia, cómo se busca: un corpus académico sobre metodología de búsqueda bibliográfica profesional —cómo se planifica, ejecuta y verifica una búsqueda rigurosa— y una capa de criterios destilados, es decir, reglas operativas extraídas de ese corpus y aplicables a los protocolos de búsqueda del Documentador y a los filtros del Buscador Avanzado. Fue definido en la Versión óptima V1 y está ACTIVADO desde el 23/10/2026 (procedimiento 5.5 del Documento 0).

A diferencia del resto de archivos del bloque, este no contiene conocimiento financiero ni de dominio: contiene metodología de búsqueda y nada más —ni tesis de inversión, ni datos de mercado, ni material de opinión—. Su papel es doble: hace que las búsquedas del bloque sean mejores (sus criterios vigentes se aplican al planificar cada estrategia) y las hace trazables (todo criterio cita las entradas de corpus verificadas de las que procede, y el conjunto viaja en los paquetes de servicio como material auditable).

**Alcance ecosistémico — archivo único para todos los bloques.** Por decisión del operador (25/10/2026, Documento 0, Anexo H), este archivo es el archivo de consulta metodológica compartido del ecosistema Robot Investor y **será utilizado también en los bloques posteriores**: no se crearán fondos metodológicos paralelos ni instancias de consulta propias en otros bloques. Los agentes **Documentador** y **Buscador Avanzado** de cualquier bloque de la arquitectura lo consultan en solo lectura, por acceso a archivo, conforme a la matriz de archivos y a los protocolos de cada bloque, sin mensajes agente a agente y sin contrato del catálogo; la escritura no sale del Documentador para el Analizador (Bloque A). El Documento 0 de cada bloque posterior declarará esta consulta en su matriz de archivos como consulta ecosistémica al Fondo del Bloque A.

Su propietario es el **Documentador para el Analizador**, que realiza el registro, el mantenimiento y la consulta; lo consultan en solo lectura el **Buscador Avanzado** (para aplicar sus criterios a sus filtros), el **Documentador para el Motor de Cálculo Avanzado** (9.7 de su prompt) y, en el propio bloque, el Orquestador y el Auditor por extractos en paquetes. Se rige por un esquema propio de tres registros —entrada de corpus, criterio destilado e índice del Fondo— y por una política de mantenimiento mensual (ciclo FONDO_MAINTENANCE), con reindexado trimestral. La regla central que lo gobierna es «sin criterio sin fuente»: el conocimiento interno del modelo nunca es fuente de un criterio.

## 2. Ficha de uso para el agente

| Campo | Detalle |
|---|---|
| Nombre canónico (Documento 0, 2.3) | «Fondo metodológico de búsqueda bibliográfica» |
| Naturaleza del archivo | Corpus metodológico verificado + capa de criterios destilados; archivo de mejora y trazabilidad de la búsqueda, no de contenido financiero; archivo de consulta metodológica compartido del ecosistema Robot Investor |
| Alcance del archivo | Ecosistémico: archivo único para todos los bloques. Será utilizado en los bloques posteriores (B, C…) por sus agentes Documentador y Buscador Avanzado en solo lectura, sin creación de archivos ni instancias paralelas (decisión del operador, 25/10/2026) |
| Propietario (escritura y mantenimiento) | Documentador para el Analizador |
| Lectores autorizados | Documentador para el Analizador (consulta operativa); Buscador Avanzado (solo lectura, para sus filtros); Documentador para el Motor de Cálculo Avanzado (solo lectura, 9.7 de su prompt); Orquestador y Auditor (extractos en paquetes); y, por declaración ecosistémica, los agentes Documentador y Buscador Avanzado de cualquier bloque de la arquitectura (solo lectura) |
| Cuándo leerlo | El Documentador para el Analizador, al planificar cada estrategia de búsqueda (para aplicar los criterios vigentes); el Buscador Avanzado, antes de aplicar sus filtros; el Documentador para el Motor, al planificar sus búsquedas bibliográficas matemáticas; y, en general, cualquier agente consultor —del bloque o de bloques posteriores—, antes de aplicar un criterio o proponer un alta |
| Cuándo escribir en él | En el ciclo FONDO_MAINTENANCE (mensual): altas de corpus con verificación completa, destilación y revisión de criterios, regeneración del índice; y en las altas puntuales verificadas. Único escritor en todo el ecosistema: el Documentador para el Analizador |
| Reglas de escritura | Solo añadir: toda modificación produce una versión nueva del registro con fecha y motivo, nunca borrado ni sobrescritura; un criterio en revisión o derogado no alimenta estrategias |
| Contratos implicados | CT-02 (peticiones de conocimiento, Buscador → Documentador); CT-05 (paquete de servicio, Documentador → Orquestador); CT-09 (guías para agentes de apoyo); consulta propia del Buscador Avanzado dentro de su protocolo (6.7 de su prompt). La consulta ecosistémica no añade contratos: es acceso a archivo |
| Relación con otros archivos | Segundo archivo propio del Documentador junto a la «Documentación para tendencias de inversión»; se coordina con la «Documentación para el Motor» (su homólogo en el ámbito matemático, 9.7 del prompt del Documentador para el Motor), también de alcance ecosistémico |
| Material auditable | Sí: registros, altas y versiones viajan en el paquete de servicio (CT-05) con toda la trazabilidad cuando la estrategia de búsqueda sea objeto de revisión |
| Estado de esta copia | Archivo operativo en arranque; esquema 1.0; carga de arranque del 25/10/2026 (10 entradas de corpus y 4 criterios) |

## 3. Convenciones de formato

1. **Identificadores únicos e inmutables** con prefijo `fondo_`: `fondo_entry_id` para las entradas de corpus (fondo_entry_001, fondo_entry_002…) y `fondo_criterion_id` para los criterios destilados (fondo_criterion_001, fondo_criterion_002…).
2. **Fechado ISO 8601** en todos los campos de fecha.
3. **Registros de solo añadir**, como en la Documentación: los cambios de estado son entradas nuevas con fecha y motivo, nunca borrados ni sobrescrituras; toda modificación de un criterio produce una versión nueva del criterio.
4. **Sin criterio sin fuente**: cada criterio destilado cita, al menos, una entrada de corpus verificada de la que procede; el conocimiento del modelo nunca es fuente de un criterio.
5. **Sin entrada sin verificación**: ninguna entrada de corpus se da de alta sin texto completo obtenido legalmente y sin superar el filtro de verificación del Documentador (Anexo B de su prompt), con anotación del nivel y de las comprobaciones omitidas.
6. **Campo no disponible se declara**: «desconocido», «no aplicable» o «no consultado en la carga de arranque», nunca inventado.
7. **Vigencia**: solo los criterios en estado «vigente» alimentan estrategias y filtros; un criterio en revisión o derogado se consulta pero no se aplica.
8. **Formato compacto de ficha (desde el 26/10/2026, por disposición del operador)**: las entradas de corpus y los criterios destilados se disponen como bloques de párrafos con los campos etiquetados en negrita, agrupados por temas, en sustitución de la tabla vertical de campos. El conjunto de campos y sus valores son los del esquema 1.0: solo cambia la disposición, verificada campo a campo en la conversión. Las entradas y criterios nuevos se incorporan directamente en formato compacto.
9. **Criterio del estado «descartada» (desde el 26/10/2026, adenda V1.2 del Bloque A)**: una entrada de corpus pasa a «descartada» por bajo aporte relativo frente a otras entradas de su ámbito metodológico o por sustitución, conforme a la revisión de conjunto (9.9 del prompt del Documentador); hace las veces del estado «retirada» del resto de archivos. La salida es siempre lógica y trazable: entrada nueva con fecha y motivo en el registro de altas, versiones y cambios de estado (4.4), la entrada permanece en el archivo y nunca se borra ni se renumera. Los criterios destilados mantienen sus estados (vigente, en revisión, derogado).

## 4. Estructura del archivo

El Fondo se compone de **tres registros**, en este orden. La carga de arranque del operador (25/10/2026) rellena los tres registros; su trazabilidad completa queda en el Registro 3.

**Nota sobre la carga de arranque.** Las entradas de corpus siguientes se dispusieron a partir de citas verificadas el 25/10/2026 en fuentes bibliográficas públicas (DOI resolutivos, repositorios académicos y páginas editoriales). Ningún dato se ha inventado: donde un dato no se consultó, el campo lo declara. Las dos entradas en revisión ilustran el tratamiento honesto de una fuente conocida cuyo texto completo aún no se ha obtenido por vía legal gratuita.

### 4.1 Índice del Fondo (ficha maestra)

| Campo | Valor |
|---|---|
| fondo_schema_version | 1.0 |
| Recuentos por tipo de registro | 10 entradas de corpus · 4 criterios destilados · 15 movimientos en el diario |
| Entradas de corpus por ámbito metodológico | Planificación (4) · Consultas (1) · Filtrado (2) · Gestión del corpus (1) · Verificación y reproducibilidad (1) · Métricas (1) |
| Entradas de corpus por estado | 8 vigentes · 2 en revisión · 0 descartadas |
| Criterios por fase de aplicación | Planificación (1) · Consultas (1) · Filtrado (1) · Gestión del corpus (1) |
| Criterios por estado y fuerza | 4 vigentes (3 obligatorios, 1 recomendado) |
| Listado por fase con criterios vigentes y fuentes | Planificación → fondo_criterion_001 (fondo_entry_001, 002, 005) · Consultas → fondo_criterion_002 (fondo_entry_003, 004, 005) · Filtrado → fondo_criterion_003 (fondo_entry_006) · Gestión del corpus → fondo_criterion_004 (fondo_entry_007, 008) |
| Fecha de regeneración | 2026-10-25 (carga de arranque) |
| Pendientes declarados | Resolver el acceso legal gratuito de fondo_entry_009 y fondo_entry_010 (en revisión); completar los datos «no consultados» de las fichas 003, 004 y 010 (URL/DOI) |

### 4.2 Registro 1 — Entradas de corpus

Una entrada por fuente metodológica verificada (campos del esquema 9.7 del Anexo D del Documentador para el Analizador), dispuesta en formato compacto (convención 8): un bloque de párrafos por entrada con los campos etiquetados en negrita.

#### fondo_entry_001 — PRISMA 2020

*Identificación y acceso.* **fondo_entry_id:** fondo_entry_001 · **Cita normalizada:** Page, M. J., McKenzie, J. E., Bossuyt, P. M., et al. (2021). The PRISMA 2020 statement: an updated guideline for reporting systematic reviews. BMJ, 372, n71. · **DOI o identificador persistente y URL de acceso:** DOI: 10.1136/bmj.n71 · Acceso gratuito en la editorial (bmj.com) · **Tipo de fuente:** Artículo revisado por pares (declaración de consenso) · **Año:** 2021 · **Idioma:** Inglés · **Ámbito metodológico:** Planificación

*Contenido.* **Ficha metodológica:** Declara el estándar internacional de reporte de revisiones sistemáticas: diagrama de flujo de identificación, cribado y inclusión de resultados, y lista de comprobación de 27 puntos. Da al Fondo el modelo de trazabilidad del proceso de búsqueda: qué se buscó, dónde, con qué ecuación y qué se descartó.

*Verificación y estado.* **Resultado del filtro de verificación:** Completa (carga de arranque): cita, DOI y acceso abierto verificados el 25/10/2026; comprobaciones omitidas: lectura del texto completo por el Documentador, pendiente de la primera revisión · **Criterios derivados:** fondo_criterion_001 · **Fecha de alta:** 2026-10-25 · **Última revisión:** 2026-10-25 · **Versión de ficha:** 1.0 · **Estado:** Vigente


#### fondo_entry_002 — PRISMA 2009

*Identificación y acceso.* **fondo_entry_id:** fondo_entry_002 · **Cita normalizada:** Moher, D., Liberati, A., Tetzlaff, J., Altman, D. G., y The PRISMA Group (2009). Preferred Reporting Items for Systematic Reviews and Meta-Analyses: The PRISMA Statement. PLoS Medicine, 6(7), e1000097. · **DOI o identificador persistente y URL de acceso:** DOI: 10.1371/journal.pmed.1000097 · Acceso abierto en la editorial (journals.plos.org) · **Tipo de fuente:** Artículo revisado por pares (declaración de consenso) · **Año:** 2009 · **Idioma:** Inglés · **Ámbito metodológico:** Planificación

*Contenido.* **Ficha metodológica:** Versión previa de la declaración PRISMA. Se conserva por valor de compatibilidad: mucha literatura aplicada aún se documenta contra PRISMA 2009, y conocer sus 27 puntos y su diagrama de flujo de cuatro fases permite leer esa literatura con criterio. Actualizada materialmente por fondo_entry_001 (PRISMA 2020); para reporte nuevo se aplica la versión 2020.

*Verificación y estado.* **Resultado del filtro de verificación:** Completa (carga de arranque): cita, DOI y acceso abierto verificados el 25/10/2026; comprobaciones omitidas: lectura del texto completo por el Documentador · **Criterios derivados:** fondo_criterion_001 · **Fecha de alta:** 2026-10-25 · **Última revisión:** 2026-10-25 · **Versión de ficha:** 1.0 · **Estado:** Vigente


#### fondo_entry_003 — Kitchenham y Charters (2007)

*Identificación y acceso.* **fondo_entry_id:** fondo_entry_003 · **Cita normalizada:** Kitchenham, B., y Charters, S. (2007). Guidelines for performing Systematic Literature Reviews in Software Engineering. Technical Report EBSE-2007-01, Keele University y University of Durham. · **DOI o identificador persistente y URL de acceso:** Sin DOI (informe técnico). URL: disponible legalmente en repositorios universitarios abiertos; URL concreta no consultada en la carga de arranque (fijarla en la primera revisión) · **Tipo de fuente:** Informe técnico institucional · **Año:** 2007 · **Idioma:** Inglés · **Ámbito metodológico:** Consultas

*Contenido.* **Ficha metodológica:** Guía operativa completa de la revisión sistemática aplicada: definición de preguntas de investigación, estrategia de búsqueda por fuentes y cadenas, criterios de inclusión y exclusión, extracción de datos y control de calidad. Complementa a PRISMA (que reporta resultados) con el procedimiento paso a paso (que los produce).

*Verificación y estado.* **Resultado del filtro de verificación:** Completa (carga de arranque): cita y existencia del informe verificadas el 25/10/2026; URL concreta no consultada; comprobaciones omitidas: localización y lectura de la copia de referencia · **Criterios derivados:** fondo_criterion_002 · **Fecha de alta:** 2026-10-25 · **Última revisión:** 2026-10-25 · **Versión de ficha:** 1.0 · **Estado:** Vigente


#### fondo_entry_004 — Webster y Watson (2002)

*Identificación y acceso.* **fondo_entry_id:** fondo_entry_004 · **Cita normalizada:** Webster, J., y Watson, R. T. (2002). Analyzing the Past to Prepare for the Future: Writing a Literature Review. MIS Quarterly, 26(2), xiii-xxiii. · **DOI o identificador persistente y URL de acceso:** Sin DOI consultado en la carga de arranque. Acceso: copias de acceso público en páginas universitarias; URL concreta a fijar en la primera revisión · **Tipo de fuente:** Artículo revisado por pares (guía editorial) · **Año:** 2002 · **Idioma:** Inglés · **Ámbito metodológico:** Consultas

*Contenido.* **Ficha metodológica:** Guía clásica de redacción de revisiones de literatura; su aportación operativa al Fondo es el modelo de búsqueda por concepto-centrismo y las técnicas de búsqueda hacia atrás (referencias de los documentos centrales) y hacia adelante (citas que reciben), pilares de cualquier estrategia completa.

*Verificación y estado.* **Resultado del filtro de verificación:** Completa (carga de arranque): cita verificada el 25/10/2026; URL de la copia de referencia no consultada; comprobaciones omitidas: localización de copia estable y lectura del texto completo · **Criterios derivados:** fondo_criterion_002 · **Fecha de alta:** 2026-10-25 · **Última revisión:** 2026-10-25 · **Versión de ficha:** 1.0 · **Estado:** Vigente


#### fondo_entry_005 — Okoli y Schabram (2010)

*Identificación y acceso.* **fondo_entry_id:** fondo_entry_005 · **Cita normalizada:** Okoli, C., y Schabram, K. (2010). A Guide to Conducting a Systematic Literature Review of Information Systems Research. Communications of the Association for Information Systems, 26, artículo 18. · **DOI o identificador persistente y URL de acceso:** DOI: 10.17705/1CAIS.02618 · SSRN: papers.ssrn.com/sol3/papers.cfm?abstract_id=1954824 (descarga gratuita con registro) · **Tipo de fuente:** Artículo revisado por pares (guía metodológica) · **Año:** 2010 · **Idioma:** Inglés · **Ámbito metodológico:** Planificación

*Contenido.* **Ficha metodológica:** Guía de revisión sistemática en diez pasos, desde el propósito hasta la presentación, con recomendaciones explícitas sobre ecuaciones de búsqueda y documentación del proceso. Es el puente entre PRISMA (médica) y la práctica en dominios de información y negocios.

*Verificación y estado.* **Resultado del filtro de verificación:** Completa (carga de arranque): cita, DOI y página SSRN verificadas el 25/10/2026; comprobaciones omitidas: lectura del texto completo por el Documentador · **Criterios derivados:** fondo_criterion_001, fondo_criterion_002 · **Fecha de alta:** 2026-10-25 · **Última revisión:** 2026-10-25 · **Versión de ficha:** 1.0 · **Estado:** Vigente


#### fondo_entry_006 — Wohlin (2014)

*Identificación y acceso.* **fondo_entry_id:** fondo_entry_006 · **Cita normalizada:** Wohlin, C. (2014). Guidelines for Snowballing in Systematic Literature Studies and a Replication in Software Engineering. Proceedings of EASE '14, ACM, Londres. · **DOI o identificador persistente y URL de acceso:** DOI: 10.1145/2601248.2601268 · PDF de autor: wohlin.eu/ease14.pdf (acceso gratuito verificado) · **Tipo de fuente:** Artículo de congreso revisado por pares · **Año:** 2014 · **Idioma:** Inglés · **Ámbito metodológico:** Filtrado

*Contenido.* **Ficha metodológica:** Directrices operativas de la bola de nieve como estrategia de búsqueda: iteraciones hacia atrás y hacia adelante, criterios de inclusión por iteración y reglas de parada. Legitima y disciplina el snowballing dentro de las estrategias del bloque, con trazabilidad de cada iteración.

*Verificación y estado.* **Resultado del filtro de verificación:** Completa (carga de arranque): cita, DOI y PDF de autor verificados el 25/10/2026; comprobaciones omitidas: lectura del texto completo por el Documentador · **Criterios derivados:** fondo_criterion_003 · **Fecha de alta:** 2026-10-25 · **Última revisión:** 2026-10-25 · **Versión de ficha:** 1.0 · **Estado:** Vigente


#### fondo_entry_007 — Ouzzani et al. (2016)

*Identificación y acceso.* **fondo_entry_id:** fondo_entry_007 · **Cita normalizada:** Ouzzani, M., Hammady, H., Fedorowicz, Z., y Elmagarmid, A. (2016). Rayyan—a web and mobile app for systematic reviews. Systematic Reviews, 5, 210. · **DOI o identificador persistente y URL de acceso:** DOI: 10.1186/s13643-016-0384-4 · Acceso abierto en la editorial (systematicreviewsjournal.biomedcentral.com) · **Tipo de fuente:** Artículo revisado por pares (herramienta) · **Año:** 2016 · **Idioma:** Inglés · **Ámbito metodológico:** Gestión del corpus

*Contenido.* **Ficha metodológica:** Describe el flujo de gestión del cribado de una revisión: deduplicación, cribado por títulos y resúmenes con resaltado automático de razones, resolución de conflictos y registro de decisiones. Da al Fondo el vocabulario de gestión del corpus (deduplicación, cribado, conflictos) aplicable a sus propios registros.

*Verificación y estado.* **Resultado del filtro de verificación:** Completa (carga de arranque): cita, DOI y acceso abierto verificados el 25/10/2026; comprobaciones omitidas: lectura del texto completo por el Documentador · **Criterios derivados:** fondo_criterion_004 · **Fecha de alta:** 2026-10-25 · **Última revisión:** 2026-10-25 · **Versión de ficha:** 1.0 · **Estado:** Vigente


#### fondo_entry_008 — Sandve et al. (2013)

*Identificación y acceso.* **fondo_entry_id:** fondo_entry_008 · **Cita normalizada:** Sandve, G. K., Nekrutenko, A., Taylor, J., y Hovig, E. (2013). Ten Simple Rules for Reproducible Computational Research. PLoS Computational Biology, 9(10), e1003285. · **DOI o identificador persistente y URL de acceso:** DOI: 10.1371/journal.pcbi.1003285 · Acceso abierto en la editorial (journals.plos.org) · **Tipo de fuente:** Artículo revisado por pares (guía) · **Año:** 2013 · **Idioma:** Inglés · **Ámbito metodológico:** Verificación y reproducibilidad

*Contenido.* **Ficha metodológica:** Diez reglas de reproducibilidad computacional (versionar todo, registrar cada resultado intermedio, externalizar scripts y datos, no sobrescribir resultados). Aplicadas al proceso documental del bloque, garantizan que cualquier búsqueda y verificación pueda reconstruirse sin ayuda del agente que la ejecutó.

*Verificación y estado.* **Resultado del filtro de verificación:** Completa (carga de arranque): cita, DOI y acceso abierto verificados el 25/10/2026; comprobaciones omitidas: lectura del texto completo por el Documentador · **Criterios derivados:** fondo_criterion_004 · **Fecha de alta:** 2026-10-25 · **Última revisión:** 2026-10-25 · **Versión de ficha:** 1.0 · **Estado:** Vigente


#### fondo_entry_009 — Harzing y Alakangas (2016)

*Identificación y acceso.* **fondo_entry_id:** fondo_entry_009 · **Cita normalizada:** Harzing, A.-W., y Alakangas, S. (2016). Google Scholar, Scopus and the Web of Science: a longitudinal and cross-disciplinary comparison. Scientometrics, 106(2), 787-804. · **DOI o identificador persistente y URL de acceso:** DOI: 10.1007/s11192-015-1798-9 · Editorial: link.springer.com (acceso por suscripción) · **Tipo de fuente:** Artículo revisado por pares · **Año:** 2016 · **Idioma:** Inglés · **Ámbito metodológico:** Métricas

*Contenido.* **Ficha metodológica:** Compara longitudinalmente Google Scholar, Scopus y Web of Science por disciplina, con implicaciones directas para decidir qué métricas de citación son fiables en cada ámbito y qué cobertura esperar de cada base. Cuando el bloque necesite consultar métricas de citación de una fuente (campo 19 de la ficha de la Documentación), esta entrada guiará la elección de la base.

*Verificación y estado.* **Resultado del filtro de verificación:** Ligera (carga de arranque): cita y DOI verificados el 25/10/2026; texto completo no obtenido (peldaño 5 de la escalera); comprobaciones omitidas: lectura del contenido completo · **Criterios derivados:** Ninguno aún (destilación pendiente de acceso al texto completo) · **Fecha de alta:** 2026-10-25 · **Última revisión:** 2026-10-25 · **Versión de ficha:** 1.0 · **Estado:** En revisión


#### fondo_entry_010 — Goodman (1961)

*Identificación y acceso.* **fondo_entry_id:** fondo_entry_010 · **Cita normalizada:** Goodman, L. A. (1961). Snowball Sampling. The Annals of Mathematical Statistics, 32(1), 148-170. · **DOI o identificador persistente y URL de acceso:** DOI: no consultado en la carga de arranque · Localización: JSTOR (acceso por suscripción) · **Tipo de fuente:** Artículo revisado por pares (origen histórico) · **Año:** 1961 · **Idioma:** Inglés · **Ámbito metodológico:** Filtrado

*Contenido.* **Ficha metodológica:** Formulación original matemática del muestreo por bola de nieve, del que procede la técnica de expansión del corpus por referencias. Su valor es fundacional: fundamenta el criterio fondo_criterion_003 junto a las directrices modernas de Wohlin (fondo_entry_006).

*Verificación y estado.* **Resultado del filtro de verificación:** Ligera (carga de arranque): cita y localización JSTOR verificadas el 25/10/2026; DOI no consultado; texto completo no obtenido (peldaño 5 de la escalera); comprobaciones omitidas: DOI, lectura del contenido completo · **Criterios derivados:** Ninguno aún (destilación pendiente de acceso al texto completo) · **Fecha de alta:** 2026-10-25 · **Última revisión:** 2026-10-25 · **Versión de ficha:** 1.0 · **Estado:** En revisión


### 4.3 Registro 2 — Criterios destilados

Una entrada por regla operativa (campos del esquema 9.7 del Anexo D del Documentador para el Analizador). Regla «sin criterio sin fuente»: solo destilan desde entradas vigentes. Desde el 26/10/2026 los criterios se disponen en formato compacto (convención 8): un bloque de párrafos por criterio con los campos etiquetados en negrita.

#### fondo_criterion_001

*Criterio.* **fondo_criterion_id:** fondo_criterion_001 · **Texto operativo:** Documenta toda estrategia de búsqueda antes de ejecutarla: ecuación de búsqueda, bases consultadas, límites temporales y de idioma, y fecha de ejecución, de modo que otra agencia pueda repetirla idéntica y auditar lo descartado.

*Aplicación y estado.* **Fase de aplicación:** Planificación · **Fuerza:** Obligatorio · **Fuentes:** fondo_entry_001 (PRISMA 2020), fondo_entry_002 (PRISMA 2009), fondo_entry_005 (Okoli y Schabram 2010) · **Estado:** Vigente · **Fecha de alta:** 2026-10-25 · **Última revisión:** 2026-10-25 · **Versión del criterio:** 1.0


#### fondo_criterion_002

*Criterio.* **fondo_criterion_id:** fondo_criterion_002 · **Texto operativo:** Completa toda búsqueda en bases con búsqueda reversa (referencias de los documentos centrales) y búsqueda hacia adelante (citas que reciben); registra ambas pasadas en la estrategia.

*Aplicación y estado.* **Fase de aplicación:** Consultas · **Fuerza:** Obligatorio · **Fuentes:** fondo_entry_003 (Kitchenham y Charters 2007), fondo_entry_004 (Webster y Watson 2002), fondo_entry_005 (Okoli y Schabram 2010) · **Estado:** Vigente · **Fecha de alta:** 2026-10-25 · **Última revisión:** 2026-10-25 · **Versión del criterio:** 1.0


#### fondo_criterion_003

*Criterio.* **fondo_criterion_id:** fondo_criterion_003 · **Texto operativo:** Usa la bola de nieve para ampliar o sustituir la búsqueda en bases cuando el corpus sea pequeño o muy interconectado: itera hacia atrás y hacia adelante con criterios de inclusión explícitos por iteración y una regla de parada declarada.

*Aplicación y estado.* **Fase de aplicación:** Filtrado · **Fuerza:** Recomendado · **Fuentes:** fondo_entry_006 (Wohlin 2014) · **Estado:** Vigente · **Fecha de alta:** 2026-10-25 · **Última revisión:** 2026-10-25 · **Versión del criterio:** 1.0


#### fondo_criterion_004

*Criterio.* **fondo_criterion_id:** fondo_criterion_004 · **Texto operativo:** Registra cada entrada del corpus con su fecha de consulta, la versión del documento utilizada y la trazabilidad suficiente para reproducir el cribado: deduplica, anota las decisiones de inclusión y no sobrescribas ningún resultado intermedio.

*Aplicación y estado.* **Fase de aplicación:** Gestión del corpus · **Fuerza:** Obligatorio · **Fuentes:** fondo_entry_007 (Ouzzani et al. 2016), fondo_entry_008 (Sandve et al. 2013) · **Estado:** Vigente · **Fecha de alta:** 2026-10-25 · **Última revisión:** 2026-10-25 · **Versión del criterio:** 1.0


### 4.4 Registro 3 — Altas, versiones y cambios de estado

Diario de solo añadir (fecha; identificador afectado; movimiento; agente responsable; motivo).

| Fecha | Identificador | Movimiento | Agente responsable | Motivo |
|---|---|---|---|---|
| 2026-10-25 | fondo_entry_001 | Alta de corpus | Operador (carga de arranque) | Estándar de reporte y trazabilidad de revisiones |
| 2026-10-25 | fondo_entry_002 | Alta de corpus | Operador (carga de arranque) | Versión previa de PRISMA; compatibilidad con literatura aplicada |
| 2026-10-25 | fondo_entry_003 | Alta de corpus | Operador (carga de arranque) | Guía operativa de revisión sistemática |
| 2026-10-25 | fondo_entry_004 | Alta de corpus | Operador (carga de arranque) | Búsqueda hacia atrás y hacia adelante |
| 2026-10-25 | fondo_entry_005 | Alta de corpus | Operador (carga de arranque) | Guía de revisión sistemática en dominio de información |
| 2026-10-25 | fondo_entry_006 | Alta de corpus | Operador (carga de arranque) | Directrices de snowballing |
| 2026-10-25 | fondo_entry_007 | Alta de corpus | Operador (carga de arranque) | Gestión del cribado y deduplicación |
| 2026-10-25 | fondo_entry_008 | Alta de corpus | Operador (carga de arranque) | Reproducibilidad computacional del proceso documental |
| 2026-10-25 | fondo_entry_009 | Alta de corpus (en revisión) | Operador (carga de arranque) | Métricas de citación; resolver acceso legal gratuito |
| 2026-10-25 | fondo_entry_010 | Alta de corpus (en revisión) | Operador (carga de arranque) | Origen histórico del snowballing; resolver acceso legal gratuito |
| 2026-10-25 | fondo_criterion_001 | Destilación | Operador (carga de arranque) | Criterio de planificación documentada de búsquedas |
| 2026-10-25 | fondo_criterion_002 | Destilación | Operador (carga de arranque) | Criterio de búsqueda reversa y hacia adelante |
| 2026-10-25 | fondo_criterion_003 | Destilación | Operador (carga de arranque) | Criterio de uso disciplinado del snowballing |
| 2026-10-25 | fondo_criterion_004 | Destilación | Operador (carga de arranque) | Criterio de trazabilidad y reproducibilidad del corpus |
| 2026-10-25 | (índice) | Regeneración del índice | Operador (carga de arranque) | Primera regeneración, con la carga de arranque |

## 5. Qué se registra y qué no

Se registra metodología de búsqueda bibliográfica profesional: cómo se planifica una búsqueda, cómo se formulan consultas, cómo se filtran y verifican resultados, cómo se gestiona un corpus y cómo se miden sus resultados. No se registra: tesis de inversión, datos de mercado, material de opinión o cualquier contenido financiero (para eso están la «Documentación para tendencias de inversión» y el «Registro de fuentes fiables»); criterios sin entrada de corpus que los respalde; entradas sin verificación completa; y propuestas del Buscador Avanzado o de otros agentes como instrucciones: llegan como material de trabajo y solo el Documentador las eleva a registro conforme a estas reglas.

## 6. Reglas de mantenimiento y ciclo de vida

1. **Revisión de primera petición**: en la primera planificación de búsqueda que aplique un criterio del Fondo, el Documentador para el Analizador revalida la carga de arranque (acceso vigente de las 10 entradas, URL concreta de fondo_entry_003 y fondo_entry_004, DOI de fondo_entry_010) y declara el resultado de la revisión.
2. **Ciclo FONDO_MAINTENANCE (mensual)**, coincidente con el DOC_MAINTENANCE: altas de entradas de corpus con verificación completa; destilación y revisión de criterios (toda modificación produce versión nueva con fecha y motivo); regeneración del índice con sus recuentos.
3. **Reindexado completo del índice trimestral**, coincidente con el de la Documentación.
4. **Aplicación trazable**: los criterios se aplican citándolos con su identificador y sus fuentes; un criterio derogado o en revisión no alimenta estrategias.
5. **Consulta ecosistémica**: las consultas de los Documentadores y Buscadores Avanzados de bloques posteriores se resuelven por acceso a archivo conforme a los protocolos de cada bloque; sus propuestas de nuevas entradas o criterios llegan como material de trabajo y solo el Documentador para el Analizador las eleva a registro conforme a la sección 3.
6. **Degradación honesta**: si el mantenimiento no puede completarse por limitación del entorno, se declara la limitación y queda anotada.

## 7. Control de versiones del archivo


| Versión | Fecha | Cambio |

|---|---|---|

| 1.0 | 2026-10-25 | Primera emisión como plantilla de formato, vacía de contenido y de fuentes. |

| 2.0 | 2026-10-25 | Conversión a archivo operativo: carga de arranque con 10 entradas de corpus y 4 criterios destilados dispuesta por el operador; alcance ecosistémico declarado (archivo único para todos los bloques, en vigor desde el 25/10/2026). |
| 2.1 | 2026-10-25 | Anexo documental del operador: añadida la sección 8 «Fuentes fiables específicas de este archivo», con el canal de verificación y acceso por entrada (8.1) y los canales institucionales (8.2); resueltos y verificados los pendientes declarados de fondo_entry_003, fondo_entry_004 y fondo_entry_010. No altera el esquema 1.0 ni los datos de las entradas. |

| 2.2 | 2026-10-26 | Cambio de disposición de las fichas por disposición del operador: las 10 entradas de corpus y los 4 criterios destilados pasan de la tabla vertical de campos al formato compacto de bloques de párrafos con campos etiquetados en negrita (convención 8), para contener la extensión y el peso del documento .docx ante nuevas altas. No altera el esquema 1.0: el conjunto de campos y los valores de cada ficha se conservan íntegros (conversión verificada campo a campo). |

| 2.3 | 2026-10-26 | Adenda V1.2 del Bloque A (aprobada por el operador y aplicada por paquete coordinado conforme al Documento 0, 5.3): precisado el criterio del estado «descartada» de las entradas de corpus (convención 9), que hace las veces del estado «retirada» del resto de archivos y se aplica por bajo aporte relativo o por sustitución conforme a la revisión de conjunto (9.9 del prompt del Documentador); salida siempre lógica y trazable, nunca un borrado. No altera el esquema 1.0 ni los datos de las entradas. |
## 8. Fuentes fiables específicas de este archivo

*(Anexo documental del operador, 25/10/2026.)* Este apartado reúne, para cada entrada del Fondo, las fuentes fiables concretas donde se verifica la cita y se consulta el documento registrado, además de los sitios oficiales de los estándares metodológicos que el Fondo destila. No sustituye al campo «DOI o identificador persistente y URL de acceso» de cada entrada: lo complementa como canal de verificación y acceso. Todos los enlaces listados se comprobaron el 25/10/2026. Los pendientes declarados en la regla de primera revisión (sección 6, regla 1) —URL concreta de fondo_entry_003 y fondo_entry_004, DOI de fondo_entry_010— quedan aquí resueltos y verificados para que el Documentador para el Analizador los absorba, con entrada nueva en el registro 4.4 cuando la absorción toque una entrada. En los ciclos FONDO_MAINTENANCE, estos enlaces se revisan igual que los de las entradas.

### 8.1 Fuentes de verificación por entrada

| Entrada | Fuentes fiables específicas | Qué se verifica ahí |
|---|---|---|
| fondo_entry_001 — PRISMA 2020 | DOI: doi.org/10.1136/bmj.n71 (BMJ, acceso abierto, ficha) · Sitio oficial del estándar: prisma-statement.org (lista de comprobación de 27 puntos, diagrama de flujo y extensiones) · Registro del guideline en EQUATOR Network: equator-network.org | Cita, DOI, texto abierto y documentación vigente del estándar |
| fondo_entry_002 — PRISMA 2009 | DOI: doi.org/10.1371/journal.pmed.1000097 (PLOS Medicine, acceso abierto, ficha) · Sitio oficial: prisma-statement.org (documentación histórica de la versión 2009) | Cita, DOI y compatibilidad de lectura de la literatura documentada contra 2009 |
| fondo_entry_003 — Kitchenham y Charters (2007) | Informe técnico EBSE-2007-01 (Keele University y University of Durham) · **Copia estable verificada hoy**: repositorio abierto EdTech Hub, docs.edtechhub.org/lib/EDAG684W · Localizable también vía Google Scholar y OpenAlex | La URL concreta que la entrada declara pendiente (sección 6.1); la URL editorial original del EBSE está fuera de servicio, por lo que la copia de repositorio es el canal de verificación y lectura |
| fondo_entry_004 — Webster y Watson (2002) | **DOI verificado hoy**: 10.2307/4132319 · JSTOR: jstor.org/stable/4132319 · Página de la revista: misq.umn.edu (MIS Quarterly 26(2), xiii-xxiii) | El DOI y la localización que la entrada deja pendientes |
| fondo_entry_005 — Okoli y Schabram (2010) | DOI: doi.org/10.17705/1CAIS.02618 (AIS eLibrary, ficha) · SSRN abstract_id=1954824 (ficha, descarga gratuita con registro) | Cita, DOI y versión abierta |
| fondo_entry_006 — Wohlin (2014) | DOI: doi.org/10.1145/2601248.2601268 (ACM Digital Library, ficha) · PDF de autor: wohlin.eu/ease14.pdf (ficha) | Cita, DOI y versión de autor |
| fondo_entry_007 — Ouzzani et al. (2016) | DOI: doi.org/10.1186/s13643-016-0384-4 (Systematic Reviews, BMC, acceso abierto, ficha) · Herramienta objeto del artículo: rayyan.ai (sitio oficial) | Cita, DOI y vigencia de la herramienta |
| fondo_entry_008 — Sandve et al. (2013) | DOI: doi.org/10.1371/journal.pcbi.1003285 (PLOS Computational Biology, acceso abierto, ficha) | Cita, DOI y acceso abierto vigente |
| fondo_entry_009 — Harzing y Alakangas (2016) | DOI: doi.org/10.1007/s11192-015-1798-9 (Scientometrics, Springer, ficha) · Publicaciones de la autora: harzing.com (recursos y copias de autor de sus trabajos sobre métricas) | Cita, DOI y obra del autor |
| fondo_entry_010 — Goodman (1961) | **DOI verificado hoy**: 10.1214/aoms/1177705148 · Project Euclid, acceso abierto: projecteuclid.org (Annals of Mathematical Statistics 32(1), 148-170) | El DOI que la entrada deja pendiente; el artículo es de acceso abierto en la editorial |

### 8.2 Canales institucionales de verificación (todo el archivo)

| Canal | Uso en este archivo |
|---|---|
| doi.org (Crossref) | Resolver cualquier DOI de la tabla 8.1 y de las entradas |
| Sitios oficiales de estándares | prisma-statement.org y equator-network.org: la referencia vigente de los guidelines de reporte que el Fondo destila; revisar en FONDO_MAINTENANCE si el estándar emite actualizaciones |
| ACM Digital Library | DOI y ediciones de las entradas de metodología presentadas en conferencias (Wohlin 2014) |
| Springer, BMJ, PLOS, BMC, Project Euclid | Portales editoriales primarios de las entradas; PLOS, BMC y Project Euclid en acceso abierto |
| IDEAS/RePEc, Google Scholar y OpenAlex | Metadatos normalizados, copias de autor adicionales y métricas |
| Retraction Watch Database (retractionwatch.com) | Comprobación de retractaciones en los ciclos FONDO_MAINTENANCE; una entrada retractada pasa a «en revisión» con fecha y motivo |
