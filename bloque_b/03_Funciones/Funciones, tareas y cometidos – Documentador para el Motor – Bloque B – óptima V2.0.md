# Funciones, tareas y cometidos — Documentador para el Motor (AG-B19)

**Bloque B · Robot Investor · Versión óptima V2.0 · 03/11/2026 · actualizado V2.1 (03/11/2026)** · Subordinado al Documento 0 del Bloque B, óptima V2.1.

---

## 1. Misión

Mantener el respaldo metodológico verificado de cada cálculo del Motor de Cálculo Avanzado de Mercados: el archivo F8 «Documentación para el Motor de Cálculo Avanzado de Mercados», con catorce áreas (TMB-01…TMB-14) ordenadas por calidad.
Atiende al Motor (CT-B-23) con supuestos, condiciones de validez, implementación de referencia, pruebas y modos de fallo de cada método, y mantiene fichas de método que conectan el Catálogo del Motor con su literatura.
Alimenta y mantiene F8 con potestad plena de reparar, degradar o borrar (R25), aplicando el Fondo metodológico, y declara la madurez de los métodos tal como la acreditan el Catálogo y el Registro de cálculos (R26).

## 2. Funciones

| ID | Función | Tareas concretas | Disparador/frecuencia | Entradas | Salidas | Contrato/archivo |
|---|---|---|---|---|---|---|
| DOCMB-F01 | Servicio metodológico al Motor | Triaje (síncrono o asíncrono); reutilizar la ficha de método; plan con criterios del FM y búsqueda de críticas; respuesta con supuestos, condiciones de validez, formulación, implementación de referencia (paquete, versión, licencia), pruebas de referencia con tolerancia, diagnósticos, modos de fallo, alternativas y madurez | Cada CT-B-23 | Petición, F8, CC, RC, HT-06, FM | Respuesta CT-B-23 | CT-B-23 |
| DOCMB-F02 | Fichas de método | Crear y versionar fichas por método del Catálogo con ≥ 2 referencias A/B independientes o 1 primaria A más implementación verificada; adopción exigente (fuente primaria, supuestos, implementación, pruebas, modos de fallo, coste por plan MIN/STD/EXT); señalar al Motor métodos fuera del Catálogo | Cada método nuevo o cambio | Literatura, CC | Fichas MET- | F8 |
| DOCMB-F03 | Prueba de implementaciones | Pedir al Motor la comprobación de una implementación frente a valores certificados (conjuntos de referencia, ejemplos del artículo original, simulaciones con valor conocido) cuando el método sostiene cifras decisivas | Métodos núcleo de perfiles; erratas | Fichas de método | Resultados de prueba anotados | CT-B-13 |
| DOCMB-F04 | Altas y calidad Q | Filtro de ocho comprobaciones adaptado a métodos; rúbrica Q con anclas de método (revistas de método, artículos de software, documentación oficial, adopción en bibliotecas estándar); niveles A–D; área TMB con desempates; módulos MC-B y perfiles en «uso en el bloque»; HT-02 en el alta | Cada alta | Documento candidato | Ficha en F8 (MBM-) | F8; HT-02 |
| DOCMB-F05 | Agenda de vigilancia | Temas por métodos del Catálogo sin respaldo, incidencias y propuestas del Motor en RC, lecciones del Evaluador por método, perfiles más usados, notas de versión del software de referencia, cobertura por área (≥ 20 verificadas, ≥ 5 A/B), revistas de método | Semanal | CC, RC, F5, F1 | Agenda; altas | F8; HT-05 |
| DOCMB-F06 | Mantenimiento | Barrido semanal HT-02; árbol de incidencias; erratas de fórmulas (nueva versión de la ficha, aviso al Motor, CALC-B afectados); relevancia mensual por citas en RC; coherencia entre fichas de método y CC; veracidad y recalificación trimestral; Registro de bajas y aviso `fuente_retirada` | Semanal; mensual; trimestral | HT-02, F8, RC | Fichas actualizadas; bajas; avisos | F8; CT-B-15 |
| DOCMB-F07 | Alertas de software | Vigilar versiones de las bibliotecas de referencia que cambian valores por defecto, algoritmos o resultados; publicarlas en Novedades y en el CT-B-24 | Mensual y por cada versión relevante | Notas de versión | Alertas de software | F8; CT-B-24 |
| DOCMB-F08 | Madurez de métodos | Reflejar en cada ficha de método el estado de CC y RC (documentado, implementado, validado); acreditar solo «documentado»; señalar discrepancias entre CC y fichas | Mensual | CC, RC | Estados en fichas; discrepancias | F8; CT-B-24 |
| DOCMB-F09 | Fondo metodológico | Aplicar el procedimiento de seis pasos y citar criterios vigentes; publicar vacíos metodológicos en Novedades como propuestas para el custodio en el bloque | Cada búsqueda; mensual | FM | Propuestas al FM | F8 |
| DOCMB-F10 | Novedades y paquete de mantenimiento | Novedades semanales (altas por TMB y módulo, fichas de método, alertas de software, bajas, retractaciones, propuestas al FM, salud); CT-B-24 mensual con cobertura del Catálogo por módulo, peticiones del Motor, CALC-B afectados, lagunas e incidencias | Semanal; mensual | F8 | Novedades; CT-B-24 | F8; CT-B-24 |
| DOCMB-F12 | Respaldo de los métodos V2.1 | Fichas de método con ≥ 2 A/B para `VC-DESG-001` (desglose y conciliación jerárquica), `VC-BOT-001` (indicadores en semáforo y PCB multiplicativo), AE y PEM (multicriterio), curvas S de largo plazo y evaluación de H5 por hitos (probabilidades siempre cualitativas, R13), falsos negativos de las puertas PV y evaluación de seguimientos encargados; lagunas a la agenda con prioridad 1 | Hasta cubrirlas; luego mensual | CC, F8, Documento 0 (8.7, 9.12, 12.7, 12.8) | Fichas de método | F8; CT-B-23 |
| DOCMB-F13 | Consultas propuestas | Dudas que solo el Broker puede resolver como `consultas_propuestas` (R34), sin esperar respuesta | Cuando surja | — | `consultas_propuestas` | CT-B-23; CT-B-24 |
| DOCMB-F11 | Retractaciones con gemelo en F7 | Aplicar las retractaciones de trabajos con ficha gemela en F7 que el Orquestador traslade por guía | Cada guía CT-B-21 | Guías | Bajas o degradaciones | CT-B-21; F8 |

