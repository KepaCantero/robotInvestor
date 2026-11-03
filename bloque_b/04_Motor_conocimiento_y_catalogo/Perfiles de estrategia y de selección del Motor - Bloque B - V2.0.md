# Perfiles de estrategia y de selección del Motor de Cálculo Avanzado de Mercados (AG-B16)

**Bloque B · Robot Investor · Versión V2.0 · 03/11/2026 · actualizado V2.1 (03/11/2026)** · Subordinado al Documento 0 del Bloque B, óptima V2.1. V2.1: `VC-DESG-001` y `VC-BOT-001` en todo perfil con D4 en P2 o P3 (8.4 del Documento 0) para el entregable 6 y la puerta PV3; `EMG-PEM-001` donde AG-B24 está activado; `DIF-H5-001` y `FC-HITO-001` con horizonte principal H5; insumos de las puertas PV1–PV3 por capa (sección 2 bis); columna H5 en la matriz de la sección 23.

Archivo **CC** (propietario: operador, tipo 3; el Motor propone). Lectores: AG-B16 y sus módulos, AG-B19, AG-B12 (Seleccionador), AG-B13 (Prospectiva), AG-B21 (Orquestador técnico). Comparte códigos con el «Catálogo de cálculos del Motor - Bloque B - V2.0» y con el «Mapa de conocimientos del Motor - Bloque B - V2.0».

---

## 1. Propósito y reglas de uso

1.1. Un perfil es la **especialización del Motor** para una configuración de la estrategia de análisis (8.1 del Documento 0):

- **Perfiles de estrategia PERF-B-** (uno por tipo de objeto, 2.5 y 8.4): qué preguntas cuantitativas importan, qué fichas se ejecutan por defecto en cada plan, qué datos mínimos se exigen, qué guardas protegen contra los errores típicos del tipo de objeto y cuándo abstenerse.
- **Perfiles de selección SEL-** (uno por tipo de activo, 2.6 y 8.5): cómo se calculan la pureza y cada componente de S, qué métricas entran, en qué dirección, qué alertas se miden y con qué fichas, y qué se calcula en cada nivel de servicio.

El perfil decide **cómo se calcula bien**; la pregunta y su valor informativo los decide el solicitante (Director, especialistas, Seleccionador, Prospectiva).

1.2. **Reglas.**

1. El Orquestador de Cálculo clasifica cada petición CT-B-13 por tipo de objeto (perfil PERF-B-) y, si afecta a candidatos, por tipo de activo (perfil SEL-); si la petición trae el perfil, lo verifica; si no, lo infiere y lo declara.
2. Una ficha solo se aplica a los perfiles que declara compatibles; aplicar otra exige justificación en el plan.
3. **Composición**: los perfiles se componen (un MERCADO_GEOGRAFICO con sector ancla añade PERF-B-CADENA, 8.4). Toda petición con candidatos usa además el SEL- de cada tipo de activo aplicable y MC-B10 para las referencias ingenuas.
4. El perfil **no añade operaciones** al Catálogo ni amplía horizontes: respeta la aplicabilidad de 8.6 del Documento 0 (una previsión en un horizonte «No» se rechaza con `HORIZONTE_NO_APLICABLE`; «Limitado» exige frecuencia, liquidez y catalizador declarados).
5. **Los parámetros del Documento 0 mandan**: pesos de S, mínimos PC2, umbrales de alerta, filtros de liquidez, top-N y reglas de diversidad son los vigentes en F10 (iniciales de 8.5 y del Anexo A; calibrables por el Evaluador dentro de bandas, salvo el top-N, que es parámetro de servicio: lo fija el Broker y el Evaluador solo propone cambios). Este archivo indica **qué métricas y fichas** los alimentan, no los cambia.
6. **Pesos internos** de las métricas dentro de cada componente: los del playbook del Seleccionador; en su defecto, **equiponderados** y declarados en el artefacto.
7. **Madurez** (R26): todos los perfiles están **documentados**; la madurez de cada ficha que citan consta en el Catálogo. Mientras una ficha esté DOCUMENTADO, el Motor ofrece la alternativa implementada más próxima con la limitación declarada o rechaza con `METODO_NO_IMPLEMENTADO`.
8. **Frontera con los Bloques C.x** (R7): toda valoración de candidato sale `para_ordenacion`; ningún perfil produce precios objetivo ni valoraciones individuales completas.
9. Concluir «datos insuficientes» o «método no aplicable» es un resultado legítimo y registrable.

## 2. Planes y cálculos por defecto por nivel de servicio

| Nivel (7.2) | Plan del Motor | Qué se calcula por defecto | IC de S y de rango | Sensibilidad |
|---|---|---|---|---|
| **N0** Consulta | Sin cálculo nuevo (o MIN si una cifra entregada debe reconstruirse) | Recuperación de artefactos de RC | — | — |
| **N1** Rápido | MIN; STD solo en D9, D12 y la cifra decisiva | Métodos «N1» de cada perfil; S provisional sobre el universo; S completo del top-N (3 por tipo) | Solo perturbación de pesos, B = 200 | Tornado de las 3 premisas críticas |
| **N2** Estándar | STD | Métodos «N2» de cada perfil; S completo de los 2 × top-N (GC3) | Insumos + pesos, B = 1 000 | Tornado completo; referencia ingenua; consistencia premisas–conclusiones |
| **N3** Exhaustivo | EXT en dimensiones con peso modulado ≥ 9 y en finalistas; STD en el resto | Métodos «N3» de cada perfil; S completo de los 2 × top-N (10 + 5 alternativas) | Insumos + pesos + variantes de winsorización y neutralización, B = 2 000 | Morris + Sobol; validación fuera de muestra; *vintages*; estabilidad entre regímenes y semillas |
| **PERS** | Según el tiempo autorizado | ≤ 10 min como N1; el resto como N2; recorte declarado | Como el nivel equivalente | Como el nivel equivalente |

**Bandas marginales** (siempre EXT para los componentes decisivos): ámbito a ≤ 5 puntos de un umbral; candidato a ≤ 3 puntos de 65, 50 o del corte del top-N (Anexo A). **Controles de integridad** (doble pasada, réplica de HT-03, fuga, supervivencia) nunca se recortan (R23).

**N1-SEG (ciclo de seguimiento encargado, V2.1).** Plan MIN: solo el delta de las cifras de las dimensiones clave y de las señales del encargo con su referencia ingenua (RI-UV); S de los candidatos vigentes solo si una métrica de su componente decisivo cambió más de su banda; sin nuevos universos ni rankings. Presupuesto ≈ 5 UC por ciclo.

## 2 bis. Cálculos por capa e insumos de las puertas de viabilidad (V2.1)

