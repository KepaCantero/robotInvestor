# Registro de pronósticos congelados (esquema V1.0) — Archivo F4

**Proyecto Robot Investor · Bloque A — Analizador de Tendencias de Inversión**

**Archivo operativo · Esquema V1.0 · 01/11/2026 · Propietario único de escritura: Analizador de Tendencias de Inversión (con la colaboración de cálculo del Motor por el CT-11) · Estado: operativo desde la publicación coordinada de la óptima V3.0 (01/11/2026)**

Archivo F4 creado por la óptima V3.0 del Bloque A (Documento 0, secciones 2.3 y 2.7.7). Se rige por el «Documento 0 — Protocolo maestro del Bloque A», versión óptima V3.0 (01/11/2026). Ante cualquier conflicto entre este archivo y el Documento 0, prevalece el Documento 0. Se publica sin entradas reales: contiene su estructura completa, sus reglas y una única entrada de ejemplo claramente marcada como plantilla.

---

## 1. Propósito y alcance

### 1.1 Qué es

El «Registro de pronósticos congelados» (archivo F4) conserva los pronósticos, escenarios y estimaciones que el bloque declara congelados en su fecha: una entrada por pronóstico, con su identificador estable, su vínculo a la tendencia (TND-), a la oportunidad (OPP-) y a la ejecución (run_id), su fecha de congelación, su horizonte, sus supuestos, sus escenarios, sus probabilidades cuando exista base metodológica declarada, sus indicadores de seguimiento, sus condiciones de invalidación y su resultado posterior cuando pueda medirse. Es la base de la evaluación histórica sin fuga de información y del nivel B del circuito de aprendizaje (2.7.7 del Documento 0), y, cuando se active, del Evaluador de previsiones (elemento en transición, 2.6).

### 1.2 Qué no es

- **No es editable hacia atrás**: el historial es append-only; las correcciones generan una nueva versión referenciada a la original y nunca se reescribe un pronóstico congelado (regla crítica 16 del Documento 0). Ningún agente puede retocar pronósticos antiguos para que parezcan acertados.
- **No es un entregable**: no se envía al Broker Personal ni al usuario; los entregables citan sus `prg_id`.
- **No es un registro de tendencias ni de oportunidades**: complementa a F1 y F3 con las declaraciones prospectivas contrastables.
- **No es un sustituto del cálculo reproducible**: las cifras de un pronóstico congelado referencian sus entradas del Registro de cálculos (esquema V1.2) con su artefacto; F4 no reproduce el cálculo.
- **No es una fuente de probabilidades libres**: toda probabilidad registrada exige base metodológica declarada (método, muestra y limitaciones); sin ella, el campo queda vacío.

## 2. Ficha técnica

| Punto | Contenido |
|---|---|
| 1. Nombre, identificador y propósito | «Registro de pronósticos congelados» (nombre canónico en el Documento 0, 2.3), código F4. Propósito: congelación append-only de pronósticos, escenarios y estimaciones contrastables, con condiciones de invalidación y resultado posterior. |
| 2. Esquema de datos y versión | Esquema V1.0, publicado con la óptima V3.0 (01/11/2026). Cambios de esquema por tipo 3 con publicación coordinada. |
| 3. Propietario único de escritura | Analizador de Tendencias de Inversión; las cifras de cálculo se solicitan al Motor por el CT-11 y quedan referenciadas por su `entry_id`. |
| 4. Lectores autorizados y finalidad | Orquestador técnico: lectura para comprobaciones deterministas (coherencia PRG↔TND/OPP, ausencia de reescrituras, condiciones de invalidación declaradas). El Auditor y el Analista de hipótesis contrarias carecen de acceso directo (material por CT-07 y CT-14). El futuro Evaluador de previsiones lo contrastará en su fecha (2.6). |
| 5. Claves e identificadores de enlace | `prg_id` (formato PRG-AAAA-NNNN) como clave primaria. Enlaces salientes: `trend_id` (F1), `opp_id` (F3), `run_id`/`request_id` (ejecución), `entry_id` con method_id y versión (Registro de cálculos), `evidence_id`/`claim_id` (F2) para los supuestos, `source_id` (Registro de Fuentes Fiables) para los indicadores. Enlaces entrantes: F1 (pronosticos_vinculados), F3 (cuando la oportunidad declare pronósticos), Evaluador de previsiones (cuando se active). |
| 6. Política de actualización, conservación y corrección | Append-only (regla crítica 16): la congelación es una entrada nueva fechada; el resultado posterior es un campo aditivo registrado en su fecha; toda corrección es una nueva versión referenciada a la original. Conservación indefinida, incluidos los pronósticos fallidos y las invalidaciones (sin sesgo de supervivencia). |
| 7. Reglas de duplicación y resolución de conflictos | Antes de congelar, comprobación de duplicados por `trend_id`/`opp_id` + tipo de pronóstico + horizonte + fecha; duplicado declarado sin entrada nueva. Dos pronósticos distintos sobre lo mismo pueden coexistir (escenarios alternativos) si sus supuestos difieren declaradamente. |
| 8. Criterios de calidad e integridad | Todo campo obligatorio cumplimentado o declarado; fechas ISO 8601; horizonte y condiciones de invalidación operativas y observables; probabilidades solo con base metodológica declarada; cifras con `entry_id` del Registro de cálculos; campos temporales de la normalización (2.7.6) presentes cuando el pronóstico dependa de series; sin fuga de información (nada registrado como conocido después de la fecha de congelación). El Orquestador verifica estos criterios. |
| 9. Contratos que lo utilizan | CT-11 (servicio de cálculo): cifras del pronóstico con su artefacto reproducible. CT-03 (paquete de auditoría): los pronósticos congelados en la ejecución quedan referenciados. CT-07/CT-08: material de revisión experta. CT-19 (reserva): cuando se active el Evaluador de previsiones, su entrada será el F4. |
| 10. Pruebas de aceptación y procedimiento de reversión | Aceptación: estructura completa; plantilla válida contra el esquema de la sección 3; referencias de la plantilla resolvibles (con F1 y F2 publicados; F3 cuando exista). Reversión: si el operador retira la óptima V3.0, el archivo se retira con ella; las entradas registradas se conservan en copia de solo lectura fechada, sin renumeración de identificadores. |

