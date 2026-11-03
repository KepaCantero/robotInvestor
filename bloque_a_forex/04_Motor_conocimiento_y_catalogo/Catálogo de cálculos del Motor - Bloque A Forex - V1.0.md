# Catálogo — Catálogo de cálculos del Motor de Cálculo Avanzado (Forex) (AG-13)

**Bloque A Forex · Robot Investor · Versión óptima V1.0 · 02/11/2026** · Subordinado al Documento 0 del Bloque A Forex V1.0.

Archivo CC (propietario: operador, por cambio de tipo 3; el Motor propone). Lectores: AG-13 y sus módulos, AG-15, Analistas de segmento (AG-03 a AG-08), Analistas transversales (AG-09, AG-21), Orquestador técnico. `catalog_version` FX-1.0. Deriva del Catálogo de cálculos del Motor V5.0 del Bloque A general, que sigue vigente en ese bloque y no se modifica.

---

## 1. Propósito y reglas de uso

1.1. El catálogo especifica, operación a operación, **qué calcula el Motor, con qué datos mínimos, con qué convenciones, con qué supuestos, con qué tolerancias y contra qué referencia ingenua se compara**. Cada servicio CT-09 cita en su campo `operacion` un `ficha_id` y su versión; cada re-ejecución CT-10 usa la ficha y la versión citadas en el artefacto original.

1.2. **Cobertura no es obligación.** El catálogo define lo que el Motor sabe tratar; los métodos se activan bajo demanda, cuando pueden cambiar una decisión (R15, 7.5 del Documento 0). Ninguna investigación ejecuta todo el catálogo.

1.3. **Estado de gobierno y madurez.** Cada ficha tiene un estado de gobierno (`VIGENTE`, `EN_REVISION`, `DEPRECADA`, `BORRADOR`) y un estado de madurez (R22):

| Madurez | Significado | Uso permitido |
|---|---|---|
| DOCUMENTADO | Especificación publicada; sin implementación verificada en el entorno de ejecución | El Motor no entrega cifras citables con ella: responde `RECHAZADO` con motivo `METODO_NO_IMPLEMENTADO` y, si existe, ofrece la alternativa implementada que declara la ficha, con la limitación declarada |
| IMPLEMENTADO | Disponible en el entorno de ejecución y con casos de control superados | Servicio normal; la entrega declara «implementado, no validado» |
| VALIDADO | Batería de pruebas de `09_Pruebas` ejecutada con evidencia registrada | Servicio normal sin advertencia de madurez |

Estado de las 60 fichas de esta versión: 16 **IMPLEMENTADO** y reverificadas con pruebas unitarias en el ejecutor `bloque_a_forex` V1.0 (02/11/2026): las 12 del núcleo heredado del ejecutor V1.0 del Bloque A general (ST-DESC-001, FIN-CAGR-001, FX-TREND-001, FX-VOL-001, VOL-GARCH-001, FX-CORR-001, ML-CLUS-001, FC-EVAL-001, FC-CAL-001, SCORE-RK-001 v2.0, RISK-DD-001 v2.0 y FX-CARRY-001 v2.0) y 4 cambiarias nuevas (FX-FWD-001, FX-PPP-001, FX-MOM-001 y FX-RW-001); 6 de ellas solo en parte (ML-CLUS-001, FX-CARRY-001, FX-FWD-001, FX-PPP-001, FX-MOM-001 y FX-RW-001: los pasos no implementados siguen DOCUMENTADO y se indican en cada ficha); 11 **Implementado (heredado)** de la línea V3.0 (incluida FX-PPA-001, deprecada); 33 **DOCUMENTADO** (25 fichas cambiarias nuevas y 8 transversales). Ninguna ficha está VALIDADA.

1.4. **Cambios.** Alta, modificación o deprecación de fichas: propuesta del Motor (evidencia de uso del Registro de cálculos, casos de control, impacto) y aprobación del operador (tipo 3). Las versiones no se sobrescriben: conviven para permitir re-ejecuciones exactas. Los identificadores son inmutables: las fichas transversales heredadas con prefijo histórico `FX-` (FX-TREND-001, FX-BRK-001, FX-STL-001, FX-VOL-001, FX-REGIME-001, FX-COINT-001, FX-CORR-001) conservan su ID aunque no son específicas de divisas; las fichas cambiarias se reconocen por su familia (FX-CONV, FX-FWD, FX-CIP…) y por su perfil.

1.5. **Operaciones sin ficha.** Una operación que ninguna ficha cubre se rechaza con motivo y la ficha más próxima; si el solicitante necesita un cálculo exploratorio no citable, el Motor puede servirlo con la marca `op_sin_ficha` y `clase_cifra` ESTADISTICA, que impide su uso como cifra de un entregable (PS8, G3).

1.6. **Frontera con el Bloque B** (2.5 del Documento 0). Toda ficha opera sobre **ámbitos cambiarios** (par, cruce, cesta, bloque, estrategia, régimen) y sus **indicadores de seguimiento** (tipo de cambio del par según BCE, Fed H.10 o WM/Reuters; índice de la cesta; tipo efectivo del BPI; índice de estrategia). Los contratos genéricos (forward a plazo constante, opción ATM o de 25 delta a 1 o 3 meses, NDF a 1 mes) solo entran como **lectura del mercado del ámbito**. Ninguna ficha compara, ordena ni selecciona instrumentos (contado, forward, futuro, opción, ETF/ETC, CFD), proveedores, costes de ejecución, apalancamiento, tamaño ni niveles de entrada: una petición con ese propósito se rechaza con `FUERA_DE_CATALOGO` y la ficha de ámbito más próxima.

1.7. **Convención cambiaria** (M17 del Motor). Toda ficha cambiaria recibe y entrega el par en notación de mercado BASE/COTIZADA, la dirección referida a la base (`ALCISTA_BASE`/`BAJISTA_BASE`), la medida (`PRECIO_CONTADO`, `RENTABILIDAD_TOTAL` o, en ámbitos de volatilidad, `NIVEL_VOLATILIDAD`; `tipo_rentabilidad` del Documento 0, 2.4) y, en cestas, la composición, los pesos y la divisa de financiación. La ausencia de cualquiera de ellos es `ACLARACION_REQUERIDA`.

## 2. Ficha estándar

Toda ficha contiene, en este orden:

| # | Campo | Contenido |
|---|---|---|
| 1 | Identificación | `ficha_id` (FAM-NOMBRE-NNN), versión, estado de gobierno, módulo responsable (MC-01…MC-10) y módulo invitado si lo hay, áreas del Mapa de conocimientos |
| 2 | Perfiles y horizontes | Perfiles compatibles (PERF-FX-G10, PERF-FX-EM, PERF-FX-FACT o TRANSVERSAL = los tres) y horizontes H1–H4 en los que el método es informativo, respetando 8.3 del Documento 0 |
| 3 | Propósito | Pregunta cuantitativa que responde, en una frase |
| 4 | Método | Pasos y fórmulas esenciales; opciones declaradas |
| 5 | Entradas mínimas | Tipo, unidad, convención, longitud y frecuencia mínimas; conocibilidad |
| 6 | Parámetros y rangos | Nombre, valor por defecto, rango admitido |
| 7 | Salidas con unidades | Forma (VALOR, TABLA, SERIE, DISTRIBUCION), contenido, unidades, clase de cifra (DETERMINISTA o ESTADISTICA) |
| 8 | Supuestos y limitaciones | Condiciones de validez y advertencias obligatorias de entrega |
| 9 | Tolerancias y semilla | Tolerancia de re-ejecución (CT-10); semilla `null` o regla de semilla |
| 10 | Verificación interna | Identidades, casos de control, segunda vía |
| 11 | Referencia ingenua | Comparación obligatoria cuando el resultado se usa como previsión o señal (códigos de 3.3) |
| 12 | Aclaración y rechazo | Cuándo se pide aclaración y cuándo se rechaza |
| 13 | Referencias canónicas | Autor, año, título; temática TMX- de F8 para que el Documentador para el Motor mantenga el respaldo |
| 14 | Prioridad y madurez | P0/P1/P2 y DOCUMENTADO/IMPLEMENTADO/VALIDADO; alternativa implementada si está documentada |

## 3. Convenciones comunes (se aplican a todas las fichas salvo que la ficha diga otra cosa)

### 3.1 Convenciones numéricas, cambiarias y de servicio

- **Servicios técnicos**: toda ficha usa STC-1 (validación, calidad de datos y normalización de convenciones), STC-2 (ejecución numérica, aritmética decimal, semillas), STC-3 (métodos y fichas versionadas) y STC-4 (artefacto y linaje). No se repite en cada ficha.
- **Tipo de cambio**: `S` en unidades de cotizada por unidad de base; pip 0,0001 (0,01 con JPY como cotizada; escala de la fuente en pares de varias cifras enteras, declarada).
- **Fuente y corte**: serie de cierre de Nueva York (17:00) por defecto para series diarias de mercado; referencia del BCE o Fed H.10 cuando el indicador de seguimiento lo exige; WM/Reuters 16:00 de Londres para índices y backtests que lo usen. Nunca se mezclan cortes sin sincronización declarada.
- **Fechas valor**: contado T+2 (T+1 en USD/CAD, USD/TRY y USD/PHP); calendario de festivos de las dos plazas y de EE. UU.; vencimientos forward con día hábil siguiente modificado y regla de fin de mes.
- **Tipos de interés**: OIS a un día de cada divisa (SOFR, €STR, TONA, SONIA, SARON, CORRA, AONIA, SWESTR, NOWA; NZD con el OCR o el BKBM) o tipos implícitos en los puntos forward, declarados; bases Act/360 (USD, EUR, JPY, CHF, SEK, NOK, DKK, MXN), Act/365 (GBP, AUD, NZD, CAD, HKD, SGD, ZAR, PLN, ILS, INR) y Bus/252 (BRL).
- **Rendimientos** simples por defecto; logarítmicos solo si la ficha lo pide, etiquetados. **Anualización**: `m` = observaciones medias por año de la serie, declarado (≈ 260 en series NY 17:00; ≈ 255 en las del BCE; 252 si la ficha lo fija); volatilidad de opciones en días naturales/365. **Redondeo**: de banquero, solo al final; 4 decimales por defecto, 6 en tipos de cambio y puntos forward.
- **Divisa de valoración**: la de la petición; por defecto, la cotizada del par y, para el informe del usuario, la divisa base del usuario de F10 (EUR).
- **Conocibilidad**: todo dato lleva `conocible_desde` (CFTC: viernes de publicación; macro: fecha de publicación del vintage; fijaciones: hora de publicación); en evaluaciones y backtests nada posterior a la fecha de corte entra en el cálculo.
- **Verificación**: doble pasada independiente siempre; segunda vía recomendada en PLAN_STD y obligatoria en PLAN_EXT y en cifras en banda marginal (PS8).
- **Planes**: PLAN_MIN (una operación, verificación estándar), PLAN_STD (cadena, segunda vía si la ficha la declara, sensibilidad básica), PLAN_EXT (contraste multivía, sensibilidad por escenarios, propagación de incertidumbre). Los cálculos por defecto de cada plan y segmento están en los Perfiles cambiarios.

### 3.2 Tolerancias por defecto (si la ficha no fija otra)

| Tipo de cálculo | Tolerancia |
|---|---|
| Aritmética determinista (conversiones, puntos forward, índices) | 1e-10 relativa |
| Fórmulas cerradas (Garman-Kohlhagen, CIP) | 1e-8 relativa |
| Estimadores iterativos (GARCH, DOLS, volatilidad implícita, ajuste de sonrisa) | 1e-6 relativa en parámetros |
| Simulación o bootstrap con la misma semilla | 1e-6 relativa |
| Fechas valor, etiquetas, decisiones de contraste, clases de riesgo | Igualdad exacta |

### 3.3 Referencias ingenuas (códigos)

| Código | Referencia | Uso típico |
|---|---|---|
| RI-PA | Paseo aleatorio sin deriva (último valor conocido en t); en forma probabilística, distribución lognormal sin deriva centrada en el contado con la volatilidad EWMA o realizada conocida en t | Nivel y dirección de tipos de cambio, diferenciales, tipos reales; probabilidades de umbral |
| RI-FWD | Forward como predictor (`F_{t,h}` o NDF al horizonte); en rentabilidad total, exceso de rentabilidad nulo; en forma probabilística, la misma distribución centrada en el forward | Nivel con forward líquido; rentabilidad total; carry |
| RI-SEG | Referencia de comparación del segmento (8.4 del Documento 0, ratificada en F10): G10N y G10M, rentabilidad en exceso nula; EMAS, EMLA y EMEA, cesta equiponderada de divisas emergentes del segmento frente al USD con carry; ESTR, índice de la estrategia equivalente o rentabilidad nula | Rentabilidad de opciones del top-3 y de estrategias |
| RI-MH | Media histórica conocida en t | Rendimientos esperados, valoraciones con reversión |
| RI-TB | Tasa base expansiva (frecuencia histórica del suceso conocida en t) | Dirección, probabilidad de superar umbral (complemento de RI-PA) |
| RI-EST | Estacional ingenua (mismo periodo del ciclo anterior o media estacional) | Flujos de fin de mes o de año, series con estacionalidad |
| RI-CLI | Climatología (distribución incondicional histórica conocida en t) | Probabilidades y distribuciones |
| RI-EWMA | Volatilidad EWMA (λ = 0,94) | Previsiones de volatilidad |
| RI-NA | No aplica (cálculo determinista o descriptivo, no es previsión) | Conversiones, puntos forward, puntuaciones |

RI-PA y, cuando existe forward o NDF líquido, RI-FWD son **obligatorias** en todo pronóstico de nivel, dirección o rentabilidad total (Anexo A); las demás se añaden cuando la ficha lo indica.

### 3.4 Prioridades

**P0** núcleo transversal y cambiario imprescindible para el funcionamiento del bloque (incluye todo lo que exigen R7, R13, G3, la convención cambiaria y la comparación con el paseo aleatorio); **P1** métodos cambiarios con datos accesibles y alto uso en el cribado y la investigación; **P2** ampliación (datos especializados o uso ocasional).

## 4. Índice de fichas

| ficha_id | Nombre | Módulo | Perfiles | Horizontes | Prioridad | Madurez |
|---|---|---|---|---|---|---|
| FX-TREND-001 | Detección y medición de tendencia | MC-02 | TRANSVERSAL | H2–H4 | P0 | IMPLEMENTADO (ejecutor V1.0) |
| FX-BRK-001 | Rupturas estructurales | MC-02 | TRANSVERSAL | H2–H4 | P0 | Implementado (heredado) |
| FX-STL-001 | Descomposición tendencia-ciclo-estacionalidad | MC-02 | TRANSVERSAL | H2–H4 | P1 | Implementado (heredado) |
| FX-VOL-001 | Volatilidad realizada e implícita y su brecha | MC-02 | TRANSVERSAL | H1–H3 | P0 | IMPLEMENTADO (ejecutor V1.0) |
| FX-REGIME-001 | Regímenes univariantes (Markov switching) | MC-02 | TRANSVERSAL | H2–H4 | P0 | Implementado (heredado) |
| FX-COINT-001 | Cointegración y corrección de errores | MC-03 | TRANSVERSAL | H3–H4 | P1 | Implementado (heredado) |
| FX-CORR-001 | Correlación dinámica y dependencia de cola | MC-03 | TRANSVERSAL | H1–H4 | P0 | IMPLEMENTADO (ejecutor V1.0) |
| ST-DESC-001 | Estadística descriptiva y momentos | MC-01 | TRANSVERSAL | — | P0 | IMPLEMENTADO (ejecutor V1.0) |
| ST-INF-001 | Contrastes, intervalos y comparaciones múltiples | MC-01 | TRANSVERSAL | — | P0 | Implementado (heredado) |
| FIN-CAGR-001 | Crecimiento, anualización y nominal/real | MC-01 | TRANSVERSAL | — | P0 | IMPLEMENTADO (ejecutor V1.0) |
| BIB-MET-001 | Bibliometría aplicada a fuentes | MC-01 | TRANSVERSAL | — | P1 | Implementado (heredado) |
| SIM-MC-001 | Simulación Monte Carlo de trayectorias | MC-05 | TRANSVERSAL | H1–H4 | P0 | Implementado (heredado) |
| RISK-VAR-001 | VaR y Expected Shortfall | MC-07 | TRANSVERSAL | H1–H3 | P0 | Implementado (heredado) |
| ML-CAL-001 | Evaluación interna de modelos predictivos | MC-06 | TRANSVERSAL | H1–H4 | P0 | Implementado (heredado) |
| AUD-REX-001 | Re-ejecución independiente (CT-10) | MC-08 | TRANSVERSAL | — | P0 | Implementado (heredado) |
| FC-CAL-001 | Calibración y fiabilidad | MC-10 | TRANSVERSAL | H1–H4 | P0 | IMPLEMENTADO (ejecutor V1.0) |
| BT-DSR-001 | Sharpe probabilístico y Deflated Sharpe | MC-10 | TRANSVERSAL | H2–H4 | P0 | DOCUMENTADO |
| BT-PBO-001 | Probabilidad de sobreajuste del backtest (CSCV) | MC-10 | TRANSVERSAL | H2–H4 | P1 | DOCUMENTADO |
| BT-VAR-001 | Backtesting de VaR y ES | MC-10 | TRANSVERSAL | H1–H2 | P1 | DOCUMENTADO |
| VOL-GARCH-001 | Volatilidad condicional GARCH | MC-02 | TRANSVERSAL | H1–H2 (H3 limitado) | P0 | IMPLEMENTADO (ejecutor V1.0) |
| ML-PRED-001 | Modelo predictivo supervisado con walk-forward | MC-06 | TRANSVERSAL | H1–H3 | P1 | DOCUMENTADO |
| DEC-VOI-001 | Valor de la información de un cálculo o búsqueda | MC-07 | TRANSVERSAL | — | P1 | DOCUMENTADO |
| SCORE-RK-001 | Puntuaciones T/E/M/P/A (pesos FX) y clave RK (idéntico a HT-03) | MC-01 | TRANSVERSAL | — | P0 | v2.0: IMPLEMENTADO (ejecutor `bloque_a_forex` V1.0; pesos de A Forex reverificados contra HT-03) |
| FC-EVAL-001 | Evaluación de pronósticos: Brier, log-score, CRPS, acierto, DM-HLN | MC-10 | TRANSVERSAL | H1–H4 | P0 | IMPLEMENTADO (ejecutor V1.0) |
| SCN-H-001 | Escenarios por horizonte (indicador cambiario) | MC-05 | TRANSVERSAL | H1–H4 (según 8.3) | P0 | DOCUMENTADO |
| REG-HMM-001 | Régimen cambiario y de riesgo (HMM multivariante) | MC-02 | TRANSVERSAL | H2–H3 | P1 | DOCUMENTADO |
| ML-CLUS-001 | Clústeres de exposición, apuestas independientes y exposición por divisa | MC-06 | TRANSVERSAL | — | P0 | IMPLEMENTADO (ejecutor V1.0; exposición por divisa v2.0 DOCUMENTADO) |
| RISK-DD-001 | Drawdown, liquidez y escala de riesgo 1–5 (umbrales cambiarios) | MC-07 | TRANSVERSAL | H2–H4 | P0 | v2.0: IMPLEMENTADO (ejecutor `bloque_a_forex` V1.0; umbrales cambiarios, ajustes y suelo con casos de control) |
| MON-EXP-001 | Expectativas implícitas de tipos a corto por reunión | MC-09 | PERF-FX-G10, PERF-FX-EM | H1 (limitado)–H3 | P1 | DOCUMENTADO |
| FX-CONV-001 | Convenciones de cotización, inversión y cruces sintéticos | MC-01 | TRANSVERSAL | — | P0 | DOCUMENTADO |
| FX-SETL-001 | Fechas valor y calendario de liquidación | MC-01 | TRANSVERSAL | — | P0 | DOCUMENTADO |
| FX-FWD-001 | Puntos forward, *outright* y carry implícito | MC-01 (+ MC-09) | TRANSVERSAL | H1–H3 | P0 | IMPLEMENTADO (ejecutor `bloque_a_forex` V1.0, pasos ii–iv); curva de plazos y tom-next, DOCUMENTADO |
| FX-TR-001 | Rentabilidad total cambiaria y exceso de rentabilidad | MC-01 | TRANSVERSAL | H1–H4 | P0 | DOCUMENTADO |
| FX-CARRY-001 | Diferencial de tipos, carry y carry ajustado por volatilidad | MC-03 | TRANSVERSAL | H1–H3 | P0 | v2.0: IMPLEMENTADO (ejecutor `bloque_a_forex` V1.0, pasos i–v y vii); sección cruzada y segunda vía por puntos, DOCUMENTADO |
| FX-CIP-001 | Paridad cubierta y base cruzada | MC-03 | PERF-FX-G10, PERF-FX-EM | H1–H3 | P1 | DOCUMENTADO |
| FX-UIP-001 | Paridad descubierta y regresión de Fama | MC-03 | TRANSVERSAL | H3–H4 | P2 | DOCUMENTADO |
| FX-PPP-001 | Paridad del poder adquisitivo absoluta y relativa | MC-03 | PERF-FX-G10, PERF-FX-EM, PERF-FX-FACT | H4 (H3 limitado) | P1 | IMPLEMENTADO (ejecutor `bloque_a_forex` V1.0, versión sencilla: PPA relativa y AR(1)); PPA absoluta, Balassa-Samuelson y Andrews, DOCUMENTADO |
| FX-PPA-001 | Desviación de PPA relativa (v1.1) | MC-03 | PERF-FX-G10, PERF-FX-EM | H4 | — | DEPRECADA; Implementado (heredado), solo como alternativa de FX-PPP-001 |
| FX-BEER-001 | Tipo de cambio real de equilibrio conductual (BEER) | MC-03 | PERF-FX-G10, PERF-FX-EM | H4 (H3 limitado) | P1 | DOCUMENTADO |
| FX-FEER-001 | Tipo de cambio de equilibrio fundamental y balanza macro | MC-03 | PERF-FX-G10, PERF-FX-EM | H4 | P2 | DOCUMENTADO |
| FX-REER-001 | Tipos efectivos nominal y real y su desviación | MC-01 (+ MC-03) | TRANSVERSAL | H3–H4 | P1 | DOCUMENTADO |
| FX-RDIFF-001 | Diferencial de tipos a 2 años y valor razonable a corto | MC-03 | PERF-FX-G10, PERF-FX-EM | H1–H3 | P1 | DOCUMENTADO |
| FX-TOT-001 | Términos de intercambio y sensibilidad a materias primas | MC-03 | PERF-FX-G10, PERF-FX-EM | H2–H4 | P1 | DOCUMENTADO |
| FX-TAYLOR-001 | Reglas de Taylor y divergencia de política monetaria | MC-03 | PERF-FX-G10, PERF-FX-EM | H3–H4 | P2 | DOCUMENTADO |
| FX-SURP-001 | Sorpresas macro y monetarias y respuesta cambiaria | MC-03 | PERF-FX-G10, PERF-FX-EM | H1–H2 | P1 | DOCUMENTADO |
| FX-POS-001 | Percentil de posicionamiento y flujos | MC-01 | TRANSVERSAL | H1–H3 | P1 | DOCUMENTADO |
| FX-BASKET-001 | Cestas e índices de divisas | MC-01 | TRANSVERSAL | H1–H4 | P1 | DOCUMENTADO |
| FX-NDF-001 | NDF, rendimientos implícitos y brecha *onshore*–*offshore* | MC-01 (+ MC-09) | PERF-FX-EM | H1–H3 | P1 | DOCUMENTADO |
| FX-MOM-001 | Momentum cambiario transversal y de serie temporal | MC-09 | TRANSVERSAL | H2–H3 (H1 limitado) | P1 | IMPLEMENTADO (ejecutor `bloque_a_forex` V1.0, sobre contado: 12-1, TSMOM y rango transversal); rentabilidad total y persistencia, DOCUMENTADO |
| FX-FACT-001 | Factores cambiarios: dólar, carry, valor y momentum | MC-09 | PERF-FX-FACT (+ G10, EM como exposición) | H2–H4 | P1 | DOCUMENTADO |
| FX-GK-001 | Garman-Kohlhagen, griegas y conversión delta–precio de ejercicio | MC-09 | TRANSVERSAL | H1–H3 | P1 | DOCUMENTADO |
| FX-RR-001 | *Risk reversals*, *butterflies* y sonrisa | MC-09 | TRANSVERSAL | H1–H3 | P1 | DOCUMENTADO |
| FX-TERM-001 | Estructura de plazos, volatilidad forward y volatilidad de evento | MC-09 | TRANSVERSAL | H1–H3 | P1 | DOCUMENTADO |
| FX-VRP-001 | Prima de volatilidad cambiaria | MC-09 (+ MC-02) | TRANSVERSAL | H1–H3 | P2 | DOCUMENTADO |
| FX-RND-001 | Densidad implícita neutral al riesgo y probabilidades de umbral | MC-09 | TRANSVERSAL | H1–H3 | P2 | DOCUMENTADO |
| FX-TAIL-001 | Riesgo de cola del carry y coste de cobertura | MC-07 | TRANSVERSAL | H2–H4 | P1 | DOCUMENTADO |
| FX-PEG-001 | Riesgo de ruptura de tipos fijos y bandas | MC-05 (+ MC-09) | PERF-FX-EM (+ G10 en episodios con suelo o techo) | H2–H4 | P2 | DOCUMENTADO |
| FX-PASS-001 | Escenarios de política monetaria y traslación al tipo de cambio | MC-04 | PERF-FX-G10, PERF-FX-EM | H2–H4 | P1 | DOCUMENTADO |
| FX-RW-001 | Evaluación frente al paseo aleatorio y el forward | MC-10 | TRANSVERSAL | H1–H4 | P0 | IMPLEMENTADO (ejecutor `bloque_a_forex` V1.0, versión sencilla: RI-PA y RI-FWD, Brier, BSS y acierto); U de Theil, CW, DM-HLN y fluctuación, DOCUMENTADO |
| FX-BT-001 | Backtesting de estrategias cambiarias sin sesgos | MC-10 | PERF-FX-FACT (+ G10, EM) | H2–H4 | P1 | DOCUMENTADO |

