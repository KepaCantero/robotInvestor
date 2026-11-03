# Perfiles — Perfiles de tipo de activo del Motor de Cálculo Avanzado (AG-13)

**Bloque A · Robot Investor · Versión óptima V5.0 · 02/11/2026** · Subordinado al Documento 0 óptima V5.0.

Archivo CC (propietario: operador, tipo 3; el Motor propone). Lectores: AG-13 y sus módulos, AG-15, Analistas de tipo de activo (AG-03 a AG-09 y AG-21 a AG-25), Prospectiva, Evaluador, Orquestador técnico. «Tipo de activo» y «clase de activo» son sinónimos (2.6 del Documento 0).

---

## 1. Propósito y reglas de uso

1.1. Un perfil PERF-xx es la **especialización del Motor para un tipo de activo**: qué variables importan, qué indicadores de seguimiento representan los ámbitos del tipo, qué métodos del Catálogo aplican en cada horizonte, qué datos mínimos exige, qué guardas protegen contra errores típicos del tipo, qué referencia ingenua y qué referencia de comparación usar y cuándo abstenerse. Sirve a la estrategia de cada Analista de tipo de activo (sección 8 del Documento 0) sin sustituirla: el Analista decide qué preguntar; el perfil decide cómo se calcula bien.

1.2. **Reglas**:
1. El Orquestador de Cálculo clasifica cada petición CT-09 por su tipo de activo principal y aplica el perfil o perfiles correspondientes; si la petición trae el perfil, lo verifica; si no, lo infiere y lo declara.
2. Una ficha solo se aplica a los perfiles que declara (R21). Aplicar un método de otro tipo exige justificación declarada en el plan.
3. Ámbitos híbridos: se combinan perfiles de forma declarada (sección 16) con sus riesgos cruzados; el tipo principal es el que fija la regla 1 de asignación de 2.6 (motor de rentabilidad).
4. El perfil no añade operaciones al Catálogo ni amplía horizontes: respeta la tabla 8.3 del Documento 0 («Limitado» = solo con datos de frecuencia y liquidez suficientes y catalizador identificado; «No» = el Motor rechaza el cálculo de previsión para ese horizonte).
5. Concluir «datos insuficientes» o «método no aplicable» es un resultado legítimo y registrable.
6. **Madurez** (R22): todos los perfiles están **documentados**. Las fichas que citan figuran con su madurez en el Catálogo de cálculos (V5.0); mientras una ficha esté solo documentada, el Motor sirve la alternativa del núcleo transversal con la limitación declarada o rechaza con motivo.
7. **Frontera con el Bloque B** (2.5 del Documento 0): ningún perfil se orienta a comparar, ordenar ni seleccionar instrumentos concretos (valores, emisiones, fondos, contratos, tokens) ni sus costes, comisiones o plataformas. La unidad de cálculo es el **ámbito** (mercado, índice, sector, subsector, segmento, categoría, curva, factor, estrategia) y su **indicador de seguimiento**. Los datos de instrumentos individuales solo entran como componentes de un agregado o como representación genérica de un tramo (p. ej., la opción ATM a 3 meses de un índice, el bono genérico a 10 años). Una petición cuyo propósito sea elegir o comparar instrumentos concretos se rechaza con `FUERA_DE_CATALOGO` (ninguna ficha cubre la selección de instrumentos), indicando la ficha de ámbito más próxima.
8. **Invertibilidad del ámbito** (PS3): el Motor puede calcular métricas agregadas que la sostienen (número de componentes negociables, volumen agregado, concentración, existencia de un indicador de seguimiento con serie suficiente); la conclusión sobre PS3 es del Analista.

1.3. **Correspondencia con la taxonomía del Documento 0 (2.6)**:

| N.º | Tipo | Analista | Perfil principal | Perfiles combinables habituales |
|---|---|---|---|---|
| 1 | RV Renta variable | AG-03 | PERF-ACC | PERF-TEM, PERF-ESG, PERF-MAC |
| 2 | RF Renta fija | AG-04 | PERF-FIR | PERF-TCV (contexto de curva y crédito), PERF-FX, PERF-ESG |
| 3 | DIV Divisas | AG-05 | PERF-FX | PERF-MON (tipos a corto), PERF-MAC |
| 4 | MP Materias primas | AG-06 | PERF-CMD | PERF-ESG, PERF-MAC |
| 5 | IDX Índices bursátiles | AG-21 | PERF-IDX | PERF-ACC (agregados sectoriales), PERF-FX, PERF-MAC |
| 6 | FON Fondos y vehículos de inversión colectiva | AG-22 | PERF-ETF | Perfil del subyacente de la categoría (PERF-ACC, PERF-FIR, PERF-CMD…), PERF-DER (apalancados) |
| 7 | DER Derivados financieros | AG-23 | PERF-DER | Perfil del subyacente (PERF-IDX, PERF-ACC, PERF-FX, PERF-CMD, PERF-FIR) |
| 8 | INM Activos inmobiliarios cotizados | AG-07 | PERF-REI | PERF-ACC, PERF-FIR |
| 9 | CRI Criptoactivos y activos digitales | AG-08 | PERF-CHR | PERF-DER (perpetuos y opciones) |
| 10 | ALT Capital privado y activos alternativos | AG-09 | PERF-PRV, PERF-ALT | PERF-FIR (deuda privada), PERF-REI (referencia cotizada), PERF-ETF (vehículos cotizados del activo privado) |
| 11 | MON Instrumentos monetarios y liquidez | AG-24 | PERF-MON | PERF-FX (comparación cubierta entre divisas), PERF-TCV |
| 12 | TCV Tipos de interés, crédito y volatilidad | AG-25 | PERF-TCV | PERF-FIR, PERF-DER, PERF-MON |
| — | Capas transversales | Todos | PERF-TEM, PERF-ESG, PERF-MAC | — |

1.4. **Formato de cada perfil**: estado y prioridad · ámbito · variables relevantes · régimen del tipo (indicadores que el Motor calcula) · indicadores de seguimiento típicos · métodos por horizonte (tabla 8.3) · referencia ingenua y referencia de comparación (8.4) · datos mínimos · convenciones · guardas del dominio · insuficiencia y abstención.

## 2. PERF-ACC — Renta variable (RV)

**Estado:** documentado · **Prioridad:** P1 · **Ámbito:** sectores, subsectores, industrias, temáticas, estilos y factores, tamaños, y países o regiones cuando la tesis es de fundamentales sectoriales o de estilo. La asignación entre mercados completos representados por índices de referencia corresponde a PERF-IDX (regla 2 de 2.6). Empresas individuales solo como componentes del agregado o como ejemplos ilustrativos del ámbito.

**Variables relevantes.** Beneficio por acción agregado (realizado y esperado) y sus revisiones; márgenes; ventas; flujo de caja libre; dividendos y recompras; deuda neta; ROIC, ROE; múltiplos agregados (PER adelantado, EV/EBITDA, EV/ventas, P/VC, FCF yield) frente a su historia y frente al mercado; prima de riesgo implícita; rendimiento real del bono a 10 años; momentum relativo; amplitud del segmento; flujos; volatilidad implícita; posicionamiento.

**Régimen del tipo.** REG-HMM-001 sobre rendimiento a 3 meses, volatilidad realizada a 1 mes y diferencial HY; percentil de la prima de riesgo implícita (ACC-ERP-001); pendiente de la curva (TCV-SLOPE-001) como indicador de ciclo; amplitud (IDX-CONC-001); momentum (ACC-MOM-001, TSMOM).

**Indicadores de seguimiento típicos.** Índices sectoriales e industriales (GICS o ICB) de proveedores reconocidos en rentabilidad total neta; índices de estilo, factor y tamaño; cestas temáticas publicadas con metodología pública; ratio del índice del ámbito frente a MSCI ACWI para pronósticos relativos.

**Métodos por horizonte** (8.3: H1 limitado; H2–H4 sí):