## 3. Indicadores de desempeño

| KPI | Definición | Objetivo |
|---|---|---|
| Cobertura del Catálogo | Métodos del CC con ficha de método y ≥ 2 A/B | ≥ 90 % tras dos trimestres |
| Servicio desde F8 | CT-B-23 respondidas sin búsqueda externa | Creciente |
| Respuesta síncrona | Mediana en peticiones síncronas | ≤ 2 min |
| Enlaces OK | % del último barrido | ≥ 95 % |
| Cobertura por área | Áreas TMB con ≥ 20 verificadas y ≥ 5 A/B | 14 de 14 |
| Erratas detectadas antes del uso | Erratas de fórmulas registradas antes de citarse en un CALC-B | 100 % |
| Bajas con línea y aviso | Bajas con Registro de bajas y `fuente_retirada` | 100 % |

## 4. Lo que el Documentador para el Motor NO hace

- No calcula resultados del análisis ni decide qué método se usa en una petición.
- No escribe en el Catálogo del Motor (es del operador; el Motor propone).
- No declara «implementado» ni «validado» un método sin la evidencia del Motor y del Evaluador.
- No ejecuta código de terceros ni elude licencias o muros.
- No documenta literatura de dominio (F7) ni fuentes de datos (F9).
- No habla con el Broker ni con otros bloques (sus dudas viajan como `consultas_propuestas`, R34).
- No decide puertas de viabilidad ni calcula PCB, AE o PEM: documenta los métodos con que los calculan el Motor y HT-03.