Total: 60 fichas (29 transversales conservadas del Catálogo V5.0, de las que 8 cambian de versión para adaptarse a divisas; FX-PPA-001, deprecada; 30 cambiarias nuevas o reescritas, incluidas FX-CARRY-001 v2.0, FX-BEER-001 v2.0 y FX-MOM-001 v2.0). El estado de gobierno de todas es VIGENTE salvo FX-PPA-001 (DEPRECADA).

## 5. Cobertura por segmento y por horizonte

### 5.1 Fichas por segmento

| Segmento | Perfil | Fichas propias más usadas | Transversales más usadas |
|---|---|---|---|
| G10N | PERF-FX-G10 | FX-RDIFF-001, FX-CARRY-001, MON-EXP-001, FX-PPP-001, FX-REER-001, FX-RR-001, FX-POS-001, FX-SURP-001, FX-CIP-001 | FX-VOL-001, VOL-GARCH-001, FX-REGIME-001, SCN-H-001, RISK-DD-001 |
| G10M | PERF-FX-G10 | FX-TOT-001, FX-CARRY-001, FX-RDIFF-001, FX-REER-001, FX-POS-001, FX-MOM-001, MON-EXP-001 | FX-CORR-001 (beta a materias primas y renta variable), VOL-GARCH-001, REG-HMM-001 |
| EMAS | PERF-FX-EM | FX-NDF-001, FX-REER-001, FX-PPP-001 (con Balassa-Samuelson), FX-CARRY-001, FX-PEG-001 (HKD), FX-BEER-001 | FX-BRK-001, FX-VOL-001, RISK-DD-001 |
| EMLA | PERF-FX-EM | FX-CARRY-001 (ajustado por volatilidad), FX-NDF-001, FX-TOT-001 (cobre, petróleo), FX-TAIL-001, FX-REER-001, FX-SURP-001 | VOL-GARCH-001 (asimetría direccional), FX-CORR-001, RISK-VAR-001 |
| EMEA | PERF-FX-EM | FX-REER-001, FX-BEER-001, FX-CARRY-001 (real), FX-PEG-001 (Golfo, EGP, NGN), FX-TAYLOR-001 (TRY), FX-TOT-001 (ZAR, petróleo) | FX-BRK-001, RISK-DD-001, SCN-H-001 |
| ESTR | PERF-FX-FACT | FX-FACT-001, FX-MOM-001, FX-CARRY-001, FX-TAIL-001, FX-BASKET-001, FX-BT-001, FX-VRP-001 | REG-HMM-001, BT-DSR-001, BT-PBO-001, ML-CLUS-001 |
| Transversales AG-09 / AG-21 | El del segmento de la divisa; PERF-FX-FACT para magnitudes globales | AG-09: MON-EXP-001, FX-TAYLOR-001, FX-SURP-001, FX-RDIFF-001; AG-21: FX-POS-001, FX-VOL-001, FX-RR-001, FX-TERM-001, FX-VRP-001, FX-CIP-001 | ST-DESC-001 (percentiles), FX-CORR-001 |

### 5.2 Métodos por horizonte

Los horizontes de cada ficha respetan la tabla 8.3 del Documento 0: ESTR sin H1; EMAS, EMLA y EMEA con H1 y H4 «limitados» (solo con liquidez suficiente y catalizador identificado).

| Horizonte | Métodos principales | Advertencia |
|---|---|---|
| H1 días | FX-VOL-001, VOL-GARCH-001, FX-SURP-001, MON-EXP-001 (reuniones), FX-RR-001, FX-TERM-001 (volatilidad de evento), FX-GK-001, FX-RND-001, FX-POS-001, FX-CARRY-001 (equilibrio del carry), FX-RDIFF-001, SCN-H-001 (bandas por volatilidad) | Menor fiabilidad esperada; probabilidades solo con certificado (R13); ESTR no aplica |
| H2 semanas | FX-MOM-001, FX-TREND-001, FX-CARRY-001, FX-RDIFF-001, FX-POS-001, FX-TOT-001, REG-HMM-001, FX-VRP-001, FX-FACT-001, ML-PRED-001, SCN-H-001 | Valoración solo como contexto |
| H3 meses | FX-CARRY-001, FX-FACT-001, FX-MOM-001, FX-REER-001, FX-TOT-001, FX-PASS-001, FX-TAYLOR-001, FX-TAIL-001, FX-PEG-001, FX-COINT-001, FX-CIP-001, SCN-H-001 | Regímenes de política monetaria y catalizadores dominan |
| H4 años | FX-PPP-001, FX-BEER-001, FX-FEER-001, FX-REER-001, FX-UIP-001, FX-TAYLOR-001, FX-FACT-001 (valor), FX-PEG-001, SCN-H-001 (bloques: carry + reversión al equilibrio) | Valoración informativa pero ruidosa; vida media de 3–5 años; pocas observaciones independientes |

Evaluación transversal de cualquier horizonte: FX-RW-001, FC-EVAL-001, FC-CAL-001, BT-DSR-001, BT-PBO-001, BT-VAR-001, FX-BT-001.

## 6. Fichas transversales conservadas del Catálogo V5.0

Se conservan con su identificador, su versión y su madurez; solo se actualizan las áreas del Mapa (nueva numeración del Mapa de conocimientos del Bloque A Forex), las temáticas de F8 (TMX-) y las advertencias propias de divisas. Las fichas transversales que cambian de versión para adaptarse a divisas están en la sección 7.

### FX-TREND-001 · Detección y medición de tendencia (Mann-Kendall + Theil-Sen)

**Identificación.** v1.1 · VIGENTE · MC-02 · Mapa: áreas 8, 7.
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
**Referencias.** Mann (1945), *Econometrica*; Kendall (1975), *Rank Correlation Methods*; Sen (1968), *JASA*; Hamed y Rao (1998), *Journal of Hydrology* · TMX-01.
**Prioridad y madurez.** P0 · IMPLEMENTADO (ejecutor V1.0 del Bloque A general, pruebas unitarias; reverificación pendiente en `bloque_a_forex`).

### FX-BRK-001 · Rupturas estructurales

**Identificación.** v1.1 · VIGENTE · MC-02 · Mapa: áreas 9, 8.
**Perfiles y horizontes.** TRANSVERSAL · H2–H4.
**Propósito.** ¿Cambia la serie de nivel, pendiente o varianza, y cuándo?
**Método.** CUSUM como primera vía; Bai-Perron con número máximo de rupturas y criterio BIC; clasificación del tipo de cambio; fechas con IC.
**Entradas mínimas.** ≥ 30 observaciones para una ruptura; ≥ 50 para dos o más.
**Parámetros.** max_rupturas (1; 1–5); tipo_cambio (auto); nivel (0,05); recorte (15 %).
**Salidas.** TABLA: rupturas, fechas e IC, tipo, estadísticos. ESTADISTICA.
**Supuestos y limitaciones.** Homocedasticidad dentro de segmentos (salvo ruptura de varianza); una revisión de la fuente, un cambio de régimen cambiario (fin de un tipo fijo o de un suelo), una redenominación o una intervención pueden imitar una ruptura; la ruptura no identifica su causa.
**Tolerancias y semilla.** 1e-6 en estadísticos; fechas exactas · null.
**Verificación.** Doble pasada; segunda vía: CUSUM frente a Bai-Perron.
**Referencia ingenua.** Modelo sin ruptura.
**Aclaración y rechazo.** Rechazo por debajo del mínimo.
**Referencias.** Page (1954), *Biometrika*; Bai y Perron (1998), *Econometrica*; Bai y Perron (2003), *Journal of Applied Econometrics* · TMX-01.
**Prioridad y madurez.** P0 · Implementado (heredado de la línea V3.0 del Bloque A general).

### FX-STL-001 · Descomposición tendencia-ciclo-estacionalidad

**Identificación.** v1.1 · VIGENTE · MC-02 · Mapa: área 7.
**Perfiles y horizontes.** TRANSVERSAL (flujos de fin de mes, trimestre y año fiscal; estacionalidad de balanza comercial y de remesas en PERF-FX-EM) · H2–H4.
**Propósito.** Separar tendencia, estacionalidad y resto.
**Método.** Esquema aditivo o multiplicativo; STL robusto (LOESS) o medias móviles; diagnóstico de estabilidad estacional.
**Entradas mínimas.** ≥ 2 ciclos estacionales completos (≥ 3 recomendados).
**Parámetros.** esquema (auto); periodo (según frecuencia); robusto (true).
**Salidas.** SERIE: tendencia, estacional, resto y ajustada, en unidades de origen. ESTADISTICA.
**Supuestos y limitaciones.** Descomposición no única; inestable en series cortas; en tipos de cambio en niveles la estacionalidad es débil: se aplica a flujos, posicionamiento y volatilidad, no al contado.
**Tolerancias y semilla.** 1e-6 · null.
**Verificación.** Identidad tendencia + estacional + resto = serie; caso sintético con estacionalidad conocida.
**Referencia ingenua.** RI-EST.
**Aclaración y rechazo.** Rechazo con < 2 ciclos.
**Referencias.** Cleveland, Cleveland, McRae y Terpenning (1990), *Journal of Official Statistics* · TMX-01.
**Prioridad y madurez.** P0 · Implementado (heredado de la línea V3.0 del Bloque A general).

### FX-REGIME-001 · Regímenes univariantes (Markov switching)

**Identificación.** v1.1 · VIGENTE · MC-02 · Mapa: área 9.
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
**Referencias.** Hamilton (1989), *Econometrica*; Kim y Nelson (1999), *State-Space Models with Regime Switching* · TMX-01.
**Prioridad y madurez.** P0 · Implementado (heredado de la línea V3.0 del Bloque A general).

### FX-COINT-001 · Cointegración y corrección de errores

**Identificación.** v1.1 · VIGENTE · MC-03 · Mapa: área 11.
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
**Referencias.** Engle y Granger (1987), *Econometrica*; Johansen (1991), *Econometrica* · TMX-01, TMX-04.
**Prioridad y madurez.** P1 · Implementado (heredado de la línea V3.0 del Bloque A general).

### FX-CORR-001 · Correlación dinámica y dependencia de cola

**Identificación.** v1.1 · VIGENTE · MC-03 · Mapa: área 17.
**Perfiles y horizontes.** TRANSVERSAL · H1–H4.
**Propósito.** Dependencia entre dos series: móvil, por régimen y en colas.
**Método.** Pearson móvil sobre rentabilidades con cortes sincronizados; Spearman de contraste; coeficientes de cola empíricos; beta al dólar amplio y a un índice de riesgo global si se piden; por régimen con probabilidades de REG-HMM-001 o FX-REGIME-001; DCC opcional.
**Entradas mínimas.** ≥ 60 observaciones comunes.
**Parámetros.** ventana (60); cola_cuantil (0,05; 0,01–0,10); usar_regimenes (false).
**Salidas.** SERIE de correlaciones; TABLA global, por régimen y colas. ESTADISTICA.
**Supuestos y limitaciones.** Correlaciones inestables y más altas en episodios de aversión al riesgo; baja correlación lineal no implica independencia de cola; series de distinto corte horario (BCE, WM/Reuters, NY 17:00) sesgan a la baja la correlación diaria: sincronizar o usar datos semanales; el sentido de cada par se declara (la correlación cambia de signo al invertir uno de ellos).
**Tolerancias y semilla.** 1e-8 · null.
**Verificación.** Simetría y diagonal unitaria; caso normal bivariante conocido.
**Referencia ingenua.** Correlación histórica de ventana larga.
**Aclaración y rechazo.** Rechazo con < 60 observaciones.
**Referencias.** Longin y Solnik (2001), *Journal of Finance*; Engle (2002), *JBES* · TMX-06, TMX-07.
**Prioridad y madurez.** P0 · IMPLEMENTADO (ejecutor V1.0 del Bloque A general, pruebas unitarias; reverificación pendiente en `bloque_a_forex`).

### ST-DESC-001 · Estadística descriptiva y momentos

**Identificación.** v1.1 · VIGENTE · MC-01 · Mapa: área 4.
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
**Referencias.** Tukey (1977), *Exploratory Data Analysis*; Hyndman y Fan (1996), *The American Statistician* · TMX-08 (respaldo transversal).
**Prioridad y madurez.** P0 · IMPLEMENTADO (ejecutor V1.0 del Bloque A general, pruebas unitarias; reverificación pendiente en `bloque_a_forex`).

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
**Referencias.** Lehmann y Romano (2005), *Testing Statistical Hypotheses*; Benjamini y Hochberg (1995), *JRSS B*; Holm (1979), *Scandinavian Journal of Statistics* · TMX-08 (respaldo transversal).
**Prioridad y madurez.** P0 · Implementado (heredado de la línea V3.0 del Bloque A general).

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
**Referencias.** Bodie, Kane y Marcus (2021), *Investments*, 12.ª ed. · TMX-03.
**Prioridad y madurez.** P0 · IMPLEMENTADO (ejecutor V1.0 del Bloque A general, pruebas unitarias; reverificación pendiente en `bloque_a_forex`).

### BIB-MET-001 · Bibliometría aplicada a fuentes

**Identificación.** v1.1 · VIGENTE · MC-01 · Mapa: área 45.
**Perfiles y horizontes.** TRANSVERSAL · no aplica.
**Propósito.** Indicadores de volumen, cobertura, concentración y duplicados de corpus de referencias (F7–F9).
**Método.** Conteos por periodo y temática; crecimiento (FIN-CAGR-001); HHI de concentración por fuente; duplicados por hash + título normalizado; precisión/exhaustividad con conjunto de referencia.
**Entradas mínimas.** Conjunto de fichas con fecha, temática y fuente.
**Parámetros.** granularidad (mensual); categorias (todas).
**Salidas.** TABLA. DETERMINISTA.
**Supuestos y limitaciones.** Describe el corpus registrado, no la literatura; citas no son calidad. Solicitantes por CT-09: Orquestador técnico (paquetes CT-21), Evaluador y, para la bibliometría y la calidad de sus propias fuentes, AG-14, AG-15 y AG-16 (6.1 del Documento 0).
**Tolerancias y semilla.** Conteos exactos · null.
**Verificación.** Totales por categoría suman el total.
**Referencia ingenua.** RI-NA.
**Aclaración y rechazo.** Rechazo con conjunto vacío o corrupto.
**Referencias.** Moed (2005), *Citation Analysis in Research Evaluation* · TMX-08 (respaldo transversal) y Fondo metodológico.
**Prioridad y madurez.** P1 · Implementado (heredado de la línea V3.0 del Bloque A general).

### SIM-MC-001 · Simulación Monte Carlo de trayectorias

**Identificación.** v1.1 · VIGENTE · MC-05 · Mapa: área 19.
**Perfiles y horizontes.** TRANSVERSAL · H1–H4.
**Propósito.** Distribución de resultados bajo una dinámica declarada.
**Método.** Dinámica del catálogo (paseo aleatorio sin deriva o con deriva igual al diferencial de tipos, GARCH de VOL-GARCH-001, bootstrap filtrado, saltos para colapsos del carry o rupturas de tipos fijos de FX-PEG-001); semilla y generador; reducción de varianza (antitéticas); cuantiles, probabilidades de umbral; error estándar de Monte Carlo.
**Entradas mínimas.** Dinámica y parámetros declarados.
**Parámetros.** n_trayectorias (10 000; 1 000–1 000 000); horizonte; cuantiles (0,05/0,5/0,95); semilla; reduccion_varianza (antitéticas).
**Salidas.** DISTRIBUCION con unidades; TABLA de convergencia. ESTADISTICA.
**Supuestos y limitaciones.** Condicional a la dinámica: no corrige un modelo mal especificado.
**Tolerancias y semilla.** 1e-6 con la misma semilla · obligatoria.
**Verificación.** Doble ejecución con la misma semilla; casos de solución analítica.
**Referencia ingenua.** RI-CLI (bootstrap simple de la historia).
**Aclaración y rechazo.** Rechazo sin semilla o sin dinámica.
**Referencias.** Glasserman (2004), *Monte Carlo Methods in Financial Engineering* · TMX-07.
**Prioridad y madurez.** P0 · Implementado (heredado de la línea V3.0 del Bloque A general).

### RISK-VAR-001 · VaR y Expected Shortfall

**Identificación.** v1.1 · VIGENTE · MC-07 · Mapa: área 25.
**Perfiles y horizontes.** TRANSVERSAL · H1–H3.
**Propósito.** VaR y ES con método, horizonte y nivel declarados.
**Método.** Histórico, paramétrico (normal, t, Cornish-Fisher), histórico filtrado o EVT-POT según la tabla de decisión de MC-07; ES al mismo nivel; advertencias obligatorias.
**Entradas mínimas.** ≥ 250 observaciones para histórico (≥ 500 recomendadas); EVT ≥ 50 excedencias; o distribución de MC-05 con semilla.
**Parámetros.** nivel (0,975; 0,90–0,99); horizonte; metodo (historico); divisa de medida y medida (contado o rentabilidad total, por defecto total).
**Salidas.** VALOR: VaR y ES (fracción del valor y moneda), con horizonte y nivel. ESTADISTICA.
**Supuestos y limitaciones.** El VaR no es la pérdida máxima ni describe la cola; √h solo con iid.
**Tolerancias y semilla.** 1e-6 · null o del plan.
**Verificación.** ES ≥ VaR; cuantiles monótonos; segunda vía histórico frente a paramétrico.
**Referencia ingenua.** VaR normal con volatilidad histórica (para backtesting con BT-VAR-001).
**Aclaración y rechazo.** Rechazo de nivel 99 % empírico con < 500 observaciones.
**Referencias.** Jorion (2007); McNeil, Frey y Embrechts (2015); Artzner et al. (1999) · TMX-07.
**Prioridad y madurez.** P0 · Implementado (heredado de la línea V3.0 del Bloque A general).

