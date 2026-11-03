# Documentación para el Motor de Cálculo Avanzado

**Proyecto Robot Investor · Bloque A — Analizador de Tendencias de Inversión · Ecosistema Robot Investor**

**Archivo operativo · Versión 2.3 · 26/10/2026 · Estado: EN OPERACIÓN (carga de arranque de 13 fuentes verificadas, 25/10/2026; estado «retirada» en vigor por la adenda V1.2 del Bloque A, 26/10/2026)**

Este archivo está listo para su uso. Contiene su estructura completa, sus reglas y una **carga de arranque de 13 fuentes matemáticas reales verificadas**, dispuesta por el operador el 25/10/2026, que muestra cómo se introducen las fuentes (fichas en formato compacto desde el 26/10/2026). A partir de aquí, el mantenimiento corresponde al agente propietario conforme a los contratos del Documento 0. La ubicación física y la tecnología del archivo siguen siendo parámetros del operador (Documento 0, Anexo A): este archivo fija la propiedad y la estructura, no la tecnología. La sección 8 añade el anexo del operador con las fuentes fiables específicas de verificación y acceso de cada ficha o entrada registrada (25/10/2026). El 26/10/2026, por disposición del operador, las fichas se convirtieron al formato compacto (bloques de párrafos con los campos etiquetados en negrita, agrupados por temas, en sustitución de la tabla vertical de campos) para contener la extensión y el peso del documento Word ante nuevas altas: el conjunto de campos y los valores de cada ficha no varían y el esquema 1.0 queda intacto (conversión verificada campo a campo). Por la adenda V1.2 del Bloque A (26/10/2026), las fichas admiten además el estado «retirada»: retirada lógica y trazable por revisión de conjunto (convención 9), nunca un borrado físico.

---

## 1. Rol del archivo en la arquitectura del Bloque A

La «Documentación para el Motor de Cálculo Avanzado» (añadida al inventario del Documento 0, 2.3, con la Versión óptima V1) es el fondo de conocimiento matemático y técnico que respalda los métodos del **Motor de Cálculo Avanzado**: artículos revisados por pares, documentos de trabajo, tesis, estándares y manuales que fundamentan los cálculos que el Motor presta como servicio. Cuando el Motor ejecuta un cálculo, la base metodológica de ese cálculo debe poder rastrearse hasta las fichas de este archivo; cuando el Auditor re-ejecuta de forma independiente (CT-12), ambas ejecuciones apoyan en las mismas fichas.

Este archivo tiene una particularidad frente a los otros archivos del bloque: el Motor no es un agente exclusivo del Bloque A, sino un **servicio compartido del ecosistema Robot Investor** (en vigor desde el 23/10/2026). Sus clientes en el bloque son el Analizador de Tendencias de Inversión (14.4), el Buscador, el Documentador y el Orquestador (F.5), y el Auditor en el circuito de auditoría (F.4); en la arquitectura global, el servicio atiende igualmente a los demás bloques según sus contratos.

**Alcance ecosistémico — archivo único para todos los bloques.** El operador ha confirmado que este archivo **será utilizado en los bloques posteriores, igual que el Motor que documenta**: el Documento 0, 2.3, ya fija que sus entradas se indexan «por solicitante, familia y fecha para que cualquier servicio pueda reconstruirse sin ayuda del Motor», y esa reconstrucción es precisamente lo que exigirán los bloques que consuman el servicio (CT-11/CT-12). Por eso: ningún bloque posterior creará una documentación paralela del Motor; los agentes de esos bloques que consuman el servicio consultan este archivo en solo lectura, por acceso a archivo, conforme a la matriz de archivos de su bloque y sin mensajes agente a agente; y la escritura no sale del Documentador para el Motor de Cálculo Avanzado (Bloque A). Un cambio en este archivo puede afectar a más de un bloque: su disciplina de versionado es más estricta y sus entradas distinguen qué métodos del Motor respalda cada fuente.

Su propietario es el **Documentador para el Motor de Cálculo Avanzado**, con escritura exclusiva; el **Motor** lo consulta en solo lectura y no escribe en él. No debe confundirse con el archivo «Registro de cálculos del Motor de cálculo avanzado», que es distinto: ese registro lo gestiona el propio Motor (servicios, rechazos, re-ejecuciones), mientras que esta Documentación alberga el conocimiento que fundamenta los cálculos. Tampoco debe confundirse con la «Documentación para tendencias de inversión» (dominio del análisis de tendencias) ni con el «Fondo metodológico» (metodología de búsqueda, también ecosistémico): aquí el ámbito es matemático aplicado, sin conclusiones de inversión.

## 2. Ficha de uso para el agente

| Campo | Detalle |
|---|---|
| Nombre canónico (Documento 0, 2.3) | «Documentación para el Motor de Cálculo Avanzado» |
| Naturaleza del archivo | Fondo documental de conocimiento matemático aplicado que respalda los métodos del servicio de cálculo; archivo de evidencia y trazabilidad, no entregable |
| Alcance del archivo | Ecosistémico: acompaña al servicio de cálculo compartido. Será utilizado en los bloques posteriores que consuman el Motor (CT-11/CT-12), en solo lectura y por acceso a archivo, sin creación de documentación paralela |
| Propietario (escritura) | Documentador para el Motor de Cálculo Avanzado (escritura exclusiva) |
| Lectores autorizados | Motor de Cálculo Avanzado (solo lectura); Orquestador técnico y Auditor (extractos y paquetes); clientes del servicio, con carácter informativo; y, en los bloques posteriores que consuman el servicio, sus agentes para la reconstrucción de servicios (solo lectura) |
| Cuándo leerlo | El Motor, antes de invocar o documentar un método y al reconstruir un cálculo; el Auditor, en la re-ejecución independiente (CT-12); el Orquestador, al consolidar paquetes; los agentes de bloques posteriores, al reconstruir un servicio recibido |
| Cuándo escribir en él | El Documentador para el Motor, tras verificar cada fuente aprobada; en los ciclos MDOC_MAINTENANCE; al regenerar el índice |
| Reglas de escritura | Lectura antes de cada escritura; comprobación de duplicados (mismo documento, misma versión o mismo contenido por otra vía); solo añadir (los cambios de estado, calidad, licencia o ámbito son entradas nuevas con fecha y motivo); relectura posterior; única excepción: corrección o eliminación de enlaces rotos verificada en mantenimiento, anotada con fecha y motivo |
| Contratos implicados | CT-11 (servicio de cálculo, en vigor desde el 23/10/2026); CT-12 (re-ejecución independiente); CT-05 (paquete de servicio del Documentador para el Motor → Orquestador); CT-09 (guías para agentes de apoyo) |
| Modos de servicio asociados | MDOC_REQUEST y MDOC_MAINTENANCE (Documentador para el Motor) |
| Relación con otros archivos | Complementa al «Registro de cálculos del Motor» (acta de servicios, gestionado por el propio Motor) y se coordina con el «Fondo metodológico» (su homólogo en metodología de búsqueda, 9.7 del prompt del Documentador para el Motor), también de alcance ecosistémico; se diferencia de la «Documentación para tendencias de inversión» en el ámbito (matemático aplicado, no de tendencias) |
| Material auditable | Sí: fichas, versiones de documento y cambios de estado viajan en el paquete de servicio (CT-05) y sustentan el circuito de auditoría del cálculo (CT-11/CT-12) |
| Estado de esta copia | Archivo operativo en arranque; esquema 1.0; carga de arranque de 13 fichas del 25/10/2026 |

