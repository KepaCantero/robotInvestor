# Registro de cálculos del Motor de Cálculo Avanzado (esquema V1.2)

**Proyecto Robot Investor · Ecosistema Robot Investor — Motor de Cálculo Avanzado para el Analizador de Tendencias de Inversión (agente de cálculo propio del Bloque A, óptima V2.0)**

**Archivo operativo · Esquema V1.1 · 01/11/2026 · Propietario único de escritura: Motor de Cálculo Avanzado para el Analizador de Tendencias de Inversión · Estado: operativo desde la publicación coordinada de la decisión de un Motor por bloque (01/11/2026); las entradas registradas bajo el esquema V1.0 conservan su formato y los campos nuevos se cumplimentan desde la entrada que abre esta versión**

Archivo publicado con la decisión del operador de un Motor de Cálculo Avanzado propio para cada bloque (01/11/2026). El Motor es el agente de cálculo propio del Bloque A desde esa fecha (registro histórico: «Motor de cálculo avanzado del Robot Investor», agente transversal activado el 23/10/2026), y este archivo es su único archivo de escritura. Se rige por el «Documento 0 — Protocolo maestro del Bloque A», versión óptima V2.1 (01/11/2026): inventario de archivos (sección 2.3), matriz de archivos (sección 4.3) y catálogo de contratos (sección 4.1, CT-11 y CT-12 en vigor). Su esquema V1.1 es conforme al prompt del Motor de Cálculo Avanzado (óptima V2.0), en particular a sus anexos D, E y F, y añade al V1.0 el bloque de ejecución interna (plan de cálculo, módulos, ficha y servicios técnicos). Ante cualquier conflicto entre este archivo y el Documento 0, prevalece el Documento 0. Las entradas registradas bajo el esquema V1.0 conservan su formato; este documento fija el esquema a partir de la entrada que abre la V1.1.

---

## 1. Propósito y alcance

### 1.1 Qué es

El «Registro de cálculos del Motor de Cálculo Avanzado» es el único archivo de escritura del Motor: registra cada servicio, rechazo, aclaración y re-ejecución con sus identificadores, su solicitante, su familia de cálculo, su método (method_id y versión), su ficha aplicada (ficha_id y versión, desde la V1.1), su módulo ejecutor (MC-XX, desde la V1.1), su plan de cálculo (plan_id y nivel, desde la V1.1), su estado final y el artefacto reproducible referenciado. Está indexado por solicitante, familia, método, módulo y fecha para que cualquier servicio pueda reconstruirse sin ayuda del Motor. Es la condición de reproducibilidad del servicio CT-11 y la base sobre la que la re-ejecución independiente CT-12 compara resultados: un cálculo que no quede registrado con su artefacto no puede auditarse.

### 1.2 Qué no es

- No es el canal de petición de cálculos: las peticiones viajan por el CT-11 y el registro anota su resultado; el archivo no recibe peticiones ni las responde.
- No es un repositorio de código de producción: referencia el artefacto reproducible (code_ref, entradas efectivas, transformaciones, semilla y política de redondeo), no lo sustituye.
- No es un archivo de resultados de negocio: conserva la salida técnica de cada cálculo; la interpretación y la integración en entregables corresponden al agente solicitante.
- No es un archivo compartido con otros bloques: desde la decisión de un Motor por bloque (01/11/2026), el Motor presta servicio al Bloque A y este archivo registra sus servicios; los demás bloques operarán sus propios motores con sus propios registros.

## 2. Ficha técnica

