# README — Herramientas deterministas del Bloque A Forex (HT-02, HT-03, HT-05, HT-07, HT-09)

**Bloque A Forex · Robot Investor · Versión óptima V1.0 · 02/11/2026 · actualizado V1.1 (03/11/2026)** · Subordinado al Documento 0 del Bloque A Forex V1.1.

**Actualización V1.1 (03/11/2026).** HT-09 (versión `FX-1.1`) añade tres comprobaciones: **C17** naturaleza de la inversión y horizonte principal (regla de adecuación de 8.3), **C18** H5 «limitado» (solo `ESTRUCTURAL` en tres ámbitos, sin probabilidad numérica, ≥ 3 hitos HIT-FX- con el espaciado del Anexo A) y **C19** supuestos declarados por consultas CT-23 sin respuesta; C13 detecta además valores de credenciales (solo se admite el alias `credencial_ref`); C10 incluye el horizonte principal H5 en la relevancia ALTA; C11 exige `horizonte_principal` en el encargo para el Bloque B. Nueva función `validar_seguimiento` (S01–S06) para el **informe de seguimiento de opción** del ciclo C6 (`--seguimiento` en la línea de órdenes). La tabla 8.3 incluye H5 «limitado» en los seis segmentos. Los ejemplos añaden `naturaleza_inversion` a cada opción, una opción G10N con H5 (EUR/USD estructural, ámbito sistema monetario internacional, tres hitos) y un supuesto declarado, y `ejemplos/informe_seguimiento_ejemplo.json`. HT-05: el planificador del ejecutor programa además los ciclos C6 y los plazos de las consultas CT-23 (sección 9).

Implementaciones de referencia de las herramientas deterministas de la sección 4.4 del Documento 0 Forex. Son herramientas, no agentes: no razonan, no tienen iniciativa y no consumen modelo de lenguaje (10.5). Todas son reproducibles: con la misma entrada devuelven la misma salida.

**Qué cambia respecto del Bloque A general (V5.0).** HT-02 (verificador de enlaces) y HT-07 (legibilidad, con la versión corregida de Fernández-Huerta de Law, 2011) se mantienen sin cambios: valen igual para F7, F8 y F9 del Forex y para el informe visual. HT-03 y HT-09 se han adaptado al mercado de divisas: seis segmentos (G10N, G10M, EMAS, EMLA, EMEA, ESTR) en lugar de tipos de activo; pesos de la A FX del Anexo A; diversidad del segmento por clúster y por divisa-dirección; tabla de horizontes 8.3 Forex; notación BASE/COTIZADA con códigos ISO 4217, dirección, composición y divisa de financiación; PS3 de convertibilidad; infijo FX en todos los identificadores (`RUN-FX-`, `OPP-FX-`, `PRG-FX-`, `TND-FX-`, `CLM-FX-`, `EVD-FX-`, `CALC-FX-`, `TRV-FX-`); las once comprobaciones G3-FX del Anexo 1 del Plan de pruebas; frontera con el Bloque B sin instrumentos; y exposición agregada por divisa.

## 1. Estado de madurez (R22)

| Herramienta | Archivo | Estado |
|---|---|---|
| HT-02 Verificador de enlaces y contenido | `ht02_verificador_enlaces.py` | Implementada (referencia), pruebas unitarias superadas; pendiente de integración |
| HT-03 Calculadora de puntuaciones y ranking | `ht03_puntuaciones.py` | Implementada (referencia), pruebas unitarias superadas; pendiente de integración |
| HT-05 Planificador | `ht05_planificador_ejemplo.md` | Documentada (especificación); no implementada |
| HT-07 Medidor de legibilidad | `ht07_legibilidad.py` | Implementada (referencia), pruebas unitarias superadas; pendiente de integración |
| HT-09 Validador determinista G3 | `ht09_validador_g3.py` | Implementada (referencia), pruebas unitarias superadas; pendiente de integración |

«Pendiente de integración» significa que no se han conectado aún a los agentes, a los archivos reales F1–F10 ni al planificador, y que no se han validado con la batería de `09_Pruebas`. Ninguna se presenta como validada.

## 2. Requisitos

- Python ≥ 3.8. **Solo biblioteca estándar**: no se usan `requests` ni `jsonschema`.
- Pruebas: `pytest` (opcional) o `unittest` de la biblioteca estándar.
- Dependencias internas: HT-02 y HT-09 importan `ht07_legibilidad.py`; HT-09 importa `ht03_puntuaciones.py`. Los cuatro archivos deben estar en el mismo directorio.

