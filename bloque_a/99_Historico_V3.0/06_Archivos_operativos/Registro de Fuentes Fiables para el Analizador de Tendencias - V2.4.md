# Registro de Fuentes Fiables para el Analizador de Tendencias

**Proyecto Robot Investor · Bloque A — Analizador de Tendencias de Inversión**

**Archivo operativo · Versión 2.4 · 31/10/2026 · Estado: EN OPERACIÓN (carga de arranque de 14 entradas de fuente y 3 fichas de pieza, 25/10/2026; estado «retirada» en vigor por la adenda V1.2 del Bloque A, 26/10/2026)**

**Nota de la versión 2.4 (31/10/2026).** Por la Versión óptima V2.0 del Bloque A, la ficha de fuente incorpora una ampliación de esquema con cuatro campos nuevos (tipología primaria/secundaria/terciaria, enlace a la raíz de evidencia en F2, fiabilidad de la afirmación concreta distinta de la fiabilidad de la fuente y vigencia), definida en la sección 4.2. Las entradas existentes conservan íntegro su esquema; los campos nuevos se cumplimentan en las altas y en las revisiones posteriores de cada ficha, sin reescribir entradas antiguas (regla crítica R16 del bloque). Conforme a la regla crítica R18, la solidez de una evidencia se mide por sus raíces independientes: las copias sindicadas enlazan a su raíz y no cuentan como raíces.

Este archivo está listo para su uso. Contiene su estructura completa, sus reglas y una **carga de arranque de 14 fuentes reales verificadas (8 de nivel A, 4 de nivel B y 2 de nivel C) y 3 fichas de pieza**, dispuesta por el operador el 25/10/2026, que muestra cómo se introducen las fuentes y sus piezas (entradas y piezas en formato compacto desde el 26/10/2026). A partir de aquí, el mantenimiento corresponde a los agentes propietarios conforme a los contratos del Documento 0. La ubicación física y la tecnología del archivo siguen siendo parámetros del operador (Documento 0, Anexo A): este archivo fija la propiedad y la estructura, no la tecnología. La sección 8 añade el anexo del operador con las fuentes fiables específicas de verificación y acceso de cada ficha o entrada registrada (25/10/2026). El 26/10/2026, por disposición del operador, las entradas y las fichas de pieza se convirtieron al formato compacto (bloques de párrafos con los campos etiquetados en negrita, agrupados por temas, en sustitución de la tabla vertical de campos) para contener la extensión y el peso del documento Word ante nuevas altas: el conjunto de campos y los valores no varían (conversión verificada campo a campo). Por la adenda V1.2 del Bloque A (26/10/2026), las entradas y las fichas de pieza admiten además el estado «retirada»: retirada lógica y trazable por revisión de conjunto (convención 9), nunca un borrado físico.

---

## 1. Rol del archivo en la arquitectura del Bloque A

El «Registro de Fuentes Fiables para el Analizador de Tendencias» (nombre canónico en el inventario del Documento 0, 2.3: «Registro de fuentes fiables para tendencias de inversión») es la lista blanca de fuentes del Bloque A: el catálogo de fuentes de mercado, opinión y actualidad verificadas, con su nivel de fiabilidad (A/B/C), su calidad, sus campos de verificación y su historial de uso. Su función esencial es proteger el análisis: nada que no esté en el Registro puede citarse como fuente de un ciclo, y toda afirmación de los entregables es rastreable hasta entradas de este archivo.

Lo alimentan dos agentes con escritura: el **Buscador de tendencias de inversión** (sus propios hallazgos, con origen «Analizador» y verificación ligera) y el **Buscador de fuentes avanzadas** (sus búsquedas avanzadas, con verificación completa o ligera conforme a su protocolo); el operador puede añadir fuentes con origen «Operador». Lo lee el **Buscador** para planificar sus consultas; el **Buscador Avanzado** lo mantiene y lo consulta antes de cada servicio; y sus extractos viajan en los paquetes de servicio al **Orquestador técnico** y de ahí al **Auditor**. Ninguno de los agentes altera las entradas de los otros: cada escritor añade con origen propio y el historial es parte de la evidencia del sistema.

El Registro ocupa la CAPA 3 del esquema arquitectural (archivos y entregables) y se rige por un principio de prudencia: se registra lo que es útil y verificable para el descubrimiento de tendencias, no lo que aparente actividad —ante la duda, no se registra—. Es un archivo **específico del Bloque A**: a diferencia del «Fondo metodológico» y de la «Documentación para el Motor de Cálculo Avanzado» (archivos de alcance ecosistémico que seguirán utilizándose en los bloques posteriores), esta lista blanca atiende a las búsquedas del análisis de tendencias de este bloque. Se diferencia de la «Documentación para tendencias de inversión» (literatura académica y técnica, ámbito del Documentador) y del «Fondo metodológico» (metodología de búsqueda): aquí van los medios, portales, cuentas y fuentes de actualidad con valor de referencia estable.

## 2. Ficha de uso para el agente

| Campo | Detalle |
|---|---|
| Nombre canónico (Documento 0, 2.3) | «Registro de fuentes fiables para tendencias de inversión» |
| Naturaleza del archivo | Lista blanca viva de fuentes verificadas de mercado, opinión y actualidad; catálogo de referencia con niveles de fiabilidad e historial de uso |
| Alcance del archivo | Específico del Bloque A. Los archivos de alcance ecosistémico del bloque (seguirán usándose en bloques posteriores) son el «Fondo metodológico» y la «Documentación para el Motor de Cálculo Avanzado» |
| Propietarios (escritura) | Buscador de fuentes avanzadas (verificación completa o ligera) y Buscador de tendencias de inversión (hallazgos propios, origen «Analizador», verificación ligera); el operador añade con origen «Operador» |
| Lectores autorizados | Buscador (consulta operativa); Buscador Avanzado (mantenimiento y consulta); Orquestador técnico y Auditor (extractos y paquetes) |
| Cuándo leerlo | El Buscador, antes de cada petición de búsqueda y al planificar consultas; el Buscador Avanzado, al inicio de cada servicio y en su primera petición; cualquier agente, antes de citar una fuente |
| Cuándo escribir en él | Tras la verificación de cada fuente aprobada; en los ciclos REG_MAINTENANCE; en la revisión de la primera petición |
| Reglas de escritura | Lectura antes de cada escritura; comprobación de duplicados (misma pieza, misma URL o mismo contenido por otra vía); solo añadir en cuanto al contenido de fuentes (los cambios de estado, calidad o ámbito son entradas nuevas con fecha y motivo); relectura posterior; única excepción: corrección o eliminación de enlaces rotos verificada en mantenimiento, anotada con fecha y motivo |
| Contratos implicados | CT-01 (petición de búsqueda avanzada, Buscador → Buscador Avanzado); CT-06 (paquete de servicio, Buscador Avanzado → Orquestador); CT-07 (revisión experta, extractos); CT-09 (guías para agentes de apoyo) |
| Modos de servicio asociados | ADV_SEARCH y REG_MAINTENANCE (Buscador Avanzado) |
| Relación con otros archivos | Complementa a la «Documentación para tendencias de inversión» (académica y técnica) y al «Fondo metodológico» (metodología de búsqueda); sus verificadores se apoyan en la información de contexto que el propio Registro acumula (fiabilidad histórica, sesgos, sindicación) |
| Material auditable | Sí: entradas, cambios de estado y registros de mantenimiento viajan en el paquete de servicio (CT-06) y alimentan el paquete de auditoría |
| Estado de esta copia | Archivo operativo en arranque; esquema 1.0; carga de arranque del 25/10/2026 (14 entradas y 3 piezas) |

