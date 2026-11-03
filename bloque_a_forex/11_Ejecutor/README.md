# Ejecutor programático del Bloque A Forex (V1.0, actualizado V1.1)

**Bloque A Forex · Robot Investor · 02/11/2026 · actualizado V1.1 (03/11/2026)** · Subordinado al Documento 0 del Bloque A Forex V1.1.

**Novedades V1.1 (03/11/2026).** Contratos CT-23, CT-24 y CT-25 (`version_contrato` FX-1.1); archivo **F11** «Registro de seguimientos encargados» (`F11_registro_seguimientos.jsonl`, propietario AG-01); **naturaleza de la inversión y horizonte principal** coherentes en cada opción (`horizontes.py`; HT-09 C17); **H5 «limitado»** con hitos HIT-FX- congelados en F4 y evaluados en F6 por el Evaluador (`resolver_hitos`); **consultas al Broker** (`comunicacion.Consultas`: bloqueante con punto de control —pausa el segmento afectado sin consumir presupuesto— o no bloqueante con supuesto declarado; vencimiento; agrupación; recurrentes → CT-22); **credenciales** por CT-25 con **bóveda simulada de HT-01** (`herramientas/boveda.py`; ningún valor llega a mensajes, archivos ni agentes); **seguimiento encargado de opción** (`seguimiento.py`: alta, modificación, pausa, reanudación, cancelación inmediata y ciclo C6 con informe breve + JSON validado por HT-09 `validar_seguimiento`). Nuevos subcomandos `seguimiento`, `consulta-broker` y `credencial` (sección 6). `methodology_version` FX-1.1. Pruebas: `tests/test_v11.py` (14).

Este README está escrito para quien va a **hacer backtests** con el bloque: cómo instalarlo, qué datos necesita, cómo
lanzar un backtest sin fuga de información y cómo leer lo que exporta. Las secciones 6 a 10 explican lo que hace por
dentro para quien quiera auditarlo o modificarlo.

El paquete `bloque_a_forex` hace funcionar el Bloque A Forex de extremo a extremo con la API de Claude: los **21
agentes** con sus system prompts íntegros (`02_System_prompts`), los contratos CT-01…CT-25 y CT-06T, los archivos
F1–F6, F10, F11, RC y HA, las herramientas HT-01…HT-09 y un Motor de cálculo determinista con las fichas del Catálogo
Forex. Puede ejecutarse **como si** fuera una fecha histórica, sin fuga de información.

**Qué hace el Bloque A Forex.** Solo busca oportunidades cambiarias: delimita **ámbitos** (un par, un cruce, una cesta,
un bloque, una estrategia, una vista de volatilidad o un régimen cambiario) en **seis segmentos** (G10N G10 núcleo,
G10M G10 de materias primas y escandinavas, EMAS emergentes de Asia, EMLA emergentes de Latinoamérica, EMEA emergentes
de Europa, Oriente Medio y África, ESTR estrategias y cestas) y entrega al Bloque B un encargo para que elija el
instrumento (contado, forward, futuro, opción, ETF/ETC o CFD), el coste, la cobertura y la ejecución. El ejecutor
nunca propone instrumentos, tamaños ni niveles de entrada.

Estado de madurez (R22): **implementado, con pruebas automáticas superadas con un cliente simulado**. No está validado
con el modelo real: la calidad analítica de los agentes solo puede medirse ejecutándolo con la API.

---

## 1. Instalación

```bash
cd 11_Ejecutor
pip install -e .            # o: pip install -r requirements.txt
pip install -e ".[garch]"   # opcional: VOL-GARCH-001 (paquete arch)
python -m pytest -q tests   # batería de pruebas (≈ 3 minutos, sin red ni clave)
```

Requisitos: Python ≥ 3.10; `anthropic` 2.x, `jsonschema`, `numpy`, `pandas`, `scipy`, `PyYAML`. La orden de consola es
`bloque-a-forex` (o `python -m bloque_a_forex.cli`). El ejecutor lee el resto del paquete (prompts, plantillas, esquema
JSON, F7–F9) desde la carpeta padre; si lo mueve, fije `rutas.raiz_paquete` en el YAML o la variable
`BLOQUE_A_FOREX_RAIZ`.

## 2. Backtest en cinco minutos

