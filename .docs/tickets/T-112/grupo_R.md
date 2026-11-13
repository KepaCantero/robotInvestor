# T-112 · Grupo R · riesgo, simulación, backtest y modelos

| Campo | Valor |
| --- | --- |
| Módulo | `bloque_a/11_Ejecutor/bloque_a/motor/fichas_riesgo.py` |
| Pruebas | `bloque_a/11_Ejecutor/tests/test_fase2_riesgo.py`: **415 pruebas, todas en verde** (≈ 10 s) |
| Mutantes | `.docs/tickets/T-112/revisores/impl_R_mutantes.py`, con la salida en `impl_R_mutantes.log`: 43 mutantes, ninguno vivo |
| Fichas | RISK-VAR-001, SIM-MC-001, ML-CAL-001 (heredadas, §6) · SCN-H-001, BT-DSR-001, BT-PBO-001, BT-VAR-001, ML-PRED-001, DEC-VOI-001 (§7) |
| Fuente | Catálogo V5.0: §2, §3 y §20, y cada ficha por su identificador. Nada de `99_Historico*` |
| Dependencias | numpy, scipy y pandas. El módulo importa además `configuracion` (`parametro`, `sesiones_horizonte`, `TABLA_HORIZONTES`) y `motor.evaluacion` (`EPS` del log-score y `ece` de FC-CAL-001) |
| ruff · mypy | sin hallazgos en el módulo, las pruebas ni el script de mutantes |
| Casos de control | 36 en total, y las 9 fichas superan los suyos. También pasan por `Motor.verificar_casos_control`: se comprobó con un parche en memoria sobre `servicio`, sin tocar el archivo |

El módulo exporta `PARAMETROS_POR_DEFECTO`, `UMBRALES`, `ADVERTENCIAS`, `FICHAS` y `CASOS_CONTROL` con el formato de `fichas_mon_idx.py`.

## Integración en `servicio.py` (la hace el coordinador)

1. **Añadir `fichas_riesgo` al bucle de módulos.** Ninguna de las nueve fichas tiene código previo en `IMPLEMENTADAS`.
2. **Semilla.**
   - SIM-MC-001 y SCN-H-001 rechazan la petición si no traen `semilla` (es lo que dice su ficha).
   - Ahora mismo `servir` no pasa `peticion["semilla"]` a los parámetros: la semilla solo llega si viene en `parametros.semilla`.
   - Propuesta: `params.setdefault("semilla", peticion["semilla"])` cuando venga, igual que ya se hace con `clase`.
3. **Clase.** SCN-H-001 exige `clase` (tabla 8.3) y BT-DSR-001 la usa: CRI se anualiza con 365. El servicio ya la añade.
4. **Advertencias.** Las «Supuestos y limitaciones» se entregan ya en `resultado["advertencias"]` y no están en `limitaciones`. Con eso `_advertencias_aparte` no tiene nada que mover y deja el resultado como está.
5. **Ninguna cifra no finita.** La envoltura `_cerrado` rechaza cualquier NaN o inf, así que las nueve fichas pueden entrar en `ESTRICTAS`.
6. **Coste.** Los 36 casos tardan unos 5 s; los cuatro de BT-PBO-001 se llevan casi 1 s cada uno (12 870 combinaciones con S = 16).

## Convenciones comunes

- **Entradas.**
  - Llegan en `ent["valores"]` como listas de números.
  - RISK-VAR, SCN-H y BT-DSR aceptan también una única serie de precios en `ent["series"]` y la pasan a rendimientos simples. Con dos o más series, la ficha rechaza la petición.
  - Lo que viene de otra ficha o de otro módulo (GARCH, régimen, valoración, bloques, rango plausible, muestras) debe traer `fuente`.
- **Unidades.**
  - Rendimientos simples en tanto por uno (§3.1).
  - VaR y ES se entregan como **pérdidas positivas** (fracción del valor), con la misma convención que el ES de TCV-VIXTS-001 y de DER-VRP-001. Una prueba comprueba que coinciden.
