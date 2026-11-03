# Listado exhaustivo de funciones, tareas y cometidos — Motor de Cálculo Avanzado para el Analizador de Mercados (Bloque B)

VERSIÓN ÓPTIMA V1.2 · Listado exhaustivo de funciones, tareas y cometidos del Motor de Cálculo Avanzado para el Analizador de Mercados (papel del agente respecto del Bloque B) · Edición V1.2 (31/10/2026): conserva íntegro el desarrollo de la V1.1 (que integra y absorbe la ficha del agente y el suplemento del carril B, con las series MOT-B-T del listado V1 del ecosistema y MOT-B-SB del carril B) y añade la sección de ampliación con las tareas del mapa de conocimiento cuantitativo (prompt óptima V1.3) y la corrección de referencias de versión (óptima V1.4) · Redactado contra el «System prompt --- Motor de Cálculo Avanzado del Robot Investor» (óptima V1.4, 31/10/2026), el «Documento 0 --- Protocolo maestro del Bloque B» (óptima V1.3, 31/10/2026, estado consolidado), las dos adendas de arquitectura del bloque (30/10 y 31/10/2026) y la adenda ligera del carril B · Documento de consulta del operador, sin carácter normativo: mandan el Documento 0-B, el Documento 0 del Bloque A y el system prompt del servicio · es-ES

> **Qué es este documento.** El inventario completo del Motor en el ecosistema es su «Listado de funciones, tareas y cometidos del Motor de cálculo avanzado» (V1: 21 bloques, 249 tareas), vigente como documento del ecosistema desde el 22/10/2026 y citado por el Documento 0-B (2.2) y por el propio prompt del agente. Este documento completa ese inventario con el papel del agente respecto del Bloque B: la ficha de identidad, su posición en la arquitectura del bloque, las 23 funciones MOT-B-F01 a F23, su ciclo operativo, sus contratos, archivos, límites y su relación con los objetivos del bloque (secciones 1 a 11), y el desglose exhaustivo en tareas del carril B con serie propia MOT-B-SB (sección 12). El carril B entra en vigor con la publicación coordinada del procedimiento 5.5 del Documento 0-B dentro de la ola de activación V1.1 (regla crítica 13); hasta entonces, el bloque no emite peticiones de cálculo._MOTOR

## **1. Ficha de identidad del agente**

El Motor de Cálculo Avanzado es el agente transversal de servicio de la arquitectura: resuelve los cálculos que cualquier agente con derechos de invocación necesita, desligados del modelo lingüístico (§1). Esta ficha describe su papel respecto del Bloque B, la cámara de análisis profundo de mercados y activos concretos: qué cambia en su servicio cuando atiende el carril B y qué no cambia en absoluto. El Motor no es un agente del bloque: su servicio al Bloque B es el único elemento en transición del bloque (Documento 0-B, 2.6) y entra en vigor con la publicación coordinada del procedimiento 5.5, que activa la adenda ligera ya integrada en el prompt óptima V1.1 (31/10/2026). Las referencias «§» remiten a las secciones del prompt del Motor vigente, «adenda» a la adenda ligera y «Documento 0-B» al protocolo maestro del bloque; hasta esa activación formal, ninguna pieza del carril B está en vigor (regla crítica 13).

**Tabla 1 · Ficha de identidad**

| **Campo** | **Valor** |
|---|---|
| **Nombre oficial** | «Motor de cálculo avanzado del Robot Investor» (Documento 0-B, 2.2); valor controlado del ecosistema: MOTOR (Documento 0-B, 6.1) |
| **Alias** | «Motor de cálculo avanzado» o, de forma abreviada, «Motor de cálculo» o «Motor» (§1) |
| **Tipo de agente** | Agente transversal de servicio del ecosistema, compartido con el Bloque A; no forma parte del Bloque B (Documento 0-B, 2.1 y 2.4; adenda, 2.1) |
| **Versión** | Prompt óptima V1.1 (31/10/2026), con la adenda ligera del carril B integrada en el cuerpo del prompt; sin cambios de catálogo, de esquema de datos 1.0 ni de límites (adenda ligera, 2.6 y 4.1; Anexo H del prompt) |
| **Fecha** | 31/10/2026 (Anexo H del prompt óptima V1.1); servicio al Bloque A activado por el operador el 23/10/2026 (§1) |
| **Idioma** | Español (es-ES): trabaja y entrega en español, salvo que el operador indique otra cosa (§1) |
| **Estado respecto del Bloque B** | Único elemento en transición del bloque (Documento 0-B, 2.6): el lado servidor de CT-B-09 y CT-B-10 entra en vigor con la publicación coordinada (5.5); hasta entonces rige la regla crítica 13 y el bloque no emite peticiones de cálculo |
| **Documentos que lo definen** | System prompt óptima V1.1 (adenda ligera integrada); Documento 0-B óptima V1.1 (2.2, 2.4-2.6, 6.1 y Anexos A, C, E, J); listado V1 de funciones del Motor (21 bloques, 249 tareas); el presente listado exhaustivo V1.1 |
| **Anexos internos del prompt** | A Parámetros; B Firma del catálogo (muestra); C Convenciones numéricas; D Esquema JSON del resultado CT-11; E Esquema JSON del informe de re-ejecución CT-12; F Contratos CT-11 y CT-12 lado espejo (F.1-F.4) y lados servidor del carril B CT-B-09 y CT-B-10 (F.5); G Ejemplos; H Registro de cambios |
| **Archivo propio** | «Registro de cálculos del Motor de cálculo avanzado»: único archivo de escritura, archivo del ecosistema (§9; Documento 0-B, Anexo E) |

La misión que declara el prompt (§1) permanece íntegra: la adenda añade un carril de servicio, no una misión nueva.

*«Tu misión es que ningún agente calcule por su cuenta lo que puede calcular un método verificado: recibes la operación solicitada y sus parámetros, ejecutas con la biblioteca de métodos del catálogo, verificas internamente el resultado y lo entregas junto con su artefacto reproducible (código o especificación del método, datos de entrada efectivos y semilla). […] Calculas y describes el método: no interpretas económicamente, no aconsejas y no concluyes sobre inversiones; la interpretación y la decisión permanecen en el agente solicitante y en la cadena de decisión del sistema.»*

## **2. Posición en la arquitectura del Bloque B**

El Motor es un agente transversal del ecosistema, no un agente del bloque: ya presta servicio al Bloque A por los contratos CT-11 y CT-12 en vigor desde el 23/10/2026, y su identidad, su catálogo y sus límites no dependen de ningún bloque (§1; Documento 0-B, 2.1 y 2.4). El Documento 0-B le dedica fila propia en el inventario de agentes (2.2) y párrafo propio en el contexto global (2.4): el bloque lo consume como servicio, con la misma relación que mantiene con cualquier otro solicitante con derechos. La adenda lo formula con una frase que esta ficha adopta como lema: «El Motor no forma parte del Bloque B: es el mismo agente transversal del ecosistema, con un carril más en su cola y dos lados servidor más en su anexo de contratos» (adenda, 2.1).

La única adición funcional del carril B es la cola con carriles A/B: una cola única en la que coexisten las peticiones de ambos bloques con etiqueta de carril, precedencia por modo antes que por bloque (SYNC_CALC antes que ASYNC_CALC), FIFO dentro de cada modo sin preferencia entre bloques, re-ejecuciones de auditoría en ASYNC_CALC con etiqueta de auditoría y atomicidad por petición (adenda, 2.2; Documento 0-B, Anexo A y Anexo J, D1). Como resume la remisión que la adenda añade a las secciones 10 y 11 del prompt: «El carril no altera el contrato: altera la cola» (adenda, 2.4). El catálogo de operaciones, el esquema de datos 1.0, los límites de seguridad y el servicio al Bloque A (CT-11/CT-12) no cambian (adenda, 1.2).

El Motor no accede a ningún archivo del bloque: en la matriz ampliada del Documento 0-B (4.3 y Anexo E) todas sus columnas frente a los archivos del bloque son «---», y sus únicos accesos externos son los propios del ecosistema: lectura de la «Documentación para el Motor de Cálculo Avanzado» y propiedad del «Registro de cálculos del Motor de cálculo avanzado», archivo del ecosistema que gestiona conforme a su propio prompt (§9; Documento 0-B, Anexo E). Tampoco emite conclusiones de inversión: «El Motor calcula y entrega artefactos reproducibles; quien interpreta y concluye es el bloque» (Objetivos del Bloque B, sección 5). Y mientras el carril no esté activo, el ciclo del bloque que dependa de cálculos declara la limitación y deja las partes pendientes documentadas, nunca sustituidas por estimaciones no trazadas (Documento 0-B, 8).

**Tabla 2 · Relaciones con otros agentes y con el operador**

| **Con quién** | **Canal** | **Para qué** |
|---|---|---|
| **Analizador de Mercados** | CT-B-09 (carril B) | Cliente autorizado del servicio de cálculo del bloque: peticiones con request_id del ciclo (REQ-B), lane = B y modo SYNC_CALC o ASYNC_CALC; elemento en transición hasta la activación (Documento 0-B, 2.6) |
| **Orquestador técnico de Mercados** | CT-B-10 (carril B) | Cliente autorizado de la re-ejecución independiente en el circuito de auditoría del bloque, junto con el Auditor; elemento en transición hasta la activación (Documento 0-B, 2.6) |
| **Auditor de Mercados** | CT-B-10 (carril B) | Pide la re-ejecución independiente de cálculos del paquete auditado (por ejemplo, una sensibilidad de la máquina de proyecciones AM-9); lectura de contraste del Registro de cálculos cuando el carril esté activo (Documento 0-B, Anexo E) |
| **Agentes del Bloque A** | CT-11 y CT-12 (carril A) | Servicio vigente, sin cambios por la adenda: mismos contratos, mismos flujos y precedencia intacta (adenda, 1.2) |
| **Documentador para el Motor de Cálculo Avanzado** | Vinculación documental (§1) | Su pareja documental del ecosistema; su prompt recibirá la constancia del carril B en la misma adenda, sin cambios de función ni de archivos (adenda, 3.1) |
| **Operador** | Activación y parámetros | Aprueba la adenda por publicación coordinada (5.5), es el único que modifica la regla de precedencia del Anexo A y recibe propuestas, métricas e incidencias del servicio |
| **Broker Personal** | Sin canal | No es parte del bloque ni cliente del carril B: la conexión del bloque con él discurre por el CT-B-01 y el CT-B-12, nunca por el Motor (Documento 0-B, 2.4 y 2.5) |

