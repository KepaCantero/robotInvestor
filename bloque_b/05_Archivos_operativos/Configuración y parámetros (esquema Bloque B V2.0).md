# Esquema de archivo operativo — F10 Configuración y parámetros

**Bloque B · Robot Investor · Versión óptima V2.0 · actualizado V2.1, 03/11/2026** · Subordinado al Documento 0 del Bloque B óptima V2.1 (ante discrepancia, manda el Documento 0).

---

## 1. Propósito

F10 publica los **valores vigentes** de todos los parámetros del Bloque B (Anexo A del Documento 0 y los asociados de 2.7, 7.2, 8.3, 8.5, 8.6, 9.1–9.9 y 12.2), con su **régimen** (quién puede cambiarlo y dentro de qué banda), su historial de cambios y la `methodology_version` vigente. Incluye la **política de autorización automática del Broker** (reglas POL-), el **marco de invertibilidad por defecto**, el top-N, los pesos y umbrales vigentes y el **registro de conectores de datos** activos. Todo agente y toda herramienta (HT-03, HT-08, HT-09, HT-11) leen de aquí lo que aplican. Un valor que no esté en F10 no es vigente.

## 2. Propietario, lectores y contratos

| Régimen | Quién escribe | Cómo | Ejemplos |
|---|---|---|---|
| SERVICIO | AG-B01 Coordinador | A petición del Broker por CT-B-04, registrada en F1 (RET-B) | Política de autorización automática, tope de autorización automática (≤ 480 min), criterios de nivel AUTO, objetivos de tiempo por nivel, marco de invertibilidad, top-N, idioma |
| CALIBRABLE | AG-B23 Evaluador | Dentro de banda, con evidencia (`aju_id` en F5), evaluación en sombra y versión menor de metodología | Pesos de A, E, C y S; umbrales de veredicto; matriz de estrategia; mínimos de pureza; caducidades de F6; modelo de tiempos; aplicabilidad de horizontes |
| OPERADOR | Operador humano | Propuesta de tipo 3 aprobada (`p3_id`); el Orquestador verifica la publicación y la registra en HA | Umbral de 30 minutos, margen de la PTA, corroboración mínima, certificados, antigüedad máxima de datos, conectores de pago, retención |

**Lectores**: todos los agentes y herramientas. **Contratos**: CT-B-04 (cambios de servicio), CT-B-22 (difusión de ajustes), cola de tipo 3 en HA (cambios del operador).

## 3. Reglas

1. **Escritura por régimen** (R8): un cambio fuera del régimen del parámetro se rechaza; el Coordinador responde al Broker con el motivo (RET-B `APLICADA_PARCIALMENTE` o `RECHAZADA`) y no se escribe nada.
2. **Bandas** (12.2): cada peso ±5 puntos por trimestre y ±15 en total frente al valor inicial; cada umbral ±5 por trimestre y ±10 en total; mínimos de pureza ±10 en total. Un CALIBRABLE sin banda explícita en el Documento 0 lleva banda `PENDIENTE_OPERADOR` con una propuesta: mientras el operador no la ratifique, todo cambio es tipo 3 (R27).
3. **Intocables por ajuste automático** (12.6): reglas críticas, seguridad, canales, matriz de archivos y el **umbral de 30 minutos**.
4. **Límites del servicio**: el Broker no puede quitar las exclusiones de valores sancionados o suspendidos ni admitir opciones binarias (2.7); no puede activar un horizonte «No» de la matriz 8.6; no puede fijar un tope de autorización automática superior a 480 minutos; no puede cambiar parámetros de otro régimen.
5. **Versionado**: todo cambio CALIBRABLE incrementa la versión menor de metodología (2.0 → 2.1); un cambio mayor del operador (2.x → 3.0) **revoca los certificados vigentes**. Los cambios de SERVICIO no cambian la versión de metodología.
6. **Efecto**: cada cambio declara `fecha_efecto`; las peticiones en curso terminan con los valores con que empezaron (registrados en su RUN-B). La política de autorización vigente es la del momento en que se dispara la puerta.
7. **Append-only**: el historial conserva todos los valores; una reversión es un cambio nuevo (`revierte_a`).
8. Como máximo un ajuste por trimestre por parámetro CALIBRABLE y tres parámetros en sombra simultánea.
9. **Prefijos internos**: `P-B-NN` (parámetro) y `CFG-B-AAAA-NNNN` (cambio); `POL-n` (regla de política, Anexo C).

