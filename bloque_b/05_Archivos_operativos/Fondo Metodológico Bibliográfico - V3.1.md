# Archivo operativo FM — Fondo Metodológico Bibliográfico

**Bloque A · Robot Investor · Versión óptima V4.0 · 01/11/2026** · Subordinado al Documento 0 óptima V5.0.

**Versión del archivo:** V3.1 (01/11/2026), alineada con el Documento 0 óptima V5.0 · **Código:** FM · **Custodio en el Bloque A:** AG-14 Documentador para el Analizador (DOC-A) · **Alcance:** ecosistémico, archivo único para todos los bloques de Robot Investor (R20)

## Cómo usar este archivo

**Propósito.** Metodología de búsqueda, verificación y evaluación de fuentes: cómo se planifica, ejecuta, filtra, verifica y documenta una búsqueda. No contiene conocimiento financiero ni de dominio.

**Propietario y acceso.** Escribe solo AG-14 (custodio). Leen: AG-14, AG-15, AG-16 y los Documentadores y Buscadores de todos los bloques (Documento 0, 5.1). Cualquier agente que detecte un vacío metodológico lo propone al custodio, que lo incorpora tras verificación (13.2).

**Reglas de uso.**

1. **Lectura.** Consulte primero los criterios vigentes y el procedimiento «Uso por todos los bloques»; las entradas de corpus se ordenan por ámbito metodológico y, dentro de cada ámbito, por Q descendente.
2. **Sin criterio sin fuente.** Cada criterio cita al menos una entrada vigente y verificada; el conocimiento interno del modelo nunca es fuente de un criterio. Solo los criterios «vigentes» se aplican; los «en revisión» o «derogados» se consultan pero no se aplican.
3. **Calidad.** Q (0–100) con la rúbrica 13.3 del Documento 0 (Tipo 25 · Rigor 20 · Autoridad 15 · Vigencia 10 · Impacto 10 · Independencia 10 · Accesibilidad 10); niveles A ≥ 80, B 65–79, C 50–64, D < 50. En las semillas la Q es provisional.
4. **Estados del enlace y acciones.** Los mismos que F7–F9: `OK`, `REDIRIGIDO`, `ROTO`, `MURO_PAGO`, `CONTENIDO_CAMBIADO`, `PENDIENTE_BARRIDO` (estado inicial: sin barrido HT-02 todavía); acciones `REPARAR`, `DEGRADAR`, `BORRAR`, con línea en el «Registro de bajas». Las entradas «descartadas» por bajo aporte o sustitución pasan también al registro de bajas.
5. **Ciclo.** Revisión mensual de entradas y criterios (toda modificación de un criterio crea versión nueva con fecha y motivo); reindexado trimestral; informe al Orquestador en el paquete de mantenimiento de DOC-A (CT-21).

## Índice por ámbito metodológico

| Código | Temática | Referencias | Verificadas | Pendientes de verificación | A | B | C | D | Q medio |
|---|---|---|---|---|---|---|---|---|---|
| MB-01 | Planificación y reporte de búsquedas | 21 | 21 | 0 | 20 | 1 | 0 | 0 | 88,7 |
| MB-02 | Construcción de consultas y selección de bases | 26 | 26 | 0 | 23 | 3 | 0 | 0 | 86,7 |
| MB-03 | Filtrado, cribado y bola de nieve | 26 | 26 | 0 | 22 | 4 | 0 | 0 | 86,3 |
| MB-04 | Gestión del corpus | 24 | 24 | 0 | 19 | 5 | 0 | 0 | 84,0 |
| MB-05 | Verificación y reproducibilidad | 20 | 20 | 0 | 18 | 2 | 0 | 0 | 88,3 |
| MB-06 | Métricas bibliométricas y cobertura de bases | 27 | 27 | 0 | 25 | 2 | 0 | 0 | 86,4 |
| MB-07 | Evaluación de credibilidad de fuentes | 20 | 20 | 0 | 13 | 5 | 2 | 0 | 80,7 |
| **Total** | — | **164** | **164** | 0 | 140 | 22 | 2 | 0 | 85,9 |

«Verificadas»: enlace en estado OK, REDIRIGIDO, MURO_PAGO o VERIFICADO_BUSQUEDA (existencia y datos confirmados por búsqueda web el 02/11/2026), o verificación documental completa en una carga anterior (25–26/10/2026), pendiente solo del barrido automático HT-02. «Pendientes»: semillas aún en PENDIENTE_VERIFICACION_ALTA o fichas con alerta sin resolver.

## Uso por todos los bloques

Procedimiento de consulta en seis pasos, obligatorio para los Documentadores y Buscadores de cualquier bloque antes de diseñar una búsqueda (R20):

1. **Delimitar la necesidad.** Formule la pregunta (qué, para qué decisión, clase de activo, horizonte), el tipo de fuente buscada (académica, institucional, opinión, dato) y el presupuesto. Consulte antes la caché del bloque (HT-06) y su propio archivo: no busque lo que ya está registrado.
2. **Seleccionar criterios vigentes.** Identifique en «Criterios destilados» los aplicables a cada fase y cítelos por su ID en la estrategia.
3. **Documentar y ejecutar la estrategia.** Antes de ejecutar, registre ecuación de búsqueda, sistemas consultados, límites temporales y de idioma y fecha (fondo_criterion_001). Use al menos dos sistemas complementarios y complete con búsqueda hacia atrás y hacia adelante (fondo_criterion_002); incluya literatura gris institucional cuando proceda.
4. **Filtrar y ampliar.** Aplique criterios de inclusión explícitos; si el corpus es pequeño o muy interconectado, itere por bola de nieve con regla de parada declarada (fondo_criterion_003).
5. **Verificar cada fuente.** Compruebe enlace, DOI, coincidencia de metadatos, retractaciones y copia archivada (HT-02); para fuentes de opinión, aplique lectura lateral antes de confiar en el contenido; puntúe Q con la rúbrica del archivo de destino.
6. **Registrar y cerrar.** Dé de alta con fecha de consulta, versión del documento y decisiones de cribado sin sobrescribir resultados intermedios (fondo_criterion_004); declare lagunas y, si detecta un vacío metodológico, propóngalo al custodio de este Fondo.

## Criterios destilados

| ID | Texto operativo | Fase | Fuerza | Fuentes | Estado | Versión |
|---|---|---|---|---|---|---|
| fondo_criterion_001 | Documenta toda estrategia de búsqueda antes de ejecutarla: ecuación de búsqueda, bases consultadas, límites temporales y de idioma, y fecha de ejecución, de modo que otra agencia pueda repetirla idéntica y auditar lo descartado. | Planificación | Obligatorio | fondo_entry_001 (PRISMA 2020), fondo_entry_002 (PRISMA 2009), fondo_entry_005 (Okoli y Schabram 2010) | Vigente | 1.0 (2026-10-25) |
| fondo_criterion_002 | Completa toda búsqueda en bases con búsqueda reversa (referencias de los documentos centrales) y búsqueda hacia adelante (citas que reciben); registra ambas pasadas en la estrategia. | Consultas | Obligatorio | fondo_entry_003 (Kitchenham y Charters 2007), fondo_entry_004 (Webster y Watson 2002), fondo_entry_005 (Okoli y Schabram 2010) | Vigente | 1.0 (2026-10-25) |
| fondo_criterion_003 | Usa la bola de nieve para ampliar o sustituir la búsqueda en bases cuando el corpus sea pequeño o muy interconectado: itera hacia atrás y hacia adelante con criterios de inclusión explícitos por iteración y una regla de parada declarada. | Filtrado | Recomendado | fondo_entry_006 (Wohlin 2014) | Vigente | 1.0 (2026-10-25) |
| fondo_criterion_004 | Registra cada entrada del corpus con su fecha de consulta, la versión del documento utilizada y la trazabilidad suficiente para reproducir el cribado: deduplica, anota las decisiones de inclusión y no sobrescribas ningún resultado intermedio. | Gestión del corpus | Obligatorio | fondo_entry_007 (Ouzzani et al. 2016), fondo_entry_008 (Sandve et al. 2013) | Vigente | 1.0 (2026-10-25) |

## Novedades

Sección de difusión semanal (Documento 0, 6.1): el propietario anota aquí las altas, reparaciones, degradaciones y bajas de la semana; los agentes lectores la consultan al inicio de cada encargo mediante HT-06. Se conservan las cuatro últimas semanas; lo anterior queda en el historial del archivo.

| Semana (lunes) | Tipo | ID | Temática | Resumen (una línea) |
|---|---|---|---|---|

Tipos admitidos: `ALTA`, `REPARACION`, `DEGRADACION`, `RECALIFICACION`, `BAJA`, `VERIFICACION_ALTA` (semilla confirmada o rechazada).

## MB-01 Planificación y reporte de búsquedas

#### fondo_entry_001 · Q 98 (A) — PRISMA 2020

- **Cita normalizada:** Page, M. J., McKenzie, J. E., Bossuyt, P. M., et al. (2021). The PRISMA 2020 statement: an updated guideline for reporting systematic reviews. BMJ, 372, n71.
- **Tipo de fuente:** Artículo revisado por pares (declaración de consenso)
- **Ámbito metodológico:** MB-01 Planificación y reporte de búsquedas (principal) (en V2.3: Planificación)
- **Calidad Q:** 98 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 10/10
- **DOI / URL:** DOI: 10.1136/bmj.n71 · Acceso gratuito en la editorial (bmj.com) · Verificación (anexo 8.1 V2.3): DOI: doi.org/10.1136/bmj.n71 (BMJ, acceso abierto, ficha) · Sitio oficial del estándar: prisma-statement.org (lista de comprobación de 27 puntos, diagrama de flujo y extensiones) · Registro del guideline en EQUATOR Network: equator-network.org
- **Estado:** Vigente
- **Estado del enlace:** PENDIENTE_BARRIDO
- **Última verificación:** 2026-10-25
- **Ficha metodológica:** Declara el estándar internacional de reporte de revisiones sistemáticas: diagrama de flujo de identificación, cribado y inclusión de resultados, y lista de comprobación de 27 puntos. Da al Fondo el modelo de trazabilidad del proceso de búsqueda: qué se buscó, dónde, con qué ecuación y qué se descartó.
- **Criterios derivados:** fondo_criterion_001
- **Verificación V2.3:** Completa (carga de arranque): cita, DOI y acceso abierto verificados el 25/10/2026; comprobaciones omitidas: lectura del texto completo por el Documentador, pendiente de la primera revisión

#### fondo_entry_012 · Q 95 (A) — PRISMA-S: an extension to the PRISMA Statement for Reporting Literature Searches in Systematic Reviews

- **Cita normalizada:** Rethlefsen, M. L., Kirtley, S., Waffenschmidt, S., et al. (2021). PRISMA-S: an extension to the PRISMA Statement for Reporting Literature Searches in Systematic Reviews. Systematic Reviews, 10, 39.
- **Tipo de fuente:** Artículo revisado por pares (declaración de consenso)
- **Ámbito metodológico:** MB-01 Planificación y reporte de búsquedas (principal) · secundarias: MB-02, MB-05
- **Calidad Q:** 95 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 8/10 · Independencia 10/10 · Acceso 10/10
- **DOI / URL:** DOI: 10.1186/s13643-020-01542-z · Repositorio institucional (Oxford ORA): https://ora.ox.ac.uk/objects/uuid:7d3d9091-bb85-440c-8506-ff4d70e96582 · PDF editorial: https://systematicreviewsjournal.biomedcentral.com/counter/pdf/10.1186/s13643-020-01542-z .pdf · Acceso abierto, licencia CC BY 4.0 (confirmada en ORA)
- **Estado:** Vigente
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Rethlefsen PRISMA-S extension reporting literature searches Systematic Reviews 2021 10 39»; WebFetch: sí, ORA)
- **Ficha metodológica:** Lista de 16 elementos para documentar búsquedas de forma reproducible (bases y plataformas, estrategias completas línea a línea, límites y filtros, fechas, búsqueda de citas, contacto con expertos, revisión por pares de la estrategia, deduplicación y número de registros). Complementa a fondo_entry_001 en la fase de reporte y es la base natural para ampliar fondo_criterion_001.
- **Criterios derivados:** Ninguno todavía (candidata a fuente adicional de fondo_criterion_001 en la próxima revisión mensual).
- **Origen:** Semilla V3.0 (2026-11-01); verificación de alta completada el 2026-11-02 (cita, DOI, licencia y copia en repositorio institucional). El registro de ORA solo muestra el primer autor; los coautores se mantienen tal como figuraban en la semilla, pendientes de cotejo en el barrido HT-02.
- **Nota:** Diseñada para ciencias de la salud; los elementos sobre registros de ensayos y bases biomédicas se adaptan a bases económicas y financieras (SSRN, RePEc, EconLit, repositorios de bancos centrales).

#### fondo_entry_104 · Q 95 (A) — Preferred reporting items for systematic review and meta-analysis protocols (PRISMA-P) 2015 statement

- **Cita normalizada:** Moher, D., Shamseer, L., Clarke, M., Ghersi, D., Liberati, A., Petticrew, M., Shekelle, P., y Stewart, L. A. (2015). Preferred reporting items for systematic review and meta-analysis protocols (PRISMA-P) 2015 statement. Systematic Reviews, 4(1), 1.
- **Tipo de fuente:** Artículo revisado por pares (declaración de consenso)
- **Ámbito metodológico:** MB-01 Planificación y reporte de búsquedas (principal) · secundarias: MB-05
- **Calidad Q:** 95 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 10/10
- **DOI / URL:** DOI: 10.1186/2046-4053-4-1 · https://systematicreviewsjournal.biomedcentral.com/articles/10.1186/2046-4053-4-1 (enlace tomado del índice) · Página oficial: https://www.prisma-statement.org/protocols · Acceso abierto
- **Estado:** Vigente
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «EQUATOR Network reporting guidelines systematic reviews PRISMA-P PRISMA-ScR protocol scoping»; WebFetch: sí, índices de la University of Tasmania y del Memorial Sloan Kettering (ambos con la cita completa); artículo no leído)
- **Ficha metodológica:** Lista de comprobación para redactar el protocolo de una revisión antes de ejecutarla: pregunta, criterios de elegibilidad, fuentes, estrategia de búsqueda prevista, gestión de datos y proceso de selección. Es la base para exigir que la estrategia se fije por escrito antes de buscar (fondo_criterion_001).
- **Criterios derivados:** Ninguno todavía.
- **Origen:** Alta V4.0 (2026-11-02). Confirmada en el índice de la guía de la University of Tasmania Library (https://utas.libguides.com/SystematicReviews/ReportingStandards) y en el índice del blog de la biblioteca del Memorial Sloan Kettering (https://library.mskcc.org/blog/?p=26672).

#### fondo_entry_103 · Q 93 (A) — PRISMA extension for scoping reviews (PRISMA-ScR): checklist and explanation

- **Cita normalizada:** Tricco, A. C., Lillie, E., Zarin, W., O'Brien, K. K., Colquhoun, H., Levac, D., Moher, D., Peters, M. D. J., et al. (2018). PRISMA Extension for Scoping Reviews (PRISMA-ScR): Checklist and Explanation. Annals of Internal Medicine, 169(7), 467-473.
- **Tipo de fuente:** Artículo revisado por pares (declaración de consenso)
- **Ámbito metodológico:** MB-01 Planificación y reporte de búsquedas (principal) · secundarias: MB-03
- **Calidad Q:** 93 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 7/10
- **DOI / URL:** DOI: 10.7326/M18-0850 · Repositorio institucional (University of Adelaide): https://digital.library.adelaide.edu.au/items/66fd45ea-e4b1-4ea8-b350-01cd6f309e7b · Editorial (ACP Journals), versión publicada por suscripción; manuscrito aceptado en abierto en el repositorio
- **Estado:** Vigente
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «EQUATOR Network reporting guidelines systematic reviews PRISMA-P PRISMA-ScR protocol scoping»; WebFetch: sí, repositorio de Adelaide; autores completos cotejados además en el índice del blog de la biblioteca del Memorial Sloan Kettering)
- **Ficha metodológica:** Lista de comprobación con explicación para informar revisiones de alcance (scoping reviews), con explicación de cada uno. Fija qué debe declararse cuando el objetivo es cartografiar un campo y no responder a una pregunta cerrada, nivel de exhaustividad habitual en las búsquedas exploratorias del bloque.
- **Criterios derivados:** Ninguno todavía.
- **Origen:** Alta V4.0 (2026-11-02). Verificación directa (autores, revista, volumen, páginas, DOI).
- **Nota:** Elaborada en ciencias de la salud; texto completo no leído en esta verificación.

#### fondo_entry_002 · Q 93 (A) — PRISMA 2009

- **Cita normalizada:** Moher, D., Liberati, A., Tetzlaff, J., Altman, D. G., y The PRISMA Group (2009). Preferred Reporting Items for Systematic Reviews and Meta-Analyses: The PRISMA Statement. PLoS Medicine, 6(7), e1000097.
- **Tipo de fuente:** Artículo revisado por pares (declaración de consenso)
- **Ámbito metodológico:** MB-01 Planificación y reporte de búsquedas (principal) (en V2.3: Planificación)
- **Calidad Q:** 93 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 6/10 · Impacto 10/10 · Independencia 10/10 · Acceso 10/10
- **DOI / URL:** DOI: 10.1371/journal.pmed.1000097 · Acceso abierto en la editorial (journals.plos.org) · Verificación (anexo 8.1 V2.3): DOI: doi.org/10.1371/journal.pmed.1000097 (PLOS Medicine, acceso abierto, ficha) · Sitio oficial: prisma-statement.org (documentación histórica de la versión 2009)
- **Estado:** Vigente
- **Estado del enlace:** PENDIENTE_BARRIDO
- **Última verificación:** 2026-10-25
- **Ficha metodológica:** Versión previa de la declaración PRISMA. Se conserva por valor de compatibilidad: mucha literatura aplicada aún se documenta contra PRISMA 2009, y conocer sus 27 puntos y su diagrama de flujo de cuatro fases permite leer esa literatura con criterio. Actualizada materialmente por fondo_entry_001 (PRISMA 2020); para reporte nuevo se aplica la versión 2020.
- **Criterios derivados:** fondo_criterion_001
- **Verificación V2.3:** Completa (carga de arranque): cita, DOI y acceso abierto verificados el 25/10/2026; comprobaciones omitidas: lectura del texto completo por el Documentador
- **Nota:** Versión superada por fondo_entry_001; se conserva por compatibilidad de lectura.

#### fondo_entry_110 · Q 91 (A) — Guidelines for including grey literature and conducting multivocal literature reviews in software engineering

- **Cita normalizada:** Garousi, V., Felderer, M., y Mäntylä, M. V. (2019). Guidelines for including grey literature and conducting multivocal literature reviews in software engineering. Information and Software Technology, 106, 101-121.
- **Tipo de fuente:** Artículo revisado por pares (guía metodológica)
- **Ámbito metodológico:** MB-01 Planificación y reporte de búsquedas (principal) · secundarias: MB-02, MB-07
- **Calidad Q:** 91 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 12/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 9/10
- **DOI / URL:** DOI: 10.1016/j.infsof.2018.09.006 · Repositorio institucional (Universidad de Oulu): https://oulurepo.oulu.fi/handle/10024/27678 · Preprint en arXiv: https://arxiv.org/abs/1707.02553v4
- **Estado:** Vigente
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Petersen Vakkalanka Kuzniarz guidelines systematic mapping studies software engineering Garousi multivocal literature review grey literature guidelines»; WebFetch: sí, repositorio de Oulu y arXiv)
- **Ficha metodológica:** Guía para planificar, ejecutar e informar revisiones «multivocales», que combinan literatura académica con literatura gris (blogs, informes técnicos, libros blancos), con reglas propias de búsqueda en buscadores generalistas, criterios de parada y evaluación de la calidad de fuentes no revisadas por pares. Es la guía más próxima a la mezcla de fuentes académicas y de opinión que maneja el bloque (F7 + F9).
- **Criterios derivados:** Ninguno todavía.
- **Origen:** Alta V4.0 (2026-11-02). Verificación directa (cita completa en el repositorio de Oulu; resumen en arXiv).
- **Nota:** Publicada en línea en 2018 y en volumen en 2019; ejemplos de ingeniería de software.

#### fondo_entry_106 · Q 91 (A) — Scoping studies: advancing the methodology

- **Cita normalizada:** Levac, D., Colquhoun, H., y O'Brien, K. K. (2010). Scoping studies: advancing the methodology. Implementation Science, 5, 69.
- **Tipo de fuente:** Artículo revisado por pares (metodología)
- **Ámbito metodológico:** MB-01 Planificación y reporte de búsquedas (principal) · secundarias: MB-03
- **Calidad Q:** 91 (A) — Tipo 25/25 · Rigor 14/20 · Autoridad 13/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 10/10
- **DOI / URL:** DOI: 10.1186/1748-5908-5-69 · DOAJ: https://doaj.org/article/3a6c8738730e4fe793eb151f2e924635 · PDF editorial: https://implementationscience.biomedcentral.com/track/pdf/10.1186/1748-5908-5-69 · Acceso abierto
- **Estado:** Vigente
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Arksey O'Malley scoping studies methodological framework Levac Colquhoun advancing the methodology Peters JBI guidance»; WebFetch: sí, DOAJ (título, año, revista y resumen) y guía del Medical College of Wisconsin (autores, volumen y DOI))
- **Ficha metodológica:** Refina las seis etapas del marco de Arksey y O'Malley: vincular propósito y pregunta, equilibrar factibilidad y exhaustividad, selección y extracción en equipo, análisis numérico y temático, y consulta a interesados como paso de transferencia. Aporta reglas prácticas para dimensionar una búsqueda exploratoria.
- **Criterios derivados:** Ninguno todavía.
- **Origen:** Alta V4.0 (2026-11-02). Verificación directa en DOAJ y en la guía del MCW.

#### fondo_entry_109 · Q 90 (A) — Guidelines for conducting systematic mapping studies in software engineering: An update

- **Cita normalizada:** Petersen, K., Vakkalanka, S., y Kuzniarz, L. (2015). Guidelines for conducting systematic mapping studies in software engineering: An update. Information and Software Technology, 64, 1-18.
- **Tipo de fuente:** Artículo revisado por pares (guía metodológica)
- **Ámbito metodológico:** MB-01 Planificación y reporte de búsquedas (principal) · secundarias: MB-02, MB-03
- **Calidad Q:** 90 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 13/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 7/10
- **DOI / URL:** DOI: 10.1016/j.infsof.2015.03.007 · Ficha en el sitio EBSE de la Durham University: https://ebse.webspace.durham.ac.uk/?p=466
- **Estado:** Vigente
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Petersen Vakkalanka Kuzniarz guidelines systematic mapping studies software engineering Garousi multivocal literature review grey literature guidelines»; WebFetch: sí, sitio EBSE de Durham)
- **Ficha metodológica:** Mapeo sistemático de los propios estudios de mapeo y guía actualizada para realizarlos: definición de la búsqueda, uso combinado de bases y bola de nieve, criterios de selección y evaluación de la calidad. Útil cuando un encargo pide cartografiar qué se ha publicado sobre un tema más que sintetizar resultados.
- **Criterios derivados:** Ninguno todavía.
- **Origen:** Alta V4.0 (2026-11-02). Verificación directa en el sitio EBSE.
- **Nota:** La página consultada da volumen 65 en el detalle y 64 en su BibTeX; se cita 64 pendiente de cotejo en el barrido HT-02.

#### fondo_entry_117 · Q 90 (A) — PRISMA for Abstracts: Reporting Systematic Reviews in Journal and Conference Abstracts

- **Cita normalizada:** Beller, E. M., Glasziou, P. P., Altman, D. G., Hopewell, S., Bastian, H., Chalmers, I., Gøtzsche, P. C., Lasserson, T., Tovey, D., y PRISMA for Abstracts Group (2013). PRISMA for Abstracts: Reporting Systematic Reviews in Journal and Conference Abstracts. PLoS Medicine, 10(4), e1001419.
- **Tipo de fuente:** Artículo revisado por pares (declaración de consenso)
- **Ámbito metodológico:** MB-01 Planificación y reporte de búsquedas (principal) · secundarias: MB-04
- **Calidad Q:** 90 (A) — Tipo 25/25 · Rigor 15/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 8/10 · Independencia 10/10 · Acceso 8/10
- **DOI / URL:** Sin DOI visto · PMID 23585737 · Confirmada en el índice del blog de la biblioteca del Memorial Sloan Kettering: https://library.mskcc.org/blog/?p=26672 · PLOS Medicine, acceso abierto
- **Estado:** Vigente
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «EQUATOR Network reporting guidelines systematic reviews PRISMA-P PRISMA-ScR protocol scoping»; WebFetch: sí, índice del Memorial Sloan Kettering; artículo no leído)
- **Ficha metodológica:** Lista de comprobación para los resúmenes de revisiones sistemáticas en revistas y congresos, que incluye la identificación de las fuentes consultadas. Útil como plantilla mínima del resumen de cada encargo de búsqueda del bloque.
- **Criterios derivados:** Ninguno todavía.
- **Origen:** Alta V4.0 (2026-11-02). Confirmada en índice (cita completa con PMID).
- **Nota:** Aporte marginal frente a PRISMA 2020 (fondo_entry_001), cuya lista para resúmenes la incorpora; se mantiene por su formato breve.

#### fondo_entry_108 · Q 90 (A) — A typology of reviews: an analysis of 14 review types and associated methodologies

- **Cita normalizada:** Grant, M. J., y Booth, A. (2009). A typology of reviews: an analysis of 14 review types and associated methodologies. Health Information and Libraries Journal, 26(2), 91-108.
- **Tipo de fuente:** Artículo revisado por pares
- **Ámbito metodológico:** MB-01 Planificación y reporte de búsquedas (principal) · secundarias: MB-02
- **Calidad Q:** 90 (A) — Tipo 25/25 · Rigor 14/20 · Autoridad 14/15 · Vigencia 9/10 · Impacto 10/10 · Independencia 10/10 · Acceso 8/10
- **DOI / URL:** DOI: 10.1111/j.1471-1842.2009.00848.x · Repositorio institucional (University of Salford): https://salford-repository.worktribe.com/output/1454519/a-typology-of-reviews-an-analysis-of-14-review-types-and-associated-methodologies · Revisión retrospectiva en EBLIP: https://journals.library.ualberta.ca/eblip/index.php/EBLIP/article/view/30093
- **Estado:** Vigente
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Grant Booth 2009 typology of reviews 14 review types Tranfield Denyer Smart 2003 evidence-informed management knowledge»; WebFetch: sí, repositorio de Salford y EBLIP)
- **Ficha metodológica:** Define 14 tipos de revisión (sistemática, de alcance, rápida, paraguas, mapeo, etc.) con el marco SALSA (búsqueda, evaluación, síntesis y análisis), indicando qué exhaustividad de búsqueda corresponde a cada uno. Permite asignar a cada encargo un tipo de revisión y, con él, el nivel de búsqueda N0-N3.
- **Criterios derivados:** Ninguno todavía.
- **Origen:** Alta V4.0 (2026-11-02). Verificación directa (cita completa y DOI en Salford y EBLIP).

#### fondo_entry_112 · Q 90 (A) — MECIR Manual — Methodological Expectations of Cochrane Intervention Reviews

- **Cita normalizada:** Cochrane (versión vigente). Methodological Expectations of Cochrane Intervention Reviews (MECIR) Manual. Londres: Cochrane.
- **Tipo de fuente:** Manual de referencia (estándares de conducta y reporte)
- **Ámbito metodológico:** MB-01 Planificación y reporte de búsquedas (principal) · secundarias: MB-02, MB-05
- **Calidad Q:** 90 (A) — Tipo 20/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 9/10
- **DOI / URL:** Sin DOI · https://community.cochrane.org/mecir-manual (enlace tomado del índice) · Estándares equivalentes para la Campbell Collaboration (MECCIR): https://www.campbellcollaboration.org/about-meccir.html · Acceso gratuito
- **Estado:** Vigente
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «EQUATOR Network reporting guidelines systematic reviews PRISMA-P PRISMA-ScR protocol scoping»; WebFetch: sí, índice de la guía de NUS Libraries; manual no leído)
- **Ficha metodológica:** Estándares obligatorios y altamente deseables para planificar, ejecutar e informar revisiones Cochrane, con apartados específicos sobre búsqueda (fuentes mínimas, documentación de estrategias, actualización antes de publicar). Sirve para graduar los criterios del Fondo en «obligatorio» y «recomendado».
- **Criterios derivados:** Ninguno todavía.
- **Origen:** Alta V4.0 (2026-11-02). Confirmada en el índice de la guía de NUS Libraries (https://libguides.nus.edu.sg/sysreviews/guidelines); autoría institucional, sin autores individuales visibles.
- **Nota:** Documento vivo: citar versión y fecha de consulta.

#### fondo_entry_111 · Q 89 (A) — Meta-analysis of observational studies in epidemiology: a proposal for reporting (MOOSE)

- **Cita normalizada:** Stroup, D. F., Berlin, J. A., Morton, S. C., Olkin, I., Williamson, G. D., Rennie, D., Moher, D., Becker, B. J., Sipe, T. A., y Thacker, S. B. (2000). Meta-analysis of observational studies in epidemiology: a proposal for reporting. Meta-analysis Of Observational Studies in Epidemiology (MOOSE) group. JAMA, 283(15), 2008-2012.
- **Tipo de fuente:** Artículo revisado por pares (declaración de consenso)
- **Ámbito metodológico:** MB-01 Planificación y reporte de búsquedas (principal) · secundarias: MB-02
- **Calidad Q:** 89 (A) — Tipo 25/25 · Rigor 15/20 · Autoridad 15/15 · Vigencia 7/10 · Impacto 10/10 · Independencia 10/10 · Acceso 7/10
- **DOI / URL:** Sin DOI visto · PubMed: https://www.ncbi.nlm.nih.gov/pubmed/10789670 · Ficha EQUATOR: http://www.equator-network.org/reporting-guidelines/meta-analysis-of-observational-studies-in-epidemiology-a-proposal-for-reporting-meta-analysis-of-observational-studies-in-epidemiology-moose-group/ (enlaces tomados del índice)
- **Estado:** Vigente
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «EQUATOR Network reporting guidelines systematic reviews PRISMA-P PRISMA-ScR protocol scoping»; WebFetch: sí, índice de la University of Tasmania Library (cita completa); artículo no leído)
- **Ficha metodológica:** Lista de reporte para metaanálisis de estudios observacionales que incluye elementos específicos sobre la estrategia de búsqueda (fuentes, términos, contacto con autores, idiomas, estudios no localizados); lista no leída en esta verificación. Pertinente porque la evidencia financiera es casi siempre observacional.
- **Criterios derivados:** Ninguno todavía.
- **Origen:** Alta V4.0 (2026-11-02). Confirmada en el índice de la University of Tasmania Library (https://utas.libguides.com/SystematicReviews/ReportingStandards).
- **Nota:** Anterior a PRISMA 2009; parte de sus elementos de búsqueda están hoy cubiertos por PRISMA-S (fondo_entry_012).

#### fondo_entry_107 · Q 87 (A) — Chapter 11: Scoping Reviews (2020 version), JBI Manual for Evidence Synthesis

- **Cita normalizada:** Peters, M. D. J., Godfrey, C., McInerney, P., et al. (2020). Chapter 11: Scoping Reviews (2020 version). En Aromataris, E., y Munn, Z. (eds.), JBI Manual for Evidence Synthesis. JBI.
- **Tipo de fuente:** Manual de referencia (capítulo)
- **Ámbito metodológico:** MB-01 Planificación y reporte de búsquedas (principal) · secundarias: MB-02
- **Calidad Q:** 87 (A) — Tipo 20/25 · Rigor 16/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 8/10 · Independencia 10/10 · Acceso 9/10
- **DOI / URL:** DOI: 10.46658/JBIMES-20-12 · Confirmada en la guía del Medical College of Wisconsin: https://mcw.libguides.com/ScopingReviews/Process · Manual JBI de acceso gratuito en línea
- **Estado:** Vigente
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Arksey O'Malley scoping studies methodological framework Levac Colquhoun advancing the methodology Peters JBI guidance»; WebFetch: sí, guía del MCW (cita con DOI); capítulo no leído)
- **Ficha metodológica:** Método JBI de revisiones de alcance: protocolo, pregunta PCC (población, concepto, contexto), estrategia de búsqueda iterativa y presentación de resultados (capítulo no leído en esta verificación; contenido a cotejar en la primera revisión). El esquema PCC es aplicable a preguntas no clínicas como las del bloque.
- **Criterios derivados:** Ninguno todavía.
- **Origen:** Alta V4.0 (2026-11-02). Confirmada en índice (cita y DOI).
- **Nota:** Existe una versión posterior del capítulo; citar siempre la versión consultada.

#### fondo_entry_115 · Q 87 (A) — Expediting systematic reviews: methods and implications of rapid reviews

- **Cita normalizada:** Ganann, R., Ciliska, D., y Thomas, H. (2010). Expediting systematic reviews: methods and implications of rapid reviews. Implementation Science, 5, 56.
- **Tipo de fuente:** Artículo revisado por pares
- **Ámbito metodológico:** MB-01 Planificación y reporte de búsquedas (principal) · secundarias: MB-03
- **Calidad Q:** 87 (A) — Tipo 25/25 · Rigor 14/20 · Autoridad 12/15 · Vigencia 8/10 · Impacto 9/10 · Independencia 10/10 · Acceso 9/10
- **DOI / URL:** Sin DOI visto · Confirmada en la bibliografía de la presentación de A. Booth sobre selección de estudios, EPPI Centre, 2024 (https://eppi.ioe.ac.uk/CMS/Portals/0/Study%20Selection%20-%20Andrew%20Booth%20-%20ESG.pdf) · Implementation Science, acceso abierto
- **Estado:** Vigente
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «single screening versus double screening study selection systematic reviews Waffenschmidt Gartlehner»; WebFetch: sí, presentación de Booth (índice); artículo no leído)
- **Ficha metodológica:** Revisión de los métodos de las revisiones rápidas y de las implicaciones de sus atajos (menos bases, límites de idioma y fecha, cribado simple). Ayuda a decidir qué recortes de búsqueda son aceptables cuando el encargo tiene plazo corto y a declararlos.
- **Criterios derivados:** Ninguno todavía.
- **Origen:** Alta V4.0 (2026-11-02). Confirmada en índice.

#### fondo_entry_105 · Q 87 (A) — Scoping studies: towards a methodological framework

- **Cita normalizada:** Arksey, H., y O'Malley, L. (2005). Scoping studies: towards a methodological framework. International Journal of Social Research Methodology.
- **Tipo de fuente:** Artículo revisado por pares (marco metodológico)
- **Ámbito metodológico:** MB-01 Planificación y reporte de búsquedas (principal) · secundarias: MB-03
- **Calidad Q:** 87 (A) — Tipo 25/25 · Rigor 14/20 · Autoridad 13/15 · Vigencia 9/10 · Impacto 10/10 · Independencia 10/10 · Acceso 6/10
- **DOI / URL:** DOI no visto · Confirmada en la guía CASRAI: https://casrai.org/guides/arksey-omalley-scoping-review-framework-levac-refinements · Revista Taylor & Francis (suscripción)
- **Estado:** Vigente
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Arksey O'Malley scoping studies methodological framework Levac Colquhoun advancing the methodology Peters JBI guidance»; WebFetch: sí, guía CASRAI (autores, año, título y revista); artículo no leído)
- **Ficha metodológica:** Marco fundacional en seis etapas de las revisiones de alcance: identificar la pregunta, identificar estudios relevantes, seleccionarlos, cartografiar los datos, cotejar y resumir, y consulta opcional. Es el origen del enfoque exploratorio que refinan Levac et al. (fondo_entry_106) y el manual JBI (fondo_entry_107).
- **Criterios derivados:** Ninguno todavía.
- **Origen:** Alta V4.0 (2026-11-02). Confirmada en índice; volumen, páginas y DOI pendientes de cotejo.

#### fondo_entry_113 · Q 85 (A) — Predicting the time needed for environmental systematic reviews and systematic maps

- **Cita normalizada:** Haddaway, N. R., y Westgate, M. J. (2019). Predicting the time needed for environmental systematic reviews and systematic maps. Conservation Biology, 33(2), 434-443.
- **Tipo de fuente:** Artículo revisado por pares
- **Ámbito metodológico:** MB-01 Planificación y reporte de búsquedas (principal) · secundarias: MB-04
- **Calidad Q:** 85 (A) — Tipo 25/25 · Rigor 15/20 · Autoridad 12/15 · Vigencia 9/10 · Impacto 7/10 · Independencia 10/10 · Acceso 7/10
- **DOI / URL:** DOI: 10.1111/cobi.13231 · Confirmada en la bibliografía de la presentación de A. Booth, EPPI Centre, 2024: https://eppi.ioe.ac.uk/CMS/Portals/0/Study%20Selection%20-%20Andrew%20Booth%20-%20ESG.pdf
- **Estado:** Vigente
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «single screening versus double screening study selection systematic reviews Waffenschmidt Gartlehner»; WebFetch: sí, presentación de Booth (índice); artículo no leído)
- **Ficha metodológica:** Modelo de predicción del tiempo de cada fase de una revisión (búsqueda, cribado de títulos y resúmenes, texto completo, extracción) a partir del volumen de registros. Sirve para presupuestar el esfuerzo de un encargo antes de ejecutar la búsqueda.
- **Criterios derivados:** Ninguno todavía.
- **Origen:** Alta V4.0 (2026-11-02). Confirmada en índice (cita con DOI).
- **Nota:** El índice fecha la obra en 2018 (publicación en línea); el volumen 33(2) corresponde a 2019. Datos de revisiones ambientales.

