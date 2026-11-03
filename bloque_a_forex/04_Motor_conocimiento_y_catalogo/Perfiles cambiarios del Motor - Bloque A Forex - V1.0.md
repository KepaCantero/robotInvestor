# Perfiles — Perfiles cambiarios del Motor de Cálculo Avanzado (Forex) (AG-13)

**Bloque A Forex · Robot Investor · Versión óptima V1.0 · 02/11/2026** · Subordinado al Documento 0 del Bloque A Forex V1.0.

Archivo CC (propietario: operador, tipo 3; el Motor propone). Lectores: AG-13 y sus módulos, AG-15, Analistas de segmento (AG-03 a AG-08), Analistas transversales (AG-09, AG-21), Prospectiva, Evaluador, Orquestador técnico. Sustituye, para este bloque, al documento «Perfiles de tipo de activo del Motor» del Bloque A general, que sigue vigente en ese bloque.

---

## 1. Propósito y reglas de uso

1.1. Un perfil PERF-FX-xx es la **especialización del Motor para un grupo de segmentos de divisas**: qué datos usa y con qué convenciones, qué cálculos hace por defecto en cada plan (PLAN_MIN, PLAN_STD, PLAN_EXT), qué métodos del Catálogo aplican en cada horizonte, qué referencias ingenuas y de comparación se usan, qué cautelas protegen contra los errores típicos del segmento y cuándo abstenerse. Sirve a la estrategia de cada Analista de segmento (sección 8 del Documento 0) sin sustituirla: el Analista decide qué preguntar; el perfil decide cómo se calcula bien.

1.2. **Reglas**:
1. El Orquestador de Cálculo clasifica cada petición CT-09 por su segmento y aplica el perfil correspondiente; si la petición trae el perfil, lo verifica; si no, lo infiere y lo declara.
2. Una ficha solo se aplica a los perfiles que declara (TRANSVERSAL = los tres). Aplicar un método fuera de su perfil exige justificación declarada en el plan (R21: aplicar a un segmento el marco de otro sin justificación es un hallazgo).
3. Ámbitos que cruzan segmentos: se combinan perfiles de forma declarada (sección 6) con sus riesgos cruzados; el segmento principal es el que fijan las reglas de asignación de 2.6 del Documento 0.
4. El perfil no añade operaciones al Catálogo ni amplía horizontes: respeta la tabla 8.3 del Documento 0 («Limitado» = solo con liquidez suficiente y catalizador identificado, declarados en la petición; «No» = el Motor rechaza la previsión con `HORIZONTE_NO_APLICABLE`).
5. Concluir «datos insuficientes» o «método no aplicable» es un resultado legítimo y registrable.
6. **Madurez** (R22): los tres perfiles están **documentados**. Las fichas que citan figuran con su madurez en el Catálogo de cálculos del bloque (V1.0); mientras una ficha esté solo documentada, el Motor sirve la alternativa implementada que la ficha declara, con la limitación declarada, o rechaza con motivo.
7. **Frontera con el Bloque B** (2.5 del Documento 0): ningún perfil se orienta a elegir o comparar instrumentos (contado, forward, futuro, opción, ETF/ETC, CFD), proveedores, costes de ejecución, apalancamiento, tamaño ni niveles de entrada. La unidad de cálculo es el **ámbito** (par, cruce, cesta, bloque, estrategia, régimen) y su **indicador de seguimiento**. Los contratos genéricos (forward a plazo constante, NDF a 1 mes, opción ATM o de 25 delta) solo se usan como lectura del mercado. Una petición cuyo propósito sea elegir o comparar instrumentos se rechaza con `FUERA_DE_CATALOGO`, indicando la ficha de ámbito más próxima.
8. **Convertibilidad e invertibilidad** (PS3): el Motor puede calcular métricas que la sostienen (existencia y liquidez de forward o NDF, brecha *onshore*–*offshore*, horquilla agregada, serie suficiente del indicador de seguimiento); la conclusión sobre PS3 es del Analista.
9. **Convención** (M17): par en notación BASE/COTIZADA, dirección referida a la base, medida contado o rentabilidad total, y en cestas composición, pesos y divisa de financiación.

1.3. **Correspondencia con la taxonomía del Documento 0 (2.6)**:

| N.º | Segmento | Analista | Perfil principal | Perfiles combinables habituales |
|---|---|---|---|---|
| 1 | G10N G10 núcleo (USD, EUR, JPY, GBP, CHF) | AG-03 | PERF-FX-G10 | PERF-FX-FACT (dólar amplio, refugio) |
| 2 | G10M G10 de materias primas y escandinavas (AUD, NZD, CAD, NOK, SEK) | AG-04 | PERF-FX-G10 | PERF-FX-FACT (carry G10) |
| 3 | EMAS Emergentes de Asia | AG-05 | PERF-FX-EM | PERF-FX-G10 (cruces con JPY o EUR), PERF-FX-FACT |
| 4 | EMLA Emergentes de Latinoamérica | AG-06 | PERF-FX-EM | PERF-FX-FACT (carry emergente) |
| 5 | EMEA Emergentes de Europa, Oriente Medio y África | AG-07 | PERF-FX-EM | PERF-FX-G10 (pares frente al EUR de las europeas centrales) |
| 6 | ESTR Estrategias y cestas cambiarias | AG-08 | PERF-FX-FACT | PERF-FX-G10 y PERF-FX-EM según el universo de la estrategia |
| — | Transversales: Bancos Centrales y Macro (BCM) y Posicionamiento, Flujos y Volatilidad (PFV) | AG-09, AG-21 | El del segmento de la divisa o el par; PERF-FX-FACT para magnitudes globales | Sección 5 |

1.4. **Formato de cada perfil**: estado y prioridad · ámbito · variables relevantes · régimen (indicadores que el Motor calcula) · indicadores de seguimiento típicos · **datos** (fuentes vía HT-01, convenciones, mínimos) · **cálculos por defecto por plan** · métodos por horizonte (8.3) · **referencias ingenuas** y de comparación (8.4) · **cautelas** del dominio · insuficiencia y abstención.

1.5. **Cálculos por defecto por plan.** Son el contenido que el Motor ejecuta cuando el solicitante pide un plan sin enumerar operaciones (p. ej., «cribado PLAN_MIN del segmento G10M»). Nunca se añaden cálculos no pedidos a una petición que sí los enumera (M10). PLAN_STD incluye siempre lo de PLAN_MIN para el ámbito investigado y PLAN_EXT lo de PLAN_STD.

---

## 2. PERF-FX-G10 — G10 núcleo y G10 de materias primas y escandinavas (G10N, G10M)

**Estado:** documentado · **Prioridad:** P1 · **Ámbito:** pares principales (EUR/USD, USD/JPY, GBP/USD, USD/CHF, AUD/USD, NZD/USD, USD/CAD) y cruces entre divisas del G10 (EUR/JPY, EUR/GBP, EUR/CHF, GBP/JPY, AUD/NZD, EUR/NOK, EUR/SEK, AUD/JPY, CAD/JPY…); cestas de dos o tres divisas del G10 con un factor común; opiniones de volatilidad (`VOLATILIDAD`) sobre un par del G10; regímenes con suelo o techo (EUR/CHF hasta 2015) como casos históricos.

**Variables relevantes.** Contado; puntos forward y tipos OIS de cada divisa; diferencial a 2 años nominal y real; senda descontada por reunión de cada banco central (Fed, BCE, BoJ, BoE, BNS, RBA, RBNZ, BoC, Norges Bank, Riksbank); inflación y brecha; sorpresas macro relativas; volatilidad implícita ATM, *risk reversals* y *butterflies* por plazo; posicionamiento CFTC; tipos efectivos del BPI; términos de intercambio (G10M); base cruzada (EUR, JPY, CHF frente a USD).

**Régimen.** REG-HMM-001 sobre dólar amplio, volatilidad cambiaria global, cesta de carry G10 y riesgo global (*dollar smile*: dólar fuerte en aversión al riesgo y en expansión diferencial de EE. UU.; débil en crecimiento global sincronizado); FX-REGIME-001 sobre la volatilidad implícita del par; ciclo de tipos por la senda de MON-EXP-001.

**Indicadores de seguimiento típicos.** Tipo de cambio del par: referencia del BCE (pares frente al EUR y cruces calculados desde ella) o Fed H.10 (pares frente al USD), o WM/Reuters 16:00 de Londres, declarado; índice de rentabilidad total del par (FX-TR-001); tipo efectivo del BPI de la divisa; DXY o índice amplio de la Fed para tesis de dólar.

