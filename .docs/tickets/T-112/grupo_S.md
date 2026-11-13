# T-112 · Grupo S · estadística y series

| Campo | Valor |
| --- | --- |
| Módulo | `bloque_a/11_Ejecutor/bloque_a/motor/fichas_series.py` |
| Pruebas | `bloque_a/11_Ejecutor/tests/test_fase2_series.py` |
| Mutantes | `.docs/tickets/T-112/revisores/impl_S_mutantes.py` |
| Fichas | ST-INF-001, FX-BRK-001, FX-STL-001, FX-REGIME-001, REG-HMM-001, FX-COINT-001, BIB-MET-001, TEM-DIFF-001 |
| Fuente de verdad | Catálogo V5.0: §6 (heredadas), §7 (REG-HMM-001 y TEM-DIFF-001), §3 (convenciones) y §20 (casos de control) |

El módulo exporta `PARAMETROS_POR_DEFECTO`, `UMBRALES`, `ADVERTENCIAS`, `FICHAS` y `CASOS_CONTROL` con el mismo formato que
los módulos de T-106. Solo usa numpy, scipy y pandas: Markov switching, HMM, Johansen, Engle-Granger, STL y LOESS están escritos
con numpy y scipy. No toca `servicio.py` ni ningún otro archivo.

## Reglas comunes

- **Firma.** `fn(ent, params) -> (resultado, limitaciones)`. La envoltura `_cerrado`:
  - valida la forma de `ent`;
  - aplica `_parametros`, que rechaza un umbral de `UMBRALES` («umbral fijo de la ficha») y un parámetro desconocido. Se admite
    `clase` porque el servicio la añade a toda petición;
  - traduce las excepciones numéricas o de tipo a `ErrorFicha`;
  - rechaza cualquier no finito del resultado;
  - pone `ADVERTENCIAS[ficha]` en `resultado["advertencias"]`, nunca en las limitaciones.
- **Dominio.** Todo parámetro de la petición tiene tipo y rango (`_validar`).
- **Datos.** Llegan en `valores`, con `fechas` ISO opcionales. Las series de HT-01 (`ent["series"]`) se aceptan:
  - en FX-BRK, FX-STL y FX-COINT, como niveles;
  - en FX-REGIME, como rendimientos simples (3.1);
  - en ST-INF, como rendimientos simples contrastados frente a 0.
- **Semilla.** FX-REGIME, REG-HMM y TEM-DIFF tienen azar y lo controlan con el parámetro `semilla` (por defecto 0). **Para la
  integración:** el servicio no pasa `peticion["semilla"]` a `params`. Si se quiere que la semilla de la petición mande, el
  servicio debe copiarla en `params["semilla"]` para estas tres fichas.
- **Casos de control.** Se ejecutaron con `Motor.verificar_casos_control`, inyectando el módulo en memoria en un guion de
  borrador sin tocar `servicio.py`: las 8 fichas superan sus 36 casos (dos pasadas idénticas y la comprobación).

## Por ficha

### ST-INF-001 · Contrastes, intervalos y comparaciones múltiples

**Qué hace.** Contrasta lo declarado y devuelve, por contraste:
- estadístico, grados de libertad, p-valor e IC (en los contrastes t);
- tamaño del efecto;
- normalidad, comprobada con Shapiro-Wilk;
- p ajustado: Holm o Benjamini-Hochberg cuando m > 1;
- potencia y n mínimo, solo si se piden.

**Datos.** `valores.contrastes`, una lista con:
- `nombre`;
- `muestra` o `estadisticos {media, desviacion, n}`;
- o `muestra_a`/`muestra_b`, o `estadisticos_a`/`estadisticos_b`;
- `mu0`.

También se puede contrastar cada serie de HT-01: sus rendimientos frente a 0.

**Decisiones `[PROPUESTO]`:**
- Contrastes disponibles: t de una muestra, t pareado, t de Welch, Wilcoxon de rangos con signo y Mann-Whitney.
- `tipo_contraste` no tiene valor por defecto, porque la ficha pide un «contraste declarado»: si falta, se rechaza.
- `correccion: auto` aplica Holm, que controla la tasa de error por familia; `bh` es opcional. Con m > 1 no se admite «ninguna».
- `mu0` vale 0 por defecto.
- Se rechaza H₀ si p < nivel, que es lo coherente con un IC cerrado: si μ₀ está en el extremo del IC, p = nivel.
- Tamaño del efecto:
  - d de Cohen; en Welch, con la raíz de la media de las dos varianzas;
  - correlación biserial de rangos en los contrastes de rangos.