- **Umbrales.** Una clave de `UMBRALES` en la petición se rechaza («umbrales fijos»). Cada parámetro tiene tipo y rango (`_validar`). Las claves que la ficha no declara se ignoran, como en TCV.
- **Determinismo.**
  - Con la misma semilla, dos pasadas dan el mismo resultado.
  - SCN-H usa un `SeedSequence.spawn` por horizonte.
  - Las pruebas comprueban también que cambiar la semilla cambia el resultado en SIM-MC, SCN-H, ML-CAL y ML-PRED.

## Por ficha

### RISK-VAR-001 · VaR y ES — supera sus 7 casos

**Qué hace.** Calcula el VaR y el ES al nivel y al horizonte de la petición, como fracción y, si se pide, en moneda. Métodos:
- `historico`;
- `normal`;
- `t`;
- `cornish_fisher`;
- `historico_filtrado`;
- `evt_pot`.

Además:
- **Verificación.** Comprueba que ES ≥ VaR y que el VaR crece con el nivel en 0,90, el nivel pedido y 0,99. Si una de las dos falla, rechaza.
- **Segunda vía.** Si el método es histórico, la segunda vía es la normal; si es otro, es la histórica.
- **Referencia ingenua.** VaR normal con la volatilidad histórica.

**Datos.**
- `valores.rendimientos`, o una serie de precios.
- O bien `valores.distribucion = {rendimientos, semilla}`: la distribución de MC-05, que sin semilla se rechaza.
- `valores.valor_posicion` (opcional), que exige el parámetro `moneda`.

**Rechazos.**
- Menos de 250 observaciones. Con menos de 500 se sirve, con una limitación.
- Nivel 0,99 con el método histórico y menos de 500 observaciones.
- EVT con menos de 50 excedencias.
- Dispersión nula en los métodos paramétricos.
- t con curtosis en exceso ≤ 0.
- Cornish-Fisher no monótona en la cola.

**Coincide con TCV-VIXTS-001 y DER-VRP-001:** nivel 0,975 y rango 0,90–0,99 (hay una prueba que lo compara).

**Decisiones `[PROPUESTO]` (INC-T112-01):**
- horizonte por defecto de 1 periodo, porque la ficha no da ninguno;
- escalado √h para todos los métodos, con la limitación de iid;
- el mínimo de 250 observaciones se aplica a todos los métodos, no solo al histórico;
- t por momentos: ν = 4 + 6/curtosis en exceso, escalada a la varianza muestral;
- ES de Cornish-Fisher integrando z_cf en la cola, y z_cf monótona exigida de forma analítica;
- EVT-POT: umbral en el cuantil 0,90 de las pérdidas. Exige ξ < 1 y que el nivel quede en la cola;
- histórico filtrado con el GARCH(1,1) propio (ver SCN-H);
- la referencia ingenua usa media cero;
- la tabla de decisión de MC-07 no está en el corpus: el método lo elige la petición y por defecto es `historico`.

### SIM-MC-001 · Monte Carlo de trayectorias — supera sus 5 casos

**Qué hace.** Simula la dinámica declarada:
- `paseo_aleatorio`;
- `garch`;
- `bootstrap_filtrado`;
- `saltos` de Merton.

Usa semilla, antitéticas (z, −z intercaladas) y error estándar de MC. Entrega cuantiles, probabilidades de umbral con su EE, una tabla de convergencia, la solución analítica cuando existe y la referencia RI-CLI si se aporta `historia_rendimientos`.

**Datos.**
- `valores.dinamica = {tipo, mu, …parámetros, valor_inicial?}`.
- Parámetros `horizonte` y `semilla`, los dos obligatorios.

**Rechazos.**
- Sin semilla, sin dinámica o sin horizonte.
- n impar con antitéticas.
- GARCH integrado sin `sigma2_inicial`.
- Un parámetro de la dinámica que falta.

**Decisiones `[PROPUESTO]`:**
- dinámicas en log-rendimiento, con salida en nivel (`V0·eˣ`) o en rendimiento simple;
- la tabla de convergencia se hace con mitades sucesivas (n, n/2, n/4, n/8);
- con bootstrap filtrado no se usan antitéticas, y se declara;
- los casos admiten 4 errores estándar y un 10 % en la curtosis.

### SCN-H-001 · Escenarios por horizonte — supera sus 3 casos

