# README — Herramientas deterministas del Bloque A (HT-02, HT-03, HT-05, HT-07, HT-09)

**Bloque A · Robot Investor · Versión óptima V5.0 · 02/11/2026 · actualizado V5.1 (03/11/2026)** · Subordinado al Documento 0 óptima V5.1. Cambios V5.1: HT-09 con H5 y las comprobaciones C17 (horizonte principal y naturaleza de la inversión), C18 (H5 con hitos HIT-) y C19 (supuestos declarados), y validación del informe de seguimiento de opción (`--seguimiento`); HT-05 de ejemplo con los ciclos C6, los vencimientos CT-23 y los recordatorios CT-25 y de hitos.

Implementaciones de referencia de las herramientas deterministas de la sección 4.4 del Documento 0. Son herramientas, no agentes: no razonan, no tienen iniciativa y no consumen modelo de lenguaje (10.5). Todas son reproducibles: con la misma entrada devuelven la misma salida.

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
│   ├── ht03_entrada_ejemplo.json           (opciones de RV, RF y TCV, y candidatas de IDX, para HT-03)
│   ├── paquete_oportunidades_ejemplo.json  (paquete del Anexo B V5.1 para HT-09: naturaleza, horizonte principal, H5 con hitos y supuestos)
│   ├── certificados_ejemplo.json           (certificados de horizonte para HT-09)
│   ├── desgloses_ejemplo.json              (dimensiones HT-03 por opp_id para HT-09)
│   ├── trazas_ejemplo.json                 (extracto CLM→EVD de F2 para HT-09)
│   ├── artefactos_ejemplo.json             (CALC- presentes en el Registro de cálculos)
│   ├── informe_visual_ejemplo.html         (informe visual para HT-07 y HT-09)
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

Resultado de la última ejecución (03/11/2026, V5.1): **135 pruebas superadas** (más 38 subpruebas de silabeo), en unos 6 segundos; HT-09 tiene 59 (19 nuevas de la V5.1: tabla H5, C17, C18, C19, credenciales, encargo para el Bloque B con horizonte principal e informe de seguimiento de opción). Las pruebas de HT-02 levantan un servidor `http.server` local en un hilo y no necesitan red externa.

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

**Qué hace.** Calcula T, E, M, P y A a partir de sus dimensiones, RK, banda marginal, cambios materiales, elegibilidad (9.2) y top-3 por tipo de activo (9.6) para los doce tipos de 2.6 (RV, RF, DIV, MP, IDX, FON, DER, INM, CRI, ALT, MON, TCV). Aritmética exacta con fracciones.

- Dimensiones de 0 a 100 en múltiplos de 10, o `"NA"` / `"NE"`; pesos de 9.1 (sobrescribibles con `parametros` desde F10).
- `NA`: peso redistribuido proporcionalmente; `NE`: puntúa 0 y conserva su peso; más de dos NA/NE: puntuación no calculable y opción no elegible.
- Total redondeado al múltiplo de 5 más próximo, empates hacia abajo (72,5 → 70). RK = 0,45·A + 0,35·E + 0,20·T sobre los totales, redondeado al entero con empates hacia abajo.
- P incorpora el total T como dimensión (40 %).
- Tope por saturación narrativa: la dimensión `valoracion` de A no supera 40.
- T `"NA"` en bloque (oportunidad táctica): se exige A ≥ 65 y RK reparte el peso de T entre A y E.
- Banda marginal (≤ 5 puntos de un umbral de elegibilidad o de GC2): con `segunda_pasada` se usa el menor valor; sin ella, la opción no es elegible (PS8).
- Cambios ≥ 15 puntos frente a `anterior`: se señalan como `exige_justificacion`.
- A (9.1 V5.0) mide el atractivo del **ámbito**, no de un instrumento: asimetría 30, valoración del ámbito 25, catalizadores 15, momento 15, profundidad e invertibilidad del universo 15. Las dimensiones V4.x `liquidez_accesibilidad` y `costes_implementacion` se rechazan con un mensaje que remite a `invertibilidad`.
- Tipo de activo: cada opción declara `tipo_activo` (o `clase`, alias aceptado por compatibilidad); un código fuera de los doce (o de `parametros.tipos_activo`, si F10 desactiva alguno) es un error de entrada. La salida `seleccion` sigue el orden de la tabla 2.6 e incluye los tipos con `candidatas_analizadas` aunque no tengan opciones.
- Top-3: orden por RK; dentro de ±2 puntos, mayor E y después menor `riesgo_cola`; continuidad de vigentes (se mantienen si su RK no queda más de 10 puntos por debajo de la mejor nueva); diversidad (si las tres comparten clúster, la tercera cede ante la mejor de otro clúster a ≤ 10 puntos); menos de tres con motivo, candidatas analizadas y qué tendría que ocurrir.

