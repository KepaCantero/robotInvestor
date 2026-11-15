# T-146 · Análisis técnico

## Causa raíz (de T-145)

`Bloque._invocar` llamaba si `Presupuesto.puede(bolsa, estimado)`, con `estimado = _estimar_uc(agente, mensaje)`: el encargo medido más 1 500 tokens, el system prompt **como lectura de caché** y **2 500 tokens de salida**, sin reparación ni continuaciones; lo real se cargaba **después**. Además: (1) la escritura de caché de los agentes compartidos (AG-10, AG-11, AG-12, AG-14, AG-16) se cargaba como lectura hasta `liquidar_primas`, que después repartía **toda** la escritura de la fase; (2) AG-18, AG-19 y AG-20 se llamaban sin presupuesto; (3) las búsquedas web no contaban en UC. Con el peor caso, una bolsa acababa muy por encima de su límite.

## Lo que dice el Documento 0 (solo lo necesario)

- §10.3: cada ciclo y cada petición tienen un presupuesto en UC repartido por fases y clases; ampliar más del 25 % exige autorización (el Orquestador en el ciclo periódico); sin respuesta, se cierra con alcance reducido declarado.
- R16: la falta de presupuesto reduce el alcance, nunca la verificación.
- §7.2 y Anexo A: N0 1 UC, N1 5, N2 18 por tipo, N3 50; ciclo semanal ≤ 240 UC; 1 UC ≈ una llamada de 8 000 tokens de entrada y 1 500 de salida; ampliación sin autorización +25 %.
- No dice nada de quién paga el dictamen G3 (AG-18), la auditoría (AG-19) ni el informe de aprendizaje (AG-20), ni cuánto cuesta una búsqueda en UC.

## Diseño implementado

### La reserva petición a petición (`consumo.ReservaLlamada`)

Una por llamada a un agente (`Bloque._invocar` la crea si hay presupuesto). Antes de **cada petición** (el primer intento y cada reparación, en `Agentes.invocar`; cada continuación tras `pause_turn`, dentro de `AnthropicClient.generar`, que recibe la guarda por la variable de contexto `llm._GUARDA`, una por hilo):

1. **Peor caso**: la entrada (system, mensajes y definición de herramientas) medida con 3,6 caracteres por token (`llm._tokens_aprox`), por `presupuesto_uc.reserva.factor_tokens_entrada` (1,35) o por el factor mayor observado en la bolsa, toda como escritura de caché (en la fórmula de UC, la escritura vale como la entrada sin caché: no hay garantía de lectura); `max_tokens` de salida; `max_uses` búsquedas por `uc.uc_por_busqueda_web`. En UC con `Contabilidad.uc_de` (la fórmula del ejecutor).
2. **Si cabe** en `límite − (consumido + reservado + retenido)`, se reserva y la petición sale.
3. **Si no**, la ampliación con la regla del ejecutor (`_solicitar_ampliacion`, su AUT- en HA): se admite en prospectiva, refutación y respuesta a objeciones, como antes, y en los controles (`control=True`: AG-18 y AG-19, por R16), siempre dentro de `asignado × (1 + ampliacion_max_autorizable)`.
4. **Si se deniega**, la petición sale con la salida que cabe, si es al menos `presupuesto_uc.reserva.salida_minima_tokens` (se anota en `Presupuesto.recortes` y en `recortes_salida` del RUN de F5).
5. **Si ni eso**, no sale: en el primer intento, `Agentes.invocar` devuelve `SIN_PRESUPUESTO` sin llamar al cliente y `_invocar` devuelve None (como antes); en una reparación o continuación, la llamada queda PARCIAL (`presupuesto_agotado`, incidencia «Salida no conforme» como cualquier PARCIAL). En los dos casos la fase se cierra declarada (`cierre_parcial`, motivo «presupuesto insuficiente para … (X UC en el peor caso)»).

