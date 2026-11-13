# Catálogo — Catálogo de cálculos del Motor de Cálculo Avanzado (AG-13)

**Bloque A · Robot Investor · Versión óptima V5.0 · 02/11/2026** · Subordinado al Documento 0 óptima V5.0.

Archivo CC (propietario: operador, por cambio de tipo 3; el Motor propone). Lectores: AG-13 y sus módulos, AG-15, Analistas de tipo de activo (AG-03 a AG-09 y AG-21 a AG-25), Orquestador técnico. `catalog_version` 5.0. «Tipo de activo» y «clase de activo» son sinónimos (2.6 del Documento 0).

---

## 1. Propósito y reglas de uso

1.1. El catálogo especifica, operación a operación, **qué calcula el Motor, con qué datos mínimos, con qué supuestos, con qué tolerancias y contra qué referencia ingenua se compara**. Cada servicio CT-09 cita en su campo `operacion` un `ficha_id` y su versión; cada re-ejecución CT-10 usa la ficha y la versión citadas en el artefacto original.

1.2. **Cobertura no es obligación.** El catálogo define lo que el Motor sabe tratar; los métodos se activan bajo demanda, cuando pueden cambiar una decisión (R15, 7.5 del Documento 0). Ninguna investigación ejecuta todo el catálogo.

1.3. **Estado de gobierno y madurez.** Cada ficha tiene un estado de gobierno (`VIGENTE`, `EN_REVISION`, `DEPRECADA`, `BORRADOR`) y un estado de madurez (R22):

| Madurez | Significado | Uso permitido |
|---|---|---|
| DOCUMENTADO | Especificación publicada; sin implementación verificada en el entorno de ejecución | El Motor no entrega cifras citables con ella: responde `RECHAZADO` con motivo `METODO_NO_IMPLEMENTADO` y, si existe, ofrece la alternativa del núcleo transversal con la limitación declarada |
| IMPLEMENTADO | Disponible en el entorno de ejecución y con casos de control superados | Servicio normal; la entrega declara «implementado, no validado» |
| VALIDADO | Batería de pruebas de `09_Pruebas` ejecutada con evidencia registrada | Servicio normal sin advertencia de madurez |

Estado actual de las 81 fichas: 71 **IMPLEMENTADO** (14 del ejecutor V1.0 con pruebas unitarias y 57 con casos de control registrados, T-106 y T-112); 10 **DOCUMENTADO** (10 de la línea V4.0). Ninguna ficha está VALIDADA.

1.4. **Cambios.** Alta, modificación o deprecación de fichas: propuesta del Motor (evidencia de uso del Registro de cálculos, casos de control, impacto) y aprobación del operador (tipo 3). Las versiones no se sobrescriben: conviven para permitir re-ejecuciones exactas.

1.5. **Operaciones sin ficha.** Una operación que ninguna ficha cubre se rechaza con motivo y la ficha más próxima; si el solicitante necesita un cálculo exploratorio no citable, el Motor puede servirlo con la marca `op_sin_ficha` y `clase_cifra` ESTADISTICA, que impide su uso como cifra de un entregable (PS8, G3).

1.6. **Frontera con el Bloque B** (2.5 del Documento 0). Toda ficha opera sobre **ámbitos** (mercado, índice, sector, subsector, segmento, categoría de vehículos, curva, factor, estrategia) y sus **indicadores de seguimiento**. Los datos de instrumentos individuales (valores, emisiones, fondos, contratos, tokens) solo entran como componentes de un agregado o como representación genérica de un tramo (bono genérico a 10 años, opción ATM a 3 meses, futuro a vencimiento constante). Ninguna ficha compara, ordena ni selecciona instrumentos concretos, ni sus costes, comisiones o plataformas: una petición con ese propósito se rechaza con `FUERA_DE_CATALOGO` y la ficha de ámbito más próxima.

## 2. Ficha estándar

Toda ficha contiene, en este orden:

| # | Campo | Contenido |
|---|---|---|
| 1 | Identificación | `ficha_id` (FAM-NOMBRE-NNN), nombre, versión, estado de gobierno, módulo responsable (MC-01…MC-10), áreas del Mapa de conocimientos |
| 2 | Perfiles y horizontes | Perfiles compatibles (PERF-xx o TRANSVERSAL) y horizontes H1–H4 en los que el método es informativo |
| 3 | Propósito | Pregunta cuantitativa que responde, en una frase |
| 4 | Método | Pasos y fórmulas esenciales; opciones declaradas |
| 5 | Entradas mínimas | Tipo, unidad, longitud y frecuencia mínimas; conocibilidad |
| 6 | Parámetros y rangos | Nombre, valor por defecto, rango admitido |
| 7 | Salidas con unidades | Forma (VALOR, TABLA, SERIE, DISTRIBUCION), contenido, unidades, clase de cifra (DETERMINISTA o ESTADISTICA) |
| 8 | Supuestos y limitaciones | Condiciones de validez y advertencias obligatorias de entrega |
| 9 | Tolerancias y semilla | Tolerancia de re-ejecución (CT-10); semilla `null` o regla de semilla |
| 10 | Verificación interna | Identidades, casos de control, segunda vía |
| 11 | Referencia ingenua | Comparación obligatoria cuando el resultado se usa como previsión o señal (códigos de 3.3) |
| 12 | Aclaración y rechazo | Cuándo se pide aclaración y cuándo se rechaza |
| 13 | Referencias canónicas | Autor, año, título; temática TM- de F8 para que el Documentador para el Motor mantenga el respaldo |
| 14 | Prioridad y madurez | P0/P1/P2 y DOCUMENTADO/IMPLEMENTADO/VALIDADO |

## 3. Convenciones comunes (se aplican a todas las fichas salvo que la ficha diga otra cosa)

### 3.1 Convenciones numéricas y de servicio

- **Servicios técnicos**: toda ficha usa STC-1 (validación y calidad de datos), STC-2 (ejecución numérica, aritmética decimal, semillas), STC-3 (métodos y fichas versionadas) y STC-4 (artefacto y linaje). No se repite en cada ficha.
- **Rendimientos** simples por defecto; logarítmicos solo si la ficha lo pide, etiquetados. **Anualización**: 252 sesiones (365 días naturales en criptoactivos, que cotizan siempre), capitalización compuesta. **Recuento de días**: Real/365 salvo convención de mercado (renta fija, monetario). **Redondeo**: de banquero, solo al final; 4 decimales por defecto. **Divisa**: la de la petición; conversiones con tipo, fecha y fuente.
- **Conocibilidad**: todo dato lleva `conocible_desde`; en evaluaciones y backtests nada posterior a la fecha de corte entra en el cálculo.
- **Verificación**: doble pasada independiente siempre; segunda vía recomendada en PLAN_STD y obligatoria en PLAN_EXT y en cifras en banda marginal (PS8).
- **Planes**: PLAN_MIN (una operación, verificación estándar), PLAN_STD (cadena, segunda vía si la ficha la declara, sensibilidad básica), PLAN_EXT (contraste multivía, sensibilidad por escenarios, propagación de incertidumbre).

### 3.2 Tolerancias por defecto (si la ficha no fija otra)

| Tipo de cálculo | Tolerancia |
|---|---|
| Aritmética determinista | 1e-10 relativa |
| Fórmulas cerradas | 1e-8 relativa |
| Estimadores iterativos | 1e-6 relativa en parámetros |
| Simulación o bootstrap con la misma semilla | 1e-6 relativa |
| Fechas, etiquetas, decisiones de contraste | Igualdad exacta |

### 3.3 Referencias ingenuas (códigos)

| Código | Referencia | Uso típico |
|---|---|---|
| RI-PA | Paseo aleatorio sin deriva (último valor) | Precios, tipos de cambio, tipos de interés, diferenciales |
| RI-MH | Media histórica conocida en t | Rendimientos esperados, valoraciones con reversión |
| RI-TB | Tasa base expansiva (frecuencia histórica del suceso conocida en t) | Dirección, probabilidad de superar umbral |
| RI-EST | Estacional ingenua (mismo periodo del ciclo anterior o media estacional) | Inventarios, demanda, series con estacionalidad |
| RI-CM | Comprar y mantener la referencia de comparación del tipo de activo (8.4 del Documento 0) | Rentabilidad de opciones del top-3 |
| RI-CLI | Climatología (distribución incondicional histórica conocida en t) | Probabilidades y distribuciones |
| RI-EWMA | Volatilidad EWMA (λ = 0,94) | Previsiones de volatilidad |
| RI-NA | No aplica (cálculo determinista o descriptivo, no es previsión) | Precio de un bono, puntuaciones |

### 3.4 Prioridades

**P0** núcleo transversal imprescindible para el funcionamiento del bloque (incluye todo lo que exige R13 y G3); **P1** métodos propios de tipo de activo con datos accesibles y alto uso; **P2** ampliación (datos especializados o uso ocasional).

## 4. Índice de fichas

| ficha_id | Nombre | Módulo | Perfiles | Horizontes | Prioridad | Madurez |
|---|---|---|---|---|---|---|
| FX-TREND-001 | Detección y medición de tendencia | MC-02 | TRANSVERSAL | H2–H4 | P0 | IMPLEMENTADO (ejecutor V1.0, pruebas unitarias) |
| FX-BRK-001 | Rupturas estructurales | MC-02 | TRANSVERSAL | H2–H4 | P0 | IMPLEMENTADO (ejecutor, casos de control registrados (T-112)) |
| FX-STL-001 | Descomposición tendencia-ciclo-estacionalidad | MC-02 | TRANSVERSAL | H2–H4 | P0 | IMPLEMENTADO (ejecutor, casos de control registrados (T-112)) |
| FX-VOL-001 | Volatilidad realizada e implícita | MC-02 | TRANSVERSAL | H1–H3 | P0 | IMPLEMENTADO (ejecutor V1.0, pruebas unitarias) |
| FX-REGIME-001 | Regímenes univariantes (Markov switching) | MC-02 | TRANSVERSAL | H2–H4 | P0 | IMPLEMENTADO (ejecutor, casos de control registrados (T-112)) |
| FX-PPA-001 | Desviación de PPA relativa | MC-03 | PERF-FX | H4 (H3 limitado) | P1 | IMPLEMENTADO (ejecutor, casos de control registrados (T-112)) |
| FX-CARRY-001 | Diferencial de tipos y carry | MC-03 | PERF-FX, PERF-FIR | H1–H3 | P1 | IMPLEMENTADO (ejecutor V1.0, pruebas unitarias) |
| FX-COINT-001 | Cointegración y corrección de errores | MC-03 | TRANSVERSAL | H3–H4 | P1 | IMPLEMENTADO (ejecutor, casos de control registrados (T-112)) |
| FX-CORR-001 | Correlación dinámica y dependencia de cola | MC-03 | TRANSVERSAL | H1–H4 | P0 | IMPLEMENTADO (ejecutor V1.0, pruebas unitarias) |
| ST-DESC-001 | Estadística descriptiva | MC-01 | TRANSVERSAL | — | P0 | IMPLEMENTADO (ejecutor V1.0, pruebas unitarias) |
| ST-INF-001 | Contrastes, intervalos y comparaciones múltiples | MC-01 | TRANSVERSAL | — | P0 | IMPLEMENTADO (ejecutor, casos de control registrados (T-112)) |
| FIN-CAGR-001 | Crecimiento, anualización, nominal/real | MC-01 | TRANSVERSAL | — | P0 | IMPLEMENTADO (ejecutor V1.0, pruebas unitarias) |
| BIB-MET-001 | Bibliometría aplicada a fuentes | MC-01 | TRANSVERSAL | — | P1 | IMPLEMENTADO (ejecutor, casos de control registrados (T-112)) |
| SIM-MC-001 | Simulación Monte Carlo de trayectorias | MC-05 | TRANSVERSAL | H1–H4 | P0 | IMPLEMENTADO (ejecutor, casos de control registrados (T-112)) |
| RISK-VAR-001 | VaR y Expected Shortfall | MC-07 | TRANSVERSAL | H1–H3 | P0 | IMPLEMENTADO (ejecutor, casos de control registrados (T-112)) |
| ML-CAL-001 | Evaluación interna de modelos predictivos | MC-06 | TRANSVERSAL | H1–H4 | P0 | IMPLEMENTADO (ejecutor, casos de control registrados (T-112)) |
| AUD-REX-001 | Re-ejecución independiente (CT-10) | MC-08 | TRANSVERSAL | — | P0 | IMPLEMENTADO (ejecutor, casos de control registrados (T-112)) |
| SCORE-RK-001 | Puntuaciones T/E/M/P/A y clave RK (idéntico a HT-03) | MC-01 | TRANSVERSAL | — | P0 | IMPLEMENTADO (ejecutor V1.0, pruebas unitarias) |
| FC-EVAL-001 | Evaluación de pronósticos: Brier, log-score, CRPS, acierto, DM-HLN | MC-10 | TRANSVERSAL | H1–H4 | P0 | IMPLEMENTADO (ejecutor V1.0, pruebas unitarias) |
| FC-CAL-001 | Calibración: fiabilidad, ECE con nulo, PIT, cobertura | MC-10 | TRANSVERSAL | H1–H4 | P0 | IMPLEMENTADO (ejecutor V1.0, pruebas unitarias) |
| BT-DSR-001 | Sharpe probabilístico y Deflated Sharpe | MC-10 | TRANSVERSAL | H2–H4 | P0 | IMPLEMENTADO (ejecutor, casos de control registrados (T-112)) |
| BT-PBO-001 | Probabilidad de sobreajuste del backtest (CSCV) | MC-10 | TRANSVERSAL | H2–H4 | P1 | IMPLEMENTADO (ejecutor, casos de control registrados (T-112)) |
| BT-VAR-001 | Backtesting de VaR y ES | MC-10 | TRANSVERSAL | H1–H2 | P1 | IMPLEMENTADO (ejecutor, casos de control registrados (T-112)) |
| SCN-H-001 | Escenarios por horizonte | MC-05 | TRANSVERSAL | H1–H4 | P0 | IMPLEMENTADO (ejecutor, casos de control registrados (T-112)) |
| VOL-GARCH-001 | Volatilidad condicional GARCH | MC-02 | TRANSVERSAL | H1–H2 (H3 limitado) | P0 | IMPLEMENTADO (ejecutor V1.0, pruebas unitarias) |
| REG-HMM-001 | Régimen de clase (HMM multivariante) | MC-02 | TRANSVERSAL | H2–H3 | P1 | IMPLEMENTADO (ejecutor, casos de control registrados (T-112)) |
| ML-PRED-001 | Modelo predictivo supervisado con walk-forward | MC-06 | TRANSVERSAL | H1–H3 | P1 | IMPLEMENTADO (ejecutor, casos de control registrados (T-112)) |
| ML-CLUS-001 | Clústeres de exposición y apuestas independientes | MC-06 | TRANSVERSAL | — | P0 | IMPLEMENTADO (ejecutor V1.0, pruebas unitarias) |
| RISK-DD-001 | Drawdown, liquidez y escala de riesgo 1–5 | MC-07 | TRANSVERSAL | H2–H4 | P0 | IMPLEMENTADO (ejecutor V1.0, pruebas unitarias) |
| DEC-VOI-001 | Valor de la información de un cálculo o búsqueda | MC-07 | TRANSVERSAL | — | P1 | IMPLEMENTADO (ejecutor, casos de control registrados (T-112)) |
| DER-OPT-001 | Opciones: BSM, binomial, griegas, volatilidad implícita | MC-09 | PERF-DER (+ PERF-ACC, PERF-IDX, PERF-FIR, PERF-FX, PERF-CMD, PERF-CHR, PERF-TCV) | H1–H3 | P1 | IMPLEMENTADO (ejecutor, casos de control registrados (T-112)) |
| TEM-DIFF-001 | Curvas de difusión y adopción | MC-04 | PERF-TEM (capa) | H3–H4 | P1 | IMPLEMENTADO (ejecutor, casos de control registrados (T-112)) |
| ACC-VAL-001 | DCF, DCF inverso y múltiplos | MC-09 | PERF-ACC (+ PERF-REI) | H3–H4 | P1 | IMPLEMENTADO (ejecutor, casos de control registrados (T-112)) |
| ACC-ERP-001 | Prima de riesgo implícita | MC-09 | PERF-ACC, PERF-IDX | H4 (H3 contexto) | P1 | IMPLEMENTADO (ejecutor, casos de control registrados (T-112)) |
| ACC-FACT-001 | Exposición factorial | MC-09 | PERF-ACC (+ PERF-IDX, PERF-ALT, PERF-ETF, PERF-REI) | H2–H4 | P1 | IMPLEMENTADO (ejecutor, casos de control registrados (T-112)) |
| ACC-MOM-001 | Momentum 12-1 y de series temporales | MC-09 | PERF-ACC (+ TRANSVERSAL) | H2–H3 | P1 | IMPLEMENTADO (ejecutor V1.0, pruebas unitarias) |
| FIR-PRICE-001 | Precio, rendimiento, duración y convexidad | MC-09 | PERF-FIR | H1–H4 | P1 | IMPLEMENTADO (ejecutor, casos de control registrados (T-112)) |
| FIR-CURVE-001 | Curva Nelson-Siegel-Svensson y valor relativo | MC-09 | PERF-FIR | H2–H4 | P1 | IMPLEMENTADO (ejecutor, casos de control registrados (T-112)) |
| FIR-CARRY-001 | Carry y rolldown | MC-09 | PERF-FIR (+ PERF-TCV) | H2–H3 | P1 | IMPLEMENTADO (ejecutor, casos de control registrados (T-112)) |
| FIR-SPREAD-001 | Percentil y valor del diferencial de crédito | MC-09 | PERF-FIR | H2–H4 | P1 | IMPLEMENTADO (ejecutor, casos de control registrados (T-112)) |
| FIR-CRED-001 | Merton agregado: distancia al impago y diferencial implícito de un segmento | MC-09 | PERF-FIR (+ PERF-TCV, PERF-ACC) | H3–H4 | P2 | Documentado |
| FX-BEER-001 | Tipo de cambio real de equilibrio (BEER) | MC-03 | PERF-FX | H4 (H3 limitado) | P2 | Documentado |
| FX-MOM-001 | Momentum cambiario y carry ajustado por volatilidad | MC-09 | PERF-FX | H1–H3 | P1 | IMPLEMENTADO (ejecutor, casos de control registrados (T-112)) |
| CMD-CURVE-001 | Estructura de la curva de futuros y roll yield | MC-09 | PERF-CMD | H1–H3 | P1 | IMPLEMENTADO (ejecutor V1.0, pruebas unitarias) |
| CMD-INV-001 | Inventarios frente a media estacional | MC-02 | PERF-CMD | H2–H3 | P1 | IMPLEMENTADO (ejecutor, casos de control registrados (T-112)) |
| CMD-RETDEC-001 | Descomposición de la rentabilidad de futuros | MC-09 | PERF-CMD | H3–H4 | P1 | IMPLEMENTADO (ejecutor, casos de control registrados (T-112)) |
| CMD-REAL-001 | Precio real y coste marginal | MC-09 | PERF-CMD | H4 (H3 contexto) | P2 | Documentado |
| REI-NAV-001 | Prima/descuento sobre NAV | MC-09 | PERF-REI | H3–H4 | P1 | IMPLEMENTADO (ejecutor, casos de control registrados (T-112)) |
| REI-CAP-001 | Cap rate y diferencial cap rate–bono | MC-09 | PERF-REI (+ PERF-PRV) | H3–H4 | P1 | IMPLEMENTADO (ejecutor, casos de control registrados (T-112)) |
| REI-FFO-001 | FFO/AFFO y sostenibilidad del dividendo | MC-09 | PERF-REI | H3 | P1 | IMPLEMENTADO (ejecutor, casos de control registrados (T-112)) |
| REI-LEV-001 | Apalancamiento y riesgo de refinanciación | MC-09 | PERF-REI | H3–H4 | P2 | Documentado |
| CHR-ONCHAIN-001 | MVRV y NVT | MC-09 | PERF-CHR | H3 (H2 contexto; H4 limitado) | P2 | Documentado |
| CHR-FUND-001 | Financiación de perpetuos y base | MC-09 | PERF-CHR | H1–H2 | P1 | IMPLEMENTADO (ejecutor, casos de control registrados (T-112)) |
| CHR-FLOW-001 | Flujos de ETF y oferta de stablecoins | MC-02 | PERF-CHR | H1–H2 | P1 | IMPLEMENTADO (ejecutor, casos de control registrados (T-112)) |
| CHR-TOKEN-001 | Tokenómica y dilución | MC-09 | PERF-CHR | H2–H4 | P2 | Documentado |
| PRV-PME-001 | Public market equivalent | MC-09 | PERF-PRV | H4 | P2 | Documentado |
| PRV-CF-001 | TIR, múltiplos, curva J y proyección de flujos | MC-09 | PERF-PRV | H4 | P2 | Documentado |
| ALT-DESMOOTH-001 | Desuavizado de rentabilidades | MC-09 | PERF-PRV, PERF-ALT (+ PERF-REI, PERF-ETF) | H3–H4 | P1 | IMPLEMENTADO (ejecutor, casos de control registrados (T-112)) |
| ALT-HF-001 | Exposición factorial de estrategias hedge | MC-09 | PERF-ALT (+ PERF-ETF) | H3–H4 | P2 | Documentado |
| ALT-AUC-001 | Índice de transacciones de coleccionables | MC-09 | PERF-ALT | H4 | P2 | Documentado |
| IDX-ERP-001 | Rentabilidad esperada por índice (Grinold-Kroner) | MC-09 | PERF-IDX (+ PERF-ACC) | H4 (H3 contexto) | P1 | IMPLEMENTADO (ejecutor, casos de control registrados (T-106)) |
| IDX-CONC-001 | Concentración y amplitud de un índice | MC-01 | PERF-IDX (+ PERF-ACC) | H2–H4 | P1 | IMPLEMENTADO (ejecutor, casos de control registrados (T-106)) |
| IDX-REL-001 | Valor relativo entre índices | MC-09 | PERF-IDX | H2–H4 | P1 | IMPLEMENTADO (ejecutor, casos de control registrados (T-106)) |
| IDX-REB-001 | Efecto de rebalanceo y cambios de composición | MC-03 | PERF-IDX | H1 (limitado)–H2 | P2 | IMPLEMENTADO (ejecutor, casos de control registrados (T-106)) |
| FON-DISC-001 | Descuento de fondos cerrados frente a su media (z-score) | MC-09 | PERF-ETF (+ PERF-PRV, PERF-REI) | H3–H4 (H2 limitado) | P1 | IMPLEMENTADO (ejecutor, casos de control registrados (T-106)) |
| FON-FLOW-001 | Flujos por categoría de vehículos | MC-02 | PERF-ETF (+ todos como señal de demanda) | H2 (limitado)–H3 | P1 | IMPLEMENTADO (ejecutor, casos de control registrados (T-106)) |
| FON-TD-001 | Diferencia de seguimiento agregada por categoría | MC-01 | PERF-ETF | H3–H4 | P2 | IMPLEMENTADO (ejecutor, casos de control registrados (T-106)) |
| FON-LEV-001 | Decaimiento por volatilidad de vehículos apalancados e inversos | MC-09 | PERF-ETF (+ PERF-DER) | H2 (limitado)–H3 | P2 | IMPLEMENTADO (ejecutor, casos de control registrados (T-106)) |
| DER-VRP-001 | Prima de varianza implícita-realizada | MC-09 | PERF-DER (+ PERF-TCV) | H1–H3 | P1 | IMPLEMENTADO (ejecutor, casos de control registrados (T-106)) |
| DER-SKEW-001 | Sesgo de la volatilidad implícita | MC-09 | PERF-DER (+ PERF-FX, PERF-TCV) | H1–H3 | P1 | IMPLEMENTADO (ejecutor, casos de control registrados (T-106)) |
| DER-TERM-001 | Estructura de plazos de la volatilidad implícita | MC-09 | PERF-DER (+ PERF-TCV, PERF-IDX) | H1–H3 | P1 | IMPLEMENTADO (ejecutor, casos de control registrados (T-106)) |
| DER-ROLL-001 | Carry y roll de futuros financieros | MC-09 | PERF-DER (+ PERF-TCV, PERF-FX) | H1–H3 | P1 | IMPLEMENTADO (ejecutor, casos de control registrados (T-106)) |
| MON-YLD-001 | Rentabilidad equivalente y comparación de segmentos monetarios | MC-01 | PERF-MON (+ PERF-FX) | H1 (limitado)–H3 | P1 | IMPLEMENTADO (ejecutor, casos de control registrados (T-106)) |
| MON-EXP-001 | Expectativas implícitas de tipos a corto | MC-09 | PERF-MON (+ PERF-FIR, PERF-TCV, PERF-FX) | H1 (limitado)–H3 | P1 | IMPLEMENTADO (ejecutor, casos de control registrados (T-106)) |
| MON-REAL-001 | Rentabilidad real a corto plazo | MC-01 | PERF-MON (+ PERF-FIR) | H2–H3 | P1 | IMPLEMENTADO (ejecutor, casos de control registrados (T-106)) |
| MON-FIX-001 | Valor de fijar plazo frente a renovar | MC-09 | PERF-MON | H2–H3 | P1 | IMPLEMENTADO (ejecutor, casos de control registrados (T-106)) |
| TCV-SLOPE-001 | Pendiente de la curva y su valor razonable | MC-09 | PERF-TCV (+ PERF-FIR, PERF-ACC como indicador de ciclo) | H1–H3 (H4 limitado) | P1 | IMPLEMENTADO (ejecutor, casos de control registrados (T-106)) |
| TCV-BEI-001 | Inflación implícita frente a esperada | MC-09 | PERF-TCV (+ PERF-FIR, PERF-REI) | H2–H3 (H4 limitado) | P1 | IMPLEMENTADO (ejecutor, casos de control registrados (T-106)) |
| TCV-CDS-001 | Diferencial de índice CDS frente a pérdidas esperadas | MC-09 | PERF-TCV (+ PERF-FIR) | H2–H3 (H4 limitado) | P1 | IMPLEMENTADO (ejecutor, casos de control registrados (T-106)) |
| TCV-VIXTS-001 | Estructura de plazos del VIX y roll de sus futuros | MC-09 | PERF-TCV (+ PERF-DER) | H1–H3 | P1 | IMPLEMENTADO (ejecutor, casos de control registrados (T-106)) |
| TCV-TP-001 | Prima por plazo | MC-09 | PERF-TCV (+ PERF-FIR, PERF-MON) | H3 (H2 contexto; H4 limitado) | P1 | IMPLEMENTADO (ejecutor, casos de control registrados (T-106)) |

