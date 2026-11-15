# T-128 · Análisis técnico

## Causa raíz o motivo

El Catálogo V5.0 (1.6, «Frontera con el Bloque B») dice que los datos de instrumentos individuales (valores, emisiones,
fondos, contratos, tokens) «solo entran como componentes de un agregado o como representación genérica de un tramo» y que
«ninguna ficha compara, ordena ni selecciona instrumentos concretos, ni sus costes, comisiones o plataformas». Las fichas de
T-106 y T-112 se escribieron antes de que T-119 y T-127 fijaran la regla para las P2, y varias entregaban una fila por
componente con su identificador (o lo citaban en una limitación), o el mínimo y el máximo de muy pocos componentes.

## Evidencia

- Barrido de las 66 fichas con casos de control: `.venv/bin/python -I .docs/tickets/T-128/revisores/impl_barrido_identificadores.py bloque_a/11_Ejecutor`.
  Ejecuta cada caso como `verificar_casos_control` y busca en el resultado y en las limitaciones los identificadores de
  los datos (claves `id`, `ticker`, `emisor`…, o las claves de un objeto de objetos, como `miembros`) y las filas por algo
  (listas de objetos, objetos con identificadores por clave). Antes: REI-NAV-001 `.componentes{id}`, REI-FFO-001
  `.cobertura_por_componente{id}`, IDX-REB-001 `.por_componente{id}`, CHR-FUND-001 `.financiacion_por_plataforma…{id}` y
  `.pesos{id}`, más 28 candidatas que son series temporales, curvas, rejillas, categorías o regímenes (leídas una a una,
  abajo). Después: ninguna de las cuatro; CHR-FUND-001 conserva los nombres de las plataformas como fuentes, sin cifra.
- Lectura del código de las 14 fichas del ejecutor V1.0 (`motor/servicio.py`, sin casos de control) y de las que reciben
  listas u objetos de componentes (`grep` de `componentes`, `miembros`, `plataformas`, `tokens` en `motor/fichas_*.py`):
  además, FON-DISC-001 (subcategorías, mínimo y máximo de 5 miembros, el miembro en una limitación) y FON-TD-001 (segmentos
  de un vehículo).
- Del Catálogo se ha leído solo la ficha que tocaba, por su identificador (el «Propósito» de las 81 y, de las candidatas,
  «Método», «Salidas» y «Supuestos»).

## Tabla de las 80 fichas con manejador (CA-1)

«Componentes» dice qué entra por instrumento; «Decisión»: **cambia** (y qué) o **no cambia** (y por qué), con lo que dice
la ficha del Catálogo.

