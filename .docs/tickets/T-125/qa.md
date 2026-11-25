# T-125 · QA independiente

- **Revisor:** revisor nuevo sin contexto de la implementación (subagente de Claude; no implementó T-125) · **Ronda:** r01 · 2026-11-15
- **Copia revisada:** clon desconectado en `fb3ccd4` (incluye `df4a60a`, el commit de T-125). Mutantes en una copia desechable aparte («qa7_mut»), ya borrada.
- Opinión formada con el plan (PB-46), el Documento 0 (12.2, 12.5, 13.3, rúbrica de F9), los esquemas de F2 (3, reglas 2–4 y 8; 4.1) y F6 (4.5) y el código, antes de leer `analisis-tecnico.md`.

## Reproducción desde limpio

| Qué | Orden (desde `bloque_a/11_Ejecutor`) | Resultado |
| --- | --- | --- |
| Pruebas del ticket | dentro de la suite completa de A | en verde (ver la suite en `T-116/qa.md`, ronda r04) |
| Goldens de contratos | `python tests/goldens_ct.py` | «goldens de contratos: coinciden» |
| ruff (tres `11_Ejecutor`, como el gate) | `ruff check --output-format=concise … \| wc -l` desde la raíz | 2902 (cuota 2902) |
| Gates ligeros | `tools/secrets_scan.py`, `refs_vivas.py`, `nfc_check.py`, `corpus_integridad.py` | los cuatro con 0 |
| Ataques | `QA_TMP=<carpeta temporal> python ../../.docs/tickets/T-125/revisores/r01_01_ataques_fiabilidad.py` | abajo |
| Camino de entrada a F2 | `QA_TMP=<carpeta temporal> python ../../.docs/tickets/T-125/revisores/r01_03_camino_de_entrada_a_f2.py` | abajo (H-01) |
| Mutantes | desde la raíz: `python .docs/tickets/T-125/revisores/r01_02_mutantes.py <copia desechable de bloque_a con «_mut»>` | abajo |

## Criterios de aceptación

| Criterio | Cumple | Evidencia |
| --- | --- | --- |
| CA-1 · dos fuentes de 25, FUE- con la fórmula, la hábil > 10 y la otra < 10 | sí | `test_pb46_dos_fuentes_…`; K03 y K14 mueren. A mano (A8): BSS 0 da 10 puntos; una fuente que siempre falla con 0,99 da 0 |
| CA-2 · en un ciclo, la FUE- en F6 con el `msg_id` del CT-19 a AG-16 | sí, **solo con F2 sembrado a mano** | `test_pb46_las_fue_quedan_…` (K02 muere). Pero en un ciclo de verdad F2 nunca recibe un pronóstico de fuente (H-01) |
| CA-3 · una vez al mes; sin muestra, nada | sí, con un matiz (H-06) | K04 y K10 mueren. A4: con dos ciclos en junio, la fuente que llega a `n_min` a mitad de mes espera a julio |
| CA-4 · no vencidos, mal formados o sin dato no cuentan; las cuatro direcciones | **no** | Una fecha objetivo con zona horaria (ISO válido) lanza `TypeError` y tumba el C5 entero en cada ciclo (H-02). Además, dos casos de la prueba pasan por otro motivo: «fuera de ventana» (2020) y «no ha vencido» (2026-12-31) caen por falta de datos o por la antigüedad del cierre, no por la regla que dicen probar: K05 y K07 viven (H-07) |
| CA-5 · sin pronósticos de fuentes el ciclo no cambia; goldens, ruff, mypy, gate | sí en lo comprobado | goldens y ruff, arriba; mypy y el gate no los he pasado (encargo) |

## Ataques (`revisores/r01_01_ataques_fiabilidad.py`, ejecutado)

| Ataque | Obtenido | Juicio |
| --- | --- | --- |
| A1 · la pieza entra en F2 cuando su fecha objetivo ya pasó (resultado conocido al registrarla) | 5 de 5 cuentan | H-03 |
| A2 · `ref_id` arbitrario («cualquier cosa», «OPP-2026-0001», «REF-9999») | tres FUE- con esos `ref_id` | H-04 |
| A3 · el mismo pronóstico de la fuente en dos afirmaciones de texto distinto | n = 10 en vez de 5 | H-05 |
| A4 · dos ciclos en junio; REF-0002 llega a 5 resueltos entre los dos | junio: solo REF-0001; julio: REF-0001 y REF-0002 | H-06 |
| A5 · probabilidades 0, 1, NaN, inf, −0,2, «0.7», 70, `[0.7]`, `True` | fuera; 1e-9 y 0,999999999 cuentan; sin declarar → 0,7 | correcto (falla cerrado) |
| A6 · fechas | con hora, cuenta; objetivo = `as_of`, cuenta; 30 de febrero, número, fuera de ventana, objetivo > `as_of`, objetivo = emisión: fuera; **con zona horaria: `TypeError`** | H-02 |
| A6b/A6c · una sola pieza con zona horaria dentro de un ciclo | el ciclo acaba COMPLETO, pero `evaluacion` = `{"error"}`, ninguna FUE- (tampoco la de la fuente sana) e incidencia HERRAMIENTA «Evaluador no disponible»; un mes después, otra vez | H-02 |
| A7 · determinismo (mismo escenario, dos almacenes) | idénticos | correcto |
| A8 · extremos | siempre 0,99 y falla: BSS −2,92, puntos 0; siempre 0,5: BSS 0, puntos 10 | correcto |
| A9 · `prob_sin_declarar` frente a la banda «más probable que no» | 0,7 frente a 0,65 de `bandas_verbales` | H-08 |

## Camino de entrada a F2 (`revisores/r01_03_camino_de_entrada_a_f2.py`, ejecutado)

Con el cliente simulado parcheado para que el Analista devuelva en cada afirmación un bloque `pronostico_fuente` completo y el Curador las clasifique como PRONOSTICO_FUENTE (lo más que puede hacer el modelo real): «ciclo COMPLETO · CLM en F2: 12 · clasificadas PRONOSTICO_FUENTE: 12 · **con bloque pronostico_fuente: 0** · pronósticos de fuentes que ve el Evaluador: 0». Leído: `_f_analistas` construye cada pieza con cinco claves fijas (`afirmacion`, `fuente`, `direccion`, `extracto`, `origen`; `orquestacion.py`, línea 882), y las piezas del Buscador y del momentum tampoco llevan el bloque (líneas 885 y 958); la línea nueva de T-125 (`clm["pronostico_fuente"] = dict(p["pronostico_fuente"])`, 1265) no se alcanza nunca. K01 (borrarla) vive.

