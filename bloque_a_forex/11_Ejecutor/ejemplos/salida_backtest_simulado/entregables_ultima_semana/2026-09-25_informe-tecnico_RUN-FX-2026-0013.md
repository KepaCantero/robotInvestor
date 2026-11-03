# Informe técnico del Bloque A Forex — Semana 39 de 2026

**Bloque A Forex · Robot Investor · Versión V1.0** · Documento 0 del Bloque A Forex V1.0 · Generado por el ejecutor `bloque_a_forex` V1.0.

> El Bloque A Forex delimita ámbitos cambiarios (qué divisa, frente a cuál, por qué y en qué plazo); el instrumento, el coste, la cobertura y la ejecución corresponden al Bloque B, que recibe el encargo del `paquete_para_bloque_B`.

| Campo | Valor |
|---|---|
| Identificador | `RUN-FX-2026-0013` |
| Tipo | PERIODICO |
| Fecha de referencia | 2026-09-25 |
| Datos de mercado al cierre de | 2026-09-25 |
| Divisa base del usuario | EUR |
| Versión de metodología | FX-1.1 |
| Informes transversales (CT-06T) | BCM `TRV-FX-2026-0025` · PFV `TRV-FX-2026-0026` |
| Dictamen G3 | APTO  |
| Estado del retorno | COMPLETO |
| Entregables hermanos | `/tmp/claude-0/-home-claude/d1ab3b3e-4909-5455-a67a-e01975b6ec91/scratchpad/bt11/salida/entregables/2026-09-25/2026-09-25_informe-visual_RUN-FX-2026-0013.html` · `/tmp/claude-0/-home-claude/d1ab3b3e-4909-5455-a67a-e01975b6ec91/scratchpad/bt11/salida/entregables/2026-09-25/2026-09-25_paquete-json_RUN-FX-2026-0013.json` |

## 1. Resumen ejecutivo

**Lectura del conjunto.** Las opciones dependen sobre todo del dólar y del carry; las apuestas comparten riesgo de giro de tipos.

**Qué ha cambiado.** Cambios derivados de la evolución de las señales y de los diferenciales.

**Apuestas independientes: 14** (N efectivo ML-CLUS-001: 11.290174517647445).

- CL-1: Factor común del clúster CL-1 — OPP-FX-2026-0045
- CL-11: Factor común del clúster CL-11 — OPP-FX-2026-0004
- CL-13: Factor común del clúster CL-13 — OPP-FX-2026-0054
- CL-14: Factor común del clúster CL-14 — OPP-FX-2026-0019
- CL-16: Factor común del clúster CL-16 — OPP-FX-2026-0025
- CL-17: Factor común del clúster CL-17 — OPP-FX-2026-0050
- CL-19: Factor común del clúster CL-19 — OPP-FX-2026-0012
- CL-2: Factor común del clúster CL-2 — OPP-FX-2026-0036
- CL-21: Factor común del clúster CL-21 — OPP-FX-2026-0037
- CL-3: Factor común del clúster CL-3 — OPP-FX-2026-0022
- CL-4: Factor común del clúster CL-4 — OPP-FX-2026-0002
- CL-5: Factor común del clúster CL-5 — OPP-FX-2026-0007
- CL-7: Factor común del clúster CL-7 — OPP-FX-2026-0039
- CL-8: Factor común del clúster CL-8 — OPP-FX-2026-0003

| Segmento | Semáforo | Opción | RK | Riesgo | Carry | Relevancia | Siguiente paso |
|---|---|---|---|---|---|---|---|
| G10N | VERDE | 1 · GBP/JPY alcista · `OPP-FX-2026-0003` | 69 | 2 | +5.10 % anual (a favor) | BAJA | ENVIAR_A_BLOQUE_B |
| G10N | VERDE | 2 · EUR/GBP bajista · `OPP-FX-2026-0002` | 67 | 1 | +2.96 % anual (a favor) | BAJA | ENVIAR_A_BLOQUE_B |
| G10N | VERDE | 3 · USD/CHF alcista · `OPP-FX-2026-0004` | 65 | 2 | +2.45 % anual (a favor) | BAJA | ENVIAR_A_BLOQUE_B |
| G10M | VERDE | 1 · AUD/JPY alcista · `OPP-FX-2026-0045` | 72 | 2 | +2.49 % anual (a favor) | MEDIA | ENVIAR_A_BLOQUE_B |
| G10M | VERDE | 2 · EUR/NOK alcista · `OPP-FX-2026-0007` | 69 | 2 | -4.17 % anual (en contra) | MEDIA | ENVIAR_A_BLOQUE_B |
| G10M | VERDE | 3 · CAD/JPY alcista · `OPP-FX-2026-0036` | 65 | 2 | +3.52 % anual (a favor) | BAJA | ENVIAR_A_BLOQUE_B |
| EMAS | VERDE | 1 · USD/THB alcista · `OPP-FX-2026-0012` | 71 | 1 | +0.39 % anual (a favor) | BAJA | ENVIAR_A_BLOQUE_B |
| EMAS | VERDE | 2 · USD/KRW alcista · `OPP-FX-2026-0025` | 67 | 2 | +0.19 % anual (neutro) | ALTA | ENVIAR_A_BLOQUE_B |
| EMLA | VERDE | 1 · USD/COP bajista · `OPP-FX-2026-0054` | 69 | 5 | +11.25 % anual (a favor) | ALTA | ENVIAR_A_BLOQUE_B |
| EMLA | VERDE | 2 · USD/MXN bajista · `OPP-FX-2026-0050` | 65 | 4 | +4.72 % anual (a favor) | ALTA | ENVIAR_A_BLOQUE_B |
| EMEA | VERDE | 1 · USD/EGP bajista · `OPP-FX-2026-0019` | 69 | 4 | +22.00 % anual (a favor) | ALTA | ENVIAR_A_BLOQUE_B |
| EMEA | VERDE | 2 · USD/ZAR alcista · `OPP-FX-2026-0037` | 65 | 2 | -4.03 % anual (en contra) | MEDIA | ENVIAR_A_BLOQUE_B |
| ESTR | VERDE | 1 · Divisas latinoamericanas frente al USD · `OPP-FX-2026-0022` | 74 | 4 | +5.15 % anual (a favor) | ALTA | ENVIAR_A_BLOQUE_B |
| ESTR | VERDE | 2 · Momentum G10 frente al USD (posición invertida) · `OPP-FX-2026-0039` | 65 | 2 | -0.99 % anual (en contra) | BAJA | ENVIAR_A_BLOQUE_B |

## 2. Alcance, nivel, presupuesto y consumo

| Segmento | Nivel | GC0 cambio material | Motivos |
|---|---|---|---|
| G10N | N1 | no | arrastre verificado |
| G10M | N2 | sí | índice representativo (cesta equiponderada del segmento) se mueve -1.78% en la semana (> 1.5 σ); opción vigente o finalista sobre AUDJPY se mueve -2.29% en la semana (> 1.5 σ); opción vigente o finalista sobre NZDUSD se mueve -1.55% en la semana (> 1.5 σ); opción vigente o finalista sobre USDCAD se mueve -3.59% en la semana (> 1.5 σ); 5 de 8 pares vigilados del segmento se mueven > 1.5 σ (≥ un tercio) |
| EMAS | N1 | no | arrastre verificado |
| EMLA | N2 | sí | índice representativo (cesta equiponderada del segmento) se mueve -1.24% en la semana (> 1.5 σ); opción vigente o finalista sobre USDPEN se mueve -2.39% en la semana (> 1.5 σ); condición de invalidación cumplida en OPP-FX-2026-0016 |
| EMEA | N2 | sí | índice representativo (cesta equiponderada del segmento) se mueve -1.48% en la semana (> 1.5 σ); opción vigente o finalista sobre USDILS se mueve -2.02% en la semana (> 1.5 σ); opción vigente o finalista sobre USDTRY se mueve -1.68% en la semana (> 1.5 σ); 3 de 7 pares vigilados del segmento se mueven > 1.5 σ (≥ un tercio) |
| ESTR | N1 | no | arrastre verificado |

Consumo del RUN (hasta la redacción): 25 llamadas, 19.0675 UC (LLM 17.4675, Motor 1.6); tokens de entrada 92841, salida 23330, caché escritura 0, lectura 622118.

## 3. Régimen macro y cambiario y exposición agregada

Régimen sintético a 2026-09-25: lectura agregada de las señales de 6 segmentos.

**Régimen cambiario.** Dólar debil · riesgo neutro · volatilidad baja.

| Divisa | Exposición agregada | Neta (opciones equivalentes) |
|---|---|---|
| AUD | larga moderada | +0.75 |
| BRL | larga moderada | +0.25 |
| CAD | larga moderada | +0.75 |
| CHF | corta | -1.00 |
| CLP | larga moderada | +0.25 |
| COP | larga | +1.25 |
| EGP | larga | +1.00 |
| EUR | corta moderada | -0.25 |
| GBP | larga | +1.75 |
| JPY | corta fuerte | -3.00 |
| KRW | corta | -1.00 |
| MXN | larga | +1.25 |
| NOK | corta | -1.00 |
| THB | corta | -1.00 |
| USD | larga | +1.00 |
| ZAR | corta | -1.00 |

**Lectura para la divisa base (EUR).** se_deprecia: Las ideas de esta semana apuntan a que el euro pierda algo de valor.

## 4. Análisis por segmento de divisas

### 4.1 G10 núcleo (G10N) — semáforo VERDE

**Régimen.** Régimen de G10N a 2026-09-25: fuerza media de la señal 0.20.

| Etapa | Número |
|---|---|
| Candidatas cribadas | 0 |
| Pasan GC1 | 0 |
| Pasan GC2 | 0 |
| Finalistas GC3 | 0 |
| Elegibles | 3 |
| En el top-3 | 3 |

##### 1. GBP/JPY alcista · `OPP-FX-2026-0003`

- Tipo de opción: CRUCE · par: GBP/JPY · dirección: ALCISTA_BASE · divisa de financiación: JPY
- **Composición.** GBP LARGO 1.00, JPY CORTO 1.00 · Sube la libra esterlina y baja el yen japonés.
- **Ámbito.** Incluye: GBP/JPY, cruce de fixings WM/Reuters: tipo de cambio al contado y su rentabilidad total con carry · Excluye: Instrumentos concretos: su elección corresponde al Bloque B
- **Indicador de seguimiento.** GBP/JPY, cruce de fixings WM/Reuters (`GBPJPY`, HT-01:csv)
- **Convertibilidad (PS3).** convertible sí · NDF no · controles no · profundidad alta · Convertibilidad según el universo del ejecutor y las notas del Analista.
- **Carry (FX-CARRY-001).** +5.10 % anual (a favor) · diferencial base − cotizada +5.10 % · `CALC-FX-2026-1217`
- Clúster: CL-8 · confianza: probable · relevancia: BAJA · reversibilidad: alta · liquidez: alta · régimen de la divisa: LIBRE_FLOTACION
- **Naturaleza de la inversión y horizonte principal (8.3).** CICLICA · **H3**
- **Siguiente paso sugerido: ENVIAR_A_BLOQUE_B**

**Tesis.** GBP/JPY alcista: la señal compuesta, el carry y la valoración sostienen el movimiento en los próximos meses. Sube la libra esterlina y baja el yen japonés.