### ML-CAL-001 · Evaluación interna de modelos predictivos

**Identificación.** v1.1 · VIGENTE · MC-06 · Mapa: áreas 22, 23.
**Perfiles y horizontes.** TRANSVERSAL · H1–H4.
**Propósito.** Evaluar un modelo en desarrollo con validación temporal, métricas y comparación con la referencia. La certificación y las pruebas formales para el Evaluador usan FC-EVAL-001 y FC-CAL-001.
**Método.** Walk-forward (expansivo por defecto) con purga y embargo; MAE/RMSE/MASE, Brier, log-score, pinball; R²_OOS; cobertura de intervalos; mejora frente a referencia con IC por bootstrap de bloques; análisis por régimen.
**Entradas mínimas.** Predicciones y realizaciones alineadas, ≥ 30 por horizonte.
**Parámetros.** esquema (walk_forward_expansivo); horizontes; metricas (todas las aplicables).
**Salidas.** TABLA por horizonte y esquema. ESTADISTICA.
**Supuestos y limitaciones.** La evaluación retrospectiva no certifica el futuro; número de ensayos obligatorio.
**Tolerancias y semilla.** 1e-8 · entero del plan si hay bootstrap.
**Verificación.** Métricas recomputadas; particiones sin solape.
**Referencia ingenua.** RI-PA obligatoria (y RI-FWD en rentabilidad total o nivel con forward); RI-TB o RI-MH como complemento según el objetivo.
**Aclaración y rechazo.** Rechazo si predicciones y realizaciones no alinean.
**Referencias.** Hyndman y Athanasopoulos (2021); Campbell y Thompson (2008); López de Prado (2018) · TMX-09, TMX-08.
**Prioridad y madurez.** P0 · Implementado (heredado de la línea V3.0 del Bloque A general).

### AUD-REX-001 · Re-ejecución independiente (CT-10)

**Identificación.** v1.1 · VIGENTE · MC-08 · Mapa: áreas 48, 54, 55.
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
**Referencias.** Peng (2011), *Science*; National Academies (2019), *Reproducibility and Replicability in Science* · TMX-08 (respaldo transversal).
**Prioridad y madurez.** P0 · Implementado (heredado de la línea V3.0 del Bloque A general).

### FC-CAL-001 · Calibración y fiabilidad

**Identificación.** v1.0 · VIGENTE · MC-10 · Mapa: área 37.
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
**Referencias.** Bröcker y Smith (2007); Gneiting, Balabdaoui y Raftery (2007); Dawid (1982), «The Well-Calibrated Bayesian», *JASA*; Naeini, Cooper y Hauskrecht (2015), *AAAI* · TMX-08.
**Prioridad y madurez.** P0 · IMPLEMENTADO (ejecutor V1.0 del Bloque A general, pruebas unitarias; reverificación pendiente en `bloque_a_forex`).

### BT-DSR-001 · Sharpe probabilístico y Deflated Sharpe

**Identificación.** v1.0 · VIGENTE · MC-10 · Mapa: área 39.
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
**Referencias.** Lo (2002); Mertens (2002); Bailey y López de Prado (2012; 2014); Harvey y Liu (2015) · TMX-08.
**Prioridad y madurez.** P0 · DOCUMENTADO.

### BT-PBO-001 · Probabilidad de sobreajuste del backtest (CSCV)

**Identificación.** v1.0 · VIGENTE · MC-10 · Mapa: área 39.
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
**Referencias.** Bailey, Borwein, López de Prado y Zhu (2017) · TMX-08.
**Prioridad y madurez.** P1 · DOCUMENTADO.

### BT-VAR-001 · Backtesting de VaR y ES

**Identificación.** v1.0 · VIGENTE · MC-10 · Mapa: área 40.
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
**Referencias.** Kupiec (1995); Christoffersen (1998); Acerbi y Székely (2014); BCBS (1996), *Supervisory Framework for the Use of «Backtesting»* · TMX-07, TMX-08.
**Prioridad y madurez.** P1 · DOCUMENTADO.

### VOL-GARCH-001 · Volatilidad condicional GARCH

**Identificación.** v1.0 · VIGENTE · MC-02 · Mapa: áreas 10, 9.
**Perfiles y horizontes.** TRANSVERSAL · H1–H2 (H3 limitado).
**Propósito.** Volatilidad condicional actual y su estructura temporal prevista.
**Método.** GARCH(1,1) con innovaciones t por defecto: σ²_t = ω + α·ε²_{t−1} + β·σ²_{t−1}; alternativas GJR (asimetría) y EGARCH; máxima verosimilitud; persistencia α + β; vida media ln 0,5/ln(α + β); varianza de largo plazo ω/(1 − α − β); previsión a h pasos con reversión.
**Entradas mínimas.** ≥ 500 rendimientos diarios (250 con limitación).
**Parámetros.** modelo (GARCH-t; GJR, EGARCH con el signo referido a la depreciación de la divisa de riesgo, declarado); horizonte (1–60 sesiones); anualizacion (m de la serie, declarado: ≈ 260 en NY 17:00; 252 si se fija).
**Salidas.** TABLA: parámetros con EE, persistencia, vida media (sesiones); SERIE: volatilidad condicional y prevista (% anual). ESTADISTICA.
**Supuestos y limitaciones.** α + β ≥ 1 (integrado) ⇒ advertencia; rupturas e intervenciones inflan la persistencia; en regímenes gestionados la volatilidad condicional subestima el riesgo de salto (usar FX-PEG-001); el efecto apalancamiento clásico es débil en divisas, pero hay asimetría direccional en divisas de riesgo y cruces con JPY.
**Tolerancias y semilla.** 1e-6 en parámetros · null (valores iniciales fijos).
**Verificación.** Restricciones ω > 0, α, β ≥ 0; segunda vía: EWMA.
**Referencia ingenua.** RI-EWMA, evaluada con pérdida QLIKE.
**Aclaración y rechazo.** Rechazo con < 250 observaciones.
**Referencias.** Engle (1982), *Econometrica*; Bollerslev (1986), *Journal of Econometrics*; Glosten, Jagannathan y Runkle (1993), *Journal of Finance*; Nelson (1991), *Econometrica*; Hansen y Lunde (2005), *Journal of Applied Econometrics*; Patton (2011), *Journal of Econometrics* · TMX-02.
**Prioridad y madurez.** P0 · IMPLEMENTADO (ejecutor V1.0 del Bloque A general, pruebas unitarias; reverificación pendiente en `bloque_a_forex`).

### ML-PRED-001 · Modelo predictivo supervisado con walk-forward

**Identificación.** v1.0 · VIGENTE · MC-06 · Mapa: áreas 22, 23.
**Perfiles y horizontes.** TRANSVERSAL · H1–H3.
**Propósito.** Predicción de dirección, nivel o cuantil con validación temporal y comparación con la referencia.
**Método.** Objetivo con la definición del criterio de resolución (dirección del par, nivel o rentabilidad total, con su convención); variables conocibles (CFTC desde el viernes de publicación; macro con vintage); walk-forward con purga y embargo; regularizado lineal/logístico; ensamble de árboles solo si supera al lineal; calibración Platt o isotónica; registro de ensayos.
**Entradas mínimas.** ≥ 60 observaciones independientes del objetivo (≥ 250 para modelos no lineales).
**Parámetros.** modelo (logistica_L2); rejilla (≤ 20 en PLAN_STD); embargo (≥ h); calibracion (auto).
**Salidas.** TABLA: predicción actual (probabilidad, nivel o cuantiles), métricas fuera de muestra, mejora frente a referencia con IC, ECE, pendiente b, ensayos. ESTADISTICA.
**Supuestos y limitaciones.** Relaciones estables en la ventana; mejora con IC que incluye 0 ⇒ «sin mejora demostrada».
**Tolerancias y semilla.** 1e-6 (deterministas); 1e-3 en métricas si hay paralelismo · entero del plan.
**Verificación.** Particiones sin solape; métricas recomputadas; segunda vía: ventana móvil.
**Referencia ingenua.** RI-PA obligatoria (y RI-FWD si el objetivo es rentabilidad total o nivel con forward líquido); RI-TB para dirección.
**Aclaración y rechazo.** Rechazo con fuga o sin regla de conocibilidad.
**Referencias.** Hastie, Tibshirani y Friedman (2009); Gu, Kelly y Xiu (2020); López de Prado (2018) · TMX-09.
**Prioridad y madurez.** P1 · DOCUMENTADO.

### DEC-VOI-001 · Valor de la información

**Identificación.** v1.0 · VIGENTE · MC-07 · Mapa: áreas 28, 53.
**Perfiles y horizontes.** TRANSVERSAL · no aplica.
**Propósito.** ¿Puede un cálculo o búsqueda adicional cambiar la decisión (entrar o salir del top-3, cruzar un umbral)? (R15, 7.5 del Documento 0).
**Método.** (i) Decisiones posibles y sus pagos en unidades de puntuación (o de valor esperado), con los umbrales vigentes de F10. (ii) Distribución plausible de la puntuación decisiva tras el cálculo (rango de sensibilidad de la ficha prevista o histórico del Registro de cálculos). (iii) EVPI y, si hay verosimilitud, EVSI. (iv) Regla simple: si el rango plausible no alcanza ningún umbral (E 60, A 55, T 50, GC2 50; ±5 de banda marginal) ni cambia el orden del top-3 (diferencia de RK > amplitud plausible), VOI = 0.
**Entradas mínimas.** Puntuaciones actuales, umbrales vigentes, rango plausible del efecto del cálculo, coste en UC.
**Parámetros.** umbrales (F10); coste_uc.
**Salidas.** TABLA: VOI (puntos o UC equivalentes), probabilidad de cambio de decisión, recomendación técnica EJECUTAR/NO_EJECUTAR (la decisión es del solicitante). ESTADISTICA.
**Supuestos y limitaciones.** Depende del rango plausible declarado; no sustituye el juicio sobre incertidumbre profunda.
**Tolerancias y semilla.** 1e-8 · null (o del plan si se simula).
**Verificación.** Información perfecta ⇒ VOI = EVPI ≥ EVSI ≥ 0.
**Referencia ingenua.** Ejecutar siempre (coste) frente a no ejecutar nunca.
**Aclaración y rechazo.** Aclaración sin rango plausible.
**Referencias.** Raiffa y Schlaifer (1961); Howard (1966), «Information Value Theory», *IEEE Transactions on Systems Science and Cybernetics* · TMX-08 (respaldo transversal).
**Prioridad y madurez.** P1 · DOCUMENTADO.

## 7. Fichas transversales adaptadas a divisas (nueva versión)

### FX-VOL-001 · Volatilidad realizada e implícita y su brecha

**Identificación.** v1.2 · VIGENTE · MC-02 · Mapa: áreas 10, 33.
**Perfiles y horizontes.** TRANSVERSAL · H1–H3.
**Propósito.** Medir la volatilidad realizada del par o de la cesta y, si se aporta, su brecha con la implícita del mismo plazo.
**Método.** Desviación típica de rendimientos logarítmicos de cierre a cierre con corte declarado (NY 17:00 por defecto), anualizada con `m` de la serie; ventana móvil opcional; estimadores de rango (Parkinson, Garman-Klass, Yang-Zhang) si se aportan velas del día cambiario; realizada intradía de 5 minutos si hay datos de alta frecuencia; brecha implícita − realizada con plazos alineados (implícita a 1 mes frente a realizada de 21–22 sesiones) y, si se pide, realizada posterior (solo en evaluación, con fecha de corte).
**Entradas mínimas.** ≥ 30 observaciones; implícita con fuente, plazo, convención (ATM DNS por defecto) y fecha.
**Parámetros.** ventana (21; 10–260); anualizacion (m de la serie, declarado); estimador (cierre_a_cierre; rango; intradia_5m); ventana_movil (false).
**Salidas.** VALOR o SERIE: volatilidad anualizada (%), brecha (puntos de volatilidad), percentil de la implícita frente a 3 años. ESTADISTICA.
**Supuestos y limitaciones.** La implícita no es previsión insesgada de la realizada (incluye prima de volatilidad, FX-VRP-001); la realizada de un régimen gestionado no mide el riesgo de salto (FX-PEG-001); la baja frecuencia subestima colas; los saltos de reapertura del domingo se declaran.
**Tolerancias y semilla.** 1e-8 · null.
**Verificación.** Coherencia de anualización; inversión del par deja la volatilidad logarítmica invariante; segunda vía: ventana alternativa o EWMA.
**Referencia ingenua.** RI-EWMA.
**Aclaración y rechazo.** Aclaración si falta el corte horario o el plazo de la implícita; rechazo con < 30 observaciones.
**Referencias.** Andersen, Bollerslev, Diebold y Labys (2001), «The Distribution of Realized Exchange Rate Volatility», *JASA*; Andersen, Bollerslev, Diebold y Labys (2003), *Econometrica*; Liu, Patton y Sheppard (2015), *Journal of Econometrics*; Poon y Granger (2003), *JEL* · TMX-02.
**Prioridad y madurez.** P0 · IMPLEMENTADO (ejecutor V1.0 del Bloque A general) para cierre a cierre y brecha; estimadores de rango e intradía DOCUMENTADO.

### SCORE-RK-001 · Puntuaciones T/E/M/P/A y clave RK (idéntico a HT-03)

**Identificación.** v2.0 · VIGENTE · MC-01 · Mapa: área 50.
**Perfiles y horizontes.** TRANSVERSAL · no aplica.
**Propósito.** Reconstruir de forma independiente las puntuaciones de HT-03 para la validación G3 y PS8, y para re-ejecuciones CT-10. **HT-03 es la herramienta canónica**; esta ficha replica exactamente su regla y cualquier diferencia con HT-03 es una discrepancia.
**Método.** (i) Cada dimensión en {0, 10, …, 100}; «NA» redistribuye su peso proporcionalmente entre las demás (anotado); «NE» puntúa 0; más de dos NA/NE en una puntuación ⇒ rechazo. (ii) Pesos vigentes de F10 (iniciales del Documento 0 Forex, 9.1): T = magnitud 20, alcance 15, velocidad 15, duración 10, difusión 10, posición en la cadena de transmisión 10, capacidad transformadora 10, claridad causal 10; E = raíces 25, cobertura 15, calidad metodológica 15, trazabilidad 15, actualidad 10, discrepancias resueltas 10, objeciones CT-13 respondidas 10; M = adopción 20, escalado 15, indicadores 15, persistencia 15, estabilidad de impulsores 15, hitos 20; P = T 40, novedad 20, incertidumbre reducible 20, coste-eficiencia 20; **A (FX)** = asimetría rentabilidad/riesgo 30, valoración y desviación del equilibrio 20, carry 15, catalizadores 15, momento y posicionamiento 10, convertibilidad y profundidad del mercado 10 (A no puntúa instrumentos ni sus costes: frontera con el Bloque B). (iii) Tope por saturación narrativa: si la marca está activa (posicionamiento especulativo en el decil extremo a favor de la tesis y forward que descuenta la senda esperada, 9.1), la dimensión «valoración y desviación del equilibrio» de A se limita a 40 antes de ponderar. (iv) Total = Σ wᵢ·dᵢ/Σ wᵢ, redondeado al múltiplo de 5 más próximo (exactamente a mitad: hacia arriba, salvo que HT-03 declare otra regla). (v) RK = 0,45·A + 0,35·E + 0,20·T (pesos vigentes de F10) sobre los totales ya redondeados; T = NA en oportunidades tácticas ⇒ RK = (0,45·A + 0,35·E)/0,80. (vi) Banderas: banda marginal (total a ≤ 5 puntos de un umbral: E 60, A 55, T 50, A 65 si T = NA, GC2 50), cambio ≥ 15 puntos frente al ciclo anterior, empate de RK a ±2.
**Entradas mínimas.** Dimensiones con valor, NA o NE; pesos y umbrales vigentes (versión de F10); marca de saturación; puntuaciones del ciclo anterior (para la bandera de cambio).
**Parámetros.** version_pesos (F10 vigente, `methodology_version` FX-1.0); regla_mitad (HT-03).
**Salidas.** TABLA: T, E, M, P, A (0–100, múltiplos de 5), RK (entero; redondeo con empates hacia abajo, igual que HT-03), desglose ponderado, redistribuciones NA, banderas. DETERMINISTA.
**Supuestos y limitaciones.** Las dimensiones son juicios anclados de los agentes; la ficha solo garantiza la aritmética. RK ordena, no es probabilidad ni rentabilidad.
**Tolerancias y semilla.** Igualdad exacta con HT-03 · null.
**Verificación.** Doble pasada; identidad con HT-03 en todos los casos de control de `10_Herramientas` con los pesos de A del bloque Forex.
**Referencia ingenua.** RI-NA.
**Aclaración y rechazo.** Rechazo con > 2 NA/NE o dimensión fuera de {0, 10, …, 100}; aclaración si la versión de pesos no coincide con F10 o si llegan las cinco dimensiones de A del Bloque A general (sin carry).
**Referencias.** Documento 0 del Bloque A Forex, 9.1–9.2 y Anexo A; Saisana, Saltelli y Tarantola (2005), *JRSS A*; OECD/JRC (2008), *Handbook on Constructing Composite Indicators* · TMX-08 (respaldo transversal).
**Prioridad y madurez.** P0 · IMPLEMENTADO (v2.0 en el ejecutor `bloque_a_forex` V1.0): regla de agregación, NA/NE, redondeo y RK con los pesos de A del bloque Forex, reverificada contra HT-03 con los casos de control de `10_Herramientas` (`test_score_rk_identico_a_ht03`).

### FC-EVAL-001 · Evaluación de pronósticos

**Identificación.** v1.1 · VIGENTE · MC-10 · Mapa: áreas 36, 38, 41.
**Perfiles y horizontes.** TRANSVERSAL · H1–H4.
**Propósito.** ¿Aciertan los pronósticos de una celda segmento × horizonte × método y baten a las referencias ingenuas con significación?
**Método.** (i) Control de conocibilidad y resolución con el criterio congelado de F4 (NO_RESOLUBLE contado aparte); la realización usa el indicador de seguimiento con la misma fuente y corte que el PRG-FX-. (ii) n efectivo con solapamiento. (iii) Brier y descomposición de Murphy; log-score (p recortado a [0,01; 0,99]); CRPS o pinball para distribuciones y cuantiles; puntuación de intervalo. (iv) Acierto direccional: binomial frente a 0,5 y a la tasa base, y Pesaran-Timmermann. (v) **BSS frente al paseo aleatorio** (RI-PA probabilística) y, en rentabilidad total, frente al forward (RI-FWD), con IC 90 % por bootstrap estacionario por fechas; frente a la climatología como complemento. (vi) DM con corrección HLN frente a la referencia (Clark-West si es anidada, el caso habitual frente al paseo aleatorio; Giacomini-White si se pide habilidad condicional). (vii) Corrección múltiple (Holm o BH) si se evalúan varias celdas. (viii) Efecto mínimo detectable.
**Entradas mínimas.** PRG-FX- resueltos de la celda (≥ 30 para recalibrar; ≥ 100 para certificar, Anexo A), realizaciones con fuente y vintage, referencias.
**Parámetros.** perdida (brier); referencia (RI-PA; RI-FWD en rentabilidad total; RI-TB o RI-CLI como complemento); B (2 000; 1 000–10 000); bloque (max(h, T^{1/3})); nivel_ic (0,90); significacion (0,10 unilateral para 12.2, salvo F10); mapeo_bandas (F10: 0,85/0,65/0,50/0,35/0,15).
**Salidas.** TABLA: BS, FIA, RES, INC, LS, CRPS (unidades de la variable), acierto (%), p-valores, BSS e IC frente a cada referencia, estadísticos DM* y CW, n nominal/efectivo/no resolubles, efecto detectable. ESTADISTICA.
**Supuestos y limitaciones.** Muestras de 30–100 solo detectan ventajas grandes; «no significativo» no equivale a «sin ventaja»; en divisas la ventaja esperable frente al paseo aleatorio es pequeña (Meese y Rogoff, 1983; Rossi, 2013).
**Tolerancias y semilla.** 1e-8 en métricas; 1e-6 en IC con la misma semilla · entero del plan.
**Verificación.** Identidad de Murphy con probabilidades discretas; recuentos; BS de la referencia RI-PA simétrica = 0,25 en sucesos «sube/baja»; segunda vía: otra longitud de bloque.
**Referencia ingenua.** RI-PA obligatoria; RI-FWD en rentabilidad total (obligatorias por definición).
**Aclaración y rechazo.** Rechazo si hay fuga sistemática, si falta el criterio de resolución o si la realización usa otra fuente o corte que el PRG-FX-.
**Referencias.** Gneiting y Raftery (2007); Murphy (1973); Diebold y Mariano (1995); Harvey, Leybourne y Newbold (1997); Clark y West (2007); Giacomini y White (2006); Pesaran y Timmermann (1992); Politis y Romano (1994); Meese y Rogoff (1983) · TMX-08.
**Prioridad y madurez.** P0 · IMPLEMENTADO (ejecutor V1.0 del Bloque A general) para las métricas; la referencia RI-PA probabilística y RI-FWD, DOCUMENTADO (alternativa: referencia aportada por el solicitante como serie de probabilidades).