## Mutantes (`revisores/r01_02_mutantes.py`, contra las 12 pruebas de `test_t125_fiabilidad_fuentes.py`)

| Mutante | Qué rompe | Resultado |
| --- | --- | --- |
| K01 | el alta en F2 deja de guardar `pronostico_fuente` | **VIVO** (H-01) |
| K02 | la FUE- no anota el `msg_id` del CT-19 | MUERTO |
| K03 | sin contracción n / (n + k) | MUERTO |
| K04 | sin «una vez al mes» | MUERTO |
| K05 | sin ventana de 24 meses | **VIVO** (H-07) |
| K06 | sin el control de antigüedad del cierre (H2) | **VIVO** (H-07) |
| K07 | cuenta pronósticos no vencidos | **VIVO** (H-07; el proveedor recorta en `as_of`, así que no hay fuga, pero la regla no tiene prueba) |
| K08 | admite emisión = objetivo | **VIVO** (baja, dentro de H-07) |
| K09 | probabilidad sin declarar 0,5 | MUERTO |
| K10 | `n_min` uno menos | MUERTO |
| K11 | puntos sin acotar a [0, 20] | **VIVO** (H-07) |
| K12 | admite probabilidad 0 y 1 | **VIVO** (H-07) |
| K13 | «dentro» con bordes abiertos | **VIVO** (H-07) |
| K14 | referencia ingenua fija en 0,4 | MUERTO |

Resumen: 6 de 14 muertos (K02, K03, K04, K09, K10, K14), 8 vivos.

## Hallazgos

| ID | Gravedad | Cómo reproducirlo | Esperado / obtenido | Corrección sugerida | Estado |
| --- | --- | --- | --- | --- | --- |
| H-01 | **alta** | `r01_03_camino_de_entrada_a_f2.py`; leer `orquestacion.py` 880–890 y 955–960; K01 de `r01_02` | Esperado (README, Diseño: «el registro de evidencia guarda ahora ese bloque cuando la pieza lo trae»; Doc. 0 12.5): un pronóstico explícito de una fuente que devuelve un agente llega a F2 y el Evaluador lo mide. Obtenido: **ninguna pieza puede traer el bloque**; el ejecutor reconstruye cada pieza con claves fijas y lo pierde, también con el modelo real. Fuera de las pruebas (que siembran F2 a mano), ningún ciclo produce nunca una FUE-. El análisis técnico lo atribuye al cliente simulado («con el cliente simulado no se generan piezas PRONOSTICO_FUENTE»), y el mapa de PB-46 solo declara como hueco la recalificación en F9 | Copiar `pronostico_fuente` (y `tipo_afirmacion`) de la afirmación del Analista y de la referencia del Buscador a la pieza, validado (H-02, H-04) y con su prueba de extremo a extremo (cliente simulado parcheado, como `r01_03`); o, si se decide no hacerlo ahora, declararlo como hueco en el mapa (PB-46), en INC-T125-01 y en el análisis, sin atribuirlo al simulador |
| H-02 | media | `r01_01`, A6, A6b y A6c | Esperado (CA-4; docstring: «uno mal formado o sin dato se omite»): la pieza se omite. Obtenido: `fecha_objetivo` con zona («2025-06-02T10:00:00+05:00») lanza `TypeError: Cannot compare tz-naive and tz-aware timestamps`; `Bloque.ciclo` lo recoge como «Evaluador no disponible», el resultado del C5 del run se pierde (`evaluacion = {"error"}`, sin FUE- de ninguna fuente) y, como F2 es append-only y la ventana es de 24 meses, se repite en cada ciclo. Hoy no llega por H-01; en cuanto se conecte, sí | En `_campos_pronostico_fuente`, normalizar a fecha sin zona (`tz_convert(None)` o quedarse con la fecha) o rechazar la pieza; envolver cada pieza para que una sola no tumbe las demás; prueba con zona, con `Z` y con hora |
| H-03 | media | `r01_01`, A1 | Esperado (F2, regla 4: «`conocible_desde` … es el filtro anti-fuga»; Doc. 0 12.2: sin fuga): solo cuentan los pronósticos registrados antes de conocerse su resultado. Obtenido: una pieza que entra en F2 después de su fecha objetivo cuenta igual; un agente que cita «como predijo X» solo lo que acertó infla la fiabilidad de esa fuente. No está en INC-T125-01 | Contar solo las CLM cuya alta en F2 (o `conocible_desde` de su evidencia) sea anterior a la fecha objetivo; decisión `[PROPUESTO]` en INC-T125-01 y prueba |
| H-04 | media | `r01_01`, A2 | Esperado (valida antes de mutar): el `ref_id` es el de una fuente registrada de F9 (o, al menos, la fuente de la evidencia de la pieza). Obtenido: FUE- para «cualquier cosa», «OPP-2026-0001» y «REF-9999», que se comunican al Buscador por CT-19 | Exigir que `ref_id` exista en F9 (`Referencias.por_id`) y coincida con la fuente de la pieza; prueba |
| H-05 | baja | `r01_01`, A3 | Esperado (R10, contar raíces): un mismo pronóstico de la fuente cuenta una vez. Obtenido: dos afirmaciones de texto distinto con el mismo bloque dan n = 10 en vez de 5 (la deduplicación de CLM es por texto) | Deduplicar por (`ref_id`, `serie_ht01`, `fecha_objetivo`, `umbral_o_rango`, `direccion`, `fecha_emision`) |
| H-06 | baja | `r01_01`, A4 | INC-T125-01 dice «una FUE- por fuente y mes»; el código hace «una tanda por mes»: si hay alguna FUE- del mes, no calcula ninguna más, y una fuente que llega a `n_min` después espera al mes siguiente | Comprobar el periodo por `ref_id`, o decir en INC-T125-01 que es una tanda mensual |
| H-07 | baja | K05 a K08 y K11 a K13 de `r01_02` viven | En `test_pb46_no_se_resuelve_…` el caso «fuera de ventana» (objetivo 2020) cae porque los datos sintéticos empiezan en 2022, y el de «no ha vencido» (2026-12-31) por la antigüedad del cierre: ninguna de las dos reglas tiene prueba. Tampoco la antigüedad, los bordes de «dentro», el tope de puntos ni el rechazo de 0 y 1 | Casos con datos dentro de la ventana y un día fuera; objetivo `as_of` + 1 con cierre fresco; cierre de hace 4 días; valor justo en el borde del rango; p = 0 y 1; fuente que siempre falla (puntos 0) |
| H-08 | baja | `config/por_defecto.yaml`, `fiabilidad_fuentes.prob_sin_declarar` | El comentario dice 0,7 «más probable que no», y la banda «más probable que no» de `bandas_verbales` tiene `prob_interna` 0,65. Además, la FUE- sale con `calc_id: null`, cuando el esquema de F6 (4.5) lo nombra y las demás métricas del Evaluador pasan por el Motor (FC-EVAL-001) | Usar la `prob_interna` de la banda (o explicar en INC-T125-01 por qué 0,7) y pasar el cálculo por el Motor o decir por qué no |

