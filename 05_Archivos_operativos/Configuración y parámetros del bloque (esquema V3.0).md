# Esquema de archivo operativo — F10 Configuración y parámetros del bloque

**Bloque A · Robot Investor · Versión óptima V5.0 · 02/11/2026 · actualizado V5.1 (03/11/2026)** · Subordinado al Documento 0 óptima V5.1. Cambios V5.1: P-03 y P-13 con H5; P-27 con horizonte principal H5; P-30 = 5.1; P-31 con columna H5; parámetros nuevos P-34 a P-44 (consultas al Broker, credenciales, seguimientos encargados, H5 y rangos de horizonte principal); limitaciones de servicio por credenciales denegadas (régimen SERVICIO, AG-01).

---

## 1. Propósito

F10 publica los **valores vigentes** de todos los parámetros del Bloque A (Anexo A del Documento 0 y parámetros asociados de las secciones 8.3, 9.1 y 14), con su **régimen** (quién puede cambiarlo y dentro de qué banda), su historial de cambios y la `methodology_version` vigente. Todo agente lee de F10 los umbrales, pesos y presupuestos que aplica; HT-03 y HT-09 los toman de aquí. Un valor que no esté en F10 no es vigente.

## 2. Propietario, lectores y contratos

| Régimen | Quién escribe | Cómo | Ejemplos |
|---|---|---|---|
| SERVICIO | AG-01 Coordinador | A petición del Broker por CT-04, registrada en F5 (RET-); y, desde V5.1, las **limitaciones de servicio por credenciales denegadas** (CT-25, sin valores) | Periodicidad, tipos de activo activos (de entre los doce), horizontes de interés, idioma, frecuencias de seguimiento encargado, plazos de consulta, estado de servicios externos |
| CALIBRABLE | AG-20 Evaluador | Dentro de banda, con evidencia, `aju_id` en F6 y nueva `methodology_version` menor | Pesos, umbrales, presupuestos (si tienen banda) |
| OPERADOR | Operador humano (registro técnico por el Orquestador tras aprobación de tipo 3) | Propuesta de tipo 3 aprobada (`p3_id`) | Corroboración mínima, muestra para certificar, criterio de certificado |

**Lectores**: todos los agentes y herramientas. **Contratos**: CT-04 (cambios de servicio), CT-19 (difusión de ajustes), cola de tipo 3 en HA (cambios del operador).

## 3. Reglas

1. **Escritura por régimen**: un cambio fuera del régimen del parámetro se rechaza y se registra como incidencia (R6, R18).
2. **Bandas** (12.2 del Documento 0): pesos ±5 puntos porcentuales (±0,05) por trimestre y ±15 (±0,15) en total frente al valor inicial; umbrales ±5 puntos por trimestre y ±10 en total. **Calibrables sin banda explícita** en el Documento 0: banda `PENDIENTE_OPERADOR`; mientras el operador no la fije, cualquier cambio es tipo 3 (regla más restrictiva, R23). Se incluye una banda propuesta para su ratificación.
3. **Servicio con límites**: el Broker no puede activar un horizonte «No» de la matriz 8.3 ni cambiar parámetros de otro régimen; el Coordinador rechaza esa parte con motivo (RET- `APLICADA_PARCIALMENTE`).
4. **Versionado**: todo cambio CALIBRABLE incrementa la versión menor (5.1 → 5.2); los cambios del operador que alteren metodología pueden incrementar la mayor (4.x → 5.0), lo que **revoca los certificados vigentes**. Los cambios de SERVICIO no cambian la versión de metodología.
5. **Efecto**: cada cambio declara `fecha_efecto`; los análisis en curso terminan con los valores con que empezaron (registrados en su RUN-).
6. **Append-only**: el historial de cambios conserva todos los valores anteriores; la reversión es un cambio nuevo.
7. Una vez por trimestre como máximo por parámetro CALIBRABLE; máximo tres parámetros en evaluación sombra simultánea.

## 4. Formato de entrada

### 4.1 Registro de parámetro