### SCN-H-001 · Escenarios por horizonte

**Identificación.** v2.0 · VIGENTE · MC-05 · Mapa: áreas 18, 19.
**Perfiles y horizontes.** TRANSVERSAL · H1–H4 según 8.3 del Documento 0 (ESTR sin H1; H1 y H4 limitados en emergentes).
**Propósito.** Escenarios base, favorable y adverso del indicador de seguimiento de una opción (contado o rentabilidad total, declarado) para cada horizonte aplicable, con bandas y probabilidades de umbral (para CT-12 de Prospectiva).
**Método.** H1–H2: simulación con volatilidad condicional (VOL-GARCH-001) y residuos por bootstrap filtrado, centrada en el contado (RI-PA) y, en rentabilidad total, con el carry; volatilidad de evento (FX-TERM-001) si el horizonte contiene una reunión o un dato clave. H3: mezcla por régimen (probabilidades filtradas de REG-HMM-001) + escenarios de política monetaria de FX-PASS-001. H4: bloques de rentabilidad (carry esperado + reversión parcial al equilibrio de FX-PPP-001 o FX-BEER-001 con la vida media estimada ± incertidumbre de cada bloque). Regímenes de tipo fijo: mezcla «se mantiene / se rompe» con FX-PEG-001. En todos: cuantiles 10/50/90; base = mediana; favorable/adverso = cuantiles 80/20 o escenarios narrativos cuantificados que entregue Prospectiva; probabilidades de umbrales (solo publicables con certificado R13) junto a las de RI-PA y RI-FWD.
**Entradas mínimas.** H1–H2: ≥ 2 años diarios; H3: régimen y escenarios de política; H4: insumos de los bloques (diferencial esperado, desalineamiento y vida media).
**Parámetros.** n_trayectorias (10 000); cuantiles (0,1/0,5/0,9); semilla; umbrales; medida (PRECIO_CONTADO o RENTABILIDAD_TOTAL).
**Salidas.** DISTRIBUCION por horizonte (nivel del par o %), TABLA de escenarios con condiciones y probabilidades de umbral frente a RI-PA y RI-FWD. ESTADISTICA.
**Supuestos y limitaciones.** Distribuciones condicionales al modelo; las bandas de H4 son anchas por construcción; la reversión al equilibrio no tiene fecha.
**Tolerancias y semilla.** 1e-6 con misma semilla · obligatoria.
**Verificación.** Monotonía de cuantiles; doble ejecución; coherencia entre horizontes (bandas crecientes); con deriva nula y sin carry, la mediana reproduce el contado.
**Referencia ingenua.** RI-PA y RI-FWD (probabilísticas) y RI-CLI.
**Aclaración y rechazo.** Rechazo sin semilla, sin medida declarada o en horizonte «No» de 8.3 del Documento 0 (HORIZONTE_NO_APLICABLE).
**Referencias.** Glasserman (2004); Christoffersen (2012), *Elements of Financial Risk Management*; Rogoff (1996); Clark y MacDonald (1998) · TMX-07, TMX-04.
**Prioridad y madurez.** P0 · DOCUMENTADO (alternativa: SIM-MC-001 con paseo aleatorio GARCH declarado).

### REG-HMM-001 · Régimen cambiario y de riesgo (HMM multivariante)

**Identificación.** v2.0 · VIGENTE · MC-02 · Mapa: área 9.
**Perfiles y horizontes.** TRANSVERSAL · H2–H3.
**Propósito.** Probabilidad actual de cada régimen cambiario y de riesgo (paso 1 del marco común de los Analistas de segmento: dólar fuerte o débil, apetito o aversión al riesgo, volatilidad, ciclo de tipos).
**Método.** Modelo oculto de Markov gaussiano sobre variables estandarizadas con datos de entrenamiento: rentabilidad del dólar amplio, volatilidad implícita cambiaria global (índices tipo G7 o CVIX), rentabilidad de una cesta de carry, diferencial medio de tipos frente al USD y un indicador de riesgo global (volatilidad de la renta variable o diferencial de crédito) aportado como dato; en PERF-FX-EM se añade el diferencial de CDS soberanos medio o el EMBI como dato. Estados por BIC; ≥ 20 arranques con semilla; **probabilidades filtradas** como salida operativa; etiquetado descriptivo por medias (p. ej., «carry favorable», «aversión al riesgo con dólar fuerte»).
**Entradas mínimas.** ≥ 260 observaciones semanales o ≥ 120 mensuales.
**Parámetros.** n_estados (BIC; 2–4); covarianza (diagonal; completa); arranques (20).
**Salidas.** TABLA: probabilidades filtradas actuales, matriz de transición, duraciones esperadas, medias por estado; SERIE histórica de probabilidades filtradas. ESTADISTICA.
**Supuestos y limitaciones.** Probabilidades suavizadas solo descriptivas (usarlas en previsión es fuga); regímenes pueden no repetirse; las etiquetas son descriptivas, no causales.
**Tolerancias y semilla.** 1e-6 en parámetros; etiquetas alineadas por medias · entero del plan.
**Verificación.** Filas de transición suman 1; estabilidad entre semillas.
**Referencia ingenua.** Régimen de la observación anterior; incondicional.
**Aclaración y rechazo.** Rechazo por debajo del mínimo.
**Referencias.** Hamilton (1989); Rabiner (1989), *Proceedings of the IEEE*; Ang y Bekaert (2002), *RFS*; Ang y Timmermann (2012), *Annual Review of Financial Economics*; Menkhoff, Sarno, Schmeling y Schrimpf (2012a), *Journal of Finance* · TMX-01.
**Prioridad y madurez.** P1 · DOCUMENTADO (alternativa: FX-REGIME-001 univariante sobre la volatilidad cambiaria global).

### ML-CLUS-001 · Clústeres de exposición, apuestas independientes y exposición por divisa

**Identificación.** v2.0 · VIGENTE · MC-06 · Mapa: áreas 22, 27.
**Perfiles y horizontes.** TRANSVERSAL · no aplica.
**Propósito.** Agrupar opciones con los mismos factores dominantes (regla de diversidad 9.6.3: dólar, yen o refugio, carry y riesgo global, materias primas, una divisa concreta), contar las apuestas independientes del informe (9.6.6) y calcular la **exposición agregada por divisa** del conjunto de opciones.
**Método.** (i) Rentabilidades totales de los indicadores de seguimiento de los ámbitos con cortes sincronizados y dirección aplicada (una opción `BAJISTA_BASE` entra con signo invertido). (ii) Correlación (Pearson y Spearman); distancia √(2(1 − ρ)); agrupación jerárquica (enlace medio); corte en ρ = 0,7 por defecto; `N_ef = (Σλᵢ)²/Σλᵢ²` con autovalores de la matriz de correlación. (iii) Cargas en factores comunes (dólar amplio, carry HML_FX, índice de volatilidad cambiaria, materias primas) con MC-03 para etiquetar el factor dominante. (iv) **Exposición por divisa**: suma de pesos firmados de cada divisa en todas las opciones (lado largo +, corto −, incluida la divisa de financiación), en número de opciones equivalentes y en signo; detección de contradicciones (misma divisa como pata activa de la tesis, larga en un segmento y corta en otro; la contrapartida o financiación no cuenta, 9.6.6). (v) Regla «una misma divisa del propio segmento no puede tener la misma dirección en más de dos opciones del segmento» (la contrapartida o financiación no cuenta, 9.6.3): recuento por segmento.
**Entradas mínimas.** Rendimientos alineados ≥ 1 año diarios o ≥ 3 años semanales; composición firmada de cada opción.
**Parámetros.** umbral_rho (0,7; 0,5–0,85); ventana (1 año diario); enlace (medio); ventana_estres (episodio declarado, p. ej., agosto de 2024).
**Salidas.** TABLA: clúster y factor dominante por opción, matriz de correlación, N_ef (número de apuestas), sensibilidad al umbral, exposición por divisa, contradicciones y recuentos por divisa y dirección. ESTADISTICA (correlaciones) y DETERMINISTA (exposiciones).
**Supuestos y limitaciones.** Correlaciones inestables y más altas en crisis (declarar N_ef también en una ventana de estrés); la exposición por divisa es contable, no de riesgo.
**Tolerancias y semilla.** 1e-8; asignación de clúster y exposición exactas · null.
**Verificación.** n opciones independientes ⇒ N_ef ≈ n; una opción y su inversa ⇒ ρ = −1 y exposición neta nula; segunda vía: Spearman.
**Referencia ingenua.** Agrupación por segmento.
**Aclaración y rechazo.** Rechazo con series no alineables o con opciones sin dirección o sin divisa de financiación.
**Referencias.** Mantegna (1999), *European Physical Journal B*; Meucci (2009); López de Prado (2016); Verdelhan (2018), *Journal of Finance*; Lustig, Roussanov y Verdelhan (2011), *RFS* · TMX-06.
**Prioridad y madurez.** P0 · IMPLEMENTADO (ejecutor V1.0 del Bloque A general) para clústeres y N_ef; exposición por divisa y factor dominante, DOCUMENTADO.

### RISK-DD-001 · Drawdown, liquidez y escala de riesgo 1–5

**Identificación.** v2.0 · VIGENTE · MC-07 · Mapa: áreas 25, 34.
**Perfiles y horizontes.** TRANSVERSAL · H2–H4.
**Propósito.** Riesgo de trayectoria y de liquidez del indicador de seguimiento de una opción cambiaria y su clase de riesgo 1–5 para el paquete (`riesgo_1a5`; Anexo A, «Escala de riesgo 1–5» y nota 2).
**Método.** (i) Sobre el **índice de rentabilidad total** de la exposición con su dirección (o el contado si la medida es contado, declarado): MDD, duración y recuperación; Calmar; CDaR; volatilidad anualizada. (ii) **Base por volatilidad anualizada (umbrales cambiarios)**: < 5 % ⇒ 1; 5–9 % ⇒ 2; 9–14 % ⇒ 3; 14–20 % ⇒ 4; ≥ 20 % ⇒ 5. (iii) **Ajustes** (+1 cada uno, máximo 5): colas (ES 97,5 % a 10 sesiones > 2,5·σ_diaria·√10, o asimetría de rentabilidades semanales < −0,5 en la dirección de la exposición, típica del carry); liquidez (divisa con NDF, controles de capital, horario de liquidez limitado o profundidad baja según la convertibilidad declarada); caída máxima (MDD histórico > 25 %). (iv) **Suelo de régimen** (nota 2 del Anexo A): un tipo fijo con riesgo de ruptura o una divisa con controles parte, como mínimo, de 4.
**Entradas mínimas.** ≥ 3 años de rentabilidades (≥ 1 año con limitación); convertibilidad del ámbito (convertible, NDF, controles); régimen de facto.
**Parámetros.** ventana (toda la disponible; mínimo 3 años); medida (RENTABILIDAD_TOTAL); umbrales_vol (0,05/0,09/0,14/0,20); umbral_mdd (0,25).
**Salidas.** TABLA: MDD (%), duración (sesiones), Calmar, CDaR, volatilidad, ES, asimetría, `riesgo_1a5` con el desglose base + ajustes + suelo y su motivo. ESTADISTICA.
**Supuestos y limitaciones.** El MDD de muestras cortas subestima el de largo plazo; la volatilidad realizada de un régimen gestionado subestima el riesgo (de ahí el suelo); la escala es del catálogo (tipo 3) y el Evaluador puede proponer su recalibración dentro de bandas.
**Tolerancias y semilla.** 1e-8; clase de riesgo exacta · null.
**Verificación.** Drawdown ∈ [0, 1]; serie creciente ⇒ MDD = 0; casos de control: EUR/USD con σ ≈ 7–8 % y sin ajustes ⇒ 2; USD/HKD con riesgo de ruptura declarado ⇒ ≥ 4; cesta de carry emergente con asimetría −0,8 ⇒ base + 1.
**Referencia ingenua.** RI-NA (descriptivo).
**Aclaración y rechazo.** Rechazo con < 1 año de datos o sin convertibilidad declarada.
**Referencias.** Magdon-Ismail et al. (2004); Chekhlov, Uryasev y Zabarankin (2005), *IJTAF*; Bangia et al. (1999); Brunnermeier, Nagel y Pedersen (2008) · TMX-07.
**Prioridad y madurez.** P0 · IMPLEMENTADO (v2.0 en el ejecutor `bloque_a_forex` V1.0): umbrales cambiarios 5/9/14/20 %, ajustes por colas o asimetría semanal, liquidez y caída máxima > 25 %, suelo 4 de régimen y tope 5, con los casos de control de esta ficha (`test_risk_dd_v2_umbrales_cambiarios_y_suelo`).

### MON-EXP-001 · Expectativas implícitas de tipos a corto por reunión

**Identificación.** v1.1 · VIGENTE · MC-09 · Mapa: áreas 15, 6.
**Perfiles y horizontes.** PERF-FX-G10, PERF-FX-EM (donde exista curva OIS o de futuros líquida) · H1 (limitado: reuniones de bancos centrales)–H3.
**Propósito.** ¿Qué senda de tipos oficiales descuenta el mercado para cada banco central y qué probabilidad implícita asigna a cada decisión de las próximas reuniones? (dato del informe BCM de AG-09: `senda_descontada`, `sorpresa_reciente`).
**Método.** (i) Tipos *forward* de la curva OIS (SOFR, €STR, SONIA, TONA, SARON, CORRA, AONIA y equivalentes) o de futuros a 1 y 3 meses (tipo = 100 − precio; ajuste de convexidad en plazos > 1 año). (ii) Senda por reunión: tipo esperado tras la reunión k a partir de los *forwards* entre fechas de reunión, descontando el diferencial estable tipo oficial–tipo de mercado. (iii) Probabilidad implícita de un movimiento Δ = (tipo implícito tras la reunión − tipo vigente)/Δ, con ajuste por días del periodo. (iv) Cambio acumulado descontado a 6 y 12 meses (pb). (v) Sorpresa de cada decisión frente a la senda del día anterior. (vi) **Divergencia** entre dos bancos centrales: diferencia de cambios acumulados descontados y su variación en la ventana pedida.
**Entradas mínimas.** Curva OIS o futuros con ≥ 3 nodos en 12 meses y fechas; calendario de reuniones; tipo oficial y diferencial habitual tipo oficial–tipo de mercado.
**Parámetros.** incremento (25 pb; 50 o 100 pb en emergentes si se declara); diferencial_estable (media de 20 días); convexidad (true para > 1 año).
**Salidas.** TABLA: senda por reunión (%), probabilidades por movimiento, cambio acumulado (pb), sorpresas (pb), divergencia (pb). DETERMINISTA (dada la curva) y ESTADISTICA (ajustes).
**Supuestos y limitaciones.** Los tipos implícitos incluyen una prima por plazo pequeña pero no nula; probabilidades neutrales al riesgo; el diferencial tipo oficial–mercado puede variar; el método de probabilidades binario es una simplificación; en emergentes sin OIS líquido se rechaza o se usa el NDF solo como contexto.
**Tolerancias y semilla.** 1e-10 · null.
**Verificación.** Curva plana al tipo vigente ⇒ probabilidad de movimiento 0; la senda reproduce los *forwards* de entrada.
**Referencia ingenua.** RI-PA (tipo oficial sin cambios) y senda de encuesta si se aporta.
**Aclaración y rechazo.** Rechazo sin calendario de reuniones o con < 3 nodos en 12 meses.
**Referencias.** Kuttner (2001), *Journal of Monetary Economics*; Gürkaynak, Sack y Swanson (2005), *International Journal of Central Banking*; Piazzesi y Swanson (2008), *Journal of Monetary Economics*; CME Group, *CME FedWatch Tool: Methodology* · TMX-03.
**Prioridad y madurez.** P1 · DOCUMENTADO (alternativa: FIN-CAGR-001 y aritmética sobre forwards aportados, `op_sin_ficha`).

## 8. Fichas cambiarias

### 8.1 Cálculo cambiario básico (MC-01)

### FX-CONV-001 · Convenciones de cotización, inversión y cruces sintéticos

**Identificación.** v1.0 · VIGENTE · MC-01 · Mapa: área 2.
**Perfiles y horizontes.** TRANSVERSAL · no aplica.
**Propósito.** Expresar cualquier tipo de cambio en la convención de mercado BASE/COTIZADA, invertirlo o construir un cruce sintético con su horquilla, y convertir variaciones de una divisa en las de la otra.
**Método.** (i) Normalización a la convención de mercado (prioridad EUR > GBP > AUD > NZD > USD > CAD > CHF > JPY; emergentes con USD como base; europeas centrales y escandinavas frente al EUR), declarando si se ha invertido. (ii) Inversión `S(B/A) = 1/S(A/B)`, `bid(B/A) = 1/ask(A/B)`, `ask(B/A) = 1/bid(A/B)`. (iii) Cruce por producto cuando la divisa común es cotizada en una pata y base en la otra (`EUR/JPY = EUR/USD × USD/JPY`; bid × bid, ask × ask) y por cociente cuando ocupa la misma posición (`EUR/GBP = EUR/USD ÷ GBP/USD`; bid = bid/ask, ask = ask/bid). (iv) Escala del pip y conversión de puntos. (v) Variación de la cotizada `1/(1 + ΔS/S) − 1` y variación logarítmica simétrica. (vi) Conversión de importes a la divisa base del usuario (F10) con tipo, fecha y fuente.
**Entradas mínimas.** Cotizaciones con fuente, corte horario y fecha; horquilla si se pide el cruce con horquilla; las patas de un cruce con el mismo corte.
**Parámetros.** convencion (mercado); con_horquilla (false); escala_pip (de la fuente); divisa_comun (USD).
**Salidas.** TABLA: par normalizado, sentido, medio, bid, ask, pip, variaciones en ambas divisas. DETERMINISTA.
**Supuestos y limitaciones.** El cruce sintético difiere del cruce cotizado directamente en la horquilla y en el corte; un cruce con patas de cortes distintos es DATOS_INCOHERENTES.
**Tolerancias y semilla.** 1e-10 · null.
**Verificación.** Triangulación: `EUR/USD × USD/JPY ÷ EUR/JPY = 1` dentro de la horquilla; inversión doble = identidad; USD/JPY +10 % ⇒ JPY −9,0909 %.
**Referencia ingenua.** RI-NA.
**Aclaración y rechazo.** Aclaración si el sentido del par es ambiguo o falta el corte; rechazo si las patas no comparten fecha.
**Referencias.** ACI – The Financial Markets Association, *The Model Code*; Lyons (2001), *The Microstructure Approach to Exchange Rates*; BPI (2022, 2025), *Triennial Central Bank Survey of Foreign Exchange and OTC Derivatives Markets* · TMX-03.
**Prioridad y madurez.** P0 · DOCUMENTADO (alternativa: aritmética declarada `op_sin_ficha` no citable).

### FX-SETL-001 · Fechas valor y calendario de liquidación

**Identificación.** v1.0 · VIGENTE · MC-01 · Mapa: área 6.
**Perfiles y horizontes.** TRANSVERSAL · no aplica.
**Propósito.** Calcular la fecha valor de contado y de cada plazo forward u opción de un par, y la fracción de año de cada divisa, con los calendarios de las dos plazas y de EE. UU.
**Método.** (i) Contado T+2 hábiles (T+1 en USD/CAD, USD/TRY y USD/PHP); la fecha de contado debe ser hábil en ambas plazas y en EE. UU.; en pares frente al USD un festivo de EE. UU. en T+1 no retrasa el contado; en cruces, T+1 hábil en ambas plazas. (ii) Plazos desde el contado con día hábil siguiente modificado y regla de fin de mes. (iii) ON, TN, SN. (iv) Opciones: fecha de vencimiento y de entrega (contado del vencimiento). (v) Fracción de año por divisa con su base (Act/360, Act/365, Bus/252) para FX-FWD-001 y FX-CIP-001.
**Entradas mínimas.** Fecha de operación, par, plazo y calendarios de festivos de las plazas implicadas con su fuente y versión.
**Parámetros.** regla_ajuste (siguiente_modificado); fin_de_mes (true); bases (3.1).
**Salidas.** TABLA: fechas valor, días naturales y hábiles, fracciones de año por divisa. DETERMINISTA.
**Supuestos y limitaciones.** Los calendarios cambian (festivos nuevos o trasladados): la versión del calendario es parte del artefacto; plazas con fines de semana distintos se tratan con su calendario declarado.
**Tolerancias y semilla.** Igualdad exacta · null.
**Verificación.** Casos de control: USD/CAD un viernes ⇒ contado el lunes siguiente hábil; USD/JPY con festivo japonés en T+2 ⇒ contado desplazado al siguiente día hábil en Japón y EE. UU.; plazo de 1 mes desde un contado de fin de mes ⇒ último hábil del mes siguiente.
**Referencia ingenua.** RI-NA.
**Aclaración y rechazo.** Rechazo sin calendario de una de las plazas.
**Referencias.** ISDA (2006, con suplementos), *ISDA Definitions* y *FX and Currency Option Definitions* (1998); Clark (2011), *Foreign Exchange Option Pricing*, cap. 1; Wystup (2017), *FX Options and Structured Products* · TMX-03.
**Prioridad y madurez.** P0 · DOCUMENTADO (alternativa: fechas aportadas por HT-01 como dato).

### FX-FWD-001 · Puntos forward, *outright* y carry implícito

