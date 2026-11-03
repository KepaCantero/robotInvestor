# Esquema de archivo operativo — F10 Configuración y parámetros del bloque

**Bloque A Forex · Robot Investor · Versión V1.0 · 02/11/2026 · actualizado V1.1 (03/11/2026)** · Subordinado al Documento 0 del Bloque A Forex, versión óptima V1.1. Actualización V1.1: H5 en la matriz de horizontes, regla de adecuación del horizonte principal, parámetros de las consultas al Broker (CT-23), de las credenciales (CT-25) y de los seguimientos encargados (CT-24), y limitaciones de servicio por credenciales denegadas.

---

## 1. Propósito

F10 publica los **valores vigentes** de todos los parámetros del Bloque A Forex (Anexo A del Documento 0 y parámetros asociados de las secciones 2.6, 8.3, 8.4, 9.1 y 14), con su **régimen** (quién puede cambiarlo y dentro de qué banda), su historial de cambios y la `methodology_version` vigente (inicial: **FX-1.0**). Todo agente lee de F10 los segmentos activos, la divisa base del usuario, los umbrales, pesos y presupuestos que aplica; HT-03 y HT-09 los toman de aquí. Un valor que no esté en F10 no es vigente.

## 2. Propietario, lectores y contratos

| Régimen | Quién escribe | Cómo | Ejemplos |
|---|---|---|---|
| SERVICIO | AG-01 Coordinador | A petición del Broker por CT-04, registrada en F5 (RET-) | Periodicidad, segmentos activos (de entre los seis), divisa base del usuario, horizontes de interés (H1–H5), idioma, plazos de las consultas CT-23 |
| LIMITACION_SERVICIO (V1.1) | AG-01 Coordinador | Al recibir `DENEGADA` en un CT-25 (registro CRD-FX- en F5) | `LIM-<servicio>`: servicio degradado por credencial denegada, sin valores; se retira si la credencial se provee más tarde |
| CALIBRABLE | AG-20 Evaluador | Dentro de banda, con evidencia, `aju_id` en F6 y nueva `methodology_version` menor | Pesos de A FX y de RK, umbrales, presupuestos (si tienen banda) |
| OPERADOR | Operador humano (registro técnico por el Orquestador tras aprobación de tipo 3) | Propuesta de tipo 3 aprobada (`p3_id`) | Corroboración mínima, muestra para certificar, criterio de certificado, referencias ingenuas obligatorias |

**Lectores**: todos los agentes y herramientas. **Contratos**: CT-04 (cambios de servicio), CT-19 (difusión de ajustes), cola de tipo 3 en HA (cambios del operador).

## 3. Reglas

1. **Escritura por régimen**: un cambio fuera del régimen del parámetro se rechaza y se registra como incidencia (R6, R18).
2. **Bandas** (12.2 del Documento 0): pesos ±5 puntos porcentuales (±0,05) por trimestre y ±15 (±0,15) en total frente al valor inicial; umbrales ±5 puntos por trimestre y ±10 en total. **Calibrables sin banda explícita** en el Documento 0: banda `PENDIENTE_OPERADOR`; mientras el operador no la fije, cualquier cambio es tipo 3 (regla más restrictiva, R23). Se incluye una banda propuesta para su ratificación.
3. **Servicio con límites**: el Broker no puede activar un horizonte «No» de la matriz 8.3, dejar vacía la lista de segmentos activos ni cambiar parámetros de otro régimen; el Coordinador rechaza esa parte con motivo (RET- `APLICADA_PARCIALMENTE`).
4. **Versionado**: todo cambio CALIBRABLE incrementa la versión menor (FX-1.0 → FX-1.1); los cambios del operador que alteren metodología pueden incrementar la mayor (FX-1.x → FX-2.0), lo que **revoca los certificados vigentes**. Los cambios de SERVICIO (incluida la divisa base del usuario) no cambian la versión de metodología. El prefijo «FX-» distingue estas versiones de las del Bloque A general.
5. **Efecto**: cada cambio declara `fecha_efecto`; los análisis en curso terminan con los valores con que empezaron (registrados en su RUN-FX-). Un cambio de divisa base no reescribe los pronósticos ya congelados, que conservan su divisa de medición.
6. **Append-only**: el historial de cambios conserva todos los valores anteriores; la reversión es un cambio nuevo.
7. Una vez por trimestre como máximo por parámetro CALIBRABLE; máximo tres parámetros en evaluación sombra simultánea.
8. **Credenciales (V1.1, R8)**: F10 nunca contiene valores de credenciales; solo la limitación de servicio (`LIM-`) cuando una credencial se deniega, con el `crd_id` de F5. Los valores viven exclusivamente en la bóveda de HT-01.

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

