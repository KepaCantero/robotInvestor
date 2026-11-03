# Catálogo de cálculos del Motor de Cálculo Avanzado de Mercados (AG-B16)

**Bloque B · Robot Investor · Versión V2.0 · 03/11/2026 · actualizado V2.1 (03/11/2026)** · Subordinado al Documento 0 del Bloque B, óptima V2.1.

Archivo **CC** (propietario: operador, por cambio de tipo 3; el Motor propone). Lectores: AG-B16 y sus módulos MC-B01…MC-B10, AG-B19 (Documentador para el Motor), AG-B12 (Seleccionador), AG-B13 (Prospectiva), AG-B21 (Orquestador técnico). `catalog_version` 2.1 (V2.1: seis fichas nuevas —`VC-DESG-001` desglose jerárquico y AE, `VC-BOT-001` indicadores de cuello y PCB, `EMG-PEM-001` potencial de emergentes, `DIF-H5-001` proyección estructural H5, `FC-HITO-001` evaluación por hitos y `EVL-PV-001` evaluación de puertas de viabilidad y de seguimientos encargados—, horizonte H5 y referencia ingenua RI-LIN; detalle en la sección 17). Acompañan a este catálogo los «Perfiles de estrategia y de selección del Motor» y el «Mapa de conocimientos del Motor» (V2.0), con los que comparte códigos y numeración de áreas.

---

## 1. Propósito y reglas de uso

1.1. El catálogo especifica, operación a operación, **qué calcula el Motor del Bloque B, para qué, con qué entradas mínimas, con qué método, con qué salidas, bajo qué supuestos, cómo se valida y con qué respaldo bibliográfico de F8 (TMB-01…TMB-14)**. Cada servicio CT-B-13 cita en `metodo` un `ficha_id` y su versión; cada re-ejecución CT-B-14 usa la ficha y la versión del artefacto original.

1.2. **Cobertura no es obligación** (R22). El catálogo define lo que el Motor sabe tratar; los métodos se activan cuando pueden cambiar A, E, C, S, el top-N, una puerta o un horizonte (10.4 del Documento 0). Ninguna petición ejecuta todo el catálogo; los perfiles PERF-B- y SEL- fijan los métodos por defecto de cada plan.

1.3. **Estados.** Cada ficha tiene un estado de gobierno (`VIGENTE`, `EN_REVISION`, `DEPRECADA`, `BORRADOR`) y un estado de madurez (R26):

| Madurez | Significado | Uso permitido |
|---|---|---|
| DOCUMENTADO | Especificación publicada; sin implementación verificada en el ejecutor del Bloque B (`11_Ejecutor`) | El Motor no entrega cifras citables con ella: responde `METODO_NO_IMPLEMENTADO` y ofrece, si existe, la alternativa implementada más próxima con la limitación declarada |
| IMPLEMENTADO (heredado) | Ficha conservada del Catálogo V5.0 del Bloque A, implementada en su ejecutor; pendiente de reverificación con los casos de control de esta ficha en el ejecutor del Bloque B | Servicio con la limitación «implementación heredada no reverificada» |
| IMPLEMENTADO | Implementada en el ejecutor del Bloque B con sus casos de control superados y registrados en RC | Servicio normal; la entrega declara «implementado, no validado» |
| VALIDADO | Batería de `09_Pruebas` ejecutada con evidencia (incluido, para las fichas de selección y evaluación, un backtesting de rankings con datos reales sin sesgos) | Servicio sin advertencia de madurez |

**Estado de partida (V2.0):** 106 fichas; **22 IMPLEMENTADO (heredado)** del ejecutor del Bloque A V5.0 y **84 DOCUMENTADO**. **V2.1:** 112 fichas; las seis nuevas, **DOCUMENTADO** (90 en total). Ninguna está IMPLEMENTADA en el ejecutor del Bloque B ni VALIDADA (18.4 del Documento 0). El orden de implantación recomendado está en la sección 16 y en el Mapa (sección 7).

1.4. **Fichas conservadas del Bloque A.** Las fichas transversales útiles del Catálogo V5.0 del Bloque A se conservan **con el mismo `ficha_id`** para preservar la trazabilidad de su implementación; su contenido se adapta al Bloque B (perfiles PERF-B y SEL, clases de cifra del Documento 0 del Bloque B, respaldo en TMB-). Se retira de ellas la restricción del Bloque A que impedía ordenar instrumentos concretos: en el Bloque B ordenar candidatos es una función central.

1.5. **Frontera con los Bloques C.x (R7).** Ninguna ficha produce precios objetivo ni valoraciones individuales completas. Toda valoración de un candidato sale con `uso: para_ordenacion`, con banda de sensibilidad y con supuestos comunes a todo su universo. Una petición de precio objetivo, tamaño de posición o idoneidad para un inversor se rechaza (`PRECIO_OBJETIVO_FUERA_DE_ROL`).

1.6. **HT-03 es canónica.** Las fichas SCR-S-001 y SCR-AEC-001 replican exactamente la aritmética de HT-03 para estimar la incertidumbre de S y reconstruir A, E y C; cualquier diferencia con HT-03 es `DISCREPANCIA_HT03` y bloquea la cifra hasta su resolución.

1.7. **Cambios.** Alta, modificación o deprecación de fichas: propuesta del Motor en «Incidencias y propuestas» de RC (evidencia de uso, casos de control, respaldo de F8, impacto) y aprobación del operador (tipo 3). Las versiones no se sobrescriben: conviven para permitir re-ejecuciones exactas.

1.8. **Operaciones sin ficha.** Se rechazan con la ficha más próxima (`FUERA_DE_CATALOGO`); un cálculo exploratorio puede servirse marcado `op_sin_ficha`, que impide su uso como cifra de un entregable (PA7, PC7, G3).

## 2. Ficha estándar

| # | Campo | Contenido |
|---|---|---|
| 1 | Identificación | `ficha_id` (FAM-NOMBRE-NNN), nombre, versión, estado de gobierno, módulo responsable, áreas del Mapa |
| 2 | Perfiles y horizontes | Perfiles PERF-B- y SEL- compatibles (o TRANSVERSAL) y horizontes H1–H5 en que el método es informativo (respetando las dos tablas de aplicabilidad de 8.6 del Documento 0). Las fichas marcadas «H4» son informativas también en H5 cuando su salida se usa como trayectoria estructural con bandas (nunca como probabilidad numérica, R13): ver 5.3 |
| 3 | Propósito | Pregunta cuantitativa que responde y decisión del bloque que informa |
| 4 | Entradas mínimas | Tipo, unidad, longitud, frecuencia, universo, conocibilidad |
| 5 | Método | Pasos y fórmulas esenciales; opciones declaradas |
| 6 | Parámetros | Nombre, valor por defecto, rango admitido |
| 7 | Salidas | Forma (VALOR, TABLA, SERIE, DISTRIBUCION, RANKING), contenido, unidades, clase de cifra (`determinista`, `estimacion_estadistica`, `juicio_experto`), `uso` cuando aplica |
| 8 | Supuestos y limitaciones | Condiciones de validez y advertencias obligatorias de entrega |
| 9 | Validaciones | Identidades, casos de control, segunda vía; cuándo se pide aclaración y cuándo se rechaza |
| 10 | Tolerancia y semilla | Tolerancia de re-ejecución (CT-B-14); semilla `null` o regla |
| 11 | Referencia ingenua | Código de 3.3 cuando el resultado se usa como pronóstico, señal o ranking |
| 12 | Referencias | Temática TMB- de F8 e IDs de referencia que respaldan el método |
| 13 | Prioridad y madurez | P0/P1/P2 y DOCUMENTADO, IMPLEMENTADO (heredado), IMPLEMENTADO o VALIDADO |

## 3. Convenciones comunes

### 3.1 Numéricas y de servicio

- **Capas técnicas internas**: toda ficha usa CTI-1 (validación y calidad de datos), CTI-2 (ejecución numérica, aritmética decimal, semillas), CTI-3 (fichas versionadas) y CTI-4 (artefacto y linaje). No se repite en cada ficha.
- **Rentabilidades** simples por defecto y en EUR (divisa base del marco de invertibilidad, 2.7 del Documento 0) salvo otra divisa en la petición; logarítmicas solo si la ficha lo pide, etiquetadas. **Anualización**: 252 sesiones (365 en criptoactivos; 260 o 252 declarado en divisas; 4 o 12 en series trimestrales o mensuales), capitalización compuesta. **Recuento de días**: Real/365 salvo convención de mercado. **Redondeo**: de banquero, solo al final; 4 decimales por defecto; S y A/E/C con la regla de HT-03.
- **Conocibilidad**: todo dato lleva «conocible desde»; con `fecha_corte` nada posterior entra. **Universos**: con su fecha; *point-in-time* en evaluación y backtesting.
- **Intervalos** al 90 % por defecto.
- **Clase de cifra compuesta**: la más débil de sus insumos críticos (`juicio_experto` < `estimacion_estadistica` < `determinista`).
- **Verificación**: doble pasada siempre; segunda vía recomendada en STD y obligatoria en EXT y en bandas marginales (ámbito ≤ 5 puntos de un umbral; candidato ≤ 3 puntos de 65, 50 o del corte del top-N).

### 3.2 Tolerancias por defecto (si la ficha no fija otra)

| Tipo de cálculo | Tolerancia |
|---|---|
| Aritmética determinista | 1e-10 relativa |
| Fórmulas cerradas | 1e-8 relativa |
| Estimadores iterativos | 1e-6 relativa en parámetros |
| Simulación o bootstrap con la misma semilla | 1e-6 relativa; rangos y marcas (`FRONTERA`, PC2) idénticos |
| Puntuaciones S, A, E, C | Igualdad exacta con HT-03 |
| Fechas, etiquetas, decisiones de contraste | Igualdad exacta |

### 3.3 Referencias ingenuas (códigos; 9.11 del Documento 0)

| Código | Referencia | Uso típico |
|---|---|---|
| RI-PA | Paseo aleatorio: rentabilidad relativa nula frente a la referencia del ámbito | PRG-B del indicador del ámbito |
| RI-UV | Último valor | Niveles: tamaño de mercado, tasa, diferencial, utilización |
| RI-MH | Media histórica conocida en t | Rentabilidades esperadas; valoraciones con reversión |
| RI-TB | Frecuencia base (climatología) | Probabilidades de evento y de dirección |
| RI-EST | Estacional ingenua | Inventarios, demanda estacional |
| RI-RA | Ranking aleatorio | Rankings de candidatos |
| RI-F1 | Ranking por un factor trivial (capitalización o momento 12-1) | Rankings de candidatos |
| RI-EQ | Media equiponderada del universo cribado | Rentabilidad del top-N |
| RI-LIN | Extrapolación lineal de la tendencia reciente conocida en t (V2.1) | Hitos intermedios H5 (9.11 del Documento 0) |
| RI-NA | No procede (cálculo descriptivo o determinista) | Descriptivos, réplicas, aritmética |

### 3.4 Prioridades

**P0** núcleo imprescindible: sin él el bloque no puede puntuar ni seleccionar con trazabilidad (R9), validar (G3), refutar con cifras ni certificar (R13). **P1** métodos propios de un tipo de objeto o de activo con datos gratuitos accesibles y uso frecuente. **P2** ampliación (datos especializados, coste alto o uso ocasional).

### 3.5 Planes

**MIN**: una operación, cribado (paso 5 de 9.4), N1; doble pasada e identidades. **STD**: cadenas, cifras de entregables, finalistas (N2); segunda vía si la ficha la declara, sensibilidad básica, IC de S y de rango con B = 1 000. **EXT**: N3, bandas marginales, CT-B-14 previsto; contraste multivía, Sobol, estabilidad entre semillas, variantes de winsorización y neutralización, B = 2 000.

## 4. Índice de fichas

| ficha_id | Nombre | Módulo | Perfiles principales | Horiz. | Prior. | Madurez |
|---|---|---|---|---|---|---|
| ST-DESC-001 | Estadística descriptiva y robusta | MC-B01 | TRANSVERSAL | — | P0 | IMPLEMENTADO (heredado) |
| ST-INF-001 | Contrastes, intervalos y comparaciones múltiples | MC-B01 | TRANSVERSAL | — | P0 | IMPLEMENTADO (heredado) |
| ST-BOOT-001 | Bootstrap iid, por bloques y estacionario | MC-B01 | TRANSVERSAL | — | P0 | DOCUMENTADO |
| FIN-CAGR-001 | Crecimiento, anualización y nominal/real | MC-B01 | TRANSVERSAL | — | P0 | IMPLEMENTADO (heredado) |
| FX-TREND-001 | Tendencia (Mann-Kendall y Sen) | MC-B01 | TRANSVERSAL | H2–H4 | P0 | IMPLEMENTADO (heredado) |
| FX-STL-001 | Descomposición tendencia-estacionalidad | MC-B01 | TRANSVERSAL | H2–H4 | P1 | IMPLEMENTADO (heredado) |
| FX-BRK-001 | Rupturas estructurales | MC-B01 | TRANSVERSAL | H2–H4 | P0 | IMPLEMENTADO (heredado) |
| FX-REGIME-001 | Regímenes (Markov-switching) | MC-B01 | TRANSVERSAL | H2–H4 | P0 | IMPLEMENTADO (heredado) |
| FX-VOL-001 | Volatilidad realizada | MC-B01 | TRANSVERSAL | H1–H3 | P0 | IMPLEMENTADO (heredado) |
| VOL-GARCH-001 | Volatilidad condicional GARCH | MC-B01 | TRANSVERSAL | H1–H3 | P1 | IMPLEMENTADO (heredado) |
| SER-HIER-001 | Conciliación jerárquica de previsiones | MC-B01 | PERF-B-TEMA, PERF-B-SECT | H3–H4 | P2 | DOCUMENTADO |
| SER-FLOW-001 | Flujos, posicionamiento y sentimiento | MC-B01 | PERF-B-SEGM, PERF-B-FACT; SEL-FON, SEL-DIV | H1–H3 | P1 | DOCUMENTADO |
| MKT-DIM-001 | TAM/SAM/SOM descendente | MC-B02 | PERF-B-TEMA, -SECT, -CADENA | H3–H4 | P0 | DOCUMENTADO |
| MKT-DIM-002 | TAM ascendente (demanda y oferta) | MC-B02 | PERF-B-TEMA, -SECT, -CADENA | H3–H4 | P0 | DOCUMENTADO |
| MKT-TRI-001 | Triangulación y conciliación de tamaños | MC-B02 | PERF-B-TEMA, -SECT, -CADENA | H3–H4 | P0 | DOCUMENTADO |
| MKT-SEG-001 | Crecimiento por segmento, volumen y precio | MC-B02 | PERF-B-TEMA, -SECT, -GEO | H3–H4 | P1 | DOCUMENTADO |
| DIF-BASS-001 | Difusión de Bass | MC-B02 | PERF-B-TEMA, -CADENA | H3–H4 | P1 | DOCUMENTADO |
| DIF-LOG-001 | Logística, Gompertz y sustitución | MC-B02 | PERF-B-TEMA, -CADENA | H3–H4 | P1 | DOCUMENTADO |
| DIF-GEN-001 | Generaciones sucesivas (Norton-Bass) | MC-B02 | PERF-B-TEMA | H4 | P2 | DOCUMENTADO |
| DIF-ANLG-001 | Analogías y a prioris de difusión | MC-B02 | PERF-B-TEMA | H4 | P1 | DOCUMENTADO |
| DIF-H5-001 | Proyección estructural H5: curvas S de largo plazo, sustitución e hitos (V2.1) | MC-B02 (con MC-B04, MC-B08) | PERF-B-TEMA, -CADENA, -SECT, -GEO | H5 | P1 | DOCUMENTADO |
| IO-CONC-001 | Concentración (HHI, CRn, N_eq, ΔHHI) | MC-B03 | PERF-B-SECT, -CADENA, -TEMA | H3–H4 | P0 | DOCUMENTADO |
| IO-LERN-001 | Lerner, márgenes precio-coste y markups | MC-B03 | PERF-B-SECT, -CADENA | H4 | P1 | DOCUMENTADO |
| IO-MARG-001 | Márgenes y captura de valor por eslabón | MC-B03 | PERF-B-CADENA, -SECT, -TEMA | H3–H4 | P0 | DOCUMENTADO |
| IO-SHARE-001 | Estabilidad y rotación de cuotas | MC-B03 | PERF-B-SECT, -CADENA | H4 | P1 | DOCUMENTADO |
| IO-PROF-001 | Persistencia de la rentabilidad | MC-B03 | PERF-B-SECT; SEL-RV | H4 | P1 | DOCUMENTADO |
| IO-BARG-001 | Poder de negociación | MC-B03 | PERF-B-CADENA, -SECT; SEL-RV | H3–H4 | P2 | DOCUMENTADO |
| VC-DESG-001 | Desglose jerárquico de la cadena de valor y atractivo del eslabón AE (V2.1) | MC-B03 (con MC-B04, MC-B09) | PERF-B-CADENA, -SECT, -TEMA; todo ámbito con D4 en P2 o P3 | H3–H5 | P0 | DOCUMENTADO |
| SUP-COST-001 | Curva de costes y coste marginal | MC-B04 | PERF-B-CADENA, -SEGM; SEL-MP | H3–H4 | P1 | DOCUMENTADO |
| SUP-UTIL-001 | Utilización, capacidad y balance | MC-B04 | PERF-B-CADENA, -SECT, -SEGM | H3–H4 | P1 | DOCUMENTADO |
| SUP-BOTT-001 | Identificación de cuellos de botella | MC-B04 | PERF-B-CADENA, -TEMA | H3–H4 | P0 | DOCUMENTADO |
| VC-BOT-001 | Indicadores de cuello en semáforo y puntuación PCB (V2.1) | MC-B04 (con MC-B08) | PERF-B-CADENA, -SECT, -TEMA; todo ámbito con D4 en P2 o P3 | H3–H5 | P0 | DOCUMENTADO |
| SUP-LRN-001 | Curva de aprendizaje (Wright) | MC-B04 | PERF-B-TEMA, -CADENA | H4 | P1 | DOCUMENTADO |
| SUP-LRN-002 | Previsión tecnológica probabilística | MC-B04 | PERF-B-TEMA | H4 | P2 | DOCUMENTADO |
| SUP-INV-001 | Inventarios frente a norma estacional | MC-B04 | PERF-B-SEGM; SEL-MP | H2–H3 | P1 | DOCUMENTADO |
| ECO-ELAS-001 | Elasticidades precio y renta | MC-B05 | PERF-B-SECT, -TEMA, -SEGM | H3–H4 | P1 | DOCUMENTADO |
| ECO-PANEL-001 | Paneles sectoriales | MC-B05 | PERF-B-SECT, -GEO | H3–H4 | P1 | DOCUMENTADO |
| ECO-CYC-001 | Betas al ciclo y sensibilidad a tipos | MC-B05 | PERF-B-SECT, -GEO, -SEGM | H2–H4 | P0 | DOCUMENTADO |
| ECO-LP-001 | Proyecciones locales (respuestas a impulsos) | MC-B05 | PERF-B-GEO, -SECT | H3–H4 | P2 | DOCUMENTADO |
| ECO-GRANG-001 | Causalidad de Granger con cautela | MC-B05 | TRANSVERSAL | H2–H4 | P2 | DOCUMENTADO |
| FX-COINT-001 | Cointegración y corrección de errores | MC-B05 | TRANSVERSAL | H3–H4 | P1 | IMPLEMENTADO (heredado) |
| ECO-EXPO-001 | Exposición del candidato al factor del ámbito | MC-B05 | SEL-DIV, SEL-MP, SEL-TCV, SEL-RV | H2–H4 | P0 | DOCUMENTADO |
| VAL-DCF-001 | DCF del agregado y de candidatos (para ordenar) | MC-B06 | PERF-B-SECT, -TEMA; SEL-RV | H3–H4 | P0 | DOCUMENTADO |
| VAL-REV-001 | DCF inverso y brecha de expectativas | MC-B06 | PERF-B-SECT, -TEMA, -GEO; SEL-RV | H3–H4 | P0 | DOCUMENTADO |
| VAL-MULT-001 | Múltiplos relativos y bandas de comparables | MC-B06 | PERF-B-SECT, -GEO; SEL-RV, SEL-IDX, SEL-FON | H3–H4 | P0 | DOCUMENTADO |
| VAL-ROIC-001 | ROIC − WACC y beneficio económico | MC-B06 | PERF-B-SECT; SEL-RV | H4 | P0 | DOCUMENTADO |
| VAL-WACC-001 | Coste de capital sectorial (Damodaran) | MC-B06 | PERF-B-SECT, -GEO, -TEMA | H3–H4 | P0 | DOCUMENTADO |
| VAL-PROJ-001 | Máquina de proyecciones (TAM a capitalización implícita) | MC-B06 | PERF-B-TEMA, -SECT, -CADENA | H4 | P0 | DOCUMENTADO |
| ACC-ERP-001 | Prima de riesgo implícita | MC-B06 | PERF-B-GEO, -SECT | H3–H4 | P1 | DOCUMENTADO |
| IDX-ERP-001 | Rentabilidad esperada por componentes (Grinold-Kroner) | MC-B06 | PERF-B-GEO; SEL-IDX | H4 | P1 | DOCUMENTADO |
| VAL-RF-001 | Rentabilidad esperada neta de pérdida esperada, carry y rolldown | MC-B06 | PERF-B-SEGM; SEL-RF | H2–H4 | P1 | DOCUMENTADO |
| FIR-SPREAD-001 | Diferencial de crédito: percentil y valor relativo | MC-B06 | PERF-B-SEGM; SEL-RF | H2–H4 | P1 | DOCUMENTADO |
| FX-CARRY-001 | Carry de divisas ajustado por volatilidad | MC-B06 | SEL-DIV, SEL-MON | H1–H3 | P1 | IMPLEMENTADO (heredado) |
| FX-PPA-001 | Desviación de PPA relativa | MC-B06 | SEL-DIV; PERF-B-GEO | H4 | P1 | IMPLEMENTADO (heredado) |
| FX-BEER-001 | Tipo de cambio real de equilibrio (BEER) | MC-B06 | SEL-DIV; PERF-B-GEO | H4 | P2 | DOCUMENTADO |
| CMD-CURVE-001 | Estructura de la curva de futuros y roll yield | MC-B06 | SEL-MP, SEL-DER | H1–H4 | P1 | IMPLEMENTADO (heredado) |
| REI-NAV-001 | Prima o descuento sobre NAV | MC-B06 | SEL-INM | H3–H4 | P1 | DOCUMENTADO |
| REI-CAP-001 | Cap rate implícito y diferencial con el bono | MC-B06 | SEL-INM | H3–H4 | P1 | DOCUMENTADO |
| FON-DISC-001 | Descuento de vehículos cerrados frente a su media | MC-B06 | SEL-FON, SEL-ALT | H3–H4 | P1 | DOCUMENTADO |
| DER-VRP-001 | Prima de varianza, sesgo y estructura de plazos | MC-B06 | SEL-DER, SEL-TCV | H1–H3 | P1 | DOCUMENTADO |
| CHR-ONCHAIN-001 | Métricas de red (capitalización/comisiones, NVT, MVRV, FDV) | MC-B06 | SEL-CRI | H3–H4 | P1 | DOCUMENTADO |
| MON-YLD-001 | Rentabilidad monetaria equivalente y fijar frente a renovar | MC-B06 | SEL-MON | H2–H3 | P1 | DOCUMENTADO |
| TCV-CARRY-001 | Valor razonable, carry y rolldown de factores de tipos, crédito y volatilidad | MC-B06 | SEL-TCV | H1–H3 | P1 | DOCUMENTADO |
| PRV-PME-001 | Public market equivalent | MC-B06 | SEL-ALT | H4 | P1 | DOCUMENTADO |
| ALT-DESMOOTH-001 | Desuavizado de rentabilidades | MC-B06 | SEL-ALT, SEL-INM | H3–H4 | P1 | DOCUMENTADO |
| QLT-ACC-001 | Calidad contable y señales de alerta | MC-B06 | SEL-RV, SEL-RF, SEL-INM | H3–H4 | P0 | DOCUMENTADO |
| SCR-NORM-001 | Winsorización, percentiles y neutralización | MC-B07 | Todos los SEL- | — | P0 | DOCUMENTADO |
| SCR-PUR-001 | Pureza de exposición | MC-B07 | Todos los SEL-; PERF-B-TEMA | — | P0 | DOCUMENTADO |
| SCR-PUR-002 | Pureza por análisis de texto | MC-B07 | SEL-RV, SEL-RF; PERF-B-TEMA | — | P2 | DOCUMENTADO |
| SCR-S-001 | Puntuación S (réplica de HT-03) | MC-B07 | Todos los SEL- | — | P0 | DOCUMENTADO |
| SCR-AEC-001 | Puntuaciones A, E y C (réplica de HT-03) | MC-B07 | TRANSVERSAL | — | P0 | DOCUMENTADO |
| SCR-ROB-001 | Robustez del ranking: IC de S y de rango | MC-B07 | Todos los SEL- | — | P0 | DOCUMENTADO |
| SCR-DUP-001 | Duplicación de exposición | MC-B07 | Todos los SEL- | — | P0 | DOCUMENTADO |
| ML-CLUS-001 | Clústeres y apuestas independientes | MC-B07 | TRANSVERSAL | — | P0 | IMPLEMENTADO (heredado) |
| ACC-MOM-001 | Momento 12-1, de serie temporal y revisiones | MC-B07 | SEL-RV, SEL-IDX, SEL-DIV, SEL-MP, SEL-CRI | H2–H3 | P1 | IMPLEMENTADO (heredado) |
| SCR-LIQ-001 | Liquidez y costes de mantener | MC-B07 | Todos los SEL- | — | P0 | DOCUMENTADO |
| SCR-MCDA-001 | Decisión multicriterio para rasgos de la tesis | MC-B07 | TRANSVERSAL | — | P2 | DOCUMENTADO |
| FAC-PREM-001 | Prima y descomposición de un factor | MC-B07 | PERF-B-FACT | H3–H4 | P1 | DOCUMENTADO |
| FAC-SPREAD-001 | Diferencial de valoración del factor | MC-B07 | PERF-B-FACT | H3–H4 | P1 | DOCUMENTADO |
| FAC-CROWD-001 | Crowding del factor o de la tesis | MC-B07 | PERF-B-FACT, -TEMA | H2–H3 | P2 | DOCUMENTADO |
| EMG-PEM-001 | Puntuación de potencial de emergentes PEM y pureza de la vía de exposición (V2.1) | MC-B07 (con MC-B02) | PERF-B-TEMA, -SECT, -CADENA; SEL-RV, SEL-FON | H4–H5 | P1 | DOCUMENTADO |
| SIM-MC-001 | Monte Carlo y cuasi-Monte Carlo | MC-B08 | TRANSVERSAL | H1–H5 (H5 con bandas) | P0 | IMPLEMENTADO (heredado) |
| SIM-IC-001 | Dependencias por Iman-Conover y cópulas | MC-B08 | TRANSVERSAL | H2–H4 | P0 | DOCUMENTADO |
| SIM-SCN-001 | Escenarios coherentes, probabilidad frente a la referencia y RE | MC-B08 | Todos los PERF-B- | H2–H4 | P0 | DOCUMENTADO |
| SIM-TOR-001 | Tornado y cribado de Morris | MC-B08 | TRANSVERSAL | — | P0 | DOCUMENTADO |
| SIM-SOB-001 | Índices de Sobol | MC-B08 | TRANSVERSAL | — | P1 | DOCUMENTADO |
| SIM-JUD-001 | Agregación de juicio experto | MC-B08 | TRANSVERSAL | — | P1 | DOCUMENTADO |
| SIM-BOTT-001 | Persistencia del cuello por simulación | MC-B08 | PERF-B-CADENA | H3–H4 | P2 | DOCUMENTADO |
| DEC-VOI-001 | Valor de la información | MC-B08 | TRANSVERSAL | — | P1 | DOCUMENTADO |
| RISK-VAR-001 | VaR y Expected Shortfall | MC-B09 | TRANSVERSAL | H1–H3 | P0 | IMPLEMENTADO (heredado) |
| RISK-DD-001 | Drawdown, liquidez y escala de riesgo 1–5 | MC-B09 | TRANSVERSAL | H2–H4 | P0 | IMPLEMENTADO (heredado) |
| RISK-STR-001 | Estrés histórico, hipotético e inverso | MC-B09 | Todos los PERF-B- | H2–H4 | P0 | DOCUMENTADO |
| RISK-CRASH-001 | Distribución de pérdidas y colapsos de factores | MC-B09 | PERF-B-FACT | H2–H4 | P1 | DOCUMENTADO |
| RISK-GEO-001 | Riesgo país y de divisa | MC-B09 | PERF-B-GEO; SEL-DIV, SEL-RF | H3–H4 | P1 | DOCUMENTADO |
| FX-CORR-001 | Correlación dinámica y dependencia de cola | MC-B09 | TRANSVERSAL | H1–H4 | P0 | IMPLEMENTADO (heredado) |
| RISK-RGC-001 | Correlaciones condicionadas al régimen | MC-B09 | PERF-B-GEO, -SEGM, -FACT | H2–H4 | P1 | DOCUMENTADO |
| NET-IO-001 | Análisis input-output | MC-B09 | PERF-B-CADENA, -GEO, -TEMA | H4 | P1 | DOCUMENTADO |
| NET-SHOCK-001 | Contagio de choques en la cadena | MC-B09 | PERF-B-CADENA, -TEMA | H3–H4 | P1 | DOCUMENTADO |
| NET-EXPO-001 | Concentración de exposiciones comunes | MC-B09 | PERF-B-CADENA, -GEO; todos los SEL- | H3–H4 | P1 | DOCUMENTADO |
| FC-EVAL-001 | Puntuación y comparación de pronósticos | MC-B10 | TRANSVERSAL | H1–H4 | P0 | IMPLEMENTADO (heredado) |
| FC-CAL-001 | Calibración y fiabilidad | MC-B10 | TRANSVERSAL | H1–H4 | P0 | IMPLEMENTADO (heredado) |
| FC-CERT-001 | Insumos del certificado de probabilidad | MC-B10 | TRANSVERSAL | H1–H4 | P0 | DOCUMENTADO |
| RK-IC-001 | IC de rango | MC-B10 | Todos los SEL- | H2–H4 | P0 | DOCUMENTADO |
| RK-TOPN-001 | Exceso y acierto del top-N | MC-B10 | Todos los SEL- | H2–H4 | P0 | DOCUMENTADO |
| RK-CERT-001 | Insumos del certificado de ranking | MC-B10 | Todos los SEL- | H2–H4 | P0 | DOCUMENTADO |
| BT-SEL-001 | Backtesting de selección sin sesgos | MC-B10 | Todos los SEL-; PERF-B-FACT | H2–H4 | P0 | DOCUMENTADO |
| BT-DSR-001 | Sharpe probabilístico y deflactado | MC-B10 | PERF-B-FACT; TRANSVERSAL | — | P1 | DOCUMENTADO |
| BT-PBO-001 | Probabilidad de sobreajuste del backtest (CSCV) | MC-B10 | PERF-B-FACT; TRANSVERSAL | — | P1 | DOCUMENTADO |
| EVL-TIME-001 | Modelo de tiempos (p50 y p80) | MC-B10 | TRANSVERSAL | — | P1 | DOCUMENTADO |
| FC-HITO-001 | Evaluación de H5 por hitos intermedios (V2.1) | MC-B10 | TRANSVERSAL | H5 | P1 | DOCUMENTADO |
| EVL-PV-001 | Evaluación de puertas de viabilidad y de seguimientos encargados (V2.1) | MC-B10 | TRANSVERSAL | H1–H5 | P1 | DOCUMENTADO |
| AUD-REX-001 | Re-ejecución independiente (CT-B-14) | Instancia aislada | TRANSVERSAL | — | P0 | IMPLEMENTADO (heredado) |