| Horizonte | Fichas | Uso |
|---|---|---|
| H1 (limitado) | VOL-GARCH-001, DER-OPT-001, RISK-VAR-001, SCN-H-001 | Bandas de movimiento esperado del agregado alrededor de eventos (resultados del sector, bancos centrales); sin señal direccional salvo certificado |
| H2 | ACC-MOM-001, FX-TREND-001, REG-HMM-001, ML-PRED-001 | Momentum relativo, revisiones de beneficios, régimen |
| H3 | ACC-FACT-001, ACC-VAL-001 (contexto), ACC-MOM-001, SCN-H-001 | Rotación sectorial y factorial; valoración relativa frente al mercado |
| H4 | ACC-VAL-001, ACC-ERP-001, TEM-DIFF-001 (con PERF-TEM), SCN-H-001 (bloques de rentabilidad) | Valoración absoluta del agregado, crecimiento descontado, prima implícita |

**Referencia ingenua y de comparación.** RI-CM con MSCI ACWI (8.4) en rentabilidad total neta y en la divisa del pronóstico; RI-TB para dirección (la renta variable sube en torno al 53–56 % de las semanas y ≈ 60–65 % de los meses según mercado y periodo).

**Datos mínimos.** Rentabilidad total diaria del indicador ≥ 3 años (momentum ≥ 13 meses; factores ≥ 36 meses); agregados contables ≥ 3 ejercicios con fecha de publicación; múltiplos del agregado ≥ 10 años (20 recomendados) para percentiles.

**Convenciones.** Índices de rentabilidad total (neta de retenciones por defecto); divisa declarada con conversión; beneficios adelantados con fecha del consenso; agregación de múltiplos por media armónica; ejercicios fiscales alineados.

**Guardas del dominio.**
- La valoración no es señal de tiempo en H1–H2.
- PER bajo en máximos de ciclo y PER alto en mínimos son trampas: usar beneficios normalizados.
- La concentración del agregado (pocas empresas con gran peso) cambia la lectura de su valoración: informar del peso de los 10 mayores (IDX-CONC-001).
- Narrativa saturada: el tope de 40 en «valoración del ámbito» de A (9.1) se aplica cuando el solicitante lo marca.
- Supervivencia y composición histórica en cualquier backtest.
- Ningún cálculo ordena empresas individuales para elegir entre ellas (regla 7).

**Insuficiencia y abstención.** Agregados sin estados auditados; mercados con controles de capital no modelados; ámbitos sin indicador de seguimiento con serie de rentabilidad total; temáticas sin exposición cuantificable por ingresos (PS4).

## 3. PERF-FIR — Renta fija (RF)

**Estado:** documentado · **Prioridad:** P1 · **Ámbito:** segmentos de bonos para cobrar su rentabilidad y su revalorización: soberanos por país y tramo, supranacionales, corporativos IG y HY por rating, sector y vencimiento, emergentes (moneda fuerte y local), subordinados, convertibles, titulizados, verdes y sostenibles, ligados a la inflación, flotantes. Vencimientos de hasta 12 meses usados como liquidez: PERF-MON; exposiciones a factores (pendiente, breakevens, índices CDS) sin tenencia de bonos: PERF-TCV (reglas 1 y 4 de 2.6).

**Variables relevantes.** Rendimientos por tramo; curva cupón cero y *forward*; nivel, pendiente y curvatura (NSS); expectativas de tipos implícitas; breakevens; prima por plazo; diferenciales (G, I, Z, OAS) por rating y sector; tasas de impago y recuperación; duración, convexidad, DV01; carry y rolldown; emisiones netas; volatilidad de tipos.

**Régimen del tipo.** REG-HMM-001 sobre nivel, pendiente 2s10s e inflación implícita; fase del ciclo monetario a partir de MON-EXP-001; percentil del diferencial HY e IG (FIR-SPREAD-001); prima por plazo (TCV-TP-001) como contexto.

**Indicadores de seguimiento típicos.** Índices de bonos del segmento (Bloomberg, ICE BofA, iBoxx, JP Morgan EMBI y GBI-EM) en rentabilidad total, cubiertos o no a la divisa declarada; rendimiento del bono genérico del tramo; OAS del índice del segmento.

**Métodos por horizonte** (8.3: H1 limitado; H2–H4 sí):

| Horizonte | Fichas | Uso |
|---|---|---|
| H1 (limitado) | FIR-PRICE-001, VOL-GARCH-001, SCN-H-001 | Sensibilidad del segmento a eventos (bancos centrales, inflación): DV01 × movimiento esperado |
| H2 | FIR-CARRY-001, FIR-SPREAD-001, REG-HMM-001 | Carry ajustado por volatilidad, momentum de diferenciales |
| H3 | FIR-CURVE-001, FIR-CARRY-001, FIR-SPREAD-001, TCV-TP-001 (contexto), SCN-H-001 | Tramo de la curva, valor relativo entre segmentos, ciclo de crédito |
| H4 | FIR-PRICE-001 (rendimiento como ancla), FIR-CRED-001, FIR-SPREAD-001 | El rendimiento actual del segmento es el mejor estimador de su rentabilidad a horizonte ≈ duración |

**Referencia ingenua y de comparación.** RI-PA para rendimientos y diferenciales; curva *forward* como alternativa; RI-CM con Bloomberg Global Aggregate cubierto a EUR (8.4) o, en pronósticos absolutos, el índice del segmento.

**Datos mínimos.** Curva con ≥ 6 nodos; diferenciales del segmento ≥ 10 años (15 recomendados, incluida una recesión); convención y fecha de liquidación; para ligados, índice de inflación de referencia y retardo de indexación.

**Convenciones.** Rendimientos en % con base anual; cambios en pb; precios por 100 nominal, limpio y sucio diferenciados; convención de días del mercado; cobertura de divisa declarada.

**Guardas del dominio.**
- Duración modificada prohibida en segmentos con opciones (efectiva obligatoria).
- Breakeven ≠ inflación esperada pura (primas de riesgo y liquidez).
- El carry no es previsión: la curva *forward* ya descuenta la reversión bajo expectativas puras.
- No mezclar riesgo de tipos, de diferencial y de divisa en una sola cifra sin descomposición.
- Agregados con emisiones ilíquidas valoradas a modelo: declarar.
- Nunca se ordenan emisiones o emisores concretos para elegir entre ellos (regla 7).

**Insuficiencia y abstención.** Sin curva fiable de referencia; titulizaciones sin datos de colateral agregados; deuda local con controles de capital no modelados.

## 4. PERF-FX — Divisas (DIV)

**Estado:** documentado (lote FX heredado parcialmente implementado; véase el Catálogo) · **Prioridad:** P1 · **Ámbito:** pares principales, cruzados y exóticos; bloques de divisas (G10, emergentes, exportadores de materias primas); estrategias de carry, valor y momentum sobre cestas.

**Variables relevantes.** Spot, *forwards* y puntos *swap*; diferenciales de tipos nominales y reales; inflación relativa; tipo de cambio real efectivo; términos de intercambio; cuenta corriente y posición de inversión internacional; reservas; volatilidad implícita y *risk reversals*; posicionamiento (CFTC); sorpresas macro relativas.

**Régimen del tipo.** FX-REGIME-001 o REG-HMM-001 sobre volatilidad implícita G10 y apetito de riesgo (diferencial HY, VIX); rentabilidad acumulada de la cesta de carry (entorno favorable o colapso).

**Indicadores de seguimiento típicos.** Tipo de cambio spot del par; índice de rentabilidad total del par o de la cesta (spot + carry); tipo de cambio efectivo nominal o real; índices de estrategia (carry, momentum, valor) con metodología pública.

**Métodos por horizonte** (8.3: H1–H3 sí; H4 limitado):

