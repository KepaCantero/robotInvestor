# T-119 · QA independiente

## Ronda r01

- **Revisor:** un revisor nuevo sin contexto de la implementación (subagente de Claude) · **Copia revisada:** `git worktree` en `3d857f1` (T-119, commit `d0c1f17`, integrado sobre T-118) · **Fecha:** 2026-11-14
- **Estado de la ronda:** terminada. Orden de lectura: plan (`README.md`) → las diez secciones del Catálogo → `fichas_p2.py` (leído entero hasta el registro de fichas; de los datos sintéticos, solo el registro `CASOS_CONTROL`) y las pruebas adaptadas → y solo al final `analisis-tecnico.md`, `pruebas.md` e INC-T119-01. `test_t119_p2.py` y `test_t119_motor.py` no los leí línea a línea: los ejecuté (suite y mutantes). Todo lo que sigue sale de ejecutar scripts propios, salvo donde digo «leído».

### Entorno y reproducción

- Copia propia (worktree del scratchpad), con `/home/user/robotinvestor/.venv/bin/python` (Python 3.12; numpy 2.5.4, scipy 1.18.1, pandas 3.1.1, statsmodels 0.15.0). No se tocó el árbol principal. **El gate completo `./tools/check_all.sh` no se lanzó** (máquina compartida, por instrucción): se pasaron sus piezas.
- Suite de `bloque_a/11_Ejecutor` (una vez, `pytest -q`): **5258 passed** en 28 min 52 s (con otros trabajos en la máquina; incluye las pruebas de T-118, ya integrado: `pruebas.md` da 4994 sin él).
- Gates ligeros, desde la raíz de la copia: `corpus_integridad.py` «Corpus íntegro: 695 archivos»; `refs_vivas.py`, `secrets_scan.py` y `nfc_check.py` en verde.
- ruff (los tres `11_Ejecutor`, `--output-format=concise | wc -l`): **2902** (cuota 2902); `fichas_p2.py` y las dos pruebas nuevas, «All checks passed». mypy de `bloque_a`: **109** (cuota 109), 0 líneas de `fichas_p2.py`.
- Mutantes y la reproducción del Catálogo, en copias desechables bajo `…/scratchpad/qa3_mut/`, borradas al acabar.

### Scripts del revisor

Todos con `.venv/bin/python -W ignore .docs/tickets/T-119/revisores/<script>` desde la raíz de la copia.

| Script | Qué ataca | Resultado |
| --- | --- | --- |
| `r01_comun.py` | Utilidades (Motor con Almacén temporal) | — |
| `r01_01_casos_ct09_ct10.py` | Los 33 casos de control por `Motor.servir`, su `comprobar` sobre lo servido, entrada SERVICIO en RC, `reejecutar` (CT-10), `verificar_casos_control` y dos procesos con distinto `PYTHONHASHSEED` | **37/37**: los 33 servidos (el más lento, 0,09 s), CT-10 = SI en los 33, una entrada CASOS_CONTROL por ficha, misma huella en los dos procesos |
| `r01_02_oraculos_a.py` | Oráculos propios de FIR-CRED, FX-BEER, CMD-REAL, REI-LEV, CHR-ONCHAIN y CHR-TOKEN (datos aleatorios propios) | **280/280** |
| `r01_03_oraculos_b.py` | Oráculos propios de PRV-PME, PRV-CF, ALT-HF y ALT-AUC; TIR con varias raíces, sin raíz y fuera de rango | **102/103** (H-03) |
| `r01_04_hostiles.py` | **35 659 llamadas** por `Motor.servir`: cada hoja de `valores` (primer, último y un elemento intermedio de cada lista) de tres casos por ficha con 38 valores hostiles (NaN, ±inf, −0.0, 1e308, 1e-320, 1e101, 10⁴⁰⁰, 2⁶³, texto numérico, vacío, None, bool, listas, objetos, tupla, tipos de numpy, Decimal, Fraction, complejo, bytes, lista anidada a 3 000 niveles, fechas imposibles) y quitada; cada bloque entero; cada parámetro (y dentro de sus listas); 11 campos de la petición; el solicitante; `datos` mal formados; parámetros no declarados, cada umbral de `UMBRALES` y `semilla` | Una entrada en RC por llamada, **nada no finito servido**, la llamada más lenta 0,5 s, parámetros no declarados, umbrales y `semilla` en `parametros` rechazados en las diez. Excepciones que escapan: 70, **ninguna de las fichas**: 60 son de mi proveedor de pruebas (no tiene `cierres`; una «serie» de texto llega a HT-01) y 10 son `RecursionError` con un **solicitante** anidado a 3 000 niveles (H-07, de `servicio.py`). Los 474 «tipo raro servido» son: campos que la ficha no usa con esos parámetros (`mu_historico` con `mu: r`), opcionales con None, y Decimal servido desde la caché (H-06) |
| `r01_05_catalogo.py` | §4, secciones, §1.3, diff frente al padre, manifiesto, CA-2 y la reproducción con `promover_fichas_catalogo.py` en una copia desechable | **29/29** |
| `r01_06_corte_cotas_config.py` | Fecha de corte campo a campo, por `as_of` y con la caché; cada cota en su máximo y con uno más; coste; configuración y CT-10 tras cambiarla | **113/114** (la que falla es de la caché del Motor, H-08) |
| `r01_07_merton_barrido.py` | 1 800 combinaciones de E/D, σ_E, T y r frente a un `fsolve` propio con 20 arranques; unicidad | **3/3**: 1 657 servidas, todas coinciden con la solución propia; ninguna con dos soluciones; ninguna combinación plausible rechazada |
| `r01_08_frontera_b.py` | Frontera con el Bloque B | **11/15** (H-01) |
| `r01_09_mutantes.py` | 74 mutantes nuevos de `fichas_p2.py` (41 de fórmula, 14 de fecha de corte, 19 de validaciones y cotas; 2 más no se aplicaron por un texto mal copiado, Q28 y Q83) frente a los casos de control y a `test_t119_p2.py` + `test_t119_motor.py` | **62 muertos, 12 vivos** (H-02) |