- Los contrastes de rangos no llevan IC; se declara como limitación.
- Normalidad: si Shapiro-Wilk da p < nivel, se añade una limitación, no un rechazo.
- Potencia con la t no central. En Welch, n mínimo por grupo con la aproximación de varianzas iguales.
- «Los datos no sostienen el contraste»:
  - n < 2;
  - dispersión nula;
  - todas las diferencias nulas (Wilcoxon);
  - todo empatado (Mann-Whitney).
- Dominios:
  - nivel en (0, 1);
  - efecto_potencia > 0;
  - potencia_objetivo en (0, 1), y exige efecto_potencia.

**Casos de control (6, superados):**
- p conocido con 2 gl (forma cerrada) y su IC;
- p conocido con 1 gl (Cauchy);
- Mann-Whitney exacto: p = 2/C(6,3);
- coherencia entre IC y p-valor, con μ₀ en el extremo, dentro y fuera;
- Holm por definición;
- Benjamini-Hochberg por definición.

### FX-BRK-001 · Rupturas estructurales

**Qué hace.**
- Bai-Perron por programación dinámica, con recorte y BIC.
- CUSUM de residuos MCO como primera vía, con su p-valor de Kolmogorov.
- Clasificación del tipo: nivel, pendiente o varianza.
- Fechas con IC de Bai (1997).
- Segunda vía: la fecha del CUSUM cae en el IC de Bai-Perron.

**Datos.** `valores.serie` (con `fechas`) o una serie de HT-01.

**Decisiones `[PROPUESTO]`:**
- Los tres tipos de modelo:
  - nivel: media por segmento;
  - pendiente: recta por segmento, cambian la constante y la tendencia;
  - varianza: varianza por segmento, con la media global.
- `auto` elige el BIC mínimo entre los tipos y el número de rupturas, 0 incluido.
- BIC = −2 ln L + k ln n, con k = q(m+1) + m + 1 (más una varianza).
- Segmento mínimo h = máx(⌈recorte·n⌉, q + 1). Dominio de `recorte`: (0, 1/(max_rupturas + 1)].
- IC de la fecha: Bai (1997) aplicado a la «señal» del tipo, con la CDF de Yao (1987) y nivel de confianza 1 − nivel:
  - nivel: la propia serie y;
  - pendiente: Δy, una aproximación conservadora que se declara como limitación;
  - varianza: (y − ȳ)².
- El índice de una ruptura es la primera observación del régimen nuevo.
- Una serie constante se rechaza.

**Casos de control (6, superados):**
- salto conocido: fecha exacta, salto igual a la diferencia de medias, IC que contiene la fecha y CUSUM que coincide;
- Bai-Perron coincide con la búsqueda exhaustiva de la SSR;
- sin ruptura: 0 rupturas y el CUSUM no rechaza;
- dos rupturas exactas;
- ruptura de varianza;
- ruptura de pendiente.

### FX-STL-001 · Descomposición tendencia-ciclo-estacionalidad

**Qué hace.**
- STL de Cleveland et al. (1990) con LOESS local lineal, robusto o no.
- Esquema aditivo o multiplicativo (STL sobre el logaritmo).
- Componentes de salida: tendencia, estacional, resto y serie ajustada.
- Diagnóstico: F de estacionalidad estable (ANOVA por posición) y variación del patrón.
- Segunda vía: medias móviles centradas.

**Datos.** `valores.serie` con `periodo`, o con `fechas` de las que se deduce el periodo.

**Decisiones `[PROPUESTO]`:**
- n_s = 7.
- n_l es el impar ≥ periodo; n_t, el impar ≥ 1,5·p/(1 − 1,5/n_s).
- Bucles (interno, externo): (2, 15) si es robusto y (5, 0) si no.
- `auto` elige multiplicativo si la varianza del resto en logaritmos es menor que la del resto aditivo relativo a la tendencia;
  solo se plantea con serie positiva.
- Periodo deducido de la frecuencia (pandas `infer_freq`):

  | Frecuencia | Periodo |
  | --- | --- |
  | mensual | 12 |
  | trimestral | 4 |
  | semanal | 52 |
  | días hábiles | 5 |
  | diaria | 7 |

  Con otra frecuencia, o con fechas irregulares, hay que declarar `periodo`.
- Con menos de 3 ciclos se añade una limitación.

**Casos de control (4, superados):**
- identidad T + S + R = serie, con ruido;
- estacionalidad conocida recuperada a 1e-6 (y el esquema elegido es aditivo);
- multiplicativo: T·S·R = serie, y `auto` lo elige;
- segunda vía de medias móviles igual en el caso exacto.