| Capa (7.10) | Qué calcula el Motor por defecto | Para qué puerta |
|---|---|---|
| 1 · Prueba de viabilidad | MIN: VAL-MULT-001 o VAL-REV-001 del agregado en **percentil de su historia de 10 años** (criterio «ya descontado»); SCR-LIQ-001 y la pureza disponible (SCR-PUR-001) sobre el **universo preliminar** de HT-11 (invertibilidad mínima: ≥ 1 instrumento que supera PC1; materialidad: capitalización o patrimonio invertible agregado y número de instrumentos) | PV1 |
| 2 · Núcleo | STD solo en las dimensiones líderes: IO-CONC-001 y IO-MARG-001 a nivel de macro-eslabón; MKT-DIM-001/002; VAL-ROIC-001; VAL-REV-001 preliminar (MIN); SCR-AEC-001 para A y E provisionales | PV2 |
| 3 · Profundización y selección | VC-DESG-001 (desglose y AE), VC-BOT-001 (indicadores y PCB), EMG-PEM-001 (si AG-B24 activado), canal de selección con S provisional y PC1–PC4 de las opciones por eslabón | PV3 |
| 4 · Contraste y veredicto | Máquina de proyecciones, escenarios, sensibilidades, referencias ingenuas, réplicas finales; en H5, DIF-H5-001 con hitos | — (G1–G4) |

Un análisis detenido en PV1 o PV2 no ejecuta las capas siguientes: los cálculos ya hechos quedan en RC y se reutilizan si el Broker fuerza la continuación (punto de control).

---

## 3. PERF-B-SECT — Sector o subsector (SECTOR)

**Ámbito.** Industria definida por lo que produce o el servicio que presta, con clasificaciones GICS, ICB o NACE como punto de partida corregido por exposición económica real.
**Preguntas cuantitativas.** ¿Cuán concentrado está y quién captura el valor (D4)? ¿Gana el sector más que su coste de capital y con qué estabilidad (D8)? ¿Qué crecimiento y márgenes descuenta el precio frente a lo plausible (D9)? ¿Cuán cíclico es (D7)? ¿Cómo responde la demanda a precio y renta (D2)?
**Dimensiones con peso alto en la matriz** (8.3.1): D4 13 · P3; D8 12 · P3; D9 12 · P3; D2 10 · P2.

| Nivel | Cálculos por defecto |
|---|---|
| N1 | IO-CONC-001 (eslabón crítico); VAL-MULT-001 del agregado frente a su historia; VAL-REV-001 del agregado (STD); RISK-DD-001 (escala 1–5); SIM-SCN-001 con escenarios deterministas (STD) |
| N2 | + IO-MARG-001; IO-SHARE-001; ECO-CYC-001; ECO-ELAS-001; VAL-ROIC-001; VAL-WACC-001; QLT-ACC-001 agregada; SIM-MC-001 + SIM-IC-001 sobre la máquina; SIM-TOR-001; RISK-STR-001 (histórico) |
| N3 | + ECO-PANEL-001 (márgenes sobre ciclo e insumos); IO-PROF-001; IO-LERN-001; RISK-STR-001 de márgenes e inverso; SIM-SOB-001 sobre el crecimiento implícito; RISK-RGC-001; validación fuera de muestra de las proyecciones |

**Datos mínimos.** Agregados contables ≥ 5 ejercicios con fecha de presentación; múltiplos del agregado ≥ 10 años (20 recomendados); rentabilidad total del índice sectorial ≥ 5 años mensual; cuotas de mercado con definición.
**Convenciones.** Índices de rentabilidad total neta en EUR; múltiplos adelantados por media armónica; beneficios normalizados en cíclicos; WACC común a todo el universo de candidatos.
**Referencias.** Comparación: índice sectorial o su ETF UCITS más líquido; ingenuas: RI-PA (rentabilidad relativa nula), RI-MH (múltiplo medio).
**Guardas.** Clasificación oficial ≠ exposición económica (usar pureza); PER bajo en máximos de ciclo; concentración del índice sectorial (peso de los 10 mayores); beneficios negativos excluidos de PER; valor terminal > 85 % del EV advertido.
**Abstención.** Agregados sin cuentas auditadas; sector sin índice con serie de rentabilidad total (D9 solo con múltiplos y advertencia).
**Composición habitual.** SEL-RV, SEL-FON, SEL-RF; + PERF-B-CADENA si el ámbito depende de un eslabón crítico.
**V2.1.** Con D4 en P2 o P3 (lo habitual en SECTOR): VC-DESG-001 y VC-BOT-001 (N1: eslabón crítico hasta actividad; N2: eslabones del plan; N3: cadena completa) y EMG-PEM-001 (AG-B24 activado por defecto). Con horizonte principal H5: DIF-H5-001 sobre la demanda del sector y contraste obligatorio con VAL-REV-001.

## 4. PERF-B-TEMA — Temática transversal (TEMATICA)

**Ámbito.** Tendencia que atraviesa varios sectores y cuya captura exige medir la exposición de cada empresa o vehículo.
**Preguntas cuantitativas.** ¿Cuánto mide de verdad el mercado y a qué ritmo se adopta (D2)? ¿Cómo evolucionan los costes de la tecnología (D5)? ¿Quién captura el valor (D4)? ¿Qué pureza tienen los vehículos y empresas «temáticos» (D1)? ¿Qué adopción y márgenes descuenta el precio de la cesta (D9)?
**Dimensiones con peso alto.** D2 13 · P3; D5 13 · P3; D4 12 · P3; D9 11 · P2; D1 8 · P2.

| Nivel | Cálculos por defecto |
|---|---|
| N1 | MKT-DIM-001 o MKT-DIM-002 (la vía con mejores datos) con banda; SCR-PUR-001 sobre el universo preliminar; VAL-REV-001 de la cesta (STD); escenarios deterministas de adopción |
| N2 | + MKT-TRI-001 (ambas vías y terceros); DIF-BASS-001 y DIF-LOG-001 (con m por escenarios si no hay inflexión); DIF-ANLG-001; IO-MARG-001; VAL-PROJ-001 completa; SIM-MC-001 + SIM-IC-001; SIM-TOR-001; FAC-CROWD-001 o SER-FLOW-001 (saturación narrativa) |
| N3 | + SUP-LRN-001 y SUP-LRN-002; NET-IO-001 y NET-SHOCK-001 (redes de proveedores); SCR-PUR-002 (texto) para candidatos sin segmentos; DIF-GEN-001 si hay generaciones; SIM-SOB-001 sobre la capitalización implícita; SER-HIER-001 si se proyectan segmentos y total |

