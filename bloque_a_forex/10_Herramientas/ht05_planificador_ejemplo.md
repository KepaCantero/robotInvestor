# Especificación — HT-05 Planificador (ejemplo de configuración por defecto)

**Bloque A Forex · Robot Investor · actualizado V1.1 (03/11/2026)** · Subordinado al Documento 0 del Bloque A Forex V1.1 (la versión original de esta especificación procedía del Bloque A general óptima V4.0, 01/11/2026). Actualización V1.1: sección 7 (ciclos C6 de seguimiento encargado, plazos de las consultas CT-23, recordatorios de credenciales CT-25 y de hitos H5).

**Estado de madurez (R22):** documentado (especificación de referencia). No implementado ni validado.

## 1. Función

HT-05 es la herramienta determinista que **dispara** los ciclos programados del bloque (secciones 4.4 y 7.1 del Documento 0). No razona ni decide: emite un evento de disparo al agente responsable, que es quien actúa. Su usuario es el **Coordinador de Peticiones y Consultas** (AG-01), que la configura desde F10 cuando el Broker cambia la periodicidad por CT-04. Programa:

- **C1 · Ciclo periódico** (ejecución y entrega del informe).
- **C4 · Mantenimiento continuo de conocimiento** (DOC-A, DOC-M, BFA; barridos de HT-02).
- **C5 · Evaluación y aprendizaje** (Evaluador: resolución de pronósticos y revisiones periódicas).

Los disparos de C4 y C5 corren en segundo plano y **nunca bloquean** C1–C3 (7.1).

## 2. Zona horaria

- Todas las expresiones se interpretan en la **zona horaria del usuario** guardada en F10 (`zona_horaria`, nombre IANA). Valor por defecto: `Europe/Madrid` (idioma es-ES).
- Se usa la directiva `CRON_TZ=<zona>` por expresión, de modo que «lunes 07:00» sigue siendo las 07:00 locales tras los cambios de horario de verano.
- Ningún disparo se programa entre las 02:00 y las 03:00 locales: en `Europe/Madrid` esa franja no existe el último domingo de marzo y se repite el último domingo de octubre.

## 3. Expresiones cron por defecto (Anexo A)

Formato de cinco campos `minuto hora día-mes mes día-semana` (0 = domingo).

| ID de disparo | Ciclo | Expresión (CRON_TZ=Europe/Madrid) | Momento | Destinatario y acción |
|---|---|---|---|---|
| C1-EJEC | C1 | `0 6 * * 6` | Sábado 06:00 | Coordinador: abre RUN- y emite CT-05 al Analizador (ciclo semanal por clase, F0 con GC0) |
| C1-CONTROL | C1 | `0 18 * * 0` | Domingo 18:00 | Coordinador: comprueba que el RUN- ha superado G3; si no, avisa al Orquestador (prioridad máxima) |
| C1-ENTREGA | C1 | `0 7 * * 1` | Lunes 07:00 | Coordinador: entrega CT-02 al Broker; si G3 no es apto, comunica retraso con plazo estimado |
| C4-DIARIO | C4 | `30 1 * * *` | Diario 01:30 | DOC-A, DOC-M, BFA: agenda de vigilancia (altas, alertas de fuentes) |
| C4-NOVEDADES | C4 | `0 22 * * 5` | Viernes 22:00 | DOC-A, DOC-M, BFA: publican «Novedades» en F7–F9 antes de la ejecución de C1 |
| C4-BARRIDO | C4 | `0 4 * * 0` | Domingo 04:00 | HT-02 sobre F7, F8 y F9 (barrido semanal de enlaces del Anexo A); el agente propietario revisa incidencias |
| C4-REINTENTO | C4 | `0 5 * * 1` | Lunes 05:00 | HT-02 `--ids` sobre las fichas con «Primer fallo» del barrido (25 h después: confirma ROTO, 13.4) |
| C4-MENSUAL | C4 | `0 4 1 * *` | Día 1, 04:00 | Revisión de relevancia (uso en 90 días, temática vigente, redundancia) |
| C4-CT21 | C4 | `0 9 1 * *` | Día 1, 09:00 | Paquete de mantenimiento CT-21 al Orquestador (altas, reparaciones, bajas, % OK, lagunas) |
| C4-TRIMESTRAL | C4 | `0 5 2 1,4,7,10 *` | Día 2 de ene/abr/jul/oct, 05:00 | Veracidad: retractaciones, erratas, refutaciones; recalificación Q |
| C5-DIARIO | C5 | `45 0 * * *` | Diario 00:45 | Evaluador: resolución de los pronósticos PRG- vencidos (F4) |
| C5-CIERRE | C5 | — (evento) | Tras cada CT-02 de C1 | Evaluador: métricas del ciclo cerrado (disparo por evento, no por calendario) |
| C5-MENSUAL | C5 | `0 6 3 * *` | Día 3, 06:00 | Evaluador: métricas mensuales, lecciones, propuestas de ajuste |
| C5-TRIMESTRAL | C5 | `0 7 4 1,4,7,10 *` | Día 4 de ene/abr/jul/oct, 07:00 | Evaluador: recalibración dentro de bandas (12.2), certificados de horizonte |

## 4. Periodicidades del ciclo C1 configurables por el Broker (CT-04)

| Periodicidad | Ejecución | Entrega | Condición adicional |
|---|---|---|---|
| Diario | `0 5 * * 1-5` | `0 7 * * 1-5` | N1 por defecto salvo cambio material (GC0) |
| Semanal (defecto) | `0 6 * * 6` | `0 7 * * 1` | — |
| Quincenal | `0 6 * * 6` | `0 7 * * 1` | Guarda: solo si `(semana_ISO − semana_ancla) mod 2 = 0`; cron no expresa «cada dos semanas» |
| Mensual | `0 6 1-7 * *` | `0 7 1-10 * *` | Guarda: ejecución solo si el día es sábado; entrega el primer lunes posterior a la ejecución |
| Personalizado | Expresión validada | Expresión validada | Intervalo mínimo de 1 día; la entrega debe quedar ≥ 24 h después de la ejecución |