### FX-REGIME-001 · Regímenes univariantes (Markov switching)

**Qué hace.**
- Hamilton con 2 o 3 estados, ajustado por máxima verosimilitud con EM (Baum-Welch) y varios arranques.
- Probabilidades filtradas (operativas) y suavizadas (marcadas «solo descriptivas»).
- Transiciones, duraciones, distribución estacionaria y régimen actual según el umbral.
- Segunda vía: otra semilla.
- Referencia ingenua: un solo régimen, por BIC.

**Datos.** `valores.serie` (rendimientos) o una serie de precios de HT-01, que se pasa a rendimientos simples.

**Decisiones `[PROPUESTO]`:**
- Sin términos autorregresivos.
- 20 arranques, como REG-HMM-001. Arranques aleatorios por cuantiles aleatorios de la serie, o de |x − mediana| si solo cambian
  las varianzas.
- Semilla por defecto 0; la segunda vía usa semilla + 1.
- Convergencia: el cambio relativo máximo de los parámetros baja de 1e-6·1e-2 (`FACTOR_CONVERGENCIA`), para reproducir 1e-6 con
  convergencia lineal.
- Tope de 1 000 iteraciones. Si ningún arranque converge: «CONVERGENCIA».
- Suelo de varianza: tol·var(y).
- Distribución inicial: la suavizada en t = 1 (EM estándar).
- Etiquetas por varianza creciente, o por media si las varianzas son iguales.
- El mínimo de 100 observaciones (200 recomendadas) se aplica también con 3 estados.
- La segunda semilla «coincide» si |ΔLL| ≤ 1e-6·(1 + |LL|).

**Casos de control (4, superados):**
- filtradas, suavizadas y filas de la transición suman 1;
- filtradas y log-verosimilitud reproducen el filtro de Hamilton paso a paso;
- otra semilla llega al mismo óptimo;
- el BIC prefiere dos regímenes, con identidades del BIC.

### REG-HMM-001 · Régimen de clase (HMM multivariante)

**Qué hace.**
- HMM gaussiano sobre las variables estandarizadas, con covarianza diagonal o completa.
- Número de estados de 2 a 4, por BIC o declarado.
- 20 arranques o más, con semilla.
- Probabilidades filtradas actuales y su serie, transiciones, duraciones y medias por estado (originales y estandarizadas).
- Referencia ingenua: el régimen de la observación anterior y la distribución incondicional.

**Datos.** `valores.variables` (nombre → lista) y `fechas`, o `frecuencia` (`semanal` o `mensual`).

**Decisiones `[PROPUESTO]`:**
- Estandarización con toda la ventana de entrenamiento. Se declara como limitación: la serie histórica de filtradas no es
  estrictamente en tiempo real.
- El BIC cuenta la distribución inicial.
- Las variables se ordenan alfabéticamente y las etiquetas siguen la media de la primera.
- Suelo de covarianza: tol·I.
- Mismo criterio de convergencia y tope que FX-REGIME.
- Una frecuencia que no sea semanal ni mensual se rechaza.

**Casos de control (4, superados):**
- las filas suman 1 y los estados quedan ordenados;
- estabilidad entre semillas;
- las filtradas y la log-verosimilitud se reproducen con densidades normales de scipy, con covarianza diagonal y con completa.

**Coste.** Con `n_estados: BIC`, unos 12 s por llamada con n = 300; el Motor hace dos pasadas. Los casos de control fijan 2 estados
(menos de 1 s).

### FX-COINT-001 · Cointegración y corrección de errores

**Qué hace.**
- ADF de cada serie, en nivel y en diferencias, para el orden de integración.
- Johansen (traza) o Engle-Granger.
- Vector normalizado en la primera serie, velocidades de ajuste, MCE y vida media.
- Serie de desviación del equilibrio.
- Segunda vía: el método no elegido.

**Datos.** `valores.series` (de 2 a 5 series de igual longitud, con `fechas`) o series de HT-01, alineadas por fechas comunes.

**Decisiones `[PROPUESTO]`:**
- Johansen en el caso 2: constante restringida al vector, sin tendencia en los datos.
- Valores críticos asintóticos de la literatura de la ficha:
  - traza de Johansen: MacKinnon, Haug y Michelis (1999);
  - ADF y Engle-Granger: MacKinnon (2010), τ∞.

  Por eso `nivel` solo admite 0,01, 0,05 o 0,10, y se aceptan como máximo 5 series. Las tablas se verificaron con una simulación
  Monte Carlo, que es también una prueba.