### Fidelidad a las fichas (oráculo propio en las diez)

| Ficha | Oráculo propio | Resultado |
| --- | --- | --- |
| FIR-CRED-001 | Sí: sistema de Merton con `fsolve` en (ln V, ln σ_V), 17 componentes aleatorios, T = 0,25, 1 y 3,5, iterativo e ingenuo; diferencial por la identidad B = V − E; PD real con μ; cuartiles y media ponderada por deuda; barrido de 1 800 combinaciones | Coincide (DD, PD neutral y real, proporción DD < 2, diferencial implícito, brecha y referencia). Fórmulas = ficha. Con σ_E·√T ≳ 22 (σ_E 500–1 000 % y T ≥ 5–30) se rechaza con un «math domain error» genérico: entradas absurdas, mensaje mejorable (observación) |
| FX-BEER-001 | Sí: DOLS con `statsmodels` OLS + HAC (Bartlett, sin corrección) con retardos 1, 2 y 4; ADF con `adfuller`; Johansen con `VECM(deterministic="ci")`; vida media con OLS; IC a mano | Coincide (β, ee, t, constante, equilibrio, desalineamiento, IC, velocidad, vida media, PPA, τ del ADF, vector de Johansen; crítico de la traza 76,97 = MHM caso 2, 5 variables) |
| CMD-REAL-001 | Sí: deflactado y percentil a mano, `scipy.stats.theilslopes`, percentil ponderado de 37 tramos con percentiles 0,013, 0,5, 0,9 y 1 | Coincide. Observación H-09: el IC de la tendencia no lleva la corrección de autocorrelación que sí lleva el p-valor |
| REI-LEV-001 | Sí: bucles a mano con 9 componentes, covenants en 6, borde exacto de los 24 meses, margen y caídas de la petición | Coincide |
| CHR-ONCHAIN-001 | Sí: `pandas.rolling` con medias de 1, 7, 90 y 365 días, 1 700 días | Coincide (MVRV, MVRV-Z, NVT, señal y los cuatro percentiles) |
| CHR-TOKEN-001 | Sí: sumas a mano con 7 tokens, uno sin oferta máxima, bordes de 30 y 90 días, cuatro ventanas | Coincide |
| PRV-PME-001 | Sí: KS-PME con bucles; TIR por Newton en tiempo continuo; alfa directo como raíz en a de Σ FV·e^{−a·t}; PME+ por su definición (la inversión en el índice acaba con el NAV del fondo) | Coincide |
| PRV-CF-001 | Sí: múltiplos y curva J a mano; Takahashi-Alexander con recurrencia propia; TIR con 2 y 3 raíces, sin raíz, sin cambio de signo y fuera de rango | Coincide; H-03 en el texto de la limitación con dos raíces |
| ALT-HF-001 | Sí: Geltner + OLS HAC de `statsmodels` con y sin desuavizado (97 meses, serie suavizada de verdad); ACC-FACT-001 servida con los mismos datos | Coincide (α, α anual compuesto, t de Newey-West, β, t, R²; idéntica a ACC-FACT-001) |
| ALT-AUC-001 | Sí: BMN y hedónico con `statsmodels` sobre 570 piezas, 2–3 ventas, ruido, pares en el mismo año y transacciones desordenadas | Coincide (índice periodo a periodo, bruta, neta, volatilidad, dispersión, referencias y segunda vía) |

