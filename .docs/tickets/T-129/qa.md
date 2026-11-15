# T-129 · QA independiente

# Ronda r01 · 2026-11-15

- **Revisor:** subagente revisor nuevo, sin contexto de la implementación (Claude; implementó otra sesión de Claude) · **Ronda:** r01
- **Copia revisada:** copia git desconectada en `fe5b7d0` (T-129 entra en `08b357e`: `config/precios_anthropic.yaml`, `.docs/scripts/estimar_coste_ciclo_a.py`, `tests/test_t129_modo_sombra.py`, INC-T129-01).
- **Orden de lectura:** `README.md` → tarifa, estimador, prueba y `llm.AnthropicClient` → mis scripts → al final `analisis-tecnico.md`, `pruebas.md` e INC-T129-01.
- **Sin gasto:** ninguna llamada a la API. El SDK real (`anthropic` 2.8.0) se usó con una clave falsa y un transporte HTTP en memoria (`httpx2.MockTransport`): no sale nada a la red.
- **Documentación pública consultada (solo lectura, 15-11-2026):** página de precios y página de la herramienta de búsqueda web de `platform.claude.com`.

## Reproducción desde limpio

Desde la raíz de la copia, con el intérprete del repositorio (`/home/user/robotinvestor/.venv/bin/python`, abreviado `py`).

| Comprobación | Orden | Resultado |
| --- | --- | --- |
| Tabla del README, solo divisas | `cd bloque_a/11_Ejecutor && py ../../.docs/scripts/medir_consumo_a.py <tmp>/div` y, desde la raíz, `py .docs/scripts/estimar_coste_ciclo_a.py <tmp>/div` | **8 llamadas · 0,86 · 1,68 USD**: coincide |
| Tabla del README, los 12 tipos | ídem con `2024-03-29 --config <tmp>/doce.yaml` (`perfiles.activos` con los 12) en las dos órdenes | **77 llamadas · 2,98 · 11,47 USD (30 búsquedas)**: coincide. El README no dice qué YAML se usó para «los 12 tipos»; con el de una línea de arriba sale exacto |
| Tarifa frente a la documentación | lectura de la página de precios | Opus 5.5 4 / 20, escritura 1 h 8, lectura 0,20; Sonnet 5.5 2 / 10, 4, 0,10; Haiku 5.5 0,10 / 0,50, 0,20, 0,01 (hasta 100 000 tokens; por encima ×5); búsqueda web 10 USD por 1 000, la fallida no se cobra; `inference_geo: "us"` ×1,1. **Todo coincide** con `precios_anthropic.yaml` |
| Modelos y herramienta | página de la búsqueda web | `claude-opus-5-5`, `claude-sonnet-5-5` y `claude-haiku-5-5` admiten la búsqueda; versiones `web_search_20250305`, `_20260209` y `_20260318` (la más reciente, añade `response_inclusion`). Coincide con el README |
| `por_defecto.yaml` sin precios | `git diff 08b357e~1 HEAD -- bloque_a/11_Ejecutor/config/por_defecto.yaml` | La sección `precios_por_millon` sigue con `null`; el único cambio del fichero es de T-125 (`prob_sin_declarar`) |
| Mi script 1 | `py -I .docs/tickets/T-129/revisores/r01_01_sdk_real_sin_red.py` | **10 ok, 1 fallo** (H-01). Ciclo en vivo (RV + DIV, N2) con el SDK real: 17 peticiones HTTP, claves `max_tokens, messages, metadata, model, system, tools`; sin prefill; `web_search_20260318` con `max_uses` 5; `anthropic-version: 2026-10-21`; `cache_control` con `ttl: "1h"`, un punto por petición; un 400 del servidor acaba en `error_proveedor` sin el mensaje |
| Mi script 2 | `py -I .docs/tickets/T-129/revisores/r01_02_sensibilidad_cota.py <tmp>/doce --config <tmp>/doce.yaml` | Ver H-01: la «cota superior» de 11,47 pasa a 13,85 con `pause_turn`, a 16,54 sin las lecturas de caché del simulador y a 19,14 con eso y tokens ×1,35. Haiku: prompt máximo 12 875 tokens, lejos del umbral de 100 000 |
| Mi script 3 (mutantes) | `py -I .docs/tickets/T-129/revisores/r01_03_mutantes_cliente.py <copia qa11_mut>` | **13/15 muertos**: temperature, top_p, top_k, thinking desactivado o con presupuesto, `tool_choice` any y tool, prefill, thinking en `extra_body`, búsqueda en todos los agentes, `metadata` con un correo, `max_tokens` 64 000 y un modelo retirado. Vivos: `output_config` con un `effort` inválido y la herramienta `web_search_20250305` (H-03) |
| Suite, goldens, gates y cuotas | comunes a T-129…T-132 (ver «Comunes» en `T-132/qa.md`) | ver allí |

## Criterios de aceptación

| Criterio | Cumple | Evidencia |
| --- | --- | --- |
| CA-1 | sí | `test_t129_modo_sombra.py` en la suite completa (10 pruebas) |
| CA-2 | sí | Las dos filas de la tabla salen exactas con las órdenes del README (falta decir el YAML de «los 12 tipos») |
| CA-3 | sí, salvo el gate entero (no lanzado por instrucción) | `por_defecto.yaml` sin precios; `test_la_configuracion_por_defecto_sigue_sin_precios` y las pruebas de la entrega en verde; gates ligeros y cuotas en verde |