| Horizonte | Fichas | Uso |
|---|---|---|
| H1 | FX-VOL-001, VOL-GARCH-001, FX-CARRY-001, FX-MOM-001, DER-SKEW-001, MON-EXP-001 | Bandas por volatilidad, carry diario, eventos de bancos centrales |
| H2 | FX-MOM-001, FX-CARRY-001, FX-TREND-001 | Momentum cambiario y carry/volatilidad |
| H3 | FX-CARRY-001, FX-MOM-001, FX-COINT-001, SCN-H-001 | Carry con régimen; divergencias de política monetaria |
| H4 (limitado) | FX-PPA-001, FX-BEER-001 | Paridades y equilibrio: vida media de 3–5 años |

**Referencia ingenua y de comparación.** RI-PA (paseo aleatorio sin deriva), notoriamente difícil de batir (Meese y Rogoff, 1983); RI-CM con la cesta equiponderada G10 frente a EUR (8.4).

**Datos mínimos.** Spot y diferenciales diarios ≥ 2 años (H1–H3); PPA y BEER ≥ 15–20 años con índices de precios y vintages.

**Convenciones.** Dirección del par explícita (unidades de cotizada por unidad de base); *fixing* declarado; anualización 252; carry con base de tipos declarada (3 meses).

**Guardas del dominio.**
- La paridad descubierta no se usa como previsión.
- El carry tiene colas izquierdas: entregar siempre con volatilidad y escenario de colapso.
- Tipos fijos, bandas o controles de capital: los métodos de libre flotación no aplican.
- Intervenciones y cambios de régimen cambiario rompen las series.

**Insuficiencia y abstención.** Pares con mercado *offshore* y *onshore* divergentes sin especificar; regímenes cambiados en la ventana; datos de reservas o intervención no disponibles cuando son decisivos.

## 5. PERF-CMD — Materias primas (MP)

**Estado:** documentado · **Prioridad:** P1 · **Ámbito:** metales preciosos, industriales y para baterías; energía (petróleo, gas, refinados, carbón, electricidad); uranio; cereales; tropicales; ganadería; madera; derechos de emisión y créditos ambientales; subsectores y diferenciales entre materias primas.

**Variables relevantes.** Spot y curva de futuros; roll yield; *convenience yield*; inventarios y días de cobertura; producción, capacidad y utilización; costes marginales; márgenes de transformación (*crack* y *crush spreads*); estacionalidad; meteorología; posicionamiento (CFTC); dólar; demanda china; políticas (OPEP+, aranceles, cuotas); precio del carbono.

**Régimen del tipo.** Estado de la curva por subsector (CMD-CURVE-001); inventarios frente a estacional (CMD-INV-001); REG-HMM-001 sobre rendimiento, volatilidad y pendiente; TSMOM (ACC-MOM-001).

**Indicadores de seguimiento típicos.** Subíndices de futuros de rentabilidad total por materia prima o subsector (Bloomberg Commodity, S&P GSCI); precio de referencia del mercado físico (con advertencia de que no es invertible); diferencial entre contratos para tesis de curva.

**Métodos por horizonte** (8.3: H1 sí en energía y metales líquidos; H2–H4 sí):

| Horizonte | Fichas | Uso |
|---|---|---|
| H1 | CMD-CURVE-001, VOL-GARCH-001, DER-OPT-001, SCN-H-001 | Inventarios semanales, reuniones OPEP+, meteorología |
| H2 | CMD-INV-001, CMD-CURVE-001, ACC-MOM-001 (TSMOM), FX-STL-001 | Sorpresas de inventarios, estacionalidad |
| H3 | CMD-CURVE-001, CMD-INV-001, CMD-RETDEC-001, SCN-H-001 | Balance oferta-demanda, roll esperado |
| H4 | CMD-REAL-001, CMD-RETDEC-001 | Superciclos, coste marginal, precio real |

**Referencia ingenua y de comparación.** RI-PA del precio; RI-EST para inventarios y curvas estacionales; RI-CM con Bloomberg Commodity Index (8.4) en rentabilidad total.

**Datos mínimos.** Curva con ≥ 3 vencimientos líquidos; inventarios ≥ 5 años; precio real ≥ 30 años para H4 (15 con limitación).

**Convenciones.** Unidad física del contrato y conversión; divisa de cotización (normalmente USD); calendario de vencimientos y roll; spot de referencia frente a contrato próximo.

**Guardas del dominio.**
- El inversor en futuros no obtiene la variación del spot: usar CMD-RETDEC-001.
- Comparar pendientes de curvas estacionales por el mismo mes del año.
- Estacionalidad estimada con pocas campañas es frágil.
- La comparación entre vehículos o contratos concretos para acceder a la materia prima es del Bloque B.

**Insuficiencia y abstención.** Sin curva líquida; mercados opacos (litio, tierras raras, metales menores) solo con limitaciones; inventarios no publicados.

## 6. PERF-IDX — Índices bursátiles (IDX)

**Estado:** documentado (nuevo en V5.0) · **Prioridad:** P1 · **Ámbito:** mercados completos representados por índices de referencia (globales, regionales, de país, emergentes; también índices sectoriales, de dividendos, de volatilidad, de renta fija o de materias primas cuando la tesis es la asignación entre índices); valoración relativa entre índices; estructura del índice (concentración, ponderación, composición sectorial); eventos de índice (rebalanceos, inclusiones, cambios metodológicos). Sectores y temáticas por sus fundamentales: PERF-ACC (regla 2 de 2.6).

**Variables relevantes.** Nivel y rentabilidad total; rentabilidad por dividendo y recompras netas; crecimiento del BPA agregado y sus revisiones; múltiplos agregados (PER adelantado, CAPE, P/VC) y su historia; prima de riesgo implícita por región; concentración (peso de los 10 mayores, HHI, número efectivo de componentes); composición sectorial; amplitud; flujos hacia productos indexados; divisa; sorpresas macro por región; calendario de rebalanceos y activos que replican el índice.

**Régimen del tipo.** REG-HMM-001 sobre rendimiento, volatilidad y diferencial HY del agregado global; percentil de la prima implícita por región (ACC-ERP-001, IDX-ERP-001); momentum relativo entre regiones (IDX-REL-001); concentración (IDX-CONC-001).

**Indicadores de seguimiento típicos.** El propio índice de referencia en rentabilidad total neta y en la divisa declarada (cubierta o no); ratio entre dos índices para tesis relativas; versión equiponderada frente a ponderada por capitalización para tesis de concentración; cesta de inclusiones o exclusiones para tesis de evento.

**Métodos por horizonte** (8.3: H1 limitado a eventos de índice; H2–H4 sí):

| Horizonte | Fichas | Uso |
|---|---|---|
| H1 (limitado) | IDX-REB-001, VOL-GARCH-001, DER-TERM-001 | Presión de demanda de un rebalanceo o cambio de composición fechado; bandas de movimiento |
| H2 | IDX-REL-001 (momentum relativo), ACC-MOM-001, IDX-CONC-001 (amplitud), IDX-REB-001, REG-HMM-001 | Rotación entre regiones, amplitud, eventos |
| H3 | IDX-REL-001, IDX-CONC-001, ACC-FACT-001, SCN-H-001 | Valoración relativa con ajuste sectorial, ciclo macro relativo |
| H4 | IDX-ERP-001, ACC-ERP-001, IDX-REL-001, SCN-H-001 (bloques de rentabilidad) | Rentabilidad esperada a largo plazo por índice y prima por región |

**Referencia ingenua y de comparación.** RI-CM con MSCI ACWI (8.4) en rentabilidad total neta; RI-MH para brechas de valoración; RI-TB para dirección.

**Datos mínimos.** Rentabilidad total diaria ≥ 3 años; múltiplos y rentabilidad por dividendo mensuales ≥ 15 años (10 con limitación); CAPE con ≥ 10 años de beneficios reales; composición fechada (sin supervivencia) para concentración; ≥ 20 eventos comparables para estudios de rebalanceo.

**Convenciones.** Variante del índice declarada (precio, rentabilidad total neta o bruta); divisa común y cobertura declaradas; composición en su fecha; múltiplos agregados por media armónica.