## 4. Formato de entrada

### 4.1 Registro de parámetro

`param_id` (`P-B-NN`), `nombre`, `valor_inicial`, `valor_vigente`, `unidad`, `regimen` (SERVICIO · CALIBRABLE · CALIBRABLE_RESTRINGIDO · OPERADOR), `banda` `{trimestral, total, estado DEFINIDA·PENDIENTE_OPERADOR, propuesta}`, `acumulado_vs_inicial`, `escritor_autorizado` (AG-B01 · AG-B23 · OPERADOR), `ultimo_cambio` `{cfg_id, fecha_efecto, origen ret_id·aju_id·p3_id}`, `en_sombra`.

### 4.2 Registro de cambio (CFG-B)

`cfg_id`, `param_id`, `de`, `a`, `regimen`, `autor`, `origen` (`ret_id` · `aju_id` · `p3_id`), `motivo`, `methodology_version` `{de, a}`, `fecha_registro`, `fecha_efecto`, `revierte_a`.

### 4.3 Volcado inicial del Anexo A

| ID | Parámetro | Valor inicial | Régimen | Banda |
|---|---|---|---|---|
| P-B-01 | Umbral de la puerta de tiempo | 30 minutos (estimación p80) | OPERADOR | — |
| P-B-02 | Margen de la PTA sobre el tiempo autorizado | +10 % o +5 min, lo que sea mayor | OPERADOR | — |
| P-B-03 | Objetivos de tiempo por nivel | N0 < 2 min · N1 ≤ 10 min · N2 ≤ 30 min · N3 hasta 240 min si el Broker no indica tiempo | SERVICIO | — |
| P-B-04 | Presupuesto orientativo por nivel | N0 ≈ 1 UC · N1 ≈ 15 · N2 ≈ 60 · N3 ≥ 150 · N1-SEG ≈ 5 UC por ciclo (V2.1); sin techo; registro obligatorio | CALIBRABLE | PENDIENTE_OPERADOR (propuesta: ±10 % por trimestre; ±25 % total) |
| P-B-05 | Definición de 1 UC | ≈ 8 000 tokens de entrada y 1 500 de salida, o un cálculo de plan STD | OPERADOR | — |
| P-B-06 | Criterios de nivel AUTO | N3: relevancia de origen ALTA sin ficha F6 vigente, o alto impacto · N1: ficha F6 vigente < 30 días y pregunta acotada · N2: resto | SERVICIO | — |
| P-B-07 | Política de autorización automática | Ninguna regla (todas las ampliaciones son manuales) | SERVICIO | Tabla 4.5 |
| P-B-08 | Tope absoluto de autorización automática | 240 min por petición | SERVICIO | ≤ 480 min |
| P-B-09 | Recordatorio y caducidad de autorizaciones pendientes | Recordatorio a las 24 h; CADUCADA a los 7 días | SERVICIO | — |
| P-B-10 | Modelo de tiempos | Regresión por tipo de nodo sobre F1; p50 y p80; reestimación mensual con ≥ 20 peticiones nuevas | CALIBRABLE | Versión MOD-B en F5; nunca cambia P-B-01 |
| P-B-11 | Marco de invertibilidad por defecto | Tabla 4.7 (2.7) | SERVICIO | Exclusiones de sancionados y suspendidos, y de opciones binarias, no modificables |
| P-B-12 | Top-N por tipo de activo | N1: 3 · N2: 5 + 2 alternativas · N3: 10 + 5 alternativas · PERS: según límite | SERVICIO | Véase la nota de 4.8 |
| P-B-13 | Hipótesis competidoras mínimas | N1: 1 · N2: 2 de naturaleza distinta · N3: ≥ 2 | OPERADOR | — |
| P-B-14 | Cuota de búsquedas de discriminación | N1: contraste junto a la hipótesis · N2: 1 por tesis · N3: 1 por hipótesis no cerrada | CALIBRABLE | PENDIENTE_OPERADOR |
| P-B-15 | Matriz de estrategia y moduladores | Documento 0, 8.3.1–8.3.3 | CALIBRABLE | ±5 por trimestre; ±15 total por celda (columnas renormalizadas a 100) |
| P-B-16 | Desviación del Director sobre la matriz | ±5 puntos por dimensión con justificación | OPERADOR | — |
| P-B-17 | Pesos de A | Tabla 4.4 | CALIBRABLE | ±5 / ±15 por peso |
| P-B-18 | Pesos de E | Tabla 4.4 | CALIBRABLE | ±5 / ±15 por peso |
| P-B-19 | Fórmula de C | 0,20·A + 0,35·E + 0,25·RF + 0,20·RE; tope C ≤ E + 10 | CALIBRABLE (pesos) · OPERADOR (tope) | ±5 / ±15 por peso |
| P-B-20 | Umbrales del veredicto del ámbito | INVERTIR: A ≥ 65, E ≥ 60, C ≥ 65 · ESCALONADO: A ≥ 60, E ≥ 60, C ≥ 55 · VIGILAR: A ≥ 50 · DESCARTAR: A < 50 | CALIBRABLE | ±5 / ±10 por umbral |
| P-B-21 | GC2 / PV2 (V2.1: GC2 integrada en PV2) | A provisional ≥ 50 y E provisional ≥ 50, tesis viva tras una autorrefutación | CALIBRABLE | ±5 / ±10 |
| P-B-22 | Pesos de S por playbook | Tabla 4.6 (8.5.1–8.5.12) | CALIBRABLE | ±5 / ±15 por peso |
| P-B-23 | Mínimos de pureza (PC2) | Los de cada playbook (tabla 4.6) | CALIBRABLE | ±10 puntos total |
| P-B-24 | Umbrales del candidato | PRIORITARIO_PARA_C: S ≥ 65 y extremo inferior del IC 90 % ≥ 55 · SECUNDARIO: S ≥ 50 | CALIBRABLE | ±5 / ±10 |
| P-B-25 | GC3 | 2 × top-N por S provisional | CALIBRABLE | PENDIENTE_OPERADOR (propuesta: 1,5× a 3×) |
| P-B-26 | Diversidad | Solapamiento > 80 % = duplicado · ≤ 2 emisiones por emisor (RF) · ≤ 40 % del top-N por subclúster · correlación > 0,9 a 2 años = duplicado | CALIBRABLE | PENDIENTE_OPERADOR |
| P-B-27 | Banda marginal | Ámbito: ≤ 5 puntos del umbral · Candidato: ≤ 3 puntos del umbral o del corte | OPERADOR | — |
| P-B-28 | Filtros de liquidez por defecto | RV ≥ 1 M€/día · INM ≥ 0,5 M€/día · ETF ≥ 100 M€ de patrimonio · DER ≥ 1 000 contratos de interés abierto · CRI ≥ 500 M€ de capitalización | CALIBRABLE | PENDIENTE_OPERADOR (propuesta: ±25 % por trimestre) |
| P-B-29 | Corroboración mínima (PA1) | 2 raíces independientes A/B o 1 fuente primaria A | OPERADOR | — |
| P-B-30 | Antigüedad máxima de datos de mercado | H1: 1 día · H2: 3 días · H3: 7 días · H4: 30 días · H5: 90 días (V2.1) | OPERADOR | — |
| P-B-31 | Antigüedad máxima de fundamentales | Último periodo publicado; > 6 meses desde el cierre se declara | OPERADOR | — |
| P-B-32 | Caducidad por dimensión en F6 | D1, D4, D11: 12 m · D2, D3, D5: 6 m · D6, D8: 3 m · D7, D12: 1 m · D9: 7 días (H1–H2), 1 m (H3–H4) o 3 m (H5) · radar de emergentes: 3 m (V2.1) · D10: 7 días · universos: 1 m · régimen: 1 m | CALIBRABLE | PENDIENTE_OPERADOR (propuesta: ±50 % por trimestre) |
| P-B-33 | Cambio material (GC0) | Indicador > 1,5 σ desde la ficha; evento del calendario; dato con sorpresa > 1 σ; invalidación a < 10 % | CALIBRABLE | PENDIENTE_OPERADOR (propuesta: ±0,25 σ por trimestre) |
| P-B-34 | Muestreo de la auditoría previa | N0: 10 % · N1: 30 % · N2 y N3: 100 % · informe de parada: 30 % · informe de seguimiento (N1-SEG): 20 % (V2.1) | CALIBRABLE (N0, N1) · OPERADOR (N2, N3) | PENDIENTE_OPERADOR (propuesta: ±10 pp por trimestre en N0 y N1) |
| P-B-35 | Vueltas del bucle de auditoría | 3 | OPERADOR | — |
| P-B-36 | Certificado de probabilidad | n ≥ 100; extremo inferior del IC 90 % del BSS > 0; ECE ≤ percentil 90 nulo y < 0,15; Holm | OPERADOR | — |
| P-B-37 | Certificado de ranking | ≥ 30 rankings por playbook × horizonte; IC de rango medio y exceso del top-N con extremo inferior del IC 90 % > 0 | OPERADOR | — |
| P-B-38 | Muestra mínima para recalibrar | 30 pronósticos o 15 rankings resueltos por celda | OPERADOR | — |
| P-B-39 | Bandas verbales | Tabla 4.9 | CALIBRABLE | PENDIENTE_OPERADOR |
| P-B-40 | Escala de riesgo 1–5 | Volatilidad anualizada de la exposición con ajustes por colas, liquidez y caída máxima (ficha del Catálogo) | CALIBRABLE | PENDIENTE_OPERADOR |
| P-B-41 | Frecuencia del Vigía | H1: diaria · H2: cada 2 días hábiles · H3: semanal · H4: mensual · H5: trimestral y en cada fecha de hito (V2.1); y en cada catalizador fechado | CALIBRABLE | PENDIENTE_OPERADOR |
| P-B-42 | Clasificación de alertas | FLUCTUACION · REVISION · INVALIDACION_PROBABLE · INVALIDACION_CONFIRMADA | OPERADOR | — |
| P-B-43 | Criterio de separación del Vigía | > 150 REC-B vigentes en vigilancia o > 40 % del tiempo de AG-B23 dos meses seguidos | OPERADOR | — |
| P-B-44 | Caducidad de la vigilancia pre-salida a bolsa | Dos horizontes del análisis de origen sin señal relevante | CALIBRABLE | PENDIENTE_OPERADOR |
| P-B-45 | Presupuesto de tareas de fondo | Vigía 4 UC/semana · Evaluación 3 · DOC-A 3 · BFA 3 · DOC-M 2 (barridos HT-02 sin UC) | CALIBRABLE | PENDIENTE_OPERADOR |
| P-B-46 | Pregunta repetida | 3 veces en 4 semanas | CALIBRABLE | PENDIENTE_OPERADOR |
| P-B-47 | Umbral de escalado por instancias | Cola > 3 encargos o tiempo de respuesta > 2× el objetivo | CALIBRABLE | PENDIENTE_OPERADOR |
| P-B-48 | Barrido de enlaces | Semanal (domingo) | CALIBRABLE | PENDIENTE_OPERADOR |
| P-B-49 | Criterio de borrado por baja calidad | Q < 50 sin uso en 180 días | CALIBRABLE | PENDIENTE_OPERADOR |
| P-B-50 | Conectores de datos activos | Solo gratuitos (con registro o clave gratuita); de pago desactivados | OPERADOR | Tabla 4.10 |
| P-B-51 | Numeración de los Bloques C | C.1 RV … C.12 TCV (2.6), provisional | OPERADOR | — |
| P-B-52 | Referencias de comparación | Las de cada playbook (8.5) y 9.11 | OPERADOR | — |
| P-B-53 | Retención | F1–F6, F11, RC, HA: indefinida · artefactos del Motor y anexos de datos: 5 años · extractos externos: mínimos | OPERADOR | — |
| P-B-54 | Idioma | es-ES (informe visual en el idioma configurado por el Broker) | SERVICIO | — |
| P-B-55 | Versión de metodología | 2.1 (V2.1, 03/11/2026) | CALIBRABLE (menores) · OPERADOR (mayores) | — |
| P-B-56 | Aplicabilidad de horizontes por tipo de activo | Tabla 4.8 (8.6) | CALIBRABLE_RESTRINGIDO | «Sí» ↔ «Limitado» dentro de 12.2 con evidencia; todo cambio desde o hacia «No», tipo 3 |
| P-B-57 | Regla de relevancia decisional | 7.9 | OPERADOR (interpretación: el Documento 0 no le asigna régimen; se aplica la regla más restrictiva) | — |
| P-B-58 | Objetivos orientativos por capa (p50) (V2.1) | N1: capa 0 1 min · 1: 3 · 2: 3 · 3: 2 · 4: 1 — N2: 3 · 6 · 9 · 8 · 4 — N3: 5 · 8 · 30–60 · 60–120 · 30–60 | CALIBRABLE | PENDIENTE_OPERADOR |
| P-B-59 | PV1 · criterios eliminatorios (V2.1) | Ningún tipo de activo con ≥ 1 instrumento que supere PC1 en el universo preliminar · alerta grave de integridad en la premisa central · ficha F6 vigente con DESCARTAR y sin cambio material (GC0) | OPERADOR | — |
| P-B-60 | PV1 · criterios de debilidad (dos o más = parada) (V2.1) | Materialidad: capitalización o patrimonio invertible agregado < 2 000 M€, o < 3 instrumentos invertibles en todos los tipos · Ya descontado: percentil ≥ 90 de 10 años con saturación narrativa probable (≥ 3 de 6 indicadores) y sin tesis diferencial · Tesis sin mecanismo plausible | CALIBRABLE | ±5 / ±10 por umbral |
| P-B-61 | PV3 (V2.1) | ≥ 1 eslabón con AE ≥ 60 o PCB ≥ 30 (con ≥ 2 indicadores en rojo) que tenga ≥ 1 opción con PC1–PC4 superadas y S provisional ≥ 50 | CALIBRABLE | ±5 / ±10 |
| P-B-62 | Plazo para forzar la continuación tras una parada (V2.1) | 7 días desde la entrega del informe de parada | SERVICIO | — |
| P-B-63 | Umbrales de los indicadores de cuello, ámbar / rojo (V2.1) | Utilización 85–90 % / > 90 % · plazos > 1,5× / > 2× media de 5 años · book-to-bill > 1,1 dos trimestres / > 1,2 cuatro trimestres · HHI de proveedores 1 500–2 500 / > 2 500 · primer país > 40 % / > 60 % · margen sobre eslabones adyacentes > +5 / > +10 pp · spot/contrato > 1,15 / > 1,3 · nueva capacidad frente al plazo hasta el déficit (igual / mayor) · permisos > 12 / > 24 meses · inventarios < p25 / < p10 · insumo sin sustituto: rojo | CALIBRABLE | PENDIENTE_OPERADOR |
| P-B-64 | Cuello material (V2.1) | PCB ≥ 30 y ≥ 2 indicadores en rojo; PCB = round(100 · severidad · persistencia · relevancia / 125) | CALIBRABLE | ±5 / ±10 (umbral) |
| P-B-65 | Pesos de AE y eslabón atractivo (V2.1) | Crecimiento 20 · margen y ROIC relativos 20 · poder de negociación y barreras 15 · cuello favorable 20 · expectativas descontadas (inversa) 15 · sustitución (inversa) 10; atractivo: AE ≥ 60 | CALIBRABLE | ±5 / ±15 por peso; ±5 / ±10 el umbral |
| P-B-66 | Pesos de PEM (V2.1) | Tecnología 20 · tracción 25 · equipo 15 · financiación 15 · posición en la cadena 15 · vía de exposición 10 | CALIBRABLE | ±5 / ±15 por peso |
| P-B-67 | Mejores opciones por eslabón (V2.1) | Hasta 5 (N1: hasta 3, solo el eslabón crítico); adicionales al top-N, sin duplicar | SERVICIO | — |
| P-B-68 | Profundidad del desglose de la cadena (V2.1) | N1: eslabón crítico hasta actividad · N2: eslabones del plan hasta actividad e insumos críticos de los eslabones con cuello · N3: cadena completa hasta insumo o nodo crítico | CALIBRABLE | PENDIENTE_OPERADOR |
| P-B-69 | Hitos intermedios H5 (V2.1) | ≥ 3 por tesis H5, con fecha entre 1 y 5 años; dos hitos críticos incumplidos generan alerta `REVISION` | OPERADOR | — |
| P-B-70 | Consultas al Broker · límites (V2.1) | Por petición: N1 1 · N2 3 · N3 6 · PERS según el límite · ciclo N1-SEG 1; BLOQUEANTES como máximo 1 (N3: 2) | SERVICIO | — |
| P-B-71 | Consultas al Broker · plazos (V2.1) | BLOQUEANTE: 4 h (recordatorio a las 2 h) · NO_BLOQUEANTE: hasta el inicio de F8 o 48 h · al vencer: supuesto declarado aplicado | SERVICIO | — |
| P-B-72 | Consulta recurrente (V2.1) | La misma clase de duda (tipo y tema) en 3 peticiones distintas en 8 semanas | CALIBRABLE | PENDIENTE_OPERADOR |
| P-B-73 | Seguimientos encargados · frecuencias (V2.1) | DIARIA · SEMANAL · QUINCENAL · MENSUAL · TRIMESTRAL · PERSONALIZADA (N ≥ 1 días); mayor que la del Vigía para el horizonte principal: aceptada con advertencia | SERVICIO | — |
| P-B-74 | Seguimientos encargados · límites (V2.1) | Máximo 25 activos; ciclo < 10 min con PT30; ≈ 5 UC por ciclo; línea base ≤ 20 min; sin fecha de fin, recordatorio cada 6 meses; pausado > 6 meses, recordatorio trimestral | SERVICIO | — |

