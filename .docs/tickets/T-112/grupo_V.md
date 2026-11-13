# T-112 · Grupo V · valoración de RV, RF, FX y DER

| Campo | Valor |
| --- | --- |
| Módulo | `bloque_a/11_Ejecutor/bloque_a/motor/fichas_valoracion.py` (exporta `PARAMETROS_POR_DEFECTO`, `UMBRALES`, `ADVERTENCIAS`, `FICHAS`, `CASOS_CONTROL`) |
| Pruebas | `bloque_a/11_Ejecutor/tests/test_fase2_valoracion.py`: **547 pruebas (61 funciones), todas en verde** (≈ 20 s) |
| Mutantes | `.docs/tickets/T-112/revisores/impl_V_mutantes.py`: **34 mutantes, 34 muertos ante los casos de control y 34 ante las pruebas** |
| ruff · mypy | Sin hallazgos en el módulo, las pruebas y el script (`ruff check`, `mypy --ignore-missing-imports`) |
| Fichas | ACC-VAL-001, ACC-ERP-001, ACC-FACT-001, FIR-PRICE-001, FIR-CURVE-001, FIR-CARRY-001, FIR-SPREAD-001, FX-MOM-001, FX-PPA-001 (heredada, §6) y DER-OPT-001 |
| Resultado | **Las 10 superan sus casos de control (38 casos)**. Ninguna tiene una «Verificación» que no se pueda comprobar. Las condiciones están en §3 |

## 1. Convenciones del módulo

- **Datos.** Todo llega en línea en `valores`. FX-MOM-001 acepta además el spot de cada par en `ent["series"][par]`.
- **Unidades.** Tipos, rendimientos, cupones, crecimientos, volatilidades y rentabilidades en **% anual**. Diferenciales en **pb**. Precios de bonos por 100 nominal. Plazos en años. ACC-FACT recibe los rendimientos en % por periodo. FIR-SPREAD recibe la recuperación y la PD en tanto por uno, como la ficha.
- **Umbrales fijos.** `UMBRALES[ficha]` cita su campo de la ficha o va marcado [PROPUESTO]. Una petición que traiga un umbral se rechaza («umbrales fijos»).
- **Parámetros.** Todo parámetro tiene tipo y rango (`_validar_parametros`). Los rangos que dependen de los datos los comprueba el manejador: g_L en [r_f − 1 pp, r_f] y g_terminal en [0, r_f]. Un parámetro que la ficha no declara se rechaza; solo se ignora `clase`, que la añade el servicio.
- **Fallo cerrado.** La envoltura `_cerrado` hace lo mismo que la de `fichas_mon_idx`:
  - traduce cualquier excepción numérica o de tipo a `ErrorFicha`;
  - rechaza cualquier no finito en el resultado.
- **Iteraciones.** Los métodos iterativos tienen tope y rechazan con «CONVERGENCIA» si no convergen: TIR, NSS, r implícita, DCF inverso y volatilidad implícita.
- **Advertencias.** Las «Supuestos y limitaciones» de cada ficha van literales en `resultado["advertencias"]`. Detrás van las que dispara el cálculo (valor terminal > 85 %). No van como limitaciones.
- **Determinismo.** Solo FIR-CURVE-001 usa azar, en los arranques del ajuste. Lleva una semilla explícita en los parámetros.

## 2. Por ficha

Cada ficha indica:
- qué hace;
- qué datos espera;
- qué decisiones de método toma que la ficha no fija;
- sus casos de control.

[P] = [PROPUESTO], para INC-T112-01.

### ACC-VAL-001 · DCF, DCF inverso y múltiplos (MC-09 · DETERMINISTA · tol 1e-8)