**Guardas del dominio.**
- Las brechas de valoración entre regiones pueden persistir por composición sectorial, crecimiento, gobernanza y tipos: comparar también con ajuste neutral sectorial.
- Grinold-Kroner es una identidad aproximada, no una previsión: muy sensible a la reversión del múltiplo.
- En la comparación entre índices la divisa puede dominar el resultado: entregar cubierto y no cubierto.
- El efecto de inclusión se ha reducido con el tiempo y se anticipa: el estudio de eventos describe el agregado, nunca selecciona valores afectados.
- Los productos que replican un índice no se comparan entre sí (Bloque B).

**Insuficiencia y abstención.** Índices sin serie de rentabilidad total; cambios metodológicos que rompen la comparabilidad sin enlace; mercados con controles de capital no modelados; activos indexados no estimables cuando son decisivos.

## 7. PERF-ETF — Fondos y vehículos de inversión colectiva (FON)

**Estado:** documentado (reorientado en V5.0) · **Prioridad:** P1 · **Ámbito:** **oportunidades propias del vehículo** como categoría o segmento: descuentos y primas de fondos cerrados y vehículos cotizados con NAV; categorías con flujos persistentes; estrategias de gestión en régimen favorable (macro global, arbitraje, renta fija flexible, tendencia); estructuras nuevas (ELTIF, ETF activos, ETF de bonos con vencimiento); dinámica estructural de apalancados e inversos; diferencias de seguimiento sistemáticas de una categoría. Si el motor de rentabilidad es el subyacente (un sector, un segmento de bonos), el ámbito pertenece a su tipo aunque se acceda con un vehículo (regla 1 de 2.6). Este perfil **ya no** es una capa de implementación: la elección del vehículo concreto, sus costes y su plataforma son del Bloque B.

**Variables relevantes.** Precio y NAV de los miembros de la categoría; descuento/prima agregado y su dispersión; flujos netos y AUM por categoría; diferencia y error de seguimiento agregados; gastos corrientes medios de la categoría (como componente explicativo de la diferencia de seguimiento, no como comparación de productos); apalancamiento y rebalanceo diario; volatilidad del subyacente; liquidez agregada de la categoría; catalizadores estructurales (recompras, ofertas, votaciones de continuidad, cambios regulatorios).

**Régimen del tipo.** Descuento agregado de fondos cerrados frente a su historia (FON-DISC-001); flujos por categoría (FON-FLOW-001); régimen de volatilidad del subyacente (VOL-GARCH-001, REG-HMM-001) para apalancados y estrategias.

**Indicadores de seguimiento típicos.** Índice de descuento agregado de la categoría; índice de la categoría del vehículo (8.4); índices de estrategias de gestión con metodología pública (familias HFRX o equivalentes); series de flujos por categoría de proveedores reconocidos.

**Métodos por horizonte** (8.3: H1 no; H2 limitado; H3–H4 sí):

| Horizonte | Fichas | Uso |
|---|---|---|
| H1 (no) | — | El Motor rechaza el cálculo de previsión |
| H2 (limitado) | FON-FLOW-001, FON-LEV-001, FON-DISC-001 (con catalizador) | Persistencia de flujos, arrastre de apalancados en el régimen actual, catalizadores de descuento |
| H3 | FON-DISC-001, FON-FLOW-001, FON-TD-001, FON-LEV-001, ALT-HF-001 (estrategias), SCN-H-001 | Normalización de descuentos, estrategias en régimen favorable |
| H4 | FON-DISC-001, FON-TD-001, ALT-HF-001, ALT-DESMOOTH-001, RISK-DD-001 | Descuentos estructurales, rentabilidad neta de la estrategia, riesgo desuavizado |

**Referencia ingenua y de comparación.** Índice de la categoría del vehículo (8.4); RI-MH del descuento; flujo nulo para flujos; L × rentabilidad del índice para apalancados.

**Datos mínimos.** Precio y NAV fechados ≥ 3 años (≥ 5 recomendados) y ≥ 5 vehículos por categoría para agregar; flujos mensuales ≥ 3 años con taxonomía fija; rentabilidades diarias del subyacente ≥ 1 año para apalancados; estrategias ≥ 36 meses.

**Convenciones.** Variante del índice correcta (precio, rentabilidad total neta o bruta); NAV con fecha y frecuencia; agregación por mediana salvo declaración; taxonomía de categorías del proveedor declarada.

**Guardas del dominio.**
- Comparar con la variante correcta del índice; un error de variante genera diferencias de seguimiento espurias.
- Apalancados: rentabilidad a h días ≠ L × rentabilidad del índice (arrastre por volatilidad).
- NAV retrasados (privados, inmobiliario) sesgan el descuento.
- Solapamiento entre vehículos no es diversificación.
- Nunca se ordenan vehículos concretos por coste, seguimiento o comisión: la salida es siempre la categoría (regla 7).

**Insuficiencia y abstención.** Categorías con menos de 5 vehículos; NAV sin fecha o con antigüedad > 6 meses (> 12 en privados) sin ajuste; taxonomía cambiante; estrategias sin índice con metodología pública.

## 8. PERF-DER — Derivados financieros (DER)

**Estado:** documentado (reorientado en V5.0) · **Prioridad:** P1 · **Ámbito:** **oportunidades propias del instrumento derivado** sobre subyacentes representativos (índices, divisas, bonos, materias primas, sectores): prima de varianza (implícita frente a realizada), sesgo, estructura de plazos de la volatilidad, carry y roll de futuros financieros, primas de estrategias de opciones en régimen favorable (venta cubierta, protecciones baratas), eventos descontados. Se trabaja con contratos genéricos del subyacente (ATM, deltas estándar, vencimiento constante), nunca con la comparación de contratos, emisores de productos o plataformas concretas. Volatilidad, tipos y crédito como factores: PERF-TCV.

**Variables relevantes.** Volatilidad implícita por vencimiento y precio de ejercicio; volatilidad realizada y prevista; prima de varianza; sesgo 25Δ y mariposa; estructura de plazos y volatilidad *forward*; base y carry de futuros; dividendos y repo implícitos; interés abierto y volumen agregados por subyacente; posicionamiento de gamma agregado cuando se aporta; calendario de eventos.

**Régimen del tipo.** Percentil de la prima de varianza (DER-VRP-001); estado de la estructura de plazos (DER-TERM-001); percentil del sesgo (DER-SKEW-001); régimen de volatilidad del subyacente (VOL-GARCH-001, REG-HMM-001).

**Indicadores de seguimiento típicos.** Índices de estrategias de opciones con metodología pública (p. ej., índices Cboe de venta cubierta y de venta de puts); índices de volatilidad implícita del subyacente; índices de rentabilidad de futuros con roll; diferencial implícita–realizada como serie propia del ámbito.

**Métodos por horizonte** (8.3: H1–H2 sí; H3 sí hasta 12 meses; H4 no):

| Horizonte | Fichas | Uso |
|---|---|---|
| H1 | DER-VRP-001, DER-TERM-001 (eventos descontados), DER-SKEW-001, DER-OPT-001, VOL-GARCH-001, RISK-VAR-001 | Prima de varianza, movimiento descontado de eventos, bandas |
| H2 | DER-VRP-001, DER-SKEW-001, DER-ROLL-001, FX-VOL-001 | Normalización de primas y sesgos, carry de futuros |
| H3 (≤ 12 meses) | DER-VRP-001, DER-TERM-001, DER-ROLL-001, SIM-MC-001, SCN-H-001 | Primas de estrategias en régimen, estructura de plazos |
| H4 (no) | — | El Motor rechaza el cálculo de previsión |

**Referencia ingenua y de comparación.** Rentabilidad del subyacente sin derivado (8.4); RI-EWMA para volatilidad; RI-MH para primas y sesgos.

**Datos mínimos.** Volatilidad implícita diaria ≥ 3 años (≥ 5 recomendados para percentiles); superficie con ≥ 5 precios de ejercicio por vencimiento y ≥ 3 vencimientos; spot y ≥ 2 vencimientos de futuros con tipos y dividendos esperados.