#### fondo_entry_005 · Q 85 (A) — Okoli y Schabram (2010)

- **Cita normalizada:** Okoli, C., y Schabram, K. (2010). A Guide to Conducting a Systematic Literature Review of Information Systems Research. Communications of the Association for Information Systems, 26, artículo 18.
- **Tipo de fuente:** Artículo revisado por pares (guía metodológica)
- **Ámbito metodológico:** MB-01 Planificación y reporte de búsquedas (principal) · secundarias: MB-02 (en V2.3: Planificación)
- **Calidad Q:** 85 (A) — Tipo 22/25 · Rigor 15/20 · Autoridad 12/15 · Vigencia 9/10 · Impacto 8/10 · Independencia 10/10 · Acceso 9/10
- **DOI / URL:** DOI: 10.17705/1CAIS.02618 · SSRN: papers.ssrn.com/sol3/papers.cfm?abstract_id=1954824 (descarga gratuita con registro) · Verificación (anexo 8.1 V2.3): DOI: doi.org/10.17705/1CAIS.02618 (AIS eLibrary, ficha) · SSRN abstract_id=1954824 (ficha, descarga gratuita con registro)
- **Estado:** Vigente
- **Estado del enlace:** PENDIENTE_BARRIDO
- **Última verificación:** 2026-10-25
- **Ficha metodológica:** Guía de revisión sistemática en diez pasos, desde el propósito hasta la presentación, con recomendaciones explícitas sobre ecuaciones de búsqueda y documentación del proceso. Es el puente entre PRISMA (médica) y la práctica en dominios de información y negocios.
- **Criterios derivados:** fondo_criterion_001, fondo_criterion_002
- **Verificación V2.3:** Completa (carga de arranque): cita, DOI y página SSRN verificadas el 25/10/2026; comprobaciones omitidas: lectura del texto completo por el Documentador

#### fondo_entry_116 · Q 84 (A) — Advancing knowledge of rapid reviews: an analysis of results, conclusions and recommendations from published review articles examining rapid reviews

- **Cita normalizada:** Featherstone, R. M., et al. (2015). Advancing knowledge of rapid reviews: an analysis of results, conclusions and recommendations from published review articles examining rapid reviews. Systematic Reviews, 4(1), 50.
- **Tipo de fuente:** Artículo revisado por pares (revisión de revisiones)
- **Ámbito metodológico:** MB-01 Planificación y reporte de búsquedas (principal) · secundarias: MB-03
- **Calidad Q:** 84 (A) — Tipo 25/25 · Rigor 14/20 · Autoridad 11/15 · Vigencia 8/10 · Impacto 7/10 · Independencia 10/10 · Acceso 9/10
- **DOI / URL:** Sin DOI visto · Confirmada en la bibliografía de la presentación de A. Booth, EPPI Centre, 2024: https://eppi.ioe.ac.uk/CMS/Portals/0/Study%20Selection%20-%20Andrew%20Booth%20-%20ESG.pdf · Systematic Reviews, acceso abierto
- **Estado:** Vigente
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «single screening versus double screening study selection systematic reviews Waffenschmidt Gartlehner»; WebFetch: sí, presentación de Booth (índice); artículo no leído)
- **Ficha metodológica:** Síntesis de las revisiones que han estudiado las revisiones rápidas: qué atajos se usan, con qué consecuencias y qué recomendaciones de transparencia se derivan. Complementa a fondo_entry_115 para justificar el nivel de exhaustividad de cada encargo.
- **Criterios derivados:** Ninguno todavía.
- **Origen:** Alta V4.0 (2026-11-02). Confirmada en índice; el índice solo da «Featherstone RM et al.»; coautores pendientes de cotejo en el barrido.
- **Nota:** Coautores distintos del primero no confirmados en esta verificación.

#### fondo_entry_014 · Q 83 (A) — Systematic Approaches to a Successful Literature Review (3.ª ed.)

- **Cita normalizada:** Booth, A., Sutton, A., Clowes, M., y Martyn-St James, M. (2021). Systematic Approaches to a Successful Literature Review (3.ª ed.). Los Ángeles: SAGE. ISBN 9781529711851 (rústica), 9781529711844 (tapa dura), 9781529759662 (electrónico).
- **Tipo de fuente:** Manual de referencia
- **Ámbito metodológico:** MB-01 Planificación y reporte de búsquedas (principal) · secundarias: MB-02, MB-03
- **Calidad Q:** 83 (A) — Tipo 20/25 · Rigor 16/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 8/10 · Independencia 10/10 · Acceso 5/10
- **DOI / URL:** Sin DOI visto · Registro bibliográfico de la British Library: https://eld.bl.uk/catalog/020342183 · Obra comercial (SAGE), sin acceso abierto
- **Estado:** Vigente
- **Estado del enlace:** MURO_PAGO
- **Última verificación:** 2026-11-02 (búsqueda web: «Booth Sutton Clowes Martyn-St James Systematic Approaches to a Successful Literature Review third edition 2021 SAGE ISBN»; WebFetch: sí, catálogo de la British Library)
- **Ficha metodológica:** Manual práctico de revisiones de literatura (sistemáticas, de alcance, rápidas, de mapeo): planificación, búsqueda, evaluación, síntesis y reporte; tipología de revisiones según el tiempo y el propósito, útil para escoger el nivel de exhaustividad N0-N3 de cada encargo.
- **Criterios derivados:** Ninguno todavía.
- **Origen:** Semilla V3.0 (2026-11-01); verificación de alta completada el 2026-11-02 (autores, edición, editorial, año e ISBN en el catálogo de la British Library). Texto completo no leído (obra de pago).
- **Nota:** El catálogo atribuye la edición a 2021 (pie de imprenta SAGE, Los Ángeles); algunas librerías la fechan en 2022.

#### fondo_entry_114 · Q 81 (A) — Estimating time to conduct a meta-analysis from number of citations retrieved

- **Cita normalizada:** Allen, I., y Olkin, I. (1999). Estimating time to conduct a meta-analysis from number of citations retrieved. JAMA, 282(7), 634-635.
- **Tipo de fuente:** Artículo revisado por pares (carta de investigación)
- **Ámbito metodológico:** MB-01 Planificación y reporte de búsquedas (principal) · secundarias: MB-04
- **Calidad Q:** 81 (A) — Tipo 25/25 · Rigor 12/20 · Autoridad 14/15 · Vigencia 6/10 · Impacto 8/10 · Independencia 10/10 · Acceso 6/10
- **DOI / URL:** DOI: 10.1001/jama.282.7.634 · Confirmada en la bibliografía de la presentación de A. Booth, EPPI Centre, 2024: https://eppi.ioe.ac.uk/CMS/Portals/0/Study%20Selection%20-%20Andrew%20Booth%20-%20ESG.pdf
- **Estado:** Vigente
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «single screening versus double screening study selection systematic reviews Waffenschmidt Gartlehner»; WebFetch: sí, presentación de Booth (índice); artículo no leído)
- **Ficha metodológica:** Relación empírica entre el número de registros recuperados y las horas necesarias para completar un metaanálisis. Referencia clásica para estimar el coste de una búsqueda antes de lanzarla.
- **Criterios derivados:** Ninguno todavía.
- **Origen:** Alta V4.0 (2026-11-02). Confirmada en índice (cita con DOI).
- **Nota:** Datos de 1999; usar como orden de magnitud, completado con fondo_entry_113.

#### fondo_entry_118 · Q 78 (B) — PROTOCOL: Searching and reporting in Campbell Collaboration systematic reviews: An assessment of current methods

- **Cita normalizada:** Young, S., Bethel, A., Keenan, C., Ghezzi-Kopel, K., Moreton, E., Pickup, D., Premji, Z. A., Rogers, M., y Viinholt, B. C. A. (2021). PROTOCOL: Searching and reporting in Campbell Collaboration systematic reviews: An assessment of current methods. Campbell Systematic Reviews, 17(4), e1208.
- **Tipo de fuente:** Protocolo revisado por pares
- **Ámbito metodológico:** MB-01 Planificación y reporte de búsquedas (principal) · secundarias: MB-02
- **Calidad Q:** 78 (B) — Tipo 20/25 · Rigor 12/20 · Autoridad 12/15 · Vigencia 9/10 · Impacto 5/10 · Independencia 10/10 · Acceso 10/10
- **DOI / URL:** DOI: 10.1002/cl2.1208 · RePEc/IDEAS: https://ideas.repec.org/a/wly/camsys/v17y2021i4ne1208.html · Acceso abierto
- **Estado:** Vigente
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Campbell Collaboration Searching for studies guide to information retrieval Kugley Wade Thomas 2017»; WebFetch: sí, IDEAS)
- **Ficha metodológica:** Protocolo para evaluar cómo buscan e informan sus búsquedas las revisiones Campbell (ciencias sociales) frente a MECCIR y PRISMA, incluyendo automatización y búsqueda web. Aporta la lista de comprobaciones de auditoría de búsquedas en ciencias sociales, más próximas a la economía que las de salud.
- **Criterios derivados:** Ninguno todavía.
- **Origen:** Alta V4.0 (2026-11-02). Verificación directa.
- **Nota:** Es un protocolo: sus resultados se publican aparte; sustituir por el estudio final cuando se localice.

## MB-02 Construcción de consultas y selección de bases

#### fondo_entry_119 · Q 94 (A) — Searching for studies: A guide to information retrieval for Campbell systematic reviews

- **Cita normalizada:** MacDonald, H., Comer, C., Foster, M., Labelle, P. R., Marsalis, S., Nyhan, K., Premji, Z., Rogers, M., Splenda, R., Stansfield, C., y Young, S. (2024). Searching for studies: A guide to information retrieval for Campbell systematic reviews. Campbell Systematic Reviews, 20(3), e1433.
- **Tipo de fuente:** Artículo revisado por pares (guía metodológica institucional)
- **Ámbito metodológico:** MB-02 Construcción de consultas y selección de bases (principal) · secundarias: MB-01, MB-04
- **Calidad Q:** 94 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 7/10 · Independencia 10/10 · Acceso 10/10
- **DOI / URL:** DOI: 10.1002/cl2.1433 · RePEc/IDEAS: https://ideas.repec.org/a/wly/camsys/v20y2024i3ne1433.html · Editorial: https://journals.sagepub.com/doi/10.1002/cl2.1433 · Acceso abierto
- **Estado:** Vigente
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Campbell Collaboration Searching for studies guide to information retrieval Kugley Wade Thomas 2017»; WebFetch: sí, IDEAS)
- **Ficha metodológica:** Guía de recuperación de información de la Campbell Collaboration (ciencias sociales, educación, justicia, desarrollo): fuentes principales, planificación de la búsqueda, diseño y ejecución de estrategias, gestión de referencias y documentación y reporte. Es el equivalente para ciencias sociales del capítulo 4 de Cochrane (fondo_entry_011) y el más próximo al dominio económico.
- **Criterios derivados:** Ninguno todavía.
- **Origen:** Alta V4.0 (2026-11-02). Verificación directa. Sustituye a la guía Campbell de 2017 (Kugley et al.), que no se localizó en esta pasada.

#### fondo_entry_011 · Q 94 (A) — Chapter 4: Searching for and selecting studies

- **Cita normalizada:** Lefebvre, C., Glanville, J., Briscoe, S., Littlewood, A., Marshall, C., Metzendorf, M.-I., Noel-Storr, A., Rader, T., Shokraneh, F., Thomas, J., y Wieland, L. S. (2019). Chapter 4: Searching for and selecting studies. En Higgins, J. P. T., Thomas, J., et al. (eds.), Cochrane Handbook for Systematic Reviews of Interventions (2.ª ed.). Chichester: Wiley / Cochrane. (Versión en línea vigente: 6.5, 2024.)
- **Tipo de fuente:** Manual de referencia (capítulo)
- **Ámbito metodológico:** MB-02 Construcción de consultas y selección de bases (principal) · secundarias: MB-01, MB-03
- **Calidad Q:** 94 (A) — Tipo 20/25 · Rigor 19/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 10/10
- **DOI / URL:** DOI: 10.1002/9781119536604.ch4 (edición impresa 2019) · Repositorio institucional (University of Nottingham): https://nottingham-repository.worktribe.com/output/1380231/searching-for-and-selecting-studies · Versión en línea gratuita (archivo v6.4): https://training-noproxy.cochrane.org/zh-hans/handbook/archive/v6.4/chapter-04 · Acceso gratuito a la versión en línea del Handbook
- **Estado:** Vigente
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Cochrane Handbook Chapter 4 Searching for and selecting studies Lefebvre Glanville Briscoe»; WebFetch: sí, repositorio de Nottingham; la página de Cochrane Training bloquea la lectura automática por robots.txt)
- **Ficha metodológica:** Procedimiento de referencia para diseñar búsquedas: fuentes a consultar (bases bibliográficas, registros, literatura gris), construcción de estrategias con vocabulario controlado y texto libre, operadores booleanos y de proximidad, filtros metodológicos, documentación, gestión de registros y actualización de la búsqueda.
- **Criterios derivados:** Ninguno todavía (candidata a fuente de fondo_criterion_001 y fondo_criterion_002).
- **Origen:** Semilla V3.0 (2026-11-01); verificación de alta completada el 2026-11-02 (autores, año, DOI del capítulo impreso).
- **Nota:** El capítulo se revisa entre versiones del Handbook; citar siempre la versión en línea consultada y su fecha.

#### fondo_entry_122 · Q 92 (A) — Introduction to Information Retrieval

- **Cita normalizada:** Manning, C. D., Raghavan, P., y Schütze, H. (2008). Introduction to Information Retrieval. Cambridge: Cambridge University Press. ISBN 9780521865715.
- **Tipo de fuente:** Manual de referencia
- **Ámbito metodológico:** MB-02 Construcción de consultas y selección de bases (principal) · secundarias: MB-04
- **Calidad Q:** 92 (A) — Tipo 20/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 10/10 · Independencia 10/10 · Acceso 10/10
- **DOI / URL:** Sin DOI visto · Sitio oficial con edición en línea completa (HTML y PDF): https://nlp.stanford.edu/IR-book/
- **Estado:** Vigente
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Introduction to Information Retrieval Manning Raghavan Schütze Boolean retrieval online edition Cambridge»; WebFetch: sí, sitio del libro (Stanford NLP))
- **Ficha metodológica:** Manual de referencia de recuperación de información: modelo booleano (capítulo 1), índices invertidos, consultas de frase y proximidad, normalización y truncamiento, modelos de ranking, evaluación por exhaustividad y precisión y detección de casi duplicados. Fundamenta técnicamente cómo responden los buscadores a cada operador de una ecuación.
- **Criterios derivados:** Ninguno todavía.
- **Origen:** Alta V4.0 (2026-11-02). Verificación directa en el sitio oficial.

#### fondo_entry_101 · Q 91 (A) — Technical Supplement to Chapter 4: Searching for and selecting studies

- **Cita normalizada:** Lefebvre, C., Glanville, J., Briscoe, S., Featherstone, R., Littlewood, A., Metzendorf, M.-I., Noel-Storr, A., Paynter, R., Rader, T., Thomas, J., y Wieland, L. S., en nombre del Cochrane Information Retrieval Methods Group (2024). Technical Supplement to Chapter 4: Searching for and selecting studies. En Higgins, J. P. T., Thomas, J., Chandler, J., Cumpston, M., Li, T., Page, M. J., et al. (eds.), Cochrane Handbook for Systematic Reviews of Interventions, versión 6.5 (actualizado en septiembre de 2024). Cochrane.
- **Tipo de fuente:** Manual de referencia (suplemento técnico de capítulo)
- **Ámbito metodológico:** MB-02 Construcción de consultas y selección de bases (principal) · secundarias: MB-01, MB-04
- **Calidad Q:** 91 (A) — Tipo 20/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 8/10 · Independencia 10/10 · Acceso 10/10
- **DOI / URL:** Sin DOI visto · https://www.cochrane.org/es/authors/handbooks-and-manuals/handbook/current/chapter-04-technical-supplement-searching-and-selecting-studies · Acceso gratuito en el sitio de Cochrane
- **Estado:** Vigente
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Cochrane Handbook Chapter 4 Searching for and selecting studies Lefebvre Glanville Briscoe»; WebFetch: sí)
- **Ficha metodológica:** Desarrollo operativo del capítulo 4: detalle de fuentes y plataformas, técnicas de construcción de estrategias, filtros, búsqueda de literatura gris y registros, gestión y deduplicación de resultados y documentación. Acompañado de un apéndice de recursos (4.S2). Es el «cómo» detallado que el capítulo 4 (fondo_entry_011) resume.
- **Criterios derivados:** Ninguno todavía.
- **Origen:** Alta V4.0 (2026-11-02) por verificación directa (autores, versión, fecha y editores en la página oficial). Cuerpo del texto no extraído por la herramienta; contenido descrito a partir de la estructura del Handbook.
- **Nota:** Orientado a revisiones de intervenciones sanitarias; las técnicas de construcción de consultas son transferibles, los recursos concretos (bases biomédicas, registros de ensayos) no.

#### fondo_entry_016 · Q 91 (A) — Which academic search systems are suitable for systematic reviews or meta-analyses? Evaluating retrieval qualities of Google Scholar, PubMed, and 26 other resources

- **Cita normalizada:** Gusenbauer, M., y Haddaway, N. R. (2020). Which academic search systems are suitable for systematic reviews or meta-analyses? Evaluating retrieval qualities of Google Scholar, PubMed, and 26 other resources. Research Synthesis Methods, 11(2), 181-217.
- **Tipo de fuente:** Artículo revisado por pares
- **Ámbito metodológico:** MB-02 Construcción de consultas y selección de bases (principal) · secundarias: MB-06
- **Calidad Q:** 91 (A) — Tipo 24/25 · Rigor 17/20 · Autoridad 13/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 8/10
- **DOI / URL:** DOI: 10.1002/jrsm.1378 · Repositorio institucional (Johannes Kepler Universität Linz): https://research.jku.at/en/publications/which-academic-search-systems-are-suitable-for-systematic-reviews/ · Ficha del Stockholm Environment Institute: https://www.sei.org/publications/academic-search-suitablesystematic-reviews-analyses-google-scholar-pubmed/
- **Estado:** Vigente
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Gusenbauer Haddaway 2020 Which academic search systems are suitable for systematic reviews Google Scholar PubMed 26 other resources»; WebFetch: sí, repositorio JKU)
- **Ficha metodológica:** Evalúa 28 sistemas de búsqueda académica (Google Scholar, PubMed y otros 26) por sus cualidades de recuperación (búsqueda booleana, reproducibilidad, filtros) y distingue los aptos como sistema principal de los aptos solo como complementarios (Google Scholar, entre estos últimos). Fundamenta qué sistemas pueden sostener una búsqueda reproducible.
- **Criterios derivados:** Ninguno todavía (candidata a fuente de fondo_criterion_002: «al menos dos sistemas complementarios»).
- **Origen:** Semilla V3.0 (2026-11-01); verificación de alta completada el 2026-11-02 (autores, año, revista, volumen, páginas y DOI en el repositorio JKU).
- **Nota:** Las capacidades de los buscadores cambian; la evaluación refleja el estado de 2019. Licencia de acceso abierto no confirmada en la página leída.

#### fondo_entry_013 · Q 91 (A) — PRESS Peer Review of Electronic Search Strategies: 2015 Guideline Statement

- **Cita normalizada:** McGowan, J., Sampson, M., Salzwedel, D. M., Cogo, E., Foerster, V., y Lefebvre, C. (2016). PRESS Peer Review of Electronic Search Strategies: 2015 Guideline Statement. Journal of Clinical Epidemiology, 75, 40-46.
- **Tipo de fuente:** Artículo revisado por pares (guía)
- **Ámbito metodológico:** MB-02 Construcción de consultas y selección de bases (principal) · secundarias: MB-05
- **Calidad Q:** 91 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 8/10 · Independencia 10/10 · Acceso 7/10
- **DOI / URL:** DOI no visto en esta verificación (el de la semilla, 10.1016/j.jclinepi.2016.01.021, queda pendiente de confirmar en el barrido HT-02) · Guía resumida (CASRAI): https://casrai.org/guides/press-2015-peer-review-of-search-strategies · Página del proyecto en Canada's Drug Agency (CDA-AMC, antes CADTH), con la cita completa en J Clin Epidemiol 2016;75:40-6: https://www.cda-amc.ca/node/92248 · Artículo de revista por suscripción; informe completo gratuito (ver fondo_entry_102)
- **Estado:** Vigente
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «McGowan PRESS Peer Review of Electronic Search Strategies 2015 Guideline Statement Journal of Clinical Epidemiology»; WebFetch: sí, CASRAI y CDA-AMC)
- **Ficha metodológica:** Lista de revisión por pares de estrategias de búsqueda en seis elementos: traducción de la pregunta, operadores booleanos y de proximidad, encabezamientos de materia, búsqueda en texto libre (sinónimos, variantes, truncamiento), ortografía, sintaxis y numeración de líneas, y límites y filtros. Útil para que un segundo agente revise una estrategia antes de ejecutarla.
- **Criterios derivados:** Ninguno todavía.
- **Origen:** Semilla V3.0 (2026-11-01); verificación de alta completada el 2026-11-02 (autores, año, revista, volumen y páginas); DOI pendiente.

#### fondo_entry_120 · Q 90 (A) — Errors in search strategies used in systematic reviews and their effects on information retrieval

- **Cita normalizada:** Salvador-Oliván, J. A., Marco-Cuenca, G., y Arquero-Avilés, R. (2019). Errors in search strategies used in systematic reviews and their effects on information retrieval. Journal of the Medical Library Association, 107(2), 210-221.
- **Tipo de fuente:** Artículo revisado por pares
- **Ámbito metodológico:** MB-02 Construcción de consultas y selección de bases (principal) · secundarias: MB-05
- **Calidad Q:** 90 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 11/15 · Vigencia 10/10 · Impacto 8/10 · Independencia 10/10 · Acceso 10/10
- **DOI / URL:** DOI: 10.5195/jmla.2019.567 · Revista en acceso abierto: https://jmla.pitt.edu/ojs/jmla/article/view/567/811 · Ficha en el portal de producción científica de la UCM: https://produccioncientifica.ucm.es/documentos/5fa080c7299952440aae81bd?lang=en
- **Estado:** Vigente
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «errors in search strategies used in systematic reviews Salvador-Oliván Marco-Cuenca Arquero-Avilés»; WebFetch: sí, JMLA)
- **Ficha metodológica:** Analiza 137 revisiones sistemáticas de 2018: el 92,7 % de sus estrategias tiene al menos un error y el 78,1 % errores que reducen la exhaustividad (sinónimos ausentes 54 %, truncamiento ausente o mal colocado, términos redundantes, vocabulario controlado omitido, paréntesis ausentes). Es la lista de errores típicos que debe revisar un segundo agente antes de ejecutar una ecuación.
- **Criterios derivados:** Ninguno todavía.
- **Origen:** Alta V4.0 (2026-11-02). Verificación directa. Autores de la Universidad de Zaragoza y la Universidad Complutense de Madrid.

#### fondo_entry_100 · Q 90 (A) — A systematic approach to searching: an efficient and complete method to develop literature searches

- **Cita normalizada:** Bramer, W. M., de Jonge, G. B., Rethlefsen, M. L., Mast, F., y Kleijnen, J. (2018). A systematic approach to searching: an efficient and complete method to develop literature searches. Journal of the Medical Library Association, 106(4), 531-541.
- **Tipo de fuente:** Artículo revisado por pares (método)
- **Ámbito metodológico:** MB-02 Construcción de consultas y selección de bases (principal) · secundarias: MB-01
- **Calidad Q:** 90 (A) — Tipo 23/25 · Rigor 16/20 · Autoridad 13/15 · Vigencia 10/10 · Impacto 8/10 · Independencia 10/10 · Acceso 10/10
- **DOI / URL:** DOI: 10.5195/jmla.2018.283 · Revista en acceso abierto: https://jmla.pitt.edu/ojs/jmla/article/view/283/704
- **Estado:** Vigente
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Bramer Rethlefsen Kleijnen Franco 2017 Optimal database combinations for literature searches in systematic reviews», resultado jmla.pitt.edu; WebFetch: sí)
- **Ficha metodológica:** Método en 15 pasos para construir estrategias de búsqueda: desde aclarar la pregunta y fijar conceptos hasta probar y revisar la búsqueda final; estrategias en una sola línea redactadas en un documento de texto, optimización comparando resultados de términos de tesauro frente a texto libre para hallar sinónimos omitidos, y traducción sistemática de la sintaxis entre bases.
- **Criterios derivados:** Ninguno todavía (candidata a criterio de construcción iterativa de consultas).
- **Origen:** Alta V4.0 (2026-11-02) por verificación directa (autores, año, revista, volumen, páginas y DOI en la página de la revista).
- **Nota:** Los propios autores advierten que las estrategias en una sola línea son más difíciles de revisar y que el método rinde mejor en interfaces con operadores de proximidad (Embase.com, Ovid); en buscadores generalistas su aplicación es parcial.

#### fondo_entry_004 · Q 90 (A) — Webster y Watson (2002)

- **Cita normalizada:** Webster, J., y Watson, R. T. (2002). Analyzing the Past to Prepare for the Future: Writing a Literature Review. MIS Quarterly, 26(2), xiii-xxiii.
- **Tipo de fuente:** Artículo revisado por pares (guía editorial)
- **Ámbito metodológico:** MB-02 Construcción de consultas y selección de bases (principal) · secundarias: MB-03 (en V2.3: Consultas)
- **Calidad Q:** 90 (A) — Tipo 25/25 · Rigor 14/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 10/10 · Independencia 10/10 · Acceso 7/10
- **DOI / URL:** Sin DOI consultado en la carga de arranque. Acceso: copias de acceso público en páginas universitarias; URL concreta a fijar en la primera revisión · Verificación (anexo 8.1 V2.3): DOI verificado el 25/10/2026: 10.2307/4132319 · JSTOR: jstor.org/stable/4132319 · Página de la revista: misq.umn.edu (MIS Quarterly 26(2), xiii-xxiii)
- **Estado:** Vigente
- **Estado del enlace:** PENDIENTE_BARRIDO
- **Última verificación:** 2026-10-25
- **Ficha metodológica:** Guía clásica de redacción de revisiones de literatura; su aportación operativa al Fondo es el modelo de búsqueda por concepto-centrismo y las técnicas de búsqueda hacia atrás (referencias de los documentos centrales) y hacia adelante (citas que reciben), pilares de cualquier estrategia completa.
- **Criterios derivados:** fondo_criterion_002
- **Verificación V2.3:** Completa (carga de arranque): cita verificada el 25/10/2026; URL de la copia de referencia no consultada; comprobaciones omitidas: localización de copia estable y lectura del texto completo
- **Nota:** DOI resuelto en el anexo 8.1 V2.3 (10.2307/4132319); acceso por JSTOR.

#### fondo_entry_121 · Q 90 (A) — The design of browsing and berrypicking techniques for the online search interface

- **Cita normalizada:** Bates, M. J. (1989). The design of browsing and berrypicking techniques for the online search interface. Online Review (Emerald).
- **Tipo de fuente:** Artículo revisado por pares (modelo teórico)
- **Ámbito metodológico:** MB-02 Construcción de consultas y selección de bases (principal) · secundarias: MB-03
- **Calidad Q:** 90 (A) — Tipo 25/25 · Rigor 13/20 · Autoridad 15/15 · Vigencia 8/10 · Impacto 10/10 · Independencia 10/10 · Acceso 9/10
- **DOI / URL:** DOI: 10.1108/eb024320 · Copia de la autora (UCLA): https://pages.gseis.ucla.edu/faculty/bates/berrypicking.html · PDF: https://www.pages.gseis.ucla.edu/faculty/bates/articles/berrypicking.pdf
- **Estado:** Vigente
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Bates berrypicking browsing techniques online search interface 1989 information search tactics 1979»; WebFetch: sí, copia de la autora en UCLA)
- **Ficha metodológica:** Modelo de búsqueda «berrypicking»: la consulta evoluciona a medida que se aprende y el resultado se recoge por partes con técnicas diversas (rastreo de notas al pie, búsqueda de citas, revisión de números de una revista clave, exploración de áreas, búsqueda temática en índices y por autor). Justifica combinar la ecuación booleana con técnicas de rastreo y reformular la consulta durante la búsqueda.
- **Criterios derivados:** Ninguno todavía.
- **Origen:** Alta V4.0 (2026-11-02). Verificación directa (título, autora y año en la copia de la autora; DOI en los resultados de búsqueda).
- **Nota:** Volumen y páginas no mostrados en la copia consultada; cotejar en el barrido HT-02.

#### fondo_entry_130 · Q 89 (A) — Search where you will find most: Comparing the disciplinary coverage of 56 bibliographic databases

- **Cita normalizada:** Gusenbauer, M. (2022). Search where you will find most: Comparing the disciplinary coverage of 56 bibliographic databases. Scientometrics.
- **Tipo de fuente:** Artículo revisado por pares
- **Ámbito metodológico:** MB-02 Construcción de consultas y selección de bases (principal) · secundarias: MB-06
- **Calidad Q:** 89 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 12/15 · Vigencia 10/10 · Impacto 8/10 · Independencia 10/10 · Acceso 8/10
- **DOI / URL:** DOI: 10.1007/s11192-022-04289-7 · Reseña en infoDOCKET (Library Journal): https://www.infodocket.com/2022/05/07/journal-article-search-where-you-will-find-most-comparing-the-disciplinary-coverage-of-56-bibliographic-databases/
- **Estado:** Vigente
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Gusenbauer 2019 Google Scholar to overshadow them all comparing size of 12 academic search engines and bibliographic databases Scientometrics»; WebFetch: sí, infoDOCKET)
- **Ficha metodológica:** Compara la cobertura temática absoluta y relativa de 56 bases bibliográficas con un método basado en recuentos de consultas: la cobertura absoluta orienta las búsquedas de alta exhaustividad y la relativa la elección de bases especializadas. Permite justificar qué bases consultar para economía y finanzas.
- **Criterios derivados:** Ninguno todavía.
- **Origen:** Alta V4.0 (2026-11-02). Verificación directa (autor, revista, año y DOI en la reseña).
- **Nota:** Volumen y páginas no visibles en la página consultada.

#### fondo_entry_015 · Q 89 (A) — Optimal database combinations for literature searches in systematic reviews: a prospective exploratory study

- **Cita normalizada:** Bramer, W. M., Rethlefsen, M. L., Kleijnen, J., y Franco, O. H. (2017). Optimal database combinations for literature searches in systematic reviews: a prospective exploratory study. Systematic Reviews, 6, 245.
- **Tipo de fuente:** Artículo revisado por pares
- **Ámbito metodológico:** MB-02 Construcción de consultas y selección de bases (principal) · secundarias: MB-06
- **Calidad Q:** 89 (A) — Tipo 23/25 · Rigor 16/20 · Autoridad 13/15 · Vigencia 9/10 · Impacto 8/10 · Independencia 10/10 · Acceso 10/10
- **DOI / URL:** DOI: 10.1186/s13643-017-0644-y · PubMed Central: https://pmc.ncbi.nlm.nih.gov/articles/5718002 · PubMed: https://pubmed.ncbi.nlm.nih.gov/29208034/ · Acceso abierto, licencia CC BY 4.0
- **Estado:** Vigente
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Bramer Rethlefsen Kleijnen Franco 2017 Optimal database combinations for literature searches in systematic reviews»; WebFetch: sí, PMC)
- **Ficha metodológica:** Estudio prospectivo sobre revisiones sistemáticas reales: la combinación Embase + MEDLINE + Web of Science Core Collection + Google Scholar alcanza una exhaustividad global del 98,3 % de las referencias incluidas, frente al 92,8 % de Embase + MEDLINE. Fundamenta no depender de una sola base y combinar bases bibliográficas con un buscador académico amplio.
- **Criterios derivados:** Ninguno todavía (candidata a fuente de fondo_criterion_002).
- **Origen:** Semilla V3.0 (2026-11-01); verificación de alta completada el 2026-11-02 (cita, DOI, licencia y resultado principal).
- **Nota:** Dominio biomédico: la combinación concreta no se traslada a finanzas, pero sí el principio de medir la exhaustividad por combinación de bases.

#### fondo_entry_133 · Q 89 (A) — So many filters, so little time: the development of a search filter appraisal checklist

- **Cita normalizada:** Glanville, J., Bayliss, S., Booth, A., Dundar, Y., Fernandes, H., Fleeman, N. D., Foster, L., Fraser, C., Fry-Smith, A., Golder, S., Lefebvre, C., Miller, C., Paisley, S., Payne, L., Price, A., y Welch, K. (2008). So many filters, so little time: the development of a search filter appraisal checklist. Journal of the Medical Library Association, 96(4), 356-361.
- **Tipo de fuente:** Artículo revisado por pares
- **Ámbito metodológico:** MB-02 Construcción de consultas y selección de bases (principal) · secundarias: MB-05
- **Calidad Q:** 89 (A) — Tipo 25/25 · Rigor 15/20 · Autoridad 14/15 · Vigencia 7/10 · Impacto 8/10 · Independencia 10/10 · Acceso 10/10
- **DOI / URL:** DOI: 10.3163/1536-5050.96.4.011 · Repositorio de la University of York: https://pure.york.ac.uk/portal/en/publications/so-many-filters-so-little-time-the-development-of-a-search-filter/
- **Estado:** Vigente
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «ISSG Search Filters Resource InterTASC search filter design methodological filters Glanville»; WebFetch: sí, repositorio de York)
- **Ficha metodológica:** Lista de evaluación de filtros de búsqueda (bloques predefinidos de términos para recuperar un tipo de estudio): cómo se construyó y validó el filtro y con qué sensibilidad y precisión. Aplicable a cualquier bloque reutilizable de la ecuación, por ejemplo un filtro de «documentos de trabajo de bancos centrales».
- **Criterios derivados:** Ninguno todavía.
- **Origen:** Alta V4.0 (2026-11-02). Verificación directa.

#### fondo_entry_124 · Q 88 (A) — Shades of Grey: Guidelines for Working with the Grey Literature in Systematic Reviews for Management and Organizational Studies

- **Cita normalizada:** Adams, R. J., Smart, P., y Huff, A. S. (2017). Shades of Grey: Guidelines for Working with the Grey Literature in Systematic Reviews for Management and Organizational Studies. International Journal of Management Reviews, 19(4), 432-454.
- **Tipo de fuente:** Artículo revisado por pares (guía metodológica)
- **Ámbito metodológico:** MB-02 Construcción de consultas y selección de bases (principal) · secundarias: MB-07
- **Calidad Q:** 88 (A) — Tipo 25/25 · Rigor 15/20 · Autoridad 13/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 6/10
- **DOI / URL:** DOI: 10.1111/ijmr.12102 · Confirmada en la bibliografía de la guía de literatura gris de la Radboud University Library: https://libguides.ru.nl/greyliterature/searchstrategy
- **Estado:** Vigente
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «grey literature searching systematic reviews Godin 2015 applying search methods Adams Smart Huff shades of grey Mahood»; WebFetch: sí, guía de Radboud (índice); artículo no leído)
- **Ficha metodológica:** Directrices para incorporar literatura gris (informes de consultoras, documentos de organismos, prensa especializada) en revisiones de gestión, con una clasificación por «tonos de gris» según la autoridad y el control editorial del emisor. Es la guía más cercana al dominio empresarial y financiero del bloque.
- **Criterios derivados:** Ninguno todavía.
- **Origen:** Alta V4.0 (2026-11-02). Confirmada en índice (cita con DOI).
- **Nota:** El índice la fecha en 2016 (publicación en línea); el volumen 19(4) corresponde a 2017.

#### fondo_entry_129 · Q 87 (A) — Google Scholar to overshadow them all? Comparing the sizes of 12 academic search engines and bibliographic databases

- **Cita normalizada:** Gusenbauer, M. (2019). Google Scholar to overshadow them all? Comparing the sizes of 12 academic search engines and bibliographic databases. Scientometrics, 118(1), 177-214.
- **Tipo de fuente:** Artículo revisado por pares
- **Ámbito metodológico:** MB-02 Construcción de consultas y selección de bases (principal) · secundarias: MB-06
- **Calidad Q:** 87 (A) — Tipo 25/25 · Rigor 15/20 · Autoridad 12/15 · Vigencia 8/10 · Impacto 9/10 · Independencia 10/10 · Acceso 8/10
- **DOI / URL:** DOI: 10.1007/s11192-018-2958-5 · RePEc/IDEAS: https://ideas.repec.org/a/spr/scient/v118y2019i1d10.1007_s11192-018-2958-5.html · Repositorio JKU: https://research.jku.at/en/publications/google-scholar-to-overshadow-them-all-comparing-the-sizes-of-12-a/
- **Estado:** Vigente
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Gusenbauer 2019 Google Scholar to overshadow them all comparing size of 12 academic search engines and bibliographic databases Scientometrics»; WebFetch: sí, IDEAS)
- **Ficha metodológica:** Estima el tamaño de 12 buscadores y bases académicas mediante recuentos de consultas optimizados: Google Scholar, con unos 389 millones de registros, sería el más amplio. Informa la elección de sistemas por cobertura, a combinar con su aptitud para búsquedas reproducibles (fondo_entry_016).
- **Criterios derivados:** Ninguno todavía.
- **Origen:** Alta V4.0 (2026-11-02). Verificación directa.
- **Nota:** Tamaños de 2018; la cobertura de las bases cambia (p. ej., cierre de Microsoft Academic).