| Ficha | Módulo | Componentes en la entrada | Decisión y motivo |
| --- | --- | --- | --- |
| ST-DESC-001 | servicio | no: series del universo (ámbitos de HT-01) | no cambia: una tabla por serie de ámbito |
| FIN-CAGR-001 | servicio | no: series del universo | no cambia: ídem |
| ACC-MOM-001 | servicio | no: series del universo | no cambia: el rango transversal es entre ámbitos del universo (sectores, índices), no entre valores |
| FX-VOL-001 | servicio | no: series del universo | no cambia |
| VOL-GARCH-001 | servicio | no: series del universo | no cambia |
| FX-TREND-001 | servicio | no: series del universo | no cambia |
| RISK-DD-001 | servicio | no: el indicador del ámbito | no cambia («del indicador de seguimiento del ámbito») |
| FX-CORR-001 | servicio | no: dos series del universo | no cambia |
| ML-CLUS-001 | servicio | no: opciones del Buscador (ámbitos) | no cambia (agrupa opciones, regla 9.6.3) |
| FX-CARRY-001 | servicio | no: un par | no cambia (un par es un ámbito) |
| CMD-CURVE-001 | servicio | futuros próximo y siguiente | no cambia: contratos genéricos de la curva (tramo, 1.6) |
| FC-EVAL-001 | servicio | no: pronósticos del sistema | no cambia |
| FC-CAL-001 | servicio | no: pronósticos del sistema | no cambia |
| SCORE-RK-001 | servicio | no: dimensiones de una opción | no cambia (HT-03 de una opción del Buscador) |
| IDX-CONC-001 | fichas_mon_idx | pesos de los componentes del índice | no cambia: entrega el peso y la contribución de los n mayores, HHI y amplitud, sin identificar a ninguno; es lo que su ficha mide (la concentración del índice). **Cambia en la r02 (H-02, «otra igual»):** la amplitud con los precios de un solo componente y la contribución de un índice de uno (o que aporta casi entera uno, `FRONTERA_B`) eran las de ese componente: `null` con su limitación (`IDX_CONC_COMPONENTES_MINIMOS = 2`) |
| IDX-ERP-001 | fichas_mon_idx | no: un índice | no cambia |
| IDX-REL-001 | fichas_mon_idx | no: dos índices | no cambia |
| IDX-REB-001 | fichas_mon_idx | cambios de peso por valor (`id`) | **cambia**: sin `por_componente`; la demanda de una cesta que aporta casi entera un valor (o la de un solo valor) va a `null` («la salida describe la cesta del evento, nunca selecciona valores afectados») |
| MON-EXP-001 | fichas_mon_idx | no: futuros y reuniones | no cambia |
| MON-FIX-001 | fichas_mon_idx | no: tipos por plazo | no cambia |
| MON-REAL-001 | fichas_mon_idx | no: divisas y plazos | no cambia |
| MON-YLD-001 | fichas_mon_idx | segmentos de liquidez | no cambia: los segmentos (letras, pagarés, repos…) son ámbitos |
| DER-ROLL-001 | fichas_fon_der | futuros genéricos | no cambia (tramo genérico) |
| DER-SKEW-001 | fichas_fon_der | superficie de un subyacente | no cambia |
| DER-TERM-001 | fichas_fon_der | vencimientos estándar | no cambia |
| DER-VRP-001 | fichas_fon_der | un subyacente | no cambia |
| FON-DISC-001 | fichas_fon_der | miembros de la categoría (por nombre) | **cambia**: subcategorías con < 5 miembros sin descuento; mínimo, máximo y rango con 7 o más; la limitación del NAV antiguo sin el miembro |
| FON-FLOW-001 | fichas_fon_der | categorías de vehículos | no cambia: filas por categoría (ámbitos) |
| FON-LEV-001 | fichas_fon_der | no: una estructura genérica L | no cambia |
| FON-TD-001 | fichas_fon_der | miembros de la categoría | **cambia**: segmentos con < 5 miembros sin TD («nunca un ranking de vehículos») |
| TCV-BEI-001 | fichas_tcv | no: curvas | no cambia |
| TCV-CDS-001 | fichas_tcv | no: un índice de CDS | no cambia |
| TCV-SLOPE-001 | fichas_tcv | no: tramos de la curva | no cambia |
| TCV-TP-001 | fichas_tcv | no: curva y encuestas | no cambia |
| TCV-VIXTS-001 | fichas_tcv | futuros de índices de volatilidad | no cambia: puntos de la curva (tramo genérico) |
| BIB-MET-001 | fichas_series | registros de F7–F9 | no cambia: identificadores de referencias bibliográficas, no instrumentos |
| FX-BRK-001 | fichas_series | no: una serie | no cambia |
| FX-COINT-001 | fichas_series | no: series | no cambia |
| FX-REGIME-001 | fichas_series | no: una serie | no cambia |
| FX-STL-001 | fichas_series | no: una serie | no cambia |
| REG-HMM-001 | fichas_series | no: variables del tipo de activo | no cambia |
| ST-INF-001 | fichas_series | muestras con nombre | no cambia: los nombres los pone quien pide; si las muestras son de instrumentos concretos, 1.6 manda rechazar la petición por su propósito (declarado en INC-T128-01) |
| TEM-DIFF-001 | fichas_series | no: una temática | no cambia |
| BT-DSR-001 | fichas_riesgo | no: una señal o estrategia | no cambia |
| BT-PBO-001 | fichas_riesgo | no: configuraciones | no cambia |
| BT-VAR-001 | fichas_riesgo | no: excedencias | no cambia |
| DEC-VOI-001 | fichas_riesgo | no: decisiones | no cambia |
| ML-CAL-001 | fichas_riesgo | no: un modelo | no cambia |
| ML-PRED-001 | fichas_riesgo | no: una serie | no cambia |
| RISK-VAR-001 | fichas_riesgo | no: una serie | no cambia |
| SCN-H-001 | fichas_riesgo | no: el indicador del ámbito | no cambia (filas por horizonte y régimen) |
| SIM-MC-001 | fichas_riesgo | no: una dinámica | no cambia |
| ACC-ERP-001 | fichas_valoracion | no: un índice | no cambia |
| ACC-FACT-001 | fichas_valoracion | no: el indicador del ámbito | no cambia |
| ACC-VAL-001 | fichas_valoracion | no: datos del agregado | no cambia (entra el agregado, no sus componentes) |
| DER-OPT-001 | fichas_valoracion | contratos | no cambia: «contratos genéricos del subyacente (ATM, deltas estándar)»; el propósito lo juzga quien pide (declarado) |
| FIR-CARRY-001 | fichas_valoracion | no: un tramo | no cambia |
| FIR-CURVE-001 | fichas_valoracion | nodos de la curva | no cambia: residuos por plazo (tramo genérico); su ficha pide «residuos (pb) y z-scores» |
| FIR-PRICE-001 | fichas_valoracion | no: bono genérico de un tramo | no cambia |
| FIR-SPREAD-001 | fichas_valoracion | no: el diferencial de un índice | no cambia |
| FX-MOM-001 | fichas_valoracion | pares | no cambia: filas por par (ámbitos) |
| FX-PPA-001 | fichas_valoracion | no: un par | no cambia |
| ALT-DESMOOTH-001 | fichas_reales | no: una serie suavizada | no cambia |
| CHR-FLOW-001 | fichas_reales | ofertas de *stablecoins*; flujos del agregado de ETF | no cambia: entrega la oferta agregada, sin cifra por moneda. **Cambia en la r02 (H-02):** con una moneda era la suya; ahora 2 monedas distintas por su crecimiento y ninguna de más del 95 % de la oferta (rechazo), y el crecimiento que aporta casi entero una, `null`. Los flujos de ETF llegan ya agregados (H-03, declarado) |
| CHR-FUND-001 | fichas_reales | plataformas (por nombre) | **cambia**: sin la financiación ni el peso de cada plataforma (1.6 prohíbe comparar plataformas); los nombres quedan como fuentes |
| CMD-INV-001 | fichas_reales | no: inventarios | no cambia |
| CMD-RETDEC-001 | fichas_reales | calendario de contratos | no cambia: contratos genéricos del roll (tramo) |
| REI-CAP-001 | fichas_reales | no: el subsector agregado | no cambia |
| REI-FFO-001 | fichas_reales | sociedades (`id`) | **cambia**: sin `cobertura_por_componente` ni el id en la limitación; mínimo de 2; la cobertura en mediana, IQR, mínimo y máximo con 7 distintos; reglas de `frontera_b` |
| REI-NAV-001 | fichas_reales | sociedades (`id`) | **cambia**: sin `componentes`; `rango_pct` con 7 distintos; `dispersion_pct` con 3; reglas de `frontera_b`; el id fuera de la limitación |
| ALT-AUC-001 | fichas_p2 | transacciones | no cambia: el índice y la dispersión de rentabilidades individuales con ≥ 200 pares y ≥ 500 transacciones (lo pide su ficha), sin identificar piezas |
| ALT-HF-001 | fichas_p2 | no: índice de la estrategia | no cambia |
| CHR-ONCHAIN-001 | fichas_p2 | no: la red | no cambia |
| CHR-TOKEN-001 | fichas_p2 | tokens | ya en T-127 (y ronda r02) |
| CMD-REAL-001 | fichas_p2 | no: un precio y su curva de costes | no cambia |
| FIR-CRED-001 | fichas_p2 | emisores | ya en T-127 (y ronda r02) |
| FX-BEER-001 | fichas_p2 | no: fundamentales | no cambia |
| PRV-CF-001 | fichas_p2 | no: flujos agregados | no cambia («flujos agregados; los fondos individuales solo como componentes»); podrían ser de un solo fondo (H-03 de la r02, declarado) |
| PRV-PME-001 | fichas_p2 | no: flujos agregados | no cambia; podrían ser de un solo fondo (H-03 de la r02, declarado) |
| REI-LEV-001 | fichas_p2 | sociedades | ya en T-127 (y ronda r02) |