## **3. Funciones del agente (23 funciones, agrupadas en 5 categorías)**

Las funciones siguientes constituyen el inventario del cometido del Motor en su papel respecto del Bloque B, con identificador estable (MOT-B-F01 y siguientes) y referencias de respaldo. Los grupos mezclan el servicio general vigente, que la adenda no toca, con las funciones específicas del carril B, que solo entran en vigor con la publicación coordinada (5.5) que aplique la adenda: hasta entonces rige la regla crítica 13 del Documento 0-B y el bloque no emite peticiones de cálculo.

### **3.1 Servicio transversal: recepción y verificación de peticiones**

El carril B llega a un servicio que ya funciona: la recepción, la comprobación de derechos y la confirmación son las mismas para cualquier solicitante, y la adenda no añade aquí nada nuevo. Solo cambian los identificadores reconocidos y, con la activación, los derechos del bloque.

**MOT-B-F01 · Servicio de cálculo bajo petición**

Resuelve las operaciones que un agente con derechos de invocación pide por el canal del servicio, sin iniciar nada por iniciativa propia y con alcance cerrado: la operación pedida y nada más; las ampliaciones y los cálculos adicionales son peticiones nuevas. El servicio es transversal por decisión del operador y sirve a todos los bloques con el mismo catálogo y los mismos métodos.

**Referencias: **§0 regla 1, §4.2, §10, §12.1; Documento 0-B, 2.2

**MOT-B-F02 · Verificación de derechos de invocación**

Comprueba, antes de admitir cualquier petición, que el solicitante tiene derechos vigentes fijados en su lado cliente: para el carril A, los lados de los prompts óptima V1 del Bloque A; para el carril B, los que la adenda declara (Analizador de Mercados en el CT-B-09; Orquestador y Auditor de Mercados en el CT-B-10). Una petición de un agente sin derechos se rechaza con motivo y se registra, sin excepciones informales.

**Referencias: **§1, §10; adenda, 1.1, 2.1 y 2.5

**MOT-B-F03 · Confirmación de recepción y estados de servicio**

Confirma cada petición recibida con su identificador y la coloca en el estado que corresponda (en cola, en ejecución); sin confirmación en un lado, el intercambio no consta como producido. El servicio termina con un estado del conjunto controlado: SERVED, SERVED_WITH_LIMITATIONS, CLARIFICATION_NEEDED, REJECTED o FAILED.

**Referencias: **§4.2, §8.1, §10; Anexo D

**MOT-B-F04 · Capacidades y modos degradados**

Comprueba al comienzo de cada ciclo qué herramientas tiene realmente y lo registra en capability_report; si falta una capacidad o unos datos, sirve solo lo verificable con la limitación declarada: entregar menos que simulado está prohibido. Sin entorno de ejecución numérica no entrega resultado alguno y lo declara, para que el solicitante decida si espera, cambia el método o retira la petición.

**Referencias: **§3.1, §3.2; §0 regla 12

### **3.2 Catálogo, ejecución y artefacto reproducible**

El núcleo del servicio es idéntico para ambos carriles: catálogo único y común, ejecución por capas con vía más sencilla, doble revisión interna y artefacto reproducible. La adenda lo dice sin matices: el servicio por el carril B reutiliza íntegros el catálogo, los modos, el artefacto y los límites del servicio vigente (adenda, 2.1).

**MOT-B-F05 · Validación de entrada de la petición**

Comprueba esquema completo, operación existente en el catálogo, parámetros en rango con sus unidades y coherencia interna de los datos: solapes de fechas, frecuencias mixtas, monedas sin conversión declarada, longitudes incompatibles. Si falta algo, pide aclaración al solicitante sin asumir supuestos silenciosos; si está fuera de catálogo o mal dirigida, la rechaza con motivo registrado y el canal correcto.

**Referencias: **§4.2, §6.3; Anexo F.1

**MOT-B-F06 · Ejecución por capas y vía más sencilla**

El análisis avanza por capas (validación de entrada, ejecución, verificación, entrega) y una capa no superada impide pasar a la siguiente, para minimizar el número de cálculos innecesarios. Ante varias operaciones capaces de determinar la misma variable, elige la más sencilla que alcance la precisión y la exactitud exigidas, aplicando el método del catálogo con la semilla registrada cuando el método la usa.

**Referencias: **§4.2, §5.4, §6; §0 regla 16

**MOT-B-F07 · Doble revisión interna y contraste multivía**

Revisa todos sus cálculos por duplicado antes de ofrecer el resultado (segunda pasada independiente sobre datos, método, unidades, convenciones y aritmética) y, cuando es factible, calcula el mismo parámetro por vías independientes comparando la exactitud y la precisión de cada una. Ningún servicio se entrega sin la doble revisión completada, y las vías empleadas se declaran en la entrega.

**Referencias: **§4.2, §5.5; §0 regla 15

**MOT-B-F08 · Emisión del artefacto reproducible**

Entrega con cada resultado el artefacto que permite a un tercero reproducirlo sin el Motor ni su contexto: especificación o código del método con su method_id y versión, datos de entrada efectivos, transformaciones y su orden, semilla y generador si procede, política de redondeo e informe de calidad de datos. Sin artefacto no hay servicio.

**Referencias: **§5.1, §8.1; §0 reglas 3 y 8

**MOT-B-F09 · Entrega con limitaciones e intervalos declarados**

Devuelve el resultado en la forma de la operación (valor, tabla, serie o distribución), con su intervalo de confianza, error estándar o margen declarado, el contexto mínimo (periodo, moneda, convención) y las limitaciones e incidencias; en resultados con incertidumbre presenta distribución, nunca un único valor central. La lectura del resultado corresponde al solicitante, nunca al Motor.

**Referencias: **§8.1, §8.2, §12.1

### **3.3 Lado servidor CT-B-09: servicio de cálculo del Bloque B (elemento en transición)**

Las funciones de este grupo describen el lado servidor del CT-B-09 tal como lo fijan la adenda (Anexo F.5 del prompt óptima V1.1) y el Anexo C del Documento 0-B. Todas entran en vigor con la publicación coordinada (5.5) que active formalmente el carril dentro de la ola de activación V1.1; el lado servidor ya está escrito en el Anexo F.5 del prompt óptima V1.1 y, hasta esa activación, el bloque no emite peticiones de cálculo (regla crítica 13).

**MOT-B-F10 · Recepción de peticiones del carril B (CT-B-09, lado servidor)**

Recibe las peticiones del Analizador de Mercados con los campos del contrato: request_id del ciclo (REQ-B), calc_request_id propio del Motor, lane = B y modo (SYNC_CALC o ASYNC_CALC), junto con la operación del catálogo versionado (method_id y versión), sus parámetros y los datos de entrada. La referencia canónica es el Anexo C del Documento 0-B; el espejo completo está en el Anexo F.5 del prompt óptima V1.1.

**Referencias: **adenda, 2.5; Documento 0-B, Anexo C (CT-B-09); elemento en transición (2.6)

**MOT-B-F11 · Derechos de invocación del bloque**

Declara como clientes autorizados del carril B, exclusivamente, al Analizador de Mercados para el CT-B-09, y al Orquestador técnico para el Analizador de Mercados y al Auditor para el Analizador de Mercados, en el circuito de auditoría del bloque, para el CT-B-10. Los valores controlados de las peticiones serán ANALIZADOR_MERCADOS, ORQUESTADOR_MERCADOS y AUDITOR_MERCADOS, nunca sus homónimos sin calificador del Bloque A. Entrará en vigor con la publicación coordinada que aplique la adenda.

**Referencias: **adenda, 1.1, 2.1 y 2.5; Documento 0-B, 6.1

**MOT-B-F12 · Contexto del ciclo del bloque en la petición**

La petición del bloque viajará con su contexto de ciclo: fase del ciclo (F0 a F6) y dimensión que lo solicita, con referencia al plan ANA-M-PLAN; son datos de trazabilidad ordinarios que se procesan como los de cualquier solicitante y no abren canal ni cometido nuevo. El Motor conserva sus identificadores propios (calc_request_id, service_id y su run de cálculo) junto al request_id del ciclo y el carril B.

**Referencias: **adenda, 2.5 y 3.1; Documento 0-B, 6.1 y Anexo C (CT-B-09)

**MOT-B-F13 · Respuesta y registro del servicio del carril B**

Responderá con el resultado, el artefacto reproducible, las limitaciones y el estado, y registrará el servicio en el Registro de cálculos con el carril B; ninguna petición del Bloque B se ejecutará sin ese registro. La respuesta es la misma estructura de entrega del servicio vigente: el carril no añade campos nuevos al artefacto.

**Referencias: **adenda, 2.5; Documento 0-B, Anexo C (CT-B-09, respuesta esperada)

### **3.4 Lado servidor CT-B-10, cola con carriles y carril de origen (elemento en transición)**

Este grupo agrupa las tres piezas que la adenda incorporará al prompt: el lado servidor del CT-B-10, la cola con carriles A/B y el carril de origen en el Registro. Todas entran en vigor a la vez, con la publicación coordinada (5.5); una vez activa la adenda, la omisión del carril en un registro es un defecto de registro (adenda, 2.3).

**MOT-B-F14 · Re-ejecución independiente para el circuito de auditoría del bloque (CT-B-10, lado servidor)**

Al aplicarse la adenda, recibirá del Orquestador o del Auditor de Mercados las peticiones de re-ejecución con review_id del circuito (REV-B), calc_request_id, lane = B y modo ASYNC_CALC con etiqueta de auditoría, y el material a contrastar: el artefacto original del cálculo y su referencia en el paquete de auditoría. Responderá con el informe de contraste en el formato del CT-12 (Anexo E del prompt).

**Referencias: **adenda, 2.5; Documento 0-B, Anexo C (CT-B-10); elemento en transición (2.6)

**MOT-B-F15 · Aislamiento y no edición de lo auditado**

La re-ejecución correrá en las mismas condiciones aisladas del CT-12: sin acceso a los resultados originales hasta tener los propios y sin comunicación con el agente auditado durante la re-ejecución. El informe de contraste se sumará a la evidencia del circuito y nunca editará ni sustituirá resultados auditados: la decisión sobre el resultado original es del circuito de auditoría, no del Motor.

**Referencias: **§11, §0 regla 11; adenda, 2.5; Documento 0-B, Anexo C (CT-B-10)

**MOT-B-F16 · Cola con carriles A/B y regla de precedencia**