## Invariantes

- Sin LLM en la ruta: la FUE- y el CT-19 son deterministas. ✔
- Falla cerrado y valida antes de mutar: **no del todo** (H-02 tumba el C5; H-04 acepta cualquier `ref_id`). ✗
- Números: los de la fórmula salen de la configuración (k, neutro y máximo citan el esquema de F6; el resto `[PROPUESTO]`). ✔, con la nota de H-08.
- Decisiones del operador: las `[PROPUESTO]` están en INC-T125-01, salvo el trato del registro tardío (H-03). ✗ (menor)
- Secretos y datos personales: nada (los gates en verde). ✔
- Documentación: el análisis atribuye al simulador lo que es del ejecutor (H-01). ✗

## Lo que no comprobé

- mypy y el gate completo (`check_all.sh`), por el encargo; A-Forex y B.
- Que el Buscador use la FUE- (fuera del ejecutor).

## Veredicto

**NO APTO** · H-01 (alta): la función nueva no se alcanza en ningún ciclo, porque el ejecutor pierde el bloque `pronostico_fuente` al construir las piezas, y la documentación lo atribuye al cliente simulado. CA-4 no se cumple (H-02: una fecha con zona tumba el C5 en cada ciclo). Tras la corrección, volver a ejecutar `r01_01`, `r01_02` y `r01_03`.

## Ronda r02

- **Revisor:** revisor nuevo sin contexto de la implementación (subagente de Claude; no es el de la r01 ni quien implementó) · 2026-11-15
- **Copia revisada:** clon desconectado en `41c0ea4` (wip local con T-125 r02, T-116 r05 y T-126 r02). Mutantes y la versión anterior (`fb3ccd4`, para comparar) en copias desechables con «qa10_mut» en la ruta, ya borradas.
- Opinión formada con el código (`orquestacion.py`: `_bloque_pronostico_fuente`, `_tipo_con_pronostico_fuente`; `evaluador.py`: `motivo_pronostico_fuente_no_registrable`, `pronosticos_de_fuentes`, `fiabilidad_fuentes`, `_brier_del_motor`), los esquemas de F2 (regla 8 y 4.1) y F6 (4.5) y las pruebas, antes de leer el apartado «Ronda r02» de `analisis-tecnico.md`.

### Reproducción

| Qué | Orden | Resultado |
| --- | --- | --- |
| Suite completa de A, una vez | ver `T-116/qa.md`, ronda r05 | dentro de la suite |
| Goldens, ruff, mypy A, gates ligeros | ver `T-116/qa.md`, ronda r05 | coinciden · 2902 · 109 · los cuatro con 0 |
| Las 12 pruebas de la r01 «cambiaron sus datos, no sus afirmaciones» | `git diff fb3ccd4 41c0ea4 -- bloque_a/11_Ejecutor/tests/test_t125_fiabilidad_fuentes.py` | **cierto**: los `assert` son los mismos salvo el nombre de las constantes (`REF-0001` → `FUENTE_A = "REF-RF-0001"`, `REF-0002` → `FUENTE_B = "REF-RF-0003"`); cambia el sembrado (`_escribir_clm` registra cada pieza el día de su emisión). Un matiz: en `test_pb46_no_se_resuelve_…` el caso «emitido después de su fecha objetivo» se registra el 2025-01-01, antes de su emisión, así que cae por dos reglas a la vez (no es una prueba aislada de la regla) |
| Scripts de la r01, tal cual | desde `bloque_a/11_Ejecutor`: `QA_TMP=<tmp> python ../../.docs/tickets/T-125/revisores/r01_01_ataques_fiabilidad.py` y `r01_03_camino_de_entrada_a_f2.py` | `r01_01`: A1–A8 dan 0 (siembran `REF-0001` con el reloj en `AS_OF`: ahora no cuentan por H-03 y H-04, que es lo correcto); A6b: un ciclo con una pieza con zona da la evaluación completa y ninguna incidencia HERRAMIENTA; A7 determinismo `True`; A9 `(0.65, 0.65)`. `r01_03`: 0 con bloque (su bloque tiene otra fuente que la de la pieza: se rechaza) |
| Script del implementador | `QA_TMP=<tmp> python ../../.docs/tickets/T-125/r02_camino_de_entrada_a_f2.py` | 8 CLM con bloque y, un ciclo después, FUE- de REF-RF-0001 (n 8, 12,4 puntos, `CALC-2026-0021`) comunicada por CT-19 y anotada, como dice `pruebas.md` |
| Mutantes de la r01, tal cual | desde la raíz: `python .docs/tickets/T-125/revisores/r01_02_mutantes.py <copia «qa10_mut»>/bloque_a` | 6 de 14 muertos (igual que en la r01: el script fija las 12 pruebas de la r01) |
| Los mismos, con `test_t125_r02.py` | `python .docs/scripts/mutantes_revisor_ampliado.py .docs/tickets/T-125/revisores/r01_02_mutantes.py <copia>/bloque_a tests/test_t125_r02.py` | **13 de 14 muertos**; K08 vivo. Comprobado a mano que es equivalente: con `emision <= registro < objetivo` (H-03), `emision < objetivo` ya no puede fallar |
| Ataques nuevos en ciclos | `QA_TMP=<tmp> python ../../.docs/tickets/T-125/revisores/r02_01_ataques_ciclo.py` | abajo |
| Ciclos sin bloque, antes y después | desde el `11_Ejecutor` de cada versión: `QA_TMP=<tmp> python <ruta>/r02_02_ciclos_sin_bloque.py > salida.json`, y `cmp` | abajo |

### Camino entero en vivo y ataques (`revisores/r02_01_ataques_ciclo.py`, ejecutado)

