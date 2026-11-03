# Esquema de archivo operativo — F1 Registro maestro de tendencias

**Bloque A · Robot Investor · Versión óptima V4.0 · 01/11/2026** · Subordinado al Documento 0 óptima V5.0.

---

## 1. Propósito

F1 es la memoria estructurada de **tendencias** (TND-) del Bloque A y la fuente de verdad de su estado: qué está cambiando, por qué, en qué clases de activo influye, con qué evidencia, en qué estado de la máquina 9.4 está y qué lo invalidaría. Las oportunidades (F3) y los pronósticos (F4) se vinculan a sus tendencias; el Evaluador lo usa para medir la calidad de la detección de tendencias y el Coordinador para responder consultas de estado.

**No es**: un entregable (los informes citan `tnd_id`), un registro de oportunidades (una tendencia real no garantiza una oportunidad atractiva), ni un archivo de evidencia (las afirmaciones viven en F2). No es desechable: las tendencias invalidadas y archivadas se conservan (sin sesgo de supervivencia).

## 2. Propietario, lectores y contratos

| Aspecto | Contenido |
|---|---|
| Propietario de escritura | AG-02 Analizador de Tendencias de Inversión (único) |
| Lectores | Plano P2 (AG-02 a AG-13, AG-17), AG-18 Orquestador, AG-19 Auditor, AG-20 Evaluador, AG-01 Coordinador |
| Contratos que lo alimentan | CT-06 (informes de clase), CT-12 (prospectiva), CT-13 (objeciones), CT-05 (orden y retorno) |
| Herramientas | HT-03 (puntuaciones T/E/M/P), HT-06 (índice), HT-09 (comprobaciones G3-DAT-08, G3-MET-01) |

## 3. Reglas

1. **Append-only en lo sustantivo** (5.2 del Documento 0): altas, cambios de estado, nuevas puntuaciones y correcciones son entradas nuevas fechadas; nada se sobrescribe ni se borra.
2. **Control de novedad** antes de un alta: búsqueda por nombre canónico, denominaciones alternativas y similitud temática (HT-06). Si existe, se anota la detección en la ficha existente.
3. **Fusión**: una de las fichas pasa a `archivada` con `fusionada_en` = TND- que subsiste.
4. **Transiciones solo legales** (sección 5). Toda transición registra fecha, `run_id`, justificación y evidencia (EVD-/CLM-).
5. **Puntuaciones** T, E, M y P solo con HT-03, con desglose por dimensión (múltiplos de 10) y pesos vigentes de F10; total redondeado al múltiplo de 5; máximo dos NA/NE; cambios ≥ 15 puntos con justificación.
6. **Clases y horizontes unificados**: clases RV, RF, DIV, MP, INM, CRI, ALT; horizontes H1–H4. Una tendencia multiclase declara clase principal y secundarias.
7. **Revisión periódica**: toda ficha abierta tiene `fecha_proxima_revision` (por defecto, 90 días) y disparadores de reevaluación. Dos revisiones trimestrales sin actividad → candidata a `archivada`.
8. **Sin datos personales ni credenciales**; los extractos de contenido externo no se copian aquí (viven, mínimos, en F2).

## 4. Formato de entrada

