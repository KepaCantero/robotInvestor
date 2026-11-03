# Historial de auditorías (esquema V1.1)

**Proyecto Robot Investor · Bloque A — Orquestador técnico**

**Archivo operativo semilla · Esquema V1.0 · 31/10/2026 · Propietario único de escritura: Orquestador técnico · Estado: operativo desde la publicación coordinada de la óptima V2.0 (31/10/2026); semilla con cero entradas**

Archivo semilla creado por la óptima V2.0 del Bloque A. Se rige por el «Documento 0 — Protocolo maestro del Bloque A», versión óptima V2.0 (31/10/2026): inventario de archivos (sección 2.3), circuito de auditoría asíncrona (sección 2.7, fase 09), matriz de archivos (sección 4.3) y matriz RACI del mantenimiento del Historial (sección 3.2). Su esquema es conforme a la sección 9 del prompt del Orquestador técnico (versión óptima V2.0, 31/10/2026). Ante cualquier conflicto entre este archivo y el Documento 0, prevalece el Documento 0. El archivo se publica con cero entradas: contiene su estructura completa, sus reglas y una única plantilla de entrada claramente marcada como plantilla; la primera auditoría posterior a la activación de la óptima V2.0 abrirá la serie.

---

## 1. Propósito y alcance

### 1.1 Qué es

El «Historial de auditorías» (nombre canónico en el Documento 0, 2.3: «Historial de auditorías para tendencias de inversión») es el registro de los ciclos de auditoría del Bloque A: paquetes recibidos, validaciones y comprobaciones deterministas del Orquestador, coordinación con el Auditor, hallazgos consolidados con su severidad y tipo, propuestas clasificadas, guías de mejora emitidas, muestras de revisión humana preparadas, incidencias y estados finales de cada ciclo. Alimenta la guía de mejora, las comparaciones antes y después, el índice de defectos recurrentes por agente y el informe periódico al operador. Es el único archivo de escritura del Orquestador técnico.

### 1.2 Qué no es

- No es el canal de hallazgos del Auditor: el Auditor entrega sus hallazgos al Orquestador a través de su canal técnico (CT-10 de coordinación y calibración), y es el Orquestador quien los consolida y registra; el Auditor no escribe en este archivo.
- No es un instrumento en línea: la auditoría es asíncrona y nunca bloquea el servicio (regla crítica 14); un hallazgo no reabre una ejecución cerrada salvo escalado del operador (R14).
- No es un repositorio de paquetes: se registran referencias y resúmenes, no copias íntegras (salvo política de retención distinta del operador).
- No es un registro de credenciales ni de datos del inversor: si llegaran en un paquete, se aíslan y se declara la incidencia registrando solo su existencia, sin el contenido.
- No es un archivo de opiniones: cada entrada debe permitir reconstruir la auditoría por quien audite la auditoría; no se registra por mera cantidad.

## 2. Ficha técnica

