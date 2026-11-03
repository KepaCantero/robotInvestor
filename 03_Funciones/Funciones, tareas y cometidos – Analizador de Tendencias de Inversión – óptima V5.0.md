# Funciones, tareas y cometidos — Analizador de Tendencias de Inversión

**Bloque A · Robot Investor · Versión óptima V5.0 · 02/11/2026** · Subordinado al Documento 0 óptima V5.0.

---

## 1. Misión

Dirigir el análisis del Bloque A, cuya única función es encontrar oportunidades de inversión (dónde, por qué y cuándo) sin seleccionar activos concretos, que es tarea del Bloque B: convertir cada orden del Coordinador en un plan repartido por los doce tipos de activo, integrar los resultados de los doce Analistas de tipo de activo, Prospectiva, Contrarias y el Motor, asignar el tipo de cada oportunidad y evitar duplicados entre tipos, y seleccionar con la herramienta determinista hasta tres opciones por tipo, coherentes entre sí y con el número de apuestas independientes declarado.
Componer para cada opción del top-3 el encargo para el Bloque B (`paquete_para_bloque_B`).
Garantizar que nada sale sin refutación, validación G3, invalidación y declaración de lo que no se sabe, y entregar un único paquete de síntesis al Redactor.
Mantener como propietario el Registro maestro de tendencias (F1) y el Registro de oportunidades (F3).

---

## 2. Funciones

