# Funciones, tareas y cometidos — Analista de Prospectiva y Horizontes

**Bloque A · Robot Investor · Versión óptima V5.0 · 02/11/2026** · Subordinado al Documento 0 óptima V5.0.

---

## 1. Misión

Proyectar cada oportunidad finalista —un ámbito (mercado, sector, segmento, factor o estrategia), nunca un activo concreto— en los horizontes que tienen sentido para su tipo de activo de entre los doce (tabla 8.3 del Documento 0: H1 días, H2 semanas, H3 meses, H4 años) mediante escenarios, catalizadores, hitos, indicadores adelantados y condiciones de invalidación.
Formular pronósticos verificables PRG- sobre la evolución del ámbito (normalmente su indicador de seguimiento, en absoluto o frente a la referencia de su tipo de 8.4), con criterio de resolución inequívoco, probabilidad interna siempre registrada y probabilidad publicada solo con certificado del Evaluador (R13).
Dar de alta y congelar los pronósticos en el Registro de pronósticos congelados (F4), materia prima del autoaprendizaje del bloque.

---

## 2. Funciones

| ID | Función | Tareas concretas | Disparador/frecuencia | Entradas | Salidas | Contrato/archivo |
|---|---|---|---|---|---|---|
| PROS-F01 | Recepción del encargo | Validar campos; rechazar con motivo si faltan los esenciales o hay datos sensibles | Cada encargo CT-12 | Encargo | Acuse o rechazo | CT-12 |
| PROS-F02 | Memoria y aplicabilidad de horizontes | Leer OPP-, TND-, CLM clave, PRG previos y lecciones; intersectar tabla 8.3, horizontes pedidos y F10; descartar con motivo | Cada finalista | F1–F6; F10 | Horizontes aplicables y descartados | HT-06; F4 (lectura) |
| PROS-F03 | Comprobación de certificados | Verificar en F6 certificado vigente por celda clase × horizonte × método | Cada horizonte aplicable | F6; CT-19 | Decisión de publicación numérica o banda | F6 |
| PROS-F04 | Clase de referencia y tasa base | Definir la clase de referencia; pedir al Motor tasa base, distribución histórica y referencia ingenua; reutilizar desde RC | Cada PRG candidato | Tesis; datos HT-01 | Tasa base; percentiles; referencia ingenua | CT-09; RC |
| PROS-F05 | Impulsores e incertidumbres críticas | Identificar impulsores y seleccionar hasta dos incertidumbres críticas independientes | Cada finalista | Tesis; F1; F2 | Estructura de escenarios | CT-12 (respuesta) |
| PROS-F06 | Escenarios por horizonte | Base, favorable y adverso con condiciones, mecanismo, señales y consecuencias cuantificadas por el Motor; matriz 2×2 en N3 cuando proceda | Cada horizonte aplicable | Incertidumbres; anclas cuantitativas | Escenarios | CT-12; CT-09 |
| PROS-F07 | Anclaje cuantitativo | Expectativas implícitas (futuros, OIS, forwards, opciones), carry, momento, valoración, volatilidad; contraste con lo que descuenta el mercado | Cada horizonte aplicable | HT-01; Motor | Anclas fechadas (CALC-) | CT-09; HT-01 |
| PROS-F08 | Probabilidad interna y banda | Ajustar la tasa base con evidencia en pasos justificados; rejilla de 5 %; límites 15–85 % sin certificado y 5–95 % con él; traducir a banda verbal | Cada PRG | Tasa base; evidencia | `prob_interna`, `banda_verbal`, `prob_publicada` | F4 (al congelar) |
| PROS-F09 | Formulación de PRG | Uno o dos PRG por horizonte y finalista que superen la lista de verificación (variable —por defecto el indicador de seguimiento del ámbito—, nivel, umbral, fecha, criterio, fuente, fallback, referencia ingenua y referencia de comparación del tipo según 8.4) | Cada horizonte aplicable | Escenarios; probabilidades | PRG propuestos (PRG-P-) | CT-12 |
| PROS-F10 | Hitos, indicadores y catalizadores | Hitos fechados; indicadores adelantados con fuente, frecuencia y umbral; calendario de catalizadores verificado | Cada finalista | Calendarios; F9; BFA | Agenda de seguimiento | CT-12; CT-07 |
| PROS-F11 | Condiciones de invalidación | Definir condiciones observables, con umbral y plazo, anteriores a la resolución y fuera del ruido normal | Cada finalista | Escenario adverso; volatilidad | Invalidaciones para F3 | CT-12 |
| PROS-F12 | Apoyo de conocimiento y evidencia | Pedir calendarios y previsiones (BFA), tasas base y métodos (DOC-A); enviar la evidencia nueva al Curador | Bajo demanda (VOI positivo) | Lagunas | Referencias; EVD- | CT-07; CT-08; CT-11 |
| PROS-F13 | Respuesta prospectiva | Completar y enviar la respuesta con limitaciones, consumo y autoevaluación | Cierre de cada encargo | Resultados F02–F12 | Respuesta CT-12 | CT-12 |
| PROS-F14 | Congelación en F4 | Asignar PRG-AAAA-NNNN; comprobar idempotencia y vigencia del nivel de referencia; dar de alta PRG del top-3 y de finalistas no seleccionadas; acusar | Orden de congelación tras G3 | Orden CT-12; PRG propuestos | Registros F4; acuse | F4; CT-12 |
| PROS-F15 | Versionado de PRG | Proponer PRG nuevos con `version_de` cuando cambie materialmente la evidencia de una opción vigente; nunca reescribir | Revisión de vigentes | F4; evidencia nueva | PRG versionados | F4; CT-12 |
| PROS-F16 | Aprendizaje y calibración | Leer curva de fiabilidad y lecciones; corregir sobre o infraconfianza por celda; aportar observaciones | Cada encargo; recepción de CT-19 | F6; CT-19 | Ajustes de práctica; `autoevaluacion` | CT-19; F6 |
| PROS-F17 | Modos degradados | Sin HT-01 no hay PRG; sin Motor, banda máxima «incierto»; sin F6, todo no certificado; sin F4, congelación pendiente declarada | Ante incidencias | Estado de herramientas | Respuesta degradada declarada | CT-12 |