## 5. Cobertura

### 5.1 Por tipo de objeto y dimensión

| Dimensión | SECTOR | TEMATICA | MERCADO_GEOGRAFICO | SEGMENTO_DE_CLASE | ESTRATEGIA_FACTOR | CADENA_DE_VALOR |
|---|---|---|---|---|---|---|
| D1 | IO-CONC-001 | SCR-PUR-001 (universo), SCR-PUR-002 | — | IO-CONC-001 | FAC-PREM-001 (definición del factor) | IO-CONC-001 |
| D2 | MKT-DIM-001/002, ECO-ELAS-001 | MKT-DIM-001/002, MKT-TRI-001, DIF-BASS-001, DIF-LOG-001 | MKT-SEG-001 | ECO-ELAS-001 | SCR-LIQ-001 (capacidad de la estrategia) | MKT-DIM-002, MKT-SEG-001 |
| D3 | SUP-UTIL-001, SUP-COST-001 | SUP-LRN-001 | — | SUP-COST-001, SUP-INV-001, SUP-UTIL-001 | — | SUP-COST-001, SUP-UTIL-001, SUP-BOTT-001 |
| D4 | IO-CONC-001, IO-MARG-001, IO-SHARE-001, VC-DESG-001, VC-BOT-001 | IO-MARG-001, NET-IO-001, VC-DESG-001, VC-BOT-001 | NET-IO-001 (sector ancla) | IO-CONC-001 | — | IO-MARG-001, NET-IO-001, NET-SHOCK-001, VC-DESG-001, VC-BOT-001 |
| D5 | SUP-LRN-001 | SUP-LRN-001/002, DIF-GEN-001, DIF-H5-001 | — | — | — | SUP-LRN-001, DIF-H5-001 |
| Emergentes (AG-B24; D4, D5) | EMG-PEM-001 | EMG-PEM-001 | EMG-PEM-001 (condicional) | EMG-PEM-001 (condicional) | — | EMG-PEM-001 |
| D6 | NET-EXPO-001 | NET-EXPO-001 | RISK-GEO-001 | RISK-STR-001 | — | NET-EXPO-001, NET-SHOCK-001 |
| D7 | ECO-CYC-001, FX-REGIME-001 | ECO-CYC-001 | ECO-CYC-001, ECO-LP-001, RISK-RGC-001 | ECO-CYC-001, FX-REGIME-001 | FX-REGIME-001, RISK-RGC-001 | ECO-CYC-001 |
| D8 | VAL-ROIC-001, IO-PROF-001, QLT-ACC-001 | VAL-ROIC-001 | VAL-ROIC-001 (agregado) | VAL-RF-001 (crédito agregado) | FAC-PREM-001 (fundamento de la prima) | IO-MARG-001, VAL-ROIC-001 |
| D9 | VAL-REV-001, VAL-MULT-001, VAL-WACC-001 | VAL-REV-001, VAL-PROJ-001 | IDX-ERP-001, ACC-ERP-001, VAL-MULT-001 | Fichas específicas por tipo | FAC-SPREAD-001 | VAL-REV-001 |
| D10 | SER-FLOW-001 | SER-FLOW-001, FAC-CROWD-001 | SER-FLOW-001 | SER-FLOW-001 | FAC-CROWD-001 | — |
| D11 | RISK-STR-001 (transición) | RISK-STR-001 | RISK-STR-001 | RISK-STR-001 | — | RISK-STR-001 |
| D12 | SIM-SCN-001, RISK-STR-001, RISK-VAR-001 | SIM-SCN-001, SIM-SOB-001 | SIM-SCN-001, RISK-GEO-001 | RISK-STR-001, RISK-VAR-001 | RISK-CRASH-001, BT-SEL-001 | SIM-SCN-001, SIM-BOTT-001 |
| Puntuaciones | SCR-AEC-001, SIM-SCN-001 (RE), DEC-VOI-001 (todas las columnas); V2.1: AE y PCB (VC-DESG-001, VC-BOT-001) y PEM (EMG-PEM-001) con réplica exacta de HT-03; insumos de las puertas PV1–PV3 (VAL-MULT-001 o VAL-REV-001 en percentil histórico, SCR-LIQ-001 y SCR-PUR-001 sobre el universo preliminar, VC-DESG-001 y VC-BOT-001 en PV3) | | | | | |

### 5.2 Por tipo de activo (perfiles de selección)

| SEL- | Pureza | QL | VA | MO | RI | LA | CO |
|---|---|---|---|---|---|---|---|
| SEL-RV | SCR-PUR-001 (segmentos), ECO-EXPO-001 (2.ª vía) | VAL-ROIC-001, QLT-ACC-001, IO-PROF-001 | VAL-MULT-001, VAL-REV-001 | ACC-MOM-001 | FX-VOL-001, ECO-CYC-001, IO-BARG-001 | SCR-LIQ-001 | NA |
| SEL-RF | SCR-PUR-001 | QLT-ACC-001 (emisor), métricas de crédito | FIR-SPREAD-001, VAL-RF-001 | Deriva de calificación (ST-DESC-001) | RISK-DD-001 | SCR-LIQ-001 | NA |
| SEL-DIV | ECO-EXPO-001 | Macro externa (RISK-GEO-001) | FX-PPA-001, FX-BEER-001, FX-CARRY-001 | ACC-MOM-001 | FX-VOL-001, RISK-VAR-001 | SCR-LIQ-001 | SCR-LIQ-001 |
| SEL-MP | ECO-EXPO-001 | Emisor y colateral (dato) | CMD-CURVE-001, SUP-COST-001, SUP-INV-001 | ACC-MOM-001 | FX-VOL-001 | SCR-LIQ-001 | SCR-LIQ-001 |
| SEL-IDX | SCR-PUR-001 | Concentración (IO-CONC-001) | IDX-ERP-001, VAL-MULT-001 | ACC-MOM-001 | RISK-DD-001 | SCR-LIQ-001 | SCR-LIQ-001 |
| SEL-FON | SCR-PUR-001 (solapamiento) | Seguimiento (ST-DESC-001), alfa (FAC-PREM-001) | VAL-MULT-001 (cartera), FON-DISC-001 | SER-FLOW-001 | RISK-DD-001 | SCR-LIQ-001 | SCR-LIQ-001 |
| SEL-DER | Herencia del subyacente | NA | DER-VRP-001, CMD-CURVE-001 | ACC-MOM-001 | RISK-VAR-001 | SCR-LIQ-001 | SCR-LIQ-001 |
| SEL-INM | SCR-PUR-001 (GAV) | Métricas de cartera (dato), QLT-ACC-001 | REI-NAV-001, REI-CAP-001 | ACC-MOM-001 | RISK-DD-001 | SCR-LIQ-001 | SCR-LIQ-001 |
| SEL-CRI | SCR-PUR-001 | Métricas de uso (dato) | CHR-ONCHAIN-001 | ACC-MOM-001 | RISK-VAR-001, RISK-DD-001 | SCR-LIQ-001 | SCR-LIQ-001 |
| SEL-ALT | SCR-PUR-001 (NAV) | PRV-PME-001 | FON-DISC-001, ALT-DESMOOTH-001 | ACC-MOM-001 | RISK-DD-001 | SCR-LIQ-001 | SCR-LIQ-001 |
| SEL-MON | SCR-PUR-001 (binaria) | Calidad y WAM (dato) | MON-YLD-001 | NA | RISK-DD-001 | SCR-LIQ-001 | SCR-LIQ-001 |
| SEL-TCV | ECO-EXPO-001 | NA | TCV-CARRY-001, DER-VRP-001 | ACC-MOM-001 | RISK-VAR-001 | SCR-LIQ-001 | SCR-LIQ-001 |

Comunes a todos: SCR-NORM-001, SCR-S-001, SCR-ROB-001, SCR-DUP-001, ML-CLUS-001, NET-EXPO-001 (exposiciones comunes), RK-IC-001, RK-TOPN-001 (evaluación).

### 5.3 Por horizonte (aplicabilidad de 8.6 del Documento 0)

| Horizonte | Métodos dominantes | Advertencia |
|---|---|---|
| H1 días | FX-VOL-001, VOL-GARCH-001, RISK-VAR-001, DER-VRP-001, CMD-CURVE-001, FX-CARRY-001, TCV-CARRY-001, SER-FLOW-001 | Sin tiempo real (R30): frescura declarada; menor fiabilidad; no en FON, INM, ALT |
| H2 semanas | ACC-MOM-001, SER-FLOW-001, FX-TREND-001, FX-REGIME-001, ECO-CYC-001, FIR-SPREAD-001, SUP-INV-001, MON-YLD-001 | Valoración solo como contexto |
| H3 meses | VAL-MULT-001, ECO-CYC-001, RISK-RGC-001, REI-NAV-001, FON-DISC-001, VAL-RF-001, SIM-SCN-001, RISK-STR-001 | Regímenes y catalizadores dominan; DER ≤ 12 meses |
| H4 años | MKT-DIM-001/002, MKT-TRI-001, DIF-BASS-001, DIF-LOG-001, SUP-LRN-001/002, IO-*, VAL-DCF-001, VAL-REV-001, VAL-ROIC-001, VAL-PROJ-001, IDX-ERP-001, NET-IO-001, PRV-PME-001 | Pocas observaciones independientes; no en DER ni MON |

| H5 décadas (V2.1) | DIF-H5-001 (con DIF-BASS-001, DIF-LOG-001, DIF-GEN-001, DIF-ANLG-001, SUP-LRN-002), MKT-DIM-001/002 y MKT-TRI-001 a largo plazo, VAL-REV-001 y VAL-PROJ-001 (lo que el precio ya descuenta), VC-BOT-001 (persistencia de cuellos), EMG-PEM-001, SIM-SCN-001 de sustitución y demografía | Probabilidades **siempre cualitativas** (R13): las fichas entregan trayectorias y bandas, nunca probabilidades numéricas publicables; ≥ 3 hitos verificables por tesis (FC-HITO-001); antigüedad máxima de datos de mercado 90 días; no en DER ni MON; «Limitado» en RF, DIV, CRI, TCV y MP |

Evaluación de cualquier horizonte: FC-EVAL-001, FC-CAL-001, FC-CERT-001, RK-IC-001, RK-TOPN-001, RK-CERT-001, BT-SEL-001, BT-DSR-001, BT-PBO-001; en H5, FC-HITO-001; de las puertas y de los seguimientos, EVL-PV-001.

---

## 6. Fichas — MC-B01 Estadística y series

### ST-DESC-001 · Estadística descriptiva y robusta

**Identificación.** v2.0 · VIGENTE · MC-B01 · Mapa: áreas 2, 3. Conservada del Catálogo V5.0 del Bloque A.
**Perfiles y horizontes.** TRANSVERSAL · no aplica.
**Propósito.** Describir una muestra (serie, corte transversal de un universo) con medidas clásicas y robustas, atípicos marcados y percentiles históricos.
**Entradas mínimas.** ≥ 5 observaciones con unidad y periodo; ≥ 250 para cuantiles al 1 %.
**Método.** (i) Media, mediana, desviación típica, `σ_rob = 1,4826·MAD`, media recortada al 10 %, asimetría G1 y exceso de curtosis G2 ajustados, cuantiles tipo 7. (ii) Atípicos marcados si `|x − med|/σ_rob > 3` (o Tukey; Hampel en series). (iii) Percentil histórico y z (clásico y robusto) del último valor frente a una ventana declarada. (iv) IC de media y mediana (analítico o bootstrap).
**Parámetros.** ventana (10 años RV/RF; toda la historia en MP); nivel (0,90); umbral_atipico (3).
**Salidas.** TABLA de estadísticos con IC; lista de atípicos; percentil y z. `estimacion_estadistica`.
**Supuestos y limitaciones.** La curtosis muestral es inestable con colas pesadas (IC bootstrap obligatorio); un percentil histórico no es una probabilidad futura.
**Validaciones.** Doble pasada; cuantiles monótonos; normal simulada con momentos conocidos. Rechazo con < 5 observaciones; aclaración si falta la unidad.
**Tolerancia y semilla.** 1e-10 (deterministas), 1e-6 (bootstrap) · entero del plan.
**Referencia ingenua.** RI-NA.
**Referencias.** TMB-01, TMB-14 · DOC-MOT-0471.
**Prioridad y madurez.** P0 · IMPLEMENTADO (heredado).

### ST-INF-001 · Contrastes, intervalos y comparaciones múltiples

**Identificación.** v2.0 · VIGENTE · MC-B01 · Mapa: área 3. Conservada del Bloque A.
**Perfiles y horizontes.** TRANSVERSAL · no aplica.
**Propósito.** Contrastar hipótesis sobre medias, medianas, proporciones, correlaciones y distribuciones con tamaño de efecto, potencia y control de comparaciones múltiples.
**Entradas mínimas.** Muestras con unidad; m (número de pruebas sobre la misma conclusión).
**Método.** (i) Elección de la prueba (t/Welch, Wilcoxon, Mann-Whitney, KS, Anderson-Darling, χ², Fisher, binomial exacta con IC de Wilson, correlación con z de Fisher). (ii) Estadístico, p, tamaño del efecto e IC. (iii) Potencia `n ≈ [(z_{1−α/2} + z_{1−β})σ/δ]²`. (iv) Holm (confirmatorio) o BH con q = 0,10 (cribado). (v) Bayes Beta-binomial con n pequeño.
**Parámetros.** alfa (0,10 bilateral para IC 90 %); correccion (holm | bh); m (obligatorio si > 1).
**Salidas.** TABLA: estadístico, p, p ajustado, efecto, IC, potencia. `estimacion_estadistica`.
**Supuestos y limitaciones.** Pruebas iid no válidas con autocorrelación (usar ST-BOOT-001 por bloques); «no significativo» con baja potencia no es «sin efecto».
**Validaciones.** IC coherente con p; caso con p conocido. Rechazo si m no se declara en contexto de múltiples pruebas.
**Tolerancia y semilla.** 1e-8 · null (o entero del plan si hay remuestreo).
**Referencia ingenua.** RI-NA.
**Referencias.** TMB-01, TMB-14 · DOC-MOT-0471, DOC-MOT-0472.
**Prioridad y madurez.** P0 · IMPLEMENTADO (heredado).

### ST-BOOT-001 · Bootstrap iid, por bloques y estacionario

**Identificación.** v1.0 · VIGENTE · MC-B01 · Mapa: área 4.
**Perfiles y horizontes.** TRANSVERSAL · no aplica.
**Propósito.** Intervalos y errores estándar de estadísticos sin forma cerrada fiable, respetando la dependencia temporal y, en universos, la correlación transversal.
**Entradas mínimas.** Muestra o panel con índice temporal; ≥ 30 observaciones (≥ 100 para bloques).
**Método.** (i) Diagnóstico de dependencia (Ljung-Box en la serie y sus cuadrados). (ii) iid, bloques móviles, circular o **estacionario** de Politis-Romano (longitud media por Politis-White o `T^{1/3}`). (iii) En universos, mismos índices temporales para todos los candidatos. (iv) IC percentil, BCa o estudentizado.
**Parámetros.** B (1 000 EE; 2 000 IC; 10 000 colas o EXT); tipo (auto); bloque (auto).
**Salidas.** DISTRIBUCION bootstrap; IC; EE; error de Monte Carlo. `estimacion_estadistica`.
**Supuestos y limitaciones.** Estacionariedad; los bloques cortos infravaloran la dependencia; el bootstrap no corrige sesgos de selección de la muestra.
**Validaciones.** Proceso AR(1) simulado con varianza conocida de la media; segunda vía: IC analítico HAC. Rechazo con < 30 observaciones.
**Tolerancia y semilla.** 1e-6 · entero del plan.
**Referencia ingenua.** RI-NA.
**Referencias.** TMB-08, TMB-01 · DOC-MOT-0080.
**Prioridad y madurez.** P0 · DOCUMENTADO.

### FIN-CAGR-001 · Crecimiento, anualización y nominal/real

**Identificación.** v2.0 · VIGENTE · MC-B01 · Mapa: área 1. Conservada del Bloque A.
**Perfiles y horizontes.** TRANSVERSAL · no aplica.
**Propósito.** Tasas de crecimiento, anualizaciones, conversiones de divisa y deflactación con efecto base controlado.
**Entradas mínimas.** Valores inicial y final con fechas (o serie); deflactor o tipo de cambio con fecha y fuente si se piden.
**Método.** `CAGR = (V_f/V_i)^{1/años} − 1` (indefinido si `V_i ≤ 0`); `(1 + R)^m − 1`; `1 + R_EUR = (1 + R_local)(1 + R_fx)`; Fisher exacta; contribuciones `w_{s,t−1}·g_s` con residuo de encadenamiento; tasa sobre dos años anualizada como contraste del efecto base.
**Parámetros.** base_anual (Real/365); divisa (EUR).
**Salidas.** VALOR o TABLA con unidades. `determinista`.
**Supuestos y limitaciones.** El CAGR oculta la trayectoria; anualizar menos de un año amplifica el ruido.
**Validaciones.** Capitalizar las tasas reproduce el acumulado. Rechazo con signos opuestos en extremos.
**Tolerancia y semilla.** 1e-10 · null.
**Referencia ingenua.** RI-NA (como previsión: crecimiento constante RI-MH).
**Referencias.** TMB-01.
**Prioridad y madurez.** P0 · IMPLEMENTADO (heredado).

### FX-TREND-001 · Tendencia (Mann-Kendall y pendiente de Sen)

**Identificación.** v2.0 · VIGENTE · MC-B01 · Mapa: área 5. Conservada del Bloque A.
**Perfiles y horizontes.** TRANSVERSAL · H2–H4.
**Propósito.** ¿Tiene la serie del ámbito (ventas, precios, penetración, flujos) una tendencia monótona y cuál es su pendiente?
**Entradas mínimas.** ≥ 10 observaciones (20 recomendadas) con frecuencia declarada.
**Método.** (i) Mann-Kendall con corrección de Hamed-Rao. (ii) Pendiente de Sen con IC por rangos. (iii) Aceleración opcional (pendientes de dos mitades). (iv) Sensibilidad a la ventana en STD/EXT.
**Parámetros.** ventana; corregir_autocorrelacion (true); nivel (0,10).
**Salidas.** TABLA: S, Z, p, pendiente con IC, dirección. `estimacion_estadistica`.
**Supuestos y limitaciones.** No distingue tendencia de ciclo largo.
**Validaciones.** Serie creciente de n puntos ⇒ `S = n(n − 1)/2`; segunda vía MCO-HAC. Rechazo con < 10 observaciones.
**Tolerancia y semilla.** 1e-6 · null.
**Referencia ingenua.** RI-PA (pendiente nula).
**Referencias.** TMB-01 · DOC-MOT-0021, DOC-MOT-0022, DOC-MOT-0023, DOC-MOT-0202.
**Prioridad y madurez.** P0 · IMPLEMENTADO (heredado).

### FX-STL-001 · Descomposición tendencia-estacionalidad

**Identificación.** v2.0 · VIGENTE · MC-B01 · Mapa: área 6. Conservada del Bloque A.
**Perfiles y horizontes.** TRANSVERSAL · H2–H4.
**Propósito.** Separar tendencia, estacionalidad y resto en series sectoriales (ventas, producción, inventarios).
**Entradas mínimas.** ≥ 2 ciclos completos (3 recomendados).
**Método.** STL robusta (ventana estacional impar ≥ 7 o periódica); X-13 o TRAMO-SEATS para series oficiales si se pide; filtro de Hamilton (h = 8 trimestres) en lugar de HP para el ciclo.
**Parámetros.** periodo; s_window (7); robusto (true).
**Salidas.** SERIE de componentes; fuerza de la estacionalidad. `estimacion_estadistica`.
**Supuestos y limitaciones.** Estacionalidad cambiante; sesgo de extremo en filtros de ciclo.
**Validaciones.** Tendencia + estacionalidad + resto = serie. Rechazo con < 2 ciclos.
**Tolerancia y semilla.** 1e-8 · null.
**Referencia ingenua.** RI-EST.
**Referencias.** TMB-01 · DOC-MOT-0030, DOC-MOT-0029, DOC-MOT-0257, MBM-0009, MBM-0011.
**Prioridad y madurez.** P1 · IMPLEMENTADO (heredado).

### FX-BRK-001 · Rupturas estructurales

**Identificación.** v2.0 · VIGENTE · MC-B01 · Mapa: área 7. Conservada del Bloque A.
**Perfiles y horizontes.** TRANSVERSAL · H2–H4.
**Propósito.** Fechar cambios de nivel o pendiente (cambio de régimen de demanda, regulación, tecnología) y alimentar el criterio de cambio estructural del Vigía.
**Entradas mínimas.** ≥ 30 observaciones por segmento (50 para dos o más rupturas).
**Método.** Chow (fecha conocida); Quandt-Andrews; Bai-Perron (hasta 5, segmento mínimo 15 %, BIC/LWZ, IC de fechas); CUSUM de Page para vigilancia.
**Parámetros.** max_rupturas (5); recorte (0,15); h_cusum (4σ).
**Salidas.** TABLA: fechas con IC, parámetros por segmento, estadísticos. `estimacion_estadistica`.
**Supuestos y limitaciones.** Una revisión metodológica de la fuente imita una ruptura; la ruptura no identifica su causa.
**Validaciones.** Ruptura sintética recuperada; segunda vía CUSUM. Rechazo bajo mínimos.
**Tolerancia y semilla.** 1e-6; fechas exactas · null.
**Referencia ingenua.** RI-NA.
**Referencias.** TMB-01 · DOC-MOT-0024, DOC-MOT-0025, DOC-MOT-0253, DOC-MOT-0254, DOC-MOT-0031, DOC-MOT-0256.
**Prioridad y madurez.** P0 · IMPLEMENTADO (heredado).

### FX-REGIME-001 · Regímenes (Markov-switching)

**Identificación.** v2.0 · VIGENTE · MC-B01 · Mapa: área 8. Conservada del Bloque A.
**Perfiles y horizontes.** TRANSVERSAL · H2–H4.
**Propósito.** Probabilidad de régimen (expansión/contracción, calma/estrés) del ámbito o de su macro de referencia; insumo de RGM-B, de betas y correlaciones condicionadas y del Vigía.
**Entradas mínimas.** ≥ 100 observaciones para 2 estados (200 recomendadas).
**Método.** Hamilton con media y varianza por estado (AR opcional); EM con ≥ 10–20 arranques; probabilidades **filtradas**; duración `1/(1 − p_ii)`; RCM de Ang-Bekaert; HMM multivariante opcional.
**Parámetros.** estados (2); arranques (20).
**Salidas.** TABLA de parámetros; SERIE de probabilidades filtradas. `estimacion_estadistica`.
**Supuestos y limitaciones.** Probabilidades suavizadas prohibidas en señales y evaluación; número de estados mal identificado.
**Validaciones.** Probabilidades suman 1; dos regímenes simulados recuperados. Rechazo bajo mínimos.
**Tolerancia y semilla.** 1e-6 · entero del plan.
**Referencia ingenua.** RI-TB (régimen más frecuente).
**Referencias.** TMB-01 · DOC-MOT-0028.
**Prioridad y madurez.** P0 · IMPLEMENTADO (heredado).

### FX-VOL-001 · Volatilidad realizada

**Identificación.** v2.0 · VIGENTE · MC-B01 · Mapa: área 9. Conservada del Bloque A.
**Perfiles y horizontes.** TRANSVERSAL · H1–H3.
**Propósito.** Volatilidad del indicador del ámbito o de cada candidato (componente RI; escala 1–5; insumo de DER-VRP-001).
**Entradas mínimas.** ≥ 20 sesiones (≥ 60 recomendadas); OHLC si se pide un estimador de rango.
**Método.** Cierre a cierre; Parkinson; Garman-Klass; Rogers-Satchell; Yang-Zhang; EWMA (λ = 0,94); anualización por el `m` del perfil.
**Parámetros.** estimador (yang_zhang con OHLC; cierre sin OHLC); ventana (63 sesiones).
**Salidas.** VALOR o SERIE anualizada con IC. `estimacion_estadistica`.
**Supuestos y limitaciones.** Sin saltos de apertura en CRI; anualizar con `√m` supone iid.
**Validaciones.** Serie constante ⇒ 0; segunda vía EWMA. Rechazo con < 20 sesiones.
**Tolerancia y semilla.** 1e-8 · null.
**Referencia ingenua.** RI-UV (última volatilidad) como previsión.
**Referencias.** TMB-09, TMB-01.
**Prioridad y madurez.** P0 · IMPLEMENTADO (heredado).

### VOL-GARCH-001 · Volatilidad condicional GARCH

**Identificación.** v2.0 · VIGENTE · MC-B01 · Mapa: área 9. Conservada del Bloque A.
**Perfiles y horizontes.** TRANSVERSAL · H1–H3.
**Propósito.** Previsión de volatilidad y simulación histórica filtrada para colas (MC-B09).
**Entradas mínimas.** ≥ 500 observaciones diarias (1 000 recomendadas).
**Método.** GARCH(1,1), GJR o EGARCH con innovaciones t; previsión `E[σ²_{t+h}] = V_L + (α + β)^{h−1}(σ²_{t+1} − V_L)`; diagnóstico Ljung-Box de residuos estandarizados y sus cuadrados.
**Parámetros.** modelo (garch); distribucion (t).
**Salidas.** TABLA de parámetros con EE robustos; SERIE de varianza condicional; previsión por horizonte. `estimacion_estadistica`.
**Supuestos y limitaciones.** `α + β < 1`; persistencia cercana a 1 inestable.
**Validaciones.** Proceso simulado recuperado; segunda vía EWMA; evaluación con QLIKE. Rechazo bajo mínimos.
**Tolerancia y semilla.** 1e-6 · null.
**Referencia ingenua.** RI-UV.
**Referencias.** TMB-09 · DOC-MOT-0033, DOC-MOT-0210, DOC-MOT-0426.
**Prioridad y madurez.** P1 · IMPLEMENTADO (heredado).