**Qué hace.** Calcula, para el agregado:
- el WACC: CAPM con la β de ACC-FACT-001 o 1, y la PRM de ACC-ERP-001 o el 5 %;
- el FCFF del último ejercicio y su proyección a `anios_explicitos`;
- el valor terminal de Gordon, o con ROIC_nuevo: VT = NOPAT·(1 + g)·(1 − g/ROIC)/(WACC − g);
- el EV, el valor del agregado, el peso del valor terminal y la brecha frente a la capitalización;
- el DCF inverso: crecimiento y margen implícitos;
- los múltiplos con su percentil y frente al mercado;
- la matriz de sensibilidad WACC ±1 pp × g ±0,5 pp.

Con `enfoque: FCFE` hace el método (vi): descuenta el flujo al accionista al coste del capital.

**Datos (`valores`).**
- Obligatorios:
  - `moneda`;
  - `ejercicios` (≥ 3; cada uno con ejercicio, fecha_presentacion, moneda, ventas, ebit, amortizaciones, capex y variacion_circulante; opcionales ebitda, fondos_propios y flujo_accionista);
  - `capitalizacion` ({valor, fecha});
  - `deuda_neta`;
  - `rf` ({valor, moneda});
  - `coste_deuda_pct`;
  - `crecimiento_explicito` ({valor, fuente});
  - `tasa_impositiva_legal`, o el parámetro `tasa_impositiva`.
- Opcionales: `beta`, `prm` ({valor, fuente}), `roic_nuevo_pct`, `beneficio_adelantado`, `historia_multiplos` y `multiplos_mercado`.

**Decisiones.**
- [P] **Proyección explícita:** FCFF₀ = EBIT·(1 − t) + amortizaciones − capex − Δcirculante del último ejercicio, creciendo a `crecimiento_explicito`. La ficha no dice cómo se proyecta. Este dato y `coste_deuda_pct` no están en «Entradas mínimas», pero sin ellos no hay DCF.
- [P] **Peso de la deuda:** se usa la deuda neta positiva; con deuda neta ≤ 0 el peso es 0 y se declara.
- [P] **DCF inverso:**
  - el crecimiento implícito se resuelve con Brent sobre 1 + g;
  - el margen implícito del flujo sobre las ventas sale cerrado, porque el EV es lineal en el margen;
  - con ROIC_nuevo no se calcula el margen y se declara.
- [P] **Sensibilidad:** rejilla de 3 × 3 puntos (−, 0, +); son las amplitudes de la ficha. Una celda con g ≥ tasa o g < 0 queda `None`.
- [P] **Múltiplos:**
  - salen de los totales del agregado, que es la media armónica ponderada por capitalización (comprobado en las pruebas);
  - FCF yield = FCFF₀/EV de mercado;
  - EBITDA = EBIT + amortizaciones si no se aporta;
  - el percentil se calcula frente a la historia aportada (≥ 10 años; menos, `None` y limitación).
- [P] Tope de 100 iteraciones en el DCF inverso, el de `scipy.optimize.brentq`.
- De la ficha: el PER no aplica con beneficio ≤ 0 (`None` y limitación). Rechazos: g ≥ tasa, < 3 ejercicios, monedas inconsistentes y flujo base ≤ 0.

**Casos de control (4/4).**
- ΣVP + VT = EV.
- g = 0 y flujo constante ⇒ FCF/WACC; WACC y FCFF₀ recalculados a mano.
- El DCF inverso reproduce el EV de mercado, con un descuento escrito aparte.
- Segunda vía: PER implícito del DCF = valor/beneficio, y la celda central de la sensibilidad = valor base.

### ACC-ERP-001 · Prima de riesgo implícita (MC-09 · ESTADISTICA · tol 1e-6)

**Qué hace.**
- (i) Método de Damodaran: la r que iguala el nivel a 5 años de flujo al accionista creciendo a g₅, más una perpetuidad a g_L. PRM = r − r_f.
- (ii) Versión simple: rendimiento del beneficio adelantado − real a 10 años.
- (iii) ECY = 1/CAPE − real.
- (iv) Percentiles y z frente a ≥ 20 años (mínimo 10).