## 3. Contenido

```
10_Herramientas/
├── README.md
├── ht02_verificador_enlaces.py
├── ht03_puntuaciones.py
├── ht05_planificador_ejemplo.md
├── ht07_legibilidad.py
├── ht09_validador_g3.py
├── ejemplos/
│   ├── referencias_ejemplo.md              (archivo de referencias para HT-02)
│   ├── ht03_entrada_ejemplo.json           (opciones de G10N, EMLA y ESTR, y candidatas de EMAS, para HT-03)
│   ├── paquete_oportunidades_ejemplo.json  (paquete del Anexo B Forex para HT-09; datos ilustrativos)
│   ├── certificados_ejemplo.json           (certificados de horizonte para HT-09)
│   ├── desgloses_ejemplo.json              (dimensiones HT-03, con la A FX, por opp_id para HT-09)
│   ├── trazas_ejemplo.json                 (extracto CLM→EVD de F2 para HT-09)
│   ├── artefactos_ejemplo.json             (CALC- presentes en el Registro de cálculos)
│   ├── informe_visual_ejemplo.html         (informe visual para HT-07 y HT-09)
│   ├── informe_seguimiento_ejemplo.json    (V1.1: informe de seguimiento de opción para validar_seguimiento)
│   └── jerga_personalizada.txt             (lista de jerga alternativa para HT-07)
└── tests/
    ├── test_ht02_verificador_enlaces.py    (servidor HTTP local en un hilo; sin red externa)
    ├── test_ht03_puntuaciones.py
    ├── test_ht07_legibilidad.py
    └── test_ht09_validador_g3.py
```

## 4. Ejecutar las pruebas

```bash
cd 10_Herramientas
python3 -m pytest -q tests          # o bien:
python3 -m unittest discover -s tests
```

Resultado de la última ejecución (03/11/2026, V1.1): **147 pruebas superadas** (más 38 subpruebas de silabeo), en unos 10 segundos: HT-02 25, HT-03 38, HT-07 15 y HT-09 69 (51 de V1.0 y 18 nuevas de V1.1: horizonte principal, H5 e hitos, supuestos, credenciales e informe de seguimiento). Las pruebas de HT-02 levantan un servidor `http.server` local en un hilo y no necesitan red externa.

## 5. HT-02 · Verificador de enlaces y contenido

**Qué hace.** Lee un archivo de referencias (F7, F8 o F9) con fichas `#### ID · Q nn (N) — Título` seguidas de líneas `- **Campo:** valor` y comprueba cada URL o DOI:

- HEAD y, si procede, GET con tiempo límite y reintentos con espera exponencial (5xx, 408, 429 y errores de conexión); si HEAD falla (p. ej., 405), decide el GET.
- Resolución del DOI por `https://doi.org/` y cadena de redirecciones.
- Detección heurística de muro de pago (HTTP 402; 401/403 con marcas; dos o más marcas textuales; `isAccessibleForFree=false`) y de retractaciones.
- Detección de soft-404 (redirección a la portada o título de página de error).
- Hash SHA-256 del texto visible normalizado (sin cifras, para ignorar fechas y contadores) y huella SimHash de 64 bits; similitud = 1 − Hamming/64, comparada con el umbral del Anexo A (0,8).
- Copia en Wayback mediante `https://archive.org/wayback/available` ante incidencias (o siempre, en altas).

**Estados y acciones (13.4–13.5).**

| Estado | Acción sugerida |
|---|---|
| OK | NINGUNA (o BORRAR si Q < 50 y sin uso en 180 días, campo «Último uso») |
| REDIRIGIDO | REPARAR si la redirección es permanente (301/308); NINGUNA si es temporal |
| ROTO | Primer fallo: NINGUNA (reintentar ≥ 24 h). Con alternativa (DOI o Wayback): REPARAR. Confirmado sin alternativa: DEGRADAR; si el primer fallo tiene ≥ 7 días (dos barridos): BORRAR |
| MURO_PAGO | REPARAR si hay copia abierta archivada; si no, DEGRADAR (criterio de accesibilidad de 13.3) |
| CONTENIDO_CAMBIADO | DEGRADAR, con la versión archivada sugerida, a la espera de revisión del agente |
| (retractación detectada) | BORRAR, con aviso al Curador si la ficha tiene «Evidencias» |

**Invocación.**