## 3. Convenciones de formato

1. **Identificadores únicos e inmutables** con prefijo `RF-` y cuatro dígitos (RF-0001, RF-0002…) para cada fuente registrada; las piezas concretas se identifican por su URL dentro de la fuente de su `source_id`.
2. **Fechado ISO 8601** en todos los campos de fecha, con distinción entre fecha de publicación de la pieza, fecha de los datos subyacentes y fecha de consulta.
3. **Registro de solo añadir** en cuanto al contenido de fuentes: los cambios de estado, calidad o ámbito son entradas nuevas con fecha y motivo; el historial es parte de la evidencia del sistema.
4. **Nivel de fiabilidad A/B/C** según el protocolo de verificación del Buscador Avanzado: A, fuentes primarias u oficiales y revistas académicas de referencia; B, fuentes académicas o institucionales intermedias (preprints, agregadores académicos) cuyo contenido exige contraste adicional antes de citar afirmaciones sensibles; C, agregadores comerciales y secundarios, útiles como pista de descubrimiento pero nunca como única base de una afirmación. La calidad de la pieza se valora como Alta, Media, Limitada o Insuficiente, con marca «provisional» cuando proceda.
5. **Naturaleza del contenido** siempre tipificada: hecho, análisis, opinión, previsión, rumor o promocional.
6. **Sindicación explícita**: cuando la fuente registrada sea una copia, se anota la pieza original (`syndicated_of`) y sus dependencias; dos copias del mismo origen no son fuentes independientes.
7. **Campo no disponible se declara**: «desconocido», «no aplicable» o «no consultado en la carga de arranque», nunca inventado; ante la duda, no se registra.
8. **Formato compacto de ficha (desde el 26/10/2026, por disposición del operador)**: las entradas (RF) y las fichas de pieza se disponen como bloques de párrafos con los campos etiquetados en negrita, agrupados por temas, en sustitución de la tabla vertical de campos. El conjunto de campos y sus valores son los del esquema 1.0: solo cambia la disposición, verificada campo a campo en la conversión. Las entradas y piezas nuevas se incorporan directamente en formato compacto.
9. **Estado «retirada» (desde el 26/10/2026, adenda V1.2 del Bloque A)**: las entradas y las fichas de pieza admiten el estado «retirada» cuando el Buscador Avanzado las retire por la revisión de conjunto (9.8 de su prompt): redundancia funcional frente a una entrada vigente de calidad, nivel o fiabilidad no inferior, sustitución por una fuente que asuma su cobertura con mejor fiabilidad histórica, o bajo aporte mantenido. La retirada es siempre lógica y trazable: entrada nueva con fecha y motivo en el historial (4.6); la ficha permanece en el archivo como evidencia, deja de alimentar el índice (4.1) y las respuestas a peticiones, y nunca se borra físicamente ni se renumeran identificadores.

## 4. Estructura del archivo

El archivo se compone de seis secciones, en este orden. La carga de arranque del operador (25/10/2026) rellena las secciones 4.1, 4.2, 4.3 y 4.6; los registros de mantenimiento (4.4) y de servicios (4.5) se abren con la primera operación del Buscador Avanzado.

**Nota sobre la carga de arranque.** Las entradas siguientes son fuentes institucionales y editoriales de existencia y URL estables, verificadas el 25/10/2026. Los niveles A/B/C asignados reflejan la naturaleza de cada fuente (primaria u oficial, académica intermedia, comercial secundaria) conforme a la convención 3; el Buscador Avanzado revalidará niveles y restricciones en la revisión de primera petición, sin borrar esta carga.

### 4.1 Índice operativo del Registro

| Campo | Valor |
|---|---|
| Versión del esquema | 1.0 |
| Entradas por nivel | Nivel A (8): RF-0001 a RF-0007 y RF-0012 · Nivel B (4): RF-0008 a RF-0011 · Nivel C (2): RF-0013 y RF-0014 |
| Entradas por acceso | Acceso gratuito íntegro (11) · Acceso variable por pieza (1: RF-0012) · Acceso gratuito como pista, con piezas detrás de muros parciales (2: RF-0013, RF-0014) |
| Mapa de coberturas por ámbito | Datos macro y precios (buena: FRED, Banco Mundial, OCDE, FMI, BCE) · Filings y regulatorio (buena: SEC EDGAR) · Banca central y crédito (buena: BIS, BCE) · Investigación académica (parcial: NBER, SSRN, arXiv, RePEc, FAJ) · Descubrimiento comercial (pista: Yahoo Finance, Investing.com) |
| Coberturas ausentes declaradas | Sin fuente especializada aún en materias primas y futuros como clase de activo (los datos quedan cubiertos por FRED/BIS; el análisis especializado, pendiente de alta) |
| Última revisión del índice | 2026-10-25 (carga de arranque) |
| Carencias y prioridades | Alta futura de una fuente especializada de futuros y commodities; revalidar el nivel y el acceso de RF-0012 por pieza en la primera petición |

### 4.2 Entradas del Registro (sección principal)

Una entrada por fuente estable (campos del Anexo D del prompt del Buscador de fuentes avanzadas, 9.1). Toda la carga tiene origen «Operador» y fecha 2026-10-25; en cada entrada se indican solo los valores que difieren del patrón común: Estado «Aprobada»; Origen «Operador (carga de arranque, sin request_id ni run_id)»; Nivel de verificación «Completa (URL viva y naturaleza del contenido comprobadas el 25/10/2026)»; Fecha de incorporación y de última revisión «2026-10-25»; Historial de correcciones «Sin correcciones registradas (alta reciente)»; Fiabilidad histórica «Sin uso observado aún en el bloque; sin aciertos ni errores registrados». Desde el 26/10/2026 las entradas se disponen en formato compacto (convención 8): un bloque de párrafos por entrada con los campos etiquetados en negrita.

**Esquema ampliado de la ficha de fuente (desde la V2.4 del archivo, 31/10/2026, por la Versión óptima V2.0 del Bloque A).** Además de los campos vigentes del esquema 1.0, cada entrada incorpora los siguientes campos nuevos:

- `source_tier`: tipología cerrada de la fuente: primaria | secundaria | terciaria. Primaria: origen u oficial del dato o del hecho; secundaria: reproduce, comenta o analiza material primario; terciaria: agregador o compilación de material secundario. Complementa al nivel de fiabilidad A/B/C (convención 4) sin sustituirlo.
- `root_evidence_ref`: enlace a la raíz de evidencia registrada en el Registro de evidencia y afirmaciones (F2), en formato EVD-AAAA-NNNN, cuando la fuente derive de otra fuente raíz ya registrada; si la entrada es ella misma raíz, se declara «no aplicable (fuente raíz)».
- `claim_reliability_note`: fiabilidad de la afirmación concreta que la fuente sustenta en cada uso, distinta de la fiabilidad de la fuente (nivel A/B/C), con el vocabulario controlado del bloque: establecido | probable | especulativo | en disputa.
- `validity_note`: vigencia de la fuente: desde cuándo cubre el ámbito que se le registra y su estado de actualidad (vigente | en revisión | desfasada), con la fecha de la última comprobación.

**Nota de política (append-only, reglas críticas R16 y R18 del bloque).** Las entradas existentes conservan íntegro su esquema y sus valores: no se reescriben, no se renumeran y no se les añaden campos retroactivamente. Los campos nuevos se cumplimentan en las altas y en las revisiones posteriores de cada ficha; toda revisión es una entrada nueva con fecha y motivo, referenciada a la ficha original, conforme a la convención 3. En las entradas ya registradas, un campo nuevo sin cumplimentar se declara «no aplicable a la carga de arranque» o «pendiente de la revisión de primera petición», y nunca se inventa (convención 7). La solidez de una evidencia se mide por sus raíces independientes, no por el número de publicaciones que la reproducen: las copias sindicadas (`syndicated_of`, convención 6) enlazan a su raíz y no cuentan como fuentes independientes.

#### RF-0001 — FRED (Federal Reserve Economic Data, Banco de la Reserva Federal de San Luis)

*Identificación y estado.* **source_id:** RF-0001 · **Estado:** Aprobada · **Origen:** Operador (carga de arranque, sin request_id ni run_id) · **Fecha de incorporación:** 2026-10-25 · **Nivel de verificación:** Completa (URL viva y naturaleza del contenido comprobadas el 25/10/2026) · **Fecha de última revisión:** 2026-10-25

*Ámbito y motivo de inclusión.* **Motivo de inclusión:** Portal de datos oficiales más completo para series macroeconómicas y financieras de Estados Unidos, con metadatos de fuente y metodología por serie · **Ámbitos de especialización:** Macroeconomía; precios e inflación; tipos de interés; mercado laboral; indicadores de recesión; renta variable a nivel agregado · **Restricciones de uso:** Uso académico y de referencia; citar la serie concreta y la fuente original que FRED declara en sus metadatos

*Historial y riesgos.* **Fiabilidad histórica:** Sin uso observado aún en el bloque; sin aciertos ni errores registrados · **Historial de correcciones:** Sin correcciones registradas (alta reciente) · **Sesgos posibles:** Ninguno editorial conocido; posible sesgo de cobertura hacia series estadounidenses · **Cambios de propiedad o de metodología:** Sin cambios conocidos; mantiene el hosting del Fed de San Luis; verificar en cada mantenimiento


#### RF-0002 — SEC EDGAR (U.S. Securities and Exchange Commission)

*Identificación y estado.* **source_id:** RF-0002 · **Estado:** Aprobada · **Origen:** Operador (carga de arranque, sin request_id ni run_id) · **Fecha de incorporación:** 2026-10-25 · **Nivel de verificación:** Completa (URL viva y naturaleza del contenido comprobadas el 25/10/2026) · **Fecha de última revisión:** 2026-10-25

*Ámbito y motivo de inclusión.* **Motivo de inclusión:** Repositorio primario de documentos regulatorios de emisores estadounidenses (10-K, 10-Q, 8-K, 13F): la fuente de máxima autoridad para hechos corporativos · **Ámbitos de especialización:** Filings y documentos regulatorios; hechos corporativos; participaciones institucionales; emisores estadounidenses · **Restricciones de uso:** Datos públicos; citar el formulario, la fecha de presentación y el CIK del emisor

*Historial y riesgos.* **Fiabilidad histórica:** Sin uso observado aún en el bloque; sin aciertos ni errores registrados · **Historial de correcciones:** Sin correcciones registradas (alta reciente) · **Sesgos posibles:** Ninguno; son documentos primarios, con el matiz de que los propios emisores redactan sus declaraciones · **Cambios de propiedad o de metodología:** Sin cambios conocidos; dependencia del servicio público EDGAR


#### RF-0003 — BIS (Bank for International Settlements), sección de estadísticas

*Identificación y estado.* **source_id:** RF-0003 · **Estado:** Aprobada · **Origen:** Operador (carga de arranque, sin request_id ni run_id) · **Fecha de incorporación:** 2026-10-25 · **Nivel de verificación:** Completa (URL viva y naturaleza del contenido comprobadas el 25/10/2026) · **Fecha de última revisión:** 2026-10-25

*Ámbito y motivo de inclusión.* **Motivo de inclusión:** Estadísticas internacionales de referencia en banca central: crédito, tipos de cambio efectivos, derivados de OTC y deuda global · **Ámbitos de especialización:** Crédito global; banca central; deuda; derivados de OTC; mercados de divisas · **Restricciones de uso:** Uso libre con atribución; citar la base estadística concreta y la fecha de extracción

*Historial y riesgos.* **Fiabilidad histórica:** Sin uso observado aún en el bloque; sin aciertos ni errores registrados · **Historial de correcciones:** Sin correcciones registradas (alta reciente) · **Sesgos posibles:** Ninguno editorial conocido; cobertura centrada en bancos centrales miembros · **Cambios de propiedad o de metodología:** Sin cambios conocidos; el BIS revisa metodologías de sus bases periódicamente (vigilar notas de las series)


#### RF-0004 — BCE Data Portal (Banco Central Europeo)

*Identificación y estado.* **source_id:** RF-0004 · **Estado:** Aprobada · **Origen:** Operador (carga de arranque, sin request_id ni run_id) · **Fecha de incorporación:** 2026-10-25 · **Nivel de verificación:** Completa (URL viva y naturaleza del contenido comprobadas el 25/10/2026) · **Fecha de última revisión:** 2026-10-25

*Ámbito y motivo de inclusión.* **Motivo de inclusión:** Fuente oficial de datos de la eurozona: tipos, agregados monetarios, inflación HICP y balanza de pagos, con API pública · **Ámbitos de especialización:** Eurozona; tipos de cambio; política monetaria; inflación HICP; agregados monetarios · **Restricciones de uso:** Datos públicos con atribución; citar la serie de la base SDW y su fecha