### SER-HIER-001 · Conciliación jerárquica de previsiones

**Identificación.** v1.0 · VIGENTE · MC-B01 · Mapa: área 6.
**Perfiles y horizontes.** PERF-B-TEMA, PERF-B-SECT · H3–H4.
**Propósito.** Hacer coherentes las previsiones de segmentos (geografía × producto) y del total del ámbito.
**Entradas mínimas.** Previsiones base de todos los nodos con sus residuos históricos (≥ 12 periodos) y la matriz de agregación.
**Método.** (i) Matriz de sumas S. (ii) Covarianza de errores base (contracción). (iii) MinT `ỹ = S(SᵀW⁻¹S)⁻¹SᵀW⁻¹ŷ`. (iv) Incoherencia previa `‖ŷ_total − Σŷ_segmentos‖`.
**Parámetros.** estimador_W (contraccion | diagonal).
**Salidas.** TABLA de previsiones conciliadas y diferencias. `estimacion_estadistica`.
**Supuestos y limitaciones.** Previsiones base insesgadas; W mal estimada con pocos periodos.
**Validaciones.** Segmentos suman el total; jerarquía ya coherente no cambia. Rechazo sin residuos históricos.
**Tolerancia y semilla.** 1e-8 · null.
**Referencia ingenua.** Agregación ascendente simple.
**Referencias.** TMB-01 · MBM-0005, MBM-0006.
**Prioridad y madurez.** P2 · DOCUMENTADO.

### SER-FLOW-001 · Flujos, posicionamiento y sentimiento

**Identificación.** v1.0 · VIGENTE · MC-B01 (con MC-B07) · Mapa: área 10.
**Perfiles y horizontes.** PERF-B-SEGM, PERF-B-FACT, PERF-B-TEMA; SEL-FON (MO), SEL-DIV (alertas) · H1–H3.
**Propósito.** Medir flujos hacia el ámbito y sus vehículos, posicionamiento especulativo, posiciones cortas, revisiones y sentimiento (D10); insumos de MO en SEL-FON, de alertas de SEL-DIV y de la marca de saturación narrativa.
**Entradas mínimas.** Series semanales o mensuales ≥ 3 años (flujos, COT, cortos) con fecha de publicación.
**Método.** (i) Flujo relativo `F_t/AUM_{t−1}`, acumulados a 4, 13 y 26 semanas; separación de flujo y efecto mercado. (ii) Posición neta especulativa sobre interés abierto, percentil a 3 años e índice COT. (iii) Días para cubrir. (iv) Revisiones netas de BPA. (v) z robustos y percentiles; compuesto con pesos declarados.
**Parámetros.** ventana_percentil (156 semanas); pesos_compuesto (iguales).
**Salidas.** TABLA de métricas, percentiles y compuesto. `estimacion_estadistica` (compuesto con pesos de juicio: `juicio_experto`).
**Supuestos y limitaciones.** COT conocible el viernes con datos del martes; un vehículo grande domina la categoría.
**Validaciones.** Flujo + efecto mercado = ΔAUM. Rechazo sin fechas de publicación.
**Tolerancia y semilla.** 1e-8 · null.
**Referencia ingenua.** RI-PA para cualquier uso predictivo.
**Referencias.** TMB-01, TMB-12 · MBM-0239, MBM-0240; fuentes TFB-15 (RF-0049, RF-0053, RF-0345, MBF-0511).
**Prioridad y madurez.** P1 · DOCUMENTADO.

---
## 7. Fichas — MC-B02 Dimensionado de mercado y difusión

### MKT-DIM-001 · TAM, SAM y SOM por la vía descendente

**Identificación.** v1.0 · VIGENTE · MC-B02 · Mapa: área 11.
**Perfiles y horizontes.** PERF-B-TEMA, PERF-B-SECT, PERF-B-CADENA, PERF-B-GEO (sector ancla) · H3–H4.
**Propósito.** Estimar el tamaño del ámbito desde agregados (estadística oficial, población objetivo) y sus filtros hasta SAM y SOM; etapa 1 de la máquina de proyecciones (D2).
**Entradas mínimas.** Definición operativa del ámbito (incluye/excluye de producto, cliente, geografía, eslabón); agregado de partida con año, moneda, base y fuente (DAT-B); filtros con su justificación; cuota alcanzable y capacidad para SOM.
**Método.** (i) Agregado de partida y corrección de la clasificación oficial por exposición real. (ii) `TAM = población × adopción potencial × gasto por adoptante` o `gasto agregado × cuota de categoría`. (iii) `SAM = TAM × Π f_k`. (iv) `SOM = SAM × cuota_alcanzable`, con tope `capacidad × utilización × precio`. (v) Banda por propagación de la incertidumbre de cada factor (en logaritmos).
**Parámetros.** anio; moneda (EUR); precios (corrientes); base (valor final | valor añadido).
**Salidas.** TABLA: TAM, SAM, SOM con banda p10–p90 y los seis atributos (año, moneda, precios, base, geografía, fuente). Clase: la más débil de los factores.
**Supuestos y limitaciones.** Los filtros suelen ser juicios (`juicio_experto`); la clasificación oficial no es el ámbito.
**Validaciones.** `SOM ≤ SAM ≤ TAM`; coherencia con el gasto de los clientes o el PIB del sector; segunda vía MKT-DIM-002. Aclaración sin definición del ámbito; rechazo si falta alguno de los seis atributos.
**Tolerancia y semilla.** 1e-10 · null.
**Referencia ingenua.** RI-UV (último tamaño publicado) para previsiones de tamaño.
**Referencias.** TMB-02, TMB-03 · fuentes TFB-01 (MBF-0016, MBF-0007, RF-0021).
**Prioridad y madurez.** P0 · DOCUMENTADO.

### MKT-DIM-002 · TAM ascendente por demanda y por oferta

**Identificación.** v1.0 · VIGENTE · MC-B02 · Mapa: área 11.
**Perfiles y horizontes.** PERF-B-TEMA, PERF-B-SECT, PERF-B-CADENA · H3–H4.
**Propósito.** Estimar el tamaño sumando unidades × precio, usuarios × ARPU, parque × reposición × precio, o ingresos de segmento de los participantes más los no cotizados.
**Entradas mínimas.** Por demanda: unidades por segmento y precio medio con fecha; por oferta: ingresos de segmento de los participantes (≥ 60 % del mercado estimado cubierto) y método para el resto.
**Método.** (i) Suma por segmento. (ii) Por oferta, cotizados + privados (empleados × productividad del sector, capacidad × utilización × precio o cuota residual de asociación). (iii) **Control de doble cómputo**: valor final de la cadena o valor añadido del eslabón; nunca suma de ingresos de eslabones sucesivos. (iv) Consumo aparente `producción + importaciones − exportaciones` en mercados nacionales. (v) Banda por cobertura y por precio.
**Parámetros.** via (demanda | oferta | ambas); cobertura_min (0,60).
**Salidas.** TABLA por segmento con total, cobertura y banda. `estimacion_estadistica` (o `juicio_experto` si el resto no cotizado es de juicio).
**Supuestos y limitaciones.** Definiciones de segmento distintas entre empresas; precios de transferencia intragrupo.
**Validaciones.** Σ segmentos = total; doble cómputo comprobado; segunda vía MKT-DIM-001. Rechazo con cobertura < 0,60 sin método para el resto (`DATOS_INSUFICIENTES`) o con eslabones sucesivos sumados (`DATOS_INCOHERENTES`).
**Tolerancia y semilla.** 1e-10 · null.
**Referencia ingenua.** RI-UV.
**Referencias.** TMB-02 · fuentes TFB-07 (MBF-0201, MBF-0202, MBF-0203), TFB-05 (MBF-0036, MBF-0061), TFB-04.
**Prioridad y madurez.** P0 · DOCUMENTADO.

### MKT-TRI-001 · Triangulación y conciliación de tamaños

**Identificación.** v1.0 · VIGENTE · MC-B02 · Mapa: área 12.
**Perfiles y horizontes.** PERF-B-TEMA, PERF-B-SECT, PERF-B-CADENA · H3–H4.
**Propósito.** Conciliar varias estimaciones del tamaño con pesos por precisión, medir su discrepancia y decidir si cabe una cifra única.
**Entradas mínimas.** ≥ 2 estimaciones con incertidumbre (EE en logaritmos, rango p10–p90 o «±x %») y su raíz (independencia declarada por el Curador).
**Método.** (i) `σ_i` en logaritmos (`(ln p90 − ln p10)/2,563`; `ln(1 + x)/1,645`). (ii) Agrupar por raíz común. (iii) `ln T̂ = Σw_i ln T_i`, `w_i ∝ 1/(σ_i² + τ²)`; τ² de DerSimonian-Laird. (iv) Q de heterogeneidad; `D = max/min`. (v) Si `D > 1,5`, descomposición de la diferencia por perímetro y precio cuando hay definiciones.
**Parámetros.** efectos (aleatorios | fijos); umbral_D (1,5; 3).
**Salidas.** TABLA: conciliada con IC, D, Q, τ², pesos y diagnóstico de causa. `estimacion_estadistica`.
**Supuestos y limitaciones.** Raíces comunes ocultas inflan la precisión; las estimaciones de terceros sin método son [INTERPRETACIÓN].
**Validaciones.** Dos estimaciones iguales ⇒ misma cifra y varianza a la mitad (fijos). `D > 3` ⇒ rango sin cifra única (aviso para DSC-B).
**Tolerancia y semilla.** 1e-8 · null.
**Referencia ingenua.** Media geométrica equiponderada.
**Referencias.** TMB-02 (meta-análisis) · MBM-0037.
**Prioridad y madurez.** P0 · DOCUMENTADO.

### MKT-SEG-001 · Crecimiento por segmento, volumen y precio

**Identificación.** v1.0 · VIGENTE · MC-B02 · Mapa: área 13.
**Perfiles y horizontes.** PERF-B-TEMA, PERF-B-SECT, PERF-B-GEO · H3–H4.
**Propósito.** Descomponer el crecimiento del ámbito en segmentos, volumen y precio, y en efectos de *shift-share* geográficos; etapa 2 de la máquina.
**Entradas mínimas.** Series por segmento de valor y volumen (o precio) ≥ 5 periodos.
**Método.** `ΔV/V ≈ Δq/q + Δp/p + (Δq/q)(Δp/p)`; contribuciones `w_{s,0}·g_s`; *shift-share* (nacional, mezcla, competitivo); motor de ingresos (volumen × precio; usuarios × ARPU; capacidad × utilización).
**Parámetros.** base (periodo inicial); geografias.
**Salidas.** TABLA de contribuciones y efectos. `determinista` sobre datos dados.
**Supuestos y limitaciones.** Índices encadenados no aditivos (residuo declarado).
**Validaciones.** Σ contribuciones = crecimiento total ± residuo. Rechazo con segmentos que no suman el total.
**Tolerancia y semilla.** 1e-10 · null.
**Referencia ingenua.** RI-MH (crecimiento medio).
**Referencias.** TMB-02.
**Prioridad y madurez.** P1 · DOCUMENTADO.

### DIF-BASS-001 · Difusión de Bass

**Identificación.** v1.0 · VIGENTE · MC-B02 · Mapa: área 14. Desarrolla la parte de Bass de la ficha TEM-DIFF-001 del Bloque A.
**Perfiles y horizontes.** PERF-B-TEMA, PERF-B-CADENA · H3–H4.
**Propósito.** Estimar p, q y m de una adopción, su fase y su trayectoria con incertidumbre.
**Entradas mínimas.** Serie de primeras adopciones ≥ 8 periodos con un tramo de aceleración observado; m fijado por escenarios si la serie no ha pasado la inflexión.
**Método.** (i) Arranque con MCO discreto de Bass. (ii) NLS de Srinivasan-Mason sobre `m[F(t) − F(t − 1)]` con 20 arranques. (iii) Bayesiano con a prioris de DIF-ANLG-001 si n < 12. (iv) Pico `t* = ln(q/p)/(p + q)`, fase por `F(t)`. (v) Bandas por bootstrap de residuos (por bloques si autocorrelados) y por escenarios de m. (vi) Validación fuera de muestra en el último 20 %.
**Parámetros.** m (estimado | escenarios); arranques (20); B (1 000).
**Salidas.** TABLA: p, q, m con EE, t*, fase, error fuera de muestra; SERIE p10–p50–p90. `estimacion_estadistica` (`juicio_experto` si m es de escenarios).
**Supuestos y limitaciones.** Datos truncados antes del pico subestiman m (Van den Bulte-Lilien); ventas totales incluyen reposición.
**Validaciones.** Bass sintético (p = 0,03; q = 0,38; m = 100) recuperado con ≥ 15 puntos tras el pico; segunda vía DIF-LOG-001. Rechazo sin tramo de aceleración (`SUPUESTOS_VIOLADOS`).
**Tolerancia y semilla.** 1e-6 · entero del plan.
**Referencia ingenua.** Extrapolación lineal del crecimiento reciente y crecimiento constante (RI-MH).
**Referencias.** TMB-03 · DOC-MOT-0106, DOC-MOT-0433, DOC-MOT-0436, DOC-MOT-0444, DOC-MOT-0445, DOC-MOT-0112.
**Prioridad y madurez.** P1 · DOCUMENTADO.

### DIF-LOG-001 · Logística, Gompertz y sustitución tecnológica

**Identificación.** v1.0 · VIGENTE · MC-B02 · Mapa: área 14.
**Perfiles y horizontes.** PERF-B-TEMA, PERF-B-CADENA · H3–H4.
**Propósito.** Ajustar curvas S a series de penetración o cuota de sustitución y proyectarlas.
**Entradas mínimas.** Serie de penetración ≥ 8 periodos con aceleración observada.
**Método.** Logística `m/[1 + e^{−k(t − t0)}]`; Gompertz `m·exp(−b·e^{−ct})`; Fisher-Pry `ln[f/(1 − f)] = k(t − t0)`; selección por AICc y error fuera de muestra; bandas por bootstrap y escenarios de m.
**Parámetros.** modelo (auto); m (estimado | escenarios).
**Salidas.** TABLA de parámetros, inflexión, tiempo 10→90 %; SERIE con bandas. `estimacion_estadistica` o `juicio_experto`.
**Supuestos y limitaciones.** Las curvas extrapolan mal lejos de los datos; ningún modelo domina.
**Validaciones.** Logística sintética recuperada; segunda vía Bass. Rechazo sin aceleración.
**Tolerancia y semilla.** 1e-6 · entero del plan.
**Referencia ingenua.** Extrapolación lineal.
**Referencias.** TMB-03 · DOC-MOT-0441, DOC-MOT-0442, DOC-MOT-0440, MBM-0039.
**Prioridad y madurez.** P1 · DOCUMENTADO.

### DIF-GEN-001 · Generaciones sucesivas y sustitución (Norton-Bass)

**Identificación.** v1.0 · VIGENTE · MC-B02 · Mapa: área 14.
**Perfiles y horizontes.** PERF-B-TEMA · H4.
**Propósito.** Modelizar tecnologías con generaciones que se canibalizan (estándares, nodos, químicas de baterías).
**Entradas mínimas.** Series por generación ≥ 6 periodos de la generación más antigua; fechas de lanzamiento.
**Método.** Norton-Bass con p y q comunes y m por generación; ventas de la generación g como su adopción menos la sustitución por g + 1; estimación NLS conjunta.
**Parámetros.** generaciones; q_comun (true).
**Salidas.** SERIE por generación con bandas. `estimacion_estadistica`.
**Supuestos y limitaciones.** Parámetros comunes entre generaciones; pocas generaciones observadas.
**Validaciones.** Suma de generaciones = total. Rechazo con una sola generación observada.
**Tolerancia y semilla.** 1e-6 · entero del plan.
**Referencia ingenua.** Bass agregado (DIF-BASS-001).
**Referencias.** TMB-03 · DOC-MOT-0435.
**Prioridad y madurez.** P2 · DOCUMENTADO.

### DIF-ANLG-001 · Analogías y a prioris de difusión

**Identificación.** v1.0 · VIGENTE · MC-B02 · Mapa: área 15.
**Perfiles y horizontes.** PERF-B-TEMA · H4.
**Propósito.** Proporcionar a prioris de p, q y velocidad de adopción desde clases de referencia y meta-análisis cuando la serie es corta.
**Entradas mínimas.** Producto o tecnología con atributos de similitud declarados (precio relativo, infraestructura, red, regulación).
**Método.** (i) A prioris del meta-análisis de Sultan, Farley y Lehmann (medias p ≈ 0,03, q ≈ 0,38) o de análogos de la base CHAT. (ii) Selección de análogos por similitud declarada. (iii) Distribución a priori (lognormal) con dispersión del meta-análisis. (iv) Sensibilidad al análogo.
**Parámetros.** analogos; peso_meta (0,5).
**Salidas.** TABLA de a prioris y su dispersión. `juicio_experto`.
**Supuestos y limitaciones.** La difusión depende de época y país; análogos discutibles.
**Validaciones.** Retroprevisión de un caso conocido con sus análogos. Rechazo sin atributos de similitud.
**Tolerancia y semilla.** 1e-8 · null.
**Referencia ingenua.** Medias del meta-análisis.
**Referencias.** TMB-03 · DOC-MOT-0436, DOC-MOT-0107, MBM-0040, MBM-0041, MBM-0043, MBM-0046.
**Prioridad y madurez.** P1 · DOCUMENTADO.

---

### DIF-H5-001 · Proyección estructural H5: curvas S de largo plazo, sustitución e hitos (V2.1)

**Identificación.** v1.0 · VIGENTE · MC-B02 (con MC-B04 y MC-B08) · Mapa: área 79.
**Perfiles y horizontes.** PERF-B-TEMA, PERF-B-CADENA, PERF-B-SECT, PERF-B-GEO · H5 (5–30 años).
**Propósito.** Trayectorias estructurales de adopción, sustitución tecnológica, TAM a largo plazo o variables demográficas para la tesis H5 (8.6 del Documento 0), con bandas que se ensanchan con el horizonte y **hitos intermedios verificables** para su evaluación (12.8).
**Entradas mínimas.** Serie de adopción o cuota (≥ 6 observaciones) o análogos (DIF-ANLG-001); techo `m` con su fundamento (restricción física, demográfica, presupuestaria o de análogos); curva de costes o de aprendizaje si la sustitución depende del coste (SUP-LRN-002); escenarios de Prospectiva.
**Método.** (i) Ajuste de Bass, logística o Gompertz con a priori de análogos si no hay inflexión observada; sustitución de Fisher-Pry `f/(1−f) = e^{k(t−t₀)}` o Norton-Bass por generaciones. (ii) Distribución de parámetros por bootstrap o bayesiana; trayectorias p10–p50–p90 por escenario (base, favorable, adverso) con SIM-MC-001. (iii) Contraste de coste: fecha de paridad con la tecnología incumbente por curva de experiencia distributiva. (iv) **Hitos**: para cada tesis, ≥ 3 valores de la trayectoria base en fechas entre 1 y 5 años con su tolerancia, su serie resoluble y su marca `critico`; para cada hito, su valor bajo la **extrapolación lineal** (RI-LIN) y la separación entre ambos (un hito que no discrimina entre la tesis y la ingenua se marca `no_discriminante`).
**Parámetros.** modelo (BASS | LOGISTICA | GOMPERTZ | FISHER_PRY | NORTON_BASS); n_hitos (≥ 3); tolerancia_hito (por defecto ±10 % del valor base); n (10 000).
**Salidas.** SERIE de trayectorias con bandas; TABLA de hitos (fecha, valor base, tolerancia, valor ingenuo, discriminante sí/no, crítico sí/no). `estimacion_estadistica` (`juicio_experto` si el techo o los parámetros proceden de juicio). **Sin probabilidades numéricas publicables** (R13): las frecuencias de la simulación se entregan como bandas verbales.
**Supuestos y limitaciones.** Antes de la inflexión, `m` y `q` están mal identificados (DOC-MOT-0445); el error de previsión crece con el horizonte (DOC-MOT-0111); los techos son la variable más incierta; una curva S cierta puede ser mala inversión si el precio la descuenta (contraste obligatorio con VAL-REV-001).
**Validaciones.** Trayectoria monótona y acotada por `m`; suma de cuotas de tecnologías sustitutas ≤ 1; hitos dentro de las bandas de su propio escenario; rechazo si no hay techo fundamentado (`DATOS_INSUFICIENTES`) o si se pide una probabilidad numérica H5 (`PROBABILIDAD_NO_CERTIFICABLE`).
**Tolerancia y semilla.** 1e-6 · entero del plan.
**Referencia ingenua.** RI-LIN.
**Referencias.** TMB-03, TMB-05, TMB-08 · DOC-MOT-0106, DOC-MOT-0434, DOC-MOT-0435, DOC-MOT-0445, DOC-MOT-0112, DOC-MOT-0110, DOC-MOT-0111, DOC-MOT-0428, MBM-0047.
**Prioridad y madurez.** P1 · DOCUMENTADO.

## 8. Fichas — MC-B03 Organización industrial

### IO-CONC-001 · Concentración (HHI, CRn, N_eq, ΔHHI)

**Identificación.** v1.0 · VIGENTE · MC-B03 · Mapa: área 16.
**Perfiles y horizontes.** PERF-B-SECT, PERF-B-CADENA, PERF-B-TEMA; SEL-IDX (concentración del índice) · H3–H4.
**Propósito.** Medir la concentración del mercado o del eslabón (D1, D4, sub-bloque 4a) y de los índices candidatos.
**Entradas mínimas.** Mercado definido (producto, geografía, eslabón, base); cuotas o magnitudes base de los participantes con fecha; cuota de la franja.
**Método.** (i) Cuotas en %; franja explícita. (ii) `HHI = Σs_i²`, `N_eq = 10 000/HHI`, `CR_n`, entropía. (iii) Cotas `HHI_min` (franja atomizada) y `HHI_max` (franja en empresas del tamaño de la menor). (iv) `ΔHHI = 2·s_a·s_b` si se pide. (v) Segunda base (capacidad o unidades).
**Parámetros.** base (ingresos); n_CR (4).
**Salidas.** TABLA con cotas y referencias de umbrales (EE. UU. 2023; Comisión Europea). `determinista` con banda.
**Supuestos y limitaciones.** La definición del mercado domina el resultado; importaciones fuera de la cuota doméstica.
**Validaciones.** Σs = 100 % con franja; n iguales ⇒ 10 000/n. Aclaración sin definición; rechazo con cuotas reescaladas sin franja.
**Tolerancia y semilla.** 1e-10 · null.
**Referencia ingenua.** RI-NA.
**Referencias.** TMB-04 · MBM-0089, MBM-0090, MBM-0091, MBM-0092, DOC-MOT-0515, ANA-DOC-0454.
**Prioridad y madurez.** P0 · DOCUMENTADO.

### IO-LERN-001 · Índice de Lerner, márgenes precio-coste y markups

**Identificación.** v1.0 · VIGENTE · MC-B03 · Mapa: área 17.
**Perfiles y horizontes.** PERF-B-SECT, PERF-B-CADENA · H4.
**Propósito.** Estimar el poder de mercado del sector o eslabón (componente «ventaja estructural» de A; D4, D8).
**Entradas mínimas.** Ingresos, coste de ventas y gastos variables por empresa ≥ 3 años; para markups de producción, activos e inputs variables en panel ≥ 5 años.
**Método.** (i) PCM contable. (ii) Markup de producción `μ = θ^V·PQ/(P^V V)` con θ^V por función de producción (Ackerberg-Caves-Frazer). (iii) Lerner teórico `HHI/(10 000·|ε|)` como contraste con elasticidad de ECO-ELAS-001.
**Parámetros.** metodo (pcm | produccion | ambos).
**Salidas.** TABLA por empresa y agregada (ponderada por ventas) con IC. `estimacion_estadistica`.
**Supuestos y limitaciones.** El PCM contable no es el Lerner económico; costes fijos altos; composición del agregado.
**Validaciones.** L ∈ [0; 1); Cournot simétrico ⇒ `1/(n|ε|)`. Rechazo sin costes variables (PCM aproximado por margen bruto con limitación).
**Tolerancia y semilla.** 1e-6 · null.
**Referencia ingenua.** RI-MH (margen medio histórico).
**Referencias.** TMB-04 · MBM-0069, MBM-0070, MBM-0071, MBM-0072, MBM-0081, MBM-0085, MBM-0086, MBM-0088, MBM-0093.
**Prioridad y madurez.** P1 · DOCUMENTADO.

### IO-MARG-001 · Márgenes y captura de valor por eslabón

**Identificación.** v1.0 · VIGENTE · MC-B03 · Mapa: área 18.
**Perfiles y horizontes.** PERF-B-CADENA, PERF-B-SECT, PERF-B-TEMA · H3–H4.
**Propósito.** Cuantificar dónde se captura el valor en la cadena (sub-bloque 4a, D8; etapa 3 de la máquina).
**Entradas mínimas.** Por eslabón: ingresos y margen operativo de los participantes con cobertura declarada; o valor añadido de tablas input-output.
**Método.** (i) *Profit pool* `π_k = ingresos_k × margen_k`. (ii) Cuota en beneficio frente a cuota en ingresos. (iii) ROIC por eslabón frente a WACC (con MC-B06). (iv) Matriz eslabón × {HHI, margen, intensidad de capital, utilización, crecimiento}.
**Parámetros.** margen (EBIT | EBITDA).
**Salidas.** TABLA por eslabón con cobertura. `estimacion_estadistica`.
**Supuestos y limitaciones.** Los cotizados no son el eslabón (sesgo de selección); conglomerados con segmentos mezclados.
**Validaciones.** Σ π_k = beneficio total de la cadena. Aclaración si la cobertura < 50 %.
**Tolerancia y semilla.** 1e-10 · null.
**Referencia ingenua.** RI-NA.
**Referencias.** TMB-04, TMB-10 · MBM-0219.
**Prioridad y madurez.** P0 · DOCUMENTADO.

### IO-SHARE-001 · Estabilidad y rotación de cuotas

**Identificación.** v1.0 · VIGENTE · MC-B03 · Mapa: área 19.
**Perfiles y horizontes.** PERF-B-SECT, PERF-B-CADENA · H4.
**Propósito.** Medir la dinámica competitiva (persistencia del liderazgo, competencia por el mercado).
**Entradas mínimas.** Cuotas de un mismo mercado definido en ≥ 2 fechas separadas k años (≥ 5 recomendados).
**Método.** Hymer-Pashigian `½·Σ|s_{i,t} − s_{i,t−k}|`; Spearman de rangos; probabilidad de persistencia del líder; entradas y salidas del top-5; volatilidad de cuota.
**Parámetros.** k (5).
**Salidas.** TABLA. `determinista` (descriptivo); IC por bootstrap si hay serie.
**Supuestos y limitaciones.** Cambios de perímetro del mercado entre fechas.
**Validaciones.** Cuotas idénticas ⇒ I = 0. Rechazo con definiciones distintas entre fechas.
**Tolerancia y semilla.** 1e-10 · null.
**Referencia ingenua.** RI-UV (cuotas constantes).
**Referencias.** TMB-04 · MBM-0082, MBM-0083.
**Prioridad y madurez.** P1 · DOCUMENTADO.

### IO-PROF-001 · Persistencia de la rentabilidad

**Identificación.** v1.0 · VIGENTE · MC-B03 · Mapa: área 19.
**Perfiles y horizontes.** PERF-B-SECT; SEL-RV (QL) · H4.
**Propósito.** Estimar la velocidad de convergencia del ROIC hacia la media o el WACC (supuesto del valor terminal; calidad del candidato).
**Entradas mínimas.** Panel de ROIC ≥ 10 años (≥ 6 para matriz de transición).
**Método.** (i) AR(1) de Mueller `π_it = α_i + λ_i·π_{i,t−1} + ε`; nivel `α/(1 − λ)`; semivida `ln 0,5/ln λ`. (ii) Corrección de Nickell o GMM si T < 15. (iii) Matriz de transición entre quintiles como alternativa.
**Parámetros.** ventana (10 años).
**Salidas.** TABLA: λ con IC, nivel permanente, semivida; matriz. `estimacion_estadistica`.
**Supuestos y limitaciones.** Supervivencia en el panel (empresas que desaparecen); cambios contables.
**Validaciones.** AR(1) simulado recuperado. Rechazo con T < 6.
**Tolerancia y semilla.** 1e-6 · null.
**Referencia ingenua.** RI-MH (reversión inmediata a la media).
**Referencias.** TMB-04, TMB-02 · MBM-0025, MBM-0026, MBM-0028.
**Prioridad y madurez.** P1 · DOCUMENTADO.

### IO-BARG-001 · Poder de negociación con clientes y proveedores

