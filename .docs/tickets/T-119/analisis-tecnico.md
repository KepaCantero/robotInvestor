# T-119 · Análisis técnico

## Motivo

El Catálogo V5.0 del Motor tenía 71 fichas IMPLEMENTADO y 10 DOCUMENTADO, las de prioridad P2 (T-112 las dejó fuera). Una ficha DOCUMENTADO responde `METODO_NO_IMPLEMENTADO`: los analistas de crédito, divisas, materias primas, inmobiliario, cripto y alternativos no tenían esos cálculos citables.

## Implementación

| Fichero | Qué cambia |
| --- | --- |
| `bloque_a/11_Ejecutor/bloque_a/motor/fichas_p2.py` (nuevo) | Las diez fichas, sus parámetros, umbrales, advertencias, datos sintéticos y casos de control |
| `bloque_a/11_Ejecutor/bloque_a/motor/servicio.py` | `MODULOS_P2`, `P2` y `ESTRICTAS = FASE1 \| FASE2 \| P2`; el bucle de registro recorre también el módulo nuevo |
| `bloque_a/11_Ejecutor/tests/test_t119_p2.py` (nuevo) | Pruebas del módulo |
| `bloque_a/11_Ejecutor/tests/test_t119_motor.py` (nuevo) | Integración con el Motor, el Registro de cálculos y el Catálogo |
| `bloque_a/11_Ejecutor/tests/test_unitarias.py`, `test_t65_resto_t53.py`, `test_t112_motor.py` | Regresiones adaptadas (ver `pruebas.md`) |
| `bloque_a/04_Motor_conocimiento_y_catalogo/Catálogo de cálculos del Motor - V5.0.md` | Madurez de las diez fichas (fila del §4 y línea de la ficha) y recuento del §1.3. Nada más |
| `tools/corpus_manifest.txt` | Corpus re-congelado por ese cambio del Catálogo |
| `.docs/scripts/promover_fichas_catalogo.py` | El §1.3 puede quedar sin fichas DOCUMENTADO y nombra T-119 |
| `docs/incidencias.md` | INC-T119-01 |
| `CLAUDE.md`, `bloque_a/11_Ejecutor/README.md`, deuda técnica | Recuentos |

El módulo sigue el patrón de `fichas_reales.py` (T-112) e importa de él las utilidades de validación (`_num`, `_rango`, `_entero`, `_opcion`, `_fecha`, `_tabla`, `_corte`, `_hasta_corte`, `_posicion`) y la envoltura `_cerrado`, a la que añade el rechazo por magnitud. En `servicio.py` basta con añadir el módulo al bucle: las diez entran en `IMPLEMENTADAS`, en `CASOS_CONTROL` y en `ESTRICTAS`. Ninguna declara `semilla`, así que no entran en `ACEPTA_SEMILLA`.

## Reglas comunes

- **Entradas.** Todas en línea, en `ent["valores"]`, con `fecha` ISO. Ninguna ficha lee series de HT-01.
- **Unidades.** Entradas en tanto por uno, salvo ALT-HF-001, que recibe % por periodo, como ACC-FACT-001. Salidas con la unidad en el sufijo (`_pct`, `_pb`, `_veces`).
- **Cotas.** Cada parámetro de tamaño y cada lista de datos tiene cota superior en `UMBRALES`; la lista se rechaza antes de recorrerla. Una cifra de magnitud mayor que 1e100 se rechaza antes de calcular.
- **Parámetros.** Un umbral en la petición o un parámetro no declarado se rechazan.
- **Fecha de corte.** Todo dato observado posterior se rechaza. Los vencimientos de deuda y los desbloqueos de tokens pueden ser posteriores: son fechas contractuales.
- **Frontera 1.6.** FIR-CRED-001, REI-LEV-001 y CHR-TOKEN-001 no entregan ninguna fila por componente.
- **Sin azar.** Las diez declaran semilla `null`.

## Por ficha

### FIR-CRED-001 · Merton agregado — supera sus 4 casos

- **Datos:** `fecha`; `segmento` = {`nombre`, `financiero`, `cobertura`}; `r`; `diferencial_indice_pb`; `componentes` (10 a 500) = {`id`, `capitalizacion`, `volatilidad_acciones`, `deuda_corto`, `deuda_largo`, `mu_historico`}; opcional `pd_historica_rating_pct`.
- **Método:** punto de impago = deuda a corto + ½ deuda a largo. El sistema E = V·N(d₁) − D·e^{−rT}·N(d₂), σ_E·E = N(d₁)·σ_V·V se resuelve con dos raíces de Brent anidadas: dentro, el V que da E (entre E y E + D·e^{−rT}); fuera, el σ_V que da σ_E (entre ½·σ_E·E/V_max y σ_E, horquilla con cambio de signo demostrado). Alternativa ingenua de Bharath-Shumway. DD y PD neutrales (con r) y reales (con μ); diferencial implícito de Merton; agregación en mediana, cuartiles, mínimo, máximo y media ponderada por deuda; proporción con DD < 2.
- **Segunda vía:** triángulo de crédito, intensidad × pérdida en caso de impago del modelo. Aproxima por arriba el diferencial implícito.
- **Rechazos:** segmento financiero, o sin declararlo; menos de 10 componentes; cobertura por debajo de 0,5; componente sin deuda; sistema que no converge a 1e-6.
- **Casos de control:** σ → 0 con V > D ⇒ PD → 0; el sistema recupera los (V, σ_V) con los que se construyeron E y σ_E (fórmula directa frente a inversa); triángulo; ingenuo a mano.

