# Esquema de archivo operativo — F1 Registro maestro de tendencias

**Bloque A Forex · Robot Investor · Versión V1.0 · 02/11/2026** · Subordinado al Documento 0 del Bloque A Forex, versión óptima V1.0.

---

## 1. Propósito

F1 es la memoria estructurada de **tendencias cambiarias** (TND-FX-) del Bloque A Forex y la fuente de verdad de su estado: qué está cambiando en el mercado de divisas (p. ej., divergencia prolongada de política monetaria, deterioro de la balanza por cuenta corriente, desdolarización de reservas, cambio de régimen de un banco central), por qué, a qué segmentos y divisas afecta y en qué sentido, por qué canales se transmite al tipo de cambio, con qué evidencia, en qué estado de la máquina 9.4 está y qué la invalidaría. Las oportunidades (F3) y los pronósticos (F4) se vinculan a sus tendencias; el Evaluador lo usa para medir la calidad de la detección de tendencias y el Coordinador para responder consultas de estado.

**No es**: un entregable (los informes citan `tnd_id`), un registro de oportunidades (una tendencia real no garantiza una oportunidad atractiva si el forward y el posicionamiento ya la descuentan), ni un archivo de evidencia (las afirmaciones viven en F2). Tampoco sustituye a los informes transversales de AG-09 y AG-21 (que se archivan en F5): F1 recoge tendencias persistentes, no la fotografía semanal. No es desechable: las tendencias invalidadas y archivadas se conservan (sin sesgo de supervivencia).

## 2. Propietario, lectores y contratos

| Aspecto | Contenido |
|---|---|
| Propietario de escritura | AG-02 Analizador de Oportunidades en Divisas (único) |
| Lectores | Plano P2 (AG-02 a AG-13, AG-17 y AG-21), AG-14, AG-15, AG-16, AG-18 Orquestador, AG-19 Auditor, AG-20 Evaluador, AG-01 Coordinador |
| Contratos que lo alimentan | CT-06 (informes de segmento), CT-06T (señales de los informes transversales de AG-09 y AG-21, que el Analizador convierte en tendencias cuando son persistentes), CT-12 (prospectiva), CT-13 (objeciones), CT-05 (orden y retorno) |
| Herramientas | HT-03 (puntuaciones T/E/M/P), HT-06 (índice), HT-09 (comprobaciones G3-DAT-08, G3-MET-01) |

## 3. Reglas

1. **Append-only en lo sustantivo** (5.2 del Documento 0): altas, cambios de estado, nuevas puntuaciones y correcciones son entradas nuevas fechadas; nada se sobrescribe ni se borra.
2. **Control de novedad** antes de un alta: búsqueda por nombre canónico, denominaciones alternativas, divisas afectadas y similitud temática (HT-06). Si existe, se anota la detección en la ficha existente. Una misma tendencia vista desde dos segmentos (p. ej., «endurecimiento del BoJ», que afecta a G10N, G10M y ESTR) tiene **una sola ficha** con segmento principal y secundarios.
3. **Fusión**: una de las fichas pasa a `archivada` con `fusionada_en` = TND-FX- que subsiste.
4. **Transiciones solo legales** (sección 5). Toda transición registra fecha, `run_id`, justificación y evidencia (EVD-/CLM-).
5. **Puntuaciones** T, E, M y P solo con HT-03, con desglose por dimensión (múltiplos de 10) y pesos vigentes de F10; total redondeado al múltiplo de 5; máximo dos NA/NE; cambios ≥ 15 puntos con justificación. En T, la dimensión «posición en la cadena de transmisión» mide si la tendencia actúa en el origen (p. ej., la función de reacción del banco central) o en un eslabón derivado (p. ej., un flujo de cartera que reacciona a ella).
6. **Segmentos, divisas y horizontes unificados**: segmentos G10N, G10M, EMAS, EMLA, EMEA y ESTR (2.6); divisas con código ISO 4217 (CNH se admite como código de mercado del renminbi offshore); horizontes H1–H4. Una tendencia multisegmento declara segmento principal y secundarios. El efecto esperado se declara **por divisa** (aprecia, deprecia o ambiguo), nunca solo «el par sube».
7. **Saturación narrativa**: `narrativa_saturada` = true cuando el posicionamiento especulativo está en el decil extremo de su historia a favor de la tesis y el forward o la curva ya descuentan la senda de tipos que la tesis espera (9.1); activa el tope de 40 en la valoración de A de sus oportunidades.
8. **Revisión periódica**: toda ficha abierta tiene `fecha_proxima_revision` (por defecto, 90 días; antes si hay reunión del banco central afectado) y disparadores de reevaluación. Dos revisiones trimestrales sin actividad → candidata a `archivada`.
9. **Sin datos personales ni credenciales**; los extractos de contenido externo no se copian aquí (viven, mínimos, en F2).

