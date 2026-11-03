# Registro maestro de tendencias (esquema V1.1) — Archivo F1

**Proyecto Robot Investor · Bloque A — Analizador de Tendencias de Inversión**

**Archivo operativo · Esquema V1.1 · 01/11/2026 · Propietario único de escritura: Analizador de Tendencias de Inversión · Estado: operativo desde la publicación coordinada de la óptima V2.0 (31/10/2026); esquema ampliado con la óptima V3.0 (01/11/2026)**

Archivo nuevo F1 creado por la óptima V2.0 del Bloque A. Se rige por el «Documento 0 — Protocolo maestro del Bloque A», versión óptima V3.0 (01/11/2026): inventario de archivos (sección 2.3), flujo de investigación, niveles, puertas y máquina de estados (sección 2.7), matriz de archivos (sección 4.3) y glosario. Ante cualquier conflicto entre este archivo y el Documento 0, prevalece el Documento 0. Este archivo se publica sin entradas reales: contiene su estructura completa, sus reglas y una única entrada de ejemplo claramente marcada como plantilla.

---

## 1. Propósito y alcance

### 1.1 Qué es

El «Registro maestro de tendencias» (archivo F1) es la memoria estructurada de tendencias del Bloque A y la fuente de verdad de su estado: una ficha por tendencia detectada, investigada o seguida, con su identificador estable, su estado dentro de una máquina de estados legal, sus puntuaciones E/T/M con fecha y desglose, su prioridad P, sus relaciones con otras tendencias, su historial de cambios de estado (append-only) y sus referencias a ejecuciones y evidencia. Da cumplimiento a los objetivos OBJ-65 (máquina de estados legal, historial append-only y relaciones entre tendencias) y OBJ-78 (conservación de descartadas e insuficiencias, sin sesgo de supervivencia) del Documento 0 óptima V2.0.

### 1.2 Qué no es

- No es un entregable ni un informe: no se envía al Broker Personal ni al usuario; los entregables citan sus `trend_id` y sus afirmaciones con `claim_id`, pero la comunicación con el exterior es siempre a través de los entregables del Analizador.
- No es una cartera, una recomendación de inversión ni un registro de oportunidades: la prioridad P es una prioridad de investigación, desligada de toda probabilidad de éxito, rentabilidad esperada o recomendación de inversión.
- No es un archivo de evidencia: la evidencia y las afirmaciones residen en F2 («Registro de evidencia y afirmaciones»); F1 las referencia, no las reproduce.
- No es un archivo de acceso libre interno: el Auditor y el Analista de hipótesis contrarias no tienen acceso directo; el material les llega por los contratos CT-07 (revisión experta) y CT-14 (petición de refutación), con las evidencias y las pruebas deterministas antes que las conclusiones.
- No es un histórico desechable: las tendencias invalidadas y archivadas permanecen en el archivo; el registro conserva también los descartes y las insuficiencias para evitar el sesgo de supervivencia (OBJ-78).

## 2. Ficha técnica