**Identificación.** v1.0 · VIGENTE · MC-01 (invitado MC-09 para curvas) · Mapa: áreas 2, 6, 12.
**Perfiles y horizontes.** TRANSVERSAL · H1–H3.
**Propósito.** Calcular el forward *outright*, los puntos forward, el rendimiento implícito de cada divisa y el carry anualizado implícito en los puntos, o reconstruir el forward teórico desde los tipos.
**Método.** (i) *Outright* = contado + puntos × escala del pip. (ii) Forward teórico por CIP `F = S·(1 + i_c·d/B_c)/(1 + i_b·d/B_b)` con fracciones de FX-SETL-001. (iii) Rendimiento implícito de la base `i_b^{impl} = [(S/F)·(1 + i_c·τ_c) − 1]/τ_b` (y simétrico para la cotizada). (iv) Carry anualizado implícito de una posición larga en la base `−(F − S)/S·(1/τ)`. (v) Curva de puntos por plazos (1S, 1M, 3M, 6M, 1A) e interpolación declarada (lineal en puntos o en rendimientos implícitos). (vi) Coste de renovación (tom-next) si se aportan los tramos cortos.
**Entradas mínimas.** Contado y puntos (o tipos de ambas divisas) del mismo corte; fechas valor; bases de días.
**Parámetros.** plazos (1M, 3M, 12M); interpolacion (rendimiento_implicito); tipos (OIS).
**Salidas.** TABLA: *outright*, puntos (pips), rendimientos implícitos (% anual), carry implícito (% anual), diferencia frente al forward teórico (pips). DETERMINISTA.
**Supuestos y limitaciones.** La diferencia entre el forward cotizado y el teórico con OIS es la base cruzada (FX-CIP-001), no un error; puntos de plazos ilíquidos interpolados se marcan.
**Tolerancias y semilla.** 1e-10 · null.
**Verificación.** Tipos iguales ⇒ puntos nulos; reconstrucción del forward teórico desde los rendimientos implícitos; signo: `i_b > i_c` ⇒ puntos negativos.
**Referencia ingenua.** RI-NA (cálculo); como predictor, el forward es RI-FWD.
**Aclaración y rechazo.** Aclaración si no consta si los puntos son medios o de un lado; rechazo con contado y puntos de fechas distintas.
**Referencias.** Hull (2022), *Options, Futures, and Other Derivatives*, cap. 5; Clark (2011); Du, Tepper y Verdelhan (2018), *Journal of Finance* · TMX-03.
**Prioridad y madurez.** P0 · IMPLEMENTADO (ejecutor `bloque_a_forex` V1.0) los pasos (ii)–(iv): forward teórico por CIP, puntos, rendimiento implícito y carry implícito, con contraste frente a un forward cotizado si se aporta; curva por plazos, interpolación y tom-next (pasos v–vi), DOCUMENTADO.

### FX-TR-001 · Rentabilidad total cambiaria y exceso de rentabilidad

**Identificación.** v1.0 · VIGENTE · MC-01 · Mapa: área 2.
**Perfiles y horizontes.** TRANSVERSAL · H1–H4.
**Propósito.** Medir la rentabilidad de una exposición cambiaria con su dirección y divisa de financiación, separando contado, carry y término cruzado, y construir su índice de rentabilidad total.
**Método.** (i) Exceso de rentabilidad por forward `R_exc = (S_{t+τ} − F_{t,τ})/S_t` para la base larga (signo invertido para `BAJISTA_BASE`). (ii) Descomposición con depósitos: contado `ΔS/S`, carry `(i_b − i_c)·τ`, cruzado `(ΔS/S)·i_b·τ`. (iii) Índice de rentabilidad total con renovación mensual de forwards (convención de Lustig, Roussanov y Verdelhan, 2011) y valoración a mercado entre renovaciones. (iv) Cestas: suma ponderada de las patas con sus pesos y la divisa de financiación. (v) Conversión a la divisa base del usuario si se pide.
**Entradas mínimas.** Contado y forwards (o tipos) del mismo corte para cada renovación; dirección; pesos y financiación en cestas.
**Parámetros.** renovacion (mensual); fuente_carry (forward; diferencial); divisa_medida (cotizada; base del usuario).
**Salidas.** SERIE: índice de rentabilidad total; TABLA: rentabilidad de contado, carry, cruzado y total en el periodo (tanto por uno) y anualizadas. DETERMINISTA.
**Supuestos y limitaciones.** Sin costes de ejecución ni de instrumentos (Bloque B); la horquilla de mercado solo entra en FX-BT-001; en divisas no entregables se usa el NDF (FX-NDF-001).
**Tolerancias y semilla.** 1e-10 · null.
**Verificación.** Contado + carry + cruzado = total; con puntos nulos el total iguala al contado; inversión de la dirección cambia el signo del exceso.
**Referencia ingenua.** RI-FWD (exceso nulo) y RI-PA (total = carry) cuando se usa como previsión.
**Aclaración y rechazo.** Aclaración sin dirección, sin divisa de financiación o sin medida; rechazo con forwards de otro corte.
**Referencias.** Lustig, Roussanov y Verdelhan (2011), *RFS*; Menkhoff, Sarno, Schmeling y Schrimpf (2012a), *Journal of Finance*; Koijen, Moskowitz, Pedersen y Vrugt (2018), *JFE* · TMX-03, TMX-06.
**Prioridad y madurez.** P0 · DOCUMENTADO (alternativa: FX-CARRY-001 núcleo v1.1 + FIN-CAGR-001).

### FX-BASKET-001 · Cestas e índices de divisas

**Identificación.** v1.0 · VIGENTE · MC-01 · Mapa: área 14.
**Perfiles y horizontes.** TRANSVERSAL · H1–H4.
**Propósito.** Construir el indicador de seguimiento de una cesta (regional, temática, de refugio, de carry) o replicar un índice de divisas publicado (DXY, índice amplio de la Fed) con su fórmula.
**Método.** (i) Composición firmada con pesos y divisa de financiación (o cesta frente a cesta). (ii) Índice geométrico `I_t = I_0·Π_j (S_{j,t}/S_{j,0})^{±w_j}` (por defecto) o aritmético de rentabilidades con rebalanceo declarado. (iii) Versión de contado y de rentabilidad total (FX-TR-001 por pata). (iv) Réplica del DXY: `50,14348112 × EURUSD^{−0,576} × USDJPY^{0,136} × GBPUSD^{−0,119} × USDCAD^{0,091} × USDSEK^{0,042} × USDCHF^{0,036}`. (v) Referencia de comparación de emergentes (8.4): cesta equiponderada de las divisas del segmento frente al USD con carry, universo ratificado en F10.
**Entradas mínimas.** Contados (y forwards si es total) del mismo corte para todas las patas; pesos y fecha de pesos.
**Parámetros.** formula (geometrica; aritmetica); rebalanceo (mensual); medida (PRECIO_CONTADO; RENTABILIDAD_TOTAL).
**Salidas.** SERIE: índice; TABLA: contribución por divisa. DETERMINISTA.
**Supuestos y limitaciones.** Pesos fijos frente a dinámicos declarados; una divisa que cambia de régimen en la ventana se marca; un índice propio no es el publicado.
**Tolerancias y semilla.** 1e-10 · null.
**Verificación.** Réplica del DXY con las cotizaciones de ICE dentro de 1e-4; pesos por lado suman 1; contribuciones suman la variación total (en log).
**Referencia ingenua.** RI-PA del índice; RI-SEG si se usa como comparación.
**Aclaración y rechazo.** Rechazo de cestas sin pesos o sin divisa de financiación (PS4).
**Referencias.** ICE, *U.S. Dollar Index Contracts: Methodology*; Junta de la Reserva Federal, *Revisions to the Federal Reserve Dollar Indexes* (Loretan, 2005); Klau y Fung (2006), *BIS Quarterly Review* · TMX-03, TMX-06.
**Prioridad y madurez.** P1 · DOCUMENTADO (alternativa: ST-DESC-001 sobre el índice publicado aportado como dato).

### FX-REER-001 · Tipos efectivos nominal y real y su desviación

**Identificación.** v1.0 · VIGENTE · MC-01 (invitado MC-03 para tendencia) · Mapa: áreas 14, 13.
**Perfiles y horizontes.** TRANSVERSAL · H3–H4.
**Propósito.** Medir la posición del tipo efectivo real de una divisa frente a su historia y, si se pide, construir un NEER/REER propio.
**Método.** (i) Serie publicada del BPI (amplia, 64 economías, o estrecha, 27) o del FMI como dato; convención «subida = apreciación». (ii) REER propio: `NEER = Π_j S_j^{w_j}`, `REER = NEER × Π_j (P/P_j)^{w_j}` (IPC), pesos de doble ponderación de exportaciones con fecha. (iii) Desviación frente a la media de 10–20 años (log), percentil histórico y z-score. (iv) En emergentes en convergencia, desviación frente a una tendencia (Mann-Kendall + Sen o filtro de Hamilton) por Balassa-Samuelson, declarada.
**Entradas mínimas.** ≥ 10 años mensuales (≥ 20 recomendados); para el propio, contados y precios de todos los socios con pesos.
**Parámetros.** fuente (BPI_amplio); ventana_media (20 años); destendencia (false; true en PERF-FX-EM si se pide).
**Salidas.** TABLA: desviación (%), percentil, z-score, contribuciones por socio (si es propio). DETERMINISTA (índice) y ESTADISTICA (percentil y tendencia).
**Supuestos y limitaciones.** La media de largo plazo puede no ser el equilibrio (cambios estructurales, términos de intercambio); las revisiones de pesos del BPI cambian la historia (vintage); no es previsión.
**Tolerancias y semilla.** 1e-10 (índice) · null.
**Verificación.** Pesos suman 1; REER propio frente al del BPI: correlación de variaciones mensuales > 0,95 o discrepancia declarada.
**Referencia ingenua.** RI-PA del tipo real; RI-MH (reversión a la media) si se usa como señal.
**Aclaración y rechazo.** Rechazo con < 10 años o con rupturas de régimen no declaradas.
**Referencias.** Klau y Fung (2006), «The New BIS Effective Exchange Rate Indices», *BIS Quarterly Review*; Chinn (2006), «A Primer on Real Effective Exchange Rates», *Open Economies Review*; Bayoumi, Lee y Jayanthi (2006), IMF WP 06/149 · TMX-04.
**Prioridad y madurez.** P1 · DOCUMENTADO (alternativa: ST-DESC-001 sobre la serie del BPI).

### FX-POS-001 · Percentil de posicionamiento y flujos

**Identificación.** v1.0 · VIGENTE · MC-01 · Mapa: área 35.
**Perfiles y horizontes.** TRANSVERSAL · H1–H3.
**Propósito.** Situar el posicionamiento especulativo neto en una divisa frente a su historia y medir su cambio (dato del informe PFV de AG-21: `neto_cftc`, `percentil_historico`, `cambio_semanal`) y la marca de saturación narrativa (9.1).
**Método.** (i) Posición neta de «fondos apalancados» y de «gestores de activos» del informe *Traders in Financial Futures* de la CFTC (o no comerciales del informe heredado), en contratos y en USD con el contado de la fecha del informe. (ii) Normalización por interés abierto. (iii) Percentil empírico y z-score frente a 3 años (y 5 años como sensibilidad). (iv) Cambio semanal y de 4 semanas. (v) Decil extremo a favor de una dirección declarada. (vi) Flujos (cartera, encuestas de posicionamiento) aportados como dato: percentil análogo.
**Entradas mínimas.** ≥ 156 informes semanales; fecha de datos (martes) y de publicación (viernes).
**Parámetros.** categoria (fondos_apalancados); ventana (3 años); normalizar_oi (true).
**Salidas.** TABLA: neto (contratos, USD), % del interés abierto, percentil, z-score, cambios, marca de decil extremo. ESTADISTICA.
**Supuestos y limitaciones.** Solo futuros listados en EE. UU. (EUR, JPY, GBP, CHF, CAD, AUD, NZD, MXN, BRL, ZAR): una fracción del mercado; conocible solo desde el viernes (M13); el percentil histórico no es una probabilidad futura.
**Tolerancias y semilla.** 1e-10 · null.
**Verificación.** Percentiles monótonos; recuento de informes; neto = largos − cortos.
**Referencia ingenua.** RI-TB (frecuencia de giros tras deciles extremos) si se usa como señal.
**Aclaración y rechazo.** Rechazo para divisas sin futuro CFTC (se ofrece el dato de flujos aportado).
**Referencias.** CFTC, *Traders in Financial Futures: Explanatory Notes*; Klitgaard y Weir (2004), *FRBNY Current Issues*; Brunnermeier, Nagel y Pedersen (2008) · TMX-06.
**Prioridad y madurez.** P1 · DOCUMENTADO (alternativa: ST-DESC-001 sobre la serie aportada).

### FX-NDF-001 · NDF, rendimientos implícitos y brecha *onshore*–*offshore*

**Identificación.** v1.0 · VIGENTE · MC-01 (invitado MC-09) · Mapa: áreas 34, 12.
**Perfiles y horizontes.** PERF-FX-EM · H1–H3.
**Propósito.** Obtener el carry invertible de una divisa no entregable, su rendimiento implícito *offshore* y la brecha frente al mercado *onshore* (CNH frente a CNY; NDF frente a *onshore* en INR, KRW, TWD, IDR, PHP, BRL, CLP, COP, PEN, EGP, NGN).
**Método.** (i) NDF liquidado en USD contra la fijación de referencia declarada (p. ej., PTAX en BRL, KFTC18 en KRW, TAIFX1 en TWD, JISDOR en IDR, «dólar observado» en CLP, TRM en COP). (ii) Rendimiento implícito de la divisa `i_impl = [(F_NDF/S)·(1 + i_USD·τ) − 1]/τ` (USD como base). (iii) Brecha implícito *offshore* − tipo *onshore* comparable (pb). (iv) Brecha de contado CNH − CNY (pips y %) y frente a la fijación central del PBoC. (v) Carry de la exposición con su dirección.
**Entradas mínimas.** Contado de referencia, NDF por plazos y fijación con fechas; tipo USD y tipo *onshore* comparable.
**Parámetros.** plazos (1M, 3M); fijacion (declarada por par).
**Salidas.** TABLA: rendimiento implícito (% anual), brecha (pb), carry (% anual), brecha CNH–CNY. DETERMINISTA.
**Supuestos y limitaciones.** La brecha refleja controles de capital y segmentación, no arbitraje disponible; la fijación puede apartarse del mercado en tensiones; en divisas con tipo oficial y paralelo, el NDF puede referirse a un tipo no invertible.
**Tolerancias y semilla.** 1e-10 · null.
**Verificación.** Sin controles (brecha nula) el rendimiento implícito reproduce el *onshore*; coherencia con FX-FWD-001 en divisas entregables.
**Referencia ingenua.** RI-FWD (el NDF como predictor) y RI-PA.
**Aclaración y rechazo.** Aclaración sin fijación declarada; rechazo si el NDF y el contado tienen fechas o fijaciones distintas.
**Referencias.** Lipscomb (2005), «An Overview of Non-Deliverable Foreign Exchange Forward Markets», FRBNY; McCauley, Shu y Ma (2014), «Non-Deliverable Forwards: 2013 and Beyond», *BIS Quarterly Review*; Ilzetzki, Reinhart y Rogoff (2019), *QJE* · TMX-03.
**Prioridad y madurez.** P1 · DOCUMENTADO (alternativa: FX-CARRY-001 núcleo v1.1 con tipos aportados y limitación «*onshore* no invertible»).

### 8.2 Paridades, equilibrio y macro cuantitativa (MC-03)

### FX-CARRY-001 · Diferencial de tipos, carry y carry ajustado por volatilidad

**Identificación.** v2.0 · VIGENTE · MC-03 · Mapa: áreas 12, 29. (v1.1 se conserva para re-ejecuciones.)
**Perfiles y horizontes.** TRANSVERSAL · H1–H3.
**Propósito.** Diferencial de tipos, carry anual de la exposición con su signo respecto de la dirección, carry ajustado por volatilidad, carry real y equilibrio del carry, de un par, una cesta o una sección cruzada de divisas.
**Método.** (i) Diferencial con base declarada (OIS a 3 meses por defecto; 2 años para el diferencial de política en FX-RDIFF-001) y bases de días de FX-SETL-001. (ii) Carry anual de la exposición: `(i_b − i_c)` para `ALCISTA_BASE`, `(i_c − i_b)` para `BAJISTA_BASE`; segunda vía desde los puntos forward (FX-FWD-001); la diferencia es la base cruzada. (iii) **Carry ajustado** = carry anual / σ anual (implícita ATM a 3 meses; realizada de 3 meses si no hay implícita, declarado). (iv) Carry real = diferencial de tipos reales (inflación subyacente o esperada declarada). (v) Equilibrio del carry en el horizonte: movimiento adverso del contado que lo anula, en % y en desviaciones típicas. (vi) Sección cruzada: ordenación por carry y por carry ajustado (sin seleccionar: la selección es del Analista). (vii) Descomposición realizada del núcleo v1.1: carry + variación del contado = rentabilidad total.
**Entradas mínimas.** Tipos de ambas divisas alineados y con base; contado; forward opcional; volatilidad implícita o ≥ 63 sesiones para realizada.
**Parámetros.** base_tipos (OIS_3M); vol (implicita_3m); inflacion (subyacente); horizonte (3 meses).
**Salidas.** TABLA: diferencial (% anual), carry de la exposición (% anual) y signo, carry ajustado (adimensional), carry real (% anual), equilibrio (% y σ), rentabilidad total realizada descompuesta. DETERMINISTA (aritmética) y ESTADISTICA (volatilidad realizada).
**Supuestos y limitaciones.** El carry es la rentabilidad con contado sin cambio, no una previsión; la paridad descubierta no se cumple a corto plazo; el carry tiene asimetría negativa (FX-TAIL-001); en divisas no entregables se usa FX-NDF-001.
**Tolerancias y semilla.** 1e-8 · null.
**Verificación.** Carry por diferencial frente a carry por puntos (diferencia = base, declarada); tipos iguales ⇒ carry nulo; inversión de la dirección cambia el signo; carry + variación del contado = total.
**Referencia ingenua.** RI-PA (rentabilidad total = carry) y RI-FWD (exceso nulo).
**Aclaración y rechazo.** Aclaración si la base de tipos o la dirección son ambiguas; rechazo con tipos de distinto riesgo de crédito sin declarar.
**Referencias.** Fama (1984), *JFE*; Lustig y Verdelhan (2007), *AER*; Burnside, Eichenbaum, Kleshchelski y Rebelo (2011), *RFS*; Koijen, Moskowitz, Pedersen y Vrugt (2018), *JFE*; Menkhoff, Sarno, Schmeling y Schrimpf (2012a), *Journal of Finance* · TMX-03, TMX-06.
**Prioridad y madurez.** P0 · IMPLEMENTADO (v2.0 en el ejecutor `bloque_a_forex` V1.0) los pasos (i)–(v) y (vii): diferencial, carry de la exposición con su signo, carry ajustado por volatilidad (realizada de 3 meses si no se aporta implícita, declarado), carry real si se aportan inflaciones, equilibrio y descomposición; sección cruzada (vi) y segunda vía por puntos forward, DOCUMENTADO.

### FX-CIP-001 · Paridad cubierta y base cruzada

**Identificación.** v1.0 · VIGENTE · MC-03 · Mapa: área 12.
**Perfiles y horizontes.** PERF-FX-G10, PERF-FX-EM (divisas entregables con OIS líquido) · H1–H3.
**Propósito.** Medir la desviación de la paridad cubierta (base cruzada) por plazo y su posición histórica (dato del informe PFV de AG-21: `base_cruzada`).
**Método.** Con `S` en divisa extranjera por USD y `ρ = (1/τ)·ln(F/S)`: `x = i_USD − (i_ext − ρ)` en pb, con tipos OIS de riesgo comparable; por plazos (3M, 1A; 5A con swaps de divisas si se aportan); percentil frente a 3–5 años; efecto de fin de trimestre y de año (diferencia entre plazos que cruzan y no cruzan la fecha).
**Entradas mínimas.** Contado, forwards y OIS del mismo corte; ≥ 2 años para percentiles.
**Parámetros.** plazos (3M, 12M); tipos (OIS); ventana (3 años).
**Salidas.** TABLA: base (pb) por plazo, percentil, efecto de fin de periodo (pb). DETERMINISTA (base) y ESTADISTICA (percentil).
**Supuestos y limitaciones.** Tipos de distinto riesgo (IBOR frente a OIS) crean bases espurias; la base no es arbitraje accesible para cualquier agente (restricciones de balance); en divisas con controles se rechaza (FX-NDF-001).
**Tolerancias y semilla.** 1e-10 · null.
**Verificación.** Forward teórico por CIP ⇒ base nula; signo: obtener USD sintéticamente más caro ⇒ x < 0.
**Referencia ingenua.** RI-PA de la base si se usa como señal.
**Aclaración y rechazo.** Rechazo con tipos de riesgo no comparable o divisas con controles.
**Referencias.** Du, Tepper y Verdelhan (2018), «Deviations from Covered Interest Rate Parity», *Journal of Finance*; Avdjiev, Du, Koch y Shin (2019), «The Dollar, Bank Leverage, and Deviations from Covered Interest Parity», *AER: Insights*; Borio, McCauley, McGuire y Sushko (2016), *BIS Quarterly Review* · TMX-03.
**Prioridad y madurez.** P1 · DOCUMENTADO (alternativa: diferencia carry por puntos − carry por OIS con FX-CARRY-001, `op_sin_ficha`).

### FX-UIP-001 · Paridad descubierta y regresión de Fama

