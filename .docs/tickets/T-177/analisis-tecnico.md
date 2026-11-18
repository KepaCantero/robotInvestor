# T-177 · Análisis técnico

## Causa raíz

PB-58 (plan V3.0) pide los pasos 1 y 2 del 7.10 del Documento 0 V5.3: el Buscador de Fuentes Avanzadas (AG-16) declara en su retorno del mantenimiento C4 las credenciales que faltan en la bóveda de HT-01 (`solicitudes_credenciales`), y el Coordinador (AG-01) deduplica, comprueba en HT-01 y emite el CT-25. El ejecutor tenía la mitad del circuito a partir de `Credenciales.solicitar` (orden `credencial solicitar`), pero no tenía mantenimiento C4 ni leía `solicitudes_credenciales` de ningún retorno (INC-T116-03, r05).

## Implementación

| Archivo | Cambio |
| --- | --- |
| `bloque_a/11_Ejecutor/bloque_a/mantenimiento_c4.py` (nuevo) | `servicios_bfa(cfg)` valida `credenciales.servicios_bfa` (falla antes de mutar); `mantenimiento_c4(bloque, as_of)` arma el encargo de AG-16 con el estado de la bóveda de cada servicio (solo `servicio`, `uso_previsto`, `impacto_si_falta`, `credencial_ref`, `estado`), lo invoca por `_invocar` con el esquema `BUSQUEDA` y la bolsa C4 del Anexo A, pasa el retorno al Coordinador y escribe la C4- en F5 (`tipo_entrada: C4_CREDENCIALES`) |
| `bloque_a/11_Ejecutor/bloque_a/interfaz_broker.py` | `Credenciales.desde_retorno(retorno, solicitante, as_of, origen)`: rechaza íntegro un retorno con un campo de valor o un patrón de `contiene_credenciales` (incidencia SEGURIDAD en HA sin copiar el dato, ningún CT-25); valida cada solicitud (servicio, motivo e impacto de texto, o se descarta con motivo), deduplica por `alias_de`, normaliza la urgencia (ALTA o NORMAL) y llama a `solicitar` (que comprueba HT-01, lo abierto y lo denegado y emite el CT-25). `CAMPOS_VALOR` pasa a salir de `contratos.CAMPOS_VALOR_CREDENCIAL` (mismo conjunto) |
| `bloque_a/11_Ejecutor/bloque_a/contratos.py` | `CAMPOS_VALOR_CREDENCIAL` y `claves_valor_credencial(obj)` (campos de valor a cualquier profundidad). No cambia `CANALES`, `ESQUEMAS` ni ningún golden |
| `bloque_a/11_Ejecutor/bloque_a/agentes.py` | Un retorno cuyo `solicitudes_credenciales` trae un campo de valor se bloquea por R8 como los demás secretos: sin esto, el valor se guardaba en `cache_resultados.jsonl` antes de que el Coordinador lo rechazara (lo encontró `test_t177_c4_con_valor_en_el_retorno_del_bfa_no_emite_nada`) |
| `bloque_a/11_Ejecutor/bloque_a/mock_respuestas.py` | AG-16 con `tipo: MANTENIMIENTO_C4`: pide lo que no está PROVISTA. Los demás encargos de AG-16 no cambian |
| `bloque_a/11_Ejecutor/bloque_a/cli.py` | `credencial c4` |
| `bloque_a/11_Ejecutor/config/por_defecto.yaml` | `credenciales.servicios_bfa: []` `[PROPUESTO]` y `mantenimiento_c4.presupuesto_uc_semana` (DOC-A 3, BFA 3, DOC-M 2: la fila del Anexo A). Fuera de `presupuesto_uc` para no cambiar el P-17 de F10 |
| `bloque_a/11_Ejecutor/tests/test_t177_c4_credenciales.py` (nuevo) | 16 pruebas (ver `pruebas.md`) |
| `tests/mapa_plan_pruebas.json`, `tests/MAPA_PLAN_DE_PRUEBAS.md` | PB-58 → AUTOMATICA, con las pruebas nuevas y sin «No comprueba» |
| `bloque_a/11_Ejecutor/README.md` | Orden `credencial c4`, nota de T-177 y el módulo en la tabla |
| `docs/incidencias.md` | INC-T177-01 `[PROPUESTO]` y la nota «Aplicada en T-177» en INC-T116-03 (PB-58, r05) |
| `docs/evidencias_pruebas_bloque_a.md` | Regenerado con `evidencias_plan_a.py --ejecutar` |

