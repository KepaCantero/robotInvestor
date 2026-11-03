# Registro de solicitudes y ejecuciones del Bloque B

VERSIÓN V1.1 · Archivo operativo del Bloque B de la arquitectura Robot Investor · Memoria operativa del protocolo on-demand: cada solicitud recibida, su normalización y encuadre, la asignación o el rechazo con motivo catalogado, los estados por fase del ciclo (F0-F6), el bucle de auditoría, la autorización de salida y la entrega · Propietario de escritura y mantenimiento: Orquestador técnico para el Analizador de Mercados · Lectura: Analizador de Mercados y Documentador de Mercados (contexto); extractos al Auditor de Mercados por el CT-B-07 · Gobernanza: «Documento 0 --- Protocolo maestro del Bloque B» (óptima V1.1, 30/10/2026), Anexo I (protocolo on-demand); régimen operativo: system prompt del Orquestador técnico para el Analizador de Mercados (óptima V1.1) · Esquema ampliado por la «Adenda de arquitectura --- Bloque B» (V1.0, 30/10/2026): bloque de referencias cruzadas entre solicitudes (D23) · es-ES

## 1. Rol del archivo en la arquitectura del Bloque B

Este archivo es la memoria del flujo on-demand del bloque: donde vive la trazabilidad mínima por solicitud que el Anexo I del Documento 0 fija (request_id; fechas de cada cambio de estado; encuadre normalizado; plan ANA-M-PLAN con sus versiones; peticiones de búsqueda y de cálculo con sus identificadores; paquetes de auditoría y vueltas del bucle; autorización de salida con su fecha y su guía; referencias de los tres entregables; altas de REC-B; y, en su caso, rechazo, anulación o espera con su motivo). El bloque no tiene cadencia: actúa con solicitud registrada, y este registro es la prueba de esa actuación. Su criterio de calidad, compartido con todos los archivos del bloque, es la reconstrucción: cualquier ciclo debe poder reconstruirse sin ayuda de sus protagonistas.

A diferencia de los otros tres archivos del bloque, este documenta el flujo que el propio propietario conduce: la misma relación que el Orquestador técnico del Bloque A mantiene con su Historial de auditorías. La custodia centralizada del registro (regla crítica 4 del Documento 0) deja fuera de este archivo todo lo que otros agentes registran: las fuentes viven en el Registro de Mercados, el conocimiento en la Documentación de Mercados, las recomendaciones en el Registro de recomendaciones; aquí vive el flujo.

## 2. Ficha de uso para los agentes

**Orquestador de Mercados (escritura y mantenimiento).** Cada paso que conduce deja constancia en el momento en que ocurre: recepción (S0), encuadre o rechazo (S1/R), asignación (S2), estados por fase remitidos por el Analizador (S3), vueltas del bucle y consolidados (S4), autorización (S5), entrega (S6) y cierre (S7), o los estados terminales y de espera (R/A/W). Mantenimiento híbrido D6: revisión post-solicitud en 48 horas naturales desde la entrega autorizada y revisión mensual ligera en la primera semana natural del mes.

**Analizador de Mercados (lectura).** Consulta el archivo para conocer el estado registrado de su ciclo y anclar sus remisiones (CT-B-04) al request_id y run_id correctos; la discrepancia entre lo que remite y lo registrado se resuelve a favor del Registro con la diferencia declarada.

**Documentador de Mercados (lectura como contexto).** Consulta el archivo para anclar cada remisión a su solicitud y verificar la constancia de autorización antes de dar de alta REC-B (4.4 de su prompt).

**Auditor de Mercados (vía extractos CT-B-07).** No accede directamente: recibe los extractos que el Orquestador remita con el material de revisión, tal cual están registrados.

**Broker Personal (sin acceso directo).** Recibe del Orquestador los acuses y la confirmación de entrega; este archivo es la trazabilidad interna del flujo.

## 3. Convenciones de formato

