# T-112 · Grupo P · inmobiliario, materias primas, cripto y alternativos

| Campo | Valor |
| --- | --- |
| Módulo | `bloque_a/11_Ejecutor/bloque_a/motor/fichas_reales.py` |
| Pruebas | `bloque_a/11_Ejecutor/tests/test_fase2_reales.py`: **585 pruebas, todas en verde** (≈ 21 s; 505 en r01, §Ronda r02) |
| Mutantes | `.docs/tickets/T-112/revisores/impl_P_mutantes.py` (resultado en §Mutantes) |
| Fichas | REI-CAP-001, REI-FFO-001, REI-NAV-001, CMD-INV-001, CMD-RETDEC-001, CHR-FLOW-001, CHR-FUND-001, ALT-DESMOOTH-001 |
| Fuente | Catálogo V5.0: §2, §3, §11–§14 (cada ficha por su identificador) y §20. Nada de `99_Historico*` |
| Dependencias | numpy, scipy y pandas |
| ruff · mypy | ninguna incidencia en el módulo ni en las pruebas (los 9 errores de mypy que salen al importar son de `configuracion.py`, `evaluacion.py`, `operaciones.py` y `servicio.py`, previos) |

El módulo exporta `PARAMETROS_POR_DEFECTO`, `UMBRALES`, `ADVERTENCIAS`, `FICHAS` y `CASOS_CONTROL` en el formato de
`fichas_mon_idx.py`. Para integrarlo en `servicio.py` basta con añadir `fichas_reales` al bucle de módulos. Al hacerlo,
la entrada REI-CAP-001 de `IMPLEMENTADAS` se sustituye y la ficha sale de `DOCUMENTADAS_CON_CODIGO`.

## Convenciones comunes

- **Entradas.** Todas llegan en línea en `ent["valores"]`, en bloques con `fecha` ISO. ALT-DESMOOTH-001 acepta también
  niveles de índice en `series_rol["indice_suavizado"]` y `series_rol["mercado"]`.
- **Unidades.** Tipos, rentabilidades, cap rates y primas entran en tanto por uno. Las salidas llevan la unidad de la
  ficha en el sufijo: `_pct` en %, `_pb` en pb. Los días se cuentan Real/365 (§3.1).
- **Posición histórica.** Percentil = proporción de la historia ≤ valor, como `operaciones.posicion_historica`. El z se
  calcula con desviación n − 1 (ST-DESC-001). Con dispersión nula, z = `None` y se declara una limitación.
- **Fallo cerrado.** La envoltura `_cerrado` sigue el patrón de MON/IDX:
  - una entrada mal formada o fuera de dominio da `ErrorFicha`;
  - un resultado nunca lleva NaN ni inf;
  - un bloque opcional sin datos se entrega como `None` y se declara en las limitaciones.
- **Umbrales y parámetros.** Una petición que traiga una clave de `UMBRALES` se rechaza («umbral fijo de la ficha»).
  Cada parámetro tiene tipo y rango (`_validar_parametros`), con cota superior en los tamaños. Una clave que la ficha no
  declara se rechaza, salvo `clase`, que añade el servicio (ronda r02, H-02).
- **Fecha de corte.** Con `ent["fecha_corte"]`, un dato en línea fechado después se rechaza (ronda r02, H-07).
- **Advertencias.** Las «Supuestos y limitaciones» de cada ficha van en `resultado["advertencias"]`, no en las
  limitaciones.
- **Determinismo.** Ninguna ficha usa azar: las ocho declaran semilla `null`. El arranque del estimador GLM es fijo.

## Por ficha

### REI-CAP-001 · Cap rate y diferencial cap rate–bono — supera sus 3 casos

**Código heredado: lo rehice.** El de `servicio.py` (`f_cap`, sobre `operaciones.diferencial_rentabilidades`) no
cumplía la ficha:
- no calculaba el cap rate (NOI/valor): lo recibía ya hecho;
- no tenía cap rate de mercado implícito ni cap de equilibrio r − g_NOI;
- no exigía 15 años de historia: con 5 observaciones bastaba;
- no aplicaba la ventana de 20 años;
- no tenía la aclaración por base del NOI ambigua;
- con historia constante daba z = 0,0 en vez de un z indefinido.

El nuevo, `f_rei_cap`, sustituye a ese manejador.

- **Datos** (`valores`):
  - `moneda`;
  - `noi` = {`valor`, `base` (adelantado | historico), `definicion` (antes_capex | despues_capex)};
  - `valor_tasacion`;
  - opcional `valor_mercado_implicito` = {`capitalizacion`, `deuda_neta`};
  - `soberano_10a` = {`rendimiento`, `moneda`};
  - `historia` = [{`fecha`, `cap_rate`, `soberano_10a`}], de 15 años o más;
  - opcional `equilibrio` = {`r`, `g_noi`}.