**Entrada (resumen).**

```json
{"parametros": {}, "candidatas_analizadas": {"RV": 12, "IDX": 5},
 "opciones": [{"opp_id": "OPP-2026-0007", "tipo_activo": "RV", "cluster": "ciclo_europeo", "vigente": false,
   "riesgo_cola": 2, "saturacion_narrativa": false,
   "dimensiones": {"T": {"magnitud": 70, "...": 70}, "E": {}, "M": {}, "A": {}, "P": {"novedad": 60, "incertidumbre_reducible": 60, "coste_eficiencia": 70}},
   "segunda_pasada": {"E": {}}, "anterior": {"A": 80},
   "puertas": {"G1": true, "...": true, "PS8": true}, "objeciones_fuertes_abiertas": 0}]}
```

Claves de dimensiones: T `magnitud, alcance, velocidad, duracion, difusion, posicion_cadena_valor, capacidad_transformadora, claridad_causal`; E `calidad_raices, cobertura_variables, calidad_metodologica, trazabilidad, actualidad, discrepancias_resueltas, objeciones_respondidas`; M `adopcion, escalado, indicadores_disponibles, persistencia, estabilidad_impulsores, hitos_claros`; P `T (automática), novedad, incertidumbre_reducible, coste_eficiencia`; A `asimetria, valoracion, catalizadores, momento, invertibilidad`.

**Invocación.** `python3 ht03_puntuaciones.py ejemplos/ht03_entrada_ejemplo.json --salida resultado.json` (código 0; 2 si la entrada no es válida).

## 7. HT-07 · Medidor de legibilidad

**Qué hace.** Sobre texto plano o HTML (solo texto visible: excluye `script`, `style`, `head`, elementos `hidden`, `aria-hidden` o `display:none`):

- Índice de Fernández-Huerta (1959): `L = 206,84 − 0,60·P − 1,02·F`, con P = sílabas por 100 palabras y F = frases por 100 palabras; interpretación de muy fácil a muy difícil; umbral 70 (14.2).
- Silabeo español por reglas: dígrafos ch, ll, rr; «qu» y «gu» con u muda; diptongos, triptongos e hiatos (vocales fuertes contiguas o débil tildada junto a fuerte); «y» vocálica final; grupos consonánticos inseparables (pr, br, tr, dr, cr, gr, fr, kr, pl, bl, cl, gl, fl, kl); «tl» se separa (norma peninsular).
- Longitud media de frase y porcentaje de frases de más de 20 palabras, con la lista de frases largas.
- Jerga: lista inicial de más de 100 términos financieros (configurable con `--jerga`, en texto o JSON), sin distinguir mayúsculas ni tildes y con coincidencia más larga primero; indica si la primera aparición va explicada entre paréntesis (o con «es decir»).

**Invocación.** `python3 ht07_legibilidad.py informe.html [--jerga lista.txt] [--umbral 70] [--salida r.json]`. Código 0 si cumple el umbral; 1 si no; 3 si hay error de lectura.

**Limitaciones declaradas.** El silabeo es ortográfico y aproximado (la «h» intercalada se trata como consonante: «ahu-ma-do» se cuenta como cuatro sílabas). Los números cuentan como una palabra de dos sílabas.

## 8. HT-09 · Validador determinista G3

**Qué hace.** Valida un `paquete_oportunidades` (Anexo B V5.1) y devuelve `APTO`, `APTO_CON_ADVERTENCIAS` o `BLOQUEADO` con 19 comprobaciones, cada una con sus incidencias (`ruta`, `detalle`, `severidad`):

