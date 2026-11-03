# Registro de evidencia y afirmaciones (esquema V1.1) — Archivo F2

**Proyecto Robot Investor · Bloque A — Analizador de Tendencias de Inversión (módulo de curación)**

**Archivo operativo · Esquema V1.0 · 31/10/2026 · Propietario único de escritura: Analizador de Tendencias de Inversión, por su módulo de curación · Estado: operativo desde la publicación coordinada de la óptima V2.0 (31/10/2026)**

Archivo nuevo F2 creado por la óptima V2.0 del Bloque A. Se rige por el «Documento 0 — Protocolo maestro del Bloque A», versión óptima V2.0 (31/10/2026): inventario de archivos (sección 2.3), regla crítica R18 (cuenta raíces, no menciones), seguridad de contenido externo (sección 8) y matriz de archivos (sección 4.3). Ante cualquier conflicto entre este archivo y el Documento 0, prevalece el Documento 0. Este archivo se publica sin entradas reales: contiene su estructura completa, sus reglas y una única entrada de ejemplo claramente marcada como plantilla.

---

## 1. Propósito y alcance

### 1.1 Qué es

El «Registro de evidencia y afirmaciones» (archivo F2) es el registro de la evidencia y de las afirmaciones del Bloque A y el soporte de la trazabilidad claim/evidence: cada afirmación concreta verificable recibe un `claim_id`, cada pieza de evidencia recibe un `evidence_id`, y ambos quedan vinculados con su procedencia completa (cadena raíz→derivada→comentario), su dirección, su estado de verificación y su nivel de confianza. Es la fuente de verdad del enlace entre cada conclusión del Analizador y su soporte probatorio (objetivo OBJ-64) y materializa la organización de la evidencia por raíces y procedencia con deduplicación (OBJ-63). Lo alimenta el módulo de curación del Analizador en la fase 04 del flujo de investigación, con apoyo en el servicio determinista de deduplicación y procedencia.

### 1.2 Qué no es

- No es una colección de enlaces ni un repositorio documental: registra la procedencia y el extracto mínimo con finalidad de verificación, no copias íntegras de obras ajenas; los extractos respetan los límites de conservación del Documento 0 (sección 8).
- No es una valoración de fiabilidad de fuentes: la fiabilidad de la fuente reside en el «Registro de Fuentes Fiables» (source_tier A/B/C), que este archivo referencia; aquí se valora la fiabilidad de cada afirmación concreta (nivel de confianza), que es distinta de la de su fuente.
- No es un archivo de conclusiones del entregable: las conclusiones viajan en los entregables del Analizador; F2 conserva los soportes que las sostienen.
- No es un archivo de acceso libre interno: el Auditor y el Analista de hipótesis contrarias no tienen acceso directo; reciben el material pertinente por CT-07 (revisión experta) y CT-14 (evidence_pack de la petición de refutación).
- No es un archivo reescritible: los estados y los niveles de confianza registrados se congelan (R16); toda corrección es una entrada nueva referenciada a la original.

## 2. Ficha técnica