**Identificación.** v1.0 · VIGENTE · MC-B03 · Mapa: área 20.
**Perfiles y horizontes.** PERF-B-CADENA, PERF-B-SECT; SEL-RV (RI) · H3–H4.
**Propósito.** Cuantificar la dependencia de clientes y proveedores del eslabón o del candidato.
**Entradas mínimas.** Cuotas de los mayores clientes y proveedores (notas de clientes significativos, segmentos); duración de contratos si se conoce.
**Método.** Cuota de los 5 mayores clientes; HHI de clientes y de proveedores; peso del insumo en el coste del cliente; índice compuesto con z robustos y pesos declarados.
**Parámetros.** pesos_compuesto (iguales).
**Salidas.** TABLA. `estimacion_estadistica` (compuesto con pesos de juicio: `juicio_experto`).
**Supuestos y limitaciones.** Divulgación parcial; umbrales de divulgación distintos por jurisdicción.
**Validaciones.** Cuotas ≤ 100 %. Rechazo sin ningún dato de concentración.
**Tolerancia y semilla.** 1e-10 · null.
**Referencia ingenua.** RI-NA.
**Referencias.** TMB-04 · fuentes TFB-03 (RF-0002), TFB-07 (MBF-0201).
**Prioridad y madurez.** P2 · DOCUMENTADO.

---

### VC-DESG-001 · Desglose jerárquico de la cadena de valor y atractivo del eslabón AE (V2.1)

**Identificación.** v1.0 · VIGENTE · MC-B03 (con MC-B04 para capacidad y MC-B09 para input-output) · Mapa: área 76.
**Perfiles y horizontes.** PERF-B-CADENA, PERF-B-SECT, PERF-B-TEMA; obligatoria en todo ámbito con D4 en P2 o P3 (8.4 del Documento 0) · H3–H5.
**Propósito.** Construir el árbol de eslabones `ESL-` (macro-eslabón → sub-eslabón → actividad → insumo o nodo crítico; 8.7.1), conciliar tamaños y márgenes entre niveles, detectar márgenes anómalos frente a eslabones adyacentes y calcular los insumos y la réplica de **AE** (9.12) para el `mapa_cadena_valor` (B.16) y la puerta PV3.
**Entradas mínimas.** Por nodo: padre, nivel, actores con cuota y periodo, ingresos o valor añadido, margen bruto y operativo (por segmento publicado), capacidad y utilización (si existen), concentración de proveedores y por país, plazos de entrega, sustitutos; componentes de AE en múltiplos de 10 con su ancla y evidencia (los aporta AG-B03 con AG-B05 y AG-B06); pesos de AE vigentes en F10.
**Método.** (i) **Árbol** con identificadores estables y profundidad según el nivel (Anexo A: N1 eslabón crítico hasta actividad; N2 eslabones del plan hasta actividad e insumos críticos de los eslabones con cuello; N3 hasta insumo). (ii) **Conciliación jerárquica**: tamaño del padre frente a Σ hijos (en valor añadido, no en ingresos brutos encadenados, para evitar doble cómputo); diferencia `d = (padre − Σ hijos)/padre` declarada; reconciliación MinT opcional cuando hay varias fuentes por nivel. (iii) Por nodo: HHI y CRn de actores (IO-CONC-001), HHI de proveedores y cuota del primer país (NET-EXPO-001), margen y ROIC (IO-MARG-001), poder de negociación (IO-BARG-001). (iv) **Margen anómalo**: `Δm_k = m_k − media(m_adyacentes)` en puntos porcentuales (insumo del indicador de 8.7.2; ámbar > +5 pp, rojo > +10 pp). (v) **AE** `= round(Σ w_c·c_c / Σ w_c)` con los seis componentes (crecimiento de la demanda del eslabón 20; margen y ROIC frente a adyacentes 20; poder de negociación y barreras 15; cuello favorable 20 con el PCB escalado de VC-BOT-001 a múltiplo de 10; expectativas descontadas en el eslabón, inversa, 15; riesgo de sustitución o desintermediación, inversa, 10); `atractivo = AE ≥ 60`. (vi) Sensibilidad de AE a ±5 puntos en cada peso (marca `frontera_AE` si cruza 60).
**Parámetros.** profundidad (N1 | N2 | N3); base_conciliacion (VALOR_ANADIDO | INGRESOS con advertencia); umbral_AE (60, de F10).
**Salidas.** TABLA por eslabón (métricas de B.16, `Δm_k`, conciliación, AE con desglose y `frontera_AE`); árbol en formato estructurado para HT-04. `estimacion_estadistica` (componentes de AE: `juicio_experto` anclado). AE replica HT-03 con igualdad exacta (`DISCREPANCIA_HT03` si no).
**Supuestos y limitaciones.** Las empresas cotizadas no son el eslabón (sesgo de selección); los conglomerados mezclan eslabones (asignación por segmento publicado o estimada con método declarado); AE ordena eslabones dentro del ámbito y **no sustituye a A**.
**Validaciones.** Cada nodo con padre existente salvo los macro-eslabones; `ESL-00` en objetos sin cadena; Σ cuotas por nodo ≤ 100 %; diferencia de conciliación > 20 % sin explicación ⇒ advertencia obligatoria; caso de control con una cadena de tres niveles de tamaños conocidos.
**Tolerancia y semilla.** 1e-10 · null.
**Referencia ingenua.** RI-NA.
**Referencias.** TMB-04, TMB-10, TMB-13 · MBM-0219, MBM-0226, MBM-0005, MBM-0254, MBM-0202.
**Prioridad y madurez.** P0 · DOCUMENTADO.

## 9. Fichas — MC-B04 Oferta y costes

### SUP-COST-001 · Curva de costes de la industria y coste marginal

**Identificación.** v1.0 · VIGENTE · MC-B04 · Mapa: área 21.
**Perfiles y horizontes.** PERF-B-CADENA, PERF-B-SEGM, PERF-B-SECT; SEL-MP (VA) · H3–H4.
**Propósito.** Construir la curva de costes, el coste marginal a la demanda, sus percentiles y el precio incentivo (D3; VA de SEL-MP).
**Entradas mínimas.** Por productor o activo: capacidad y coste unitario (C1 o coste sostenido) con año y moneda; demanda prevista.
**Método.** (i) Orden ascendente por coste; capacidad acumulada. (ii) Cruce con la demanda: productor marginal. (iii) Percentiles 50, 75, 90 ponderados por capacidad. (iv) Precio incentivo con WACC sectorial. (v) Sensibilidad a demanda ±10 %, tipo de cambio ±10 %, energía ±20 %.
**Parámetros.** coste (c1 | sostenido | total); wacc (de VAL-WACC-001).
**Salidas.** TABLA y SERIE escalonada; coste marginal; percentiles; precio incentivo. `estimacion_estadistica`.
**Supuestos y limitaciones.** Costes publicados con retraso; coproductos; precio ≠ coste.
**Validaciones.** Capacidad acumulada final = Σ capacidades. Rechazo con años o monedas mezclados sin conversión.
**Tolerancia y semilla.** 1e-10 · null.
**Referencia ingenua.** RI-UV (precio actual) para cualquier uso como previsión.
**Referencias.** TMB-05 · fuentes TFB-12 (RF-0356, RF-0059, MBF-0248).
**Prioridad y madurez.** P1 · DOCUMENTADO.

### SUP-UTIL-001 · Utilización, capacidad y balance

**Identificación.** v1.0 · VIGENTE · MC-B04 · Mapa: área 22.
**Perfiles y horizontes.** PERF-B-CADENA, PERF-B-SECT, PERF-B-SEGM · H3–H4.
**Propósito.** Medir utilización y proyectar el balance oferta-demanda con la tubería de capacidad (D3; etapa 2 de la máquina).
**Entradas mínimas.** Capacidad efectiva y producción ≥ 3 años; tubería de proyectos con fase y fecha; demanda por escenario.
**Método.** `U = producción/capacidad efectiva`; capacidad futura ponderada por probabilidad de fase (por defecto 0,3/0,6/0,85/0,95, sustituible por la tasa histórica del sector); balance `B_t = Σ cap·U_max·P(entrada) − D_t`.
**Parámetros.** U_max (0,90); probabilidades_fase.
**Salidas.** SERIE de utilización y balance por escenario. `estimacion_estadistica` (`juicio_experto` si las probabilidades de fase son de juicio).
**Supuestos y limitaciones.** Capacidad nominal ≠ efectiva; anuncios duplicados; cierres omitidos.
**Validaciones.** U ∈ [0; 1]; producción ≤ capacidad. Rechazo sin capacidad efectiva ni método para estimarla.
**Tolerancia y semilla.** 1e-10 · null.
**Referencia ingenua.** RI-UV (utilización actual).
**Referencias.** TMB-05 · MBM-0067, MBM-0068.
**Prioridad y madurez.** P1 · DOCUMENTADO.

### SUP-BOTT-001 · Identificación de cuellos de botella

**Identificación.** v1.0 · VIGENTE · MC-B04 · Mapa: área 23.
**Perfiles y horizontes.** PERF-B-CADENA, PERF-B-TEMA · H3–H4.
**Propósito.** Identificar el eslabón que limita la cadena, su holgura y su persistencia (sub-bloque 4d).
**Entradas mínimas.** Por eslabón: capacidad y coeficiente técnico `a_k` por unidad de producto final; indicadores de tensión (utilización, plazos, márgenes, proveedores capaces).
**Método.** (i) `Y_max = min_k(cap_k/a_k)`; argumento del mínimo. (ii) Holgura `(cap_k/a_k)/D_final − 1` por eslabón. (iii) Indicadores de tensión (≥ 2 de: U > 90 %, plazos crecientes, margen > media de 5 años, ≤ 3 proveedores). (iv) Persistencia `plazo × probabilidad de entrada` frente al crecimiento de la demanda (simulación en SIM-BOTT-001).
**Parámetros.** umbral_U (0,90); proveedores_max (3).
**Salidas.** TABLA por eslabón: holgura, tensión, cuello sí/no, persistencia estimada. `estimacion_estadistica`.
**Supuestos y limitaciones.** Coeficientes fijos; sustitutos y rutas alternativas (si existen, programación lineal de máximo flujo).
**Validaciones.** Cadena de tres eslabones con cuello conocido identificada. Aclaración sin coeficientes (solo indicadores de tensión, declarado).
**Tolerancia y semilla.** 1e-10 · null.
**Referencia ingenua.** RI-NA.
**Referencias.** TMB-05, TMB-10 · MBM-0219, MBM-0225.
**Prioridad y madurez.** P0 · DOCUMENTADO.

### VC-BOT-001 · Indicadores de cuello en semáforo y puntuación PCB (V2.1)

**Identificación.** v1.0 · VIGENTE · MC-B04 (con MC-B08 para la persistencia simulada) · Mapa: área 77.
**Perfiles y horizontes.** PERF-B-CADENA, PERF-B-SECT, PERF-B-TEMA; obligatoria en todo ámbito con D4 en P2 o P3 · H3–H5.
**Propósito.** **Medir** (no afirmar) si un eslabón es cuello de botella con los nueve indicadores de 8.7.2 y calcular la puntuación **PCB** (9.12), su materialidad y su señal de resolución, para el `mapa_cadena_valor`, la puerta PV3 y AE (VC-DESG-001).
**Entradas mínimas.** Por eslabón candidato, cada indicador con dato, fecha y fuente (DAT-B): utilización; plazos de entrega frente a su media de 5 años; book-to-bill trimestral; HHI de proveedores; cuota del primer país; `Δm_k` de VC-DESG-001; precio spot/contrato; tiempo de construcción de nueva capacidad frente al plazo hasta el déficit (de SUP-UTIL-001 o SIM-BOTT-001); plazos de permisos y cualificaciones; inventarios en percentil de 5 años; insumo sin sustituto (D5). Relevancia para el valor (1–5) con su argumento (AG-B03). Umbrales vigentes de F10.
**Método.** (i) **Semáforo** por indicador con los umbrales ámbar/rojo del Anexo A (utilización 85–90 % / > 90 %; plazos > 1,5× / > 2×; book-to-bill > 1,1 dos trimestres / > 1,2 cuatro; HHI 1 500–2 500 / > 2 500; primer país > 40 % / > 60 %; margen sobre adyacentes > +5 / > +10 pp; spot/contrato > 1,15 / > 1,3; nueva capacidad: ámbar si iguala el plazo hasta el déficit, rojo si lo supera; permisos > 12 / > 24 meses; inventarios < p25 / < p10; insumo sin sustituto: rojo); sin dato ⇒ `SIN_DATO` (nunca verde). (ii) **Severidad** 1–5: 1 ninguno en rojo; 2 un rojo o ≥ 3 ámbar; 3 dos rojos; 4 tres o cuatro rojos; 5 ≥ 5 rojos, o insumo sin sustituto con utilización > 95 %. (iii) **Persistencia** 1–5 por el tiempo esperado hasta cerrar el déficit (< 6 meses; 6–12; 1–2 años; 2–4; > 4), con la distribución de SIM-BOTT-001 cuando hay tubería de proyectos (se usa la mediana; p80 como sensibilidad). (iv) **PCB** `= round(100·sev·pers·rel/125)`; **material** si PCB ≥ 30 y ≥ 2 rojos. (v) **Control de doble cómputo**: matriz de correlación de los indicadores de demanda (plazos, book-to-bill, spot/contrato) en la historia del eslabón; si dos tienen ρ > 0,8, la severidad se calcula también contándolos como uno y se declara la diferencia. (vi) **Señal de resolución**: el indicador cuyo cruce de vuelta a ámbar es más probable primero, con su umbral observable.
**Parámetros.** umbrales (F10); rho_dup (0,8); usar_simulacion (sí si hay tubería).
**Salidas.** TABLA por eslabón: indicadores con valor, estado y fuente; severidad, persistencia, relevancia, PCB, `material`, `causa` (capacidad, tecnología, regulación, geopolítica, materia prima), señal de resolución, severidad sin doble cómputo. `estimacion_estadistica` (relevancia: `juicio_experto` anclado). PCB replica HT-03 con igualdad exacta.
**Supuestos y limitaciones.** Umbrales generales que pueden no ajustarse a industrias con utilización estructuralmente alta (declarar); la capacidad «anunciada» no es capacidad (solo cuenta con permisos y financiación); un cuello que no altera tesis ni escenarios está mal analizado o no lo es (8.7).
**Validaciones.** Caso de control con indicadores sintéticos de severidad conocida (0, 2 y 5 rojos); PCB máximo 100 con 5·5·5; `material` falso con PCB ≥ 30 y un solo rojo; rechazo si la relevancia no tiene argumento (`ACLARACION_REQUERIDA`).
**Tolerancia y semilla.** 1e-10 (1e-6 con simulación) · entero del plan si usa SIM-BOTT-001.
**Referencia ingenua.** RI-UV (persistencia del estado actual del indicador) para la señal de resolución.
**Referencias.** TMB-05, TMB-10, TMB-13 · MBM-0219, MBM-0225, MBM-0254, MBM-0204; laguna declarada en F8 sobre métodos de identificación de cuellos (Mapa, TMB-05).
**Prioridad y madurez.** P0 · DOCUMENTADO.

### SUP-LRN-001 · Curva de aprendizaje (Wright)

**Identificación.** v1.0 · VIGENTE · MC-B04 · Mapa: área 24.
**Perfiles y horizontes.** PERF-B-TEMA, PERF-B-CADENA · H4.
**Propósito.** Estimar la tasa de aprendizaje de una tecnología y la trayectoria de su coste unitario (D3, D5; precio en el TAM en valor).
**Entradas mínimas.** Serie de coste (o precio con margen estable declarado) y producción acumulada con ≥ 3 duplicaciones.
**Método.** (i) `ln C = ln C_1 − b·ln x + u` con HAC o en diferencias. (ii) `LR = 1 − 2^{−b}` con IC por el método delta. (iii) Dos factores (I+D) opcional. (iv) Segunda vía Moore e identidad de Sahal `b ≈ m/g`. (v) Proyección con escenario de producción.
**Parámetros.** factores (1 | 2); escenario_produccion.
**Salidas.** TABLA: b, LR con IC, rango observado; SERIE proyectada. `estimacion_estadistica`.
**Supuestos y limitaciones.** Confusión con escala, insumos y márgenes; extrapolación fuera del rango sin suelo físico.
**Validaciones.** Wright sintético (b = 0,322) recuperado. Rechazo con < 3 duplicaciones.
**Tolerancia y semilla.** 1e-6 · null.
**Referencia ingenua.** RI-UV (coste constante) y tendencia exponencial (Moore).
**Referencias.** TMB-05 · DOC-MOT-0109, DOC-MOT-0110, DOC-MOT-0430, DOC-MOT-0431, MBM-0049, MBM-0050, MBM-0052, MBM-0063.
**Prioridad y madurez.** P1 · DOCUMENTADO.

### SUP-LRN-002 · Previsión tecnológica probabilística (Nagy, Farmer-Lafond, Way)

**Identificación.** v1.0 · VIGENTE · MC-B04 · Mapa: área 25.
**Perfiles y horizontes.** PERF-B-TEMA · H4.
**Propósito.** Intervalos de previsión calibrados del coste de una tecnología a varios años.
**Entradas mínimas.** Serie anual de coste ≥ 15 años (o producción acumulada para la versión de Wright).
**Método.** (i) Paseo aleatorio con deriva y ruido MA(1): `y_{t+1} = y_t − μ + v_t + θv_{t−1}`. (ii) Estimación de μ, σ, θ. (iii) Distribución del error a horizonte τ con su fórmula y corrección por θ. (iv) Versión de Wright con escenarios de producción (Way et al.). (v) Retroprevisión con origen móvil y cobertura empírica del 90 %.
**Parámetros.** version (moore | wright); horizonte (≤ 10 años).
**Salidas.** SERIE p10–p50–p90; cobertura empírica. `estimacion_estadistica`.
**Supuestos y limitaciones.** Ritmos históricos no garantizados (desaceleración de Moore en semiconductores); cambios de tecnología.
**Validaciones.** Cobertura empírica del 90 % en retroprevisión en [80 %; 97 %] o advertencia. Rechazo con < 15 años.
**Tolerancia y semilla.** 1e-6 · entero del plan.
**Referencia ingenua.** RI-UV (coste constante).
**Referencias.** TMB-05 · DOC-MOT-0110, DOC-MOT-0111, DOC-MOT-0428, MBM-0047, MBM-0065.
**Prioridad y madurez.** P2 · DOCUMENTADO.

### SUP-INV-001 · Inventarios frente a norma estacional

**Identificación.** v1.0 · VIGENTE · MC-B04 · Mapa: área 26. Desarrolla CMD-INV-001 del Bloque A.
**Perfiles y horizontes.** PERF-B-SEGM; SEL-MP (VA) · H2–H3.
**Propósito.** Medir la tensión física del mercado por inventarios (D3; VA de SEL-MP).
**Entradas mínimas.** Inventarios y consumo ≥ 5 años semanales o mensuales con fecha de publicación.
**Método.** Desviación frente a la media estacional de 5 años y z frente a su desviación estacional; días de cobertura; relación con la estructura de la curva (CMD-CURVE-001) como contraste.
**Parámetros.** ventana (5 años).
**Salidas.** SERIE de desviación, z y cobertura. `estimacion_estadistica`.
**Supuestos y limitaciones.** Inventarios no observados; rupturas de cobertura de la estadística.
**Validaciones.** Serie igual a su media estacional ⇒ z = 0. Rechazo con < 3 años.
**Tolerancia y semilla.** 1e-8 · null.
**Referencia ingenua.** RI-EST.
**Referencias.** TMB-05, TMB-01 · fuentes TFB-12 (RF-0059, RF-0065, RF-0062).
**Prioridad y madurez.** P1 · DOCUMENTADO.

---

## 10. Fichas — MC-B05 Econometría y macro-sector

### ECO-ELAS-001 · Elasticidades precio y renta

**Identificación.** v1.0 · VIGENTE · MC-B05 · Mapa: área 27.
**Perfiles y horizontes.** PERF-B-SECT, PERF-B-TEMA, PERF-B-SEGM · H3–H4.
**Propósito.** Estimar la respuesta de la demanda al precio y a la renta, a corto y largo plazo (D2; proyección del TAM; estrés de demanda).
**Entradas mínimas.** Serie de cantidad, precio y renta ≥ 30 observaciones; instrumentos si se pide VI.
**Método.** (i) Diagnóstico de integración. (ii) Log-log por MCO-HAC (descriptivo). (iii) VI con desplazadores de oferta (F de primera etapa > 10; Hansen J). (iv) ARDL con prueba de límites; `θ = Σβ/(1 − Σφ)` con método delta. (v) A priori de meta-análisis si no hay identificación (declarado).
**Parámetros.** identificacion (mco | vi | ardl | meta); rezagos (BIC).
**Salidas.** TABLA: ε_p, ε_y corto y largo con IC; diagnósticos. `estimacion_estadistica` (`juicio_experto` si es a priori).
**Supuestos y limitaciones.** Sin instrumento, la elasticidad es descriptiva; cambios estructurales de la demanda.
**Validaciones.** Datos simulados con endogeneidad: MCO sesgado, VI recupera; segunda vía ARDL frente a MCE. Rechazo con < 30 observaciones sin a priori.
**Tolerancia y semilla.** 1e-6 · null.
**Referencia ingenua.** Elasticidad mediana del meta-análisis correspondiente.
**Referencias.** TMB-02 · DOC-MOT-0239, DOC-MOT-0046, MBM-0014, MBM-0016, MBM-0019, MBM-0021, MBM-0033, MBM-0034, MBM-0035, MBM-0036, MBM-0037.
**Prioridad y madurez.** P1 · DOCUMENTADO.

### ECO-PANEL-001 · Paneles sectoriales

**Identificación.** v1.0 · VIGENTE · MC-B05 · Mapa: área 28.
**Perfiles y horizontes.** PERF-B-SECT, PERF-B-GEO · H3–H4.
**Propósito.** Estimar relaciones en paneles de empresas, subsectores o países (márgenes sobre ciclo e insumos; difusión entre países).
**Entradas mínimas.** Panel con N ≥ 20 entidades y T ≥ 5.
**Método.** Efectos fijos de entidad y tiempo; Hausman; errores agrupados; Driscoll-Kraay con dependencia transversal (prueba CD); GMM en sistema con T < 15 y regresor retardado (instrumentos < grupos; AR(2); Hansen).
**Parámetros.** efectos (fijos); errores (cluster | driscoll_kraay); gmm (false).
**Salidas.** TABLA de coeficientes con EE robustos y diagnósticos. `estimacion_estadistica`.
**Supuestos y limitaciones.** Supervivencia en el panel; proliferación de instrumentos en GMM.
**Validaciones.** Panel simulado con efecto conocido; segunda vía primeras diferencias. Rechazo con N < 20 o T < 5.
**Tolerancia y semilla.** 1e-6 · null.
**Referencia ingenua.** RI-NA.
**Referencias.** TMB-02 · DOC-MOT-0232, MBM-0025, MBM-0026, MBM-0027, MBM-0029, MBM-0030, MBM-0032.
**Prioridad y madurez.** P1 · DOCUMENTADO.

### ECO-CYC-001 · Betas al ciclo y sensibilidad a tipos

**Identificación.** v1.0 · VIGENTE · MC-B05 · Mapa: área 29.
**Perfiles y horizontes.** PERF-B-SECT, PERF-B-GEO, PERF-B-SEGM; SEL-RV (RI) · H2–H4.
**Propósito.** Medir la sensibilidad del ámbito (o del candidato) al mercado, al ciclo (PMI, PIB), a tipos e inflación, y la ciclicidad de beneficios (D7, D8).
**Entradas mínimas.** Rentabilidades mensuales ≥ 60 (36 mínimo) y factores alineados; BPA trimestral ≥ 20 para la beta de beneficios.
**Método.** (i) Regresión multifactorial con HAC. (ii) Ventanas rodantes de 60 meses. (iii) Betas por régimen filtrado (FX-REGIME-001). (iv) Beta de beneficios; apalancamiento operativo y financiero. (v) Duración de la renta variable.
**Parámetros.** factores (mercado, ΔPMI, Δy, Δπ^e); ventana (60).
**Salidas.** TABLA de betas con IC por ventana y régimen. `estimacion_estadistica`.
**Supuestos y limitaciones.** Inestabilidad entre regímenes; datos macro revisados.
**Validaciones.** Betas simuladas recuperadas; segunda vía muestra completa. Rechazo con < 36 meses.
**Tolerancia y semilla.** 1e-6 · null.
**Referencia ingenua.** Beta = 1 frente al mercado; betas a factores = 0.
**Referencias.** TMB-02, TMB-01 · DOC-MOT-0041, DOC-MOT-0028; fuentes TFB-04 (RF-0318, RF-0319), TFB-02 (RF-0001).
**Prioridad y madurez.** P0 · DOCUMENTADO.

### ECO-LP-001 · Proyecciones locales (respuestas a impulsos)

**Identificación.** v1.0 · VIGENTE · MC-B05 · Mapa: área 30.
**Perfiles y horizontes.** PERF-B-GEO, PERF-B-SECT · H3–H4.
**Propósito.** Trazar la respuesta del ámbito a un choque identificado (tipos, precio de la energía, demanda externa) a varios horizontes.
**Entradas mínimas.** Serie del choque identificado y de la respuesta ≥ 80 observaciones.
**Método.** Para cada h: `y_{t+h} − y_{t−1} = α_h + β_h·choque_t + Γ_h'controles + u`; HAC con `L ≥ h`; bandas al 90 %; VAR como segunda vía.
**Parámetros.** h_max (12); controles (rezagos 4).
**Salidas.** SERIE de β_h con bandas. `estimacion_estadistica`.
**Supuestos y limitaciones.** La identificación del choque es del solicitante y se declara; varianza mayor que VAR.
**Validaciones.** Proceso simulado con IRF conocida. Rechazo sin identificación declarada.
**Tolerancia y semilla.** 1e-6 · null.
**Referencia ingenua.** Respuesta nula.
**Referencias.** TMB-02 · DOC-MOT-0044.
**Prioridad y madurez.** P2 · DOCUMENTADO.

### ECO-GRANG-001 · Causalidad de Granger con cautela declarada

**Identificación.** v1.0 · VIGENTE · MC-B05 · Mapa: área 31.
**Perfiles y horizontes.** TRANSVERSAL · H2–H4.
**Propósito.** Contrastar precedencia predictiva entre series (indicadores adelantados del ámbito).
**Entradas mínimas.** Series estacionarias (o Toda-Yamamoto) ≥ 60 observaciones.
**Método.** VAR con rezagos por BIC; prueba de Wald de exclusión; Toda-Yamamoto con rezagos extra en I(1); corrección de Holm sobre el conjunto de pruebas.
**Parámetros.** rezagos (BIC); correccion (holm).
**Salidas.** TABLA: estadísticos, p ajustados, etiqueta «precedencia estadística, no mecanismo». `estimacion_estadistica`.
**Supuestos y limitaciones.** Variables omitidas; expectativas; frecuencia de muestreo.
**Validaciones.** Proceso con precedencia conocida detectada. Rechazo con series no estacionarias sin Toda-Yamamoto.
**Tolerancia y semilla.** 1e-6 · null.
**Referencia ingenua.** RI-NA.
**Referencias.** TMB-02 · DOC-MOT-0240.
**Prioridad y madurez.** P2 · DOCUMENTADO.

### FX-COINT-001 · Cointegración y corrección de errores

**Identificación.** v2.0 · VIGENTE · MC-B05 · Mapa: área 31. Conservada del Bloque A.
**Perfiles y horizontes.** TRANSVERSAL · H3–H4.
**Propósito.** Relaciones de equilibrio de largo plazo (precio de una materia prima y su sustituto; BEER; spread y fundamentales).
**Entradas mínimas.** Series I(1) confirmadas ≥ 60 observaciones.
**Método.** Engle-Granger (valores críticos de MacKinnon) y Johansen (traza y máximo autovalor); MCE con velocidad de ajuste y semivida.
**Parámetros.** metodo (johansen | eg); rezagos (BIC).
**Salidas.** TABLA: vectores, α con IC, semivida. `estimacion_estadistica`.
**Supuestos y limitaciones.** Rupturas no modeladas; muestras cortas.
**Validaciones.** Residuos I(0); par cointegrado simulado recuperado. Rechazo entre series I(0) (`SUPUESTOS_VIOLADOS`).
**Tolerancia y semilla.** 1e-6 · null.
**Referencia ingenua.** RI-PA.
**Referencias.** TMB-02 · DOC-MOT-0039, DOC-MOT-0040, DOC-MOT-0240.
**Prioridad y madurez.** P1 · IMPLEMENTADO (heredado).

### ECO-EXPO-001 · Exposición del candidato al factor del ámbito

