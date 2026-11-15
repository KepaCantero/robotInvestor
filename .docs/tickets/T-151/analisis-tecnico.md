# T-151 · Análisis técnico

## Causa raíz o motivo

Las QA r02 de T-146 y T-148 dieron APTO y dejaron hallazgos bajos (secciones «Ronda r02» de `.docs/tickets/T-146/qa.md` y `.docs/tickets/T-148/qa.md`, scripts en sus `revisores/r02_*.py`), más el H-09 de la r01 de T-146:

- **H-11.** El arreglo de H-01 dejó de observar el factor del tokenizador en las peticiones con búsquedas, pero no en la continuación de `pause_turn` que no busca y reenvía los bloques de búsqueda de las vueltas anteriores. Si la medida (3,6 caracteres por token sobre el `model_dump` de esos bloques) se queda corta, el factor de la bolsa sube (6,57 en el R9 del revisor) y cierra fases antes de tiempo. Falla cerrado, pero injusto.
- **H-12.** `Bloque.ciclo` corre AG-20 contra `pres_c5` y, si no queda ningún tipo que analizar, sale por `_run_sin_analisis` antes de `presupuesto.absorber(pres_c5)`, que no escribía `presupuesto` en el RUN de F5: lo gastado estaba en la contabilidad y acotado, pero en ninguna bolsa (R7).
- **H-13.** Texto: la salvedad del CA-1 de T-146 («después no sale ninguna más de esa bolsa») solo vale respecto del límite máximo (R8), y la línea «Límites declarados» de INC-T146-01 decía que tras una búsqueda que lee mucho la bolsa usa el factor observado (desde la r02, no).
- **V01, V04, V05.** Mutantes vivos del revisor: ninguna prueba comparaba los excesos con el prefijo leído o escrito, ni un `KeyboardInterrupt` por `Bloque._invocar` en las suites del mutante, ni la rama `RecursionError` de R8.
- **H-09 (r01).** `AnthropicClient` creaba el SDK con `max_retries=llm.max_reintentos_api` (4): el SDK reintentaba conexión, *timeout*, 408, 409, 429 y 5xx por su cuenta, dentro de una sola llamada a `messages.create`, sin pasar por `ReservaLlamada`. Un *timeout* que el servidor completó se podía cobrar sin reserva, hasta cuatro veces por petición. Y la escritura de caché a 1 h cuesta en USD el doble que la entrada, mientras `Contabilidad.uc_de` la cuenta como entrada.
- **H-04 (T-148 r02).** Mutantes W04 (la frase de la salida con `tokens_lectura_por_busqueda` > 0) y W05 (el peso por bolsa con `--sin-t146`) vivos.

## Evidencia

- Antes (código de `e1a8f87`): `r02_01_arreglos_r02.py` daba R7 y R9 en VIOLA; `r02_02_mutantes_qa.py` de T-146, 7/10 (V01, V04 y V05 vivos); el de T-148, 2/5 (W02, W04 y W05 vivos).
- `llm.py` (antes): `sdk = anthropic.Anthropic(api_key=clave, max_retries=max_reintentos, timeout=timeout_s)`; `except Exception: return RespuestaLLM("", uso, modelo, stop_reason="error_proveedor")` (comentario: «El SDK ya ha agotado sus reintentos»). En el SDK 2.8 instalado, `BaseClient._should_retry` reintenta 408, 409, 429 y ≥ 500 y `_calculate_retry_timeout` espera 0,5 s doblando hasta 8 s con variación aleatoria (`anthropic/_constants.py`).
- Después: ver `pruebas.md` (R7 y R9 OK, 28/28; V 10/10; W 4/5 con W02 equivalente).

## Implementación