**Datos mínimos.** Serie de adopción ≥ 8 periodos con aceleración observada (para difusión); ≥ 2 estimaciones de tamaño con raíz identificada; segmentos de ingresos de los candidatos (o método de estimación con validación).
**Convenciones.** Tamaño con año, moneda, precios, base, geografía y fuente; adopción en primeras adopciones o penetración, declarado; precio unitario decreciente por aprendizaje cuando proceda.
**Referencias.** Comparación: índice o ETF temático UCITS de referencia, y MSCI ACWI como contraste; ingenuas: extrapolación lineal y crecimiento constante para tamaños; RI-PA para la cesta.
**Guardas.** TAM inflado de consultoras; pureza por nombre y no por ingresos (mínimo PC2 de cada SEL-); techo m mal identificado antes de la inflexión (escenarios, clase `juicio_experto`); difusión ≠ captura de valor; saturación narrativa (tope de 40 en A cuando D10 lo marca).
**Abstención.** Temática sin definición operativa (incluye/excluye); ningún candidato con pureza medible (PA8 lo evalúa el Director).
**Composición habitual.** SEL-RV, SEL-FON, SEL-IDX; + PERF-B-CADENA para cuellos.
**V2.1.** VC-DESG-001 y VC-BOT-001 si D4 en P2 o P3; EMG-PEM-001 (AG-B24 activado por defecto; pureza de la vía de exposición de matrices cotizadas y ETF temáticos); con horizonte principal H5 —frecuente en TEMATICA—, DIF-H5-001 con ≥ 3 hitos discriminantes y FC-HITO-001 para su evaluación.

## 5. PERF-B-GEO — Mercado geográfico (MERCADO_GEOGRAFICO)

**Ámbito.** Una economía o un bloque de economías como objeto de inversión.
**Preguntas cuantitativas.** ¿En qué régimen macro está y cuán sensible es el mercado al ciclo global, a tipos y a la divisa (D7)? ¿Qué rentabilidad esperada ofrece el mercado en EUR y qué descuenta (D9)? ¿Qué riesgos de país, divisa y jurisdicción soporta (D6, D12)? ¿Depende de un sector ancla (D4 por modulador)?
**Dimensiones con peso alto.** D7 17 · P3; D6 13 · P3; D9 13 · P3.

| Nivel | Cálculos por defecto |
|---|---|
| N1 | FX-REGIME-001 (macro de referencia); IDX-ERP-001 en EUR; VAL-MULT-001 (CAPE y PER adelantado frente a historia y a ACWI); RISK-DD-001; RISK-GEO-001 (divisa) |
| N2 | + ECO-CYC-001 (betas al ciclo global, tipos y divisa); ACC-ERP-001; RISK-GEO-001 completo (deuda, sostenibilidad externa); RISK-STR-001 (episodios del país); SIM-SCN-001 con régimen de referencia; ML-CLUS-001 frente a otros mercados |
| N3 | + RISK-RGC-001 (correlaciones por régimen y corrección de Forbes-Rigobon); ECO-LP-001 (respuesta a choques de tipos o materias primas); escenarios de convertibilidad y controles de capital; si hay sector ancla, métodos de PERF-B-CADENA y NET-IO-001 del país |

**Datos mínimos.** Índice amplio del país en rentabilidad total ≥ 10 años; CAPE o beneficios para 10 años; tipo de cambio ≥ 10 años; datos fiscales y externos (FMI, Banco Mundial, BIS).
**Convenciones.** Todo en EUR con la conversión declarada y, si se pide, versión cubierta; composición sectorial del índice declarada al comparar valoraciones.
**Referencias.** Comparación: MSCI ACWI o índice regional amplio; ingenuas: RI-PA, RI-MH.
**Guardas.** Crecimiento del PIB ≠ rentabilidad bursátil; CAPE de mercados con mezclas sectoriales distintas; divisa dominante; controles de capital no modelados; datos fiscales con retraso.
**Abstención.** Mercado sin índice invertible desde el marco (2.7) o con controles de capital que impidan medir rentabilidades.
**Composición habitual.** SEL-IDX, SEL-FON, SEL-DIV, SEL-RF (soberanos); + PERF-B-CADENA con sector ancla.
**V2.1.** Con H5 (demografía, productividad, instituciones): DIF-H5-001 en su variante demográfica con hitos verificables; EMG-PEM-001 solo si AG-B24 se activa (condicional).

## 6. PERF-B-SEGM — Segmento de una clase de activo (SEGMENTO_DE_CLASE)

**Ámbito.** Subconjunto definido por características dentro de una clase (high yield europeo, cobre, REIT logísticos, DeFi, volatilidad, letras a 6–12 meses).
**Preguntas cuantitativas.** ¿Cuál es la valoración específica del segmento frente a su historia (diferencial, curva, descuento sobre NAV, cap rate, estructura de futuros, métricas de red) (D9)? ¿En qué régimen está (D7)? ¿Cómo está la oferta física o de emisión (D3)? ¿Quién compra y vende y con qué apalancamiento (D10)? ¿Qué estrés soporta (D12)?
**Dimensiones con peso alto.** D9 14 · P3; D7 13 · P3; D10 11 · P2; D3 10 · P2.

| Nivel | Cálculos por defecto |
|---|---|
| N1 | Ficha de valoración específica del segmento (FIR-SPREAD-001, CMD-CURVE-001, REI-NAV-001, FON-DISC-001, CHR-ONCHAIN-001, MON-YLD-001, TCV-CARRY-001 o DER-VRP-001) con percentil histórico; FX-REGIME-001; RISK-DD-001 |
| N2 | + VAL-RF-001 o equivalente de rentabilidad esperada; SUP-UTIL-001 o SUP-INV-001 (oferta física o de emisión); SER-FLOW-001; FX-BRK-001; RISK-STR-001; SIM-SCN-001 |
| N3 | + pérdida esperada por impago con escenarios de PD y LGD (RF); descomposición del roll yield (MP); DER-VRP-001 completo (superficie); RISK-RGC-001; ALT-DESMOOTH-001 si hay series tasadas; SIM-SOB-001 |

**Datos mínimos.** Serie de la métrica de valoración del segmento ≥ 5 años (10 recomendados); índice del segmento en rentabilidad total; datos de oferta (emisiones, inventarios, oferta nueva) con fecha.
**Convenciones.** Las del tipo de activo del segmento (convención de días y diferencial en RF; regla de enlace de futuros en MP; NAV EPRA en INM; UTC y 365 días en CRI; cotización monetaria en MON; DV01 en TCV).
**Referencias.** Comparación: índice del segmento (8.5 del Documento 0); ingenuas: RI-UV, RI-MH.
**Guardas.** Microestructura y liquidez del segmento; series suavizadas (desuavizar); diferenciales de referencias distintas no comparables; probabilidades neutrales al riesgo como reales; volumen lavado en cripto.
**Abstención.** Segmento sin índice ni serie de valoración ≥ 3 años.
**Composición habitual.** SEL- del tipo del segmento; SEL-FON para vehículos; SEL-DER y SEL-TCV cuando la tesis es un factor.

## 7. PERF-B-FACT — Estrategia o factor (ESTRATEGIA_FACTOR)

**Ámbito.** Prima de riesgo o estilo replicable (valor, tamaño, dividendos, calidad, carry de divisas, momento de materias primas).
**Preguntas cuantitativas.** ¿Existe la prima, con qué significación tras pruebas múltiples y con qué fundamento económico (D8)? ¿Está barato el factor (diferencial de valoración, D9)? ¿Está concurrido (D10)? ¿Cómo y cuánto colapsa (D12)? ¿Cuánta capacidad tiene (D2 reinterpretado)? ¿Sobrevive a un backtest sin sesgos?
**Dimensiones con peso alto.** D12 18 · P3; D9 17 · P3; D7 15 · P3; D10 15 · P3.