| Punto | Contenido |
|---|---|
| 1. Nombre, identificador y propósito | «Registro maestro de tendencias» (nombre canónico en el Documento 0, 2.3), código de archivo F1. Propósito: memoria estructurada de tendencias del bloque y fuente de verdad de su estado, con máquina de estados legal, historial append-only y relaciones entre tendencias (OBJ-65). |
| 2. Esquema de datos y versión | Esquema V1.0, publicado con la óptima V2.0 (31/10/2026). Los cambios de esquema se tramitan como propuesta de tipo 3 y exigen publicación coordinada. |
| 3. Propietario único de escritura | Analizador de Tendencias de Inversión. Ningún otro agente escribe en este archivo. |
| 4. Lectores autorizados y finalidad | Orquestador técnico: lectura para sus comprobaciones deterministas (referencias cruzadas F1/F2 válidas, puntuaciones reconstruibles, fechas y estados válidos). El Auditor y el Analista de hipótesis contrarias carecen de acceso directo: reciben el material pertinente por CT-07 y CT-14. El Broker Personal y el usuario solo ven lo que los entregables del Analizador declaren. |
| 5. Claves e identificadores de enlace | `trend_id` (formato TND-AAAA-NNNN) como clave primaria. Enlaces salientes: `evidence_id` y `claim_id` hacia F2; `run_id` y `request_id` hacia las ejecuciones del Analizador; `objection_id` del paquete CT-14; `source_id` (RF-AAAA) y `source_tier` del Registro de Fuentes Fiables en los indicadores de seguimiento; `audit_id`/`package_id` cuando un cambio de estado viaja en el paquete de auditoría CT-03. Enlaces entrantes: F2 registra qué tendencias utilizan cada evidencia; CT-14 referencia el `trend_id`; CT-13 (retroalimentación del Broker Personal) aporta contexto de calibración que puede motivar revisiones de prioridad P. |
| 6. Política de actualización, conservación y corrección | Append-only: las altas y los cambios de estado son entradas nuevas con fecha; las previsiones y los estados registrados se congelan y no se reescriben (regla crítica R16). Toda corrección es una nueva versión de la ficha referenciada a la original, con fecha, motivo y autor. Las tendencias invalidadas, archivadas y los cierres por insuficiencia se conservan indefinidamente (OBJ-78, sin sesgo de supervivencia). Conservación de extractos conforme a la seguridad de contenido externo del Documento 0 (sección 8). |
| 7. Reglas de duplicación y resolución de conflictos | Antes de dar de alta una tendencia, el Analizador comprueba por nombre canónico, denominaciones alternativas y similitud temática si existe ya una ficha (candidata, en investigación, validada, en observación o archivada). Si existe, la detección se anota en la ficha existente (duplicado declarado) y no se abre ficha nueva; la fusión de dos fichas exige marcar una como absorbida y archivarla con «fusión referenciada» al `trend_id` que subsiste. Conflicto de datos entre fichas (relaciones contradictorias, puntuaciones que no cuadran con su desglose): prevalece la ficha revisada más recientemente con su justificación documentada y la discrepancia se corrige en nueva versión referenciada. |
| 8. Criterios de calidad e integridad | Todo campo obligatorio cumplimentado o declarado («desconocido», «no aplicable», «no consultado»); fechas en ISO 8601; ningún estado fuera de la máquina de estados; ninguna transición ilegal; puntuaciones E/T/M/P entre 0 y 100 con desglose reconstruible (puerta G3); todo cambio de estado con fecha, `run_id`, justificación y evidencia; referencias cruzadas a F2 alcanzables (sin `evidence_id` o `claim_id` rotos). El Orquestador verifica estos criterios con pruebas automatizables (catálogo del Documento 0, sección 2.7.7 del prompt del Orquestador óptima V2.0). |
| 9. Contratos que lo utilizan | CT-14 «Petición de refutación y paquete de objeciones»: el paquete referencia el `trend_id` y las objeciones devueltas se registran en la ficha (abiertas y resueltas) y en el `objections_ledger` del paquete de auditoría. CT-03 «Paquete de auditoría del Analizador»: transporta el `gates_record` (estado y evidencia de G1–G4) y los cambios de estado de la tendencia afectada en la ejecución auditada. CT-13 «Retroalimentación del Broker Personal sobre sugerencias»: aporta contexto de calibración (decisiones y resultados observados sobre sugerencias del ciclo) que el Analizador pondera en las revisiones de prioridad P y en la agenda de seguimiento. CT-07/CT-08 (revisión experta): transportan el material de F1 (evidencias y pruebas deterministas antes que conclusiones) al circuito de auditoría. |
| 10. Pruebas de aceptación y procedimiento de reversión | Aceptación del esquema: (i) la estructura del archivo está completa y sin campos vacíos de definición; (ii) la entrada plantilla valida campo a campo contra el esquema de la sección 3; (iii) todas las transiciones declaradas coinciden exactamente con la máquina de estados del Documento 0 (2.7.4); (iv) el Orquestador puede resolver `trend_id`, `evidence_id` y `claim_id` de la plantilla sin referencias rotas (con F2 publicado). Reversión: si el operador retira la óptima V2.0, este archivo se retira con ella; por ser un archivo nuevo sin entradas reales, la reversión se limita a retirar la copia publicada; si se hubieran registrado entradas, se conservan en copia de solo lectura fechada antes de la reversión, sin renumeración de identificadores, para permitir una futura reactivación sin pérdida de memoria. |

