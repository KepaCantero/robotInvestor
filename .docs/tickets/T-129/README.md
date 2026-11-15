# T-129 · Bloque A: preparar el modo sombra sin gasto

| Campo | Valor |
| --- | --- |
| Estado | CERRADO |
| Pieza | bloque_a (11_Ejecutor: `config/precios_anthropic.yaml`, pruebas; `.docs/scripts/estimar_coste_ciclo_a.py`). No cambia código de producción |
| Planifica · implementa · QA | claude · claude · un revisor nuevo sin contexto |
| Aprobación del operador | 2026-11-15: «me parece genial» (punto 6 de la lista de tareas de la noche) |
| Deuda técnica | T-129 en `sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md` |

## Objetivo

Que el día que el operador autorice el gasto, el modo sombra (Fase 5) arranque sin sorpresas: modelos y herramienta de búsqueda válidos, ninguna petición que la API rechace, el cliente real cerrado sin clave y una cifra de coste por ciclo antes de gastar. Nada de esto llama a la API.

## Qué se hace

- **Comprobado en la documentación de Anthropic (15-11-2026):** `claude-opus-5-5`, `claude-sonnet-5-5` y `claude-haiku-5-5` son vigentes; `web_search_20260318` es la versión más reciente de la búsqueda web (añade el control de qué resultados vuelven en la respuesta).
- **Tarifa aparte** en `config/precios_anthropic.yaml`, con fuente y fecha. `por_defecto.yaml` sigue sin precios (la entrega no los inventa y sus pruebas lo comprueban); la tarifa se pasa con `--config`.
- **Estimador** `.docs/scripts/estimar_coste_ciclo_a.py`: aplica la tarifa a lo que mide `medir_consumo_a.py` y da una estimación y una cota superior por ciclo.
- **Pruebas** `tests/test_t129_modo_sombra.py`: un ciclo con el cliente real sobre un doble del SDK, en backtest y en vivo, sin parámetros que la familia 5.5 rechace con un 400 (temperatura, razonamiento desactivado, `tool_choice` forzado, «prefill» de asistente), con la búsqueda web solo en vivo y solo en sus agentes, y sin datos personales en `metadata`; sin clave, el cliente no arranca; modelos vigentes con tarifa.

## Coste estimado de un ciclo semanal C1 (tarifa del 15-11-2026, USD)

| Tipos activos | Llamadas | Estimación | Cota superior |
| --- | --- | --- | --- |
| Solo divisas (configuración actual) | 8 | 0,86 | 1,68 |
| Los 12 tipos | 77 | 2,98 | 11,47 (con hasta 30 búsquedas web) |

No incluye lo que lee cada búsqueda (se cobra como entrada), reintentos ni reparaciones de JSON. Órdenes: `cd bloque_a/11_Ejecutor && ../../.venv/bin/python ../../.docs/scripts/medir_consumo_a.py <carpeta> [as_of] [--config yaml]` y, desde la raíz, `.venv/bin/python .docs/scripts/estimar_coste_ciclo_a.py <carpeta> [--config yaml]`.

## Criterios de aceptación (binarios)

1. CA-1: `test_t129_modo_sombra.py` en verde (10 pruebas).
2. CA-2: el estimador da la cifra de la tabla con las dos órdenes de arriba.
3. CA-3: `por_defecto.yaml` sin cambios; pruebas de la entrega «sin precios inventados» en verde; gate 12/12.

## Registro

- 2026-11-15 · ABIERTO · creado con nuevo_ticket.sh
- 2026-11-15 · EN QA · claude · implementado; decisiones en INC-T129-01
- 2026-11-15 · CERRADO · QA r01 APTO (revisor nuevo sin contexto); hallazgos (H-01 media: la cota superior no es una cota; H-02 y H-03 bajas) en T-136