| Punto | Contenido |
|---|---|
| 1. Nombre, identificador y propósito | «Historial de auditorías para tendencias de inversión» (Documento 0, 2.3). Propósito: registro completo y reconstruible de los ciclos de auditoría, base de la guía de mejora, de las comparaciones entre periodos y del informe periódico al operador. |
| 2. Esquema de datos y versión | Esquema V1.0, conforme a la sección 9 del prompt del Orquestador técnico óptima V2.0, publicado con la óptima V2.0 (31/10/2026). Los cambios de esquema se tramitan como propuesta de tipo 3 y exigen publicación coordinada. |
| 3. Propietario único de escritura | Orquestador técnico. Ningún otro agente escribe en este archivo. |
| 4. Lectores autorizados y finalidad | Auditor: consulta de entradas y comparaciones para su revisión y su calibración (CT-10). Los agentes auditados no leen el Historial: reciben su transmisión conforme al contrato del Anexo F del prompt del Orquestador (confirmación, validación, hallazgos, guía y propuestas de tipo 3). El operador recibe el informe periódico. |
| 5. Claves e identificadores de enlace | `audit_id` (AUD-AAAA-NNNN) como clave del ciclo; `package_id` del paquete auditado; `run_id` y `request_id` de la ejecución o servicio auditado; `finding_id` de cada hallazgo consolidado; `guide_id` y versión de cada guía emitida; `sample_id` de cada muestra de revisión humana; `reexec_id` cuando el ciclo incluye una re-ejecución CT-12. Enlaces salientes: versiones de prompts y guías en juego; referencias a las entradas del Registro de cálculos del Motor (`calculation_id`) cuando el ciclo las verifique. Enlaces entrantes: los agentes auditados registran el `audit_id` en su `audit_status`; el informe periódico cita `audit_id`. |
| 6. Política de actualización, conservación y corrección | Append-only: cada ciclo y cada corrección o cambio de estado es una entrada nueva con fecha y motivo; prohibido borrar o sobrescribir entradas; la disciplina es leer antes de escribir, comprobar duplicados, añadir y releer para confirmar el registro. Corrección de un error del propio proceso de auditoría (falso positivo, reclasificación incorrecta, guía con ítem defectuoso): entrada nueva que referencia la original, comunicación al agente afectado y al operador; la entrada original no se altera. Conservación indefinida; sin renumeración de identificadores. |
| 7. Reglas de duplicación y resolución de conflictos | Antes de abrir una entrada, el Orquestador comprueba si el paquete ya tiene `audit_id` asignado (un paquete, un ciclo; reanudaciones con el mismo `audit_id` y anotación de la reanudación). Discrepancia entre el contraste del Orquestador y el hallazgo del Auditor: no se promedia ni se silencia; se documentan las dos posiciones con su evidencia y la comprobación adicional que la resolvería; si persiste, ambas posiciones quedan registradas y llegan al proceso de clasificación y al informe del operador con su mapa completo. Duplicado de hallazgos del mismo origen en ciclos distintos: se registran como refuerzo de hallazgo previo con referencia a su `finding_id`. |
| 8. Criterios de calidad e integridad | Toda entrada con los campos mínimos de la sección 9.2 del prompt del Orquestador (identificadores, fechas, versiones en juego, resultado de la validación, comprobaciones deterministas, coordinación con el Auditor, hallazgos consolidados, propuestas con tipo y estado, guía emitida, muestra, incidencias y estados finales); sin ellos la entrada no se considera completa. Severidad siempre con justificación (severidad sin motivo es opinión, no auditoría); severidad y alcance declarados por separado; estados reales, sin declarar recepciones, comprobaciones ni envíos sin comprobación real. El Orquestador declara qué comprobaciones omitió y qué partes del paquete quedaron sin cubrir. |
| 9. Contratos que lo utilizan | CT-03 (paquete de auditoría del Analizador): entrada del ciclo con su `gates_record`, `coverage_statement`, `objections_ledger`, `evidence_root_summary` y bloque de reconstrucción de puntuaciones. CT-04 (paquete de auditoría de los agentes de fuente). CT-05/CT-06 (paquetes de servicio del Documentador y del Buscador avanzado). CT-07/CT-08 (revisión experta: material con evidencias y pruebas deterministas antes que conclusiones). CT-09 (guías para agentes de apoyo: la guía emitida se registra aquí). CT-10 (coordinación y calibración Orquestador–Auditor: discrepancias, ajustes de severidad, puntos ciegos). CT-12 (re-ejecución independiente: el `reexec_id` y su contraste quedan referenciados en el ciclo). |
| 10. Pruebas de aceptación y procedimiento de reversión | Aceptación del esquema: (i) estructura completa y sin campos de definición vacíos; (ii) la plantilla de entrada valida campo a campo contra el esquema de la sección 3; (iii) las escalas de severidad y tipo y los cuatro estados finales coinciden con el prompt del Orquestador óptima V2.0; (iv) cero entradas reales en la fecha de publicación. Reversión: si el operador retira la óptima V2.0, la versión de esquema se retira con ella; al ser una semilla sin entradas, la reversión se limita a retirar la copia publicada; si la primera auditoría ya abrió la serie, se conserva copia de solo lectura fechada antes de la reversión, sin renumeración, para no perder evidencia del sistema. |

## 3. Esquema de datos

Cada entrada de auditoría contiene los campos siguientes. Los valores controlados son cerrados; su ampliación es un cambio de esquema (tipo 3).