**Identificación.** v1.0 · VIGENTE · MC-B05 · Mapa: área 32.
**Perfiles y horizontes.** SEL-DIV, SEL-MP, SEL-TCV (pureza); SEL-RV (segunda vía de pureza) · H2–H4.
**Propósito.** Medir cuánto se mueve cada candidato con el factor del ámbito (pureza por sensibilidad; PC2 en DIV, MP y TCV).
**Entradas mínimas.** Rentabilidades semanales ≥ 104 (o mensuales ≥ 60) del candidato, del mercado y del factor, alineadas.
**Método.** (i) Factor ortogonalizado respecto al mercado y sin el candidato si pesa en él. (ii) `r_i = α + β_m r_m + β_f f + u` con HAC. (iii) R² incremental del factor. (iv) Estabilidad por ventanas y regímenes. (v) MP: correlación con la referencia física; TCV: fracción de varianza y DV01 del tramo. (vi) Rentabilidades no sincrónicas: semanales o retardos de Dimson.
**Parámetros.** frecuencia (semanal); ventana (2 años).
**Salidas.** TABLA por candidato: β_f con IC, p, R² incremental, signo frente a la tesis, estabilidad. `estimacion_estadistica`.
**Supuestos y limitaciones.** Relaciones dependientes del régimen; sobreestimación en conglomerados de beta alta.
**Validaciones.** Exposición simulada recuperada; segunda vía mensual. Rechazo con < 52 semanas.
**Tolerancia y semilla.** 1e-6 · null.
**Referencia ingenua.** β_f = 0.
**Referencias.** TMB-02, TMB-07 · DOC-MOT-0041.
**Prioridad y madurez.** P0 · DOCUMENTADO.

---
## 11. Fichas — MC-B06 Valoración sectorial y de candidatos

Regla común de las fichas de esta sección: toda valoración de un **candidato** sale con `uso: para_ordenacion`, supuestos de coste de capital y horizonte comunes a su universo y banda de sensibilidad; nunca es un precio objetivo (R7).

### VAL-DCF-001 · DCF del agregado y de candidatos (para ordenar)

**Identificación.** v1.0 · VIGENTE · MC-B06 · Mapa: área 33. Desarrolla ACC-VAL-001 del Bloque A.
**Perfiles y horizontes.** PERF-B-SECT, PERF-B-TEMA, PERF-B-GEO; SEL-RV (VA) · H3–H4.
**Propósito.** Valor por flujos del agregado del ámbito (D9; etapa 4 de la máquina) y valor relativo de los candidatos de un universo.
**Entradas mínimas.** Agregados contables ≥ 3 ejercicios (5 recomendados) con fecha de presentación; capitalización y deuda neta a la fecha de corte; WACC (VAL-WACC-001); premisas de crecimiento y márgenes con su DAT-B o CALC-B.
**Método.** (i) FCFF = NOPAT − inversión neta. (ii) Fases: explícita (5 años; 10 en temáticas), convergencia lineal, terminal. (iii) Terminal por fórmula de impulsores de valor `NOPAT_{n+1}(1 − g/RONIC)/(WACC − g)` con RONIC = WACC por defecto. (iv) Beneficios normalizados en cíclicos. (v) Candidatos: mismo modelo y supuestos; salida `valor/precio − 1` y percentil. (vi) Sensibilidad WACC ±1 pp × g ±0,5 pp; peso del terminal.
**Parámetros.** anios_explicitos (5; 3–10); g_terminal (≤ crecimiento nominal de largo plazo; 0–4 % en EUR); RONIC (= WACC).
**Salidas.** TABLA: EV, valor del capital, peso del terminal, matriz de sensibilidad; por candidato, brecha relativa y percentil (`para_ordenacion`). `estimacion_estadistica` si las premisas son estimaciones; `juicio_experto` si son escenarios de juicio.
**Supuestos y limitaciones.** No es precio objetivo; terminal > 85 % ⇒ advertencia; coherencia g = reinversión × RONIC.
**Validaciones.** Σ VP + VP(VT) = EV; perpetuidad con g = 0 ⇒ FCF/WACC; segunda vía VAL-MULT-001. Rechazo con g ≥ WACC, < 3 ejercicios o monedas inconsistentes.
**Tolerancia y semilla.** 1e-8 · null.
**Referencia ingenua.** Valor = precio de mercado (la señal es la brecha); RI-EQ en rankings.
**Referencias.** TMB-06 · MBM-0095, MBM-0100, MBM-0104, DOC-MOT-0054, DOC-MOT-0314.
**Prioridad y madurez.** P0 · DOCUMENTADO.

### VAL-REV-001 · DCF inverso y brecha de expectativas

**Identificación.** v1.0 · VIGENTE · MC-B06 · Mapa: área 34.
**Perfiles y horizontes.** PERF-B-SECT, PERF-B-TEMA, PERF-B-GEO; SEL-RV (VA) · H3–H4.
**Propósito.** ¿Qué crecimiento, margen o duración de la ventaja descuenta el precio y cuánto difiere de lo plausible? (componente «valoración frente a expectativas» de A; etapa 5 de la máquina; VA de SEL-RV).
**Entradas mínimas.** Las de VAL-DCF-001 y la distribución del crecimiento plausible (de VAL-PROJ-001 o MKT-* con SIM-MC-001).
**Método.** (i) Resolver `g*` (o `M*`, o duración) con `DCF(g*) = EV` por Brent (tolerancia 1e-6, monotonicidad comprobada). (ii) Brecha `Δg = g* − g_plausible,p50`; `z = Δg/σ_plausible`; `P(g_plausible ≥ g*)`. (iii) Banda por WACC ±1 pp y g terminal ±0,5 pp. (iv) Segunda vía: margen implícito con g = p50; coste de capital implícito.
**Parámetros.** variable (crecimiento | margen | duracion); rango_busqueda (−10 %; 40 %).
**Salidas.** TABLA: implícito con banda, brecha, z, probabilidad. `estimacion_estadistica` (o `juicio_experto` por herencia).
**Supuestos y limitaciones.** El implícito depende del WACC; la brecha hereda la incertidumbre del plausible.
**Validaciones.** DCF(g*) reproduce el precio; precio generado con g conocido recuperado. `SIN_RESULTADO` si no hay raíz en el rango.
**Tolerancia y semilla.** 1e-6 · null (entero del plan si hay simulación del plausible).
**Referencia ingenua.** Brecha nula.
**Referencias.** TMB-06 · MBM-0098, MBM-0099, MBM-0102, MBM-0103, MBM-0107.
**Prioridad y madurez.** P0 · DOCUMENTADO.

### VAL-MULT-001 · Múltiplos relativos y bandas de comparables

**Identificación.** v1.0 · VIGENTE · MC-B06 · Mapa: área 35.
**Perfiles y horizontes.** PERF-B-SECT, PERF-B-GEO, PERF-B-TEMA; SEL-RV, SEL-IDX, SEL-FON (VA) · H3–H4.
**Propósito.** Valoración relativa del agregado frente a su historia y al mercado, y de cada candidato frente a sus comparables.
**Entradas mínimas.** Precios a la fecha de corte; beneficios adelantados con fecha de consenso o realizados; ≥ 10 años de historia para percentiles; ≥ 8 comparables por subgrupo (≥ 20 para regresión).
**Método.** (i) Agregación armónica. (ii) Percentil y z frente a 10 años (20 recomendados) y frente al mercado. (iii) Múltiplos justificados (`P/VC = (ROE − g)/(r − g)`; `EV/NOPAT = (1 − g/RONIC)/(WACC − g)`). (iv) Regresión transversal en el subgrupo `ln(múltiplo) = a + b·margen + c·g + d·riesgo + u`; residuo estandarizado del candidato. (v) Exclusiones (BN ≤ 0; EV en financieras).
**Parámetros.** multiplo (PER_adelantado | EV/EBITDA | EV/Ventas | P/VC | P/AFFO | FCF_yield); ventana (10 años).
**Salidas.** TABLA: múltiplos, percentiles, z, residuos (`para_ordenacion` en candidatos). `estimacion_estadistica`.
**Supuestos y limitaciones.** Concentración del agregado; beneficios de pico de ciclo; consenso optimista.
**Validaciones.** Armónica ≤ aritmética; segunda vía VAL-DCF-001. Rechazo con < 8 comparables (percentil del universo con advertencia).
**Tolerancia y semilla.** 1e-8 · null.
**Referencia ingenua.** RI-MH (reversión al múltiplo medio) para usos predictivos.
**Referencias.** TMB-06 · MBM-0096, MBM-0101, MBM-0106, DOC-MOT-0052.
**Prioridad y madurez.** P0 · DOCUMENTADO.

### VAL-ROIC-001 · ROIC − WACC y beneficio económico

**Identificación.** v1.0 · VIGENTE · MC-B06 · Mapa: área 36.
**Perfiles y horizontes.** PERF-B-SECT, PERF-B-CADENA; SEL-RV (QL) · H4.
**Propósito.** ¿Crea valor el ámbito o el candidato y cuán estable es? (D8; calidad del crecimiento de A; QL de SEL-RV).
**Entradas mínimas.** NOPAT y capital invertido ≥ 5 ejercicios; WACC sectorial.
**Método.** `ROIC = NOPAT/capital invertido` (con y sin fondo de comercio); capitalización opcional de I+D y arrendamientos; diferencial y beneficio económico; dispersión (rango intercuartílico) y estabilidad (σ a 5 años) del sector; persistencia con IO-PROF-001.
**Parámetros.** fondo_comercio (con | sin | ambos); capitalizar_ID (false).
**Salidas.** TABLA por candidato y agregada. `determinista` sobre datos; `estimacion_estadistica` con WACC estimado.
**Supuestos y limitaciones.** Normas contables distintas; intangibles no capitalizados.
**Validaciones.** ROIC × capital = NOPAT. Rechazo con < 3 ejercicios.
**Tolerancia y semilla.** 1e-10 · null.
**Referencia ingenua.** RI-MH (ROIC medio del sector).
**Referencias.** TMB-06 · MBM-0095, MBM-0104.
**Prioridad y madurez.** P0 · DOCUMENTADO.

### VAL-WACC-001 · Coste de capital sectorial (método de Damodaran)

**Identificación.** v1.0 · VIGENTE · MC-B06 · Mapa: área 37.
**Perfiles y horizontes.** PERF-B-SECT, PERF-B-GEO, PERF-B-TEMA · H3–H4.
**Propósito.** WACC del sector o del agregado con banda, común a todo el universo de un ranking.
**Entradas mínimas.** Betas de las empresas del sector (o tabla sectorial de Damodaran con fecha); D/E y tipo impositivo; r_f en la moneda de los flujos; ERP; CRP y exposición por ingresos.
**Método.** (i) Desapalancar (Hamada). (ii) Mediana sectorial y corrección por caja. (iii) Reapalancar a la estructura objetivo. (iv) `r_e = r_f + β·ERP + λ·CRP`. (v) `r_d` por calificación sintética (cobertura de intereses). (vi) WACC y banda (β ± EE; ERP ± 1 pp).
**Parámetros.** estructura (mediana sectorial); ERP (implícita vigente).
**Salidas.** TABLA: β_U, β_L, r_e, r_d, WACC con banda. `estimacion_estadistica`.
**Supuestos y limitaciones.** El error estándar del coste de capital de una industria suele superar 3 puntos (Fama-French); betas inestables.
**Validaciones.** D/E = 0 ⇒ β_L = β_U; segunda vía coste de capital implícito. Rechazo sin r_f en la moneda.
**Tolerancia y semilla.** 1e-8 · null.
**Referencia ingenua.** RI-NA.
**Referencias.** TMB-06 · MBM-0097, DOC-MOT-0053, DOC-MOT-0054, DOC-MOT-0340, DOC-MOT-0071; fuente TFB-07 (RF-0050).
**Prioridad y madurez.** P0 · DOCUMENTADO.

### VAL-PROJ-001 · Máquina de proyecciones: de TAM a capitalización implícita

**Identificación.** v1.0 · VIGENTE · MC-B06 (con MC-B02, MC-B04, MC-B08) · Mapa: área 38.
**Perfiles y horizontes.** PERF-B-TEMA, PERF-B-SECT, PERF-B-CADENA · H4.
**Propósito.** Encadenar las cinco etapas de 8.8 del Documento 0 con premisas falsables registradas y propagar la incertidumbre de extremo a extremo.
**Entradas mínimas.** Premisas por etapa con valor, fuente o fundamento, distribución y condición de invalidación; precio a la fecha de corte.
**Método.** (1) Mercado (MKT-*, DIF-*). (2) Agregado: ingresos por segmento con su motor. (3) Márgenes y caja coherentes con D8 y D4. (4) Valor implícito con múltiplos de salida anclados a comparables reales y DCF (p10–p50–p90 con SIM-MC-001 y SIM-IC-001). (5) Contraste con el precio (VAL-REV-001). Saneo entre etapas.
**Parámetros.** escenarios (base, favorable, adverso); n (10 000).
**Salidas.** TABLA por etapa y escenario; DISTRIBUCION de la capitalización implícita; brecha. Clase: la más débil de las premisas críticas.
**Supuestos y limitaciones.** Sin premisa no hay cifra; múltiplos de salida no anclados están prohibidos.
**Validaciones.** SOM ≤ SAM ≤ TAM; márgenes dentro del rango histórico o justificados; g < WACC. Rechazo con premisas sin fuente ni condición de invalidación.
**Tolerancia y semilla.** 1e-6 · entero del plan.
**Referencia ingenua.** Capitalización actual (RI-UV) y crecimiento histórico del agregado (RI-MH).
**Referencias.** TMB-06, TMB-08, TMB-03.
**Prioridad y madurez.** P0 · DOCUMENTADO.

### ACC-ERP-001 · Prima de riesgo implícita

**Identificación.** v2.0 · VIGENTE · MC-B06 · Mapa: área 37. Conservada del Bloque A.
**Perfiles y horizontes.** PERF-B-GEO, PERF-B-SECT · H3–H4.
**Propósito.** ERP implícita del mercado o región (coste de capital; atractivo relativo del mercado geográfico).
**Entradas mínimas.** Nivel del índice, dividendos y recompras de 12 meses, crecimiento esperado a 5 años, r_f.
**Método.** TIR que iguala el nivel del índice a los flujos al accionista (crecimiento explícito y terminal = r_f), menos r_f; histórica como contraste.
**Parámetros.** g_5a (consenso o tendencia); terminal (r_f).
**Salidas.** VALOR con banda y percentil histórico. `estimacion_estadistica`.
**Supuestos y limitaciones.** Sensible al crecimiento supuesto.
**Validaciones.** Flujos descontados a la TIR = nivel. Rechazo sin recompras ni dividendos.
**Tolerancia y semilla.** 1e-8 · null.
**Referencia ingenua.** RI-MH (ERP histórica).
**Referencias.** TMB-06 · DOC-MOT-0053, DOC-MOT-0315, DOC-MOT-0316.
**Prioridad y madurez.** P1 · DOCUMENTADO.

### IDX-ERP-001 · Rentabilidad esperada por componentes (Grinold-Kroner)

**Identificación.** v2.0 · VIGENTE · MC-B06 · Mapa: área 37. Conservada del Bloque A.
**Perfiles y horizontes.** PERF-B-GEO; SEL-IDX (VA) · H4.
**Propósito.** Rentabilidad esperada a largo plazo de un mercado o índice en EUR (D9 de MERCADO_GEOGRAFICO; VA de SEL-IDX).
**Entradas mínimas.** Rentabilidad por dividendo, recompras netas, inflación esperada, crecimiento real del BPA, CAPE o PER y supuesto de reversión.
**Método.** `E[R] ≈ D/P − ΔS + i + g_real + ΔPE` (anual); efecto de divisa esperado declarado (o cero); CAPE con ajuste por composición sectorial.
**Parámetros.** reversion_PE (0 por defecto; parcial declarada).
**Salidas.** TABLA por componente y total con banda. `estimacion_estadistica` o `juicio_experto` (ΔPE).
**Supuestos y limitaciones.** ΔPE es juicio; composiciones distintas sesgan comparaciones de CAPE.
**Validaciones.** Suma de componentes = total. Rechazo sin rentabilidad por dividendo.
**Tolerancia y semilla.** 1e-10 · null.
**Referencia ingenua.** RI-MH (rentabilidad histórica del índice).
**Referencias.** TMB-06 · DOC-MOT-0509, DOC-MOT-0052; fuente TFB-06 (RF-0052).
**Prioridad y madurez.** P1 · DOCUMENTADO.

### VAL-RF-001 · Rentabilidad esperada neta de pérdida esperada, carry y rolldown

**Identificación.** v1.0 · VIGENTE · MC-B06 · Mapa: área 39.
**Perfiles y horizontes.** PERF-B-SEGM; SEL-RF (VA) · H2–H4.
**Propósito.** Valor relativo de emisiones de bonos para ordenar (VA de SEL-RF).
**Entradas mínimas.** Precio o rendimiento a la fecha de corte, cupón, vencimiento, prelación, calificación; curva de referencia; PD y LGD por calificación y prelación.
**Método.** (i) Rendimiento y duración. (ii) Pérdida esperada anual `PD·LGD`. (iii) Rentabilidad esperada neta `y − PD·LGD`. (iv) Carry `y − r_financiación`; rolldown por la pendiente de la curva del emisor o del segmento. (v) Rentabilidad de equilibrio `carry/duración`. (vi) Percentil del universo (`para_ordenacion`).
**Parámetros.** horizonte (12 meses); fuente_PD (tablas de calificación | Merton).
**Salidas.** TABLA por emisión. `estimacion_estadistica`.
**Supuestos y limitaciones.** PD por calificación es media histórica; opcionalidad (usar OAS).
**Validaciones.** Precio reconstruido desde el rendimiento. Rechazo sin curva de referencia.
**Tolerancia y semilla.** 1e-8 · null.
**Referencia ingenua.** RI-EQ (media del universo) en rankings.
**Referencias.** TMB-06, TMB-09.
**Prioridad y madurez.** P1 · DOCUMENTADO.

### FIR-SPREAD-001 · Diferencial de crédito: percentil y valor relativo

**Identificación.** v2.0 · VIGENTE · MC-B06 · Mapa: área 39. Conservada del Bloque A y ampliada a emisiones.
**Perfiles y horizontes.** PERF-B-SEGM; SEL-RF (VA) · H2–H4.
**Propósito.** Situar el diferencial del segmento o de una emisión frente a su historia y frente a la curva de su calificación y sector.
**Entradas mínimas.** Serie de diferenciales ≥ 5 años (segmento) o diferencial actual y curva de calificación y sector (emisión).
**Método.** Percentil y z a 5 años; diferencial frente a la curva ajustada de su calificación y sector (residuo en pb y en σ); OAS si hay opcionalidad.
**Parámetros.** tipo_diferencial (OAS | Z | G).
**Salidas.** TABLA. `estimacion_estadistica`.
**Supuestos y limitaciones.** Referencias de diferencial distintas no son comparables.
**Validaciones.** Percentil ∈ [0; 100]. Rechazo con referencias mezcladas.
**Tolerancia y semilla.** 1e-8 · null.
**Referencia ingenua.** RI-MH.
**Referencias.** TMB-06 · fuentes TFB-06 (RF-0660, RF-0667).
**Prioridad y madurez.** P1 · DOCUMENTADO.

### FX-CARRY-001 · Carry de divisas ajustado por volatilidad

**Identificación.** v2.0 · VIGENTE · MC-B06 · Mapa: área 39. Conservada del Bloque A.
**Perfiles y horizontes.** SEL-DIV (VA), SEL-MON · H1–H3.
**Propósito.** Carry del par frente a EUR y carry por unidad de volatilidad.
**Entradas mínimas.** Tipos a corto de ambas divisas o puntos *forward*; volatilidad (FX-VOL-001).
**Método.** `carry = i_divisa − i_EUR` (o por puntos *forward*); carry/σ; percentil del universo de pares.
**Parámetros.** plazo (3 meses).
**Salidas.** TABLA. `determinista` (carry) y `estimacion_estadistica` (ajustado).
**Supuestos y limitaciones.** Colapsos del carry en episodios de aversión al riesgo.
**Validaciones.** Paridad cubierta. Rechazo con sentido del par no declarado.
**Tolerancia y semilla.** 1e-10 · null.
**Referencia ingenua.** RI-PA.
**Referencias.** TMB-06, TMB-07 · DOC-MOT-0065.
**Prioridad y madurez.** P1 · IMPLEMENTADO (heredado).

### FX-PPA-001 · Desviación de PPA relativa

**Identificación.** v2.0 · VIGENTE · MC-B06 · Mapa: área 39. Conservada del Bloque A.
**Perfiles y horizontes.** SEL-DIV (VA); PERF-B-GEO · H4.
**Propósito.** Desviación del tipo de cambio real frente a su media de largo plazo.
**Entradas mínimas.** Tipo de cambio e índices de precios ≥ 15 años.
**Método.** Tipo real `q = s + p* − p`; desviación frente a su media y z; semivida de reversión (AR(1)).
**Parámetros.** indice_precios (IPC).
**Salidas.** TABLA. `estimacion_estadistica`.
**Supuestos y limitaciones.** Semividas de 3–5 años; efecto Balassa-Samuelson.
**Validaciones.** Coherencia de signos. Rechazo con < 10 años.
**Tolerancia y semilla.** 1e-8 · null.
**Referencia ingenua.** RI-PA.
**Referencias.** TMB-06 · fuente TFB-01 (FXF-0058).
**Prioridad y madurez.** P1 · IMPLEMENTADO (heredado).

### FX-BEER-001 · Tipo de cambio real de equilibrio (BEER)

**Identificación.** v2.0 · VIGENTE · MC-B06 · Mapa: área 39. Conservada del Bloque A.
**Perfiles y horizontes.** SEL-DIV (VA); PERF-B-GEO · H4.
**Propósito.** Desalineamiento del tipo real frente a fundamentales.
**Entradas mínimas.** Tipo real, productividad relativa, términos de intercambio, activos exteriores netos ≥ 15 años.
**Método.** Cointegración (FX-COINT-001) del tipo real sobre fundamentales; desalineamiento = observado − ajustado; IC por bootstrap.
**Parámetros.** fundamentales (declarados).
**Salidas.** TABLA. `estimacion_estadistica`.
**Supuestos y limitaciones.** Especificación sensible; rupturas.
**Validaciones.** Residuos I(0). Rechazo sin cointegración.
**Tolerancia y semilla.** 1e-6 · null.
**Referencia ingenua.** RI-PA.
**Referencias.** TMB-02, TMB-06 · fuente TFB-05 (FXF-0053).
**Prioridad y madurez.** P2 · DOCUMENTADO.

### CMD-CURVE-001 · Estructura de la curva de futuros y roll yield

**Identificación.** v2.0 · VIGENTE · MC-B06 · Mapa: área 39. Conservada del Bloque A.
**Perfiles y horizontes.** SEL-MP, SEL-DER (VA) · H1–H4.
**Propósito.** *Contango* o *backwardation*, roll yield y *convenience yield* implícito del contrato o del ETC.
**Entradas mínimas.** Precios de ≥ 3 vencimientos a la fecha de corte; tipo de interés; coste de almacenamiento si se pide el *convenience yield*.
**Método.** Pendiente anualizada; roll yield `≈ (F_1/F_2 − 1)` anualizado; `y = r + u − (1/T)·ln(F/S)`; percentil histórico; para ETC sobre futuros, coste de roll según su metodología.
**Parámetros.** vencimientos (1–2); regla_enlace.
**Salidas.** TABLA. `determinista` (curva) y `estimacion_estadistica` (percentiles).
**Supuestos y limitaciones.** Estacionalidad de la curva (gas, agrícolas).
**Validaciones.** Coherencia de signos con inventarios (SUP-INV-001). Rechazo con < 2 vencimientos.
**Tolerancia y semilla.** 1e-10 · null.
**Referencia ingenua.** RI-UV.
**Referencias.** TMB-06 · fuentes TFB-12 (RF-0059, RF-0065).
**Prioridad y madurez.** P1 · IMPLEMENTADO (heredado).

### REI-NAV-001 · Prima o descuento sobre NAV

**Identificación.** v2.0 · VIGENTE · MC-B06 · Mapa: área 39. Conservada del Bloque A y ampliada a candidatos.
**Perfiles y horizontes.** SEL-INM (VA) · H3–H4.
**Propósito.** Descuento o prima de cada REIT, SOCIMI o inmobiliaria frente a su NAV EPRA y frente a su historia.
**Entradas mínimas.** NAV EPRA (NTA) con fecha; precio a la fecha de corte; historia ≥ 5 años.
**Método.** `P/NAV − 1`; z frente a su media; ajuste por antigüedad del NAV (declarado).
**Parámetros.** tipo_NAV (NTA).
**Salidas.** TABLA (`para_ordenacion`). `estimacion_estadistica`.
**Supuestos y limitaciones.** NAV por tasación retrasada.
**Validaciones.** Signos coherentes. Rechazo con NAV de > 12 meses.
**Tolerancia y semilla.** 1e-10 · null.
**Referencia ingenua.** RI-MH.
**Referencias.** TMB-06 · fuentes TFB-13 (RF-0069, RF-0068).
**Prioridad y madurez.** P1 · DOCUMENTADO.

### REI-CAP-001 · Cap rate implícito y diferencial con el bono

**Identificación.** v2.0 · VIGENTE · MC-B06 · Mapa: área 39. Conservada del Bloque A.
**Perfiles y horizontes.** SEL-INM (VA) · H3–H4.
**Propósito.** Rentabilidad inmobiliaria implícita en la cotización frente a transacciones y tipos.
**Entradas mínimas.** NOI, EV y activos no operativos con fecha; cap rates de transacciones del subsector; bono a 10 años.
**Método.** `cap implícito = NOI/(EV − activos no operativos)`; diferencial con transacciones y con el bono; percentil.
**Parámetros.** NOI (próximos 12 meses | último).
**Salidas.** TABLA (`para_ordenacion`). `estimacion_estadistica`.
**Supuestos y limitaciones.** NOI no recurrente; desarrollo en curso.
**Validaciones.** EV coherente. Rechazo sin NOI.
**Tolerancia y semilla.** 1e-10 · null.
**Referencia ingenua.** RI-MH.
**Referencias.** TMB-06 · fuente TFB-13 (RF-0070).
**Prioridad y madurez.** P1 · DOCUMENTADO.

### FON-DISC-001 · Descuento de vehículos cerrados frente a su media

**Identificación.** v2.0 · VIGENTE · MC-B06 · Mapa: área 39. Conservada del Bloque A y ampliada a vehículos concretos.
**Perfiles y horizontes.** SEL-FON, SEL-ALT (VA) · H3–H4.
**Propósito.** Descuento sobre NAV de fondos cerrados cotizados, ELTIF y vehículos cotizados de activos privados frente a su media.
**Entradas mínimas.** NAV con fecha y precio; historia ≥ 3 años.
**Método.** `P/NAV − 1`; z frente a la media de 3 años; ajuste por desfase del NAV.
**Parámetros.** ventana (3 años).
**Salidas.** TABLA (`para_ordenacion`). `estimacion_estadistica`.
**Supuestos y limitaciones.** NAV desfasado en activos privados.
**Validaciones.** Signos coherentes. Rechazo con NAV de > 6 meses.
**Tolerancia y semilla.** 1e-10 · null.
**Referencia ingenua.** RI-MH.
**Referencias.** TMB-06 · fuentes TFB-08.
**Prioridad y madurez.** P1 · DOCUMENTADO.

### DER-VRP-001 · Prima de varianza, sesgo y estructura de plazos

**Identificación.** v2.0 · VIGENTE · MC-B06 · Mapa: área 39. Conservada del Bloque A (fusiona sesgo y estructura).
**Perfiles y horizontes.** SEL-DER, SEL-TCV (VA) · H1–H3.
**Propósito.** Atractivo relativo de opciones y futuros de volatilidad: implícita frente a realizada, sesgo, estructura y base del futuro.
**Entradas mínimas.** Volatilidades implícitas por plazo y delta; realizada (FX-VOL-001); para futuros, spot, tipos y dividendos.
**Método.** `IV² − RV²` y percentil de la implícita; sesgo 25Δ; pendiente de la estructura; base frente a `F* = S·e^{(r − q)T}`.
**Parámetros.** plazo (1 mes); delta (25).
**Salidas.** TABLA (`para_ordenacion`). `estimacion_estadistica`.
**Supuestos y limitaciones.** Probabilidades neutrales al riesgo ≠ reales; la realizada futura solo en evaluación.
**Validaciones.** Paridad put-call. Rechazo con realizada posterior a la fecha de corte (`FUGA_INFORMACION`).
**Tolerancia y semilla.** 1e-8 · null.
**Referencia ingenua.** RI-UV.
**Referencias.** TMB-06, TMB-09 · fuente TFB-06 (RF-0302).
**Prioridad y madurez.** P1 · DOCUMENTADO.

### CHR-ONCHAIN-001 · Métricas de red

