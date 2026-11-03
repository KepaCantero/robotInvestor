# Plan de pruebas del Bloque A — batería mínima de integración, regresión y calidad

VERSIÓN V1.0 · 01/11/2026 · Documento de garantía de calidad del Bloque A · Coherente con el
Documento 0 — Protocolo maestro del Bloque A (Versión óptima V3.0, secciones 2.7.7, 9.4 y
Anexo A) · Regla de gobierno: las pruebas de la batería son el criterio para declarar
**validado** un componente (regla crítica 19); ningún cambio metodológico se da por vigente sin
sus pruebas de regresión registradas · es-ES

## 1. Propósito y alcance

Este documento fija la batería mínima de pruebas de integración, regresión y calidad del Bloque
A, derivada de la sección 14 de la petición maestra de modificación y optimización (20 pruebas).
Cada prueba define sus entradas, sus condiciones previas, su resultado esperado, su criterio de
aprobación y su estado. **Regla de honestidad del registro**: el estado de cada prueba distingue
expresamente lo diseñado de lo ejecutado; ninguna prueba se declara aprobada sin evidencia de
ejecución registrada en este documento (sección 4).

Estados posibles de una prueba: **diseñada** (especificada, pendiente de ejecución),
**ejecutada_aprobada** (con evidencia registrada), **ejecutada_fallida** (con incidencia y
plan), **bloqueada** (depende de un componente pendiente) o **no_aplicable** (justificado).

## 2. Condiciones generales de ejecución

- Las pruebas P-01 a P-20 son pruebas de **integración multiagente**: exigen el entorno de
  ejecución del bloque con sus agentes activos, sus archivos y sus contratos operativos. En la
  fecha de esta versión el paquete está **documentado** y su servicio de cálculo
  **implementado** en producción, pero el entorno multiagente de pruebas con datos reales no
  está desplegado: por eso están **diseñadas** y no ejecutadas.
- Las pruebas de verificación documental (V-01 a V-06, sección 3.2) son **ejecutadas** por
  herramienta determinista sobre el propio paquete, con su evidencia en la sección 4.
- Las pruebas que involucren cálculos del Motor se ejecutan con datos sintéticos deterministas
  (semilla registrada) y sus artefactos reproducibles referenciados.

## 3. La batería mínima

### 3.1 Batería de integración, regresión y calidad (P-01 a P-20; diseñadas)

