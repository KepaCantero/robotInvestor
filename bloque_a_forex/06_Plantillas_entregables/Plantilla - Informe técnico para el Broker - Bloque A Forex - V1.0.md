# Plantilla — Informe técnico para el Broker (Bloque A Forex)

**Bloque A Forex · Robot Investor · Versión óptima V1.0 · 02/11/2026 · actualizado V1.1 (03/11/2026)** · Subordinado al Documento 0 del Bloque A Forex V1.1. Actualización V1.1: naturaleza de la inversión y horizonte principal por opción, H5 «limitado» con hitos y supuestos declarados (CT-23).

> **Uso.** Plantilla del entregable 14.1 del Documento 0 Forex. La rellena **AG-17 Redactor y Diseñador de Informes** a partir del paquete de síntesis (CT-15) y la publica **AG-01 Coordinador de Peticiones y Consultas** por CT-02. Los marcadores `{{…}}` se sustituyen por valores del paquete; los bloques entre `<!-- REPETIR: … -->` y `<!-- FIN REPETIR -->` se repiten por elemento y se eliminan si no hay ninguno; un comentario `<!-- REPETIR (fila con marcadores de la tabla siguiente): … -->` indica que la fila con marcadores de esa tabla se repite tantas veces como elementos haya (los comentarios se colocan fuera de las tablas para no romper su formato). Las líneas que empiezan por `> Instrucción:` se borran del entregable final.
>
> **Reglas que rigen todo el informe.**
> 1. **Mismos números en los tres entregables**: toda cifra, puntuación, estado, banda o identificador de este informe es idéntica a la del paquete JSON (`Paquetes JSON/`) y a la del informe visual del mismo `run_id`. El JSON es la fuente de verdad; ante discrepancia se corrige el origen y se regeneran los tres.
> 2. **Trazabilidad (R7)**: cada afirmación material lleva su `CLM-FX-`; cada cifra (diferenciales, carry, PPA, REER, volatilidades, posicionamiento), su `CALC-FX-` o su dato HT-01 con fecha y fuente (BCE, Fed H.10, WM/Reuters, BPI, CFTC). No se calcula nada al redactar.
> 3. **Vocabulario de confianza** en cada conclusión: *establecido · probable · especulativo · en disputa*.
> 4. **R13 y Meese-Rogoff**: sin certificado del Evaluador, ningún horizonte lleva probabilidad numérica; se usa la banda («más probable que no», «incierto», «poco probable») y la etiqueta «sin ventaja demostrada frente al paseo aleatorio». Todo pronóstico declara su referencia ingenua: paseo aleatorio (sin cambio) y, cuando procede, el forward como predictor (8.4).
> 5. **R14**: si un segmento tiene menos de tres opciones, se explica; nunca se rellena.
> 6. **Notación (2.4)**: todo par en convención de mercado BASE/COTIZADA con códigos ISO 4217 (EUR/USD = dólares por euro); en las opciones con par (PAR, CRUCE, REGIMEN) la dirección se refiere siempre a la base (`ALCISTA_BASE` o `BAJISTA_BASE`) y se acompaña de la frase «sube X, baja Y». En cestas, bloques y estrategias la dirección se expresa con la `composicion` (lado LARGO/CORTO y peso de cada divisa) y la divisa de financiación; en VOLATILIDAD, con `vista_volatilidad` (ALZA/BAJA y plazo). Cada pronóstico declara su `tipo_rentabilidad` (**PRECIO_CONTADO** o **RENTABILIDAD_TOTAL**, con carry) y su divisa de medición (G3-FX-11).
> 6 bis. **Identificadores**: todos llevan el infijo FX (`RUN-FX-`, `OPP-FX-`, `TND-FX-`, `PRG-FX-`, `CLM-FX-`, `EVD-FX-`, `CALC-FX-`, `QRY-FX-`, `LEC-FX-`, `TRV-FX-`).
> 7. **Frontera con el Bloque B (R21)**: el informe habla de **pares, cruces, cestas, bloques, estrategias y regímenes**, nunca de instrumentos (contado, forward, futuro, opción, ETF/ETC, CFD), proveedores, costes, apalancamiento, tamaño ni niveles de entrada. Los niveles del par solo aparecen como **condiciones de invalidación** o niveles de referencia. Mencionar que «existen futuros y opciones líquidos sobre el par» solo sirve para justificar la invertibilidad (PS3).
> 8. Registro formal, conciso, sin adornos. Tablas para lo comparable; prosa breve para el razonamiento.
> 9. Nombre del archivo: `Informes técnicos Broker/{{FECHA}}_informe-tecnico_{{RUN_ID}}.md` (y `.pdf` con el mismo nombre base).