| Campo | Tipo | Valores / formato |
|---|---|---|
| `param_id` | Identificador | `P-NN` (tabla 4.3) |
| `nombre` | Texto | — |
| `valor_inicial` | Según parámetro | Anexo A |
| `valor_vigente` | Según parámetro | — |
| `unidad` | Texto | — |
| `regimen` | Enumerado | SERVICIO · CALIBRABLE · OPERADOR (· CALIBRABLE_RESTRINGIDO para la matriz 8.3) |
| `banda` | Objeto | `{trimestral, total, estado DEFINIDA·PENDIENTE_OPERADOR, propuesta}` |
| `acumulado_vs_inicial` | Número | Para el control de banda total |
| `escritor_autorizado` | Enumerado | AG-01 · AG-20 · OPERADOR |
| `ultimo_cambio` | Objeto | `{cfg_id, fecha_efecto, origen ret_id·aju_id·p3_id}` |
| `en_sombra` | Booleano | — |

### 4.2 Registro de cambio (CFG-)

`cfg_id` (`CFG-AAAA-NNNN`), `param_id`, `de`, `a`, `regimen`, `autor` (AG-01 · AG-20 · OPERADOR), `origen` (`ret_id` · `aju_id` · `p3_id`), `motivo`, `methodology_version` `{de, a}`, `fecha_registro`, `fecha_efecto`, `revierte_a` (si es reversión).

### 4.3 Volcado inicial del Anexo A