**Casos de control.** Son frases de la «Verificación» de cada ficha (σ_V → 0 ⇒ PD → 0 y triángulo; residuo de media nula y FX-PPA; IPC constante; suma de vencimientos = deuda; MVRV = 1; circulante ≤ total ≤ máxima; réplica del índice ⇒ KS-PME = 1; TVPI = DPI + RVPI; coherencia con ACC-FACT-001; índice 100 y método alternativo) más identidades del «Método» escritas por el implementador con datos sintéticos; cada uno recalcula lo esperado desde los datos. Bien registrados (una entrada CASOS_CONTROL por ficha). De mis 41 mutantes de fórmula, 24 mueren ya ante ellos.

**Lo que la ficha nombra y no se calcula.** LN-PME: la ficha lo da por «opcional» y no lo lista entre los valores de `metodo`; no calcularlo es coherente, pero solo está declarado en INC-T119-01 y en el docstring, no en la entrega (H-05). Case-Shiller: la ficha nombra la familia de ventas repetidas; BMN la cumple y la falta de ponderación está en la incidencia. IC con Johansen: `null` y limitación en la respuesta. A mi juicio la promoción de las tres es correcta.

### Criterios de aceptación

| Criterio | Cumple | Evidencia |
| --- | --- | --- |
| CA-1 | sí | `r01_01`: 33 casos servidos y superados; `verificar_casos_control` supera en las diez y deja su entrada en RC. `r01_05`: `promover_fichas_catalogo.py` sobre el Catálogo del padre da «Promovidas: 10 · No superan: []» |
| CA-2 | sí | `r01_05`: 80 manejadores, 80 servibles (= código ∩ IMPLEMENTADO), AUD-REX-001 solo por CT-10; con el Catálogo del padre, METODO_NO_IMPLEMENTADO y 70 servibles. `r01_01`: CT-10 = SI en los 33 |
| CA-3 | sí | `r01_04` (umbrales, parámetros no declarados y `semilla` rechazados; dominios de cada parámetro sin escape) y `r01_06` (cada lista y cada tamaño: servido en su máximo, rechazado con uno más en < 2 s). Coste en el máximo, con la máquina cargada: ALT-AUC-001 53 s (50 000 transacciones, 100 años, 20 características), CHR-TOKEN-001 25 s; el resto < 4 s |
| CA-4 | sí | `r01_04`: 35 659 llamadas, nada no finito, ninguna excepción de las fichas, una entrada en RC por llamada. `r01_06`: un dato observado posterior al corte se rechaza en las diez, campo a campo (también con el corte por `as_of`, y la caché no lo salta). `r01_01`: dos procesos |
| CA-5 | **no** | Oráculo por ficha sí (los del paquete matan mis mutantes de fórmula, y los míos coinciden), pero **12 mutantes propios viven** ante los casos de control y las dos pruebas del paquete, 8 de ellos no equivalentes (H-02) |
| CA-6 | sí | `r01_05`: 81 IMPLEMENTADO, 0 DOCUMENTADO, §1.3 «81 = 14 + 67»; el diff del Catálogo son 21 líneas (10 filas, solo la columna de madurez; 10 líneas de ficha; §1.3); manifiesto de 695 huellas con una sola línea cambiada y la huella correcta; el script reproduce el Catálogo **byte a byte** |
| CA-7 | sí | 5258 pruebas en verde; ruff 2902 y mypy 109, iguales a la cuota; corpus, refs, secretos y NFC en verde |

### Otros puntos pedidos

- **Fecha de corte y fechas contractuales.** La decisión es correcta: un vencimiento o un desbloqueo futuros son el dato conocido hoy. No encontré por dónde colar información: un vencimiento anterior a la fecha de los datos se rechaza, un desbloqueo no posterior se excluye y se declara, y la fecha de los datos sí se compara con el corte. Quedan sin fecha propia (van con la del bloque) `pd_historica_rating_pct`, `referencia_cosecha`, `referencia` de ALT-AUC y `coste_refinanciacion`: no hay forma de comprobarlos.
- **Números.** Leído: los umbrales salen de la ficha o están marcados [PROPUESTO]. INC-T119-01 lista las cotas de tamaño y las decisiones de método; no enumera algunos rangos de dominio (H-04). El único número de configuración, `evaluacion.nivel_ic`, lo sigue FX-BEER-001 (con 0,5 el IC escala con z(0,75)/z(0,95)); el artefacto guarda la sección `evaluacion` usada y CT-10 da SI tras cambiar la configuración; una configuración inválida (1,5, 0, texto, None, NaN, bool, lista) se rechaza sin excepción. Las otras nueve no leen la configuración.
- **Regresiones adaptadas.** Leído el diff: las tres conservan su regla. La rama «Documentado en el Catálogo» la cubren además `test_t119_motor.py` y `test_t106_*`, y `r01_05`. Las 70 fichas anteriores: sus pruebas pasan en la suite (no volví a ejecutar sus casos de control aparte).
- **Invariantes.** El módulo solo calcula (numpy, scipy, pandas): ni LLM ni camino a órdenes. Falla cerrado y valida antes de calcular. Sin secretos ni datos personales. Decisiones como `[PROPUESTO]` en INC-T119-01, a T-57. `CLAUDE.md`, README del ejecutor y deuda técnica, al día y con recuentos ciertos (80 manejadores, 81 IMPLEMENTADO).

