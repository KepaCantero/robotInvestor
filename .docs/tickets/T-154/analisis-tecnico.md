# T-154 · Análisis técnico

## Causa raíz o motivo

La QA r01 de T-151 (`.docs/tickets/T-151/qa.md`) dio APTO con cinco hallazgos bajos, reproducibles con sus scripts (`.docs/tickets/T-151/revisores/r01_0*.py`):

- **H-01.** `clasificar_error` daba «cobro posible» solo a lo que se reintentaba (`return reintenta, reintenta and …`). Un 5xx fuera de `estados_reintentables` (501, 505, 520) o un 500 con `x-should-retry: false` no se reintentaba y soltaba su reserva como no cobrado, aunque el README del ejecutor e INC-T146-01 dicen que se carga todo 5xx salvo el 529 (`r01_01` X9).
- **H-02.** `Bloque.ciclo` escribe el RUN en F5 (`_registrar_run`, F8) y después corre la auditoría (`_auditar`, F9). Lo que AG-19 deja en el presupuesto (la petición sin respuesta, y desde T-146 sus cierres, recortes y excesos) estaba en la bolsa y en `resultado["presupuesto"]`, pero en ninguna entrada de F5 (`r01_02 … --veces 2`: F5 declaraba 20,47 de 24,68 UC sin respuesta).
- **H-03.** `Presupuesto.liquidar_primas` reparte entre las bolsas de un grupo de prefijos lo escrito que se vio (`_reales`). Si la petición que no respondió era la primera que escribía el prefijo, ninguna respuesta trae esa escritura: con ese orden de hilos no se reparte nada, y con otro (otra bolsa escribe antes y lo ve) se reparte el prefijo entero. Lo consumido de DIV, MP y RV cambiaba 0,5157 UC según el orden (`r01_02 … --cache --orden directo --veces 3`: DISTINTO).
- **H-04.** Ninguna prueba miraba un `retry-after` infinito o NaN (mutante Q09) ni `x-should-retry` con mayúsculas (Q10). El código ya los trataba bien (`math.isfinite`, `.lower()`); faltaban las pruebas. El nombre de la cabecera se leía sin normalizar (con un diccionario simple, «Retry-After» no se veía) y no había tope a la espera que pide el servidor (`r01_01` X10: 100 000 s).
- **H-05.** Textos: el CA-7 de T-151 decía ruff ≤ 2838 y su análisis y sus pruebas que `tools/cuotas.txt` no se tocaba (el commit `1ccffd5` la bajó a 2831); INC-T129-01 y el S5 de `.docs/scripts/estimar_coste_ciclo_a.py` decían «los reintentos del SDK».

## Evidencia

- Antes (código de `1ccffd5`): `r01_01` X9 «cargado sin respuesta 0» en los cuatro casos; X10 «espera 100000.0 s»; `r01_02 --tipos RV,RF,DIV,MP --hilos 4 --cache --orden directo --veces 3`: DISTINTO (firmas `8426771dbee9` y `c95463da2b97`); `r01_03_mutantes_qa.py`: 14/16 (Q09 y Q10 vivos).
- Después: ver `pruebas.md` (X9 cargado 1 en los cuatro; X10 None; r01_02 IGUAL en todos los órdenes; 16/16).

## Implementación

- Archivos cambiados y por qué:
  - `bloque_a/llm.py`: `ReglaReintentos` lleva `espera_servidor_max_s` y `cobro_posible` (de `llm.reintentos.espera_servidor_max_s` y `cobro_posible_desde`, validados como las demás claves). `clasificar_error`: desde `cobro_posible`, cobro posible = no está en `sin_cobro`, se reintente o no (H-01); `x-should-retry` sin espacios ni mayúsculas. `_cabeceras(error)`: las cabeceras con el nombre en minúsculas (H-04). `ReglaReintentos.espera` devuelve None si el servidor pide más del tope, y `_crear` entonces no reintenta (`error_proveedor`).
  - `bloque_a/consumo.py`: `Presupuesto.marca()` y `Presupuesto.desde(marca)` (un `TramoPresupuesto` con lo declarado después de la marca y el resumen de ahora; H-02); `Presupuesto.grupo_sin_respuesta(grupo)` y, en `liquidar_primas`, un grupo marcado reparte la suma de los pesos «solo» (`reales = total`): cada bolsa paga su prima «solo» entera (H-03).
  - `bloque_a/orquestacion.py`: `grupo_primas(v6, agente)` (el grupo que ya calculaba `_cargar`, ahora función de módulo para que `_invocar` marque el mismo); `_invocar` marca el grupo si la llamada tuvo una petición sin respuesta que pudo cobrarse; `ciclo` toma la marca antes de `_auditar` y llama a `_registrar_f9`, que escribe `PRESUPUESTO_F9` en F5 solo si la auditoría dejó algo que declarar.
  - `config/por_defecto.yaml`: `llm.reintentos.espera_servidor_max_s` (600) y `cobro_posible_desde` (500), con su origen y `[PROPUESTO]`.
  - `README.md` del ejecutor (párrafo de presupuestos), `docs/incidencias.md` (INC-T146-01, ronda T-154; INC-T129-01, dos líneas), `.docs/scripts/estimar_coste_ciclo_a.py` (S5), `.docs/tickets/T-151/README.md` (CA-7), `analisis-tecnico.md` y `pruebas.md` de T-151 (cuotas).
  - Pruebas: `tests/test_t154.py` (nuevo, 67); en `tests/test_t151_reintentos.py`, la línea del 500 con `x-should-retry: false` pasa de (False, False) a (False, True): es la expectativa que corrige H-01, no se debilita.
  - `.docs/tickets/T-154/mutantes_t154.py`: 18 mutantes de lo que cambia T-154.
