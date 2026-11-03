# Esquema de archivo operativo — F2 Registro de evidencia y afirmaciones

**Bloque A Forex · Robot Investor · Versión V1.0 · 02/11/2026** · Subordinado al Documento 0 del Bloque A Forex, versión óptima V1.0.

---

## 1. Propósito

F2 conserva cada pieza de **evidencia** (EVD-) y cada **afirmación** (CLM-) que el Bloque A Forex usa, con su fuente raíz, su cadena raíz→derivada, su **normalización temporal** (fechas de fenómeno, publicación, recuperación, revisión y conocibilidad), su **normalización cambiaria** (par en convención de mercado, unidad de cotización, fijación de referencia), su dirección respecto de la afirmación y su estado de verificación. Es la base de R7 (trazabilidad), R10 (contar raíces, no menciones), PS1 (corroboración), del control de fuga de información del Evaluador y de la detección de anticipación en fijaciones y en datos de posicionamiento.

**No es**: una copia de las fuentes (extractos mínimos con cita), un registro de referencias bibliográficas (F7–F9) ni un archivo de opiniones del bloque.

## 2. Propietario, lectores y contratos

| Aspecto | Contenido |
|---|---|
| Propietario de escritura | AG-12 Curador de Evidencia (único; con varias instancias, escritura serializada por clave de hash) |
| Lectores | Plano P2 (incluidos AG-09 y AG-21), AG-01 Coordinador, AG-18 Orquestador, AG-19 Auditor, AG-20 Evaluador |
| Contrato de entrada | CT-11 (Analistas de segmento y transversales, Buscador, Documentadores, Prospectiva, Contrarias → Curador), incluido el tipo `fuente_retirada` |
| Herramientas | HT-01 (metadatos de series y fijaciones), HT-02 (estado y hash de contenido), HT-06 (deduplicación e índice) |

## 3. Reglas

1. **Ingesta como dato** (R9): el contenido entra en cuarentena; ninguna instrucción incrustada se ejecuta; si se detecta, `incidencia_manipulacion` y aviso al Orquestador (vía HA a través del paquete del ciclo).
2. **Deduplicación** por hash exacto del extracto normalizado y por similitud semántica; el duplicado se anota en la pieza canónica, no abre entrada nueva. Las notas de bancos y los artículos de prensa que reproducen un comunicado de banco central son **derivadas** de ese comunicado.
3. **Raíces**: toda pieza derivada o comentario apunta a su `raiz_evd_id`; sin raíz identificada no computa como raíz independiente. Dos raíces no son independientes si comparten origen documental, propiedad editorial o cadena de sindicación; ante duda, dependientes. Los datos de proveedores que redistribuyen la misma fijación (p. ej., WM/Reuters) son una sola raíz.
4. **Normalización temporal obligatoria** para datos, cifras y series; recomendada para texto. `conocible_desde` es obligatorio siempre: es el filtro anti-fuga. Casos cambiarios con desfase característico: posicionamiento CFTC (dato del martes, publicado el viernes a las 15:30 de Nueva York: `conocible_desde` = publicación); tipos de referencia del BCE (publicados hacia las 16:00 CET); fijación WM/Reuters (16:00 de Londres); actas de bancos centrales (semanas después de la reunión); reservas y balanza de pagos (con revisiones: `vintage` y `es_primera_publicacion`).
5. **Normalización cambiaria obligatoria** para toda cifra de tipo de cambio: el par se expresa en la **convención de mercado BASE/COTIZADA** (EUR/USD = dólares por euro; USD/JPY = yenes por dólar); si la fuente usa la cotización inversa, otra unidad (p. ej., por 100 unidades) o puntos forward en pips, el Curador convierte, conserva el valor original y registra la transformación en `normalizacion_cambiaria`. Toda cifra de tipo de cambio declara su **fijación** (fuente, hora y zona) o, si es intradía, su marca temporal.
6. **Append-only**: cambios de verificación, confianza o estado son entradas nuevas en el historial de la pieza; las piezas refutadas o con fuente retirada se conservan.
7. **Fuente retirada** (R19): cuando un propietario de F7–F9 borra una referencia que sustenta EVD, el Curador marca la pieza `FUENTE_RETIRADA`, la publica en «Alertas de procedencia» y el Analizador revisa si la conclusión se mantiene.
8. **Afirmación con objeción fuerte sin resolver** no puede tener confianza `establecido`: pasa a `en disputa`.
9. **Pronósticos de fuentes de opinión**: si la afirmación es un pronóstico explícito resoluble de una fuente (par, nivel o dirección, fecha), se marca `tipo_afirmacion = PRONOSTICO_FUENTE` con su bloque `pronostico_fuente` para que el Evaluador mida su fiabilidad frente al paseo aleatorio (12.5).