*Historial y riesgos.* **Fiabilidad histórica:** Sin uso observado aún en el bloque; sin aciertos ni errores registrados · **Historial de correcciones:** Sin correcciones registradas (alta reciente) · **Sesgos posibles:** Ninguno; cobertura eurozona · **Cambios de propiedad o de metodología:** Portal nuevo (sucesor del SDW clásico): vigilar reorganizaciones de series


#### RF-0005 — World Bank Open Data (Banco Mundial)

*Identificación y estado.* **source_id:** RF-0005 · **Estado:** Aprobada · **Origen:** Operador (carga de arranque, sin request_id ni run_id) · **Fecha de incorporación:** 2026-10-25 · **Nivel de verificación:** Completa (URL viva y naturaleza del contenido comprobadas el 25/10/2026) · **Fecha de última revisión:** 2026-10-25

*Ámbito y motivo de inclusión.* **Motivo de inclusión:** Indicadores macro globales comparables (PIB, población, desarrollo) con metodología documentada y acceso API · **Ámbitos de especialización:** Macroeconomía global; desarrollo; indicadores por país; comparaciones internacionales · **Restricciones de uso:** CC BY 4.0 en general; citar indicador (código), país y año

*Historial y riesgos.* **Fiabilidad histórica:** Sin uso observado aún en el bloque; sin aciertos ni errores registrados · **Historial de correcciones:** Sin correcciones registradas (alta reciente) · **Sesgos posibles:** Revisión retrospectiva de datos nacionales; desfase de publicación de un año en varios indicadores · **Cambios de propiedad o de metodología:** Sin cambios conocidos; las series se revisan con las actualizaciones anuales del World Development Indicators


#### RF-0006 — OECD Data (Organización para la Cooperación y el Desarrollo Económicos)

*Identificación y estado.* **source_id:** RF-0006 · **Estado:** Aprobada · **Origen:** Operador (carga de arranque, sin request_id ni run_id) · **Fecha de incorporación:** 2026-10-25 · **Nivel de verificación:** Completa (URL viva y naturaleza del contenido comprobadas el 25/10/2026) · **Fecha de última revisión:** 2026-10-25

*Ámbito y motivo de inclusión.* **Motivo de inclusión:** Indicadores comparables de países OCDE (crecimiento, empleo, precios, comercio) con notas metodológicas editoriales · **Ámbitos de especialización:** Países OCDE; empleo; comercio; industria; política económica comparada · **Restricciones de uso:** Condiciones de uso del portal; citar indicador y país

*Historial y riesgos.* **Fiabilidad histórica:** Sin uso observado aún en el bloque; sin aciertos ni errores registrados · **Historial de correcciones:** Sin correcciones registradas (alta reciente) · **Sesgos posibles:** Cobertura OCDE; los antiguos data.oecd.org redirigen al portal vigente (oecd.org) · **Cambios de propiedad o de metodología:** Migración de portal (data.oecd.org → oecd.org): revalidar URLs en el primer mantenimiento


#### RF-0007 — IMF Data (Fondo Monetario Internacional)

*Identificación y estado.* **source_id:** RF-0007 · **Estado:** Aprobada · **Origen:** Operador (carga de arranque, sin request_id ni run_id) · **Fecha de incorporación:** 2026-10-25 · **Nivel de verificación:** Completa (URL viva y naturaleza del contenido comprobadas el 25/10/2026) · **Fecha de última revisión:** 2026-10-25

*Ámbito y motivo de inclusión.* **Motivo de inclusión:** Bases de datos oficiales del FMI (Perspectivas de la Economía Mundial, estadísticas financieras internacionales, servicios y prerrogativas de los países miembros) · **Ámbitos de especialización:** Macroeconomía global; balanza de pagos; reservas; estabilidad financiera · **Restricciones de uso:** Condiciones del portal del FMI; citar base, serie y edición (los datos de proyección cambian por edición)

*Historial y riesgos.* **Fiabilidad histórica:** Sin uso observado aún en el bloque; sin aciertos ni errores registrados · **Historial de correcciones:** Sin correcciones registradas (alta reciente) · **Sesgos posibles:** Las proyecciones WEO son estimaciones del FMI, no hechos: tratarlas como previsión · **Cambios de propiedad o de metodología:** Ediciones WEO semestrales: anotar siempre la edición usada


#### RF-0008 — NBER Working Papers (National Bureau of Economic Research)

*Identificación y estado.* **source_id:** RF-0008 · **Estado:** Aprobada · **Origen:** Operador (carga de arranque, sin request_id ni run_id) · **Fecha de incorporación:** 2026-10-25 · **Nivel de verificación:** Completa (URL viva y naturaleza del contenido comprobadas el 25/10/2026) · **Fecha de última revisión:** 2026-10-25

*Ámbito y motivo de inclusión.* **Motivo de inclusión:** Documentos de trabajo de investigación económica de primer nivel; muchos se publican después en revistas revisadas por pares · **Ámbitos de especialización:** Investigación económica y financiera; literatura de frontera; datos y metodologías nuevos · **Restricciones de uso:** Muchos WP son de descarga gratuita y otros tienen coste o requieren registro; verificar pieza a pieza; un WP no está revisado por pares: citarlo como documento de trabajo

*Historial y riesgos.* **Fiabilidad histórica:** Sin uso observado aún en el bloque; sin aciertos ni errores registrados · **Historial de correcciones:** Sin correcciones registradas (alta reciente) · **Sesgos posibles:** Contenido no revisado por pares en el momento de la publicación; verificar si existe versión publicada posterior · **Cambios de propiedad o de metodología:** Sin cambios conocidos


#### RF-0009 — SSRN (Social Science Research Network)

*Identificación y estado.* **source_id:** RF-0009 · **Estado:** Aprobada · **Origen:** Operador (carga de arranque, sin request_id ni run_id) · **Fecha de incorporación:** 2026-10-25 · **Nivel de verificación:** Completa (URL viva y naturaleza del contenido comprobadas el 25/10/2026) · **Fecha de última revisión:** 2026-10-25

*Ámbito y motivo de inclusión.* **Motivo de inclusión:** Principal repositorio de preprints de finanzas y economía: acceso temprano a la investigación antes de su publicación en revista · **Ámbitos de especialización:** Finanzas; economía; literatura de frontera; versiones de autor · **Restricciones de uso:** Descarga gratuita con registro; citar como preprint con su abstract_id y comprobar si existe versión publicada posterior

*Historial y riesgos.* **Fiabilidad histórica:** Sin uso observado aún en el bloque; sin aciertos ni errores registrados · **Historial de correcciones:** Sin correcciones registradas (alta reciente) · **Sesgos posibles:** Sin revisión por pares garantizada; sesgo de publicación de autores y de papers aún no filtrados · **Cambios de propiedad o de metodología:** Propiedad de Elsevier desde 2016; vigilar cambios de acceso