**Mecanismo.** Diferencial de tipos y flujos de carry coherentes con la señal compuesta del segmento.

**Valoración.** Indicador en el percentil 82% de sus últimos tres años (ST-DESC-001).

**Puntuaciones (HT-03, `HT03-FX-2026-0013-0003`).** T 60 · E 80 · M 50 · A 65 · RK 69

| Horizonte | Vista | Banda o probabilidad | Certificado | Referencia | Medida | Pronóstico | Resolución |
|---|---|---|---|---|---|---|---|
| H2 | alcista | incierto | sin ventaja demostrada frente al paseo aleatorio | paseo aleatorio y forward | PRECIO_CONTADO en JPY | `PRG-FX-2026-0209` | 2026-10-09 — Cierre HT-01 (17:00 America/New_York) de la última sesión ≤ 2026-10-09 frente al de la última sesión ≤ 2026-09-11; suceso: subida de GBPJPY (precio contado, medida en JPY) entre 2026-09-11 y 2026-10-09: Sube la libra esterlina y baja el yen japonés. |
| H3 | alcista | incierto | sin ventaja demostrada frente al paseo aleatorio | paseo aleatorio y forward | PRECIO_CONTADO en JPY | `PRG-FX-2026-0042` | 2027-01-17 — Cierre HT-01 (17:00 America/New_York) de la última sesión ≤ 2027-01-17 frente al de la última sesión ≤ 2026-07-17; suceso: subida de GBPJPY (precio contado, medida en JPY) entre 2026-07-17 y 2027-01-17: Sube la libra esterlina y baja el yen japonés. |

**Catalizadores.** Reunión de política monetaria del banco central de la divisa (2026-08-17)

**Riesgos.** Giro de la política monetaria; Episodio de aversión al riesgo — riesgo sintético **2/5** (RISK-DD-001 v2.0).

**Invalidación.** Cierre de GBPJPY por debajo de 212.9637 (nivel de invalidación, no de entrada)

**Qué cambiaría la conclusión.** Cierre de GBPJPY por debajo de 212.9637 (nivel de invalidación, no de entrada); Confirmación del impulso en las próximas cuatro semanas

**Lo que no sabemos.** Si el diferencial de tipos se mantendrá tras la próxima reunión

**Encargo para el Bloque B.** Consideraciones de implementación: Liquidez máxima en el solape de las sesiones de Londres y Nueva York; Divisas convertibles para un inversor minorista europeo; liquidez máxima en las sesiones de Londres y Nueva York; Carry de la exposición +5.10 % anual (a favor). Carry esperado: +5.10 % anual (a favor). Niveles de referencia: nivel_actual: 225.312 (2026-09-25, 17:00 America/New_York); invalidacion_1: 212.964 (2026-09-25, 17:00 America/New_York). Métricas clave: Evolución del indicador de seguimiento (GBPJPY); Diferencial de tipos y carry de la exposición. Preguntas: ¿Qué forma de exposición a «GBP/JPY alcista» ofrece mejor carry neto de costes para un inversor europeo?

**Evidencia y cálculos.** CLM-FX-2026-0133, CLM-FX-2026-0134, CLM-FX-2026-0011, CLM-FX-2026-0135 · CALC-FX-2026-1204, CALC-FX-2026-1205, CALC-FX-2026-1206, CALC-FX-2026-1207, CALC-FX-2026-1208, CALC-FX-2026-1209, CALC-FX-2026-1217, CALC-FX-2026-1282

##### 2. EUR/GBP bajista · `OPP-FX-2026-0002`

- Tipo de opción: CRUCE · par: EUR/GBP · dirección: BAJISTA_BASE · divisa de financiación: EUR
- **Composición.** EUR CORTO 1.00, GBP LARGO 1.00 · Sube la libra esterlina y baja el euro.
- **Ámbito.** Incluye: EUR/GBP, tipo de referencia del BCE: tipo de cambio al contado y su rentabilidad total con carry · Excluye: Instrumentos concretos: su elección corresponde al Bloque B
- **Indicador de seguimiento.** EUR/GBP, tipo de referencia del BCE (`EURGBP`, HT-01:csv)
- **Convertibilidad (PS3).** convertible sí · NDF no · controles no · profundidad alta · Convertibilidad según el universo del ejecutor y las notas del Analista.
- **Carry (FX-CARRY-001).** +2.96 % anual (a favor) · diferencial base − cotizada -2.96 % · `CALC-FX-2026-1215`
- Clúster: CL-4 · confianza: probable · relevancia: BAJA · reversibilidad: alta · liquidez: alta · régimen de la divisa: LIBRE_FLOTACION
- **Naturaleza de la inversión y horizonte principal (8.3).** CICLICA · **H3**
- **Siguiente paso sugerido: ENVIAR_A_BLOQUE_B**

**Tesis.** EUR/GBP bajista: la señal compuesta, el carry y la valoración sostienen el movimiento en los próximos meses. Sube la libra esterlina y baja el euro.

**Mecanismo.** Diferencial de tipos y flujos de carry coherentes con la señal compuesta del segmento.

**Valoración.** Indicador en el percentil 29% de sus últimos tres años (ST-DESC-001).

**Puntuaciones (HT-03, `HT03-FX-2026-0013-0002`).** T 60 · E 75 · M 50 · A 65 · RK 67

| Horizonte | Vista | Banda o probabilidad | Certificado | Referencia | Medida | Pronóstico | Resolución |
|---|---|---|---|---|---|---|---|
| H2 | bajista | incierto | sin ventaja demostrada frente al paseo aleatorio | paseo aleatorio y forward | PRECIO_CONTADO en GBP | `PRG-FX-2026-0184` | 2026-10-02 — Cierre HT-01 (17:00 America/New_York) de la última sesión ≤ 2026-10-02 frente al de la última sesión ≤ 2026-09-04; suceso: bajada de EURGBP (precio contado, medida en GBP) entre 2026-09-04 y 2026-10-02: Sube la libra esterlina y baja el euro. |
| H3 | bajista | incierto | sin ventaja demostrada frente al paseo aleatorio | paseo aleatorio y forward | PRECIO_CONTADO en GBP | `PRG-FX-2026-0093` | 2027-02-07 — Cierre HT-01 (17:00 America/New_York) de la última sesión ≤ 2027-02-07 frente al de la última sesión ≤ 2026-08-07; suceso: bajada de EURGBP (precio contado, medida en GBP) entre 2026-08-07 y 2027-02-07: Sube la libra esterlina y baja el euro. |

**Catalizadores.** Reunión de política monetaria del banco central de la divisa (2026-09-07)

**Riesgos.** Giro de la política monetaria; Episodio de aversión al riesgo — riesgo sintético **1/5** (RISK-DD-001 v2.0).

**Invalidación.** Cierre de EURGBP por encima de 1.004 (nivel de invalidación, no de entrada)

**Qué cambiaría la conclusión.** Cierre de EURGBP por encima de 1.004 (nivel de invalidación, no de entrada); Confirmación del impulso en las próximas cuatro semanas

**Lo que no sabemos.** Si el diferencial de tipos se mantendrá tras la próxima reunión

**Encargo para el Bloque B.** Consideraciones de implementación: Liquidez máxima en el solape de las sesiones de Londres y Nueva York; Divisas convertibles para un inversor minorista europeo; liquidez máxima en las sesiones de Londres y Nueva York; Carry de la exposición +2.96 % anual (a favor). Carry esperado: +2.96 % anual (a favor). Niveles de referencia: nivel_actual: 0.993657 (2026-09-25, 17:00 America/New_York); invalidacion_1: 1.004 (2026-09-25, 17:00 America/New_York). Métricas clave: Evolución del indicador de seguimiento (EURGBP); Diferencial de tipos y carry de la exposición. Preguntas: ¿Qué forma de exposición a «EUR/GBP bajista» ofrece mejor carry neto de costes para un inversor europeo?

**Evidencia y cálculos.** CLM-FX-2026-0189, CLM-FX-2026-0190, CLM-FX-2026-0007, CLM-FX-2026-0208 · CALC-FX-2026-1204, CALC-FX-2026-1205, CALC-FX-2026-1206, CALC-FX-2026-1207, CALC-FX-2026-1208, CALC-FX-2026-1209, CALC-FX-2026-1215, CALC-FX-2026-1282

##### 3. USD/CHF alcista · `OPP-FX-2026-0004`

- Tipo de opción: PAR · par: USD/CHF · dirección: ALCISTA_BASE · divisa de financiación: CHF
- **Composición.** USD LARGO 1.00, CHF CORTO 1.00 · Sube el dólar de EE. UU. y baja el franco suizo.
- **Ámbito.** Incluye: USD/CHF, Fed H.10: tipo de cambio al contado y su rentabilidad total con carry · Excluye: Instrumentos concretos: su elección corresponde al Bloque B
- **Indicador de seguimiento.** USD/CHF, Fed H.10 (`USDCHF`, HT-01:csv)
- **Convertibilidad (PS3).** convertible sí · NDF no · controles no · profundidad alta · Convertibilidad según el universo del ejecutor y las notas del Analista.
- **Carry (FX-CARRY-001).** +2.45 % anual (a favor) · diferencial base − cotizada +2.45 % · `CALC-FX-2026-1213`
- Clúster: CL-11 · confianza: probable · relevancia: BAJA · reversibilidad: alta · liquidez: alta · régimen de la divisa: FLOTACION_ADMINISTRADA
- **Naturaleza de la inversión y horizonte principal (8.3).** CICLICA · **H3**
- **Siguiente paso sugerido: ENVIAR_A_BLOQUE_B**

**Tesis.** USD/CHF alcista: la señal compuesta, el carry y la valoración sostienen el movimiento en los próximos meses. Sube el dólar de EE. UU. y baja el franco suizo.

**Mecanismo.** Diferencial de tipos y flujos de carry coherentes con la señal compuesta del segmento.

**Valoración.** Indicador en el percentil 91% de sus últimos tres años (ST-DESC-001).

**Puntuaciones (HT-03, `HT03-FX-2026-0013-0004`).** T 60 · E 75 · M 50 · A 60 · RK 65

| Horizonte | Vista | Banda o probabilidad | Certificado | Referencia | Medida | Pronóstico | Resolución |
|---|---|---|---|---|---|---|---|
| H2 | alcista | incierto | sin ventaja demostrada frente al paseo aleatorio | paseo aleatorio y forward | PRECIO_CONTADO en CHF | `PRG-FX-2026-0210` | 2026-10-09 — Cierre HT-01 (17:00 America/New_York) de la última sesión ≤ 2026-10-09 frente al de la última sesión ≤ 2026-09-11; suceso: subida de USDCHF (precio contado, medida en CHF) entre 2026-09-11 y 2026-10-09: Sube el dólar de EE. UU. y baja el franco suizo. |
| H3 | alcista | incierto | sin ventaja demostrada frente al paseo aleatorio | paseo aleatorio y forward | PRECIO_CONTADO en CHF | `PRG-FX-2026-0211` | 2027-03-11 — Cierre HT-01 (17:00 America/New_York) de la última sesión ≤ 2027-03-11 frente al de la última sesión ≤ 2026-09-11; suceso: subida de USDCHF (precio contado, medida en CHF) entre 2026-09-11 y 2027-03-11: Sube el dólar de EE. UU. y baja el franco suizo. |

