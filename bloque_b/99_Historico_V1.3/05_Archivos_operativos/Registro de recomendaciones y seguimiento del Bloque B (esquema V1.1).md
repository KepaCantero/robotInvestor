# Registro de recomendaciones y seguimiento del Bloque B

VERSIÓN V1.1 · Archivo operativo del Bloque B de la arquitectura Robot Investor · Ciclo de vida completo de las recomendaciones REC-B: alta de cada recomendación emitida (con su plan de análisis, premisas falsables, señales de seguimiento y condiciones de invalidación), estados de seguimiento a remisión del Orquestador con la retroalimentación del Broker Personal (CT-B-12), invalidaciones y retiradas · Propietario de escritura y mantenimiento: Documentador para el Analizador de Mercados · Lectura: Analizador de Mercados y Orquestador técnico para el Analizador de Mercados; extractos al Auditor de Mercados por el CT-B-07 · Gobernanza: «Documento 0 --- Protocolo maestro del Bloque B» (óptima V1.1, 30/10/2026); régimen operativo: system prompt del Documentador para el Analizador de Mercados (óptima V1.1) · Esquema ampliado por la «Adenda de arquitectura --- Bloque B» (V1.0, 30/10/2026): dos campos nuevos por REC-B (evaluaciones separadas y régimen de referencia; D17, D18) y sección de previsiones y resultados PRV-B (D12) · es-ES

## 1. Rol del archivo en la arquitectura del Bloque B

Este archivo es la memoria que cierra el bucle falsable de las recomendaciones del bloque: lo prometido (premisas y señales), lo observado (resultados que el Broker comunica) y lo corregido (invalidaciones y retiradas) viven en el mismo registro, vinculados a la misma REC-B. Cada recomendación del listado REC-B se da de alta aquí tras la autorización de salida del ciclo; cada evento de retroalimentación del Broker Personal (CT-B-12) se registra como seguimiento; cada invalidación abre un estado de revisión que solo el ciclo de análisis resuelve. Es el archivo que hace falsables las tesis del bloque en el tiempo: una recomendación sin seguimiento registrado es una promesa sin prueba. Desde la V1.1 es también la memoria de las previsiones verificables del bloque (serie PRV-B, sección 5.5): toda predicción evaluable del ciclo --- de la tesis, de una REC-B o de la máquina de proyecciones --- se registra aquí con su fecha de evaluación, y a su vencimiento recibe resultado observado, error y causa clasificada (datos · modelo · régimen · incertidumbre irreductible); las previsiones fallidas no se borran ni se reescriben: se registran (D12).

La conexión con el futuro Bloque C es contexto externo: el Broker Personal clasificará y repartirá las REC-B cuando ese bloque exista, y este registro prepara esa trazabilidad (campo de clasificación) sin abrir ningún canal ni código reservado (2.4 del Documento 0). El registro no interpreta la retroalimentación: la custodia con fidelidad; la recalibración es del Analizador.

## 2. Ficha de uso para los agentes

**Documentador de Mercados (escritura y mantenimiento).** Alta de REC-B por remisión del Analizador (CT-B-04) solo tras verificar la constancia de autorización de salida en el Registro de solicitudes; registro de seguimiento por remisión del Orquestador (CT-B-12) con fidelidad al evento; invalidaciones y retiradas como entradas nuevas que referencian a la original; mantenimiento híbrido D6.

**Analizador de Mercados (lectura).** Consulta el archivo para el seguimiento de sus recomendaciones emitidas: la retroalimentación te llega por notificación del Orquestador y como calibración para fases F5 de ciclos de revisión del mismo objeto (4.5 y Anexo I.7 de su prompt); este archivo es la única memoria viva de las REC-B.

**Orquestador de Mercados (lectura).** Consulta el archivo para verificar que las REC-B autorizadas quedaron dadas de alta (11.3 de su prompt), para remitir la retroalimentación del CT-B-12 y para componer los extractos al circuito.

**Auditor de Mercados (vía extractos CT-B-07).** No accede directamente: recibe los extractos que el Orquestador remita con el material de revisión.

## 3. Convenciones de formato