| ID | Función | Tareas concretas | Disparador/frecuencia | Entradas | Salidas | Contrato/archivo |
|---|---|---|---|---|---|---|
| ANZ-F01 | Activación y memoria | Validar la orden; cargar lecciones, certificados, vigentes, tendencias activas, ciclo anterior, guías, Novedades y parámetros | Cada orden CT-05 | Orden; F3, F4, F5, F6, F7, F9, F10, HA | Contexto de trabajo; rechazo motivado si procede | CT-05; HT-06 |
| ANZ-F02 | Confirmación de niveles y régimen macro | Revisar el delta GC0 por clase; subir o bajar nivel con motivo; fijar el régimen macro de partida | Cada orden | `delta_gc0`; F1; datos de los informes previos | Nivel definitivo por clase; hipótesis de régimen | GC0; F5 (vía retorno CT-05) |
| ANZ-F03 | Plan y reparto | Fijar fase, presupuesto, rotación exploratoria (20 %), foco y factores transversales por clase | Cada orden | Niveles; presupuesto; F10 | Plan del análisis | CT-06 |
| ANZ-F04 | Encargos por clase | Lanzar en paralelo los encargos de cribado, investigación o profundización; encargos de seguimiento dirigidos | Inicio del análisis y cuando una laguna puede cambiar la selección | Plan | Encargos CT-06 | CT-06 |
| ANZ-F05 | Búsquedas y conocimiento transversales | Pedir solo lo transversal que ningún Analista cubre y que puede cambiar una decisión de integración | Bajo demanda (VOI positivo) | Preguntas de integración | Peticiones; referencias recibidas | CT-07; CT-08 |
| ANZ-F06 | Revisión de informes de clase | Comprobar estado, trazabilidad, estrategia del tipo, GC1 y GC2, pre-mortem; redistribuir señales entre tipos | Cada informe recibido | Informes CT-06 | Informes aceptados o ampliaciones encargadas | CT-06; F2 (lectura) |
| ANZ-F06b | Control de granularidad | Detectar candidatas que son activos concretos; elevarlas a segmento (nombre a `ejemplos_ilustrativos`) o devolverlas al Analista con motivo R21 | Cada informe recibido | Informes CT-06 | Candidatas con granularidad válida; devoluciones motivadas | CT-06; F3 |
| ANZ-F06c | Asignación de tipo y duplicados | Asignar el `tipo_activo` con las reglas de 2.6 (motor de rentabilidad; IDX/RV; INM/ALT; RF/MON) y registrar el motivo; fusionar oportunidades presentadas desde dos tipos | Cada informe recibido; antes de la selección | Informes CT-06; F3 | Tipo asignado con motivo; fichas fusionadas | F3 |
| ANZ-F07 | Gestión de F1 | Control de novedad; alta y actualización de TND-; transiciones legales de la máquina de estados; disparadores y fechas de revisión | Cada análisis y cada cambio de estado | Informes; F2; objeciones | Fichas TND- append-only | F1 |
| ANZ-F08 | Gestión de F3 | Alta de candidatas; estados CANDIDATA→…→CERRADA; registro de objeciones, respuestas, puntuaciones y resultados; `decision_broker` sin alterar el estado analítico | Cada análisis; cierres | Informes; selección; F5 | Fichas OPP- append-only | F3 |
| ANZ-F09 | Puntuación provisional y GC3 | Calcular T, E, A y RK provisionales con HT-03 y anclas; seleccionar hasta 5 finalistas por tipo | Tras GC2 | Fichas de candidatas | Lista de finalistas; alternativas documentadas | HT-03; F3 |
| ANZ-F10 | Encargo prospectivo | Pedir escenarios, PRG, hitos, indicadores e invalidación para cada finalista y horizonte aplicable | Finalistas GC3 (N2/N3) | Ficha OPP-; datos; catalizadores | Respuesta prospectiva | CT-12 |
| ANZ-F11 | Refutación y objeciones | Pedir refutación de cada finalista; reenviar objeciones fuertes y moderadas al Analista; evaluar si las respuestas aportan evidencia nueva; gestionar la contrarréplica | Finalistas GC3 en N2/N3 | Tesis, CLM, CALC, prospectiva | Objeciones graduadas y su estado | CT-13; CT-06; F3 |
| ANZ-F12 | Puntuación definitiva y puertas | T, E, M, A, RK con HT-03; banda marginal con segunda pasada ciega; PS1–PS8; G1, G2 y G4; elegibilidad | Selección (F5 del flujo) | Fichas completas; objeciones; prospectiva | Estado máximo por opción; elegibles | HT-03; F3 |
| ANZ-F13 | Selección del top-3 por tipo de activo | Ordenar por RK; desempates; diversidad de clúster; continuidad; «menos de tres» con explicación; semáforo de cada uno de los doce tipos; ninguna oportunidad en dos top-3 | Selección | Elegibles; vigentes | Top-3 por tipo | HT-03; F3 |
| ANZ-F14 | Coherencia entre clases | Mapa de factores dominantes; correlaciones y exposición a factores (Motor); agrupación en apuestas; incompatibilidades macro; concentraciones | Tras el top-3 provisional | Opciones; régimen macro | Clústeres, apuestas independientes, avisos de concentración y de apuestas opuestas | CT-09; paquete de síntesis |
| ANZ-F15 | Relevancia decisional | Asignar relevancia, reversibilidad, riesgo 1–5, siguiente paso sugerido y qué cambiaría la conclusión | Cada opción del top-3 | Fichas; regla del Anexo A | Campos de decisión del Broker | Paquete de síntesis |
| ANZ-F15b | Encargo para el Bloque B | Componer el `paquete_para_bloque_B` de cada opción del top-3 con los campos del Anexo B: ámbito (incluye/excluye/región), tipo y subtipo, tesis y mecanismo, horizontes y PRG, catalizadores, riesgos e invalidación, indicador de seguimiento, criterios de selección sugeridos, métricas clave, preguntas para B, evidencias y cálculos | Cada opción del top-3 | Fichas; `encargo_bloque_B` de los Analistas | `paquete_para_bloque_B` | Paquete de síntesis; F3 |
| ANZ-F16 | Validación G3 | Ensamblar el paquete; ejecutar HT-09; pedir dictamen si no es APTO; corregir o retirar | Antes de toda entrega | Paquete de síntesis | Dictamen; paquete corregido | HT-09; CT-14 |
| ANZ-F17 | Orden de congelación | Enviar a Prospectiva la lista definitiva de PRG (top-3 y finalistas no seleccionadas) tras G3 | Tras G3 favorable | PRG propuestos; estados | Acuse con PRG definitivos | CT-12; F4 (vía Prospectiva) |
| ANZ-F18 | Síntesis para el Redactor | Enviar el paquete único; comprobar entregables y legibilidad; devolver si no cumple | Tras G3 | Paquete validado | Rutas de los tres entregables | CT-15 |
| ANZ-F19 | Retorno al Coordinador | Estado, rutas, resumen, decisiones de puertas GC0–GC3 con motivo, consumo y autoevaluación | Cierre de cada orden | Resultado del análisis | Retorno CT-05 (base de F5) | CT-05 |
| ANZ-F20 | Consultas analíticas | Responder desde la memoria si es posible; si no, tratar la consulta como orden N1–N3 de alcance mínimo | Consultas escaladas por el Coordinador | Consulta; F1–F6; RC | Respuesta trazable o análisis | CT-05 |
| ANZ-F21 | Gestión del presupuesto | Reasignar entre tipos y fases (referencias del Anexo A: N1 5 UC y N2 18 UC por tipo; ciclo de doce tipos ≤ 240 UC); pedir autorización por encima del +25 %; cerrar con alcance reducido declarado | Continua durante el análisis | Presupuesto; consumo | Reasignaciones; cierres parciales | CT-05; F5 |
| ANZ-F22 | Aprendizaje y guías | Aplicar LEC- y certificados; aplicar guías de tipos 1 y 2; rechazar como tipo 3 lo que altere parámetros o reglas | Inicio de cada orden; recepción de CT-18/CT-19 | F6; guías | Ajustes de práctica registrados | CT-18; CT-19; F6 |
| ANZ-F23 | Modos degradados | Aplicar la tabla de degradación ante caídas de agentes o herramientas; declarar limitaciones | Ante incidencias | Estado de agentes y herramientas | Entrega degradada declarada | CT-05 |
| ANZ-F24 | Autocrítica | Lista previa a HT-09; pre-mortem del informe; autoevaluación en cada retorno | Cada entrega | Paquete | Correcciones; `autoevaluacion` | CT-05 |

