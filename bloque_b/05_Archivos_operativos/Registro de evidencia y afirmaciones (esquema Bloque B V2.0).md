# Esquema de archivo operativo — F2 Registro de evidencia y afirmaciones

**Bloque B · Robot Investor · Versión óptima V2.0 · 03/11/2026** · Subordinado al Documento 0 del Bloque B óptima V2.0 (ante discrepancia, manda el Documento 0).

---

## 1. Propósito

F2 conserva cada pieza de **evidencia** (EVD-B), cada **afirmación** (CLM-B), cada **declaración de datos de entrada** (DAT-B) y cada **discrepancia entre fuentes** (DSC-B) que el Bloque B usa, con su fuente raíz, su cadena raíz→derivada, sus fechas normalizadas (fenómeno, publicación, recuperación, revisión, «conocible desde»), su dirección respecto de la afirmación, su **etiqueta epistémica** y su **clase de cifra**. Mantiene además la sección **«Alertas de procedencia»** (fuentes retiradas, manipulación detectada, herencias del Bloque A no confirmadas).

Es la base de R9 (toda afirmación enlaza con evidencia; toda cifra procede de CALC-B o de un DAT-B con fuente y fecha), R16 (etiquetado epistémico), PA1 (corroboración: dos raíces independientes A/B o una primaria A), PA6 (discrepancias), PC3 (datos del candidato con DAT-B), R31 (la herencia del Bloque A se re-verifica) y del control sin fuga de información del Evaluador y del Vigía.

**No es**: una copia de las fuentes (solo extractos mínimos con cita, Anexo A), un registro de referencias bibliográficas (F7–F9) ni un archivo de conclusiones del bloque (F3).

## 2. Propietario, lectores y contratos

| Aspecto | Contenido |
|---|---|
| Propietario de escritura | AG-B15 Curador de Evidencia (único; con varias instancias, escritura serializada por clave de hash, 4.5) |
| Lectores | Plano P2 (AG-B02 a AG-B17), AG-B01 (respuestas N0), AG-B21 Orquestador, AG-B22 Auditor, AG-B23 Evaluador |
| Contrato de entrada | CT-B-15 (especialistas, Seleccionador, Prospectiva, Contrarias, Buscador y Documentadores → Curador), incluido el tipo `fuente_retirada` (13.4) |
| Herramientas | HT-02 (estado HTTP, hash de contenido, copia archivada, retractaciones), HT-06 (deduplicación e índice), HT-09 (lee F2 para G3) |

## 3. Reglas

1. **Ingesta como dato** (R12): el contenido entra en cuarentena; ninguna instrucción incrustada se ejecuta. Si se detecta, la pieza lleva `incidencia_manipulacion` y se anota en «Alertas de procedencia»; el Orquestador la registra en HA al recorrer F2.
2. **Deduplicación** por hash exacto del extracto normalizado y por similitud; el duplicado se anota en la pieza canónica y no abre entrada nueva.
3. **Raíces independientes**: toda pieza derivada apunta a su `raiz_evd_id`. Dos raíces no son independientes si comparten origen documental, propiedad editorial, cadena de sindicación o la misma nota de prensa corporativa; ante duda, dependientes. Una fuente no registrada en F7–F9 cuenta como «C provisional» (PA1).
4. **Etiqueta epistémica en la afirmación, no en el párrafo** (R16; 8.9): [HECHO] solo si es verificable en fuentes registradas, con fecha y desacuerdo mínimo; [INTERPRETACIÓN] para la inferencia razonada, toda proyección anclada en datos y **toda cifra de consenso de terceros**; [ESPECULACIÓN] sin anclaje suficiente. Lo que no admite etiqueta no entra en un entregable.
5. **Clase de cifra** obligatoria en toda cifra relevante: `determinista` · `estimacion_estadistica` · `juicio_experto`.
6. **Declaración de datos de entrada** (DAT-B; 8.9): todo conjunto que alimente una nota o un cálculo la lleva completa; sin declaración completa, el dato **no sostiene cifras críticas** (el Curador marca `apta_cifra_critica = false`).
7. **Protocolo de discrepancias** (DSC-B; 8.9): identificar, clasificar la causa, buscar la fuente primaria si es crítica (CT-B-11 del agente que la detecta), evaluar la relevancia de cada explicación, registrar la no resuelta con ambas posiciones y reflejar la incertidumbre en la premisa. Nunca se esconde tras la fuente que conviene.
8. **Herencia no es evidencia** (R31): las afirmaciones, CLM-, CALC- y PRG- del `paquete_para_bloque_B` entran como **pistas** (`origen_heredado`) con `estado_reverificacion = PENDIENTE`; solo pueden etiquetarse [HECHO] tras confirmarse con fuentes propias. Los identificadores del Bloque A se conservan como referencia, nunca como identificadores del Bloque B (Anexo C).
9. **Normalización temporal** obligatoria para datos, cifras y series; `conocible_desde` siempre (filtro sin fuga para la evaluación, el backtesting y el Vigía, 6.2.9).
10. **Append-only**: los cambios de verificación, confianza o estado son entradas nuevas del `historial`; las piezas refutadas o con fuente retirada se conservan.
11. **Fuente retirada** (R25; 5.2.3): cuando un propietario de F7–F9 borra una referencia que sustenta EVD-B, el Curador marca la pieza `FUENTE_RETIRADA`, lo anota en «Alertas de procedencia» y lo comunica al Director en su siguiente retorno; si la pieza sostiene una REC-B vigente, el Vigía lo tiene en cuenta en su ronda.
12. **Objeción fuerte sin resolver**: la afirmación afectada no puede tener confianza `establecido`; pasa a `en disputa`.
13. **Extractos mínimos**: cita breve entre comillas o referencia precisa; nunca la obra íntegra (Anexo A, retención).