1. **Identificadores únicos e inmutables**: cada recomendación lleva su identificador REC-B con ordinal secuencial del bloque, de cuatro dígitos, asignado en el alta (REC-B-0001, REC-B-0002…). El ordinal es del bloque y no se reasigna jamás; una recomendación retirada conserva su identificador como historial.
2. **Fechado ISO 8601** en todos los eventos: alta, seguimientos, cambios de estado.
3. **Registro de solo añadir**: los cambios de estado son entradas nuevas con fecha y motivo; ninguna recomendación se borra nunca (el historial de errores es parte del capital metodológico del bloque); la retirada es lógica.
4. **Once campos obligatorios del alta** (formato REC-B del diseño del Analizador, V1.1, sección 11.3): identificador · objeto y familia · dirección · invertibilidad · tesis con convicción · premisas falsables · horizonte · riesgos · señales de seguimiento · condiciones de invalidación · trazabilidad (request_id, run_id, PLAN-B, PKT-B de origen y fecha de autorización).
5. **Clases de investibilidad (AM-10)**: invertible hoy (dirección operable y REC-B completa) · vigilancia pre-IPO (sin dirección operable, vigilancia activa) · informativa (nunca genera alta: la vigilancia informativa del informe no alcanza el listado ni este registro).
6. **Estados del ciclo de vida de una REC-B**: emitida → en seguimiento → (en revisión) → retirada o activa; con la clasificación Bloque C como atributo, no como canal.
7. **Fidelidad al evento en el seguimiento**: lo que el Broker comunica se registra como lo comunica (decisión, resultado, invalidación alegada, clasificación); el registro no interpreta ni descarta.
8. **Esquema 1.0 del ecosistema**: los valores controlados (direcciones, convicciones, estados) son los compartidos; este archivo solo fija la disposición.

## 4. Qué se registra y qué no

Se registran: las recomendaciones REC-B emitidas por los ciclos del bloque tras su autorización de salida (con sus once campos), los eventos de retroalimentación del Broker Personal (CT-B-12) con su decisión, resultados observados, invalidaciones alegadas y clasificación Bloque C si la hay, las invalidaciones confirmadas y las retiradas con su motivo, y los vínculos con los ciclos de revisión del mismo objeto. No se registran: recomendaciones sin autorización de salida verificada (incidencia grave: se rechaza el alta y se escala), recomendaciones de otros bloques (el Bloque A tiene sus propios registros), datos personales del inversor o credenciales (nunca), ni interpretaciones del Documentador sobre el fundamento de una invalidación (el registro custodia; el análisis recalibra).

## 5. Estructura del archivo

### 5.1 Índice operativo

| Campo | Valor |
|---|---|
| Versión del esquema | 1.0 |
| REC-B registradas | 0 (nacimiento del archivo: sin recomendaciones aún) |
| REC-B por estado | --- |
| Última revisión del índice | 2026-10-28 (nacimiento del archivo) |

### 5.2 Fichas de recomendación (sección principal)

*(Sin recomendaciones aún: el archivo nace vacío con el bloque. La primera REC-B autorizada abre REC-B-0001.)*

Plantilla de alta (los once campos):

> **REC-B-XXXX — [objeto]**
>
> **Identificación.** **REC-B:** REC-B-XXXX · **Fecha de alta:** AAAA-MM-DD · **Estado:** emitida
>
> **Recomendación.** **Objeto y familia:** … · **Dirección:** [alcista / bajista / neutral / vigilancia activa (pre-IPO)] · **Invertibilidad:** [invertible hoy / vigilancia pre-IPO] · **Tesis con convicción:** [tesis falsable enunciada · convicción: alta / media / baja]
>
> **Falsabilidad.** **Premisas falsables:** [cada premisa: qué afirma, con qué evidencia, cómo se comprobaría, con qué horizonte] · **Condiciones de invalidación:** [qué hechos la invalidan]
>
> **Seguimiento.** **Horizonte:** … · **Señales de seguimiento:** [señales tempranas observables] · **Riesgos:** [riesgos principales con su mecanismo]
>
> **Evaluaciones separadas y régimen (V1.1).** **Evaluaciones:** [atractivo del mercado · calidad de la empresa · atractivo bursátil (expectativas y valoración) · accesibilidad de instrumentos] · **Régimen de referencia:** [régimen del ciclo en el que vale la recomendación; su cambio es causa de revisión]
>
> **Trazabilidad.** **request_id:** … · **run_id:** … · **PLAN-B:** … · **PKT-B:** … · **Autorización de salida:** AAAA-MM-DD · **Origen:** remisión DOC-B del Analizador (CT-B-04)

Plantilla de entrada de seguimiento (CT-B-12):