**Datos.**
- Fuentes (HT-01): contado de cierre NY 17:00 o referencia oficial; forwards 1M–12M; OIS (SOFR, €STR, TONA, SONIA, SARON, CORRA, AONIA, NZD OCR/BKBM, NOWA, SWESTR); deuda pública a 2 años como alternativa declarada; volatilidades ATM, RR y BF a 25 y 10 delta (1S–1A); CFTC (TFF, semanal); BPI (REER/NEER mensual); IPC y deflactores con vintage; precios de materias primas y pesos de exportación (G10M).
- Convenciones: contado T+2 (T+1 en USD/CAD); bases Act/360 (USD, EUR, JPY, CHF, SEK, NOK) y Act/365 (GBP, AUD, NZD, CAD); delta de contado hasta 1 año y forward después; delta ajustada por prima en USD/JPY, USD/CHF y USD/CAD, sin ajuste en EUR/USD, GBP/USD, AUD/USD y NZD/USD (salvo que la fuente declare otra); ATM DNS.
- Mínimos: contado y diferenciales diarios ≥ 2 años (H1–H3); REER ≥ 10 años; PPA y BEER ≥ 15–20 años con vintages; percentiles CFTC ≥ 3 años.

**Cálculos por defecto por plan.**

| Plan | Cálculos | Uso |
|---|---|---|
| PLAN_MIN (cribado F1, lote por segmento) | FX-TR-001 (rentabilidad total 1M, 3M, 12M); FX-CARRY-001 (carry de la exposición y carry ajustado por implícita 3M); FX-MOM-001 (TSMOM 12M y 3M); FX-RDIFF-001 (cambio del diferencial a 2 años en 4 y 12 semanas y sensibilidad rodante); FX-VOL-001 (implícita 1M, realizada 1M, brecha, percentil); FX-RR-001 (RR 25D 1M y percentil); FX-POS-001 (percentil CFTC y cambio semanal); FX-REER-001 (desviación frente a la media de 20 años); banda GC0 (movimiento semanal en σ semanales, ST-DESC-001) | Señal compuesta y concordancia de lentes (GC1) |
| PLAN_STD (investigación F2) | Lo anterior para la candidata + MON-EXP-001 (senda y divergencia de los dos bancos centrales); FX-PPP-001 (relativa, dos bases); FX-CIP-001 (base 3M y 1A); FX-SURP-001 (sorpresas relativas de 3 meses); FX-TOT-001 (G10M); FX-TERM-001 (volatilidad de evento de la próxima reunión); VOL-GARCH-001; RISK-DD-001; SCN-H-001 (H1–H3) con RI-PA y RI-FWD; segunda vía: carry por puntos frente a OIS, FX-RDIFF-001 en otra ventana | Valoración, carry, catalizadores y asimetría de A; escala de riesgo |
| PLAN_EXT (N3, banda marginal) | Lo anterior + FX-BEER-001 (dos especificaciones); FX-RND-001 (probabilidades neutrales al riesgo de los umbrales de invalidación); FX-PASS-001 (escenarios halcón/paloma); FX-TAIL-001 si la exposición es de carry; FX-COINT-001 (estabilidad de la relación con el diferencial); sensibilidad por fuente de contado (BCE frente a NY 17:00) y por ventana; estabilidad entre semillas | Refutación de supuestos críticos; Prospectiva |

**Métodos por horizonte** (8.3: H1–H4 sí en G10N y G10M):

| Horizonte | Fichas | Uso |
|---|---|---|
| H1 | FX-VOL-001, VOL-GARCH-001, FX-TERM-001, FX-SURP-001, MON-EXP-001, FX-RR-001, FX-GK-001, SCN-H-001 | Bandas por volatilidad y volatilidad de evento alrededor de reuniones y datos; sin señal direccional salvo certificado |
| H2 | FX-RDIFF-001, FX-MOM-001, FX-CARRY-001, FX-POS-001, FX-TOT-001 (G10M), REG-HMM-001 | Diferenciales y sorpresas, momentum, carry/volatilidad, posicionamiento |
| H3 | FX-CARRY-001, MON-EXP-001, FX-PASS-001, FX-REER-001, FX-TOT-001, FX-COINT-001, SCN-H-001 | Divergencia de política monetaria; términos de intercambio; carry con régimen |
| H4 | FX-PPP-001, FX-BEER-001, FX-FEER-001, FX-REER-001, FX-TAYLOR-001, SCN-H-001 (bloques: carry + reversión) | Valor y equilibrio: vida media de 3–5 años |

**Referencias ingenuas y de comparación.** RI-PA (paseo aleatorio sin deriva; notoriamente difícil de batir, Meese y Rogoff, 1983) y RI-FWD (forward como predictor; exceso de rentabilidad nulo) en todo pronóstico; RI-EWMA en volatilidad; **RI-SEG**: rentabilidad en exceso nula (liquidez en la divisa base del usuario, EUR por defecto; 8.4). Habilidad con U de Theil, BSS frente a RI-PA y Clark-West (FX-RW-001).