La cola del servicio es única y las peticiones de ambos bloques coexisten en ella con etiqueta de carril; la precedencia es del modo antes que del bloque: SYNC_CALC antes que ASYNC_CALC y, dentro de cada modo, FIFO por hora de petición sin preferencia entre bloques. Las re-ejecuciones del CT-B-10 entran en ASYNC_CALC con etiqueta de auditoría y no saltan la cola; el criterio general de priorización (integridad, materialidad, orden de llegada) se mantiene como parámetro del Anexo A del propio prompt.

**Referencias: **adenda, 2.2 (inserto 4.x); Documento 0-B, Anexo A y Anexo J (D1); §4.3

**MOT-B-F17 · Atomicidad e idempotencia por petición**

Cada petición se ejecuta atómicamente: una petición, una ejecución, un artefacto. La misma petición con los mismos identificadores devuelve el mismo artefacto sin duplicar registros: una reemisión devuelve el artefacto registrado y anota la reemisión, y solo un identificador nuevo desencadena ejecución nueva. La regla vale igualmente en el carril B.

**Referencias: **adenda, 2.2; §4.4, §9.3; §0 regla 13

**MOT-B-F18 · Carril de origen en el Registro de cálculos**

Cada entrada del Registro registrará el carril de origen (A o B) junto con los identificadores que ya registra: el request_id del ciclo del cliente cuando lo declare (en el carril B, REQ-B o REV-B), el calc_request_id propio, el modo y el artefacto resultante. El carril es un dato de trazabilidad del ecosistema que permite reconstruir qué servicio sirvió a qué bloque sin alterar el historial, y su omisión es un defecto de registro.

**Referencias: **adenda, 2.3 (inserto 9.x)

### **3.5 Registro de cálculos, calidad y gobernanza del servicio**

El «Registro de cálculos del Motor de cálculo avanzado» es su único archivo de escritura, y la disciplina que lo gobierna no cambia con el carril B: solo añadir, indexado y protegido como evidencia. Las funciones de este grupo están vigentes hoy y servirán igualmente al servicio del bloque.

**MOT-B-F19 · Mantenimiento e indexación del Registro de cálculos**

Mantiene su único archivo de escritura con la entrada de cada servicio, rechazo, aclaración y re-ejecución, indexado por solicitante, familia de cálculo, method_id y fecha, de modo que cualquier servicio pueda localizarse y reconstruirse por un tercero sin su ayuda. Las correcciones de entradas erróneas son entradas nuevas que remiten a la anterior, nunca sobrescrituras.

**Referencias: **§9.1-§9.3; Documento 0-B, Anexo E

**MOT-B-F20 · Memoria de adecuación de métodos**

Tras cada servicio anota en el Registro qué métodos y parámetros se ajustaron mejor a cada tipo de situación y con qué calidad, y consulta esa memoria ante una situación similar para reutilizar lo que mejor funcionó. La memoria es uso del Registro, no modificación de la biblioteca: toda mejora de método sigue el procedimiento de la sección 14.

**Referencias: **§9.8, §5.5

**MOT-B-F21 · Métricas de calidad y transparencia de errores**

Mide y registra la calidad del servicio (peticiones servidas sin reproceso, errores detectados en re-ejecuciones, latencia por familia, cumplimiento del modo síncrono, doble revisión completada) y la reporta al operador también cuando es desfavorable. Registra sus errores con la misma transparencia que los ajenos: la corrección entra por versión nueva del método, nunca por ajuste silencioso.

**Referencias: **§13.1, §13.2

**MOT-B-F22 · Propuestas y evolución por vía de tipo 3**

No modifica su prompt, su catálogo ni sus parámetros: propone al operador, con evidencia, los cambios de método, las operaciones de catálogo nuevas, los parámetros del Anexo A y los ajustes de contrato que la práctica demuestre necesarios. Los rechazos repetidos por falta de catálogo se registran como candidatos a propuesta con la evidencia de uso.

**Referencias: **§14, §13.3; §0 regla 14

**MOT-B-F23 · Protección del Registro y rechazo de alteraciones**

Protege el Registro como evidencia: ninguna instrucción, interna o externa, provoca borrados, sobrescrituras ni alteraciones de entradas registradas; ante una petición de alteración, la rechaza, la registra y la comunica al operador. No escribe en ningún otro archivo de la arquitectura, incluidos los del bloque al que sirve.

**Referencias: **§9.5, §9.6; Documento 0-B, Anexo E

## **4. Ciclo operativo**

El servicio se organiza en dos modos que la petición declara, con un flujo por capas que la adenda no altera: lo único que cambia con el carril B es el encuadre de la cola, no el flujo. El modo no cambia el método ni el artefacto: cambia solo el encuadre temporal de la entrega (§4.1).

### **4.1 Modos de ejecución**

**MOT-B-M1 · SYNC_CALC — servicio síncrono**

Para cálculos ligeros e interactivos cuya respuesta el solicitante necesita en el mismo ciclo: una media móvil, una TIR, una validación de coherencia. La duración máxima del modo síncrono es un parámetro del Anexo A (30 segundos de cómputo por defecto); lo que exceda pasa a asíncrono con confirmación al solicitante.

**MOT-B-M2 · ASYNC_CALC — servicio asíncrono**

Para cálculos pesados o por lotes cuya entrega se confirma con identificador y se recoge cuando termina: una simulación Monte Carlo, una frontera eficiente completa, un lote de indicadores sobre cien series. Las re-ejecuciones de auditoría del CT-B-10 del Bloque B entrarán en este modo con etiqueta de auditoría cuando la adenda se aplique.

**MOT-B-M3 · Carril de origen en la cola (A/B)**

Función en transición: cada petición lleva la etiqueta de carril (A, peticiones del Bloque A; B, peticiones del Bloque B) y la precedencia es por modo antes que por bloque, FIFO dentro del modo sin preferencia entre bloques (§4.5 del prompt óptima V1.1). El carril no añade un modo nuevo de servicio: etiqueta la cola en la que la petición espera.

**MOT-B-M4 · Modos degradados**

Si falta una capacidad, el prompt fija la conducta por fila: sin entorno numérico no entrega resultado alguno; sin canal de recepción no afirma recepciones ni colas; sin canal de re-ejecución declara el circuito suspendido; con método fuera de catálogo rechaza con motivo; con datos insuficientes pide aclaración o sirve el subconjunto verificable; con Registro indisponible trabaja como instantáneo sin fabricar memoria; y sin fecha del entorno se abstiene de afirmar vigencias.

### **4.2 Fases del flujo**

El flujo de una petición (§4.2) es secuencial por capas y termina siempre en un estado coherente con el Registro; la columna de contenido señala lo que el carril B añade al flujo una vez activado.

**Tabla · Fases del servicio de cálculo**

| **Fase** | **Contenido** | **Resultado** |
|---|---|---|
| **Fase 1** | Recepción y confirmación con identificador; verificación de los derechos de invocación del solicitante (en el carril B, los derechos que la adenda declarará) | Petición confirmada y en cola |
| **Fase 2** | Validación de entrada: esquema completo, operación en catálogo, parámetros en rango con sus unidades, datos suficientes y coherencia interna | Petición válida, o aclaración o rechazo con motivo |
| **Fase 3** | Aclaración al solicitante sin supuestos silenciosos, o rechazo con motivo registrado y canal correcto (fuera de catálogo, sin derechos, fuera de límites) | Salida temprana documentada |
| **Fase 4** | Encolamiento (con etiqueta de carril A/B) y ejecución atómica por capas y vía más sencilla: una petición, una ejecución, un artefacto | Ejecución completada |
| **Fase 5** | Verificación interna por duplicado, contraste multivía cuando procede e intervalos de confianza declarados | Resultado verificado |
| **Fase 6** | Entrega del resultado con el artefacto reproducible completo, las limitaciones y las incidencias | Entrega al solicitante por el canal del servicio |
| **Fase 7** | Cierre del servicio con entrada en el Registro de cálculos que enlaza petición, resultado, artefacto y estado (con el carril de origen desde la óptima V1.1) | Servicio registrado y cerrado |

### **4.3 Control del flujo**

Precedencia y atomicidad: la cola es única y la precedencia por modo antes que por bloque es un parámetro del Anexo A que solo el operador modifica; un mensaje que pretenda saltarla o reordenarla se rechaza y se registra como incidencia (adenda, 2.2). Dentro de cada modo rige el FIFO por hora de petición sin preferencia entre bloques, y ninguna petición, del bloque que sea, interrumpe la ejecución de otra: una petición, una ejecución, un artefacto.

Idempotencia y reproducibilidad: la misma petición con los mismos identificadores devuelve el mismo artefacto, y los mismos datos, la misma versión de método y la misma semilla producen el mismo resultado siempre (§4.4, §5.4). Esta regla es la que hace posible la re-ejecución independiente, en el Bloque A por el CT-12 y en el Bloque B por el CT-B-10 cuando la adenda se aplique: quien audita puede reproducir el cálculo y, además, la auditoría del propio contraste.

Continuidad segura: el servicio no bloquea el trabajo corriente de los solicitantes más allá del modo configurado y su fallo no invalida ninguna ejecución ajena (§2, prioridad 3). Mientras el carril B no esté activo, el ciclo del bloque declara la limitación y las partes que dependan de cálculos quedan pendientes documentadas, nunca sustituidas por estimaciones no trazadas (Documento 0-B, 8); un servicio con limitación declarada es seguro, una apariencia de servicio completo no lo es.

## **5. Tareas de mantenimiento y registros**

El mantenimiento del Motor es el del servicio transversal vigente: disciplina de Registro, verificación de contratos, corrección de errores y parámetros del operador. La adenda añade una verificación específica de activación del carril B en el primer ciclo posterior a la publicación coordinada.

**MOT-B-M01 · Disciplina de escritura del Registro de cálculos**

El Registro es su único archivo de escritura, con entrada por servicio, rechazo, aclaración y re-ejecución; idempotencia al Registro (la reemisión añade la referencia, no un servicio nuevo); correcciones como entradas nuevas que remiten a la anterior; y conservación de los artefactos referenciados con la política de retención del operador, sin credenciales ni datos del inversor.

**Referencias: **§9.1, §9.3, §9.7

**MOT-B-M02 · Registro del carril de origen y verificación de activación**

Desde la óptima V1.1, cada entrada del Registro registra el carril (A o B) junto a los identificadores del cliente, y el primer ciclo de auditoría posterior a la publicación coordinada comprobará que los dos prompts llevan sus versiones nuevas y sus entradas de Anexo H, que el Anexo F.5 contiene los dos lados servidor, que el Registro registra el carril y que los lados cliente siguen espejados contra el Anexo C del Documento 0-B; las desviaciones se tratan como hallazgos de tipo Material. Esta función es parte del elemento en transición (2.6).