**Catalizadores.** Reunión de política monetaria del banco central de la divisa (2026-10-11)

**Riesgos.** Giro de la política monetaria; Episodio de aversión al riesgo — riesgo sintético **2/5** (RISK-DD-001 v2.0).

**Invalidación.** Cierre de USDCHF por debajo de 1.3256 (nivel de invalidación, no de entrada)

**Qué cambiaría la conclusión.** Cierre de USDCHF por debajo de 1.3256 (nivel de invalidación, no de entrada); Confirmación del impulso en las próximas cuatro semanas

**Lo que no sabemos.** Si el diferencial de tipos se mantendrá tras la próxima reunión

**Encargo para el Bloque B.** Consideraciones de implementación: Liquidez máxima en el solape de las sesiones de Londres y Nueva York; Divisas convertibles para un inversor minorista europeo; liquidez máxima en las sesiones de Londres y Nueva York; Carry de la exposición +2.45 % anual (a favor). Carry esperado: +2.45 % anual (a favor). Niveles de referencia: nivel_actual: 1.38602 (2026-09-25, 17:00 America/New_York); invalidacion_1: 1.3256 (2026-09-25, 17:00 America/New_York). Métricas clave: Evolución del indicador de seguimiento (USDCHF); Diferencial de tipos y carry de la exposición. Preguntas: ¿Qué forma de exposición a «USD/CHF alcista» ofrece mejor carry neto de costes para un inversor europeo?

**Evidencia y cálculos.** CLM-FX-2026-0368, CLM-FX-2026-0289, CLM-FX-2026-0015, CLM-FX-2026-0369 · CALC-FX-2026-1204, CALC-FX-2026-1205, CALC-FX-2026-1206, CALC-FX-2026-1207, CALC-FX-2026-1208, CALC-FX-2026-1209, CALC-FX-2026-1213, CALC-FX-2026-1282

### 4.2 G10 de materias primas y escandinavas (G10M) — semáforo VERDE

**Régimen.** Régimen de G10M a 2026-09-25: fuerza media de la señal 0.28.

| Etapa | Número |
|---|---|
| Candidatas cribadas | 8 |
| Pasan GC1 | 6 |
| Pasan GC2 | 4 |
| Finalistas GC3 | 4 |
| Elegibles | 3 |
| En el top-3 | 3 |

##### 1. AUD/JPY alcista · `OPP-FX-2026-0045`

- Tipo de opción: CRUCE · par: AUD/JPY · dirección: ALCISTA_BASE · divisa de financiación: JPY
- **Composición.** AUD LARGO 1.00, JPY CORTO 1.00 · Sube el dólar australiano y baja el yen japonés.
- **Ámbito.** Incluye: AUD/JPY, cruce de fixings WM/Reuters: tipo de cambio al contado y su rentabilidad total con carry · Excluye: Instrumentos concretos: su elección corresponde al Bloque B
- **Indicador de seguimiento.** AUD/JPY, cruce de fixings WM/Reuters (`AUDJPY`, HT-01:csv)
- **Convertibilidad (PS3).** convertible sí · NDF no · controles no · profundidad alta · Convertibilidad según el universo del ejecutor y las notas del Analista.
- **Carry (FX-CARRY-001).** +2.49 % anual (a favor) · diferencial base − cotizada +2.49 % · `CALC-FX-2026-1230`
- Clúster: CL-1 · confianza: probable · relevancia: MEDIA · reversibilidad: alta · liquidez: alta · régimen de la divisa: LIBRE_FLOTACION
- **Naturaleza de la inversión y horizonte principal (8.3).** CICLICA · **H3**
- **Siguiente paso sugerido: ENVIAR_A_BLOQUE_B**

**Tesis.** AUD/JPY alcista: la señal compuesta, el carry y la valoración sostienen el movimiento en los próximos meses. Sube el dólar australiano y baja el yen japonés.

**Mecanismo.** Diferencial de tipos y flujos de carry coherentes con la señal compuesta del segmento.

**Valoración.** Indicador en el percentil 59% de sus últimos tres años (ST-DESC-001).

**Puntuaciones (HT-03, `HT03-FX-2026-0013-0045`).** T 70 · E 75 · M 50 · A 70 · RK 72

| Horizonte | Vista | Banda o probabilidad | Certificado | Referencia | Medida | Pronóstico | Resolución |
|---|---|---|---|---|---|---|---|
| H2 | alcista | más probable que no | sin ventaja demostrada frente al paseo aleatorio | paseo aleatorio y forward | PRECIO_CONTADO en JPY | `PRG-FX-2026-0247` | 2026-10-23 — Cierre HT-01 (17:00 America/New_York) de la última sesión ≤ 2026-10-23 frente al de la última sesión ≤ 2026-09-25; suceso: subida de AUDJPY (precio contado, medida en JPY) entre 2026-09-25 y 2026-10-23: Sube el dólar australiano y baja el yen japonés. |
| H3 | alcista | más probable que no | sin ventaja demostrada frente al paseo aleatorio | paseo aleatorio y forward | PRECIO_CONTADO en JPY | `PRG-FX-2026-0248` | 2027-03-25 — Cierre HT-01 (17:00 America/New_York) de la última sesión ≤ 2027-03-25 frente al de la última sesión ≤ 2026-09-25; suceso: subida de AUDJPY (precio contado, medida en JPY) entre 2026-09-25 y 2027-03-25: Sube el dólar australiano y baja el yen japonés. |

**Catalizadores.** Reunión de política monetaria del banco central de la divisa (2026-10-25)

**Riesgos.** Giro de la política monetaria; Episodio de aversión al riesgo — riesgo sintético **2/5** (RISK-DD-001 v2.0).

**Invalidación.** Cierre de AUDJPY por debajo de 98.9076 (nivel de invalidación, no de entrada)

**Qué cambiaría la conclusión.** Cierre de AUDJPY por debajo de 98.9076 (nivel de invalidación, no de entrada); Confirmación del impulso en las próximas cuatro semanas

**Lo que no sabemos.** Si el diferencial de tipos se mantendrá tras la próxima reunión

**Encargo para el Bloque B.** Consideraciones de implementación: Liquidez máxima en el solape de las sesiones de Londres y Nueva York; Divisas convertibles para un inversor minorista europeo; liquidez máxima en las sesiones de Londres y Nueva York; Carry de la exposición +2.49 % anual (a favor). Carry esperado: +2.49 % anual (a favor). Niveles de referencia: nivel_actual: 104.113 (2026-09-25, 17:00 America/New_York); invalidacion_1: 98.9076 (2026-09-25, 17:00 America/New_York). Métricas clave: Evolución del indicador de seguimiento (AUDJPY); Diferencial de tipos y carry de la exposición. Preguntas: ¿Qué forma de exposición a «AUD/JPY alcista» ofrece mejor carry neto de costes para un inversor europeo?

**Evidencia y cálculos.** CLM-FX-2026-0350, CLM-FX-2026-0143, CLM-FX-2026-0025, CLM-FX-2026-0426 · CALC-FX-2026-1218, CALC-FX-2026-1219, CALC-FX-2026-1220, CALC-FX-2026-1221, CALC-FX-2026-1222, CALC-FX-2026-1223, CALC-FX-2026-1230, CALC-FX-2026-1282

##### 2. EUR/NOK alcista · `OPP-FX-2026-0007`

- Tipo de opción: CRUCE · par: EUR/NOK · dirección: ALCISTA_BASE · divisa de financiación: NOK
- **Composición.** EUR LARGO 1.00, NOK CORTO 1.00 · Sube el euro y baja la corona noruega.
- **Ámbito.** Incluye: EUR/NOK, tipo de referencia del BCE: tipo de cambio al contado y su rentabilidad total con carry · Excluye: Instrumentos concretos: su elección corresponde al Bloque B
- **Indicador de seguimiento.** EUR/NOK, tipo de referencia del BCE (`EURNOK`, HT-01:csv)
- **Convertibilidad (PS3).** convertible sí · NDF no · controles no · profundidad media · Convertibilidad según el universo del ejecutor y las notas del Analista.
- **Carry (FX-CARRY-001).** -4.17 % anual (en contra) · diferencial base − cotizada -4.17 % · `CALC-FX-2026-1227`
- Clúster: CL-5 · confianza: probable · relevancia: MEDIA · reversibilidad: media · liquidez: media · régimen de la divisa: LIBRE_FLOTACION
- **Naturaleza de la inversión y horizonte principal (8.3).** CICLICA · **H3**
- **Siguiente paso sugerido: ENVIAR_A_BLOQUE_B**

**Tesis.** EUR/NOK alcista: la señal compuesta, el carry y la valoración sostienen el movimiento en los próximos meses. Sube el euro y baja la corona noruega.

**Mecanismo.** Diferencial de tipos y flujos de carry coherentes con la señal compuesta del segmento.

**Valoración.** Indicador en el percentil 36% de sus últimos tres años (ST-DESC-001).

**Puntuaciones (HT-03, `HT03-FX-2026-0013-0007`).** T 70 · E 75 · M 50 · A 65 · RK 69

| Horizonte | Vista | Banda o probabilidad | Certificado | Referencia | Medida | Pronóstico | Resolución |
|---|---|---|---|---|---|---|---|
| H2 | alcista | más probable que no | sin ventaja demostrada frente al paseo aleatorio | paseo aleatorio y forward | PRECIO_CONTADO en NOK | `PRG-FX-2026-0249` | 2026-10-23 — Cierre HT-01 (17:00 America/New_York) de la última sesión ≤ 2026-10-23 frente al de la última sesión ≤ 2026-09-25; suceso: subida de EURNOK (precio contado, medida en NOK) entre 2026-09-25 y 2026-10-23: Sube el euro y baja la corona noruega. |
| H3 | alcista | más probable que no | sin ventaja demostrada frente al paseo aleatorio | paseo aleatorio y forward | PRECIO_CONTADO en NOK | `PRG-FX-2026-0250` | 2027-03-25 — Cierre HT-01 (17:00 America/New_York) de la última sesión ≤ 2027-03-25 frente al de la última sesión ≤ 2026-09-25; suceso: subida de EURNOK (precio contado, medida en NOK) entre 2026-09-25 y 2027-03-25: Sube el euro y baja la corona noruega. |

**Catalizadores.** Reunión de política monetaria del banco central de la divisa (2026-10-25)

**Riesgos.** Giro de la política monetaria; Episodio de aversión al riesgo — riesgo sintético **2/5** (RISK-DD-001 v2.0).

**Invalidación.** Cierre de EURNOK por debajo de 9.4029 (nivel de invalidación, no de entrada)

**Qué cambiaría la conclusión.** Cierre de EURNOK por debajo de 9.4029 (nivel de invalidación, no de entrada); Confirmación del impulso en las próximas cuatro semanas

**Lo que no sabemos.** Si el diferencial de tipos se mantendrá tras la próxima reunión