**Cautelas.**
- Invertir el par o mezclar convenciones de delta y ATM entre pares (USD/JPY ajustada por prima frente a EUR/USD sin ajuste).
- Olvidar el carry en la rentabilidad total o confundir carry por puntos con carry por OIS (la diferencia es la base cruzada, relevante en EUR, JPY y CHF frente a USD).
- Leer la UIP o el forward como previsión; leer la densidad implícita como probabilidad real.
- La relación par–diferencial a 2 años es inestable y se rompe en aversión al riesgo (el JPY y el CHF se aprecian con independencia del diferencial).
- Intervenciones del Ministerio de Finanzas de Japón y del BNS: marcan rupturas de la serie y saltos de volatilidad; el suelo de 1,20 de EUR/CHF (2011–2015) invalida métodos de flotación en esa ventana.
- Liquidez de las coronas (NOK, SEK): horquillas más amplias y saltos en horas de baja liquidez; correlación de G10M con la renta variable global y con las materias primas (FX-CORR-001 por régimen).
- Flujos de cobertura de inversores japoneses y europeos y flujos de fin de mes: estacionalidad de alta frecuencia (FX-STL-001 sobre flujos, no sobre el contado).

**Insuficiencia y abstención.** Ventanas que cruzan un cambio de régimen (suelo de EUR/CHF; tipos negativos y control de la curva del BoJ hasta 2024) sin tratar; implícitas sin convención declarada; diferenciales con tipos de distinto riesgo; percentiles CFTC con menos de 3 años; previsión H1 con probabilidad sin certificado (se entregan bandas).

---

## 3. PERF-FX-EM — Emergentes de Asia, Latinoamérica y EMEA (EMAS, EMLA, EMEA)

**Estado:** documentado · **Prioridad:** P1 · **Ámbito:** pares de divisas emergentes frente al USD o al EUR (USD/CNH, USD/INR, USD/KRW, USD/TWD, USD/IDR, USD/SGD, USD/THB, USD/MYR, USD/PHP, USD/BRL, USD/MXN, USD/CLP, USD/COP, USD/PEN, EUR/PLN, EUR/HUF, EUR/CZK, EUR/RON, USD/TRY, USD/ZAR, USD/ILS…); cruces con el G10 asignados al emergente (regla 1 de 2.6: EUR/PLN → EMEA; USD/MXN → EMLA); bloques regionales (`BLOQUE`); regímenes de tipo fijo, banda o control (`REGIMEN`: HKD, SAR, AED, QAR; ARS, EGP, NGN en ciertos periodos).

**Variables relevantes.** Contado *onshore* y *offshore*; NDF y su fijación; tipos *onshore* e implícitos *offshore*; diferencial real; inflación frente a tipos (ortodoxia monetaria); reservas y sus componentes (métrica ARA), balanza básica y cuenta corriente; deuda externa a corto; CDS soberanos y EMBI (como dato); flujos de cartera e inclusión en índices de bonos; precios de materias primas relevantes (cobre para CLP y PEN; petróleo para COP, MXN y divisas del Golfo; oro y platino para ZAR; semiconductores para KRW y TWD como dato); fijación diaria del CNY y brecha CNH–CNY; régimen de facto (Ilzetzki, Reinhart y Rogoff); volatilidad implícita y RR donde exista mercado.

**Régimen.** REG-HMM-001 con dólar amplio, volatilidad cambiaria global, diferencial de CDS o EMBI y cesta de carry emergente; FX-REGIME-001 sobre la volatilidad del par; FX-BRK-001 para detectar cambios de régimen cambiario e intervenciones; clasificación de facto del régimen en la ventana como **requisito previo** de cualquier método de flotación.

**Indicadores de seguimiento típicos.** Tipo de cambio del par según la referencia oficial publicada (BCE para las divisas que publica; fijaciones locales declaradas: PTAX en BRL, fijación central del PBoC para CNY, tipo de referencia del RBI/FBIL para INR) o WM/Reuters; índice de rentabilidad total del par con carry de NDF en divisas no entregables (FX-NDF-001, FX-TR-001); REER del BPI; **cesta equiponderada de divisas emergentes del segmento frente al USD con carry** como referencia (8.4).

**Datos.**
- Fuentes (HT-01): contado *onshore*, CNH y NDF por plazos con su fijación (p. ej., PTAX, KFTC18, TAIFX1, JISDOR, «dólar observado», TRM); tipos *onshore* (DI en BRL con Bus/252; TIIE en MXN); reservas (FMI, bancos centrales; COFER como contexto); balanza de pagos; CDS soberanos; CFTC solo para MXN, BRL y ZAR; BPI (REER).
- Convenciones: contado T+2 salvo USD/TRY y USD/PHP (T+1); delta forward y ajustada por prima en la mayoría de pares frente al USD (declarada por la fuente); fines de semana y festivos locales; tipo oficial frente a paralelo declarado.
- Mínimos: contado y carry diarios ≥ 2 años (H2–H3); para H1 y H4 «limitados», la petición declara liquidez y catalizador; REER y BEER ≥ 15 años o panel; reservas trimestrales ≥ 5 años.