### Hallazgos

| ID | Gravedad | Cómo reproducirlo | Esperado / obtenido | Corrección sugerida | Estado |
| --- | --- | --- | --- | --- | --- |
| H-01 | media | `r01_08_frontera_b.py` (11/15) | **REI-LEV-001 entrega las cifras de un emisor concreto.** Con `componentes` de un solo elemento se sirve (SERVED, sin limitación) y el «agregado» es el LTV, el ICR, los vencimientos, el impacto en FFO y la holgura de covenants de esa sociedad; con una petición por emisor se ordenan (el script ordena S3 < S1 < S2 por LTV). INC-T119-01 dice que la frontera «la garantiza la forma de la salida»: con un componente no. Con dos, el mínimo y el máximo de la dispersión son las dos cifras individuales. Además: FIR-CRED-001 exige 10 componentes pero acepta 10 copias idénticas del mismo emisor con ids distintos (la mediana es su DD y su PD), y CHR-TOKEN-001 sirve un solo token con ámbito «sector» sin declararlo (la ficha solo lo admite «cuando el ámbito es la propia red»). No hay ids ni filas por componente en ninguna salida, y la diferencia entre dos peticiones es inherente a cualquier agregado (no es hallazgo). REI-NAV-001 (T-112) tiene el mismo hueco | Mínimo de componentes en REI-LEV-001 ([PROPUESTO], p. ej. 3) o rechazo con uno; dispersión sin mínimo ni máximo por debajo de un tamaño; rechazo de componentes con datos idénticos en FIR-CRED-001; en CHR-TOKEN-001, un token solo si el ámbito se declara como la propia red, y declararlo en la entrega. Pruebas de cada uno | abierto |
| H-02 | media | `r01_09_mutantes.py <carpeta desechable>` | **Reglas sin red: 12 mutantes vivos.** No equivalentes: Q12 (CMD-REAL: Mann-Kendall sin la corrección de Hamed-Rao: cambia el p-valor y la dirección publicados); Q17 (REI-LEV: «en incumplimiento» solo si fallan los dos covenants a la vez); Q55 (PRV-CF: un NAV posterior al corte se admite); Q58 (CMD-REAL: curva de costes posterior al corte dentro del último mes); Q54 (PRV-PME: niveles del índice posteriores al corte); Q84 (PRV-PME: `rentabilidad_total` con cualquier valor verdadero, p. ej. el texto "no"); Q86 (ALT-HF: φ = ±1 admitido); Q70 (magnitud de tipos de numpy sin mirar). Equivalentes o redundantes hoy: Q50 y Q53 (la serie y los flujos ya quedan acotados por el vintage y por el NAV), Q60 (por los niveles) y Q73 (la identificación de Johansen la cubren otras comprobaciones). El código actual es correcto en todos (los rechazos se ven en `r01_06`), pero un cambio que los rompa pasa las pruebas: CA-5 no se cumple | Pruebas: dirección y p-valor de la tendencia con una serie autocorrelacionada; un componente que incumple solo un covenant; el corte campo a campo (NAV de PRV-CF, curva de costes, niveles del índice), no solo un campo por ficha; `rentabilidad_total` con 1 y con texto; φ en el borde. Volver a pasar `r01_09` | abierto |
| H-03 | baja | `r01_03_oraculos_b.py`: flujos −100, +230, −132 a 0, 1 y 2 años | Hay dos TIR (10 % y 20 %) y la respuesta dice «TIR: sin TIR entre -0.99 y 10» (con `tir_pct` null). El `null` está declarado en `analisis-tecnico.md` («con un número par de raíces, null»), pero el texto de la limitación afirma algo falso. Con tres raíces (5, 15 y 40 %) entrega 40 % con el aviso: correcto según la ficha | Cambiar el texto («no se aísla una TIR única entre…») o buscar los cambios de signo en una rejilla y declarar cuántas hay | abierto |
| H-04 | baja | Leído: `UMBRALES` frente a INC-T119-01 | Varios rangos marcados [PROPUESTO] en el código no están enumerados en la incidencia: tipos y costes en (−1, 1), volatilidad de las acciones ≤ 10, margen en [0, 1), rendimiento de *staking* en (−1, 10), 20 características y 3 periodos mínimos en ALT-AUC-001, `percentil_coste` en (0, 1] | Añadirlos a INC-T119-01 | abierto |
| H-05 | baja | Leído y `r01_03` | PRV-PME-001 no declara en la entrega (advertencias o limitaciones) que LN-PME no se calcula; solo en la incidencia y el docstring | Una línea en `ADVERTENCIAS` o en las limitaciones | abierto |
| H-06 | baja (heredado, `servicio.py`; no es de T-119) | En un mismo Motor: servir FIR-CRED-001 con `capitalizacion = np.float32(1.5)` y después con `Decimal("1.5")` o con el texto `"1.5"` | La segunda y la tercera se sirven desde la caché (CACHE_HIT) cuando solas se rechazan: la clave de idempotencia serializa con `str` los tipos que no son JSON y colisiona. Solo alcanzable en proceso con un tipo de numpy que no viene de JSON | Rechazar en la forma de la petición los tipos no JSON de `valores`, o distinguir el tipo en la clave. A la deuda | abierto |
| H-07 | baja (heredado, `servicio.py`) | `r01_04`: `Motor.servir(peticion, solicitante=<lista anidada a 3 000 niveles>)` | `RecursionError` que escapa (10 veces, una por ficha). El solicitante lo pone el código, no la petición | Comprobar que el solicitante es texto al entrar. A la deuda | abierto |
| H-08 | baja (heredado, mecanismo de T-118) | `r01_06`, bloque 3: servir FX-BEER-001, cambiar `m.cfg["evaluacion"]["nivel_ic"]` en el mismo Motor y servir otra vez | La segunda se sirve desde la caché con el nivel anterior (0,5 en vez de 0,99): la configuración leída no entra en la clave. En el ejecutor la configuración se carga al arrancar y la caché es de proceso: escenario artificial | Incluir en la clave la huella de las secciones leídas, o vaciar la caché al cambiar la configuración. A la deuda | abierto |
| H-09 | baja (heredado, FX-TREND-001) | `r01_02`, CMD-REAL: paseo aleatorio de 400 meses | `ic_tendencia_pct_anual` = [−1,15; −0,53] (excluye el 0) con `tendencia_p_valor` 0,31 y «sin tendencia»: el p-valor lleva la corrección de Hamed-Rao y el IC de la pendiente no | Usar la varianza corregida en el IC de Sen, o declararlo en la entrega de CMD-REAL-001 | abierto |