**Encargo para el Bloque B.** Consideraciones de implementación: Liquidez máxima en el solape de las sesiones de Londres y Nueva York; Divisas convertibles para un inversor minorista europeo; liquidez máxima en las sesiones de Londres y Nueva York; Carry de la exposición -4.17 % anual (en contra). Carry esperado: -4.17 % anual (en contra). Niveles de referencia: nivel_actual: 9.8978 (2026-09-25, 17:00 America/New_York); invalidacion_1: 9.4029 (2026-09-25, 17:00 America/New_York). Métricas clave: Evolución del indicador de seguimiento (EURNOK); Diferencial de tipos y carry de la exposición. Preguntas: ¿Qué forma de exposición a «EUR/NOK alcista» ofrece mejor carry neto de costes para un inversor europeo?

**Evidencia y cálculos.** CLM-FX-2026-0242, CLM-FX-2026-0028, CLM-FX-2026-0029, CLM-FX-2026-0428 · CALC-FX-2026-1218, CALC-FX-2026-1219, CALC-FX-2026-1220, CALC-FX-2026-1221, CALC-FX-2026-1222, CALC-FX-2026-1223, CALC-FX-2026-1227, CALC-FX-2026-1282

##### 3. CAD/JPY alcista · `OPP-FX-2026-0036`

- Tipo de opción: CRUCE · par: CAD/JPY · dirección: ALCISTA_BASE · divisa de financiación: JPY
- **Composición.** CAD LARGO 1.00, JPY CORTO 1.00 · Sube el dólar canadiense y baja el yen japonés.
- **Ámbito.** Incluye: CAD/JPY, cruce de fixings WM/Reuters: tipo de cambio al contado y su rentabilidad total con carry · Excluye: Instrumentos concretos: su elección corresponde al Bloque B
- **Indicador de seguimiento.** CAD/JPY, cruce de fixings WM/Reuters (`CADJPY`, HT-01:csv)
- **Convertibilidad (PS3).** convertible sí · NDF no · controles no · profundidad media · Convertibilidad según el universo del ejecutor y las notas del Analista.
- **Carry (FX-CARRY-001).** +3.52 % anual (a favor) · diferencial base − cotizada +3.53 % · `CALC-FX-2026-1231`
- Clúster: CL-2 · confianza: probable · relevancia: BAJA · reversibilidad: media · liquidez: media · régimen de la divisa: LIBRE_FLOTACION
- **Naturaleza de la inversión y horizonte principal (8.3).** CICLICA · **H3**
- **Siguiente paso sugerido: ENVIAR_A_BLOQUE_B**

**Tesis.** CAD/JPY alcista: la señal compuesta, el carry y la valoración sostienen el movimiento en los próximos meses. Sube el dólar canadiense y baja el yen japonés.

**Mecanismo.** Diferencial de tipos y flujos de carry coherentes con la señal compuesta del segmento.

**Valoración.** Indicador en el percentil 51% de sus últimos tres años (ST-DESC-001).

**Puntuaciones (HT-03, `HT03-FX-2026-0013-0036`).** T 60 · E 75 · M 50 · A 60 · RK 65

| Horizonte | Vista | Banda o probabilidad | Certificado | Referencia | Medida | Pronóstico | Resolución |
|---|---|---|---|---|---|---|---|
| H2 | alcista | incierto | sin ventaja demostrada frente al paseo aleatorio | paseo aleatorio y forward | PRECIO_CONTADO en JPY | `PRG-FX-2026-0237` | 2026-10-16 — Cierre HT-01 (17:00 America/New_York) de la última sesión ≤ 2026-10-16 frente al de la última sesión ≤ 2026-09-18; suceso: subida de CADJPY (precio contado, medida en JPY) entre 2026-09-18 y 2026-10-16: Sube el dólar canadiense y baja el yen japonés. |
| H3 | alcista | incierto | sin ventaja demostrada frente al paseo aleatorio | paseo aleatorio y forward | PRECIO_CONTADO en JPY | `PRG-FX-2026-0238` | 2027-03-18 — Cierre HT-01 (17:00 America/New_York) de la última sesión ≤ 2027-03-18 frente al de la última sesión ≤ 2026-09-18; suceso: subida de CADJPY (precio contado, medida en JPY) entre 2026-09-18 y 2027-03-18: Sube el dólar canadiense y baja el yen japonés. |

**Catalizadores.** Reunión de política monetaria del banco central de la divisa (2026-10-18)

**Riesgos.** Giro de la política monetaria; Episodio de aversión al riesgo — riesgo sintético **2/5** (RISK-DD-001 v2.0).

**Invalidación.** Cierre de CADJPY por debajo de 95.144 (nivel de invalidación, no de entrada)

**Qué cambiaría la conclusión.** Cierre de CADJPY por debajo de 95.144 (nivel de invalidación, no de entrada); Confirmación del impulso en las próximas cuatro semanas

**Lo que no sabemos.** Si el diferencial de tipos se mantendrá tras la próxima reunión

**Encargo para el Bloque B.** Consideraciones de implementación: Liquidez máxima en el solape de las sesiones de Londres y Nueva York; Divisas convertibles para un inversor minorista europeo; liquidez máxima en las sesiones de Londres y Nueva York; Carry de la exposición +3.52 % anual (a favor). Carry esperado: +3.52 % anual (a favor). Niveles de referencia: nivel_actual: 99.6635 (2026-09-25, 17:00 America/New_York); invalidacion_1: 95.144 (2026-09-25, 17:00 America/New_York). Métricas clave: Evolución del indicador de seguimiento (CADJPY); Diferencial de tipos y carry de la exposición. Preguntas: ¿Qué forma de exposición a «CAD/JPY alcista» ofrece mejor carry neto de costes para un inversor europeo?

**Evidencia y cálculos.** CLM-FX-2026-0409, CLM-FX-2026-0294, CLM-FX-2026-0248, CLM-FX-2026-0410 · CALC-FX-2026-1218, CALC-FX-2026-1219, CALC-FX-2026-1220, CALC-FX-2026-1221, CALC-FX-2026-1222, CALC-FX-2026-1223, CALC-FX-2026-1231, CALC-FX-2026-1282

### 4.3 Emergentes de Asia (EMAS) — semáforo VERDE

**Régimen.** Régimen de EMAS a 2026-09-25: fuerza media de la señal 0.22.

| Etapa | Número |
|---|---|
| Candidatas cribadas | 0 |
| Pasan GC1 | 0 |
| Pasan GC2 | 0 |
| Finalistas GC3 | 0 |
| Elegibles | 2 |
| En el top-3 | 2 |

**Menos de tres (R14).** Se proponen 2 opción(es) en Emergentes de Asia. Se proponen 2 opción(es): de 2 candidatas analizadas, 2 finalistas evaluadas y 2 elegibles (R14).

##### 1. USD/THB alcista · `OPP-FX-2026-0012`

- Tipo de opción: PAR · par: USD/THB · dirección: ALCISTA_BASE · divisa de financiación: THB
- **Composición.** USD LARGO 1.00, THB CORTO 1.00 · Sube el dólar de EE. UU. y baja el baht tailandés.
- **Ámbito.** Incluye: USD/THB, Banco de Tailandia: tipo de cambio al contado y su rentabilidad total con carry · Excluye: Instrumentos concretos: su elección corresponde al Bloque B
- **Indicador de seguimiento.** USD/THB, Banco de Tailandia (`USDTHB`, HT-01:csv)
- **Convertibilidad (PS3).** convertible sí · NDF no · controles no · profundidad media · Convertibilidad según el universo del ejecutor y las notas del Analista.
- **Carry (FX-CARRY-001).** +0.39 % anual (a favor) · diferencial base − cotizada +0.39 % · `CALC-FX-2026-1244`
- Clúster: CL-19 · confianza: probable · relevancia: BAJA · reversibilidad: media · liquidez: media · régimen de la divisa: FLOTACION_ADMINISTRADA
- **Naturaleza de la inversión y horizonte principal (8.3).** CICLICA · **H3**
- **Siguiente paso sugerido: ENVIAR_A_BLOQUE_B**

**Tesis.** USD/THB alcista: la señal compuesta, el carry y la valoración sostienen el movimiento en los próximos meses. Sube el dólar de EE. UU. y baja el baht tailandés.

**Mecanismo.** Diferencial de tipos y flujos de carry coherentes con la señal compuesta del segmento.

**Valoración.** Indicador en el percentil 80% de sus últimos tres años (ST-DESC-001).

**Puntuaciones (HT-03, `HT03-FX-2026-0013-0012`).** T 70 · E 80 · M 50 · A 65 · RK 71

| Horizonte | Vista | Banda o probabilidad | Certificado | Referencia | Medida | Pronóstico | Resolución |
|---|---|---|---|---|---|---|---|
| H2 | alcista | incierto | sin ventaja demostrada frente al paseo aleatorio | paseo aleatorio y forward | PRECIO_CONTADO en THB | `PRG-FX-2026-0241` | 2026-10-16 — Cierre HT-01 (17:00 America/New_York) de la última sesión ≤ 2026-10-16 frente al de la última sesión ≤ 2026-09-18; suceso: subida de USDTHB (precio contado, medida en THB) entre 2026-09-18 y 2026-10-16: Sube el dólar de EE. UU. y baja el baht tailandés. |
| H3 | alcista | incierto | sin ventaja demostrada frente al paseo aleatorio | paseo aleatorio y forward | PRECIO_CONTADO en THB | `PRG-FX-2026-0242` | 2027-03-18 — Cierre HT-01 (17:00 America/New_York) de la última sesión ≤ 2027-03-18 frente al de la última sesión ≤ 2026-09-18; suceso: subida de USDTHB (precio contado, medida en THB) entre 2026-09-18 y 2027-03-18: Sube el dólar de EE. UU. y baja el baht tailandés. |

**Catalizadores.** Reunión de política monetaria del banco central de la divisa (2026-10-18)

**Riesgos.** Giro de la política monetaria; Episodio de aversión al riesgo — riesgo sintético **1/5** (RISK-DD-001 v2.0).

**Invalidación.** Cierre de USDTHB por debajo de 34.5688 (nivel de invalidación, no de entrada)

**Qué cambiaría la conclusión.** Cierre de USDTHB por debajo de 34.5688 (nivel de invalidación, no de entrada); Confirmación del impulso en las próximas cuatro semanas

**Lo que no sabemos.** Si el diferencial de tipos se mantendrá tras la próxima reunión

**Encargo para el Bloque B.** Consideraciones de implementación: Liquidez máxima en el solape de las sesiones de Londres y Nueva York; Divisas convertibles para un inversor minorista europeo; liquidez máxima en las sesiones de Londres y Nueva York; Carry de la exposición +0.39 % anual (a favor). Carry esperado: +0.39 % anual (a favor). Niveles de referencia: nivel_actual: 36.6401 (2026-09-25, 17:00 America/New_York); invalidacion_1: 34.5688 (2026-09-25, 17:00 America/New_York). Métricas clave: Evolución del indicador de seguimiento (USDTHB); Diferencial de tipos y carry de la exposición. Preguntas: ¿Qué forma de exposición a «USD/THB alcista» ofrece mejor carry neto de costes para un inversor europeo?

**Evidencia y cálculos.** CLM-FX-2026-0411, CLM-FX-2026-0304, CLM-FX-2026-0049, CLM-FX-2026-0412 · CALC-FX-2026-1232, CALC-FX-2026-1233, CALC-FX-2026-1234, CALC-FX-2026-1235, CALC-FX-2026-1236, CALC-FX-2026-1237, CALC-FX-2026-1244, CALC-FX-2026-1282