- **Salidas:**
  - cap rates de tasación y de mercado (%);
  - diferencial frente al soberano (pb);
  - percentil, z y media histórica del diferencial (RI-MH);
  - cap de equilibrio (%) y brecha (pb);
  - `verificacion` de la coherencia NOI/valor.
- **Rechazos:**
  - base del NOI ausente o ambigua (aclaración);
  - base del NOI distinta de `base_noi`;
  - definición del NOI sin declarar;
  - historia < 15 años;
  - soberano de otra moneda;
  - r ≤ g;
  - valor implícito no positivo.
- **Decisiones:**
  - `[PROPUESTO]` valor de mercado implícito del agregado = capitalización + deuda neta;
  - `[PROPUESTO]` el NOI aportado debe declarar la misma base que pide `base_noi`; si no, se pide aclaración;
  - `[PROPUESTO]` `ventana` en años enteros, de 15 o más (el mínimo de «Entradas mínimas»). La ventana toma las
    observaciones con fecha posterior a la última fecha menos la ventana.
- **Casos de control:**
  - cap × valor = NOI, en tasación y en mercado, con valores a mano;
  - diferencial y su posición en una ventana de 15 años que deja fuera parte de la historia;
  - cap de equilibrio r − g_NOI y brecha.

### REI-NAV-001 · Prima/descuento sobre NAV — supera sus 3 casos

- **Datos:**
  - `componentes` = [{`id`, `fecha_precio`, `precio`, `acciones`, `nav_por_accion`, `fecha_nav`, `variante_nav`,
    `gav`, `deuda_neta`, `otros_pasivos` (opcional), `cap_rate_tasacion`}];
  - opcional `historia_prima` = [{`fecha`, `prima`}] del agregado.
- **Salidas:**
  - prima agregada ponderada por capitalización (%), dispersión (%) y rango;
  - detalle por componente;
  - NAV ajustado agregado (variación %) con `cap_objetivo`;
  - percentil, z y media histórica (RI-MH).
- **Rechazos:**
  - NAV de antigüedad > 12 meses (frente a la fecha del precio);
  - NAV posterior al precio;
  - variante distinta de `nav_variante`, o sin declarar;
  - NAV ≠ GAV − deuda neta − otros pasivos, por encima de la tolerancia 1e-10 de la ficha;
  - componentes a fechas de precio distintas;
  - identificadores repetidos.
- **Decisiones:**
  - `[PROPUESTO]` La «Aclaración y rechazo» dice «Rechazo con NAV de antigüedad > 12 meses sin advertencia». Lo leo
    como rechazo estricto, sin servirlo con advertencia. **Es ambiguo: lo propongo como incidencia** (INC-T112-01), por
    si la intención era permitirlo con advertencia;
  - `[PROPUESTO]` variantes admitidas: EPRA NTA, NRV y NDV (EPRA *Best Practices Recommendations*, referencia de la
    ficha), sin mezclar variantes;
  - `[PROPUESTO]` sin `otros_pasivos`, se derivan por diferencia (GAV − deuda − NAV) y la identidad se declara no
    verificable;
  - `[PROPUESTO]` dispersión = desviación típica ponderada por capitalización. Variación del NAV ajustado = ΣNAV_aj/ΣNAV − 1;
  - percentil solo con una historia de 10 años o más (el «Método»); con menos, `None` y limitación;
  - `cap_objetivo` en (0, 1), sin valor por defecto (la ficha dice «o null»).
- **Casos de control:**
  - NAV = activos − pasivos: con cap_objetivo igual al cap de tasación, el NAV ajustado es el publicado;
  - prima ponderada, dispersión y NAV ajustado a otro cap rate, a mano;
  - percentil frente a 12 años.

### REI-FFO-001 · FFO/AFFO y sostenibilidad del dividendo — supera sus 3 casos

- **Datos:**
  - `moneda`;
  - `componentes` = [{`id`, `precio`, `acciones`, `ejercicios`: [{`ejercicio`, `beneficio_neto`,
    `amortizaciones_inmobiliarias`, `plusvalias`, `capex_mantenimiento`, `rentas`, `ajuste_rentas_lineales`,
    `dividendo`}]}];
  - opcional `historia_multiplos` = [{`fecha`, `p_ffo`, `p_affo`}].
- **Salidas:**
  - FFO y AFFO agregados (moneda y rendimiento %);
  - P/FFO y P/AFFO agregados (Σcapitalización/ΣFFO) y sus percentiles;
  - cobertura AFFO/dividendo agregada y por componente: mediana, IQR, mínimo y máximo;
  - serie por ejercicio;
  - `verificacion` de la reconciliación.
- **Rechazos:**
  - sin `amortizaciones_inmobiliarias` desglosadas, también si solo llega el total `amortizaciones`;
  - < 3 ejercicios comunes;
  - CAPEX sin reportar y sin `capex_pct_rentas`;
  - dividendo o ajuste de rentas lineales ausentes;
  - ejercicios o componentes repetidos.