#### RF-0010 — arXiv q-fin (Quantitative Finance)

*Identificación y estado.* **source_id:** RF-0010 · **Estado:** Aprobada · **Origen:** Operador (carga de arranque, sin request_id ni run_id) · **Fecha de incorporación:** 2026-10-25 · **Nivel de verificación:** Completa (URL viva y naturaleza del contenido comprobadas el 25/10/2026) · **Fecha de última revisión:** 2026-10-25

*Ámbito y motivo de inclusión.* **Motivo de inclusión:** Repositorio abierto de preprints de finanzas cuantitativas y econofísica: acceso gratuito e inmediato · **Ámbitos de especialización:** Finanzas cuantitativas; modelización; econofísica; métodos estadísticos · **Restricciones de uso:** Licencias abiertas por pieza (frecuente arXiv non-exclusive); citar identificador arXiv y versión

*Historial y riesgos.* **Fiabilidad histórica:** Sin uso observado aún en el bloque; sin aciertos ni errores registrados · **Historial de correcciones:** Sin correcciones registradas (alta reciente) · **Sesgos posibles:** Sin revisión por pares (solo moderación de ámbito); calidad heterogénea · **Cambios de propiedad o de metodología:** Sin cambios conocidos


#### RF-0011 — RePEc / IDEAS (Research Papers in Economics)

*Identificación y estado.* **source_id:** RF-0011 · **Estado:** Aprobada · **Origen:** Operador (carga de arranque, sin request_id ni run_id) · **Fecha de incorporación:** 2026-10-25 · **Nivel de verificación:** Completa (URL viva y naturaleza del contenido comprobadas el 25/10/2026) · **Fecha de última revisión:** 2026-10-25

*Ámbito y motivo de inclusión.* **Motivo de inclusión:** Agregador académico descentralizado de literatura económica: localiza versiones de acceso gratuito (verdes) de artículos publicados en revistas de pago · **Ámbitos de especialización:** Economía y finanzas; localización de versiones de trabajo y de acceso gratuito; bibliografía estructurada · **Restricciones de uso:** Es un agregador: citar la fuente primaria que RePEc enlaza, no IDEAS

*Historial y riesgos.* **Fiabilidad histórica:** Sin uso observado aún en el bloque; sin aciertos ni errores registrados · **Historial de correcciones:** Sin correcciones registradas (alta reciente) · **Sesgos posibles:** Cobertura dependiente de los archivos participantes; metadatos a veces incompletos · **Cambios de propiedad o de metodología:** Sin cambios conocidos


#### RF-0012 — Financial Analysts Journal (CFA Institute / Taylor & Francis)

*Identificación y estado.* **source_id:** RF-0012 · **Estado:** Aprobada · **Origen:** Operador (carga de arranque, sin request_id ni run_id) · **Fecha de incorporación:** 2026-10-25 · **Nivel de verificación:** Completa (URL viva y naturaleza del contenido comprobadas el 25/10/2026) · **Fecha de última revisión:** 2026-10-25

*Ámbito y motivo de inclusión.* **Motivo de inclusión:** Revista insignia revisada por pares para profesionales de la inversión (publica desde 1945); puente entre la academia y la práctica de carteras · **Ámbitos de especialización:** Gestión de carteras; análisis de inversiones; investigación aplicada para el inversor profesional · **Restricciones de uso:** Publicada por Taylor & Francis para el CFA Institute; el acceso es variable por pieza (opción de acceso abierto para autores; verificar cada artículo)

*Historial y riesgos.* **Fiabilidad histórica:** Sin uso observado aún en el bloque; sin aciertos ni errores registrados · **Historial de correcciones:** Sin correcciones registradas (alta reciente) · **Sesgos posibles:** Orientación profesional (gestión de carteras); premios Graham and Dodd como señal de calidad · **Cambios de propiedad o de metodología:** Sin cambios conocidos; revalidar nivel de acceso por pieza en cada uso


#### RF-0013 — Yahoo Finance

*Identificación y estado.* **source_id:** RF-0013 · **Estado:** Aprobada · **Origen:** Operador (carga de arranque, sin request_id ni run_id) · **Fecha de incorporación:** 2026-10-25 · **Nivel de verificación:** Completa (URL viva y naturaleza del contenido comprobadas el 25/10/2026) · **Fecha de última revisión:** 2026-10-25

*Ámbito y motivo de inclusión.* **Motivo de inclusión:** Agregador comercial gratuito de cotizaciones, gráficos y titulares: útil como pista de descubrimiento y para corroborar fechas de mercado · **Ámbitos de especialización:** Cotizaciones; titulares de mercado; calendario económico básico · **Restricciones de uso:** Condiciones del servicio; no citar como fuente primaria de un hecho

*Historial y riesgos.* **Fiabilidad histórica:** Sin uso observado aún en el bloque; sin aciertos ni errores registrados · **Historial de correcciones:** Sin correcciones registradas (alta reciente) · **Sesgos posibles:** Agregación sin control editorial de los datos de cotización; titulares sindicados de terceros (anotar siempre `syndicated_of` cuando se identifique) · **Cambios de propiedad o de metodología:** Propiedad de Yahoo/Verizon Media; vigilar cambios de URL de piezas


#### RF-0014 — Investing.com

*Identificación y estado.* **source_id:** RF-0014 · **Estado:** Aprobada · **Origen:** Operador (carga de arranque, sin request_id ni run_id) · **Fecha de incorporación:** 2026-10-25 · **Nivel de verificación:** Completa (URL viva y naturaleza del contenido comprobadas el 25/10/2026) · **Fecha de última revisión:** 2026-10-25

*Ámbito y motivo de inclusión.* **Motivo de inclusión:** Portal comercial de datos de mercado, calendario económico y análisis; cobertura global y gratuita · **Ámbitos de especialización:** Cotizaciones; calendario económico; análisis de opinión · **Restricciones de uso:** Condiciones del portal; doblar verificación contra fuentes primarias (RF-0001 a RF-0007) antes de citar cualquier dato

*Historial y riesgos.* **Fiabilidad histórica:** Sin uso observado aún en el bloque; sin aciertos ni errores registrados · **Historial de correcciones:** Sin correcciones registradas (alta reciente) · **Sesgos posibles:** Contenido de analistas de naturaleza opinativa; datos agregados sin metodología declarada en muchas páginas · **Cambios de propiedad o de metodología:** Sin cambios conocidos


### 4.3 Fichas de pieza registrada