---

# Informe técnico del Bloque A Forex — {{TITULO_RUN}}

| Campo | Valor |
|---|---|
| Identificador | `{{RUN_ID}}` (RUN-FX-AAAA-NNNN) |
| Tipo | {{TIPO}} (PERIODICO · AD_HOC · PROFUNDIZACION) |
| Fecha de referencia | {{FECHA}} |
| Datos de mercado al cierre de | {{FECHA_DATOS_MERCADO}} (cierre de Nueva York del viernes en el ciclo semanal) |
| Disparador | {{DISPARADOR}} (ciclo C1 programado · CT-01 de {{FECHA_PETICION}}) |
| Divisa base del usuario | {{DIVISA_BASE_USUARIO}} (F10; EUR por defecto) |
| Versión de metodología | {{METHODOLOGY_VERSION}} (FX-x.y) |
| Informes transversales (CT-06T) | `{{TRV_BCM_ID}}` (TRV-FX-, AG-09 Bancos Centrales y Macro Cambiaria) · `{{TRV_PFV_ID}}` (TRV-FX-, AG-21 Posicionamiento, Flujos y Volatilidad Cambiaria) · o declaración de su ausencia o reutilización (G3-FX-10) |
| Dictamen G3 | {{ESTADO_G3}} {{ADVERTENCIAS_G3}} |
| Estado del retorno | {{ESTADO}} (COMPLETO · PARCIAL) |
| Entregables hermanos | `{{RUTA_INFORME_VISUAL}}` · `{{RUTA_PAQUETE_JSON}}` |

---

## 1. Resumen ejecutivo

> Instrucción: máximo 250 palabras más la tabla. Responde a: qué ha cambiado, qué proponemos, cuántas apuestas independientes hay, cuál es la exposición neta al dólar (y a la divisa base del usuario) y qué decisión se le facilita al Broker. Empieza por lo más relevante para decidir, no por el contexto.

**Qué ha cambiado desde `{{RUN_ANTERIOR}}`.** {{CAMBIOS_VS_ANTERIOR}}

**Lectura del conjunto.** {{LECTURA_CONJUNTO}}

**Apuestas independientes: {{APUESTAS_INDEPENDIENTES}}.** {{DESCRIPCION_CLUSTERES}} (factor dominante de cada clúster: dólar, yen o refugio, carry y riesgo global, materias primas o una divisa concreta).

**Exposición neta al USD: {{EXPOSICION_USD}}** · **a la divisa base ({{DIVISA_BASE_USUARIO}}): {{EXPOSICION_DIVISA_BASE}}.**

<!-- REPETIR (fila con marcadores de la tabla siguiente): FILA_RESUMEN por cada opción (y una fila «—» por cada segmento sin opciones) -->
| Segmento | Semáforo | Opción (rango · nombre · `OPP-FX-`) | Par o composición · dirección | RK | Riesgo 1–5 | Relevancia | Siguiente paso |
|---|---|---|---|---|---|---|---|
| {{SEGMENTO}} | {{SEMAFORO}} | {{RANGO}} · {{NOMBRE}} · `{{OPP_ID}}` | {{PAR_O_COMPOSICION}} · {{DIRECCION}} | {{RK}} | {{RIESGO_1A5}} | {{RELEVANCIA_DECISIONAL}} | {{SIGUIENTE_PASO}} |