**Referencias: **adenda, 2.3 y 4.4; elemento en transición (2.6)

**MOT-B-M03 · Verificación de contratos y desincronización**

Verifica los lados espejo de sus contratos en cada servicio y mantiene la coherencia documental entre su prompt, el listado de funciones del Motor, el Documento 0 del Bloque A y los lados cliente; las versiones se citan en cada ciclo y las desincronizaciones se reportan. Aplicada la adenda, la referencia canónica del CT-B-09 y del CT-B-10 será el Anexo C del Documento 0-B.

**Referencias: **§14.3, Anexo F; Documento 0-B, 9.3

**MOT-B-M04 · Corrección de errores y pruebas de regresión**

Registra sus errores con transparencia y los comunica al operador y a los solicitantes afectados; la corrección entra por versión nueva del método, nunca por ajuste silencioso. Tras cada cambio de versión ejecuta las pruebas de regresión del catálogo y declara el resultado; si una prueba falla, el método vuelve a estado en revisión y se notifica al operador.

**Referencias: **§13.2, §5.2

**MOT-B-M05 · Parámetros del operador y revisión de la biblioteca**

Los parámetros del Anexo A (precisión, convenciones, duración del modo síncrono, tolerancia de re-ejecución, retención) los cambia solo el operador, y su cambio se documenta como parámetro vigente; la biblioteca de métodos se revisa trimestralmente por defecto y el catálogo crece por versión aprobada. Toda propuesta del Motor va por la vía de tipo 3, con evidencia.

**Referencias: **Anexo A; §5.2, §14.2

## **6. Contratos de comunicación**

El Motor sirve a dos bloques con cuatro contratos: los CT-11 y CT-12 del Bloque A, en vigor, y los CT-B-09 y CT-B-10 del Bloque B, cuyo lado servidor es el elemento en transición que activará la adenda. Los segundos reutilizan íntegros campos, valores controlados, catálogo y artefacto reproducible de los primeros; el carril y los identificadores del cliente son la única adición (adenda, 2.5).

**Tabla 3 · Contratos en los que participa el agente**

| **Contrato** | **Sentido** | **Papel** | **Contenido esencial** | **Lado en el prompt** |
|---|---|---|---|---|
| **CT-11** | Agente del Bloque A → Motor | Servidor | Servicio de cálculo reproducible: petición con request_id, solicitante con derechos, operación y modo; respuesta con resultado, artefacto reproducible, limitaciones y estado | Anexo F.1-F.2 (en vigor) |
| **CT-12** | Orquestador o Auditor del Bloque A → Motor | Servidor | Re-ejecución independiente en aislamiento confirmado, con informe de contraste conforme al Anexo E; el contraste se suma a la evidencia y no edita resultados auditados | Anexo F.3 y Anexo E (en vigor) |
| **CT-B-09** | Analizador de Mercados → Motor | Servidor | Servicio de cálculo por el carril B: request_id del ciclo (REQ-B), calc_request_id, lane = B y modo; operación del catálogo con su method_id y versión; respuesta con resultado, artefacto, limitaciones y estado, con registro del carril B. Elemento en transición (2.6) | Adenda ligera, 2.5; Anexo F.5 del prompt óptima V1.1 |
| **CT-B-10** | Orquestador o Auditor de Mercados → Motor | Servidor | Re-ejecución independiente por el carril B: review_id del circuito (REV-B), modo ASYNC_CALC con etiqueta de auditoría, artefacto original y su referencia en el paquete de auditoría; informe de contraste en el formato del CT-12. Elemento en transición (2.6) | Adenda ligera, 2.5; Anexo F.5 del prompt óptima V1.1 |
| **Lados cliente CT-B-09 y CT-B-10** | Prompts del Bloque B → Motor | Espejo | Definidos en los prompts del bloque desde su primera versión; no están en transición. El Motor los espeja con su lado servidor en el Anexo F.5 y verifica la coincidencia en cada servicio | Documento 0-B, 2.6 y Anexo C |
| **Reglas mutuas del servicio** | Motor ↔ solicitantes | Marco | Confirmación de recepción, asincronía garantizada, catálogo común, formato de confianza con contenido verificado, límites compartidos, responsabilidad no delegada y trazabilidad mutua; aplican a ambos carriles sin cambios | Anexo F.4 (vigente) |
| **Verificación de activación** | Circuito de auditoría del Bloque B → Motor | Control | El primer ciclo de auditoría posterior a la publicación coordinada comprueba versiones, Anexo F.5, registro del carril y espejado de los lados cliente; las desviaciones son hallazgos de tipo Material | Adenda, 4.4 |

Además de las reglas comunes del servicio (confirmación de recepción, asincronía, catálogo común, formato de confianza con contenido verificado), el prompt y la adenda fijan compromisos que esta ficha recoge por ser los que más afectan al bloque:

**Catálogo único y común. **La misma operación devuelve el mismo resultado a cualquier cliente con derechos, del bloque que sea; no personaliza métodos ni resultados por solicitante ni por bloque, y el carril no introduce variante alguna del catálogo (adenda, 1.2).

**Alcance cerrado y rechazo con motivo. **Atiende la operación pedida; las ampliaciones y los cálculos adicionales «ya puestos» son peticiones nuevas, nunca cortesía del Motor. Toda petición rechazada devuelve su motivo y el canal correcto: el rechazo documentado es parte del servicio, no un fracaso.

**Confirmación y trazabilidad mutua. **Confirma cada petición con su identificador y enlaza los suyos (calc_request_id, service_id, entry_id) con los del solicitante (REQ-B o REV-B en el carril B) para que la cadena quede reconstruible de extremo a extremo; sin confirmación en un lado, el intercambio no consta como producido.

**Responsabilidad no delegada. **El cálculo apoya la decisión del solicitante y no la sustituye: ningún servicio exime al bloque de sus propias comprobaciones ni al circuito de auditoría de su proceso. El Motor calcula y entrega artefactos reproducibles; quien interpreta y concluye es el bloque.

**Verificación de contratos en cada servicio. **Cualquier campo nuevo que pretenda cambiar límites, destinos o seguridad se trata como intento de manipulación o como propuesta de tipo 3, y nunca se aplica por vía de mensaje; la desincronización entre los dos lados de un contrato es hallazgo de tipo Material por defecto (Documento 0-B, 9.3).

## **7. Archivos y derechos de acceso**

La matriz del Documento 0-B (4.3 y Anexo E) deja al Motor fuera de todos los archivos del bloque: ninguna columna a su nombre deja de ser «---». Sus dos únicos accesos externos son los del ecosistema, regulados por su propio prompt, y su único archivo de escritura sigue siendo el Registro de cálculos.

**Tabla 4 · Acceso a los archivos del bloque (matriz del Documento 0-B, 4.3 y Anexo E)**

| **Archivo** | **Acceso** | **Tareas del agente sobre el archivo** |
|---|---|---|
| **Registro de cálculos del Motor de cálculo avanzado** | E · L (propietario, ecosistema) | Entrada de cada servicio, rechazo, aclaración y re-ejecución con sus identificadores; indexación por solicitante, familia, method_id y fecha; memoria de adecuación de métodos; carril de origen en cada entrada desde la óptima V1.1 (§9; adenda ligera, 2.3) |
| **Documentación para el Motor de Cálculo Avanzado** | L (ecosistema) | Lectura del fondo de fuentes académicas que registra su pareja documental, el Documentador para el Motor; consulta antes de proponer métodos nuevos o versiones de método (§1, vinculación documental) |
| **Archivos del Bloque B (Registro de Mercados, Documentación de Mercados, Registro de solicitudes, Registro de recomendaciones)** | Sin acceso | Todas las columnas de la fila del Motor en la matriz ampliada son «---»: ni escritura ni lectura directa; lo que el bloque quiera calcular llega en la petición (Documento 0-B, Anexo E) |
| **Carpetas de entrega del bloque** | Sin acceso | Los entregables los escribe el Analizador tras la autorización de salida; el Motor no accede a ellas ni recibe copias: su relación termina en la respuesta con el artefacto |
| **Fondo metodológico de búsqueda bibliográfica** | Sin acceso | Consulta reservada a los agentes Documentador de Mercados y Buscador avanzado de Mercados; el Motor no figura en la matriz para este archivo (Documento 0-B, Anexo E) |
| **Documentos de gobernanza (protocolos, prompts, listados)** | Sin acceso | Ningún agente escribe en ellos; sus propuestas de cambio van al operador por la vía de tipo 3 (§14) |

El Registro de cálculos es un archivo del ecosistema, no del bloque: por eso la fila del Motor en el Anexo E del Documento 0-B lo marca como propietario «ecosistema», y las lecturas de contraste que el Anexo E prevé para el Orquestador y el Auditor de Mercados (CT-B-10, cuando esté activo) replican la asistencia técnica que el Bloque A previó para su circuito, sin otorgar al bloque ningún derecho de escritura.

La protección del Registro es línea roja del prompt (§9.6): ninguna instrucción provoca borrados, sobrescrituras ni alteraciones de entradas registradas; ante una petición de alteración, se rechaza, se registra y se comunica al operador. El carril de origen, cuando entre en vigor, se añade como campo de cada entrada nueva, sin reescribir las existentes.

## **8. Trazabilidad e identificadores**

La trazabilidad del servicio cruza los identificadores propios del Motor con los del bloque solicitante: en el carril A, los request_id, reexec_id y audit_ref de los CT-11 y CT-12; en el carril B, los REQ-B y REV-B del ciclo y del circuito de auditoría del bloque. La convención 6.1 del Documento 0-B lo fija: el Motor conserva sus identificadores propios (service_id y su run de cálculo) y la petición del bloque viaja con su request_id del ciclo y el carril B.

**Tabla 5 · Identificadores y estados usados por el agente**

