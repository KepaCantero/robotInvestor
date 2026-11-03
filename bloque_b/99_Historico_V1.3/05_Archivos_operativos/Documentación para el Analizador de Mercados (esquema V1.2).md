# Documentación para el Analizador de Mercados

VERSIÓN V1.2 · Archivo operativo del Bloque B de la arquitectura Robot Investor · Fondo de fuentes académicas y técnicas de conocimiento del bloque (metodología de valoración, estructuras de mercado, literatura por familia) con fichas de verificación, cobertura por ámbitos e índice · Propietario de escritura y mantenimiento: Documentador para el Analizador de Mercados · Lectura: Analizador de Mercados (solo lectura) y Buscador de fuentes avanzadas para el Analizador de Mercados (solo lectura) · Nace con sus convenciones y taxonomía registradas y sin fichas: el «Fondo metodológico de búsqueda bibliográfica» compartido del ecosistema cubre la base metodológica común (decisión AM-6 y D8 del Anexo J del Documento 0 del Bloque B) · Gobernanza: «Documento 0 --- Protocolo maestro del Bloque B» (óptima V1.2, 31/10/2026); régimen operativo: system prompt del Documentador para el Analizador de Mercados (óptima V1.2) · Esquema ampliado por la «Adenda de arquitectura --- Bloque B» (V1.0, 30/10/2026): dos ámbitos nuevos de ficha (ficha de régimen y ficha de lección; D20, D23) · Esquema ampliado por la «Adenda de arquitectura --- Bloque B: Asimilación de la propuesta de mejoras y evolución arquitectónica» (V1.0, 31/10/2026): ámbito nuevo «caso de calibración» con el banco de casos del bloque (D34) y ficha de régimen ampliada con estado de confianza, naturaleza de las relaciones y criterio de transición (D27) · es-ES

## 1. Rol del archivo en la arquitectura del Bloque B

Este archivo es el fondo de conocimiento del bloque: las fichas metodológicas y de conocimiento que el Analizador de Mercados consulta por el lado petición del CT-B-04 cuando una dimensión o una familia exigen conocimiento registrado que no está en su prompt (su prompt codifica metodología; aquí se custodia el conocimiento factual-metodológico que las fuentes aportan). El Documentador de Mercados lo registra y mantiene; los agentes lectores lo consultan; el Auditor de Mercados recibe sus extractos por el circuito. Su diferencia con el «Fondo metodológico de búsqueda bibliográfica» compartido: aquel es el corpus académico de metodología de búsqueda común a todo el ecosistema (solo lectura para el bloque, referencia en lugar de duplicación); este es el fondo de conocimiento propio del Bloque B, con sus fichas verificadas y su taxonomía de familias.

El archivo nace deliberadamente sin fichas (2.3 del Documento 0): la base metodológica común está en el Fondo compartido y en las fichas de familia del prompt del Analizador (Anexo J de su prompt), y las fichas propias llegan por remisión (CT-B-04) o por curación documentada a medida que los ciclos las produzcan. Un archivo metodológico que nace lleno de fichas no verificadas es un vertedero; este nace vacío y crece con aporte marginal.

## 2. Ficha de uso para los agentes

**Analizador de Mercados (lectura, vía CT-B-04).** Pide por knowledge_need lo que su dimensión o familia exige y no está en su prompt (por ejemplo, la metodología de curvas para renta fija, o la ficha provisional de una familia provisional). Recibe fichas o referencias con relevancia y contenido pertinente, sin conclusiones de inversión.

**Buscador avanzado de Mercados (lectura).** Consulta el índice y las fichas para orientar qué tipo de fuente sostiene cada dimensión o familia (su Anexo B) y para conocer qué conocimiento ya está registrado.

**Documentador de Mercados (escritura y mantenimiento).** Alta de fichas por remisión (CT-B-04) o curación propia documentada, con aporte marginal, verificación y estados del ciclo de vida V1.2; índice y mapa de cobertura al día; mantenimiento híbrido D6.

**Auditor de Mercados (vía extractos CT-B-07).** No accede directamente: trabaja con los extractos que el Orquestador remita.