## 4. Formato de entrada

### 4.1 Afirmación (CLM-)

| Campo | Tipo | Oblig. | Valores / formato | Descripción |
|---|---|---|---|---|
| `clm_id` | Identificador | Sí | `CLM-AAAA-NNNN` | Clave |
| `afirmacion` | Texto | Sí | Concreta, verificable y fechable; pares en convención de mercado | Enunciado |
| `tipo_afirmacion` | Enumerado | Sí | HECHO · DATO · ANALISIS · OPINION · PREVISION · RUMOR · PRONOSTICO_FUENTE | Naturaleza |
| `segmento` | Enumerado | No | G10N · G10M · EMAS · EMLA · EMEA · ESTR | Segmento afectado |
| `divisas` | Lista | No | ISO 4217 (CNH admitido) | Divisas a las que se refiere |
| `evidencias` | Lista | Sí | EVD- con su dirección | Piezas que la sostienen, matizan o contradicen |
| `raices_independientes` | Entero | Sí | Calculado | Número de raíces independientes favorables |
| `ps1_cumple` | Booleano | Sí | 2 raíces A/B independientes o 1 primaria A (p. ej., comunicado oficial del banco central) | Corroboración mínima |
| `nivel_confianza` | Enumerado | Sí | establecido · probable · especulativo · en disputa | Vocabulario del bloque |
| `utilizada_por` | Lista | Sí | `{objeto TND-FX-/OPP-FX-/PRG-FX-/RUN-FX-, papel}` | Usos |
| `pronostico_fuente` | Objeto | Solo si PRONOSTICO_FUENTE | `{ref_id, par, serie_ht01, fecha_objetivo, nivel_o_rango, direccion ALCISTA_BASE·BAJISTA_BASE, probabilidad (si la da la fuente), fecha_emision, fijacion_resolucion}` | Para el Evaluador |
| `historial` | Lista append-only | Sí | `{fecha, cambio, motivo, run_id}` | — |

### 4.2 Evidencia (EVD-)