Total: 81 fichas (17 heredadas de la línea V3.0, 43 de la línea V4.0 y 21 incorporadas en V5.0 para IDX, FON, DER, MON y TCV).

## 5. Cobertura por tipo de activo y por horizonte

### 5.1 Operaciones propias por tipo de activo (mínimo 4)

| Tipo | Perfil | Fichas propias | Transversales más usadas |
|---|---|---|---|
| RV | PERF-ACC | ACC-VAL-001, ACC-ERP-001, ACC-FACT-001, ACC-MOM-001 | FX-TREND-001, VOL-GARCH-001, REG-HMM-001, RISK-VAR-001, IDX-CONC-001 |
| RF | PERF-FIR | FIR-PRICE-001, FIR-CURVE-001, FIR-CARRY-001, FIR-SPREAD-001, FIR-CRED-001 | FX-BRK-001, REG-HMM-001, FX-CORR-001, TCV-TP-001 |
| DIV | PERF-FX | FX-PPA-001, FX-CARRY-001, FX-BEER-001, FX-MOM-001 | FX-VOL-001, VOL-GARCH-001, FX-REGIME-001, FX-COINT-001, MON-EXP-001 |
| MP | PERF-CMD | CMD-CURVE-001, CMD-INV-001, CMD-RETDEC-001, CMD-REAL-001 | FX-STL-001, VOL-GARCH-001, ACC-MOM-001 (momentum de series temporales) |
| IDX | PERF-IDX | IDX-ERP-001, IDX-CONC-001, IDX-REL-001, IDX-REB-001 | ACC-ERP-001, ACC-MOM-001, ACC-FACT-001, REG-HMM-001 |
| FON | PERF-ETF | FON-DISC-001, FON-FLOW-001, FON-TD-001, FON-LEV-001 | ALT-HF-001, ALT-DESMOOTH-001, VOL-GARCH-001, RISK-DD-001 |
| DER | PERF-DER | DER-VRP-001, DER-SKEW-001, DER-TERM-001, DER-ROLL-001, DER-OPT-001 | FX-VOL-001, VOL-GARCH-001, SIM-MC-001, RISK-VAR-001 |
| INM | PERF-REI | REI-NAV-001, REI-CAP-001, REI-FFO-001, REI-LEV-001 | ALT-DESMOOTH-001, ACC-FACT-001, FIR-CURVE-001, TCV-BEI-001 |
| CRI | PERF-CHR | CHR-ONCHAIN-001, CHR-FUND-001, CHR-FLOW-001, CHR-TOKEN-001 | VOL-GARCH-001, RISK-VAR-001, REG-HMM-001 |
| ALT | PERF-PRV, PERF-ALT | PRV-PME-001, PRV-CF-001, ALT-DESMOOTH-001, ALT-HF-001, ALT-AUC-001 | RISK-DD-001, ACC-FACT-001, FIR-SPREAD-001, REI-CAP-001 |
| MON | PERF-MON | MON-YLD-001, MON-EXP-001, MON-REAL-001, MON-FIX-001 | FIN-CAGR-001, FIR-CURVE-001, FX-CARRY-001 |
| TCV | PERF-TCV | TCV-SLOPE-001, TCV-BEI-001, TCV-CDS-001, TCV-VIXTS-001, TCV-TP-001 | FIR-CURVE-001, FIR-CARRY-001, FIR-SPREAD-001, DER-VRP-001, REG-HMM-001 |

### 5.2 Métodos por horizonte

Los horizontes de cada ficha respetan la tabla 8.3 del Documento 0 para cada tipo (FON sin H1; DER y MON sin H4; ALT sin H1–H2).

| Horizonte | Métodos principales | Advertencia |
|---|---|---|
| H1 días | VOL-GARCH-001, FX-VOL-001, DER-OPT-001, DER-VRP-001, DER-SKEW-001, DER-TERM-001, DER-ROLL-001, TCV-VIXTS-001, TCV-SLOPE-001, MON-EXP-001 (limitado), MON-YLD-001 (limitado), IDX-REB-001 (limitado), CHR-FUND-001, CHR-FLOW-001, FX-CARRY-001, FX-MOM-001, CMD-CURVE-001, RISK-VAR-001, SCN-H-001 (bandas por volatilidad) | Menor fiabilidad esperada; probabilidades solo con certificado (R13) |
| H2 semanas | ACC-MOM-001, FX-TREND-001, REG-HMM-001, FIR-CARRY-001, FIR-SPREAD-001, CMD-INV-001, IDX-REL-001 (momentum relativo), IDX-CONC-001, IDX-REB-001, FON-FLOW-001 (limitado), FON-LEV-001 (limitado), DER-VRP-001, DER-SKEW-001, DER-ROLL-001, MON-YLD-001, MON-FIX-001, MON-REAL-001, TCV-SLOPE-001, TCV-BEI-001, TCV-CDS-001, TCV-VIXTS-001, ML-PRED-001, SCN-H-001 | Valoración solo como contexto |
| H3 meses | FIR-CURVE-001, FIR-CARRY-001, ACC-FACT-001, IDX-REL-001, IDX-CONC-001, FON-DISC-001, FON-FLOW-001, FON-TD-001, FON-LEV-001, DER-VRP-001, DER-TERM-001, DER-ROLL-001 (≤ 12 meses), MON-FIX-001, MON-REAL-001, MON-EXP-001, TCV-TP-001, TCV-SLOPE-001, TCV-BEI-001, TCV-CDS-001, REI-NAV-001, REI-CAP-001, REI-FFO-001, CHR-ONCHAIN-001, CMD-RETDEC-001, ALT-DESMOOTH-001, SCN-H-001 | Regímenes y catalizadores dominan |
| H4 años | TEM-DIFF-001, ACC-VAL-001, ACC-ERP-001, IDX-ERP-001, IDX-REL-001, FON-DISC-001, FON-TD-001, FX-PPA-001, FX-BEER-001, CMD-REAL-001, FIR-CRED-001, TCV-TP-001 (limitado), TCV-BEI-001 (limitado), TCV-CDS-001 (limitado), PRV-PME-001, PRV-CF-001, ALT-AUC-001, SCN-H-001 (bloques de rentabilidad) | Valoración informativa pero ruidosa; pocas observaciones independientes |

Evaluación transversal de cualquier horizonte: FC-EVAL-001, FC-CAL-001, BT-DSR-001, BT-PBO-001, BT-VAR-001.

## 6. Fichas heredadas de la línea V3.0

### FX-TREND-001 · Detección y medición de tendencia (Mann-Kendall + Theil-Sen)

**Identificación.** v1.1 · VIGENTE · MC-02 · Mapa: áreas 7, 6.
**Perfiles y horizontes.** TRANSVERSAL · H2–H4 (H1 no informativo con datos diarios).
**Propósito.** ¿Tiene la serie una tendencia monótona persistente y cuál es su pendiente?
**Método.** (i) Validación de frecuencia y huecos. (ii) Mann-Kendall con corrección por autocorrelación (Hamed y Rao) por defecto. (iii) Pendiente de Theil-Sen con IC. (iv) Aceleración opcional (pendientes de las dos mitades).
**Entradas mínimas.** Serie con frecuencia declarada; ≥ 10 observaciones (≥ 20 recomendadas).
**Parámetros.** ventana (serie completa); corregir_autocorrelacion (true); nivel (0,05; 0,01–0,10); aceleracion (false).
**Salidas.** TABLA: S, Z, p-valor, pendiente de Sen (unidades de la serie por periodo) con IC, dirección, aceleración. ESTADISTICA.
**Supuestos y limitaciones.** Tendencia monótona en la ventana; sensibilidad a la ventana obligatoria en PLAN_STD; no distingue tendencia de ciclo largo.
**Tolerancias y semilla.** 1e-6 en la pendiente · null.
**Verificación.** Doble pasada; segunda vía: pendiente MCO; serie estrictamente creciente de n puntos da S = n(n − 1)/2.
**Referencia ingenua.** RI-PA (pendiente nula).
**Aclaración y rechazo.** Aclaración si falta la frecuencia; rechazo con < 10 observaciones.
**Referencias.** Mann (1945), *Econometrica*; Kendall (1975), *Rank Correlation Methods*; Sen (1968), *JASA*; Hamed y Rao (1998), *Journal of Hydrology* · TM-02.
**Prioridad y madurez.** P0 · IMPLEMENTADO (ejecutor V1.0, pruebas unitarias).

### FX-BRK-001 · Rupturas estructurales

**Identificación.** v1.1 · VIGENTE · MC-02 · Mapa: áreas 10, 7.
**Perfiles y horizontes.** TRANSVERSAL · H2–H4.
**Propósito.** ¿Cambia la serie de nivel, pendiente o varianza, y cuándo?
**Método.** CUSUM como primera vía; Bai-Perron con número máximo de rupturas y criterio BIC; clasificación del tipo de cambio; fechas con IC.
**Entradas mínimas.** ≥ 30 observaciones para una ruptura; ≥ 50 para dos o más.
**Parámetros.** max_rupturas (1; 1–5); tipo_cambio (auto); nivel (0,05); recorte (15 %).
**Salidas.** TABLA: rupturas, fechas e IC, tipo, estadísticos. ESTADISTICA.
**Supuestos y limitaciones.** Homocedasticidad dentro de segmentos (salvo ruptura de varianza); una revisión de la fuente puede imitar una ruptura; la ruptura no identifica su causa.
**Tolerancias y semilla.** 1e-6 en estadísticos; fechas exactas · null.
**Verificación.** Doble pasada; segunda vía: CUSUM frente a Bai-Perron.
**Referencia ingenua.** Modelo sin ruptura.
**Aclaración y rechazo.** Rechazo por debajo del mínimo.
**Referencias.** Page (1954), *Biometrika*; Bai y Perron (1998), *Econometrica*; Bai y Perron (2003), *Journal of Applied Econometrics* · TM-02, TM-03.
**Prioridad y madurez.** P0 · IMPLEMENTADO (ejecutor, casos de control registrados (T-112)).

### FX-STL-001 · Descomposición tendencia-ciclo-estacionalidad

**Identificación.** v1.1 · VIGENTE · MC-02 · Mapa: área 6.
**Perfiles y horizontes.** TRANSVERSAL (especialmente PERF-CMD, PERF-REI) · H2–H4.
**Propósito.** Separar tendencia, estacionalidad y resto.
**Método.** Esquema aditivo o multiplicativo; STL robusto (LOESS) o medias móviles; diagnóstico de estabilidad estacional.
**Entradas mínimas.** ≥ 2 ciclos estacionales completos (≥ 3 recomendados).
**Parámetros.** esquema (auto); periodo (según frecuencia); robusto (true).
**Salidas.** SERIE: tendencia, estacional, resto y ajustada, en unidades de origen. ESTADISTICA.
**Supuestos y limitaciones.** Descomposición no única; inestable en series cortas.
**Tolerancias y semilla.** 1e-6 · null.
**Verificación.** Identidad tendencia + estacional + resto = serie; caso sintético con estacionalidad conocida.
**Referencia ingenua.** RI-EST.
**Aclaración y rechazo.** Rechazo con < 2 ciclos.
**Referencias.** Cleveland, Cleveland, McRae y Terpenning (1990), *Journal of Official Statistics* · TM-02.
**Prioridad y madurez.** P0 · IMPLEMENTADO (ejecutor, casos de control registrados (T-112)).

### FX-VOL-001 · Volatilidad realizada e implícita y su brecha

**Identificación.** v1.1 · VIGENTE · MC-02 · Mapa: áreas 6, 33, 49.
**Perfiles y horizontes.** TRANSVERSAL · H1–H3.
**Propósito.** Medir la volatilidad realizada y, si se aporta, su brecha con la implícita.
**Método.** Desviación típica de rendimientos logarítmicos en ventana, anualizada (252; 365 en CRI); ventana móvil opcional; brecha implícita − realizada con horizontes alineados.
**Entradas mínimas.** ≥ 30 observaciones; implícita con fuente, horizonte y convención.
**Parámetros.** ventana (20; 10–260); convencion_anual (252); ventana_movil (false).
**Salidas.** VALOR o SERIE: volatilidad anualizada (%), brecha (puntos de volatilidad). ESTADISTICA.
**Supuestos y limitaciones.** La implícita no es previsión de la realizada (incluye prima de varianza); baja frecuencia subestima colas.
**Tolerancias y semilla.** 1e-8 · null.
**Verificación.** Coherencia de anualización; segunda vía: ventana alternativa.
**Referencia ingenua.** RI-EWMA.
**Aclaración y rechazo.** Rechazo con < 30 observaciones.
**Referencias.** Andersen, Bollerslev, Diebold y Labys (2003), *Econometrica*; Poon y Granger (2003), *JEL* · TM-03.
**Prioridad y madurez.** P0 · IMPLEMENTADO (ejecutor V1.0, pruebas unitarias).

### FX-REGIME-001 · Regímenes univariantes (Markov switching)

**Identificación.** v1.1 · VIGENTE · MC-02 · Mapa: área 10.
**Perfiles y horizontes.** TRANSVERSAL · H2–H4.
**Propósito.** Probabilidad de estar en cada régimen de media o varianza.
**Método.** Hamilton con n estados (varianzas distintas por defecto); máxima verosimilitud; probabilidades **filtradas** (las únicas utilizables en tiempo real) y suavizadas (solo descriptivas); duraciones esperadas.
**Entradas mínimas.** ≥ 100 observaciones para 2 estados (≥ 200 recomendadas).
**Parámetros.** n_estados (2; 2–3); varianzas_distintas (true); medias_distintas (false); umbral (0,5; 0,3–0,7).
**Salidas.** SERIE de probabilidades; TABLA de parámetros, matriz de transición y duraciones. ESTADISTICA.
**Supuestos y limitaciones.** Número de regímenes declarado (BIC); regímenes en series cortas pueden ser artefactos; usar probabilidades suavizadas en una previsión es fuga.
**Tolerancias y semilla.** 1e-6 · entero del plan si hay arranques aleatorios.
**Verificación.** Probabilidades suman 1; segunda vía: otra semilla.
**Referencia ingenua.** Un solo régimen.
**Aclaración y rechazo.** Rechazo con < 100 observaciones.
**Referencias.** Hamilton (1989), *Econometrica*; Kim y Nelson (1999), *State-Space Models with Regime Switching* · TM-03.
**Prioridad y madurez.** P0 · IMPLEMENTADO (ejecutor, casos de control registrados (T-112)).

### FX-PPA-001 · Desviación de paridad de poder adquisitivo relativa

**Identificación.** v1.1 · VIGENTE · MC-03 · Mapa: áreas 51, 19.
**Perfiles y horizontes.** PERF-FX · H4 (H3 limitado).
**Propósito.** Cuánto se desvía el tipo de cambio de su senda de PPA relativa.
**Método.** Inflaciones acumuladas con vintages; senda = cambio base × razón de índices de precios; desviación = log-diferencia (%); tipo real q = s + p* − p; vida media de la desviación por AR(1).
**Entradas mínimas.** Tipo de cambio y dos índices de precios con base y vintage; ≥ 24 meses (≥ 20 años para la vida media).
**Parámetros.** ventana (completa); base (primer periodo común o media de largo plazo); suavizado (null).
**Salidas.** SERIE de desviación (%); VALOR final; vida media (años). ESTADISTICA.
**Supuestos y limitaciones.** Ancla de largo plazo (vida media habitual 3–5 años); no corrige Balassa-Samuelson; no es previsión ni valor objetivo.
**Tolerancias y semilla.** 1e-8 · null.
**Verificación.** Inflación constante igual ⇒ desviación nula.
**Referencia ingenua.** RI-PA del tipo de cambio.
**Aclaración y rechazo.** Rechazo con canastas o periodicidades incompatibles.
**Referencias.** Rogoff (1996), *JEL*; Taylor y Taylor (2004), «The Purchasing Power Parity Debate», *JEP* · TM-13.
**Prioridad y madurez.** P1 · IMPLEMENTADO (ejecutor, casos de control registrados (T-112)).

### FX-CARRY-001 · Diferencial de tipos y carry

**Identificación.** v1.1 · VIGENTE · MC-03 · Mapa: áreas 51, 19.
**Perfiles y horizontes.** PERF-FX, PERF-FIR · H1–H3.
**Propósito.** Diferencial de tipos y rentabilidad de carry con su descomposición.
**Método.** Diferencial con base declarada (tipo a 3 meses por defecto); carry = diferencial ajustado por variación del cambio o por el *forward*; comprobación de paridad cubierta; residuo de paridad descubierta como estimación.
**Entradas mínimas.** Dos series de tipos alineadas; tipo de cambio; *forward* opcional.
**Parámetros.** base_tipos (3M); periodicidad (mensual); incluir_forward (false).
**Salidas.** SERIE de diferencial y carry (% anual); TABLA de descomposición. DETERMINISTA (aritmética); ESTADISTICA (prima estimada).
**Supuestos y limitaciones.** La paridad descubierta no se cumple empíricamente; el carry tiene asimetría negativa (colapsos).
**Tolerancias y semilla.** 1e-8 · null.
**Verificación.** Carry + variación cambiaria = rentabilidad total.
**Referencia ingenua.** RI-PA del tipo de cambio (rentabilidad = diferencial).
**Aclaración y rechazo.** Aclaración si la base de tipos es ambigua.
**Referencias.** Fama (1984), *JFE*; Lustig y Verdelhan (2007), *AER*; Burnside, Eichenbaum y Rebelo (2011), *Annual Review of Financial Economics* · TM-13.
**Prioridad y madurez.** P1 · IMPLEMENTADO (ejecutor V1.0, pruebas unitarias).

### FX-COINT-001 · Cointegración y corrección de errores

**Identificación.** v1.1 · VIGENTE · MC-03 · Mapa: área 8.
**Perfiles y horizontes.** TRANSVERSAL · H3–H4.
**Propósito.** ¿Se mueven las series juntas a largo plazo? Vector y velocidad de ajuste.
**Método.** Orden de integración (ADF con regla de rezagos); Johansen (por defecto) o Engle-Granger; vector normalizado; MCE con velocidad de ajuste y vida media.
**Entradas mínimas.** ≥ 50 observaciones comunes.
**Parámetros.** metodo (Johansen); max_rezagos (AIC); nivel (0,05).
**Salidas.** TABLA de contrastes, vector, velocidad; SERIE de desviación de equilibrio. ESTADISTICA.
**Supuestos y limitaciones.** Estabilidad del vector obligatoria en PLAN_STD; baja potencia en muestras cortas; no es causalidad.
**Tolerancias y semilla.** 1e-6 · null.
**Verificación.** Residuos de media nula; segunda vía: Engle-Granger.
**Referencia ingenua.** RI-PA (sin relación).
**Aclaración y rechazo.** Rechazo con < 50 observaciones.
**Referencias.** Engle y Granger (1987), *Econometrica*; Johansen (1991), *Econometrica* · TM-04.
**Prioridad y madurez.** P1 · IMPLEMENTADO (ejecutor, casos de control registrados (T-112)).

### FX-CORR-001 · Correlación dinámica y dependencia de cola

**Identificación.** v1.1 · VIGENTE · MC-03 · Mapa: área 18.
**Perfiles y horizontes.** TRANSVERSAL · H1–H4.
**Propósito.** Dependencia entre dos series: móvil, por régimen y en colas.
**Método.** Pearson móvil; Spearman de contraste; coeficientes de cola empíricos; por régimen con probabilidades de REG-HMM-001 o FX-REGIME-001; DCC opcional.
**Entradas mínimas.** ≥ 60 observaciones comunes.
**Parámetros.** ventana (60); cola_cuantil (0,05; 0,01–0,10); usar_regimenes (false).
**Salidas.** SERIE de correlaciones; TABLA global, por régimen y colas. ESTADISTICA.
**Supuestos y limitaciones.** Correlaciones inestables; baja correlación lineal no implica independencia de cola.
**Tolerancias y semilla.** 1e-8 · null.
**Verificación.** Simetría y diagonal unitaria; caso normal bivariante conocido.
**Referencia ingenua.** Correlación histórica de ventana larga.
**Aclaración y rechazo.** Rechazo con < 60 observaciones.
**Referencias.** Longin y Solnik (2001), *Journal of Finance*; Engle (2002), *JBES* · TM-07, TM-08.
**Prioridad y madurez.** P0 · IMPLEMENTADO (ejecutor V1.0, pruebas unitarias).

### ST-DESC-001 · Estadística descriptiva y momentos

**Identificación.** v1.1 · VIGENTE · MC-01 · Mapa: áreas 4, 33.
**Perfiles y horizontes.** TRANSVERSAL · no aplica.
**Propósito.** Localización, dispersión, forma y cuantiles con variantes robustas.
**Método.** Media, mediana, recortada; desviación (n − 1), IQR, MAD; asimetría y curtosis en exceso; cuantiles tipo 7; atípicos a 3 desviaciones robustas (marcado, no eliminación).
**Entradas mínimas.** ≥ 5 observaciones.
**Parámetros.** cuantiles (0,05/0,25/0,5/0,75/0,95); pesos (null); por_grupos (null).
**Salidas.** TABLA con unidades. DETERMINISTA.
**Supuestos y limitaciones.** Momentos superiores inestables con n pequeño.
**Tolerancias y semilla.** 1e-10 · null.
**Verificación.** Cuantiles monótonos; media ponderada coherente.
**Referencia ingenua.** RI-NA.
**Aclaración y rechazo.** Rechazo con < 5 observaciones o sin unidades.
**Referencias.** Tukey (1977), *Exploratory Data Analysis*; Hyndman y Fan (1996), *The American Statistician* · TM-01.
**Prioridad y madurez.** P0 · IMPLEMENTADO (ejecutor V1.0, pruebas unitarias).

### ST-INF-001 · Contrastes, intervalos y comparaciones múltiples

**Identificación.** v1.1 · VIGENTE · MC-01 · Mapa: área 5.
**Perfiles y horizontes.** TRANSVERSAL · no aplica.
**Propósito.** Contrastes de hipótesis e IC con potencia y corrección múltiple.
**Método.** Contraste declarado (paramétrico o no); supuestos comprobados; estadístico, p-valor, tamaño de efecto; Holm o Benjamini-Hochberg si m > 1; potencia y n mínimo bajo petición.
**Entradas mínimas.** Muestras o estadísticos suficientes.
**Parámetros.** tipo_contraste; alternativa (bilateral); nivel (0,05); correccion (auto si m > 1).
**Salidas.** TABLA: estadístico, p-valor, IC, efecto, corrección. ESTADISTICA.
**Supuestos y limitaciones.** Significación no es relevancia; el p-valor no es P(H₀).
**Tolerancias y semilla.** 1e-8 · null salvo remuestreo.
**Verificación.** IC coherente con p-valor; casos de p-valor conocido.
**Referencia ingenua.** RI-NA.
**Aclaración y rechazo.** Rechazo si los datos no sostienen el contraste.
**Referencias.** Lehmann y Romano (2005), *Testing Statistical Hypotheses*; Benjamini y Hochberg (1995), *JRSS B*; Holm (1979), *Scandinavian Journal of Statistics* · TM-01.
**Prioridad y madurez.** P0 · IMPLEMENTADO (ejecutor, casos de control registrados (T-112)).

### FIN-CAGR-001 · Crecimiento, anualización y nominal/real

**Identificación.** v1.1 · VIGENTE · MC-01 · Mapa: área 2.
**Perfiles y horizontes.** TRANSVERSAL · no aplica.
**Propósito.** Tasas acumuladas, anualizadas y deflactadas, con efecto base.
**Método.** CAGR = (V_fin/V_ini)^{1/años} − 1; real = (1 + nominal)/(1 + inflación) − 1; descomposición precio/volumen; efecto base.
**Entradas mínimas.** Serie con unidad, periodicidad y moneda; deflactor si se pide real.
**Parámetros.** ventana (completa); frecuencia (anual); deflactar (false).
**Salidas.** TABLA (%). DETERMINISTA.
**Supuestos y limitaciones.** El CAGR oculta la trayectoria; no extrapola.
**Tolerancias y semilla.** 1e-10 · null.
**Verificación.** Capitalización de tasas parciales = acumulado; de 100 a 200 en 10 años = 7,177 %.
**Referencia ingenua.** RI-NA.
**Aclaración y rechazo.** Rechazo con bases incompatibles.
**Referencias.** Bodie, Kane y Marcus (2021), *Investments*, 12.ª ed. · TM-01.
**Prioridad y madurez.** P0 · IMPLEMENTADO (ejecutor V1.0, pruebas unitarias).

### BIB-MET-001 · Bibliometría aplicada a fuentes