### Veredicto

**NO APTO.** No hay ningún hallazgo crítico ni alto, pero CA-5 no se cumple (H-02: 8 mutantes no equivalentes viven ante los casos de control y las pruebas del paquete) y queda un medio de frontera con el Bloque B (H-01: REI-LEV-001 sirve las cifras de un emisor con un solo componente). Ambos son de corrección corta: pruebas en H-02 y una regla de mínimo de componentes en H-01. Los bajos (H-03 a H-05) conviene corregirlos en la misma ronda; H-06 a H-09 son heredados y pueden ir a la deuda.

Lo demás está bien: las diez fichas coinciden con oráculos propios en datos no degenerados (385 comprobaciones, una sola discrepancia, de texto), los 33 casos de control se sirven, quedan en RC y se re-ejecutan con SI, 35 659 llamadas hostiles sin una cifra no finita ni una excepción de las fichas, todas las cotas funcionan y el servicio más caro termina en menos de un minuto, la fecha de corte se aplica campo a campo, el Catálogo se reproduce byte a byte y el corpus está íntegro.

**Sin comprobar:** el gate completo `check_all.sh` y las suites de A-Forex y B (no se lanzaron); la regresión del ciclo simulado de `CLAUDE.md` (T-119 no toca el ciclo); los casos de control de las 70 fichas anteriores aparte de la suite; los mutantes Q28 y Q83 (no aplicados); `test_t119_p2.py` y `test_t119_motor.py` no se leyeron enteros; el hostil solo sustituye tres elementos por lista.

Vuelve a `ri-implementar`. En la r02 se vuelven a ejecutar `r01_01` a `r01_09`.

## Ronda r02

- **Revisor:** subagente revisor nuevo, sin contexto de la implementación (Claude; implementó otra sesión de Claude) · 2026-11-14
- **Copia revisada:** `git worktree` con HEAD separado en `63d6ae9` («wip local: integrar T-119 r02 y T-121»): `fichas_p2.py`, `fichas_reales.py` (REI-NAV-001), `servicio.py` (caché, solicitante) y `tests/test_t119_r02.py`, `tests/test_t119_p2.py`. Los cambios de `servicio.py` se comparten con T-121 (H-02); los atribuyo por sus comentarios («r02 de T-119»).
- **Orden de lectura:** `qa.md` r01 → diff → scripts → al final la «Ronda r02» de `analisis-tecnico.md` y `pruebas.md` e INC-T119-01.

