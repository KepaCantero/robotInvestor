# Esquema de archivo operativo — F4 Registro de pronósticos congelados

**Bloque B · Robot Investor · Versión óptima V2.0 · actualizado V2.1, 03/11/2026** · Subordinado al Documento 0 del Bloque B óptima V2.1 (ante discrepancia, manda el Documento 0).

---

## 1. Propósito

F4 conserva cada **pronóstico verificable** (PRG-B) que el Bloque B entrega, **congelado** con su fecha, horizonte (H1–H5), afirmación, probabilidad interna o banda, referencia de comparación, referencia ingenua, criterio y fecha de resolución (R14); y, cuando vence, su **resolución** y su puntuación. Hay dos familias:

- **Pronósticos del ámbito**: sobre el indicador de seguimiento del ámbito, en absoluto o frente a su referencia (8.5, campo «Referencia»; 9.11).
- **Hitos intermedios H5 (V2.1)**: en una tesis de décadas (horizonte principal H5), afirmaciones verificables con fecha entre 1 y 5 años (`tipo_pronostico = HITO_H5`, fichas DIF-H5-001 y FC-HITO-001) que permiten evaluar la tesis antes de su horizonte; al menos tres por tesis H5; dos hitos **críticos** incumplidos generan una alerta `REVISION` del Vigía (Anexo A).
- **Pronósticos del ranking**: sobre la rentabilidad relativa del top-N de un tipo de activo frente a la **media equiponderada del universo cribado** del mismo tipo, y sobre el IC de rango (Spearman entre S y la rentabilidad posterior relativa al universo).

Es la base de la evaluación sin fuga de información, de los certificados de probabilidad y de ranking (R13; 12.3), del historial de aciertos que se publica en cada entrega y de la recalibración dentro de bandas (12.2).

**No es editable hacia atrás** (R14): nadie retoca un pronóstico congelado.

## 2. Propietario, lectores y contratos

| Aspecto | Contenido |
|---|---|
| Escritura de altas | AG-B13 Analista de Prospectiva, Escenarios y Proyecciones (propone en F4 de la petición; congela en la fase F10, tras la autorización de salida) |
| Escritura de resolución | AG-B23 Evaluador, **exclusivamente** en el bloque `resolucion` y en `estado` |
| Lectores | Todos los agentes |
| Contratos | CT-B-16 (PRG-B propuestos), CT-B-08 (retorno al cierre), CT-B-13/CT-B-14 (puntuaciones del Motor, MC-B10), CT-B-22 (difusión de resultados) |
| Herramientas | HT-01 (series con fecha «conocible desde»), HT-05 (recordatorios de vencimiento), HT-09 (comprobaciones de pronósticos congelables y de probabilidad certificada) |

## 3. Reglas

1. **Congelación** (R14): la entrada de alta no se modifica jamás. Una corrección es un PRG-B nuevo con `version_de`; **el original se sigue evaluando** en su fecha y la versión nueva desde su propia congelación.
2. **Separación de escritura**: altas solo Prospectiva; resolución solo el Evaluador. Otra escritura es incidencia Material (R8).
3. **Probabilidad honesta** (R13): `prob_interna` se registra siempre (rejilla de 5 puntos; 15–85 % sin certificado); `prob_publicada` solo con certificado vigente de la celda (`certificado_ref`). Sin certificado, el entregable muestra la banda verbal del Anexo A y «sin ventaja demostrada todavía» (una frecuencia histórica o probabilidad implícita de mercado solo se publica como «ponderación de base externa» con su fuente, nunca como probabilidad propia); para los rankings, «ranking sin ventaja demostrada todavía».
4. **Sin fuga**: nada en el alta es posterior a `fecha_congelacion`; el nivel de referencia respeta la antigüedad máxima del Anexo A para su horizonte; la referencia ingenua se calcula con datos conocibles en esa fecha (MC-B10).
5. **Universo completo**: todos los PRG-B se resuelven, incluidos los de análisis invalidados, de candidatos descartados por el Broker o de ámbitos con veredicto VIGILAR o DESCARTAR (se mide también lo que el Broker no siguió, 7.8; y los falsos negativos, 12.1).
6. **Rankings sin supervivencia**: el universo de referencia de un pronóstico de ranking se fija en la congelación (`universo_ref`, artefacto de RC); los miembros deslistados, fusionados o suspendidos durante el horizonte se resuelven con la regla `tratamiento_bajas` declarada en el alta, nunca eliminándolos (12.6).
7. **NO_RESOLUBLE** solo con motivo (dato inexistente tras el fallback, afirmación ambigua, serie discontinuada); se cuenta y se publica.
8. **Horizontes aplicables**: un PRG-B solo puede tener un horizonte «Sí» o «Limitado» (con catalizador y datos declarados) para su tipo de activo según la matriz vigente en F10 (8.6). H1 lleva la advertencia de menor fiabilidad (R30).
9. Conservación indefinida (Anexo A).
10. **H5 (V2.1)**: un PRG-B con horizonte H5 lleva solo **probabilidad cualitativa** (banda verbal; `prob_publicada` siempre null, aunque exista certificado de otra celda) y se apoya en sus hitos `HITO_H5`, cuya referencia ingenua es la extrapolación lineal de la tendencia (`RI-LIN`). La antigüedad máxima del nivel de referencia de H5 es de 90 días; la longitud nominal del horizonte, 1260 sesiones.
11. **Paradas en puerta (V2.1)**: un análisis detenido en PV1 o PV2 no congela pronósticos (7.11).