#### fondo_entry_132 · Q 87 (A) — Information retrieval in the workplace: A comparison of professional search practices

- **Cita normalizada:** Russell-Rose, T., Chamberlain, J., y Azzopardi, L. (2018). Information retrieval in the workplace: A comparison of professional search practices. Information Processing & Management, 54(6), 1042-1057.
- **Tipo de fuente:** Artículo revisado por pares
- **Ámbito metodológico:** MB-02 Construcción de consultas y selección de bases (principal) · secundarias: MB-01
- **Calidad Q:** 87 (A) — Tipo 25/25 · Rigor 15/20 · Autoridad 12/15 · Vigencia 10/10 · Impacto 7/10 · Independencia 10/10 · Acceso 8/10
- **DOI / URL:** DOI: 10.1016/j.ipm.2018.07.003 · Repositorio de Goldsmiths, University of London: https://research.gold.ac.uk/27128
- **Estado:** Vigente
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Russell-Rose Chamberlain expert search strategies information retrieval practices healthcare information professionals Boolean»; WebFetch: sí, repositorio de Goldsmiths)
- **Ficha metodológica:** Compara las prácticas de búsqueda profesional de juristas, reclutadores, documentalistas sanitarios y analistas de patentes: preferencia persistente por consultas booleanas, necesidad de gestionar y reutilizar estrategias, y distinto peso de exhaustividad frente a precisión según la profesión. Ayuda a fijar el equilibrio exhaustividad/precisión según el tipo de encargo.
- **Criterios derivados:** Ninguno todavía.
- **Origen:** Alta V4.0 (2026-11-02). Verificación directa.

#### fondo_entry_131 · Q 87 (A) — Expert search strategies: the information retrieval practices of healthcare information professionals

- **Cita normalizada:** Russell-Rose, T., y Chamberlain, J. (2017). Expert search strategies: the information retrieval practices of healthcare information professionals. JMIR Medical Informatics, 5(4), e33.
- **Tipo de fuente:** Artículo revisado por pares
- **Ámbito metodológico:** MB-02 Construcción de consultas y selección de bases (principal) · secundarias: MB-04
- **Calidad Q:** 87 (A) — Tipo 25/25 · Rigor 14/20 · Autoridad 11/15 · Vigencia 10/10 · Impacto 7/10 · Independencia 10/10 · Acceso 10/10
- **DOI / URL:** DOI: 10.2196/medinform.7680 · Repositorio de Goldsmiths, University of London: https://research.gold.ac.uk/27126 · Revista en acceso abierto: https://medinform.jmir.org/2017/4/e33
- **Estado:** Vigente
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Russell-Rose Chamberlain expert search strategies information retrieval practices healthcare information professionals Boolean»; WebFetch: sí, repositorio de Goldsmiths)
- **Ficha metodológica:** Encuesta a 107 profesionales de la información: sus búsquedas deben ser repetibles y transparentes; construir una estrategia lleva en torno a una hora y una tarea completa unas cuatro horas y 15 líneas de estrategia; revisan una mediana de 175 resultados. Da referencias de esfuerzo y de las funciones que necesita un buscador profesional (combinar consultas y resultados).
- **Criterios derivados:** Ninguno todavía.
- **Origen:** Alta V4.0 (2026-11-02). Verificación directa.

#### fondo_entry_126 · Q 85 (A) — Exploring issues in the conduct of website searching and other online sources for systematic reviews: how can we be systematic?

- **Cita normalizada:** Stansfield, C., Dickson, K., y Bangpan, M. (2016). Exploring issues in the conduct of website searching and other online sources for systematic reviews: how can we be systematic? Systematic Reviews, 5, 9.
- **Tipo de fuente:** Artículo revisado por pares
- **Ámbito metodológico:** MB-02 Construcción de consultas y selección de bases (principal) · secundarias: MB-04
- **Calidad Q:** 85 (A) — Tipo 23/25 · Rigor 14/20 · Autoridad 12/15 · Vigencia 9/10 · Impacto 7/10 · Independencia 10/10 · Acceso 10/10
- **DOI / URL:** DOI: 10.1186/s13643-016-0371-9 · Confirmada en la bibliografía de la guía de literatura gris de la Radboud University Library: https://libguides.ru.nl/greyliterature/searchstrategy · Acceso abierto
- **Estado:** Vigente
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «grey literature searching systematic reviews Godin 2015 applying search methods Adams Smart Huff shades of grey Mahood»; WebFetch: sí, guía de Radboud (índice); artículo no leído)
- **Ficha metodológica:** Problemas y soluciones para buscar de forma sistemática en sitios web y otras fuentes en línea (planificación, registro de lo consultado, límites de las funciones de búsqueda de cada sitio). Directamente aplicable a la búsqueda en webs de bancos centrales, supervisores y organismos.
- **Criterios derivados:** Ninguno todavía.
- **Origen:** Alta V4.0 (2026-11-02). Confirmada en índice (cita con DOI).

#### fondo_entry_017 · Q 85 (A) — The Role of Google Scholar in Evidence Reviews and Its Applicability to Grey Literature Searching

- **Cita normalizada:** Haddaway, N. R., Collins, A. M., Coughlin, D., y Kirk, S. (2015). The Role of Google Scholar in Evidence Reviews and Its Applicability to Grey Literature Searching. PLoS ONE, 10(9), e0138237.
- **Tipo de fuente:** Artículo revisado por pares
- **Ámbito metodológico:** MB-02 Construcción de consultas y selección de bases (principal) · secundarias: MB-06
- **Calidad Q:** 85 (A) — Tipo 22/25 · Rigor 15/20 · Autoridad 12/15 · Vigencia 8/10 · Impacto 8/10 · Independencia 10/10 · Acceso 10/10
- **DOI / URL:** DOI: 10.1371/journal.pone.0138237 · RePEc/IDEAS: https://ideas.repec.org/a/plo/pone00/0138237.html · Repositorio institucional (Imperial College, Spiral): https://spiral.imperial.ac.uk/entities/publication/961b18a6-685b-4fc5-a242-c8d624dc897e · Acceso abierto (PLOS ONE)
- **Estado:** Vigente
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Haddaway Collins Coughlin Kirk 2015 The Role of Google Scholar in Evidence Reviews grey literature PLoS ONE»; WebFetch: sí, IDEAS y Spiral)
- **Ficha metodológica:** Google Scholar localiza mucha literatura gris y estudios concretos, pero no debe usarse como única fuente de una búsqueda sistemática; como complemento, recomienda revisar por título los primeros 200–300 resultados y documentar los resultados con herramientas que hagan el proceso transparente y actualizable.
- **Criterios derivados:** Ninguno todavía.
- **Origen:** Semilla V3.0 (2026-11-01); verificación de alta completada el 2026-11-02 (cita, DOI y recomendación principal en IDEAS y Spiral).
- **Nota:** Comportamiento de Google Scholar a fecha de 2015; el número de resultados accesibles y la ordenación pueden haber cambiado.

#### fondo_entry_123 · Q 85 (A) — Applying systematic review search methods to the grey literature: a case study examining guidelines for school-based breakfast programs in Canada

- **Cita normalizada:** Godin, K., Stapleton, J., Kirkpatrick, S. I., Hanning, R. M., y Leatherdale, S. T. (2015). Applying systematic review search methods to the grey literature: a case study examining guidelines for school-based breakfast programs in Canada. Systematic Reviews, 4, 138.
- **Tipo de fuente:** Artículo revisado por pares (estudio de caso metodológico)
- **Ámbito metodológico:** MB-02 Construcción de consultas y selección de bases (principal) · secundarias: MB-01
- **Calidad Q:** 85 (A) — Tipo 23/25 · Rigor 14/20 · Autoridad 11/15 · Vigencia 9/10 · Impacto 8/10 · Independencia 10/10 · Acceso 10/10
- **DOI / URL:** DOI: 10.1186/s13643-015-0125-0 · PDF editorial: https://systematicreviewsjournal.biomedcentral.com/track/pdf/10.1186/s13643-015-0125-0 · Acceso abierto
- **Estado:** Vigente
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «grey literature searching systematic reviews Godin 2015 applying search methods Adams Smart Huff shades of grey Mahood»; WebFetch: sí, guía de Radboud (cita completa); PDF no leído)
- **Ficha metodológica:** Caso práctico que traslada la búsqueda sistemática a la literatura gris en cuatro vías: bases de literatura gris, motores de búsqueda personalizados, sitios web seleccionados y consulta a expertos, con documentación de cada vía. Modelo para buscar informes de organismos y sitios institucionales.
- **Criterios derivados:** Ninguno todavía.
- **Origen:** Alta V4.0 (2026-11-02). Confirmada en resultados de búsqueda (PDF editorial) y en la bibliografía de la guía de Radboud (https://libguides.ru.nl/greyliterature/searchstrategy).

#### fondo_entry_102 · Q 83 (A) — PRESS Peer Review of Electronic Search Strategies: 2015 Guideline Explanation and Elaboration (PRESS E&E)

- **Cita normalizada:** McGowan, J., Sampson, M., Salzwedel, D. M., Cogo, E., Foerster, V., y Lefebvre, C. (2016). PRESS – Peer Review of Electronic Search Strategies: 2015 Guideline Explanation and Elaboration (PRESS E&E). Ottawa: CADTH (Canadian Agency for Drugs and Technologies in Health), enero de 2016.
- **Tipo de fuente:** Informe técnico institucional (con revisión sistemática, encuesta y consenso)
- **Ámbito metodológico:** MB-02 Construcción de consultas y selección de bases (principal) · secundarias: MB-05
- **Calidad Q:** 83 (A) — Tipo 15/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 7/10 · Independencia 10/10 · Acceso 10/10
- **DOI / URL:** Sin DOI · Informe completo (PDF gratuito): https://www.cda-amc.ca/sites/default/files/pdf/CP0015_PRESS_Update_Report_2016.pdf · Página del proyecto: https://www.cda-amc.ca/node/92248
- **Estado:** Vigente
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «McGowan PRESS Peer Review of Electronic Search Strategies 2015 Guideline Statement Journal of Clinical Epidemiology»; WebFetch: sí, PDF y página del proyecto)
- **Ficha metodológica:** Versión extensa de la guía PRESS (fondo_entry_013): revisión sistemática de 39 estudios, encuesta a 117 expertos y foro de consenso; reduce la lista a seis elementos, incluye la lista de comprobación actualizada, el formulario de evaluación, seis recomendaciones de práctica y cuatro estrategias de implantación (revisión tras desarrollar la estrategia principal y antes de traducirla al resto de bases).
- **Criterios derivados:** Ninguno todavía (candidata a criterio de revisión por pares de estrategias entre agentes).
- **Origen:** Alta V4.0 (2026-11-02) por verificación directa (título, autores, editor y fecha en el PDF).
- **Nota:** Complementa, no sustituye, a fondo_entry_013; contexto de evaluación de tecnologías sanitarias.

#### fondo_entry_125 · Q 83 (A) — Searching for grey literature for systematic reviews: challenges and benefits

- **Cita normalizada:** Mahood, Q., Van Eerd, D., e Irvin, E. (2014). Searching for grey literature for systematic reviews: challenges and benefits. Research Synthesis Methods, 5(3), 221-234.
- **Tipo de fuente:** Artículo revisado por pares
- **Ámbito metodológico:** MB-02 Construcción de consultas y selección de bases (principal) · secundarias: MB-04
- **Calidad Q:** 83 (A) — Tipo 25/25 · Rigor 14/20 · Autoridad 12/15 · Vigencia 8/10 · Impacto 8/10 · Independencia 10/10 · Acceso 6/10
- **DOI / URL:** DOI: 10.1002/jrsm.1106 · Confirmada en la bibliografía de la guía de literatura gris de la Radboud University Library: https://libguides.ru.nl/greyliterature/searchstrategy
- **Estado:** Vigente
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «grey literature searching systematic reviews Godin 2015 applying search methods Adams Smart Huff shades of grey Mahood»; WebFetch: sí, guía de Radboud (índice); artículo no leído)
- **Ficha metodológica:** Experiencia de búsqueda de literatura gris en una revisión: dificultades (interfaces sin booleanos, exportación limitada, volumen de resultados) y beneficios (estudios no publicados en revistas). Útil para presupuestar y documentar la parte gris de una estrategia.
- **Criterios derivados:** Ninguno todavía.
- **Origen:** Alta V4.0 (2026-11-02). Confirmada en índice (cita con DOI).

#### fondo_entry_003 · Q 82 (A) — Kitchenham y Charters (2007)

- **Cita normalizada:** Kitchenham, B., y Charters, S. (2007). Guidelines for performing Systematic Literature Reviews in Software Engineering. Technical Report EBSE-2007-01, Keele University y University of Durham.
- **Tipo de fuente:** Informe técnico institucional
- **Ámbito metodológico:** MB-02 Construcción de consultas y selección de bases (principal) · secundarias: MB-01 (en V2.3: Consultas)
- **Calidad Q:** 82 (A) — Tipo 15/25 · Rigor 17/20 · Autoridad 14/15 · Vigencia 9/10 · Impacto 10/10 · Independencia 10/10 · Acceso 7/10
- **DOI / URL:** Sin DOI (informe técnico). URL: disponible legalmente en repositorios universitarios abiertos; URL concreta no consultada en la carga de arranque (fijarla en la primera revisión) · Verificación (anexo 8.1 V2.3): Informe técnico EBSE-2007-01 (Keele University y University of Durham) · Copia estable verificada el 25/10/2026: repositorio abierto EdTech Hub, docs.edtechhub.org/lib/EDAG684W · Localizable también vía Google Scholar y OpenAlex
- **Estado:** Vigente
- **Estado del enlace:** PENDIENTE_BARRIDO
- **Última verificación:** 2026-10-25
- **Ficha metodológica:** Guía operativa completa de la revisión sistemática aplicada: definición de preguntas de investigación, estrategia de búsqueda por fuentes y cadenas, criterios de inclusión y exclusión, extracción de datos y control de calidad. Complementa a PRISMA (que reporta resultados) con el procedimiento paso a paso (que los produce).
- **Criterios derivados:** fondo_criterion_002
- **Verificación V2.3:** Completa (carga de arranque): cita y existencia del informe verificadas el 25/10/2026; URL concreta no consultada; comprobaciones omitidas: localización y lectura de la copia de referencia
- **Nota:** URL concreta resuelta en el anexo 8.1 V2.3 (copia de repositorio EdTech Hub); la URL editorial original está fuera de servicio.

#### fondo_entry_128 · Q 79 (B) — Can ChatGPT Write a Good Boolean Query for Systematic Review Literature Search?

- **Cita normalizada:** Wang, S., Scells, H., Koopman, B., y Zuccon, G. (2023). Can ChatGPT Write a Good Boolean Query for Systematic Review Literature Search? arXiv:2302.03495.
- **Tipo de fuente:** Documento de trabajo (preprint)
- **Ámbito metodológico:** MB-02 Construcción de consultas y selección de bases (principal) · secundarias: MB-03
- **Calidad Q:** 79 (B) — Tipo 15/25 · Rigor 14/20 · Autoridad 12/15 · Vigencia 10/10 · Impacto 8/10 · Independencia 10/10 · Acceso 10/10
- **DOI / URL:** Sin DOI visto · arXiv: https://arxiv.org/abs/2302.03495v2
- **Estado:** Vigente
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Can ChatGPT write a good Boolean query for systematic review literature search Wang Scells Koopman Zuccon SIGIR 2023»; WebFetch: sí, arXiv)
- **Ficha metodológica:** Evalúa consultas booleanas generadas por ChatGPT en colecciones de prueba de revisiones sistemáticas: alta precisión pero menor exhaustividad que las consultas de expertos. Fundamenta que una ecuación generada por un modelo de lenguaje se revise y amplíe antes de usarse en búsquedas exhaustivas.
- **Criterios derivados:** Ninguno todavía.
- **Origen:** Alta V4.0 (2026-11-02). Verificación directa en arXiv.
- **Nota:** La página de arXiv no confirma la publicación en SIGIR 2023; tratar como preprint hasta cotejar la versión publicada. Resultados dependientes de la versión del modelo.

#### fondo_entry_134 · Q 77 (B) — The ISSG Search Filter Resource

- **Cita normalizada:** InterTASC Information Specialists' Sub-Group (ISSG) (actualización continua). The ISSG Search Filter Resource. York: University of York, Centre for Reviews and Dissemination.
- **Tipo de fuente:** Recurso institucional (repositorio de filtros con metodología)
- **Ámbito metodológico:** MB-02 Construcción de consultas y selección de bases (principal) · secundarias: MB-05
- **Calidad Q:** 77 (B) — Tipo 15/25 · Rigor 13/20 · Autoridad 14/15 · Vigencia 9/10 · Impacto 8/10 · Independencia 10/10 · Acceso 8/10
- **DOI / URL:** Sin DOI · https://www.york.ac.uk/inst/crd/intertasc/ (redirige a un sitio de Google Sites del grupo) · Presentación en el Coloquio Cochrane 2023: https://events.cochrane.org/colloquium-2023/session/1473902/the-issg-search-filter-resource-improving-the-efficiency-and-quality-of-searches-for-studies-for-systematic-reviews
- **Estado:** Vigente
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «ISSG Search Filters Resource InterTASC search filter design methodological filters Glanville»; WebFetch: intentado: la URL redirige a un dominio no leíble por la herramienta)
- **Ficha metodológica:** Repositorio de filtros de búsqueda validados y de estudios sobre su diseño y evaluación, mantenido por los especialistas en información de InterTASC. Referencia práctica para reutilizar bloques de consulta evaluados en lugar de improvisarlos.
- **Criterios derivados:** Ninguno todavía.
- **Origen:** Alta V4.0 (2026-11-02). Confirmada en resultados de búsqueda (sitio oficial y sesión del Coloquio Cochrane 2023).
- **Nota:** Orientado a bases biomédicas; para finanzas sirve como modelo de documentación de filtros, no como fuente de filtros.

#### fondo_entry_127 · Q 65 (B) — Grey literature: search strategy (Radboud University Library guide)

- **Cita normalizada:** Radboud University Library (s. f., consultada 2026-11-02). Grey literature: Search strategy [guía de biblioteca]. Nimega: Radboud Universiteit.
- **Tipo de fuente:** Divulgación especializada (guía de biblioteca universitaria)
- **Ámbito metodológico:** MB-02 Construcción de consultas y selección de bases (principal) · secundarias: MB-01, MB-03
- **Calidad Q:** 65 (B) — Tipo 8/25 · Rigor 12/20 · Autoridad 11/15 · Vigencia 10/10 · Impacto 5/10 · Independencia 10/10 · Acceso 9/10
- **DOI / URL:** Sin DOI · https://libguides.ru.nl/greyliterature/searchstrategy
- **Estado:** Vigente
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «grey literature searching systematic reviews Godin 2015 applying search methods Adams Smart Huff shades of grey Mahood»; WebFetch: sí)
- **Ficha metodológica:** Procedimiento práctico para buscar literatura gris: combinar varios métodos, elegir fuentes según el tipo de documento, redactar un plan previo, documentar cada sitio (cadena, filtros, fecha, si se cribó en pantalla o se exportó) según PRISMA-S, fijar reglas de parada por adelantado (número fijo de resultados o resultados irrelevantes consecutivos) y llevar registro de contactos con expertos.
- **Criterios derivados:** Ninguno todavía.
- **Origen:** Alta V4.0 (2026-11-02). Verificación directa.
- **Nota:** Página viva sin fecha de versión; la plantilla de plan procede de la University of Toronto (CC BY-NC-SA 4.0).

## MB-03 Filtrado, cribado y bola de nieve

#### fondo_entry_145 · Q 94 (A) — Single screening versus conventional double screening for study selection in systematic reviews: a methodological systematic review

- **Cita normalizada:** Waffenschmidt, S., Knelangen, M., Sieben, W., Bühn, S., y Pieper, D. (2019). Single screening versus conventional double screening for study selection in systematic reviews: a methodological systematic review. BMC Medical Research Methodology, 19(1).
- **Tipo de fuente:** Artículo revisado por pares (revisión sistemática metodológica)
- **Ámbito metodológico:** MB-03 Filtrado, cribado y bola de nieve (principal)
- **Calidad Q:** 94 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 13/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 10/10
- **DOI / URL:** DOI: 10.1186/s12874-019-0782-0 · PDF editorial: https://bmcmedresmethodol.biomedcentral.com/track/pdf/10.1186/s12874-019-0782-0 · DOAJ: https://doaj.org/article/567ba97f039f4e4d9c3ad7691033edaf · Acceso abierto
- **Estado:** Vigente
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «single screening versus double screening study selection systematic reviews Waffenschmidt Gartlehner»; WebFetch: intentado: el PDF redirige a un dominio no leíble; cita completa cotejada en la presentación de Booth (índice))
- **Ficha metodológica:** Revisión metodológica que compara el cribado por un solo revisor frente al doble cribado independiente: el cribado simple pierde más estudios relevantes, por lo que el doble cribado sigue siendo la norma en revisiones exhaustivas. Justifica la doble revisión (dos agentes) en los encargos de nivel alto.
- **Criterios derivados:** Ninguno todavía.
- **Origen:** Alta V4.0 (2026-11-02). Confirmada en resultados de búsqueda y en la bibliografía de la presentación de Booth (https://eppi.ioe.ac.uk/CMS/Portals/0/Study%20Selection%20-%20Andrew%20Booth%20-%20ESG.pdf).
- **Nota:** Número de artículo no visto.

#### fondo_entry_149 · Q 94 (A) — Using text mining for study identification in systematic reviews: a systematic review of current approaches

- **Cita normalizada:** O'Mara-Eves, A., Thomas, J., McNaught, J., Miwa, M., y Ananiadou, S. (2015). Using text mining for study identification in systematic reviews: a systematic review of current approaches. Systematic Reviews, 4, 5.
- **Tipo de fuente:** Artículo revisado por pares (revisión sistemática)
- **Ámbito metodológico:** MB-03 Filtrado, cribado y bola de nieve (principal) · secundarias: MB-04
- **Calidad Q:** 94 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 14/15 · Vigencia 8/10 · Impacto 10/10 · Independencia 10/10 · Acceso 10/10
- **DOI / URL:** Sin DOI visto · Confirmada en la bibliografía de la presentación de A. Booth sobre selección de estudios (EPPI Centre, 2024): https://eppi.ioe.ac.uk/CMS/Portals/0/Study%20Selection%20-%20Andrew%20Booth%20-%20ESG.pdf · Systematic Reviews, acceso abierto
- **Estado:** Vigente
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «single screening versus double screening study selection systematic reviews Waffenschmidt Gartlehner»; WebFetch: sí, presentación de Booth (índice); artículo no leído)
- **Ficha metodológica:** Revisión sistemática del uso de minería de textos para identificar estudios: reducción de carga de cribado, priorización y clasificación automática, con sus riesgos de pérdida de estudios. Base para decidir cuándo un agente puede priorizar o descartar registros automáticamente.
- **Criterios derivados:** Ninguno todavía.
- **Origen:** Alta V4.0 (2026-11-02). Confirmada en índice.

#### fondo_entry_136 · Q 92 (A) — Successful combination of database search and snowballing for identification of primary studies in systematic literature studies

- **Cita normalizada:** Wohlin, C., Kalinowski, M., Felizardo, K. R., y Mendes, E. (2022). Successful combination of database search and snowballing for identification of primary studies in systematic literature studies. Information and Software Technology, 147, 106908.
- **Tipo de fuente:** Artículo revisado por pares
- **Ámbito metodológico:** MB-03 Filtrado, cribado y bola de nieve (principal) · secundarias: MB-02
- **Calidad Q:** 92 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 8/10 · Independencia 10/10 · Acceso 9/10
- **DOI / URL:** DOI: 10.1016/j.infsof.2022.106908 · arXiv: https://arxiv.org/abs/2307.02612 · Ficha en el sitio EBSE de Durham: https://ebse.webspace.durham.ac.uk/ebse-bibliography/successful-combination-of-database-search-and-snowballing-for-identification-of-primary-studies-in-systematic-literature-studies/
- **Estado:** Vigente
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Wohlin Kalinowski Felizardo Mendes successful combination of database search and snowballing identification of primary studies»; WebFetch: sí, arXiv; revista y volumen cotejados en la bibliografía de litball)
- **Ficha metodológica:** Replica una revisión con una estrategia híbrida (búsqueda en bases + bola de nieve) y encuentra en torno a un 30 % más de estudios relevantes; introduce los conceptos de «comodines» y «artículos limítrofes» para no excluir por error trabajos dudosos. Actualiza y refuerza fondo_entry_006 (Wohlin 2014).
- **Criterios derivados:** Ninguno todavía.
- **Origen:** Alta V4.0 (2026-11-02). Verificación directa.

#### fondo_entry_143 · Q 91 (A) — Citation tracking for systematic literature searching: A scoping review

- **Cita normalizada:** Hirt, J., Nordhausen, T., Appenzeller-Herzog, C., y Ewald, H. (2023). Citation tracking for systematic literature searching: A scoping review. Research Synthesis Methods, 14(3), 563-579.
- **Tipo de fuente:** Artículo revisado por pares (revisión de alcance)
- **Ámbito metodológico:** MB-03 Filtrado, cribado y bola de nieve (principal) · secundarias: MB-02
- **Calidad Q:** 91 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 12/15 · Vigencia 10/10 · Impacto 8/10 · Independencia 10/10 · Acceso 9/10
- **DOI / URL:** DOI: 10.1002/jrsm.1635 · Repositorio de la Universität Basel: https://edoc.unibas.ch/94515 · Versión de autor (Cochrane Deutschland): https://www.cochrane.de/sites/cochrane.de/files/uploads/Hirt%20et%20al._2022_PP.pdf
- **Estado:** Vigente
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «citation tracking systematic literature searching scoping review Hirt backward forward citationchaser»; WebFetch: sí, repositorio de Basilea)
- **Ficha metodológica:** Revisión de 47 estudios sobre rastreo de citas (hacia atrás y hacia adelante) en búsquedas sistemáticas: el 96 % lo considera un complemento útil; los índices más usados son SCI y SSCI; el uso de varios índices en paralelo, la cocitación y las iteraciones repetidas es raro y la terminología es inconsistente. Da el vocabulario y las variantes para documentar la bola de nieve.
- **Criterios derivados:** Ninguno todavía.
- **Origen:** Alta V4.0 (2026-11-02). Verificación directa (revista deducida del DOI y del contexto; la página no la nombra).
- **Nota:** Ámbito sanitario; los autores anuncian un Delphi para recomendaciones de uso y reporte.

#### fondo_entry_148 · Q 91 (A) — Increasing the efficiency of study selection for systematic reviews using prioritization tools and a single-screening approach

- **Cita normalizada:** Waffenschmidt, S., Sieben, W., Jakubeit, T., Knelangen, M., Overesch, I., Bühn, S., Pieper, D., Skoetz, N., y Hausner, E. (2023). Increasing the efficiency of study selection for systematic reviews using prioritization tools and a single-screening approach. Systematic Reviews, 12, 161.
- **Tipo de fuente:** Artículo revisado por pares
- **Ámbito metodológico:** MB-03 Filtrado, cribado y bola de nieve (principal) · secundarias: MB-04
- **Calidad Q:** 91 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 13/15 · Vigencia 10/10 · Impacto 7/10 · Independencia 10/10 · Acceso 10/10
- **DOI / URL:** DOI: 10.1186/s13643-023-02334-x · PDF editorial: https://systematicreviewsjournal.biomedcentral.com/counter/pdf/10.1186/s13643-023-02334-x.pdf · Acceso abierto
- **Estado:** Vigente
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «single screening versus double screening study selection systematic reviews Waffenschmidt Gartlehner»; WebFetch: sí, PDF editorial)
- **Ficha metodológica:** EPPI-Reviewer priorizó antes que Rayyan (88 % frente a 66 % de relevantes tras cribar la mitad), pero no lo bastante para cribar solo la mitad; el cribado simple bastó solo si se complementaba con listas de referencias y registros. Concluye que el doble cribado sigue justificado en muchos casos.
- **Criterios derivados:** Ninguno todavía.
- **Origen:** Alta V4.0 (2026-11-02). Verificación directa. Su protocolo (Waffenschmidt et al. 2018, Systematic Reviews 7, DOI 10.1186/s13643-018-0839-x) también se confirmó y no se da de alta por redundante.

#### fondo_entry_146 · Q 91 (A) — Single-reviewer abstract screening missed 13 percent of relevant studies: a crowd-based, randomized controlled trial

- **Cita normalizada:** Gartlehner, G., Affengruber, L., Titscher, V., Noel-Storr, A., Dooley, G., Ballarini, N., y König, F. (2020). Single-reviewer abstract screening missed 13 percent of relevant studies: a crowd-based, randomized controlled trial. Journal of Clinical Epidemiology, 121, 20-28.
- **Tipo de fuente:** Artículo revisado por pares (ensayo aleatorizado)
- **Ámbito metodológico:** MB-03 Filtrado, cribado y bola de nieve (principal)
- **Calidad Q:** 91 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 13/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 6/10
- **DOI / URL:** Sin DOI visto · Confirmada en la bibliografía de la presentación de A. Booth sobre selección de estudios (EPPI Centre, 2024): https://eppi.ioe.ac.uk/CMS/Portals/0/Study%20Selection%20-%20Andrew%20Booth%20-%20ESG.pdf
- **Estado:** Vigente
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «single screening versus double screening study selection systematic reviews Waffenschmidt Gartlehner»; WebFetch: sí, presentación de Booth (índice); artículo no leído)
- **Ficha metodológica:** Ensayo aleatorizado con cribadores de Cochrane Crowd: el cribado de resúmenes por un solo revisor perdió de media el 13 % de los estudios relevantes. Cuantifica el coste de prescindir del segundo revisor.
- **Criterios derivados:** Ninguno todavía.
- **Origen:** Alta V4.0 (2026-11-02). Confirmada en índice.

#### fondo_entry_150 · Q 91 (A) — Semi-automated screening of biomedical citations for systematic reviews

- **Cita normalizada:** Wallace, B. C., Trikalinos, T. A., Lau, J., Brodley, C., y Schmid, C. H. (2010). Semi-automated screening of biomedical citations for systematic reviews. BMC Bioinformatics, 11, 55.
- **Tipo de fuente:** Artículo revisado por pares
- **Ámbito metodológico:** MB-03 Filtrado, cribado y bola de nieve (principal) · secundarias: MB-04
- **Calidad Q:** 91 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 13/15 · Vigencia 8/10 · Impacto 9/10 · Independencia 10/10 · Acceso 10/10
- **DOI / URL:** Sin DOI visto · Confirmada en la bibliografía de la presentación de A. Booth sobre selección de estudios (EPPI Centre, 2024): https://eppi.ioe.ac.uk/CMS/Portals/0/Study%20Selection%20-%20Andrew%20Booth%20-%20ESG.pdf · BMC Bioinformatics, acceso abierto
- **Estado:** Vigente
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «single screening versus double screening study selection systematic reviews Waffenschmidt Gartlehner»; WebFetch: sí, presentación de Booth (índice); artículo no leído)
- **Ficha metodológica:** Cribado semiautomático de citas mediante clasificadores entrenados con las decisiones del revisor. Antecedente de las herramientas de cribado asistido como Abstrackr (fondo_entry_152).
- **Criterios derivados:** Ninguno todavía.
- **Origen:** Alta V4.0 (2026-11-02). Confirmada en índice.

#### fondo_entry_135 · Q 91 (A) — Effectiveness and efficiency of search methods in systematic reviews of complex evidence: audit of primary sources

- **Cita normalizada:** Greenhalgh, T., y Peacock, R. (2005). Effectiveness and efficiency of search methods in systematic reviews of complex evidence: audit of primary sources. BMJ, 331(7524), 1064-1065.
- **Tipo de fuente:** Artículo revisado por pares
- **Ámbito metodológico:** MB-03 Filtrado, cribado y bola de nieve (principal) · secundarias: MB-02
- **Calidad Q:** 91 (A) — Tipo 25/25 · Rigor 14/20 · Autoridad 14/15 · Vigencia 9/10 · Impacto 10/10 · Independencia 10/10 · Acceso 9/10
- **DOI / URL:** DOI: 10.1136/bmj.38636.593461.68 · Repositorio de la Middlesex University: https://repository.mdx.ac.uk/item/80vw1 · PMC: https://pmc.ncbi.nlm.nih.gov/articles/PMC1283190
- **Estado:** Vigente
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Greenhalgh Peacock 2005 effectiveness efficiency search methods systematic reviews complex evidence audit of primary sources snowballing»; WebFetch: sí, repositorio de Middlesex; autores cotejados en la bibliografía de litball)
- **Ficha metodológica:** Auditoría del origen de las fuentes de una revisión de evidencia compleja: la búsqueda protocolizada en bases encontró una parte minoritaria, y el rastreo de citas desde documentos clave localizó trabajos que de otro modo se habrían perdido. Fundamento empírico de exigir bola de nieve además de la búsqueda en bases (fondo_criterion_002).
- **Criterios derivados:** Ninguno todavía.
- **Origen:** Alta V4.0 (2026-11-02). Verificación directa.
- **Nota:** El repositorio invierte el orden de autores; se sigue el orden de la publicación (Greenhalgh, Peacock) que da la bibliografía de litball. Porcentajes no leídos en esta verificación.

#### fondo_entry_010 · Q 91 (A) — Goodman (1961)

- **Cita normalizada:** Goodman, L. A. (1961). Snowball Sampling. The Annals of Mathematical Statistics, 32(1), 148-170.
- **Tipo de fuente:** Artículo revisado por pares (origen histórico)
- **Ámbito metodológico:** MB-03 Filtrado, cribado y bola de nieve (principal) (en V2.3: Filtrado)
- **Calidad Q:** 91 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 15/15 · Vigencia 7/10 · Impacto 9/10 · Independencia 10/10 · Acceso 9/10
- **DOI / URL:** DOI: no consultado en la carga de arranque · Localización: JSTOR (acceso por suscripción) · Verificación (anexo 8.1 V2.3): DOI verificado el 25/10/2026: 10.1214/aoms/1177705148 · Project Euclid, acceso abierto: projecteuclid.org (Annals of Mathematical Statistics 32(1), 148-170)
- **Estado:** En revisión
- **Estado del enlace:** PENDIENTE_BARRIDO
- **Última verificación:** 2026-10-25
- **Ficha metodológica:** Formulación original matemática del muestreo por bola de nieve, del que procede la técnica de expansión del corpus por referencias. Su valor es fundacional: fundamenta el criterio fondo_criterion_003 junto a las directrices modernas de Wohlin (fondo_entry_006).
- **Criterios derivados:** Ninguno aún (destilación pendiente de acceso al texto completo)
- **Verificación V2.3:** Ligera (carga de arranque): cita y localización JSTOR verificadas el 25/10/2026; DOI no consultado; texto completo no obtenido (peldaño 5 de la escalera); comprobaciones omitidas: DOI, lectura del contenido completo
- **Nota:** DOI resuelto en el anexo 8.1 V2.3 (10.1214/aoms/1177705148); acceso abierto en Project Euclid según ese anexo.

#### fondo_entry_137 · Q 89 (A) — On the performance of hybrid search strategies for systematic literature reviews in software engineering

- **Cita normalizada:** Mourão, E., Pimentel, J. F., Murta, L., Kalinowski, M., Mendes, E., y Wohlin, C. (2020). On the performance of hybrid search strategies for systematic literature reviews in software engineering. Information and Software Technology, 123, 106294.
- **Tipo de fuente:** Artículo revisado por pares
- **Ámbito metodológico:** MB-03 Filtrado, cribado y bola de nieve (principal) · secundarias: MB-02
- **Calidad Q:** 89 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 12/15 · Vigencia 10/10 · Impacto 7/10 · Independencia 10/10 · Acceso 9/10
- **DOI / URL:** DOI: 10.1016/j.infsof.2020.106294 · arXiv: https://arxiv.org/abs/2004.09741v1
- **Estado:** Vigente
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Wohlin Kalinowski Felizardo Mendes successful combination of database search and snowballing identification of primary studies»; WebFetch: sí, arXiv; revista y volumen cotejados en la bibliografía de litball)
- **Ficha metodológica:** Compara cuatro estrategias híbridas (biblioteca digital + bola de nieve hacia atrás y hacia adelante, iterativa, en paralelo o secuencial) en tres revisiones: Scopus con bola de nieve paralela o secuencial dio el mejor equilibrio de precisión y exhaustividad. Orienta el orden de las pasadas de bola de nieve.
- **Criterios derivados:** Ninguno todavía.
- **Origen:** Alta V4.0 (2026-11-02). Verificación directa.

#### fondo_entry_006 · Q 89 (A) — Wohlin (2014)

- **Cita normalizada:** Wohlin, C. (2014). Guidelines for Snowballing in Systematic Literature Studies and a Replication in Software Engineering. Proceedings of EASE '14, ACM, Londres.
- **Tipo de fuente:** Artículo de congreso revisado por pares
- **Ámbito metodológico:** MB-03 Filtrado, cribado y bola de nieve (principal) (en V2.3: Filtrado)
- **Calidad Q:** 89 (A) — Tipo 20/25 · Rigor 16/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 10/10
- **DOI / URL:** DOI: 10.1145/2601248.2601268 · PDF de autor: wohlin.eu/ease14.pdf (acceso gratuito verificado) · Verificación (anexo 8.1 V2.3): DOI: doi.org/10.1145/2601248.2601268 (ACM Digital Library, ficha) · PDF de autor: wohlin.eu/ease14.pdf (ficha)
- **Estado:** Vigente
- **Estado del enlace:** PENDIENTE_BARRIDO
- **Última verificación:** 2026-10-25
- **Ficha metodológica:** Directrices operativas de la bola de nieve como estrategia de búsqueda: iteraciones hacia atrás y hacia adelante, criterios de inclusión por iteración y reglas de parada. Legitima y disciplina el snowballing dentro de las estrategias del bloque, con trazabilidad de cada iteración.
- **Criterios derivados:** fondo_criterion_003
- **Verificación V2.3:** Completa (carga de arranque): cita, DOI y PDF de autor verificados el 25/10/2026; comprobaciones omitidas: lectura del texto completo por el Documentador