| ID | Comprobación | Bloquea cuando… |
|---|---|---|
| C01 | Campos obligatorios y valores permitidos | Falta o está vacío un campo del Anexo B (incluidos `tipo_activo`, `subtipo` e `invertibilidad`); valor fuera de vocabulario; tipo de activo desconocido (doce válidos); `tipo_activo` distinto del tipo en que figura |
| C02 | Opciones por tipo de activo | Más de 3 opciones o rangos distintos de 1..n |
| C03 | Menos de tres | Menos de 3 opciones sin `menos_de_tres_motivo` |
| C04 | Puntuaciones reconstruibles | RK no coincide con 0,45·A + 0,35·E + 0,20·T; total no múltiplo de 5; desglose (si se aporta) distinto de HT-03 |
| C05 | Elegibilidad y puertas | E < 60, A < 55 (A < 65 con T NA), T < 50; puerta G/PS no superada; banda marginal sin segunda pasada; PS3: `invertibilidad.universo_suficiente` distinto de `true` |
| C06 | Horizontes (8.3 V5.1, H1–H5) | Horizonte «No» para el tipo (p. ej., FON H1, DER H4–H5, MON H4–H5, TCV H5, INM H1, ALT H1–H2); «Limitado» sin catalizador ni `justificacion_horizonte` (con justificación y sin catalizador: advertencia); horizonte sin PRG- |
| C07 | Probabilidad numérica (R13) | `prob` sin certificado vigente para tipo × horizonte (y método, si consta) |
| C08 | Evidencias y cálculos (R7) | Listas vacías; CLM- sin EVD (si se aporta `--trazas`); CALC- sin artefacto (si se aporta `--artefactos`) |
| C09 | Objeciones (R12) | Objeción fuerte sin resolver; objeción moderada sin respuesta |
| C10 | Relevancia decisional | La regla del Anexo A exige ALTA y se declara otra |
| C11 | Encargo para el Bloque B | Opción con `ENVIAR_A_BLOQUE_B` sin encargo; encargo sin alguno de los campos del Anexo B V5.0 (`tipo_activo`, `subtipo`, `ambito`, `tesis`, `mecanismo`, `horizontes`, `pronosticos`, `catalizadores`, `riesgos`, `invalidacion`, `indicador_seguimiento`, `criterios_seleccion_sugeridos`, `metricas_clave`, `preguntas_para_B`, `evidencias`, `calculos`) o con `tipo_activo` distinto; advierte de horizontes o PRG- ajenos a la opción y de ámbito distinto |
| C12 | Legibilidad (HT-07) | Fernández-Huerta < 70 o informe ilegible |
| C13 | Credenciales (R8) | Patrones de claves, contraseñas o tokens; campos de valor de credencial (`valor_credencial`, `clave_api`) |
| C14 | Semáforo y apuestas | Solo advertencias (VERDE sin opciones, GRIS con opciones, apuestas > opciones) |
| C15 | Selección de activo concreto (frontera con el Bloque B, 2.4–2.5, R21) | `tipo_opcion` fuera de MERCADO/SECTOR/SUBSECTOR/TEMATICA/SEGMENTO/FACTOR/ESTILO/ESTRATEGIA (INSTRUMENTO_GENERICO e INDUSTRIA se retiraron; INDUSTRIA → SUBSECTOR); falta o está incompleto `ambito` (incluye, excluye, región); falta `indicador_seguimiento`; aparece el campo retirado `vehiculos_genericos` (en la opción o en el encargo); ISIN válido en nombre, tesis o ámbito (los nombres concretos solo caben en `ejemplos_ilustrativos`) |
| C16 | Oportunidad duplicada en dos tipos (regla 5 de 2.6) | Dos opciones de tipos distintos con el mismo nombre normalizado o el mismo ámbito normalizado (`incluye` + `region`, sin tildes, mayúsculas, signos ni palabras vacías), o el mismo `opp_id` en dos tipos; en el mismo tipo solo advierte |
| C17 | Horizonte principal y naturaleza de la inversión (8.3, V5.1) | `horizonte_principal` o `naturaleza_inversion` ausentes o fuera de vocabulario; principal que no figura entre los horizontes de la opción; principal en celda «No» del tipo; principal fuera del rango de su naturaleza (TACTICA H1–H2, LIQUIDEZ H1–H3, CICLICA y PRIMA_RIESGO H2–H4, VALORACION H3–H4, ESTRUCTURAL H4–H5) sin `justificacion_horizonte`. Con justificación, o principal «Limitado» sin catalizador: advertencia |
| C18 | Pronósticos H5 (R13, V5.1) | H5 con probabilidad numérica (aunque haya certificado: H5 nunca se certifica); sin banda verbal; sin hitos o con menos de 3; hitos sin `HIT-`, fecha, indicador o criterio; primer hito anterior a la fecha del paquete. Primer hito a más de 12 meses o más de 24 meses entre hitos: advertencia |
| C19 | Supuestos declarados (6.2.9, V5.1) | `supuestos_declarados` que no es lista o con supuestos sin texto o sin `cns_id` CNS-; sin `efecto_si_falso`: advertencia |