### 4.4 Pesos iniciales de A y E (P-B-17, P-B-18)

| Puntuación | Componentes y pesos |
|---|---|
| A | Asimetría 25 · valoración frente a expectativas 20 (tope 40 con saturación narrativa) · calidad del crecimiento 15 · ventaja estructural y barreras 10 · catalizadores 10 · momento y flujos 10 · riesgos (inversa) 10 |
| E | Calidad e independencia de raíces 25 · cobertura dimensional ponderada por la matriz 15 · calidad metodológica y de los datos 15 · trazabilidad 15 · actualidad 10 · discrepancias resueltas 10 · hipótesis competidoras cerradas 10 |

### 4.5 Política de autorización automática (P-B-07)

Cada regla es un objeto `POL-n` evaluado en orden; se aplica la primera que cubre el caso. Si ninguna cubre, o si la estimación supera el tope P-B-08, la decisión es manual.

| Campo | Valores / formato |
|---|---|
| `regla_id` | `POL-n` |
| `orden` | Entero (evaluación ascendente) |
| `condicion` | `{relevancia ALTA·MEDIA·BAJA·null, nivel [N1,N2,N3,PERS], origen BLOQUE_A·LIBRE·null, siguiente_paso_A ENVIAR_A_BLOQUE_B·null, alto_impacto, puerta PT30·PTA·null, minutos_p80_min, minutos_p80_max}` (umbrales opcionales sobre la estimación p80 que dispara la puerta) |
| `accion` | AUTORIZAR_HASTA · ELEGIR_OPCION · DECISION_MANUAL |
| `minutos` / `uc` | Si AUTORIZAR_HASTA (minutos ≤ P-B-08) |
| `opcion` | Si ELEGIR_OPCION: VERSION_30_MIN · DIVIDIR_EN_FASES |
| `vigencia` | `{desde, hasta}` |
| `ret_id` | Comunicación del Broker que la creó |