#### fondo_entry_152 · Q 88 (A) — Faster title and abstract screening? Evaluating Abstrackr, a semi-automated online screening program for systematic reviewers

- **Cita normalizada:** Rathbone, J., Hoffmann, T., y Glasziou, P. (2015). Faster title and abstract screening? Evaluating Abstrackr, a semi-automated online screening program for systematic reviewers. Systematic Reviews, 4, 80.
- **Tipo de fuente:** Artículo revisado por pares
- **Ámbito metodológico:** MB-03 Filtrado, cribado y bola de nieve (principal) · secundarias: MB-04
- **Calidad Q:** 88 (A) — Tipo 25/25 · Rigor 15/20 · Autoridad 13/15 · Vigencia 7/10 · Impacto 8/10 · Independencia 10/10 · Acceso 10/10
- **DOI / URL:** DOI: 10.1186/s13643-015-0067-6 · Confirmada en la bibliografía de la presentación de A. Booth sobre selección de estudios (EPPI Centre, 2024): https://eppi.ioe.ac.uk/CMS/Portals/0/Study%20Selection%20-%20Andrew%20Booth%20-%20ESG.pdf
- **Estado:** Vigente
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «single screening versus double screening study selection systematic reviews Waffenschmidt Gartlehner»; WebFetch: sí, presentación de Booth (índice); artículo no leído)
- **Ficha metodológica:** Evalúa Abstrackr (cribado semiautomático por aprendizaje activo) en revisiones reales: ahorro de carga y riesgo de omisiones. Útil como referencia de rendimiento del cribado asistido.
- **Criterios derivados:** Ninguno todavía.
- **Origen:** Alta V4.0 (2026-11-02). Confirmada en índice (cita con DOI).

#### fondo_entry_151 · Q 87 (A) — The SAFE procedure: a practical stopping heuristic for active learning-based screening in systematic reviews and meta-analyses

- **Cita normalizada:** Boetje, J., y van de Schoot, R. (2024). The SAFE procedure: a practical stopping heuristic for active learning-based screening in systematic reviews and meta-analyses. Systematic Reviews, 13, 81.
- **Tipo de fuente:** Artículo revisado por pares
- **Ámbito metodológico:** MB-03 Filtrado, cribado y bola de nieve (principal)
- **Calidad Q:** 87 (A) — Tipo 25/25 · Rigor 14/20 · Autoridad 12/15 · Vigencia 10/10 · Impacto 7/10 · Independencia 9/10 · Acceso 10/10
- **DOI / URL:** DOI: 10.1186/s13643-024-02502-7 · Repositorio de la Open Universiteit: https://research.ou.nl/en/publications/the-safe-procedure-a-practical-stopping-heuristic-for-active-lear/ · Acceso abierto
- **Estado:** Vigente
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «stopping criteria technology-assisted review active learning screening systematic reviews ASReview SAFE procedure»; WebFetch: sí, repositorio de la Open Universiteit)
- **Ficha metodológica:** Conjunto conservador de heurísticas de parada para el cribado por aprendizaje activo (p. ej., con ASReview), que combina varias reglas para reducir el riesgo de perder estudios relevantes. Da al bloque una regla de parada declarable para el cribado asistido (fondo_criterion_003).
- **Criterios derivados:** Ninguno todavía.
- **Origen:** Alta V4.0 (2026-11-02). Verificación directa.
- **Nota:** Autores vinculados al proyecto ASReview.

#### fondo_entry_156 · Q 87 (A) — Assessing the accuracy of machine-assisted abstract screening with DistillerAI: a user study

- **Cita normalizada:** Gartlehner, G., Wagner, G., Lux, L. J., et al. (2019). Assessing the accuracy of machine-assisted abstract screening with DistillerAI: a user study. Systematic Reviews, 8(1).
- **Tipo de fuente:** Artículo revisado por pares
- **Ámbito metodológico:** MB-03 Filtrado, cribado y bola de nieve (principal) · secundarias: MB-04
- **Calidad Q:** 87 (A) — Tipo 25/25 · Rigor 14/20 · Autoridad 12/15 · Vigencia 9/10 · Impacto 7/10 · Independencia 10/10 · Acceso 10/10
- **DOI / URL:** DOI: 10.1186/s13643-019-1221-3 · Confirmada en la bibliografía de la presentación de A. Booth sobre selección de estudios (EPPI Centre, 2024): https://eppi.ioe.ac.uk/CMS/Portals/0/Study%20Selection%20-%20Andrew%20Booth%20-%20ESG.pdf
- **Estado:** Vigente
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «single screening versus double screening study selection systematic reviews Waffenschmidt Gartlehner»; WebFetch: sí, presentación de Booth (índice); artículo no leído)
- **Ficha metodológica:** Estudio de usuario sobre la exactitud del cribado de resúmenes asistido por DistillerAI frente al cribado humano. Aporta datos para decidir si un clasificador puede actuar como segundo revisor.
- **Criterios derivados:** Ninguno todavía.
- **Origen:** Alta V4.0 (2026-11-02). Confirmada en índice (cita con DOI).

#### fondo_entry_144 · Q 86 (A) — Citationchaser: A tool for transparent and efficient forward and backward citation chasing in systematic searching

- **Cita normalizada:** Haddaway, N. R., Grainger, M. J., y Gray, C. T. (2022). Citationchaser: A tool for transparent and efficient forward and backward citation chasing in systematic searching. Research Synthesis Methods, 13(4), 533-545.
- **Tipo de fuente:** Artículo revisado por pares (herramienta)
- **Ámbito metodológico:** MB-03 Filtrado, cribado y bola de nieve (principal) · secundarias: MB-04
- **Calidad Q:** 86 (A) — Tipo 25/25 · Rigor 14/20 · Autoridad 12/15 · Vigencia 10/10 · Impacto 8/10 · Independencia 8/10 · Acceso 9/10
- **DOI / URL:** DOI: 10.1002/jrsm.1563 · Ficha en la wiki de la University of British Columbia: https://wiki.ubc.ca/Citationchaser · Aplicación: https://estech.shinyapps.io/citationchaser/
- **Estado:** Vigente
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «citationchaser R package Shiny app forward backward citation chasing Haddaway Grainger Gray Research Synthesis Methods»; WebFetch: sí, wiki de UBC)
- **Ficha metodológica:** Herramienta abierta (paquete R y aplicación Shiny) que automatiza el rastreo de citas hacia atrás y hacia adelante a partir de una lista de DOI o un archivo RIS/BibTeX, usando la API de Lens.org, y exporta los resultados en RIS. Hace reproducible y documentable cada iteración de bola de nieve.
- **Criterios derivados:** Ninguno todavía.
- **Origen:** Alta V4.0 (2026-11-02). Verificación directa.
- **Nota:** Artículo de los autores de la herramienta (independencia limitada); depende de la cobertura de Lens.org.

#### fondo_entry_147 · Q 86 (A) — The value of a second reviewer for study selection in systematic reviews

- **Cita normalizada:** Stoll, C. R. T., Izadi, S., Fowler, S., Green, P., Suls, J., y Colditz, G. A. (2019). The value of a second reviewer for study selection in systematic reviews. Research Synthesis Methods, 10(4), 539-545.
- **Tipo de fuente:** Artículo revisado por pares
- **Ámbito metodológico:** MB-03 Filtrado, cribado y bola de nieve (principal)
- **Calidad Q:** 86 (A) — Tipo 25/25 · Rigor 15/20 · Autoridad 12/15 · Vigencia 10/10 · Impacto 8/10 · Independencia 10/10 · Acceso 6/10
- **DOI / URL:** DOI: 10.1002/jrsm.1369 · Confirmada en la bibliografía de la presentación de A. Booth sobre selección de estudios (EPPI Centre, 2024): https://eppi.ioe.ac.uk/CMS/Portals/0/Study%20Selection%20-%20Andrew%20Booth%20-%20ESG.pdf
- **Estado:** Vigente
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «single screening versus double screening study selection systematic reviews Waffenschmidt Gartlehner»; WebFetch: sí, presentación de Booth (índice); artículo no leído)
- **Ficha metodológica:** Cuantifica cuántos estudios elegibles añade el segundo revisor en la selección: el doble cribado identifica más estudios que uno solo. Complementa a fondo_entry_145 y fondo_entry_146.
- **Criterios derivados:** Ninguno todavía.
- **Origen:** Alta V4.0 (2026-11-02). Confirmada en índice (cita con DOI); iniciales de autores según el índice («Stoll C, Izadi S, Fowler SA…»).

#### fondo_entry_153 · Q 85 (A) — Pinpointing needles in giant haystacks: use of text mining to reduce impractical screening workload in extremely large scoping reviews

- **Cita normalizada:** Shemilt, I., et al. (2014). Pinpointing needles in giant haystacks: use of text mining to reduce impractical screening workload in extremely large scoping reviews. Research Synthesis Methods, 5(1), 31-49.
- **Tipo de fuente:** Artículo revisado por pares
- **Ámbito metodológico:** MB-03 Filtrado, cribado y bola de nieve (principal) · secundarias: MB-04
- **Calidad Q:** 85 (A) — Tipo 25/25 · Rigor 15/20 · Autoridad 13/15 · Vigencia 8/10 · Impacto 8/10 · Independencia 10/10 · Acceso 6/10
- **DOI / URL:** Sin DOI visto · Confirmada en la bibliografía de la presentación de A. Booth sobre selección de estudios (EPPI Centre, 2024): https://eppi.ioe.ac.uk/CMS/Portals/0/Study%20Selection%20-%20Andrew%20Booth%20-%20ESG.pdf
- **Estado:** Vigente
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «single screening versus double screening study selection systematic reviews Waffenschmidt Gartlehner»; WebFetch: sí, presentación de Booth (índice); artículo no leído)
- **Ficha metodológica:** Uso de minería de textos para hacer abordables revisiones de alcance con volúmenes de registros inmanejables a mano. Útil para búsquedas amplias sobre temas financieros con miles de resultados.
- **Criterios derivados:** Ninguno todavía.
- **Origen:** Alta V4.0 (2026-11-02). Confirmada en índice (autores distintos del primero no listados).

#### fondo_entry_142 · Q 84 (A) — SYMBALS: A systematic review methodology blending active learning and snowballing

- **Cita normalizada:** van Haastrecht, M., et al. (2021). SYMBALS: A systematic review methodology blending active learning and snowballing. Frontiers in Research Metrics and Analytics, 6, 685591.
- **Tipo de fuente:** Artículo revisado por pares (método)
- **Ámbito metodológico:** MB-03 Filtrado, cribado y bola de nieve (principal) · secundarias: MB-02
- **Calidad Q:** 84 (A) — Tipo 25/25 · Rigor 14/20 · Autoridad 10/15 · Vigencia 10/10 · Impacto 6/10 · Independencia 10/10 · Acceso 9/10
- **DOI / URL:** Sin DOI visto · Confirmada en la bibliografía sobre bola de nieve de la documentación de litball: https://litball.readthedocs.io/en/latest/literature.html · Frontiers, acceso abierto
- **Estado:** Vigente
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Wohlin Kalinowski Felizardo Mendes successful combination of database search and snowballing identification of primary studies»; WebFetch: sí, bibliografía de litball (índice); artículo no leído)
- **Ficha metodológica:** Metodología que combina cribado por aprendizaje activo con bola de nieve hacia atrás y hacia adelante, con criterios de parada en cada fase. Modelo para encadenar cribado asistido y expansión del corpus.
- **Criterios derivados:** Ninguno todavía.
- **Origen:** Alta V4.0 (2026-11-02). Confirmada en índice.

#### fondo_entry_158 · Q 84 (A) — Aligning text mining and machine learning algorithms with best practices for study selection in systematic literature reviews

- **Cita normalizada:** Popoff, E., et al. (2020). Aligning text mining and machine learning algorithms with best practices for study selection in systematic literature reviews. Systematic Reviews, 9(1).
- **Tipo de fuente:** Artículo revisado por pares
- **Ámbito metodológico:** MB-03 Filtrado, cribado y bola de nieve (principal)
- **Calidad Q:** 84 (A) — Tipo 25/25 · Rigor 14/20 · Autoridad 10/15 · Vigencia 10/10 · Impacto 6/10 · Independencia 9/10 · Acceso 10/10
- **DOI / URL:** DOI: 10.1186/s13643-020-01520-5 · Confirmada en la bibliografía de la presentación de A. Booth sobre selección de estudios (EPPI Centre, 2024): https://eppi.ioe.ac.uk/CMS/Portals/0/Study%20Selection%20-%20Andrew%20Booth%20-%20ESG.pdf
- **Estado:** Vigente
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «single screening versus double screening study selection systematic reviews Waffenschmidt Gartlehner»; WebFetch: sí, presentación de Booth (índice); artículo no leído)
- **Ficha metodológica:** Propone cómo integrar algoritmos de minería de textos y aprendizaje automático en la selección de estudios respetando las buenas prácticas (doble revisión, trazabilidad de decisiones). Útil para fijar las reglas de uso del cribado automático por los agentes.
- **Criterios derivados:** Ninguno todavía.
- **Origen:** Alta V4.0 (2026-11-02). Confirmada en índice (cita con DOI).

#### fondo_entry_155 · Q 84 (A) — Selecting and appraising studies for a systematic review

- **Cita normalizada:** Meade, M. O., y Richardson, W. S. (1997). Selecting and appraising studies for a systematic review. Annals of Internal Medicine, 127, 531-537.
- **Tipo de fuente:** Artículo revisado por pares (guía)
- **Ámbito metodológico:** MB-03 Filtrado, cribado y bola de nieve (principal)
- **Calidad Q:** 84 (A) — Tipo 25/25 · Rigor 13/20 · Autoridad 14/15 · Vigencia 7/10 · Impacto 9/10 · Independencia 10/10 · Acceso 6/10
- **DOI / URL:** Sin DOI visto · Confirmada en la bibliografía de la presentación de A. Booth sobre selección de estudios (EPPI Centre, 2024): https://eppi.ioe.ac.uk/CMS/Portals/0/Study%20Selection%20-%20Andrew%20Booth%20-%20ESG.pdf
- **Estado:** Vigente
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «single screening versus double screening study selection systematic reviews Waffenschmidt Gartlehner»; WebFetch: sí, presentación de Booth (índice); artículo no leído)
- **Ficha metodológica:** Guía clásica para seleccionar estudios con criterios de inclusión explícitos aplicados de forma reproducible y evaluar su calidad. Referencia de base del paso de cribado.
- **Criterios derivados:** Ninguno todavía.
- **Origen:** Alta V4.0 (2026-11-02). Confirmada en índice.

#### fondo_entry_138 · Q 81 (A) — Experiences from using snowballing and database searches in systematic literature studies

- **Cita normalizada:** Badampudi, D., Wohlin, C., y Petersen, K. (2015). Experiences from using snowballing and database searches in systematic literature studies. Proceedings of the 19th International Conference on Evaluation and Assessment in Software Engineering (EASE '15). ACM.
- **Tipo de fuente:** Artículo de congreso revisado por pares
- **Ámbito metodológico:** MB-03 Filtrado, cribado y bola de nieve (principal) · secundarias: MB-02
- **Calidad Q:** 81 (A) — Tipo 20/25 · Rigor 14/20 · Autoridad 13/15 · Vigencia 9/10 · Impacto 8/10 · Independencia 10/10 · Acceso 7/10
- **DOI / URL:** DOI: 10.1145/2745802.2745818 · Confirmada en la bibliografía sobre bola de nieve de la documentación de litball: https://litball.readthedocs.io/en/latest/literature.html
- **Estado:** Vigente
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Wohlin Kalinowski Felizardo Mendes successful combination of database search and snowballing identification of primary studies»; WebFetch: sí, bibliografía de litball (índice); artículo no leído)
- **Ficha metodológica:** Compara en la práctica la bola de nieve y la búsqueda en bases para identificar estudios: rendimiento, esfuerzo y estudios que solo encuentra cada método. Complementa las directrices de Wohlin (fondo_entry_006).
- **Criterios derivados:** Ninguno todavía.
- **Origen:** Alta V4.0 (2026-11-02). Confirmada en índice (cita con DOI).

#### fondo_entry_157 · Q 80 (A) — Prioritising references for systematic reviews with RobotAnalyst: a user study

- **Cita normalizada:** Przybyła, P., et al. (2018). Prioritising references for systematic reviews with RobotAnalyst: a user study. Research Synthesis Methods, 9(3), 470-488.
- **Tipo de fuente:** Artículo revisado por pares
- **Ámbito metodológico:** MB-03 Filtrado, cribado y bola de nieve (principal) · secundarias: MB-04
- **Calidad Q:** 80 (A) — Tipo 25/25 · Rigor 14/20 · Autoridad 12/15 · Vigencia 8/10 · Impacto 7/10 · Independencia 8/10 · Acceso 6/10
- **DOI / URL:** DOI: 10.1002/jrsm.1311 · Confirmada en la bibliografía de la presentación de A. Booth sobre selección de estudios (EPPI Centre, 2024): https://eppi.ioe.ac.uk/CMS/Portals/0/Study%20Selection%20-%20Andrew%20Booth%20-%20ESG.pdf
- **Estado:** Vigente
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «single screening versus double screening study selection systematic reviews Waffenschmidt Gartlehner»; WebFetch: sí, presentación de Booth (índice); artículo no leído)
- **Ficha metodológica:** Estudio de usuario de RobotAnalyst, herramienta de priorización de referencias por minería de textos: rendimiento y aceptación por los revisores. Ejemplo de evaluación de una herramienta de cribado priorizado.
- **Criterios derivados:** Ninguno todavía.
- **Origen:** Alta V4.0 (2026-11-02). Confirmada en índice (cita con DOI).
- **Nota:** Autores vinculados al desarrollo de la herramienta.

#### fondo_entry_139 · Q 79 (B) — Systematic literature studies: database searches vs. backward snowballing

- **Cita normalizada:** Jalali, S., y Wohlin, C. (2012). Systematic literature studies: database searches vs. backward snowballing. Proceedings of the ACM-IEEE International Symposium on Empirical Software Engineering and Measurement (ESEM).
- **Tipo de fuente:** Artículo de congreso revisado por pares
- **Ámbito metodológico:** MB-03 Filtrado, cribado y bola de nieve (principal) · secundarias: MB-02
- **Calidad Q:** 79 (B) — Tipo 20/25 · Rigor 14/20 · Autoridad 13/15 · Vigencia 8/10 · Impacto 8/10 · Independencia 10/10 · Acceso 6/10
- **DOI / URL:** Sin DOI visto · Confirmada en la bibliografía sobre bola de nieve de la documentación de litball: https://litball.readthedocs.io/en/latest/literature.html
- **Estado:** Vigente
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Wohlin Kalinowski Felizardo Mendes successful combination of database search and snowballing identification of primary studies»; WebFetch: sí, bibliografía de litball (índice); artículo no leído)
- **Ficha metodológica:** Comparación directa entre búsqueda en bases y bola de nieve hacia atrás en una misma revisión (resultados no leídos en esta verificación). Referencia para valorar la bola de nieve como estrategia principal cuando las bases son pobres.
- **Criterios derivados:** Ninguno todavía.
- **Origen:** Alta V4.0 (2026-11-02). Confirmada en índice.

#### fondo_entry_141 · Q 78 (B) — Second-generation systematic literature studies using snowballing

- **Cita normalizada:** Wohlin, C. (2016). Second-generation systematic literature studies using snowballing. Proceedings of the 20th International Conference on Evaluation and Assessment in Software Engineering (EASE '16).
- **Tipo de fuente:** Artículo de congreso revisado por pares
- **Ámbito metodológico:** MB-03 Filtrado, cribado y bola de nieve (principal) · secundarias: MB-04
- **Calidad Q:** 78 (B) — Tipo 20/25 · Rigor 12/20 · Autoridad 14/15 · Vigencia 9/10 · Impacto 7/10 · Independencia 10/10 · Acceso 6/10
- **DOI / URL:** Sin DOI visto · Confirmada en la bibliografía sobre bola de nieve de la documentación de litball: https://litball.readthedocs.io/en/latest/literature.html
- **Estado:** Vigente
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Wohlin Kalinowski Felizardo Mendes successful combination of database search and snowballing identification of primary studies»; WebFetch: sí, bibliografía de litball (índice); artículo no leído)
- **Ficha metodológica:** Propone actualizar revisiones existentes («segunda generación») mediante bola de nieve hacia adelante desde los estudios ya incluidos. Modelo para refrescar periódicamente un corpus del bloque sin repetir la búsqueda completa.
- **Criterios derivados:** Ninguno todavía.
- **Origen:** Alta V4.0 (2026-11-02). Confirmada en índice.

#### fondo_entry_140 · Q 77 (B) — Using forward snowballing to update systematic reviews in software engineering

- **Cita normalizada:** Felizardo, K. R., et al. (2016). Using forward snowballing to update systematic reviews in software engineering. Proceedings of the 10th ACM/IEEE International Symposium on Empirical Software Engineering and Measurement (ESEM).
- **Tipo de fuente:** Artículo de congreso revisado por pares
- **Ámbito metodológico:** MB-03 Filtrado, cribado y bola de nieve (principal) · secundarias: MB-04
- **Calidad Q:** 77 (B) — Tipo 20/25 · Rigor 13/20 · Autoridad 12/15 · Vigencia 9/10 · Impacto 7/10 · Independencia 10/10 · Acceso 6/10
- **DOI / URL:** Sin DOI visto · Confirmada en la bibliografía sobre bola de nieve de la documentación de litball: https://litball.readthedocs.io/en/latest/literature.html
- **Estado:** Vigente
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Wohlin Kalinowski Felizardo Mendes successful combination of database search and snowballing identification of primary studies»; WebFetch: sí, bibliografía de litball (índice); artículo no leído)
- **Ficha metodológica:** Evalúa la bola de nieve hacia adelante como método de actualización de revisiones frente a repetir la búsqueda en bases (resultados no leídos en esta verificación). Complementa a fondo_entry_141.
- **Criterios derivados:** Ninguno todavía.
- **Origen:** Alta V4.0 (2026-11-02). Confirmada en índice.

#### fondo_entry_154 · Q 75 (B) — Identifying strategies for study selection in systematic reviews and maps

- **Cita normalizada:** Petersen, K., y Ali, N. B. (2011). Identifying strategies for study selection in systematic reviews and maps. 2011 International Symposium on Empirical Software Engineering and Measurement (ESEM), Banff, 351-354.
- **Tipo de fuente:** Artículo de congreso revisado por pares (breve)
- **Ámbito metodológico:** MB-03 Filtrado, cribado y bola de nieve (principal)
- **Calidad Q:** 75 (B) — Tipo 20/25 · Rigor 12/20 · Autoridad 12/15 · Vigencia 8/10 · Impacto 7/10 · Independencia 10/10 · Acceso 6/10
- **DOI / URL:** DOI: 10.1109/ESEM.2011.46 · Confirmada en la bibliografía de la presentación de A. Booth sobre selección de estudios (EPPI Centre, 2024): https://eppi.ioe.ac.uk/CMS/Portals/0/Study%20Selection%20-%20Andrew%20Booth%20-%20ESG.pdf
- **Estado:** Vigente
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «single screening versus double screening study selection systematic reviews Waffenschmidt Gartlehner»; WebFetch: sí, presentación de Booth (índice); artículo no leído)
- **Ficha metodológica:** Cataloga estrategias de selección de estudios (criterios, número de revisores, resolución de desacuerdos, pilotaje) en revisiones y mapeos. Lista de opciones de diseño para el paso de cribado.
- **Criterios derivados:** Ninguno todavía.
- **Origen:** Alta V4.0 (2026-11-02). Confirmada en índice (cita con DOI).

## MB-04 Gestión del corpus

#### fondo_entry_168 · Q 92 (A) — Duplicate Record Detection: A Survey

- **Cita normalizada:** Elmagarmid, A. K., Ipeirotis, P. G., y Verykios, V. S. (2007). Duplicate Record Detection: A Survey. IEEE Transactions on Knowledge and Data Engineering, 19(1), 1-16.
- **Tipo de fuente:** Artículo revisado por pares (revisión)
- **Ámbito metodológico:** MB-04 Gestión del corpus (principal)
- **Calidad Q:** 92 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 8/10 · Impacto 10/10 · Independencia 10/10 · Acceso 7/10
- **DOI / URL:** DOI: 10.1109/tkde.2007.250581 · Copia en el repositorio de la New York University: https://archive.nyu.edu/handle/2451/27823 · Ficha HBKU: https://elmi.hbku.edu.qa/en/publications/duplicate-record-detection-a-survey/
- **Estado:** Vigente
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Elmagarmid Ipeirotis Verykios "Duplicate Record Detection: A Survey" IEEE Transactions on Knowledge and Data Engineering 2007»; WebFetch: sí, repositorio de NYU (revista, volumen y número) y Wikipedia «Record linkage» (páginas y DOI))
- **Ficha metodológica:** Revisión de las técnicas de detección de registros duplicados: medidas de similitud de campos (edición, fonéticas, por tokens), métodos de decisión probabilísticos, supervisados y basados en distancia, técnicas de eficiencia (bloqueo, vecindario ordenado) y herramientas. Mapa de opciones para la deduplicación del corpus.
- **Criterios derivados:** Ninguno todavía.
- **Origen:** Alta V4.0 (2026-11-02). Verificación directa.

#### fondo_entry_167 · Q 92 (A) — A Theory for Record Linkage

- **Cita normalizada:** Fellegi, I. P., y Sunter, A. B. (1969). A Theory for Record Linkage. Journal of the American Statistical Association, 64(328), 1183-1210.
- **Tipo de fuente:** Artículo revisado por pares (origen teórico)
- **Ámbito metodológico:** MB-04 Gestión del corpus (principal) · secundarias: MB-05
- **Calidad Q:** 92 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 8/10 · Impacto 10/10 · Independencia 10/10 · Acceso 6/10
- **DOI / URL:** DOI: 10.2307/2286061 · JSTOR 2286061 (suscripción) · Referencias en Wikipedia «Record linkage»: https://en.wikipedia.org/wiki/Record_linkage · Copia docente: https://courses.cs.washington.edu/courses/cse590q/04au/papers/Felligi69.pdf
- **Estado:** Vigente
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Fellegi Sunter 1969 "A Theory for Record Linkage" Journal of the American Statistical Association 64 328»; WebFetch: sí, artículo «Record linkage» de Wikipedia (cita completa con DOI) e índice de Leipzig)
- **Ficha metodológica:** Modelo probabilístico del emparejamiento de registros: compara pares de registros campo a campo, pondera los acuerdos y desacuerdos y clasifica cada par en coincidencia, no coincidencia o revisión manual según umbrales que controlan los errores. Es la base formal de la deduplicación aproximada de referencias bibliográficas.
- **Criterios derivados:** Ninguno todavía.
- **Origen:** Alta V4.0 (2026-11-02). Confirmada en Wikipedia (referencias) y en el índice de Leipzig (https://pubs.dbs.uni-leipzig.de/dc/pubs/results/taxonomy:74).

#### fondo_entry_159 · Q 91 (A) — Evaluating the accuracy and speed of eight deduplication tools: A comparative study

- **Cita normalizada:** Bateup, S., Fulbright, H., Moberg, K., Hair, K., Peterson, E., Stansfield, C., Qureshi, R., y Clark, J. (2026). Evaluating the accuracy and speed of eight deduplication tools: A comparative study. Research Synthesis Methods.
- **Tipo de fuente:** Artículo revisado por pares
- **Ámbito metodológico:** MB-04 Gestión del corpus (principal)
- **Calidad Q:** 91 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 13/15 · Vigencia 10/10 · Impacto 6/10 · Independencia 10/10 · Acceso 10/10
- **DOI / URL:** DOI: 10.1017/rsm.2026.10100 · Repositorio White Rose: https://eprints.whiterose.ac.uk/id/eprint/242760/ · Acceso abierto (CC BY)
- **Estado:** Vigente
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «de-duplication of database search results for systematic reviews comparison EndNote Rayyan Covidence ASySD Deduklick»; WebFetch: sí, repositorio White Rose)
- **Ficha metodológica:** Compara ASySD, Covidence, Deduklick, EPPI-Reviewer, PICO Portal, Rayyan y dos versiones del SRA Deduplicator sobre conjuntos de referencia de cinco revisiones Cochrane: Rayyan, Covidence y el SRA focalizado eliminan menos registros únicos por error; ASySD, Rayyan y EPPI-Reviewer detectan más duplicados; ninguna herramienta se desaconseja. Recomienda ponderar los tres resultados, coste y revisión manual.
- **Criterios derivados:** Ninguno todavía.
- **Origen:** Alta V4.0 (2026-11-02). Verificación directa. Sustituye como referencia principal al resumen de congreso de Clark et al. (Coloquio Cochrane 2023), del mismo equipo, que no se da de alta por redundante.
- **Nota:** Publicado en línea en junio de 2026; volumen no asignado en la página consultada.

#### fondo_entry_160 · Q 91 (A) — De-duplication of database search results for systematic reviews in EndNote

- **Cita normalizada:** Bramer, W. M., Giustini, D., de Jonge, G. B., Holland, L., y Bekhuis, T. (2016). De-duplication of database search results for systematic reviews in EndNote. Journal of the Medical Library Association, 104(3), 240-243.
- **Tipo de fuente:** Artículo revisado por pares (método)
- **Ámbito metodológico:** MB-04 Gestión del corpus (principal)
- **Calidad Q:** 91 (A) — Tipo 25/25 · Rigor 15/20 · Autoridad 13/15 · Vigencia 9/10 · Impacto 9/10 · Independencia 10/10 · Acceso 10/10
- **DOI / URL:** DOI: 10.3163/1536-5050.104.3.014 · Revista en acceso abierto: https://jmla.pitt.edu/ojs/jmla/article/view/24 · Confirmada en la guía de deduplicación de McGill Library: https://libraryguides.mcgill.ca/knowledge-syntheses/deduplicating
- **Estado:** Vigente
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Bramer Giustini de Jonge Holland Bekhuis 2016 De-duplication of database search results for systematic reviews in EndNote JMLA»; WebFetch: sí, JMLA (autores, fecha) y guía de McGill (revista, volumen, páginas y DOI))
- **Ficha metodológica:** Método por pasos para eliminar duplicados en EndNote tras buscar en varias bases, combinando comparaciones sucesivas de campos (autor, año, título, revista, páginas) con revisión manual. Procedimiento de referencia para deduplicar exportaciones RIS del bloque.
- **Criterios derivados:** Ninguno todavía.
- **Origen:** Alta V4.0 (2026-11-02). Verificación directa.
- **Nota:** La página de JMLA muestra el DOI 10.5195/jmla.2016.24 (DOI de la plataforma); la cita de McGill da 10.3163/1536-5050.104.3.014.

#### fondo_entry_172 · Q 91 (A) — A guided tour to approximate string matching

- **Cita normalizada:** Navarro, G. (2001). A guided tour to approximate string matching. ACM Computing Surveys.
- **Tipo de fuente:** Artículo revisado por pares (revisión)
- **Ámbito metodológico:** MB-04 Gestión del corpus (principal)
- **Calidad Q:** 91 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 14/15 · Vigencia 8/10 · Impacto 10/10 · Independencia 10/10 · Acceso 6/10
- **DOI / URL:** DOI: 10.1145/375360.375365 · Página del autor (Universidad de Chile): https://users.dcc.uchile.cl/~gnavarro/abstracts/acmcs01.1.html · Repositorio de la Universidad de Chile: https://repositorio.uchile.cl/handle/2250/126168
- **Estado:** Vigente
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Navarro 2001 "A guided tour to approximate string matching" ACM Computing Surveys»; WebFetch: sí, página del autor)
- **Ficha metodológica:** Revisión de los algoritmos de búsqueda de cadenas con errores (distancia de edición y variantes), su comportamiento estadístico y una comparación experimental. Fundamento de la comparación aproximada de títulos y autores al deduplicar referencias con erratas o variantes.
- **Criterios derivados:** Ninguno todavía.
- **Origen:** Alta V4.0 (2026-11-02). Verificación directa (autor, título y resumen); revista y año según los resultados de búsqueda y el índice de Leipzig; DOI visto en los resultados de búsqueda.
- **Nota:** Volumen y páginas no mostrados en las páginas consultadas.

#### fondo_entry_162 · Q 90 (A) — Considerations for conducting systematic reviews: evaluating the performance of different methods for de-duplicating references

- **Cita normalizada:** McKeown, S., y Mir, Z. M. (2021). Considerations for conducting systematic reviews: evaluating the performance of different methods for de-duplicating references. Systematic Reviews, 10(1), 38.
- **Tipo de fuente:** Artículo revisado por pares
- **Ámbito metodológico:** MB-04 Gestión del corpus (principal)
- **Calidad Q:** 90 (A) — Tipo 25/25 · Rigor 15/20 · Autoridad 12/15 · Vigencia 10/10 · Impacto 8/10 · Independencia 10/10 · Acceso 10/10
- **DOI / URL:** DOI: 10.1186/s13643-021-01583-y · Confirmada en la guía de deduplicación de McGill Library: https://libraryguides.mcgill.ca/knowledge-syntheses/deduplicating · Acceso abierto
- **Estado:** Vigente
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Bramer Giustini de Jonge Holland Bekhuis 2016 De-duplication of database search results for systematic reviews in EndNote JMLA»; WebFetch: sí, guía de McGill (índice); artículo no leído)
- **Ficha metodológica:** Evalúa el rendimiento de distintos métodos y programas de deduplicación de referencias (gestores bibliográficos y plataformas de revisión) frente a una deduplicación de referencia. Útil para justificar el método elegido.
- **Criterios derivados:** Ninguno todavía.
- **Origen:** Alta V4.0 (2026-11-02). Confirmada en índice (cita con DOI).

#### fondo_entry_164 · Q 89 (A) — Software tools to support title and abstract screening for systematic reviews in healthcare: an evaluation

- **Cita normalizada:** Harrison, H., Griffin, S. J., Kuhn, I., y Usher-Smith, J. A. (2020). Software tools to support title and abstract screening for systematic reviews in healthcare: an evaluation. BMC Medical Research Methodology, 20(1).
- **Tipo de fuente:** Artículo revisado por pares
- **Ámbito metodológico:** MB-04 Gestión del corpus (principal) · secundarias: MB-03
- **Calidad Q:** 89 (A) — Tipo 25/25 · Rigor 15/20 · Autoridad 12/15 · Vigencia 9/10 · Impacto 8/10 · Independencia 10/10 · Acceso 10/10
- **DOI / URL:** DOI: 10.1186/s12874-020-0897-3 · Confirmada en la bibliografía de la presentación de A. Booth sobre selección de estudios (EPPI Centre, 2024): https://eppi.ioe.ac.uk/CMS/Portals/0/Study%20Selection%20-%20Andrew%20Booth%20-%20ESG.pdf · Acceso abierto
- **Estado:** Vigente
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «single screening versus double screening study selection systematic reviews Waffenschmidt Gartlehner»; WebFetch: sí, presentación de Booth (índice); artículo no leído)
- **Ficha metodológica:** Evalúa funciones, coste y usabilidad de las herramientas de cribado de títulos y resúmenes (Covidence, Rayyan, EPPI-Reviewer y otras) con un análisis de características. Base para elegir la plataforma de gestión del cribado.
- **Criterios derivados:** Ninguno todavía.
- **Origen:** Alta V4.0 (2026-11-02). Confirmada en índice (cita con DOI).

#### fondo_entry_163 · Q 88 (A) — Better duplicate detection for systematic reviewers: evaluation of Systematic Review Assistant-Deduplication Module

- **Cita normalizada:** Rathbone, J., Carter, M., Hoffmann, T., y Glasziou, P. (2015). Better duplicate detection for systematic reviewers: evaluation of Systematic Review Assistant-Deduplication Module. Systematic Reviews, 4(1), 6.
- **Tipo de fuente:** Artículo revisado por pares
- **Ámbito metodológico:** MB-04 Gestión del corpus (principal)
- **Calidad Q:** 88 (A) — Tipo 25/25 · Rigor 15/20 · Autoridad 13/15 · Vigencia 8/10 · Impacto 8/10 · Independencia 9/10 · Acceso 10/10
- **DOI / URL:** DOI: 10.1186/2046-4053-4-6 · Confirmada en la guía de deduplicación de McGill Library: https://libraryguides.mcgill.ca/knowledge-syntheses/deduplicating · Acceso abierto
- **Estado:** Vigente
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Bramer Giustini de Jonge Holland Bekhuis 2016 De-duplication of database search results for systematic reviews in EndNote JMLA»; WebFetch: sí, guía de McGill (índice); artículo no leído)
- **Ficha metodológica:** Evalúa el módulo de deduplicación del Systematic Review Assistant frente a EndNote, al que supera en duplicados detectados según el preprint de ASySD. Origen del SRA Deduplicator recomendado en guías de biblioteca.
- **Criterios derivados:** Ninguno todavía.
- **Origen:** Alta V4.0 (2026-11-02). Confirmada en índice (cita con DOI); el resultado frente a EndNote figura además en el preprint de ASySD.
- **Nota:** Autores del grupo que desarrolla la herramienta.