- `max_rezagos: AIC` busca hasta ⌊4(T/100)^{2/9}⌋ (la regla de ACC-FACT-001). El orden del VAR también se elige por AIC, hasta ese
  tope + 1.
- Vida media: AR(1) de la desviación, ln ½ / ln ρ. Si ρ ∉ (0, 1), no hay vida media y se declara.
- MCE de Engle-Granger con Δx contemporáneas.
- Si alguna serie no es I(1), se añade una limitación (no un rechazo).

**Casos de control (4, superados):**
- residuos de media nula en la regresión de cointegración y en el MCE;
- Johansen y Engle-Granger coinciden en un par cointegrado conocido;
- paseos aleatorios independientes, sin cointegración;
- traza = −T·Σ ln(1 − λ) y vida media = ln ½ / ln ρ.

### BIB-MET-001 · Bibliometría aplicada a fuentes

**Qué hace.**
- Conteos por periodo (con los periodos vacíos a 0), por temática, por fuente y cruzados.
- HHI por fuente y crecimiento CAGR (FIN-CAGR-001, `operaciones.cagr`).
- Duplicados por huella y por título normalizado.
- Precisión y exhaustividad frente a una referencia.
- Comprobación de que los totales cuadran.

**Datos.** `valores.fichas` con `fecha`, `tematica` y `fuente` obligatorias, e `id`, `titulo` y `hash` opcionales.
`valores.referencia` (identificadores) es opcional.

**Decisiones `[PROPUESTO]`:**
- Granularidades: mensual, trimestral y anual.
- Un solo registro mal formado o un `id` repetido hace que todo el conjunto se rechace como «corrupto».
- Duplicados: componentes conexas por huella (sin distinguir mayúsculas) o por título normalizado (NFKD, sin acentos, en
  minúsculas y solo alfanuméricos).
- HHI en escala 0–1.
- CAGR entre el primer y el último periodo, con años = (periodos − 1)/periodos por año. Si un extremo es 0, no hay CAGR y se
  declara.
- **Para la integración:** la ficha limita los solicitantes por CT-09 al Orquestador técnico y al Evaluador. El manejador no ve al
  solicitante: la regla va como advertencia, y si se quiere aplicar debe hacerlo `servicio.py`.

**Casos de control (4, superados):**
- totales recontados aparte;
- duplicados;
- HHI y CAGR;
- precisión y exhaustividad.

### TEM-DIFF-001 · Curvas de difusión y adopción

**Qué hace.**
- Ajusta tres curvas por mínimos cuadrados no lineales con varios arranques: logística, Gompertz y Bass.
- Elige por AIC y da el error fuera de muestra.
- Fase y punto de inflexión (año decimal y fecha).
- Previsión con bandas 10/50/90 por bootstrap de residuos.
- Escenarios de techo m.
- Segunda vía: el modelo alternativo.
- Referencia ingenua: extrapolación lineal y crecimiento constante (FIN-CAGR-001).

**Datos.** `valores.adopcion` (acumulada), `anios` (decimales) o `fechas`, y `lanzamiento` opcional.

**Decisiones `[PROPUESTO]`:**
- Horizonte de 5 años (el límite de H4 en el Documento 0), con dominio (0, 30] (el límite de H5).
- Lanzamiento por defecto: un periodo antes de la primera observación. Solo lo usa Bass.
- Tramo de aceleración: algún Δy_{i−1} > 0 con Δy_i > Δy_{i−1}.
- Arranques:
  - m₀ ~ U(máx y, máx y/0,16);
  - t₀ ~ U(t₁, t_n + (t_n − t₁));
  - k₀, p₀ y q₀, de la pendiente máxima observada.
- `least_squares` (trf) con xtol = ftol = gtol = tol² = 1e-12.
- AIC = n ln(SSR/n) + 2k.
- Error fuera de muestra en el último cuarto (⌊n/4⌋), solo si el tramo de ajuste conserva 8 observaciones. Si el AIC y el error
  fuera de muestra no coinciden, se añade una limitación.
- `m`:
  - un número lo fija; se rechaza si es menor que la adopción observada;
  - una lista da escenarios.
- Fases: < 16 % introducción, 16–50 % crecimiento, > 50 % madurez.
- Dominios: `arranques` ≥ 1, `B` ≥ 1.

**Casos de control (4, superados):**
- logística recuperada a 1e-6;
- Gompertz elegida, con el modelo alternativo servido;
- Bass con su inflexión ln(q/p)/(p+q);
- fase de introducción con el techo declarado.

## Promoción

Las 8 fichas superan sus casos de control y se pueden promover, **a condición de que el operador acepte las decisiones `[PROPUESTO]`
de INC-T112-01**. Hay que tener en cuenta:

- **FX-COINT-001.** Sus valores críticos son tablas de la literatura (`[PROPUESTO]`), verificadas por simulación. Si el operador no
  las acepta, la ficha no se debe promover.
- **BIB-MET-001.** La restricción de solicitantes de CT-09 no la aplica el manejador. Promoverla sin aplicarla en el servicio deja
  la regla solo como advertencia.
- **REG-HMM-001.** Con BIC es lenta (unos 12 s por pasada con n = 300). No impide la promoción, pero hay que tenerlo en cuenta en
  los presupuestos.

No hay ninguna ficha del grupo que no supere sus casos.

## Pruebas y mutantes

- `tests/test_fase2_series.py`: 320 pruebas, todas en verde (unos 70 s):
  - casos de control y prueba de que cada caso puede fallar ante un resultado alterado;
  - rechazos de «Aclaración y rechazo» y «Entradas mínimas»;
  - dominio de cada parámetro;
  - cada umbral fijo, rechazado desde la petición;
  - parámetros desconocidos;
  - determinismo de dos pasadas y semilla;
  - entradas hostiles: vacías, NaN, inf, texto, None, bool, estructuras mal formadas y desbordamiento;
  - al menos un oráculo independiente por ficha:

    | Ficha | Oráculo |
    | --- | --- |
    | ST-INF-001 | scipy `ttest_ind`/`ttest_rel`; Wilcoxon exacto; n de Cohen; Monte Carlo |
    | FX-BRK-001 | cuantiles de Bai (1997); BIC, CUSUM e IC a mano |
    | FX-STL-001 | `polyfit` ponderado frente al LOESS; ANOVA a mano |
    | FX-REGIME-001 | filtro de Hamilton escalar; máximo local |
    | REG-HMM-001 | filtro con densidades a mano; estacionaria |
    | FX-COINT-001 | autovalores por correlaciones canónicas; Engle-Granger con `polyfit`; tablas por Monte Carlo |
    | BIB-MET-001 | `Counter` |
    | TEM-DIFF-001 | `curve_fit` de scipy; AIC a mano |
- `ruff check` y `mypy --ignore-missing-imports` sobre el módulo y las pruebas: sin hallazgos.

### Mutantes

`impl_S_mutantes.py` define 55 mutantes de las fórmulas principales y de las reglas de rechazo de las 8 fichas: estadísticos,
IC, Holm/BH, BIC, programación dinámica, CUSUM, IC de Bai, LOESS, paso bajo, criterio de esquema, pasos E y M, etiquetado, traza,
valores críticos, vida media, HHI, duplicados, CAGR, curvas, inflexión, fases, AIC, bandas, umbrales fijos, parámetros
desconocidos y cifras no finitas. Trabaja sobre copias de `bloque_a` sin `*.docx` en el directorio que se le indique (el
scratchpad), nunca sobre el árbol principal. Mide dos cosas:
- CC: los casos de control de la ficha, con dos pasadas;
- T: las pruebas de la ficha, con `-k`.

Antes de mutar, la copia sin mutar pasa todas las pruebas.

| Pasada | Mutantes | Vivos frente a CC | Vivos frente a CC y T a la vez |
| --- | --- | --- | --- |
| 1.ª | 55 | 31 | 11: B02, B04, L01, L06, H02, H07, C02, C06, C07, H11, D03 |
| 2.ª (`--solo` con los 11 vivos, tras añadir las pruebas de abajo) | 11 | 11 | 0 |

Pruebas añadidas para matar a los 11 vivos:
- recorte del segmento mínimo de Bai-Perron;
- IC de Bai con un salto pequeño;
- paso bajo exacto con una serie periódica pura;
- serie ajustada aditiva;
- derivada nula de la verosimilitud en el máximo (FX-REGIME, y REG-HMM con covarianza completa);
- valores críticos y decisión fila a fila, con una traza entre la mitad del valor crítico y el valor crítico;
- α de Johansen por MCO;
- fases por umbral.

**Resultado final: ningún mutante sobrevive a la vez a los casos de control y a las pruebas.** Los vivos frente a CC son
mutantes de reglas de rechazo, de dominio o de cifras que los casos de control no ejercitan. Por ejemplo, los mínimos de
observaciones, el sesgo pequeño de un paso M o el valor crítico. Los cazan las pruebas.

Mutante equivalente no incluido: usar la misma semilla en la segunda vía de FX-REGIME-001 o REG-HMM-001. Llega al mismo óptimo y
no se distingue desde fuera. Se declara aquí: la segunda vía «otra semilla» solo puede detectar óptimos distintos, no comprobar
que se usó otra semilla.