### Scripts del revisor anterior (sin modificar)

Desde la raíz de la copia, `.venv/bin/python -I .docs/tickets/T-119/revisores/<script> bloque_a/11_Ejecutor`.

| Script | r01 | r02 |
| --- | --- | --- |
| `r01_01_casos_ct09_ct10.py` | 37/37 | **37/37** (33 casos de control por CT-09, en RC y por CT-10 con SI; dos procesos con la misma huella) |
| `r01_02_oraculos_a.py` | — | **280/280** |
| `r01_03_oraculos_b.py` | H-03 | **103/103**; flujos −100, +230, −132: «2 soluciones entre -0.99 y 10 (rejilla de 1000 puntos): no se aísla una TIR única y no se entrega ninguna» (H-03 corregido) |
| `r01_04_hostiles.py` | 70 escapes (60 del proveedor de pruebas, 10 de H-07); 474 «tipo raro servido» | **4/5**, mismas 35 659 llamadas, nada no finito, una entrada en RC por llamada, la más lenta 0,4 s. El que falla, «ninguna excepción escapa», es por las **60** llamadas con una `serie` de texto en `datos`, que llegan a HT-01 y el proveedor de pruebas del script no tiene `cierres` (`AttributeError` del propio doble de pruebas, igual que en la r01). Con el `ProveedorCSV` real y su `as_of` fijado, esas seis series (y `"\ud800"`) dan RECHAZADO con una entrada en RC cada una; sin fijar el `as_of`, sale de `servir` el `RuntimeError` de HT-01 «fije la fecha as_of» (anterior a T-119; el ciclo siempre lo fija). Los 10 `RecursionError` del solicitante (H-07) **ya no salen**. «Tipo no numérico servido donde había un número»: 97 (antes 474; ya no hay Decimal servido desde la caché) |
| `r01_05_catalogo.py --desechable <carpeta>` | 29/29 | **29/29** (despacho: 80 manejadores servibles; `promover_fichas_catalogo.py` da 10 promovidas y reproduce el Catálogo byte a byte) |
| `r01_07_merton_barrido.py` | 3/3 (1 657 servidas de 1 800) | **3/3**: 1 657 servidas y 143 rechazadas, como en la r01; ninguna combinación plausible rechazada. De las 135 rechazadas que tienen solución propia, los ejemplos que imprime el script están en los bordes extremos (E/D ≤ 0,01 con T = 30 y r negativo; «math domain error» o no convergencia); el script comprueba que ninguna esté en el rango plausible |
| `r01_06_corte_cotas_config.py` | H-08 | **114/114**; vencimientos y desbloqueos futuros servidos, el resto de fechas observadas rechazadas |
| `r01_08_frontera_b.py` | 11/15 | **Se detiene** en la línea 83 con `KeyError: 'limitaciones'`, tal como dice el implementador: el script imprime `r['limitaciones']` de la respuesta de CHR-TOKEN-001 con un token, y esa respuesta es ahora un **rechazo** (`RECHAZADO`, que no lleva `limitaciones`). Es un defecto del script, no del paquete: lo que la línea iba a comprobar («RECHAZADO o declarado») se cumple (lo he comprobado aparte: con un token y sin `ambito_es_red`, o con `false`, RECHAZADO; con `true`, servido con «un solo token: el ámbito declarado es la propia red»; con `"si"`, RECHAZADO). Antes de pararse, los 15 `ok` de los bloques 1 y 2 (sin ids ni filas por componente; REI-LEV con un componente y FIR-CRED con 9 o con 10 copias idénticas, rechazados). Los bloques 3 y 4 no llegan a correr: el 3 (REI-LEV con 2) lo cubre ahora el mínimo de 3; el 4 era informativo |
| `r01_09_mutantes.py <desechable> --solo Q12,Q17,Q55,Q58,Q54,Q84,Q86,Q70` | 8 vivos no equivalentes | **8 muertos, 0 vivos**, cada uno por una prueba nueva de `test_t119_p2.py` (`test_r02_h02_…`) |

### Scripts nuevos de esta ronda

| Script | Orden | Resultado |
| --- | --- | --- |
| `r02_01_frontera_b.py` | `.venv/bin/python -I .docs/tickets/T-119/revisores/r02_01_frontera_b.py bloque_a/11_Ejecutor` | **0/5**: las cifras de un solo emisor o token salen por las tres vías (H-10) |
| `r02_02_cache.py` | `.venv/bin/python -I .docs/tickets/T-119/revisores/r02_02_cache.py bloque_a/11_Ejecutor` | **11/12** (H-11) |