**Cálculos por defecto por plan.**

| Plan | Cálculos | Uso |
|---|---|---|
| PLAN_MIN (cribado F1, lote por segmento) | FX-TR-001 (con NDF donde proceda); FX-CARRY-001 (carry nominal, real y ajustado por volatilidad); FX-NDF-001 (rendimiento implícito y brecha; CNH–CNY y fijación en EMAS); FX-MOM-001 (3M y 12M); FX-VOL-001 (realizada 1M y 3M; implícita y RR si existen); FX-REER-001 (desviación frente a la media o a la tendencia); FX-POS-001 (MXN, BRL, ZAR); banda GC0 | Señal compuesta (carry ajustado, valor, momentum, flujos) |
| PLAN_STD (investigación F2) | Lo anterior + FX-PPP-001 con ajuste de Balassa-Samuelson; FX-BEER-001 (o panel); FX-TOT-001 (cobre, petróleo, oro, platino según la divisa); cocientes de reservas (FX-PEG-001, paso iv); FX-TAYLOR-001 (inflación frente a tipos, p. ej., TRY); MON-EXP-001 donde haya curva; FX-SURP-001; VOL-GARCH-001 con asimetría direccional; FX-TAIL-001 si la tesis es de carry; RISK-DD-001 con suelo de régimen; SCN-H-001 con RI-PA y RI-FWD; segunda vía: carry por NDF frente a diferencial *onshore* | Valoración, carry, convertibilidad (PS3), riesgo y asimetría |
| PLAN_EXT (N3, banda marginal, `REGIMEN`) | Lo anterior + FX-PEG-001 completo (probabilidad neutral al riesgo de ruptura por escenarios de salto, simulación «se mantiene / se rompe»); FX-RND-001 si hay opciones; FX-PASS-001; estrés con episodios del segmento (1997–98, 2013 *taper tantrum*, 2015, 2018, 2020); sensibilidad a *onshore* frente a *offshore* y a oficial frente a paralelo | Tesis de régimen y de alto impacto |

**Métodos por horizonte** (8.3: H1 limitado; H2–H3 sí; H4 limitado):

| Horizonte | Fichas | Uso |
|---|---|---|
| H1 (limitado) | FX-VOL-001, VOL-GARCH-001, FX-SURP-001, FX-TERM-001 (elecciones, reuniones) | Solo con liquidez suficiente y catalizador; bandas, no direcciones |
| H2 | FX-CARRY-001, FX-NDF-001, FX-MOM-001, FX-POS-001, FX-TOT-001 | Carry ajustado, flujos y momentum |
| H3 | FX-CARRY-001, FX-REER-001, FX-TOT-001, FX-TAYLOR-001, FX-PEG-001, FX-PASS-001, SCN-H-001 | Ciclos de política, términos de intercambio, regímenes |
| H4 (limitado) | FX-PPP-001 (Balassa-Samuelson), FX-BEER-001, FX-FEER-001, FX-PEG-001 | Equilibrio con tendencia de convergencia; sostenibilidad de tipos fijos |

**Referencias ingenuas y de comparación.** RI-PA y RI-FWD (con NDF en divisas no entregables) en todo pronóstico; en tipos fijos creíbles, la habilidad se mide sobre el suceso de ruptura (RI-TB de rupturas comparables), no sobre el nivel; **RI-SEG**: cesta equiponderada de divisas emergentes del segmento frente al USD, con carry (universo ratificado en F10).

**Cautelas.**
- Métodos de libre flotación sobre regímenes gestionados (CNY con fijación y banda de ±2 %; HKD en 7,75–7,85; divisas del Golfo; tipos con intervención frecuente): la volatilidad realizada baja **no** es riesgo bajo; aplicar FX-PEG-001 y el suelo de RISK-DD-001.
- *Onshore* frente a *offshore* (CNY/CNH; INR, KRW y TWD con NDF): el carry invertible para un inversor extranjero es el del NDF; el diferencial *onshore* puede no ser accesible (PS3).
- Tipos oficiales frente a paralelos (ARS, y en ciertos periodos NGN y EGP): el oficial puede no ser invertible ni representativo; series con devaluaciones y unificaciones (EGP 2016 y 2024; NGN 2023) y redenominaciones (TRY 2005) rompen la comparabilidad.
- Asimetría direccional de la volatilidad (USD/ZAR, USD/MXN, USD/BRL suben con la volatilidad) y colas del carry emergente: entregar siempre con FX-TAIL-001 o, como mínimo, con asimetría y ES.
- Balassa-Samuelson: la apreciación real tendencial de economías en convergencia (PLN, CZK, divisas asiáticas) no es desalineamiento.
- Liquidez y horarios locales; festivos y fines de semana distintos; fijaciones con sesgo en tensiones; controles de capital y de repatriación (PS3, PS7).
- Datos de reservas y de balanza de pagos con desfases y revisiones (vintages, M13).

