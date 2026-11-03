# Esquema de archivo operativo — F6 Memoria de aprendizaje

**Bloque A Forex · Robot Investor · Versión V1.0 · 02/11/2026** · Subordinado al Documento 0 del Bloque A Forex, versión óptima V1.0.

---

## 1. Propósito

F6 es la memoria de lo que el Bloque A Forex **ha aprendido de forma verificable** (sección 12 del Documento 0): resultados de la resolución de pronósticos, métricas de acierto y calibración por celda **segmento × horizonte** medidas siempre **frente al paseo aleatorio** y, cuando procede, frente al **forward como predictor**, certificados de horizonte, lecciones LEC-, fiabilidad de fuentes de opinión (incluidas las previsiones de pares de bancos y casas de análisis), rendimiento de las estrategias cambiarias (carry, valor, momentum, dólar amplio), ajustes aplicados y propuestos, evaluaciones sombra, historial de aciertos publicable y asignación exploratoria. Cada agente lee al inicio de cada encargo el extracto de su ámbito (máximo 10 lecciones, las de mayor fuerza) y la sección «Novedades»: así el aprendizaje entra en el contexto sin engordar los prompts.

## 2. Propietario, lectores y contratos

| Aspecto | Contenido |
|---|---|
| Propietario de escritura | AG-20 Evaluador de Previsiones y Aprendizaje (único) |
| Lectores | Todos (extracto por ámbito vía HT-06) |
| Contratos | CT-19 (difusión de su contenido), CT-22 (entradas de producto), CT-09/CT-10 (cálculos que sostienen métricas y decisiones) |
| Consumidores clave | Analizador (historial de aciertos para CT-15, certificados), Prospectiva (calibración, certificados), Analistas de segmento y transversales (lecciones de su ámbito), HT-09 (certificados para G3-CON-10), Buscador (fiabilidad de fuentes), Orquestador (lecciones de nivel A) |

## 3. Reglas

1. **Append-only**: métricas, certificados, lecciones y ajustes son entradas nuevas; los estados cambian por entradas nuevas; nada se borra.
2. **Toda cifra publicada** procede de un CALC- del Motor o de un recuento reproducible sobre F4/F5 (R7).
3. **Sin fuga**: cada métrica declara `comprobacion_fuga`, incluida la verificación de que las fijaciones, los datos de posicionamiento y los vintages usados eran conocibles en la fecha de congelación.
4. **Referencias obligatorias**: toda métrica de habilidad se calcula frente al **paseo aleatorio**; las de rentabilidad total, también frente al **forward**; las de estrategias (ESTR), frente a la rentabilidad nula o el índice de la estrategia; las de rentabilidad relativa, frente a la referencia del segmento (8.4). Para comparar modelos anidados con el paseo aleatorio se usa Clark-West; para no anidados, Diebold-Mariano con corrección HLN.
5. **Celdas**: nivel 1 segmento × horizonte; nivel 2 + método (certificación); nivel 3 + estrategia, tipo de opción, tipo de rentabilidad y fuente (diagnóstico, con contracción).
6. **Muestras**: sin ≥ 30 resueltos en la celda de nivel 1, ninguna recalibración; sin ≥ 100 en la de nivel 2, ningún certificado (Anexo A). Un backtest del Motor informa pero **no sustituye** a los pronósticos congelados para certificar.
7. **Lecciones**: máximo 10 vigentes por ámbito en el extracto de lectura; caducidad obligatoria.
8. **Novedades**: sección semanal con altas, revocaciones, ajustes y lecciones nuevas, enlazadas por identificador.

## 4. Formato de entrada

### 4.1 Lote de resolución (RES-)

`res_id` (`RES-AAAA-MM-DD`), `fecha`, `prg_resueltos` (lista), `prg_no_resolubles` (lista con motivo), `fijaciones_usadas` (fuente, hora, zona por par), `fallbacks_aplicados`, `calc_id`, `comprobacion_fuga`.

### 4.2 Métricas por celda (MET-)