| Bloque | Qué | Obtenido | Juicio |
| --- | --- | --- | --- |
| B01 | El Analista simulado da en cada finalista 4 pronósticos de REF-RF-0001 (dos aciertos seguros, dos fallos seguros, p = 0,8); ciclos el 2026-04-03 y el 2026-06-05 | C1: 16 CLM PRONOSTICO_FUENTE con su bloque, registradas el 2026-04-03, ninguna FUE-. C2: FUE- (n 16, 8 aciertos, BSS −0,36, 8,4 puntos). BSS a mano −0,360000 = FUE-; `calc_id` CALC-2026-0021 en RC con `FC-EVAL-001` y solicitante AG-20; CT-19 a AG-16 `MSG-2026-000008`, anotado en la FUE- | correcto (H-01 y H-08 corregidos); la entrada de RC va **sin `run_id`** (H-13) |
| B02 | Determinismo: B01 en dos almacenes | FUE- y bloques de F2 idénticos | correcto |
| B03 | Fechas raras en el alta (`motivo_pronostico_fuente_no_registrable`) | `''`, `NaT`, `None`, `tomorrow`, `yesterday`: fuera. **Registrables:** objetivo `now`, `2026-07`, `July 1 2026`, `20260701`, `9999-12-31`. `1/7/2026` se lee 7 de enero | H-10 |
| B04 | Lecturas de `_fecha_de_calendario` | `now` y `today` → **la fecha de la máquina** (2026-11-15); `1/7/2026` → 2026-01-07; `2026` → 2026-01-01. Emisión «today» con registro a +3 días y objetivo a +10 de hoy: REGISTRABLE (otro día, otra fecha de emisión) | H-10 |
| B05 | Registro tardío en el ciclo: objetivo hoy, ayer; emitido mañana; objetivo mañana | solo entra «objetivo mañana»; los otros, rechazados en HA con su motivo | correcto (H-03) |
| B06 | Fuentes falsas en el ciclo: otra fuente de F9 en el bloque, F7, `REF-RF-9999`, `HT-01:` con bloque de F9, dirección `{"x": 1}`, serie `["SPY"]` | ninguna entra; seis motivos distintos en HA; ciclo COMPLETO | correcto (H-04) |
| B07 | Duplicados en un ciclo: el mismo bloque con dos textos, con umbral `1` en vez de `1.0` y con la fecha con hora | cuentan **2 por serie** (lo esperado: 1): la del umbral entero no se deduplica | H-11 |
| B08 | El mismo pronóstico citado en dos ciclos con textos distintos | uno por serie | correcto (H-05) |
| B09 | El Buscador trae pronósticos de sus referencias | backtest: 0 con bloque, 0 rechazos (como dicen INC-T125-01 y el mapa); vivo: 2 con bloque (REF-RF-0342, REF-RF-0343) | correcto |
| B10 | F2 manipulado: un bloque con `direccion` lista (no hashable) junto a 6 pronósticos sanos de otra fuente | `fiabilidad_fuentes` lanza `TypeError: unhashable type: 'list'`: se pierde la FUE- de la fuente sana (en el ciclo, el `try` lo deja en `[]` con incidencia, y se repite en cada ciclo) | H-12 |
| B11 | En un ciclo, objetivos `now`, `1/7/2026` y `July 1 2026` | **`now` y `July 1 2026` quedan guardados en F2**; `1/7/2026` se rechaza como «emitido en su fecha objetivo o después» (leído como 7 de enero) | H-10 |
| B12 | El campo `variable` | Un bloque **sin `variable`** es registrable; con `variable: rentabilidad_12m` también. Cinco pronósticos «rentabilidad a 12 meses de SPY > 0,05» se resuelven con **el cierre** (≈ 123): los cinco «aciertan» y la fuente sale con 11,92 puntos | H-09 |

### Ciclos que no traen el bloque (`revisores/r02_02_ciclos_sin_bloque.py`, ejecutado con `fb3ccd4` y con `41c0ea4`)

Tres escenarios (backtest de RV, dos ciclos en vivo de RV y el ciclo de las doce clases): **la última huella y el número de entradas de cada archivo del almacén (F1–F11, HA, RC…) y la SHA-256 de cada entregable coinciden byte a byte** entre las dos versiones. La única diferencia es el resumen de `Bloque.estado()`, y viene de las latencias medidas con el reloj de la máquina (`W_medio_s`, `latencia_s`), no del código nuevo (comprobado con un `diff` del `estado()` tras un ciclo). Nada de T-125 cambia los ciclos sin pronósticos de fuentes.

### Hallazgos de la r01

| ID | Estado | Evidencia |
| --- | --- | --- |
| H-01 (alta) | **corregido** | B01, B09; K01 muere con las pruebas nuevas |
| H-02 (media) | **corregido** en lo que pedía | A6b de `r01_01`; las fechas con zona no lanzan. Pero la lectura de fechas sigue siendo laxa (H-10) |
| H-03 (media) | **corregido** | B05; A1 de `r01_01` da 0 |
| H-04 (media) | **corregido** | B06; A2 de `r01_01` da 0 |
| H-05 (baja) | **corregido en parte** | B07, B08; queda el umbral `1` / `1.0` (H-11) |
| H-06 (baja) | **corregido** | `test_r02_h06_…` (y K04 muere) |
| H-07 (baja) | **corregido** | K05–K07 y K11–K13 mueren; K08 equivalente |
| H-08 (baja) | **corregido** | 0,65 = banda; B01: Brier del Motor con su `calc_id` (sin `run_id`: H-13) |

### Hallazgos nuevos