## 4. Formato de entrada

### 4.1 Campos de alta (Prospectiva)

| Campo | Tipo | Oblig. | Valores / formato | Descripción |
|---|---|---|---|---|
| `prg_id` | Identificador | Sí | `PRG-B-AAAA-NNNN` | Clave |
| `version_de` | Identificador | No | PRG-B anterior | Corrección |
| `pet_id` / `rec_id` / `run_id` | Identificadores | Sí | — | Vínculos |
| `familia` | Enumerado | Sí | AMBITO · RANKING (los HITO_H5 pertenecen a AMBITO) | Sección 1 |
| `celda` | Objeto | Sí | `{tipo_objeto, tipo_activo, horizonte, metodo, playbook (si RANKING), perfil_motor}` | Celda de evaluación y certificación (12.1) |
| `tipo_pronostico` | Enumerado | Sí | DIRECCIONAL · RELATIVO · RANGO · UMBRAL · EVENTO · CUANTIL · RANKING_EXCESO · RANKING_IC · HITO_H5 (V2.1) | Forma |
| `hito` | Objeto | Si HITO_H5 | `{descripcion, fecha_objetivo (1–5 años), critico sí/no, tesis_h5 (PRG-B de la tesis), observable, fuente_resolucion}` | DIF-H5-001, FC-HITO-001 |
| `afirmacion` | Texto | Sí | Inequívoca | Lo que se pronostica |
| `variable` | Objeto | Sí | `{serie_ht01, descripcion, tipo_rentabilidad PRECIO·TOTAL, divisa (EUR por defecto)}` | Qué se mide |
| `referencia_comparacion` | Objeto | Sí | `{tipo INDICE_AMBITO·UNIVERSO_EQUIPONDERADO·NINGUNA, serie_ht01 o universo_ref}` | 9.11 |
| `universo_ref` | Identificador | Si RANKING | CALC-B del universo cribado congelado | Base sin supervivencia |
| `top_n_congelado` | Lista | Si RANKING | `{cand_id, rango, S}` | Ranking que se evalúa |
| `tratamiento_bajas` | Texto | Si RANKING | p. ej., «último precio negociado; fusiones a la contraprestación» | Regla 6 |
| `nivel_referencia` | Objeto | Sí | `{valor, fecha_hora, fuente}` | Punto de partida |
| `umbral` / `rango` / `cuantiles` | Número / par / lista | Según tipo | — | Condición |
| `fecha_congelacion` / `fecha_resolucion` | Fecha-hora / fecha | Sí | ISO 8601 | — |
| `criterio_resolucion` / `fuente_resolucion` / `regla_fallback` | Texto | Sí | Convención exacta | — |
| `banda_verbal` | Enumerado | Sí | MUY_PROBABLE · MAS_PROBABLE_QUE_NO · INCIERTO · POCO_PROBABLE · MUY_POCO_PROBABLE | Correspondencia del Anexo A |
| `prob_interna` | Número | Sí | 0,05–0,95 (rejilla 0,05) | Siempre registrada |
| `prob_publicada` / `certificado_ref` | Número o null / identificador | Sí / si publicada | CERT-B de F5 | R13 |
| `referencia_ingenua` | Objeto | Sí | `{tipo PASEO_ALEATORIO·ULTIMO_VALOR·MEDIA_HISTORICA·TASA_BASE·CLIMATOLOGIA·RANKING_ALEATORIO·FACTOR_TRIVIAL·RI-LIN (extrapolación lineal, HITO_H5), valor_o_prob, calc_id}` | 9.11 |
| `escenario_asociado` | Enumerado | Sí | BASE · FAVORABLE · ADVERSO | — |
| `veredicto_asociado` | Enumerado | Sí | Veredicto del ámbito o del candidato | Falsos positivos y negativos |
| `advertencia_H1` | Booleano | Si H1 | true | R30 |
| `en_entregable` | Booleano | Sí | — | Publicado o solo interno |
| `estado` | Enumerado | Sí | ABIERTO al alta | — |

### 4.2 Campos de resolución (exclusivos del Evaluador)