| ID | Prueba | Entradas y condiciones previas | Resultado esperado | Criterio de aprobación | Estado |
|---|---|---|---|---|---|
| P-01 | Misma tendencia, implicaciones distintas por clase de activo | Una tendencia multiactivo (p. ej. digitalización de la red eléctrica) con peticiones para ACC, FIR, FX, CMD y CHR | El Analizador clasifica la clase en la fase 02; el Motor aplica el perfil o perfiles correspondientes y las fichas compatibles por clase; los entregables distinguen las implicaciones | Cada clase produce su análisis con su perfil declarado en la respuesta CT-11 y en el Registro (V1.2); sin mezcla de indicadores | Diseñada |
| P-02 | Activo híbrido con dos perfiles combinados | Un ETF de bonos denominados en divisas (PERF-ETF + PERF-FIR + PERF-FX) | El Motor combina los perfiles de forma declarada, explicita los riesgos cruzados y no fuerza clasificación única | La respuesta declara la lista de perfiles combinados y los riesgos cruzados; registro con clase MIX | Diseñada |
| P-03 | Investigación con datos insuficientes | Serie con historia inferior al mínimo del perfil aplicable | El Motor declara la insuficiencia y rechaza o sirve con limitación; el Analizador documenta el cierre legítimo (R15) | Sin datos inventados; insuficiencia registrada en la ejecución y, si procede, en F1/F3 | Diseñada |
| P-04 | Datos obsoletos, revisados o contradictorios | Serie con revisión posterior y dos fuentes con cifras discrepantes | La normalización temporal (2.7.6) registra las fechas de publicación y de conocimiento; la discrepancia se registra; el dato usado declara su versión | Toda cifra lleva su fecha de conocimiento; la contradicción queda en F2 y no se resuelve por popularidad | Diseñada |
| P-05 | Hipótesis central refutada antes de cálculos adicionales | Ejecución donde el CT-14 devuelve objeción fuerte confirmada | No se ejecutan cálculos adicionales para sostener la hipótesis; transición a invalidada según la máquina de estados | El gates_record y el historial de F1 muestran la parada y la transición legal | Diseñada |
| P-06 | Cálculo con unidades incompatibles | Petición CT-11 con series en unidades no convertidas | El STC-1 o el Motor rechaza con motivo o exige aclaración; nunca convierte en silencio | Rechazo/aclaración registrada en el Registro de cálculos; sin resultado entregado | Diseñada |
| P-07 | Solicitud duplicada resuelta por idempotencia | Reemisión de una petición CT-11 con el mismo identificador | Se devuelve el artefacto registrado sin recalcular ni duplicar registros | Una sola entrada del Registro; respuesta idéntica (clave de idempotencia V1.2) | Diseñada |
| P-08 | Agotamiento del presupuesto de investigación | Ejecución con presupuesto del nivel agotado | Cierre con estado explícito de alcance reducido, agenda de seguimiento y sin omisión de controles de integridad (2.7.5) | El cierre documenta las lagunas; gates_record de las fases ejecutadas intacto; sin datos inventados | Diseñada |
| P-09 | Fallo de un agente y recuperación de estado | Interrupción simulada de un agente de apoyo durante la fase 03 | Reintento con límites, recuperación desde los archivos y modo degradado declarado | Sin pérdida de trazabilidad; el estado recuperado coincide con los archivos; limitaciones declaradas | Diseñada |
| P-10 | Interrupción durante una tarea paralela | Búsqueda paralela (CT-01 y CT-02) interrumpida a mitad | Puntos de sincronización y reanudación sin duplicar fuentes ni evidencias | Duplicados detectados por hash en F2; agenda de lo pendiente | Diseñada |
| P-11 | Mensajes con contratos incompatibles o campos ausentes | Mensaje con campo fuera de contrato y mensaje sin campo obligatorio | Rechazo con motivo, procesado conforme al contrato vigente ignorando el campo no previsto, y registro | La respuesta declara la discrepancia; incidencia registrada en ambos lados | Diseñada |
| P-12 | Conclusión bloqueada por un error determinista | Cifra citada sin soporte de cálculo referenciado | G3 (control bloqueante) impide presentar la conclusión como válida hasta su corrección | El gates_record registra el bloqueo; el entregable no sale con la cifra | Diseñada |
| P-13 | Auditoría proporcional al riesgo | Ciclo con material de bajo riesgo y otro con hallazgo material potencial | La auditoría asíncrona no bloquea tareas de bajo riesgo y detecta el problema material | Hallazgo con severidad correcta; cero bloqueos indebidos del servicio | Diseñada |
| P-14 | Evaluación histórica sin fuga de información | Contraste de un pronóstico congelado (F4) con lo ocurrido | El contraste usa solo información disponible en la fecha de conocimiento; el resultado posterior se añade sin reescribir | La entrada original de F4 permanece intacta; el contraste queda registrado (nivel B del aprendizaje) | Diseñada |
| P-15 | Conservación de pronósticos y resultados posteriores | Corrección de un pronóstico congelado | Nueva versión referenciada; la entrada original conserva valores, supuestos y fecha (R16) | Historial de F4 muestra las dos versiones y el vínculo | Diseñada |
| P-16 | Alta concurrencia sin saturación | Ráfaga de peticiones CT-11 y de ejecuciones del Analizador | Cola y prioridades del Motor (4.3) y límites del Orquestador evitan la saturación; lo pospuesto se declara | Ninguna petición perdida en silencio; pospuestos con identificador declarado | Diseñada |
| P-17 | Cambio de versión de un método con reproducción | Publicación de una versión nueva de una ficha del Catálogo | Las re-ejecuciones CT-12 citando la versión anterior reproducen el resultado anterior dentro de tolerancia | Diferencia dentro de la tolerancia de la ficha; versiones coexisten sin sobrescritura | Diseñada |
| P-18 | Cálculo adicional sin valor informativo suficiente | Solicitud de cálculo cuyo resultado no puede cambiar la conclusión | El sistema lo omite o lo declara de escaso valor según las reglas de parada (2.7.5) y el valor informativo esperado | La omisión queda registrada con su justificación; sin consumo innecesario | Diseñada |
| P-19 | Instrumento con liquidez o costes inviables | Exposición con costes, spread o restricciones que anulan el beneficio | El filtro de accesibilidad (9.1 del Analizador) y el perfil declaran la inviabilidad; la tendencia puede seguir vigente | La recomendación de F3 no es «profundizar» por esa vía; inviabilidad documentada | Diseñada |
| P-20 | Tendencia real que no es una oportunidad atractiva | Tendencia validada con activos sobrevalorados o captura de valor en otro eslabón | El bloque separa la validez de la tendencia (E/T/M) de la identificación de la exposición (F3) y no produce recomendación | Los dos registros dicen cosas distintas y consistentes; sin mezcla de indicadores | Diseñada |