## 3. Convenciones de formato

1. **Identificadores únicos e inmutables** con prefijo `DM-B-` y cuatro dígitos (DM-B-0001, DM-B-0002…) para cada ficha. Sin renumeraciones.
2. **Fechado ISO 8601** en todos los campos de fecha.
3. **Registro de solo añadir**: los cambios de estado o de contenido son entradas nuevas con fecha y motivo; la retirada es lógica (la ficha permanece como evidencia).
4. **Estados del ciclo de vida (estándar V1.2)**: vigente · en revisión · retirada · provisional (fichas de familias provisionales por la regla de extensión AM-2, hasta su propuesta de tipo 3 al operador).
5. **Sin conclusiones de inversión**: las fichas organizan conocimiento metodológico y factual de fuentes verificadas; jamás ponderan atractivos, proponen tesis ni califican valores (regla crítica 4 del Documentador). Una ficha que opina se devuelve por el canal de origen.
6. **Referencia al Fondo compartido en lugar de duplicación**: cuando un conocimiento metodológico ya está en el «Fondo metodológico de búsqueda bibliográfica», la ficha lo referencia (con su localización) en lugar de replicarlo; la duplicación metodológica crea divergencias.
7. **Formato compacto de ficha**: bloque de párrafos con campos etiquetados en negrita, en la convención de formato del ecosistema (identificación · clasificación · contenido · verificación y ciclo de vida · trazabilidad).
8. **Campo no disponible se declara**: «desconocido», «no aplicable» o «pendiente de alta», nunca inventado.
9. **Esquema 1.0 del ecosistema**: el conjunto de campos es el del esquema compartido; este archivo solo fija la disposición y los estados propios del bloque.

## 4. Taxonomía registrada del bloque

La taxonomía de familias del Analizador de Mercados (decisión AM-2), registrada aquí como referencia del índice de ámbitos. Cada familia tiene su ficha metodológica como anexo del prompt del Analizador (Anexo J de su prompt, decisión AM-6): este archivo registra la taxonomía y acoge las fichas de conocimiento que los ciclos produzcan, no las fichas de familia del prompt. Un objeto no catalogado recibe familia provisional por la regla de extensión (AM-2): su ficha provisional se registra aquí marcada como provisional.

| # | Familia | Ámbitos de conocimiento típicos que este archivo puede acoger |
|---|---|---|
| 1 | Acciones (sociedad individual) | Valoración por descomposición de ingresos, estructuras de capital, filings y hechos corporativos, análisis de cadena de valor por sector |
| 2 | Índices y ETFs de acciones | Metodología de índices, comisión y réplica, tracking error, primas/descuentos de ETFs |
| 3 | Renta fija soberana | Curva de tipos, duración y convexidad, riesgo soberano, primas de riesgo país |
| 4 | Renta fija corporativa | Spreads de crédito, covenants, estructura de senioridad, métricas de default |
| 5 | Divisas | Paridades, diferenciales de tipos, flujos de balanza de pagos, intervenciones |
| 6 | Materias primas | Estructura de contango/backwardation, costes de carry, estacionalidad, cadenas de oferta física |
| 7 | Criptoactivos | Tokenomics, on-chain metrics, custodia y regulación, ciclos de halving |
| 8 | Inmobiliario | Cap rates, NOIs, métricas de REITs, ciclos de mercado inmobiliario |
| 9 | Fondos de inversión | Fee structures, alfas y betas, due diligence de gestoras, clases de participación |
| 10 | Derivados | Griegas y sensibilidades, volatilidad implícita, estructuras de payoff, margen y liquidación |
| 11 | Macro-país y mercados emergentes | Fundamentos macro por país, crisis de balanza de pagos, capitales oportunistas, ratings |
| — | Familia provisional (regla de extensión) | La que el objeto exija; ficha provisional registrada con estado «provisional» y propuesta de tipo 3 al operador |

## 5. Estructura del archivo

### 5.1 Índice de ámbitos