**Encargos para el Bloque B**: {{N_ENCARGOS_B}} (uno por opción del top-3, en `paquete_para_bloque_B` del JSON; el Broker decide si los reenvía, R4).

**Alertas** (si las hay): {{ALERTAS}} — p. ej., condición de invalidación cercana en una opción vigente, reunión de banco central en los próximos 5 días con opciones expuestas, objeción moderada sin resolver, dato desactualizado (PS2), riesgo de intervención.

---

## 2. Alcance, nivel, presupuesto y consumo

> Instrucción: datos de F5 y del paquete. Declarar toda reducción de alcance (R16). Los informes transversales de AG-09 y AG-21 tienen presupuesto propio (Anexo A: 6 UC cada uno por ciclo).

<!-- REPETIR (fila con marcadores de la tabla siguiente): FILA_ALCANCE por segmento activo -->
| Segmento | Nivel | GC0 (delta material) | Motivo GC0 | Presupuesto (UC) | Consumo (UC) | Desviación |
|---|---|---|---|---|---|---|
| {{SEGMENTO}} | {{NIVEL}} | {{GC0_SI_NO}} | {{GC0_MOTIVO}} | {{PRESUPUESTO_UC}} | {{CONSUMO_UC}} | {{DESVIACION_PCT}} |
| Transversales (AG-09, AG-21) | — | — | — | {{PRESUPUESTO_TRANSVERSAL}} | {{CONSUMO_TRANSVERSAL}} | {{DESVIACION_TRANSVERSAL}} |
| **Total** | — | — | — | **{{PRESUPUESTO_TOTAL}}** | **{{CONSUMO_TOTAL}}** | {{DESVIACION_TOTAL}} |

- **Alcance pedido**: {{ALCANCE}} (segmentos, divisas, pares, temáticas y pregunta).
- **Horizontes de interés**: {{HORIZONTES}} (aplicabilidad por segmento de la tabla 8.3: ESTR sin H1; EMAS, EMLA y EMEA con H1 y H4 «limitados»; H5 «limitado» en los seis segmentos).
- **Reducciones de alcance declaradas**: {{REDUCCIONES}} (o «ninguna»).
- **Modos degradados**: {{DEGRADACIONES}} (herramienta, credencial o fuente no disponible; efecto sobre las conclusiones).

---

## 3. Régimen macro y cambiario y exposición agregada

> Instrucción: 150–300 palabras. Resume los informes transversales de AG-09 (bancos centrales, sendas descontadas, sorpresas, diferenciales nominales y reales a 2 años, calendario, intervención) y de AG-21 (posicionamiento CFTC y percentiles, flujos, volatilidad implícita y realizada, risk reversals a 25 delta, base cruzada, crowding). Cada afirmación con `CLM-FX-` y nivel de confianza. Cierra con los dos o tres factores de los que dependen más opciones (enlaza con los clústeres).

{{REGIMEN_MACRO}}

**Régimen cambiario.** Dólar: **{{REGIMEN_DOLAR}}** (fuerte · neutro · débil) · riesgo: **{{REGIMEN_RIESGO}}** (apetito · neutro · aversión) · volatilidad: **{{REGIMEN_VOLATILIDAD}}** (baja · media · alta). {{REGIMEN_CAMBIARIO_NOTA}}

<!-- REPETIR (fila con marcadores de la tabla siguiente): FILA_BANCO_CENTRAL (bancos centrales relevantes del ciclo, del informe BCM) -->
| Banco central | Tipo actual | Senda descontada (12 meses) | Sesgo | Próxima reunión | Sorpresa reciente | Referencia |
|---|---|---|---|---|---|---|
| {{BANCO}} | {{TIPO_ACTUAL}} | {{SENDA_DESCONTADA}} | {{SESGO}} | {{PROXIMA_REUNION}} | {{SORPRESA}} | `{{CLM_O_CALC}}` |

