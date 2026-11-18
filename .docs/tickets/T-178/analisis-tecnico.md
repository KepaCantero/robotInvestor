# T-178 · Análisis técnico

## Causa raíz o motivo

PB-19 (Plan de pruebas V3.0) pide, con el Analizador (instancia única) con seis CT-05 en cola: ninguna instancia nueva, reordenación por prioridad, aviso al Coordinador sobre plazos (vía HA) y propuesta de tipo 3 si se repite. HT-08 (`Monitor.evaluar_instancias`) ya no abría instancias de los agentes con estado y dejaba un CAR-, pero el CAR- solo lo anotaba («se reordena por prioridad» era una nota): la cola del monitor era un contador sin órdenes, no había aviso y nadie miraba si la saturación se repetía (INC-T116-03). La regla está en el prompt del Orquestador V5.0, 5.3 punto 5.

## Evidencia

- Antes: `bloque_a/herramientas/ht08_monitor.py`, rama `else` de `evaluar_instancias`, un dict con `nota` y nada más; `orquestacion.py` escribía las entradas en HA tal cual.
- Ahora: `.docs/scripts/evidencias_plan_a.py --pb PB-19` → «PB-19 Agente de instancia única saturado: Superada» (17 pruebas propias + 3 de antes).

## Implementación

- **Archivos cambiados y por qué:**
  - `bloque_a/11_Ejecutor/bloque_a/herramientas/ht08_monitor.py`: `CAMINO_ENTREGA`, `PRIORIDADES`, `TIPOS_C6`, `clave_prioridad`; `Monitor.pendientes` (órdenes conocidas de cada cola); `encolar(…, ordenes=)` con validación previa (falla cerrado sin tocar la cola); `retirar`; `_saturacion` (reordena la cola en el monitor y arma el CAR- con `saturado`, `umbral_cola`, `encargos_completados`, `reordenada`, `orden_cambiado`, `cola_reordenada`, `sin_detalle`, `afecta_plazos` y, si afecta, `aviso_coordinador`). La rama de los agentes sin estado (ORD-) no cambia.
  - `bloque_a/11_Ejecutor/bloque_a/carga.py` (nuevo): `registrar_carga` (escribe ORD-/CAR- en HA bajo AG-18, igual que antes, y decide la P3- por repetición, que escribe antes que el CAR- que la cita), `avisos_plazos` (lectura del Coordinador).
  - `bloque_a/11_Ejecutor/bloque_a/orquestacion.py`: un import y una línea (el bucle de escritura en HA pasa a `registrar_carga`). Nada más, por T-176 y T-177.
  - `bloque_a/11_Ejecutor/tests/test_t178.py` (17 pruebas), `tests/mapa_plan_pruebas.json` (PB-19 AUTOMATICA), `docs/evidencias_pruebas_bloque_a.md` (regenerado), `docs/incidencias.md` (INC-T178-01), `bloque_a/11_Ejecutor/README.md` (tabla de archivos), deuda técnica (fila T-178).
- **Decisiones y desviaciones del plan:** ninguna desviación. Las decisiones `[PROPUESTO]` están en INC-T178-01: «si se repite» = otro CAR- de saturación del mismo agente en otro run desde la última entrada de su última P3-; «afecta a plazos» = AG-01, AG-02, AG-18; la clave de orden; el Coordinador lee de HA solo sus avisos. Las decisiones del operador sobre una P3- (entradas nuevas con el mismo id, append-only, que no repiten `clave`) se reconocen por el id de la propuesta (vista consolidada de `almacen.estado`). Ningún número nuevo: el umbral es `paralelismo.umbral_cola`. Ningún esquema cambia.
- **Límites conocidos:** el ciclo no encola sus CT-05 en el monitor (el ejecutor atiende los ciclos en serie; no hay cola real de CT-05), así que en producción la reordenación solo actúa sobre las órdenes que alguien registre con `ordenes=`; lo que se encola como número (las llamadas de `Agentes`) se cuenta en `sin_detalle`. El CAR- no lleva W_medio, W_p90 ni ρ (dependen del reloj o no se miden; PB-18, INC-T159-01). El Coordinador no renegocia plazos con el Broker: el prompt solo pide informarle.
- **Comandos exactos para probarlo:**
  - `cd bloque_a/11_Ejecutor && ../../.venv/bin/python -m pytest -q tests/test_t178.py tests/test_fase4_huecos.py -k pb19`
  - `../../.venv/bin/python ../../.docs/tickets/T-178/mutantes.py .` (27 mutantes)
  - Desde la raíz: `.venv/bin/python .docs/scripts/evidencias_plan_a.py --pb PB-19`