```bash
# Informe JSON + CSV
python3 ht02_verificador_enlaces.py F7.md --salida-json informe.json --salida-csv informe.csv
# Actualizar en el markdown estado, fecha, primer fallo, hash, huella y copia archivada
python3 ht02_verificador_enlaces.py F7.md --aplicar
# Reintento de 24 h solo de algunas fichas
python3 ht02_verificador_enlaces.py F7.md --ids ANA-DOC-0003 ANA-DOC-0007 --aplicar
# Baja con línea en el «Registro de bajas» (REF-id, título, motivo, fecha, sustituta)
python3 ht02_verificador_enlaces.py F7.md --borrar ANA-DOC-0099 --motivo "Q < 50 sin uso en 180 días" --sustituta ANA-DOC-0012
# Aceptar el contenido actual como nueva referencia de hash (tras revisar un CONTENIDO_CAMBIADO)
python3 ht02_verificador_enlaces.py F7.md --rebasar ANA-DOC-0003
```

Otras opciones: `--fecha`, `--timeout`, `--reintentos`, `--espera`, `--hilos`, `--umbral-similitud`, `--wayback {siempre,incidencias,nunca}`, `--wayback-api`, `--doi-base`, `--sin-contenido`, `--sin-proxy`, `--ca-bundle`.

**Campos que lee o escribe:** `URL`, `DOI`, `Estado del enlace`, `Última verificación`, `Primer fallo`, `Hash de contenido`, `Huella de contenido`, `Copia archivada`, `Último uso`, `Evidencias`. Los que faltan se insertan al final de la ficha.

**Salvaguarda de red.** Si ninguna comprobación obtiene respuesta HTTP (caída de red o proxy), el informe lo marca como `incidencia_red` y `--aplicar` no modifica el archivo.

**Códigos de salida:** 0 correcto; 2 error en `--borrar`/`--rebasar`; 3 archivo ilegible.

## 6. HT-03 · Calculadora determinista de puntuaciones y ranking

**Qué hace.** Calcula T, E, M, P y A a partir de sus dimensiones, RK, banda marginal, cambios materiales, elegibilidad (9.2) y top-3 por segmento de divisas (9.6) para los seis segmentos de 2.6 (G10N, G10M, EMAS, EMLA, EMEA, ESTR). Aritmética exacta con fracciones.

- Dimensiones de 0 a 100 en múltiplos de 10, o `"NA"` / `"NE"`; pesos de 9.1 (sobrescribibles con `parametros` desde F10).
- `NA`: peso redistribuido proporcionalmente; `NE`: puntúa 0 y conserva su peso; más de dos NA/NE: puntuación no calculable y opción no elegible.
- Total redondeado al múltiplo de 5 más próximo, empates hacia abajo (72,5 → 70). RK = 0,45·A + 0,35·E + 0,20·T sobre los totales, redondeado al entero con empates hacia abajo.
- P incorpora el total T como dimensión (40 %).
- **A FX** (9.1 y Anexo A): `asimetria` 30 · `valoracion` (valoración y desviación del equilibrio: PPA, BEER, REER, lo que descuentan el forward y la curva) 20 · `carry` (diferencial de tipos a favor o en contra de la tesis, ajustado por volatilidad; un carry negativo puntúa bajo pero no impide la opción) 15 · `catalizadores` 15 · `momento_posicionamiento` (un posicionamiento extremo a favor de la tesis puntúa bajo por aglomeración) 10 · `convertibilidad` (liquidez, convertibilidad, NDF y controles de capitales) 10. Las dimensiones de la A del Bloque A general (`momento`, `invertibilidad`, `liquidez_accesibilidad`, `costes_implementacion`) se rechazan con un mensaje que indica su equivalente FX. A no puntúa instrumentos ni sus costes.
- Tope por saturación narrativa: la dimensión `valoracion` de A no supera 40 (en divisas, posicionamiento especulativo en el decil extremo a favor de la tesis y forward que ya descuenta la senda de tipos esperada).
- T `"NA"` en bloque (oportunidad táctica, frecuente en H1–H2): se exige A ≥ 65 y RK reparte el peso de T entre A y E.
- Banda marginal (≤ 5 puntos de un umbral de elegibilidad o de GC2): con `segunda_pasada` se usa el menor valor; sin ella, la opción no es elegible (PS8).
- Cambios ≥ 15 puntos frente a `anterior`: se señalan como `exige_justificacion`.
- Segmento: cada opción declara `segmento` (o `clase`, alias aceptado: «Analista de clase» es sinónimo histórico, Anexo C); un código fuera de los seis (o de `parametros.segmentos`, si F10 desactiva alguno) es un error de entrada. La salida `seleccion` sigue el orden de la tabla 2.6 e incluye los segmentos con `candidatas_analizadas` aunque no tengan opciones.
- Top-3: orden por RK; dentro de ±2 puntos, mayor E y después menor `riesgo_cola`; continuidad de vigentes (se mantienen si su RK no queda más de 10 puntos por debajo de la mejor nueva); **diversidad del segmento (9.6.3)**: como máximo dos opciones del mismo clúster de exposición y una misma divisa con la misma dirección (LARGO o CORTO) en no más de dos opciones. La opción que rompería una de las dos reglas cede su puesto (`CEDE_POR_DIVERSIDAD`) a la siguiente elegible que las cumpla si su RK está a ≤ 10 puntos; si no hay ninguna, el hueco queda vacío y se explica (R14); menos de tres con motivo, candidatas analizadas y qué tendría que ocurrir.
- Exposición por divisa de cada opción (`exposiciones_de`): `exposiciones` [{divisa, lado}] explícitas; si no, `composicion` [{divisa, peso, lado}]; si no, `par` BASE/COTIZADA y `direccion` (`ALCISTA_BASE`: base LARGO y cotizada CORTO; `BAJISTA_BASE`: al revés). En cestas, bloques y estrategias la dirección está en la composición (`direccion` nula); las opciones de volatilidad (`direccion` nula y `vista_volatilidad` ALZA/BAJA con plazo) no tienen exposición direccional.