- **Decisiones:**
  - `[PROPUESTO]` la ficha no fija el % de rentas del CAPEX estimado. Lo aporta el solicitante en `capex_pct_rentas`,
    en [0, 1) y sin valor por defecto;
  - dispersión de la cobertura = IQR con cuantiles tipo 7 (ST-DESC-001);
  - percentiles de múltiplos con 5 observaciones o más (ST-DESC-001, «Entradas mínimas»);
  - `[PROPUESTO]` el agregado usa el último ejercicio común a todos los componentes, y se declara;
  - con FFO o AFFO agregado no positivo, el múltiplo es `None` y se declara.
- **Casos de control:**
  - reconciliación con el beneficio neto (FFO − amortizaciones + plusvalías = BN; AFFO + CAPEX + ajustes = FFO), con
    agregados a mano en los tres ejercicios;
  - múltiplos, rendimientos, cobertura en mediana e IQR y percentiles a mano, con tres componentes para que mediana y
    media difieran;
  - CAPEX estimado como % de rentas.

### CMD-INV-001 · Inventarios frente a media estacional — supera sus 4 casos

- **Datos:**
  - `inventarios` = {`frecuencia` (semanal | mensual), `unidad`, `observaciones`: [{`fecha`, `fecha_publicacion`,
    `valor`}]};
  - opcional `demanda_diaria` = {`valor`, `fuente`};
  - opcional `pendiente_curva` = [{`fecha`, `pendiente`}] (CMD-CURVE-001).
- **Salidas:**
  - media y desviación de la misma época de los `anos_estacional` años previos;
  - desviación (unidades y %) y z;
  - sorpresa: variación del periodo frente a la variación típica de la misma época;
  - días de cobertura;
  - serie de desviaciones y su correlación con la pendiente de la curva;
  - segunda vía FX-STL-001.
- **Rechazos y limitaciones:**
  - rechazo con < 3 años de serie («Aclaración y rechazo»);
  - entre 3 y 5 años, limitación («Entradas mínimas»); por debajo de 10, limitación («10 recomendados»);
  - rechazo sin fecha de publicación, o con una publicación anterior a su periodo;
  - rechazo con dos observaciones del mismo periodo;
  - rechazo si `excluir_anos` incluye el año actual;
  - rechazo con < 3 años previos que tengan el mismo periodo.
- **Decisiones:**
  - mínimo de 3 años previos: el mínimo del rango de `anos_estacional` (3–10) y el de rechazo;
  - `[PROPUESTO]` en datos semanales, la semana ISO 53 se compara con la 52 de los años que no la tienen;
  - `[PROPUESTO]` segunda vía FX-STL-001 por medias móviles, esquema aditivo:
    - tendencia = media móvil centrada 2×P (P = 12 o 52);
    - índice estacional = media de la serie sin tendencia de los mismos años previos, normalizado a suma 0;
    - nivel esperado = última tendencia + índice;
    - exige una serie sin huecos; si no, `None` y limitación;
  - correlación con la pendiente con 5 fechas comunes o más (ST-DESC-001).
- **Casos de control:**
  - serie periódica pura ⇒ desviación 0 y sorpresa 0, con valores distintos en cada mes para que un periodo
    equivocado no dé 0;
  - segunda vía con desviación 0 y su nivel e índice a mano;
  - método a mano con un año excluido: media, %, z, cobertura y sorpresa, con datos en los que media y mediana
    difieren;
  - segunda vía a mano, término a término, en una serie con tendencia curva, ruido y un sesgo de la 2×12 que obliga a
    normalizar el índice estacional.

### CMD-RETDEC-001 · Descomposición de la rentabilidad de futuros — supera sus 2 casos

- **Datos.** Hay dos modos, según `calendario_roll`:
  - `indice` (por defecto, «el del índice»): `indices` = {`calendario_roll` (nombre declarado), `fechas`, `exceso`,
    `total`, `spot`};
  - `declarado`: `contratos` = {`fechas`, `precios` por contrato, `calendario_roll` = [{`desde`, `contrato`}], `spot`}.
  - En los dos: `tipo_colateral` alineado con las fechas y, opcional, `indice_amplio` (RI-CM).
- **Salidas:**
  - componentes spot, roll y colateral (% anual) y total;
  - identidad suma = total;
  - total compuesto (FIN-CAGR-001);
  - colateral implícito menos tipo (pb);
  - acumulados;
  - RI-CM.
- **Rechazos:**
  - sin calendario de roll: el índice no declara el suyo, o la lista está vacía;
  - fechas que no son periodos consecutivos de la frecuencia;
  - vectores no alineados;
  - falta el precio del contrato mantenido;
  - el calendario no cubre la primera fecha;
  - contratos sin precios.