Uso:

```
.venv/bin/python -I -B .docs/tickets/T-112/revisores/impl_S_mutantes.py <scratchpad>/mut -j 3
```

Tarda unos 20 minutos con 3 copias.

## Ronda r02 (correcciones de la QA r01)

Hallazgos del grupo S en la QA r01: H-01 (tamaños sin cota) y H-08 (mutantes QS04, QS05 y QS08 vivos). Solo cambian
`motor/fichas_series.py`, `tests/test_fase2_series.py` y esta nota.

### H-01 · Cotas de los tamaños de la petición

**Qué cambió.**
- Cada tamaño tiene una cota fija en `UMBRALES` (la petición no la puede cambiar: la regla «umbral fijo» la cubre).
- Las cotas de datos se comprueban **antes** de convertir o calcular (`_vector(..., maximo=)`, `_serie_ht01(..., maximo)`):
  lo que pasa de la cota se rechaza en milisegundos.
- `_entero` compara los enteros sin pasar por float, para que la cota sea exacta (2⁶³ − 1 entra y 2⁶³ no).
- La búsqueda del n mínimo de potencia de ST-INF-001 no pasa de la cota de observaciones: si la aproximación ya la supera
  (o con d diminuto, que antes podía desbordar o no acabar), `n_minimo` es None, con `n_minimo_supera_cota` y una limitación.
- TEM-DIFF-001 rechaza, antes de ajustar, un horizonte que daría más puntos de previsión que la cota (p. ej., datos diarios
  con 5 años: 1 825 puntos). Antes, un paso de tiempo diminuto pedía un `arange` sin fin práctico.
- Coste, sin cambiar las cifras de método:
  - FX-BRK-001: los índices de la matriz de costes van por difusión en vez de `meshgrid`. Mismas cifras, bit a bit, y dos
    matrices n² de enteros menos (n = 2 520: unos 640 MB en vez de 730 MB, 5 s).
  - FX-STL-001: el LOESS se calcula por bloques y solo sobre la banda de puntos que pueden pesar (los q vecinos están a
    distancia ≤ q). Pasa de O(n²) a O(n·q): n = 2 520 con periodo 12, de 156 s a 6 s por llamada. Diferencia con el LOESS
    anterior ≤ 3e-13 relativa (orden de las sumas) en 126 combinaciones de longitud, q, posiciones y pesos robustos; el
    oráculo de mínimos cuadrados ponderados de las pruebas sigue igual.

**Cotas y su origen.**

| Ficha | Cota | Valor | Origen |
| --- | --- | --- | --- |
| Todas las de series | `obs_maximas` | 2 520 | H5 en sesiones: 120 meses = 2 520 (Anexo A del Documento 0; `horizontes` y `calendario` de la configuración) |
| ST-INF-001 | `obs_maximas` (por muestra y `n` de los estadísticos) | 2 520 | ídem |
| ST-INF-001 | `contrastes_maximos` | 1 000 | `[PROPUESTO]` |
| FX-BRK-001 | `obs_maximas` | 2 520 | H5 en sesiones (max_rupturas ya tenía 1–5, de la ficha) |
| FX-STL-001 | `obs_maximas` | 2 520 | H5 en sesiones |
| FX-STL-001 | `periodo_maximo` | 52 | `[PROPUESTO]`: el mayor de la tabla de frecuencias de la ficha (semanal) |
| FX-REGIME-001 | `obs_maximas` | 756 | `[PROPUESTO]`: la ventana de datos de las fichas del lote, `senales.ventana_anios` 3 (configuración, T-65), × 252 sesiones (Catálogo 3.1). Arranques (20) e iteraciones (1 000) ya eran fijos |
| REG-HMM-001 | `arranques_maximos` | 50 | `[PROPUESTO]` (la ficha pide ≥ 20) |
| REG-HMM-001 | `obs_maximas` | 520 | `[PROPUESTO]`: H5 (120 meses) en semanas, 10 años semanales |
| REG-HMM-001 | `variables_maximas` | 5 | el tope multivariante de FX-COINT-001 (5 series) |
| FX-COINT-001 | `obs_maximas` | 2 520 | H5 en sesiones (series ya tenía 5) |
| FX-COINT-001 | `rezagos_maximos` (max_rezagos declarado) | 24 | `[PROPUESTO]`: dos años de rezagos mensuales; la regla de ACC-FACT-001 da 8 con 2 520 observaciones |
| BIB-MET-001 | `fichas_maximas` (también la referencia) | 20 000 | `[PROPUESTO]`: por encima de F7–F9 (almacenes de 7 000–11 000 líneas) |
| BIB-MET-001 | `periodos_maximos` | 1 200 | `[PROPUESTO]`: 100 años mensuales; el mensaje pide otra granularidad |
| BIB-MET-001 | `tematicas_maximas` (datos y `categorias`) | 100 | `[PROPUESTO]`: el sistema usa TM-01 a TM-18 |
| TEM-DIFF-001 | `B_maximo` | 10 000 | ML-CAL-001: «B (2 000; 1 000–10 000)», el bootstrap del Catálogo |
| TEM-DIFF-001 | `arranques_maximos` | 200 | la misma regla que FIR-CURVE-001 (10 × los 20 de la ficha), `[PROPUESTO]` allí |
| TEM-DIFF-001 | `obs_maximas` (y puntos de previsión) | 360 | `[PROPUESTO]`: 30 años (límite de H5, el mismo del horizonte) en meses, «anuales o equivalentes» |
| TEM-DIFF-001 | `escenarios_maximos` (lista de m) | 10 | `[PROPUESTO]` |
| FX-REGIME, REG-HMM, TEM-DIFF | semilla | 2⁶³ − 1 | dominio técnico, el mismo de `fichas_riesgo.py` |