**Invocación.**

```bash
python3 ht09_validador_g3.py ejemplos/paquete_oportunidades_ejemplo.json \
  --certificados ejemplos/certificados_ejemplo.json \
  --informe-visual ejemplos/informe_visual_ejemplo.html \
  --desgloses ejemplos/desgloses_ejemplo.json \
  --trazas ejemplos/trazas_ejemplo.json --artefactos ejemplos/artefactos_ejemplo.json
```

Con todas las entradas, el ejemplo da `APTO`; sin certificados da `BLOQUEADO` (C07: probabilidad numérica en RV×H3). Opciones: `--parametros` (F10 en formato HT-03), `--umbral-fh`, `--salida`. Códigos de salida: 0 APTO, 1 APTO_CON_ADVERTENCIAS, 2 BLOQUEADO, 3 error de entrada.

**Informe de seguimiento de opción (V5.1).** `validar_seguimiento(informe, parametros, texto_breve)` (CLI: `--seguimiento`) valida el JSON `informe_seguimiento_opcion` del ciclo C6: S01 campos y valores; S02 una sola recomendación coherente con 7.11.4 (`PROPONER_ENVIO_A_B` solo si vuelve a ser elegible con los umbrales vigentes, sin objeciones fuertes abiertas y con `paquete_para_bloque_B`); S03 RK y elegibilidad reconstruibles; S04 pronósticos abiertos con PRG- y H5 con el estado de sus hitos; S05 credenciales; S06 brevedad (≤ 300 palabras, advertencia).

**Campos opcionales que HT-09 aprovecha si existen en la opción:** `puertas` (G1–G4, PS1–PS8), `cluster`, `vigente`, `objeciones[].resuelta`, `horizontes.Hn.advertencia` (exigida en H1), `horizontes.Hn.metodo` y `ejemplos_ilustrativos` (no se inspeccionan en C15: son ilustración permitida).

## 9. HT-05 · Planificador

Especificación en `ht05_planificador_ejemplo.md`: expresiones cron por defecto de C1 (ejecución el sábado 06:00 y entrega el lunes 07:00), C4 (barrido de enlaces el domingo 04:00, reintento de 24 h, revisiones mensual y trimestral, CT-21) y C5 (resolución diaria de pronósticos, revisiones mensual y trimestral), con `CRON_TZ` en la zona horaria del usuario (por defecto, `Europe/Madrid`) y las periodicidades alternativas que el Broker puede fijar por CT-04.

## 10. Decisiones de diseño relevantes

1. **RK redondeado al entero** con empates hacia abajo (el Documento 0 no fija su redondeo; el ejemplo del Anexo B, RK 72 con A 70, E 75, T 70, es coherente con esta regla).
2. **Banda marginal sin segunda pasada = no elegible (PS8)**; se consideran los umbrales de elegibilidad y el de GC2 (E 50).
3. **Diversidad sin alternativa a ≤ 10 puntos**: se mantienen las tres del mismo clúster y se declara la excepción.
4. **ROTO** se confirma con un segundo fallo ≥ 24 h después del primero; la baja por «dos barridos» se sugiere cuando el primer fallo tiene ≥ 7 días y no hubo aciertos intermedios.
5. **Relevancia decisional**: subestimar (no marcar ALTA cuando la regla lo exige) bloquea; sobrestimar solo advierte.
6. **Objeción moderada sin respuesta** bloquea (F4 exige respuesta a fuertes y moderadas).
7. **Duplicados entre tipos (C16)**: se compara por nombre y por ámbito normalizados; el criterio es conservador (coincidencia exacta tras normalizar) para no bloquear por similitudes legítimas; las coincidencias parciales quedan para el Analizador y el Auditor.
8. **ISIN (C15)**: se exige dígito de control válido para evitar falsos positivos con palabras en mayúsculas. Los tickers no se detectan (demasiados falsos positivos); su control es del Auditor.
9. **`methodology_version`**: se aceptan 4.x y 5.x sin advertencia (el Anexo A del Documento 0 V5.0 mantiene la versión de metodología 4.0).