**Convenciones.** Convención de delta declarada (spot o *forward*, con o sin prima); varianza total para interpolar entre vencimientos; anualización 252 (365 en CRI); vencimiento constante interpolado declarado.

**Guardas del dominio.**
- Probabilidades neutrales al riesgo no son probabilidades reales.
- La prima de varianza es positiva en promedio con pérdidas extremas: entregar siempre ES de la estrategia de venta.
- La varianza realizada posterior solo se usa para la historia, nunca para la señal actual (fuga).
- Modelos fuera de supuestos (barreras, ejercicio anticipado complejo, exóticos) rechazados; márgenes y liquidaciones declarados.
- Apalancamiento y pérdidas superiores al desembolso se declaran como riesgo del ámbito, sin evaluar productos concretos.

**Insuficiencia y abstención.** Superficies con arbitraje no corregible; subyacentes sin mercado de opciones líquido; datos de implícita de una sola fuente sin metodología; horizonte H4.

## 9. PERF-REI — Activos inmobiliarios cotizados (INM)

**Estado:** documentado · **Prioridad:** P1 · **Ámbito:** inmobiliario **cotizado** únicamente: REIT, SOCIMI, inmobiliarias y promotoras cotizadas, gestoras de inmuebles, financiación hipotecaria cotizada, por subsector (residencial, oficinas, comercial, logística, residencias, hoteles, centros de datos) y región. El inmobiliario y las infraestructuras privados son PERF-PRV/PERF-ALT (regla 3 de 2.6); las sociedades cotizadas de infraestructuras se asignan por su motor de rentabilidad (regla 1), por defecto RV.

**Variables relevantes.** NOI, rentas y su crecimiento; ocupación y vacancia; oferta en construcción; cap rates (tasación e implícito); NAV (EPRA NTA) y prima/descuento agregados; FFO, AFFO; rentabilidad por dividendo y cobertura; LTV, ICR, vencimientos y coste de deuda agregados; WAULT; índices de precios de vivienda y comercial como contexto.

**Régimen del tipo.** Diferencial cap rate–bono (REI-CAP-001) y su percentil; descuento sobre NAV agregado (REI-NAV-001); dirección de los tipos reales (FIR-CURVE-001, TCV-BEI-001); condiciones de crédito.

**Indicadores de seguimiento típicos.** FTSE EPRA Nareit por región y subsector en rentabilidad total; índices de REIT por subsector; descuento agregado sobre NAV del subsector.

**Métodos por horizonte** (8.3: H1 no; H2 limitado; H3–H4 sí):

| Horizonte | Fichas | Uso |
|---|---|---|
| H1 (no) | — | El Motor rechaza el cálculo de previsión; bandas descriptivas con VOL-GARCH-001 solo como contexto |
| H2 (limitado) | ACC-MOM-001, FIR-CARRY-001 (sensibilidad a tipos) | Solo subsectores líquidos con catalizador |
| H3 | REI-NAV-001, REI-CAP-001, REI-FFO-001, ACC-FACT-001, SCN-H-001 | Descuentos frente a NAV, sensibilidad a tipos, subsectores |
| H4 | REI-CAP-001, REI-LEV-001, ALT-DESMOOTH-001 (índices de tasación de referencia), SCN-H-001 | Ciclo inmobiliario, refinanciación, obsolescencia |

**Referencia ingenua y de comparación.** RI-MH para descuentos y diferenciales; RI-CM con FTSE EPRA Nareit Developed (8.4).

**Datos mínimos.** Rentabilidad total del indicador ≥ 5 años; NAV y cap rates agregados ≥ 10 años (15 para percentiles robustos); índices de tasación trimestrales ≥ 40 observaciones para desuavizar cuando se usan como referencia.

**Convenciones.** NAV variante EPRA declarada; NOI antes o después de CAPEX declarado; divisa y superficie (m²); frecuencia de tasación.

**Guardas del dominio.**
- Series de tasación siempre desuavizadas antes de comparar con el cotizado.
- NAV publicado no es precio objetivo y va retrasado.
- Oficinas: obsolescencia (eficiencia energética, teletrabajo) que las tasaciones reflejan tarde.
- Regulación de alquileres y fiscalidad específica (SOCIMI/REIT) condiciona flujos.
- Los agregados del subsector no se descomponen para elegir sociedades concretas (regla 7).

**Insuficiencia y abstención.** Subsectores con menos de 5 sociedades cotizadas; NAV agregado de antigüedad > 12 meses; riesgo regulatorio no evaluable.

## 10. PERF-CHR — Criptoactivos y activos digitales (CRI)

**Estado:** documentado, con cautela metodológica declarada · **Prioridad:** P1 (precio, volatilidad, financiación, flujos) / P2 (métricas en cadena, tokenómica) · **Ámbito:** redes (Bitcoin, plataformas de contratos inteligentes), sectores del ecosistema (DeFi, capa 2, tokenización, RWA, stablecoins) y narrativas; productos cotizados sobre criptoactivos solo como fuente de flujos agregados.

**Variables relevantes.** Precio y volatilidad (mercado 24/7); capitalización circulante y totalmente diluida; capitalización realizada, MVRV, NVT; direcciones activas y comisiones (con cautela); flujos a plataformas de intercambio; flujos agregados de productos cotizados; oferta de stablecoins; financiación de perpetuos, base e interés abierto; dominancia de Bitcoin; tokenómica agregada del sector (emisión, quema, desbloqueos, *staking*); liquidez global; eventos de protocolo y regulación.

**Régimen del tipo.** REG-HMM-001 sobre rendimiento, volatilidad y financiación; MVRV en percentil (CHR-ONCHAIN-001); flujos (CHR-FLOW-001); dominancia.

**Indicadores de seguimiento típicos.** Precio de la red (para ámbitos de red); índices sectoriales de criptoactivos con metodología pública; índice de criptoactivos de gran capitalización; ratio frente a bitcoin para tesis relativas.

**Métodos por horizonte** (8.3: H1–H3 sí; H4 limitado):

| Horizonte | Fichas | Uso |
|---|---|---|
| H1 | VOL-GARCH-001, CHR-FUND-001, CHR-FLOW-001, RISK-VAR-001, SCN-H-001 | Apalancamiento, flujos, bandas de volatilidad |
| H2 | CHR-FLOW-001, CHR-FUND-001, ACC-MOM-001 (TSMOM), REG-HMM-001, CHR-TOKEN-001 (desbloqueos) | Momentum, flujos, presión de oferta |
| H3 | CHR-ONCHAIN-001, REG-HMM-001, SCN-H-001 | Posición en el ciclo con advertencia de pocos ciclos |
| H4 (limitado) | CHR-ONCHAIN-001, CHR-TOKEN-001 | Alta incertidumbre estructural: solo escenarios amplios |

**Referencia ingenua y de comparación.** RI-PA; RI-CM con bitcoin (8.4).

**Datos mínimos (sin exigir 5 años).** Precio y volatilidad: ≥ 1 año diario (≥ 2 recomendados) para H1–H2; métricas en cadena: historia completa disponible, ≥ 2 años, con la limitación «pocos ciclos»; financiación: ≥ 90 días (1 año para percentiles); sectores o redes con < 1 año de historia: solo descriptivos y escenarios, sin modelos de régimen ni EVT.

**Convenciones.** Hora UTC y cierre diario a las 00:00 UTC por defecto; anualización 365; unidad del activo y cadena; fuente en cadena con metodología y fecha de consulta; capitalización circulante frente a FDV explícita.

**Guardas del dominio.**
- No aplicar DCF a activos sin flujos; no usar stock-to-flow salvo para advertir de su fracaso.
- Métricas de actividad no son valor capturado; volumen en cadena contaminado por movimientos internos.
- Desanclaje de stablecoins y riesgo de contraparte (plataformas, puentes, custodios): escenario específico.
- Volumen y precios de plataformas poco reguladas pueden estar manipulados: fuentes agregadas fiables.
- Colas extremas (ξ alto): VaR paramétrico normal prohibido.
- Dentro de un sector del ecosistema, los tokens individuales entran como componentes del agregado; no se ordenan para elegir (regla 7).

