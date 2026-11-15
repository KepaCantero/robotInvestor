# T-154 · Bloque A: hallazgos bajos de la QA r01 de T-151 (5xx sin cobro, AG-19 en F5, determinismo con un fallo que escribe el prefijo, retry-after y x-should-retry, textos)

| Campo | Valor |
| --- | --- |
| Estado | CERRADO (QA r01 APTO) |
| Pieza | Bloque A (`bloque_a/11_Ejecutor`: `bloque_a/llm.py`, `bloque_a/consumo.py`, `bloque_a/orquestacion.py`, `config/por_defecto.yaml`, `README.md`; `tests/test_t151_reintentos.py`, `tests/test_t154.py`); `docs/incidencias.md` (INC-T146-01, INC-T129-01); `.docs/scripts/estimar_coste_ciclo_a.py` (texto de S5); textos de `.docs/tickets/T-151/` (CA-7 y cuotas) |
| Planifica · implementa · QA | claude · claude · el otro agente o un revisor nuevo |
| Aprobación del operador | no necesaria (correcciones, pruebas y textos de un ticket cerrado; lo nuevo, `[PROPUESTO]` en INC-T146-01) |
| Deuda técnica | T-154 en `sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md` (la fila la pone quien coordina en el árbol principal; este ticket no la toca) |

## Objetivo

Cerrar los cinco hallazgos bajos (H-01 a H-05) que dejó APTO la QA r01 de T-151 (`.docs/tickets/T-151/qa.md`, scripts en `.docs/tickets/T-151/revisores/`), antes del modo sombra.

## Alcance

- Entra:
  - **H-01.** `llm.clasificar_error`: todo estado 5xx (desde `llm.reintentos.cobro_posible_desde`) que no esté en `estados_sin_cobro` cuenta como cobro posible, se reintente o no (501, 505, 520, o un 500 con `x-should-retry: false`): se carga por su peor caso y queda en `peticiones_sin_respuesta`. Lo que declaran el README del ejecutor e INC-T146-01 («5xx salvo 529») pasa a ser lo que hace el código.
  - **H-02.** Lo que la auditoría (AG-19, F9) deja en el presupuesto después de escribir el RUN en F5 (peticiones sin respuesta, cierres, recortes y excesos) queda en F5 en una entrada propia, `PRESUPUESTO_F9`, que completa el RUN (solo si AG-19 dejó algo de eso).
  - **H-03.** `Presupuesto.liquidar_primas`: en un grupo de prefijos en el que una llamada tuvo una petición sin respuesta que pudo cobrarse, cada bolsa paga su prima «solo» entera (la cota que ya tenía retenida), en vez del reparto de lo escrito que se vio. Así no depende de qué hilo llegó antes.
  - **H-04.** Pruebas de Q09 (`retry-after` infinito, NaN o negativo no vale como espera) y Q10 (`x-should-retry` sin distinguir mayúsculas). Las cabeceras se leen sin distinguir mayúsculas en el nombre ni en el valor. Tope nuevo, `llm.reintentos.espera_servidor_max_s`: si el servidor pide esperar más, no se reintenta (falla cerrado).
  - **H-05.** Textos: el CA-7 del README de T-151 y las cuotas de su `analisis-tecnico.md` y `pruebas.md`; INC-T129-01 y la salida S5 de `estimar_coste_ciclo_a.py` («los reintentos del SDK»).
- No entra: A-Forex y B (su `max_retries`, H-05 c: un ticket por bloque antes de su modo sombra); la fila de la deuda técnica; el Documento 0 y los goldens; `bloque_a/cadena_b.py`, `motor/frontera_b.py`, `.docs/scripts/cadena_a_b.py`, `.docs/scripts/descargar_datos_bce.py`, `tests/test_t14[479].py` y `test_t150.py` (otra sesión); `sistema_global/marco_comun_c/`, la Constitución y el corpus; medir con la API.

## Diseño