En todos los casos el Coordinador **genera, registra y notifica la justificación** (AUT-B `AUTORIZACION_AUTOMATICA_NOTIFICADA`, R20).

### 4.6 Pesos de S y mínimos de pureza por playbook (P-B-22, P-B-23)

| Playbook | PE | QL | VA | MO | RI | LA | CO | Mínimo PC2 |
|---|---|---|---|---|---|---|---|---|
| SEL-RV | 20 | 20 | 20 | 15 | 15 | 10 | NA | 25 % ingresos o EBIT |
| SEL-RF | 15 | 25 | 25 | 5 | 15 | 15 | NA | 25 % |
| SEL-DIV | 10 | 15 | 25 | 15 | 15 | 10 | 10 | Beta significativa al 90 % y del signo de la tesis |
| SEL-MP | 20 | 10 | 20 | 15 | 10 | 15 | 10 | Correlación ≥ 0,8 con la referencia física |
| SEL-IDX | 25 | 15 | 20 | 15 | 10 | 10 | 5 | 60 % del índice en el ámbito |
| SEL-FON | 25 | 20 | 10 | 5 | 10 | 15 | 15 | 50 % del patrimonio |
| SEL-DER | 20 | NA | 25 | 5 | 20 | 20 | 10 | Subyacente con PE ≥ 60 % |
| SEL-INM | 15 | 20 | 25 | 10 | 15 | 10 | 5 | 50 % del GAV |
| SEL-CRI | 15 | 20 | 20 | 15 | 15 | 10 | 5 | 50 % |
| SEL-ALT | 15 | 20 | 20 | 5 | 15 | 10 | 15 | 50 % del NAV |
| SEL-MON | 5 | 25 | 30 | NA | 10 | 15 | 15 | Divisa y plazo del ámbito |
| SEL-TCV | 25 | NA | 25 | 5 | 15 | 15 | 15 | 70 % de la sensibilidad en el factor |