## 3. Esquema de datos

Cada ficha de tendencia contiene los campos siguientes. Los valores controlados son cerrados; su ampliación es un cambio de esquema (tipo 3).

| Campo | Tipo | Obligatorio | Valores controlados / formato | Descripción |
|---|---|---|---|---|
| `trend_id` | Identificador | Sí (inmutable) | `TND-AAAA-NNNN` (AAAA año de alta; NNNN correlativo dentro del año, sin reutilización) | Clave primaria de la ficha. |
| `nombre_canonico` | Texto | Sí | Libre, único en el archivo | Denominación canónica de la tendencia. |
| `denominaciones_alternativas` | Lista de texto | No | Libre; vacío declarado si no hay | Sinónimos, siglas y denominaciones de terceros usadas en la detección y la deduplicación. |
| `categoria` | Valor controlado | Sí | tecnológica · macroeconómica · sectorial · regulatoria · social · demográfica · medioambiental · geopolítica (taxonomía inicial, calibrable) | Ámbito temático principal. |
| `subcategoria` | Texto tipificado | Sí | Libre, coherente con la categoría | Especialización dentro de la categoría. |
| `ambitos_geograficos` | Lista de valores controlados | Sí | global · región macro (indicada) · país (indicado) · mercado doméstico (indicado) | Ámbitos donde se observa o proyecta la tendencia. |
| `cadenas_de_valor` | Lista de texto | Sí | Libre | Cadenas de valor y eslabones afectados. |
| `clase_activo` | Valor controlado | Sí | ACC · FIR · FX · CMD · ETF · DER · REI · CHR · PRV · ALT · MIX (Catálogo de perfiles del Motor, V1.0) | Clase de activo principal de la tendencia; MIX cuando el fenómeno es inherentemente multiclase. Campo añadido con la óptima V3.0; las fichas anteriores se cumplimentan en su próxima revisión. |
| `perfiles_aplicados` | Lista de valores controlados | No (obligatoria en MIX) | PERF-xx del Catálogo de perfiles del Motor (V1.0), o TRANSVERSAL | Perfiles del Motor aplicables a la investigación de la tendencia; en activos híbridos, la lista de perfiles combinados. |
| `mercados_moneda` | Texto estructurado | No | Libre (mercado, región operativa y moneda de referencia por instrumento) | Contexto de mercado y moneda para las vinculaciones cuantitativas. |
| `oportunidades_vinculadas` | Lista de identificadores | No | `OPP-AAAA-NNNN` del Registro de oportunidades (F3) | Identificaciones preliminares de exposición derivadas de la tendencia (Documento 0, 1.5 y 2.3). |
| `pronosticos_vinculados` | Lista de identificadores | No | `PRG-AAAA-NNNN` del Registro de pronósticos congelados (F4) | Pronósticos y escenarios congelados declarados para la tendencia (2.7.7). |
| `fecha_primera_deteccion` | Fecha | Sí | ISO 8601 | Fecha de la ejecución en que se detectó por primera vez. |
| `fecha_ultima_revision` | Fecha | Sí | ISO 8601 | Fecha de la última revisión de la ficha (altas, revisiones y correcciones la actualizan como dato, sin reescribir el historial). |
| `state` | Valor controlado | Sí | candidata · en investigación · validada · en observación · acelerándose · desacelerándose · invalidada · archivada | Estado vigente según la máquina de estados (sección 5). |
| `fase_madurez` | Valor controlado | Sí | señal temprana · emergente · en adopción · consolidada · en declive (taxonomía inicial, calibrable) | Estado evolutivo del fenómeno (no confundir con el estado epistemológico que expresan E y las objeciones). |
| `horizonte_temporal` | Valor controlado | Sí | corto (hasta 2 años) · medio (2 a 5 años) · largo (más de 5 años) | Horizonte temporal estimado de la tendencia. |
| `hipotesis_principal` | Texto con referencia | Sí | Afirmación refutable, enlazada a `claim_id` de F2 | Enunciado central que la investigación sostiene o refuta. |
| `explicaciones_alternativas` | Lista de texto con referencias | Sí (mínimo una desde el alta) | Libre; vacío prohibido | Explicaciones rivales consideradas (factor cíclico, efecto base, sesgo de selección u otra); cada una con su estado de tratamiento. |
| `condiciones_invalidez` | Lista de texto | Sí (mínimo una) | Libre, operativa y observable | Condiciones concretas que, cumplidas, obligan a reclamar la invalidación. |
| `indicadores_seguimiento` | Lista estructurada | Sí | Cada indicador con: nombre, `source_id` del Registro de Fuentes Fiables, `source_tier` (A · B · C), frecuencia (diaria · semanal · mensual · trimestral · anual) y umbral de alerta | Indicadores adelantados y confirmatorios con su fuente, frecuencia y umbral. |
| `hitos_agenda` | Lista estructurada | Sí | Cada hito con: descripción, fecha prevista (o condición), indicador asociado y estado (pendiente · alcanzado · incumplido) | Hitos futuros observables y agenda de seguimiento. |
| `relaciones_tendencias` | Lista estructurada | No | tipo: impulsora · dependiente · competidora · sustituta; contraparte: `trend_id` válido | Relación con otras fichas de este archivo. |
| `puntuaciones` | Bloque estructurado | Sí en transición a validada; opcional en candidata y en investigación | E, T y M: enteros 0–100, cada una con fecha ISO y desglose por variables; un solo bloque vigente; los bloques sustituidos se conservan en el historial de la ficha | E (calidad de la evidencia), T (relevancia de la tendencia) y M (madurez y seguimiento), separadas y reconstruibles (puerta G3); regla de debilidad dominante: el desglose declara la variable más débil. |
| `prioridad_P` | Entero con desglose | Sí | 0–100 con desglose declarado: relevancia potencial (T), novedad, incertidumbre reducible y coste de investigación | Prioridad de investigación; jamás se expresa como probabilidad de éxito, rentabilidad esperada ni recomendación de inversión. |
| `historial_estados` | Lista append-only | Sí | Cada entrada con: fecha ISO, `run_id`, estado anterior, estado nuevo, justificación y referencia de evidencia (`evidence_id`/`claim_id`) | Cambios de estado; prohibido reescribir el pasado (R16). |
| `objeciones_ct14` | Bloque estructurado | Sí en validada; opcional antes | Cada objeción con: `objection_id`, tipo (explicación alternativa · evidencia contraria · extrapolación injustificada · factor cíclico, efecto base o sesgo de selección · dato omitido · causalidad no justificada), fuerza (fuerte · moderada · débil), estado (abierta · respondida con evidencia · sin resolver) y `what_would_resolve` | Objeciones del contrato CT-14 abiertas y resueltas; espejo del `objections_ledger` del paquete CT-03. |
| `referencias_ejecuciones` | Lista de identificadores | Sí | `run_id` (y `request_id` cuando proceda) | Ejecuciones del Analizador en que la tendencia se detectó, investigó o revisó. |
| `referencias_evidencia` | Lista de identificadores | Sí | `evidence_id` y `claim_id` de F2 | Soporte probatorio de la hipótesis, de las explicaciones alternativas y de los cambios de estado. |