<!-- REPETIR (fila con marcadores de la tabla siguiente): FILA_POSICIONAMIENTO_VOLATILIDAD (máx. 8, del informe PFV) -->
| Divisa o par | Posicionamiento neto CFTC (percentil) | Volatilidad implícita 1 m (percentil) | Risk reversal 25 d | Lectura | Referencia |
|---|---|---|---|---|---|
| {{DIVISA_O_PAR}} | {{NETO_CFTC}} ({{PCT_CFTC}}) | {{IV_1M}} ({{PCT_IV}}) | {{RR_25D}} | {{LECTURA}} | `{{CLM_O_CALC}}` |

**Exposición agregada por divisa del conjunto de opciones** (14.1; comprobada por HT-09 frente a las composiciones):

<!-- REPETIR (fila con marcadores de la tabla siguiente): FILA_EXPOSICION por divisa con exposición distinta de neutra -->
| Divisa | Exposición agregada | Opciones que la generan | Comentario |
|---|---|---|---|
| {{DIVISA}} | {{EXPOSICION}} (larga · corta · moderada · fuerte · neutra) | {{OPP_IDS}} | {{COMENTARIO_EXPOSICION}} |

**Contradicciones entre segmentos** (9.6.6): {{CONTRADICCIONES}} (misma divisa como pata activa de la tesis —la que se pronostica— larga en un segmento y corta en otro, con su `justificacion_contradiccion` por mecanismos u horizontes distintos, o resolución; el USD o el EUR como contrapartida o financiación no cuentan; o «ninguna»; G3-FX-08).

**Termómetro de la divisa base ({{DIVISA_BASE_USUARIO}})**: {{LECTURA_DIVISA_BASE}} (qué significan las opciones para quien ahorra en esa divisa; es la frase del informe visual).

**Factores dominantes**: {{FACTORES_DOMINANTES}}.

---

## 4. Análisis por segmento de divisas

> Instrucción: una subsección por segmento activo en F10 (hasta seis), en este orden: G10N G10 núcleo (USD, EUR, JPY, GBP, CHF), G10M G10 de materias primas y escandinavas (AUD, NZD, CAD, NOK, SEK), EMAS Emergentes de Asia, EMLA Emergentes de Latinoamérica, EMEA Emergentes de Europa, Oriente Medio y África, ESTR Estrategias y cestas cambiarias. Los segmentos sin opciones conservan 4.x.1, 4.x.2 y 4.x.4.

<!-- REPETIR: SECCION_SEGMENTO -->
### 4.{{N}} {{NOMBRE_SEGMENTO}} ({{SEGMENTO}}) — semáforo {{SEMAFORO}}

#### 4.{{N}}.1 Régimen del segmento

{{REGIMEN_SEGMENTO}} *(confianza: {{CONFIANZA_REGIMEN}}; `{{CLM_REGIMEN}}`)*

#### 4.{{N}}.2 Embudo de cribado (seis lentes cambiarias: política monetaria, carry, valor, momentum, flujos y posicionamiento, riesgo y régimen)

| Etapa | Número | Comentario |
|---|---|---|
| Candidatas cribadas (F1) | {{CRIBADAS}} | incluye rotación exploratoria: {{ROTACION}} |
| Pasan GC1 (señal compuesta ≥ 0,75 y dos familias de lentes concordantes) | {{PASAN_GC1}} | {{GC1_COMENTARIO}} |
| Pasan GC2 (tesis, E provisional ≥ 50) | {{PASAN_GC2}} | {{GC2_COMENTARIO}} |
| Finalistas GC3 | {{FINALISTAS}} | refutadas por CT-13: {{REFUTADAS}} |
| Elegibles (9.2, PS1–PS8) | {{ELEGIBLES}} | {{ELEGIBLES_COMENTARIO}} |
| En el top-3 (diversidad 9.6.3: ≤ 2 por clúster y ≤ 2 con la misma divisa en la misma dirección) | {{N_OPCIONES}} | {{MENOS_DE_TRES_MOTIVO}} |

