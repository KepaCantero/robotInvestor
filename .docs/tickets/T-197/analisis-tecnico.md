# T-197 · Análisis técnico

## Causa raíz o motivo

PB-09 (Plan de pruebas V3.0) pide que, tras un CT-04 con periodicidad QUINCENAL y entrega MIE 08:00, el siguiente C1 se dispare en la fecha nueva y ningún otro parámetro cambie. Estaba «Superada en parte» (INC-T159-01) por dos huecos:

1. El CT-04 componía P-01 como `f"{periodicidad} · {horario}"`: «SEMANAL · SAB 06:00 · entrega LUN 07:00» pasaba a «QUINCENAL · MIE 08:00» y se perdía la ejecución del ciclo.
2. `ht05_planificador.proxima_ejecucion` existía, pero nada la llamaba con el P-01 de F10: ningún código disparaba el C1 según F10.

## Evidencia

- Antes: `orquestacion.py`, `Bloque.decision`, línea `valor = v if pid != "P-01" else f"{periodicidad} · {horario}"`; `grep -rn proxima_ejecucion bloque_a` solo devolvía su definición.
- Con el CT-04 de develop, 8 de las 17 pruebas de la primera versión fallan (las de CA-1, CA-2 y CA-3); sin `planificacion_c1.py` el módulo de pruebas no se puede ni recoger.
- Ahora: `.docs/scripts/evidencias_plan_a.py --pb PB-09` → «Superada».

## Implementación

- **Archivos cambiados y por qué:**
  - `bloque_a/11_Ejecutor/bloque_a/herramientas/ht05_planificador.py`: `P01_INICIAL`, `P01Invalido` (subclase de `ValueError`), `dia_hora`, `ejecucion_para_entrega` (adelanto de la configuración, redondeo hacia abajo, franja sin disparos, diaria que caería el día anterior), `componer_p01` y `leer_p01` (tres partes; también las dos de antes), `es_dia_de_ejecucion` (diaria L-V, semanal, quincenal anclada en su primera ejecución, mensual días 1-7), `siguiente_ejecucion`, `ultima_ejecucion`, `entrega_de`. `proxima_ejecucion` y las demás funciones no cambian.
  - `bloque_a/11_Ejecutor/bloque_a/planificacion_c1.py` (nuevo): `proximo` (siguiente C1 con los cambios de P-01 ya conocidos: si uno rige antes del candidato, se recalcula desde su fecha de efecto con el P-01 nuevo), `ultimo_programado` (último C1 programado; si el P-01 vigente no tiene ninguno desde su inicio, baja al anterior) y `disparar` (ver INC-T197-01: reserva `DISPARO` en F5 dentro de `almacen._transaccion()`, EMITIDO, RECUPERADO o PERDIDO, ciclo con `disparador` y cierre con `run_id`/`estado_run` o FALLIDO en un `finally`, sin capturar la excepción).
  - `bloque_a/11_Ejecutor/bloque_a/orquestacion.py`: un import; `_inicializar_f10` usa `ht05.P01_INICIAL`; en `decision`, solo la parte P-01 (lectura del P-01 vigente con `leer_p01`, cálculo y validación de la ejecución, valor con `componer_p01`). La parte de horizontes no se toca (T-189).
  - `bloque_a/11_Ejecutor/bloque_a/cli.py`: orden `planificar [--ejecutar]` (el parser junto a `ciclo` y el despacho al final, lejos de los cambios de Astra en ese fichero).
  - `bloque_a/11_Ejecutor/config/por_defecto.yaml`: sección `planificador` (tras `seguimiento`).
  - `bloque_a/11_Ejecutor/README.md`: la orden en §5.
  - `bloque_a/11_Ejecutor/tests/test_t197_periodicidad.py` (18 pruebas); `tests/test_t87_contratos.py` (la prueba de CT-04 espera el P-01 de tres partes); `tests/mapa_plan_pruebas.json` (PB-09 AUTOMATICA); `docs/evidencias_pruebas_bloque_a.md` (regenerado); `docs/incidencias.md` (INC-T197-01 y la nota de PB-09 en INC-T159-01); deuda técnica (fila T-197).