## 4. Reglas de registro

### 4.1 Altas

1. El Analizador da de alta una ficha cuando registra una nueva detección. El alta exige, como mínimo: `trend_id` asignado por correlativo, nombre canónico, categoría y subcategoría, ámbitos geográficos, fecha de primera detección, hipótesis principal, una explicación alternativa, una condición de invalidación y, al menos, una raíz independiente registrada en F2. La máquina de estados fija el estado inicial: candidata.
2. El cierre de una ejecución con cero tendencias es legítimo y no genera ficha (R15); la insuficiencia de evidencia se documenta en la ejecución y en la agenda de seguimiento, no como ficha vacía.
3. El estado de una ficha recién abierta es «candidata»; el paso a «en investigación» exige dos raíces independientes o la asignación de un nivel N2/N3 (sección 5).

### 4.2 Cambios

1. Todo cambio de estado sigue la máquina de estados de la sección 5 y se registra en `historial_estados` con fecha, `run_id`, justificación y evidencia. El campo `state` refleja siempre el último estado del historial.
2. Las revisiones de puntuaciones (E/T/M) crean un bloque nuevo fechado; el bloque anterior se conserva en el historial de la ficha. El desglose debe permitir reconstruir cada puntuación desde sus variables (control G3).
3. Las objeciones del CT-14 se actualizan al recibirlas (altas) y al responderlas (cambio de estado de la objeción, con la evidencia de la respuesta o la declaración de que permanece sin resolver). El Analizador no puede descartar una objeción porque contradiga su conclusión (R14 del contrato CT-14: cada objeción fuerte o moderada se responde con evidencia o se declara sin resolver; una fuerte sin resolver impide la transición a «validada»).
4. La prioridad P se recalcula en cada revisión con su desglose; el valor anterior se conserva en el historial de la ficha.