| Nivel | Cálculos por defecto |
|---|---|
| N1 | FAC-PREM-001 con datos publicados (Kenneth French u otro proveedor con metodología pública); FAC-SPREAD-001; RISK-DD-001 del factor |
| N2 | + FAC-CROWD-001; RISK-CRASH-001; FX-REGIME-001 y rentabilidad por régimen; BT-SEL-001 de la regla de implementación con universo *point-in-time*; BT-DSR-001; SCR-LIQ-001 (capacidad) |
| N3 | + BT-PBO-001; robustez entre regímenes y subperiodos; degradación de la señal tras su publicación; RISK-RGC-001; SIM-SCN-001 de colapso y recuperación |

**Datos mínimos.** Rentabilidades del factor ≥ 20 años mensuales (10 mínimo) o universo *point-in-time* para reconstruirlo; número de configuraciones probadas (obligatorio para DSR y PBO).
**Convenciones.** Carteras larga-corta con ponderación y rebalanceo declarados; rentabilidades netas de costes estimados; divisa EUR o cubierta declarada.
**Referencias.** Comparación: la implementación invertible más próxima (ETF UCITS del factor) o el índice amplio; ingenuas: prima nula, RI-F1.
**Guardas.** Prima arbitrada tras su publicación; sobreajuste (declarar ensayos; `t > 3` para factores nuevos); crowding; microcapitalizaciones que dominan la prima teórica pero no son invertibles; costes que eliminan la prima.
**Abstención.** Factor sin definición replicable o sin vehículo invertible desde el marco; backtest sin universo *point-in-time* (`UNIVERSO_SESGADO`).
**Composición habitual.** SEL-FON (vehículos del factor), SEL-IDX (índices de factor), SEL-DIV o SEL-MP para carry y momento.

## 8. PERF-B-CADENA — Eslabón o cuello de botella (CADENA_DE_VALOR)

**Ámbito.** Un eslabón concreto de una cadena productiva, especialmente si limita al conjunto.
**Preguntas cuantitativas.** ¿Es el eslabón realmente el cuello (holgura mínima) y cuánto persistirá (D3, 4d)? ¿Qué capacidad, utilización y costes tiene (D3)? ¿Cómo se reparte el margen a lo largo de la cadena (D4, 4a)? ¿Qué pasa aguas abajo si falla (4e, D12)? ¿Qué tecnología lo desatasca (D5)? ¿Qué dependencias geográficas tiene (D6)?
**Dimensiones con peso alto.** D4 17 · P3; D3 14 · P3; D2 10 · P2; D5 10 · P2; D8 10 · P2.

| Nivel | Cálculos por defecto |
|---|---|
| N1 | SUP-BOTT-001 (eslabón crítico, indicadores de tensión); **VC-BOT-001 (PCB del eslabón crítico)**; **VC-DESG-001 (eslabón crítico hasta actividad, AE)**; SUP-UTIL-001; IO-CONC-001 del eslabón; IO-MARG-001 aproximada; EMG-PEM-001 del eslabón crítico |
| N2 | + SUP-COST-001; NET-IO-001 (multiplicadores, *upstreamness*, modelo de precios); NET-SHOCK-001; NET-EXPO-001; IO-MARG-001 completa; **VC-DESG-001 y VC-BOT-001 de los eslabones del plan (insumos críticos de los eslabones con cuello)**; EMG-PEM-001 por eslabón; SIM-SCN-001 de resolución del cuello; VAL-REV-001 del agregado del eslabón |
| N3 | + SUP-LRN-001 (tecnología sustitutiva o de ampliación); SIM-BOTT-001 (persistencia por simulación, alimenta la persistencia de VC-BOT-001); **VC-DESG-001 hasta insumo o nodo crítico en toda la cadena**; IO-SHARE-001; RISK-STR-001 inverso (choque que resuelve o agrava el cuello); DIF-H5-001 si el horizonte principal es H5 (sustitución tecnológica y nueva capacidad) |

**Datos mínimos.** Capacidades por eslabón con fecha; coeficientes técnicos o tabla input-output con desagregación suficiente; tubería de proyectos; márgenes por eslabón con cobertura declarada.
**Convenciones.** Unidades físicas por eslabón; capacidad efectiva; probabilidades de fase declaradas.
**Referencias.** Comparación: índice o cesta del eslabón (o del sector que lo contiene); ingenuas: persistencia nula del cuello (resolución en la fecha nominal de la capacidad anunciada), RI-UV de la utilización.
**Guardas.** Persistencia del cuello sobreestimada; perdedores del eslabón ignorados; precio ≠ coste; capacidad anunciada ≠ existente; Ghosh no causal; eslabón diluido en un sector amplio de la tabla; **doble cómputo de indicadores de demanda correlacionados en la severidad del PCB**; tamaños de eslabones sucesivos sumados en ingresos y no en valor añadido.
**Abstención.** Sin datos de capacidad ni indicadores de tensión; eslabón sin participantes invertibles (el mapa de cobertura lo declara como vigilancia informativa).
**Composición habitual.** SEL-RV (participantes del eslabón y proveedores), SEL-FON, SEL-MP (insumos críticos).

---
## 9. Perfiles de selección: estructura común

Cada SEL- recibe el universo del Seleccionador (construido por HT-11 tras PC1, con su fecha y sus exclusiones motivadas); mide la pureza para PC2 y normaliza dentro del **universo cribado** (candidatos que superan PC1–PC4, Anexo C), y devuelve, por candidato: pureza con intervalo y marca respecto al mínimo PC2; métricas en bruto, winsorizadas (2,5/97,5) y en percentil (rango medio) dentro del universo o del subgrupo; componentes 0–100; S (réplica de HT-03); IC 90 % de S y del rango; `P(top-N)`; `FRONTERA`; valores de alerta frente a sus umbrales; duplicados y apuestas independientes; referencia ingenua del ranking. **Dirección**: (+) más es mejor; (−) métrica inversa (se percentila `100 − pct`).

**Cálculos comunes por nivel** (además de los propios de cada SEL-):

| Nivel | Cribado (todo el universo) | Finalistas (2 × top-N, GC3) |
|---|---|---|
| N1 | SCR-PUR-001 (método disponible), SCR-NORM-001, SCR-S-001 provisional (plan MIN) | SCR-ROB-001 solo pesos (B = 200); SCR-DUP-001 |
| N2 | Igual | Componentes completos (STD); SCR-ROB-001 insumos + pesos (B = 1 000); SCR-DUP-001; ML-CLUS-001; segunda pasada en banda marginal |
| N3 | Igual, con neutralización por subgrupo comprobada | Como N2 con B = 2 000, variantes de winsorización y neutralización, segunda vía de pureza en todos los finalistas, RISK-STR-001 inverso del candidato |

## 10. SEL-RV — Renta variable (→ C.1)