| Campo | Tipo | Oblig. | Valores / formato | Descripción |
|---|---|---|---|---|
| `tnd_id` | Identificador | Sí (inmutable) | `TND-AAAA-NNNN` | Clave primaria |
| `version` | Entero | Sí | ≥ 1 | Versión de la ficha (correcciones) |
| `nombre_canonico` | Texto | Sí | Único en el archivo | Denominación canónica |
| `denominaciones_alternativas` | Lista de texto | No | — | Sinónimos y siglas para deduplicar |
| `categoria` | Enumerado | Sí | TECNOLOGICA · MACROECONOMICA · MONETARIA_FINANCIERA · SECTORIAL · REGULATORIA · SOCIAL_DEMOGRAFICA · MEDIOAMBIENTAL · GEOPOLITICA | Ámbito principal |
| `subcategoria` | Texto | Sí | Coherente con la categoría | Especialización |
| `clase_principal` | Enumerado | Sí | RV · RF · DIV · MP · INM · CRI · ALT | Clase de activo más afectada |
| `clases_secundarias` | Lista de enumerados | No | Mismos valores | Otras clases afectadas |
| `perfiles_motor` | Lista | No | PERF-ACC, PERF-FIR, PERF-FX, PERF-CMD, PERF-REI, PERF-CHR, PERF-PRV, PERF-ALT, PERF-ETF, PERF-DER, PERF-TEM, PERF-ESG | Perfiles aplicables (2.5) |
| `regiones` | Lista de enumerados | Sí | NAM · LAT · EUR · AFR · ORM · CHN · ASE · JPN · OCE · GLB | Ámbitos geográficos |
| `cadenas_de_valor` | Lista de texto | Sí | — | Eslabones afectados y quién captura el valor |
| `mecanismo` | Texto | Sí | Causal, con referencia CLM- | Por qué ocurre |
| `hipotesis_principal` | Texto + CLM- | Sí | Afirmación refutable | Enunciado central |
| `explicaciones_alternativas` | Lista de objetos | Sí (≥ 1) | `{texto, estado: ABIERTA·DESCARTADA·VIGENTE, evidencia}` | Rivales (ciclo, efecto base, selección…) |
| `condiciones_invalidacion` | Lista de objetos | Sí (≥ 1) | `{indicador, umbral, plazo}` | Observables y fechables |
| `indicadores_seguimiento` | Lista de objetos | Sí | `{nombre, serie_ht01 o ref_id, nivel_fuente A·B·C·D, frecuencia DIARIA·SEMANAL·MENSUAL·TRIMESTRAL·ANUAL, umbral_alerta, tipo ADELANTADO·COINCIDENTE·CONFIRMATORIO}` | Seguimiento |
| `hitos` | Lista de objetos | Sí | `{descripcion, fecha_o_condicion, indicador, estado PENDIENTE·ALCANZADO·INCUMPLIDO}` | Agenda |
| `horizontes_relevantes` | Lista | Sí | H1 · H2 · H3 · H4 | Horizontes en que la tendencia es accionable |
| `fase_madurez` | Enumerado | Sí | SENAL_TEMPRANA · EMERGENTE · EN_ADOPCION · CONSOLIDADA · EN_DECLIVE | Fase del fenómeno (distinta del estado epistémico) |
| `estado` | Enumerado | Sí | Sección 5 | Último estado del historial |
| `puntuaciones` | Objeto | Sí desde `en investigación` | `{T, E, M, P: {total, desglose[{dim, valor, NA/NE, justificacion}], fecha, methodology_version, pasada 1·2, ht03_ref}}` | Separadas, nunca fundidas |
| `narrativa_saturada` | Booleano | Sí | — | Activa el tope de 40 en la valoración de A de sus oportunidades |
| `relaciones` | Lista de objetos | No | `{tipo IMPULSORA·DEPENDIENTE·COMPETIDORA·SUSTITUTA, tnd_id}` | Relaciones entre tendencias |
| `objeciones` | Lista de objetos | Sí en `validada` | `{obj_id, run_id, tipo, fuerza FUERTE·MODERADA·DEBIL, estado ABIERTA·RESPONDIDA·SIN_RESOLVER, respuesta, evidencia}` | Objeciones del CT-13 |
| `opp_vinculadas` | Lista | No | OPP- | Oportunidades derivadas (F3) |
| `prg_vinculados` | Lista | No | PRG- | Pronósticos asociados (F4) |
| `referencias_evidencia` | Lista | Sí | EVD-, CLM- | Soporte probatorio |
| `referencias_ejecuciones` | Lista | Sí | RUN- | Ejecuciones que la tocaron |
| `lecciones_aplicadas` | Lista | No | LEC- | Lecciones de F6 usadas al revisarla |
| `fecha_primera_deteccion` | Fecha | Sí | ISO 8601 | — |
| `fecha_ultima_revision` | Fecha | Sí | ISO 8601 | — |
| `fecha_proxima_revision` | Fecha | Sí | ISO 8601 | Por defecto +90 días |
| `disparadores_reevaluacion` | Lista | Sí | `{evento_o_umbral, fecha}` | Qué obliga a revisarla antes |
| `fusionada_en` | Identificador | No | TND- | Solo si `archivada` por fusión |
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
| validada / en observación | acelerándose / desacelerándose | Indicadores de velocidad con evidencia |
| acelerándose / desacelerándose / en observación | invalidada | Condición de invalidación cumplida |
| cualquiera | archivada | Fusión, inactividad en dos revisiones trimestrales o fuera de alcance |
| invalidada | candidata | Evidencia nueva sustantiva (reapertura referenciada) |