**Datos.**
- `moneda`, `nivel`, `dividendos_12m` y `recompras_netas_12m`;
- `g5` ({valor, fuente, fecha});
- `rf_nominal_10a` y `rf_real_10a` ({valor, moneda, fuente});
- `beneficio_adelantado`;
- `cape` ({valor, fuente}) o `beneficios_reales_10a` (≥ 10);
- opcional `historia` ({fechas, prm_pp, simple_pp, ecy_pp}).

**Decisiones.**
- [P] Las historias de las medidas se aportan ya calculadas; no se recalculan.
- [P] r se resuelve sobre x = r − g_L > 0: se acota doblando y partiendo por 2 desde 1, y se resuelve con Brent; tope de 100 iteraciones.
- [P] El CAPE es el dato aportado o la media de los 10 últimos beneficios reales.
- De la ficha: rechazo sin r_f (nominal y real) en la moneda del índice. No se ofrece la comparación con el rendimiento nominal: es una advertencia, no una salida.

**Código previo.** `servicio.f_erp` → `operaciones.diferencial_rentabilidades`. Solo daba la versión (ii), sin r implícita, sin ECY, sin ventana de percentil y sin el rechazo por moneda. **Rehecho** en el módulo.

**Casos de control (3/3).**
- g₅ = g_L ⇒ r = y·(1 + g) + g.
- Con g₅ ≠ g_L, la r reproduce el nivel con una suma año a año escrita aparte.
- Versión simple y ECY.

### ACC-FACT-001 · Exposición factorial (MC-09 · ESTADISTICA · tol 1e-8)

**Qué hace.**
- Regresión MCO de los rendimientos en exceso sobre los factores del modelo: FF5 + UMD, FF3 o CAPM, con QMJ y BAB opcionales.
- Errores de Newey-West con L = ⌊4(T/100)^{2/9}⌋.
- α anualizado, R² y contribuciones a la varianza.
- Betas móviles; segunda vía CAPM; referencia ingenua CAPM con β = 1.
- `factores_nuevos_t_mayor_3` aplica el «t > 3» de la ficha.

**Datos.** `fechas` (mensuales consecutivas o semanales cada 7 días), `rendimientos` (%), `rf` o `en_exceso: true`, `factores` y `region`.

**Decisiones.**
- [P] α anualizado con capitalización compuesta, como manda la §3.1: ((1 + α)^12 − 1).
- [P] Contribuciones a la varianza: β_j·Cov(f_j, ajustado)/Var(r) y un residuo. Suman el 100 %.
- [P] Ventana móvil semanal = ⌊36·52/12⌋ = 156 observaciones.
- [P] El estadístico t queda `None`, con su limitación, si el error estándar es 0. Pasa con un ajuste exacto: el caso de la ficha «factor sobre sí mismo».

**Casos de control (4/4).**
- Un factor sobre sí mismo (FF5 + UMD) ⇒ β = 1 y α = 0.
- Segunda vía CAPM: el mercado sobre sí mismo.
- Newey-West con T = 300 (L = 5), con el núcleo de Bartlett escrito aparte con bucles, y α compuesto.
- Contribuciones que suman el 100 % y R² = 1 − residuo.

### FIR-PRICE-001 · Precio, rendimiento, duración y convexidad (MC-09 · DETERMINISTA · tol 1e-10)

**Qué hace.**
- Precio limpio y sucio, cupón corrido, YTM y YTW.
- D_Macaulay, D_mod, DV01 y convexidad.
- Duración y convexidad efectivas por ±Δy.
- Duración real y breakeven si el bono está ligado a inflación.
- Segunda vía: la aproximación por duración y convexidad frente al reprecio exacto.

**Datos.**
- `cupon`, `frecuencia`, `liquidacion` y `vencimiento`;
- `convencion`, en los datos o en los parámetros;
- `precio_limpio` o `rendimiento`;
- opcionales: `rescates` [{fecha de cupón, precio}], `ligado_inflacion` y `rendimiento_nominal_comparable` ({valor, fuente}).

