# Esquema de archivo operativo — F4 Registro de pronósticos congelados

**Bloque A · Robot Investor · Versión óptima V4.0 · 01/11/2026 · actualizado V5.1 (03/11/2026)** · Subordinado al Documento 0 óptima V5.1. Cambios V5.1: horizonte H5 (décadas) con solo banda verbal e hitos intermedios HIT- (4.3); `es_principal`; estado de los pronósticos H5 derivado de sus hitos (5.1); doce tipos de activo en `clase`.

---

## 1. Propósito

F4 conserva cada **pronóstico verificable** (PRG-) que el bloque emite, congelado en su fecha con su horizonte (H1–H5), su afirmación, su probabilidad interna y su banda (en H5, solo la banda y sus hitos HIT-), su criterio y fecha de resolución y su referencia ingenua; y, cuando vence, su **resolución** y puntuación. Es la base de la evaluación sin fuga de información, de los certificados de horizonte (R13), del historial de aciertos y de la recalibración (sección 12 del Documento 0).

**No es editable hacia atrás** (R11): nadie retoca un pronóstico congelado. Incluye los pronósticos de finalistas no seleccionadas (`en_informe: false`) para medir falsos negativos.

## 2. Propietario, lectores y contratos

| Aspecto | Contenido |
|---|---|
| Escritura de altas | AG-10 Analista de Prospectiva y Horizontes (único autor de altas, tras la orden de congelación del Analizador, posterior a G3) |
| Escritura de resolución | AG-20 Evaluador, **exclusivamente** en el bloque `resolucion` y en `estado` (ABIERTO → RESUELTO/NO_RESOLUBLE) |
| Lectores | Todos los agentes |
| Contratos | CT-12 (propuesta y orden de congelación), CT-19 (resultados), CT-09 (puntuaciones del Motor, MC-10) |
| Herramientas | HT-01 (vintages), HT-05 (recordatorios de resolución), HT-09 (G3-CON-13) |

## 3. Reglas

1. **Congelación**: la entrada de alta no se modifica jamás. Una corrección es un PRG nuevo con `version_de` = PRG anterior; **el original sigue evaluándose** en su fecha (impide «corregir» los pronósticos que van mal) y la versión nueva se evalúa desde su propia congelación.
2. **Separación de escritura**: los campos de alta los escribe solo Prospectiva; los de resolución solo el Evaluador. Cualquier otra escritura es incidencia Material.
3. **Probabilidad**: `prob_interna` se registra siempre (en rejilla de 5 puntos, 5–95 %; 15–85 % sin certificado), **salvo en H5**, donde se registra solo la banda verbal; `prob_publicada` solo con certificado vigente (`certificado_ref`), que H5 nunca obtiene (R13).
3 bis. **H5 (V5.1)**: todo PRG H5 lleva ≥ 3 hitos HIT- (el primero a ≤ 12 meses, ≤ 24 meses entre hitos), dados de alta en la misma congelación; cada hito es un pronóstico ordinario de su propio horizonte (con su `prob_interna`), se resuelve en su fecha y es lo que se evalúa (12.1). El PRG H5 no se puntúa con Brier ni log-score antes de su vencimiento.
4. **Sin fuga**: nada en el alta puede ser posterior a `fecha_congelacion`; el nivel de referencia respeta la antigüedad máxima de PS2.
5. **Universo completo**: todos los PRG se resuelven, incluidos los de opciones cerradas, invalidadas o descartadas por el Broker. La invalidación de una opción no anula sus PRG.
6. **NO_RESOLUBLE** solo con motivo (dato inexistente tras fallback, afirmación ambigua, variable discontinuada); se cuenta y se publica.
7. Conservación indefinida.

## 4. Formato de entrada

### 4.1 Campos de alta (Prospectiva)