**Identificación.** v2.0 · VIGENTE · MC-B06 · Mapa: área 39. Conservada del Bloque A y ampliada.
**Perfiles y horizontes.** SEL-CRI (VA, QL) · H3–H4.
**Propósito.** Valoración relativa de tokens por actividad económica de la red.
**Entradas mínimas.** Capitalización y FDV, comisiones anualizadas, valor transferido ajustado, capitalización realizada; ≥ 12 meses.
**Método.** Capitalización/comisiones; NVT; MVRV; FDV/capitalización; percentiles del universo; filtro de volumen lavado.
**Parámetros.** ventana_comisiones (90 días).
**Salidas.** TABLA (`para_ordenacion`). `estimacion_estadistica`.
**Supuestos y limitaciones.** Actividad no es valor; cambios de metodología del proveedor.
**Validaciones.** FDV ≥ capitalización. Rechazo con < 12 meses.
**Tolerancia y semilla.** 1e-10 · null.
**Referencia ingenua.** RI-EQ.
**Referencias.** TMB-06 · fuentes TFB-14 (RF-0074, RF-0076, MBF-0481).
**Prioridad y madurez.** P1 · DOCUMENTADO.

### MON-YLD-001 · Rentabilidad monetaria equivalente y fijar frente a renovar

**Identificación.** v2.0 · VIGENTE · MC-B06 · Mapa: área 39. Fusiona MON-YLD-001 y MON-FIX-001 del Bloque A.
**Perfiles y horizontes.** SEL-MON (VA) · H2–H3.
**Propósito.** Comparar letras, fondos monetarios y pagarés por rentabilidad neta equivalente y valor de fijar el plazo.
**Entradas mínimas.** Precio o rendimiento con su convención; TER; €STR y curva corta o expectativas implícitas.
**Método.** Conversión a TAE neta; diferencial frente a €STR compuesto o a la curva del plazo; valor de fijar = rentabilidad a plazo − renovación esperada según la curva implícita.
**Parámetros.** convencion (descuento | simple | money_market).
**Salidas.** TABLA (`para_ordenacion`). `determinista` (conversión) y `estimacion_estadistica` (renovación esperada).
**Supuestos y limitaciones.** Prima por plazo en la curva implícita.
**Validaciones.** Conversiones inversas reproducen el precio. Rechazo sin convención declarada.
**Tolerancia y semilla.** 1e-10 · null.
**Referencia ingenua.** €STR compuesto (RI-UV).
**Referencias.** TMB-06 · fuentes TFB-02 (RF-0004), TFB-15 (RF-0347).
**Prioridad y madurez.** P1 · DOCUMENTADO.

### TCV-CARRY-001 · Valor razonable, carry y rolldown de factores de tipos, crédito y volatilidad

**Identificación.** v1.0 · VIGENTE · MC-B06 · Mapa: área 39. Integra TCV-SLOPE-001, TCV-BEI-001, TCV-CDS-001, TCV-VIXTS-001 y FIR-CARRY-001 del Bloque A.
**Perfiles y horizontes.** SEL-TCV (VA) · H1–H3.
**Propósito.** Ordenar futuros de tipos y bonos, ETF de tramo e inflación y productos de crédito o volatilidad por valor y carry.
**Entradas mínimas.** Curva, inflación implícita, encuestas (SPF), índices CDS o futuros de volatilidad con fecha; DV01 o vega del instrumento.
**Método.** (i) Pendiente frente a su valor razonable (regresión sobre expectativas de política). (ii) Inflación implícita frente a encuestas. (iii) Diferencial CDS frente a pérdidas esperadas. (iv) Estructura de futuros de volatilidad y coste de roll. (v) Carry y rolldown por unidad de DV01 o vega; percentil del universo.
**Parámetros.** factor (pendiente | inflacion | credito | volatilidad).
**Salidas.** TABLA (`para_ordenacion`). `estimacion_estadistica`.
**Supuestos y limitaciones.** Breakeven ≠ inflación esperada (prima de riesgo); deterioro estructural de productos de volatilidad.
**Validaciones.** DV01 neutral declarado. Rechazo sin sensibilidad del instrumento.
**Tolerancia y semilla.** 1e-8 · null.
**Referencia ingenua.** RI-UV.
**Referencias.** TMB-06 · fuentes TFB-06 (RF-0656, RF-0650, RF-0302), TFB-02 (RF-0669).
**Prioridad y madurez.** P1 · DOCUMENTADO.

### PRV-PME-001 · Public market equivalent

**Identificación.** v2.0 · VIGENTE · MC-B06 · Mapa: área 39. Conservada del Bloque A.
**Perfiles y horizontes.** SEL-ALT (QL) · H4.
**Propósito.** Historial del gestor del vehículo frente al mercado cotizado.
**Entradas mínimas.** Flujos (aportaciones, distribuciones) y NAV con fechas; índice de referencia.
**Método.** KS-PME; PME+; Direct Alpha; TVPI, DPI con XIRR.
**Parámetros.** indice (declarado).
**Salidas.** TABLA. `determinista` sobre flujos dados.
**Supuestos y limitaciones.** NAV es valoración; riesgo distinto del índice.
**Validaciones.** TVPI = DPI + RVPI. Rechazo sin fechas de flujos.
**Tolerancia y semilla.** 1e-8 · null.
**Referencia ingenua.** PME = 1.
**Referencias.** TMB-06.
**Prioridad y madurez.** P1 · DOCUMENTADO.

### ALT-DESMOOTH-001 · Desuavizado de rentabilidades

**Identificación.** v2.0 · VIGENTE · MC-B06 · Mapa: área 39. Conservada del Bloque A.
**Perfiles y horizontes.** SEL-ALT, SEL-INM (RI, VA) · H3–H4.
**Propósito.** Recuperar la volatilidad y la correlación reales de series tasadas o de NAV suavizado.
**Entradas mínimas.** Serie trimestral ≥ 20 observaciones.
**Método.** Geltner `r_t = (r*_t − ρ·r*_{t−1})/(1 − ρ)`; Getmansky-Lo-Makarov como segunda vía.
**Parámetros.** orden (1).
**Salidas.** SERIE desuavizada; volatilidad y ρ. `estimacion_estadistica`.
**Supuestos y limitaciones.** Suavizado AR(1).
**Validaciones.** Serie AR(1) simulada recuperada. Rechazo con < 12 observaciones.
**Tolerancia y semilla.** 1e-8 · null.
**Referencia ingenua.** Serie sin desuavizar.
**Referencias.** TMB-09.
**Prioridad y madurez.** P1 · DOCUMENTADO.

### QLT-ACC-001 · Calidad contable y señales de alerta

**Identificación.** v1.0 · VIGENTE · MC-B06 · Mapa: área 40.
**Perfiles y horizontes.** SEL-RV (QL, alertas PC4), SEL-RF (emisor), SEL-INM · H3–H4.
**Propósito.** Calcular Piotroski F, Beneish M, Altman Z, devengos y dilución y su comparación con los umbrales del playbook.
**Entradas mínimas.** Estados financieros de los dos últimos ejercicios publicados con fecha.
**Método.** F (9 señales); M de 8 variables; Z (y Z'' para no manufactureras); devengos de Sloan; dilución anual; comparación con umbrales (M > −1,78; Z < 1,8; dilución > 10 %).
**Parámetros.** umbrales (del playbook en F10).
**Salidas.** TABLA por candidato: valores, umbral, cruce sí/no. `determinista` sobre datos.
**Supuestos y limitaciones.** Altman no aplicable a financieras; modelos estimados en otras épocas.
**Validaciones.** F ∈ [0; 9]. Rechazo sin dos ejercicios.
**Tolerancia y semilla.** 1e-10 · null.
**Referencia ingenua.** RI-NA.
**Referencias.** TMB-07 · MBM-0121, MBM-0122.
**Prioridad y madurez.** P0 · DOCUMENTADO.

---
## 12. Fichas — MC-B07 Cribado y ranking

### SCR-NORM-001 · Winsorización, percentiles y neutralización

**Identificación.** v1.0 · VIGENTE · MC-B07 · Mapa: área 41.
**Perfiles y horizontes.** Todos los SEL- · no aplica.
**Propósito.** Convertir métricas heterogéneas en puntuaciones 0–100 comparables dentro del universo cribado (9.5.1 del Documento 0).
**Entradas mínimas.** Universo cribado (candidatos que superan PC1–PC4, Anexo C) con fecha y subgrupos; métricas por candidato con dirección (directa o inversa).
**Método.** (i) Winsorización 2,5/97,5 por métrica en el universo. (ii) Percentil por rango medio `100·(rango − 0,5)/n`, empates promediados, en el universo o en el subgrupo (≥ 10 elementos; si no, fusión declarada). (iii) Inversión `100 − pct` de métricas inversas. (iv) Neutralización opcional por residuos de regresión transversal sobre variables ficticias del subgrupo y ln(tamaño). (v) z robusto como escala auxiliar. (vi) Componente = media ponderada de sus métricas disponibles (pesos internos del playbook o iguales, declarados).
**Parámetros.** winsor (0,025; 0,975); subgrupo (del playbook); neutralizar (auto si heterogéneo).
**Salidas.** TABLA por candidato: bruto, winsorizado, percentil, componente. `determinista` sobre datos dados.
**Supuestos y limitaciones.** El percentil pierde distancias; universos pequeños dan baja resolución.
**Validaciones.** Percentiles en [0; 100]; métrica idéntica para todos ⇒ 50; métricas con correlación > 0,8 en un mismo componente señaladas. Rechazo con universo < 5.
**Tolerancia y semilla.** Igualdad exacta · null.
**Referencia ingenua.** RI-NA.
**Referencias.** TMB-07, TMB-13 · MBM-0111.
**Prioridad y madurez.** P0 · DOCUMENTADO.

### SCR-PUR-001 · Pureza de exposición

**Identificación.** v1.0 · VIGENTE · MC-B07 (con MC-B05) · Mapa: área 42.
**Perfiles y horizontes.** Todos los SEL-; PERF-B-TEMA (pureza del universo) · no aplica.
**Propósito.** Medir la proporción de la rentabilidad económica del candidato que procede del ámbito (2.4 del Documento 0) y su cruce con el mínimo PC2.
**Entradas mínimas.** Según tipo: segmentos (RV), uso de fondos o ingresos del emisor (RF), cartera con fecha (FON, IDX), GAV (INM), comisiones (CRI), NAV por segmento (ALT), exposición estimada (DIV, MP, TCV con ECO-EXPO-001).
**Método.** Métrica del playbook (tabla de 10.2 del prompt de MC-B07): RV `% ingresos` y `% EBIT`; FON `Σ w_i·1[i supera PC2]` y `Σ w_i·p_i`; IDX `Σ w_i·p_i` y cobertura; INM `% GAV`; DIV, MP, TCV sensibilidad; DER herencia; MON binaria. Intervalo: publicada ± error de clasificación (± 5 pp por defecto si el segmento mezcla actividades); estimada, intervalo del método. Marca `frontera_PC2`.
**Parámetros.** minimo_PC2 (del playbook en F10); metodo (publicado | estimado).
**Salidas.** TABLA por candidato: valor, intervalo, método, fuente, `frontera_PC2`. `determinista` (publicada) o `estimacion_estadistica` (estimada).
**Supuestos y limitaciones.** Segmentos con definiciones distintas; carteras desfasadas.
**Validaciones.** Pureza ∈ [0; 1]; segunda vía con ECO-EXPO-001 o SCR-PUR-002. Rechazo sin dato ni método (`DATOS_INSUFICIENTES`).
**Tolerancia y semilla.** 1e-10 · null.
**Referencia ingenua.** RI-NA.
**Referencias.** TMB-07, TMB-12 · fuentes TFB-07 (MBF-0201, MBF-0203), TFB-08 (RF-0521).
**Prioridad y madurez.** P0 · DOCUMENTADO.

### SCR-PUR-002 · Pureza por análisis de texto

**Identificación.** v1.0 · VIGENTE · MC-B07 · Mapa: áreas 42, 75.
**Perfiles y horizontes.** SEL-RV, SEL-RF; PERF-B-TEMA · no aplica.
**Propósito.** Estimar la pureza cuando no hay segmentos que la separen, a partir de la descripción del negocio y las notas.
**Entradas mínimas.** Textos del informe anual (descripción del negocio, segmentos) con fecha; texto de referencia del ámbito; muestra de validación con segmentos publicados (≥ 20 empresas).
**Método.** (i) Diccionario del ámbito o similitud de coseno con el texto de referencia (representación por bolsa de palabras ponderada o incrustaciones declaradas). (ii) Calibración de la similitud a pureza con la muestra de validación (regresión isotónica). (iii) Error de validación cruzada como incertidumbre.
**Parámetros.** representacion (tfidf | incrustaciones); validacion (cv 5).
**Salidas.** TABLA: pureza estimada con intervalo y error de validación. `estimacion_estadistica`.
**Supuestos y limitaciones.** Lenguaje promocional; empresas que describen aspiraciones.
**Validaciones.** Error de validación declarado; segunda vía SCR-PUR-001 estimada. Rechazo sin muestra de validación.
**Tolerancia y semilla.** 1e-6 · entero del plan.
**Referencia ingenua.** Pureza por clasificación sectorial.
**Referencias.** TMB-12 · FXM-0271, MBM-0235, MBM-0236, MBM-0238.
**Prioridad y madurez.** P2 · DOCUMENTADO.

### SCR-S-001 · Puntuación S (réplica de HT-03)

**Identificación.** v1.0 · VIGENTE · MC-B07 · Mapa: área 43.
**Perfiles y horizontes.** Todos los SEL- · no aplica.
**Propósito.** Reproducir exactamente el cálculo de S de HT-03 para estimar su incertidumbre (SCR-ROB-001), reconstruir en G3 (PC7) y re-ejecutar (CT-B-14). **HT-03 es canónica**.
**Entradas mínimas.** Componentes 0–100 (o NA/NE) por candidato; pesos del playbook en la versión vigente de F10.
**Método.** (i) NA redistribuye su peso proporcionalmente entre los demás. (ii) NE puntúa 0. (iii) > 2 NE ⇒ `DATOS_INSUFICIENTES`. (iv) `S = Σ w_c·C_c` con la regla de redondeo de HT-03. (v) Banderas: banda marginal (≤ 3 puntos de 65, 50 o del corte del top-N), cambio frente a un ranking previo del mismo ámbito.
**Parámetros.** version_pesos (F10); regla_redondeo (HT-03).
**Salidas.** TABLA: S, desglose ponderado, redistribuciones, banderas. `determinista`.
**Supuestos y limitaciones.** La ficha garantiza la aritmética, no la calidad de los componentes.
**Validaciones.** Identidad con HT-03 en todos los casos de `10_Herramientas`. Aclaración si la versión de pesos no coincide con F10; `DISCREPANCIA_HT03` ante cualquier diferencia.
**Tolerancia y semilla.** Igualdad exacta · null.
**Referencia ingenua.** RI-NA.
**Referencias.** TMB-13, TMB-07 · Documento 0, 8.5 y 9.5.
**Prioridad y madurez.** P0 · DOCUMENTADO.

### SCR-AEC-001 · Puntuaciones A, E y C (réplica de HT-03)

**Identificación.** v1.0 · VIGENTE · MC-B07 · Mapa: área 43.
**Perfiles y horizontes.** TRANSVERSAL · no aplica.
**Propósito.** Reconstruir A, E y C de HT-03 para G3, PA7, banda marginal del ámbito y CT-B-14.
**Entradas mínimas.** Componentes de A y E en múltiplos de 10 (o NA/NE); RF y RE; marca de saturación narrativa; pesos de F10.
**Método.** (i) NA/NE (máximo dos por puntuación). (ii) Tope de 40 en «valoración frente a expectativas» con saturación. (iii) Media ponderada redondeada al múltiplo de 5 con la regla de HT-03. (iv) `C = 0,20·A + 0,35·E + 0,25·RF + 0,20·RE`; tope `C ≤ E + 10`. (v) Banderas: banda marginal (≤ 5 puntos de 65, 60, 55, 50), cambio ≥ 15 puntos frente a un análisis previo.
**Parámetros.** version_pesos (F10).
**Salidas.** TABLA: A, E, C, desglose, banderas. `determinista`.
**Supuestos y limitaciones.** Los componentes son juicios anclados de los agentes.
**Validaciones.** Identidad con HT-03. `DISCREPANCIA_HT03` ante diferencias.
**Tolerancia y semilla.** Igualdad exacta · null.
**Referencia ingenua.** RI-NA.
**Referencias.** TMB-13 · Documento 0, 9.1 y Anexo A.
**Prioridad y madurez.** P0 · DOCUMENTADO.

### SCR-ROB-001 · Robustez del ranking: IC de S y de rango

**Identificación.** v1.0 · VIGENTE · MC-B07 (con MC-B01) · Mapa: área 44.
**Perfiles y horizontes.** Todos los SEL- · no aplica.
**Propósito.** IC 90 % de S y del rango de cada candidato, `P(top-N)`, marca `FRONTERA` (9.5.4; PC6).
**Entradas mínimas.** Salida de SCR-NORM-001 y SCR-S-001; incertidumbre de cada insumo (EE, intervalos de pureza, series de precio para remuestreo); top-N; B; semilla.
**Método.** Para b = 1…B: (i) perturbar insumos según su incertidumbre (series por bootstrap por bloques comunes a todo el universo); (ii) perturbar pesos `w_c + U(−5; +5)` puntos, truncar a ≥ 0 y renormalizar a 100 (NA en 0); (iii) recalcular **todo el universo** (winsorización, percentiles, componentes, S, rangos). Salidas: cuantiles 5 y 95 de S y del rango; `P(top-N)`; τ de Kendall medio frente a la base; `FRONTERA` si el IC del rango contiene N y N + 1; error de Monte Carlo del extremo del IC de S. En EXT, variantes de winsorización (1/99, 5/95) y de neutralización.
**Parámetros.** B (200 MIN solo pesos; 1 000 STD; 2 000 EXT); amplitud_pesos (5); bloque (4 semanas).
**Salidas.** RANKING con IC. `estimacion_estadistica`.
**Supuestos y limitaciones.** La incertidumbre declarada de los insumos condiciona el IC; no incluye la del modelo de S.
**Validaciones.** Universo sin ruido ⇒ IC degenerado; Σ pesos = 100 por réplica; S base = HT-03. Rechazo con universo < 5.
**Tolerancia y semilla.** 1e-6 en cuantiles; rangos y `FRONTERA` idénticos con la misma semilla · entero del plan.
**Referencia ingenua.** RI-RA (IC de rango esperado bajo ranking aleatorio) y RI-F1.
**Referencias.** TMB-07, TMB-08, TMB-13 · MBM-0111, MBM-0205, DOC-MOT-0080.
**Prioridad y madurez.** P0 · DOCUMENTADO.

### SCR-DUP-001 · Duplicación de exposición

**Identificación.** v1.0 · VIGENTE · MC-B07 · Mapa: área 45.
**Perfiles y horizontes.** Todos los SEL- · no aplica.
**Propósito.** Detectar los duplicados de 9.7 (mismo índice o cartera, mismo emisor, subclúster, correlación) y las exposiciones compartidas entre tipos (PC8).
**Entradas mínimas.** Carteras con fecha (vehículos), emisor y subclúster por candidato, rentabilidades semanales a 2 años.
**Método.** Solapamiento `Σ_i min(w_i^a, w_i^b)` (> 0,80); correlación semanal a 2 años con IC de Fisher (> 0,9); proporción del top-N por subclúster (> 40 %); emisiones por emisor en RF (> 2); emisor común entre tipos (exposición compartida).
**Parámetros.** umbrales (Anexo A, F10).
**Salidas.** TABLA de pares y marcas. `estimacion_estadistica` (correlaciones) y `determinista` (solapamientos).
**Supuestos y limitaciones.** Correlaciones de un solo régimen.
**Validaciones.** Solapamiento simétrico ≤ 1; candidato consigo mismo = 1. Rechazo sin carteras para vehículos (solo correlación, declarado).
**Tolerancia y semilla.** 1e-8 · null.
**Referencia ingenua.** RI-NA.
**Referencias.** TMB-07, TMB-09.
**Prioridad y madurez.** P0 · DOCUMENTADO.

### ML-CLUS-001 · Clústeres de exposición y apuestas independientes

**Identificación.** v2.0 · VIGENTE · MC-B07 · Mapa: área 45. Conservada del Bloque A y aplicada a candidatos.
**Perfiles y horizontes.** TRANSVERSAL · no aplica.
**Propósito.** Agrupar candidatos (o tipos) por factor dominante y contar las apuestas independientes que el informe declara (9.7.5).
**Entradas mínimas.** Rentabilidades alineadas ≥ 1 año diarias o ≥ 2 años semanales (series suavizadas desuavizadas).
**Método.** Correlación (Pearson y Spearman); distancia `√(2(1 − ρ))`; agrupación jerárquica de enlace medio; corte en ρ = 0,7; `N_ef = (Σλ)²/Σλ²` y `exp(H)`; ventana de estrés; exposición compartida cuenta una vez.
**Parámetros.** umbral_rho (0,7; 0,5–0,85); ventana (2 años semanal).
**Salidas.** TABLA: clúster por candidato, N_ef normal y de estrés, sensibilidad al umbral. `estimacion_estadistica`.
**Supuestos y limitaciones.** Correlaciones inestables y más altas en crisis.
**Validaciones.** n independientes ⇒ N_ef ≈ n. Rechazo con series no alineables.
**Tolerancia y semilla.** 1e-8; asignación exacta · null.
**Referencia ingenua.** Agrupación por tipo de activo.
**Referencias.** TMB-07, TMB-09.
**Prioridad y madurez.** P0 · IMPLEMENTADO (heredado).

### ACC-MOM-001 · Momento 12-1, de serie temporal y revisiones

**Identificación.** v2.0 · VIGENTE · MC-B07 · Mapa: área 47. Conservada del Bloque A y ampliada con revisiones.
**Perfiles y horizontes.** SEL-RV, SEL-IDX, SEL-DIV, SEL-MP, SEL-CRI, SEL-INM, SEL-ALT (MO) · H2–H3.
**Propósito.** Componente MO de S: tendencia relativa de precio y de estimaciones.
**Entradas mínimas.** Rentabilidad total ≥ 13 meses; revisiones de BPA con fecha (RV).
**Método.** 12-1; momento de serie temporal escalado por volatilidad; momento a 3 y 12 meses (DIV); revisiones netas de BPA a 3 meses; percentil en el universo.
**Parámetros.** ventanas (12-1; 3; 12).
**Salidas.** TABLA por candidato. `estimacion_estadistica`.
**Supuestos y limitaciones.** Caídas en rebotes de mercado.
**Validaciones.** Coherencia con rentabilidades acumuladas. Rechazo con < 13 meses (MO = NE).
**Tolerancia y semilla.** 1e-10 · null.
**Referencia ingenua.** RI-F1 (es en sí una referencia trivial del ranking).
**Referencias.** TMB-07 · DOC-MOT-0064, DOC-MOT-0065.
**Prioridad y madurez.** P1 · IMPLEMENTADO (heredado).

### SCR-LIQ-001 · Liquidez y costes de mantener

**Identificación.** v1.0 · VIGENTE · MC-B07 · Mapa: área 46.
**Perfiles y horizontes.** Todos los SEL- (LA, CO); PERF-B-FACT (capacidad) · no aplica.
**Propósito.** Componentes LA y CO de S; insumos de filtros de liquidez de PC1 (que aplica HT-11); capacidad de una estrategia.
**Entradas mínimas.** Volumen y precios diarios ≥ 3 meses; horquillas o datos para estimarlas; TER, diferencia de seguimiento, coste de roll, comisiones (KID).
**Método.** ADV en EUR; Amihud; horquilla cotizada o estimador de Roll; días de liquidación al 20 % del ADV; coste total `TER + diferencia de seguimiento + roll + horquilla/periodo de tenencia + éxito esperado`; para estrategias, capacidad por participación máxima del volumen.
**Parámetros.** participacion_ADV (0,20); periodo_tenencia (horizonte).
**Salidas.** TABLA por candidato. `estimacion_estadistica`.
**Supuestos y limitaciones.** Liquidez en estrés menor que la observada.
**Validaciones.** Coste total ≥ TER. Rechazo sin volumen (LA = NE).
**Tolerancia y semilla.** 1e-10 · null.
**Referencia ingenua.** RI-NA.
**Referencias.** TMB-07 · MBM-0119; fuentes TFB-08 (MBF-0218, RF-0523, RF-0529).
**Prioridad y madurez.** P0 · DOCUMENTADO.

### SCR-MCDA-001 · Decisión multicriterio para rasgos de la tesis

**Identificación.** v1.0 · VIGENTE · MC-B07 · Mapa: área 48.
**Perfiles y horizontes.** TRANSVERSAL · no aplica.
**Propósito.** Convertir rasgos cualitativos de la tesis en pesos internos de métricas cuando el Seleccionador lo pide (9.5.6), con consistencia y sensibilidad.
**Entradas mínimas.** Matriz de comparaciones por pares o valoraciones de atributos.
**Método.** AHP (vector propio principal, `CR = CI/RI < 0,10`); alternativa de valor multiatributo; PROMETHEE si se pide superación; sensibilidad de los pesos.
**Parámetros.** metodo (ahp | mavt | promethee).
**Salidas.** TABLA de pesos con CR y sensibilidad. `juicio_experto`.
**Supuestos y limitaciones.** No altera los pesos de componentes de S de F10.
**Validaciones.** Matriz recíproca; CR. Rechazo con CR ≥ 0,10 sin revisión.
**Tolerancia y semilla.** 1e-8 · null.
**Referencia ingenua.** Pesos iguales.
**Referencias.** TMB-13 · MBM-0241, MBM-0242, MBM-0244, MBM-0254, MBM-0257, MBM-0258.
**Prioridad y madurez.** P2 · DOCUMENTADO.

### FAC-PREM-001 · Prima y descomposición de un factor

**Identificación.** v1.0 · VIGENTE · MC-B07 · Mapa: área 47.
**Perfiles y horizontes.** PERF-B-FACT · H3–H4.
**Propósito.** Rentabilidad del factor, su significación ajustada por pruebas múltiples, su alfa frente a otros factores y su descomposición (D8 y D9 de ESTRATEGIA_FACTOR).
**Entradas mínimas.** Carteras larga-corta o rentabilidades del factor ≥ 10 años mensuales; factores de referencia.
**Método.** Carteras por quintiles o terciles (equiponderadas y por capitalización); rentabilidad, Sharpe con EE de Lo; alfa frente a 3/5 factores y momento; GRS; Fama-MacBeth si se parte de características; descomposición en cambio de valoración + rentabilidad estructural; `t > 3` si es un factor nuevo.
**Parámetros.** carteras (quintiles); rebalanceo (mensual).
**Salidas.** TABLA. `estimacion_estadistica`.
**Supuestos y limitaciones.** Decaimiento tras la publicación; microcapitalizaciones.
**Validaciones.** Factor simulado sin prima ⇒ t no significativo; segunda vía con datos de Kenneth French. Rechazo con < 5 años.
**Tolerancia y semilla.** 1e-8 · null.
**Referencia ingenua.** Prima nula.
**Referencias.** TMB-07, TMB-11 · DOC-MOT-0060, DOC-MOT-0061, DOC-MOT-0063, DOC-MOT-0064, DOC-MOT-0103, DOC-MOT-0104, DOC-MOT-0338, DOC-MOT-0347, ANA-DOC-0279; fuente TFB-06 (RF-0051).
**Prioridad y madurez.** P1 · DOCUMENTADO.

### FAC-SPREAD-001 · Diferencial de valoración del factor

**Identificación.** v1.0 · VIGENTE · MC-B07 · Mapa: área 47.
**Perfiles y horizontes.** PERF-B-FACT · H3–H4.
**Propósito.** Valoración del factor (D9 de ESTRATEGIA_FACTOR): ¿está barata la pata larga frente a la corta respecto a su historia?
**Entradas mínimas.** Múltiplos por valor de las carteras ≥ 10 años.
**Método.** Razón de medianas del múltiplo (corta/larga) o diferencia de medianas en logaritmos; percentil y z históricos; neutralización sectorial opcional.
**Parámetros.** multiplo (P/VC | PER | EV/EBITDA).
**Salidas.** TABLA. `estimacion_estadistica`.
**Supuestos y limitaciones.** Composición sectorial cambiante.
**Validaciones.** Signos coherentes. Rechazo con < 5 años.
**Tolerancia y semilla.** 1e-8 · null.
**Referencia ingenua.** RI-MH.
**Referencias.** TMB-07 · DOC-MOT-0065, MBM-0115.
**Prioridad y madurez.** P1 · DOCUMENTADO.

### FAC-CROWD-001 · Crowding del factor o de la tesis

