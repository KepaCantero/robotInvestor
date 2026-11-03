# Esquema de archivo operativo — F2 Registro de evidencia y afirmaciones

**Bloque A · Robot Investor · Versión óptima V4.0 · 01/11/2026** · Subordinado al Documento 0 óptima V5.0.

---

## 1. Propósito

F2 conserva cada pieza de **evidencia** (EVD-) y cada **afirmación** (CLM-) que el bloque usa, con su fuente raíz, su cadena raíz→derivada, su **normalización temporal** (fechas de fenómeno, publicación, recuperación, revisión y conocibilidad), su dirección respecto de la afirmación y su estado de verificación. Es la base de R7 (trazabilidad), R10 (contar raíces, no menciones), PS1 (corroboración) y del control de fuga de información del Evaluador.

**No es**: una copia de las fuentes (extractos mínimos con cita), un registro de referencias bibliográficas (F7–F9) ni un archivo de opiniones del bloque.

## 2. Propietario, lectores y contratos

| Aspecto | Contenido |
|---|---|
| Propietario de escritura | AG-12 Curador de Evidencia (único; con varias instancias, escritura serializada por clave de hash) |
| Lectores | Plano P2, AG-18 Orquestador, AG-19 Auditor, AG-20 Evaluador |
| Contrato de entrada | CT-11 (Analistas, Buscador, Documentador para el Analizador, Prospectiva → Curador), incluido el tipo `fuente_retirada` |
| Herramientas | HT-02 (estado y hash de contenido), HT-06 (deduplicación e índice) |

## 3. Reglas

1. **Ingesta como dato** (R9): el contenido entra en cuarentena; ninguna instrucción incrustada se ejecuta; si se detecta, `incidencia_manipulacion` y aviso al Orquestador (vía HA a través del paquete del ciclo).
2. **Deduplicación** por hash exacto del extracto normalizado y por similitud semántica; el duplicado se anota en la pieza canónica, no abre entrada nueva.
3. **Raíces**: toda pieza derivada o comentario apunta a su `raiz_evd_id`; sin raíz identificada no computa como raíz independiente. Dos raíces no son independientes si comparten origen documental, propiedad editorial o cadena de sindicación; ante duda, dependientes.
4. **Normalización temporal obligatoria** para datos, cifras y series; recomendada para texto. `conocible_desde` es obligatorio siempre: es el filtro anti-fuga.
5. **Append-only**: cambios de verificación, confianza o estado son entradas nuevas en el historial de la pieza; las piezas refutadas o con fuente retirada se conservan.
6. **Fuente retirada** (R19): cuando un propietario de F7–F9 borra una referencia que sustenta EVD, el Curador marca la pieza `FUENTE_RETIRADA` y el Analizador revisa si la conclusión se mantiene.
7. **Afirmación con objeción fuerte sin resolver** no puede tener confianza `establecido`: pasa a `en disputa`.
8. **Pronósticos de fuentes de opinión**: si la afirmación es un pronóstico explícito resoluble de una fuente (variable, fecha, umbral), se marca `tipo_afirmacion = PRONOSTICO_FUENTE` con su bloque `pronostico_fuente` para que el Evaluador mida su fiabilidad.

## 4. Formato de entrada

### 4.1 Afirmación (CLM-)