**Entrada (resumen).**

```json
{"parametros": {}, "candidatas_analizadas": {"G10N": 10, "EMAS": 5},
 "opciones": [{"opp_id": "OPP-FX-2026-0007", "segmento": "G10N", "par": "USD/JPY", "direccion": "BAJISTA_BASE",
   "cluster": "yen_refugio", "vigente": false, "riesgo_cola": 3, "saturacion_narrativa": false,
   "dimensiones": {"T": {"magnitud": 80, "...": 80}, "E": {}, "M": {},
                   "A": {"asimetria": 80, "valoracion": 80, "carry": 40, "catalizadores": 80, "momento_posicionamiento": 80, "convertibilidad": 80},
                   "P": {"novedad": 60, "incertidumbre_reducible": 60, "coste_eficiencia": 70}},
   "segunda_pasada": {"E": {}}, "anterior": {"A": 80},
   "puertas": {"G1": true, "...": true, "PS8": true}, "objeciones_fuertes_abiertas": 0}]}
```

Claves de dimensiones: T `magnitud, alcance, velocidad, duracion, difusion, posicion_cadena_valor, capacidad_transformadora, claridad_causal`; E `calidad_raices, cobertura_variables, calidad_metodologica, trazabilidad, actualidad, discrepancias_resueltas, objeciones_respondidas`; M `adopcion, escalado, indicadores_disponibles, persistencia, estabilidad_impulsores, hitos_claros`; P `T (automática), novedad, incertidumbre_reducible, coste_eficiencia`; A `asimetria, valoracion, carry, catalizadores, momento_posicionamiento, convertibilidad`.

**Ejemplo incluido.** En G10N, EUR/JPY bajista (tercera opción del clúster «yen_refugio» y tercera con el yen largo) cede su puesto a EUR/GBP alcista, a ≤ 10 puntos; la vigente GBP/USD queda sustituida por estar a más de 10 puntos de la mejor nueva; en EMLA solo entra la oportunidad táctica USD/BRL (T = NA, A ≥ 65); EMAS no tiene opciones y conserva su motivo.

**Invocación.** `python3 ht03_puntuaciones.py ejemplos/ht03_entrada_ejemplo.json --salida resultado.json` (código 0; 2 si la entrada no es válida).

## 7. HT-07 · Medidor de legibilidad

**Qué hace.** Sobre texto plano o HTML (solo texto visible: excluye `script`, `style`, `head`, elementos `hidden`, `aria-hidden` o `display:none`):