## Decisiones y desviaciones del plan

- **Sin canal nuevo.** El retorno del BFA no pasa por la mensajería (como el de CT-07); el CT-25 sale AG-01 → BROKER. Así los goldens de contratos coinciden (`goldens_ct.py`: «coinciden»).
- **Esquema del retorno.** `BUSQUEDA`, sin esquema nuevo (lo prohíbe el encargo); el Coordinador valida `solicitudes_credenciales`.
- **Desviación: la capa de agentes.** El plan no tocaba `agentes.py`. Hizo falta para cumplir R8: la caché de resultados guardaba el retorno con el valor. El cambio solo mira `solicitudes_credenciales` (un campo `valor` o `token` es corriente en otros retornos).
- **Campo `impacto`.** Se acepta también `impacto` como sinónimo de `impacto_si_falta` (el prompt del BFA dice «impacto si falta»). En INC-T177-01.
- **El presupuesto** de la llamada es la bolsa semanal del BFA (3 UC); no se lleva la cuenta entre llamadas de la misma semana (INC-T177-01).

## Límites conocidos

- El otro origen del paso 1 (el retorno parcial del CT-05, con las solicitudes de los Analistas que eleva el Analizador) sigue sin leerse (INC-T116-03). `desde_retorno` sirve para ese caso cuando se implemente.
- El resto del C4 (barridos HT-02, Novedades, CT-21) no está en `credencial c4`.
- Sin lista de servicios en la configuración por defecto, el simulado no pide nada; con el cliente real, el BFA puede pedir lo que vea necesario.

## Cómo probarlo

```bash
cd bloque_a/11_Ejecutor
../../.venv/bin/python -m pytest -q tests/test_t177_c4_credenciales.py      # 16
../../.venv/bin/python tests/goldens_ct.py                                   # coinciden
cd ../..
.venv/bin/python .docs/tickets/T-177/mutantes_t177.py                        # 12/12 muertos
.docs/tickets/T-177/ciclo_mock_t177.sh                                       # CLI de punta a punta, cliente simulado
.venv/bin/python .docs/scripts/evidencias_plan_a.py --pb PB-58
```

## Ronda r02 (QA r01 NO APTO, `qa.md`)

| Hallazgo | Corrección | Archivo |
| --- | --- | --- |
| H-01 (alta) y H-04 (alta) | `llm.solicitud_con_valor(texto)` en `respuesta_segura`, antes de la caché y de la cinta: si el texto nombra `solicitudes_credenciales` (clave normalizada), se lee el tramo `{…}` y es sensible un campo de valor con texto en **todo** el dict, o una ficha opaca en las solicitudes; ilegible o demasiado anidado, sensible (falla cerrado). `agentes.invocar` la repite como segunda barrera sobre `datos` y al leer la caché (una entrada envenenada no se sirve) | `llm.py`, `agentes.py` |
| H-02 (media) | `solicitar` busca lo previo por `alias_de` | `interfaz_broker.py` |
| H-03 (media) | `solicitar`, tras el caso PROVISTA, comprueba y escribe dentro de `almacen._transaccion()` (exclusión entre hilos y procesos; el precedente es `respuesta_final.py`) | `interfaz_broker.py` |
| H-05 | `clave_normalizada` (minúsculas, solo `[a-z0-9ñ]`) y `CAMPOS_VALOR_CREDENCIAL` ampliado con la lista de la QA; `interfaz_broker.CAMPOS_VALOR` es el mismo conjunto y `responder` compara la clave normalizada | `contratos.py`, `interfaz_broker.py` |
| H-06 | `contratos.RE_FICHA_OPACA` con `LONGITUD_MIN_VALOR_OPACO` (16), la constante que ahora usa también `RE_VALOR_GENERICO` (mismo patrón que antes); `desde_retorno` rechaza el retorno entero, antes de pedir nada, si el servicio, el motivo o el impacto de alguna solicitud la tiene. El caso LEI, documentado en INC-T177-01 | `contratos.py`, `interfaz_broker.py`, `llm.py` |
| H-07 | (a) sin servicios no se llama a AG-16 (`SIN_SERVICIOS`, 0 UC); (b) la C4- guarda `uc` y `uc_semana_disponible`; la bolsa de la llamada es la semanal menos lo gastado por las C4- de AG-16 de los 7 días hasta `as_of` (`HT-05 FRECUENCIAS["semanal"]`); si no queda, o la llamada no cabe, `SIN_PRESUPUESTO` | `mantenimiento_c4.py` |