Cuentas (r01): **6 fichas cambian** (REI-NAV-001, REI-FFO-001, IDX-REB-001, CHR-FUND-001, FON-DISC-001 y FON-TD-001), 3 ya
seguían la regla desde T-127 y 71 no cambian. AUD-REX-001 (la 81 del Catálogo) no es un manejador del CT-09. En la r02 cambian además CHR-FLOW-001 e IDX-CONC-001 (8 en total, 69 sin cambios).

## Implementación

- Archivos cambiados y por qué:
  - `bloque_a/11_Ejecutor/bloque_a/motor/frontera_b.py` (nuevo): las reglas de T-127 (`FRONTERA_B` y sus funciones),
    sacadas de `fichas_p2.py` sin cambiarlas para compartirlas entre módulos; `fichas_p2.py` las importa con los mismos
    nombres (las pruebas y los scripts que usan `fichas_p2.FRONTERA_B` o `fichas_p2._sin_dominio` siguen valiendo).
  - `motor/fichas_reales.py`: REI-NAV-001, REI-FFO-001 y CHR-FUND-001 (y sus casos de control); `UMBRALES` de REI-NAV-001
    (`componentes_minimos_dispersion: 3` y `FRONTERA_B`) y de REI-FFO-001 (`componentes_minimos: 2` y `FRONTERA_B`).
  - `motor/fichas_mon_idx.py`: IDX-REB-001 y `_evento_reb` (dos valores por cesta).
  - `motor/fichas_fon_der.py`: FON-DISC-001 y FON-TD-001, y dos casos de control de FON-DISC-001.