Cualquier otra transición es ilegal (hallazgo Material).

## 6. Índices de consulta

| Índice | Clave | Uso típico |
|---|---|---|
| Por estado | `estado` | Tendencias activas para F0 del ciclo |
| Por clase | `clase_principal`, `clases_secundarias` | Carga de memoria de cada Analista de clase |
| Por región | `regiones` | Mapa del informe visual; consultas del Broker |
| Por revisión pendiente | `fecha_proxima_revision` ≤ hoy | Agenda de revisión |
| Por disparador | `disparadores_reevaluacion` | GC0: cambio material |
| Por oportunidad y pronóstico | `opp_vinculadas`, `prg_vinculados` | Trazabilidad TND↔OPP↔PRG |
| Por saturación | `narrativa_saturada` = true | Tope de valoración de A |
| Índice operativo (cabecera del archivo) | — | Recuentos por estado, clase y categoría; altas y archivadas del trimestre; fecha de revisión del índice |

## 7. Ejemplo ficticio

> **EJEMPLO FICTICIO — no es una entrada real.** Ningún dato describe una tendencia existente; los identificadores no se reutilizan.

```json
{"tnd_id":"TND-2026-0001","version":1,"nombre_canonico":"Ejemplo ficticio: electrificación de flotas logísticas urbanas",
 "categoria":"TECNOLOGICA","subcategoria":"movilidad eléctrica comercial","clase_principal":"RV","clases_secundarias":["MP"],
 "perfiles_motor":["PERF-ACC","PERF-CMD","PERF-TEM"],"regiones":["EUR"],
 "cadenas_de_valor":["baterías","infraestructura de recarga","operadores logísticos"],
 "mecanismo":"Coste total de propiedad inferior al diésel en rutas urbanas (CLM-2026-0001)",
 "hipotesis_principal":{"texto":"La cuota de furgonetas eléctricas en matriculaciones urbanas de la UE superará el 25 % en 2027","clm_id":"CLM-2026-0001"},
 "explicaciones_alternativas":[{"texto":"Efecto temporal de subvenciones","estado":"ABIERTA","evidencia":["EVD-2026-0003"]}],
 "condiciones_invalidacion":[{"indicador":"cuota de matriculaciones eléctricas comerciales","umbral":"< 12 % dos trimestres seguidos","plazo":"2027-12-31"}],
 "indicadores_seguimiento":[{"nombre":"matriculaciones eléctricas comerciales","ref_id":"RF-0001","nivel_fuente":"A","frecuencia":"MENSUAL","umbral_alerta":"variación interanual < 10 %","tipo":"COINCIDENTE"}],
 "hitos":[{"descripcion":"Entrada en vigor de zonas de bajas emisiones adicionales","fecha_o_condicion":"2027-01-01","indicador":"normativa","estado":"PENDIENTE"}],
 "horizontes_relevantes":["H3","H4"],"fase_madurez":"EN_ADOPCION","estado":"candidata","narrativa_saturada":false,
 "puntuaciones":null,"opp_vinculadas":[],"prg_vinculados":[],"referencias_evidencia":["EVD-2026-0001","CLM-2026-0001"],
 "referencias_ejecuciones":["RUN-2026-0001"],"fecha_primera_deteccion":"2026-11-07","fecha_ultima_revision":"2026-11-07",
 "fecha_proxima_revision":"2027-02-05","disparadores_reevaluacion":[{"evento_o_umbral":"publicación de matriculaciones del 4T","fecha":"2027-01-20"}],
 "historial_estados":[{"fecha":"2026-11-07","run_id":"RUN-2026-0001","de":null,"a":"candidata","justificacion":"una raíz independiente","evidencia":["EVD-2026-0001"]}]}
```