```bash
# 1) Datos de prueba (sintéticos): 43 indicadores del universo de ejemplo + 30 series de tipos de interés TIPO-<ISO>
bloque-a-forex generar-sinteticos --desde 2021-01-04 --hasta 2026-10-30

# 2) Backtest semanal con el cliente simulado (comprueba la tubería; no mide nada)
bloque-a-forex --datos ejemplos/datos_sinteticos --salida ./bt backtest --desde 2026-07-03 --hasta 2026-09-25

# 3) Con el modelo real, sus datos y su universo (periodo POSTERIOR a la fecha de corte del modelo; ver 9.1)
export ANTHROPIC_API_KEY=sk-ant-...      # nunca en archivos (R8)
bloque-a-forex --cliente anthropic --datos MIS_DATOS --universo MI_UNIVERSO.csv --salida ./bt \
               backtest --desde 2026-07-03 --hasta 2026-12-25 --frecuencia semanal [--segmentos G10N,EMLA] [--anonimizar]
```

`ejemplos/salida_backtest_simulado/` contiene la salida del paso 2 (13 ciclos semanales, todos con dictamen G3 «APTO»;
29 de los 78 ciclos de segmento en arrastre verificado N1)
para ver los formatos sin ejecutar nada.

Para que dos ejecuciones con el modelo real sean idénticas: `--cliente replay --replay grabacion.jsonl --replay-modo
grabar` la primera vez (envuelve al cliente real; `BLOQUE_A_CLIENTE_BASE=mock` para grabar el simulado) y
`--replay-modo reproducir` después.

## 3. Datos que necesita (HT-01)

**Proveedor CSV** (`--datos CARPETA`): un archivo por serie, `<CODIGO>.csv`, con `fecha,cierre` como mínimo (admite
`apertura,maximo,minimo,volumen` y los alias `date`, `close`, `adj close`, `valor`). Fechas `AAAA-MM-DD`, sin
duplicados. Columna opcional `fecha_publicacion`: la fila solo es visible cuando `fecha_publicacion <= as_of`.

Series necesarias:

| Serie | Contenido | Uso |
|---|---|---|
| `<CODIGO>` de cada fila del universo | Tipo de cambio del par en notación de mercado (EURUSD = dólares por euro), índice de la cesta o de la estrategia en base 100, o nivel de volatilidad implícita | Señales, tendencia, riesgo, resolución de los pronósticos |
| `TIPO-<ISO>` por cada divisa que aparece en el universo (TIPO-USD, TIPO-EUR, TIPO-JPY, TIPO-MXN…) | Tipo a corto plazo en **% anual** (OIS o interbancario a 3 meses) | Carry (FX-CARRY-001), forward como predictor (RI-FWD), rentabilidad total |

Use una **hora de fijación única** para todos los pares (por defecto `ht01.hora_fijacion: "17:00 America/New_York"`, el
cierre de Nueva York; cámbiela si sus datos son el fixing WM/Reuters de las 16:00 de Londres o el tipo de referencia
del BCE). Las cestas y estrategias deben entregarse ya calculadas como índice (en rentabilidad total si quiere
pronósticos de rentabilidad total) y con la composición declarada en el universo.

**Guardia de fuga.** Con una fecha as_of activa, el proveedor nunca devuelve observaciones posteriores y pedirlas lanza
`FugaDeInformacion`; el Motor rechaza (`FUGA_DE_INFORMACION`) cualquier dato posterior a su fecha de corte; el almacén
filtra F1–F6 por la fecha en que se conoció cada entrada; los tipos de interés se leen con la misma guardia, así que el
carry y el forward de cada fecha solo usan tipos conocidos en ella.

Otros proveedores: `ProveedorSintetico` (pruebas: factor común del dólar + factor del segmento, tipos con decisiones
mensuales de ±25 pb; ficticio) y `ProveedorYahoo` (opcional, `yfinance`, **solo modo vivo**; no sirve las series
`TIPO-` ni los índices propios: cárguelos en CSV).

## 4. Universo (`--universo`, por defecto `config/universo_ejemplo.csv`, solo un ejemplo)

Cada fila es un **ámbito cambiario** y `codigo` es la serie HT-01 de su **indicador de seguimiento** (no un instrumento).