| Campo | Valor |
|---|---|
| Versión del esquema | 1.2 (adenda de arquitectura, 31/10/2026: ámbito «caso de calibración» y ficha de régimen ampliada; D27, D34. Antecedente 1.1: fichas de régimen y de lección, 30/10/2026) |
| Fichas registradas | 0 (nacimiento sin fichas: la base metodológica común vive en el Fondo compartido y en las fichas de familia del prompt del Analizador) |
| Taxonomía registrada | Once familias más la regla de extensión (sección 4) |
| Cobertura por ámbitos | Sin fichas propias aún; el índice se rellena con las primeras altas |
| Coberturas ausentes declaradas | Metodología de curvas de tipos (familias 3-4) prevista como primera alta probable por demanda de ciclo; metodología de curación de familia provisional (AM-2) prevista por la regla de extensión |
| Última revisión del índice | 2026-10-28 (nacimiento del archivo) |

### 5.2 Fichas (sección principal)

*(Sin fichas aún: el archivo nace vacío por diseño. Las fichas llegan por remisión del Analizador (CT-B-04) o por curación propia del Documentador documentada, siempre con aporte marginal declarado, verificación y estado del ciclo de vida.)*

Plantilla de ficha nueva (formato compacto):

> **Identificación.** **id de ficha:** DM-B-XXXX · **Título:** … · **Estado:** vigente · **Fecha de alta:** …
>
> **Clasificación.** **Familia o dimensiones que sirve:** … · **Ámbito del índice:** … · **Relación con el Fondo compartido:** referencia directa (localización) o sin equivalencia.
>
> **Contenido.** Resumen del conocimiento registrado, con su fuente verificada y su nivel (A/B/C); sin conclusiones de inversión.
>
> **Verificación y ciclo de vida.** **Fecha y método de verificación:** … · **Resultado:** … · **Historial de estados:** alta [fecha]; …
>
> **Trazabilidad.** **Origen:** remisión del Analizador (DOC-B con request_id y run_id) o curación propia (motivo) · **Vínculos:** ciclos que la usaron.

### 5.3 Registro de mantenimiento

Sección abierta con la primera operación de mantenimiento del Documentador de Mercados (revisión post-solicitud en 48 horas o mensual ligera).

*(Sin entradas aún.)*

### 5.4 Historial de altas y cambios de estado

| Fecha | Ficha | Evento | Detalle |
|---|---|---|---|
| 2026-10-28 | --- | Nacimiento del archivo | Convenciones y taxonomía registradas; sin fichas por diseño (la base común vive en el Fondo compartido y en el Anexo J del prompt del Analizador) |

## 6. Qué se registra y qué no

Se registran fichas de conocimiento metodológico y técnico con fuente verificada: metodologías de valoración y sus variantes por familia, estructuras de mercado y de cadena de valor, literatura de referencia aplicada a los instrumentos de la espina dorsal, y las fichas provisionales de la regla de extensión. Desde la V1.1 se registran además dos ámbitos nuevos (D20, D23): la **ficha de régimen** --- la evaluación de régimen de un ciclo (variables y estados observados con evidencia, variables dominantes para la tesis, relaciones apoyadas como estables; y, desde la V1.2 (D27), el estado de confianza del régimen (definido, mixto, incierto o en transición), la naturaleza declarada de cada relación (histórica observada o causal demostrada) y el criterio de transición de sus variables dominantes), reutilizable por los ciclos siguientes con re-verificación en primer uso y caducidad por la puerta de frescura; si el régimen cambió, la ficha nueva la sustituye con supersedes --- y la **ficha de lección** --- hallazgos recurrentes por foco y familia, métodos con mejor desempeño por contexto y decisiones metodológicas aprobadas o rechazadas con su evidencia; alimenta el apartado de lecciones del Orquestador y la memoria de decisiones del bloque (D20). Desde la V1.2 se registra el ámbito **caso de calibración** (D34): el expediente de un caso representativo del bloque (real anonimizado con anonimización completa y trazable, o ficticio declarado como tal) con su clase (una de las nueve: abundante información fiable; fuentes contradictorias; poca información; objeto híbrido o difícil de clasificar; cambio de régimen; hipótesis popular débil; riesgo de sesgo de supervivencia; análisis adicional que no cambia la conclusión; evidencia nueva que cambia materialmente el resultado), su situación y disponibilidad de datos, qué debería producir el bloque en ese caso (tipo de resultado y señales de calidad observables) y su evidencia; el conjunto de casos forma el banco de casos de calibración, consolidado en el mantenimiento mensual con su mapa de clases y usado en la calibración CT-B-11, en la priorización del muestreo post-entrega y en las evaluaciones comparativas de mejoras. Ninguno de estos ámbitos contiene conclusiones de inversión ni datos del inversor jamás. No se registran: conclusiones de inversión o valoraciones de atractivo (regla crítica 5 del Documentador), contenido que duplique al Fondo metodológico compartido (se referencia), metodología de búsqueda profesional (vive en el Fondo), ni conocimiento sin fuente verificada o sin aporte marginal declarado. La duda se resuelve no registrando y documentando la razón.