NA redistribuye su peso proporcionalmente (8.5.0). Los pesos internos de las métricas de cada componente viven en el prompt del Seleccionador y en el perfil SEL- del Catálogo (CC).

### 4.7 Marco de invertibilidad por defecto (P-B-11; 2.7)

`{perfil: MINORISTA_UE_DEFECTO, mercados: regulados y SMN del EEE, Reino Unido, Suiza, EE. UU., Canadá, Japón, Australia, Hong Kong, Singapur (otros solo vía vehículo), vehiculos: UCITS con KID PRIIPs (no UCITS solo informativo), derivados: solo listados; opciones binarias excluidas; CFD excluidos salvo indicación expresa, cripto: proveedores MiCA o ETP del EEE, divisa_base: EUR, denominacion_minima_RF: señalada > 1 000 € (penaliza LA), exclusiones_fijas: sancionados (UE, ONU, OFAC) y suspendidos}`.

### 4.8 Aplicabilidad de horizontes (P-B-56; 8.6) y nota sobre el top-N

**Por tipo de activo** (V2.1: columna H5; un horizonte es admisible si lo es en esta tabla y en la de tipo de objeto, y «Limitado» en cualquiera lo hace limitado):

| Tipo | H1 | H2 | H3 | H4 | H5 |
|---|---|---|---|---|---|
| RV, IDX | Limitado | Sí | Sí | Sí | Sí |
| RF | Limitado | Sí | Sí | Sí | Limitado |
| DIV | Sí | Sí | Sí | Limitado | Limitado |
| CRI, TCV | Sí | Sí | Sí | Limitado | Limitado |
| MP | Sí (energía y metales líquidos) | Sí | Sí | Sí | Limitado (superciclos y transición) |
| FON, INM | No | Limitado | Sí | Sí | Sí |
| DER | Sí | Sí | Sí (≤ 12 meses) | No | No |
| ALT | No | No | Limitado | Sí | Sí |
| MON | Limitado | Sí | Sí | No | No |