Una ficha por pieza concreta (artículo, emisión, publicación o serie) vinculada a su `source_id` (campos del Anexo D, 9.2). La carga de arranque incluye tres piezas de ejemplo —series de datos estables de fuentes de nivel A— para mostrar el formato completo de pieza. Desde el 26/10/2026 las piezas se disponen en formato compacto (convención 8): un bloque de párrafos por pieza con los campos etiquetados en negrita.

#### Pieza de RF-0001 — Serie CPIAUCSL de FRED

*Identificación.* **source_id:** RF-0001 (FRED) · **Nombre del medio o cuenta y URL de la pieza:** FRED · Serie CPIAUCSL «Consumer Price Index for All Urban Consumers: All Items in U.S. City Average» · fred.stlouisfed.org/series/CPIAUCSL · **Tipo de medio:** Serie de datos oficial · **Nivel:** A · **Autor o entidad responsable:** U.S. Bureau of Labor Statistics (compilación y hospedaje: Banco de la Reserva Federal de San Luis)

*Fechas y metodología.* **Fecha de publicación de la pieza (published_at):** No aplicable (serie continua con actualización mensual) · **Fecha de los datos subyacentes (data_as_of):** Variable: la última observación disponible es la que declara la propia serie en la fecha de consulta · **Fecha de consulta:** 2026-10-25 · **Metodología declarada:** Sí: el BLS publica la metodología del IPC y FRED enlaza la fuente original y las notas de la serie

*Contenido y uso.* **Naturaleza del contenido:** Hecho (serie estadística oficial) · **Calidad:** Alta · **Temáticas y ámbitos:** Inflación de Estados Unidos; tipos de interés reales; contexto macro del ciclo · **Afirmaciones que respalda:** Ninguna aún (sin uso en operación); apta para datar afirmaciones sobre inflación observada · **Limitaciones conocidas:** Dato revisado y reajustable; definición de «todos los bienes urbanos» acotada al ámbito de consumo estadounidense

*Estado y verificación.* **Estado:** Aprobada · **Resultado de la verificación:** Completa (carga de arranque): URL viva, fuente original y periodicidad comprobadas el 25/10/2026 · **Posibles conflictos de interés:** Ninguno conocido; sin sindicación (syndicated_of: no aplicable, fuente primaria) · **Historial de fiabilidad:** Sin uso observado aún en el bloque · **Restricciones de uso:** Citar la serie por su identificador, la fecha de consulta y la fuente original declarada por FRED · **Origen en la ejecución:** Carga de arranque del operador · **request_id y run_id de origen:** Sin request_id ni run_id (alta preoperativa del operador)


#### Pieza de RF-0005 — Indicador NY.GDP.MKTP.CD del Banco Mundial

*Identificación.* **source_id:** RF-0005 (World Bank Open Data) · **Nombre del medio o cuenta y URL de la pieza:** World Bank Open Data · Indicador NY.GDP.MKTP.CD «GDP (current US$)» · data.worldbank.org/indicator/NY.GDP.MKTP.CD · **Tipo de medio:** Serie de datos oficial · **Nivel:** A · **Autor o entidad responsable:** Banco Mundial (datos compilados de cuentas nacionales de los países miembros y de la OCDE)

*Fechas y metodología.* **Fecha de publicación de la pieza (published_at):** No aplicable (serie anual con actualización en la edición anual del World Development Indicators) · **Fecha de los datos subyacentes (data_as_of):** Variable por país; la serie declara el último año disponible en la fecha de consulta · **Fecha de consulta:** 2026-10-25 · **Metodología declarada:** Sí: notas metodológicas por indicador y fuentes nacionales declaradas

*Contenido y uso.* **Naturaleza del contenido:** Hecho (serie estadística oficial) · **Calidad:** Alta · **Temáticas y ámbitos:** PIB nominal en dólares; comparaciones internacionales; tamaño de mercado por país · **Afirmaciones que respalda:** Ninguna aún (sin uso en operación); apta para datar afirmaciones sobre tamaño económico comparado · **Limitaciones conocidas:** Reajustes retrospectivos; conversiones a dólares corrientes sensibles al tipo de cambio; desfase de un año en la publicación

*Estado y verificación.* **Estado:** Aprobada · **Resultado de la verificación:** Completa (carga de arranque): URL viva y estructura del indicador comprobadas el 25/10/2026 · **Posibles conflictos de interés:** Ninguno conocido; sin sindicación (syndicated_of: no aplicable, fuente primaria) · **Historial de fiabilidad:** Sin uso observado aún en el bloque · **Restricciones de uso:** Licencia CC BY 4.0 en general; citar código de indicador, país, año y fecha de consulta · **Origen en la ejecución:** Carga de arranque del operador · **request_id y run_id de origen:** Sin request_id ni run_id (alta preoperativa del operador)


#### Pieza de RF-0003 — Estadísticas de crédito del BIS

*Identificación.* **source_id:** RF-0003 (BIS Statistics) · **Nombre del medio o cuenta y URL de la pieza:** BIS · «Credit to the non-financial sector» · bis.org/statistics/totcredit.htm · **Tipo de medio:** Base estadística oficial · **Nivel:** A · **Autor o entidad responsable:** Bank for International Settlements

*Fechas y metodología.* **Fecha de publicación de la pieza (published_at):** No aplicable (base trimestral de actualización continua) · **Fecha de los datos subyacentes (data_as_of):** Variable: último trimestre declarado por la base en la fecha de consulta · **Fecha de consulta:** 2026-10-25 · **Metodología declarada:** Sí: notas metodológicas de las series de crédito al sector no financiero

*Contenido y uso.* **Naturaleza del contenido:** Hecho (serie estadística oficial) · **Calidad:** Alta · **Temáticas y ámbitos:** Crédito total y privado; apalancamiento macro; ciclos de crédito por país · **Afirmaciones que respalda:** Ninguna aún (sin uso en operación); apta para datar afirmaciones sobre el ciclo de crédito · **Limitaciones conocidas:** Cobertura por países participantes; revisiones de metodología del BIS documentadas en sus notas

*Estado y verificación.* **Estado:** Aprobada · **Resultado de la verificación:** Completa (carga de arranque): URL viva y presencia de la base comprobadas el 25/10/2026 · **Posibles conflictos de interés:** Ninguno conocido; sin sindicación (syndicated_of: no aplicable, fuente primaria) · **Historial de fiabilidad:** Sin uso observado aún en el bloque · **Restricciones de uso:** Uso con atribución; citar base, país, serie y trimestre · **Origen en la ejecución:** Carga de arranque del operador · **request_id y run_id de origen:** Sin request_id ni run_id (alta preoperativa del operador)


### 4.4 Registro de mantenimiento

El primer ciclo REG_MAINTENANCE lo ejecutará el Buscador Avanzado según el calendario que fije el operador (Anexo A). Columnas del registro: service_id; fecha; tipo de ciclo (enlaces, propiedad y línea editorial, desmentidos y correcciones, revalidación, índice); entradas revisadas; hallazgos; cambios de estado registrados con fecha y motivo; correcciones o eliminaciones de enlaces con fecha y motivo; pendientes declarados. Prioridad de mantenimiento: las entradas más utilizadas por el Buscador y las que sostienen tesis abiertas.