Los identificadores P-01 a P-33 conservan la numeración del Bloque A general (con contenido cambiario); P-34 a P-40 son parámetros del Anexo A Forex sin equivalente directo.

| ID | Parámetro | Valor inicial | Régimen | Banda |
|---|---|---|---|---|
| P-01 | Periodicidad del ciclo C1 | Semanal; ejecución el sábado, tras el cierre de Nueva York del viernes; entrega el lunes a las 07:00 (zona horaria del usuario) | SERVICIO | — (opciones: diaria, semanal, quincenal, mensual, personalizada; la ejecución se sitúa siempre tras un cierre de Nueva York) |
| P-02 | Segmentos activos | Los seis: G10N, G10M, EMAS, EMLA, EMEA y ESTR | SERVICIO | — (subconjunto no vacío de los seis) |
| P-03 | Horizontes de interés del usuario | H1–H5 según la aplicabilidad de 8.3 (H5 «limitado») | SERVICIO | No puede activar un horizonte «No» |
| P-04 | Opciones máximas por segmento en el informe periódico | 3 | OPERADOR | — |
| P-05 | Candidatas máximas tras el cribado | 8 por segmento | CALIBRABLE | PENDIENTE_OPERADOR (propuesta: ±1 por trimestre; ±2 total) |
| P-06 | Finalistas máximas (GC3) | 5 por segmento | CALIBRABLE | PENDIENTE_OPERADOR (propuesta: ±1 por trimestre; ±2 total) |
| P-07 | Rotación exploratoria en el cribado | 20 % del presupuesto de cribado | CALIBRABLE | PENDIENTE_OPERADOR (propuesta: ±5 pp por trimestre; ±10 pp total; nunca < 10 %) |
| P-08 | Banda de cambio material GC0 | Cualquiera de: (1) un par del segmento se mueve más de 1,5 desviaciones típicas semanales; (2) reunión de banco central con cambio de tipos o de orientación; (3) dato con sorpresa superior a 1 desviación típica; (4) intervención confirmada o sospechada; (5) condición de invalidación a menos del 10 % de activarse | CALIBRABLE | PENDIENTE_OPERADOR (propuesta: ±0,25 σ por trimestre y ±0,5 σ total en (1) y (3); ±2 pp en (5); (2) y (4) no calibrables) |
| P-09 | Umbrales de elegibilidad | E ≥ 60; A ≥ 55; T ≥ 50 (o T NA con A ≥ 65) | CALIBRABLE | ±5 por trimestre; ±10 total (cada umbral) |
| P-10 | Umbral GC2 | E provisional ≥ 50 | CALIBRABLE | ±5 por trimestre; ±10 total |
| P-11 | Pesos de RK | A 0,45 · E 0,35 · T 0,20 | CALIBRABLE | ±0,05 por trimestre; ±0,15 total (cada peso; suma 1) |
| P-12 | Pesos de A (FX), E, T, M y P | Tabla 4.4 | CALIBRABLE | ±5 puntos por trimestre; ±15 total (cada peso; suma 100) |
| P-13 | Antigüedad máxima de los datos de mercado (PS2) | H1: 1 día · H2: 2 días · H3: 5 días · H4: 30 días · H5: 90 días | OPERADOR | — |
| P-14 | Corroboración mínima (PS1) | 2 raíces independientes de nivel A o B, o 1 fuente primaria de nivel A | OPERADOR | — |
| P-15 | Muestra mínima para calibrar o certificar | 30 pronósticos resueltos por celda segmento × horizonte para recalibrar; 100 para certificar | OPERADOR | — |
| P-16 | Criterio de certificado de horizonte (R13) | n ≥ 100 con corrección de Holm; extremo inferior del IC 90 % del BSS frente al **paseo aleatorio** > 0; ECE ≤ percentil 90 del ECE simulado bajo calibración perfecta con el mismo n y las mismas probabilidades (Bröcker y Smith, 2007) y, en todo caso, ECE < 0,15 | OPERADOR | — |
| P-17 | Presupuesto de referencia (UC) | N0: 1 · N1: 5 por segmento · N2: 18 por segmento · N3: 50 por petición · informes transversales AG-09 y AG-21: 6 UC cada uno por ciclo · ciclo semanal completo ≤ 140 | CALIBRABLE | PENDIENTE_OPERADOR (propuesta: ±10 % por trimestre; ±25 % total) |
| P-18 | Definición de 1 UC | ≈ una llamada de agente de tamaño medio (≈ 8 000 tokens de entrada y 1 500 de salida) o un cálculo PLAN_STD | OPERADOR | — |
| P-19 | Ampliación de presupuesto sin autorización | Hasta +25 % | OPERADOR | — |
| P-20 | Umbral de escalado por instancias (R25) | Cola de más de 3 encargos o tiempo de respuesta superior al doble del objetivo | CALIBRABLE | PENDIENTE_OPERADOR (propuesta: cola ±1; factor de tiempo ±0,5 por trimestre) |
| P-21 | Objetivo de respuesta N0 | < 2 minutos | SERVICIO | — |
| P-22 | Muestreo de auditoría | 100 % de los informes periódicos · 30 % de las peticiones ad hoc N1–N2 · 100 % de las N3 · 10 % de las consultas N0 | CALIBRABLE | PENDIENTE_OPERADOR (propuesta: ±10 pp por trimestre en ad hoc y N0; los 100 % no bajan) |
| P-23 | Barrido de enlaces | Semanal (domingo) | CALIBRABLE | PENDIENTE_OPERADOR |
| P-24 | Umbral de cambio de contenido | Similitud de texto < 0,8 frente a la versión archivada | CALIBRABLE | PENDIENTE_OPERADOR (propuesta: ±0,05 por trimestre) |
| P-25 | Criterio de borrado por baja calidad | Q < 50 y sin uso en 180 días | CALIBRABLE | PENDIENTE_OPERADOR (propuesta: Q ±5; días ±30) |
| P-26 | Pregunta repetida (lección de producto) | 3 veces en 4 semanas | CALIBRABLE | PENDIENTE_OPERADOR |
| P-27 | Relevancia decisional ALTA | Cualquiera de: riesgo ≥ 4; reversibilidad baja (divisa con NDF o controles); horizonte H4 con riesgo ≥ 3 o liquidez baja; horizonte principal H5; E < 70 con A ≥ 75; opción de tipo `REGIMEN`; divisa emergente de liquidez baja | CALIBRABLE | PENDIENTE_OPERADOR (propuesta: umbrales de E y A ±5 por trimestre; las condiciones de régimen y controles no bajan) |
| P-28 | Retención | F1–F6, RC y HA: indefinida · extractos externos: mínimos · artefactos del Motor: 5 años | OPERADOR | — |
| P-29 | Idioma | es-ES (informe del usuario en el idioma configurado por el Broker) | SERVICIO | — |
| P-30 | Versión de metodología | FX-1.1 (V1.1, 03/11/2026) | CALIBRABLE (menores) / OPERADOR (mayores) | — |
| P-31 | Matriz de aplicabilidad de horizontes | Tabla 4.5 | CALIBRABLE_RESTRINGIDO | «Sí» ↔ «Limitado» automático con las condiciones de 12.2; todo cambio desde o hacia «No», tipo 3 |
| P-32 | Referencias de comparación por segmento | Tabla 4.6 (las de 8.4) | OPERADOR | — (propuesta del bloque a ratificar por el operador) |
| P-33 | Bandas verbales y probabilidad interna | Tabla 4.7 | CALIBRABLE | PENDIENTE_OPERADOR (propuesta: solo la probabilidad interna por defecto, ±5 pp por trimestre, dentro de su intervalo) |
| P-34 | Divisa base del usuario | EUR (para el cálculo de rentabilidades y del riesgo en el informe del usuario y para la referencia de G10N y G10M) | SERVICIO | — (código ISO 4217 de divisa convertible) |
| P-35 | Umbral de señal GC1 | Señal compuesta normalizada ≥ 0,75 y concordancia de al menos dos familias de lentes cambiarias de naturaleza distinta (p. ej., política monetaria y valor); cada segmento añade sus vetos en su prompt | CALIBRABLE | PENDIENTE_OPERADOR (propuesta: ±0,05 por trimestre; ±0,10 total; el requisito de dos familias no baja) |
| P-36 | Referencia ingenua obligatoria | Paseo aleatorio (sin cambio) en dirección y nivel; forward como predictor en rentabilidad total; en estrategias, rentabilidad nula o índice de la estrategia | OPERADOR | — |
| P-37 | Escala de riesgo 1–5 | Ficha RISK-DD-001 del Catálogo (volatilidad anualizada de la exposición con ajustes por colas, liquidez, riesgo de régimen y caída máxima); tipo fijo con riesgo de ruptura o divisa con controles: mínimo 4 | CALIBRABLE | PENDIENTE_OPERADOR (propuesta: cortes de volatilidad ±1 pp por trimestre; el suelo de 4 no baja) |
| P-38 | Relevancia decisional MEDIA / BAJA | MEDIA: opción nueva que no cumple ALTA, o vigente con cambio material · BAJA: vigente sin cambio material | CALIBRABLE | PENDIENTE_OPERADOR |
| P-39 | Valores de liquidez | alta · media · baja | OPERADOR | — |
| P-40 | Presupuesto de mantenimiento (C4) | DOC-A 2 UC/semana · BFA 3 UC/semana · DOC-M 2 UC/semana | CALIBRABLE | PENDIENTE_OPERADOR (propuesta: ±1 UC por trimestre por agente) |
| P-41 | Consultas al Broker (CT-23): plazo de respuesta (V1.1) | BLOQUEANTE: 4 h en peticiones ad hoc; en el ciclo periódico, hasta la hora que permite cumplir la entrega (como tarde, domingo 18:00). NO_BLOQUEANTE: 24 h o hasta la entrega, lo que llegue antes | SERVICIO | — |
| P-42 | Consultas al Broker: máximo por análisis (V1.1) | 3 mensajes CT-23 por RUN-FX- (cada uno puede agrupar varias preguntas); BLOQUEANTE solo si la respuesta puede cambiar el alcance o un top-3 | CALIBRABLE | PENDIENTE_OPERADOR |
| P-43 | Consulta recurrente (lección de normalización) (V1.1) | Mismo tipo y motivo 3 veces en 8 semanas | CALIBRABLE | PENDIENTE_OPERADOR |
| P-44 | Credenciales (CT-25) (V1.1) | Respuesta esperada en 72 h; recordatorio cada 7 días mientras el servicio siga degradado, máximo 3; una DENEGADA no se vuelve a pedir salvo cambio de circunstancias | OPERADOR | — |
| P-45 | Frecuencias de seguimiento encargado (CT-24) (V1.1) | Diaria, semanal (por defecto), quincenal, mensual, trimestral o personalizada; sin límite de encargos (prioridad inferior a C1–C3). Se guarda por encargo en F11 | SERVICIO | — |
| P-46 | Frecuencia orientativa por horizonte principal (aviso, no veto) (V1.1) | H1 diaria · H2 diaria o semanal · H3 semanal a mensual · H4 mensual o trimestral · H5 trimestral | CALIBRABLE | PENDIENTE_OPERADOR |
| P-47 | Presupuesto por ciclo de seguimiento encargado (C6) (V1.1) | 2 UC; hasta 5 UC si el delta es material; «sin novedad» ≤ 0,5 UC | CALIBRABLE | PENDIENTE_OPERADOR |
| P-48 | Pronósticos H5 (V1.1) | Limitados a los tres ámbitos de 8.3 (equilibrio a muy largo plazo, regímenes cambiarios, sistema monetario internacional); solo banda verbal (sin probabilidad numérica ni certificado); ≥ 3 hitos HIT-FX-, el primero a ≤ 12 meses y ≤ 24 meses entre hitos | OPERADOR | — |
| P-49 | Degradación automática de H5 (V1.1) | Tasa de hitos cumplidos < 50 % con ≥ 20 hitos resueltos en la celda segmento × H5 → «No» en esa celda | CALIBRABLE | PENDIENTE_OPERADOR |
| P-50 | Rangos de horizonte principal por naturaleza de la inversión (V1.1) | TACTICA H1–H2 · CICLICA H2–H4 · PRIMA_RIESGO H2–H4 · VALORACION H3–H4 · ESTRUCTURAL H4–H5 (LIQUIDEZ no se usa en Forex); fuera de rango solo con `justificacion_horizonte` | OPERADOR | — |