| Campo | Tipo | Oblig. | Valores / formato | Descripción |
|---|---|---|---|---|
| `prg_id` | Identificador | Sí | `PRG-AAAA-NNNN` | Clave |
| `version_de` | Identificador | No | PRG- anterior | Corrección |
| `opp_id` / `tnd_ids` | Identificadores | Sí / No | OPP- / TND- | Vínculos |
| `run_id` | Identificador | Sí | RUN- | Ejecución |
| `clase` | Enumerado | Sí | RV · RF · DIV · MP · IDX · FON · DER · INM · CRI · ALT · MON · TCV | Celda |
| `horizonte` | Enumerado | Sí | H1 · H2 · H3 · H4 · H5 | Celda (aplicable según 8.3 vigente; un hito HIT- lleva el horizonte de su propio plazo) |
| `es_principal` | Booleano | Sí (V5.1) | — | Pronóstico del horizonte principal de la opción (8.3) |
| `estrategia` | Texto codificado | Sí | Lente de la clase (p. ej. RV-REVISIONES, RF-CARRY, DIV-PPA) | Celda de diagnóstico |
| `tipo_opcion` | Enumerado | Sí | Tipos de 2.4 | Celda de diagnóstico |
| `tipo_pronostico` | Enumerado | Sí | DIRECCIONAL · RELATIVO · RANGO · UMBRAL · EVENTO · CUANTIL | Forma |
| `afirmacion` | Texto | Sí | Inequívoca | Lo que se pronostica |
| `variable` | Objeto | Sí | `{serie_ht01, descripcion, tipo_rentabilidad PRECIO·TOTAL, divisa}` | Qué se mide |
| `nivel_referencia` | Objeto | Sí | `{valor, fecha_hora, fuente}` | Punto de partida |
| `umbral` / `rango` / `cuantiles` | Número / par / lista | Según tipo | — | Condición |
| `fecha_congelacion` | Fecha-hora | Sí | ISO 8601 con zona | Momento de congelación |
| `fecha_resolucion` | Fecha | Sí | ISO 8601 | Cuándo se resuelve |
| `criterio_resolucion` | Texto | Sí | Convención exacta (cierre oficial, primera publicación, fixing) | Cómo se resuelve |
| `fuente_resolucion` | Texto | Sí | Serie HT-01 o fuente oficial | — |
| `regla_fallback` | Texto | Sí | Fuente alternativa, festivos, revisiones | — |
| `banda_verbal` | Enumerado | Sí | MUY_PROBABLE · MAS_PROBABLE_QUE_NO · INCIERTO · POCO_PROBABLE · MUY_POCO_PROBABLE | Correspondencia fija (80–95 %, 60–75 %, 45–55 %, 25–40 %, 5–20 %) |
| `prob_interna` | Número o null | Sí | 0,05–0,95 (rejilla 0,05); null en H5 | Siempre registrada salvo en H5 |
| `prob_publicada` | Número o null | Sí | null salvo certificado | R13 |
| `certificado_ref` | Identificador | Si `prob_publicada` | CERT- | — |
| `metodo` | Texto | Sí | Método o combinación (method_id del Catálogo) | Celda de certificación |
| `fuentes_clave` | Lista | No | REF- | Celda de diagnóstico por fuente |
| `referencia_ingenua` | Objeto | Sí | `{tipo PASEO_ALEATORIO·ULTIMO_VALOR·MEDIA_HISTORICA·TASA_BASE·COMPRAR_Y_MANTENER·IMPLICITA_MERCADO, valor_o_prob, calc_id}` | Calculada sin fuga |
| `escenario_asociado` | Texto | Sí | BASE · FAVORABLE · ADVERSO | — |
| `en_informe` | Booleano | Sí | — | Publicado o no |
| `estado` | Enumerado | Sí | ABIERTO al alta | — |

### 4.3 Campos propios de H5 y de sus hitos (V5.1)

| Campo | Tipo | Oblig. | Valores / formato | Descripción |
|---|---|---|---|---|
| `hit_ids` | Lista | Sí en H5 | ≥ 3 `HIT-AAAA-NNNN` | Hitos de la senda del PRG H5 |
| `tesis_estructural` | Texto | Sí en H5 | — | Tesis de largo plazo que sostiene el H5 |
| `prg_padre` | Identificador | Sí en un hito | PRG- H5 | Vínculo del hito con su pronóstico H5 |
| `es_hito` / `necesario` | Booleanos | Sí en un hito | — | Un hito necesario fallado invalida el H5 |
| (resto de campos) | — | Sí en un hito | Los de 4.1 | Fecha, indicador (`variable`), criterio y fuente de resolución, banda y `prob_interna` propias |

### 4.2 Campos de resolución (exclusivos del Evaluador)

| Campo | Tipo | Oblig. al resolver | Descripción |
|---|---|---|---|
| `resolucion.fecha_resuelto` | Fecha | Sí | — |
| `resolucion.valor_observado` | Número / texto | Sí (salvo NO_RESOLUBLE) | Con unidad |
| `resolucion.fuente_usada` / `vintage` | Texto | Sí | Serie y versión |
| `resolucion.fallback_aplicado` | Booleano | Sí | — |
| `resolucion.resultado` | Enumerado | Sí | OCURRIDO · NO_OCURRIDO · VALOR (cuantiles) |
| `resolucion.resultado_binario` | 0/1 | Si binario | — |
| `resolucion.puntuaciones` | Objeto | Sí | `{brier, log, brier_ref, log_ref, pinball, error_vs_ingenua}` |
| `resolucion.calc_id` | Identificador | Sí | CALC- del Motor (MC-10) |
| `resolucion.comprobacion_fuga` | Enumerado | Sí | SUPERADA · FALLIDA |
| `resolucion.motivo_no_resoluble` | Texto | Si NO_RESOLUBLE | — |
| `resolucion.corrige_a` | Identificador | Si es corrección | Resolución anterior corregida |