**Subgrupo por defecto.** Industria GICS (o subindustria si n ≥ 10).
**Pureza (PE, 20).** SCR-PUR-001: % de ingresos y % de EBIT del ámbito (segmentos XBRL o ESEF); si no hay desglose, estimación por líneas de producto, por ECO-EXPO-001 (regresión sobre el índice del ámbito ortogonalizado) o por SCR-PUR-002; PE = máximo de las dos medidas publicadas, o la estimada con su intervalo. **PC2**: 25 % de ingresos o de EBIT; *pure play* ≥ 50 %.

| Componente (peso) | Métricas (dirección) | Ficha |
|---|---|---|
| QL (20) | ROIC medio a 3 años (+) y su σ a 5 años (−); margen bruto y operativo frente a la mediana del subgrupo (+); deuda neta/EBITDA (−); conversión de caja FCF/BN (+); Piotroski F (+) | VAL-ROIC-001, QLT-ACC-001 |
| VA (20) | Residuo de múltiplos garantizados en el subgrupo (−, barato es mejor) o percentil del PER/EV-EBITDA adelantado (−); percentil del múltiplo frente a su historia a 10 años (−); brecha de crecimiento implícito frente a plausible (−); rentabilidad del flujo libre (+) | VAL-MULT-001, VAL-REV-001, VAL-DCF-001 (`para_ordenacion`) |
| MO (15) | Momento 12-1 (+); revisiones netas de BPA a 3 meses (+) | ACC-MOM-001 |
| RI (15) | Volatilidad a 1 año (−); beta al mercado (−); deuda neta/EBITDA (−); concentración de clientes y proveedores (−); dilución anual (−); alertas no críticas (−) | FX-VOL-001, ECO-CYC-001, IO-BARG-001, QLT-ACC-001 |
| LA (10) | ADV en EUR a 3 meses (+); Amihud (−); capital flotante (+) | SCR-LIQ-001 |
| CO | NA | — |

**Alertas medidas** (valor y umbral; la clasificación es del playbook): M de Beneish > −1,78; Z de Altman < 1,8 (no financieras); devengos altos (decil superior del universo); dilución > 10 %/año; posiciones cortas > 10 % del flotante (SER-FLOW-001).
**Referencias.** Ámbito: índice sectorial o temático (o su ETF UCITS más líquido). Ranking: RI-EQ, RI-RA, RI-F1 (capitalización y momento).
**Guardas.** Financieras: P/VC frente a ROE en lugar de EV; beneficios negativos fuera de PER; supervivencia en universos históricos; neutralización obligatoria si el universo mezcla industrias.
**Abstención.** Candidatos con > 2 componentes NE ⇒ `DATOS_INSUFICIENTES` (PC3).

## 11. SEL-RF — Renta fija (→ C.2)

**Subgrupo por defecto.** Calificación (IG/HY y escalón) × sector; vencimiento en tramos.
**Pureza (PE, 15).** % de ingresos o flujo del emisor ligado al ámbito; uso de los fondos en bonos verdes o sociales con marco verificado; en soberanos, peso del ámbito en la economía o en la recaudación. **PC2** 25 %.

| Componente (peso) | Métricas (dirección) | Ficha |
|---|---|---|
| QL (25) | Calificación numérica (+) y perspectiva (+); deuda/EBITDA (−); cobertura de intereses (+); liquidez sobre vencimientos a 24 meses (+); tendencia de métricas (+) | QLT-ACC-001 (emisor), ST-DESC-001 |
| VA (25) | Diferencial frente a la curva de su calificación y sector (residuo, +); z del diferencial a 5 años (+); rentabilidad esperada neta de pérdida esperada (+); carry y rolldown (+) | FIR-SPREAD-001, VAL-RF-001 |
| MO (5) | Deriva de calificación a 12 meses (+); evolución del diferencial a 3 meses (estrechamiento +) | ST-DESC-001 |
| RI (15) | Duración (−); subordinación (−); opciones de amortización desfavorables (−); covenants laxos (−); divisa distinta de EUR (−) | VAL-RF-001, RISK-DD-001 |
| LA (15) | Horquilla (−); saldo vivo (+); denominación mínima > 1 000 € (penalización); accesibilidad minorista (+) | SCR-LIQ-001 |
| CO | NA | — |

**Alertas medidas.** Ensanchamiento del CDS > 2 σ en un mes; muro de vencimientos sin refinanciación; subordinación estructural (holding).
**Referencias.** Ámbito: índice de bonos del segmento (o su ETF UCITS). Ranking: rentabilidad total equiponderada del universo ajustada por duración (RI-EQ por tramos).
**Guardas.** Diferenciales de referencias distintas (G, I, Z, OAS) no comparables; opcionalidad con OAS; máximo de dos emisiones por emisor en el top-N (9.7.2: marca para HT-03).
**Abstención.** Emisión sin precio observable en mercado regulado o SMN del marco.

## 12. SEL-DIV — Divisas (→ C.3)

**Subgrupo por defecto.** G10 frente a emergentes.
**Pureza (PE, 10).** ECO-EXPO-001: beta del par frente a EUR al factor del ámbito (materia prima, ciclo regional, diferencial de tipos) con HAC; peso del ámbito en exportaciones o en la balanza como dato. **PC2**: beta significativa al 90 % y del signo de la tesis.

| Componente (peso) | Métricas (dirección) | Ficha |
|---|---|---|
| QL (15) | Cuenta corriente/PIB (+); reservas en meses de importaciones (+); inflación frente al objetivo (−); estabilidad política (dato) | RISK-GEO-001 |
| VA (25) | Desviación frente a PPA (infravalorado +); desalineamiento BEER (+); tipo de cambio efectivo real frente a su media (+); carry ajustado por volatilidad (+) | FX-PPA-001, FX-BEER-001, FX-CARRY-001 |
| MO (15) | Momento a 3 y 12 meses (+); sorpresas macro relativas (+) | ACC-MOM-001, SER-FLOW-001 |
| RI (15) | Volatilidad (−); ES 97,5 % (−); sensibilidad a la aversión al riesgo (beta al VIX o a la renta variable global, −) | FX-VOL-001, RISK-VAR-001, ECO-CYC-001 |
| LA (10) | Liquidez del instrumento de acceso (+) | SCR-LIQ-001 |
| CO (10) | Coste del instrumento: roll, TER, horquilla (−) | SCR-LIQ-001 |

**Alertas medidas.** Posicionamiento especulativo en percentil > 90 (SER-FLOW-001); reservas < 3 meses de importaciones.
**Referencias.** Ámbito: cesta G10 equiponderada frente a EUR. Ranking: media equiponderada de los pares cribados.
**Guardas.** Sentido del par declarado (frente a EUR); carry en la rentabilidad total; colapsos del carry.
**Abstención.** Divisa con controles de capital materiales (PC1 de HT-11).

## 13. SEL-MP — Materias primas (→ C.4)

**Subgrupo por defecto.** Familia (energía, metales industriales, preciosos, agrícolas).
**Pureza (PE, 20).** ECO-EXPO-001: correlación del instrumento con la referencia física del ámbito; correspondencia de grado y lugar; en ETC sobre futuros, metodología de roll. **PC2** correlación ≥ 0,8.