### 4.4 Pesos iniciales de las dimensiones (P-12)

| Puntuación | Dimensiones y pesos |
|---|---|
| T | Magnitud 20; alcance 15; velocidad 15; duración 10; difusión 10; posición en la cadena de transmisión 10; capacidad transformadora 10; claridad causal 10 |
| E | Calidad e independencia de las raíces 25; cobertura de las variables esenciales 15; calidad metodológica 15; trazabilidad 15; actualidad 10; discrepancias resueltas 10; objeciones del CT-13 respondidas 10 |
| M | Adopción 20; escalado 15; indicadores disponibles 15; persistencia 15; estabilidad de los impulsores 15; hitos claros 20 |
| P | T 40; novedad 20; incertidumbre reducible 20; coste-eficiencia 20 |
| A (FX) | Asimetría rentabilidad/riesgo esperada (escenarios del Motor sobre el indicador de seguimiento, en rentabilidad total) 30; valoración y desviación del equilibrio (PPA, BEER, REER; lo que descuentan el forward y la curva) 20; carry (a favor o en contra de la tesis, ajustado por volatilidad) 15; catalizadores identificados y fechados 15; momento y posicionamiento (posicionamiento extremo a favor de la tesis puntúa bajo) 10; convertibilidad y profundidad del mercado 10. Tope de valoración 40 con narrativa saturada. No puntúa instrumentos concretos ni sus costes |