**El caso más caro con las cotas máximas** (tiempo de una llamada al manejador; el Motor hace dos pasadas, así que un
servicio tarda el doble). Medido con los otros tres grupos trabajando a la vez (carga 5–7 en 4 núcleos), así que son cotas
por arriba:

| Ficha y entrada | Tiempo por llamada | Memoria máxima del proceso |
| --- | --- | --- |
| REG-HMM-001: 520 obs., 5 variables, covarianza completa, BIC (2–4 estados), 50 arranques | 110 s | 174 MB |
| FX-REGIME-001: 756 obs., 3 estados | 76 s | 155 MB |
| FX-COINT-001: 5 series × 2 520 obs., max_rezagos 24 | 43 s | — |
| TEM-DIFF-001: 360 obs., auto, 200 arranques, B = 10 000 | 32 s | 160 MB |
| FX-STL-001: 2 520 obs., periodo 52, auto robusto | 15 s | 155 MB |
| FX-BRK-001: 2 520 obs., 5 rupturas, auto | 5 s | 635 MB |
| ST-INF-001: 1 000 contrastes de Welch × 2 520 por muestra, con potencia | 3 s | — |
| BIB-MET-001: 20 000 fichas, 100 temáticas, 1 200 periodos, referencia de 20 000 | 1 s | — |

El peor servicio (REG-HMM-001 al máximo) queda en unos 4 minutos con la máquina cargada. Es mucho más que un caso normal
(los casos de control tardan menos de 3 s), pero termina y la memoria queda por debajo de 1 GB en todas. Si el operador quiere
un tope de tiempo más bajo, la palanca es `arranques_maximos` de REG-HMM-001 (el tiempo crece de forma lineal con él).

### H-08 · Mutantes vivos

- **QS04 (regla de rezagos de Schwert).** `test_fx_coint_rezago_maximo_es_la_regla_de_acc_fact_a_mano`: T = 60 ⇒ 3 y
  T = 300 ⇒ 5, escritos a mano (Schwert daría 10 y 15); además, ningún ADF pasa de ese tope.
- **QS05 (ADF por BIC).** `test_fx_coint_adf_elige_los_rezagos_por_aic_frente_a_una_referencia`: una serie I(1) con un
  término AR en el rezago 3 y un ADF escrito aparte en la prueba (muestra común, AIC y BIC, τ con el rezago elegido). La
  referencia comprueba que el AIC elige 3 y el BIC 0, así que el caso discrimina; la ficha da 3 rezagos y el τ de la
  referencia a 1e-9, con AIC y con max_rezagos 6.
- **QS08 (BH sin monotonía).** `test_st_inf_holm_y_bh_monotonos_con_valores_a_mano`: p = (0,01; 0,04; 0,045; 0,2). En BH,
  m·p₍ⱼ₎/j = 0,04; 0,08; 0,06; 0,2, y el mínimo acumulado da 0,04; 0,06; 0,06; 0,2 (el mutante deja 0,08). En Holm, el
  máximo acumulado da 0,12 donde (m − j + 1)·p₍ⱼ₎ = 0,09. Se prueba con `ajuste_bh`/`ajuste_holm` y por la ficha
  (estadísticos suficientes con el t exacto de cada p-valor), con sus decisiones.

### Fecha de corte (contrato nuevo de `servicio.py`)