**Trampa conocida:** en cron estándar, si se restringen a la vez día del mes y día de la semana (`0 6 1-7 * 6`), el disparo ocurre cuando se cumple **cualquiera** de los dos, no ambos. Por eso la periodicidad mensual usa una guarda en el disparo en lugar de combinar campos.

Si el Broker fija «día y hora de entrega» (p. ej., `MIE 08:00`), la ejecución se adelanta automáticamente 49 horas (por defecto, sábado 06:00 → lunes 07:00) y se redondea a la hora en punto.

## 5. Reglas de funcionamiento

1. **Idempotencia** (6.2): cada disparo lleva `disparo_id = <ID>-<fecha programada ISO>`; un segundo disparo con el mismo identificador se descarta.
2. **Disparos perdidos**: si el sistema estuvo parado, al reanudarse se ejecuta **una sola vez** cada disparo perdido de C1 cuya entrega aún no haya vencido en más de 24 h, y una vez cada disparo de C4/C5 pendiente; nunca se acumulan repeticiones.
3. **Prioridad**: C1–C3 > C5 > C4. Si coinciden, los ciclos de fondo esperan a que el Orquestador (HT-08) confirme capacidad.
4. **Registro**: cada disparo y su resultado (emitido, descartado por duplicado, recuperado) se anota en F5.
5. **Cambios**: el Coordinador actualiza F10 y regenera el calendario; el cambio surte efecto desde el siguiente disparo, nunca a mitad de un RUN-.
6. **Sin credenciales** (R8): los disparos solo contienen identificadores y parámetros.

## 6. Ejemplo de configuración en F10

```json
{"planificador":{"zona_horaria":"Europe/Madrid","periodicidad_c1":"SEMANAL","semana_ancla_quincenal":null,
 "disparos":[
  {"id":"C1-EJEC","cron":"CRON_TZ=Europe/Madrid 0 6 * * 6","destino":"AG-01","accion":"ABRIR_RUN"},
  {"id":"C1-ENTREGA","cron":"CRON_TZ=Europe/Madrid 0 7 * * 1","destino":"AG-01","accion":"ENTREGAR_CT02"},
  {"id":"C4-BARRIDO","cron":"CRON_TZ=Europe/Madrid 0 4 * * 0","destino":"AG-14,AG-15,AG-16","accion":"HT02_BARRIDO"},
  {"id":"C4-REINTENTO","cron":"CRON_TZ=Europe/Madrid 0 5 * * 1","destino":"AG-14,AG-15,AG-16","accion":"HT02_REINTENTO_ROTOS"},
  {"id":"C5-DIARIO","cron":"CRON_TZ=Europe/Madrid 45 0 * * *","destino":"AG-20","accion":"RESOLVER_PRG_VENCIDOS"}]}}
```

## 7. Agendas añadidas en V1.1 (Documento 0 Forex, 4.4, 7.1 C6, 7.9, 7.10 y 7.11)

| Agenda | Disparo | Destino | Regla |
|---|---|---|---|
| **C6 · seguimiento encargado** | Por encargo `ACTIVO` de F11, según su frecuencia (CT-24): DIARIA (siguiente día hábil), SEMANAL, QUINCENAL, MENSUAL, TRIMESTRAL o PERSONALIZADA (lista de fechas o cada *n* días) | AG-01 (`ABRIR_RUN_SEGUIMIENTO`) | Prioridad inferior a C1–C3; si coincide con un C1 en que la opción es VIGENTE, se omite y se anota en F11; si dos C6 del mismo encargo se solapan, se fusionan; la cancelación borra los disparos pendientes de inmediato; al pasar la fecha de fin, FINALIZADO |
| **CT-23 · vencimiento de consultas** | `plazo_respuesta` de cada CNS-FX- pendiente (BLOQUEANTE: 4 h en ad hoc o hasta la hora que permite la entrega periódica, como tarde domingo 18:00; NO_BLOQUEANTE: 24 h o hasta la entrega) | AG-01 (`VENCER_CONSULTA`) | Al vencer: estado VENCIDA, supuesto declarado aplicado y reanudación de la parte pausada |
| **CT-25 · recordatorios de credenciales** | Cada 7 días desde la solicitud mientras el servicio siga degradado (máximo 3) | AG-01 (`RECORDAR_CREDENCIAL`) | Una credencial DENEGADA no genera recordatorios |
| **H5 · hitos** | Fecha de cada HIT-FX- de los PRG H5 abiertos | AG-20 (`RESOLVER_HITO`) | Resolución sin fuga; resultado y estado del PRG H5 en F6 |

Implementación de referencia en el ejecutor: `bloque_a_forex/herramientas/ht05_planificador.py` (`proximo_ciclo_seguimiento`, `vencimiento_consulta`), `seguimiento.Seguimientos.pendientes`, `comunicacion.Consultas.vencer`, `comunicacion.Credenciales.recordatorios` y `evaluador.Evaluador.resolver_hitos` (estado: implementado con pruebas, R22).

```json
{"id":"C6-SEG-FX-2026-0003","cron":"CRON_TZ=Europe/Madrid 30 8 * * 1","destino":"AG-01","accion":"ABRIR_RUN_SEGUIMIENTO",
 "seg_id":"SEG-FX-2026-0003","frecuencia":"SEMANAL","prioridad":"INFERIOR_A_C1_C3"}
```