| Punto | Contenido |
|---|---|
| 1. Nombre, identificador y propósito | «Registro de evidencia y afirmaciones» (nombre canónico en el Documento 0, 2.3), código de archivo F2. Propósito: registrar la evidencia y las afirmaciones con procedencia, dirección y verificación, y sostener la trazabilidad claim/evidence de todos los entregables (OBJ-63 y OBJ-64). |
| 2. Esquema de datos y versión | Esquema V1.1 (ampliación de normalización temporal con la óptima V3.0, 01/11/2026; base V1.0 publicada con la óptima V2.0, 31/10/2026). Los cambios de esquema se tramitan como propuesta de tipo 3 y exigen publicación coordinada. |
| 3. Propietario único de escritura | Analizador de Tendencias de Inversión, por su módulo de curación. El módulo de curación no es un agente independiente: es un módulo operativo del Analizador (elemento en transición su eventual separación, contratos reservados CT-15/CT-16). Ningún otro agente escribe en este archivo. |
| 4. Lectores autorizados y finalidad | Orquestador técnico: lectura para sus comprobaciones deterministas (deduplicación por hash, alcanzabilidad de referencias, referencias cruzadas F1/F2 válidas, cuenta de raíces independientes por conclusión). El Auditor y el Analista de hipótesis contrarias carecen de acceso directo: reciben evidencias y extractos por CT-07 y CT-14. |
| 5. Claves e identificadores de enlace | `evidence_id` (EVD-AAAA-NNNN) y `claim_id` (CLM-AAAA-NNNN) como claves. Enlaces salientes: `trend_id` y `run_id` de F1 y de las ejecuciones que utilizan cada pieza; `source_id` (RF-AAAA) y `source_tier` (A/B/C) hacia el Registro de Fuentes Fiables; `objection_id` y `refutation_id` cuando la pieza sustenta o refuta una objeción CT-14; `audit_id`/`package_id` cuando viaja en el paquete CT-03 (`evidence_root_summary`). Enlaces entrantes: F1 referencia `evidence_id`/`claim_id` por cada hipótesis y cambio de estado; los entregables citan `claim_id`. |
| 6. Política de actualización, conservación y corrección | Append-only: las altas son entradas nuevas; los estados de verificación y los niveles de confianza registrados se congelan (R16); toda corrección es una entrada nueva referenciada a la original, con fecha, motivo y autor. Las piezas refutadas o no verificables se conservan con su estado (nunca se eliminan): la evidencia contraria y los descartes forman parte de la memoria probatoria (OBJ-78). Extractos mínimos con cita y finalidad de verificación, respetando derechos (sección 8 del Documento 0). |
| 7. Reglas de duplicación y resolución de conflictos | Antes de dar de alta una pieza, el módulo de curación aplica el servicio determinista de deduplicación: hash del contenido, normalización de URL y comparación de identificadores documental. Duplicado confirmado: no se abre pieza nueva; la detección se anota en la pieza existente (duplicados resueltos: hash y URL canónica) y se añade la vía de llegada. Dos piezas que provienen de la misma raíz no son raíces independientes: se registran como derivadas de la misma `evidence_id` raíz. Conflicto de contenido entre piezas (mismo hecho, datos distintos): ambas se conservan, se marca la dirección de cada una y la discrepancia queda reflejada como controversia; prevalece la raíz sobre la derivada y, entre raíces, la de mayor proximidad al hecho. |
| 8. Criterios de calidad e integridad | Toda pieza con URL o identificador documental y fecha de acceso; fecha del hecho y periodo de los datos declarados o marcados «desconocido»; extracto con cita o referencia precisa al pasaje; grado de independencia asignado (raíz, derivada o comentario); ninguna afirmación de nivel «establecido» sin raíces independientes que la sustenten (R18); ningún `evidence_id` o `claim_id` roto en las referencias cruzadas con F1. El Orquestador verifica estos criterios con su catálogo de pruebas automatizables. |
| 9. Contratos que lo utilizan | CT-14 «Petición de refutación y paquete de objeciones»: el `evidence_pack` de la petición transporta referencias a afirmaciones y evidencias pertinentes de F2, y las objeciones devueltas referencian `evidence_id`. CT-03 «Paquete de auditoría del Analizador»: transporta el `evidence_root_summary` (raíces independientes por conclusión) y las referencias claim/evidence de la ejecución. CT-07/CT-08 (revisión experta): transportan las evidencias y las pruebas deterministas antes que las conclusiones. CT-13 (retroalimentación del Broker Personal): aporta contexto de calibración que puede motivar la revisión de la confianza de afirmaciones concretas. |
| 10. Pruebas de aceptación y procedimiento de reversión | Aceptación del esquema: (i) estructura completa y sin campos de definición vacíos; (ii) la entrada plantilla valida campo a campo contra el esquema de la sección 3; (iii) la cadena raíz→derivada→comentario de la plantilla es alcanzable y coherente; (iv) el Orquestador puede resolver los identificadores de la plantilla sin referencias rotas (con F1 y el Registro de Fuentes Fiables V2.4 publicados). Reversión: si el operador retira la óptima V2.0, este archivo se retira con ella; por ser un archivo nuevo sin entradas reales, la reversión se limita a retirar la copia publicada; si se hubieran registrado entradas, se conservan en copia de solo lectura fechada antes de la reversión, sin renumeración de identificadores. |

## 3. Esquema de datos

Cada entrada de evidencia contiene los campos siguientes. Los valores controlados son cerrados; su ampliación es un cambio de esquema (tipo 3).