1. **Identificadores únicos e inmutables**: request_id con prefijo `REQ-B-` y cuatro dígitos (REQ-B-0001, REQ-B-0002…), run_id con `RUN-B-` (RUN-B-0001…), planes PLAN-B con versión (PLAN-B-v1, v2…), paquetes PKT-B con versión, revisiones REV-B, hallazgos FND-B, guías GUI-B. Sin renumeraciones; los duplicados se declaran, no se reasignan.
2. **Fechado ISO 8601** en todos los eventos: cada cambio de estado lleva su fecha y hora.
3. **Registro de solo añadir**: las correcciones y los deshaces son entradas nuevas que referencian a la entrada corregida; nunca se borra ni se reescribe una entrada existente.
4. **Estados del protocolo on-demand (Anexo I del Documento 0)**: S0 RECIBIDA · S1 EN ENCUADRE · S2 ASIGNADA · S3 EN CURSO · S4 EN AUDITORÍA · S5 AUTORIZADA · S6 ENTREGADA · S7 CERRADA · R RECHAZADA (motivo catalogado R1-R4) · A ANULADA · W EN ESPERA (suspensión documentada por discrepancias insubsanables).
5. **Una entrada maestra por solicitud** con sus bloques (sección 5), actualizada por adición de sub-entradas fechadas dentro de cada bloque; la reconstrucción del ciclo se lee de arriba abajo en orden cronológico.
6. **Versiones siempre presentes**: cada entrada lleva las versiones del Orquestador que la escribe y, cuando procede, las del Analizador.
7. **Campo no disponible se declara**: «no aplicable» o «pendiente», nunca inventado.
8. **Esquema 1.0 del ecosistema**: los valores controlados (estados, motivos, severidades, tipos) son los compartidos; este archivo solo fija la disposición.

## 4. Qué se registra y qué no

Se registra todo el flujo del protocolo on-demand por solicitud: recepción, encuadre con sus campos normalizados, rechazos con motivo y justificación sustantiva, asignaciones, plan con sus versiones, peticiones de búsqueda (SRCH-B) y de cálculo (calc_request_id) con sus identificadores, paquetes de auditoría con sus versiones, vueltas del bucle con sus consolidados, autorizaciones, entregas con las referencias de los tres entregables, altas de REC-B referenciadas, eventos CT-B-12 del ciclo, incidencias y escalados. No se registra: el contenido de los entregables (que vive en las carpetas de entrega, por referencias), el material de análisis (que vive en la Documentación de Mercados y en el paquete del ciclo), las fuentes (Registro de Mercados), ni datos personales del inversor o credenciales (nunca: incidencia de seguridad). La duda se resuelve registrando la referencia, no el contenido.

## 5. Estructura de la entrada por solicitud

Cada solicitud ocupa una entrada maestra con los bloques siguientes (desarrollo del Anexo E del prompt del Orquestador de Mercados, coherente con el Anexo I del Documento 0). Los bloques se rellenan por adición cronológica de sub-entradas fechadas. Desde la V1.1, la entrada incorpora el bloque de referencias cruzadas (D23): cuando un ciclo registra un hallazgo o una invalidación que afecta al objeto de otra solicitud en curso o recientemente cerrada, el Orquestador registra aquí el vínculo (solicitud afectada, hallazgo con su evidencia, remisión o disparador de revisión propuesto); la memoria inter-ciclos del bloque vive en este bloque, sin colas ni prioridades nuevas.