### 4.5 Matriz inicial de aplicabilidad de horizontes (P-31; Documento 0, 8.3)

| Segmento | H1 días | H2 semanas | H3 meses | H4 años (1–5) | H5 décadas (5–30) |
|---|---|---|---|---|---|
| G10N | Sí (eventos de bancos centrales y datos) | Sí | Sí | Sí (valor y equilibrio) | Limitado |
| G10M | Sí | Sí | Sí | Sí | Limitado |
| EMAS | Limitado (gestión y controles) | Sí | Sí | Limitado | Limitado |
| EMLA | Limitado (liquidez y eventos políticos) | Sí | Sí | Limitado | Limitado |
| EMEA | Limitado | Sí | Sí | Limitado | Limitado |
| ESTR | No | Sí | Sí | Sí | Limitado |

«Limitado» significa que el horizonte solo se ofrece con liquidez suficiente y un catalizador identificado. En **H5** (V1.1) significa además: solo naturaleza `ESTRUCTURAL` en los tres ámbitos de P-48, probabilidad siempre cualitativa y evaluación por hitos; nunca pasa a «Sí» sin un cambio de tipo 3 y puede pasar a «No» por P-49.

### 4.6 Referencias de comparación por segmento (P-32; Documento 0, 8.4; propuesta inicial a ratificar por el operador)