**Insuficiencia y abstención.** Régimen cambiado en la ventana sin tratar; ausencia de forward o NDF y de tipo *onshore* invertible (no hay carry invertible medible); divisa con controles sin exposición alternativa (PS3: el Motor lo señala, el Analista concluye); datos de reservas no disponibles cuando son decisivos; H1 o H4 sin liquidez ni catalizador declarados (`HORIZONTE_NO_APLICABLE`).

---

## 4. PERF-FX-FACT — Estrategias y cestas cambiarias (ESTR)

**Estado:** documentado · **Prioridad:** P1 · **Ámbito:** estrategias sistemáticas (carry G10, carry emergente, carry ajustado por volatilidad, valor, momentum, dólar amplio, *dollar carry*), cestas de refugio (JPY, CHF y oro como referencia), cestas regionales y temáticas de tres o más divisas de segmentos distintos, estrategias de volatilidad cambiaria sobre varias divisas (regla 2 y 3 de 2.6); magnitudes globales para los Analistas transversales.

**Variables relevantes.** Rentabilidades totales de un universo amplio de divisas frente al USD (y frente al EUR si F10 lo pide); primas forward; tipos reales; rentabilidades de formación; volatilidad cambiaria global (media de implícitas o de realizadas); dispersión de tipos entre divisas; correlaciones entre patas; posicionamiento agregado; índices de estrategia publicados como referencia; régimen de riesgo.

**Régimen.** REG-HMM-001 (carry favorable, aversión al riesgo con dólar fuerte, volatilidad alta); percentil de la volatilidad cambiaria global; dispersión de tipos (oportunidad de carry); correlación media entre operaciones de carry (*crowding*).

**Indicadores de seguimiento típicos.** Índice de la estrategia construido por FX-FACT-001 o FX-BASKET-001 con regla publicada; índices de estrategia de terceros con metodología pública (como referencia, no como instrumento); DXY o índice amplio de la Fed para tesis de dólar amplio; índice de la cesta con pesos y divisa de financiación.

**Datos.**
- Fuentes (HT-01): contado y forwards 1M de fin de mes del mismo corte (WM/Reuters o NY 17:00) para un universo fechado de ≥ 20 divisas; tipos reales (IPC con vintage); CFTC; volatilidades implícitas ATM 1M y 3M; horquillas de contado y de puntos forward para costes.
- Convenciones: rentabilidad total en exceso por forwards (FX-TR-001); divisa de valoración USD por defecto (EUR si F10), declarada; rebalanceo mensual; ponderación equiponderada o por inversa de volatilidad, declarada.
- Mínimos: ≥ 10 años mensuales para factores (≥ 20 recomendados); ≥ 5 años para riesgo de cola; universo con altas y bajas fechadas.

**Cálculos por defecto por plan.**

| Plan | Cálculos | Uso |
|---|---|---|
| PLAN_MIN (cribado F1) | FX-FACT-001 (rentabilidad 1M, 3M, 12M y volatilidad de DOL, HML_FX, valor y momentum frente a su historia); FX-CARRY-001 en sección cruzada (dispersión de carry y carry ajustado medio); FX-VOL-001 (volatilidad cambiaria global y percentil); FX-POS-001 agregado (*crowding*); FX-BASKET-001 para cestas propuestas | Régimen de la estrategia y señal de entrada (GC1) |
| PLAN_STD (investigación F2) | Lo anterior + FX-TAIL-001 (asimetría, ES, MDD, carry neto de cobertura); FX-BT-001 de la regla (con costes y subperiodos); BT-DSR-001 con el número de variantes; REG-HMM-001; ML-CLUS-001 (correlación con las opciones de los demás segmentos); RISK-DD-001; SCN-H-001 (H2–H4) frente a RI-SEG | Asimetría, valor relativo de la estrategia, riesgo de cola |
| PLAN_EXT (N3, banda marginal) | Lo anterior + BT-PBO-001; Reality Check o SPA si se probaron muchas variantes; estrés en episodios de colapso (2008, 2015, marzo de 2020, agosto de 2024); sensibilidad al universo, a la ponderación y a los costes; estabilidad entre ventanas | Refutación de sobreajuste |