### 4.3 Correcciones

1. Toda corrección es una nueva versión de la ficha referenciada a la original, con fecha, motivo y autor; los campos se congelan conforme a R16 y no se reescriben.
2. Si una corrección afecta a un estado registrado o a una previsión congelada, la corrección añade una entrada al historial que referencia la entrada original; la original no se modifica ni se elimina.
3. Los errores de identificador (por ejemplo, un `evidence_id` mal transcrito) se corrigen en nueva versión con referencia cruzada a la ficha anterior; los identificadores no se renumeran.

### 4.4 Estados

Los ocho estados y su significado operativo:

| Estado | Significado operativo |
|---|---|
| candidata | Señal registrada con al menos una raíz independiente; pendiente de decidir si se investiga. |
| en investigación | La tendencia está siendo investigada bajo un nivel N1/N2/N3 asignado y su presupuesto. |
| validada | G1–G3 superadas, sin objeción fuerte ni moderada sin resolver y E ≥ 60; hipótesis sostenida por la evidencia disponible. |
| en observación | Señal estable, sin cambio de fase; seguimiento por agenda. |
| acelerándose | Indicadores de velocidad con evidencia de aceleración. |
| desacelerándose | Indicadores de velocidad con evidencia de desaceleración. |
| invalidada | La hipótesis quedó refutada (objeción fuerte confirmada, evidencia contraria decisiva o condición de invalidación cumplida). La ficha se conserva. |
| archivada | Absorbida por otra ficha (fusión referenciada), sin actividad en dos revisiones trimestrales o fuera de alcance. La ficha se conserva. |

### 4.5 Máquina de estados

El estado de cada tendencia se rige por una máquina de estados legal; toda transición no listada está prohibida. Transiciones legales exactas:

| Transición | Condición exigida |
|---|---|
| nueva detección → candidata | Mínimo una raíz independiente registrada en F2. |
| candidata → en investigación | Mínimo dos raíces independientes o nivel N2/N3 asignado y justificado. |
| en investigación → validada | G1–G3 superadas; sin objeción fuerte ni moderada sin resolver; E ≥ 60. |
| en investigación → invalidada | Objeción fuerte confirmada o evidencia contraria decisiva. |
| en investigación → candidata | Insuficiencia de evidencia sostenida; rebaja documentada. |
| validada → en observación | Señal estable, sin cambio de fase. |
| validada → acelerándose o desacelerándose | Indicadores de velocidad con evidencia. |
| en observación → acelerándose o desacelerándose | Indicadores de velocidad con evidencia. |
| acelerándose → invalidada | Condición de invalidación cumplida. |
| desacelerándose → invalidada | Condición de invalidación cumplida. |
| en observación → invalidada | Condición de invalidación cumplida. |
| cualquier estado → archivada | Absorción por otra ficha (fusión referenciada), sin actividad en dos revisiones trimestrales o fuera de alcance. |
| invalidada → candidata | Solo con evidencia nueva sustantiva; reapertura referenciada. |

Notas de la máquina:

1. El umbral de raíces por transición y el umbral E ≥ 60 son valores iniciales, calibrables por el mecanismo del Anexo A del Documento 0, y se recalibrarán con evidencia histórica cuando se active el Evaluador de previsiones (elemento en transición).
2. El historial de estados es append-only: cada cambio se registra con fecha, `run_id`, justificación y evidencia; está prohibido reescribir el pasado (R16).
3. Conservación sin sesgo de supervivencia (OBJ-78): F1 conserva también las tendencias descartadas, las invalidadas, las archivadas y las insuficiencias de evidencia declaradas; ningún descarte se elimina físicamente, de modo que la evaluación retrospectiva futura (Evaluador en transición) pueda contrastar previsiones y estados con el conjunto completo, no solo con los casos de éxito.
4. El `gates_record` del paquete de auditoría (CT-03) y el `historial_estados` de la ficha deben ser consistentes: un cambio de estado que el paquete no registró o un `gates_record` sin reflejo en la ficha son incidencias de integridad de datos para el Orquestador.

## 5. Índice del registro y plantilla de entrada

### 5.1 Estructura del archivo

El archivo se compone de cuatro secciones, en este orden:

1. Índice operativo del registro: recuento de fichas por estado y por categoría, fichas dadas de alta y archivadas en el último trimestre, relaciones activas entre tendencias, carencias y prioridades de mantenimiento, y fecha de última revisión del índice.
2. Fichas por tendencia (sección principal): una ficha por `trend_id`, en orden de alta; dentro de cada ficha, los bloques de campos del esquema (sección 3), el historial de estados y las objeciones.
3. Registro de correcciones y reversiones: entradas de corrección referenciadas a la ficha y a la entrada original.
4. Registro de versiones del propio archivo (sección 6).

### 5.2 Índice operativo (estado de arranque)

| Campo | Valor |
|---|---|
| Versión del esquema | V1.0 |
| Fichas por estado | candidata: 0 · en investigación: 0 · validada: 0 · en observación: 0 · acelerándose: 0 · desacelerándose: 0 · invalidada: 0 · archivada: 0 |
| Fichas por categoría | Ninguna (archivo recién publicado) |
| Altas y archivados del último trimestre | Ninguno (archivo recién publicado) |
| Relaciones activas entre tendencias | Ninguna |
| Fecha de última revisión del índice | 2026-10-31 (publicación) |
| Carencias y prioridades | Primera carga de fichas con la primera ejecución del Analizador tras la activación de la óptima V2.0 |

### 5.3 Plantilla de entrada de tendencia

La entrada siguiente es un ejemplo ficticio que muestra el formato de ficha: **(plantilla — no es una entrada real)**. Ningún dato de esta plantilla describe una tendencia existente; los identificadores de ejemplo no se reutilizan.