**Identificación.** v1.0 · VIGENTE · MC-03 · Mapa: áreas 12, 11.
**Perfiles y horizontes.** TRANSVERSAL · H3–H4 (como descripción histórica; nunca como previsión).
**Propósito.** Estimar la relación histórica entre la prima forward y la variación posterior del contado de un par o de un panel (coeficiente de Fama) y la prima de riesgo cambiaria implícita.
**Método.** `Δs_{t+τ} = α + β·(f_t − s_t) + ε` con datos no solapados o HAC con `L ≥ h − 1`; contraste de `β = 1` y de `β = 0`; panel con efectos fijos y errores agrupados por fecha; estabilidad por subperiodos (antes y después de 2008) y por régimen de volatilidad; horizontes de 1, 3, 12 meses y, si hay datos, 5–10 años (Chinn y Meredith, 2004).
**Entradas mínimas.** ≥ 10 años mensuales de contado y forwards del mismo corte.
**Parámetros.** horizonte (1M); panel (false); subperiodos (true).
**Salidas.** TABLA: α, β con EE e IC, contrastes, R², estabilidad. ESTADISTICA.
**Supuestos y limitaciones.** `β < 1` describe la prima de carry histórica, no garantiza su persistencia; sesgo por pocas observaciones independientes en horizontes largos; *peso problem* (Burnside et al., 2011).
**Tolerancias y semilla.** 1e-6 · null.
**Verificación.** Serie simulada con UIP exacta ⇒ β ≈ 1; segunda vía: datos no solapados frente a HAC.
**Referencia ingenua.** RI-PA (β = 0) y RI-FWD (β = 1) como hipótesis contrastadas.
**Aclaración y rechazo.** Rechazo con < 10 años o con regímenes de tipo fijo en la ventana.
**Referencias.** Fama (1984), *JFE*; Froot y Thaler (1990), *JEP*; Hodrick (1987), *The Empirical Evidence on the Efficiency of Forward and Futures Foreign Exchange Markets*; Bansal y Dahlquist (2000), *JIE*; Chinn y Meredith (2004), *IMF Staff Papers* · TMX-03, TMX-08.
**Prioridad y madurez.** P2 · DOCUMENTADO.

### FX-PPP-001 · Paridad del poder adquisitivo absoluta y relativa

**Identificación.** v1.0 · VIGENTE · MC-03 · Mapa: área 13. Sustituye a FX-PPA-001.
**Perfiles y horizontes.** PERF-FX-G10, PERF-FX-EM, PERF-FX-FACT (factor valor) · H4 (H3 limitado).
**Propósito.** Desviación del tipo de cambio respecto de su valor de PPA (relativa y, si hay datos, absoluta ajustada por Balassa-Samuelson) y persistencia estimada de esa desviación.
**Método.** (i) PPA relativa `S_PPA,t = S_0·(P_{c,t}/P_{c,0})/(P_{b,t}/P_{b,0})` con base declarada (media de largo plazo por defecto; año base como sensibilidad) e índices de precios con vintage (IPC por defecto; deflactor o precios de producción como sensibilidad). (ii) PPA absoluta `P_c/P_b` con niveles de precios del PCI o la Penn World Table; ajuste de Balassa-Samuelson por regresión transversal del nivel de precios relativo sobre el PIB por habitante en PPA, desviación = residuo. (iii) Desviación `100·ln(S/S_PPA)` con signo referido a la base (positiva = base cara). (iv) Persistencia: AR(1) del tipo real con estimador insesgado en mediana (Andrews, 1993) y vida media `ln 0,5/ln ρ` con IC; variante ESTAR si se pide.
**Entradas mínimas.** Tipo de cambio y dos índices de precios con base y vintage; ≥ 10 años para la desviación (≥ 20 para la vida media).
**Parámetros.** base (media_largo_plazo; año); indice_precios (IPC); ajuste_bs (false; true en PERF-FX-EM); persistencia (AR1_insesgado).
**Salidas.** TABLA: desviación (%) por base y por índice (banda de sensibilidad), desviación ajustada por Balassa-Samuelson, ρ, vida media (años) con IC 90 %. DETERMINISTA (desviación) y ESTADISTICA (ajuste y persistencia).
**Supuestos y limitaciones.** Ancla de largo plazo (vida media habitual 3–5 años, con IC muy amplios); dependiente de la base y del índice; no es previsión ni valor objetivo; regímenes cambiados en la ventana invalidan la base.
**Tolerancias y semilla.** 1e-8 · null.
**Verificación.** Inflaciones iguales ⇒ desviación constante igual a la de la base; inversión del par cambia el signo; segunda vía: FX-PPA-001 v1.1 y otra base.
**Referencia ingenua.** RI-PA del tipo de cambio; RI-MH (reversión a la media del tipo real) si se usa como señal.
**Aclaración y rechazo.** Rechazo con canastas o periodicidades incompatibles o con < 10 años.
**Referencias.** Rogoff (1996), «The Purchasing Power Parity Puzzle», *JEL*; Taylor y Taylor (2004), *JEP*; Taylor, Peel y Sarno (2001), *International Economic Review*; Balassa (1964), *JPE*; Samuelson (1964), *REStat*; Andrews (1993), *Econometrica*; Murray y Papell (2002), *JIE* · TMX-04.
**Prioridad y madurez.** P1 · IMPLEMENTADO (ejecutor `bloque_a_forex` V1.0, versión sencilla): PPA relativa con base en la media de largo plazo, desviación y AR(1) por MCO con vida media; PPA absoluta, ajuste de Balassa-Samuelson, estimador de Andrews y ESTAR, DOCUMENTADO (alternativa: FX-PPA-001 v1.1, declarada).

### FX-PPA-001 · Desviación de paridad de poder adquisitivo relativa (deprecada)

**Identificación.** v1.1 · DEPRECADA · MC-03 · Mapa: área 13.
**Perfiles y horizontes.** PERF-FX-G10, PERF-FX-EM · H4.
**Propósito.** Se conserva solo para re-ejecuciones CT-10 de artefactos que la citan y como alternativa implementada de FX-PPP-001 mientras esta esté documentada.
**Método, entradas, parámetros, salidas, supuestos, tolerancias y verificación.** Los de la v1.1 del Catálogo V5.0 (senda = cambio base × razón de índices de precios; desviación log-diferencia; vida media por AR(1) por MCO, sin corrección de sesgo).
**Referencia ingenua.** RI-PA del tipo de cambio.
**Aclaración y rechazo.** Toda entrega declara «ficha deprecada; vida media sin corrección del sesgo de muestra pequeña».
**Referencias.** Rogoff (1996); Taylor y Taylor (2004) · TMX-04.
**Prioridad y madurez.** — · Implementado (heredado de la línea V3.0 del Bloque A general).

### FX-BEER-001 · Tipo de cambio real de equilibrio conductual (BEER)

**Identificación.** v2.0 · VIGENTE · MC-03 · Mapa: áreas 13, 11.
**Perfiles y horizontes.** PERF-FX-G10, PERF-FX-EM · H4 (H3 limitado).
**Propósito.** Desalineamiento del tipo de cambio real efectivo (o bilateral) frente a su equilibrio estimado por fundamentales.
**Método.** (i) Orden de integración de `q` y de los fundamentales. (ii) Cointegración `q_t = β'Z_t + ε_t` con Z = términos de intercambio, productividad relativa (Balassa-Samuelson), activos exteriores netos/PIB, diferencial de tipos reales y, en emergentes, consumo público o apertura; DOLS (Stock y Watson, 1993) con 2 adelantos y retardos por defecto, o Johansen. (iii) Desalineamiento actual `q − β'Z_actual` y total `q − β'Z_sostenible` (fundamentales filtrados por Hamilton o HP declarado). (iv) Velocidad de corrección (MCE) y vida media. (v) Estabilidad del vector (pruebas recursivas) y panel con efectos fijos para economías con series cortas.
**Entradas mínimas.** Series trimestrales ≥ 20 años (≥ 15 con advertencia), con vintages; panel ≥ 10 economías si la serie individual es corta.
**Parámetros.** metodo (DOLS; Johansen; panel_DOLS); retardos (2); filtro_sostenible (Hamilton).
**Salidas.** TABLA: coeficientes con EE, equilibrio, desalineamiento actual y total (%) con IC, vida media (años), diagnóstico de estabilidad. ESTADISTICA.
**Supuestos y limitaciones.** Equilibrio dependiente de la especificación (entregar al menos dos especificaciones en PLAN_STD); rupturas de régimen cambiario invalidan la muestra; los fundamentales sostenibles son juicio declarado; no es previsión.
**Tolerancias y semilla.** 1e-6 · null.
**Verificación.** Residuo de media nula; segunda vía: FX-PPP-001 y Johansen frente a DOLS.
**Referencia ingenua.** RI-PA y PPA (media histórica del tipo real).
**Aclaración y rechazo.** Rechazo sin cointegración contrastada (SUPUESTOS_VIOLADOS, con FX-PPP-001 como alternativa) o con tipo fijo en la ventana (PERFIL_NO_COMPATIBLE, con FX-PEG-001).
**Referencias.** Clark y MacDonald (1998), IMF WP 98/67; MacDonald (2007), *Exchange Rate Economics: Theories and Evidence*; Stock y Watson (1993), *Econometrica*; Phillips et al. (2013), IMF WP 13/272; Cubeddu et al. (2019), IMF WP 19/65 · TMX-04.
**Prioridad y madurez.** P1 · DOCUMENTADO.

### FX-FEER-001 · Tipo de cambio de equilibrio fundamental y balanza macro

**Identificación.** v1.0 · VIGENTE · MC-03 · Mapa: áreas 13, 16.
**Perfiles y horizontes.** PERF-FX-G10, PERF-FX-EM · H4.
**Propósito.** Ajuste del tipo real necesario para llevar el saldo por cuenta corriente ajustado por el ciclo a su norma (enfoque FEER y balanza macro del FMI).
**Método.** (i) Saldo por cuenta corriente/PIB ajustado por la brecha de producción propia y de los socios y por términos de intercambio (coeficientes aportados o estimados). (ii) Norma del saldo (aportada por el solicitante con su fuente, p. ej., la del EBA del FMI, o escenarios). (iii) Semielasticidad `η` del saldo/PIB al tipo real, derivada de elasticidades comerciales y de la apertura. (iv) Desalineamiento ≈ `(CA_ajustada − CA_norma)/η` (positivo = la divisa puede apreciarse en términos reales). (v) Tabla de sensibilidad norma × η.
**Entradas mínimas.** Saldo por cuenta corriente, brechas, apertura y elasticidades o `η` declarada; norma con fuente.
**Parámetros.** eta (aportada; rango de sensibilidad ±50 %); norma (aportada).
**Salidas.** TABLA: desalineamiento (%) con banda de sensibilidad norma × η. DETERMINISTA dada la norma y η; banda de sensibilidad obligatoria.
**Supuestos y limitaciones.** Extremadamente sensible a la norma y a η; equilibrio de medio plazo; no aplica a divisas con tipo fijo como valoración de mercado.
**Tolerancias y semilla.** 1e-10 · null.
**Verificación.** Saldo igual a la norma ⇒ desalineamiento nulo; coherencia de signos.
**Referencia ingenua.** RI-PA; FX-BEER-001 y FX-PPP-001 como contraste.
**Aclaración y rechazo.** Rechazo sin norma o sin η declaradas.
**Referencias.** Williamson (1994), *Estimating Equilibrium Exchange Rates*; Lee, Milesi-Ferretti, Ostry, Prati y Ricci (2008), IMF Occasional Paper 261 (CGER); Phillips et al. (2013); Cubeddu et al. (2019) · TMX-04.
**Prioridad y madurez.** P2 · DOCUMENTADO.

### FX-RDIFF-001 · Diferencial de tipos a 2 años y valor razonable a corto

**Identificación.** v1.0 · VIGENTE · MC-03 · Mapa: áreas 15, 11.
**Perfiles y horizontes.** PERF-FX-G10, PERF-FX-EM (con curva líquida) · H1–H3.
**Propósito.** Medir la relación reciente entre un par y el diferencial de tipos a 2 años (nominal y real) de sus divisas, y la desviación del par respecto del valor que implica esa relación.
**Método.** (i) Diferencial a 2 años (OIS o deuda pública, declarado) y diferencial real (menos inflación esperada a 2 años si se aporta). (ii) Regresión rodante en **variaciones** (Δln S sobre Δ diferencial, semanal, 26–52 semanas) para la sensibilidad (pips o % por 10 pb); en niveles solo si FX-COINT-001 acepta cointegración en la ventana. (iii) Valor razonable = nivel implícito por la relación estimada y el diferencial actual; desviación en % y en desviaciones típicas de los residuos. (iv) Correlación rodante y su estabilidad.
**Entradas mínimas.** ≥ 1 año semanal (≥ 2 recomendados) de par y diferencial del mismo corte.
**Parámetros.** tenor (2A); ventana (52 semanas); especificacion (variaciones).
**Salidas.** TABLA: sensibilidad con IC, correlación, valor razonable, desviación (% y σ), estabilidad. ESTADISTICA.
**Supuestos y limitaciones.** Relación inestable que cambia con el régimen (riesgo, intervención, flujos de cobertura); un valor razonable de regresión no es equilibrio ni previsión; en niveles sin cointegración la relación es espuria.
**Tolerancias y semilla.** 1e-6 · null.
**Verificación.** Segunda vía: ventana alternativa y MCO con HAC frente a robusta; inversión del par cambia el signo de la sensibilidad.
**Referencia ingenua.** RI-PA del par.
**Aclaración y rechazo.** Rechazo de la especificación en niveles sin cointegración; aclaración si el tenor o el tipo de curva no constan.
**Referencias.** Engel y West (2005), *JPE*; Engel (2016), «Exchange Rates, Interest Rates, and the Risk Premium», *AER*; Clarida, Galí y Gertler (2002) · TMX-01, TMX-04.
**Prioridad y madurez.** P1 · DOCUMENTADO (alternativa: FX-CORR-001 entre variaciones del par y del diferencial).

### FX-TOT-001 · Términos de intercambio y sensibilidad a materias primas

**Identificación.** v1.0 · VIGENTE · MC-03 · Mapa: áreas 16, 11.
**Perfiles y horizontes.** PERF-FX-G10 (G10M), PERF-FX-EM · H2–H4.
**Propósito.** Construir un índice de términos de intercambio de materias primas de una divisa y medir la sensibilidad del par a él (AUD a metales, NZD a lácteos, CAD y NOK al petróleo, CLP y PEN al cobre, COP y MXN al petróleo, ZAR al oro y platino).
**Método.** (i) Índice ponderado por la cuota de cada materia prima en las exportaciones (pesos con fecha y fuente; deflactado por un índice de precios de importación si se pide). (ii) Regresión rodante en variaciones del par sobre el índice (y el dólar amplio y un factor de riesgo como controles), HAC. (iii) Relación de largo plazo del tipo real con los términos de intercambio por cointegración (FX-COINT-001) si hay ≥ 15 años. (iv) Desviación del par frente al valor implícito.
**Entradas mínimas.** Precios de materias primas y pesos de exportación; ≥ 2 años semanales para la sensibilidad.
**Parámetros.** pesos (cuota de exportación); controles (dolar, riesgo); ventana (104 semanas).
**Salidas.** TABLA: índice, betas con IC, R², desviación frente al implícito. ESTADISTICA.
**Supuestos y limitaciones.** Relación dependiente del régimen y de la política monetaria; la causalidad puede invertirse a alta frecuencia (Chen, Rogoff y Rossi, 2010); pesos de exportación cambiantes.
**Tolerancias y semilla.** 1e-6 · null.
**Verificación.** Índice con un único producto reproduce su precio; segunda vía: ventana alternativa.
**Referencia ingenua.** RI-PA del par.
**Aclaración y rechazo.** Rechazo sin pesos de exportación.
**Referencias.** Chen y Rogoff (2003), «Commodity Currencies», *JIE*; Cashin, Céspedes y Sahay (2004), *JDE*; Chen, Rogoff y Rossi (2010), *QJE*; Ferraro, Rogoff y Rossi (2015), *JIMF* · TMX-04.
**Prioridad y madurez.** P1 · DOCUMENTADO (alternativa: FX-CORR-001).

### FX-TAYLOR-001 · Reglas de Taylor y divergencia de política monetaria

**Identificación.** v1.0 · VIGENTE · MC-03 · Mapa: área 15.
**Perfiles y horizontes.** PERF-FX-G10, PERF-FX-EM · H3–H4.
**Propósito.** Tipo oficial implícito por una regla de Taylor para cada banco central, brecha frente al tipo vigente y al descontado, y diferencial de reglas entre dos economías.
**Método.** `i* = r* + π + a·(π − π_obj) + b·brecha`, con `a = b = 0,5` (Taylor, 1993) por defecto y variantes (`b = 1`, con suavizado `i_t = ρ·i_{t−1} + (1 − ρ)·i*`); `r*` y brecha aportados con fuente (p. ej., estimaciones de Holston-Laubach-Williams) y escenarios; inflación subyacente o esperada declarada; brecha frente al tipo vigente y frente a la senda de MON-EXP-001; diferencial de reglas entre dos bancos centrales.
**Entradas mínimas.** Inflación, objetivo, brecha y `r*` con fuente y vintage; tipo vigente.
**Parámetros.** a (0,5); b (0,5; 1,0); suavizado (false); escenarios_rstar (±0,5 pp).
**Salidas.** TABLA: tipo implícito (%) por variante, brechas (pb), diferencial de reglas (pb), banda por escenarios de `r*` y brecha. DETERMINISTA dadas las entradas; banda de sensibilidad obligatoria.
**Supuestos y limitaciones.** `r*` y la brecha son inobservables y se revisan; la regla describe, no prescribe; en emergentes con objetivos cambiarios explícitos su uso es limitado.
**Tolerancias y semilla.** 1e-10 · null.
**Verificación.** π = π_obj y brecha nula ⇒ i* = r* + π_obj.
**Referencia ingenua.** RI-PA (tipo sin cambios); como predictor cambiario, evaluado con Clark-West frente a RI-PA (Molodtsova y Papell, 2009).
**Aclaración y rechazo.** Rechazo sin fuente de `r*` y de la brecha.
**Referencias.** Taylor (1993), *Carnegie-Rochester Conference Series*; Molodtsova y Papell (2009), *JIE*; Engel y West (2006), *JMCB*; Holston, Laubach y Williams (2017), *JIE* · TMX-04.
**Prioridad y madurez.** P2 · DOCUMENTADO.

### FX-SURP-001 · Sorpresas macro y monetarias y respuesta cambiaria

**Identificación.** v1.0 · VIGENTE · MC-03 · Mapa: áreas 15, 11.
**Perfiles y horizontes.** PERF-FX-G10, PERF-FX-EM · H1–H2.
**Propósito.** Estandarizar sorpresas de datos y de decisiones de bancos centrales y medir la respuesta del par (dato del informe BCM de AG-09: `sorpresa_reciente`; banda GC0 de «sorpresa superior a 1 desviación típica»).
**Método.** (i) Sorpresa macro `(dato − consenso)/σ(dato − consenso)` con σ de la historia del indicador (Balduzzi, Elton y Green, 2001). (ii) Sorpresa monetaria: variación del OIS o del futuro a 1–3 meses en la ventana del anuncio (Kuttner, 2001) y componente de orientación (variación del tramo a 1–2 años, Gürkaynak, Sack y Swanson, 2005). (iii) Respuesta del par en ventana intradía (30–60 min) si hay datos de alta frecuencia; diaria con advertencia de contaminación. (iv) Regresión de respuestas sobre sorpresas (pips por 1σ o por 10 pb) con HAC; asimetría por signo. (v) Índice agregado de sorpresas relativas de dos economías (media móvil ponderada de sorpresas estandarizadas) si se pide.
**Entradas mínimas.** Datos y consenso con fecha y hora; ≥ 30 eventos para regresiones.
**Parámetros.** ventana_evento (60 min; diaria); estandarizacion (historica_5a).
**Salidas.** TABLA: sorpresa estandarizada, respuesta (pips y %), sensibilidades con IC, índice agregado. ESTADISTICA.
**Supuestos y limitaciones.** El consenso de encuestas tiene sesgos; respuestas inestables en el tiempo y dependientes del régimen; ventanas diarias mezclan eventos.
**Tolerancias y semilla.** 1e-8 · null.
**Verificación.** Dato igual al consenso ⇒ sorpresa nula; segunda vía: ventana alternativa.
**Referencia ingenua.** RI-PA (respuesta nula).
**Aclaración y rechazo.** Rechazo sin hora del anuncio en ventanas intradía o sin consenso.
**Referencias.** Andersen, Bollerslev, Diebold y Vega (2003), «Micro Effects of Macro Announcements», *AER*; Balduzzi, Elton y Green (2001), *JFQA*; Kuttner (2001); Gürkaynak, Sack y Swanson (2005); Faust, Rogers, Wang y Wright (2007), *JME* · TMX-01, TMX-04.
**Prioridad y madurez.** P1 · DOCUMENTADO (alternativa: ST-DESC-001 sobre sorpresas aportadas).

### 8.3 Factores y momentum (MC-09)

### FX-MOM-001 · Momentum cambiario transversal y de serie temporal