## Hallazgos

| ID | Gravedad | Cómo reproducirlo | Esperado / obtenido | Corrección sugerida | Estado |
| --- | --- | --- | --- | --- | --- |
| H-01 | media | `r01_01` [2] y `r01_02` (orden de arriba) | **Esperado:** la «cota superior» del README y del estimador acota el coste de un ciclo, salvo lo que dice que no incluye (lo leído por cada búsqueda, reintentos, reparaciones de JSON). **Obtenido:** hay tres cosas más que la superan y no están dichas. (1) `pause_turn`: el cliente continúa hasta `max_continuaciones_pause_turn` = 3 veces; con el SDK real, una llamada de un agente con búsqueda puede ser 4 peticiones, cada una con su entrada y hasta `max_tokens` de salida; y con el filtrado dinámico (`web_search_20260209` y posteriores), las búsquedas hechas desde la ejecución de código en peticiones anteriores del turno no cuentan para `max_uses` (documentación de la herramienta). Con los 12 tipos: 13,85 USD y hasta 120 búsquedas (no 11,47 y 30). (2) Las lecturas de caché las pone el simulador, que con su cerrojo lee al instante; los Analistas van en 4 hilos y en la API una entrada de caché solo existe cuando la primera respuesta empieza, así que llamadas en paralelo con el mismo prefijo escriben en vez de leer: sin lecturas, 16,54 USD. Con los 12 tipos, 1,07 M de los 1,66 M tokens de entrada son lecturas de caché del simulador. (3) Los tokens son una aproximación (3,6 caracteres por token), no el tokenizador del modelo: el docstring dice que la entrada «es la real», y lo es el texto, no su recuento | Llamar «estimación alta» a la cifra o añadir a la cota las continuaciones (×(1 + max_continuaciones) en los agentes con búsqueda) y una variante sin lecturas de caché; decir en el README y en INC-T129-01 que los tokens son aproximados (el recuento real pide `count_tokens`, que no cobra pero necesita clave) | abierto |
| H-02 | baja | lectura de `estimar_coste_ciclo_a.py` y de la documentación (pensamiento adaptativo) | **Esperado** (`analisis-tecnico.md`: «la cifra real debería estar entre las dos»). **Obtenido:** la «estimación» toma como salida el JSON del simulador (161 a 4 524 tokens por agente). Los tres modelos piensan por defecto (en Opus 5.5 no se puede desactivar) y el pensamiento se cobra como salida, así que la cifra real estará casi seguro por encima de la estimación; es un suelo, no un valor central | Decirlo en el README («la estimación no incluye el razonamiento del modelo, que se cobra como salida») | abierto |
| H-03 | baja | `r01_03` | **Esperado:** la prueba fija lo que el README dice comprobado. **Obtenido:** dos mutantes viven: (a) `output_config` con cualquier contenido pasa (`CLAVES_PERMITIDAS` mira solo la clave de primer nivel; un `effort` inválido daría un 400); (b) volver a `web_search_20250305` pasa (`BUSQUEDA_WEB_VIGENTES` admite las tres versiones), aunque el README dice que se usa la más reciente. Ninguno de los dos lo hace hoy el código | En la prueba: si hay `output_config`, que solo lleve `format` (y `effort` en la lista de la API si se añade); y que el tipo de la herramienta sea el de `busqueda_web.tipo_herramienta` | abierto |

Los scripts de ataque están en `revisores/` (r01_01 a r01_03).

## Invariantes

- Ningún camino a una orden sin F y G: no aplica (T-129 no toca la ruta de decisión). Sin LLM en la ruta determinista: el estimador y la prueba no llaman a ningún modelo. ✔
- Falla cerrado: sin `ANTHROPIC_API_KEY` el cliente real no arranca (prueba); un 400 queda en `error_proveedor` sin el texto del servidor (`r01_01` [3]). ✔
- Números a mano: la tarifa está en un YAML con fuente y fecha, fuera de `por_defecto.yaml`, que sigue sin precios. ✔
- Decisiones del operador: tres `[PROPUESTO]` en INC-T129-01 y en `Decisiones_del_operador_Bloque_A.md`. ✔
- Secretos y datos personales: `metadata.user_id` es `bloque-a-AG-NN` (prueba y mutante); gate de secretos en verde con mis scripts. ✔
- Documentación: README, INC, deuda y diario al día; H-01 y H-02 piden matizar la tabla.

## Veredicto

**APTO** · Los tres criterios se cumplen (CA-3 sin el gate entero, que no lancé por instrucción). La tarifa, los modelos y la versión de la búsqueda coinciden con la documentación pública del 15-11-2026; el cliente real, con el SDK de verdad, no envía nada que la familia 5.5 rechace, y la prueba mata los mutantes de los parámetros prohibidos. No hay hallazgos críticos ni altos. Pasan a la deuda con su ID: **H-01** (media: la «cota superior» no lo es con `pause_turn`, llamadas en paralelo sin caché y tokens aproximados; con los 12 tipos, 13,85–19,14 USD en vez de 11,47), **H-02** y **H-03** (bajas). Conviene corregir H-01 antes de pedir al operador que autorice el gasto con esa cifra.