### 3.2 Pruebas de verificación documental (V-01 a V-06; ejecutadas con la óptima V3.0)

| ID | Prueba | Método | Resultado | Estado |
|---|---|---|---|---|
| V-01 | Ausencia de restos de la denominación antigua del Motor fuera del registro de cambios e historial | Búsqueda determinista de «relacionadas con Divisas» en el paquete | Los restos solo aparecen en registros históricos (Anexos H, denominaciones históricas y notas de versión) | Ejecutada_aprobada |
| V-02 | Coherencia de versiones declaradas (Documento 0 sección 5.1 y Anexo D frente a nombres de archivo) | Comparación determinista de versiones citadas frente a los nombres de archivo del paquete | Coincidencia de versiones en las filas actualizadas; desviaciones documentadas en la sección 4 | Ejecutada (con incidencias menores documentadas) |
| V-03 | Coherencia de identificadores nuevos (F3, F4, OPP-, PRG-, PERF-xx) en todo el paquete | Búsqueda determinista de los identificadores en los documentos que deben citarlos | Los identificadores aparecen en los documentos que corresponden (Documento 0, prompts, registros, catálogo, perfiles, listados) | Ejecutada_aprobada |
| V-04 | No reintroducción del Opportunity Score | Búsqueda determinista de «Opportunity Score» en el paquete | Solo aparece en su declaración de retirada (F1, F3, Documento 0); sin uso como puntuación vigente | Ejecutada_aprobada |
| V-05 | Coherencia del recuento de reglas críticas (R1–R23) | Conteo de reglas en la sección 0 del Documento 0 y referencias R19–R23 en el resto del paquete | Veintitrés reglas presentes; las referencias externas citan solo R1–R23 | Ejecutada_aprobada |
| V-06 | Estructura de los documentos actualizados (encabezados y tablas bien formadas) | Conversión de los .md a .docx con herramienta determinista y verificación del índice de encabezados | Estructura válida; las tablas críticas (inventario de agentes, matriz de archivos, glosario) conservan su forma | Ejecutada_aprobada |

La evidencia de ejecución de V-01 a V-06 (script determinista, fecha y resultados) se registra
en la sección 4 y en el README de la entrega.

## 4. Registro de ejecuciones y evidencia

| Fecha | Prueba | Entorno | Resultado | Evidencia |
|---|---|---|---|---|
| 01/11/2026 | V-01 a V-06 | Paquete óptima V3.0 (verificación documental determinista) | Aprobadas con incidencias menores documentadas | Script de verificación (scripts/v30_verificacion_coherencia.py); resultados resumidos en el README (sección de verificaciones) |
| — | P-01 a P-20 | Entorno multiagente (pendiente de despliegue) | Diseñadas; pendientes de ejecución | — |

Nota de estado (regla crítica 19): con esta batería, los componentes del paquete V3.0 quedan
**documentados** (y el servicio del Motor, **implementado** en producción con su lote de
fichas); **ningún componente se declara validado** hasta que las pruebas P-01 a P-20 se
ejecuten en el entorno multiagente y su evidencia se registre aquí.

## 5. Procedimiento de mantenimiento

1. Toda modificación metodológica (nivel C del circuito de aprendizaje, 2.7.7) añade o actualiza
   las pruebas de regresión pertinentes antes de su aprobación.
2. La revisión trimestral del Documento 0 (9.4) comprueba el estado de la batería y su evidencia.
3. La activación de perfiles (P1/P2) exige las pruebas P-01, P-02, P-03 y P-19 ejecutadas sobre
   el perfil afectado, además de las pruebas de sus fichas.
4. Las incidencias de pruebas fallidas se registran como hallazgos del circuito de auditoría, con
   su severidad y su clase de control (regla crítica 22).

## 6. Registro de versiones del documento

| Versión | Fecha | Cambios |
|---|---|---|
| V1.0 | 01/11/2026 | Primera versión, aplicada con la petición maestra de modificación y optimización del Bloque A: batería mínima de 20 pruebas de integración, regresión y calidad (P-01 a P-20, diseñadas y pendientes del entorno multiagente) y 6 pruebas de verificación documental (V-01 a V-06, ejecutadas con evidencia del script determinista); condiciones generales, procedimiento de mantenimiento y regla de estados (diseñada, ejecutada, aprobada, fallida, bloqueada). |