| Campo | Tipo | Obligatorio | Valores controlados / formato | Descripción |
|---|---|---|---|---|
| `audit_id` | Identificador | Sí (inmutable) | `AUD-AAAA-NNNN` (AAAA año del ciclo; NNNN correlativo, sin reutilización) | Clave del ciclo de auditoría; compartido con las reanudaciones del mismo ciclo. |
| `package_id` | Identificador | Sí | Identificador del paquete recibido según el contrato de origen | Paquete auditado. |
| `run_id` / `request_id` | Identificadores | Sí | Identificadores de la ejecución o servicio auditado | Trazabilidad hacia la ejecución de origen. |
| `agente_auditado` | Valor controlado | Sí | Analizador de Tendencias de Inversión · Buscador de fuentes avanzadas · Documentador para el Analizador · Analista de hipótesis contrarias · Orquestador técnico · Auditor | Agente de origen del paquete. |
| `modo_ejecucion` | Valor controlado | Sí | WEEKLY_AUTONOMOUS · BROKER_REQUEST · ALERT_CHECK · ADV_SEARCH · DOC_MAINTENANCE · GUIDE_MAINTENANCE · otro modo declarado del prompt del agente | Ejecución o servicio auditado. |
| `fecha_recepcion` / `fecha_cierre` | Fechas | Sí | ISO 8601 | Recepción del paquete y cierre del ciclo. |
| `versiones_en_juego` | Bloque estructurado | Sí | Prompt y metodología del Orquestador; prompt del agente auditado; guía de mejora vigente que este tenía aplicada | Versiones al tiempo del ciclo. |
| `resultado_validacion` | Texto estructurado | Sí | Comprobaciones realizadas y omitidas, con su resultado | Validación formal del paquete. |
| `comprobaciones_deterministas` | Lista estructurada | Sí | Cada comprobación con: grupo de control (integridad estructural · integridad de datos · integridad metodológica · integridad de las conclusiones · seguimiento de incidencias), prueba aplicada y resultado | Comprobaciones deterministas del Orquestador, incluido el contraste de referencias cruzadas F1/F2 y el cómputo de raíces del `evidence_root_summary`. |
| `coordinacion_auditor` | Bloque estructurado | Sí | Material enviado (CT-07/CT-08, en el orden declarado: evidencias y pruebas deterministas antes que conclusiones); hallazgos recibidos; discrepancias; ajustes de severidad transmitidos como calibración; declaración de puntos ciegos recibida | Coordinación Orquestador–Auditor (CT-10). |
| `hallazgos_consolidados` | Lista estructurada | Sí (puede declararse «sin hallazgos», que es un resultado válido) | Cada hallazgo con: `finding_id`, severidad, tipo, alcance, descripción, evidencia y estado | Hallazgos consolidados; severidad: Crítica · Material · Operativa · Menor; tipo: 1 (corrección de errores de una ejecución o servicio concreto) · 2 (mejora operativa dentro del marco vigente) · 3 (cambio de metodología, esquema, contrato, topología o prompt; nunca se aplica sin aprobación del operador). |
| `severidad` | Valor controlado por hallazgo | Sí | Crítica · Material · Operativa · Menor, con su justificación y su alcance | Crítica: evidencia fabricada o citación inexistente; infracción de seguridad; conclusión central incompatible con sus datos; manipulación u ocultación de conflicto de interés. Severidad no es alcance: una Crítica localizable puede aislar una afirmación sin invalidar todo el informe. |
| `estado_hallazgo` | Valor controlado por hallazgo | Sí | abierto · transmitido · corregido · reclasificado · cerrado sin acción (con motivo) | Estado y resolución de cada hallazgo; los cambios de estado son entradas nuevas con fecha. |
| `propuestas` | Lista estructurada | Sí | Cada propuesta con: tipo (1 · 2 · 3), instrucción accionable y estado (PENDING_OPERATOR · REJECTED · APPLIED) | Propuestas clasificadas; las de tipo 3 esperan la decisión del operador en la cola de pendientes. |
| `guia_emitida` | Bloque estructurado | No | `guide_id`, versión, ítems contenidos, versión sustituida y fecha de aplicación | Guía de mejora emitida con propuestas de tipo 1 y 2 confirmadas; «no emitida» si no procede. |
| `muestra_revision_humana` | Bloque estructurado | No | `sample_id`, criterio de selección, envío al Auditor y resultado cuando exista | Muestra preparada para calibración (CT-10). |
| `incidencias` | Lista estructurada | No | Cada incidencia con: descripción (sin credenciales ni datos del inversor), afectación y tratamiento | Incidencias del ciclo, incluidas las de registro o envío. |
| `estados_finales` | Bloque estructurado | Sí | `audit_process_status`: COMPLETED · COMPLETED_WITH_LIMITATIONS · FAILED; `guidance_status`: ISSUED · SUPERSEDED · NONE; `delivery_status`: CONFIRMED · PENDING · ATTEMPTED · FAILED; `operator_report_status`: SENT · PENDING · FAILED | Cuatro estados separados; un envío fallido no convierte el ciclo en exitoso ni al revés. |
| `trazabilidad_contratos` | Lista de códigos | Sí | CT-03 · CT-04 · CT-05 · CT-06 · CT-07 · CT-08 · CT-09 · CT-10 (y CT-12 cuando el ciclo incluye re-ejecución) | Contratos empleados en el ciclo, con referencia al campo o anexo de cada uno. |

