# T-178 · QA independiente

- **Revisor:** claude (subagente revisor nuevo, sin el contexto de la implementación) · **Ronda:** r01 · 2026-11-17
- **Código revisado:** `wip/t178`, commit `06bb04b`, en un worktree aparte. El repo principal no se ha tocado.

## Reproducción desde limpio

Por indicación del operador, no se han pasado ni la suite completa ni `./tools/check_all.sh`. Las cifras de suite, ruff 2813 y mypy 102 son las de `pruebas.md`. Desde `bloque_a/11_Ejecutor`, con `PYTHONPATH=.` para que se use el código del worktree:

- `pytest -q tests/test_t178.py tests/test_fase4_huecos.py tests/test_t53_evaluacion_y_almacen.py tests/test_unitarias.py`: **117 passed**. Son los ficheros que tocan el monitor, PB-19 o los CAR-.
- `.docs/tickets/T-178/mutantes.py .`: **27 de 27 muertos**, ninguno vivo.
- Backtest del README (`--cliente mock … backtest --desde 2024-01-05 --hasta 2024-03-29`): rc 0, con `senales.csv`, `pronosticos.csv` y `metricas.json`. En su HA hay 0 ORD-, 0 CAR- y 0 P3-, así que el caso normal no cambia.
- Ciclos mock del README sobre el mismo estado: `--as-of 2026-06-05 ciclo`, `peticion --json ejemplos/peticiones/peticion_ad_hoc.json`, `evaluar` y `estado`. Los cuatro dan rc 0.
- Ataques del revisor: `revisores/r01_ataques.py`. Se lanza desde `bloque_a/11_Ejecutor` con `PYTHONPATH=. python ../../.docs/tickets/T-178/revisores/r01_ataques.py`. Resultado: **4 de 13 OK**; los fallos se detallan abajo.

## Contraste con las fuentes (por ID y sección)

- **Plan V3.0, PB-19.** Resultado esperado: «ninguna instancia nueva de AG-02; reordenación por prioridad; aviso al Coordinador sobre plazos (vía HA); propuesta de tipo 3 si se repite». Criterio: «cero ORD- para AG-02; registro CAR-». Las cuatro piezas están implementadas y cubiertas por pruebas.
- **Prompt del Orquestador V5.0, 5.3 punto 5.** Dice literalmente «reordenas prioridades **de tu propia cola**». La implementación reordena la cola del agente saturado, y INC-T178-01 lo parafrasea como «reordenar su cola». La lectura adoptada es razonable, porque PB-19 habla de reordenar las órdenes CT-05 del Analizador. Pero es una ambigüedad del spec y no está documentada (H-07).
  - El mismo punto 5 cuenta AG-10 y AG-11 como «no declarados escalables», lo que contradice el 4.5 del Documento 0 y el propio prompt en su 6.x. Manda el Documento 0, el código lo sigue y queda fuera del alcance de T-178; es solo una observación.
- **Documento 0 V5.3.**
  - 4.5: AG-01, AG-02, AG-18, AG-19 y AG-20 son instancia única con cola. Se cumple: ninguno recibe ORD-, ni con el umbral a 0.
  - R25 y Anexo A (cola > 3): el umbral se lee de `paralelismo.umbral_cola` y no hay ningún número nuevo.
  - R5 y 6 (C6 por detrás de C1–C3): se cumplen.
  - R6: la P3- y el CAR- los escribe solo AG-18 en HA.
  - 18.1 (tipo 3 con evidencia, impacto, pruebas de regresión y aprobación del operador): la P3- lleva `evidencia`, `impacto`, `pruebas_regresion`, `plan_reversion` y el estado PENDING_OPERATOR.
  - Esquema de HA V2.0, 4.8 y 5: la transición PENDING_OPERATOR → APROBADA → APLICADA / RECHAZADA es coherente con `ABIERTAS`. Que la P3- use `id` en lugar de `p3_id` es el mismo convenio que ya sigue `guias.py`.
- **R8.** Ni el aviso ni el CAR- copian campos ajenos de la orden: solo `ref`, `prioridad`, `tipo` y `fecha_objetivo`. Lo comprueba el ataque A7 con una clave ficticia y el cuerpo del mensaje dentro de la orden. No hay datos personales ni credenciales.

## Criterios de aceptación