##### 2. USD/KRW alcista · `OPP-FX-2026-0025`

- Tipo de opción: PAR · par: USD/KRW · dirección: ALCISTA_BASE · divisa de financiación: KRW
- **Composición.** USD LARGO 1.00, KRW CORTO 1.00 · Sube el dólar de EE. UU. y baja el won coreano.
- **Ámbito.** Incluye: USD/KRW, cierre de Seúl: tipo de cambio al contado y su rentabilidad total con carry · Excluye: Instrumentos concretos: su elección corresponde al Bloque B
- **Indicador de seguimiento.** USD/KRW, cierre de Seúl (`USDKRW`, HT-01:csv)
- **Convertibilidad (PS3).** convertible no · NDF sí · controles no · profundidad media · Convertibilidad según el universo del ejecutor y las notas del Analista.
- **Carry (FX-CARRY-001).** +0.19 % anual (neutro) · diferencial base − cotizada +0.19 % · `CALC-FX-2026-1240`
- Clúster: CL-16 · confianza: probable · relevancia: ALTA · reversibilidad: baja · liquidez: media · régimen de la divisa: LIBRE_FLOTACION
- **Naturaleza de la inversión y horizonte principal (8.3).** CICLICA · **H3**
- **Siguiente paso sugerido: ENVIAR_A_BLOQUE_B**

**Tesis.** USD/KRW alcista: la señal compuesta, el carry y la valoración sostienen el movimiento en los próximos meses. Sube el dólar de EE. UU. y baja el won coreano.

**Mecanismo.** Diferencial de tipos y flujos de carry coherentes con la señal compuesta del segmento.

**Valoración.** Indicador en el percentil 97% de sus últimos tres años (ST-DESC-001).

**Puntuaciones (HT-03, `HT03-FX-2026-0013-0025`).** T 60 · E 80 · M 50 · A 60 · RK 67

| Horizonte | Vista | Banda o probabilidad | Certificado | Referencia | Medida | Pronóstico | Resolución |
|---|---|---|---|---|---|---|---|
| H2 | alcista | más probable que no | sin ventaja demostrada frente al paseo aleatorio | paseo aleatorio y forward | PRECIO_CONTADO en KRW | `PRG-FX-2026-0199` | 2026-10-02 — Cierre HT-01 (17:00 America/New_York) de la última sesión ≤ 2026-10-02 frente al de la última sesión ≤ 2026-09-04; suceso: subida de USDKRW (precio contado, medida en KRW) entre 2026-09-04 y 2026-10-02: Sube el dólar de EE. UU. y baja el won coreano. |
| H3 | alcista | más probable que no | sin ventaja demostrada frente al paseo aleatorio | paseo aleatorio y forward | PRECIO_CONTADO en KRW | `PRG-FX-2026-0034` | 2027-01-10 — Cierre HT-01 (17:00 America/New_York) de la última sesión ≤ 2027-01-10 frente al de la última sesión ≤ 2026-07-10; suceso: subida de USDKRW (precio contado, medida en KRW) entre 2026-07-10 y 2027-01-10: Sube el dólar de EE. UU. y baja el won coreano. |

**Catalizadores.** Reunión de política monetaria del banco central de la divisa (2026-08-10)

**Riesgos.** Giro de la política monetaria; Episodio de aversión al riesgo — riesgo sintético **2/5** (RISK-DD-001 v2.0).

**Invalidación.** Cierre de USDKRW por debajo de 1283.1146 (nivel de invalidación, no de entrada)

**Qué cambiaría la conclusión.** Cierre de USDKRW por debajo de 1283.1146 (nivel de invalidación, no de entrada); Confirmación del impulso en las próximas cuatro semanas

**Lo que no sabemos.** Si el diferencial de tipos se mantendrá tras la próxima reunión

**Encargo para el Bloque B.** Consideraciones de implementación: Liquidez máxima en el solape de las sesiones de Londres y Nueva York; Divisa no plenamente convertible: existe mercado no entregable (liquidación en otra divisa); Carry de la exposición +0.19 % anual (neutro). Carry esperado: +0.19 % anual (neutro). Niveles de referencia: nivel_actual: 1310.89 (2026-09-25, 17:00 America/New_York); invalidacion_1: 1283.11 (2026-09-25, 17:00 America/New_York). Métricas clave: Evolución del indicador de seguimiento (USDKRW); Diferencial de tipos y carry de la exposición. Preguntas: ¿Qué forma de exposición a «USD/KRW alcista» ofrece mejor carry neto de costes para un inversor europeo?

**Evidencia y cálculos.** CLM-FX-2026-0113, CLM-FX-2026-0114, CLM-FX-2026-0115, CLM-FX-2026-0116 · CALC-FX-2026-1232, CALC-FX-2026-1233, CALC-FX-2026-1234, CALC-FX-2026-1235, CALC-FX-2026-1236, CALC-FX-2026-1237, CALC-FX-2026-1240, CALC-FX-2026-1282

### 4.4 Emergentes de Latinoamérica (EMLA) — semáforo VERDE

**Régimen.** Régimen de EMLA a 2026-09-25: fuerza media de la señal 0.23.

| Etapa | Número |
|---|---|
| Candidatas cribadas | 5 |
| Pasan GC1 | 3 |
| Pasan GC2 | 3 |
| Finalistas GC3 | 3 |
| Elegibles | 2 |
| En el top-3 | 2 |

**Menos de tres (R14).** Se proponen 2 opción(es) en Emergentes de Latinoamérica. Se proponen 2 opción(es): de 5 candidatas analizadas, 3 finalistas evaluadas y 2 elegibles (R14). OPP-FX-2026-0015: CLP con dirección opuesta en otro segmento sin justificación (9.6.6); sale la de menor RK → CLP con dirección opuesta en otro segmento sin justificación (9.6.6); sale la de menor RK.

##### 1. USD/COP bajista · `OPP-FX-2026-0054`

- Tipo de opción: PAR · par: USD/COP · dirección: BAJISTA_BASE · divisa de financiación: USD
- **Composición.** USD CORTO 1.00, COP LARGO 1.00 · Sube el peso colombiano y baja el dólar de EE. UU.
- **Ámbito.** Incluye: USD/COP, TRM de Colombia: tipo de cambio al contado y su rentabilidad total con carry · Excluye: Instrumentos concretos: su elección corresponde al Bloque B
- **Indicador de seguimiento.** USD/COP, TRM de Colombia (`USDCOP`, HT-01:csv)
- **Convertibilidad (PS3).** convertible no · NDF sí · controles no · profundidad media · Convertibilidad según el universo del ejecutor y las notas del Analista.
- **Carry (FX-CARRY-001).** +11.25 % anual (a favor) · diferencial base − cotizada -11.25 % · `CALC-FX-2026-1255`
- Clúster: CL-13 · confianza: probable · relevancia: ALTA · reversibilidad: baja · liquidez: media · régimen de la divisa: LIBRE_FLOTACION
- **Naturaleza de la inversión y horizonte principal (8.3).** CICLICA · **H3**
- **Siguiente paso sugerido: ENVIAR_A_BLOQUE_B**

**Tesis.** USD/COP bajista: la señal compuesta, el carry y la valoración sostienen el movimiento en los próximos meses. Sube el peso colombiano y baja el dólar de EE. UU.

**Mecanismo.** Diferencial de tipos y flujos de carry coherentes con la señal compuesta del segmento.

**Valoración.** Indicador en el percentil 0% de sus últimos tres años (ST-DESC-001).

**Puntuaciones (HT-03, `HT03-FX-2026-0013-0054`).** T 70 · E 75 · M 50 · A 65 · RK 69

| Horizonte | Vista | Banda o probabilidad | Certificado | Referencia | Medida | Pronóstico | Resolución |
|---|---|---|---|---|---|---|---|
| H2 | bajista | incierto | sin ventaja demostrada frente al paseo aleatorio | paseo aleatorio y forward | PRECIO_CONTADO en COP | `PRG-FX-2026-0251` | 2026-10-23 — Cierre HT-01 (17:00 America/New_York) de la última sesión ≤ 2026-10-23 frente al de la última sesión ≤ 2026-09-25; suceso: bajada de USDCOP (precio contado, medida en COP) entre 2026-09-25 y 2026-10-23: Sube el peso colombiano y baja el dólar de EE. UU. |
| H3 | bajista | incierto | sin ventaja demostrada frente al paseo aleatorio | paseo aleatorio y forward | PRECIO_CONTADO en COP | `PRG-FX-2026-0252` | 2027-03-25 — Cierre HT-01 (17:00 America/New_York) de la última sesión ≤ 2027-03-25 frente al de la última sesión ≤ 2026-09-25; suceso: bajada de USDCOP (precio contado, medida en COP) entre 2026-09-25 y 2027-03-25: Sube el peso colombiano y baja el dólar de EE. UU. |

**Catalizadores.** Reunión de política monetaria del banco central de la divisa (2026-10-25)

**Riesgos.** Giro de la política monetaria; Episodio de aversión al riesgo — riesgo sintético **5/5** (RISK-DD-001 v2.0).

**Invalidación.** Cierre de USDCOP por encima de 2233.9339 (nivel de invalidación, no de entrada)

**Qué cambiaría la conclusión.** Cierre de USDCOP por encima de 2233.9339 (nivel de invalidación, no de entrada); Confirmación del impulso en las próximas cuatro semanas

**Lo que no sabemos.** Si el diferencial de tipos se mantendrá tras la próxima reunión

**Encargo para el Bloque B.** Consideraciones de implementación: Liquidez máxima en el solape de las sesiones de Londres y Nueva York; Divisa no plenamente convertible: existe mercado no entregable (liquidación en otra divisa); Carry de la exposición +11.25 % anual (a favor). Carry esperado: +11.25 % anual (a favor). Niveles de referencia: nivel_actual: 2127.56 (2026-09-25, 17:00 America/New_York); invalidacion_1: 2233.93 (2026-09-25, 17:00 America/New_York). Métricas clave: Evolución del indicador de seguimiento (USDCOP); Diferencial de tipos y carry de la exposición. Preguntas: ¿Qué forma de exposición a «USD/COP bajista» ofrece mejor carry neto de costes para un inversor europeo?

**Evidencia y cálculos.** CLM-FX-2026-0381, CLM-FX-2026-0321, CLM-FX-2026-0057, CLM-FX-2026-0433 · CALC-FX-2026-1246, CALC-FX-2026-1247, CALC-FX-2026-1248, CALC-FX-2026-1249, CALC-FX-2026-1250, CALC-FX-2026-1251, CALC-FX-2026-1255, CALC-FX-2026-1282

##### 2. USD/MXN bajista · `OPP-FX-2026-0050`