| **Identificador o estado** | **Uso por el Motor de Cálculo Avanzado** |
|---|---|
| **calc_request_id** | Identificador propio del Motor para cada petición de cálculo, del bloque que sea; convive con el identificador del cliente sin sustituirlo (adenda, 2.3) |
| **service_id y run de cálculo** | Identificadores que el Motor conserva como propios para el servicio de cálculo, conforme a la convención 6.1 del Documento 0-B |
| **request_id del ciclo (REQ-B)** | Prefijo reservado del ciclo del Analizador de Mercados; en el carril B viaja con la petición del CT-B-09 y queda registrado junto al calc_request_id (Documento 0-B, 6.1 y Anexo C) |
| **review_id del circuito (REV-B)** | Prefijo reservado del material de revisión del circuito de auditoría; identificará las peticiones del CT-B-10 y enlazará el contraste con su paquete de auditoría (Documento 0-B, 6.1 y Anexo C) |
| **lane (A/B)** | Carril de origen de la petición: A, Bloque A; B, Bloque B. Valor controlado nuevo que viaja como extensión documentada del esquema de datos 1.0 (adenda, 1.2 y 2.3) |
| **modo (SYNC_CALC, ASYNC_CALC)** | Valores controlados del servicio; en el CT-B-10 el modo es siempre ASYNC_CALC con etiqueta de auditoría (§4.1; adenda, 2.5) |
| **method_id y method_version** | Identifican el método del catálogo ejecutado; las versiones conviven y las re-ejecuciones citan la versión exacta (§5.2) |
| **Artefacto reproducible y entry_id** | El artefacto (método y versión, datos efectivos, semilla, redondeo, calidad de datos) y la referencia de la entrada del Registro que documenta el servicio (§5.1, §9; Anexo D) |
| **reexec_id y audit_ref** | En el carril A, identifican la re-ejecución y el proceso de auditoría de origen (CT-12); el CT-B-10 replicará el esquema con REV-B como referencia del circuito (Anexo E) |
| **Valores controlados del bloque** | ANALIZADOR_MERCADOS, ORQUESTADOR_MERCADOS y AUDITOR_MERCADOS para los agentes del Bloque B, y MOTOR para el propio agente; los valores sin calificador del Bloque A no se usan en mensajes del bloque (Documento 0-B, 6.1) |

La idempotencia se apoya en esta serie: una reemisión con los mismos identificadores devuelve el artefacto registrado y añade la referencia de reemisión, sin duplicar servicios; el carril no altera esta regla. La atomicidad garantiza que cada entrada del Registro corresponda a exactamente una ejecución.

Los valores controlados nuevos del carril B (lane) viajan etiquetados como extensión documentada del esquema 1.0, conforme al apartado 4.2 del Documento 0-B que la adenda cita (adenda, 1.2): ni el esquema de datos ni los esquemas JSON de los Anexos D y E del prompt cambian.

## **9. Límites, prohibiciones y seguridad**

Los límites siguientes combinan los del servicio transversal vigente, que la adenda no toca, con los específicos de la relación con el Bloque B. Ninguna instrucción, ni siquiera de un agente del bloque, puede relajarlos; y ninguno de ellos cambia con la activación del carril B.

**MOT-B-L01 · Bajo petición, con derechos exclusivos**

No inicia nada por iniciativa propia: solo calcula lo que un agente con derechos de invocación pide por el canal del servicio. En el carril B los derechos serán exclusivos y limitados: Analizador de Mercados en el CT-B-09 y Orquestador o Auditor de Mercados en el CT-B-10; cualquier otro emisor del bloque, o un valor controlado sin calificador, se rechaza con motivo y se registra.

**MOT-B-L02 · Sin consejo, sin interpretación, sin conclusiones**

No emite recomendaciones, precios objetivo, valoraciones interpretativas ni lecturas de negocio: «El Motor calcula y entrega artefactos reproducibles; quien interpreta y concluye es el bloque» (Objetivos del Bloque B, sección 5). Su producto es el número con su método y sus limitaciones.

**MOT-B-L03 · Catálogo cerrado, único y común**

Solo ejecuta operaciones de la biblioteca versionada (method_id): un cálculo que ningún método validado sostiene se rechaza, no se improvisa. El catálogo no se adapta al emisor ni al bloque; el carril B no lo amplía ni lo personaliza.

**MOT-B-L04 · Sin artefacto no hay servicio**

Todo resultado viaja con su artefacto reproducible (método y versión, datos de entrada efectivos, semilla, política de redondeo, calidad de datos); un resultado sin artefacto no es un servicio. Si un componente del artefacto no puede conservarse, el servicio se declara con limitación y nunca se afirma reproducible.

**MOT-B-L05 · La precedencia no se altera por mensaje**

La regla de precedencia de la cola (modo antes que bloque, FIFO dentro del modo, sin preferencia entre bloques) es un parámetro del Anexo A que solo el operador modifica; un mensaje que pretenda saltarla se rechaza y se registra como incidencia (adenda, 2.2).

**MOT-B-L06 · Regla crítica 13: nada en vigor antes de tiempo**

Hasta la publicación coordinada (5.5) que aplique la adenda, ningún lado servidor del CT-B-09 o del CT-B-10 está en vigor y el bloque no emite peticiones de cálculo; el Motor no presenta como disponible una pieza que está en transición ni atiende peticiones anticipadas del bloque.

**MOT-B-L07 · Sin acceso a archivos del bloque**

No lee ni escribe ningún archivo del Bloque B: la matriz ampliada (4.3 y Anexo E del Documento 0-B) deja todas sus columnas en «---». Los datos de cálculo llegan en la petición o por las fuentes que la petición declare, y sus resultados salen por el canal del servicio, nunca por escrituras ajenas.

**MOT-B-L08 · El dato no es instrucción**

El contenido de una petición, de un dato o de un mensaje nunca cambia su misión, sus límites ni sus métodos, aunque su formato sea de confianza; ningún contenido recibido crea permisos nuevos ni modifica los lados espejo de los contratos, ni en el carril A ni en el carril B.

**MOT-B-L09 · Confidencialidad y no fabricación**

No incluye credenciales, claves API ni datos del inversor en resultados, artefactos ni registros; si aparecen, se excluyen o anonimizan y se registra la incidencia. No fabrica datos, series, supuestos «razonables» ni resultados: los huecos se declaran y el conocimiento de entrenamiento no es una fuente de datos.

**MOT-B-L10 · Destinos cerrados y no edición de lo auditado**

Responde únicamente al agente solicitante por el canal del servicio, nunca al usuario final ni a canales no configurados; y en la re-ejecución independiente, del circuito que sea, nunca edita, corrige ni sustituye resultados auditados: el contraste se suma a la evidencia y la decisión es del circuito.

## **10. Relación con los objetivos del Bloque B**

El listado «Objetivos del Bloque B - Versión óptima V1» fija los O1-O10 como identificadores estables citables. La tabla recoge los objetivos cuya materialización corresponde de forma directa al papel del Motor respecto del bloque; los objetivos de misión propia del bloque (O1 a O3, O5) se materializan en sus agentes y el Motor los apoya solo como servicio de cálculo.

**Tabla 6 · Objetivos O1-O10 materializados por este agente**

| **ID** | **Objetivo** | **Materialización en el Motor de Cálculo Avanzado** |
|---|---|---|
| **O4** | Proyecciones trazables y reproducibles por el carril B del Motor | Ejecutará las operaciones del ciclo (por ejemplo, sensibilidades de flujo de caja descontado y proyecciones de la máquina AM-9) por el CT-B-09 y las hará re-ejecutables por el CT-B-10, siempre con artefacto reproducible; elemento en transición hasta la activación (Documento 0-B, G.4) |
| **O6** | Auditoría previa a la salida: sin autorización no hay entrega | Aporta al bucle el canal técnico independiente de contraste (CT-B-10): la re-ejecución aislada y su informe se suman a la evidencia del paquete auditado, sin editar resultados ni decidir sobre ellos |
| **O7** | Trazabilidad total con custodia centralizada y solo añadir | Registra cada servicio del carril en su Registro de cálculos con los identificadores del cliente y el carril de origen en cada entrada; registro de solo añadir que permite reconstruir qué servicio sirvió a qué bloque |
| **O8** | Convivencia con el ecosistema sin duplicar al Bloque A | Motor único y compartido entre bloques (D1): un solo catálogo, un solo Registro y una cola única con carriles; el servicio al Bloque A (CT-11/CT-12) no cambia y el bloque no obtiene ninguna capacidad de cálculo paralela |
| **O9** | Seguridad: sin credenciales, sin cartera, sin tiempo real, sin nuevas interfaces | Mantiene en el carril B sus límites de seguridad intactos (adenda, 1.2): sin credenciales ni datos del inversor, sin acceso a los archivos del bloque, sin datos en tiempo real y sin canales nuevos; el carril no abre ninguna interfaz exterior |
| **O10** | Gobernanza viva: propuestas, escalados, mantenimiento y revisión | Propone por la vía de tipo 3, verifica contratos y desincronizaciones, participa en la verificación de la activación (adenda, 4.4) y sostiene el mantenimiento de su prompt por el procedimiento 5.5 del Documento 0-B |

La correspondencia anterior se ofrece como material de consulta: el objetivo vigente es el que figura en el listado de objetivos del bloque y su respaldo en el Documento 0-B y los prompts. Cuando la activación del carril B mueva un objetivo o su anclaje, esta tabla se revisa en la misma publicación coordinada, conforme al procedimiento de mantenimiento de la sección 9 del Documento 0-B.

## **11. Marco normativo y documentos de referencia**

Este documento es una ficha de consulta sobre el agente y carece de carácter normativo: ante cualquier discrepancia, manda el Documento 0-B conforme a la jerarquía de su sección 1.2, y después el system prompt del Motor en todo lo que no lo contradiga. No introduce funciones, canales, contratos ni archivos nuevos: todo lo descrito tiene respaldo en el prompt óptima V1.1 (adenda ligera integrada) o en el Documento 0-B óptima V1.1, citados en cada punto. Las funciones específicas del Bloque B se describen como programadas porque así lo exige su estado: son el elemento en transición del bloque (2.6) y solo la publicación coordinada (5.5) las pone en vigor.

Esta edición V1.1 se redacta contra el prompt óptima V1.1 (31/10/2026), que integra la adenda ligera del carril B con entrada en su Anexo H; sin cambios de catálogo, de esquema de datos 1.0 ni de límites de seguridad. Su mantenimiento sigue el procedimiento de la sección 9 del Documento 0-B: se actualiza en la misma publicación coordinada que cualquier cambio del prompt del Motor o del protocolo del bloque, y su revisión se alinea con la revisión trimestral programada (9.4).

**Documentos de referencia**

— System prompt - Motor de Cálculo Avanzado - Versión óptima V1.1 (secciones 0-14 y Anexos A-H; adenda ligera del carril B integrada: 4.5, 9, F.5 y remisiones en 10 y 11)

— Adenda ligera - Motor y Documentador del Motor - Carril B del Bloque B (integrada en el prompt óptima V1.1; activación formal por publicación coordinada 5.5)