## 4. Formato de entrada

| Campo | Tipo | Oblig. | Valores / formato | Descripción |
|---|---|---|---|---|
| `tnd_id` | Identificador | Sí (inmutable) | `TND-FX-AAAA-NNNN` | Clave primaria (prefijo FX para no colisionar con el Bloque A general) |
| `version` | Entero | Sí | ≥ 1 | Versión de la ficha (correcciones) |
| `nombre_canonico` | Texto | Sí | Único en el archivo | Denominación canónica |
| `denominaciones_alternativas` | Lista de texto | No | — | Sinónimos y siglas para deduplicar |
| `categoria` | Enumerado | Sí | POLITICA_MONETARIA · CICLO_MACRO · BALANZA_DE_PAGOS_Y_FLUJOS · VALORACION_EQUILIBRIO · REGIMEN_E_INTERVENCION · MATERIAS_PRIMAS_TERMINOS_INTERCAMBIO · RIESGO_GLOBAL_Y_REFUGIO · POSICIONAMIENTO_Y_MICROESTRUCTURA · GEOPOLITICA_SANCIONES_Y_POLITICA · SISTEMA_MONETARIO_INTERNACIONAL | Ámbito principal |
| `subcategoria` | Texto | Sí | Coherente con la categoría | Especialización (p. ej., «divergencia Fed–BoJ», «desdolarización de reservas») |
| `segmento_principal` | Enumerado | Sí | G10N · G10M · EMAS · EMLA · EMEA · ESTR | Segmento más afectado |
| `segmentos_secundarios` | Lista de enumerados | No | Mismos valores | Otros segmentos afectados |
| `divisas_afectadas` | Lista de objetos | Sí (≥ 1) | `{divisa ISO 4217, efecto APRECIACION·DEPRECIACION·AMBIGUO, frente_a (divisa o «amplio»), intensidad ALTA·MEDIA·BAJA}` | Efecto esperado por divisa |
| `bancos_centrales` | Lista | No | Fed, BCE, BoJ, BoE, BNS, RBA, RBNZ, BoC, Norges Bank, Riksbank, PBoC, RBI, BoK, Banxico, BCB, BCRP, BanRep, BCCh, NBP, MNB, CNB, CBRT, SARB… | Autoridades monetarias implicadas |
| `perfiles_motor` | Lista | No | PERF-FX-G10 · PERF-FX-EM · PERF-FX-FACT | Perfiles aplicables |
| `canales_transmision` | Lista de objetos | Sí | `{canal DIFERENCIAL_TIPOS·FLUJOS_CARTERA·FLUJOS_COBERTURA·COMERCIO_Y_CUENTA_CORRIENTE·TERMINOS_INTERCAMBIO·RIESGO_GLOBAL·INTERVENCION·CONTROLES_CAPITALES·RESERVAS·CONFIANZA_POLITICA, descripcion}` | Cómo llega la tendencia al tipo de cambio |
| `mecanismo` | Texto | Sí | Causal, con referencia CLM- | Por qué ocurre |
| `hipotesis_principal` | Texto + CLM- | Sí | Afirmación refutable | Enunciado central |
| `explicaciones_alternativas` | Lista de objetos | Sí (≥ 1) | `{texto, estado: ABIERTA·DESCARTADA·VIGENTE, evidencia}` | Rivales (efecto dólar global, prima de riesgo, flujo puntual, estacionalidad de fin de año…) |
| `condiciones_invalidacion` | Lista de objetos | Sí (≥ 1) | `{indicador, umbral, plazo}` | Observables y fechables (p. ej., «diferencial a 2 años EE. UU.–Japón se amplía > 50 pb») |
| `indicadores_seguimiento` | Lista de objetos | Sí | `{nombre, serie_ht01 o ref_id, nivel_fuente A·B·C·D, frecuencia DIARIA·SEMANAL·MENSUAL·TRIMESTRAL·ANUAL, umbral_alerta, tipo ADELANTADO·COINCIDENTE·CONFIRMATORIO}` | Seguimiento (diferenciales, curvas OIS, REER del BPI, COT, reservas…) |
| `hitos` | Lista de objetos | Sí | `{descripcion, fecha_o_condicion, indicador, estado PENDIENTE·ALCANZADO·INCUMPLIDO}` | Agenda (reuniones, datos, elecciones, revisiones de índices de bonos) |
| `horizontes_relevantes` | Lista | Sí | H1 · H2 · H3 · H4 | Horizontes en que la tendencia es accionable, dentro de la matriz 8.3 de su segmento |
| `fase_madurez` | Enumerado | Sí | SENAL_TEMPRANA · EMERGENTE · EN_CURSO · CONSOLIDADA · EN_DECLIVE | Fase del fenómeno (distinta del estado epistémico) |
| `estado` | Enumerado | Sí | Sección 5 | Último estado del historial |
| `puntuaciones` | Objeto | Sí desde `en investigación` | `{T, E, M, P: {total, desglose[{dim, valor, NA/NE, justificacion}], fecha, methodology_version, pasada 1·2, ht03_ref}}` | Separadas, nunca fundidas |
| `narrativa_saturada` | Objeto | Sí | `{valor booleano, percentil_posicionamiento, descontado_en_forward sí/no, fuente_pfv (msg_id del CT-06T), fecha}` | Activa el tope de 40 en la valoración de A |
| `relaciones` | Lista de objetos | No | `{tipo IMPULSORA·DEPENDIENTE·COMPETIDORA·SUSTITUTA, tnd_id}` | Relaciones entre tendencias |
| `objeciones` | Lista de objetos | Sí en `validada` | `{obj_id, run_id, tipo, fuerza FUERTE·MODERADA·DEBIL, estado ABIERTA·RESPONDIDA·SIN_RESOLVER, respuesta, evidencia}` | Objeciones del CT-13 |
| `opp_vinculadas` | Lista | No | OPP-FX- | Oportunidades derivadas (F3) |
| `prg_vinculados` | Lista | No | PRG-FX- | Pronósticos asociados (F4) |
| `referencias_evidencia` | Lista | Sí | EVD-, CLM- | Soporte probatorio |
| `referencias_ejecuciones` | Lista | Sí | RUN-FX- | Ejecuciones que la tocaron |
| `origen_transversal` | Lista | No | `{capa BCM·PFV, msg_id del CT-06T, fecha}` | Informes transversales que la originaron o la modificaron |
| `lecciones_aplicadas` | Lista | No | LEC- | Lecciones de F6 usadas al revisarla |
| `fecha_primera_deteccion` | Fecha | Sí | ISO 8601 | — |
| `fecha_ultima_revision` | Fecha | Sí | ISO 8601 | — |
| `fecha_proxima_revision` | Fecha | Sí | ISO 8601 | Por defecto +90 días o la siguiente reunión del banco central afectado, lo que ocurra antes |
| `disparadores_reevaluacion` | Lista | Sí | `{evento_o_umbral, fecha}` | Qué obliga a revisarla antes |
| `fusionada_en` | Identificador | No | TND-FX- | Solo si `archivada` por fusión |
| `historial_estados` | Lista append-only | Sí | `{fecha, run_id, de, a, justificacion, evidencia}` | Transiciones |
| `correcciones` | Lista append-only | No | `{fecha, campo, valor_anterior_ref, motivo, autor}` | Correcciones referenciadas |