| Criterio | Cumple | Evidencia |
| --- | --- | --- |
| CA-1 | sí | `test_pb19_seis_ct05_…` y la de integración con dos ciclos del Bloque; las pruebas de antes de HT-08 siguen en verde (117 passed) |
| CA-2 | sí | `test_pb19_seis_ct05_…`, `…_estable_…` y `…_sin_detalle_…`. Las claves `fecha_objetivo` y `tipo` no se validan (H-03, H-04) |
| CA-3 | sí | `…_aviso_al_coordinador_…` y `…_el_coordinador_lee_su_aviso_en_ha` |
| CA-4 | sí, en secuencia; **no**, frente a concurrencia o un estado fuera del enum | Las pruebas secuenciales pasan. Con dos runs concurrentes se crean dos P3- (H-01, A1). Un `estado` fuera del enum vuelve a armar la propuesta y la duplica (H-02, A2). La P3- APROBADA sin aplicar se trata bien: el CAR- la cita y no se duplica (prueba del implementador; M25 muere) |
| CA-5 | sí, para la prioridad, la `ref` y el umbral 0 | `…_una_orden_invalida_…` (4 casos) y `…_umbral_cero`. La validación antes de mutar no es completa (H-03, H-04) |
| CA-6 | sí (suite y cuotas según `pruebas.md`, por indicación del operador; mock y backtest reproducidos aquí) | 117 passed en los ficheros afectados, 27 de 27 mutantes muertos y los ciclos mock con rc 0 |

## Decisiones `[PROPUESTO]` (INC-T178-01)

- **«Si se repite» = otro run con saturación, desde la última P3- decidida.** Es razonable: no inventa ningún número, el mismo run no cuenta y se vuelve a armar tras RECHAZADA o APLICADA.
- **«Afecta a plazos» = AG-01, AG-02 y AG-18.** Es razonable. AG-19 es asíncrono (R17) y AG-20 trabaja en C4 y C5, en segundo plano (6).
- **Clave de orden.** Es razonable y sale de R5, de 6 y de CT-01.
- **El Coordinador lee HA.** Es aceptable, porque lo dice el prompt. Queda bien anotado como pendiente para una entrega futura de la matriz de 5.
- **Límite «el ciclo no encola CT-05 en el monitor».**
  - Es aceptable para PB-19. Su «Preparación» es inyectar seis CT-05 en la cola del Analizador, y la prueba de integración lo hace sobre un `Bloque` real con dos `ciclo()`.
  - En un run real, el ejecutor atiende las llamadas en serie (`agentes.llamar` hace `encolar` y después `fin`), así que AG-02 nunca supera el umbral. El backtest lo confirma: 0 CAR-. No es una regresión, y el límite está declarado en el README del ticket y en INC-T178-01.
  - Lo que sí falla es la coherencia del contador cuando las dos vías se mezclan (H-06).

## Hallazgos