- **Decisiones:**
  - `[PROPUESTO]` anualización aritmética (media por periodo × periodos por año), para que suma de componentes =
    total sea exacta. El compuesto se da aparte;
  - colateral por periodo = tipo al inicio × días/365 (Real/365, §3.1);
  - en modo contratos, total = rentabilidad del contrato mantenido + colateral;
  - `[PROPUESTO]` frecuencias admitidas: mensual (la de la ficha), trimestral y anual.
- **Casos de control:**
  - suma = total con índices, y cada componente a mano;
  - suma = total con contratos y un calendario con dos rolls, y cada componente a mano.

### CHR-FUND-001 · Financiación de perpetuos y base — supera sus 3 casos

- **Datos:**
  - `plataformas` = {nombre: {`periodo_horas`, `historia`: [{`fecha`, `tasa`, `interes_abierto`}]}};
  - `futuro` = [{`fecha`, `precio`, `vencimiento`}];
  - `spot` = [{`fecha`, `precio`}];
  - opcional `capitalizacion` = {`fecha`, `valor`}.
- **Salidas:**
  - financiación agregada (% anual) y por plataforma, con sus pesos;
  - base anualizada (% anual);
  - percentiles en 1 año;
  - interés abierto/capitalización (%);
  - `verificacion`: base − financiación (pb, la última y la media) y su correlación.
- **Rechazos y limitaciones:**
  - rechazo con < 2 plataformas;
  - rechazo con < 90 días comunes;
  - el futuro o el spot no cotizan en la última fecha;
  - vencimiento no posterior a la fecha;
  - fechas repetidas;
  - capitalización de otra fecha;
  - entre 90 días y 1 año, los percentiles son `None` y se declara.
- **Decisiones:**
  - anualizada = tasa × (24/horas) × 365 («3 × 365 con periodos de 8 h»);
  - `[PROPUESTO]` `periodo_horas` en (0, 24];
  - `[PROPUESTO]` ponderación alternativa «igual» además de «interes_abierto»;
  - `[PROPUESTO]` `ventana_percentil` en días enteros, de 365 o más («≥ 1 año para percentiles»). La ventana es
    (T − ventana, T];
  - `[PROPUESTO]` la «coherencia base–financiación (arbitraje aproximado)» se entrega como diferencia y correlación,
    sin umbral de rechazo, porque es aproximada por naturaleza. La correlación pide 5 observaciones o más (ST-DESC-001).
- **Casos de control:**
  - base construida igual a la financiación ponderada ⇒ diferencia 0 y correlación 1, con pesos de interés abierto
    distintos para que una media sin ponderar no cuadre;
  - método a mano: periodos de 8 h y de 4 h, pesos, base, OI/capitalización;
  - percentil en 1 año.

### CHR-FLOW-001 · Flujos de ETF y oferta de stablecoins — supera sus 3 casos

- **Datos:**
  - `flujos_etf` = [{`fecha`, `fecha_publicacion`, `flujo`, `patrimonio`}] del agregado;
  - `oferta_stablecoins` = {moneda: [{`fecha`, `oferta`}]}, que se suman en las fechas comunes;
  - opcional `capitalizacion_total`.
- **Salidas:**
  - flujos acumulados a 5 y 20 días (moneda y % del patrimonio) con su z;
  - crecimiento de las stablecoins a 30 días (%);
  - razón stablecoins/capitalización (%);
  - RI (flujo nulo y RI-PA);
  - `verificacion` de los acumulados.
- **Rechazos:**
  - sin fecha de publicación de flujos, o con una publicación anterior a su fecha;
  - < 120 días de flujos o de stablecoins;
  - fechas repetidas;
  - una ventana sin patrimonio previo.
- **Decisiones:**
  - `[PROPUESTO]` las ventanas (5, 20) cuentan sesiones con flujo publicado;
  - % del patrimonio = acumulado / patrimonio previo a la ventana (flujo relativo = flujo/AUM_{t−1}, FON-FLOW-001 (ii));
  - `[PROPUESTO]` z del acumulado relativo frente a los acumulados que terminan en el último `ventana_z` (años
    enteros);
  - crecimiento a 30 días frente a la última oferta con fecha ≤ T − 30 días;
  - la razón con la capitalización exige la misma fecha; si no, `None` y limitación.
- **Casos de control:**
  - acumulados coherentes con los diarios (5, 20 y 20 − 5 = días 6 a 20);
  - % del patrimonio previo, crecimiento y razón a mano;
  - z en 1 año, que deja fuera parte de la historia.

### ALT-DESMOOTH-001 · Desuavizado de rentabilidades — supera sus 4 casos

- **Datos:**
  - `rentabilidades` = [{`fecha`, `r`}], trimestrales consecutivas, o niveles en `series_rol["indice_suavizado"]`;
  - opcional `mercado`, igual, o `series_rol["mercado"]`.
- **Salidas:**
  - serie desuavizada;
  - φ, o θ e índice de suavizado (GLM);
  - volatilidad observada y desuavizada (% anual, √4);
  - MDD de las dos series (RISK-DD-001);
  - beta de Dimson;
  - medias;
  - `verificacion`: error de resuavizado, término de borde y error de la identidad de la media.