| Campo | Tipo | Oblig. | Valores / formato | Descripción |
|---|---|---|---|---|
| `clm_id` | Identificador | Sí | `CLM-AAAA-NNNN` | Clave |
| `afirmacion` | Texto | Sí | Concreta, verificable y fechable | Enunciado |
| `tipo_afirmacion` | Enumerado | Sí | HECHO · DATO · ANALISIS · OPINION · PREVISION · RUMOR · PRONOSTICO_FUENTE | Naturaleza |
| `clase` | Enumerado | No | RV · RF · DIV · MP · INM · CRI · ALT | Clase afectada |
| `evidencias` | Lista | Sí | EVD- con su dirección | Piezas que la sostienen, matizan o contradicen |
| `raices_independientes` | Entero | Sí | Calculado | Número de raíces independientes favorables |
| `ps1_cumple` | Booleano | Sí | 2 raíces A/B independientes o 1 primaria A | Corroboración mínima |
| `nivel_confianza` | Enumerado | Sí | establecido · probable · especulativo · en disputa | Vocabulario del bloque |
| `utilizada_por` | Lista | Sí | `{objeto TND-/OPP-/PRG-/RUN-, papel}` | Usos |
| `pronostico_fuente` | Objeto | Solo si PRONOSTICO_FUENTE | `{ref_id, variable, serie_ht01, fecha_objetivo, umbral_o_rango, direccion, probabilidad (si la da la fuente), fecha_emision}` | Para el Evaluador |
| `historial` | Lista append-only | Sí | `{fecha, cambio, motivo, run_id}` | — |

### 4.2 Evidencia (EVD-)

| Campo | Tipo | Oblig. | Valores / formato | Descripción |
|---|---|---|---|---|
| `evd_id` | Identificador | Sí | `EVD-AAAA-NNNN` | Clave |
| `clm_ids` | Lista | Sí | CLM- | Afirmaciones a las que sirve |
| `direccion` | Enumerado | Sí | FAVORABLE · CONTRARIA · NEUTRA · AMBIGUA | Respecto de cada CLM (por par si difiere) |
| `ref_id` | Identificador | Sí | Referencia de F7 (ANA-DOC-), F8 (DOC-MOT-), F9 (RF-) o serie HT-01 | Fuente |
| `nivel_fuente` | Enumerado | Sí | A · B · C · D | Nivel de calidad Q de la fuente en su archivo |
| `url_canonica` | URL | Sí | La de la raíz | Localización |
| `copia_archivada` | URL | Sí si existe | — | Copia en archivo web |
| `identificador_documental` | Texto | Sí | DOI, expediente, página, sección | Localización estable |
| `extracto` | Texto | Sí | Cita mínima entre comillas o referencia precisa | Nunca la obra íntegra |
| `tipo_fuente` | Enumerado | Sí | PRIMARIA · SECUNDARIA · TERCIARIA | Proximidad al hecho |
| `grado_independencia` | Enumerado | Sí | RAIZ · DERIVADA · COMENTARIO | Posición en la cadena |
| `raiz_evd_id` | Identificador | Sí si no es RAIZ | EVD- o «no identificada» con motivo | — |
| `hash_contenido` | Texto | Sí | SHA-256 del extracto normalizado | Deduplicación |
| `duplicados` | Lista | No | `{url, hash, fecha}` | Copias resueltas |
| `estado_verificacion` | Enumerado | Sí | Sección 5 | — |
| `limitaciones` | Texto | Sí | «ninguna conocida» solo con motivo | Muestra, conflicto de interés, autodeclaración |
| `incidencia_manipulacion` | Objeto | No | `{tipo INSTRUCCION_INCRUSTADA·FUENTES_COORDINADAS·DATO_FABRICADO·CAMPANA_REDES, detalle}` | R9 y 17.4 |
| **Normalización temporal** | | | | |
| `fecha_fenomeno` | Fecha | Sí en datos | ISO 8601 | Cuándo ocurrió el hecho |
| `periodo_datos` | Texto | Sí en datos | p. ej. «2026-T3», «2026-10» | Periodo al que corresponde |
| `fecha_publicacion` | Fecha-hora | Sí | ISO 8601 con zona | Publicación por la fuente |
| `fecha_recuperacion` | Fecha-hora | Sí | ISO 8601 con zona | Acceso del agente |
| `fecha_revision_fuente` | Fecha | No | ISO 8601 | Última revisión declarada |
| `vintage` | Texto | Sí en series revisables | Fecha de la versión de la serie (HT-01) | Para reproducir lo conocido |
| `es_primera_publicacion` | Booleano | Sí en datos macro | — | Distingue primera publicación y revisadas |
| `conocible_desde` | Fecha-hora | Sí | ISO 8601 con zona; = `fecha_publicacion` salvo embargo o retraso declarado | **Filtro anti-fuga** |
| `frecuencia` | Enumerado | Sí en series | DIARIA · SEMANAL · MENSUAL · TRIMESTRAL · ANUAL · IRREGULAR | — |
| `zona_horaria` | Texto IANA | Sí en series | p. ej. Europe/Madrid | — |
| `unidad` | Texto | Sí en cifras | p. ej. «%», «puntos básicos», «millones» | — |
| `divisa` | Código ISO 4217 | Sí en cifras monetarias | EUR, USD… | — |
| `conversion` | Objeto | Si hay conversión | `{de, a, tipo, fecha, fuente}` | Conversión declarada |
| `historial` | Lista append-only | Sí | `{fecha, cambio, motivo, run_id, agente}` | Verificación y estados |