## 3-bis. Tipo de control y clase de resultado (añadidos con la óptima V3.0)

Con la óptima V3.0 del Documento 0 (regla crítica 22), cada ciclo o validación registrada
declara además:

| Campo | Valores controlados | Descripción |
|---|---|---|
| `tipo_control` | SINCRONO_DETERMINISTA · ASINCRONO | Naturaleza del control: validación técnica determinista previa a la entrega (puerta G3 y comprobaciones del Orquestador) o revisión metodológica y auditoría posterior (CT-03 a CT-10). Una revisión asíncrona no se registra nunca como condición previa de entrega. |
| `clase_resultado` | BLOQUEANTE · ADVERTENCIA · PROVISIONAL | Clase del resultado del control: bloqueante (impide presentar el resultado como válido hasta su corrección), advertencia (permite la entrega con limitación declarada) o provisional (resultado provisional con su etiqueta y condición de revisión). |

Las entradas registradas bajo el esquema V1.0 conservan su formato; los campos nuevos se
cumplimentan desde la entrada siguiente a la publicación de la óptima V3.0.

## 4. Reglas de registro

### 4.1 Altas

1. Cada paquete recibido abre un ciclo con `audit_id` propio; la entrada se registra al cierre del ciclo y las reanudaciones se anotan en la misma entrada con su fecha y motivo.
2. La entrada se considera completa solo con los campos mínimos de la sección 9.2 del prompt del Orquestador; una entrada incompleta es una incidencia del propio proceso de auditoría y se corrige por entrada nueva.
3. El material enviado al Auditor por CT-07/CT-08 se prepara con las evidencias y las pruebas deterministas antes que las conclusiones; la entrada registra que el material se preparó en ese orden.

### 4.2 Cambios

1. Los cambios de estado de hallazgos, propuestas y envíos son entradas nuevas con fecha y motivo; la entrada original no se altera.
2. La cola de pendientes de tipo 3 se recuenta en cada consolidación y en cada informe: ningún pendiente se pierde entre ciclos; si el operador no ha decidido, sigue en la cola con su antigüedad y su decisión solicitada (PENDING_OPERATOR).
3. Las decisiones del operador sobre pendientes de tipo 3 se registran como entradas nuevas con su fecha, su referencia y la propagación realizada (documentos, guías y agentes afectados).

### 4.3 Correcciones y estados

1. Si tras el cierre se descubre un error del proceso de auditoría (falso positivo transmitido, reclasificación incorrecta, guía con un ítem defectuoso), la corrección es una entrada nueva que referencia la original, con comunicación al agente afectado y al operador.
2. Los cuatro estados finales se declaran por separado y con comprobación real: el proceso puede completarse con un envío fallido o un registro pendiente; la incidencia se declara en el estado correspondiente y en la transmisión al agente.
3. Un ciclo sin hallazgos es un resultado válido si el sistema funcionó; no se infla la lista de hallazgos para justificar la actividad, y no son hallazgos la laguna declarada con transparencia, el resultado desfavorable sin error de procedimiento ni la decisión del agente dentro de su margen.

## 5. Índice del registro y plantilla de entrada

### 5.1 Estructura del archivo

El archivo se compone de cinco secciones, en este orden:

1. Índice operativo del Historial: entradas por agente y periodo, hallazgos por severidad y tipo, guías vigentes, cola de pendientes de tipo 3 con su antigüedad y comparaciones antes y después disponibles.
2. Entradas de auditoría (sección principal): una entrada por `audit_id`, en orden de ciclo.
3. Índice de guías de mejora vigentes: registro por agente (versión aplicada, fecha desde la que aplica, ítems contenidos, versión sustituida) y su ciclo de mantenimiento (GUIDE_MAINTENANCE: consolidación de periodos, actualización del índice, refresco de comparaciones y depuración de la cola).
4. Registro de correcciones del Historial: entradas de corrección referenciadas a la entrada original.
5. Registro de versiones del propio archivo (sección 6).

### 5.2 Índice operativo (estado de arranque)

| Campo | Valor |
|---|---|
| Versión del esquema | V1.0 |
| Entradas por agente auditado | Ninguna (semilla sin entradas) |
| Hallazgos por severidad | Crítica: 0 · Material: 0 · Operativa: 0 · Menor: 0 |
| Hallazgos por tipo | Tipo 1: 0 · Tipo 2: 0 · Tipo 3: 0 |
| Comparaciones antes y después disponibles | Ninguna |
| Fecha de última revisión del índice | 2026-10-31 (publicación) |
| Estado de la serie | Sin entradas en la fecha de publicación; la primera auditoría posterior a la activación de la óptima V2.0 abrirá la serie |