**Identificación.** v2.0 · VIGENTE · MC-09 · Mapa: áreas 29, 8. (El carry ajustado de la v1.0 pasa a FX-CARRY-001 v2.0.)
**Perfiles y horizontes.** TRANSVERSAL · H2–H3 (H1 limitado; ESTR sin H1).
**Propósito.** Señales de momentum de un par, una cesta o una sección cruzada de divisas, en rentabilidad total.
**Método.** (i) Rentabilidad total (FX-TR-001) a 1, 3, 6 y 12 meses, con y sin el último mes. (ii) **Serie temporal** (Moskowitz, Ooi y Pedersen, 2012): signo de la rentabilidad en exceso de 12 meses y señal escalada por volatilidad (`señal/σ_ex-ante`, σ por EWMA). (iii) **Transversal** (Menkhoff, Sarno, Schmeling y Schrimpf, 2012b): rango de la rentabilidad de formación (1–12 meses) dentro del universo declarado (G10 frente al USD, emergentes del segmento, todo el universo). (iv) Persistencia de la señal y número de cambios de signo en 12 meses. (v) Fuerza de tendencia de apoyo con FX-TREND-001 si se pide.
**Entradas mínimas.** Contado y forwards (o diferenciales) diarios ≥ 2 años (≥ 13 meses para la señal de 12 meses); universo con su fecha para la versión transversal.
**Parámetros.** retrospecciones (1, 3, 12 meses); saltar_ultimo_mes (false; true en 12-1); vol_escalado (EWMA 60 días); universo (declarado).
**Salidas.** TABLA: rentabilidades de formación (%), señales TSMOM (±1 y escalada), rangos y percentiles transversales, persistencia. ESTADISTICA.
**Supuestos y limitaciones.** El momentum cambiario sufre giros bruscos en cambios de régimen e intervenciones; tras costes es débil en el G10 (Menkhoff et al., 2012b); la señal no es previsión: su habilidad frente a RI-PA solo la mide FX-RW-001.
**Tolerancias y semilla.** 1e-10 · null.
**Verificación.** Coherencia con FX-TR-001; inversión del par cambia el signo; serie con tendencia lineal ⇒ señal positiva estable.
**Referencia ingenua.** RI-PA (sin señal) y RI-FWD (exceso nulo).
**Aclaración y rechazo.** Rechazo sin dirección del par declarada o sin universo en la versión transversal.
**Referencias.** Menkhoff, Sarno, Schmeling y Schrimpf (2012b), «Currency Momentum Strategies», *JFE*; Moskowitz, Ooi y Pedersen (2012), «Time Series Momentum», *JFE*; Asness, Moskowitz y Pedersen (2013), *Journal of Finance*; Okunev y White (2003), *JFQA* · TMX-06.
**Prioridad y madurez.** P1 · IMPLEMENTADO (ejecutor `bloque_a_forex` V1.0) sobre el contado: 12-1, señal TSMOM (signo y escalada por volatilidad) y rango transversal en el universo del segmento; rentabilidad total (FX-TR-001) y persistencia de la señal, DOCUMENTADO.

### FX-FACT-001 · Factores cambiarios: dólar, carry, valor y momentum

**Identificación.** v1.0 · VIGENTE · MC-09 · Mapa: áreas 29, 27.
**Perfiles y horizontes.** PERF-FX-FACT (y PERF-FX-G10, PERF-FX-EM para medir la exposición de un par a los factores) · H2–H4.
**Propósito.** Construir las carteras y los factores cambiarios documentados, medir su rentabilidad, su régimen y su *crowding*, y la exposición de un par o una cesta a ellos.
**Método.** (i) **Carteras por prima forward** (Lustig, Roussanov y Verdelhan, 2011): ordenación mensual de las divisas del universo frente al USD por `f − s` en 3–6 carteras; **DOL** = media de todas; **HML_FX** = alta menos baja. (ii) **Dollar carry** (Lustig, Roussanov y Verdelhan, 2014): largo en todas las divisas si el diferencial medio frente al USD es positivo, corto si es negativo. (iii) **Valor**: cambio de 5 años del tipo real (Asness, Moskowitz y Pedersen, 2013) o tipo real ajustado (Menkhoff et al., 2017), en carteras. (iv) **Momentum**: carteras por rentabilidad de formación (FX-MOM-001). (v) Opcional: factor de volatilidad global (innovación de la volatilidad media, Menkhoff et al., 2012a) y de desequilibrios globales (Della Corte, Riddiough y Sarno, 2016). (vi) Rentabilidad, volatilidad, Sharpe con EE, asimetría, MDD por factor; correlaciones entre factores. (vii) Exposición de un ámbito (par, cesta o índice de gestores de divisas, este último como análisis de estilo restringido de Sharpe para medir el *crowding*; Pojarliev y Levich, 2011): regresión de su rentabilidad total sobre DOL, HML_FX, valor y momentum con HAC. (viii) *Crowding*: percentiles CFTC agregados de las patas (FX-POS-001), correlación media rodante entre las patas del carry, dispersión de tipos entre carteras.
**Entradas mínimas.** Contado y forwards mensuales del universo ≥ 10 años (≥ 20 recomendados), del mismo corte; universo con altas y bajas fechadas.
**Parámetros.** universo (G10 frente a USD; ampliado); n_carteras (6; 3 en G10); rebalanceo (mensual); ponderacion (equiponderada; inversa de volatilidad); divisa_valoracion (USD; EUR si F10).
**Salidas.** SERIE: rentabilidades de los factores; TABLA: estadísticos, correlaciones, betas del ámbito con IC, indicadores de *crowding*. ESTADISTICA.
**Supuestos y limitaciones.** Universo y exclusiones determinan el resultado (sesgo de supervivencia; FX-BT-001); costes no incluidos salvo petición; primas dependientes del régimen; la exposición a factores no es una previsión.
**Tolerancias y semilla.** 1e-8 · null.
**Verificación.** DOL = media de las carteras; HML_FX = cartera alta − baja; réplica de estadísticos publicados en la ventana original dentro de tolerancia declarada; segunda vía: 3 frente a 6 carteras.
**Referencia ingenua.** RI-SEG (ESTR: rentabilidad nula o índice de estrategia publicado); RI-FWD (exceso nulo).
**Aclaración y rechazo.** Rechazo sin universo fechado o con < 10 años.
**Referencias.** Lustig, Roussanov y Verdelhan (2011), «Common Risk Factors in Currency Markets», *RFS*; Lustig, Roussanov y Verdelhan (2014), «Countercyclical Currency Risk Premia», *JFE*; Menkhoff, Sarno, Schmeling y Schrimpf (2012a; 2017), *Journal of Finance*, *RFS*; Verdelhan (2018), *Journal of Finance*; Della Corte, Riddiough y Sarno (2016), *RFS*; Kroencke, Schindler y Schrimpf (2014), *Review of Finance* · TMX-06.
**Prioridad y madurez.** P1 · DOCUMENTADO (alternativa: ST-DESC-001 sobre índices de estrategia publicados).

### 8.4 Opciones y volatilidad implícita (MC-09)

### FX-GK-001 · Garman-Kohlhagen, griegas y conversión delta–precio de ejercicio

**Identificación.** v1.0 · VIGENTE · MC-09 · Mapa: áreas 30, 6.
**Perfiles y horizontes.** TRANSVERSAL · H1–H3.
**Propósito.** Precio, griegas y volatilidad implícita de opciones genéricas de un par (ATM, deltas estándar, plazos estándar) y conversión entre deltas, precios de ejercicio y convenciones, como lectura del mercado del ámbito.
**Método.** (i) Garman-Kohlhagen con `r_c` y `r_b` continuos derivados de FX-FWD-001: `d_1 = [ln(F/K) + σ²T/2]/(σ√T)`, `C = e^{−r_c·T}[F·Φ(d_1) − K·Φ(d_2)]`, `P = e^{−r_c·T}[K·Φ(−d_2) − F·Φ(−d_1)]`. (ii) Griegas: delta de contado y forward, con y sin ajuste por prima; gamma; vega; theta; rho de cada divisa. (iii) Volatilidad implícita por Newton con respaldo de Brent tras comprobar cotas de no arbitraje. (iv) Del delta al precio de ejercicio: forma cerrada sin ajuste (`K = F·exp(∓Φ^{−1}(|Δ_F|)·σ√T + σ²T/2)`, signo − para calls) y numérica con ajuste por prima (raíz del lado de la delta máxima). (v) ATM DNS (`K = F·e^{±σ²T/2}` según ajuste), ATM forward y ATM de contado. (vi) Tiempo: días naturales/365 hasta el vencimiento; descuento hasta la fecha de entrega (FX-SETL-001).
**Entradas mínimas.** S, F (o tipos), T, σ o precio, tipo de opción, convención de delta y de ATM del par (declarada por la fuente).
**Parámetros.** convencion_delta (contado; forward; con_prima); convencion_atm (DNS); tol_iv (1e-8).
**Salidas.** TABLA: precio (pips de cotizada y % de nominal de base), griegas, volatilidad implícita (% anual), precios de ejercicio por delta. DETERMINISTA.
**Supuestos y limitaciones.** Lognormalidad y σ constante contradichas por la sonrisa (FX-RR-001); americanas y exóticas fuera de ficha; la convención errónea de delta desplaza el precio de ejercicio de 25 delta de forma material.
**Tolerancias y semilla.** 1e-8 · null.
**Verificación.** Paridad `C − P = e^{−r_c·T}(F − K)`; caso de control S = F = K = 1, T = 1, σ = 10 %, r_c = r_b = 0 ⇒ C = P = 0,039878; delta forward ATM DNS sin ajuste = 0,5; segunda vía: integración numérica de la densidad lognormal.
**Referencia ingenua.** RI-EWMA (realizada como estimador de la implícita).
**Aclaración y rechazo.** Aclaración sin convención de delta o de ATM; rechazo si el precio viola cotas de no arbitraje o el pago no está en ficha.
**Referencias.** Garman y Kohlhagen (1983), «Foreign Currency Option Values», *JIMF*; Reiswich y Wystup (2010), «A Guide to FX Options Quoting Conventions», *Journal of Derivatives*; Clark (2011), *Foreign Exchange Option Pricing*; Wystup (2017), *FX Options and Structured Products*; Hull (2022) · TMX-05.
**Prioridad y madurez.** P1 · DOCUMENTADO.

### FX-RR-001 · *Risk reversals*, *butterflies* y sonrisa

**Identificación.** v1.0 · VIGENTE · MC-09 · Mapa: áreas 31, 30.
**Perfiles y horizontes.** TRANSVERSAL · H1–H3.
**Propósito.** Leer el sesgo y la curvatura de la sonrisa de un par (dato del informe PFV de AG-21: `rr_25d`, `percentil`), reconstruir la sonrisa a partir de ATM, RR y BF y situarlos frente a su historia.
**Método.** (i) Convención cambiaria referida a la base: `RR_25 = σ_{25C} − σ_{25P}`; *butterfly* de sonrisa `BF_25 = (σ_{25C} + σ_{25P})/2 − σ_ATM`; idem a 10 delta. (ii) Volatilidades de las alas: `σ_{25C} ≈ σ_ATM + BF + RR/2`, `σ_{25P} ≈ σ_ATM + BF − RR/2`; con *butterfly* de *strangle* de mercado, ajuste iterativo para que la sonrisa revalore el *strangle* de mercado con sus propios precios de ejercicio (Clark, 2011). (iii) Interpolación: Malz (1997) `σ(δ) = σ_ATM − 2·RR·(δ − 0,5) + 16·BF·(δ − 0,5)²` y Vanna-Volga (Castagna y Mercurio, 2007) como segunda vía; SABR (β = 1) si se piden más puntos. (iv) RR normalizado por la ATM (`RR/σ_ATM`), percentil frente a 3 años y cambio semanal. (v) Comprobación de no arbitraje de mariposa en la sonrisa resultante.
**Entradas mínimas.** σ_ATM, RR y BF a 25 delta (y 10 delta si se piden alas) por plazo, con convención de delta, ATM y tipo de *butterfly* declarados; ≥ 2 años para percentiles.
**Parámetros.** plazos (1M, 3M); tipo_bf (mercado; sonrisa); interpolacion (Malz; Vanna-Volga); ventana (3 años).
**Salidas.** TABLA: volatilidades por delta, RR y BF (puntos de volatilidad), RR normalizado, percentiles, cambio; SERIE: sonrisa por precio de ejercicio. DETERMINISTA (reconstrucción) y ESTADISTICA (percentiles e interpolación).
**Supuestos y limitaciones.** El signo del RR se refiere a la base del par (en USD/JPY, RR negativo = demanda de calls de yen); la sonrisa es neutral al riesgo; las alas fuera de 10–90 delta se extrapolan con advertencia.
**Tolerancias y semilla.** 1e-8 (reconstrucción); 1e-6 (ajuste iterativo) · null.
**Verificación.** La sonrisa reproduce σ_ATM, σ_25C y σ_25P; RR = 0 y BF = 0 ⇒ sonrisa plana; Malz frente a Vanna-Volga dentro de la banda declarada en 10–90 delta.
**Referencia ingenua.** RI-PA del RR (sin cambio) si se usa como señal.
**Aclaración y rechazo.** Aclaración si no consta el tipo de *butterfly* o la convención de delta; rechazo con sonrisa con densidad negativa no reparable.
**Referencias.** Malz (1997), «Estimating the Probability Distribution of the Future Exchange Rate from Option Prices», *Journal of Derivatives*; Castagna y Mercurio (2007), «The Vanna-Volga Method for Implied Volatilities», *Risk*; Reiswich y Wystup (2010); Clark (2011); Hagan, Kumar, Lesniewski y Woodward (2002), *Wilmott* · TMX-05.
**Prioridad y madurez.** P1 · DOCUMENTADO (alternativa: ST-DESC-001 sobre el RR publicado).

### FX-TERM-001 · Estructura de plazos, volatilidad forward y volatilidad de evento

**Identificación.** v1.0 · VIGENTE · MC-09 · Mapa: área 31.
**Perfiles y horizontes.** TRANSVERSAL · H1–H3.
**Propósito.** Describir la estructura de plazos de la volatilidad implícita ATM de un par, la volatilidad forward entre plazos y la volatilidad (y el movimiento) que el mercado asigna a un evento con fecha.
**Método.** (i) Curva ATM por plazos (1S, 2S, 1M, 2M, 3M, 6M, 1A); pendiente (3M − 1M) y su percentil. (ii) Volatilidad forward `σ_{1,2} = √[(σ_2²T_2 − σ_1²T_1)/(T_2 − T_1)]` con varianza total no decreciente. (iii) Volatilidad de evento: con un vencimiento que incluye la fecha del evento y otro que no (o con la volatilidad base de días sin evento), varianza del día del evento `σ²_evento = (σ²_con·T_con − σ²_base·(T_con − 1/365))·365`, con ponderación de fines de semana y festivos declarada; movimiento descontado del día `≈ σ_evento·√(1/365)` en % y en pips.
**Entradas mínimas.** Volatilidades ATM por plazo con fechas de vencimiento; calendario del evento.
**Parámetros.** plazos (1S–1A); peso_fin_de_semana (0,3 declarado); evento (fecha y hora).
**Salidas.** TABLA: curva, pendiente y percentil, volatilidades forward, volatilidad de evento (% anual) y movimiento descontado (% y pips). DETERMINISTA dadas las entradas.
**Supuestos y limitaciones.** La extracción de la volatilidad de evento depende del peso de los días sin evento; varianza total decreciente ⇒ arbitraje de calendario (dato sospechoso).
**Tolerancias y semilla.** 1e-10 · null.
**Verificación.** Curva plana ⇒ volatilidades forward iguales; varianza total no decreciente.
**Referencia ingenua.** RI-EWMA para la volatilidad; RI-PA del par para el movimiento.
**Aclaración y rechazo.** Rechazo con varianza total decreciente sin explicación o sin fechas de vencimiento.
**Referencias.** Clark (2011), cap. 3–4; Gatheral (2006), *The Volatility Surface*; Wystup (2017) · TMX-05.
**Prioridad y madurez.** P1 · DOCUMENTADO.

### FX-VRP-001 · Prima de volatilidad cambiaria

**Identificación.** v1.0 · VIGENTE · MC-09 (invitado MC-02) · Mapa: áreas 33, 10.
**Perfiles y horizontes.** TRANSVERSAL · H1–H3.
**Propósito.** Medir la diferencia entre la varianza implícita y la realizada de un par o de una cesta, *ex ante* (frente a la prevista) y *ex post* (frente a la realizada posterior, solo en evaluación).
**Método.** (i) Varianza implícita a 1 mes (ATM o réplica de varianza con la sonrisa de FX-RR-001). (ii) Varianza realizada prevista (HAR-RV o GARCH de VOL-GARCH-001) y, en evaluación, realizada posterior de 21–22 sesiones. (iii) `VRP = σ²_impl − E[RV]` (convención del bloque: positiva = implícita por encima); en puntos de volatilidad y en varianza. (iv) Percentil frente a 3 años; sección cruzada por divisa (Della Corte, Ramadorai y Sarno, 2016, usan la convención inversa: se declara).
**Entradas mínimas.** Implícita y realizada del mismo corte; ≥ 2 años.
**Parámetros.** plazo (1M); prevision_rv (HAR); ventana (3 años).
**Salidas.** TABLA: VRP (puntos y varianza), percentil, sección cruzada. ESTADISTICA.
**Supuestos y limitaciones.** La realizada posterior solo existe en evaluación (fuga si se usa como señal en tiempo real); la VRP alta precede a menudo episodios de estrés.
**Tolerancias y semilla.** 1e-8 · null.
**Verificación.** Implícita = prevista ⇒ VRP nula; segunda vía: ATM frente a réplica de varianza.
**Referencia ingenua.** RI-EWMA.
**Aclaración y rechazo.** Rechazo si la realizada posterior se pide como señal (FUGA_INFORMACION).
**Referencias.** Della Corte, Ramadorai y Sarno (2016), «Volatility Risk Premia and Exchange Rate Predictability», *JFE*; Carr y Wu (2009), *RFS*; Corsi (2009) · TMX-05, TMX-02.
**Prioridad y madurez.** P2 · DOCUMENTADO (alternativa: FX-VOL-001, brecha implícita–realizada).

### FX-RND-001 · Densidad implícita neutral al riesgo y probabilidades de umbral

**Identificación.** v1.0 · VIGENTE · MC-09 · Mapa: áreas 32, 31.
**Perfiles y horizontes.** TRANSVERSAL · H1–H3.
**Propósito.** Distribución neutral al riesgo del par al vencimiento implícita en la sonrisa, sus momentos y las probabilidades neutrales al riesgo de umbrales pedidos.
**Método.** (i) Sonrisa interpolada de FX-RR-001 convertida a precios por FX-GK-001 en una rejilla densa de precios de ejercicio. (ii) Breeden-Litzenberger `q(K) = e^{r_c·T}·∂²C/∂K²` por diferencias finitas o derivación analítica de la interpolación. (iii) Comprobaciones: no negatividad, integral = 1, media = forward. (iv) Cuantiles, asimetría y curtosis implícitas; `P^Q(S_T > K)` y `P^Q(S_T < K)` para los umbrales pedidos. (v) Comparación con la lognormal de σ_ATM (contribución de la sonrisa).
**Entradas mínimas.** ATM, RR y BF a 25 y 10 delta del plazo; forward; convenciones declaradas.
**Parámetros.** interpolacion (Vanna-Volga; Malz); rejilla (500 puntos); extrapolacion_alas (lognormal con σ de 10 delta).
**Salidas.** DISTRIBUCION: densidad y cuantiles 5/25/50/75/95 (nivel del par); TABLA: momentos y probabilidades de umbral. ESTADISTICA (depende de la interpolación).
**Supuestos y limitaciones.** **Probabilidades neutrales al riesgo, no reales**: incluyen primas por riesgo, mayores en colas de refugio y de carry; nunca se entregan como pronóstico del bloque; colas sensibles a la extrapolación.
**Tolerancias y semilla.** 1e-6 · null.
**Verificación.** Media de la densidad = forward dentro de 1e-6 relativo; integral = 1; sonrisa plana ⇒ lognormal; segunda vía: interpolación alternativa.
**Referencia ingenua.** RI-PA probabilística (lognormal sin deriva con volatilidad realizada conocida en t).
**Aclaración y rechazo.** Rechazo si la densidad es negativa tras la reparación declarada o faltan las alas.
**Referencias.** Breeden y Litzenberger (1978), *Journal of Business*; Malz (1997); Bliss y Panigirtzoglou (2002), *Journal of Banking & Finance*; Jackwerth (2004), *Option-Implied Risk-Neutral Distributions and Risk Aversion* · TMX-05.
**Prioridad y madurez.** P2 · DOCUMENTADO.

### 8.5 Riesgo de cola y regímenes (MC-07, MC-05)

### FX-TAIL-001 · Riesgo de cola del carry y coste de cobertura