**Identificación.** v1.0 · VIGENTE · MC-B07 (con MC-B01) · Mapa: áreas 10, 47.
**Perfiles y horizontes.** PERF-B-FACT, PERF-B-TEMA · H2–H3.
**Propósito.** Medir cuán concurrida está la estrategia o la tesis (D10; insumo de la saturación narrativa).
**Entradas mínimas.** Rentabilidades diarias de la pata larga; diferencial de valoración; interés corto; flujos de vehículos; posicionamiento.
**Método.** Correlación media por pares de la pata larga (comomentum); diferencial comprimido (FAC-SPREAD-001); interés corto de la pata corta; flujos (SER-FLOW-001); compuesto de z robustos con pesos declarados y su percentil.
**Parámetros.** ventana (63 sesiones); pesos (iguales).
**Salidas.** TABLA y SERIE del compuesto. `estimacion_estadistica` (`juicio_experto` por pesos).
**Supuestos y limitaciones.** Indicadores ruidosos; relación con caídas futuras incierta.
**Validaciones.** Componentes con signo coherente. Rechazo con < 1 año.
**Tolerancia y semilla.** 1e-8 · null.
**Referencia ingenua.** RI-MH.
**Referencias.** TMB-07, TMB-12 · fuentes TFB-15 (RF-0049, MBF-0511).
**Prioridad y madurez.** P2 · DOCUMENTADO.

---

### EMG-PEM-001 · Puntuación de potencial de emergentes PEM y pureza de la vía de exposición (V2.1)

**Identificación.** v1.0 · VIGENTE · MC-B07 (con MC-B02 para tracción y mercado) · Mapa: área 78.
**Perfiles y horizontes.** PERF-B-TEMA, PERF-B-SECT, PERF-B-CADENA; SEL-RV y SEL-FON para la vía de exposición · H4–H5.
**Propósito.** Agregar la evaluación de cada emergente del radar de AG-B24 (8.7.3) en **PEM** (0–100) con réplica exacta de HT-03, ordenar la subtabla de emergentes de cada eslabón y medir la **pureza de la vía de exposición** (cuánta exposición al emergente da su matriz cotizada o el ETF o fondo que lo contiene).
**Entradas mínimas.** Por emergente (`EMG-B-`): seis criterios en múltiplos de 10 con ancla y evidencia (tecnología, tracción, equipo, financiación, posición en la cadena, vía de exposición); pesos vigentes de F10; para `MATRIZ_COTIZADA`: participación de la matriz y peso del emergente en su valor o ingresos (estimado con método declarado); para `ETF_O_FONDO`: peso en cartera (N-PORT o informe del fondo).
**Método.** (i) `PEM = round(Σ w_c·c_c / Σ w_c)` con pesos tecnología 20, tracción 25, equipo 15, financiación 15, posición 15, vía 10; criterios NA redistribuidos, más de dos NE ⇒ `DATOS_INSUFICIENTES`. (ii) Sensibilidad de PEM a ±5 puntos de peso y orden estable de la subtabla (IC de rango por perturbación). (iii) **Pureza de la vía**: `pureza_matriz = participación × valor_emergente / valor_matriz` (o por ingresos), con banda; `pureza_fondo = peso en cartera`; marca `exposicion_residual` si < 5 %. (iv) **Tasas base** que acompañan a la subtabla (contexto, no componente): rentabilidad posterior media de salidas a bolsa y SPAC frente al mercado y su dispersión, de la literatura registrada (F7, TB-23).
**Parámetros.** pesos (F10); umbral_residual (5 %).
**Salidas.** TABLA por eslabón: PEM con desglose y orden; pureza de la vía con banda; marcas `exposicion_residual` y `fuera_de_filtros` (si el instrumento no supera los filtros del playbook). `juicio_experto` anclado (criterios) y `estimacion_estadistica` (pureza). **PEM no es S ni valoración**: se rotula así.
**Supuestos y limitaciones.** Valoraciones de rondas posrenta sobrevaloran la empresa; las bases de capital riesgo tienen sesgo de selección y retraso; lo que procede de la propia empresa sin contraste es [INTERPRETACIÓN] como máximo (8.7.3).
**Validaciones.** Réplica de HT-03 exacta; caso de control con criterios conocidos; rechazo de una petición de valor razonable de un emergente (`PRECIO_OBJETIVO_FUERA_DE_ROL`).
**Tolerancia y semilla.** Igualdad exacta con HT-03 · null (semilla del plan en la sensibilidad).
**Referencia ingenua.** RI-NA (no es pronóstico).
**Referencias.** TMB-13, TMB-07, TMB-03 · MBM-0254, MBM-0248, MBM-0202; literatura de dominio en F7 (TB-23) por `ver_tambien`.
**Prioridad y madurez.** P1 · DOCUMENTADO.

## 13. Fichas — MC-B08 Simulación, escenarios y sensibilidad

### SIM-MC-001 · Monte Carlo y cuasi-Monte Carlo

**Identificación.** v2.0 · VIGENTE · MC-B08 · Mapa: área 49. Conservada del Bloque A y ampliada a modelos de la máquina de proyecciones.
**Perfiles y horizontes.** TRANSVERSAL · H1–H4; en H5, solo como motor de trayectorias de DIF-H5-001 con salida en bandas verbales (V2.1, R13).
**Propósito.** Distribución de una salida (capitalización implícita, rentabilidad frente a la referencia, pérdidas) dados insumos inciertos.
**Entradas mínimas.** Modelo explícito; distribuciones de insumos con fuente y clase; n; semilla.
**Método.** Muestreo aleatorio, LHS o Sobol aleatorizado; reducción de varianza (antitéticas, control); evaluación; cuantiles y su error; estabilidad entre semillas en EXT.
**Parámetros.** n (10 000 STD; 2 000 MIN con LHS); muestreo (lhs | sobol | aleatorio).
**Salidas.** DISTRIBUCION (p5…p95, media), error de Monte Carlo. Clase: la más débil de los insumos críticos.
**Supuestos y limitaciones.** El resultado no es mejor que sus distribuciones de entrada.
**Validaciones.** Modelo lineal con momentos analíticos; segunda vía con otra semilla. Rechazo sin modelo explícito.
**Tolerancia y semilla.** 1e-6 · entero del plan.
**Referencia ingenua.** Según el uso (RI-PA en rentabilidad frente a la referencia).
**Referencias.** TMB-08 · DOC-MOT-0006, DOC-MOT-0371, DOC-MOT-0372, DOC-MOT-0378, MBM-0209.
**Prioridad y madurez.** P0 · IMPLEMENTADO (heredado).

### SIM-IC-001 · Dependencias por Iman-Conover y cópulas

**Identificación.** v1.0 · VIGENTE · MC-B08 · Mapa: área 50.
**Perfiles y horizontes.** TRANSVERSAL · H2–H4.
**Propósito.** Inducir dependencias realistas entre insumos de la simulación sin alterar sus marginales.
**Entradas mínimas.** Muestras marginales (n ≥ 1 000); matriz de Spearman objetivo justificada (histórica con ventana o juicio declarado); o cópula con parámetros.
**Método.** (i) Comprobar y reparar C (Higham) con distancia declarada. (ii) Puntuaciones de van der Waerden permutadas; `E = F·Fᵀ`, `C = P·Pᵀ`; `T = S·(F⁻¹)ᵀ·Pᵀ`. (iii) Reordenar cada marginal según los rangos de T. (iv) Cópula t si importan las colas conjuntas (ν declarado).
**Parámetros.** metodo (iman_conover | copula_t | copula_gauss); nu (5).
**Salidas.** Muestra conjunta; Spearman logrado frente al objetivo. Clase heredada.
**Supuestos y limitaciones.** Controla rangos, no colas; empates con marginales discretas.
**Validaciones.** Marginales idénticas; Spearman logrado a ± 0,02 del objetivo con n ≥ 1 000. Rechazo con C irreparable (insumos independientes con limitación y sensibilidad).
**Tolerancia y semilla.** 1e-6 · entero del plan.
**Referencia ingenua.** Insumos independientes.
**Referencias.** TMB-08 · MBM-0208, MBM-0210.
**Prioridad y madurez.** P0 · DOCUMENTADO.

### SIM-SCN-001 · Escenarios coherentes, probabilidad frente a la referencia y RE

**Identificación.** v1.0 · VIGENTE · MC-B08 · Mapa: área 51. Desarrolla SCN-H-001 del Bloque A.
**Perfiles y horizontes.** Todos los PERF-B- · H2–H4.
**Propósito.** Resultados del ámbito por escenario y por simulación frente a su referencia; RE para C (9.1) y asimetría para A.
**Entradas mínimas.** ≥ 3 escenarios con premisas, disparadores y régimen; probabilidades con base (o equiponderación declarada); modelo; referencia de comparación del ámbito.
**Método.** (i) Comprobar coherencia (mismas variables, relaciones respetadas). (ii) Simular dentro de cada escenario (SIM-MC-001). (iii) `P_s(R > R_ref)`; `RE = 100·Σ π_s·P_s`. (iv) Asimetría `E[(R − R_ref)⁺]/E[(R_ref − R)⁺]` y cuantiles del exceso. (v) Bandas verbales del Anexo A si no hay probabilidades con base.
**Parámetros.** probabilidades (con_base | equiponderadas); n_por_escenario (5 000).
**Salidas.** TABLA por escenario y total: cuantiles, probabilidad, RE (0–100), asimetría. Clase heredada.
**Supuestos y limitaciones.** RE depende de los escenarios elegidos; probabilidades sin base prohibidas como numéricas.
**Validaciones.** RE ∈ [0; 100]; Σ π = 1. Rechazo con < 3 escenarios.
**Tolerancia y semilla.** 1e-6 · entero del plan.
**Referencia ingenua.** RI-PA (probabilidad 0,5 de superar a la referencia).
**Referencias.** TMB-08 · MBM-0211, ANA-DOC-0531, ANA-DOC-0535.
**Prioridad y madurez.** P0 · DOCUMENTADO.

### SIM-TOR-001 · Tornado y cribado de Morris

**Identificación.** v1.0 · VIGENTE · MC-B08 · Mapa: área 52.
**Perfiles y horizontes.** TRANSVERSAL · no aplica.
**Propósito.** Ordenar las premisas por influencia (sensibilidades críticas del protocolo cuantitativo, 8.8).
**Entradas mínimas.** Modelo; rango p10–p90 (o declarado) de cada insumo.
**Método.** Tornado OAT p10/p90 ordenado por amplitud; Morris con r trayectorias y p niveles (`μ*`, σ) cuando k > 10 o hay sospecha de interacciones.
**Parámetros.** r (20); p (4).
**Salidas.** TABLA ordenada. Clase heredada.
**Supuestos y limitaciones.** OAT no es global.
**Validaciones.** Modelo lineal: amplitudes proporcionales a |a_i|·rango_i. Rechazo sin rangos.
**Tolerancia y semilla.** 1e-8 (tornado); 1e-6 (Morris) · entero del plan.
**Referencia ingenua.** RI-NA.
**Referencias.** TMB-08 · MBM-0214, MBM-0215, MBM-0204.
**Prioridad y madurez.** P0 · DOCUMENTADO.

### SIM-SOB-001 · Índices de Sobol

**Identificación.** v1.0 · VIGENTE · MC-B08 · Mapa: área 53.
**Perfiles y horizontes.** TRANSVERSAL (PERF-B-SECT EXT: crecimiento implícito; PERF-B-TEMA: adopción) · no aplica.
**Propósito.** Sensibilidad global: fracción de la varianza de la salida atribuible a cada premisa y a sus interacciones.
**Entradas mínimas.** Modelo; distribuciones de insumos; N (potencia de 2).
**Método.** Matrices A, B y `A_B^{(i)}` con Sobol aleatorizado; estimadores de Saltelli (S_i) y Jansen (S_Ti); IC por bootstrap de filas; con insumos correlacionados, Borgonovo o Shapley.
**Parámetros.** N (2 048–8 192).
**Salidas.** TABLA: S_i, S_Ti con IC; interacciones. Clase heredada.
**Supuestos y limitaciones.** Insumos independientes para la versión clásica; coste `N(k + 2)`.
**Validaciones.** Función de Ishigami; modelo lineal con índices analíticos; S_Ti ≥ S_i. Rechazo con presupuesto insuficiente (Morris + tornado, declarado).
**Tolerancia y semilla.** 1e-6 · entero del plan.
**Referencia ingenua.** Tornado (SIM-TOR-001).
**Referencias.** TMB-08 · MBM-0201, MBM-0202, MBM-0203, MBM-0205, MBM-0206, MBM-0217, MBM-0212.
**Prioridad y madurez.** P1 · DOCUMENTADO.

### SIM-JUD-001 · Agregación de juicio experto

**Identificación.** v1.0 · VIGENTE · MC-B08 · Mapa: área 54.
**Perfiles y horizontes.** TRANSVERSAL · no aplica.
**Propósito.** Combinar juicios (rangos, probabilidades, techos de mercado) de forma trazable cuando no hay datos.
**Entradas mínimas.** ≥ 2 juicios con su forma (cuantiles o probabilidad) y su fuente; preguntas semilla si se usa Cooke.
**Método.** Agregación lineal de distribuciones (pesos iguales por defecto); modelo clásico de Cooke (calibración × informatividad); media de logit con extremización moderada solo con evidencia; distribución PERT resultante para simulación.
**Parámetros.** metodo (lineal | cooke | logit); a_extremizacion (1).
**Salidas.** DISTRIBUCION o probabilidad agregada. `juicio_experto`, siempre.
**Supuestos y limitaciones.** Juicios correlacionados (misma fuente) no son independientes.
**Validaciones.** Pesos suman 1. Rechazo con un solo juicio (se entrega tal cual, sin agregación).
**Tolerancia y semilla.** 1e-8 · null.
**Referencia ingenua.** Media simple de los juicios.
**Referencias.** TMB-13 · MBM-0248, MBM-0249, MBM-0250, MBM-0252, MBM-0259, MBM-0264, MBM-0267, ANA-DOC-0236.
**Prioridad y madurez.** P1 · DOCUMENTADO.

### SIM-BOTT-001 · Persistencia del cuello por simulación

**Identificación.** v1.0 · VIGENTE · MC-B08 (con MC-B04) · Mapa: áreas 23, 49.
**Perfiles y horizontes.** PERF-B-CADENA (EXT) · H3–H4.
**Propósito.** Distribución de la fecha de resolución del cuello y probabilidad de persistencia al final del horizonte (sub-bloque 4d).
**Entradas mínimas.** Tubería por proyecto (capacidad, fase, probabilidad, retraso); demanda por escenario; holgura de resolución.
**Método.** Simulación por proyecto (entrada Bernoulli por fase, retraso lognormal) frente a la demanda; fecha en que capacidad ≥ demanda × (1 + h); probabilidad de persistencia; margen del eslabón si se aporta su relación con la holgura.
**Parámetros.** h (0,05); n (10 000).
**Salidas.** DISTRIBUCION de la fecha; probabilidad. Clase heredada (probabilidades de fase de juicio ⇒ `juicio_experto`).
**Supuestos y limitaciones.** Independencia entre proyectos salvo correlación declarada.
**Validaciones.** Tubería determinista ⇒ fecha única. Rechazo sin tubería.
**Tolerancia y semilla.** 1e-6 · entero del plan.
**Referencia ingenua.** Fecha de resolución = fecha de entrada nominal de los proyectos anunciados.
**Referencias.** TMB-05, TMB-08.
**Prioridad y madurez.** P2 · DOCUMENTADO.

### DEC-VOI-001 · Valor de la información

**Identificación.** v2.0 · VIGENTE · MC-B08 · Mapa: área 55. Conservada del Bloque A.
**Perfiles y horizontes.** TRANSVERSAL · no aplica.
**Propósito.** Priorizar búsquedas y cálculos por su capacidad de cambiar una decisión de umbral (R22; 10.4 del Documento 0).
**Entradas mínimas.** Decisión con umbral (A, S, top-N), modelo y distribución de la variable incierta.
**Método.** VEIP y valor de información parcial; probabilidad de que resolver la variable cruce el umbral; con Sobol, ordenación por S_Ti × probabilidad de cruce.
**Parámetros.** umbral (de F10).
**Salidas.** TABLA ordenada de variables. Clase heredada.
**Supuestos y limitaciones.** Distribuciones a priori de juicio.
**Validaciones.** VEIP ≥ 0. Rechazo sin decisión de umbral.
**Tolerancia y semilla.** 1e-6 · entero del plan.
**Referencia ingenua.** RI-NA.
**Referencias.** TMB-13 · MBM-0256.
**Prioridad y madurez.** P1 · DOCUMENTADO.

---

## 14. Fichas — MC-B09 Riesgo y redes

### RISK-VAR-001 · VaR y Expected Shortfall

**Identificación.** v2.0 · VIGENTE · MC-B09 · Mapa: área 56. Conservada del Bloque A.
**Perfiles y horizontes.** TRANSVERSAL · H1–H3.
**Propósito.** Colas de la exposición (indicador del ámbito, candidato, top-N ilustrativo): RI de S, D12.
**Entradas mínimas.** ≥ 3 años diarios (≥ 1 000 para EVT).
**Método.** Histórico; Cornish-Fisher; simulación histórica filtrada (VOL-GARCH-001); EVT por excedentes (umbral p95); ES al 97,5 %; backtesting de Kupiec y Christoffersen si hay historia.
**Parámetros.** nivel (0,975 ES; 0,99 VaR); horizonte (10 sesiones).
**Salidas.** TABLA: VaR, ES por método. `estimacion_estadistica`.
**Supuestos y limitaciones.** Estacionariedad; colas de muestras cortas.
**Validaciones.** ES ≥ VaR; normal simulada. Rechazo con < 1 año.
**Tolerancia y semilla.** 1e-8 · entero del plan si hay simulación.
**Referencia ingenua.** VaR normal.
**Referencias.** TMB-09 · DOC-MOT-0074, DOC-MOT-0075, DOC-MOT-0350, DOC-MOT-0072, DOC-MOT-0073, DOC-MOT-0363.
**Prioridad y madurez.** P0 · IMPLEMENTADO (heredado).

### RISK-DD-001 · Drawdown, liquidez y escala de riesgo 1–5

**Identificación.** v2.0 · VIGENTE · MC-B09 · Mapa: área 56. Conservada del Bloque A; es la «ficha del Catálogo» que cita el Anexo A para la escala 1–5.
**Perfiles y horizontes.** TRANSVERSAL · H2–H4.
**Propósito.** Riesgo de trayectoria y de liquidez y clase de riesgo 1–5 del paquete (`riesgo_1a5`).
**Entradas mínimas.** ≥ 3 años de rentabilidades (series suavizadas desuavizadas con ALT-DESMOOTH-001); volumen si hay mercado.
**Método.** MDD, duración y recuperación; Calmar; CDaR; días de liquidación al 20 % del ADV; LVaR; escala por volatilidad anualizada (< 5 % ⇒ 1; 5–10 % ⇒ 2; 10–20 % ⇒ 3; 20–35 % ⇒ 4; ≥ 35 % ⇒ 5) con +1 (máximo 5) por colas pesadas (ES 97,5 % a 10 sesiones > 2,5·σ_diaria·√10), liquidez baja (> 5 días) o MDD histórico > 50 %.
**Parámetros.** ventana (toda; mínimo 3 años); participacion_ADV (0,20).
**Salidas.** TABLA: MDD, duración, Calmar, CDaR, días de liquidación, LVaR, `riesgo_1a5` con motivo. `estimacion_estadistica`.
**Supuestos y limitaciones.** MDD de muestras cortas subestima el de largo plazo; la escala es calibrable por el Evaluador (propuesta).
**Validaciones.** MDD ∈ [0; 1]; serie creciente ⇒ 0. Rechazo con < 1 año.
**Tolerancia y semilla.** 1e-8; clase exacta · null.
**Referencia ingenua.** RI-NA.
**Referencias.** TMB-09 · DOC-MOT-0076.
**Prioridad y madurez.** P0 · IMPLEMENTADO (heredado).

### RISK-STR-001 · Estrés histórico, hipotético e inverso

**Identificación.** v1.0 · VIGENTE · MC-B09 · Mapa: área 57.
**Perfiles y horizontes.** Todos los PERF-B- · H2–H4.
**Propósito.** Pérdidas del ámbito y de los candidatos en episodios y choques (D11, D12) y choque mínimo que invalida la tesis o expulsa a un candidato del top-N.
**Entradas mínimas.** Sensibilidades de la exposición a las variables de riesgo; episodios con fechas o choques con mecanismo; umbral del estrés inverso.
**Método.** (i) Histórico: movimientos del episodio aplicados a la exposición actual. (ii) Hipotético: choque de demanda (elasticidades), márgenes (apalancamiento operativo), insumos (modelo de precios de NET-IO-001), carbono (escenarios NGFS), tipos (duración). (iii) Inverso: choque mínimo que cruza el umbral y su percentil histórico.
**Parámetros.** episodios (catálogo del perfil); umbral_inverso.
**Salidas.** TABLA de pérdidas por escenario; choque inverso. `estimacion_estadistica` o `juicio_experto` (hipotéticos).
**Supuestos y limitaciones.** Composición actual distinta de la histórica; sensibilidades lineales.
**Validaciones.** Choque nulo ⇒ pérdida nula. Rechazo sin sensibilidades.
**Tolerancia y semilla.** 1e-8 · null.
**Referencia ingenua.** RI-NA.
**Referencias.** TMB-09, TMB-08 · ANA-DOC-0517, ANA-DOC-0531; fuentes TFB-17 (MBF-0443, MBF-0444).
**Prioridad y madurez.** P0 · DOCUMENTADO.

### RISK-CRASH-001 · Distribución de pérdidas y colapsos de factores

**Identificación.** v1.0 · VIGENTE · MC-B09 · Mapa: área 56.
**Perfiles y horizontes.** PERF-B-FACT · H2–H4.
**Propósito.** D12 de ESTRATEGIA_FACTOR: frecuencia, magnitud y duración de los colapsos de la prima.
**Entradas mínimas.** Rentabilidades mensuales del factor ≥ 10 años (diarias para episodios).
**Método.** Distribución de pérdidas mensuales; ES 97,5 %; MDD y duración; asimetría condicional al régimen; episodios catalogados; probabilidad empírica de pérdidas > k σ en el horizonte.
**Parámetros.** k (2; 3).
**Salidas.** TABLA. `estimacion_estadistica`.
**Supuestos y limitaciones.** Pocos episodios independientes.
**Validaciones.** Coherencia con RISK-DD-001. Rechazo con < 5 años.
**Tolerancia y semilla.** 1e-8 · null.
**Referencia ingenua.** Distribución normal con la misma media y σ.
**Referencias.** TMB-09, TMB-07.
**Prioridad y madurez.** P1 · DOCUMENTADO.

### RISK-GEO-001 · Riesgo país y de divisa

**Identificación.** v1.0 · VIGENTE · MC-B09 · Mapa: área 59.
**Perfiles y horizontes.** PERF-B-GEO; SEL-DIV (QL, RI), SEL-RF (soberanos) · H3–H4.
**Propósito.** Estrés de la divisa frente a EUR, dinámica de la deuda pública y sostenibilidad externa.
**Entradas mínimas.** Tipo de cambio ≥ 10 años; deuda, tipos, crecimiento nominal, saldo primario; cuenta corriente, reservas, deuda externa a corto plazo.
**Método.** Percentiles de la variación de la divisa en el horizonte; `Δd = [(r − g)/(1 + g)]·d − sp` con estrés de r y g; Greenspan-Guidotti; reservas en meses de importaciones (alerta < 3).
**Parámetros.** horizonte; escenarios_r_g.
**Salidas.** TABLA. `estimacion_estadistica`.
**Supuestos y limitaciones.** Datos fiscales con retraso y revisiones.
**Validaciones.** Identidad de la deuda. Rechazo sin datos fiscales (solo divisa).
**Tolerancia y semilla.** 1e-8 · null.
**Referencia ingenua.** RI-PA (divisa).
**Referencias.** TMB-09 · fuentes TFB-05 (FXF-0053), TFB-01 (FXF-0415, RF-0007).
**Prioridad y madurez.** P1 · DOCUMENTADO.

### FX-CORR-001 · Correlación dinámica y dependencia de cola

**Identificación.** v2.0 · VIGENTE · MC-B09 · Mapa: área 58. Conservada del Bloque A.
**Perfiles y horizontes.** TRANSVERSAL · H1–H4.
**Propósito.** Correlaciones rodantes, EWMA y DCC; dependencia de cola empírica; insumo de duplicación, apuestas independientes y escenarios.
**Entradas mínimas.** Series alineadas ≥ 1 año diarias o 2 años semanales.
**Método.** Pearson y Spearman rodantes; EWMA; DCC; `λ_L(5 %)` empírica; reparación de Higham si se agregan matrices.
**Parámetros.** ventana (2 años semanal); lambda (0,94).
**Salidas.** SERIE y TABLA. `estimacion_estadistica`.
**Supuestos y limitaciones.** Inestabilidad; asincronía entre mercados.
**Validaciones.** Simetría, diagonal 1, semidefinida positiva. Rechazo con series no alineables.
**Tolerancia y semilla.** 1e-8 · null.
**Referencia ingenua.** Correlación de muestra completa.
**Referencias.** TMB-09 · DOC-MOT-0214.
**Prioridad y madurez.** P0 · IMPLEMENTADO (heredado).

### RISK-RGC-001 · Correlaciones condicionadas al régimen

**Identificación.** v1.0 · VIGENTE · MC-B09 · Mapa: área 58.
**Perfiles y horizontes.** PERF-B-GEO, PERF-B-SEGM, PERF-B-FACT · H2–H4.
**Propósito.** Matrices de correlación por régimen y corrección del sesgo de heterocedasticidad al comparar calma y crisis (D7; estrés; apuestas en estrés).
**Entradas mínimas.** Series alineadas y regímenes filtrados (FX-REGIME-001) con ≥ 30 observaciones por régimen.
**Método.** Correlaciones por régimen; Forbes-Rigobon `ρ* = ρ/√[1 + δ(1 − ρ²)]`; conectividad de Diebold-Yilmaz opcional; CoVaR opcional.
**Parámetros.** regimenes (2).
**Salidas.** TABLA por régimen con IC. `estimacion_estadistica`.
**Supuestos y limitaciones.** Pocos datos de crisis.
**Validaciones.** Matrices semidefinidas positivas. Rechazo con < 30 observaciones por régimen.
**Tolerancia y semilla.** 1e-8 · null.
**Referencia ingenua.** Correlación incondicional.
**Referencias.** TMB-09 · DOC-MOT-0365, MBM-0218, DOC-MOT-0356, DOC-MOT-0357.
**Prioridad y madurez.** P1 · DOCUMENTADO.

### NET-IO-001 · Análisis input-output

**Identificación.** v1.0 · VIGENTE · MC-B09 · Mapa: área 60.
**Perfiles y horizontes.** PERF-B-CADENA, PERF-B-GEO (sector ancla), PERF-B-TEMA · H4.
**Propósito.** Multiplicadores, encadenamientos, *upstreamness*, valor añadido en el comercio y traslado de costes (sub-bloques 4a y 4e; D4, D6).
**Entradas mínimas.** Tabla input-output (OCDE ICIO por defecto) con año y precios; sectores relevantes; desagregación del eslabón si existe.
**Método.** `A = Z·diag(x)⁻¹`; `L = (I − A)⁻¹`; multiplicadores; Rasmussen (BL, FL con Ghosh); *upstreamness* `U = (I − Δ)⁻¹·1`; VA en el comercio; modelo de precios `p = (I − Aᵀ)⁻¹·v`; extracción hipotética.
**Parámetros.** tabla (ICIO | WIOD); anio; pais.
**Salidas.** TABLA por sector. `determinista` sobre la tabla (supuestos de Leontief declarados).
**Supuestos y limitaciones.** Coeficientes fijos; agregación sectorial; Ghosh no causal.
**Validaciones.** `x = L·f`; columnas de A < 1; economía de dos sectores analítica. Rechazo sin tabla.
**Tolerancia y semilla.** 1e-10 · null.
**Referencia ingenua.** RI-NA.
**Referencias.** TMB-10 · MBM-0219, MBM-0221, MBM-0222, MBM-0223, MBM-0224, MBM-0226, MBM-0227, MBM-0229, MBM-0231, ANA-DOC-0451; fuente TFB-05 (MBF-0052).
**Prioridad y madurez.** P1 · DOCUMENTADO.

### NET-SHOCK-001 · Contagio de choques en la cadena