| Componente (peso) | Métricas (dirección) | Ficha |
|---|---|---|
| QL (10) | Calidad del emisor del ETC y del colateral (dato); respaldo físico auditado (dato) | — (dato con DAT-B) |
| VA (20) | Roll yield anualizado (+); precio frente al percentil 90 de la curva de coste (cerca del suelo +); inventarios frente a la media estacional (bajos +) | CMD-CURVE-001, SUP-COST-001, SUP-INV-001 |
| MO (15) | Momento temporal 12-1 (+); momento de carry (+) | ACC-MOM-001 |
| RI (10) | Volatilidad (−); frecuencia de saltos (−); riesgo de emisor (−) | FX-VOL-001 |
| LA (15) | Interés abierto o volumen (+); creadores de mercado (+) | SCR-LIQ-001 |
| CO (10) | TER (−); coste de roll (−) | SCR-LIQ-001, CMD-CURVE-001 |

**Alertas medidas.** *Contango* profundo persistente (percentil > 90 de la pendiente); concentración extrema del interés abierto.
**Referencias.** Ámbito: Bloomberg Commodity Index o subíndice. Ranking: media equiponderada de los instrumentos cribados.
**Guardas.** Regla de enlace de la serie continua; spot ≠ rentabilidad invertible; estacionalidad de la curva.
**Abstención.** Contrato con liquidación física no apta para el marco.

## 14. SEL-IDX — Índices bursátiles (→ C.5)

**Subgrupo por defecto.** Ninguno (universo pequeño); por proveedor si n ≥ 10.
**Pureza (PE, 25).** SCR-PUR-001: % del índice en el ámbito `Σ w_i·p_i`, cobertura del universo del ámbito, exposición no deseada. **PC2** 60 %.

| Componente (peso) | Métricas (dirección) | Ficha |
|---|---|---|
| QL (15) | Peso de los 10 mayores (−); N_eq de la composición (+); rotación en rebalanceos (−); transparencia de reglas (dato) | IO-CONC-001 |
| VA (20) | PER adelantado y CAPE frente a su historia y a índices alternativos (−); prima de riesgo implícita (+); rentabilidad esperada por componentes (+) | VAL-MULT-001, IDX-ERP-001, ACC-ERP-001 |
| MO (15) | Momento 12-1 (+) | ACC-MOM-001 |
| RI (10) | Volatilidad (−); caída máxima (−); divisa no EUR (−) | RISK-DD-001 |
| LA (10) | Número, tamaño y liquidez de los vehículos que lo replican (+) | SCR-LIQ-001 |
| CO (5) | TER mínimo de réplica (−); coste de los futuros (−) | SCR-LIQ-001 |

**Alertas medidas.** Concentración > 40 % en 10 valores; rotación anual > 30 %.
**Referencias.** Ámbito: MSCI ACWI o índice regional amplio. Ranking: media de los índices alternativos cribados.
**Guardas.** Variante del índice (precio, neta, bruta) y divisa declaradas; composición en la fecha.
**Abstención.** Índice sin metodología pública.

## 15. SEL-FON — Fondos y vehículos de inversión colectiva (→ C.6)

**Subgrupo por defecto.** Gestión pasiva frente a activa; tipo de subyacente (`tipo_subyacente`).
**Pureza (PE, 25).** SCR-PUR-001: `Σ w_i·1[i supera PC2 de su tipo]` sobre la cartera publicada con fecha (medida principal) y `Σ w_i·p_i` (segunda); exposición no deseada; *active share* para activos. **PC2** 50 % del patrimonio.

| Componente (peso) | Métricas (dirección) | Ficha |
|---|---|---|
| QL (20) | Pasivos: diferencia de seguimiento (−) y error de seguimiento (−). Activos: alfa frente a factores (+), consistencia (+), estabilidad del gestor (dato) | ST-DESC-001, FAC-PREM-001 |
| VA (10) | Valoración agregada de la cartera frente al índice del ámbito (−); en cerrados, z del descuento sobre NAV (descuento mayor que su media +) | VAL-MULT-001, FON-DISC-001 |
| MO (5) | Flujos netos a 3 y 6 meses coherentes con la tesis (+) | SER-FLOW-001 |
| RI (10) | Concentración de cartera (−); réplica sintética y contraparte (−); apalancamiento (−); préstamo de valores (−) | IO-CONC-001 |
| LA (15) | Volumen y horquilla en bolsa (+); creadores de mercado (+); disponibilidad en el marco (+) | SCR-LIQ-001 |
| CO (15) | TER (−); diferencia de seguimiento (−); comisión de éxito (−) | SCR-LIQ-001 |

**Alertas medidas.** Diferencia de seguimiento > 2 × TER; salidas netas > 20 % en 6 meses.
**Referencias.** Ámbito: índice del ámbito. Ranking: media equiponderada neta de los vehículos cribados.
**Guardas.** Dos vehículos del mismo índice o con solapamiento > 80 %: marca de duplicado (9.7.1); NAV y carteras con fecha; clase en EUR o cubierta.
**Abstención.** Vehículo sin cartera publicada ni índice con composición pública (PE `SIN_RESULTADO`).

## 16. SEL-DER — Derivados financieros (→ C.7)

**Subgrupo por defecto.** Futuros frente a opciones frente a productos cotizados.
**Pureza (PE, 20).** Pureza del subyacente según su propio SEL-; delta y vega útiles para la tesis. **PC2** subyacente con PE ≥ 60 %.

| Componente (peso) | Métricas (dirección) | Ficha |
|---|---|---|
| QL | NA | — |
| VA (25) | Implícita frente a realizada y su percentil (según la estrategia, declarado); sesgo; estructura de plazos; base y carry del futuro frente a su valor razonable | DER-VRP-001, CMD-CURVE-001 |
| MO (5) | Momento del subyacente (+) | ACC-MOM-001 |
| RI (20) | Apalancamiento (−); pérdida máxima (−); riesgo de salto (−); riesgo de emisor en certificados (−) | RISK-VAR-001, RISK-DD-001 |
| LA (20) | Interés abierto (+); volumen (+); horquilla (−) | SCR-LIQ-001 |
| CO (10) | Coste de roll (−); horquilla (−); margen del emisor (−) | SCR-LIQ-001 |

**Alertas medidas.** Implícita en percentil > 95 para estrategias compradoras; interés abierto concentrado.
**Referencias.** Ámbito: subyacente sin derivado. Ranking: estrategia equiponderada sobre los instrumentos cribados.
**Guardas.** Probabilidades neutrales al riesgo ≠ reales; realizada futura solo en evaluación (fuga); sin H4 (8.6).
**Abstención.** Opciones binarias y CFD (fuera de marco; PC1).

## 17. SEL-INM — Inmobiliario cotizado (→ C.8)