## 3. Esquema de datos

| Campo | Tipo | Obligatorio | Valores controlados / formato | Descripción |
|---|---|---|---|---|
| `prg_id` | Identificador | Sí (inmutable) | `PRG-AAAA-NNNN` | Clave primaria de la entrada. |
| `trend_id` | Identificador | Sí (uno de trend_id u opp_id) | `TND-AAAA-NNNN` válido en F1 | Tendencia a la que pertenece el pronóstico. |
| `opp_id` | Identificador | No | `OPP-AAAA-NNNN` válido en F3 | Oportunidad relacionada, cuando exista. |
| `run_id` | Identificador | Sí | `RUN-AAAA-NNNN` (y `request_id` cuando proceda) | Ejecución en que se congeló. |
| `fecha_congelacion` | Fecha | Sí | ISO 8601 | Fecha en que el pronóstico se declara congelado. |
| `tipo_pronostico` | Valor controlado | Sí | trayectoria · dirección · fase_o_regimen · umbral_de_hito · escenarios_condicionados | Naturaleza del pronóstico. |
| `horizonte` | Texto estructurado | Sí | Fecha objetivo o plazo declarado (ISO 8601 o rango) | Cuándo se contrastará. |
| `supuestos` | Lista de texto con referencias | Sí | Libre, enlazado a `claim_id`/`evidence_id` de F2 cuando proceda | Supuestos explícitos del pronóstico. |
| `escenarios` | Lista estructurada | Sí (mínimo dos) | Cada escenario con: nombre, descripción, supuestos y valores o trayectorias declarados | Escenarios congelados (base, adverso y, si procede, optimista). |
| `probabilidades` | Bloque estructurado | No | Solo con base metodológica declarada: método, muestra, limitaciones; sin ella, vacío | Probabilidades asociadas a los escenarios. |
| `valores_congelados` | Lista estructurada | Sí cuando existan cifras | Cada cifra con: valor, unidad, fecha y `entry_id` del Registro de cálculos (method_id y versión) | Cifras congeladas con su cálculo reproducible referenciado. |
| `indicadores_seguimiento` | Lista estructurada | Sí | Cada indicador con: nombre, `source_id` (Registro de Fuentes Fiables), frecuencia y umbral | Qué se observará para contrastar el pronóstico. |
| `condiciones_invalidez` | Lista de texto | Sí (mínimo una) | Libre, operativa y observable | Condiciones que, cumplidas, invalidan el pronóstico. |
| `estado` | Valor controlado | Sí | congelado · contrastado_conforme · contrastado_desviado · invalidado · expirado_sin_contraste | Estado del pronóstico; transiciones declaradas en la sección 4. |
| `resultado_posterior` | Bloque estructurado | No | Solo cuando pueda medirse: fecha del contraste, observación con su fuente, desviación frente al valor congelado y referencia del contraste | Resultado observado, registrado en su fecha; alimenta el nivel B del circuito de aprendizaje (2.7.7). |
| `historial_versiones` | Lista append-only | Sí | Cada entrada con: fecha ISO, `run_id`, tipo (congelación · corrección en nueva versión · resultado posterior · invalidación) y referencias | Historial del pronóstico; prohibido reescribir la entrada original. |
| `fecha_conocimiento` | Fecha | Sí | ISO 8601 | Fecha a partir de la cual el pronóstico podía haberse formado (normalización temporal, 2.7.6); base del filtro anti-fuga en la evaluación histórica. |