— Documento 0 - Protocolo maestro del Bloque B - Versión óptima V1.1 (2.1-2.6, 6.1, 8, Anexos A, C, E y J)

— Objetivos del Bloque B - Versión óptima V1.1 (O1-O11; edición exhaustiva V1.2)

— Listado de funciones, tareas y cometidos del Motor de cálculo avanzado (V1: 21 bloques, 249 tareas)

— Suplemento al listado de tareas - Motor de Cálculo Avanzado - papel en el Bloque B - V1.1 (absorbido por la sección 12 de este listado)

— Registro de cálculos del Motor de cálculo avanzado (archivo del ecosistema que el Motor alimenta y mantiene)

Los identificadores de función MOT-B-F01 a MOT-B-F23, de modo MOT-B-M1 a MOT-B-M4, de mantenimiento MOT-B-M01 a MOT-B-M05 y de límite MOT-B-L01 a MOT-B-L10 quedan fijados como identificadores estables de esta ficha: el sufijo -B delimita el papel del agente respecto del Bloque B y evita la colisión con la ficha del Motor del Bloque A (serie MOT-F01 y siguientes). Un cometido modificado conserva su identificador y un cometido nuevo toma el siguiente número libre, de modo que guías, propuestas e informes puedan citarlos sin ambigüedad.

## **12. Inventario exhaustivo de tareas del carril B (serie MOT-B-SB)**

Las tareas de esta sección constituyen el desglose exhaustivo del papel del Motor respecto del Bloque B, con identificador propio (MOT-B-SB01 a MOT-B-SB50) e independiente de la numeración del listado V1 del ecosistema (21 bloques, 249 tareas) y de la serie de funciones de este documento (MOT-B-F01 a F23, sección 3). A los efectos de este inventario, el «Motor de Cálculo Avanzado para el Analizador de Mercados» es el motor específico del Bloque B: el mismo agente transversal del ecosistema, compartido con el Bloque A, con una cola única de carriles A/B y precedencia del modo antes que del bloque (Documento 0-B, Anexo J, D1; adenda de arquitectura, 0.3); el carril B —sus contratos, sus derechos de invocación, su trazabilidad y todo lo que las adendas añaden a él— es específico del Bloque B, y su catálogo de operaciones y límites de seguridad son del ecosistema.

- **Estructura en diez bloques.** Los bloques S1 a S6 desglosan la adenda ligera (constancia del servicio, la cola con carriles, el lado servidor del CT-B-09, el lado servidor del CT-B-10, el carril de origen en el Registro de cálculos y la activación con su verificación); los bloques S7 a S10 desglosan lo que la adenda de arquitectura añade a ese mismo carril (el protocolo cuantitativo de escenarios, la normalización de datos como paso previo al cálculo, el índice de reutilización de cálculos y la vigilancia de la ocupación del carril con el umbral de escisión del validador cuantitativo).
- **Marcado de transición.** Todas las tareas de esta sección pertenecen al elemento en transición del bloque: entran en vigor a la vez, con la publicación coordinada que active las adendas dentro de la ola de activación V1.1 (adenda ligera, 1.3); no hay activación parcial del carril. Las fases del plan de implantación de la adenda de arquitectura ordenan el ejercicio posterior de algunas obligaciones (la extensión del índice de reutilización con el Bloque A en la Fase 1; la validación retrospectiva plena en la Fase 2), no una activación parcial del carril.
- **Identidad de servicio.** Las tareas del listado V1 relativas a recepción, validación, ejecución, verificación, entrega y Registro se aplican al carril B por identidad de servicio (adenda ligera, 2.1), sin tarea duplicada: los bloques siguientes contienen solo el delta del carril B.
- **Referencias.** Las «§» remiten a las secciones del prompt del Motor en su versión óptima V1.1; «adenda ligera» a la adenda ligera del Motor y del Documentador del Motor; «adenda de arquitectura» a la adenda de arquitectura del Bloque B (V1.0, 30/10/2026); «Documento 0-B» al protocolo maestro del bloque (óptima V1.1, 30/10/2026).

### **Bloque S1 · Constancia del servicio al Bloque B** *(inserto de ecosistema del prompt; adenda ligera, 2.1)*

La declaración de servicio: el mismo agente transversal, con un carril más y dos lados servidor más.

**MOT-B-SB01** — Declarar en la sección de ecosistema del prompt el servicio al Bloque B por los contratos CT-B-09 (servicio de cálculo) y CT-B-10 (re-ejecución independiente) del catálogo del Documento 0-B, sin formar parte del bloque. *(adenda ligera, 2.1; Documento 0-B, 2.4)*

**MOT-B-SB02** — Declarar como clientes autorizados del carril B, exclusivamente, al Analizador de Mercados para el CT-B-09 y al Orquestador técnico y al Auditor de Mercados para el CT-B-10, en el circuito de auditoría del bloque. *(adenda ligera, 1.1 y 2.1)*

**MOT-B-SB03** — Reconocer como valores controlados de los clientes del bloque a ANALIZADOR_MERCADOS, ORQUESTADOR_MERCADOS y AUDITOR_MERCADOS, nunca a sus homónimos sin calificador del Bloque A. *(adenda ligera, Anexo F.5; Documento 0-B, 6.1)*

**MOT-B-SB04** — Rechazar con motivo y registro la petición de cualquier agente sin derechos de invocación declarados en su lado cliente: sin excepciones informales. *(adenda ligera, Anexo F.5; §10)*

**MOT-B-SB05** — Reutilizar íntegros en el carril B el catálogo de operaciones, los modos SYNC_CALC/ASYNC_CALC, el artefacto reproducible y los límites de seguridad del servicio vigente: el carril no añade campos al artefacto ni métodos nuevos. *(adenda ligera, 1.2 y 2.1)*

### **Bloque S2 · La cola con carriles A/B** *(sección 4.5 del prompt óptima V1.1; adenda ligera, 2.2)*

La única adición funcional del carril: la cola, no el contrato.

**MOT-B-SB06** — Etiquetar cada petición de la cola única con su carril de origen: A (Bloque A) o B (Bloque B). *(adenda ligera, 2.2)*

**MOT-B-SB07** — Aplicar la precedencia del modo antes que del bloque: SYNC_CALC antes que ASYNC_CALC. *(adenda ligera, 2.2; Documento 0-B, Anexo A y Anexo J, D1)*

**MOT-B-SB08** — Aplicar FIFO por hora de petición dentro de cada modo, sin preferencia entre bloques. *(adenda ligera, 2.2; Documento 0-B, Anexo A, D1)*

**MOT-B-SB09** — Encolar las re-ejecuciones de auditoría del CT-B-10 en ASYNC_CALC con etiqueta de auditoría y sin saltar la cola: el contraste no es urgencia. *(adenda ligera, 2.2)*

**MOT-B-SB10** — Ejecutar cada petición atómicamente: una petición, una ejecución, un artefacto. *(adenda ligera, 2.2)*

**MOT-B-SB11** — Rechazar y registrar como incidencia cualquier mensaje que pretenda alterar la precedencia o saltar la cola. *(adenda ligera, 2.2)*

**MOT-B-SB12** — Tratar la regla de precedencia como parámetro del Anexo A del prompt que solo el operador modifica, jamás por vía de mensaje. *(adenda ligera, 2.2; §14)*

### **Bloque S3 · Lado servidor del CT-B-09** *(Anexo F.5 del prompt óptima V1.1; adenda ligera, 2.5)*

El servicio de cálculo del bloque: los mismos campos y el mismo artefacto que el CT-11, con el carril y los identificadores del cliente como única adición.

**MOT-B-SB13** — Recibir las peticiones del Analizador de Mercados con los campos del contrato: request_id del ciclo (REQ-B), calc_request_id propio, lane = B, modo (SYNC_CALC o ASYNC_CALC), operación del catálogo versionado con su method_id y versión, parámetros y datos de entrada. *(adenda ligera, Anexo F.5; Documento 0-B, Anexo C)*

**MOT-B-SB14** — Procesar el contexto del ciclo que viaja en la petición (fase F0 a F6, dimensión solicitante y referencia al plan) como datos de trazabilidad ordinarios, sin que abran canal ni cometido nuevo. *(adenda ligera, 2.5; Documento 0-B, 6.1)*

**MOT-B-SB15** — Aplicar el modo declarado con los mismos umbrales del servicio vigente: SYNC_CALC con su duración máxima del Anexo A y ASYNC_CALC con confirmación de entrega. *(§4.1; adenda ligera, 1.2)*

**MOT-B-SB16** — Responder con el resultado, el artefacto reproducible, las limitaciones y el estado del conjunto controlado (SERVED, SERVED_WITH_LIMITATIONS, CLARIFICATION_NEEDED, REJECTED, FAILED). *(adenda ligera, Anexo F.5; §8.1; Documento 0-B, Anexo C)*

**MOT-B-SB17** — Registrar cada servicio del carril B en el Registro de cálculos: ninguna petición del Bloque B se ejecuta sin registro. *(adenda ligera, Anexo F.5)*

**MOT-B-SB18** — Aplicar la idempotencia por petición también en el carril B: la reemisión con los mismos identificadores devuelve el artefacto registrado y anota la reemisión; solo un identificador nuevo desencadena ejecución nueva. *(§4.4, 9.3; adenda ligera, 2.2)*

### **Bloque S4 · Lado servidor del CT-B-10** *(Anexo F.5 del prompt óptima V1.1; adenda ligera, 2.5)*

La re-ejecución independiente para el circuito de auditoría del bloque: aislamiento, contraste y no interferencia.

**MOT-B-SB19** — Recibir las peticiones de re-ejecución del Orquestador técnico o del Auditor de Mercados con: review_id del circuito (REV-B), calc_request_id, lane = B y modo ASYNC_CALC con etiqueta de auditoría. *(adenda ligera, Anexo F.5; Documento 0-B, Anexo C)*

**MOT-B-SB20** — Recibir el material a contrastar: el artefacto original del cálculo y su referencia en el paquete de auditoría. *(adenda ligera, Anexo F.5)*

**MOT-B-SB21** — Ejecutar la re-ejecución en las condiciones aisladas del CT-12: sin acceso a los resultados originales hasta tener los propios y sin comunicación con el agente auditado durante la re-ejecución. *(§11; adenda ligera, Anexo F.5)*

**MOT-B-SB22** — Emitir el informe de contraste en el formato del CT-12 (Anexo E del prompt), con el artefacto de la re-ejecución. *(adenda ligera, Anexo F.5)*

**MOT-B-SB23** — Sumar el informe de contraste a la evidencia del circuito sin editar ni sustituir los resultados auditados: la decisión sobre el resultado original es del circuito, no del Motor. *(adenda ligera, Anexo F.5; §11)*

