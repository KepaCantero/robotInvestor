# Perfiles de clase de activo del Motor — especificación versionada por familia

VERSIÓN V1.0 · 01/11/2026 · Documento de especificación del agente «Motor de Cálculo Avanzado
para el Analizador de Tendencias de Inversión» (system prompt del Motor, óptima V3.0) · Coherente
con el Documento 0 --- Protocolo maestro del Bloque A (Versión óptima V3.0), con el Mapa de
conocimientos del Motor (V2.0) y con el Catálogo de cálculos del Motor (V3.0) · es-ES

## 1. Propósito, alcance y reglas de uso

Este documento define los **perfiles de clase de activo** (códigos PERF-xx, décima convención de
la sección 6.1 del Documento 0): especializaciones versionadas del Motor por familia de activo.
Un perfil declara, para su familia, las variables relevantes, los indicadores, las fuentes de
datos, las frecuencias, los métodos del catálogo aplicables, los benchmarks, los riesgos, las
convenciones, las pruebas de validación y los criterios de insuficiencia. El perfil no añade
operaciones al catálogo, no cambia los límites del Motor y no convierte la cobertura en
obligación: sirve a la secuencia de selección de la sección 4.6 del prompt del Motor (regla
crítica 20 del Documento 0).

Reglas de uso: (i) el Orquestador de Cálculo clasifica cada petición por su clase principal y
aplica el perfil o perfiles correspondientes, declarándolos en la respuesta y en el Registro de
cálculos (esquema V1.2); (ii) los perfiles compatibles se combinan de forma declarada en
**activos híbridos** (sección 14), explicitando los riesgos cruzados y sin forzar una
clasificación única; (iii) cada perfil declara su **estado de madurez** (documentado,
implementado, validado; regla crítica 19) y su **prioridad de implantación** (P0/P1/P2, regla
crítica 21): mientras un perfil esté solo documentado, el Motor lo declara así y sirve con el
núcleo transversal y la limitación declarada; (iv) ningún perfil se declara operativo sin sus
fichas de método publicadas en el Catálogo y sus pruebas registradas en el Plan de pruebas; y
(v) la ampliación de un perfil (nuevas variables, métodos o pruebas) sigue el cauce de tipos 3
del Motor (secciones 13.3 y 14.2 de su prompt).

Clases y códigos: PERF-ACC acciones; PERF-FIR renta fija y crédito; PERF-FX divisas; PERF-CMD
materias primas; PERF-ETF fondos y ETF; PERF-DER derivados; PERF-REI inmobiliario,
REIT/SOCIMI e infraestructuras; PERF-CHR criptoactivos; PERF-PRV capital privado; PERF-ALT
inversiones alternativas; PERF-TEM inversión temática y sectores (capa transversal sobre
perfiles); PERF-ESG sostenibilidad y clima (capa transversal sobre perfiles). La clase MIX
designa en los registros a los activos híbridos con combinación declarada.

## 2. Formato estándar del perfil

Cada perfil se documenta con los campos siguientes: identificador y versión; familia y
descripción; variables relevantes; indicadores y métricas típicas; fuentes de datos y
frecuencias; métodos del catálogo aplicables y fichas asociadas; benchmarks de referencia;
riesgos y errores de interpretación frecuentes; convenciones (unidades, calendarios, divisas,
ajustes); pruebas de validación; criterios de insuficiencia y abstención; dependencias de otros
perfiles; estado de madurez y prioridad; e historial de versiones del perfil.

## 3. PERF-ACC — Acciones, empresas y participaciones societarias

**Estado: documentado · Prioridad: P1.** Familia: acciones cotizadas y no cotizadas,
participaciones y derechos sobre beneficios empresariales.

- **Variables relevantes**: ingresos y su calidad; márgenes (bruto, EBITDA, EBIT, neto);
  crecimiento orgánico e inorgánico; flujo de caja operativo, libre y para accionistas;
  CAPEX y necesidades de reinversión; ROIC, ROE, ROA y rentabilidad incremental del capital;
  WACC y coste de deuda; deuda neta, apalancamiento y vencimientos; dilución, recompras y
  remuneración en acciones; dividendos y payout.