| Campo | Tipo | Oblig. | Valores / formato | Descripción |
|---|---|---|---|---|
| `evd_id` | Identificador | Sí | `EVD-AAAA-NNNN` | Clave |
| `clm_ids` | Lista | Sí | CLM- | Afirmaciones a las que sirve |
| `direccion` | Enumerado | Sí | FAVORABLE · CONTRARIA · NEUTRA · AMBIGUA | Respecto de cada CLM (por par si difiere) |
| `ref_id` | Identificador | Sí | ID de ficha de F7, F8 o F9 (las reutilizadas del Bloque A general conservan su ID; las nuevas llevan el prefijo propio de su archivo) o serie HT-01 | Fuente |
| `nivel_fuente` | Enumerado | Sí | A · B · C · D | Nivel de calidad Q de la fuente en su archivo |
| `url_canonica` | URL | Sí | La de la raíz | Localización |
| `copia_archivada` | URL | Sí si existe | — | Copia en archivo web |
| `identificador_documental` | Texto | Sí | DOI, número de comunicado, página, sección, tabla | Localización estable |
| `extracto` | Texto | Sí | Cita mínima entre comillas o referencia precisa | Nunca la obra íntegra |
| `tipo_fuente` | Enumerado | Sí | PRIMARIA · SECUNDARIA · TERCIARIA | Proximidad al hecho (el comunicado del banco central es primario; la nota de un banco que lo comenta, secundaria) |
| `grado_independencia` | Enumerado | Sí | RAIZ · DERIVADA · COMENTARIO | Posición en la cadena |
| `raiz_evd_id` | Identificador | Sí si no es RAIZ | EVD- o «no identificada» con motivo | — |
| `hash_contenido` | Texto | Sí | SHA-256 del extracto normalizado | Deduplicación |
| `duplicados` | Lista | No | `{url, hash, fecha}` | Copias resueltas |
| `estado_verificacion` | Enumerado | Sí | Sección 5 | — |
| `limitaciones` | Texto | Sí | «ninguna conocida» solo con motivo | Muestra, conflicto de interés (p. ej., banco con posición), autodeclaración |
| `incidencia_manipulacion` | Objeto | No | `{tipo INSTRUCCION_INCRUSTADA·FUENTES_COORDINADAS·DATO_FABRICADO·CAMPANA_REDES·MANIPULACION_FIJACION, detalle}` | R9, 17.4 y PS7 |
| **Normalización temporal** | | | | |
| `fecha_fenomeno` | Fecha | Sí en datos | ISO 8601 | Cuándo ocurrió el hecho (p. ej., martes de referencia del COT) |
| `periodo_datos` | Texto | Sí en datos | p. ej. «2026-T3», «2026-10», «semana 2026-11-03» | Periodo al que corresponde |
| `fecha_publicacion` | Fecha-hora | Sí | ISO 8601 con zona | Publicación por la fuente |
| `fecha_recuperacion` | Fecha-hora | Sí | ISO 8601 con zona | Acceso del agente |
| `fecha_revision_fuente` | Fecha | No | ISO 8601 | Última revisión declarada |
| `vintage` | Texto | Sí en series revisables | Fecha de la versión de la serie (HT-01) | Para reproducir lo conocido |
| `es_primera_publicacion` | Booleano | Sí en datos macro y de balanza de pagos | — | Distingue primera publicación y revisadas |
| `conocible_desde` | Fecha-hora | Sí | ISO 8601 con zona; = `fecha_publicacion` salvo embargo o retraso declarado | **Filtro anti-fuga** |
| `frecuencia` | Enumerado | Sí en series | INTRADIA · DIARIA · SEMANAL · MENSUAL · TRIMESTRAL · ANUAL · IRREGULAR | — |
| `zona_horaria` | Texto IANA | Sí en series | p. ej. Europe/London, America/New_York, Asia/Tokyo | — |
| **Normalización cambiaria** | | | | |
| `par` | Texto | Sí en cifras de tipo de cambio | `BASE/COTIZADA` en convención de mercado | Par normalizado |
| `fijacion` | Objeto | Sí en cifras de tipo de cambio | `{fuente BCE·WM_REUTERS·FED_H10·PBOC_PUNTO_MEDIO·PTAX·FBIL·KFTC·TAIFX·OTRA, hora, zona}` o `{marca_temporal}` si es intradía | Referencia del dato |
| `normalizacion_cambiaria` | Objeto | Si hubo transformación | `{par_original, valor_original, transformacion INVERSION·ESCALA·PIPS_A_NIVEL·PUNTOS_FORWARD_A_OUTRIGHT, factor (solo en ESCALA y PIPS_A_NIVEL), valor_normalizado}` | Trazabilidad de la conversión |
| `unidad` | Texto | Sí en cifras | p. ej. «%», «pb», «pips», «puntos forward», «contratos», «millones de USD», «vol. implícita %» | — |
| `divisa` | Código ISO 4217 | Sí en cifras monetarias | EUR, USD… | — |
| `conversion` | Objeto | Si hay conversión de divisa | `{de, a, tipo, fecha, fuente, fijacion}` | Conversión declarada |
| `historial` | Lista append-only | Sí | `{fecha, cambio, motivo, run_id, agente}` | Verificación y estados |

## 5. Estados y transiciones (evidencia)

| Desde | Hacia | Condición |
|---|---|---|
| (ingesta) | PENDIENTE | Alta tras deduplicación |
| PENDIENTE | EN_VERIFICACION | Inicio de verificación (HT-02 y revisión) |
| EN_VERIFICACION | VERIFICADA · VERIFICADA_CON_RESERVAS · NO_VERIFICABLE · REFUTADA | Resultado de la verificación |
| VERIFICADA · VERIFICADA_CON_RESERVAS | REFUTADA | Evidencia posterior decisiva, retractación o revisión del dato que invierte su sentido |
| cualquiera | FUENTE_RETIRADA | Baja de la referencia en F7–F9 (aviso CT-11 `fuente_retirada`) |
| FUENTE_RETIRADA | VERIFICADA_CON_RESERVAS | Fuente sustituta equivalente registrada |