| Campo | Tipo | Oblig. al resolver | Descripción |
|---|---|---|---|
| `resolucion.fecha_resuelto` / `fecha_corte` | Fechas | Sí | `fecha_corte` = fecha de resolución; ningún dato posterior (6.2.9) |
| `resolucion.valor_observado` | Número / texto | Sí salvo NO_RESOLUBLE | Con unidad |
| `resolucion.fuente_usada` / `vintage` / `fallback_aplicado` | Texto / texto / booleano | Sí | — |
| `resolucion.resultado` | Enumerado | Sí | OCURRIDO · NO_OCURRIDO · VALOR |
| `resolucion.puntuaciones` | Objeto | Sí | `{brier, log, brier_ref, log_ref, pinball, error_vs_ingenua}` |
| `resolucion.ranking` | Objeto | Si RANKING | `{exceso_topN_vs_universo, ic_rango_spearman, tasa_acierto_topN, contribucion_componentes {PE, QL, VA, MO, RI, LA, CO}, bajas_tratadas}` |
| `resolucion.calc_id` | Identificador | Sí | CALC-B (MC-B10) |
| `resolucion.comprobacion_fuga` | Enumerado | Sí | SUPERADA · FALLIDA |
| `resolucion.motivo_no_resoluble` / `corrige_a` | Texto / identificador | Si aplica | — |

## 5. Estados y transiciones

| Desde | Hacia | Quién | Condición |
|---|---|---|---|
| (alta) | ABIERTO | Prospectiva | Congelación en la fase F10 |
| ABIERTO | RESUELTO | Evaluador | Dato disponible y resultado calculado |
| ABIERTO | NO_RESOLUBLE | Evaluador | Motivo documentado tras el fallback (o 10 días hábiles sin dato) |
| RESUELTO | RESUELTO (corrección) | Evaluador | Entrada nueva con `corrige_a`; la anterior se conserva |

No existen estados «anulado» ni «invalidado»: la invalidación de una REC-B o de un candidato no detiene la resolución.

## 6. Índices de consulta

| Índice | Clave | Uso |
|---|---|---|
| Vencimientos | `fecha_resolucion`, `estado` = ABIERTO | Resolución (HT-05) |
| Celda | `celda` | Métricas, certificados, recalibración, aplicabilidad de horizontes |
| Por familia | `familia` | Separación ámbito / ranking |
| Por análisis | `rec_id`, `pet_id` | Historial de aciertos; respuestas N0 |
| Correcciones | `version_de` | Evaluación conjunta del original y de la corrección |
| Publicados con probabilidad | `prob_publicada` ≠ null | Coherencia con certificados vigentes |
| Hitos H5 (V2.1) | `tipo_pronostico` = HITO_H5, `hito.critico`, `hito.tesis_h5` | Alerta `REVISION` con dos hitos críticos incumplidos; evaluación de tesis H5 |

## 7. Ejemplo ficticio

> **EJEMPLO FICTICIO — no es una entrada real.**

```json
{"prg_id":"PRG-B-2026-0021","pet_id":"PET-B-2026-0007","rec_id":"REC-B-2026-0007","run_id":"RUN-B-2026-0007-01","familia":"RANKING",
 "celda":{"tipo_objeto":"CADENA_DE_VALOR","tipo_activo":"RV","horizonte":"H3","metodo":"S-SEL-RV-2.0","playbook":"SEL-RV","perfil_motor":"PERF-B-CADENA"},
 "tipo_pronostico":"RANKING_EXCESO","afirmacion":"La media equiponderada del top-5 RV superará a la media equiponderada del universo cribado RV (n = 53) en rentabilidad total en EUR a 6 meses",
 "variable":{"serie_ht01":"CESTA-TOPN-PRG-B-2026-0021","descripcion":"rentabilidad total equiponderada","tipo_rentabilidad":"TOTAL","divisa":"EUR"},
 "referencia_comparacion":{"tipo":"UNIVERSO_EQUIPONDERADO","universo_ref":"CALC-B-2026-0139"},"universo_ref":"CALC-B-2026-0139",
 "top_n_congelado":[{"cand_id":"CAND-B-2026-0041","rango":1,"S":79},{"cand_id":"CAND-B-2026-0044","rango":2,"S":76}],
 "tratamiento_bajas":"último precio negociado; fusiones a la contraprestación en efectivo o en títulos",
 "nivel_referencia":{"valor":100.0,"fecha_hora":"2026-11-10T17:35:00+01:00","fuente":"HT-01"},
 "fecha_congelacion":"2026-11-10T19:02:00+01:00","fecha_resolucion":"2027-05-10","criterio_resolucion":"cierre oficial; dividendos reinvertidos",
 "fuente_resolucion":"HT-01","regla_fallback":"sesión hábil anterior","banda_verbal":"MAS_PROBABLE_QUE_NO","prob_interna":0.60,"prob_publicada":null,"certificado_ref":null,
 "referencia_ingenua":{"tipo":"RANKING_ALEATORIO","valor_o_prob":0.5,"calc_id":"CALC-B-2026-0141"},"escenario_asociado":"BASE","veredicto_asociado":"INVERTIR_ESCALONADO",
 "advertencia_H1":false,"en_entregable":true,"estado":"ABIERTO"}
```