## 5. Estados y transiciones

Estados: `candidata` · `en investigación` · `validada` · `en observación` · `acelerándose` · `desacelerándose` · `invalidada` · `archivada`.

| Desde | Hacia | Condición |
|---|---|---|
| (detección) | candidata | ≥ 1 raíz independiente en F2 |
| candidata | en investigación | ≥ 2 raíces o nivel N2/N3 asignado |
| en investigación | validada | G1–G3 superadas, sin objeción fuerte ni moderada abierta, E ≥ 60 (umbral de F10) |
| en investigación | invalidada | Objeción fuerte confirmada o evidencia contraria decisiva |
| en investigación | candidata | Insuficiencia de evidencia sostenida |
| validada | en observación | Señal estable sin cambio de fase |
| validada / en observación | acelerándose / desacelerándose | Indicadores de velocidad con evidencia (p. ej., ampliación o estrechamiento del diferencial esperado) |
| acelerándose / desacelerándose / en observación | invalidada | Condición de invalidación cumplida |
| cualquiera | archivada | Fusión, inactividad en dos revisiones trimestrales o fuera de alcance |
| invalidada | candidata | Evidencia nueva sustantiva (reapertura referenciada) |

Cualquier otra transición es ilegal (hallazgo Material).

## 6. Índices de consulta

| Índice | Clave | Uso típico |
|---|---|---|
| Por estado | `estado` | Tendencias activas para F0 del ciclo |
| Por segmento | `segmento_principal`, `segmentos_secundarios` | Carga de memoria de cada Analista de segmento |
| Por divisa | `divisas_afectadas.divisa`, `efecto` | Exposición agregada; mapa de divisas del informe visual; consultas del Broker |
| Por banco central | `bancos_centrales` | Agenda de AG-09; disparadores en semanas de reunión |
| Por revisión pendiente | `fecha_proxima_revision` ≤ hoy | Agenda de revisión |
| Por disparador | `disparadores_reevaluacion` | GC0: cambio material |
| Por oportunidad y pronóstico | `opp_vinculadas`, `prg_vinculados` | Trazabilidad TND↔OPP↔PRG |
| Por saturación | `narrativa_saturada.valor` = true | Tope de valoración de A |
| Índice operativo (cabecera del archivo) | — | Recuentos por estado, segmento, divisa y categoría; altas y archivadas del trimestre; fecha de revisión del índice |