| Campo | Tipo | Valores / formato |
|---|---|---|
| `met_id` | Identificador | `MET-AAAA-MM` (o `-Wss` si semanal) + celda |
| `celda` | Objeto | `{nivel 1·2·3, segmento, horizonte, metodo, estrategia, tipo_opcion, tipo_rentabilidad, fuente}` |
| `ventana` | Texto | Fechas de congelación incluidas |
| `n` / `n_eff` | Enteros | `n_eff` corrige el solapamiento de horizontes y la correlación entre pares del mismo clúster |
| `acierto` | Objeto | `{tasa, ic90_wilson, pesaran_timmermann_p}` |
| `brier` / `log` / `rps` | Números | — |
| `murphy` | Objeto | `{rel, res, unc, bins}` |
| `bss` | Objeto | `{valor, ic90, referencia PASEO_ALEATORIO·FORWARD·RENTABILIDAD_NULA·INDICE_ESTRATEGIA, metodo_bootstrap BLOQUES·CONGLOMERADOS, replicas}` (uno por referencia) |
| `error_relativo` | Objeto | `{rmse_vs_paseo_aleatorio, u_theil, mae_vs_forward}` en pronósticos de nivel o rango |
| `ece` / `mce` | Números | Con número de bins |
| `calibracion_global` | Objeto | `{p_media, frecuencia, pendiente, ic_pendiente}` |
| `pruebas` | Objeto | `{dm_hln {estadistico, p_valor, h, referencia}, clark_west {estadistico, p_valor, referencia}}` |
| `rentabilidad` | Objeto | `{total_relativa_media, contado_media, carry_medio, ir, sharpe, sortino, drawdown_max, referencia_segmento}` |
| `riesgo_cola_carry` | Objeto | `{frecuencia_superacion_adverso, frecuencia_nominal, n}` |
| `seleccion` | Objeto | `{falsos_positivos, falsos_negativos, ic_spearman_rk, precision_at_3}` |
| `calc_ids` | Lista | CALC- |
| `comprobacion_fuga` | Enumerado | SUPERADA · FALLIDA |
| `madurez` | Enumerado | documentado · implementado · validado |

### 4.3 Certificado (CERT-)

`cert_id` (`CERT-AAAA-NNNN`), `celda` `{segmento, horizonte, metodo, tipo_pronostico opcional}`, `ventana`, `n`, `n_eff`, `brier`, `brier_paseo_aleatorio`, `bss_vs_paseo_aleatorio`, `bss_ic90`, `holm_superado`, `ece`, `ece_p90_simulado`, `bins`, `curva_fiabilidad` (CALC-), `reejecucion` (CALC- de CT-10), `methodology_version`, `emitido`, `revision`, `estado`, `motivo_cambio`. Criterio (Anexo A, nota 1): n ≥ 100 con Holm; extremo inferior del IC 90 % del BSS frente al **paseo aleatorio** > 0; ECE ≤ percentil 90 del ECE simulado bajo calibración perfecta (Bröcker y Smith, 2007) y < 0,15.

### 4.4 Lección (LEC-)

| Campo | Tipo | Valores / formato |
|---|---|---|
| `lec_id` | Identificador | `LEC-AAAA-NNNN` |
| `fecha` | Fecha | ISO 8601 |
| `ambito` | Objeto | `{segmento, divisa, horizonte, agente[], fuente, metodo, estrategia}` |
| `nivel` | Enumerado | A (operativo) · B (predictivo) · C (metodológico, solo como antecedente de tipo 3) |
| `tipo` | Enumerado | PREDICTIVA · OPERATIVA · PRODUCTO · FUENTE · CALIBRACION |
| `observacion` | Texto | Factual, con cifras y referencia (paseo aleatorio, forward) |
| `evidencia` | Lista | CALC-, MET-, PRG-FX-, RUN-FX-, QRY-, HAL- |
| `recomendacion` | Texto | Operativa (qué hacer distinto y en qué fase) |
| `fuerza` | Enumerado | anecdotica · recurrente · estadistica |
| `n` / `efecto` | Entero / texto | Tamaño y magnitud con IC |
| `caducidad` | Fecha | 3, 6 o 12 meses según fuerza |
| `estado` | Enumerado | Sección 5 |
| `sustituye` | Identificador | LEC- anterior |

### 4.5 Fiabilidad de fuente (FUE-)

`fue_id`, `ref_id` (ficha de F9), `periodo`, `n`, `aciertos`, `bss_vs_paseo_aleatorio`, `bss_contraido` (k = 20), `puntos_historial` (0–20; neutro 10), `pares_cubiertos`, `calc_id`, `comunicado_ct19` (msg_id).

### 4.6 Ajuste (AJU-) y evaluación sombra

`aju_id` (`AJU-AAAA-NNNN`), `parametro` (identificador de F10), `de`, `a`, `banda` `{trimestral, total}`, `acumulado_vs_inicial`, `evidencia` `{objetivo, mejora_fuera_muestra, ic90, calc, reejecucion}`, `methodology_version` (de → a; p. ej., FX-1.0 → FX-1.1), `efecto_desde`, `sombra_hasta`, `estado`, `resultado_sombra` `{metrica_nueva, metrica_anterior, dm_hln_p, decisiones_top3_cambiadas, decision CONFIRMADO·REVERTIDO}`.