**Decisiones.**
- [P] **Lo modelable:**
  - convenciones ACT/ACT-ICMA y 30E/360;
  - frecuencias 1, 2, 4 y 12;
  - solo bonos «bullet» (tipo fijo y amortización única);
  - rescates solo en fechas de cupón.
  
  Todo lo demás se rechaza como «flujos no modelables en ficha».
- [P] **Calendario:** se construye hacia atrás desde el vencimiento, sin ajuste de días hábiles. El precio es el de la convención de mercado, Σ CF/(1 + y/f)^{w + k − 1}.
- [P] **TIR:** Newton sobre v = 1/(1 + y/f), arrancando en el cupón, con respaldo de Brent. Como el precio es monótono en v, la raíz es única. Tope de 100 iteraciones; convergencia cuando |ΔP| ≤ 1e-10·P, la tolerancia de la ficha.
- [P] **Duración y convexidad efectivas con rescates:** por «precio al peor», el mínimo de los escenarios a YTW ± Δy. No hay modelo de opción ni se usa la curva. Se declara como limitación.
- El breakeven es nominal − real, la definición de TCV-BEI-001 (i).

**Casos de control (6/6).**
- Cupón = rendimiento ⇒ 100.
- 10 años al 5 % ⇒ D_mac 8,1078 y D_mod 7,7217.
- Ida y vuelta precio → rendimiento → precio por la vía pública.
- Fuera de fecha de cupón, en ACT/ACT ICMA y en 30E/360 con el día 31: corrido = C/f·A/E y precio = (C/f + P siguiente)·v^(1 − A/E).
- Segunda vía: reprecio exacto ±Δy, órdenes 1 y 2, y convexidad = segunda derivada numérica.

### FIR-CURVE-001 · Curva NSS y valor relativo (MC-09 · ESTADISTICA · tol 1e-6)

**Qué hace.**
- Ajuste NS (< 8 nodos) o NSS (≥ 8 nodos) por mínimos cuadrados, con β₀ ≥ 0 y λ > 0 (por ln λ); se rechaza si β₀ sale ≤ 0.
- ≥ 20 arranques con semilla; λ fijo de Diebold-Li opcional, solo con NS.
- RMSE, residuos y su z frente a la historia.
- Pendientes 2s10s y 3m10y, con su percentil.
- Curva cero y forward.
- Segunda vía: interpolación lineal de los nodos.

**Datos.**
- `curva` ({fecha, plazos > 0 y crecientes, rendimientos cupón cero en %});
- opcional `historia` ({fechas, rendimientos[[…]]}) con los mismos plazos.

**Decisiones.**
- [P] La semilla por defecto es 0.
- [P] Hasta 200 arranques (10 × el valor por defecto).
- [P] Tope de 100 evaluaciones por parámetro, el de `scipy.optimize.least_squares`.
- [P] **Arranques:** λ log-uniformes entre el plazo mínimo y el máximo, y β por MCO dado λ.
- [P] **Ajuste en rendimientos sin ponderar.** La ficha admite «rendimientos o precios ponderados»; las entradas se toman como cupón cero.
- [P] **Historia:** cada fecha se ajusta arrancando en la solución de la anterior (un solo arranque).
- [P] **Pendientes:** una pendiente fuera del rango de nodos no se extrapola: `None` y limitación.
- [P] **Segunda vía:** la diferencia NSS − lineal en los puntos medios entre nodos.
- El λ de Diebold-Li = 1/(0,0609·12) años, de Diebold y Li (2006), que la ficha cita.

**Coherencia con TCV-SLOPE-001.**
- β en %, así que y(∞) − y(0) = −β₁.
- Probado: −β₁ de FIR-CURVE alimenta la segunda vía de TCV-SLOPE y da la misma pendiente en pb.

**Casos de control (3/3).** Los datos se generan con una NSS escrita aparte con `math`, no con las cargas del módulo.
- Recupera los parámetros (tol 1e-6) con RMSE < 1e-4 pb.
- τ → ∞ ⇒ β₀ y τ → 0 ⇒ β₀ + β₁, y el forward de la serie es d(τ·y)/dτ, derivado a mano.
- Diebold-Li recupera los β por MCO.