- Decisiones (INC-T128-01, `[PROPUESTO]`):
  - Quitar las filas por componente (no basta con quitar el identificador: la fila se reconoce por sus datos).
  - REI-NAV-001: la dispersión es una desviación típica, no un estadístico de orden; con la prima agregada y los pesos son
    dos ecuaciones que con 2 sociedades dan las dos primas: hace falta 1 más (3). El rango sí es de orden: 7.
  - REI-FFO-001: un mínimo de 2, el de REI-NAV-001; las reglas de copias, dominancia y aportación de T-127 r02, porque sus
    cifras son cocientes de sumas de sociedades, como REI-LEV-001.
  - IDX-REB-001: `null` y no el rechazo (el estudio de eventos de la cesta sigue valiendo). Con un solo valor por cesta, su
    demanda no se entrega: es el caso de un cambio de composición con una inclusión.
  - CHR-FUND-001: una plataforma no es un instrumento; no se exige mínimo ni dominancia, solo no compararlas.
  - FON-DISC-001 y FON-TD-001: subconjuntos con el mínimo de la ficha (5), y el mínimo y el máximo con 7. No se les aplica
    la regla de copias (su agregado es una mediana, que ya es la cifra de un miembro con n impar, y sus casos de control
    de identidad son miembros con las mismas cifras): declarado.
- Casos de control (comprueban lo mismo, con su comentario «T-128»): REI-NAV-001 (NAV ajustado en su total, dispersión
  ausente con 2), REI-FFO-001 (cuatro sociedades más con la misma capitalización, FFO y AFFO de 2025: los múltiplos y el
  empate del percentil no cambian; la mediana y el IQR de la cobertura se siguen comprobando), IDX-REB-001 (dos valores por
  cesta con la misma demanda total), CHR-FUND-001 (la agregada contra las de cada plataforma calculadas a mano), FON-DISC-001
  («P = NAV ⇒ d = 0» con la desviación nula; la segunda vía con el indicador `ponderada_entre_min_y_max`).
- Pruebas existentes cambiadas por el comportamiento nuevo (comentario «T-128»; ninguna se debilita: lo que dejan de
  comprobar con 2 o 5 componentes lo comprueba `tests/test_t128_frontera.py` con 3 y 7):
  - `test_fase2_reales.py::test_rei_nav_doce_meses_justos_se_admiten_y_otros_pasivos_derivados_se_declaran` (la antigüedad
    en `antiguedad_nav_dias_max`) y `::test_rei_nav_oraculo_independiente` (con 2, dispersión y rango `null`);
  - `test_fase1_mon_idx.py::test_idx_reb_demanda_a_mano` (los días de volumen con los dos valores por cesta);
  - `test_fase1_fon_der.py::test_disc_valores_a_mano` (rango `null` con 5) y `_completos` de FON-DISC-001 (7 miembros, para
    que siga sin limitaciones).
- Límites conocidos: los de INC-T128-01 (medianas de 5 miembros en FON; propósito de ST-INF-001 y DER-OPT-001; los de
  T-127 sobre quien conoce las cifras de sus rellenos).
