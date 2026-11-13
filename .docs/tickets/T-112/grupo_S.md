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