**Por tipo de objeto** (V2.1):

| Tipo de objeto | H1 | H2 | H3 | H4 | H5 |
|---|---|---|---|---|---|
| SECTOR | Limitado | Sí | Sí | Sí | Sí |
| TEMATICA | No | Limitado | Sí | Sí | Sí |
| MERCADO_GEOGRAFICO | Limitado | Sí | Sí | Sí | Sí |
| SEGMENTO_DE_CLASE | Sí | Sí | Sí | Sí | Limitado |
| ESTRATEGIA_FACTOR | Limitado | Sí | Sí | Sí | Limitado |
| CADENA_DE_VALOR | No | Limitado | Sí | Sí | Sí |

H5 (décadas, 5–30 años; 1260 sesiones nominales): probabilidades siempre cualitativas y al menos tres hitos intermedios (P-B-69).

**Nota sobre el top-N**: es parámetro de **servicio** (Anexo A y A.2 del Documento 0): lo fija el Broker por CT-B-04 y el Evaluador solo puede **proponer** cambios (CT-B-22) con su evidencia.

### 4.9 Bandas verbales (P-B-39)

Muy probable 80–95 % · Más probable que no 60–75 % · Incierto 45–55 % · Poco probable 25–40 % · Muy poco probable 5–20 %. La probabilidad interna se registra siempre en F4.