## 3. Convenciones de formato

1. **Identificadores únicos e inmutables** con prefijo `DOC-MOT-` y cuatro dígitos (DOC-MOT-0001, DOC-MOT-0002…) para cada ficha de fuente matemática.
2. **Fechado ISO 8601** en todos los campos de fecha.
3. **Registro de solo añadir**: nunca se borra ni se sobrescribe; cada cambio de estado, calidad, licencia o ámbito es una entrada nueva con fecha y motivo; si una versión posterior de un documento corrige o contradice materialmente a una registrada, el estado de la entrada original se actualiza mediante entrada nueva, sin borrarla.
4. **Versiones de documento explícitas**: la relación entre preprint, versión aceptada y versión publicada se registra cuando coexistan, con sus diferencias materiales conocidas (erratas incluidas) y la versión recomendada de acceso gratuito.
5. **Sin entrada sin verificación**: ninguna fuente se da de alta sin texto completo obtenido legalmente y sin superar el filtro de verificación académica del Documentador para el Motor, con anotación del nivel (completa o ligera) y de las comprobaciones omitidas.
6. **Etiquetado alineado con el catálogo temático** del Documentador para el Motor (áreas matemáticas aplicadas, 6.7 de su prompt), para que el índice sea consistente.
7. **Campo no disponible se declara**: «desconocido», «no aplicable» o «no consultado en la carga de arranque», nunca inventado.
8. **Formato compacto de ficha (desde el 26/10/2026, por disposición del operador)**: cada ficha se dispone como bloques de párrafos con los campos etiquetados en negrita, agrupados en cinco líneas temáticas (identificación y cita; acceso; clasificación y estado; contenido y uso; verificación y calidad), en sustitución de la tabla vertical de campos. El conjunto de campos y sus valores son los del esquema 1.0: solo cambia la disposición, verificada campo a campo en la conversión. Las fichas nuevas se incorporan directamente en formato compacto.
9. **Estado «retirada» (desde el 26/10/2026, adenda V1.2 del Bloque A)**: las fichas admiten el estado «retirada» cuando el Documentador las retire por la revisión de conjunto (9.9 de su prompt): redundancia funcional frente a una fuente vigente de calidad o acceso no inferior, sustitución por una versión o edición superior ya registrada, o bajo aporte mantenido. La retirada es siempre lógica y trazable: entrada nueva con fecha y motivo en el historial (4.6); la ficha permanece en el archivo como evidencia, deja de alimentar el índice (4.1) y las respuestas a peticiones, y nunca se borra físicamente ni se renumeran identificadores.

## 4. Estructura del archivo

El archivo se compone de seis secciones, en este orden. La carga de arranque del operador (25/10/2026) rellena las secciones 4.1, 4.2, 4.3 y 4.6; los registros de servicios (4.4) y de mantenimiento (4.5) se abren con la primera operación del Documentador para el Motor.

**Nota sobre la carga de arranque.** Las fichas siguientes se dispusieron a partir de citas verificadas el 25/10/2026 en fuentes bibliográficas públicas (DOI resolutivos, repositorios académicos y páginas editoriales). Ningún dato se ha inventado: donde un dato no se consultó, el campo lo declara. Las obras clásicas de acceso por suscripción quedan honestamente anotadas como «pendiente de acceso gratuito» (peldaño 5 de la escalera, 6.5 del prompt): el formato se muestra igualmente completo y el acceso se resolverá en operación.

### 4.1 Índice temático y mapa de coberturas

| Campo | Valor |
|---|---|
| Versión del esquema | 1.0 |
| Fichas por estado | 4 aprobadas · 9 pendientes de acceso gratuito · 0 en revisión |
| Fichas por área matemática | Valoración de derivados y procesos estocásticos (5) · Optimización y álgebra lineal numérica (2) · Análisis numérico y estabilidad (3) · Simulación estocástica (1) · Reproducibilidad computacional (1) · Referencia matemática continua (1) |
| Métodos del Motor cubiertos | Valoración cerrada y en árbol (buena) · Monte Carlo y least-squares (buena) · Optimización de carteras (parcial: solo base clásica) · Estabilidad y álgebra lineal numérica (parcial: bases sin texto aún accesible) · Volatilidad y saltos (parcial) · Reproducibilidad (buena) |
| Última regeneración del índice | 2026-10-25 (carga de arranque) |
| Pendientes declarados | Resolver el acceso legal gratuito de las 9 fichas pendientes (peldaños 1-4); completar el ISBN de DOC-MOT-0009 y los DOI no consultados |

### 4.2 Fichas de fuente matemática (sección principal)

Una ficha por fuente (campos del Anexo D del prompt del Documentador para el Motor de Cálculo Avanzado, 9.2), dispuesta en formato compacto (convención 8): un bloque de párrafos por ficha con los campos etiquetados en negrita.

#### DOC-MOT-0001 — Black y Scholes (1973)

*Identificación y cita.* **source_id:** DOC-MOT-0001 · **Título:** The Pricing of Options and Corporate Liabilities · **Autores:** Fischer Black; Myron Scholes · **Publicación o institución:** The Journal of Political Economy, vol. 81, n.º 3, págs. 637-654 (University of Chicago Press) · **Año:** 1973 · **Tipo de documento:** Artículo revisado por pares · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** DOI: 10.1086/260062 (journals.uchicago.edu) · **Peldaño de la escalera de acceso:** Peldaño 5 (resumen visible en la editorial; texto completo por suscripción) — pendiente de acceso gratuito · **Licencia y restricciones:** Copyright University of Chicago Press · **Versión del documento y su relación:** Publicada; circulan copias docentes de la misma versión en páginas universitarias (verificar legalidad de cada copia antes de usarla como texto de trabajo)

