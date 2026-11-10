# Ejecutor programático del Bloque A (V1.2)

**Bloque A · Robot Investor · Versión óptima V5.0 · 02/11/2026 · actualizado V5.1 (03/11/2026)** · Subordinado al Documento 0 óptima V5.1. Cambios V5.1 (ejecutor V1.2): horizonte H5 con hitos HIT- y horizonte principal con naturaleza de la inversión; contratos CT-23 a CT-25; archivo F11; subcomandos `seguimiento`, `consulta-broker` y `credencial` (bóveda simulada de HT-01); 13 pruebas nuevas (`tests/test_v51.py`).

Programa en Python que hace funcionar el Bloque A de extremo a extremo con la API de Claude: los 25 agentes (doce Analistas de tipo de activo: AG-03..AG-09 y AG-21..AG-25) con sus system prompts íntegros (`02_System_prompts`), los contratos CT-01…CT-25, los archivos F1–F6, F10, F11, RC y HA, las herramientas HT-01…HT-09 y un Motor de cálculo determinista. Puede ejecutarse **como si** fuera una fecha histórica, sin fuga de información, para que un ingeniero haga sus propios backtests y conecte las señales y los pronósticos a su backtester.

**Función del Bloque A (V5.0).** El bloque solo busca oportunidades: delimita **ámbitos** de inversión (mercado, sector, subsector, temática, segmento, factor, estilo o estrategia) en cualquiera de los **doce tipos de activo** (RV, RF, DIV, MP, IDX, FON, DER, INM, CRI, ALT, MON, TCV) y entrega al Bloque B un encargo para que localice los mejores activos concretos. El ejecutor no selecciona ni compara activos, instrumentos, costes ni plataformas: cada opción lleva su `ambito`, su `indicador_seguimiento` (un símbolo del universo con el que se miden la tendencia y los pronósticos), su `invertibilidad` y su `paquete_para_bloque_B`.

Estado de madurez (R22): **implementado, con pruebas automáticas superadas con un cliente simulado**. No está validado con el modelo real: la calidad analítica de los agentes solo puede medirse ejecutándolo con la API.

---

## 1. Instalación

```bash
cd 11_Ejecutor
pip install -e .            # o: pip install -r requirements.txt
pip install -e ".[garch]"   # opcional: VOL-GARCH-001 (paquete arch)
python -m pytest -q tests   # batería de pruebas (≈ 1,5 minutos, sin red ni clave)
```

Requisitos: Python ≥ 3.10; `anthropic` 2.x, `jsonschema`, `numpy`, `pandas`, `scipy`, `PyYAML`. El ejecutor lee el resto del paquete (prompts, plantillas, esquema JSON, F7–F9) desde la carpeta padre; si lo mueve, fije `rutas.raiz_paquete` en el YAML o la variable `BLOQUE_A_RAIZ`.

## 2. Clave de API

```bash
export ANTHROPIC_API_KEY=sk-ant-...      # nunca en archivos (R8)
bloque-a --cliente anthropic --datos MIS_DATOS ciclo
```

Sin clave, use `--cliente mock` (por defecto). Para reproducir exactamente una ejecución real: `--cliente replay --replay grabacion.jsonl --replay-modo grabar` la primera vez (envuelve al cliente real; `BLOQUE_A_CLIENTE_BASE=mock` para grabar el simulado) y `--replay-modo reproducir` después.

Detalles del cliente real (`bloque_a/llm.py`, comprobados contra el SDK `anthropic` 2.3 instalado):

- `messages.create` con `system` como lista de bloques de texto: el prompt íntegro del agente y un bloque fijo de interfaz, con `cache_control: {"type": "ephemeral", "ttl": "1h"}` en el último (caché de prompts). Todo lo variable va en el mensaje de usuario, para que la caché sea efectiva.
- Búsqueda web: herramienta de servidor `{"type": "web_search_20260318", "name": "web_search", "max_uses": 5}`, solo para AG-14, AG-15 y AG-16 y **solo en modo vivo**. Se gestiona `stop_reason = "pause_turn"` reenviando el contenido y continuando.
- Se registran `input_tokens`, `output_tokens`, `cache_creation_input_tokens`, `cache_read_input_tokens` y `server_tool_use.web_search_requests`.
- Salida estructurada opcional (`llm.salida_estructurada: true` → `output_config.format` con el esquema JSON); por defecto desactivada: el ejecutor valida con `jsonschema` y hace un reintento de reparación; si falla, el resultado queda PARCIAL y se registra en HA.

## 3. Configuración

`config/por_defecto.yaml` (se fusiona con el YAML que pase con `--config`). Claves principales:

| Clave | Uso |
|---|---|
| `modelos.AG-xx` | Modelo por agente. Por defecto: Analizador, Contrarias y Evaluador `claude-opus-5-5`; Coordinador y Curador `claude-haiku-5-5`; el resto `claude-sonnet-5-5`. **Compruebe los identificadores en la documentación de modelos de Anthropic** antes de usar el cliente real. |
| `max_tokens.AG-xx` | Límite de salida por agente |
| `prompts.marco_comun_si_falta` | Si falta el prompt específico de un Analista de tipo de activo, usar el «Marco común de los Analistas de tipo de activo (plantilla)» con incidencia en HA (modo degradado; por defecto `true`) |
| `presupuesto_uc` | UC por nivel (N0 1 · N1 5 por tipo · N2 18 por tipo · N3 50 por petición), ciclo semanal con los doce tipos ≤ 240, reparto por fases, ampliación sin autorización +25 % (Anexo A V5.0) |
| `uc` | Conversión tokens → UC (ver 8) y UC de los cálculos deterministas del Motor |
| `precios_por_millon` | **Vacíos a propósito**: rellénelos con la tarifa vigente; mientras sean `null`, el coste queda vacío en `consumo.csv` |
| `horizontes` | H1 = 5 sesiones, H2 = 4 semanas, H3 = 6 meses, H4 = 12 meses |
| `indices_referencia` | Referencia de comparación por tipo de activo (8.4): símbolo, `CESTA` (equiponderada del tipo), `SUBYACENTE` (columna `subyacente` del universo; DER) o `NINGUNA` (pronóstico absoluto; TCV). Por defecto: RV e IDX `ACWI`, RF `AGG`, DIV y FON `CESTA`, MP `DBC`, DER `SUBYACENTE`, INM `REET`, CRI `BTC-USD`, ALT `PSP`, MON `XEON.DE` (€STR), TCV `NINGUNA`. Los símbolos son aproximaciones disponibles en el universo de ejemplo de las referencias de 8.4; el operador las ratifica en F10 |
| `gc0` | Banda de cambio material (1,5 σ semanales, invalidación a < 10 %, eventos de calendario) |
| `busqueda_web` | Activación en vivo (en backtest siempre desactivada) |
| `evaluacion` | Muestras mínimas (30 / 100), ECE máximo, réplicas de bootstrap, `aplicar_recalibracion` (falso = modo sombra) |
| `backtest` | Frecuencia, día de la semana de las fechas as_of, `fecha_corte_modelo`, `anonimizar` |
| `auditoria` | Auditor en vivo (sí) y en backtest (no, por coste) |

## 4. Datos (HT-01) y universo

**Proveedor CSV** (`--datos CARPETA`): un archivo por símbolo, `<SIMBOLO>.csv`, cabecera `fecha,apertura,maximo,minimo,cierre,volumen` o como mínimo `fecha,cierre` (alias admitidos: `date`, `close`, `adj close`, `valor`). Fechas `AAAA-MM-DD`, sin duplicados. Columna opcional `fecha_publicacion`: la fila solo es visible cuando `fecha_publicacion <= as_of` (series macro con retraso o revisiones). Series adicionales (tipos, curvas, inventarios) con el mismo formato y símbolos propios. Use precios ajustados por dividendos si quiere rentabilidad total.

**Guardia de fuga**: con una fecha as_of activa, `serie()` nunca devuelve observaciones posteriores y pedir datos más allá lanza `FugaDeInformacion`. El Motor rechaza (`FUGA_DE_INFORMACION`) cualquier dato posterior a su `fecha_corte`; el almacén filtra F1–F6 por la fecha en que cada entrada se conoció.

Otros proveedores: `ProveedorSintetico` (pruebas; `bloque-a generar-sinteticos`) y `ProveedorYahoo` (opcional, `yfinance`, **solo modo vivo**).

**Universo** (`--universo`, por defecto `config/universo_ejemplo.csv`, **solo un ejemplo**): cada fila es un **ámbito** de un tipo de activo y su `simbolo` es la serie HT-01 de su **indicador de seguimiento** (no un activo propuesto). Columnas obligatorias `simbolo,clase,nombre,tipo_opcion,region,sector,divisa,notas` y opcionales `subtipo,ambito_incluye,ambito_excluye,indicador,subyacente`; `clase` ∈ los doce códigos; `tipo_opcion` ∈ MERCADO, SECTOR, SUBSECTOR, TEMATICA, SEGMENTO, FACTOR, ESTILO, ESTRATEGIA (compatibilidad V4.x: INSTRUMENTO_GENERICO se lee como SEGMENTO e INDUSTRIA como SUBSECTOR; cualquier otro valor es un error); `region` ∈ NAM, LAT, EUR, AFR, ORM, CHN, ASE, JPN, OCE, GLB. Cada Analista recibe el universo de su tipo y toda finalista debe llevar `indicador_seguimiento.simbolo` del universo; las que no, se descartan (PS3). Las `notas` son contenido externo: se sanean (R9).