| service_id | Fecha | Tipo de ciclo | Entradas revisadas | Hallazgos | Pendientes |
|---|---|---|---|---|---|
| (sin ciclos registrados a la fecha de la carga de arranque) | — | — | — | — | Revalidar nivel de acceso de RF-0012 por pieza; revalidar URLs de RF-0006 tras la migración del portal de la OCDE |

### 4.5 Registro de servicios

Una fila por servicio del Buscador Avanzado. La carga de arranque del operador no es un servicio ADV_SEARCH ni REG_MAINTENANCE y no se registra aquí; queda anotada en el historial (4.6). Columnas del registro: service_id; request_id; run_id; execution_mode (ADV_SEARCH, REG_MAINTENANCE); origin (BUSCADOR, OPERATOR, SCHEDULER); started_at; completed_at; as_of; prompt_version; estrategia aplicada; consultas e iteraciones; fuentes entregadas, rechazadas y sin verificar; escrituras en el Registro y su confirmación; lagunas; incidencias y manipulaciones detectadas; estado final del servicio.

| service_id | request_id | run_id | execution_mode | origin | started_at | completed_at | Estado |
|---|---|---|---|---|---|---|---|
| (sin servicios registrados a la fecha de la carga de arranque) | — | — | — | — | — | — | — |

### 4.6 Historial de altas y cambios de estado

Diario de solo añadir (fecha; `source_id` afectado; movimiento; agente u origen responsable; motivo).

| Fecha | Fuente afectada | Movimiento | Agente u origen responsable | Motivo |
|---|---|---|---|---|
| 2026-10-25 | RF-0001 | Alta (nivel A) | Operador (carga de arranque) | Datos macro oficiales de Estados Unidos |
| 2026-10-25 | RF-0002 | Alta (nivel A) | Operador (carga de arranque) | Filings regulatorios primarios |
| 2026-10-25 | RF-0003 | Alta (nivel A) | Operador (carga de arranque) | Estadísticas de banca central global |
| 2026-10-25 | RF-0004 | Alta (nivel A) | Operador (carga de arranque) | Datos oficiales de la eurozona |
| 2026-10-25 | RF-0005 | Alta (nivel A) | Operador (carga de arranque) | Indicadores macro globales comparables |
| 2026-10-25 | RF-0006 | Alta (nivel A) | Operador (carga de arranque) | Indicadores OCDE comparables |
| 2026-10-25 | RF-0007 | Alta (nivel A) | Operador (carga de arranque) | Bases oficiales del FMI |
| 2026-10-25 | RF-0008 | Alta (nivel B) | Operador (carga de arranque) | Documentos de trabajo académicos |
| 2026-10-25 | RF-0009 | Alta (nivel B) | Operador (carga de arranque) | Preprints académicos de finanzas y economía |
| 2026-10-25 | RF-0010 | Alta (nivel B) | Operador (carga de arranque) | Preprints de finanzas cuantitativas |
| 2026-10-25 | RF-0011 | Alta (nivel B) | Operador (carga de arranque) | Agregador académico y localizador de versiones verdes |
| 2026-10-25 | RF-0012 | Alta (nivel A) | Operador (carga de arranque) | Revista profesional revisada por pares |
| 2026-10-25 | RF-0013 | Alta (nivel C) | Operador (carga de arranque) | Agregador comercial: solo pista de descubrimiento |
| 2026-10-25 | RF-0014 | Alta (nivel C) | Operador (carga de arranque) | Portal comercial: doblar verificación |
| 2026-10-25 | Pieza de RF-0001 | Alta de pieza | Operador (carga de arranque) | Serie CPIAUCSL como pieza de ejemplo de datos oficiales |
| 2026-10-25 | Pieza de RF-0005 | Alta de pieza | Operador (carga de arranque) | Indicador NY.GDP.MKTP.CD como pieza de ejemplo |
| 2026-10-25 | Pieza de RF-0003 | Alta de pieza | Operador (carga de arranque) | Base de crédito del BIS como pieza de ejemplo |

## 5. Qué se registra y qué no

Se registran fuentes de mercado, opinión y actualidad con valor de referencia estable: medios, portales especializados, cuentas e informes verificados, cuyo uso previsible sirva al descubrimiento de tendencias. No se registra: literatura académica o técnica (ámbito del Documentador y de la «Documentación para tendencias de inversión»); cotizaciones, series de precios o datos de mercado como datos (las series estadísticas oficiales del Registro se registran como fuentes de referencia y sus metadatos, no como volúmenes de datos); piezas de uso puntual sin valor de referencia estable; fuentes que no superen el filtro de verificación; y nada cuya fiabilidad no pueda comprobarse. Tampoco se registra por mera cantidad ni para aparentar actividad: cada entrada debe justificarse por su utilidad previsible.

## 6. Reglas de mantenimiento y ciclo de vida

1. **Revisión de primera petición**: en la primera petición de búsqueda que reciba el Buscador Avanzado, se revisa el Registro completo —con prioridad en las URL de RF-0006 (migración del portal de la OCDE) y el acceso por pieza de RF-0012—, se clasifican las fuentes según criterio útil para el Buscador y se ordenan por importancia conforme al criterio del propio Buscador; el resultado se declara en la respuesta.
2. **Comprobación previa a cada servicio**: los enlaces del Registro deben funcionar; los rotos se corrigen (URL nueva o equivalente estable) o se eliminan, anotándolo con fecha y motivo; la comprobación no bloquea el servicio si no puede completarse, y la limitación se declara.
3. **Ciclo REG_MAINTENANCE** conforme al calendario que fije el operador (Anexo A): vitalidad de enlaces, cambios de propiedad o de línea editorial, desmentidos y correcciones, vigencia de las fuentes; las entradas afectadas se marcan «en revisión» con motivo y fecha y se revalidan.
4. **Reordenación tras cada petición**: tras finalizar una búsqueda, las fuentes se reordenan por prioridad para el Buscador, de acuerdo con el índice operativo y el mapa de coberturas; la reordenación se declara, sin borrar ni reescribir historial.
5. **Degradación honesta**: sin planificador real, el calendario se formula como recomendación, sin afirmar que está programado.

## 7. Control de versiones del archivo


| Versión | Fecha | Cambio |

|---|---|---|

| 1.0 | 2026-10-25 | Primera emisión como plantilla de formato, vacía de contenido y de fuentes. |