**Coste.** ≈ 1,5 s por llamada con 20 arranques y 11 nodos.

### FIR-CARRY-001 · Carry y rolldown (MC-09 · DETERMINISTA · tol 1e-10)

**Qué hace.**
- carry = (y − financiación)·Δt;
- rolldown = −D_mod·[y(τ − Δt) − y(τ)];
- el total;
- la subida de equilibrio = total/D_mod (pb);
- carry/volatilidad;
- segunda vía: el reprecio completo del cupón cero a t + Δt con la curva inalterada.

**Datos.**
- La curva: `curva` (nodos en %, interpolación lineal sin extrapolar) o `nss` (parámetros de FIR-CURVE-001 con fuente);
- `tramo` (o una lista);
- `financiacion` (%);
- opcional `volatilidad_rendimiento_pb`.

**Decisiones.**
- D_mod = τ/(1 + y) del nodo cupón cero. Es la misma fórmula y el mismo rango de Δt (1–12 meses) que `fichas_tcv._carry_tramo` y `UMBRALES["TCV-SLOPE-001"]`. Probado: coincide con `_carry_tramo` con tolerancia 1e-14.
- [P] carry/volatilidad = total/(D_mod·σ_y·√Δt): la rentabilidad esperada entre su volatilidad en el horizonte.
- Rechazos: aclaración sin financiación; un tramo que vence antes de Δt.

**Casos de control (3/3).**
- Curva plana ⇒ rolldown 0, y carry = (y − f)·Δt.
- Curva con pendiente: el rolldown y la subida de equilibrio a mano.
- Segunda vía con curva plana: (1 + y)^Δt − 1 − f·Δt.

### FIR-SPREAD-001 · Percentil y valor del diferencial de crédito (MC-09 · ESTADISTICA · tol 1e-8)

**Qué hace.**
- Percentil (proporción ≤) y z del diferencial actual frente a la ventana.
- Pérdida esperada PD·(1 − R) y el exceso sobre ella.
- Ampliación de equilibrio s/duración.
- Ajuste opcional por composición.

**Datos.**
- `historia` ({fechas, diferenciales_pb, duraciones opcionales});
- `impagos` ({fuente, pd_anual} o {fuente, por_rating: {r: {pd_anual, peso}}});
- opcionales: `duracion_diferencial`, `medida` (OAS o Z-spread) e `incluye_recesion`.

**Decisiones.**
- [P] **Ajuste de composición:** solo por duración, con los diferenciales reescalados a la duración actual, s_t·D_hoy/D_t. El rating no se ajusta y se declara.
- [P] La PD por rating es la media ponderada; los pesos deben sumar 1 (tol 1e-8 de la ficha).
- [P] Aviso si la frecuencia es menor que semanal (mediana > 7 días).
- Umbrales de la ficha:
  - rechazo con < 5 años;
  - limitación con < 10 años y con < 15 recomendados;
  - limitación si no consta una recesión.

**Casos de control (2/2).**
- El percentil del máximo histórico = 1.
- Exceso = s − PD·(1 − R) y ampliación = s/D.

### FX-MOM-001 · Momentum cambiario y carry ajustado por volatilidad (MC-09 · ESTADISTICA · tol 1e-10)

**Qué hace.**
- Rendimiento en exceso a 1, 3 y 12 meses: variación del spot + carry devengado.
- TSMOM, el signo a 12 meses, como en ACC-MOM-001.
- Rango transversal en el universo (percentil y z).
- carry/volatilidad = diferencial/volatilidad implícita a 3 meses, o la realizada si no hay implícita.

**Datos.** `pares` = {par: {direccion «BASE/COT», spot (o `ent["series"][par]`), diferencial_pct {fechas, valores} o forward {fechas, valores, plazo_dias}, vol_implicita_3m opcional}} y `universo` opcional.

