# BLOQUE A — VERSIÓN ÓPTIMA V3.0 · REFORMA DE ALCANCE MULTIACTIVO Y DE MADUREZ DE COMPONENTES

## Índice de la entrega y registro de la actualización (01/11/2026)

**Proyecto:** Ecosistema Robot Investor · **Bloque:** A (Analizador de Tendencias de Inversión)
**Registro formal:** es-ES · **Fecha:** 01/11/2026 · **Estado:** paquete canónico vigente
**Base:** óptima V2.2 (Integración de conocimientos de agentes, 01/11/2026)
**Origen:** petición maestra de modificación y optimización del Bloque A y recomendación de implantación que la acompaña

---

## 1. Qué es esta entrega

Esta entrega aplica la **petición maestra de modificación y optimización del Bloque A** como paquete
coordinado de actualización conforme al procedimiento 5.3 del Documento 0 (actualización de tipo 3
aprobada por el operador mediante la propia orden de trabajo). La reforma transforma el bloque en
tres dimensiones, con la topología de agentes y canales **inalterada** (ocho agentes operativos,
contratos CT-01 a CT-14 en vigor, reservas CT-15 a CT-22 sin vigor):

1. **Alcance multiactivo.** El bloque detecta tendencias, señales tempranas y oportunidades
   potenciales en **cualquier clase de activo invertible**, con independencia del mercado, la
   región, el horizonte temporal y la estrategia aplicable; distingue operativamente **tendencia,
   exposición y oportunidad** (Documento 0, 1.5) y las registra por separado (F1, F3).
2. **Motor transversal con perfiles.** El agente de cálculo pasa a denominarse **«Motor de Cálculo
   Avanzado para el Analizador de Tendencias de Inversión»** y deja de ser un motor especializado
   en divisas: su arquitectura es un **núcleo transversal común** (módulos MC-01 a MC-08 y
   servicios técnicos STC-1 a STC-4) más **perfiles de clase de activo versionados** (PERF-xx),
   combinables de forma declarada en activos híbridos, con secuencia de selección en trece pasos
   y clasificación del activo en el Orquestador de Cálculo.
3. **Madurez y gradualidad.** Se integran como reglas críticas R19 a R23 las tres restricciones de
   implantación de la recomendación adjunta a la petición: **estados de madurez** (documentado,
   implementado, validado), **cobertura sin obligación de ejecución** (el inventario de
   conocimientos define cobertura, no una lista de operaciones obligatorias; activación bajo
   demanda) e **implantación gradual y priorizada** (núcleo transversal P0 fiable primero,
   perfiles comprobados P1 después, ampliación documentada P2), más la separación de controles
   (R22) y la política de secretos (R23).

## 2. Inventario canónico del paquete

| Carpeta | Contenido | Versión vigente |
|---|---|---|
| 01_Gobernanza | Documento 0 — Protocolo maestro del Bloque A | óptima V3.0 |
| 02_System_prompts | 14 system prompts: Analizador; Orquestador técnico; Auditor; Documentador para el Analizador; Buscador de fuentes avanzadas; Documentador para el Motor; Analista de hipótesis contrarias; Flujo de Investigación (en transición); Motor de Cálculo Avanzado; módulos MC-01 a MC-08 | Analizador V2.1; Orquestador, Auditor, Documentador y Buscador V2.2; Documentador del Motor V1.8; Contrarias V1.3; Flujo V1.1; Motor V3.0; MC-01 a MC-08 V1.1 |
| 03_Conocimientos | Mapa de conocimientos del Motor | V2.0 (cobertura transversal y perfiles) |
| 04_Catalogo | Catálogo de cálculos del Motor; Perfiles de clase de activo del Motor | Catálogo V3.0 (catalog_version 3.0); Perfiles V1.0 |
| 05_Listados | 8 fichas de funciones, tareas y cometidos | Motor V3.0; Analizador, Auditor, Orquestador, Buscador, Documentador para el Analizador y Documentador para el Motor V2.1; Contrarias V1.1 |
| 06_Archivos_operativos | Registro maestro de tendencias (F1); Registro de evidencia y afirmaciones (F2); Registro de oportunidades e hipótesis cuantitativas (F3, nuevo); Registro de pronósticos congelados (F4, nuevo); Registro de cálculos; Historial de auditorías; Documentación para el Analizador (V2.7); Documentación para el Motor (V2.3); Fondo metodológico (V2.3); Registro de Fuentes Fiables (V2.4); Módulo de automatización (V1.0) | F1 V1.1; F2 V1.1; F3 V1.0; F4 V1.0; Registro de cálculos V1.2; Historial V1.1 |
| 07_Objetivos | Objetivos del Bloque A | óptima V2.1 (86 objetivos, 9 dimensiones) |
| 08_Descripcion | Arquitectura del Bloque A — descripción detallada para LLM | V2.0 |
| 09_Pruebas | Plan de pruebas del Bloque A — batería mínima | V1.0 |