*Clasificación y estado.* **Área matemática:** Valoración de derivados; cálculo estocástico · **Etiquetas:** opciones; valoracion-cerrada; sin-arbitraje · **Estado:** Pendiente de acceso gratuito · **Fecha de registro:** 2026-10-25 · **request_id y run_id de origen:** Carga de arranque del operador (25/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Deriva la ecuación de valoración de una opción europea en el marco de la cartera autofinanciada sin arbitraje y obtiene la fórmula cerrada de Black-Scholes bajo volatilidad constante, sin dividendos y tipos sin riesgo constantes. · **Estatus epistémico:** Resultado clásico revisado por pares; fundamento teórico de la valoración moderna · **Métodos del Motor que respalda:** Valoración cerrada de opciones europeas; base teórica de toda familia de precios de derivados

*Verificación y calidad.* **Resultado del filtro de verificación:** Ligera (carga de arranque): cita, DOI y paginación verificadas el 25/10/2026; texto completo no obtenido (peldaño 5); comprobaciones omitidas: análisis del contenido completo · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Limitaciones:** Supuestos estrictos (volatilidad y tipos constantes, sin costes de transacción); no cubre ejercicio americano sin extensiones


#### DOC-MOT-0002 — Cox, Ross y Rubinstein (1979)

*Identificación y cita.* **source_id:** DOC-MOT-0002 · **Título:** Option Pricing: A Simplified Approach · **Autores:** John C. Cox; Stephen A. Ross; Mark Rubinstein · **Publicación o institución:** Journal of Financial Economics, vol. 7, n.º 3, págs. 229-263 (Elsevier) · **Año:** 1979 · **Tipo de documento:** Artículo revisado por pares · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** DOI: 10.1016/0304-405X(79)90015-1 · Copia de acceso gratuito verificada: página institucional de la Università del Salento (unisalento.it, «Option Pricing - A Simplified Approach») · **Peldaño de la escalera de acceso:** Peldaño 3 (versión de autor localizable legalmente en página universitaria) · **Licencia y restricciones:** Copyright Elsevier; la copia universitaria se cita como acceso de lectura · **Versión del documento y su relación:** Publicada; circuló antes como documento de trabajo de los autores (más extenso); la versión de revista es la de referencia

*Clasificación y estado.* **Área matemática:** Valoración de derivados; métodos en diferencias discretas · **Etiquetas:** binomial; crr; opciones-americanas · **Estado:** Aprobada · **Fecha de registro:** 2026-10-25 · **request_id y run_id de origen:** Carga de arranque del operador (25/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Formula el modelo binomial CRR: árbol recombinate con probabilidades neutrales al riesgo, convergencia a la fórmula de Black-Scholes y tratamiento natural de la valoración americana por retro-inducción. · **Estatus epistémico:** Resultado clásico revisado por pares · **Métodos del Motor que respalda:** Valoración binomial (SYNC); valoración americana discreta; convergencia de métodos discretos

*Verificación y calidad.* **Resultado del filtro de verificación:** Completa (carga de arranque): cita, DOI y copia de acceso verificadas el 25/10/2026; comprobaciones omitidas: lectura del texto completo por el Documentador, pendiente de la primera revisión · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Limitaciones:** Discretización; sensibilidad numérica del árbol para pasos bajos; convergencia no uniforme en puntos concretos


#### DOC-MOT-0003 — Markowitz (1952)

*Identificación y cita.* **source_id:** DOC-MOT-0003 · **Título:** Portfolio Selection · **Autores:** Harry M. Markowitz · **Publicación o institución:** The Journal of Finance, vol. 7, n.º 1, págs. 77-91 (Wiley; JSTOR 2975974) · **Año:** 1952 · **Tipo de documento:** Artículo revisado por pares · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** DOI: 10.1111/j.1540-6261.1952.tb01525.x · JSTOR: jstor.org/stable/2975974 (acceso por suscripción) · **Peldaño de la escalera de acceso:** Peldaño 5 (resumen visible en editorial; texto completo tras muro de pago) — pendiente de acceso gratuito · **Licencia y restricciones:** Copyright American Finance Association/Wiley · **Versión del documento y su relación:** Publicada

*Clasificación y estado.* **Área matemática:** Optimización; teoría de carteras · **Etiquetas:** media-varianza; optimizacion; carteras · **Estado:** Pendiente de acceso gratuito · **Fecha de registro:** 2026-10-25 · **request_id y run_id de origen:** Carga de arranque del operador (25/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Formula la selección de carteras como problema de optimización media-varianza: la frontera eficiente como combinación de esperanza y covarianza de rendimientos, con la diversificación como principio cuantitativo. · **Estatus epistémico:** Resultado fundacional revisado por pares · **Métodos del Motor que respalda:** Optimización media-varianza; construcción de carteras eficientes (SYNC)

*Verificación y calidad.* **Resultado del filtro de verificación:** Ligera (carga de arranque): cita, DOI y JSTOR verificados el 25/10/2026; texto completo no obtenido (peldaño 5); comprobaciones omitidas: análisis del contenido completo · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Limitaciones:** Media-varianza con parámetros estimados; sensibilidad a errores de estimación; extensiones modernas no cubiertas por el artículo original


#### DOC-MOT-0004 — Heston (1993)

*Identificación y cita.* **source_id:** DOC-MOT-0004 · **Título:** A Closed-Form Solution for Options with Stochastic Volatility with Applications to Bond and Currency Options · **Autores:** Steven L. Heston · **Publicación o institución:** The Review of Financial Studies, vol. 6, n.º 2, págs. 327-343 (Oxford University Press) · **Año:** 1993 · **Tipo de documento:** Artículo revisado por pares · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** DOI: 10.1093/rfs/6.2.327 (academic.oup.com) · **Peldaño de la escalera de acceso:** Peldaño 5 (resumen visible en editorial; texto completo por suscripción) — pendiente de acceso gratuito · **Licencia y restricciones:** Copyright Oxford University Press · **Versión del documento y su relación:** Publicada

*Clasificación y estado.* **Área matemática:** Valoración de derivados; volatilidad estocástica · **Etiquetas:** volatilidad-estocastica; heston; transformadas · **Estado:** Pendiente de acceso gratuito · **Fecha de registro:** 2026-10-25 · **request_id y run_id de origen:** Carga de arranque del operador (25/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Deriva una solución en forma cerrada (mediante transformadas características) para opciones europeas con volatilidad estocástica de media reversión y correlación con el subyacente, aplicable a opciones de bonos y divisas. · **Estatus epistémico:** Resultado clásico revisado por pares · **Métodos del Motor que respalda:** Valoración con volatilidad estocástica (integración numérica de transformadas); superficies de volatilidad

*Verificación y calidad.* **Resultado del filtro de verificación:** Ligera (carga de arranque): cita, DOI y paginación verificadas el 25/10/2026; texto completo no obtenido (peldaño 5); comprobaciones omitidas: análisis del contenido completo · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Limitaciones:** Integración numérica sensible a parámetros; calibración no incluida en el artículo original


#### DOC-MOT-0005 — Longstaff y Schwartz (2001)

*Identificación y cita.* **source_id:** DOC-MOT-0005 · **Título:** Valuing American Options by Simulation: A Simple Least-Squares Approach · **Autores:** Francis A. Longstaff; Eduardo S. Schwartz · **Publicación o institución:** The Review of Financial Studies, vol. 14, n.º 1, págs. 113-147 (Oxford University Press) · **Año:** 2001 · **Tipo de documento:** Artículo revisado por pares · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** DOI: 10.1093/rfs/14.1.113 · Versión de acceso gratuito verificada: eScholarship (University of California), escholarship.org/uc/item/43n1k4jb · **Peldaño de la escalera de acceso:** Peldaño 2 (versión en repositorio institucional abierto) · **Licencia y restricciones:** Copyright Oxford University Press; la copia eScholarship se cita como acceso de lectura · **Versión del documento y su relación:** Publicada; coexiste la versión depositada en eScholarship de contenido equivalente

*Clasificación y estado.* **Área matemática:** Simulación estocástica; valoración americana · **Etiquetas:** monte-carlo; lsm; opciones-americanas · **Estado:** Aprobada · **Fecha de registro:** 2026-10-25 · **request_id y run_id de origen:** Carga de arranque del operador (25/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Propone el algoritmo de Monte Carlo con mínimos cuadrados (LSM): condiciona la decisión de ejercicio americano a una regresión de la continuación sobre las variables de estado, con convergencia y ejemplos numéricos. · **Estatus epistémico:** Resultado clásico revisado por pares, estándar de facto en valoración americana por simulación · **Métodos del Motor que respalda:** Monte Carlo con regresión de continuación (ASYNC); valoración americana por simulación

*Verificación y calidad.* **Resultado del filtro de verificación:** Completa (carga de arranque): cita, DOI y copia eScholarship verificadas el 25/10/2026; comprobaciones omitidas: lectura del texto completo por el Documentador, pendiente de la primera revisión · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Limitaciones:** Sesgo de regresión con bases elegidas mal; requiere control de error de Monte Carlo; no cubre todo tipo de opciones exóticas sin extensiones


#### DOC-MOT-0006 — Glasserman (2003)

*Identificación y cita.* **source_id:** DOC-MOT-0006 · **Título:** Monte Carlo Methods in Financial Engineering · **Autores:** Paul Glasserman · **Publicación o institución:** Springer (colección Stochastic Modelling and Applied Probability, vol. 53) · **Año:** 2003 · **Tipo de documento:** Libro académico · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** DOI del libro: no consultado en la carga de arranque · Localización: Springer (link.springer.com, acceso por suscripción) · **Peldaño de la escalera de acceso:** Peldaño 5 (resumen y tabla de contenidos visibles en la editorial; sin texto completo gratuito legal identificado) — pendiente de acceso gratuito · **Licencia y restricciones:** Copyright Springer · **Versión del documento y su relación:** Primera edición; reimpresiones posteriores sin cambio material conocido

*Clasificación y estado.* **Área matemática:** Simulación estocástica; ingeniería financiera · **Etiquetas:** monte-carlo; simulacion; referencia · **Estado:** Pendiente de acceso gratuito · **Fecha de registro:** 2026-10-25 · **request_id y run_id de origen:** Carga de arranque del operador (25/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Tratamiento sistemático de Monte Carlo en finanzas: generación de caminos, varianzas de control, variables antitéticas y estratificación, cálculo de sensibilidades, y estimación de errores. Es la referencia de rigor para cualquier servicio de simulación del Motor. · **Estatus epistémico:** Monografía de referencia académica; nivel alto · **Métodos del Motor que respalda:** Servicios de simulación Monte Carlo (SYNC/ASYNC); control de error y varianza

*Verificación y calidad.* **Resultado del filtro de verificación:** Ligera (carga de arranque): cita y existencia editorial verificadas el 25/10/2026; texto completo no obtenido (peldaño 5); comprobaciones omitidas: análisis del contenido completo · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Limitaciones:** Antecede a los métodos más recientes de redes y aprendizaje; complementar con literatura posterior si el servicio lo exige


#### DOC-MOT-0007 — Golub y Van Loan (2013)

*Identificación y cita.* **source_id:** DOC-MOT-0007 · **Título:** Matrix Computations · **Autores:** Gene H. Golub; Charles F. Van Loan · **Publicación o institución:** Johns Hopkins University Press · **Año:** 2013 · **Tipo de documento:** Libro académico · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** Sin DOI de uso común para el libro completo · Localización: editorial JHU Press (sin texto completo gratuito legal identificado) · **Peldaño de la escalera de acceso:** Peldaño 5 (descripción editorial visible; sin texto completo gratuito legal) — pendiente de acceso gratuito · **Licencia y restricciones:** Copyright Johns Hopkins University Press · **Versión del documento y su relación:** Cuarta edición; ediciones anteriores con diferencias de contenido material

*Clasificación y estado.* **Área matemática:** Álgebra lineal numérica · **Etiquetas:** algebra-lineal; svd; minimos-cuadrados · **Estado:** Pendiente de acceso gratuito · **Fecha de registro:** 2026-10-25 · **request_id y run_id de origen:** Carga de arranque del operador (25/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Tratamiento canónico de descomposiciones matriciales (LU, QR, SVD), resolución de sistemas, mínimos cuadrados y problemas de valores propios, con análisis de estabilidad y coste. Base de cualquier cálculo matricial reproducible del Motor. · **Estatus epistémico:** Monografía de referencia académica; nivel alto · **Métodos del Motor que respalda:** Descomposiciones SVD/QR; mínimos cuadrados (incluido el paso de regresión de LSM); problemas de valores propios

*Verificación y calidad.* **Resultado del filtro de verificación:** Ligera (carga de arranque): cita y edición verificadas el 25/10/2026; texto completo no obtenido (peldaño 5); comprobaciones omitidas: análisis del contenido completo · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Limitaciones:** Edición concreta a fijar como referencia; el registro de versiones aplicará la que use el Motor en cada servicio


#### DOC-MOT-0008 — Higham (2002)

*Identificación y cita.* **source_id:** DOC-MOT-0008 · **Título:** Accuracy and Stability of Numerical Algorithms · **Autores:** Nicholas J. Higham · **Publicación o institución:** Society for Industrial and Applied Mathematics (SIAM) · **Año:** 2002 · **Tipo de documento:** Libro académico · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** DOI del libro: no consultado en la carga de arranque · Localización: SIAM Bookstore (epubs.siam.org, acceso por suscripción) · **Peldaño de la escalera de acceso:** Peldaño 5 (descripción editorial visible; sin texto completo gratuito legal identificado) — pendiente de acceso gratuito · **Licencia y restricciones:** Copyright SIAM · **Versión del documento y su relación:** Segunda edición; la primera (1996) con diferencias de contenido material

*Clasificación y estado.* **Área matemática:** Análisis numérico y estabilidad · **Etiquetas:** estabilidad-numerica; error-redondeo; referencia · **Estado:** Pendiente de acceso gratuito · **Fecha de registro:** 2026-10-25 · **request_id y run_id de origen:** Carga de arranque del operador (25/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Tratamiento de referencia del error de redondeo, la estabilidad backward y el comportamiento de los algoritmos numéricos en aritmética de precisión finita. Fundamenta las declaraciones de limitaciones numéricas que el Motor anota en cada resultado. · **Estatus epistémico:** Monografía de referencia académica; nivel alto · **Métodos del Motor que respalda:** Análisis de error y estabilidad de los servicios de cálculo; justificación de las limitaciones declaradas en los resultados

*Verificación y calidad.* **Resultado del filtro de verificación:** Ligera (carga de arranque): cita y edición verificadas el 25/10/2026; texto completo no obtenido (peldaño 5); comprobaciones omitidas: análisis del contenido completo · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Limitaciones:** Edición concreta a fijar como referencia; trata algoritmos, no implementaciones concretas


#### DOC-MOT-0009 — Press, Teukolsky, Vetterling y Flannery (2007)

*Identificación y cita.* **source_id:** DOC-MOT-0009 · **Título:** Numerical Recipes: The Art of Scientific Computing · **Autores:** William H. Press; Saul A. Teukolsky; William T. Vetterling; Brian P. Flannery · **Publicación o institución:** Cambridge University Press · **Año:** 2007 · **Tipo de documento:** Libro académico · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** ISBN: no consultado en la carga de arranque · Localización: Cambridge University Press (sin texto completo gratuito legal de la tercera edición; el código de ejemplo histórico está disponible en nr.com) · **Peldaño de la escalera de acceso:** Peldaño 5 (descripción editorial visible; sin texto completo gratuito legal de la edición de referencia) — pendiente de acceso gratuito · **Licencia y restricciones:** Copyright Cambridge University Press; el código tiene licencia propia distinta del texto · **Versión del documento y su relación:** Tercera edición; ediciones anteriores (Fortran/C) con diferencias materiales; separar siempre texto y código en las citas

*Clasificación y estado.* **Área matemática:** Análisis numérico; algoritmos científicos · **Etiquetas:** algoritmos-numericos; referencia-practica · **Estado:** Pendiente de acceso gratuito · **Fecha de registro:** 2026-10-25 · **request_id y run_id de origen:** Carga de arranque del operador (25/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Enciclopedia práctica de algoritmos numéricos con discusión de criterios de elección, errores y alternativas. Útil como compendio de segundo nivel cuando el Motor necesite justificar la elección de una rutina estándar. · **Estatus epistémico:** Obra de referencia académico-profesional; nivel medio-alto · **Métodos del Motor que respalda:** Selección y justificación de rutinas numéricas estándar (interpolación, integración, raíces, optimización)

*Verificación y calidad.* **Resultado del filtro de verificación:** Ligera (carga de arranque): cita y edición verificadas el 25/10/2026; ISBN no consultado; texto completo no obtenido (peldaño 5); comprobaciones omitidas: ISBN, análisis del contenido completo · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Limitaciones:** Cobertura enciclopédica pero no exhaustiva en finanzas; licencia del código restrictiva


#### DOC-MOT-0010 — Cont y Tankov (2004)

*Identificación y cita.* **source_id:** DOC-MOT-0010 · **Título:** Financial Modelling with Jump Processes · **Autores:** Rama Cont; Peter Tankov · **Publicación o institución:** Chapman and Hall / CRC Press · **Año:** 2004 · **Tipo de documento:** Libro académico · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** Sin DOI de uso común para el libro completo · Localización: CRC Press (sin texto completo gratuito legal identificado) · **Peldaño de la escalera de acceso:** Peldaño 5 (descripción editorial visible; sin texto completo gratuito legal) — pendiente de acceso gratuito · **Licencia y restricciones:** Copyright CRC Press · **Versión del documento y su relación:** Primera edición; reimpresiones sin cambio material conocido

*Clasificación y estado.* **Área matemática:** Procesos estocásticos con saltos · **Etiquetas:** saltos; levy; simulacion · **Estado:** Pendiente de acceso gratuito · **Fecha de registro:** 2026-10-25 · **request_id y run_id de origen:** Carga de arranque del operador (25/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Teoría y simulación de procesos de Lévy y saltos con aplicación a la valoración de opciones: construcción de modelos con saltos, medidas equivalentes y métodos numéricos asociados. Base de los servicios de cálculo con dinámicas discontinuas. · **Estatus epistémico:** Monografía de referencia académica; nivel alto · **Métodos del Motor que respalda:** Modelos con saltos; simulación de trayectorias discontinuas; valoración en modelos de Lévy

*Verificación y calidad.* **Resultado del filtro de verificación:** Ligera (carga de arranque): cita y existencia editorial verificadas el 25/10/2026; texto completo no obtenido (peldaño 5); comprobaciones omitidas: análisis del contenido completo · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Limitaciones:** Requiere base teórica sólida de procesos estocásticos; calibración práctica limitada en el libro


#### DOC-MOT-0011 — Gatheral (2006)

*Identificación y cita.* **source_id:** DOC-MOT-0011 · **Título:** The Volatility Surface: A Practitioner's Guide · **Autores:** Jim Gatheral · **Publicación o institución:** John Wiley and Sons (Wiley Finance) · **Año:** 2006 · **Tipo de documento:** Libro académico-profesional · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** Sin DOI de uso común para el libro completo · Localización: Wiley (sin texto completo gratuito legal identificado) · **Peldaño de la escalera de acceso:** Peldaño 5 (descripción editorial visible; sin texto completo gratuito legal) — pendiente de acceso gratuito · **Licencia y restricciones:** Copyright Wiley · **Versión del documento y su relación:** Primera edición; reimpresiones sin cambio material conocido

*Clasificación y estado.* **Área matemática:** Volatilidad; valoración de derivados · **Etiquetas:** volatilidad; superficie; calibracion · **Estado:** Pendiente de acceso gratuito · **Fecha de registro:** 2026-10-25 · **request_id y run_id de origen:** Carga de arranque del operador (25/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Guía práctica de la superficie de volatilidad: asas de la sonrisa, modelos estocásticos y locales, y calibración. Referencia del vocabulario y de los criterios de calibración que los resultados del Motor deben declarar. · **Estatus epistémico:** Monografía de referencia profesional con aparato académico; nivel medio-alto · **Métodos del Motor que respalda:** Servicios con superficies de volatilidad; calibración de modelos de volatilidad

*Verificación y calidad.* **Resultado del filtro de verificación:** Ligera (carga de arranque): cita y existencia editorial verificadas el 25/10/2026; texto completo no obtenido (peldaño 5); comprobaciones omitidas: análisis del contenido completo · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Limitaciones:** Orientado a práctica de opciones; verificar modelos más recientes antes de servicios con datos actuales


#### DOC-MOT-0012 — Sandve et al. (2013)

*Identificación y cita.* **source_id:** DOC-MOT-0012 · **Título:** Ten Simple Rules for Reproducible Computational Research · **Autores:** Geir Kjetil Sandve; Anton Nekrutenko; James Taylor; Eivind Hovig · **Publicación o institución:** PLoS Computational Biology, vol. 9, n.º 10, e1003285 (Public Library of Science) · **Año:** 2013 · **Tipo de documento:** Artículo revisado por pares (guía) · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** DOI: 10.1371/journal.pcbi.1003285 · Acceso abierto en la editorial (journals.plos.org) · **Peldaño de la escalera de acceso:** Peldaño 1 (acceso abierto en la editorial) · **Licencia y restricciones:** Creative Commons (acceso abierto PLoS); verificar la variante CC exacta de la pieza · **Versión del documento y su relación:** Publicada (v1 en PLoS)

*Clasificación y estado.* **Área matemática:** Reproducibilidad computacional · **Etiquetas:** reproducibilidad; trazabilidad; ct-12 · **Estado:** Aprobada · **Fecha de registro:** 2026-10-25 · **request_id y run_id de origen:** Carga de arranque del operador (25/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Diez reglas operativas de reproducibilidad computacional: versionar todo, anotar el entorno, no sobrescribir resultados, externalizar datos y scripts. Son las reglas que sustentan la exigencia del Motor de devolver resultado, artefacto y limitaciones reproducibles en cada servicio CT-11. · **Estatus epistémico:** Guía revisada por pares; nivel alto para el propósito de trazabilidad · **Métodos del Motor que respalda:** Reproducibilidad de los servicios (calculation_log, artefactos); base de la re-ejecución independiente (CT-12)

*Verificación y calidad.* **Resultado del filtro de verificación:** Completa (carga de arranque): cita, DOI y acceso abierto verificados el 25/10/2026; comprobaciones omitidas: lectura del texto completo por el Documentador, pendiente de la primera revisión · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Limitaciones:** Reglas generales de reproducibilidad, no específicas de finanzas


#### DOC-MOT-0013 — NIST DLMF (Digital Library of Mathematical Functions)

*Identificación y cita.* **source_id:** DOC-MOT-0013 · **Título:** NIST Digital Library of Mathematical Functions (edición electrónica del NIST Handbook of Mathematical Functions) · **Autores:** Daniel W. Lozier y colaboradores (ed. general: Frank W. J. Olver et al.) · **Publicación o institución:** National Institute of Standards and Technology (NIST); edición impresa: Cambridge University Press · **Año:** Edición en línea continua (lanzamiento 2010; fecha de la versión consultada en cada uso) · **Tipo de documento:** Referencia matemática institucional (biblioteca digital) · **Idioma:** Inglés

*Acceso.* **DOI o identificador persistente y URL de acceso:** Portal: dlmf.nist.gov (acceso gratuito oficial) · Edición impresa: ISBN no consultado en la carga de arranque · **Peldaño de la escalera de acceso:** Peldaño 1 (recurso oficial de acceso abierto del NIST) · **Licencia y restricciones:** Dominio público estadounidense (obras del gobierno federal); citar sección y versión/fecha de la entrada · **Versión del documento y su relación:** Edición en línea actualizada continuamente: registrar la fecha de versión consultada en cada uso

*Clasificación y estado.* **Área matemática:** Funciones especiales y matemática de referencia · **Etiquetas:** funciones-especiales; referencia; nist · **Estado:** Aprobada · **Fecha de registro:** 2026-10-25 · **request_id y run_id de origen:** Carga de arranque del operador (25/10/2026): sin request_id ni run_id; origen OPERATOR

*Contenido y uso.* **Descripción del contenido pertinente:** Referencia canónica de funciones especiales (gamma, Bessel, hipergeométricas, funciones de error), con definiciones, propiedades, gráficos y referencias bibliográficas. Sustenta la definición precisa de las funciones matemáticas que los cálculos del Motor emplean. · **Estatus epistémico:** Referencia institucional de máxima autoridad en su ámbito · **Métodos del Motor que respalda:** Definiciones exactas de funciones especiales usadas en fórmulas cerradas y distribuciones estadísticas

*Verificación y calidad.* **Resultado del filtro de verificación:** Completa (carga de arranque): portal vivo y naturaleza del recurso verificadas el 25/10/2026; comprobaciones omitidas: ninguna declarada para el uso como referencia de definiciones · **Calidad por uso con su ámbito:** No aplicable (sin uso en operación) · **Limitaciones:** No trata modelización financiera: es referencia de funciones, no de métodos


### 4.3 Registro de versiones de documento

Una entrada por relación de versiones detectada (source_id; versiones existentes y su relación; diferencias materiales conocidas; versión recomendada de acceso gratuito; fecha de anotación; motivo).

| source_id | Versiones y relación | Diferencias materiales conocidas | Versión recomendada | Fecha | Motivo |
|---|---|---|---|---|---|
| DOC-MOT-0002 | Documento de trabajo (1976-1979) → publicada (JFE 1979) | El documento de trabajo es más extenso; la versión de revista es la referencia citada | Publicada, vía copia de acceso gratuito (peldaño 3) | 2026-10-25 | Carga de arranque |
| DOC-MOT-0005 | Publicada (RFS 2001) → copia depositada (eScholarship) | Contenido equivalente; la copia sirve de acceso gratuito | Copia eScholarship (peldaño 2) | 2026-10-25 | Carga de arranque |
| DOC-MOT-0007 | Primera edición (1996) → cuarta edición (2013) | Contenido materialmente distinto entre ediciones | Cuarta edición (la que registre el Motor por servicio) | 2026-10-25 | Carga de arranque |
| DOC-MOT-0009 | Ediciones anteriores (Fortran/C) → tercera edición (2007) | Cambios de capítulos y de código entre ediciones | Tercera edición | 2026-10-25 | Carga de arranque |
| DOC-MOT-0013 | Edición en línea (continua) → edición impresa del handbook | La versión en línea se actualiza continuamente | Edición en línea, con fecha de versión registrada por uso | 2026-10-25 | Carga de arranque |

### 4.4 Registro de servicios

Una fila por servicio del Documentador para el Motor. La carga de arranque del operador no es un servicio MDOC_REQUEST ni MDOC_MAINTENANCE y no se registra aquí; queda anotada en el historial (4.6). Columnas del registro: service_id; request_id; run_id; execution_mode (MDOC_REQUEST, MDOC_MAINTENANCE); origin (MOTOR, OPERATOR, SCHEDULER); started_at; completed_at; as_of; prompt_version; estrategia aplicada; canales consultados; cadenas aplicadas e iteraciones; fuentes entregadas, rechazadas y sin verificar; escrituras y su confirmación; lagunas; incidencias; estado final del servicio.

| service_id | request_id | run_id | execution_mode | origin | started_at | completed_at | Estado |
|---|---|---|---|---|---|---|---|
| (sin servicios registrados a la fecha de la carga de arranque) | — | — | — | — | — | — | — |

### 4.5 Registro de mantenimiento

El primer ciclo MDOC_MAINTENANCE lo ejecutará el Documentador para el Motor según el calendario que fije el operador (Anexo A). Columnas del registro: service_id; fecha; tipo de ciclo (enlaces, erratas, ediciones, índice); entradas revisadas; hallazgos (enlaces rotos, erratas, ediciones nuevas); correcciones o eliminaciones de enlaces con fecha y motivo; cambios de estado registrados; pendientes declarados.

| service_id | Fecha | Tipo de ciclo | Entradas revisadas | Hallazgos | Pendientes |
|---|---|---|---|---|---|
| (sin ciclos registrados a la fecha de la carga de arranque) | — | — | — | — | Resolver el acceso legal gratuito de las 9 fichas pendientes; completar ISBN/DOI no consultados |

### 4.6 Historial de altas y cambios de estado

Diario de solo añadir (fecha; `source_id` afectado; movimiento; agente responsable; motivo).

| Fecha | Ficha afectada | Movimiento | Agente responsable | Motivo |
|---|---|---|---|---|
| 2026-10-25 | DOC-MOT-0001 | Alta (pendiente de acceso gratuito) | Operador (carga de arranque) | Base teórica de valoración cerrada |
| 2026-10-25 | DOC-MOT-0002 | Alta | Operador (carga de arranque) | Valoración binomial; copia de acceso verificada |
| 2026-10-25 | DOC-MOT-0003 | Alta (pendiente de acceso gratuito) | Operador (carga de arranque) | Base de optimización media-varianza |
| 2026-10-25 | DOC-MOT-0004 | Alta (pendiente de acceso gratuito) | Operador (carga de arranque) | Volatilidad estocástica |
| 2026-10-25 | DOC-MOT-0005 | Alta | Operador (carga de arranque) | Monte Carlo least-squares; copia de acceso verificada |
| 2026-10-25 | DOC-MOT-0006 | Alta (pendiente de acceso gratuito) | Operador (carga de arranque) | Referencia de Monte Carlo |
| 2026-10-25 | DOC-MOT-0007 | Alta (pendiente de acceso gratuito) | Operador (carga de arranque) | Álgebra lineal numérica |
| 2026-10-25 | DOC-MOT-0008 | Alta (pendiente de acceso gratuito) | Operador (carga de arranque) | Estabilidad numérica |
| 2026-10-25 | DOC-MOT-0009 | Alta (pendiente de acceso gratuito) | Operador (carga de arranque) | Algoritmos numéricos de referencia |
| 2026-10-25 | DOC-MOT-0010 | Alta (pendiente de acceso gratuito) | Operador (carga de arranque) | Procesos con saltos |
| 2026-10-25 | DOC-MOT-0011 | Alta (pendiente de acceso gratuito) | Operador (carga de arranque) | Superficie de volatilidad |
| 2026-10-25 | DOC-MOT-0012 | Alta | Operador (carga de arranque) | Reproducibilidad; acceso abierto verificado |
| 2026-10-25 | DOC-MOT-0013 | Alta | Operador (carga de arranque) | Referencia de funciones especiales; acceso abierto verificado |
| 2026-10-25 | DOC-MOT-0002, 0005, 0007, 0009, 0013 | Registro de versiones de documento | Operador (carga de arranque) | Relaciones de versiones detectadas en la carga |

## 5. Qué se registra y qué no

Se registra conocimiento matemático aplicado que respalda métodos de cálculo: enunciados, métodos, condiciones y resultados con valor de referencia estable, obtenidos por acceso legal y gratuito y verificados académicamente. No se registra: contenido de tendencias o de dominio del análisis de inversiones (ámbito de la «Documentación para tendencias de inversión»); metodología de búsqueda bibliográfica (ámbito del «Fondo metodológico»); actas de ejecución del servicio (ámbito del «Registro de cálculos del Motor», gestionado por el propio Motor); recomendaciones, tesis de inversión o conclusiones de mercado, que no forman parte de la documentación matemática; y fuentes que no superen el filtro de verificación académica. Ante la duda, no se registra.

## 6. Reglas de mantenimiento y ciclo de vida

1. **Revisión de primera ejecución**: en su primera ejecución, el Documentador para el Motor revisa el archivo (enlaces vivos, acceso gratuito vigente, ISBN/DOI no consultados), clasifica y ordena las fuentes por utilidad para el Motor y declara el resultado de la revisión.
2. **Ciclo MDOC_MAINTENANCE** conforme al calendario que fije el operador (Anexo A): vitalidad de enlaces, erratas y ediciones nuevas; corrección o eliminación de enlaces rotos con anotación; revalidación de estados y de las 9 fichas pendientes de acceso gratuito.
3. **Reindexado** del índice temático y del mapa de coberturas tras cada incorporación relevante y en el ciclo programado; el índice queda siempre en el estado que refleja la última petición atendida.
4. **Vigilancia de versiones**: cuando se detecte una versión posterior que corrija o contradiga materialmente a una fuente registrada, se anota mediante entrada nueva y se recomienda la versión de referencia, sin borrar la entrada original.
5. **Consulta ecosistémica**: las consultas de los agentes de bloques posteriores que reconstruyan servicios del Motor se resuelven por acceso a archivo conforme a los protocolos de cada bloque; sus propuestas de nuevas entradas llegan como material de trabajo y solo el Documentador para el Motor las eleva a registro conforme a la sección 3.
6. **Degradación honesta**: si el mantenimiento no puede completarse por limitación del entorno, se declara la limitación y el servicio continúa con ella anotada.

## 7. Control de versiones del archivo


| Versión | Fecha | Cambio |

|---|---|---|

| 1.0 | 2026-10-25 | Primera emisión como plantilla de formato, vacía de contenido y de fuentes. |

| 2.0 | 2026-10-25 | Conversión a archivo operativo: carga de arranque con 13 fuentes reales verificadas dispuesta por el operador; prefijo de identificador DOC-MOT- fijado; alcance ecosistémico declarado (archivo único de la documentación del Motor para todos los bloques). |
| 2.1 | 2026-10-25 | Anexo documental del operador: añadida la sección 8 «Fuentes fiables específicas de este archivo», con el canal de verificación y acceso por ficha (8.1) y los canales institucionales (8.2); identificadores verificados hoy para las fichas 0006, 0007, 0008, 0009, 0010, 0011 y 0013. No altera el esquema 1.0 ni los datos de las fichas. |

| 2.2 | 2026-10-26 | Cambio de disposición de las fichas por disposición del operador: las 13 fichas pasan de la tabla vertical de campos al formato compacto de bloques de párrafos con campos etiquetados en negrita (convención 8), para contener la extensión y el peso del documento .docx ante nuevas altas. No altera el esquema 1.0: el conjunto de campos y los valores de cada ficha se conservan íntegros (conversión verificada campo a campo). |

| 2.3 | 2026-10-26 | Adenda V1.2 del Bloque A (aprobada por el operador y aplicada por paquete coordinado conforme al Documento 0, 5.3): las fichas admiten el estado «retirada» (convención 9) para la retirada lógica de fuentes por revisión de conjunto del Documentador (9.9 de su prompt); la retirada es siempre un cambio de estado trazable (entrada nueva con fecha y motivo en 4.6) y nunca un borrado físico ni una renumeración. No altera el esquema 1.0 ni los datos de las fichas. |
## 8. Fuentes fiables específicas de este archivo

*(Anexo documental del operador, 25/10/2026.)* Este apartado reúne, para cada ficha del archivo, las fuentes fiables concretas donde se verifica la cita y se consulta el documento registrado. No sustituye al campo «DOI o identificador persistente y URL de acceso» de cada ficha: lo complementa como canal de verificación y acceso. Todos los enlaces listados se comprobaron el 25/10/2026. Los identificadores que las fichas declaran «no consultado en la carga de arranque» quedan aquí verificados por el operador para que el Documentador para el Motor los absorba en su primera revisión; las ediciones que impliquen tocar una ficha exigen entrada nueva en el historial (4.6). En los ciclos MDOC_MAINTENANCE, estos enlaces se revisan igual que los de las fichas.

### 8.1 Fuentes de verificación por ficha

| Ficha | Fuentes fiables específicas | Qué se verifica ahí |
|---|---|---|
| DOC-MOT-0001 — Black y Scholes (1973) | DOI: doi.org/10.1086/260062 (The Journal of Political Economy, journals.uchicago.edu, ficha) · Agregadores: IDEAS/RePEc y Google Scholar para versiones de trabajo citables | Cita, DOI y localización editorial; pendiente de acceso gratuito sin resolver |
| DOC-MOT-0002 — Cox, Ross y Rubinstein (1979) | DOI: doi.org/10.1016/0304-405X(79)90015-1 (ScienceDirect, re-verificado) · Copia de acceso gratuito (ficha): página institucional de la Università del Salento (unisalento.it) | Cita, DOI y copia institucional abierta |
| DOC-MOT-0003 — Markowitz (1952) | DOI: doi.org/10.1111/j.1540-6261.1952.tb01525.x (Wiley, ficha) · JSTOR: jstor.org/stable/2975974 (ficha, acceso por suscripción) | Cita, DOI y localización; pendiente de acceso gratuito sin resolver |
| DOC-MOT-0004 — Heston (1993) | DOI: doi.org/10.1093/rfs/6.2.327 (The Review of Financial Studies, academic.oup.com, ficha) | Cita y DOI en la editorial |
| DOC-MOT-0005 — Longstaff y Schwartz (2001) | DOI: doi.org/10.1093/rfs/14.1.113 (Oxford University Press, ficha) · Copia de acceso gratuito (ficha): eScholarship, escholarship.org/uc/item/43n1k4jb | Cita, DOI y versión de autor en repositorio universitario |
| DOC-MOT-0006 — Glasserman (2003) | **DOI del libro verificado hoy**: 10.1007/978-0-387-21617-1 · Página editorial: link.springer.com/book/10.1007/978-0-387-21617-1 (Springer, Stochastic Modelling and Applied Probability, vol. 53) | Existencia editorial, DOI del libro y metadatos de la colección; completar el campo de la ficha en la primera revisión |
| DOC-MOT-0007 — Golub y Van Loan (2013) | Editorial: press.jhu.edu/books/title/10678/matrix-computations (Johns Hopkins University Press) · **ISBN verificado hoy**: 978-1-4214-0794-4 · Edición electrónica SIAM: epubs.siam.org/doi/book/10.1137/1.9781421407944 | Existencia editorial, ISBN y localización del e-book institucional; completar la ficha en la primera revisión |
| DOC-MOT-0008 — Higham (2002) | SIAM Bookstore: epubs.siam.org/doi/book/10.1137/1.9780898718027 · **ISBN verificado hoy**: 978-0-89871-521-7 | DOI de la edición SIAM y ISBN; completar la ficha en la primera revisión |
| DOC-MOT-0009 — Press, Teukolsky, Vetterling y Flannery (2007) | Editorial: Cambridge University Press · **ISBN verificado hoy**: 978-0-521-88068-8 · Código de ejemplo histórico: nr.com (ficha) | Existencia editorial, ISBN y estado del código de ejemplo; completar la ficha en la primera revisión |
| DOC-MOT-0010 — Cont y Tankov (2004) | Editorial: routledge.com/Financial-Modelling-with-Jump-Processes/Cont-Tankov/p/book/9781584884132 (Routledge / Chapman & Hall-CRC) · **ISBN verificado hoy**: 978-1-58488-413-2 (impreso, ISBN-10 1-58488-413-4) | Existencia editorial e ISBN; completar la ficha en la primera revisión |
| DOC-MOT-0011 — Gatheral (2006) | Editorial: wiley.com (The Volatility Surface: A Practitioner's Guide, Wiley Finance) · **ISBN verificado hoy**: 978-0-471-79251-2 · DOI del e-book: 10.1002/9781119202073 | Existencia editorial, ISBN y DOI del e-book; completar la ficha en la primera revisión |
| DOC-MOT-0012 — Sandve et al. (2013) | DOI: doi.org/10.1371/journal.pcbi.1003285 · Acceso abierto en la editorial (journals.plos.org, ficha) | Cita, DOI y acceso abierto vigente |
| DOC-MOT-0013 — NIST DLMF | Portal oficial: dlmf.nist.gov (acceso gratuito, ficha) · **Edición impresa verificada hoy**: Olver, Lozier, Boisvert y Clark (eds.), NIST Handbook of Mathematical Functions, Cambridge University Press, 2010, ISBN 978-0-521-19225-5 | Portal, release vigente y edición impresa; citar siempre sección del DLMF y fecha de consulta (regla del estándar del propio NIST) |

### 8.2 Canales institucionales de verificación (todo el archivo)

| Canal | Uso en este archivo |
|---|---|
| doi.org (Crossref) | Resolver los DOI de artículos y de libros (Springer, SIAM, Wiley) listados en la tabla 8.1 |
| Portales editoriales primarios | journals.uchicago.edu, ScienceDirect, Wiley Online Library, academic.oup.com, link.springer.com, epubs.siam.org, cambridge.org, routledge.com: son las fuentes de máxima autoridad para citación, licencias y ediciones |
| IDEAS/RePEc y Google Scholar | Metadatos, versiones de trabajo citables y métricas de los artículos |
| OpenAlex | Metadatos abiertos y búsqueda de copias legales (método OA) para las fichas pendientes de acceso gratuito |
| NIST DLMF (dlmf.nist.gov) | Autoridad primaria en funciones especiales: la ficha DOC-MOT-0013 se consulta siempre en su versión vigente del portal |
| Retraction Watch Database (retractionwatch.com) | Comprobación de retractaciones en los ciclos MDOC_MAINTENANCE |