| 2.0 | 2026-10-25 | Conversión a archivo operativo: carga de arranque con 14 entradas (niveles A/B/C) y 3 fichas de pieza dispuesta por el operador; prefijo de identificador RF- fijado; alcance específico del Bloque A declarado. |
| 2.1 | 2026-10-25 | Anexo documental del operador: añadida la sección 8 «Fuentes fiables específicas de este archivo», con el canal oficial de acceso y documentación por entrada (8.1) y los canales transversales (8.2). No altera el esquema 1.0 ni los niveles, estados ni restricciones de las fichas. |

| 2.2 | 2026-10-26 | Cambio de disposición de las fichas por disposición del operador: las 14 entradas y las 3 fichas de pieza pasan de la tabla vertical de campos al formato compacto de bloques de párrafos con campos etiquetados en negrita (convención 8), para contener la extensión y el peso del documento .docx ante nuevas altas. No altera el esquema 1.0: el conjunto de campos y los valores de cada ficha se conservan íntegros (conversión verificada campo a campo). |

| 2.3 | 2026-10-26 | Adenda V1.2 del Bloque A (aprobada por el operador y aplicada por paquete coordinado conforme al Documento 0, 5.3): las entradas y las fichas de pieza admiten el estado «retirada» (convención 9) para la retirada lógica de fuentes por revisión de conjunto del Buscador Avanzado (9.8 de su prompt); la retirada es siempre un cambio de estado trazable (entrada nueva con fecha y motivo en 4.6) y nunca un borrado físico ni una renumeración. No altera el esquema 1.0 ni los datos de las fichas. |
| 2.4 | 2026-10-31 | V2.4 · esquema ampliado (tipología primaria/secundaria/terciaria, enlace a raíz de evidencia F2, fiabilidad de la afirmación, vigencia), definido en la sección 4.2. No altera los datos de las fichas: las entradas existentes conservan su esquema (append-only, regla crítica R16) y los campos nuevos se cumplimentan en altas y en revisiones posteriores de cada ficha; la solidez se mide por raíces independientes (regla crítica R18). |

## 8. Fuentes fiables específicas de este archivo

*(Anexo documental del operador, 25/10/2026.)* Las fichas del Registro (4.2) describen cada fuente fiable sin fijar su URL oficial de acceso ni su canal de documentación: este apartado los fija por entrada, verificados el 25/10/2026. Son los canales oficiales que el Buscador de fuentes avanzadas debe usar para citar y consultar cada fuente, y los que se revisan en los ciclos REG_MAINTENANCE (vitalidad de enlaces, cambios de propiedad y de línea editorial) igual que las piezas registradas (4.3). El acceso programático, cuando exista API, se rige por las condiciones de uso que cada servicio publica en su propio portal y, en su caso, por el régimen de claves API del Broker Personal (prompt del Buscador de fuentes avanzadas). Este anexo no modifica niveles, estados ni restricciones de las fichas.

### 8.1 Canal oficial de acceso y documentación por entrada

| Entrada | Canal oficial de acceso | Documentación y notas de verificación |
|---|---|---|
| RF-0001 — FRED | fred.stlouisfed.org | Documentación de la API: fred.stlouisfed.org/docs/api/fred/ · Cada serie declara su fuente original y metodología en sus metadatos (p. ej. la serie CPIAUCSL de la pieza 4.3: fred.stlouisfed.org/series/CPIAUCSL) |
| RF-0002 — SEC EDGAR | sec.gov/edgar | Búsqueda de texto completo: sec.gov/edgar/search/ · Documentación de APIs estructuradas: sec.gov/edgar/sec-api-documentation · Citar formulario, fecha de presentación y CIK (ficha) |
| RF-0003 — BIS | bis.org/statistics/ | Portal de datos vigente: data.bis.org · Serie de crédito total de la pieza 4.3: bis.org/statistics/totcredit.htm |
| RF-0004 — BCE Data Portal | data.ecb.europa.eu | Descargas, metadatos SDMX y documentación desde el propio portal · Citar la serie con su clave SDMX y la fecha de consulta |
| RF-0005 — World Bank Open Data | data.worldbank.org | Documentación de API: datahelpdesk.worldbank.org · Indicador de la pieza 4.3: data.worldbank.org/indicator/NY.GDP.MKTP.CD |
| RF-0006 — OCDE | data-explorer.oecd.org (portal vigente) | Con documentación de API y límites de descarga en el propio portal · Los antiguos data.oecd.org redirigen al portal actual (nota ya anotada en la ficha: revalidar en el primer mantenimiento) |
| RF-0007 — IMF Data | data.imf.org | **Nota de verificación**: el punto de acceso SDMX histórico (dataservices.imf.org) quedó retirado en 2025; el acceso vigente es el propio portal data.imf.org. Revalidar esta entrada en el primer mantenimiento |
| RF-0008 — NBER Working Papers | nber.org/papers | Trabajos con página propia por número (nber.org/papers/wNNNNN); citar número de WP y año; versiones abiertas del autor frecuentes |
| RF-0009 — SSRN | ssrn.com | Resúmenes y descargas gratuitas con registro; citar el abstract_id de cada trabajo |
| RF-0010 — arXiv q-fin | arxiv.org/list/q-fin/recent | Documentación de API: info.arxiv.org/help/api/ · Citar identificador arXiv y versión (ficha) |
| RF-0011 — RePEc / IDEAS | ideas.repec.org | Espejo: econpapers.repec.org · Útil para metadatos normalizados de trabajos y revistas económicas que sustentan otras entradas (NBER, SSRN, FAJ) |
| RF-0012 — Financial Analysts Journal | tandfonline.com (página de la revista en Taylor & Francis) | Institución editora: cfainstitute.org · Acceso variable por pieza (ficha): verificar cada artículo en el primer uso |
| RF-0013 — Yahoo Finance | finance.yahoo.com | Pista de descubrimiento (nivel C): todo dato extraído aquí debe verificarse contra una fuente de nivel A antes de citarse (ficha) |
| RF-0014 — Investing.com | investing.com | Pista de descubrimiento (nivel C): mismo matiz de verificación previa que RF-0013 (ficha) |

### 8.2 Canales transversales de verificación (todo el archivo)

| Canal | Uso en este archivo |
|---|---|
| Wayback Machine (web.archive.org) | Capturas históricas de páginas para reparar enlaces rotos en REG_MAINTENANCE: la única excepción de escritura admitida por el Registro (corrección de enlaces, anotada con fecha y motivo) |
| Políticas de uso de cada servicio | Cada portal fija límites, condiciones y condiciones de citación; revisarlas antes de cualquier acceso programático y registrar los cambios relevantes como «cambios de propiedad o de metodología» de la ficha |
| Crossref / OpenAlex | Para las entradas académicas (RF-0008 a RF-0012): comprobar citas normalizadas, versiones y metadatos antes de dar por buena una referencia localizada |
| Retraction Watch Database (retractionwatch.com) | Comprobación de retractaciones en los trabajos académicos usados como fuente de las entradas de investigación |