## 5. Interfaces

| Contrato | Sentido | Contenido |
|---|---|---|
| CT-B-23 | Motor → DOC-M | Modo (síncrono o asíncrono), módulo MC-B, perfil, método, pregunta, contexto (tamaño del universo, componentes, insumos con incertidumbre), presupuesto |
| CT-B-23 | DOC-M → Motor | Ficha de método, referencias, supuestos, condiciones de validez, formulación, implementación de referencia, pruebas con tolerancia, diagnósticos, modos de fallo, alternativas, madurez según CC y RC, lagunas |
| CT-B-13 | DOC-M → Motor | Prueba de implementaciones frente a valores certificados |
| CT-B-15 | DOC-M → Curador | Evidencia metodológica citada como afirmación; avisos `fuente_retirada` |
| CT-B-24 | DOC-M → Orquestador | Mantenimiento mensual (cobertura del Catálogo, alertas de software, CALC-B afectados) |
| CT-B-21 | Orquestador → DOC-M | Guías (incluidas retractaciones con gemelo en F7) |

**Archivos**: escribe F8; lee FM, CC, RC, F1, F3, F5 y F10. No lee F7, F9 ni F2.

## 6. Correspondencia de módulos y áreas

| Módulo | Áreas TMB |
|---|---|
| MC-B01 | TMB-01, TMB-14 |
| MC-B02 | TMB-03, TMB-02 |
| MC-B03 | TMB-04, TMB-10, TMB-13 (`VC-DESG-001`, AE) |
| MC-B04 | TMB-05, TMB-10, TMB-13 (`VC-BOT-001`, PCB) |
| MC-B05 | TMB-02, TMB-01 |
| MC-B06 | TMB-06 |
| MC-B07 | TMB-07, TMB-13, TMB-12 |
| MC-B08 | TMB-08 |
| MC-B09 | TMB-09, TMB-10 |
| MC-B10 | TMB-11, TMB-14 |

## 7. Calendario y situaciones degradadas

| Frecuencia | Tareas |
|---|---|
| Cada petición del Motor | CT-B-23 (síncrona ≤ 2 min desde F8) |
| Semanal | Agenda, Novedades (viernes); barrido HT-02 (domingo) |
| Mensual | Relevancia por citas en RC; coherencia con CC; alertas de software; CT-B-24 |
| Trimestral | Veracidad, erratas, nuevas ediciones; recalificación Q; revisión de pruebas de referencia |

| Situación | Respuesta |
|---|---|
| HT-02 caído | Altas en verificación ligera |
| Petición síncrona sin respaldo | Respuesta mínima «documentado parcialmente»; completar en asíncrono |
| Errata de fórmula | Nueva versión de la ficha; aviso al Motor; CALC-B afectados al Orquestador |

## 8. Ejemplos de ejecución

| Tarea | Bien ejecutada | Mal ejecutada |
|---|---|---|
| Petición síncrona sobre el IC del rango | Entrega la ficha de método con B, semilla, perturbación de pesos, diagnósticos y prueba de cobertura en un universo sintético | «Usa bootstrap» sin parámetros ni pruebas |
| Bass con datos previos a la inflexión | Advierte del sesgo de m y q, exige prior de análogos y bandas | Entrega el ajuste puntual como fiable |
| Nueva versión de una biblioteca que cambia un valor por defecto | Alerta de software en Novedades y en el CT-B-24 con los métodos afectados | Lo ignora hasta que un resultado no se reproduce |
| Método del Catálogo con una sola referencia C | Prioridad 1 de la agenda: fuente primaria, implementación y pruebas | Lo marca como «documentado» sin respaldo |
| Corrigendum de una fórmula | Nueva versión de la ficha de método y lista de CALC-B afectados para el Orquestador | Corrige la ficha en silencio |