| ID | Gravedad | Cómo reproducirlo | Esperado / obtenido | Corrección sugerida |
| --- | --- | --- | --- | --- |
| H-09 | **media** | `r02_01_ataques_ciclo.py`, B12 | Esperado (esquema de F2, 4.1: el bloque es `{ref_id, variable, serie_ht01, …}`; docstring de `motivo_…`: «se exige el bloque completo y bien formado»; CA-4: lo mal formado no cuenta): un bloque sin `variable`, o con una variable que el Evaluador no sabe resolver, no entra. Obtenido: `variable` no se lee en ningún sitio; el Evaluador resuelve siempre contra el **cierre** de `serie_ht01`. Un pronóstico «rentabilidad a 12 meses > 5 %» acierta siempre (cierre ≈ 123 > 0,05) e infla la fiabilidad de la fuente, que se comunica al Buscador por CT-19 | Exigir `variable` y aceptar solo las que se resuelven (hoy, `cierre`), con el resto rechazado en HA con su motivo; prueba con `variable` ausente y con otra variable. `[PROPUESTO]` en INC-T125-01 si se amplía |
| H-10 | **media** | `r02_01`, B03, B04 y B11 | Esperado (docstring de `_fecha_de_calendario`: «un texto ISO 8601»; invariante: determinista y falla cerrado): solo fechas ISO. Obtenido: `pd.Timestamp` acepta palabras relativas y formatos libres: `now`/`today` se leen con **el reloj de la máquina** (el mismo F2 da otra fecha otro día: no determinista, y un objetivo «now» flota con la fecha de la evaluación); `July 1 2026`, `2026-07`, `20260701` entran; `1/7/2026` se lee como 7 de enero. `now` y `July 1 2026` llegan a F2 en un ciclo | Leer con `datetime.date.fromisoformat` / `datetime.fromisoformat` (o una expresión regular `AAAA-MM-DD` con hora y zona opcionales) y rechazar lo demás; pruebas con `now`, `today`, `1/7/2026` y `July 1 2026` |
| H-11 | baja | `r02_01`, B07 | El mismo pronóstico con umbral `1` y `1.0` (o `[1, 2]` y `[1.0, 2.0]`) cuenta dos veces: la clave de deduplicación usa `repr(umbral)` | Normalizar el umbral a `float` (o tupla de `float`) en la clave |
| H-12 | baja | `r02_01`, B10 | Esperado (INC-T125-01: «falla por pronóstico, no por run»): una entrada rara de F2 se omite. Obtenido: con `direccion` no hashable (solo en un F2 manipulado o antiguo; el alta la rechaza), `clave in vistos` lanza `TypeError` antes de validar la dirección y se pierde la FUE- de todas las fuentes en cada ciclo | Validar dirección y umbral antes de formar la clave (o envolver cada pieza); prueba |
| H-13 | baja | `r02_01`, B01 (`run_id` de la entrada de RC) | El esquema de RC (`msg_id` / `run_id` · `query_id`: «Sí», trazabilidad) pide ligar el cálculo a la ejecución; el de la FUE- entra con `run_id` y `msg_id` nulos (el otro cálculo del Evaluador, en `resolver`, pasa el `run_id`) | Pasar el `run_id` del C5 a `fiabilidad_fuentes` y a `_brier_del_motor` |

### Criterios de aceptación

| Criterio | Cumple | Evidencia |
| --- | --- | --- |
| CA-1 · dos fuentes de 25, fórmula, > 10 y < 10 | sí | `test_pb46_dos_fuentes_…` (afirmaciones sin cambios); B01: BSS del Motor = BSS a mano |
| CA-2 · en un ciclo, la FUE- en F6 con el `msg_id` del CT-19 a AG-16 | **sí, ahora de verdad** | B01 (camino Analista → F2 → FUE- → CT-19 en ciclos en vivo), B09 (Buscador) |
| CA-3 · una vez al mes; sin muestra, nada | sí | K04, K10 mueren; H-06 corregido |
| CA-4 · no vencidos, mal formados o sin dato no cuentan; las cuatro direcciones | **no** | Un bloque sin `variable` (mal formado según el esquema de F2) cuenta y se resuelve contra el cierre (H-09); fechas no ISO y relativas (`now`, `July 1 2026`) entran y cuentan (H-10). Lo demás, bien (B03, B05, B06, mutantes) |
| CA-5 · sin pronósticos de fuentes el ciclo no cambia; goldens, ruff, mypy | sí | `r02_02`: byte a byte igual que `fb3ccd4`; goldens coinciden; ruff 2902; mypy 109 (el gate completo no lo pasé) |

### Invariantes

- Sin LLM en la ruta: alta, resolución, FUE- y CT-19 son código. ✔ Determinismo: sí entre ejecuciones (B02), **salvo las fechas relativas**, que dependen del reloj de la máquina (H-10). ✗ (menor)
- Falla cerrado y valida antes de mutar: el alta valida casi todo (B05, B06), pero no `variable` (H-09) ni el formato de fecha (H-10). ✗
- Números: de la configuración; 0,65 de la banda. ✔
- Decisiones del operador: INC-T125-01 ampliada `[PROPUESTO]` y fila en `Decisiones_del_operador_Bloque_A.md`. ✔
- Secretos: gates en verde; mis scripts no llevan ninguno. ✔
- Documentación: el análisis técnico ya no atribuye al simulador lo que era del ejecutor; el mapa de PB-46 declara el límite del backtest. ✔

### Lo que no comprobé

- El gate completo (`check_all.sh`), B (encargo).
- Que el Buscador use la FUE- y recalifique F9 (modelo real).
- El esquema de las respuestas de los agentes (`contratos.py`) no declara `pronostico_fuente`; no lo he cambiado ni medido más allá de que lo deja pasar.

## Veredicto (r02)

**NO APTO** · Los hallazgos de la r01 están corregidos (H-01, el alto, también: el pronóstico de una fuente viaja del Analista y del Buscador a F2 y, vencido, sale en la FUE- con el Brier del Motor y su `calc_id`, comunicado por CT-19; los ciclos sin el bloque no cambian ni un byte; 13 de 14 mutantes mueren y el que vive es equivalente). Pero CA-4 sigue sin cumplirse: el alta acepta bloques sin `variable` y el Evaluador resuelve cualquier variable contra el cierre (H-09, media), y la lectura de fechas acepta `now`/`today` (reloj de la máquina) y formatos no ISO (H-10, media). Tras corregirlo, volver a ejecutar `r02_01_ataques_ciclo.py` (B03, B04, B07, B10, B11 y B12 deben cambiar) y `r02_02_ciclos_sin_bloque.py`.

## Ronda r03

- **Revisor:** revisor nuevo sin contexto de la implementación (subagente de Claude; no es el de la r01 ni el de la r02, ni quien implementó) · 2026-11-15
- **Copia revisada:** clon desconectado en `4125525` (instantánea con T-125 r03). Versión anterior (`5098b09`, la de la r02) y mutantes, en copias desechables extraídas con `git archive` dentro del scratchpad («qa12_prev» y «qa12_mut»), ya borradas.
- Opinión formada con el diff de la r03 (`evaluador.py`: `RE_FECHA_ISO`, `_fecha_de_calendario`, `variable_resoluble`, `motivo_pronostico_fuente_no_registrable`, `pronosticos_de_fuentes`, `fiabilidad_fuentes`/`_brier_del_motor` con `run_id`; `orquestacion.py`, `_tipo_con_pronostico_fuente`; `por_defecto.yaml`), el esquema de F2 (regla 8 y 4.1, que no enumera los valores de `variable`) y las pruebas, antes de leer el apartado «Ronda r03» de `analisis-tecnico.md`.

