# Plantilla — Informe técnico para el Broker

**Bloque A · Robot Investor · Versión óptima V5.0 · 02/11/2026 · actualizado V5.1 (03/11/2026)** · Subordinado al Documento 0 óptima V5.1. Cambios V5.1: naturaleza de la inversión y horizonte principal en cada ficha; H5 (décadas) con hitos HIT-; supuestos declarados por consultas al Broker sin respuesta (CT-23).

> **Uso.** Plantilla del entregable 14.1 del Documento 0. La rellena **AG-17 Redactor y Diseñador de Informes** a partir del paquete de síntesis (CT-15) y la publica **AG-01 Coordinador** por CT-02. Los marcadores `{{…}}` se sustituyen por valores del paquete; los bloques entre `<!-- REPETIR: … -->` y `<!-- FIN REPETIR -->` se repiten por elemento y se eliminan si no hay ninguno; un comentario `<!-- REPETIR (fila con marcadores de la tabla siguiente): … -->` indica que la fila con marcadores de esa tabla se repite tantas veces como elementos haya (los comentarios se colocan fuera de las tablas para no romper su formato). Las líneas que empiezan por `> Instrucción:` se borran del entregable final.
>
> **Reglas que rigen todo el informe.**
> 1. **Mismos números en los tres entregables**: toda cifra, puntuación, estado, banda o identificador de este informe es idéntica a la del paquete JSON (`Paquetes JSON/`) y a la del informe visual del mismo `run_id`. El JSON es la fuente de verdad; ante discrepancia se corrige el origen y se regeneran los tres.
> 2. **Trazabilidad (R7)**: cada afirmación material lleva su `CLM-`; cada cifra, su `CALC-` o su dato HT-01 con fecha. No se calcula nada al redactar.
> 3. **Vocabulario de confianza** en cada conclusión: *establecido · probable · especulativo · en disputa*.
> 4. **R13**: sin certificado del Evaluador, ningún horizonte lleva probabilidad numérica; en **H5** (décadas) nunca, y el pronóstico se presenta con sus hitos intermedios HIT-; se usa la banda («más probable que no», «incierto», «poco probable») y la etiqueta «sin ventaja demostrada todavía».
> 5. **R14**: si un tipo de activo tiene menos de tres opciones, se explica; nunca se rellena.
> 5 bis. **Frontera con el Bloque B (R21)**: el informe habla de **ámbitos** (mercado, región, sector, subsector, temática, segmento, factor o estrategia) en los doce tipos de activo, nunca de activos concretos. No se seleccionan ni comparan valores, emisiones, fondos, contratos o tokens, ni sus costes o plataformas: eso lo hace el Bloque B con el encargo de cada opción. Los nombres concretos solo aparecen como «Ejemplos ilustrativos del ámbito (no son propuestas)».
> 6. Registro formal, conciso, sin adornos. Tablas para lo comparable; prosa breve para el razonamiento.
> 7. Nombre del archivo: `Informes técnicos Broker/{{FECHA}}_informe-tecnico_{{RUN_ID}}.md` (y `.pdf` con el mismo nombre base).

---

# Informe técnico del Bloque A — {{TITULO_RUN}}

| Campo | Valor |
|---|---|
| Identificador | `{{RUN_ID}}` |
| Tipo | {{TIPO}} (PERIODICO · AD_HOC · PROFUNDIZACION) |
| Fecha de referencia | {{FECHA}} |
| Datos de mercado al cierre de | {{FECHA_DATOS_MERCADO}} |
| Disparador | {{DISPARADOR}} (ciclo C1 programado · CT-01 de {{FECHA_PETICION}}) |
| Versión de metodología | {{METHODOLOGY_VERSION}} |
| Dictamen G3 | {{ESTADO_G3}} {{ADVERTENCIAS_G3}} |
| Estado del retorno | {{ESTADO}} (COMPLETO · PARCIAL) |
| Entregables hermanos | `{{RUTA_INFORME_VISUAL}}` · `{{RUTA_PAQUETE_JSON}}` |

---

## 1. Resumen ejecutivo

> Instrucción: máximo 250 palabras más la tabla. Responde a: qué ha cambiado, qué proponemos, cuántas apuestas independientes hay y qué decisión se le facilita al Broker. Empieza por lo más relevante para decidir, no por el contexto.