| Columna | Obligatoria | Contenido |
|---|---|---|
| `codigo` | sí | Código de la serie (EURUSD, USDJPY, FX-CARRY-G10, VOL-EURUSD-1M…) |
| `segmento` | sí | G10N, G10M, EMAS, EMLA, EMEA o ESTR (reglas de 2.6: la divisa menos líquida decide; tres o más divisas o una regla sistemática ⇒ ESTR) |
| `tipo` | sí | PAR, CRUCE, CESTA, BLOQUE, ESTRATEGIA, VOLATILIDAD o REGIMEN |
| `base`, `cotizada` | sí (vacía `base` en cestas) | Códigos ISO 4217 en convención de mercado (EUR/USD, USD/JPY, EUR/PLN, USD/MXN) |
| `convertible`, `ndf` | sí | `si`/`no`: convertible para un inversor minorista europeo; existe mercado no entregable |
| `controles_capitales` | no | `si`/`no` (suelo 4 de riesgo y relevancia ALTA) |
| `composicion` | en CESTA, BLOQUE y ESTRATEGIA | `AUD:LARGO:0.34;NZD:LARGO:0.33;NOK:LARGO:0.33;JPY:CORTO:0.5;CHF:CORTO:0.5` (los pesos de cada lado suman 1) |
| `divisa_financiacion`, `regimen`, `liquidez`, `nombre`, `indicador`, `notas` | no | Régimen de facto (LIBRE_FLOTACION, FLOTACION_ADMINISTRADA, BANDA, TIPO_FIJO, CAJA_CONVERSION, CONTROLES); liquidez alta/media/baja; texto (las `notas` se sanean, R9) |

El universo de ejemplo tiene 43 ámbitos: 9 en G10N (incluida una volatilidad implícita de EUR/USD), 8 en G10M, 8 en
EMAS (USD/INR con controles y NDF, USD/HKD con caja de conversión), 5 en EMLA, 7 en EMEA (USD/EGP con controles y
liquidez baja) y 6 en ESTR (carry G10, carry emergente, momentum G10, dólar amplio, cesta refugio y cesta
latinoamericana).

## 5. Qué exporta el backtest y cómo conectarlo a su backtester

Carpeta `--salida`:

**`senales.csv`** — una fila por opción publicada y fecha:

| Columna | Contenido |
|---|---|
| `fecha_asof`, `run_id`, `segmento`, `rango` | Fecha del ciclo (la señal solo usa información hasta esa fecha), RUN-FX-, segmento y posición 1–3 |
| `opp_id`, `tipo_opcion`, `nombre` | Oportunidad (OPP-FX-, estable mientras siga vigente con la misma dirección) |
| `par`, `direccion` | `EUR/USD` y `ALCISTA_BASE`/`BAJISTA_BASE` en PAR, CRUCE y REGIMEN; vacías en el resto |
| `composicion`, `divisa_financiacion` | `DIVISA:LADO:PESO;…` de la exposición propuesta (en un par, la base y la cotizada con peso 1) |
| `vista_volatilidad` | `ALZA:1M` o `BAJA:1M` en las opciones VOLATILIDAD |
| `indicador_seguimiento_simbolo`, `indicador_sube` | Serie del universo con la que se mide la idea y `si`/`no`: si la tesis espera que **suba esa serie** |
| `tipo_rentabilidad`, `divisa_medicion` | PRECIO_CONTADO (pares), RENTABILIDAD_TOTAL (estrategias) o NIVEL_VOLATILIDAD; divisa en que se mide |
| `carry_anual_pct`, `carry_signo` | Carry anual de la exposición a favor de la tesis (tipo de lo largo − tipo de lo corto) |
| `horizontes`, `horizonte_principal`, `banda`, `prob_interna` | p. ej. `H2\|H3`, `H3`; banda publicable y probabilidad interna de F4 (sin certificado no se publica) |
| `RK`, `A`, `E`, `T`, `riesgo_1a5`, `relevancia_decisional`, `siguiente_paso`, `vigente_nueva` | Puntuaciones HT-03 (A Forex), RISK-DD-001 v2.0 y reglas del Anexo A |