### Reproducción

| Qué | Orden | Resultado |
| --- | --- | --- |
| Suite completa de A, una vez | `cd bloque_a/11_Ejecutor && python -m pytest -q -p no:cacheprovider` | **5968 passed** en 27 min 24 s (línea base 607) |
| Goldens de contratos | `python tests/goldens_ct.py` | «goldens de contratos: coinciden» |
| ruff (tres `11_Ejecutor`, desde la raíz) | `ruff check --output-format=concise … \| wc -l` | 2838 (cuota 2838) |
| mypy de A, como el gate | `mypy bloque_a --ignore-missing-imports --no-error-summary \| wc -l` | 109 (cuota 109) |
| Gates ligeros | `tools/secrets_scan.py`, `refs_vivas.py`, `nfc_check.py`, `corpus_integridad.py` | los cuatro en verde (695 archivos del corpus coinciden) |
| Script de la r02, tal cual | desde `bloque_a/11_Ejecutor`: `QA_TMP=<tmp> python ../../.docs/tickets/T-125/revisores/r02_01_ataques_ciclo.py` | B01–B03 bien y **se para en B04** con `ValueError: fecha no ISO 8601: 'now'`. Es lo esperado: B04 llamaba a `_fecha_de_calendario("now")` dando por hecho que devolvía una fecha; ahora falla cerrado, que es lo que pedía H-10 |
| La r02 con B04 adaptado | `QA_TMP=<tmp> python ../../.docs/tickets/T-125/revisores/r03_01_r02_con_b04_adaptado.py` (ejecuta el fichero de la r02 sin tocarlo, con solo B04 sustituido en memoria) | abajo |
| Ataques nuevos | `QA_TMP=<tmp> python ../../.docs/tickets/T-125/revisores/r03_02_fechas_variables_y_numeros.py` | abajo |
| Ciclo tras el desbordamiento | `QA_TMP=<tmp> python ../../.docs/tickets/T-125/revisores/r03_03_ciclo_tras_desbordamiento.py` | abajo (H-14) |
| Ciclos sin bloque, antes y después | desde el `11_Ejecutor` de `5098b09` y de `4125525`, con el mismo `QA_TMP`: `python <ruta>/r02_02_ciclos_sin_bloque.py > salida.json`, y `diff` | abajo |
| Mutantes de la r03 | desde la raíz: `python .docs/tickets/T-125/revisores/r03_04_mutantes.py <copia «qa12_mut»>/bloque_a` | abajo |

### La r02 otra vez (`revisores/r03_01_r02_con_b04_adaptado.py`, ejecutado)

| Bloque | r02 | r03 | Juicio |
| --- | --- | --- | --- |
| B01 | FUE- de REF-RF-0001 (n 16, BSS −0,36, 8,4 puntos); RC **sin `run_id`** | igual, y la entrada de RC lleva `RUN-2026-0002`, el run del ciclo | H-13 corregido |
| B02 | determinista | determinista | correcto |
| B03 | `now`, `2026-07`, `July 1 2026`, `20260701` registrables; `1/7/2026` leído 7 de enero | todos rechazados («faltan campos del bloque o una fecha no se lee»); siguen registrables `2026-07-01T23:00-12:00` (ISO) y `9999-12-31` (ISO, no se resuelve nunca: no cuenta) | H-10 corregido |
| B04 (adaptado) | `now`/`today` con el reloj de la máquina | `now`, `today`, `tomorrow`, `1/7/2026`, `July 1 2026`, `2026`, `2026-07`, `20260701`, `2026/07/01`, `01-07-2026`: todos `ValueError`; emisión «today»: rechazada | H-10 corregido |
| B05, B06, B08, B09 | correctos | iguales (B06 rechaza ahora la dirección `{"x": 1}` con «dirección no reconocida») | correcto |
| B07 | 2 por serie (umbral `1` frente a `1.0`) | **4 para 4 series** | H-11 corregido |
| B10 | `TypeError: unhashable type: 'list'` y se pierde la FUE- sana | FUE- de REF-RF-0001 | H-12 corregido |
| B11 | `now` y `July 1 2026` guardados en F2 | ninguno en F2; rechazos en HA | H-10 corregido |
| B12 | sin `variable` registrable; «rentabilidad_12m > 0,05» acierta con el cierre (11,92 puntos) | sin `variable`: rechazado; `rentabilidad_12m`: «no resoluble con el cierre de la serie (solo nivel, cierre, precio)»; en F2 manipulado, 0 resueltos y ninguna FUE- | H-09 corregido |

### Ataques nuevos (`revisores/r03_02_fechas_variables_y_numeros.py`, ejecutado)