Después de cada petición, `pagar` suelta su reserva y aparta su coste real (sin comprobar: ya se gastó) para que la siguiente petición de la misma llamada lo vea. Si lo real pasa de lo reservado (el tokenizador o lo que lee una búsqueda), se anota en `excesos_reserva` y la bolsa usa desde entonces el factor observado. Al volver de la llamada, `cerrar` suelta lo apartado y `_cargar` carga lo real con la regla de T-88.

### La escritura de caché (`Bloque._cargar`)

T-88 aplazaba toda la escritura de caché de los agentes compartidos a `liquidar_primas` (para que no dependiera del orden de los hilos). Ahora se aplaza solo la del prefijo compartido, y como mucho la de la primera llamada de la bolsa a ese agente (`diferido = min(escrito, solo)`, con `solo` = lo cacheado en la primera petición); lo demás escrito se carga ya como escritura. La prima «solo» de un agente compartido queda **retenida** en la bolsa (cuenta como ocupado) hasta la liquidación. Como lo aplazado en un grupo nunca pasa de la suma de las primas «solo», la liquidación no carga a ninguna bolsa más de lo que tenía retenido: ninguna pasa de su límite al liquidar. En los ciclos simulados el prefijo solo se escribe en la primera llamada, así que el reparto y las cifras de T-88 no cambian (`test_t88_consumo.py` pasa; `test_r04_h13` cambia la forma de calcular su «base», no el total: la reescritura del prompt se carga ya, no al liquidar).

### AG-18, AG-19 y AG-20

Contra la bolsa **COMÚN**, la de las fases transversales del ejecutor. Una bolsa propia («CONTROL») cambiaría la forma de `presupuesto_por_clase` del CT-05 en los goldens (`formas_flujos_mock.json` lista sus claves), así que no se crea. AG-18 y AG-19 llevan `control=True` (pueden pedir la ampliación). AG-20 corre en C5, antes del reparto del ciclo: corre contra una bolsa COMÚN del tamaño que COMÚN tiene como mínimo (`fraccion_minima_comun × ciclo_semanal_max`, o el `presupuesto_override` de COMÚN) y `Presupuesto.absorber` pasa lo consumido y lo declarado a la bolsa del ciclo. Sin sitio, AG-20 no sale y se declara; las lecciones deterministas siguen.

### Búsquedas y suma del ciclo

`Contabilidad.uc_de` suma `busquedas_web × uc.uc_por_busqueda_web` (y `resumen` las incluye en los tokens sumados). `Presupuesto(asign, cfg, tope_total=ciclo_semanal_max)`: si el reparto pasa del ciclo (N3 forzado en un periódico, un override), cada bolsa se escala para que la suma de los límites con la ampliación máxima no pase de `ciclo_semanal_max × (1 + ampliacion_max_autorizable)`. Con el reparto normal la suma es exactamente el ciclo y la escala es 1.

### Determinismo con hilos (T-88)

Cada bolsa de tipo la usa un solo hilo; COMÚN y la del ciclo V6, el principal. Las reservas, lo retenido y los recortes de una bolsa dependen solo de sus propias llamadas; la escala es fija desde el principio. Los recortes y excesos se ordenan al escribir F5. `test_ca2_determinista_con_hilos_cerca_del_limite` (cuatro tipos, cuatro hilos, todas las bolsas al límite) da el mismo F5 dos veces.

## El peor caso, antes y después (UC por bolsa)

`peor_caso_por_bolsa.py` (cliente real sobre el SDK falso de peor caso, ciclo N2 del 29-03-2024): límite = asignado × 1,25 + ampliado; máximo = asignado × 1,5.