#### 4.{{N}}.3 Opciones propuestas

<!-- REPETIR: FICHA_OPCION (ficha completa 9.6.7) -->
##### {{RANGO}}. {{NOMBRE}} · `{{OPP_ID}}`

| Campo | Valor |
|---|---|
| Tipo de opción | {{TIPO_OPCION}} (PAR · CRUCE · CESTA · BLOQUE · ESTRATEGIA · VOLATILIDAD · REGIMEN) |
| Segmento | {{SEGMENTO}} |
| Par (BASE/COTIZADA) | {{PAR}} (o «—» en cestas y estrategias) |
| Dirección | **{{DIRECCION}}** (opciones con par) · vista de volatilidad {{VISTA_VOLATILIDAD}} (ALZA/BAJA y plazo, solo VOLATILIDAD) — {{SUBE_BAJA_LLANO}} |
| Composición (divisa · peso · lado) | {{COMPOSICION}} (en cestas, bloques y estrategias es la dirección) |
| Divisa de financiación | {{DIVISA_FINANCIACION}} |
| Régimen cambiario de la divisa (si es REGIMEN) | {{REGIMEN_CAMBIARIO_DIVISA}} |
| Ámbito: incluye | {{AMBITO_INCLUYE}} |
| Ámbito: excluye | {{AMBITO_EXCLUYE}} |
| Indicador de seguimiento | {{INDICADOR_NOMBRE}} (`{{INDICADOR_SIMBOLO}}`, {{INDICADOR_FUENTE}}) |
| Convertibilidad e invertibilidad (PS3) | convertible: {{CONVERTIBLE}} · NDF: {{NDF}} · controles de capitales: {{CONTROLES}} · profundidad: {{PROFUNDIDAD}} — {{CONVERTIBILIDAD_NOTA}} |
| Carry | {{CARRY_ANUAL_PCT}} % anual, **{{CARRY_SIGNO}}** de la tesis · diferencial base − cotizada {{DIFERENCIAL_TIPOS}} % · ajustado por volatilidad: {{CARRY_AJUSTADO_VOL}} (`{{CARRY_CALC}}`, CALC-FX-) |
| Nombre llano (informe del usuario) | {{NOMBRE_LLANO}} |
| Tendencias vinculadas | {{TND_IDS}} (`TND-FX-`; o «táctica, T = NA») |
| Clúster de exposición | {{CLUSTER_ID}} — {{FACTOR_DOMINANTE}} |
| Confianza global | {{CONFIANZA}} |
| Relevancia decisional · reversibilidad | {{RELEVANCIA_DECISIONAL}} · {{REVERSIBILIDAD}} |
| Liquidez del par o de la cesta | {{LIQUIDEZ}} |
| Siguiente paso sugerido | **{{SIGUIENTE_PASO}}** |

**Tesis.** {{TESIS}} *(`{{CLM_TESIS}}`)*

**Mecanismo causal.** {{MECANISMO}}

**Valoración: qué descuentan ya el forward, la curva y el posicionamiento.** {{VALORACION}} (PPA, BEER/FEER, REER frente a su media, forward frente al contado) *(`{{CALC_VALORACION}}`)*

**Puntuaciones (HT-03, `{{DESGLOSE_REF}}`).**

| T | E | M | A | RK | Dimensiones decisivas de A (asimetría · valoración · carry · catalizadores · momento y posicionamiento · convertibilidad) |
|---|---|---|---|---|---|
| {{T}} | {{E}} | {{M}} | {{A}} | {{RK}} | {{DIMENSIONES_DECISIVAS}} |