**Qué ha cambiado desde `{{RUN_ANTERIOR}}`.** {{CAMBIOS_VS_ANTERIOR}}

**Lectura del conjunto.** {{LECTURA_CONJUNTO}}

**Apuestas independientes: {{APUESTAS_INDEPENDIENTES}}.** {{DESCRIPCION_CLUSTERES}}

<!-- REPETIR (fila con marcadores de la tabla siguiente): FILA_RESUMEN por cada opción (y una fila «—» por cada tipo de activo sin opciones) -->
| Tipo de activo | Semáforo | Opciones (rango · nombre · `OPP-`) | RK | Riesgo 1–5 | Relevancia | Siguiente paso |
|---|---|---|---|---|---|---|
| {{CLASE}} | {{SEMAFORO}} | {{RANGO}} · {{NOMBRE}} · `{{OPP_ID}}` | {{RK}} | {{RIESGO_1A5}} | {{RELEVANCIA_DECISIONAL}} | {{SIGUIENTE_PASO}} |

**Encargos para el Bloque B**: {{N_ENCARGOS_B}} (uno por opción del top-3, en `paquete_para_bloque_B` del JSON; el Broker decide si los reenvía).

**Alertas** (si las hay): {{ALERTAS}} — p. ej., condición de invalidación cercana en una opción vigente, objeción moderada sin resolver, dato desactualizado.

---

## 2. Alcance, nivel, presupuesto y consumo

> Instrucción: datos de F5 y del paquete. Declarar toda reducción de alcance (R16).

<!-- REPETIR (fila con marcadores de la tabla siguiente): FILA_ALCANCE por tipo de activo activo -->
| Tipo de activo | Nivel | GC0 (delta material) | Motivo GC0 | Presupuesto (UC) | Consumo (UC) | Desviación |
|---|---|---|---|---|---|---|
| {{CLASE}} | {{NIVEL}} | {{GC0_SI_NO}} | {{GC0_MOTIVO}} | {{PRESUPUESTO_UC}} | {{CONSUMO_UC}} | {{DESVIACION_PCT}} |
| **Total** | — | — | — | **{{PRESUPUESTO_TOTAL}}** | **{{CONSUMO_TOTAL}}** | {{DESVIACION_TOTAL}} |

- **Alcance pedido**: {{ALCANCE}} (tipos de activo, regiones, temáticas, activos citados —analizados a nivel de su ámbito—, pregunta).
- **Horizontes de interés**: {{HORIZONTES}}.
- **Reducciones de alcance declaradas**: {{REDUCCIONES}} (o «ninguna»).
- **Modos degradados**: {{DEGRADACIONES}} (herramienta, credencial o fuente no disponible; efecto sobre las conclusiones).

---

## 3. Régimen macro y de mercado

> Instrucción: 150–300 palabras. Diagnóstico común que condiciona varias clases. Cada afirmación con `CLM-` y nivel de confianza. Cerrar con los dos o tres factores macro de los que dependen más opciones (enlaza con los clústeres).

{{REGIMEN_MACRO}}

<!-- REPETIR (fila con marcadores de la tabla siguiente): FILA_MACRO (máx. 8) -->
| Variable | Último dato | Fecha | Lectura | Referencia |
|---|---|---|---|---|
| {{VARIABLE}} | {{VALOR}} | {{FECHA_DATO}} | {{LECTURA}} | `{{CLM_O_CALC}}` |

**Factores dominantes**: {{FACTORES_DOMINANTES}}.

---

## 4. Análisis por tipo de activo

> Instrucción: una subsección por tipo de activo activo en F10 (hasta doce), en este orden: RV Renta variable, RF Renta fija, DIV Divisas, MP Materias primas, IDX Índices bursátiles, FON Fondos y vehículos de inversión colectiva, DER Derivados financieros, INM Activos inmobiliarios cotizados, CRI Criptoactivos y activos digitales, ALT Capital privado y activos alternativos, MON Instrumentos monetarios y liquidez, TCV Tipos de interés, crédito y volatilidad. Los tipos sin opciones conservan 4.x.1, 4.x.2 y 4.x.4.

<!-- REPETIR: SECCION_CLASE -->
### 4.{{N}} {{NOMBRE_CLASE}} ({{CLASE}}) — semáforo {{SEMAFORO}}

#### 4.{{N}}.1 Régimen del tipo de activo