- **Decisiones y desviaciones del plan:** ninguna desviación. Las decisiones `[PROPUESTO]` están en INC-T197-01. La ejecución sale de la entrega con el adelanto de la especificación de HT-05 (§4: MIE 08:00 → LUN 07:00), no se conserva la del P-01 anterior: con «SAB 06:00» y entrega el miércoles, la ejecución quedaría cuatro días antes de la entrega.
- **Números:** solo los de `planificador` (de la especificación de HT-05). Los días (L-V, 1-7 del mes, 14 días de la quincenal) son las reglas de §4, no parámetros.
- **Límites conocidos:**
  - El ejecutor no tiene demonio: alguien (cron) llama a `planificar --ejecutar` cada hora. Un sondeo que llega tarde dentro de la hora sigue siendo EMITIDO (antes de la entrega).
  - El F10 inicial se escribe con la fecha real del sistema al crear el bloque: una simulación con `--as-of` anterior a la instalación no tiene P-01 y el planificador falla cerrado. Las pruebas fijan la fecha de instalación sustituyendo el reloj del bloque.
  - Los C1 lanzados a mano con `ciclo` no cuentan como disparos de HT-05 (podría haber dos C1 el mismo día si el operador lanza uno a mano en el día programado).
  - No se implementan C1-ENTREGA, C1-CONTROL, C4, C5 ni el personalizado.

## Ronda r02 (QA r01 NO APTO)

| Hallazgo | Corrección | Prueba de regresión |
| --- | --- | --- |
| H-01 (media) la quincena se reinicia con cualquier CFG- de P-01 | `decision`: un P-01 compuesto igual al vigente no escribe CFG- (`aplicado_en_f10.sin_cambio` en el RET- y `sin_cambio` en el acuse). Todo CFG- de P-01 lleva `semana_ancla_quincenal` explícita: de QUINCENAL a QUINCENAL se copia la del P-01 vigente (`ht05.ancla_de_p01`, que para un P-01 anterior a la r02 la calcula con su primera ejecución desde que rige); de otra periodicidad, `ht05.ancla_quincenal` (primera ejecución desde la fecha de efecto); None si no es quincenal. `_p01_en` la lee y `es_dia_de_ejecucion`/`siguiente_ejecucion`/`ultima_ejecucion` la usan (parámetro `ancla`) | `test_r02_h01_cambio_solo_de_hora_conserva_la_quincena` (A1), `…_ct04_identico_no_escribe_cfg_ni_reinicia_la_quincena` (A2), `…_cambio_de_dia_de_entrega_sigue_en_la_misma_quincena` (MIE → JUE: martes 23-06), `…_de_otra_periodicidad_a_quincenal_ancla_de_nuevo` |
| H-02 (media) disparo huérfano | La reserva DISPARO guarda `pid`. `_previo`: abierta (sin `estado_run` ni `cierre_huerfano`) y `_pid_vivo` False → se escribe una vez `cierre_huerfano` (`estado_run` FALLIDO, «proceso terminado», pid, fecha) y una incidencia Operativa en HA (`disparo_huerfano`), y la salida es FALLIDO, sin repetir el C1; vivo → EN_CURSO sin escribir; sin saberlo → DESCARTADO_DUPLICADO. El cierre va en `cierre_huerfano.estado_run` y no en `estado_run` de la entrada: el ataque A9 del revisor exige que la reserva siga sin `estado_run` tras el sondeo (las dos formas dicen FALLIDO; esta no confunde el cierre del sondeo con el del proceso que corrió el ciclo) | `test_r02_h02_proceso_muerto_deja_el_disparo_fallido_con_incidencia_y_sin_repetir` (proceso real que muere con `os._exit(9)`), `test_r02_h02_proceso_vivo_da_en_curso_sin_escribir`; la de concurrencia con hilos ahora espera EN_CURSO de los otros tres mientras el ciclo corre |
| H-03 (media) la orden `planificar` sin prueba | Prueba por `cli.main` (sin `--ejecutar`: PENDIENTE y ningún DISPARO; con `--ejecutar`: EMITIDO con RUN- real; otra vez: DESCARTADO_DUPLICADO), citada en el mapa de PB-09 | `test_r02_h03_orden_planificar_de_la_cli` |
| H-04 (baja) entrega en la franja sin disparos | `ejecucion_para_entrega` rechaza también la entrega entre las 02:00 y las 03:00 | tres casos nuevos en `test_ca1_rechaza_lo_que_ht05_no_puede_programar_sin_tocar_f10` |
| H-05 (baja) documentación | `pruebas.md`: fusión con la rama de Astra (también choca `docs/evidencias_pruebas_bloque_a.md`, que se regenera con `evidencias_plan_a.py --ejecutar` tras fusionar) y las 2 omitidas de `test_t149.py`; comentario de `planificador` en el YAML con todos los [PROPUESTO] (diaria 2 h, redondeo, borde de 24 h) | documentación |
| H-06 (baja) mutantes vivos R3, R6 a R11, R14 a R16 | Una prueba por mutante | `test_r02_h06_r3_…` a `test_r02_h06_r16_…` (diez) |