| Bloque | Qué | Obtenido | Juicio |
| --- | --- | --- | --- |
| N01a | ISO válidas: fecha, con espacios alrededor, con hora, segundos, microsegundos, `+05:00`, `Z`, `+0500`, `-12:00` | las nueve se leen como 2026-07-01 | correcto |
| N01b | En un ciclo, objetivos con hora (`…T16:00`), con zona (`…T16:00:00+02:00`, emisión `…T08:00Z`) y con `Z` | 12 en F2, ningún rechazo, los 12 cuentan y se resuelven | correcto: las ISO con hora y zona siguen entrando |
| N02a | Formatos que aún pasan el filtro | **cifras de ancho completo (`２０２６-０７-０１`), árabes orientales y devanagari** se leen y son registrables (el `\d` de `re` es Unicode); `2026-07-01-05:00` (zona sin hora, no es ISO) también; `9999-12-31` registrable (no cuenta nunca); `0001-01-01` como emisión se lee | H-16 (baja) |
| N02b | En un ciclo, fecha objetivo en cifras de ancho completo | se guarda **tal cual** en F2 (`２０２６-０４-０８`) y cuenta (4 resueltos) | H-16 (baja): determinista y sin ambigüedad, pero no es ISO y queda así en el registro |
| N03a | Variables: `CIERRE`, `" precio\n"`, `Nivel`, `nivel ` → sí; `cierre​`, `cierre_ajustado`, `rentabilidad`, `close`, `c`, `""`, `None`, `1`, `["cierre"]` → no | correcto (falla cerrado) |
| N03b | `variables_nivel` mal formada | texto `"cierre"`: **la variable `c` es registrable** (se recorre letra a letra); `[]`: nada registrable; número `5`: **`TypeError`** en el alta | H-17 (baja) |
| N03c | Configuración propia con `variables_nivel: [cierre]` en un ciclo | el alta del ciclo la respeta: solo `cierre` en F2 y `precio` rechazado en HA con su motivo | correcto (pero sin prueba: M14 vive) |
| N03d | Se estrecha la lista después de registrar | 8 cuentan con la de por defecto, 4 con `[cierre]` | correcto (conservador) |
| N04a | Alta con un entero de 400 cifras (JSON válido: `json.loads` lo lee como `int`) | umbral, rango `[0, 10^400]` y probabilidad: **`OverflowError: int too large to convert to float`** (`_numero_finito` y `_prob_valida` → `math.isfinite`); `1e400` (inf) y `True`: rechazados con motivo | H-14 |
| N04b | El mismo umbral, devuelto por el Analista en un ciclo | **el ciclo entero lanza `OverflowError`** (`ciclo` → `_registrar_evidencia_clase` → `_tipo_con_pronostico_fuente` → `motivo_…`): ni estado, ni entregables, ni incidencia en HA | H-14 |
| N04c | F2 manipulado: seis pronósticos sanos y uno con umbral de 400 cifras | `fiabilidad_fuentes` lanza `OverflowError` y se pierde la FUE- de la fuente sana (en el ciclo, el `try` del C5 la deja en `[]` con incidencia, y se repite cada ciclo) | H-15 (baja, la misma clase que H-12) |
| N05 | Rangos `[a, b]` enteros y decimales; `[0, 1e9]`, `[-0.0, 1e9]`, `[0.0, 1e9]` | cuentan dos | correcto (H-11) |

### Ciclo tras el desbordamiento (`revisores/r03_03_ciclo_tras_desbordamiento.py`, ejecutado)

C1 con el umbral de 400 cifras: `OverflowError`; quedan en el almacén 2 entradas de F2, 9 de F10 y 6 de RC del run a medias, sin cierre del run; `verificar_integridad()` da todo `True`. C2, en el mismo almacén y con respuestas normales: COMPLETO (`RUN-2026-0002`), integridad `True`. No se repite (el bloque no llegó a F2), pero cada respuesta así tumba su ciclo. Con `5098b09` (la versión de la r02) el ciclo cae igual: viene de la r02 (el alta de T-125), no de la r03; antes de T-125 el bloque no se leía y no tumbaba nada.

### Ciclos que no traen el bloque (`revisores/r02_02_ciclos_sin_bloque.py`, con `5098b09` y con `4125525`)

En los tres escenarios, **la última huella y el número de entradas de cada archivo del almacén y la SHA-256 de cada entregable coinciden** entre las dos versiones. Solo difiere la huella del resumen de `Bloque.estado()`, y difiere también entre **dos ejecuciones de la misma versión** (`4125525` contra sí misma): son las latencias del reloj de la máquina, como vio la r02. La r03 no cambia los ciclos sin pronósticos de fuentes.

### Mutantes (`revisores/r03_04_mutantes.py`, contra `test_t125_r03.py`, `test_t125_r02.py` y `test_t125_fiabilidad_fuentes.py`)

| Mutante | Qué rompe | Resultado |
| --- | --- | --- |
| M01 | sin el filtro ISO | MUERTO |
| M02 | el filtro admite AAAAMMDD | MUERTO |
| M03 | el filtro sin zona horaria | MUERTO |
| M04 | cualquier variable es resoluble | MUERTO |
| M05 | variable sin `strip` | MUERTO |
| M06 | variable sin `lower` | MUERTO |
| M07 | el Evaluador no mira la variable | MUERTO |
| M08 | el Evaluador no mira si la dirección es texto | VIVO · equivalente: una lista o un dict no está en `("por_encima", …)` (la tupla compara con `==`, sin hash) y cae en `else: continue`; la clave se forma después |
| M09 | el alta no mira la variable | MUERTO |
| M10 | el alta no mira si la dirección es texto | VIVO · equivalente, por lo mismo (cae en «dirección no reconocida») |
| M11 | deduplicación con `repr(umbral)` | MUERTO |
| M12 | el C5 no pasa el `run_id` a `fiabilidad_fuentes` | **VIVO** (H-18): `test_h13_…` llama a `fiabilidad_fuentes(AS_OF, "RUN-…")` directamente; ninguna prueba mira el `run_id` de RC en un ciclo (B01 sí lo muestra) |
| M13 | la petición al Motor sin `run_id` | MUERTO |
| M14 | el alta del ciclo usa la lista por defecto y no la de la configuración | **VIVO** (H-18): ninguna prueba cambia `variables_nivel` en un ciclo (N03c muestra que funciona) |
| M15 | la fecha sin `strip` antes del filtro | VIVO · más estricto (rechaza `" 2026-07-01"`): conservador |
| M16 | la lista de la configuración sin `lower` | VIVO · equivalente con la configuración de por defecto (en minúsculas) |

Resumen: 10 de 16 muertos; de los 6 vivos, 3 equivalentes (M08, M10, M16), 1 conservador (M15) y 2 huecos de prueba (M12, M14).

### Hallazgos de la r02

| ID | Estado | Evidencia |
| --- | --- | --- |
| H-09 (media) | **corregido** | B12; N03a; M04, M07 y M09 mueren |
| H-10 (media) | **corregido** en lo que pedía | B03, B04 (adaptado) y B11; N01a/N01b (las ISO con hora y zona siguen leyéndose); M01–M03 mueren. Queda el `\d` Unicode (H-16, baja) |
| H-11 (baja) | **corregido** | B07; N05; M11 muere |
| H-12 (baja) | **corregido** | B10; queda la misma clase con un entero enorme (H-15) |
| H-13 (baja) | **corregido** | B01 (`RUN-2026-0002` en RC); M13 muere (M12 vive: H-18) |

### Hallazgos nuevos