## 7. Reglas de mantenimiento y ciclo de vida

Mantenimiento híbrido (D6): revisión post-solicitud en 48 horas naturales desde la entrega autorizada (fichas del ciclo registradas, índice al día) y revisión mensual ligera en la primera semana natural del mes (aporte marginal, retirada lógica, mapa de cobertura, estados colgados). Las fichas «provisional» se revisan en cada ciclo que las use hasta su propuesta de tipo 3 al operador (regla de extensión, AM-2); las «en revisión» no sostienen conocimiento crítico hasta resolverse. Las fichas de régimen (V1.1) se re-verifican en primer uso cuando un ciclo las arrastra y caducan por la puerta de frescura del plan (D23); las fichas de lección se revisan en el mantenimiento mensual y su retirada sigue la regla general. Desde la V1.2, el mantenimiento mensual consolida además el banco de casos de calibración (D34): alta por anonimización documentada de los ciclos que sirvan como caso cuando su clase no esté cubierta, actualización del mapa de las nueve clases y remisión de los casos pertinentes en el paquete de servicio para la calibración y las comparativas. Reglas completas en las secciones 5, 8 y 12 del prompt del Documentador de Mercados.

## 8. Control de versiones del archivo

| Versión | Fecha | Cambios |
|---|---|---|
| V1.0 | 2026-10-28 | Nacimiento del archivo: convenciones propias del bloque (formato compacto, estados V1.2, identificadores DM-B), taxonomía de las once familias registrada como referencia del índice, plantilla de ficha y estructura completa. Sin fichas por diseño |
| V1.1 | 2026-10-30 | Esquema ampliado por la adenda de arquitectura (antes de la primera ficha): ámbitos nuevos «ficha de régimen» y «ficha de lección» (D20, D23), con sus reglas de ciclo de vida (re-verificación en primer uso, caducidad por frescura, sustitución con supersedes). El resto del esquema no cambia |
| V1.2 | 2026-10-31 | Esquema ampliado por la adenda de arquitectura V1.2 (antes de la primera ficha): ámbito nuevo «caso de calibración» con el banco de casos del bloque, sus nueve clases y su mapa de cobertura por clases (D34), y ficha de régimen ampliada con estado de confianza del régimen, naturaleza declarada de las relaciones y criterio de transición (D27); versión de esquema 1.2 en el índice de ámbitos. El resto del esquema no cambia |

## 9. Fuentes fiables específicas de este archivo

Para la verificación de las fichas metodológicas, el bloque parte de las fuentes registradas del «Registro de Fuentes Fiables para el Analizador de Mercados» (entrada RF-B-0008 a RF-B-0012 para la literatura académica) y del «Fondo metodológico de búsqueda bibliográfica» compartido para la metodología de búsqueda. La búsqueda de fuentes metodológicas nuevas para este archivo la ejecuta el Buscador avanzado de Mercados por petición del Analizador (CT-B-03) o la curación propia del Documentador documentada; el alta de fuentes metodológicas al Registro de Mercados sigue sus reglas ordinarias (aporte marginal, verificación, estados).