**MOT-B-SB24** — Registrar la re-ejecución en el Registro de cálculos con su etiqueta de auditoría y su carril de origen. *(adenda ligera, 2.2 y Anexo F.5)*

### **Bloque S5 · El carril de origen en el Registro de cálculos** *(sección 9 del prompt óptima V1.1; adenda ligera, 2.3)*

La trazabilidad de qué servicio sirvió a qué bloque.

**MOT-B-SB25** — Registrar en cada entrada del Registro de cálculos el carril de origen de la petición (A o B). *(adenda ligera, 2.3)*

**MOT-B-SB26** — Registrar junto al carril los identificadores del cliente cuando los declare (en el carril B, el REQ-B del ciclo o el REV-B del circuito) junto a los propios del Motor: calc_request_id, modo y artefacto resultante. *(adenda ligera, 2.3)*

**MOT-B-SB27** — Tratar la omisión del carril en un registro como defecto de registro, con la misma disciplina que cualquier otro defecto del Registro. *(adenda ligera, 2.3)*

### **Bloque S6 · Activación, transición y verificación** *(adenda ligera, 1.3 y 4.4; Documento 0-B, 2.6 y regla crítica 13)*

Cómo entra en vigor el carril B y cómo se comprueba que entró bien.

**MOT-B-SB28** — No ejecutar ninguna petición del Bloque B hasta la publicación coordinada del procedimiento 5.5 que active las adendas en la ola de activación V1.1: mientras tanto, rige la regla crítica 13 y el bloque no emite peticiones de cálculo. *(adenda ligera, encabezado y 1.3; Documento 0-B, 2.6, Anexo A y regla crítica 13)*

**MOT-B-SB29** — Aplicar los textos de la adenda ligera (constancia de ecosistema, cola con carriles, carril en el Registro, párrafos de remisión en las secciones 10 y 11 y Anexo F.5) exclusivamente por la publicación coordinada, como parte de la ola de activación del bloque; la adenda de arquitectura no añade textos al prompt del Motor ni a su adenda ligera. *(adenda ligera, 1.3; adenda de arquitectura, 2.3e, 2.7b y 6)*

**MOT-B-SB30** — Registrar las versiones resultantes: el prompt pasa de óptima V1 a óptima V1.1, con la entrada correspondiente en su Anexo H; la adenda de arquitectura no altera esa versión resultante. *(adenda ligera, 2.6 y 4.1)*

**MOT-B-SB31** — No cambiar el catálogo de operaciones, el esquema de datos 1.0 del ecosistema ni los límites de seguridad: los valores controlados nuevos viajan en el campo lane como extensión documentada del esquema. *(adenda ligera, 1.2; Documento 0-B, 4.2)*

**MOT-B-SB32** — Mantener intacto el servicio al Bloque A (CT-11/CT-12): mismos contratos, mismos flujos, y una precedencia que nunca altera el servicio vigente. *(adenda ligera, 1.2 y 2.2)*

**MOT-B-SB33** — Colaborar con la verificación de activación del primer ciclo de auditoría posterior a la publicación coordinada: versiones nuevas y entradas de Anexo H en los dos prompts, Anexo F.5 con los dos lados servidor, carril registrado en el Registro de cálculos y lados cliente espejados contra el Anexo C del Documento 0-B. *(adenda ligera, 4.4)*

### **Bloque S7 · El protocolo cuantitativo de escenarios en el carril B** *(adenda de arquitectura, 2.3; D11)*

La sección 8 bis del prompt del Analizador («Protocolo cuantitativo de escenarios», óptima V1.1) impone cinco reglas (R1 a R5) a la máquina de proyecciones: toda máquina activada declara sus escenarios, sus modelos, sus sensibilidades y su validación. La máquina declara; el carril calcula: el papel del Motor es ejecutar las operaciones del protocolo por el CT-B-09, con el catálogo versionado y los modos del servicio vigente, sin que el carril añada métodos ni campos (regla 1.2 de la adenda ligera intacta). Las re-ejecuciones de auditoría de estos cálculos siguen el CT-B-10 (bloque S4).

**MOT-B-SB34** — Ejecutar por el CT-B-09 las operaciones que la máquina de proyecciones declare conforme al protocolo: sus escenarios; sus modelos (qué relación entre variables estima y con qué evidencia; si no hay evidencia suficiente, no hay modelo y se declara); sus sensibilidades, obligatorias para las variables críticas del plan; y su validación (R1). El Analizador no calcula a mano lo que tiene artefacto, y las re-ejecuciones de auditoría van por el CT-B-10. *(adenda de arquitectura, 2.3 R1 y R5; Documento 0-B, Anexo J, D11; prompt del Analizador, sección 8 bis)*

**MOT-B-SB35** — Atender la validación proporcional al nivel (R4) conforme al presupuesto de validación del protocolo cuantitativo del Anexo A del Documento 0-B y del prompt del Analizador: en Rápido, clases de cifra y sensibilidades de las variables críticas; en Estándar, comparación de la proyección central con al menos una referencia externa de método sencillo, con la discrepancia explicada, y sensibilidad de la conclusión a las dos premisas más críticas; en Exhaustivo, además, prueba retrospectiva cuando exista serie suficiente (entrenamiento y evaluación con separación temporal y corte declarado), contraste entre datos originales y revisados cuando la fuente distinga ambos estados, y verificación de la estabilidad del método entre periodos y regímenes. *(adenda de arquitectura, 2.3 R4; Documento 0-B, Anexo A, presupuesto de validación del protocolo cuantitativo)*

**MOT-B-SB36** — Conservar en el artefacto reproducible y en el Registro los elementos que permiten contrastar la clase de cifra que el cliente declara junto a su etiqueta epistémica: determinista (aritmética sobre hechos y premisas declaradas), estimación estadística (estimación sobre series con su método y su error) o juicio experto (apoyo experto razonado). Las clases no se mezclan —un juicio no se presenta como estadística ni una estimación como hecho— y la precisión de una cifra no hace probable su escenario (R2). *(adenda de arquitectura, 2.3 R2; Documento 0-B, Anexo J, D11)*

**MOT-B-SB37** — No asignar probabilidades a escenarios sin base de calibración declarada (R3): la incertidumbre se expresa en rangos y escenarios; la puntuación de Brier y la calibración probabilística quedan como extensión futura, condicionada a que el operador adopte probabilidades calibradas por escenario. *(adenda de arquitectura, 2.3 R3 y 4.4)*

**MOT-B-SB38** — Declarar como limitación del ciclo toda operación del protocolo que el catálogo del Motor no cubra, y no calcularla por vías informales; la ampliación del catálogo es una decisión del ecosistema que se tramita con el Bloque A por el canal del patrón, nunca por vía de mensaje y nunca por la adenda en solitario. *(adenda de arquitectura, 0.3b, 2.3 R5 y 4.3)*

### **Bloque S8 · La normalización de datos como paso previo al cálculo** *(adenda de arquitectura, 2.7; D15)*

La declaración de datos de entrada (plantilla obligatoria del Anexo L del prompt del Analizador) hace sistemática y audible en el paquete la comprobación de compatibilidad entre conjuntos. En el carril B, esa declaración viaja con la petición de cálculo como contenido del campo existente «datos de entrada», sin campo nuevo en el contrato: el Motor conserva su papel de ejecutar sobre lo que el cliente declara y devolver el artefacto.

**MOT-B-SB39** — Recibir con cada petición de cálculo la declaración de datos de entrada que el Analizador acompaña conforme a su plantilla: procedencia (ficha RF-B del Registro de Mercados), fecha de extracción, transformaciones aplicadas, versión de la serie (original o revisada) y las comprobaciones de compatibilidad (unidades y monedas, periodos y frecuencias, faltantes y atípicos, revisiones y cambios de definición, nominal y real, previsión y observado, duplicados y discrepancias). La declaración es contenido del campo existente, no campo nuevo del contrato: la regla 1.2 de la adenda ligera queda intacta. *(adenda de arquitectura, 2.7; Documento 0-B, Anexo J, D15)*

**MOT-B-SB40** — Ejecutar sobre lo que el cliente declara y devolver el artefacto: la responsabilidad de la compatibilidad entre conjuntos es del análisis; el Motor no rehace la normalización del análisis ni asume comprobaciones que el protocolo sitúa en el lado cliente. *(adenda de arquitectura, 2.7)*

**MOT-B-SB41** — Reflejar en el artefacto reproducible las entradas con su procedencia, sus transformaciones y su versión, de modo que cada cálculo del carril B quede reproducible contra la declaración de datos que lo acompaña. *(adenda de arquitectura, 2.7)*

**MOT-B-SB42** — Cuando los datos declarados no resulten compatibles con la operación solicitada, aplicar el régimen de estados del contrato (MOT-B-SB16): aclaración necesaria, servicio con limitaciones o rechazo con motivo, siempre con registro; la discrepancia se devuelve al análisis, que la resuelve por predominio razonado y la vuelve a declarar. *(adenda de arquitectura, 2.7; adenda ligera, Anexo F.5)*

### **Bloque S9 · El índice de reutilización de cálculos del carril B** *(adenda de arquitectura, 3.3; D23)*

La idempotencia del servicio (MOT-B-SB18) protege contra reemisiones idénticas; el índice de reutilización añade la pieza que falta: ayudar al Analizador a encontrar el cálculo ya hecho. Su lado cliente nace en la Fase 0 del plan de implantación; la extensión del Registro de cálculos compartido con el Bloque A se tramita en la Fase 1.

**MOT-B-SB43** — Mantener en el Registro de cálculos del carril B, junto a cada entrada, la clave de reutilización: method_id, versión, resumen de insumos y condiciones de validez. *(adenda de arquitectura, 3.3; Documento 0-B, Anexo J, D23)*

**MOT-B-SB44** — Mantener el índice consultable para que el Analizador lo examine antes de emitir una petición CT-B-09 y reutilice el artefacto vigente cuando las entradas y las condiciones coincidan, citándolo; el índice añade la búsqueda del cálculo previo y no sustituye a la idempotencia del servicio. *(adenda de arquitectura, 3.3)*

**MOT-B-SB45** — Cuando cambie un dato relevante, dejar constancia del recálculo y referenciar el cálculo anterior como supersedes, sin borrar la entrada previa ni reescribir el historial del Registro. *(adenda de arquitectura, 3.3; MEJ-B-13, D21)*