| Punto | Contenido |
|---|---|
| 1. Nombre, identificador y propósito | «Registro de cálculos del Motor de cálculo avanzado» (Documento 0, 2.3). Propósito: registro completo, reconstruible y auditable de cada servicio, rechazo, aclaración y re-ejecución del Motor, indexado para permitir a un tercero reconstruir cualquier cálculo sin ayuda del Motor. |
| 2. Esquema de datos y versión | Esquema V1.1 (01/11/2026), conforme al prompt del Motor óptima V2.0 (anexos D, E y F), con el bloque de ejecución interna (plan, módulos, ficha, servicios técnicos) añadido al V1.0 (31/10/2026). Los cambios de esquema se tramitan como propuesta de tipo 3 y exigen publicación coordinada. Las entradas V1.0 conservan su formato. |
| 3. Propietario único de escritura | Motor de Cálculo Avanzado para el Analizador de Tendencias de Inversión (agente propio del Bloque A, óptima V2.0). Ningún otro agente escribe en este archivo; el Documentador para el Motor lo consulta en solo lectura contextual para su función documental. |
| 4. Lectores autorizados y finalidad | Orquestador técnico y Auditor: consulta en el circuito de auditoría (matriz de archivos del Documento 0, 4.3 y Anexo E), para validar resultados, contrastar artefactos y tramitar re-ejecuciones CT-12. Agentes solicitantes: reciben su resultado por el CT-11 y su `log_entry` de registro; no editan el archivo. |
| 5. Claves e identificadores de enlace | `calculation_id` (CLC-AAAA-NNNN) como clave del registro. Enlaces salientes: `request_id` y `run_id` del solicitante; `method_id`, `method_version`, `ficha_id`, `ficha_version` y `catalog_version` del catálogo versionado; `plan_id` y `plan_level` del plan de cálculo; módulos intervinientes (MC-XX) y servicios técnicos (STC-x); `reexec_id` y `audit_id` cuando proceda (CT-12); `package_id`/`audit_id` del ciclo de auditoría que verificó el cálculo. Enlaces entrantes: los paquetes de servicio de los agentes referencian el `calculation_id`; el Historial de auditorías referencia los cálculos verificados en cada ciclo. |
| 6. Política de actualización, conservación y corrección | Append-only: cada servicio, rechazo, aclaración y re-ejecución es una entrada nueva; prohibido borrar o sobrescribir entradas; los errores se corrigen por entrada nueva referenciada a la original (R16 aplicable al registro). Conservación indefinida, sin renumeración de identificadores; la re-ejecución de un cálculo registrado abre entrada propia referenciada a la original, nunca la sustituye. |
| 7. Reglas de duplicación y resolución de conflictos | Un `request_id` con un resultado servido no se vuelve a registrar: una nueva petición idéntica abre entrada propia con su `calculation_id`. Duplicado de peticiones simultáneas del mismo solicitante: el Motor lo declara en la entrada (aclaración o rechazo por duplicidad) y registra la que sirve. Conflicto entre el resultado registrado y una re-ejecución CT-12: no se modifica la entrada original; la discrepancia se registra en la entrada de la re-ejecución con su categoría (DATOS_DISTINTOS, CONVENCION_DISTINTA, SEMILLA_DISTINTA, ERROR_IMPLEMENTACION, ERROR_REDONDEO, SIN_CAUSA_CLARA) y llega al circuito de auditoría. |
| 8. Criterios de calidad e integridad | Toda entrada con identificadores completos (calculation_id, request_id/run_id, solicitante, método, ficha aplicada cuando exista, módulos y plan desde la V1.1), parámetros con unidades explícitas, timestamps (started_at, completed_at, as_of), estado final controlado y artefacto reproducible referenciado (inputs_effective, transformaciones, semilla y política de redondeo); toda cifra con unidad y periodo; semilla registrada cuando el cálculo es estocástico, con el generador nombrado. El Orquestador y el Auditor pueden reconstruir cualquier servicio desde la entrada sin ayuda del Motor: si una entrada no lo permite, es una incidencia del propio registro. |
| 9. Contratos que lo utilizan | CT-11 «Servicio de cálculo reproducible»: el `log_entry` de cada servicio confirma el registro (recorded y entry_id). CT-12 «Re-ejecución independiente en auditoría»: la entrada de la re-ejecución referencia la original, el `audit_id` del ciclo y el contraste (tolerancia, diferencia y within_tolerance). Consumo de auditoría: el Orquestador y el Auditor consultan el archivo conforme a la matriz de archivos del Documento 0. |
| 10. Pruebas de aceptación y procedimiento de reversión | Aceptación del esquema V1.1: (i) estructura completa y sin campos de definición vacíos; (ii) la plantilla de entrada valida campo a campo contra los anexos D y E del prompt del Motor óptima V2.0; (iii) los valores controlados de modo, estado, prioridad, forma del resultado, clase de cifra y nivel de plan coinciden con el catálogo del Motor; (iv) las entradas V1.0 conservan su formato y las nuevas cumplimentan los campos V1.1. Reversión: si el operador retira esta publicación, la copia se retira con ella; las entradas ya registradas se conservan en su formato con copia de solo lectura fechada, sin renumeración de identificadores. |