### 4.10 Registro de conectores de datos (P-B-50)

`{conector_id, proveedor, ficha_F9, tipo GRATUITO·GRATUITO_CON_REGISTRO·DE_PAGO_FUTURO, requiere_credencial sí/no, credencial_ref (alias de la bóveda; nunca la clave), estado ACTIVO·SIN_CREDENCIAL·DESACTIVADO, degradacion_declarada, limite_llamadas, cred_id (F1)}`. Un conector `DE_PAGO_FUTURO` solo pasa a ACTIVO con decisión del operador (tipo 3).

## 5. Estados y transiciones

Parámetro: `VIGENTE` → (cambio) `VIGENTE` con nueva versión; para CALIBRABLE: `VIGENTE` → `EN_SOMBRA` (un trimestre) → `VIGENTE` (confirmado) o reversión (`CFG-B` con `revierte_a`). Banda: `PENDIENTE_OPERADOR` → `DEFINIDA` (tipo 3). Regla POL-: `VIGENTE` → `RETIRADA` (CT-B-04) · `CADUCADA` (fin de vigencia).

## 6. Índices de consulta

| Índice | Clave | Uso |
|---|---|---|
| Valores vigentes por fecha | `param_id`, `fecha_efecto` | Lo que aplica un RUN-B concreto (reproducibilidad; HT-03 y HT-09) |
| Por régimen | `regimen` | Validación de escrituras |
| Política vigente | `POL-n` con `vigencia` | Coordinador al dispararse PT30 o PTA |
| En sombra | `en_sombra` = true | Evaluador y HT-03 (cálculo en paralelo) |
| Por versión de metodología | `methodology_version` | G3; certificados |
| Conectores | `estado`, `requiere_credencial` | HT-01; solicitudes CRED-B |
| Bandas pendientes | `banda.estado` = PENDIENTE_OPERADOR | Cola de tipo 3 |