### 5.3 Índice de guías de mejora vigentes (estado de arranque) y su ciclo

| Agente auditado | Guía vigente | Versión aplicada | Desde | Ítems | Sustituye a |
|---|---|---|---|---|---|
| (vacío — sin guías emitidas en la fecha de publicación; la primera guía se registrará con el ciclo que la emita) | --- | --- | --- | --- | --- |

Ciclo de las guías: las propuestas de tipo 1 y 2 confirmadas se integran en una guía versionada con instrucción accionable (qué cambia, dónde se comprueba y cómo se sabe que se aplicó) y fecha de aplicación desde la que el agente la registra en sus ejecuciones; cada guía nueva sustituye a la anterior (guidance_status: SUPERSEDED) sin borrarla. En GUIDE_MAINTENANCE el Orquestador consolida periodos, actualiza este índice, refresca las comparaciones antes y después y depura la cola de pendientes de tipo 3; sin planificador real de ciclos, el calendario se formula como recomendación al operador, sin afirmar que está programado.

### 5.4 Plantilla de entrada de auditoría

La entrada siguiente es un ejemplo ficticio que muestra el formato de ficha: **(plantilla — no es una entrada real)**. Ningún dato de esta plantilla describe una auditoría realizada; los identificadores de ejemplo no se reutilizan.

#### AUD-2026-0001 — (plantilla — no es una entrada real)

*Identificación.* **audit_id:** AUD-2026-0001 · **package_id:** PKG-2026-0001 (plantilla) · **run_id / request_id:** RUN-2026-1110 / REQ-2026-1110 (plantilla) · **agente_auditado:** Analizador de Tendencias de Inversión · **modo_ejecucion:** WEEKLY_AUTONOMOUS · **fecha_recepcion:** 2026-11-05 · **fecha_cierre:** 2026-11-07 · **versiones_en_juego:** Orquestador óptima V2.0; Analizador óptima V2.0; guía vigente del agente: ninguna (primera auditoría de la serie)

*Validación y comprobaciones.* **resultado_validacion:** paquete completo; sin campos obligatorios ausentes · **comprobaciones_deterministas:** (1) integridad de datos: referencias cruzadas F1/F2 válidas, sin identificadores rotos; (2) integridad metodológica: puntuaciones E/T/M reconstruidas desde su desglose, concordantes; (3) integridad de las conclusiones: `evidence_root_summary` contrastado con F2, cuenta de raíces conforme; todas con resultado conforme (plantilla)

*Coordinación y hallazgos.* **coordinacion_auditor:** material CT-07 enviado con evidencias y pruebas deterministas antes que conclusiones; un hallazgo recibido; sin discrepancias; sin ajustes de severidad; sin declaración de puntos ciegos pendiente (plantilla) · **hallazgos_consolidados:** FRG-2026-0001 (plantilla): extrapolación fuera del periodo observado en una afirmación del informe; severidad: Operativa, con justificación y alcance localizado a la afirmación; tipo: 1 · **estado_hallazgo:** transmitido · **propuestas:** tipo 1, instrucción accionable de plantilla, estado APPLIED · **guia_emitida:** no emitida (propuesta integrada en la transmisión) · **muestra_revision_humana:** no preparada en este ciclo · **incidencias:** ninguna

*Estados y trazabilidad.* **estados_finales:** audit_process_status COMPLETED · guidance_status NONE · delivery_status CONFIRMED · operator_report_status SENT · **trazabilidad_contratos:** CT-03, CT-07, CT-10 (plantilla)

## 6. Registro de versiones del archivo

| Versión | Fecha | Descripción |
|---|---|---|
| V1.1 | 01/11/2026 | Ampliación del esquema aplicada con la óptima V3.0: campos nuevos `tipo_control` (síncrono determinista / asíncrono) y `clase_resultado` (bloqueante, advertencia, provisional) conforme a la regla crítica 22; las entradas V1.0 conservan su formato. |
| V1.0 | 31/10/2026 | Publicación inicial del archivo como semilla con la óptima V2.0 del Bloque A: esquema V1.0 conforme a la sección 9 del prompt del Orquestador técnico, ficha técnica de diez puntos, escalas de severidad (Crítica, Material, Operativa, Menor) y de tipo (1, 2, 3), estados finales separados, índice de arranque, índice de guías de mejora vacío con su ciclo y plantilla de entrada. Cero entradas: la primera auditoría posterior a la activación de la óptima V2.0 abrirá la serie. |