**Identificación.** v1.1 · VIGENTE · MC-01 · Mapa: área 28.
**Perfiles y horizontes.** TRANSVERSAL · no aplica.
**Propósito.** Indicadores de volumen, cobertura, concentración y duplicados de corpus de referencias (F7–F9).
**Método.** Conteos por periodo y temática; crecimiento (FIN-CAGR-001); HHI de concentración por fuente; duplicados por hash + título normalizado; precisión/exhaustividad con conjunto de referencia.
**Entradas mínimas.** Conjunto de fichas con fecha, temática y fuente.
**Parámetros.** granularidad (mensual); categorias (todas).
**Salidas.** TABLA. DETERMINISTA.
**Supuestos y limitaciones.** Describe el corpus registrado, no la literatura; citas no son calidad. Solicitantes por CT-09: Orquestador técnico (paquetes CT-21) y Evaluador; los agentes de conocimiento no son clientes del CT-09.
**Tolerancias y semilla.** Conteos exactos · null.
**Verificación.** Totales por categoría suman el total.
**Referencia ingenua.** RI-NA.
**Aclaración y rechazo.** Rechazo con conjunto vacío o corrupto.
**Referencias.** Moed (2005), *Citation Analysis in Research Evaluation* · TM-14.
**Prioridad y madurez.** P1 · IMPLEMENTADO (ejecutor, casos de control registrados (T-112)).

### SIM-MC-001 · Simulación Monte Carlo de trayectorias

**Identificación.** v1.1 · VIGENTE · MC-05 · Mapa: área 14.
**Perfiles y horizontes.** TRANSVERSAL · H1–H4.
**Propósito.** Distribución de resultados bajo una dinámica declarada.
**Método.** Dinámica del catálogo (paseo aleatorio con deriva, GARCH de VOL-GARCH-001, bootstrap filtrado, saltos); semilla y generador; reducción de varianza (antitéticas); cuantiles, probabilidades de umbral; error estándar de Monte Carlo.
**Entradas mínimas.** Dinámica y parámetros declarados.
**Parámetros.** n_trayectorias (10 000; 1 000–1 000 000); horizonte; cuantiles (0,05/0,5/0,95); semilla; reduccion_varianza (antitéticas).
**Salidas.** DISTRIBUCION con unidades; TABLA de convergencia. ESTADISTICA.
**Supuestos y limitaciones.** Condicional a la dinámica: no corrige un modelo mal especificado.
**Tolerancias y semilla.** 1e-6 con la misma semilla · obligatoria.
**Verificación.** Doble ejecución con la misma semilla; casos de solución analítica.
**Referencia ingenua.** RI-CLI (bootstrap simple de la historia).
**Aclaración y rechazo.** Rechazo sin semilla o sin dinámica.
**Referencias.** Glasserman (2004), *Monte Carlo Methods in Financial Engineering* · TM-09.
**Prioridad y madurez.** P0 · IMPLEMENTADO (ejecutor, casos de control registrados (T-112)).

### RISK-VAR-001 · VaR y Expected Shortfall

**Identificación.** v1.1 · VIGENTE · MC-07 · Mapa: área 25.
**Perfiles y horizontes.** TRANSVERSAL · H1–H3.
**Propósito.** VaR y ES con método, horizonte y nivel declarados.
**Método.** Histórico, paramétrico (normal, t, Cornish-Fisher), histórico filtrado o EVT-POT según la tabla de decisión de MC-07; ES al mismo nivel; advertencias obligatorias.
**Entradas mínimas.** ≥ 250 observaciones para histórico (≥ 500 recomendadas); EVT ≥ 50 excedencias; o distribución de MC-05 con semilla.
**Parámetros.** nivel (0,975; 0,90–0,99); horizonte; metodo (historico); moneda.
**Salidas.** VALOR: VaR y ES (fracción del valor y moneda), con horizonte y nivel. ESTADISTICA.
**Supuestos y limitaciones.** El VaR no es la pérdida máxima ni describe la cola; √h solo con iid.
**Tolerancias y semilla.** 1e-6 · null o del plan.
**Verificación.** ES ≥ VaR; cuantiles monótonos; segunda vía histórico frente a paramétrico.
**Referencia ingenua.** VaR normal con volatilidad histórica (para backtesting con BT-VAR-001).
**Aclaración y rechazo.** Rechazo de nivel 99 % empírico con < 500 observaciones.
**Referencias.** Jorion (2007); McNeil, Frey y Embrechts (2015); Artzner et al. (1999) · TM-08.
**Prioridad y madurez.** P0 · IMPLEMENTADO (ejecutor, casos de control registrados (T-112)).

### ML-CAL-001 · Evaluación interna de modelos predictivos

**Identificación.** v1.1 · VIGENTE · MC-06 · Mapa: áreas 16, 17.
**Perfiles y horizontes.** TRANSVERSAL · H1–H4.
**Propósito.** Evaluar un modelo en desarrollo con validación temporal, métricas y comparación con la referencia. La certificación y las pruebas formales para el Evaluador usan FC-EVAL-001 y FC-CAL-001.
**Método.** Walk-forward (expansivo por defecto) con purga y embargo; MAE/RMSE/MASE, Brier, log-score, pinball; R²_OOS; cobertura de intervalos; mejora frente a referencia con IC por bootstrap de bloques; análisis por régimen.
**Entradas mínimas.** Predicciones y realizaciones alineadas, ≥ 30 por horizonte.
**Parámetros.** esquema (walk_forward_expansivo); horizontes; metricas (todas las aplicables).
**Salidas.** TABLA por horizonte y esquema. ESTADISTICA.
**Supuestos y limitaciones.** La evaluación retrospectiva no certifica el futuro; número de ensayos obligatorio.
**Tolerancias y semilla.** 1e-8 · entero del plan si hay bootstrap.
**Verificación.** Métricas recomputadas; particiones sin solape.
**Referencia ingenua.** RI-PA, RI-TB o RI-MH según el objetivo.
**Aclaración y rechazo.** Rechazo si predicciones y realizaciones no alinean.
**Referencias.** Hyndman y Athanasopoulos (2021); Campbell y Thompson (2008); López de Prado (2018) · TM-10, TM-11.
**Prioridad y madurez.** P0 · IMPLEMENTADO (ejecutor, casos de control registrados (T-112)).

### AUD-REX-001 · Re-ejecución independiente (CT-10)

**Identificación.** v1.1 · VIGENTE · MC-08 · Mapa: áreas 31, 41, 42.
**Perfiles y horizontes.** TRANSVERSAL · no aplica.
**Propósito.** Reproducir en aislamiento un cálculo registrado y clasificar discrepancias.
**Método.** Artefacto completo y tolerancia previa; reconstrucción con la versión de método y ficha del artefacto; verificación del recálculo; comparación; categorías DATOS_DISTINTOS, CONVENCION_DISTINTA, SEMILLA_DISTINTA, ERROR_IMPLEMENTACION, ERROR_REDONDEO, SIN_CAUSA_CLARA; materialidad frente a umbrales del bloque.
**Entradas mínimas.** Artefacto completo (método, versión, ficha, entradas efectivas con hash, transformaciones, parámetros, semilla, redondeo) y tolerancia.
**Parámetros.** segunda_via (false); alcance (el declarado).
**Salidas.** Informe CT-10: `coincide` (SI, NO, DENTRO_DE_TOLERANCIA), diferencias, diagnóstico, artefacto propio. Clase de cifra la del cálculo re-ejecutado.
**Supuestos y limitaciones.** Artefacto incompleto ⇒ re-ejecución imposible; no se reconstruye por inferencia.
**Tolerancias y semilla.** Las de la ficha original · la del artefacto original.
**Verificación.** Doble pasada del recálculo; casos de control periódicos.
**Referencia ingenua.** RI-NA.
**Aclaración y rechazo.** Rechazo sin artefacto, tolerancia o motivo; resultado original presente en el despacho ⇒ incidencia.
**Referencias.** Peng (2011), *Science*; National Academies (2019), *Reproducibility and Replicability in Science* · TM-14.
**Prioridad y madurez.** P0 · IMPLEMENTADO (ejecutor, casos de control registrados (T-112)).

## 7. Fichas nuevas — núcleo transversal

### SCORE-RK-001 · Puntuaciones T/E/M/P/A y clave RK (idéntico a HT-03)

**Identificación.** v1.0 · VIGENTE · MC-01 · Mapa: área 37.
**Perfiles y horizontes.** TRANSVERSAL · no aplica.
**Propósito.** Reconstruir de forma independiente las puntuaciones de HT-03 para la validación G3 y PS8, y para re-ejecuciones CT-10. **HT-03 es la herramienta canónica**; esta ficha replica exactamente su regla y cualquier diferencia con HT-03 es una discrepancia.
**Método.** (i) Cada dimensión en {0, 10, …, 100}; «NA» redistribuye su peso proporcionalmente entre las demás (anotado); «NE» puntúa 0; más de dos NA/NE en una puntuación ⇒ rechazo. (ii) Pesos vigentes de F10 (iniciales del Documento 0, 9.1): T = magnitud 20, alcance 15, velocidad 15, duración 10, difusión 10, posición en la cadena de valor 10, capacidad transformadora 10, claridad causal 10; E = raíces 25, cobertura 15, calidad metodológica 15, trazabilidad 15, actualidad 10, discrepancias resueltas 10, objeciones CT-13 respondidas 10; M = adopción 20, escalado 15, indicadores 15, persistencia 15, estabilidad de impulsores 15, hitos 20; P = T 40, novedad 20, incertidumbre reducible 20, coste-eficiencia 20; A = asimetría 30, valoración del ámbito 25, catalizadores 15, momento 15, profundidad e invertibilidad del universo 15 (A no puntúa instrumentos concretos ni sus costes: frontera con el Bloque B). (iii) Tope por saturación narrativa: si la marca está activa, la dimensión «valoración del ámbito» de A se limita a 40 antes de ponderar. (iv) Total = Σ wᵢ·dᵢ/Σ wᵢ, redondeado al múltiplo de 5 más próximo (exactamente a mitad: hacia arriba, salvo que HT-03 declare otra regla). (v) RK = 0,45·A + 0,35·E + 0,20·T (pesos vigentes de F10) sobre los totales ya redondeados; T = NA en oportunidades tácticas ⇒ RK = (0,45·A + 0,35·E)/0,80. (vi) Banderas: banda marginal (total a ≤ 5 puntos de un umbral: E 60, A 55, T 50, A 65 si T = NA, GC2 50), cambio ≥ 15 puntos frente al ciclo anterior, empate de RK a ±2.
**Entradas mínimas.** Dimensiones con valor, NA o NE; pesos y umbrales vigentes (versión de F10); marca de saturación; puntuaciones del ciclo anterior (para la bandera de cambio).
**Parámetros.** version_pesos (F10 vigente); regla_mitad (HT-03).
**Salidas.** TABLA: T, E, M, P, A (0–100, múltiplos de 5), RK (entero; redondeo con empates hacia abajo, igual que HT-03), desglose ponderado, redistribuciones NA, banderas. DETERMINISTA.
**Supuestos y limitaciones.** Las dimensiones son juicios anclados de los agentes; la ficha solo garantiza la aritmética. RK ordena, no es probabilidad ni rentabilidad.
**Tolerancias y semilla.** Igualdad exacta con HT-03 · null.
**Verificación.** Doble pasada; identidad con HT-03 en todos los casos de control de `10_Herramientas`.
**Referencia ingenua.** RI-NA.
**Aclaración y rechazo.** Rechazo con > 2 NA/NE o dimensión fuera de {0, 10, …, 100}; aclaración si la versión de pesos no coincide con F10.
**Referencias.** Documento 0, 9.1–9.2 y Anexo A; Saisana, Saltelli y Tarantola (2005), «Uncertainty and Sensitivity Analysis Techniques as Tools for the Quality Assessment of Composite Indicators», *JRSS A*; OECD/JRC (2008), *Handbook on Constructing Composite Indicators* · TM-01.
**Prioridad y madurez.** P0 · IMPLEMENTADO (ejecutor V1.0, pruebas unitarias).

### FC-EVAL-001 · Evaluación de pronósticos

**Identificación.** v1.0 · VIGENTE · MC-10 · Mapa: áreas 58, 60, 63.
**Perfiles y horizontes.** TRANSVERSAL · H1–H4.
**Propósito.** ¿Aciertan los pronósticos de una celda y baten a la referencia ingenua con significación?
**Método.** (i) Control de conocibilidad y resolución con el criterio congelado de F4 (NO_RESOLUBLE contado aparte). (ii) n efectivo con solapamiento. (iii) Brier y descomposición de Murphy; log-score (p recortado a [0,01; 0,99]); CRPS o pinball para distribuciones y cuantiles; puntuación de intervalo. (iv) Acierto direccional: binomial frente a tasa base y Pesaran-Timmermann. (v) BSS frente a climatología conocida en t, con IC 90 % por bootstrap estacionario por fechas. (vi) DM con corrección HLN frente a la referencia (Clark-West si es anidada; Giacomini-White si se pide habilidad condicional). (vii) Corrección múltiple (Holm o BH) si se evalúan varias celdas. (viii) Efecto mínimo detectable.
**Entradas mínimas.** PRG- resueltos de la celda (≥ 30 para calibrar; ≥ 50 para certificar, Anexo A), realizaciones con fuente y vintage, referencia.
**Parámetros.** perdida (brier); referencia (RI-CLI/RI-TB/RI-PA según objetivo); B (2 000; 1 000–10 000); bloque (max(h, T^{1/3})); nivel_ic (0,90); significacion (0,10 unilateral para 12.2, salvo F10); mapeo_bandas (F10; por defecto 0,25/0,50/0,65).
**Salidas.** TABLA: BS, FIA, RES, INC, LS, CRPS (unidades de la variable), acierto (%), p-valores, BSS e IC, estadístico DM*, n nominal/efectivo/no resolubles, efecto detectable. ESTADISTICA.
**Supuestos y limitaciones.** Muestras de 30–50 solo detectan ventajas grandes; «no significativo» no equivale a «sin ventaja».
**Tolerancias y semilla.** 1e-8 en métricas; 1e-6 en IC con la misma semilla · entero del plan.
**Verificación.** Identidad de Murphy con probabilidades discretas; recuentos; segunda vía: otra longitud de bloque.
**Referencia ingenua.** La de la celda (obligatoria por definición).
**Aclaración y rechazo.** Rechazo si hay fuga sistemática o falta el criterio de resolución.
**Referencias.** Gneiting y Raftery (2007); Murphy (1973); Diebold y Mariano (1995); Harvey, Leybourne y Newbold (1997); Clark y West (2007); Giacomini y White (2006); Pesaran y Timmermann (1992); Politis y Romano (1994) · TM-11.
**Prioridad y madurez.** P0 · IMPLEMENTADO (ejecutor V1.0, pruebas unitarias).

### FC-CAL-001 · Calibración y fiabilidad

**Identificación.** v1.0 · VIGENTE · MC-10 · Mapa: área 59.
**Perfiles y horizontes.** TRANSVERSAL · H1–H4.
**Propósito.** ¿Ocurren los sucesos con la frecuencia que dicen las probabilidades?
**Método.** Curva de fiabilidad (10 tramos de igual anchura si n ≥ 200; 5 por cuantiles si no, ≥ 10 casos por tramo); bandas de consistencia por simulación; ECE y MCE; ECE nulo (media y cuantil 90 bajo calibración perfecta, simulando o* ~ Bernoulli(p)); recalibración logística (a, b) con IC; calibración global; PIT e histograma para distribuciones; cobertura empírica de intervalos con binomial.
**Entradas mínimas.** ≥ 50 pares (p, o) (≥ 100 recomendados); para PIT, ≥ 50 pronósticos de distribución.
**Parámetros.** tramos (auto); simulaciones_nulo (5 000); nivel (0,90).
**Salidas.** TABLA: ECE, MCE, ECE nulo (media, q90), a, b con IC, cobertura (%), p-valores; SERIE: curva de fiabilidad. ESTADISTICA.
**Supuestos y limitaciones.** Con n ≈ 50 el ECE de un pronosticador perfecto ronda 0,12; por eso el Anexo A no usa un umbral fijo: la ficha entrega siempre el percentil 90 del ECE bajo calibración perfecta (`ece_nulo_q90`) y el certificado exige n ≥ 100, ECE ≤ q90 nulo y ECE < 0,15.
**Tolerancias y semilla.** 1e-8 en ECE; 1e-6 en el nulo con misma semilla · entero del plan.
**Verificación.** Pesos de tramos suman 1; caso sintético calibrado.
**Referencia ingenua.** RI-CLI (probabilidad constante igual a la tasa base: perfectamente calibrada y sin resolución).
**Aclaración y rechazo.** Rechazo con < 30 pares.
**Referencias.** Bröcker y Smith (2007); Gneiting, Balabdaoui y Raftery (2007); Dawid (1982), «The Well-Calibrated Bayesian», *JASA*; Naeini, Cooper y Hauskrecht (2015), *AAAI* · TM-11.
**Prioridad y madurez.** P0 · IMPLEMENTADO (ejecutor V1.0, pruebas unitarias).

### BT-DSR-001 · Sharpe probabilístico y Deflated Sharpe

**Identificación.** v1.0 · VIGENTE · MC-10 · Mapa: área 61.
**Perfiles y horizontes.** TRANSVERSAL · H2–H4.
**Propósito.** ¿Es el Sharpe de una señal o estrategia significativo tras descontar los ensayos realizados?
**Método.** SR por periodo; EE de Lo/Mertens con asimetría y curtosis; ajuste de Lo por autocorrelación; PSR(SR*); SR*₀ esperado del máximo de N ensayos; DSR = PSR(SR*₀); MinTRL.
**Entradas mínimas.** Rendimientos netos de costes ≥ 24 meses o 250 sesiones; N ensayos y varianza de sus SR.
**Parámetros.** SR_referencia (0); N (obligatorio); nivel (0,95).
**Salidas.** TABLA: SR anualizado, EE, PSR, SR*₀, DSR (probabilidad), MinTRL (periodos). ESTADISTICA.
**Supuestos y limitaciones.** N ensayos efectivamente independientes (si están correlacionados, N efectivo por agrupación de ML-CLUS-001); rendimientos netos de costes.
**Tolerancias y semilla.** 1e-8 · null.
**Verificación.** PSR(SR) = 0,5; caso normal con SR conocido.
**Referencia ingenua.** SR = 0 y RI-CM.
**Aclaración y rechazo.** Aclaración sin N ensayos.
**Referencias.** Lo (2002); Mertens (2002); Bailey y López de Prado (2012; 2014); Harvey y Liu (2015) · TM-11.
**Prioridad y madurez.** P0 · IMPLEMENTADO (ejecutor, casos de control registrados (T-112)).

### BT-PBO-001 · Probabilidad de sobreajuste del backtest (CSCV)

**Identificación.** v1.0 · VIGENTE · MC-10 · Mapa: área 61.
**Perfiles y horizontes.** TRANSVERSAL · H2–H4.
**Propósito.** ¿Con qué probabilidad la mejor configuración dentro de muestra rinde por debajo de la mediana fuera de muestra?
**Método.** Matriz T × N; S bloques; todas las combinaciones C(S, S/2); mejor configuración dentro de muestra, rango relativo fuera, logit λ; PBO = P(λ ≤ 0); pendiente de degradación dentro→fuera; probabilidad de pérdida fuera de muestra.
**Entradas mínimas.** N ≥ 2 configuraciones (≥ 10 útil); T ≥ 4·S observaciones.
**Parámetros.** S (16; 8–20, par); metrica (Sharpe).
**Salidas.** TABLA: PBO, distribución de λ, pendiente, probabilidad de pérdida. ESTADISTICA.
**Supuestos y limitaciones.** Bloques aproximadamente estacionarios; PBO ≥ 0,5 = sobreajuste probable; 0,2–0,5 sospecha.
**Tolerancias y semilla.** 1e-8 · null (enumeración completa).
**Verificación.** Configuraciones idénticas ⇒ PBO indefinido declarado; caso sintético sin habilidad ⇒ PBO ≈ 0,5.
**Referencia ingenua.** Selección aleatoria de configuración.
**Aclaración y rechazo.** Rechazo con N < 2.
**Referencias.** Bailey, Borwein, López de Prado y Zhu (2017) · TM-11.
**Prioridad y madurez.** P1 · IMPLEMENTADO (ejecutor, casos de control registrados (T-112)).

### BT-VAR-001 · Backtesting de VaR y ES

**Identificación.** v1.0 · VIGENTE · MC-10 · Mapa: área 62.
**Perfiles y horizontes.** TRANSVERSAL · H1–H2.
**Propósito.** ¿Las excedencias del VaR tienen la frecuencia y la independencia correctas?
**Método.** Kupiec LR_uc; Christoffersen LR_ind y LR_cc; semáforo de Basilea (250 días, 99 %); Acerbi-Székely Z₂ para ES.
**Entradas mínimas.** Serie de VaR/ES previstos ex ante y resultados realizados alineados, ≥ 250 observaciones.
**Parámetros.** nivel (el del VaR); significacion (0,05).
**Salidas.** TABLA: excedencias (n, %), LR y p-valores, zona del semáforo, Z₂. ESTADISTICA.
**Supuestos y limitaciones.** VaR solapados (h > 1) inducen dependencia: usar observaciones no solapadas o declarar.
**Tolerancias y semilla.** 1e-8 · null.
**Verificación.** 250 observaciones, 99 %, 5 excedencias ⇒ LR_uc ≈ 1,96.
**Referencia ingenua.** VaR normal con volatilidad histórica.
**Aclaración y rechazo.** Rechazo con < 250 observaciones (salvo declaración de baja potencia).
**Referencias.** Kupiec (1995); Christoffersen (1998); Acerbi y Székely (2014); BCBS (1996), *Supervisory Framework for the Use of «Backtesting»* · TM-08, TM-11.
**Prioridad y madurez.** P1 · IMPLEMENTADO (ejecutor, casos de control registrados (T-112)).

### SCN-H-001 · Escenarios por horizonte

**Identificación.** v1.0 · VIGENTE · MC-05 · Mapa: áreas 13, 14.
**Perfiles y horizontes.** TRANSVERSAL · H1–H4.
**Propósito.** Escenarios base, favorable y adverso del indicador de seguimiento del ámbito de una opción para cada horizonte aplicable, con bandas y probabilidades de umbral (para CT-12 de Prospectiva).
**Método.** H1–H2: simulación con volatilidad condicional (VOL-GARCH-001) y residuos por bootstrap filtrado. H3: mezcla por régimen (probabilidades filtradas de REG-HMM-001) + escenarios de valoración de MC-09. H4: bloques de rentabilidad esperada (rendimiento corriente + crecimiento + cambio de valoración ± incertidumbre de cada bloque). En todos: cuantiles 10/50/90; base = mediana; favorable/adverso = cuantiles 80/20 o escenarios narrativos cuantificados que entregue Prospectiva; probabilidades de umbrales (solo publicables con certificado R13).
**Entradas mínimas.** H1–H2: ≥ 2 años diarios; H3: régimen y valoración; H4: insumos de los bloques.
**Parámetros.** n_trayectorias (10 000); cuantiles (0,1/0,5/0,9); semilla; umbrales.
**Salidas.** DISTRIBUCION por horizonte (unidades de la variable o %), TABLA de escenarios con condiciones. ESTADISTICA.
**Supuestos y limitaciones.** Distribuciones condicionales al modelo; las bandas de H4 son anchas por construcción.
**Tolerancias y semilla.** 1e-6 con misma semilla · obligatoria.
**Verificación.** Monotonía de cuantiles; doble ejecución; coherencia entre horizontes (bandas crecientes).
**Referencia ingenua.** RI-CLI (bootstrap incondicional) y RI-PA.
**Aclaración y rechazo.** Rechazo sin semilla o en horizonte «No» de 8.3 del Documento 0 para el tipo de activo.
**Referencias.** Glasserman (2004); Christoffersen (2012), *Elements of Financial Risk Management*; Grinold y Kroner (2002), «The Equity Risk Premium», *Investment Insights*; Ilmanen (2011), *Expected Returns* · TM-09, TM-12.
**Prioridad y madurez.** P0 · IMPLEMENTADO (ejecutor, casos de control registrados (T-112)).

### VOL-GARCH-001 · Volatilidad condicional GARCH

**Identificación.** v1.0 · VIGENTE · MC-02 · Mapa: áreas 6, 10.
**Perfiles y horizontes.** TRANSVERSAL · H1–H2 (H3 limitado).
**Propósito.** Volatilidad condicional actual y su estructura temporal prevista.
**Método.** GARCH(1,1) con innovaciones t por defecto: σ²_t = ω + α·ε²_{t−1} + β·σ²_{t−1}; alternativas GJR (asimetría) y EGARCH; máxima verosimilitud; persistencia α + β; vida media ln 0,5/ln(α + β); varianza de largo plazo ω/(1 − α − β); previsión a h pasos con reversión.
**Entradas mínimas.** ≥ 500 rendimientos diarios (250 con limitación).
**Parámetros.** modelo (GARCH-t; GJR, EGARCH); horizonte (1–60 sesiones); anualizacion (252; 365 CRI).
**Salidas.** TABLA: parámetros con EE, persistencia, vida media (sesiones); SERIE: volatilidad condicional y prevista (% anual). ESTADISTICA.
**Supuestos y limitaciones.** α + β ≥ 1 (integrado) ⇒ advertencia; rupturas inflan la persistencia.
**Tolerancias y semilla.** 1e-6 en parámetros · null (valores iniciales fijos).
**Verificación.** Restricciones ω > 0, α, β ≥ 0; segunda vía: EWMA.
**Referencia ingenua.** RI-EWMA, evaluada con pérdida QLIKE.
**Aclaración y rechazo.** Rechazo con < 250 observaciones.
**Referencias.** Engle (1982), *Econometrica*; Bollerslev (1986), *Journal of Econometrics*; Glosten, Jagannathan y Runkle (1993), *Journal of Finance*; Nelson (1991), *Econometrica*; Hansen y Lunde (2005), *Journal of Applied Econometrics*; Patton (2011), *Journal of Econometrics* · TM-03.
**Prioridad y madurez.** P0 · IMPLEMENTADO (ejecutor V1.0, pruebas unitarias).

### REG-HMM-001 · Régimen de clase (HMM multivariante)