El universo de ejemplo (57 ámbitos) incluye proxies de seguimiento para los tipos nuevos: **IDX** índices amplios (ACWI, S&P 500, Europa, Japón, emergentes, `^NSEI`); **FON** categorías de vehículos (fondos cerrados con descuento `CEFS`, multiestrategia `QAI`, futuros gestionados `DBMF`, arbitraje de fusiones `MNA`); **DER** índices de estrategias de opciones (`^BXM`, `^PUT`) y protección de cola (`TAIL`), con subyacente `SPY`; **MON** €STR (`XEON.DE`) y letras (`BIL`, `SHV`); **TCV** volatilidad (`^VIX`, `^MOVE`), nivel de tipos (`^TNX`), inflación implícita (`T10YIE`, FRED), diferencial de crédito (`BAMLH0A0HYM2`, FRED) y curva (`CURVA-USD-2S10S-TR`, serie propia). Las series FRED y las propias no las sirve `ProveedorYahoo`: cárguelas en CSV. **Series que pueden ser cero o negativas** (pendientes, diferenciales entre vencimientos) deben entregarse como índice de rentabilidad de una posición en base 100, porque el Motor trabaja con variaciones relativas. Los mercados completos pasan de RV a IDX; QAI y DBMF, de ALT a FON; IGF, de INM a RV (reglas de asignación de 2.6).

`ejemplos/datos_sinteticos/` contiene 57 series sintéticas (2022-01-03 a 2026-10-30, días hábiles) del universo de ejemplo. Son ficticias.

## 5. Uso

```bash
# Ciclo periódico C1 (vivo o con --as-of para simular una fecha)
bloque-a --datos DATOS --estado ./estado --salida ./entregables --as-of 2026-06-05 ciclo
# Petición ad hoc CT-01 (ejemplo en ejemplos/peticiones/peticion_ad_hoc.json)
bloque-a --datos DATOS --estado ./estado peticion --json ejemplos/peticiones/peticion_ad_hoc.json
# Consulta CT-03 (N0 desde la memoria o escalado a C2)
bloque-a --datos DATOS --estado ./estado consulta "¿Por qué no aparece la renta fija esta semana?"
# Decisiones y configuración CT-04
bloque-a --datos DATOS --estado ./estado decision --json ejemplos/peticiones/decision_ejemplo.json
bloque-a --datos DATOS --estado ./estado evaluar          # C5: resolver pronósticos vencidos, métricas, lecciones
bloque-a --datos DATOS --estado ./estado estado           # colas, consumo, últimos runs, integridad
bloque-a --salida ./informes_enlaces verificar-enlaces    # HT-02 sobre F7, F8, F9 y FM (sin --aplicar no modifica)
# V5.1 · Seguimiento encargado de opción (CT-24, ciclo C6, F11)
bloque-a --datos DATOS --estado ./estado seguimiento alta --json '{"opp_id":"OPP-2026-0002","frecuencia":"SEMANAL","motivo":"…","senales_interes":["…"],"fecha_fin":null}'
bloque-a --datos DATOS --estado ./estado seguimiento modificar|pausar|reanudar|cancelar --seg SEG-2026-0001 [--json '{"frecuencia":"MENSUAL"}']
bloque-a --datos DATOS --estado ./estado --as-of 2026-06-12 seguimiento ejecutar [--seg SEG-… --forzar]   # ciclos C6 vencidos → informe de seguimiento
bloque-a --datos DATOS --estado ./estado seguimiento responder --seg SEG-2026-0001 --decision RECHAZADA   # CT-22 DECISION_SEGUIMIENTO
bloque-a --datos DATOS --estado ./estado seguimiento listar
# V5.1 · Consultas del bloque al Broker (CT-23)
bloque-a --datos DATOS --estado ./estado consulta-broker enviar --json '{"tipo":"ACLARACION_ALCANCE","modo":"BLOQUEANTE","clases":["CRI"],"preguntas":[{"texto":"…","supuesto_declarado":"…","efecto_si_falso":"…"}]}'
bloque-a --datos DATOS --estado ./estado consulta-broker responder --cns CNS-2026-0001 --json '{"respuestas":[{"indice":0,"texto":"…"}]}'
bloque-a --datos DATOS --estado ./estado consulta-broker entrante|vencer|listar
# V5.1 · Credenciales (CT-25, bóveda simulada de HT-01: el valor nunca entra en mensajes, F1–F11 ni salidas)
bloque-a --datos DATOS --estado ./estado credencial solicitar --servicio "API de fondos cerrados" --solicitante AG-16
CLAVE=… bloque-a --datos DATOS --estado ./estado credencial depositar --crd CRD-2026-0001 --valor-desde-entorno CLAVE   # el Broker, fuera de banda
bloque-a --datos DATOS --estado ./estado credencial responder --crd CRD-2026-0002 --respuesta DENEGADA
bloque-a --datos DATOS --estado ./estado credencial estado|recordatorios
# Backtest
bloque-a --datos DATOS --universo MI_UNIVERSO.csv --salida ./bt --cliente anthropic \
         backtest --desde 2026-07-03 --hasta 2026-12-25 --frecuencia semanal [--clases RV,RF] [--anonimizar]
```