## 4. Formato de entrada

### 4.1 Afirmación (CLM-B)

| Campo | Tipo | Oblig. | Valores / formato | Descripción |
|---|---|---|---|---|
| `clm_id` | Identificador | Sí | `CLM-B-AAAA-NNNN` | Clave |
| `afirmacion` | Texto | Sí | Concreta, verificable, fechable | Enunciado |
| `etiqueta_epistemica` | Enumerado | Sí | HECHO · INTERPRETACION · ESPECULACION | Se publica como [HECHO], [INTERPRETACIÓN], [ESPECULACIÓN] |
| `clase_cifra` | Enumerado | Si contiene cifra | determinista · estimacion_estadistica · juicio_experto | 8.8 (2) |
| `tipo_afirmacion` | Enumerado | Sí | HECHO · DATO · ANALISIS · OPINION · PREVISION · CONSENSO · RUMOR · PRONOSTICO_FUENTE | Naturaleza |
| `dimension` | Enumerado | Sí | D1…D12 · SELECCION · REGIMEN | Dimensión de 8.2 o uso transversal |
| `ambito` | Objeto | Sí | `{pet_id, mkt_id}` | Petición y ficha de Biblioteca |
| `objeto` | Lista | No | REC-B · CAND-B · HIP-B · PRG-B · premisa | A qué sostiene |
| `evidencias` | Lista | Sí | `{evd_id, direccion}` | Piezas que la sostienen, matizan o contradicen |
| `dat_ids` / `calc_ids` | Listas | Si contiene cifra | DAT-B / CALC-B | Origen de la cifra (R9) |
| `raices_independientes` | Entero | Sí | Calculado | Raíces independientes favorables |
| `pa1_cumple` | Booleano | Sí | 2 raíces A/B independientes o 1 primaria A | Corroboración mínima |
| `nivel_confianza` | Enumerado | Sí | establecido · probable · especulativo · en disputa | Vocabulario de confianza |
| `discrepancias` | Lista | No | DSC-B | Abiertas o registradas |
| `origen_heredado` | Objeto | Si procede del Bloque A | `{opp_id_A, ref_A (CLM-/CALC-/PRG- del Bloque A), estado_reverificacion PENDIENTE·CONFIRMADA·REFUTADA·SIN_VERIFICAR, evd_reverificacion[]}` | R31; alimenta «qué se confirmó o refutó» del informe técnico |
| `pronostico_fuente` | Objeto | Si PRONOSTICO_FUENTE | `{ref_id, variable, serie_ht01, fecha_objetivo, umbral_o_rango, direccion, probabilidad, fecha_emision}` | Para que el Evaluador mida la exactitud de fuentes de F9 |
| `historial` | Lista append-only | Sí | `{fecha, cambio, motivo, pet_id, run_id, agente}` | — |

### 4.2 Evidencia (EVD-B)