- Índice de Fernández-Huerta en su versión corregida (Law, 2011): `L = 206,84 − 0,60·P − 1,02·F`, con P = sílabas por 100 palabras y F = palabras por frase (la fórmula original de 1959, con F = frases por 100 palabras, se informa aparte); interpretación de muy fácil a muy difícil; umbral 70 (14.2).
- Silabeo español por reglas: dígrafos ch, ll, rr; «qu» y «gu» con u muda; diptongos, triptongos e hiatos (vocales fuertes contiguas o débil tildada junto a fuerte); «y» vocálica final; grupos consonánticos inseparables (pr, br, tr, dr, cr, gr, fr, kr, pl, bl, cl, gl, fl, kl); «tl» se separa (norma peninsular).
- Longitud media de frase y porcentaje de frases de más de 20 palabras, con la lista de frases largas.
- Jerga: lista inicial de más de 100 términos financieros (configurable con `--jerga`, en texto o JSON), sin distinguir mayúsculas ni tildes y con coincidencia más larga primero; indica si la primera aparición va explicada entre paréntesis (o con «es decir»).

**Invocación.** `python3 ht07_legibilidad.py informe.html [--jerga lista.txt] [--umbral 70] [--salida r.json]`. Código 0 si cumple el umbral; 1 si no; 3 si hay error de lectura.

**Limitaciones declaradas.** El silabeo es ortográfico y aproximado (la «h» intercalada se trata como consonante: «ahu-ma-do» se cuenta como cuatro sílabas). Los números cuentan como una palabra de dos sílabas.

## 8. HT-09 · Validador determinista G3

**Qué hace.** Valida un `paquete_oportunidades` Forex (Anexo B del Documento 0 Forex y esquema JSON de `06_Plantillas_entregables`) y devuelve `APTO`, `APTO_CON_ADVERTENCIAS` o `BLOQUEADO` con 30 comprobaciones: 19 generales (C01–C19, adaptadas a segmentos; C17–C19 desde V1.1) y las 11 específicas de divisas **G3-FX-01 a G3-FX-11** del Anexo 1 del Plan de pruebas del Bloque A Forex, con sus mismos identificadores. Cada comprobación lista sus incidencias (`ruta`, `detalle`, `severidad`):