| Hallazgo | Cambio |
| --- | --- |
| H-01 | En `clasificar_error`, si el estado es ≥ `regla.cobro_posible_desde` (500), cobro posible = no está en `regla.sin_cobro`, se reintente o no. Los 4xx no cambian (cobro posible solo si se reintentan: 408, 409 o `x-should-retry: true`) |
| H-02 | `Presupuesto.marca()` antes de `_auditar` y, después, `Bloque._registrar_f9`: si desde la marca hay peticiones sin respuesta, cierres, recortes o excesos, escribe en F5 `{"tipo_entrada": "PRESUPUESTO_F9", "id": F5F9-…, "run_id", "fase": "F9"}` con `_f5_presupuesto` del tramo (`Presupuesto.desde(marca)`: el resumen tras la auditoría y solo lo nuevo de las listas). El RUN no cambia (ni su orden ni su contenido) |
| H-03 | `Bloque._invocar`: si la llamada tuvo una petición sin respuesta que pudo cobrarse, marca su grupo de prefijos (`Presupuesto.grupo_sin_respuesta`). En `liquidar_primas`, un grupo marcado reparte `total` (la suma de los pesos «solo») en vez de lo escrito que se vio: cada bolsa paga su prima «solo». Es una cota superior de lo escrito (lo diferido de cada llamada es como mucho su peso) y lo que ya estaba retenido, así que ninguna bolsa pasa de su límite por ello |
| H-04 | `ReglaReintentos.espera` devuelve None si el servidor pide más de `espera_servidor_max_s`; `_crear` no reintenta entonces (`error_proveedor`). Un `retry-after` no finito, negativo o cero sigue sin valer (la espera de la regla). Cabeceras: nombres en minúsculas (`_cabeceras`) y valor de `x-should-retry` sin espacios ni mayúsculas |
| H-05 | Solo texto |

- Contratos y esquemas: no cambian (goldens).
- Estado persistido: sin versión nueva. F5 puede llevar una entrada nueva, `PRESUPUESTO_F9`, solo cuando AG-19 deja peticiones sin respuesta, cierres, recortes o excesos; los lectores de F5 filtran por `tipo_entrada` (`RUN`, `CNS`, `CRD`, `QRY`…) y su `id` (`F5F9-AAAA-NNNN`) no choca con el del RUN.
- Números nuevos, en `config/por_defecto.yaml` con su origen, `[PROPUESTO]`: `llm.reintentos.cobro_posible_desde` 500 (RFC 9110 §15.6, la clase 5xx; el SDK 2.8 reintenta todo ≥ 500 en `_should_retry`) y `llm.reintentos.espera_servidor_max_s` 600 (lo que se espera una respuesta, `llm.timeout_s`; el SDK 2.8 solo pone el tope de la plataforma, 4 294 967 s).
- Cómo falla cerrado: un 5xx dudoso se carga por su peor caso; un `retry-after` mayor que el tope no se reintenta; una clave ausente es `KeyError` y un valor inválido, `ValueError`, antes de crear el cliente.
- Decisiones `[PROPUESTO]` (INC-T146-01, ronda T-154): las cinco de arriba; el tope de la espera, con su pregunta al operador (T-57).

## Riesgos

| Riesgo | Consecuencia | Mitigación |
| --- | --- | --- |
| La entrada nueva de F5 rompe un lector | Un RUN mal leído | Solo se escribe con fallos de AG-19; `id` propio; los lectores filtran por `tipo_entrada` (búsqueda en el código); suite completa |
| Cambiar líneas que citan los mutantes de T-146, T-148 y T-151 | Sus scripts darían «NO APLICA» | Se conservan las líneas citadas (Q05, Q09, Q10, Q15, N11, N13, N16, N17, Q12 de r01_05…); se pasan todos los scripts de mutantes |
| H-03 carga más en los grupos con un fallo | Fases que cierran antes | Solo con peticiones sin respuesta; es la prima ya retenida; prudente y declarado |
| El tope de la espera corta un reintento que habría salido | Un `error_proveedor` más | 600 s, lo mismo que se espera una respuesta; decisión del operador (T-57) |

## Criterios de aceptación (binarios)