| Escenario | Bolsa | Antes (consumido / límite) | Después (consumido / límite) |
| --- | --- | --- | --- |
| Solo divisas | DIV | **48,36** / 26,30 | **24,87** / 25,09 |
| | COMÚN | 22,69 / 277,50 | 31,39 / 277,50 |
| | Suma de bolsas · gastado | 71,04 · 79,97 (AG-18/19/20 fuera) | 56,26 · 56,26 |
| 12 tipos, 6 hilos | cada tipo | 46,97–57,98 / 22,50–26,46 (las 12 pasan) | 24,00–25,72 / 24,00–25,72 (ninguna pasa) |
| | COMÚN | 23,56 / 30,00 | 32,19 / 32,37 (ampliación de 2,37 para los controles) |
| | Suma de bolsas · gastado | 653,01 · 671,89 (tope del ciclo con +50 %: 360) | 328,27 · 328,27 |

Ningún escenario pasa de 240 × 1,5 = 360 UC, y lo gastado es exactamente lo cargado en las bolsas. Los ciclos terminan PARCIAL con los cierres declarados en el paquete y en F5.

## Los ciclos simulados de siempre (`comparar_ciclos.sh`)

Mismos tres escenarios con el código de antes (19f3f3b) y el de después, en la misma ruta. Diferencias, todas del presupuesto:

| Escenario | Qué cambia | Por qué |
| --- | --- | --- |
| Ciclo de divisas (29-03-2024) | Solo F10 (la configuración trae los parámetros nuevos) y los sellos | — |
| Backtest de divisas (13 ciclos) | Entregables (informes, `senales.csv`, `pronosticos.csv`, `metricas.json`) **iguales**. En las 9 semanas N1, el Analista de divisas sale con 11 785–11 820 tokens de salida en vez de 12 000 (`recortes_salida` en F5) y un AUT- DENEGADA por semana en HA (la fase de cribado no admite ampliación); con un tic más del reloj lógico del almacén, las marcas de hora de F3, F4, F5 y RC van un segundo detrás. En las 4 semanas con informe de aprendizaje, COMÚN suma lo de AG-20 (0,17–1,40 UC) | El peor caso del Analista (12 000 tokens de salida, 4 UC, más su entrada) es 6,31 UC y el límite N1 es 5 × 1,25 = 6,25. AG-20 ya no queda fuera del presupuesto |
| Ciclo de los 12 tipos | Informe técnico: la línea de consumo pasa de 62,46 a 64,38 UC (6 búsquedas × 0,32). F5: COMÚN pasa de 5,21 a 6,53 UC (el dictamen G3 de AG-18) | Las búsquedas cuentan en UC y AG-18 carga en COMÚN |

Ninguna selección, pronóstico ni texto de los entregables cambia. `consumo.csv` y `cache_resultados.jsonl` también difieren entre dos pasadas del código de antes (latencias y orden).

## Archivos cambiados

- `bloque_a/consumo.py`: `uc_de` con búsquedas; `resumen` con las búsquedas sumadas; `Presupuesto` con `reservado`, `retenido`, `recortes`, `excesos`, `factor_observado`, `tope_total` (escala), `limite`, `limite_maximo`, `reservar`, `retener_real`, `liberar`, `anotar`, `factor_de`, `observar_factor`, `absorber`; `cargar_con_prima(…, tokens_retener)`; `liquidar_primas` suelta lo retenido; `autorizar_hasta_tope` cuenta lo reservado y lo retenido; `ReservaLlamada`, `tokens_de_peticion`, `busquedas_maximas`.
- `bloque_a/llm.py`: `_GUARDA` y `con_guarda`; `AnthropicClient.generar` reserva cada continuación y paga cada petición.
- `bloque_a/agentes.py`: `invocar(…, guarda=None)`: reserva cada intento, `SIN_PRESUPUESTO`, `presupuesto_agotado`.
- `bloque_a/orquestacion.py`: `_invocar` con la guarda y `control`; `_cargar` con el prefijo de la primera petición, lo diferido acotado y lo retenido; `_solicitar_ampliacion(…, control)`; el ciclo con la bolsa de C5, `tope_total` y `absorber`; `_validar_g3`, `_auditar` e `_informe_aprendizaje` con presupuesto en COMÚN; F5 con `recortes_salida` y `excesos_reserva` si los hay; fuera `_estimar_uc` (ya no se usa).
- `config/por_defecto.yaml`: `presupuesto_uc.reserva` (`factor_tokens_entrada`, `salida_minima_tokens`) y `uc.uc_por_busqueda_web`, con su origen y `[PROPUESTO]`.
- `README.md` del ejecutor: el párrafo de presupuestos y la fórmula de UC.
- `tests/test_t146_presupuesto.py` (nuevo, 22 pruebas). `tests/test_t88_consumo.py::test_r04_h13…` y `tests/test_fase4_huecos.py::test_pb17_en_un_ciclo…`: cambio comentado «T-146» (la reescritura del prompt se carga ya; con 6 UC, la prospectiva cabe en el tope y se autoriza, y lo demás se deniega).