Opciones globales: `--config`, `--cliente mock|anthropic|replay`, `--replay`, `--replay-modo`, `--proveedor csv|yahoo`, `--anonimizar` (antes del subcomando).

## 6. Qué hace un ciclo

F0: el Evaluador resuelve lo vencido (C5) y el Coordinador carga la memoria; **GC0 determinista** por clase (movimiento semanal de la referencia > 1,5 σ, invalidación cumplida o a < 10 %, eventos de calendario, lecciones nuevas, candidata exploratoria del ciclo anterior). Sin cambio material → **N1 «arrastre verificado»**: el Analista solo revisa las vigentes y la rotación exploratoria (modo ligero); las vigentes se reconfirman con HT-03, datos frescos (PS2) y sus pronósticos abiertos. Con cambio → N2. F1–F2: el Motor calcula las señales de todo el universo (momentum, volatilidad, tendencia, riesgo, posición histórica) y los doce Analistas trabajan en paralelo (sus prompts se cargan antes en el hilo principal); GC2 (E ≥ 50) y GC3 (5 mejores por RK). F3–F4: Prospectiva y Contrarias por lotes de clase; el Analista responde a las objeciones fuertes y moderadas. F5: puertas G1–G4 y PS1–PS8 deterministas (PS3 = invertibilidad del ámbito con indicador medible), HT-03 (top-3 por tipo con continuidad, diversidad y menos de tres; A = asimetría 30, valoración 25, catalizadores 15, momento 15, invertibilidad 15), **sin duplicados entre tipos** (regla 5 de 2.6: se conserva la de mayor RK y el otro tipo vuelve a seleccionar), clústeres ML-CLUS-001 y apuestas independientes, integración del Analizador. F6: HT-09 (si no es APTO, dictamen del Orquestador; los bloqueos retiran las opciones afectadas y se revalida). F7: Redactor, tres entregables, HT-07 (≥ 70) y segunda pasada de HT-09 con coherencia entre entregables y validación con el esquema JSON vigente. F8: congelación de PRG- en F4 (también de las finalistas no publicadas, `en_informe = false`), F1, F3, F5 y CT-02. F9: auditoría asíncrona (no bloquea).

Presupuestos: antes de cada llamada se estima su coste en UC; si no cabe, se pide ampliación (registro AUT- en HA) y, si se deniega, la fase se cierra con alcance reducido declarado (PARCIAL). La validación nunca se recorta (R16).

## 7. Qué exporta el backtest

Carpeta `--salida`:

- `senales.csv` — una fila por opción publicada y fecha:

| Columna | Contenido |
|---|---|
| `fecha_asof` | Fecha del ciclo (AAAA-MM-DD); la señal solo usa información hasta esa fecha |
| `run_id`, `clase`, `tipo_activo`, `subtipo`, `rango` | RUN-, tipo de activo (`clase` y `tipo_activo` coinciden: doce códigos), subtipo, posición 1–3 en el top-3 |
| `opp_id`, `tipo_opcion`, `nombre`, `ambito` | Oportunidad (estable entre ciclos mientras siga vigente) y su ámbito (`incluye · región`) |
| `indicador_seguimiento_simbolo` | Símbolo HT-01 del indicador de seguimiento del ámbito (sustituye a `proxy_backtest` de V1.0) |
| `direccion` | `LARGO` (alcista o relativa favorable) · `CORTO` (bajista o relativa desfavorable) |
| `horizontes`, `horizonte_principal` | p. ej. `H2\|H3` y `H3` |
| `banda`, `prob_interna` | Banda publicable y probabilidad interna registrada en F4 (sin certificado, la probabilidad no se publica) |
| `RK`, `A`, `E`, `T` | Puntuaciones HT-03 (`T` puede ser `NA`) |
| `riesgo_1a5` | RISK-DD-001 |
| `relevancia_decisional`, `siguiente_paso` | Anexo A y regla del ejecutor (sección 10) |
| `vigente_nueva` | `VIGENTE` (continuidad) o `NUEVA` |
| `proxy_backtest` | **Obsoleto**: alias de `indicador_seguimiento_simbolo` (mismo valor), al final de la fila para no romper lectores V1.0 por nombre de columna; se retirará en V1.2 |