**Regla práctica para el backtester:** compre la serie `indicador_seguimiento_simbolo` si `indicador_sube = si` y
véndala si es `no` (en un par, `ALCISTA_BASE` equivale a `si`). Para medir en rentabilidad total sume el carry con los
tipos `TIPO-<ISO>` conocidos en cada fecha (o use `carry_anual_pct`, que ya está orientado a la tesis). Ejecute al
cierre siguiente a `fecha_asof` y mantenga hasta la fecha siguiente o hasta el `horizonte_principal`. El Bloque A no
dice con qué instrumento: eso lo decidiría el Bloque B.

**`pronosticos.csv`** — todos los PRG-FX- de F4 (también los de finalistas no publicadas, `en_informe = False`, para
evaluar sin sesgo de selección): `prg_id, opp_id, run_id, fecha_emision, segmento, simbolo, par, direccion,
composicion, horizonte, fecha_resolucion, sentido_indicador (SUBE|BAJA), tipo_rentabilidad, divisa_medicion,
carry_anual_pct_indicador, referencia_segmento, umbral, banda_verbal, prob_interna, prob_publicada,
prob_paseo_aleatorio, prob_forward, cambio_forward, nivel_referencia, hora_fijacion, en_informe, estado
(ABIERTO|RESUELTO|NO_RESOLUBLE), fecha_resuelto, rent_proxy, rent_referencia, valor_observado, resultado_binario, brier,
log_score, brier_ref, brier_forward, acierto_forward, comprobacion_fuga, version_de`.

- Un pronóstico acierta si el indicador se mueve en el `sentido_indicador` entre el cierre ≤ `fecha_emision` y el cierre
  ≤ `fecha_resolucion` (en RENTABILIDAD_TOTAL se suma el carry congelado en la emisión).
- **Referencias ingenuas obligatorias** (8.4 y Anexo A; RI-PA y RI-FWD del Catálogo): `prob_paseo_aleatorio` = 0,5
  (paseo aleatorio sin deriva) y `prob_forward` = probabilidad del mismo suceso con una lognormal centrada en el
  forward (`cambio_forward` = −carry·plazo, paridad cubierta) con la volatilidad EWMA conocida en la emisión.
  `brier_ref` es el Brier del paseo aleatorio y `brier_forward`, el del forward. En divisas, batir al paseo aleatorio
  es difícil (Meese-Rogoff): la referencia real es esa, no el 50 % de una moneda al aire.
- `rent_referencia` es la rentabilidad de la referencia del segmento (8.4): cesta equiponderada de los indicadores del
  segmento en EMAS, EMLA y EMEA; vacía (rentabilidad en exceso nula) en G10N, G10M y ESTR.

**`metricas.json`** — por `segmento|horizonte`: n, acierto (IC de Wilson y prueba binomial frente a 0,5), Brier, Brier
del paseo aleatorio y del forward, BSS frente al paseo aleatorio (IC 90 % por bootstrap de bloques) y frente al
forward, acierto del forward, log-score, ECE con su nulo, Diebold-Mariano con HLN, calibración global, rentabilidad
media del top-3 y frente a la referencia del segmento; métricas solo de opciones publicadas; certificados (Anexo A:
n ≥ 100, IC 90 % del BSS > 0 con Holm, ECE ≤ q90 del nulo y < 0,15); consumo; advertencias.

**`consumo.csv`** — por RUN: llamadas, tokens (entrada, salida, escritura y lectura de caché), búsquedas web, UC (LLM y
Motor) y coste (vacío mientras `precios_por_millon` esté vacío).

**`entregables/AAAA-MM-DD/`** — informe técnico (`.md`), informe visual (`.html`: monedas que suben y bajan, lista,
termómetro de la divisa base, semáforo de los seis segmentos, tarjetas con banderas) y paquete JSON (esquema del
Bloque A Forex V1.0) de cada fecha. **`estado/`** — F1–F6, F10, RC, HA en JSONL append-only con cadena de hash.

Por defecto, tras el último ciclo se resuelven los pronósticos con los datos posteriores disponibles
(`--sin-resolucion-final` para desactivarlo).

## 6. Otras órdenes