**Frontera con el Bloque B (`r02_01`).** La r02 rechaza un solo componente y los clones exactos; lo de al lado sigue pasando:
- **Casi clones.** FIR-CRED-001 con 10 copias de un emisor cuya capitalización difiere en 1e-9 relativo por copia: se sirve, y la dispersión de la DD colapsa (mínimo = mediana = máximo a 6 decimales). Con tres emisores del caso de control: C00 1493,80 · C05 1303,81 · C09 1240,35, es decir, la DD de cada emisor y su orden. REI-LEV-001 con 3 casi clones de S1, S2 o S3: LTV 40,0 · 50,0 · 22,5 (los de cada sociedad). CHR-TOKEN-001 con un token y su casi clon, ámbito «sector»: se sirve como sector.
- **Peso casi total.** REI-LEV-001 con una sociedad y las otras dos a escala 1e-6: LTV agregado 39,999999 / 49,999965 / 22,500085 frente a 40 / 50 / 22,5 de cada una; ICR 3,999999 / 2,700002 / 4,999991 frente a 4 / 2,7 / 5. CHR-TOKEN-001 con un relleno de precio 1e-9: la capitalización es la del token.
- **La dispersión con el mínimo nuevo.** REI-LEV-001 con sus 3 componentes de control: mínimo, mediana y máximo del LTV son **exactamente** los tres LTV individuales (22,5; 40; 50), y lo mismo en las demás métricas. INC-T119-01 justifica el mínimo de 3 con «con dos, el mínimo y el máximo de la dispersión son las dos cifras individuales»; con tres, además la mediana. La sugerencia de la r01 («dispersión sin mínimo ni máximo por debajo de un tamaño») no se aplicó.
- **`ambito_es_red`.** Un token solo se sirve si la petición declara `ambito_es_red: true`; es una declaración del solicitante, que nada comprueba.
- Fuera de las P2 (para que conste): REI-NAV-001 (T-112) devuelve `componentes: {"A": {"prima_pct": -10.0, …}, "B": {"prima_pct": 5.0, …}}`, una fila por sociedad **con su identificador**. Puede ser lo que pide su ficha (no lo he comprobado en el Catálogo); el mínimo de 2 de la r02 no cambia eso.

**Caché (`r02_02`).** H-06: con `np.float32`, `Decimal`, texto, `np.int64`, `True` por 1 y `np.float64`, lo servido tras una petición válida es lo mismo que la variante sola en un Motor nuevo (Decimal y texto, rechazados las dos veces; `np.float64` sale de la caché con el mismo resultado). Pero **una tupla** en lugar de la lista de `componentes`: sola, RECHAZADO («se esperaba una lista no vacía»); tras la lista, **CACHE_HIT** servido (H-11). H-08: sustituir la sección `evaluacion` de `m.cfg`, mutarla en su sitio, volver a un valor anterior y cambiar la copia en memoria de `por_defecto.yaml` con la sección ausente del Motor: en los cuatro, las cifras de un Motor nuevo con esa configuración (sin caché indebida).

### Criterios de aceptación

| Criterio | Cumple | Evidencia |
| --- | --- | --- |
| CA-1 | sí | `r01_01` 37/37; mi `r01_04_casos_control.py` de T-121: `verificar_casos_control` 67/67 (incluye las diez) |
| CA-2 | sí | `r01_01`: CT-10 SI en los 33; `r01_05` 29/29 (despacho de 80 manejadores servibles) |
| CA-3 | sí | `r01_06` 114/114; `r01_04`: umbrales, parámetros no declarados y dominios sin escape de las fichas |
| CA-4 | sí | `r01_06` (fecha de corte en las diez), `r01_01` (dos procesos); escapes de `servir`: `r01_04` (los únicos 60 son del doble de pruebas del script, como en la r01; los 10 de H-07 ya no salen) y el fuzz de T-121 (0 escapes en 5 758 llamadas) |
| CA-5 | **sí** | Los 8 mutantes no equivalentes de la r01 mueren (`r01_09 --solo`); `r01_02` 280/280 y `r01_03` 103/103 con oráculos propios |
| CA-6 | sí | `r01_05` 29/29 (Catálogo reproducido byte a byte); corpus íntegro (695) |
| CA-7 | sí, salvo el gate entero | Suite de A: **5663 passed** (23 min 43 s, una vez, común a los cuatro tickets); ruff 2902, mypy 109; corpus, refs, secretos y NFC en verde |

### Hallazgos de la r01