Desviaciones de la corrección sugerida:
- `solicitud_con_valor` solo cuenta un campo de valor que lleva texto (`claves_valor_credencial(…, solo_texto=True)`): un `valor` numérico de un retorno corriente que, además, trae `solicitudes_credenciales` no se bloquea. El backtest mock no da falsos positivos (ver `pruebas.md`).
- La ficha opaca también se comprueba en `respuesta_segura`, no solo en `desde_retorno`: si no, el caso `motivo_sin_etiqueta` del revisor dejaba el valor en la caché antes del rechazo.
- Una llamada que no cabe en lo que queda de la bolsa (la reserva del peor caso de T-146) da `SIN_PRESUPUESTO`, no `SIN_RESULTADO`.

Además: evidencias de PB-58 con «Superada con su preparación» (la fila del mapa lo dice) y la fila T-179 de la deuda (pendiente del operador: declarar `credenciales.servicios_bfa`).

## Ronda r03 (QA r02 NO APTO)

| Hallazgo | Corrección | Archivo |
| --- | --- | --- |
| H-12 (alta) | `contratos.retorno_con_credencial`. Dentro del subárbol `solicitudes_credenciales`, lo de H-08 y H-11. Fuera, solo las claves inequívocas de `CAMPOS_VALOR_CREDENCIAL` con texto, y las de `CAMPOS_VALOR_AMBIGUOS` (`valor`, `clave`, `token`, `credencial`) solo con ficha opaca. El simulado de los Analistas devuelve `solicitudes_credenciales: []` e `indicadores[].valor` de texto («0,61»), así que el backtest y los ciclos ejercitan siempre la barrera | `contratos.py`, `llm.py`, `mock_respuestas.py` |
| H-08 (alta) | Con alguna solicitud no vacía, una ficha opaca en cualquier clave u hoja de texto del retorno, subárbol incluido y a cualquier profundidad, hace sensible el retorno. `_subarbol_sensible` añade las claves de valor dentro de un texto que es JSON. Es la misma regla en `llm.solicitud_con_valor` y en `Credenciales.desde_retorno`, que la aplica antes de comprobar si la lista es una lista. Los mutantes M21 y M26 de la primera pasada eran equivalentes: la ficha opaca del subárbol ya la ve la pasada sobre el retorno entero. Se quitó esa comprobación duplicada | `contratos.py`, `interfaz_broker.py` |
| H-09 (media) | `solicitud_con_valor` lee primero el JSON (`_leer_json`, como `agentes.extraer_json`) y decide con él; el prefiltro textual solo actúa si no se puede leer | `llm.py` |
| H-10 | `contratos.ficha_opaca(t)`: `RE_FICHA_OPACA` o una palabra entera sin «.» ni «:» con forma de base64 (`RE_PALABRA_BASE64`) | `contratos.py` |
| H-11 | Dentro del subárbol, un número (no un booleano) bajo una clave de valor cuenta | `contratos.py` |
| H-13 | `RE_FICHA_OPACA` sin `-` ni `_` en la ficha: son separadores de tramo. UUID declarado en INC-T177-01 | `contratos.py` |
| Observación (bolsa) | `uc_c4_semana` se lee dentro de `almacen._transaccion()` y la C4 reserva lo que queda (C4- `EN_CURSO`). `uc_c4_semana` cuenta cada C4- una vez, por su último `uc`. Si la llamada falla, la reserva pasa a `ERROR` con lo gastado | `mantenimiento_c4.py` |