**Subgrupo por defecto.** Subsector (logístico, residencial, oficinas, comercial, sanitario, centros de datos) × región.
**Pureza (PE, 15).** % del GAV en el subsector y la geografía del ámbito (informe EPRA); % de rentas como segunda medida. **PC2** 50 % del GAV.

| Componente (peso) | Métricas (dirección) | Ficha |
|---|---|---|
| QL (20) | Ocupación (+); duración media de contratos WAULT (+); coste medio de la deuda (−); calificación (+) | QLT-ACC-001, ST-DESC-001 |
| VA (25) | z del descuento sobre NAV frente a su media (descuento mayor +); cap rate implícito frente a transacciones (+); rentabilidad AFFO (+) | REI-NAV-001, REI-CAP-001 |
| MO (10) | Momento 12-1 (+) | ACC-MOM-001 |
| RI (15) | LTV (−); vencimientos de deuda a 24 meses (−); % a tipo fijo (+); concentración de inquilinos (−) | RISK-DD-001 |
| LA (10) | ADV (+) | SCR-LIQ-001 |
| CO (5) | Gastos generales y gestión externa sobre GAV (−) | SCR-LIQ-001 |

**Alertas medidas.** Dividendo > AFFO; revalorizaciones contrarias a transacciones; refinanciaciones a 24 meses sin cobertura.
**Referencias.** Ámbito: FTSE EPRA Nareit Developed o regional. Ranking: media equiponderada del universo.
**Guardas.** NAV retrasado; comparar con índices de tasación solo tras desuavizar (ALT-DESMOOTH-001).
**Abstención.** Sin NAV publicado al menos semestral.

## 18. SEL-CRI — Criptoactivos (→ C.9)

**Subgrupo por defecto.** Capa base, capa 2, DeFi, infraestructura, tokenización.
**Pureza (PE, 15).** % de comisiones o actividad del protocolo ligado al ámbito; en ETP, correspondencia con el token. **PC2** 50 %.

| Componente (peso) | Métricas (dirección) | Ficha |
|---|---|---|
| QL (20) | Comisiones anualizadas (+); direcciones activas (+); valor bloqueado (+); desarrolladores (+); historial de seguridad (dato); descentralización (dato) | CHR-ONCHAIN-001, ST-DESC-001 |
| VA (20) | Capitalización/comisiones (−); NVT (−); MVRV (−); FDV/capitalización (−) | CHR-ONCHAIN-001 |
| MO (15) | Momento a 3 y 12 meses (+) | ACC-MOM-001 |
| RI (15) | Volatilidad (−); desbloqueos y emisión a 12 meses (−); concentración de tenedores (−); riesgo de contrato y puentes (dato, −) | RISK-VAR-001, RISK-DD-001 |
| LA (10) | Volumen real sin lavado (+) | SCR-LIQ-001 |
| CO (5) | TER del ETP (−); custodia (−) | SCR-LIQ-001 |

**Alertas medidas.** Desbloqueo > 5 % de la oferta en 90 días; concentración > 50 % en 10 direcciones no identificadas; caída sostenida de actividad.
**Referencias.** Ámbito: bitcoin o índice amplio del segmento. Ranking: media equiponderada del universo.
**Guardas.** 365 días y UTC; volumen lavado; actividad ≠ valor; cambios de metodología del proveedor de datos en cadena.
**Abstención.** Token sin 12 meses de historia (PC1 de HT-11).

## 19. SEL-ALT — Capital privado y alternativos (→ C.10)

**Subgrupo por defecto.** Estrategia (capital privado, deuda privada, infraestructuras, regalías).
**Pureza (PE, 15).** % del NAV en el segmento del ámbito. **PC2** 50 %.

| Componente (peso) | Métricas (dirección) | Ficha |
|---|---|---|
| QL (20) | PME del gestor (+); DPI (+); dispersión entre vehículos (−); diversificación por *vintage* (+) | PRV-PME-001 |
| VA (20) | z del descuento sobre NAV frente a su historia (+); NAV desuavizado frente a cotizados comparables | FON-DISC-001, ALT-DESMOOTH-001 |
| MO (5) | Momento 12-1 (+) | ACC-MOM-001 |
| RI (15) | Apalancamiento del vehículo y de la cartera (−); concentración (−); desfase de valoración (−) | RISK-DD-001 |
| LA (10) | ADV o ventanas de reembolso (+) | SCR-LIQ-001 |
| CO (15) | Comisiones totales incluida la de éxito (−) | SCR-LIQ-001 |

**Alertas medidas.** Descuento creciente con salidas; compromisos no desembolsados elevados frente a la liquidez.
**Referencias.** Ámbito: LPX50 o índice cotizado del segmento. Ranking: media equiponderada del universo.
**Guardas.** Series suavizadas; TIR no realizable; sin H1–H2 (8.6).
**Abstención.** Vehículos no accesibles al minorista: vigilancia informativa, no candidatos.

## 20. SEL-MON — Monetarios y liquidez (→ C.11)

**Subgrupo por defecto.** Tipo de instrumento (letra, fondo VNAV/LVNAV/CNAV, ETF monetario, pagaré).
**Pureza (PE, 5).** Ajuste a la divisa y al plazo del ámbito (binaria). **PC2** divisa y plazo del ámbito.

| Componente (peso) | Métricas (dirección) | Ficha |
|---|---|---|
| QL (25) | Calidad crediticia (+); tipo de fondo (dato); vencimiento medio ponderado (−) | ST-DESC-001 |
| VA (30) | Rentabilidad neta equivalente frente a €STR o a la curva del plazo (+); valor de fijar frente a renovar (+) | MON-YLD-001 |
| MO | NA | — |
| RI (10) | Riesgo de reinversión (−); divisa (−); liquidez del fondo (+) | RISK-DD-001 |
| LA (15) | Liquidez diaria (+) | SCR-LIQ-001 |
| CO (15) | TER (−); horquilla (−) | SCR-LIQ-001 |

**Alertas medidas.** Rentabilidad del fondo por debajo de €STR − TER durante 3 meses; concentración en un emisor.
**Referencias.** Ámbito: €STR compuesto. Ranking: media de los instrumentos cribados.
**Guardas.** Convención de cotización declarada (descuento, simple, *money market yield*); salida en TAE; sin H4 (8.6).
**Abstención.** Instrumento sin divisa o plazo del ámbito.

## 21. SEL-TCV — Tipos de interés, crédito y volatilidad (→ C.12)

**Subgrupo por defecto.** Factor (nivel o pendiente, inflación implícita, crédito, volatilidad).
**Pureza (PE, 25).** ECO-EXPO-001: fracción de la sensibilidad en el factor (DV01 del tramo, sensibilidad al breakeven, beta al índice de crédito, vega). **PC2** 70 %.

| Componente (peso) | Métricas (dirección) | Ficha |
|---|---|---|
| QL | NA | — |
| VA (25) | Pendiente o inflación implícita frente a su valor razonable; carry y rolldown por DV01 (+); diferencial esperado frente a pérdidas (+); prima de volatilidad | TCV-CARRY-001, DER-VRP-001 |
| MO (5) | Momento del factor (+) | ACC-MOM-001 |
| RI (15) | Convexidad desfavorable (−); deterioro por roll (−); saltos (−) | RISK-VAR-001 |
| LA (15) | Liquidez del futuro o del ETF (+) | SCR-LIQ-001 |
| CO (15) | Roll (−); TER (−); diferencia de seguimiento (−) | SCR-LIQ-001 |