- **Rechazos y limitaciones:**
  - rechazo con < 24 observaciones;
  - entre 24 y 39, limitación;
  - rechazo con huecos o fechas repetidas;
  - rechazo con φ estimado fuera de (−1, 1);
  - φ negativo, limitación;
  - rechazo de un `phi` con el método GLM;
  - rechazo de un θ GLM no invertible.
- **Decisiones:**
  - φ estimado = AR(1) por MCO con constante;
  - `[PROPUESTO]` φ fijado en [0, 1);
  - serie desuavizada en t = 2…n. La volatilidad y el MDD «antes y después» usan las mismas fechas;
  - `[PROPUESTO]` «Media de la serie conservada» se verifica como la identidad exacta de muestra finita:
    media(desuavizada) − media(observada) = φ/(1 − φ)·(r*_n − r*_1)/(n − 1), que tiende a 0. No se recentra la serie,
    porque falsearía la recuperación de la serie real. Para GLM, el término es Σ_j θ_j·(…), en el código;
  - `[PROPUESTO]` GLM por máxima verosimilitud gaussiana exacta del MA(k), con:
    - σ concentrada, θ_j ≥ 0 y Σθ = 1;
    - SLSQP desde θ iguales, con `ftol` = tolerancia de la ficha (1e-8);
    - si no converge, se rechaza;
  - `[PROPUESTO]` la verosimilitud del MA no distingue un θ de su versión con las raíces reflejadas. Se toma la
    representación invertible (raíces dentro del círculo unidad → 1/ρ̄, renormalizada) y se rechaza si queda en el
    borde o con coeficientes negativos;
  - `[PROPUESTO]` el filtro GLM arranca con r_t = r*_t en t ≤ k, y se declara;
  - `[PROPUESTO]` la beta de Dimson usa L = k rezagos. Si los rezagos son colineales (rango deficiente), da `None` y
    se declara.
- **Casos de control:**
  - φ = 0 ⇒ serie sin cambios;
  - Geltner con φ fijado recupera la serie real plantada y cumple la identidad de la media con un término de borde no
    nulo;
  - φ = AR(1) por MCO (ecuaciones normales);
  - GLM: θ ≥ 0, Σθ = 1, invertible, resuavizado = observada e identidad de la media.

## Qué no se debe promover

Las ocho superan sus casos de control. **Ninguna tiene un motivo para quedarse en DOCUMENTADO**, con dos avisos que
deben quedar en INC-T112-01 antes de promoverlas:

1. **REI-NAV-001.** La lectura de «Rechazo con NAV de antigüedad > 12 meses sin advertencia» es ambigua: hoy el código
   rechaza en firme. Si el operador quería «servir con advertencia», el cambio es pequeño, pero cambia la regla.
2. **ALT-DESMOOTH-001, método GLM.** Con series que no son un MA (por ejemplo, sinusoides deterministas), el estimador
   de máxima verosimilitud cae en el borde de invertibilidad (raíz en |z| ≈ 1):
   - si la raíz cae en |z| ≤ 1, se rechaza;
   - si cae justo fuera, se sirve, y el filtro es casi inestable.

   No he puesto un margen numérico, porque la ficha no lo fija. Si se quiere uno, va a INC-T112-01. La vía Geltner, que
   es la principal, no tiene este problema.

## Pruebas (505)

| Bloque | Qué comprueba |
| --- | --- |
| Registro y parámetros | Las cinco tablas cubren las ocho fichas. Metadatos, tolerancias y valores por defecto salen de la ficha |
| Casos de control (25) | Cada caso se supera. Sale serializable sin NaN, con las advertencias aparte |
| Los casos pueden fallar | Con las cifras del resultado movidas 1e-6, cada uno de los 25 casos falla (T-106, H-08) |
| Determinismo | Dos pasadas dan el mismo JSON (25 casos). Ni la entrada ni los parámetros se modifican |
| Umbrales fijos | Cada clave de `UMBRALES` en la petición se rechaza (31) |
| Dominio | 69 valores fuera de tipo o de rango se rechazan. Los extremos admitidos se sirven (10) |
| Entradas hostiles | `ent` y parámetros mal formados. NaN, inf, texto, booleanos, `None`, listas y dicts en hojas de los datos: o `ErrorFicha` o un resultado finito. Datos requeridos hostiles se rechazan. Fechas ilegibles o numéricas se rechazan. La envoltura `_cerrado` rechaza un resultado no finito y traduce excepciones |
| Rechazos por ficha | Cada regla de «Aclaración y rechazo» y de «Entradas mínimas», con su motivo |
| Oráculos independientes (≥ 1 por ficha) | REI-CAP: fracciones exactas, `percentileofscore`, `statistics`. REI-NAV: `np.average` ponderado y fracciones. REI-FFO: tabla larga de pandas con `groupby`, `statistics.median`. CMD-INV: filtros de pandas y 2×12 con `rolling` para la segunda vía. CMD-RETDEC: `pct_change` y CAGR por logaritmos. CHR-FUND: `pivot` y `np.average` por fila, `percentileofscore`. CHR-FLOW: `rolling`, `shift` y `asof`. ALT: `scipy.signal.lfilter` con el filtro inverso, `np.polyfit`, `cummax`, Dimson por ecuaciones normales con `shift`, y verosimilitud GLM por rejilla con `scipy.stats.multivariate_normal` |