**Decisiones.**
- Identidad aditiva de FX-CARRY-001: total = variación cambiaria + carry·años.
- [P] **Carry:** se devenga tramo a tramo con el diferencial conocido al inicio de cada tramo, en Real/365. Así no mira adelante (conocibilidad, §3.1).
- [P] **Meses de calendario:** la última observación ≤ t − h meses.
- [P] **Volatilidad realizada:** los últimos 3 meses de rendimientos logarítmicos diarios × √252.
- [P] **Carry con forwards:** (S/F − 1)/τ, el carry exacto de la posición a plazo.
- [P] **Rango transversal:** con ≥ 2 pares.
- De la ficha: rechazo sin dirección del par declarada; rechazo con < 2 años.

**Código previo.** `servicio.f_fx_mom` → `operaciones.momentum_12_1` + `carry_ajustado_vol`. Tenía estas carencias frente a la ficha:
- el rendimiento era solo del spot, sin carry;
- los meses eran de 21 sesiones;
- no exigía la dirección del par;
- no calculaba el rango transversal;
- la volatilidad era siempre la realizada a un año.

**Rehecho.** Cambia la interfaz: ahora hacen falta `valores["pares"]` con la dirección y la historia del diferencial; el spot puede seguir llegando por HT-01.

**Casos de control (3/3).**
- Coherencia con FX-CARRY-001 (`operaciones.carry_divisas`).
- Carry con un diferencial escalonado, sin mirar adelante, con un bucle escrito aparte.
- TSMOM = signo, y el mayor exceso tiene percentil 1.

### FX-PPA-001 · Desviación de la PPA relativa (heredada · MC-03 · v1.1 · ESTADISTICA · tol 1e-8)

**Qué hace.**
- Senda PPA = S₀·(P_cot/P_cot,₀)/(P_base/P_base,₀).
- Desviación = ln S − ln senda (%).
- q = s + p_base − p_cot.
- Base de anclaje: el primer periodo o la media de largo plazo.
- Suavizado opcional.
- Vida media por AR(1) con ≥ 20 años.
- Inflaciones acumuladas.

**Datos.** `par`, `fechas`, `tipo_cambio` e `indices` {base, cotizada}, cada uno con valores, base_indice, vintage, canasta y periodicidad.

**Decisiones.**
- [P] Periodicidades mensual y trimestral.
- [P] AR(1) con constante por MCO sobre q.
- [P] El suavizado es una media móvil de k periodos.
- [P] La ventana va en meses.
- [P] Con φ ∉ (0, 1) la vida media queda `None` y se declara.
- De la ficha: rechazo con canastas o periodicidades incompatibles (también si las fechas no siguen la periodicidad declarada) y con < 24 meses.

**Casos de control (4/4).**
- Inflación igual y cambio constante ⇒ 0.
- Cambio sobre la PPA con inflaciones distintas ⇒ 0.
- Un 10 % sobre la senda ⇒ 100·ln 1,1.
- AR(1) exacto ⇒ vida media = ln 0,5/ln φ.

### DER-OPT-001 · Opciones: BSM, Black-76, CRR, griegas y volatilidad implícita (MC-09 · DETERMINISTA · tol 1e-8)

**Qué hace.**
- Precio y griegas:
  - Δ;
  - Γ;
  - vega por punto;
  - θ por día (/365);
  - ρ por punto, que en Black-76 es −T·C.
- Volatilidad implícita (Newton con respaldo de Brent).
- Paridad put-call y segunda vía CRR frente a BSM en europeas; prima de ejercicio anticipado en americanas.
- Superficie:
  - volatilidad ATM;
  - risk reversal y butterfly 25Δ;
  - estructura temporal ATM;
  - densidad de Breeden-Litzenberger opcional.

**Datos.**
- `contratos` [{S, K, T, r %, q %, tipo, estilo, precio o sigma %, subyacente «futuro» opcional}];
- opcional `superficie` {vencimientos: [{T, forward, r, strikes ≥ 5, vol_pct}]}.