{{REGIMEN_CLASE}} *(confianza: {{CONFIANZA_REGIMEN}}; `{{CLM_REGIMEN}}`)*

#### 4.{{N}}.2 Embudo de cribado

| Etapa | Número | Comentario |
|---|---|---|
| Candidatas cribadas (F1) | {{CRIBADAS}} | incluye rotación exploratoria: {{ROTACION}} |
| Pasan GC1 (señal) | {{PASAN_GC1}} | {{GC1_COMENTARIO}} |
| Pasan GC2 (tesis) | {{PASAN_GC2}} | {{GC2_COMENTARIO}} |
| Finalistas GC3 | {{FINALISTAS}} | refutadas por CT-13: {{REFUTADAS}} |
| Elegibles (9.2, PS1–PS8) | {{ELEGIBLES}} | {{ELEGIBLES_COMENTARIO}} |
| En el top-3 | {{N_OPCIONES}} | {{MENOS_DE_TRES_MOTIVO}} |

#### 4.{{N}}.3 Opciones propuestas

<!-- REPETIR: FICHA_OPCION (ficha completa 9.6.7) -->
##### {{RANGO}}. {{NOMBRE}} · `{{OPP_ID}}`

| Campo | Valor |
|---|---|
| Tipo de opción | {{TIPO_OPCION}} (MERCADO · SECTOR · SUBSECTOR · TEMATICA · SEGMENTO · FACTOR/ESTILO · ESTRATEGIA) |
| Tipo de activo · subtipo | {{TIPO_ACTIVO}} · {{SUBTIPO}} {{TIPOS_SECUNDARIOS}} |
| Ámbito: incluye | {{AMBITO_INCLUYE}} |
| Ámbito: excluye | {{AMBITO_EXCLUYE}} |
| Ámbito: región | {{AMBITO_REGION}} |
| Indicador de seguimiento | {{INDICADOR_NOMBRE}} (`{{INDICADOR_SIMBOLO}}`, HT-01) |
| Invertibilidad del ámbito (PS3) | {{UNIVERSO_SUFICIENTE}} — {{INVERTIBILIDAD_NOTA}} |
| Nombre llano (informe del usuario) | {{NOMBRE_LLANO}} |
| Tendencias vinculadas | {{TND_IDS}} (o «táctica, T = NA») |
| Regiones | {{REGIONES}} |
| Clúster de exposición | {{CLUSTER_ID}} — {{FACTOR_DOMINANTE}} |
| Confianza global | {{CONFIANZA}} |
| Relevancia decisional · reversibilidad | {{RELEVANCIA_DECISIONAL}} · {{REVERSIBILIDAD}} |
| Liquidez del ámbito | {{LIQUIDEZ}} |
| Naturaleza de la inversión · horizonte principal | {{NATURALEZA_INVERSION}} · **{{HORIZONTE_PRINCIPAL}}** {{JUSTIFICACION_HORIZONTE}} (8.3: TACTICA H1–H2 · LIQUIDEZ H1–H3 · CICLICA y PRIMA_RIESGO H2–H4 · VALORACION H3–H4 · ESTRUCTURAL H4–H5) |
| Siguiente paso sugerido | **{{SIGUIENTE_PASO}}** |

**Tesis.** {{TESIS}} *(`{{CLM_TESIS}}`)*

**Mecanismo causal.** {{MECANISMO}}

**Valoración del ámbito: qué descuentan ya los precios.** {{VALORACION}} *(`{{CALC_VALORACION}}`)*

**Puntuaciones (HT-03, `{{DESGLOSE_REF}}`).**

| T | E | M | A | RK | Dimensiones decisivas |
|---|---|---|---|---|---|
| {{T}} | {{E}} | {{M}} | {{A}} | {{RK}} | {{DIMENSIONES_DECISIVAS}} |

> Instrucción: si alguna puntuación quedó en banda marginal, indicar «segunda pasada aplicada: se usa el menor valor». Si se aplicó el tope por saturación narrativa, indicarlo.

**Horizontes y pronósticos congelados (F4).**

<!-- REPETIR (fila con marcadores de la tabla siguiente): FILA_HORIZONTE -->
| Horizonte | Vista | Banda / probabilidad | Certificado R13 | `PRG-` | Fecha y criterio de resolución |
|---|---|---|---|---|---|
| {{H}} | {{VISTA}} | {{BANDA_O_PROB}} | {{CERTIFICADO}} | `{{PRG_ID}}` | {{FECHA_RESOLUCION}} — {{CRITERIO}} |