| Campo | Tipo | Oblig. | Valores / formato | Descripción |
|---|---|---|---|---|
| `evd_id` | Identificador | Sí | `EVD-B-AAAA-NNNN` | Clave |
| `clm_ids` | Lista | Sí | CLM-B | Afirmaciones a las que sirve |
| `direccion` | Enumerado | Sí | FAVORABLE · CONTRARIA · NEUTRA · AMBIGUA | Por par afirmación-evidencia si difiere |
| `ref_id` | Identificador | Sí | Ficha de F7 (MBA-, ANA-DOC-…), F8 (MBM-, DOC-MOT-…), F9 (MBF-, RF-…), serie HT-01 o `NO_REGISTRADA` | Fuente |
| `nivel_fuente` | Enumerado | Sí | A · B · C · D · C_PROVISIONAL | Nivel Q de la ficha; no registrada = C provisional |
| `url_canonica` / `copia_archivada` | URL | Sí / si existe | — | Localización |
| `identificador_documental` | Texto | Sí | DOI, expediente, página, tabla, sección | Localización estable |
| `extracto` | Texto | Sí | Cita mínima | Nunca la obra íntegra |
| `tipo_fuente` | Enumerado | Sí | PRIMARIA · SECUNDARIA · TERCIARIA | Proximidad al hecho |
| `grado_independencia` | Enumerado | Sí | RAIZ · DERIVADA · COMENTARIO | Posición en la cadena |
| `raiz_evd_id` | Identificador | Sí si no es RAIZ | EVD-B o «no identificada» con motivo | — |
| `hash_contenido` | Texto | Sí | SHA-256 del extracto normalizado | Deduplicación |
| `duplicados` | Lista | No | `{url, hash, fecha}` | — |
| `estado_verificacion` | Enumerado | Sí | Sección 5 | — |
| `limitaciones` | Texto | Sí | — | Muestra, conflicto de interés, autodeclaración, promoción comercial |
| `incidencia_manipulacion` | Objeto | No | `{tipo INSTRUCCION_INCRUSTADA·FUENTES_COORDINADAS·DATO_FABRICADO·CAMPANA_REDES·VOLUMEN_LAVADO·PROMOCION_BAJA_CAPITALIZACION, detalle}` | R12; 17.5 |
| `aportada_por` | Objeto | Sí | `{agente, msg_id_ct15, pet_id}` | — |
| **Normalización temporal** | | | | |
| `fecha_fenomeno` / `periodo_datos` | Fecha / texto | Sí en datos | ISO 8601 / «2026-T3» | — |
| `fecha_publicacion` / `fecha_recuperacion` | Fecha-hora | Sí | ISO 8601 con zona | — |
| `fecha_revision_fuente` / `vintage` | Fecha / texto | Si aplica | — | Series revisables |
| `es_primera_publicacion` | Booleano | Sí en datos macro | — | Original frente a revisado |
| `conocible_desde` | Fecha-hora | Sí | = publicación salvo embargo o retraso declarado | Filtro sin fuga |
| `unidad` / `divisa` / `conversion` | Texto / ISO 4217 / objeto | Sí en cifras | `{de, a, tipo, fecha, fuente}` | — |
| `historial` | Lista append-only | Sí | `{fecha, cambio, motivo, run_id, agente}` | — |

### 4.3 Declaración de datos de entrada (DAT-B)

| Campo | Tipo | Oblig. | Valores / formato |
|---|---|---|---|
| `dat_id` | Identificador | Sí | `DAT-B-AAAA-NNNN` |
| `conjunto` | Texto | Sí | Descripción (p. ej., «márgenes EBIT de 38 emisores del universo RV, 2016–2025») |
| `procedencia` | Objeto | Sí | `{ref_f9 (ficha), serie_ht01, conector, credencial_ref (alias, si lo hay)}` |
| `fecha_extraccion` | Fecha-hora | Sí | — |
| `periodo` / `frecuencia` | Texto / enumerado | Sí | DIARIA · SEMANAL · MENSUAL · TRIMESTRAL · ANUAL · IRREGULAR |
| `version` | Enumerado | Sí | ORIGINAL · REVISADA · MIXTA (declarada) |
| `transformaciones` | Lista | Sí | Paso a paso (deflactar, convertir divisa, agregar, ajustar por dividendos…) |
| `comprobaciones` | Objeto | Sí | `{unidades_divisas, periodos, faltantes, atipicos, nominal_real, duplicados, previsiones_separadas, zona_horaria_calendario, sesgo_supervivencia, sesgo_disponibilidad, retraso_publicacion, riesgo_anticipacion}`, cada una `OK · CORREGIDO · LIMITACION · NO_APLICA (motivo)` |
| `fecha_corte_resultante` | Fecha | Sí | La más restrictiva del conjunto |
| `completa` | Booleano | Sí | Todas las comprobaciones resueltas |
| `apta_cifra_critica` | Booleano | Sí | false si `completa` = false (8.9) |
| `usada_por` | Lista | Sí | CLM-B, CALC-B, CAND-B |
| `antiguedad_vs_maximo` | Objeto | Sí en datos de mercado | `{antiguedad_dias, maximo_anexo_A, horizonte, dentro_frescura sí/no, justificacion}` (PA2, PC3) |

### 4.4 Discrepancia (DSC-B)