**Qué hace.**
- **H1–H2.** GARCH(1,1) y bootstrap filtrado, a través de SIM-MC.
- **H3.** Mezcla por régimen con las probabilidades filtradas de REG-HMM-001, más el ajuste de valoración de MC-09.
- **H4.** Bloques: rendimiento corriente + crecimiento + cambio de valoración, cada uno con su incertidumbre.

En todos los horizontes:
- cuantiles 10/50/90;
- base = mediana; favorable y adverso = cuantiles 80/20, o los narrativos de Prospectiva (con fuente);
- probabilidades de umbral, con la limitación R13;
- referencia RI-CLI (bootstrap incondicional, en H1–H2) y RI-PA.

Verifica la monotonía de los cuantiles y que las bandas crecen de un horizonte al siguiente. Si no crecen, lo declara como limitación.

**Datos.**
- `valores.rendimientos` diarios, o una serie de precios.
- `valores.garch` (opcional, con fuente, p. ej. de VOL-GARCH-001).
- `valores.regimen = {fuente, probabilidades_filtradas, estados: {k: {media, volatilidad}}}` y `valores.valoracion = {fuente, ajuste}`.
- `valores.bloques = {fuente, rendimiento_corriente|crecimiento|cambio_valoracion: {valor, incertidumbre}}`.
- `valores.valor_inicial` (opcional): sin él, la salida va en %.
- Parámetros `semilla` y `clase`, los dos obligatorios.

**Rechazos.**
- Sin semilla.
- Horizonte «No» en la tabla 8.3 para la clase (`TABLA_HORIZONTES`). Un horizonte «Limitado» se sirve, con una limitación.
- H5, que está fuera de la ficha.
- Menos de 2 años diarios en H1–H2: 504 sesiones, o 730 en CRI.
- Probabilidades que no suman 1.
- Escenarios narrativos incoherentes.

**Pasos de cada horizonte.** Salen de la configuración (`sesiones_horizonte`): H1 5, H2 20, H3 126 y H4 252 sesiones, es decir, 1 año.

**Decisiones `[PROPUESTO]`:**
- **GARCH(1,1) por QMLE gaussiana con objetivo de varianza.** Usa Nelder-Mead desde α = 0,05 y β = 0,90, que son valores iniciales fijos como pide VOL-GARCH-001. Si no converge, se rechaza.
- **Por qué no se usa VOL-GARCH-001.** Su ficha pide GARCH-t y el ejecutor la calcula con `arch`, que no es dependencia de A.
- **H3.** El régimen se sortea una vez por trayectoria; dentro de él, normal iid. El ajuste de valoración se suma en log.
- **H4.** Bloques normales independientes, en tasa anual.
- **n par**, por las antitéticas.

### BT-DSR-001 · Sharpe probabilístico y Deflated Sharpe — supera sus 3 casos

**Qué hace.** Calcula:
- el SR por periodo y anualizado: el ingenuo y el de Lo (2002);
- el EE de Lo/Mertens con asimetría y curtosis;
- PSR(SR_referencia), SR\*₀ de Bailey y López de Prado, DSR = PSR(SR\*₀) y MinTRL al nivel pedido.

**Datos.**
- `valores.rendimientos`.
- `valores.varianza_sr_ensayos = {valor, unidad: anual|periodo}`.
- Parámetro `N`, obligatorio.

**Rechazos.**
- Sin N: aclaración.
- Menos de 250 sesiones (diaria) o de 24 meses (mensual).
- Sin la varianza de los SR.
- Dispersión nula.

**Decisiones `[PROPUESTO]`:**
- `SR_referencia` en tasa anual;
- N = 1 ⇒ SR\*₀ = 0, sin deflación, y se declara;
- momentos con la convención de ST-DESC-001: ddof = 1, asimetría y curtosis sin sesgo;
- Lo con autocorrelación AR(1) de primer orden;
- frecuencias diaria y mensual, las dos de «Entradas mínimas».

### BT-PBO-001 · PBO por CSCV — supera sus 4 casos