| ID | Gravedad | Cómo reproducirlo | Esperado / obtenido | Corrección sugerida | Estado |
| --- | --- | --- | --- | --- | --- |
| H-01 | media | `r01_ataques.py` A1. Hay un CAR- de RUN-0 y dos `Almacen` sobre la misma carpeta (dos procesos) llaman a `registrar_carga` con RUN-1 y RUN-2; una barrera hace que los dos lean HA antes de escribir. | Esperado: una sola P3- abierta. Obtenido: `P3-ORQ-2026-0001` y `P3-ORQ-2026-0002`. `_propuesta` lee HA, decide y escribe fuera de una transacción del almacén. | En `carga.registrar_carga`, envolver el cuerpo del bucle en `with almacen._transaccion():`. Es reentrante y bloquea entre procesos con `flock`, de modo que el `nuevo_id`, la lectura de HA, la P3- y el CAR- quedan en una sola sección crítica. Añadir una prueba de regresión con dos `Almacen` y una barrera (A1). El revisor lo ha verificado en local: A1 OK y `test_t178.py` 17 de 17. | abierto |
| H-02 | media | A2. La P3- recibe una decisión con `estado` `"Rechazada"`, `None` o `"EN_ESTUDIO"`, que están fuera del enum del esquema 4.8. Se satura en dos runs más. | Esperado: un estado desconocido no cierra la propuesta, para no duplicar la cola de tipo 3. Obtenido: se trata como cerrada, se vuelve a armar y aparece una segunda P3-. Es un fallo abierto, no cerrado. | En `carga.py`, sustituir `ABIERTAS = ("PENDING_OPERATOR", "APROBADA")` por `CERRADAS = ("RECHAZADA", "APLICADA")`, y la condición por `if estados.get(pid, {}).get("estado") not in CERRADAS: return pid`. Añadir una prueba con los tres estados de A2. Verificado en local: A2 OK y 17 de 17. Hay que ajustar el mutante M25 a la nueva constante. | abierto |
| H-03 | baja | A3. `encolar` con `fecha_objetivo` en `"2026-6-5"`, `"05/06/2026"`, `datetime.date` o `float("nan")`. | Esperado: rechazo al encolar, porque la fecha forma parte de la clave de orden. Obtenido: se acepta y el orden sale lexicográfico, no por fecha (`['D','C','A','B']`, cuando lo correcto es `['C','B','D','A']`); NaN también se acepta. | En `Monitor.encolar`, dentro del bucle de validación: `f = o.get("fecha_objetivo")`; `if f is not None:` `if isinstance(f, dt.date): f = f.isoformat()` y, `elif not (isinstance(f, str) and re.fullmatch(r"\d{4}-\d{2}-\d{2}", f)): raise ValueError(f"HT-08: fecha_objetivo {f!r} de {ref} no es AAAA-MM-DD")`, seguido de `dt.date.fromisoformat(f)` (que rechaza el 2026-02-30). Guardar `f`. Añadir los casos de A3 al `parametrize` de `test_pb19_una_orden_invalida_…`. | abierto |
| H-04 | baja | A4. `encolar` con `tipo: "seguimiento"` (en minúsculas) y prioridad ALTA, junto a una BAJA sin tipo. | Esperado: rechazo, o la C6 al final. Obtenido: la C6 pasa delante (`['S','N']`), en contra de R5 y 6. | En `ht08_monitor.py`, añadir `TIPOS: frozenset = frozenset({"AD_HOC", "PROFUNDIZACION", "PERIODICO", "SEGUIMIENTO"})`, que son los de CT-01 en `contratos.py` más el CT-05 de C6 de `seguimiento.py`. En `encolar`: `if o.get("tipo") is not None and o["tipo"] not in TIPOS: raise ValueError(...)`. Añadir el caso al `parametrize`. | abierto |
| H-05 | baja | A5. La escritura del CAR- falla (`OSError`) después de escribir la P3-. | Esperado: HA coherente. Obtenido: la `evidencia.car` de la P3- cita `CAR-2026-0002`, que no existe. El run siguiente reutiliza bien la P3- (A5b OK). | En `registrar_carga`, si la escritura del CAR- lanza una excepción después de crear la P3- en esa misma vuelta, escribir una entrada de corrección con el mismo id, como permite el modelo append-only: `{"tipo_entrada": "P3", "id": p3_id, "evidencia": {**evidencia, "car": [ids sin car_id]}, "nota": "CAR- disparador no escrito (fallo de escritura)"}`. Hacerlo dentro de un `try` que no oculte la excepción original, y relanzarla después. Añadir una prueba con `escribir` parcheado, como A5. | abierto |
| H-06 | baja | A9. `encolar("AG-02", ordenes=6)` seguido de tres `fin("AG-02", …)`, que es la ruta de `agentes.llamar`. | Esperado: el contador y el detalle coherentes. Obtenido: `cola` 3, `cola_reordenada` con 6 órdenes y `en_espera_sobre_umbral` 3. El CAR- se contradice. | En `Monitor.fin`, sustituir `self.cola[agente] = max(self.cola[agente] - 1, 0)` por `self.cola[agente] = max(self.cola[agente] - 1, len(self.pendientes[agente]))`: una orden con detalle solo sale de la cola con `retirar`. Añadir una prueba como A9. | abierto |
| H-07 | baja | Comparar 5.3 punto 5 del prompt del Orquestador («reordenas prioridades de tu propia cola») con INC-T178-01 («reordenar su cola»). | Esperado: la ambigüedad del spec documentada (regla 7 del proyecto). Obtenido: se parafrasea y la ambigüedad no se registra. | Añadir a INC-T178-01 un punto: «**Qué cola se reordena.** El prompt dice "reordenas prioridades de tu propia cola"; PB-19 pide "reordenación por prioridad" con seis CT-05 del Analizador. `[PROPUESTO]`: se reordena la cola del agente saturado, que es la que lleva HT-08, la herramienta del Orquestador; la cola de tareas propia de AG-18 no se modela en el ejecutor.» | abierto |