- Comandos exactos (desde la raíz, con `.venv`):
  - `cd bloque_a/11_Ejecutor && ../../.venv/bin/python -m pytest -q tests/test_t128_frontera.py tests/test_fase2_reales.py tests/test_fase1_fon_der.py tests/test_fase1_mon_idx.py`
  - `.venv/bin/python -I .docs/tickets/T-128/revisores/impl_barrido_identificadores.py bloque_a/11_Ejecutor`
  - `.venv/bin/python .docs/tickets/T-128/revisores/impl_mutantes.py bloque_a/11_Ejecutor <scratchpad>/t127r02_mut_t128`

## Ronda r02 (QA r01: H-01 alta, H-02 media, H-03 y H-04 bajas)

Hecha junto con la ronda r03 de T-127 (detalle de lo común en `.docs/tickets/T-127/analisis-tecnico.md`, «Ronda r03»).

- **H-01 (alta), límite declarado.** De dónde salen los componentes: los aporta quien pide (datos en línea de CT-09); en el
  ciclo, ninguna de estas fichas se pide desde el código, y HT-01 solo da cierres por símbolo, así que no hay fuente contra
  la que verificar una sociedad o un valor. Una sociedad o un valor troceados (o con su NAV por acción perturbado de forma
  simétrica) dan su cifra; CA-2 se matiza («sin construir los componentes a propósito»). Mitigación: el aviso de
  `frontera_b._aviso_casi_clones` en REI-NAV-001 (firma: precio, acciones, NAV por acción, deuda neta, otros pasivos, cap
  rate; el GAV no, lo fija la identidad del balance), que da la vía «S» del revisor. En REI-FFO-001 e IDX-REB-001 no hay
  aviso (datos que derivan unos de otros; dos datos por valor): declarado.
- **H-02 (media), CHR-FLOW-001** (`motor/fichas_reales.py`): las ofertas de cada moneda se guardan (`por_moneda`); con
  la oferta en la última fecha (o_T) y en la base del crecimiento (o_b): grupos por crecimiento a 30 días con la tolerancia
  de clon (`_etiquetas_casi_iguales`), rechazo con menos de `monedas_estables_minimas` (2, nuevo en `UMBRALES`), rechazo
  por dominancia de o_T y de o_b por grupos (`_sin_dominio`), y el crecimiento a `null` si su aportación (Σ(o_T − o_b) /
  Σo_b, en valor absoluto y con signo) pasa del 95 % (`_concentradas`). `FRONTERA_B` entra en sus `UMBRALES` (la petición
  no lo cambia). La capitalización total se valida igual. Rechazo y no `null` porque la oferta es una entrada obligatoria
  de la ficha, como un sector de un token en CHR-TOKEN-001; `null` para el crecimiento, como las cifras de CHR-TOKEN-001.
- **H-02, la «otra igual» de la tabla: IDX-CONC-001** (`motor/fichas_mon_idx.py`): con los precios de un solo componente
  la amplitud va a `null`; con un solo componente con sesiones suficientes, el porcentaje sobre la media; la contribución,
  con un índice de un componente o si la aporta casi entera uno (`_concentradas` con `FRONTERA_B`). Número nuevo
  `IDX_CONC_COMPONENTES_MINIMOS = 2` (el de REI-NAV, REI-FFO y un sector de CHR-TOKEN), `[PROPUESTO]`. Las demás filas: las
  que suman instrumentos tienen su mínimo (FON-DISC, FON-TD, ALT-AUC, IDX-REB, REI-*, CHR-TOKEN, FIR-CRED) o reciben
  ámbitos, tramos genéricos o el agregado ya hecho.
- **H-03 (baja):** declarado en INC-T128-01 («Límites declarados»), con la regla general (las que reciben el agregado o
  una serie hechos por quien pide no pueden saber si es de un instrumento).
- **H-04 (baja):** la fila de T-128 en `sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md` ya está
  en el árbol principal; no se toca.
- Pruebas: `tests/test_t128_r02.py` (nueva); ninguna existente cambia. Casos de control sin cambios (67/67).
- Comandos: los de `.docs/tickets/T-127/analisis-tecnico.md` («Ronda r03») y
  `/home/user/robotinvestor/.venv/bin/python -I .docs/tickets/T-128/revisores/r01_02_troceo_y_una_moneda.py bloque_a/11_Ejecutor`,
  `…/r01_01_barrido_un_componente.py bloque_a/11_Ejecutor`.