**Identificación.** v1.0 · VIGENTE · MC-02 · Mapa: área 10.
**Perfiles y horizontes.** TRANSVERSAL · H2–H3.
**Propósito.** Probabilidad actual de cada régimen del tipo de activo a partir de varias variables (paso 1 del marco común: «régimen del tipo de activo»).
**Método.** Modelo oculto de Markov gaussiano sobre variables estandarizadas con datos de entrenamiento (p. ej., RV e IDX: rendimiento, volatilidad, diferencial HY; RF y TCV: nivel, pendiente, inflación; DER: volatilidad implícita, prima de varianza, sesgo; CRI: rendimiento, volatilidad, financiación); estados por BIC; ≥ 20 arranques con semilla; **probabilidades filtradas** como salida operativa; etiquetado descriptivo por medias.
**Entradas mínimas.** ≥ 260 observaciones semanales o ≥ 120 mensuales.
**Parámetros.** n_estados (BIC; 2–4); covarianza (diagonal; completa); arranques (20).
**Salidas.** TABLA: probabilidades filtradas actuales, matriz de transición, duraciones esperadas, medias por estado; SERIE histórica de probabilidades filtradas. ESTADISTICA.
**Supuestos y limitaciones.** Probabilidades suavizadas solo descriptivas (usarlas en previsión es fuga); regímenes pueden no repetirse.
**Tolerancias y semilla.** 1e-6 en parámetros; etiquetas alineadas por medias · entero del plan.
**Verificación.** Filas de transición suman 1; estabilidad entre semillas.
**Referencia ingenua.** Régimen de la observación anterior; incondicional.
**Aclaración y rechazo.** Rechazo por debajo del mínimo.
**Referencias.** Hamilton (1989); Rabiner (1989), *Proceedings of the IEEE*; Ang y Bekaert (2002), *RFS*; Ang y Timmermann (2012), «Regime Changes and Financial Markets», *Annual Review of Financial Economics* · TM-03.
**Prioridad y madurez.** P1 · IMPLEMENTADO (ejecutor, casos de control registrados (T-112)).

### ML-PRED-001 · Modelo predictivo supervisado con walk-forward

**Identificación.** v1.0 · VIGENTE · MC-06 · Mapa: áreas 16, 17.
**Perfiles y horizontes.** TRANSVERSAL · H1–H3.
**Propósito.** Predicción de dirección, nivel o cuantil con validación temporal y comparación con la referencia.
**Método.** Objetivo con la definición del criterio de resolución; variables conocibles; walk-forward con purga y embargo; regularizado lineal/logístico; ensamble de árboles solo si supera al lineal; calibración Platt o isotónica; registro de ensayos.
**Entradas mínimas.** ≥ 60 observaciones independientes del objetivo (≥ 250 para modelos no lineales).
**Parámetros.** modelo (logistica_L2); rejilla (≤ 20 en PLAN_STD); embargo (≥ h); calibracion (auto).
**Salidas.** TABLA: predicción actual (probabilidad, nivel o cuantiles), métricas fuera de muestra, mejora frente a referencia con IC, ECE, pendiente b, ensayos. ESTADISTICA.
**Supuestos y limitaciones.** Relaciones estables en la ventana; mejora con IC que incluye 0 ⇒ «sin mejora demostrada».
**Tolerancias y semilla.** 1e-6 (deterministas); 1e-3 en métricas si hay paralelismo · entero del plan.
**Verificación.** Particiones sin solape; métricas recomputadas; segunda vía: ventana móvil.
**Referencia ingenua.** RI-TB, RI-PA o RI-MH según objetivo.
**Aclaración y rechazo.** Rechazo con fuga o sin regla de conocibilidad.
**Referencias.** Hastie, Tibshirani y Friedman (2009); Gu, Kelly y Xiu (2020); López de Prado (2018) · TM-10.
**Prioridad y madurez.** P1 · IMPLEMENTADO (ejecutor, casos de control registrados (T-112)).

### ML-CLUS-001 · Clústeres de exposición y apuestas independientes

**Identificación.** v1.0 · VIGENTE · MC-06 · Mapa: áreas 16, 18.
**Perfiles y horizontes.** TRANSVERSAL · no aplica.
**Propósito.** Agrupar opciones con los mismos factores dominantes (regla de diversidad 9.6.3) y contar las apuestas independientes del informe (9.6.6).
**Método.** Rendimientos de los indicadores de seguimiento de los ámbitos (8.4 y 2.4 del Documento 0); correlación (Pearson y Spearman); distancia √(2(1 − ρ)); agrupación jerárquica (enlace medio); corte en ρ = 0,7 por defecto; N_ef = (Σλᵢ)²/Σλᵢ² con autovalores de la matriz de correlación; opcionalmente, cargas en factores macro comunes (tipos, dólar, crecimiento, petróleo) con MC-03.
**Entradas mínimas.** Rendimientos alineados ≥ 1 año diarios o ≥ 3 años semanales (en ALT, series desuavizadas).
**Parámetros.** umbral_rho (0,7; 0,5–0,85); ventana (1 año diario); enlace (medio).
**Salidas.** TABLA: clúster por opción, matriz de correlación, N_ef (número de apuestas), sensibilidad al umbral. ESTADISTICA.
**Supuestos y limitaciones.** Correlaciones inestables y más altas en crisis (declarar N_ef también en una ventana de estrés).
**Tolerancias y semilla.** 1e-8; asignación de clúster exacta · null.
**Verificación.** n opciones independientes ⇒ N_ef ≈ n; segunda vía: Spearman.
**Referencia ingenua.** Agrupación por tipo de activo.
**Aclaración y rechazo.** Rechazo con series no alineables.
**Referencias.** Mantegna (1999), «Hierarchical Structure in Financial Markets», *European Physical Journal B*; Meucci (2009); López de Prado (2016) · TM-07.
**Prioridad y madurez.** P0 · IMPLEMENTADO (ejecutor V1.0, pruebas unitarias).

### RISK-DD-001 · Drawdown, liquidez y escala de riesgo 1–5

**Identificación.** v1.0 · VIGENTE · MC-07 · Mapa: área 25.
**Perfiles y horizontes.** TRANSVERSAL · H2–H4.
**Propósito.** Riesgo de trayectoria y de liquidez del indicador de seguimiento del ámbito de una opción (o de su universo agregado), y su clase de riesgo 1–5 para el paquete (`riesgo_1a5`).
**Método.** MDD, duración y recuperación; Calmar; CDaR; días de liquidación (20 % del volumen medio diario); LVaR; escala 1–5 por volatilidad anualizada (< 5 % ⇒ 1; 5–10 % ⇒ 2; 10–20 % ⇒ 3; 20–35 % ⇒ 4; ≥ 35 % ⇒ 5) con +1 (máximo 5) por colas pesadas (ES 97,5 % a 10 sesiones > 2,5·σ_diaria·√10), liquidez baja (> 5 días) o MDD histórico > 50 %.
**Entradas mínimas.** ≥ 3 años de rendimientos (series suavizadas desuavizadas con ALT-DESMOOTH-001); volumen y horquilla si hay mercado.
**Parámetros.** ventana (toda la disponible; mínimo 3 años); participacion_adv (0,20).
**Salidas.** TABLA: MDD (%), duración (sesiones), Calmar, CDaR, días de liquidación, LVaR, `riesgo_1a5` con motivo. ESTADISTICA.
**Supuestos y limitaciones.** El MDD de muestras cortas subestima el de largo plazo; la escala 1–5 es del catálogo (tipo 3) y el Evaluador puede proponer su recalibración.
**Tolerancias y semilla.** 1e-8; clase de riesgo exacta · null.
**Verificación.** Drawdown ∈ [0, 1]; serie creciente ⇒ MDD = 0.
**Referencia ingenua.** RI-NA (descriptivo).
**Aclaración y rechazo.** Rechazo con < 1 año de datos.
**Referencias.** Magdon-Ismail et al. (2004); Chekhlov, Uryasev y Zabarankin (2005), «Drawdown Measure in Portfolio Optimization», *IJTAF*; Bangia et al. (1999) · TM-08.
**Prioridad y madurez.** P0 · IMPLEMENTADO (ejecutor V1.0, pruebas unitarias).

### DEC-VOI-001 · Valor de la información

**Identificación.** v1.0 · VIGENTE · MC-07 · Mapa: áreas 24, 40.
**Perfiles y horizontes.** TRANSVERSAL · no aplica.
**Propósito.** ¿Puede un cálculo o búsqueda adicional cambiar la decisión (entrar o salir del top-3, cruzar un umbral)? (R15, 7.5 del Documento 0).
**Método.** (i) Decisiones posibles y sus pagos en unidades de puntuación (o de valor esperado). (ii) Distribución plausible de la puntuación decisiva tras el cálculo (rango de sensibilidad de la ficha prevista o histórico del Registro de cálculos). (iii) EVPI y, si hay verosimilitud, EVSI. (iv) Regla simple: si el rango plausible no alcanza ningún umbral (E 60, A 55, T 50, GC2 50; ±5 de banda marginal) ni cambia el orden del top-3 (diferencia de RK > amplitud plausible), VOI = 0.
**Entradas mínimas.** Puntuaciones actuales, umbrales vigentes, rango plausible del efecto del cálculo, coste en UC.
**Parámetros.** umbrales (F10); coste_uc.
**Salidas.** TABLA: VOI (puntos o UC equivalentes), probabilidad de cambio de decisión, recomendación técnica EJECUTAR/NO_EJECUTAR (la decisión es del solicitante). ESTADISTICA.
**Supuestos y limitaciones.** Depende del rango plausible declarado; no sustituye el juicio sobre incertidumbre profunda.
**Tolerancias y semilla.** 1e-8 · null (o del plan si se simula).
**Verificación.** Información perfecta ⇒ VOI = EVPI ≥ EVSI ≥ 0.
**Referencia ingenua.** Ejecutar siempre (coste) frente a no ejecutar nunca.
**Aclaración y rechazo.** Aclaración sin rango plausible.
**Referencias.** Raiffa y Schlaifer (1961); Howard (1966), «Information Value Theory», *IEEE Transactions on Systems Science and Cybernetics* · TM-08.
**Prioridad y madurez.** P1 · IMPLEMENTADO (ejecutor, casos de control registrados (T-112)).

### DER-OPT-001 · Opciones: BSM, binomial, griegas y volatilidad implícita

**Identificación.** v1.0 · VIGENTE · MC-09 · Mapa: área 49.
**Perfiles y horizontes.** PERF-DER (+ PERF-ACC, PERF-IDX, PERF-FIR, PERF-FX, PERF-CMD, PERF-CHR, PERF-TCV como lectura de su subyacente) · H1–H3.
**Propósito.** Precio, griegas y volatilidad implícita de contratos genéricos del subyacente (ATM, deltas estándar, vencimientos estándar); lectura de la superficie (sesgo, estructura temporal, prima de varianza). No compara contratos ni productos concretos (1.6).
**Método.** BSM con dividendo continuo; Black-76 para futuros; CRR para americanas (N = 500, promedio N/N + 1); volatilidad implícita por Newton con respaldo Brent; *risk reversal* 25Δ y *butterfly*; estructura temporal ATM; densidad neutral al riesgo (Breeden-Litzenberger) opcional.
**Entradas mínimas.** S, K, T (años), r, q, tipo y estilo; precio de la opción o σ; para superficie, ≥ 5 precios de ejercicio por vencimiento.
**Parámetros.** modelo (BSM; Black-76; CRR); pasos (500); tol_iv (1e-8).
**Salidas.** TABLA: precio (moneda por unidad de subyacente), Δ, Γ, vega (por punto de volatilidad), θ (por día), ρ (por punto de tipo), IV (% anual), sesgo y estructura temporal. DETERMINISTA (fórmulas); ESTADISTICA (superficie ajustada).
**Supuestos y limitaciones.** Probabilidades neutrales al riesgo ≠ reales; BSM no captura sonrisa ni saltos; exóticos fuera de ficha.
**Tolerancias y semilla.** 1e-8 · null.
**Verificación.** Paridad put-call; caso S = K = 100, r = 5 %, σ = 20 %, T = 1 ⇒ call 10,4506, put 5,5735; segunda vía: CRR frente a BSM en europeas.
**Referencia ingenua.** Volatilidad realizada histórica como estimador de la implícita (RI-EWMA).
**Aclaración y rechazo.** Rechazo si el precio viola cotas de no arbitraje o el payoff no está en ficha.
**Referencias.** Black y Scholes (1973); Merton (1973); Black (1976); Cox, Ross y Rubinstein (1979); Hull (2022); Breeden y Litzenberger (1978); Carr y Wu (2009), «Variance Risk Premiums», *RFS* · TM-06.
**Prioridad y madurez.** P1 · IMPLEMENTADO (ejecutor, casos de control registrados (T-112)).

### TEM-DIFF-001 · Curvas de difusión y adopción

**Identificación.** v1.0 · VIGENTE · MC-04 · Mapa: áreas 9, 13.
**Perfiles y horizontes.** PERF-TEM (capa sobre RV, MP, INM, CRI) · H3–H4.
**Propósito.** ¿En qué fase de adopción está una tecnología o temática y qué trayectoria es plausible?
**Método.** Ajuste de curvas logística (m/(1 + e^{−k(t − t₀)})), Gompertz y Bass (p innovación, q imitación; adopción acumulada N(t) = m·[1 − e^{−(p+q)t}]/[1 + (q/p)e^{−(p+q)t}]) por mínimos cuadrados no lineales con varios arranques; selección por AIC y error fuera de muestra en el último tramo; punto de inflexión y fase (introducción < 16 %, crecimiento 16–50 %, madurez > 50 % de m); bandas por bootstrap de residuos; escenarios de techo m alternativo.
**Entradas mínimas.** Serie de adopción (unidades, penetración o ventas) ≥ 8 observaciones anuales o equivalentes, con al menos un tramo de aceleración observado; techo de mercado m declarado o estimado con advertencia.
**Parámetros.** modelo (auto: logística, Gompertz, Bass); m (estimado o fijado por escenarios); arranques (20); B (1 000).
**Salidas.** TABLA: parámetros, fase, punto de inflexión (fecha), adopción prevista con bandas 10/50/90 (unidades o %); SERIE: trayectoria. ESTADISTICA.
**Supuestos y limitaciones.** Antes del punto de inflexión el techo m está muy mal identificado (bandas muy anchas); la difusión de una tecnología no implica rentabilidad para el inversor (competencia, valoración).
**Tolerancias y semilla.** 1e-6 en parámetros · entero del plan.
**Verificación.** Serie sintética logística recuperada dentro de tolerancia; segunda vía: modelo alternativo.
**Referencia ingenua.** Extrapolación lineal del crecimiento reciente y crecimiento constante (FIN-CAGR-001).
**Aclaración y rechazo.** Rechazo con < 8 observaciones o sin tramo de aceleración.
**Referencias.** Bass (1969), «A New Product Growth Model for Consumer Durables», *Management Science*; Griliches (1957), *Econometrica*; Rogers (2003), *Diffusion of Innovations*, 5.ª ed.; Meade e Islam (2006), «Modelling and Forecasting the Diffusion of Innovation – A 25-Year Review», *International Journal of Forecasting* · TM-12.
**Prioridad y madurez.** P1 · IMPLEMENTADO (ejecutor, casos de control registrados (T-112)).

## 8. Fichas nuevas — renta variable (PERF-ACC)

### ACC-VAL-001 · DCF, DCF inverso y múltiplos

**Identificación.** v1.0 · VIGENTE · MC-09 · Mapa: áreas 44, 45.
**Perfiles y horizontes.** PERF-ACC (+ PERF-REI para sociedades inmobiliarias; + PERF-TEM) · H3–H4 (H2 solo contexto).
**Propósito.** ¿Cuánto descuenta el precio del agregado (sector, subsector, temática o índice)? Valor por flujos con sensibilidad, crecimiento implícito y múltiplos frente a su historia y frente al mercado. Las sociedades individuales solo entran como componentes del agregado (1.6).
**Método.** (i) FCFF y WACC (CAPM con β de ACC-FACT-001 o 1; PRM de ACC-ERP-001). (ii) Horizonte explícito y valor terminal de Gordon con g = tasa de reinversión × ROIC_nuevo. (iii) DCF inverso (crecimiento o margen implícito). (iv) Múltiplos del agregado (PER adelantado, EV/EBITDA, EV/ventas, P/VC, FCF yield; por media armónica) con percentil frente a ≥ 10 años y frente al mercado o a sectores comparables. (v) Matriz de sensibilidad WACC ±1 pp × g ±0,5 pp. (vi) Para índices y agregados amplios, DCF de flujo al accionista.
**Entradas mínimas.** Agregados contables del ámbito ≥ 3 ejercicios (5 recomendados) con fecha de presentación; nivel o capitalización agregada con fecha HT-01; deuda neta agregada; r_f en la moneda de los flujos.
**Parámetros.** años_explicitos (5; 3–10); g_terminal (min(r_f, 4 %); 0–r_f); PRM (ACC-ERP-001 o 5 %; 3–7 %); tasa_impositiva (legal marginal).
**Salidas.** TABLA: valor del agregado y EV (moneda o puntos de índice), peso del valor terminal (%), crecimiento implícito (% anual), múltiplos y percentiles, matriz de sensibilidad. DETERMINISTA (DCF sobre supuestos); ESTADISTICA (percentiles).
**Supuestos y limitaciones.** No es precio objetivo; valor terminal > 85 % ⇒ advertencia; sectores cíclicos con beneficios normalizados.
**Tolerancias y semilla.** 1e-8; DCF inverso 1e-6 · null.
**Verificación.** Suma de VP + VT = EV; g = 0 y flujo constante ⇒ perpetuidad FCF/WACC; segunda vía: múltiplos frente a DCF.
**Referencia ingenua.** Valor = precio de mercado (la señal se expresa como brecha); para previsión, RI-CM.
**Aclaración y rechazo.** Rechazo con g ≥ WACC, < 3 ejercicios o monedas inconsistentes; PER no aplicable con beneficio ≤ 0.
**Referencias.** Damodaran (2012); Koller, Goedhart y Wessels (2020); Campbell y Shiller (1988) · TM-05.
**Prioridad y madurez.** P1 · IMPLEMENTADO (ejecutor, casos de control registrados (T-112)).

### ACC-ERP-001 · Prima de riesgo implícita

**Identificación.** v1.0 · VIGENTE · MC-09 · Mapa: área 45.
**Perfiles y horizontes.** PERF-ACC, PERF-IDX · H4 (H3 contexto).
**Propósito.** ¿Qué rentabilidad esperada en exceso del tipo libre de riesgo descuenta el índice y dónde está frente a su historia?
**Método.** (i) Método de Damodaran: r que iguala el nivel del índice a 5 años de flujo al accionista (dividendos + recompras netas) creciendo a g₅ y perpetuidad a g_L = r_f; PRM = r − r_f. (ii) Rendimiento del beneficio adelantado − rendimiento real a 10 años. (iii) *Excess CAPE yield* = 1/CAPE − rendimiento real a 10 años. (iv) Percentil y z-score frente a ≥ 20 años.
**Entradas mínimas.** Nivel del índice, flujo al accionista 12 meses, crecimiento a 5 años (consenso con fecha o histórico), r_f nominal y real a 10 años, beneficios reales 10 años para CAPE.
**Parámetros.** g_L (r_f; r_f − 1 pp a r_f); incluir_recompras (true); ventana_percentil (20 años; mínimo 10).
**Salidas.** TABLA: r implícita (%), PRM (pp), versión simple (pp), ECY (pp), percentiles. ESTADISTICA.
**Supuestos y limitaciones.** Sensible a g₅; comparar rendimiento del beneficio con rendimiento nominal es un error (no se ofrece).
**Tolerancias y semilla.** 1e-6 (iterativo) · null.
**Verificación.** Con g₅ = g_L, r = rendimiento de flujo × (1 + g) + g; segunda vía: versión simple.
**Referencia ingenua.** RI-MH (PRM media histórica).
**Aclaración y rechazo.** Rechazo sin r_f de la moneda del índice.
**Referencias.** Damodaran (actualización anual); Fama y French (2002), «The Equity Premium», *Journal of Finance*; Asness (2003); Campbell y Shiller (1988) · TM-05.
**Prioridad y madurez.** P1 · IMPLEMENTADO (ejecutor, casos de control registrados (T-112)).

### ACC-FACT-001 · Exposición factorial

**Identificación.** v1.0 · VIGENTE · MC-09 · Mapa: área 50.
**Perfiles y horizontes.** PERF-ACC (+ PERF-IDX, PERF-ALT, PERF-ETF, PERF-REI) · H2–H4.
**Propósito.** ¿A qué factores está expuesto el indicador de seguimiento del ámbito y cuánto es alfa?
**Método.** Regresión de series temporales de rendimientos en exceso sobre factores de la región (MKT, SMB, HML, RMW, CMA, UMD; opcional QMJ, BAB); errores Newey-West con L = ⌊4(T/100)^{2/9}⌋; betas móviles; contribución de factores a la varianza.
**Entradas mínimas.** ≥ 36 rendimientos mensuales o 104 semanales, alineados con los factores.
**Parámetros.** modelo (FF5 + UMD; CAPM; FF3); frecuencia (mensual); ventana_movil (36 meses).
**Salidas.** TABLA: betas con t, α anualizado (%) con t, R², contribuciones (%); SERIE de betas móviles. ESTADISTICA.
**Supuestos y limitaciones.** Factores de la región correcta; α no significativo es lo habitual; t > 3 para afirmar un factor nuevo.
**Tolerancias y semilla.** 1e-8 · null.
**Verificación.** Regresión de un factor sobre sí mismo ⇒ β = 1, α = 0; segunda vía: CAPM.
**Referencia ingenua.** CAPM con β = 1.
**Aclaración y rechazo.** Rechazo con < 36 observaciones mensuales.
**Referencias.** Fama y French (1993; 2015); Carhart (1997); Newey y West (1987), *Econometrica*; Harvey, Liu y Zhu (2016) · TM-07.
**Prioridad y madurez.** P1 · IMPLEMENTADO (ejecutor, casos de control registrados (T-112)).

### ACC-MOM-001 · Momentum 12-1 y de series temporales

**Identificación.** v1.0 · VIGENTE · MC-09 · Mapa: área 50.
**Perfiles y horizontes.** PERF-ACC (variante de series temporales aplicable a PERF-FIR, PERF-CMD, PERF-FX) · H2–H3.
**Propósito.** Fuerza de la tendencia de precio relativa (transversal) y absoluta (series temporales).
**Método.** Rendimiento total de t − 12 a t − 1 meses (excluido el último mes); percentil y z-score transversal dentro del universo del tipo de activo; TSMOM = signo del rendimiento en exceso a 12 meses; escalado a volatilidad objetivo (40 %/σ) opcional; alerta de caída del momentum (mercado bajista de 24 meses + rebote > 1 σ).
**Entradas mínimas.** ≥ 13 meses de rentabilidad total (≥ 24 para escalado); universo ≥ 10 miembros para rango transversal.
**Parámetros.** retrospeccion (12; 3–12); salto (1; 0–1); escalado_vol (false).
**Salidas.** TABLA: momentum (%), percentil, z-score, señal TSMOM, volatilidad, alerta. ESTADISTICA.
**Supuestos y limitaciones.** Riesgo de caídas bruscas; costes de rotación; señal más débil en H1.
**Tolerancias y semilla.** 1e-10 · null.
**Verificación.** Rendimiento acumulado coherente con FIN-CAGR-001.
**Referencia ingenua.** RI-CM (referencia del tipo de activo) para la señal; RI-PA.
**Aclaración y rechazo.** Rechazo con precios sin ajuste por dividendos.
**Referencias.** Jegadeesh y Titman (1993); Moskowitz, Ooi y Pedersen (2012); Asness, Moskowitz y Pedersen (2013); Daniel y Moskowitz (2016) · TM-07.
**Prioridad y madurez.** P1 · IMPLEMENTADO (ejecutor V1.0, pruebas unitarias).

## 9. Fichas nuevas — renta fija y crédito (PERF-FIR)

### FIR-PRICE-001 · Precio, rendimiento, duración y convexidad

**Identificación.** v1.0 · VIGENTE · MC-09 · Mapa: área 46.
**Perfiles y horizontes.** PERF-FIR (+ deuda de PERF-REI) · H1–H4.
**Propósito.** Precio limpio y sucio, rendimientos y sensibilidades del bono genérico de un tramo o del índice representativo de un segmento (1.6).
**Método.** Precio por descuento de flujos con convención de mercado; cupón corrido; YTM y YTW por Newton/Brent; D_Macaulay, D_mod, DV01, convexidad; duración y convexidad efectivas (±Δy) en bonos con opciones; duración real en ligados a inflación; breakeven con su bono nominal.
**Entradas mínimas.** Cupón, frecuencia, vencimiento, fecha de liquidación, convención de días, precio limpio o rendimiento; calendario de rescates y curva para efectiva.
**Parámetros.** convencion (de mercado); delta_y (10 pb; 1–25).
**Salidas.** TABLA: precio limpio y sucio (por 100 nominal), cupón corrido, YTM/YTW (%), D_mac y D_mod (años), DV01 (moneda por 100 nominal y pb), convexidad (años²), breakeven (pb). DETERMINISTA.
**Supuestos y limitaciones.** La duración modificada no vale en bonos con opciones; breakeven ≠ inflación esperada pura.
**Tolerancias y semilla.** 1e-10 precio; 1e-8 rendimiento · null.
**Verificación.** Cupón = rendimiento ⇒ precio 100; caso 10 años, 5 % anual ⇒ D_mac 8,1078, D_mod 7,7217; segunda vía: aproximación por duración + convexidad frente a reprecio exacto.
**Referencia ingenua.** RI-NA (cálculo); para previsión de rendimientos, RI-PA.
**Aclaración y rechazo.** Aclaración sin convención; rechazo de bonos con flujos no modelables en ficha.
**Referencias.** Fabozzi (2012); Tuckman y Serrat (2011); ICMA, *Primary Market Handbook* y reglas de recuento · TM-05.
**Prioridad y madurez.** P1 · IMPLEMENTADO (ejecutor, casos de control registrados (T-112)).

