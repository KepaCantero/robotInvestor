# Archivo operativo F9 — Registro de Fuentes para el Analizador de Tendencias de Inversión

**Bloque A · Robot Investor · Versión óptima V4.0 · 01/11/2026** · Subordinado al Documento 0 óptima V5.0.

**Versión del archivo:** V3.2 (01/11/2026), alineada con el Documento 0 óptima V5.0 · **Código:** F9 · **Propietario:** AG-16 Buscador de Fuentes Avanzadas (BFA)

## Cómo usar este archivo

**Propósito.** Registro de fuentes de opinión, actualidad, datos de mercado, posicionamiento, grandes inversores, regulación y redes con filtro de calidad (Documento 0, 5.1 y 13.1). No contiene literatura académica de dominio (F7) ni métodos de cálculo (F8).

**Propietario y acceso.** Escribe solo AG-16 (BFA). Leen: agentes del plano P2, AG-14, Orquestador, Auditor y Evaluador (este último mide el historial de exactitud de cada fuente). Cualquier otro acceso es una incidencia (Documento 0, 5.2).

**Reglas de uso.**

1. **Lectura.** Lea primero «Novedades»; después el índice de temáticas; dentro de la temática, las fichas aparecen **ordenadas por Q descendente** (a igualdad, la más reciente primero). Cite siempre el ID de la ficha. Para corroboración (PS1) solo cuentan fichas de nivel A o B con `Estado del enlace` distinto de `ROTO`; una ficha `PENDIENTE_VERIFICACION_ALTA` no sustenta evidencia hasta que su propietario la confirme.
2. **Calidad.** Q (0–100) con la rúbrica de fuentes de opinión y actualidad (13.3): Primariedad 20 · Historial de exactitud medido por el Evaluador 20 (neutro 10 mientras no haya pronósticos resueltos) · Transparencia de método y conflictos 15 · Autoridad 15 · Independencia 10 · Actualidad 10 · Accesibilidad 10. Niveles: A (Q ≥ 80), B (65–79), C (50–64), D (< 50: candidata a baja salvo que sea la única fuente de un dato necesario, declarado). En las semillas la Q es provisional hasta la verificación de alta.
3. **Estados del enlace** (HT-02, barrido semanal del domingo): `OK`, `REDIRIGIDO`, `ROTO` (4xx/5xx en dos intentos separados 24 h), `MURO_PAGO`, `CONTENIDO_CAMBIADO` (similitud < 0,8 frente a la copia archivada) y `PENDIENTE_BARRIDO` (estado inicial de esta versión: ningún enlace se ha comprobado aún con HT-02). `Última verificación` recoge la última comprobación documentada, no una del barrido.
4. **Acciones** (potestad plena del propietario, R19): `REPARAR` (DOI, nueva URL oficial o copia archivada; obligatoria cuando la ficha lleva «Alerta»); `DEGRADAR` (bajar Q o nivel, con motivo); `BORRAR` cuando haya enlace roto sin alternativa tras dos barridos, contenido retirado o retractado, falsedad o manipulación demostrada, redundancia total con una ficha de mayor Q, o Q < 50 sin uso en 180 días. Cada borrado añade una línea al «Registro de bajas»; si la ficha sustentaba EVD de F2 se avisa al Curador (CT-11, tipo `fuente_retirada`).
5. **Ciclo.** BFA alimenta el registro por su agenda de vigilancia y por las peticiones de búsqueda (CT-07); antes de buscar aplica el Fondo metodológico (R20), en especial los criterios de credibilidad (lectura lateral). Mensualmente el propietario informa al Orquestador de altas, reparaciones, bajas, salud de enlaces y lagunas (CT-21). Los IDs son inmutables y no se reutilizan; en el «Registro de bajas», «REF-id» es el ID propio de la ficha.

**Reglas propias de F9.** (a) Una fuente de opinión nunca prueba un hecho: los hechos se citan en su fuente primaria. (b) Las copias sindicadas enlazan a su raíz y no cuentan como fuentes independientes. (c) Las fuentes de acceso restringido solo se usan por sus contenidos públicos citables; las credenciales viven en HT-01, nunca en este archivo. (d) Las «piezas» (series, informes o artículos concretos) se registran bajo su fuente y heredan su temática y calidad salvo anotación. (e) Las semillas (`PENDIENTE_VERIFICACION_ALTA`) no sustentan evidencia hasta su confirmación.

## Índice de temáticas (Anexo D, TF-)

| Código | Temática | Referencias | Verificadas | Pendientes de verificación | A | B | C | D | Q medio |
|---|---|---|---|---|---|---|---|---|---|
| TF-01 | Bancos centrales, organismos internacionales y estadísticas oficiales | 20 | 20 | 0 | 19 | 1 | 0 | 0 | 86,3 |
| TF-02 | Reguladores, registros públicos y documentación corporativa | 20 | 20 | 0 | 19 | 1 | 0 | 0 | 83,3 |
| TF-03 | Prensa financiera y agencias de noticias | 21 | 20 | 1 | 0 | 12 | 9 | 0 | 64,8 |
| TF-04 | Grandes inversores, gestoras y cartas de inversión | 20 | 20 | 0 | 3 | 15 | 2 | 0 | 72,5 |
| TF-05 | Análisis de bancos de inversión y casas de análisis | 20 | 20 | 0 | 1 | 17 | 2 | 0 | 70,3 |
| TF-06 | Datos de mercado, posicionamiento y flujos | 20 | 20 | 0 | 14 | 4 | 2 | 0 | 77,5 |
| TF-07 | Fuentes sectoriales y de industria | 20 | 20 | 0 | 5 | 14 | 1 | 0 | 76,0 |
| TF-08 | Materias primas y energía (agencias y datos) | 21 | 21 | 0 | 15 | 6 | 0 | 0 | 80,6 |
| TF-09 | Inmobiliario (índices y datos) | 20 | 20 | 0 | 11 | 9 | 0 | 0 | 80,2 |
| TF-10 | Cripto: datos en cadena, investigación y noticias | 20 | 20 | 0 | 4 | 14 | 2 | 0 | 72,5 |
| TF-11 | Mercados privados y alternativos (datos e índices) | 20 | 20 | 0 | 2 | 16 | 2 | 0 | 71,1 |
| TF-12 | Redes sociales y foros con filtro de calidad | 20 | 20 | 0 | 0 | 11 | 7 | 2 | 64,6 |
| TF-13 | Repositorios académicos y de investigación abierta | 20 | 20 | 0 | 9 | 11 | 0 | 0 | 79,1 |
| TF-14 | Think tanks y prospectiva | 25 | 25 | 0 | 2 | 22 | 1 | 0 | 73,3 |
| TF-15 | Proveedores de índices y metodologías | 20 | 20 | 0 | 11 | 9 | 0 | 0 | 78,2 |
| TF-16 | Fondos y ETF: datos, flujos y categorías | 20 | 20 | 0 | 3 | 16 | 1 | 0 | 72,0 |
| TF-17 | Derivados y volatilidad: mercados y datos | 21 | 21 | 0 | 9 | 12 | 0 | 0 | 78,3 |
| TF-18 | Mercado monetario y tipos a corto plazo | 21 | 21 | 0 | 18 | 3 | 0 | 0 | 84,0 |
| TF-19 | Curvas de tipos, crédito e inflación implícita: datos | 20 | 20 | 0 | 15 | 5 | 0 | 0 | 81,5 |
| **Total** | — | **389** | **388** | 1 | 160 | 198 | 29 | 2 | 76,1 |

«Verificadas»: enlace en estado OK, REDIRIGIDO, MURO_PAGO o VERIFICADO_BUSQUEDA (existencia y datos confirmados por búsqueda web el 02/11/2026), o verificación documental completa en una carga anterior (25–26/10/2026), pendiente solo del barrido automático HT-02. «Pendientes»: semillas aún en PENDIENTE_VERIFICACION_ALTA o fichas con alerta sin resolver.

## Novedades

Sección de difusión semanal (Documento 0, 6.1): el propietario anota aquí las altas, reparaciones, degradaciones y bajas de la semana; los agentes lectores la consultan al inicio de cada encargo mediante HT-06. Se conservan las cuatro últimas semanas; lo anterior queda en el historial del archivo.

| Semana (lunes) | Tipo | ID | Temática | Resumen (una línea) |
|---|---|---|---|---|

Tipos admitidos: `ALTA`, `REPARACION`, `DEGRADACION`, `RECALIFICACION`, `BAJA`, `VERIFICACION_ALTA` (semilla confirmada o rechazada).

## TF-01 Bancos centrales, organismos internacionales y estadísticas oficiales

#### RF-0003 · Q 89 (A) — BIS (Bank for International Settlements), sección de estadísticas

- **Canal oficial:** bis.org/statistics/
- **Documentación y notas:** Portal de datos vigente: data.bis.org · Serie de crédito total de la pieza 4.3: bis.org/statistics/totcredit.htm
- **Temática:** TF-01 Bancos centrales, organismos internacionales y estadísticas oficiales (principal)
- **Calidad Q:** 89 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 15/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 9/10 · Acceso 10/10
- **Nivel de fiabilidad en V2.4:** A
- **Tipología:** primaria
- **Motivo de inclusión:** Estadísticas internacionales de referencia en banca central: crédito, tipos de cambio efectivos, derivados de OTC y deuda global
- **Ámbitos:** Crédito global; banca central; deuda; derivados de OTC; mercados de divisas
- **Restricciones de uso:** Uso libre con atribución; citar la base estadística concreta y la fecha de extracción
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Sesgos posibles:** Ninguno editorial conocido; cobertura centrada en bancos centrales miembros
- **Cambios de propiedad o de metodología:** Sin cambios conocidos; el BIS revisa metodologías de sus bases periódicamente (vigilar notas de las series)
- **Estado:** Aprobada
- **Estado del enlace:** PENDIENTE_BARRIDO
- **Última verificación:** 2026-10-25 (Completa (URL viva y naturaleza del contenido comprobadas el 25/10/2026))

##### Pieza RF-0003/P1 — Estadísticas de crédito del BIS

- **Pieza y URL:** BIS · «Credit to the non-financial sector» · bis.org/statistics/totcredit.htm
- **Tipo de medio:** Base estadística oficial
- **Responsable:** Bank for International Settlements
- **Temática y Calidad:** heredadas de RF-0003 (TF-01, Q 89, nivel A); calidad de la pieza en V2.4: Alta
- **Fechas:** Publicación: No aplicable (base trimestral de actualización continua) · Datos: Variable: último trimestre declarado por la base en la fecha de consulta · Consulta: 2026-10-25
- **Metodología declarada:** Sí: notas metodológicas de las series de crédito al sector no financiero
- **Naturaleza:** Hecho (serie estadística oficial)
- **Temáticas y ámbitos:** Crédito total y privado; apalancamiento macro; ciclos de crédito por país
- **Limitaciones:** Cobertura por países participantes; revisiones de metodología del BIS documentadas en sus notas
- **Conflictos de interés:** Ninguno conocido; sin sindicación (syndicated_of: no aplicable, fuente primaria)
- **Restricciones de uso:** Uso con atribución; citar base, país, serie y trimestre
- **Estado:** Aprobada
- **Estado del enlace:** PENDIENTE_BARRIDO
- **Última verificación:** 2026-10-25

#### RF-0004 · Q 89 (A) — BCE Data Portal (Banco Central Europeo)

- **Canal oficial:** data.ecb.europa.eu
- **Documentación y notas:** Descargas, metadatos SDMX y documentación desde el propio portal · Citar la serie con su clave SDMX y la fecha de consulta
- **Temática:** TF-01 Bancos centrales, organismos internacionales y estadísticas oficiales (principal)
- **Calidad Q:** 89 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 15/15 · Autoridad 15/15 · Independencia 9/10 · Actualidad 10/10 · Acceso 10/10
- **Nivel de fiabilidad en V2.4:** A
- **Tipología:** primaria
- **Motivo de inclusión:** Fuente oficial de datos de la eurozona: tipos, agregados monetarios, inflación HICP y balanza de pagos, con API pública
- **Ámbitos:** Eurozona; tipos de cambio; política monetaria; inflación HICP; agregados monetarios
- **Restricciones de uso:** Datos públicos con atribución; citar la serie de la base SDW y su fecha
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Sesgos posibles:** Ninguno; cobertura eurozona
- **Cambios de propiedad o de metodología:** Portal nuevo (sucesor del SDW clásico): vigilar reorganizaciones de series
- **Estado:** Aprobada
- **Estado del enlace:** PENDIENTE_BARRIDO
- **Última verificación:** 2026-10-25 (Completa (URL viva y naturaleza del contenido comprobadas el 25/10/2026))

#### RF-0015 · Q 89 (A) — ALFRED (Archival FRED)

- **Canal oficial (URL raíz):** https://alfred.stlouisfed.org/ (ayuda: https://alfred.stlouisfed.org/help)
- **Emisor:** Federal Reserve Bank of St. Louis (Research Division)
- **Temática:** TF-01 Bancos centrales, organismos internacionales y estadísticas oficiales (principal) · secundarias: TF-06
- **Calidad Q:** 89 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 15/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 9/10 · Acceso 10/10
- **Tipología:** primaria
- **Acceso:** Abierto (condiciones en fred.stlouisfed.org/legal/)
- **Ámbitos:** Vintages (versiones históricas) de series macro de EE. UU. con fechas de publicación
- **Motivo de inclusión y uso:** Muestra el dato tal como estaba disponible en cada fecha; la St. Louis Fed añade observaciones nuevas y revisadas normalmente en un día hábil y contrasta los vintages con la fuente original. Uso: backtests sin sesgo de anticipación y resolución de pronósticos con el dato de su momento (Evaluador, Motor de Cálculo).
- **Sesgos y cautelas:** Cobertura de series menor que FRED; algunos vintages se reconstruyen con servicios de terceros cuando la fuente no conserva estimaciones pasadas.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «ALFRED Archival Federal Reserve Economic Data vintage St. Louis Fed»; WebFetch: sí)
- **Origen:** Semilla V3.0 (2026-11-01) confirmada en verificación de alta 2026-11-02.

#### RF-0022 · Q 89 (A) — U.S. Bureau of Labor Statistics (BLS)

- **Canal oficial (URL raíz):** https://www.bls.gov/ (sala de prensa y calendario: https://www.bls.gov/newsroom/home.htm)
- **Emisor:** U.S. Department of Labor
- **Temática:** TF-01 Bancos centrales, organismos internacionales y estadísticas oficiales (principal)
- **Calidad Q:** 89 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 15/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 9/10 · Acceso 10/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** IPC, IPP, empleo (Employment Situation), JOLTS, salarios reales, productividad de EE. UU.
- **Motivo de inclusión y uso:** Publicador original de IPC y nóminas; su sala de prensa fija fecha y hora de cada publicación (p. ej., Employment Situation 6/11/2026 y CPI 10/11/2026, 8:30 ET). Uso: calendario de catalizadores y dato primario para inflación y mercado laboral.
- **Sesgos y cautelas:** Revisiones mensuales y anuales; cambios metodológicos documentados; calendario alterable por cierres administrativos (publica fechas revisadas).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «U.S. Bureau of Labor Statistics official site CPI employment situation»; WebFetch: sí)
- **Origen:** Semilla V3.0 (2026-11-01) confirmada en verificación de alta 2026-11-02.

#### RF-0023 · Q 89 (A) — U.S. Bureau of Economic Analysis (BEA)

- **Canal oficial (URL raíz):** https://www.bea.gov/ (renta y ahorro: https://www.bea.gov/taxonomy/term/1071)
- **Emisor:** U.S. Department of Commerce
- **Temática:** TF-01 Bancos centrales, organismos internacionales y estadísticas oficiales (principal)
- **Calidad Q:** 89 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 15/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 9/10 · Acceso 10/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** PIB, renta y gasto personal (PCE), tasa de ahorro, balanza de pagos, renta estatal de EE. UU.
- **Motivo de inclusión y uso:** Publicador original de las cuentas nacionales de EE. UU. y del deflactor PCE (objetivo de inflación de la Fed). Desde 2026 publica renta y gasto personal junto con las estimaciones del PIB. Uso: dato primario de crecimiento e inflación PCE.
- **Sesgos y cautelas:** Revisiones sustanciales del PIB entre estimaciones; calendario reprogramado en 2025–2026 (verificar fecha en el aviso de la BEA).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «U.S. Bureau of Economic Analysis GDP personal income outlays bea.gov»; WebFetch: sí)
- **Origen:** Semilla V3.0 (2026-11-01) confirmada en verificación de alta 2026-11-02.

#### RF-0001 · Q 88 (A) — FRED (Federal Reserve Economic Data, Banco de la Reserva Federal de San Luis)

- **Canal oficial:** fred.stlouisfed.org
- **Documentación y notas:** Documentación de la API: fred.stlouisfed.org/docs/api/fred/ · Cada serie declara su fuente original y metodología en sus metadatos (p. ej. la serie CPIAUCSL de la pieza 4.3: fred.stlouisfed.org/series/CPIAUCSL)
- **Temática:** TF-01 Bancos centrales, organismos internacionales y estadísticas oficiales (principal) · secundarias: TF-06
- **Calidad Q:** 88 (A) — Primariedad 18/20 · Historial 10/20 · Transparencia 15/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 10/10 · Acceso 10/10
- **Nivel de fiabilidad en V2.4:** A
- **Tipología:** primaria (hospeda series de los emisores oficiales)
- **Motivo de inclusión:** Portal de datos oficiales más completo para series macroeconómicas y financieras de Estados Unidos, con metadatos de fuente y metodología por serie
- **Ámbitos:** Macroeconomía; precios e inflación; tipos de interés; mercado laboral; indicadores de recesión; renta variable a nivel agregado
- **Restricciones de uso:** Uso académico y de referencia; citar la serie concreta y la fuente original que FRED declara en sus metadatos
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Sesgos posibles:** Ninguno editorial conocido; posible sesgo de cobertura hacia series estadounidenses
- **Cambios de propiedad o de metodología:** Sin cambios conocidos; mantiene el hosting del Fed de San Luis; verificar en cada mantenimiento
- **Estado:** Aprobada
- **Estado del enlace:** PENDIENTE_BARRIDO
- **Última verificación:** 2026-10-25 (Completa (URL viva y naturaleza del contenido comprobadas el 25/10/2026))

##### Pieza RF-0001/P1 — Serie CPIAUCSL de FRED

- **Pieza y URL:** FRED · Serie CPIAUCSL «Consumer Price Index for All Urban Consumers: All Items in U.S. City Average» · fred.stlouisfed.org/series/CPIAUCSL
- **Tipo de medio:** Serie de datos oficial
- **Responsable:** U.S. Bureau of Labor Statistics (compilación y hospedaje: Banco de la Reserva Federal de San Luis)
- **Temática y Calidad:** heredadas de RF-0001 (TF-01, Q 88, nivel A); calidad de la pieza en V2.4: Alta
- **Fechas:** Publicación: No aplicable (serie continua con actualización mensual) · Datos: Variable: la última observación disponible es la que declara la propia serie en la fecha de consulta · Consulta: 2026-10-25
- **Metodología declarada:** Sí: el BLS publica la metodología del IPC y FRED enlaza la fuente original y las notas de la serie
- **Naturaleza:** Hecho (serie estadística oficial)
- **Temáticas y ámbitos:** Inflación de Estados Unidos; tipos de interés reales; contexto macro del ciclo
- **Limitaciones:** Dato revisado y reajustable; definición de «todos los bienes urbanos» acotada al ámbito de consumo estadounidense
- **Conflictos de interés:** Ninguno conocido; sin sindicación (syndicated_of: no aplicable, fuente primaria)
- **Restricciones de uso:** Citar la serie por su identificador, la fecha de consulta y la fuente original declarada por FRED
- **Estado:** Aprobada
- **Estado del enlace:** PENDIENTE_BARRIDO
- **Última verificación:** 2026-10-25

#### RF-0016 · Q 88 (A) — Federal Reserve Board (comunicados, actas del FOMC, discursos, proyecciones SEP)

- **Canal oficial (URL raíz):** https://www.federalreserve.gov/ (calendario, comunicados y actas del FOMC: https://federalreserve.gov/monetarypolicy/fomccalendars.htm)
- **Emisor:** Board of Governors of the Federal Reserve System
- **Temática:** TF-01 Bancos centrales, organismos internacionales y estadísticas oficiales (principal)
- **Calidad Q:** 88 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 15/15 · Autoridad 15/15 · Independencia 9/10 · Actualidad 10/10 · Acceso 9/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** Política monetaria de EE. UU.: calendario del FOMC, comunicados, actas, conferencias de prensa, Summary of Economic Projections (marzo, junio, septiembre, diciembre)
- **Motivo de inclusión y uso:** Fuente original de las decisiones de tipos y de las proyecciones del FOMC (próxima reunión con SEP: 8–9/12/2026). Uso: catalizadores de calendario y lectura de la función de reacción de la Fed.
- **Sesgos y cautelas:** Comunicación con orientación de política (no neutral sobre su propia actuación); las actas se publican tres semanas después.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Federal Reserve Board FOMC meeting calendars statements minutes»; WebFetch: sí)
- **Origen:** Semilla V3.0 (2026-11-01) confirmada en verificación de alta 2026-11-02.

#### RF-0017 · Q 88 (A) — Banco Central Europeo (decisiones, cuentas de política monetaria, discursos, proyecciones)

- **Canal oficial (URL raíz):** https://www.ecb.europa.eu/ (decisiones del Consejo de Gobierno: https://www.ecb.europa.eu/press/govcdec)
- **Emisor:** Banco Central Europeo
- **Temática:** TF-01 Bancos centrales, organismos internacionales y estadísticas oficiales (principal)
- **Calidad Q:** 88 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 15/15 · Autoridad 15/15 · Independencia 9/10 · Actualidad 10/10 · Acceso 9/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** Política monetaria de la eurozona: decisiones de tipos (14:15 CET), declaración y preguntas de la conferencia de prensa, cuentas de la reunión (4 semanas después), otras decisiones (supervisión, estabilidad financiera, estadísticas)
- **Motivo de inclusión y uso:** Fuente original de las decisiones del BCE (última conferencia registrada: 29/10/2026). Uso: catalizadores y lectura de la orientación de política monetaria del área del euro.
- **Sesgos y cautelas:** Comunicación con orientación de política; los metadatos de algunas páginas no reflejan la fecha real del contenido.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «European Central Bank monetary policy decisions accounts ecb.europa.eu»; WebFetch: sí)
- **Origen:** Semilla V3.0 (2026-11-01) confirmada en verificación de alta 2026-11-02.

#### RF-0021 · Q 88 (A) — Eurostat

- **Canal oficial (URL raíz):** https://ec.europa.eu/eurostat (guía del sitio: https://ec.europa.eu/eurostat/en/help/website-guide)
- **Emisor:** Comisión Europea — Oficina Estadística de la Unión Europea
- **Temática:** TF-01 Bancos centrales, organismos internacionales y estadísticas oficiales (principal)
- **Calidad Q:** 88 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 15/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 8/10 · Acceso 10/10
- **Tipología:** primaria
- **Acceso:** Abierto (acceso gratuito a todas sus bases de datos)
- **Ámbitos:** IPCA (HICP), PIB, empleo, comercio, finanzas públicas de la UE; calendario de publicaciones y «euro indicators»
- **Motivo de inclusión y uso:** Estadística oficial armonizada de la UE con calendario de publicaciones y notas «euro indicators» de los principales indicadores mensuales y trimestrales. Uso: dato primario macro europeo y comparaciones entre países.
- **Sesgos y cautelas:** Datos agregados a partir de institutos nacionales; revisiones y desfases según país.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Eurostat official website European statistics database»; WebFetch: sí)
- **Origen:** Semilla V3.0 (2026-11-01) confirmada en verificación de alta 2026-11-02.

#### RF-0005 · Q 87 (A) — World Bank Open Data (Banco Mundial)

- **Canal oficial:** data.worldbank.org
- **Documentación y notas:** Documentación de API: datahelpdesk.worldbank.org · Indicador de la pieza 4.3: data.worldbank.org/indicator/NY.GDP.MKTP.CD
- **Temática:** TF-01 Bancos centrales, organismos internacionales y estadísticas oficiales (principal)
- **Calidad Q:** 87 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 15/15 · Autoridad 15/15 · Independencia 9/10 · Actualidad 8/10 · Acceso 10/10
- **Nivel de fiabilidad en V2.4:** A
- **Tipología:** primaria
- **Motivo de inclusión:** Indicadores macro globales comparables (PIB, población, desarrollo) con metodología documentada y acceso API
- **Ámbitos:** Macroeconomía global; desarrollo; indicadores por país; comparaciones internacionales
- **Restricciones de uso:** CC BY 4.0 en general; citar indicador (código), país y año
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Sesgos posibles:** Revisión retrospectiva de datos nacionales; desfase de publicación de un año en varios indicadores
- **Cambios de propiedad o de metodología:** Sin cambios conocidos; las series se revisan con las actualizaciones anuales del World Development Indicators
- **Estado:** Aprobada
- **Estado del enlace:** PENDIENTE_BARRIDO
- **Última verificación:** 2026-10-25 (Completa (URL viva y naturaleza del contenido comprobadas el 25/10/2026))

##### Pieza RF-0005/P1 — Indicador NY.GDP.MKTP.CD del Banco Mundial

- **Pieza y URL:** World Bank Open Data · Indicador NY.GDP.MKTP.CD «GDP (current US$)» · data.worldbank.org/indicator/NY.GDP.MKTP.CD
- **Tipo de medio:** Serie de datos oficial
- **Responsable:** Banco Mundial (datos compilados de cuentas nacionales de los países miembros y de la OCDE)
- **Temática y Calidad:** heredadas de RF-0005 (TF-01, Q 87, nivel A); calidad de la pieza en V2.4: Alta
- **Fechas:** Publicación: No aplicable (serie anual con actualización en la edición anual del World Development Indicators) · Datos: Variable por país; la serie declara el último año disponible en la fecha de consulta · Consulta: 2026-10-25
- **Metodología declarada:** Sí: notas metodológicas por indicador y fuentes nacionales declaradas
- **Naturaleza:** Hecho (serie estadística oficial)
- **Temáticas y ámbitos:** PIB nominal en dólares; comparaciones internacionales; tamaño de mercado por país
- **Limitaciones:** Reajustes retrospectivos; conversiones a dólares corrientes sensibles al tipo de cambio; desfase de un año en la publicación
- **Conflictos de interés:** Ninguno conocido; sin sindicación (syndicated_of: no aplicable, fuente primaria)
- **Restricciones de uso:** Licencia CC BY 4.0 en general; citar código de indicador, país, año y fecha de consulta
- **Estado:** Aprobada
- **Estado del enlace:** PENDIENTE_BARRIDO
- **Última verificación:** 2026-10-25

#### RF-0006 · Q 87 (A) — OECD Data (Organización para la Cooperación y el Desarrollo Económicos)

- **Canal oficial:** data-explorer.oecd.org (portal vigente)
- **Documentación y notas:** Con documentación de API y límites de descarga en el propio portal · Los antiguos data.oecd.org redirigen al portal actual (nota ya anotada en la ficha: revalidar en el primer mantenimiento)
- **Temática:** TF-01 Bancos centrales, organismos internacionales y estadísticas oficiales (principal)
- **Calidad Q:** 87 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 15/15 · Autoridad 15/15 · Independencia 9/10 · Actualidad 9/10 · Acceso 9/10
- **Nivel de fiabilidad en V2.4:** A
- **Tipología:** primaria
- **Motivo de inclusión:** Indicadores comparables de países OCDE (crecimiento, empleo, precios, comercio) con notas metodológicas editoriales
- **Ámbitos:** Países OCDE; empleo; comercio; industria; política económica comparada
- **Restricciones de uso:** Condiciones de uso del portal; citar indicador y país
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Sesgos posibles:** Cobertura OCDE; los antiguos data.oecd.org redirigen al portal vigente (oecd.org)
- **Cambios de propiedad o de metodología:** Migración de portal (data.oecd.org → oecd.org): revalidar URLs en el primer mantenimiento
- **Estado:** Aprobada
- **Estado del enlace:** PENDIENTE_BARRIDO
- **Última verificación:** 2026-10-25 (Completa (URL viva y naturaleza del contenido comprobadas el 25/10/2026))
- **Alerta:** Los antiguos data.oecd.org redirigen al portal data-explorer.oecd.org: revalidar en el primer barrido.

#### RF-0018 · Q 87 (A) — Banco de España (informes, boletín económico, estadísticas)

- **Canal oficial (URL raíz):** https://www.bde.es/ (Boletín Económico: https://www.bde.es/bde/es/secciones/informes/analisis-economico-e-investigacion/boletin-economico/ · Boletín Estadístico: https://www.bde.es/wbe/es/publicaciones/informacion-estadistica/boletin-estadistico/)
- **Emisor:** Banco de España
- **Temática:** TF-01 Bancos centrales, organismos internacionales y estadísticas oficiales (principal)
- **Calidad Q:** 87 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 9/10 · Actualidad 9/10 · Acceso 10/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** Economía española; proyecciones macroeconómicas; Informe Anual; estabilidad financiera; Boletín Estadístico; repositorio institucional (repositorio.bde.es)
- **Motivo de inclusión y uso:** Fuente oficial del análisis de coyuntura y de las estadísticas monetarias y financieras de España. Uso: dato primario y diagnóstico oficial para la economía y el sistema financiero españoles.
- **Sesgos y cautelas:** Perspectiva institucional del Eurosistema; algunos enlaces internos del portal (p. ej., «Notas Económicas») apuntaban a anclas rotas en la fecha de consulta.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Banco de España Boletín Económico informes estadísticas bde.es»; WebFetch: sí)
- **Origen:** Semilla V3.0 (2026-11-01) confirmada en verificación de alta 2026-11-02.

#### RF-0019 · Q 87 (A) — Bank of England (Monetary Policy Report, actas del MPC)

- **Canal oficial (URL raíz):** https://www.bankofengland.co.uk/ (índice del Monetary Policy Report: https://www.bankofengland.co.uk/sitemap/monetary-policy-report · ejemplo: https://www.bankofengland.co.uk/monetary-policy-report/2026/july-2026)
- **Emisor:** Bank of England
- **Temática:** TF-01 Bancos centrales, organismos internacionales y estadísticas oficiales (principal)
- **Calidad Q:** 87 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 15/15 · Autoridad 15/15 · Independencia 9/10 · Actualidad 9/10 · Acceso 9/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** Política monetaria del Reino Unido: Monetary Policy Report trimestral, Monetary Policy Summary y actas del MPC con votaciones individuales, calendario de reuniones 2026–2027
- **Motivo de inclusión y uso:** Fuente original de las decisiones y proyecciones del MPC (p. ej., MPR de julio de 2026: Bank Rate al 3,75 % con votación 6–3). Uso: catalizadores de libra y gilts; reparto de votos como señal adelantada.
- **Sesgos y cautelas:** Comunicación con orientación de política; documentos extensos (leer resumen y actas).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «bankofengland.co.uk monetary-policy-report 2026»; WebFetch: sí)
- **Origen:** Semilla V3.0 (2026-11-01) confirmada en verificación de alta 2026-11-02.

#### RF-0200 · Q 87 (A) — BIS — Central bankers' speeches (discursos de banqueros centrales)

- **Canal oficial (URL raíz):** https://www.bis.org/ (ejemplo de la colección: https://www.bis.org/speeches/20251010-japans-economy-and-monetary-policy · archivo histórico: https://www.bis.org/review/)
- **Emisor:** Bank for International Settlements
- **Temática:** TF-01 Bancos centrales, organismos internacionales y estadísticas oficiales (principal)
- **Calidad Q:** 87 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 15/15 · Independencia 9/10 · Actualidad 10/10 · Acceso 10/10
- **Tipología:** primaria (textos de los propios banqueros centrales)
- **Acceso:** Abierto
- **Ámbitos:** Discursos de gobernadores y miembros de consejos de bancos centrales de todo el mundo, en un único repositorio
- **Motivo de inclusión y uso:** Agrega en un solo canal los discursos de banqueros centrales (p. ej., Kazuo Ueda, BoJ, 10/10/2025), separado de los discursos de la dirección del BIS. Uso: seguimiento de la comunicación de bancos centrales sin cobertura propia en F9 (orientación futura, tono).
- **Sesgos y cautelas:** Es un agregador oficial: citar el discurso con su banco central emisor; los textos reflejan la visión de cada orador.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Bank of Japan Outlook for Economic Activity and Prices statements on monetary policy boj.or.jp»; WebFetch: sí)
- **Origen:** Alta 2026-11-02 (F9_S1).

#### RF-0007 · Q 85 (A) — IMF Data (Fondo Monetario Internacional)

- **Canal oficial:** data.imf.org
- **Documentación y notas:** Nota de verificación: el punto de acceso SDMX histórico (dataservices.imf.org) quedó retirado en 2025; el acceso vigente es el propio portal data.imf.org. Revalidar esta entrada en el primer mantenimiento
- **Temática:** TF-01 Bancos centrales, organismos internacionales y estadísticas oficiales (principal)
- **Calidad Q:** 85 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 15/15 · Autoridad 15/15 · Independencia 9/10 · Actualidad 9/10 · Acceso 7/10
- **Nivel de fiabilidad en V2.4:** A
- **Tipología:** primaria
- **Motivo de inclusión:** Bases de datos oficiales del FMI (Perspectivas de la Economía Mundial, estadísticas financieras internacionales, servicios y prerrogativas de los países miembros)
- **Ámbitos:** Macroeconomía global; balanza de pagos; reservas; estabilidad financiera
- **Restricciones de uso:** Condiciones del portal del FMI; citar base, serie y edición (los datos de proyección cambian por edición)
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Sesgos posibles:** Las proyecciones WEO son estimaciones del FMI, no hechos: tratarlas como previsión
- **Cambios de propiedad o de metodología:** Ediciones WEO semestrales: anotar siempre la edición usada
- **Estado:** Aprobada
- **Estado del enlace:** PENDIENTE_BARRIDO
- **Última verificación:** 2026-10-25 (Completa (URL viva y naturaleza del contenido comprobadas el 25/10/2026))
- **Alerta:** El punto de acceso SDMX histórico (dataservices.imf.org) se retiró en 2025; el acceso vigente es data.imf.org: revalidar.

#### RF-0020 · Q 85 (A) — Bank of Japan (declaraciones de política, Outlook Report)

- **Canal oficial (URL raíz):** https://www.boj.or.jp/en/ (Outlook for Economic Activity and Prices: https://www.boj.or.jp/en/mopo/outlook/index.htm)
- **Emisor:** Bank of Japan
- **Temática:** TF-01 Bancos centrales, organismos internacionales y estadísticas oficiales (principal)
- **Calidad Q:** 85 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 9/10 · Actualidad 9/10 · Acceso 8/10
- **Tipología:** primaria
- **Acceso:** Abierto (versión inglesa con cierto desfase respecto a la japonesa)
- **Ámbitos:** Política monetaria de Japón; Outlook Report trimestral (último: «The Bank's View», 30/10/2026); declaraciones de política
- **Motivo de inclusión y uso:** Fuente original de decisiones y previsiones del BoJ, clave para yen, JGB y carry trade. Uso: catalizadores de calendario y lectura de la normalización monetaria japonesa.
- **Sesgos y cautelas:** El texto completo del Outlook se publica días después de «The Bank's View»; traducciones al inglés con retraso.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Bank of Japan Outlook for Economic Activity and Prices statements on monetary policy boj.or.jp»; WebFetch: sí)
- **Origen:** Semilla V3.0 (2026-11-01) confirmada en verificación de alta 2026-11-02.

#### RF-0024 · Q 83 (A) — FMI — World Economic Outlook y blog del FMI

- **Canal oficial (URL raíz):** https://www.imf.org/en/publications/weo (edición vigente: https://www.imf.org/en/publications/weo/issues/2026/10/13/world-economic-outlook-october-2026)
- **Emisor:** Fondo Monetario Internacional
- **Temática:** TF-01 Bancos centrales, organismos internacionales y estadísticas oficiales (principal) · secundarias: TF-14
- **Calidad Q:** 83 (A) — Primariedad 16/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 9/10 · Actualidad 9/10 · Acceso 10/10
- **Tipología:** primaria (previsiones propias del organismo)
- **Acceso:** Abierto
- **Ámbitos:** Previsiones macro mundiales y por país (abril y octubre, con actualizaciones en enero y julio); base de datos del WEO
- **Motivo de inclusión y uso:** Escenario central de referencia del sector oficial (WEO de octubre de 2026, «Resilience Under Strain, Urgent Choices»: crecimiento mundial 3,1 % en 2026 y 3,4 % en 2027). Uso: ancla de consenso oficial frente a la que medir escenarios propios.
- **Sesgos y cautelas:** Previsiones, no hechos; sesgo histórico hacia la continuidad; el blog del FMI expresa opiniones del personal.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «IMF World Economic Outlook October 2026»; WebFetch: sí)
- **Origen:** Semilla V3.0 (2026-11-01) confirmada en verificación de alta 2026-11-02; URL raíz corregida (minúsculas en la ruta vigente).

#### RF-0025 · Q 83 (A) — Liberty Street Economics (blog del Federal Reserve Bank of New York)

- **Canal oficial (URL raíz):** https://libertystreeteconomics.newyorkfed.org/
- **Emisor:** Federal Reserve Bank of New York (economistas del Research and Statistics Group)
- **Temática:** TF-01 Bancos centrales, organismos internacionales y estadísticas oficiales (principal) · secundarias: TF-13
- **Calidad Q:** 83 (A) — Primariedad 16/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 14/15 · Independencia 9/10 · Actualidad 10/10 · Acceso 10/10
- **Tipología:** secundaria cualificada (análisis de economistas de banco central)
- **Acceso:** Abierto
- **Ámbitos:** Mercados financieros, crédito de hogares, mercados monetarios, inflación, estabilidad financiera
- **Motivo de inclusión y uso:** Blog del NY Fed (desde 2011) con análisis basados en datos propios. Uso: interpretación de mercados monetarios y crédito por economistas del sistema Fed.
- **Sesgos y cautelas:** Aviso expreso: las opiniones son de los autores, no posición oficial del NY Fed ni del Sistema.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Liberty Street Economics Federal Reserve Bank of New York blog»; WebFetch: sí)
- **Origen:** Semilla V3.0 (2026-11-01) confirmada en verificación de alta 2026-11-02.

#### RF-0201 · Q 82 (A) — FRASER (Federal Reserve Archival System for Economic Research)

- **Canal oficial (URL raíz):** https://fraser.stlouisfed.org/
- **Emisor:** Federal Reserve Bank of St. Louis
- **Temática:** TF-01 Bancos centrales, organismos internacionales y estadísticas oficiales (principal) · secundarias: TF-13
- **Calidad Q:** 82 (A) — Primariedad 18/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 14/15 · Independencia 10/10 · Actualidad 6/10 · Acceso 10/10
- **Tipología:** primaria (documentos históricos digitalizados)
- **Acceso:** Abierto (búsqueda a texto completo, API REST y OAI-PMH)
- **Ámbitos:** Historia financiera, económica y bancaria de EE. UU.: publicaciones estadísticas históricas, documentos de la Fed, colecciones de archivo
- **Motivo de inclusión y uso:** Archivo digital de documentos y estadísticas históricas (p. ej., ediciones antiguas de publicaciones de la Fed). Uso: reconstruir series largas, analogías históricas y contexto de episodios de crisis.
- **Sesgos y cautelas:** Cobertura centrada en EE. UU.; fondos históricos, no datos de actualidad.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «ALFRED Archival Federal Reserve Economic Data vintage St. Louis Fed»; WebFetch: sí)
- **Origen:** Alta 2026-11-02 (F9_S1).

#### RF-0202 · Q 76 (B) — The FRED Blog (Federal Reserve Bank of St. Louis)

- **Canal oficial (URL raíz):** https://fredblog.stlouisfed.org/
- **Emisor:** Federal Reserve Bank of St. Louis (Research Division)
- **Temática:** TF-01 Bancos centrales, organismos internacionales y estadísticas oficiales (principal) · secundarias: TF-06
- **Calidad Q:** 76 (B) — Primariedad 12/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 13/15 · Independencia 9/10 · Actualidad 9/10 · Acceso 10/10
- **Tipología:** secundaria cualificada (divulgación sobre datos oficiales)
- **Acceso:** Abierto
- **Ámbitos:** Lectura de series de FRED y ALFRED; revisiones de datos; gráficos reproducibles
- **Motivo de inclusión y uso:** Notas breves que explican cómo leer y combinar series (p. ej., cómo cambian las estimaciones de empleo del BLS entre vintages). Uso: apoyo metodológico para agentes que consumen FRED/ALFRED (RF-0001, RF-0015).
- **Sesgos y cautelas:** Divulgativo; no sustituye a la serie primaria.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «ALFRED Archival Federal Reserve Economic Data vintage St. Louis Fed»; WebFetch: sí)
- **Origen:** Alta 2026-11-02 (F9_S1).

## TF-02 Reguladores, registros públicos y documentación corporativa

#### RF-0002 · Q 89 (A) — SEC EDGAR (U.S. Securities and Exchange Commission)

- **Canal oficial:** sec.gov/edgar
- **Documentación y notas:** Búsqueda de texto completo: sec.gov/edgar/search/ · Documentación de APIs estructuradas: sec.gov/edgar/sec-api-documentation · Citar formulario, fecha de presentación y CIK (ficha)
- **Temática:** TF-02 Reguladores, registros públicos y documentación corporativa (principal) · secundarias: TF-04
- **Calidad Q:** 89 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 10/10 · Acceso 10/10
- **Nivel de fiabilidad en V2.4:** A
- **Tipología:** primaria
- **Motivo de inclusión:** Repositorio primario de documentos regulatorios de emisores estadounidenses (10-K, 10-Q, 8-K, 13F): la fuente de máxima autoridad para hechos corporativos
- **Ámbitos:** Filings y documentos regulatorios; hechos corporativos; participaciones institucionales; emisores estadounidenses
- **Restricciones de uso:** Datos públicos; citar el formulario, la fecha de presentación y el CIK del emisor
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Sesgos posibles:** Ninguno; son documentos primarios, con el matiz de que los propios emisores redactan sus declaraciones
- **Cambios de propiedad o de metodología:** Sin cambios conocidos; dependencia del servicio público EDGAR
- **Estado:** Aprobada
- **Estado del enlace:** PENDIENTE_BARRIDO
- **Última verificación:** 2026-10-25 (Completa (URL viva y naturaleza del contenido comprobadas el 25/10/2026))

#### RF-0026 · Q 87 (A) — CNMV (registros oficiales, información privilegiada, otra información relevante, participaciones significativas)

- **Canal oficial (URL raíz):** https://www.cnmv.es/ (Otra información relevante: https://www.cnmv.es/portal/Otra-Informacion-Relevante/Consulta-OIR?lang=es · Información privilegiada: https://www.cnmv.es/portal/informacion-privilegiada/consulta-ip?lang=es)
- **Emisor:** Comisión Nacional del Mercado de Valores
- **Temática:** TF-02 Reguladores, registros públicos y documentación corporativa (principal)
- **Calidad Q:** 87 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 10/10 · Acceso 8/10
- **Tipología:** primaria
- **Acceso:** Abierto (alertas por correo por entidad o tipo de información)
- **Ámbitos:** Comunicaciones de emisores españoles: información privilegiada, OIR (informes financieros y de auditoría, derechos de voto, autocartera, OPA, operaciones vinculadas, suspensiones, calificaciones), participaciones significativas
- **Motivo de inclusión y uso:** Registro oficial de lo que comunican los emisores cotizados (art. 227 LMV), filtrable por entidad, código LEI, tipo y fecha. Uso: hechos corporativos de primera mano para valores españoles.
- **Sesgos y cautelas:** La CNMV publica sin responsabilizarse de la exactitud del contenido remitido por el emisor; contrastar con cuentas auditadas.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «CNMV registros oficiales información privilegiada otra información relevante participaciones significativas»; WebFetch: sí)
- **Origen:** Semilla V3.0 (2026-11-01) confirmada en verificación de alta 2026-11-02.

#### RF-0027 · Q 87 (A) — ESMA (registros, informes de tendencias, riesgos y vulnerabilidades)

- **Canal oficial (URL raíz):** https://www.esma.europa.eu/ (TRV n.º 1 2026: https://www.esma.europa.eu/document/trends-risks-and-vulnerabilities-trv-report-no-1-2026)
- **Emisor:** European Securities and Markets Authority
- **Temática:** TF-02 Reguladores, registros públicos y documentación corporativa (principal) · secundarias: TF-01
- **Calidad Q:** 87 (A) — Primariedad 19/20 · Historial 10/20 · Transparencia 15/15 · Autoridad 15/15 · Independencia 9/10 · Actualidad 9/10 · Acceso 10/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** Supervisión de valores de la UE; informes TRV (Risk Monitor y anexo estadístico, semestrales); indicadores estructurales de mercado; registros
- **Motivo de inclusión y uso:** Diagnóstico oficial de riesgos de los mercados de valores europeos con anexo estadístico. Uso: mapa de riesgos sistémicos y vulnerabilidades del mercado europeo.
- **Sesgos y cautelas:** Perspectiva supervisora (énfasis en riesgos); las fichas de documento no siempre muestran fecha de publicación.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «ESMA TRV Trends Risks and Vulnerabilities report registers esma.europa.eu»; WebFetch: sí)
- **Origen:** Semilla V3.0 (2026-11-01) confirmada en verificación de alta 2026-11-02.

#### RF-0028 · Q 86 (A) — Financial Conduct Authority (FCA)

- **Canal oficial (URL raíz):** https://www.fca.org.uk/ (Financial Services Register: https://www.fca.org.uk/firms/financial-services-register)
- **Emisor:** Financial Conduct Authority (Reino Unido)
- **Temática:** TF-02 Reguladores, registros públicos y documentación corporativa (principal)
- **Calidad Q:** 86 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 9/10 · Actualidad 9/10 · Acceso 9/10
- **Tipología:** primaria
- **Acceso:** Abierto (API gratuita del Register sin garantías de servicio; extractos masivos de pago)
- **Ámbitos:** Autorizaciones de firmas e individuos (FCA y PRA), firmas no autorizadas y clones, representantes designados, sanciones
- **Motivo de inclusión y uso:** Registro público para comprobar si una entidad o persona está autorizada y su historial disciplinario. Uso: control de credibilidad y detección de fraudes en emisores y gestores del Reino Unido.
- **Sesgos y cautelas:** Jurisdicción británica; la lista de firmas no autorizadas no es exhaustiva.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Financial Conduct Authority FCA Financial Services Register fca.org.uk»; WebFetch: sí)
- **Origen:** Semilla V3.0 (2026-11-01) confirmada en verificación de alta 2026-11-02.

#### RF-0206 · Q 85 (A) — BaFin (Bundesanstalt für Finanzdienstleistungsaufsicht)

- **Canal oficial (URL raíz):** http://www.bafin.de/EN/Homepage/homepage_node.html (según directorio FCA)
- **Emisor:** Autoridad Federal de Supervisión Financiera de Alemania
- **Temática:** TF-02 Reguladores, registros públicos y documentación corporativa (principal)
- **Calidad Q:** 85 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 9/10 · Actualidad 9/10 · Acceso 8/10
- **Tipología:** primaria
- **Acceso:** Abierto (parte del contenido solo en alemán)
- **Ámbitos:** Supervisión integrada (banca, seguros, valores) de Alemania; bases de datos de entidades autorizadas, notificaciones de derechos de voto y posiciones cortas netas, sanciones
- **Motivo de inclusión y uso:** Fuente primaria de hechos regulatorios y de registros de emisores y entidades alemanas. Uso: confirmar autorizaciones, participaciones significativas y medidas supervisoras en Alemania.
- **Sesgos y cautelas:** Cobertura nacional; terminología y versiones en alemán más completas.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «list of financial regulatory authorities by country wikipedia» → directorio FCA; WebFetch: sí, sobre el directorio FCA; sitio de BaFin no leído)
- **Origen:** Alta 2026-11-02 (F9_S1, tanda 2).

#### RF-0207 · Q 85 (A) — AMF (Autorité des marchés financiers, Francia)

- **Canal oficial (URL raíz):** https://www.amf-france.org/en (según directorio FCA)
- **Emisor:** Autorité des marchés financiers
- **Temática:** TF-02 Reguladores, registros públicos y documentación corporativa (principal)
- **Calidad Q:** 85 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 9/10 · Actualidad 9/10 · Acceso 8/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** Mercados de valores franceses: base documental de emisores (BDIF), declaraciones de umbrales, OPA, sanciones, listas negras de sitios no autorizados
- **Motivo de inclusión y uso:** Regulador del principal mercado de Euronext. Uso: hechos corporativos y regulatorios de emisores franceses y alertas de fraude.
- **Sesgos y cautelas:** Parte de la documentación de emisores solo en francés.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «list of financial regulatory authorities by country wikipedia» → directorio FCA; WebFetch: sí, sobre el directorio FCA)
- **Origen:** Alta 2026-11-02 (F9_S1, tanda 2).

#### RF-0208 · Q 85 (A) — CONSOB (Commissione Nazionale per le Società e la Borsa)

- **Canal oficial (URL raíz):** https://www.consob.it/ (directorio de supervisores europeos: https://www.consob.it/web/consob-and-its-activities/financial-market-supervisory-authorities-in-europe)
- **Emisor:** CONSOB (Italia)
- **Temática:** TF-02 Reguladores, registros públicos y documentación corporativa (principal)
- **Calidad Q:** 85 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 9/10 · Actualidad 9/10 · Acceso 8/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** Mercados de valores italianos: participaciones relevantes, información regulada de emisores, sanciones; directorio de las autoridades nacionales europeas con enlace a sus registros de entidades autorizadas
- **Motivo de inclusión y uso:** Regulador de Borsa Italiana. Su directorio (actualizado el 30/03/2026) da, por país, la web en inglés y el registro de entidades autorizadas de cada supervisor de la UE, el EEE, Suiza y el Reino Unido. Uso: hechos de emisores italianos y punto de entrada a los registros europeos.
- **Sesgos y cautelas:** El directorio enlaza erróneamente a la CNMV en la fila de Suecia (comprobado el 2/11/2026) y no garantiza la vigencia de los enlaces.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «list of financial regulatory authorities by country wikipedia»; WebFetch: sí)
- **Origen:** Alta 2026-11-02 (F9_S1, tanda 2).

#### RF-0209 · Q 84 (A) — Central Bank of Ireland (supervisión de fondos y ETF domiciliados en Irlanda)

- **Canal oficial (URL raíz):** http://www.centralbank.ie/Pages/home.aspx (según directorio FCA)
- **Emisor:** Central Bank of Ireland
- **Temática:** TF-02 Reguladores, registros públicos y documentación corporativa (principal) · secundarias: TF-01
- **Calidad Q:** 84 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 14/15 · Independencia 9/10 · Actualidad 9/10 · Acceso 8/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** Registros de fondos UCITS/AIF y gestoras autorizadas en Irlanda (principal domicilio europeo de ETF); estadísticas de fondos; estabilidad financiera
- **Motivo de inclusión y uso:** Autoridad que autoriza buena parte de los ETF UCITS comercializados en Europa. Uso: verificar autorización de fondos y gestoras, estadísticas del sector de fondos irlandés.
- **Sesgos y cautelas:** La URL del directorio FCA tiene formato antiguo (http, «Pages/home.aspx»); comprobar redirección en el barrido HT-02.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «list of financial regulatory authorities by country wikipedia» → directorio FCA; WebFetch: sí, sobre el directorio FCA)
- **Origen:** Alta 2026-11-02 (F9_S1, tanda 2).

#### RF-0210 · Q 84 (A) — CSSF (Commission de Surveillance du Secteur Financier, Luxemburgo)

- **Canal oficial (URL raíz):** http://www.cssf.lu/en/ (según directorio FCA)
- **Emisor:** Commission de Surveillance du Secteur Financier
- **Temática:** TF-02 Reguladores, registros públicos y documentación corporativa (principal)
- **Calidad Q:** 84 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 14/15 · Independencia 9/10 · Actualidad 9/10 · Acceso 8/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** Registro de OIC/UCITS y gestoras de Luxemburgo (primer domicilio de fondos de la UE); folletos; estadísticas mensuales de patrimonio de OIC
- **Motivo de inclusión y uso:** Supervisor del mayor centro de fondos de Europa. Uso: verificar fondos luxemburgueses y seguir sus estadísticas de patrimonio y flujos.
- **Sesgos y cautelas:** Cobertura nacional; comprobar redirección de la URL en el barrido.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «list of financial regulatory authorities by country wikipedia» → directorio FCA; WebFetch: sí, sobre el directorio FCA)
- **Origen:** Alta 2026-11-02 (F9_S1, tanda 2).

#### RF-0211 · Q 84 (A) — AFM (Autoriteit Financiële Markten, Países Bajos)

- **Canal oficial (URL raíz):** http://www.afm.nl/en (según directorio FCA)
- **Emisor:** Netherlands Authority for the Financial Markets
- **Temática:** TF-02 Reguladores, registros públicos y documentación corporativa (principal)
- **Calidad Q:** 84 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 14/15 · Independencia 9/10 · Actualidad 9/10 · Acceso 8/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** Registros públicos de participaciones sustanciales, posiciones cortas netas, operaciones de directivos y folletos de emisores de Euronext Ámsterdam
- **Motivo de inclusión y uso:** Registros de transparencia muy granulares (participaciones y cortos) de un mercado con grandes emisores europeos. Uso: posicionamiento de grandes inversores y bajistas en valores neerlandeses.
- **Sesgos y cautelas:** Cobertura nacional; comprobar redirección de la URL.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «list of financial regulatory authorities by country wikipedia» → directorio FCA; WebFetch: sí, sobre el directorio FCA)
- **Origen:** Alta 2026-11-02 (F9_S1, tanda 2).

#### RF-0212 · Q 83 (A) — Securities and Futures Commission (SFC, Hong Kong)

- **Canal oficial (URL raíz):** https://www.sfc.hk/ (página IOSCO MMoU: https://www.sfc.hk/web/EN/about-the-sfc/collaboration/overseas/iosco-mmou.html)
- **Emisor:** Securities and Futures Commission of Hong Kong
- **Temática:** TF-02 Reguladores, registros públicos y documentación corporativa (principal)
- **Calidad Q:** 83 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 14/15 · Independencia 8/10 · Actualidad 9/10 · Acceso 9/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** Supervisión de valores y futuros de Hong Kong; registro público de intermediarios; acciones de enforcement; cooperación internacional (IOSCO MMoU)
- **Motivo de inclusión y uso:** Regulador del principal mercado de acceso a renta variable china fuera del continente. Uso: hechos regulatorios y sancionadores de Hong Kong.
- **Sesgos y cautelas:** Contexto político de Hong Kong; cobertura limitada a su jurisdicción.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «list of financial regulatory authorities by country wikipedia»; WebFetch: sí)
- **Origen:** Alta 2026-11-02 (F9_S1, tanda 2).

#### RF-0213 · Q 83 (A) — ACPR (Autorité de contrôle prudentiel et de résolution, Francia)

- **Canal oficial (URL raíz):** https://acpr.banque-france.fr/en (según directorio FCA)
- **Emisor:** ACPR, adscrita a la Banque de France
- **Temática:** TF-02 Reguladores, registros públicos y documentación corporativa (principal)
- **Calidad Q:** 83 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 14/15 · Independencia 9/10 · Actualidad 8/10 · Acceso 9/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** Supervisión prudencial de banca y seguros en Francia; listas de entidades autorizadas (REGAFI); listas negras
- **Motivo de inclusión y uso:** Complementa a la AMF en el lado prudencial (bancos y aseguradoras). Uso: autorizaciones y medidas prudenciales francesas.
- **Sesgos y cautelas:** Cobertura nacional.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «list of financial regulatory authorities by country wikipedia» → directorio FCA; WebFetch: sí, sobre el directorio FCA)
- **Origen:** Alta 2026-11-02 (F9_S1, tanda 2).

#### RF-0214 · Q 82 (A) — CMVM (Comissão do Mercado de Valores Mobiliários, Portugal)

- **Canal oficial (URL raíz):** https://www.cmvm.pt/PInstitucional/PortalInstitucional?Input_language=en-US (según directorio FCA)
- **Emisor:** CMVM
- **Temática:** TF-02 Reguladores, registros públicos y documentación corporativa (principal)
- **Calidad Q:** 82 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 14/15 · Independencia 9/10 · Actualidad 8/10 · Acceso 8/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** Información privilegiada y participaciones cualificadas de emisores de Euronext Lisboa; registros de fondos y gestoras portugueses
- **Motivo de inclusión y uso:** Equivalente portugués de la CNMV, relevante para emisores ibéricos. Uso: hechos corporativos de cotizadas portuguesas.
- **Sesgos y cautelas:** Cobertura nacional; parte del contenido solo en portugués.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «list of financial regulatory authorities by country wikipedia» → directorio FCA; WebFetch: sí, sobre el directorio FCA)
- **Origen:** Alta 2026-11-02 (F9_S1, tanda 2).

#### RF-0215 · Q 82 (A) — Finansinspektionen (Suecia)

- **Canal oficial (URL raíz):** http://www.fi.se/en/ (según directorio FCA)
- **Emisor:** Swedish Financial Supervisory Authority
- **Temática:** TF-02 Reguladores, registros públicos y documentación corporativa (principal)
- **Calidad Q:** 82 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 14/15 · Independencia 9/10 · Actualidad 8/10 · Acceso 8/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** Registro de operaciones de directivos (insynsregistret), posiciones cortas, folletos y entidades autorizadas en Suecia
- **Motivo de inclusión y uso:** Registro público de operaciones de directivos de cotizadas nórdicas de gran tamaño. Uso: señales de compras y ventas de insiders en Suecia.
- **Sesgos y cautelas:** Cobertura nacional; el directorio de CONSOB enlaza por error a otra autoridad en la fila sueca (usar esta URL).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «list of financial regulatory authorities by country wikipedia» → directorio FCA; WebFetch: sí, sobre el directorio FCA)
- **Origen:** Alta 2026-11-02 (F9_S1, tanda 2).

#### RF-0216 · Q 81 (A) — FSMA (Financial Services and Markets Authority, Bélgica)

- **Canal oficial (URL raíz):** http://www.fsma.be/en.aspx (según directorio FCA)
- **Emisor:** FSMA
- **Temática:** TF-02 Reguladores, registros públicos y documentación corporativa (principal)
- **Calidad Q:** 81 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 13/15 · Independencia 9/10 · Actualidad 8/10 · Acceso 8/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** Participaciones importantes y operaciones de directivos de emisores de Euronext Bruselas; avisos sobre entidades fraudulentas
- **Motivo de inclusión y uso:** Fuente primaria para emisores belgas. Uso: hechos corporativos y alertas de fraude.
- **Sesgos y cautelas:** URL de formato antiguo; comprobar redirección.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «list of financial regulatory authorities by country wikipedia» → directorio FCA; WebFetch: sí, sobre el directorio FCA)
- **Origen:** Alta 2026-11-02 (F9_S1, tanda 2).

#### RF-0217 · Q 81 (A) — Finanstilsynet (Noruega)

- **Canal oficial (URL raíz):** http://www.finanstilsynet.no/en/ (según directorio FCA)
- **Emisor:** Financial Supervisory Authority of Norway
- **Temática:** TF-02 Reguladores, registros públicos y documentación corporativa (principal)
- **Calidad Q:** 81 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 13/15 · Independencia 9/10 · Actualidad 8/10 · Acceso 8/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** Supervisión financiera noruega; entidades autorizadas; informes de riesgos del sistema financiero
- **Motivo de inclusión y uso:** Supervisor de un mercado con fuerte peso energético y del fondo soberano como inversor. Uso: hechos regulatorios noruegos.
- **Sesgos y cautelas:** Cobertura nacional.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «list of financial regulatory authorities by country wikipedia» → directorio FCA; WebFetch: sí, sobre el directorio FCA)
- **Origen:** Alta 2026-11-02 (F9_S1, tanda 2).

#### RF-0218 · Q 80 (A) — KNF (Komisja Nadzoru Finansowego, Polonia)

- **Canal oficial (URL raíz):** https://www.knf.gov.pl/en/ (según directorio FCA)
- **Emisor:** Polish Financial Supervision Authority
- **Temática:** TF-02 Reguladores, registros públicos y documentación corporativa (principal)
- **Calidad Q:** 80 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 13/15 · Independencia 8/10 · Actualidad 8/10 · Acceso 8/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** Supervisión del mayor mercado de valores de Europa central (Bolsa de Varsovia); lista de advertencias públicas
- **Motivo de inclusión y uso:** Fuente primaria para emisores y entidades polacas. Uso: hechos regulatorios y alertas en Europa central.
- **Sesgos y cautelas:** Cobertura nacional; contenido completo en polaco.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «list of financial regulatory authorities by country wikipedia» → directorio FCA; WebFetch: sí, sobre el directorio FCA)
- **Origen:** Alta 2026-11-02 (F9_S1, tanda 2).

#### RF-0219 · Q 80 (A) — FMA (Finanzmarktaufsicht, Austria)

- **Canal oficial (URL raíz):** https://www.fma.gv.at/en/ (según directorio FCA)
- **Emisor:** Austrian Financial Market Authority
- **Temática:** TF-02 Reguladores, registros públicos y documentación corporativa (principal)
- **Calidad Q:** 80 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 13/15 · Independencia 9/10 · Actualidad 7/10 · Acceso 8/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** Supervisión integrada austríaca; base de datos de entidades supervisadas; advertencias a inversores
- **Motivo de inclusión y uso:** Fuente primaria para emisores y bancos austríacos con exposición a Europa central y del este. Uso: hechos regulatorios y alertas.
- **Sesgos y cautelas:** Cobertura nacional.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «list of financial regulatory authorities by country wikipedia» → directorio FCA; WebFetch: sí, sobre el directorio FCA)
- **Origen:** Alta 2026-11-02 (F9_S1, tanda 2).

#### RF-0220 · Q 80 (A) — Finanstilsynet (Danish Financial Supervisory Authority)

- **Canal oficial (URL raíz):** https://www.dfsa.dk/ (según directorio FCA)
- **Emisor:** Danish Financial Supervisory Authority
- **Temática:** TF-02 Reguladores, registros públicos y documentación corporativa (principal)
- **Calidad Q:** 80 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 13/15 · Independencia 9/10 · Actualidad 7/10 · Acceso 8/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** Supervisión financiera danesa (incluido el gran mercado de bonos hipotecarios); entidades autorizadas
- **Motivo de inclusión y uso:** Fuente primaria para emisores daneses de gran capitalización y para el mercado de bonos hipotecarios. Uso: hechos regulatorios de Dinamarca.
- **Sesgos y cautelas:** Cobertura nacional.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «list of financial regulatory authorities by country wikipedia» → directorio FCA; WebFetch: sí, sobre el directorio FCA)
- **Origen:** Alta 2026-11-02 (F9_S1, tanda 2).

#### RF-0221 · Q 79 (B) — IVASS (Istituto per la Vigilanza sulle Assicurazioni, Italia)

- **Canal oficial (URL raíz):** https://www.ivass.it/homepage/index.html (según directorio FCA, que añade parámetros de idioma y caché)
- **Emisor:** IVASS
- **Temática:** TF-02 Reguladores, registros públicos y documentación corporativa (principal)
- **Calidad Q:** 79 (B) — Primariedad 20/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 13/15 · Independencia 9/10 · Actualidad 7/10 · Acceso 8/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** Supervisión del seguro italiano; registros de aseguradoras e intermediarios; estadísticas del sector
- **Motivo de inclusión y uso:** Fuente primaria para el sector asegurador italiano (grandes tenedores de deuda pública). Uso: hechos regulatorios del seguro en Italia.
- **Sesgos y cautelas:** Cobertura nacional y sectorial; contenido completo en italiano.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «list of financial regulatory authorities by country wikipedia» → directorio FCA; WebFetch: sí, sobre el directorio FCA)
- **Origen:** Alta 2026-11-02 (F9_S1, tanda 2).

## TF-03 Prensa financiera y agencias de noticias

#### RF-0222 · Q 79 (B) — Associated Press (AP)

- **Canal oficial (URL raíz):** https://apnews.com/ (noticias) · https://www.ap.org/ (corporativo) (según Wikipedia)
- **Emisor:** The Associated Press (cooperativa sin ánimo de lucro, Nueva York, fundada en 1846)
- **Temática:** TF-03 Prensa financiera y agencias de noticias (principal)
- **Calidad Q:** 79 (B) — Primariedad 16/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 13/15 · Independencia 9/10 · Actualidad 10/10 · Acceso 9/10
- **Tipología:** primaria (reporterismo de agencia)
- **Acceso:** Abierto (apnews.com)
- **Ámbitos:** Noticias generales, económicas y políticas de EE. UU. y el mundo
- **Motivo de inclusión y uso:** Agencia cooperativa de alcance mundial con acceso abierto; segunda raíz independiente frente a Reuters para corroborar hechos de actualidad. Uso: hechos de actualidad, a confirmar con la fuente oficial.
- **Sesgos y cautelas:** Cobertura financiera menos profunda que la de agencias especializadas; las copias en otros medios son sindicadas (enlazar a la raíz).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «list of news agencies wikipedia» → artículo de Wikipedia «Associated Press»; WebFetch: sí, sobre Wikipedia)
- **Origen:** Alta 2026-11-02 (F9_S1, tanda 2).

#### RF-0029 · Q 72 (B) — Reuters

- **Canal oficial (URL raíz):** reuters.com (según Wikipedia) · Principios de confianza: https://thomsonreuters.com/en/about-us/trust-principles.html
- **Emisor:** Thomson Reuters (distribución profesional vía LSEG)
- **Temática:** TF-03 Prensa financiera y agencias de noticias (principal)
- **Calidad Q:** 72 (B) — Primariedad 15/20 · Historial 10/20 · Transparencia 10/15 · Autoridad 13/15 · Independencia 8/10 · Actualidad 10/10 · Acceso 6/10
- **Tipología:** primaria
- **Acceso:** Muro parcial
- **Ámbitos:** Noticias de mercados, empresas, macro, materias primas
- **Motivo de inclusión y uso:** Agencia con reporterismo original (fundada en 1851) sujeta a los Trust Principles (integridad, independencia y ausencia de sesgo, desde 1941). Uso: primera fuente de hechos de actualidad.
- **Sesgos y cautelas:** Titulares tempranos corregidos; verificar contra fuente oficial.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «list of news agencies wikipedia» → artículo de Wikipedia «Reuters»; «Reuters markets business news reuters.com Thomson Reuters Trust Principles»; WebFetch: sí, sobre Wikipedia y sobre los Trust Principles)
- **Origen:** Semilla V3.0 (2026-11-01) confirmada en verificación de alta 2026-11-02 (tanda 2), por vía Wikipedia.

#### RF-0255 · Q 70 (B) — Reuters Breakingviews

- **Canal oficial (URL raíz):** https://www.breakingviews.com/ (página leída: https://breakingviews.com/?p=136)
- **Emisor:** Reuters News (Thomson Reuters), marca internacional de comentario financiero
- **Temática:** TF-03 Prensa financiera y agencias de noticias (principal) · secundarias: TF-05
- **Calidad Q:** 70 (B) — Primariedad 10/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 13/15 · Independencia 8/10 · Actualidad 10/10 · Acceso 7/10
- **Tipología:** secundaria (opinión firmada)
- **Acceso:** Suscripción (prueba gratuita); algunas columnas también en Reuters.com
- **Ámbitos:** Comentario en tiempo real sobre operaciones corporativas, valoraciones, mercados y economía; unos 36 columnistas en centros financieros
- **Motivo de inclusión y uso:** Opinión de referencia con cálculos explícitos (valoración, sinergias) sobre noticias corporativas. Uso: segunda lectura crítica de operaciones; nunca como prueba de hechos (regla F9 a).
- **Sesgos y cautelas:** Comparte raíz con Reuters (RF-0029); no cuenta como fuente independiente de esta.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Reuters Breakingviews financial commentary»; WebFetch: sí)
- **Origen:** Alta 2026-11-02 (F9_S1, tanda 3).

#### RF-0030 · Q 69 (B) — Financial Times

- **Canal oficial (URL raíz):** www.ft.com (según Wikipedia)
- **Emisor:** The Financial Times Ltd. (propiedad de Nikkei Inc.)
- **Temática:** TF-03 Prensa financiera y agencias de noticias (principal)
- **Calidad Q:** 69 (B) — Primariedad 14/20 · Historial 10/20 · Transparencia 10/15 · Autoridad 13/15 · Independencia 8/10 · Actualidad 10/10 · Acceso 4/10
- **Tipología:** primaria y secundaria (opinión)
- **Acceso:** Suscripción (muro de pago medido desde 2007)
- **Ámbitos:** Mercados globales, empresas, política económica; columnas de opinión
- **Motivo de inclusión y uso:** Prensa financiera de referencia con reporterismo propio (fundada en 1888, Londres). Uso: hechos y contexto de mercados globales; columnas como opinión.
- **Sesgos y cautelas:** Muro de pago; separar noticia de columna de opinión.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «list of financial newspapers wikipedia business newspapers» → artículo de Wikipedia «Financial Times»; WebFetch: sí, sobre Wikipedia)
- **Origen:** Semilla V3.0 (2026-11-01) confirmada en verificación de alta 2026-11-02 (tanda 2), por vía Wikipedia.

#### RF-0223 · Q 69 (B) — Dow Jones Newswires

- **Canal oficial (URL raíz):** dowjones.com (sitio oficial de Dow Jones & Company según Wikipedia)
- **Emisor:** Dow Jones & Company (News Corp)
- **Temática:** TF-03 Prensa financiera y agencias de noticias (principal)
- **Calidad Q:** 69 (B) — Primariedad 16/20 · Historial 10/20 · Transparencia 10/15 · Autoridad 13/15 · Independencia 7/10 · Actualidad 10/10 · Acceso 3/10
- **Tipología:** primaria (agencia de noticias financieras en tiempo real, desde 1882)
- **Acceso:** Suscripción profesional (terminales y Factiva)
- **Ámbitos:** Noticias financieras en tiempo real: empresas, mercados, materias primas, renta fija
- **Motivo de inclusión y uso:** Agencia financiera en tiempo real del grupo editor de The Wall Street Journal, Barron's y MarketWatch. Uso: hechos de última hora cuando se accede por licencia; para citar, preferir la versión publicada en WSJ o la fuente primaria.
- **Sesgos y cautelas:** Acceso restringido; misma raíz que RF-0032 (no cuentan como fuentes independientes entre sí).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «wsj.com markets The Wall Street Journal Dow Jones» → artículo de Wikipedia «Dow Jones & Company»; WebFetch: sí, sobre Wikipedia)
- **Origen:** Alta 2026-11-02 (F9_S1, tanda 2).

#### RF-0031 · Q 68 (B) — Bloomberg News

- **Canal oficial (URL raíz):** https://www.bloomberg.com/ (ejemplo de programa Bloomberg Markets: https://www.bloomberg.com/news/videos/2026-03-26/bloomberg-markets-3-26-2026-video)
- **Emisor:** Bloomberg L.P.
- **Temática:** TF-03 Prensa financiera y agencias de noticias (principal)
- **Calidad Q:** 68 (B) — Primariedad 14/20 · Historial 10/20 · Transparencia 10/15 · Autoridad 13/15 · Independencia 7/10 · Actualidad 10/10 · Acceso 4/10
- **Tipología:** primaria (reporterismo propio) y secundaria (opinión)
- **Acceso:** Muro de pago (artículos); vídeos y resúmenes parcialmente abiertos
- **Ámbitos:** Noticias de mercados, empresas, macro y política económica; programas de vídeo
- **Motivo de inclusión y uso:** Reporterismo financiero de alta velocidad con fuentes propias. Uso: hechos de actualidad a corroborar con la fuente primaria; las piezas de Bloomberg Opinion se tratan como opinión.
- **Sesgos y cautelas:** Propiedad vinculada al negocio de terminales; distinguir noticia y opinión; muro de pago limita la citación pública.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Bloomberg News markets bloomberg.com/markets»; WebFetch: sí, página de vídeo cargada con resumen; artículo completo no comprobado)
- **Origen:** Semilla V3.0 (2026-11-01) confirmada en verificación de alta 2026-11-02.

#### RF-0032 · Q 68 (B) — The Wall Street Journal

- **Canal oficial (URL raíz):** wsj.com (según Wikipedia)
- **Emisor:** Dow Jones & Company (News Corp)
- **Temática:** TF-03 Prensa financiera y agencias de noticias (principal)
- **Calidad Q:** 68 (B) — Primariedad 14/20 · Historial 10/20 · Transparencia 10/15 · Autoridad 13/15 · Independencia 7/10 · Actualidad 10/10 · Acceso 4/10
- **Tipología:** primaria y secundaria (opinión)
- **Acceso:** Suscripción
- **Ámbitos:** Mercados y empresas de EE. UU.
- **Motivo de inclusión y uso:** Reporterismo original de referencia en EE. UU. (fundado en 1889, Nueva York).
- **Sesgos y cautelas:** Muro de pago; página editorial con línea de opinión diferenciada; misma raíz que Dow Jones Newswires (RF-0223).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «list of financial newspapers wikipedia business newspapers» → artículo de Wikipedia «The Wall Street Journal»; WebFetch: sí, sobre Wikipedia)
- **Origen:** Semilla V3.0 (2026-11-01) confirmada en verificación de alta 2026-11-02 (tanda 2), por vía Wikipedia.

#### RF-0254 · Q 68 (B) — Nikkei Asia

- **Canal oficial (URL raíz):** https://asia.nikkei.com/ (presentación del medio: https://info.asia.nikkei.com/about · anuncio de cambio de nombre: https://asia.nikkei.com/announcements/nikkei-to-rename-flagship-english-publication-nikkei-asia)
- **Emisor:** Nikkei Inc. (grupo propietario también de The Nikkei, del índice Nikkei 225 y del Financial Times)
- **Temática:** TF-03 Prensa financiera y agencias de noticias (principal)
- **Calidad Q:** 68 (B) — Primariedad 14/20 · Historial 10/20 · Transparencia 9/15 · Autoridad 13/15 · Independencia 7/10 · Actualidad 10/10 · Acceso 5/10
- **Tipología:** primaria (reporterismo propio) y secundaria
- **Acceso:** Suscripción (no se ha confirmado el detalle del muro de pago)
- **Ámbitos:** Empresas, economía, política y mercados de Asia; entrevistas; lista Asia300
- **Motivo de inclusión y uso:** Principal medio económico en inglés centrado en Asia, con reporterismo propio en Japón, China y el Sudeste Asiático. Uso: hechos y contexto de empresas y mercados asiáticos.
- **Sesgos y cautelas:** Mismo grupo propietario que el FT (RF-0030): artículos compartidos no son raíces independientes.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Nikkei Asia business news asia.nikkei.com»; WebFetch: sí)
- **Origen:** Alta 2026-11-02 (F9_S1, tanda 3).

#### RF-0034 · Q 66 (B) — Expansión

- **Canal oficial (URL raíz):** expansion.com (según Wikipedia)
- **Emisor:** Unidad Editorial (controlada por RCS MediaGroup)
- **Temática:** TF-03 Prensa financiera y agencias de noticias (principal)
- **Calidad Q:** 66 (B) — Primariedad 13/20 · Historial 10/20 · Transparencia 9/15 · Autoridad 11/15 · Independencia 7/10 · Actualidad 10/10 · Acceso 6/10
- **Tipología:** primaria y secundaria
- **Acceso:** Muro parcial
- **Ámbitos:** Mercados y empresas españolas
- **Motivo de inclusión y uso:** Prensa económica española de referencia (fundada en 1986, Madrid).
- **Sesgos y cautelas:** Muro parcial; cobertura nacional; Wikipedia da datos de propiedad no coincidentes (infobox: Grupo Recoletos; texto: Unidad Editorial/RCS).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «expansion.com mercados diario Expansión Unidad Editorial» → artículo de Wikipedia «Expansión (Spanish newspaper)»; WebFetch: sí, sobre Wikipedia)
- **Origen:** Semilla V3.0 (2026-11-01) confirmada en verificación de alta 2026-11-02 (tanda 2), por vía Wikipedia.

#### RF-0035 · Q 66 (B) — Cinco Días

- **Canal oficial (URL raíz):** https://cincodias.elpais.com/ (a verificar)
- **Emisor:** PRISA
- **Temática:** TF-03 Prensa financiera y agencias de noticias (principal)
- **Calidad Q (provisional):** 66 (B) — Primariedad 13/20 · Historial 10/20 · Transparencia 9/15 · Autoridad 11/15 · Independencia 7/10 · Actualidad 10/10 · Acceso 6/10
- **Tipología:** primaria
- **Acceso:** Muro parcial
- **Ámbitos:** Mercados y empresas españolas
- **Motivo de inclusión y uso:** Prensa económica española de referencia.
- **Sesgos y cautelas:** Muro parcial; cobertura nacional.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** PENDIENTE_VERIFICACION_ALTA
- **Estado del enlace:** PENDIENTE_BARRIDO
- **Última verificación:** — (sin verificar)
- **Origen:** Semilla V3.0 (2026-11-01); BFA la verifica en su primer barrido (HT-02: URL oficial, titularidad, condiciones de uso) y la confirma, repara o da de baja.

#### RF-0203 · Q 66 (B) — Central Banking (Infopro Digital)

- **Canal oficial (URL raíz):** https://www.centralbanking.com/
- **Emisor:** Infopro Digital Services Limited (Londres)
- **Temática:** TF-03 Prensa financiera y agencias de noticias (principal) · secundarias: TF-01
- **Calidad Q:** 66 (B) — Primariedad 12/20 · Historial 10/20 · Transparencia 10/15 · Autoridad 12/15 · Independencia 8/10 · Actualidad 9/10 · Acceso 5/10
- **Tipología:** secundaria especializada
- **Acceso:** Muro de pago (suscripción individual o corporativa)
- **Ámbitos:** Banca central: política monetaria, estabilidad financiera, divisas, reservas, gobernanza, fintech; encuestas de benchmarking
- **Motivo de inclusión y uso:** Publicación especializada en bancos centrales con archivo largo (artículos desde al menos 2002). Uso: contexto y entrevistas sobre bancos centrales sin cobertura en la prensa generalista; los hechos se citan en la fuente oficial (TF-01).
- **Sesgos y cautelas:** Acceso restringido; parte del negocio son premios y eventos con la propia industria.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** MURO_PAGO
- **Última verificación:** 2026-11-02 (búsqueda web: «Bank of England Monetary Policy Report Monetary Policy Committee minutes»; WebFetch: sí)
- **Origen:** Alta 2026-11-02 (F9_S1).

#### RF-0036 · Q 65 (B) — CoinDesk

- **Canal oficial (URL raíz):** https://www.coindesk.com/ (política ética: https://www.CoinDesk.com/ethics/)
- **Emisor:** CoinDesk (propiedad de Bullish desde noviembre de 2023)
- **Temática:** TF-03 Prensa financiera y agencias de noticias (principal) · secundarias: TF-10
- **Calidad Q:** 65 (B) — Primariedad 13/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 10/15 · Independencia 4/10 · Actualidad 10/10 · Acceso 6/10
- **Tipología:** primaria (reporterismo cripto) y secundaria
- **Acceso:** Abierto con publicidad; algunos productos de pago
- **Ámbitos:** Noticias de criptoactivos, mercados de activos digitales, regulación cripto
- **Motivo de inclusión y uso:** Medio especializado de referencia en cripto con política ética publicada (actualizada en diciembre de 2024): divulgación de propiedad en cada artículo y de tenencias de periodistas ≥ 1.000 USD. Uso: actualidad cripto, a contrastar con datos en cadena (TF-10).
- **Sesgos y cautelas:** Conflicto estructural: el propietario (Bullish) opera un exchange cripto y su presidente dirige Block.one; episodios de salidas de editores tras la compra. Independencia puntuada a la baja.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «CoinDesk ownership Bullish editorial independence coindesk.com»; WebFetch: sí)
- **Origen:** Semilla V3.0 (2026-11-01) confirmada en verificación de alta 2026-11-02; Q 65 mantenida con desglose revisado (Independencia 4/10 por la propiedad de Bullish).

#### RF-0033 · Q 64 (C) — The Economist

- **Canal oficial (URL raíz):** www.economist.com (según Wikipedia)
- **Emisor:** The Economist Group (The Economist Newspaper Limited)
- **Temática:** TF-03 Prensa financiera y agencias de noticias (principal) · secundarias: TF-14
- **Calidad Q:** 64 (C) — Primariedad 12/20 · Historial 10/20 · Transparencia 9/15 · Autoridad 13/15 · Independencia 8/10 · Actualidad 8/10 · Acceso 4/10
- **Tipología:** secundaria (análisis y opinión)
- **Acceso:** Suscripción
- **Ámbitos:** Análisis económico y geopolítico semanal
- **Motivo de inclusión y uso:** Síntesis analítica de tendencias globales (desde 1843); útil para narrativas y consenso.
- **Sesgos y cautelas:** Línea editorial liberal explícita; artículos sin firma («voz colectiva»).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «list of financial newspapers wikipedia business newspapers» → artículo de Wikipedia «The Economist»; WebFetch: sí, sobre Wikipedia)
- **Origen:** Semilla V3.0 (2026-11-01) confirmada en verificación de alta 2026-11-02 (tanda 2), por vía Wikipedia.

#### RF-0224 · Q 64 (C) — finews.com / finews.ch

- **Canal oficial (URL raíz):** https://www.finews.com/ (edición en inglés; ejemplo leído: https://www.finews.com/news/english-news/23784-guide-to-the-markets-jpm-asset-management)
- **Emisor:** Finews AG (Suiza)
- **Temática:** TF-03 Prensa financiera y agencias de noticias (principal) · secundarias: TF-04
- **Calidad Q:** 64 (C) — Primariedad 11/20 · Historial 10/20 · Transparencia 8/15 · Autoridad 10/15 · Independencia 7/10 · Actualidad 10/10 · Acceso 8/10
- **Tipología:** secundaria especializada
- **Acceso:** Abierto (alertas gratuitas por correo)
- **Ámbitos:** Banca privada y gestión de patrimonios en Suiza; nombramientos, fintech; ediciones en alemán e inglés y finews.asia
- **Motivo de inclusión y uso:** Actualidad del centro financiero suizo (UBS, banca privada, gestoras). Uso: vigilancia de la industria suiza de gestión de patrimonios.
- **Sesgos y cautelas:** Medio pequeño centrado en la industria; contraste con fuentes primarias.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «am.jpmorgan.com Guide to the Markets quarterly US»; WebFetch: sí)
- **Origen:** Alta 2026-11-02 (F9_S1, tanda 2).

#### RF-0256 · Q 63 (C) — elEconomista.es

- **Canal oficial (URL raíz):** https://www.eleconomista.es/ (mercados: https://www.eleconomista.es/mercados-cotizaciones/)
- **Emisor:** Editorial Ecoprensa, S.A.
- **Temática:** TF-03 Prensa financiera y agencias de noticias (principal)
- **Calidad Q:** 63 (C) — Primariedad 12/20 · Historial 10/20 · Transparencia 8/15 · Autoridad 10/15 · Independencia 7/10 · Actualidad 10/10 · Acceso 6/10
- **Tipología:** primaria y secundaria
- **Acceso:** Muro parcial (no confirmado en la página leída)
- **Ámbitos:** Mercados y empresas españolas; índice propio Eco10 (difundido también en Bloomberg y Reuters con el código eco10p)
- **Motivo de inclusión y uso:** Tercera cabecera económica española, independiente de Expansión (RF-0034) y de Cinco Días. Uso: corroboración de actualidad española entre raíces distintas.
- **Sesgos y cautelas:** Cobertura nacional; el índice Eco10 es un producto editorial, no una referencia oficial.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «elEconomista.es diario económico mercados»; WebFetch: sí)
- **Origen:** Alta 2026-11-02 (F9_S1, tanda 3).

#### RF-0204 · Q 60 (C) — Funds Society

- **Canal oficial (URL raíz):** https://www.fundssociety.com/ (edición en español: https://www.fundssociety.com/es/)
- **Emisor:** Funds Society (editor de medios para la industria de gestión de activos y patrimonios)
- **Temática:** TF-03 Prensa financiera y agencias de noticias (principal) · secundarias: TF-04
- **Calidad Q:** 60 (C) — Primariedad 10/20 · Historial 10/20 · Transparencia 7/15 · Autoridad 9/15 · Independencia 6/10 · Actualidad 9/10 · Acceso 9/10
- **Tipología:** secundaria especializada
- **Acceso:** Abierto
- **Ámbitos:** Industria de fondos y banca privada: negocio, regulación, ETF, nombramientos, alternativos, pensiones; ediciones España, internacional, offshore, LATAM y Brasil
- **Motivo de inclusión y uso:** Actualidad del sector gestor en español (lanzamientos, cambios de gestores, flujos comentados). Uso: vigilancia de gestoras y productos (TF-04) y señales de industria.
- **Sesgos y cautelas:** Modelo de negocio basado en eventos y relación con gestoras (riesgo de contenido patrocinado); propiedad no declarada en la página consultada.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «site:expansion.com mercados»; WebFetch: sí)
- **Origen:** Alta 2026-11-02 (F9_S1).

#### RF-0260 · Q 58 (C) — MarketScreener

- **Canal oficial (URL raíz):** https://www.marketscreener.com/ (ejemplo leído: https://www.marketscreener.com/news/bofa-sees-resilient-consumers-despite-higher-gas-prices-ce7f59d8de8aff26)
- **Emisor:** Surperformance SAS (grupo Zonebourse)
- **Temática:** TF-03 Prensa financiera y agencias de noticias (principal) · secundarias: TF-06
- **Calidad Q:** 58 (C) — Primariedad 8/20 · Historial 10/20 · Transparencia 8/15 · Autoridad 8/15 · Independencia 7/10 · Actualidad 10/10 · Acceso 7/10
- **Tipología:** agregador (noticias sindicadas de MT Newswires, datos de FactSet, Morningstar y S&P Capital IQ)
- **Acceso:** Abierto con registro; funciones de suscripción
- **Ámbitos:** Noticias breves por empresa, calendarios económicos y corporativos, cotizaciones, filtros
- **Motivo de inclusión y uso:** Agregador multimercado con ediciones por país, útil para localizar noticias y calendarios por emisor. Uso: localización; se cita la fuente original (regla F9 b).
- **Sesgos y cautelas:** Contenido mayoritariamente sindicado; las marcas de tiempo pueden no coincidir con la publicación original.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Bank of America Institute Consumer Checkpoint»; WebFetch: sí)
- **Origen:** Alta 2026-11-02 (F9_S1, tanda 3).

#### RF-0225 · Q 57 (C) — InvestmentNews

- **Canal oficial (URL raíz):** https://www.investmentnews.com/ (ejemplo leído: https://www.investmentnews.com/companies/bridgewater-associates/264888?page=1)
- **Emisor:** KM Business Information US, Inc. (Key Media)
- **Temática:** TF-03 Prensa financiera y agencias de noticias (principal) · secundarias: TF-04
- **Calidad Q:** 57 (C) — Primariedad 10/20 · Historial 10/20 · Transparencia 8/15 · Autoridad 9/15 · Independencia 7/10 · Actualidad 9/10 · Acceso 4/10
- **Tipología:** secundaria especializada
- **Acceso:** Muro de pago (suscripción digital)
- **Ámbitos:** Industria de asesoramiento financiero y gestión de patrimonios de EE. UU.; noticias por gestora (p. ej., Bridgewater)
- **Motivo de inclusión y uso:** Seguimiento de la industria de asesores y gestoras en EE. UU. Uso: contexto sectorial; nunca como prueba de hechos.
- **Sesgos y cautelas:** Orientada a profesionales del asesoramiento; muro de pago.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** MURO_PAGO
- **Última verificación:** 2026-11-02 (búsqueda web: «Bridgewater Associates research and insights Daily Observations»; WebFetch: sí)
- **Origen:** Alta 2026-11-02 (F9_S1, tanda 2).

#### RF-0259 · Q 57 (C) — Investment Week

- **Canal oficial (URL raíz):** https://www.investmentweek.co.uk/
- **Emisor:** Incisive Business Media Limited (red Arc de Incisive Media)
- **Temática:** TF-03 Prensa financiera y agencias de noticias (principal) · secundarias: TF-04
- **Calidad Q:** 57 (C) — Primariedad 10/20 · Historial 10/20 · Transparencia 7/15 · Autoridad 9/15 · Independencia 5/10 · Actualidad 9/10 · Acceso 7/10
- **Tipología:** secundaria especializada
- **Acceso:** Abierto con registro
- **Ámbitos:** Industria de fondos del Reino Unido: fondos, investment trusts, ETF, gestión de patrimonios, regulación
- **Motivo de inclusión y uso:** Actualidad de gestoras y fondos británicos (cambios de gestores, flujos, lanzamientos). Uso: vigilancia sectorial.
- **Sesgos y cautelas:** Publica contenido patrocinado de gestoras («Partner Insight», «Industry Voice», rutas «/sponsored/»), p. ej., de PIMCO. Excluir ese contenido como evidencia.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «PIMCO secular outlook cyclical outlook insights pimco.com»; WebFetch: sí)
- **Origen:** Alta 2026-11-02 (F9_S1, tanda 3).

#### RF-0258 · Q 56 (C) — WealthBriefing

- **Canal oficial (URL raíz):** https://www.wealthbriefing.com/
- **Emisor:** ClearView Financial Media Ltd (Londres); títulos hermanos WealthBriefing Asia y Family Wealth Report
- **Temática:** TF-03 Prensa financiera y agencias de noticias (principal) · secundarias: TF-04
- **Calidad Q:** 56 (C) — Primariedad 9/20 · Historial 10/20 · Transparencia 7/15 · Autoridad 8/15 · Independencia 6/10 · Actualidad 9/10 · Acceso 7/10
- **Tipología:** secundaria especializada
- **Acceso:** Mixto (registro y suscripción)
- **Ámbitos:** Gestión de patrimonios y banca privada: gestoras, family offices, alternativos, regulación
- **Motivo de inclusión y uso:** Actualidad de la industria de patrimonios a escala global. Uso: vigilancia de tendencias de banca privada y family offices.
- **Sesgos y cautelas:** El negocio incluye premios y eventos con la propia industria.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «UBS Global Investment Returns Yearbook 2026 Dimson Marsh Staunton»; WebFetch: sí)
- **Origen:** Alta 2026-11-02 (F9_S1, tanda 3).

#### RF-0257 · Q 55 (C) — Mondo Visione

- **Canal oficial (URL raíz):** https://mondovisione.com/
- **Emisor:** Mondo Visione
- **Temática:** TF-03 Prensa financiera y agencias de noticias (principal) · secundarias: TF-02
- **Calidad Q:** 55 (C) — Primariedad 9/20 · Historial 10/20 · Transparencia 6/15 · Autoridad 8/15 · Independencia 7/10 · Actualidad 9/10 · Acceso 6/10
- **Tipología:** agregador especializado (reproduce comunicados de bolsas, reguladores y empresas)
- **Acceso:** Noticias abiertas; zona de miembros con suscripción
- **Ámbitos:** Bolsas e infraestructuras de mercado; directorio de bolsas; índice FTSE Mondo Visione Exchanges
- **Motivo de inclusión y uso:** Archivo largo de comunicados de bolsas y reguladores (p. ej., de 2009). Uso: localizar comunicados antiguos de infraestructuras de mercado y citarlos en su fuente original.
- **Sesgos y cautelas:** Mayormente reproduce comunicados; no aporta verificación propia.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Reuters Breakingviews financial commentary»; WebFetch: sí)
- **Origen:** Alta 2026-11-02 (F9_S1, tanda 3).

## TF-04 Grandes inversores, gestoras y cartas de inversión

#### RF-0245 · Q 85 (A) — Norges Bank Investment Management (fondo soberano noruego, GPFG)

- **Canal oficial (URL raíz):** https://www.nbim.no/ (sobre el fondo: https://www.nbim.no/en/about-us/)
- **Emisor:** Norges Bank Investment Management (Norges Bank), gestor del Government Pension Fund Global
- **Temática:** TF-04 Grandes inversores, gestoras y cartas de inversión (principal) · secundarias: TF-06
- **Calidad Q:** 85 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 15/15 · Autoridad 14/15 · Independencia 9/10 · Actualidad 7/10 · Acceso 10/10
- **Tipología:** primaria
- **Acceso:** Abierto (datos de posiciones con condiciones de uso, también en Snowflake Marketplace)
- **Ámbitos:** Uno de los mayores fondos del mundo: publicación de posiciones totales, votaciones en juntas, informe anual y de inversión responsable
- **Motivo de inclusión y uso:** Gran inversor muy transparente, con posiciones y votos publicados. Próximas fechas: cifras clave el 28/01/2027 e informe anual el 26/02/2027. Uso: posicionamiento del mayor accionista institucional europeo y señales ASG.
- **Sesgos y cautelas:** Mandato fijado por el Ministerio de Finanzas noruego (exclusiones éticas); posiciones con frecuencia semestral o anual.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Norges Bank Investment Management government pension fund global holdings nbim.no»; WebFetch: sí)
- **Origen:** Alta 2026-11-02 (F9_S1, tanda 3).

#### RF-0044 · Q 82 (A) — SEC EDGAR — formularios 13F (posiciones de grandes gestores)

- **Canal oficial (URL raíz):** https://www.sec.gov/ (FAQ del Form 13F: https://www.sec.gov/divisions/investment/13ffaq; búsqueda de presentaciones en EDGAR)
- **Emisor:** U.S. Securities and Exchange Commission
- **Temática:** TF-04 Grandes inversores, gestoras y cartas de inversión (principal) · secundarias: TF-02, TF-06
- **Calidad Q:** 82 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 14/15 · Independencia 9/10 · Actualidad 6/10 · Acceso 10/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** Posiciones trimestrales de gestores institucionales con discreción sobre ≥ 100 M USD en valores 13(f)
- **Motivo de inclusión y uso:** Movimientos documentados de grandes inversores. Presentación obligatoria en EDGAR dentro de los 45 días siguientes al cierre del trimestre (p. ej., 15/05/2026 para el trimestre de marzo de 2026). Pieza especializada del portal general RF-0002.
- **Sesgos y cautelas:** Desfase de hasta 45 días; solo posiciones largas en valores 13(f) de EE. UU.; tratamiento confidencial posible para algunas posiciones.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «SEC Form 13F frequently asked questions institutional investment managers»; WebFetch: sí)
- **Origen:** Semilla V3.0 (2026-11-01) confirmada en verificación de alta 2026-11-02 (tanda 2); URL raíz corregida a la FAQ oficial del 13F.

#### RF-0247 · Q 80 (A) — Temasek — Temasek Review

- **Canal oficial (URL raíz):** https://www.temasek.com.sg/ (nota de resultados 2026: https://www.temasek.com.sg/en/news-and-resources/news-room/news/2026/temasek-net-portfolio-value-grows-to-518b-up-49b-from-last-year · Temasek Review: https://www.temasekreview.com.sg/media-centre.html)
- **Emisor:** Temasek Holdings (Private) Limited (Singapur)
- **Temática:** TF-04 Grandes inversores, gestoras y cartas de inversión (principal) · secundarias: TF-11
- **Calidad Q:** 80 (A) — Primariedad 19/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 14/15 · Independencia 8/10 · Actualidad 6/10 · Acceso 10/10
- **Tipología:** primaria
- **Acceso:** Abierto (informe, gráficos descargables y presentación)
- **Ámbitos:** Valor neto de cartera (518.000 M SGD a 31/03/2026), rentabilidad total para el accionista a 1, 5, 10 y 20 años, asignación por segmentos y objetivos temáticos (IA, infraestructura core-plus, crédito privado)
- **Motivo de inclusión y uso:** Inversor soberano con objetivos de asignación explícitos a cinco años (p. ej., IA del 6 % al 15 % hacia el ejercicio 2031). Uso: tendencias de asignación de grandes inversores de largo plazo.
- **Sesgos y cautelas:** Autoinforme anual; valoración de no cotizadas a mercado desde 2026 (cambio de método).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Temasek Review 2026 net portfolio value»; WebFetch: sí)
- **Origen:** Alta 2026-11-02 (F9_S1, tanda 3).

#### RF-0037 · Q 78 (B) — Berkshire Hathaway — cartas anuales a los accionistas

- **Canal oficial (URL raíz):** www.berkshirehathaway.com (según Wikipedia; el archivo de cartas está alojado en ese sitio, la ruta concreta queda pendiente del barrido HT-02)
- **Emisor:** Berkshire Hathaway Inc.
- **Temática:** TF-04 Grandes inversores, gestoras y cartas de inversión (principal)
- **Calidad Q:** 78 (B) — Primariedad 18/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 14/15 · Independencia 8/10 · Actualidad 6/10 · Acceso 10/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** Filosofía de inversión de largo plazo; asignación de capital
- **Motivo de inclusión y uso:** Fuente original del pensamiento de un gran inversor; señal de posicionamiento junto a su 13F (RF-0044).
- **Sesgos y cautelas:** Perspectiva de un inversor con cartera propia; frecuencia anual; las búsquedas devolvieron sobre todo copias de terceros (usar solo el sitio oficial).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Berkshire Hathaway shareholder letters Warren Buffett letters.html»; ruta: artículo de Wikipedia «Berkshire Hathaway»; WebFetch: sí, sobre Wikipedia)
- **Origen:** Semilla V3.0 (2026-11-01) confirmada en verificación de alta 2026-11-02 (tanda 2), por vía Wikipedia.

#### RF-0226 · Q 77 (B) — Fairfax Financial — cartas anuales de Prem Watsa

- **Canal oficial (URL raíz):** www.fairfax.ca (según Wikipedia)
- **Emisor:** Fairfax Financial Holdings Limited (Toronto; fundador, presidente y consejero delegado: V. Prem Watsa)
- **Temática:** TF-04 Grandes inversores, gestoras y cartas de inversión (principal)
- **Calidad Q:** 77 (B) — Primariedad 18/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 13/15 · Independencia 8/10 · Actualidad 6/10 · Acceso 10/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** Carta anual (marzo, con resultados) sobre suscripción de seguros, filosofía de inversión valor, cartera y visión de mercados y economía
- **Motivo de inclusión y uso:** Carta de referencia en la comunidad value, con apuestas macro explícitas (coberturas deflacionarias, crédito) que el Evaluador puede contrastar. Uso: posicionamiento y tesis de un gran inversor asegurador.
- **Sesgos y cautelas:** Perspectiva de un inversor con cartera propia; frecuencia anual.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Fairfax Financial Prem Watsa annual letter shareholders Markel annual letter Pershing Square annual letter» → artículo de Wikipedia «Fairfax Financial»; WebFetch: sí, sobre Wikipedia)
- **Origen:** Alta 2026-11-02 (F9_S1, tanda 2).

#### RF-0246 · Q 77 (B) — GIC (fondo soberano de Singapur) — GIC Report

- **Canal oficial (URL raíz):** https://www.gic.com.sg/ (preguntas frecuentes: https://www.gic.com.sg/who-we-are/faqs/)
- **Emisor:** GIC Private Limited (propiedad del Gobierno de Singapur, fundada en 1981)
- **Temática:** TF-04 Grandes inversores, gestoras y cartas de inversión (principal)
- **Calidad Q:** 77 (B) — Primariedad 18/20 · Historial 10/20 · Transparencia 10/15 · Autoridad 14/15 · Independencia 8/10 · Actualidad 7/10 · Acceso 10/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** Rentabilidad real anualizada a 20 años (3,4 % al 31/03/2026, GIC Report 2025/26), rentabilidades nominales a 5, 10 y 20 años en USD, distribución por activos y geografías
- **Motivo de inclusión y uso:** Señal de asignación de un gran gestor de reservas. Uso: tendencias de asignación de inversores soberanos.
- **Sesgos y cautelas:** No publica patrimonio gestionado, posiciones concretas ni rentabilidades a un año; transparencia limitada a propósito.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «GIC Report annual 20-year real rate of return gic.com.sg»; WebFetch: sí)
- **Origen:** Alta 2026-11-02 (F9_S1, tanda 3).

#### RF-0038 · Q 75 (B) — Oaktree Capital — memos de Howard Marks

- **Canal oficial (URL raíz):** https://cnt.oaktreecapital.com/insights (enlace «Memos from Howard Marks» del propio sitio; aniversario: https://cnt.oaktreecapital.com/insights/memo-podcast/35-years-of-memos) · Recopilación completa 1990–2025 enlazada desde Brookfield Oaktree Wealth Solutions: https://privatewealth.brookfield.com/insight/35-years-memos-howard-marks
- **Emisor:** Oaktree Capital Management (grupo Brookfield)
- **Temática:** TF-04 Grandes inversores, gestoras y cartas de inversión (principal)
- **Calidad Q:** 75 (B) — Primariedad 17/20 · Historial 10/20 · Transparencia 11/15 · Autoridad 14/15 · Independencia 6/10 · Actualidad 8/10 · Acceso 9/10
- **Tipología:** primaria
- **Acceso:** Abierto (registro opcional; la página de Brookfield exige elegir región)
- **Ámbitos:** Ciclos de mercado, crédito, psicología del inversor
- **Motivo de inclusión y uso:** Memos publicados desde 1990 (35 años en octubre de 2025) por el cofundador de un gestor de crédito de referencia. Uso: detectar fases del ciclo y el sentimiento del crédito.
- **Sesgos y cautelas:** Gestora con productos propios (incluidos fondos de crédito comercializados por Brookfield).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Howard Marks memos Oaktree Capital insights»; WebFetch: sí)
- **Origen:** Semilla V3.0 (2026-11-01) confirmada en verificación de alta 2026-11-02 (tanda 2); URL corregida (subdominio cnt. y ruta /insights).

#### RF-0040 · Q 75 (B) — AQR — investigación

- **Canal oficial (URL raíz):** https://www.aqr.com/ (Data Library: https://www.aqr.com/insights/datasets/an-academic-quality-data-library-for-practitioners)
- **Emisor:** AQR Capital Management, LLC
- **Temática:** TF-04 Grandes inversores, gestoras y cartas de inversión (principal) · secundarias: TF-06, TF-13
- **Calidad Q:** 75 (B) — Primariedad 16/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 13/15 · Independencia 6/10 · Actualidad 8/10 · Acceso 10/10
- **Tipología:** primaria (investigación propia y datos)
- **Acceso:** Abierto (datos en Excel con pestaña de condiciones de uso; atribución a AQR)
- **Ámbitos:** Factores (valor, momento, baja beta), seguimiento de tendencia, carry, primas alternativas
- **Motivo de inclusión y uso:** Investigación cuantitativa con datos públicos: series de los artículos de sus investigadores (p. ej., Asness-Moskowitz-Pedersen 2013; Frazzini-Pedersen 2014; Moskowitz-Ooi-Pedersen 2012). Uso: series de factores para el Motor de Cálculo y contexto de primas de riesgo.
- **Sesgos y cautelas:** Gestora que comercializa las estrategias que estudia; las series reproducen carteras de los artículos, no productos reales.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «AQR Capital Management research insights papers»; WebFetch: sí)
- **Origen:** Semilla V3.0 (2026-11-01) confirmada en verificación de alta 2026-11-02 (tanda 2); la ruta «/Insights/Research» de la semilla no se ha comprobado (usar la raíz).

#### RF-0252 · Q 74 (B) — Pershing Square Holdings — informes y cartas de Bill Ackman

- **Canal oficial (URL raíz):** https://pershingsquareholdings.com/
- **Emisor:** Pershing Square Holdings, Ltd. (vehículo cotizado gestionado por Pershing Square Capital Management; tickers LN:PSH y NA:PSH)
- **Temática:** TF-04 Grandes inversores, gestoras y cartas de inversión (principal)
- **Calidad Q:** 74 (B) — Primariedad 18/20 · Historial 10/20 · Transparencia 11/15 · Autoridad 12/15 · Independencia 6/10 · Actualidad 8/10 · Acceso 9/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** Valor liquidativo y rentabilidades, informes y estados mensuales, fichas mensuales, cartera, presentaciones e informes periódicos
- **Motivo de inclusión y uso:** Vehículo cotizado de un inversor activista con cartera concentrada y publicación mensual. Uso: posicionamiento y tesis de un gran inversor activista, junto a su 13F (RF-0044).
- **Sesgos y cautelas:** Inversor con posiciones y tesis públicas propias; la página leída es un comunicado de 2018 (las cartas anuales no se comprobaron directamente).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Pershing Square Holdings annual letter Bill Ackman Markel Group Tom Gayner letter»; WebFetch: sí)
- **Origen:** Alta 2026-11-02 (F9_S1, tanda 3).

#### RF-0043 · Q 73 (B) — Vanguard — investigación y perspectivas económicas

- **Canal oficial (URL raíz):** https://corporate.vanguard.com/ (outlook 2026: https://corporate.vanguard.com/content/dam/corp/research/pdf/isg_vemo_2026.pdf · nota de prensa: https://corporate.vanguard.com/content/corporatesite/us/en/corp/who-we-are/pressroom/press-release-vanguard-releases-2026-economic-and-market-outlook-121025.html)
- **Emisor:** The Vanguard Group
- **Temática:** TF-04 Grandes inversores, gestoras y cartas de inversión (principal)
- **Calidad Q:** 73 (B) — Primariedad 15/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 13/15 · Independencia 6/10 · Actualidad 8/10 · Acceso 9/10
- **Tipología:** primaria (previsiones propias)
- **Acceso:** Abierto
- **Ámbitos:** Previsiones de rentabilidad a 5–10 años (Vanguard Capital Markets Model, 10.000 simulaciones por clase de activo), macro, costes, comportamiento inversor
- **Motivo de inclusión y uso:** Previsiones explícitas y contrastables (outlook 2026, «AI exuberance: Economic upside, stock market downside», 10/12/2025: renta variable de EE. UU. con un 4–5 % anual a 5–10 años). Uso: previsiones para el Evaluador y escenario de consenso institucional.
- **Sesgos y cautelas:** Sesgo hacia la gestión indexada; proyecciones hipotéticas.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Vanguard economic and market outlook 2026»; WebFetch: sí)
- **Origen:** Semilla V3.0 (2026-11-01) confirmada en verificación de alta 2026-11-02 (tanda 2).

#### RF-0039 · Q 72 (B) — GMO — investigación y previsiones a 7 años

- **Canal oficial (URL raíz):** https://gmo.com/ (previsión de marzo de 2025: https://gmo.com/globalassets/articles/gmo-7-year-asset-class-forecast/2025/gmo-7-year-asset-class-forecast-mar25.pdf)
- **Emisor:** GMO LLC
- **Temática:** TF-04 Grandes inversores, gestoras y cartas de inversión (principal)
- **Calidad Q:** 72 (B) — Primariedad 16/20 · Historial 10/20 · Transparencia 11/15 · Autoridad 13/15 · Independencia 6/10 · Actualidad 7/10 · Acceso 9/10
- **Tipología:** primaria (previsiones propias)
- **Acceso:** Abierto (algunos contenidos con registro)
- **Ámbitos:** Previsiones de rentabilidad real a 7 años por clase de activo, con dos escenarios de tipo real de equilibrio (1,3 % y 0,0 %)
- **Motivo de inclusión y uso:** Previsiones explícitas y contrastables, útiles para el Evaluador; republicadas periódicamente (la de julio de 2026 aparece sindicada en Advisor Perspectives, que no cuenta como fuente independiente).
- **Sesgos y cautelas:** Sesgo valor persistente; gestora con productos; las previsiones no son garantías.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «GMO 7-year asset class forecast»; WebFetch: sí)
- **Origen:** Semilla V3.0 (2026-11-01) confirmada en verificación de alta 2026-11-02 (tanda 2).

#### RF-0042 · Q 72 (B) — BlackRock Investment Institute

- **Canal oficial (URL raíz):** https://www.blackrock.com/corporate/insights/blackrock-investment-institute
- **Emisor:** BlackRock
- **Temática:** TF-04 Grandes inversores, gestoras y cartas de inversión (principal)
- **Calidad Q:** 72 (B) — Primariedad 15/20 · Historial 10/20 · Transparencia 11/15 · Autoridad 13/15 · Independencia 5/10 · Actualidad 9/10 · Acceso 9/10
- **Tipología:** secundaria cualificada (visión de gestora)
- **Acceso:** Abierto
- **Ámbitos:** Weekly Market Commentary, Global Investment Outlook trimestral (Q4 2026: 15/09/2026), Geopolitical Risk Dashboard, Capital Market Assumptions
- **Motivo de inclusión y uso:** Visión del mayor gestor del mundo; señal de consenso institucional. El panel de riesgo geopolítico es útil para escenarios.
- **Sesgos y cautelas:** Comercializa productos ligados a sus tesis.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «BlackRock Investment Institute weekly commentary»; WebFetch: sí)
- **Origen:** Semilla V3.0 (2026-11-01) confirmada en verificación de alta 2026-11-02 (tanda 2).

#### RF-0227 · Q 72 (B) — Thinking Ahead Institute (WTW) — estudio P&I 500 de grandes gestoras

- **Canal oficial (URL raíz):** https://www.thinkingaheadinstitute.org/ (edición 2024: https://www.thinkingaheadinstitute.org/?p=23724)
- **Emisor:** Thinking Ahead Institute (WTW), con Pensions & Investments
- **Temática:** TF-04 Grandes inversores, gestoras y cartas de inversión (principal) · secundarias: TF-06
- **Calidad Q:** 72 (B) — Primariedad 15/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 13/15 · Independencia 8/10 · Actualidad 6/10 · Acceso 8/10
- **Tipología:** primaria (estudio propio)
- **Acceso:** Abierto (PDF descargable; área de miembros con registro)
- **Ámbitos:** Ranking anual de las 500 mayores gestoras por activos discrecionales (2023: 128,0 billones de USD); concentración y tendencias de la industria
- **Motivo de inclusión y uso:** Mapa de quiénes son los grandes inversores y cómo evoluciona la concentración de la gestión. Uso: ponderar la relevancia de gestoras y detectar flujos estructurales (pasiva, privados).
- **Sesgos y cautelas:** Datos autodeclarados por las gestoras; frecuencia anual con desfase de un año.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «list of largest asset management companies wikipedia»; WebFetch: sí)
- **Origen:** Alta 2026-11-02 (F9_S1, tanda 2).

#### RF-0248 · Q 72 (B) — PIMCO — perspectivas cíclicas y seculares

- **Canal oficial (URL raíz):** https://www.pimco.com/ (Cyclical Outlook: https://www.pimco.com/insights/cyclical-outlook)
- **Emisor:** PIMCO
- **Temática:** TF-04 Grandes inversores, gestoras y cartas de inversión (principal)
- **Calidad Q:** 72 (B) — Primariedad 15/20 · Historial 10/20 · Transparencia 11/15 · Autoridad 14/15 · Independencia 5/10 · Actualidad 9/10 · Acceso 8/10
- **Tipología:** secundaria cualificada (visión de gestora)
- **Acceso:** Abierto (por región)
- **Ámbitos:** Perspectivas cíclicas y seculares de renta fija, tipos, crédito y macro; comentarios de mercado
- **Motivo de inclusión y uso:** Visión de una de las mayores gestoras de renta fija del mundo. Uso: consenso institucional sobre tipos y crédito.
- **Sesgos y cautelas:** Gestora con productos ligados a sus tesis; la página de índice se cargó sin contenido renderizado.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «PIMCO secular outlook cyclical outlook insights pimco.com»; WebFetch: sí, página sin contenido renderizado)
- **Origen:** Alta 2026-11-02 (F9_S1, tanda 3).

#### RF-0249 · Q 71 (B) — Amundi Investment Institute — Research Center

- **Canal oficial (URL raíz):** https://research-center.amundi.com/ (Global Investment Views: https://research-center.amundi.com/publications/global-investment-views)
- **Emisor:** Amundi (Amundi Investment Institute)
- **Temática:** TF-04 Grandes inversores, gestoras y cartas de inversión (principal) · secundarias: TF-05
- **Calidad Q:** 71 (B) — Primariedad 14/20 · Historial 10/20 · Transparencia 11/15 · Autoridad 13/15 · Independencia 5/10 · Actualidad 10/10 · Acceso 8/10
- **Tipología:** secundaria cualificada (visión de gestora)
- **Acceso:** Abierto con aceptación de condiciones (dirigido a profesionales no estadounidenses)
- **Ámbitos:** Global Investment Views mensual (última: octubre de 2026), convicciones de los CIO, estrategia de mercados e investigación académica
- **Motivo de inclusión y uso:** Visión de la mayor gestora europea. Uso: consenso institucional europeo y asignación táctica.
- **Sesgos y cautelas:** Gestora con productos; audiencia profesional.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Amundi Investment Institute outlook research»; WebFetch: sí)
- **Origen:** Alta 2026-11-02 (F9_S1, tanda 3).

#### RF-0250 · Q 70 (B) — Man Group — Insights

- **Canal oficial (URL raíz):** https://www.man.com/insights
- **Emisor:** Man Group (vinculado al Oxford–Man Institute)
- **Temática:** TF-04 Grandes inversores, gestoras y cartas de inversión (principal) · secundarias: TF-13
- **Calidad Q:** 70 (B) — Primariedad 14/20 · Historial 10/20 · Transparencia 11/15 · Autoridad 13/15 · Independencia 5/10 · Actualidad 9/10 · Acceso 8/10
- **Tipología:** secundaria cualificada (investigación de gestora cuantitativa)
- **Acceso:** Abierto (pide elegir región y perfil profesional)
- **Ámbitos:** Investigación de inversión, análisis de mercado y trabajos con universidades (sección Views From the Floor)
- **Motivo de inclusión y uso:** Investigación de uno de los mayores gestores alternativos y cuantitativos. Uso: análisis de tendencia, factores y riesgo desde la óptica de un hedge fund.
- **Sesgos y cautelas:** Gestora con estrategias propias.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Schroders insights economic and strategy viewpoint Man Group Man Institute»; WebFetch: sí)
- **Origen:** Alta 2026-11-02 (F9_S1, tanda 3).

#### RF-0251 · Q 69 (B) — Schroders — News and Insights

- **Canal oficial (URL raíz):** https://www.schroders.com/ (página leída: https://www.schroders.com/en/global/individual/)
- **Emisor:** Schroders (integrada con Nuveen desde el 1/10/2026; unos 2,6 billones de USD gestionados en conjunto)
- **Temática:** TF-04 Grandes inversores, gestoras y cartas de inversión (principal)
- **Calidad Q:** 69 (B) — Primariedad 13/20 · Historial 10/20 · Transparencia 11/15 · Autoridad 12/15 · Independencia 5/10 · Actualidad 9/10 · Acceso 9/10
- **Tipología:** secundaria cualificada (visión de gestora)
- **Acceso:** Abierto
- **Ámbitos:** Economía, mercados, mercados privados, sostenibilidad, CIO Lens
- **Motivo de inclusión y uso:** Visión de una gran gestora británica con equipo de economistas propio. Uso: consenso institucional y temas de mercados privados.
- **Sesgos y cautelas:** Cambio de propiedad reciente (integración con Nuveen): vigilar cambios de sitio y de línea de análisis.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Schroders insights economic and strategy viewpoint Man Group Man Institute»; WebFetch: sí)
- **Origen:** Alta 2026-11-02 (F9_S1, tanda 3).

#### RF-0041 · Q 68 (B) — Bridgewater Associates — investigación pública

- **Canal oficial (URL raíz):** https://www.bridgewater.com/research-and-insights (enlace de navegación del sitio oficial; página leída: https://www.bridgewater.com/people/jim-haskel)
- **Emisor:** Bridgewater Associates, LP
- **Temática:** TF-04 Grandes inversores, gestoras y cartas de inversión (principal)
- **Calidad Q:** 68 (B) — Primariedad 15/20 · Historial 10/20 · Transparencia 9/15 · Autoridad 13/15 · Independencia 6/10 · Actualidad 9/10 · Acceso 6/10
- **Tipología:** secundaria cualificada (visión de gestora)
- **Acceso:** Parcialmente abierto
- **Ámbitos:** Macro global, deuda, ciclos
- **Motivo de inclusión y uso:** Visión macro de un gran fondo; solo la parte pública es utilizable.
- **Sesgos y cautelas:** Las Daily Observations completas son de acceso restringido; circulan copias no autorizadas en sitios de terceros (no usar); gestora con posiciones.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Bridgewater Associates research and insights Daily Observations»; WebFetch: sí, sobre una página del sitio oficial; la sección de investigación no se leyó)
- **Origen:** Semilla V3.0 (2026-11-01) confirmada en verificación de alta 2026-11-02 (tanda 2).

#### RF-0253 · Q 55 (C) — Global Pension Transparency Benchmark (Top1000funds y CEM Benchmarking)

- **Canal oficial (URL raíz):** https://global-pension-transparency-benchmark.top1000funds.com/ (ficha del GPFG: https://global-pension-transparency-benchmark.top1000funds.com/global-pension-transparency-benchmark-funds-2022/government-pension-fund-global)
- **Emisor:** Top1000funds.com
- **Temática:** TF-04 Grandes inversores, gestoras y cartas de inversión (principal)
- **Calidad Q:** 55 (C) — Primariedad 12/20 · Historial 10/20 · Transparencia 9/15 · Autoridad 10/15 · Independencia 7/10 · Actualidad 2/10 · Acceso 5/10
- **Tipología:** secundaria (calificaciones de transparencia)
- **Acceso:** Abierto
- **Ámbitos:** Puntuaciones de transparencia de grandes fondos de pensiones y soberanos (global, costes, gobernanza, rentabilidad, inversión responsable)
- **Motivo de inclusión y uso:** Permite ponderar cuánto fiarse de la información publicada por cada gran inversor institucional. Uso: contexto de calidad de divulgación de las fichas de TF-04.
- **Sesgos y cautelas:** El proyecto terminó tras cinco años (datos históricos, sin actualización); metodología no descrita en la página leída.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Norges Bank Investment Management government pension fund global holdings nbim.no»; WebFetch: sí)
- **Origen:** Alta 2026-11-02 (F9_S1, tanda 3).

#### RF-0228 · Q 52 (C) — Hedge Fund Alpha — base de datos de cartas de inversores

- **Canal oficial (URL raíz):** https://hedgefundalpha.com/ (ejemplo: https://hedgefundalpha.com/investor-letters/old-west-investment-management-annual-letter/)
- **Emisor:** Hedge Fund Alpha (vinculado a ValueWalk según los metadatos; editor no declarado)
- **Temática:** TF-04 Grandes inversores, gestoras y cartas de inversión (principal)
- **Calidad Q:** 52 (C) — Primariedad 8/20 · Historial 10/20 · Transparencia 6/15 · Autoridad 7/15 · Independencia 6/10 · Actualidad 8/10 · Acceso 7/10
- **Tipología:** agregador (reproduce cartas de terceros)
- **Acceso:** Mayormente abierto; productos de suscripción
- **Ámbitos:** Cartas trimestrales y anuales de hedge funds y gestoras valor; base de datos de cartas
- **Motivo de inclusión y uso:** Localizador de cartas de gestores sin web propia accesible. Uso: solo para encontrar la carta; se cita el PDF original del gestor (regla F9 b: las copias sindicadas no son fuentes independientes).
- **Sesgos y cautelas:** Editor poco transparente; reproducciones sin garantía de integridad; promoción de productos de pago.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Fairfax Financial Prem Watsa annual letter shareholders Markel annual letter Pershing Square annual letter»; WebFetch: sí)
- **Origen:** Alta 2026-11-02 (F9_S1, tanda 2).

## TF-05 Análisis de bancos de inversión y casas de análisis

#### RF-0241 · Q 81 (A) — UBS Global Investment Returns Yearbook (Dimson, Marsh y Staunton)

- **Canal oficial (URL raíz):** https://www.ubs.com/global/en/investment-bank/insights-and-data/articles/global-investment-returns-yearbook-2026.html (resumen público: https://www.ubs.com/content/dam/assets/wm/static/cio/documents/giry2026-summary-public.pdf)
- **Emisor:** UBS, con Elroy Dimson (Cambridge) y Paul Marsh y Mike Staunton (London Business School)
- **Temática:** TF-05 Análisis de bancos de inversión y casas de análisis (principal) · secundarias: TF-06, TF-13
- **Calidad Q:** 81 (A) — Primariedad 17/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 8/10 · Actualidad 7/10 · Acceso 10/10
- **Tipología:** primaria (base de datos DMS propia) y secundaria
- **Acceso:** Resumen público en PDF; informe completo para clientes de UBS Investment Bank (UBS Neo)
- **Ámbitos:** Rentabilidades anuales de acciones, bonos, letras, inflación, divisas y, desde 2026, oro, en 35 mercados desde 1900 (126 años)
- **Motivo de inclusión y uso:** Referencia de rentabilidades y primas de riesgo de muy largo plazo. Uso: supuestos de largo plazo del Motor de Cálculo y contraste de narrativas.
- **Sesgos y cautelas:** Informe completo restringido; el título HTML de la página decía «2025» aunque el contenido era de 2026.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «UBS Global Investment Returns Yearbook 2026 Dimson Marsh Staunton»; WebFetch: sí)
- **Origen:** Alta 2026-11-02 (F9_S1, tanda 3).

#### RF-0235 · Q 78 (B) — FactSet Insight — Earnings Insight (John Butters)

- **Canal oficial (URL raíz):** https://insight.factset.com/ (ejemplo: https://insight.factset.com/sp-500-earnings-season-update-february-13-2026)
- **Emisor:** FactSet (John Butters, Vice President y Senior Earnings Analyst)
- **Temática:** TF-05 Análisis de bancos de inversión y casas de análisis (principal) · secundarias: TF-06
- **Calidad Q:** 78 (B) — Primariedad 16/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 13/15 · Independencia 8/10 · Actualidad 10/10 · Acceso 8/10
- **Tipología:** primaria (agregados de consenso propios)
- **Acceso:** Abierto
- **Ámbitos:** Temporada de resultados del S&P 500: crecimiento combinado de beneficios e ingresos, porcentaje de sorpresas positivas, PER adelantado a 12 meses frente a medias a 5 y 10 años
- **Motivo de inclusión y uso:** Serie semanal de referencia sobre beneficios y valoración del S&P 500 (p. ej., 13/02/2026: beneficio combinado del 4T 2025 +13,2 %, PER adelantado de 21,5). Uso: estado de los beneficios y del consenso.
- **Sesgos y cautelas:** Basada en el consenso de analistas (sesgo optimista conocido de las previsiones).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «FactSet Earnings Insight John Butters S&P 500»; WebFetch: sí)
- **Origen:** Alta 2026-11-02 (F9_S1, tanda 3).

#### RF-0242 · Q 75 (B) — Bank of America Institute — Consumer Checkpoint

- **Canal oficial (URL raíz):** https://institute.bankofamerica.com/ (Consumer Checkpoint: https://institute.bankofamerica.com/bank-of-america-institute/consumer-checkpoint.html)
- **Emisor:** Bank of America Institute
- **Temática:** TF-05 Análisis de bancos de inversión y casas de análisis (principal) · secundarias: TF-01
- **Calidad Q:** 75 (B) — Primariedad 16/20 · Historial 10/20 · Transparencia 10/15 · Autoridad 12/15 · Independencia 7/10 · Actualidad 10/10 · Acceso 10/10
- **Tipología:** primaria (datos propios del banco)
- **Acceso:** Abierto
- **Ámbitos:** Gasto del consumidor de EE. UU. con datos propios del banco; publicación mensual (última: octubre de 2026, «Strength in numbers»)
- **Motivo de inclusión y uso:** Indicador adelantado de consumo, anterior a las cifras oficiales. Uso: lectura temprana del consumo antes del dato de la BEA (RF-0023).
- **Sesgos y cautelas:** Muestra limitada a la clientela del banco; metodología resumida.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Bank of America Institute Consumer Checkpoint»; WebFetch: sí)
- **Origen:** Alta 2026-11-02 (F9_S1, tanda 3).

#### RF-0205 · Q 74 (B) — CaixaBank Research

- **Canal oficial (URL raíz):** https://www.caixabankresearch.com/ (ejemplo, Financial Markets Daily Report: https://www.caixabankresearch.com/en/publications/financial-markets-daily-report/04-may-2020)
- **Emisor:** CaixaBank (servicio de estudios)
- **Temática:** TF-05 Análisis de bancos de inversión y casas de análisis (principal) · secundarias: TF-01
- **Calidad Q:** 74 (B) — Primariedad 12/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 12/15 · Independencia 6/10 · Actualidad 10/10 · Acceso 10/10
- **Tipología:** secundaria cualificada (análisis de banco)
- **Acceso:** Abierto (ES, CA, EN; PDF descargables)
- **Ámbitos:** Economía española y portuguesa, mercados financieros, sectores, comunidades autónomas, consumo (Monitor de consumo), divisas; Informe Mensual, Pulso Económico Semanal, informe diario de mercados, documentos de trabajo
- **Motivo de inclusión y uso:** Servicio de estudios bancario español de acceso libre con publicaciones de alta frecuencia y datos propios de consumo. Uso: segunda opinión sobre coyuntura española frente a Banco de España e INE.
- **Sesgos y cautelas:** Visión de un banco comercial (conflicto de interés potencial en vivienda, crédito y renta variable española); aviso legal en la web de CaixaBank.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Cinco Días cincodias.elpais.com mercados financieros»; WebFetch: sí)
- **Origen:** Alta 2026-11-02 (F9_S1).

<!-- ===== Tanda 2 (2026-11-02): 22 búsquedas WebSearch. Las fichas siguientes se fusionan en su temática y por Q descendente. ===== -->
<!-- Vía «directorio FCA»: URL tomada de la página oficial de la FCA «Regulators in the EU and European Economic Area (EEA)» (https://www.fca.org.uk/firms/regulators-eu-eea, devuelta por búsqueda y leída con WebFetch); la propia FCA advierte que algunos enlaces pueden estar desactualizados. Vía «Wikipedia»: URL oficial leída en la ficha (infobox) del artículo de Wikipedia alcanzado desde una búsqueda. -->

#### RF-0232 · Q 74 (B) — ING THINK

- **Canal oficial (URL raíz):** https://think.ing.com/ (quiénes somos: https://think.ing.com/about/)
- **Emisor:** ING (más de 40 economistas)
- **Temática:** TF-05 Análisis de bancos de inversión y casas de análisis (principal)
- **Calidad Q:** 74 (B) — Primariedad 12/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 12/15 · Independencia 6/10 · Actualidad 10/10 · Acceso 10/10
- **Tipología:** secundaria cualificada (análisis de banco)
- **Acceso:** Abierto
- **Ámbitos:** Macro, bancos centrales, divisas (tabla mensual de previsiones FX Talking), materias primas, sectores; ING Monthly
- **Motivo de inclusión y uso:** Análisis bancario europeo abierto, con tablas de previsiones publicadas. Uso: previsiones de divisas y tipos para el Evaluador; consenso europeo.
- **Sesgos y cautelas:** Visión de un banco; la investigación profesional regulada está en otro portal.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «ING THINK economic and financial analysis think.ing.com»; WebFetch: sí)
- **Origen:** Alta 2026-11-02 (F9_S1, tanda 3).

#### RF-0238 · Q 74 (B) — Capital Economics

- **Canal oficial (URL raíz):** https://www.capitaleconomics.com/ (la empresa: https://capitaleconomics.com/about-us/the-company/)
- **Emisor:** Capital Economics (Londres, fundada en 1999)
- **Temática:** TF-05 Análisis de bancos de inversión y casas de análisis (principal)
- **Calidad Q:** 74 (B) — Primariedad 12/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 13/15 · Independencia 10/10 · Actualidad 10/10 · Acceso 7/10
- **Tipología:** secundaria cualificada (casa de análisis independiente)
- **Acceso:** Suscripción; algunos contenidos públicos
- **Ámbitos:** Macro y mercados de más de 100 economías, con más de 60 economistas; previsiones y modelos propios
- **Motivo de inclusión y uso:** Casa independiente sin banca de inversión, intermediación ni cartera propia. Uso: contrapunto independiente a los bancos de inversión y previsiones contrastables para el Evaluador.
- **Sesgos y cautelas:** Acceso mayoritariamente de pago.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Capital Economics independent macroeconomic research consultancy»; WebFetch: sí)
- **Origen:** Alta 2026-11-02 (F9_S1, tanda 3).

#### RF-0233 · Q 73 (B) — BNP Paribas Economic Research

- **Canal oficial (URL raíz):** https://economic-research.bnpparibas.com/ (equipos: https://economic-research.bnpparibas.com/Teams/en-US · Eco Flash: https://economic-research.bnpparibas.com/Publications/Eco-Flash/en-US)
- **Emisor:** BNP Paribas, departamento de estudios económicos (París; economista jefa del grupo: Isabelle Mateos y Lago)
- **Temática:** TF-05 Análisis de bancos de inversión y casas de análisis (principal)
- **Calidad Q:** 73 (B) — Primariedad 12/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 12/15 · Independencia 6/10 · Actualidad 10/10 · Acceso 10/10
- **Tipología:** secundaria cualificada (análisis de banco)
- **Acceso:** Abierto (EN/FR, RSS y suscripción)
- **Ámbitos:** Economías de la OCDE, emergentes y riesgo país, economía bancaria; Eco Flash, Eco Conjoncture, Eco Week, Eco Emerging, escenarios y previsiones
- **Motivo de inclusión y uso:** Estudios de un gran banco de la zona euro con equipo de riesgo país. Uso: escenario y previsiones de la eurozona y de emergentes.
- **Sesgos y cautelas:** Visión de un banco comercial.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «BNP Paribas Economic Research economic-research.bnpparibas.com EcoFlash»; WebFetch: sí)
- **Origen:** Alta 2026-11-02 (F9_S1, tanda 3).

#### RF-0229 · Q 72 (B) — BBVA Research

- **Canal oficial (URL raíz):** https://www.bbvaresearch.com/ (quiénes somos: https://www.bbvaresearch.com/en/about-us/)
- **Emisor:** BBVA (servicio de estudios fundado en 1932; economista jefe: Jorge Sicilia)
- **Temática:** TF-05 Análisis de bancos de inversión y casas de análisis (principal) · secundarias: TF-01
- **Calidad Q:** 72 (B) — Primariedad 12/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 12/15 · Independencia 6/10 · Actualidad 10/10 · Acceso 10/10
- **Tipología:** secundaria cualificada (análisis de banco)
- **Acceso:** Abierto (publicaciones descargables; no hay declaración expresa de licencia)
- **Ámbitos:** Macro, sistemas financieros, economía digital y geoestrategia; previsiones para más de 10 países (España, México, Turquía, Colombia, Argentina, Perú, China); indicadores de big data
- **Motivo de inclusión y uso:** Servicio de estudios con más de 100 analistas, previsiones publicadas e indicadores de alta frecuencia. Uso: segunda opinión sobre España y Latinoamérica, y previsiones para el Evaluador.
- **Sesgos y cautelas:** Visión de un banco comercial con intereses en los países que cubre.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «ING THINK economic research BBVA Research Allianz Research publications»; WebFetch: sí)
- **Origen:** Alta 2026-11-02 (F9_S1, tanda 2).

#### RF-0234 · Q 72 (B) — S&P Global Ratings — Research

- **Canal oficial (URL raíz):** https://www.spglobal.com/ratings/en/research/ (ejemplos: https://spglobal.com/ratings/en/research/articles/210726-sovereign-ratings-history-12029439 · https://www.spglobal.com/ratings/en/research/articles/200511-an-overview-of-sovereign-rating-actions-related-to-covid-19-11484790)
- **Emisor:** S&P Global Ratings
- **Temática:** TF-05 Análisis de bancos de inversión y casas de análisis (principal) · secundarias: TF-02
- **Calidad Q:** 72 (B) — Primariedad 16/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 14/15 · Independencia 5/10 · Actualidad 10/10 · Acceso 5/10
- **Tipología:** primaria (acciones de rating) y secundaria (análisis)
- **Acceso:** Comunicados de calificación y parte de la investigación con registro; el resto, de pago
- **Ámbitos:** Calificaciones de soberanos, empresas y finanzas estructuradas; historial de calificaciones soberanas
- **Motivo de inclusión y uso:** Una de las tres grandes agencias de calificación (junto con Moody's, RF-0231, y Fitch). Uso: acciones de rating como hechos con efecto en el mercado e historial soberano.
- **Sesgos y cautelas:** Conflicto «emisor-pagador»; errores documentados en 2008. La página leída cargó vacía.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «S&P Global Ratings research and Fitch Ratings research sovereign outlook»; WebFetch: sí, la página no mostró contenido)
- **Origen:** Alta 2026-11-02 (F9_S1, tanda 3).

#### RF-0045 · Q 71 (B) — J.P. Morgan Asset Management — Guide to the Markets

- **Canal oficial (URL raíz):** https://am.jpmorgan.com/ (Guide to the Markets: https://am.jpmorgan.com/lu/en/asset-management/nra/insights/market-insights/guide-to-the-markets/)
- **Emisor:** J.P. Morgan Asset Management
- **Temática:** TF-05 Análisis de bancos de inversión y casas de análisis (principal)
- **Calidad Q:** 71 (B) — Primariedad 14/20 · Historial 10/20 · Transparencia 11/15 · Autoridad 13/15 · Independencia 5/10 · Actualidad 9/10 · Acceso 9/10
- **Tipología:** secundaria (compendio de datos)
- **Acceso:** Abierto (PDF por región: EE. UU., Latinoamérica)
- **Ámbitos:** Gráficos de valoración, macro y mercados por clase de activo
- **Motivo de inclusión y uso:** Compendio trimestral de datos y gráficos; útil para contexto y consenso.
- **Sesgos y cautelas:** Gestora con productos; compilación de datos de terceros (citar la fuente primaria de cada gráfico).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «am.jpmorgan.com Guide to the Markets quarterly US»; WebFetch: sí)
- **Origen:** Semilla V3.0 (2026-11-01) confirmada en verificación de alta 2026-11-02 (tanda 2).

#### RF-0231 · Q 71 (B) — Moody's Ratings

- **Canal oficial (URL raíz):** ratings.moodys.io (según Wikipedia; comprobar en el barrido HT-02)
- **Emisor:** Moody's Ratings (Moody's Corporation; fundada en 1909 por John Moody)
- **Temática:** TF-05 Análisis de bancos de inversión y casas de análisis (principal) · secundarias: TF-02
- **Calidad Q:** 71 (B) — Primariedad 16/20 · Historial 10/20 · Transparencia 11/15 · Autoridad 14/15 · Independencia 5/10 · Actualidad 10/10 · Acceso 5/10
- **Tipología:** primaria (acciones de calificación) y secundaria (análisis)
- **Acceso:** Comunicados de calificación públicos; informes con registro o suscripción
- **Ámbitos:** Calificaciones crediticias de soberanos, empresas, bancos y finanzas estructuradas; perspectivas sectoriales
- **Motivo de inclusión y uso:** Una de las tres grandes agencias (junto con S&P y Fitch, alrededor del 95 % del mercado). Sus cambios de calificación son hechos con efecto en el mercado. Uso: calendario y contenido de las acciones de rating.
- **Sesgos y cautelas:** Conflicto «emisor-pagador»; fallos de calificación documentados en la crisis de 2008 (Financial Crisis Inquiry Report).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Big Three credit rating agencies wikipedia» → artículos de Wikipedia «Moody's Ratings» y «Big Three (credit rating agencies)»; WebFetch: sí, sobre Wikipedia)
- **Origen:** Alta 2026-11-02 (F9_S1, tanda 2).

#### RF-0237 · Q 70 (B) — Morningstar DBRS

- **Canal oficial (URL raíz):** https://dbrs.morningstar.com/ (ejemplo: https://dbrs.morningstar.com/research/327566/dbrs-releases-report-on-deutsche-bank-ag)
- **Emisor:** Morningstar DBRS (Morningstar Inc.)
- **Temática:** TF-05 Análisis de bancos de inversión y casas de análisis (principal) · secundarias: TF-02
- **Calidad Q:** 70 (B) — Primariedad 16/20 · Historial 10/20 · Transparencia 11/15 · Autoridad 12/15 · Independencia 5/10 · Actualidad 9/10 · Acceso 7/10
- **Tipología:** primaria (acciones de rating) y secundaria
- **Acceso:** Comunicados públicos; investigación de crédito con registro o suscripción
- **Ámbitos:** Calificaciones crediticias (agencia NRSRO y CRA registrada); bancos, soberanos, titulizaciones
- **Motivo de inclusión y uso:** Agencia de calificación alternativa a las tres grandes; útil cuando estas difieren. Uso: acciones de rating de soberanos y bancos europeos.
- **Sesgos y cautelas:** Conflicto «emisor-pagador»; mismo grupo que Morningstar (RF-0048).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Deutsche Bank Research dbresearch.com publications»; WebFetch: sí)
- **Origen:** Alta 2026-11-02 (F9_S1, tanda 3).

#### RF-0230 · Q 69 (B) — Allianz Research

- **Canal oficial (URL raíz):** https://www.allianz.com/en/economic_research/ (publicaciones: https://www.allianz.com/en/economic_research/publications/insights.html)
- **Emisor:** Allianz SE (servicio de estudios económicos)
- **Temática:** TF-05 Análisis de bancos de inversión y casas de análisis (principal) · secundarias: TF-14
- **Calidad Q:** 69 (B) — Primariedad 12/20 · Historial 10/20 · Transparencia 11/15 · Autoridad 12/15 · Independencia 6/10 · Actualidad 9/10 · Acceso 9/10
- **Tipología:** secundaria cualificada
- **Acceso:** Abierto (sin declaración expresa de licencia)
- **Ámbitos:** Riesgo país y sectorial, Global Wealth Report (2026), Global Insurance Map, investigación de clima y transición, gráficos y podcast
- **Motivo de inclusión y uso:** Estudios de un gran asegurador europeo, con datos propios de riesgo país y riqueza financiera de los hogares. Uso: riesgo país e insolvencias, y contexto de ahorro y riqueza.
- **Sesgos y cautelas:** Visión de un grupo asegurador con negocio de gestión de activos; el listado de publicaciones no se mostró completo al leerlo.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «ING THINK economic research BBVA Research Allianz Research publications»; WebFetch: sí)
- **Origen:** Alta 2026-11-02 (F9_S1, tanda 2).

#### RF-0239 · Q 69 (B) — Oxford Economics

- **Canal oficial (URL raíz):** https://www.oxfordeconomics.com/ (Global Macro Service: https://www.oxfordeconomics.com/subscriptions/global-macro-service/)
- **Emisor:** Oxford Economics (grupo que incluye Tourism Economics, Alpine Macro y FrontierView)
- **Temática:** TF-05 Análisis de bancos de inversión y casas de análisis (principal)
- **Calidad Q:** 69 (B) — Primariedad 12/20 · Historial 10/20 · Transparencia 11/15 · Autoridad 13/15 · Independencia 8/10 · Actualidad 9/10 · Acceso 6/10
- **Tipología:** secundaria cualificada (consultora de previsión)
- **Acceso:** Suscripción; notas de investigación y blogs públicos
- **Ámbitos:** Previsiones nacionales, sectoriales y urbanas de más de 200 economías; Global Economic Model y Global Industry Model
- **Motivo de inclusión y uso:** Modelo macro global usado por empresas y gobiernos. Uso: escenarios y previsiones de terceros independientes de la banca.
- **Sesgos y cautelas:** Acceso mayoritariamente de pago; consultora con encargos de clientes.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Oxford Economics global economic forecasts research»; WebFetch: sí)
- **Origen:** Alta 2026-11-02 (F9_S1, tanda 3).

#### RF-0046 · Q 66 (B) — Goldman Sachs Global Investment Research

- **Canal oficial (URL raíz):** https://www.goldmansachs.com/insights/goldman-sachs-research (Top of Mind e informes: https://www.goldmansachs.com/insights/reports)
- **Emisor:** Goldman Sachs
- **Temática:** TF-05 Análisis de bancos de inversión y casas de análisis (principal)
- **Calidad Q:** 66 (B) — Primariedad 14/20 · Historial 10/20 · Transparencia 11/15 · Autoridad 14/15 · Independencia 5/10 · Actualidad 9/10 · Acceso 3/10
- **Tipología:** secundaria cualificada
- **Acceso:** Restringido (clientes, Marquee); resúmenes públicos (Top of Mind, artículos, boletín semanal Briefings)
- **Ámbitos:** Previsiones macro, estrategia, sectores
- **Motivo de inclusión y uso:** Análisis de banco de inversión influyente; usar solo resúmenes públicos citables.
- **Sesgos y cautelas:** Conflictos de interés de banca de inversión; acceso restringido; el portal no señala qué contenidos son solo para clientes.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Goldman Sachs Global Investment Research insights Top of Mind»; WebFetch: sí)
- **Origen:** Semilla V3.0 (2026-11-01) confirmada en verificación de alta 2026-11-02 (tanda 2); URL raíz corregida.

#### RF-0048 · Q 66 (B) — Morningstar — investigación de fondos y valoraciones

- **Canal oficial (URL raíz):** https://global.morningstar.com/ (explicación del Medalist Rating: https://global.morningstar.com/en-gb/funds/whats-changing-not-changing-with-morningstar-medalist-rating · metodología, 31/12/2024: https://morningstar.com/content/cs-images/v3/assets/blt9415ea4cc4157833/blt1a4eaedeeda4b1c2/6781997a969dc5ffde9da0a0/1227010.pdf)
- **Emisor:** Morningstar Inc.
- **Temática:** TF-05 Análisis de bancos de inversión y casas de análisis (principal) · secundarias: TF-04, TF-06
- **Calidad Q:** 66 (B) — Primariedad 12/20 · Historial 10/20 · Transparencia 11/15 · Autoridad 12/15 · Independencia 6/10 · Actualidad 9/10 · Acceso 6/10
- **Tipología:** secundaria cualificada
- **Acceso:** Muro parcial (metodologías abiertas)
- **Ámbitos:** Fondos, ETF, flujos, valoraciones de analistas; Medalist Rating (pilares Personas, Proceso y Matriz, más precio; unos 130 analistas, más de 3.200 estrategias)
- **Motivo de inclusión y uso:** Datos y análisis de fondos y flujos con metodología pública. Uso: calidad de gestoras y fondos, y señales de coste.
- **Sesgos y cautelas:** Calificaciones con conflictos potenciales (patrocinio); metodología revisada (sin curva forzada, comparación con la media de la categoría), con más medallas Gold y Silver tras el cambio.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Morningstar Medalist Rating methodology fund research»; WebFetch: sí)
- **Origen:** Semilla V3.0 (2026-11-01) confirmada en verificación de alta 2026-11-02 (tanda 2); URL raíz corregida.

<!-- ===== Tanda 3 (2026-11-02): 25 búsquedas WebSearch. Las fichas se fusionan en su temática y por Q descendente. ===== -->

#### RF-0240 · Q 66 (B) — Morgan Stanley — Ideas y pódcast «Thoughts on the Market»

- **Canal oficial (URL raíz):** https://www.morganstanley.com/ideas (pódcasts: https://www.morganstanley.com/ideas/morgan-stanley-podcast-homepage)
- **Emisor:** Morgan Stanley
- **Temática:** TF-05 Análisis de bancos de inversión y casas de análisis (principal)
- **Calidad Q:** 66 (B) — Primariedad 12/20 · Historial 10/20 · Transparencia 10/15 · Autoridad 14/15 · Independencia 5/10 · Actualidad 10/10 · Acceso 5/10
- **Tipología:** secundaria cualificada
- **Acceso:** Pódcast diario abierto; investigación completa restringida a clientes
- **Ámbitos:** Estrategia de mercados, macro, sectores (pódcast diario con analistas del banco)
- **Motivo de inclusión y uso:** Resumen público diario de la visión de estrategas y analistas de un gran banco de inversión. Uso: consenso de la banca de inversión.
- **Sesgos y cautelas:** Conflictos de interés de banca de inversión; contenido público resumido.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Morgan Stanley Research ideas Thoughts on the Market»; WebFetch: sí)
- **Origen:** Alta 2026-11-02 (F9_S1, tanda 3).

#### RF-0243 · Q 65 (B) — Citi GPS (Global Perspectives & Solutions)

- **Canal oficial (URL raíz):** https://www.citigroup.com/global/insights/tags/citi-global-perspectives-solutions
- **Emisor:** Citigroup
- **Temática:** TF-05 Análisis de bancos de inversión y casas de análisis (principal) · secundarias: TF-14
- **Calidad Q:** 65 (B) — Primariedad 11/20 · Historial 10/20 · Transparencia 10/15 · Autoridad 13/15 · Independencia 5/10 · Actualidad 8/10 · Acceso 8/10
- **Tipología:** secundaria cualificada (informes temáticos)
- **Acceso:** Abierto (suscripción por correo)
- **Ámbitos:** Tendencias globales: mercados y economía, tecnología, sostenibilidad, estrategia empresarial; colaboración con la Oxford Martin School
- **Motivo de inclusión y uso:** Informes temáticos de largo plazo de un banco global. Uso: detección de megatendencias para el Analizador.
- **Sesgos y cautelas:** Visión de un banco con intereses comerciales; la página de etiqueta no listó informes concretos.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Citi GPS Global Perspectives and Solutions reports»; WebFetch: sí)
- **Origen:** Alta 2026-11-02 (F9_S1, tanda 3).

#### RF-0236 · Q 62 (C) — Deutsche Bank Research (portal profesional)

- **Canal oficial (URL raíz):** https://research.db.com/ (ejemplo: https://research.db.com/Research/Disclosures/FICCDisclosures)
- **Emisor:** Deutsche Bank AG (Fráncfort)
- **Temática:** TF-05 Análisis de bancos de inversión y casas de análisis (principal)
- **Calidad Q:** 62 (C) — Primariedad 12/20 · Historial 10/20 · Transparencia 11/15 · Autoridad 13/15 · Independencia 5/10 · Actualidad 8/10 · Acceso 3/10
- **Tipología:** secundaria cualificada (análisis de banco de inversión)
- **Acceso:** Restringido (clientes); divulgaciones regulatorias públicas
- **Ámbitos:** Renta fija, divisas, materias primas, crédito, estrategia; históricos de recomendaciones (divulgaciones de octubre de 2026)
- **Motivo de inclusión y uso:** Análisis de un gran banco europeo; las divulgaciones públicas permiten auditar recomendaciones históricas. Uso: solo extractos públicos citables.
- **Sesgos y cautelas:** Conflictos de interés de banca de inversión; casi todo el contenido es de acceso restringido.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Deutsche Bank Research dbresearch.com publications»; WebFetch: sí)
- **Origen:** Alta 2026-11-02 (F9_S1, tanda 3).

#### RF-0244 · Q 58 (C) — Trading Economics

- **Canal oficial (URL raíz):** https://tradingeconomics.com/ (ejemplo: https://tradingeconomics.com/sdr:ln)
- **Emisor:** Trading Economics (titularidad no declarada en la página leída)
- **Temática:** TF-05 Análisis de bancos de inversión y casas de análisis (principal) · secundarias: TF-06
- **Calidad Q:** 58 (C) — Primariedad 8/20 · Historial 10/20 · Transparencia 6/15 · Autoridad 9/15 · Independencia 8/10 · Actualidad 10/10 · Acceso 7/10
- **Tipología:** agregador con previsiones de modelo propio
- **Acceso:** Consulta abierta; API y descargas masivas de pago
- **Ámbitos:** Indicadores económicos por país, calendario, cotizaciones, consenso de beneficios y previsiones propias («global macro models projections and analysts expectations»)
- **Motivo de inclusión y uso:** Previsiones explícitas y masivas por indicador, contrastables por el Evaluador. Uso: punto de comparación de previsiones; los datos se citan en su fuente oficial.
- **Sesgos y cautelas:** Metodología de previsión apenas descrita; posible solape con TF-06 (decidir al fusionar).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Schroders insights economic and strategy viewpoint Man Group Man Institute»; WebFetch: sí)
- **Origen:** Alta 2026-11-02 (F9_S1, tanda 3).

## TF-06 Datos de mercado, posicionamiento y flujos

#### RF-0343 · Q 88 (A) — OFR — Short-term Funding Monitor (incluye estadísticas de primary dealers de la Fed de Nueva York)

- **Canal oficial (URL raíz):** https://www.financialresearch.gov/short-term-funding-monitor/datasets/nypd/
- **Emisor:** Office of Financial Research (Tesoro de EE. UU.); datos de primary dealers publicados por la Federal Reserve Bank of New York
- **Documentación y notas:** Monitor con resúmenes de colateral, plazos, volúmenes y tipos; conjuntos de fondos monetarios, repo, tipos de referencia, primary dealers (posiciones, operaciones, financiación y fallos; semanal, jueves) y curva constante del Tesoro; API y documentación; actualización diaria.
- **Temática:** TF-06 Datos de mercado, posicionamiento y flujos (principal) · secundarias: TF-01
- **Calidad Q:** 88 (A) — Primariedad 18/20 · Historial 10/20 · Transparencia 15/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 10/10 · Acceso 10/10
- **Tipología:** primaria
- **Acceso:** Abierto (API)
- **Ámbitos:** Financiación a corto plazo, repo, posiciones de primary dealers
- **Motivo de inclusión y uso:** Seguimiento de tensiones de liquidez y del posicionamiento de los intermediarios en bonos.
- **Restricciones de uso:** Uso libre con atribución; citar serie y fecha.
- **Sesgos y cautelas:** Subconjunto de las series de la Fed de Nueva York.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «New York Fed primary dealer statistics weekly positions»; WebFetch: sí)

#### RF-0342 · Q 86 (A) — FINRA — estadísticas de margen

- **Canal oficial (URL raíz):** https://www.finra.org/investors/margin-statistics
- **Emisor:** Financial Industry Regulatory Authority (FINRA)
- **Documentación y notas:** Saldos deudores en cuentas de margen y saldos acreedores libres (regla 4521(d)), a fin de mes, publicados hacia la tercera semana del mes siguiente; histórico desde enero de 1997 en Excel (serie homogénea desde febrero de 2010). Septiembre de 2026: 1,48 billones de dólares de saldos deudores.
- **Temática:** TF-06 Datos de mercado, posicionamiento y flujos (principal) · secundarias: —
- **Calidad Q:** 86 (A) — Primariedad 19/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 8/10 · Acceso 10/10
- **Tipología:** primaria
- **Acceso:** Abierto (web y Excel; sin feed)
- **Ámbitos:** Apalancamiento de inversores minoristas y de intermediarios en EE. UU.
- **Motivo de inclusión y uso:** Indicador de apalancamiento y euforia (deuda de margen) para el régimen de riesgo.
- **Restricciones de uso:** Uso con atribución; citar mes.
- **Sesgos y cautelas:** Cambios de método de cálculo de algunas firmas desde 2021; ruptura de serie en 2010.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Integración NYSE/NASD (2010).
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «FINRA margin statistics customer margin balances»; WebFetch: sí)

#### RF-0344 · Q 86 (A) — Tesoro de EE. UU. — Treasury International Capital (TIC)

- **Canal oficial (URL raíz):** https://home.treasury.gov/archives-of-tic-monthly-data-releases
- **Emisor:** U.S. Department of the Treasury
- **Documentación y notas:** Notas mensuales de flujos de capital transfronterizos (p. ej., nota de 16/09/2026 sobre julio de 2026: entrada neta de 83.700 M$, 73.500 M$ privados y 10.200 M$ oficiales; siguiente 16/10/2026); archivo histórico de publicaciones.
- **Temática:** TF-06 Datos de mercado, posicionamiento y flujos (principal) · secundarias: TF-01
- **Calidad Q:** 86 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 7/10 · Acceso 10/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** Compras extranjeras de valores de EE. UU.; tenencias de Treasuries por país
- **Motivo de inclusión y uso:** Flujos de capital extranjero hacia activos estadounidenses (demanda de Treasuries).
- **Restricciones de uso:** Uso libre; citar mes de referencia.
- **Sesgos y cautelas:** Desfase de unos dos meses y medio; atribución por país de custodia.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Treasury International Capital TIC system monthly data»; WebFetch: sí, nota de septiembre de 2026)

#### RF-0049 · Q 85 (A) — CFTC — Commitments of Traders (COT)

- **Canal oficial (URL raíz):** https://www.cftc.gov/MarketReports/CommitmentsofTraders/index.htm
- **Emisor:** U.S. Commodity Futures Trading Commission (CFTC)
- **Documentación y notas:** La página oficial describe los cuatro informes (Legacy, Supplemental, Disaggregated, Traders in Financial Futures) y remite al calendario de publicación y al Public Reporting Environment (históricos consultables). Catálogo federal: catalog.data.gov/dataset/commitment-of-traders-cot
- **Temática:** TF-06 Datos de mercado, posicionamiento y flujos (principal) · secundarias: TF-08
- **Calidad Q:** 85 (A) — Primariedad 18/20 · Historial 10/20 · Transparencia 15/15 · Autoridad 14/15 · Independencia 10/10 · Actualidad 8/10 · Acceso 10/10
- **Tipología:** primaria
- **Acceso:** Abierto (dominio público, datos federales de EE. UU.)
- **Ámbitos:** Posicionamiento semanal en futuros y opciones sobre futuros (mercados con ≥ 20 operadores declarables): comerciales/no comerciales; productores, swap dealers, managed money; dealers, gestores de activos y fondos apalancados en futuros financieros (divisas, Treasuries, índices bursátiles, VIX)
- **Motivo de inclusión y uso:** Dato primario de posicionamiento especulativo y de cobertura para divisas, materias primas, bonos e índices; insumo de señales de sentimiento extremo y de crowding.
- **Restricciones de uso:** Uso libre; citar informe (Legacy/Disaggregated/TFF), contrato y fecha del martes de referencia.
- **Sesgos y cautelas:** Datos del martes publicados el viernes a las 15:30 ET (desfase de 3 días; festivos alteran el calendario). Categorías amplias; los datos publicados no se revisan. Históricos: Legacy desde 15/01/1986; Disaggregated y TFF desde 13/06/2006.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos; vigilar avisos de calendario de la CFTC.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «CFTC Commitments of Traders reports official»; WebFetch: sí)

#### RF-0051 · Q 85 (A) — Kenneth R. French — Data Library

- **Canal oficial (URL raíz):** https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html
- **Emisor:** Kenneth R. French (Tuck School of Business, Dartmouth College)
- **Documentación y notas:** Cada serie enlaza su página de descripción; existen páginas de archivo de versiones anteriores (p. ej., data_library_202412_archive.html). Desde la entrega de enero de 2025 las series de EE. UU. se generan con los ficheros CRSP Flat File Format 2.0 (CIZ).
- **Temática:** TF-06 Datos de mercado, posicionamiento y flujos (principal) · secundarias: TF-13
- **Calidad Q:** 85 (A) — Primariedad 18/20 · Historial 10/20 · Transparencia 15/15 · Autoridad 14/15 · Independencia 10/10 · Actualidad 8/10 · Acceso 10/10
- **Tipología:** primaria
- **Acceso:** Abierto (TXT y CSV)
- **Ámbitos:** Factores Fama/French de 3 y 5 factores (mensual, semanal, diario), momentum y reversión; carteras por tamaño, B/M, rentabilidad, inversión, E/P, CF/P, D/P, beta, emisiones netas, varianza; carteras sectoriales (5 a 49 industrias); breakpoints; factores de mercados desarrollados y regionales
- **Motivo de inclusión y uso:** Fuente estándar de rentabilidades de factores y carteras para atribución de rentabilidad, contraste de anomalías y primas de estilo.
- **Restricciones de uso:** Uso libre con atribución; citar la serie y el mes de la entrega (la tabla de la página cubría septiembre de 2026 en la consulta).
- **Sesgos y cautelas:** Revisiones retroactivas de las series en cada entrega (cambio CRSP CIZ en 2025): guardar la versión descargada para reproducibilidad.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Cambio de fuente de datos CRSP a formato CIZ (enero de 2025).
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «"data_library" ken.french Current Research Returns Fama/French factors»; WebFetch: sí)

#### RF-0053 · Q 82 (A) — Investment Company Institute (ICI) — flujos de fondos

- **Canal oficial (URL raíz):** https://www.ici.org/research/stats/flows
- **Emisor:** Investment Company Institute
- **Documentación y notas:** Publicación semanal (miércoles) de los flujos estimados de fondos de inversión a largo plazo; la estimación de flujos combinados ETF + fondos se publica aparte; históricos descargables en ici.org. Última publicación vista: 28/10/2026 (semana cerrada el 21/10/2026).
- **Temática:** TF-06 Datos de mercado, posicionamiento y flujos (principal)
- **Calidad Q:** 82 (A) — Primariedad 18/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 14/15 · Independencia 9/10 · Actualidad 8/10 · Acceso 9/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** Flujos netos semanales de fondos de inversión de EE. UU.: renta variable (doméstica y mundial), mixtos, renta fija (gravable y municipal)
- **Motivo de inclusión y uso:** Dato primario de flujos de inversores en fondos de EE. UU. (cobertura ≈ 98 % de los activos del sector) para medir apetito por riesgo y rotaciones entre clases de activo.
- **Restricciones de uso:** Uso con atribución; citar la semana de referencia y si la cifra excluye ETF.
- **Sesgos y cautelas:** Asociación sectorial; estimaciones semanales que se revisan; excluye ETF y fondos de fondos en la serie principal.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Investment Company Institute weekly estimated long-term mutual fund flows»; WebFetch: sí)

#### RF-0302 · Q 82 (A) — Cboe Global Markets — estadísticas de opciones (put/call) y VIX

- **Canal oficial (URL raíz):** http://www.cboe.com/
- **Emisor:** Cboe Global Markets
- **Documentación y notas:** Fuente original de los ratios put/call (OEX, acciones, total Cboe) publicados a diario tras el cierre, según el catálogo de indicadores de sentimiento DecisionPoint de StockCharts (chartschool.stockcharts.com), que cita cboe.com como fuente. Cboe calcula además el VIX.
- **Temática:** TF-06 Datos de mercado, posicionamiento y flujos (principal)
- **Calidad Q:** 82 (A) — Primariedad 19/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 14/15 · Independencia 7/10 · Actualidad 10/10 · Acceso 8/10
- **Tipología:** primaria
- **Acceso:** Abierto (estadísticas diarias); datos históricos detallados con licencia
- **Ámbitos:** Volúmenes y ratios put/call; índices de volatilidad (VIX)
- **Motivo de inclusión y uso:** Dato primario de posicionamiento en opciones y de aversión al riesgo, para señales de sentimiento contrarias.
- **Restricciones de uso:** Condiciones de Cboe; citar el ratio exacto (equity, index, total) y la fecha.
- **Sesgos y cautelas:** Bolsa con interés comercial en sus productos; los ratios dependen del universo de opciones elegido.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «AAII Investor Sentiment Survey NAAIM Exposure Index Cboe put/call ratio FINRA margin statistics»; URL tomada del catálogo DecisionPoint de StockCharts, leído con WebFetch; WebFetch al sitio: no)

#### RF-0050 · Q 81 (A) — Damodaran Online

- **Canal oficial (URL raíz):** https://pages.stern.nyu.edu/~adamodar/New_Home_Page/home.htm
- **Emisor:** Aswath Damodaran (NYU Stern School of Business)
- **Documentación y notas:** Sección de datos con rentabilidades históricas (acciones, bonos, inmobiliario, oro), ERP implícita mensual (desde 09/2008) y anual (desde 1960), primas de riesgo país (CRP); archivo de años anteriores. Última actualización general vista: 09/01/2026; CRP: 01/07/2026; próxima: enero de 2027.
- **Temática:** TF-06 Datos de mercado, posicionamiento y flujos (principal) · secundarias: TF-05
- **Calidad Q:** 81 (A) — Primariedad 16/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 14/15 · Independencia 9/10 · Actualidad 8/10 · Acceso 10/10
- **Tipología:** secundaria
- **Acceso:** Abierto
- **Ámbitos:** Prima de riesgo implícita, múltiplos y costes de capital por sector y país, primas de riesgo país
- **Motivo de inclusión y uso:** Conjuntos de datos de valoración con metodología explicada; referencia para ERP y coste de capital en AC de valoración.
- **Restricciones de uso:** Uso libre con atribución; citar fichero y fecha de actualización.
- **Sesgos y cautelas:** Un solo autor y supuestos propios; actualización general anual (datos sectoriales desfasados a lo largo del año).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Damodaran Online data current NYU Stern»; WebFetch: sí)

#### RF-0056 · Q 81 (A) — S&P Dow Jones Indices (metodologías, SPIVA)

- **Canal oficial (URL raíz):** https://www.spglobal.com/spdji/en/research-insights/spiva/
- **Emisor:** S&P Dow Jones Indices (S&P Global)
- **Documentación y notas:** Sección SPIVA con resultados por región, biblioteca (spglobal.com/spdji/en/research-insights/spiva/spiva-library/), vídeos e investigación; blog Indexology del mismo emisor (indexologyblog.com, no cuenta como fuente independiente). Metodologías de índices en las fichas de cada índice de spglobal.com/spdji/en/.
- **Temática:** TF-06 Datos de mercado, posicionamiento y flujos (principal) · secundarias: TF-05
- **Calidad Q:** 81 (A) — Primariedad 18/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 14/15 · Independencia 8/10 · Actualidad 8/10 · Acceso 9/10
- **Tipología:** primaria
- **Acceso:** Abierto (parcial)
- **Ámbitos:** Metodologías de índices; informes SPIVA (gestión activa frente a índices, persistencia de gestores) por región
- **Motivo de inclusión y uso:** Reglas de índices y evidencia periódica de rendimiento relativo de la gestión activa.
- **Restricciones de uso:** Condiciones de S&P DJI; citar informe SPIVA (región, periodo) y fecha.
- **Sesgos y cautelas:** Proveedor comercial de índices (interés en la gestión indexada).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «S&P Dow Jones Indices SPIVA scorecard» y «SPIVA S&P Dow Jones Indices spglobal.com/spdji/en/research-insights/spiva»; WebFetch: sí)

#### RF-0346 · Q 81 (A) — CME Group — FedWatch Tool

- **Canal oficial (URL raíz):** https://www.cmegroup.com/markets/interest-rates/cme-fedwatch-tool.html
- **Emisor:** CME Group
- **Documentación y notas:** Probabilidades de decisiones del FOMC implícitas en futuros de fondos federales a 30 días; metodología publicada (cmegroup.com/articles/2023/understanding-the-cme-group-fedwatch-tool-methodology.html): árbol de probabilidades por reunión, movimientos de 25 pb, tipo efectivo no negativo.
- **Temática:** TF-06 Datos de mercado, posicionamiento y flujos (principal) · secundarias: TF-01
- **Calidad Q:** 81 (A) — Primariedad 17/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 14/15 · Independencia 7/10 · Actualidad 10/10 · Acceso 9/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** Expectativas de mercado sobre el tipo de los fondos federales
- **Motivo de inclusión y uso:** Expectativas de política monetaria descontadas por el mercado (catalizador H1).
- **Restricciones de uso:** Condiciones de CME; citar fecha y hora.
- **Sesgos y cautelas:** Probabilidades de mercado (no previsión de la Fed); supuestos simplificadores.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «CME FedWatch Tool fed funds target rate probabilities»; WebFetch: sí, página de metodología)

#### RF-0052 · Q 80 (A) — Robert J. Shiller — datos online (CAPE, series largas)

- **Canal oficial (URL raíz):** https://www.irrationalexuberance.com/index.htm
- **Emisor:** Robert J. Shiller (Yale University)
- **Documentación y notas:** La web oficial del libro *Irrational Exuberance* enlaza el fichero Excel actualizado con precios, beneficios, dividendos y tipos de interés desde 1871 (base del CAPE). El dominio de datos citado en la semilla (shillerdata.com) **no** apareció en los resultados de búsqueda: no se registra; la URL exacta del fichero no se ha confirmado (los destinos de enlace no eran visibles en la lectura). Agregadores derivados (p. ej., multpl.com) no cuentan como fuente independiente.
- **Temática:** TF-06 Datos de mercado, posicionamiento y flujos (principal) · secundarias: TF-13
- **Calidad Q:** 80 (A) — Primariedad 17/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 14/15 · Independencia 10/10 · Actualidad 7/10 · Acceso 8/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** CAPE, dividendos, beneficios, precios del S&P y tipos desde 1871
- **Motivo de inclusión y uso:** Serie larga de valoración de la renta variable estadounidense.
- **Restricciones de uso:** Uso libre con atribución; citar versión/fecha del fichero.
- **Sesgos y cautelas:** Mantenimiento por un único autor; frecuencia de actualización irregular; Acceso rebajado a 8 hasta confirmar la URL directa de descarga.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Migración del alojamiento de datos desde econ.yale.edu (dominio vigente del fichero pendiente de confirmar en el próximo barrido HT-02).
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Robert Shiller "Online Data" stock market data used in Irrational Exuberance updated» y «"shillerdata.com"»; WebFetch: sí)
- **Alerta:** REPARAR en el próximo barrido: confirmar la URL directa del fichero de datos.

#### RF-0054 · Q 80 (A) — MSCI — metodologías de índices

- **Canal oficial (URL raíz):** https://www.msci.com/indexes/index-resources/index-methodology
- **Emisor:** MSCI Inc.
- **Documentación y notas:** Buscador de metodologías vigentes e históricas por nombre o código de índice; documentos clave enlazados (MSCI Index Calculation Methodology, MSCI Index Policies —p. ej., versión 27/01/2026 en msci.com/indexes/documents/methodology/—, Fixed Income Index Policies). Las URL antiguas (msci.com/index-methodology, msci.com/eqb/methodology/) siguen apareciendo en buscadores.
- **Temática:** TF-06 Datos de mercado, posicionamiento y flujos (principal)
- **Calidad Q:** 80 (A) — Primariedad 18/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 14/15 · Independencia 7/10 · Actualidad 9/10 · Acceso 8/10
- **Tipología:** primaria
- **Acceso:** Abierto (metodologías); datos de índices de pago
- **Ámbitos:** Reglas de índices (GIMI), reequilibrios, clasificación de mercados
- **Motivo de inclusión y uso:** Reglas oficiales que generan flujos indexados (reclasificaciones, reequilibrios trimestrales).
- **Restricciones de uso:** Condiciones de MSCI; citar documento y fecha de versión.
- **Sesgos y cautelas:** Proveedor comercial; la página no aclara si algún documento exige acceso de cliente.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Reorganización de URL del sitio (rutas /eqb/ antiguas): vigilar redirecciones.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «MSCI index methodology page»; WebFetch: sí)

#### RF-0055 · Q 80 (A) — FTSE Russell — metodologías de índices

- **Canal oficial (URL raíz):** https://lseg.com/en/ftse-russell
- **Emisor:** FTSE Russell (London Stock Exchange Group, LSEG)
- **Documentación y notas:** Las reglas (ground rules) y metodologías se publican como PDF bajo lseg.com/content/dam/ftse-russell/en_us/documents/ (p. ej., «Global Equity Index Methodology», «Russell US Equity Indexes – history of ground rule updates», «Russell Indexes – impacts of reconstitution 2025»). La portada remite al «Benchmark and Index Finder».
- **Temática:** TF-06 Datos de mercado, posicionamiento y flujos (principal)
- **Calidad Q:** 80 (A) — Primariedad 18/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 14/15 · Independencia 7/10 · Actualidad 9/10 · Acceso 8/10
- **Tipología:** primaria
- **Acceso:** Abierto (reglas y metodologías); datos de pago
- **Ámbitos:** Reglas de índices FTSE y Russell, reconstitución de los índices Russell de EE. UU., clasificación de países
- **Motivo de inclusión y uso:** Calendario y efectos de reconstituciones como catalizador de flujos indexados.
- **Restricciones de uso:** Condiciones de LSEG; citar documento y versión.
- **Sesgos y cautelas:** Proveedor comercial; la portada no enlaza directamente las reglas (se llega por el buscador de índices). Comprobar el calendario de reconstitución en el documento vigente antes de usarlo.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Integrado en LSEG; el dominio russell.com redirige parcialmente al de LSEG.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «FTSE Russell index ground rules methodology LSEG Russell reconstitution» y «FTSE Russell LSEG index provider home page»; WebFetch: sí)

<!-- Tanda 2 · 2026-11-02 · cupo de 25 búsquedas · verificación de semillas TF-07…TF-10 y altas RF-0300…RF-0316. Convención: «VERIFICADO_BUSQUEDA (directorio)» = URL raíz tomada de un directorio oficial o de referencia leído con WebFetch (indicado en «Última verificación»); el sitio en sí no se pudo leer porque la herramienta solo admite URL devueltas por búsqueda. -->

#### RF-0463 · Q 80 (A) — OCC (Options Clearing Corporation) — estadísticas de volumen y préstamo de valores

- **Emisor/organización:** The Options Clearing Corporation (OCC)
- **Año:** Publicación mensual
- **Publicación o institución:** Cámara de compensación de derivados sobre acciones (supervisada por SEC, CFTC y Reserva Federal)
- **Tipo de documento:** Estadísticas oficiales mensuales de volumen de opciones, futuros y préstamo de valores
- **Temática:** TF-06 Datos de mercado, posicionamiento y flujos (principal) · secundarias: —
- **Calidad Q:** 80 (A) — Primariedad 20/20 · Exactitud histórica 10/20 · Transparencia 12/15 · Autoridad 14/15 · Independencia 9/10 · Actualidad 9/10 · Accesibilidad 6/10
- **Canal oficial (URL raíz):** https://www.theocc.com · ejemplo leído: https://www.theocc.com/newsroom/press-releases/2024/1-03-occ-reports-december-2023-and-total-2023-volume-data
- **Acceso y licencia:** Notas de prensa mensuales gratuitas; datos detallados en la web de la OCC
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «OCC Options Clearing Corporation market data volume and open interest statistics»; WebFetch: sí)
- **Contenido:** Volumen mensual y anual de opciones sobre acciones, índices y ETF, futuros y préstamo de valores en EE. UU.; indicador de actividad especulativa y de cobertura.
- **Uso en el bloque:** AC-RV y AC-CRI: posicionamiento y sentimiento (actividad en opciones); Motor: series de volumen para indicadores de euforia o cobertura.
- **Limitaciones:** Cubre solo mercado estadounidense; el volumen no distingue compra de venta ni intención. Sustituye a RF-0317 (duplicado de Trading Economics).

#### RF-0345 · Q 79 (B) — EFAMA — estadísticas de fondos europeos

- **Canal oficial (URL raíz):** https://efama.org/node/501
- **Emisor:** European Fund and Asset Management Association (EFAMA)
- **Documentación y notas:** Estadísticas mensuales y trimestrales de UCITS y AIF (patrimonio y ventas netas), estadística internacional trimestral con ICI para IIFA y Fact Book. 2T 2026: 27,51 billones de euros de patrimonio y 267.000 M€ de entradas netas, con récord de ventas de ETF UCITS (117.000 M€).
- **Temática:** TF-06 Datos de mercado, posicionamiento y flujos (principal) · secundarias: —
- **Calidad Q:** 79 (B) — Primariedad 18/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 14/15 · Independencia 7/10 · Actualidad 8/10 · Acceso 9/10
- **Tipología:** primaria
- **Acceso:** Abierto (resúmenes); más datos para miembros
- **Ámbitos:** Flujos y patrimonio de fondos europeos por categoría
- **Motivo de inclusión y uso:** Contraparte europea de RF-0053 (ICI) para medir flujos de inversores.
- **Restricciones de uso:** Citar trimestre o mes.
- **Sesgos y cautelas:** Asociación sectorial; datos agregados de asociaciones nacionales.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «EFAMA fund market statistics quarterly UCITS AIF net sales»; WebFetch: sí)

#### RF-0300 · Q 74 (B) — AAII — Investor Sentiment Survey

- **Canal oficial (URL raíz):** https://www.aaii.com/sentimentsurvey
- **Emisor:** American Association of Individual Investors (AAII)
- **Documentación y notas:** Encuesta semanal a miembros (votación de jueves a miércoles; publicación los jueves) desde julio de 1987. Promedios históricos publicados: alcistas 37,5 %, neutrales 31,0 %, bajistas 31,5 %. Lectura vista: semana al 28/10/2026 (37,8 / 20,7 / 41,4).
- **Temática:** TF-06 Datos de mercado, posicionamiento y flujos (principal) · secundarias: TF-12
- **Calidad Q:** 74 (B) — Primariedad 16/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 12/15 · Independencia 8/10 · Actualidad 10/10 · Acceso 6/10
- **Tipología:** primaria
- **Acceso:** Lectura semanal gratuita; histórico completo solo para miembros (de pago)
- **Ámbitos:** Sentimiento del inversor minorista estadounidense (alcista/neutral/bajista)
- **Motivo de inclusión y uso:** Indicador contrario clásico de sentimiento minorista con serie larga.
- **Restricciones de uso:** Condiciones de AAII; citar semana y porcentajes.
- **Sesgos y cautelas:** Muestra autoseleccionada de miembros; ruido semanal elevado.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Encuesta postal hasta 2000, en línea desde entonces.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «AAII Investor Sentiment Survey NAAIM Exposure Index Cboe put/call ratio FINRA margin statistics»; WebFetch: sí)

#### RF-0301 · Q 70 (B) — NAAIM — Exposure Index

- **Canal oficial (URL raíz):** https://www.naaim.org/
- **Emisor:** National Association of Active Investment Managers (NAAIM)
- **Documentación y notas:** Exposición media a la renta variable de EE. UU. declarada por gestores activos miembros, actualizada semanalmente (según el catálogo DecisionPoint de StockCharts, que cita naaim.org como fuente).
- **Temática:** TF-06 Datos de mercado, posicionamiento y flujos (principal)
- **Calidad Q:** 70 (B) — Primariedad 15/20 · Historial 10/20 · Transparencia 10/15 · Autoridad 10/15 · Independencia 7/10 · Actualidad 10/10 · Acceso 8/10
- **Tipología:** primaria
- **Acceso:** Abierto (lectura semanal)
- **Ámbitos:** Posicionamiento de gestores activos en renta variable estadounidense
- **Motivo de inclusión y uso:** Complemento profesional al sentimiento minorista (RF-0300) para medir crowding.
- **Restricciones de uso:** Citar semana y valor.
- **Sesgos y cautelas:** Muestra pequeña y autodeclarada; asociación sectorial.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «AAII Investor Sentiment Survey NAAIM Exposure Index Cboe put/call ratio FINRA margin statistics»; URL tomada del catálogo DecisionPoint de StockCharts, leído con WebFetch; WebFetch al sitio: no)

#### RF-0347 · Q 68 (B) — Crane Data — datos de fondos del mercado monetario

- **Canal oficial (URL raíz):** https://www.cranedata.com/archives/all-articles/4480/
- **Emisor:** Crane Data LLC
- **Documentación y notas:** Editor de noticias y datos de fondos monetarios: Money Fund Intelligence (mensual, con versión XLS), Money Fund Wisdom, conferencias; noticias diarias (p. ej., patrimonio mundial de fondos monetarios de 13,7 billones de dólares según MFI).
- **Temática:** TF-06 Datos de mercado, posicionamiento y flujos (principal) · secundarias: —
- **Calidad Q:** 68 (B) — Primariedad 14/20 · Historial 10/20 · Transparencia 10/15 · Autoridad 11/15 · Independencia 8/10 · Actualidad 9/10 · Acceso 6/10
- **Tipología:** secundaria
- **Acceso:** Noticias abiertas; datos de pago
- **Ámbitos:** Patrimonio, rentabilidades y flujos de fondos monetarios
- **Motivo de inclusión y uso:** Seguimiento del «efectivo al margen» como munición potencial para activos de riesgo.
- **Restricciones de uso:** Citar publicación y fecha; datos completos solo por suscripción.
- **Sesgos y cautelas:** Proveedor comercial; artículo leído de 2013.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin datos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «New York Fed primary dealer statistics weekly positions»; WebFetch: sí)

#### RF-0013 · Q 51 (C) — Yahoo Finance

- **Canal oficial:** finance.yahoo.com
- **Documentación y notas:** Pista de descubrimiento (nivel C): todo dato extraído aquí debe verificarse contra una fuente de nivel A antes de citarse (ficha)
- **Temática:** TF-06 Datos de mercado, posicionamiento y flujos (principal) · secundarias: TF-03
- **Calidad Q:** 51 (C) — Primariedad 5/20 · Historial 10/20 · Transparencia 4/15 · Autoridad 7/15 · Independencia 6/10 · Actualidad 10/10 · Acceso 9/10
- **Nivel de fiabilidad en V2.4:** C
- **Tipología:** terciaria (agregador)
- **Motivo de inclusión:** Agregador comercial gratuito de cotizaciones, gráficos y titulares: útil como pista de descubrimiento y para corroborar fechas de mercado
- **Ámbitos:** Cotizaciones; titulares de mercado; calendario económico básico
- **Restricciones de uso:** Condiciones del servicio; no citar como fuente primaria de un hecho
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Sesgos posibles:** Agregación sin control editorial de los datos de cotización; titulares sindicados de terceros (anotar siempre `syndicated_of` cuando se identifique)
- **Cambios de propiedad o de metodología:** Propiedad de Yahoo/Verizon Media; vigilar cambios de URL de piezas
- **Estado:** Aprobada
- **Estado del enlace:** PENDIENTE_BARRIDO
- **Última verificación:** 2026-10-25 (Completa (URL viva y naturaleza del contenido comprobadas el 25/10/2026))
- **Alerta:** Pista de descubrimiento: todo dato debe verificarse contra una fuente de nivel A antes de citarse.

#### RF-0014 · Q 50 (C) — Investing.com

- **Canal oficial:** investing.com
- **Documentación y notas:** Pista de descubrimiento (nivel C): mismo matiz de verificación previa que RF-0013 (ficha)
- **Temática:** TF-06 Datos de mercado, posicionamiento y flujos (principal) · secundarias: TF-03
- **Calidad Q:** 50 (C) — Primariedad 5/20 · Historial 10/20 · Transparencia 4/15 · Autoridad 6/15 · Independencia 6/10 · Actualidad 10/10 · Acceso 9/10
- **Nivel de fiabilidad en V2.4:** C
- **Tipología:** terciaria (agregador)
- **Motivo de inclusión:** Portal comercial de datos de mercado, calendario económico y análisis; cobertura global y gratuita
- **Ámbitos:** Cotizaciones; calendario económico; análisis de opinión
- **Restricciones de uso:** Condiciones del portal; doblar verificación contra fuentes primarias (RF-0001 a RF-0007) antes de citar cualquier dato
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Sesgos posibles:** Contenido de analistas de naturaleza opinativa; datos agregados sin metodología declarada en muchas páginas
- **Cambios de propiedad o de metodología:** Sin cambios conocidos
- **Estado:** Aprobada
- **Estado del enlace:** PENDIENTE_BARRIDO
- **Última verificación:** 2026-10-25 (Completa (URL viva y naturaleza del contenido comprobadas el 25/10/2026))
- **Alerta:** Pista de descubrimiento: todo dato debe verificarse contra una fuente de nivel A antes de citarse.

## TF-07 Fuentes sectoriales y de industria

#### RF-0319 · Q 83 (A) — Institute for Supply Management — ISM Report On Business

- **Canal oficial (URL raíz):** https://ismworld.org/supply-management-news-and-reports/reports/ism-report-on-business
- **Emisor:** Institute for Supply Management (ISM)
- **Documentación y notas:** PMI manufacturero (1.er día hábil del mes), servicios (3.er día hábil) y hospitalario (5.º día hábil), a las 10:00 EST; comités de encuesta con representación proporcional al PIB sectorial; calendario y notas sobre ajustes estacionales anuales.
- **Temática:** TF-07 Fuentes sectoriales y de industria (principal) · secundarias: TF-01
- **Calidad Q:** 83 (A) — Primariedad 19/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 15/15 · Independencia 9/10 · Actualidad 10/10 · Acceso 7/10
- **Tipología:** primaria
- **Acceso:** Abierto (titulares); detalle completo en ismworld.org
- **Ámbitos:** Actividad manufacturera y de servicios de EE. UU. por sector
- **Motivo de inclusión y uso:** Encuesta de referencia del ciclo industrial estadounidense; catalizador de calendario.
- **Restricciones de uso:** Condiciones de ISM; citar informe y mes.
- **Sesgos y cautelas:** Encuesta de opinión de compras; revisiones estacionales anuales.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «ismworld.org Report On Business Manufacturing PMI Services PMI»; WebFetch: sí)

#### RF-0349 · Q 83 (A) — Stanford HAI — AI Index Report

- **Canal oficial (URL raíz):** https://hai.stanford.edu/ai-index/2026-ai-index-report
- **Emisor:** Stanford Institute for Human-Centered Artificial Intelligence (HAI)
- **Documentación y notas:** Informe anual en nueve capítulos (I+D, rendimiento técnico, IA responsable, economía, ciencia, medicina, educación, política, opinión pública); inversión privada en IA por país (EE. UU. 285.880 M$ en 2025); datos públicos en carpeta compartida y PDF completo.
- **Temática:** TF-07 Fuentes sectoriales y de industria (principal) · secundarias: TF-14
- **Calidad Q:** 83 (A) — Primariedad 16/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 8/10 · Acceso 10/10
- **Tipología:** secundaria
- **Acceso:** Abierto
- **Ámbitos:** Inversión, adopción, capacidades y regulación de la IA
- **Motivo de inclusión y uso:** Referencia académica independiente sobre el ciclo de inversión en IA.
- **Restricciones de uso:** Citar edición y capítulo; licencia de datos no declarada en la página.
- **Sesgos y cautelas:** Compilación de fuentes de terceros con métodos heterogéneos.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Stanford HAI AI Index Report 2026»; WebFetch: sí)

#### RF-0318 · Q 82 (A) — S&P Global — PMI (HCOB Eurozona y otros países)

- **Canal oficial (URL raíz):** https://www.pmi.spglobal.com/Public/Home/PressRelease/0fe4c657a20b4c469a65bd2aaae141d5
- **Emisor:** S&P Global Market Intelligence (patrocinio HCOB en la eurozona)
- **Documentación y notas:** Notas de prensa PMI con metodología: encuesta mensual (segunda quincena), índices de difusión desestacionalizados; PMI manufacturero = pedidos 30 %, producción 25 %, empleo 20 %, plazos de proveedores 15 % (invertido), existencias 10 %; ponderación por país según valor añadido de Eurostat; avance (flash) con ~89 % de respuestas. Página de producto: spglobal.com/marketintelligence/en/mi/products/pmi.html.
- **Temática:** TF-07 Fuentes sectoriales y de industria (principal) · secundarias: TF-01
- **Calidad Q:** 82 (A) — Primariedad 18/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 14/15 · Independencia 8/10 · Actualidad 10/10 · Acceso 8/10
- **Tipología:** primaria
- **Acceso:** Abierto (notas de titulares); series completas de pago
- **Ámbitos:** PMI manufacturero, servicios y compuesto por país y sector
- **Motivo de inclusión y uso:** Indicador adelantado del ciclo industrial y de servicios con avance flash a final de mes.
- **Restricciones de uso:** Condiciones de S&P Global; citar país, sector y mes (flash o final).
- **Sesgos y cautelas:** Proveedor comercial; datos detallados de pago; ajuste estacional revisable.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Patrocinadores nacionales cambian (p. ej., HCOB en la eurozona).
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «ISM Report On Business Manufacturing PMI S&P Global PMI HCOB eurozone»; WebFetch: sí)

#### RF-0322 · Q 81 (A) — Baltic Exchange — índices de fletes (BDI y otros)

- **Canal oficial (URL raíz):** https://balticexchange.com/en/who-we-are/faqs.html
- **Emisor:** Baltic Exchange (filial Baltic Exchange Information Services Ltd, administrador de índices autorizado por la FCA; vinculada al grupo SGX)
- **Documentación y notas:** Índices de graneles secos (Capesize, Panamax, Supramax, Handysize; BDI derivado de los tres primeros), petroleros (BDTI, BCTI), gas (BLNG, BLPG), contenedores (con Freightos), carga aérea semanal y curvas forward; evaluaciones de corredores panelistas sin posiciones propias.
- **Temática:** TF-07 Fuentes sectoriales y de industria (principal) · secundarias: TF-08
- **Calidad Q:** 81 (A) — Primariedad 19/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 15/15 · Independencia 8/10 · Actualidad 10/10 · Acceso 6/10
- **Tipología:** primaria
- **Acceso:** Licencia para uso de datos (API, prueba gratuita); valores difundidos por prensa
- **Ámbitos:** Fletes marítimos de graneles, petroleros y gas
- **Motivo de inclusión y uso:** Índice de referencia del comercio de materias primas a granel y del ciclo global.
- **Restricciones de uso:** Licencia Baltic Data para uso contractual; citar índice y fecha.
- **Sesgos y cautelas:** Datos completos de pago; las cifras de prensa son de segunda mano.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Propiedad del grupo SGX (no detallada en la página leída).
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «balticexchange.com Baltic Dry Index dry bulk freight indices»; WebFetch: sí)

#### RF-0350 · Q 81 (A) — SIPRI — base de datos de la industria de armamento (Top 100)

- **Canal oficial (URL raíz):** https://sipri.org/databases/armsindustry
- **Emisor:** Stockholm International Peace Research Institute (SIPRI)
- **Documentación y notas:** Ventas de armamento de las 100 principales empresas (Excel 2002–2024), con fuentes abiertas (informes anuales, prensa) y estimaciones; revisión anual de toda la serie; uso comercial con licencia.
- **Temática:** TF-07 Fuentes sectoriales y de industria (principal) · secundarias: TF-14
- **Calidad Q:** 81 (A) — Primariedad 16/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 7/10 · Acceso 9/10
- **Tipología:** secundaria
- **Acceso:** Abierto (uso no comercial)
- **Ámbitos:** Industria de defensa: ingresos por armamento por empresa y país
- **Motivo de inclusión y uso:** Referencia para el ciclo de gasto en defensa y sus beneficiarios cotizados.
- **Restricciones de uso:** Términos de SIPRI; uso comercial con autorización.
- **Sesgos y cautelas:** Estimaciones a partir de fuentes abiertas; cobertura limitada de China y Rusia.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Rusia desde 2002 y China parcial desde 2015.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «SIPRI Top 100 arms-producing companies arms industry database»; WebFetch: sí)

#### RF-0320 · Q 79 (B) — worldsteel — producción mundial de acero

- **Canal oficial (URL raíz):** https://worldsteel.org/media/press-releases
- **Emisor:** World Steel Association (worldsteel)
- **Documentación y notas:** Nota mensual de producción de acero bruto (70 países; septiembre de 2026: 142,4 Mt, −0,2 % interanual, publicada el 23/10/2026); World Steel in Figures (junio) y Short Range Outlook de demanda (abril y octubre).
- **Temática:** TF-07 Fuentes sectoriales y de industria (principal) · secundarias: TF-08
- **Calidad Q:** 79 (B) — Primariedad 18/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 14/15 · Independencia 7/10 · Actualidad 9/10 · Acceso 9/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** Producción de acero por país; demanda prevista
- **Motivo de inclusión y uso:** Termómetro de construcción, automóvil y maquinaria; demanda de mineral de hierro y carbón.
- **Restricciones de uso:** Citar mes y nota.
- **Sesgos y cautelas:** Asociación sectorial; datos de algunos países estimados.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «worldsteel monthly crude steel production press release»; WebFetch: sí)

#### RF-0325 · Q 79 (B) — ONU Turismo (UN Tourism, antes UNWTO) — barómetro y estadísticas de turismo

- **Canal oficial (URL raíz):** https://www.untourism.int/
- **Emisor:** Organización Mundial del Turismo de las Naciones Unidas (ONU Turismo)
- **Documentación y notas:** Organismo de la ONU que publica el World Tourism Barometer y estadísticas de llegadas internacionales; dominio untourism.int (el anterior unwto.org sigue apareciendo en resultados).
- **Temática:** TF-07 Fuentes sectoriales y de industria (principal) · secundarias: TF-01
- **Calidad Q:** 79 (B) — Primariedad 18/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 15/15 · Independencia 9/10 · Actualidad 7/10 · Acceso 8/10
- **Tipología:** primaria
- **Acceso:** Abierto (parcial)
- **Ámbitos:** Llegadas e ingresos por turismo internacional
- **Motivo de inclusión y uso:** Indicador de demanda turística (relevante para España).
- **Restricciones de uso:** Citar edición y periodo.
- **Sesgos y cautelas:** Frecuencia baja; estimaciones provisionales.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Cambio de denominación UNWTO → UN Tourism.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «IATA air passenger market analysis monthly UN Tourism World Tourism Barometer»; WebFetch: intentado, error del sitio)

#### RF-0303 · Q 77 (B) — ACEA — estadísticas del automóvil en Europa

- **Canal oficial (URL raíz):** https://www.acea.auto/reliable-data-statistics/
- **Emisor:** European Automobile Manufacturers' Association (ACEA)
- **Documentación y notas:** Notas de prensa mensuales de matriculaciones de turismos (por país, combustible y fabricante) y trimestrales de vehículos comerciales; calendario anual de publicación; series de producción, comercio, parque, empleo y fiscalidad. Directorio de asociaciones nacionales: acea.auto/national-automobile-associations/. Datos avanzados en ACEA Intelligence (servicio aparte).
- **Temática:** TF-07 Fuentes sectoriales y de industria (principal)
- **Calidad Q:** 77 (B) — Primariedad 17/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 14/15 · Independencia 6/10 · Actualidad 9/10 · Acceso 9/10
- **Tipología:** primaria
- **Acceso:** Abierto (notas y series públicas); servicio avanzado aparte
- **Ámbitos:** Matriculaciones UE/EFTA/Reino Unido, cuota de vehículo eléctrico, producción
- **Motivo de inclusión y uso:** Indicador mensual de demanda de automóviles y de transición a eléctrico en Europa.
- **Restricciones de uso:** Citar nota de prensa y mes.
- **Sesgos y cautelas:** Asociación sectorial (agenda de lobby).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «OICA ACEA ANFAC vehicle production registrations statistics official»; WebFetch: sí)

#### RF-0057 · Q 76 (B) — Semiconductor Industry Association (SIA) y WSTS

- **Canal oficial (URL raíz):** https://www.semiconductors.org/
- **Emisor:** Semiconductor Industry Association (SIA); datos de World Semiconductor Trade Statistics (WSTS, https://www.wsts.org/)
- **Documentación y notas:** Nota mensual «Global Semiconductor Sales…» con ventas mundiales (media móvil de 3 meses compilada por WSTS) y desglose regional; SIA Databook (histórico) y paquete de suscripción WSTS (datos mensuales y previsiones) enlazados desde las notas.
- **Temática:** TF-07 Fuentes sectoriales y de industria (principal)
- **Calidad Q:** 76 (B) — Primariedad 17/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 13/15 · Independencia 6/10 · Actualidad 8/10 · Acceso 9/10
- **Tipología:** primaria
- **Acceso:** Abierto (notas mensuales); datos detallados de pago
- **Ámbitos:** Ventas mensuales de semiconductores por región; previsiones WSTS
- **Motivo de inclusión y uso:** Indicador sectorial adelantado del ciclo tecnológico.
- **Restricciones de uso:** Citar mes de referencia y que es media móvil de 3 meses.
- **Sesgos y cautelas:** Asociación sectorial (sesgo promocional); desfase de unas 5 semanas.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Semiconductor Industry Association global semiconductor sales WSTS monthly»; WebFetch: sí, nota de prensa mensual)

#### RF-0324 · Q 76 (B) — IATA — análisis de mercado de pasajeros y carga aérea

- **Canal oficial (URL raíz):** https://www.iata.org/en/publications/economics/economics-library/?page=25
- **Emisor:** International Air Transport Association (IATA)
- **Documentación y notas:** Biblioteca económica (1.963 informes desde 2005): Air Passenger Market Analysis y Air Cargo Market Analysis mensuales, Chart of the Week, Quarterly Air Transport Chartbook, Global Outlook for Air Transport semestral, Airlines Financial Monitor.
- **Temática:** TF-07 Fuentes sectoriales y de industria (principal) · secundarias: TF-14
- **Calidad Q:** 76 (B) — Primariedad 17/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 14/15 · Independencia 6/10 · Actualidad 9/10 · Acceso 8/10
- **Tipología:** primaria
- **Acceso:** Abierto (la mayoría de informes)
- **Ámbitos:** Tráfico aéreo de pasajeros (RPK, ASK) y carga; resultados del sector
- **Motivo de inclusión y uso:** Indicador mensual de viajes y comercio aéreo.
- **Restricciones de uso:** Citar informe y mes.
- **Sesgos y cautelas:** Asociación de aerolíneas (sesgo sectorial).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «IATA air passenger market analysis monthly UN Tourism World Tourism Barometer»; WebFetch: sí)

#### RF-0305 · Q 75 (B) — ANFAC — matriculaciones y producción en España

- **Canal oficial (URL raíz):** https://www.anfac.com/
- **Emisor:** Asociación Española de Fabricantes de Automóviles y Camiones (ANFAC)
- **Documentación y notas:** Asociación nacional española miembro de ACEA (listada en el directorio oficial de ACEA). Publica matriculaciones mensuales y datos de producción de vehículos en España.
- **Temática:** TF-07 Fuentes sectoriales y de industria (principal)
- **Calidad Q:** 75 (B) — Primariedad 17/20 · Historial 10/20 · Transparencia 11/15 · Autoridad 13/15 · Independencia 6/10 · Actualidad 9/10 · Acceso 9/10
- **Tipología:** primaria
- **Acceso:** Abierto (notas de prensa)
- **Ámbitos:** Mercado y producción de automóviles en España
- **Motivo de inclusión y uso:** Fuente sectorial española para consumo duradero e industria del automóvil.
- **Restricciones de uso:** Citar nota y mes.
- **Sesgos y cautelas:** Asociación sectorial. Productos concretos no leídos directamente: confirmar en el próximo barrido.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «OICA ACEA ANFAC vehicle production registrations statistics official»; URL tomada del directorio de asociaciones nacionales de ACEA leído con WebFetch; WebFetch al sitio: no)

#### RF-0306 · Q 75 (B) — SMMT — matriculaciones y producción en el Reino Unido

- **Canal oficial (URL raíz):** https://www.smmt.co.uk/
- **Emisor:** Society of Motor Manufacturers and Traders (SMMT)
- **Documentación y notas:** Asociación nacional británica listada en el directorio oficial de ACEA; referencia de matriculaciones mensuales y producción de vehículos en el Reino Unido.
- **Temática:** TF-07 Fuentes sectoriales y de industria (principal)
- **Calidad Q:** 75 (B) — Primariedad 17/20 · Historial 10/20 · Transparencia 11/15 · Autoridad 13/15 · Independencia 6/10 · Actualidad 9/10 · Acceso 9/10
- **Tipología:** primaria
- **Acceso:** Abierto (notas de prensa)
- **Ámbitos:** Mercado y producción de automóviles en el Reino Unido
- **Motivo de inclusión y uso:** Dato mensual de demanda de vehículos fuera de la UE.
- **Restricciones de uso:** Citar nota y mes.
- **Sesgos y cautelas:** Asociación sectorial. Productos concretos no leídos directamente: confirmar en el próximo barrido.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «OICA ACEA ANFAC vehicle production registrations statistics official»; URL tomada del directorio de asociaciones nacionales de ACEA leído con WebFetch; WebFetch al sitio: no)

#### RF-0321 · Q 75 (B) — SEMI — facturación mundial de equipos de semiconductores

- **Canal oficial (URL raíz):** https://www.semi.org/en/semi-press-release/semi-reports-global-semiconductor-equipment-billings-increased-14-percent-year-over-year-in-q1-2026
- **Emisor:** SEMI (asociación mundial de la cadena de suministro de semiconductores)
- **Documentación y notas:** Notas trimestrales de facturación mundial de equipos (1T 2026: 36.550 M$, +14 % interanual; publicada 04/06/2026) a partir del informe mensual WWSEMS (datos de miembros de SEMI y de SEAJ); suscripción EMDS con informe norteamericano mensual y previsión semestral.
- **Temática:** TF-07 Fuentes sectoriales y de industria (principal) · secundarias: TF-06
- **Calidad Q:** 75 (B) — Primariedad 17/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 14/15 · Independencia 6/10 · Actualidad 8/10 · Acceso 8/10
- **Tipología:** primaria
- **Acceso:** Abierto (notas); datos detallados de pago
- **Ámbitos:** Inversión en equipos de semiconductores por región y segmento
- **Motivo de inclusión y uso:** Indicador del ciclo de inversión (capex) en semiconductores, complemento de RF-0057.
- **Restricciones de uso:** Citar trimestre y nota.
- **Sesgos y cautelas:** Asociación sectorial (sesgo promocional).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «SEMI worldwide semiconductor equipment billings report»; WebFetch: sí)

#### RF-0307 · Q 74 (B) — VDA — industria del automóvil en Alemania

- **Canal oficial (URL raíz):** https://www.vda.de/
- **Emisor:** Verband der Automobilindustrie (VDA)
- **Documentación y notas:** Asociación nacional alemana listada en el directorio oficial de ACEA; publica producción y exportación de turismos de fabricantes alemanes.
- **Temática:** TF-07 Fuentes sectoriales y de industria (principal)
- **Calidad Q:** 74 (B) — Primariedad 17/20 · Historial 10/20 · Transparencia 11/15 · Autoridad 13/15 · Independencia 6/10 · Actualidad 9/10 · Acceso 8/10
- **Tipología:** primaria
- **Acceso:** Abierto (parcial; contenidos en alemán)
- **Ámbitos:** Producción, exportación y mercado interior de automóviles en Alemania
- **Motivo de inclusión y uso:** Termómetro del principal productor europeo de automóviles (ciclo industrial alemán).
- **Restricciones de uso:** Citar publicación y mes.
- **Sesgos y cautelas:** Asociación sectorial. Productos concretos no leídos directamente: confirmar en el próximo barrido.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «OICA ACEA ANFAC vehicle production registrations statistics official»; URL tomada del directorio de asociaciones nacionales de ACEA leído con WebFetch; WebFetch al sitio: no)

#### RF-0348 · Q 74 (B) — GSMA Intelligence — The Mobile Economy

- **Canal oficial (URL raíz):** https://www.gsma.com/solutions-and-impact/connectivity-for-good/mobile-economy/wp-content/uploads/2026/02/The-Mobile-Economy-2026.pdf
- **Emisor:** GSMA (GSMA Intelligence)
- **Documentación y notas:** Informe anual mundial y regional: 8.800 millones de conexiones y 5.800 millones de abonados únicos, adopción de 5G, ingresos y capex de operadores con previsiones a 2030; serie en gsmaintelligence.com/series/the-mobile-economy.
- **Temática:** TF-07 Fuentes sectoriales y de industria (principal) · secundarias: TF-14
- **Calidad Q:** 74 (B) — Primariedad 16/20 · Historial 10/20 · Transparencia 11/15 · Autoridad 14/15 · Independencia 6/10 · Actualidad 8/10 · Acceso 9/10
- **Tipología:** primaria
- **Acceso:** Abierto (informe); datos detallados de pago
- **Ámbitos:** Telecomunicaciones móviles: abonados, 5G, ingresos, inversión
- **Motivo de inclusión y uso:** Referencia sectorial para operadores y fabricantes de redes.
- **Restricciones de uso:** Citar edición y región.
- **Sesgos y cautelas:** Asociación de operadores (sesgo sectorial); previsiones propias.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «GSMA Intelligence The Mobile Economy report»; WebFetch: sí)

#### RF-0304 · Q 73 (B) — OICA — producción y ventas mundiales de vehículos

- **Canal oficial (URL raíz):** https://oica.net/statistics
- **Emisor:** Organisation Internationale des Constructeurs d'Automobiles (OICA)
- **Documentación y notas:** Secciones de producción (por fabricante y mercado) y ventas mundiales; Destatis la registra como fuente de estadística internacional.
- **Temática:** TF-07 Fuentes sectoriales y de industria (principal)
- **Calidad Q:** 73 (B) — Primariedad 17/20 · Historial 10/20 · Transparencia 11/15 · Autoridad 14/15 · Independencia 7/10 · Actualidad 6/10 · Acceso 8/10
- **Tipología:** primaria
- **Acceso:** Abierto (tablas); existe área de miembros
- **Ámbitos:** Producción y ventas mundiales de vehículos por país y fabricante
- **Motivo de inclusión y uso:** Comparativa global anual de la industria del automóvil.
- **Restricciones de uso:** Citar año y tabla.
- **Sesgos y cautelas:** Frecuencia anual; la página no indica el último año cubierto.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «OICA ACEA ANFAC vehicle production registrations statistics official»; WebFetch: sí)

#### RF-0351 · Q 73 (B) — American Chemistry Council — Chemical Activity Barometer

- **Canal oficial (URL raíz):** https://www.americanchemistry.com/
- **Emisor:** American Chemistry Council (ACC)
- **Documentación y notas:** Indicador adelantado mensual de la actividad industrial de EE. UU. basado en la química (media móvil de tres meses); difundido por la prensa sectorial y por Calculated Risk, que enlaza las notas de prensa en americanchemistry.com y lo describe como adelantado de la producción industrial.
- **Temática:** TF-07 Fuentes sectoriales y de industria (principal) · secundarias: TF-01
- **Calidad Q:** 73 (B) — Primariedad 16/20 · Historial 10/20 · Transparencia 10/15 · Autoridad 13/15 · Independencia 6/10 · Actualidad 9/10 · Acceso 9/10
- **Tipología:** primaria
- **Acceso:** Abierto (notas de prensa)
- **Ámbitos:** Química estadounidense como indicador adelantado industrial
- **Motivo de inclusión y uso:** Señal temprana del ciclo manufacturero.
- **Restricciones de uso:** Citar mes.
- **Sesgos y cautelas:** Asociación sectorial. Página del barómetro no leída directamente: confirmar URL de la pieza.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «American Chemistry Council Chemical Activity Barometer»; dominio confirmado por el enlace de Calculated Risk leído con WebFetch; WebFetch al sitio: no)

#### RF-0058 · Q 71 (B) — International Federation of Robotics — World Robotics

- **Canal oficial (URL raíz):** https://ifr.org/about-world-robotics/
- **Emisor:** International Federation of Robotics (IFR)
- **Documentación y notas:** Informe anual en dos volúmenes (Industrial Robots, con cobots; Service Robots); estadísticas de proveedores y asociaciones nacionales; instalaciones, parque operativo y densidad robótica; base de datos histórica (desde 1993 en algunos casos) en versión premium. Gratuitos: presentación de la rueda de prensa y notas de prensa (p. ej., «World Robotics 2025 report»).
- **Temática:** TF-07 Fuentes sectoriales y de industria (principal)
- **Calidad Q:** 71 (B) — Primariedad 16/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 13/15 · Independencia 6/10 · Actualidad 7/10 · Acceso 7/10
- **Tipología:** primaria
- **Acceso:** Resúmenes y presentaciones abiertos; informe de pago (VDMA Verlag)
- **Ámbitos:** Instalaciones de robots industriales y de servicio
- **Motivo de inclusión y uso:** Medida de difusión de la automatización.
- **Restricciones de uso:** Citar edición y tabla; usar solo contenidos públicos.
- **Sesgos y cautelas:** Asociación sectorial; informe completo de pago; frecuencia anual.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «IFR World Robotics report International Federation of Robotics»; WebFetch: sí)

#### RF-0323 · Q 71 (B) — Drewry — World Container Index

- **Canal oficial (URL raíz):** https://www.drewry.co.uk/logistics-executive-briefing/logistics-executive-briefing-articles/world-container-index
- **Emisor:** Drewry (consultora marítima)
- **Documentación y notas:** Índice compuesto Este-Oeste en $/FEU con variación semanal; difundido cada semana por prensa marítima. La página leída mostraba un valor de 16/02/2023 (contenido desactualizado o en caché) y no detalla metodología.
- **Temática:** TF-07 Fuentes sectoriales y de industria (principal) · secundarias: TF-08
- **Calidad Q:** 71 (B) — Primariedad 16/20 · Historial 10/20 · Transparencia 9/15 · Autoridad 13/15 · Independencia 7/10 · Actualidad 8/10 · Acceso 8/10
- **Tipología:** primaria
- **Acceso:** Abierto (valor compuesto)
- **Ámbitos:** Fletes de contenedores en rutas Este-Oeste
- **Motivo de inclusión y uso:** Indicador semanal del coste del transporte marítimo de contenedores.
- **Restricciones de uso:** Citar fecha y ruta.
- **Sesgos y cautelas:** Metodología no publicada en la página; consultora con servicios de pago.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Drewry World Container Index drewry.co.uk»; WebFetch: sí)

#### RF-0326 · Q 61 (C) — gCaptain — noticias marítimas

- **Canal oficial (URL raíz):** https://gcaptain.com/tag/baltic-dry-index
- **Emisor:** gCaptain
- **Documentación y notas:** Medio de noticias marítimas y offshore; etiqueta del Baltic Dry Index con artículos (último visto: 07/05/2026).
- **Temática:** TF-07 Fuentes sectoriales y de industria (principal) · secundarias: TF-03
- **Calidad Q:** 61 (C) — Primariedad 9/20 · Historial 10/20 · Transparencia 7/15 · Autoridad 9/15 · Independencia 7/10 · Actualidad 9/10 · Acceso 10/10
- **Tipología:** secundaria
- **Acceso:** Abierto
- **Ámbitos:** Transporte marítimo, fletes, puertos
- **Motivo de inclusión y uso:** Contexto de noticias del sector naval; los datos se citan en RF-0322 o RF-0323.
- **Restricciones de uso:** Opinión/noticia: los hechos se citan en su fuente primaria.
- **Sesgos y cautelas:** Entidad editora no declarada en la página leída.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin datos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «balticexchange.com Baltic Dry Index dry bulk freight indices»; WebFetch: sí)

## TF-08 Materias primas y energía (agencias y datos)

#### RF-0059 · Q 90 (A) — U.S. Energy Information Administration (EIA)

- **Canal oficial (URL raíz):** https://www.eia.gov/
- **Emisor:** U.S. Energy Information Administration (Departamento de Energía de EE. UU.)
- **Documentación y notas:** Pieza principal: Weekly Petroleum Status Report (https://eia.gov/petroleum/supply/weekly; calendario en …/weekly/schedule.php; descargas XLSX/CSV/JSON; notas explicativas y fe de erratas). Enlaza Short-Term Energy Outlook (eia.gov/outlooks/steo/), Annual Energy Outlook, Monthly Energy Review, precios spot diarios y precios minoristas semanales. Último número listado en la consulta: 21/10/2026.
- **Temática:** TF-08 Materias primas y energía (agencias y datos) (principal) · secundarias: TF-01
- **Calidad Q:** 90 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 15/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 10/10 · Acceso 10/10
- **Tipología:** primaria
- **Acceso:** Abierto (dominio público)
- **Ámbitos:** Inventarios semanales de crudo y productos, producción, importaciones; previsiones STEO
- **Motivo de inclusión y uso:** Dato primario de energía; catalizador semanal para H1-H2.
- **Restricciones de uso:** Uso libre; citar informe, tabla y semana.
- **Sesgos y cautelas:** Cobertura centrada en EE. UU.; estimaciones semanales sujetas a revisión mensual.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «EIA Weekly Petroleum Status Report Short-Term Energy Outlook eia.gov»; WebFetch: sí)

#### RF-0061 · Q 89 (A) — USDA — WASDE

- **Canal oficial (URL raíz):** https://www.usda.gov/about-usda/general-information/staff-offices/office-chief-economist/commodity-markets/wasde-report
- **Emisor:** U.S. Department of Agriculture — World Agricultural Outlook Board (WAOB)
- **Documentación y notas:** Informe mensual (12:00 ET) de oferta y demanda de trigo, arroz, cereales secundarios, oleaginosas y algodón (EE. UU. y mundo) y de azúcar, carne, aves, huevos y leche (EE. UU.). Último visto: 09/10/2026; siguiente: 10/11/2026. Acceso corto: usda.gov/wasde. Archivo histórico en ESMIS (esmis.nal.usda.gov).
- **Temática:** TF-08 Materias primas y energía (agencias y datos) (principal)
- **Calidad Q:** 89 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 15/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 9/10 · Acceso 10/10
- **Tipología:** primaria
- **Acceso:** Abierto (dominio público)
- **Ámbitos:** Balances mundiales de oferta y demanda agrícola
- **Motivo de inclusión y uso:** Informe mensual que mueve los precios agrícolas (catalizador de calendario).
- **Restricciones de uso:** Uso libre; citar edición mensual.
- **Sesgos y cautelas:** Revisiones mensuales de las estimaciones.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Reorganización de URL en usda.gov (la URL antigua /oce/commodity/wasde aparece aún en buscadores).
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «USDA WASDE World Agricultural Supply and Demand Estimates report»; WebFetch: sí)

#### RF-0067 · Q 89 (A) — FAO — Índice de precios de los alimentos

- **Canal oficial (URL raíz):** https://www.fao.org/worldfoodsituation/FoodPricesIndex/en
- **Emisor:** Organización de las Naciones Unidas para la Alimentación y la Agricultura (FAO)
- **Documentación y notas:** Índice mensual ponderado por cuotas de exportación 2014-2016 de cinco subíndices (cereales, aceites vegetales, azúcar, carne, lácteos). Última publicación vista: 02/10/2026 (septiembre: 136,0 puntos); próxima: 06/11/2026.
- **Temática:** TF-08 Materias primas y energía (agencias y datos) (principal) · secundarias: TF-01
- **Calidad Q:** 89 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 15/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 9/10 · Acceso 10/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** Precios internacionales de alimentos
- **Motivo de inclusión y uso:** Indicador mensual de inflación alimentaria global.
- **Restricciones de uso:** Uso con atribución; citar mes y versión (se revisa).
- **Sesgos y cautelas:** Índice agregado; el subíndice de carne usa precios proyectados y se revisa de forma significativa.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «EIA WASDE FAO food price index OPEC MOMR World Bank Pink Sheet LBMA LME World Gold Council»; WebFetch: sí)

#### RF-0356 · Q 86 (A) — USGS — Mineral Commodity Summaries

- **Canal oficial (URL raíz):** https://www.usgs.gov/centers/national-minerals-information-center/mineral-commodity-summaries
- **Emisor:** U.S. Geological Survey (National Minerals Information Center)
- **Documentación y notas:** Publicación anual con fichas de más de 90 minerales (estructura de la industria, aranceles, cinco años de estadísticas, producción mundial y reservas); edición 2026 y publicación de datos (doi.org/10.5066/P1WKQ63T).
- **Temática:** TF-08 Materias primas y energía (agencias y datos) (principal) · secundarias: TF-01
- **Calidad Q:** 86 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 15/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 6/10 · Acceso 10/10
- **Tipología:** primaria
- **Acceso:** Abierto (dominio público)
- **Ámbitos:** Producción, reservas y precios de minerales y metales críticos
- **Motivo de inclusión y uso:** Referencia oficial sobre minerales críticos (litio, cobre, tierras raras).
- **Restricciones de uso:** Uso libre; citar edición y mineral.
- **Sesgos y cautelas:** Frecuencia anual; datos del año anterior estimados.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «USGS Mineral Commodity Summaries 2026»; WebFetch: sí)

#### RF-0062 · Q 85 (A) — OPEP — Monthly Oil Market Report

- **Canal oficial (URL raíz):** https://www.opec.org/
- **Emisor:** Organización de Países Exportadores de Petróleo (OPEP)
- **Documentación y notas:** URL raíz confirmada en la lista de organizaciones socias de JODI (jodidata.org). La página concreta del Monthly Oil Market Report no se ha leído (sitio no accesible con la herramienta).
- **Temática:** TF-08 Materias primas y energía (agencias y datos) (principal)
- **Calidad Q:** 85 (A) — Primariedad 18/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 14/15 · Independencia 9/10 · Actualidad 10/10 · Acceso 10/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** Oferta, demanda y producción de crudo de la OPEP
- **Motivo de inclusión y uso:** Fuente primaria de la política de oferta de la OPEP.
- **Restricciones de uso:** Citar edición del MOMR.
- **Sesgos y cautelas:** Parte interesada en el precio; producción de miembros por fuentes secundarias y comunicación directa.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «JODI Oil World Database partner organisations APEC Eurostat GECF IEA OPEC»; URL tomada de la página de socios de JODI leída con WebFetch; WebFetch al sitio: no)
- **Alerta:** REPARAR en el próximo barrido: leer y registrar la URL de la pieza MOMR.

#### RF-0066 · Q 85 (A) — Banco Mundial — Commodity Markets (Pink Sheet y Outlook)

- **Canal oficial (URL raíz):** https://www.worldbank.org/en/research/commodity-markets
- **Emisor:** Banco Mundial
- **Documentación y notas:** Pink Sheet mensual (PDF de precios, XLS mensual y anual; última actualización vista 02/10/2026, siguiente 03/11/2026) y Commodity Markets Outlook semestral (última edición octubre de 2026, siguiente abril de 2027). Ficheros en Open Knowledge Repository; licencia CC BY para datos.
- **Temática:** TF-08 Materias primas y energía (agencias y datos) (principal) · secundarias: TF-01
- **Calidad Q:** 85 (A) — Primariedad 18/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 8/10 · Acceso 10/10
- **Tipología:** secundaria
- **Acceso:** Abierto (CC BY)
- **Ámbitos:** Precios mensuales de materias primas y previsiones semestrales
- **Motivo de inclusión y uso:** Serie homogénea larga de precios y previsiones institucionales.
- **Restricciones de uso:** Atribución CC BY; citar edición.
- **Sesgos y cautelas:** Frecuencia mensual; previsiones con supuestos propios.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «World Bank Commodity Markets Pink Sheet monthly prices Commodity Markets Outlook»; WebFetch: sí)

#### RF-0358 · Q 85 (A) — CORES — Boletín Estadístico de Hidrocarburos

- **Canal oficial (URL raíz):** https://www.cores.es/sites/default/files/archivos/publicaciones/boletin-est-hidrocarburos-333-agosto-2025.pdf
- **Emisor:** Corporación de Reservas Estratégicas de Productos Petrolíferos (CORES; tutelada por el MITECO)
- **Documentación y notas:** Boletín numerado mensual con consumo de productos petrolíferos y gas natural, importaciones de crudo por origen, balances, precios, comercio exterior y reservas en España (n.º 333, agosto de 2025: importaciones de crudo de 5.138 kt, −10,9 % interanual).
- **Temática:** TF-08 Materias primas y energía (agencias y datos) (principal) · secundarias: TF-01
- **Calidad Q:** 85 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 7/10 · Acceso 10/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** Consumo de carburantes y gas, importaciones de crudo en España
- **Motivo de inclusión y uso:** Fuente oficial española de energía (demanda doméstica y seguridad de suministro).
- **Restricciones de uso:** Uso con atribución; citar número y mes.
- **Sesgos y cautelas:** Desfase de unos dos meses.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «CORES Corporación de Reservas Estratégicas de Productos Petrolíferos boletín estadístico consumo»; WebFetch: sí)

#### RF-0354 · Q 84 (A) — IRENA — estadísticas de energías renovables

- **Canal oficial (URL raíz):** https://www.irena.org/-/media/Files/IRENA/Agency/Publication/2026/Jul/IRENA_DAT_RE_Statistics_2026.pdf
- **Emisor:** International Renewable Energy Agency (IRENA)
- **Documentación y notas:** Renewable Energy Statistics 2026: capacidad 2016–2025 y producción 2016–2024 por tecnología, país y región, capacidad aislada, financiación pública e indicadores ODS 7; datos en irena.org/statistics. Publica además Renewable Capacity Statistics (marzo/abril).
- **Temática:** TF-08 Materias primas y energía (agencias y datos) (principal) · secundarias: TF-01
- **Calidad Q:** 84 (A) — Primariedad 19/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 9/10 · Actualidad 7/10 · Acceso 10/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** Capacidad y generación renovable mundial
- **Motivo de inclusión y uso:** Fuente oficial intergubernamental de despliegue renovable.
- **Restricciones de uso:** Uso con atribución; citar edición.
- **Sesgos y cautelas:** Desfase de uno a dos años en producción.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «IRENA Renewable Capacity Statistics 2026»; WebFetch: sí)

#### RF-0355 · Q 84 (A) — GIE — AGSI+ y ALSI (almacenamiento de gas y GNL en Europa)

- **Canal oficial (URL raíz):** https://www.gie.eu/agsi-and-alsi-transparency-platforms/
- **Emisor:** Gas Infrastructure Europe (GIE)
- **Documentación y notas:** Plataformas de transparencia con datos diarios de existencias de almacenamiento subterráneo (AGSI, agsi.gie.eu; 100 % del mercado UE-27) y de terminales de GNL (ALSI, alsi.gie.eu), aportados por los operadores; plataforma de información privilegiada iip.gie.eu.
- **Temática:** TF-08 Materias primas y energía (agencias y datos) (principal) · secundarias: —
- **Calidad Q:** 84 (A) — Primariedad 19/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 14/15 · Independencia 8/10 · Actualidad 10/10 · Acceso 10/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** Llenado de almacenes de gas y emisión de GNL en Europa
- **Motivo de inclusión y uso:** Indicador diario clave del equilibrio del gas europeo (precio TTF).
- **Restricciones de uso:** Citar fecha y país.
- **Sesgos y cautelas:** Datos declarados por operadores de forma voluntaria.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «GIE AGSI+ aggregated gas storage inventory»; WebFetch: sí)

#### RF-0308 · Q 83 (A) — JODI — Joint Organisations Data Initiative (JODI-Oil y JODI-Gas)

- **Canal oficial (URL raíz):** https://www.jodidata.org/oil/database.aspx
- **Emisor:** Joint Organisations Data Initiative, coordinada por el International Energy Forum (IEF); socios: APEC, Eurostat, GECF, IEA, OLADE, OPEP, UNSD
- **Documentación y notas:** Base mundial de petróleo actualizada mensualmente con datos de unos 100 países (≈ 90 % de la oferta y demanda mundial); calendario de actualización y lista de economías participantes; cuestionario normalizado.
- **Temática:** TF-08 Materias primas y energía (agencias y datos) (principal) · secundarias: TF-01
- **Calidad Q:** 83 (A) — Primariedad 18/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 9/10 · Acceso 8/10
- **Tipología:** primaria
- **Acceso:** Abierto (descargas; algunas funciones con registro)
- **Ámbitos:** Producción, demanda, existencias y comercio de crudo y productos por país (y gas en JODI-Gas)
- **Motivo de inclusión y uso:** Base multilateral oficial para balances petroleros por país, independiente de una sola agencia.
- **Restricciones de uso:** Citar país, serie y mes de actualización.
- **Sesgos y cautelas:** Calidad heterogénea según el país declarante; la página de base de datos mostraba «Coming soon» en la sección de visualización.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «JODI Oil World Database partner organisations APEC Eurostat GECF IEA OPEC»; WebFetch: sí)

#### RF-0352 · Q 83 (A) — Energy Institute — Statistical Review of World Energy

- **Canal oficial (URL raíz):** https://www.energyinst.org/__data/assets/pdf_file/0004/1822009/Statistical-Review-of-World-Energy-2026-Summary-version.pdf
- **Emisor:** Energy Institute (con Ember, Kearney y KPMG; compilación de Wattage)
- **Documentación y notas:** 75.ª edición (2026, datos de 2025): producción, consumo, comercio y emisiones de energía por país; libro Excel y base de datos con histórico desde 1965 en energyinst.org/statistical-review. Heredera de la antigua revisión de BP.
- **Temática:** TF-08 Materias primas y energía (agencias y datos) (principal) · secundarias: TF-14
- **Calidad Q:** 83 (A) — Primariedad 17/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 9/10 · Actualidad 8/10 · Acceso 10/10
- **Tipología:** secundaria
- **Acceso:** Abierto
- **Ámbitos:** Balances energéticos mundiales por país y fuente
- **Motivo de inclusión y uso:** Serie larga homogénea de energía mundial para análisis estructural.
- **Restricciones de uso:** Citar edición y tabla.
- **Sesgos y cautelas:** Frecuencia anual; datos del año anterior.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Editor desde 2023: Energy Institute (antes BP).
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Energy Institute Statistical Review of World Energy 2026»; WebFetch: sí)

#### RF-0060 · Q 82 (A) — International Energy Agency (IEA)

- **Canal oficial (URL raíz):** https://www.iea.org/
- **Emisor:** International Energy Agency (IEA)
- **Documentación y notas:** URL raíz confirmada en la lista de organizaciones socias de JODI. Las piezas (Oil Market Report, World Energy Outlook) no se han leído (sitio no accesible con la herramienta).
- **Temática:** TF-08 Materias primas y energía (agencias y datos) (principal) · secundarias: TF-14
- **Calidad Q:** 82 (A) — Primariedad 18/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 9/10 · Actualidad 9/10 · Acceso 7/10
- **Tipología:** primaria
- **Acceso:** Parcialmente abierto
- **Ámbitos:** Oil Market Report, World Energy Outlook, transición energética
- **Motivo de inclusión y uso:** Referencia global de oferta y demanda de energía y escenarios.
- **Restricciones de uso:** Condiciones de la IEA (parte de los datos con licencia).
- **Sesgos y cautelas:** Escenarios con supuestos de política; parte de pago.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «JODI Oil World Database partner organisations APEC Eurostat GECF IEA OPEC»; URL tomada de la página de socios de JODI leída con WebFetch; WebFetch al sitio: no)
- **Alerta:** REPARAR en el próximo barrido: registrar URL de las piezas OMR y WEO.

#### RF-0063 · Q 82 (A) — LBMA — precios y estadísticas de metales preciosos

- **Canal oficial (URL raíz):** https://www.lbma.org.uk/prices-and-data/london-vault-data
- **Emisor:** London Bullion Market Association (LBMA)
- **Documentación y notas:** Sección Prices & Data: LBMA Gold/Silver/Platinum/Palladium Price, datos diarios de negociación (trade reporting), compensación, origen por país, encuesta anual de previsiones. Datos de cámaras de Londres mensuales (5.º día hábil, mes vencido): fin de septiembre de 2026, 9.821 t de oro y 28.985 t de plata.
- **Temática:** TF-08 Materias primas y energía (agencias y datos) (principal)
- **Calidad Q:** 82 (A) — Primariedad 18/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 14/15 · Independencia 8/10 · Actualidad 10/10 · Acceso 8/10
- **Tipología:** primaria
- **Acceso:** Abierto (parcial); precios de referencia con licencia
- **Ámbitos:** Precios de referencia de metales preciosos; existencias en Londres; volúmenes negociados
- **Motivo de inclusión y uso:** Referencia oficial del mercado de lingotes y de existencias físicas.
- **Restricciones de uso:** Licencia para uso de precios; citar mes de datos.
- **Sesgos y cautelas:** La página mostraba una cifra de metadatos (US$430 000 M) incoherente con el cuerpo (US$1,3 billones): usar el cuerpo/tabla.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «LBMA Gold Price LBMA Silver Price London vault holdings data»; WebFetch: sí)

#### RF-0065 · Q 82 (A) — London Metal Exchange (LME)

- **Canal oficial (URL raíz):** https://www.lme.com/market-data
- **Emisor:** London Metal Exchange (grupo HKEX)
- **Documentación y notas:** Precios de referencia diarios (LME Official y Closing Prices), informes de almacenes y existencias (lme.com/market-data/reports-and-data/warehouse-and-stocks-reports), volumen e interés abierto; datos en tiempo real, diferidos o históricos vía LMElive, LMEsource y distribuidores con licencia; Benchmark Statement de precios oficiales publicada.
- **Temática:** TF-08 Materias primas y energía (agencias y datos) (principal)
- **Calidad Q:** 82 (A) — Primariedad 18/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 14/15 · Independencia 8/10 · Actualidad 10/10 · Acceso 8/10
- **Tipología:** primaria
- **Acceso:** Parcial (informes públicos; datos detallados y tiempo real con licencia)
- **Ámbitos:** Precios, inventarios y actividad de metales industriales
- **Motivo de inclusión y uso:** Inventarios y estructura de curva de metales básicos.
- **Restricciones de uso:** Licencia de datos de mercado de la LME.
- **Sesgos y cautelas:** Datos detallados de pago; la página no aclara qué conjuntos son gratuitos.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «London Metal Exchange LME official prices stocks warehouse reports»; WebFetch: sí)

#### RF-0353 · Q 80 (A) — Ember — datos de electricidad

- **Canal oficial (URL raíz):** https://ember-energy.org/data/electricity-data-explorer/
- **Emisor:** Ember Energy Research CIC (think tank energético)
- **Documentación y notas:** Generación, capacidad, emisiones y demanda eléctrica de 215 países (anual para 91 países, ~93 % de la demanda; mensual para 88); actualización mensual o quincenal (última vista 30/10/2026); licencia CC BY 4.0.
- **Temática:** TF-08 Materias primas y energía (agencias y datos) (principal) · secundarias: TF-14
- **Calidad Q:** 80 (A) — Primariedad 16/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 13/15 · Independencia 7/10 · Actualidad 10/10 · Acceso 10/10
- **Tipología:** secundaria
- **Acceso:** Abierto (CC BY 4.0)
- **Ámbitos:** Mix eléctrico, emisiones del sector eléctrico, demanda
- **Motivo de inclusión y uso:** Datos mensuales de transición energética (solar, eólica, carbón).
- **Restricciones de uso:** Atribución CC BY 4.0; citar país y mes.
- **Sesgos y cautelas:** Organización con misión de transición (posible sesgo de enfoque).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Ember electricity data explorer»; WebFetch: sí)

#### RF-0064 · Q 77 (B) — World Gold Council

- **Canal oficial (URL raíz):** https://gold.org/goldhub/research/central-banks
- **Emisor:** World Gold Council (WGC)
- **Documentación y notas:** Goldhub: estadísticas mensuales de reservas de oro de bancos centrales (última vista: agosto de 2026), Gold Demand Trends trimestral (último visto: 2T 2026), datos de precios y primas; las notas «Gold Focus» tratan flujos de ETF (gold.org/goldhub/gold-focus/…). Invest.gold para particulares.
- **Temática:** TF-08 Materias primas y energía (agencias y datos) (principal)
- **Calidad Q:** 77 (B) — Primariedad 16/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 14/15 · Independencia 6/10 · Actualidad 9/10 · Acceso 9/10
- **Tipología:** secundaria
- **Acceso:** Abierto (algunas descargas con registro)
- **Ámbitos:** Demanda de oro por segmento; compras de bancos centrales; flujos de ETF
- **Motivo de inclusión y uso:** Datos de demanda y flujos de oro.
- **Restricciones de uso:** Condiciones de Goldhub; citar informe y trimestre.
- **Sesgos y cautelas:** Asociación financiada por mineras (sesgo promocional).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «World Gold Council Gold Demand Trends Goldhub gold ETF flows central banks»; WebFetch: sí)

#### RF-0309 · Q 73 (B) — International Energy Forum (IEF)

- **Canal oficial (URL raíz):** https://www.ief.org/
- **Emisor:** International Energy Forum (IEF)
- **Documentación y notas:** Coordinador de JODI (según jodidata.org) y foro de productores y consumidores; publica materiales sobre JODI (p. ej., FAQ y reuniones de jefes de organizaciones socias en ief.org).
- **Temática:** TF-08 Materias primas y energía (agencias y datos) (principal) · secundarias: TF-14
- **Calidad Q:** 73 (B) — Primariedad 14/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 13/15 · Independencia 9/10 · Actualidad 7/10 · Acceso 8/10
- **Tipología:** secundaria
- **Acceso:** Abierto
- **Ámbitos:** Diálogo productor-consumidor; transparencia de datos energéticos
- **Motivo de inclusión y uso:** Contexto institucional de JODI y comparativas de perspectivas energéticas.
- **Restricciones de uso:** Citar documento y fecha.
- **Sesgos y cautelas:** Foro intergubernamental (lenguaje de consenso); productos de datos vía JODI (RF-0308): no duplicar raíz.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «JODI Oil World Database partner organisations APEC Eurostat GECF IEA OPEC» —ief.org en resultados y en la lista de socios de JODI—; WebFetch al sitio: no)

#### RF-0357 · Q 70 (B) — Our World in Data — energía

- **Canal oficial (URL raíz):** https://ourworldindata.org/grapher/installed-solar-PV-capacity?tab=map
- **Emisor:** Global Change Data Lab (con la Universidad de Oxford)
- **Documentación y notas:** Gráficos y datos reprocesados con atribución explícita a la fuente original (p. ej., IRENA 2026); licencia CC BY 4.0 para lo propio; fecha de actualización y próxima actualización visibles (28/07/2026 y 28/07/2027).
- **Temática:** TF-08 Materias primas y energía (agencias y datos) (principal) · secundarias: TF-13
- **Calidad Q:** 70 (B) — Primariedad 8/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 12/15 · Independencia 9/10 · Actualidad 7/10 · Acceso 10/10
- **Tipología:** terciaria (agregador)
- **Acceso:** Abierto (CC BY 4.0)
- **Ámbitos:** Series energéticas y de emisiones armonizadas
- **Motivo de inclusión y uso:** Acceso rápido y documentado a series de terceros; citar siempre la fuente original.
- **Restricciones de uso:** Citar la fuente original indicada en cada gráfico.
- **Sesgos y cautelas:** No es fuente primaria; actualización anual.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «IRENA Renewable Capacity Statistics 2026»; WebFetch: sí)

#### RF-0310 · Q 69 (B) — Gas Exporting Countries Forum (GECF)

- **Canal oficial (URL raíz):** https://www.gecf.org/
- **Emisor:** Gas Exporting Countries Forum (GECF)
- **Documentación y notas:** Organización socia de JODI (JODI-Gas) según jodidata.org; foro de países exportadores de gas.
- **Temática:** TF-08 Materias primas y energía (agencias y datos) (principal)
- **Calidad Q:** 69 (B) — Primariedad 15/20 · Historial 10/20 · Transparencia 11/15 · Autoridad 12/15 · Independencia 5/10 · Actualidad 8/10 · Acceso 8/10
- **Tipología:** secundaria
- **Acceso:** Abierto (parcial)
- **Ámbitos:** Mercado mundial de gas natural y GNL desde la óptica de los exportadores
- **Motivo de inclusión y uso:** Contraste de la visión de productores de gas frente a IEA/EIA.
- **Restricciones de uso:** Citar publicación y fecha.
- **Sesgos y cautelas:** Parte interesada (exportadores). Publicaciones concretas no leídas: confirmar en el próximo barrido.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «JODI Oil World Database partner organisations APEC Eurostat GECF IEA OPEC»; URL tomada de la página de socios de JODI leída con WebFetch; WebFetch al sitio: no)

#### RF-0311 · Q 69 (B) — OLADE — Organización Latinoamericana de Energía

- **Canal oficial (URL raíz):** https://www.olade.org/
- **Emisor:** Organización Latinoamericana de Energía (OLADE)
- **Documentación y notas:** Organización socia de JODI para América Latina y el Caribe (lista de socios de jodidata.org; olade.org aparece en resultados de búsqueda sobre JODI).
- **Temática:** TF-08 Materias primas y energía (agencias y datos) (principal) · secundarias: TF-01
- **Calidad Q:** 69 (B) — Primariedad 15/20 · Historial 10/20 · Transparencia 11/15 · Autoridad 12/15 · Independencia 8/10 · Actualidad 6/10 · Acceso 7/10
- **Tipología:** secundaria
- **Acceso:** Abierto (parcial)
- **Ámbitos:** Estadística energética regional de América Latina y el Caribe
- **Motivo de inclusión y uso:** Diversidad geográfica en balances energéticos (región relevante para empresas españolas).
- **Restricciones de uso:** Citar publicación y año.
- **Sesgos y cautelas:** Productos concretos no leídos: confirmar en el próximo barrido.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «JODI Oil World Database partner organisations APEC Eurostat GECF IEA OPEC»; WebFetch al sitio: no)

#### RF-0359 · Q 66 (B) — Mysteel — precios e índices de materias primas (acero y otras)

- **Canal oficial (URL raíz):** https://www.mysteel.net/news/5129302-wsa-global-crude-steel-output-declines-15-over-jan-may
- **Emisor:** Mysteel Global Pte. Ltd. (filial internacional de Mysteel, China)
- **Documentación y notas:** Noticias, encuestas, índices y precios diarios de materias primas ferrosas, no ferrosas, energía, química, agricultura y nuevas energías; herramientas MyData; contenido completo con suscripción (prueba de 7 días).
- **Temática:** TF-08 Materias primas y energía (agencias y datos) (principal) · secundarias: TF-07
- **Calidad Q:** 66 (B) — Primariedad 14/20 · Historial 10/20 · Transparencia 9/15 · Autoridad 12/15 · Independencia 6/10 · Actualidad 10/10 · Acceso 5/10
- **Tipología:** secundaria
- **Acceso:** De pago (titulares abiertos)
- **Ámbitos:** Precios y existencias de acero y mineral de hierro en China
- **Motivo de inclusión y uso:** Visión del mercado chino del acero, principal consumidor de mineral de hierro.
- **Restricciones de uso:** Solo contenidos públicos citables.
- **Sesgos y cautelas:** Muro de pago; metodología de índices no leída.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin datos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «worldsteel monthly crude steel production press release»; WebFetch: sí)

## TF-09 Inmobiliario (índices y datos)

#### RF-0313 · Q 89 (A) — FHFA — House Price Index

- **Canal oficial (URL raíz):** https://www.fhfa.gov/taxonomy/term/301
- **Emisor:** Federal Housing Finance Agency (FHFA)
- **Documentación y notas:** Índice de ventas repetidas ponderado de viviendas unifamiliares desde mediados de los setenta (nacional, división censal, estado, metro, condado, código postal, sección censal); informes mensuales (última semana del mes; último visto: 27/10/2026) y trimestrales (finales de feb., may., ago., nov.).
- **Temática:** TF-09 Inmobiliario (índices y datos) (principal) · secundarias: TF-01
- **Calidad Q:** 89 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 15/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 9/10 · Acceso 10/10
- **Tipología:** primaria
- **Acceso:** Abierto (dominio público)
- **Ámbitos:** Precios de vivienda en EE. UU. (hipotecas conformes)
- **Motivo de inclusión y uso:** Índice oficial de precios de vivienda de EE. UU., contraste del Case-Shiller (RF-0071).
- **Restricciones de uso:** Uso libre; citar versión (purchase-only o all-transactions) y periodo.
- **Sesgos y cautelas:** Cobertura limitada a préstamos de Fannie Mae/Freddie Mac; revisiones.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «FHFA House Price Index Freddie Mac Primary Mortgage Market Survey NAHB Housing Market Index NAR existing-home sales»; WebFetch: sí)

#### RF-0360 · Q 89 (A) — U.S. Census Bureau / HUD — New Residential Construction

- **Canal oficial (URL raíz):** https://www.census.gov/construction/nrc/pdf/newresconst_202609.pdf
- **Emisor:** U.S. Census Bureau y U.S. Department of Housing and Urban Development
- **Documentación y notas:** Publicación mensual conjunta (8:30 ET) de viviendas iniciadas, permisos y terminadas: septiembre de 2026, 1.221.000 iniciadas y 1.400.000 permisos (tasa anual desestacionalizada), publicada 20/10/2026; siguiente 18/11/2026.
- **Temática:** TF-09 Inmobiliario (índices y datos) (principal) · secundarias: TF-01
- **Calidad Q:** 89 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 15/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 9/10 · Acceso 10/10
- **Tipología:** primaria
- **Acceso:** Abierto (dominio público)
- **Ámbitos:** Construcción residencial en EE. UU.
- **Motivo de inclusión y uso:** Dato oficial adelantado de la actividad inmobiliaria.
- **Restricciones de uso:** Uso libre; citar mes y revisión.
- **Sesgos y cautelas:** Márgenes de error amplios; revisiones.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Census Bureau New Residential Construction housing starts building permits release»; WebFetch: sí)

#### RF-0070 · Q 88 (A) — BIS — precios de la vivienda residencial

- **Canal oficial (URL raíz):** https://data.bis.org/topics/RPP
- **Emisor:** Bank for International Settlements (BIS)
- **Documentación y notas:** Dos conjuntos: «Selected» (un indicador por país, nominal y real) y «Detailed» (más de 300 series de unos 60 países); series retrotraídas a ~1970 en 23 países. Actualización mensual (última semana): última 29/10/2026, próxima 26/11/2026. Documentación en bis.org/pages/statistics/pp-documentation.pdf; notas de publicación trimestrales.
- **Temática:** TF-09 Inmobiliario (índices y datos) (principal) · secundarias: TF-01
- **Calidad Q:** 88 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 15/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 8/10 · Acceso 10/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** Precios de vivienda por país, series largas
- **Motivo de inclusión y uso:** Base comparada internacional de precios de vivienda.
- **Restricciones de uso:** Uso con atribución; citar conjunto, país y fecha de extracción.
- **Sesgos y cautelas:** Métodos nacionales heterogéneos (usar «Selected» para comparar).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Migración del portal de bis.org/statistics/pp.htm a data.bis.org.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «BIS residential property price statistics data.bis.org»; WebFetch: sí)

#### RF-0072 · Q 88 (A) — INE — Índice de Precios de Vivienda y estadísticas inmobiliarias

- **Canal oficial (URL raíz):** https://www.ine.es/htdocs/prensa/ipv_prensa.htm
- **Emisor:** Instituto Nacional de Estadística (INE)
- **Documentación y notas:** Página de prensa del IPV con último dato y enlace al calendario del INE; metadatos de la operación en ine.es/dynt3/metadatos/es/RespuestaDatos.html?oper=15; metodología 2025 (ine.es/daco/daco42/ipv/metodologia2025.pdf).
- **Temática:** TF-09 Inmobiliario (índices y datos) (principal) · secundarias: TF-01
- **Calidad Q:** 88 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 15/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 8/10 · Acceso 10/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** Precios de vivienda libre (nueva y de segunda mano) en España
- **Motivo de inclusión y uso:** Fuente estadística oficial de España.
- **Restricciones de uso:** Uso libre con atribución; citar trimestre y base.
- **Sesgos y cautelas:** Frecuencia trimestral. En la lectura, la página de prensa mostraba como último dato el 3T 2025 (+12,8 % anual), lo que parece desfasado: confirmar el último dato en INEbase o en el calendario.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Nueva metodología 2025 publicada.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «INE Índice de Precios de Vivienda IPV último dato Registradores Notariado Banco de España indicadores mercado vivienda»; WebFetch: sí)

#### RF-0331 · Q 88 (A) — ONS / HM Land Registry — UK House Price Index

- **Canal oficial (URL raíz):** https://www.ons.gov.uk/releases/ukhousepriceindexnovember2023
- **Emisor:** Office for National Statistics (datos de HM Land Registry, Registers of Scotland y Land and Property Services NI)
- **Documentación y notas:** Índice oficial mensual de precios de vivienda del Reino Unido; boletines en ons.gov.uk/economy/inflationandpriceindices/bulletins/housepriceindex/.
- **Temática:** TF-09 Inmobiliario (índices y datos) (principal) · secundarias: TF-01
- **Calidad Q:** 88 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 15/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 8/10 · Acceso 10/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** Precios de vivienda en el Reino Unido por nación y región
- **Motivo de inclusión y uso:** Fuente oficial británica de precios de vivienda.
- **Restricciones de uso:** Licencia de datos abiertos del Gobierno británico; citar mes.
- **Sesgos y cautelas:** Desfase de dos meses por el registro de transacciones; revisiones.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «HM Land Registry UK House Price Index monthly release gov.uk»; WebFetch: sí)

#### RF-0330 · Q 86 (A) — Federal Reserve Bank of Dallas — International House Price Database

- **Canal oficial (URL raíz):** https://www.dallasfed.org/institute/houseprice
- **Emisor:** Federal Reserve Bank of Dallas (Globalization Institute)
- **Documentación y notas:** Panel trimestral desde 1975 de 26 países (incluida España): índice de precios nominal y real, renta disponible per cápita nominal y real; indicadores de exuberancia (pruebas SADF/GSADF, Pavlidis et al., 2016); última versión 2T 2026 (publicada 09/10/2026).
- **Temática:** TF-09 Inmobiliario (índices y datos) (principal) · secundarias: TF-01
- **Calidad Q:** 86 (A) — Primariedad 18/20 · Historial 10/20 · Transparencia 15/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 8/10 · Acceso 10/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** Precios reales de vivienda y ratio precio/renta comparados; detección de burbujas
- **Motivo de inclusión y uso:** Base homogénea para valoración relativa de la vivienda y señales de exuberancia.
- **Restricciones de uso:** Uso con atribución; citar versión trimestral.
- **Sesgos y cautelas:** Algunos datos recientes son previsiones que se sustituyen en revisiones posteriores.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Dallas Fed International House Price Database»; WebFetch: sí)

#### RF-0327 · Q 85 (A) — Freddie Mac — Primary Mortgage Market Survey (PMMS)

- **Canal oficial (URL raíz):** https://freddiemac.gcs-web.com/node/32031/pdf
- **Emisor:** Freddie Mac
- **Documentación y notas:** Encuesta semanal de tipos hipotecarios (prestamistas encuestados de lunes a miércoles; publicación los jueves a las 10:00 ET). Nota leída: 03/09/2026 (30 años 6,71 %; 15 años 6,04 %). Según Mortgage News Daily, el 29/10/2026 el tipo a 30 años era del 7,24 %.
- **Temática:** TF-09 Inmobiliario (índices y datos) (principal) · secundarias: TF-01
- **Calidad Q:** 85 (A) — Primariedad 19/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 15/15 · Independencia 8/10 · Actualidad 10/10 · Acceso 10/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** Tipos hipotecarios fijos a 30 y 15 años en EE. UU.
- **Motivo de inclusión y uso:** Coste de financiación de la vivienda; insumo de asequibilidad.
- **Restricciones de uso:** Citar semana y plazo.
- **Sesgos y cautelas:** Tipos de préstamos conformes de primera calidad; entidad patrocinada por el Gobierno.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Freddie Mac Primary Mortgage Market Survey weekly mortgage rates»; WebFetch: sí)

#### RF-0314 · Q 83 (A) — Consejo General del Notariado — Portal Estadístico del Notariado

- **Canal oficial (URL raíz):** https://www.penotariado.com/
- **Emisor:** Consejo General del Notariado (desarrollado por CTNotariado)
- **Documentación y notas:** Portal gratuito con precios reales de compraventa (€/m²) a partir de escrituras anonimizadas, por comunidad, provincia, municipio y código postal; número de compraventas, tipo de vivienda, edad y nacionalidad de compradores, esfuerzo en años de renta; histórico de 12 años; actualización mensual. Lanzado el 23/10/2025 (según Vozpópuli, 28/10/2026).
- **Temática:** TF-09 Inmobiliario (índices y datos) (principal)
- **Calidad Q:** 83 (A) — Primariedad 19/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 14/15 · Independencia 9/10 · Actualidad 9/10 · Acceso 10/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** Precios de transacción y compraventas de vivienda en España, con granularidad local
- **Motivo de inclusión y uso:** Precios efectivos de escritura (no tasación ni oferta) para contrastar INE, tasadoras y portales.
- **Restricciones de uso:** Citar ámbito geográfico y mes.
- **Sesgos y cautelas:** Fuente colegial; URL obtenida de prensa: confirmar en el próximo barrido.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Portal nuevo (2025).
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Estadística Registral Inmobiliaria Registradores portal estadístico Notariado Tinsa IMIE valor tasado vivienda Ministerio»; URL tomada del artículo de Vozpópuli leído con WebFetch; WebFetch al sitio: no)

#### RF-0328 · Q 81 (A) — NAHB/Wells Fargo — Housing Market Index (HMI)

- **Canal oficial (URL raíz):** https://www.nahb.org/hmi
- **Emisor:** National Association of Home Builders (con Wells Fargo)
- **Documentación y notas:** Confianza de los constructores de vivienda unifamiliar (0–100) con ventas actuales (peso 0,5920), ventas esperadas (0,1358) y visitas de compradores (0,2722); mensual; octubre de 2026: 29 (−3), con el 43 % de constructores rebajando precios.
- **Temática:** TF-09 Inmobiliario (índices y datos) (principal) · secundarias: —
- **Calidad Q:** 81 (A) — Primariedad 17/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 13/15 · Independencia 7/10 · Actualidad 10/10 · Acceso 10/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** Confianza y condiciones del mercado de vivienda nueva en EE. UU.
- **Motivo de inclusión y uso:** Indicador adelantado de construcción residencial.
- **Restricciones de uso:** Citar mes y componente.
- **Sesgos y cautelas:** Asociación sectorial; encuesta de opinión.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Panel renovado anualmente.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «NAHB Wells Fargo Housing Market Index builder confidence»; WebFetch: sí)

#### RF-0071 · Q 80 (A) — S&P Cotality Case-Shiller Home Price Indices (antes S&P CoreLogic Case-Shiller)

- **Canal oficial (URL raíz):** https://www.spglobal.com/spdji/en/index-announcements/article/sp-cotality-case-shiller-index-reports-annual-gain-in-august-2026/
- **Emisor:** S&P Dow Jones Indices (con Cotality, antes CoreLogic)
- **Documentación y notas:** Anuncios mensuales «S&P Cotality Case-Shiller Index Reports…» en spglobal.com/spdji/en/index-announcements/ (último visto en resultados: datos de agosto de 2026). Series en FRED: CSUSHPINSA y CSUSHPISA.
- **Temática:** TF-09 Inmobiliario (índices y datos) (principal)
- **Calidad Q:** 80 (A) — Primariedad 18/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 14/15 · Independencia 8/10 · Actualidad 8/10 · Acceso 8/10
- **Tipología:** primaria
- **Acceso:** Abierto (parcial)
- **Ámbitos:** Precios de vivienda en EE. UU. por ventas repetidas (nacional, 20 y 10 ciudades)
- **Motivo de inclusión y uso:** Índice de referencia de vivienda en EE. UU.
- **Restricciones de uso:** Condiciones de S&P DJI; citar mes de datos y serie (SA/NSA).
- **Sesgos y cautelas:** Desfase de dos meses.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Cambio de nombre: CoreLogic → Cotality (el índice pasa a «S&P Cotality Case-Shiller»).
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «S&P Cotality Case-Shiller U.S. National Home Price NSA Index»; WebFetch: intentado, error del sitio)

#### RF-0363 · Q 80 (A) — RICS — UK Residential Market Survey

- **Canal oficial (URL raíz):** https://www.rics.org/news-insights/uk-residential-survey-may-2026
- **Emisor:** Royal Institution of Chartered Surveyors (RICS)
- **Documentación y notas:** Encuesta mensual a tasadores con balances netos de precios, consultas de compradores, ventas y expectativas; mayo de 2026: balance de precios −35 % y nuevas consultas −34 %. PDF mensuales en rics.org/content/dam/ricsglobal/documents/market-surveys/.
- **Temática:** TF-09 Inmobiliario (índices y datos) (principal) · secundarias: —
- **Calidad Q:** 80 (A) — Primariedad 16/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 14/15 · Independencia 8/10 · Actualidad 10/10 · Acceso 10/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** Sentimiento y condiciones del mercado de vivienda británico
- **Motivo de inclusión y uso:** Indicador adelantado de precios de vivienda del Reino Unido.
- **Restricciones de uso:** Citar mes y balance.
- **Sesgos y cautelas:** Encuesta de opinión; organismo profesional.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «RICS UK Residential Market Survey»; WebFetch: sí)

#### RF-0068 · Q 79 (B) — Nareit

- **Canal oficial (URL raíz):** https://reit.com/data-research/reit-indexes/real-time-index-returns
- **Emisor:** National Association of Real Estate Investment Trusts (Nareit)
- **Documentación y notas:** Rentabilidades en tiempo real de la serie FTSE Nareit U.S. Real Estate (total y por sector: industrial, oficinas, comercial, residencial, salud, centros de datos, hipotecarios) y del FTSE EPRA Nareit Global Real Estate Index (por región).
- **Temática:** TF-09 Inmobiliario (índices y datos) (principal)
- **Calidad Q:** 79 (B) — Primariedad 17/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 14/15 · Independencia 7/10 · Actualidad 8/10 · Acceso 9/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** Rentabilidades, valoraciones y datos de REIT estadounidenses
- **Motivo de inclusión y uso:** Datos sectoriales del inmobiliario cotizado de EE. UU.
- **Restricciones de uso:** Citar índice y fecha/hora.
- **Sesgos y cautelas:** Asociación sectorial (sesgo promocional); marcas de tiempo distintas entre índices.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «FTSE EPRA Nareit Global Real Estate Index Series EPRA Nareit REIT data»; WebFetch: sí)

#### RF-0361 · Q 77 (B) — National Association of Realtors — Existing-Home Sales

- **Canal oficial (URL raíz):** https://nar.realtor/node/156145
- **Emisor:** National Association of Realtors (NAR)
- **Documentación y notas:** Encuesta mensual de ventas de vivienda usada a partir de datos de asociaciones locales y MLS (los datos recibidos antes del día 15 entran en la publicación principal); calendario de publicaciones estadísticas de NAR. La página leída es la de ampliación de la encuesta, no una nota de cifras.
- **Temática:** TF-09 Inmobiliario (índices y datos) (principal) · secundarias: —
- **Calidad Q:** 77 (B) — Primariedad 18/20 · Historial 10/20 · Transparencia 11/15 · Autoridad 14/15 · Independencia 6/10 · Actualidad 9/10 · Acceso 9/10
- **Tipología:** primaria
- **Acceso:** Abierto (titulares)
- **Ámbitos:** Ventas, precio mediano e inventario de vivienda usada en EE. UU.
- **Motivo de inclusión y uso:** Indicador mensual del mercado de reventa (aprox. 90 % de las transacciones).
- **Restricciones de uso:** Citar mes y revisión.
- **Sesgos y cautelas:** Asociación de agentes (sesgo promocional); revisiones de referencia.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «NAR existing-home sales monthly report National Association of Realtors»; WebFetch: sí)

#### RF-0069 · Q 76 (B) — EPRA

- **Canal oficial (URL raíz):** https://epra.com/indexes/index-data
- **Emisor:** European Public Real Estate Association (EPRA)
- **Documentación y notas:** Panel de datos del índice global (capitalización, rentabilidades, sectores, constituyentes) **solo para miembros de pleno derecho**; informes mensuales en la sección Research; boletines estadísticos mensuales históricos (prodapp.epra.com/media/…). Metodología del índice en LSEG (ftse-epra-nareit-global-real-estate-index-series-methodology-overview.pdf).
- **Temática:** TF-09 Inmobiliario (índices y datos) (principal)
- **Calidad Q:** 76 (B) — Primariedad 17/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 14/15 · Independencia 7/10 · Actualidad 8/10 · Acceso 6/10
- **Tipología:** primaria
- **Acceso:** Restringido (datos de índice para miembros); informes públicos parciales
- **Ámbitos:** Índices FTSE EPRA Nareit, NAV, mejores prácticas contables (EPRA NTA)
- **Motivo de inclusión y uso:** Inmobiliario cotizado europeo y métricas estándar.
- **Restricciones de uso:** Solo contenidos públicos citables.
- **Sesgos y cautelas:** Asociación sectorial; Acceso rebajado de 9 a 6 por la restricción a miembros (Q provisional 79 → 76).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «FTSE EPRA Nareit Global Real Estate Index Series EPRA Nareit REIT data»; WebFetch: sí)

#### RF-0329 · Q 76 (B) — Colegio de Registradores — Estadística Registral Inmobiliaria (ERI)

- **Canal oficial (URL raíz):** https://datos.gob.es/es/catalogo/a16003011-estadistica-registral-inmobiliaria-20221
- **Emisor:** Colegio de Registradores de la Propiedad y Mercantiles de España (estadística ERI; ficha en el catálogo nacional datos.gob.es)
- **Documentación y notas:** La ERI figura en el catálogo de datos abiertos datos.gob.es con ediciones anuales (2020, 2022, 2025); Euskadi publica una estadística registral derivada con metodología propia. Precios, compraventas e hipotecas según inscripciones registrales.
- **Temática:** TF-09 Inmobiliario (índices y datos) (principal) · secundarias: —
- **Calidad Q:** 76 (B) — Primariedad 18/20 · Historial 10/20 · Transparencia 11/15 · Autoridad 14/15 · Independencia 8/10 · Actualidad 7/10 · Acceso 8/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** Compraventas, precios e hipotecas de vivienda en España por inscripción registral
- **Motivo de inclusión y uso:** Contraste registral de los precios notariales (RF-0314) y del INE (RF-0072).
- **Restricciones de uso:** Citar edición y trimestre.
- **Sesgos y cautelas:** Editor de la ficha del catálogo no leído (la página dio error): confirmar en el próximo barrido.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Colegio de Registradores Estadística Registral Inmobiliaria ERI trimestral»; WebFetch: intentado, error del sitio)

#### RF-0332 · Q 76 (B) — Zillow Research — datos de vivienda (ZHVI, ZORI)

- **Canal oficial (URL raíz):** https://www.zillow.com/research/data/
- **Emisor:** Zillow Group (Zillow Research)
- **Documentación y notas:** Descargas CSV gratuitas: ZHVI (valor típico, percentiles 35–65), ZORI (alquiler observado de repetición), previsiones, inventario, ventas, días en mercado, rebajas, Market Heat Index, obra nueva y asequibilidad; metodologías publicadas (neural ZHVI, ZORI); calendario de publicación.
- **Temática:** TF-09 Inmobiliario (índices y datos) (principal) · secundarias: —
- **Calidad Q:** 76 (B) — Primariedad 15/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 12/15 · Independencia 7/10 · Actualidad 10/10 · Acceso 9/10
- **Tipología:** secundaria
- **Acceso:** Abierto (licencia no declarada en la página)
- **Ámbitos:** Valores y alquileres de vivienda en EE. UU. con gran detalle geográfico
- **Motivo de inclusión y uso:** Alquileres y precios de alta frecuencia (útil para la inflación de vivienda).
- **Restricciones de uso:** Citar serie y fecha de descarga; seguir la guía de cita de ZHVI.
- **Sesgos y cautelas:** Modelo propio (valoración automática); portal inmobiliario comercial.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Cambios de metodología documentados (p. ej., obra nueva desde 08/2025).
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Zillow Research data ZHVI ZORI home value rent index»; WebFetch: sí)

#### RF-0312 · Q 75 (B) — Tinsa — IMIE (Mercados Locales y General)

- **Canal oficial (URL raíz):** https://www.tinsa.es/informes/imie-mercados-locales/imie-mercados-locales-1o-trimestre-2026-143/
- **Emisor:** Tinsa (sociedad de tasación)
- **Documentación y notas:** Valor unitario (€/m²) de vivienda libre terminada a partir de tasaciones hipotecarias (base de más de 6 millones de valoraciones, más del 25 % de las tasaciones anuales en España), por CCAA, provincia, capital, municipio y distritos de grandes ciudades; trimestral. 1T 2026: +14,3 % anual nominal (+11,8 % real). Metodología: medias móviles ponderadas estratificadas con tasaciones según normativa del Banco de España.
- **Temática:** TF-09 Inmobiliario (índices y datos) (principal)
- **Calidad Q:** 75 (B) — Primariedad 16/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 12/15 · Independencia 7/10 · Actualidad 9/10 · Acceso 9/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** Valor de tasación de vivienda en España con detalle local
- **Motivo de inclusión y uso:** Indicador de tasación con mayor granularidad y menor desfase que el IPV.
- **Restricciones de uso:** Citar edición y trimestre.
- **Sesgos y cautelas:** Valor de tasación (no precio de transacción); empresa privada.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Estadística Registral Inmobiliaria Registradores portal estadístico Notariado Tinsa IMIE valor tasado vivienda Ministerio»; WebFetch: sí)

#### RF-0364 · Q 72 (B) — Calculated Risk — blog de vivienda y economía (Bill McBride)

- **Canal oficial (URL raíz):** https://www.calculatedriskblog.com/2018/07/chemical-activity-barometer-increased.html
- **Emisor:** Bill McBride (Calculated Risk)
- **Documentación y notas:** Blog con seguimiento diario de datos de vivienda y economía de EE. UU., gráficos propios y enlaces a la fuente primaria (p. ej., notas del ACC).
- **Temática:** TF-09 Inmobiliario (índices y datos) (principal) · secundarias: TF-12
- **Calidad Q:** 72 (B) — Primariedad 9/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 12/15 · Independencia 9/10 · Actualidad 10/10 · Acceso 10/10
- **Tipología:** secundaria
- **Acceso:** Abierto
- **Ámbitos:** Vivienda, hipotecas y ciclo económico de EE. UU.
- **Motivo de inclusión y uso:** Pista de descubrimiento y lectura experta del dato inmobiliario; los hechos se citan en la fuente primaria que enlaza.
- **Restricciones de uso:** Opinión: citar la fuente primaria.
- **Sesgos y cautelas:** Un solo autor.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin datos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «American Chemistry Council Chemical Activity Barometer»; WebFetch: sí)

#### RF-0362 · Q 69 (B) — idealista — informes de precios de vivienda

- **Canal oficial (URL raíz):** https://www.idealista.com/news/estadisticas/
- **Emisor:** idealista
- **Documentación y notas:** Informes de evolución del precio de la vivienda en venta y alquiler por comunidad, provincia, municipio y barrio; indicadores de demanda (diferencia entre precio anunciado y ofertas) y euríbor; idealista aparece como caso de éxito en datos.gob.es.
- **Temática:** TF-09 Inmobiliario (índices y datos) (principal) · secundarias: —
- **Calidad Q:** 69 (B) — Primariedad 13/20 · Historial 10/20 · Transparencia 9/15 · Autoridad 11/15 · Independencia 6/10 · Actualidad 10/10 · Acceso 10/10
- **Tipología:** secundaria
- **Acceso:** Abierto
- **Ámbitos:** Precios de oferta de venta y alquiler en España
- **Motivo de inclusión y uso:** Indicador adelantado y granular (precios de oferta, no de cierre).
- **Restricciones de uso:** Citar informe y mes; contrastar con RF-0314 y RF-0072.
- **Sesgos y cautelas:** Precios de anuncio, no de transacción; portal comercial; metodología no leída.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «idealista informe precio vivienda venta índice mensual»; WebFetch: sí)

#### RF-0333 · Q 66 (B) — Mortgage News Daily — índice diario de tipos hipotecarios

- **Canal oficial (URL raíz):** https://www.mortgagenewsdaily.com/mortgage-rates/freddie-mac
- **Emisor:** Mortgage News Daily, LLC
- **Documentación y notas:** Índice diario propio de tipos (30 años: 7,27 % a 30/10/2026) y reproducción del PMMS de Freddie Mac; existe una página sobre el índice diario, pero su metodología no se leyó.
- **Temática:** TF-09 Inmobiliario (índices y datos) (principal) · secundarias: TF-03
- **Calidad Q:** 66 (B) — Primariedad 12/20 · Historial 10/20 · Transparencia 8/15 · Autoridad 10/15 · Independencia 7/10 · Actualidad 10/10 · Acceso 9/10
- **Tipología:** secundaria
- **Acceso:** Abierto
- **Ámbitos:** Tipos hipotecarios diarios en EE. UU.
- **Motivo de inclusión y uso:** Alta frecuencia entre publicaciones semanales del PMMS (RF-0327).
- **Restricciones de uso:** Citar fecha; contrastar con RF-0327.
- **Sesgos y cautelas:** Metodología no leída; medio comercial.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin datos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Freddie Mac Primary Mortgage Market Survey weekly mortgage rates»; WebFetch: sí)

## TF-10 Cripto: datos en cadena, investigación y noticias

#### RF-0338 · Q 83 (A) — CCAF — Cambridge Bitcoin Electricity Consumption Index (CBECI)

- **Canal oficial (URL raíz):** https://cbeci.org/
- **Emisor:** Cambridge Centre for Alternative Finance (Cambridge Judge Business School)
- **Documentación y notas:** Índice en tiempo real del consumo eléctrico anual de la red Bitcoin (modelo ascendente con eficiencia de más de 60 equipos de minería), lanzado el 02/07/2019. URL cbeci.org confirmada en la página de la Judge Business School (jbs.cam.ac.uk/insight/2019/cambridge-bitcoin-electricity-consumption-index-cbeci/) y en Decrypt.
- **Temática:** TF-10 Cripto: datos en cadena, investigación y noticias (principal) · secundarias: TF-13
- **Calidad Q:** 83 (A) — Primariedad 16/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 8/10 · Acceso 10/10
- **Tipología:** secundaria
- **Acceso:** Abierto
- **Ámbitos:** Consumo energético y geografía de la minería de bitcoin
- **Motivo de inclusión y uso:** Fuente académica de referencia para el impacto energético (riesgo ESG y regulatorio).
- **Restricciones de uso:** Citar estimación (central/rango) y fecha.
- **Sesgos y cautelas:** Estimación de modelo con rango amplio.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Cambridge Bitcoin Electricity Consumption Index CCAF»; URL tomada de la página de la Judge Business School leída con WebFetch; WebFetch al sitio: no)

#### RF-0076 · Q 82 (A) — DefiLlama

- **Canal oficial (URL raíz):** https://defillama.com/
- **Emisor:** DefiLlama (proyecto abierto)
- **Documentación y notas:** Secciones de visión de mercado (cadenas, protocolos, TVL puenteado), stablecoins, comisiones e ingresos (por protocolo y cadena), rendimientos; enlaces «Data Definitions» y «Report Incorrect Data».
- **Temática:** TF-10 Cripto: datos en cadena, investigación y noticias (principal)
- **Calidad Q:** 82 (A) — Primariedad 18/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 12/15 · Independencia 9/10 · Actualidad 10/10 · Acceso 10/10
- **Tipología:** terciaria
- **Acceso:** Abierto
- **Ámbitos:** Valor total bloqueado (TVL), ingresos de protocolos, stablecoins, rendimientos
- **Motivo de inclusión y uso:** Datos agregados de DeFi.
- **Restricciones de uso:** Citar métrica, protocolo/cadena y fecha.
- **Sesgos y cautelas:** TVL con doble cómputo; datos autodeclarados por protocolos; la página leída no incluía declaración de código abierto (comprobar).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «DefiLlama DeFi TVL dashboard stablecoins fees revenue»; WebFetch: sí, defillama.com/revenue/chain/vaulta)

#### RF-0074 · Q 80 (A) — Coin Metrics

- **Canal oficial (URL raíz):** https://docs.coinmetrics.io/network-data
- **Emisor:** Coin Metrics (sus productos Pro se comercializan bajo Talos, según talos.com)
- **Documentación y notas:** Documentación de datos en cadena (metodologías, disponibilidad, glosario); paquete Community (docs.coinmetrics.io/packages/coin-metrics-community-data); boletín «State of the Network» (coinmetrics.substack.com). Aviso de 28/10/2025: retirada de parte de métricas Community; siguen gratis Research Asset Metrics, Reference Rates y Atlas (con restricciones).
- **Temática:** TF-10 Cripto: datos en cadena, investigación y noticias (principal) · secundarias: TF-13
- **Calidad Q:** 80 (A) — Primariedad 17/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 13/15 · Independencia 9/10 · Actualidad 10/10 · Acceso 7/10
- **Tipología:** secundaria
- **Acceso:** Freemium (Community reducida desde 2025)
- **Ámbitos:** Datos en cadena y de mercado con documentación metodológica
- **Motivo de inclusión y uso:** Métricas en cadena con metodología documentada.
- **Restricciones de uso:** Licencia Community para datos gratuitos.
- **Sesgos y cautelas:** Cobertura gratuita recortada (Acceso 8 → 7; Q 81 → 80).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Integración comercial con Talos (la nota no detalla la operación): vigilar.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Coin Metrics State of the Network Community network data»; WebFetch: sí)

#### RF-0337 · Q 80 (A) — L2BEAT — análisis de redes de capa 2 de Ethereum

- **Canal oficial (URL raíz):** https://www.l2beat.com/scaling/tvs
- **Emisor:** L2BEAT
- **Documentación y notas:** Valor total asegurado (TVS) de rollups de Ethereum con desglose (puenteado canónico, nativo, externo); vistas de riesgo (l2beat.com/?view=risk). Instantánea leída: 33.260 M$ a 04/02/2026 (Arbitrum One, Base, OP Mainnet en cabeza).
- **Temática:** TF-10 Cripto: datos en cadena, investigación y noticias (principal) · secundarias: —
- **Calidad Q:** 80 (A) — Primariedad 16/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 12/15 · Independencia 9/10 · Actualidad 10/10 · Acceso 10/10
- **Tipología:** secundaria
- **Acceso:** Abierto
- **Ámbitos:** Capa 2 de Ethereum: valor asegurado, riesgos y fases
- **Motivo de inclusión y uso:** Evaluación independiente de riesgos y adopción de redes de capa 2.
- **Restricciones de uso:** Citar proyecto, métrica y fecha.
- **Sesgos y cautelas:** La página leída no describe el operador ni la metodología completa.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Cambio de métrica TVL → TVS.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «L2BEAT layer 2 rollups risk analysis value secured»; WebFetch: sí)

#### RF-0341 · Q 79 (B) — mempool.space — explorador de la red Bitcoin

- **Canal oficial (URL raíz):** https://mempool.space
- **Emisor:** mempool.space (proyecto de código abierto)
- **Documentación y notas:** Explorador de bloques y del mempool para estimar comisiones y congestión; URL confirmada en el glosario de River (river.com/learn/terms/m/mempool-explorer/), que cita también Blockstream (blockstream.info) y el explorador de Jochen Hoenicke.
- **Temática:** TF-10 Cripto: datos en cadena, investigación y noticias (principal) · secundarias: —
- **Calidad Q:** 79 (B) — Primariedad 18/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 10/15 · Independencia 9/10 · Actualidad 10/10 · Acceso 10/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** Comisiones, mempool, bloques y hashrate de Bitcoin
- **Motivo de inclusión y uso:** Dato directo de la cadena para congestión y demanda de espacio de bloque.
- **Restricciones de uso:** Citar bloque/fecha.
- **Sesgos y cautelas:** Instancia pública de un proyecto comunitario; datos en tiempo real sin archivo oficial.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «mempool.space bitcoin explorer fees mempool»; URL tomada del glosario de River leído con WebFetch; WebFetch al sitio: no)

#### RF-0365 · Q 78 (B) — Etherscan — explorador de Ethereum

- **Canal oficial (URL raíz):** https://etherscan.io/charts
- **Emisor:** Etherscan
- **Documentación y notas:** Explorador de bloques y gráficos y estadísticas de Ethereum (y más de 60 cadenas EVM con una sola clave de API); documentación en docs.etherscan.io.
- **Temática:** TF-10 Cripto: datos en cadena, investigación y noticias (principal) · secundarias: —
- **Calidad Q:** 78 (B) — Primariedad 18/20 · Historial 10/20 · Transparencia 11/15 · Autoridad 12/15 · Independencia 8/10 · Actualidad 10/10 · Acceso 9/10
- **Tipología:** primaria
- **Acceso:** Abierto; API con niveles
- **Ámbitos:** Transacciones, comisiones, contratos y estadísticas de Ethereum
- **Motivo de inclusión y uso:** Verificación directa en cadena de transacciones y métricas de Ethereum.
- **Restricciones de uso:** Condiciones de Etherscan; citar transacción o gráfico y fecha.
- **Sesgos y cautelas:** Etiquetas de direcciones propias; empresa privada.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Etherscan Ethereum blockchain explorer charts statistics»; WebFetch: sí, documentación)

#### RF-0334 · Q 77 (B) — CoinGecko — precios y capitalización de criptoactivos

- **Canal oficial (URL raíz):** https://www2.coingecko.com/en/methodology
- **Emisor:** CoinGecko
- **Documentación y notas:** Metodología publicada: índice de precio de BTC por VWAP, eliminación de valores atípicos, capitalización = precio × oferta circulante verificada; Trust Score de exchanges (liquidez, regulación, ciberseguridad, prueba de reservas; actualización «Basilisk» de mayo de 2026); cambios de metodología aprobados en un foro de gobernanza; sin cobro por listar.
- **Temática:** TF-10 Cripto: datos en cadena, investigación y noticias (principal) · secundarias: —
- **Calidad Q:** 77 (B) — Primariedad 14/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 12/15 · Independencia 8/10 · Actualidad 10/10 · Acceso 9/10
- **Tipología:** terciaria (agregador)
- **Acceso:** Abierto; API con niveles de pago
- **Ámbitos:** Precios, capitalización y volumen de criptoactivos y exchanges
- **Motivo de inclusión y uso:** Agregador de precios con metodología transparente.
- **Restricciones de uso:** Condiciones de CoinGecko; citar activo, métrica y hora.
- **Sesgos y cautelas:** Volúmenes de exchanges con posibles lavados; oferta circulante declarada por los proyectos.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Trust Score revisado en 2026.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «CoinGecko methodology cryptocurrency market capitalization»; WebFetch: sí)

#### RF-0315 · Q 76 (B) — Dune

- **Canal oficial (URL raíz):** https://docs.dune.com/data-catalog/overview
- **Emisor:** Dune Analytics
- **Documentación y notas:** Catálogo de datos brutos, decodificados y curados de más de 100 cadenas (EVM y Solana con decodificación; Bitcoin y otras con datos brutos); consultas SQL, API de datos, Datashare (Snowflake, BigQuery, Databricks); conjuntos públicos en todos los planes y conjuntos premium (stablecoins, RWA, etc.) con derecho de acceso.
- **Temática:** TF-10 Cripto: datos en cadena, investigación y noticias (principal)
- **Calidad Q:** 76 (B) — Primariedad 17/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 11/15 · Independencia 8/10 · Actualidad 10/10 · Acceso 8/10
- **Tipología:** secundaria
- **Acceso:** Freemium
- **Ámbitos:** Datos en cadena consultables por SQL; paneles comunitarios
- **Motivo de inclusión y uso:** Verificación directa de métricas en cadena (consultas reproducibles) frente a cifras de terceros.
- **Restricciones de uso:** Citar consulta/panel (ID) y fecha; los paneles de terceros heredan la calidad de su autor.
- **Sesgos y cautelas:** Paneles comunitarios sin revisión; etiquetas de direcciones heurísticas.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «mempool.space Etherscan Dune Analytics Token Terminal CoinGecko L2BEAT on-chain data sources»; WebFetch: sí)

#### RF-0367 · Q 76 (B) — Kaiko — datos e investigación de mercado cripto

- **Canal oficial (URL raíz):** https://www.kaiko.com/use-cases/research
- **Emisor:** Kaiko
- **Documentación y notas:** Datos de mercado (nivel 1 y 2, CeFi y DeFi, contado y derivados), Market Explorer (volumen y profundidad), tipos de referencia administrados según los principios IOSCO; cuenta de investigación gratuita.
- **Temática:** TF-10 Cripto: datos en cadena, investigación y noticias (principal) · secundarias: TF-06
- **Calidad Q:** 76 (B) — Primariedad 16/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 13/15 · Independencia 8/10 · Actualidad 10/10 · Acceso 7/10
- **Tipología:** secundaria
- **Acceso:** Freemium (investigación gratuita; datos de pago)
- **Ámbitos:** Liquidez, profundidad de libro y volúmenes de exchanges
- **Motivo de inclusión y uso:** Calidad de mercado y liquidez de criptoactivos.
- **Restricciones de uso:** Condiciones de Kaiko.
- **Sesgos y cautelas:** Proveedor comercial; datos detallados de pago.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Kaiko Research crypto market liquidity data»; WebFetch: sí)

#### RF-0073 · Q 74 (B) — Glassnode

- **Canal oficial (URL raíz):** https://docs.glassnode.com/
- **Emisor:** Glassnode AG
- **Documentación y notas:** Documentación oficial con catálogo de métricas y acceso a Glassnode Studio (studio.glassnode.com); suscripciones de pago referidas en el FAQ.
- **Temática:** TF-10 Cripto: datos en cadena, investigación y noticias (principal)
- **Calidad Q:** 74 (B) — Primariedad 16/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 12/15 · Independencia 8/10 · Actualidad 10/10 · Acceso 6/10
- **Tipología:** secundaria
- **Acceso:** Freemium (métricas avanzadas de pago)
- **Ámbitos:** Métricas en cadena de Bitcoin y Ethereum (MVRV, SOPR, flujos a plataformas)
- **Motivo de inclusión y uso:** Métricas en cadena de referencia para PERF-CHR.
- **Restricciones de uso:** Condiciones de Glassnode.
- **Sesgos y cautelas:** Metodologías propietarias (la página de inicio de la documentación no explica cálculos); heurísticas de etiquetado de direcciones.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Glassnode Coin Metrics Messari DefiLlama The Block crypto data»; WebFetch: sí)

#### RF-0077 · Q 70 (B) — Messari

- **Canal oficial (URL raíz):** https://docs.messari.io/docs/research
- **Emisor:** Messari Inc.
- **Documentación y notas:** Research Reports, Protocol Reporting (en colaboración directa con los protocolos), Diligence Reports; boletín y pódcast «Unqualified Opinions»; niveles Free, Pro y Enterprise (Pro accede a informes Enterprise 90 días después). Informe anual «Crypto Theses».
- **Temática:** TF-10 Cripto: datos en cadena, investigación y noticias (principal)
- **Calidad Q:** 70 (B) — Primariedad 14/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 12/15 · Independencia 7/10 · Actualidad 9/10 · Acceso 6/10
- **Tipología:** secundaria
- **Acceso:** Freemium
- **Ámbitos:** Informes de protocolos y activos digitales; tesis anuales
- **Motivo de inclusión y uso:** Investigación estructurada del sector cripto.
- **Restricciones de uso:** Solo contenidos públicos citables.
- **Sesgos y cautelas:** Protocol Reporting en asociación con los propios protocolos (posible conflicto de interés; la página no detalla la financiación).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Messari crypto research reports Crypto Theses»; WebFetch: sí)

#### RF-0335 · Q 70 (B) — Farside Investors — flujos diarios de ETF de bitcoin y ether

- **Canal oficial (URL raíz):** https://farside.co.uk/?p=997
- **Emisor:** Farside Investors
- **Documentación y notas:** Tablas diarias de flujos netos (millones de dólares) por ETF al contado de bitcoin (IBIT, FBTC, GBTC…) y de ether (farside.co.uk/?p=1518); generadas automáticamente a partir de webs de emisores y proveedores de datos; advierte que prioriza rapidez sobre exactitud y que contiene estimaciones.
- **Temática:** TF-10 Cripto: datos en cadena, investigación y noticias (principal) · secundarias: TF-06
- **Calidad Q:** 70 (B) — Primariedad 14/20 · Historial 10/20 · Transparencia 9/15 · Autoridad 10/15 · Independencia 7/10 · Actualidad 10/10 · Acceso 10/10
- **Tipología:** secundaria
- **Acceso:** Abierto
- **Ámbitos:** Flujos de ETF de criptoactivos en EE. UU.
- **Motivo de inclusión y uso:** Medida diaria de demanda institucional de criptoactivos; muy citada por la prensa.
- **Restricciones de uso:** Citar fecha y ETF; contrastar con datos de emisores.
- **Sesgos y cautelas:** Estimaciones con errores declarados; gestora con producto propio.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin datos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Farside Investors bitcoin ETF flow data»; WebFetch: sí)

#### RF-0336 · Q 70 (B) — CoinShares — Digital Asset Fund Flows (semanal)

- **Canal oficial (URL raíz):** https://coinshares.com/us/insights/research-data/fund-flows-18-03-24
- **Emisor:** CoinShares (investigación: James Butterfill)
- **Documentación y notas:** Informe semanal de flujos de ETP de activos digitales por proveedor, país de cotización y activo (bitcoin, ether, Solana, cortos, acciones blockchain), volumen negociado y flujos sobre patrimonio; sin metodología ni fuentes detalladas en la página.
- **Temática:** TF-10 Cripto: datos en cadena, investigación y noticias (principal) · secundarias: TF-06
- **Calidad Q:** 70 (B) — Primariedad 14/20 · Historial 10/20 · Transparencia 9/15 · Autoridad 12/15 · Independencia 6/10 · Actualidad 10/10 · Acceso 9/10
- **Tipología:** secundaria
- **Acceso:** Abierto
- **Ámbitos:** Flujos semanales de productos cotizados de criptoactivos a escala mundial
- **Motivo de inclusión y uso:** Serie semanal global de flujos (incluye Europa), complemento de RF-0335.
- **Restricciones de uso:** Citar semana; aviso legal del emisor.
- **Sesgos y cautelas:** Emisor de ETP (conflicto de interés); metodología no publicada.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «CoinShares Digital Asset Fund Flows Weekly Report»; WebFetch: sí)

#### RF-0075 · Q 67 (B) — The Block

- **Canal oficial (URL raíz):** https://www.theblock.co/
- **Emisor:** The Block
- **Documentación y notas:** Noticias, investigación y panel de datos gratuito (lanzado en 2020 con más de 70 gráficos: en cadena, mercados, finanzas abiertas, métricas alternativas; fuentes declaradas: Coin Metrics, Chainalysis, CFTC COT, Dune, entre otras). Páginas de equipo editorial, conflictos de interés y divulgaciones; contenido patrocinado etiquetado.
- **Temática:** TF-10 Cripto: datos en cadena, investigación y noticias (principal) · secundarias: TF-03
- **Calidad Q:** 67 (B) — Primariedad 12/20 · Historial 10/20 · Transparencia 10/15 · Autoridad 11/15 · Independencia 7/10 · Actualidad 10/10 · Acceso 7/10
- **Tipología:** primaria
- **Acceso:** Muro parcial
- **Ámbitos:** Noticias e investigación de criptoactivos; panel de datos
- **Motivo de inclusión y uso:** Reporterismo e investigación del sector cripto.
- **Restricciones de uso:** Citar artículo y fecha; los datos del panel citan su fuente original.
- **Sesgos y cautelas:** Historial de cambios de propiedad y conflictos de interés en el sector; uso declarado de IA con revisión editorial.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Vigilar propiedad (no declarada en la página leída).
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «The Block crypto news research data dashboard theblock.co»; WebFetch: sí, artículo del panel de datos)

#### RF-0316 · Q 67 (B) — DL News

- **Canal oficial (URL raíz):** https://www.dlnews.com/
- **Emisor:** DL News
- **Documentación y notas:** Medio de noticias sobre cripto y finanzas descentralizadas; sección educativa «Llama U» (p. ej., guía de DefiLlama, 16/08/2023). La página leída no declara la propiedad ni relación alguna con DefiLlama.
- **Temática:** TF-10 Cripto: datos en cadena, investigación y noticias (principal) · secundarias: TF-03
- **Calidad Q:** 67 (B) — Primariedad 11/20 · Historial 10/20 · Transparencia 10/15 · Autoridad 10/15 · Independencia 7/10 · Actualidad 10/10 · Acceso 9/10
- **Tipología:** secundaria
- **Acceso:** Abierto
- **Ámbitos:** Noticias de DeFi, cripto y regulación
- **Motivo de inclusión y uso:** Segunda raíz periodística en cripto independiente de CoinDesk (RF-0036) y The Block (RF-0075).
- **Restricciones de uso:** Opinión/noticia: los hechos se citan en su fuente primaria.
- **Sesgos y cautelas:** Propiedad no declarada en la página leída: verificar posible vínculo con DefiLlama antes de usarla como corroboración independiente de RF-0076.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin datos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «DefiLlama DeFi TVL dashboard stablecoins fees revenue»; WebFetch: sí)

<!-- Tanda 3 · 2026-11-02 · cupo de 22 búsquedas · altas RF-0317…RF-0341 (anexo; dentro de cada temática, por Q descendente) -->

#### RF-0366 · Q 67 (B) — Chainalysis — Crypto Crime Report

- **Canal oficial (URL raíz):** https://chainalysis.com/reports/crypto-crime-2026
- **Emisor:** Chainalysis
- **Documentación y notas:** Informe anual sobre blanqueo, estafas, exploits de DeFi y ransomware (edición 2026), en varios idiomas, con boletín semanal; la página no describe metodología.
- **Temática:** TF-10 Cripto: datos en cadena, investigación y noticias (principal) · secundarias: TF-02
- **Calidad Q:** 67 (B) — Primariedad 14/20 · Historial 10/20 · Transparencia 8/15 · Autoridad 14/15 · Independencia 6/10 · Actualidad 8/10 · Acceso 7/10
- **Tipología:** secundaria
- **Acceso:** Abierto con descarga (posible formulario)
- **Ámbitos:** Actividad ilícita en criptoactivos
- **Motivo de inclusión y uso:** Referencia sectorial de riesgo regulatorio y reputacional.
- **Restricciones de uso:** Citar edición y cifra; contrastar con datos oficiales.
- **Sesgos y cautelas:** Vende herramientas de análisis relacionadas (conflicto de interés); metodología no publicada en la página.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Chainalysis Crypto Crime Report 2026»; WebFetch: sí)

#### RF-0340 · Q 66 (B) — Decrypt — noticias cripto

- **Canal oficial (URL raíz):** https://decrypt.co/7741/cambridge-bitcoin-electricity-index
- **Emisor:** Decrypt Media, Inc.
- **Documentación y notas:** Medio de noticias sobre criptoactivos y web3; páginas de divulgación financiera (decrypt.co/financial-disclosures), manifiesto y código de conducta.
- **Temática:** TF-10 Cripto: datos en cadena, investigación y noticias (principal) · secundarias: TF-03
- **Calidad Q:** 66 (B) — Primariedad 10/20 · Historial 10/20 · Transparencia 10/15 · Autoridad 10/15 · Independencia 7/10 · Actualidad 10/10 · Acceso 9/10
- **Tipología:** secundaria
- **Acceso:** Abierto
- **Ámbitos:** Noticias de criptoactivos
- **Motivo de inclusión y uso:** Raíz periodística con política de divulgación publicada.
- **Restricciones de uso:** Opinión/noticia: los hechos se citan en su fuente primaria.
- **Sesgos y cautelas:** Medio sectorial; revisar las divulgaciones financieras.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin datos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Cambridge Bitcoin Electricity Consumption Index CCAF»; WebFetch: sí)

#### RF-0339 · Q 65 (B) — Blockworks — noticias, investigación y análisis cripto

- **Canal oficial (URL raíz):** https://blockworks.com/news/layer-2-secured-by-ethereum
- **Emisor:** Blockworks Inc. (Nueva York)
- **Documentación y notas:** Red con noticias, pódcasts, boletines, eventos, Analytics y Blockworks Research (plataforma de investigación). La página leída no enlaza política editorial ni de divulgación.
- **Temática:** TF-10 Cripto: datos en cadena, investigación y noticias (principal) · secundarias: TF-03
- **Calidad Q:** 65 (B) — Primariedad 11/20 · Historial 10/20 · Transparencia 8/15 · Autoridad 11/15 · Independencia 7/10 · Actualidad 10/10 · Acceso 8/10
- **Tipología:** secundaria
- **Acceso:** Abierto (noticias); investigación de pago
- **Ámbitos:** Noticias e investigación de criptoactivos y finanzas descentralizadas
- **Motivo de inclusión y uso:** Raíz periodística adicional en cripto.
- **Restricciones de uso:** Opinión/noticia: los hechos se citan en su fuente primaria.
- **Sesgos y cautelas:** Sin política de conflictos visible; ingresos por eventos y patrocinios.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin datos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «L2BEAT layer 2 rollups risk analysis value secured»; WebFetch: sí)

<!-- Tanda 4 · 2026-11-02 · cupo de 28 búsquedas · altas RF-0342…RF-0369 -->

#### RF-0369 · Q 62 (C) — BTC-ECHO — noticias cripto (Alemania)

- **Canal oficial (URL raíz):** https://www.btc-echo.de/news/chainalysis-report-so-kriminell-waren-bitcoin-und-co-2023-177458/
- **Emisor:** BTC-ECHO GmbH
- **Documentación y notas:** Medio alemán de Bitcoin y blockchain desde 2014; políticas de principios, ética, publicidad, correcciones y uso de IA enlazadas; parte del contenido es de pago (Plus+).
- **Temática:** TF-10 Cripto: datos en cadena, investigación y noticias (principal) · secundarias: TF-03
- **Calidad Q:** 62 (C) — Primariedad 9/20 · Historial 10/20 · Transparencia 10/15 · Autoridad 9/15 · Independencia 7/10 · Actualidad 10/10 · Acceso 7/10
- **Tipología:** secundaria
- **Acceso:** Abierto con muro parcial
- **Ámbitos:** Noticias de criptoactivos en el ámbito germanófono
- **Motivo de inclusión y uso:** Diversidad geográfica europea en noticias cripto.
- **Restricciones de uso:** Opinión/noticia: los hechos se citan en su fuente primaria.
- **Sesgos y cautelas:** Medio sectorial con ingresos publicitarios.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin datos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Cambridge Bitcoin Electricity Consumption Index CCAF»; WebFetch: sí)

#### RF-0368 · Q 60 (C) — Cointelegraph — noticias cripto

- **Canal oficial (URL raíz):** https://cointelegraph.com/news/energy-used-by-idle-device-in-the-us-can-power-bitcoin-for-4-years/
- **Emisor:** Cointelegraph
- **Documentación y notas:** Medio de noticias de criptoactivos de gran difusión (artículo leído de 03/07/2019 sobre CBECI con cifras y cita de fuentes).
- **Temática:** TF-10 Cripto: datos en cadena, investigación y noticias (principal) · secundarias: TF-03
- **Calidad Q:** 60 (C) — Primariedad 9/20 · Historial 10/20 · Transparencia 7/15 · Autoridad 9/15 · Independencia 5/10 · Actualidad 10/10 · Acceso 10/10
- **Tipología:** secundaria
- **Acceso:** Abierto
- **Ámbitos:** Noticias de criptoactivos
- **Motivo de inclusión y uso:** Pista de actualidad; los hechos se citan en su fuente primaria.
- **Restricciones de uso:** Opinión/noticia: no usar como prueba de hechos.
- **Sesgos y cautelas:** Historial de controversias sobre contenido patrocinado en el sector; política editorial no leída.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin datos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Cambridge Bitcoin Electricity Consumption Index CCAF»; WebFetch: sí)

## TF-11 Mercados privados y alternativos (datos e índices)

#### RF-0401 · Q 86 (A) — SEC — Private Fund Statistics (datos del Form PF)

- **Canal oficial (URL raíz):** https://www.sec.gov/data-research/data-visualizations/private-fund-statistics
- **Emisor:** U.S. Securities and Exchange Commission, División de Gestión de Inversiones (Analytics Office)
- **Temática:** TF-11 Mercados privados y alternativos (datos e índices) (principal) · secundarias: TF-02
- **Calidad Q:** 86 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 8/10 · Acceso 10/10
- **Tipología:** primaria (estadística oficial agregada de declaraciones regulatorias)
- **Acceso:** Abierto
- **Ámbitos:** Número de fondos privados y gestores, activos brutos y netos, estrategias de hedge funds, apalancamiento, liquidez, titularidad; último trimestre visto: 2025Q4 (58.891 fondos; 29,6 billones USD de activos brutos)
- **Motivo de inclusión y uso:** Fuente oficial y censal del tamaño, apalancamiento y liquidez de los fondos privados en EE. UU.; contraste de cifras de proveedores comerciales (Preqin, PitchBook). AC-AL: tamaño y apalancamiento del crédito privado y hedge funds; AG-14: riesgo sistémico.
- **Sesgos y cautelas:** Datos agregados con desfase de varios trimestres; cambios de formulario Form PF alteran la comparabilidad de series.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «SEC Private Funds Statistics Form PF Division of Investment Management»; WebFetch: sí)
- **Origen:** Alta F9_S3 (2026-11-02).

#### RF-0403 · Q 83 (A) — ESMA — Annual Statistical Report on EU Alternative Investment Funds

- **Canal oficial (URL raíz):** https://www.esma.europa.eu/press-news/esma-news/esma-report-highlights-liquidity-concerns-alternative-investment-funds-0 (serie de informes ASR AIF; p. ej., https://www.esma.europa.eu/sites/default/files/library/esma50-165-1948_asr_aif_2022.pdf)
- **Emisor:** European Securities and Markets Authority (ESMA)
- **Temática:** TF-11 Mercados privados y alternativos (datos e índices) (principal) · secundarias: TF-02
- **Calidad Q:** 83 (A) — Primariedad 19/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 6/10 · Acceso 10/10
- **Tipología:** primaria (estadística supervisora a partir de los informes de gestores autorizados en el EEE)
- **Acceso:** Abierto
- **Ámbitos:** Patrimonio de FIA de la UE por tipo (capital privado, inmobiliario, hedge funds, fondos de fondos), apalancamiento y desajuste de liquidez
- **Motivo de inclusión y uso:** Equivalente europeo de RF-0401; tamaño y riesgos de liquidez de los fondos alternativos en la UE. AC-AL y AG-14 (vulnerabilidades de liquidez).
- **Sesgos y cautelas:** Periodicidad anual con desfase superior a un año; excluye Reino Unido desde el Brexit (ruptura de series).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «ESMA market report EU alternative investment funds AIF annual statistical report»; WebFetch: sí)
- **Origen:** Alta F9_S3 (2026-11-02).

#### RF-0402 · Q 77 (B) — NCREIF — NCREIF Property Index (NPI)

- **Canal oficial (URL raíz):** https://user.ncreif.org/data-products/property/
- **Emisor:** National Council of Real Estate Investment Fiduciaries (NCREIF)
- **Temática:** TF-11 Mercados privados y alternativos (datos e índices) (principal) · secundarias: TF-09
- **Calidad Q:** 77 (B) — Primariedad 18/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 14/15 · Independencia 7/10 · Actualidad 8/10 · Acceso 7/10
- **Tipología:** primaria (índice construido con datos de propiedades de los miembros)
- **Acceso:** Muro parcial (rentabilidades trimestrales abiertas; desgloses y apalancadas para miembros)
- **Ámbitos:** Rentabilidad trimestral sin apalancar del inmobiliario privado institucional de EE. UU. (oficinas, residencial, industrial, retail, hoteles) desde 4T1977; desglose geográfico
- **Motivo de inclusión y uso:** Referencia histórica del inmobiliario privado (no cotizado) en EE. UU.; comparación con REIT (RF-0068). AC-AL / AC-INM: ciclo inmobiliario privado y prima de iliquidez.
- **Sesgos y cautelas:** Basado en tasaciones (suavizado y retraso frente a precios de transacción); índice congelado desde 1T2003 salvo correcciones; asociación del sector.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «NCREIF Property Index NPI quarterly returns»; WebFetch: sí)
- **Origen:** Alta F9_S3 (2026-11-02).

#### RF-0082 · Q 75 (B) — Liv-ex

- **Canal oficial (URL raíz):** https://www.liv-ex.com/ (índice Liv-ex 100: https://www.liv-ex.com/?p=20589)
- **Emisor:** London International Vintners Exchange (Liv-ex)
- **Temática:** TF-11 Mercados privados y alternativos (datos e índices) (principal)
- **Calidad Q:** 75 (B) — Primariedad 17/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 13/15 · Independencia 7/10 · Actualidad 10/10 · Acceso 6/10
- **Tipología:** primaria
- **Acceso:** Muro parcial (nivel mensual de índices y comentarios abiertos; base de precios para miembros)
- **Ámbitos:** Índices de precios de vino fino (Liv-ex 100, 1000); el Liv-ex 100 agrupa vinos con puntuación ≥ 95 de un crítico de referencia y negociación regular, con revisión anual de componentes
- **Motivo de inclusión y uso:** Precios de transacción del mercado secundario del vino. AC-AL: coleccionables.
- **Sesgos y cautelas:** Plataforma de negociación con interés en el mercado; la página pública no detalla el método de precio del índice.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Liv-ex fine wine 100 index official site»; WebFetch: sí)
- **Origen:** Semilla V3.0 (2026-11-01) confirmada por BFA en F9_S3 (2026-11-02).

#### RF-0080 · Q 72 (B) — Cambridge Associates — benchmarks de capital privado

- **Canal oficial (URL raíz):** https://www.cambridgeassociates.com/private-investment-benchmarks/
- **Emisor:** Cambridge Associates (distribución completa a través de S&P Dow Jones Indices)
- **Temática:** TF-11 Mercados privados y alternativos (datos e índices) (principal)
- **Calidad Q:** 72 (B) — Primariedad 15/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 14/15 · Independencia 7/10 · Actualidad 7/10 · Acceso 7/10
- **Tipología:** secundaria (índices construidos con estados financieros trimestrales de fondos)
- **Acceso:** Resúmenes abiertos (estadísticas seleccionadas gratuitas; informes completos de pago vía S&P DJI)
- **Ámbitos:** Benchmarks trimestrales de capital riesgo y capital privado de EE. UU., desarrollados ex-EE. UU., emergentes, inmobiliario; rentabilidad por añada (Benchmark Books)
- **Motivo de inclusión y uso:** Referencias de rentabilidad agregada por estrategia y añada. AC-AL: comparación capital privado frente a cotizado.
- **Sesgos y cautelas:** Consultora con clientes inversores; datos de fondos de clientes; desfase de unos dos trimestres.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Cambridge Associates private equity benchmark index»; WebFetch: sí)
- **Origen:** Semilla V3.0 (2026-11-01) confirmada por BFA en F9_S3 (2026-11-02); Q corregida de 71 a 72.

#### RF-0448 · Q 72 (B) — Hagerty — Hagerty Market Rating y Valuation Tools (coches clásicos)

- **Canal oficial (URL raíz):** https://hagerty.com/media/?p=364145
- **Emisor:** Hagerty (aseguradora de vehículos de colección)
- **Temática:** TF-11 Mercados privados y alternativos (datos e índices) (principal)
- **Calidad Q:** 72 (B) — Primariedad 14/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 12/15 · Independencia 6/10 · Actualidad 10/10 · Acceso 8/10
- **Tipología:** primaria (con datos propios de pólizas y ventas privadas) y secundaria (subastas)
- **Acceso:** Abierto (índice y metodología); guía de precios con registro
- **Ámbitos:** Índice mensual 0-100 del mercado de coches de colección: subastas, ventas privadas de clientes, valores asegurados, guía de precios (Hagerty Hundred, Blue Chip), panel de expertos e indicadores financieros correlacionados
- **Motivo de inclusión y uso:** Seguimiento del ciclo de los coches de colección como activo alternativo.
- **Sesgos y cautelas:** Aseguradora con interés en el mercado; ponderaciones no publicadas en detalle; centrado en EE. UU.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Hagerty Market Rating classic car index HAGI historic automobile index»; WebFetch: sí, artículo metodológico)
- **Origen:** Alta F9_S3, tanda 3 (2026-11-02).

#### RF-0451 · Q 72 (B) — EDHEC Infra & Private Assets / Scientific Infra & Private Assets (SIPA) — índices de infraestructuras y capital privado

- **Canal oficial (URL raíz):** https://www.edhec.edu/en/research-and-faculty/centres-and-chairs/edhec-infra (índices: https://edhecinfraprivateassets.com/)
- **Emisor:** EDHEC Infrastructure & Private Assets Research Institute; índices comercializados por SIPA (escisión de 2019, adquirida por PEI Group en marzo de 2026)
- **Temática:** TF-11 Mercados privados y alternativos (datos e índices) (principal)
- **Calidad Q:** 72 (B) — Primariedad 16/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 13/15 · Independencia 7/10 · Actualidad 9/10 · Acceso 4/10
- **Tipología:** secundaria (índices construidos con modelos de valoración de activos no cotizados)
- **Acceso:** Restringido (índices de pago; investigación académica abierta)
- **Ámbitos:** Índices y benchmarks de capital y deuda de infraestructuras no cotizadas y de capital privado (infraMetrics, privateMetrics); clasificaciones TICCS y PECCS; proveedor de índices registrado en ESMA
- **Motivo de inclusión y uso:** Único benchmark académico de infraestructuras no cotizadas, con valoración a precio de mercado (menos suavizado que la tasación). AC-AL.
- **Sesgos y cautelas:** Desde 2026 propiedad de PEI Group (grupo de medios y datos de mercados privados); modelos sujetos a riesgo de especificación.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «EDHECinfra Scientific Infra private infrastructure index infraMetrics»; WebFetch: sí, página de EDHEC y nota de prensa de PEI (23/03/2026))
- **Origen:** Alta F9_S3, tanda 3 (2026-11-02).

#### RF-0400 · Q 71 (B) — MSCI — Private Capital Indexes (datos Burgiss)

- **Canal oficial (URL raíz):** https://www.msci.com/our-solutions/private-capital/private-capital-indexes
- **Emisor:** MSCI Inc. (MSCI Private Capital Solutions, antigua The Burgiss Group, adquirida por MSCI)
- **Temática:** TF-11 Mercados privados y alternativos (datos e índices) (principal)
- **Calidad Q:** 71 (B) — Primariedad 16/20 · Historial 10/20 · Transparencia 11/15 · Autoridad 14/15 · Independencia 7/10 · Actualidad 9/10 · Acceso 4/10
- **Tipología:** secundaria (índices de flujos de caja de LP)
- **Acceso:** Restringido (clientes; fichas bajo solicitud)
- **Ámbitos:** Más de 550 índices de activos privados (capital privado, crédito privado, inmobiliario, infraestructuras, recursos naturales), más de 15.400 fondos y 13,2 billones USD de capitalización; series desde 1978; índices de fondos de continuación y semiliquidos
- **Motivo de inclusión y uso:** Base de datos con flujos de caja aportados por inversores (LP), menos expuesta a sesgo de autodeclaración de gestores; contraste con RF-0080. AC-AL.
- **Sesgos y cautelas:** Acceso de pago; la página pública no documenta la relación con los datos Burgiss (se infiere de la adquisición publicada por MSCI); proveedor de índices con interés comercial.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «MSCI Private Capital Solutions Burgiss private capital index data»; WebFetch: sí)
- **Origen:** Alta F9_S3 (2026-11-02).

#### RF-0452 · Q 71 (B) — EY-Parthenon y SpainCap — Estudio sobre la Rentabilidad del Capital Privado en España

- **Canal oficial (URL raíz):** https://www.ey.com/es_es/newsroom/2025/12/el-capital-privado-en-espana-confirma-su-capacidad-de-generar-valor-con-una-tir-neta-del-11
- **Emisor:** EY-Parthenon y SpainCap (asociación española del capital privado), con Webcapitalriesgo
- **Temática:** TF-11 Mercados privados y alternativos (datos e índices) (principal) · secundarias: TF-01
- **Calidad Q:** 71 (B) — Primariedad 16/20 · Historial 10/20 · Transparencia 11/15 · Autoridad 13/15 · Independencia 6/10 · Actualidad 6/10 · Acceso 9/10
- **Tipología:** secundaria (encuesta a gestoras con flujos de fondos)
- **Acceso:** Abierto
- **Ámbitos:** Rentabilidad del capital privado en España: IV estudio (cierre de 2024), 52 gestoras y 187 fondos; TIR neta agregada del 11,1 %, TVPI de 1,6x; private equity 11,6 %, venture capital 8,9 %
- **Motivo de inclusión y uso:** Única referencia de rentabilidad agregada del capital privado español. AC-AL con foco España.
- **Sesgos y cautelas:** Asociación del sector como coautora; participación voluntaria de las gestoras (sesgo de supervivencia); periodicidad irregular.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «SpainCap informe actividad capital privado España 2025» (tanda 1); WebFetch: sí, nota de prensa de EY)
- **Origen:** Alta F9_S3, tanda 3 (2026-11-02).

#### RF-0453 · Q 71 (B) — Carta — State of Private Markets

- **Canal oficial (URL raíz):** https://carta.com/data/
- **Emisor:** Carta (plataforma de gestión de participaciones de empresas no cotizadas)
- **Temática:** TF-11 Mercados privados y alternativos (datos e índices) (principal)
- **Calidad Q:** 71 (B) — Primariedad 16/20 · Historial 10/20 · Transparencia 9/15 · Autoridad 12/15 · Independencia 7/10 · Actualidad 9/10 · Acceso 8/10
- **Tipología:** primaria (datos agregados y anonimizados de la propia plataforma)
- **Acceso:** Abierto (informe trimestral y libro de datos descargable)
- **Ámbitos:** Rondas de financiación, valoraciones medianas y tamaño de ronda de startups de EE. UU. por fase
- **Motivo de inclusión y uso:** Datos de financiación de startups de una plataforma con cobertura amplia; contraste de RF-0079. AC-AL, AC-TEC.
- **Sesgos y cautelas:** Muestra limitada a clientes de Carta; la página leída no publica método, muestra ni definiciones.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Carta State of Private Markets report startup data»; WebFetch: sí)
- **Origen:** Alta F9_S3, tanda 3 (2026-11-02).

#### RF-0404 · Q 70 (B) — HFR — Hedge Fund Research Indices (HFRI, HFRX)

- **Canal oficial (URL raíz):** https://www.hfr.com/hfr-indices/hfr-indices-faq/
- **Emisor:** Hedge Fund Research, Inc. (HFR)
- **Temática:** TF-11 Mercados privados y alternativos (datos e índices) (principal) · secundarias: TF-06
- **Calidad Q:** 70 (B) — Primariedad 15/20 · Historial 10/20 · Transparencia 11/15 · Autoridad 13/15 · Independencia 6/10 · Actualidad 10/10 · Acceso 5/10
- **Tipología:** secundaria (índices con datos autodeclarados por los fondos)
- **Acceso:** Muro parcial (niveles de índice públicos; constituyentes en base de suscripción; uso comercial con licencia)
- **Ámbitos:** Rentabilidad de hedge funds por estrategia (HFRI mensual, rentabilidades netas de comisiones; HFRX diario T+1, investible); base de fondos liquidados
- **Motivo de inclusión y uso:** Referencia de rentabilidad agregada de hedge funds por estrategia. AC-AL: comparación de estrategias alternativas y correlaciones.
- **Sesgos y cautelas:** Aportación voluntaria (sesgos de autoselección y supervivencia; la FAQ no los trata); revisiones Flash/Mid/Final; algunos índices son investibles (interés comercial).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «HFR Hedge Fund Research HFRI indices»; WebFetch: sí)
- **Origen:** Alta F9_S3 (2026-11-02).

#### RF-0405 · Q 70 (B) — Cliffwater Direct Lending Index (CDLI)

- **Canal oficial (URL raíz):** https://cliffwater.com/DefinitionsCDLI (ficha: https://cliffwater.com/files/cdli/docs/CDLI_Fact_Page.pdf)
- **Emisor:** Cliffwater LLC
- **Temática:** TF-11 Mercados privados y alternativos (datos e índices) (principal) · secundarias: TF-06
- **Calidad Q:** 70 (B) — Primariedad 16/20 · Historial 10/20 · Transparencia 11/15 · Autoridad 12/15 · Independencia 6/10 · Actualidad 8/10 · Acceso 7/10
- **Tipología:** secundaria (índice construido con estados trimestrales presentados ante la SEC)
- **Acceso:** Muro parcial (definiciones, ficha e informes resumidos abiertos)
- **Ámbitos:** Rentabilidad, rendimiento, pérdidas y antigüedad de préstamos de crédito directo (préstamos a empresas del mercado medio de EE. UU.); serie trimestral desde septiembre de 2004
- **Motivo de inclusión y uso:** Benchmark de referencia del crédito privado (direct lending) con base en datos regulatorios; mide pérdidas y rendimientos. AC-AL / AC-RF: prima del crédito privado frente a préstamos sindicados.
- **Sesgos y cautelas:** Cliffwater asesora y gestiona vehículos de crédito privado (conflicto potencial); valoraciones contables suavizadas; la página no detalla la ponderación.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Cliffwater Direct Lending Index CDLI»; WebFetch: sí)
- **Origen:** Alta F9_S3 (2026-11-02).

#### RF-0084 · Q 69 (B) — Art Basel y UBS — The Art Market Report

- **Canal oficial (URL raíz):** https://theartmarket.artbasel.com/ (edición 2026: https://www.artbasel.com/stories/the-art-basel-and-ubs-global-art-market-report-2026)
- **Emisor:** Art Basel y UBS; elaborado por Arts Economics (Dr. Clare McAndrew)
- **Temática:** TF-11 Mercados privados y alternativos (datos e índices) (principal)
- **Calidad Q:** 69 (B) — Primariedad 14/20 · Historial 10/20 · Transparencia 11/15 · Autoridad 13/15 · Independencia 7/10 · Actualidad 6/10 · Acceso 8/10
- **Tipología:** secundaria
- **Acceso:** Abierto (descarga del PDF)
- **Ámbitos:** Tamaño y tendencias del mercado mundial del arte (ventas de galerías, subastas, coleccionistas); edición 2026: ventas de 2025 de 59,6 mm USD (+4 %)
- **Motivo de inclusión y uso:** Informe anual de referencia del mercado del arte. AC-AL: coleccionables.
- **Sesgos y cautelas:** Patrocinadores con interés comercial (feria y banca privada); datos de galerías por encuesta.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Art Basel UBS Art Market Report 2026»; WebFetch: sí)
- **Origen:** Semilla V3.0 (2026-11-01) confirmada por BFA en F9_S3 (2026-11-02); URL raíz corregida a theartmarket.artbasel.com.

#### RF-0449 · Q 69 (B) — HAGI — Historic Automobile Group International (índices de coches clásicos)

- **Canal oficial (URL raíz):** https://www.historicautogroup.com/
- **Emisor:** Historic Automobile Group International (Londres; fundado en 2007 por Dietrich Hatlapa)
- **Temática:** TF-11 Mercados privados y alternativos (datos e índices) (principal)
- **Calidad Q:** 69 (B) — Primariedad 15/20 · Historial 10/20 · Transparencia 11/15 · Autoridad 11/15 · Independencia 8/10 · Actualidad 9/10 · Acceso 5/10
- **Tipología:** secundaria (índices de precios de transacción)
- **Acceso:** Muro parcial
- **Ámbitos:** Siete índices en libras esterlinas (HAGI Top: 50 modelos de 19 marcas; Porsche, Ferrari, Mercedes-Benz, Lamborghini, BMW); ponderados por capitalización, método Paasche encadenado, actualización mensual; unos 70 % de transacciones privadas y 30 % de subastas
- **Motivo de inclusión y uso:** Índice europeo de coches clásicos con método documentado; contraste de RF-0448.
- **Sesgos y cautelas:** Datos privados no auditables; solo vehículos en excelente estado (sesgo de selección); comité de índice propio.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Hagerty Market Rating classic car index HAGI historic automobile index»; WebFetch: sí, artículo de Wikipedia que da la URL oficial; la web no se cargó)
- **Origen:** Alta F9_S3, tanda 3 (2026-11-02).

#### RF-0447 · Q 68 (B) — Bain & Company — Global Private Equity Report

- **Canal oficial (URL raíz):** https://www.bain.com/insights/topics/global-private-equity-report/
- **Emisor:** Bain & Company
- **Temática:** TF-11 Mercados privados y alternativos (datos e índices) (principal)
- **Calidad Q:** 68 (B) — Primariedad 12/20 · Historial 10/20 · Transparencia 10/15 · Autoridad 13/15 · Independencia 7/10 · Actualidad 8/10 · Acceso 8/10
- **Tipología:** secundaria
- **Acceso:** Abierto (informe anual; edición 2026: «Powering forward in a new era»; informe de mitad de año)
- **Ámbitos:** Operaciones, salidas, captación y rentabilidades del capital privado a escala mundial
- **Motivo de inclusión y uso:** Informe anual de referencia sobre el ciclo del capital privado; contexto para RF-0080 y RF-0400.
- **Sesgos y cautelas:** Consultora con clientes en el sector; la página leída no detalla las fuentes de datos.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Bain Global Private Equity Report 2026 McKinsey Global Private Markets Report 2026»; WebFetch: sí, página del seminario web de bain.com que enlaza el informe; la página del informe no se cargó)
- **Origen:** Alta F9_S3, tanda 3 (2026-11-02).

#### RF-0079 · Q 67 (B) — PitchBook

- **Canal oficial (URL raíz):** https://pitchbook.com/ (informe público PitchBook-NVCA Venture Monitor: https://nvca.org/research/pitchbook-nvca-venture-monitor)
- **Emisor:** PitchBook (Morningstar); Venture Monitor en coautoría con la National Venture Capital Association (NVCA)
- **Temática:** TF-11 Mercados privados y alternativos (datos e índices) (principal)
- **Calidad Q:** 67 (B) — Primariedad 15/20 · Historial 10/20 · Transparencia 11/15 · Autoridad 13/15 · Independencia 7/10 · Actualidad 8/10 · Acceso 3/10
- **Tipología:** secundaria
- **Acceso:** Restringido (suscripción); Venture Monitor trimestral con PDF y paquete de datos enlazados desde NVCA
- **Ámbitos:** Capital riesgo, operaciones, valoraciones, salidas y captación en EE. UU.
- **Motivo de inclusión y uso:** Base de datos de capital riesgo; usar sus informes públicos periódicos (Venture Monitor). AC-AL / AC-TEC: ciclo de financiación de startups.
- **Sesgos y cautelas:** Acceso restringido; la asociación del sector (NVCA) es coautora del informe público.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «PitchBook NVCA Venture Monitor report»; WebFetch: sí, sobre la página de NVCA; la raíz pitchbook.com solo se confirmó en resultados)
- **Origen:** Semilla V3.0 (2026-11-01) confirmada por BFA en F9_S3 (2026-11-02).

#### RF-0078 · Q 66 (B) — Preqin

- **Canal oficial (URL raíz):** https://www.preqin.com/
- **Emisor:** Preqin (BlackRock desde el 3 de marzo de 2025)
- **Temática:** TF-11 Mercados privados y alternativos (datos e índices) (principal)
- **Calidad Q:** 66 (B) — Primariedad 15/20 · Historial 10/20 · Transparencia 11/15 · Autoridad 13/15 · Independencia 6/10 · Actualidad 8/10 · Acceso 3/10
- **Tipología:** secundaria
- **Acceso:** Restringido (suscripción)
- **Ámbitos:** Capital privado, deuda privada, infraestructuras, hedge funds: captación, rentabilidades, benchmarks (cobertura declarada de 210.000 fondos)
- **Motivo de inclusión y uso:** Base de datos de referencia de mercados privados; usar informes públicos citables. AC-AL.
- **Sesgos y cautelas:** Propiedad de BlackRock, gran gestor de activos privados (conflicto de interés potencial, independencia rebajada de 7 a 6); datos parcialmente autodeclarados por gestores.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Preqin BlackRock acquisition completed private markets data»; WebFetch: sí, nota de prensa en preqin.com)
- **Origen:** Semilla V3.0 (2026-11-01) confirmada por BFA en F9_S3 (2026-11-02); Q corregida de 67 a 66 por el cambio de propiedad.

#### RF-0081 · Q 66 (B) — Knight Frank — The Wealth Report

- **Canal oficial (URL raíz):** https://www.knightfrank.com/wealthreport (índice KFLII: https://www.knightfrank.com/research/article/2026/4/knight-frank-luxury-investment-index-luxury-holds-steady)
- **Emisor:** Knight Frank
- **Temática:** TF-11 Mercados privados y alternativos (datos e índices) (principal) · secundarias: TF-09
- **Calidad Q:** 66 (B) — Primariedad 13/20 · Historial 10/20 · Transparencia 10/15 · Autoridad 12/15 · Independencia 7/10 · Actualidad 6/10 · Acceso 8/10
- **Tipología:** secundaria
- **Acceso:** Abierto (registro)
- **Ámbitos:** Patrimonio de grandes fortunas; Knight Frank Luxury Investment Index (arte, grabados, coches clásicos, relojes, vino, diamantes de color, bolsos): −0,4 % en 2025, +38,6 % en diez años
- **Motivo de inclusión y uso:** Contexto de demanda de activos de lujo y coleccionables. AC-AL.
- **Sesgos y cautelas:** Agencia inmobiliaria (sesgo promocional); periodicidad anual; metodología y ponderaciones del índice no publicadas en la página.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Knight Frank The Wealth Report 2026 luxury investment index»; WebFetch: sí, artículo KFLII)
- **Origen:** Semilla V3.0 (2026-11-01) confirmada por BFA en F9_S3 (2026-11-02).

#### RF-0083 · Q 64 (C) — Artprice (Artmarket.com)

- **Canal oficial (URL raíz):** https://news.artprice.com/ (informe anual: https://news.artprice.com/en/7070/the-art-market-in-2023)
- **Emisor:** Artprice, departamento de Artmarket.com (cotizada en Euronext París)
- **Temática:** TF-11 Mercados privados y alternativos (datos e índices) (principal)
- **Calidad Q:** 64 (C) — Primariedad 14/20 · Historial 10/20 · Transparencia 9/15 · Autoridad 11/15 · Independencia 7/10 · Actualidad 8/10 · Acceso 5/10
- **Tipología:** secundaria
- **Acceso:** Restringido (suscripción); informes anuales abiertos
- **Ámbitos:** Resultados de subastas e índices de arte; informes anuales del mercado de subastas (con Artron/ARAA para China)
- **Motivo de inclusión y uso:** Base de precios de subastas; contraste de RF-0084. AC-AL.
- **Sesgos y cautelas:** Solo subastas (no ventas privadas); índices con sesgo de selección; metodología poco transparente; empresa cotizada con interés en la difusión.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Artprice.com Artmarket art market report auction results»; WebFetch: sí)
- **Origen:** Semilla V3.0 (2026-11-01) confirmada por BFA en F9_S3 (2026-11-02).

#### RF-0450 · Q 63 (C) — Westfleet Advisors — Litigation Finance Market Report

- **Canal oficial (URL raíz):** https://www.westfleetadvisors.com/publications/
- **Emisor:** Westfleet Advisors
- **Temática:** TF-11 Mercados privados y alternativos (datos e índices) (principal)
- **Calidad Q:** 63 (C) — Primariedad 14/20 · Historial 10/20 · Transparencia 9/15 · Autoridad 11/15 · Independencia 6/10 · Actualidad 6/10 · Acceso 7/10
- **Tipología:** secundaria (datos de operaciones de financiadores)
- **Acceso:** Abierto (informe anual)
- **Ámbitos:** Financiación de litigios comercial en EE. UU.: compromisos de capital y número de operaciones nuevas (7.º informe, 2026; 39 financiadores)
- **Motivo de inclusión y uso:** Única serie pública del mercado de financiación de litigios, activo alternativo poco correlacionado. AC-AL.
- **Sesgos y cautelas:** Asesor del sector (conflicto potencial); método de recogida no detallado en la fuente leída; solo EE. UU.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Westfleet Insider litigation finance market report commercial»; WebFetch: sí, noticia de RPX que enlaza la página de publicaciones; la web no se cargó)
- **Origen:** Alta F9_S3, tanda 3 (2026-11-02).

## TF-12 Redes sociales y foros con filtro de calidad

#### RF-0417 · Q 75 (B) — Metaculus (plataforma de pronósticos con puntuación)

- **Canal oficial (URL raíz):** https://www.metaculus.com/ (FAQ y método: https://www.metaculus.com/faq)
- **Emisor:** Metaculus
- **Temática:** TF-12 Redes sociales y foros con filtro de calidad (principal) · secundarias: TF-14
- **Calidad Q:** 75 (B) — Primariedad 12/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 11/15 · Independencia 9/10 · Actualidad 10/10 · Acceso 10/10
- **Tipología:** secundaria (agregación de pronósticos de una comunidad puntuada)
- **Acceso:** Abierto
- **Ámbitos:** Probabilidades agregadas sobre geopolítica, tecnología (IA), macroeconomía y ciencia
- **Motivo de inclusión y uso:** Probabilidades explícitas y puntuadas para escenarios del Analizador y para calibrar sus propias probabilidades. AC-ESC y Evaluador (contraste de calibración).
- **Sesgos y cautelas:** Preguntas a veces poco ligadas a mercados; participación sesgada hacia temas tecnológicos.
- **Criterios anti-manipulación:** Predicción de la Comunidad como mediana ponderada por recencia, resistente a valores atípicos, oculta al abrir cada pregunta y sin bots por defecto; puntuaciones propias (Baseline y Peer); reglas contra el juego de puntos (cierre anticipado, retiradas); historial de exactitud publicado (Brier 0,108 en preguntas resueltas en 2021).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Metaculus forecasting platform track record accuracy»; WebFetch: sí, FAQ)
- **Origen:** Alta F9_S3 (2026-11-02).

#### RF-0454 · Q 75 (B) — Musings on Markets (Aswath Damodaran)

- **Canal oficial (URL raíz):** https://aswathdamodaran.blogspot.com/ (réplica: https://aswathdamodaran.substack.com/)
- **Emisor:** Aswath Damodaran (NYU Stern)
- **Temática:** TF-12 Redes sociales y foros con filtro de calidad (principal) · secundarias: TF-06
- **Calidad Q:** 75 (B) — Primariedad 10/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 14/15 · Independencia 9/10 · Actualidad 9/10 · Acceso 10/10
- **Tipología:** secundaria (valoración con modelos y datos publicados)
- **Acceso:** Abierto
- **Ámbitos:** Valoración de empresas, primas de riesgo, tipos de interés y bolsa, OPV (p. ej., valoración de la OPV de Anthropic, 28/10)
- **Motivo de inclusión y uso:** Valoraciones razonadas con hojas de cálculo descargables; contraste de narrativas de mercado. AC-RV.
- **Sesgos y cautelas:** Opinión de autor; valoraciones sensibles a supuestos.
- **Criterios anti-manipulación:** Autor académico identificado que publica sus datos y modelos (complementa RF-0050); BFA reproduce los supuestos antes de usarlos.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Aswath Damodaran Musings on Markets blog»; WebFetch: sí, archivo de Substack; la página de NYU Stern redirige al blog)
- **Origen:** Alta F9_S3, tanda 3 (2026-11-02).

#### RF-0458 · Q 75 (B) — Follow the Money (Brad Setser, CFR)

- **Canal oficial (URL raíz):** https://www.cfr.org/blogs/follow-the-money
- **Emisor:** Brad W. Setser, Council on Foreign Relations
- **Temática:** TF-12 Redes sociales y foros con filtro de calidad (principal) · secundarias: TF-14
- **Calidad Q:** 75 (B) — Primariedad 12/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 14/15 · Independencia 8/10 · Actualidad 9/10 · Acceso 10/10
- **Tipología:** secundaria (análisis de datos oficiales de flujos)
- **Acceso:** Abierto
- **Ámbitos:** Flujos de capital transfronterizos, reservas, divisas (renminbi, Taiwán), datos TIC, desequilibrios comerciales, deuda soberana
- **Motivo de inclusión y uso:** Referencia en flujos y desequilibrios globales con datos oficiales. AC-FX, AC-MAC.
- **Sesgos y cautelas:** Exfuncionario del Tesoro de EE. UU.; opinión sobre política cambiaria de China.
- **Criterios anti-manipulación:** Autor identificado, investigador sénior de un think tank; gráficos con fuente oficial.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Brad Setser Follow the Money blog Council on Foreign Relations»; WebFetch: sí (última entrada 11/10/2026))
- **Origen:** Alta F9_S3, tanda 3 (2026-11-02).

#### RF-0408 · Q 73 (B) — Calculated Risk (Bill McBride)

- **Canal oficial (URL raíz):** https://www.calculatedriskblog.com/ (boletín: calculatedrisk.substack.com)
- **Emisor:** Bill McBride (Calculated Risk)
- **Temática:** TF-12 Redes sociales y foros con filtro de calidad (principal) · secundarias: TF-09
- **Calidad Q:** 73 (B) — Primariedad 12/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 12/15 · Independencia 8/10 · Actualidad 10/10 · Acceso 9/10
- **Tipología:** secundaria (análisis diario de datos oficiales)
- **Acceso:** Abierto (boletín inmobiliario de pago sin publicidad)
- **Ámbitos:** Vivienda e inmobiliario de EE. UU., empleo, indicadores macro de alta frecuencia
- **Motivo de inclusión y uso:** Lectura rápida y con historial de los datos oficiales de vivienda y empleo; sus gráficos citan la fuente primaria. AC-MAC y AC-INM.
- **Sesgos y cautelas:** Autor único; foco en EE. UU.
- **Criterios anti-manipulación:** Bitácora nominal con trayectoria desde mediados de los 2000 y gráficos con fuente; incluida en la lista de Time de mejores blogs financieros (2011). BFA: citar la fuente primaria que enlaza, no el blog.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «economics blogs list Calculated Risk Marginal Revolution Econbrowser»; WebFetch: sí, entrada de 2011 y listado de Intelligent Economist 2026)
- **Origen:** Alta F9_S3 (2026-11-02).

#### RF-0409 · Q 72 (B) — Econbrowser (James Hamilton y Menzie Chinn)

- **Canal oficial (URL raíz):** https://econbrowser.com/
- **Emisor:** James D. Hamilton (UC San Diego) y Menzie Chinn (Universidad de Wisconsin)
- **Temática:** TF-12 Redes sociales y foros con filtro de calidad (principal) · secundarias: TF-13
- **Calidad Q:** 72 (B) — Primariedad 11/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 14/15 · Independencia 9/10 · Actualidad 6/10 · Acceso 10/10
- **Tipología:** secundaria (bitácora académica)
- **Acceso:** Abierto
- **Ámbitos:** Macroeconomía, petróleo y energía, política monetaria y fiscal, previsiones
- **Motivo de inclusión y uso:** Análisis académico aplicado de coyuntura por economistas de referencia (p. ej., Hamilton sobre shocks petroleros). AC-MAC y AC-MP.
- **Sesgos y cautelas:** Opiniones de autor; la actividad reciente no se comprobó en la página leída (entrada de 2013), aunque figura en el listado de blogs de 2026.
- **Criterios anti-manipulación:** Autores académicos identificados, con publicaciones revisadas por pares; entradas con datos y referencias.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «economics blogs list Calculated Risk Marginal Revolution Econbrowser»; WebFetch: sí)
- **Origen:** Alta F9_S3 (2026-11-02).

#### RF-0416 · Q 71 (B) — Nada es Gratis

- **Canal oficial (URL raíz):** http://www.nadaesgratis.es/
- **Emisor:** Bitácora colectiva de economistas académicos alojada por FEDEA; fundadores: Antonio Cabrales, Jesús Fernández-Villaverde, Luis Garicano y Juan Rubio-Ramírez
- **Temática:** TF-12 Redes sociales y foros con filtro de calidad (principal) · secundarias: TF-14
- **Calidad Q:** 71 (B) — Primariedad 9/20 · Historial 10/20 · Transparencia 11/15 · Autoridad 14/15 · Independencia 8/10 · Actualidad 9/10 · Acceso 10/10
- **Tipología:** secundaria (divulgación académica)
- **Acceso:** Abierto
- **Ámbitos:** Economía española e hispanohablante: mercado laboral, vivienda, fiscalidad, educación, política económica
- **Motivo de inclusión y uso:** Principal bitácora académica en español; socia del consorcio de VoxEU (RF-0090). AC-MAC con foco España.
- **Sesgos y cautelas:** Columnas sin revisión por pares; algunos autores con actividad política o pública.
- **Criterios anti-manipulación:** Autores académicos identificados, con afiliación; alojada por un centro de investigación (FEDEA, RF-0439) y asociada a VoxEU.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Nada es Gratis blog economía Fedea»; WebFetch: sí, columna de VoxEU que presenta el blog; nadaesgratis.es no se cargó)
- **Origen:** Alta F9_S3 (2026-11-02).

#### RF-0410 · Q 70 (B) — Marginal Revolution (Tyler Cowen y Alex Tabarrok)

- **Canal oficial (URL raíz):** https://marginalrevolution.com/
- **Emisor:** Tyler Cowen y Alex Tabarrok (George Mason University)
- **Temática:** TF-12 Redes sociales y foros con filtro de calidad (principal)
- **Calidad Q:** 70 (B) — Primariedad 8/20 · Historial 10/20 · Transparencia 10/15 · Autoridad 13/15 · Independencia 9/10 · Actualidad 10/10 · Acceso 10/10
- **Tipología:** secundaria (bitácora académica)
- **Acceso:** Abierto
- **Ámbitos:** Economía general, innovación, IA, política económica; enlaces diarios a investigación nueva
- **Motivo de inclusión y uso:** Detección temprana de investigación y debates económicos nuevos. AC-TEC y AC-MAC.
- **Sesgos y cautelas:** Orientación liberal-libertaria declarada; mucho contenido de enlaces sin análisis.
- **Criterios anti-manipulación:** Autores académicos identificados; trayectoria larga; BFA cita el trabajo enlazado, nunca la entrada.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «economics blogs list Calculated Risk Marginal Revolution Econbrowser»; WebFetch: sí, listado de Intelligent Economist 2026 que da autores y URL; la web no se cargó)
- **Origen:** Alta F9_S3 (2026-11-02).

#### RF-0413 · Q 68 (B) — Money Stuff (Matt Levine, Bloomberg Opinion)

- **Canal oficial (URL raíz):** https://www.bloomberg.com/opinion/authors/ARbTQlRLRjE/matthew-s-levine
- **Emisor:** Matt Levine, columnista de Bloomberg Opinion (exabogado de Wachtell Lipton y exbanquero de Goldman Sachs)
- **Temática:** TF-12 Redes sociales y foros con filtro de calidad (principal) · secundarias: TF-03
- **Calidad Q:** 68 (B) — Primariedad 9/20 · Historial 10/20 · Transparencia 11/15 · Autoridad 14/15 · Independencia 7/10 · Actualidad 10/10 · Acceso 7/10
- **Tipología:** secundaria (columna y boletín diario)
- **Acceso:** Muro parcial (boletín gratuito por correo; web con suscripción)
- **Ámbitos:** Finanzas corporativas, estructura de mercado, regulación de valores, fraude y escándalos financieros
- **Motivo de inclusión y uso:** Interpretación experta de operaciones, litigios y regulación de mercados; útil para entender mecánica y riesgos. AC-REG y AG-14.
- **Sesgos y cautelas:** Columna de opinión de un medio con intereses comerciales (terminal Bloomberg); tono humorístico.
- **Criterios anti-manipulación:** Autor identificado con experiencia profesional; cita documentos primarios (demandas, filings). BFA: verificar el hecho en el documento enlazado.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Matt Levine Money Stuff Noahpinion Apricitas Economics newsletter»; WebFetch: sí, ficha de Wikipedia y listado de Full Stack Economics que da la URL; la página de Bloomberg no se cargó)
- **Origen:** Alta F9_S3 (2026-11-02).

#### RF-0415 · Q 68 (B) — Apricitas Economics (Joseph Politano)

- **Canal oficial (URL raíz):** https://apricitas.substack.com/
- **Emisor:** Joseph (Joey) Politano
- **Temática:** TF-12 Redes sociales y foros con filtro de calidad (principal)
- **Calidad Q:** 68 (B) — Primariedad 11/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 10/15 · Independencia 8/10 · Actualidad 9/10 · Acceso 8/10
- **Tipología:** secundaria (análisis gráfico de datos oficiales)
- **Acceso:** Abierto (Substack; parte de pago)
- **Ámbitos:** Macroeconomía de EE. UU., empleo, comercio, inversión industrial y en IA, con gráficos de datos oficiales
- **Motivo de inclusión y uso:** Análisis visual de series oficiales con fuente identificada. AC-MAC.
- **Sesgos y cautelas:** Autor joven sin trayectoria académica; plataforma de suscripción.
- **Criterios anti-manipulación:** Cada gráfico cita la serie oficial (BLS, BEA, Census); BFA reproduce el dato desde la fuente primaria.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Matt Levine Money Stuff Noahpinion Apricitas Economics newsletter»; WebFetch: sí, listado de Full Stack Economics que da la URL; la web no se cargó)
- **Origen:** Alta F9_S3 (2026-11-02).

#### RF-0412 · Q 66 (B) — Conversable Economist (Timothy Taylor)

- **Canal oficial (URL raíz):** https://conversableeconomist.blogspot.com/
- **Emisor:** Timothy Taylor
- **Temática:** TF-12 Redes sociales y foros con filtro de calidad (principal)
- **Calidad Q:** 66 (B) — Primariedad 7/20 · Historial 10/20 · Transparencia 11/15 · Autoridad 12/15 · Independencia 9/10 · Actualidad 7/10 · Acceso 10/10
- **Tipología:** secundaria (divulgación económica)
- **Acceso:** Abierto
- **Ámbitos:** Síntesis de investigación y de informes oficiales sobre economía y política económica
- **Motivo de inclusión y uso:** Resúmenes fiables de literatura e informes oficiales. AC-MAC.
- **Sesgos y cautelas:** Autor único; orientado a divulgación, no a mercados.
- **Criterios anti-manipulación:** Autor identificado; cita y enlaza las fuentes originales.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «economics blogs list Calculated Risk Marginal Revolution Econbrowser»; WebFetch: sí, listado de Intelligent Economist 2026; la web no se cargó)
- **Origen:** Alta F9_S3 (2026-11-02).

#### RF-0455 · Q 66 (B) — Alpha Architect — blog de investigación

- **Canal oficial (URL raíz):** https://alphaarchitect.com/
- **Emisor:** Alpha Architect (gestora de activos; fundada por Wesley Gray)
- **Temática:** TF-12 Redes sociales y foros con filtro de calidad (principal) · secundarias: TF-13
- **Calidad Q:** 66 (B) — Primariedad 9/20 · Historial 10/20 · Transparencia 11/15 · Autoridad 12/15 · Independencia 5/10 · Actualidad 9/10 · Acceso 10/10
- **Tipología:** secundaria (resúmenes de investigación académica)
- **Acceso:** Abierto
- **Ámbitos:** Factores (valor, momento), inversión basada en evidencia, resúmenes de artículos académicos
- **Motivo de inclusión y uso:** Puente entre la literatura académica de factores y la práctica. AC-FAC.
- **Sesgos y cautelas:** Gestora con productos propios de factores (conflicto de interés); avisos de que las opiniones son del autor.
- **Criterios anti-manipulación:** Autores identificados (Wesley Gray, doctor en Finanzas por Chicago); cita los artículos de origen; BFA cita el artículo académico, no el resumen.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Alpha Architect blog research summaries Wes Gray»; WebFetch: sí)
- **Origen:** Alta F9_S3, tanda 3 (2026-11-02).

#### RF-0406 · Q 64 (C) — Bogleheads (foro y wiki)

- **Canal oficial (URL raíz):** https://www.bogleheads.org/
- **Emisor:** John C. Bogle Center for Financial Literacy (organización sin ánimo de lucro 501(c)(3), voluntaria)
- **Temática:** TF-12 Redes sociales y foros con filtro de calidad (principal)
- **Calidad Q:** 64 (C) — Primariedad 6/20 · Historial 10/20 · Transparencia 11/15 · Autoridad 9/15 · Independencia 9/10 · Actualidad 9/10 · Acceso 10/10
- **Tipología:** terciaria (comunidad moderada)
- **Acceso:** Abierto
- **Ámbitos:** Inversión pasiva, asignación de activos, fiscalidad del inversor particular; wiki de referencia
- **Motivo de inclusión y uso:** Termómetro de la práctica del inversor minorista prudente y de su reacción a productos y comisiones; la wiki como glosario de contraste. AC-SEN y AG-14 (comportamiento minorista).
- **Sesgos y cautelas:** Sesgo doctrinal pro-indexación y pro-Vanguard; mayoritariamente estadounidense.
- **Criterios anti-manipulación:** Foro sin publicidad ni ánimo de lucro (financiado por donaciones), nacido en 1998 en Morningstar y propio desde 2007; moderación por voluntarios. BFA: solo hilos con enlaces a datos primarios; no usar como pronóstico de mercado.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Bogleheads forum Value Investors Club investment community quality»; WebFetch: sí, página «About» del Bogle Center (boglecenter.net), que identifica Bogleheads.org; el foro no se cargó)
- **Origen:** Alta F9_S3 (2026-11-02).

#### RF-0411 · Q 64 (C) — The Big Picture (Barry Ritholtz)

- **Canal oficial (URL raíz):** https://ritholtz.com/
- **Emisor:** Barry Ritholtz (Ritholtz Wealth Management)
- **Temática:** TF-12 Redes sociales y foros con filtro de calidad (principal) · secundarias: TF-04
- **Calidad Q:** 64 (C) — Primariedad 7/20 · Historial 10/20 · Transparencia 9/15 · Autoridad 12/15 · Independencia 6/10 · Actualidad 10/10 · Acceso 10/10
- **Tipología:** secundaria (bitácora de mercados)
- **Acceso:** Abierto
- **Ámbitos:** Mercados, comportamiento del inversor, finanzas; listas de lecturas diarias; listado anual de mejores blogs de economía
- **Motivo de inclusión y uso:** Contexto de mercado y curaduría de lecturas; útil como índice de otras fuentes. AC-SEN.
- **Sesgos y cautelas:** Autor gestor de patrimonio (interés comercial); mezcla de temas no económicos.
- **Criterios anti-manipulación:** Autor identificado; BFA usa la bitácora como índice de lecturas y cita la fuente enlazada.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «economics blogs list Calculated Risk Marginal Revolution Econbrowser»; WebFetch: sí, «Top 100 Economics Blogs of 2016»; autoría según el listado de Intelligent Economist 2026)
- **Origen:** Alta F9_S3 (2026-11-02).

#### RF-0414 · Q 63 (C) — Noahpinion (Noah Smith)

- **Canal oficial (URL raíz):** https://noahpinion.substack.com/
- **Emisor:** Noah Smith
- **Temática:** TF-12 Redes sociales y foros con filtro de calidad (principal) · secundarias: TF-14
- **Calidad Q:** 63 (C) — Primariedad 7/20 · Historial 10/20 · Transparencia 9/15 · Autoridad 11/15 · Independencia 8/10 · Actualidad 10/10 · Acceso 8/10
- **Tipología:** secundaria (boletín de opinión)
- **Acceso:** Abierto (Substack; parte de pago)
- **Ámbitos:** Macroeconomía, política industrial, tecnología, geoeconomía (EE. UU., China, Japón)
- **Motivo de inclusión y uso:** Opinión informada sobre política industrial y tecnológica; contraste de narrativas. AC-TEC y AC-GEO.
- **Sesgos y cautelas:** Columnista de opinión con posiciones marcadas; sin revisión.
- **Criterios anti-manipulación:** Autor identificado con formación académica en economía; BFA solo lo usa para narrativas, nunca como evidencia de un hecho.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Matt Levine Money Stuff Noahpinion Apricitas Economics newsletter»; WebFetch: sí, listado de Full Stack Economics que da la URL; la web no se cargó)
- **Origen:** Alta F9_S3 (2026-11-02).

#### RF-0456 · Q 62 (C) — Quantitative Finance Stack Exchange

- **Canal oficial (URL raíz):** http://quant.stackexchange.com/
- **Emisor:** Stack Exchange
- **Temática:** TF-12 Redes sociales y foros con filtro de calidad (principal) · secundarias: TF-13
- **Calidad Q:** 62 (C) — Primariedad 6/20 · Historial 10/20 · Transparencia 11/15 · Autoridad 8/15 · Independencia 9/10 · Actualidad 8/10 · Acceso 10/10
- **Tipología:** terciaria (preguntas y respuestas moderadas por la comunidad)
- **Acceso:** Abierto
- **Ámbitos:** Valoración de derivados, modelización de riesgos, matemáticas financieras y programación cuantitativa
- **Motivo de inclusión y uso:** Resolución de dudas técnicas de métodos (complemento de F8).
- **Sesgos y cautelas:** Respuestas de calidad desigual; autores a menudo con seudónimo.
- **Criterios anti-manipulación:** Votos y reputación de la comunidad, moderación por usuarios con reputación alta; BFA solo usa respuestas aceptadas con referencias.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Quantitative Finance Stack Exchange»; WebFetch: sí, entrada de R-bloggers (2011) que da la URL; el sitio no se cargó)
- **Origen:** Alta F9_S3, tanda 3 (2026-11-02).

#### RF-0407 · Q 61 (C) — Value Investors Club

- **Canal oficial (URL raíz):** https://valueinvestorsclub.com/
- **Emisor:** Value Investors Club (comunidad privada de inversores; según fuentes secundarias, vinculada a Joel Greenblatt)
- **Temática:** TF-12 Redes sociales y foros con filtro de calidad (principal) · secundarias: TF-04
- **Calidad Q:** 61 (C) — Primariedad 10/20 · Historial 10/20 · Transparencia 9/15 · Autoridad 12/15 · Independencia 6/10 · Actualidad 8/10 · Acceso 6/10
- **Tipología:** secundaria (tesis de inversión de miembros seleccionados)
- **Acceso:** Muro parcial (no miembros: ideas con unos 45 días de retraso)
- **Ámbitos:** Tesis de inversión fundamentales (valor, situaciones especiales) con debate entre miembros
- **Motivo de inclusión y uso:** Fuente de tesis de alta calidad y contra-tesis para valores concretos. AC-RV: ideas de valor; el Evaluador puede medir el acierto por autor.
- **Sesgos y cautelas:** Los miembros pueden tener posiciones; retraso de acceso para no miembros; foco en pequeñas compañías.
- **Criterios anti-manipulación:** Admisión muy selectiva: hay que presentar una tesis que valora un gestor de inversiones (alta tasa de rechazo); obligación de publicar entre 2 y 6 ideas al año; pérdida de la membresía por comentarios irrelevantes. BFA: contrastar siempre los datos de la tesis en EDGAR o CNMV.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Bogleheads forum Value Investors Club investment community quality»; WebFetch: sí, página «About us» y reseña de Old School Value)
- **Origen:** Alta F9_S3 (2026-11-02).

#### RF-0457 · Q 56 (C) — Wilmott Forum

- **Canal oficial (URL raíz):** https://forum.wilmott.com/
- **Emisor:** Wilmott (comunidad de finanzas cuantitativas)
- **Temática:** TF-12 Redes sociales y foros con filtro de calidad (principal)
- **Calidad Q:** 56 (C) — Primariedad 5/20 · Historial 10/20 · Transparencia 7/15 · Autoridad 9/15 · Independencia 8/10 · Actualidad 8/10 · Acceso 9/10
- **Tipología:** terciaria (foro profesional)
- **Acceso:** Abierto (registro para publicar)
- **Ámbitos:** Foro técnico de finanzas cuantitativas: métodos numéricos, trading, programación, carreras
- **Motivo de inclusión y uso:** Debate técnico entre profesionales cuantitativos; señal de problemas de métodos.
- **Sesgos y cautelas:** Moderación poco documentada; mucho contenido fuera de tema.
- **Criterios anti-manipulación:** Normas publicadas: los proveedores deben contactar con la administración antes de promocionar productos; foro técnico reservado a profesionales. BFA: solo hilos con referencias.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Quantitative Finance Stack Exchange»; WebFetch: sí)
- **Origen:** Alta F9_S3, tanda 3 (2026-11-02).

#### RF-0087 · Q 52 (C) — Seeking Alpha

- **Canal oficial (URL raíz):** https://seekingalpha.com/ (principios editoriales: https://about.seekingalpha.com/editorial)
- **Emisor:** Seeking Alpha Ltd.
- **Temática:** TF-12 Redes sociales y foros con filtro de calidad (principal) · secundarias: TF-05
- **Calidad Q:** 52 (C) — Primariedad 6/20 · Historial 10/20 · Transparencia 8/15 · Autoridad 6/15 · Independencia 5/10 · Actualidad 10/10 · Acceso 7/10
- **Tipología:** terciaria
- **Acceso:** Muro parcial
- **Ámbitos:** Análisis de colaboradores externos con calificación Comprar/Mantener/Vender; transcripciones de conferencias de resultados
- **Motivo de inclusión y uso:** Pista de tesis y contra-tesis; transcripciones de resultados. Nunca evidencia de un hecho.
- **Sesgos y cautelas:** Calidad muy heterogénea; los colaboradores eligen valores y calificación (los editores no cambian el fondo); incentivo a publicar sobre valores pequeños.
- **Criterios anti-manipulación:** La plataforma exige declarar posiciones personales en los valores tratados y aplica escrutinio adicional a valores de menos de 1 USD o capitalización inferior a 100 M USD. BFA añade: usar solo autores con historial ≥ 2 años y declaración de posiciones; descartar artículos sobre micro y nanocapitalizaciones salvo contraste en EDGAR; no usar calificaciones agregadas como señal sin validación del Evaluador.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Seeking Alpha contributor disclosure policy positions»; WebFetch: sí, página de principios editoriales)
- **Origen:** Semilla V3.0 (2026-11-01) confirmada por BFA en F9_S3 (2026-11-02). Q corregida de 49 a 52 por la política de declaración de posiciones.

#### RF-0086 · Q 46 (D) — X (antes Twitter), cuentas verificadas por historial

- **Canal oficial (URL raíz):** https://x.com/ (Notas de la Comunidad: https://help.x.com/en/using-x/community-notes)
- **Emisor:** X Corp.
- **Temática:** TF-12 Redes sociales y foros con filtro de calidad (principal)
- **Calidad Q:** 46 (D) — Primariedad 5/20 · Historial 10/20 · Transparencia 5/15 · Autoridad 4/15 · Independencia 4/10 · Actualidad 10/10 · Acceso 8/10
- **Tipología:** terciaria
- **Acceso:** Abierto (limitado)
- **Ámbitos:** Declaraciones de responsables, analistas y empresas; sentimiento; Notas de la Comunidad como contexto colaborativo
- **Motivo de inclusión y uso:** Detectar declaraciones primarias (confirmar siempre en la fuente original) y cambios de narrativa.
- **Sesgos y cautelas:** La verificación de cuenta no equivale a fiabilidad; bots, cuentas coordinadas y desinformación; acceso a la API restringido.
- **Criterios anti-manipulación:** Solo cuentas de una lista blanca mantenida por BFA (cuentas oficiales de organismos, empresas y autores ya registrados en F7–F9, enlazadas desde su web oficial). Tratar como señal de alerta una publicación con Nota de la Comunidad visible (las notas solo se muestran si las valoran útiles colaboradores de puntos de vista distintos; algoritmo y datos abiertos en GitHub). Nunca usar recuentos de interacción como medida de fiabilidad.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «X Community Notes how it works help center»; WebFetch: sí, página de ayuda de Notas de la Comunidad)
- **Justificación de permanencia (nivel D):** Única vía para medir sentimiento y atención minorista (señal, nunca evidencia de hechos); uso restringido y declarado. Si el Evaluador no mide aporte predictivo en 180 días, BORRAR.
- **Origen:** Semilla V3.0 (2026-11-01) confirmada por BFA en F9_S3 (2026-11-02). Q corregida de 44 a 46 por el mecanismo de notas con algoritmo abierto.

#### RF-0085 · Q 45 (D) — Reddit (subforos de inversión con filtro de calidad)

- **Canal oficial (URL raíz):** https://www.reddit.com/r/SecurityAnalysis/ (subforo de referencia; raíz: https://www.reddit.com/)
- **Emisor:** Reddit Inc.; subforos moderados por voluntarios
- **Temática:** TF-12 Redes sociales y foros con filtro de calidad (principal)
- **Calidad Q:** 45 (D) — Primariedad 4/20 · Historial 10/20 · Transparencia 4/15 · Autoridad 4/15 · Independencia 4/10 · Actualidad 10/10 · Acceso 9/10
- **Tipología:** terciaria
- **Acceso:** Abierto
- **Ámbitos:** Sentimiento minorista; narrativas emergentes; r/SecurityAnalysis (unos 215.000 miembros, activo desde 2010) para tesis de análisis fundamental
- **Motivo de inclusión y uso:** Solo como señal de sentimiento o atención (nunca evidencia de un hecho).
- **Sesgos y cautelas:** Manipulación coordinada, bots, promoción encubierta; los subforos generalistas pierden calidad por la diversidad de la audiencia.
- **Criterios anti-manipulación:** Usar solo subforos de lista blanca con normas publicadas y moderación activa (r/SecurityAnalysis, r/Bogleheads); filtrar por antigüedad de cuenta ≥ 1 año, karma, enlace a fuente primaria y ausencia de valores de baja capitalización sin contraste; medir picos de menciones como posible campaña coordinada antes de usarlos como sentimiento.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «reddit r/SecurityAnalysis r/investing subreddit rules moderation»; WebFetch: sí, sobre el directorio The Hive Index, que da la URL del subforo; reddit.com no se cargó)
- **Justificación de permanencia (nivel D):** Única vía para medir sentimiento y atención minorista (señal, nunca evidencia de hechos); uso restringido y declarado. Si el Evaluador no mide aporte predictivo en 180 días, BORRAR.
- **Origen:** Semilla V3.0 (2026-11-01) confirmada por BFA en F9_S3 (2026-11-02). Q corregida de 43 a 45; ámbito acotado a subforos de lista blanca.

## TF-13 Repositorios académicos y de investigación abierta

#### RF-0420 · Q 84 (A) — Crossref (registro de DOI y metadatos abiertos)

- **Canal oficial (URL raíz):** https://www.crossref.org/
- **Emisor:** Crossref (organización sin ánimo de lucro con más de 19.000 miembros)
- **Temática:** TF-13 Repositorios académicos y de investigación abierta (principal)
- **Calidad Q:** 84 (A) — Primariedad 16/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 14/15 · Independencia 10/10 · Actualidad 10/10 · Acceso 10/10
- **Tipología:** primaria (registro oficial de metadatos de DOI)
- **Acceso:** Abierto (API REST de metadatos)
- **Ámbitos:** Unos 150 millones de registros DOI; metadatos de obras, financiadores, referencias y retractaciones
- **Motivo de inclusión y uso:** Resolución y validación de DOI y metadatos en cada alta (R19: «DOI resuelto»); detección de retractaciones vía datos de Retraction Watch (RF-0421). AG-16, Auditor.
- **Sesgos y cautelas:** Calidad de metadatos dependiente de lo que depositan los editores.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Crossref Retraction Watch database open retraction data»; WebFetch: sí, nota de EASE (14/09/2023) que enlaza crossref.org; la web no se cargó)
- **Origen:** Alta F9_S3 (2026-11-02).

#### RF-0422 · Q 84 (A) — BIS Working Papers

- **Canal oficial (URL raíz):** https://www.bis.org/wpapers
- **Emisor:** Bank for International Settlements (BIS)
- **Temática:** TF-13 Repositorios académicos y de investigación abierta (principal) · secundarias: TF-01
- **Calidad Q:** 84 (A) — Primariedad 18/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 15/15 · Independencia 9/10 · Actualidad 9/10 · Acceso 10/10
- **Tipología:** primaria (documentos de trabajo)
- **Acceso:** Abierto
- **Ámbitos:** Investigación de economistas del BIS y ocasionalmente de bancos centrales y universidades: política monetaria, estabilidad financiera, mercados
- **Motivo de inclusión y uso:** Investigación de frontera de banca central con datos propios del BIS. AC-MP, AC-RF, AG-14.
- **Sesgos y cautelas:** Las opiniones son de los autores y no necesariamente del BIS; sin revisión por pares completa.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «ECB Working Paper Series BIS Working Papers IMF Working Papers»; WebFetch: sí)
- **Origen:** Alta F9_S3 (2026-11-02).

#### RF-0423 · Q 84 (A) — ECB Working Paper Series

- **Canal oficial (URL raíz):** https://www.ecb.europa.eu/press/research-publications/working-papers
- **Emisor:** Banco Central Europeo (BCE)
- **Temática:** TF-13 Repositorios académicos y de investigación abierta (principal) · secundarias: TF-01
- **Calidad Q:** 84 (A) — Primariedad 18/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 15/15 · Independencia 9/10 · Actualidad 9/10 · Acceso 10/10
- **Tipología:** primaria (documentos de trabajo)
- **Acceso:** Abierto
- **Ámbitos:** Investigación económica relevante para las funciones del BCE: política monetaria, transmisión, banca, mercados del área del euro
- **Motivo de inclusión y uso:** Literatura de banca central europea para fundamentar análisis del área del euro. AC-MP, AC-MAC.
- **Sesgos y cautelas:** Trabajo en curso; las opiniones son de los autores y no necesariamente del BCE.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «ECB Working Paper Series BIS Working Papers IMF Working Papers»; WebFetch: sí)
- **Origen:** Alta F9_S3 (2026-11-02).

#### RF-0461 · Q 84 (A) — IMF Working Papers

- **Canal oficial (URL raíz):** https://www.imf.org/en/Publications/WP (ruta de la serie vista en los resultados; página leída: https://www.imf.org/en/Publications/WP/Issues/2016/12/30/Working-Paper-Summaries-WP-95-62-95-146-2022)
- **Emisor:** Fondo Monetario Internacional (FMI)
- **Temática:** TF-13 Repositorios académicos y de investigación abierta (principal) · secundarias: TF-01
- **Calidad Q:** 84 (A) — Primariedad 18/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 15/15 · Independencia 9/10 · Actualidad 9/10 · Acceso 10/10
- **Tipología:** primaria (documentos de trabajo)
- **Acceso:** Abierto (con DOI)
- **Ámbitos:** Unos 300 documentos al año de personal del FMI: balanza de pagos, política monetaria y fiscal, liquidez global, economías nacionales
- **Motivo de inclusión y uso:** Investigación aplicada de un organismo internacional con cobertura de emergentes. AC-MAC, AC-FX.
- **Sesgos y cautelas:** No representan la opinión del FMI; sin revisión por pares completa.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «IMF Working Papers series imf.org publications»; WebFetch: sí)
- **Origen:** Alta F9_S3, tanda 3 (2026-11-02).

#### RF-0424 · Q 83 (A) — Banco de España — Documentos de Trabajo

- **Canal oficial (URL raíz):** https://www.bde.es/bde/en/secciones/informes/analisis-economico-e-investigacion/documentos-de-trabajo/ (repositorio: https://repositorio.bde.es/handle/123456789/5661)
- **Emisor:** Banco de España
- **Temática:** TF-13 Repositorios académicos y de investigación abierta (principal) · secundarias: TF-01
- **Calidad Q:** 83 (A) — Primariedad 18/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 14/15 · Independencia 9/10 · Actualidad 9/10 · Acceso 10/10
- **Tipología:** primaria (documentos de trabajo)
- **Acceso:** Abierto (PDF; serie desde 1978 en el repositorio institucional)
- **Ámbitos:** Macroeconomía, política monetaria, banca, finanzas y economía española; último visto: n.º 2640 (26/10/2026)
- **Motivo de inclusión y uso:** Investigación de banco central con foco España y área del euro. AC-MAC y AC-MP con perspectiva española.
- **Sesgos y cautelas:** Opiniones de los autores; sin revisión por pares completa.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Banco de España documentos de trabajo Federal Reserve FEDS finance and economics discussion series»; WebFetch: sí)
- **Origen:** Alta F9_S3 (2026-11-02).

#### RF-0008 · Q 82 (A) — NBER Working Papers (National Bureau of Economic Research)

- **Canal oficial:** nber.org/papers
- **Documentación y notas:** Trabajos con página propia por número (nber.org/papers/wNNNNN); citar número de WP y año; versiones abiertas del autor frecuentes
- **Temática:** TF-13 Repositorios académicos y de investigación abierta (principal)
- **Calidad Q:** 82 (A) — Primariedad 18/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 14/15 · Independencia 9/10 · Actualidad 9/10 · Acceso 9/10
- **Nivel de fiabilidad en V2.4:** B
- **Tipología:** primaria (trabajos originales sin revisión por pares completa)
- **Motivo de inclusión:** Documentos de trabajo de investigación económica de primer nivel; muchos se publican después en revistas revisadas por pares
- **Ámbitos:** Investigación económica y financiera; literatura de frontera; datos y metodologías nuevos
- **Restricciones de uso:** Muchos WP son de descarga gratuita y otros tienen coste o requieren registro; verificar pieza a pieza; un WP no está revisado por pares: citarlo como documento de trabajo
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Sesgos posibles:** Contenido no revisado por pares en el momento de la publicación; verificar si existe versión publicada posterior
- **Cambios de propiedad o de metodología:** Sin cambios conocidos
- **Estado:** Aprobada
- **Estado del enlace:** PENDIENTE_BARRIDO
- **Última verificación:** 2026-10-25 (Completa (URL viva y naturaleza del contenido comprobadas el 25/10/2026))

#### RF-0421 · Q 82 (A) — Retraction Watch Database (datos abiertos vía Crossref)

- **Canal oficial (URL raíz):** https://retractionwatch.com/the-retraction-watch-database/ (datos: https://gitlab.com/crossref/retraction-watch-data)
- **Emisor:** Retraction Watch / Center for Scientific Integrity; datos adquiridos y abiertos por Crossref en 2023
- **Temática:** TF-13 Repositorios académicos y de investigación abierta (principal)
- **Calidad Q:** 82 (A) — Primariedad 17/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 13/15 · Independencia 9/10 · Actualidad 10/10 · Acceso 10/10
- **Tipología:** primaria (registro de retractaciones)
- **Acceso:** Abierto
- **Ámbitos:** Retractaciones, expresiones de preocupación y correcciones de artículos académicos
- **Motivo de inclusión y uso:** Comprobación trimestral de retractaciones exigida por R19 para F7, F8 y FM. Auditor y AG-16.
- **Sesgos y cautelas:** Cobertura incompleta en ciencias sociales y documentos de trabajo.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Crossref Retraction Watch database open retraction data»; WebFetch: sí)
- **Origen:** Alta F9_S3 (2026-11-02).

#### RF-0462 · Q 82 (A) — Zenodo (repositorio abierto de CERN y OpenAIRE)

- **Emisor/organización:** CERN, en el marco de OpenAIRE (Comisión Europea)
- **Año:** Servicio vigente
- **Publicación o institución:** Repositorio multidisciplinar de investigación abierta
- **Tipo de documento:** Repositorio de publicaciones, datos y software con DOI
- **Temática:** TF-13 Repositorios académicos y de investigación abierta (principal) · secundarias: —
- **Calidad Q:** 82 (A) — Primariedad 16/20 · Exactitud histórica 10/20 · Transparencia 15/15 · Autoridad 14/15 · Independencia 10/10 · Actualidad 8/10 · Accesibilidad 9/10
- **Canal oficial (URL raíz):** https://zenodo.org (confirmada en la página oficial de OpenAIRE, https://www.openaire.eu/zenodo/)
- **Acceso y licencia:** Gratuito; cada depósito recibe DOI; recolectable por OAI-PMH; licencia según depósito
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Zenodo open repository CERN research data publications»; WebFetch: sí, a openscience.web.cern.ch/zenodo y openaire.eu/zenodo, que confirman operador, DOI y URL)
- **Contenido:** Repositorio de CERN para cualquier resultado de investigación (artículos, datos, código), con DOI y vínculo a financiadores; útil para localizar datos y código de réplica de artículos.
- **Uso en el bloque:** DOC-A, DOC-M y Motor: obtener datos y código de réplica citables; Curador: identificar versiones y DOI de depósitos.
- **Limitaciones:** No hay revisión por pares de los depósitos; la calidad depende del autor. Sustituye a RF-0425 (duplicado de FRASER).

#### RF-0426 · Q 81 (A) — Fed in Print (catálogo de investigación del Sistema de la Reserva Federal)

- **Canal oficial (URL raíz):** https://www.fedinprint.org/
- **Emisor:** Sistema de la Reserva Federal (Board of Governors y los 12 bancos regionales)
- **Temática:** TF-13 Repositorios académicos y de investigación abierta (principal) · secundarias: TF-01
- **Calidad Q:** 81 (A) — Primariedad 14/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 10/10 · Acceso 10/10
- **Tipología:** terciaria (catálogo de publicaciones)
- **Acceso:** Abierto (API y RSS)
- **Ámbitos:** Documentos de trabajo, informes y blogs de toda la Reserva Federal, por banco, serie, autor y código JEL
- **Motivo de inclusión y uso:** Punto único de búsqueda de la investigación de la Fed (FEDS, Staff Reports, Liberty Street, On the Economy). AG-16, AC-MP.
- **Sesgos y cautelas:** Enlaza al texto en la web de cada banco; no aloja contenido.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «FRASER Federal Reserve Bank of St. Louis digital library EconStor ZBW open access economics repository»; WebFetch: sí, ficha de registro en fedinprint.org)
- **Origen:** Alta F9_S3 (2026-11-02).

#### RF-0089 · Q 79 (B) — OpenAlex

- **Canal oficial (URL raíz):** https://openalex.org/ (API: api.openalex.org)
- **Emisor:** OurResearch (organización sin ánimo de lucro, fundada en 2011)
- **Temática:** TF-13 Repositorios académicos y de investigación abierta (principal)
- **Calidad Q:** 79 (B) — Primariedad 14/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 12/15 · Independencia 10/10 · Actualidad 10/10 · Acceso 9/10
- **Tipología:** terciaria
- **Acceso:** Abierto (datos CC0; API con cuota gratuita diaria y precios por uso desde febrero de 2026; búsquedas por ID o DOI gratuitas; volcado completo en S3)
- **Ámbitos:** Índice abierto de obras, autores, revistas, instituciones y conceptos; sustituto del Microsoft Academic Graph desde enero de 2022
- **Motivo de inclusión y uso:** Metadatos abiertos, citas y detección de acceso abierto con API documentada; base para búsqueda hacia adelante y comprobación de metadatos (R19). AG-16 y Auditor.
- **Sesgos y cautelas:** Errores de desambiguación de autores; parte de la jerarquía de conceptos heredada de MAG.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «OpenAlex Unpaywall OurResearch open scholarly metadata API»; WebFetch: sí, artículo de Priem, Piwowar y Orr (2022) en arXiv:2205.01833 y guía de CASRAI; openalex.org no se cargó)
- **Origen:** Semilla V3.0 (2026-11-01) confirmada por BFA en F9_S3 (2026-11-02). Q corregida de 80 a 79 por el nuevo modelo de precios de la API.

#### RF-0419 · Q 79 (B) — Unpaywall

- **Canal oficial (URL raíz):** https://unpaywall.org/
- **Emisor:** OurResearch
- **Temática:** TF-13 Repositorios académicos y de investigación abierta (principal)
- **Calidad Q:** 79 (B) — Primariedad 13/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 12/15 · Independencia 10/10 · Actualidad 10/10 · Acceso 10/10
- **Tipología:** terciaria (base de estado de acceso abierto)
- **Acceso:** Abierto (API REST gratuita por DOI con correo de contacto; volcados periódicos; extensión de navegador)
- **Ámbitos:** Estado de acceso abierto por DOI (gold, hybrid, green, bronze, closed) y mejor ubicación abierta legal
- **Motivo de inclusión y uso:** Comprobación automática de la existencia de versión abierta legal para cada DOI de F7, F8 y FM; alimenta el campo «Acceso y licencia». AG-16 y HT-02.
- **Sesgos y cautelas:** No aloja contenido; la clasificación puede errar en versiones de autor.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «OpenAlex Unpaywall OurResearch open scholarly metadata API»; WebFetch: sí, guía de CASRAI sobre Unpaywall; unpaywall.org no se cargó)
- **Origen:** Alta F9_S3 (2026-11-02).

#### RF-0090 · Q 78 (B) — CEPR — VoxEU

- **Canal oficial (URL raíz):** https://cepr.org/voxeu
- **Emisor:** Centre for Economic Policy Research (CEPR)
- **Temática:** TF-13 Repositorios académicos y de investigación abierta (principal) · secundarias: TF-14
- **Calidad Q:** 78 (B) — Primariedad 14/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 13/15 · Independencia 9/10 · Actualidad 10/10 · Acceso 10/10
- **Tipología:** secundaria
- **Acceso:** Abierto (columnas descargables sin suscripción)
- **Ámbitos:** Columnas de investigación aplicada de economistas académicos; consorcio de portales asociados (p. ej., Nada es Gratis, RF-0416)
- **Motivo de inclusión y uso:** Síntesis accesibles de investigación reciente con enlace al trabajo de origen. AC-MAC, AC-MP.
- **Sesgos y cautelas:** Columnas sin revisión por pares completa.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Nada es Gratis blog economía Fedea»; WebFetch: sí, columna en cepr.org/voxeu)
- **Origen:** Semilla V3.0 (2026-11-01) confirmada por BFA en F9_S3 (2026-11-02).

#### RF-0418 · Q 78 (B) — CORE (agregador de investigación en acceso abierto)

- **Canal oficial (URL raíz):** https://core.ac.uk/
- **Emisor:** CORE, Open University (Reino Unido)
- **Temática:** TF-13 Repositorios académicos y de investigación abierta (principal)
- **Calidad Q:** 78 (B) — Primariedad 13/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 12/15 · Independencia 10/10 · Actualidad 10/10 · Acceso 10/10
- **Tipología:** terciaria (agregador de texto completo)
- **Acceso:** Abierto
- **Ámbitos:** Millones de textos completos en acceso abierto de cientos de repositorios y revistas; búsqueda, minería y desarrollo de aplicaciones
- **Motivo de inclusión y uso:** Localiza el texto completo abierto de trabajos citados en F7 y F8 cuando el editor tiene muro de pago. AG-16.
- **Sesgos y cautelas:** Metadatos heterogéneos de los repositorios de origen; duplicados de versiones.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «CORE core.ac.uk Semantic Scholar BASE Bielefeld open access aggregator»; WebFetch: sí)
- **Origen:** Alta F9_S3 (2026-11-02).

#### RF-0459 · Q 78 (B) — Semantic Scholar

- **Canal oficial (URL raíz):** https://www.semanticscholar.org/
- **Emisor:** Ai2 (Allen Institute for Artificial Intelligence)
- **Temática:** TF-13 Repositorios académicos y de investigación abierta (principal)
- **Calidad Q:** 78 (B) — Primariedad 13/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 12/15 · Independencia 10/10 · Actualidad 10/10 · Acceso 10/10
- **Tipología:** terciaria (buscador académico con IA)
- **Acceso:** Abierto (API gratuita; datos con licencia ODC-BY 1.0)
- **Ámbitos:** Más de 214 millones de artículos; grafo de citas, recomendaciones, resúmenes TLDR; lanzado en 2015
- **Motivo de inclusión y uso:** Búsqueda y grafo de citas con API abierta; alternativa a RF-0088. AG-16.
- **Sesgos y cautelas:** Fusiones de registros erróneas; TLDR en beta y con cobertura parcial.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Semantic Scholar Allen Institute for AI academic search engine API»; WebFetch: sí, guía de CASRAI; semanticscholar.org no se cargó)
- **Origen:** Alta F9_S3, tanda 3 (2026-11-02).

#### RF-0460 · Q 77 (B) — DOAJ — Directory of Open Access Journals

- **Canal oficial (URL raíz):** https://doaj.org/
- **Emisor:** DOAJ (independiente, financiado con donaciones; activo desde 2003)
- **Temática:** TF-13 Repositorios académicos y de investigación abierta (principal)
- **Calidad Q:** 77 (B) — Primariedad 13/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 12/15 · Independencia 10/10 · Actualidad 10/10 · Acceso 10/10
- **Tipología:** terciaria (índice de revistas en acceso abierto)
- **Acceso:** Abierto (datos abiertos)
- **Ámbitos:** Índice de revistas de acceso abierto revisadas por editores y voluntarios
- **Motivo de inclusión y uso:** Filtro de revistas de acceso abierto legítimas (prevención de revistas depredadoras en F7 y F8). AG-16, Auditor.
- **Sesgos y cautelas:** La página leída no detalla los criterios de inclusión ni el número de revistas.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «DOAJ Directory of Open Access Journals about»; WebFetch: sí)
- **Origen:** Alta F9_S3, tanda 3 (2026-11-02).

#### RF-0010 · Q 75 (B) — arXiv q-fin (Quantitative Finance)

- **Canal oficial:** arxiv.org/list/q-fin/recent
- **Documentación y notas:** Documentación de API: info.arxiv.org/help/api/ · Citar identificador arXiv y versión (ficha)
- **Temática:** TF-13 Repositorios académicos y de investigación abierta (principal)
- **Calidad Q:** 75 (B) — Primariedad 16/20 · Historial 10/20 · Transparencia 9/15 · Autoridad 10/15 · Independencia 10/10 · Actualidad 10/10 · Acceso 10/10
- **Nivel de fiabilidad en V2.4:** B
- **Tipología:** primaria (preprints)
- **Motivo de inclusión:** Repositorio abierto de preprints de finanzas cuantitativas y econofísica: acceso gratuito e inmediato
- **Ámbitos:** Finanzas cuantitativas; modelización; econofísica; métodos estadísticos
- **Restricciones de uso:** Licencias abiertas por pieza (frecuente arXiv non-exclusive); citar identificador arXiv y versión
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Sesgos posibles:** Sin revisión por pares (solo moderación de ámbito); calidad heterogénea
- **Cambios de propiedad o de metodología:** Sin cambios conocidos
- **Estado:** Aprobada
- **Estado del enlace:** PENDIENTE_BARRIDO
- **Última verificación:** 2026-10-25 (Completa (URL viva y naturaleza del contenido comprobadas el 25/10/2026))

#### RF-0012 · Q 75 (B) — Financial Analysts Journal (CFA Institute / Taylor & Francis)

- **Canal oficial:** tandfonline.com (página de la revista en Taylor & Francis)
- **Documentación y notas:** Institución editora: cfainstitute.org · Acceso variable por pieza (ficha): verificar cada artículo en el primer uso
- **Temática:** TF-13 Repositorios académicos y de investigación abierta (principal) · secundarias: TF-05
- **Calidad Q:** 75 (B) — Primariedad 16/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 14/15 · Independencia 8/10 · Actualidad 8/10 · Acceso 6/10
- **Nivel de fiabilidad en V2.4:** A
- **Tipología:** primaria (revista revisada por pares)
- **Motivo de inclusión:** Revista insignia revisada por pares para profesionales de la inversión (publica desde 1945); puente entre la academia y la práctica de carteras
- **Ámbitos:** Gestión de carteras; análisis de inversiones; investigación aplicada para el inversor profesional
- **Restricciones de uso:** Publicada por Taylor & Francis para el CFA Institute; el acceso es variable por pieza (opción de acceso abierto para autores; verificar cada artículo)
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Sesgos posibles:** Orientación profesional (gestión de carteras); premios Graham and Dodd como señal de calidad
- **Cambios de propiedad o de metodología:** Sin cambios conocidos; revalidar nivel de acceso por pieza en cada uso
- **Estado:** Aprobada
- **Estado del enlace:** PENDIENTE_BARRIDO
- **Última verificación:** 2026-10-25 (Completa (URL viva y naturaleza del contenido comprobadas el 25/10/2026))
- **Alerta:** Acceso variable por pieza: verificar cada artículo en su primer uso.

#### RF-0088 · Q 75 (B) — Google Scholar

- **Canal oficial (URL raíz):** https://scholar.google.com/
- **Emisor:** Google
- **Temática:** TF-13 Repositorios académicos y de investigación abierta (principal)
- **Calidad Q:** 75 (B) — Primariedad 14/20 · Historial 10/20 · Transparencia 9/15 · Autoridad 12/15 · Independencia 10/10 · Actualidad 10/10 · Acceso 10/10
- **Tipología:** terciaria
- **Acceso:** Abierto
- **Ámbitos:** Búsqueda académica, recuento de citas, versiones de autor; cobertura estimada del 79–90 % de los artículos académicos en inglés
- **Motivo de inclusión y uso:** Descubrimiento de literatura, búsqueda hacia adelante y localización de versiones abiertas. AG-16.
- **Sesgos y cautelas:** No publica la lista de fuentes que rastrea ni su frecuencia de actualización; sin API pública ni exportación de DOI; indexa revistas depredadoras; recuentos de citas manipulables (artículos generados con SCIgen, servicios de compra de citas documentados en 2024).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Wikipedia list of academic databases and search engines»; WebFetch: sí, listado y artículo de Wikipedia sobre Google Scholar; scholar.google.com no se cargó)
- **Origen:** Semilla V3.0 (2026-11-01) confirmada por BFA en F9_S3 (2026-11-02). Q corregida de 78 a 75 por la opacidad de cobertura y la manipulabilidad de citas documentadas.

#### RF-0009 · Q 72 (B) — SSRN (Social Science Research Network)

- **Canal oficial:** ssrn.com
- **Documentación y notas:** Resúmenes y descargas gratuitas con registro; citar el abstract_id de cada trabajo
- **Temática:** TF-13 Repositorios académicos y de investigación abierta (principal)
- **Calidad Q:** 72 (B) — Primariedad 16/20 · Historial 10/20 · Transparencia 9/15 · Autoridad 10/15 · Independencia 9/10 · Actualidad 10/10 · Acceso 8/10
- **Nivel de fiabilidad en V2.4:** B
- **Tipología:** primaria (preprints)
- **Motivo de inclusión:** Principal repositorio de preprints de finanzas y economía: acceso temprano a la investigación antes de su publicación en revista
- **Ámbitos:** Finanzas; economía; literatura de frontera; versiones de autor
- **Restricciones de uso:** Descarga gratuita con registro; citar como preprint con su abstract_id y comprobar si existe versión publicada posterior
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Sesgos posibles:** Sin revisión por pares garantizada; sesgo de publicación de autores y de papers aún no filtrados
- **Cambios de propiedad o de metodología:** Propiedad de Elsevier desde 2016; vigilar cambios de acceso
- **Estado:** Aprobada
- **Estado del enlace:** PENDIENTE_BARRIDO
- **Última verificación:** 2026-10-25 (Completa (URL viva y naturaleza del contenido comprobadas el 25/10/2026))

#### RF-0011 · Q 70 (B) — RePEc / IDEAS (Research Papers in Economics)

- **Canal oficial:** ideas.repec.org
- **Documentación y notas:** Espejo: econpapers.repec.org · Útil para metadatos normalizados de trabajos y revistas económicas que sustentan otras entradas (NBER, SSRN, FAJ)
- **Temática:** TF-13 Repositorios académicos y de investigación abierta (principal)
- **Calidad Q:** 70 (B) — Primariedad 8/20 · Historial 10/20 · Transparencia 11/15 · Autoridad 12/15 · Independencia 10/10 · Actualidad 9/10 · Acceso 10/10
- **Nivel de fiabilidad en V2.4:** B
- **Tipología:** terciaria (agregador)
- **Motivo de inclusión:** Agregador académico descentralizado de literatura económica: localiza versiones de acceso gratuito (verdes) de artículos publicados en revistas de pago
- **Ámbitos:** Economía y finanzas; localización de versiones de trabajo y de acceso gratuito; bibliografía estructurada
- **Restricciones de uso:** Es un agregador: citar la fuente primaria que RePEc enlaza, no IDEAS
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Sesgos posibles:** Cobertura dependiente de los archivos participantes; metadatos a veces incompletos
- **Cambios de propiedad o de metodología:** Sin cambios conocidos
- **Estado:** Aprobada
- **Estado del enlace:** PENDIENTE_BARRIDO
- **Última verificación:** 2026-10-25 (Completa (URL viva y naturaleza del contenido comprobadas el 25/10/2026))

## TF-14 Think tanks y prospectiva

#### RF-0434 · Q 82 (A) — Institute for Fiscal Studies (IFS)

- **Canal oficial (URL raíz):** https://www.ifs.org.uk/
- **Emisor:** Institute for Fiscal Studies (fundado en 1969)
- **Temática:** TF-14 Think tanks y prospectiva (principal)
- **Calidad Q:** 82 (A) — Primariedad 16/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 9/10 · Actualidad 8/10 · Acceso 10/10
- **Tipología:** secundaria (análisis con microdatos y modelos propios)
- **Acceso:** Abierto
- **Ámbitos:** Política fiscal y presupuestaria del Reino Unido, impuestos, prestaciones, desigualdad; Green Budget anual desde 1982
- **Motivo de inclusión y uso:** Referencia independiente en finanzas públicas; modelo de análisis fiscal para el riesgo soberano británico.
- **Sesgos y cautelas:** Críticas de sesgo pro-mercado; financiación por proyectos (ESRC y otros). Transparify la calificó «muy transparente» en financiación (2018).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Wikipedia list of think tanks»; WebFetch: sí, listado de think tanks del Reino Unido y artículo de Wikipedia; URL oficial confirmada en la ficha de Wikipedia leída con WebFetch a partir del listado devuelto por la búsqueda (lectura lateral); la web oficial no se cargó)
- **Origen:** Alta F9_S3 (2026-11-02).

#### RF-0442 · Q 82 (A) — Kiel Institute for the World Economy (IfW Kiel)

- **Canal oficial (URL raíz):** https://www.ifw-kiel.de/ (redirige a www.kielinstitut.de)
- **Emisor:** Kiel Institute for the World Economy — Leibniz Center for Research on Global Economic Challenges
- **Temática:** TF-14 Think tanks y prospectiva (principal)
- **Calidad Q:** 82 (A) — Primariedad 17/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 14/15 · Independencia 9/10 · Actualidad 9/10 · Acceso 10/10
- **Tipología:** secundaria (instituto de investigación con datos y previsiones propias)
- **Acceso:** Abierto
- **Ámbitos:** Economía internacional, comercio, previsiones de coyuntura; documentos de trabajo, policy briefs, Review of World Economics
- **Motivo de inclusión y uso:** Previsiones y seguimiento del comercio mundial y de Alemania. AC-MAC y AC-GEO.
- **Sesgos y cautelas:** Financiación pública (Leibniz); perspectiva alemana.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** REDIRIGIDO
- **Última verificación:** 2026-11-02 (búsqueda web: «Kiel Institute for the World Economy ifo Institute CEPS ECFR think tank»; WebFetch: sí, ficha EDIRC (RePEc) con la web oficial; la página de ifw-kiel.de devolvió 302 a kielinstitut.de (no cargada))
- **Origen:** Alta F9_S3 (2026-11-02).

#### RF-0435 · Q 78 (B) — NIESR — National Institute of Economic and Social Research

- **Canal oficial (URL raíz):** https://www.niesr.ac.uk/
- **Emisor:** NIESR (fundado en 1938)
- **Temática:** TF-14 Think tanks y prospectiva (principal)
- **Calidad Q:** 78 (B) — Primariedad 16/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 14/15 · Independencia 8/10 · Actualidad 9/10 · Acceso 8/10
- **Tipología:** secundaria (previsiones con modelo propio)
- **Acceso:** Muro parcial (UK Outlook abierto; Global Outlook de pago)
- **Ámbitos:** Previsiones trimestrales del Reino Unido y globales con el modelo NiGEM; seguimiento mensual del PIB, la inflación y los salarios
- **Motivo de inclusión y uso:** Previsión macro con modelo global documentado. AC-MAC.
- **Sesgos y cautelas:** Sin financiación básica: depende de proyectos encargados (gobierno, ESRC, fundaciones, Comisión Europea, sector privado).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Wikipedia list of think tanks»; WebFetch: sí, listado de think tanks del Reino Unido y artículo de Wikipedia; URL oficial confirmada en la ficha de Wikipedia leída con WebFetch a partir del listado devuelto por la búsqueda (lectura lateral); la web oficial no se cargó)
- **Origen:** Alta F9_S3 (2026-11-02).

#### RF-0092 · Q 77 (B) — Peterson Institute for International Economics (PIIE)

- **Canal oficial (URL raíz):** https://www.piie.com/ (política de transparencia: https://www.piie.com/about/transparency-policy)
- **Emisor:** PIIE
- **Temática:** TF-14 Think tanks y prospectiva (principal)
- **Calidad Q:** 77 (B) — Primariedad 14/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 14/15 · Independencia 8/10 · Actualidad 8/10 · Acceso 10/10
- **Tipología:** secundaria
- **Acceso:** Abierto
- **Ámbitos:** Comercio, finanzas internacionales, política macroeconómica
- **Motivo de inclusión y uso:** Análisis aplicado de economía internacional.
- **Sesgos y cautelas:** Unos 150 financiadores (empresas, fundaciones, particulares, instituciones públicas); el mayor donante histórico es la Peter G. Peterson Foundation. Publica sus fuentes de financiación cada año desde 2013 y exige a los autores declarar vínculos financieros.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «brookings.edu piie.com bruegel.org think tank economic policy research»; WebFetch: sí)
- **Origen:** Semilla V3.0 (2026-11-01) confirmada por BFA en F9_S3 (2026-11-02). Q corregida de 76 a 77 por la transparencia de financiación.

#### RF-0093 · Q 76 (B) — Bruegel

- **Canal oficial (URL raíz):** https://www.bruegel.org/ (datos: https://www.bruegel.org/datasets)
- **Emisor:** Bruegel (fundado en 2005)
- **Temática:** TF-14 Think tanks y prospectiva (principal)
- **Calidad Q:** 76 (B) — Primariedad 15/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 13/15 · Independencia 8/10 · Actualidad 8/10 · Acceso 10/10
- **Tipología:** secundaria (con bases de datos propias)
- **Acceso:** Abierto
- **Ámbitos:** Política económica europea, energía, comercio; bases de datos: importaciones y demanda de gas, tipos de cambio efectivos reales de 178 países, base de datos de China, seguimiento del comercio global, agregados monetarios Divisia del área del euro, seguimiento del ETS
- **Motivo de inclusión y uso:** Think tank europeo de referencia con bases de datos propias.
- **Sesgos y cautelas:** Miembros: gobiernos de la UE, empresas internacionales e instituciones, que participan en fijar las prioridades de investigación.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «brookings.edu piie.com bruegel.org think tank economic policy research»; WebFetch: sí, páginas «About» y «Datasets»)
- **Origen:** Semilla V3.0 (2026-11-01) confirmada por BFA en F9_S3 (2026-11-02). Q corregida de 75 a 76 (primariedad por sus bases de datos).

#### RF-0433 · Q 76 (B) — Resolution Foundation

- **Canal oficial (URL raíz):** https://www.resolutionfoundation.org/
- **Emisor:** Resolution Foundation (fundada en 2005)
- **Temática:** TF-14 Think tanks y prospectiva (principal)
- **Calidad Q:** 76 (B) — Primariedad 15/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 13/15 · Independencia 8/10 · Actualidad 8/10 · Acceso 10/10
- **Tipología:** secundaria
- **Acceso:** Abierto
- **Ámbitos:** Niveles de vida, rentas bajas y medias, mercado laboral y vivienda en el Reino Unido
- **Motivo de inclusión y uso:** Análisis distributivo y del consumidor británico.
- **Sesgos y cautelas:** Financiada sobre todo por el Resolution Trust (Clive Cowdery); se cita más desde el centro-izquierda.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Wikipedia list of think tanks»; WebFetch: sí, listado de think tanks del Reino Unido y artículo de Wikipedia; URL oficial confirmada en la ficha de Wikipedia leída con WebFetch a partir del listado devuelto por la búsqueda (lectura lateral); la web oficial no se cargó)
- **Origen:** Alta F9_S3 (2026-11-02).

#### RF-0438 · Q 76 (B) — Funcas

- **Canal oficial (URL raíz):** https://www.funcas.es/
- **Emisor:** Funcas (creada y mantenida por CECA)
- **Temática:** TF-14 Think tanks y prospectiva (principal)
- **Calidad Q:** 76 (B) — Primariedad 15/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 13/15 · Independencia 7/10 · Actualidad 9/10 · Acceso 10/10
- **Tipología:** secundaria
- **Acceso:** Abierto
- **Ámbitos:** Coyuntura española y autonómica, Funcas Europe, encuestas sociales, notas técnicas, revistas y libros
- **Motivo de inclusión y uso:** Seguimiento de la economía española; consenso de previsiones. AC-MAC con foco España.
- **Sesgos y cautelas:** Vinculada al sector de cajas de ahorros (CECA).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Funcas Fedea CIDOB EsadeEcPol think tanks economía España»; WebFetch: sí, página «About us»)
- **Origen:** Alta F9_S3 (2026-11-02).

#### RF-0443 · Q 76 (B) — Comisión Europea — Strategic Foresight Report

- **Canal oficial (URL raíz):** https://commission.europa.eu/strategy-and-policy/strategic-foresight_et
- **Emisor:** Comisión Europea (Secretaría General, con apoyo del Joint Research Centre)
- **Temática:** TF-14 Think tanks y prospectiva (principal) · secundarias: TF-01
- **Calidad Q:** 76 (B) — Primariedad 16/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 14/15 · Independencia 8/10 · Actualidad 6/10 · Acceso 10/10
- **Tipología:** primaria (documento oficial de prospectiva)
- **Acceso:** Abierto
- **Ámbitos:** Informes anuales de prospectiva estratégica; 2025: «Resilience 2.0», horizonte 2040
- **Motivo de inclusión y uso:** Marco oficial de megatendencias que orienta prioridades de política de la UE. AC-ESC.
- **Sesgos y cautelas:** Documento político-institucional; periodicidad anual.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «EU Strategic Foresight Report ESPAS Global Trends OECD strategic foresight»; WebFetch: sí)
- **Origen:** Alta F9_S3 (2026-11-02).

#### RF-0097 · Q 75 (B) — World Economic Forum — Global Risks Report

- **Canal oficial (URL raíz):** https://weforum.org/publications/global-risks-report-2026
- **Emisor:** World Economic Forum
- **Temática:** TF-14 Think tanks y prospectiva (principal) · secundarias: TF-01
- **Calidad Q:** 75 (B) — Primariedad 16/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 13/15 · Independencia 7/10 · Actualidad 8/10 · Acceso 9/10
- **Tipología:** secundaria
- **Acceso:** Abierto
- **Ámbitos:** Percepción de riesgos globales a corto (2026), medio (2028) y largo plazo (2036); 21.ª edición con más de 1.300 expertos en la encuesta GRPS
- **Motivo de inclusión y uso:** Encuesta anual de percepción de riesgos; útil como medida de consenso.
- **Sesgos y cautelas:** Encuesta de percepción, no de probabilidad; financiación empresarial.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Real Instituto Elcano CSIS McKinsey Global Institute WEF Global Risks Report 2026»; WebFetch: sí)
- **Origen:** Semilla V3.0 (2026-11-01) confirmada por BFA en F9_S3 (2026-11-02).

#### RF-0439 · Q 75 (B) — Fedea — Fundación de Estudios de Economía Aplicada

- **Canal oficial (URL raíz):** https://fedea.net/
- **Emisor:** Fedea (fundada en 1985)
- **Temática:** TF-14 Think tanks y prospectiva (principal)
- **Calidad Q:** 75 (B) — Primariedad 15/20 · Historial 10/20 · Transparencia 11/15 · Autoridad 13/15 · Independencia 7/10 · Actualidad 9/10 · Acceso 10/10
- **Tipología:** secundaria (con datos y observatorios propios)
- **Acceso:** Abierto
- **Ámbitos:** Economía española: empleo, vivienda, sanidad, pensiones, financiación autonómica; Documentos Fedea, Observatorios, Datos, España en cifras; aloja Nada es Gratis
- **Motivo de inclusión y uso:** Análisis aplicado y propuestas de reforma para España. AC-MAC con foco España.
- **Sesgos y cautelas:** Financiación de miembros protectores (empresas); la página no detalla financiadores.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Nada es Gratis blog economía Fedea»; WebFetch: sí, página «What does Fedea do?»)
- **Origen:** Alta F9_S3 (2026-11-02).

#### RF-0091 · Q 74 (B) — Brookings Institution

- **Canal oficial (URL raíz):** https://www.brookings.edu/
- **Emisor:** Brookings Institution (fundada en 1916)
- **Temática:** TF-14 Think tanks y prospectiva (principal)
- **Calidad Q:** 74 (B) — Primariedad 14/20 · Historial 10/20 · Transparencia 11/15 · Autoridad 14/15 · Independencia 7/10 · Actualidad 8/10 · Acceso 10/10
- **Tipología:** secundaria
- **Acceso:** Abierto
- **Ámbitos:** Política económica, fiscal y monetaria (Hutchins Center), geopolítica
- **Motivo de inclusión y uso:** Think tank de referencia en política económica de EE. UU.
- **Sesgos y cautelas:** Financiación privada y de gobiernos extranjeros con controversias documentadas (Qatar, 2014; Huawei, 2012-2018; dimisión de su presidente en 2022 por una investigación del FBI sobre presión a favor de Qatar).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Wikipedia list of think tanks»; WebFetch: sí, listado y artículo de Wikipedia; URL oficial confirmada en la ficha de Wikipedia leída con WebFetch a partir del listado devuelto por la búsqueda (lectura lateral); la web oficial no se cargó)
- **Origen:** Semilla V3.0 (2026-11-01) confirmada por BFA en F9_S3 (2026-11-02). Q corregida de 76 a 74 (independencia 7/10 y transparencia 11/15 por las controversias de financiación).

#### RF-0430 · Q 74 (B) — RAND Corporation

- **Canal oficial (URL raíz):** https://www.rand.org/
- **Emisor:** RAND Corporation (fundada en 1948)
- **Temática:** TF-14 Think tanks y prospectiva (principal)
- **Calidad Q:** 74 (B) — Primariedad 14/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 14/15 · Independencia 7/10 · Actualidad 7/10 · Acceso 10/10
- **Tipología:** secundaria
- **Acceso:** Abierto
- **Ámbitos:** Seguridad, defensa, tecnología, economía, salud; análisis de escenarios
- **Motivo de inclusión y uso:** Análisis de escenarios y prospectiva en seguridad y tecnología. AC-GEO, AC-ESC.
- **Sesgos y cautelas:** Unos 328 M USD de sus 514 M USD de ingresos (2024) proceden del Gobierno federal de EE. UU.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Wikipedia list of think tanks»; WebFetch: sí, listado y artículo de Wikipedia; URL oficial confirmada en la ficha de Wikipedia leída con WebFetch a partir del listado devuelto por la búsqueda (lectura lateral); la web oficial no se cargó)
- **Origen:** Alta F9_S3 (2026-11-02).

#### RF-0431 · Q 74 (B) — Carnegie Endowment for International Peace

- **Canal oficial (URL raíz):** https://carnegieendowment.org/
- **Emisor:** Carnegie Endowment for International Peace (fundado en 1910)
- **Temática:** TF-14 Think tanks y prospectiva (principal)
- **Calidad Q:** 74 (B) — Primariedad 13/20 · Historial 10/20 · Transparencia 11/15 · Autoridad 14/15 · Independencia 8/10 · Actualidad 8/10 · Acceso 10/10
- **Tipología:** secundaria
- **Acceso:** Abierto
- **Ámbitos:** Geopolítica, China, Rusia y Eurasia, Oriente Medio, India, Europa, tecnología
- **Motivo de inclusión y uso:** Red global de centros (Pekín, Beirut, Bruselas, Nueva Delhi, Berlín) para riesgo geopolítico.
- **Sesgos y cautelas:** Financiación por dotación propia y donaciones.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Wikipedia list of think tanks»; WebFetch: sí, listado y artículo de Wikipedia; URL oficial confirmada en la ficha de Wikipedia leída con WebFetch a partir del listado devuelto por la búsqueda (lectura lateral); la web oficial no se cargó)
- **Origen:** Alta F9_S3 (2026-11-02).

#### RF-0094 · Q 73 (B) — Real Instituto Elcano

- **Canal oficial (URL raíz):** https://www.realinstitutoelcano.org/
- **Emisor:** Real Instituto Elcano de Estudios Internacionales y Estratégicos
- **Temática:** TF-14 Think tanks y prospectiva (principal) · secundarias: TF-01
- **Calidad Q:** 73 (B) — Primariedad 14/20 · Historial 10/20 · Transparencia 11/15 · Autoridad 12/15 · Independencia 8/10 · Actualidad 8/10 · Acceso 10/10
- **Tipología:** secundaria
- **Acceso:** Abierto
- **Ámbitos:** Geopolítica, riesgo país, energía, perspectiva española; series ARI, documentos de trabajo, Índice Elcano de Presencia Global
- **Motivo de inclusión y uso:** Análisis geopolítico en español.
- **Sesgos y cautelas:** Patronato con empresas y Estado (socios protectores y colaboradores).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Real Instituto Elcano realinstitutoelcano.org análisis»; WebFetch: sí)
- **Origen:** Semilla V3.0 (2026-11-01) confirmada por BFA en F9_S3 (2026-11-02).

#### RF-0437 · Q 73 (B) — Committee for a Responsible Federal Budget (CRFB)

- **Canal oficial (URL raíz):** https://www.crfb.org/
- **Emisor:** CRFB (fundado en 1981)
- **Temática:** TF-14 Think tanks y prospectiva (principal) · secundarias: TF-01
- **Calidad Q:** 73 (B) — Primariedad 14/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 12/15 · Independencia 6/10 · Actualidad 9/10 · Acceso 10/10
- **Tipología:** secundaria
- **Acceso:** Abierto
- **Ámbitos:** Déficit y deuda federal de EE. UU., estimaciones del coste de propuestas legislativas
- **Motivo de inclusión y uso:** Seguimiento de la trayectoria fiscal de EE. UU. y del riesgo soberano. AC-RF.
- **Sesgos y cautelas:** Orientación declarada a la reducción del déficit; vínculos con la Peter G. Peterson Foundation.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Wikipedia list of think tanks»; WebFetch: sí, listado y artículo de Wikipedia (EE. UU.); URL oficial confirmada en la ficha de Wikipedia leída con WebFetch a partir del listado devuelto por la búsqueda (lectura lateral); la web oficial no se cargó)
- **Origen:** Alta F9_S3 (2026-11-02).

#### RF-0444 · Q 73 (B) — ESPAS — Global Trends to 2040

- **Canal oficial (URL raíz):** https://espas.eu/files/espas_files/about/ESPAS-Global-Trends-to-2040-Choosing-Europes-Future.pdf
- **Emisor:** European Strategy and Policy Analysis System (nueve instituciones y órganos de la UE)
- **Temática:** TF-14 Think tanks y prospectiva (principal)
- **Calidad Q:** 73 (B) — Primariedad 15/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 14/15 · Independencia 8/10 · Actualidad 4/10 · Acceso 10/10
- **Tipología:** primaria (informe interinstitucional de prospectiva)
- **Acceso:** Abierto
- **Ámbitos:** Diez megatendencias a 2040: geopolítica, economía, demografía, clima, energía, desigualdad, tecnología, salud, trabajo, democracia; 4.º informe (abril de 2024)
- **Motivo de inclusión y uso:** Marco de megatendencias de largo plazo para escenarios. AC-ESC.
- **Sesgos y cautelas:** Periodicidad plurianual; enfoque político-institucional.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «EU Strategic Foresight Report ESPAS Global Trends OECD strategic foresight»; WebFetch: sí)
- **Origen:** Alta F9_S3 (2026-11-02).

#### RF-0428 · Q 72 (B) — Council on Foreign Relations (CFR)

- **Canal oficial (URL raíz):** https://www.cfr.org/
- **Emisor:** Council on Foreign Relations (fundado en 1921)
- **Temática:** TF-14 Think tanks y prospectiva (principal)
- **Calidad Q:** 72 (B) — Primariedad 13/20 · Historial 10/20 · Transparencia 11/15 · Autoridad 14/15 · Independencia 7/10 · Actualidad 8/10 · Acceso 9/10
- **Tipología:** secundaria
- **Acceso:** Abierto (Foreign Affairs con muro parcial)
- **Ámbitos:** Política exterior, geoeconomía, informes de Independent Task Forces; revista Foreign Affairs
- **Motivo de inclusión y uso:** Análisis de política exterior de EE. UU. y riesgos geopolíticos.
- **Sesgos y cautelas:** Financiación de fundaciones y grandes donantes (críticas por una donación de 12 M USD en 2019).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Wikipedia list of think tanks»; WebFetch: sí, listado y artículo de Wikipedia; URL oficial confirmada en la ficha de Wikipedia leída con WebFetch a partir del listado devuelto por la búsqueda (lectura lateral); la web oficial no se cargó)
- **Origen:** Alta F9_S3 (2026-11-02).

#### RF-0095 · Q 71 (B) — CSIS — Center for Strategic and International Studies

- **Canal oficial (URL raíz):** https://www.csis.org/
- **Emisor:** CSIS (fundado en 1962; independiente desde 1987)
- **Temática:** TF-14 Think tanks y prospectiva (principal)
- **Calidad Q:** 71 (B) — Primariedad 13/20 · Historial 10/20 · Transparencia 11/15 · Autoridad 13/15 · Independencia 6/10 · Actualidad 8/10 · Acceso 10/10
- **Tipología:** secundaria
- **Acceso:** Abierto
- **Ámbitos:** Geopolítica, seguridad económica, cadenas de suministro críticas, tecnología
- **Motivo de inclusión y uso:** Análisis geoeconómico (controles de exportación, minerales críticos).
- **Sesgos y cautelas:** Financiación de contratistas de defensa (Northrop Grumman, Lockheed Martin, Boeing, entre otros), empresas energéticas y gobiernos extranjeros; críticas documentadas por presión a favor de donantes (NYT, 2016).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Wikipedia list of think tanks»; WebFetch: sí, listado y artículo de Wikipedia; URL oficial confirmada en la ficha de Wikipedia leída con WebFetch a partir del listado devuelto por la búsqueda (lectura lateral); la web oficial no se cargó)
- **Origen:** Semilla V3.0 (2026-11-01) confirmada por BFA en F9_S3 (2026-11-02). Q corregida de 72 a 71 (independencia 6/10).

#### RF-0440 · Q 71 (B) — EsadeEcPol — Center for Economic Policy

- **Canal oficial (URL raíz):** https://www.esade.edu/ecpol/en/about-us/
- **Emisor:** Esade (Universidad Ramon Llull)
- **Temática:** TF-14 Think tanks y prospectiva (principal)
- **Calidad Q:** 71 (B) — Primariedad 13/20 · Historial 10/20 · Transparencia 10/15 · Autoridad 12/15 · Independencia 7/10 · Actualidad 9/10 · Acceso 10/10
- **Tipología:** secundaria
- **Acceso:** Abierto
- **Ámbitos:** Políticas públicas basadas en evidencia en España; Policy Impact Lab (evaluaciones cuantitativas y experimentos)
- **Motivo de inclusión y uso:** Evaluación de políticas públicas españolas.
- **Sesgos y cautelas:** La página no detalla la financiación.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Funcas Fedea CIDOB EsadeEcPol think tanks economía España»; WebFetch: sí, página «About us»)
- **Origen:** Alta F9_S3 (2026-11-02).

#### RF-0429 · Q 70 (B) — Chatham House (Royal Institute of International Affairs)

- **Canal oficial (URL raíz):** https://www.chathamhouse.org/
- **Emisor:** Chatham House (fundado en 1920)
- **Temática:** TF-14 Think tanks y prospectiva (principal)
- **Calidad Q:** 70 (B) — Primariedad 13/20 · Historial 10/20 · Transparencia 10/15 · Autoridad 14/15 · Independencia 7/10 · Actualidad 8/10 · Acceso 8/10
- **Tipología:** secundaria
- **Acceso:** Abierto (parte para miembros)
- **Ámbitos:** Geopolítica, energía, economía global, riesgo país
- **Motivo de inclusión y uso:** Análisis geopolítico y energético europeo.
- **Sesgos y cautelas:** Miembros corporativos de energía, finanzas y defensa; divulgación de financiación limitada (Who Funds You?: B en 2024).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Wikipedia list of think tanks»; WebFetch: sí, listado de think tanks del Reino Unido y artículo de Wikipedia; URL oficial confirmada en la ficha de Wikipedia leída con WebFetch a partir del listado devuelto por la búsqueda (lectura lateral); la web oficial no se cargó)
- **Origen:** Alta F9_S3 (2026-11-02).

#### RF-0441 · Q 70 (B) — CIDOB — Barcelona Centre for International Affairs

- **Canal oficial (URL raíz):** https://www.cidob.org/
- **Emisor:** CIDOB
- **Temática:** TF-14 Think tanks y prospectiva (principal)
- **Calidad Q:** 70 (B) — Primariedad 12/20 · Historial 10/20 · Transparencia 11/15 · Autoridad 12/15 · Independencia 7/10 · Actualidad 8/10 · Acceso 10/10
- **Tipología:** secundaria
- **Acceso:** Abierto
- **Ámbitos:** Relaciones internacionales y gobernanza global; Anuario Internacional, Notes Internacionals, Revista CIDOB d'Afers Internacionals
- **Motivo de inclusión y uso:** Análisis internacional desde España (Barcelona).
- **Sesgos y cautelas:** Financiación pública y privada no detallada en la página.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Funcas Fedea CIDOB EsadeEcPol think tanks economía España»; WebFetch: sí)
- **Origen:** Alta F9_S3 (2026-11-02).

#### RF-0096 · Q 69 (B) — McKinsey Global Institute

- **Canal oficial (URL raíz):** https://www.mckinsey.com/mgi
- **Emisor:** McKinsey & Company (MGI, fundado en 1990)
- **Temática:** TF-14 Think tanks y prospectiva (principal)
- **Calidad Q:** 69 (B) — Primariedad 13/20 · Historial 10/20 · Transparencia 10/15 · Autoridad 13/15 · Independencia 7/10 · Actualidad 8/10 · Acceso 8/10
- **Tipología:** secundaria
- **Acceso:** Abierto (registro para algunos informes)
- **Ámbitos:** Productividad, tecnología, demografía, comercio, mercados de capitales, salud
- **Motivo de inclusión y uso:** Estudios de tendencias de largo plazo con estimaciones cuantitativas.
- **Sesgos y cautelas:** Brazo de investigación de una consultora; declara que sus informes no están encargados ni pagados por terceros, pero lo dirigen socios de McKinsey; estimaciones a veces optimistas.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «McKinsey Global Institute research reports mckinsey.com/mgi»; WebFetch: sí, resumen ejecutivo de MGI en mckinsey.com; la URL raíz /mgi no salió literalmente en los resultados)
- **Origen:** Semilla V3.0 (2026-11-01) confirmada por BFA en F9_S3 (2026-11-02).

#### RF-0436 · Q 67 (B) — Centre for European Reform (CER)

- **Canal oficial (URL raíz):** https://www.cer.eu/
- **Emisor:** Centre for European Reform (fundado en 1996)
- **Temática:** TF-14 Think tanks y prospectiva (principal)
- **Calidad Q:** 67 (B) — Primariedad 12/20 · Historial 10/20 · Transparencia 9/15 · Autoridad 12/15 · Independencia 6/10 · Actualidad 8/10 · Acceso 10/10
- **Tipología:** secundaria
- **Acceso:** Abierto
- **Ámbitos:** Integración europea, economía de la UE, relaciones UE-Reino Unido
- **Motivo de inclusión y uso:** Análisis de política europea.
- **Sesgos y cautelas:** Financiación empresarial significativa; posiciones tendentes a la desregulación.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Wikipedia list of think tanks»; WebFetch: sí, listado de think tanks del Reino Unido y artículo de Wikipedia; URL oficial confirmada en la ficha de Wikipedia leída con WebFetch a partir del listado devuelto por la búsqueda (lectura lateral); la web oficial no se cargó)
- **Origen:** Alta F9_S3 (2026-11-02).

#### RF-0432 · Q 66 (B) — Atlantic Council — GeoEconomics Center

- **Canal oficial (URL raíz):** https://www.atlanticcouncil.org/
- **Emisor:** Atlantic Council (fundado en 1961)
- **Temática:** TF-14 Think tanks y prospectiva (principal)
- **Calidad Q:** 66 (B) — Primariedad 12/20 · Historial 10/20 · Transparencia 9/15 · Autoridad 12/15 · Independencia 5/10 · Actualidad 8/10 · Acceso 10/10
- **Tipología:** secundaria (con monitores propios)
- **Acceso:** Abierto
- **Ámbitos:** Geoeconomía: futuro del dinero (monedas digitales), sanciones, economía de China, sistema de Bretton Woods
- **Motivo de inclusión y uso:** Seguimiento de sanciones y de monedas digitales de banco central.
- **Sesgos y cautelas:** Mayor financiación de gobiernos extranjeros entre los think tanks de EE. UU. (2019-2023, Quincy Institute); controversias de donantes.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Wikipedia list of think tanks»; WebFetch: sí, listado y artículo de Wikipedia; URL oficial confirmada en la ficha de Wikipedia leída con WebFetch a partir del listado devuelto por la búsqueda (lectura lateral); la web oficial no se cargó)
- **Origen:** Alta F9_S3 (2026-11-02).

#### RF-0446 · Q 63 (C) — Good Judgment Inc (Superforecasters)

- **Canal oficial (URL raíz):** https://goodjudgment.com/
- **Emisor:** Good Judgment Inc
- **Temática:** TF-14 Think tanks y prospectiva (principal) · secundarias: TF-12
- **Calidad Q:** 63 (C) — Primariedad 12/20 · Historial 10/20 · Transparencia 9/15 · Autoridad 12/15 · Independencia 6/10 · Actualidad 9/10 · Acceso 5/10
- **Tipología:** secundaria (pronósticos agregados de superpronosticadores)
- **Acceso:** Restringido (FutureFirst y pronósticos a medida de pago; resúmenes públicos)
- **Ámbitos:** Pronósticos probabilísticos sobre geopolítica, política monetaria y macro
- **Motivo de inclusión y uso:** Contraste de probabilidades de escenarios con un grupo de pronosticadores de historial medido. AC-ESC.
- **Sesgos y cautelas:** Empresa comercial; el historial publicado lo presenta la propia empresa (p. ej., 66 % más precisos que los futuros en puntos de giro de la Fed; 554 preguntas resueltas a septiembre de 2023), sin auditoría independiente en la página.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Metaculus Good Judgment superforecasters forecasting track record»; WebFetch: sí, página «The Superforecasters’ Track Record»)
- **Origen:** Alta F9_S3 (2026-11-02).

## TF-15 Proveedores de índices y metodologías

#### RF-0500 · Q 84 (A) — MSCI — Market Classification (revisión anual de clasificación de mercados y Global Market Accessibility Review)

- **Canal oficial (URL raíz):** https://www.msci.com/market-classification (enlazada desde la nota de 18/06/2026 en el canal de relación con inversores: https://ir.msci.com/node/22776)
- **Emisor:** MSCI Inc.
- **Documentación y notas:** Marco de clasificación de mercados (desarrollados, emergentes, frontera, standalone); revisión anual con resultados en junio (2026: 23/06/2026) precedida por la Global Market Accessibility Review (18/06/2026: 79 mercados, 5 criterios y 18 medidas de accesibilidad: apertura a la propiedad extranjera, facilidad de entradas y salidas de capital, eficiencia operativa, disponibilidad de instrumentos y estabilidad institucional). En 2026, Bulgaria en revisión de Standalone a Frontera. Canal hermano de RF-0054 (metodologías), que no cubre las reclasificaciones.
- **Temática:** TF-15 Proveedores de índices y metodologías (principal) · secundarias: TF-06
- **Calidad Q:** 84 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 7/10 · Actualidad 9/10 · Acceso 9/10
- **Tipología:** primaria (decisión del administrador del índice)
- **Acceso:** Abierto (notas y resumen); detalle completo de la revisión de accesibilidad en PDF abierto
- **Ámbitos:** Reclasificaciones de países (ascensos y descensos, listas de consulta), accesibilidad de mercados, calendario de efectividad
- **Motivo de inclusión y uso:** Las reclasificaciones de MSCI mueven flujos pasivos de gran tamaño hacia o desde un país; señal temprana (lista de consulta) y fecha de efectividad. AG-21: oportunidades por reclasificación de mercados; AG-22: flujos de ETF regionales.
- **Restricciones de uso:** Uso con atribución; datos de índices bajo licencia.
- **Sesgos y cautelas:** Decisión discrecional con consulta a grandes clientes; el anuncio no equivale a la efectividad (suele haber 12 meses o más de transición).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «MSCI annual market classification review 2026 results»; WebFetch: sí, nota en ir.msci.com)
- **Origen:** Alta F9_S4 (2026-11-02).

#### RF-0501 · Q 84 (A) — FTSE Russell — Equity Country Classification (revisión anual de septiembre e intermedia de marzo)

- **Canal oficial (URL raíz):** https://www.lseg.com/en/ftse-russell/equity-country-classification (nota de resultados de septiembre de 2026: https://www.lseg.com/en/media-centre/press-releases/ftse-russell/2026/ftse-country-classification-review-september-2026)
- **Emisor:** FTSE Russell (LSEG)
- **Documentación y notas:** Clasificación de países en desarrollados, emergentes avanzados, emergentes secundarios y frontera, con lista de vigilancia (Watch List); revisión anual en septiembre e intermedia en marzo; PDF de actualización anual e intermedia (ftse-country-classification-update-2026.pdf, ftse-interim-country-classification-review-2026.pdf). Resultados de la revisión de septiembre de 2026 (publicados el 06/10/2026): Grecia a desarrollado, Vietnam de frontera a emergente secundario, Nigeria a frontera, Egipto sale de la lista de vigilancia de descenso y Omán entra en la de ascenso; próxima actualización en abril de 2027. Canal hermano de RF-0055 (metodologías).
- **Temática:** TF-15 Proveedores de índices y metodologías (principal) · secundarias: TF-06
- **Calidad Q:** 84 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 7/10 · Actualidad 9/10 · Acceso 9/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** Reclasificación de mercados de renta variable y renta fija; criterios de calidad de mercado
- **Motivo de inclusión y uso:** Junto con RF-0500, detecta cambios de categoría de países que generan flujos indexados. AG-21 y AG-22.
- **Restricciones de uso:** Uso con atribución.
- **Sesgos y cautelas:** Criterios de calidad de mercado parcialmente cualitativos; fechas de efectividad escalonadas.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Integrado en LSEG (antes London Stock Exchange Group/Refinitiv).
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «FTSE Russell equity country classification September 2026 annual review watch list»; WebFetch: sí, nota de prensa)
- **Origen:** Alta F9_S4 (2026-11-02).

#### RF-0502 · Q 83 (A) — STOXX — Rulebooks (guías de metodología de STOXX, DAX e iSTOXX) y anuncios de revisiones

- **Canal oficial (URL raíz):** https://stoxx.com/rulebooks
- **Emisor:** STOXX Ltd. (ISS STOXX, grupo Deutsche Börse)
- **Documentación y notas:** Guías vinculantes de desarrollo, cálculo, revisión y ajuste: guías armonizadas (clasificación sectorial, cálculo, iNAV, Quality Charter), STOXX (Investable Market, World Equity, estrategia, activos digitales, renta fija ICE), DAX (DAX Equity y Strategy, guía de cálculo, eb.rexx, EUROGOV, REX) y ECPI. Menús de anuncios (actualizaciones de índices, metodología: stoxx.com/methodology) y de datos (información de revisiones periódicas, listas de selección, informes de revisión, operaciones corporativas). Administra EURO STOXX 50, DAX y los índices de volatilidad VSTOXX.
- **Temática:** TF-15 Proveedores de índices y metodologías (principal) · secundarias: TF-17
- **Calidad Q:** 83 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 15/15 · Autoridad 14/15 · Independencia 7/10 · Actualidad 9/10 · Acceso 8/10
- **Tipología:** primaria
- **Acceso:** Abierto (guías y anuncios); datos de composición detallados bajo licencia
- **Ámbitos:** Índices europeos y globales de renta variable, DAX, volatilidad (VSTOXX), renta fija y temáticos
- **Motivo de inclusión y uso:** Reglas y calendario de revisiones de los índices de referencia europeos; listas de selección para anticipar entradas y salidas. AG-21.
- **Restricciones de uso:** Uso con atribución; datos de índices bajo licencia.
- **Sesgos y cautelas:** Proveedor comercial que licencia sus índices a emisores de ETF y derivados.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Fusión de STOXX con ISS (ISS STOXX, 2023) y absorción de la marca Qontigo; la familia DAX pasó a la gestión de STOXX.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «STOXX index methodology guide rulebook stoxx.com»; WebFetch: sí)
- **Origen:** Alta F9_S4 (2026-11-02).

#### RF-0503 · Q 83 (A) — JPX Market Innovation & Research — TOPIX (guía, revisiones periódicas y consultas)

- **Canal oficial (URL raíz):** https://www.jpx.co.jp/english/markets/indices/topix/index.html (consultas: https://www.jpx.co.jp/english/markets/indices/governance/index-consultation/20260129-01.html)
- **Emisor:** JPX Market Innovation & Research, Inc. (Japan Exchange Group)
- **Documentación y notas:** TOPIX (capitalización ajustada por free float, base 100 el 04/01/1968); Tokyo Stock Exchange Index Guidebook (TOPIX) y metodología de free float; anuncios de revisión periódica (p. ej., 07/10/2026 sobre revisión periódica y selección inicial de constituyentes), revisión estructural de TOPIX con reducción escalonada de constituyentes y nuevas series (tamaño, estilo, dividendo; 27/09/2024); consultas públicas de índices.
- **Temática:** TF-15 Proveedores de índices y metodologías (principal) · secundarias: —
- **Calidad Q:** 83 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 8/10 · Actualidad 8/10 · Acceso 8/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** Renta variable japonesa; revisiones de constituyentes y pesos (free float)
- **Motivo de inclusión y uso:** Referencia del mercado japonés para flujos pasivos (incluidas compras históricas de ETF del Banco de Japón) y efecto de la reforma de TOPIX. AG-21.
- **Restricciones de uso:** Uso con atribución; datos de índice bajo licencia.
- **Sesgos y cautelas:** Propiedad de la bolsa (conflicto entre administrador y operador de mercado).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Reforma de TOPIX en fases desde 2022 (reducción de ponderación de constituyentes de menor liquidez).
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «JPX Market Innovation & Research TOPIX index guidebook review of TOPIX»; WebFetch: sí)
- **Origen:** Alta F9_S4 (2026-11-02).

#### RF-0504 · Q 82 (A) — BME (Sociedad de Bolsas) — índices IBEX: normas técnicas y avisos del Comité Asesor Técnico

- **Canal oficial (URL raíz):** https://www.bolsasymercados.es/bme-exchange/docs/docsSubidos/Indices/Regulacion/Normas_Indices_Ibex_esp.pdf (avisos del Comité, p. ej.: https://www.bolsasymercados.es/bme-exchange/docs/Indices/Avisos/esp/comiteasesor/Aviso_Comite_IBEX_01-26.pdf)
- **Emisor:** Sociedad de Bolsas, S.A. (BME, grupo SIX)
- **Documentación y notas:** «Normas técnicas para la composición y cálculo de los Índices IBEX y de Estrategia sobre Acciones» (versión de enero de 2025): Comité Asesor Técnico de 5 a 9 miembros, reuniones ordinarias semestrales y de seguimiento en los otros trimestres, efectividad el día hábil siguiente al tercer viernes; IBEX 35 (35 valores más líquidos del SIBE, umbral de capitalización del 0,30 %, ajuste por free float, tope del 20 %), IBEX Medium Cap, Small Cap, Top Dividendo, índices sectoriales, apalancados e inversos, de estrategia de opciones (VIBEX, SKEW) y ESG. Los avisos del Comité publican altas, bajas y coeficientes.
- **Temática:** TF-15 Proveedores de índices y metodologías (principal) · secundarias: TF-17
- **Calidad Q:** 82 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 14/15 · Independencia 7/10 · Actualidad 9/10 · Acceso 8/10
- **Tipología:** primaria
- **Acceso:** Abierto (PDF)
- **Ámbitos:** Renta variable española; revisiones del IBEX 35 y familia IBEX
- **Motivo de inclusión y uso:** Fuente primaria de las reglas y decisiones de composición del índice de referencia español. AG-21; AG-23 (subyacente de futuros y opciones de MEFF).
- **Restricciones de uso:** Uso con atribución; marcas IBEX registradas.
- **Sesgos y cautelas:** El administrador pertenece al operador del mercado (SIX); las decisiones del Comité tienen margen discrecional.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** BME integrada en SIX Group (2020).
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Comité Asesor Técnico IBEX 35 normas técnicas bolsasymercados.es índices revisión»; WebFetch: sí, PDF de normas técnicas)
- **Origen:** Alta F9_S4 (2026-11-02).

#### RF-0510 · Q 82 (A) — Nasdaq Global Indexes — metodologías (Nasdaq-100 y otros) y reconstitución anual

- **Canal oficial (URL raíz):** https://indexes.nasdaq.com/ (metodología del Nasdaq-100: https://indexes.NASDAQomx.com/docs/Methodology_NDX.pdf · balance de la reconstitución de enero de 2026: https://indexes.nasdaqomx.com/docs/202601%20NDX%20Reconstitution%20and%20Performance%20Highlights.pdf · consulta de noviembre de 2023: https://indexes.nasdaq.com/docs/NDX%20Index%20Consultation%20November%202023%20-%20Final.pdf)
- **Emisor:** Nasdaq, Inc. (Nasdaq Global Indexes)
- **Documentación y notas:** Repositorio de metodologías por índice (NDX, NDXT, NDXX, NDXESG, NDXMEGA, NGX, NDXLV, etc.), versiones con cambios marcados (redline), consultas de índice y notas de reconstitución anual del Nasdaq-100 (diciembre) con su balance de rendimiento; anuncios de cambios anuales en nasdaq.com.
- **Temática:** TF-15 Proveedores de índices y metodologías (principal) · secundarias: TF-17
- **Calidad Q:** 82 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 14/15 · Independencia 7/10 · Actualidad 9/10 · Acceso 8/10
- **Tipología:** primaria
- **Acceso:** Abierto (PDF de metodología y anuncios)
- **Ámbitos:** Renta variable de EE. UU. de gran capitalización no financiera y tecnológica; índices temáticos
- **Motivo de inclusión y uso:** Reglas de concentración, reequilibrios especiales y reconstitución del Nasdaq-100 (subyacente de grandes ETF y derivados). AG-21, AG-23.
- **Restricciones de uso:** Uso con atribución; marcas registradas.
- **Sesgos y cautelas:** El administrador es operador de bolsa (incentivo a mantener listados). No se pudo cargar el PDF en esta sesión (error del sitio); confirmado en resultados de búsqueda.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Consulta de 2023 sobre reglas de ponderación del Nasdaq-100.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Nasdaq Global Indexes methodology Nasdaq-100 annual reconstitution indexes.nasdaqomx.com»; WebFetch: intento fallido, error del sitio)
- **Origen:** Alta F9_S4 (2026-11-02).

#### RF-0505 · Q 81 (A) — Bloomberg Index Services — metodología de índices de renta fija (Global Aggregate, US Aggregate y otros)

- **Canal oficial (URL raíz):** https://data.bloomberglp.com/professional/sites/10/Bloomberg-Index-Publications-Fixed-Income-Index-Methodology.pdf
- **Emisor:** Bloomberg Index Services Limited (BISL)
- **Documentación y notas:** «Bloomberg Fixed Income Index Methodology» (08/01/2026): reglas de elegibilidad (divisa, sector, calidad, importe vivo, vencimiento, país, mercado de emisión), universos Projected y Returns, reequilibrio mensual, precios y rentabilidades; familias Global Aggregate, US Aggregate, Pan-European, Asian-Pacific, EM Local Currency Government (inclusión escalonada de bonos FAR de la India desde enero de 2025), WGILB, High Yield, municipales y Global Leveraged Loan (julio de 2025); revisiones anuales de elegibilidad de mercados; gobierno según el Benchmark Procedures Handbook.
- **Temática:** TF-15 Proveedores de índices y metodologías (principal) · secundarias: TF-19
- **Calidad Q:** 81 (A) — Primariedad 19/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 7/10 · Actualidad 9/10 · Acceso 7/10
- **Tipología:** primaria
- **Acceso:** Metodología abierta; niveles y composición de índices bajo licencia (terminal)
- **Ámbitos:** Índices de referencia de renta fija global; inclusión de mercados locales emergentes
- **Motivo de inclusión y uso:** Reglas de los índices de bonos más replicados; anticipar flujos por inclusión de países o cambios de elegibilidad. AG-21, AG-25.
- **Restricciones de uso:** Uso con atribución; datos bajo licencia.
- **Sesgos y cautelas:** Proveedor comercial; documentos índice-específicos prevalecen en detalles.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Antiguos índices Lehman y Bloomberg Barclays (marca Barclays retirada en 2021).
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Bloomberg Indices methodology Bloomberg Global Aggregate index rules index announcements»; WebFetch: sí, PDF de metodología)
- **Origen:** Alta F9_S4 (2026-11-02).

#### RF-0511 · Q 81 (A) — NSE Indices (Nifty Indices) — metodologías, libros blancos y revisiones semestrales

- **Canal oficial (URL raíz):** https://www.niftyindices.com/ (libro blanco Nifty 50, marzo de 2026: https://niftyindices.com/docs/default-source/indices/nifty-50/nifty-50-whitepaper_2026.pdf · fichas: https://www.niftyindices.com/Factsheet/Ind_Nifty50.pdf)
- **Emisor:** NSE Indices Limited (antes India Index Services & Products Ltd.), filial de National Stock Exchange of India
- **Documentación y notas:** Libro blanco del 30 aniversario del Nifty 50: universo Nifty 100, requisitos de inclusión en el segmento de derivados, coste de impacto y negociación diaria; 50 mayores por free float medio de seis meses; revisiones semestrales (marzo y septiembre) con regla de entrada de 1,5 veces el menor constituyente; 45 fondos pasivos domésticos (unos 4,89 billones de rupias a 30/01/2026) y 23 internacionales; futuros desde 2000 y opciones desde 2001. Fichas y metodologías por índice.
- **Temática:** TF-15 Proveedores de índices y metodologías (principal) · secundarias: TF-17
- **Calidad Q:** 81 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 14/15 · Independencia 7/10 · Actualidad 8/10 · Acceso 8/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** Renta variable india; índices sectoriales, temáticos y de estrategia
- **Motivo de inclusión y uso:** Reglas y revisiones del índice de referencia de la India y datos de su ecosistema pasivo y de derivados. AG-21, AG-23.
- **Restricciones de uso:** Uso con atribución.
- **Sesgos y cautelas:** Filial del operador de bolsa; el libro blanco presenta cifras de fondos internacionales que no cuadran del todo entre resumen y anexo.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Cambio de denominación de IISL a NSE Indices Limited.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «NSE Indices Limited niftyindices.com Nifty 50 methodology semi-annual index review»; WebFetch: sí, libro blanco 2026)
- **Origen:** Alta F9_S4 (2026-11-02).

#### RF-0506 · Q 80 (A) — ICE Data Indices — metodologías de índices de bonos (ICE y ICE BofA)

- **Canal oficial (URL raíz):** https://www.ice.com/publicdocs/data/Bond_Index_Methodologies.pdf
- **Emisor:** ICE Data Indices, LLC (Intercontinental Exchange)
- **Documentación y notas:** «Bond Index Methodologies» (30/04/2025): reglas de los índices de bonos ICE e ICE BofA (soberanos, cuasi-gubernamentales, corporativos por vencimiento y calificación, CoCo, convertibles, MBS, ABS, CMBS, sintéticos y ESG/clima); reequilibrio mensual el último día natural con fecha de bloqueo tres días hábiles antes; revisión anual de reglas (propuestas en abril, decisión en julio, aplicación a fin de septiembre). Las series de diferenciales ICE BofA se redistribuyen en FRED (no cuentan como fuente independiente).
- **Temática:** TF-15 Proveedores de índices y metodologías (principal) · secundarias: TF-19
- **Calidad Q:** 80 (A) — Primariedad 19/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 14/15 · Independencia 7/10 · Actualidad 8/10 · Acceso 8/10
- **Tipología:** primaria
- **Acceso:** Metodología abierta; datos completos bajo licencia
- **Ámbitos:** Renta fija investment grade, high yield, emergentes, titulizaciones
- **Motivo de inclusión y uso:** Reglas de los índices de crédito más usados en diferenciales (OAS) y ETF de bonos. AG-21, AG-25.
- **Restricciones de uso:** Uso con atribución; datos bajo licencia.
- **Sesgos y cautelas:** Proveedor que también opera bolsas y cámaras (ICE): conflicto potencial.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Índices de Merrill Lynch/BofA adquiridos por ICE (2017).
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «ICE Data Indices ICE BofA bond index methodology index rules»; WebFetch: sí, PDF)
- **Origen:** Alta F9_S4 (2026-11-02).

#### RF-0507 · Q 80 (A) — Nikkei Indexes — Nikkei 225 y familia de índices Nikkei (guías y sala de prensa)

- **Canal oficial (URL raíz):** https://indexes.nikkei.co.jp/en/nkave/index/profile (sala de prensa: https://indexes.nikkei.co.jp/en/nkave/newsroom?idx=nk225 · guía: https://indexes.nikkei.co.jp/en/nkave/archives/file/nikkei_stock_average_guidebook_en.pdf)
- **Emisor:** Nikkei Inc.
- **Documentación y notas:** Nikkei 225: índice ponderado por precio de 225 valores del segmento Prime de la Bolsa de Tokio, calculado cada 5 segundos; revisión semestral de constituyentes (abril y octubre); guía de metodología (Nikkei Stock Average Guidebook) y avisos de cambios en la sala de prensa (p. ej., 20260709E_2.pdf).
- **Temática:** TF-15 Proveedores de índices y metodologías (principal) · secundarias: TF-17
- **Calidad Q:** 80 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 14/15 · Independencia 7/10 · Actualidad 8/10 · Acceso 8/10
- **Tipología:** primaria
- **Acceso:** Abierto (perfil, guías y avisos); datos históricos detallados bajo licencia
- **Ámbitos:** Renta variable japonesa; subyacente de futuros y opciones de Osaka
- **Motivo de inclusión y uso:** Revisión de constituyentes y factores de ajuste del índice japonés más negociado en derivados. AG-21, AG-23.
- **Restricciones de uso:** Uso con atribución; marca registrada.
- **Sesgos y cautelas:** La ponderación por precio sobrerrepresenta valores de cotización alta (concentración en pocos nombres).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Nikkei Indexes official site Nikkei 225 index guidebook periodic review»; WebFetch: sí, página de perfil)
- **Origen:** Alta F9_S4 (2026-11-02).

#### RF-0512 · Q 80 (A) — Euronext — índices CAC y familia Euronext (revisiones trimestrales del Index Steering Committee)

- **Canal oficial (URL raíz):** https://www.euronext.com/ (anuncio de revisión trimestral leído: https://www.euronext.com/news/euronext-announces-quarterly-review-results-cac-family-indices-0 · información de mercado del CAC 40: https://www.euronext.com/en/products/indices/FR0003500008-XPAR/market-information · notas de prensa de revisiones, p. ej., marzo de 2025: https://www.euronext.com/en/about/media/euronext-press-releases/euronext-announces-update-march-2025-quarterly-review-results)
- **Emisor:** Euronext N.V.
- **Documentación y notas:** Notas de prensa de resultados de las revisiones trimestrales de la familia CAC (CAC 40, CAC Next 20, CAC Large 60, SBF 120, CAC Mid & Small, CAC 40 ESG) con altas, bajas y fechas efectivas; referencias a las reglas de índices (Indices Rules) y gestión de eventos entre publicación y efectividad. Euronext administra también AEX, BEL 20, PSI, ISEQ y FTSE MIB (con FTSE Russell).
- **Temática:** TF-15 Proveedores de índices y metodologías (principal) · secundarias: —
- **Calidad Q:** 80 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 14/15 · Independencia 7/10 · Actualidad 8/10 · Acceso 8/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** Renta variable francesa, neerlandesa, belga, portuguesa, irlandesa e italiana
- **Motivo de inclusión y uso:** Decisiones de composición de los índices de referencia de los mercados Euronext. AG-21.
- **Restricciones de uso:** Uso con atribución; marcas registradas de Euronext.
- **Sesgos y cautelas:** Operador de bolsa como administrador; la página leída es un anuncio antiguo (marzo de 2019) usado como muestra del canal.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Integración de Borsa Italiana (2021) en el grupo.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Euronext indices CAC 40 rule book index advisory committee quarterly review live.euronext.com»; WebFetch: sí)
- **Origen:** Alta F9_S4 (2026-11-02).

#### RF-0513 · Q 79 (B) — SIX — índices suizos (SMI, SLI, SPI): revisiones ordinarias y mensajes de índices

- **Canal oficial (URL raíz):** https://www.six-group.com/ (revisión ordinaria de 2026: https://www.six-group.com/dam/download/market-data/indices/index-messages/index-adjustments-on-the-occasion-of-the-ordinary-index-review-2026.pdf)
- **Emisor:** SIX Group (SIX Swiss Exchange / SIX Index)
- **Documentación y notas:** Nota de 08/07/2026 sobre la revisión ordinaria anual por recomendación de la Index Commission: Galderma y Sandoz entran en el SMI y salen Swisscom y Kuehne+Nagel; cambios en SMIM y SPI; tope del 9 % en el SLI; ajuste el 18/09/2026 y efectividad el 21/09/2026. Mensajes de índices y reglas de SMI, SLI, SPI y SXI.
- **Temática:** TF-15 Proveedores de índices y metodologías (principal) · secundarias: —
- **Calidad Q:** 79 (B) — Primariedad 20/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 14/15 · Independencia 7/10 · Actualidad 9/10 · Acceso 7/10
- **Tipología:** primaria
- **Acceso:** Abierto (mensajes); la lista de selección requiere acceso de grupo cerrado
- **Ámbitos:** Renta variable suiza
- **Motivo de inclusión y uso:** Revisiones de los índices suizos (alta concentración en pocos valores defensivos). AG-21.
- **Restricciones de uso:** Uso con atribución; marcas registradas.
- **Sesgos y cautelas:** Lista de selección no pública; el administrador pertenece al operador de mercado (también dueño de BME, RF-0504).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «SIX Swiss Exchange SMI index rules ordinary review six-group.com indices»; WebFetch: sí, PDF de 2026)
- **Origen:** Alta F9_S4 (2026-11-02).

#### RF-0514 · Q 77 (B) — Morningstar Indexes — reglamentos de índices (incluye la familia CRSP migrada)

- **Canal oficial (URL raíz):** https://indexes.morningstar.com/ (reglamento leído: https://indexes.morningstar.com/api/docs/68b407a0f8270052cc84d908 · página de metodología de CRSP que redirige a Morningstar: https://www.crsp.org/indexes/crsp-market-indexes-methodology/)
- **Emisor:** Morningstar Indexes (Morningstar, Inc.)
- **Documentación y notas:** Reglamentos («Construction Rules») por familia, p. ej., Morningstar Target Allocation Indexes (agosto de 2025: reconstitución anual en junio, reequilibrio mensual), con gobierno en tres comités (metodología, operaciones y supervisión conforme al BMR de la UE y del Reino Unido). El 02/11/2026 la página de metodología de los índices de mercado de CRSP (crsp.org) redirige (302) a un reglamento de Morningstar US Total Market, lo que indica la migración de la familia CRSP (referencia de grandes fondos indexados de EE. UU.) a Morningstar Indexes. Canal distinto de RF-0048 (investigación y calificación de fondos) y de RF-0520 (categorías).
- **Temática:** TF-15 Proveedores de índices y metodologías (principal) · secundarias: TF-16
- **Calidad Q:** 77 (B) — Primariedad 18/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 13/15 · Independencia 6/10 · Actualidad 8/10 · Acceso 8/10
- **Tipología:** primaria
- **Acceso:** Abierto (reglamentos PDF); datos bajo licencia
- **Ámbitos:** Índices de renta variable de mercado amplio, factores, multiactivo, sostenibilidad
- **Motivo de inclusión y uso:** Reglas de índices de referencia de grandes fondos indexados y de asignación de activos. AG-21, AG-22.
- **Restricciones de uso:** Uso con atribución.
- **Sesgos y cautelas:** Morningstar es a la vez proveedor de índices, calificador de fondos y proveedor de datos (conflictos potenciales). La continuidad de los índices CRSP bajo Morningstar se deduce de la redirección: confirmar la transición en cada uso.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Integración de los índices CRSP (redirección observada en 2026).
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Morningstar Indexes methodology rulebook indexes.morningstar.com» y «CRSP US Total Market Index methodology quarterly reconstitution crsp.org indexes»; WebFetch: sí, reglamento; redirección de crsp.org observada)
- **Origen:** Alta F9_S4 (2026-11-02).

#### RF-0508 · Q 76 (B) — China Securities Index Co. (CSI) — índices CSI 300 y familia CSI

- **Canal oficial (URL raíz):** http://www.csindex.com.cn/ (ficha del CSI 300: www.csindex.com.cn#/indices/family/detail?indexCode=000300, según la página índice de Wikipedia «CSI 300 Index»)
- **Emisor:** China Securities Index Co., Ltd.
- **Documentación y notas:** Compilador del CSI 300 (acciones A de Shanghái y Shenzhen) y de la familia CSI (CSI 500, CSI 1000, sectoriales, ESG). El historial de cambios muestra revisiones semestrales (fin de mayo/junio y noviembre-diciembre).
- **Temática:** TF-15 Proveedores de índices y metodologías (principal) · secundarias: —
- **Calidad Q:** 76 (B) — Primariedad 19/20 · Historial 10/20 · Transparencia 11/15 · Autoridad 14/15 · Independencia 6/10 · Actualidad 9/10 · Acceso 7/10
- **Tipología:** primaria
- **Acceso:** Abierto (web en chino e inglés; documentación inglesa parcial)
- **Ámbitos:** Renta variable china continental (acciones A)
- **Motivo de inclusión y uso:** Reglas y revisiones del índice de referencia de acciones A (subyacente de ETF y futuros). AG-21.
- **Restricciones de uso:** Uso con atribución; datos bajo licencia.
- **Sesgos y cautelas:** Entidad vinculada a las bolsas de Shanghái y Shenzhen; transparencia en inglés limitada. Confirmada por lectura lateral, sin cargar la web oficial.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «China Securities Index Co csindex.com.cn CSI 300 methodology»; WebFetch: sí, página índice de Wikipedia «CSI 300 Index»)
- **Origen:** Alta F9_S4 (2026-11-02).

#### RF-0515 · Q 76 (B) — Hang Seng Indexes Company — Hang Seng Index y familia de índices de Hong Kong

- **Canal oficial (URL raíz):** https://www.hsi.com.hk/ (según la página índice de Wikipedia «Hang Seng Index»)
- **Emisor:** Hang Seng Indexes Company Limited (filial al 100 % de Hang Seng Bank)
- **Documentación y notas:** Compilador del Hang Seng Index (88 constituyentes según la página índice; las revisiones trimestrales de 2026 lo ampliaron a 93 en mayo y a 95 en agosto según prensa local), Hang Seng TECH, China Enterprises y Composite. Las revisiones trimestrales se publican hacia mediados de febrero, mayo, agosto y noviembre; HKEX archiva los resultados en PDF (p. ej., https://www.hkex.com.hk/-/media/HKEX_Common/Market/Indices/SCCEA/Documents/20260821_EN_review_result.pdf, revisión vinculada al Stock Connect).
- **Temática:** TF-15 Proveedores de índices y metodologías (principal) · secundarias: TF-17
- **Calidad Q:** 76 (B) — Primariedad 19/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 14/15 · Independencia 6/10 · Actualidad 9/10 · Acceso 6/10
- **Tipología:** primaria
- **Acceso:** Abierto (resultados de revisiones y metodologías en la web oficial)
- **Ámbitos:** Renta variable de Hong Kong y empresas chinas cotizadas en Hong Kong
- **Motivo de inclusión y uso:** Revisiones de los índices de Hong Kong (subyacentes de ETF, futuros y opciones de HKEX). AG-21, AG-23.
- **Restricciones de uso:** Uso con atribución; datos bajo licencia.
- **Sesgos y cautelas:** Pertenece a un banco local (conflicto potencial); web oficial no cargada en esta sesión (lectura lateral).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Reforma del HSI anunciada en 2021 (aumento progresivo del número de constituyentes y topes de peso).
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «hsi.com.hk Hang Seng Indexes official website index methodology» y «"Hang Seng Indexes" hsi.com.hk index announcements quarterly review»; WebFetch: sí, página índice de Wikipedia «Hang Seng Index»)
- **Origen:** Alta F9_S4 (2026-11-02).

#### RF-0509 · Q 74 (B) — Solactive — guías de índices y anuncios de cambios de metodología

- **Canal oficial (URL raíz):** https://www.solactive.com/ (anuncio leído: https://legacy2.solactive.com/methodology-change-several-solactive-indices-effective-date-24-11-2025/ · guías en solactive.com/downloads/, p. ej., https://solactive.com/downloads/Solactive_EU_1Day_Rolling_Future_Index_Guideline.pdf)
- **Emisor:** Solactive AG (Fráncfort)
- **Documentación y notas:** Administrador de índices a medida para emisores de ETF y productos estructurados; guías (Guideline) por índice y sección de anuncios con cambios de metodología, nombre, ISIN y RIC (p. ej., aviso de 10/11/2025 sobre la revisión trimestral ESG de siete índices, efectiva el 24/11/2025).
- **Temática:** TF-15 Proveedores de índices y metodologías (principal) · secundarias: TF-16
- **Calidad Q:** 74 (B) — Primariedad 18/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 11/15 · Independencia 6/10 · Actualidad 9/10 · Acceso 7/10
- **Tipología:** primaria
- **Acceso:** Abierto (guías y anuncios)
- **Ámbitos:** Índices de ETF temáticos, de renta fija y de estrategia
- **Motivo de inclusión y uso:** Reglas de muchos índices subyacentes de ETF europeos de bajo coste y temáticos. AG-21, AG-22.
- **Restricciones de uso:** Uso con atribución.
- **Sesgos y cautelas:** Índices a medida a petición del emisor del producto (riesgo de diseño orientado a marketing).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos (migración de web con dominio legacy2).
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Solactive index guidelines announcements solactive.com»; WebFetch: sí, anuncio)
- **Origen:** Alta F9_S4 (2026-11-02).

#### RF-0516 · Q 73 (B) — Wilshire Indexes — FT Wilshire 5000 Index Series

- **Canal oficial (URL raíz):** https://www.wilshireindexes.com/products/ft-wilshire-5000-index-series (catálogo: https://wilshireindexes.com/products/all-indexes)
- **Emisor:** Wilshire Indexes (Wilshire OpCo UK Limited; grupo Wilshire Advisors)
- **Documentación y notas:** Serie que mide todo el mercado de acciones de EE. UU. con precio disponible, ponderada por capitalización completa y ajustada por free float; subíndices por tamaño (mega, mid, small, micro), FT Wilshire 4500 y 2500 y sectoriales; metodología WI-METH-001 y ficha de diciembre de 2025. Marca «FT» bajo licencia del Financial Times.
- **Temática:** TF-15 Proveedores de índices y metodologías (principal) · secundarias: —
- **Calidad Q:** 73 (B) — Primariedad 18/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 12/15 · Independencia 6/10 · Actualidad 8/10 · Acceso 7/10
- **Tipología:** primaria
- **Acceso:** Abierto (página y metodología); datos bajo licencia
- **Ámbitos:** Mercado total de renta variable de EE. UU.; tamaño y sectores
- **Motivo de inclusión y uso:** Medida de mercado total para el indicador capitalización/PIB y comparación con índices de gran capitalización. AG-21.
- **Restricciones de uso:** Uso con atribución.
- **Sesgos y cautelas:** Gestora de inversiones y consultora en el mismo grupo; redistribución de series en FRED limitada por licencia.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Rediseño de la serie Wilshire 5000 como FT Wilshire 5000 con el Financial Times.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Wilshire Indexes Wilshire 5000 methodology wilshireindexes.com»; WebFetch: sí)
- **Origen:** Alta F9_S4 (2026-11-02).

#### RF-0517 · Q 72 (B) — MarketVector Indexes — revisiones trimestrales y semestrales (temáticos y activos digitales)

- **Canal oficial (URL raíz):** https://www.marketvector.com/ (resultados de la revisión del 1T 2025: https://prod.marketvector.com/insights/index-updates/quarterly-and-semi-annual-index-review-results-for-q1-2025 · archivo de noticias: https://marketvector.com/insights/news?page=4)
- **Emisor:** MarketVector Indexes (empresa constituida en Alemania; antes MV Index Solutions, grupo VanEck)
- **Documentación y notas:** Administra índices temáticos, sectoriales y de activos digitales; publica trimestralmente los resultados de sus revisiones (14/03/2025 y anteriores desde 2013) y guías de índices.
- **Temática:** TF-15 Proveedores de índices y metodologías (principal) · secundarias: TF-10
- **Calidad Q:** 72 (B) — Primariedad 17/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 11/15 · Independencia 6/10 · Actualidad 8/10 · Acceso 8/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** Índices temáticos (semiconductores, energía nuclear, oro y minería, etc.) y de criptoactivos
- **Motivo de inclusión y uso:** Reglas y revisiones de índices subyacentes de ETF temáticos y de criptoactivos. AG-21, AG-22.
- **Restricciones de uso:** Uso con atribución.
- **Sesgos y cautelas:** Vinculada a un emisor de ETF (VanEck), según su antigua denominación; la página leída no detalla las familias revisadas.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Cambio de nombre de MV Index Solutions a MarketVector Indexes (2022).
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «MarketVector Indexes index guide review announcements marketvector.com»; WebFetch: sí)
- **Origen:** Alta F9_S4 (2026-11-02).

#### RF-0518 · Q 72 (B) — Scientific Beta — índices smart beta y de factores

- **Canal oficial (URL raíz):** https://www.scientificbeta.com/ (según el anuncio de adquisición de SGX de 23/01/2020: https://links.sgx.com/1.0.0/corporate-announcements/NOG6SYOAQUBWSHPU/594339_20200123_SGX_scales_up_its_index_business_with_EUR186M_acquisition.pdf)
- **Emisor:** Scientific Beta Pte. Ltd. (93 % SGX Group desde 2020; 7 % afiliada de EDHEC)
- **Documentación y notas:** Plataforma de índices smart beta y multifactoriales nacida en EDHEC-Risk Institute (2013); unos 54.700 M$ ligados a sus índices en septiembre de 2019; investigación publicada sobre primas de factores, riesgos de implementación y clima.
- **Temática:** TF-15 Proveedores de índices y metodologías (principal) · secundarias: TF-13
- **Calidad Q:** 72 (B) — Primariedad 17/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 12/15 · Independencia 7/10 · Actualidad 7/10 · Acceso 6/10
- **Tipología:** primaria (reglas de índices) y analítica (investigación)
- **Acceso:** Mixto (investigación abierta; datos con registro o licencia)
- **Ámbitos:** Factores (valor, tamaño, momentum, baja volatilidad, calidad), multifactor, clima
- **Motivo de inclusión y uso:** Análisis de estrategias de factores y de su construcción como índices. AG-21.
- **Restricciones de uso:** Uso con atribución.
- **Sesgos y cautelas:** Su investigación defiende su propio enfoque de diversificación; web oficial no cargada en esta sesión.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Adquirida por SGX en 2020 por 186 M€.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Scientific Beta smart beta indices EDHEC scientificbeta.com»; WebFetch: sí, anuncio de SGX)
- **Origen:** Alta F9_S4 (2026-11-02).

#### RF-0519 · Q 66 (B) — Index Industry Association (IIA) — encuesta anual del sector de índices

- **Canal oficial (URL raíz):** http://www.indexindustry.org/ (según la nota de la sexta encuesta anual, 01/11/2022: https://www.businesswire.com/news/home/20221101005816/en/Sixth-Annual-Index-Industry-Association-Benchmark-Survey-Reveals-Continuing-Record-Breaking-ESG-Growth-Multi-Asset-Expansion-by-Index-Providers-Globally)
- **Emisor:** Index Industry Association (asociación de proveedores de índices; 18 miembros, entre ellos Bloomberg, Cboe Global Indices, CSI, FTSE Russell, Hang Seng Indexes, ICE, JPXI, Morningstar, MSCI, Nasdaq, STOXX y S&P DJI)
- **Documentación y notas:** Encuesta anual (benchmark survey) sobre el número de índices por clase de activo, región y estilo (p. ej., 2022: +4,43 % en total, más de 50.000 índices ESG; encuestas posteriores con unos 3,7 millones de índices); posiciones sobre regulación de índices de referencia.
- **Temática:** TF-15 Proveedores de índices y metodologías (principal) · secundarias: —
- **Calidad Q:** 66 (B) — Primariedad 15/20 · Historial 10/20 · Transparencia 10/15 · Autoridad 12/15 · Independencia 5/10 · Actualidad 6/10 · Acceso 8/10
- **Tipología:** secundaria (encuesta agregada del sector)
- **Acceso:** Abierto
- **Ámbitos:** Estructura y tendencias del sector de índices (ESG, renta fija, multiactivo)
- **Motivo de inclusión y uso:** Contexto de la oferta de índices y de la proliferación de índices temáticos y ESG. AG-21.
- **Restricciones de uso:** Uso con atribución.
- **Sesgos y cautelas:** Patronal del sector (defiende los intereses de sus miembros); cifras autodeclaradas por los proveedores. Web oficial no cargada (lectura lateral).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Index Industry Association annual benchmark survey number of indexes 2025»; WebFetch: sí, nota de Business Wire)
- **Origen:** Alta F9_S4 (2026-11-02).

## TF-16 Fondos y ETF: datos, flujos y categorías

#### RF-0521 · Q 86 (A) — SEC — Form N-PORT Data Sets (carteras mensuales de fondos registrados)

- **Canal oficial (URL raíz):** https://www.sec.gov/data-research/sec-markets-data/form-n-port-data-sets
- **Emisor:** U.S. Securities and Exchange Commission (División de Análisis Económico y de Riesgos, DERA)
- **Documentación y notas:** Conjuntos de datos estructurados extraídos de los formularios N-PORT públicos (carteras de fondos de inversión y ETF registrados a fin de mes); actualización trimestral; cobertura de octubre de 2019 a septiembre de 2026 (fichero 2026 Q3, ZIP de 441 MB; página actualizada el 30/09/2026); documento «readme» con tablas y definiciones. Complementa los datos de 13F (RF-0044) con la totalidad de la cartera, derivados y liquidez de los fondos.
- **Temática:** TF-16 Fondos y ETF: datos, flujos y categorías (principal) · secundarias: TF-02
- **Calidad Q:** 86 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 8/10 · Acceso 9/10
- **Tipología:** primaria (declaraciones regulatorias)
- **Acceso:** Abierto (descarga masiva)
- **Ámbitos:** Posiciones agregadas de fondos de EE. UU. por activo, emisor, derivado y país
- **Motivo de inclusión y uso:** Medir exposición agregada de la industria de fondos a segmentos (p. ej., crédito privado en fondos abiertos, derivados en ETF apalancados) y concentración. AG-22, AG-23.
- **Restricciones de uso:** Dominio público; citar trimestre del fichero.
- **Sesgos y cautelas:** Solo se publican los datos públicos (con desfase); ficheros voluminosos que requieren tratamiento.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Enmiendas del formulario N-PORT (reglas de 2024 sobre frecuencia de publicación) pueden alterar la serie.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «SEC Form N-PORT data sets Form N-CEN data sets structured data»; WebFetch: sí)
- **Origen:** Alta F9_S4 (2026-11-02).

#### RF-0522 · Q 82 (A) — SEC — Form N-CEN Data Sets (informe censal anual de fondos registrados)

- **Canal oficial (URL raíz):** https://www.sec.gov/dera/data/form-ncen-data-sets (ruta mostrada en los resultados de búsqueda; catálogo federal: https://catalog.data.gov/organization/sec-gov?tags=__)
- **Emisor:** U.S. Securities and Exchange Commission (DERA)
- **Documentación y notas:** Datos estructurados del formulario N-CEN, informe anual de fondos registrados (proveedores de servicios, información específica de ETF —creadores autorizados, unidades de creación—, préstamo de valores, uso de líneas de crédito). Adoptado en la reforma de información de fondos de 2016 junto con N-PORT.
- **Temática:** TF-16 Fondos y ETF: datos, flujos y categorías (principal) · secundarias: TF-02
- **Calidad Q:** 82 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 6/10 · Acceso 8/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** Estructura de la industria de fondos y ETF de EE. UU.; proveedores y mecanismos de creación/reembolso
- **Motivo de inclusión y uso:** Análisis de la infraestructura del mercado de ETF (concentración de creadores autorizados) y de prácticas de préstamo de valores. AG-22.
- **Restricciones de uso:** Dominio público.
- **Sesgos y cautelas:** Frecuencia anual; la página no se pudo cargar en esta sesión (fuera de la lista permitida), confirmada por resultados de búsqueda.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «SEC Form N-PORT data sets Form N-CEN data sets structured data»; WebFetch: no, URL no admitida)
- **Origen:** Alta F9_S4 (2026-11-02).

#### RF-0523 · Q 82 (A) — ESMA — Market report on the costs and performance of EU retail investment products

- **Canal oficial (URL raíz):** https://www.esma.europa.eu/press-news/esma-news/new-investment-funds-drive-reduction-costs-investors (informe de 2025, publicado el 03/03/2026: https://www.esma.europa.eu/sites/default/files/2026-03/ESMA50-1949966494-4065_Market_Report_-_Costs_and_Performance_of_EU_Retail_Investment_Products.pdf)
- **Emisor:** European Securities and Markets Authority (ESMA)
- **Documentación y notas:** Octava edición del informe anual de costes y rentabilidad de UCITS, FIA minoristas y productos estructurados: en 2024 los gastos corrientes bajaron un 8 % en fondos de renta variable y casi un 15 % en renta fija minoristas (impulso de fondos nuevos), rentabilidades reales netas positivas en todas las categorías, UCITS ESG más baratos pero con peor rentabilidad que los no ESG, participación minorista en FIA del 9 %, auge de estructurados ligados a tipos (27 % del mercado). Pieza distinta de RF-0027 (TRV) y de RF-0403 (FIA).
- **Temática:** TF-16 Fondos y ETF: datos, flujos y categorías (principal) · secundarias: TF-02
- **Calidad Q:** 82 (A) — Primariedad 18/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 6/10 · Acceso 10/10
- **Tipología:** primaria (estadística supervisora)
- **Acceso:** Abierto
- **Ámbitos:** Costes, rentabilidad bruta y neta por categoría de fondo UCITS (incluidos ETF), FIA y estructurados en la UE
- **Motivo de inclusión y uso:** Referencia oficial del coste de implementación por categoría y del diferencial gestión activa/pasiva en Europa. AG-22.
- **Restricciones de uso:** Uso libre con atribución.
- **Sesgos y cautelas:** Desfase de más de un año; muestras basadas en bases de datos comerciales.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «ESMA market report costs and performance of EU retail investment products 2026»; WebFetch: sí)
- **Origen:** Alta F9_S4 (2026-11-02).

#### RF-0524 · Q 79 (B) — EIOPA — Costs and past performance report (productos de inversión basados en seguros)

- **Canal oficial (URL raíz):** https://www.eiopa.europa.eu/publications/costs-and-past-performance-report-2026_en
- **Emisor:** European Insurance and Occupational Pensions Authority (EIOPA)
- **Documentación y notas:** Informe de 01/04/2026 sobre costes y rentabilidad pasada de productos minoristas de inversión bajo su ámbito (unit-linked y con participación en beneficios), periodo 2020-2024: 5.906 productos de 175 aseguradoras, más del 60 % de las primas de esos productos en el EEE; PDF enlazado.
- **Temática:** TF-16 Fondos y ETF: datos, flujos y categorías (principal) · secundarias: TF-02
- **Calidad Q:** 79 (B) — Primariedad 17/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 14/15 · Independencia 10/10 · Actualidad 6/10 · Acceso 10/10
- **Tipología:** primaria (estadística supervisora)
- **Acceso:** Abierto
- **Ámbitos:** Vehículos de inversión envueltos en seguros (unit-linked) frente a fondos
- **Motivo de inclusión y uso:** Complemento de RF-0523 para comparar costes entre vehículos (fondo directo frente a seguro de inversión). AG-22.
- **Restricciones de uso:** Uso libre con atribución.
- **Sesgos y cautelas:** Muestra parcial de aseguradoras; la página no resume resultados (están en el PDF).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «ESMA market report costs and performance of EU retail investment products 2026»; WebFetch: sí)
- **Origen:** Alta F9_S4 (2026-11-02).

#### RF-0525 · Q 78 (B) — INVERCO — estadísticas mensuales de fondos de inversión e IIC en España

- **Canal oficial (URL raíz):** http://www.inverco.es/ (informe mensual de julio de 2026: https://www.inverco.es/wp-content/uploads/2026/08/2607_Julio-2026.pdf · informe anual 2025: https://www.inverco.es/informe/informe-anual-2025)
- **Emisor:** Asociación de Instituciones de Inversión Colectiva y Fondos de Pensiones (INVERCO)
- **Documentación y notas:** Informe mensual de fondos (patrimonio, suscripciones netas, partícipes y rentabilidad por vocación inversora: monetarios, renta fija, mixtos, renta variable nacional e internacional por zonas, globales, garantizados, índice, rentabilidad objetivo, retorno absoluto, inversión libre) y notas de prensa. Julio de 2026: 478.069 M€ de patrimonio (+6 % en el año), 10.959 M€ de suscripciones netas acumuladas, 19,27 millones de cuentas de partícipes.
- **Temática:** TF-16 Fondos y ETF: datos, flujos y categorías (principal) · secundarias: —
- **Calidad Q:** 78 (B) — Primariedad 19/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 13/15 · Independencia 5/10 · Actualidad 9/10 · Acceso 10/10
- **Tipología:** primaria (datos agregados de las gestoras asociadas)
- **Acceso:** Abierto
- **Ámbitos:** Fondos de inversión españoles, SICAV, fondos de pensiones
- **Motivo de inclusión y uso:** Flujos y preferencias del inversor español por categoría (rotación de monetarios y renta fija a renta variable). AG-22.
- **Restricciones de uso:** Uso con atribución.
- **Sesgos y cautelas:** Patronal del sector; cifras provisionales que la CNMV (RF-0026) publica después con datos oficiales; partícipes contados por cuentas, no personas.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «INVERCO estadísticas fondos de inversión patrimonio suscripciones netas 2026»; WebFetch: sí, informe de julio de 2026)
- **Origen:** Alta F9_S4 (2026-11-02).

#### RF-0520 · Q 74 (B) — Morningstar — Category Classifications (metodología de categorías de fondos)

- **Canal oficial (URL raíz):** https://www.morningstar.com/content/cs-assets/v3/assets/blt9415ea4cc4157833/bltc0c557175d70b1fd/68dea997aed382ecc562dbce/Morningstar_Category_Classification_for_Funds_-_October_2024.pdf (clasificación global: https://advisor.morningstar.com/Enterprise/VTC/MorningstarGlobalCategory_April2021.pdf · repositorio de metodologías: https://www.morningstar.com/business/insights/research/methodology-documents?page=7)
- **Emisor:** Morningstar, Inc. (Manager Research)
- **Documentación y notas:** Metodología de octubre de 2024 para fondos de EE. UU.: 127 categorías en nueve grupos; asignación por estadísticas medias de cartera de los tres años previos (no por el folleto); revisiones semestrales por grupo (renta variable abril y septiembre; alternativos, mixtos y materias primas abril y octubre; renta fija julio y noviembre); filtro cuantitativo más validación de analistas y apelaciones. Existen versiones regionales (Europa/global, Japón, Australia) y la clasificación global (Global Category). Canal distinto de RF-0048 (investigación y Medalist Rating) y de RF-0514 (índices).
- **Temática:** TF-16 Fondos y ETF: datos, flujos y categorías (principal) · secundarias: —
- **Calidad Q:** 74 (B) — Primariedad 17/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 13/15 · Independencia 6/10 · Actualidad 7/10 · Acceso 7/10
- **Tipología:** primaria (taxonomía del proveedor)
- **Acceso:** Abierto (PDF); datos por fondo bajo licencia
- **Ámbitos:** Taxonomía de fondos y ETF por estilo, región, sector y clase de activo
- **Motivo de inclusión y uso:** Taxonomía de referencia para agregar flujos y rentabilidades por segmento de forma comparable. AG-22.
- **Restricciones de uso:** Uso con atribución.
- **Sesgos y cautelas:** Taxonomía propietaria; las reasignaciones alteran series históricas por categoría.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Revisiones periódicas de definiciones (ediciones 2018, 2021, 2024, 2025).
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Morningstar Global Category Classifications methodology document»; WebFetch: sí, PDF de octubre de 2024)
- **Origen:** Alta F9_S4 (2026-11-02).

#### RF-0527 · Q 73 (B) — AIC (Association of Investment Companies) — estadísticas de investment trusts y descuentos

- **Canal oficial (URL raíz):** https://www.theaic.co.uk/ (serie histórica de descuentos, 05/01/2026: https://www.theaic.co.uk/aic/news/press-releases/aic-releases-53-years-of-investment-trust-discount-history)
- **Emisor:** The Association of Investment Companies (281 miembros)
- **Documentación y notas:** Publica la serie mensual de descuento medio de los investment trusts desde diciembre de 1972 (calculada con datos de Morningstar; ex-par frente al actual cum-fair) y la actualización mensual «Investment company statistics» (patrimonio por sector, captaciones, salidas a bolsa y operaciones corporativas); herramientas de investigación en la web.
- **Temática:** TF-16 Fondos y ETF: datos, flujos y categorías (principal) · secundarias: TF-11
- **Calidad Q:** 73 (B) — Primariedad 17/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 12/15 · Independencia 5/10 · Actualidad 8/10 · Acceso 9/10
- **Tipología:** primaria (estadística sectorial)
- **Acceso:** Abierto
- **Ámbitos:** Fondos cerrados cotizados del Reino Unido (investment trusts), descuentos sobre valor liquidativo
- **Motivo de inclusión y uso:** El descuento medio de los fondos cerrados es indicador de sentimiento y de oportunidades de valor relativo (incluidos alternativos e infraestructuras). AG-22.
- **Restricciones de uso:** Uso con atribución.
- **Sesgos y cautelas:** Patronal del sector; cambio de método de descuento (ex-par frente a cum-fair) rompe la comparabilidad.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Association of Investment Companies AIC investment trust industry statistics discounts theaic.co.uk»; WebFetch: sí)
- **Origen:** Alta F9_S4 (2026-11-02).

#### RF-0528 · Q 72 (B) — LSEG Lipper — U.S. Weekly FundFlows Insight Report (Lipper Alpha)

- **Canal oficial (URL raíz):** https://lipperalpha.refinitiv.com/ (ejemplo leído: https://lipperalpha.refinitiv.com/2024/05/u-s-weekly-fundflows-insight-report-fund-market-reports-first-outflow-in-six-weeks/)
- **Emisor:** LSEG Lipper (London Stock Exchange Group)
- **Documentación y notas:** Informe semanal de flujos netos de fondos de inversión y ETF de EE. UU. por clasificación Lipper (renta variable, renta fija, mixtos, monetarios, materias primas, alternativos, ETF de bitcoin al contado), con rentabilidades de índices y tipos; semana de jueves a miércoles; datos de Lipper Global Fund Flows.
- **Temática:** TF-16 Fondos y ETF: datos, flujos y categorías (principal) · secundarias: TF-06
- **Calidad Q:** 72 (B) — Primariedad 16/20 · Historial 10/20 · Transparencia 11/15 · Autoridad 13/15 · Independencia 7/10 · Actualidad 8/10 · Acceso 7/10
- **Tipología:** secundaria (proveedor de datos)
- **Acceso:** Comentarios abiertos; datos completos bajo licencia
- **Ámbitos:** Flujos semanales de fondos y ETF por clasificación
- **Motivo de inclusión y uso:** Contraste semanal de los flujos de ICI (RF-0053) con desglose por clasificación más fino. AG-22.
- **Restricciones de uso:** Uso con atribución.
- **Sesgos y cautelas:** Muestra del propio proveedor; la última pieza leída es de 2024 (comprobar continuidad del blog tras la migración de marca Refinitiv a LSEG).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Refinitiv integrada en LSEG (2021).
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «LSEG Lipper weekly fund flows report US ETFs mutual funds»; WebFetch: sí)
- **Origen:** Alta F9_S4 (2026-11-02).

#### RF-0531 · Q 72 (B) — The Investment Association (IA) — estadísticas de fondos del Reino Unido

- **Canal oficial (URL raíz):** https://www.theia.org/ (enlazada desde el listado oficial de miembros de EFAMA: https://www.efama.org/about-us/our-members)
- **Emisor:** The Investment Association (Reino Unido)
- **Documentación y notas:** Asociación nacional de fondos y gestión de activos de el Reino Unido, miembro de EFAMA; fuente de las estadísticas nacionales que EFAMA (RF-0345) agrega en sus informes mensuales y trimestrales. Mayor mercado de gestión de activos de Europa; mantiene los sectores IA con los que se clasifican los fondos británicos.
- **Temática:** TF-16 Fondos y ETF: datos, flujos y categorías (principal) · secundarias: —
- **Calidad Q:** 72 (B) — Primariedad 17/20 · Historial 10/20 · Transparencia 11/15 · Autoridad 13/15 · Independencia 5/10 · Actualidad 8/10 · Acceso 8/10
- **Tipología:** secundaria (patronal; datos de sus asociados)
- **Acceso:** Abierto (web oficial; algunos informes solo para socios)
- **Ámbitos:** Patrimonio y flujos de fondos domiciliados o comercializados en el Reino Unido
- **Motivo de inclusión y uso:** Desglose nacional de flujos y patrimonio por categoría cuando el agregado europeo de EFAMA no basta. AG-22.
- **Restricciones de uso:** Uso con atribución.
- **Sesgos y cautelas:** Patronal del sector (interés promocional). La web oficial no se cargó en esta sesión: la existencia y la URL se confirmaron por lectura lateral en el listado de EFAMA; comprobar la sección estadística y su periodicidad en el primer uso.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «EFAMA member associations national fund associations list»; WebFetch: sí, página índice de miembros de EFAMA)
- **Origen:** Alta F9_S4 (2026-11-02).

#### RF-0532 · Q 72 (B) — BVI (Bundesverband Investment und Asset Management) — estadísticas de fondos de Alemania

- **Canal oficial (URL raíz):** https://www.bvi.de (enlazada desde el listado oficial de miembros de EFAMA: https://www.efama.org/about-us/our-members)
- **Emisor:** Bundesverband Investment und Asset Management e.V. (BVI)
- **Documentación y notas:** Asociación nacional de fondos y gestión de activos de Alemania, miembro de EFAMA; fuente de las estadísticas nacionales que EFAMA (RF-0345) agrega en sus informes mensuales y trimestrales. Cubre fondos minoristas y fondos institucionales Spezialfonds.
- **Temática:** TF-16 Fondos y ETF: datos, flujos y categorías (principal) · secundarias: —
- **Calidad Q:** 72 (B) — Primariedad 17/20 · Historial 10/20 · Transparencia 11/15 · Autoridad 13/15 · Independencia 5/10 · Actualidad 8/10 · Acceso 8/10
- **Tipología:** secundaria (patronal; datos de sus asociados)
- **Acceso:** Abierto (web oficial; algunos informes solo para socios)
- **Ámbitos:** Patrimonio y flujos de fondos domiciliados o comercializados en Alemania
- **Motivo de inclusión y uso:** Desglose nacional de flujos y patrimonio por categoría cuando el agregado europeo de EFAMA no basta. AG-22.
- **Restricciones de uso:** Uso con atribución.
- **Sesgos y cautelas:** Patronal del sector (interés promocional). La web oficial no se cargó en esta sesión: la existencia y la URL se confirmaron por lectura lateral en el listado de EFAMA; comprobar la sección estadística y su periodicidad en el primer uso.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «EFAMA member associations national fund associations list»; WebFetch: sí, página índice de miembros de EFAMA)
- **Origen:** Alta F9_S4 (2026-11-02).

#### RF-0534 · Q 71 (B) — Assogestioni — estadísticas de fondos de Italia

- **Canal oficial (URL raíz):** https://www.assogestioni.it/ (enlazada desde el listado oficial de miembros de EFAMA: https://www.efama.org/about-us/our-members)
- **Emisor:** Associazione Italiana del Risparmio Gestito (Assogestioni)
- **Documentación y notas:** Asociación nacional de fondos y gestión de activos de Italia, miembro de EFAMA; fuente de las estadísticas nacionales que EFAMA (RF-0345) agrega en sus informes mensuales y trimestrales. Representa a la gestión colectiva y discrecional italiana.
- **Temática:** TF-16 Fondos y ETF: datos, flujos y categorías (principal) · secundarias: —
- **Calidad Q:** 71 (B) — Primariedad 17/20 · Historial 10/20 · Transparencia 11/15 · Autoridad 12/15 · Independencia 5/10 · Actualidad 8/10 · Acceso 8/10
- **Tipología:** secundaria (patronal; datos de sus asociados)
- **Acceso:** Abierto (web oficial; algunos informes solo para socios)
- **Ámbitos:** Patrimonio y flujos de fondos domiciliados o comercializados en Italia
- **Motivo de inclusión y uso:** Desglose nacional de flujos y patrimonio por categoría cuando el agregado europeo de EFAMA no basta. AG-22.
- **Restricciones de uso:** Uso con atribución.
- **Sesgos y cautelas:** Patronal del sector (interés promocional). La web oficial no se cargó en esta sesión: la existencia y la URL se confirmaron por lectura lateral en el listado de EFAMA; comprobar la sección estadística y su periodicidad en el primer uso.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «EFAMA member associations national fund associations list»; WebFetch: sí, página índice de miembros de EFAMA)
- **Origen:** Alta F9_S4 (2026-11-02).

#### RF-0533 · Q 69 (B) — AFG (Association Française de la Gestion Financière) — gestión de activos en Francia

- **Canal oficial (URL raíz):** https://www.afg.asso.fr/ (enlazada desde el listado oficial de miembros de EFAMA: https://www.efama.org/about-us/our-members)
- **Emisor:** Association Française de la Gestion Financière (AFG)
- **Documentación y notas:** Asociación nacional de fondos y gestión de activos de Francia, miembro de EFAMA; fuente de las estadísticas nacionales que EFAMA (RF-0345) agrega en sus informes mensuales y trimestrales. Representa a la gestión de activos francesa (fondos OPCVM y FIA y mandatos).
- **Temática:** TF-16 Fondos y ETF: datos, flujos y categorías (principal) · secundarias: —
- **Calidad Q:** 69 (B) — Primariedad 16/20 · Historial 10/20 · Transparencia 11/15 · Autoridad 12/15 · Independencia 5/10 · Actualidad 7/10 · Acceso 8/10
- **Tipología:** secundaria (patronal; datos de sus asociados)
- **Acceso:** Abierto (web oficial; algunos informes solo para socios)
- **Ámbitos:** Patrimonio y flujos de fondos domiciliados o comercializados en Francia
- **Motivo de inclusión y uso:** Desglose nacional de flujos y patrimonio por categoría cuando el agregado europeo de EFAMA no basta. AG-22.
- **Restricciones de uso:** Uso con atribución.
- **Sesgos y cautelas:** Patronal del sector (interés promocional). La web oficial no se cargó en esta sesión: la existencia y la URL se confirmaron por lectura lateral en el listado de EFAMA; comprobar la sección estadística y su periodicidad en el primer uso.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «EFAMA member associations national fund associations list»; WebFetch: sí, página índice de miembros de EFAMA)
- **Origen:** Alta F9_S4 (2026-11-02).

#### RF-0537 · Q 69 (B) — Fondbolagens Förening — estadísticas de fondos de Suecia

- **Canal oficial (URL raíz):** https://www.fondbolagen.se/ (enlazada desde el listado oficial de miembros de EFAMA: https://www.efama.org/about-us/our-members)
- **Emisor:** Fondbolagens Förening (Swedish Investment Fund Association)
- **Documentación y notas:** Asociación nacional de fondos y gestión de activos de Suecia, miembro de EFAMA; fuente de las estadísticas nacionales que EFAMA (RF-0345) agrega en sus informes mensuales y trimestrales. Mercado nórdico con alta penetración de fondos entre hogares y en el sistema de pensiones.
- **Temática:** TF-16 Fondos y ETF: datos, flujos y categorías (principal) · secundarias: —
- **Calidad Q:** 69 (B) — Primariedad 16/20 · Historial 10/20 · Transparencia 11/15 · Autoridad 11/15 · Independencia 5/10 · Actualidad 8/10 · Acceso 8/10
- **Tipología:** secundaria (patronal; datos de sus asociados)
- **Acceso:** Abierto (web oficial; algunos informes solo para socios)
- **Ámbitos:** Patrimonio y flujos de fondos domiciliados o comercializados en Suecia
- **Motivo de inclusión y uso:** Desglose nacional de flujos y patrimonio por categoría cuando el agregado europeo de EFAMA no basta. AG-22.
- **Restricciones de uso:** Uso con atribución.
- **Sesgos y cautelas:** Patronal del sector (interés promocional). La web oficial no se cargó en esta sesión: la existencia y la URL se confirmaron por lectura lateral en el listado de EFAMA; comprobar la sección estadística y su periodicidad en el primer uso.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «EFAMA member associations national fund associations list»; WebFetch: sí, página índice de miembros de EFAMA)
- **Origen:** Alta F9_S4 (2026-11-02).

#### RF-0526 · Q 68 (B) — ETFGI — informes mensuales del sector mundial de ETF

- **Canal oficial (URL raíz):** https://etfgi.com/ (nota de 19/08/2026 leída: https://etfgi.com/node/28936)
- **Emisor:** ETFGI LLP (consultora independiente; fundadora y socia directora: Deborah Fuhr)
- **Documentación y notas:** Notas de prensa mensuales con patrimonio y flujos de ETF por región, clase de activo y emisor (fin de julio de 2026: 23,11 billones de dólares, récord; entradas de 383.600 M$ en julio y 1,71 billones en el año; 86 meses consecutivos de entradas; 17.654 ETF de 1.025 proveedores en 85 bolsas; ETF activos con 590.460 M$ de entradas en el año). Informes completos por suscripción.
- **Temática:** TF-16 Fondos y ETF: datos, flujos y categorías (principal) · secundarias: TF-06
- **Calidad Q:** 68 (B) — Primariedad 15/20 · Historial 10/20 · Transparencia 10/15 · Autoridad 12/15 · Independencia 7/10 · Actualidad 9/10 · Acceso 5/10
- **Tipología:** secundaria (agregador)
- **Acceso:** Notas de prensa abiertas; informes de pago
- **Ámbitos:** ETF y ETP mundiales: patrimonio, flujos, lanzamientos y cierres
- **Motivo de inclusión y uso:** Vista global y mensual del mercado de ETF (incluidos ETF activos, temáticos y de cripto). AG-22.
- **Restricciones de uso:** Uso con atribución; no redistribuir informes de pago.
- **Sesgos y cautelas:** Metodología de recuento no auditada; titulares orientados a récords; financiada por patrocinio de eventos.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «ETFGI reports assets invested in ETFs industry globally record 2026»; WebFetch: sí)
- **Origen:** Alta F9_S4 (2026-11-02).

#### RF-0530 · Q 67 (B) — Irish Funds — estadísticas del sector de fondos irlandés

- **Canal oficial (URL raíz):** https://www.irishfunds.ie/ (estadísticas: https://www.irishfunds.ie/facts-figures/industry-statistics/ · nota leída: https://irishfunds.ie/news-knowledge/news/ireland-hosts-global-investment-funds-industry-leaders-as-global-fund-assets-reach-euro70-6-trillion)
- **Emisor:** Irish Funds Industry Association (miembro de EFAMA y de IIFA)
- **Documentación y notas:** Asociación del principal domicilio europeo de ETF UCITS; página de estadísticas sectoriales («Facts & Figures»). Organizó en 2024 la 37.ª conferencia de IIFA (25 asociaciones, 97 % del patrimonio mundial de fondos, 70,6 billones de euros). Irlanda: tercer domicilio mundial y segundo de la UE en fondos regulados.
- **Temática:** TF-16 Fondos y ETF: datos, flujos y categorías (principal) · secundarias: —
- **Calidad Q:** 67 (B) — Primariedad 15/20 · Historial 10/20 · Transparencia 10/15 · Autoridad 12/15 · Independencia 5/10 · Actualidad 7/10 · Acceso 8/10
- **Tipología:** secundaria (patronal; datos derivados del Banco Central de Irlanda)
- **Acceso:** Abierto
- **Ámbitos:** Fondos y ETF UCITS domiciliados en Irlanda
- **Motivo de inclusión y uso:** Contexto del domicilio de la mayoría de ETF UCITS. AG-22. Para cifras oficiales, usar el Central Bank of Ireland (RF-0209).
- **Restricciones de uso:** Uso con atribución.
- **Sesgos y cautelas:** Patronal con interés promocional; la página leída no contiene cifras del domicilio irlandés.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «IIFA International Investment Funds Association worldwide regulated fund statistics members»; WebFetch: sí)
- **Origen:** Alta F9_S4 (2026-11-02).

#### RF-0535 · Q 67 (B) — ALFI (Association of the Luxembourg Fund Industry) — sector de fondos de Luxemburgo

- **Canal oficial (URL raíz):** https://www.alfi.lu/ (enlazada desde el listado oficial de miembros de EFAMA: https://www.efama.org/about-us/our-members)
- **Emisor:** Association of the Luxembourg Fund Industry (ALFI)
- **Documentación y notas:** Asociación nacional de fondos y gestión de activos de Luxemburgo, miembro de EFAMA; fuente de las estadísticas nacionales que EFAMA (RF-0345) agrega en sus informes mensuales y trimestrales. Primer domicilio europeo de fondos de distribución transfronteriza; las cifras oficiales las publica la CSSF (RF-0210).
- **Temática:** TF-16 Fondos y ETF: datos, flujos y categorías (principal) · secundarias: —
- **Calidad Q:** 67 (B) — Primariedad 15/20 · Historial 10/20 · Transparencia 10/15 · Autoridad 12/15 · Independencia 5/10 · Actualidad 7/10 · Acceso 8/10
- **Tipología:** secundaria (patronal; datos de sus asociados)
- **Acceso:** Abierto (web oficial; algunos informes solo para socios)
- **Ámbitos:** Patrimonio y flujos de fondos domiciliados o comercializados en Luxemburgo
- **Motivo de inclusión y uso:** Desglose nacional de flujos y patrimonio por categoría cuando el agregado europeo de EFAMA no basta. AG-22.
- **Restricciones de uso:** Uso con atribución.
- **Sesgos y cautelas:** Patronal del sector (interés promocional). La web oficial no se cargó en esta sesión: la existencia y la URL se confirmaron por lectura lateral en el listado de EFAMA; comprobar la sección estadística y su periodicidad en el primer uso.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «EFAMA member associations national fund associations list»; WebFetch: sí, página índice de miembros de EFAMA)
- **Origen:** Alta F9_S4 (2026-11-02).

#### RF-0529 · Q 66 (B) — justETF — buscador y base de datos de ETF UCITS en Europa

- **Canal oficial (URL raíz):** https://www.justetf.com/ (buscador: https://justetf.com/en/find-etf.html)
- **Emisor:** justETF (plataforma independiente de información sobre ETF, Alemania)
- **Documentación y notas:** Buscador con unos 4.974 productos cotizados (2.921 de renta variable, 1.564 de bonos, materias primas, cripto, metales preciosos, monetarios e inmobiliarios) y 3.167 índices subyacentes; comparador, fichas por ETF y configuración por país (Alemania, Austria, Suiza, Reino Unido, Italia, Francia, España, Países Bajos, Bélgica, Luxemburgo).
- **Temática:** TF-16 Fondos y ETF: datos, flujos y categorías (principal) · secundarias: TF-15
- **Calidad Q:** 66 (B) — Primariedad 13/20 · Historial 10/20 · Transparencia 9/15 · Autoridad 10/15 · Independencia 6/10 · Actualidad 9/10 · Acceso 9/10
- **Tipología:** secundaria (agregador)
- **Acceso:** Abierto (funciones avanzadas de pago)
- **Ámbitos:** Oferta de ETF UCITS por índice, clase de activo, coste y domicilio
- **Motivo de inclusión y uso:** Mapear qué índices y segmentos tienen vehículo cotizado en Europa (amplitud de oferta por ámbito), sin seleccionar productos. AG-22, AG-21.
- **Restricciones de uso:** Uso con atribución; no constituye asesoramiento.
- **Sesgos y cautelas:** Ingresos por afiliación con brókers; cobertura no exhaustiva; datos de terceros.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «justETF ETF screener Europe UCITS ETF database»; WebFetch: sí)
- **Origen:** Alta F9_S4 (2026-11-02).

#### RF-0536 · Q 66 (B) — Asset Management Association Switzerland (AMAS) — fondos y gestión de activos en Suiza

- **Canal oficial (URL raíz):** https://www.am-switzerland.ch/en (enlazada desde el listado oficial de miembros de EFAMA: https://www.efama.org/about-us/our-members)
- **Emisor:** Asset Management Association Switzerland
- **Documentación y notas:** Asociación nacional de fondos y gestión de activos de Suiza, miembro de EFAMA; fuente de las estadísticas nacionales que EFAMA (RF-0345) agrega en sus informes mensuales y trimestrales. Fuera de la UE; útil para fondos domiciliados o distribuidos en Suiza.
- **Temática:** TF-16 Fondos y ETF: datos, flujos y categorías (principal) · secundarias: —
- **Calidad Q:** 66 (B) — Primariedad 15/20 · Historial 10/20 · Transparencia 10/15 · Autoridad 11/15 · Independencia 5/10 · Actualidad 7/10 · Acceso 8/10
- **Tipología:** secundaria (patronal; datos de sus asociados)
- **Acceso:** Abierto (web oficial; algunos informes solo para socios)
- **Ámbitos:** Patrimonio y flujos de fondos domiciliados o comercializados en Suiza
- **Motivo de inclusión y uso:** Desglose nacional de flujos y patrimonio por categoría cuando el agregado europeo de EFAMA no basta. AG-22.
- **Restricciones de uso:** Uso con atribución.
- **Sesgos y cautelas:** Patronal del sector (interés promocional). La web oficial no se cargó en esta sesión: la existencia y la URL se confirmaron por lectura lateral en el listado de EFAMA; comprobar la sección estadística y su periodicidad en el primer uso.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «EFAMA member associations national fund associations list»; WebFetch: sí, página índice de miembros de EFAMA)
- **Origen:** Alta F9_S4 (2026-11-02).

#### RF-0539 · Q 65 (B) — APFIPP — fondos de inversión, pensiones y patrimonios en Portugal

- **Canal oficial (URL raíz):** http://www.apfipp.pt/index.aspx?MenuCode=bottomHomePage (enlazada desde el listado oficial de miembros de EFAMA: https://www.efama.org/about-us/our-members)
- **Emisor:** Associação Portuguesa de Fundos de Investimento, Pensões e Patrimónios (APFIPP)
- **Documentación y notas:** Asociación nacional de fondos y gestión de activos de Portugal, miembro de EFAMA; fuente de las estadísticas nacionales que EFAMA (RF-0345) agrega en sus informes mensuales y trimestrales. Cubre también fondos de pensiones y fondos inmobiliarios portugueses.
- **Temática:** TF-16 Fondos y ETF: datos, flujos y categorías (principal) · secundarias: —
- **Calidad Q:** 65 (B) — Primariedad 15/20 · Historial 10/20 · Transparencia 10/15 · Autoridad 10/15 · Independencia 5/10 · Actualidad 7/10 · Acceso 8/10
- **Tipología:** secundaria (patronal; datos de sus asociados)
- **Acceso:** Abierto (web oficial; algunos informes solo para socios)
- **Ámbitos:** Patrimonio y flujos de fondos domiciliados o comercializados en Portugal
- **Motivo de inclusión y uso:** Desglose nacional de flujos y patrimonio por categoría cuando el agregado europeo de EFAMA no basta. AG-22.
- **Restricciones de uso:** Uso con atribución.
- **Sesgos y cautelas:** Patronal del sector (interés promocional). La web oficial no se cargó en esta sesión: la existencia y la URL se confirmaron por lectura lateral en el listado de EFAMA; comprobar la sección estadística y su periodicidad en el primer uso.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «EFAMA member associations national fund associations list»; WebFetch: sí, página índice de miembros de EFAMA)
- **Origen:** Alta F9_S4 (2026-11-02).

#### RF-0538 · Q 63 (C) — DUFAS (Dutch Fund and Asset Management Association) — gestión de activos en los Países Bajos

- **Canal oficial (URL raíz):** https://www.dufas.nl/ (enlazada desde el listado oficial de miembros de EFAMA: https://www.efama.org/about-us/our-members)
- **Emisor:** Dutch Fund and Asset Management Association (DUFAS)
- **Documentación y notas:** Asociación nacional de fondos y gestión de activos de los Países Bajos, miembro de EFAMA; fuente de las estadísticas nacionales que EFAMA (RF-0345) agrega en sus informes mensuales y trimestrales. Mercado dominado por la gestión institucional para fondos de pensiones.
- **Temática:** TF-16 Fondos y ETF: datos, flujos y categorías (principal) · secundarias: —
- **Calidad Q:** 63 (C) — Primariedad 14/20 · Historial 10/20 · Transparencia 10/15 · Autoridad 10/15 · Independencia 5/10 · Actualidad 6/10 · Acceso 8/10
- **Tipología:** secundaria (patronal; datos de sus asociados)
- **Acceso:** Abierto (web oficial; algunos informes solo para socios)
- **Ámbitos:** Patrimonio y flujos de fondos domiciliados o comercializados en los Países Bajos
- **Motivo de inclusión y uso:** Desglose nacional de flujos y patrimonio por categoría cuando el agregado europeo de EFAMA no basta. AG-22.
- **Restricciones de uso:** Uso con atribución.
- **Sesgos y cautelas:** Patronal del sector (interés promocional). La web oficial no se cargó en esta sesión: la existencia y la URL se confirmaron por lectura lateral en el listado de EFAMA; comprobar la sección estadística y su periodicidad en el primer uso.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «EFAMA member associations national fund associations list»; WebFetch: sí, página índice de miembros de EFAMA)
- **Origen:** Alta F9_S4 (2026-11-02).

## TF-17 Derivados y volatilidad: mercados y datos

#### RF-0540 · Q 88 (A) — BIS — estadísticas de derivados OTC (semestrales) y Encuesta Trienal

- **Canal oficial (URL raíz):** https://www.bis.org/publ/otc_hy2512.htm (comentario más reciente: https://www.bis.org/stats_derivatives_commentaries/latest.htm · tablas: https://data.bis.org/topics/OTC_DER/tables-and-dashboards/BIS,DER_D9,1.0 · derivados negociados en bolsa, según la página índice de ISDA: http://www.bis.org/statistics/extderiv.htm)
- **Emisor:** Bank for International Settlements (BIS)
- **Documentación y notas:** Estadística semestral (junio y diciembre) de importes nocionales y valores brutos de mercado de derivados OTC por riesgo (tipos, divisas, renta variable, materias primas, CDS), con 12 países y 65 dealers declarantes; ampliada cada tres años por la Encuesta Trienal (más de 30 jurisdicciones adicionales). Publicación de 08/12/2025 (fin de junio de 2025): 846 billones de dólares de nocional (+16 %), 21,8 billones de valor bruto de mercado (+29 %), tipos de interés el 79 % del total. Pieza temática de RF-0003 (portal general de estadísticas del BIS), registrada aparte como RF-0070.
- **Temática:** TF-17 Derivados y volatilidad: mercados y datos (principal) · secundarias: TF-01
- **Calidad Q:** 88 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 15/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 8/10 · Acceso 10/10
- **Tipología:** primaria (estadística oficial coordinada por bancos centrales)
- **Acceso:** Abierto (API y descargas en data.bis.org)
- **Ámbitos:** Tamaño, composición y riesgo de contraparte del mercado mundial de derivados OTC
- **Motivo de inclusión y uso:** Medida de referencia del tamaño y la evolución de los mercados de swaps, opciones OTC y CDS. AG-23, AG-25.
- **Restricciones de uso:** Uso libre con atribución.
- **Sesgos y cautelas:** Semestral con unos cinco meses de desfase; los años entre encuestas trienales incluyen estimaciones.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «BIS OTC derivatives statistics end-June 2026 notional ISDA SwapsInfo»; WebFetch: sí)
- **Origen:** Alta F9_S4 (2026-11-02).

#### RF-0541 · Q 87 (A) — CFTC — Weekly Swaps Report

- **Canal oficial (URL raíz):** https://www.cftc.gov/index.php/MarketReports/SwapsReports/index.htm (archivo: https://www.cftc.gov/MarketReports/SwapsReports/Archive/index.htm)
- **Emisor:** U.S. Commodity Futures Trading Commission (CFTC)
- **Documentación y notas:** Informe semanal (lunes, 15:30 ET) con nocional bruto vivo por tipo de participante, estado de compensación y producto (últimas cinco semanas) y volumen de transacciones de swaps de tipos, CDS y swaps de divisas (importe y número de operaciones), a partir de los registros de swaps (CME SDR, DTCC Data Repository, ICE Trade Vault); archivo completo desde su inicio. Canal distinto de RF-0049 (COT).
- **Temática:** TF-17 Derivados y volatilidad: mercados y datos (principal) · secundarias: TF-06
- **Calidad Q:** 87 (A) — Primariedad 19/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 10/10 · Acceso 9/10
- **Tipología:** primaria (agregación supervisora de datos de registros)
- **Acceso:** Abierto
- **Ámbitos:** Swaps de tipos, crédito y divisas bajo jurisdicción de la CFTC
- **Motivo de inclusión y uso:** Pulso semanal de la actividad de swaps (cobertura de tipos, demanda de protección de crédito). AG-23, AG-25.
- **Restricciones de uso:** Dominio público.
- **Sesgos y cautelas:** Solo swaps declarados bajo reglas de la CFTC (no cubre swaps basados en valores de la SEC); cambios de registros afectan a la serie.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Bloomberg SDR operó entre 2014 y 2018.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «CFTC Weekly Swaps Report interest rate swaps notional»; WebFetch: sí)
- **Origen:** Alta F9_S4 (2026-11-02).

#### RF-0547 · Q 85 (A) — OCC (Office of the Comptroller of the Currency) — Quarterly Report on Bank Trading and Derivatives Activities

- **Canal oficial (URL raíz):** https://occ.gov/publications-and-resources/publications/quarterly-report-on-bank-trading-and-derivatives-activities/index-quarterly-report-on-bank-trading-and-derivatives-activities.html (archivo histórico en el mismo directorio, p. ej. https://www.occ.gov/publications-and-resources/publications/quarterly-report-on-bank-trading-and-derivatives-activities/files/q2-2013-derivatives-quarterly.html)
- **Emisor:** Office of the Comptroller of the Currency (Tesoro de EE. UU.)
- **Documentación y notas:** Informe trimestral, basado en los informes de condición (Call Reports) de bancos y holdings, con importes nocionales de derivados por tipo y contrato, exposición crediticia, concentración en los mayores bancos e ingresos de trading; serie disponible desde 1995. Ediciones vigentes: primer y segundo trimestre de 2026 (la del segundo trimestre, difundida en septiembre de 2026). No confundir con The Options Clearing Corporation (RF-0463).
- **Temática:** TF-17 Derivados y volatilidad: mercados y datos (principal) · secundarias: TF-02
- **Calidad Q:** 85 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 8/10 · Acceso 8/10
- **Tipología:** primaria (datos supervisores de informes de condición bancaria)
- **Acceso:** Abierto y gratuito
- **Ámbitos:** Derivados en balance de los bancos de EE. UU.; ingresos de trading
- **Motivo de inclusión y uso:** Concentración, volumen nocional y riesgo de contraparte de derivados en el sistema bancario estadounidense; ingresos de trading como termómetro de la actividad de los dealers. AG-23, AG-14.
- **Restricciones de uso:** Dominio público.
- **Sesgos y cautelas:** Solo entidades con licencia federal o holdings de EE. UU.; el nocional sobrestima el riesgo económico (compresión y compensación). La página índice no cargó en esta sesión (error del servidor); URL vigente confirmada en los resultados de búsqueda junto con la cobertura de prensa de las ediciones de 2026.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Migración del sitio de occ.treas.gov a occ.gov (URL antigua sustituida en esta revisión).
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «OCC Quarterly Report on Bank Trading and Derivatives Activities 2026»; WebFetch: intento fallido, error del servidor de occ.gov)
- **Origen:** Alta F9_S4 (2026-11-02); reescrita F9_S6 (2026-11-02): URL reparada.

#### RF-0560 · Q 84 (A) — ESMA — Annual Statistical Report on EU Derivatives Markets (datos EMIR) y ESMA Statistics on Securities and Markets

- **Canal oficial (URL raíz):** https://www.esma.europa.eu/sites/default/files/library/esma50_157_2025_asr_derivatives.pdf (edición de 2019, datos de 2018) · ediciones de 2020 y 2021: https://www.esma.europa.eu/sites/default/files/library/esma50-165-1362_asr_derivatives_2020.pdf y https://www.esma.europa.eu/sites/default/files/library/esma50-165-2001_emir_asr_derivatives_2021.pdf · estadística estructural más reciente (12/12/2025, tabla 7 de derivados): https://www.esma.europa.eu/sites/default/files/2025-12/ESMA11-239717167-20877_ESMA_statistics_on_securities_and_markets.pdf
- **Emisor:** European Securities and Markets Authority (ESMA)
- **Documentación y notas:** Informe estadístico anual sobre los derivados de la UE a partir de los datos de los registros de operaciones bajo EMIR: nocional vivo, número de operaciones, reparto por clase de activo, compensación central, negociación en plataforma y contrapartes (edición de 2019: 735 billones de euros a fin de 2018; tipos de interés 76 %; 63 % del nocional OTC de tipos compensado centralmente, 25 % en crédito). La «ESMA Statistics on Securities and Markets» de diciembre de 2025 actualiza el nocional del EEE30 a 27/12/2024: 29,0 millones de contratos y 379.140 miles de millones de euros (tipos 314.569).
- **Temática:** TF-17 Derivados y volatilidad: mercados y datos (principal) · secundarias: TF-02, TF-19
- **Calidad Q:** 84 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 6/10 · Acceso 9/10
- **Tipología:** primaria (estadística supervisora sobre datos regulatorios)
- **Acceso:** Abierto y gratuito (PDF)
- **Ámbitos:** Derivados OTC y cotizados de la UE/EEE por clase de activo; compensación central
- **Motivo de inclusión y uso:** Fuente europea oficial del tamaño y la estructura del mercado de derivados de la UE, complementaria de BIS (RF-0540) y de los datos de EE. UU. (RF-0541). AG-23, AG-25.
- **Restricciones de uso:** Uso libre con atribución.
- **Sesgos y cautelas:** Calidad de datos de EMIR mejorable (ESMA lo reconoce); cifras de distintas ediciones no siempre comparables por cambios de perímetro y metodología; la serie de informes anuales específicos parece más espaciada (última edición específica no confirmada en esta sesión). Pieza distinta de RF-0027 (informes de tendencias y riesgos).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Cambios de perímetro tras el Brexit y con EMIR Refit.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «ESMA Annual Statistical Report EU derivatives markets 2025 EMIR data»; WebFetch: sí, PDF de la edición de 2019 y PDF de la estadística de diciembre de 2025)
- **Origen:** Alta F9_S6 (2026-11-02), sustituta de RF-0557.

#### RF-0546 · Q 83 (A) — Deutsche Bundesbank — estadística de derivados OTC (contribución a la encuesta semestral del BIS)

- **Canal oficial (URL raíz):** https://www.bundesbank.de/en/statistics/banks-and-other-financial-corporations/banks/otc-derivatives/otc-derivatives-793960 (sección: https://bundesbank.de/en/statistics/banks-and-other-financial-corporations/banks/otc-derivatives)
- **Emisor:** Deutsche Bundesbank
- **Documentación y notas:** Estadística semestral de nocionales y valores brutos de mercado de derivados OTC (divisas, tipos, renta variable, materias primas y crédito) y exposiciones crediticias antes y después de compensación, dentro del ejercicio coordinado por el BIS; tablas en la serie estadística de banca y series en el portal estadístico; directrices (en alemán) de 01/07/2026.
- **Temática:** TF-17 Derivados y volatilidad: mercados y datos (principal) · secundarias: TF-01
- **Calidad Q:** 83 (A) — Primariedad 19/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 6/10 · Acceso 9/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** Derivados OTC de los dealers alemanes
- **Motivo de inclusión y uso:** Desglose nacional europeo del mercado OTC (complemento de RF-0540). AG-23.
- **Restricciones de uso:** Uso libre con atribución.
- **Sesgos y cautelas:** Semestral; la página no indica la última fecha de referencia.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Directrices actualizadas en julio de 2026.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «BIS OTC derivatives statistics end-June 2026 notional ISDA SwapsInfo»; WebFetch: sí)
- **Origen:** Alta F9_S4 (2026-11-02).

#### RF-0543 · Q 82 (A) — Eurex — estadísticas mensuales y diarias de derivados

- **Canal oficial (URL raíz):** https://www.eurex.com/ (estadística de septiembre de 2026: https://www.eurex.com/resource/blob/5619300/123b20220f20deb12dc1bbf726359039/data/monthlystat_202609.pdf · estadísticas en línea: https://www.eurex.com/ex-en/data/statistics/market-statistics-online/100!onlineStats · nota de cifras de junio de 2026: https://www.eurex.com/ec-en/find/news/June-2026-figures-at-Eurex-5368808)
- **Emisor:** Eurex Frankfurt AG (Deutsche Börse Group)
- **Documentación y notas:** Estadística mensual por segmento (septiembre de 2026: 273 millones de contratos, +45,2 % interanual; 168,2 millones de derivados de tipos, 72,0 millones de índices, 32,8 millones de acciones; derivados de índices de volatilidad como VSTOXX), interés abierto y estadísticas diarias en línea por producto (incluidos futuros sobre EURO STOXX 50, Bund, Schatz, Bobl y Buxl).
- **Temática:** TF-17 Derivados y volatilidad: mercados y datos (principal) · secundarias: TF-06
- **Calidad Q:** 82 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 14/15 · Independencia 7/10 · Actualidad 9/10 · Acceso 9/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** Derivados europeos de tipos, índices, acciones, volatilidad y dividendos
- **Motivo de inclusión y uso:** Actividad e interés abierto de los derivados de referencia europeos (cobertura de tipos alemanes, volatilidad europea). AG-23, AG-25.
- **Restricciones de uso:** Uso con atribución.
- **Sesgos y cautelas:** Operador de mercado (comunicación orientada a récords).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Eurex MEFF monthly derivatives statistics volume open interest 2026»; WebFetch: sí, PDF de septiembre de 2026)
- **Origen:** Alta F9_S4 (2026-11-02).

#### RF-0544 · Q 81 (A) — Eurex Clearing — volúmenes mensuales de compensación (derivados cotizados, OTC IRD y repo)

- **Canal oficial (URL raíz):** https://www.eurex.com/resource/blob/5564302/b71fcc143858aa62aa61597691620c71/data/ecag_clearing_volumes_2026_08.pdf
- **Emisor:** Eurex Clearing AG (Deutsche Börse Group)
- **Documentación y notas:** «Monthly Clearing Volumes 2026» (datos hasta septiembre de 2026): derivados cotizados por segmento, derivados OTC de tipos de interés (64.888 miles de millones de euros de nocional en el año; compresión de 40.132), valores de Xetra y FWB y repo (saldo medio diario de 982 a 1.245 miles de millones de euros entre enero y septiembre). Pertinente para la relocalización de la compensación de swaps en euros a la UE.
- **Temática:** TF-17 Derivados y volatilidad: mercados y datos (principal) · secundarias: TF-18
- **Calidad Q:** 81 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 14/15 · Independencia 7/10 · Actualidad 9/10 · Acceso 9/10
- **Tipología:** primaria
- **Acceso:** Abierto (PDF)
- **Ámbitos:** Compensación central de derivados en euros (cotizados y OTC) y repo
- **Motivo de inclusión y uso:** Cuota de la UE en la compensación de swaps en euros y dinámica del repo compensado. AG-23, AG-24.
- **Restricciones de uso:** Uso con atribución.
- **Sesgos y cautelas:** Unidades no siempre rotuladas en las tablas; dobles cómputos en repo.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Eurex MEFF monthly derivatives statistics volume open interest 2026»; WebFetch: sí)
- **Origen:** Alta F9_S4 (2026-11-02).

#### RF-0552 · Q 80 (A) — ESMA — intervención de producto sobre CFD y opciones binarias

- **Canal oficial (URL raíz):** https://esma.europa.eu/investor-corner/product-intervention (también https://www.esma.europa.eu/node/200006 · opinión sobre las medidas españolas de CFD: https://www.esma.europa.eu/sites/default/files/library/esma-35-43-1935-esma_opinion_under_article_432_mifir_es_cfd.pdf)
- **Emisor:** European Securities and Markets Authority (ESMA)
- **Documentación y notas:** Página de intervención de producto: medidas temporales de ESMA (2018-2019) sobre CFD y opciones binarias a minoristas (límites de apalancamiento, cierre de posiciones por margen, protección de saldo negativo, advertencia con el porcentaje de cuentas con pérdidas), medidas nacionales permanentes adoptadas después por las autoridades competentes y opiniones de ESMA sobre ellas (art. 43 MiFIR).
- **Temática:** TF-17 Derivados y volatilidad: mercados y datos (principal) · secundarias: TF-02
- **Calidad Q:** 80 (A) — Primariedad 18/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 5/10 · Acceso 8/10
- **Tipología:** primaria (normativa supervisora)
- **Acceso:** Abierto
- **Ámbitos:** Derivados minoristas apalancados (CFD, opciones binarias) en la UE
- **Motivo de inclusión y uso:** Marco regulatorio que delimita el acceso minorista a derivados apalancados en Europa. AG-23.
- **Restricciones de uso:** Uso libre con atribución.
- **Sesgos y cautelas:** La página no cargó en esta sesión (error del sitio); contenido confirmado por resultados de búsqueda. Pieza temática distinta de RF-0027.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Medidas temporales de ESMA sustituidas por medidas nacionales.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «ESMA CFD product intervention measures retail investors national competent authorities»; WebFetch: intento fallido, error del sitio)
- **Origen:** Alta F9_S4 (2026-11-02).

#### RF-0554 · Q 80 (A) — V-Lab (NYU Stern) — análisis y previsiones de volatilidad, correlación y riesgo sistémico

- **Canal oficial (URL raíz):** https://vlab.stern.nyu.edu/ (ayuda del resumen de volatilidad: https://vlab.stern.nyu.edu/help/volatility_summary · análisis: https://vlab.stern.nyu.edu/help/volatility_analysis)
- **Emisor:** V-Lab, NYU Stern School of Business (Volatility Institute)
- **Documentación y notas:** Doce modelos de volatilidad (GARCH, GJR-GARCH por defecto, EGARCH, APARCH, Spline-GARCH, MEM, GAS, MF2-GARCH) reestimados a diario tras el cierre, con previsiones a 1 día, 1 semana, 1 mes, 6 meses y 1 año para miles de activos; además análisis de correlación, VaR a largo plazo y SRISK (riesgo sistémico).
- **Temática:** TF-17 Derivados y volatilidad: mercados y datos (principal) · secundarias: TF-13
- **Calidad Q:** 80 (A) — Primariedad 14/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 13/15 · Independencia 10/10 · Actualidad 10/10 · Acceso 9/10
- **Tipología:** analítica (modelos académicos sobre precios de mercado)
- **Acceso:** Abierto
- **Ámbitos:** Volatilidad realizada y prevista de acciones, índices, divisas, materias primas
- **Motivo de inclusión y uso:** Contraste de la volatilidad implícita (VIX y similares) con previsiones econométricas; régimen de volatilidad por mercado. AG-23, AG-25.
- **Restricciones de uso:** Uso académico con atribución.
- **Sesgos y cautelas:** Resultados dependientes del modelo; algunos activos inactivos conservan su último valor.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «V-Lab NYU Stern volatility laboratory GARCH forecasts»; WebFetch: sí)
- **Origen:** Alta F9_S4 (2026-11-02).

#### RF-0549 · Q 78 (B) — LCH (LSEG) — estadísticas de volumen de SwapClear

- **Canal oficial (URL raíz):** https://www.lseg.com/en/post-trade/clearing/lch-services/swapclear/volumes (productos de datos de volumen: https://www.lseg.com/en/post-trade/clearing/lch-services/swapclear/volumes/volume-data-products)
- **Emisor:** LCH Ltd (LCH Group, London Stock Exchange Group)
- **Documentación y notas:** Tablas mensuales de nocional registrado, nocional vivo, operaciones registradas y operaciones vivas de SwapClear, en dólares y en divisa base, separando servicio total y clientes; SwapClear declara compensar más del 50 % de todos los swaps de tipos OTC y más del 90 % del mercado compensado, con más de 3,5 billones de dólares de nocional diario y más de 3 millones de operaciones vivas. Notas metodológicas: cifras tras la novación a la cámara; los volúmenes de clientes cuentan solo el lado del cliente; conversión a dólares con tipos diarios.
- **Temática:** TF-17 Derivados y volatilidad: mercados y datos (principal) · secundarias: TF-19
- **Calidad Q:** 78 (B) — Primariedad 19/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 13/15 · Independencia 7/10 · Actualidad 9/10 · Acceso 7/10
- **Tipología:** primaria
- **Acceso:** Abierto (tablas web); productos de datos detallados de pago
- **Ámbitos:** Swaps de tipos compensados por divisa (incluidos OIS)
- **Motivo de inclusión y uso:** Actividad de cobertura de tipos por divisa y competencia Londres-UE en la compensación de swaps en euros (contraste con RF-0544). AG-23, AG-25.
- **Restricciones de uso:** Uso con atribución.
- **Sesgos y cautelas:** Operador de mercado (comunicación orientada a récords); las tablas se despliegan en la página y no se extraen como texto; doble cómputo propio de la novación.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** LCH.Clearnet renombrada LCH; propiedad de LSEG; la web de LCH se integró en lseg.com (URL antigua sustituida en esta revisión).
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «LCH SwapClear volumes cleared notional statistics LSEG»; WebFetch: sí)
- **Origen:** Alta F9_S4 (2026-11-02); reescrita F9_S6 (2026-11-02): URL reparada.

#### RF-0556 · Q 78 (B) — CME Group — swaps de tipos de interés compensados (Cleared OTC IRS): volumen, interés abierto y curvas

- **Canal oficial (URL raíz):** https://www.cmegroup.com/trading/interest-rates/cleared-otc (seguimiento de volumen OTC: https://www.cmegroup.com/education/cme-volume-oi-records.html · histórico mensual 2013-2018: https://www.cmegroup.com/education/files/otc-irs-complete-history-2013-2018.xlsx · curvas IRS: https://www.cmegroup.com/ftp/irs/ · metodología de curvas: https://www.cmegroup.com/trading/interest-rates/files/irs-curve-building-methodology.pdf · boletín diario de swaps solo compensados: https://www.cmegroup.com/daily_bulletin/current/Section67_OTC_Cleared_Only.pdf)
- **Emisor:** CME Group (CME Clearing)
- **Documentación y notas:** Compensación de swaps de tipos en 24 divisas (fijo/flotante, cupón cero, OIS sobre SOFR, Fed Funds, SONIA, €STR, TONA, SARON, CORRA y otros, swaps de base y FRA), con datos diarios de volumen e interés abierto por divisa (incluidas las reducciones por compresión multilateral, p. ej. la del 28/10/2026 en COP), curvas de valoración y ahorro de márgenes frente a los futuros de tipos cotizados. Canal distinto de RF-0346 (FedWatch) y de RF-0562 (CVOL).
- **Temática:** TF-17 Derivados y volatilidad: mercados y datos (principal) · secundarias: TF-19
- **Calidad Q:** 78 (B) — Primariedad 19/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 13/15 · Independencia 7/10 · Actualidad 9/10 · Acceso 7/10
- **Tipología:** primaria
- **Acceso:** Abierto (página y curvas); series diarias en CME DataMine con registro o licencia
- **Ámbitos:** Swaps de tipos compensados en dólares y otras 23 divisas
- **Motivo de inclusión y uso:** Complemento de LCH SwapClear (RF-0549) y Eurex Clearing (RF-0544) para la cuota y actividad de la compensación de swaps de tipos; curvas OIS de referencia. AG-23, AG-25.
- **Restricciones de uso:** Uso con atribución; datos de mercado bajo licencia.
- **Sesgos y cautelas:** Operador de mercado; las tablas de datos por divisa no se extraen como texto. Se excluyen los antiguos informes de CDS (CME cerró la compensación de CDS en 2018) y de ClearPort, no confirmados en esta revisión.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Reorganización de la web de CME (URL antiguas sustituidas en esta revisión); cese de la compensación de CDS (2018).
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «CME Group interest rate swaps clearing OTC IRS open interest record 2026»; WebFetch: sí, página Cleared OTC IRS y boletín diario del 30/10/2026)
- **Origen:** Alta F9_S4 (2026-11-02); reescrita F9_S6 (2026-11-02): URL reparada y alcance acotado a IRS.

#### RF-0551 · Q 77 (B) — MEFF (BME) — mercado español de derivados financieros

- **Canal oficial (URL raíz):** https://www.meff.es/ing/Financial-Derivatives/Market-Prices (redirige, 302, a https://www.bolsasymercados.es/en/bme-exchange/prices-and-markets/meff/equities.html)
- **Emisor:** MEFF Sociedad Rectora del Mercado de Productos Derivados (BME, grupo SIX)
- **Documentación y notas:** Precios de mercado de los derivados sobre renta variable negociados en MEFF (futuros y opciones sobre IBEX 35 y sus variantes mini y micro, futuros y opciones sobre acciones); los subyacentes se rigen por las normas técnicas de RF-0504 (incluidos índices de estrategia de opciones y VIBEX).
- **Temática:** TF-17 Derivados y volatilidad: mercados y datos (principal) · secundarias: TF-15
- **Calidad Q:** 77 (B) — Primariedad 20/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 13/15 · Independencia 7/10 · Actualidad 8/10 · Acceso 7/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** Derivados sobre renta variable española
- **Motivo de inclusión y uso:** Actividad, precios y volatilidad implícita del mercado de derivados español. AG-23.
- **Restricciones de uso:** Uso con atribución.
- **Sesgos y cautelas:** La página de destino no se pudo cargar (fuera de la lista permitida); confirmada por resultados de búsqueda y redirección observada.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Integración de la web de MEFF en bolsasymercados.es.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Eurex MEFF monthly derivatives statistics volume open interest 2026»; WebFetch: redirección observada, destino no admitido)
- **Origen:** Alta F9_S4 (2026-11-02).

#### RF-0542 · Q 76 (B) — FIA — informes mensuales y anuales de volumen de derivados cotizados (ETD Volume)

- **Canal oficial (URL raíz):** https://www.fia.org/etd-volume-reports (informe de diciembre de 2025: https://www.fia.org/fia/articles/etd-volume-december-2025 · resumen anual: https://fia.org/node/2439 · datos: https://www.fia.org/data-1)
- **Emisor:** FIA (Futures Industry Association)
- **Documentación y notas:** Informes mensuales y anuales de volumen e interés abierto de futuros y opciones cotizados por región, clase de activo y bolsa (ETD Tracker). 2025: 119,29 miles de millones de contratos (−42,2 %; opciones −50,3 % por la caída de opciones sobre índices en la India; futuros +8,6 %), interés abierto de 1,52 miles de millones de contratos a fin de diciembre (+22,8 %).
- **Temática:** TF-17 Derivados y volatilidad: mercados y datos (principal) · secundarias: TF-06
- **Calidad Q:** 76 (B) — Primariedad 17/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 14/15 · Independencia 6/10 · Actualidad 9/10 · Acceso 8/10
- **Tipología:** secundaria (agregación de datos de bolsas)
- **Acceso:** Resúmenes abiertos; ETD Tracker con detalle por bolsa
- **Ámbitos:** Derivados cotizados mundiales
- **Motivo de inclusión y uso:** Panorama mundial de la actividad de derivados cotizados por región y clase de activo. AG-23.
- **Restricciones de uso:** Uso con atribución.
- **Sesgos y cautelas:** Patronal del sector; el recuento por contratos mezcla tamaños nominales muy distintos.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «FIA annual global futures and options volume 2025 exchange-traded derivatives WFE derivatives report»; WebFetch: sí)
- **Origen:** Alta F9_S4 (2026-11-02).

#### RF-0545 · Q 76 (B) — ISDA — investigación y SwapsInfo (volúmenes de derivados OTC)

- **Canal oficial (URL raíz):** https://www.isda.org/ (revisión SwapsInfo del 1S 2026, 11/08/2026: https://www.isda.org/2026/08/11/swapsinfo-first-half-of-2026-and-the-second-quarter-of-2026-review/ · SwapsInfo: https://www.swapsinfo.org/ · directorio de fuentes de datos OTC: https://www.isda.org/1985/01/01/otc-derivatives-data-sources · encuestas: https://www.isda.org/category/research/surveys/)
- **Emisor:** International Swaps and Derivatives Association (ISDA)
- **Documentación y notas:** SwapsInfo: volúmenes y número de operaciones de derivados de tipos y de crédito a partir de datos públicos de registros (1S 2026: 318,5 billones de dólares negociados en derivados de tipos, +27,3 %, impulsados por OIS; 12,5 billones en índices de crédito, +18,5 %); revisiones trimestrales, encuesta de márgenes y notas de tendencias clave; directorio de fuentes de datos OTC.
- **Temática:** TF-17 Derivados y volatilidad: mercados y datos (principal) · secundarias: TF-19
- **Calidad Q:** 76 (B) — Primariedad 17/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 14/15 · Independencia 5/10 · Actualidad 9/10 · Acceso 9/10
- **Tipología:** secundaria (agregación de datos públicos por la patronal)
- **Acceso:** Abierto
- **Ámbitos:** Swaps de tipos, CDS sobre índices y single-name
- **Motivo de inclusión y uso:** Actividad de swaps por producto y divisa y tendencias del mercado OTC. AG-23, AG-25.
- **Restricciones de uso:** Uso con atribución.
- **Sesgos y cautelas:** Patronal de los dealers (posiciones de lobby en sus análisis); datos basados en registros de EE. UU.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «BIS OTC derivatives statistics end-June 2026 notional ISDA SwapsInfo»; WebFetch: sí, revisión SwapsInfo y directorio)
- **Origen:** Alta F9_S4 (2026-11-02).

#### RF-0550 · Q 76 (B) — ICE — Report Center (datos de futuros y de compensación de CDS)

- **Canal oficial (URL raíz):** https://www.theice.com/marketdata/reports/ReportCenter.shtml (según la página índice de ISDA «OTC derivatives data sources»)
- **Emisor:** Intercontinental Exchange (ICE Futures Europe, ICE Futures U.S., ICE Clear Credit)
- **Documentación y notas:** Centro de informes con volúmenes, interés abierto y datos de liquidación de los futuros y opciones de ICE (Brent, gasóleo, tipos a corto en libras y euros, índices) y datos de compensación de CDS de ICE Clear Credit. ICE Trade Vault es uno de los registros que alimentan RF-0541.
- **Temática:** TF-17 Derivados y volatilidad: mercados y datos (principal) · secundarias: TF-08
- **Calidad Q:** 76 (B) — Primariedad 19/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 14/15 · Independencia 7/10 · Actualidad 8/10 · Acceso 6/10
- **Tipología:** primaria
- **Acceso:** Abierto con registro para algunos informes
- **Ámbitos:** Futuros de energía, tipos a corto plazo europeos, índices; CDS compensados
- **Motivo de inclusión y uso:** Interés abierto y volúmenes de los contratos de referencia de ICE (STIR en libras y euros, energía). AG-23, AG-24.
- **Restricciones de uso:** Uso con atribución; datos bajo licencia.
- **Sesgos y cautelas:** URL de una página índice (no cargada en esta sesión); operador con negocio de índices (RF-0506).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Absorción de LIFFE e IPE en ICE Futures Europe.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «BIS OTC derivatives statistics end-June 2026 notional ISDA SwapsInfo»; WebFetch: sí, página índice de ISDA)
- **Origen:** Alta F9_S4 (2026-11-02).

#### RF-0555 · Q 76 (B) — Credit Derivatives Determinations Committees (ISDA DC) — determinaciones de eventos de crédito

- **Canal oficial (URL raíz):** https://dc.isda.org/ (según la página índice de ISDA «OTC derivatives data sources»)
- **Emisor:** Credit Derivatives Determinations Committees (constituidos bajo las reglas de ISDA)
- **Documentación y notas:** Publica las preguntas y decisiones sobre eventos de crédito (impago, reestructuración, sucesión) que activan los CDS, con convocatorias de subastas de liquidación por región.
- **Temática:** TF-17 Derivados y volatilidad: mercados y datos (principal) · secundarias: TF-19
- **Calidad Q:** 76 (B) — Primariedad 20/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 14/15 · Independencia 6/10 · Actualidad 7/10 · Acceso 7/10
- **Tipología:** primaria (decisiones vinculantes para contratos CDS)
- **Acceso:** Abierto
- **Ámbitos:** Eventos de crédito corporativos y soberanos
- **Motivo de inclusión y uso:** Hechos que liquidan coberturas de crédito (soberanos en crisis, reestructuraciones). AG-23, AG-25.
- **Restricciones de uso:** Uso con atribución.
- **Sesgos y cautelas:** Comités formados por dealers y compradores de protección (conflictos de interés señalados en casos polémicos); no cargada en esta sesión (dominio fuera de la lista permitida).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Cambios de secretaría administrativa de los comités a lo largo del tiempo.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «BIS OTC derivatives statistics end-June 2026 notional ISDA SwapsInfo»; WebFetch: sí, página índice de ISDA; intento sobre dc.isda.org no admitido)
- **Origen:** Alta F9_S4 (2026-11-02).

#### RF-0562 · Q 76 (B) — CME Group — CVOL (CME Group Volatility Indexes): volatilidad implícita de tipos, divisas y materias primas

- **Canal oficial (URL raíz):** https://www.cmegroup.com/market-data/cme-group-benchmark-administration/cme-group-volatility-indexes-faq.html (introducción: https://www.cmegroup.com/education/articles-and-reports/introduction-to-the-cme-group-volatility-index-cvol.html · guía de cálculo en tiempo real: https://www.cmegroup.com/market-data/cme-group-benchmark-administration/files/live-streaming-index-calculation-guide.pdf)
- **Emisor:** CME Group Benchmark Administration Limited (CBA)
- **Documentación y notas:** Familia de índices de volatilidad implícita a 30 días basados en varianza simple (admite precios negativos) calculados con opciones sobre futuros: tipos (STIR y bonos del Tesoro, p. ej. el de 10 años), divisas G5, agrícolas, energía, metales y un índice transversal de materias primas (32 productos más 6 índices amplios). Publica además UpVar/DnVar, sesgo (skew), convexidad y volatilidad ATM. Índices de cierre registrados bajo el BMR del Reino Unido y diseñados según los principios de IOSCO; los CVOL de Eurodólar dejaron de publicarse (historia en DataMine).
- **Temática:** TF-17 Derivados y volatilidad: mercados y datos (principal) · secundarias: TF-19, TF-08
- **Calidad Q:** 76 (B) — Primariedad 18/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 13/15 · Independencia 6/10 · Actualidad 10/10 · Acceso 6/10
- **Tipología:** primaria (índice de referencia calculado sobre precios de opciones cotizadas)
- **Acceso:** Visualizador web con últimos valores (solo consulta, no comercial); histórico de cierre en CME DataMine con registro; flujo en tiempo real vía redistribuidores
- **Ámbitos:** Volatilidad implícita de tipos de interés, divisas y materias primas
- **Motivo de inclusión y uso:** Medida homogénea de volatilidad implícita fuera de la renta variable (complemento del VIX y del MOVE, RF-0561), con sesgo put/call por mercado. AG-23, AG-25.
- **Restricciones de uso:** Visualizador solo para referencia; uso comercial con licencia.
- **Sesgos y cautelas:** Administrador que es a la vez la bolsa que lista las opciones subyacentes; historia relativamente corta (desde 2020); no comparable directamente con índices de varianza logarítmica como el VIX.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Cese de los CVOL de Eurodólar tras la transición del LIBOR.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «CME Group CVOL index methodology implied volatility rates FX commodities»; WebFetch: sí, FAQ de CVOL)
- **Origen:** Alta F9_S6 (2026-11-02), sustituta de RF-0559.

#### RF-0548 · Q 72 (B) — DTCC — CDS Kinetics (datos agregados del Trade Information Warehouse)

- **Canal oficial (URL raíz):** https://www.dtcc.com/data-services/market-aggregates-and-analytics/cds-kinetics (ficha del servicio: https://www.dtcc.com/-/media/Files/Downloads/Data-Services/dtccdata/CDS_Kinetics_factsheet.pdf · ficha del Trade Information Warehouse: https://www.dtcc.com/-/media/Files/Downloads/Data-and-Repository-Services/TIW/TIW-FS.pdf)
- **Emisor:** The Depository Trust & Clearing Corporation (DTCC)
- **Documentación y notas:** Servicio de datos construido sobre las posiciones del Trade Information Warehouse (TIW), que DTCC estima en ~98 % de los CDS vivos del mundo: nocional bruto y neto y volúmenes de más de 1.700 instrumentos (índices, single-name corporativos y soberanos, tramos), por sector, tipo de mercado y región, con más de diez años de series e informes semanales de saldos y volúmenes; posiciones anonimizadas de más de 2.500 participantes. DTCC Data Repository es además uno de los registros que alimentan el Weekly Swaps Report de la CFTC (RF-0541).
- **Temática:** TF-17 Derivados y volatilidad: mercados y datos (principal) · secundarias: TF-19
- **Calidad Q:** 72 (B) — Primariedad 19/20 · Historial 10/20 · Transparencia 11/15 · Autoridad 14/15 · Independencia 7/10 · Actualidad 8/10 · Acceso 3/10
- **Tipología:** primaria (registro de operaciones)
- **Acceso:** Servicio comercial (portal web, API o SFTP; precio bajo consulta); no se confirmó la continuidad de los antiguos agregados públicos gratuitos
- **Ámbitos:** CDS sobre índices, single-name y tramos registrados en el TIW
- **Motivo de inclusión y uso:** Posicionamiento agregado (nocional neto) en CDS por nombre, sector e índice, base para medir dónde se concentra la demanda de protección. AG-23, AG-25.
- **Restricciones de uso:** Según licencia del servicio.
- **Sesgos y cautelas:** Datos de pago; el nocional bruto sobrestima el riesgo; la página no indica condiciones de acceso. Para datos gratuitos de swaps, usar RF-0541 (CFTC) y RF-0545 (ISDA SwapsInfo).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Los datos públicos de la antigua sección «repository-otc-data» se reorganizaron en DTCC Data Services (URL antiguas sustituidas en esta revisión).
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «DTCC Trade Information Warehouse CDS public data weekly stocks volumes»; WebFetch: sí, página de CDS Kinetics y artículo de DTCC de 18/08/2021)
- **Origen:** Alta F9_S4 (2026-11-02); reescrita F9_S6 (2026-11-02): URL reparada y acceso revisado.

#### RF-0561 · Q 72 (B) — ICE Data Indices — ICE BofA MOVE Index (volatilidad implícita de los bonos del Tesoro de EE. UU.)

- **Canal oficial (URL raíz):** https://developer.ice.com/fixed-income-data-services/catalog/ice-data-indices-move-index (adquisición del índice por ICE: https://ir.theice.com/press/news-details/2019/Intercontinental-Exchange-Completes-Acquisition-of-the-Merrill-Lynch-Option-Volatility-Estimate-MOVE-Index-from-Bank-of-America-Merrill-Lynch/default.aspx)
- **Emisor:** ICE Data Indices, LLC (Intercontinental Exchange); ficha matriz del emisor: RF-0506
- **Documentación y notas:** ICE BofA U.S. Bond Market Option Volatility Estimate Index (MOVE), presentado por ICE como el indicador de referencia de la volatilidad de la renta fija: volatilidad implícita de una cesta de opciones OTC sobre swaps de tipos de interés de EE. UU. (con variantes sobre cestas de opciones a 3 y 6 meses); historia desde 1996, datos intradía y de cierre; precio casi intradía. ICE adquirió el índice a Bank of America Merrill Lynch en 2019.
- **Temática:** TF-17 Derivados y volatilidad: mercados y datos (principal) · secundarias: TF-19, TF-15
- **Calidad Q:** 72 (B) — Primariedad 18/20 · Historial 10/20 · Transparencia 10/15 · Autoridad 13/15 · Independencia 7/10 · Actualidad 10/10 · Acceso 4/10
- **Tipología:** primaria (índice calculado por el administrador)
- **Acceso:** Datos bajo licencia de ICE (ICE Connect, API, ficheros); el valor diario se difunde por terminales y medios
- **Ámbitos:** Volatilidad implícita de tipos de EE. UU.
- **Motivo de inclusión y uso:** Termómetro estándar de la volatilidad de tipos («VIX de los bonos») para el régimen de volatilidad de la renta fija y la relación MOVE/VIX. AG-25, AG-23.
- **Restricciones de uso:** Licencia de ICE; citar valor y fecha.
- **Sesgos y cautelas:** La página del catálogo no detalla pesos por plazo ni la metodología completa (documento metodológico no localizado en esta sesión); los valores que publican webs de terceros pueden ir con retraso o error.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Antes «Merrill Lynch Option Volatility Estimate», propiedad de BofA Merrill Lynch hasta 2019.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «ICE BofA MOVE Index methodology Treasury implied volatility ICE Data Indices»; WebFetch: sí, catálogo de ICE Data Services)
- **Origen:** Alta F9_S6 (2026-11-02), sustituta adicional (refuerzo de la cobertura de volatilidad de tipos).

#### RF-0553 · Q 71 (B) — WFE (World Federation of Exchanges) — estadísticas de derivados cotizados (Statistics Portal e informes semestrales)

- **Canal oficial (URL raíz):** https://statistics.world-exchanges.org (sección de estadísticas: https://www.world-exchanges.org/our-work/statistics · informe del 1S 2025, 14/08/2025: https://www.world-exchanges.org/news/articles/new-wfe-hy25-market-data-ipos-down-first-half · documento completo: https://www.world-exchanges.org/our-work/articles/h1-2025-market-highlights · reseña de FOW de los datos anuales de 2025, 27/02/2026: https://www.fow.com/insights/derivatives-trading-volume-decrease-in-2025-wfe-data)
- **Emisor:** World Federation of Exchanges
- **Documentación y notas:** Portal estadístico con volúmenes de contratos de derivados cotizados de las bolsas miembro por región, clase de activo y producto, e informes semestrales y anuales. 1S 2025: 43,92 miles de millones de contratos (−47,8 % interanual, por la regulación de opciones en la India); futuros 14,18 miles de millones (+7,8 %); Américas +11,7 % y EMEA +21,9 % interanual, Asia-Pacífico −64,8 %. Año 2025 (según FOW): 93,75 miles de millones de contratos (−47,1 %). Publica además investigación de estructura de mercado.
- **Temática:** TF-17 Derivados y volatilidad: mercados y datos (principal) · secundarias: TF-06
- **Calidad Q:** 71 (B) — Primariedad 16/20 · Historial 10/20 · Transparencia 11/15 · Autoridad 14/15 · Independencia 6/10 · Actualidad 8/10 · Acceso 6/10
- **Tipología:** secundaria (agregación de datos de bolsas miembro)
- **Acceso:** Notas e informes resumidos abiertos; detalle del portal con registro o suscripción
- **Ámbitos:** Derivados cotizados mundiales; contraste con FIA (RF-0542), que da cifras distintas por cobertura
- **Motivo de inclusión y uso:** Segunda fuente agregada del volumen mundial de derivados cotizados y de su reparto regional. AG-23.
- **Restricciones de uso:** Uso con atribución.
- **Sesgos y cautelas:** Patronal de bolsas; cobertura limitada a miembros; el recuento por contratos mezcla tamaños muy distintos. El portal estadístico se tomó del enlace de una página oficial leída, sin cargarlo.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sustitución del antiguo informe anual IOMA de derivados por el portal estadístico y los informes de mercado semestrales (URL de pruebas antigua sustituida en esta revisión).
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «World Federation of Exchanges 2025 derivatives report statistics world-exchanges.org»; WebFetch: sí, nota del 1S 2025 y página de etiqueta «derivatives»)
- **Origen:** Alta F9_S4 (2026-11-02); reescrita F9_S6 (2026-11-02): URL reparada.

#### RF-0558 · Q 67 (B) — Creditex (ICE) — Credit Event Auctions (resultados de subastas de eventos de crédito)

- **Canal oficial (URL raíz):** https://www.ice.com/service/creditex/credit-auctions (página del servicio Creditex: https://www.theice.com/SERVICE/CREDITEX)
- **Emisor:** Creditex (Intercontinental Exchange), coadministrador de las subastas con Markit (S&P Global)
- **Documentación y notas:** Explica el protocolo de subastas que liquida los CDS tras un evento de crédito (quiebra, reestructuración) y enlaza, por año, los resultados de más de 160 subastas desde 2005 de créditos corporativos y soberanos de Norteamérica, Europa y Japón (p. ej., Anglo Irish Bank 2011, Venezuela y PDVSA 2017, Novo Banco 2018); el precio final se publica en creditfixings.com o en el sitio de los comités de determinación de ISDA (RF-0555).
- **Temática:** TF-17 Derivados y volatilidad: mercados y datos (principal) · secundarias: TF-19
- **Calidad Q:** 67 (B) — Primariedad 18/20 · Historial 10/20 · Transparencia 11/15 · Autoridad 12/15 · Independencia 6/10 · Actualidad 3/10 · Acceso 7/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** Tasas de recuperación implícitas de impagos corporativos y soberanos
- **Motivo de inclusión y uso:** Archivo histórico de precios finales de subasta para calibrar recuperaciones y diferenciales de crédito tras impagos. AG-25, AG-23.
- **Restricciones de uso:** Uso con atribución.
- **Sesgos y cautelas:** La lista de la página termina en 2018: para subastas posteriores, consultar RF-0555. Administrador con interés comercial en la infraestructura de CDS.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Creditex integrada en ICE; Markit en S&P Global (URL antigua de creditfixings.com sustituida como canal raíz en esta revisión).
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «creditfixings credit event auction historical results ISDA auction»; WebFetch: sí)
- **Origen:** Alta F9_S4 (2026-11-02); reescrita F9_S6 (2026-11-02): URL reparada, Q revisada a la baja por actualidad.

## TF-18 Mercado monetario y tipos a corto plazo

#### RF-0600 · Q 90 (A) — BCE — €STR (euro short-term rate) y €STR compuesto

- **Canal oficial (URL raíz):** https://www.ecb.europa.eu/stats/financial_markets_and_interest_rates/euro_short-term_rate/html/eurostr_overview.en.html (series: https://data.ecb.europa.eu/data/data-categories/financial-markets-and-interest-rates/euro-money-market/euro-short-term-rate-data)
- **Emisor:** Banco Central Europeo (administrador del índice), con datos recogidos por Bundesbank, Banco de España, Banque de France y Banca d'Italia
- **Temática:** TF-18 Mercado monetario y tipos a corto plazo (principal) · secundarias: TF-01
- **Calidad Q:** 90 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 15/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 10/10 · Acceso 10/10
- **Tipología:** primaria (índice de referencia oficial calculado sobre transacciones)
- **Acceso:** Abierto y gratuito (sin licencia de uso)
- **Ámbitos:** Tipo de interés a un día no garantizado de los bancos de la eurozona; publicación a las 08:00 CET de cada día TARGET2; tipos compuestos a 1 semana y 1, 3, 6 y 12 meses e índice compuesto (09:15 CET); pre-€STR hasta 30/09/2019; revisión metodológica anual (última vista: 09/12/2025)
- **Motivo de inclusión y uso:** Tipo libre de riesgo de referencia del euro y ancla de la curva OIS en euros. AG-24 (Monetarios y liquidez): nivel y diferencial del €STR frente a la facilidad de depósito; AG-25: tramo corto de la curva.
- **Sesgos y cautelas:** Solo mide préstamos no garantizados captados por bancos (incluye depósitos de entidades no bancarias, por eso cotiza por debajo de la facilidad de depósito); procedimiento de contingencia si informan menos de 20 bancos.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «ECB euro short-term rate €STR money market statistical reporting»; WebFetch: sí)
- **Origen:** Alta F9_S5 (2026-11-02).

#### RF-0602 · Q 90 (A) — Federal Reserve Bank of New York — Reference Rates (SOFR, EFFR, OBFR, TGCR, BGCR)

- **Canal oficial (URL raíz):** https://www.newyorkfed.org/markets/reference-rates (SOFR: https://www.newyorkfed.org/markets/reference-rates/sofr · medias e índice: https://www.newyorkfed.org/markets/reference-rates/sofr-averages-and-index)
- **Emisor:** Federal Reserve Bank of New York (administrador; en cooperación con la OFR para los tipos repo)
- **Temática:** TF-18 Mercado monetario y tipos a corto plazo (principal) · secundarias: TF-01
- **Calidad Q:** 90 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 15/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 10/10 · Acceso 10/10
- **Tipología:** primaria (índices de referencia oficiales sobre transacciones; declaración de cumplimiento IOSCO)
- **Acceso:** Abierto (API de datos de mercados)
- **Ámbitos:** EFFR y OBFR (mediana ponderada por volumen de fondos federales y eurodólares; ~9:00 ET); TGCR, BGCR y SOFR (repo a un día con colateral del Tesoro; SOFR excluye el 20 % de menor tipo del DVP); medias SOFR a 30, 90 y 180 días e índice SOFR (8:00 ET)
- **Motivo de inclusión y uso:** Fuente primaria de los tipos a un día del dólar. AG-24: posición del EFFR dentro de la banda objetivo, diferencial SOFR–IORB como señal de escasez de reservas; AG-25: tramo corto de la curva en dólares.
- **Sesgos y cautelas:** Revisiones del mismo día (~14:30 ET) posibles; el SOFR se publica con un día de retraso respecto a la fecha valor. RF-0343 (OFR) redistribuye estas series: citar aquí la fuente primaria.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «New York Fed reference rates SOFR EFFR OBFR TGCR BGCR»; WebFetch: sí, página «additional information about reference rates»)
- **Origen:** Alta F9_S5 (2026-11-02).

#### RF-0605 · Q 89 (A) — Bank of England — SONIA (Sterling Overnight Index Average) y SONIA Compounded Index

- **Canal oficial (URL raíz):** https://www.bankofengland.co.uk/markets/sonia-benchmark
- **Emisor:** Bank of England (administrador del índice desde 2016)
- **Temática:** TF-18 Mercado monetario y tipos a corto plazo (principal) · secundarias: TF-01
- **Calidad Q:** 89 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 15/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 10/10 · Acceso 9/10
- **Tipología:** primaria (índice de referencia oficial sobre transacciones)
- **Acceso:** Abierto (serie IUDSOIA en la base de datos estadística interactiva del BoE)
- **Ámbitos:** Tipo medio a un día no garantizado en libras; publicación cada día hábil de Londres; índice compuesto desde 03/08/2020; documento de características y políticas; actas del grupo asesor
- **Motivo de inclusión y uso:** Tipo libre de riesgo de la libra y ancla de la curva OIS en libras. AG-24: diferencial SONIA–Bank Rate; AG-25: tramo corto de la curva británica.
- **Sesgos y cautelas:** Refleja préstamos a bancos (incluye depósitos de no bancarias); la ficha general del BoE es RF-0019.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Bank of England SONIA interest rate benchmark»; WebFetch: sí)
- **Origen:** Alta F9_S5 (2026-11-02).

#### RF-0601 · Q 87 (A) — BCE — Estadísticas del mercado monetario del euro (MMSR)

- **Canal oficial (URL raíz):** https://data.ecb.europa.eu/methodology/euro-money-market
- **Emisor:** Banco Central Europeo (Money Market Statistical Reporting, Reglamento MMSR)
- **Temática:** TF-18 Mercado monetario y tipos a corto plazo (principal) · secundarias: TF-01
- **Calidad Q:** 87 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 8/10 · Acceso 10/10
- **Tipología:** primaria (estadística oficial agregada de transacciones declaradas)
- **Acceso:** Abierto (descargas SDMX 2.1 CSV de los conjuntos EST, MMSR y MMS en el BCE Data Portal)
- **Ámbitos:** Volúmenes y tipos de los segmentos no garantizado, garantizado (repo) y OIS por periodo de mantenimiento de reservas (series desde 2017 y 2018); OIS a plazo trimestral; publicación 15 días TARGET tras cada periodo; serie histórica de la antigua Euro Money Market Survey (2001–2015)
- **Motivo de inclusión y uso:** Única fuente oficial de la actividad del mercado monetario del euro por segmento. AG-24: tensión en el repo (tipos repo frente a €STR), fragmentación y desplazamiento entre segmentos.
- **Sesgos y cautelas:** Muestra de bancos informadores (no el universo); el segmento de swaps de divisas no se publica; desfase de unas tres semanas. Es un conjunto específico dentro del BCE Data Portal (RF-0004).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «ECB euro short-term rate €STR money market statistical reporting»; WebFetch: sí)
- **Origen:** Alta F9_S5 (2026-11-02).

#### RF-0603 · Q 87 (A) — Federal Reserve Bank of New York — Desk Operations (repo, reverse repo ON RRP, SOMA)

- **Canal oficial (URL raíz):** https://www.newyorkfed.org/markets/desk-operations/reverse-repo (repo: https://www.newyorkfed.org/markets/desk-operations/repo · cartera SOMA: https://www.newyorkfed.org/markets/soma-holdings)
- **Emisor:** Federal Reserve Bank of New York, Open Market Trading Desk
- **Temática:** TF-18 Mercado monetario y tipos a corto plazo (principal) · secundarias: TF-01, TF-19
- **Calidad Q:** 87 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 10/10 · Acceso 9/10
- **Tipología:** primaria (resultados de operaciones de mercado abierto)
- **Acceso:** Abierto (resultados diarios, datos históricos de transacciones y API)
- **Ámbitos:** Resultados de las operaciones repo (incluida la Standing Repo Facility) y reverse repo (ON RRP: volumen y contrapartes), compras/ventas de Tesoro y MBS de agencia, préstamo de valores, swaps de liquidez con bancos centrales y tenencias SOMA
- **Motivo de inclusión y uso:** Termómetro diario de la liquidez en dólares: el saldo ON RRP como colchón de liquidez excedente y el uso de la SRF como señal de tensión. AG-24 y AG-25 (ritmo de reducción del balance).
- **Sesgos y cautelas:** Los resultados reflejan decisiones de política (no precios de mercado libres); la página de reverse repo no detalla calendario, hay que acudir a las declaraciones operativas.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «New York Fed reference rates SOFR EFFR OBFR TGCR BGCR» → enlaces de la página de tipos de referencia; WebFetch: sí)
- **Origen:** Alta F9_S5 (2026-11-02).

#### RF-0619 · Q 87 (A) — Tesoro Público (España) — Subastas y resultados de Letras del Tesoro

- **Canal oficial (URL raíz):** https://www.tesoro.es/en/deuda-publica/subastas/resultado-ultimas-subastas/letras-del-tesoro (subastas anteriores: https://www.tesoro.es/en/deuda-publica/subastas/resultados-subastas-anteriores · calendario 2026: https://www.tesoro.es/documents/d/tesoro/calendario-tesoro-publico-2026-espanol-12-pdf · minoristas: https://elijo.tesoro.es/subastas)
- **Emisor:** Secretaría General del Tesoro y Financiación Internacional (Ministerio de Economía, Comercio y Empresa); Banco de España como agente
- **Temática:** TF-18 Mercado monetario y tipos a corto plazo (principal) · secundarias: TF-19, TF-01
- **Calidad Q:** 87 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 9/10 · Actualidad 10/10 · Acceso 9/10
- **Tipología:** primaria (resultados oficiales del emisor)
- **Acceso:** Abierto (resultados, calendario y estadísticas mensuales e históricas)
- **Ámbitos:** Subastas de Letras a 3, 6, 9 y 12 meses: importes solicitados y adjudicados, tipo marginal y medio, ratio de cobertura, peticiones no competitivas; estadísticas de tipos marginales, coste medio, tipos efectivos de nuevas emisiones y tenedores. Ejemplo visto: subasta a 12 meses de 06/10/2026, tipo marginal 3,026 %, cobertura 1,36
- **Motivo de inclusión y uso:** Rentabilidad del activo sin riesgo a corto plazo en España, de gran peso en el ahorro minorista; comparación con depósitos (RF-0609), €STR (RF-0600) y fondos monetarios. AG-24.
- **Sesgos y cautelas:** Precios de subasta (primario), no de mercado secundario; los tipos de las letras incorporan una pequeña prima soberana frente al €STR.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Tesoro Público Letras del Tesoro subastas calendario», limitada a tesoro.es; WebFetch: sí)
- **Origen:** Alta F9_S5 (2026-11-02).

#### RF-0609 · Q 86 (A) — BCE — Estadísticas de tipos de interés de las IFM (MIR): depósitos y préstamos bancarios

- **Canal oficial (URL raíz):** https://www.ecb.europa.eu/press/stats/mfi/html/ecb.mir2605~8bd04df5cc.es.html (nota mensual; versión española traducida por el Banco de España: https://www.bde.es/f/webbe/GAP/Secciones/SalaPrensa/ComunicadosBCE/NotasInformativasBCE/26/presbce2026-126.pdf)
- **Emisor:** Banco Central Europeo (con los bancos centrales nacionales del Eurosistema, incluido el Banco de España)
- **Temática:** TF-18 Mercado monetario y tipos a corto plazo (principal) · secundarias: TF-01, TF-19
- **Calidad Q:** 86 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 7/10 · Acceso 10/10
- **Tipología:** primaria (estadística oficial)
- **Acceso:** Abierto (nota de prensa mensual; datos por país, incluida España, en el BCE Data Portal)
- **Ámbitos:** Tipos de nuevas operaciones de depósitos a la vista, a plazo hasta un año y con preaviso de hogares y sociedades no financieras; coste sintético de financiación de préstamos a empresas y vivienda; volúmenes. Ejemplo visto: marzo de 2026, depósitos a plazo de hogares 1,86 %, a la vista 0,26 %
- **Motivo de inclusión y uso:** Remuneración efectiva del ahorro bancario frente al €STR y las letras: mide el traslado de los tipos oficiales a depositantes (y el atractivo relativo de monetarios y letras). AG-24.
- **Sesgos y cautelas:** Medias ponderadas por volumen (efecto composición); desfase de unas cinco semanas; revisiones de periodos anteriores.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Banco de España tipos de interés estadísticas depósitos nuevas operaciones hogares sociedades»; WebFetch: sí, nota de mayo de 2026 y PDF de septiembre de 2026)
- **Origen:** Alta F9_S5 (2026-11-02).

#### RF-0612 · Q 86 (A) — Federal Reserve Board — H.4.1 Factors Affecting Reserve Balances (balance de la Fed)

- **Canal oficial (URL raíz):** https://www.federalreserve.gov/releases/h41/
- **Emisor:** Board of Governors of the Federal Reserve System
- **Temática:** TF-18 Mercado monetario y tipos a corto plazo (principal) · secundarias: TF-01
- **Calidad Q:** 86 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 9/10 · Acceso 8/10
- **Tipología:** primaria (estado contable semanal oficial)
- **Acceso:** Abierto (cada jueves, hacia las 16:30 ET)
- **Ámbitos:** Factores que aportan y absorben reservas: valores en cartera, préstamos y facilidades, reverse repos (incluido el ON RRP), cuenta general del Tesoro (TGA), billetes; saldo de reservas bancarias. Última actualización vista: 29/10/2026
- **Motivo de inclusión y uso:** Medida semanal de la liquidez del sistema en dólares (reservas = activos − TGA − ON RRP − billetes); clave para anticipar tensiones de fin de mes/trimestre y el fin de la reducción del balance. AG-24.
- **Sesgos y cautelas:** Datos de miércoles y medias semanales: la volatilidad intrasemanal (TGA, fechas fiscales) no se ve; la página índice no describe las tablas (consultar la publicación).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «federalreserve.gov releases H.15 selected interest rates commercial paper rates» → enlace desde la página H.15; WebFetch: sí)
- **Origen:** Alta F9_S5 (2026-11-02).

#### RF-0608 · Q 85 (A) — U.S. Treasury / TreasuryDirect — Auctions: Announcements, Data & Results

- **Canal oficial (URL raíz):** https://www.treasurydirect.gov/auctions (anuncios y resultados: https://www.treasurydirect.gov/auctions/announcements-data-results/announcement-results-press-releases)
- **Emisor:** U.S. Department of the Treasury, Bureau of the Fiscal Service
- **Temática:** TF-18 Mercado monetario y tipos a corto plazo (principal) · secundarias: TF-19
- **Calidad Q:** 85 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 10/10 · Acceso 6/10
- **Tipología:** primaria (anuncios y resultados oficiales de subastas)
- **Acceso:** Abierto (la web bloquea robots; consulta manual o vía las API del Fiscal Service)
- **Ámbitos:** Calendario de subastas, anuncios y resultados de letras (bills), notas, bonos, TIPS y FRN: importes, tipo de corte, ratio de cobertura (bid-to-cover), adjudicación por tipo de postor
- **Motivo de inclusión y uso:** Oferta de letras del Tesoro (drenaje de liquidez, competencia con fondos monetarios y con el ON RRP) y demanda en las subastas. AG-24 (oferta de bills) y AG-25 (colas de subasta en plazos largos).
- **Sesgos y cautelas:** Página principal no legible por herramientas automáticas (robots); para series largas preferir el conjunto de datos de subastas del Fiscal Service.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «TreasuryDirect auctions announcements results bills»; WebFetch: intentado, bloqueado por robots)
- **Origen:** Alta F9_S5 (2026-11-02).

#### RF-0610 · Q 85 (A) — SEC — Money Market Fund Statistics (datos del Form N-MFP)

- **Canal oficial (URL raíz):** https://www.sec.gov/divisions/investment/mmf-statistics.shtml (informe de ejemplo: https://SEC.GOV/files/mmf-statistics-2019-05.pdf)
- **Emisor:** U.S. Securities and Exchange Commission, División de Gestión de Inversiones (Analytics Office)
- **Temática:** TF-18 Mercado monetario y tipos a corto plazo (principal) · secundarias: TF-16
- **Calidad Q:** 85 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 8/10 · Acceso 9/10
- **Tipología:** primaria (estadística oficial agregada de declaraciones regulatorias)
- **Acceso:** Abierto (PDF mensual y series descargables desde 2010, ampliadas en abril de 2025)
- **Ámbitos:** Número y patrimonio de fondos monetarios por categoría (prime, exentos, gobierno/Tesoro; institucional y minorista), rentabilidad a 7 días, WAM, WAL, activos líquidos diarios y semanales, exposición bancaria por país, contrapartes repo (incluida la Fed). Dato visto: febrero de 2026, patrimonio récord de 8,341 billones USD
- **Motivo de inclusión y uso:** Fuente oficial y censal de los fondos monetarios de EE. UU.; contraste de RF-0347 (Crane) y RF-0053 (ICI). AG-24: flujos hacia fondos de gobierno, duración de cartera y uso del ON RRP.
- **Sesgos y cautelas:** Desfase de unas cuatro semanas; el personal puede corregir errores de los declarantes.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «SEC money market fund statistics Form N-MFP monthly report Division of Investment Management»; WebFetch: sí, PDF de la SEC y artículo de Crane Data de 26/03/2026 que enlaza la página de estadísticas)
- **Origen:** Alta F9_S5 (2026-11-02).

#### RF-0611 · Q 85 (A) — Federal Reserve Board — Commercial Paper Rates and Outstanding (CP)

- **Canal oficial (URL raíz):** https://www.federalreserve.gov/releases/cp/
- **Emisor:** Board of Governors of the Federal Reserve System (datos de The Depository Trust & Clearing Corporation, DTCC)
- **Temática:** TF-18 Mercado monetario y tipos a corto plazo (principal) · secundarias: TF-19
- **Calidad Q:** 85 (A) — Primariedad 19/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 10/10 · Acceso 8/10
- **Tipología:** primaria (estadística oficial a partir de liquidaciones de DTCC)
- **Acceso:** Abierto (publicación diaria hacia las 13:00 ET; el «Build Your Package» del DDP se retira en noviembre de 2026: series también en FRED, RF-0001)
- **Ámbitos:** Tipos diarios del papel comercial AA no financiero, AA financiero, AA respaldado por activos (ABCP) y A2/P2 no financiero de 1 a 90 días; saldo vivo semanal y mensual por tipo de emisor. Dato visto: 28/10/2026, saldo total desestacionalizado 1.499,0 mm USD
- **Motivo de inclusión y uso:** Prima de crédito a corto plazo (diferencial A2/P2–AA y CP–letras) como señal temprana de tensión en la financiación de empresas y bancos. AG-24 y AG-25.
- **Sesgos y cautelas:** Plazos largos con frecuentes «n.a.» por escaso volumen; el Board no garantiza la hora de publicación.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «federalreserve.gov releases H.15 selected interest rates commercial paper rates» → enlace desde la página H.15; WebFetch: sí)
- **Origen:** Alta F9_S5 (2026-11-02).

#### RF-0606 · Q 84 (A) — Bank of England — Market operations: resultados y uso de facilidades (Sterling Monetary Framework)

- **Canal oficial (URL raíz):** https://www.bankofengland.co.uk/markets/bank-of-england-market-operations-guide (resultados: https://www.bankofengland.co.uk/markets/bank-of-england-market-operations-guide/results-and-usage-data)
- **Emisor:** Bank of England
- **Temática:** TF-18 Mercado monetario y tipos a corto plazo (principal) · secundarias: TF-01
- **Calidad Q:** 84 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 8/10 · Acceso 7/10
- **Tipología:** primaria (resultados de operaciones del banco central)
- **Acceso:** Abierto
- **Ámbitos:** Resultados y uso de las operaciones repo a corto plazo, ILTR (Indexed Long-Term Repo), facilidad permanente operativa y ventanilla de descuento; notas de mercado sobre precios; informe anual de operaciones de mercado
- **Motivo de inclusión y uso:** Demanda de reservas y tensión de liquidez en libras en la transición a un sistema de reservas «a demanda». AG-24.
- **Sesgos y cautelas:** Información técnica dispersa en notas de mercado; los datos de uso de algunas facilidades se publican con desfase.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Bank of England SONIA interest rate benchmark» → enlace de la página SONIA; WebFetch: sí)
- **Origen:** Alta F9_S5 (2026-11-02).

#### RF-0613 · Q 84 (A) — Federal Reserve Bank of New York — Central Bank Liquidity Swap Operations (líneas swap en dólares)

- **Canal oficial (URL raíz):** https://www.newyorkfed.org/markets/desk-operations/central-bank-liquidity-swap-operations
- **Emisor:** Federal Reserve Bank of New York, Open Market Trading Desk
- **Temática:** TF-18 Mercado monetario y tipos a corto plazo (principal) · secundarias: TF-01
- **Calidad Q:** 84 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 8/10 · Acceso 8/10
- **Tipología:** primaria (resultados de operaciones oficiales)
- **Acceso:** Abierto (resultados semanales cuando hay operaciones; API de datos de mercados)
- **Ámbitos:** Uso de las líneas swap de liquidez en dólares por bancos centrales extranjeros (enlaces a resultados del BoE, BoJ, BCE y BNS), incluidas operaciones de prueba de pequeño importe
- **Motivo de inclusión y uso:** Indicador de escasez de dólares fuera de EE. UU.: la demanda en las subastas de dólares de otros bancos centrales sube en episodios de tensión (2008, 2020). AG-24.
- **Sesgos y cautelas:** La página no muestra saldos: hay que ir a los resultados de cada banco central o a la API; las operaciones de prueba no reflejan demanda real.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «New York Fed reference rates SOFR EFFR OBFR TGCR BGCR» → enlace desde la página de tipos de referencia; WebFetch: sí)
- **Origen:** Alta F9_S5 (2026-11-02).

#### RF-0604 · Q 83 (A) — Federal Reserve Bank of New York — Survey of Market Expectations (SME)

- **Canal oficial (URL raíz):** https://www.newyorkfed.org/markets/market-intelligence/survey-of-market-expectations
- **Emisor:** Federal Reserve Bank of New York, Open Market Trading Desk
- **Temática:** TF-18 Mercado monetario y tipos a corto plazo (principal) · secundarias: TF-19
- **Calidad Q:** 83 (A) — Primariedad 17/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 9/10 · Actualidad 8/10 · Acceso 10/10
- **Tipología:** primaria (encuesta oficial; las respuestas son opiniones de participantes)
- **Acceso:** Abierto (cuestionarios, resultados y datos en Excel)
- **Ámbitos:** Expectativas sobre la senda del tipo de los fondos federales, el tamaño del balance de la Fed y la economía; antes de cada reunión del FOMC; fusiona desde 2025 la Survey of Primary Dealers (2002–2024) y la Survey of Market Participants (2014–2024)
- **Motivo de inclusión y uso:** Contraste de la senda implícita en futuros (RF-0346) con las expectativas declaradas (distribuciones de probabilidad). AG-24 y AG-25: prima de plazo implícita en el tramo corto.
- **Sesgos y cautelas:** Opinión agregada, no hechos; resultados publicados unas tres semanas después de la reunión (tras las actas). Una fuente de opinión no prueba hechos (regla F9-a).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «New York Fed reference rates SOFR EFFR OBFR TGCR BGCR» → enlace de la página de tipos de referencia; WebFetch: sí)
- **Origen:** Alta F9_S5 (2026-11-02).

#### RF-0607 · Q 82 (A) — EMMI — Euribor® (European Money Markets Institute)

- **Canal oficial (URL raíz):** https://www.emmi-benchmarks.eu/benchmarks/euribor/rate/ (metodología híbrida y reformas: https://emmi-benchmarks.eu/benchmarks/euribor/reforms)
- **Emisor:** European Money Markets Institute (EMMI), administrador autorizado bajo el Reglamento de Índices de Referencia (BMR); supervisado por ESMA desde 01/01/2022
- **Temática:** TF-18 Mercado monetario y tipos a corto plazo (principal) · secundarias: TF-19
- **Calidad Q:** 82 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 14/15 · Independencia 8/10 · Actualidad 10/10 · Acceso 6/10
- **Tipología:** primaria (índice de referencia regulado, metodología híbrida en cascada sobre transacciones de los bancos del panel)
- **Acceso:** Datos diferidos visibles en la web; tiempo real y redistribución con licencia
- **Ámbitos:** Euribor a 1 semana y 1, 3, 6 y 12 meses (tipo de financiación mayorista no garantizada de los bancos del panel); revisión anual de la metodología; mejoras de 2024 (supresión del nivel 3 de juicio experto, migración completada en octubre de 2024)
- **Motivo de inclusión y uso:** Tipo de referencia de hipotecas variables y préstamos en la eurozona (y en España). AG-24: diferencial Euribor–€STR como prima de crédito/plazo bancaria; transmisión a familias y empresas.
- **Sesgos y cautelas:** Asociación del sector bancario; uso comercial y redistribución sujetos a licencia (citar fecha y plazo). En la UE convive con €STR (RF-0600) como tipo libre de riesgo.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «EMMI Euribor rates hybrid methodology European Money Markets Institute»; WebFetch: sí, página de reformas)
- **Origen:** Alta F9_S5 (2026-11-02).

#### RF-0618 · Q 82 (A) — Bank of Japan — TONA (Tokyo Overnight Average Rate) y estadísticas del mercado monetario

- **Canal oficial (URL raíz):** https://www3.boj.or.jp/market/en/menu_m.htm (TONA diario) · https://www.stat-search.boj.or.jp/ssi/mtshtml/fm02_m_1_en.html (TONA mensual, estadísticas principales del BoJ)
- **Emisor:** Bank of Japan
- **Temática:** TF-18 Mercado monetario y tipos a corto plazo (principal) · secundarias: TF-01
- **Calidad Q:** 82 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 9/10 · Acceso 6/10
- **Tipología:** primaria (tipo oficial de referencia sobre transacciones)
- **Acceso:** Abierto (páginas en inglés con navegación poco amigable)
- **Ámbitos:** Tipo a un día no garantizado del mercado interbancario de call en yenes («mutan rate»), tipo libre de riesgo recomendado del yen desde el 28/12/2016 y objetivo operativo de la política monetaria tras el cambio de marco de marzo de 2024; medias y el índice TONA los publica QUICK Corp.
- **Motivo de inclusión y uso:** Seguimiento de la normalización monetaria japonesa (subidas de tipos) y del carry trade en yenes. AG-24; AG-25 (tramo corto de la curva JGB). La ficha general del BoJ es RF-0020.
- **Sesgos y cautelas:** Las URL oficiales se tomaron de la ficha de Wikipedia (lectura lateral) y no se cargaron; los promedios compuestos no los publica el BoJ.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Bank of Japan TONA uncollateralized overnight call rate data» → Wikipedia «TONAR»; WebFetch: sí, sobre Wikipedia)
- **Origen:** Alta F9_S5 (2026-11-02).

#### RF-0614 · Q 80 (A) — Federal Reserve Board — Senior Credit Officer Opinion Survey on Dealer Financing Terms (SCOOS)

- **Canal oficial (URL raíz):** https://www.federalreserve.gov/data/scoos.htm
- **Emisor:** Board of Governors of the Federal Reserve System
- **Temática:** TF-18 Mercado monetario y tipos a corto plazo (principal) · secundarias: TF-19, TF-17
- **Calidad Q:** 80 (A) — Primariedad 16/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 7/10 · Acceso 9/10
- **Tipología:** primaria (encuesta oficial; respuestas cualitativas de los intermediarios)
- **Acceso:** Abierto (trimestral, desde marzo de 2010; última vista: septiembre de 2026)
- **Ámbitos:** Condiciones de crédito en la financiación de valores (repo y préstamo de valores) y derivados OTC ofrecidas por los intermediarios a hedge funds, gestoras y otros clientes; panel de grandes dealers que concentran casi toda la actividad en dólares
- **Motivo de inclusión y uso:** Medida del apalancamiento disponible vía financiación de valores (márgenes, plazos, demanda), complemento cualitativo de los datos de repo. AG-24 y AG-25.
- **Sesgos y cautelas:** Respuestas cualitativas (direccionales) de los propios intermediarios; trimestral.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «federalreserve.gov releases H.15 selected interest rates commercial paper rates» → enlace desde la página H.15; WebFetch: sí)
- **Origen:** Alta F9_S5 (2026-11-02).

#### RF-0620 · Q 80 (A) — SIX — SARON (Swiss Average Rate Overnight) y SARON compuesto

- **Canal oficial (URL raíz):** https://www.six-group.com/en/market-data/indices/switzerland/saron.html (reglamento: https://www.six-group.com/dam/download/market-data/indices/swiss-reference-rates/six-methodology-swiss-reference-rates-rules-en.pdf · datos: https://indexdata.six-group.com/swiss_reference_rates/reference_rates.html)
- **Emisor:** SIX Group (administrador del índice de referencia)
- **Temática:** TF-18 Mercado monetario y tipos a corto plazo (principal) · secundarias: TF-19
- **Calidad Q:** 80 (A) — Primariedad 19/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 14/15 · Independencia 8/10 · Actualidad 10/10 · Acceso 5/10
- **Tipología:** primaria (índice de referencia sobre operaciones y cotizaciones firmes del repo en francos)
- **Acceso:** Histórico descargable gratis; tipos compuestos públicos con un día de retraso; intradía y difusión pública inmediata con licencia de pago
- **Ámbitos:** Tipo medio ponderado por volumen del repo a un día en francos suizos (desde 30/06/1999), fijaciones a las 12, 16 y 18 h CET; tipos compuestos e índices a 1 semana y 1, 2, 3, 6, 9 y 12 meses
- **Motivo de inclusión y uso:** Tipo libre de riesgo del franco (referencia de hipotecas suizas) y de la política del Banco Nacional Suizo; tipos negativos y carry en francos. AG-24.
- **Sesgos y cautelas:** Operador privado de mercado con licencias costosas (citar con 24 h de retraso); mercado repo concentrado.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «SARON Swiss Average Rate Overnight SIX index data», limitada a six-group.com; WebFetch: sí)
- **Origen:** Alta F9_S5 (2026-11-02).

#### RF-0616 · Q 79 (B) — BCE — Survey of Monetary Analysts (SMA)

- **Canal oficial (URL raíz):** https://www.ecb.europa.eu/stats/ecb_surveys/sma/shared/pdf/ecb.smar260323_march.en.pdf (resultados agregados de marzo de 2026; serie en la sección de encuestas del BCE)
- **Emisor:** Banco Central Europeo
- **Temática:** TF-18 Mercado monetario y tipos a corto plazo (principal) · secundarias: TF-19
- **Calidad Q:** 79 (B) — Primariedad 15/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 9/10 · Actualidad 7/10 · Acceso 9/10
- **Tipología:** primaria (encuesta oficial; las respuestas son previsiones de analistas)
- **Acceso:** Abierto (resultados agregados antes/después de cada reunión de política monetaria)
- **Ámbitos:** Sendas esperadas de la facilidad de depósito, MRO, €STR y Euribor a 3 meses; probabilidades de cambios en las dos próximas reuniones; OIS y bonos a 10 años de Alemania, Francia, Italia y España; carteras APP/PEPP; probabilidad de activación del TPI; macro (PIB, paro, HICP). Marzo de 2026: 70 participantes
- **Motivo de inclusión y uso:** Expectativas de política monetaria del euro declaradas por analistas, para contrastar con la curva OIS sobre €STR (prima de plazo en el tramo corto). AG-24 y AG-25.
- **Sesgos y cautelas:** Opinión de analistas (regla F9-a), no hechos; panel de entidades financieras; preguntas con menos de seis respuestas no se publican.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «ECB Survey of Monetary Analysts SMA results and Survey of Professional Forecasters inflation expectations»; WebFetch: sí, PDF de marzo de 2026)
- **Origen:** Alta F9_S5 (2026-11-02).

#### RF-0615 · Q 76 (B) — BCE — Money Market Contact Group (MMCG): resúmenes y presentaciones

- **Canal oficial (URL raíz):** https://www.ecb.europa.eu/mopo/market-contact-groups/mmcg/html/index.en.html
- **Emisor:** Banco Central Europeo (preside el Director General Adjunto de Operaciones de Mercado; miembros de entidades activas en el mercado monetario del euro)
- **Temática:** TF-18 Mercado monetario y tipos a corto plazo (principal) · secundarias: TF-01
- **Calidad Q:** 76 (B) — Primariedad 14/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 14/15 · Independencia 8/10 · Actualidad 7/10 · Acceso 10/10
- **Tipología:** secundaria (resúmenes de debate entre banco central y participantes; opinión del sector)
- **Acceso:** Abierto
- **Ámbitos:** Unas tres reuniones al año (2026: 26/03, 24/06, 16/09) con orden del día, resumen y presentaciones sobre evolución del mercado monetario, perspectivas de política, demanda de reservas, liquidación T+1, finanzas tokenizadas y stablecoins; encuestas puntuales (expectativas de tipos, 2023) y material del Euro Money Market Study (EMMS 2022)
- **Motivo de inclusión y uso:** Lectura cualitativa del funcionamiento del mercado monetario del euro y de los temas que preocupan al BCE (exceso de liquidez decreciente, repo). AG-24.
- **Sesgos y cautelas:** Opiniones de participantes del mercado, no hechos (regla F9-a); resúmenes breves y con retraso.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «ECB euro short-term rate €STR money market statistical reporting» → enlace desde la página del €STR; WebFetch: sí)
- **Origen:** Alta F9_S5 (2026-11-02).

#### RF-0617 · Q 76 (B) — ICMA — European Repo Market Survey (encuesta semestral del mercado repo europeo)

- **Canal oficial (URL raíz):** https://www.icmagroup.org/market-practice-and-regulatory-policy/repo-and-collateral-markets/market-data/icma-european-repo-market-survey/ (archivo: https://www.icmagroup.org/market-practice-and-regulatory-policy/repo-and-collateral-markets/repo-market-surveys/)
- **Emisor:** International Capital Market Association (ICMA), European Repo and Collateral Council (ERCC)
- **Temática:** TF-18 Mercado monetario y tipos a corto plazo (principal) · secundarias: TF-07
- **Calidad Q:** 76 (B) — Primariedad 16/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 13/15 · Independencia 7/10 · Actualidad 8/10 · Acceso 10/10
- **Tipología:** primaria (encuesta sectorial de saldos vivos a una fecha)
- **Acceso:** Abierto (informe descargable y archivo histórico)
- **Ámbitos:** Tamaño y composición del mercado repo europeo (colateral, divisa, contrapartes, plazos) a una fecha de junio y de diciembre; edición 51 (junio de 2026, publicada el 13/10/2026): 14.915,9 mm EUR con 60 participantes; próxima referencia: 09/12/2026
- **Motivo de inclusión y uso:** Única fuente que dimensiona el repo europeo en conjunto (bilateral, tripartito y cámaras), complemento del MMSR (RF-0601). AG-24: financiación garantizada y demanda de colateral.
- **Sesgos y cautelas:** Asociación del sector; muestra voluntaria que varía entre ediciones (comparar con cautela); foto de un único día.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «ICMA European repo market survey semi-annual»; WebFetch: sí)
- **Origen:** Alta F9_S5 (2026-11-02).

## TF-19 Curvas de tipos, crédito e inflación implícita: datos

#### RF-0650 · Q 88 (A) — U.S. Treasury — Interest Rate Statistics (curva par diaria, letras y curva real)

- **Canal oficial (URL raíz):** https://home.treasury.gov/policy-issues/financing-the-government/interest-rate-statistics
- **Emisor:** U.S. Department of the Treasury (Office of Debt Management)
- **Temática:** TF-19 Curvas de tipos, crédito e inflación implícita: datos (principal) · secundarias: TF-18
- **Calidad Q:** 88 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 10/10 · Acceso 10/10
- **Tipología:** primaria (curva oficial del emisor)
- **Acceso:** Abierto (vista de texto, ficheros XML)
- **Ámbitos:** Curva par diaria nominal (cierres de los valores recién subastados), curva par real de TIPS (desde 2004), tipos de letras (bid de cierre), tipos a largo plazo y factores de extrapolación a 30 años, medias de tipos reales a largo plazo
- **Motivo de inclusión y uso:** Curva oficial del Tesoro de EE. UU. que alimenta las constantes de vencimiento del H.15 (RF-0651); pendiente 2s10s y 3m10a, y breakevens nominal–real. AG-25; AG-24 para el tramo de letras.
- **Sesgos y cautelas:** Curva par basada solo en emisiones recientes (on-the-run); para tipos cupón cero y a plazo usar RF-0652. Cambios anunciados en los ficheros XML.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «home.treasury.gov interest rate statistics daily treasury bill rates par yield curve real yield curve»; WebFetch: sí)
- **Origen:** Alta F9_S5 (2026-11-02).

#### RF-0656 · Q 88 (A) — BCE — Curvas de rendimiento de la zona del euro (Svensson; AAA y todos los soberanos)

- **Canal oficial (URL raíz):** https://www.ecb.europa.eu/stats/financial_markets_and_interest_rates/euro_area_yield_curves/html/index.en.html (metodología: https://data.ecb.europa.eu/methodology/yield-curves · serie de ejemplo: https://data.ecb.europa.eu/data/datasets/YC/YC.B.U2.EUR.4F.G_N_W.SV_C_YM.SR_6M)
- **Emisor:** Banco Central Europeo
- **Temática:** TF-19 Curvas de tipos, crédito e inflación implícita: datos (principal) · secundarias: TF-01
- **Calidad Q:** 88 (A) — Primariedad 18/20 · Historial 10/20 · Transparencia 15/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 10/10 · Acceso 10/10
- **Tipología:** primaria (estimación oficial del banco central con metodología publicada)
- **Acceso:** Abierto (publicación diaria a mediodía; conjunto YC del BCE Data Portal)
- **Ámbitos:** Curvas diarias desde el 06/09/2004 de deuda soberana de la eurozona (muestra AAA y muestra de todos los emisores centrales): cupón cero, forwards instantáneos y rendimientos par de 3 meses a 30 años, y parámetros Svensson
- **Motivo de inclusión y uso:** Curva libre de riesgo soberano del euro (AAA) y diferencial con la curva de todos los emisores como medida agregada de prima de riesgo soberano. AG-25: pendiente, forwards y valor relativo frente a OIS (€STR).
- **Sesgos y cautelas:** Excluye bonos ligados a la inflación y de cupón variable; composición AAA cambia con las calificaciones (rupturas). Conjunto específico dentro del BCE Data Portal (RF-0004).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «ECB euro area yield curves Svensson AAA all government bonds spot forward rates»; WebFetch: sí, página de metodología)
- **Origen:** Alta F9_S5 (2026-11-02).

#### RF-0651 · Q 87 (A) — Federal Reserve Board — H.15 Selected Interest Rates

- **Canal oficial (URL raíz):** https://www.federalreserve.gov/releases/h15/
- **Emisor:** Board of Governors of the Federal Reserve System
- **Temática:** TF-19 Curvas de tipos, crédito e inflación implícita: datos (principal) · secundarias: TF-18
- **Calidad Q:** 87 (A) — Primariedad 18/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 10/10 · Acceso 10/10
- **Tipología:** primaria (compilación oficial de tipos de mercado y administrados)
- **Acceso:** Abierto (diario, lunes a viernes, 16:15 ET; histórico en la propia publicación y en FRED)
- **Ámbitos:** Fondos federales efectivos, papel comercial, tipo preferencial (prime), ventanilla de descuento, letras del Tesoro, vencimientos constantes nominales (1 mes a 30 años) y ligados a la inflación (5 a 30 años). Última publicación vista: 30/10/2026
- **Motivo de inclusión y uso:** Serie histórica estándar de la curva del Tesoro y de los tipos a corto en EE. UU. (base de las series de FRED). AG-25: pendiente de la curva y tipos reales; AG-24: prime y fondos federales.
- **Sesgos y cautelas:** Series retiradas a lo largo del tiempo (swaps, eurodólares, bonos corporativos de Moody's en versiones antiguas): comprobar la disponibilidad; el «Build Your Package» del DDP se retira en noviembre de 2026.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «federalreserve.gov releases H.15 selected interest rates commercial paper rates»; WebFetch: sí, publicación de 24/05/2010 y página actual)
- **Origen:** Alta F9_S5 (2026-11-02).

#### RF-0658 · Q 87 (A) — Bank of England — Yield curves (gilts nominal, real e inflación implícita; curva OIS SONIA)

- **Canal oficial (URL raíz):** https://www.bankofengland.co.uk/statistics/yield-curves (conceptos: https://www.bankofengland.co.uk/statistics/yield-curves/terminology-and-concepts)
- **Emisor:** Bank of England
- **Temática:** TF-19 Curvas de tipos, crédito e inflación implícita: datos (principal) · secundarias: TF-18
- **Calidad Q:** 87 (A) — Primariedad 18/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 10/10 · Acceso 10/10
- **Tipología:** primaria (estimación oficial del banco central)
- **Acceso:** Abierto (últimas curvas antes del mediodía del día hábil siguiente; archivo mensual; sin API para el archivo)
- **Ámbitos:** Curvas diarias al contado y forwards instantáneos: gilts nominal (hasta 40 años), real e inflación implícita (RPI); curva OIS sobre SONIA (hasta 25 años) usada para la senda de mercado del Bank Rate en el Monetary Policy Report; método Waggoner ajustado (Anderson y Sleath, 2001)
- **Motivo de inclusión y uso:** Única fuente oficial de inflación implícita británica y de la senda esperada del Bank Rate. AG-25 y AG-24.
- **Sesgos y cautelas:** El BoE no publica código ni selección de instrumentos; la inflación implícita es sobre RPI (alineación con CPIH prevista en 2030); curvas LIBOR suprimidas a finales de 2021.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Bank of England yield curves nominal real inflation spot curves data»; WebFetch: sí)
- **Origen:** Alta F9_S5 (2026-11-02).

#### RF-0657 · Q 86 (A) — Deutsche Bundesbank — Estructura temporal de tipos de los valores federales cotizados (Zinsstrukturkurve) y rendimientos

- **Canal oficial (URL raíz):** https://www.bundesbank.de/en/statistics/money-and-capital-markets/interest-rates-and-yields/daily-term-structure-on-listed-federal-securities-651570 (tablas: https://www.bundesbank.de/en/statistics/money-and-capital-markets/interest-rates-and-yields/term-structure-of-interest-rates/term-structure-of-interest-rates-793596 · series estimadas: https://www.bundesbank.de/en/statistics/overview-of-the-statistical-series/-/a-term-structure-of-interest-rates-in-the-debt-securities-market-estimated-values-listed-federal-securities--809524)
- **Emisor:** Deutsche Bundesbank
- **Temática:** TF-19 Curvas de tipos, crédito e inflación implícita: datos (principal) · secundarias: TF-01
- **Calidad Q:** 86 (A) — Primariedad 18/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 10/10 · Acceso 9/10
- **Tipología:** primaria (estimación oficial del banco central)
- **Acceso:** Abierto (PDF diario y base de datos de series temporales; ejemplo de serie BBSIS.M.I.ZST.ZI.EUR.S1311.B.A604.R01XX.R.A.A._Z._Z.A; PDF visto de 30/10/2026)
- **Ámbitos:** Curva cupón cero estimada (Svensson) de la deuda federal alemana, diaria y mensual, con series largas; páginas hermanas de tipos del mercado monetario, rendimientos de la deuda en circulación, precios y rendimientos de valores federales y tipos reales esperados
- **Motivo de inclusión y uso:** Curva Bund de referencia (activo refugio del euro) con historia larga; base para diferenciales soberanos frente a Alemania. AG-25.
- **Sesgos y cautelas:** Escasez de Bunds y efecto colateral pueden deprimir los rendimientos cortos (no solo expectativas); la página no describe el método en línea (ver PDF).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Bundesbank term structure of interest rates listed Federal securities Svensson time series»; WebFetch: sí)
- **Origen:** Alta F9_S5 (2026-11-02).

#### RF-0652 · Q 85 (A) — Federal Reserve Board — Nominal Yield Curve (Gürkaynak, Sack y Wright; feds200628)

- **Canal oficial (URL raíz):** https://www.federalreserve.gov/data/nominal-yield-curve.htm (CSV: https://www.federalreserve.gov/data/yield-curve-tables/feds200628.csv · documento: https://www.federalreserve.gov/econres/feds/the-us-treasury-yield-curve-1961-to-the-present.htm)
- **Emisor:** Board of Governors of the Federal Reserve System (personal de investigación; Gürkaynak, Sack y Wright, 2006/2007)
- **Temática:** TF-19 Curvas de tipos, crédito e inflación implícita: datos (principal) · secundarias: TF-13
- **Calidad Q:** 85 (A) — Primariedad 17/20 · Historial 10/20 · Transparencia 15/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 8/10 · Acceso 10/10
- **Tipología:** primaria (estimación del banco central con metodología publicada)
- **Acceso:** Abierto (CSV actualizado semanalmente)
- **Ámbitos:** Curva cupón cero y a plazo diaria del Tesoro de EE. UU. desde 1961 (Nelson-Siegel-Svensson), parámetros del ajuste; rendimientos y forwards a cualquier plazo
- **Motivo de inclusión y uso:** Curva cupón cero estándar en la investigación y base de los modelos de prima de plazo (ACM, RF-0655). AG-25: forwards implícitos, pendiente y curvatura.
- **Sesgos y cautelas:** Producto de investigación, no estadística oficial: sujeto a retrasos, revisiones o cambios sin aviso; excluye letras y valores con menos de tres meses.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Federal Reserve Board data nominal yield curve Gurkaynak Sack Wright TIPS yield curve Kim Wright term premium»; WebFetch: sí, página del documento y página «Yield Curve Models and Data»)
- **Origen:** Alta F9_S5 (2026-11-02).

#### RF-0653 · Q 83 (A) — Federal Reserve Board — TIPS Yield Curve and Inflation Compensation (breakevens)

- **Canal oficial (URL raíz):** https://www.federalreserve.gov/data/tips-yield-curve-and-inflation-compensation.htm (documento: https://www.federalreserve.gov/econres/feds/the-tips-yield-curve-and-inflation-compensation.htm · DOI del FEDS 2008-05: 10.17016/FEDS.2008.05)
- **Emisor:** Board of Governors of the Federal Reserve System (Gürkaynak, Sack y Wright, 2008/2010)
- **Temática:** TF-19 Curvas de tipos, crédito e inflación implícita: datos (principal) · secundarias: TF-13
- **Calidad Q:** 83 (A) — Primariedad 17/20 · Historial 10/20 · Transparencia 15/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 7/10 · Acceso 9/10
- **Tipología:** primaria (estimación del banco central con metodología publicada)
- **Acceso:** Abierto
- **Ámbitos:** Curva real cupón cero de los TIPS, compensación por inflación (breakeven) al contado y a plazo (p. ej., 5 años dentro de 5 años)
- **Motivo de inclusión y uso:** Inflación implícita de mercado en EE. UU. con curvas ajustadas (no solo los vencimientos constantes del H.15). AG-25: anclaje de expectativas de inflación a largo plazo.
- **Sesgos y cautelas:** La compensación por inflación incluye primas de riesgo y de liquidez de los TIPS (no es expectativa pura); producto de investigación sujeto a revisiones.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Federal Reserve Board data nominal yield curve Gurkaynak Sack Wright TIPS yield curve Kim Wright term premium»; WebFetch: sí sobre la página índice «Yield Curve Models and Data», que la enlaza; la página propia no se pudo cargar)
- **Origen:** Alta F9_S5 (2026-11-02).

#### RF-0655 · Q 82 (A) — Federal Reserve Bank of New York — ACM Term Premia (Adrian, Crump y Moench)

- **Canal oficial (URL raíz):** https://www.newyorkfed.org/research/data_indicators/term-premia-tabs (presentación: https://libertystreeteconomics.newyorkfed.org/2014/05/treasury-term-premia-1961-present/)
- **Emisor:** Federal Reserve Bank of New York (Adrian, Crump y Moench, 2013)
- **Temática:** TF-19 Curvas de tipos, crédito e inflación implícita: datos (principal) · secundarias: TF-13
- **Calidad Q:** 82 (A) — Primariedad 15/20 · Historial 10/20 · Transparencia 15/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 8/10 · Acceso 9/10
- **Tipología:** secundaria (estimación de modelo publicada por el banco central)
- **Acceso:** Abierto
- **Ámbitos:** Prima de plazo diaria del Tesoro de EE. UU. desde el 14/06/1961, vencimientos anuales de 1 a 10 años, rendimientos ajustados y tipo corto medio esperado (modelo afín de cinco factores sobre la curva GSW, RF-0652)
- **Motivo de inclusión y uso:** Estimación de prima de plazo más citada en el mercado; separa expectativas de política monetaria y compensación por riesgo de duración. AG-25.
- **Sesgos y cautelas:** Resultado de modelo sin encuestas (puede atribuir a expectativas lo que es prima); actualización semanal según la presentación de 2014; la página de datos no pudo cargarse (lectura vía Liberty Street, RF-0025).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «New York Fed ACM term premia Adrian Crump Moench data»; WebFetch: sí sobre la entrada de Liberty Street de mayo de 2014; la página de datos no se pudo cargar)
- **Origen:** Alta F9_S5 (2026-11-02).

#### RF-0661 · Q 82 (A) — Federal Reserve Bank of Cleveland — Inflation Expectations (modelo de expectativas, tipos reales y prima de riesgo de inflación)

- **Canal oficial (URL raíz):** https://www.clevelandfed.org/indicators-and-data/inflation-expectations
- **Emisor:** Federal Reserve Bank of Cleveland
- **Temática:** TF-19 Curvas de tipos, crédito e inflación implícita: datos (principal) · secundarias: TF-01
- **Calidad Q:** 82 (A) — Primariedad 15/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 9/10 · Acceso 9/10
- **Tipología:** secundaria (estimación de modelo publicada por un banco de la Reserva Federal)
- **Acceso:** Abierto (actualización mensual el día del IPC; descarga de datos)
- **Ámbitos:** Inflación esperada media de 1 a 30 años, tipos reales, prima de riesgo de inflación y prima de riesgo real, a partir de rendimientos del Tesoro, IPC, swaps de inflación y encuestas (SPF, Blue Chip). Dato visto: expectativa a 10 años 2,73 % (actualización de 14/10/2026)
- **Motivo de inclusión y uso:** Separa el breakeven de mercado en expectativa y prima de riesgo, lo que no hacen RF-0653 ni FRED. AG-25: tipos reales ex ante y anclaje de expectativas.
- **Sesgos y cautelas:** Resultado de modelo; usó un nowcast cuando faltó el IPC de octubre de 2025; mensual (no capta movimientos diarios).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Cleveland Fed inflation expectations model real interest rates inflation risk premium»; WebFetch: sí)
- **Origen:** Alta F9_S5 (2026-11-02).

#### RF-0664 · Q 82 (A) — ESMA — CEREP (Central Rating Repository): rendimiento de las agencias de calificación

- **Canal oficial (URL raíz):** https://registers.esma.europa.eu/cerep-publication/ (ayuda: https://registers.esma.europa.eu/cerep-publication/helpFile/ · nota: https://www.esma.europa.eu/press-news/esma-news/esma-publishes-latest-data-credit-rating-agencies-performance)
- **Emisor:** European Securities and Markets Authority (ESMA)
- **Temática:** TF-19 Curvas de tipos, crédito e inflación implícita: datos (principal) · secundarias: TF-02
- **Calidad Q:** 82 (A) — Primariedad 18/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 7/10 · Acceso 9/10
- **Tipología:** primaria (estadística supervisora a partir de los datos declarados por las agencias registradas o certificadas en la UE)
- **Acceso:** Abierto
- **Ámbitos:** Estadísticas semestrales de actividad de calificación, tasas de impago y matrices de transición por agencia, clase de activo (empresas, soberanos, finanzas estructuradas), región y horizonte
- **Motivo de inclusión y uso:** Comparación independiente del comportamiento histórico de las calificaciones de todas las agencias (no solo las tres grandes); calibración de probabilidades de impago por nivel de rating. AG-25.
- **Sesgos y cautelas:** Datos declarados por las propias agencias; la URL antigua (cerep.esma.europa.eu) citada en la nota de 25/05/2018 ha migrado a registers.esma.europa.eu; comprobar la vigencia del periodo publicado.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «ESMA CEREP central repository credit rating agencies default rates transition matrices»; WebFetch: sí, nota de prensa de ESMA)
- **Origen:** Alta F9_S5 (2026-11-02).

#### RF-0666 · Q 82 (A) — Federal Reserve Board — Senior Loan Officer Opinion Survey on Bank Lending Practices (SLOOS)

- **Canal oficial (URL raíz):** https://www.federalreserve.gov/data/sloos.htm
- **Emisor:** Board of Governors of the Federal Reserve System
- **Temática:** TF-19 Curvas de tipos, crédito e inflación implícita: datos (principal) · secundarias: TF-01
- **Calidad Q:** 82 (A) — Primariedad 17/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 7/10 · Acceso 10/10
- **Tipología:** primaria (encuesta oficial a bancos)
- **Acceso:** Abierto (trimestral, antes de cuatro reuniones del FOMC; última vista: julio de 2026)
- **Ámbitos:** Cambios en criterios y condiciones de concesión de préstamos y en la demanda de crédito de empresas y hogares; hasta 80 grandes bancos nacionales y 24 sucursales de bancos extranjeros; preguntas especiales de actualidad
- **Motivo de inclusión y uso:** Indicador adelantado del ciclo de crédito y de los impagos (el endurecimiento de criterios precede a la ampliación de diferenciales). AG-25.
- **Sesgos y cautelas:** Respuestas cualitativas en «porcentaje neto»; solo crédito bancario (no crédito privado ni bonos).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «federalreserve.gov releases H.15 selected interest rates commercial paper rates» → enlace desde la página H.15; WebFetch: sí)
- **Origen:** Alta F9_S5 (2026-11-02).

#### RF-0667 · Q 81 (A) — FINRA — Fixed Income Data (TRACE: agregados del mercado de bonos)

- **Canal oficial (URL raíz):** https://www.finra.org/finra-data/fixed-income (datos, informes y publicaciones TRACE: https://www.finra.org/filing-reporting/trade-reporting-and-compliance-engine-trace/trace-data-reports-publications · TRACE FactBook 2025: https://www.finra.org/sites/default/files/2026-02/TRACE_FactBook_2025.pdf)
- **Emisor:** Financial Industry Regulatory Authority (FINRA)
- **Temática:** TF-19 Curvas de tipos, crédito e inflación implícita: datos (principal) · secundarias: TF-06, TF-02
- **Calidad Q:** 81 (A) — Primariedad 19/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 14/15 · Independencia 9/10 · Actualidad 10/10 · Acceso 7/10
- **Tipología:** primaria (datos de operaciones declaradas al regulador)
- **Acceso:** Consulta y agregados abiertos (aceptando el acuerdo de usuario); ficheros de fin de día, tiempo real e históricos ampliados de pago
- **Ámbitos:** Agregados diarios de actividad y sentimiento del mercado de bonos corporativos y de agencias, bonos más negociados, volumen mensual (corporativos, agencias, titulizaciones), estadísticas agregadas de negociación del Tesoro, actividad en ABS/MBS/TBA/CMO; consulta de operaciones por CUSIP
- **Motivo de inclusión y uso:** Liquidez y volumen reales del crédito de EE. UU. (no cotizaciones indicativas); detección de ventas forzadas o sequía de liquidez. AG-25. Producto distinto de las estadísticas de margen del mismo emisor (RF-0342).
- **Sesgos y cautelas:** No cubre municipales (ver EMMA/MSRB); FINRA no garantiza la exactitud; parte de los datos detallados requiere suscripción.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «FINRA TRACE corporate bond market data aggregates»; WebFetch: sí)
- **Origen:** Alta F9_S5 (2026-11-02).

#### RF-0669 · Q 81 (A) — BCE — Survey of Professional Forecasters (SPF): expectativas de inflación de la zona del euro

- **Canal oficial (URL raíz):** https://www.ecb.europa.eu/stats/ecb_surveys/survey_of_professional_forecasters/html/index.en.html (ejemplo de nota trimestral: https://www.ecb.europa.eu//press/pr/date/2024/html/ecb.pr240126~fae16e158f.en.html)
- **Emisor:** Banco Central Europeo
- **Temática:** TF-19 Curvas de tipos, crédito e inflación implícita: datos (principal) · secundarias: TF-01
- **Calidad Q:** 81 (A) — Primariedad 15/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 7/10 · Acceso 10/10
- **Tipología:** primaria (encuesta oficial; las respuestas son previsiones de expertos)
- **Acceso:** Abierto (resultados trimestrales y microdatos anonimizados en el BCE Data Portal)
- **Ámbitos:** Previsiones trimestrales de HICP general y subyacente, PIB real y paro para el año en curso, los dos siguientes y el largo plazo (unos cinco años vista), con distribuciones de probabilidad. Ejemplo: 1T2024, 59 respuestas, inflación a largo plazo 2,0 %
- **Motivo de inclusión y uso:** Referencia de expectativas de inflación a largo plazo de encuesta para contrastar con la inflación implícita de mercado (swaps y bonos ligados) y estimar la prima de riesgo de inflación en el euro. AG-25.
- **Sesgos y cautelas:** Opinión de expertos (regla F9-a); trimestral; la página índice no se pudo cargar (se leyó la nota de prensa del 26/01/2024).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «ECB Survey of Monetary Analysts SMA results and Survey of Professional Forecasters inflation expectations»; WebFetch: sí, nota de prensa del SPF 1T2024)
- **Origen:** Alta F9_S5 (2026-11-02).

#### RF-0654 · Q 80 (A) — Federal Reserve Board — Three-Factor Nominal Term Structure Model (Kim y Wright): prima de plazo

- **Canal oficial (URL raíz):** https://www.federalreserve.gov/data/three-factor-nominal-term-structure-model.htm (índice: https://www.federalreserve.gov/data/yield-curve-models.htm)
- **Emisor:** Board of Governors of the Federal Reserve System (modelo de Kim y Wright, 2005)
- **Temática:** TF-19 Curvas de tipos, crédito e inflación implícita: datos (principal) · secundarias: TF-13
- **Calidad Q:** 80 (A) — Primariedad 15/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 7/10 · Acceso 9/10
- **Tipología:** secundaria (estimación de modelo publicada por el banco central)
- **Acceso:** Abierto
- **Ámbitos:** Descomposición de los rendimientos nominales del Tesoro en tipo corto esperado y prima de plazo (modelo afín de tres factores con encuestas)
- **Motivo de inclusión y uso:** Segunda estimación oficial de la prima de plazo, para contrastar con ACM (RF-0655): la divergencia entre modelos mide la incertidumbre. AG-25.
- **Sesgos y cautelas:** Resultado de modelo (no observable); sensible a la especificación y al uso de encuestas; producto de investigación sin calendario garantizado.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Federal Reserve Board data nominal yield curve Gurkaynak Sack Wright TIPS yield curve Kim Wright term premium»; WebFetch: sí sobre la página índice y la FEDS Note «Robustness of long-maturity term premium estimates» (2017), que compara KW y ACM; la página propia no se pudo cargar)
- **Origen:** Alta F9_S5 (2026-11-02).

#### RF-0662 · Q 80 (A) — Federal Reserve Board — Excess Bond Premium (Gilchrist y Zakrajšek): datos mensuales

- **Canal oficial (URL raíz):** https://www.federalreserve.gov/econres/notes/feds-notes/updating-the-recession-risk-and-the-excess-bond-premium-20161006.html (CSV: https://www.federalreserve.gov/econres/notes/feds-notes/ebp_csv.csv · artículo original: https://www.nber.org/papers/w17021)
- **Emisor:** Board of Governors of the Federal Reserve System (personal de investigación; medida de Gilchrist y Zakrajšek, 2012)
- **Temática:** TF-19 Curvas de tipos, crédito e inflación implícita: datos (principal) · secundarias: TF-13
- **Calidad Q:** 80 (A) — Primariedad 15/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 7/10 · Acceso 9/10
- **Tipología:** secundaria (estimación de modelo publicada por el banco central)
- **Acceso:** Abierto (CSV mensual, hacia el cuarto día hábil de cada mes; desde enero de 1973)
- **Ámbitos:** Prima de bonos en exceso (componente del diferencial de crédito corporativo no explicado por el riesgo esperado de impago) y probabilidad de recesión en EE. UU. implícita en el modelo
- **Motivo de inclusión y uso:** Indicador adelantado de la actividad y del apetito por riesgo de los intermediarios; distingue precio del riesgo de cantidad de riesgo. AG-25 y AG-14 (riesgo de recesión).
- **Sesgos y cautelas:** Toda la historia se revisa cada mes (balances y muestra de bonos); producto de investigación sin calendario garantizado; publicación aplazada en periodos de silencio del FOMC.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «excess bond premium Gilchrist Zakrajsek data update and New York Fed Corporate Bond Market Distress Index»; WebFetch: sí, FEDS Note de 06/10/2016)
- **Origen:** Alta F9_S5 (2026-11-02).

#### RF-0663 · Q 79 (B) — Federal Reserve Bank of New York — Corporate Bond Market Distress Index (CMDI)

- **Canal oficial (URL raíz):** https://www.newyorkfed.org/research/policy/cmdi (presentación: https://libertystreeteconomics.newyorkfed.org/2022/06/what-is-corporate-bond-market-distress/)
- **Emisor:** Federal Reserve Bank of New York (Boyarchenko, Crump, Kovner y Shachar; Staff Report 957)
- **Temática:** TF-19 Curvas de tipos, crédito e inflación implícita: datos (principal) · secundarias: TF-06
- **Calidad Q:** 79 (B) — Primariedad 15/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 7/10 · Acceso 8/10
- **Tipología:** secundaria (indicador compuesto publicado por el banco central)
- **Acceso:** Abierto (lecturas mensuales)
- **Ámbitos:** Índice de tensión del mercado de bonos corporativos de EE. UU. (grado de inversión y high yield) que combina siete rasgos de funcionamiento: volúmenes y precios del mercado primario, volúmenes, liquidez y precios del secundario, precios ajustados por impago y cotizaciones de bonos no negociados (Mergent FISD, FINRA TRACE, ICE)
- **Motivo de inclusión y uso:** Detecta disfunción del mercado (no solo diferenciales altos) mediante un criterio de «preponderancia de métricas». AG-25 y AG-14.
- **Sesgos y cautelas:** Indicador de investigación; mensual; la página de datos no se cargó (lectura vía Liberty Street, RF-0025).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «excess bond premium Gilchrist Zakrajsek data update and New York Fed Corporate Bond Market Distress Index»; WebFetch: sí sobre la entrada de Liberty Street de 29/06/2022, que enlaza la página de datos)
- **Origen:** Alta F9_S5 (2026-11-02).

#### RF-0659 · Q 77 (B) — S&P Dow Jones Indices — Índices de CDS iTraxx y CDX

- **Canal oficial (URL raíz):** https://www.spglobal.com/spdji/en/indices/products/markit-cdx.html (guía: https://www.spglobal.com/spdji/en/documents/campaigns/cds-indices-primer.pdf · reglas CDX: https://www.spglobal.com/spdji/en/documents/methodologies/Markit%20CDX%20HY%20and%20IG%20Rules%20Feb2022.pdf)
- **Emisor:** S&P Dow Jones Indices (S&P Global), creador y administrador de iTraxx y CDX (antes Markit / IHS Markit)
- **Temática:** TF-19 Curvas de tipos, crédito e inflación implícita: datos (principal) · secundarias: TF-17, TF-15
- **Calidad Q:** 77 (B) — Primariedad 17/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 14/15 · Independencia 7/10 · Actualidad 10/10 · Acceso 6/10
- **Tipología:** primaria (índices negociables; precios aportados por bancos con control de calidad)
- **Acceso:** Precios diarios y características públicos en la web; series históricas completas de pago; reglamentos abiertos
- **Ámbitos:** iTraxx Europe (125 nombres, cupón 100 pb), iTraxx Crossover (75, 500 pb), CDX.NA.IG (125), CDX.NA.HY (100, cotiza en precio), CDX.EM, además de iTraxx Japón, Australia y Asia ex Japón; renovación semestral (marzo y septiembre); subastas de eventos de crédito
- **Motivo de inclusión y uso:** Medida más líquida y diaria del riesgo de crédito corporativo agregado en Europa y EE. UU. (Main y Crossover como termómetros de aversión al riesgo). AG-25 y AG-23 (derivados de crédito).
- **Sesgos y cautelas:** Proveedor comercial; cambios de serie en cada renovación (empalmar series «on-the-run»); el CDS incluye prima de liquidez y de contraparte. La ficha RF-0056 cubre los índices de renta variable del mismo emisor.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «S&P Global iTraxx CDX credit default swap indices rules roll»; WebFetch: sí, página CDX y guía «CDS Indices Primer» 2025)
- **Origen:** Alta F9_S5 (2026-11-02).

#### RF-0660 · Q 76 (B) — ICE Data Indices — ICE BofA bond indices (diferenciales ajustados por opciones)

- **Canal oficial (URL raíz):** https://fred.stlouisfed.org/data/BAMLH0A0HYM2 (distribución pública de ICE Data Indices en FRED; p. ej., también https://fred.stlouisfed.org/data/BAMLHE00EHYIOAS para el high yield en euros)
- **Emisor:** ICE Data Indices, LLC (Intercontinental Exchange; antes índices de BofA Merrill Lynch)
- **Temática:** TF-19 Curvas de tipos, crédito e inflación implícita: datos (principal) · secundarias: TF-15
- **Calidad Q:** 76 (B) — Primariedad 16/20 · Historial 10/20 · Transparencia 11/15 · Autoridad 14/15 · Independencia 8/10 · Actualidad 10/10 · Acceso 7/10
- **Tipología:** primaria (índices del proveedor) redistribuida en FRED
- **Acceso:** Abierto en FRED con licencia restrictiva (solo uso interno; desde abril de 2026, solo tres años de historia en FRED); historia completa de pago en ICE
- **Ámbitos:** Diferenciales ajustados por opciones (OAS), rendimientos efectivos y rentabilidades totales de índices de bonos corporativos investment grade y high yield de EE. UU., euro y emergentes, por calificación (AAA a CCC). Dato visto: OAS high yield EE. UU. 3,26 % el 29/10/2026
- **Motivo de inclusión y uso:** Serie de referencia de los diferenciales de crédito al contado (bonos), complemento de los CDS (RF-0659). AG-25: valoración del crédito por calificación y en el ciclo.
- **Sesgos y cautelas:** Reproducción y difusión a terceros requieren permiso de ICE (citar cifras puntuales con fecha, no redistribuir series); historia en FRED recortada.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «ICE BofA bond indices ICE Data Indices option-adjusted spread high yield index methodology»; WebFetch: sí, página de datos de FRED)
- **Origen:** Alta F9_S5 (2026-11-02).

#### RF-0665 · Q 72 (B) — S&P Global Ratings — Serie «Default, Transition, and Recovery» (estudios anuales de impago y transición)

- **Canal oficial (URL raíz):** https://www.spglobal.com/ratings/en/research/ (ejemplos: https://www.spglobal.com/ratings/en/research/articles/220808-default-transition-and-recovery-overall-stable-corporate-default-trends-camouflage-pockets-of-vulnerabilit-12465947 · estudio anual de Asia 2019: https://www.spglobal.com/ratings/en/research/articles/201014-default-transition-and-recovery-2019-annual-asia-corporate-default-and-rating-transition-study-11669637)
- **Emisor:** S&P Global Ratings
- **Temática:** TF-19 Curvas de tipos, crédito e inflación implícita: datos (principal) · secundarias: TF-05
- **Calidad Q:** 72 (B) — Primariedad 17/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 14/15 · Independencia 5/10 · Actualidad 9/10 · Acceso 5/10
- **Tipología:** primaria (estadística propia de impagos de entidades calificadas) y secundaria (análisis)
- **Acceso:** Algunos artículos abiertos; la mayoría con registro o suscripción
- **Ámbitos:** Recuento corriente de impagos corporativos mundiales, tasas de impago por calificación, sector y región, matrices de transición y recuperaciones; estudios anuales globales y regionales (EE. UU., Europa, Asia, Japón)
- **Motivo de inclusión y uso:** Tasas de impago históricas por calificación para traducir diferenciales en pérdidas esperadas. AG-25. Publicación específica del emisor de RF-0234.
- **Sesgos y cautelas:** Solo entidades calificadas por S&P; conflicto «emisor-pagador»; la página de un estudio leído cargó vacía.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «annual default study corporate default and recovery rates Moody's S&P Global Ratings default transition study 2025»; WebFetch: sí, la página no mostró contenido)
- **Origen:** Alta F9_S5 (2026-11-02).

#### RF-0668 · Q 71 (B) — Scope Ratings — calificaciones y anuncios (agencia europea)

- **Canal oficial (URL raíz):** https://scoperatings.com/whoweare (ejemplos de anuncios soberanos: https://scoperatings.com/announcements/rating-announcement/EN/180994 · https://scoperatings.com/announcements/rating-announcement/EN/181031)
- **Emisor:** Scope Ratings (Scope Group)
- **Temática:** TF-19 Curvas de tipos, crédito e inflación implícita: datos (principal) · secundarias: TF-05
- **Calidad Q:** 71 (B) — Primariedad 16/20 · Historial 10/20 · Transparencia 11/15 · Autoridad 12/15 · Independencia 5/10 · Actualidad 10/10 · Acceso 7/10
- **Tipología:** primaria (acciones de calificación) y secundaria (análisis)
- **Acceso:** Anuncios de calificación públicos; parte de la investigación con registro
- **Ámbitos:** Calificaciones de soberanos (p. ej., mejora de España a A+ con perspectiva estable; rebaja de Francia a A+), organismos supranacionales (FEEF), bancos, empresas y finanzas estructuradas; única agencia europea aceptada por el BCE en el marco ECAF (elegibilidad de colateral del Eurosistema)
- **Motivo de inclusión y uso:** Cuarta opinión de calificación con peso en la elegibilidad de colateral del BCE y a menudo distinta de las tres grandes (RF-0231, RF-0234) en soberanos europeos. AG-25: riesgo soberano europeo.
- **Sesgos y cautelas:** Conflicto «emisor-pagador»; menor historial que las grandes; la web no detalla el acceso a la investigación. Fitch Ratings no se dio de alta por no haberse podido verificar en esta tanda.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Scope Ratings European credit rating agency sovereign ratings», limitada a scoperatings.com; WebFetch: sí, página «Who we are»)
- **Origen:** Alta F9_S5 (2026-11-02).

## Lagunas de cobertura

Áreas con menos de 20 referencias verificadas tras la carga del 02/11/2026 (V3.2) (objetivo del propietario: 20–50 por área):

| Código | Temática | Verificadas | Faltan para 20 |
|---|---|---|---|
| — | Ninguna | — | — |

## Registro de bajas

Sin bajas en la emisión V3.0 (no hay duplicados exactos). Las semillas que BFA no logre verificar se registran aquí con motivo «semilla no verificable».

| REF-id | Título | Motivo | Fecha | Sustituta |
|---|---|---|---|---|
| RF-0047 | Research Affiliates | Contenido retirado del emisor original: researchaffiliates.com (incluidos la herramienta Asset Allocation Interactive y los PDF de publicaciones) redirige a una página que anuncia el cambio de nombre del negocio de gestión a Syzygy Asset Management y la venta de los índices RAFI a VettaFi (TMX). La URL de la semilla ya no ofrece el contenido descrito. | 2026-11-02 | — (ver la tanda 3 si se verifica una sucesora) |
| RF-0425 | FRASER | Duplicado de RF-0201 | 2026-11-02 | RF-0462 |
| RF-0317 | Trading Economics | Duplicado de RF-0244 | 2026-11-02 | RF-0463 |
| RF-0445 | Stanford HAI — AI Index Report | Duplicado de RF-0349 | 2026-11-02 | RF-0349 |
| RF-0557 | AFMA — Australian Financial Markets Report | El informe no tiene edición vigente localizable: la búsqueda solo devuelve la edición de 2015 (reseña de Investor Daily) y la de 2009; afma.com.au sigue activo pero no publica el informe (solo memorias anuales, la última de 2025, y avisos de mercado). URL antigua (afma.com.au/home.html) sin sucesora para este producto; pertinencia baja para TF-17. | 2026-11-02 | RF-0560 |
| RF-0559 | TriOptima (OSTTRA) — estadísticas de compresión triReduce | La página de estadísticas ya no existe: la URL de TriOptima/CME redirige (302) a la página comercial de compresión de OSTTRA, que describe el servicio pero no publica cifras de nocional eliminado ni estadísticas por ciclo. Sin canal de datos públicos; la compresión se sigue con los datos de las cámaras (RF-0544, RF-0556) y del BIS (RF-0540). | 2026-11-02 | RF-0562 |

## Historial de versión

- V2.4 (31/10/2026): 14 entradas de fuente y 3 piezas de la carga de arranque del operador.
- V3.0 (01/11/2026): reorganización por familias TF- del Anexo D, Q con la rúbrica de fuentes y orden por calidad, canal oficial volcado a cada entrada, 83 fuentes semilla pendientes de verificación, Novedades, lagunas y registro de bajas.
| V3.1 | 02/11/2026 | Carga verificada por búsqueda web: 194 referencias nuevas, 81 fichas existentes reverificadas o reparadas, 4 bajas; reordenación por temática y Q; índice con recuento de verificadas. |
| V3.2 | 02/11/2026 | Áreas nuevas para los tipos de activo de la V5.0 (índices, fondos y vehículos, derivados, monetario, tipos/crédito/volatilidad): 104 referencias nuevas verificadas por búsqueda web, 0 fichas existentes reverificadas o reparadas, 2 bajas; reordenación por temática y Q; índice con recuento de verificadas. |