## 3. Informe de cambios (archivo, modificación, justificación, efecto)

| Archivo | Modificación | Justificación (sección de la petición maestra) | Dependencias | Efecto esperado |
|---|---|---|---|---|
| Documento 0 | Cabecera V3.0; reglas críticas R19–R23; sección 1.5 (tendencia/exposición/oportunidad); alcance multiactivo (1.1); fila del Motor en 2.2; archivos F3 y F4 en 2.3; papel del Flujo en 2.6; fases 02/08/10; clases de control en 2.7.3; secciones nuevas 2.7.5 (presupuestos y parada), 2.7.6 (canalización y normalización temporal) y 2.7.7 (aprendizaje en tres niveles); RACI ampliado; CT-11 con extensión aditiva y CT-21 ampliada; reglas 10–11 de 4.2; matriz 4.3 y Anexo E con F3/F4; inventarios 5.1/Anexo D/Anexo F/Anexo H; convenciones 5.ª/9.ª/10.ª; glosario ampliado; conflictos 7.2; seguridad (secretos); revisión trimestral ampliada; Anexo A con parámetros nuevos | 3.1–3.3, 4.1, 5.1, 5.2–5.4, 6, 7.1–7.3, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17 | Todos los documentos del paquete | Referencia única de coherencia de la reforma; manda en el conjunto |
| System prompt del Motor | óptima V3.0: renombrado con historia fiel; cobertura multiactiva; reglas 19–21; sección 4.6 (secuencia de selección en trece pasos); sección 15.5 (capa de perfiles); Anexo I al Mapa V2.0 y Perfiles V1.0; referencias a Catálogo V3.0 y Registro V1.2; Anexo H | 5.1, 5.3, 5.4 | Mapa V2.0, Perfiles V1.0, Catálogo V3.0, módulos MC V1.1, Registro de cálculos V1.2 | El Motor sirve a cualquier clase de activo con perfiles, estados y abstinencia |
| Módulos MC-01 a MC-08 | óptima V1.1: cabecera; regla 11 (estados, cobertura y abstinencia); identidad multiactiva por módulo; nota de fichas (FX-* = PERF-FX; transversales); gobierno actualizado | 5.2, 5.3 | Motor V3.0, Mapa V2.0, Perfiles V1.0, Catálogo V3.0 | Competencias transversales con aplicabilidad por perfil declarada |
| System prompt del Analizador | óptima V2.1: cabecera; ecosistema con F3/F4; misión con identificación de exposiciones; sección 9.2 (registro de oportunidades en F3); secciones 13.7 y 13.8; Anexo C.1 con correspondencia PERF-xx; Anexo H | 1, 4.1, 5.2, 12 | F3, F4, Catálogo de perfiles | Exposiciones preliminares registradas y pronósticos congelados sin reescritura |
| System prompt del Orquestador | óptima V2.2: cabecera; clases de control y estados de madurez en 6.2; lectura de F3/F4; Anexo H | 8, 9, 10 | Reglas R19/R22; F3, F4 | Validación determinista con clases de control; supervisión de la cobertura y la madurez |
| System prompt del Auditor | óptima V2.2: cabecera; revisión multiactiva; clases de hallazgo; verificación de estados; Anexo H | 10, 17 | Reglas R19/R22 | Auditoría asíncrona sin bloquear; detección de estados mal declarados |
| System prompts del Documentador (Analizador), Buscador Avanzado y Documentador del Motor | óptima V2.2/V2.2/V1.8: cabecera; cobertura multiactiva de fuentes con declaración de insuficiencia; Anexo H/I | 7.2 | Catálogo de perfiles | Fuentes por clase de activo sin duplicación de normalización |
| System prompt del Analista de hipótesis contrarias | óptima V1.3: cabecera; refutación multiactiva con mecánica causal por familia; registro de cambios | 3.1 (distinción documentadores/buscador); 17 | — | Refutación pertinente por clase de activo |
| System prompt del Flujo de Investigación | óptima V1.1: papel de análisis agregado y mejora metodológica; no controlador operativo | 13 | Documento 0 2.6/2.7.7 | Papel verificable sin facultades no implementadas |
| Mapa de conocimientos del Motor | V2.0 nuevo: cobertura transversal y perfiles; correspondencia áreas A–T; capas P0/P1/P2 con estados; distribución por módulo; pruebas ampliadas; sustituye al Mapa V1.0 (divisas absorbido por PERF-FX) | 5.2, 5.3, 6 | Perfiles V1.0, Catálogo V3.0 | Mapa de cobertura multiactivo con estados y prioridades |
| Perfiles de clase de activo del Motor | V1.0 nuevo: marco (formato, reglas, híbridos) y doce perfiles (ACC, FIR, FX, CMD, ETF, DER, REI, CHR, PRV, ALT, capas TEM y ESG) con estados y prioridades | 5.2 (familias D–O), 6 | Catálogo V3.0, Mapa V2.0 | Especialización por clase de activo versionada y combinable |
| Catálogo de cálculos del Motor | V3.0: cabecera; regla de cobertura (1.2/1.4); ficha ampliada (clases compatibles, prioridad, estado de madurez); clasificación del lote (4.1); registro de versiones | 5.3, 6 | Perfiles V1.0, Plan de pruebas | Métodos activables bajo demanda con clasificación y estados |
| Registro maestro de tendencias (F1) | esquema V1.1: clase de activo, perfiles aplicados, mercados y moneda, vínculos OPP/PRG | 4.1, 12 | F3, F4, Perfiles | Tendencias clasificadas y vinculadas a oportunidades y pronósticos |
| Registro de evidencia y afirmaciones (F2) | esquema V1.1: normalización temporal (fecha de conocimiento, revisión, frecuencia, zona horaria, unidad y divisa, versión de fuente) | 7.3 | Canalización 2.7.6 | Evaluación histórica sin fuga de información |
| Registro de oportunidades (F3) | V1.0 nuevo: ficha de identificación preliminar de exposición con recomendación cualitativa | 12 | F1, F2, Registro de cálculos, CT-21 (reserva) | Memoria de oportunidades sin recomendar inversiones |
| Registro de pronósticos congelados (F4) | V1.0 nuevo: congelación append-only con invalidación y resultado posterior | 11, 12 | F1, F3, Registro de cálculos, CT-19 (reserva) | Evaluación predictiva sin reescritura |
| Registro de cálculos del Motor | esquema V1.2: perfil aplicado, estado de madurez del método, clave de idempotencia | 5.3, 5.4, 10 | Motor V3.0, CT-11 | Trazabilidad de perfil y estados por servicio |
| Historial de auditorías | esquema V1.1: tipo de control y clase de resultado | 10 | Regla R22 | Auditoría síncrona/asíncrona distinguible en el registro |
| Objetivos del Bloque A | óptima V2.1: dimensión 9 nueva (OBJ-79 a OBJ-86) | 15, 17 | Documento 0 V3.0 | Objetivos de cobertura, madurez, oportunidades, pronósticos y presupuestos |
| Descripción de arquitectura para LLM | V2.0: actualizada a la reforma (perfiles, estados, F3/F4, R19–R23, 2.7.5–2.7.7) | 1 | Documento 0 V3.0 | Descripción fiel para ingesta por LLM |
| Plan de pruebas del Bloque A | V1.0 nuevo: batería P-01 a P-20 (diseñadas) y V-01 a V-06 (ejecutadas) | 14, 15.11 | Todos | Criterio de validación declarado y evidencia registrada |
| README de la entrega | V3.0: este documento | 15.2, 15.12, 15.13 | Todos | Informe de cambios, estados, riesgos y despliegue |
| Documentación para el Analizador (V2.7), Documentación para el Motor (V2.3), Fondo metodológico (V2.3), Registro de Fuentes Fiables (V2.4), Módulo de automatización (V1.0) | Sin cambios en esta versión | Son archivos de contenido o herramientas ya alineadas; su ampliación de cobertura se materializa en cargas futuras | — | Declarado en el plan de despliegue (fase 3) |