**Insuficiencia y abstención.** Sin fuente en cadena verificable; protocolo en cambio activo; liquidez agregada insuficiente; concentración extrema de tenedores sin dato fiable.

## 11. PERF-PRV — Capital privado, deuda privada e infraestructuras privadas (ALT)

**Estado:** documentado · **Prioridad:** P2 · **Ámbito:** el **mercado del activo privado** por segmento y cosecha: capital riesgo y privado (*buyout*, *growth*, *venture*), secundarios, deuda privada y financiación privada, préstamos participativos, infraestructuras y renovables privadas, inmobiliario privado. Se distingue siempre el activo privado de su vehículo cotizado (los descuentos de los vehículos cotizados son PERF-ETF).

**Variables relevantes.** Flujos agregados de aportaciones y distribuciones por cosecha; NAV; TIR, TVPI, DPI, RVPI; PME; curva J; *dry powder*; múltiplos de compra (EV/EBITDA de operaciones); apalancamiento de operaciones; descuentos en secundario; diferenciales y tasas de impago de deuda privada; para infraestructuras y renovables privadas, flujos regulados o concesionales, indexación a inflación, precios de la electricidad capturados y tasas de descuento de transacciones; comisiones como componente de la rentabilidad neta del segmento.

**Régimen del tipo.** Ciclo de captación y de salidas; descuentos de secundario; diferencial de la deuda privada frente a préstamos sindicados y HY; valoraciones cotizadas comparables; tasas de descuento de transacciones de infraestructuras frente al bono real.

**Indicadores de seguimiento típicos.** Índices de capital privado cotizado (LPX50 y familias LPX); índices de rentabilidad de mercados privados por cosecha y estrategia (publicados con retraso); índices de deuda privada con metodología pública; índices de infraestructuras privadas y de inmobiliario privado (MSCI o equivalentes), desuavizados.

**Métodos por horizonte** (8.3: H1 no; H2 no; H3 limitado; H4 sí):

| Horizonte | Fichas | Uso |
|---|---|---|
| H1–H2 (no) | — | El Motor rechaza el cálculo de previsión |
| H3 (limitado) | FIR-SPREAD-001 (aproximación cotizada), FON-DISC-001 (vehículos cotizados del segmento, con PERF-ETF) | Solo con catalizador (descuentos de secundario, ciclo de crédito) |
| H4 | PRV-PME-001, PRV-CF-001, ALT-DESMOOTH-001, REI-CAP-001 (análogo para infraestructuras e inmobiliario privados), RISK-DD-001 | Rentabilidad frente a mercado cotizado, iliquidez, riesgo desuavizado |

**Referencia ingenua y de comparación.** LPX50 (8.4); PME = 1 frente al índice cotizado comparable (pequeña capitalización para *buyout*; infraestructuras cotizadas para infraestructuras privadas).

**Datos mínimos.** Flujos fechados agregados por cosecha y estrategia; series trimestrales ≥ 24 observaciones para desuavizar (40 recomendadas); NAV con antigüedad ≤ 12 meses.

**Convenciones.** Divisa del segmento; fechas de flujo; rentabilidades netas o brutas de comisiones declaradas.

**Guardas del dominio.**
- TIR no comparable con rentabilidades anuales de índices; líneas de suscripción inflan la TIR.
- Volatilidad y correlaciones de NAV suavizados subestiman el riesgo: desuavizar siempre.
- Sesgos de supervivencia y autoselección en bases de datos privadas.
- La invertibilidad del ámbito (PS3) se sostiene con métricas agregadas del universo accesible a un minorista europeo (número de vehículos regulados del segmento, volumen); la elección del vehículo es del Bloque B.
- Nunca se ordenan gestoras o fondos concretos (regla 7).

**Insuficiencia y abstención.** Sin flujos agregados de la cosecha o segmento; NAV de antigüedad > 12 meses; estructura jurídica del universo desconocida. «No hay datos suficientes» es un resultado frecuente y legítimo.

## 12. PERF-ALT — Activos alternativos no tradicionales y estrategias (ALT)

**Estado:** documentado · **Prioridad:** P2 · **Ámbito:** bosques y explotaciones agrícolas; arte, vino, relojes y coleccionables; regalías y propiedad intelectual (música, farmacéuticas); litigios financiados; bonos catastróficos y riesgo de seguros; créditos de carbono no cotizados (con PERF-CMD); estrategias hedge como mercado de estrategias (sus vehículos cotizados o UCITS como categoría: PERF-ETF).

**Variables relevantes.** Índices de transacciones (ventas repetidas, hedónicos); tasas de piezas no vendidas en subastas; flujos subyacentes y su duración (regalías); producción y precios de la madera y de la tierra agrícola; estructura del evento (bonos catastróficos); exposiciones factoriales y dispersión de las estrategias; costes de transacción del mercado; autenticidad, custodia y fraude como riesgos del ámbito.

**Régimen del tipo.** Volumen y tasa de no vendidos en subastas; precio de la tierra y de la madera frente a sus rentas; régimen de volatilidad y tendencia de los mercados subyacentes para estrategias (REG-HMM-001 de los tipos afectados); diferencial de los bonos catastróficos frente a pérdida esperada de modelo.

**Indicadores de seguimiento típicos.** Índices de subastas por categoría con metodología pública; índices de tierras agrícolas y de explotaciones forestales (NCREIF u homólogos); índices de bonos catastróficos; índices de estrategias hedge con metodología pública.

**Métodos por horizonte** (8.3: H1 no; H2 no; H3 limitado; H4 sí):

| Horizonte | Fichas | Uso |
|---|---|---|
| H1–H2 (no) | — | El Motor rechaza el cálculo de previsión |
| H3 (limitado) | ALT-HF-001, ACC-FACT-001 | Estrategias con índice líquido y catalizador de régimen |
| H4 | ALT-HF-001, ALT-AUC-001, ALT-DESMOOTH-001, RISK-DD-001, SCN-H-001 | Rentabilidad neta de costes del mercado, riesgo desuavizado, diversificación |

**Referencia ingenua y de comparación.** LPX50 (8.4) como referencia común del tipo; IPC (rentabilidad real nula) y renta variable global para coleccionables y activos reales; cartera pasiva de factores o 60/40 para estrategias.

**Datos mínimos.** Estrategias: ≥ 36 meses; coleccionables: ≥ 500 transacciones (≥ 200 pares de ventas repetidas); activos reales: series de valoración trimestrales ≥ 40 observaciones.

**Convenciones.** Rentabilidades netas de costes de transacción del mercado; divisa de las transacciones; frecuencia de valoración declarada.

**Guardas del dominio.**
- Sesgos de supervivencia y relleno retrospectivo en índices de estrategias.
- Sesgo de selección en subastas; la mediana del índice no es la rentabilidad de una pieza.
- Riesgo de fraude y autenticidad no cuantificable por el Motor: limitación declarada.
- Bonos catastróficos: la pérdida esperada procede de modelos de catástrofe, no de series históricas cortas.

**Insuficiencia y abstención.** Sin precios observables o mercado bilateral sin historial; régimen regulatorio indeterminado. La abstención es el resultado esperado en muchas subfamilias.

## 13. PERF-MON — Instrumentos monetarios y liquidez (MON)

**Estado:** documentado (nuevo en V5.0) · **Prioridad:** P1 · **Ámbito:** **dónde, en qué divisa y a qué plazo rinde mejor la liquidez** con riesgo reducido, y cuándo conviene fijar rentabilidades: segmentos de letras, depósitos negociables y certificados de depósito, papel comercial y pagarés a corto, repos, categorías de fondos monetarios, deuda pública de vencimiento ≤ 12 meses, por divisa y plazo (regla 4 de 2.6). Nunca la comparación de depósitos, fondos o emisores concretos.