## 3. Esquema de datos

Cada entrada contiene los campos siguientes. Los valores controlados son cerrados y coinciden con los del prompt del Motor (óptima V2.0, anexos D y E); su ampliación es un cambio de esquema (tipo 3). Los campos marcados como V1.1 son nuevos respecto del esquema V1.0; las entradas V1.0 conservan su formato sin ellos.

| Campo | Tipo | Obligatorio | Valores controlados / formato | Descripción |
|---|---|---|---|---|
| `calculation_id` | Identificador | Sí (inmutable) | `CLC-AAAA-NNNN` (AAAA año de registro; NNNN correlativo, sin reutilización) | Clave de la entrada; el `log_entry` del servicio la devuelve al solicitante. |
| `request_id` | Identificador | Sí | Identificador de la petición CT-11 del solicitante | Petición de origen. |
| `run_id` | Identificador | Sí | run_id de la ejecución o ciclo del solicitante | Contexto de ejecución del solicitante. |
| `agente_solicitante` | Valor controlado | Sí | Analizador de Tendencias de Inversión · Buscador de fuentes avanzadas · Documentador para el Analizador · Analista de hipótesis contrarias · Orquestador técnico · Auditor · otro agente autorizado | Cliente del servicio. Desde la V2.1 del prompt, los agentes de otros bloques no son clientes del Motor (v1.0 permitía «otro agente autorizado del ecosistema»). |
| `operacion` | Bloque estructurado | Sí | `method_id`, `method_version`, `catalog_version` del catálogo versionado, `ficha_id` y `ficha_version` cuando exista ficha publicada (V1.1), familia de cálculo y marcador `op_sin_ficha` cuando la operación opere por firma (V1.1) | Operación solicitada según el catálogo vigente del Motor. |
| `modo` | Valor controlado | Sí | SYNC_CALC · ASYNC_CALC | Modo del servicio CT-11 declarado en la petición. |
| `prioridad` | Valor controlado | Sí | INTEGRIDAD · MATERIAL · ORDEN_LLEGADA | Prioridad de la petición. |
| `ejecucion_interna` | Bloque estructurado (V1.1) | Sí en entradas V1.1 | `plan_id`; `plan_level` (PLAN_MIN · PLAN_STD · PLAN_EXT); `modulos` (códigos MC-01 a MC-08 y los que el operador incorpore); `servicios_tecnicos` (STC-1 a STC-4); `opciones_plan` cuando existan | Trazabilidad de la arquitectura modular: plan proporcional, módulos intervinientes y servicios técnicos usados (conforme a la sección 15 y al Anexo J del prompt del Motor). |
| `parametros` | Lista estructurada | Sí | Cada parámetro con nombre, valor y unidad explícita (por ejemplo, «porcentaje», «millones de euros», «años») | Parámetros efectivos del cálculo, con unidades. |
| `started_at` / `completed_at` / `as_of` | Timestamps | Sí | ISO 8601 con huso declarado | Inicio y fin del servicio; corte temporal de los datos usados (as_of). |
| `estado` | Valor controlado | Sí | SERVED · SERVED_WITH_LIMITATIONS · CLARIFICATION_NEEDED · REJECTED · FAILED | Estado final del servicio; los rechazos y aclaraciones se registran como entrada completa. |
| `resultado` | Bloque estructurado | Sí en SERVED y SERVED_WITH_LIMITATIONS | `form`: VALOR · TABLA · SERIE · DISTRIBUCION; `figure_class`: DETERMINISTA · ESTADISTICA (V1.1); `payload` con las cifras; `units` con las unidades de cada magnitud | Salida del cálculo; en CLARIFICATION_NEEDED y REJECTED se registra el motivo; en FAILED, el punto de fallo. |
| `artefacto_reproducible` | Bloque estructurado | Sí | `method_id` y `method_version`; `ficha_id` y `ficha_version` cuando exista; `code_ref`; `inputs_effective`; `transformations`; `seed` (null o entero registrado); `generator` (nombre del generador cuando seed no es null); `rounding_policy`; `data_quality_report` | Artefacto que permite reconstruir el cálculo sin ayuda del Motor. |
| `verificacion_interna` | Bloque estructurado | Sí | `identity_checks` (comprobaciones de identidad ejecutadas) y `second_path` (segunda vía, cuando proceda); `verificacion_integracion` del Orquestador de Cálculo en planes multietapa (V1.1) | Verificación determinista interna del Motor (doble revisión del módulo ejecutor e integración del plan). |
| `limitaciones` / `incidencias` | Listas de texto | Sí | Declaración expresa; «ninguna» solo con motivo | Limitaciones del servicio e incidencias técnicas. |
| `re_ejecucion_ct12` | Bloque estructurado | No | `reexec_id`; `audit_id` del ciclo cuando proceda; `requested_by` (Orquestador o Auditor que la formuló); `original_request_id`; `isolation`: CONFIRMED; `modulos`: ["MC-08"] (V1.1); `comparison` con `tolerance`, `difference` y `within_tolerance` (true · false · null solo con el estado declarado que lo justifique); `discrepancies` con categoría controlada (DATOS_DISTINTOS · CONVENCION_DISTINTA · SEMILLA_DISTINTA · ERROR_IMPLEMENTACION · ERROR_REDONDEO · SIN_CAUSA_CLARA), magnitud y evidencia; `status`: COMPLETED · COMPLETED_WITH_LIMITATIONS · FAILED | Vínculo con la re-ejecución independiente CT-12; se registra como entrada propia referenciada a la original y anota aquí su contraste. La re-ejecución la ejecuta el módulo MC-08. |
| `trazabilidad_auditoria` | Bloque estructurado | No | `audit_id` y `package_id` del ciclo que verificó el cálculo; `finding_id` si un hallazgo lo afecta | Referencia al circuito de auditoría (CT-03 a CT-10) que consumió la entrada. |

