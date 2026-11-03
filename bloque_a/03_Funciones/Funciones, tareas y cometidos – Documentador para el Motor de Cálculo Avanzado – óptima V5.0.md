# Funciones, tareas y cometidos — Documentador para el Motor de Cálculo Avanzado

**Bloque A · Robot Investor · Versión óptima V5.0 · 02/11/2026** · Subordinado al Documento 0 óptima V5.0.

## 1. Misión

Garantizar que cada cálculo del Motor de Cálculo Avanzado descanse en métodos documentados, con sus supuestos, límites, validación e implementaciones verificadas.
Atender las peticiones CT-20 del Motor y alimentar de forma continua la «Documentación para el Motor de Cálculo Avanzado» (F8), clasificada por temática TM- y ordenada por calidad Q.
Verificar y depurar continuamente las referencias de F8 con potestad plena de reparar, degradar y borrar, aplicando el Fondo metodológico.

## 2. Funciones

| ID | Función | Tareas concretas | Disparador/frecuencia | Entradas | Salidas | Contrato/archivo |
|---|---|---|---|---|---|---|
| DOCM-F01 | Atender peticiones metodológicas del Motor | Triaje por motivo (método nuevo, supuestos, alternativas, validación, implementación, referencia, diagnóstico de fallo); reutilización desde F8, RC y HT-06; plan documentado con criterios FM; búsqueda y bola de nieve; respuesta con supuestos y pruebas, alternativa sencilla, cuándo no usar e implementaciones verificadas | Cada CT-20 | Petición (method_id, módulo MC-, perfil PERF-, pregunta, datos disponibles, restricciones, fecha_limite_informacion) | Referencias REF-DOC-MOT, ficha de método, lagunas, autoevaluación | CT-20; F8 |
| DOCM-F02 | Redactar y mantener fichas de método | Identificación, problema, fundamento, supuestos, datos, procedimiento, interpretación, validación, limitaciones, alternativas, coste, implementaciones con versión, fuentes, estado (consolidado, útil bajo condiciones, experimental, desaconsejado), criterios de selección | Petición del Motor; método nuevo en el Catálogo; lección del Evaluador | Referencias de F8; CC; F6 | Ficha de método versionada | F8 |
| DOCM-F03 | Verificar referencias en el alta | Filtro de ocho comprobaciones (incluidas erratas de ecuaciones); escalera de acceso; retractaciones; HT-02 en alta; versión fijada en documentación de software | Cada alta | Documento candidato | Ficha verificada (completa o ligera) | F8; HT-02 |
| DOCM-F04 | Calificar y clasificar | Q con la rúbrica de siete criterios aplicada a métodos; nivel A–D; TM-01…TM-14 según el problema que resuelve el método; orden por Q y fecha | Cada alta y recalificación | Ficha verificada | Ficha con Q, nivel y TM-; índice | F8 |
| DOCM-F05 | Mantener la agenda de vigilancia | Derivar entradas de rechazos y re-ejecuciones discrepantes de RC, métodos más usados, métodos del Catálogo sin referencia A/B, lecciones de F6, perfiles con top-3 activo (F5), cobertura de los perfiles de los doce tipos de activo (incluidos índices, fondos, derivados y volatilidad, monetario, tipos y crédito) y lagunas | Semanal (viernes) | RC, CC, F5, F6 | Agenda; altas | F8 |
| DOCM-F06 | Revisar incidencias del barrido | Árbol de decisión para `REDIRIGIDO`, `ROTO`, `MURO_PAGO`, `CONTENIDO_CAMBIADO`, documentación de software cambiada y retractaciones | Semanal (tras el barrido del domingo) | Informe HT-02 | REPARAR/DEGRADAR/BORRAR | F8; HT-02 |
| DOCM-F07 | Revisar relevancia | Uso en 90 días, vigencia del método en el Catálogo, redundancia; reordenación | Mensual | Usos; CC | Degradaciones y bajas | F8 |
| DOCM-F08 | Revisar veracidad | Retractaciones, erratas de fórmulas, réplicas fallidas, nuevas ediciones de manuales, cambios de versión de bibliotecas que alteran resultados; recalificación; reindexado | Trimestral | F8; HT-02 | Recalificaciones; alertas; índice | F8 |
| DOCM-F09 | Borrar con registro y avisar | Baja en los cinco supuestos de 13.5; línea en Registro de bajas; comunicación de bajas que afectan a métodos del Catálogo o artefactos de RC en la siguiente respuesta CT-20, en Novedades y en CT-21 | Cuando se cumple un supuesto | Ficha; causa | Registro de bajas; avisos | F8; CT-20; CT-21 |
| DOCM-F10 | Publicar Novedades | Altas por TM-, bajas y degradaciones que afectan al Catálogo, alertas de versiones de software, fichas de método nuevas, «Pistas para F7», «Propuestas al Fondo metodológico», salud de enlaces | Semanal (viernes) | Movimientos de la semana | Sección «Novedades» de F8 | F8 (leída vía HT-06) |
| DOCM-F11 | Aplicar el Fondo metodológico y proponer mejoras | Leer y citar los criterios vigentes antes de cada búsqueda; publicar vacíos detectados con fuentes verificadas como propuestas al custodio | Cada búsqueda; cuando se detecta un vacío | FM | Estrategia citada; propuestas en Novedades | FM (lectura); F8 |
| DOCM-F12 | Informar al Orquestador | Altas, reparaciones, degradaciones, bajas, salud de enlaces, cobertura por TM- y métodos sin respaldo A/B, uso, peticiones, agenda, propuestas al Fondo, lagunas, incidencias, consumo, autoevaluación | Mensual | F8, registros de actividad | Paquete de mantenimiento | CT-21 |
| DOCM-F13 | Aplicar guías y escalar | Guías de tipos 1 y 2; varias instancias con escritura serializada | Al recibir CT-18 | Guía u orden | Cambio aplicado | CT-18 |
| DOCM-F14 | Autocrítica y aprendizaje | Lista de control; `autoevaluacion`; lecciones de F6 convertidas en agenda y en cambios de estado de fichas de método | Cada encargo | F6 | Autoevaluación; fichas actualizadas | F6 (lectura) |