Desviaciones y extensiones:
- Si alguna solicitud no está vacía, el retorno entero se mira por fichas opacas. Así se bloquean los casos `en_lagunas` y `sintesis_con_json` del revisor, que estaban entre los HALLAZGO_H08. A un informe de Analista con la lista vacía no se le aplica.
- Pruebas del revisor adaptadas, sin tocar ninguna aserción HALLAZGO salvo para invertirla:
  - `r01_ataques_r8.py::test_r01_c4_concurrente_dos_bloques` y `r02_concurrencia_presupuesto.py::test_r02_h07_carrera_del_presupuesto` ponían una barrera que exige dos C4 a la vez dentro de `solicitar` o de `uc_c4_semana`. Con la reserva bajo la transacción, eso ya no puede pasar.
  - La primera ejerce ahora la carrera de H-03 en `desde_retorno`, y además dos C4 a la vez (una sola CRD-).
  - La segunda ensancha la ventana con una espera y comprueba que no se pasa de la bolsa (COMPLETO y SIN_PRESUPUESTO).

## Ronda de cierre de la QA r03 (APTO con H-14 a H-17 bajos)

| Hallazgo | Corrección | Archivo |
| --- | --- | --- |
| H-14 | El último `return` de `solicitud_con_valor` mira también el texto con los `\uXXXX` resueltos (`or`) | `llm.py` |
| H-15 | `contratos._publico`: dirección `0x` de 40 o LEI con módulo 97. Se quita del texto antes de buscar la ficha opaca de las claves ambiguas en `_fuera_sensible`, solo fuera del subárbol. No se aplica en el barrido del retorno entero, para que la prueba del revisor `lei_en_finalista_con_solicitud` siga en verde (INC-T177-01) | `contratos.py` |
| H-16 | `pid` en la reserva `EN_CURSO`. `reservas_huerfanas()` rellena `reservas_en_curso` en la C4- `SIN_PRESUPUESTO` y deja una sola incidencia Operativa por reserva de un proceso muerto, sin liberarla | `mantenimiento_c4.py` |
| H-17 | `CAMPOS_SOLICITUD`: en el subárbol, cualquier otra clave con contenido es sensible | `contratos.py` |

## Segunda ronda de cierre de la QA r03 (H-18)

| Hallazgo | Corrección | Archivo |
| --- | --- | --- |
| H-18 | En `_subarbol_sensible`, por cada dict: la clave se compara tal cual con `CAMPOS_SOLICITUD_LITERALES`; es sensible, con contenido, una `urgencia` que no está en `URGENCIAS` (`ALTA`, `NORMAL`) y un `impacto` cuando el dict también tiene `impacto_si_falta` | `contratos.py` |

Efecto en `desde_retorno`: una urgencia fuera de la lista ya no se reduce a NORMAL, porque el retorno se rechaza antes (`retorno_con_credencial`). Se ajustaron dos pruebas propias que daban por buenos esos casos.

## Tercera ronda de cierre de la QA r03 (H-19)

En la segunda ronda de cierre retiré el mutante M08 por equivalente, y era un error. Una urgencia sin contenido (`" "`, `[""]` o `{"": ""}`) no es un valor, así que pasa la barrera y llega a `desde_retorno`, que la reduce a NORMAL. Con M08, la CRD- de F5 y el CT-25 llevarían el valor crudo, y ninguna prueba lo veía. Ahora M08 vuelve a `mutantes_t177.py`, como estaba en `5f98163`. La prueba que lo mata es `test_t177_cierre3_h19_urgencia_sin_contenido_se_reduce_a_normal` (×3): da SOLICITADA, y tanto la CRD- como el CT-25 llevan `urgencia == "NORMAL"`. El código no cambia.