### FIR-CURVE-001 · Curva Nelson-Siegel-Svensson y valor relativo

**Identificación.** v1.0 · VIGENTE · MC-09 · Mapa: área 47.
**Perfiles y horizontes.** PERF-FIR (+ PERF-FX para diferenciales de curvas) · H2–H4.
**Propósito.** Nivel, pendiente y curvatura de la curva; bonos ricos o baratos; pendientes 2s10s y 3m10y en percentil.
**Método.** NS o NSS por mínimos cuadrados (rendimientos o precios ponderados por 1/duración); ≥ 20 arranques con semilla; restricciones β₀ > 0, λ > 0; curva cupón cero y *forwards*; residuos por bono y su z-score frente a su historia.
**Entradas mínimas.** ≥ 6 vencimientos (≥ 8 para Svensson) con fecha común.
**Parámetros.** modelo (NSS si ≥ 8 nodos; NS); lambda (estimado; fijo Diebold-Li); arranques (20).
**Salidas.** TABLA: β₀–β₃ (%), λ₁, λ₂ (años), RMSE de ajuste (pb), residuos (pb) y z-scores, pendientes (pb) y percentiles; SERIE: curva cero y *forward*. ESTADISTICA.
**Supuestos y limitaciones.** No convexidad ⇒ mínimos locales; extremos de la curva poco anclados; prima temporal no observable.
**Tolerancias y semilla.** 1e-6 en parámetros; 1e-4 pb en ajuste · entero del plan.
**Verificación.** τ → ∞ ⇒ y → β₀; τ → 0 ⇒ y → β₀ + β₁; segunda vía: *bootstrapping* lineal.
**Referencia ingenua.** Para ajuste, interpolación lineal; para previsión, curva sin cambios (RI-PA).
**Aclaración y rechazo.** Rechazo con < 6 nodos.
**Referencias.** Nelson y Siegel (1987); Svensson (1994); Diebold y Li (2006); Gürkaynak, Sack y Wright (2007), «The U.S. Treasury Yield Curve: 1961 to the Present», *Journal of Monetary Economics* · TM-05.
**Prioridad y madurez.** P1 · IMPLEMENTADO (ejecutor, casos de control registrados (T-112)).

### FIR-CARRY-001 · Carry y rolldown

**Identificación.** v1.0 · VIGENTE · MC-09 · Mapa: áreas 47, 68.
**Perfiles y horizontes.** PERF-FIR (+ PERF-TCV para exposiciones neutrales en duración) · H2–H3.
**Propósito.** Rentabilidad esperada de un tramo con curva estable y margen de subida de tipos antes de perder.
**Método.** Carry = (rendimiento − financiación) × Δt; rolldown = −D_mod × [y(τ − Δt) − y(τ)]; total; subida de equilibrio = total/D_mod; carry/volatilidad.
**Entradas mínimas.** Curva (FIR-CURVE-001 o nodos), tramo, financiación (repo o tipo a corto), Δt.
**Parámetros.** delta_t (3 meses; 1–12).
**Salidas.** TABLA: carry, rolldown y total (pb y %), subida de equilibrio (pb), carry/volatilidad. DETERMINISTA (dada la curva).
**Supuestos y limitaciones.** Curva inalterada (supuesto, no previsión); las *forwards* implican que el carry se neutraliza bajo expectativas puras.
**Tolerancias y semilla.** 1e-10 · null.
**Verificación.** Curva plana ⇒ rolldown 0; segunda vía: reprecio completo del bono a t + Δt.
**Referencia ingenua.** Curva *forward* realizada (hipótesis de expectativas) y RI-PA.
**Aclaración y rechazo.** Aclaración sin financiación.
**Referencias.** Koijen, Moskowitz, Pedersen y Vrugt (2018), «Carry», *JFE*; Ilmanen (2011) · TM-05.
**Prioridad y madurez.** P1 · IMPLEMENTADO (ejecutor, casos de control registrados (T-112)).

### FIR-SPREAD-001 · Percentil y valor del diferencial de crédito

**Identificación.** v1.0 · VIGENTE · MC-09 · Mapa: área 48.
**Perfiles y horizontes.** PERF-FIR (+ deuda de PERF-REI y aproximación cotizada de deuda privada en PERF-PRV) · H2–H4.
**Propósito.** ¿Está el diferencial caro o barato frente a su historia y a la pérdida esperada?
**Método.** Percentil y z-score del OAS (o Z-spread) frente a ≥ 15 años que incluyan una recesión; ajuste opcional por composición (rating y duración); exceso sobre pérdida esperada s − PD·(1 − R); ampliación de equilibrio = s/duración del diferencial.
**Entradas mínimas.** Serie de diferencial semanal ≥ 10 años (15 recomendados); tasas de impago por rating; recuperación.
**Parámetros.** ventana (20 años; mínimo 10 con limitación); recuperacion (0,40; 0,2–0,6); ajuste_composicion (false).
**Salidas.** TABLA: diferencial (pb), percentil, z-score, exceso sobre pérdida esperada (pb), ampliación de equilibrio (pb). ESTADISTICA.
**Supuestos y limitaciones.** Cambios de composición del índice alteran la comparabilidad; percentiles bajos pueden persistir.
**Tolerancias y semilla.** 1e-8 · null.
**Verificación.** Percentil del máximo histórico = 1.
**Referencia ingenua.** RI-PA y RI-MH del diferencial.
**Aclaración y rechazo.** Rechazo con < 5 años.
**Referencias.** Elton, Gruber, Agrawal y Mann (2001), *Journal of Finance*; Collin-Dufresne, Goldstein y Martin (2001), *Journal of Finance*; Huang y Huang (2012), *Review of Asset Pricing Studies*; Giesecke, Longstaff, Schaefer y Strebulaev (2011), *JFE* · TM-05.
**Prioridad y madurez.** P1 · IMPLEMENTADO (ejecutor, casos de control registrados (T-112)).

### FIR-CRED-001 · Merton agregado: distancia al impago y diferencial implícito de un segmento