#### fondo_entry_165 · Q 87 (A) — Tools to support the automation of systematic reviews: a scoping review

- **Cita normalizada:** Khalil, H., Ameen, D., y Zarnegar, A. (2022). Tools to support the automation of systematic reviews: a scoping review. Journal of Clinical Epidemiology, 144, 22-42.
- **Tipo de fuente:** Artículo revisado por pares (revisión de alcance)
- **Ámbito metodológico:** MB-04 Gestión del corpus (principal) · secundarias: MB-03
- **Calidad Q:** 87 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 12/15 · Vigencia 10/10 · Impacto 8/10 · Independencia 10/10 · Acceso 6/10
- **DOI / URL:** Sin DOI visto · Confirmada en la bibliografía de la presentación de A. Booth sobre selección de estudios (EPPI Centre, 2024): https://eppi.ioe.ac.uk/CMS/Portals/0/Study%20Selection%20-%20Andrew%20Booth%20-%20ESG.pdf
- **Estado:** Vigente
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «single screening versus double screening study selection systematic reviews Waffenschmidt Gartlehner»; WebFetch: sí, presentación de Booth (índice); artículo no leído)
- **Ficha metodológica:** Revisión de alcance de las herramientas que automatizan fases de la revisión (búsqueda, deduplicación, cribado, extracción): qué hacen y con qué evidencia de validación. Catálogo para elegir herramientas por fase.
- **Criterios derivados:** Ninguno todavía.
- **Origen:** Alta V4.0 (2026-11-02). Confirmada en índice.

#### fondo_entry_007 · Q 86 (A) — Ouzzani et al. (2016)

- **Cita normalizada:** Ouzzani, M., Hammady, H., Fedorowicz, Z., y Elmagarmid, A. (2016). Rayyan—a web and mobile app for systematic reviews. Systematic Reviews, 5, 210.
- **Tipo de fuente:** Artículo revisado por pares (herramienta)
- **Ámbito metodológico:** MB-04 Gestión del corpus (principal) (en V2.3: Gestión del corpus)
- **Calidad Q:** 86 (A) — Tipo 22/25 · Rigor 14/20 · Autoridad 13/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 8/10 · Acceso 10/10
- **DOI / URL:** DOI: 10.1186/s13643-016-0384-4 · Acceso abierto en la editorial (systematicreviewsjournal.biomedcentral.com) · Verificación (anexo 8.1 V2.3): DOI: doi.org/10.1186/s13643-016-0384-4 (Systematic Reviews, BMC, acceso abierto, ficha) · Herramienta objeto del artículo: rayyan.ai (sitio oficial)
- **Estado:** Vigente
- **Estado del enlace:** PENDIENTE_BARRIDO
- **Última verificación:** 2026-10-25
- **Ficha metodológica:** Describe el flujo de gestión del cribado de una revisión: deduplicación, cribado por títulos y resúmenes con resaltado automático de razones, resolución de conflictos y registro de decisiones. Da al Fondo el vocabulario de gestión del corpus (deduplicación, cribado, conflictos) aplicable a sus propios registros.
- **Criterios derivados:** fondo_criterion_004
- **Verificación V2.3:** Completa (carga de arranque): cita, DOI y acceso abierto verificados el 25/10/2026; comprobaciones omitidas: lectura del texto completo por el Documentador
- **Nota:** Artículo de los autores de la herramienta descrita (independencia limitada).

#### fondo_entry_170 · Q 86 (A) — The State of Record Linkage and Current Research Problems

- **Cita normalizada:** Winkler, W. E. (1999). The State of Record Linkage and Current Research Problems. Statistical Research Report Series RR99-04. Washington: U.S. Census Bureau.
- **Tipo de fuente:** Documento de trabajo institucional
- **Ámbito metodológico:** MB-04 Gestión del corpus (principal)
- **Calidad Q:** 86 (A) — Tipo 20/25 · Rigor 15/20 · Autoridad 15/15 · Vigencia 7/10 · Impacto 9/10 · Independencia 10/10 · Acceso 10/10
- **DOI / URL:** Sin DOI · https://www.census.gov/library/working-papers/1999/adrm/rr99-04.html · Acceso gratuito
- **Estado:** Vigente
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «record linkage Fellegi Sunter duplicate record detection survey Elmagarmid Christen data matching»; WebFetch: sí, sitio del U.S. Census Bureau)
- **Ficha metodológica:** Revisión de métodos y sistemas de emparejamiento de registros desde Newcombe y Fellegi-Sunter, con los problemas abiertos de estimar automáticamente parámetros y tasas de error. Visión de un organismo estadístico oficial sobre la deduplicación a escala.
- **Criterios derivados:** Ninguno todavía.
- **Origen:** Alta V4.0 (2026-11-02). Verificación directa.

#### fondo_entry_166 · Q 85 (A) — Usability and acceptability of four systematic review automation software packages: a mixed method design

- **Cita normalizada:** Cleo, G., Scott, A. M., Islam, F., Julien, B., y Beller, E. (2019). Usability and acceptability of four systematic review automation software packages: a mixed method design. Systematic Reviews, 8(1).
- **Tipo de fuente:** Artículo revisado por pares
- **Ámbito metodológico:** MB-04 Gestión del corpus (principal)
- **Calidad Q:** 85 (A) — Tipo 25/25 · Rigor 14/20 · Autoridad 11/15 · Vigencia 8/10 · Impacto 7/10 · Independencia 10/10 · Acceso 10/10
- **DOI / URL:** DOI: 10.1186/s13643-019-1069-6 · Confirmada en la bibliografía de la presentación de A. Booth sobre selección de estudios (EPPI Centre, 2024): https://eppi.ioe.ac.uk/CMS/Portals/0/Study%20Selection%20-%20Andrew%20Booth%20-%20ESG.pdf
- **Estado:** Vigente
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «single screening versus double screening study selection systematic reviews Waffenschmidt Gartlehner»; WebFetch: sí, presentación de Booth (índice); artículo no leído)
- **Ficha metodológica:** Evalúa con métodos mixtos la usabilidad y aceptación de cuatro paquetes de automatización de revisiones. Complementa a fondo_entry_164 con la perspectiva del usuario.
- **Criterios derivados:** Ninguno todavía.
- **Origen:** Alta V4.0 (2026-11-02). Confirmada en índice (cita con DOI).

#### fondo_entry_171 · Q 85 (A) — Data Matching: Concepts and Techniques for Record Linkage, Entity Resolution, and Duplicate Detection

- **Cita normalizada:** Christen, P. (2012). Data Matching: Concepts and Techniques for Record Linkage, Entity Resolution, and Duplicate Detection. Berlín/Heidelberg: Springer.
- **Tipo de fuente:** Manual de referencia
- **Ámbito metodológico:** MB-04 Gestión del corpus (principal)
- **Calidad Q:** 85 (A) — Tipo 20/25 · Rigor 18/20 · Autoridad 14/15 · Vigencia 9/10 · Impacto 9/10 · Independencia 10/10 · Acceso 5/10
- **DOI / URL:** Sin DOI visto · Registro bibliográfico (Universidad Veracruzana, procedente del CERN): https://ebusca.uv.mx/Record/cern-1488418 · Obra comercial
- **Estado:** Vigente
- **Estado del enlace:** MURO_PAGO
- **Última verificación:** 2026-11-02 (búsqueda web: «record linkage Fellegi Sunter duplicate record detection survey Elmagarmid Christen data matching»; WebFetch: sí, catálogo)
- **Ficha metodológica:** Manual completo de emparejamiento de datos: preparación y normalización, indexación y bloqueo, comparación de campos, clasificación, evaluación de calidad y privacidad. Referencia técnica para diseñar la deduplicación del corpus.
- **Criterios derivados:** Ninguno todavía.
- **Origen:** Alta V4.0 (2026-11-02). Verificación directa en catálogo (autor, año, título y editorial).

#### fondo_entry_169 · Q 85 (A) — Automatic Linkage of Vital Records

- **Cita normalizada:** Newcombe, H. B., Kennedy, J. M., Axford, S. J., y James, A. P. (1959). Automatic Linkage of Vital Records. Science, 130(3381), 954-959.
- **Tipo de fuente:** Artículo revisado por pares (origen histórico)
- **Ámbito metodológico:** MB-04 Gestión del corpus (principal)
- **Calidad Q:** 85 (A) — Tipo 25/25 · Rigor 14/20 · Autoridad 15/15 · Vigencia 6/10 · Impacto 9/10 · Independencia 10/10 · Acceso 6/10
- **DOI / URL:** DOI: 10.1126/science.130.3381.954 · Confirmada en las referencias de Wikipedia «Record linkage»: https://en.wikipedia.org/wiki/Record_linkage
- **Estado:** Vigente
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Fellegi Sunter 1969 "A Theory for Record Linkage" Journal of the American Statistical Association 64 328»; WebFetch: sí, Wikipedia (índice); artículo no leído)
- **Ficha metodológica:** Primer emparejamiento automático de registros a gran escala con ponderaciones por frecuencia de valores, antecedente directo del modelo de Fellegi y Sunter (fondo_entry_167).
- **Criterios derivados:** Ninguno todavía.
- **Origen:** Alta V4.0 (2026-11-02). Confirmada en índice (cita con DOI).

#### fondo_entry_173 · Q 84 (A) — Efficient clustering of high-dimensional data sets with application to reference matching

- **Cita normalizada:** McCallum, A., Nigam, K., y Ungar, L. H. (2000). Efficient clustering of high-dimensional data sets with application to reference matching. Proceedings of the Sixth ACM SIGKDD International Conference on Knowledge Discovery and Data Mining (KDD 2000).
- **Tipo de fuente:** Artículo de congreso revisado por pares
- **Ámbito metodológico:** MB-04 Gestión del corpus (principal)
- **Calidad Q:** 84 (A) — Tipo 20/25 · Rigor 16/20 · Autoridad 14/15 · Vigencia 8/10 · Impacto 10/10 · Independencia 10/10 · Acceso 6/10
- **DOI / URL:** Sin DOI visto · Confirmada en el índice bibliográfico de la Universität Leipzig sobre limpieza de datos y emparejamiento de registros: https://pubs.dbs.uni-leipzig.de/dc/pubs/results/taxonomy:74
- **Estado:** Vigente
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «record linkage Fellegi Sunter duplicate record detection survey Elmagarmid Christen data matching»; WebFetch: sí, índice de Leipzig; artículo no leído)
- **Ficha metodológica:** Método de agrupamiento en dos fases («canopies» baratas y comparación fina dentro de cada grupo) aplicado precisamente a emparejar referencias bibliográficas. Modelo de deduplicación eficiente de grandes conjuntos de citas.
- **Criterios derivados:** Ninguno todavía.
- **Origen:** Alta V4.0 (2026-11-02). Confirmada en índice (autores, año y título); congreso según la cita habitual, pendiente de cotejo.
- **Nota:** Sede no mostrada en el índice consultado.

#### fondo_entry_174 · Q 83 (A) — The merge/purge problem for large databases

- **Cita normalizada:** Hernández, M. A., y Stolfo, S. J. (1995). The merge/purge problem for large databases. Proceedings of the 1995 ACM SIGMOD International Conference on Management of Data.
- **Tipo de fuente:** Artículo de congreso revisado por pares
- **Ámbito metodológico:** MB-04 Gestión del corpus (principal)
- **Calidad Q:** 83 (A) — Tipo 20/25 · Rigor 16/20 · Autoridad 14/15 · Vigencia 7/10 · Impacto 10/10 · Independencia 10/10 · Acceso 6/10
- **DOI / URL:** Sin DOI visto · Confirmada en el índice bibliográfico de la Universität Leipzig sobre limpieza de datos y emparejamiento de registros: https://pubs.dbs.uni-leipzig.de/dc/pubs/results/taxonomy:74
- **Estado:** Vigente
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «record linkage Fellegi Sunter duplicate record detection survey Elmagarmid Christen data matching»; WebFetch: sí, índice de Leipzig; artículo no leído)
- **Ficha metodológica:** Formula el problema de fusionar y depurar duplicados en grandes bases y propone el método de vecindario ordenado (ordenar por clave y comparar solo registros cercanos), con varias pasadas por claves distintas. Técnica básica para deduplicar exportaciones masivas.
- **Criterios derivados:** Ninguno todavía.
- **Origen:** Alta V4.0 (2026-11-02). Confirmada en índice (autores, año y título); sede según la cita habitual, pendiente de cotejo.
- **Nota:** Sede no mostrada en el índice consultado.

#### fondo_entry_161 · Q 81 (A) — High precision but variable recall: comparing the performance of five deduplication tools

- **Cita normalizada:** Janka, H., y Metzendorf, M.-I. (2024). High precision but variable recall: comparing the performance of five deduplication tools. Journal of EAHIL, 20(1), 12-17.
- **Tipo de fuente:** Artículo de revista profesional revisada
- **Ámbito metodológico:** MB-04 Gestión del corpus (principal)
- **Calidad Q:** 81 (A) — Tipo 20/25 · Rigor 14/20 · Autoridad 12/15 · Vigencia 10/10 · Impacto 6/10 · Independencia 10/10 · Acceso 9/10
- **DOI / URL:** DOI: 10.32384/jeahil20607 · Confirmada en la guía de deduplicación de McGill Library: https://libraryguides.mcgill.ca/knowledge-syntheses/deduplicating · Resumen previo (Coloquio Cochrane 2023): https://abstracts.cochrane.org/2023-london/evaluation-performance-five-deduplication-tools
- **Estado:** Vigente
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Bramer Giustini de Jonge Holland Bekhuis 2016 De-duplication of database search results for systematic reviews in EndNote JMLA»; WebFetch: sí, guía de McGill (cita) y resumen del Coloquio Cochrane 2023; artículo no leído)
- **Ficha metodológica:** Compara EndNote, Covidence, Rayyan, Deduklick y SRA Deduplicator: alta precisión en todas pero exhaustividad variable; en el resumen previo, Deduklick y SRA Deduplicator superaron la deduplicación manual en EndNote y Rayyan requería comprobación manual. Útil para elegir herramienta y prever la revisión manual.
- **Criterios derivados:** Ninguno todavía.
- **Origen:** Alta V4.0 (2026-11-02). Confirmada en índice.

#### fondo_entry_175 · Q 81 (A) — Managing large-volume literature searches in research synthesis studies

- **Cita normalizada:** Havill, N. L., Leeman, J., Shaw-Kokot, J., Knafl, K., Crandell, J., y Sandelowski, M. (2014). Managing large-volume literature searches in research synthesis studies. Nursing Outlook, 62(2), 112-118.
- **Tipo de fuente:** Artículo revisado por pares
- **Ámbito metodológico:** MB-04 Gestión del corpus (principal) · secundarias: MB-03
- **Calidad Q:** 81 (A) — Tipo 25/25 · Rigor 13/20 · Autoridad 12/15 · Vigencia 8/10 · Impacto 7/10 · Independencia 10/10 · Acceso 6/10
- **DOI / URL:** Sin DOI visto · Confirmada en la bibliografía de la presentación de A. Booth sobre selección de estudios (EPPI Centre, 2024): https://eppi.ioe.ac.uk/CMS/Portals/0/Study%20Selection%20-%20Andrew%20Booth%20-%20ESG.pdf
- **Estado:** Vigente
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «single screening versus double screening study selection systematic reviews Waffenschmidt Gartlehner»; WebFetch: sí, presentación de Booth (índice); artículo no leído)
- **Ficha metodológica:** Estrategias para gestionar búsquedas con volúmenes muy altos de registros en estudios de síntesis: organización del corpus, reparto del cribado y control de versiones de las decisiones.
- **Criterios derivados:** Ninguno todavía.
- **Origen:** Alta V4.0 (2026-11-02). Confirmada en índice.

#### fondo_entry_176 · Q 81 (A) — TAILOR: A Record Linkage Toolbox

- **Cita normalizada:** Elfeky, M. G., Verykios, V. S., y Elmagarmid, A. K. (2002). TAILOR: A Record Linkage Toolbox. Proceedings of the 18th International Conference on Data Engineering (ICDE 2002).
- **Tipo de fuente:** Artículo de congreso revisado por pares
- **Ámbito metodológico:** MB-04 Gestión del corpus (principal)
- **Calidad Q:** 81 (A) — Tipo 20/25 · Rigor 15/20 · Autoridad 13/15 · Vigencia 7/10 · Impacto 8/10 · Independencia 10/10 · Acceso 8/10
- **DOI / URL:** Sin DOI visto · PDF en la página de A. Elmagarmid (Purdue University): https://www.cs.purdue.edu/homes/ake/pub/TAILOR_ICDE2002.pdf
- **Estado:** Vigente
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «record linkage Fellegi Sunter duplicate record detection survey Elmagarmid Christen data matching»; WebFetch: sí, PDF)
- **Ficha metodológica:** Caja de herramientas extensible de emparejamiento de registros con modelos de aprendizaje (inducción, agrupamiento e híbrido) que superan al enfoque probabilístico de Fellegi-Sunter en exactitud y completitud en sus experimentos. Ejemplo de arquitectura modular para deduplicar.
- **Criterios derivados:** Ninguno todavía.
- **Origen:** Alta V4.0 (2026-11-02). Verificación directa (autores, título y resumen en el PDF; congreso y año según el nombre del archivo).
- **Nota:** Sede y año no impresos en el texto leído; cotejar.

#### fondo_entry_178 · Q 77 (B) — The Automated Systematic Search Deduplicator (ASySD): a rapid, open-source, interoperable tool to remove duplicate citations in biomedical systematic reviews

- **Cita normalizada:** Hair, K., Bahor, Z., Macleod, M., Liao, J., y Sena, E. S. (2021). The Automated Systematic Search Deduplicator (ASySD): a rapid, open-source, interoperable tool to remove duplicate citations in biomedical systematic reviews. bioRxiv, 2021.05.04.442412.
- **Tipo de fuente:** Documento de trabajo (preprint)
- **Ámbito metodológico:** MB-04 Gestión del corpus (principal)
- **Calidad Q:** 77 (B) — Tipo 15/25 · Rigor 15/20 · Autoridad 12/15 · Vigencia 10/10 · Impacto 7/10 · Independencia 8/10 · Acceso 10/10
- **DOI / URL:** DOI: 10.1101/2021.05.04.442412 · bioRxiv: https://www.biorxiv.org/content/10.1101/2021.05.04.442412v1.full.pdf+html · Versión publicada en PMC: https://pmc.ncbi.nlm.nih.gov/articles/PMC10483700
- **Estado:** Vigente
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «de-duplication of database search results for systematic reviews comparison EndNote Rayyan Covidence ASySD Deduklick»; WebFetch: sí, bioRxiv (la página de PMC devolvió una verificación de navegador))
- **Ficha metodológica:** Herramienta abierta (paquete R y aplicación Shiny) de deduplicación automática de citas, comparada con EndNote y el SRA Deduplicator; se basa en emparejamiento de registros (paquete RecordLinkage). Alternativa reproducible y programable para el bloque.
- **Criterios derivados:** Ninguno todavía.
- **Origen:** Alta V4.0 (2026-11-02). Verificación directa del preprint; existe versión publicada (registro en PMC) cuya revista no se ha podido leer.
- **Nota:** Autores de la herramienta (independencia limitada); citar la versión publicada cuando se coteje.

#### fondo_entry_179 · Q 76 (B) — Tools to support systematic literature reviews in software engineering: A mapping study

- **Cita normalizada:** Marshall, C., y Brereton, P. (2013). Tools to support systematic literature reviews in software engineering: A mapping study. 2013 ACM/IEEE International Symposium on Empirical Software Engineering and Measurement (ESEM). IEEE.
- **Tipo de fuente:** Artículo de congreso revisado por pares
- **Ámbito metodológico:** MB-04 Gestión del corpus (principal) · secundarias: MB-03
- **Calidad Q:** 76 (B) — Tipo 20/25 · Rigor 13/20 · Autoridad 13/15 · Vigencia 7/10 · Impacto 7/10 · Independencia 10/10 · Acceso 6/10
- **DOI / URL:** Sin DOI visto · Confirmada en la bibliografía sobre bola de nieve de la documentación de litball: https://litball.readthedocs.io/en/latest/literature.html
- **Estado:** Vigente
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Wohlin Kalinowski Felizardo Mendes successful combination of database search and snowballing identification of primary studies»; WebFetch: sí, bibliografía de litball (índice); artículo no leído)
- **Ficha metodológica:** Mapeo de las herramientas que apoyan las revisiones sistemáticas (búsqueda, gestión de referencias, cribado, extracción) en ingeniería de software. Visión de conjunto de funciones de gestión del corpus fuera del ámbito sanitario.
- **Criterios derivados:** Ninguno todavía.
- **Origen:** Alta V4.0 (2026-11-02). Confirmada en índice.

#### fondo_entry_180 · Q 74 (B) — Systematic review automation tool use by systematic reviewers, health technology assessors and clinical guideline developers

- **Cita normalizada:** Scott, A., Forbes, C., Clark, J., Carter, M., Glasziou, P., y Munn, Z. (2021). Systematic review automation tool use by systematic reviewers, health technology assessors and clinical guideline developers. medRxiv.
- **Tipo de fuente:** Documento de trabajo (preprint)
- **Ámbito metodológico:** MB-04 Gestión del corpus (principal)
- **Calidad Q:** 74 (B) — Tipo 15/25 · Rigor 13/20 · Autoridad 12/15 · Vigencia 9/10 · Impacto 6/10 · Independencia 10/10 · Acceso 9/10
- **DOI / URL:** DOI: 10.1101/2021.04.26.21255833 · Confirmada en la bibliografía de la presentación de A. Booth sobre selección de estudios (EPPI Centre, 2024): https://eppi.ioe.ac.uk/CMS/Portals/0/Study%20Selection%20-%20Andrew%20Booth%20-%20ESG.pdf
- **Estado:** Vigente
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «single screening versus double screening study selection systematic reviews Waffenschmidt Gartlehner»; WebFetch: sí, presentación de Booth (índice); artículo no leído)
- **Ficha metodológica:** Encuesta sobre qué herramientas de automatización usan realmente revisores, evaluadores de tecnologías y elaboradores de guías, para qué fases y con qué barreras. Útil para elegir herramientas con adopción profesional.
- **Criterios derivados:** Ninguno todavía.
- **Origen:** Alta V4.0 (2026-11-02). Confirmada en índice (cita con DOI).

#### fondo_entry_177 · Q 72 (B) — A comparison of probabilistic record linkage techniques in the Institute of Statistics of Andalusia

- **Cita normalizada:** Pino-Mejías, R., Cubiles-de-la-Vega, M.-D., y Caballero-Ruiz, E. (2011). A comparison of probabilistic record linkage techniques in the Institute of Statistics of Andalusia. Proceedings of the 58th World Statistical Congress (ISI), Dublín, sesión CPS070, 6773-6778.
- **Tipo de fuente:** Comunicación a congreso (organismo estadístico oficial)
- **Ámbito metodológico:** MB-04 Gestión del corpus (principal)
- **Calidad Q:** 72 (B) — Tipo 15/25 · Rigor 14/20 · Autoridad 12/15 · Vigencia 8/10 · Impacto 4/10 · Independencia 10/10 · Acceso 9/10
- **DOI / URL:** Sin DOI · PDF en el sitio del International Statistical Institute: https://isi-web.org/sites/default/files/import/files-2011/950535.pdf
- **Estado:** Vigente
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «record linkage Fellegi Sunter duplicate record detection survey Elmagarmid Christen data matching»; WebFetch: sí, PDF)
- **Ficha metodológica:** Caso del Instituto de Estadística y Cartografía de Andalucía: enlace de registros sin identificador común con Febrl y R (limpieza, bloqueo, comparación con distancias exacta, de edición, Jaro y Winkler, y clasificadores supervisados y no supervisados); los árboles, los bosques aleatorios y EM con comparación exacta dieron los mejores resultados. Ejemplo español y aplicado del flujo completo de deduplicación.
- **Criterios derivados:** Ninguno todavía.
- **Origen:** Alta V4.0 (2026-11-02). Verificación directa.

#### fondo_entry_181 · Q 69 (B) — Covidence and Rayyan

- **Cita normalizada:** Kellermeyer, L., Harnke, B., y Knight, S. (2018). Covidence and Rayyan. Journal of the Medical Library Association, 106(4).
- **Tipo de fuente:** Reseña de recursos en revista revisada
- **Ámbito metodológico:** MB-04 Gestión del corpus (principal) · secundarias: MB-03
- **Calidad Q:** 69 (B) — Tipo 15/25 · Rigor 10/20 · Autoridad 11/15 · Vigencia 7/10 · Impacto 6/10 · Independencia 10/10 · Acceso 10/10
- **DOI / URL:** DOI: 10.5195/jmla.2018.513 · Confirmada en la bibliografía de la presentación de A. Booth sobre selección de estudios (EPPI Centre, 2024): https://eppi.ioe.ac.uk/CMS/Portals/0/Study%20Selection%20-%20Andrew%20Booth%20-%20ESG.pdf · JMLA, acceso abierto
- **Estado:** Vigente
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «single screening versus double screening study selection systematic reviews Waffenschmidt Gartlehner»; WebFetch: sí, presentación de Booth (índice); artículo no leído)
- **Ficha metodológica:** Reseña comparada de Covidence y Rayyan (importación, deduplicación, cribado, resolución de conflictos, exportación y coste). Guía rápida para elegir plataforma de cribado.
- **Criterios derivados:** Ninguno todavía.
- **Origen:** Alta V4.0 (2026-11-02). Confirmada en índice (cita con DOI).
- **Nota:** Funciones y precios de 2018; las plataformas han cambiado.

## MB-05 Verificación y reproducibilidad

#### fondo_entry_208 · Q 97 (A) — Is There a Replication Crisis in Finance?

- **Cita normalizada:** Jensen, T. I., Kelly, B. T., y Pedersen, L. H. (2023). Is There a Replication Crisis in Finance? Journal of Finance, 78(5), 2465-2518.
- **Tipo de fuente:** Artículo revisado por pares (estudio empírico)
- **Ámbito metodológico:** MB-05 Verificación y reproducibilidad (principal) · secundarias: —
- **Calidad Q:** 97 (A) — Tipo 25/25 · Rigor 19/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 9/10
- **DOI / URL:** DOI: 10.1111/jofi.13249 · Versión del editor en el repositorio de Copenhagen Business School: https://research-api.cbs.dk/ws/portalfiles/portal/95651880/theis_ingerslev_jensen_et_al_is_there_a_replication_crisis_in_finance_publishersversion.pdf · NBER WP 28432: https://www.nber.org/papers/w28432
- **Acceso y licencia:** Revista por suscripción; versión del editor gratuita en el repositorio institucional de CBS
- **Estado:** Vigente
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «"Is There a Replication Crisis in Finance?" Jensen Kelly Pedersen Journal of Finance 2023 Hou Xue Zhang "Replicating Anomalies"»; WebFetch: sí)
- **Ficha metodológica:** Frente al 35 % de replicación de Hou, Xue y Zhang (2020), obtiene un 55,6 % con MCO sobre rendimientos brutos y un 82,4 % con alfas CAPM y un modelo bayesiano jerárquico de pruebas múltiples (tasa bayesiana de falsos descubrimientos del 0,1 %); la tasa es similar en 93 países, los factores se agrupan en 13 temas y los alfas posteriores a la publicación son menores pero positivos. Muestra que la conclusión sobre «crisis de replicación» depende del método de replicación elegido.
- **Uso en el bloque:** AC del Analizador y Motor de Cálculo (F7, F8) y Evaluador: valorar si una anomalía o factor publicado es reproducible antes de usarlo como evidencia; documentar siempre el método de replicación.
- **Limitaciones:** Resultados ligados a la base de factores y a las decisiones de construcción de los autores; centrado en renta variable.
- **Criterios derivados:** Ninguno aún.
- **Origen:** Alta V4.0 (2026-11-02), segunda tanda de verificación.

#### fondo_entry_215 · Q 95 (A) — A manifesto for reproducible science

- **Cita normalizada:** Munafò, M. R., Nosek, B. A., Bishop, D. V. M., Button, K. S., Chambers, C. D., Percie du Sert, N., Simonsohn, U., Wagenmakers, E.-J., Ware, J. J., y Ioannidis, J. P. A. (2017). A manifesto for reproducible science. Nature Human Behaviour, 1(1), 0021.
- **Tipo de fuente:** Artículo revisado por pares (perspectiva de consenso)
- **Ámbito metodológico:** MB-05 Verificación y reproducibilidad (principal) · secundarias: MB-01
- **Calidad Q:** 95 (A) — Tipo 25/25 · Rigor 15/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 10/10
- **DOI / URL:** DOI: 10.1038/s41562-016-0021 · https://orca.cardiff.ac.uk/id/eprint/97336/
- **Acceso y licencia:** Acceso abierto (Creative Commons Attribution); PDF en el repositorio ORCA de Cardiff
- **Estado:** Vigente
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Munafò 2017 "A manifesto for reproducible science" Nature Human Behaviour»; WebFetch: sí)
- **Ficha metodológica:** Propone medidas para mejorar la fiabilidad de la investigación en cinco frentes (métodos, reporte y difusión, reproducibilidad, evaluación e incentivos), entre ellas el registro previo, la transparencia de datos y código y la protección frente al sesgo cognitivo del investigador.
- **Uso en el bloque:** DOC-A: lista de buenas prácticas para el diseño y registro de búsquedas y análisis del bloque.
- **Limitaciones:** Orientado a ciencias biomédicas y del comportamiento; recomendaciones generales, no protocolos.
- **Criterios derivados:** Ninguno aún.
- **Origen:** Alta V4.0 (2026-11-02), segunda tanda de verificación.

#### fondo_entry_209 · Q 95 (A) — … and the Cross-Section of Expected Returns

- **Cita normalizada:** Harvey, C. R., Liu, Y., y Zhu, H. (2016). … and the Cross-Section of Expected Returns. Review of Financial Studies, 29(1), 5-68 (Editor's Choice).
- **Tipo de fuente:** Artículo revisado por pares
- **Ámbito metodológico:** MB-05 Verificación y reproducibilidad (principal) · secundarias: MB-07
- **Calidad Q:** 95 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 10/10 · Independencia 10/10 · Acceso 8/10
- **DOI / URL:** DOI: 10.1093/rfs/hhv059 · https://ideas.repec.org/a/oup/rfinst/v29y2016i1p5-68..html · Documento de trabajo: https://papers.ssrn.com/abstract=2513152 · https://nber.org/papers/w20592
- **Acceso y licencia:** Revista por suscripción; documento de trabajo gratuito en SSRN y NBER
- **Estado:** Vigente
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Harvey Liu Zhu "...and the Cross-Section of Expected Returns" Review of Financial Studies 2016 multiple testing»; WebFetch: sí (SSRN e IDEAS/RePEc))
- **Ficha metodológica:** Con cientos de factores propuestos, el umbral habitual t ≈ 2,0 deja de ser válido: construye un marco de pruebas múltiples que tiene en cuenta la correlación entre pruebas y los datos no publicados y concluye que un factor nuevo debería superar t > 3,0; la mayoría de los hallazgos declarados en economía financiera serían probablemente falsos.
- **Uso en el bloque:** Motor de Cálculo (F8) y Evaluador: umbral de significación reforzado y registro del número de pruebas realizadas antes de dar por buena una señal o factor.
- **Limitaciones:** La corrección depende de supuestos sobre el número de pruebas no publicadas; contrastar con fondo_entry_208.
- **Criterios derivados:** Ninguno aún.
- **Origen:** Alta V4.0 (2026-11-02), segunda tanda de verificación.

#### fondo_entry_205 · Q 94 (A) — Misconduct accounts for the majority of retracted scientific publications

- **Cita normalizada:** Fang, F. C., Steen, R. G., y Casadevall, A. (2012). Misconduct accounts for the majority of retracted scientific publications. Proceedings of the National Academy of Sciences, 109(42), 17028-17033 (corrección: PNAS 110(3), 1137).
- **Tipo de fuente:** Artículo revisado por pares (estudio empírico)
- **Ámbito metodológico:** MB-05 Verificación y reproducibilidad (principal) · secundarias: MB-07
- **Calidad Q:** 94 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 8/10 · Impacto 10/10 · Independencia 10/10 · Acceso 9/10
- **DOI / URL:** DOI: 10.1073/pnas.1212247109 · https://pmc.ncbi.nlm.nih.gov/articles/PMC3479492
- **Acceso y licencia:** Texto completo gratuito en PMC (cortesía de la NAS; sin licencia CC declarada)
- **Estado:** Vigente
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Fang Steen Casadevall 2012 "Misconduct accounts for the majority of retracted scientific publications" PNAS»; WebFetch: sí)
- **Ficha metodológica:** Revisa 2.047 artículos retractados indexados en PubMed: ~67 % de las retractaciones se deben a mala conducta (fraude o sospecha ~43 %, publicación duplicada ~14 %, plagio ~10 %) y solo ~21 % a error; los avisos de retractación poco informativos subestimaban el fraude. Justifica comprobar retractaciones y erratas en cada alta y en la revisión trimestral, leyendo el motivo real y no solo el aviso.
- **Uso en el bloque:** DOC-A y Evaluadores (revisión trimestral 13.4): control de retractaciones y acción `BORRAR` por contenido retractado.
- **Limitaciones:** Solo biomedicina y ciencias de la vida, datos hasta mayo de 2012; no incluye economía ni finanzas.
- **Criterios derivados:** Ninguno aún.
- **Origen:** Alta V4.0 (2026-11-02), verificada por búsqueda web y lectura de la página.

#### fondo_entry_211 · Q 93 (A) — Transparency, Reproducibility, and the Credibility of Economics Research

- **Cita normalizada:** Christensen, G., y Miguel, E. (2018). Transparency, Reproducibility, and the Credibility of Economics Research. Journal of Economic Literature (número de septiembre). Documento de trabajo previo: NBER Working Paper 22989 (diciembre de 2016).
- **Tipo de fuente:** Artículo de revisión revisado por pares (survey)
- **Ámbito metodológico:** MB-05 Verificación y reproducibilidad (principal) · secundarias: MB-07
- **Calidad Q:** 93 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 14/15 · Vigencia 9/10 · Impacto 9/10 · Independencia 10/10 · Acceso 9/10
- **DOI / URL:** DOI: 10.1257/jel.20171350 · NBER WP 22989: https://www.nber.org/papers/w22989.pdf · Reseña de la AEA: https://aeastaging.aeaweb.org/research/transparency-reproducibility-credibility-economics
- **Acceso y licencia:** Documento de trabajo NBER gratuito; versión JEL por suscripción
- **Estado:** Vigente
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Christensen Miguel 2018 "Transparency, Reproducibility, and the Credibility of Economics Research" Journal of Economic Literature pdf»; WebFetch: sí (NBER y AEA))
- **Ficha metodológica:** Revisión de la evidencia sobre sesgo de publicación, búsqueda de especificaciones y falta de replicación en economía (Ioannidis 2005, Brodeur et al. 2016, proyecto JMCB de Dewald, Thursby y Anderson 1986, Franco et al. 2014) y de las soluciones: registro previo, planes de análisis previos, publicación de datos y código, y replicación.
- **Uso en el bloque:** DOC-A y Documentadores: marco general para puntuar la transparencia de una obra económica y para justificar los criterios de reproducibilidad del Fondo.
- **Limitaciones:** Volumen y páginas de JEL no confirmados en las páginas leídas; centrado en economía académica.
- **Criterios derivados:** Ninguno aún.
- **Origen:** Alta V4.0 (2026-11-02), segunda tanda de verificación.

#### fondo_entry_216 · Q 93 (A) — The FAIR Guiding Principles for scientific data management and stewardship

- **Cita normalizada:** Wilkinson, M. D., Dumontier, M., Aalbersberg, IJ. J., et al. (2016). The FAIR Guiding Principles for scientific data management and stewardship. Scientific Data, 3, 160018.
- **Tipo de fuente:** Artículo revisado por pares (principios de consenso)
- **Ámbito metodológico:** MB-05 Verificación y reproducibilidad (principal) · secundarias: MB-04
- **Calidad Q:** 93 (A) — Tipo 25/25 · Rigor 14/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 9/10
- **DOI / URL:** DOI: 10.1038/sdata.2016.18 · https://pure.eur.nl/en/publications/the-fair-guiding-principles-for-scientific-data-management-and-st/
- **Acceso y licencia:** Acceso abierto en la editorial (licencia no indicada en la página del repositorio leída)
- **Estado:** Vigente
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Wilkinson 2016 "The FAIR Guiding Principles for scientific data management and stewardship" Scientific Data»; WebFetch: sí (repositorio de la Universidad Erasmus))
- **Ficha metodológica:** Principios FAIR: datos localizables (identificadores persistentes y metadatos ricos), accesibles (protocolos abiertos), interoperables (vocabularios normalizados) y reutilizables (licencia y procedencia claras). Proporciona la vara de medir la estabilidad y reutilización de una fuente de datos.
- **Uso en el bloque:** Documentadores de F7–F9 y HT-02: criterio de Accesibilidad y estabilidad; diseño de metadatos de las fichas del Fondo.
- **Limitaciones:** Principios, no métricas; su aplicación concreta requiere indicadores adicionales.
- **Criterios derivados:** Ninguno aún.
- **Origen:** Alta V4.0 (2026-11-02), segunda tanda de verificación.

#### fondo_entry_212 · Q 93 (A) — Estimating the reproducibility of psychological science