**Decisiones.**
- [P] Las americanas se valoran siempre con CRR (promedio de N y N + 1), y se declara.
- [P] **Griegas del árbol:** Δ, Γ y θ salen del propio árbol; vega y ρ por ±1 punto, la unidad de la salida.
- [P] Pasos en el rango 2–5000: Γ del árbol necesita 2 pasos, y 5000 es el tope de coste.
- tol_iv ≤ 1e-6, de §3.2.
- [P] **Volatilidad implícita:** Newton con el arranque de Brenner y Subrahmanyam (1988); respaldo de Brent acotado doblando; tope de 100 iteraciones.
- [P] **Superficie:**
  - delta forward sin prima para 25Δ;
  - ATM por interpolación lineal en el strike en K = F;
  - RR = σ25c − σ25p y BF = (σ25c + σ25p)/2 − σATM.
- [P] **Cotas de no arbitraje estrictas:** un precio en la cota se rechaza, porque su volatilidad implícita no está definida.
- De la ficha: rechazo si el precio viola las cotas o si el payoff no está en la ficha (tipo ≠ call/put, o estilo ≠ europea/americana).

**Casos de control (6/6).**
- S = K = 100, r = 5 %, σ = 20 %, T = 1 ⇒ 10,4506 y 5,5735.
- Paridad con dividendo.
- Griegas = derivadas centrales del precio, con sus unidades.
- CRR frente a BSM, con error ≤ precio/N.
- Volatilidad implícita ida y vuelta.
- Americanas: la put es mayor que la europea; la call sin dividendo es igual a la europea.

## 3. Qué promover y qué no

**Las 10 superan sus casos de control**, en el módulo y por el Motor. `Motor.verificar_casos_control` las pasa con las fichas registradas por monkeypatch y deja una entrada CASOS_CONTROL por ficha en RC (`test_los_casos_de_control_pasan_por_el_motor_y_quedan_en_rc`). Ninguna tiene una «Verificación» que no se pueda comprobar.

Condiciones para la integración:

- **ACC-VAL-001.** Promover **solo si el operador acepta, en INC-T112-01:**
  - el modelo de proyección: FCFF₀ del último ejercicio creciendo a una tasa aportada con fuente;
  - los dos datos que la ficha no lista: `coste_deuda_pct` y `crecimiento_explicito`.
  
  Si no se acepta, se queda en DOCUMENTADO con código: la «Verificación» se cumple, pero el método de proyección es una decisión propia.
- **FIR-PRICE-001.** Las efectivas con rescates son por «precio al peor», sin modelo de opción. La ficha pide ±Δy (se hace), pero cita «curva para efectiva». Es promovible con la limitación declarada. Si se quiere OAS, es otra ficha.
- **ACC-ERP-001 y FX-MOM-001.** Al promoverlas salen de `DOCUMENTADAS_CON_CODIGO`:
  - sus entradas de `IMPLEMENTADAS` en `servicio.py` las sustituye este módulo; el bucle de integración las sobrescribe;
  - `servicio.f_erp` y `f_fx_mom` quedan sin uso;
  - FX-MOM cambia de interfaz;
  - `tests/test_t65_resto_t53.py` y `tests/test_t92_revision.py` comprueban hoy que no se sirven y habrá que actualizarlos;
  - REI-CAP-001 es del grupo P.
- **`ALTERNATIVAS` de `servicio.py`:** ACC-VAL → ACC-ERP, FIR-SPREAD → ST-DESC y FIR-CARRY → FX-CARRY dejan de usarse cuando las tres se sirvan.

## 4. Pruebas y mutantes

**Pruebas: 547.**

| Ficha | Pruebas |
| --- | --- |
| ACC-VAL | 76 |
| DER-OPT | 63 |
| FIR-PRICE | 60 |
| ACC-FACT | 59 |
| ACC-ERP | 53 |
| FIR-CURVE | 53 |
| FX-PPA | 48 |
| FX-MOM | 46 |
| FIR-CARRY | 44 |
| FIR-SPREAD | 40 |
| Comunes | 5 |