**Identificación.** v1.0 · VIGENTE · MC-B09 · Mapa: área 61.
**Perfiles y horizontes.** PERF-B-CADENA, PERF-B-TEMA · H3–H4.
**Propósito.** Pérdidas de producción y de ingresos por eslabón y por candidato ante un choque de oferta (cuellos, sanciones, catástrofes).
**Entradas mínimas.** Choque (insumo, país, magnitud, duración); coeficientes técnicos o tabla; cuotas de compra; supuesto de sustituibilidad.
**Método.** Propagación aguas abajo con sustituibilidad σ (0 = Leontief; > 0 parcial) y horizonte; pérdidas por eslabón y candidato expuesto; banda por σ y cuotas.
**Parámetros.** sigma (0; 0,5); duracion.
**Salidas.** TABLA con banda. `estimacion_estadistica` (`juicio_experto` si σ es de juicio).
**Supuestos y limitaciones.** Sustituibilidad incierta; inventarios amortiguadores.
**Validaciones.** Choque nulo ⇒ sin pérdidas. Rechazo sin choque definido.
**Tolerancia y semilla.** 1e-10 · null.
**Referencia ingenua.** Pérdida proporcional a la cuota del insumo.
**Referencias.** TMB-10 · MBM-0225, ANA-DOC-0448, ANA-DOC-0449, ANA-DOC-0450, ANA-DOC-0455.
**Prioridad y madurez.** P1 · DOCUMENTADO.

### NET-EXPO-001 · Concentración de exposiciones comunes

**Identificación.** v1.0 · VIGENTE · MC-B09 · Mapa: área 62.
**Perfiles y horizontes.** PERF-B-CADENA, PERF-B-GEO; todos los SEL- (apuestas) · H3–H4.
**Propósito.** Dependencias estratégicas del ámbito (D6) y dependencias comunes de los candidatos (apuestas no independientes).
**Entradas mínimas.** Comercio o producción por país del insumo crítico; matriz candidato × proveedor, cliente o país.
**Método.** HHI por país; cuota del primer país; cuota bajo sanciones o controles; candidatos con la misma dependencia dominante agrupados.
**Parámetros.** umbral_HHI (2 500); umbral_primer_pais (0,50).
**Salidas.** TABLA. `determinista` sobre datos.
**Supuestos y limitaciones.** Comercio indirecto (reexportaciones) oculto.
**Validaciones.** Cuotas suman 1. Rechazo sin datos por país.
**Tolerancia y semilla.** 1e-10 · null.
**Referencia ingenua.** RI-NA.
**Referencias.** TMB-10 · fuentes TFB-05 (MBF-0036, MBF-0061, MBF-0051), TFB-12 (RF-0356, MBF-0248), TFB-16 (MBF-0414).
**Prioridad y madurez.** P1 · DOCUMENTADO.

---

## 15. Fichas — MC-B10 Evaluación predictiva y backtesting de selección

### FC-EVAL-001 · Puntuación y comparación de pronósticos

**Identificación.** v2.0 · VIGENTE · MC-B10 · Mapa: área 63. Conservada del Bloque A.
**Perfiles y horizontes.** TRANSVERSAL · H1–H4.
**Propósito.** Resolver la calidad de los PRG-B congelados frente a sus referencias ingenuas.
**Entradas mínimas.** Pares pronóstico–resultado con fechas de congelación y resolución; referencia.
**Método.** Brier y descomposición de Murphy; log-score; CRPS; MASE; acierto direccional con Pesaran-Timmermann; Diebold-Mariano con HLN (n ≥ 30); Clark-West; Giacomini-White; BSS con IC por bootstrap.
**Parámetros.** B (2 000); bloques (si hay solapamiento).
**Salidas.** TABLA por celda. `estimacion_estadistica`.
**Supuestos y limitaciones.** Solapamiento reduce n efectivo.
**Validaciones.** REL − RES + UNC = BS. Rechazo con < 30 pares (solo descriptivos).
**Tolerancia y semilla.** 1e-8 · entero del plan.
**Referencia ingenua.** RI-PA, RI-UV, RI-MH, RI-TB según el pronóstico.
**Referencias.** TMB-11 · DOC-MOT-0091, DOC-MOT-0092, DOC-MOT-0093, DOC-MOT-0094, DOC-MOT-0095, DOC-MOT-0097, DOC-MOT-0098, DOC-MOT-0105.
**Prioridad y madurez.** P0 · IMPLEMENTADO (heredado).

### FC-CAL-001 · Calibración y fiabilidad

**Identificación.** v2.0 · VIGENTE · MC-B10 · Mapa: área 64. Conservada del Bloque A.
**Perfiles y horizontes.** TRANSVERSAL · H1–H4.
**Propósito.** ¿Ocurren los sucesos con la frecuencia que dicen las probabilidades?
**Entradas mínimas.** ≥ 50 pares (≥ 100 recomendados); para PIT, ≥ 50 distribuciones.
**Método.** Curva de fiabilidad (10 tramos con n ≥ 200; 5 por cuantiles si no); ECE y MCE; ECE nulo (5 000 simulaciones bajo calibración perfecta; media y q90); recalibración logística (a, b) con IC; PIT; cobertura de intervalos.
**Parámetros.** tramos (auto); simulaciones_nulo (5 000).
**Salidas.** TABLA y SERIE. `estimacion_estadistica`.
**Supuestos y limitaciones.** Con n ≈ 50 el ECE de un pronosticador perfecto ronda 0,12.
**Validaciones.** Pronosticador sintético calibrado dentro del nulo. Rechazo con < 30 pares.
**Tolerancia y semilla.** 1e-8; 1e-6 en el nulo · entero del plan.
**Referencia ingenua.** RI-TB (climatología: calibrada y sin resolución).
**Referencias.** TMB-11 · MBM-0233, DOC-MOT-0420, DOC-MOT-0422.
**Prioridad y madurez.** P0 · IMPLEMENTADO (heredado).

### FC-CERT-001 · Insumos del certificado de probabilidad

**Identificación.** v1.0 · VIGENTE · MC-B10 · Mapa: área 65.
**Perfiles y horizontes.** TRANSVERSAL · H1–H4.
**Propósito.** Preparar la tabla con la que el Evaluador decide el certificado de probabilidad de una celda (R13; 12.3 y Anexo A).
**Entradas mínimas.** Salidas de FC-EVAL-001 y FC-CAL-001 por celda; número de celdas evaluadas a la vez.
**Método.** Por celda: n; BSS y extremo inferior del IC 90 %; ECE, q90 nulo y comparación con 0,15; p-valores y corrección de Holm entre celdas; semáforo por condición (sin emitir certificado).
**Parámetros.** umbrales (Anexo A, F10).
**Salidas.** TABLA por celda. `estimacion_estadistica`.
**Supuestos y limitaciones.** El certificado es del Evaluador.
**Validaciones.** Holm monótono. Rechazo con celdas sin referencia ingenua.
**Tolerancia y semilla.** 1e-8 · entero del plan.
**Referencia ingenua.** RI-TB.
**Referencias.** TMB-11 · DOC-MOT-0420.
**Prioridad y madurez.** P0 · DOCUMENTADO.

### RK-IC-001 · IC de rango

**Identificación.** v1.0 · VIGENTE · MC-B10 · Mapa: área 66.
**Perfiles y horizontes.** Todos los SEL- · H2–H4.
**Propósito.** Capacidad del ranking: correlación de Spearman entre S y la rentabilidad posterior relativa al universo (Anexo C).
**Entradas mínimas.** Ranking congelado (S y componentes en la entrega); universo *point-in-time* con rentabilidades posteriores en el horizonte, incluidas las de exclusión.
**Método.** `ρ_Spearman(S_i, R_i − R̄_EW)`; IC por Fisher con factor 1,06; IC de rango por componente; entre rankings, media con t de Newey-West y bootstrap.
**Parámetros.** horizonte; costes (netos | brutos, declarado).
**Salidas.** TABLA por ranking y agregada. `estimacion_estadistica`.
**Supuestos y limitaciones.** Universos pequeños dan IC amplios.
**Validaciones.** Ranking aleatorio ⇒ IC ≈ 0. Rechazo con universo superviviente (`UNIVERSO_SESGADO`).
**Tolerancia y semilla.** 1e-8 · entero del plan.
**Referencia ingenua.** RI-RA, RI-F1.
**Referencias.** TMB-11, TMB-07 · MBM-0111, DOC-MOT-0063.
**Prioridad y madurez.** P0 · DOCUMENTADO.

### RK-TOPN-001 · Exceso y acierto del top-N

**Identificación.** v1.0 · VIGENTE · MC-B10 · Mapa: área 66.
**Perfiles y horizontes.** Todos los SEL- · H2–H4.
**Propósito.** Rentabilidad del top-N frente a la media equiponderada del universo cribado y tasa de acierto (12.1).
**Entradas mínimas.** Las de RK-IC-001 y la composición del top-N entregado.
**Método.** `X = R̄_top-N − R̄_EW` por ranking; media con IC por bootstrap; tasa de acierto (fracción del top-N sobre la mediana del universo) con IC de Wilson; contribución por componente (Fama-MacBeth del exceso sobre percentiles de componentes).
**Parámetros.** B (2 000).
**Salidas.** TABLA. `estimacion_estadistica`.
**Supuestos y limitaciones.** El top-N incluye solo prioritarios y secundarios del top; las decisiones del Broker no alteran la medición (7.8).
**Validaciones.** Top-N = universo ⇒ X = 0. Rechazo con universo superviviente.
**Tolerancia y semilla.** 1e-8 · entero del plan.
**Referencia ingenua.** RI-EQ, RI-RA, RI-F1.
**Referencias.** TMB-11 · DOC-MOT-0063.
**Prioridad y madurez.** P0 · DOCUMENTADO.

### RK-CERT-001 · Insumos del certificado de ranking

**Identificación.** v1.0 · VIGENTE · MC-B10 · Mapa: área 65.
**Perfiles y horizontes.** Todos los SEL- · H2–H4.
**Propósito.** Preparar la tabla con la que el Evaluador decide el certificado de ranking de un playbook × horizonte (12.3).
**Entradas mínimas.** Salidas de RK-IC-001 y RK-TOPN-001 de todos los rankings resueltos de la celda.
**Método.** n de rankings; IC de rango medio y extremo inferior del IC 90 %; exceso medio y extremo inferior; comparación con RI-F1; semáforo por condición (≥ 30; > 0; > 0); Holm si hay varias celdas.
**Parámetros.** umbrales (Anexo A).
**Salidas.** TABLA. `estimacion_estadistica`.
**Supuestos y limitaciones.** Rankings solapados en el tiempo no son independientes (bloques).
**Validaciones.** Coherencia con RK-IC-001. Rechazo con < 15 rankings (solo descriptivos).
**Tolerancia y semilla.** 1e-8 · entero del plan.
**Referencia ingenua.** RI-RA, RI-F1.
**Referencias.** TMB-11.
**Prioridad y madurez.** P0 · DOCUMENTADO.

### BT-SEL-001 · Backtesting de selección sin sesgos

**Identificación.** v1.0 · VIGENTE · MC-B10 · Mapa: áreas 67, 72.
**Perfiles y horizontes.** Todos los SEL-; PERF-B-FACT · H2–H4.
**Propósito.** Evaluar retrospectivamente una regla de selección o un factor sin sesgo de supervivencia ni de anticipación (PERF-B-FACT; validación del playbook; 18.4 del Documento 0).
**Entradas mínimas.** Universos *point-in-time* por fecha; precios con dividendos; rentabilidades de exclusión; fundamentales con fecha de publicación; reglas fijadas antes de la prueba; costes.
**Método.** (i) Reconstrucción del universo en cada fecha. (ii) Señales con datos conocibles en esa fecha (fundamentales con su publicación o cierre + 3 meses; macro por *vintage*). (iii) Carteras y rentabilidades netas de costes. (iv) Rentabilidad de exclusión (imputación declarada y sensibilidad). (v) División temporal con embargo. (vi) Sharpe deflactado, PBO, *Reality Check*/SPA; número de configuraciones probadas.
**Parámetros.** rebalanceo; costes; imputacion_exclusion (−30 % por rendimiento, declarada).
**Salidas.** TABLA y SERIE: rentabilidades, exceso frente a RI-EQ, IC de rango, DSR, PBO. `estimacion_estadistica`.
**Supuestos y limitaciones.** El pasado no garantiza el futuro; capacidad.
**Validaciones.** Universo con supervivientes eliminados artificialmente: el exceso debe caer al restaurarlos. Rechazo sin universo *point-in-time* (`UNIVERSO_SESGADO`) o con datos posteriores a cada fecha (`FUGA_INFORMACION`).
**Tolerancia y semilla.** 1e-8 · entero del plan.
**Referencia ingenua.** RI-EQ, RI-F1, RI-RA.
**Referencias.** TMB-11, TMB-14 · DOC-MOT-0099, DOC-MOT-0100, DOC-MOT-0101, DOC-MOT-0102, DOC-MOT-0124, DOC-MOT-0125, DOC-MOT-0417, DOC-MOT-0468, DOC-MOT-0469, MBM-0271, MBM-0272, MBM-0273.
**Prioridad y madurez.** P0 · DOCUMENTADO.

### BT-DSR-001 · Sharpe probabilístico y deflactado

**Identificación.** v2.0 · VIGENTE · MC-B10 · Mapa: área 68. Conservada del Bloque A.
**Perfiles y horizontes.** PERF-B-FACT; TRANSVERSAL · no aplica.
**Propósito.** Probabilidad de que un Sharpe observado supere a un umbral, corrigiendo por asimetría, curtosis y número de ensayos.
**Entradas mínimas.** Rentabilidades de la estrategia; número de configuraciones probadas y varianza de sus Sharpe.
**Método.** PSR; `SR_0` esperado máximo de N ensayos; DSR con γ₃ y γ₄.
**Parámetros.** N_ensayos (obligatorio).
**Salidas.** TABLA. `estimacion_estadistica`.
**Supuestos y limitaciones.** N subdeclarado invalida la corrección.
**Validaciones.** N = 1 ⇒ PSR. Rechazo sin N.
**Tolerancia y semilla.** 1e-8 · null.
**Referencia ingenua.** Sharpe = 0.
**Referencias.** TMB-11 · DOC-MOT-0101, DOC-MOT-0104, DOC-MOT-0418.
**Prioridad y madurez.** P1 · DOCUMENTADO.

### BT-PBO-001 · Probabilidad de sobreajuste del backtest (CSCV)

**Identificación.** v2.0 · VIGENTE · MC-B10 · Mapa: área 68. Conservada del Bloque A.
**Perfiles y horizontes.** PERF-B-FACT; TRANSVERSAL · no aplica.
**Propósito.** Probabilidad de que la configuración elegida en muestra quede por debajo de la mediana fuera de muestra.
**Entradas mínimas.** Matriz de rentabilidades de todas las configuraciones probadas.
**Método.** Validación cruzada combinatoriamente simétrica (S bloques; todas las combinaciones de S/2); logit del rango fuera de muestra; PBO.
**Parámetros.** S (16).
**Salidas.** TABLA: PBO, degradación del rendimiento. `estimacion_estadistica`.
**Supuestos y limitaciones.** Requiere todas las configuraciones probadas.
**Validaciones.** Configuraciones aleatorias ⇒ PBO ≈ 0,5. Rechazo con < 10 configuraciones.
**Tolerancia y semilla.** 1e-8 · null.
**Referencia ingenua.** PBO = 0,5.
**Referencias.** TMB-11 · DOC-MOT-0102, DOC-MOT-0415.
**Prioridad y madurez.** P1 · DOCUMENTADO.

### EVL-TIME-001 · Modelo de tiempos (p50 y p80)

**Identificación.** v1.0 · VIGENTE · MC-B10 · Mapa: área 69.
**Perfiles y horizontes.** TRANSVERSAL · no aplica.
**Propósito.** Estimar p50 y p80 de tiempo y UC por nodo del grafo del plan para la estimación de F0 y la puerta de tiempo (9.9; Anexo A). El umbral de 30 minutos no es un parámetro.
**Entradas mínimas.** Registro de F1 con tiempos por nodo de ≥ 20 peticiones.
**Método.** Regresión cuantílica (τ = 0,5; 0,8) de `ln(minutos)` sobre tipo de tarea, dimensión × profundidad, tipos de activo, tamaño del universo, nivel y vueltas de auditoría; validación fuera de muestra; cobertura empírica del p80.
**Parámetros.** reestimacion (mensual con ≥ 20 nuevas).
**Salidas.** TABLA de coeficientes; predicciones por nodo; cobertura. `estimacion_estadistica`.
**Supuestos y limitaciones.** Cambios de carga y de modelos de lenguaje.
**Validaciones.** Cobertura del p80 en [0,70; 0,90] o advertencia. Rechazo con < 20 peticiones.
**Tolerancia y semilla.** 1e-6 · null.
**Referencia ingenua.** Mediana histórica por tipo de nodo.
**Referencias.** TMB-14, TMB-02.
**Prioridad y madurez.** P1 · DOCUMENTADO.

### FC-HITO-001 · Evaluación de H5 por hitos intermedios (V2.1)

**Identificación.** v1.0 · VIGENTE · MC-B10 · Mapa: área 80.
**Perfiles y horizontes.** TRANSVERSAL · H5 (hitos con fecha a 1–5 años).
**Propósito.** Resolver los hitos H5 congelados en F4 y medir la capacidad de la máquina de proyecciones H5 (12.8 del Documento 0) para el Evaluador; insumo de la alerta `REVISION` por dos hitos críticos incumplidos.
**Entradas mínimas.** PRG-B de tipo `HITO_H5` con valor base, tolerancia, serie resoluble, `critico`, valor ingenuo (RI-LIN) fijado en la congelación; dato observado con `conocible_desde` ≤ fecha de corte.
**Método.** (i) Resolución: CUMPLIDO si `|obs − base| ≤ tolerancia` (o cruce del umbral en la dirección del hito); NO_CUMPLIDO; INDETERMINADO sin dato o con cambio de definición sin fallback. (ii) Por celda (tipo de objeto × tipo de activo): tasa de cumplidos con IC de Wilson y, con n < 30, Clopper-Pearson; **conglomerado por tesis** (bootstrap por tesis). (iii) **Desvío** `δ = ln(obs/base)` y `δ_ing = ln(obs/ingenuo)`; ganancia frente a la ingenua `G = media(|δ_ing|) − media(|δ|)` con IC por bootstrap por tesis. (iv) Señal por tesis: número de hitos críticos NO_CUMPLIDO (≥ 2 ⇒ alerta).
**Parámetros.** nivel_IC (90 %); B (2 000).
**Salidas.** TABLA por hito (resultado, δ, δ_ing); TABLA por celda (tasa con IC, G con IC, n de tesis); lista de tesis con ≥ 2 críticos incumplidos. `estimacion_estadistica`. **Nunca** produce insumos de certificado de probabilidad (R13).
**Supuestos y limitaciones.** Hitos de una misma tesis correlacionados; muestras pequeñas durante años; un hito no discriminante (DIF-H5-001) se reporta aparte y no cuenta en G.
**Validaciones.** Fuga: dato posterior a la fecha de corte ⇒ `FUGA_INFORMACION`; hito redefinido tras la congelación ⇒ rechazo (R14); caso de control con trayectorias sintéticas.
**Tolerancia y semilla.** 1e-6 · entero del plan.
**Referencia ingenua.** RI-LIN.
**Referencias.** TMB-11, TMB-03 · DOC-MOT-0095, DOC-MOT-0111, DOC-MOT-0110.
**Prioridad y madurez.** P1 · DOCUMENTADO.

### EVL-PV-001 · Evaluación de puertas de viabilidad y de seguimientos encargados (V2.1)

**Identificación.** v1.0 · VIGENTE · MC-B10 · Mapa: área 81.
**Perfiles y horizontes.** TRANSVERSAL · horizonte principal de cada REC-B (H1–H5).
**Propósito.** Calcular para el Evaluador (12.7) los **falsos negativos** de PV1–PV3 y el resultado de las continuaciones forzadas, y la calidad de los **semáforos** y recomendaciones de los seguimientos encargados (N1-SEG).
**Entradas mínimas.** (a) Puertas: REC-B `DETENIDO_EN_PUERTA` y REC-B que superaron la puerta en la misma celda, con indicador del ámbito, referencia (9.11), horizonte principal y fecha; continuaciones forzadas (F1). (b) Seguimientos: CIC-B con semáforo y recomendación (F11) y estado confirmado posterior (alertas del Vigía, invalidaciones, análisis posteriores).
**Método.** (a) Exceso anualizado en EUR del indicador frente a su referencia en el horizonte principal; **falso negativo** si > 10 pp (F10); tasa por puerta y celda con IC de Wilson; diferencia de exceso medio detenidos − superados con IC por bootstrap por conglomerados de fecha; atribución por criterio fallido; función de coste `L = FN·c_FN − minutos_ahorrados·c_t` solo si el operador fija `c_FN` y `c_t`. (b) Matriz de confusión semáforo × estado confirmado; **kappa ponderado** (pesos lineales); tasa de omisiones (VERDE seguido de invalidación) y de falsas alarmas (ROJO no confirmado); antelación en ciclos; coste por ciclo y ciclos sin novedad.
**Parámetros.** umbral_FN (10 pp, F10); pesos_kappa (LINEALES); B (2 000).
**Salidas.** TABLA por puerta y celda; TABLA por SEG-B y agregada. `estimacion_estadistica`.
**Supuestos y limitaciones.** Sin indicador invertible del ámbito la parada es `NO_EVALUABLE`; sin grupo de comparación no hay tasa base (no se publica la tasa sola); el estado confirmado de un ciclo puede tardar varios ciclos.
**Validaciones.** Universo de REC-B completo (todas las detenidas y superadas de la celda, también las descartadas por el Broker); fuga controlada; caso de control con puertas sintéticas de tasa conocida.
**Tolerancia y semilla.** 1e-6 · entero del plan.
**Referencia ingenua.** RI-PA (exceso nulo) para las puertas; semáforo constante (siempre VERDE) para los seguimientos.
**Referencias.** TMB-11, TMB-14 · DOC-MOT-0095, DOC-MOT-0124, MBM-0271.
**Prioridad y madurez.** P1 · DOCUMENTADO.

### AUD-REX-001 · Re-ejecución independiente (CT-B-14)

**Identificación.** v2.0 · VIGENTE · instancia aislada del Motor con el módulo de la ficha original · Mapa: área 73. Conservada del Bloque A.
**Perfiles y horizontes.** TRANSVERSAL · no aplica.
**Propósito.** Reproducir un artefacto en aislamiento y clasificar las diferencias.
**Entradas mínimas.** `calc_id` con artefacto completo (ficha y versión, datos con hash, universo, transformaciones, semilla, redondeo); tolerancia fijada antes.
**Método.** Reconstrucción de lo hecho en instancia distinta; comparación al cerrar; categoría (DATOS_DISTINTOS, CONVENCION_DISTINTA, SEMILLA_DISTINTA, UNIVERSO_DISTINTO, ERROR_IMPLEMENTACION, ERROR_REDONDEO, SIN_CAUSA_CLARA); `altera_conclusion` si cambia un umbral, el corte del top-N o `FRONTERA`.
**Parámetros.** tolerancia (de la ficha original).
**Salidas.** Informe CT-B-14. `determinista`.
**Supuestos y limitaciones.** No corrige el original; un posible error de método se anota aparte.
**Validaciones.** Artefacto incompleto ⇒ `ARTEFACTO_INCOMPLETO`.
**Tolerancia y semilla.** La de la ficha original · la del original.
**Referencia ingenua.** RI-NA.
**Referencias.** TMB-14 · MBM-0268, MBM-0269.
**Prioridad y madurez.** P0 · IMPLEMENTADO (heredado).

---

## 16. Pruebas de regresión, casos de control y orden de implantación

1. **Casos de control por ficha** (campo «Validaciones»): se ejecutan tras cada cambio de versión de método o de ficha; un fallo devuelve la ficha a `EN_REVISION` y se registra en «Incidencias y propuestas».
2. **Paso a IMPLEMENTADO**: casos de control superados en el ejecutor del Bloque B y registrados en RC. Las 22 fichas heredadas se reverifican primero (prioridad P0).
3. **Paso a VALIDADO**: batería de `09_Pruebas` con evidencia, incluidos datos reales por tipo de objeto y de activo, datos insuficientes, universos pequeños y heterogéneos, y —para SCR-*, RK-* y BT-SEL-001— un backtesting de rankings con universo *point-in-time* (18.4 del Documento 0).
4. **SCR-S-001 y SCR-AEC-001** se prueban contra HT-03 con el conjunto común de casos de `10_Herramientas`; cualquier diferencia bloquea ambas hasta su resolución.
5. **SCR-ROB-001**: universo sintético con orden conocido (IC degenerado sin ruido), candidato en la frontera conocida (`FRONTERA` = sí), comprobación de que cada réplica recalcula el universo completo.
6. **FC-*, RK-* y BT-SEL-001** se prueban con pronosticadores y rankings sintéticos de propiedades conocidas (calibrado, sobreconfiado, sin resolución; ranking aleatorio; universo con supervivientes eliminados) antes de usarse en insumos de certificado (R13).
7. **Frontera con los Bloques C.x**: la batería incluye, para VAL-DCF-001, VAL-REV-001 y VAL-MULT-001, una petición de precio objetivo que debe rechazarse con `PRECIO_OBJETIVO_FUERA_DE_ROL`, y una valoración de candidato que debe salir con `uso: para_ordenacion`.
8. **Fuga**: para cada ficha con `fecha_corte`, un caso con un dato posterior que debe rechazarse con `FUGA_INFORMACION`.
9. **Orden de implantación recomendado**: (a) reverificación de las 22 heredadas; (b) canal de selección P0 (SCR-NORM-001, SCR-PUR-001, SCR-S-001, SCR-AEC-001, SCR-ROB-001, SCR-DUP-001, SCR-LIQ-001, QLT-ACC-001, ECO-EXPO-001); (c) tesis y máquina P0 (MKT-DIM-001/002, MKT-TRI-001, IO-CONC-001, IO-MARG-001, SUP-BOTT-001, VAL-DCF-001, VAL-REV-001, VAL-MULT-001, VAL-ROIC-001, VAL-WACC-001, VAL-PROJ-001, ECO-CYC-001, SIM-IC-001, SIM-SCN-001, SIM-TOR-001, RISK-STR-001); (d) evaluación P0 (FC-CERT-001, RK-IC-001, RK-TOPN-001, RK-CERT-001, BT-SEL-001); (e) P1 de valoración específica por tipo de activo (al menos una por SEL-); (f) P2 bajo demanda acreditada por RC. **V2.1**: `VC-DESG-001` y `VC-BOT-001` entran en el grupo (c) (son P0: sin ellas no hay entregable 6 ni PV3 reconstruible); `EMG-PEM-001`, `DIF-H5-001`, `FC-HITO-001` y `EVL-PV-001` en el grupo (e).
10. **Casos de control V2.1**: AE y PCB contra HT-03 con el conjunto común de `10_Herramientas` (igualdad exacta); árbol con conciliación de tamaños conocidos; indicadores sintéticos con 0, 2 y 5 rojos y un par de indicadores correlacionados (doble cómputo); PEM con NA redistribuido; trayectoria H5 con hitos y su ingenua; petición de probabilidad numérica H5 rechazada (`PROBABILIDAD_NO_CERTIFICABLE`); puertas sintéticas con tasa de falsos negativos conocida y grupo de comparación.

## 17. Registro de cambios

| Versión | Fecha | Cambio |
|---|---|---|
| V2.1 | 03/11/2026 | Cambios del propietario B1, B3, B4 y B6 (Anexo E.4 del Documento 0): seis fichas nuevas, todas DOCUMENTADO — `VC-DESG-001` (desglose jerárquico, conciliación, margen anómalo y AE; MC-B03), `VC-BOT-001` (nueve indicadores en semáforo, severidad, persistencia, PCB y materialidad; MC-B04), `EMG-PEM-001` (PEM y pureza de la vía de exposición; MC-B07), `DIF-H5-001` (trayectorias estructurales H5 e hitos; MC-B02), `FC-HITO-001` (evaluación por hitos; MC-B10) y `EVL-PV-001` (falsos negativos de las puertas y calidad de los seguimientos; MC-B10); horizonte H5 en la ficha estándar y en la cobertura; referencia ingenua RI-LIN; código de rechazo `PROBABILIDAD_NO_CERTIFICABLE`; áreas 76–81 del Mapa. `catalog_version` 2.1. |
| V2.0 | 03/11/2026 | Primer catálogo propio del Motor del Bloque B (AG-B16): 106 fichas en diez módulos MC-B01…MC-B10 y la re-ejecución aislada; conserva 37 fichas útiles del Catálogo V5.0 del Bloque A con su `ficha_id` (22 implementadas en su ejecutor), desarrolla o integra otras 6 (ACC-VAL-001, TEM-DIFF-001, CMD-INV-001, SCN-H-001, MON-FIX-001 y las fichas TCV del Bloque A) y añade las propias de dimensionado, difusión, organización industrial, costes y aprendizaje, econometría sectorial, valoración para ordenar, cribado y ranking, escenarios con dependencias, redes input-output y evaluación de rankings. |