| Bloque | Contenido |
|---|---|
| Identificación de la solicitud | request_id (REQ-B), fecha de recepción, canal de entrada (CT-B-01), resumen de los campos recibidos (objeto, scope, context, restrictions), versiones del Orquestador |
| Encuadre | Estado S1 y resultado: asignación (campos del CT-B-02) o rechazo (motivo R1-R4, justificación sustantiva, opciones de reformulación) o anulación (A, con fecha) |
| Asignación | CT-B-02: fecha, presupuesto del nivel, respuesta del Analizador (aceptación / devolución justificada con su motivo) |
| Ciclo | run_id (RUN-B), plan ANA-M-PLAN con sus versiones, estados por fase (F0-F6) remitidos por CT-B-04, peticiones de búsqueda (SRCH-B) y de cálculo (calc_request_id, cuando el carril B esté activo) |
| Bucle de auditoría | Paquetes (PKT-B-v1, v2…) con fechas, vueltas del bucle, revisiones (REV-B), hallazgos (FND-B) con severidad definitiva y tipo, desacuerdos documentados, guías (GUI-B) con su aplicación, re-ejecuciones (CT-B-10) si las hubo |
| Cierre | Autorización de salida (fecha, packet_id final), referencias de los tres entregables con su convención de nombres, altas de REC-B (referencias), estados S6/S7 |
| Retroalimentación | Eventos CT-B-12 referidos a las REC-B del ciclo (fecha, remisión al Documentador, notificación al Analizador) |
| Referencias cruzadas (V1.1, D23) | Vínculos con otras solicitudes en curso o cerradas recientemente afectadas por hallazgos o invalidaciones de este ciclo: solicitud afectada, hallazgo con su evidencia, remisión efectuada o disparador de revisión propuesto |
| Incidencias | Cualquier incidencia del ciclo (seguridad, canal, escritura, trazabilidad) con su registro y su escalado si procedió |

### Plantilla de entrada nueva

> **REQ-B-XXXX — [objeto normalizado o «solicitud no normalizable»]**
>
> **Identificación.** **request_id:** REQ-B-XXXX · **Fecha de recepción:** AAAA-MM-DD · **Canal:** CT-B-01 · **Campos recibidos:** objeto (…), scope (geografía, moneda, horizonte, nivel sugerido), context (referencias del Bloque A si las hay), restrictions (…) · **Versiones del Orquestador:** …
>
> **Encuadre.** **Estado:** S1 · **Resultado:** [asignada / rechazada (motivo, justificación, opciones) / anulada] · **Fecha:** …
>
> *(Los bloques siguientes se añaden conforme avanza el ciclo, cada sub-entrada con su fecha.)*

## 6. Secciones del archivo

### 6.1 Índice operativo

| Campo | Valor |
|---|---|
| Versión del esquema | 1.0 |
| Solicitudes registradas | 0 (nacimiento del archivo: sin solicitudes aún) |
| Solicitudes por estado | --- |
| Última revisión del índice | 2026-10-28 (nacimiento del archivo) |

### 6.2 Entradas por solicitud

*(Sin entradas aún: el archivo nace vacío con el bloque. La primera solicitud recibida por el CT-B-01 abre REQ-B-0001.)*

### 6.3 Registro de mantenimiento

| Fecha | Tipo | Alcance y resultado |
|---|---|---|
| 2026-10-28 | Nacimiento | Archivo creado con su esquema (Anexo E del prompt del Orquestador), convenciones del bloque y plantilla de entrada; sin solicitudes |

## 7. Reglas de mantenimiento y ciclo de vida

Mantenimiento híbrido (D6): revisión ligera post-solicitud dentro de las 48 horas naturales siguientes a cada entrega autorizada (verificar que la trazabilidad del ciclo quedó completa: estados, plan, paquetes, vueltas, autorización, entrega, altas REC-B) y revisión mensual ligera en la primera semana natural del mes (índices por objeto y fecha, estados colgados en S1-S4 sin movimiento, coherencia de la trazabilidad). Las reglas completas están en la sección 10 del prompt del Orquestador de Mercados. Este archivo nunca se borra ni se renumera; los extractos al Auditor salen tal cual está registrado, sin sumarios reescritos.

## 8. Control de versiones del archivo

| Versión | Fecha | Cambios |
|---|---|---|
| V1.0 | 2026-10-28 | Nacimiento del archivo: esquema de entrada por solicitud (ocho bloques), convenciones del bloque (identificadores REQ-B/RUN-B, estados S0-S7 y R/A/W, solo añadir), plantilla de entrada e índice operativo. Sin solicitudes registradas |
| V1.1 | 2026-10-30 | Esquema ampliado por la adenda de arquitectura (antes de la primera alta): nuevo bloque «Referencias cruzadas» por solicitud (D23, SUG-B-08), con su regla de registro en la sección 5. El resto del esquema no cambia |