| ID | Parámetro | Valor inicial | Régimen | Banda |
|---|---|---|---|---|
| P-01 | Periodicidad del ciclo C1 | Semanal; ejecución el sábado, entrega el lunes 07:00 (zona horaria del usuario) | SERVICIO | — (opciones: diaria, semanal, quincenal, mensual, personalizada) |
| P-02 | Tipos de activo activos | Los doce: RV, RF, DIV, MP, IDX, FON, DER, INM, CRI, ALT, MON, TCV | SERVICIO | — (subconjunto no vacío de los doce) |
| P-03 | Horizontes de interés del usuario | H1–H5 según aplicabilidad 8.3 | SERVICIO | No puede activar un horizonte «No» |
| P-04 | Opciones máximas por tipo de activo en el informe periódico | 3 | OPERADOR | — |
| P-05 | Candidatas máximas tras cribado | 8 por tipo de activo | CALIBRABLE | PENDIENTE_OPERADOR (propuesta: ±1 por trimestre; ±2 total) |
| P-06 | Finalistas máximas (GC3) | 5 por tipo de activo | CALIBRABLE | PENDIENTE_OPERADOR (propuesta: ±1 por trimestre; ±2 total) |
| P-07 | Rotación exploratoria en cribado | 20 % del presupuesto de cribado | CALIBRABLE | PENDIENTE_OPERADOR (propuesta: ±5 pp por trimestre; ±10 pp total; nunca < 10 %) |
| P-08 | Banda de cambio material GC0 | Precio > 1,5 desviaciones típicas semanales de la clase; evento relevante del calendario; dato macro con sorpresa > 1 desviación típica; invalidación a < 10 % de activarse | CALIBRABLE | PENDIENTE_OPERADOR (propuesta: ±0,25 σ por trimestre; ±0,5 σ total) |
| P-09 | Umbrales de elegibilidad | E ≥ 60; A ≥ 55; T ≥ 50 (o NA con A ≥ 65) | CALIBRABLE | ±5 por trimestre; ±10 total (cada umbral) |
| P-10 | Umbral GC2 | E provisional ≥ 50 | CALIBRABLE | ±5 por trimestre; ±10 total |
| P-11 | Pesos de RK | A 0,45 · E 0,35 · T 0,20 | CALIBRABLE | ±0,05 por trimestre; ±0,15 total (cada peso; suma 1) |
| P-12 | Pesos de A, E, T, M, P | Tabla 4.4 | CALIBRABLE | ±5 puntos por trimestre; ±15 total (cada peso; suma 100) |
| P-13 | Antigüedad máxima de datos de mercado (PS2) | H1: 1 día; H2: 3 días; H3: 7 días; H4: 30 días; H5: 90 días | OPERADOR | — |
| P-14 | Corroboración mínima (PS1) | 2 raíces independientes A/B o 1 fuente primaria A | OPERADOR | — |
| P-15 | Muestra mínima para calibrar o certificar | 30 resueltos por celda clase × horizonte; 100 para certificar | OPERADOR | — |
| P-16 | Criterio de certificado de horizonte (R13) | n ≥ 100; extremo inferior del IC 90 % del BSS frente a la referencia > 0; calibración no rechazada (ECE observado ≤ percentil 90 del ECE simulado bajo calibración perfecta con el mismo n y las mismas probabilidades —remuestreo de consistencia de Bröcker y Smith, 2007— y, en todo caso, ECE < 0,15) | OPERADOR | — |
| P-17 | Presupuesto de referencia (UC) | N0: 1 · N1: 5 por tipo de activo · N2: 18 por tipo de activo · N3: 50 por petición; ciclo semanal completo con los doce tipos ≤ 240 | CALIBRABLE | PENDIENTE_OPERADOR (propuesta: ±10 % por trimestre; ±25 % total) |
| P-18 | Definición de 1 UC | ≈ 8 000 tokens de entrada y 1 500 de salida, o un cálculo PLAN_STD | OPERADOR | — |
| P-19 | Ampliación de presupuesto sin autorización | Hasta +25 % | OPERADOR | — |
| P-20 | Umbral de escalado por instancias (R25) | Cola > 3 encargos o tiempo de respuesta > 2× el objetivo | CALIBRABLE | PENDIENTE_OPERADOR (propuesta: cola ±1; factor de tiempo ±0,5 por trimestre) |
| P-21 | Objetivo de respuesta N0 | < 2 minutos | SERVICIO | — |
| P-22 | Muestreo de auditoría | 100 % periódicos; 30 % ad hoc N1–N2; 100 % N3; 10 % N0 | CALIBRABLE | PENDIENTE_OPERADOR (propuesta: ±10 pp por trimestre en ad hoc y N0; los 100 % no bajan) |
| P-23 | Barrido de enlaces | Semanal (domingo) | CALIBRABLE | PENDIENTE_OPERADOR |
| P-24 | Umbral de cambio de contenido | Similitud de texto < 0,8 frente a la versión archivada | CALIBRABLE | PENDIENTE_OPERADOR (propuesta: ±0,05 por trimestre) |
| P-25 | Criterio de borrado por baja calidad | Q < 50 y sin uso en 180 días | CALIBRABLE | PENDIENTE_OPERADOR (propuesta: Q ±5; días ±30) |
| P-26 | Pregunta repetida (lección de producto) | 3 veces en 4 semanas | CALIBRABLE | PENDIENTE_OPERADOR |
| P-27 | Relevancia decisional ALTA | Cualquiera de: riesgo ≥ 4/5; reversibilidad baja; H4 con iliquidez; horizonte principal H5; E < 70 con A ≥ 75; opción nueva en CRI o ALT | CALIBRABLE | PENDIENTE_OPERADOR (propuesta: umbrales de E y A ±5 por trimestre) |
| P-28 | Retención | F1–F6, RC, HA: indefinida; extractos externos: mínimos; artefactos del Motor: 5 años | OPERADOR | — |
| P-29 | Idioma | es-ES (informe del usuario en el idioma configurado por el Broker) | SERVICIO | — |
| P-30 | Versión de metodología | 5.1 | CALIBRABLE (menores) / OPERADOR (mayores) | — |
| P-31 | Matriz de aplicabilidad de horizontes | Tabla 4.5 | CALIBRABLE_RESTRINGIDO | «Sí» ↔ «Limitado» automático con las condiciones de 12.2; todo cambio desde o hacia «No», tipo 3 |
| P-32 | Referencias de comparación por tipo de activo | Tabla 4.6 (las de 8.4) | OPERADOR | — |
| P-33 | Bandas verbales de probabilidad | Tabla 4.7 (en H5, solo banda: nunca probabilidad interna ni publicada) | OPERADOR | — |
| P-34 | Consultas al Broker (CT-23): plazo de respuesta | `BLOQUEANTE`: 4 h en peticiones ad hoc; en el ciclo periódico, hasta la hora que permite cumplir la entrega (como tarde, domingo 18:00). `NO_BLOQUEANTE`: 24 h o hasta la entrega, lo que llegue antes | SERVICIO | — |
| P-35 | Consultas al Broker: máximo por análisis | 3 mensajes CT-23 por RUN- (cada uno puede agrupar varias preguntas); las bloqueantes, solo si la respuesta puede cambiar el alcance o un top-3 | CALIBRABLE | PENDIENTE_OPERADOR (propuesta: ±1 por trimestre; mínimo 1) |
| P-36 | Consulta recurrente (lección de normalización) | El mismo tipo y motivo de consulta 3 veces en 8 semanas | CALIBRABLE | PENDIENTE_OPERADOR |
| P-37 | Credenciales (CT-25) | Respuesta esperada en 72 h; recordatorio cada 7 días mientras el servicio siga degradado, máximo 3; una credencial `DENEGADA` no se vuelve a pedir salvo cambio de circunstancias | OPERADOR | — |
| P-38 | Frecuencias de seguimiento encargado (CT-24) | Diaria, semanal (por defecto), quincenal, mensual, trimestral o personalizada, a elección del Broker; sin límite de encargos (prioridad inferior a C1–C3) | SERVICIO | — |
| P-39 | Frecuencia orientativa por horizonte principal (aviso, no veto) | H1: diaria · H2: diaria o semanal · H3: semanal a mensual · H4: mensual o trimestral · H5: trimestral | CALIBRABLE | PENDIENTE_OPERADOR |
| P-40 | Presupuesto por ciclo de seguimiento encargado (C6) | 2 UC; hasta 5 UC si el delta es material; ciclo «sin novedad»: ≤ 0,5 UC | CALIBRABLE | PENDIENTE_OPERADOR (propuesta: ±0,5 UC por trimestre) |
| P-41 | Pronósticos H5 | Solo banda verbal (sin probabilidad numérica ni certificado); ≥ 3 hitos HIT- por pronóstico, el primero a ≤ 12 meses y con ≤ 24 meses entre hitos consecutivos | OPERADOR | — |
| P-42 | Degradación automática de H5 (12.2) | Tasa de hitos cumplidos < 50 % con ≥ 20 hitos resueltos en la celda tipo × H5 → la aplicabilidad baja un escalón («Sí» → «Limitado» → «No») | CALIBRABLE | PENDIENTE_OPERADOR; volver a subir exige tipo 3 |
| P-43 | Rangos de horizonte principal por naturaleza de la inversión | Tabla 4.8 (los de 8.3) | OPERADOR | — |
| P-44 | Estado de servicios externos por credencial (V5.1) | Una entrada `SRV-<servicio>` por servicio con credencial denegada: «degradado (credencial denegada)», `crd_id`; sin valores | SERVICIO (AG-01) | — |