| Campo | Tipo | Oblig. | Valores / formato |
|---|---|---|---|
| `dsc_id` | Identificador | Sí | `DSC-B-AAAA-NNNN` |
| `dato_en_conflicto` | Texto | Sí | Identificado con precisión (variable, periodo, unidad) |
| `posiciones` | Lista | Sí | `{evd_id, valor, fuente, nivel}` (al menos dos) |
| `causa` | Enumerado | Sí | fechas · definiciones · metodologia · estimacion |
| `critica` | Booleano | Sí | Afecta a una premisa central o a un insumo de S decisivo |
| `busqueda_primaria` | Objeto | Si crítica | `{msg_id_ct11, resultado}` |
| `relevancia_por_explicacion` | Texto | Sí | Para la pregunta decisiva |
| `estado` | Enumerado | Sí | ABIERTA · RESUELTA · REGISTRADA_NO_RESUELTA |
| `reflejo_en_premisa` | Objeto | Si no resuelta | `{premisa, tratamiento PREDOMINIO_RAZONADO·CAUTELA·CONDICION_INVALIDACION, texto}` (PA6) |

### 4.5 Alertas de procedencia (sección del archivo)

Lista append-only de `{fecha, tipo FUENTE_RETIRADA·MANIPULACION·HERENCIA_REFUTADA·CONTENIDO_CAMBIADO·RETRACTACION, ref_id, evd_ids afectadas, clm_ids afectadas, rec_ids vigentes afectadas, comunicado_a, estado}`.

## 5. Estados y transiciones (evidencia)

| Desde | Hacia | Condición |
|---|---|---|
| (ingesta) | PENDIENTE | Alta tras deduplicación |
| PENDIENTE | EN_VERIFICACION | HT-02 y revisión |
| EN_VERIFICACION | VERIFICADA · VERIFICADA_CON_RESERVAS · NO_VERIFICABLE · REFUTADA | Resultado |
| VERIFICADA · VERIFICADA_CON_RESERVAS | REFUTADA | Evidencia posterior decisiva o retractación |
| cualquiera | FUENTE_RETIRADA | Baja de la referencia en F7–F9 (CT-B-15 `fuente_retirada`) |
| FUENTE_RETIRADA | VERIFICADA_CON_RESERVAS | Fuente sustituta equivalente registrada |

Confianza de la afirmación: `establecido` (hecho verificado con raíces independientes y PA1 cumplida), `probable`, `especulativo`, `en disputa`. La vigente es la última del historial. DAT-B: `INCOMPLETA` → `COMPLETA`. DSC-B: `ABIERTA` → `RESUELTA` · `REGISTRADA_NO_RESUELTA`.

## 6. Índices de consulta

| Índice | Clave | Uso |
|---|---|---|
| Por hash | `hash_contenido` | Deduplicación antes del alta |
| Por afirmación | `clm_id` → EVD-B | Raíces y PA1; G3 |
| Por raíz | `raiz_evd_id` | Cadena raíz→derivada |
| Por referencia | `ref_id` | Propagación de bajas de F7–F9 |
| Por conocibilidad | `conocible_desde` | Evaluación, backtesting y Vigía sin fuga |
| Por dirección | `direccion` = CONTRARIA | Sesgo de confirmación (Auditor; hipótesis competidoras) |
| Por etiqueta y clase | `etiqueta_epistemica`, `clase_cifra` | G3 y foco 2 del Auditor |
| Herencias pendientes | `origen_heredado.estado_reverificacion` | Informe técnico (sección 3); R31 |
| Declaraciones incompletas | `DAT-B.completa` = false | PA2, PC3, G3 |
| Discrepancias abiertas | `DSC-B.estado` | PA6 |
| Por candidato | `usada_por` CAND-B | PC3, PC7 |

## 7. Ejemplo ficticio

> **EJEMPLO FICTICIO — no es una entrada real.** Datos, URL e identificadores inventados.

```json
{"dat_id":"DAT-B-2026-0031","conjunto":"Ingresos por segmento de 41 emisores del universo RV (empaquetado avanzado), ejercicios 2021–2025",
 "procedencia":{"ref_f9":"MBF-0000","serie_ht01":null,"conector":"documentacion_corporativa_gratuita","credencial_ref":null},
 "fecha_extraccion":"2026-11-10T08:40:00+01:00","periodo":"2021–2025","frecuencia":"ANUAL","version":"ORIGINAL",
 "transformaciones":["conversión a EUR con el tipo medio anual del BCE","reclasificación de segmentos a la delimitación del ámbito (D1)"],
 "comprobaciones":{"unidades_divisas":"CORREGIDO","periodos":"OK","faltantes":"LIMITACION","atipicos":"OK","nominal_real":"NO_APLICA (comparación de proporciones)",
   "duplicados":"OK","previsiones_separadas":"OK","zona_horaria_calendario":"OK","sesgo_supervivencia":"OK (incluye 3 deslistados)",
   "sesgo_disponibilidad":"LIMITACION","retraso_publicacion":"OK","riesgo_anticipacion":"OK"},
 "fecha_corte_resultante":"2026-11-07","completa":true,"apta_cifra_critica":true,"usada_por":["CALC-B-2026-0112","CAND-B-2026-0044"],
 "antiguedad_vs_maximo":null}
```