- **Cita normalizada:** Open Science Collaboration (2015). Estimating the reproducibility of psychological science. Science, 349(6251), aac4716.
- **Tipo de fuente:** Artículo revisado por pares (estudio de replicación a gran escala)
- **Ámbito metodológico:** MB-05 Verificación y reproducibilidad (principal) · secundarias: —
- **Calidad Q:** 93 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 8/10 · Impacto 10/10 · Independencia 10/10 · Acceso 7/10
- **DOI / URL:** DOI: 10.1126/science.aac4716 (https://doi.org/10.1126/science.aac4716) · Verificada en: https://ber.jcx.au/critical-reading/open-science-collaboration-2015.html
- **Acceso y licencia:** Editor por suscripción
- **Estado:** Vigente
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Replication crisis Wikipedia Open Science Collaboration 2015 Camerer 2016 economics Ioannidis 2005»; WebFetch: sí, página índice (ber.jcx.au); página del editor no cargada)
- **Ficha metodológica:** Replicación coordinada de un centenar de estudios publicados en revistas de psicología, con tasas de éxito muy inferiores a las de los originales; es el estudio que abrió el debate sobre la «crisis de replicación». Su lectura debe acompañarse del comentario de Gilbert et al. (fondo_entry_214) y de la respuesta de Anderson et al. (2016).
- **Uso en el bloque:** DOC-A: referencia canónica para justificar que un resultado aislado no se trate como hecho establecido sin replicación.
- **Limitaciones:** Psicología experimental; las tasas dependen del criterio de éxito de replicación elegido.
- **Criterios derivados:** Ninguno aún.
- **Origen:** Alta V4.0 (2026-11-02), segunda tanda de verificación.

#### fondo_entry_200 · Q 93 (A) — Scholarly Context Not Found: One in Five Articles Suffers from Reference Rot

- **Cita normalizada:** Klein, M., Van de Sompel, H., Sanderson, R., Shankar, H., Balakireva, L., Zhou, K., y Tobin, R. (2014). Scholarly Context Not Found: One in Five Articles Suffers from Reference Rot. PLoS ONE, 9(12), e115253.
- **Tipo de fuente:** Artículo revisado por pares (estudio empírico)
- **Ámbito metodológico:** MB-05 Verificación y reproducibilidad (principal) · secundarias: MB-04
- **Calidad Q:** 93 (A) — Tipo 23/25 · Rigor 18/20 · Autoridad 14/15 · Vigencia 9/10 · Impacto 9/10 · Independencia 10/10 · Acceso 10/10
- **DOI / URL:** DOI: 10.1371/journal.pone.0115253 · https://pmc.ncbi.nlm.nih.gov/articles/PMC4277367 · Datos del proyecto Hiberlink: Edinburgh DataShare, DOI: 10.7488/ds/230 (https://www.research.ed.ac.uk/en/datasets/hiberlink-project-data/)
- **Acceso y licencia:** Acceso abierto (Creative Commons Attribution)
- **Estado:** Vigente
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Klein 2014 "Scholarly Context Not Found: One in Five Articles Suffers from Reference Rot" PLoS ONE»; WebFetch: sí)
- **Ficha metodológica:** Define «reference rot» como suma de enlace roto (link rot) y deriva de contenido (content drift) y la mide sobre más de un millón de referencias web en 3,5 millones de artículos (arXiv, Elsevier, PMC, 1997–2012): uno de cada cinco artículos, y siete de cada diez de los que citan recursos web, ya no permiten revisitar su contexto. Justifica la copia archivada obligatoria en cada alta.
- **Uso en el bloque:** DOC-A y Documentadores/Buscadores de todos los bloques (HT-02): fundamento de la exigencia de copia archivada y del barrido periódico de enlaces.
- **Limitaciones:** Corpus científico-técnico hasta 2012; las tasas exactas por año figuran en gráficos; no cubre fuentes financieras ni de opinión.
- **Criterios derivados:** Ninguno aún.
- **Origen:** Alta V4.0 (2026-11-02), verificada por búsqueda web y lectura de la página.

#### fondo_entry_201 · Q 92 (A) — Scholarly Context Adrift: Three out of Four URI References Lead to Changed Content

- **Cita normalizada:** Jones, S. M., Van de Sompel, H., Shankar, H., Klein, M., Tobin, R., y Grover, C. (2016). Scholarly Context Adrift: Three out of Four URI References Lead to Changed Content. PLoS ONE, 11(12), e0167475 (corrección: PLoS ONE 12(1), e0171057, 2017).
- **Tipo de fuente:** Artículo revisado por pares (estudio empírico)
- **Ámbito metodológico:** MB-05 Verificación y reproducibilidad (principal) · secundarias: —
- **Calidad Q:** 92 (A) — Tipo 23/25 · Rigor 18/20 · Autoridad 14/15 · Vigencia 9/10 · Impacto 8/10 · Independencia 10/10 · Acceso 10/10
- **DOI / URL:** DOI: 10.1371/journal.pone.0167475 · https://pmc.ncbi.nlm.nih.gov/articles/PMC5135130
- **Acceso y licencia:** Acceso abierto (CC0)
- **Estado:** Vigente
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Jones 2016 "Scholarly Context Adrift: Three out of Four URI References Lead to Changed Content" PLoS ONE»; WebFetch: sí)
- **Ficha metodológica:** Con 19 archivos web, mide la deriva de contenido: más del 75 % de las referencias web que siguen vivas muestran contenido distinto del citado; entre las que tienen copia archivada representativa, 21,8 % de enlaces rotos y 59,7 % de deriva. Demuestra que un código HTTP 200 no prueba que el contenido citado siga ahí: hay que comparar con la copia archivada o con un hash.
- **Uso en el bloque:** HT-02 y DOC-A: fundamento del estado `CONTENIDO_CAMBIADO` (variación de hash) y de archivar en el momento de la cita.
- **Limitaciones:** Umbral de similitud muy estricto (estimaciones conservadoras); corpus STM 1997–2012.
- **Criterios derivados:** Ninguno aún.
- **Origen:** Alta V4.0 (2026-11-02), verificada por búsqueda web y lectura de la página.

#### fondo_entry_213 · Q 92 (A) — Evaluating replicability of laboratory experiments in economics

- **Cita normalizada:** Camerer, C. F., Dreber, A., Forsell, E., Ho, T.-H., Huber, J., Johannesson, M., Kirchler, M., Almenberg, J., Altmejd, A., Chan, T., Heikensten, E., Holzmeister, F., Imai, T., Isaksson, S., Nave, G., Pfeiffer, T., Razen, M., y Wu, H. (2016). Evaluating replicability of laboratory experiments in economics. Science, 351(6280), 1433-1436.
- **Tipo de fuente:** Artículo revisado por pares (estudio de replicación)
- **Ámbito metodológico:** MB-05 Verificación y reproducibilidad (principal) · secundarias: —
- **Calidad Q:** 92 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 8/10 · Impacto 9/10 · Independencia 10/10 · Acceso 7/10
- **DOI / URL:** DOI: 10.1126/science.aaf0918 (https://doi.org/10.1126/science.aaf0918) · Verificada en: https://td.jcx.au/interpreting-trial-results/the-replication-crisis y https://ber.jcx.au/critical-reading/open-science-collaboration-2015.html
- **Acceso y licencia:** Editor por suscripción
- **Estado:** Vigente
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Replication crisis Wikipedia Open Science Collaboration 2015 Camerer 2016 economics Ioannidis 2005»; WebFetch: sí, páginas índice (td.jcx.au y ber.jcx.au); página del editor no cargada)
- **Ficha metodológica:** Replica experimentos de laboratorio de economía publicados en revistas de primer nivel y compara la tasa de replicación con la de psicología; aporta la evidencia de replicabilidad específica de la economía experimental.
- **Uso en el bloque:** Documentadores de F7: ponderar la evidencia de economía conductual y experimental según exista replicación.
- **Limitaciones:** Muestra pequeña de experimentos de laboratorio; no cubre estudios con datos de mercado.
- **Criterios derivados:** Ninguno aún.
- **Origen:** Alta V4.0 (2026-11-02), segunda tanda de verificación.

#### fondo_entry_210 · Q 91 (A) — Is Economics Research Replicable? Sixty Published Papers From Thirteen Journals Say «Often Not»

- **Cita normalizada:** Chang, A. C., y Li, P. (2022). Is Economics Research Replicable? Sixty Published Papers From Thirteen Journals Say «Often Not». Critical Finance Review, 11(1), 185-206. Versión previa: Finance and Economics Discussion Series 2015-083, Board of Governors of the Federal Reserve System («Usually Not»).
- **Tipo de fuente:** Artículo revisado por pares (con documento de trabajo de banco central)
- **Ámbito metodológico:** MB-05 Verificación y reproducibilidad (principal) · secundarias: —
- **Calidad Q:** 91 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 13/15 · Vigencia 9/10 · Impacto 8/10 · Independencia 10/10 · Acceso 9/10
- **DOI / URL:** DOI: 10.1561/104.00000053 · https://nowpublishers.com/article/Details/CFR-0053 · FEDS 2015-083, DOI: 10.17016/FEDS.2015.083: https://www.federalreserve.gov/econres/feds/is-economics-research-replicable-sixty-published-papers-from-thirteen-journals-say-quotusually-notquot.htm
- **Acceso y licencia:** Documento de trabajo FEDS gratuito (con materiales de replicación); versión de revista en Now Publishers
- **Estado:** Vigente
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Chang Li "Is Economics Research Replicable? Sixty Published Papers from Thirteen Journals Say Often Not" Federal Reserve FEDS»; WebFetch: sí (Fed y Now Publishers))
- **Ficha metodológica:** Intenta reproducir 67 artículos de macroeconomía de 13 revistas con los datos y el código de los autores: sin ayuda de los autores reproduce el resultado cualitativo principal en 22 de 67 (33 %), y con su ayuda en 29 de 59 (49 %); las revistas que exigen ficheros de replicación los tienen en 29 de 35 casos frente a 11 de 26. Base empírica para exigir datos y código disponibles como señal de verificabilidad.
- **Uso en el bloque:** Documentadores de F7 y F8: puntuar más alto en Rigor y Accesibilidad las obras con datos y código públicos; DOC-A: criterio de reproducibilidad.
- **Limitaciones:** Solo macroeconomía empírica; reproducción con los materiales originales, no replicación con datos nuevos.
- **Criterios derivados:** Ninguno aún.
- **Origen:** Alta V4.0 (2026-11-02), segunda tanda de verificación.

#### fondo_entry_008 · Q 88 (A) — Sandve et al. (2013)

- **Cita normalizada:** Sandve, G. K., Nekrutenko, A., Taylor, J., y Hovig, E. (2013). Ten Simple Rules for Reproducible Computational Research. PLoS Computational Biology, 9(10), e1003285.
- **Tipo de fuente:** Artículo revisado por pares (guía)
- **Ámbito metodológico:** MB-05 Verificación y reproducibilidad (principal) · secundarias: MB-04 (en V2.3: Verificación y reproducibilidad)
- **Calidad Q:** 88 (A) — Tipo 22/25 · Rigor 14/20 · Autoridad 13/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 10/10
- **DOI / URL:** DOI: 10.1371/journal.pcbi.1003285 · Acceso abierto en la editorial (journals.plos.org) · Verificación (anexo 8.1 V2.3): DOI: doi.org/10.1371/journal.pcbi.1003285 (PLOS Computational Biology, acceso abierto, ficha)
- **Estado:** Vigente
- **Estado del enlace:** PENDIENTE_BARRIDO
- **Última verificación:** 2026-10-25
- **Ficha metodológica:** Diez reglas de reproducibilidad computacional (versionar todo, registrar cada resultado intermedio, externalizar scripts y datos, no sobrescribir resultados). Aplicadas al proceso documental del bloque, garantizan que cualquier búsqueda y verificación pueda reconstruirse sin ayuda del agente que la ejecutó.
- **Criterios derivados:** fondo_criterion_004
- **Verificación V2.3:** Completa (carga de arranque): cita, DOI y acceso abierto verificados el 25/10/2026; comprobaciones omitidas: lectura del texto completo por el Documentador

#### fondo_entry_217 · Q 86 (A) — COPE Retraction guidelines (actualización 2025)

- **Cita normalizada:** Committee on Publication Ethics (COPE) (2025, septiembre). Retraction guidelines (actualización de la versión de 2019) y nueva guía sobre expresiones de preocupación. Reseña: Retraction Watch (4-9-2025), «New COPE retraction guidelines address paper mills, third parties, and more».
- **Tipo de fuente:** Guía de organismo de ética editorial
- **Ámbito metodológico:** MB-05 Verificación y reproducibilidad (principal) · secundarias: MB-07
- **Calidad Q:** 86 (A) — Tipo 20/25 · Rigor 14/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 9/10 · Acceso 9/10
- **DOI / URL:** https://publicationethics.org/guidance/guideline/retraction-guidelines (enlace citado en la reseña) · Guía de expresiones de preocupación: DOI 10.24318/mw2J3661 · Reseña: https://retractionwatch.com/2025/09/04/new-cope-retraction-guidelines-address-paper-mills-third-parties-and-more/
- **Acceso y licencia:** Acceso gratuito
- **Estado:** Vigente
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «COPE retraction guidelines 2019 publicationethics.org Retraction Watch database Crossref open»; WebFetch: sí, reseña de Retraction Watch; página de COPE no cargada)
- **Ficha metodológica:** Fija cuándo retractar (incluidos fábricas de artículos, autoría no verificable, revisión por pares manipulada y uso no declarado de IA), exige avisos sin muro de pago y conforme a la práctica NISO RP-45-2024, regula las retractaciones en bloque y recomienda una expresión de preocupación mientras dura una investigación.
- **Uso en el bloque:** DOC-A y Evaluadores (revisión trimestral): interpretar avisos de retractación y expresiones de preocupación; una expresión de preocupación justifica `DEGRADAR` y una retractación, `BORRAR`.
- **Limitaciones:** Texto de COPE no leído directamente (verificado a través de la reseña); guía para editores, no para lectores.
- **Criterios derivados:** Ninguno aún.
- **Origen:** Alta V4.0 (2026-11-02), segunda tanda de verificación.

#### fondo_entry_202 · Q 85 (A) — Perma: Scoping and Addressing the Problem of Link and Reference Rot in Legal Citations

- **Cita normalizada:** Zittrain, J., Albert, K., y Lessig, L. (2014). Perma: Scoping and Addressing the Problem of Link and Reference Rot in Legal Citations. Harvard Law Review Forum, 127, 176. Reeditado en Legal Information Management, 14(2), 88-99.
- **Tipo de fuente:** Artículo de revista jurídica (estudio empírico y propuesta)
- **Ámbito metodológico:** MB-05 Verificación y reproducibilidad (principal) · secundarias: —
- **Calidad Q:** 85 (A) — Tipo 22/25 · Rigor 14/20 · Autoridad 15/15 · Vigencia 8/10 · Impacto 9/10 · Independencia 8/10 · Acceso 9/10
- **DOI / URL:** DOI (versión LIM): 10.1017/S1472669614000255 · https://harvardlawreview.org/2014/03/perma-scoping-and-addressing-the-problem-of-link-and-reference-rot-in-legal-citations/ · https://www.cambridge.org/core/journals/legal-information-management/article/abs/perma-scoping-and-addressing-the-problem-of-link-and-reference-rot-in-legal-citations/15A59548BF9882B06D3064DA7E290859
- **Acceso y licencia:** Gratuito en harvardlawreview.org; versión LIM por suscripción
- **Estado:** Vigente
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Zittrain Albert Lessig 2014 "Perma: Scoping and Addressing the Problem of Link and Reference Rot in Legal Citations"»; WebFetch: sí)
- **Ficha metodológica:** Más del 70 % de las URL de tres revistas de Harvard y el 49,9 % de los enlaces de sentencias del Tribunal Supremo de EE. UU. ya no muestran el material citado; además, un código 200 es una señal poco fiable de que la fuente sigue presente. Propone el archivado permanente en el momento de citar (Perma.cc) como remedio institucional.
- **Uso en el bloque:** HT-02 y DOC-A: archivar la versión citada en el alta; no confiar en el código HTTP como prueba de vigencia.
- **Limitaciones:** Corpus jurídico estadounidense; los autores impulsan Perma.cc (independencia limitada en la parte propositiva).
- **Criterios derivados:** Ninguno aún.
- **Origen:** Alta V4.0 (2026-11-02), verificada por búsqueda web y lectura de la página.

#### fondo_entry_220 · Q 84 (A) — DOI Handbook

- **Cita normalizada:** International DOI Foundation (versión consultada: actualización de 17-10-2015). DOI Handbook. DOI 10.1000/182. El sistema DOI está normalizado como ISO 26324 (aprobada en 2010, publicada en 2012).
- **Tipo de fuente:** Manual técnico de organismo normalizador
- **Ámbito metodológico:** MB-05 Verificación y reproducibilidad (principal) · secundarias: MB-04
- **Calidad Q:** 84 (A) — Tipo 20/25 · Rigor 13/20 · Autoridad 15/15 · Vigencia 8/10 · Impacto 9/10 · Independencia 9/10 · Acceso 10/10
- **DOI / URL:** DOI: 10.1000/182 · https://albany.doi.org/doi_handbook/1_Introduction.html · https://www-old.doi.org/doi_handbook/TOC.html
- **Acceso y licencia:** Acceso gratuito
- **Estado:** Vigente
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «DOI Handbook International DOI Foundation ISO 26324 persistent identifier resolution doi.org»; WebFetch: sí)
- **Ficha metodológica:** Referencia oficial del sistema DOI: el nombre DOI es persistente aunque cambie la información del objeto y se resuelve, mediante el Handle System, a datos actuales como la URL, con posibilidad de resolución múltiple (varias ubicaciones o registros de metadatos). Fundamenta preferir el DOI sobre la URL en las fichas.
- **Uso en el bloque:** HT-02 y Documentadores: el DOI resuelto es la comprobación primaria del enlace; la URL, secundaria.
- **Limitaciones:** La página consultada no se actualiza desde 2015; la norma ISO 26324 es de pago.
- **Criterios derivados:** Ninguno aún.
- **Origen:** Alta V4.0 (2026-11-02), segunda tanda de verificación.

#### fondo_entry_214 · Q 83 (A) — Comment on «Estimating the reproducibility of psychological science»

- **Cita normalizada:** Gilbert, D. T., King, G., Pettigrew, S., y Wilson, T. D. (2016). Comment on «Estimating the reproducibility of psychological science». Science, 351(6277), 1037. Respuesta: Anderson, C. J., et al. (2016), Science, 351(6277), 1037 (DOI 10.1126/science.aad9163).
- **Tipo de fuente:** Comentario técnico revisado (Science)
- **Ámbito metodológico:** MB-05 Verificación y reproducibilidad (principal) · secundarias: —
- **Calidad Q:** 83 (A) — Tipo 22/25 · Rigor 14/20 · Autoridad 14/15 · Vigencia 8/10 · Impacto 8/10 · Independencia 10/10 · Acceso 7/10
- **DOI / URL:** DOI: 10.1126/science.aad7243 (https://doi.org/10.1126/science.aad7243) · Verificada en: https://ber.jcx.au/critical-reading/open-science-collaboration-2015.html
- **Acceso y licencia:** Editor por suscripción
- **Estado:** Vigente
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Replication crisis Wikipedia Open Science Collaboration 2015 Camerer 2016 economics Ioannidis 2005»; WebFetch: sí, página índice (ber.jcx.au); página del editor no cargada)
- **Ficha metodológica:** Crítica metodológica a fondo_entry_212: sostiene que el error muestral, la baja potencia y las desviaciones de protocolo en las réplicas pueden explicar buena parte de los fracasos, por lo que la tasa de replicación es sensible a cómo se mide. Enseña a leer con cautela cualquier cifra de «replicabilidad».
- **Uso en el bloque:** Evaluador y DOC-A: contrapeso a fondo_entry_212 y fondo_entry_208 al interpretar tasas de replicación.
- **Limitaciones:** Comentario breve; debate abierto con la respuesta de Anderson et al. (2016).
- **Criterios derivados:** Ninguno aún.
- **Origen:** Alta V4.0 (2026-11-02), segunda tanda de verificación.

#### fondo_entry_203 · Q 82 (A) — When Online Content Disappears

- **Cita normalizada:** Chapekis, A., Bestvater, S., Remy, E., y Rivero, G. (2024, 17 de mayo). When Online Content Disappears. Pew Research Center (Data Labs).
- **Tipo de fuente:** Informe técnico con metodología
- **Ámbito metodológico:** MB-05 Verificación y reproducibilidad (principal) · secundarias: MB-07
- **Calidad Q:** 82 (A) — Tipo 15/25 · Rigor 16/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 7/10 · Independencia 10/10 · Acceso 10/10
- **DOI / URL:** https://www.pewresearch.org/data-labs/2024/05/17/when-online-content-disappears/ · PDF: https://pewresearch.org/wp-content/uploads/sites/20/2024/05/pl_2024.05.17_link-rot_report.pdf
- **Acceso y licencia:** Acceso gratuito
- **Estado:** Vigente
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Pew Research Center 2024 "When Online Content Disappears" 38% of webpages»; WebFetch: sí)
- **Ficha metodológica:** Mide la pérdida de contenido web general 2013–2023: el 25 % de las páginas ya no es accesible (38 % de las de 2013); el 21 % de páginas gubernamentales y el 23 % de las de medios tienen algún enlace roto; el 54 % de los artículos de Wikipedia tiene al menos una referencia muerta; ~18 % de los tuits desaparece en tres meses. Extiende la evidencia de enlace roto a fuentes institucionales, de prensa y redes sociales.
- **Uso en el bloque:** HT-02 y Documentadores de F9: calibrar la frecuencia de barrido y archivar de inmediato fuentes de prensa y redes (TF-03, TF-12).
- **Limitaciones:** Muestras de EE. UU. y en inglés; descriptivo, sin análisis por tipo de editor financiero.
- **Criterios derivados:** Ninguno aún.
- **Origen:** Alta V4.0 (2026-11-02), verificada por búsqueda web y lectura de la página.

#### fondo_entry_204 · Q 80 (A) — RFC 7089: HTTP Framework for Time-Based Access to Resource States — Memento

- **Cita normalizada:** Van de Sompel, H., Nelson, M., y Sanderson, R. (2013). HTTP Framework for Time-Based Access to Resource States — Memento. RFC 7089 (Informational, Independent Submission). IETF.
- **Tipo de fuente:** Especificación técnica
- **Ámbito metodológico:** MB-05 Verificación y reproducibilidad (principal) · secundarias: MB-04
- **Calidad Q:** 80 (A) — Tipo 15/25 · Rigor 15/20 · Autoridad 13/15 · Vigencia 9/10 · Impacto 8/10 · Independencia 10/10 · Acceso 10/10
- **DOI / URL:** https://datatracker.ietf.org/doc/rfc7089
- **Acceso y licencia:** Acceso abierto (IETF)
- **Estado:** Vigente
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «RFC 7089 "HTTP Framework for Time-Based Access to Resource States -- Memento"»; WebFetch: sí)
- **Ficha metodológica:** Define la negociación por fecha (datetime negotiation), los TimeGates y los TimeMaps que listan las copias archivadas de un recurso en distintos archivos web. Es el protocolo que permite a HT-02 localizar automáticamente una copia archivada cercana a la fecha de cita de cualquier URL.
- **Uso en el bloque:** HT-02: búsqueda automática de copia archivada (acción `REPARAR`) y comprobación de la versión citada.
- **Limitaciones:** RFC informativo, no estándar del IETF; requiere archivos web compatibles con Memento.
- **Criterios derivados:** Ninguno aún.
- **Origen:** Alta V4.0 (2026-11-02), verificada por búsqueda web y lectura de la página.

#### fondo_entry_218 · Q 79 (B) — News: Crossref and Retraction Watch

- **Cita normalizada:** Hendricks, G., Lammey, R., Ofiesh, L., Bilder, G., y Pentz, E. (2023, 12 de septiembre). News: Crossref and Retraction Watch. Crossref Blog.
- **Tipo de fuente:** Comunicado institucional (infraestructura de metadatos)
- **Ámbito metodológico:** MB-05 Verificación y reproducibilidad (principal) · secundarias: MB-04
- **Calidad Q:** 79 (B) — Tipo 15/25 · Rigor 13/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 8/10 · Independencia 9/10 · Acceso 10/10
- **DOI / URL:** DOI: 10.13003/c23rw1d9 · https://crossref.org/blog/news-crossref-and-retraction-watch · Datos: https://gitlab.com/crossref/retraction-watch-data
- **Acceso y licencia:** Acceso gratuito; contenido del sitio bajo CC BY 4.0 (licencia del conjunto de datos no indicada en la página)
- **Estado:** Vigente
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Crossref Retraction Watch database acquisition 2023 openly available Crossref blog»; WebFetch: sí)
- **Ficha metodológica:** Crossref adquiere la base de datos de Retraction Watch y la hace pública: unas 50.000 retractaciones combinadas (≈43.000 de Retraction Watch y ≈14.000 de Crossref), descargables en CSV por la API de Crossref Labs y en GitLab, y visibles en la ruta /works/ cuando hay metadatos. Es la fuente operativa para comprobar retractaciones por DOI de forma automática.
- **Uso en el bloque:** HT-02 y DOC-A: cruce automático de los DOI del Fondo y de F7–F8 con la base de retractaciones en cada alta y en la revisión trimestral.
- **Limitaciones:** Cobertura dependiente de que el DOI exista; acuerdo comercial plurianual entre las partes.
- **Criterios derivados:** Ninguno aún.
- **Origen:** Alta V4.0 (2026-11-02), segunda tanda de verificación.

#### fondo_entry_219 · Q 71 (B) — Hiberlink project data

- **Cita normalizada:** Tobin, R., Grover, C., y Zhou, K. (2015). Hiberlink project data [conjunto de datos]. Edinburgh DataShare.
- **Tipo de fuente:** Conjunto de datos de investigación
- **Ámbito metodológico:** MB-05 Verificación y reproducibilidad (principal) · secundarias: MB-04
- **Calidad Q:** 71 (B) — Tipo 15/25 · Rigor 14/20 · Autoridad 12/15 · Vigencia 7/10 · Impacto 5/10 · Independencia 10/10 · Acceso 8/10
- **DOI / URL:** DOI: 10.7488/ds/230 · https://www.research.ed.ac.uk/en/datasets/hiberlink-project-data/
- **Acceso y licencia:** Acceso gratuito (licencia no indicada en la página)
- **Estado:** Vigente
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Klein 2014 "Scholarly Context Not Found: One in Five Articles Suffers from Reference Rot" PLoS ONE»; WebFetch: sí)
- **Ficha metodológica:** Ficheros XML con cerca de un millón de URI citadas en unos tres millones de artículos de arXiv, Elsevier y PMC (1997–2012): los datos de base de fondo_entry_200 y fondo_entry_201, que permiten reproducir o extender las mediciones de deterioro de referencias.
- **Uso en el bloque:** HT-02: conjunto de prueba para calibrar el detector de enlaces rotos y deriva de contenido.
- **Limitaciones:** Datos de 1997–2012; útil solo para pruebas y réplica, no como fuente de criterio.
- **Criterios derivados:** Ninguno aún.
- **Origen:** Alta V4.0 (2026-11-02), segunda tanda de verificación.

## MB-06 Métricas bibliométricas y cobertura de bases

#### fondo_entry_224 · Q 95 (A) — Google Scholar, Microsoft Academic, Scopus, Dimensions, Web of Science, and OpenCitations' COCI: a multidisciplinary comparison of coverage via citations

- **Cita normalizada:** Martín-Martín, A., Thelwall, M., Orduna-Malea, E., y Delgado López-Cózar, E. (2021). Google Scholar, Microsoft Academic, Scopus, Dimensions, Web of Science, and OpenCitations' COCI: a multidisciplinary comparison of coverage via citations. Scientometrics, 126(1), 871-906.
- **Tipo de fuente:** Artículo revisado por pares
- **Ámbito metodológico:** MB-06 Métricas bibliométricas y cobertura de bases (principal) · secundarias: MB-02
- **Calidad Q:** 95 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 14/15 · Vigencia 9/10 · Impacto 9/10 · Independencia 10/10 · Acceso 10/10
- **DOI / URL:** DOI: 10.1007/s11192-020-03690-4 · https://arxiv.org/pdf/2004.14329 · Repositorio de la Universidad de Granada: https://digibug.ugr.es/handle/10481/66233
- **Acceso y licencia:** Acceso abierto (arXiv y repositorio institucional)
- **Estado:** Vigente
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Martín-Martín Thelwall Orduna-Malea Delgado López-Cózar 2021 Google Scholar Microsoft Academic Scopus Dimensions Web of Science OpenCitations COCI comparison Scientometrics»; WebFetch: sí)
- **Ficha metodológica:** Con 3.073.351 citas a 2.515 documentos muy citados de 2006 en 252 categorías: Google Scholar encuentra el 88 % de todas las citas, Microsoft Academic el 60 %, Dimensions el 54 %, Scopus y WoS en torno al 52–60 % y COCI el 28 %. Es la comparación de cobertura más amplia disponible y procede de un grupo español (EC3, Universidad de Granada).
- **Uso en el bloque:** Buscadores de todos los bloques: elegir la base para contar citas y para búsquedas hacia adelante según disciplina.
- **Limitaciones:** Documentos de 2006; Microsoft Academic ya cerrado; no incluye OpenAlex (ver fondo_entry_231).
- **Criterios derivados:** Ninguno aún.
- **Origen:** Alta V4.0 (2026-11-02), segunda tanda de verificación.

#### fondo_entry_221 · Q 93 (A) — An index to quantify an individual's scientific research output

- **Cita normalizada:** Hirsch, J. E. (2005). An index to quantify an individual's scientific research output. Proceedings of the National Academy of Sciences, 102(46), 16569-16572.
- **Tipo de fuente:** Artículo revisado por pares
- **Ámbito metodológico:** MB-06 Métricas bibliométricas y cobertura de bases (principal) · secundarias: —
- **Calidad Q:** 93 (A) — Tipo 25/25 · Rigor 15/20 · Autoridad 15/15 · Vigencia 8/10 · Impacto 10/10 · Independencia 10/10 · Acceso 10/10
- **DOI / URL:** DOI: 10.1073/pnas.0507655102 · https://arxiv.org/pdf/physics/0508025 · https://pmc.ncbi.nlm.nih.gov/articles/PMC1283832
- **Acceso y licencia:** Acceso abierto (arXiv y PMC)
- **Estado:** Vigente
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «h-index Wikipedia Hirsch 2005 PNAS "An index to quantify an individual's scientific research output"»; WebFetch: sí (arXiv; PMC devolvió verificación de navegador))
- **Ficha metodológica:** Define el índice h: un investigador tiene índice h si h de sus artículos tienen al menos h citas cada uno. Es el indicador de autor más difundido y el que los Documentadores encontrarán en Google Scholar, Scopus y Web of Science.
- **Uso en el bloque:** Documentadores de F7–F8: dato orientativo de Autoridad del autor (nunca decisivo; ver fondo_entry_244 y fondo_entry_222).
- **Limitaciones:** Depende del campo, la edad académica, la coautoría y la base de datos usada (fondo_entry_242).
- **Criterios derivados:** Ninguno aún.
- **Origen:** Alta V4.0 (2026-11-02), segunda tanda de verificación.

#### fondo_entry_231 · Q 92 (A) — Reference Coverage Analysis of OpenAlex compared to Web of Science and Scopus

- **Cita normalizada:** Culbert, J., Hobert, A., Jahn, N., Haupka, N., Schmidt, M., Donner, P., y Mayr, P. (2025). Reference Coverage Analysis of OpenAlex compared to Web of Science and Scopus. Scientometrics (preprint arXiv:2401.16359, v3 de 1-11-2024).
- **Tipo de fuente:** Artículo revisado por pares
- **Ámbito metodológico:** MB-06 Métricas bibliométricas y cobertura de bases (principal) · secundarias: MB-02
- **Calidad Q:** 92 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 13/15 · Vigencia 10/10 · Impacto 7/10 · Independencia 10/10 · Acceso 10/10
- **DOI / URL:** DOI: 10.1007/s11192-025-05293-3 · https://arxiv.org/abs/2401.16359v3
- **Acceso y licencia:** Acceso abierto (arXiv)
- **Estado:** Vigente
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «OpenAlex coverage compared Scopus Web of Science study 2024 2025 Priem Piwowar Orr "OpenAlex: A fully-open index"»; WebFetch: sí)
- **Ficha metodológica:** Sobre 16,8 millones de publicaciones recientes indexadas en las tres bases, OpenAlex tiene recuentos medios de referencias y tasas de cobertura interna comparables a WoS y Scopus; capta más ORCID, menos resúmenes y un número similar de indicadores de acceso abierto. Avala OpenAlex como base abierta para búsquedas hacia atrás y hacia adelante.
- **Uso en el bloque:** Buscadores de todos los bloques: OpenAlex como base gratuita para la bola de nieve (fondo_criterion_002 y 003).
- **Limitaciones:** Resultados para publicaciones recientes; calidad de metadatos desigual (ver fondo_entry_232).
- **Criterios derivados:** Ninguno aún.
- **Origen:** Alta V4.0 (2026-11-02), segunda tanda de verificación.

#### fondo_entry_246 · Q 92 (A) — A standardized citation metrics author database annotated for scientific field

- **Cita normalizada:** Ioannidis, J. P. A., Baas, J., Klavans, R., y Boyack, K. W. (2019). A standardized citation metrics author database annotated for scientific field. PLOS Biology, 17(8), e3000384.
- **Tipo de fuente:** Artículo revisado por pares (base de datos)
- **Ámbito metodológico:** MB-06 Métricas bibliométricas y cobertura de bases (principal) · secundarias: —
- **Calidad Q:** 92 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 9/10 · Independencia 8/10 · Acceso 10/10
- **DOI / URL:** DOI: 10.1371/journal.pbio.3000384 · Verificada en: https://en.wikipedia.org/wiki/H-index
- **Acceso y licencia:** Acceso abierto
- **Estado:** Vigente
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «h-index Wikipedia Hirsch 2005 PNAS "An index to quantify an individual's scientific research output"»; WebFetch: sí, página índice; página del editor no cargada)
- **Ficha metodológica:** Base normalizada de métricas de citación por autor con indicador compuesto, autocitas separadas y anotación por campo científico; permite situar a un autor dentro de su campo en lugar de usar el h bruto.
- **Uso en el bloque:** Documentadores de F7–F8: comparar la autoridad de autores dentro de su disciplina.
- **Limitaciones:** Basada en Scopus (un coautor trabaja en Elsevier).
- **Criterios derivados:** Ninguno aún.
- **Origen:** Alta V4.0 (2026-11-02), segunda tanda de verificación.

#### fondo_entry_244 · Q 91 (A) — The h-index is no longer an effective correlate of scientific reputation

- **Cita normalizada:** Koltun, V., y Hafner, D. (2021). The h-index is no longer an effective correlate of scientific reputation. PLOS ONE, 16(6), e0253397.
- **Tipo de fuente:** Artículo revisado por pares
- **Ámbito metodológico:** MB-06 Métricas bibliométricas y cobertura de bases (principal) · secundarias: MB-07
- **Calidad Q:** 91 (A) — Tipo 23/25 · Rigor 17/20 · Autoridad 13/15 · Vigencia 10/10 · Impacto 8/10 · Independencia 10/10 · Acceso 10/10
- **DOI / URL:** DOI: 10.1371/journal.pone.0253397 · arXiv:2102.03234 · Verificada en: https://en.wikipedia.org/wiki/H-index
- **Acceso y licencia:** Acceso abierto
- **Estado:** Vigente
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «h-index Wikipedia Hirsch 2005 PNAS "An index to quantify an individual's scientific research output"»; WebFetch: sí, página índice; página del editor no cargada)
- **Ficha metodológica:** Muestra que la correlación entre el índice h y el reconocimiento científico (premios) ha caído con el aumento de la hiperautoría, y propone una variante fraccionada por coautoría.
- **Uso en el bloque:** Evaluador: el h no sirve como prueba de autoridad en campos con muchos coautores.
- **Limitaciones:** Análisis en física y campos afines; criterio de reputación basado en premios.
- **Criterios derivados:** Ninguno aún.
- **Origen:** Alta V4.0 (2026-11-02), segunda tanda de verificación.

#### fondo_entry_225 · Q 91 (A) — Google Scholar, Web of Science, and Scopus: A systematic comparison of citations in 252 subject categories

- **Cita normalizada:** Martín-Martín, A., Orduna-Malea, E., Thelwall, M., y Delgado López-Cózar, E. (2018). Google Scholar, Web of Science, and Scopus: A systematic comparison of citations in 252 subject categories. Journal of Informetrics, 12(4), 1160-1177.
- **Tipo de fuente:** Artículo revisado por pares
- **Ámbito metodológico:** MB-06 Métricas bibliométricas y cobertura de bases (principal) · secundarias: MB-02
- **Calidad Q:** 91 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 14/15 · Vigencia 8/10 · Impacto 9/10 · Independencia 10/10 · Acceso 7/10
- **DOI / URL:** DOI: 10.1016/j.joi.2018.09.002 · Verificada en la bibliografía de fondo_entry_224: https://arxiv.org/pdf/2004.14329
- **Acceso y licencia:** Editor por suscripción
- **Estado:** Vigente
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Martín-Martín Thelwall Orduna-Malea Delgado López-Cózar 2021 Google Scholar Microsoft Academic Scopus Dimensions Web of Science OpenCitations COCI comparison Scientometrics»; WebFetch: sí, página índice (bibliografía de fondo_entry_224); página del editor no cargada)
- **Ficha metodológica:** Antecedente de fondo_entry_224 limitado a las tres bases principales: compara por categoría temática las citas que encuentra cada una y su solapamiento, con especial ventaja de Google Scholar en humanidades, ciencias sociales y economía.
- **Uso en el bloque:** Buscadores: justificar el uso de Google Scholar como complemento obligado en ciencias sociales y economía.
- **Limitaciones:** Datos de 2006; superado en amplitud por fondo_entry_224.
- **Criterios derivados:** Ninguno aún.
- **Origen:** Alta V4.0 (2026-11-02), segunda tanda de verificación.