**Métodos por horizonte** (8.3: H1 No; H2–H4 sí):

| Horizonte | Fichas | Uso |
|---|---|---|
| H1 | — | No aplica: el Motor rechaza la previsión (`HORIZONTE_NO_APLICABLE`) |
| H2 | FX-FACT-001, FX-MOM-001, FX-CARRY-001, REG-HMM-001, FX-VRP-001 | Régimen de volatilidad y momentum de la estrategia |
| H3 | FX-FACT-001, FX-CARRY-001, FX-TAIL-001, FX-BT-001, SCN-H-001 | Carry según régimen; *crowding* |
| H4 | FX-FACT-001 (valor), FX-PPP-001, FX-BT-001, SCN-H-001 | Valor y primas de largo plazo |

**Referencias ingenuas y de comparación.** **RI-SEG**: índice de la estrategia equivalente o, si no existe, rentabilidad nula; RI-FWD (exceso nulo); selección aleatoria de configuración en backtests; RI-PA para la dirección de cestas y del dólar amplio.

**Cautelas.**
- Sobreajuste y fisgoneo (muchas variantes de ventana, universo y ponderación): DSR y PBO obligatorios en PLAN_STD y PLAN_EXT; umbral `t > 3` para factores nuevos.
- Sesgo de supervivencia del universo (divisas legadas del euro, divisas que pasan a tipo fijo o con controles) y exclusiones de la CIP documentadas.
- Costes: las primas de momentum y de carry emergente se reducen materialmente tras horquillas; el coste es un supuesto de mercado, no de un proveedor (Bloque B).
- Régimen: la prima de carry depende de la volatilidad global; los colapsos (2008, 2015, agosto de 2024) concentran pérdidas; el *crowding* aumenta la fragilidad (Brunnermeier, Nagel y Pedersen, 2008).
- Correlaciones inestables entre factores (valor y carry suelen correlacionar negativamente; momentum y carry, poco).
- Una estrategia ESTR no puede duplicar una opción de otro top-3 (regla 4 de 2.6): ML-CLUS-001 la señala.

**Insuficiencia y abstención.** Universo sin fechas de alta y baja; menos de 10 años; número de ensayos no declarado (no se calcula DSR); estrategias definidas después de ver los datos de prueba; H1.

---

## 5. Servicio a los Analistas transversales (AG-09 y AG-21)

| Analista | Campos de su informe (Anexo B, CT-06T) | Cálculos por defecto | Perfil |
|---|---|---|---|
| AG-09 Bancos Centrales y Macro Cambiaria (BCM) | `bancos_centrales` (`senda_descontada`, `sorpresa_reciente`), `diferenciales` (nominales y reales, 2 años), `regimen_global`, `riesgos_intervencion` | MON-EXP-001 por banco central (senda, probabilidades, divergencia); FX-RDIFF-001 (diferenciales y su cambio); FX-SURP-001; FX-TAYLOR-001 (PLAN_STD); REG-HMM-001 (régimen global); FX-BRK-001 (episodios de intervención) | El de la divisa; PERF-FX-FACT para el régimen global |
| AG-21 Posicionamiento, Flujos y Volatilidad Cambiaria (PFV) | `posicionamiento` (`neto_cftc`, `percentil_historico`, `cambio_semanal`), `flujos`, `volatilidad` (`iv_1m`, `rv_1m`, `rr_25d`, `percentil`), `crowding_estrategias`, `base_cruzada` | FX-POS-001; FX-VOL-001; FX-RR-001; FX-TERM-001; FX-VRP-001 (PLAN_STD); FX-CIP-001; FX-FACT-001 (*crowding*) | El del par; PERF-FX-FACT para volatilidad global y *crowding* |

Los informes transversales se calculan una vez por ciclo y sus artefactos se reutilizan por los seis Analistas de segmento (caché del Motor, 7.2): un Analista de segmento no repide un cálculo transversal registrado en el ciclo.

## 6. Ámbitos que cruzan segmentos y asignación