- **Indicadores y métricas**: múltiplos P/E, EV/EBITDA, EV/EBIT, EV/Sales, P/B y FCF yield;
  DCF y modelos de dividendos como referencia; comparables sectoriales con ajustes
  estructurales; calidad contable (diferencia beneficio-caja, ajustes no recurrentes).
- **Fuentes y frecuencias**: estados financieros trimestrales y anuales; precios y volúmenes
  diarios; estimaciones de consenso cuando existan y con su fecha de conocimiento (2.7.6).
- **Métodos del catálogo aplicables**: ST-DESC, ST-INF, FIN-CAGR (crecimiento), regresiones de
  MC-03 para sensibilidades, SIM-MC para escenarios de valoración, RISK-VAR para el riesgo de
  la serie de precios; fichas nuevas de valoración relativa por el cauce de tipos 3.
- **Benchmarks**: índices del mercado y del sector; mediana de comparables; rentabilidad
  requerida por el modelo de referencia declarado.
- **Riesgos frecuentes**: confundir crecimiento con creación de valor; múltiplos sin ajuste
  cíclico; calidad contable no examinada; beneficios concentrados en un segmento en declive;
  intangibles no reconocidos.
- **Convenciones**: moneda de reporte y moneda de comparación con la conversión declarada;
  calendarios fiscales distintos del natural; ajustes por splits y dividendos en las series de
  precios (STC-1).
- **Pruebas de validación**: recálculo de múltiplos sobre casos de referencia; coherencia
  interna de los estados financieros agregados; reproducibilidad del DCF declarado como
  supuestos, no como valor objetivo.
- **Criterios de insuficiencia**: historia financiera inferior a tres ejercicios; estados no
  auditados sin advertencia; moneda o ajustes indeterminados; empresas con beneficios
  actuales reducidos solo con métodos declarados de valoración de intangibles y escenarios.

## 4. PERF-FIR — Renta fija, crédito y financiación

**Estado: documentado · Prioridad: P1.** Familia: deuda soberana, corporativa, municipal,
supranacional y titulizada; deuda privada y préstamos.

- **Variables relevantes**: precios limpio y sucio, cupón corrido; YTM, YTC, YTW y
  rentabilidad realizada; duración de Macaulay, modificada y efectiva; convexidad; DV01/PV01 y
  key-rate durations; curvas cupón cero, forward y estructura temporal; diferenciales de
  crédito; probabilidad de impago, recuperación, pérdida esperada; rating y migración;
  covenants, garantías y subordinación.
- **Indicadores y métricas**: spreads sobre la curva de referencia; carry, rolldown y
  descomposición de rentabilidad (tipos, spread, divisa); métricas de liquidez de emisión.
- **Fuentes y frecuencias**: precios de cierre y valoraciones de mercado; curvas oficiales y
  de proveedor; calendars de cupones y convenciones de mercado (day count).
- **Métodos aplicables**: FIN-CAGR, ST-DESC, ST-INF; descomposición de rentabilidad por fichas
  nuevas; MC-05 para escenarios de curva; MC-07 para riesgo de cola y estrés de curvas.
- **Benchmarks**: índices de mercado por tramo de calidad y duración; curva soberana de
  referencia.
- **Riesgos frecuentes**: duración efectiva mal aplicada en bonos con opciones; curvas con
  extrapolaciones no declaradas; spread y riesgo de divisa mezclados; liquidez ignorada en
  valoraciones marcadas a modelo.
- **Convenciones**: day count y frecuencia de cupón declarados; moneda y base de descuento;
  tratamiento de bonos indexados a inflación (nominal frente a real).
- **Pruebas**: reproducción de precios con curvas de referencia; identidades de duración y
  convexidad; coherencia carry+rolldown+desplazamientos con la rentabilidad total.
- **Insuficiencia**: sin curva de referencia fiable; emisiones ilíquidas sin valoración
  alternativa declarada; documentación legal (covenants, subordinación) no disponible.

## 5. PERF-FX — Divisas y mercados de tipos de cambio

