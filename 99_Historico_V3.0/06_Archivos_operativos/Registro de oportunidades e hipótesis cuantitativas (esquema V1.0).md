# Registro de oportunidades e hipótesis cuantitativas (esquema V1.0) — Archivo F3

**Proyecto Robot Investor · Bloque A — Analizador de Tendencias de Inversión**

**Archivo operativo · Esquema V1.0 · 01/11/2026 · Propietario único de escritura: Analizador de Tendencias de Inversión · Estado: operativo desde la publicación coordinada de la óptima V3.0 (01/11/2026)**

Archivo F3 creado por la óptima V3.0 del Bloque A (Documento 0, secciones 1.5 y 2.3). Se rige por el «Documento 0 — Protocolo maestro del Bloque A», versión óptima V3.0 (01/11/2026): inventario de archivos (2.3), distinción entre tendencia, exposición y oportunidad (1.5), matriz de archivos (4.3) y glosario. Ante cualquier conflicto entre este archivo y el Documento 0, prevalece el Documento 0. Se publica sin entradas reales: contiene su estructura completa, sus reglas y una única entrada de ejemplo claramente marcada como plantilla.

---

## 1. Propósito y alcance

### 1.1 Qué es

El «Registro de oportunidades e hipótesis cuantitativas» (archivo F3) conserva la **identificación preliminar de exposiciones de inversión** vinculadas a tendencias del bloque: una ficha por oportunidad, con su identificador estable, su vínculo a la tendencia de origen (TND-), su tesis de exposición y mecanismo de captura de valor, sus expectativas conocidas y sus limitaciones, sus escenarios, catalizadores, riesgos y condiciones de invalidación, sus datos y cálculos de soporte con versión, y su recomendación de siguiente paso (descartar, observar, profundizar o remitir a otro bloque). Da cumplimiento a la sección 1.5 del Documento 0 y a los objetivos de la dimensión 8 del listado de objetivos óptima V2.1.

### 1.2 Qué no es

- **No es una recomendación de inversión**: la identificación preliminar de una exposición no aconseja comprar, vender ni mantener; el asesoramiento sigue siendo exclusivo del Broker Personal. Tampoco sustituye al análisis de mercado (Bloque B) ni a la evaluación de cartera de los bloques posteriores.
- **No reintroduce el Opportunity Score**: retirado como puntuación del bloque desde la óptima V2.0, no vuelve; la recomendación de siguiente paso de F3 es cualitativa, y la puntuación de la tendencia (E/T/M, F1) responde a otra pregunta y no se mezcla con la identificación de la exposición (4.2, regla 10 del Documento 0).
- **No es un registro de tendencias**: la memoria de tendencias es F1; F3 la complementa con las exposiciones, sin duplicar su contenido.
- **No es un archivo de evidencia**: la evidencia reside en F2; F3 la referencia por `evidence_id` y `claim_id`.
- **No es un histórico desechable**: las oportunidades descartadas y vencidas se conservan (sin sesgo de supervivencia, OBJ-78).

## 2. Ficha técnica