### 4.4 Pesos iniciales de las dimensiones (P-12)

| Puntuación | Dimensiones y pesos |
|---|---|
| T | Magnitud 20; alcance 15; velocidad 15; duración 10; difusión 10; posición en la cadena de valor 10; capacidad transformadora 10; claridad causal 10 |
| E | Calidad e independencia de raíces 25; cobertura de variables esenciales 15; calidad metodológica 15; trazabilidad 15; actualidad 10; discrepancias resueltas 10; objeciones del CT-13 respondidas 10 |
| M | Adopción 20; escalado 15; indicadores disponibles 15; persistencia 15; estabilidad de impulsores 15; hitos claros 20 |
| P | T 40; novedad 20; incertidumbre reducible 20; coste-eficiencia 20 |
| A | Asimetría rentabilidad/riesgo esperada del ámbito (escenarios del Motor sobre su indicador de seguimiento) 30; valoración del ámbito 25; catalizadores identificados y fechados 15; momento 15; profundidad e invertibilidad del universo 15 (tope de valoración 40 con narrativa saturada). No puntúa instrumentos concretos ni sus costes |

### 4.5 Matriz inicial de aplicabilidad de horizontes (P-31; Documento 0, 8.3)

| Tipo de activo | H1 | H2 | H3 | H4 (1–5 años) | H5 (5–30 años, V5.1) |
|---|---|---|---|---|---|
| RV | Limitado | Sí | Sí | Sí | Sí |
| RF | Limitado | Sí | Sí | Sí | Limitado |
| DIV | Sí | Sí | Sí | Limitado | Limitado |
| MP | Sí (energía y metales líquidos) | Sí | Sí | Sí (superciclos) | Sí (superciclos y transición energética) |
| IDX | Limitado (eventos de índice) | Sí | Sí | Sí | Sí |
| FON | No | Limitado | Sí | Sí | Limitado |
| DER | Sí | Sí | Sí (hasta 12 meses) | No | No |
| INM | No | Limitado | Sí | Sí | Limitado |
| CRI | Sí | Sí | Sí | Limitado | Limitado |
| ALT | No | No | Limitado | Sí | Sí |
| MON | Limitado (decisiones de bancos centrales) | Sí | Sí | No | No |
| TCV | Sí | Sí | Sí | Limitado | No |