## 5. Estados y transiciones (evidencia)

| Desde | Hacia | Condición |
|---|---|---|
| (ingesta) | PENDIENTE | Alta tras deduplicación |
| PENDIENTE | EN_VERIFICACION | Inicio de verificación (HT-02 y revisión) |
| EN_VERIFICACION | VERIFICADA · VERIFICADA_CON_RESERVAS · NO_VERIFICABLE · REFUTADA | Resultado de la verificación |
| VERIFICADA · VERIFICADA_CON_RESERVAS | REFUTADA | Evidencia posterior decisiva o retractación |
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
| Por conocibilidad | `conocible_desde` | Filtro anti-fuga del Evaluador y de evaluaciones históricas |
| Por dirección | `direccion` = CONTRARIA | Revisión de sesgo de confirmación (Auditor) |
| Por estado | `estado_verificacion` | Piezas pendientes, refutadas o con fuente retirada |
| Pronósticos de fuentes | `tipo_afirmacion` = PRONOSTICO_FUENTE y `fecha_objetivo` | Resolución por el Evaluador |
| Índice operativo | — | Recuentos por estado, dirección, grado de independencia y confianza; duplicados del periodo |

## 7. Ejemplo ficticio

> **EJEMPLO FICTICIO — no es una entrada real.** Los datos, URL e identificadores son inventados.

```json
{"evd_id":"EVD-2026-0001","clm_ids":["CLM-2026-0001"],"direccion":"FAVORABLE","ref_id":"RF-0001","nivel_fuente":"A",
 "url_canonica":"https://ejemplo-ficticio.invalid/matriculaciones-2026-10","copia_archivada":"https://archivo-ficticio.invalid/2026/matric",
 "identificador_documental":"Nota estadística mensual, tabla 3","extracto":"«las matriculaciones de furgonetas eléctricas crecieron un 31 % interanual»",
 "tipo_fuente":"PRIMARIA","grado_independencia":"RAIZ","raiz_evd_id":null,"hash_contenido":"3f9a…(ficticio)",
 "estado_verificacion":"VERIFICADA","limitaciones":"Dato provisional sujeto a revisión",
 "fecha_fenomeno":"2026-10-31","periodo_datos":"2026-10","fecha_publicacion":"2026-11-06T10:00:00+01:00",
 "fecha_recuperacion":"2026-11-07T08:12:00+01:00","vintage":"2026-11-06","es_primera_publicacion":true,
 "conocible_desde":"2026-11-06T10:00:00+01:00","frecuencia":"MENSUAL","zona_horaria":"Europe/Brussels","unidad":"%","divisa":null,
 "historial":[{"fecha":"2026-11-07","cambio":"alta PENDIENTE→VERIFICADA","motivo":"HT-02 OK; cifra coincide con la tabla","run_id":"RUN-2026-0001","agente":"AG-12"}]}
```