Los scripts de ataque están en `revisores/r01_ataques.py`. En la ronda siguiente se vuelven a ejecutar sin cambiarlos y deben dar 13 de 13 OK.

## Veredicto

**NO APTO.**

No hay hallazgos críticos ni altos. Hay dos medios que rompen invariantes del sistema:

- **H-01** rompe la unicidad de la P3- con dos runs concurrentes.
- **H-02** hace que un estado desconocido abra en vez de cerrar.

Hay además cinco bajos. La regla del operador es que se subsanan en este mismo ticket y no pasan a la deuda.

**Siguiente paso:** quien implementó corrige H-01 a H-07 con su prueba de regresión cada uno (`ri-implementar` → `ri-probar`) y ajusta el mutante M25. La QA r02 vuelve a ejecutar `revisores/r01_ataques.py` y los mutantes.

## Ronda r02

- **Revisor:** claude (el mismo revisor nuevo de la r01, sin el contexto de la implementación) · 2026-11-17
- **Código revisado:** `wip/t178`, commit `fe47d90` (sobre `06bb04b`), en un worktree nuevo. Los ficheros `revisores/r01_ataques.py` y `qa.md` de la r01 son idénticos a los del commit del revisor (`df595f2`).

### Reproducción

Desde `bloque_a/11_Ejecutor`, con `PYTHONPATH=.`. Por indicación del operador, no se pasan ni la suite completa ni el gate.

- **Pruebas afectadas.** `tests/test_t178.py` da 35 de 35. Con `test_fase4_huecos`, `test_t53_evaluacion_y_almacen` y `test_unitarias`, 135 passed. `tests/test_fase4_mapa.py` da 23 de 23: el mapa y las evidencias siguen coherentes.
- **Mutantes.** `mutantes.py .` da **36 de 36 muertos**, ninguno vivo.
- **Cuotas, con los comandos del gate desde la raíz.**
  - ruff sobre los tres ejecutores: 2813 (la cuota es 2813).
  - `mypy --ignore-missing-imports bloque_a/11_Ejecutor/bloque_a`: 102 (la cuota es 102), sin ningún error en `carga.py` ni en `ht08_monitor.py`.
- **Ciclos mock y backtest.** El backtest del README da rc 0, con `senales.csv`, `pronosticos.csv` y `metricas.json`. Los ciclos mock `--as-of 2026-06-05 ciclo`, `peticion`, `evaluar` y `estado` dan rc 0.
- **`revisores/r01_ataques.py`, sin cambios: 11 de 12 OK.** El único fallo es A3. La función lanza `ValueError` sobre «2026-6-5», que es justo el rechazo que pedía H-03 («se rechaza **o** se ordena por fecha»). Lo que falla es que mi script no capturaba ese rechazo, no el código. **El rechazo basta.** El ataque se rehace como B1 en un script nuevo, sin sobrescribir el de la r01.
- **`revisores/r02_ataques.py` (nuevo): 14 de 14 OK.**
  - B1. Siete fechas malas se rechazan sin tocar la cola: «2026-6-5», «05/06/2026», «2026-02-30», NaN, un entero, «2026-06-05T10:00» y la cadena vacía. Un `date` y un `datetime` se guardan en ISO y ordenan por fecha.
  - B2. Concurrencia de H-01 **entre procesos reales** (`multiprocessing` con fork, un `Almacen` por proceso y una barrera tras leer HA), repetida 3 veces. Sale una sola P3-, los dos CAR- la citan y la integridad de HA da True. **Contraprueba:** con el `carga.py` de `06bb04b`, B2 crea dos P3- en las 3 repeticiones, así que el ataque discrimina.
  - B3. Evidencia de H-05.
  - B4. APLICADA cierra la propuesta y hace falta otra repetición para abrir una nueva.
  - B5. Lista cerrada de `tipo`.

### Desviación en H-05

La corrección del implementador es distinta de la que propuse, y la acepto.