## 3-bis. Perfil aplicado, estados de madurez e idempotencia (añadidos con la óptima V3.0)

Con la óptima V3.0 del Documento 0 y del prompt del Motor, cada entrada del Registro declara
además:

| Campo | Valores controlados / formato | Descripción |
|---|---|---|
| `perfil_aplicable` | PERF-xx · TRANSVERSAL · MIX (lista de perfiles combinados) | Perfil o perfiles de clase de activo aplicados al servicio (documento «Perfiles de clase de activo del Motor», V1.0); TRANSVERSAL cuando el cálculo no depende de la clase. En los activos híbridos, la lista declarada de perfiles combinados. |
| `estado_madurez_metodo` | DOCUMENTADO · IMPLEMENTADO · VALIDADO | Estado de madurez del método o de la ficha aplicada en el momento del servicio (regla crítica 19 del Documento 0); la respuesta CT-11 lo replica. |
| `clave_idempotencia` | Cadena derivada de (solicitante, operación, parámetros, datos, versiones) | Clave de detección de peticiones duplicadas (idempotencia, 4.4 del prompt del Motor); la reemisión devuelve el artefacto registrado. |

Las entradas registradas bajo los esquemas V1.0 y V1.1 conservan su formato; los campos nuevos
se cumplimentan desde la entrada siguiente a la publicación de la óptima V3.0.

## 4. Reglas de registro

### 4.1 Altas

1. Cada servicio CT-11 se registra al cerrarse, con `calculation_id` propio, cualquiera que sea su estado: servido, servido con limitaciones, con aclaración pendiente, rechazado o fallido. Un rechazo o una petición de aclaración son entradas completas, no omisiones.
2. El `log_entry` devuelto al solicitante confirma el registro (recorded y entry_id); el Motor no declara registrado nada sin comprobación real del registro.
3. Cada re-ejecución CT-12 abre entrada propia con `reexec_id`, referencia a la entrada original, `audit_id` del ciclo cuando proceda, aislamiento confirmado y MC-08 como módulo ejecutor.