| Campo | Tipo | Obligatorio | Valores controlados / formato | Descripción |
|---|---|---|---|---|
| `evidence_id` | Identificador | Sí (inmutable) | `EVD-AAAA-NNNN` (AAAA año de alta; NNNN correlativo dentro del año, sin reutilización) | Clave de la pieza de evidencia. |
| `claim_id` | Identificador | Sí (inmutable) | `CLM-AAAA-NNNN` (mismo formato) | Clave de la afirmación que la pieza sostiene, matiza o contradice. Una afirmación puede tener varias piezas; una pieza puede servir a varias afirmaciones. |
| `afirmacion` | Texto | Sí | Enunciado concreto, verificable y fechable; prohibidas las fórmulas vagas sin criterio de verificación | Afirmación concreta que la evidencia sostiene. |
| `fuente_raiz` | Texto con identificador | Sí | `source_id` (RF-AAAA) del Registro de Fuentes Fiables; «no registrada» solo con declaración de motivo | Fuente original de primera mano (raíz). |
| `fuentes_derivadas` | Lista estructurada | No | Cada una con: vía (medio que reproduce), URL y relación con la raíz | Fuentes que reproducen o comentan la raíz; nunca sustituyen a la raíz para el cómputo de independencia. |
| `url` | Texto (URL) | Sí | URL canónica declarada (la de la raíz, no la del agregador) | Localización de la pieza. |
| `identificador_documental` | Texto | Sí | DOI, ISSN, número de expediente, fichero, sección o el que proceda; «no aplicable» solo para piezas sin identificador | Identificador estable del documento o pasaje. |
| `fecha_acceso` | Fecha | Sí | ISO 8601 | Fecha de consulta y captura de la pieza. |
| `fecha_hecho` | Fecha | Sí | ISO 8601 o «desconocido» declarado | Fecha del hecho que la pieza documenta. |
| `periodo_datos` | Texto | Sí | Periodo cubierto por los datos (por ejemplo, «2025-T1 a 2026-T2») o «no aplicable» | Periodicidad y ventana temporal de los datos subyacentes. |
| `extracto` | Texto con cita | Sí | Extracto mínimo entre comillas o referencia precisa al pasaje (sección, página, párrafo) | Pasaje pertinente con finalidad de verificación; nunca la obra íntegra. |
| `tipo_fuente` | Valor controlado | Sí | primaria · secundaria · terciaria | Tipología del documento según su proximidad al hecho (coherente con la tipología del Registro de Fuentes Fiables V2.4). |
| `grado_independencia` | Valor controlado | Sí | raíz · derivada · comentario | Posición en la cadena de procedencia: raíz (primera mano), derivada (reproduce la raíz), comentario (análisis u opinión sobre la raíz). |
| `direccion_evidencia` | Valor controlado | Sí | favorable · contraria · neutra · ambigua | Dirección de la pieza respecto de la afirmación referenciada. |
| `limitaciones_controversias` | Texto | Sí | Declaración expresa; «ninguna conocida» solo con motivo | Limitaciones metodológicas, muestra, conflicto de interés, revisiones posteriores y controversias con otras piezas. |
| `estado_verificacion` | Valor controlado | Sí | pendiente · en verificación · verificada · verificada con reservas · no verificable · refutada | Estado del proceso de verificación de la pieza. |
| `nivel_confianza` | Valor controlado | Sí | establecido · probable · especulativo · en disputa | Nivel de confianza de la afirmación (vocabulario de confianza del Documento 0): establecido (hecho verificado con raíces independientes), probable (respaldo sólido con incertidumbre residual), especulativo (inferencia, proyección o señal temprana), en disputa (objeción fuerte sin resolver o evidencia contradictoria relevante). |
| `utilizada_por` | Lista estructurada | Sí | Cada uso con: `trend_id` de F1 o informe (identificado por `run_id`) y papel (soporte de hipótesis · soporte de explicación alternativa · base de cambio de estado · soporte de objeción) | Tendencias e informes que utilizan la pieza. |
| `duplicados_resueltos` | Lista estructurada | No | Cada resolución con: hash del contenido, URL duplicada y URL canónica conservada | Deduplicación documentada por el servicio determinista; la pieza canónica conserva el registro de sus duplicados. |
| `source_tier` | Valor controlado con enlace | Sí | A · B · C, más `source_id` (RF-AAAA) de la ficha de fuente del Registro de Fuentes Fiables V2.4 | Nivel de fiabilidad de la fuente; distinto del nivel de confianza de la afirmación. |

## 3-bis. Normalización temporal (añadida con la óptima V3.0)

Con la óptima V3.0 del Documento 0 (2.7.6), cada entrada de evidencia con componente temporal
registra, cuando proceda, los campos siguientes (obligatorios cuando el dato es una serie o una
cifra de mercado; opcionales en evidencia textual):