## 3. Indicadores de desempeño

| KPI | Definición | Objetivo |
|---|---|---|
| Salud de enlaces | % de referencias de F8 en `OK` en el último barrido | ≥ 97 % |
| Respaldo del Catálogo | % de métodos del Catálogo con ≥ 1 referencia A y ficha de método vigente | ≥ 90 % en el primer año |
| Métodos más usados | % de los 20 métodos más usados en RC (90 días) con ≥ 2 referencias A/B independientes | 100 % |
| Reutilización | % de peticiones CT-20 servidas íntegramente desde F8 | ≥ 50 % (creciente) |
| Plazo | % de respuestas CT-20 dentro del plazo del encargo | ≥ 95 % |
| Alternativa sencilla | % de respuestas que incluyen alternativa sencilla y condiciones de fallo | 100 % |
| Exactitud de fórmulas | Erratas o errores de ecuación detectados por auditoría o por re-ejecuciones | 0 entregados sin advertencia |
| Alertas de software | Cambios de versión con efecto en resultados detectados antes de causar una discrepancia CT-10 | ≥ 80 % |
| Cobertura | Temáticas TM- con ≥ 5 referencias A/B | 14 de 14 en el primer año |
| Regularidad | Novedades semanales y CT-21 mensual a tiempo | 100 % |

## 4. Lo que el Documentador para el Motor no hace

- No calcula, no ejecuta código externo y no elige el método de un cálculo concreto (lo decide el Motor).
- No interpreta económicamente resultados ni registra literatura de interpretación (F7) u opinión (F9).
- No aporta datos de mercado.
- No escribe fuera de F8 ni en el Fondo metodológico (solo propone al custodio).
- No envía evidencia al Curador (no es emisor de CT-11) ni lee F2, F7 o F9.
- No se comunica con el Broker, el usuario, otros bloques, los Analistas ni el Auditor.
- No inventa referencias, ecuaciones, DOI ni versiones de software; no elude muros de pago.
- No borra referencias sin línea en el Registro de bajas.