- Decisiones tomadas y desviaciones del plan:
  - **H-01, el umbral en la configuración:** el 500 es la definición de la clase 5xx (RFC 9110 §15.6), pero la regla del encargo es «números solo de la configuración», así que va en `cobro_posible_desde` con su origen. No se reintentan más estados que antes (un 501 no se arregla reintentando): solo se cargan.
  - **H-02, una entrada propia en vez de mover la auditoría:** mover `_auditar` antes de `_registrar_run` cambiaría el orden de las fases (F8 escribe F5 y entrega CT-02; F9 es asíncrona), el contenido del RUN de todos los ciclos (`consumo`, `participantes` con AG-19) y lo que compara `comparar_ciclos.sh`. La entrada `PRESUPUESTO_F9` (id `F5F9-…`, distinto del RUN, que `estado("F5")` indexa por `id`) solo se escribe cuando hay algo; los lectores de F5 filtran por `tipo_entrada` (búsqueda en `bloque_a/`). Límite declarado en INC-T146-01: lo que gasta AG-19 sin incidencias no sale en F5.
  - **H-03, la regla limpia:** se descartó apuntar el prefijo de la fallida como escrito (no se sabe su tamaño ni si escribió; en el otro orden contaría dos veces). La cota «cada bolsa paga su prima solo» es determinista (los pesos lo son desde T-88 y la marca depende solo de qué peticiones fallaron), es una cota superior de lo escrito (lo diferido de cada llamada es `min(escrito, solo)` ≤ su peso) y es lo que ya estaba retenido (T-146), así que no pasa ninguna bolsa de su límite. Solo cambia algo con peticiones sin respuesta.
  - **H-04, el tope:** si el servidor pide esperar más de `espera_servidor_max_s`, no se reintenta (falla cerrado) en vez de esperar menos de lo pedido (se inventaría una espera). 600 s, lo que se espera una respuesta (`llm.timeout_s`); pregunta al operador en INC-T146-01.
  - **Textos citados por los mutantes** (`mutantes_t151.py`, `r01_03` de T-151, `mutantes_t146.py`, `r01_05` y `r02_02` de T-146, `r02_02` de T-148): se conservan (por eso el reparto de H-01 es una rama antes de la línea de N11 y Q15, y la de Q09 y N17 sigue entera). Todos aplican.
  - **Cuotas:** ruff 2831 (la línea de `import` de la prueba nueva, ordenada con `ruff --fix`) y mypy de A 109. `tools/cuotas.txt` no se toca (ya está en 2831 y 109).
- Límites conocidos:
  - Sin la API no se sabe qué 5xx cobra de verdad ni cuánto tarda un `retry-after` real: para el modo sombra (`peticiones_sin_respuesta`).
  - La contabilidad (`consumo` del RUN en F5, `consumo.csv`) dice lo que la API informó: con una escritura que nadie vio, sus tokens de escritura sí dependen de qué petición escribió. H-03 hace determinista el presupuesto (las bolsas de F5), no el uso informado.
  - En un grupo con un fallo se carga más que lo escrito (hasta la prima «solo» de cada bolsa): prudente y declarado.
- Comandos exactos para probarlo (desde la raíz de la copia):
  - `cd bloque_a/11_Ejecutor && ../../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_t154.py tests/test_t151_reintentos.py tests/test_t146_presupuesto.py tests/test_t88_consumo.py`
  - `.venv/bin/python -I .docs/tickets/T-151/revisores/r01_02_ciclo_reintentos.py bloque_a/11_Ejecutor <tmp> --tipos RV,RF,DIV,MP --hilos 4 --cache --orden directo --veces 3` (y `--orden inverso`)
  - `.venv/bin/python .docs/tickets/T-154/mutantes_t154.py <copia con «t154_mut»>`
