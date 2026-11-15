# T-154 · QA independiente

- **Revisor:** Claude, subagente revisor nuevo sin el contexto de la implementación (regla del 12-11-2026: Claude puede revisar lo suyo con un revisor nuevo) · **Ronda:** r01 · 15-11-2026

## Reproducción desde limpio

Copia: git worktree en el scratchpad sobre la instantánea `7535cc9`, con `.venv` enlazado; sin red, sin la API y sin gasto (SDK real sobre `httpx2.MockTransport` y SDK dobles). «Antes» es `git archive 1ccffd5 bloque_a`. Mutantes en copias desechables (`git archive HEAD bloque_a .docs tools`), borradas al acabar.

| Orden (desde la raíz de la copia salvo que se diga) | Resultado |
| --- | --- |
| `cd bloque_a/11_Ejecutor && ../../.venv/bin/python -m pytest -q -p no:cacheprovider` (una vez, en segundo plano) | **6624 passed, 2 skipped**, exit 0, 22 min 42 s |
| `… -m pytest -q -p no:cacheprovider tests/test_fase3_goldens.py tests/test_t154.py tests/test_t151_reintentos.py` · `python tests/goldens_ct.py` | 192 passed · «goldens de contratos: coinciden» |
| `.venv/bin/python tools/refs_vivas.py` · `secrets_scan.py` · `nfc_check.py` · `corpus_integridad.py` | exit 0 los cuatro; corpus **695** archivos coinciden |
| `.venv/bin/ruff check --output-format=concise bloque_a/11_Ejecutor bloque_a_forex/11_Ejecutor bloque_b/11_Ejecutor \| wc -l` | **2831** (cuota 2831) |
| `.venv/bin/mypy --ignore-missing-imports --no-error-summary bloque_a/11_Ejecutor/bloque_a \| wc -l` | **109** (cuota 109) |
| `.venv/bin/python -I .docs/tickets/T-151/revisores/r01_01_reintentos_unidad.py bloque_a/11_Ejecutor` | 9/9 OK, 3 OBS (X9: «cargado sin respuesta 1» en 501, 505, 520 y 500 con `false`; X10: «retry-after 100000 → espera None») |
| `… r01_02_ciclo_reintentos.py bloque_a/11_Ejecutor <tmp> --tipos RV,RF,DIV,MP --hilos 4 --cache --orden directo\|inverso --veces 2` | **IGUAL** (`dd00a82d0692`) en los dos órdenes y entre ellos; sin violaciones |
| `… --tipos <los 12> --hilos 6 --cache --orden directo\|inverso --veces 2` | **IGUAL** (`6d904b8a497b`) en los dos; sin violaciones |
| `… --veces 2` (DIV) · `--tipos RV,RF,DIV,MP --hilos 4` · `--sin-tipos` | IGUAL y sin violaciones (su «OBS: fallo de AG-19 no declarado en F5» es un texto fijo del script de T-151: ver `r01_02_ciclo_f9.py`) · sin violaciones · sin violaciones |
| `.venv/bin/python -I .docs/tickets/T-146/revisores/r02_01_arreglos_r02.py bloque_a/11_Ejecutor <tmp>` | **28/28 OK** |
| `bash .docs/tickets/T-146/comparar_ciclos.sh <1ccffd5>/bloque_a/11_Ejecutor bloque_a/11_Ejecutor <tmp> .venv/bin/python` | solo difieren `bt/salida/consumo.csv` y `doce/estado/cache_resultados.jsonl` (cambian entre dos pasadas iguales); **F5 sin campos distintos ni entradas nuevas** en ningún RUN |
| `cd bloque_a/11_Ejecutor && PYTHONPATH=$PWD ../../.venv/bin/python ../../.docs/scripts/medir_consumo_a.py <tmp>/m_div 2024-03-29`; `.venv/bin/python .docs/scripts/estimar_coste_ciclo_a.py <tmp>/m_div` | 8 llamadas; cota 28,04 USD (igual que antes); S5 dice «los reintentos ante un fallo del proveedor (T-151: los hace el cliente, no el SDK, y cada uno reserva…)» |

### Mutantes

| Script | Copia | Resultado |
| --- | --- | --- |
| `.docs/tickets/T-154/mutantes_t154.py` | `…/qa25_muts/t154_mut` | **18/18** muertos |
| `.docs/tickets/T-151/mutantes_t151.py` | `…/t151_mut` | **18/18** |
| `.docs/tickets/T-151/revisores/r01_03_mutantes_qa.py` | `…/qa24_t151_mut` | **16/16** (Q09 y Q10 muertos) |
| `.docs/tickets/T-146/mutantes_t146.py` | `…/t146_mut` | **35/35** |
| `.docs/tickets/T-146/revisores/r02_02_mutantes_qa.py` | `…/qa21_t146_mut` | **10/10** |
| `.docs/tickets/T-148/revisores/r02_02_mutantes_qa.py` | `…/qa21_t148_mut` | **5/5** |
| `.docs/tickets/T-154/revisores/r01_03_mutantes_qa.py` (propios, R01–R11) `--scripts` | `…/qa25_r0103_mut` | **8/11** muertos con las pruebas; **R01, R02 y R03 vivos** (H-02 de esta QA); con `r01_01` ampliado (U07), los tres los detecta el script del revisor |