## Ronda r02 (QA r01 NO APTO)

| Hallazgo | Corrección | Prueba de regresión |
| --- | --- | --- |
| H-01 (media) | `registrar_carga`: cada entrada en `with almacen._transaccion():` (reentrante, `flock` entre procesos): `nuevo_id`, lectura de HA, P3- y CAR- en una sección crítica | `test_r02_h01_dos_runs_concurrentes_no_duplican_la_p3` (M28) |
| H-02 (media) | `ABIERTAS` → `CERRADAS = ("RECHAZADA", "APLICADA")`; abierta = `not in CERRADAS` (un estado desconocido o ausente no cierra) | `test_r02_h02_un_estado_fuera_del_enum_no_cierra_la_propuesta` (4 estados), `test_r02_h02_aplicada_cierra_…` (M25 ajustado, M29, M30) |
| H-03 (baja) | `_fecha_objetivo`: AAAA-MM-DD y fecha real (`fromisoformat`), o `datetime.date`/`Timestamp` → ISO; lo demás, `ValueError` antes de mutar | 6 casos nuevos en `test_pb19_una_orden_invalida_…`, `test_r02_h03_una_fecha_date_…` (M31–M33) |
| H-04 (baja) | `TIPOS` = AD_HOC, PROFUNDIZACION, PERIODICO (CT-01) + SEGUIMIENTO (C6); fuera de la lista, `ValueError` | 2 casos nuevos en el `parametrize`, `test_r02_h04_los_tipos_…` (M34) |
| H-05 (baja) | **Desviación de la corrección sugerida.** En vez de una entrada de corrección de la P3-, la evidencia de la P3- cita solo los CAR- ya escritos (los de las saturaciones anteriores) más `run_actual` y la cola actual; el CAR- actual la cita a ella y se escribe después. Así ningún fallo deja una referencia colgante y no hace falta corregir nada. Motivo: con la entrada de corrección, A5 de `revisores/r01_ataques.py` desempaqueta una sola P3- en HA (`[p3] = …`) y falla; con esta, A5 y A5b dan OK | `test_r02_h05_si_el_car_falla_…` (M35) |
| H-06 (baja) | `Monitor.fin`: `max(cola - 1, len(pendientes))`; una orden con detalle solo sale con `retirar` | `test_r02_h06_fin_no_baja_…` (M36) |
| H-07 (baja) | INC-T178-01: punto «Qué cola se reordena», `[PROPUESTO]` | documental |

**A3 de `revisores/r01_ataques.py`.** La corrección de H-03 (rechazar lo que no es AAAA-MM-DD) hace que el primer `encolar` de A3 lance `ValueError` fuera de su `try`, y el script lo cuenta como «a3 (excepción)» sin llegar a A3b. El ataque esperaba que se ordenara por fecha (`["C", "B", "D", "A"]`), lo que exigiría interpretar «2026-6-5» y «05/06/2026» (ambiguo: DD/MM o MM/DD): eso contradiría la propia corrección de qa.md y la regla de fallar cerrado. Se mantiene el rechazo; las pruebas del `parametrize` comprueban que cada entrada de A3 y A3b (incluido NaN) se rechaza sin tocar la cola. Resultado del script sin cambiarlo: 11 de 12 entradas OK (A3 cuenta como excepción y A3b no se ejecuta).

Comandos: `PYTHONPATH=. ../../.venv/bin/python ../../.docs/tickets/T-178/revisores/r01_ataques.py` y `…/T-178/mutantes.py .`, desde `bloque_a/11_Ejecutor`.