```bash
bloque-a-forex --datos DATOS --estado ./estado --salida ./entregables --as-of 2026-06-05 ciclo [--segmentos G10N,ESTR]
bloque-a-forex --datos DATOS --estado ./estado peticion --json ejemplos/peticiones/peticion_ad_hoc.json
bloque-a-forex --datos DATOS --estado ./estado consulta "¿Por qué no aparece el franco suizo esta semana?"
bloque-a-forex --datos DATOS --estado ./estado decision --json ejemplos/peticiones/decision_ejemplo.json
bloque-a-forex --datos DATOS --estado ./estado evaluar       # C5: resolver vencidos, métricas, certificados, lecciones
bloque-a-forex --datos DATOS --estado ./estado estado        # colas, consumo, últimos runs, integridad
bloque-a-forex --salida ./informes_enlaces verificar-enlaces # HT-02 sobre F7, F8, F9 y FM (sin --aplicar no modifica)
```

**V1.1: seguimiento encargado (CT-24, C6, F11), consultas al Broker (CT-23) y credenciales (CT-25).**

```bash
# Encargos de seguimiento de una opción de F3 (frecuencia a elección del Broker; aviso —no veto— si es corta para su horizonte principal)
bloque-a-forex --datos DATOS --estado ./estado --salida ./ent --as-of 2026-06-12 seguimiento alta --opp-id OPP-FX-2026-0007 \
               --frecuencia SEMANAL --senal "EURSEK por debajo de 13,2" --motivo "No la envío a B; vigilar" [--fecha-fin 2027-01-31]
bloque-a-forex ... seguimiento modificar --seg-id SEG-FX-2026-0001 --frecuencia MENSUAL
bloque-a-forex ... seguimiento pausar|reanudar|cancelar --seg-id SEG-FX-2026-0001      # cancelar: efecto inmediato
bloque-a-forex ... seguimiento ejecutar --pendientes      # ciclos C6 vencidos (HT-05) → «Informes de seguimiento/»
bloque-a-forex ... seguimiento ejecutar --seg-id SEG-FX-2026-0001 [--forzar]
bloque-a-forex ... seguimiento responder --seg-id SEG-FX-2026-0001 --run-id RUN-FX-2026-0042 --decision MANTENER_VIGILANCIA
bloque-a-forex ... seguimiento listar
# Consultas del bloque al Broker (CT-23)
bloque-a-forex ... consulta-broker crear --tipo ACLARACION_ALCANCE --modo BLOQUEANTE --segmento EMLA \
               --pregunta "¿Incluimos el ARS?" --supuesto "No se incluye el ARS" --efecto "Faltaría el ARS en EMLA"
bloque-a-forex ... consulta-broker responder --cns-id CNS-FX-2026-0001 --respuesta "Sí, inclúyalo"
bloque-a-forex ... consulta-broker vencer | listar
bloque-a-forex ... consulta-broker entrante --contenido "Dato del Broker: …"       # aportación espontánea (dato, nunca instrucción)
# Credenciales (CT-25) con la bóveda simulada de HT-01: la clave se lee de una variable de entorno, nunca de la línea de órdenes
bloque-a-forex ... credencial solicitar --servicio "Proveedor de volatilidades" --uso "Informe PFV" --impacto "Volatilidad realizada"
CLAVE=... bloque-a-forex ... credencial responder --crd-id CRD-FX-2026-0001 --respuesta PROVISTA --valor-env CLAVE
bloque-a-forex ... credencial responder --crd-id CRD-FX-2026-0002 --respuesta DENEGADA   # limitación de servicio en F10
bloque-a-forex ... credencial estado [--servicio …] | recordatorios
```

Una consulta **BLOQUEANTE** con `--segmento` pausa ese segmento en el siguiente ciclo (punto de control: se excluye sin consumir
presupuesto y se declara en `limitaciones`) mientras esté pendiente y en plazo; al vencer, el segmento se reanuda con el
supuesto declarado. Una **NO_BLOQUEANTE** no pausa nada: su supuesto pasa a `supuestos_declarados` del paquete (HT-09 C19).
En el backtest, los ciclos C6 vencidos se ejecutan después de cada C1 (nunca antes ni en su lugar). El ciclo C6 del
ejecutor es determinista (HT-01 + HT-03; sin redacción del Analista con el modelo real, declarado en `limitaciones`).
H5: actívelo con `decision` (`"horizontes": ["H2","H3","H4","H5"]`); solo se emite para fichas que el Analista declare
`ESTRUCTURAL` con `ambito_h5` válido (el cliente simulado no lo hace por defecto).