**Estado: documentado, con lote inicial de fichas FX implementado en servicio · Prioridad: P1
(primer perfil maduro; hereda la especialización divisas de las óptimas V2.1/V2.2).**

- **Variables relevantes**: tipos spot, forward y puntos swap; diferenciales de tipos e
  inflación; paridades (PPA absoluta y relativa, paridad de tipos cubierta y descubierta);
  flujos de capital, balanza por cuenta corriente y reservas; regímenes cambiarios e
  intervenciones; volatilidad realizada e implícita; posicionamiento y sentiment.
- **Indicadores**: desviación de PPA; carry medible; bases de financiación; brecha
  implícita-realizada; velocidad y persistencia de tendencias; regímenes de volatilidad.
- **Fuentes y frecuencias**: tipos diarios (spot y forwards); tipos de interés de referencia;
  datos de balanza de pagos y reservas (mensuales, con fecha de publicación); encuestas de
  posicionamiento cuando existan.
- **Métodos aplicables**: lote VIGENTE FX-TREND-001, FX-BRK-001, FX-STL-001, FX-VOL-001,
  FX-REGIME-001, FX-PPA-001, FX-CARRY-001, FX-COINT-001, FX-CORR-001; fichas transversales
  ST-DESC, ST-INF, SIM-MC, RISK-VAR.
- **Benchmarks**: referencia ingenua (paseo aleatorio con deriva cero) para toda predicción;
  índices efectivos de moneda.
- **Riesgos frecuentes**: presentar una paridad como valor justo sin horizonte; ignorar la
  base de financiación en el carry; confundir correlación con cobertura; regímenes con número
  de estados impuesto sin criterio.
- **Convenciones**: cotización base/cotizada y dirección de la lectura; convención de
  anualización (360/365 o 252 días hábiles para volatilidad, declarada); fechas de fixing.
- **Pruebas**: las de las fichas del lote VIGENTE más la batería mínima (P-01, P-03, P-14).
- **Insuficiencia**: par con histórico corto o con régimen cambiario cambiado en la ventana;
  controles de capital sin modelar; datos de intervención no disponibles.

## 6. PERF-CMD — Materias primas, recursos naturales y mercados físicos

**Estado: documentado · Prioridad: P1.** Familia: energía, metales preciosos e industriales,
metales estratégicos, agricultura, ganadería y otros mercados físicos.

- **Variables relevantes**: curvas forward (contango/backwardation); spot, futuros y precio
  físico regional; costes de almacenamiento, transporte, seguro y financiación; convenience
  yield; oferta, demanda, inventarios y capacidad; costes marginales y curvas de coste;
  estacionalidad y meteorología; geopolítica y restricciones comerciales.
- **Indicadores**: estructura temporal de la curva; roll yield y rendimiento de índices de
  futuros; días de inventario; diferenciales de calidad y localización.
- **Métodos aplicables**: ST-DESC, ST-INF, FIN-CAGR; descomposición de rentabilidad de futuros
  (spot, roll, collateral) por fichas nuevas; MC-04 para balances y ciclos de inversión; MC-05
  para escenarios; MC-07 para riesgo de curva.
- **Benchmarks**: índices de futuros de la familia; costes marginales declarados como
  estimación.
- **Riesgos frecuentes**: roll yield presentado como rentabilidad esperada del subyacente;
  referencia de futuros y precio físico regional mezclados; estacionalidad generalizada desde
  pocas campañas.
- **Convenciones**: unidad de contrato y conversión a unidades físicas; calendario de
  vencimientos y rol; moneda de contratación.
- **Pruebas**: identidades de la descomposición de rentabilidad; coherencia de la curva con
  costes declarados.
- **Insuficiencia**: sin curva de futuros líquida; inventarios no publicados; productos con
  mercados opacos solo con limitaciones declaradas.

## 7. PERF-ETF — Fondos, ETF y estructuras colectivas

**Estado: documentado · Prioridad: P1.** Familia: fondos de inversión, ETF, indexados y
vehículos cotizados.