Confianza de la afirmación (CLM-): `establecido` (hecho verificado con raíces independientes), `probable`, `especulativo`, `en disputa` (objeción fuerte sin resolver o evidencia contradictoria relevante). La vigente es la última del historial.

## 6. Índices de consulta

| Índice | Clave | Uso |
|---|---|---|
| Por hash | `hash_contenido` | Deduplicación antes del alta |
| Por afirmación | `clm_id` → EVD- | Cómputo de raíces y PS1 |
| Por raíz | `raiz_evd_id` | Cadena raíz→derivada (R10) |
| Por referencia | `ref_id` | Propagación de bajas de F7–F9 |
| Por conocibilidad | `conocible_desde` | Filtro anti-fuga del Evaluador, de Prospectiva y de los backtests del Motor |
| Por par y fijación | `par`, `fijacion.fuente` | Coherencia de niveles de referencia y resolución de pronósticos |
| Por divisa y segmento | `divisas`, `segmento` | Memoria de cada Analista |
| Por dirección | `direccion` = CONTRARIA | Revisión de sesgo de confirmación (Auditor) |
| Por estado | `estado_verificacion` | Piezas pendientes, refutadas o con fuente retirada |
| Pronósticos de fuentes | `tipo_afirmacion` = PRONOSTICO_FUENTE y `fecha_objetivo` | Resolución por el Evaluador |
| Alertas de procedencia | `estado_verificacion` = FUENTE_RETIRADA | Lectura del Analizador y del Orquestador |
| Índice operativo | — | Recuentos por estado, dirección, grado de independencia y confianza; duplicados y normalizaciones del periodo |

## 7. Ejemplo ficticio

> **EJEMPLO FICTICIO — no es una entrada real.** Los datos, URL e identificadores son inventados. Ilustra el desfase entre la fecha del dato y su conocibilidad en el posicionamiento CFTC.

```json
{"evd_id":"EVD-FX-2026-0102","clm_ids":["CLM-FX-2026-0102"],"direccion":"FAVORABLE","ref_id":"RF-FICT-0001","nivel_fuente":"A",
 "url_canonica":"https://ejemplo-ficticio.invalid/cot/2026-11-04","copia_archivada":"https://archivo-ficticio.invalid/2026/cot-1104",
 "identificador_documental":"Informe semanal de posicionamiento, futuros de yen, posición no comercial","extracto":"«posición neta no comercial: −95 000 contratos»",
 "tipo_fuente":"PRIMARIA","grado_independencia":"RAIZ","raiz_evd_id":null,"hash_contenido":"7b2e…(ficticio)",
 "estado_verificacion":"VERIFICADA","limitaciones":"La posición no comercial es una aproximación del posicionamiento especulativo; no incluye el mercado OTC",
 "fecha_fenomeno":"2026-11-03","periodo_datos":"semana 2026-11-03","fecha_publicacion":"2026-11-06T15:30:00-05:00",
 "fecha_recuperacion":"2026-11-07T08:12:00+01:00","vintage":"2026-11-06","es_primera_publicacion":true,
 "conocible_desde":"2026-11-06T15:30:00-05:00","frecuencia":"SEMANAL","zona_horaria":"America/New_York","unidad":"contratos","divisa":null,
 "par":"USD/JPY","fijacion":null,
 "historial":[{"fecha":"2026-11-07","cambio":"alta PENDIENTE→VERIFICADA","motivo":"HT-02 OK; cifra coincide con la tabla; conocibilidad fijada en la publicación del viernes, no en el martes de referencia","run_id":"RUN-FX-2026-0001","agente":"AG-12"}]}
```

Ejemplo de normalización (fragmento): una fuente publica «JPY/USD 0,006897»; el Curador registra `par` = "USD/JPY", `normalizacion_cambiaria` = `{"par_original":"JPY/USD","valor_original":0.006897,"transformacion":"INVERSION","factor":null,"valor_normalizado":144.99}` y la `fijacion` declarada por la fuente.