## 4. Estados de madurez de los componentes (regla crítica 19)

| Componente | Documentado | Implementado | Validado |
|---|---|---|---|
| Documento 0 y system prompts (14) | Sí | Sí (prompts operativos en la línea óptima) | Pendiente (pruebas P-01 a P-20) |
| Núcleo transversal del Motor (MC-01 a MC-08, STC-1 a STC-4, fichas del lote VIGENTE) | Sí | Sí (servicio CT-11/CT-12 en producción) | Pendiente |
| Perfil PERF-FX (divisas, heredero de la especialización V2.2) | Sí | Sí (lote FX implementado) | Pendiente |
| Perfiles PERF-ACC, PERF-FIR, PERF-CMD, PERF-ETF, PERF-DER, PERF-REI, PERF-CHR, PERF-PRV, PERF-ALT y capas PERF-TEM/PERF-ESG | Sí (documentados) | No (fichas propias por publicar; el núcleo transversal sirve con limitación declarada) | No |
| Registros F1 (V1.1) y F2 (V1.1) | Sí | Sí (esquemas publicados) | Pendiente |
| Registros F3 y F4 (V1.0) | Sí | No (entran en operación con la primera ejecución del Analizador bajo la óptima V2.1; primero su alta documental y despliegue) | No |
| Registro de cálculos (V1.2) e Historial (V1.1) | Sí | Sí | Pendiente |
| Batería mínima de pruebas (P-01 a P-20) | Sí (diseñadas) | No (entorno multiagente de pruebas pendiente) | No |
| Verificaciones documentales (V-01 a V-06) | Sí | Sí | Sí (ejecutadas y aprobadas, evidencia en sección 6) |