| Punto | Contenido |
|---|---|
| 1. Nombre, identificador y propósito | «Registro de oportunidades e hipótesis cuantitativas» (nombre canónico en el Documento 0, 2.3), código F3. Propósito: identificación preliminar de exposiciones vinculadas a tendencias, con recomendación de siguiente paso e historial append-only. |
| 2. Esquema de datos y versión | Esquema V1.0, publicado con la óptima V3.0 (01/11/2026). Los cambios de esquema se tramitan como tipo 3 con publicación coordinada. |
| 3. Propietario único de escritura | Analizador de Tendencias de Inversión. |
| 4. Lectores autorizados y finalidad | Orquestador técnico: lectura para comprobaciones deterministas (coherencia OPP↔TND, recomendaciones válidas, fechas y estados). El Auditor y el Analista de hipótesis contrarias carecen de acceso directo (material por CT-07 y CT-14). El Broker Personal y el usuario solo ven lo que los entregables declaren. |
| 5. Claves e identificadores de enlace | `opp_id` (formato OPP-AAAA-NNNN) como clave primaria. Enlaces salientes: `trend_id` hacia F1; `evidence_id` y `claim_id` hacia F2; `entry_id` del Registro de cálculos (cálculos utilizados y su versión); `run_id`/`request_id` de la ejecución; `prg_id` hacia F4 cuando la oportunidad declare pronósticos congelados. Enlaces entrantes: F1 (oportunidades_vinculadas), F4 (referencia OPP-). |
| 6. Política de actualización, conservación y corrección | Append-only: altas y revisiones como entradas nuevas fechadas; corrección siempre en nueva versión referenciada a la original (regla crítica 16). Las oportunidades descartadas y vencidas se conservan. |
| 7. Reglas de duplicación y resolución de conflictos | Antes del alta, comprobación de duplicados por `trend_id` + instrumento + horizonte; duplicado declarado en la ficha existente sin apertura nueva. Conflicto entre fichas: prevalece la revisada más recientemente con justificación documentada; la discrepancia se registra en nueva versión. |
| 8. Criterios de calidad e integridad | Todo campo obligatorio cumplimentado o declarado; fechas ISO 8601; recomendación dentro de los valores controlados; referencias a F1, F2 y Registro de cálculos alcanzables (sin identificadores rotos); valoración cuantitativa siempre con su cálculo y versión referenciados; sin cifras sin fuente. El Orquestador verifica estos criterios en sus comprobaciones deterministas. |
| 9. Contratos que lo utilizan | CT-03 (paquete de auditoría del Analizador): las oportunidades registradas en la ejecución quedan referenciadas para su auditoría. CT-07/CT-08 (revisión experta): transportan el material de F3 pertinente. CT-11 (servicio de cálculo): los cálculos que sostienen una valoración preliminar se solicitan al Motor y quedan referenciados por su `entry_id`. CT-21 (reserva): el paquete de tendencias y oportunidades para el Bloque B, cuando se active. |
| 10. Pruebas de aceptación y procedimiento de reversión | Aceptación: estructura completa sin campos vacíos de definición; plantilla válida contra el esquema de la sección 3; referencias de la plantilla resolvibles (con F1 y F2 publicados). Reversión: si el operador retira la óptima V3.0, el archivo se retira con ella; las entradas registradas se conservan en copia de solo lectura fechada, sin renumeración de identificadores. |

## 3. Esquema de datos