### 4.7 Propuesta de tipo 3 (P3-EVAL-)

`p3_id`, `objeto`, `motivo` (fuera de banda · sin banda · cambio hacia o desde «No» · nuevo método · nueva estrategia de segmento · otro), `evidencia`, `impacto_esperado`, `pruebas_regresion` (IDs del Plan de pruebas del Bloque A Forex), `plan_reversion`, `elevada_via` (msg_id CT-19 al Orquestador), `estado` (ENVIADA · APROBADA · RECHAZADA · APLICADA, según comunique el Orquestador).

### 4.8 Historial de aciertos publicable (HAC-)

Estructura idéntica a `historial_aciertos` del paquete de oportunidades: `ventana`, `referencia` ("paseo aleatorio"), `global` y `por_segmento` con `n`, `aciertos`, `tasa_acierto`, `tasa_esperada_azar` (la del paseo aleatorio, calculada sin fuga), `significativo`, `por_horizonte`; más `nota`, `no_resolubles_excluidos`, `calc_id`, `publicado` (fecha-hora).

### 4.9 Producto (PRO-) y asignación exploratoria (BAN-)

- `PRO-`: `tema`, `qry_ids`, `veces_4_semanas`, `utilidad` `{mediana, distribucion, tendencia}`, `decisiones_broker` `{enviadas_vs_descartadas: rentabilidad total relativa media de cada grupo, n}`, `lec_id` generada.
- `BAN-`: `periodo`, `segmento`, `brazos` `{celda_exploracion (divisa, par o estrategia), alfa, beta, prob_mejor, asignacion}`, `gamma`, `suelo`, `techo`, `recompensas` (tempranas y diferidas), `propensiones`.

## 5. Estados y transiciones

| Objeto | Transiciones |
|---|---|
| CERT- | `VIGENTE` → `EN_OBSERVACION` → `VIGENTE` · `REVOCADO`; `VIGENTE` → `REVOCADO` (BSS frente al paseo aleatorio ≤ 0 en ventana, ECE ≥ 0,17, fuga, cambio de método o de versión mayor de metodología) |
| LEC- | `VIGENTE` → `REVISADA` (sustituida) · `CADUCADA` · `REFUTADA` |
| AJU- | `PROPUESTO` → `EN_SOMBRA` → `CONFIRMADO` · `REVERTIDO` |
| P3-EVAL- | `ENVIADA` → `APROBADA` → `APLICADA` · `RECHAZADA` |

## 6. Índices de consulta

| Índice | Clave | Uso |
|---|---|---|
| Lecciones por ámbito | `ambito.segmento`, `ambito.divisa`, `ambito.agente`, `fuerza`, `estado` = VIGENTE | Lectura al inicio de cada encargo (máx. 10) |
| Certificados vigentes | `celda`, `estado` | Prospectiva, Analizador, HT-09 (G3-CON-10) |
| Métricas por celda | `celda`, `ventana` | Informes CT-19; revisión trimestral |
| Rendimiento por estrategia | `celda.estrategia` | Analista ESTR; revisión trimestral |
| Historial de aciertos vigente | último HAC- | Paquete de síntesis CT-15 |
| Fiabilidad por fuente | `ref_id` | Q de F9 |
| Ajustes en sombra | `estado` = EN_SOMBRA, `sombra_hasta` | Cierre trimestral |
| Novedades | Semana | Difusión sin canal nuevo |

## 7. Ejemplo ficticio

> **EJEMPLO FICTICIO — no es una entrada real.**

```json
{"lec_id":"LEC-FX-2026-0001","fecha":"2026-11-30","ambito":{"segmento":"EMLA","divisa":null,"horizonte":"H2","agente":["AG-06","AG-10"],"fuente":null,"metodo":"carry ajustado por volatilidad","estrategia":"EMLA-CARRY-AJUSTADO"},
 "nivel":"B","tipo":"PREDICTIVA","observacion":"PRG DIRECCIONAL H2 basados solo en carry en pares de EMLA: acierto direccional 47 % (n = 38); BSS frente al paseo aleatorio −0,04 (IC 90 %: −0,12; 0,03)",
 "evidencia":["MET-2026-11-EMLA-H2","CALC-FX-2026-0298"],"recomendacion":"En H2 para EMLA, no superar la banda «incierto» con señal solo de carry; exigir confirmación de momentum o de posicionamiento no extremo (informe PFV)",
 "fuerza":"recurrente","n":38,"efecto":"−0,05 (IC 90 %: −0,16; 0,06)","caducidad":"2027-05-31","estado":"VIGENTE","sustituye":null}
```