## Mutantes

`.venv/bin/python -I -B .docs/tickets/T-112/revisores/impl_P_mutantes.py <scratchpad>` copia `bloque_a` (sin `.docx`)
en la carpeta indicada. Muta `fichas_reales.py` en la copia y mira dos cosas:
- si lo cazan los casos de control de la ficha (CC), que es lo que decide la promoción;
- si lo caza `tests/test_fase2_reales.py` (T).

**Resultado (código final): 65 mutantes, 0 vivos frente a CC y T.**

| Tipo | Mutantes | Los cazan los CC | Los cazan las pruebas |
| --- | --- | --- | --- |
| De fórmula (con CC de su ficha) | 50 | 48 | 50 |
| De regla (rechazos, umbrales fijos, envoltura) | 15 | — (los CC solo ven resultados servidos) | 15 |

Los CC de su ficha no cazan dos mutantes; los cazan las pruebas:
- P61, beta de Dimson sin sumar los rezagos. La «Verificación» de la ficha no habla de la beta, así que no tiene caso de
  control. La caza el oráculo `test_alt_oraculo_beta_dimson`;
- P64, percentil estricto (< en vez de ≤) en `_posicion`, común a REI-CAP, REI-NAV, REI-FFO y CHR-FLOW. El script lo
  ensaya con los CC de REI-CAP, que no tienen empates. Lo caza el caso de control de REI-FFO, cuya historia incluye un
  empate exacto.

Primera ejecución: quedaron tres mutantes vivos y otro solo lo cazaba el oráculo. Los corregí antes de la ejecución
final:
- P22, media estacional por mediana: los datos sintéticos daban media = mediana por casualidad. Cambié el ruido;
- P29, índice estacional sin normalizar: lo cazaba el oráculo, pero ningún CC. Añadí un cuarto caso de control con
  tendencia curva;
- P64: añadí el empate en la historia de REI-FFO;
- P65, la envoltura deja pasar no finitos: añadí una prueba directa de `_cerrado`.

Registro de la ejecución: se escribe en la carpeta de destino (no se versiona).

## Decisiones para INC-T112-01 (resumen)

Todas las marcadas `[PROPUESTO]` arriba:
- REI-CAP: valor implícito = capitalización + deuda neta; la base del NOI debe coincidir con `base_noi`; `ventana` en
  años enteros, de 15 o más.
- REI-NAV:
  - rechazo estricto con NAV de más de 12 meses (**ambigüedad**);
  - variantes EPRA admitidas;
  - otros pasivos derivados por diferencia;
  - dispersión ponderada.
- REI-FFO: `capex_pct_rentas` sin valor por defecto; último ejercicio común.
- CMD-INV: semana 53 frente a la 52; segunda vía por medias móviles 2×P.
- CMD-RETDEC: anualización aritmética; frecuencias trimestral y anual.
- CHR-FUND: `periodo_horas` en (0, 24]; ponderación «igual»; `ventana_percentil` de 365 días o más; coherencia sin
  umbral.
- CHR-FLOW: ventanas en sesiones; z del acumulado relativo en `ventana_z` años enteros.
- ALT:
  - φ fijado en [0, 1);
  - identidad exacta de la media con término de borde (sin recentrar);
  - GLM por máxima verosimilitud exacta con la representación invertible y arranque del filtro con la observada;
  - Dimson con L = k.

## Ronda r02 · correcciones de la QA r01

La QA r01 (`qa.md`) dejó al grupo P con H-01, H-02, H-07 (por analogía) y H-08 (mutante QP02). Lo que cambió, por
hallazgo. El contrato del servicio es el nuevo: `ent["configuracion"]` y `ent["fecha_corte"]`. P solo usa la fecha de
corte: ninguna de sus ocho fichas lee la configuración.

### H-02 · un parámetro no declarado se rechaza

- `_parametros` rechaza las claves que no están en `PARAMETROS_POR_DEFECTO`, como S y V, con el motivo «parámetros no
  declarados en la ficha». Se exceptúan las de `AJENOS` = {`clase`}, que añade `Motor.servir`.