- **Variables relevantes**: NAV, precio de mercado, prima/descuento; tracking difference y
  tracking error; tipo de replicación (física completa, muestreo, sintética); costes corrientes
  y costes implícitos (spreads, mercado); acumulación frente a distribución; retenciones;
  liquidez del fondo y de los subyacentes; riesgo de contraparte y colateral; préstamo de
  valores; flujos y creación/reembolso; concentración y solapamiento; moneda de cotización y
  clases cubiertas o no cubiertas; apalancamiento y rebalanceo diario en productos apalancados.
- **Métodos aplicables**: ST-DESC, ST-INF, FIN-CAGR; descomposición de la diferencia con el
  índice (costes, retenciones, replicación) por fichas nuevas; STC-1 para alineación de
  frecuencias y monedas.
- **Riesgos frecuentes**: comparar el fondo con un índice de otra variante (precio frente a
  retorno total); erosión por volatilidad en apalancados no declarada; solapamiento presentado
  como diversificación.
- **Convenciones**: variante del índice de referencia declarada (precio, retorno total, neto);
  moneda de la clase; calendario de distribución.
- **Insuficiencia**: histórico insuficiente del fondo; índice de referencia sin datos de la
  variante correcta; documentación del vehículo (KIID/prospecto) no disponible.

## 8. PERF-DER — Derivados, opciones y productos estructurados

**Estado: documentado · Prioridad: P1.** Familia: futuros, forwards, opciones, swaps y
derivados de crédito; productos con barreras y estructuras autocallables como casos de riesgo
no lineal.

- **Variables relevantes**: payoff y límites de arbitraje; volatilidad implícita, skew, smile
  y term structure; griegas (delta, gamma, vega, theta, rho); márgenes inicial y de
  mantenimiento, liquidación y margin calls; bases y roll; financiación (funding rates en
  derivados digitales).
- **Métodos aplicables**: Black-Scholes-Merton y árboles binomiales cuando su ficha lo declare;
  MC-05 para valoración por simulación y escenarios de pérdidas no lineales; MC-07 para riesgo
  de cola; RISK-VAR.
- **Riesgos frecuentes**: aplicar un modelo fuera de sus supuestos (barreras, temprano
  ejercicio); griegas sin contrato de subyacente declarado; estructuras con barrera sin el
  riesgo de gap.
- **Convenciones**: subyacente, multiplicador, calendario de ejercicios y liquidación; moneda
  de liquidación.
- **Insuficiencia**: superficie de volatilidad no disponible; subyacente con sesiones
  discontinuas sin ajuste declarado; estructuras con payoff no modelado en catálogo (rechazo
  con motivo).

## 9. PERF-REI — Inmobiliario, REIT/SOCIMI e infraestructuras

**Estado: documentado · Prioridad: P2.** Familia: activos inmobiliarios directos, REIT/SOCIMI,
sociedades cotizadas inmobiliarias, infraestructuras y activos de vida útil larga.

- **Variables relevantes**: NOI, ocupación, rentas efectivas y concesiones; cap rate, yield
  coste y cash-on-cash; IRR y múltiplos; LTV, LTC, DSCR y cobertura de la deuda; vencimientos
  y refinanciación; rent roll, WAULT y concentración de inquilinos; CAPEX y obsolescencia;
  ciclos inmobiliarios, oferta futura y absorción; FFO, AFFO y NAV para REIT/SOCIMI; flujos
  regulados y concesionales en infraestructuras.
- **Métodos aplicables**: FIN-CAGR, ST-DESC, ST-INF; capitalización de rentas y modelos
  declarados como supuestos; MC-03 para sensibilidades a tipos; MC-05 para escenarios.
- **Riesgos frecuentes**: cap rate sin especificar base (neto de CAPEX o no); NAV de REIT
  presentado como precio objetivo; flujos regulados con riesgo regulatorio no declarado.
- **Convenciones**: moneda; superficie y unidades de medida; frecuencia de valoración
  (valuaciones infrecuentes declaradas).
- **Insuficiencia**: valoraciones infrecuentes sin alternativa declarada; contratos de
  arrendamiento no disponibles; regulación local no consultada.