## Decisiones y desviaciones del plan propuesto

- **Recortar la salida antes de cerrar** (no estaba en el diseño propuesto): sin ello, en N1 el Analista no saldría nunca (su peor caso pasa del límite N1 por 0,06 UC) y la consulta N0 tampoco. Es una forma de «degradar» y el peor caso de lo que sale sigue cabiendo.
- **La consulta N0 (C3) queda fuera**: el prompt de AG-01 (≈ 26 000 tokens) escrito en caché ya pasa de 1 UC × 1,25 (≈ 2,2 UC con el margen), así que con el peor caso ninguna consulta saldría. Conserva su `max_uc_estimado=0.0` (llama siempre) y queda declarada en INC-T146-01 para el operador. No es parte del modo sombra (ciclo semanal).
- **AG-18/19/20 en COMÚN**, no en una bolsa nueva (forma de CT-05 congelada en los goldens).
- **Los controles admiten ampliación** (R16), dentro del tope de siempre.
- `_estimar_uc` se quita: nadie lo usa ya.

## Límites conocidos

- La reserva acota con el supuesto de que la entrada real no pasa de 1,35 veces la aproximación de 3,6 caracteres por token; si pasa, la petición ya está pagada: se anota en `excesos_reserva` y la bolsa sube su factor.
- Lo que lee cada búsqueda llega como tokens de entrada de la petición (o de su continuación) y se cobra después, sin reservarse: una petición con búsqueda puede pasar de su reserva (declarado; T-145 lo dejaba fuera de la cota, S5). Se puede medir en el modo sombra.
- Los reintentos del SDK ante 429/5xx (`llm.max_reintentos_api`) no se cobran si la petición falla.
- Con un reparto por encima del ciclo, lo que AG-20 consume antes del reparto se suma a COMÚN aunque su límite escalado sea menor (caso límite de un override o de N3 forzado en el periódico).
- **Para quien junte las copias:** `tests/test_t145.py::test_h01_el_presupuesto_se_pasa_y_la_cota_por_presupuesto_lo_cuenta` (otra copia) afirma `pasadas >= 1`, que con T-146 deja de ser verdad; y la «cota por presupuesto» de `.docs/scripts/estimar_coste_ciclo_a.py` suma la última llamada de cada bolsa, la caché cargada como lectura, AG-18/19/20 y las búsquedas, que T-146 ya mete en las bolsas: tras T-146 basta el límite máximo de cada bolsa. No se tocan aquí (los lleva otra copia).

## Comandos