| ID | Estado | Evidencia |
| --- | --- | --- |
| H-01 (media) | **corregido en parte** (los casos literales de la r01); el resto en H-10 | `r01_08` bloques 1 y 2; `r02_01` |
| H-02 (media) | corregido | 8 muertos |
| H-03 (baja) | corregido | `r01_03`: «2 soluciones … no se aísla una TIR única» |
| H-04 (baja) | corregido | INC-T119-01, «Ronda r02», rangos enumerados (leído) |
| H-05 (baja) | corregido | `ADVERTENCIAS["PRV-PME-001"]`: «LN-PME … no se calcula» (leído en el diff) |
| H-06 (baja, heredado) | corregido en parte: queda la tupla (H-11) | `r02_02` |
| H-07 (baja, heredado) | corregido (con T-121 H-02) | Prueba `test_h02_argumentos_de_la_llamada_que_no_son_texto` (con el solicitante de 3 000 niveles) y el fuzz de T-121 |
| H-08 (baja, heredado) | corregido | `r02_02` bloque 2 |
| H-09 (baja, heredado) | corregido (declarado en la entrega) | `ADVERTENCIAS["CMD-REAL-001"]` (leído) |

### Hallazgos nuevos

| ID | Gravedad | Cómo reproducirlo | Esperado / obtenido | Corrección sugerida | Estado |
| --- | --- | --- | --- | --- | --- |
| H-10 | media | `.venv/bin/python -I .docs/tickets/T-119/revisores/r02_01_frontera_b.py bloque_a/11_Ejecutor` | **Esperado** (1.6 y la convención del módulo: «con su salida no se puede ordenar emisores ni tokens»): ninguna petición da las cifras de un emisor o token concreto. **Obtenido:** con casi clones (1e-9), con un componente de peso casi total o simplemente con 3 componentes en REI-LEV-001, la salida da la DD y la PD (FIR-CRED), el LTV, el ICR y las demás métricas (REI-LEV) y la capitalización y la dilución (CHR-TOKEN) de un solo emisor o token, y los ordena. La regla exacta de clones es una decisión declarada («la regla es exacta, no de tolerancia»), pero la justificación del mínimo de 3 en INC-T119-01 es incorrecta (con 3, mínimo, mediana y máximo son los tres valores) y el peso casi total no está declarado | Por debajo de un tamaño (p. ej. 5 componentes [PROPUESTO]) no entregar mínimo, máximo ni cuartiles; rechazar un agregado en el que un componente pese más de una fracción (p. ej. 50 %) de la base de ponderación; tratar como clones los componentes iguales con una tolerancia relativa; o decidir con el operador que la frontera es solo de forma (sin ids) y declararlo así en INC-T119-01 | abierto |
| H-11 | baja | `.venv/bin/python -I .docs/tickets/T-119/revisores/r02_02_cache.py bloque_a/11_Ejecutor` (caso «tupla de componentes») | **Esperado:** la caché no entrega lo que la ficha sola no serviría. **Obtenido:** FIR-CRED-001 con `componentes` como tupla se rechaza sola, pero tras la misma petición con lista sale como CACHE_HIT servido: `_firma_tipos` serializa con JSON y la tupla y la lista dan lo mismo. Solo en proceso (de JSON no llega una tupla) y el resultado entregado es el correcto | Incluir en la firma el tipo de los contenedores (`default` no se llama para tuplas) o rechazar en la forma los contenedores que no son de JSON | abierto |

### Veredicto

**APTO.**

Los siete criterios se cumplen (CA-7 sin el gate entero, que no he lanzado por instrucción) y no queda ningún hallazgo crítico ni alto. Lo que decidió el NO APTO de la r01 está resuelto: los 8 mutantes no equivalentes mueren (CA-5), y los casos literales de H-01 (un componente, clones exactos, un token como sector) se rechazan. Los scripts de la r01 dan lo mismo o mejor (`r01_01` 37/37, `r01_02` 280/280, `r01_03` 103/103, `r01_05` 29/29, `r01_06` 114/114, `r01_07` 3/3; `r01_04` sin escapes de las fichas y sin los 10 de H-07; `r01_08` se para por un `KeyError` del propio script al leer `limitaciones` de lo que ahora es un rechazo, y lo que iba a comprobar se cumple). La caché ya distingue tipos y configuración (H-06 y H-08), salvo la tupla de H-11.

Queda un **medio, H-10**, que conviene decidir con el operador antes del modo sombra y no dejar solo como deuda técnica: la frontera con el Bloque B se cruza con casi clones, con un componente de peso casi total o simplemente con los 3 componentes mínimos de REI-LEV-001 (mínimo, mediana y máximo son las tres cifras individuales), y la justificación del mínimo de 3 en INC-T119-01 es incorrecta. Y un bajo, **H-11** (la tupla en la caché). Pasan a la deuda con su ID si no se corrigen.

**Condición de cierre:** `./tools/check_all.sh` 12/12 en el commit.

**Sin comprobar:** el gate entero; los mutantes de la r01 fuera de los ocho vivos (no he vuelto a pasar `r01_09` entero) e `impl_r02_mutantes.py`; la ficha de REI-NAV-001 en el Catálogo (si su fila por sociedad es lo que pide); las suites de A-Forex y B.