`_cerrado` pasa `ent["fecha_corte"]` (ISO o None; si es ilegible, ErrorFicha) y las fichas con datos fechados rechazan un
dato posterior a ella («no conocible»): FX-BRK, FX-STL y FX-REGIME (`fechas` o serie de HT-01), REG-HMM y FX-COINT
(`fechas`, o series de HT-01 alineadas), ST-INF (series de HT-01), BIB-MET (fecha de cada ficha) y TEM-DIFF (`fechas`, o
`anios` frente al año decimal del corte). Con datos hasta el corte el resultado es el mismo que sin corte. Ninguna ficha del
grupo lee `ent["configuracion"]`.

**Decisión `[PROPUESTO]` nueva:** el dato posterior al corte se rechaza, no se recorta. Con `anios` decimales solo se rechaza
lo que cae después del corte: un dato anual «2021» (2021,0) pasa con un corte de mediados de 2021, aunque su cifra se publique
en 2022. Esto se declara aquí y no se intenta resolver.

### Decisiones `[PROPUESTO]` nuevas (para INC-T112-01)

Las cotas marcadas `[PROPUESTO]` en la tabla de arriba. Además:
- el n mínimo de potencia que supera la cota de observaciones se publica como None;
- el horizonte de TEM-DIFF-001 que daría más puntos que la cota se rechaza;
- los datos posteriores a la fecha de corte se rechazan.

### Pruebas

`tests/test_fase2_series.py`: **380 pruebas** (antes 320; 18 de ellas llegan solas por las claves nuevas de `UMBRALES`, en la
prueba de umbrales fijos). Todas en verde, junto con `tests/test_t112_motor.py`: 439 en total, unos 80 s. Las nuevas son:
- una por cota de parámetro: la cota se admite, y cota + 1, 20261110, 10¹² y 1e308 se rechazan en menos de 2 s;
- la semilla;
- los escenarios y las categorías;
- las observaciones (9 casos);
- la serie de HT-01 (3 casos);
- los contrastes, las variables, las series, las fichas, la referencia y las temáticas;
- los periodos de BIB-MET;
- los puntos de previsión;
- el n mínimo acotado.

Las cotas de observaciones se prueban con cota + 1 (rechazo rápido) y con la cota exacta, con datos que la ficha rechaza por
otro motivo (constante, sin aceleración…), lo que prueba que la cota es inclusiva sin pagar el cálculo. Hay también cuatro
pruebas de H-08 (tres funciones) y 13 de la fecha de corte.

`ruff check` (desde la raíz del repositorio, como el gate) y `mypy --ignore-missing-imports` sobre el módulo y las pruebas:
sin hallazgos nuevos.

### Mutantes y entradas hostiles, otra vez sobre copias (scratchpad, `r02_S/`)

- `r01_10_mutantes.py`, parte S (QS01–QS08) sobre una copia de `bloque_a` sin `*.docx`: **mueren los 8 frente a las pruebas**
  (QS01–QS03 también frente a los casos de control). QS04, QS05 y QS08, los vivos de la r01, ahora mueren por las pruebas
  nuevas. QS06 y QS07 siguen vivos frente a los casos de control, pero mueren por las pruebas, como en la r01.
- `r01_06_hostiles.py`, parte S (las 8 fichas del grupo en los bloques 1 a 6; el bloque 4 con B, arranques, periodo,
  max_rezagos y semilla de S, y el coste real de TEM-DIFF-001 con B = 1 000, 10 000 y 10 001): **21/21 con `ulimit -v 6 GB`
  y 21/21 sin él**. Fuzzer: 442 llamadas sin excepciones, ninguna de más de 30 s, ningún no finito. Ningún tamaño sin cota,
  y TEM-DIFF-001 con B = 10 000 tarda 7 s y con 10 001 se rechaza.
- `impl_S_mutantes.py` (los 55 de la r01) sobre copias con `-j 3`: la copia sin mutar pasa sus 380 pruebas. **Se aplican
  los 55** (los cambios de código conservan los textos que mutan, también en el LOESS y en la matriz de costes de FX-BRK) y
  **ninguno vive a la vez frente a los casos de control y las pruebas**. Frente a los casos de control solos viven 31, como
  en la r01: reglas de rechazo, dominio y cifras que los casos de control no ejercitan, y que cazan las pruebas.

**Resultado: ningún mutante vivo y ningún fallo del grupo S** en `r01_10` (parte S), `r01_06` (parte S, con y sin
`ulimit`) ni `impl_S_mutantes.py`. Registros en el scratchpad de la sesión (`r02_S/impl_S.log`, `hostil_ulimit.log` y
`hostil_sin_ulimit.log`).