```bash
py=/home/user/robotinvestor/.venv/bin/python   # o .venv/bin/python desde la raíz
cd bloque_a/11_Ejecutor
$py -m pytest -q -p no:cacheprovider tests/test_t146_presupuesto.py
$py -m pytest -q -p no:cacheprovider tests/test_integracion.py tests/test_unitarias.py tests/test_t87_*.py tests/test_t88_*.py \
    tests/test_t113*.py tests/test_t12*.py tests/test_t13*.py tests/test_fase3_goldens.py tests/test_fase4_*.py
$py tests/goldens_ct.py
cd ../..
git archive 19f3f3b bloque_a | tar -x -C <antes>        # el código de antes, para comparar
$py -I .docs/tickets/T-146/peor_caso_por_bolsa.py <antes>/bloque_a/11_Ejecutor <tmp> [--doce --hilos 6]
$py -I .docs/tickets/T-146/peor_caso_por_bolsa.py bloque_a/11_Ejecutor <tmp> [--doce --hilos 6]
.docs/tickets/T-146/comparar_ciclos.sh <antes>/bloque_a/11_Ejecutor bloque_a/11_Ejecutor <tmp> $py
$py .docs/tickets/T-146/mutantes_t146.py <copia desechable con «t146_mut» en la ruta>
```

## Ronda r02 (QA r01 NO APTO)

### H-01 · el factor observado y las búsquedas

`pagar` comparaba la entrada cobrada con la medida de la petición. En una petición con búsquedas, la entrada cobrada trae lo que leyeron (la API lo cobra como entrada de esa misma petición), así que el factor subía a lo que leyeron las búsquedas (≈ 4,7 con 5 × 6 000 tokens) y todas las peticiones siguientes de la bolsa reservaban varias veces su peor caso. Ahora el factor solo se aprende de las peticiones con `busquedas_web == 0`. Se valoró restar una estimación de lo leído, pero no hay número con origen (ver H-04) y restar 0 no corrige nada. El exceso de una petición con búsquedas sigue anotándose (con `busquedas_web`, para medir en el modo sombra lo que leen).

### H-02 · determinismo con una caché compartida

Lo que se aparta entre las peticiones de una llamada decide si caben la reparación y las continuaciones. Era `uc_de(uso)`, que cuenta la lectura de caché a 0,1: dependía de si otro hilo ya había escrito el prefijo compartido (AG-10, AG-11, AG-12, AG-14, AG-16). Ahora se aparta `uc_de` con `cache_escritura + cache_lectura` como escritura, que depende solo del tamaño de la petición. El exceso (`excesos_reserva`, en F5) se calcula con lo mismo, así que también es independiente del orden. Lo cargado en la bolsa al final (`_cargar` y `liquidar_primas`, T-88) ya era independiente del orden cuando el punto de caché está al final del system prompt: el prefijo de la primera petición (`ReservaLlamada.prefijo` = lectura + escritura) es el mismo leído o escrito. Nota para quien escriba SDK falsos: si un SDK cuenta también el encargo como escritura de caché solo cuando escribe el prefijo (y no cuando lo lee), el prefijo de la primera petición cambia con el orden y F5 también; la API no hace eso (lo de después del último punto de caché es entrada), y `SDKCacheYBusquedas` de la prueba tampoco.

La prueba fuerza el orden sin depender de los tiempos: cada hilo de tipo espera a que acabe el anterior, en el orden RV, RF, DIV, MP y en el contrario. Con el código de la r01, F5 cambia (consumido, ampliado, cierres y qué petición se cierra); con la r02, iguales, y también las llamadas por agente.

### H-03 · AG-20 con escala

AG-20 corre en C5 antes del reparto, porque sus lecciones cambian GC0 (`lecciones_vigentes` → nivel N1 o N2) y no se puede mover detrás. Se calcula antes el peor reparto posible, con el mismo código del reparto (`Bloque._reparto`, sacado de `ciclo` sin cambiar nada): los tipos pedidos que estén activos en F10 (P-02 solo cambia con un CT-04, no en C5), cada uno con el nivel de más presupuesto que le puede tocar (en un periódico sin nivel forzado, el mayor de N1 y N2; si no, el forzado o el de la profundización), el override y el reparto V6. La base de COMÚN escalada baja cuando sube lo de los tipos (sin escala, COMÚN = ciclo − tipos; con escala, mínimo × ciclo / (tipos + mínimo)), así que la del peor reparto es la menor posible. La bolsa de C5 es la de antes o esa, la menor: lo que consume AG-20 (sin ampliación: no es fase de las que la admiten) cabe en el límite de COMÚN del ciclo. Con el reparto de siempre la del peor reparto es ≥ el mínimo y no cambia nada (`comparar_ciclos.sh`: F5 igual que en la r01).