Los mutantes del revisor y los de las correcciones están en `mutantes.py` (M33 a M58).

## Ronda de cierre de la QA r02

| Hallazgo | Corrección | Prueba de regresión |
| --- | --- | --- |
| H-07 (baja) un pid reutilizado deja el disparo EN_CURSO | La reserva guarda `boot_id` y `arranque_proceso` (`identidad_proceso`). `_vive`: pid propio → vivo solo si el disparo está en `_ABIERTOS` (los que este proceso reservó y aún no cerró); pid ajeno vivo → vivo solo si coinciden el `boot_id` y la hora de arranque; sin forma de leerlos → None (DESCARTADO_DUPLICADO) | B2; `test_cierre_h07_pid_propio_que_este_proceso_no_abrio_cuenta_como_muerto`, `…_pid_vivo_de_otro_proceso_con_otra_hora_de_arranque_cuenta_como_muerto`, `…_pid_vivo_del_mismo_arranque_sigue_en_curso` (y con otro `boot_id`, FALLIDO) |
| H-08 (baja) el huérfano cerrado no se lee como el ciclo cortado | Se deshace la desviación de la r02: el cierre escribe `estado_run` FALLIDO y `motivo_cierre` «proceso terminado» en la entrada (`cierre_huerfano` queda con el pid y la fecha); `_previo` decide solo con `estado_run` | B3; `test_r02_h02_proceso_muerto…` comprueba ahora `estado_run` y `motivo_cierre` |

Mutantes nuevos: M59 a M65; M52 y M56 se reescriben para el código nuevo. La aserción `"estado_run" not in f5` del ataque A9 de la r01 queda sustituida por B3 (lo dice la QA r02), así que A9 falla ahora a propósito en esa línea.

## Segunda ronda de cierre de la QA r02

El código no cambia: H-09 y H-10 son huecos de prueba.

| Hallazgo | Prueba |
| --- | --- |
| H-09 (baja) nada ataba que `arranque_proceso` fuera la hora de arranque | `test_cierre2_h09_arranque_proceso_es_la_hora_de_arranque_del_proceso`: con un `sleep` nuevo, `btime` (de `/proc/stat`) + `arranque_proceso` / `SC_CLK_TCK` queda a menos de 2 s del instante anterior al `Popen`; y la identidad del propio proceso no cambia al reservar 64 MB |
| H-10 (baja) la rama «no se puede saber» sin prueba | `test_cierre2_h10_boot_id_ilegible_no_se_puede_saber` (`RUTA_BOOT_ID` a un fichero inexistente) y `test_cierre2_h10_reserva_sin_identidad_no_se_puede_saber` (reserva con solo el pid): DESCARTADO_DUPLICADO, F5 y HA sin cambios, sin C1 |

Los mutantes C1 a C3 de `revisores/r02_02_mutantes_cierre.py` pasan a `mutantes.py` (M66 a M68).

## Comandos para probarlo

```bash
cd bloque_a/11_Ejecutor
../../.venv/bin/python -m pytest -q tests/test_t197_periodicidad.py tests/test_t87_contratos.py tests/test_integracion.py::test_peticion_ad_hoc_y_decisiones
../../.venv/bin/python ../../.docs/tickets/T-197/mutantes.py .            # mejor en una copia: modifica el árbol
../../.venv/bin/python -m pytest -q -p no:cacheprovider ../../.docs/tickets/T-197/revisores/r01_01_ataques.py
cd ../.. && .venv/bin/python .docs/scripts/evidencias_plan_a.py --pb PB-09
```