#### fondo_entry_222 · Q 90 (A) — Bibliometrics: The Leiden Manifesto for research metrics

- **Cita normalizada:** Hicks, D., Wouters, P., Waltman, L., de Rijcke, S., y Rafols, I. (2015, 23 de abril). Bibliometrics: The Leiden Manifesto for research metrics. Nature (Comment).
- **Tipo de fuente:** Artículo de opinión experta en revista de primer nivel (declaración de principios)
- **Ámbito metodológico:** MB-06 Métricas bibliométricas y cobertura de bases (principal) · secundarias: MB-07
- **Calidad Q:** 90 (A) — Tipo 22/25 · Rigor 14/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 9/10
- **DOI / URL:** https://leidenmanifesto.org/ · https://www.nature.com/news/bibliometrics-the-leiden-manifesto-for-research-metrics-1.17351
- **Acceso y licencia:** Acceso gratuito; 25 traducciones en el sitio oficial
- **Estado:** Vigente
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Leiden Manifesto for research metrics Hicks Wouters Waltman de Rijcke Rafols 2015 Nature»; WebFetch: sí (sitio oficial))
- **Ficha metodológica:** Diez principios para el uso responsable de métricas en evaluación: lo cuantitativo apoya y no sustituye al juicio experto, medir según la misión, transparencia y verificabilidad de datos y procesos, normalización por campo, evaluación cualitativa de individuos, evitar falsa precisión y revisar periódicamente los indicadores.
- **Uso en el bloque:** DOC-A y Documentadores: regla de que ninguna métrica de citación decide por sí sola la Q de una fuente.
- **Limitaciones:** Principios generales sin umbrales operativos; texto en Nature no leído (sí el sitio oficial).
- **Criterios derivados:** Ninguno aún.
- **Origen:** Alta V4.0 (2026-11-02), segunda tanda de verificación.

#### fondo_entry_233 · Q 89 (A) — The Journal Impact Factor: A brief history, critique, and discussion of adverse effects

- **Cita normalizada:** Larivière, V., y Sugimoto, C. R. (2018). The Journal Impact Factor: A brief history, critique, and discussion of adverse effects. En W. Glänzel, H. F. Moed, U. Schmoch y M. Thelwall (Eds.), Springer Handbook of Science and Technology Indicators. Springer. Preprint arXiv:1801.08992.
- **Tipo de fuente:** Capítulo de manual de referencia
- **Ámbito metodológico:** MB-06 Métricas bibliométricas y cobertura de bases (principal) · secundarias: MB-07
- **Calidad Q:** 89 (A) — Tipo 20/25 · Rigor 16/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 9/10
- **DOI / URL:** https://arxiv.org/pdf/1801.08992
- **Acceso y licencia:** Preprint de acceso abierto; manual por suscripción
- **Estado:** Vigente
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Journal impact factor Wikipedia criticism Seglen 1997 BMJ Garfield history meaning»; WebFetch: sí)
- **Ficha metodológica:** Historia y crítica del factor de impacto: asimetría numerador/denominador, ventana de dos años que favorece campos de cita rápida, distribuciones muy sesgadas (solo un tercio de los artículos alcanza el valor de su revista), ausencia de normalización por campo e inflación temporal; efectos adversos (ingeniería del FI, citas coercitivas, cárteles, falsos proveedores de «factores de impacto»).
- **Uso en el bloque:** Documentadores y Evaluador: no usar el FI de la revista como indicador de calidad de un artículo; detectar revistas con FI falsos.
- **Limitaciones:** DOI del capítulo y año de edición del manual no vistos en el preprint.
- **Criterios derivados:** Ninguno aún.
- **Origen:** Alta V4.0 (2026-11-02), segunda tanda de verificación.

#### fondo_entry_009 · Q 88 (A) — Harzing y Alakangas (2016)

- **Cita normalizada:** Harzing, A.-W., y Alakangas, S. (2016). Google Scholar, Scopus and the Web of Science: a longitudinal and cross-disciplinary comparison. Scientometrics, 106(2), 787-804.
- **Tipo de fuente:** Artículo revisado por pares
- **Ámbito metodológico:** MB-06 Métricas bibliométricas y cobertura de bases (principal) · secundarias: MB-02 (en V2.3: Métricas)
- **Calidad Q:** 88 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 14/15 · Vigencia 8/10 · Impacto 9/10 · Independencia 10/10 · Acceso 6/10
- **DOI / URL:** DOI: 10.1007/s11192-015-1798-9 · Editorial: link.springer.com (acceso por suscripción) · Verificación (anexo 8.1 V2.3): DOI: doi.org/10.1007/s11192-015-1798-9 (Scientometrics, Springer, ficha) · Publicaciones de la autora: harzing.com (recursos y copias de autor de sus trabajos sobre métricas)
- **Estado:** En revisión
- **Estado del enlace:** PENDIENTE_BARRIDO
- **Última verificación:** 2026-10-25
- **Ficha metodológica:** Compara longitudinalmente Google Scholar, Scopus y Web of Science por disciplina, con implicaciones directas para decidir qué métricas de citación son fiables en cada ámbito y qué cobertura esperar de cada base. Cuando el bloque necesite consultar métricas de citación de una fuente (campo 19 de la ficha de la Documentación), esta entrada guiará la elección de la base.
- **Criterios derivados:** Ninguno aún (destilación pendiente de acceso al texto completo)
- **Verificación V2.3:** Ligera (carga de arranque): cita y DOI verificados el 25/10/2026; texto completo no obtenido (peldaño 5 de la escalera); comprobaciones omitidas: lectura del contenido completo
- **Nota:** Texto completo tras muro de pago (en revisión).

#### fondo_entry_241 · Q 88 (A) — What do citation counts measure? A review of studies on citing behavior

- **Cita normalizada:** Bornmann, L., y Daniel, H.-D. (2008). What do citation counts measure? A review of studies on citing behavior. Journal of Documentation, 64(1), 45-80.
- **Tipo de fuente:** Artículo de revisión revisado por pares
- **Ámbito metodológico:** MB-06 Métricas bibliométricas y cobertura de bases (principal) · secundarias: MB-07
- **Calidad Q:** 88 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 14/15 · Vigencia 8/10 · Impacto 10/10 · Independencia 10/10 · Acceso 5/10
- **DOI / URL:** DOI: 10.1108/00220410810844150 · Verificada en: https://en.wikipedia.org/wiki/H-index (bibliografía)
- **Acceso y licencia:** Editor por suscripción
- **Estado:** Vigente
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «h-index Wikipedia Hirsch 2005 PNAS "An index to quantify an individual's scientific research output"»; WebFetch: sí, página índice; página del editor no cargada)
- **Ficha metodológica:** Revisa los estudios sobre por qué se cita: las citas reflejan no solo calidad o influencia, sino también motivos sociales, retóricos y de visibilidad, lo que limita su interpretación como medida de calidad.
- **Uso en el bloque:** Evaluador: interpretar el criterio Impacto (citas) como señal de uso, no de veracidad.
- **Limitaciones:** Revisión de 2008.
- **Criterios derivados:** Ninguno aún.
- **Origen:** Alta V4.0 (2026-11-02), segunda tanda de verificación.

#### fondo_entry_234 · Q 88 (A) — Why the impact factor of journals should not be used for evaluating research

- **Cita normalizada:** Seglen, P. O. (1997). Why the impact factor of journals should not be used for evaluating research. British Medical Journal, 314(7079), 498-502.
- **Tipo de fuente:** Artículo revisado por pares
- **Ámbito metodológico:** MB-06 Métricas bibliométricas y cobertura de bases (principal) · secundarias: —
- **Calidad Q:** 88 (A) — Tipo 25/25 · Rigor 15/20 · Autoridad 14/15 · Vigencia 8/10 · Impacto 10/10 · Independencia 10/10 · Acceso 6/10
- **DOI / URL:** DOI no visto · Verificada en la bibliografía de fondo_entry_233: https://arxiv.org/pdf/1801.08992
- **Acceso y licencia:** Editor (acceso no comprobado)
- **Estado:** Vigente
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Journal impact factor Wikipedia criticism Seglen 1997 BMJ Garfield history meaning»; WebFetch: sí, página índice (bibliografía de fondo_entry_233); página del editor no cargada)
- **Ficha metodológica:** Crítica clásica: la cita de los artículos de una revista está tan sesgada que el factor de impacto de la revista no representa a sus artículos individuales y no debe usarse para evaluar investigación o investigadores.
- **Uso en el bloque:** DOC-A: fundamento histórico de la regla «el FI de la revista no puntúa la obra».
- **Limitaciones:** Datos de los años noventa; argumentos actualizados en fondo_entry_233.
- **Criterios derivados:** Ninguno aún.
- **Origen:** Alta V4.0 (2026-11-02), segunda tanda de verificación.

#### fondo_entry_223 · Q 87 (A) — San Francisco Declaration on Research Assessment (DORA)

- **Cita normalizada:** San Francisco Declaration on Research Assessment (DORA) (2013). Acordada en la reunión anual de la American Society for Cell Biology (16-12-2012) y publicada el 13-5-2013; texto difundido, entre otros, en Cagan, R. (2013), Disease Models & Mechanisms, 6(4), 869-870.
- **Tipo de fuente:** Declaración institucional internacional
- **Ámbito metodológico:** MB-06 Métricas bibliométricas y cobertura de bases (principal) · secundarias: MB-07
- **Calidad Q:** 87 (A) — Tipo 20/25 · Rigor 12/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 10/10
- **DOI / URL:** https://sfdora.org · https://en.wikipedia.org/wiki/San_Francisco_Declaration_on_Research_Assessment · Cagan (2013): DOI 10.1242/dmm.012955, https://pmc.ncbi.nlm.nih.gov/articles/PMC3701204/
- **Acceso y licencia:** Acceso abierto
- **Estado:** Vigente
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «San Francisco Declaration on Research Assessment DORA read the declaration sfdora.org»; WebFetch: sí, artículo de Wikipedia como índice; PMC devolvió verificación de navegador)
- **Ficha metodológica:** Recomienda no usar el factor de impacto de la revista como sustituto de la calidad de un artículo concreto ni de su autor; evaluar la investigación por su propio contenido. Origen del movimiento de reforma de la evaluación (Project TARA, adhesiones de financiadores y universidades); véase también Alberts (2013), «Impact Factor Distortions», Science 340(6134), 787 (DOI 10.1126/science.1240319).
- **Uso en el bloque:** Documentadores de F7–F8: el factor de impacto de la revista no puntúa por sí mismo el criterio Tipo ni el de Impacto de una obra.
- **Limitaciones:** Declaración de principios; adhesión voluntaria.
- **Criterios derivados:** Ninguno aún.
- **Origen:** Alta V4.0 (2026-11-02), segunda tanda de verificación.

#### fondo_entry_239 · Q 87 (A) — A new approach to the metric of journals' scientific prestige: The SJR indicator

- **Cita normalizada:** González-Pereira, B., Guerrero-Bote, V. P., y Moya-Anegón, F. (2010). A new approach to the metric of journals' scientific prestige: The SJR indicator. Journal of Informetrics, 4(3), 379-391.
- **Tipo de fuente:** Artículo revisado por pares
- **Ámbito metodológico:** MB-06 Métricas bibliométricas y cobertura de bases (principal) · secundarias: —
- **Calidad Q:** 87 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 14/15 · Vigencia 8/10 · Impacto 9/10 · Independencia 9/10 · Acceso 6/10
- **DOI / URL:** DOI: 10.1016/j.joi.2010.03.002 · Verificada en la bibliografía de fondo_entry_233: https://arxiv.org/pdf/1801.08992
- **Acceso y licencia:** Editor por suscripción; valores SJR consultables gratuitamente
- **Estado:** Vigente
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Journal impact factor Wikipedia criticism Seglen 1997 BMJ Garfield history meaning»; WebFetch: sí, página índice; página del editor no cargada)
- **Ficha metodológica:** Define el SJR del grupo español SCImago: prestigio de revista ponderado por el prestigio de las revistas que la citan (tipo PageRank) sobre datos de Scopus.
- **Uso en el bloque:** Documentadores: indicador gratuito y normalizado de prestigio de revista, alternativa al FI.
- **Limitaciones:** Depende de la cobertura de Scopus; métrica de revista, no de artículo.
- **Criterios derivados:** Ninguno aún.
- **Origen:** Alta V4.0 (2026-11-02), segunda tanda de verificación.

#### fondo_entry_243 · Q 87 (A) — h-index: A review focused in its variants, computation and standardization for different scientific fields

- **Cita normalizada:** Alonso, S., et al. (2009). h-index: A review focused in its variants, computation and standardization for different scientific fields. Journal of Informetrics, 3(4), 273-289.
- **Tipo de fuente:** Artículo de revisión revisado por pares
- **Ámbito metodológico:** MB-06 Métricas bibliométricas y cobertura de bases (principal) · secundarias: —
- **Calidad Q:** 87 (A) — Tipo 25/25 · Rigor 15/20 · Autoridad 13/15 · Vigencia 7/10 · Impacto 9/10 · Independencia 10/10 · Acceso 8/10
- **DOI / URL:** DOI: 10.1016/j.joi.2009.04.001 · Copia en E-LIS: http://eprints.rclis.org/13282/1/hIndexReviewAlonsoCabrerizoHerrera-Viedma.pdf · Verificada en: https://en.wikipedia.org/wiki/H-index
- **Acceso y licencia:** Copia de autor en el repositorio E-LIS
- **Estado:** Vigente
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «h-index Wikipedia Hirsch 2005 PNAS "An index to quantify an individual's scientific research output"»; WebFetch: sí, página índice; copia E-LIS no cargada)
- **Ficha metodológica:** Revisión, de un grupo de la Universidad de Granada, de las variantes del índice h (g, hm, contemporáneo, etc.), su cálculo en distintas bases y las propuestas para normalizarlo entre campos.
- **Uso en el bloque:** Documentadores: elegir y declarar la variante de índice si se usa alguna distinta del h.
- **Limitaciones:** Coautores completos no mostrados en el índice (solo «Alonso, S. et al.»).
- **Criterios derivados:** Ninguno aún.
- **Origen:** Alta V4.0 (2026-11-02), segunda tanda de verificación.

#### fondo_entry_230 · Q 86 (A) — Large-scale comparison of bibliographic data sources: Scopus, Web of Science, Dimensions, Crossref, and Microsoft Academic

- **Cita normalizada:** Visser, M., van Eck, N. J., y Waltman, L. (2020). Large-scale comparison of bibliographic data sources: Scopus, Web of Science, Dimensions, Crossref, and Microsoft Academic. arXiv:2005.10732.
- **Tipo de fuente:** Preprint de centro de investigación reconocido (CWTS, Universidad de Leiden)
- **Ámbito metodológico:** MB-06 Métricas bibliométricas y cobertura de bases (principal) · secundarias: MB-02
- **Calidad Q:** 86 (A) — Tipo 18/25 · Rigor 17/20 · Autoridad 14/15 · Vigencia 9/10 · Impacto 8/10 · Independencia 10/10 · Acceso 10/10
- **DOI / URL:** https://arxiv.org/abs/2005.10732 · Verificada en la bibliografía de fondo_entry_224: https://arxiv.org/pdf/2004.14329
- **Acceso y licencia:** Acceso abierto (arXiv)
- **Estado:** Vigente
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Martín-Martín Thelwall Orduna-Malea Delgado López-Cózar 2021 Google Scholar Microsoft Academic Scopus Dimensions Web of Science OpenCitations COCI comparison Scientometrics»; WebFetch: sí, página índice; arXiv de esta obra no cargado)
- **Ficha metodológica:** Comparación a gran escala, documento a documento, de cinco fuentes bibliográficas: solapamiento de cobertura, documentos exclusivos de cada base y calidad de enlace de citas. Complementa la comparación por citas de fondo_entry_224 con una comparación por documentos.
- **Uso en el bloque:** Buscadores: elegir combinaciones de bases que maximicen cobertura sin duplicar.
- **Limitaciones:** Se cita la versión preprint; Microsoft Academic dejó de existir en 2021.
- **Criterios derivados:** Ninguno aún.
- **Origen:** Alta V4.0 (2026-11-02), segunda tanda de verificación.

#### fondo_entry_226 · Q 86 (A) — Suitability of Google Scholar as a source of scientific information and as a source of data for scientific evaluation: Review of the literature

- **Cita normalizada:** Halevi, G., Moed, H., y Bar-Ilan, J. (2017). Suitability of Google Scholar as a source of scientific information and as a source of data for scientific evaluation: Review of the literature. Journal of Informetrics, 11(3), 823-834.
- **Tipo de fuente:** Artículo de revisión revisado por pares
- **Ámbito metodológico:** MB-06 Métricas bibliométricas y cobertura de bases (principal) · secundarias: MB-02
- **Calidad Q:** 86 (A) — Tipo 25/25 · Rigor 15/20 · Autoridad 14/15 · Vigencia 8/10 · Impacto 8/10 · Independencia 10/10 · Acceso 6/10
- **DOI / URL:** DOI: 10.1016/j.joi.2017.06.005 · Verificada en la bibliografía de fondo_entry_224: https://arxiv.org/pdf/2004.14329
- **Acceso y licencia:** Editor por suscripción
- **Estado:** Vigente
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Martín-Martín Thelwall Orduna-Malea Delgado López-Cózar 2021 Google Scholar Microsoft Academic Scopus Dimensions Web of Science OpenCitations COCI comparison Scientometrics»; WebFetch: sí, página índice; página del editor no cargada)
- **Ficha metodológica:** Revisión de la literatura sobre Google Scholar distinguiendo dos usos: como fuente de información científica (amplia cobertura) y como fuente de datos para evaluación (problemas de calidad de metadatos, duplicados y falta de transparencia).
- **Uso en el bloque:** Documentadores: usar Google Scholar para localizar, pero no como única fuente de métricas en las fichas.
- **Limitaciones:** Revisión anterior a cambios recientes de Google Scholar.
- **Criterios derivados:** Ninguno aún.
- **Origen:** Alta V4.0 (2026-11-02), segunda tanda de verificación.

#### fondo_entry_238 · Q 86 (A) — Measuring contextual citation impact of scientific journals

- **Cita normalizada:** Moed, H. F. (2010). Measuring contextual citation impact of scientific journals. Journal of Informetrics, 4, 265-277.
- **Tipo de fuente:** Artículo revisado por pares
- **Ámbito metodológico:** MB-06 Métricas bibliométricas y cobertura de bases (principal) · secundarias: —
- **Calidad Q:** 86 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 14/15 · Vigencia 8/10 · Impacto 8/10 · Independencia 9/10 · Acceso 6/10
- **DOI / URL:** DOI no visto · Verificada en la bibliografía de fondo_entry_233: https://arxiv.org/pdf/1801.08992
- **Acceso y licencia:** Editor por suscripción
- **Estado:** Vigente
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Journal impact factor Wikipedia criticism Seglen 1997 BMJ Garfield history meaning»; WebFetch: sí, página índice; página del editor no cargada)
- **Ficha metodológica:** Propone el SNIP (impacto normalizado por la fuente), que corrige el impacto de una revista según la densidad de citas de su campo; es la alternativa normalizada al FI que publica Scopus.
- **Uso en el bloque:** Documentadores: preferir indicadores normalizados (SNIP, SJR) si se anota el impacto de la revista.
- **Limitaciones:** Indicador ligado a Scopus; el autor colaboró con Elsevier.
- **Criterios derivados:** Ninguno aún.
- **Origen:** Alta V4.0 (2026-11-02), segunda tanda de verificación.

#### fondo_entry_245 · Q 85 (A) — Coercive Citation in Academic Publishing

- **Cita normalizada:** Wilhite, A. W., y Fong, E. A. (2012). Coercive Citation in Academic Publishing. Science, 335(6068), 542-543.
- **Tipo de fuente:** Artículo revisado por pares (encuesta)
- **Ámbito metodológico:** MB-06 Métricas bibliométricas y cobertura de bases (principal) · secundarias: MB-07
- **Calidad Q:** 85 (A) — Tipo 25/25 · Rigor 15/20 · Autoridad 13/15 · Vigencia 8/10 · Impacto 9/10 · Independencia 10/10 · Acceso 5/10
- **DOI / URL:** DOI: 10.1126/science.1212540 · Verificada en: https://en.wikipedia.org/wiki/H-index
- **Acceso y licencia:** Editor por suscripción
- **Estado:** Vigente
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «h-index Wikipedia Hirsch 2005 PNAS "An index to quantify an individual's scientific research output"»; WebFetch: sí, página índice; página del editor no cargada)
- **Ficha metodológica:** Documenta, mediante encuesta a investigadores de economía, sociología, psicología y negocios, la práctica de editores que presionan para añadir citas a su propia revista, una vía de manipulación del factor de impacto.
- **Uso en el bloque:** Evaluador: señal de alerta cuando una revista muestra autocitación anómala.
- **Limitaciones:** Basado en declaraciones de encuestados.
- **Criterios derivados:** Ninguno aún.
- **Origen:** Alta V4.0 (2026-11-02), segunda tanda de verificación.

#### fondo_entry_228 · Q 84 (A) — Dimensions: A competitor to Scopus and the Web of Science?

- **Cita normalizada:** Thelwall, M. (2018). Dimensions: A competitor to Scopus and the Web of Science? Journal of Informetrics, 12(2), 430-435.
- **Tipo de fuente:** Artículo revisado por pares
- **Ámbito metodológico:** MB-06 Métricas bibliométricas y cobertura de bases (principal) · secundarias: MB-02
- **Calidad Q:** 84 (A) — Tipo 25/25 · Rigor 14/20 · Autoridad 14/15 · Vigencia 7/10 · Impacto 8/10 · Independencia 10/10 · Acceso 6/10
- **DOI / URL:** DOI: 10.1016/j.joi.2018.03.006 · Verificada en la bibliografía de fondo_entry_224: https://arxiv.org/pdf/2004.14329
- **Acceso y licencia:** Editor por suscripción
- **Estado:** Vigente
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Martín-Martín Thelwall Orduna-Malea Delgado López-Cózar 2021 Google Scholar Microsoft Academic Scopus Dimensions Web of Science OpenCitations COCI comparison Scientometrics»; WebFetch: sí, página índice; página del editor no cargada)
- **Ficha metodológica:** Primera evaluación de Dimensions como alternativa a Scopus y WoS para recuentos de citas, por un autor de referencia en bibliometría.
- **Uso en el bloque:** Buscadores: criterio para usar Dimensions como base complementaria.
- **Limitaciones:** Evaluación temprana (2018) de una base que ha cambiado desde entonces.
- **Criterios derivados:** Ninguno aún.
- **Origen:** Alta V4.0 (2026-11-02), segunda tanda de verificación.

#### fondo_entry_237 · Q 84 (A) — History of the journal impact factor: Contingencies and consequences

- **Cita normalizada:** Archambault, É., y Larivière, V. (2009). History of the journal impact factor: Contingencies and consequences. Scientometrics, 79(3), 635-649 (la bibliografía de fondo_entry_233 da 639-653).
- **Tipo de fuente:** Artículo revisado por pares
- **Ámbito metodológico:** MB-06 Métricas bibliométricas y cobertura de bases (principal) · secundarias: —
- **Calidad Q:** 84 (A) — Tipo 25/25 · Rigor 15/20 · Autoridad 13/15 · Vigencia 8/10 · Impacto 7/10 · Independencia 10/10 · Acceso 6/10
- **DOI / URL:** DOI: 10.1007/s11192-007-2036-x · Verificada en: https://en.wikipedia.org/wiki/San_Francisco_Declaration_on_Research_Assessment y https://arxiv.org/pdf/1801.08992
- **Acceso y licencia:** Editor por suscripción
- **Estado:** Vigente
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «San Francisco Declaration on Research Assessment DORA read the declaration sfdora.org»; WebFetch: sí, dos páginas índice; página del editor no cargada)
- **Ficha metodológica:** Reconstruye cómo decisiones contingentes (ventana de dos años, definición de documentos citables) se convirtieron en rasgos permanentes del FI y qué sesgos generan entre campos.
- **Uso en el bloque:** Evaluador: razonar por qué el FI no es comparable entre disciplinas.
- **Limitaciones:** Paginación discrepante entre índices; verificar en el DOI.
- **Criterios derivados:** Ninguno aún.
- **Origen:** Alta V4.0 (2026-11-02), segunda tanda de verificación.

#### fondo_entry_240 · Q 83 (A) — A simple proposal for the publication of journal citation distributions

- **Cita normalizada:** Larivière, V., Kiermer, V., MacCallum, C. J., McNutt, M., Patterson, M., Pulverer, B., Swaminathan, S., Taylor, S., y Curry, S. (2016). A simple proposal for the publication of journal citation distributions. bioRxiv, 062109.
- **Tipo de fuente:** Preprint de autores de referencia y editores científicos
- **Ámbito metodológico:** MB-06 Métricas bibliométricas y cobertura de bases (principal) · secundarias: MB-07
- **Calidad Q:** 83 (A) — Tipo 18/25 · Rigor 14/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 8/10 · Independencia 9/10 · Acceso 10/10
- **DOI / URL:** http://www.biorxiv.org/content/early/2016/07/05/062109 · Verificada en la bibliografía de fondo_entry_233: https://arxiv.org/pdf/1801.08992
- **Acceso y licencia:** Acceso abierto
- **Estado:** Vigente
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Journal impact factor Wikipedia criticism Seglen 1997 BMJ Garfield history meaning»; WebFetch: sí, página índice; preprint no cargado)
- **Ficha metodológica:** Propone publicar la distribución completa de citas de cada revista en lugar de un promedio, mostrando que la mayoría de los artículos queda por debajo del FI de su revista.
- **Uso en el bloque:** Evaluador: argumento cuantitativo contra inferir la calidad de un artículo desde el FI de la revista.
- **Limitaciones:** Preprint; firmado por editores de grandes editoriales.
- **Criterios derivados:** Ninguno aún.
- **Origen:** Alta V4.0 (2026-11-02), segunda tanda de verificación.

#### fondo_entry_235 · Q 83 (A) — Citation indexes for science: A new dimension in documentation through association of ideas

- **Cita normalizada:** Garfield, E. (1955). Citation indexes for science: A new dimension in documentation through association of ideas. Science, 122, 108-111.
- **Tipo de fuente:** Artículo revisado por pares (fundacional)
- **Ámbito metodológico:** MB-06 Métricas bibliométricas y cobertura de bases (principal) · secundarias: MB-02
- **Calidad Q:** 83 (A) — Tipo 25/25 · Rigor 12/20 · Autoridad 15/15 · Vigencia 6/10 · Impacto 10/10 · Independencia 10/10 · Acceso 5/10
- **DOI / URL:** DOI no visto · Verificada en la bibliografía de fondo_entry_233: https://arxiv.org/pdf/1801.08992
- **Acceso y licencia:** Editor (acceso no comprobado)
- **Estado:** Vigente
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Journal impact factor Wikipedia criticism Seglen 1997 BMJ Garfield history meaning»; WebFetch: sí, página índice; página del editor no cargada)
- **Ficha metodológica:** Propuesta fundacional del índice de citas: recuperar documentos siguiendo quién cita a quién. Es el origen conceptual tanto de la búsqueda hacia adelante (fondo_criterion_002) como de las métricas de citación.
- **Uso en el bloque:** DOC-A: referencia histórica de la búsqueda por citas.
- **Limitaciones:** Valor histórico; sin datos aplicables hoy.
- **Criterios derivados:** Ninguno aún.
- **Origen:** Alta V4.0 (2026-11-02), segunda tanda de verificación.

#### fondo_entry_242 · Q 82 (A) — Which h-index? A comparison of WoS, Scopus and Google Scholar

- **Cita normalizada:** Bar-Ilan, J. (2008). Which h-index? A comparison of WoS, Scopus and Google Scholar. Scientometrics, 74(2), 257-271 (la página índice lo fecha en 2007, publicación en línea).
- **Tipo de fuente:** Artículo revisado por pares
- **Ámbito metodológico:** MB-06 Métricas bibliométricas y cobertura de bases (principal) · secundarias: —
- **Calidad Q:** 82 (A) — Tipo 25/25 · Rigor 14/20 · Autoridad 13/15 · Vigencia 6/10 · Impacto 9/10 · Independencia 10/10 · Acceso 5/10
- **DOI / URL:** DOI: 10.1007/s11192-008-0216-y · Verificada en: https://en.wikipedia.org/wiki/H-index (bibliografía)
- **Acceso y licencia:** Editor por suscripción
- **Estado:** Vigente
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «h-index Wikipedia Hirsch 2005 PNAS "An index to quantify an individual's scientific research output"»; WebFetch: sí, página índice; página del editor no cargada)
- **Ficha metodológica:** Muestra que el índice h de un mismo investigador cambia sustancialmente según se calcule en WoS, Scopus o Google Scholar: el h no es un dato del autor sino del par autor-base.
- **Uso en el bloque:** Documentadores: anotar siempre la base y la fecha cuando se registre un índice h.
- **Limitaciones:** Datos antiguos; las coberturas han cambiado (ver fondo_entry_224).
- **Criterios derivados:** Ninguno aún.
- **Origen:** Alta V4.0 (2026-11-02), segunda tanda de verificación.

#### fondo_entry_236 · Q 82 (A) — The History and Meaning of the Journal Impact Factor

- **Cita normalizada:** Garfield, E. (2006). The History and Meaning of the Journal Impact Factor. JAMA, 295(1), 90-93.
- **Tipo de fuente:** Comentario en revista revisada de primer nivel
- **Ámbito metodológico:** MB-06 Métricas bibliométricas y cobertura de bases (principal) · secundarias: —
- **Calidad Q:** 82 (A) — Tipo 22/25 · Rigor 12/20 · Autoridad 15/15 · Vigencia 8/10 · Impacto 10/10 · Independencia 7/10 · Acceso 8/10
- **DOI / URL:** PubMed: https://pubmed.ncbi.nlm.nih.gov/16391221/ · Copia en la Universidad de Pensilvania: https://www.med.upenn.edu/mdresearchopps/assets/user-content/Resources/HistoryandMeaningJIF.pdf
- **Acceso y licencia:** Copia gratuita en sitio universitario
- **Estado:** Vigente
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Journal impact factor Wikipedia criticism Seglen 1997 BMJ Garfield history meaning»; WebFetch: sí (copia de UPenn; PubMed sin contenido))
- **Ficha metodológica:** El creador del factor de impacto explica su cálculo (citas del año a lo publicado en los dos años previos, entre artículos y revisiones «citables»), sus distorsiones (citas a cartas y editoriales en el numerador) y admite que usarlo para evaluar individuos es un mal sustituto de las citas reales de cada artículo.
- **Uso en el bloque:** Documentadores: entender qué mide exactamente el FI antes de anotarlo en una ficha.
- **Limitaciones:** Autor fundador del ISI (independencia limitada); visión favorable al indicador.
- **Criterios derivados:** Ninguno aún.
- **Origen:** Alta V4.0 (2026-11-02), segunda tanda de verificación.

#### fondo_entry_247 · Q 80 (A) — Google Scholar as a data source for research assessment

- **Cita normalizada:** Delgado López-Cózar, E., Orduna-Malea, E., y Martín-Martín, A. (2019). Google Scholar as a data source for research assessment. En W. Glänzel, H. F. Moed, U. Schmoch y M. Thelwall (Eds.), Springer Handbook of Science and Technology Indicators. Springer.
- **Tipo de fuente:** Capítulo de manual de referencia
- **Ámbito metodológico:** MB-06 Métricas bibliométricas y cobertura de bases (principal) · secundarias: MB-02
- **Calidad Q:** 80 (A) — Tipo 20/25 · Rigor 15/20 · Autoridad 14/15 · Vigencia 9/10 · Impacto 7/10 · Independencia 10/10 · Acceso 5/10
- **DOI / URL:** DOI no visto · Verificada en la bibliografía de fondo_entry_224: https://arxiv.org/pdf/2004.14329
- **Acceso y licencia:** Manual por suscripción
- **Estado:** Vigente
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Martín-Martín Thelwall Orduna-Malea Delgado López-Cózar 2021 Google Scholar Microsoft Academic Scopus Dimensions Web of Science OpenCitations COCI comparison Scientometrics»; WebFetch: sí, página índice; capítulo no cargado)
- **Ficha metodológica:** Síntesis del grupo español EC3 sobre las ventajas (cobertura) y riesgos (manipulabilidad, falta de transparencia, errores de metadatos) de Google Scholar como fuente de datos para evaluación.
- **Uso en el bloque:** Documentadores: reglas de cautela al tomar métricas de Google Scholar.
- **Limitaciones:** Capítulo de pago; páginas no vistas.
- **Criterios derivados:** Ninguno aún.
- **Origen:** Alta V4.0 (2026-11-02), segunda tanda de verificación.

#### fondo_entry_229 · Q 78 (B) — Dimensions: re-discovering the ecosystem of scientific information

- **Cita normalizada:** Orduña-Malea, E., y Delgado López-Cózar, E. (2018). Dimensions: re-discovering the ecosystem of scientific information. El Profesional de la Información, 27(2), 420-431.
- **Tipo de fuente:** Artículo revisado por pares (revista española)
- **Ámbito metodológico:** MB-06 Métricas bibliométricas y cobertura de bases (principal) · secundarias: MB-02
- **Calidad Q:** 78 (B) — Tipo 22/25 · Rigor 13/20 · Autoridad 13/15 · Vigencia 7/10 · Impacto 6/10 · Independencia 10/10 · Acceso 7/10
- **DOI / URL:** DOI: 10.3145/epi.2018.mar.21 · Verificada en la bibliografía de fondo_entry_224: https://arxiv.org/pdf/2004.14329
- **Acceso y licencia:** Acceso según la editorial (no comprobado)
- **Estado:** Vigente
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Martín-Martín Thelwall Orduna-Malea Delgado López-Cózar 2021 Google Scholar Microsoft Academic Scopus Dimensions Web of Science OpenCitations COCI comparison Scientometrics»; WebFetch: sí, página índice; página del editor no cargada)
- **Ficha metodológica:** Descripción y evaluación de Dimensions desde la perspectiva de un grupo español: contenidos, fuentes de datos y funciones respecto al ecosistema de bases bibliográficas.
- **Uso en el bloque:** Buscadores: referencia en español sobre el uso de Dimensions.
- **Limitaciones:** Análisis descriptivo y temprano.
- **Criterios derivados:** Ninguno aún.
- **Origen:** Alta V4.0 (2026-11-02), segunda tanda de verificación.

#### fondo_entry_232 · Q 75 (B) — Investigating Document Type Discrepancies between OpenAlex and the Web of Science

- **Cita normalizada:** Mongeon, P., Hare, M., Krause, G., Marjoram, R., Riddle, P., Toupin, R., y Wilson, S. (2025). Investigating Document Type Discrepancies between OpenAlex and the Web of Science. Proceedings of the Annual Conference of CAIS / Actes du congrès annuel de l'ACSI.
- **Tipo de fuente:** Comunicación de congreso con actas
- **Ámbito metodológico:** MB-06 Métricas bibliométricas y cobertura de bases (principal) · secundarias: MB-04
- **Calidad Q:** 75 (B) — Tipo 15/25 · Rigor 14/20 · Autoridad 12/15 · Vigencia 10/10 · Impacto 5/10 · Independencia 10/10 · Acceso 9/10
- **DOI / URL:** DOI: 10.29173/cais1943 · https://journals.library.ualberta.ca/ojs.cais-acsi.ca/index.php/cais-asci/article/view/1943
- **Acceso y licencia:** Acceso gratuito (licencia no indicada en la página)
- **Estado:** Vigente
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «OpenAlex coverage compared Scopus Web of Science study 2024 2025 Priem Piwowar Orr "OpenAlex: A fully-open index"»; WebFetch: sí)
- **Ficha metodológica:** Más del 4 % de las publicaciones presentes en ambas bases parece mal clasificado como artículo de investigación o revisión, y el 97 % de esos errores está en OpenAlex. Advierte de que filtrar por tipo de documento en OpenAlex puede introducir sesgos.
- **Uso en el bloque:** Buscadores: verificar manualmente el tipo de documento recuperado de OpenAlex antes de asignar la puntuación Tipo de la rúbrica.
- **Limitaciones:** Comunicación breve; solo compara con WoS.
- **Criterios derivados:** Ninguno aún.
- **Origen:** Alta V4.0 (2026-11-02), segunda tanda de verificación.

## MB-07 Evaluación de credibilidad de fuentes

#### fondo_entry_254 · Q 94 (A) — The spread of true and false news online

