# Esquema de archivo operativo — F6 Memoria de aprendizaje

**Bloque A · Robot Investor · Versión óptima V4.0 · 01/11/2026** · Subordinado al Documento 0 óptima V5.0.

---

## 1. Propósito

F6 es la memoria de lo que el bloque **ha aprendido de forma verificable** (sección 12 del Documento 0): resultados de la resolución de pronósticos, métricas de acierto y calibración por celda, certificados de horizonte, lecciones LEC-, fiabilidad de fuentes de opinión, ajustes aplicados y propuestos, evaluaciones sombra, historial de aciertos publicable y asignación exploratoria. Cada agente lee al inicio de cada encargo el extracto de su ámbito (máximo 10 lecciones, las de mayor fuerza) y la sección «Novedades»: así el aprendizaje entra en el contexto sin engordar los prompts.

## 2. Propietario, lectores y contratos

| Aspecto | Contenido |
|---|---|
| Propietario de escritura | AG-20 Evaluador (único) |
| Lectores | Todos (extracto por ámbito vía HT-06) |
| Contratos | CT-19 (difusión de su contenido), CT-22 (entradas de producto), CT-09/CT-10 (cálculos que sostienen métricas y decisiones) |
| Consumidores clave | Analizador (historial de aciertos para CT-15, certificados), Prospectiva (calibración, certificados), HT-09 (certificados para G3-CON-10), Buscador (fiabilidad de fuentes), Orquestador (lecciones de nivel A) |

## 3. Reglas

1. **Append-only**: métricas, certificados, lecciones y ajustes son entradas nuevas; los estados cambian por entradas nuevas; nada se borra.
2. **Toda cifra publicada** procede de un CALC- del Motor o de un recuento reproducible sobre F4/F5 (R7).
3. **Sin fuga**: cada métrica declara `comprobacion_fuga`.
4. **Celdas**: nivel 1 clase × horizonte; nivel 2 + método (certificación); nivel 3 + estrategia, tipo de opción y fuente (diagnóstico, con contracción).
5. **Muestras**: sin ≥ 30 resueltos en la celda de nivel 1, ninguna recalibración; sin ≥ 100 en la de nivel 2, ningún certificado (Anexo A).
6. **Lecciones**: máximo 10 vigentes por ámbito en el extracto de lectura; caducidad obligatoria.
7. **Novedades**: sección semanal con altas, revocaciones, ajustes y lecciones nuevas, enlazadas por identificador.

## 4. Formato de entrada

### 4.1 Lote de resolución (RES-)

`res_id` (`RES-AAAA-MM-DD`), `fecha`, `prg_resueltos` (lista), `prg_no_resolubles` (lista con motivo), `calc_id`, `comprobacion_fuga`.

### 4.2 Métricas por celda (MET-)

| Campo | Tipo | Valores / formato |
|---|---|---|
| `met_id` | Identificador | `MET-AAAA-MM` (o `-Wss` si semanal) + celda |
| `celda` | Objeto | `{nivel 1·2·3, clase, horizonte, metodo, estrategia, tipo_opcion, fuente}` |
| `ventana` | Texto | Fechas de congelación incluidas |
| `n` / `n_eff` | Enteros | — |
| `acierto` | Objeto | `{tasa, ic90_wilson}` |
| `brier` / `log` / `rps` | Números | — |
| `murphy` | Objeto | `{rel, res, unc, bins}` |
| `bss` | Objeto | `{valor, ic90, referencia, metodo_bootstrap BLOQUES·CONGLOMERADOS, replicas}` |
| `ece` / `mce` | Números | Con número de bins |
| `calibracion_global` | Objeto | `{p_media, frecuencia, pendiente, ic_pendiente}` |
| `dm_hln` | Objeto | `{estadistico, p_valor, h}` |
| `rentabilidad` | Objeto | `{relativa_media, ir, sharpe, sortino, alfa, t_alfa, indice_referencia}` |
| `seleccion` | Objeto | `{falsos_positivos, falsos_negativos, ic_spearman_rk, precision_at_3}` |
| `calc_ids` | Lista | CALC- |
| `comprobacion_fuga` | Enumerado | SUPERADA · FALLIDA |
| `madurez` | Enumerado | documentado · implementado · validado |

### 4.3 Certificado (CERT-)

`cert_id` (`CERT-AAAA-NNNN`), `celda` `{clase, horizonte, metodo, tipo_pronostico opcional}`, `ventana`, `n`, `n_eff`, `brier`, `brier_ref`, `bss`, `bss_ic90`, `holm_superado`, `ece`, `bins`, `curva_fiabilidad` (CALC-), `reejecucion` (CALC- de CT-10), `methodology_version`, `emitido`, `revision`, `estado`, `motivo_cambio`.

### 4.4 Lección (LEC-)

| Campo | Tipo | Valores / formato |
|---|---|---|
| `lec_id` | Identificador | `LEC-AAAA-NNNN` |
| `fecha` | Fecha | ISO 8601 |
| `ambito` | Objeto | `{clase, horizonte, agente[], fuente, metodo}` |
| `nivel` | Enumerado | A (operativo) · B (predictivo) · C (metodológico, solo como antecedente de tipo 3) |
| `tipo` | Enumerado | PREDICTIVA · OPERATIVA · PRODUCTO · FUENTE · CALIBRACION |
| `observacion` | Texto | Factual, con cifras |
| `evidencia` | Lista | CALC-, MET-, PRG-, RUN-, QRY-, HAL- |
| `recomendacion` | Texto | Operativa (qué hacer distinto y en qué fase) |
| `fuerza` | Enumerado | anecdotica · recurrente · estadistica |
| `n` / `efecto` | Entero / texto | Tamaño y magnitud con IC |
| `caducidad` | Fecha | 3, 6 o 12 meses según fuerza |
| `estado` | Enumerado | Sección 5 |
| `sustituye` | Identificador | LEC- anterior |