La columna H5 baja automáticamente un escalón con la regla de P-42 y solo vuelve a subir con un cambio de tipo 3; H5 nunca obtiene certificado de probabilidad numérica.

### 4.6 Referencias de comparación por tipo de activo (P-32; Documento 0, 8.4; propuesta inicial a ratificar por el operador)

| Tipo de activo | Referencia de comparación de los pronósticos relativos y del historial de aciertos |
|---|---|
| RV | MSCI ACWI |
| RF | Bloomberg Global Aggregate cubierto a EUR |
| DIV | Cesta equiponderada G10 frente a EUR |
| MP | Bloomberg Commodity Index |
| IDX | MSCI ACWI |
| FON | Índice de la categoría del vehículo |
| DER | Rentabilidad del subyacente sin derivado |
| INM | FTSE EPRA Nareit Developed |
| CRI | Bitcoin |
| ALT | LPX50 (capital privado cotizado) |
| MON | €STR compuesto |
| TCV | Posición neutra (rentabilidad cero frente al índice de liquidez) |

Todas en EUR y en rentabilidad total cuando aplique; si HT-01 no dispone de una serie, el Evaluador usa la sustituta más próxima y lo declara.

### 4.7 Bandas verbales de probabilidad (P-33)

| Banda | Intervalo | Probabilidad interna por defecto |
|---|---|---|
| Muy probable | 80–95 % | 85 % |
| Más probable que no | 60–75 % | 65 % |
| Incierto | 45–55 % | 50 % |
| Poco probable | 25–40 % | 35 % |
| Muy poco probable | 5–20 % | 15 % |

### 4.8 Rangos del horizonte principal por naturaleza de la inversión (P-43; Documento 0, 8.3; V5.1)

| Naturaleza | Horizonte principal admisible | Ejemplos |
|---|---|---|
| `TACTICA` | H1–H2 | Carry táctico, eventos de índice, momentum corto, volatilidad de evento |
| `LIQUIDEZ` | H1–H3 | Monetario |
| `CICLICA` | H2–H4 | Rotación sectorial, ciclo de crédito, pendiente de curva |
| `PRIMA_RIESGO` | H2–H4 | Carry estructural, venta sistemática de volatilidad |
| `VALORACION` | H3–H4 | Reversión de múltiplos, descuentos, equilibrio cambiario |
| `ESTRUCTURAL` | H4–H5 | Temáticas estructurales, superciclos, capital privado, infraestructuras |

Fuera de rango solo con `justificacion_horizonte` (HT-09: advertencia que dictamina el Orquestador); sin ella, bloqueo.

## 5. Estados y transiciones

Cada parámetro: `VIGENTE` → (cambio) `VIGENTE` con nueva versión; para CALIBRABLE: `VIGENTE` → `EN_SOMBRA` (durante un trimestre tras el cambio) → `VIGENTE` (confirmado) o reversión (`CFG-` nuevo con `revierte_a`). Bandas: `PENDIENTE_OPERADOR` → `DEFINIDA` (decisión de tipo 3).

## 6. Índices de consulta

| Índice | Clave | Uso |
|---|---|---|
| Valores vigentes por fecha | `param_id`, `fecha_efecto` | Lo que aplica un RUN- concreto (reproducibilidad) |
| Por régimen | `regimen` | Validación de escrituras |
| En sombra | `en_sombra` = true | Evaluador y HT-03 |
| Por versión de metodología | `methodology_version` | G3-EST-04; certificados |
| Bandas pendientes | `banda.estado` = PENDIENTE_OPERADOR | Cola de tipo 3 |

## 7. Ejemplo ficticio

> **EJEMPLO FICTICIO — no es una entrada real.**

```json
{"cfg_id":"CFG-2027-0003","param_id":"P-11","de":{"A":0.45,"E":0.35,"T":0.20},"a":{"A":0.48,"E":0.34,"T":0.18},"regimen":"CALIBRABLE","autor":"AG-20",
 "origen":{"aju_id":"AJU-2027-0003"},"motivo":"Mejora fuera de muestra del IC de Spearman RK–rentabilidad relativa H3",
 "methodology_version":{"de":"4.0","a":"4.1"},"fecha_registro":"2027-04-01","fecha_efecto":"2027-04-05","revierte_a":null}
```