## 10. PERF-CHR — Criptoactivos y activos digitales

**Estado: documentado, con cautela metodológica declarada · Prioridad: P2.** Familia:
criptoactivos, stablecoins y finanzas descentralizadas.

- **Variables relevantes**: precio, volatilidad y profundidad de liquidez; capitalización
  circulante y fully diluted; emisión, inflación, quema y staking; tokenómica, distribución y
  desbloqueos; métricas on-chain (actividad, comisiones, direcciones, flujos) **con cautela
  metodológica**: su relación con el valor económico capturado no se presume; stablecoins:
  reservas, mecanismo de paridad y riesgo de desanclaje; financiación, basis y funding rates;
  riesgo de contratos inteligentes, puentes, oráculos, custodia y consenso.
- **Métodos aplicables**: ST-DESC, ST-INF, FX-style de volatilidad y regímenes (con las
  conversiones declaradas); MC-02 y MC-06 bajo demanda; RISK-VAR con advertencia de colas
  extremas; fichas específicas por el cauce de tipos 3.
- **Riesgos frecuentes**: métricas de actividad interpretadas como valor; datos on-chain sin
  definición de fuente ni de método de medición; desanclaje tratado como riesgo de cola
  convencional.
- **Convenciones**: UTC por defecto; unidad de activo; cadena y versión de protocolo;
  fuente on-chain con su fecha de consulta.
- **Insuficiencia**: sin fuente on-chain verificable; protocolo en cambio activo; liquidez
  insuficiente para las métricas declaradas.

## 11. PERF-PRV — Capital privado, venture capital y financiación privada

**Estado: documentado · Prioridad: P2.** Familia: private equity, venture capital, deuda
privada y rondas de financiación.

- **Variables relevantes**: valoración por rondas y comparables; IRR, MOIC, DPI, RVPI y TVPI;
  distribución temporal de flujos, curvas J y duración del compromiso; dilución, preferencias
  de liquidación, waterfall y derechos; riesgo de down rounds y de financiación adicional;
  desfase de valoración (stale prices); sesgos de supervivencia y selección de bases privadas;
  covenants e impago en deuda privada.
- **Métodos aplicables**: ST-DESC, ST-INF; MC-05 para escenarios de salida; descomposición de
  rentabilidad por cohortes como ficha nueva; siempre con la limitación de valoración
  infrecuente declarada.
- **Riesgos frecuentes**: IRR reportado tratado como rentabilidad realizable; múltiplos de
  salida sin sensibilidad; ausencia de ajuste por desfase de precios en comparaciones con
  líquidos.
- **Convenciones**: fecha de cash flow, moneda y comisiones del vehículo declaradas.
- **Insuficiencia**: sin datos de flujos del vehículo; valoración anterior a doce meses sin
  actualización plausible; estructura jurídica desconocida.

## 12. PERF-ALT — Inversiones alternativas y activos no tradicionales

**Estado: documentado · Prioridad: P2.** Familia: hedge funds y estrategias alternativas;
infraestructuras de ingresos; derechos de propiedad intelectual y royalties; arte,
coleccionables y activos físicos especializados; cat bonds y seguros vinculados a eventos;
créditos de carbono y certificados ambientales.

- **Variables relevantes**: estrategia y exposición del vehículo; flujos subyacentes y su
  duración; dispersión de precios y costes de intermediación; custodia, autenticidad y
  fraude; ausencia de precios continuos y valoración subjetiva; restricciones de
  transmisión; estructura del evento (cat bonds) o del certificado (carbono) y su régimen
  regulatorio.
- **Métodos aplicables**: ST-DESC, ST-INF sobre series escasas con límites declarados;
  escenarios MC-05; valoración por transacciones comparables solo cuando existan y con su
  dispersión declarada.
- **Riesgos frecuentes**: series mensuales marcadas a modelo tratadas como mercado;
  comparables sin ajuste de calidad o autenticidad; fraude y falsificación no evaluados.
- **Insuficiencia**: sin precios observables; mercado bilateral sin historial; régimen
  regulatorio indeterminado. La conclusión «no hay datos suficientes» es el resultado
  esperado en muchas familias de este perfil (regla crítica 21).