## 7. Ejemplo ficticio

> **EJEMPLO FICTICIO — no es una entrada real.** Los datos, umbrales e identificadores son inventados con fines ilustrativos; los identificadores no se reutilizan.

```json
{"tnd_id":"TND-FX-2026-0001","version":1,"nombre_canonico":"Ejemplo ficticio: estrechamiento del diferencial de tipos EE. UU.–Japón por divergencia Fed–BoJ",
 "categoria":"POLITICA_MONETARIA","subcategoria":"divergencia Fed–BoJ","segmento_principal":"G10N","segmentos_secundarios":["G10M","ESTR"],
 "divisas_afectadas":[{"divisa":"JPY","efecto":"APRECIACION","frente_a":"amplio","intensidad":"ALTA"},{"divisa":"USD","efecto":"DEPRECIACION","frente_a":"JPY","intensidad":"MEDIA"}],
 "bancos_centrales":["Fed","BoJ"],"perfiles_motor":["PERF-FX-G10","PERF-FX-FACT"],
 "canales_transmision":[{"canal":"DIFERENCIAL_TIPOS","descripcion":"menor diferencial a 2 años reduce el carry a favor del USD"},{"canal":"FLUJOS_COBERTURA","descripcion":"aumento de las ratios de cobertura de inversores japoneses en activos en USD"}],
 "mecanismo":"El BoJ normaliza su política antes de lo descontado mientras la Fed recorta (CLM-FX-2026-0101)",
 "hipotesis_principal":{"texto":"El diferencial a 2 años EE. UU.–Japón se estrechará al menos 75 pb en 6 meses","clm_id":"CLM-FX-2026-0101"},
 "explicaciones_alternativas":[{"texto":"Movimiento del yen explicado por aversión global al riesgo y no por política monetaria","estado":"ABIERTA","evidencia":["EVD-FX-2026-0103"]}],
 "condiciones_invalidacion":[{"indicador":"diferencial a 2 años EE. UU.–Japón","umbral":"se amplía > 50 pb desde el nivel de detección","plazo":"2027-05-31"},{"indicador":"comunicación del BoJ","umbral":"descarta subidas en el horizonte de previsión","plazo":"2027-05-31"}],
 "indicadores_seguimiento":[{"nombre":"diferencial OIS a 2 años EE. UU.–Japón","serie_ht01":"FICT-OIS2Y-USJP","nivel_fuente":"A","frecuencia":"DIARIA","umbral_alerta":"variación semanal > 15 pb","tipo":"ADELANTADO"},{"nombre":"posición neta no comercial en JPY (COT)","serie_ht01":"FICT-COT-JPY","nivel_fuente":"A","frecuencia":"SEMANAL","umbral_alerta":"percentil > 90 o < 10","tipo":"CONFIRMATORIO"}],
 "hitos":[{"descripcion":"Reunión de política monetaria del BoJ","fecha_o_condicion":"2026-12-18","indicador":"decisión y comunicado","estado":"PENDIENTE"}],
 "horizontes_relevantes":["H2","H3"],"fase_madurez":"EMERGENTE","estado":"candidata",
 "narrativa_saturada":{"valor":false,"percentil_posicionamiento":62,"descontado_en_forward":"no","fuente_pfv":"MSG-2026-11-07-0021","fecha":"2026-11-07"},
 "puntuaciones":null,"opp_vinculadas":[],"prg_vinculados":[],"referencias_evidencia":["EVD-FX-2026-0101","CLM-FX-2026-0101"],
 "referencias_ejecuciones":["RUN-FX-2026-0001"],"origen_transversal":[{"capa":"BCM","msg_id":"MSG-2026-11-07-0018","fecha":"2026-11-07"}],
 "fecha_primera_deteccion":"2026-11-07","fecha_ultima_revision":"2026-11-07","fecha_proxima_revision":"2026-12-18",
 "disparadores_reevaluacion":[{"evento_o_umbral":"reunión del BoJ","fecha":"2026-12-18"},{"evento_o_umbral":"reunión del FOMC","fecha":"2026-12-09"}],
 "historial_estados":[{"fecha":"2026-11-07","run_id":"RUN-FX-2026-0001","de":null,"a":"candidata","justificacion":"una raíz independiente (comunicado ficticio del BoJ)","evidencia":["EVD-FX-2026-0101"]}]}
```