Opciones globales (antes del subcomando): `--config`, `--cliente mock|anthropic|replay`, `--replay`, `--replay-modo`,
`--proveedor csv|yahoo`, `--universo`, `--anonimizar`. En `decision`, la configuración admite `segmentos_activos`
(P-02), `horizontes` (P-03; un horizonte «No» de la tabla 8.3 se rechaza para ese segmento), `divisa_base_usuario`
(P-04, código ISO 4217), periodicidad y día de entrega.

## 7. Configuración (`config/por_defecto.yaml`, fusionable con `--config`)

| Clave | Uso |
|---|---|
| `divisa_base_usuario` | EUR por defecto: termómetro del informe visual y `lectura_divisa_base` |
| `segmentos_activos` | Los seis por defecto (P-02) |
| `modelos.AG-xx`, `max_tokens.AG-xx` | Modelo y límite de salida por agente. Por defecto: Analizador, Contrarias y Evaluador `claude-opus-5-5`; Coordinador y Curador `claude-haiku-5-5`; el resto `claude-sonnet-5-5`. **Compruebe los identificadores en la documentación de Anthropic** |
| `presupuesto_uc` | Anexo A: N0 1, N1 5 y N2 18 por segmento, N3 50 por petición, 6 por capa transversal, ciclo semanal ≤ 140 UC |
| `indices_referencia` | Referencia del segmento (8.4): `NINGUNA` (rentabilidad en exceso nula) en G10N, G10M y ESTR; `CESTA` en EMAS, EMLA y EMEA |
| `ht01.hora_fijacion` | Hora y zona de fijación de los niveles (`"17:00 America/New_York"`) |
| `gc0` | Cambio material (Anexo A): una opción vigente o finalista, o el índice representativo del segmento (`indice_representativo`: dólar amplio en G10N; si no, cesta equiponderada), se mueve > 1,5 σ semanales, o lo hace al menos un tercio de los pares vigilados; cambio de tipos de un banco central del segmento (series `TIPO-<ISO>`); invalidación a < 10 % de activarse (queda menos del 10 % del recorrido entre el nivel de alta y el umbral); `eventos_calendario` para sorpresas macro e intervenciones |
| `horizontes` | H1 5 sesiones, H2 4 semanas, H3 6 meses, H4 12 meses (punto de resolución) |
| `evaluacion` | Muestras mínimas (30 / 100), ECE máximo, réplicas de bootstrap, `aplicar_recalibracion` (falso = modo sombra) |
| `backtest` | Frecuencia, día de la semana (viernes), `fecha_corte_modelo`, `anonimizar` |
| `precios_por_millon` | **Vacíos a propósito**: rellénelos con la tarifa vigente |

## 8. Qué hace un ciclo

**F0** — el Evaluador resuelve lo vencido (C5); **GC0 determinista** por segmento (opción vigente o finalista,
índice representativo o un tercio de los pares vigilados > 1,5 σ semanales; cambio de tipos de un banco central;
invalidación cumplida o cercana; eventos de calendario; lecciones nuevas). Sin cambio material ⇒ N1 «arrastre verificado».
**F0b** — capas transversales (CT-06T, en paralelo y antes del cribado): AG-09 (bancos centrales y macro cambiaria) y
AG-21 (posicionamiento, flujos y volatilidad) reciben los tipos por divisa y las señales HT-01 y devuelven un informe
con identificador TRV-FX-; en un ciclo sin cambio material se reutilizan los del ciclo anterior (declarado).
**F1–F2** — el Motor calcula las señales de todo el universo (FX-MOM-001, FX-VOL-001, FX-TREND-001, RISK-DD-001 v2.0,
ST-DESC-001, FIN-CAGR-001 y FX-CARRY-001 v2.0 con los tipos HT-01) y una señal compuesta con dirección
(momentum, tendencia, valor y carry ajustado); los seis Analistas de segmento trabajan en paralelo con los informes
transversales. El ejecutor **normaliza la notación**: el par sale del universo; en PAR, CRUCE y REGIMEN la composición
se reconstruye desde la dirección; en las cestas se valida (pesos por lado = 1) o se toma la del universo; en
VOLATILIDAD la vista va en `vista_volatilidad`. GC2 (E ≥ 50) y GC3 (5 mejores por RK). **F3–F4** — Prospectiva
(pronósticos frente al paseo aleatorio y al forward) y Contrarias por lotes; el Analista responde a las objeciones.
**F5** — puertas G1–G4 y PS1–PS8 (PS3 = convertible, NDF o exposición alternativa, sin controles que impidan la
exposición; PS4 = exposición cuantificada), HT-03 (A Forex: asimetría 30, valoración 20, carry 15, catalizadores 15,
momento y posicionamiento 10, convertibilidad 10; RK = 0,45·A + 0,35·E + 0,20·T; diversidad: ≤ 2 por clúster y una
divisa con la misma dirección en ≤ 2 opciones del segmento), **sin duplicados entre segmentos** (regla 4 de 2.6),
integración del Analizador y **contradicciones entre segmentos** (9.6.6: una misma divisa como **pata activa** de la
tesis —la que se pronostica— larga en un segmento y corta en otro se justifica con mecanismos u horizontes distintos o
sale la opción de menor RK; el USD o el EUR como contrapartida o financiación no cuentan y van a la exposición agregada). **F6** — HT-09 (27 comprobaciones,
incluidas G3-FX-01…11). **F7** — Redactor, tres entregables, HT-07 (≥ 70) y segunda pasada de HT-09 con coherencia entre
entregables y el esquema JSON. **F8** — congelación de PRG-FX- en F4, F1, F3, F5 y CT-02. **F9** — auditoría asíncrona.