- Tipo de opción: PAR · par: USD/MXN · dirección: BAJISTA_BASE · divisa de financiación: USD
- **Composición.** USD CORTO 1.00, MXN LARGO 1.00 · Sube el peso mexicano y baja el dólar de EE. UU.
- **Ámbito.** Incluye: USD/MXN, FIX de Banxico: tipo de cambio al contado y su rentabilidad total con carry · Excluye: Instrumentos concretos: su elección corresponde al Bloque B
- **Indicador de seguimiento.** USD/MXN, FIX de Banxico (`USDMXN`, HT-01:csv)
- **Convertibilidad (PS3).** convertible sí · NDF no · controles no · profundidad alta · Convertibilidad según el universo del ejecutor y las notas del Analista.
- **Carry (FX-CARRY-001).** +4.72 % anual (a favor) · diferencial base − cotizada -4.72 % · `CALC-FX-2026-1252`
- Clúster: CL-17 · confianza: probable · relevancia: ALTA · reversibilidad: alta · liquidez: alta · régimen de la divisa: LIBRE_FLOTACION
- **Naturaleza de la inversión y horizonte principal (8.3).** CICLICA · **H3**
- **Siguiente paso sugerido: ENVIAR_A_BLOQUE_B**

**Tesis.** USD/MXN bajista: la señal compuesta, el carry y la valoración sostienen el movimiento en los próximos meses. Sube el peso mexicano y baja el dólar de EE. UU.

**Mecanismo.** Diferencial de tipos y flujos de carry coherentes con la señal compuesta del segmento.

**Valoración.** Indicador en el percentil 0% de sus últimos tres años (ST-DESC-001).

**Puntuaciones (HT-03, `HT03-FX-2026-0013-0050`).** T 60 · E 75 · M 50 · A 60 · RK 65

| Horizonte | Vista | Banda o probabilidad | Certificado | Referencia | Medida | Pronóstico | Resolución |
|---|---|---|---|---|---|---|---|
| H2 | bajista | incierto | sin ventaja demostrada frente al paseo aleatorio | paseo aleatorio y forward | PRECIO_CONTADO en MXN | `PRG-FX-2026-0253` | 2026-10-23 — Cierre HT-01 (17:00 America/New_York) de la última sesión ≤ 2026-10-23 frente al de la última sesión ≤ 2026-09-25; suceso: bajada de USDMXN (precio contado, medida en MXN) entre 2026-09-25 y 2026-10-23: Sube el peso mexicano y baja el dólar de EE. UU. |
| H3 | bajista | incierto | sin ventaja demostrada frente al paseo aleatorio | paseo aleatorio y forward | PRECIO_CONTADO en MXN | `PRG-FX-2026-0254` | 2027-03-25 — Cierre HT-01 (17:00 America/New_York) de la última sesión ≤ 2027-03-25 frente al de la última sesión ≤ 2026-09-25; suceso: bajada de USDMXN (precio contado, medida en MXN) entre 2026-09-25 y 2027-03-25: Sube el peso mexicano y baja el dólar de EE. UU. |

**Catalizadores.** Reunión de política monetaria del banco central de la divisa (2026-10-25)

**Riesgos.** Giro de la política monetaria; Episodio de aversión al riesgo — riesgo sintético **4/5** (RISK-DD-001 v2.0).

**Invalidación.** Cierre de USDMXN por encima de 12.8755 (nivel de invalidación, no de entrada)

**Qué cambiaría la conclusión.** Cierre de USDMXN por encima de 12.8755 (nivel de invalidación, no de entrada); Confirmación del impulso en las próximas cuatro semanas

**Lo que no sabemos.** Si el diferencial de tipos se mantendrá tras la próxima reunión

**Encargo para el Bloque B.** Consideraciones de implementación: Liquidez máxima en el solape de las sesiones de Londres y Nueva York; Divisas convertibles para un inversor minorista europeo; liquidez máxima en las sesiones de Londres y Nueva York; Carry de la exposición +4.72 % anual (a favor). Carry esperado: +4.72 % anual (a favor). Niveles de referencia: nivel_actual: 12.2623 (2026-09-25, 17:00 America/New_York); invalidacion_1: 12.8755 (2026-09-25, 17:00 America/New_York). Métricas clave: Evolución del indicador de seguimiento (USDMXN); Diferencial de tipos y carry de la exposición. Preguntas: ¿Qué forma de exposición a «USD/MXN bajista» ofrece mejor carry neto de costes para un inversor europeo?

**Evidencia y cálculos.** CLM-FX-2026-0384, CLM-FX-2026-0385, CLM-FX-2026-0163, CLM-FX-2026-0434 · CALC-FX-2026-1246, CALC-FX-2026-1247, CALC-FX-2026-1248, CALC-FX-2026-1249, CALC-FX-2026-1250, CALC-FX-2026-1251, CALC-FX-2026-1252, CALC-FX-2026-1282

### 4.5 Emergentes de Europa, Oriente Medio y África (EMEA) — semáforo VERDE

**Régimen.** Régimen de EMEA a 2026-09-25: fuerza media de la señal 0.25.

| Etapa | Número |
|---|---|
| Candidatas cribadas | 7 |
| Pasan GC1 | 5 |
| Pasan GC2 | 4 |
| Finalistas GC3 | 4 |
| Elegibles | 2 |
| En el top-3 | 2 |

**Menos de tres (R14).** Se proponen 2 opción(es) en Emergentes de Europa, Oriente Medio y África. Se proponen 2 opción(es): de 7 candidatas analizadas, 5 finalistas evaluadas y 2 elegibles (R14). OPP-FX-2026-0047: A=60 en banda marginal sin segunda pasada independiente → Segunda pasada independiente de A y cálculo verificado. OPP-FX-2026-0020: A=60 en banda marginal sin segunda pasada independiente → Segunda pasada independiente de A y cálculo verificado. OPP-FX-2026-0038: G2 no superada; 1 objeción(es) fuerte(s) sin resolver → Superar la puerta G2; Resolver las objeciones fuertes con evidencia.

##### 1. USD/EGP bajista · `OPP-FX-2026-0019`

- Tipo de opción: REGIMEN · par: USD/EGP · dirección: BAJISTA_BASE · divisa de financiación: USD
- **Composición.** USD CORTO 1.00, EGP LARGO 1.00 · Sube la libra egipcia y baja el dólar de EE. UU.
- **Ámbito.** Incluye: USD/EGP, Banco Central de Egipto: tipo de cambio al contado y su rentabilidad total con carry · Excluye: Instrumentos concretos: su elección corresponde al Bloque B
- **Indicador de seguimiento.** USD/EGP, Banco Central de Egipto (`USDEGP`, HT-01:csv)
- **Convertibilidad (PS3).** convertible no · NDF sí · controles sí · profundidad baja · Convertibilidad según el universo del ejecutor y las notas del Analista.
- **Carry (FX-CARRY-001).** +22.00 % anual (a favor) · diferencial base − cotizada -22.00 % · `CALC-FX-2026-1269`
- Clúster: CL-14 · confianza: probable · relevancia: ALTA · reversibilidad: baja · liquidez: baja · régimen de la divisa: FLOTACION_ADMINISTRADA
- **Naturaleza de la inversión y horizonte principal (8.3).** CICLICA · **H3**
- **Siguiente paso sugerido: ENVIAR_A_BLOQUE_B**

**Tesis.** USD/EGP bajista: la señal compuesta, el carry y la valoración sostienen el movimiento en los próximos meses. Sube la libra egipcia y baja el dólar de EE. UU.

**Mecanismo.** Diferencial de tipos y flujos de carry coherentes con la señal compuesta del segmento.

**Valoración.** Indicador en el percentil 60% de sus últimos tres años (ST-DESC-001).

**Puntuaciones (HT-03, `HT03-FX-2026-0013-0019`).** T 60 · E 80 · M 50 · A 65 · RK 69

| Horizonte | Vista | Banda o probabilidad | Certificado | Referencia | Medida | Pronóstico | Resolución |
|---|---|---|---|---|---|---|---|
| H2 | bajista | más probable que no | sin ventaja demostrada frente al paseo aleatorio | paseo aleatorio y forward | PRECIO_CONTADO en EGP | `PRG-FX-2026-0200` | 2026-10-02 — Cierre HT-01 (17:00 America/New_York) de la última sesión ≤ 2026-10-02 frente al de la última sesión ≤ 2026-09-04; suceso: bajada de USDEGP (precio contado, medida en EGP) entre 2026-09-04 y 2026-10-02: Sube la libra egipcia y baja el dólar de EE. UU. |
| H3 | bajista | más probable que no | sin ventaja demostrada frente al paseo aleatorio | paseo aleatorio y forward | PRECIO_CONTADO en EGP | `PRG-FX-2026-0108` | 2027-02-07 — Cierre HT-01 (17:00 America/New_York) de la última sesión ≤ 2027-02-07 frente al de la última sesión ≤ 2026-08-07; suceso: bajada de USDEGP (precio contado, medida en EGP) entre 2026-08-07 y 2027-02-07: Sube la libra egipcia y baja el dólar de EE. UU. |

**Catalizadores.** Reunión de política monetaria del banco central de la divisa (2026-09-07)

**Riesgos.** Giro de la política monetaria; Episodio de aversión al riesgo — riesgo sintético **4/5** (RISK-DD-001 v2.0).

**Invalidación.** Cierre de USDEGP por encima de 51.271 (nivel de invalidación, no de entrada)

**Qué cambiaría la conclusión.** Cierre de USDEGP por encima de 51.271 (nivel de invalidación, no de entrada); Confirmación del impulso en las próximas cuatro semanas

**Lo que no sabemos.** Si el diferencial de tipos se mantendrá tras la próxima reunión

**Encargo para el Bloque B.** Consideraciones de implementación: Liquidez máxima en el solape de las sesiones de Londres y Nueva York; Divisa no plenamente convertible: existe mercado no entregable (liquidación en otra divisa); Controles de capitales vigentes: posibles límites a la repatriación; Carry de la exposición +22.00 % anual (a favor). Carry esperado: +22.00 % anual (a favor). Niveles de referencia: nivel_actual: 47.739 (2026-09-25, 17:00 America/New_York); invalidacion_1: 51.271 (2026-09-25, 17:00 America/New_York). Métricas clave: Evolución del indicador de seguimiento (USDEGP); Diferencial de tipos y carry de la exposición. Preguntas: ¿Qué forma de exposición a «USD/EGP bajista» ofrece mejor carry neto de costes para un inversor europeo?

**Evidencia y cálculos.** CLM-FX-2026-0171, CLM-FX-2026-0078, CLM-FX-2026-0079, CLM-FX-2026-0227 · CALC-FX-2026-1257, CALC-FX-2026-1258, CALC-FX-2026-1259, CALC-FX-2026-1260, CALC-FX-2026-1261, CALC-FX-2026-1262, CALC-FX-2026-1269, CALC-FX-2026-1282

##### 2. USD/ZAR alcista · `OPP-FX-2026-0037`

- Tipo de opción: PAR · par: USD/ZAR · dirección: ALCISTA_BASE · divisa de financiación: ZAR
- **Composición.** USD LARGO 1.00, ZAR CORTO 1.00 · Sube el dólar de EE. UU. y baja el rand sudafricano.
- **Ámbito.** Incluye: USD/ZAR, fixing WM/Reuters: tipo de cambio al contado y su rentabilidad total con carry · Excluye: Instrumentos concretos: su elección corresponde al Bloque B
- **Indicador de seguimiento.** USD/ZAR, fixing WM/Reuters (`USDZAR`, HT-01:csv)
- **Convertibilidad (PS3).** convertible sí · NDF no · controles no · profundidad alta · Convertibilidad según el universo del ejecutor y las notas del Analista.
- **Carry (FX-CARRY-001).** -4.03 % anual (en contra) · diferencial base − cotizada -4.03 % · `CALC-FX-2026-1267`
- Clúster: CL-21 · confianza: probable · relevancia: MEDIA · reversibilidad: alta · liquidez: alta · régimen de la divisa: LIBRE_FLOTACION
- **Naturaleza de la inversión y horizonte principal (8.3).** CICLICA · **H3**
- **Siguiente paso sugerido: ENVIAR_A_BLOQUE_B**