<!-- REPETIR solo si la opción tiene H5 (V5.1): HITOS_H5 -->
**Hitos intermedios del pronóstico H5 `{{PRG_ID_H5}}`** (probabilidad siempre cualitativa; se evalúa por sus hitos, 8.3 y 12.1). Tesis estructural: {{TESIS_ESTRUCTURAL}}

| `HIT-` | Fecha | Indicador | Criterio | Banda | Estado |
|---|---|---|---|---|---|
| `{{HIT_ID}}` | {{FECHA_HITO}} | {{INDICADOR_HITO}} | {{CRITERIO_HITO}} | {{BANDA_HITO}} | {{ESTADO_HITO}} |
<!-- FIN REPETIR -->

**Catalizadores.** {{CATALIZADORES}} (evento · fecha)

**Riesgos principales.** {{RIESGOS}} — riesgo sintético **{{RIESGO_1A5}}/5**.

**Condiciones de invalidación.** {{INVALIDACION}}

**Qué cambiaría la conclusión.** {{QUE_CAMBIARIA}}

**Lo que no sabemos.** {{LO_QUE_NO_SABEMOS}}

**Encargo para el Bloque B** (`paquete_para_bloque_B`).

| Campo | Contenido |
|---|---|
| Universo que debe analizar | {{AMBITO_INCLUYE}} — excluye: {{AMBITO_EXCLUYE}} — región: {{AMBITO_REGION}} |
| Criterios de selección sugeridos | {{CRITERIOS_SELECCION_SUGERIDOS}} |
| Métricas clave que vigilar | {{METRICAS_CLAVE}} |
| Preguntas para el Bloque B | {{PREGUNTAS_PARA_B}} |

> Instrucción: los criterios y las preguntas orientan al Bloque B sin nombrar ni ordenar activos concretos.

**Ejemplos ilustrativos del ámbito (no son propuestas).** {{EJEMPLOS_ILUSTRATIVOS}} (o «—»).

**Objeciones (CT-13) y respuesta.** Ver sección 6 (`{{OPP_ID}}`).

**Evidencia y cálculos.** {{EVIDENCIAS}} · {{CALCULOS}}
<!-- FIN REPETIR (FICHA_OPCION) -->

#### 4.{{N}}.4 Alternativas descartadas relevantes

<!-- REPETIR (fila con marcadores de la tabla siguiente): FILA_DESCARTE (máx. 5, las más cercanas al umbral) -->
| Candidata | Puerta en la que quedó | Motivo | Qué tendría que ocurrir |
|---|---|---|---|
| {{NOMBRE_DESCARTE}} | {{PUERTA}} | {{MOTIVO}} | {{CONDICION_ENTRADA}} |

#### 4.{{N}}.5 Cambios frente al ciclo anterior

{{CAMBIOS_TIPO}} (entradas, salidas con su motivo, cambios de RK ≥ 15 puntos con su justificación).
<!-- FIN REPETIR (SECCION_CLASE) -->

---

## 5. Seguimiento de opciones vigentes y pronósticos abiertos

<!-- REPETIR (fila con marcadores de la tabla siguiente): FILA_VIGENTE -->
| `OPP-` | Nombre | Estado | Decisión del Broker | Comentario (invalidación, precio, catalizador) |
|---|---|---|---|---|
| `{{OPP_ID}}` | {{NOMBRE}} | {{ESTADO}} | {{DECISION_BROKER}} | {{COMENTARIO}} |

<!-- REPETIR (fila con marcadores de la tabla siguiente): FILA_PRONOSTICO_ABIERTO (los que vencen en las próximas 4 semanas) -->
| `PRG-` | Opción | Horizonte | Vence | Situación provisional (sin resolver) |
|---|---|---|---|---|
| `{{PRG_ID}}` | `{{OPP_ID}}` | {{H}} | {{FECHA_RESOLUCION}} | {{SITUACION}} |

> Instrucción: la situación provisional no es una resolución (la resuelve el Evaluador en su fecha); se redacta como «a fecha de hoy, el indicador está por encima/debajo del umbral».

---

## 6. Objeciones y respuestas