| Segmento | Pronósticos direccionales de un par | Rentabilidad total y rentabilidad relativa de las opciones |
|---|---|---|
| G10N | Paseo aleatorio (sin cambio) y forward como predictor | Rentabilidad en exceso nula (posición neutra en liquidez de la divisa base del usuario, P-34) |
| G10M | Paseo aleatorio y forward | Rentabilidad en exceso nula (ídem) |
| EMAS | Paseo aleatorio y forward (o NDF) | Cesta equiponderada de divisas emergentes del segmento frente al USD, con carry |
| EMLA | Paseo aleatorio y forward (o NDF) | Cesta equiponderada de divisas emergentes del segmento frente al USD, con carry |
| EMEA | Paseo aleatorio y forward (o NDF) | Cesta equiponderada de divisas emergentes del segmento frente al USD, con carry |
| ESTR | Paseo aleatorio sobre el índice de la estrategia | Índice de la estrategia equivalente, o rentabilidad nula si no existe |

Las cestas equiponderadas excluyen las divisas sin exposición accesible (PS3) y las de tipo fijo, y se reequilibran mensualmente; si HT-01 no dispone de una serie, el Evaluador usa la sustituta más próxima y lo declara.

### 4.7 Bandas verbales de probabilidad (P-33)

| Banda | Intervalo | Probabilidad interna por defecto |
|---|---|---|
| Muy probable | 80–95 % | 85 % |
| Más probable que no | 60–75 % | 65 % |
| Incierto | 45–55 % | 50 % |
| Poco probable | 25–40 % | 35 % |
| Muy poco probable | 5–20 % | 15 % |