- Archivos cambiados y por qué:
  - `bloque_a/consumo.py`: `ReservaLlamada.pagar` calcula `ya_busco` (una petición anterior de la generación en curso buscó) y no observa el factor si es así (H-11). `ReservaLlamada.fallida(cobro_posible, motivo)` (H-09): la petición que falló suelta su reserva si no se cobró; si pudo cobrarse, su peor caso queda apartado (`sin_respuesta`) y se anota en `Presupuesto.sin_respuesta`; `cerrar` lo carga en la bolsa antes de soltarlo (como H-08). `Presupuesto.absorber` pasa también `sin_respuesta`. El motivo de una petición negada dice «reparación, continuación o reintento».
  - `bloque_a/llm.py`: `ReglaReintentos` (de la configuración, con validación que falla cerrado), `clasificar_error` y `AnthropicClient._crear` (los reintentos, cada uno con su reserva y su espera; `dormir` inyectable). El SDK se crea con `max_retries=0`, y a uno recibido con `with_options` se le pone 0. `crear_cliente` pasa la regla. El parámetro `max_reintentos` del constructor desaparece (lo sustituye `reintentos`); nadie más lo usaba (búsqueda en el repo).
  - `bloque_a/orquestacion.py`: `_f5_presupuesto` (lo del presupuesto que lleva el RUN de F5, igual que antes más `peticiones_sin_respuesta`) para el RUN normal y el RUN sin análisis; `_run_sin_analisis` recibe `pres_c5` (H-12). De paso, el `import typing` sin usar (siete avisos de ruff menos).
  - `config/por_defecto.yaml`: `llm.reintentos` (`espera_inicial_s`, `espera_max_s`, `estados_reintentables`, `estados_sin_cobro`) con su origen y `[PROPUESTO]`.
  - `README.md` del ejecutor, `docs/incidencias.md` (INC-T146-01: «Límites declarados» y la ronda T-151), `.docs/tickets/T-146/README.md` (CA-1).
  - Pruebas: `tests/test_t146_presupuesto.py` (H-11, H-12, V01, V04, V05), `tests/test_t151_reintentos.py` (H-09, nuevo), `tests/test_t148.py` (W04, W05).
  - `.docs/tickets/T-151/mutantes_t151.py`: 18 mutantes de lo que cambia T-151.
- Decisiones tomadas y desviaciones del plan:
  - **H-11, la regla:** «una petición de una generación que ya buscó no observa». Una generación es una llamada al cliente (`pagar_resto` cierra la generación): la primera petición y sus continuaciones. La reparación empieza otra y no reenvía bloques de búsqueda (`Agentes.invocar` añade solo `r.texto`), así que sí observa: se prueba.
  - **H-09, reintentar en el ejecutor y no declararlo solo:** el cambio es pequeño, determinista y se prueba sin red con el SDK real sobre `httpx2.MockTransport`. Clasificación: conexión y *timeout* se reintentan y cuentan como cobro posible; un estado HTTP se reintenta si está en `estados_reintentables` (o lo pide `x-should-retry`, como el SDK) y no se cobra si está en `estados_sin_cobro` o no se reintenta (el servidor lo rechazó: 400, 401…); otro error (no del proveedor) ni se reintenta ni se cobra, como antes. Sin regla (cliente creado a mano) no se reintenta y un error del proveedor cuenta como cobrado (prudente). La espera no tiene la variación aleatoria del SDK (determinista; las esperas no cambian resultados). Se respeta `retry-after-ms` y `retry-after` en segundos; una fecha HTTP no se interpreta (espera de la regla).
  - **Lo que pudo cobrarse sin respuesta se carga por su peor caso reservado**, no por cero: es una cota superior (falla cerrado), no un valor inventado. La contabilidad no lo registra (no hay uso que registrar): el RUN lo declara en `peticiones_sin_respuesta` y lo consumido de la bolsa pasa a lo de la contabilidad en esa cantidad.
  - **Caché a 1 h:** solo se declara (cambiar la UC de la escritura cambiaría todas las bolsas y su relación con el Anexo A; es del operador).
  - **Los textos citados por los mutantes** (`mutantes_t146.py`, `r01_05`, `r02_02` de T-146 y T-148, `T-147/mutantes.py`) se conservan: aplican todos.
  - **`tools/cuotas.txt` no se toca:** ruff baja a 2831 (−7) y mypy de A se queda en 109; el *ratchet* lo deja a quien coordina (otra tarea trabaja en paralelo en el mismo paquete).
- Límites conocidos:
  - Sin la API no se sabe si los estados sin cobro son exactamente 429 y 529, ni cuánto miden de verdad los bloques de búsqueda reenviados (H-11): para el modo sombra (`peticiones_sin_respuesta`, `excesos_reserva`, `factor_observado`).
  - El motivo de las fases cerradas por una petición negada cambia de texto («reparación, continuación o reintento»): cambia la firma de F5 del `r01_02` con caché (`fce20f7854fb` frente a `20ad04339dc9`); el resto de F5 es idéntico (comprobado campo a campo).
  - Un reintento sale con el `max_tokens` de la petición que falló (o menos, si la reserva lo recorta).
- Comandos exactos para probarlo (desde la raíz de la copia):
  - `cd bloque_a/11_Ejecutor && ../../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_t151_reintentos.py tests/test_t146_presupuesto.py tests/test_t148.py`
  - `.venv/bin/python -I .docs/tickets/T-146/revisores/r02_01_arreglos_r02.py bloque_a/11_Ejecutor <tmp>` (28/28)
  - `.venv/bin/python .docs/tickets/T-151/mutantes_t151.py <copia con «t151_mut»>`; `r02_02_mutantes_qa.py` de T-146 y T-148 en copias con «qa21_» y «_mut».