#### TND-2026-0001 — (plantilla — no es una entrada real)

*Identificación.* **trend_id:** TND-2026-0001 · **nombre_canonico:** Ejemplo ficticio de automatización generativa de servicios financieros internos · **denominaciones_alternativas:** «IA generativa en back office», «automatización cognitiva de operaciones» · **categoria:** tecnológica · **subcategoria:** adopción de IA generativa en procesos operativos · **ambitos_geograficos:** región macro (Europa occidental); país (España) · **cadenas_de_valor:** servicios financieros; operaciones y procesamiento documental · **fecha_primera_deteccion:** 2026-11-04 · **fecha_ultima_revision:** 2026-11-04 · **state:** candidata · **fase_madurez:** emergente · **horizonte_temporal:** medio (2 a 5 años)

*Hipótesis y contraste.* **hipotesis_principal:** la reducción de costes unitarios del procesamiento documental impulsará la sustitución de flujos manuales por flujos generativos supervisados en entidades medianas (claim_id: CLM-2026-0001) · **explicaciones_alternativas:** factor cíclico de renovación tecnológica tras el ciclo anterior de inversión en digitalización (estado: en tratamiento) · **condiciones_invalidez:** si los pilotos públicos documentados en 2027 muestran tasas de abandono superiores al 50 por ciento sin causa regulatoria, la hipótesis pierde su base de adopción · **objeciones_ct14:** ninguna registrada (tendencia aún no investigada en N2/N3)

*Seguimiento.* **indicadores_seguimiento:** (1) gasto en pilotos declarado por entidades (fuente: RF-0001, source_tier A, frecuencia trimestral, umbral: crecimiento interanual superior al 20 por ciento); (2) normativa sectorial de supervisión (fuente: RF-0002, source_tier A, frecuencia mensual, umbral: publicación de norma aplicable) · **hitos_agenda:** (1) cierre del primer vencimiento de pilotos referenciados, fecha prevista 2027-06-30, indicador asociado (1), estado: pendiente · **relaciones_tendencias:** dependiente de TND-2026-0002 (plantilla) · **prioridad_P:** 55 (desglose: relevancia potencial 60; novedad 55; incertidumbre reducible 60; coste de investigación 40)

*Puntuaciones y trazabilidad.* **puntuaciones:** no calculadas (estado candidata; se calcularán antes de la transición a validada) · **historial_estados:** 2026-11-04 · run_id RUN-2026-1110 · de nueva detección a candidata · justificación: primera detección con una raíz independiente · evidencia: EVD-2026-0001 · **referencias_ejecuciones:** RUN-2026-1110 · **referencias_evidencia:** EVD-2026-0001; CLM-2026-0001 (todas las referencias de esta plantilla son ficticias y no existen en F2)

## 6. Registro de versiones del archivo

| Versión | Fecha | Descripción |
|---|---|---|
| V1.1 | 01/11/2026 | Ampliación del esquema aplicada con la óptima V3.0 del Documento 0 (reforma de alcance multiactivo): campos nuevos `clase_activo`, `perfiles_aplicados`, `mercados_moneda`, `oportunidades_vinculadas` (F3) y `pronosticos_vinculados` (F4); las entradas existentes conservan su esquema y los campos nuevos se cumplimentan en altas y revisiones posteriores. Sin cambios de máquina de estados, de reglas de registro ni de ficha técnica en lo esencial (referencia al Documento 0 actualizada a la óptima V3.0). |
| V1.0 | 31/10/2026 | Publicación inicial del archivo F1 con la óptima V2.0 del Bloque A: esquema V1.0 completo, ficha técnica de diez puntos, máquina de estados legal del Documento 0 (2.7.4), reglas de registro, índice de arranque y plantilla de entrada. Archivo publicado sin entradas reales. |