## 7. Ejemplo ficticio

> **EJEMPLO FICTICIO — no es una entrada real.**

```json
{"cfg_id":"CFG-B-2026-0002","param_id":"P-B-07","de":[],"a":[
   {"regla_id":"POL-1","orden":1,"condicion":{"relevancia":"ALTA","nivel":["N2","N3"],"origen":null,"siguiente_paso_A":null,"alto_impacto":null,"puerta":null,"minutos_p80_max":90},"accion":"AUTORIZAR_HASTA","minutos":90,"uc":null,"vigencia":{"desde":"2026-11-08","hasta":null}},
   {"regla_id":"POL-2","orden":2,"condicion":{"relevancia":null,"nivel":["N2","N3"],"origen":null,"siguiente_paso_A":null,"alto_impacto":null,"puerta":"PT30","minutos_p80_max":null},"accion":"ELEGIR_OPCION","opcion":"DIVIDIR_EN_FASES","vigencia":{"desde":"2026-11-08","hasta":null}}],
 "regimen":"SERVICIO","autor":"AG-B01","origen":{"ret_id":"RET-B-2026-0003"},"motivo":"Configuración inicial de la política por el Broker",
 "methodology_version":{"de":"2.0","a":"2.0"},"fecha_registro":"2026-11-08T10:02:00+01:00","fecha_efecto":"2026-11-08T10:02:00+01:00","revierte_a":null}
```