**Qué hace.**
- Enumera todas las combinaciones C(S, S/2) de bloques.
- En cada una elige la mejor configuración dentro de muestra por Sharpe y mira su rango fuera, con rango medio ante empates.
- Calcula λ = logit(ω), PBO = P(λ ≤ 0), la pendiente de degradación (MCO) y la probabilidad de pérdida fuera de muestra.
- Entrega la frecuencia con que gana cada configuración y un diagnóstico con las bandas de la ficha (0,2 y 0,5).
- Si las configuraciones son idénticas, el PBO queda indefinido y se declara.

**Datos.** `valores.rendimientos = {configuración: [T rendimientos]}`.

**Rechazos.**
- N < 2. Con N < 10 se sirve, con una limitación.
- T < 4·S.
- Longitudes distintas.
- S impar o fuera de 8–20.
- Una configuración constante.

**Decisiones `[PROPUESTO]`:**
- se descartan las T mod S observaciones más antiguas;
- ante un empate dentro de muestra se toma la primera configuración, y se declara;
- los cuantiles de λ se dan en los niveles por defecto de SIM-MC;
- el caso «sin habilidad ⇒ PBO ≈ 0,5» admite ±0,3, unas dos desviaciones entre conjuntos medidas con 20 semillas. Hay además una prueba que promedia 16 conjuntos.

### BT-VAR-001 · Backtesting de VaR y ES — supera sus 3 casos

**Qué hace.**
- Kupiec LR_uc y Christoffersen LR_ind y LR_cc, con sus p-valores y la decisión al nivel de significación.
- Semáforo de Basilea con 250 días al 99 %: verde 0–4, amarilla 5–9 y roja ≥ 10 (BCBS 1996, de la propia ficha). Una prueba lo comprueba con la binomial acumulada.
- Z₂ de Acerbi-Székely.
- Dos modos:
  - `previsto`: con el VaR que se aporta;
  - `generado`: el VaR ex ante sale de RISK-VAR-001 con la ventana anterior a cada t. Este modo incluye además la referencia ingenua, el VaR normal con la volatilidad histórica.

**Datos.**
- `valores.var_previsto`, `resultados` y, opcionalmente, `es_previsto`, todos alineados.
- O bien `valores.rendimientos` para generar el VaR.

**Rechazos.**
- Menos de 250 observaciones, salvo con `baja_potencia_declarada`, que se sirve con una limitación.
- Series que no alinean.
- ES ≤ 0.
- Generación con horizonte > 1.

**Decisiones `[PROPUESTO]`:**
- excedencia = r < −VaR, en sentido estricto;
- el semáforo solo se da con un VaR al 0,99, sobre los últimos 250 días;
- Z₂ sin p-valor, porque haría falta la distribución prevista; se declara;
- la referencia ingenua solo se da en el modo generado.

### ML-CAL-001 · Evaluación interna de modelos predictivos — supera sus 3 casos

**Qué hace.** Para cada horizonte de tipo `nivel`, `probabilidad` o `cuantil` calcula:

| Grupo | Métricas |
| --- | --- |
| Nivel | MAE, RMSE, sesgo, MASE |
| Probabilidad | Brier, log-score, acierto |
| Cuantil | pinball y cobertura del cuantil |
| Comparación | R²_OOS o BSS frente a la referencia |
| Intervalos | cobertura |
| Mejora frente a la referencia | IC por bootstrap de bloques móviles |

Además:
- **Por régimen:** las mismas métricas para cada régimen.
- **Particiones:** comprueba las que se declaran; detecta solapes, falta de embargo y un esquema expansivo con inicio variable.
- **Métricas recomputadas:** rehace por otra vía el RMSE (sesgo² + varianza), el Brier (desarrollado) y el pinball.

**Datos.**
- `valores.ensayos`, obligatorio («número de ensayos obligatorio»).
- `valores.horizontes = {h: {tipo, predicciones, realizaciones, referencia?, cuantil?, intervalos?, particiones?, embargo?, regimenes?}}`.
- Predicciones y realizaciones van como listas o como `{fecha, valor}`, que se alinean por fecha.

**Rechazos.**
- Predicciones y realizaciones que no alinean, por longitud o por fechas.
- Menos de 30 pares.
- Sin `ensayos`.
- Particiones con solape.
- Probabilidades fuera de [0, 1].