| Campo | Tipo | Obligatorio | Valores controlados / formato | Descripción |
|---|---|---|---|---|
| `opp_id` | Identificador | Sí (inmutable) | `OPP-AAAA-NNNN` | Clave primaria de la ficha. |
| `trend_id` | Identificador | Sí | `TND-AAAA-NNNN` válido en F1 | Tendencia de origen de la identificación. |
| `clase_activo` | Valor controlado | Sí | ACC · FIR · FX · CMD · ETF · DER · REI · CHR · PRV · ALT · MIX | Clase de activo del instrumento o exposición. |
| `instrumento` | Texto | Sí | Libre (denominación e identificador de mercado cuando exista) | Activo, instrumento, empresa, sector o estrategia con exposición. |
| `mercado_region_moneda` | Texto estructurado | Sí | Libre (mercado, región operativa y moneda de referencia) | Contexto de contratación. |
| `fecha_identificacion` | Fecha | Sí | ISO 8601 | Fecha de la ejecución en que se identificó. |
| `fecha_referencia` | Fecha | Sí | ISO 8601 | Fecha de referencia de los datos y valoraciones de la ficha. |
| `horizonte_temporal` | Valor controlado | Sí | corto (hasta 2 años) · medio (2 a 5 años) · largo (más de 5 años) | Horizonte de la tesis de exposición. |
| `tesis_exposicion` | Texto con referencia | Sí | Afirmación refutable, enlazada a `claim_id` de F2 | Por qué el activo ofrece exposición a la tendencia y qué parte de la cadena de valor capturaría los beneficios. |
| `exposicion_economica` | Texto | Sí | Libre, cuantificada cuando los datos lo permitan | Naturaleza y magnitud de la exposición (directa, indirecta o narrativa; ingreso, flujo o valoración dependiente). |
| `datos_fuentes` | Lista de identificadores | Sí | `evidence_id`/`claim_id` de F2 | Datos y fuentes utilizados (raíces registradas). |
| `valoracion_cuanti` | Bloque estructurado | No | Solo cuando sea viable: cifra, unidad, fecha, `entry_id` y versión del cálculo del Motor (CT-11), y método | Referencia cuantitativa preliminar; prohibido presentarla como precio objetivo o recomendación. |
| `expectativas_mercado` | Texto | No | Libre, con su fuente y limitaciones declaradas | Qué expectativas parece descontar el mercado, cuando los datos permiten estimarlo, con las limitaciones de la estimación. |
| `escenarios_supuestos` | Lista estructurada | Sí (mínimo dos: base y adverso) | Libre, con supuestos explícitos | Escenarios de evolución de la exposición y sus supuestos. |
| `catalizadores` | Lista de texto | No | Libre, observable | Hechos futuros que podrían modificar las expectativas. |
| `riesgos_invalidez` | Lista de texto | Sí (mínimo una) | Libre, operativa y observable | Riesgos que pueden impedir que la tendencia real se traduzca en rentabilidad; condiciones de invalidación de la ficha. |
| `liquidez_accesibilidad_costes` | Texto estructurado | Sí | Libre (con el filtro del Anexo F del Analizador cuando proceda) | Liquidez, accesibilidad (9.1 del Analizador) y costes de la exposición; inviabilidad declarada cuando exista. |
| `calculos_utilizados` | Lista de identificadores | No | `entry_id` (Registro de cálculos, esquema V1.2) con method_id y versión | Cálculos del Motor que sostienen la ficha. |
| `incertidumbres_pendientes` | Lista de texto | Sí | Libre | Incertidumbres abiertas que impiden profundizar. |
| `recomendacion_siguiente_paso` | Valor controlado | Sí | descartar · observar · profundizar · remitir a otro bloque | Recomendación cualitativa de siguiente paso (sin valores numéricos). |
| `estado` | Valor controlado | Sí | identificada · en estudio · propuesta de profundización · remitida a otro bloque · descartada · vencida | Estado de la ficha; transiciones declaradas en la sección 4. |
| `historial_cambios` | Lista append-only | Sí | Cada entrada con: fecha ISO, `run_id`, campo o estado anterior, nuevo, justificación y referencias | Historial de cambios; prohibido reescribir el pasado. |
| `resultado_posterior` | Bloque estructurado | No | Solo cuando pueda medirse: fecha, observación, fuente y desviación frente a la tesis | Resultado observado de la exposición, para el nivel B del circuito de aprendizaje (2.7.7); nunca se reescribe la tesis original. |

## 4. Reglas de registro

1. **Altas.** El Analizador da de alta una ficha cuando el cribado de la sección 9.2 de su prompt identifica una exposición preliminar digna de memoria. El alta exige `opp_id`, `trend_id` válido, clase de activo, instrumento, fechas, tesis con referencia a F2, escenarios, al menos una condición de invalidación, liquidez/accesibilidad y recomendación de siguiente paso.
2. **Transiciones de estado** (las no listadas están prohibidas): identificada → en estudio (búsqueda o cálculo adicional aprobado en el presupuesto); identificada o en estudio → propuesta de profundización (exposición sostenida con datos suficientes); identificada, en estudio o propuesta → descartada (exposición no demostrada, inviabilidad de acceso o invalidación); propuesta → remitida a otro bloque (cuando el operador o el Broker Personal dirijan el análisis posterior); cualquier estado → vencida (horizonte superado sin actividad). Historial append-only (regla crítica 16).
3. **Correcciones.** Siempre en nueva versión referenciada a la original; la valoración preliminar se actualiza con el cálculo nuevo referenciado, sin borrar el anterior.
4. **Prohibiciones.** No se registran recomendaciones de compra o venta; no se mezclan puntuaciones de tendencia con la identificación de exposición; no se registra valoración cuantitativa sin cálculo referenciado del Motor; no se declara la inviabilidad de acceso sin el filtro del Anexo F del Analizador cuando aplique.