> Instrucción: si alguna puntuación quedó en banda marginal, indicar «segunda pasada aplicada: se usa el menor valor». Si se aplicó el tope por saturación narrativa (posicionamiento en el decil extremo a favor de la tesis y forward que ya descuenta la senda esperada), indicarlo.

**Naturaleza de la inversión y horizonte principal (8.3).** {{NATURALEZA_INVERSION}} · horizonte principal **{{HORIZONTE_PRINCIPAL}}** {{JUSTIFICACION_HORIZONTE_SI_HAY}} {{AMBITO_H5_SI_HAY}}

**Horizontes y pronósticos congelados (F4).**

<!-- REPETIR (fila con marcadores de la tabla siguiente): FILA_HORIZONTE -->
| Horizonte | Vista sobre el indicador | Tipo de rentabilidad · divisa de medición | Banda / probabilidad | Certificado R13 | Referencia ingenua | `PRG-FX-` | Fecha y criterio de resolución |
|---|---|---|---|---|---|---|---|
| {{H}} | {{VISTA}} | {{TIPO_RENTABILIDAD}} (PRECIO_CONTADO · RENTABILIDAD_TOTAL) · {{DIVISA_MEDICION}} | {{BANDA_O_PROB}} | {{CERTIFICADO}} | {{REFERENCIA_INGENUA}} (paseo aleatorio · forward) | `{{PRG_ID}}` | {{FECHA_RESOLUCION}} — {{CRITERIO}} |

> Instrucción: en H1 añadir «previsión a días: la de menor fiabilidad esperada»; en los horizontes «limitados» (H1 y H4 de los emergentes) indicar el catalizador y la liquidez que los justifican. Marcar el horizonte principal. En **H5** (solo naturaleza ESTRUCTURAL; equilibrio a muy largo plazo, regímenes o sistema monetario internacional) la columna de banda lleva solo la banda verbal (nunca probabilidad) y, debajo de la tabla, la línea «**Hitos H5**: `{{HIT_ID}}` {{FECHA}} — {{INDICADOR}}: {{CRITERIO}}» por cada hito (≥ 3), con su estado si ya se ha resuelto.

**Catalizadores.** {{CATALIZADORES}} (reuniones de bancos centrales, datos, elecciones, revisiones de índices de bonos · fecha)

**Riesgos principales.** {{RIESGOS}} — riesgo sintético **{{RIESGO_1A5}}/5** (RISK-DD-001; un tipo fijo con riesgo de ruptura o una divisa con controles parte de 4).

**Condiciones de invalidación.** {{INVALIDACION}} (pueden incluir niveles del par; nunca son niveles de entrada)

**Qué cambiaría la conclusión.** {{QUE_CAMBIARIA}}

**Lo que no sabemos.** {{LO_QUE_NO_SABEMOS}}

**Encargo para el Bloque B** (`paquete_para_bloque_B`).

| Campo | Contenido |
|---|---|
| Ámbito, composición y dirección | {{PAR_O_COMPOSICION}} · {{DIRECCION}} · financiación {{DIVISA_FINANCIACION}} |
| Carry esperado | {{CARRY_ESPERADO}} |
| Consideraciones de implementación (información, no recomendación de instrumento) | {{CONSIDERACIONES_IMPLEMENTACION}} (liquidez del par, NDF, riesgo de evento, horario de liquidez) |
| Métricas clave que vigilar | {{METRICAS_CLAVE}} |
| Preguntas para el Bloque B | {{PREGUNTAS_PARA_B}} |
| Niveles de referencia del indicador | {{NIVELES_REFERENCIA}} (fuente, hora y zona de la fijación; solo referencia e invalidación; G3-FX-07) |

> Instrucción: las consideraciones y las preguntas orientan al Bloque B sin elegir instrumento, proveedor, coste, apalancamiento, tamaño ni nivel de entrada.