> **Seguimiento de REC-B-XXXX — [fecha del evento]**
>
> **Evento.** **Fuente:** remisión del Orquestador (CT-B-12) · **Fecha del evento:** …
>
> **Contenido.** **Decisión del Broker:** [seguimiento / aplazamiento / descarte] · **Resultados observados:** [los que el Broker comunica] · **Invalidación alegada:** [fundamento alegado, si existe] · **Clasificación Bloque C:** [la que el Broker declare, si existe]
>
> **Estado resultante.** [en seguimiento / en revisión] · **Fecha:** … · **Notificación al Analizador:** [fecha]

### 5.3 Registro de mantenimiento

| Fecha | Tipo | Alcance y resultado |
|---|---|---|
| 2026-10-28 | Nacimiento | Archivo creado con sus convenciones (once campos, estados, fidelidad al evento) y plantillas de alta y de seguimiento; sin recomendaciones registradas |

### 5.4 Historial de altas y cambios de estado

*(Sin entradas aún: se abre con la primera REC-B.)*

### 5.5 Sección de previsiones y resultados (serie PRV-B; V1.1, D12)

*(Sin previsiones aún: se abre con la primera previsión verificable registrada a remisión del Orquestador al cierre de un ciclo.)*

Plantilla de alta de previsión:

> **PRV-B-XXXX — [variable o acontecimiento previsto]**
>
> **Identificación.** **PRV-B:** PRV-B-XXXX · **Origen:** [REC-B-XXXX / REQ-B-XXXX / PLAN-B-vN] · **Método y versión:** [method_id y artefacto del Motor, o «juicio experto» con su fundamento] · **Fecha de emisión:** AAAA-MM-DD · **Horizonte:** … · **Fecha de evaluación programada:** AAAA-MM-DD
>
> **Previsión.** **Variable:** [enunciada de modo evaluable] · **Valor inicial y referencia:** [contra qué se medirá] · **Escenario y rango (o dirección):** … · **Clase de cifra:** [determinista / estimación estadística / juicio experto] · **Condiciones de validez:** [incluido el régimen de referencia]
>
> **Resultado (a su vencimiento).** **Resultado observado:** … · **Error:** [absoluto, porcentual o direccional según la variable] · **Fecha de evaluación efectiva:** … · **Causa del error (si procede):** [datos · modelo · régimen · incertidumbre irreductible]

Reglas de la serie: alta a remisión del Orquestador al cierre del ciclo (7.6 del prompt del Documentador); evaluación disparada por la fecha programada o por el evento CT-B-12 que la toque, con el resultado comunicado referenciado en la entrada de seguimiento; entradas append-only: las previsiones que no se cumplan se registran con su causa, nunca se borran ni se reescriben; la serie alimenta el cuadro de mando del Orquestador (familia calidad predictiva) y la calibración CT-B-11.

## 6. Reglas de mantenimiento y ciclo de vida

Mantenimiento híbrido (D6): revisión post-solicitud en 48 horas naturales desde la entrega autorizada (verificar que las REC-B del listado quedaron dadas de alta y que su trazabilidad está completa) y revisión mensual ligera en la primera semana natural del mes (índice por estado, señales de seguimiento vencidas, estados colgados en revisión sin resolución, coherencia con el Registro de solicitudes). Desde la V1.1, la revisión mensual evalúa además las previsiones PRV-B vencidas: resultado observado, error y causa clasificada (datos · modelo · régimen · incertidumbre irreductible), registrados como entrada nueva en la sección 5.5 (D12). Las reglas completas están en la sección 7 del prompt del Documentador de Mercados. Las REC-B en revisión por invalidación alegada se resuelven por el seguimiento del registro o por un ciclo de revisión del objeto asignado por el Orquestador; la resolución se registra como entrada nueva que referencia a la original.

## 7. Control de versiones del archivo

| Versión | Fecha | Cambios |
|---|---|---|
| V1.0 | 2026-10-28 | Nacimiento del archivo: convenciones propias del bloque (once campos del formato REC-B, estados del ciclo de vida, fidelidad al evento CT-B-12, solo añadir), plantillas de alta y de seguimiento e índice operativo. Sin recomendaciones registradas |
| V1.1 | 2026-10-30 | Esquema ampliado por la adenda de arquitectura (antes de la primera alta): dos campos nuevos por REC-B (evaluaciones_separadas y régimen_de_referencia; D17, D18) y nueva sección 5.5 de previsiones y resultados con la serie PRV-B, su plantilla y sus reglas (D12). Las once campos base no cambian |