<!-- REPETIR (fila con marcadores de la tabla siguiente): FILA_OBJECION (todas las fuertes y moderadas; débiles solo si cambian algo) -->
| `OPP-` | Fuerza | Objeción | Respuesta con evidencia | Estado |
|---|---|---|---|---|
| `{{OPP_ID}}` | {{FUERZA}} | {{RESUMEN}} | {{RESPUESTA}} | {{ESTADO_OBJECION}} |

**Veredictos globales del Analista de hipótesis contrarias**: {{VEREDICTOS}} (tesis robusta · tesis frágil · tesis refutada).

---

## 7. Limitaciones, lagunas y qué no sabemos

> Instrucción: lista honesta, priorizada por impacto en la decisión. Incluir (V5.1) los **supuestos declarados** de las consultas al Broker sin respuesta, con su `CNS-` y su efecto si fueran falsos, y los servicios degradados por falta de credencial (CT-25); y además: celdas sin certificado R13, datos desactualizados (PS2), fuentes retiradas, reducciones de alcance, degradaciones de herramientas, dependencia de una sola raíz.

<!-- REPETIR: LIMITACION -->
- {{LIMITACION}} — efecto: {{EFECTO}}.
<!-- FIN REPETIR -->

---

## 8. Historial de aciertos (Evaluador)

Ventana: **{{HIST_VENTANA}}**. Referencia: {{HIST_REFERENCIA}} (referencia de comparación de cada tipo de activo, 8.4 del Documento 0, y referencia ingenua).

<!-- REPETIR (fila con marcadores de la tabla siguiente): FILA_HISTORIAL -->
| Tipo de activo | Horizonte | Evaluadas (n) | Mejor que la referencia | Tasa | Tasa esperada por azar | ¿Significativo? |
|---|---|---|---|---|---|---|
| {{CLASE}} | {{H}} | {{N}} | {{ACIERTOS}} | {{TASA}} | {{TASA_AZAR}} | {{SIGNIFICATIVO}} |
| **Global** | — | **{{N_GLOBAL}}** | **{{ACIERTOS_GLOBAL}}** | **{{TASA_GLOBAL}}** | {{TASA_AZAR}} | {{SIGNIFICATIVO_GLOBAL}} |

**Calibración**: {{CALIBRACION}} (Brier, ECE cuando haya muestra; si no, «muestra insuficiente: n < 30 por celda»). **Lecciones aplicadas en este RUN**: {{LEC_IDS}}.

---

## 9. Anexos

### 9.1 Evidencia citada

<!-- REPETIR (fila con marcadores de la tabla siguiente): FILA_CLM -->
| `CLM-` | Afirmación (resumen) | Raíces independientes | `EVD-` | Confianza |
|---|---|---|---|---|
| `{{CLM_ID}}` | {{AFIRMACION}} | {{N_RAICES}} | {{EVD_IDS}} | {{CONFIANZA}} |

### 9.2 Cálculos (Registro de cálculos del Motor)

<!-- REPETIR (fila con marcadores de la tabla siguiente): FILA_CALC -->
| `CALC-` | Método / perfil | Resultado usado | Clase de cifra | Referencia ingenua |
|---|---|---|---|---|
| `{{CALC_ID}}` | {{METODO}} · {{PERFIL}} | {{RESULTADO}} | {{CLASE_CIFRA}} | {{REFERENCIA_INGENUA}} |

### 9.3 Metodología y versión

- Versión de metodología: {{METHODOLOGY_VERSION}}; parámetros vigentes en F10 a {{FECHA}} (umbrales E/A/T, pesos de RK: {{PESOS_RK}}).
- Ajustes de calibración vigentes desde el último informe: {{AJUSTES_F6}}.
- Métricas de legibilidad del informe visual (HT-07): Fernández-Huerta {{FH}}; frases > 20 palabras: {{FRASES_LARGAS}}; jerga sin explicar: {{JERGA}}.

---

*Este informe es información general de mercado elaborada por el Bloque A para el Broker Personal. No constituye asesoramiento personalizado ni una recomendación de compra o venta: el Bloque A no conoce la cartera, el perfil ni los objetivos del usuario. Las rentabilidades pasadas no garantizan rentabilidades futuras. El Bloque A identifica oportunidades (ámbitos de inversión), no selecciona activos concretos: localizar los mejores activos dentro de cada ámbito corresponde al Bloque B. La decisión, incluida la de enviar el encargo al Bloque B, corresponde al Broker Personal.*