| Ámbito | Segmento principal (2.6) | Perfiles combinados | Riesgos cruzados a explicitar |
|---|---|---|---|
| USD/MXN, USD/BRL, USD/ZAR | EMLA, EMLA, EMEA | PERF-FX-EM (+ PERF-FX-G10 para el lado USD: senda de la Fed) | Correlación con el riesgo global; asimetría de volatilidad |
| EUR/PLN, EUR/HUF, EUR/CZK | EMEA | PERF-FX-EM (+ PERF-FX-G10 para el lado EUR: senda del BCE) | Convergencia (Balassa-Samuelson); liquidez |
| AUD/JPY, CAD/JPY, NZD/JPY | G10M | PERF-FX-G10 | Refugio del JPY en aversión al riesgo; colas del carry |
| Cesta latinoamericana de alto carry frente al USD | ESTR | PERF-FX-FACT + PERF-FX-EM | NDF, controles, correlación de colapsos |
| Cesta de refugio (JPY, CHF; oro como referencia) | ESTR | PERF-FX-FACT + PERF-FX-G10 | Intervenciones (MoF, BNS); el oro no es divisa: solo referencia de comparación |
| Dólar amplio (DXY, índice de la Fed) | ESTR | PERF-FX-FACT + PERF-FX-G10 + PERF-FX-EM | Composición del índice (el DXY sobrepondera el EUR) |
| Ruptura del tipo fijo de una divisa del Golfo | EMEA (`REGIMEN`) | PERF-FX-EM | Precio del petróleo, reservas, forwards con prima de ruptura |
| Volatilidad de USD/JPY (`VOLATILIDAD`) | G10N | PERF-FX-G10 | Prima de volatilidad, intervención |
| Estrategia de volatilidad sobre varias divisas | ESTR | PERF-FX-FACT | Colas de la venta de volatilidad |

Regla: se declara el segmento principal y los perfiles combinados; cada cálculo aplica las cautelas de todos los perfiles afectados; las fichas de un perfil no se aplican por simetría a otro (p. ej., BEER a una divisa con tipo fijo); una misma oportunidad no se calcula como si perteneciera a dos top-3 (regla 4 de 2.6).

## 7. Matriz resumen segmento × horizonte

| Segmento | H1 | H2 | H3 | H4 |
|---|---|---|---|---|
| G10N | FX-VOL, VOL-GARCH, FX-TERM (evento), MON-EXP, FX-SURP | FX-RDIFF, FX-MOM, FX-CARRY, FX-POS | MON-EXP, FX-PASS, FX-CARRY, FX-REER | FX-PPP, FX-BEER, FX-FEER |
| G10M | FX-VOL, VOL-GARCH, FX-SURP | FX-TOT, FX-MOM, FX-CARRY, FX-POS | FX-TOT, FX-CARRY, FX-PASS, FX-COINT | FX-PPP, FX-BEER, FX-TOT |
| EMAS | Limitado: FX-VOL, FX-SURP | FX-NDF, FX-CARRY, FX-MOM | FX-REER, FX-CARRY, FX-PEG (HKD) | Limitado: FX-PPP (Balassa-Samuelson), FX-BEER |
| EMLA | Limitado: FX-VOL, VOL-GARCH | FX-CARRY, FX-NDF, FX-TOT, FX-POS | FX-CARRY, FX-TOT, FX-TAIL, FX-PASS | Limitado: FX-BEER, FX-PPP |
| EMEA | Limitado: FX-VOL, FX-SURP | FX-CARRY, FX-REER, FX-TOT | FX-TAYLOR, FX-REER, FX-PEG | Limitado: FX-BEER, FX-PEG, FX-PPP |
| ESTR | No | FX-FACT, FX-MOM, FX-CARRY | FX-FACT, FX-TAIL, FX-BT | FX-FACT (valor), FX-BT |

En todas las celdas: SCN-H-001 para escenarios sobre el indicador de seguimiento, RISK-VAR-001/RISK-DD-001 para riesgo, y evaluación con FX-RW-001, FC-EVAL-001 y FC-CAL-001 frente al paseo aleatorio y al forward (R13).

## 8. Pruebas de los perfiles

Ningún perfil pasa a «implementado» sin que sus fichas P0 y P1 de PLAN_MIN estén implementadas, ni a «validado» sin las pruebas de `09_Pruebas` que lo afecten, en particular: una misma noticia macro con implicaciones distintas por segmento (p. ej., subida de la Fed en G10N, EMLA y ESTR); un par que cruza segmentos con su asignación por la regla 1 de 2.6; datos insuficientes (divisa con menos de 2 años de NDF, universo de factores sin fechas de baja); horizonte «No» rechazado (ESTR en H1) y «Limitado» sin catalizador rechazado (EMAS en H1); régimen gestionado tratado con métodos de flotación detectado (USD/HKD, USD/CNY); divisa no convertible sin exposición alternativa señalada para PS3; aplicación indebida del método de otro perfil detectada (R21); y una petición de comparar instrumentos rechazada con `FUERA_DE_CATALOGO` (regla 7).