### 4.2 Cambios

1. Los estados finales son cerrados: un cambio posterior de estado (por ejemplo, un servicio fallido reintentado) abre entrada nueva referenciada a la original; la original conserva su estado y su fecha.
2. Las discrepancias detectadas por una re-ejecución no alteran la entrada original: se registran en la entrada de la re-ejecución con su categoría, magnitud y evidencia, y llegan al circuito de auditoría por el canal del ciclo correspondiente.
3. La cola de cálculos ASYNC_CALC se gestiona por prioridad (INTEGRIDAD, MATERIAL, ORDEN_LLEGADA); el registro anota la prioridad declarada, no la posición relativa de la cola.
4. (V1.1) El bloque `ejecucion_interna` se registra con el plan y los módulos efectivos, no con los previstos: un módulo invitado por el plan (módulo_invitado) se declara con su motivo; una operación sin ficha se marca con `op_sin_ficha` y la versión de firma aplicada.

### 4.3 Correcciones

1. Toda corrección es una entrada nueva con fecha, motivo y referencia a la entrada original (R16); prohibido editar o borrar entradas.
2. Si una corrección afecta a un resultado ya consumido por un entregable, el Motor lo declara en la entrada de corrección para que el circuito de auditoría valore el alcance; el Motor no corrige entregables ajenos.
3. Los identificadores no se renumeran ni se reutilizan, tampoco tras una reversión parcial del servicio.

## 5. Índice del registro y plantilla de entrada

### 5.1 Estructura del archivo

El archivo se compone de cinco secciones, en este orden:

1. Índice operativo del registro: entradas por solicitante, por familia de cálculo, por módulo ejecutor y por periodo; estados finales del periodo; re-ejecuciones CT-12 con su resultado de contraste; incidencias abiertas; fecha de última revisión del índice.
2. Entradas de cálculo (sección principal): una entrada por `calculation_id`, en orden de registro, con sus parámetros, su plan y sus módulos, su artefacto reproducible y su estado final.
3. Entradas de re-ejecución CT-12: entradas propias referenciadas a la original, con su contraste.
4. Registro de correcciones: entradas de corrección referenciadas a la entrada original.
5. Registro de versiones del propio archivo (sección 6).

### 5.2 Índice operativo (estado de arranque del esquema V1.1)

| Campo | Valor |
|---|---|
| Versión del esquema | V1.1 |
| Entradas bajo el esquema V1.1 | Ninguna en la fecha de publicación; la primera entrada posterior a la publicación abre la serie V1.1 |
| Entradas heredadas bajo el esquema V1.0 | Las que el servicio haya registrado hasta la fecha; conservan su formato (sin bloque `ejecucion_interna`) |
| Entradas por solicitante | Conforme al índice operativo vivo del archivo |
| Entradas por familia de cálculo | Conforme al índice operativo vivo del archivo |
| Re-ejecuciones CT-12 registradas | Conforme al índice operativo vivo del archivo |
| Incidencias abiertas | Conforme al índice operativo vivo del archivo |
| Fecha de última revisión del índice | 2026-11-01 (publicación del esquema V1.1) |
| Estado de la serie | La serie continúa: las entradas V1.0 conservan su formato y la primera entrada posterior a la publicación abre la serie V1.1 |

### 5.3 Plantilla de entrada de cálculo (esquema V1.1)

La entrada siguiente es un ejemplo ficticio que muestra el formato de ficha: **(plantilla — no es una entrada real)**. Ningún dato de esta plantilla corresponde a un servicio real; los identificadores de ejemplo no se reutilizan.

#### CLC-2026-0001 — (plantilla — no es una entrada real)

*Identificación.* **calculation_id:** CLC-2026-0001 · **request_id:** REQ-2026-1110 (plantilla) · **run_id:** RUN-2026-1110 (plantilla) · **agente_solicitante:** Analizador de Tendencias de Inversión · **operacion:** method_id MET-EJEMPLO-001, method_version 1.0, catalog_version 2.0, ficha_id FX-EJEMPLO-001, ficha_version 1.0, familia: series temporales de ejemplo · **modo:** SYNC_CALC · **prioridad:** MATERIAL