## 9. Limitaciones y advertencias

1. **Fuga por conocimiento del modelo.** El modelo conoce los tipos de cambio y las decisiones de los bancos centrales
   anteriores a su fecha de corte; en backtest se le pide que trabaje como si fuera la fecha as_of, pero no puede
   «olvidar». Backtestee **periodos posteriores** a `backtest.fecha_corte_modelo` (valor orientativo: compruébelo);
   si el periodo es anterior, `metricas.json` lo advierte. `--anonimizar` sustituye los códigos y los nombres de los
   indicadores por alias («G10N03», «Ámbito G10N03») y rebasa los niveles a 100, pero en divisas es una mitigación
   **muy débil**: el par, la composición (códigos ISO), los tipos de interés y la forma de la serie siguen visibles y
   bastan para reconocer el ámbito y el periodo.
2. **Búsqueda web desactivada en backtest**; la evidencia es sobre todo de mercado (HT-01) y de las referencias de
   F7–F9 con año ≤ as_of.
3. **Motor**: fichas implementadas en este ejecutor (Catálogo Forex, estado IMPLEMENTADO): ST-DESC-001, FIN-CAGR-001,
   FX-MOM-001 (sobre contado), FX-VOL-001, VOL-GARCH-001 (requiere `arch`), FX-TREND-001, RISK-DD-001 v2.0, FX-CORR-001,
   ML-CLUS-001, FX-CARRY-001 v2.0, FX-FWD-001, FX-PPP-001 (versión sencilla), FX-RW-001 (versión sencilla),
   FC-EVAL-001, FC-CAL-001 y SCORE-RK-001 v2.0. El resto ⇒ `RECHAZADO METODO_NO_IMPLEMENTADO` con la alternativa de la
   ficha; las fichas del Catálogo V5.0 retiradas (ACC-MOM-001, ACC-FACT-001, DER-OPT-001, ACC-ERP-001, ACC-VAL-001,
   CMD-CURVE-001…) ⇒ `FUERA_DE_CATALOGO` con la ficha cambiaria sustituta (sección 10 del Catálogo).
4. **Cliente simulado**: con `MockClient` las «opiniones» son reglas sintéticas (la dirección sale de la señal
   compuesta); el backtest simulado no dice nada de la capacidad del bloque.
5. Calendario de lunes a viernes sin festivos; una sola hora de fijación para todos los pares; sin datos de
   posicionamiento CFTC, volatilidad implícita ni base cruzada en el proveedor sintético (los informes transversales
   simulados lo declaran como laguna).
6. El forward como predictor se reconstruye por paridad cubierta con los tipos `TIPO-<ISO>` (sin base cruzada ni
   puntos cotizados); en divisas con NDF la diferencia puede ser material.
7. GC0 usa el índice representativo, las opciones vigentes y finalistas y el umbral de un tercio de los pares vigilados;
   en el ejemplo, 33 de 78 ciclos de segmento quedan en N1 y los ciclos semanales tras el primero cuestan 13–27 UC.
   Las sorpresas macro y las intervenciones no se detectan solas: se declaran en `gc0.eventos_calendario`.