## 5. Estados y transiciones

| Desde | Hacia | Quién | Condición |
|---|---|---|---|
| (alta) | ABIERTO | Prospectiva | Orden de congelación tras G3 |
| ABIERTO | RESUELTO | Evaluador | Dato disponible y resultado calculado |
| ABIERTO | NO_RESOLUBLE | Evaluador | Motivo documentado tras fallback (o 10 días hábiles sin dato) |
| RESUELTO | RESUELTO (corrección) | Evaluador | Nueva entrada de resolución con `corrige_a`; la anterior se conserva |

No existen estados «anulado» ni «invalidado»: la invalidación de una opción no detiene la resolución.

### 5.1 Estado derivado de un pronóstico H5 (V5.1, 12.1)

El Evaluador publica en F6 (no en F4) el estado de cada PRG H5 a partir de sus hitos resueltos: `EN_CURSO_CONFORME` (todos cumplidos, o como mucho uno fallado que no sea el último), `DESVIADO` (dos o más fallados, o el último fallado), `INVALIDADO` (se activa la invalidación o falla un hito `necesario`). Por celda tipo × H5 publica la tasa de hitos cumplidos (P-42 de F10). Al vencer, el PRG H5 se resuelve solo de forma descriptiva.

## 6. Índices de consulta

| Índice | Clave | Uso |
|---|---|---|
| Vencimientos | `fecha_resolucion`, `estado` = ABIERTO | Resolución diaria (HT-05) |
| Celda de decisión | `clase` × `horizonte` | Métricas, recalibración, aplicabilidad |
| Celda de certificación | `clase` × `horizonte` × `metodo` (× `tipo_pronostico`) | Certificados |
| Diagnóstico | `estrategia`, `tipo_opcion`, `fuentes_clave` | Lecciones de nivel A |
| Por oportunidad | `opp_id` | Seguimiento de vigentes; historial de aciertos |
| Publicados / no publicados | `en_informe` | Falsos negativos; sesgo de selección |
| Por banda | `banda_verbal` | Sobreconfianza por banda |
| Versiones | `version_de` | Trazabilidad de correcciones |
| Hitos H5 (V5.1) | `prg_padre`, `fecha_resolucion` | Recordatorios de HT-05; estado del H5 |

## 7. Ejemplo ficticio

> **EJEMPLO FICTICIO — no es una entrada real.** Datos, series e identificadores inventados.

```json
{"prg_id":"PRG-2026-0001","version_de":null,"opp_id":"OPP-2026-0001","tnd_ids":["TND-2026-0001"],"run_id":"RUN-2026-0001",
 "clase":"RV","horizonte":"H3","estrategia":"RV-REVISIONES","tipo_opcion":"TEMATICA","tipo_pronostico":"RELATIVO",
 "afirmacion":"La rentabilidad total en EUR del índice temático IDX-FICT-001 superará a la del índice mundial de renta variable entre el 2026-11-09 y el 2027-05-07",
 "variable":{"serie_ht01":"IDX-FICT-001 vs IDX-FICT-MUNDO","descripcion":"diferencia de rentabilidad total","tipo_rentabilidad":"TOTAL","divisa":"EUR"},
 "nivel_referencia":{"valor":"cierres del 2026-11-06","fecha_hora":"2026-11-06T17:35:00+01:00","fuente":"HT-01"},
 "fecha_congelacion":"2026-11-09T06:30:00+01:00","fecha_resolucion":"2027-05-07",
 "criterio_resolucion":"Cierre oficial del 2027-05-07 (o sesión hábil anterior) de ambas series de rentabilidad total en EUR","fuente_resolucion":"HT-01",
 "regla_fallback":"Proveedor alternativo de HT-01; si ninguno, NO_RESOLUBLE","banda_verbal":"MAS_PROBABLE_QUE_NO","prob_interna":0.65,"prob_publicada":null,"certificado_ref":null,
 "metodo":"MET-RV-REV-01","referencia_ingenua":{"tipo":"TASA_BASE","valor_o_prob":0.47,"calc_id":"CALC-2026-0013"},"escenario_asociado":"BASE","en_informe":true,"estado":"ABIERTO",
 "resolucion":null}
```