## 13. Capas transversales: PERF-TEM y PERF-ESG

**PERF-TEM (inversión temática, sectores y cadenas de valor) · Estado: documentado ·
Prioridad: P1 como capa.** Se aplica sobre el perfil de la clase de activo cuando la pregunta
es temática o sectorial: tamaño de mercado y ritmo de adopción; curvas de difusión y madurez
tecnológica; costes unitarios, curvas de aprendizaje y economías de escala; capacidad,
inventarios y plazos; cuellos de botella y dependencia de proveedores; CAPEX previsto y
retorno incremental; elasticidades y sustitución tecnológica; márgenes por eslabón de la
cadena de valor; patentes e I+D; adopción real frente a anuncios; escenarios de disrupción y
de difusión lenta; y la relación entre la tendencia tecnológica y los activos expuestos. Los
métodos típicos viven en MC-04 (crecimiento, difusión, prospectiva) y MC-03 (relaciones).

**PERF-ESG (inversión sostenible y riesgos climáticos) · Estado: documentado, con limitaciones
de datos declaradas · Prioridad: P2 como capa.** Se aplica sobre el perfil de la clase de
activo cuando la pregunta lo requiere: métricas ambientales, sociales y de gobernanza
cuantificables; emisiones directas e indirectas, intensidad de carbono y trayectorias; riesgos
físico y de transición; exposición regulatoria, impuestos y subvenciones; costes de adaptación;
escenarios climáticos; riesgos de litigio y reputación; calidad, comparabilidad, cobertura y
limitaciones de los datos ESG; doble materialidad cuando proceda; riesgo de greenwashing y
diferencia entre etiquetas y exposición efectiva. Regla dura: las métricas ESG se citan con su
fuente, su metodología y su cobertura; la falta de datos se declara y nunca se imputa.

## 14. Activos híbridos: combinación declarada de perfiles

Cuando un activo pertenece a varias categorías ---un ETF de bonos denominados en divisas (PERF-ETF
+ PERF-FIR + PERF-FX), un bono convertible (PERF-FIR + PERF-DER + PERF-ACC) o un derivado sobre
materias primas (PERF-DER + PERF-CMD)---, el Orquestador de Cálculo combina los perfiles
compatibles, declara la combinación en el plan y en la respuesta (perfil_aplicable con la lista
de PERF-xx), y explicita los **riesgos cruzados** (divisa, base, liquidez, roll, correlación)
en la entrega. No se fuerza una clasificación única que elimine información: la clase MIX se
registra cuando la combinación es la descripción correcta. Los perfiles no compatibles entre sí
para una misma operación (por ejemplo, una métrica definida solo para acciones) no se aplican
por simetría: se declaran como no aplicables.

## 15. Pruebas y registro de versiones

Cada perfil declara sus pruebas de validación; la batería mínima del Plan de pruebas del Bloque
A (V1.0) incluye las pruebas P-01 a P-20, de las cuales las P-01 (implicaciones por clase de
activo), P-02 (híbrido con dos perfiles), P-03 (datos insuficientes) y P-19 (liquidez o costes
que hacen inviable la exposición) son pruebas de perfiles. Ningún perfil pasa a «validado» sin
la evidencia de su ejecución registrada.

| Versión | Fecha | Cambios |
|---|---|---|
| V1.0 | 01/11/2026 | Primera versión, aplicada con la petición maestra de modificación y optimización del Bloque A: marco de perfiles (formato estándar, reglas de uso, estados y prioridades) y doce perfiles definidos: PERF-ACC, PERF-FIR, PERF-FX (primer perfil maduro, heredero de la especialización divisas), PERF-CMD, PERF-ETF, PERF-DER, PERF-REI, PERF-CHR, PERF-PRV, PERF-ALT y las capas transversales PERF-TEM y PERF-ESG; combinación declarada en activos híbridos. Estados: documentados; el lote FX del Catálogo V3.0 opera en servicio; la validación por pruebas queda pendiente de ejecución y se registra en el Plan de pruebas. |