## Scripts del revisor (`revisores/`, en este orden)

1. `.venv/bin/python -I .docs/tickets/T-154/revisores/r01_01_unidad_t154.py bloque_a/11_Ejecutor` — unidad: U01 matriz de 20 estados × 6 valores de `x-should-retry` (0 discrepancias con README e INC-T146-01); U02 cobro de punta a punta con el SDK real (cada petición cobrable se carga una vez, las demás se sueltan, peticiones HTTP = reservas, nada colgado; 9 guiones); U03 bordes de `retry-after` (tope exacto, tope + 1e-6, `-ms`, espacios, «+5», `1e400`, «-0», «0x10», `httpx2.Headers`); U04 503/529/500 con `retry-after` 10 veces el tope (sin dormir, `error_proveedor`, el 503 y el 500 cargados una vez, el 529 suelto) y tope 0; U05 H-03 con 200 órdenes aleatorios (semilla fija) por V5 y V6: con la marca, el mismo reparto en todos y ninguna bolsa ocupa más tras liquidar (sin la marca, 4 de 8 y 8 de 8 llamadas fallidas daban más de un reparto); U06 factor observado de T-146 igual con 0, 1 y 2 reintentos; U07 F9 con cada lista sola. **Todo OK.**
2. `.venv/bin/python -I .docs/tickets/T-154/revisores/r01_02_ciclo_f9.py bloque_a/11_Ejecutor <tmp>` — ciclos completos (DIV, N2) con AG-19 que falla de ocho formas: sin fallo (sin F9), timeout y 501 (F9 con una petición; el 501 sin reintento y la auditoría «auditor no disponible» en HA), 529 y 529 siempre (sin F9), exceso (F9 con `excesos_reserva`), mixto (AG-05 en el RUN, AG-19 en la F9), cierre (AG-17 agota COMÚN y AG-19 no cabe: F9 solo con el cierre) y dos ciclos en el mismo estado (`F5F9-2024-0001`/`0002` con su `run_id`). En todos: el RUN es idéntico al de referencia (salvo lo de antes del RUN), lo declarado en F5 = lo cobrable del SDK, `presupuesto` de la F9 = el del resultado, sin reservas colgadas, `verificar_integridad()` en verde, `estado("F5")` por id y una consulta C3 después funcionan. **Todo OK.**
3. `.venv/bin/python .docs/tickets/T-154/revisores/r01_03_mutantes_qa.py <copia con «qa25_» y «_mut»> --scripts` — R01–R11 (arriba).

## Criterios de aceptación

| Criterio | Cumple | Evidencia |
| --- | --- | --- |
| CA-1 (H-01) | sí | `r01_01` U01 y U02; X9 de `r01_01` de T-151; `test_t154_h01_*`. La línea de `test_la_clasificacion_de_los_errores` que pasa de (False, False) a (False, True) es la expectativa correcta: un 500 es de la clase 5xx, el servidor pudo ejecutarlo, y lo que cambia es que se **carga** (más prudente), no se relaja nada; sin H-01 (P01) esa línea falla. README e INC-T146-01 dicen lo mismo («5xx salvo 529»; «salvo los de `estados_sin_cobro`») |
| CA-2 (H-02) | sí | `r01_02_ciclo_f9.py` (timeout, 501, exceso, cierre, mixto, dos ciclos; sin F9 sin fallo ni con 529); `comparar_ciclos.sh` sin campos distintos. Las pruebas no fijan cada lista por separado (H-02 de esta QA, bajo) |
| CA-3 (H-03) | sí | `r01_02` de T-151 con 4 y 12 tipos en los dos órdenes: IGUAL; `r01_01` U05 (200 órdenes, V5 y V6) sin pasar límites |
| CA-4 (H-04) | sí | `r01_01` U03/U04; `test_t154_h04_*`; `r01_03` de T-151 16/16 |
| CA-5 (H-05) | sí | Lectura del CA-7 de T-151, su análisis y pruebas, INC-T129-01 (límites y cota del ciclo) y la salida S5 del estimador; `grep "reintentos del SDK"` en `docs/incidencias.md`, el README del ejecutor y el estimador: nada |
| CA-6 | sí | mutantes de T-154 18/18, T-151 18/18, `r01_03` de T-151 16/16, T-146 35/35, `r02_02` de T-146 10/10 y de T-148 5/5 |
| CA-7 | sí | suite completa 6624/2, goldens, gates ligeros, scripts de T-151 y `r02_01` de T-146, `comparar_ciclos.sh`; ruff 2831 y mypy A 109 |