Ningún componente se declara **validado** fuera de la tabla precedente (regla crítica 19).

## 5. Incompatibilidades, riesgos residuales y decisiones declaradas

1. **Compatibilidad de esquemas.** F1, F2, Registro de cálculos e Historial amplían sus esquemas
   (V1.1/V1.1/V1.2/V1.1) sin renumerar ni reformatear entradas anteriores: los campos nuevos se
   cumplimentan en altas y revisiones posteriores. No se prevé incompatibilidad con las entradas
   de esquemas previos; la verificación del primer ciclo de auditoría lo confirmará.
2. **CT-11 con extensión aditiva.** Los campos de perfil y estados son opcionales para los lados
   cliente (precedente del bloque execution de la óptima V2.1); los lados cliente no exigen
   republicación coordinada obligatoria, aunque se recomienda incorporar la referencia en su
   siguiente iteración natural.
3. **Anexo C del Analizador y valores controlados.** Los valores de asset_class del Analizador
   (lista de correspondencia con el Bloque C) y los códigos PERF-xx del Catálogo de perfiles son
   taxonomías distintas y deliberadamente separadas; la correspondencia queda fijada en el Anexo
   C.1 del Analizador. Riesgo residual: divergencia futura si una de las dos taxonomías se
   amplía sin actualizar la correspondencia; mitigación: la revisión trimestral (9.4) la incluye.
4. **Flujo de Investigación.** Su papel queda fijado como análisis agregado y mejora metodológica
   (no controlador operativo); su activación sigue siendo una propuesta de tipo 3 no aprobada
   (T3-5). Ningún documento del paquete le atribuye facultades operativas.
5. **Evaluador retrospectivo.** El nivel B del circuito de aprendizaje opera de forma limitada
   (revisión trimestral sobre F1 y F4) hasta que existan registros y muestras suficientes; el
   Evaluador de previsiones permanece en transición (2.6).
6. **Cobertura documentada sin implementar (P2).** Los perfiles documentados no implementados
   pueden generar peticiones que el Motor servirá con el núcleo transversal y la limitación
   declarada, o rechazará con motivo. Este comportamiento es el exigido por las reglas críticas
   19 a 21 y no constituye un defecto.
7. **Restos históricos de la denominación de divisas.** Las menciones a «…relacionadas con
   Divisas» que subsisten en el paquete están confinadas a registros de cambios, denominaciones
   históricas y notas de versión (verificación V-01 aprobada).
8. **Sin cambios de topología.** La reforma no añade agentes ni canales; los módulos MC y los
   perfiles son órganos o especificaciones internas del Motor, y F3/F4 son archivos con matriz de
   acceso, no agentes.

## 6. Verificaciones de regresión ejecutadas (V-01 a V-06)

Verificación documental determinista ejecutada el 01/11/2026 sobre el paquete (script
`v30_verificacion_coherencia.py`, evidencia en `scripts/resultado_verificacion_v30.txt`):