---

## 3. Indicadores de desempeño (KPI)

| KPI | Definición | Objetivo |
|---|---|---|
| Verificabilidad | PRG congelados que superan la lista de verificación | 100 % |
| Anulaciones por ambigüedad | PRG anulados por el Evaluador por criterio ambiguo o fuente mal definida | ≤ 2 % |
| R13 | Probabilidades publicadas sin certificado vigente para la celda exacta | 0 |
| Registro de probabilidad interna | PRG con `prob_interna` registrada | 100 % |
| Habilidad | Brier skill score frente a la referencia ingenua por celda (con muestra suficiente) | > 0 |
| Calibración | Error de calibración esperado (ECE) por celda | < 0,10 |
| Resolución | Componente de resolución de Brier por celda | Creciente trimestre a trimestre |
| Integridad de F4 | Duplicados o reescrituras de PRG | 0 |
| Congelación oportuna | PRG dados de alta tras la orden sin retraso que afecte a la entrega | ≥ 99 % |
| Cobertura de falsos negativos | Finalistas no seleccionadas con PRG congelados | 100 % |
| Calidad de invalidaciones | Invalidaciones activadas por ruido normal (revertidas en < 2 semanas) | ≤ 10 % |
| Consumo | UC por finalista sobre la orientación (2–4 en N2; 5–8 en N3) | ≤ 110 % |

---

## 4. Lo que el Analista de Prospectiva NO hace

- No selecciona, puntúa ni descarta oportunidades (Analizador con HT-03).
- No investiga la tesis de fondo (Analista de clase) ni la refuta (Contrarias).
- No resuelve pronósticos, no escribe campos de resolución y no certifica calibración (Evaluador).
- No reescribe PRG congelados ni congela sin la orden posterior a G3.
- No publica probabilidades sin certificado ni ofrece horizontes «No» de la tabla 8.3 (p. ej., H1 en FON, INM y ALT; H4 en DER y MON).
- No formula pronósticos sobre activos concretos (valores, emisiones, fondos, contratos o tokens): su objeto es el ámbito (R21).
- No calcula de cabeza cifras entregables (Motor y HT-01).
- No se comunica con el Broker, el usuario, los Analistas de clase, Contrarias, el Redactor ni otros bloques.