**Variables relevantes.** Tipos oficiales y de mercado a corto (€STR, SOFR, SONIA, Euribor); rendimientos de letras por plazo y país; tipos de depósitos y pagarés agregados por plazo; rentabilidad media de las categorías de fondos monetarios; curva OIS y futuros a corto; calendario de reuniones de bancos centrales; inflación realizada y esperada a corto; diferenciales entre segmentos; puntos *forward* para comparación cubierta entre divisas; riesgo emisor agregado del papel comercial.

**Régimen del tipo.** Fase del ciclo monetario (subidas, pausa, bajadas) a partir de MON-EXP-001; tipo real a corto (MON-REAL-001) frente a su historia; pendiente de la curva monetaria (3 a 12 meses).

**Indicadores de seguimiento típicos.** €STR compuesto (referencia de 8.4) y homólogos por divisa; índices de letras de 0–3 y 3–12 meses en rentabilidad total; rentabilidad media de la categoría de fondos monetarios; tipo a 12 meses del segmento.

**Métodos por horizonte** (8.3: H1 limitado a decisiones de bancos centrales; H2–H3 sí; H4 no):

| Horizonte | Fichas | Uso |
|---|---|---|
| H1 (limitado) | MON-EXP-001 | Probabilidades implícitas de la próxima decisión; sorpresa |
| H2 | MON-YLD-001, MON-EXP-001, MON-FIX-001, MON-REAL-001 | Segmento y divisa que mejor remuneran; valor de fijar plazo |
| H3 | MON-FIX-001, MON-YLD-001, MON-REAL-001, MON-EXP-001, SCN-H-001 | Senda de tipos y reinversión |
| H4 (no) | — | El Motor rechaza el cálculo de previsión |

**Referencia ingenua y de comparación.** €STR compuesto (8.4) y sus homólogos; RI-PA (tipo oficial sin cambios) para sendas; renovar al tipo actual para MON-FIX-001.

**Datos mínimos.** Tipos por segmento y plazo diarios o semanales ≥ 5 años; curva OIS o futuros con ≥ 3 nodos en 12 meses; calendario de reuniones; IPC con vintages y expectativas de inflación con fuente ≥ 10 años para tipos reales.

**Convenciones.** Convención de cotización declarada (descuento, rendimiento simple, *money market yield*); base Act/360 o Act/365 según mercado; salida homogeneizada en TAE salvo petición; divisa y cobertura declaradas.

**Guardas del dominio.**
- No comparar tipos con convenciones distintas sin homogeneizar.
- Los diferenciales entre segmentos remuneran riesgo emisor, liquidez y distinta protección: no son «gratuitos».
- Las expectativas implícitas incluyen una pequeña prima por plazo y son neutrales al riesgo.
- La comparación cubierta entre divisas incluye la base de divisas; sin cobertura, el resultado lo domina el tipo de cambio.
- Nunca se ordenan entidades, depósitos o fondos concretos (regla 7).

**Insuficiencia y abstención.** Mercados con tipos administrados o controles de capital no modelados; convenciones no declaradas; segmentos sin serie agregada.

## 14. PERF-TCV — Tipos de interés, crédito y volatilidad como factores (TCV)

**Estado:** documentado (nuevo en V5.0) · **Prioridad:** P1 · **Ámbito:** **exposiciones a factores**: nivel y pendiente de curvas (2s10s, 5s30s, 3m10y), prima por plazo, inflación implícita (breakevens, 5y5y), diferenciales de crédito agregados (índices CDS IG y HY por región, base CDS-bono), nivel y estructura de la volatilidad (VIX, VSTOXX, MOVE y sus futuros), correlaciones. Comprar bonos de un segmento para cobrar su rentabilidad es RF; la prima de una opción concreta del subyacente es DER (regla 1 de 2.6).

**Variables relevantes.** Curvas nominal, real y OIS; pendientes y curvaturas; prima por plazo estimada; breakevens y swaps de inflación; encuestas de inflación; diferenciales de índices CDS por serie, pendiente y base; tasas de impago y recuperación; índices de volatilidad y curva de futuros; volatilidad de tipos; carry y rolldown de exposiciones neutrales en duración; régimen macro y monetario.

**Régimen del tipo.** Régimen de la curva (empinamiento o aplanamiento, alcista o bajista) por TCV-SLOPE-001; percentil de la prima por plazo (TCV-TP-001); percentil del diferencial CDS (TCV-CDS-001); estado de la estructura de plazos de la volatilidad (TCV-VIXTS-001); REG-HMM-001 sobre nivel, pendiente, diferencial y volatilidad.

**Indicadores de seguimiento típicos.** Pendiente 2s10s o 5s30s en pb; breakeven 5y5y; índices iTraxx y CDX (serie *on-the-run* con enlace); VIX, VSTOXX, MOVE; índices de futuros de volatilidad a vencimiento constante; prima por plazo publicada (ACM) como serie de seguimiento.

**Métodos por horizonte** (8.3: H1–H3 sí; H4 limitado):

| Horizonte | Fichas | Uso |
|---|---|---|
| H1 | TCV-VIXTS-001, DER-VRP-001, TCV-SLOPE-001 (sensibilidad a eventos), MON-EXP-001, VOL-GARCH-001 | Eventos de bancos centrales y datos; roll de volatilidad |
| H2 | TCV-SLOPE-001, TCV-CDS-001, TCV-VIXTS-001, TCV-BEI-001, FIR-CARRY-001 | Carry y rolldown de factores, normalización de diferenciales |
| H3 | TCV-TP-001, TCV-SLOPE-001, TCV-BEI-001, TCV-CDS-001, SCN-H-001 | Prima por plazo, valor razonable de la pendiente y de los breakevens, ciclo de crédito |
| H4 (limitado) | TCV-TP-001, TCV-BEI-001, TCV-CDS-001 | Solo con datos largos y escenarios amplios |

**Referencia ingenua y de comparación.** Posición neutra (rentabilidad cero frente al índice de liquidez, 8.4); RI-PA del factor (pendiente, breakeven, diferencial, volatilidad); valores *forward* que ya descuenta la curva.

**Datos mínimos.** Curvas con ≥ 6 nodos ≥ 10 años (prima por plazo: curva cupón cero mensual ≥ 20 años, 10 con limitación); curvas reales con ≥ 3 vencimientos; índices CDS ≥ 5 años con serie y versión; índices de volatilidad y ≥ 2 vencimientos de futuros ≥ 3 años.

**Convenciones.** Cambios en pb; exposiciones neutrales en DV01 declaradas; índice de inflación de referencia de cada mercado; CDS con cupón estándar y conversión precio–diferencial declarada; volatilidad en puntos anualizados.

**Guardas del dominio.**
- Breakeven ≠ inflación esperada (primas de inflación y de liquidez de los ligados).
- La prima por plazo depende del modelo: entregar con segunda vía.
- El spot de un índice de volatilidad no es invertible; los futuros convergen al spot y el contango cuesta a la exposición larga.
- Saltos de volatilidad y convexidad: ES obligatorio en exposiciones cortas.
- El Motor calcula sobre factores e índices, nunca compara contratos o productos concretos (regla 7).

**Insuficiencia y abstención.** Curvas reales con < 3 vencimientos; índices CDS sin enlace entre series; regímenes monetarios no comparables en la ventana (control de la curva) sin declaración.

## 15. Capas transversales

### 15.1 PERF-TEM — Temáticas, sectores y cadenas de valor