| ID | Comprobación | Bloquea cuando… |
|---|---|---|
| C01 | Campos obligatorios, valores y prefijos | Falta o está vacío un campo del Anexo B (raíz: `regimen_cambiario`, `exposicion_agregada`, `segmentos`…; opción: `par`, `direccion`, `composicion` y `divisa_financiacion` deben estar presentes aunque sean nulos); valor fuera de vocabulario; segmento desconocido o distinto del de la clave; identificadores sin el infijo FX del Documento 0 (`RUN-FX-`, `OPP-FX-`, `PRG-FX-`, `TND-FX-`, `CLM-FX-`/`EVD-FX-`, `CALC-FX-`) |
| C02 | Opciones por segmento y clústeres | Más de 3 opciones, rangos distintos de 1..n o más de dos opciones del mismo clúster (9.6.3) |
| C03 | Menos de tres | Menos de 3 opciones sin `menos_de_tres_motivo` |
| C04 | Puntuaciones reconstruibles | RK no coincide con 0,45·A + 0,35·E + 0,20·T; total no múltiplo de 5; desglose distinto de HT-03 o con dimensiones que no son de la A FX |
| C05 | Elegibilidad y puertas | E < 60, A < 55 (A < 65 con T NA), T < 50; puerta G/PS no superada; banda marginal sin segunda pasada (PS8) |
| C06 | Horizontes (8.3 Forex) | Horizonte «No» (ESTR en H1); «Limitado» (EMAS, EMLA y EMEA en H1 y H4) sin catalizador o con liquidez baja; horizonte sin PRG- |
| C07 | Probabilidad numérica (R13) | `prob` sin certificado vigente para segmento × horizonte |
| C08 | Evidencias y cálculos (R7) | Listas vacías; CLM- sin EVD (`--trazas`); CALC- sin artefacto (`--artefactos`) |
| C09 | Objeciones (R12) | Objeción fuerte sin resolver; moderada sin respuesta |
| C10 | Relevancia decisional | La nota 3 del Anexo A exige ALTA (riesgo ≥ 4, reversibilidad baja, horizonte H4 con riesgo ≥ 3 o liquidez baja, E < 70 con A ≥ 75, tipo REGIMEN o divisa emergente de liquidez baja) y se declara otra |
| C11 | Encargo para el Bloque B | Falta el encargo de una opción con `ENVIAR_A_BLOQUE_B` o alguno de sus campos del Anexo B Forex (incluidos `carry_esperado` y `consideraciones_implementacion`); par, dirección, vista de volatilidad, divisa de financiación, tipo o segmento distintos de los de la opción |
| C12 | Legibilidad (HT-07) | Fernández-Huerta corregido < 70 o informe ilegible |
| C13 | Credenciales (R8) | Patrones de claves, contraseñas o tokens |
| C14 | Semáforo y apuestas | Solo advertencias |
| C15 | Frontera con el Bloque B (R21) | Tipo de opción no cambiario; ámbito o indicador ausentes; campos del Bloque B (`instrumento`, `proveedor`, `apalancamiento`, `tamano_posicion`, `nivel_entrada`, `stop_loss`…) o `ejemplos_ilustrativos`; propuesta de instrumento («comprar un ETF», «mediante CFD», «con opciones call»…) o de ejecución («nivel de entrada», «stop loss», tamaño, apalancamiento) en los textos de la opción o en las consideraciones de implementación; ISIN. Citar instrumentos para justificar la invertibilidad o en las preguntas para el Bloque B está permitido |
| C16 | Duplicada en dos segmentos (regla 4 de 2.6) | Mismo nombre, ámbito o exposición normalizados, o mismo `opp_id`, en dos segmentos |
| C17 | Naturaleza y horizonte principal (8.3, V1.1) | `naturaleza_inversion` u `horizonte_principal` ausentes; `LIQUIDEZ` (no se usa en Forex); horizonte principal no ofrecido o en celda «No»; fuera del rango de su naturaleza (TACTICA H1–H2, CICLICA y PRIMA_RIESGO H2–H4, VALORACION H3–H4, ESTRUCTURAL H4–H5) sin `justificacion_horizonte` (con justificación, o «Limitado» de H1–H4 sin catalizador: advertencia) |
| C18 | H5 limitado (8.3, R13, Anexo A; V1.1) | H5 en una opción no ESTRUCTURAL; `ambito_h5` fuera de EQUILIBRIO_LARGO_PLAZO, REGIMEN_CAMBIARIO, SISTEMA_MONETARIO_INTERNACIONAL; `prob` numérica; sin banda; < 3 hitos; primer hito a más de 12 meses de la fecha del paquete o más de 24 meses entre hitos; hito sin fecha, indicador o criterio; `hit_id` sin formato HIT-FX- |
| C19 | Supuestos declarados (6.2.9; V1.1) | `consultas_broker_sin_respuesta` con alguna CNS-FX- sin supuesto en `supuestos_declarados`; supuesto sin `efecto_si_falso`; `cns_id` sin formato |
| G3-FX-01 | Notación y dirección | Par fuera de `BASE/COTIZADA` con ISO 4217 o fuera de la convención de mercado (prelación EUR, GBP, AUD, NZD, USD, CAD, CHF, NOK, SEK, JPY; los emergentes cotizan frente al G10); PAR, CRUCE o REGIMEN sin `direccion` ALCISTA_BASE/BAJISTA_BASE; `direccion` no nula en cestas, bloques, estrategias o volatilidad (allí la dirección va en `composicion` o en `vista_volatilidad` {sentido ALZA/BAJA, plazo}); dirección incoherente con la composición, con la divisa de financiación o con `nombre_llano` («el yen podría ganar valor frente al dólar») |
| G3-FX-02 | Composición de cestas (PS4) | CESTA, BLOQUE o ESTRATEGIA sin composición, con pesos ausentes o que no suman 1 por lado, divisas no ISO 4217 o sin `divisa_financiacion` |
| G3-FX-03 | Asignación de segmento | Segmento distinto del de las reglas 1–3 de 2.6 (divisa menos líquida; tres o más divisas o estrategia → ESTR; volatilidad de un par → su segmento) sin `motivo_asignacion_segmento` (con motivo, advertencia) |
| G3-FX-04 | Convertibilidad (PS3) y riesgo de régimen | Bloque `convertibilidad` incompleto; divisa no convertible sin NDF ni exposición alternativa; controles que impiden la exposición o la repatriación; tipo fijo (o caja de conversión), divisa con controles u opción REGIMEN con `riesgo_1a5` < 4; REGIMEN sin `regimen_cambiario_divisa` |
| G3-FX-05 | Carry | Sin carry anual, signo o carry ajustado por volatilidad; sin `calc_id` CALC-FX-; signo incoherente con la cifra o, si se declara `diferencial_tipos_pct` (base − cotizada), con la dirección; «no aplicable» fuera de VOLATILIDAD |
| G3-FX-06 | Referencias ingenuas (advertencia) | PRG sin paseo aleatorio; rentabilidad total sin forward; estrategias sin rentabilidad nula o índice de la estrategia |
| G3-FX-07 | Anticipación en fijaciones | `fecha_dato` o `conocible_desde` de un nivel de referencia posterior a la fecha de los datos del paquete; fijación sin fuente u `hora_fijacion` con hora y zona («16:00 Europe/London») |
| G3-FX-08 | Exposición agregada y contradicciones | `exposicion_agregada` ausente, con valores no permitidos o con signo opuesto a la exposición neta que suman las composiciones; una misma divisa como **pata activa** de la tesis (`patas_activas`: la que se pronostica; el USD o el EUR como contrapartida o financiación no cuentan) larga en un segmento y corta en otro sin `justificacion_contradiccion` en `contradicciones_entre_segmentos` |
| G3-FX-09 | Diversidad por divisa | Una divisa con la misma dirección en más de dos opciones de un segmento |
| G3-FX-10 | Capas transversales (advertencia) | Sin `informes_transversales` con los dos `TRV-FX-` del ciclo (AG-09 y AG-21) ni `nota` que declare su ausencia o reutilización |
| G3-FX-11 | Tipo de rentabilidad | PRG sin `tipo_rentabilidad` (PRECIO_CONTADO o RENTABILIDAD_TOTAL; NIVEL_VOLATILIDAD en las opciones VOLATILIDAD, 2.4) o sin `divisa_medicion` ISO 4217 |