**Alertas medidas.** *Contango* de volatilidad extremo; cambio de cesta entregable del futuro.
**Referencias.** Ámbito: posición neutra (rentabilidad nula frente al índice de liquidez). Ranking: media de los instrumentos cribados.
**Guardas.** Breakeven ≠ inflación esperada; prima por plazo de un solo modelo; productos apalancados o inversos de volatilidad solo H1–H2 con advertencia.
**Abstención.** Producto con riesgo de liquidación anticipada por evento de volatilidad (alerta crítica del playbook).

---

## 22. Composición y ámbitos híbridos

| Situación | Composición | Riesgo cruzado que se declara |
|---|---|---|
| Mercado geográfico con sector ancla (petróleo en el Golfo, semiconductores en Taiwán) | PERF-B-GEO + PERF-B-CADENA (o PERF-B-SECT) | Concentración del índice en el sector ancla; divisa ligada a la materia prima |
| Temática con cuello de botella | PERF-B-TEMA + PERF-B-CADENA | Captura del valor en el eslabón frente a la temática |
| Segmento de crédito de un sector | PERF-B-SEGM + PERF-B-SECT | Ciclo sectorial frente a ciclo de crédito |
| Factor sobre una clase distinta de la RV (carry de divisas, momento de materias primas) | PERF-B-FACT + PERF-B-SEGM | Colapsos del factor en episodios de aversión al riesgo |
| Vehículo colectivo de cualquier subyacente | SEL-FON + SEL- del `tipo_subyacente` (métricas de valoración de la cartera) | Doble cómputo de exposición con candidatos directos (exposición compartida) |
| Producto cotizado de subyacente único (ETC, ETN, ETP cripto) | SEL- del subyacente (MP, CRI, DIV, TCV) con riesgo de emisor y costes en RI y CO | Riesgo de emisor y de colateral |
| Mismo emisor en RV y RF | SEL-RV y SEL-RF | Una sola apuesta independiente (9.7.5) |
| Emergente con vía `MATRIZ_COTIZADA` o `ETF_O_FONDO` (V2.1) | EMG-PEM-001 (pureza de la vía) + SEL-RV o SEL-FON | Exposición residual al emergente; la matriz se puntúa por su negocio total |
| Candidato con exposición a varios eslabones (V2.1) | SCR-PUR-001 por eslabón | `eslabon_id` = mayor peso; los demás en `eslabones_secundarios` (A.2) |

## 23. Matriz resumen perfil × horizonte (fichas dominantes)

| Perfil | H1 | H2 | H3 | H4 | H5 (V2.1) |
|---|---|---|---|---|---|
| PERF-B-SECT | (limitado en RV) FX-VOL-001, RISK-VAR-001 | ACC-MOM-001, ECO-CYC-001, SER-FLOW-001 | VAL-MULT-001, ECO-CYC-001, SIM-SCN-001 | VAL-REV-001, VAL-ROIC-001, IO-*, VAL-PROJ-001, VC-DESG-001, VC-BOT-001 | DIF-H5-001, VAL-REV-001, VC-BOT-001 (persistencia), FC-HITO-001 |
| PERF-B-TEMA | — | SER-FLOW-001, FAC-CROWD-001 | VAL-MULT-001, SIM-SCN-001 | MKT-*, DIF-*, SUP-LRN-*, VAL-PROJ-001, VAL-REV-001, EMG-PEM-001 | DIF-H5-001, SUP-LRN-002, MKT-TRI-001, VAL-REV-001, EMG-PEM-001, FC-HITO-001 |
| PERF-B-GEO | FX-VOL-001 (divisa) | ECO-CYC-001, FX-REGIME-001 | VAL-MULT-001, RISK-RGC-001, RISK-GEO-001 | IDX-ERP-001, ACC-ERP-001, FX-PPA-001 | DIF-H5-001 (demografía), IDX-ERP-001, FC-HITO-001 |
| PERF-B-SEGM | CMD-CURVE-001, DER-VRP-001, TCV-CARRY-001 | FIR-SPREAD-001, SUP-INV-001, MON-YLD-001 | VAL-RF-001, REI-NAV-001, FON-DISC-001 | SUP-COST-001, CHR-ONCHAIN-001, PRV-PME-001 | Limitado: SUP-COST-001 (superciclos), PRV-PME-001 |
| PERF-B-FACT | — | FAC-CROWD-001, SER-FLOW-001 | FAC-SPREAD-001, RISK-CRASH-001 | FAC-PREM-001, BT-SEL-001, BT-DSR-001, BT-PBO-001 | Limitado: FAC-PREM-001 (persistencia de la prima), BT-DSR-001 |
| PERF-B-CADENA | — | SUP-INV-001 | SUP-UTIL-001, SUP-BOTT-001, NET-SHOCK-001, VC-BOT-001 | SUP-COST-001, NET-IO-001, SIM-BOTT-001, SUP-LRN-001, VC-DESG-001, VC-BOT-001 | DIF-H5-001 (sustitución y nueva capacidad), SIM-BOTT-001, VC-BOT-001, FC-HITO-001 |

Las dos tablas de aplicabilidad de 8.6 del Documento 0 (por tipo de activo y por tipo de objeto) prevalecen sobre esta matriz (FON e INM sin H1; DER y MON sin H4 ni H5; ALT sin H1–H2; RF, DIV, CRI, TCV y MP «Limitado» en H5; TEMATICA y CADENA_DE_VALOR sin H1; «Limitado» con condiciones). En H5 ninguna ficha entrega probabilidades numéricas publicables (R13).

## 24. Pruebas de los perfiles

Batería en `09_Pruebas`, con al menos: un ámbito de cada tipo de objeto en N1, N2 y N3 (comprobando que el plan ejecuta exactamente los cálculos por defecto de su nivel); un ámbito compuesto (GEO con sector ancla); un universo heterogéneo que exige neutralización; un candidato sin segmentos con pureza estimada por dos vías; un candidato en banda marginal con segunda pasada y menor valor; un universo con dos vehículos del mismo índice (duplicado); un tipo de activo con componente NA (redistribución); una petición de precio objetivo rechazada; un backtest de un factor sin universo *point-in-time* rechazado (`UNIVERSO_SESGADO`); un horizonte «No» rechazado; V2.1: un SECTOR N2 con D4 en P3 que ejecuta VC-DESG-001 y VC-BOT-001 con la profundidad del Anexo A, una parada en PV1 que no ejecuta cálculos de las capas 2–4, una TEMATICA H5 con DIF-H5-001 y ≥ 3 hitos, y un emergente con vía `MATRIZ_COTIZADA` de exposición residual marcada. Ningún perfil se declara validado sin evidencia registrada (R26).