## 4. Reglas de registro

1. **Congelación.** Cuando una ejecución declare pronósticos, escenarios o estimaciones contrastables (fases 06 y 08 del flujo, 2.7.1 del Documento 0), el Analizador congela una entrada con los campos obligatorios. Sin condiciones de invalidación no hay congelación: el pronóstico se declara como narrativa no contrastable y no entra en F4.
2. **Transiciones de estado** (las no listadas están prohibidas): congelado → contrastado_conforme o contrastado_desviado (con el resultado posterior registrado en su fecha y fuente); congelado → invalidado (condición de invalidación cumplida); congelado → expirado_sin_contraste (horizonte superado sin medición disponible; se conserva). Historial append-only.
3. **Correcciones.** Siempre en nueva versión referenciada a la original (regla crítica 16); la entrada original conserva sus valores, sus supuestos y su fecha de congelación. El campo `resultado_posterior` se añade, nunca se reescribe.
4. **Prohibiciones.** No se congelan probabilidades sin base metodológica declarada; no se congelan cifras sin `entry_id` del Registro de cálculos; no se registran como conocidos datos posteriores a la fecha de congelación; ningún agente distinto del Analizador escribe en el archivo.

## 5. Índice del registro y plantilla

### 5.1 Estructura del archivo

1. Índice operativo: recuento por estado, tipo de pronóstico y clase de activo; pronósticos pendientes de contraste por trimestre; fecha de última revisión.
2. Entradas por pronóstico (sección principal), en orden de congelación.
3. Registro de correcciones y reversiones (nuevas versiones referenciadas).
4. Registro de versiones del propio archivo (sección 6).

### 5.2 Índice operativo (estado de arranque)

| Campo | Valor |
|---|---|
| Versión del esquema | V1.0 |
| Entradas por estado | congelado: 0 · contrastado_conforme: 0 · contrastado_desviado: 0 · invalidado: 0 · expirado_sin_contraste: 0 |
| Entradas por tipo | Ninguna (archivo recién publicado) |
| Fecha de última revisión del índice | 2026-11-01 (publicación) |
| Carencias y prioridades | Primera congelación con la primera ejecución del Analizador bajo la óptima V2.1 de su prompt; el contraste sistemático corresponde al nivel B del circuito de aprendizaje (revisión trimestral, 9.4 del Documento 0) y, cuando se active, al Evaluador de previsiones |

### 5.3 Plantilla de entrada (ficticia)

#### PRG-2026-0001 — (plantilla — no es una entrada real)

*Identificación.* **prg_id:** PRG-2026-0001 · **trend_id:** TND-2026-0001 (plantilla de F1) · **opp_id:** OPP-2026-0001 (plantilla de F3) · **run_id:** RUN-2026-1111 · **fecha_congelacion:** 2026-11-05 · **tipo_pronostico:** umbral_de_hito · **horizonte:** 2027-06-30 · **estado:** congelado · **fecha_conocimiento:** 2026-11-05

*Contenido.* **supuestos:** los pilotos documentados mantienen su calendario y su financiación (claim_id: CLM-2026-0001, plantilla) · **escenarios:** base — crecimiento interanual del gasto en pilotos superior al 20 % a 2027-06-30; adverso — crecimiento igual o inferior al 5 % · **probabilidades:** no registradas (sin base metodológica declarada) · **valores_congelados:** ninguno (pronóstico de umbral, no de cifra) · **indicadores_seguimiento:** (1) gasto en pilotos declarado por entidades (fuente: RF-0001, frecuencia trimestral, umbral 20 %) · **condiciones_invalidez:** abandono documentado de pilotos superior al 50 % sin causa regulatoria

*Trazabilidad.* **historial_versiones:** 2026-11-05 · run_id RUN-2026-1111 · congelación inicial · **resultado_posterior:** pendiente de contraste en su fecha (todas las referencias de esta plantilla son ficticias)

## 6. Registro de versiones del archivo

| Versión | Fecha | Descripción |
|---|---|---|
| V1.0 | 01/11/2026 | Publicación inicial del archivo F4 con la óptima V3.0 del Bloque A: esquema completo (pronósticos y escenarios congelados con supuestos, indicadores, condiciones de invalidación y resultado posterior), ficha técnica de diez puntos, reglas de registro y plantilla. Archivo publicado sin entradas reales. |