- **Cita normalizada:** Vosoughi, S., Roy, D., y Aral, S. (2018). The spread of true and false news online. Science, 359(6380).
- **Tipo de fuente:** Artículo revisado por pares
- **Ámbito metodológico:** MB-07 Evaluación de credibilidad de fuentes (principal) · secundarias: —
- **Calidad Q:** 94 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 14/15 · Vigencia 9/10 · Impacto 10/10 · Independencia 10/10 · Acceso 8/10
- **DOI / URL:** https://www.media.mit.edu/publications/the-spread-of-true-and-false-news-online/
- **Acceso y licencia:** Ficha y enlace en MIT Media Lab; artículo del editor por suscripción
- **Estado:** Vigente
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Fake news Wikipedia Vosoughi Roy Aral 2018 "spread of true and false news online" Lazer "science of fake news" Pennycook Rand»; WebFetch: sí)
- **Ficha metodológica:** Analiza unas 126.000 noticias verificadas compartidas en Twitter entre 2006 y 2017 (clasificadas por seis organizaciones de verificación con un 95–98 % de acuerdo): las falsas se difunden más lejos, más rápido y más ampliamente que las verdaderas, sobre todo en política, por ser más novedosas; los bots difunden ambas por igual.
- **Uso en el bloque:** Buscadores de F9: la viralidad de una afirmación en redes no es indicio de veracidad; exigir fuente primaria (TF-12).
- **Limitaciones:** Una plataforma y periodo; páginas y DOI no mostrados en la ficha leída.
- **Criterios derivados:** Ninguno aún.
- **Origen:** Alta V4.0 (2026-11-02), segunda tanda de verificación.

#### fondo_entry_258 · Q 92 (A) — Conflict of Interest and the Credibility of Underwriter Analyst Recommendations

- **Cita normalizada:** Michaely, R., y Womack, K. L. (1999). Conflict of Interest and the Credibility of Underwriter Analyst Recommendations. Review of Financial Studies, 12(4), 653-686.
- **Tipo de fuente:** Artículo revisado por pares
- **Ámbito metodológico:** MB-07 Evaluación de credibilidad de fuentes (principal) · secundarias: —
- **Calidad Q:** 92 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 8/10 · Impacto 10/10 · Independencia 10/10 · Acceso 7/10
- **DOI / URL:** https://ideas.repec.org/a/oup/rfinst/v12y1999i4p653-86.html · Copia docente: https://people.bath.ac.uk/mnsrf/Teaching%202011/IB/Literature/L6-analysts/Michaely-Womack.pdf
- **Acceso y licencia:** Revista por suscripción; copia en sitio universitario
- **Estado:** Vigente
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Michaely Womack 1999 "Conflict of Interest and the Credibility of Underwriter Analyst Recommendations" Review of Financial Studies»; WebFetch: sí (IDEAS/RePEc))
- **Ficha metodológica:** Las recomendaciones de compra de analistas del banco colocador de una OPV rinden peor que las de analistas no afiliados antes, durante y después de la recomendación; el mercado no descuenta del todo el sesgo. Evidencia canónica de que el conflicto de interés del emisor degrada la credibilidad de las recomendaciones financieras.
- **Uso en el bloque:** Documentadores de F9 y Evaluador: puntuar Independencia a la baja en recomendaciones de analistas con relación de negocio con el emisor.
- **Limitaciones:** Mercado estadounidense de los años noventa, antes de la regulación posterior a 2002.
- **Criterios derivados:** Ninguno aún.
- **Origen:** Alta V4.0 (2026-11-02), segunda tanda de verificación.

#### fondo_entry_248 · Q 90 (A) — Lateral Reading on the Open Internet: A District-Wide Field Study in High School Government Classes

- **Cita normalizada:** Wineburg, S., Breakstone, J., McGrew, S., Smith, M. D., y Ortega, T. (2022; versión en línea 2021). Lateral Reading on the Open Internet: A District-Wide Field Study in High School Government Classes. Journal of Educational Psychology.
- **Tipo de fuente:** Artículo revisado por pares (experimento de campo)
- **Ámbito metodológico:** MB-07 Evaluación de credibilidad de fuentes (principal) · secundarias: —
- **Calidad Q:** 90 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 8/10 · Independencia 9/10 · Acceso 7/10
- **DOI / URL:** https://cor.inquirygroup.org/research/lateral-reading-on-the-open-internet · SSRN: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3936112 · Material suplementario APA: https://supp.apa.org/psycarticles/supplemental/edu0000740/EDU_2020_0630_Supplemental_Materials.pdf · https://mediawell.ssrc.org/?p=510382
- **Acceso y licencia:** Revista por suscripción; versión en SSRN
- **Estado:** Vigente
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Wineburg Breakstone McGrew Smith Ortega 2022 "Lateral reading on the open Internet" Journal of Educational Psychology field study»; WebFetch: sí (COR, MediaWell y suplemento APA))
- **Ficha metodológica:** Experimento aleatorizado por grupos en un distrito escolar urbano: seis lecciones de una hora en tres meses sobre estrategias de verificadores (lectura lateral); los grupos de tratamiento (n = 271) mejoran significativamente más que los de control (n = 228) al juzgar la credibilidad de contenido digital. Prueba que la lectura lateral se puede enseñar y medir.
- **Uso en el bloque:** DOC-A: evidencia experimental que respalda el paso de lectura lateral del procedimiento «Uso por todos los bloques».
- **Limitaciones:** Volumen, páginas y DOI no confirmados en las páginas leídas; población de secundaria.
- **Criterios derivados:** Ninguno aún.
- **Origen:** Alta V4.0 (2026-11-02), segunda tanda de verificación.

#### fondo_entry_018 · Q 90 (A) — Lateral Reading and the Nature of Expertise: Reading Less and Learning More When Evaluating Digital Information

- **Cita normalizada:** Wineburg, S., y McGrew, S. (2019). Lateral Reading and the Nature of Expertise: Reading Less and Learning More When Evaluating Digital Information. Teachers College Record, 121(11). Versión previa: Stanford History Education Group Working Paper (2017), Stanford Digital Repository.
- **Tipo de fuente:** Artículo revisado por pares
- **Ámbito metodológico:** MB-07 Evaluación de credibilidad de fuentes (principal) · secundarias: MB-05
- **Calidad Q:** 90 (A) — Tipo 23/25 · Rigor 16/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 8/10
- **DOI / URL:** DOI: 10.1177/016146811912101102 · https://journals.sagepub.com/doi/10.1177/016146811912101102 · Versión abierta: https://purl.stanford.edu/yk133ht8603
- **Acceso y licencia:** Versión de la revista por suscripción (SAGE); versión de trabajo abierta en el Stanford Digital Repository (CC BY-NC-ND 3.0)
- **Estado:** Vigente
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Wineburg McGrew 2019 "Lateral Reading and the Nature of Expertise" Teachers College Record»; WebFetch: sí, repositorio de Stanford y ficha de COR)
- **Ficha metodológica:** Compara verificadores profesionales, historiadores y estudiantes universitarios evaluando sitios web: los verificadores salen de la página para averiguar quién está detrás («lectura lateral») y leen menos pero aciertan más, mientras que los demás juzgan por la apariencia del sitio. Base del control de credibilidad de fuentes de opinión.
- **Uso en el bloque:** Documentadores de F9 y Evaluador: paso de lectura lateral obligatorio antes de dar de alta o confiar en una fuente de opinión (paso 5 del procedimiento «Uso por todos los bloques»).
- **Limitaciones:** Muestra pequeña y cualitativa (estudio de tareas); dominio de temas sociales, no financieros. La versión del repositorio figura como 2018 (working paper); la versión de revista es de 2019.
- **Criterios derivados:** Ninguno aún.
- **Origen:** Semilla V3.0 (2026-11-01) confirmada en V4.0 (2026-11-02): cita, DOI y versión abierta verificados.

#### fondo_entry_261 · Q 90 (A) — Reglamento Delegado (UE) 2016/958 sobre la presentación objetiva de recomendaciones de inversión y la comunicación de conflictos de interés

- **Cita normalizada:** Comisión Europea (2016). Reglamento Delegado (UE) 2016/958 de la Comisión, de 9 de marzo de 2016, que completa el Reglamento (UE) n.º 596/2014 en lo que respecta a las normas técnicas de regulación relativas a las disposiciones técnicas para la presentación objetiva de recomendaciones de inversión u otras informaciones y para la comunicación de intereses particulares o indicaciones de conflictos de interés. Publicado el 17-6-2016; en vigor desde el 3-7-2016.
- **Tipo de fuente:** Norma oficial de la UE
- **Ámbito metodológico:** MB-07 Evaluación de credibilidad de fuentes (principal) · secundarias: —
- **Calidad Q:** 90 (A) — Tipo 25/25 · Rigor 12/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 8/10 · Independencia 10/10 · Acceso 10/10
- **DOI / URL:** https://eur-lex.europa.eu/eli/reg_del/2016/958/oj/eng · Texto consolidado del Reino Unido (capítulos II y III): https://www.legislation.gov.uk/eur/2016/958/chapter/II
- **Acceso y licencia:** Acceso abierto (EUR-Lex)
- **Estado:** Vigente
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Commission Delegated Regulation (EU) 2016/958 investment recommendations objective presentation disclosure conflicts of interest EUR-Lex»; WebFetch: sí (EUR-Lex: metadatos; legislation.gov.uk: articulado))
- **Ficha metodológica:** Obliga a quien elabora recomendaciones de inversión a identificarse, separar hechos de opiniones, citar fuentes y advertir de dudas sobre su fiabilidad, explicar supuestos, métodos de valoración y horizonte, publicar el historial de recomendaciones de 12 meses y revelar conflictos (posiciones netas > 0,5 % del capital del emisor, participaciones > 5 %, relaciones de colocación o creación de mercado). Es una lista oficial de lo que una recomendación financiera creíble debe declarar.
- **Uso en el bloque:** Documentadores de F9 y Evaluador: lista de comprobación de transparencia y conflictos para fuentes de análisis y recomendaciones (TF-04 y fuentes de opinión).
- **Limitaciones:** Articulado leído en la versión británica (marcada como derogada en el Reino Unido); verificar el texto de la UE vigente en EUR-Lex.
- **Criterios derivados:** Ninguno aún.
- **Origen:** Alta V4.0 (2026-11-02), segunda tanda de verificación.

#### fondo_entry_255 · Q 89 (A) — The science of fake news

- **Cita normalizada:** Lazer, D. M. J., Baum, M. A., Benkler, Y., Berinsky, A. J., Greenhill, K. M., Menczer, F., Metzger, M. J., Nyhan, B., Pennycook, G., Rothschild, D., Schudson, M., Sloman, S. A., Sunstein, C. R., Thorson, E. A., Watts, D. J., y Zittrain, J. L. (2018). The science of fake news. Science, 359(6380), 1094-1096.
- **Tipo de fuente:** Artículo revisado (Policy Forum, Science)
- **Ámbito metodológico:** MB-07 Evaluación de credibilidad de fuentes (principal) · secundarias: —
- **Calidad Q:** 89 (A) — Tipo 23/25 · Rigor 13/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 10/10 · Independencia 10/10 · Acceso 9/10
- **DOI / URL:** DOI: 10.1126/science.aao2998 · Manuscrito aceptado: https://arxiv.org/pdf/2307.07903 · https://mbaum.scholars.harvard.edu/publications/science-fake-news
- **Acceso y licencia:** Manuscrito aceptado de acceso abierto (arXiv)
- **Estado:** Vigente
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Fake news Wikipedia Vosoughi Roy Aral 2018 "spread of true and false news online" Lazer "science of fake news" Pennycook Rand»; WebFetch: sí)
- **Ficha metodológica:** Síntesis interdisciplinar sobre la vulnerabilidad a las noticias falsas y su difusión, atribuida a la erosión de los contrapesos institucionales; propone dos líneas de intervención (capacitar a las personas para evaluar fuentes y cambios estructurales en plataformas).
- **Uso en el bloque:** DOC-A: encuadre general de por qué el bloque debe verificar la fuente y no solo el contenido.
- **Limitaciones:** Artículo de posición breve, centrado en EE. UU.
- **Criterios derivados:** Ninguno aún.
- **Origen:** Alta V4.0 (2026-11-02), segunda tanda de verificación.

#### fondo_entry_256 · Q 89 (A) — Social Media and Fake News in the 2016 Election

- **Cita normalizada:** Allcott, H., y Gentzkow, M. (2017). Social Media and Fake News in the 2016 Election. Journal of Economic Perspectives, 31, 211-236.
- **Tipo de fuente:** Artículo revisado por pares
- **Ámbito metodológico:** MB-07 Evaluación de credibilidad de fuentes (principal) · secundarias: —
- **Calidad Q:** 89 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 14/15 · Vigencia 8/10 · Impacto 10/10 · Independencia 10/10 · Acceso 6/10
- **DOI / URL:** DOI no visto · Verificada en la bibliografía de fondo_entry_255: https://arxiv.org/pdf/2307.07903
- **Acceso y licencia:** Revista de la AEA (acceso no comprobado)
- **Estado:** Vigente
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Fake news Wikipedia Vosoughi Roy Aral 2018 "spread of true and false news online" Lazer "science of fake news" Pennycook Rand»; WebFetch: sí, página índice; página del editor no cargada)
- **Ficha metodológica:** Análisis económico de la producción y el consumo de noticias falsas en redes durante la campaña de 2016: incentivos de los productores, exposición y recuerdo de los lectores.
- **Uso en el bloque:** Evaluador: modelo económico de por qué existen fuentes con incentivos para publicar falsedades.
- **Limitaciones:** Contexto electoral estadounidense; número de la revista no visto.
- **Criterios derivados:** Ninguno aún.
- **Origen:** Alta V4.0 (2026-11-02), segunda tanda de verificación.

#### fondo_entry_259 · Q 89 (A) — Do Ads Influence Editors? Advertising and Bias in the Financial Media

- **Cita normalizada:** Reuter, J., y Zitzewitz, E. (2006). Do Ads Influence Editors? Advertising and Bias in the Financial Media. Quarterly Journal of Economics, 121(1), 197-227.
- **Tipo de fuente:** Artículo revisado por pares
- **Ámbito metodológico:** MB-07 Evaluación de credibilidad de fuentes (principal) · secundarias: —
- **Calidad Q:** 89 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 14/15 · Vigencia 8/10 · Impacto 9/10 · Independencia 10/10 · Acceso 6/10
- **DOI / URL:** DOI: 10.1093/qje/121.1.197 · https://ideas.repec.org/a/oup/qjecon/v121y2006i1p197-227..html · Versión del autor: https://www.jonreuter.com/research/ads.pdf
- **Acceso y licencia:** Revista por suscripción; versión de autor gratuita
- **Estado:** Vigente
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Reuter Zitzewitz 2006 "Do Ads Influence Editors? Advertising and Bias in the Financial Media" Quarterly Journal of Economics»; WebFetch: sí (IDEAS/RePEc))
- **Ficha metodológica:** Las recomendaciones de fondos de inversión en tres revistas de finanzas personales se correlacionan con la publicidad pasada de las gestoras (no así en dos diarios nacionales); las menciones positivas aumentan las suscripciones pero no predicen rentabilidades. Mide el sesgo comercial de la prensa financiera.
- **Uso en el bloque:** Documentadores de F9: considerar la dependencia publicitaria del medio al puntuar Independencia de prensa financiera.
- **Limitaciones:** Prensa estadounidense y fondos de inversión; coste del sesgo para el lector estimado como pequeño.
- **Criterios derivados:** Ninguno aún.
- **Origen:** Alta V4.0 (2026-11-02), segunda tanda de verificación.

#### fondo_entry_260 · Q 88 (A) — Social Media and Financial News Manipulation

- **Cita normalizada:** Kogan, S., Moskowitz, T. J., y Niessner, M. (2023). Social Media and Financial News Manipulation. Review of Finance, 27(4), 1229-1268.
- **Tipo de fuente:** Artículo revisado por pares
- **Ámbito metodológico:** MB-07 Evaluación de credibilidad de fuentes (principal) · secundarias: —
- **Calidad Q:** 88 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 7/10 · Independencia 10/10 · Acceso 6/10
- **DOI / URL:** DOI: 10.1093/rof/rfac058 · https://ideas.repec.org/a/oup/revfin/v27y2023i4p1229-1268..html
- **Acceso y licencia:** Revista por suscripción
- **Estado:** Vigente
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Kogan Moskowitz Niessner "Social Media and Financial News Manipulation" fake news Seeking Alpha Review of Finance»; WebFetch: sí (IDEAS/RePEc))
- **Ficha metodológica:** A partir de una investigación encubierta de la SEC sobre artículos financieros fraudulentos en plataformas sociales: las noticias falsas elevaron la negociación minorista y los precios, y tras destaparse el fraude cayó el volumen minorista ante todas las noticias de esas plataformas (−23,5 % en pequeñas empresas). Cuantifica el coste de la desinformación financiera y su efecto contagio sobre la credibilidad de toda la plataforma.
- **Uso en el bloque:** Documentadores de F9 (TF-12, redes y blogs financieros): tratar con cautela especial los artículos de plataformas abiertas sobre pequeñas empresas.
- **Limitaciones:** Un episodio de manipulación en EE. UU.
- **Criterios derivados:** Ninguno aún.
- **Origen:** Alta V4.0 (2026-11-02), segunda tanda de verificación.

#### fondo_entry_249 · Q 86 (A) — Lateral reading: College students learn to critically evaluate internet sources in an online course

- **Cita normalizada:** Breakstone, J., Smith, M., Connors, P., Ortega, T., Kerr, D., y Wineburg, S. (2021). Lateral reading: College students learn to critically evaluate internet sources in an online course. Harvard Kennedy School Misinformation Review, 2(1).
- **Tipo de fuente:** Artículo revisado por pares
- **Ámbito metodológico:** MB-07 Evaluación de credibilidad de fuentes (principal) · secundarias: —
- **Calidad Q:** 86 (A) — Tipo 22/25 · Rigor 14/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 7/10 · Independencia 9/10 · Acceso 10/10
- **DOI / URL:** DOI: 10.37016/mr-2020-56 · https://doaj.org/article/e106205a559240e6a672bc362d26c5e3
- **Acceso y licencia:** Acceso abierto (revista indexada en DOAJ)
- **Estado:** Vigente
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Wineburg Breakstone McGrew Smith Ortega 2022 "Lateral reading on the open Internet" Journal of Educational Psychology field study»; WebFetch: sí (DOAJ))
- **Ficha metodológica:** En un curso universitario asíncrono, la instrucción basada en métodos de verificadores mejora la evaluación de fuentes en línea; la lectura lateral es la técnica más importante y su uso aumenta tras la intervención. Extiende fondo_entry_248 a adultos y formato en línea.
- **Uso en el bloque:** DOC-A y Evaluador: base para formar a los agentes humanos y diseñar las instrucciones de verificación de credibilidad.
- **Limitaciones:** Un solo curso; sin grupo de control aleatorizado según la página leída.
- **Criterios derivados:** Ninguno aún.
- **Origen:** Alta V4.0 (2026-11-02), segunda tanda de verificación.

#### fondo_entry_262 · Q 85 (A) — Reglamento (UE) n.º 596/2014 sobre abuso de mercado, artículo 20: recomendaciones de inversión y estadísticas

- **Cita normalizada:** Parlamento Europeo y Consejo (2014). Reglamento (UE) n.º 596/2014 sobre el abuso de mercado, artículo 20 «Recomendaciones de inversión y estadísticas». Consultado en la versión retenida del Reino Unido.
- **Tipo de fuente:** Norma oficial (texto legal de base)
- **Ámbito metodológico:** MB-07 Evaluación de credibilidad de fuentes (principal) · secundarias: —
- **Calidad Q:** 85 (A) — Tipo 25/25 · Rigor 10/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 8/10 · Independencia 10/10 · Acceso 8/10
- **DOI / URL:** https://www.legislation.gov.uk/eur/2014/596/article/20
- **Acceso y licencia:** Acceso abierto
- **Estado:** Vigente
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Commission Delegated Regulation (EU) 2016/958 investment recommendations objective presentation disclosure conflicts of interest EUR-Lex»; WebFetch: sí)
- **Ficha metodológica:** Base legal de fondo_entry_261: quien produce o difunde recomendaciones de inversión debe presentarlas con objetividad razonable y revelar sus intereses o conflictos; las instituciones públicas que publican estadísticas o previsiones con impacto en los mercados deben hacerlo de forma objetiva y transparente; los periodistas sujetos a regulación o autorregulación equivalente quedan exentos de las normas técnicas.
- **Uso en el bloque:** Documentadores de F9: distinguir fuentes sujetas a la obligación (analistas, «expertos») de periodistas con régimen propio al puntuar transparencia y conflictos.
- **Limitaciones:** Leído en la versión retenida del Reino Unido (marcada como derogada allí); la versión de la UE sigue en vigor y debe consultarse en EUR-Lex.
- **Criterios derivados:** Ninguno aún.
- **Origen:** Alta V4.0 (2026-11-02), segunda tanda de verificación.

#### fondo_entry_252 · Q 84 (A) — Information Disorder: Toward an interdisciplinary framework for research and policy making

- **Cita normalizada:** Wardle, C., y Derakhshan, H. (2017, septiembre). Information Disorder: Toward an interdisciplinary framework for research and policy making. Consejo de Europa.
- **Tipo de fuente:** Informe técnico de organismo internacional
- **Ámbito metodológico:** MB-07 Evaluación de credibilidad de fuentes (principal) · secundarias: —
- **Calidad Q:** 84 (A) — Tipo 15/25 · Rigor 15/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 10/10
- **DOI / URL:** https://www.rcmediafreedom.eu/Resources/Reports-and-papers/Information-disorder-Toward-an-interdisciplinary-framework-for-research-and-policy-making · https://shorensteincenter.org/?p=10550 · PDF del Consejo de Europa (enlazado desde la ficha del RCMF): https://rm.coe.int/information-disorder-report-november-2017/1680764666
- **Acceso y licencia:** Acceso gratuito
- **Estado:** Vigente
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Wardle Derakhshan 2017 "Information Disorder: Toward an interdisciplinary framework" Council of Europe report pdf»; WebFetch: sí (ficha del Resource Centre on Media Freedom in Europe))
- **Ficha metodológica:** Distingue mis-información (falsa sin intención de dañar), des-información (falsa y deliberada) y mal-información (veraz usada para dañar), y analiza cada caso por agente, mensaje e intérprete en las fases de creación, producción y distribución. Proporciona el vocabulario europeo de referencia para clasificar contenido problemático.
- **Uso en el bloque:** Documentadores de F9 y Evaluador: tipificar las incidencias de fuentes de opinión y redes en el registro de bajas.
- **Limitaciones:** Marco conceptual, sin medición empírica.
- **Criterios derivados:** Ninguno aún.
- **Origen:** Alta V4.0 (2026-11-02), segunda tanda de verificación.

#### fondo_entry_253 · Q 82 (A) — The Debunking Handbook 2020

- **Cita normalizada:** Lewandowsky, S., Cook, J., Ecker, U. K. H., et al. (2020, 14 de octubre). The Debunking Handbook 2020. Publicado y difundido por, entre otros, el Climate Social Science Network (Brown University).
- **Tipo de fuente:** Guía de consenso de expertos
- **Ámbito metodológico:** MB-07 Evaluación de credibilidad de fuentes (principal) · secundarias: —
- **Calidad Q:** 82 (A) — Tipo 15/25 · Rigor 16/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 9/10 · Acceso 8/10
- **DOI / URL:** https://cssn.org/the-debunking-handbook-2020-a-consensus-based-handbook-of-recommendations-for-correcting-or-preventing-misinformation/ · https://open.bu.edu/handle/2144/43031
- **Acceso y licencia:** Gratuito (licencia no indicada en la página leída)
- **Estado:** Vigente
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «"The Debunking Handbook 2020" Lewandowsky Cook Ecker»; WebFetch: sí (CSSN; el repositorio de BU no cargó))
- **Ficha metodológica:** Manual de recomendaciones consensuadas por un amplio grupo de investigadores para corregir o prevenir la desinformación; sustituye al manual de 2011 y todos los autores suscriben todas sus recomendaciones.
- **Uso en el bloque:** Evaluador y AC de comunicación: cómo registrar y comunicar una corrección cuando una fuente del bloque difundió información falsa.
- **Limitaciones:** Orientado a comunicación pública; contenido detallado no leído en esta verificación.
- **Criterios derivados:** Ninguno aún.
- **Origen:** Alta V4.0 (2026-11-02), segunda tanda de verificación.

#### fondo_entry_257 · Q 76 (B) — IFCN Code of Principles

- **Cita normalizada:** International Fact-Checking Network (IFCN), Poynter Institute (en vigor). Code of Principles: the commitments.
- **Tipo de fuente:** Código deontológico profesional
- **Ámbito metodológico:** MB-07 Evaluación de credibilidad de fuentes (principal) · secundarias: —
- **Calidad Q:** 76 (B) — Tipo 15/25 · Rigor 12/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 8/10 · Independencia 7/10 · Acceso 10/10
- **DOI / URL:** https://ifcncodeofprinciples.poynter.org/the-commitments · Firmantes: https://ifcncodeofprinciples.poynter.org/signatories
- **Acceso y licencia:** Acceso gratuito
- **Estado:** Vigente
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «IFCN Code of Principles International Fact-Checking Network Poynter signatories nonpartisanship transparency of sources methodology»; WebFetch: sí)
- **Ficha metodológica:** Cinco compromisos de las organizaciones de verificación: imparcialidad, transparencia de fuentes, transparencia de financiación y organización, transparencia de método y política de correcciones abierta. Sirve de lista para juzgar si un verificador (o cualquier fuente de opinión) es fiable.
- **Uso en el bloque:** Documentadores de F9: preferir verificadores firmantes del código; usar los cinco compromisos como lista de comprobación de transparencia de fuentes de opinión.
- **Limitaciones:** Autorregulación; la firma no garantiza la calidad de cada verificación; año de creación no indicado en la página.
- **Criterios derivados:** Ninguno aún.
- **Origen:** Alta V4.0 (2026-11-02), segunda tanda de verificación.

#### fondo_entry_250 · Q 73 (B) — Evaluating Information: The Cornerstone of Civic Online Reasoning

- **Cita normalizada:** Wineburg, S., McGrew, S., Breakstone, J., y Ortega, T. (2016, noviembre). Evaluating Information: The Cornerstone of Civic Online Reasoning. Executive Summary, Stanford History Education Group.
- **Tipo de fuente:** Informe técnico (resumen ejecutivo)
- **Ámbito metodológico:** MB-07 Evaluación de credibilidad de fuentes (principal) · secundarias: —
- **Calidad Q:** 73 (B) — Tipo 12/25 · Rigor 12/20 · Autoridad 14/15 · Vigencia 8/10 · Impacto 9/10 · Independencia 10/10 · Acceso 8/10
- **DOI / URL:** https://purl.stanford.edu/fv751yt5934 · Verificada en: https://inquirygroup.org/publications
- **Acceso y licencia:** Acceso abierto (Stanford Digital Repository)
- **Estado:** Vigente
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Wineburg Breakstone McGrew Smith Ortega 2022 "Lateral reading on the open Internet" Journal of Educational Psychology field study»; WebFetch: sí, página índice (publicaciones del grupo); repositorio no cargado)
- **Ficha metodológica:** Informe del estudio de 2016 con casi 8.000 estudiantes (cifra confirmada en fondo_entry_207) que evidenció la dificultad generalizada para distinguir contenido patrocinado, fuentes interesadas y noticias fiables; punto de partida del programa de razonamiento cívico en línea.
- **Uso en el bloque:** DOC-A: evidencia descriptiva de los errores típicos de evaluación de fuentes (publicidad nativa, fuentes con intereses ocultos).
- **Limitaciones:** Resumen ejecutivo sin revisión por pares.
- **Criterios derivados:** Ninguno aún.
- **Origen:** Alta V4.0 (2026-11-02), segunda tanda de verificación.

#### fondo_entry_251 · Q 67 (B) — Web Literacy for Student Fact-Checkers

- **Cita normalizada:** Caulfield, M. (2017). Web Literacy for Student Fact-Checkers. Autoedición (Pressbooks).
- **Tipo de fuente:** Manual divulgativo especializado (libro electrónico)
- **Ámbito metodológico:** MB-07 Evaluación de credibilidad de fuentes (principal) · secundarias: —
- **Calidad Q:** 67 (B) — Tipo 8/25 · Rigor 9/20 · Autoridad 13/15 · Vigencia 10/10 · Impacto 8/10 · Independencia 10/10 · Acceso 9/10
- **DOI / URL:** https://pressbooks.pub/webliteracy/ · Verificada en: https://libguides.princeton.edu/medialiteracy/lateralreading y https://libguides.eku.edu/sift/learn-more
- **Acceso y licencia:** Gratuito en línea
- **Estado:** Vigente
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Wineburg McGrew 2019 "Lateral Reading and the Nature of Expertise" Teachers College Record»; WebFetch: sí, guías de Princeton y EKU como índice; libro no cargado)
- **Ficha metodológica:** Manual práctico de verificación web (comprobar trabajo previo de verificadores, ir a la fuente, leer lateralmente, volver a empezar) con técnicas concretas de búsqueda inversa de imágenes, WHOIS y Wikipedia; es la base de la que deriva SIFT (fondo_entry_019).
- **Uso en el bloque:** Buscadores y Documentadores de F9: técnicas concretas de verificación de páginas, imágenes y cuentas.
- **Limitaciones:** Autoeditado, sin revisión por pares; algunas herramientas citadas pueden haber cambiado.
- **Criterios derivados:** Ninguno aún.
- **Origen:** Alta V4.0 (2026-11-02), segunda tanda de verificación.

#### fondo_entry_019 · Q 66 (B) — SIFT (The Four Moves)

- **Cita normalizada:** Caulfield, M. (2019, 19 de junio). SIFT (The Four Moves). Hapgood (blog). Desarrollo de Web Literacy for Student Fact-Checkers (2017).
- **Tipo de fuente:** Divulgación especializada (guía práctica)
- **Ámbito metodológico:** MB-07 Evaluación de credibilidad de fuentes (principal) · secundarias: —
- **Calidad Q:** 66 (B) — Tipo 8/25 · Rigor 9/20 · Autoridad 12/15 · Vigencia 10/10 · Impacto 8/10 · Independencia 10/10 · Acceso 9/10
- **DOI / URL:** https://hapgood.us/2019/06/19/sift-the-four-moves/
- **Acceso y licencia:** Acceso abierto (CC BY 4.0)
- **Estado:** Vigente
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «"SIFT (The Four Moves)" Mike Caulfield Hapgood»; WebFetch: sí)
- **Ficha metodológica:** Rutina en cuatro movimientos: detenerse (Stop), investigar la fuente (Investigate the source), buscar mejor cobertura y el consenso experto (Find better coverage) y rastrear afirmaciones, citas y medios hasta su contexto original (Trace). Operativiza la lectura lateral para el filtrado rápido de noticias y redes.
- **Uso en el bloque:** Buscadores y Documentadores de F9: filtro rápido de noticias, redes y fuentes de opinión (TF-03, TF-12) antes de registrar una afirmación.
- **Limitaciones:** Entrada de blog, sin validación empírica propia (se apoya en fondo_entry_018); página modificada en 2021.
- **Criterios derivados:** Ninguno aún.
- **Origen:** Semilla V3.0 (2026-11-01) confirmada en V4.0 (2026-11-02).

#### fondo_entry_206 · Q 66 (B) — What Does Bad Information Look Like? Using the CRAAP Test for Evaluating Substandard Resources

- **Cita normalizada:** Lewis, A. B. (2018). What Does Bad Information Look Like? Using the CRAAP Test for Evaluating Substandard Resources. Issues in Science and Technology Librarianship.
- **Tipo de fuente:** Artículo revisado por pares (práctica docente)
- **Ámbito metodológico:** MB-07 Evaluación de credibilidad de fuentes (principal) · secundarias: —
- **Calidad Q:** 66 (B) — Tipo 18/25 · Rigor 8/20 · Autoridad 9/15 · Vigencia 7/10 · Impacto 4/10 · Independencia 10/10 · Acceso 10/10
- **DOI / URL:** DOI: 10.29173/istl1724 (los resultados de búsqueda muestran además doi.org/10.5062/f41n7zc4) · https://journals.library.ualberta.ca/istl/index.php/istl/article/view/1724
- **Acceso y licencia:** Acceso abierto (CC BY 4.0)
- **Estado:** Vigente
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Blakeslee 2004 "The CRAAP Test" LOEX Quarterly vol 31 iss 3»; WebFetch: sí)
- **Ficha metodológica:** Aplica la lista CRAAP a fuentes deliberadamente deficientes: los evaluadores saben reconocer fuentes sólidas y nombrar sesgo o autoridad, pero fallan al identificar qué hace poco fiable una fuente. Complementa a fondo_entry_020 mostrando cómo usar la lista para detectar fallos, no solo para aprobar fuentes.
- **Uso en el bloque:** Evaluador y Documentadores: casos de contraste para calibrar el rechazo de fuentes deficientes.
- **Limitaciones:** Experiencia docente en un curso, sin diseño experimental; autora y editor del artículo no confirmados en la página leída más allá del titular de derechos.
- **Criterios derivados:** Ninguno aún.
- **Origen:** Alta V4.0 (2026-11-02), verificada por búsqueda web y lectura de la página.

#### fondo_entry_207 · Q 60 (C) — Stanford History Education Group: written evidence (DAD0080)

- **Cita normalizada:** Wineburg, S. (c. 2019). Stanford History Education Group – written evidence (DAD0080). Parlamento del Reino Unido, evidencia escrita a comité.
- **Tipo de fuente:** Declaración experta ante órgano parlamentario (literatura gris)
- **Ámbito metodológico:** MB-07 Evaluación de credibilidad de fuentes (principal) · secundarias: —
- **Calidad Q:** 60 (C) — Tipo 8/25 · Rigor 8/20 · Autoridad 13/15 · Vigencia 9/10 · Impacto 5/10 · Independencia 8/10 · Acceso 9/10
- **DOI / URL:** https://committees.parliament.uk/writtenevidence/448/html/
- **Acceso y licencia:** Acceso gratuito (Parlamento del Reino Unido)
- **Estado:** Vigente
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Wineburg McGrew 2019 "Lateral Reading and the Nature of Expertise" Teachers College Record»; WebFetch: sí)
- **Ficha metodológica:** Resume el programa de Civic Online Reasoning: encuesta de casi 8.000 estudiantes (2016) con resultados «desalentadores», lectura lateral derivada del trabajo con verificadores y argumento explícito de que las listas de comprobación son ineficaces y fáciles de manipular. Es la exposición más directa de la crítica a CRAAP desde el grupo que propuso la lectura lateral.
- **Uso en el bloque:** DOC-A: justificar que CRAAP (fondo_entry_020) se use solo como recordatorio, subordinado a la lectura lateral.
- **Limitaciones:** Sin fecha ni comité identificados en la página; no aporta tamaños de efecto; proyecto apoyado por Google.org.
- **Criterios derivados:** Ninguno aún.
- **Origen:** Alta V4.0 (2026-11-02), verificada por búsqueda web y lectura de la página.

#### fondo_entry_020 · Q 57 (C) — The CRAAP Test

- **Cita normalizada:** Blakeslee, S. (2004). The CRAAP Test. LOEX Quarterly, 31(3), artículo 4.
- **Tipo de fuente:** Divulgación especializada (lista de comprobación)
- **Ámbito metodológico:** MB-07 Evaluación de credibilidad de fuentes (principal) · secundarias: —
- **Calidad Q:** 57 (C) — Tipo 8/25 · Rigor 7/20 · Autoridad 10/15 · Vigencia 5/10 · Impacto 9/10 · Independencia 10/10 · Acceso 8/10
- **DOI / URL:** https://commons.emich.edu/loexquarterly/vol31/iss3/4
- **Acceso y licencia:** PDF gratuito en el repositorio de Eastern Michigan University (licencia no declarada)
- **Estado:** Vigente
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Blakeslee 2004 "The CRAAP Test" LOEX Quarterly vol 31 iss 3»; WebFetch: sí)
- **Ficha metodológica:** Lista de comprobación de actualidad (Currency), relevancia, autoridad, exactitud (Accuracy) y propósito. Útil como recordatorio de criterios, pero evalúa la fuente «desde dentro»; usar junto a la lectura lateral (fondo_entry_018, fondo_entry_019) y nunca en su lugar (fondo_entry_207).
- **Uso en el bloque:** Documentadores: recordatorio de campos a revisar en la ficha de una fuente.
- **Limitaciones:** Sin validación empírica; criticada por ser manipulable por sitios con apariencia profesional.
- **Criterios derivados:** Ninguno aún.
- **Origen:** Semilla V3.0 (2026-11-01) confirmada en V4.0 (2026-11-02); Q recalificada de 58 a 57.

## Lagunas de cobertura

Áreas con menos de 20 referencias verificadas tras la carga del 02/11/2026 (objetivo del propietario: 20–50 por área):

| Código | Temática | Verificadas | Faltan para 20 |
|---|---|---|---|
| — | Ninguna | — | — |

## Registro de bajas

Sin bajas en la emisión V3.0. fondo_entry_002 (PRISMA 2009) no se da de baja: no es duplicado exacto de fondo_entry_001 y conserva valor de compatibilidad de lectura.

| REF-id | Título | Motivo | Fecha | Sustituta |
|---|---|---|---|---|
| fondo_entry_227 | Google Scholar to overshadow them all? | Duplicado de fondo_entry_129 | 2026-11-02 | fondo_entry_129 |

## Historial de versión

- V2.3 (26/10/2026): 10 entradas de corpus y 4 criterios de la carga de arranque del operador.
- V3.0 (01/11/2026): índice corregido, ordenación por ámbito y Q, identificadores del anexo 8.1 volcados, 10 semillas pendientes de verificación y procedimiento de uso para todos los bloques.
| V3.1 | 02/11/2026 | Carga verificada por búsqueda web: 145 referencias nuevas, 10 fichas existentes reverificadas o reparadas, 1 bajas; reordenación por temática y Q; índice con recuento de verificadas. |