### FX-BEER-001 · Tipo de cambio real de equilibrio — supera sus 4 casos

- **Datos:** `serie` trimestral consecutiva = {`fecha`, `reer`, `terminos_intercambio`, `diferencial_productividad`, `piin_pib`, `diferencial_tipos_reales`}; `vintage`.
- **Método:** q = ln(reer). DOLS con `retardos` adelantos y retardos de las diferencias de los fundamentales, o Johansen (el de FX-COINT-001) normalizado sobre q. Desalineamiento = residuo centrado; equilibrio = e^{c + β'x}; velocidad y vida media con el AR(1) de FX-COINT-001; contraste de cointegración (ADF de los residuos con las tablas de MacKinnon para cinco variables, o traza de Johansen).
- **IC:** solo con DOLS, con la covarianza de Newey-West de β y `evaluacion.nivel_ic` de la configuración del Motor.
- **Segunda vía:** FX-PPA-001, el desalineamiento frente a la media histórica del tipo real.
- **Rechazos:** menos de 15 años; fechas no trimestrales consecutivas; sin vintage o con uno anterior a la última observación; regresión no identificada; ajuste exacto.
- **Limitaciones:** entre 15 y 20 años; sin evidencia de cointegración; Johansen sin IC; desviación que no revierte.
- **Casos de control:** residuo de media nula y DOLS que recupera los coeficientes con los que se construyó el tipo real (la desviación se hace ortogonal al diseño); PPA; vida media a mano; Johansen frente al de FX-COINT-001.

### CMD-REAL-001 · Precio real y coste marginal — supera sus 4 casos

- **Datos:** `moneda`, `ipc_moneda`; `serie` mensual consecutiva = {`fecha`, `precio`, `ipc`}; `curva_costes` = {`fecha`, `fuente`, `tramos`: [{`produccion`, `coste`}]}.
- **Método:** precio real en moneda constante del último mes; percentil y z frente a toda la historia; tendencia real con el Mann-Kendall y la pendiente de Sen de FX-TREND-001 sobre el logaritmo, en % anual; coste del tramo en el que la producción acumulada alcanza el percentil, llevado a moneda constante.
- **Rechazos:** menos de 15 años; IPC de otra moneda; sin curva de costes, sin su fecha o su fuente; curva fuera de la serie.
- **Casos de control:** IPC constante ⇒ real = nominal; método a mano; un precio real log-lineal da su pendiente exacta; percentil 90 de la curva.

### REI-LEV-001 · Apalancamiento y refinanciación — supera sus 3 casos

- **Datos:** `fecha`, `moneda`; `coste_refinanciacion` = {`swap`, `margen`}; `componentes` (hasta 500) = {`id`, `gav`, `deuda`, `caja`, `ebitda`, `gastos_financieros`, `ffo`, `vencimientos`: [{`fecha`, `importe`, `coste`}], opcional `covenants`: {`ltv_max`, `icr_min`}}.
- **Método:** agregado por sumas y dispersión entre componentes de LTV, ICR, deuda neta/EBITDA y vencimientos a 24 meses; impacto en FFO de refinanciar esos vencimientos a swap + margen; LTV ante cada caída de valor; holgura frente a *covenants* e incumplimientos con el valor estresado.
- **Rechazos:** sin perfil de vencimientos; suma de vencimientos distinta de la deuda; vencimiento ya pasado; FFO agregado no positivo.
- **Casos de control:** suma de vencimientos = deuda y vencimientos a 24 meses; ratios y LTV estresado; impacto en FFO y *covenants*.

### CHR-ONCHAIN-001 · MVRV y NVT — supera sus 3 casos

- **Datos:** `fuente` = {`nombre`, `metodologia`, `filtros`}; `serie` diaria consecutiva = {`fecha`, `capitalizacion`, `capitalizacion_realizada`, `volumen_ajustado`}.
- **Rechazos:** sin fuente verificable; menos de 2 años; huecos; capitalización sin dispersión. **Limitación:** «pocos ciclos» con menos de 4 años.
- **Casos de control:** MVRV = 1 si precio = coste medio; método a mano; otra media de la señal NVT.

### CHR-TOKEN-001 · Tokenómica y dilución — supera sus 3 casos

- **Datos:** `fecha`, `fuente`, `ambito`; `tokens` (hasta 500) = {`id`, `precio`, `oferta_circulante`, `oferta_total`, `oferta_maxima`, `emision_anual`, `quema_anual`, `calendario`: {`fuente`, `desbloqueos`}, opcionales `staking_nominal`, `concentracion_10_mayores`}.
- **Rechazos:** circulante > total o total > máxima; sin calendario verificable; desbloqueos futuros por encima de la oferta no circulante.
- **Casos de control:** circulante = total = máxima ⇒ FDV/CM = 1; método a mano; *staking* y concentración con su cobertura.

### PRV-PME-001 · Public market equivalent — supera sus 3 casos

- **Datos:** `moneda`; `flujos` = [{`fecha`, `aportacion`, `distribucion`}]; `nav_final`; `indice` = {`nombre`, `moneda`, `rentabilidad_total`, `riesgo_comparable`, `niveles`}.
- **Rechazos:** sin flujos fechados; sin aportaciones; índice en otra moneda, de precios o sin nivel en una fecha; NAV anterior al último flujo.
- **Casos de control:** flujos que replican el índice ⇒ KS-PME = 1, alfa directo 0 y λ = 1; método a mano con valor actual neto nulo en la TIR; PME+.

### PRV-CF-001 · TIR, múltiplos, curva J y proyección — supera sus 3 casos

- **Datos:** `compromiso`; `flujos`; `navs`; opcionales `vida_anios` y `referencia_cosecha`.
- **Proyección:** Takahashi-Alexander desde el estado actual, por año de vida. Necesita `tasas_aportacion`, `crecimiento` y `vida_anios`; sin alguno, `null` y limitación.
- **Casos de control:** TVPI = DPI + RVPI con la curva J a mano; TIR exacta del 10 %; proyección a mano.

### ALT-HF-001 · Exposición factorial de estrategias hedge — supera sus 3 casos

- **Datos:** `serie` mensual consecutiva = {`fecha`, `r`, `rf`, y un valor por factor}; o `en_exceso: true` sin `rf`.
- **Rechazos:** menos de 36 observaciones; factores colineales; φ fuera de (−1, 1); falta un factor.
- **Casos de control:** coherencia con ACC-FACT-001 (se ejecuta con los mismos datos); recupera alfa y exposiciones exactas con los siete factores; desuavizado y regresión a mano.

### ALT-AUC-001 · Índice de coleccionables — supera sus 3 casos

- **Datos:** `categoria`; `transacciones` (500 a 50 000) = {`id_pieza`, `fecha`, `precio`, opcional `caracteristicas`}; opcional `referencia`.
- **Rechazos:** menos de 500 transacciones; menos de 200 pares en ventas repetidas; años sin transacciones; índice no identificado; hedónico sin características o con características colineales.
- **Casos de control:** índice = 100 en la base y ventas repetidas que recuperan el índice con el que se construyeron los precios; el método alternativo da el mismo índice; Bailey-Muth-Nourse a mano con ruido, neta de comisiones.

## Decisiones tomadas y desviaciones del plan

- Las decisiones de método están en INC-T119-01 `[PROPUESTO]`, a T-57.
- **Ninguna ficha se queda en DOCUMENTADO.** Las diez piden datos que el repositorio no tiene, pero todas se pueden calcular con honradez sobre datos en línea con su fuente declarada, como ya hacían las fichas de T-106 y T-112; sin fuente, sin fechas o por debajo del mínimo, rechazan.
- **Lo que una ficha nombra y no se calcula**, declarado: LN-PME (PRV-PME-001), la ponderación de Case-Shiller (ALT-AUC-001), el intervalo del desalineamiento con Johansen (FX-BEER-001).
- **Cota de magnitud**, no prevista en el plan: sin ella, una suma que desborda daba un total infinito y, al dividir por él, un cero con apariencia de cifra.

## Límites conocidos

- **Coste al máximo de las cotas** (una pasada; el Motor hace dos): ALT-AUC-001 con 50 000 transacciones, 100 años y 20 características, unos 5 s y menos de 500 MB (24 s con la máquina cargada); CHR-TOKEN-001 con 500 tokens y 1 000 desbloqueos cada uno, 3 s; las demás, menos de 1 s (FIR-CRED-001 con 500 componentes, 0,04 s).
- **TIR con varias soluciones:** se avisa y se entrega la que encuentra la búsqueda; con un número par de raíces en el rango, `null`.
- **FX-BEER-001:** el IC solo recoge la incertidumbre de los coeficientes; cinco variables con 60 a 100 trimestres dan contrastes de poca potencia.
- **ALT-AUC-001:** sin ajuste de sesgo de selección; la rentabilidad neta supone una sola compraventa en toda la ventana.
- **Datos reales:** ninguna prueba usa datos reales; eso es el paso a VALIDADO (Fase 4).

## Comandos

```bash
cd bloque_a/11_Ejecutor
../../.venv/bin/pytest -q tests/test_t119_p2.py tests/test_t119_motor.py
cd ../..
.venv/bin/python -I .docs/scripts/promover_fichas_catalogo.py --etiqueta "ejecutor, casos de control registrados (T-119)"   # sin --aplicar, solo informa
.venv/bin/python -I -B .docs/tickets/T-119/revisores/impl_p2_mutantes.py <carpeta desechable>
```