### 4.5 Fiabilidad de fuente (FUE-)

`fue_id`, `ref_id` (RF-), `periodo`, `n`, `aciertos`, `bss`, `bss_contraido` (k = 20), `puntos_historial` (0–20; neutro 10), `calc_id`, `comunicado_ct19` (msg_id).

### 4.6 Ajuste (AJU-) y evaluación sombra

`aju_id` (`AJU-AAAA-NNNN`), `parametro` (identificador de F10), `de`, `a`, `banda` `{trimestral, total}`, `acumulado_vs_inicial`, `evidencia` `{objetivo, mejora_fuera_muestra, ic90, calc, reejecucion}`, `methodology_version` (de → a), `efecto_desde`, `sombra_hasta`, `estado`, `resultado_sombra` `{metrica_nueva, metrica_anterior, dm_hln_p, decisiones_top3_cambiadas, decision CONFIRMADO·REVERTIDO}`.

### 4.7 Propuesta de tipo 3 (P3-EVAL-)

`p3_id`, `objeto`, `motivo` (fuera de banda · sin banda · cambio hacia o desde «No» · nuevo método · otro), `evidencia`, `impacto_esperado`, `pruebas_regresion` (IDs del plan de pruebas), `plan_reversion`, `elevada_via` (msg_id CT-19 al Orquestador), `estado` (ENVIADA · APROBADA · RECHAZADA · APLICADA, según comunique el Orquestador).

### 4.8 Historial de aciertos publicable (HAC-)

Estructura idéntica a `historial_aciertos` del paquete de oportunidades: `ventana`, `global` y `por_clase` con `n`, `aciertos`, `tasa_acierto`, `referencia`, `tasa_esperada_azar`, `significativo`, `por_horizonte`; más `nota`, `no_resolubles_excluidos`, `calc_id`, `publicado` (fecha-hora).

### 4.9 Producto (PRO-) y asignación exploratoria (BAN-)

- `PRO-`: `tema`, `qry_ids`, `veces_4_semanas`, `utilidad` `{mediana, distribucion, tendencia}`, `decisiones_broker` `{enviadas_vs_descartadas: rentabilidad relativa media de cada grupo, n}`, `lec_id` generada.
- `BAN-`: `periodo`, `clase`, `brazos` `{segmento, alfa, beta, prob_mejor, asignacion}`, `gamma`, `suelo`, `techo`, `recompensas` (tempranas y diferidas), `propensiones`.

## 5. Estados y transiciones

| Objeto | Transiciones |
|---|---|
| CERT- | `VIGENTE` → `EN_OBSERVACION` → `VIGENTE` · `REVOCADO`; `VIGENTE` → `REVOCADO` (BSS ≤ 0 en ventana, ECE ≥ 0,12, fuga, cambio de método o de versión mayor) |
| LEC- | `VIGENTE` → `REVISADA` (sustituida) · `CADUCADA` · `REFUTADA` |
| AJU- | `PROPUESTO` → `EN_SOMBRA` → `CONFIRMADO` · `REVERTIDO` |
| P3-EVAL- | `ENVIADA` → `APROBADA` → `APLICADA` · `RECHAZADA` |

## 6. Índices de consulta

| Índice | Clave | Uso |
|---|---|---|
| Lecciones por ámbito | `ambito.clase`, `ambito.agente`, `fuerza`, `estado` = VIGENTE | Lectura al inicio de cada encargo (máx. 10) |
| Certificados vigentes | `celda`, `estado` | Prospectiva, Analizador, HT-09 (G3-CON-10) |
| Métricas por celda | `celda`, `ventana` | Informes CT-19; revisión trimestral |
| Historial de aciertos vigente | último HAC- | Paquete de síntesis CT-15 |
| Fiabilidad por fuente | `ref_id` | Q de F9 |
| Ajustes en sombra | `estado` = EN_SOMBRA, `sombra_hasta` | Cierre trimestral |
| Novedades | Semana | Difusión sin canal nuevo |

## 7. Ejemplo ficticio

> **EJEMPLO FICTICIO — no es una entrada real.**

```json
{"lec_id":"LEC-2026-0001","fecha":"2026-11-30","ambito":{"clase":"DIV","horizonte":"H2","agente":["AG-05","AG-10"],"fuente":null,"metodo":"carry ajustado por volatilidad"},
 "nivel":"B","tipo":"PREDICTIVA","observacion":"PRG DIRECCIONAL H2 basados solo en carry en pares emergentes: acierto 47 % (n = 38) frente a tasa base 52 %",
 "evidencia":["MET-2026-11-DIV-H2","CALC-2026-0098"],"recomendacion":"En H2 para pares emergentes, no superar la banda «incierto» con señal solo de carry; exigir confirmación de momentum",
 "fuerza":"recurrente","n":38,"efecto":"−0,05 (IC 90 %: −0,16; 0,06)","caducidad":"2027-05-31","estado":"VIGENTE","sustituye":null}
```