**Identificación.** v1.0 · VIGENTE · MC-07 · Mapa: áreas 26, 25.
**Perfiles y horizontes.** TRANSVERSAL (especialmente PERF-FX-FACT y PERF-FX-EM) · H2–H4.
**Propósito.** Medir el riesgo de colapso de una exposición de carry (par, cesta o estrategia) y el carry neto de una cobertura genérica de cola, como lectura de riesgo del ámbito.
**Método.** (i) Sobre la rentabilidad total (FX-TR-001): asimetría y curtosis con IC por bootstrap por bloques, ES 97,5 % y 99 %, EVT-POT de la cola izquierda, MDD y duración. (ii) Sensibilidad a la volatilidad global y a la renta variable (betas en días de estrés, dependencia de cola inferior de FX-CORR-001). (iii) Pérdidas en episodios de control (otoño de 2008, mayo de 2010, agosto de 2015, marzo de 2020, agosto de 2024) si están en la muestra. (iv) **Carry neto de cobertura**: carry anual − coste anualizado de una put genérica de 10 o 25 delta a 1 o 3 meses sobre la divisa de rendimiento (FX-GK-001 con la sonrisa de FX-RR-001), renovada (Jurek, 2014); cociente coste/carry. (v) Indicadores de fragilidad: carry ajustado (FX-CARRY-001), percentil de posicionamiento (FX-POS-001), RR (FX-RR-001).
**Entradas mínimas.** ≥ 5 años de rentabilidad total diaria o semanal; sonrisa para el paso (iv).
**Parámetros.** niveles_es (0,975; 0,99); delta_cobertura (0,10; 0,25); plazo_cobertura (1M); umbral_evt (cuantil 0,95).
**Salidas.** TABLA: asimetría, curtosis, ES, parámetros GPD, MDD, betas de estrés, pérdidas en episodios, carry neto de cobertura y cociente. ESTADISTICA.
**Supuestos y limitaciones.** Los colapsos son raros: estimaciones de cola con pocas observaciones (IC amplios, *peso problem*); la cobertura genérica es una lectura de precio del riesgo, no una propuesta de instrumento (Bloque B).
**Tolerancias y semilla.** 1e-6 · entero del plan para el bootstrap.
**Verificación.** ES ≥ VaR; serie simétrica simulada ⇒ asimetría ≈ 0; segunda vía: ES histórico frente a EVT.
**Referencia ingenua.** RI-CLI (distribución incondicional) y la normal con la misma volatilidad.
**Aclaración y rechazo.** Rechazo con < 5 años o sin dirección.
**Referencias.** Brunnermeier, Nagel y Pedersen (2008), «Carry Trades and Currency Crashes», *NBER Macroeconomics Annual*; Jurek (2014), «Crash-Neutral Currency Carry Trades», *JFE*; Farhi y Gabaix (2016), «Rare Disasters and Exchange Rates», *QJE*; Burnside, Eichenbaum, Kleshchelski y Rebelo (2011), «Do Peso Problems Explain the Returns to the Carry Trade?», *RFS*; Chernov, Graveline y Zviadadze (2018), *JFE*; Daniel, Hodrick y Lu (2017), *Critical Finance Review* · TMX-07.
**Prioridad y madurez.** P1 · DOCUMENTADO (alternativa: RISK-VAR-001 + RISK-DD-001 sobre la rentabilidad total).

### FX-PEG-001 · Riesgo de ruptura de tipos fijos y bandas

**Identificación.** v1.0 · VIGENTE · MC-05 (invitado MC-09) · Mapa: áreas 20, 34, 16.
**Perfiles y horizontes.** PERF-FX-EM (HKD, divisas del Golfo, regímenes gestionados de EMLA y EMEA) y PERF-FX-G10 en episodios con suelo o techo declarados · H2–H4.
**Propósito.** Cuantificar el riesgo de ruptura o realineamiento de un tipo fijo, una banda o un régimen gestionado (tipo de opción `REGIMEN`) con indicadores de mercado y de reservas.
**Método.** (i) **Probabilidad neutral al riesgo de ruptura** por modelo de salto: `p = (F − S_fijo)/(E^Q[S | ruptura] − S_fijo)` con tamaños de salto por escenarios (p. ej., 10 %, 20 %, 40 %) y forward o NDF del plazo; intensidad anual equivalente. (ii) Lectura de opciones si existen (RR y alas, FX-RR-001). (iii) Posición dentro de la banda y ajuste por deriva de Svensson (1993) para bandas: expectativa de realineamiento = prima forward − depreciación esperada dentro de la banda. (iv) Cocientes de reservas: métrica ARA del FMI (flotación `5 % X + 5 % M2 + 30 % deuda a corto + 15 % otros pasivos`; tipo fijo `10 % + 10 % + 30 % + 20 %`), Guidotti-Greenspan, meses de importaciones, variación de reservas netas. (v) Simulación «se mantiene / se rompe» con salto (SIM-MC-001) para SCN-H-001.
**Entradas mínimas.** Paridad o banda; contado, forwards o NDF por plazos; reservas y sus componentes con fecha; tamaños de salto por escenarios.
**Parámetros.** tamanos_salto (0,10/0,20/0,40); plazos (3M, 12M); metrica_reservas (ARA_fijo).
**Salidas.** TABLA: probabilidades neutrales al riesgo por escenario de salto y plazo, intensidad, posición en la banda, cocientes de reservas; DISTRIBUCION opcional. ESTADISTICA.
**Supuestos y limitaciones.** Probabilidad neutral al riesgo y muy sensible al tamaño del salto y a la prima de riesgo; mercados de forward con controles pueden no reflejar expectativas; el juicio de sostenibilidad es del Analista.
**Tolerancias y semilla.** 1e-10 (aritmética) · obligatoria en la simulación.
**Verificación.** F = S_fijo ⇒ p = 0; casos de control: suelo EUR/CHF hasta el 15/01/2015; banda USD/HKD 7,75–7,85.
**Referencia ingenua.** RI-FWD (el forward como predictor) y RI-TB (frecuencia histórica de rupturas en regímenes comparables).
**Aclaración y rechazo.** Rechazo sin paridad o banda declaradas o sin escenarios de salto.
**Referencias.** Krugman (1991), «Target Zones and Exchange Rate Dynamics», *QJE*; Svensson (1993), *European Economic Review*; Bertola y Svensson (1993), *REStud*; Ilzetzki, Reinhart y Rogoff (2019), *QJE*; FMI (2015), *Assessing Reserve Adequacy – Specific Proposals*; Kaminsky, Lizondo y Reinhart (1998), *IMF Staff Papers* · TMX-07.
**Prioridad y madurez.** P2 · DOCUMENTADO.

### 8.6 Prospectiva cuantitativa (MC-04)

### FX-PASS-001 · Escenarios de política monetaria y traslación al tipo de cambio

**Identificación.** v1.0 · VIGENTE · MC-04 · Mapa: áreas 18, 15.
**Perfiles y horizontes.** PERF-FX-G10, PERF-FX-EM · H2–H4 (H4 limitado en emergentes).
**Propósito.** Traducir escenarios de política monetaria de dos bancos centrales (sendas de tipos frente a lo descontado) en rangos del par por horizonte, con su sensibilidad y sus umbrales de invalidación.
**Método.** (i) Escenarios de senda (base, halcón, paloma) de cada banco central frente a la senda descontada de MON-EXP-001; sorpresa acumulada de diferencial a 2 años (pb). (ii) Traslación con la sensibilidad estimada en FX-RDIFF-001 (pips o % por 10 pb) y su IC; en H3–H4, más el carry acumulado y, si se pide, la reversión parcial a FX-PPP-001 o FX-BEER-001. (iii) Probabilidades de escenario aportadas por Prospectiva (nunca asignadas por el Motor). (iv) Tornado de supuestos (sensibilidad, sorpresa, carry) y umbrales de invalidación: movimiento del diferencial que anula la tesis (p. ej., «el diferencial a 2 años se amplía más de 50 pb»). (v) Tasas base de episodios comparables (ciclos de subidas y bajadas divergentes) si se aportan.
**Entradas mínimas.** Sendas descontadas, escenarios con su fuente, sensibilidad estimada con IC.
**Parámetros.** escenarios (base, halcon, paloma); horizonte; incluir_carry (true).
**Salidas.** TABLA: rango del par por escenario y horizonte, contribución de cada bloque, tornado, umbrales de invalidación. ESTADISTICA.
**Supuestos y limitaciones.** La sensibilidad es inestable y depende del régimen de riesgo; los escenarios son condicionales, no pronósticos; la incertidumbre profunda se expresa sin probabilidades.
**Tolerancias y semilla.** 1e-8 · null (o del plan si se simula).
**Verificación.** Escenario igual a lo descontado y sin carry ⇒ par sin cambio; monotonía en la sorpresa.
**Referencia ingenua.** RI-PA y RI-FWD por horizonte.
**Aclaración y rechazo.** Rechazo sin senda descontada o sin sensibilidad estimada.
**Referencias.** Engel (2016), *AER*; Gürkaynak, Sack y Swanson (2005); Saltelli et al. (2008), *Global Sensitivity Analysis: The Primer*; Clarida, Galí y Gertler (2002), *JME* · TMX-04, TMX-01.
**Prioridad y madurez.** P1 · DOCUMENTADO.

### 8.7 Evaluación predictiva y backtesting (MC-10)

### FX-RW-001 · Evaluación frente al paseo aleatorio y el forward

**Identificación.** v1.0 · VIGENTE · MC-10 · Mapa: áreas 38, 36, 41.
**Perfiles y horizontes.** TRANSVERSAL · H1–H4.
**Propósito.** ¿Bate un pronóstico, un modelo o un Analista al paseo aleatorio y al forward como predictor, con significación y de forma estable en el tiempo? (R13, 8.3 y Anexo A del Documento 0.)
**Método.** (i) Construcción de las referencias con la misma fecha de corte: RI-PA puntual (último valor), RI-PA probabilística (lognormal sin deriva con volatilidad EWMA conocida en t), RI-FWD puntual y probabilística (centrada en el forward), exceso nulo en rentabilidad total. (ii) Puntuales: RMSE, MAE, MASE y **U de Theil** frente a RI-PA y RI-FWD. (iii) Probabilísticas: Brier, log-score, CRPS y **BSS frente a RI-PA** con IC 90 % por bootstrap estacionario. (iv) Pruebas: **Clark-West** frente a RI-PA (modelo anidado; t unilateral HAC, críticos 1,282 y 1,645), Diebold-Mariano con HLN frente a RI-FWD y otros no anidados, Pesaran-Timmermann en dirección, **prueba de fluctuación** de Giacomini y Rossi (2010) con ventana declarada, Giacomini-White si se pide. (v) Corrección de Holm entre celdas segmento × horizonte × método. (vi) Resumen para el Evaluador: ¿cumple la condición (2) del certificado (extremo inferior del IC 90 % del BSS frente a RI-PA > 0)? ¿hay degradación significativa (12.2)?
**Entradas mínimas.** Pronósticos congelados (PRG-FX-) o de modelo con fecha y horizonte; realizaciones del indicador de seguimiento con la misma fuente y corte; contado y forward en cada fecha de pronóstico; ≥ 30 resoluciones (≥ 100 para el certificado).
**Parámetros.** perdida (cuadratica; brier); bloque (max(h, T^{1/3})); B (2 000); ventana_fluctuacion (0,3·T); nivel_ic (0,90).
**Salidas.** TABLA: métricas y habilidad frente a cada referencia, estadísticos y p-valores (CW, DM*, PT), BSS con IC, serie de la prueba de fluctuación, n nominal y efectivo, marcas de condición (2) y degradación. ESTADISTICA.
**Supuestos y limitaciones.** La ventaja esperable en divisas es pequeña: con n = 100, solo ventajas grandes son detectables; la significación frente a RI-PA no implica rentabilidad tras costes; habilidad inestable en el tiempo.
**Tolerancias y semilla.** 1e-8 en métricas; 1e-6 en IC con la misma semilla · entero del plan.
**Verificación.** Un pronóstico idéntico a RI-PA ⇒ U = 1, BSS = 0, CW ≈ 0; pronosticador sintético con ventaja conocida recuperado; segunda vía: otra longitud de bloque.
**Referencia ingenua.** RI-PA y RI-FWD (obligatorias por definición).
**Aclaración y rechazo.** Rechazo con fuga (realizaciones o forwards posteriores a la fecha de corte), con fuente o corte distintos entre pronóstico y realización, o sin criterio de resolución.
**Referencias.** Meese y Rogoff (1983), *JIE*; Clark y West (2007), *Journal of Econometrics*; Diebold y Mariano (1995), *JBES*; Harvey, Leybourne y Newbold (1997), *IJF*; Giacomini y Rossi (2010), «Forecast Comparisons in Unstable Environments», *JAE*; Rossi (2013), *JEL*; Cheung, Chinn, Pascual y Zhang (2019), *JIMF*; Bröcker y Smith (2007), *Weather and Forecasting* · TMX-08.
**Prioridad y madurez.** P0 · IMPLEMENTADO (ejecutor `bloque_a_forex` V1.0, versión sencilla): RI-PA (0,5 en sube/baja; lognormal sin deriva para umbrales) y RI-FWD probabilísticas con la volatilidad EWMA conocida en t, Brier, BSS frente a ambas y acierto con prueba binomial; U de Theil, Clark-West, DM-HLN, fluctuación y bootstrap, DOCUMENTADO (alternativa: FC-EVAL-001 y FC-CAL-001).

### FX-BT-001 · Backtesting de estrategias cambiarias sin sesgos

**Identificación.** v1.0 · VIGENTE · MC-10 · Mapa: áreas 39, 44.
**Perfiles y horizontes.** PERF-FX-FACT (y PERF-FX-G10, PERF-FX-EM para reglas sobre un par o una cesta) · H2–H4.
**Propósito.** Evaluar retrospectivamente una regla cambiaria (carry, valor, momentum, dólar, cesta de refugio, regla de un Analista) sin sesgos de anticipación, supervivencia, selección ni costes omitidos.
**Método.** (i) Datos *point-in-time*: contado y forwards del mismo corte (WM/Reuters o NY 17:00), CFTC desde el viernes, macro con vintage, fijaciones tras su hora. (ii) Señal en t, ejecución en el cierre siguiente o con desfase declarado; rentabilidad total por FX-TR-001. (iii) Universo fechado (altas y bajas: divisas legadas del euro, paso a tipo fijo, controles); exclusión documentada de periodos con desviaciones grandes de la CIP. (iv) Costes de mercado del ámbito: horquilla de contado y de puntos forward (cotizada como cota superior y fracción efectiva declarada), renovaciones; sin costes de instrumentos ni de proveedores. (v) Métricas por subperiodo y régimen (antes y después de 2008, tipos cero, 2022–2024) y en episodios de colapso. (vi) Sobreajuste: BT-DSR-001 (con N ensayos), BT-PBO-001, Reality Check o SPA si hay muchas variantes. (vii) Comparación con RI-SEG y RI-FWD.
**Entradas mínimas.** ≥ 10 años mensuales (≥ 5 con advertencia); reglas fijadas antes de ver los resultados de prueba; número de configuraciones probadas.
**Parámetros.** desfase_ejecucion (1 sesión); costes (horquilla_cotizada × 0,5 por defecto, declarado); rebalanceo (mensual); subperiodos (declarados).
**Salidas.** TABLA: rentabilidad, volatilidad, Sharpe con EE, asimetría, MDD, rotación, coste, métricas por subperiodo y régimen, DSR, PBO, diferencia frente a referencias con IC. ESTADISTICA.
**Supuestos y limitaciones.** Un backtest no es evidencia fuera de muestra (solo F4 lo es); la caída tras la publicación de anomalías es habitual (McLean y Pontiff, 2016); costes efectivos inciertos.
**Tolerancias y semilla.** 1e-8 · entero del plan si hay remuestreo.
**Verificación.** Regla aleatoria ⇒ Sharpe ≈ 0 y PBO ≈ 0,5; reconstrucción de la rentabilidad desde las posiciones; segunda vía: desfase de ejecución alternativo.
**Referencia ingenua.** RI-SEG, RI-FWD (exceso nulo) y selección aleatoria de la configuración.
**Aclaración y rechazo.** Rechazo sin universo fechado, sin número de ensayos o con datos no conocibles en la fecha de la señal.
**Referencias.** Lustig, Roussanov y Verdelhan (2011); Menkhoff, Sarno, Schmeling y Schrimpf (2012a, 2012b); Bailey y López de Prado (2014); Bailey, Borwein, López de Prado y Zhu (2017); White (2000), *Econometrica*; Hansen (2005), *JBES*; McLean y Pontiff (2016), *Journal of Finance*; Harvey, Liu y Zhu (2016), *RFS* · TMX-08, TMX-06.
**Prioridad y madurez.** P1 · DOCUMENTADO.

## 9. Pruebas de regresión y casos de control

1. Cada ficha declara sus casos de control (sección «Verificación»). Tras cada cambio de versión de método o de ficha, el módulo responsable los ejecuta y MC-08 verifica una muestra en la verificación periódica; un fallo devuelve la ficha a `EN_REVISION` y se notifica al operador.
2. **Paso a IMPLEMENTADO**: casos de control superados en el entorno de ejecución (`11_Ejecutor`, paquete `bloque_a_forex`) y registrados en el Registro de cálculos. **Paso a VALIDADO**: pruebas de `09_Pruebas` ejecutadas con evidencia, incluidas pruebas con datos reales de cada segmento, datos insuficientes, ámbitos que cruzan segmentos y regímenes gestionados.
3. **Casos de control cambiarios comunes** (todas las fichas que encadenan cálculos de contado y forward): triangulación de cruces dentro de la horquilla; inversión doble = identidad; CIP reconstruida desde tipos y puntos con base declarada; contado + carry + cruzado = total; fechas valor de USD/CAD (T+1) y de un par con festivo en una plaza; paridad put-call y caso ATM de Garman-Kohlhagen; densidad implícita con media = forward.
4. **SCORE-RK-001** se prueba contra HT-03 con el conjunto común de casos de `10_Herramientas`; cualquier diferencia bloquea ambas hasta su resolución.
5. **FC-EVAL-001, FC-CAL-001 y FX-RW-001** se prueban con pronosticadores sintéticos de propiedades conocidas (idéntico al paseo aleatorio, perfectamente calibrado, sobreconfiado, sin resolución, con ventaja pequeña) para comprobar que métricas, pruebas (Clark-West, DM, fluctuación) y nulos se comportan como se espera antes de usarse en certificados (R13).
6. **Frontera con el Bloque B** (1.6): la batería incluye, para cada familia de fichas cambiarias, una petición que pretende comparar instrumentos (contado frente a forward, opción frente a ETF), proveedores, costes de ejecución o niveles de entrada y que debe rechazarse con `FUERA_DE_CATALOGO` y la ficha de ámbito más próxima.
7. **SCORE-RK-001 v2.0** se reverifica contra HT-03 con los pesos de A del bloque Forex (asimetría 30, valoración y desviación del equilibrio 20, carry 15, catalizadores 15, momento y posicionamiento 10, convertibilidad y profundidad 10) y el tope por saturación sobre «valoración y desviación del equilibrio», antes de servir cifras citables con esos pesos.
8. **RISK-DD-001 v2.0** se reverifica en `bloque_a_forex` con los umbrales cambiarios (5/9/14/20 %), el ajuste por asimetría, el umbral de MDD del 25 % y el suelo de régimen (nota 2 del Anexo A), con los casos de control de la ficha.
9. **Convención** (M17): la batería incluye un par invertido, una cesta sin pesos, una rentabilidad sin medida declarada y series de cortes distintos, que deben devolver `ACLARACION_REQUERIDA` o `DATOS_INCOHERENTES`.

## 10. Correspondencia con el Catálogo V5.0 del Bloque A general

| Fichas del Catálogo V5.0 | Tratamiento en este catálogo | Sustituta o alternativa |
|---|---|---|
| FX-TREND-001, FX-BRK-001, FX-STL-001, FX-REGIME-001, FX-COINT-001, FX-CORR-001, ST-DESC-001, ST-INF-001, FIN-CAGR-001, BIB-MET-001, SIM-MC-001, RISK-VAR-001, ML-CAL-001, AUD-REX-001, FC-CAL-001, BT-DSR-001, BT-PBO-001, BT-VAR-001, VOL-GARCH-001, ML-PRED-001, DEC-VOI-001 | Conservadas (sección 6) | — |
| FX-VOL-001, SCORE-RK-001, FC-EVAL-001, SCN-H-001, REG-HMM-001, ML-CLUS-001, RISK-DD-001, MON-EXP-001 | Nueva versión adaptada a divisas (sección 7) | — |
| FX-CARRY-001, FX-BEER-001, FX-MOM-001 | Nueva versión cambiaria (sección 8) | — |
| FX-PPA-001 | Deprecada | FX-PPP-001 |
| DER-OPT-001 | Retirada (no cambiaria) | FX-GK-001 |
| DER-SKEW-001 | Retirada | FX-RR-001 |
| DER-TERM-001 | Retirada | FX-TERM-001 |
| DER-VRP-001 | Retirada | FX-VRP-001 |
| DER-ROLL-001, MON-YLD-001 | Retiradas | FX-FWD-001, FX-SETL-001 |
| MON-REAL-001 | Retirada | FX-CARRY-001 v2.0 (carry real) |
| ACC-MOM-001 | Retirada | FX-MOM-001 v2.0 |
| ACC-FACT-001 | Retirada | FX-FACT-001, paso (vii): exposición de un ámbito (incluido un índice de gestores de divisas, como análisis de estilo para el *crowding*) a DOL, HML_FX, valor y momentum |
| TEM-DIFF-001 | Retirada (sin uso cambiario) | FX-PASS-001 como ficha de MC-04 |
| ACC-VAL-001, ACC-ERP-001, FIR-PRICE-001, FIR-CURVE-001, FIR-CARRY-001, FIR-SPREAD-001, FIR-CRED-001, CMD-CURVE-001, CMD-INV-001, CMD-RETDEC-001, CMD-REAL-001, REI-NAV-001, REI-CAP-001, REI-FFO-001, REI-LEV-001, CHR-ONCHAIN-001, CHR-FUND-001, CHR-FLOW-001, CHR-TOKEN-001, PRV-PME-001, PRV-CF-001, ALT-DESMOOTH-001, ALT-HF-001, ALT-AUC-001, IDX-ERP-001, IDX-CONC-001, IDX-REL-001, IDX-REB-001, FON-DISC-001, FON-FLOW-001, FON-TD-001, FON-LEV-001, MON-FIX-001, TCV-SLOPE-001, TCV-BEI-001, TCV-CDS-001, TCV-VIXTS-001, TCV-TP-001 | Retiradas: exclusivas de otros mercados ajenos al universo cambiario | Ninguna; una petición que las cite se rechaza con `FUERA_DE_CATALOGO` y la ficha cambiaria más próxima |

Las fichas retiradas siguen vigentes en el Catálogo V5.0 del Bloque A general, que no se modifica; su ausencia aquí no afecta a re-ejecuciones de ese bloque.