**Invocación.**

```bash
python3 ht09_validador_g3.py ejemplos/paquete_oportunidades_ejemplo.json \
  --certificados ejemplos/certificados_ejemplo.json \
  --informe-visual ejemplos/informe_visual_ejemplo.html \
  --desgloses ejemplos/desgloses_ejemplo.json \
  --trazas ejemplos/trazas_ejemplo.json --artefactos ejemplos/artefactos_ejemplo.json
```

Con todas las entradas, el ejemplo (datos ilustrativos, ocho opciones en cinco segmentos —una de ellas H5 estructural en G10N— y EMEA en gris) da `APTO`; sin certificados da `BLOQUEADO` (C07: probabilidad numérica en G10N×H3). Opciones: `--parametros` (F10 en formato HT-03), `--umbral-fh`, `--salida`. Códigos de salida: 0 APTO, 1 APTO_CON_ADVERTENCIAS, 2 BLOQUEADO, 3 error de entrada. Los certificados se identifican por `segmento` (se acepta `clase` como alias).

**Informe de seguimiento de opción (V1.1).** `python3 ht09_validador_g3.py ejemplos/informe_seguimiento_ejemplo.json --seguimiento [--informe-visual informe.md]` aplica `validar_seguimiento`: S01 campos, prefijos (SEG-FX-, OPP-FX-, RUN-FX-) y vocabularios (semáforo VERDE/AMBAR/ROJO; recomendación MANTENER_VIGILANCIA, PROPONER_ENVIO_A_B, CERRAR, PROPONER_CANCELACION) y longitud ≤ 300 palabras; S02 coherencia de la recomendación (PROPONER_ENVIO_A_B exige elegibilidad con HT-03, `paquete_para_bloque_B` y ninguna objeción fuerte; incompatible con ROJO); S03 puntuaciones de HT-03; S04 ningún pronóstico nuevo y H5 con hitos; S05 credenciales; S06 supuestos.

**Campos opcionales que HT-09 aprovecha si existen en la opción:** `puertas` (G1–G4, PS1–PS8), `cluster`, `vigente`, `objeciones[].resuelta`, `horizontes.Hn.advertencia` (exigida en H1), `horizontes.Hn.metodo`, `carry.diferencial_tipos_pct` y `motivo_asignacion_segmento`. En la raíz: `informes_transversales`, `contradicciones_entre_segmentos` y `divisa_base_usuario`. El dato `exposicion_neta_calculada` de G3-FX-08 resume la exposición neta por divisa (pesos con signo) que se compara con `exposicion_agregada`.

## 9. HT-05 · Planificador

**V1.1.** La implementación del ejecutor (`11_Ejecutor/bloque_a_forex/herramientas/ht05_planificador.py`) añade `proximo_ciclo_seguimiento` (ciclos C6 de cada encargo de F11: diaria —siguiente día hábil—, semanal, quincenal, mensual, trimestral o personalizada) y `vencimiento_consulta` (plazos CT-23 del Anexo A).