## 5. Estados y transiciones

Cada parámetro: `VIGENTE` → (cambio) `VIGENTE` con nueva versión; para CALIBRABLE: `VIGENTE` → `EN_SOMBRA` (durante un trimestre tras el cambio) → `VIGENTE` (confirmado) o reversión (`CFG-` nuevo con `revierte_a`). Bandas: `PENDIENTE_OPERADOR` → `DEFINIDA` (decisión de tipo 3).

## 6. Índices de consulta

| Índice | Clave | Uso |
|---|---|---|
| Valores vigentes por fecha | `param_id`, `fecha_efecto` | Lo que aplica un RUN-FX- concreto (reproducibilidad) |
| Por régimen | `regimen` | Validación de escrituras |
| En sombra | `en_sombra` = true | Evaluador y HT-03 |
| Por versión de metodología | `methodology_version` | G3-EST-04; certificados |
| Bandas pendientes | `banda.estado` = PENDIENTE_OPERADOR | Cola de tipo 3 |
| Servicio vigente | P-01, P-02, P-03, P-21, P-29, P-34 | Coordinador (F0 y respuestas al Broker) |

## 7. Ejemplos ficticios

> **EJEMPLOS FICTICIOS — no son entradas reales.**

Cambio calibrable de pesos de A (carry mayor, momento y posicionamiento menor):

```json
{"cfg_id":"CFG-FX-2027-0003","param_id":"P-12","de":{"A":{"asimetria":30,"valoracion":20,"carry":15,"catalizadores":15,"momento_posicionamiento":10,"convertibilidad":10}},
 "a":{"A":{"asimetria":30,"valoracion":20,"carry":20,"catalizadores":15,"momento_posicionamiento":5,"convertibilidad":10}},"regimen":"CALIBRABLE","autor":"AG-20",
 "origen":{"aju_id":"AJU-2027-0003"},"motivo":"Mejora fuera de muestra del IC de Spearman RK–rentabilidad total relativa en H3 (G10M y EMLA)",
 "methodology_version":{"de":"FX-1.0","a":"FX-1.1"},"fecha_registro":"2027-04-01","fecha_efecto":"2027-04-05","revierte_a":null}
```

Cambio de servicio de la divisa base del usuario:

```json
{"cfg_id":"CFG-FX-2027-0004","param_id":"P-34","de":"EUR","a":"USD","regimen":"SERVICIO","autor":"AG-01",
 "origen":{"ret_id":"RET-2027-0011"},"motivo":"Petición del Broker por CT-04","methodology_version":{"de":"FX-1.1","a":"FX-1.1"},
 "fecha_registro":"2027-04-08","fecha_efecto":"2027-04-12","revierte_a":null}
```