- `pronosticos.csv` — todos los PRG- de F4: `prg_id, opp_id, run_id, fecha_emision, clase, simbolo, horizonte, fecha_resolucion, tipo_pronostico (RELATIVO|DIRECCIONAL), direccion, referencia, umbral, banda_verbal, prob_interna, prob_publicada, prob_referencia_ingenua, nivel_referencia, nivel_referencia_indice, en_informe, estado (ABIERTO|RESUELTO|NO_RESOLUBLE), fecha_resuelto, rent_proxy, rent_referencia, valor_observado, resultado_binario, brier, log_score, brier_ref, comprobacion_fuga, version_de`. Un pronóstico RELATIVO acierta si `rent_proxy − rent_referencia` tiene el signo pronosticado entre el cierre ≤ `fecha_emision` y el cierre ≤ `fecha_resolucion`; uno DIRECCIONAL, si lo tiene `rent_proxy`. `prob_referencia_ingenua` es la tasa base sin fuga (ventanas no solapadas de 3 años hasta la emisión).
- `metricas.json` — por `clase|horizonte`: n, acierto con IC de Wilson y prueba binomial frente a la tasa base, Brier y Brier de la referencia, log-score, BSS con IC 90 % (bootstrap de bloques), ECE con su nulo (media y q90), Diebold-Mariano con corrección HLN, calibración global, rentabilidad relativa media del top-3 frente a la referencia de la clase; métricas solo de opciones publicadas; certificados emitidos y celdas con muestra insuficiente; consumo total; advertencias.
- `consumo.csv` — por RUN: llamadas, tokens de entrada, salida, escritura y lectura de caché, búsquedas web, UC (LLM y Motor) y coste estimado (vacío sin precios).
- `entregables/AAAA-MM-DD/` — informe técnico (`.md`), informe visual (`.html`, semáforo de doce tipos, «Qué abarca» en cada tarjeta y la frase fija sobre el Bloque B) y paquete JSON (esquema vigente: ámbito, indicador, invertibilidad y `paquete_para_bloque_B` con criterios de selección sugeridos, métricas clave y preguntas) de cada fecha.
- `estado/` — F1–F6, F10, RC, HA en JSONL append-only con cadena de hash (auditables).

**Conexión con su backtester**: lea `senales.csv`, agrupe por `fecha_asof` y construya las carteras (p. ej., `LARGO` en el indicador `indicador_seguimiento_simbolo` o en los activos que elija el Bloque B, peso por `rango` o `RK`, mantenimiento hasta la siguiente fecha o hasta el `horizonte_principal`), ejecutando al cierre siguiente a `fecha_asof` para no usar el propio cierre de la señal. `pronosticos.csv` permite evaluar la capacidad predictiva independientemente de la cartera. Por defecto, tras el último ciclo se resuelven los pronósticos con los datos disponibles posteriores (`--sin-resolucion-final` para desactivarlo).

## 8. Coste orientativo (medido en simulación)

UC por llamada = 0,5·(entrada equivalente / 8 000) + 0,5·(salida / 1 500), con entrada equivalente = entrada no cacheada + escritura de caché + 0,1·lectura de caché (decisión del ejecutor: 1 UC ≈ 8 000 tokens de entrada y 1 500 de salida, Anexo A).

Medición con `MockClient` (tokens estimados a 3,6 caracteres por token; los prompts sí son los reales) sobre el universo de ejemplo (57 ámbitos, 12 tipos; `ejemplos/salida_backtest_simulado/consumo.csv`):

| Ciclo | Llamadas | Entrada no cacheada | Escritura caché | Lectura caché | Salida | UC |
|---|---|---|---|---|---|---|
| Semanal completo, 12 tipos en N2 (primer ciclo) | 50 | ≈ 104 000 | ≈ 309 000 | ≈ 534 000 | ≈ 41 000 | ≈ 44 |
| Semanal posterior, mayoría en arrastre verificado (N1) | 14 | ≈ 49 000 | 0 (caché caliente) | ≈ 263 000 | ≈ 4 000 | ≈ 7,4 |

Ambos quedan muy por debajo del tope de 240 UC del Anexo A.

Las salidas reales del modelo serán más largas que las simuladas; tómelo como cota inferior de tokens. Para pasar a euros, rellene `precios_por_millon`. La caché de prompts tiene una vida de 1 h: en un backtest con modelo real los ciclos encadenados la reaprovechan. La primera consulta N0 de una sesión paga la escritura de la caché del prompt del Coordinador (≈ 1,5 UC); las siguientes, < 1 UC.

## 9. Limitaciones y advertencias