**Objeciones (CT-13) y respuesta.** Ver sección 6 (`{{OPP_ID}}`).

**Evidencia y cálculos.** {{EVIDENCIAS}} · {{CALCULOS}}
<!-- FIN REPETIR (FICHA_OPCION) -->

#### 4.{{N}}.4 Alternativas descartadas relevantes

<!-- REPETIR (fila con marcadores de la tabla siguiente): FILA_DESCARTE (máx. 5, las más cercanas al umbral) -->
| Candidata (par o cesta · dirección) | Puerta en la que quedó | Motivo | Qué tendría que ocurrir |
|---|---|---|---|
| {{NOMBRE_DESCARTE}} | {{PUERTA}} | {{MOTIVO}} | {{CONDICION_ENTRADA}} |

#### 4.{{N}}.5 Cambios frente al ciclo anterior

{{CAMBIOS_SEGMENTO}} (entradas, salidas con su motivo, cambios de RK ≥ 15 puntos con su justificación).
<!-- FIN REPETIR (SECCION_SEGMENTO) -->

---

## 5. Seguimiento de opciones vigentes y pronósticos abiertos

<!-- REPETIR (fila con marcadores de la tabla siguiente): FILA_VIGENTE -->
| `OPP-FX-` | Nombre | Estado | Decisión del Broker | Comentario (invalidación, nivel del par, catalizador) |
|---|---|---|---|---|
| `{{OPP_ID}}` | {{NOMBRE}} | {{ESTADO}} | {{DECISION_BROKER}} | {{COMENTARIO}} |

<!-- REPETIR (fila con marcadores de la tabla siguiente): FILA_PRONOSTICO_ABIERTO (los que vencen en las próximas 4 semanas) -->
| `PRG-FX-` | Opción | Horizonte | Vence | Situación provisional (sin resolver) |
|---|---|---|---|---|
| `{{PRG_ID}}` | `{{OPP_ID}}` | {{H}} | {{FECHA_RESOLUCION}} | {{SITUACION}} |

> Instrucción: la situación provisional no es una resolución (la resuelve el Evaluador en su fecha); se redacta como «a fecha de hoy, el par está por encima/debajo del nivel de emisión».

---

## 6. Objeciones y respuestas

<!-- REPETIR (fila con marcadores de la tabla siguiente): FILA_OBJECION (todas las fuertes y moderadas; débiles solo si cambian algo) -->
| `OPP-FX-` | Fuerza | Objeción | Respuesta con evidencia | Estado |
|---|---|---|---|---|
| `{{OPP_ID}}` | {{FUERZA}} | {{RESUMEN}} | {{RESPUESTA}} | {{ESTADO_OBJECION}} |

**Veredictos globales del Analista de hipótesis contrarias**: {{VEREDICTOS}} (tesis robusta · tesis frágil · tesis refutada). Puntos revisados en particular: lo que ya descuentan el forward y el posicionamiento, el riesgo de intervención y la fragilidad del carry.

---

## 7. Limitaciones, lagunas y qué no sabemos

> Instrucción: lista honesta, priorizada por impacto en la decisión. Incluir: **supuestos declarados** por consultas CT-23 sin respuesta (supuesto, `CNS-FX-` y efecto si fuera falso; 6.2.9), segmentos pausados por una consulta bloqueante, servicios degradados por credenciales ausentes o denegadas (CT-25, sin valores), celdas segmento × horizonte sin certificado R13, datos desactualizados (PS2), fuentes retiradas, reducciones de alcance, degradaciones de herramientas, dependencia de una sola raíz, divisas con convertibilidad limitada.

<!-- REPETIR: LIMITACION -->
- {{LIMITACION}} — efecto: {{EFECTO}}.
<!-- FIN REPETIR -->

---

## 8. Historial de aciertos (Evaluador)