### H-04 · la salvedad y la lectura por búsqueda

`presupuesto_uc.reserva.tokens_lectura_por_busqueda` (por defecto 0) se suma a la entrada reservada por cada búsqueda posible (`max_uses`). Con 0 la reserva es la de la r01. No se pone otro valor porque no hay ninguno con origen (ni el Documento 0, ni la documentación de la API, ni una medida); queda la pregunta al operador en INC-T146-01, y los excesos de F5 con sus búsquedas son la medida. La salvedad (también el margen 1,35 sobre una aproximación) va en el CA-1 y en INC-T146-01. Lo que no se reserva solo puede pasar el límite de una bolsa en la petición que lo cruza: después lo disponible es negativo y no sale ninguna más; T-148 r02 usa eso para el peso de lo leído en la cota por presupuesto.

### H-05 a H-10

- H-05: `extraer_json` → `ValueError` ante `RecursionError`; `invocar` también lo captura al validar con el esquema y, en R8, falla cerrado. `_invocar` carga lo apartado si la llamada se cae (el análisis de un tipo puede seguir en modo degradado y lo gastado debe estar en la bolsa).
- H-06: `Presupuesto.escala` y `base`; `resumen` da lo asignado escalado si la escala es < 1; CT-05 igual; F5 con `escala_presupuesto`. Con escala 1, ni un byte cambia.
- H-07: ver README.
- H-08: `_cargar` antes de `cerrar`. Entre los dos, la bolsa cuenta lo de la llamada dos veces (prudente).
- H-09: no se hace (sin la API), para la deuda.
- H-10: tres pruebas que matan Q01, Q09 y Q12.

### Límites conocidos (r02)

- Lo que lee cada búsqueda y lo que la entrada pase del margen siguen sin cota (salvedad declarada); en la petición que cruza el límite, la bolsa pasa de él en eso.
- `r01_01` U2 reproduce a mano el orden `cerrar` → `cargar` y sigue dando VIOLA; `_invocar` ya no lo hace.
- Los mensajes de V6 que llevan `presupuesto: {"uc": presupuesto.asignado…}` siguen con lo asignado sin escalar (informativo; con escala 1, igual).

### Comandos (r02)

```bash
cd bloque_a/11_Ejecutor
../../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_t146_presupuesto.py -k r02
../../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_t146_presupuesto.py tests/test_t145.py tests/test_t148.py tests/test_t88_consumo.py tests/test_fase4_huecos.py tests/test_integracion.py
cd ../..
.venv/bin/python -I .docs/tickets/T-146/revisores/r01_01_reserva_unidad.py bloque_a/11_Ejecutor
.venv/bin/python -I .docs/tickets/T-146/revisores/r01_02_ciclo_sdk_hostil.py bloque_a/11_Ejecutor <tmp> --tipos RV,RF,DIV,MP,IDX,FON,DER,INM,CRI,ALT,MON,TCV --hilos 6 --lectura 3000
.venv/bin/python -I .docs/tickets/T-146/revisores/r01_02_ciclo_sdk_hostil.py bloque_a/11_Ejecutor <tmp> --tipos RV,RF,DIV,MP --hilos 4 --cache --orden directo --veces 2
.venv/bin/python -I .docs/tickets/T-146/revisores/r01_03_c5_con_escala.py bloque_a/11_Ejecutor <tmp>
.venv/bin/python .docs/tickets/T-146/mutantes_t146.py <copia con «t146_mut»>
.venv/bin/python .docs/tickets/T-146/revisores/r01_05_mutantes_qa.py <copia con «qa19_mut»>
```