1. **Fuga por conocimiento del modelo.** El modelo conoce hechos posteriores a cualquier fecha anterior a su fecha de corte; en backtest se le pide que trabaje como si fuera la fecha as_of, pero no puede «olvidar». Backtestee **periodos posteriores** a `backtest.fecha_corte_modelo` (valor orientativo en el YAML: compruébelo en la documentación de Anthropic); si el periodo es anterior, `metricas.json` lo advierte. `--anonimizar` sustituye símbolos y nombres por alias neutros («RV03», «Activo RV03») y rebasa los precios a 100 en lo que ven los agentes; es una mitigación **parcial**: clase, región, sector y fechas siguen visibles, la forma de la serie puede delatar episodios conocidos y el modelo puede usar su conocimiento general del periodo.
2. **Búsqueda web desactivada en backtest**; los agentes trabajan con los datos HT-01 hasta as_of y las referencias de F7–F9 con año ≤ año as_of (las fuentes de F9 sin año se ofrecen solo como catálogo). La evidencia es, por tanto, sobre todo de mercado.
3. **Fichas del Motor no implementadas** en V1.0–V1.1 → `RECHAZADO METODO_NO_IMPLEMENTADO` con alternativa del núcleo: todas salvo las 14 marcadas en el Catálogo como «IMPLEMENTADO (ejecutor V1.0, pruebas unitarias)». ACC-ERP-001 y REI-CAP-001 tienen solo la versión simple (diferencial y percentil, sin Damodaran ni cap de equilibrio) y FX-MOM-001 está implementada sin prueba dedicada: siguen como «Documentado» en el Catálogo. VOL-GARCH-001 requiere `arch`. El agente LLM del Motor (AG-13) no se invoca en el ciclo estándar.
4. **Cliente simulado**: con `MockClient` las «opiniones» son reglas sintéticas; los resultados del backtest simulado no dicen nada de la capacidad del bloque.
5. Calendario de lunes a viernes sin festivos; criptoactivos también en días hábiles en los datos sintéticos.
6. Puntos simplificados respecto del diseño completo: el Curador LLM clasifica pero la deduplicación y las raíces son deterministas (las raíces HT-01 cuentan como primarias de nivel A); las peticiones CT-07/CT-08 se limitan a una por clase y ciclo; las colas son síncronas (HT-08 registra órdenes de instancias, el paralelismo real es el de los hilos de Analistas); no se mide la fiabilidad de fuentes de opinión (FUE-); el planificador HT-05 calcula fechas pero no programa tareas en el sistema operativo (use cron/systemd con `bloque-a ciclo`).
7. El informe visual se genera a partir de la cabecera, los estilos y los iconos de la plantilla vigente (doce tipos) con texto llano; si el índice Fernández-Huerta queda por debajo de 70, se pide una reescritura y, si persiste, la entrega se bloquea (C12).

## 9 bis. Novedades V5.1 (ejecutor V1.2)

- **H5 y horizonte principal.** La tabla 8.3 incluye H5 (décadas). En los tipos con H5 «Sí» (RV, MP, IDX, ALT) el mock ofrece H5 como horizonte secundario. El PRG H5 se congela **sin probabilidad interna** (solo banda) y con **3 hitos HIT-** (a 12, 30 y 54 meses; `h5.meses_hitos`), cada uno un PRG ordinario de horizonte H4 que el Evaluador resuelve en su fecha; `Evaluador.estado_h5` deriva `EN_CURSO_CONFORME`, `DESVIADO` o `INVALIDADO` y la tasa de hitos cumplidos por tipo. Cada opción lleva `naturaleza_inversion` (la del Analista si es válida; si no, por defecto por tipo: MON `LIQUIDEZ`, DER `PRIMA_RIESGO`, ALT `ESTRUCTURAL`, resto `CICLICA`) y un `horizonte_principal`: el que declara el Analista (con su `justificacion_horizonte`) si está entre los ofrecidos; si no lo declara, el ejecutor propone uno coherente con la naturaleza (y solo si la naturaleza tampoco la declaró el Analista la ajusta al horizonte). HT-09 lo valida (C17, C18) y bloquea lo incoherente sin justificar (T-53, CS-01). Los hitos H5 se excluyen de las métricas, los certificados y el historial de aciertos: se evalúan aparte en `estado_h5` (T-53, CA-08).
- **Consultas al Broker (CT-23).** `consulta-broker` registra las CNS- en F5 (máx. 3 por RUN-, agrupación automática), vigila plazos y detecta consultas recurrentes (CT-22 `CONSULTA_RECURRENTE`). En el F0 de cada ciclo, las vencidas pasan a `VENCIDA` y una `BLOQUEANTE` sin respuesta **pausa** los tipos de activo afectados (limitación declarada); los supuestos de las pendientes o vencidas viajan en `supuestos_declarados` del paquete y del informe técnico.
- **Credenciales (CT-25).** `credencial` registra las CRD- en F5 sin valores; la bóveda simulada (`<estado>/boveda/`, `secretos.json` con permisos 0600) solo devuelve alias y estado; una respuesta del Broker que traiga el valor se rechaza íntegra y se pide su depósito y renovación; las denegadas quedan como limitación de servicio en F10.
- **Seguimiento encargado (CT-24, C6, F11).** `seguimiento` gestiona los encargos en F11 (propietario AG-01) y ejecuta los ciclos vencidos: revisión ligera **determinista** (delta del indicador frente a 1,5 σ semanales, distancia a la invalidación, catalizadores, T/E/A/RK reconstruidos con HT-03 y umbrales de F10, pronósticos e hitos abiertos), una recomendación, informe breve (.md) y JSON en `Informes de seguimiento/`, validados con HT-09 (`validar_seguimiento`) y, en ejecución, con el esquema JSON V5.1; un informe bloqueado va a `_bloqueados/<RUN>/` y no a la carpeta de entrega (T-53, CA-03); RUN- de tipo `SEGUIMIENTO` en F5 (`tipo_entrada: RUN_C6`, para no mezclarse con los RUN de C1–C3). Estado de madurez: implementado sin llamada al Analista de tipo de activo (el CT-06 de fase SEGUIMIENTO queda registrado).