## 5. Índice del registro y plantilla

### 5.1 Estructura del archivo

1. Índice operativo: recuento por estado y por clase de activo; altas del trimestre; fecha de última revisión.
2. Fichas por oportunidad (sección principal), en orden de alta.
3. Registro de correcciones y reversiones.
4. Registro de versiones del propio archivo (sección 6).

### 5.2 Índice operativo (estado de arranque)

| Campo | Valor |
|---|---|
| Versión del esquema | V1.0 |
| Fichas por estado | identificada: 0 · en estudio: 0 · propuesta de profundización: 0 · remitida a otro bloque: 0 · descartada: 0 · vencida: 0 |
| Fichas por clase de activo | Ninguna (archivo recién publicado) |
| Fecha de última revisión del índice | 2026-11-01 (publicación) |
| Carencias y prioridades | Primera carga con la primera ejecución del Analizador bajo la óptima V2.1 de su prompt |

### 5.3 Plantilla de entrada (ficticia)

#### OPP-2026-0001 — (plantilla — no es una entrada real)

*Identificación.* **opp_id:** OPP-2026-0001 · **trend_id:** TND-2026-0001 (plantilla de F1) · **clase_activo:** ACC · **instrumento:** Ejemplo Industrial Térmica S. A. (acción ficticia) · **mercado_region_moneda:** mercado español; EUR · **fecha_identificacion:** 2026-11-05 · **fecha_referencia:** 2026-11-05 · **horizonte_temporal:** medio (2 a 5 años) · **estado:** identificada

*Tesis y exposición.* **tesis_exposicion:** la sustitución de flujos manuales de documentación por flujos generativos supervisados beneficia a los proveedores de integración del segmento, con captura de valor concentrada en el eslabón de software y servicios (claim_id: CLM-2026-0001, plantilla) · **exposicion_economica:** exposición directa estimada: 35 % de ingresos del segmento de servicios ligado a la tendencia (según la fuente referenciada) · **datos_fuentes:** EVD-2026-0001 (plantilla) · **expectativas_mercado:** no estimadas (sin consenso disponible); limitación declarada

*Escenarios y riesgos.* **escenarios_supuestos:** base — adopción conforme a la curva de la tendencia; adverso — abandono de pilotos superior al 50 % · **catalizadores:** contratos públicos de referencia 2027 · **riesgos_invalidez:** concentración de ingresos fuera del segmento declarado; múltiplo exigente sin mejora de márgenes verificable · **liquidez_accesibilidad_costes:** negociada en mercado regulado con acceso minorista; costes de transacción estándar · **incertidumbres_pendientes:** calidad contable de los ajustes no recurrentes

*Trazabilidad.* **valoracion_cuanti:** no registrada (sin cálculo referenciado) · **calculos_utilizados:** ninguno aún · **recomendacion_siguiente_paso:** observar · **historial_cambios:** 2026-11-05 · run_id RUN-2026-1111 · alta inicial · **resultado_posterior:** no medido (todas las referencias de esta plantilla son ficticias)

## 6. Registro de versiones del archivo

| Versión | Fecha | Descripción |
|---|---|---|
| V1.0 | 01/11/2026 | Publicación inicial del archivo F3 con la óptima V3.0 del Bloque A: esquema completo (identificación, tesis de exposición, expectativas, escenarios, riesgos, recomendación cualitativa de siguiente paso e historial append-only), ficha técnica de diez puntos, reglas de registro y plantilla. Archivo publicado sin entradas reales. |