- **V-01 Aprobada:** cero restos de la denominación antigua del Motor fuera del historial.
- **V-02 Aprobada:** versiones declaradas (Documento 0, 5.1 y Anexo D) coherentes con los
  archivos del paquete (10 documentos comprobados).
- **V-03 Aprobada:** identificadores nuevos (F3, F4, OPP-, PRG-, PERF-xx, R19–R23, MOT-F27 a
  MOT-F30, OBJ-79 a OBJ-86, P-01 a P-20) presentes en los documentos que deben citarlos
  (35 comprobaciones).
- **V-04 Aprobada:** el Opportunity Score solo aparece en su declaración de retirada o en
  historial; no es puntuación vigente.
- **V-05 Aprobada:** la sección 0 del Documento 0 contiene exactamente 23 reglas críticas (R1–R23).
- **V-06 Aprobada:** estructura de encabezados y tablas bien formada en los 44 documentos .md del
  paquete.

Las pruebas P-01 a P-20 permanecen **diseñadas** y pendientes de ejecución en el entorno
multiagente (Plan de pruebas, sección 4): no se declara ningún componente validado sin su
evidencia.

## 7. Plan de despliegue por fases

| Fase | Contenido | Dependencias | Condición de activación |
|---|---|---|---|
| 1. Publicación del paquete | Esta entrega V3.0 (documentación coordinada) | Ninguna | Efectiva con la publicación (01/11/2026) |
| 2. Despliegue operativo de F3 y F4 | Alta de los archivos en el entorno y primera escritura con la primera ejecución del Analizador bajo su óptima V2.1 | Fase 1; Analizador V2.1 desplegado | Confirmación de escritura en el entorno |
| 3. Ampliación de cobertura documental y de fuentes por clase de activo | Cargas de la Documentación (V2.7→) y del Registro de Fuentes Fiables (V2.4→) por familias; actualización del Fondo metodológico | Fase 2; Documentadores V2.2 y Buscador V2.2 | Por prioridad P de las investigaciones; sin plazo fijo |
| 4. Fichas del Catálogo por clase de activo (P1/P2) | Publicación de fichas PERF-ACC, PERF-FIR, PERF-CMD, PERF-ETF, PERF-DER y sucesivas por el cauce de tipos 3, con sus pruebas | Fase 2; Catálogo V3.0; Perfiles V1.0 | Aprobación del operador por lotes; prioridad según investigaciones |
| 5. Ejecución de la batería P-01 a P-20 | Entorno multiagente de pruebas con datos sintéticos deterministas | Fases 1–2; Motor V3.0 desplegado | Disponibilidad del entorno; evidencia registrada en el Plan de pruebas |
| 6. Validación declarada de componentes | Paso a «validado» de los componentes con pruebas ejecutadas | Fase 5 | Evidencia registrada; revisión trimestral confirma (9.4) |
| 7. Activaciones en transición (cuando proceda) | Evaluador de previsiones (CT-19/CT-20); Flujo de Investigación (CT-22); CT-21 con el Documento 0-B | Fase 6; muestras suficientes del nivel B | Procedimiento 5.5 del Documento 0, siempre tipo 3 |

## 8. Guía de mantenimiento y evolución (síntesis)

- El Documento 0 óptima V3.0 manda en la coherencia del conjunto; su sección 9 fija el procedimiento
  de cambio (propuesta con evidencia e impacto, aprobación del operador, publicación coordinada,
  verificación) y su Anexo A los parámetros calibrables (presupuestos, umbrales, capas P0/P1/P2,
  batería de pruebas).
- Versionado: los cambios menores no rompen contratos (5.2.3); los cambios de interfaz exigen
  actualización coordinada (5.2.4); los JSON no cambian por vía de guía (5.2.5); los esquemas de
  archivos amplían por tipo 3 con conservación del formato de las entradas anteriores.
- Cobertura nueva (clase de activo, método, perfil): siempre por el cauce de tipos 3 del Motor,
  con ficha publicada y pruebas registradas antes de declarar el componente implementado, y con
  la batería mínima antes de declararlo validado.

## 9. Historial de la línea óptima V3.x

| Versión | Fecha | Contenido |
|---|---|---|
| óptima V3.0 | 01/11/2026 | Esta entrega: reforma de alcance multiactivo y de madurez de componentes (petición maestra). |
| óptima V2.2 | 01/11/2026 | Integración de conocimientos de agentes (histórica, paquete anterior). |
| óptima V2.0 | 31/10/2026 | Plataforma de inteligencia de tendencias (histórica). |