## Hallazgos

| ID | Gravedad | Cómo reproducirlo | Esperado / obtenido | Corrección sugerida | Estado |
| --- | --- | --- | --- | --- | --- |
| H-01 | baja | `r01_01_unidad_t154.py`, líneas «OBS cobro_posible_desde=…» | Esperado: una clave nueva que decide si se carga una petición falla cerrado ante un valor fuera de su dominio (como `estados_sin_cobro ⊆ estados_reintentables`). Obtenido: `ReglaReintentos.de_config` acepta cualquier entero ≥ 0 (0, 100, 599, 600, 10⁶). Con 600 o más, H-01 se desactiva en silencio y un 501/520 o un 500 con `x-should-retry: false` vuelve a soltarse como no cobrado (falla abierto en la cuenta); con 0, cualquier 4xx cuenta como cobrado (prudente). Solo con una configuración mal escrita | Exigir `100 ≤ cobro_posible_desde ≤ 599` (o no mayor que el menor 5xx de `estados_reintentables`) con su prueba en `test_t154_las_claves_nuevas_invalidas_fallan_cerrado` | abierto (ticket nuevo) |
| H-02 | baja (pruebas) | `r01_03_mutantes_qa.py <copia qa25_…_mut>`: R01, R02 y R03 vivos | Esperado (CA-2: «y lo mismo con un cierre de AG-19»): una prueba que falle si `TramoPresupuesto.algo()` olvida los cierres, los recortes o los excesos. Obtenido: la única prueba (`test_t154_h02_los_cierres_y_excesos_tras_el_run_tambien`) anota los tres juntos, así que quitar cualquiera de `algo()` no la rompe. El código está bien (`r01_02` «cierre» y «exceso» en ciclos reales, `r01_01` U07 por lista) | Parametrizar esa prueba por lista (solo un cierre, solo un recorte, solo un exceso) o copiar U07 de `r01_01` a `tests/test_t154.py` | abierto (ticket nuevo) |

Observaciones (sin hallazgo):

- **H-03 cobra de más a propósito.** En un grupo marcado se cobra el peor caso de la fallida (que ya cuenta toda su entrada como escrita, prefijo incluido) y además la prima «solo» de cada bolsa: con 3 bolsas y un prefijo de 20 000 tokens, 2,25 UC más que sin el fallo (`r01_01` U05). Es prudente, determinista, no pasa ningún límite y está declarado («se carga más que lo escrito»); no está dicho que el prefijo pueda contar dos veces.
- **`retry-after-ms` manda** sobre `retry-after`: uno por encima del tope con un `retry-after: 1` válido no se reintenta (`r01_01` U03). Es el orden del SDK y falla cerrado.
- **Ruta de excepción:** si `agentes.invocar` lanzara una excepción después de una petición sin respuesta cobrable, `_invocar` la relanza sin marcar el grupo (la reserva sí se carga). En la V5 el grupo de un analista es él mismo; solo afectaría a un agente compartido que además falle con una excepción. No reproducido en un ciclo.
- **Interacción con T-146:** en el escenario «cierre», el exceso de AG-17 sube el factor observado de COMÚN (≈ 400) y el peor caso de AG-19 pasa a 459,69 UC; la petición no sale y su cierre queda en la F9. Correcto por T-146.
- Fuera del alcance (T-151): un `APIResponseValidationError` (respuesta 200 que no valida; solo con validación estricta, desactivada por defecto) se clasifica (False, False) y no se carga.

Invariantes del sistema: ningún camino nuevo llega a una orden sin F y G (T-154 solo toca el cliente LLM, el presupuesto y F5); no hay LLM en la ruta determinista ni en los controles; los controles no se relajan (H-01 carga más, H-04 deja de reintentar, H-03 reparte la cota); falla cerrado y valida antes de crear el cliente (salvo el rango de H-01); los dos números nuevos están en `config/por_defecto.yaml` con su origen y `[PROPUESTO]`, sin ninguno escrito a mano en el código; las decisiones están en INC-T146-01 (ronda T-154) con la pregunta al operador (T-57); sin secretos ni datos personales (gate en verde; la clave de los scripts es «clave-falsa-qa»). El briefing no cambia (no hay arquitectura nueva); la deuda técnica no la toca este revisor.

No comprobado: el comportamiento real de la API (qué 5xx cobra, `retry-after` reales) sin red ni gasto; `./tools/check_all.sh` entero (A-Forex y B no se tocan: gates ligeros, cuotas y suite de A, sí).

## Veredicto

**APTO** · los siete criterios se cumplen con evidencia y no hay hallazgos críticos ni altos. H-01 (rango de `cobro_posible_desde`) y H-02 (pruebas de F9 por lista) son bajos y van a un ticket nuevo. Este revisor no cierra el ticket ni toca la deuda técnica.