Ventana: **{{HIST_VENTANA}}**. Referencia: **paseo aleatorio** (sin cambio; Meese y Rogoff, 1983) y, cuando procede, **forward como predictor** (8.4). En divisas, batir al paseo aleatorio es difícil: un acierto cercano al 50 % con muestra pequeña no demuestra ventaja.

<!-- REPETIR (fila con marcadores de la tabla siguiente): FILA_HISTORIAL -->
| Segmento | Horizonte | Evaluadas (n) | Aciertos | Tasa | Paseo aleatorio | Forward | ¿Significativo? |
|---|---|---|---|---|---|---|---|
| {{SEGMENTO}} | {{H}} | {{N}} | {{ACIERTOS}} | {{TASA}} | {{TASA_AZAR}} | {{TASA_FORWARD}} | {{SIGNIFICATIVO}} |
| **Global** | — | **{{N_GLOBAL}}** | **{{ACIERTOS_GLOBAL}}** | **{{TASA_GLOBAL}}** | {{TASA_AZAR}} | {{TASA_FORWARD_GLOBAL}} | {{SIGNIFICATIVO_GLOBAL}} |

**Calibración**: {{CALIBRACION}} (Brier y BSS frente al paseo aleatorio, ECE cuando haya muestra; si no, «muestra insuficiente: n < 30 por celda»). **Lecciones aplicadas en este RUN**: {{LEC_IDS}}.

---

## 9. Anexos

### 9.1 Evidencia citada

<!-- REPETIR (fila con marcadores de la tabla siguiente): FILA_CLM -->
| `CLM-FX-` | Afirmación (resumen) | Raíces independientes | `EVD-FX-` | Confianza |
|---|---|---|---|---|
| `{{CLM_ID}}` | {{AFIRMACION}} | {{N_RAICES}} | {{EVD_IDS}} | {{CONFIANZA}} |

### 9.2 Cálculos (Registro de cálculos del Motor)

<!-- REPETIR (fila con marcadores de la tabla siguiente): FILA_CALC -->
| `CALC-FX-` | Método / perfil | Resultado usado | Clase de cifra | Referencia ingenua |
|---|---|---|---|---|
| `{{CALC_ID}}` | {{METODO}} · {{PERFIL}} (PERF-FX-G10 · PERF-FX-EM · PERF-FX-FACT) | {{RESULTADO}} | {{CLASE_CIFRA}} | {{REFERENCIA_INGENUA}} |

### 9.3 Metodología y versión

- Versión de metodología: {{METHODOLOGY_VERSION}}; parámetros vigentes en F10 a {{FECHA}} (umbrales E/A/T, pesos de RK: {{PESOS_RK}}; pesos de A FX: asimetría 30 · valoración 20 · carry 15 · catalizadores 15 · momento y posicionamiento 10 · convertibilidad 10, o los recalibrados: {{PESOS_A}}).
- Ajustes de calibración vigentes desde el último informe: {{AJUSTES_F6}}.
- Métricas de legibilidad del informe visual (HT-07): Fernández-Huerta corregido {{FH}}; frases > 20 palabras: {{FRASES_LARGAS}}; jerga sin explicar: {{JERGA}}.

---

*Este informe es información general del mercado de divisas elaborada por el Bloque A Forex para el Broker Personal. No constituye asesoramiento personalizado ni una recomendación de compra o venta: el Bloque A Forex no conoce la cartera, el perfil ni los objetivos del usuario. Los tipos de cambio son difíciles de predecir y las rentabilidades pasadas no garantizan rentabilidades futuras. El Bloque A Forex identifica oportunidades cambiarias (pares, cruces, cestas, estrategias y regímenes); no elige el instrumento, el proveedor, el coste, el apalancamiento, el tamaño ni el nivel de entrada: eso corresponde al Bloque B. La decisión, incluida la de enviar el encargo al Bloque B, corresponde al Broker Personal.*