## 10. Decisiones de diseño relevantes

- **Identificadores** con el infijo FX (Anexo C Forex): RUN-FX-, OPP-FX-, TND-FX-, PRG-FX-, CLM-FX-, EVD-FX-, CALC-FX-,
  QRY-FX-, LEC-FX- y TRV-FX-.
- **Dirección** (2.4): `direccion` solo en PAR, CRUCE y REGIMEN (referida a la base); en CESTA, BLOQUE y ESTRATEGIA va en
  `composicion` (LARGO/CORTO y peso) con `divisa_financiacion`; en VOLATILIDAD, en `vista_volatilidad` (ALZA/BAJA y
  plazo). El pronóstico se formula siempre sobre la serie del indicador (`indicador_sube`).
- **Carry** de cada opción = carry del indicador tal como cotiza (lo largo frente a lo corto, FX-CARRY-001 con los
  tipos HT-01) con el signo de la tesis; el ajuste por volatilidad usa la volatilidad realizada. El riesgo 1–5 es el de
  RISK-DD-001 v2.0 con el suelo 4 para divisas con controles, tipos fijos y opciones REGIMEN.
- **Relevancia decisional** (nota 3 del Anexo A): ALTA con riesgo ≥ 4, reversibilidad baja, horizonte H4 con riesgo ≥ 3 o
  liquidez baja, E < 70 con A ≥ 75, tipo REGIMEN o divisa emergente de liquidez baja (regla de HT-09, que usa el ejecutor).
- **Tipo de rentabilidad**: PRECIO_CONTADO en pares, cruces, cestas y regímenes; RENTABILIDAD_TOTAL en estrategias
  (índices); NIVEL_VOLATILIDAD en las opciones VOLATILIDAD (2.4). Divisa de medición: la cotizada del par o la de
  financiación.
- **Exposición agregada por divisa** (14.1) = suma de pesos firmados de todas las opciones: «larga»/«corta» con
  «moderada» si |neta| < 1 y «fuerte» si ≥ 2; `lectura_divisa_base` se deriva de la exposición neta de la divisa base.
- **Carga robusta de archivos**: prompts, plantillas, esquema y F7–F9/FM se buscan por el prefijo del nombre con
  cualquier sufijo de versión, prefiriendo los que contienen «Bloque A Forex». Si un Analista de segmento o una capa
  transversal no tiene prompt Forex, se usa el marco común de los Analistas (o el prompt del Bloque A general) en modo
  degradado con incidencia en HA; para el resto de agentes, error.
- El paquete de síntesis que valida HT-09 incluye `puertas`, `cluster`, `vigente`, la advertencia de H1 y
  `objeciones[].resuelta`; el entregable JSON los elimina y conserva `x_referencia`, `x_indicador_sube`,
  `x_lectura_conjunto` y `x_lectura_divisa_base_analizador`.
- HT-02, HT-03, HT-07 y HT-09 son copias literales de `10_Herramientas` (`bloque_a_forex/herramientas/referencia/`);
  una prueba comprueba que no divergen.

## 11. Estructura

```
11_Ejecutor/
  pyproject.toml · requirements.txt · README.md
  config/por_defecto.yaml · config/universo_ejemplo.csv
  bloque_a_forex/
    llm.py (Anthropic, Mock, Replay) · mock_respuestas.py · prompts.py · contratos.py · agentes.py · consumo.py
    almacen.py · orquestacion.py · sintesis.py · redaccion.py · evaluador.py · backtest.py · cli.py · fx.py
    referencias.py · anonimizacion.py · configuracion.py · horizontes.py · comunicacion.py · seguimiento.py (V1.1)
    motor/ (operaciones.py, evaluacion.py, servicio.py)
    herramientas/ (ht01_datos, boveda, ht02, ht03, ht04_graficos, ht05_planificador, ht06_indice, ht07, ht08_monitor, ht09, referencia/)
  tests/ (test_unitarias, test_integracion, test_autocritica, test_forex, test_v11; MAPA_PLAN_DE_PRUEBAS.md; RESULTADOS.txt)
  ejemplos/datos_sinteticos/ · ejemplos/peticiones/ · ejemplos/salida_backtest_simulado/
```