**Identificación.** v1.1 · VIGENTE · MC-09 · Mapa: área 48.
**Perfiles y horizontes.** PERF-FIR (segmentos corporativos), PERF-TCV, PERF-ACC (riesgo de quiebra de un sector) · H3–H4.
**Propósito.** Distribución de la probabilidad de impago estructural de los emisores de un segmento (por rating, sector o región) y comparación del diferencial observado del segmento con el implícito agregado. Los emisores individuales son solo componentes del agregado; la ficha no ordena emisores (1.6).
**Método.** Por cada componente del segmento, sistema E = V·N(d₁) − D·e^{−rT}·N(d₂), σ_E·E = N(d₁)·σ_V·V resuelto iterativamente; punto de impago = deuda a corto + ½ deuda a largo; DD y PD (neutral al riesgo con r; real con μ); diferencial implícito; alternativa «ingenua» de Bharath-Shumway; agregación del segmento: mediana, cuartiles y media ponderada por deuda de DD y PD, y proporción de componentes con DD < 2.
**Entradas mínimas.** Para ≥ 10 componentes cotizados del segmento: capitalización y volatilidad de las acciones (1 año diario), deuda a corto y largo; r, T; diferencial del índice del segmento.
**Parámetros.** T (1 año); metodo (iterativo; ingenuo); mu (rendimiento histórico de activos o r).
**Salidas.** TABLA del segmento: DD (desviaciones) y PD (%) en mediana y cuartiles, proporción con DD < 2 (%), diferencial implícito agregado y observado del índice (pb). ESTADISTICA.
**Supuestos y limitaciones.** Infraestima diferenciales a corto plazo; no válido para financieras ni para segmentos dominados por emisores sin acciones cotizadas (cobertura del segmento declarada).
**Tolerancias y semilla.** 1e-6 · null.
**Verificación.** σ_V → 0 con V > D ⇒ PD → 0; segunda vía: triángulo de crédito con la PD.
**Referencia ingenua.** PD histórica por rating.
**Aclaración y rechazo.** Rechazo para segmentos de bancos y aseguradoras, con < 10 componentes cotizados o si se pide para ordenar emisores (1.6).
**Referencias.** Merton (1974); Crosbie y Bohn (2003), *Modeling Default Risk* (Moody's KMV); Bharath y Shumway (2008); Vassalou y Xing (2004), *Journal of Finance* · TM-05.
**Prioridad y madurez.** P2 · DOCUMENTADO.

## 10. Fichas nuevas — divisas (PERF-FX)

### FX-BEER-001 · Tipo de cambio real de equilibrio (BEER)

**Identificación.** v1.0 · VIGENTE · MC-03 · Mapa: áreas 51, 8.
**Perfiles y horizontes.** PERF-FX · H4 (H3 limitado).
**Propósito.** Desalineamiento del tipo de cambio real frente a su equilibrio por fundamentales.
**Método.** Cointegración (DOLS con 2 adelantos y retardos, o Johansen) del tipo real efectivo sobre términos de intercambio, diferencial de productividad, posición de inversión internacional neta/PIB y diferencial de tipos reales; desalineamiento = residuo; velocidad de corrección y vida media.
**Entradas mínimas.** Series trimestrales ≥ 20 años, con vintages.
**Parámetros.** metodo (DOLS; Johansen); retardos (2).
**Salidas.** TABLA: coeficientes, equilibrio, desalineamiento (%) con IC, vida media (años). ESTADISTICA.
**Supuestos y limitaciones.** Equilibrio dependiente de la especificación; rupturas de régimen cambiario invalidan la muestra.
**Tolerancias y semilla.** 1e-6 · null.
**Verificación.** Residuo de media nula; segunda vía: FX-PPA-001.
**Referencia ingenua.** PPA (media histórica del tipo real) y RI-PA.
**Aclaración y rechazo.** Rechazo con < 15 años.
**Referencias.** Clark y MacDonald (1998); Phillips et al. (2013), «The External Balance Assessment (EBA) Methodology», IMF WP 13/272 · TM-13.
**Prioridad y madurez.** P2 · DOCUMENTADO.

### FX-MOM-001 · Momentum cambiario y carry ajustado por volatilidad

**Identificación.** v1.0 · VIGENTE · MC-09 · Mapa: áreas 50, 51.
**Perfiles y horizontes.** PERF-FX · H1–H3.
**Propósito.** Señales de momentum y de carry por unidad de riesgo de un par o de una cesta.
**Método.** Rendimiento en exceso (spot + carry) a 1, 3 y 12 meses; TSMOM; rango transversal en G10 o en emergentes; carry/volatilidad = diferencial/volatilidad implícita a 3 meses (realizada si no hay implícita).
**Entradas mínimas.** Spot y *forwards* o diferenciales diarios ≥ 2 años.
**Parámetros.** retrospecciones (1, 3, 12 meses); volatilidad (implicita_3m).
**Salidas.** TABLA: rendimientos en exceso (%), señales, rangos, carry/volatilidad. ESTADISTICA.
**Supuestos y limitaciones.** Colapsos del carry (asimetría negativa); intervenciones y controles de capital.
**Tolerancias y semilla.** 1e-10 · null.
**Verificación.** Coherencia con FX-CARRY-001.
**Referencia ingenua.** RI-PA.
**Aclaración y rechazo.** Rechazo sin dirección del par declarada.
**Referencias.** Menkhoff, Sarno, Schmeling y Schrimpf (2012); Burnside, Eichenbaum y Rebelo (2011); Asness, Moskowitz y Pedersen (2013) · TM-13.
**Prioridad y madurez.** P1 · IMPLEMENTADO (ejecutor, casos de control registrados (T-112)).

## 11. Fichas nuevas — materias primas (PERF-CMD)

### CMD-CURVE-001 · Estructura de la curva de futuros y roll yield

**Identificación.** v1.0 · VIGENTE · MC-09 · Mapa: área 52.
**Perfiles y horizontes.** PERF-CMD · H1–H3.
**Propósito.** ¿Contango o *backwardation*, cuánto rinde o cuesta el roll y dónde está frente a su historia?
**Método.** Pendiente entre contratos (1–2 y 1–12); roll yield anualizado = (F_próximo/F_siguiente − 1) × 365/días; *convenience yield* neto implícito = r − ln(F₂/F₁)/(T₂ − T₁); percentil de la pendiente frente a ≥ 10 años por mes del año (estacionalidad de la curva).
**Entradas mínimas.** ≥ 3 vencimientos con fechas; tipo libre de riesgo.
**Parámetros.** pares (1–2, 1–12); anualizacion (365).
**Salidas.** TABLA: pendiente (% por mes), roll yield (% anual), *convenience yield* (% anual), estado, percentil. DETERMINISTA y ESTADISTICA.
**Supuestos y limitaciones.** El roll yield no es la rentabilidad esperada del spot; curvas estacionales (gas, agrícolas) exigen comparar el mismo mes.
**Tolerancias y semilla.** 1e-10 · null.
**Verificación.** Curva plana ⇒ roll 0.
**Referencia ingenua.** Pendiente media histórica del mismo mes.
**Aclaración y rechazo.** Rechazo con < 2 contratos líquidos.
**Referencias.** Erb y Harvey (2006); Gorton y Rouwenhorst (2006); Koijen et al. (2018) · TM-13.
**Prioridad y madurez.** P1 · IMPLEMENTADO (ejecutor V1.0, pruebas unitarias).

### CMD-INV-001 · Inventarios frente a media estacional

**Identificación.** v1.0 · VIGENTE · MC-02 · Mapa: áreas 52, 6.
**Perfiles y horizontes.** PERF-CMD · H2–H3.
**Propósito.** ¿Está el inventario por encima o por debajo de lo normal para la época del año?
**Método.** Media y desviación de los mismos periodos (semana o mes del año) de los 5 años anteriores; desviación absoluta y en %; z-score; variación frente a la variación estacional típica; días de cobertura = inventario/demanda diaria; relación con la pendiente de la curva (CMD-CURVE-001).
**Entradas mínimas.** Serie semanal o mensual ≥ 5 años (10 recomendados) con fecha de publicación.
**Parámetros.** anos_estacional (5; 3–10); excluir_anos (ninguno; p. ej., años anómalos declarados).
**Salidas.** TABLA: desviación (unidades físicas y %), z-score, días de cobertura, sorpresa semanal frente a estacional. ESTADISTICA.
**Supuestos y limitaciones.** Cambios de definición y reservas estratégicas; revisiones de datos; inventarios no observados (flotantes, China).
**Tolerancias y semilla.** 1e-10 · null.
**Verificación.** Media estacional de una serie periódica pura ⇒ desviación 0; segunda vía: FX-STL-001.
**Referencia ingenua.** RI-EST.
**Aclaración y rechazo.** Rechazo con < 3 años.
**Referencias.** Working (1949); Gorton, Hayashi y Rouwenhorst (2013); Pindyck (2001), «The Dynamics of Commodity Spot and Futures Markets: A Primer», *Energy Journal* · TM-13.
**Prioridad y madurez.** P1 · IMPLEMENTADO (ejecutor, casos de control registrados (T-112)).

### CMD-RETDEC-001 · Descomposición de la rentabilidad de futuros

**Identificación.** v1.0 · VIGENTE · MC-09 · Mapa: área 52.
**Perfiles y horizontes.** PERF-CMD (+ PERF-ETF para categorías de vehículos sobre futuros de materias primas) · H3–H4.
**Propósito.** ¿Qué parte de la rentabilidad de una exposición en futuros procede del spot, del roll y del colateral?
**Método.** Rentabilidad total = variación del spot (o del contrato próximo) + roll yield realizado según el calendario de roll + rendimiento del colateral.
**Entradas mínimas.** Índice de exceso y de rentabilidad total o precios de contratos con calendario de roll; spot; tipo del colateral.
**Parámetros.** calendario_roll (el del índice); frecuencia (mensual).
**Salidas.** TABLA: componentes (% anual) e identidad. DETERMINISTA.
**Supuestos y limitaciones.** Spot de referencia y contrato próximo pueden diferir (base física).
**Tolerancias y semilla.** 1e-10 · null.
**Verificación.** Suma de componentes = total.
**Referencia ingenua.** RI-CM (índice amplio de materias primas).
**Aclaración y rechazo.** Rechazo sin calendario de roll.
**Referencias.** Erb y Harvey (2006); Gorton y Rouwenhorst (2006); Bhardwaj, Gorton y Rouwenhorst (2015), «Facts and Fantasies about Commodity Futures Ten Years Later» · TM-13.
**Prioridad y madurez.** P1 · IMPLEMENTADO (ejecutor, casos de control registrados (T-112)).

### CMD-REAL-001 · Precio real y coste marginal

**Identificación.** v1.0 · VIGENTE · MC-09 · Mapa: área 52.
**Perfiles y horizontes.** PERF-CMD · H4 (H3 contexto).
**Propósito.** ¿Está el precio real alto o bajo frente a su historia y frente al coste marginal de producción?
**Método.** Deflactar por IPC; percentil frente a ≥ 30 años; tendencia real (FX-TREND-001); razón precio/coste en el percentil 90 de la curva de costes.
**Entradas mínimas.** Precio mensual ≥ 30 años; IPC; curva de costes con fecha y fuente.
**Parámetros.** deflactor (IPC de la moneda de cotización); percentil_coste (0,90).
**Salidas.** TABLA: precio real (moneda constante), percentil, tendencia real (% anual), precio/coste. ESTADISTICA.
**Supuestos y limitaciones.** Curvas de coste cambian con la tecnología; superciclos largos con pocas observaciones.
**Tolerancias y semilla.** 1e-10 · null.
**Verificación.** IPC constante ⇒ real = nominal.
**Referencia ingenua.** RI-MH del precio real y RI-PA.
**Aclaración y rechazo.** Rechazo con < 15 años.
**Referencias.** Pindyck (1999), «The Long-Run Evolution of Energy Prices», *Energy Journal*; Erten y Ocampo (2013), «Super Cycles of Commodity Prices since the Mid-Nineteenth Century», *World Development*; Jacks (2019), *Explorations in Economic History* · TM-13.
**Prioridad y madurez.** P2 · DOCUMENTADO.

## 12. Fichas nuevas — inmobiliario cotizado (PERF-REI)

### REI-NAV-001 · Prima/descuento sobre NAV

**Identificación.** v1.0 · VIGENTE · MC-09 · Mapa: área 53.
**Perfiles y horizontes.** PERF-REI · H3–H4.
**Propósito.** ¿Cotiza el subsector inmobiliario cotizado (agregado) por encima o por debajo del valor de sus activos y cuánto variaría el NAV agregado si las tasaciones convergieran al mercado? Las sociedades individuales solo como componentes del agregado (1.6).
**Método.** P/NAV − 1 con NAV de referencia (EPRA NTA por defecto); NAV ajustado por cambio de cap rate: GAV × (cap_tasación/cap_objetivo) − deuda neta − otros pasivos; percentil frente a ≥ 10 años; agregado ponderado por capitalización.
**Entradas mínimas.** Precio y acciones con fecha; NAV publicado con fecha; GAV, deuda neta; cap rate de tasación.
**Parámetros.** nav_variante (EPRA NTA); cap_objetivo (implícito de REI-CAP-001 o null).
**Salidas.** TABLA: prima/descuento agregado y su dispersión (%), percentil, NAV ajustado agregado (variación %). ESTADISTICA.
**Supuestos y limitaciones.** NAV retrasado (6–18 meses frente al mercado cotizado); no es precio objetivo.
**Tolerancias y semilla.** 1e-10 · null.
**Verificación.** NAV = activos − pasivos.
**Referencia ingenua.** RI-MH del descuento.
**Aclaración y rechazo.** Rechazo con NAV de antigüedad > 12 meses sin advertencia.
**Referencias.** EPRA (2024), *Best Practices Recommendations*; Barkham y Geltner (1995), *Real Estate Economics*; Clayton y MacKinnon (2003), *Journal of Real Estate Finance and Economics* · TM-13.
**Prioridad y madurez.** P1 · IMPLEMENTADO (ejecutor, casos de control registrados (T-112)).

### REI-CAP-001 · Cap rate y diferencial cap rate–bono

**Identificación.** v1.0 · VIGENTE · MC-09 · Mapa: área 53.
**Perfiles y horizontes.** PERF-REI (+ PERF-PRV para inmobiliario e infraestructuras privados, con series desuavizadas) · H3–H4.
**Propósito.** ¿Compensa la rentabilidad inmobiliaria del subsector frente a la renta fija?
**Método.** Cap rate = NOI/valor (de tasación y de mercado implícito del agregado cotizado del subsector); diferencial frente al soberano a 10 años de la misma moneda; percentil frente a ≥ 15 años; cap rate de equilibrio ≈ r − g_NOI.
**Entradas mínimas.** NOI y valor; rendimiento soberano; historia ≥ 15 años del subsector y país.
**Parámetros.** base_noi (adelantado); ventana (20 años).
**Salidas.** TABLA: cap rates (%), diferencial (pb), percentil, cap de equilibrio (%). ESTADISTICA.
**Supuestos y limitaciones.** Cap rates de tasación suavizados; definición de NOI (antes o después de CAPEX) declarada.
**Tolerancias y semilla.** 1e-10 · null.
**Verificación.** Coherencia NOI/valor.
**Referencia ingenua.** RI-MH del diferencial.
**Aclaración y rechazo.** Aclaración si la base del NOI es ambigua.
**Referencias.** Plazzi, Torous y Valkanov (2010), *RFS*; Chervachidze y Wheaton (2013), *Journal of Real Estate Finance and Economics*; Geltner, Miller, Clayton y Eichholtz (2014), *Commercial Real Estate Analysis and Investments*, 3.ª ed. · TM-13.
**Prioridad y madurez.** P1 · IMPLEMENTADO (ejecutor, casos de control registrados (T-112)).

### REI-FFO-001 · FFO/AFFO y sostenibilidad del dividendo

**Identificación.** v1.0 · VIGENTE · MC-09 · Mapa: área 53.
**Perfiles y horizontes.** PERF-REI · H3.
**Propósito.** Generación de caja recurrente, valoración por P/FFO y sostenibilidad del dividendo del agregado de un subsector cotizado.
**Método.** FFO = beneficio neto + amortizaciones inmobiliarias − plusvalías; AFFO = FFO − CAPEX de mantenimiento − ajustes de rentas lineales; P/FFO, P/AFFO, percentiles; cobertura AFFO/dividendo; rendimiento AFFO.
**Entradas mínimas.** ≥ 3 ejercicios de estados; dividendo; precio.
**Parámetros.** capex_mantenimiento (reportado; estimado como % de rentas si no).
**Salidas.** TABLA: FFO y AFFO agregados (moneda y rendimiento %), múltiplos agregados, percentiles, cobertura (veces) en mediana y dispersión. DETERMINISTA y ESTADISTICA.
**Supuestos y limitaciones.** Definiciones no homogéneas entre emisores (EPRA frente a Nareit).
**Tolerancias y semilla.** 1e-10 · null.
**Verificación.** Reconciliación con el beneficio neto.
**Referencia ingenua.** RI-MH del P/FFO del subsector.
**Aclaración y rechazo.** Rechazo sin amortizaciones desglosadas.
**Referencias.** Nareit (2018), *Funds from Operations White Paper*; EPRA, *Best Practices Recommendations* · TM-13.
**Prioridad y madurez.** P1 · IMPLEMENTADO (ejecutor, casos de control registrados (T-112)).

### REI-LEV-001 · Apalancamiento y riesgo de refinanciación

**Identificación.** v1.0 · VIGENTE · MC-09 · Mapa: áreas 53, 48.
**Perfiles y horizontes.** PERF-REI · H3–H4.
**Propósito.** ¿Puede el subsector cotizado refinanciar su deuda y cuánto le cuesta? (agregado y dispersión de sus componentes; sin ordenar emisores, 1.6)
**Método.** LTV, ICR, deuda neta/EBITDA; vencimientos a 24 meses (% de la deuda); impacto en FFO de refinanciar al coste actual (swap + margen); LTV ante caídas de valor de −10 % y −20 %; holgura frente a *covenants*.
**Entradas mínimas.** Deuda por vencimiento y coste; EBITDA; GAV; coste de refinanciación actual.
**Parámetros.** caidas_valor (−10 %, −20 %); margen (de mercado).
**Salidas.** TABLA: ratios (%, veces), vencimientos (%), impacto en FFO (%), LTV estresado. DETERMINISTA.
**Supuestos y limitaciones.** Coste de refinanciación supuesto; acceso al mercado no garantizado en crisis.
**Tolerancias y semilla.** 1e-10 · null.
**Verificación.** Suma de vencimientos = deuda.
**Referencia ingenua.** RI-NA.
**Aclaración y rechazo.** Rechazo sin perfil de vencimientos.
**Referencias.** Geltner et al. (2014); Brueggeman y Fisher (2018), *Real Estate Finance and Investments*, 16.ª ed. · TM-13.
**Prioridad y madurez.** P2 · DOCUMENTADO.

## 13. Fichas nuevas — criptoactivos (PERF-CHR)

Datos mínimos del tipo de activo: **no se exigen 5 años de historia**. Cada ficha fija su mínimo; las fichas de valoración en cadena aceptan la historia completa disponible (≥ 2 años) con la limitación «pocos ciclos».

### CHR-ONCHAIN-001 · MVRV y NVT

**Identificación.** v1.0 · VIGENTE · MC-09 · Mapa: área 54.
**Perfiles y horizontes.** PERF-CHR · H3 (H2 contexto; H4 limitado).
**Propósito.** ¿Está el precio alto o bajo frente al coste medio de los tenedores (MVRV) y frente al uso de la red (NVT)?
**Método.** MVRV = capitalización/capitalización realizada; MVRV-Z = (CM − CR)/σ(CM) en ventana completa; NVT = valor de red/volumen transferido ajustado; señal NVT con media de 90 días; percentiles en la historia disponible.
**Entradas mínimas.** Series diarias de capitalización, capitalización realizada y volumen ajustado de una fuente en cadena declarada (metodología y filtros); ≥ 2 años (≥ 4 recomendados).
**Parámetros.** media_nvt (90 días); fuente (declarada).
**Salidas.** TABLA: MVRV, MVRV-Z, NVT, señal NVT, percentiles, fuente. ESTADISTICA.
**Supuestos y limitaciones.** Capitalización realizada solo directa en cadenas UTXO; umbrales históricos sobre ≈ 3–4 ciclos; volumen contaminado por movimientos internos.
**Tolerancias y semilla.** 1e-10 · null.
**Verificación.** MVRV = 1 si precio = coste medio.
**Referencia ingenua.** RI-PA y RI-CM (índice cripto de gran capitalización).
**Aclaración y rechazo.** Rechazo sin fuente en cadena verificable.
**Referencias.** Liu y Tsyvinski (2021), *RFS*; Cong, Li y Wang (2021), «Tokenomics: Dynamic Adoption and Valuation», *RFS*; Makarov y Schoar (2020), *JFE* · TM-13.
**Prioridad y madurez.** P2 · DOCUMENTADO.

### CHR-FUND-001 · Financiación de perpetuos y base

**Identificación.** v1.0 · VIGENTE · MC-09 · Mapa: áreas 54, 49.
**Perfiles y horizontes.** PERF-CHR · H1–H2.
**Propósito.** ¿Cuánto apalancamiento comprador o vendedor hay y cuánto cuesta mantenerlo?
**Método.** Financiación agregada ponderada por interés abierto; anualizada = tasa por periodo × periodos por año (3 × 365 con periodos de 8 h); base anualizada = (F/S − 1) × 365/días; percentil en 1 año; interés abierto/capitalización.
**Entradas mínimas.** Tasas de financiación e interés abierto por plataforma; precios de futuros y spot; ≥ 90 días (≥ 1 año para percentiles).
**Parámetros.** ponderacion (interes_abierto); ventana_percentil (365 días).
**Salidas.** TABLA: financiación (% anual), base (% anual), percentiles, interés abierto/capitalización (%). ESTADISTICA.
**Supuestos y limitaciones.** Plataformas con datos poco fiables; liquidaciones en cascada.
**Tolerancias y semilla.** 1e-10 · null.
**Verificación.** Coherencia base–financiación (arbitraje aproximado).
**Referencia ingenua.** RI-PA.
**Aclaración y rechazo.** Rechazo sin al menos dos plataformas.
**Referencias.** He, Manela, Ross y von Wachter (2022), «Fundamentals of Perpetual Futures»; Schmeling, Schrimpf y Todorov (2023), «Crypto Carry», BIS WP 1087 · TM-13.
**Prioridad y madurez.** P1 · IMPLEMENTADO (ejecutor, casos de control registrados (T-112)).

### CHR-FLOW-001 · Flujos de ETF y oferta de stablecoins

**Identificación.** v1.0 · VIGENTE · MC-02 · Mapa: áreas 54, 33.
**Perfiles y horizontes.** PERF-CHR · H1–H2.
**Propósito.** ¿Entra o sale dinero nuevo del tipo de activo?
**Método.** Flujo neto acumulado de ETF spot a 5 y 20 días (moneda y % de patrimonio); z-score en 1 año; crecimiento de la oferta de stablecoins principales a 30 días; razón stablecoins/capitalización total.
**Entradas mínimas.** Flujos diarios de ETF con fecha; oferta diaria de stablecoins; ≥ 120 días.
**Parámetros.** ventanas (5, 20 días); ventana_z (1 año).
**Salidas.** TABLA: flujos (moneda, %), z-scores, crecimiento (%), razón (%). ESTADISTICA.
**Supuestos y limitaciones.** Flujos de ETF publicados con retraso; acuñación de stablecoins no equivale a compra.
**Tolerancias y semilla.** 1e-10 · null.
**Verificación.** Acumulados coherentes con flujos diarios.
**Referencia ingenua.** Flujo nulo y RI-PA.
**Aclaración y rechazo.** Rechazo sin fecha de publicación de flujos.
**Referencias.** Griffin y Shams (2020), «Is Bitcoin Really Untethered?», *Journal of Finance*; Liu y Tsyvinski (2021) · TM-13.
**Prioridad y madurez.** P1 · IMPLEMENTADO (ejecutor, casos de control registrados (T-112)).

### CHR-TOKEN-001 · Tokenómica y dilución

**Identificación.** v1.0 · VIGENTE · MC-09 · Mapa: área 54.
**Perfiles y horizontes.** PERF-CHR · H2–H4.
**Propósito.** ¿Cuánta dilución futura y presión de oferta tiene la red o el sector del ecosistema (agregado de sus tokens)? Los tokens individuales solo como componentes o cuando el ámbito es la propia red (1.6).
**Método.** FDV/capitalización circulante; inflación neta anual = (emisión − quema)/oferta; desbloqueos a 30 y 90 días (% de la oferta circulante); rendimiento real de *staking* = nominal − inflación neta; concentración de tenedores (10 mayores, %) si existe dato fiable.
**Entradas mínimas.** Ofertas circulante, total y máxima; calendario de desbloqueos; emisión y quema; con fuente y fecha.
**Parámetros.** ventanas_desbloqueo (30, 90 días).
**Salidas.** TABLA: FDV/CM (veces), inflación (% anual), desbloqueos (%), rendimiento real (%), concentración (%). DETERMINISTA.
**Supuestos y limitaciones.** Calendarios modificables por gobernanza; direcciones de custodios distorsionan la concentración.
**Tolerancias y semilla.** 1e-10 · null.
**Verificación.** Circulante ≤ total ≤ máxima.
**Referencia ingenua.** RI-NA.
**Aclaración y rechazo.** Rechazo sin calendario verificable.
**Referencias.** Cong, Li y Wang (2021); Sockin y Xiong (2023), «A Model of Cryptocurrencies», *Management Science* · TM-13.
**Prioridad y madurez.** P2 · DOCUMENTADO.

## 14. Fichas nuevas — alternativos y mercados privados (PERF-PRV, PERF-ALT)

### PRV-PME-001 · Public market equivalent

**Identificación.** v1.0 · VIGENTE · MC-09 · Mapa: área 55.
**Perfiles y horizontes.** PERF-PRV · H4.
**Propósito.** ¿Ha batido la cosecha o el segmento de mercados privados (flujos agregados) al mercado cotizado comparable?
**Método.** KS-PME = [Σ D_t·(I_T/I_t) + NAV_T]/Σ C_t·(I_T/I_t); alfa directo; PME+ y LN-PME opcionales.
**Entradas mínimas.** Flujos agregados fechados de la cosecha o segmento (aportaciones, distribuciones), NAV final; índice de rentabilidad total en la misma moneda.
**Parámetros.** metodo (KS-PME; alfa_directo; PME+); indice (comparable en riesgo declarado).
**Salidas.** TABLA: KS-PME (veces), alfa directo (% anual), TIR, TVPI, DPI. DETERMINISTA.
**Supuestos y limitaciones.** NAV final de tasación; elección del índice decisiva (pequeña capitalización para *buyout*); sin ajuste por apalancamiento salvo declaración.
**Tolerancias y semilla.** 1e-8 · null.
**Verificación.** Flujos que replican el índice ⇒ KS-PME = 1.
**Referencia ingenua.** Índice cotizado (PME = 1).
**Aclaración y rechazo.** Rechazo sin fechas de flujos.
**Referencias.** Kaplan y Schoar (2005); Gredil, Griffiths y Stucke (2014); Sørensen y Jagannathan (2015), *FAJ*; Harris, Jenkinson y Kaplan (2014), *Journal of Finance* · TM-13.
**Prioridad y madurez.** P2 · DOCUMENTADO.

### PRV-CF-001 · TIR, múltiplos, curva J y proyección de flujos

**Identificación.** v1.0 · VIGENTE · MC-09 · Mapa: área 55.
**Perfiles y horizontes.** PERF-PRV · H4.
**Propósito.** Rendimiento realizado y proyectado de una cosecha o segmento de mercados privados (flujos agregados; los fondos individuales solo como componentes, 1.6).
**Método.** TIR (con aviso de múltiples soluciones), TVPI, DPI, RVPI; curva J; proyección de aportaciones, distribuciones y NAV con el modelo de Takahashi-Alexander (tasa de aportación, *bow*, crecimiento).
**Entradas mínimas.** Compromisos, aportaciones, distribuciones y NAV fechados.
**Parámetros.** tasas_aportacion (por año de vida); bow (2,5; 1–5); crecimiento (supuesto declarado).
**Salidas.** TABLA: TIR (%), múltiplos (veces); SERIE: curva J y proyección. DETERMINISTA (sobre supuestos).
**Supuestos y limitaciones.** Líneas de suscripción inflan la TIR; TIR no comparable con rentabilidades anuales de índices.
**Tolerancias y semilla.** 1e-8 · null.
**Verificación.** TVPI = DPI + RVPI.
**Referencia ingenua.** Mediana de la cosecha y estrategia.
**Aclaración y rechazo.** Rechazo sin flujos fechados.
**Referencias.** Takahashi y Alexander (2002), «Illiquid Alternative Asset Fund Modeling», *JPM*; Ljungqvist y Richardson (2003), NBER WP 9454 · TM-13.
**Prioridad y madurez.** P2 · DOCUMENTADO.

### ALT-DESMOOTH-001 · Desuavizado de rentabilidades

**Identificación.** v1.0 · VIGENTE · MC-09 · Mapa: área 55.
**Perfiles y horizontes.** PERF-PRV, PERF-ALT (incluidos inmobiliario e infraestructuras privados), PERF-REI (índices de tasación de referencia), PERF-ETF (estrategias) · H3–H4.
**Propósito.** Recuperar la volatilidad, la beta y las caídas reales de series de valoración suavizada.
**Método.** Geltner: r_t = (r*_t − φ·r*_{t−1})/(1 − φ), φ = AR(1) estimado; alternativa Getmansky-Lo-Makarov MA(k); beta de Dimson; volatilidad y MDD antes y después.
**Entradas mínimas.** ≥ 40 rentabilidades trimestrales (24 con limitación).
**Parámetros.** metodo (Geltner; GLM); k (2; 1–3); phi (estimado o fijado).
**Salidas.** SERIE desuavizada; TABLA: φ o θ, volatilidad observada y desuavizada (% anual), beta Dimson, MDD. ESTADISTICA.
**Supuestos y limitaciones.** Suavizado lineal y estable; φ estimado con error.
**Tolerancias y semilla.** 1e-8 · null.
**Verificación.** φ = 0 ⇒ serie sin cambios; media de la serie conservada.
**Referencia ingenua.** Serie observada sin ajuste.
**Aclaración y rechazo.** Rechazo con < 24 observaciones.
**Referencias.** Geltner (1993); Getmansky, Lo y Makarov (2004); Dimson (1979), *JFE*; Okunev y White (2003), *Journal of Alternative Investments* · TM-13.
**Prioridad y madurez.** P1 · IMPLEMENTADO (ejecutor, casos de control registrados (T-112)).

### ALT-HF-001 · Exposición factorial de estrategias hedge

**Identificación.** v1.0 · VIGENTE · MC-09 · Mapa: áreas 55, 50.
**Perfiles y horizontes.** PERF-ALT (+ PERF-ETF para categorías de estrategias) · H3–H4.
**Propósito.** ¿Cuánto de la rentabilidad de una estrategia hedge (índice de la estrategia o agregado de la categoría) es exposición a factores negociables y cuánto alfa?
**Método.** Regresión sobre factores de Fung-Hsieh (renta variable, tamaño, bonos, diferencial, factores de tendencia en bonos, divisas y materias primas) u otros declarados; desuavizado previo; alfa con Newey-West; advertencia de sesgos de supervivencia y relleno retrospectivo.
**Entradas mínimas.** ≥ 36 rentabilidades mensuales de la estrategia o índice.
**Parámetros.** factores (Fung-Hsieh 7); desuavizar (true).
**Salidas.** TABLA: exposiciones, α (% anual) con t, R². ESTADISTICA.
**Supuestos y limitaciones.** Exposiciones no lineales (opcionalidad) solo parcialmente capturadas; sesgos de bases de datos de varios puntos anuales.
**Tolerancias y semilla.** 1e-8 · null.
**Verificación.** Coherencia con ACC-FACT-001.
**Referencia ingenua.** Cartera pasiva de factores (o 60/40).
**Aclaración y rechazo.** Rechazo con < 36 observaciones.
**Referencias.** Fung y Hsieh (2001; 2004), *RFS*, *FAJ*; Agarwal y Naik (2004), *RFS*; Hasanhodzic y Lo (2007), *Journal of Investment Management* · TM-13.
**Prioridad y madurez.** P2 · DOCUMENTADO.

### ALT-AUC-001 · Índice de transacciones de coleccionables

**Identificación.** v1.0 · VIGENTE · MC-09 (regresión hedónica con MC-03 como módulo invitado) · Mapa: área 55.
**Perfiles y horizontes.** PERF-ALT · H4.
**Propósito.** Rentabilidad, riesgo y dispersión de una categoría de coleccionables (arte, vino, relojes, etc.).
**Método.** Ventas repetidas (Bailey-Muth-Nourse / Case-Shiller) o regresión hedónica sobre características con efectos temporales; índice base 100; rentabilidad y volatilidad; dispersión de rentabilidades individuales; ajuste de sesgo de selección declarado; neto de comisiones de compraventa.
**Entradas mínimas.** ≥ 500 transacciones con fecha y precio (ventas repetidas: ≥ 200 pares).
**Parámetros.** metodo (ventas_repetidas; hedonico); comisiones (supuesto declarado, 10–25 %).
**Salidas.** TABLA: rentabilidad anual bruta y neta (%), volatilidad (%), dispersión; SERIE: índice. ESTADISTICA.
**Supuestos y limitaciones.** Sesgo de selección (solo se subasta lo revalorizado); la mediana del índice no es la rentabilidad de una pieza; autenticidad no evaluada.
**Tolerancias y semilla.** 1e-6 · null.
**Verificación.** Índice = 100 en la base; segunda vía: método alternativo.
**Referencia ingenua.** IPC (rentabilidad real nula) y RI-CM de renta variable global.
**Aclaración y rechazo.** Rechazo por debajo del mínimo de transacciones.
**Referencias.** Bailey, Muth y Nourse (1963), *JASA*; Case y Shiller (1987), *New England Economic Review*; Mei y Moses (2002), *AER*; Korteweg, Kräussl y Verwijmeren (2016), *RFS*; Dimson, Rousseau y Spaenjers (2015), *JFE* · TM-13.
**Prioridad y madurez.** P2 · DOCUMENTADO.

## 15. Fichas nuevas V5.0 — índices bursátiles (PERF-IDX)

Unidad de análisis: el índice como mercado completo, el ratio entre índices o la cesta afectada por un evento de índice. Los componentes individuales solo entran como datos de composición (1.6).

### IDX-ERP-001 · Rentabilidad esperada por índice (Grinold-Kroner)

**Identificación.** v1.0 · VIGENTE · MC-09 · Mapa: áreas 64, 45.
**Perfiles y horizontes.** PERF-IDX (+ PERF-ACC para agregados sectoriales amplios) · H4 (H3 contexto).
**Propósito.** ¿Qué rentabilidad nominal y real a largo plazo descuenta el nivel actual de un índice, cuál es su prima frente al tipo libre de riesgo y cómo se compara con la de otros índices?
**Método.** (i) E[R] ≈ rentabilidad por dividendo + rentabilidad neta por recompras (recompras − emisiones, o −dilución neta) + crecimiento real del BPA + inflación esperada + cambio anualizado de valoración, con %Δ(múltiplo) = (múltiplo_objetivo/múltiplo_actual)^{1/N} − 1. (ii) Múltiplo objetivo: mediana histórica del índice con reversión parcial λ (fracción de la brecha que se cierra en N años) o sin cambio, declarado. (iii) Prima = E[R] − r_f a N años en la divisa del índice. (iv) Bandas por escenarios bajo/central/alto de cada bloque (y, si se pide, SCN-H-001 en H4). (v) Comparación entre índices en divisa común: cubierta (E[R] local + diferencial de tipos a N años) y no cubierta (con supuesto de tipo de cambio declarado).
**Entradas mínimas.** Nivel; rentabilidad por dividendo 12 meses; recompras y emisiones netas 12 meses; crecimiento real del BPA (histórico ≥ 20 años o consenso con fecha); inflación esperada a N años (encuestas o breakeven); múltiplo actual e historia ≥ 20 años (CAPE con ≥ 10 años de beneficios reales); r_f a N años de la divisa.
**Parámetros.** N (10; 5–10 años); lambda_reversion (0,5; 0–1); multiplo (CAPE; PER adelantado); cobertura (cubierta; ambas).
**Salidas.** TABLA: bloques (% anual), E[R] nominal y real (% anual), prima frente a r_f (pp), rango por escenarios, diferencias entre índices (pp). DETERMINISTA (sobre supuestos declarados); ESTADISTICA (crecimiento estimado y percentiles).
**Supuestos y limitaciones.** Identidad aproximada, no previsión; muy sensible al supuesto de reversión del múltiplo; el crecimiento del BPA del índice difiere del PIB (dilución, composición, beneficios en el extranjero); útil en H4; las diferencias entre índices incorporan diferencias de composición sectorial (declarar o combinar con IDX-REL-001).
**Tolerancias y semilla.** 1e-10 · null.
**Verificación.** Sin cambio de múltiplo y sin recompras netas, E[R] = rentabilidad por dividendo + crecimiento nominal (Gordon); suma de bloques = total; segunda vía: ACC-ERP-001 (r implícita) y 1/CAPE.
**Referencia ingenua.** RI-MH (rentabilidad histórica del índice y prima media histórica).
**Aclaración y rechazo.** Aclaración sin divisa de comparación; rechazo sin historia del múltiplo ≥ 10 años o sin r_f de la divisa.
**Referencias.** Grinold y Kroner (2002), «The Equity Risk Premium», *Investment Insights* (Barclays Global Investors); Ilmanen (2011), *Expected Returns*; Campbell y Shiller (1998), «Valuation Ratios and the Long-Run Stock Market Outlook», *JPM*; Arnott y Bernstein (2003), «Earnings Growth: The Two Percent Dilution», *FAJ*; Bogle (1991), «Investing in the 1990s», *JPM* · TM-05, TM-13.
**Prioridad y madurez.** P1 · IMPLEMENTADO (ejecutor, casos de control registrados (T-106)).

### IDX-CONC-001 · Concentración y amplitud de un índice

**Identificación.** v1.0 · VIGENTE · MC-01 · Mapa: áreas 64, 23, 33.
**Perfiles y horizontes.** PERF-IDX (+ PERF-ACC para agregados sectoriales) · H2–H4.
**Propósito.** ¿Cuán concentrado está el índice y cuán amplia es la participación de sus componentes en su evolución, frente a su propia historia?
**Método.** (i) Peso de los n mayores (%); HHI = Σwᵢ²; número efectivo de componentes N_ef = 1/HHI; HHI sectorial. (ii) Amplitud: porcentaje de componentes sobre su media de 200 sesiones; línea avance–retroceso; diferencial de rentabilidad entre la versión ponderada por capitalización y la equiponderada a 3 y 12 meses. (iii) Contribución de los n mayores a la rentabilidad del periodo. (iv) Percentil y z-score de cada métrica frente a ≥ 10 años.
**Entradas mínimas.** Pesos de los componentes con fecha (composición en su fecha, sin supervivencia); precios de los componentes ≥ 1 año para amplitud; historia de pesos ≥ 10 años para percentiles.
**Parámetros.** top_n (10; 5–50); media_amplitud (200 sesiones); ventana_percentil (20 años; mínimo 10).
**Salidas.** TABLA: peso de los n mayores (%), HHI, N_ef (componentes), HHI sectorial, amplitud (%), diferencial ponderado–equiponderado (pp), contribución (%), percentiles. DETERMINISTA (concentración) y ESTADISTICA (percentiles).
**Supuestos y limitaciones.** Los componentes son datos de composición, nunca candidatos a selección (1.6); la concentración describe el riesgo del índice, no es señal de tiempo; topes de peso y cambios metodológicos rompen la comparabilidad.
**Tolerancias y semilla.** 1e-10 · null.
**Verificación.** Pesos suman 1; índice equiponderado de n componentes ⇒ N_ef = n; segunda vía: HHI con pesos de cierre frente a pesos medios del periodo.
**Referencia ingenua.** RI-MH de la concentración; RI-NA para descriptivos.
**Aclaración y rechazo.** Rechazo sin composición fechada.
**Referencias.** Rhoades (1993), «The Herfindahl-Hirschman Index», *Federal Reserve Bulletin*; Gabaix (2011), «The Granular Origins of Aggregate Fluctuations», *Econometrica*; Bessembinder (2018), «Do Stocks Outperform Treasury Bills?», *JFE* · TM-13.
**Prioridad y madurez.** P1 · IMPLEMENTADO (ejecutor, casos de control registrados (T-106)).

### IDX-REL-001 · Valor relativo entre índices

**Identificación.** v1.0 · VIGENTE · MC-09 (MC-03 como módulo invitado para regresiones) · Mapa: áreas 64, 45, 50.
**Perfiles y horizontes.** PERF-IDX · H2–H4 (en H2 solo el momentum relativo es señal; la valoración es contexto).
**Propósito.** ¿Está un índice caro o barato frente a otro (o frente al agregado global) una vez corregidas las diferencias de composición, y lo acompaña el momentum relativo?
**Método.** (i) Brecha de múltiplos (PER adelantado, CAPE, P/VC, rentabilidad por dividendo) entre los índices A y B: ratio y log-ratio; z-score y percentil frente a ≥ 15 años. (ii) Ajuste por composición: múltiplo de B recompuesto con los pesos sectoriales de A y brecha residual neutral sectorial. (iii) Diferencia de E[R] de IDX-ERP-001. (iv) Momentum relativo 12-1 y a 3 meses del ratio de rentabilidades totales en divisa común, cubierto y no cubierto. (v) Diferencial de revisiones agregadas de BPA a 3 meses.
**Entradas mínimas.** Múltiplos y rentabilidad total mensuales de ambos índices ≥ 15 años (10 con limitación); pesos y múltiplos sectoriales para el ajuste; tipos de cambio y diferenciales de tipos.
**Parámetros.** multiplos (PER adelantado, CAPE); ajuste_sectorial (true); ventana (20 años); divisa_comun (EUR); cobertura (ambas).
**Salidas.** TABLA: brechas (% y log), z-scores, percentiles, brecha neutral sectorial (%), diferencia de E[R] (pp), momentum relativo (%), diferencial de revisiones (pp). ESTADISTICA.
**Supuestos y limitaciones.** Las brechas entre regiones pueden persistir (composición, crecimiento, gobernanza, tipos); reversión lenta: la valoración relativa no es señal de tiempo en H2; la divisa puede dominar el resultado.
**Tolerancias y semilla.** 1e-8 · null.
**Verificación.** Un índice frente a sí mismo ⇒ brecha 0 (z indefinido, declarado); segunda vía: brecha con un múltiplo alternativo.
**Referencia ingenua.** RI-MH de la brecha y RI-PA del ratio de precios.
**Aclaración y rechazo.** Rechazo con < 10 años o sin divisa común declarada.
**Referencias.** Asness, Moskowitz y Pedersen (2013), «Value and Momentum Everywhere», *Journal of Finance*; Asness, Ilmanen, Israel y Moskowitz (2015), «Investing with Style», *Journal of Investment Management*; Campbell y Shiller (1988), *Journal of Finance* · TM-05, TM-13.
**Prioridad y madurez.** P1 · IMPLEMENTADO (ejecutor, casos de control registrados (T-106)).

### IDX-REB-001 · Efecto de rebalanceo y cambios de composición

**Identificación.** v1.0 · VIGENTE · MC-03 (estudio de eventos; MC-01 para la demanda estimada) · Mapa: áreas 64, 11, 33.
**Perfiles y horizontes.** PERF-IDX · H1 (limitado: solo eventos fechados)–H2.
**Propósito.** ¿Qué presión de demanda u oferta genera un rebalanceo o un cambio de composición fechado y cómo se ha comportado históricamente la cesta afectada alrededor de eventos comparables?
**Método.** (i) Demanda estimada = Δpeso × activos que replican el índice (estimación con fuente y fecha), expresada en días de volumen medio de la cesta afectada (inclusiones, exclusiones o segmento reponderado). (ii) Estudio de eventos sobre ≥ 20 eventos comparables: rentabilidades anormales acumuladas (CAR) de la cesta frente al índice entre anuncio y efectividad y de efectividad a +20 sesiones; contraste BMP (Boehmer-Musumeci-Poulsen); tendencia temporal del efecto (anticipación creciente). (iii) Calendario del próximo evento.
**Entradas mínimas.** Fechas de anuncio y efectividad; cambios de peso; activos indexados estimados; volumen medio; ≥ 20 eventos comparables para el estudio.
**Parámetros.** ventana_evento (anuncio→efectividad; efectividad→+20); modelo_normal (índice de mercado; modelo de mercado con 250 sesiones de estimación); contraste (BMP).
**Salidas.** TABLA: demanda estimada (moneda y días de volumen), CAR medio y mediano (%) con IC, n de eventos, tendencia del efecto (pp por década). ESTADISTICA.
**Supuestos y limitaciones.** Activos indexados estimados; arbitrajistas anticipan; efecto en declive documentado; la salida describe la cesta del evento, nunca selecciona valores afectados (1.6).
**Tolerancias y semilla.** 1e-8 · null.
**Verificación.** Suma de cambios de peso = 0 salvo flujos declarados; segunda vía: modelo normal alternativo.
**Referencia ingenua.** CAR nulo; RI-TB para dirección.
**Aclaración y rechazo.** Con < 20 eventos comparables solo se entrega la demanda estimada, sin estudio de eventos.
**Referencias.** Shleifer (1986), «Do Demand Curves for Stocks Slope Down?», *Journal of Finance*; Harris y Gurel (1986), *Journal of Finance*; Greenwood (2005), «Short- and Long-Term Demand Curves for Stocks», *JFE*; Petajisto (2011), «The Index Premium and Its Hidden Cost for Index Funds», *Journal of Empirical Finance*; MacKinlay (1997), «Event Studies in Economics and Finance», *JEL*; Boehmer, Musumeci y Poulsen (1991), *JFE* · TM-04, TM-13.
**Prioridad y madurez.** P2 · IMPLEMENTADO (ejecutor, casos de control registrados (T-106)).

## 16. Fichas nuevas V5.0 — fondos y vehículos de inversión colectiva (PERF-ETF)

Unidad de análisis: la categoría o segmento de vehículos. Los vehículos individuales solo entran como miembros del agregado; ninguna ficha los ordena por coste, seguimiento o comisión (1.6).

### FON-DISC-001 · Descuento de fondos cerrados frente a su media

**Identificación.** v1.0 · VIGENTE · MC-09 · Mapa: áreas 65, 56.
**Perfiles y horizontes.** PERF-ETF (+ PERF-PRV y PERF-REI para categorías de vehículos cotizados de activos privados o inmobiliarios) · H3–H4 (H2 limitado, con catalizador).
**Propósito.** ¿Cotiza una categoría de fondos cerrados (o de vehículos cotizados con NAV) con un descuento anormalmente amplio o estrecho frente a su historia, y qué rentabilidad aportaría su normalización?
**Método.** (i) d = P/NAV − 1 por miembro y agregado de la categoría (mediana y media ponderada por capitalización). (ii) z = (d − d̄)/σ_d frente a la media de 52 semanas y de 3–5 años; percentil; dispersión entre miembros. (iii) Rentabilidad por normalización a H si el descuento cierra una fracción κ de la brecha: (1 + d_obj)/(1 + d) − 1, con d_obj = d + κ·(d̄ − d), más la rentabilidad supuesta del NAV (declarada). (iv) Vida media de la reversión por AR(1) del descuento agregado. (v) Catalizadores agregados (recompras, ofertas, votaciones de continuidad, cambios regulatorios) como variable externa declarada.
**Entradas mínimas.** Precio y NAV fechados de ≥ 5 miembros (NAV ≥ semanal; en activos privados, fecha de NAV declarada); ≥ 3 años (≥ 5 recomendados).
**Parámetros.** ventana_media (52 semanas; 26–260); ventana_larga (5 años); kappa (0,5; 0–1); agregacion (mediana).
**Salidas.** TABLA: descuento agregado (%), z-scores, percentil, dispersión (pp), vida media (meses), rentabilidad por normalización (% a H), desglose por subcategoría. ESTADISTICA.
**Supuestos y limitaciones.** NAV retrasados (privados, inmobiliario) sesgan el descuento; descuentos persistentes por comisiones, apalancamiento, fiscalidad o iliquidez; la reversión no está garantizada y el descuento puede ampliarse en crisis de liquidez.
**Tolerancias y semilla.** 1e-10 · null.
**Verificación.** P = NAV ⇒ d = 0; agregado entre el mínimo y el máximo de los miembros; segunda vía: media ponderada frente a mediana.
**Referencia ingenua.** RI-MH (media del descuento) y RI-PA (descuento sin cambio).
**Aclaración y rechazo.** Rechazo con < 5 miembros, sin fecha de NAV o con NAV de antigüedad > 6 meses (> 12 en activos privados) sin ajuste declarado.
**Referencias.** Lee, Shleifer y Thaler (1991), «Investor Sentiment and the Closed-End Fund Puzzle», *Journal of Finance*; Pontiff (1995), «Closed-End Fund Premia and Returns: Implications for Financial Market Equilibrium», *JFE*; Cherkes, Sagi y Stanton (2009), «A Liquidity-Based Theory of Closed-End Funds», *RFS*; Thompson (1978), «The Information Content of Discounts and Premiums on Closed-End Fund Shares», *JFE* · TM-13.
**Prioridad y madurez.** P1 · IMPLEMENTADO (ejecutor, casos de control registrados (T-106)).

### FON-FLOW-001 · Flujos por categoría de vehículos

**Identificación.** v1.0 · VIGENTE · MC-02 · Mapa: áreas 65, 33.
**Perfiles y horizontes.** PERF-ETF (+ cualquier perfil como señal de demanda del ámbito) · H2 (limitado)–H3.
**Propósito.** ¿Hacia qué categorías de vehículos (por tipo de activo, región, sector, estilo, temática o estrategia) entra o sale dinero, con qué persistencia y con qué intensidad relativa a su patrimonio?
**Método.** (i) Flujo neto = AUM_t − AUM_{t−1}·(1 + r_t) si no se publica directamente. (ii) Flujo relativo = flujo/AUM_{t−1}; acumulados a 1, 3 y 12 meses. (iii) z-score frente a 3 años; persistencia por autocorrelación de orden 1–3. (iv) Rango entre categorías; separación de vehículos indexados y de gestión activa. (v) Señal contraria opcional (percentil > 95 o < 5) declarada como hipótesis, no como regla.
**Entradas mínimas.** AUM y rentabilidad (o flujos publicados) por categoría, mensual ≥ 3 años o semanal ≥ 1 año; taxonomía fija declarada.
**Parámetros.** ventanas (1, 3, 12 meses); ventana_z (36 meses); taxonomia (la del proveedor, declarada).
**Salidas.** TABLA por categoría: flujos (moneda y % de AUM), z-scores, autocorrelaciones, rango; SERIE de flujos acumulados. ESTADISTICA.
**Supuestos y limitaciones.** Los flujos de vehículos cotizados incluyen creaciones y reembolsos de intermediarios y coberturas; cambios de taxonomía; los flujos persiguen rentabilidades pasadas; la relación flujo–rentabilidad futura es débil y cambiante.
**Tolerancias y semilla.** 1e-10 · null.
**Verificación.** Suma de flujos de las categorías = flujo total; identidad de AUM.
**Referencia ingenua.** Flujo nulo y RI-PA del flujo relativo.
**Aclaración y rechazo.** Rechazo sin taxonomía fija o con < 12 meses.
**Referencias.** Sirri y Tufano (1998), «Costly Search and Mutual Fund Flows», *Journal of Finance*; Coval y Stafford (2007), «Asset Fire Sales (and Purchases) in Equity Markets», *JFE*; Frazzini y Lamont (2008), «Dumb Money: Mutual Fund Flows and the Cross-Section of Stock Returns», *JFE*; Ben-David, Franzoni y Moussawi (2018), «Do ETFs Increase Volatility?», *Journal of Finance* · TM-13.
**Prioridad y madurez.** P1 · IMPLEMENTADO (ejecutor, casos de control registrados (T-106)).

### FON-TD-001 · Diferencia de seguimiento agregada por categoría

**Identificación.** v1.0 · VIGENTE · MC-01 (MC-09 como módulo invitado para la descomposición) · Mapa: áreas 56, 65.
**Perfiles y horizontes.** PERF-ETF · H3–H4.
**Propósito.** ¿Cuánto se aleja, de forma sistemática, la rentabilidad de una categoría de vehículos indexados de la de su índice, y qué componentes estructurales la explican (gastos, préstamo de valores, fiscalidad de dividendos, método de replicación)?
**Método.** (i) TDᵢ = r_vehículo − r_índice (anual, variante comparable del índice); TEᵢ = σ(diferencias periódicas)·√periodos. (ii) Agregado de la categoría: mediana, cuartiles y dispersión de TD y TE. (iii) Descomposición estimada TD ≈ −gastos corrientes + préstamo de valores + diferencial de retención fiscal ± efecto de replicación ± efecto de caja, con residuo declarado. (iv) Comparación entre segmentos de la categoría (método de replicación, domicilio) y tendencia de la TD mediana.
**Entradas mínimas.** Rentabilidades totales de ≥ 5 miembros y del índice en la variante correcta ≥ 3 años; gastos corrientes; método de replicación.
**Parámetros.** frecuencia (diaria para TE; anual para TD); variante_indice (neta); agregacion (mediana).
**Salidas.** TABLA: TD mediana y cuartiles (pb anuales), TE mediano (% anual), descomposición (pb), tendencia (pb por año), diferencias entre segmentos (pb). ESTADISTICA.
**Supuestos y limitaciones.** Una variante del índice equivocada genera TD espuria; diferencias de hora de valoración en índices de otras zonas; con pocos miembros el agregado es frágil. La salida es la categoría o el segmento, nunca un ranking de vehículos (1.6).
**Tolerancias y semilla.** 1e-10 · null.
**Verificación.** Vehículo idéntico al índice ⇒ TD = 0 y TE = 0; componentes de la descomposición + residuo = TD.
**Referencia ingenua.** TD = −gastos corrientes medios de la categoría.
**Aclaración y rechazo.** Aclaración si la variante del índice no se declara; rechazo con < 5 miembros.
**Referencias.** Pope y Yadav (1994), «Discovering Errors in Tracking Error», *JPM*; Frino y Gallagher (2001), «Tracking S&P 500 Index Funds», *JPM*; Elton, Gruber, Comer y Li (2002), «Spiders: Where Are the Bugs?», *Journal of Business* · TM-13.
**Prioridad y madurez.** P2 · IMPLEMENTADO (ejecutor, casos de control registrados (T-106)).

### FON-LEV-001 · Decaimiento por volatilidad de vehículos apalancados e inversos

**Identificación.** v1.0 · VIGENTE · MC-09 (MC-05 como módulo invitado para la simulación) · Mapa: áreas 56, 65, 14.
**Perfiles y horizontes.** PERF-ETF (+ PERF-DER) · H2 (limitado)–H3.
**Propósito.** ¿Cuánto se separa, en un horizonte dado, la rentabilidad de una estructura con apalancamiento diario L de L veces la del índice, en función de la volatilidad y de la tendencia, y en qué régimen favorece o perjudica a la categoría?
**Método.** (i) Aproximación continua: R_L(T) ≈ (1 + R_índice(T))^L · exp(−½·(L² − L)·σ²·T) − 1, menos coste de financiación (L − 1)·r·T y gastos medios de la categoría. (ii) Arrastre por volatilidad = ½·(L² − L)·σ²·T. (iii) Mapa de R_L frente a L·R_índice en una rejilla (σ, R_índice) y umbral de σ a partir del cual el arrastre domina una tendencia dada. (iv) Segunda vía: reconstrucción exacta con rebalanceo diario sobre la serie histórica del índice y simulación de trayectorias (SIM-MC-001) en el régimen de volatilidad vigente (VOL-GARCH-001).
**Entradas mínimas.** Rentabilidades diarias del índice ≥ 1 año; L; tipo de financiación; gastos medios de la categoría; horizonte.
**Parámetros.** L (2; −3 a 3); horizonte (20–250 sesiones); rejilla_sigma (10–80 %); n_trayectorias (10 000).
**Salidas.** TABLA: arrastre esperado (% a T), R_L frente a L·R_índice (pp), umbral de σ (% anual), rejilla, percentiles simulados. DETERMINISTA (fórmula y reconstrucción) y ESTADISTICA (simulación).
**Supuestos y limitaciones.** Rebalanceo diario exacto al cierre; saltos y huecos amplifican el arrastre; la fórmula es exacta solo bajo movimiento browniano geométrico. Describe la estructura de la categoría, no vehículos concretos (1.6).
**Tolerancias y semilla.** 1e-10 fórmula y reconstrucción; 1e-6 simulación con la misma semilla · obligatoria en simulación.
**Verificación.** L = 1 ⇒ arrastre 0; reconstrucción diaria frente a fórmula dentro de la banda esperada en GBM sintético.
**Referencia ingenua.** L × rentabilidad del índice.
**Aclaración y rechazo.** Rechazo sin datos diarios o sin L declarado.
**Referencias.** Cheng y Madhavan (2009), «The Dynamics of Leveraged and Inverse Exchange-Traded Funds», *Journal of Investment Management*; Avellaneda y Zhang (2010), «Path-Dependence of Leveraged ETF Returns», *SIAM Journal on Financial Mathematics* · TM-06, TM-13.
**Prioridad y madurez.** P2 · IMPLEMENTADO (ejecutor, casos de control registrados (T-106)).

## 17. Fichas nuevas V5.0 — derivados financieros (PERF-DER)

Unidad de análisis: el subyacente representativo y sus contratos genéricos (ATM, deltas estándar, vencimiento constante). Ninguna ficha compara contratos, emisores de productos o plataformas (1.6).

### DER-VRP-001 · Prima de varianza implícita-realizada

**Identificación.** v1.0 · VIGENTE · MC-09 (MC-02 como módulo invitado para la previsión de volatilidad) · Mapa: áreas 66, 49.
**Perfiles y horizontes.** PERF-DER (+ PERF-TCV para índices de volatilidad) · H1–H3.
**Propósito.** ¿Cuánto pagan las opciones de un subyacente por encima de la volatilidad que luego se realiza, y está la prima actual alta o baja frente a su historia?
**Método.** (i) Varianza implícita a 30 días: índice publicado (tipo VIX) o réplica libre de modelo con la cesta de opciones fuera de dinero, σ²_imp = (2/T)·Σ(ΔKᵢ/Kᵢ²)·e^{rT}·Q(Kᵢ) − (1/T)·(F/K₀ − 1)². (ii) Varianza realizada esperada (HAR-RV o GARCH de VOL-GARCH-001) y realizada posterior a 21 sesiones (solo para la historia). (iii) VRP ex ante = σ²_imp − E_t[RV]; VRP ex post = σ²_imp,t − RV_{t→t+21}; versión en volatilidad (σ_imp − σ_real). (iv) Percentil y z-score frente a ≥ 5 años; frecuencia histórica de VRP > 0; ES de la estrategia de venta de varianza (colas).
**Entradas mínimas.** Volatilidad implícita diaria (índice publicado o superficie con ≥ 5 precios de ejercicio) ≥ 3 años (≥ 5 recomendados); precios diarios del subyacente.
**Parámetros.** plazo (30 días; 7–90); prevision_rv (HAR; GARCH; realizada pasada); ventana_percentil (5 años).
**Salidas.** TABLA: σ_imp, σ_real esperada y posterior (% anual), VRP en varianza y en volatilidad (puntos), percentiles, frecuencia de VRP > 0 (%), ES de la venta de varianza (%). ESTADISTICA.
**Supuestos y limitaciones.** VRP positiva en promedio con pérdidas extremas en crisis (asimetría negativa); la realizada posterior usa datos futuros y nunca entra en la señal actual (fuga, M13); los índices publicados tienen metodología propia.
**Tolerancias y semilla.** 1e-8 · null.
**Verificación.** σ_imp = σ_real ⇒ VRP = 0; signo coherente entre las versiones en varianza y en volatilidad; segunda vía: índice publicado frente a réplica.
**Referencia ingenua.** RI-MH de la VRP; RI-EWMA para la realizada esperada.
**Aclaración y rechazo.** Rechazo con < 2 años o con plazos no alineados.
**Referencias.** Carr y Wu (2009), «Variance Risk Premiums», *RFS*; Bollerslev, Tauchen y Zhou (2009), «Expected Stock Returns and Variance Risk Premia», *RFS*; Bakshi y Kapadia (2003), «Delta-Hedged Gains and the Negative Market Volatility Risk Premium», *RFS*; Demeterfi, Derman, Kamal y Zou (1999), «More Than You Ever Wanted to Know about Volatility Swaps», Goldman Sachs Quantitative Strategies Research Notes; Corsi (2009), «A Simple Approximate Long-Memory Model of Realized Volatility», *Journal of Financial Econometrics*; Cboe, *VIX White Paper* · TM-06.
**Prioridad y madurez.** P1 · IMPLEMENTADO (ejecutor, casos de control registrados (T-106)).

### DER-SKEW-001 · Sesgo de la volatilidad implícita

**Identificación.** v1.0 · VIGENTE · MC-09 · Mapa: áreas 66, 49.
**Perfiles y horizontes.** PERF-DER (+ PERF-FX con *risk reversals*, PERF-TCV) · H1–H3.
**Propósito.** ¿Cuánto más caras están las protecciones bajistas (o alcistas) que las opciones en el dinero, y cómo se compara ese sesgo con su historia?
**Método.** (i) *Risk reversal* 25Δ = σ_put25Δ − σ_call25Δ (signo de convención declarado); pendiente normalizada = RR/σ_ATM; mariposa 25Δ = (σ_put25Δ + σ_call25Δ)/2 − σ_ATM. (ii) Alternativa: ajuste SVI por vencimiento y pendiente en k = 0. (iii) Asimetría neutral al riesgo (Bakshi-Kapadia-Madan) o índice de sesgo publicado. (iv) Coste de una protección estándar (put al 90 % a 3 meses, en % del nocional) frente a su historia. (v) Percentil y z-score frente a ≥ 3 años por vencimiento.
**Entradas mínimas.** Superficie con ≥ 5 precios de ejercicio por vencimiento o cotizaciones de RR y BF; diaria ≥ 2 años.
**Parámetros.** delta (25; 10–25); vencimiento (3 meses; 1–12); metodo (deltas; SVI).
**Salidas.** TABLA: RR, BF y pendiente normalizada (puntos), coste de protección (% del nocional), asimetría neutral al riesgo, percentiles. ESTADISTICA.
**Supuestos y limitaciones.** El sesgo depende de la convención de delta (spot o *forward*, con o sin prima); las probabilidades neutrales al riesgo no son reales; los cambios de nivel de la volatilidad alteran el sesgo (usar la versión normalizada).
**Tolerancias y semilla.** 1e-8 · null.
**Verificación.** Sonrisa simétrica ⇒ RR = 0; SVI sin arbitraje de mariposa; segunda vía: deltas frente a SVI.
**Referencia ingenua.** RI-MH y RI-PA del sesgo.
**Aclaración y rechazo.** Rechazo con < 5 precios de ejercicio o con una superficie con arbitraje no corregible.
**Referencias.** Bakshi, Kapadia y Madan (2003), «Stock Return Characteristics, Skew Laws, and the Differential Pricing of Individual Equity Options», *RFS*; Bollen y Whaley (2004), «Does Net Buying Pressure Affect the Shape of Implied Volatility Functions?», *Journal of Finance*; Gatheral (2006), *The Volatility Surface*; Gatheral y Jacquier (2014), «Arbitrage-Free SVI Volatility Surfaces», *Quantitative Finance*; Kozhan, Neuberger y Schneider (2013), «The Skew Risk Premium in the Equity Index Market», *RFS* · TM-06.
**Prioridad y madurez.** P1 · IMPLEMENTADO (ejecutor, casos de control registrados (T-106)).

### DER-TERM-001 · Estructura de plazos de la volatilidad implícita

**Identificación.** v1.0 · VIGENTE · MC-09 · Mapa: áreas 66, 49.
**Perfiles y horizontes.** PERF-DER (+ PERF-TCV, PERF-IDX para eventos de índice) · H1–H3.
**Propósito.** ¿Cómo se reparte la volatilidad implícita entre vencimientos (pendiente, inversión, eventos descontados) y qué indica frente a su historia?
**Método.** (i) Curva ATM por vencimiento interpolada en varianza total w = σ²·T (lineal en T), con comprobación de no arbitraje de calendario (w no decreciente). (ii) Pendiente = σ(3m) − σ(1m); ratio σ(1m)/σ(3m); estado de inversión (ratio > 1). (iii) Volatilidad *forward* entre T₁ y T₂: σ_fwd = √[(σ₂²T₂ − σ₁²T₁)/(T₂ − T₁)]. (iv) Movimiento descontado de un evento fechado: varianza del evento = σ²_con·T_con − σ²_base·T_con (con σ_base de vencimientos que lo excluyen, supuesto declarado); movimiento esperado ≈ √(varianza del evento). (v) Percentil de la pendiente ≥ 3 años; frecuencia y duración históricas de las inversiones.
**Entradas mínimas.** σ ATM para ≥ 3 vencimientos, diaria ≥ 2 años; calendario de eventos.
**Parámetros.** vencimientos (1, 3, 6, 12 meses); interpolacion (varianza_total).
**Salidas.** TABLA: σ por vencimiento (%), pendiente (puntos), ratio, estado, σ_fwd (%), movimiento descontado del evento (%), percentiles. DETERMINISTA (*forward* y evento sobre supuestos) y ESTADISTICA (percentiles).
**Supuestos y limitaciones.** Varianza total decreciente ⇒ arbitraje de calendario (rechazo o corrección declarada); el movimiento del evento depende de la varianza base supuesta.
**Tolerancias y semilla.** 1e-10 · null.
**Verificación.** Curva plana ⇒ σ_fwd = σ; w monótona.
**Referencia ingenua.** RI-MH y RI-PA de la pendiente.
**Aclaración y rechazo.** Rechazo con < 3 vencimientos.
**Referencias.** Gatheral (2006); Mixon (2007), «The Implied Volatility Term Structure of Stock Index Options», *Journal of Empirical Finance*; Johnson (2017), «Risk Premia and the VIX Term Structure», *JFQA*; Dubinsky, Johannes, Kaeck y Seeger (2019), «Option Pricing of Earnings Announcement Risks», *RFS* · TM-06.
**Prioridad y madurez.** P1 · IMPLEMENTADO (ejecutor, casos de control registrados (T-106)).

### DER-ROLL-001 · Carry y roll de futuros financieros

**Identificación.** v1.0 · VIGENTE · MC-09 · Mapa: áreas 66, 49, 47.
**Perfiles y horizontes.** PERF-DER (+ PERF-TCV para futuros de tipos y de volatilidad, PERF-FX) · H1–H3.
**Propósito.** ¿Cuánto rinde o cuesta mantener una exposición en futuros sobre índices, bonos o divisas (base, carry implícito y roll), y está ese carry alto o bajo frente a su historia?
**Método.** (i) Base = F − S; carry implícito anualizado = ln(F/S)/T (índices: ≈ r − q; divisas: ≈ i_cotizada − i_base; bonos: rendimiento del entregable más barato − repo, con factor de conversión). (ii) Roll yield anualizado = (F_próximo/F_siguiente − 1)·365/días entre vencimientos. (iii) Base implícita frente a teórica: dividendos implícitos, repo implícito, base de divisas (pb). (iv) Percentil frente a ≥ 5 años. (v) Descomposición de la rentabilidad del futuro = spot + roll + colateral (análoga a CMD-RETDEC-001).
**Entradas mínimas.** Spot y ≥ 2 vencimientos con fechas; tipos; dividendos esperados o repo; para bonos, entregable más barato y factor de conversión.
**Parámetros.** anualizacion (365; 360 en mercados monetarios); pares (1–2).
**Salidas.** TABLA: base (puntos y %), carry implícito (% anual), roll yield (% anual), desviación frente al teórico (pb), percentiles, descomposición. DETERMINISTA y ESTADISTICA.
**Supuestos y limitaciones.** Opción de entrega en futuros de bonos; dividendos esperados inciertos; márgenes y liquidación diaria; el carry no es previsión.
**Tolerancias y semilla.** 1e-10 · null.
**Verificación.** F = S·e^{(r − q)T} ⇒ carry implícito = r − q; curva plana ⇒ roll 0; suma de componentes = total.
**Referencia ingenua.** RI-MH del carry y carry teórico.
**Aclaración y rechazo.** Rechazo con < 2 vencimientos o sin tipo de financiación.
**Referencias.** Koijen, Moskowitz, Pedersen y Vrugt (2018), «Carry», *JFE*; Burghardt, Belton, Lane y Papa (2005), *The Treasury Bond Basis*, 3.ª ed.; van Binsbergen, Brandt y Koijen (2012), «On the Timing and Pricing of Dividends», *AER*; Hull (2022) · TM-06.
**Prioridad y madurez.** P1 · IMPLEMENTADO (ejecutor, casos de control registrados (T-106)).

## 18. Fichas nuevas V5.0 — instrumentos monetarios y liquidez (PERF-MON)

Unidad de análisis: el segmento monetario por divisa y plazo. Ninguna ficha compara entidades, depósitos o fondos concretos (1.6).

### MON-YLD-001 · Rentabilidad equivalente y comparación de segmentos monetarios

**Identificación.** v1.0 · VIGENTE · MC-01 (MC-09 como módulo invitado para la cobertura de divisa) · Mapa: áreas 67, 2.
**Perfiles y horizontes.** PERF-MON (+ PERF-FX para la comparación cubierta) · H1 (limitado)–H3.
**Propósito.** ¿Qué rentabilidad comparable ofrecen los segmentos de liquidez (letras, depósitos negociables, certificados, pagarés, repos, categorías de fondos monetarios) por divisa y plazo, una vez homogeneizadas las convenciones?
**Método.** (i) Conversiones: tipo de descuento d → precio P = 1 − d·t/360 → rendimiento simple equivalente = (1/P − 1)·365/t y TAE = (1/P)^{365/t} − 1; *money market yield* Act/360 ↔ Act/365; tipo simple i a TAE = (1 + i·t/base)^{365/t} − 1. (ii) Diferenciales entre segmentos a igual plazo y divisa (pagarés − letras, depósitos − letras, categoría de fondos monetarios − €STR) en pb. (iii) Rendimiento cubierto en otra divisa = (1 + i_ext·t/base_ext)·(S/F) − 1, anualizado. (iv) Percentil de cada diferencial frente a ≥ 5 años.
**Entradas mínimas.** Tipos o precios por segmento, plazo, divisa y convención, con fecha; spot y *forwards* para la cobertura.
**Parámetros.** base_salida (TAE; Act/365); plazos (1, 3, 6, 12 meses); cobertura (false).
**Salidas.** TABLA: rendimiento equivalente por segmento y plazo (% TAE), diferenciales (pb), rendimiento cubierto (% TAE), percentiles. DETERMINISTA (conversiones) y ESTADISTICA (percentiles).
**Supuestos y limitaciones.** Los segmentos difieren en riesgo emisor, liquidez y protección (garantía de depósitos, garantía soberana): el diferencial no es gratuito; las categorías de fondos monetarios se miden por su rentabilidad media pasada neta de gastos; retenciones solo si se declaran. Sin costes ni condiciones de instrumentos concretos (1.6).
**Tolerancias y semilla.** 1e-10 · null.
**Verificación.** Ida y vuelta de cada conversión = identidad; t = 365 en base 365 ⇒ simple = TAE.
**Referencia ingenua.** €STR compuesto (8.4 del Documento 0) o su homólogo de la divisa; RI-PA.
**Aclaración y rechazo.** Aclaración si falta la convención; rechazo con plazos o divisas no alineables.
**Referencias.** Stigum y Crescenzi (2007), *Stigum's Money Market*, 4.ª ed.; Choudhry (2004), *The Money Markets Handbook*; Fabozzi (2012) · TM-05, TM-13.
**Prioridad y madurez.** P1 · IMPLEMENTADO (ejecutor, casos de control registrados (T-106)).

### MON-EXP-001 · Expectativas implícitas de tipos a corto

**Identificación.** v1.0 · VIGENTE · MC-09 · Mapa: áreas 67, 47, 19.
**Perfiles y horizontes.** PERF-MON (+ PERF-FIR, PERF-TCV, PERF-FX) · H1 (limitado: decisiones de bancos centrales)–H3.
**Propósito.** ¿Qué senda de tipos oficiales descuenta el mercado y qué probabilidad implícita asigna a cada decisión de las próximas reuniones?
**Método.** (i) Tipos *forward* de la curva OIS (€STR, SOFR, SONIA) o de futuros a 1 y 3 meses (tipo = 100 − precio; ajuste de convexidad en plazos > 1 año). (ii) Senda por reunión: tipo esperado tras la reunión k a partir de los *forwards* entre fechas de reunión, descontando el diferencial estable tipo oficial–tipo de mercado. (iii) Probabilidad implícita de un movimiento Δ = (tipo implícito tras la reunión − tipo vigente)/Δ, con ajuste por días del periodo. (iv) Cambio acumulado descontado a 6 y 12 meses (pb). (v) Sorpresa de cada decisión frente a la senda del día anterior.
**Entradas mínimas.** Curva OIS o futuros con ≥ 3 nodos en 12 meses y fechas; calendario de reuniones; tipo oficial y diferencial habitual tipo oficial–tipo de mercado.
**Parámetros.** incremento (25 pb); diferencial_estable (media de 20 días); convexidad (true para > 1 año).
**Salidas.** TABLA: senda por reunión (%), probabilidades por movimiento, cambio acumulado (pb), sorpresas (pb). DETERMINISTA (dada la curva) y ESTADISTICA (ajustes).
**Supuestos y limitaciones.** Los tipos implícitos incluyen una prima por plazo pequeña pero no nula; probabilidades neutrales al riesgo; el diferencial tipo oficial–mercado puede variar; el método de probabilidades binario es una simplificación.
**Tolerancias y semilla.** 1e-10 · null.
**Verificación.** Curva plana al tipo vigente ⇒ probabilidad de movimiento 0; la senda reproduce los *forwards* de entrada.
**Referencia ingenua.** RI-PA (tipo oficial sin cambios) y senda de encuesta si se aporta.
**Aclaración y rechazo.** Rechazo sin calendario de reuniones o con < 3 nodos en 12 meses.
**Referencias.** Kuttner (2001), «Monetary Policy Surprises and Interest Rates: Evidence from the Fed Funds Futures Market», *Journal of Monetary Economics*; Gürkaynak, Sack y Swanson (2005), «Do Actions Speak Louder Than Words? The Response of Asset Prices to Monetary Policy Actions and Statements», *International Journal of Central Banking*; Piazzesi y Swanson (2008), «Futures Prices as Risk-Adjusted Forecasts of Monetary Policy», *Journal of Monetary Economics*; CME Group, *CME FedWatch Tool: Methodology* · TM-05.
**Prioridad y madurez.** P1 · IMPLEMENTADO (ejecutor, casos de control registrados (T-106)).

### MON-REAL-001 · Rentabilidad real a corto plazo

**Identificación.** v1.0 · VIGENTE · MC-01 · Mapa: áreas 67, 2, 19.
**Perfiles y horizontes.** PERF-MON (+ PERF-FIR) · H2–H3.
**Propósito.** ¿Cuánto rinde la liquidez en términos reales, por divisa y plazo, ex ante y ex post, y dónde está frente a su historia?
**Método.** (i) Real ex ante = (1 + i)/(1 + π^e) − 1, con π^e de swaps de inflación a 1 año, encuestas o previsión declarada. (ii) Real ex post = (1 + i_{t−h})/(1 + π_{t−h→t}) − 1 con IPC en su vintage. (iii) Diferencial frente a una estimación publicada del tipo real neutral (dato externo con fuente). (iv) Rentabilidad real compuesta de una política de renovación a 3 meses. (v) Percentil frente a ≥ 20 años y diferencias entre divisas.
**Entradas mínimas.** Tipos por plazo; IPC con vintages; expectativas de inflación con fuente; ≥ 10 años (≥ 20 recomendados).
**Parámetros.** medida_inflacion (IPC armonizado o el índice de referencia del mercado); expectativa (swap_1a; encuesta); plazo (3 meses).
**Salidas.** TABLA y SERIE: real ex ante y ex post (%), diferencial frente al neutral (pp), percentiles. DETERMINISTA (aritmética) y ESTADISTICA (percentiles).
**Supuestos y limitaciones.** El swap de inflación incluye prima de riesgo; la inflación medida no es la de cada inversor; fiscalidad no incluida.
**Tolerancias y semilla.** 1e-10 · null.
**Verificación.** π = 0 ⇒ real = nominal; coherencia con FIN-CAGR-001.
**Referencia ingenua.** RI-MH del tipo real y RI-PA.
**Aclaración y rechazo.** Rechazo con inflación sin fuente o vintages incompatibles.
**Referencias.** Fisher (1930), *The Theory of Interest*; Laubach y Williams (2003), «Measuring the Natural Rate of Interest», *Review of Economics and Statistics*; Holston, Laubach y Williams (2017), «Measuring the Natural Rate of Interest: International Trends and Determinants», *Journal of International Economics*; Ang, Bekaert y Wei (2007), «Do Macro Variables, Asset Markets, or Surveys Forecast Inflation Better?», *Journal of Monetary Economics* · TM-04, TM-05.
**Prioridad y madurez.** P1 · IMPLEMENTADO (ejecutor, casos de control registrados (T-106)).

### MON-FIX-001 · Valor de fijar plazo frente a renovar

**Identificación.** v1.0 · VIGENTE · MC-09 · Mapa: áreas 67, 47.
**Perfiles y horizontes.** PERF-MON · H2–H3.
**Propósito.** ¿Compensa fijar hoy la rentabilidad a un plazo T frente a renovar a plazos cortos, dada la senda de tipos descontada, y cuánto tendrían que moverse los tipos para cambiar la respuesta?
**Método.** (i) Fijar: (1 + y_T·T/base). (ii) Renovar: Π(1 + f_k·τ/base) con los *forwards* de la curva (expectativas puras) y con escenarios declarados (senda de MON-EXP-001, senda plana, encuesta, ±50 y ±100 pb). (iii) Punto muerto: tipo medio constante de renovación que iguala ambas estrategias; holgura frente a la senda descontada (pb). (iv) Prima implícita a corto = punto muerto − media de la senda esperada por encuesta (si se aporta). (v) Tabla de resultados por escenario (o media ponderada si el solicitante aporta pesos).
**Entradas mínimas.** Tipos del mismo segmento por plazo (≥ 3 nodos hasta T) con convención; senda implícita o escenarios.
**Parámetros.** T (12 meses; 3–24); tau (3 meses; 1–6); escenarios (base, ±50, ±100 pb).
**Salidas.** TABLA: rentabilidad de fijar y de renovar por escenario (% TAE), punto muerto (%), holgura (pb), prima implícita (pb). DETERMINISTA.
**Supuestos y limitaciones.** Bajo expectativas puras ambas estrategias rinden igual: la diferencia mide prima por plazo o desacuerdo con el mercado; mismo segmento y riesgo emisor en ambos lados; riesgo de reinversión explícito.
**Tolerancias y semilla.** 1e-10 · null.
**Verificación.** Renovar con los *forwards* = fijar (identidad sin arbitraje); curva y senda planas ⇒ indiferencia.
**Referencia ingenua.** Renovar al tipo vigente (RI-PA).
**Aclaración y rechazo.** Rechazo con plazos o convenciones incompatibles.
**Referencias.** Fama (1984), «The Information in the Term Structure», *JFE*; Campbell y Shiller (1991), «Yield Spreads and Interest Rate Movements: A Bird's Eye View», *Review of Economic Studies*; Cochrane y Piazzesi (2005), «Bond Risk Premia», *AER*; Tuckman y Serrat (2011) · TM-05.
**Prioridad y madurez.** P1 · IMPLEMENTADO (ejecutor, casos de control registrados (T-106)).

## 19. Fichas nuevas V5.0 — tipos de interés, crédito y volatilidad (PERF-TCV)

Unidad de análisis: el factor (pendiente, prima por plazo, inflación implícita, diferencial agregado, volatilidad) y su indicador. Ninguna ficha compara contratos o productos concretos (1.6).

### TCV-SLOPE-001 · Pendiente de la curva y su valor razonable

**Identificación.** v1.0 · VIGENTE · MC-09 (MC-03 como módulo invitado para la regresión) · Mapa: áreas 68, 47.
**Perfiles y horizontes.** PERF-TCV (+ PERF-FIR; PERF-ACC como indicador de ciclo) · H1–H3 (H4 limitado).
**Propósito.** ¿Está la pendiente de la curva (2s10s, 5s30s, 3m10y) por encima o por debajo de lo que justifican el ciclo monetario, la inflación y la prima por plazo, y cuánto rinde una exposición neutral en duración al empinamiento?
**Método.** (i) Pendiente observada (pb). (ii) Valor razonable por regresión de la pendiente sobre el cambio esperado del tipo oficial a 1 año (MON-EXP-001), la brecha de producción o de desempleo, la inflación subyacente y la prima por plazo (TCV-TP-001), con errores HAC; residuo, z-score y percentil. (iii) Pendiente *forward* a 3 y 6 meses (lo que la curva ya descuenta) y punto muerto. (iv) Carry + rolldown de la exposición neutral en DV01 (FIR-CARRY-001 en ambos tramos). (v) Régimen de la curva (empinamiento o aplanamiento, alcista o bajista) por signos de los cambios de nivel y pendiente.
**Entradas mínimas.** Curva diaria o semanal ≥ 10 años con ≥ 6 nodos; variables macro con vintages.
**Parámetros.** tramos (2s10s); regresores (los indicados); ventana (20 años); horizonte_carry (3 meses).
**Salidas.** TABLA: pendiente (pb), valor razonable con IC (pb), residuo y z, pendiente *forward* (pb), carry neutral en DV01 (pb por 3 meses), régimen. ESTADISTICA.
**Supuestos y limitaciones.** Relaciones inestables entre regímenes monetarios (compras de activos, control de curva); la pendiente *forward* implica que el carry ya descuenta la reversión bajo expectativas; la inversión de la curva no es predictor fiable de mercados en H1–H2.
**Tolerancias y semilla.** 1e-8 · null.
**Verificación.** Curva plana ⇒ pendiente 0 y rolldown 0; segunda vía: β₁ de NSS (FIR-CURVE-001) frente a la pendiente directa.
**Referencia ingenua.** RI-PA de la pendiente y pendiente *forward*.
**Aclaración y rechazo.** Rechazo con < 6 nodos o < 5 años.
**Referencias.** Litterman y Scheinkman (1991), «Common Factors Affecting Bond Returns», *Journal of Fixed Income*; Estrella y Mishkin (1998), *Review of Economics and Statistics*; Diebold, Rudebusch y Aruoba (2006), «The Macroeconomy and the Yield Curve: A Dynamic Latent Factor Approach», *Journal of Econometrics*; Engstrom y Sharpe (2019), «The Near-Term Forward Yield Spread as a Leading Indicator», *FAJ*; Koijen et al. (2018) · TM-05.
**Prioridad y madurez.** P1 · IMPLEMENTADO (ejecutor, casos de control registrados (T-106)).

### TCV-BEI-001 · Inflación implícita frente a esperada

**Identificación.** v1.0 · VIGENTE · MC-09 · Mapa: áreas 68, 46, 19.
**Perfiles y horizontes.** PERF-TCV (+ PERF-FIR, PERF-REI como contexto de tipos reales) · H2–H3 (H4 limitado).
**Propósito.** ¿Cuánta inflación descuentan los bonos ligados y los swaps de inflación, en qué difiere de la inflación esperada por encuestas y modelos, y qué parte puede atribuirse a primas de riesgo y de liquidez?
**Método.** (i) Breakeven = rendimiento nominal − real a igual vencimiento (interpolado), con ajuste de estacionalidad del índice en plazos < 3 años y del retardo de indexación. (ii) Breakeven *forward* 5y5y = [(1 + BE₁₀)^{10}/(1 + BE₅)^{5}]^{1/5} − 1. (iii) Swap de inflación como segunda vía; base swap − bono como aproximación a la prima de liquidez de los ligados. (iv) Brecha frente a encuestas a igual horizonte. (v) Descomposición con un modelo afín de curvas nominal y real si el solicitante aporta su salida (dato con fuente). (vi) Percentil y z-score frente a ≥ 10 años; carry de inflación a corto (inflación devengada esperada frente al breakeven).
**Entradas mínimas.** Curvas nominal y real (o swaps de inflación) con ≥ 3 vencimientos reales; índice de referencia y su estacionalidad; encuestas con fecha.
**Parámetros.** plazos (2, 5, 10 años; 5y5y); ajuste_estacional (true para < 3 años).
**Salidas.** TABLA: breakevens (%), 5y5y (%), base swap−bono (pb), brecha frente a encuestas (pb), percentiles, carry de inflación (pb). DETERMINISTA y ESTADISTICA.
**Supuestos y limitaciones.** Breakeven ≠ inflación esperada (prima de inflación, prima de liquidez y suelo de deflación en ligados); estacionalidad decisiva a corto; índice de referencia propio de cada mercado.
**Tolerancias y semilla.** 1e-10 · null.
**Verificación.** Nominal = real ⇒ BE = 0; 5y5y coherente con los breakevens al contado.
**Referencia ingenua.** Encuesta (inflación esperada) y RI-PA del breakeven.
**Aclaración y rechazo.** Rechazo con índices de referencia distintos sin conversión o con < 3 vencimientos reales.
**Referencias.** Gürkaynak, Sack y Wright (2010), «The TIPS Yield Curve and Inflation Compensation», *American Economic Journal: Macroeconomics*; Fleckenstein, Longstaff y Lustig (2014), «The TIPS-Treasury Bond Puzzle», *Journal of Finance*; Abrahams, Adrian, Crump, Moench y Yu (2016), «Decomposing Real and Nominal Yield Curves», *Journal of Monetary Economics*; D'Amico, Kim y Wei (2018), «Tips from TIPS: The Informational Content of Treasury Inflation-Protected Security Prices», *JFQA* · TM-05.
**Prioridad y madurez.** P1 · IMPLEMENTADO (ejecutor, casos de control registrados (T-106)).

### TCV-CDS-001 · Diferencial de índice CDS frente a pérdidas esperadas

**Identificación.** v1.0 · VIGENTE · MC-09 · Mapa: áreas 68, 48.
**Perfiles y horizontes.** PERF-TCV (+ PERF-FIR) · H2–H3 (H4 limitado).
**Propósito.** ¿Compensa el diferencial de un índice de CDS (IG, HY, por región) las pérdidas por impago esperadas, y dónde está su prima de riesgo frente a su historia y frente al crédito al contado?
**Método.** (i) Intensidad de impago neutral al riesgo λ ≈ s/(1 − R). (ii) Pérdida esperada real = PD histórica por rating medio y fase del ciclo (o tasa de impago prevista aportada) × (1 − R). (iii) Prima de riesgo de crédito = s − pérdida esperada (pb) y ratio s/pérdida esperada. (iv) Percentil del diferencial ≥ 10 años sobre la serie *on-the-run* con enlace entre series declarado. (v) Base CDS–contado = diferencial del índice − diferencial al contado comparable (OAS o Z). (vi) Pendiente 5–10 años; carry + roll-down del índice; DV01 de diferencial (*risky duration*).
**Entradas mínimas.** Diferencial diario del índice con serie y versión; recuperación supuesta; tasas de impago por rating y año con fuente; diferencial al contado comparable; ≥ 5 años.
**Parámetros.** recuperacion (0,40 IG; 0,25–0,40 HY); fuente_impagos (declarada); ventana (≥ 10 años; 5 con limitación).
**Salidas.** TABLA: diferencial (pb), λ (% anual), pérdida esperada (pb), prima (pb y ratio), percentil, base (pb), pendiente (pb), carry (pb anuales), DV01. ESTADISTICA.
**Supuestos y limitaciones.** Cambios de composición entre series; índices HY cotizados en precio (conversión declarada); recuperación supuesta; cupón estándar con pago inicial.
**Tolerancias y semilla.** 1e-8 · null.
**Verificación.** s = PD·(1 − R) ⇒ prima 0; percentil del máximo histórico = 1.
**Referencia ingenua.** RI-MH y RI-PA del diferencial.
**Aclaración y rechazo.** Rechazo sin serie y versión del índice o con < 5 años.
**Referencias.** Elton, Gruber, Agrawal y Mann (2001), *Journal of Finance*; Hull, Predescu y White (2004), «The Relationship between Credit Default Swap Spreads, Bond Yields, and Credit Rating Announcements», *Journal of Banking & Finance*; Longstaff, Mithal y Neis (2005), «Corporate Yield Spreads: Default Risk or Liquidity? New Evidence from the Credit Default Swap Market», *Journal of Finance*; Berndt, Douglas, Duffie y Ferguson (2018), «Corporate Credit Risk Premia», *Review of Finance* · TM-05.
**Prioridad y madurez.** P1 · IMPLEMENTADO (ejecutor, casos de control registrados (T-106)).

### TCV-VIXTS-001 · Estructura de plazos del VIX y roll de sus futuros

**Identificación.** v1.0 · VIGENTE · MC-09 (MC-02 como módulo invitado) · Mapa: áreas 68, 66, 49.
**Perfiles y horizontes.** PERF-TCV (+ PERF-DER) · H1–H3.
**Propósito.** ¿En qué estado está la estructura de plazos de los índices de volatilidad (VIX, VSTOXX, MOVE) y de sus futuros, y cuánto rinde o cuesta mantener una exposición larga o corta a la volatilidad por el roll?
**Método.** (i) Curva de futuros por vencimiento; estado: contango (F₂ > F₁ > spot) o *backwardation*. (ii) Ratios de la curva del índice (p. ej., VIX/VIX3M). (iii) Roll diario implícito del primer futuro = (F₁ − spot)/días al vencimiento (puntos y %). (iv) Rentabilidad esperada de la exposición a vencimiento constante de 30 días si la curva no cambia. (v) Percentil de la pendiente ≥ 5 años; frecuencia histórica de contango; rentabilidades históricas de exposiciones largas y cortas por estado (descriptivo); ES de la exposición corta.
**Entradas mínimas.** Índice spot y ≥ 2 vencimientos de futuros diarios ≥ 3 años; calendario de vencimientos.
**Parámetros.** vencimiento_constante (30 días); ventana_percentil (5 años).
**Salidas.** TABLA: curva (puntos), estado, ratios, roll (puntos por día y % mensual), percentiles, rentabilidades por estado (%), ES de la exposición corta (%). DETERMINISTA y ESTADISTICA.
**Supuestos y limitaciones.** El spot del índice de volatilidad no es invertible; el futuro converge al valor de liquidación en el vencimiento; contango habitual con saltos extremos; las estructuras que mantienen futuros de volatilidad sufren decaimiento (FON-LEV-001 si están apalancadas).
**Tolerancias y semilla.** 1e-10 · null.
**Verificación.** Curva plana igual al spot ⇒ roll 0; interpolación a 30 días coherente entre los dos contratos.
**Referencia ingenua.** RI-MH de la pendiente y RI-PA del índice.
**Aclaración y rechazo.** Rechazo con < 2 vencimientos.
**Referencias.** Whaley (2009), «Understanding the VIX», *JPM*; Simon y Campasano (2014), «The VIX Futures Basis: Evidence and Trading Strategies», *Journal of Derivatives*; Eraker y Wu (2017), «Explaining the Negative Returns to Volatility Claims: An Equilibrium Approach», *JFE*; Johnson (2017), *JFQA*; Cboe, *VIX White Paper* · TM-06.
**Prioridad y madurez.** P1 · IMPLEMENTADO (ejecutor, casos de control registrados (T-106)).

### TCV-TP-001 · Prima por plazo

**Identificación.** v1.0 · VIGENTE · MC-09 (MC-03 como módulo invitado para el VAR) · Mapa: áreas 68, 47.
**Perfiles y horizontes.** PERF-TCV (+ PERF-FIR, PERF-MON) · H3 (H2 contexto; H4 limitado).
**Propósito.** ¿Qué parte del rendimiento a largo plazo es compensación por riesgo de duración (prima por plazo) y qué parte es la senda esperada de tipos cortos, y está esa prima alta o baja frente a su historia?
**Método.** (i) Modelo afín de regresiones lineales (Adrian-Crump-Moench): componentes principales (5) de la curva cupón cero mensual; VAR(1) de los factores; regresión de excesos de rentabilidad a 1 mes sobre factores rezagados e innovaciones; precios de riesgo λ₀ y λ₁; recursiones de precios. (ii) Prima por plazo = rendimiento ajustado − rendimiento neutral al riesgo, a 2, 5 y 10 años. (iii) Alternativas: series publicadas (ACM, Kim-Wright) como dato con fuente, o aproximación por encuestas (rendimiento a 10 años − media de tipos cortos esperados a 10 años). (iv) Percentil ≥ 20 años; descomposición de los cambios recientes del rendimiento en senda esperada y prima.
**Entradas mínimas.** Curva cupón cero mensual ≥ 20 años (≥ 10 con limitación) con vencimientos de 1 a 10 años; o series publicadas con fecha.
**Parámetros.** n_factores (5; 3–5); metodo (ACM; publicado; encuesta); ventana (toda la disponible).
**Salidas.** TABLA: prima por plazo a 2, 5 y 10 años (pb), rendimiento neutral al riesgo (%), percentiles, descomposición de cambios (pb); SERIE histórica. ESTADISTICA.
**Supuestos y limitaciones.** Dependencia del modelo (las estimaciones de distintos modelos pueden diferir más de 50 pb); sesgo de muestra finita en el VAR (persistencia infraestimada); la prima no es observable.
**Tolerancias y semilla.** 1e-6 en parámetros · null.
**Verificación.** Prima + rendimiento neutral = rendimiento ajustado; error de ajuste de la curva < 5 pb; segunda vía: serie publicada o aproximación por encuestas.
**Referencia ingenua.** RI-MH de la prima y RI-PA.
**Aclaración y rechazo.** Rechazo con < 10 años de curva mensual.
**Referencias.** Adrian, Crump y Moench (2013), «Pricing the Term Structure with Linear Regressions», *JFE*; Kim y Wright (2005), «An Arbitrage-Free Three-Factor Term Structure Model and the Recent Behavior of Long-Term Yields and Distant-Horizon Forward Rates», FEDS 2005-33; Cochrane y Piazzesi (2005), *AER*; Gürkaynak, Sack y Wright (2007), *Journal of Monetary Economics*; Bauer, Rudebusch y Wu (2012), «Correcting Estimation Bias in Dynamic Term Structure Models», *JBES* · TM-05.
**Prioridad y madurez.** P1 · IMPLEMENTADO (ejecutor, casos de control registrados (T-106)).

## 20. Pruebas de regresión y casos de control

1. Cada ficha declara sus casos de control (sección «Verificación»). Tras cada cambio de versión de método o de ficha, el módulo responsable los ejecuta y MC-08 verifica una muestra en la verificación periódica; un fallo devuelve la ficha a `EN_REVISION` y se notifica al operador.
2. **Paso a IMPLEMENTADO**: casos de control superados en el entorno de ejecución y registrados en el Registro de cálculos.
3. **Paso a VALIDADO**: pruebas de `09_Pruebas` ejecutadas con evidencia (incluidas pruebas con datos reales de cada tipo de activo, datos insuficientes y ámbitos híbridos).
4. **SCORE-RK-001** se prueba contra HT-03 con el conjunto común de casos de `10_Herramientas`; cualquier diferencia bloquea ambas hasta su resolución.
5. **FC-EVAL-001 y FC-CAL-001** se prueban con pronosticadores sintéticos de propiedades conocidas (perfectamente calibrado, sobreconfiado, sin resolución) para comprobar que las métricas y sus nulos se comportan como se espera antes de usarse en certificados (R13).
6. **Frontera con el Bloque B** (1.6): la batería incluye, para cada familia IDX, FON, DER, MON y TCV, una petición que pretende ordenar instrumentos concretos y que debe rechazarse con `FUERA_DE_CATALOGO` y la ficha de ámbito más próxima.
7. **SCORE-RK-001** se reverifica contra HT-03 con los pesos de A vigentes en V5.0 (asimetría 30, valoración del ámbito 25, catalizadores 15, momento 15, profundidad e invertibilidad del universo 15) antes de mantener su estado IMPLEMENTADO.