**Tesis.** USD/ZAR alcista: la señal compuesta, el carry y la valoración sostienen el movimiento en los próximos meses. Sube el dólar de EE. UU. y baja el rand sudafricano.

**Mecanismo.** Diferencial de tipos y flujos de carry coherentes con la señal compuesta del segmento.

**Valoración.** Indicador en el percentil 75% de sus últimos tres años (ST-DESC-001).

**Puntuaciones (HT-03, `HT03-FX-2026-0013-0037`).** T 60 · E 80 · M 50 · A 55 · RK 65

| Horizonte | Vista | Banda o probabilidad | Certificado | Referencia | Medida | Pronóstico | Resolución |
|---|---|---|---|---|---|---|---|
| H2 | alcista | incierto | sin ventaja demostrada frente al paseo aleatorio | paseo aleatorio y forward | PRECIO_CONTADO en ZAR | `PRG-FX-2026-0255` | 2026-10-23 — Cierre HT-01 (17:00 America/New_York) de la última sesión ≤ 2026-10-23 frente al de la última sesión ≤ 2026-09-25; suceso: subida de USDZAR (precio contado, medida en ZAR) entre 2026-09-25 y 2026-10-23: Sube el dólar de EE. UU. y baja el rand sudafricano. |
| H3 | alcista | incierto | sin ventaja demostrada frente al paseo aleatorio | paseo aleatorio y forward | PRECIO_CONTADO en ZAR | `PRG-FX-2026-0256` | 2027-03-25 — Cierre HT-01 (17:00 America/New_York) de la última sesión ≤ 2027-03-25 frente al de la última sesión ≤ 2026-09-25; suceso: subida de USDZAR (precio contado, medida en ZAR) entre 2026-09-25 y 2027-03-25: Sube el dólar de EE. UU. y baja el rand sudafricano. |

**Catalizadores.** Reunión de política monetaria del banco central de la divisa (2026-10-25)

**Riesgos.** Giro de la política monetaria; Episodio de aversión al riesgo — riesgo sintético **2/5** (RISK-DD-001 v2.0).

**Invalidación.** Cierre de USDZAR por debajo de 19.1165 (nivel de invalidación, no de entrada)

**Qué cambiaría la conclusión.** Cierre de USDZAR por debajo de 19.1165 (nivel de invalidación, no de entrada); Confirmación del impulso en las próximas cuatro semanas

**Lo que no sabemos.** Si el diferencial de tipos se mantendrá tras la próxima reunión

**Encargo para el Bloque B.** Consideraciones de implementación: Liquidez máxima en el solape de las sesiones de Londres y Nueva York; Divisas convertibles para un inversor minorista europeo; liquidez máxima en las sesiones de Londres y Nueva York; Carry de la exposición -4.03 % anual (en contra). Carry esperado: -4.03 % anual (en contra). Niveles de referencia: nivel_actual: 20.1226 (2026-09-25, 17:00 America/New_York); invalidacion_1: 19.1165 (2026-09-25, 17:00 America/New_York). Métricas clave: Evolución del indicador de seguimiento (USDZAR); Diferencial de tipos y carry de la exposición. Preguntas: ¿Qué forma de exposición a «USD/ZAR alcista» ofrece mejor carry neto de costes para un inversor europeo?

**Evidencia y cálculos.** CLM-FX-2026-0437, CLM-FX-2026-0324, CLM-FX-2026-0075, CLM-FX-2026-0438 · CALC-FX-2026-1257, CALC-FX-2026-1258, CALC-FX-2026-1259, CALC-FX-2026-1260, CALC-FX-2026-1261, CALC-FX-2026-1262, CALC-FX-2026-1267, CALC-FX-2026-1282

### 4.6 Estrategias y cestas cambiarias (ESTR) — semáforo VERDE

**Régimen.** Régimen de ESTR a 2026-09-25: fuerza media de la señal 0.35.

| Etapa | Número |
|---|---|
| Candidatas cribadas | 0 |
| Pasan GC1 | 0 |
| Pasan GC2 | 0 |
| Finalistas GC3 | 0 |
| Elegibles | 2 |
| En el top-3 | 2 |

**Menos de tres (R14).** Se proponen 2 opción(es) en Estrategias y cestas cambiarias. Se proponen 2 opción(es): de 2 candidatas analizadas, 2 finalistas evaluadas y 2 elegibles (R14).

##### 1. Divisas latinoamericanas frente al USD · `OPP-FX-2026-0022`

- Tipo de opción: CESTA · par: — · dirección: — · divisa de financiación: USD
- **Composición.** BRL LARGO 0.25, MXN LARGO 0.25, CLP LARGO 0.25, COP LARGO 0.25, USD CORTO 1.00 · Suben el real brasileño, el peso mexicano y el peso chileno y baja el dólar de EE. UU.
- **Ámbito.** Incluye: Índice de la cesta latinoamericana frente al USD (propio): tipo de cambio al contado y su rentabilidad total con carry · Excluye: Instrumentos concretos: su elección corresponde al Bloque B
- **Indicador de seguimiento.** Índice de la cesta latinoamericana frente al USD (propio) (`CESTA-LATAM`, HT-01:csv)
- **Convertibilidad (PS3).** convertible no · NDF sí · controles no · profundidad media · Convertibilidad según el universo del ejecutor y las notas del Analista.
- **Carry (FX-CARRY-001).** +5.15 % anual (a favor) · `CALC-FX-2026-1281`
- Clúster: CL-3 · confianza: probable · relevancia: ALTA · reversibilidad: baja · liquidez: media · régimen de la divisa: LIBRE_FLOTACION
- **Naturaleza de la inversión y horizonte principal (8.3).** CICLICA · **H3**
- **Siguiente paso sugerido: ENVIAR_A_BLOQUE_B**

**Tesis.** Divisas latinoamericanas frente al USD: la señal compuesta, el carry y la valoración sostienen el movimiento en los próximos meses. Suben el real brasileño, el peso mexicano y el peso chileno y baja el dólar de EE. UU.

**Mecanismo.** Diferencial de tipos y flujos de carry coherentes con la señal compuesta del segmento.

**Valoración.** Indicador en el percentil 66% de sus últimos tres años (ST-DESC-001).

**Puntuaciones (HT-03, `HT03-FX-2026-0013-0022`).** T 80 · E 75 · M 50 · A 70 · RK 74

| Horizonte | Vista | Banda o probabilidad | Certificado | Referencia | Medida | Pronóstico | Resolución |
|---|---|---|---|---|---|---|---|
| H2 | alcista | incierto | sin ventaja demostrada frente al paseo aleatorio | rentabilidad nula | PRECIO_CONTADO en USD | `PRG-FX-2026-0230` | 2026-10-09 — Cierre HT-01 (17:00 America/New_York) de la última sesión ≤ 2026-10-09 frente al de la última sesión ≤ 2026-09-11; suceso: subida de CESTA-LATAM (precio contado, medida en USD) entre 2026-09-11 y 2026-10-09: Suben el real brasileño, el peso mexicano y el peso chileno y baja el dólar de EE. UU. |
| H3 | alcista | incierto | sin ventaja demostrada frente al paseo aleatorio | rentabilidad nula | PRECIO_CONTADO en USD | `PRG-FX-2026-0231` | 2027-03-11 — Cierre HT-01 (17:00 America/New_York) de la última sesión ≤ 2027-03-11 frente al de la última sesión ≤ 2026-09-11; suceso: subida de CESTA-LATAM (precio contado, medida en USD) entre 2026-09-11 y 2027-03-11: Suben el real brasileño, el peso mexicano y el peso chileno y baja el dólar de EE. UU. |

**Catalizadores.** Reunión de política monetaria del banco central de la divisa (2026-10-11)

**Riesgos.** Giro de la política monetaria; Episodio de aversión al riesgo — riesgo sintético **4/5** (RISK-DD-001 v2.0).

**Invalidación.** Cierre de CESTA-LATAM por debajo de 109.9333 (nivel de invalidación, no de entrada)

**Qué cambiaría la conclusión.** Cierre de CESTA-LATAM por debajo de 109.9333 (nivel de invalidación, no de entrada); Confirmación del impulso en las próximas cuatro semanas

**Lo que no sabemos.** Si el diferencial de tipos se mantendrá tras la próxima reunión

**Encargo para el Bloque B.** Consideraciones de implementación: Liquidez máxima en el solape de las sesiones de Londres y Nueva York; Divisa no plenamente convertible: existe mercado no entregable (liquidación en otra divisa); Carry de la exposición +5.15 % anual (a favor). Carry esperado: +5.15 % anual (a favor). Niveles de referencia: nivel_actual: 116.132 (2026-09-25, 17:00 America/New_York); invalidacion_1: 109.933 (2026-09-25, 17:00 America/New_York). Métricas clave: Evolución del indicador de seguimiento (CESTA-LATAM); Diferencial de tipos y carry de la exposición. Preguntas: ¿Qué forma de exposición a «Divisas latinoamericanas frente al USD» ofrece mejor carry neto de costes para un inversor europeo?

**Evidencia y cálculos.** CLM-FX-2026-0258, CLM-FX-2026-0332, CLM-FX-2026-0093, CLM-FX-2026-0396 · CALC-FX-2026-1270, CALC-FX-2026-1271, CALC-FX-2026-1272, CALC-FX-2026-1273, CALC-FX-2026-1274, CALC-FX-2026-1275, CALC-FX-2026-1281, CALC-FX-2026-1282

##### 2. Momentum G10 frente al USD (posición invertida) · `OPP-FX-2026-0039`

- Tipo de opción: ESTRATEGIA · par: — · dirección: — · divisa de financiación: AUD
- **Composición.** EUR CORTO 0.25, GBP CORTO 0.25, AUD CORTO 0.25, CAD CORTO 0.25, USD LARGO 1.00 · Sube el dólar de EE. UU. y bajan el euro, la libra esterlina y el dólar australiano.
- **Ámbito.** Incluye: Índice de momentum G10 (exceso de rentabilidad, propio): tipo de cambio al contado y su rentabilidad total con carry · Excluye: Instrumentos concretos: su elección corresponde al Bloque B
- **Indicador de seguimiento.** Índice de momentum G10 (exceso de rentabilidad, propio) (`FX-MOM-G10`, HT-01:csv)
- **Convertibilidad (PS3).** convertible sí · NDF no · controles no · profundidad alta · Convertibilidad según el universo del ejecutor y las notas del Analista.
- **Carry (FX-CARRY-001).** -0.99 % anual (en contra) · `CALC-FX-2026-1278`
- Clúster: CL-7 · confianza: probable · relevancia: BAJA · reversibilidad: alta · liquidez: alta · régimen de la divisa: LIBRE_FLOTACION
- **Naturaleza de la inversión y horizonte principal (8.3).** PRIMA_RIESGO · **H3**
- **Siguiente paso sugerido: ENVIAR_A_BLOQUE_B**