**Estado:** documentado · **Prioridad:** P1. Se aplica sobre RV (y a veces MP, INM, CRI, IDX, FON) cuando la tesis es temática.
**Variables.** Tamaño de mercado y adopción; curvas de difusión (Bass, logística); curvas de aprendizaje y costes; capacidad y cuellos de botella; márgenes por eslabón; exposición de ingresos del agregado a la temática (pureza).
**Indicadores de seguimiento típicos.** Cestas temáticas con metodología pública y exposición por ingresos.
**Métodos.** TEM-DIFF-001 (difusión y adopción, MC-04), ACC-FACT-001 (¿la temática es un factor ya conocido?), ACC-VAL-001 (¿cuánto descuenta el agregado del crecimiento?).
**Guardas.** Tendencia real no implica oportunidad (valoración y competencia); exposición narrativa sin cuantificar no supera PS4; adopción real frente a anuncios.

### 15.2 PERF-ESG — Sostenibilidad y clima

**Estado:** documentado, con limitaciones de datos · **Prioridad:** P2. Se aplica cuando la pregunta lo requiere.
**Variables.** Emisiones (alcances 1, 2 y 3) e intensidad agregadas; riesgos físicos y de transición; precio del carbono; exposición regulatoria; calidad y cobertura de datos ESG.
**Métodos.** MC-03 (sensibilidades), MC-04 (escenarios de transición), SCN-H-001 (escenarios climáticos de referencia).
**Guardas.** Métricas con fuente, metodología y cobertura; la falta de datos se declara y nunca se imputa; etiquetas no son exposición efectiva (riesgo de *greenwashing*).

### 15.3 PERF-MAC — Macroeconomía global y geopolítica

**Estado:** documentado · **Prioridad:** P1. Se sirve con el núcleo transversal (MC-03 macroeconomía cuantitativa, MC-02 regímenes, MC-05 escenarios). Variables: crecimiento, inflación, empleo, política monetaria y fiscal, condiciones financieras, sorpresas macro, riesgo geopolítico parametrizable. Uso principal: coherencia entre los doce tipos (9.6.6 del Documento 0), escenarios comunes a varias opciones y ML-CLUS-001 para contar apuestas independientes por factor macro común (p. ej., «tipos a la baja» en RF, INM, RV de crecimiento, MON y TCV).

## 16. Ámbitos híbridos y asignación

| Ámbito | Tipo principal (regla 1 de 2.6) | Perfiles combinados | Riesgos cruzados a explicitar |
|---|---|---|---|
| Sector de empresas al que se accede con vehículos indexados | RV | PERF-ACC (+ PERF-ETF solo si el vehículo añade el motor de rentabilidad) | Concentración del indicador frente al sector |
| Descuento de fondos cerrados de deuda privada | FON | PERF-ETF + PERF-PRV + PERF-FIR | NAV retrasado, crédito, apalancamiento |
| Segmento de bonos ligados a la inflación (tenencia) | RF | PERF-FIR + PERF-TCV (contexto de breakevens) | Prima de liquidez de los ligados |
| Breakeven 5y5y como factor | TCV | PERF-TCV + PERF-FIR | Liquidez de ligados, estacionalidad |
| Bonos convertibles como segmento | RF | PERF-FIR + PERF-DER + PERF-ACC | Crédito, opción sobre acciones, volatilidad |
| Prima de varianza de un índice bursátil | DER | PERF-DER + PERF-IDX | Saltos, colas izquierdas |
| Estructura de plazos del VIX como factor | TCV | PERF-TCV + PERF-DER | Convergencia de futuros, saltos |
| Subsector de REIT | INM | PERF-REI + PERF-ACC | Sensibilidad a la renta variable a corto frente a fundamentales inmobiliarios |
| Infraestructuras privadas frente a cotizadas | ALT | PERF-PRV + PERF-REI (análogo de cap rate) | Desuavizado, iliquidez |
| Productos cotizados sobre criptoactivos (flujos) | CRI | PERF-CHR + PERF-ETF | Custodia, horario de cotización frente a mercado 24/7 |
| Créditos de carbono | MP o ALT según mercado | PERF-CMD + PERF-ESG + PERF-ALT | Regulación, calidad del crédito, liquidez |
| Liquidez en otra divisa con cobertura | MON | PERF-MON + PERF-FX | Base de divisas, coste de cobertura agregado |

Regla: se declara el tipo principal (el del Analista que propone, conforme a 2.6) y los perfiles combinados; cada cálculo aplica las guardas de todos los perfiles afectados; las fichas de un perfil no se aplican por simetría a otro (p. ej., PER a un índice de bonos); una misma oportunidad no se calcula como si perteneciera a dos top-3 (regla 5 de 2.6).

## 17. Matriz resumen tipo × horizonte

| Tipo | H1 | H2 | H3 | H4 |
|---|---|---|---|---|
| RV | Limitado: VOL-GARCH, DER-OPT | ACC-MOM, REG-HMM | ACC-FACT, ACC-VAL (contexto) | ACC-VAL, ACC-ERP |
| RF | Limitado: FIR-PRICE (DV01 × evento) | FIR-CARRY, FIR-SPREAD | FIR-CURVE, FIR-CARRY, TCV-TP (contexto) | FIR-PRICE (rendimiento), FIR-CRED |
| DIV | FX-VOL, FX-CARRY, FX-MOM | FX-MOM, FX-CARRY | FX-CARRY, FX-COINT | Limitado: FX-PPA, FX-BEER |
| MP | CMD-CURVE, VOL-GARCH | CMD-INV, ACC-MOM (TSMOM) | CMD-CURVE, CMD-INV, CMD-RETDEC | CMD-REAL, CMD-RETDEC |
| IDX | Limitado: IDX-REB | IDX-REL, IDX-CONC, ACC-MOM | IDX-REL, IDX-CONC | IDX-ERP, ACC-ERP |
| FON | No | Limitado: FON-FLOW, FON-LEV | FON-DISC, FON-FLOW, FON-TD | FON-DISC, FON-TD, ALT-HF |
| DER | DER-VRP, DER-TERM, DER-SKEW | DER-VRP, DER-SKEW, DER-ROLL | DER-VRP, DER-TERM, DER-ROLL (≤ 12 meses) | No |
| INM | No | Limitado: ACC-MOM | REI-NAV, REI-CAP, REI-FFO | REI-CAP, REI-LEV, ALT-DESMOOTH |
| CRI | VOL-GARCH, CHR-FUND, CHR-FLOW | CHR-FLOW, CHR-FUND, CHR-TOKEN | CHR-ONCHAIN, REG-HMM | Limitado: CHR-ONCHAIN, CHR-TOKEN |
| ALT | No | No | Limitado: ALT-HF, FIR-SPREAD | PRV-PME, PRV-CF, ALT-DESMOOTH, ALT-AUC |
| MON | Limitado: MON-EXP | MON-YLD, MON-EXP, MON-FIX | MON-FIX, MON-YLD, MON-REAL | No |
| TCV | TCV-VIXTS, DER-VRP, MON-EXP | TCV-SLOPE, TCV-CDS, TCV-VIXTS, TCV-BEI | TCV-TP, TCV-SLOPE, TCV-BEI, TCV-CDS | Limitado: TCV-TP, TCV-BEI, TCV-CDS |

En todas las celdas: SCN-H-001 para escenarios sobre el indicador de seguimiento, RISK-VAR-001/RISK-DD-001 para riesgo, y evaluación con FC-EVAL-001/FC-CAL-001 (R13).

## 18. Pruebas de los perfiles

Ningún perfil pasa a «implementado» sin que sus fichas P1 estén implementadas, ni a «validado» sin las pruebas de `09_Pruebas` que lo afecten, en particular: una misma tendencia con implicaciones distintas por tipo; un ámbito híbrido con dos perfiles y su asignación por la regla 1 de 2.6; datos insuficientes (incluidos un criptoactivo con historia corta, una cosecha privada sin flujos y una categoría de fondos cerrados con menos de 5 vehículos); horizonte «No» rechazado (FON H1, DER H4, MON H4); ámbito no invertible por falta de universo negociable o de indicador de seguimiento (PS3); aplicación indebida del método de otro tipo detectada (R21); y una petición de comparar instrumentos concretos rechazada con `FUERA_DE_CATALOGO` (regla 7).