- Las ocho declaran semilla `null`, así que una `semilla` en `parametros` también se rechaza.
- Pruebas:
  - una errata por ficha (`Ventana`, `capex_pct_renta`, `cap_objetiv`, `excluir_años`, `calendario roll`, `ventana_Z`,
    `ponderación` y, en ALT, `metodo ` y `fi`, el ejemplo de la QA), más `semilla`;
  - `clase` no cambia la cifra, en las ocho (antes solo en REI-CAP).

### H-01 · cota superior para cada tamaño

Ninguna de las ocho fichas fija un máximo para sus ventanas. Las cotas salen de los horizontes del Documento 0
(«Horizontes»: H2 semanas, 2–8 semanas; H5 décadas, 5–30 años). Son valores fijos en `UMBRALES`, así que la petición no
los puede cambiar.

| Ficha · parámetro | Cota | Origen |
| --- | --- | --- |
| REI-CAP-001 · `ventana` (años) | 15–**30** | `[PROPUESTO]` H5 (5–30 años), el horizonte más largo del sistema |
| CHR-FLOW-001 · `ventanas` (sesiones) | 1–**40**, y como mucho 40 ventanas distintas | `[PROPUESTO]` final de H2 (8 semanas × 5 sesiones, `calendario.sesiones_por_semana`), el horizonte más largo de la ficha («Perfiles y horizontes»: H1–H2) |
| CHR-FLOW-001 · `ventana_z` (años) | 1–**30** | `[PROPUESTO]` H5 |
| CHR-FUND-001 · `ventana_percentil` (días) | 365–**10 950** | `[PROPUESTO]` H5 en días (30 × 365, Real/365) |
| CMD-INV-001 · `excluir_anos` (número de años) | **10** | máximo de `anos_estacional` (ficha, 3–10): excluir más años de los que puede tener la referencia no tiene sentido |
| CMD-INV-001 · `anos_estacional` | 3–10 | ficha (ya estaba) |
| ALT-DESMOOTH-001 · `k` (orden GLM y rezagos de Dimson) | 1–3 | ficha (ya estaba) |

REI-FFO-001, REI-NAV-001 y CMD-RETDEC-001 no tienen parámetros de tamaño.

**Defensa en profundidad: la verosimilitud GLM.** La matriz densa n × n hacía que el coste creciera con n³ en tiempo y
con n² en memoria. Con una serie larga en la petición, el proceso podía agotar la memoria o tardar sin fin práctico, el
mismo problema de H-01 por la vía de los datos. Ahora es un Cholesky en banda (`linalg.cholesky_banded`), de coste
O(n·k²):
- es la misma verosimilitud: coincide con la densa a 1e-15;
- n = 10 000 tarda 0,14 s.

Una consecuencia, que también estaba en r01: el arranque «θ iguales» cae en el borde de invertibilidad, porque las raíces
de 1 + z + … + z^k están en el círculo unidad. En series muy largas (n ≳ 1 000), el optimizador a veces se queda ahí y
la ficha rechaza («no invertible»). Falla cerrado, y en series de tamaño realista no pasa: 0 rechazos de 20 con n = 120,
200 y 400. Va a INC-T112-01 como observación.

**Arreglo encontrado al repasar los oráculos de la QA (`r01_05`).** Con los datos 1 del revisor, el óptimo cae en θ0 ≈ 0,
un retardo puro. Al reflejar la raíz en z ≈ 0, el código dejaba un coeficiente del orden del redondeo, cuyo signo
dependía del último bit:
- con la factorización densa salió positivo y se sirvió;
- con la de banda salió −0,0… y se rechazó por «θ < 0».

`_invertible` pone a 0 un coeficiente negativo dentro de la tolerancia de la ficha (1e-8). Hay prueba de regresión con
esos datos y con θ0 ∈ {0, ±1e-17}.

### H-07 · ningún dato en línea posterior a la fecha de corte

`_hasta_corte` rechaza, con «posterior a la fecha de corte (no conocible)», todo dato en línea fechado después de
`ent["fecha_corte"]`. Es lo mismo que hace el servicio con las series de HT-01 (FUGA_DE_INFORMACION) y REI-NAV-001 con un
NAV posterior al precio. Por ficha:

| Ficha | Fechas que se comprueban | No se comprueban (no son fuga) |
| --- | --- | --- |
| REI-CAP-001 | `historia` | — |
| REI-NAV-001 | `fecha_precio` (el NAV ya no podía ser posterior), `historia_prima`; **regla nueva**: la historia de la prima no puede pasar de la fecha de precio, con o sin corte | — |
| REI-FFO-001 | `historia_multiplos`; ejercicios, ver abajo | — |
| CMD-INV-001 | `fecha_publicacion` de cada observación (≥ su periodo), `pendiente_curva` | — |
| CMD-RETDEC-001 | `fechas` de índices o contratos | `calendario_roll` (un roll programado se conoce antes) |
| CHR-FUND-001 | historias de cada plataforma, `futuro`, `spot`, `capitalizacion` | `vencimiento` del futuro |
| CHR-FLOW-001 | `fecha_publicacion` de los flujos, oferta de cada stablecoin, `capitalizacion_total` | — |
| ALT-DESMOOTH-001 | `rentabilidades` y `mercado`, en línea o por `series_rol` | — |