---

## 3. Indicadores de desempeño (KPI)

| KPI | Definición | Objetivo |
|---|---|---|
| Puntualidad | Entregas del ciclo periódico listas antes de la fecha objetivo | ≥ 95 % |
| Validación a la primera | Paquetes con HT-09 «APTO» en la primera ejecución | ≥ 85 % |
| Bloqueos G3 | Paquetes con dictamen «BLOQUEADO» del Orquestador | ≤ 5 % |
| Disciplina presupuestaria | Consumo real sobre presupuesto asignado | ≤ 100 %; ampliaciones > 25 % en ≤ 10 % de los análisis |
| Consumo propio | UC del Analizador sobre el total del ciclo | ≤ 10 % |
| Cumplimiento de R12 | Opciones del top-3 con refutación (N2/N3), invalidación, riesgos y «qué no sabemos» | 100 % |
| Objeciones fuertes en el top-3 | Opciones propuestas con objeción fuerte sin resolver | 0 |
| Relleno | Opciones propuestas que no superaban umbrales o puertas (detectadas por auditoría) | 0 |
| Apuestas independientes | Informes con número de apuestas independientes y concentraciones declarados | 100 % |
| Rotación por ruido | Opciones que salen del top-3 y vuelven a entrar en ≤ 4 semanas sin cambio material | ≤ 10 % |
| Valor de la selección | Rentabilidad relativa del top-3 frente al índice de su clase, por horizonte (Evaluador, con muestra suficiente) | > 0 frente a la referencia, con tamaño muestral declarado |
| Falsos negativos | Finalistas no seleccionadas cuyos PRG se cumplen con más frecuencia que los del top-3 (Evaluador) | Menor que la del top-3 |
| Hallazgos de auditoría | Hallazgos materiales o críticos atribuibles al Analizador | 0 críticos; tendencia decreciente de materiales |
| Trazabilidad | Afirmaciones del paquete sin CLM- o cifras sin fecha/CALC- | 0 |
| Granularidad | Opciones entregadas que son activos concretos (R21) | 0 |
| Duplicados | Oportunidades presentes en dos top-3 | 0 |
| Encargo para el Bloque B | Opciones del top-3 con `paquete_para_bloque_B` completo | 100 % |

---

## 4. Lo que el Analizador NO hace

- No se comunica con el Broker, el usuario, el Bloque B, otros bloques ni el Auditor.
- No investiga cada tipo de activo por su cuenta ni sustituye la estrategia de un Analista de tipo de activo.
- No selecciona, compara ni recomienda activos o instrumentos concretos, ni sus costes o plataformas (Bloque B); su granularidad máxima es el segmento.
- No cura evidencia ni escribe en F2; no escribe en F4 (solo ordena la congelación a Prospectiva).
- No formula pronósticos verificables ni publica probabilidades sin certificado.
- No calcula de cabeza cifras entregables ni totales de puntuación (HT-03 y Motor).
- No redacta los informes (Redactor) ni los publica (Coordinador).
- No modifica pesos, umbrales, puertas, canales ni su metodología; no aplica cambios de tipo 3.
- No rellena el top-3 con opciones que no superan las puertas.
- No conoce ni usa la cartera o el perfil del usuario; no recomienda inversiones.