1. CA-1 (H-01): un 501, 505, 520 y un 500 con `x-should-retry: false` no se reintentan y se cargan por su peor caso (`peticiones_sin_respuesta`); un 529 y un 429 siguen sin cargarse; un 400 sigue sin cargarse; el README e INC-T146-01 dicen lo mismo.
2. CA-2 (H-02): en un ciclo en el que la petición de AG-19 no responde, F5 tiene una entrada `PRESUPUESTO_F9` del RUN con esa petición en `peticiones_sin_respuesta` (y lo mismo con un cierre de AG-19); sin fallos de AG-19 no hay entrada nueva y el RUN de F5 es idéntico al de antes (`comparar_ciclos.sh` sin campos distintos).
3. CA-3 (H-03): `r01_02 … --tipos RV,RF,DIV,MP --hilos 4 --cache --orden directo|inverso --veces 2` da IGUAL en los dos órdenes y entre ellos (y con los 12 tipos y 6 hilos); sin violaciones; una prueba unitaria da el mismo reparto con el fallo en cualquiera de los dos órdenes.
4. CA-4 (H-04): `retry-after` (y `-ms`) «inf», «nan», «-5» y «0» dan la espera de la regla; uno mayor que `espera_servidor_max_s` no se reintenta; `x-should-retry` «True», « FALSE » y el nombre en mayúsculas se respetan; Q09 y Q10 de `r01_03_mutantes_qa.py` muertos (16/16).
5. CA-5 (H-05): el CA-7 de T-151, su `analisis-tecnico.md` y `pruebas.md`, INC-T129-01 y la salida S5 del estimador dicen lo que hay (ruff 2831 en `tools/cuotas.txt`; reintentos del cliente con su reserva).
6. CA-6: los mutantes de `mutantes_t151.py` (18/18), `r01_03` de T-151 (16/16), `mutantes_t146.py` (35/35), `r02_02` de T-146 (10/10) y de T-148 (5/5), y los propios de T-154 (`mutantes_t154.py`) muertos.
7. CA-7: las suites citadas, los scripts `r01_*` de T-151 y `r02_01` de T-146, `comparar_ciclos.sh`, los goldens, los gates ligeros y la suite completa de A en verde; cuotas ruff ≤ 2831 y mypy A ≤ 109.

## Plan de pruebas

| Prueba (`tests/test_t154.py` salvo que se diga) | Tipo | Criterio |
| --- | --- | --- |
| `test_t154_h01_un_5xx_que_no_se_reintenta_se_carga_por_su_peor_caso` (501, 505, 520, 500 y 503 con `x-should-retry: false`; SDK real) | regresión, fallo cerrado | CA-1 |
| `test_t154_h01_lo_que_el_servidor_rechaza_sin_ejecutar_sigue_sin_cargarse` (529, 429, 400, 404) y `test_t154_h01_la_clasificacion_de_los_5xx_sale_de_la_configuracion` | límite | CA-1 |
| `test_la_clasificacion_de_los_errores` de `test_t151_reintentos.py` (el 500 con `x-should-retry: false` pasa a cobro posible) | regresión | CA-1 |
| `test_t154_h02_la_peticion_sin_respuesta_de_ag19_queda_en_f5`, `test_t154_h02_sin_nada_de_ag19_que_declarar_no_hay_entrada`, `test_t154_h02_los_cierres_y_excesos_tras_el_run_tambien` | regresión, integración | CA-2 |
| `test_t154_h03_con_un_fallo_el_reparto_no_depende_del_orden`, `test_t154_h03_un_grupo_sin_fallos_reparte_como_antes`, `test_t154_h03_el_grupo_de_un_analista_en_v6`, `test_t154_h03_en_el_ciclo_la_peticion_sin_respuesta_marca_su_grupo`; `r01_02` con caché en los dos órdenes | regresión, determinismo | CA-3 |
| `test_t154_h04_*` (espera no finita, negativa o cero; tope; mayúsculas en nombre y valor) y `test_t154_las_claves_nuevas_invalidas_fallan_cerrado`; casos de Q09 y Q10 en `test_la_espera_dobla_hasta_la_maxima_o_es_la_del_servidor` y `test_la_clasificacion_de_los_errores` de `test_t151_reintentos.py` | límite, fallo cerrado | CA-4 |
| Scripts de la QA de T-151, mutantes, `comparar_ciclos.sh`, goldens, gates, suite completa | regresión | CA-5 a CA-7 |

## Scripts

Usa `.docs/tickets/T-151/revisores/r01_0[123]_*.py`, `.docs/tickets/T-151/mutantes_t151.py`, `.docs/tickets/T-146/mutantes_t146.py`, `revisores/r02_0*_*.py` de T-146 y T-148, `.docs/tickets/T-146/comparar_ciclos.sh` y `.docs/scripts/medir_consumo_a.py`. Crea `.docs/tickets/T-154/mutantes_t154.py` (mutantes de lo que cambia T-154).

## Registro

- 2026-11-15 · ABIERTO · creado con nuevo_ticket.sh
- 2026-11-15 · PLANIFICADO · claude · plan y criterios (abierto como T-153; renumerado a T-154 por quien coordina: T-153 es de otra sesión)
- 2026-11-15 · EN QA · claude · implementado y probado (ver `analisis-tecnico.md` y `pruebas.md`)