Decisiones `[PROPUESTO]` nuevas:
- **REI-FFO-001: los ejercicios.** La ficha no da fecha de presentación. Se admite un campo opcional
  `fecha_presentacion` por ejercicio:
  - si llega, no puede ser de un año anterior al ejercicio, y con fecha de corte no puede ser posterior a ella;
  - si no llega, con fecha de corte se rechaza el ejercicio del año del corte o posterior (sin cerrar o sin presentar);
  - el del año anterior al corte se sirve, con la limitación «sin `fecha_presentacion`: no se comprueba que se
    conociera».
- **Fechas de referencia sin fecha de publicación.** Los índices de tasación (ALT, REI-CAP, REI-NAV) se publican con
  retraso, pero sus fichas no piden fecha de publicación. Se exige fecha ≤ corte y nada más.
- **El corte rechaza; no recorta.** Un dato posterior rechaza la petición, sin excluirlo con una limitación. Es la regla
  de REI-NAV-001 y la del servicio con HT-01.
- **REI-NAV-001: los datos sintéticos del caso de control.** La historia de la prima llegaba hasta el 2026-12-31, con el
  precio a 2026-09-30. Ahora termina el 2026-09-30, con los mismos valores y los mismos 12 años. El caso sigue superado.

Pruebas:
- las siete fichas fechadas, con el corte en la última fecha, dan la misma cifra que sin corte; con el corte un día
  antes, se rechazan;
- cada bloque opcional fechado (historia de la prima, pendiente de la curva, capitalización, una plataforma,
  stablecoins, mercado) también respeta el corte;
- el vencimiento del futuro y un roll programado después del corte no son fuga;
- REI-FFO-001, de punta a punta;
- niveles por `series_rol`;
- una fecha de corte ilegible se rechaza;
- integración por `Motor.servir`: el rechazo queda en RC, y una errata en `parametros` se rechaza.

### H-08 · mutante QP02 (MDD sin el punto de partida)

Nuevo caso de control de ALT-DESMOOTH-001: «MDD antes y después (RISK-DD-001) con una caída desde el inicio de la serie,
a mano»:
- la serie real cae −10 % y −5 % en los dos primeros trimestres desuavizados y después solo sube, así que su MDD es
  1 − 0,90 · 0,95 = 14,5 %; sin el punto de partida saldría 5 %;
- el MDD observado se comprueba con un recorrido propio que arranca en la riqueza 1.

Hay además una prueba con φ = 0 y un oráculo con `cummax`. ALT-DESMOOTH-001 pasa a cinco casos de control; el grupo, a
26.

### Pruebas y mutantes

- `tests/test_fase2_reales.py`: **585 pruebas** (505 en r01), en verde en unos 21 s.
- Con `tests/test_t112_motor.py`, 638 en verde. Las 2 que fallan en ese fichero son ACC-VAL-001 y FIR-CURVE-001, del
  grupo V, que se estaba editando a la vez.
- ruff y mypy (`--ignore-missing-imports`), sin hallazgos en el módulo ni en las pruebas. ruff se ejecuta desde la raíz,
  con la configuración del gate.
- Todo se pasó sobre copias en `<scratchpad>/r02_P/`; el árbol no se tocó.

| Script | Resultado |
| --- | --- |
| `revisores/impl_P_mutantes.py` | **65 mutantes, 0 vivos frente a CC y T** (copia sin mutar: 585 en verde). De los 50 de fórmula, los CC cazan 48; P61 (beta sin sumar los rezagos) y P64 (percentil estricto, ensayado con REI-CAP) los cazan las pruebas, como en r01. Los mutantes no cambiaron: siguen aplicándose todos sobre el código nuevo |
| `revisores/r01_10_mutantes.py --solo QP01…QP04` | Los cuatro mueren. QP01, QP02 y QP04 ya ante los casos de control; QP03, con `test_alt_oraculo_beta_dimson`. Lo comprobé también con `test_fase2_reales.py` solo, porque la T del script incluye `test_t112_motor.py`, que falla por las dos fichas de V |
| `r01_06_hostiles.py`, parte P (bloques 1, 2, 3 y 5 restringidos a las ocho fichas), con y sin `ulimit -v 6 GB` | **10/10** en las dos: 588 llamadas del fuzzer sin excepciones, una entrada en RC por llamada y nada no finito; ningún parámetro no declarado se sirve; ningún umbral se cambia; determinista en dos Motores |
| Bloques 4 y 7 de `r01_06` adaptados a P (cotas por `_parametros` con 10¹², y fuga por `Motor.servir` con corte 2000-01-01) | **22/22** |
| `r01_05_oraculos_P.py` (oráculos de la QA, statsmodels incluido) | **30/30** |