Especificación en `ht05_planificador_ejemplo.md`: expresiones cron por defecto de C1 (ejecución el sábado 06:00 y entrega el lunes 07:00), C4 (barrido de enlaces el domingo 04:00, reintento de 24 h, revisiones mensual y trimestral, CT-21) y C5 (resolución diaria de pronósticos, revisiones mensual y trimestral), con `CRON_TZ` en la zona horaria del usuario (por defecto, `Europe/Madrid`) y las periodicidades alternativas que el Broker puede fijar por CT-04.

## 10. Decisiones de diseño relevantes

1. **RK redondeado al entero** con empates hacia abajo (el Documento 0 no fija su redondeo; el ejemplo del Anexo B, RK 72 con A 70, E 75, T 70, es coherente con esta regla).
2. **Banda marginal sin segunda pasada = no elegible (PS8)**; se consideran los umbrales de elegibilidad y el de GC2 (E 50).
3. **Diversidad del segmento (9.6.3)**: el máximo de dos opciones por clúster y de dos opciones con la misma divisa en la misma dirección se aplica de forma estricta. El Documento 0 Forex mantiene además la frase del Bloque A general «si las tres primeras comparten clúster, la tercera cede su puesto a la mejor de otro clúster cuando su RK está a 10 puntos o menos»; se interpreta así: la opción que rompería la regla cede su puesto a la siguiente elegible que la cumpla si su RK está a ≤ 10 puntos y, si no hay ninguna, el hueco queda vacío con motivo (R14). Ya no se admite la excepción del Bloque A general (tres del mismo clúster). La exposición de una cesta cuenta cada divisa de la composición con su lado.
4. **ROTO** se confirma con un segundo fallo ≥ 24 h después del primero; la baja por «dos barridos» se sugiere cuando el primer fallo tiene ≥ 7 días y no hubo aciertos intermedios.
5. **Relevancia decisional**: subestimar (no marcar ALTA cuando la regla lo exige) bloquea; sobrestimar solo advierte. El horizonte H4 dispara ALTA solo con riesgo ≥ 3 o liquidez baja (nota 3 del Anexo A Forex).
6. **Objeción moderada sin respuesta** bloquea (F4 exige respuesta a fuertes y moderadas).
7. **Duplicados entre segmentos (C16)**: se compara por nombre, ámbito y exposición normalizados; el criterio es conservador (coincidencia exacta tras normalizar). Una opción de VOLATILIDAD no se compara por exposición con la opción direccional del mismo par.
8. **Instrumentos (C15)**: se detectan recomendaciones explícitas (verbo o preposición de uso + instrumento) y decisiones de ejecución; mencionar que «existen futuros y opciones líquidos sobre el par» para justificar la invertibilidad no bloquea (2.4). Las preguntas para el Bloque B pueden nombrar instrumentos porque son preguntas, no propuestas. ISIN con dígito de control válido.
9. **Notación convencional (G3-FX-01)**: la jerarquía de base es EUR > GBP > AUD > NZD > USD > CAD > CHF > NOK > SEK > DKK > emergentes, con el JPY siempre como cotizada; entre dos emergentes no hay convención única. Bloquea, como exige el Anexo 1 del Plan de pruebas.
12. **Tipo de rentabilidad de las opciones VOLATILIDAD**: `NIVEL_VOLATILIDAD` (2.4 del Documento 0 Forex) para los pronósticos sobre el nivel de la volatilidad implícita; solo se admite en opciones VOLATILIDAD.
13. **Signo del carry frente al diferencial (G3-FX-05)**: el diferencial de tipos solo se compara si el paquete lo declara (`carry.diferencial_tipos_pct`); en cestas el signo se valida frente a la cifra.
10. **Exposición agregada**: HT-09 suma las composiciones (pesos con signo; un par cuenta ±1 por divisa) y compara solo el signo con la categoría declarada; la intensidad («moderada», «fuerte») es juicio del Analizador.
11. **`methodology_version`**: se espera `FX-x.y` (Anexo A Forex: FX-1.0); otra versión solo advierte.
14. **Pata activa (9.6.6)**: la opción puede declararla en `pata_activa`; si no, HT-09 la deduce: en un par, la divisa distinta del USD y del EUR (las dos en un cruce sin ellas; la larga en EUR/USD); en una cesta, bloque o estrategia, el lado opuesto al de la divisa de financiación; en VOLATILIDAD, ninguna. Solo las patas activas cuentan como contradicción; el resto se refleja en la exposición agregada.