| Campo | Formato | Descripción |
|---|---|---|
| `fecha_fenomeno` | ISO 8601 | Fecha del hecho observado, cuando exista. |
| `periodo_datos` | Texto (p. ej. 2026-Q3) | Periodo al que corresponde el dato. |
| `fecha_publicacion` | ISO 8601 | Fecha de publicación de la fuente. |
| `fecha_recuperacion` | ISO 8601 | Fecha de acceso del agente. |
| `fecha_revision` | ISO 8601 | Fecha de la última revisión declarada por la fuente, si existe. |
| `frecuencia` | Valor controlado | diaria · semanal · mensual · trimestral · anual · irregular. |
| `zona_horaria` | Texto (IANA) | Zona horaria de la serie o del hecho. |
| `unidad_divisa` | Texto | Unidad y divisa del dato, con la conversión declarada cuando proceda. |
| `version_fuente` | Texto | Versión o revisión de la fuente utilizada. |
| `fecha_conocimiento` | ISO 8601 | Fecha a partir de la cual el dato podía conocerse: toda evaluación histórica debe poder filtrar por este campo (prohibición de fuga de información, 2.7.6). |

Las entradas registradas bajo el esquema V1.0 conservan su formato; los campos nuevos se
cumplimentan en altas y revisiones posteriores.

## 4. Reglas de registro

### 4.1 Altas

1. El módulo de curación da de alta cada pieza en la fase 04 del flujo (curación y normalización), tras pasar el servicio determinista de deduplicación y el marcado de procedencia (origen, fecha de acceso, cadena raíz→derivada).
2. El alta exige, como mínimo: `evidence_id`, `claim_id`, afirmación concreta, fuente con `source_tier`, URL e identificador documental con fecha de acceso, extracto con cita, tipo de fuente, grado de independencia, dirección y estado de verificación.
3. El contenido captado entra en cuarentena como dato no fiable (R17): ninguna fuente puede activar herramientas, cambiar parámetros ni alterar el flujo; el alta registra la pieza, nunca ejecuta su contenido.
4. La cadena de procedencia es obligatoria: toda pieza derivada o comentario referencia su `evidence_id` raíz; una pieza sin raíz identificada se registra con grado «comentario» o «derivada» y la raíz como «no identificada» con motivo, y jamás computa como raíz independiente.

### 4.2 Cuenta de raíces (R18)

1. La solidez de una evidencia se mide por sus raíces independientes, no por el número de publicaciones que la reproducen: cuenta raíces, no menciones.
2. Ejemplo normativo del criterio: una raíz, veinte publicaciones. Si un informe original (raíz) es reproducido por veinte medios, el registro contiene una única raíz y las veinte reproducciones se anotan como derivadas de esa raíz: la afirmación que se apoya solo en ese informe tiene una raíz independiente, no veinte. Las veinte derivadas pueden aportar difusión y comodidad de acceso, pero no independencia.
3. El `evidence_root_summary` del paquete de auditoría (CT-03) cuenta raíces, no piezas: el Orquestador contrasta el cómputo con este archivo.
4. Dos raíces no son independientes entre sí si comparten origen documental, propiedad editorial o cadena de sindicación; en caso de duda, se registran como dependientes y la independencia se declara con su justificación.

### 4.3 Cambios y estados de verificación

1. El ciclo de verificación mueve `estado_verificacion` de «pendiente» a «en verificación», «verificada», «verificada con reservas», «no verificable» o «refutada». Cada movimiento es una entrada nueva con fecha y motivo; el estado anterior se conserva en el historial de la pieza.
2. El `nivel_confianza` de la afirmación se revisa cuando cambia la evidencia (nueva raíz, refutación, objeción CT-14 fuerte sin resolver). El nivel vigente es el último registrado; los niveles anteriores se conservan.
3. Una afirmación con objeción fuerte sin resolver no puede declararse «establecido»; pasa a «en disputa» hasta su resolución documentada.

### 4.4 Correcciones

1. Toda corrección es una entrada nueva referenciada a la original (R16): si un extracto se transcribió mal, si una URL canónica cambió o si un grado de independencia estaba mal asignado, la entrada original no se modifica; se publica la corrección con su fecha, motivo y autor.
2. Los errores de identificador se corrigen con referencia cruzada; los identificadores no se renumeran ni se reutilizan.
3. Las piezas refutadas se conservan con estado «refutada» y su `direccion_evidencia`; su supresión física está prohibida (memoria probatoria completa, OBJ-78).

## 5. Índice del registro y plantilla de entrada

### 5.1 Estructura del archivo

El archivo se compone de cuatro secciones, en este orden:

1. Índice operativo del registro: recuento de piezas por grado de independencia, por dirección y por estado de verificación; raíces independientes abiertas; duplicados resueltos en el último periodo; piezas no verificables o refutadas; fecha de última revisión del índice.
2. Entradas de evidencia (sección principal): una entrada por `evidence_id`, en orden de alta, con sus campos, su cadena de procedencia y su historial de verificación.
3. Registro de correcciones: entradas de corrección referenciadas a la pieza y a la entrada original.
4. Registro de versiones del propio archivo (sección 6).

### 5.2 Índice operativo (estado de arranque)

| Campo | Valor |
|---|---|
| Versión del esquema | V1.0 |
| Piezas por grado de independencia | raíz: 0 · derivada: 0 · comentario: 0 |
| Piezas por dirección | favorable: 0 · contraria: 0 · neutra: 0 · ambigua: 0 |
| Piezas por estado de verificación | pendiente: 0 · en verificación: 0 · verificada: 0 · verificada con reservas: 0 · no verificable: 0 · refutada: 0 |
| Afirmaciones por nivel de confianza | establecido: 0 · probable: 0 · especulativo: 0 · en disputa: 0 |
| Duplicados resueltos en el último periodo | Ninguno |
| Fecha de última revisión del índice | 2026-10-31 (publicación) |
| Carencias y prioridades | Primera carga con la primera ejecución del Analizador tras la activación de la óptima V2.0 |

### 5.3 Plantilla de entrada de evidencia

La entrada siguiente es un ejemplo ficticio que muestra el formato de ficha: **(plantilla — no es una entrada real)**. Ningún dato de esta plantilla documenta un hecho real; los identificadores de ejemplo no se reutilizan.

#### EVD-2026-0001 — (plantilla — no es una entrada real)

*Identificación y afirmación.* **evidence_id:** EVD-2026-0001 · **claim_id:** CLM-2026-0001 · **afirmacion:** el ejemplo ficticio de entidad declara haber reducido el coste unitario del procesamiento documental un 30 por ciento en su piloto de 2026 · **fuente_raiz:** RF-0002 (ficha de fuente del Registro de Fuentes Fiables) · **fuentes_derivadas:** una reproducción editorial (URL y relación con la raíz anotadas en la ficha) · **tipo_fuente:** primaria · **grado_independencia:** raíz

*Localización y datos.* **url:** https://ejemplo-ficticio.invalid/piloto-2026 (URL ficticia de plantilla) · **identificador_documental:** formulario de ejemplo, sección 2, página 7 · **fecha_acceso:** 2026-11-04 · **fecha_hecho:** 2026-09-30 · **periodo_datos:** 2026-T1 a 2026-T3

*Contenido y valoración.* **extracto:** «el pasaje ficticio de plantilla declara la cifra del piloto con su metodología en la nota 4» · **direccion_evidencia:** favorable · **limitaciones_controversias:** datos autodeclarados por la entidad, muestra de un único piloto, sin auditoría externa conocida · **estado_verificacion:** verificada con reservas · **nivel_confianza:** probable · **source_tier:** A (RF-0002)

*Uso y trazabilidad.* **utilizada_por:** tendencia TND-2026-0001 (soporte de hipótesis, ficha plantilla de F1); informe de la ejecución RUN-2026-1110 (plantilla) · **duplicados_resueltos:** una copia sindicada resuelta hacia la URL canónica de la raíz (hash registrado en la ficha) · **historial_verificacion:** 2026-11-04 · alta y verificación con reservas (módulo de curación, run_id RUN-2026-1110) · todas las referencias de esta plantilla son ficticias y no existen en F1 ni en el Registro de Fuentes Fiables

## 6. Registro de versiones del archivo

| Versión | Fecha | Descripción |
|---|---|---|
| V1.1 | 01/11/2026 | Ampliación del esquema aplicada con la óptima V3.0 del Documento 0: nueva sección 3-bis de normalización temporal (fecha del fenómeno, periodo, publicación, recuperación, revisión, frecuencia, zona horaria, unidad y divisa, versión de fuente y fecha de conocimiento, con prohibición de fuga de información); las entradas V1.0 conservan su formato. |
| V1.0 | 31/10/2026 | Publicación inicial del archivo F2 con la óptima V2.0 del Bloque A: esquema V1.0 completo, ficha técnica de diez puntos, cadena raíz→derivada→comentario, regla R18 (cuenta raíces, no menciones), deduplicación por hash y URL canónica, vocabulario de confianza y reglas de registro. Archivo publicado sin entradas reales. |