*Ejecución interna (V1.1).* **plan_id:** PLAN-2026-1110 · **plan_level:** PLAN_MIN · **modulos:** [MC-02] · **servicios_tecnicos:** [STC-1, STC-2, STC-3, STC-4] · **opciones_plan:** ninguna

*Parámetros y tiempos.* **parametros:** ventana de observación: 36 meses; frecuencia: mensual; moneda de la serie: índice del tipo de cambio, base declarada · **started_at:** 2026-11-05T09:14:00+01:00 · **completed_at:** 2026-11-05T09:14:41+01:00 · **as_of:** 2026-10-31

*Resultado y artefacto.* **estado:** SERVED · **resultado:** form TABLA; figure_class ESTADISTICA; payload: pendiente de tendencia con su intervalo de confianza (plantilla); units: unidades del índice por mes · **artefacto_reproducible:** method_id MET-EJEMPLO-001, method_version 1.0, ficha_id FX-EJEMPLO-001 v1.0; code_ref: referencia de plantilla; inputs_effective: serie de entrada de plantilla con su fuente y vintage; transformations: alineación de frecuencia de plantilla; seed: null (cálculo determinista); generator: no aplicable; rounding_policy: cuatro decimales, redondeo de banquero; data_quality_report: sin lagunas de plantilla · **verificacion_interna:** identity_checks ejecutadas (identidad de la ficha aplicada), segunda vía aplicada en cálculo crítico de plantilla; verificacion_integracion: no aplicable (operación única)

*Re-ejecución y trazabilidad.* **re_ejecucion_ct12:** no procede en esta entrada (plantilla sin re-ejecución; una re-ejecución real abriría entrada propia con reexec_id, audit_id, isolation CONFIRMED, modulos [MC-08] y su comparison) · **trazabilidad_auditoria:** audit_id AUD-2026-0001 (plantilla del Historial de auditorías), package_id PKG-2026-0001 · todos los identificadores y datos de esta plantilla son ficticios

## 6. Registro de versiones del archivo

| Versión | Fecha | Descripción |
|---|---|---|
| V1.2 | 01/11/2026 | Ampliación del esquema aplicada con la óptima V3.0: campos nuevos `perfil_aplicable` (perfiles PERF-xx del Catálogo de perfiles), `estado_madurez_metodo` (regla crítica 19) y `clave_idempotencia` (detección de duplicados); las entradas de esquemas anteriores conservan su formato. |
| V1.1 | 01/11/2026 | Esquema V1.1, publicado con la decisión del operador de un Motor por bloque y con la óptima V2.0 del prompt del Motor (arquitectura modular). Añade al V1.0: campo `ejecucion_interna` (plan_id, plan_level PLAN_MIN/PLAN_STD/PLAN_EXT, módulos MC-XX, servicios técnicos STC-x) como trazabilidad de la arquitectura modular; ficha aplicada (ficha_id, ficha_version y marcador op_sin_ficha) en `operacion` y en el artefacto; `figure_class` (DETERMINISTA/ESTADISTICA) en el resultado; `verificacion_integracion` del Orquestador de Cálculo en planes multietapa; módulo ejecutor MC-08 en las re-ejecuciones CT-12; regla 4.2.4 (plan y módulos efectivos, módulo_invitado, op_sin_ficha). Ajuste del alcance del campo `agente_solicitante` (clientes del Bloque A). Las entradas registradas bajo el esquema V1.0 conservan su formato; la primera entrada posterior a la publicación abre la serie V1.1. Propietario y matriz de acceso sin cambios. |
| V1.0 | 31/10/2026 | Publicación inicial del archivo como semilla con la óptima V2.0 del Bloque A: esquema V1.0 conforme al prompt del Motor óptima V1.4 (anexos D y F), ficha técnica de diez puntos, campos de servicio CT-11 con artefacto reproducible y vínculo CT-12 con la re-ejecución independiente, índice de arranque y plantilla de entrada. Semilla con cero entradas; el primer servicio posterior abrió la serie. Archivo compartido del ecosistema en su fecha; desde la decisión de un Motor por bloque (01/11/2026), registro propio del Motor de Cálculo Avanzado del Bloque A. |