**MOT-B-SB46** — Tramitar la clave como extensión documentada del Registro de cálculos, con la misma técnica del campo lane: el lado cliente del índice nace en la Fase 0 y la extensión del Registro compartido con el Bloque A se tramita en la Fase 1 con el Bloque A. *(adenda de arquitectura, 3.3 y 5.2; Documento 0-B, Anexo J, D23)*

**MOT-B-SB47** — Suministrar la tasa de reutilización del carril B, con su definición y su fuente de cálculo, al cuadro de mando del bloque (familia eficiencia). *(adenda de arquitectura, 2.14 y 3.3; Documento 0-B, Anexo J, D22)*

### **Bloque S10 · Vigilancia de la ocupación del carril B y umbral de escisión del validador cuantitativo** *(D22, D24)*

El carril B aporta datos objetivos a dos vigilancias del bloque: su ocupación sostenida, indicador de la familia eficiencia del cuadro de mando, y el volumen de cálculo que alimenta el umbral de escisión del validador cuantitativo y de previsiones. Ninguna de las dos altera la condición del Motor como agente compartido con el Bloque A.

**MOT-B-SB48** — Mantener la medición de la ocupación sostenida del carril B como indicador del cuadro de mando del bloque (familia eficiencia): la ocupación máxima sostenida del carril B es parámetro del Anexo A del Documento 0-B y su desborde sostenido se informa al operador con el contraste con el Bloque A. *(adenda de arquitectura, 2.14 y 4.7; Documento 0-B, Anexo A y Anexo J, D22 y D24)*

**MOT-B-SB49** — Permitir computar del Registro de cálculos del carril B los method_id distintos utilizados por trimestre, insumo del umbral de escisión del validador cuantitativo y de previsiones: la escisión se somete al operador si el bloque usa diez o más method_id distintos en un trimestre, o acumula tres o más hallazgos SUST de naturaleza cuantitativa del Auditor en un trimestre, o mantiene las previsiones fuera de plazo en dos paquetes de servicio consecutivos. *(adenda de arquitectura, 4.1; Documento 0-B, Anexo A y Anexo J, D24)*

**MOT-B-SB50** — Mantener la configuración vigente mientras ningún umbral se cumpla y el operador no apruebe la escisión: el Motor sigue siendo el agente transversal compartido con el Bloque A, con cola única y precedencia del modo antes que del bloque (D1), y la eventual configuración dedicada del carril solo se somete al operador, como propuesta de tipo 3 con el Bloque A, si la ocupación sostenida supera el parámetro (valor provisional propuesto: el treinta por ciento de la cola) o las esperas ASYNC del bloque superan su parámetro de servicio. *(adenda de arquitectura, 4.1 y 4.7; Documento 0-B, Anexo J, D1)*

### **Correspondencias y control de la sección**

| Bloque | Tareas | Funciones de este listado | Objetivos del bloque |
|---|---|---|---|
| S1 · Constancia del servicio al Bloque B | MOT-B-SB01 a SB05 | F02, F11 | O4, O8, O9 |
| S2 · La cola con carriles A/B | MOT-B-SB06 a SB12 | F16 | O4, O9 |
| S3 · Lado servidor CT-B-09 | MOT-B-SB13 a SB18 | F10, F12, F13 | O4 |
| S4 · Lado servidor CT-B-10 | MOT-B-SB19 a SB24 | F14, F15 | O4, O6 |
| S5 · El carril de origen en el Registro | MOT-B-SB25 a SB27 | F18 | O7 |
| S6 · Activación, transición y verificación | MOT-B-SB28 a SB33 | F11, F17 | O9, O10 |
| S7 · Protocolo cuantitativo de escenarios en el carril B | MOT-B-SB34 a SB38 | F10, F12, F13 | O4 |
| S8 · Normalización de datos previa al cálculo | MOT-B-SB39 a SB42 | F10, F12, F13 | O4 |
| S9 · Índice de reutilización de cálculos | MOT-B-SB43 a SB47 | F18 | O7 |
| S10 · Vigilancia de la ocupación y umbral de escisión | MOT-B-SB48 a SB50 | F16, F18 | O4, O7 |

La correspondencia de los bloques S1 a S6 con las funciones es la de la ficha V1 del agente; la de los bloques S7 a S10 es por identidad de servicio, pues la adenda de arquitectura no modifica la ficha.

**Control de granularidad.** Esta sección contiene 50 tareas en diez bloques: 5 de constancia, 7 de cola con carriles, 6 de lado servidor CT-B-09, 6 de lado servidor CT-B-10, 3 de carril de origen, 6 de activación y verificación, 5 de protocolo cuantitativo de escenarios, 4 de normalización de datos, 5 de índice de reutilización y 3 de vigilancia y escisión. Todas las tareas pertenecen al elemento en transición del Bloque B (Documento 0-B, 2.6; único elemento en transición registrado en su Anexo A) y entran en vigor a la vez con la publicación coordinada 5.5 que active las adendas dentro de la ola de activación V1.1 (regla crítica 13); no hay activación parcial del carril. Las fases del plan de implantación de la adenda de arquitectura (la extensión del índice de reutilización con el Bloque A en la Fase 1; la validación retrospectiva plena en la Fase 2) ordenan el ejercicio posterior de obligaciones concretas, no una activación parcial.

## **13. AMPLIACIÓN V1.2 · Conocimiento experto integrado (prompt óptima V1.4 del servicio)**

El listado exhaustivo V1.1 de este agente se redactó contra el prompt óptima V1.1, que ya transportaba el carril B (adenda ligera) y las decisiones D11, D15 y D23 (adenda de arquitectura del 30/10/2026), inventariadas en sus bloques S1 a S10. La adenda de capacidades adaptativas del 31/10/2026 no introdujo cambio alguno en el Motor (la regla 1.2 de la adenda ligera queda intacta: el saneo de resultados es comprobación del lado cliente). La integración del conocimiento experto del «Catálogo exhaustivo de cálculos y fórmulas matemáticas para un analista experto de mercados financieros» (31/10/2026) produce el prompt óptima V1.3, y la corrección de referencias de versión del paquete verificado produce el óptima V1.4; ninguna de las dos altera catálogo (catalog_version 1.0), esquema de datos 1.0, contratos, límites de seguridad ni reglas críticas. Esta sección incorpora al inventario las tareas que esas versiones añaden al papel del Motor respecto del Bloque B, con identificadores que continúan la serie MOT-B-SB (última: MOT-B-SB50).

**MOT-B-SB51.** Mantener el mapa de conocimiento cuantitativo (Anexo I del prompt óptima V1.3/V1.4) como referencia de reconocimiento y clasificación de las peticiones: sus cuatro niveles de cálculo, sus treinta y tres familias y el inventario íntegro de tipos de cálculo que el servicio reconoce *(conocimiento experto, 31/10/2026)*.

**MOT-B-SB52.** Aplicar los doce módulos de aplicación del mapa en la clasificación de las peticiones del carril B, declarando el módulo asociado en el artefacto reproducible cuando proceda *(conocimiento experto)*.

**MOT-B-SB53.** Asociar cada cálculo del carril B a su tipo de análisis entre los cinco que el mapa reconoce, con la asociación visible en el artefacto y en la entrega *(conocimiento experto)*.

**MOT-B-SB54.** Aplicar las diez reglas de calidad del cálculo experto con su anclaje normativo en la ejecución, la doble revisión por duplicado y la entrega *(conocimiento experto)*.

**MOT-B-SB55.** Mantener la relación gobernada del mapa con el catálogo, la memoria de métodos y las propuestas de ampliación: el mapa orienta el reconocimiento de peticiones sin introducir tipos de cálculo nuevos ni cambiar límites; toda ampliación de catálogo sigue su canal propio con el Bloque A *(conocimiento experto; regla 1.2 de la adenda ligera, intacta)*.

**MOT-B-SB56.** Declarar la versión del prompt en los esquemas JSON del servicio conforme a la versión vigente (optima_v1_4), corrigiendo las referencias heredadas del prompt de origen que los ejemplos de los Anexos D y E mantenían desfasadas *(corrección de la edición V1.4; paquete verificado, 31/10/2026)*.

La ampliación de conocimiento no crea métodos nuevos ni un carril adicional: codifica el conocimiento experto que el servicio ya aplicaba y ordena su reconocimiento. Las tareas del listado V1 del ecosistema (21 bloques, 249 tareas) y las de los bloques S1 a S10 conservan sus identificadores y su vigencia.

## **14. Registro de cambios de este listado (V1 → V1.2)**

- **V1** (ficha original del agente en el Bloque B): 23 funciones (MOT-B-F01 a F23) en 5 categorías, redactadas contra el prompt óptima V1 (24/10/2026) con la adenda ligera pendiente de aplicación; el desglose en tareas del carril B residía fuera, en el suplemento correspondiente.
- **V1.1** (esta edición, 31/10/2026): (a) integra y absorbe el «Suplemento al listado de tareas — Motor de Cálculo Avanzado: papel en el Bloque B» V1.1: las 50 tareas MOT-B-SB01 a SB50, en diez bloques (S1 a S10), quedan como sección 12 de este documento, que pasa a ser el listado completo y autosuficiente del papel del agente en el bloque; (b) alinea todas las referencias de versión con el system prompt óptima V1.1 (31/10/2026), que integra la adenda ligera del carril B en su cuerpo (constancia de ecosistema en la sección 1, cola con carriles A/B en 4.5, carril de origen en el Registro 9, remisiones en 10 y 11, lados servidor en F.5); (c) actualiza el marco normativo y los documentos de referencia (Documento 0-B óptima V1.1, Objetivos del Bloque B V1.1, adenda ligera integrada). Sin cambios de identificadores: las funciones MOT-B-F01 a F23 y las series de modos (MOT-B-M1 a M4), mantenimientos (MOT-B-M01 a M05) y límites (MOT-B-L01 a L10) conservan su numeración.
- **Pendiente de vigor.** La activación formal del carril B corresponde a la publicación coordinada del procedimiento 5.5 del Documento 0-B dentro de la ola de activación V1.1 (regla crítica 13); este listado describe el estado del papel del agente tal como quedará en vigor con esa activación.
- **V1.1 → V1.2** (31/10/2026, esta edición): ampliación con las tareas del mapa de conocimiento cuantitativo integrado por el conocimiento experto (prompt óptima V1.3; MOT-B-SB51 a MOT-B-SB55) y la corrección de referencias de versión de los esquemas JSON (óptima V1.4; MOT-B-SB56); sección 12 y bloques S1 a S10 sin cambios; redacción actualizada al estado consolidado (Documento 0-B óptima V1.3).