| ID | Gravedad | Cómo reproducirlo | Esperado / obtenido | Corrección sugerida |
| --- | --- | --- | --- | --- |
| H-14 | **media** | `r03_02`, N04a y N04b; `r03_03` | Esperado (INC-T125-01: «falla por pronóstico, no por run»; valida antes de mutar): un bloque con un umbral o una probabilidad que no es un número finito representable se rechaza en HA con su motivo y el ciclo sigue. Obtenido: un entero de 400 cifras (JSON válido, lo que `json.loads` de `agentes.py` da con el modelo real; el esquema de la respuesta no declara `pronostico_fuente`) lanza `OverflowError` en `_numero_finito`/`_prob_valida` y **tumba el ciclo entero** a mitad, con entradas de F2, F10 y RC ya escritas y el run sin cerrar (la cadena de huellas sigue íntegra y el ciclo siguiente acaba bien). Viene de la r02; la r03 no lo toca. Mismo camino para la referencia del Buscador | En `_numero_finito` y `_prob_valida`, capturar `OverflowError` (o comparar enteros sin pasar a `float`) y devolver `False`; envolver el alta de cada pieza para que un fallo raro la rechace en HA en vez de tumbar el ciclo; prueba con `10**400` en umbral, rango y probabilidad, en el alta y en un ciclo |
| H-15 | baja | `r03_02`, N04c | Lo mismo en `pronosticos_de_fuentes` con un F2 manipulado o antiguo: `math.isfinite(10**400)` lanza y se pierde la FUE- de todas las fuentes en cada ciclo (la clase de H-12) | La misma corrección de H-14 (usar `_numero_finito` también aquí); prueba |
| H-16 | baja | `r03_02`, N02a y N02b | El docstring y INC-T125-01 dicen «solo ISO 8601». `\d` de `re` admite cifras Unicode (ancho completo, árabes orientales, devanagari), que pandas lee bien y que quedan **tal cual** en F2; también pasa una zona sin hora (`2026-07-01-05:00`). No es ambiguo ni depende del reloj | `re.compile(..., re.ASCII)` o `[0-9]`; la zona solo detrás de la hora; prueba con `２０２６-０７-０１` |
| H-17 | baja | `r03_02`, N03b | `fiabilidad_fuentes.variables_nivel` no se valida: un texto (`cierre`) se recorre letra a letra y hace registrable la variable `c`; un número lanza `TypeError` en el alta (tumba el ciclo). Es configuración del operador, pero T-122 fijó que una configuración mal formada falle al crear el Evaluador | Validar al crear el Evaluador (lista no vacía de textos), como `lecciones_por_encargo`; prueba |
| H-18 | baja | `r03_04`, M12 y M14 | Las dos conexiones del ciclo que añade la r03 (el `run_id` del C5 a `fiabilidad_fuentes` y la lista de la configuración al alta en `orquestacion.py`) no tienen prueba: se pueden quitar sin que falle ninguna. Hoy funcionan (B01, N03c) | Una prueba de ciclo que mire el `run_id` de la entrada de RC de la FUE- y otra con `variables_nivel: [cierre]` que rechace `precio` |

### Criterios de aceptación

| Criterio | Cumple | Evidencia |
| --- | --- | --- |
| CA-1 · dos fuentes de 25, fórmula, > 10 y < 10 | sí | `test_pb46_dos_fuentes_…` en la suite; B01: BSS del Motor = BSS a mano |
| CA-2 · en un ciclo, la FUE- en F6 con el `msg_id` del CT-19 a AG-16 | sí | B01 (`MSG-2026-000008` anotado), B09 |
| CA-3 · una vez al mes; sin muestra, nada | sí | suite; mutantes K04 y K10 de la r01/r02 no tocados por la r03 |
| CA-4 · no vencidos, mal formados o sin dato no cuentan; las cuatro direcciones | **sí** | B03, B04, B11, B12, N01–N05: lo mal formado no cuenta y las ISO válidas sí. El entero enorme tampoco cuenta, pero tumba el ciclo en vez de rechazarse (H-14, media, no del criterio sino de la robustez) |
| CA-5 · sin pronósticos de fuentes el ciclo no cambia; goldens, ruff, mypy | sí | `r02_02`: almacén y entregables iguales byte a byte que `5098b09`; goldens coinciden; ruff 2838; mypy 109; gates ligeros en verde (el `check_all.sh` completo no lo pasé, por el encargo) |

### Invariantes

- Sin LLM en la ruta: alta, resolución, FUE- y CT-19 son código. ✔ Determinismo: las fechas ya no dependen del reloj de la máquina (B04). ✔
- Falla cerrado y valida antes de mutar: sí para fechas, variables, direcciones y umbrales normales; **no** con un entero enorme, que tumba el ciclo a mitad (H-14) o la FUE- de todas las fuentes (H-15). ✗ (media)
- Números: `variables_nivel` en la configuración, `[PROPUESTO]` en INC-T125-01 y en `Decisiones_del_operador_Bloque_A.md`. ✔ (sin validar: H-17)
- Decisiones del operador: las de la r03 están como `[PROPUESTO]` (INC-T125-01, ronda r03). ✔
- Secretos y datos personales: gates en verde; mis scripts no llevan ninguno ni identificadores de modelo. ✔
- Documentación: README del ticket, `analisis-tecnico.md`, `pruebas.md`, INC-T125-01, mapa de PB-46, evidencias y deuda técnica al día con la r03. ✔

### Lo que no comprobé

- El gate completo (`./tools/check_all.sh`), B (encargo).
- Que el Buscador use la FUE- y recalifique F9 (modelo real), ni una respuesta real del modelo con un número enorme: lo reproduje con el cliente simulado parcheado, sobre el mismo camino (`json.loads` sin `parse_int` en `agentes.py` lo permite).
- Otros caminos del ciclo con enteros enormes fuera de T-125.

## Veredicto (r03)

**APTO** · Los cinco hallazgos de la r02 están corregidos (H-09 y H-10, los medios, con sus pruebas y mutantes muertos): `variable` obligatoria y resoluble con el cierre, fechas solo ISO 8601 (las de hora y zona siguen entrando, también en un ciclo), umbral comparado como número, dirección no textual descartada sin excepción y `run_id` en RC. Los cinco criterios se cumplen, los ciclos sin el bloque no cambian ni un byte y la suite completa pasa (5968). Queda abierto **H-14 (media)**: un entero de 400 cifras en el umbral o la probabilidad de un bloque tumba el ciclo entero en el alta (viene de la r02); y H-15 a H-18 (bajos). Según `ri-qa`, sin críticos ni altos abiertos es APTO, y H-14 a H-18 pasan a la deuda técnica con su ID (o se corrigen antes de cerrar, si el operador lo prefiere: H-14 y H-15 son la misma corrección de pocas líneas). El cierre (estado CERRADO, deuda, diario, memoria y commit) queda para quien coordina: este revisor solo escribe en `qa.md` y `revisores/`.