**Tesis.** Momentum G10 frente al USD (posición invertida): la señal compuesta, el carry y la valoración sostienen el movimiento en los próximos meses. Sube el dólar de EE. UU. y bajan el euro, la libra esterlina y el dólar australiano.

**Mecanismo.** Diferencial de tipos y flujos de carry coherentes con la señal compuesta del segmento.

**Valoración.** Indicador en el percentil 39% de sus últimos tres años (ST-DESC-001).

**Puntuaciones (HT-03, `HT03-FX-2026-0013-0039`).** T 60 · E 75 · M 50 · A 60 · RK 65

| Horizonte | Vista | Banda o probabilidad | Certificado | Referencia | Medida | Pronóstico | Resolución |
|---|---|---|---|---|---|---|---|
| H2 | bajista | incierto | sin ventaja demostrada frente al paseo aleatorio | rentabilidad nula | RENTABILIDAD_TOTAL en AUD | `PRG-FX-2026-0232` | 2026-10-09 — Cierre HT-01 (17:00 America/New_York) de la última sesión ≤ 2026-10-09 frente al de la última sesión ≤ 2026-09-11; suceso: bajada de FX-MOM-G10 (rentabilidad total, medida en AUD) entre 2026-09-11 y 2026-10-09: Sube el dólar de EE. UU. y bajan el euro, la libra esterlina y el dólar australiano. |
| H3 | bajista | incierto | sin ventaja demostrada frente al paseo aleatorio | rentabilidad nula | RENTABILIDAD_TOTAL en AUD | `PRG-FX-2026-0135` | 2027-02-14 — Cierre HT-01 (17:00 America/New_York) de la última sesión ≤ 2027-02-14 frente al de la última sesión ≤ 2026-08-14; suceso: bajada de FX-MOM-G10 (rentabilidad total, medida en AUD) entre 2026-08-14 y 2027-02-14: Sube el dólar de EE. UU. y bajan el euro, la libra esterlina y el dólar australiano. |

**Catalizadores.** Reunión de política monetaria del banco central de la divisa (2026-09-14)

**Riesgos.** Giro de la política monetaria; Episodio de aversión al riesgo — riesgo sintético **2/5** (RISK-DD-001 v2.0).

**Invalidación.** Cierre de FX-MOM-G10 por encima de 106.6234 (nivel de invalidación, no de entrada)

**Qué cambiaría la conclusión.** Cierre de FX-MOM-G10 por encima de 106.6234 (nivel de invalidación, no de entrada); Confirmación del impulso en las próximas cuatro semanas

**Lo que no sabemos.** Si el diferencial de tipos se mantendrá tras la próxima reunión

**Encargo para el Bloque B.** Consideraciones de implementación: Liquidez máxima en el solape de las sesiones de Londres y Nueva York; Divisas convertibles para un inversor minorista europeo; liquidez máxima en las sesiones de Londres y Nueva York; Carry de la exposición -0.99 % anual (en contra). Carry esperado: -0.99 % anual (en contra). Niveles de referencia: nivel_actual: 99.9002 (2026-09-25, 17:00 America/New_York); invalidacion_1: 106.623 (2026-09-25, 17:00 America/New_York). Métricas clave: Evolución del indicador de seguimiento (FX-MOM-G10); Diferencial de tipos y carry de la exposición. Preguntas: ¿Qué forma de exposición a «Momentum G10 frente al USD (posición invertida)» ofrece mejor carry neto de costes para un inversor europeo?

**Evidencia y cálculos.** CLM-FX-2026-0263, CLM-FX-2026-0264, CLM-FX-2026-0265, CLM-FX-2026-0266 · CALC-FX-2026-1270, CALC-FX-2026-1271, CALC-FX-2026-1272, CALC-FX-2026-1273, CALC-FX-2026-1274, CALC-FX-2026-1275, CALC-FX-2026-1278, CALC-FX-2026-1282

## 5. Seguimiento de opciones vigentes

| OPP | Estado | Decisión del Broker | Comentario |
|---|---|---|---|
| `OPP-FX-2026-0002` | VIGENTE  | — | Se mantiene en el top-3 (continuidad 9.6.4) |
| `OPP-FX-2026-0003` | VIGENTE  | — | Se mantiene en el top-3 (continuidad 9.6.4) |
| `OPP-FX-2026-0004` | VIGENTE  | — | Se mantiene en el top-3 (continuidad 9.6.4) |
| `OPP-FX-2026-0036` | VIGENTE  | — | Se mantiene en el top-3 (continuidad 9.6.4) |
| `OPP-FX-2026-0043` | CERRADA SUSTITUCION | — | Sale del top-3: sustituida o ya no elegible |
| `OPP-FX-2026-0045` | VIGENTE  | — | Se mantiene en el top-3 (continuidad 9.6.4) |
| `OPP-FX-2026-0012` | VIGENTE  | — | Se mantiene en el top-3 (continuidad 9.6.4) |
| `OPP-FX-2026-0025` | VIGENTE  | — | Se mantiene en el top-3 (continuidad 9.6.4) |
| `OPP-FX-2026-0016` | CERRADA INVALIDACION | — | Condición de invalidación cumplida |
| `OPP-FX-2026-0050` | VIGENTE  | — | Se mantiene en el top-3 (continuidad 9.6.4) |
| `OPP-FX-2026-0019` | VIGENTE  | — | Se mantiene en el top-3 (continuidad 9.6.4) |
| `OPP-FX-2026-0038` | CERRADA SUSTITUCION | — | Sale del top-3: sustituida o ya no elegible |
| `OPP-FX-2026-0047` | CERRADA SUSTITUCION | — | Sale del top-3: sustituida o ya no elegible |
| `OPP-FX-2026-0022` | VIGENTE  | — | Se mantiene en el top-3 (continuidad 9.6.4) |
| `OPP-FX-2026-0039` | VIGENTE  | — | Se mantiene en el top-3 (continuidad 9.6.4) |

## 6. Objeciones y respuestas

| OPP | Fuerza | Objeción | Respuesta | Estado |
|---|---|---|---|---|
| `OPP-FX-2026-0003` | moderada | El forward ya descuenta parte del movimiento y el carry puede deshacerse de golpe. | Respondida con los datos HT-01, el carry y los cálculos CALC-FX- del segmento. | RESPONDIDA |
| `OPP-FX-2026-0002` | moderada | El forward ya descuenta parte del movimiento y el carry puede deshacerse de golpe. | Respondida con los datos HT-01, el carry y los cálculos CALC-FX- del segmento. | RESPONDIDA |
| `OPP-FX-2026-0004` | moderada | El forward ya descuenta parte del movimiento y el carry puede deshacerse de golpe. | Respondida con los datos HT-01, el carry y los cálculos CALC-FX- del segmento. | RESPONDIDA |
| `OPP-FX-2026-0045` | moderada | El forward ya descuenta parte del movimiento y el carry puede deshacerse de golpe. | Respondida con los datos HT-01, el carry y los cálculos CALC-FX- del segmento. | RESPONDIDA |
| `OPP-FX-2026-0007` | moderada | El forward ya descuenta parte del movimiento y el carry puede deshacerse de golpe. | Respondida con los datos HT-01, el carry y los cálculos CALC-FX- del segmento. | RESPONDIDA |
| `OPP-FX-2026-0036` | moderada | El forward ya descuenta parte del movimiento y el carry puede deshacerse de golpe. | Respondida con los datos HT-01, el carry y los cálculos CALC-FX- del segmento. | RESPONDIDA |
| `OPP-FX-2026-0012` | moderada | El forward ya descuenta parte del movimiento y el carry puede deshacerse de golpe. | Respondida con los datos HT-01, el carry y los cálculos CALC-FX- del segmento. | RESPONDIDA |
| `OPP-FX-2026-0025` | moderada | El forward ya descuenta parte del movimiento y el carry puede deshacerse de golpe. | Respondida con los datos HT-01, el carry y los cálculos CALC-FX- del segmento. | RESPONDIDA |
| `OPP-FX-2026-0054` | moderada | El forward ya descuenta parte del movimiento y el carry puede deshacerse de golpe. | Respondida con los datos HT-01, el carry y los cálculos CALC-FX- del segmento. | RESPONDIDA |
| `OPP-FX-2026-0050` | moderada | El forward ya descuenta parte del movimiento y el carry puede deshacerse de golpe. | Respondida con los datos HT-01, el carry y los cálculos CALC-FX- del segmento. | RESPONDIDA |
| `OPP-FX-2026-0019` | moderada | El forward ya descuenta parte del movimiento y el carry puede deshacerse de golpe. | Respondida con los datos HT-01, el carry y los cálculos CALC-FX- del segmento. | RESPONDIDA |
| `OPP-FX-2026-0037` | moderada | El forward ya descuenta parte del movimiento y el carry puede deshacerse de golpe. | Respondida con los datos HT-01, el carry y los cálculos CALC-FX- del segmento. | RESPONDIDA |
| `OPP-FX-2026-0022` | moderada | El forward ya descuenta parte del movimiento y el carry puede deshacerse de golpe. | Respondida con los datos HT-01, el carry y los cálculos CALC-FX- del segmento. | RESPONDIDA |
| `OPP-FX-2026-0039` | moderada | El forward ya descuenta parte del movimiento y el carry puede deshacerse de golpe. | Respondida con los datos HT-01, el carry y los cálculos CALC-FX- del segmento. | RESPONDIDA |

## 7. Limitaciones, lagunas y qué no sabemos

- Datos sintéticos o de proveedor sin posicionamiento ni volatilidad implícita
- Backtest: búsqueda web desactivada; evidencia limitada a datos HT-01 y referencias anteriores a la fecha as_of; riesgo de fuga por conocimiento del modelo

## 8. Historial de aciertos (Evaluador)

Ventana: **12 semanas**. Referencia: paseo aleatorio y forward. Ventana de 12 semanas; 70 pronósticos de opciones publicadas resueltos

| Ámbito | n | Aciertos | Tasa | Paseo aleatorio | Forward | Significativo |
|---|---|---|---|---|---|---|
| Global | 70 | 27 | 0.3857 | 0.5 | 0.5 | False |
| G10N | 11 | 2 | 0.1818 | 0.5 | 0.8182 | False |
| G10M | 14 | 10 | 0.7143 | 0.5 | 0.6429 | False |
| EMAS | 8 | 1 | 0.125 | 0.5 | 0.625 | False |
| EMLA | 12 | 7 | 0.5833 | 0.5 | 0.0833 | False |
| EMEA | 13 | 2 | 0.1538 | 0.5 | 0.2308 | False |
| ESTR | 12 | 5 | 0.4167 | 0.5 | 0.6667 | False |

## 9. Preguntas sugeridas

- ¿Qué opciones comparten el mismo factor de riesgo?
- ¿Qué haría cambiar el semáforo de cada segmento?

*Este informe describe oportunidades generales del mercado de divisas y no constituye asesoramiento personalizado; el Broker Personal valora si encaja con el usuario. El instrumento, el coste, la cobertura y la ejecución los analiza el Bloque B.*