Qué cubren:
- **Casos de control.** Pasan y **pueden fallar**: cada caso se comprueba también con su resultado perturbado de forma no uniforme, y debe fallar.
- **Umbrales.** Cada umbral de `UMBRALES` en la petición se rechaza.
- **Parámetros.** Un parámetro no declarado se rechaza. Hay 54 casos de dominio malo y 16 de dominio bueno.
- **Determinismo.** Dos pasadas; también NSS con semilla.
- **Entradas hostiles:**
  - `ent`, `valores`, `series` o parámetros que no son objetos;
  - NaN, ±inf, texto, None, bool, listas y dicts en un número de cada ficha;
  - vacíos.
- **Rechazos.** Los de «Aclaración y rechazo» y los de «Entradas mínimas», ficha a ficha.
- **Envoltura.** Rechaza los no finitos y traduce las excepciones.
- **Advertencias.** Van en el resultado, no en las limitaciones.
- **Oráculos independientes, al menos uno por ficha:**
  - FIR-PRICE: la anualidad y la D_mac cerradas; la TIR con Brent sobre un precio escrito en la prueba; 30E/360 a mano.
  - FIR-CURVE: NSS escrita a mano, el forward por diferencias, `curve_fit` y Diebold-Li por `lstsq`.
  - FIR-CARRY: `fichas_tcv._carry_tramo` y la fórmula a mano con NSS.
  - FIR-SPREAD: pandas.
  - FX-MOM: pandas con `reindex(ffill)`.
  - FX-PPA: `polyfit`.
  - ACC-ERP: Brent aparte.
  - ACC-FACT: Newey-West con bucles.
  - ACC-VAL: DCF a mano y la media armónica.
  - DER-OPT: BSM con `math.erf`, las griegas por diferencias y un CRR con bucles.
- **Coherencia con TCV-SLOPE-001:** el carry y −β₁.
- **Integración con el Motor**, sin tocar `servicio.py`.

**Mutantes (`impl_V_mutantes.py`).** El script copia `bloque_a` sin los `.docx` a un directorio temporal del scratchpad y lo borra al terminar. Antes de mutar, comprueba que se importa la copia y que la copia sin mutar pasa. Luego aplica cada mutante y corre:
- **CC:** los casos de control de la ficha, en dos pasadas;
- **T:** el fichero de pruebas, sin la prueba de integración, que depende de `servicio.py`, en obras.

Hay 34 mutantes, entre 2 y 5 por ficha. Cada uno rompe una fórmula principal: periodo fraccionario, D_mod, convexidad, recuento ACT/ACT y 30E/360, cargas y forward NSS, λ de Diebold-Li, signo y D_mod del rolldown, Δt, (1 − R), percentil ≤, carry que mira adelante, spot logarítmico, base 360, tipo real cruzado, vida media en meses, Gordon sin (1 + g), PRM frente al real, Bartlett, regla de rezagos, α aritmético, descuento desplazado, escudo fiscal, signo del circulante, put con N(−d1), d1 sin q, unidades de vega y θ, y CRR sin q.

**Resultado final: 34/34 muertos ante CC y 34/34 ante T.**

En la primera pasada, dos mutantes sobrevivieron a todo:
- V05: 30E/360 sin el tope del día 31;
- V23: la regla de rezagos con exponente 1/9 (con T = 72 da el mismo L).

Otros once solo morían ante T: V01, V03, V04, V06, V08, V15, V22, V24, V31, V32 y V34. Había, entre otras, curvas de control generadas con la propia fórmula del módulo.

Se reforzaron los casos de control:
- dos casos fuera de fecha de cupón;
- convexidad numérica;
- NSS escrita aparte y forward;
- diferencial escalonado;
- Newey-West con T = 300;
- griegas por diferencias.

Y dos pruebas: la regla de rezagos con varios T, y 30E/360 con el día 31.

Uso:

```bash
.venv/bin/python -I -B .docs/tickets/T-112/revisores/impl_V_mutantes.py --destino <scratchpad> [--solo FICHA]
```