**Decisiones:**
- réplicas y nivel del IC: los de `evaluacion.bootstrap_replicas` y `evaluacion.nivel_ic` de la configuración, los mismos que usa FC-EVAL-001;
- longitud de bloque n^(1/3) y recorte del log-score con `EPS`: los de `evaluacion.py` (FC-EVAL-001);
- semilla por defecto 12345, la del servicio para FC-EVAL-001 `[PROPUESTO]`;
- sin referencia aportada se usa RI-PA (último valor) o RI-TB (frecuencia expansiva), desde t = 1 `[PROPUESTO]`;
- MASE con la media de |Δy| de las realizaciones `[PROPUESTO]`.

### ML-PRED-001 · Modelo predictivo con walk-forward — supera sus 4 casos

**Qué hace.**
- **Etiqueta.** Dirección 1{yₜ₊ₕ > yₜ} o nivel yₜ₊ₕ/yₜ − 1, construida desde el objetivo y su criterio de resolución.
- **Walk-forward expansivo con purga y embargo.** El entrenamiento usa i ≤ inicio de la prueba − embargo, con embargo ≥ h.
- **Modelo.** Logística L2 por Newton o ridge, de forma cerrada, con las variables estandarizadas con la ventana de entrenamiento.
- **λ.** Se elige en la rejilla por validación interna.
- **Calibración.** Platt o isotónica (PAV), ajustada solo con predicciones fuera de muestra cuyas etiquetas ya se conocen.
- **Salidas.**
  - predicción actual;
  - métricas fuera de muestra: Brier, log-score, acierto, BSS, ECE (FC-CAL-001) y pendiente b;
  - mejora frente a RI-TB o RI-MH con IC; si el IC incluye 0, «sin mejora demostrada»;
  - registro de ensayos;
  - particiones y su verificación;
  - predicciones fuera de muestra;
  - segunda vía con ventana móvil.

**Datos.**
- `valores.fechas`.
- `valores.objetivo = {serie, horizonte, tipo: direccion|nivel, criterio_resolucion}`.
- `valores.variables = {nombre: {serie, conocible_desde}}`.

**Rechazos.**
- Fuga: `conocible_desde` posterior a la fecha de uso.
- Sin regla de conocibilidad.
- Menos de 60 observaciones independientes, contadas como ⌊(n − h)/h⌋.
- Embargo < h.
- Un modelo que no corresponde al objetivo.
- Sin criterio de resolución.
- Fechas que no son estrictamente crecientes.

**Decisiones `[PROPUESTO]`:**
- rejilla [0,1; 1; 10];
- 5 pliegues y 50 % inicial;
- validación interna con el último 20 % del entrenamiento, con embargo;
- Newton: hasta 100 iteraciones con tolerancia 1e-10;
- la calibración `auto` es Platt;
- sin ensamble de árboles, porque scikit-learn no es dependencia de A; se declara;
- semilla e IC como en ML-CAL.

### DEC-VOI-001 · Valor de la información — supera sus 4 casos

**Qué hace.**
- **Decisiones.** Para cada umbral de la dimensión decisiva (E: E 60 y GC2 50; A: 55; T: 50) y, si se aporta el ranking, para el orden del top-3 (RK frente al de frontera ± amplitud plausible), calcula:
  - EVPI;
  - EVSI, si hay verosimilitud;
  - probabilidad de cambio de decisión.
- **Regla simple (iv).** Si el rango plausible no alcanza ningún umbral ±5 ni cambia el top-3, VOI = 0.
- **Recomendación técnica.** EJECUTAR o NO_EJECUTAR (la decisión es del solicitante).

**Cálculo.**
- **EVPI.** Cerrado para el rango uniforme y empírico para las muestras.
- **EVSI.** Exacto con la regla de Bayes, actuar si X ≥ x\*: E[(S − u)·Φ((S − x\*)/σ)] − máx(E[S] − u, 0).
- **Garantía.** EVPI ≥ EVSI ≥ 0 por construcción.

**Datos.**
- `valores.puntuacion = {dimension, actual}`.
- `valores.rango_plausible = {inferior, superior, fuente}` o `valores.muestras = {valores, fuente}` (histórico del RC).
- `valores.verosimilitud = {desviacion}` (opcional).
- `valores.ranking = {rk_opcion, rk_frontera, amplitud_rk}` (opcional).
- `valores.valor_punto_uc` (opcional).
- Parámetro `coste_uc`, obligatorio.