## 10. Decisiones de diseño relevantes

- El paquete de síntesis que valida HT-09 incluye `puertas`, `cluster`, `vigente`, la advertencia de H1 y `objeciones[].resuelta`; el entregable JSON los elimina para cumplir el esquema (que no los admite) y añade `x_referencia`, `x_lectura_conjunto`. El símbolo con el que se mide la opción va en `indicador_seguimiento.simbolo` (V1.0: `x_proxy_backtest`). En F3 el campo interno es `simbolo_seguimiento`; los registros V1.0 con `proxy_backtest` se siguen leyendo.
- **Carga de prompts robusta**: cada agente se busca en `02_System_prompts` por el nombre de su agente con cualquier sufijo de versión («… - Versión óptima V5.0.md», «… V5.0.md»…), tomando la versión más alta, tolerando NFC/NFD y aceptando el nombre anterior de AG-04, AG-07 y AG-09 mientras dure el renombrado. Lo mismo para la plantilla del informe visual y el esquema JSON en `06_Plantillas_entregables`. Si falta el prompt de un Analista de tipo de activo, se usa el marco común con una incidencia (modo degradado declarado); para el resto de agentes, error.
- **Regla anti-fuga** sin cambios: guardia de fecha as_of en HT-01 y en el Motor, búsqueda web desactivada en backtest, referencias de F7–F9 con año ≤ as_of y anonimización opcional (que ahora también cubre `indicador_seguimiento.simbolo`). La advertencia «legibilidad no comprobada» de la primera pasada de HT-09 se ignora porque el informe visual aún no existe; se comprueba en la segunda.
- Puertas, relevancia decisional, riesgo 1–5, horizontes aplicables (tabla 8.3 + F10) y confianza (E ≥ 70 → probable; si no, especulativo) son deterministas. La dimensión «objeciones respondidas» de E se fija con la fracción de objeciones fuertes y moderadas respondidas; sin PS1 la «calidad de raíces» se limita a 50. `siguiente_paso_sugerido`: PROFUNDIZAR_EN_A si relevancia ALTA y E < 70; ENVIAR_A_BLOQUE_B si RK ≥ 65; VIGILAR en otro caso.
- Un OPP- conserva su identificador mientras siga activo (mismo tipo de activo, indicador de seguimiento y tipo de opción); no se emite un PRG- nuevo para un horizonte que ya tiene uno abierto (evita solapamientos); los vencidos de una opción vigente se reemiten como versión nueva (`version_de`).
- Prospectiva, Contrarias y Curador reciben los encargos de cada clase por lotes (un mensaje con lista `encargos`/`peticiones`/`piezas`) para ahorrar llamadas; cada elemento lleva los campos del Anexo B.
- La recalibración (pesos de RK) se calcula y se registra en F6 en **modo sombra** (`aplicar_recalibracion: false`): cada ciclo compara el top-3 con los pesos propuestos sin cambiar la producción; fuera de bandas genera una propuesta P3-EVAL-.
- HT-02, HT-03, HT-07 y HT-09 son copias literales de `10_Herramientas` (`bloque_a/herramientas/referencia/`); una prueba comprueba que no divergen.

## 11. Estructura

```
11_Ejecutor/
  pyproject.toml · requirements.txt · README.md
  config/por_defecto.yaml · config/universo_ejemplo.csv
  bloque_a/
    llm.py (Anthropic, Mock, Replay) · mock_respuestas.py · prompts.py · contratos.py · agentes.py · consumo.py
    almacen.py · orquestacion.py · sintesis.py · redaccion.py · evaluador.py · backtest.py · cli.py
    referencias.py · anonimizacion.py · configuracion.py · interfaz_broker.py (CT-23, CT-25) · seguimiento.py (CT-24, C6, F11)
    motor/ (operaciones.py, evaluacion.py, servicio.py)
    herramientas/ (ht01_datos, ht01_boveda, ht02, ht03, ht04_graficos, ht05_planificador, ht06_indice, ht07, ht08_monitor, ht09, referencia/)
  tests/ (pytest: test_unitarias, test_integracion, test_autocritica, test_v5, test_v51; MAPA_PLAN_DE_PRUEBAS.md; RESULTADOS.txt)
  ejemplos/datos_sinteticos/ · ejemplos/peticiones/
```

## Correcciones de la revisión T-53 (9-11-2026)

Revisión independiente del ejecutor con 59 pruebas nuevas (de 58 a 117, con las de las dos rondas de QA). Detalle en `.docs/tickets/T-53/analisis-tecnico.md` (desde la raíz del repositorio). Lo que cambia para quien lo usa:

- **Entregables.** Se generan en `_borradores/` y se validan. Solo lo que no queda BLOQUEADO llega a las carpetas de entrega; lo bloqueado se guarda en `_bloqueados/<RUN>/`, sin `estado_g3`.
- **Datos.**
  - Un cierre no numérico rechaza la serie (`DatosInvalidos`) en lugar de convertirse en un resultado.
  - Un símbolo sin datos hasta la fecha *as_of* se excluye del ciclo y se declara como laguna; el tipo queda PARCIAL.
  - En H1, la antigüedad del dato (PS2) se cuenta en sesiones hábiles (`ps2_antiguedad_maxima_dias`).
- **Selección y presentación.**
  - Una vigente que pierde la protección de continuidad sigue compitiendo por los puestos libres.
  - La pieza automática de momentum ya no basta para PS1.
  - El semáforo y el `siguiente_paso_sugerido` siguen al prompt del Analizador (`seleccion.semaforo`, `seleccion.siguiente_paso`).
- **Evaluación.**
  - Holm escalonado (`evaluacion.alfa_holm`).
  - Cinco bandas verbales (`bandas_verbales`).
  - Los hitos H5 quedan fuera de las métricas.
  - La degradación de H5 se registra en F6 y F10.
  - Un certificado con ECE 0 ya no se revoca (`evaluacion.ece_revocacion`).
- **Almacén y bóveda.**
  - F4 rechaza una segunda alta o una segunda resolución (`PronosticoCongelado`).
  - La bóveda valida la caducidad en ISO antes de escribir, no devuelve credenciales caducadas y crea el archivo de secretos con permisos 0600.
- **Consultas al Broker.** Una consulta BLOQUEANTE sin tipos pausa todo el alcance; si queda pausado todo, el run es PARCIAL y no analiza nada.


## Propuestas de la revisión aplicadas (T-66, 10-11-2026)

De las 21 propuestas de T-53 (`.docs/tickets/T-53/propuestas.md`), se aplican las que no necesitan otro proveedor de IA, K ni llamadas reales a la API. A pasa de 117 a 181 pruebas. Detalle en `.docs/tickets/T-66/`. Lo que cambia para quien lo usa:

- **Perfiles activos (PA-01).**
  - Por defecto solo se analiza **divisas** (`perfiles.activos: [DIV]`, `[PROPUESTO]`).
  - Un tipo no activo que se pide responde NO_ESTIMABLE y se declara.
  - Para activar más tipos, se añaden a `perfiles.activos` o se cambia `clases_activas` por CT-04.
  - Si no queda nada que analizar, el run se cierra PARCIAL con `entrega: SIN_RESULTADO`, sin redactar.
- **Contradictor (PA-05, sin otro proveedor).**
  - AG-11 recibe la afirmación verificable y la evidencia, sin la tesis, el mecanismo, el pre-mortem ni las dimensiones del Analista.
  - Una objeción fuerte solo queda resuelta si el Analista cita evidencia verificable (`evidencia_citada`) **y** AG-11 lo confirma en una contrarréplica.
  - El veredicto lo calcula una regla (`contrarias.moderadas_para_fragil`). Una tesis refutada no es elegible y una frágil sale con confianza «especulativo» (INC-T66-01 y INC-T66-02).
- **Contaminación por memoria del modelo (PA-09).**
  - `backtest.anonimizar: auto` anonimiza con un modelo real; con el simulado no hace falta.
  - Los pronósticos de backtest hechos con un modelo real antes de `backtest.fecha_corte_modelo` llevan `contaminacion_posible`. No cuentan para certificados, recalibración, lecciones, degradación de H5 ni historial.
  - El informe de backtest los muestra aparte, solo como descripción.
  - Una grabación de `ReplayClient` hecha antes de T-66 (un backtest sin anonimizar) ya no se reproduce con `auto`, porque cambia la clave de la respuesta (`ReplayFaltante`). Para reproducirla, usa `backtest.anonimizar: false`.
- **Aprendizaje que solo endurece (PA-10).** Con `aprendizaje.solo_endurecer: true` (`[PROPUESTO]`):
  - un certificado que pasa el criterio nace **PROPUESTO**: el operador lo aprueba por CT-04 (`{"aprobar_certificados": [ids]}`);
  - la recalibración de pesos nunca pasa sola a producción;
  - revocar certificados y degradar H5 siguen siendo automáticos.
- **Muestra efectiva (PA-03, en parte).**
  - Los certificados exigen `n_eff ≥ min_certificar`. `n_eff` sale del efecto de diseño por conglomerados de fecha.
  - El intervalo del BSS es un bootstrap por fechas, con al menos `evaluacion.min_conglomerados_bootstrap` fechas.
- **Ablación (PA-14).** Cada run guarda en F5 (`ablacion`) dos comparaciones, sin coste en tokens:
  - el top-3 que saldría sin las objeciones del Contradictor;
  - cuántas opciones coinciden con una referencia simple, el top-3 por señal compuesta.
- **Probabilidad del Analista (PA-21).**
  - El Analista puede dar `probabilidades_propias` por horizonte, que se guardan en F4 como `prob_analista`.
  - Las métricas comparan su Brier con el de Prospectiva. No decide nada.