- **Cómo queda.** La P3- cita solo los CAR- que ya están en HA (`evidencia.car` y `runs`). Cuenta la saturación actual con `run_actual`, `cola`, `umbral_cola` y `afecta_plazos`. El CAR- actual se escribe después y cita la P3- con `p3_id`.
- **Ventajas frente a mi propuesta.**
  - Ninguna secuencia de fallos deja una referencia colgante: A5 da 0 colgantes.
  - No hace falta una escritura compensatoria, que habría podido fallar a su vez.
  - Todo va dentro de la misma transacción.
- **Sigue sirviendo al operador.** B3 muestra que la evidencia nombra los dos runs (`runs` + `run_actual`), la cola y el umbral, y que todo lo que cita existe en HA. El CAR- disparador se encuentra por su `p3_id`, que es el mismo enlace que usan los CAR- posteriores mientras la propuesta está abierta.
- **Tras un fallo del CAR-,** la P3- queda abierta y el run siguiente la cita sin duplicarla (A5b).
- **Observación, no un hallazgo.** El id del CAR- disparador no aparece en la propia P3-; se llega a él por `p3_id`. Esto está documentado en INC-T178-01 y en el docstring de `carga.py`.

### Concurrencia de H-01

- El bucle de `registrar_carga` va dentro de `almacen._transaccion()`. Esa transacción combina un `RLock` reentrante por instancia y un `flock` exclusivo sobre `.almacen.lock`, que excluye a los otros procesos.
- `leer`, `estado`, `nuevo_id` y `escribir` vuelven a entrar en la transacción sin bloquearse.
- B2 lo confirma entre procesos, y la prueba `test_r02_h01_…` lo confirma con dos `Almacen` en hilos.
- El cerrojo se toma una vez por entrada, solo en el punto ya existente del ciclo, tras la fase en paralelo. No compite con los analistas.
- **Observación.** `carga.py` usa `_transaccion`, un método privado del almacén. Ya lo comparten otros módulos del paquete y no es un hallazgo.

### Estado de los hallazgos de la r01

| ID | Gravedad | Corrección comprobada | Estado |
| --- | --- | --- | --- |
| H-01 | media | Transacción del almacén en `registrar_carga`. Prueba `test_r02_h01_…`; A1 y B2 OK, con contraprueba | corregido |
| H-02 | media | `CERRADAS = ("RECHAZADA", "APLICADA")` y `not in CERRADAS`. Prueba parametrizada `test_r02_h02_…` y `…_aplicada_cierra_…`; A2 (3 casos) y B4 OK | corregido |
| H-03 | baja | `_fecha_objetivo`: AAAA-MM-DD con fecha real, o `date`/`datetime` pasado a ISO; si no, `ValueError` antes de mutar. Prueba en el parametrize y `test_r02_h03_…`; B1 OK (8 casos) | corregido |
| H-04 | baja | `TIPOS` en lista cerrada. Prueba en el parametrize y `test_r02_h04_…`; A4 y B5 OK | corregido |
| H-05 | baja | Con otra corrección, que se acepta (ver arriba). Prueba `test_r02_h05_…`; A5, A5b y B3 OK | corregido |
| H-06 | baja | `fin` no baja la cola por debajo del detalle. Prueba `test_r02_h06_…`; A9 OK (cola 6, detalle 6) | corregido |
| H-07 | baja | INC-T178-01 lleva el punto «Qué cola se reordena», con la cita literal y la lectura adoptada como `[PROPUESTO]` | corregido |

No hay hallazgos nuevos.

### Criterios de aceptación (r02)

- **CA-1, CA-2, CA-3 y CA-5:** se cumplen. Las validaciones de CA-2 y CA-5 quedan completas con H-03 y H-04.
- **CA-4:** ahora se cumple también con concurrencia (H-01) y con estados fuera del enum (H-02). La P3- APROBADA sin aplicar sigue tratándose bien.
- **CA-6:** se cumple. Las cuotas no suben, los ciclos mock están en verde y las evidencias de PB-19 están regeneradas («Superada»). La suite completa se toma de `pruebas.md`, por indicación del operador.

### Veredicto r02

**APTO.** Los siete hallazgos de la r01 están corregidos, cada uno con su prueba de regresión. No queda ningún hallazgo abierto de ninguna gravedad, y no hay bajos pendientes para la ronda de cierre.