**Rechazos.**
- Sin rango plausible: aclaración.
- Sin coste.
- Rango vacío.
- Dimensión desconocida.
- Rango o muestras sin fuente.

**Decisiones:**
- **Umbrales.** Se leen de `parametros_ht03.umbrales` y `banda_marginal` de la configuración, que coinciden con el método (iv). No se pueden cambiar desde la petición: el F10 vigente no se lee `[PROPUESTO]`.
- **Distribución.** Uniforme en el rango plausible `[PROPUESTO]`.
- **Decisión previa.** Se toma con E[S] `[PROPUESTO]`.
- **VOI.** El máximo de las decisiones `[PROPUESTO]`.
- **Recomendación.** EJECUTAR si VOI·valor_punto_uc > coste_uc; sin equivalencia en UC, si VOI > 0, con una limitación `[PROPUESTO]`.
- **Búsqueda del corte x\*.** Hasta 60 ampliaciones del intervalo, una constante técnica `[PROPUESTO]`.

## Las que no se deben promover, y por qué

Ninguna falla sus casos de control, así que por CA-1 las nueve son promovibles. Dejo tres avisos para el coordinador y para la QA:

1. **SCN-H-001: la promovería solo si se acepta la decisión sobre el GARCH.**
   - En H1–H2 usa un GARCH(1,1) propio por QMLE gaussiana (`garch_qmle`), no el GARCH-t de VOL-GARCH-001, que en el ejecutor depende de `arch`.
   - Si el operador no acepta esa diferencia en INC-T112-01, se queda con código y DOCUMENTADO, en `DOCUMENTADAS_CON_CODIGO`.
   - Lo mismo vale para el método `historico_filtrado` de RISK-VAR-001. Ese método se puede quitar sin afectar al resto de la ficha.
2. **BT-PBO-001.** El caso «sin habilidad ⇒ PBO ≈ 0,5» es estadístico: con una sola muestra, el PBO varía ±0,15 de un conjunto a otro. La ficha queda cubierta por los otros tres casos, que son exactos (indefinido, dominante = 0 y permutaciones ≥ 0,5), y por un oráculo de fuerza bruta.
3. **DEC-VOI-001.** Los umbrales están fijados en los vigentes de la configuración. Si F10 llega a ajustarlos, DEC-VOI no los seguirá hasta que se integre esa lectura.

## Pruebas (415, todas en verde)

Por ficha:
- **Casos de control.** Además, cada caso numérico falla si las cifras se mueven un 1 ‰ (un 10 % en las de simulación). Los casos estructurales tienen un contraejemplo explícito.
- **Rechazos** de «Aclaración y rechazo» y de «Entradas mínimas».
- **Umbrales fijos.** Se prueba cada clave de `UMBRALES` en la petición.
- **Dominio de los parámetros:** 53 valores fuera de dominio y 9 bordes admitidos.
- **Determinismo** en dos pasadas, y la semilla manda.
- **Entrada intacta.** La ficha no modifica lo que recibe.
- **Entradas hostiles:** vacías, None, texto, NaN, inf, booleanos, listas anidadas, entrada y parámetros que no son objetos, y desbordes.
- **Catálogo.** Versión, módulo y tolerancia se comparan con la «Identificación» y las «Tolerancias» de la ficha; las advertencias, con sus «Supuestos y limitaciones».
- **Al menos un oráculo independiente**, sin llamar al código de la ficha:

| Ficha | Oráculo |
| --- | --- |
| RISK-VAR | cuantil de tipo 7 hecho a mano, `NormalDist` y paridad con el ES de TCV-VIXTS |
| SIM-MC | probabilidad de umbral lognormal y varianza del bootstrap con α = β = 0 |
| SCN-H | H4 con `NormalDist`; la QMLE recupera un GARCH simulado con un bucle propio |
| BT-DSR | PSR, SR\*₀, DSR y MinTRL en Python puro, y la forma cerrada AR(1) de Lo |
| BT-PBO | CSCV por fuerza bruta |
| BT-VAR | verosimilitud binomial de scipy, cadena de Markov a mano, zonas por la binomial acumulada y no anticipación del modo generado |
| ML-CAL | referencias RI-PA y RI-TB con bucles, e IC del bootstrap frente a la aproximación normal |
| ML-PRED | logística con `scipy.optimize`, ridge como mínimos cuadrados aumentados y no anticipación (cambiar el futuro no cambia el primer pliegue) |
| DEC-VOI | EVSI por doble cuadratura directa y EVPI por Monte Carlo |

## Mutantes (43, ninguno vivo)

`impl_R_mutantes.py` trabaja sobre una copia limpia de `bloque_a` (sin `*.docx`) en un directorio propio del scratchpad, que se rehace en cada ejecución. El árbol principal no se toca.

Se probaron entre dos y ocho mutantes de la fórmula principal de cada ficha: cuantiles, escalas, signos, embargo, rangos, anticipación…

| Resultado | Mutantes |
| --- | --- |
| Los cazan los casos de control y las pruebas | 34 |
| Los cazan solo las pruebas | 9 (M20, M23, M29, M32, M34, M37, M38, M41, M43) |
| Vivos | 0 |

Las nueve que solo cazan las pruebas tocan partes que la «Verificación» de la ficha no cubre:
- anualización de Lo;
- λ < 0 frente a ≤ 0;
- borde verde/amarillo del semáforo;
- RI-TB de ML-CAL;
- nivel del IC;
- estandarización y penalización del intercepto en ML-PRED;
- banda marginal y media posterior de DEC-VOI.

En la primera ronda sobrevivieron cinco mutantes. Los mató reforzando:
- el caso del histórico, con horizonte 4 (√h);
- un caso de curtosis GARCH a dos pasos, que separa α de β;
- la intensidad de saltos del caso de Merton;
- el caso de métricas de ML-PRED, ahora con BSS frente a RI-TB rehecha;
- dos pruebas nuevas: los bordes del semáforo y el IC del bootstrap.

La salida completa está en `revisores/impl_R_mutantes.log`.

Para reproducirlo, desde la raíz:

```bash
.venv/bin/python -I -B .docs/tickets/T-112/revisores/impl_R_mutantes.py --copia <dir vacío del scratchpad> --desde 1 --hasta 22
.venv/bin/python -I -B .docs/tickets/T-112/revisores/impl_R_mutantes.py --copia <el mismo dir> --desde 23 --hasta 43
```

## INC-T112-01 · decisiones `[PROPUESTO]` del grupo R, para T-57

**RISK-VAR**
- horizonte por defecto 1;
- √h para todos los métodos;
- mínimo de 250 observaciones para todos los métodos;
- t por momentos;
- ES de Cornish-Fisher por integración, con monotonía exigida;
- umbral de EVT en el cuantil 0,90;
- referencia ingenua con media cero;
- método por defecto `historico`, porque la tabla de MC-07 no está en el corpus.

**SIM-MC**
- dinámicas en log;
- convergencia por mitades;
- sin antitéticas en el bootstrap filtrado;
- casos con 4 EE y un 10 % en la curtosis.

**SCN-H y el histórico filtrado de RISK-VAR**
- GARCH QMLE gaussiana con objetivo de varianza, desde α 0,05 y β 0,90;
- régimen sorteado por trayectoria;
- ajuste de valoración en log;
- bloques de H4 normales e independientes;
- n par.

**BT-DSR**
- SR_referencia anual;
- N = 1 ⇒ SR\*₀ = 0;
- Lo con AR(1).

**BT-PBO**
- se descartan las T mod S más antiguas;
- empate: la primera configuración;
- tolerancia de ±0,3 en el caso sin habilidad.

**BT-VAR**
- excedencia estricta;
- semáforo solo con VaR al 0,99;
- Z₂ sin p-valor;
- referencia ingenua solo en el modo generado.

**ML-CAL**
- semilla 12345;
- referencias por defecto RI-PA y RI-TB;
- denominador del MASE.

**ML-PRED**
- rejilla, pliegues, fracción inicial y validación interna del 20 %;
- tope de Newton;
- `auto` = Platt.

**DEC-VOI**
- distribución uniforme;
- decisión previa con E[S];
- VOI = máximo de las decisiones;
- regla de recomendación sin UC;
- tope de ampliaciones;
- umbrales sin leer F10.
