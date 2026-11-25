# T-196 · QA independiente

- **Revisor:** claude (subagente revisor nuevo, sin el contexto de la implementación) · **Ronda:** r01 · 2026-11-24
- **Código revisado:** `wip/t196`, commit `05a8bad` sobre `6045913`, en un worktree aparte (`qa_t196`). Ni la copia del implementador ni el repo principal se han tocado.

## Reproducción desde limpio

Por indicación del coordinador (máquina compartida), no se ha lanzado `./tools/check_all.sh` completo. Todo se ha ejecutado desde `bloque_a/11_Ejecutor`.

- **Gate del implementador** (`gate196.txt`): 12/12, con RC=0 (corpus, NFC, YAML, secretos, refs, ruff 2807/2807, mypy A 102/102, FX 174/174, B 159/159, pytest A 8400, FX 68, B 176). El log terminó a las 11:34:21 y el commit es de las 11:34:44; el árbol está limpio.
- `pytest -q tests/test_t196.py`: **41 passed**. Sobre `6045913`, con solo el fichero de pruebas copiado, la colección falla (no existe `bloque_a.cola_peticiones`): las pruebas nuevas **fallan sin el cambio**.
- Mutantes del implementador (`mutantes.py`), en un worktree propio: **33 de 33 muertos**.
- Mutantes del revisor (`revisores/r01_mutantes.py`): **5 de 14 muertos, 9 vivos** (H-07 a H-09).
- Ataques del revisor (`revisores/r01_ataques.py`): **2 de 10 OK**, 8 hallazgos (H-01 a H-06).
- Equivalencia (`revisores/r01_equivalencia.py`): un CT-01 servido por la cola a las 23:30 Europe/Madrid da el mismo RUN-, F3 y F4 que `Bloque.peticion` con la fecha. Solo cambian las rutas temporales de los entregables y el `disparador`.
- Backtest del README (`--cliente mock … backtest --desde 2024-01-05 --hasta 2024-03-29`), en extracciones de `wip/t196` y de `6045913`: los dos con rc 0. `senales.csv`, `pronosticos.csv` y `metricas.json` son idénticos byte a byte (md5).
- Ruff sobre `bloque_a/11_Ejecutor`: 385 hallazgos antes y 385 después; `cola_peticiones.py` y `test_t196.py` salen limpios. Mypy de `bloque_a`: 102 antes y 102 después. Las cuotas no suben.
- **Trabajo de Astra (PR 3, `origin/astra/encargos-bloque-a-c38-c47`).** `git merge --no-commit` sobre `wip/t196` no da ningún conflicto de código: `orquestacion.py`, `cli.py` y `ht08_monitor.py` se fusionan solos (en el Bloque A no hay ningún `bloque.py`). Los conflictos son solo de texto añadido en `docs/evidencias_pruebas_bloque_a.md`, `docs/incidencias.md`, la deuda y `cola_astra.md`. En el árbol fusionado, `test_t196.py` más las pruebas de T-162 y T-169 dan **104 passed**.

## Contraste con las fuentes

- **Plan V3.0, PB-08.** El criterio pide «100 % registradas; 100 % respondidas o con plazo comunicado; N0 con p90 < 2 minutos». Con la ráfaga del plan inyectada en orden se cumple, y el p90 en tiempo real queda motivado (API, modo sombra). Pero «ninguna RECHAZADA» y «100 % respondidas» se rompen en cuanto los instantes no llegan en orden creciente o el servicio coincide con nuevas recepciones (H-01, H-02), que es justo la situación de una ráfaga real. Una PET- de un proceso muerto deja su consulta sin final para siempre, y nadie se entera (H-03).
- **Regla 2 de CLAUDE.md (los números).** Las bases, el envejecimiento y la urgencia no están en el Anexo A, sino en el §6.1 del prompt del Coordinador V5.0, un documento del corpus que fija precisamente estos números para AG-01. Se llevan a `config/por_defecto.yaml` marcados `[PROPUESTO]` y se declaran en INC-T196-01, que es el procedimiento del proyecto para lo que el Anexo A no cubre. Las pruebas leen los valores de la configuración, no los escriben. **Es legítimo**, y no es un hallazgo. P-17 (`presupuesto_uc`) y P-21 (`objetivo_respuesta_n0_s: 120`) sí son del Anexo A. `PERCENTIL_N0 = 0.9` es la definición del criterio, no un parámetro.
- **PET- frente al Documento 0 y el esquema de F5.**
  - Ningún prefijo del Documento 0 ni del esquema de F5 del Bloque A es `PET-`. El Bloque B usa `PET-B-AAAA-NNNN` (en otro almacén, con otro formato) y `cadena_b.py` lee `pet_id` solo de la respuesta del B, no de un RUN- del A, así que no chocan. Ojo: el nombre de campo `pet_id` significa cosas distintas en los dos lados; anotarlo en INC-T196-01 bastaría.
  - **Sí hay una desviación del esquema.** El esquema de F5 (§5) prevé registrar las encoladas como RUN- `ENCOLADO → EN_CURSO → …`. La decisión de usar una entrada propia `PETICION` está motivada, porque un RUN- ENCOLADO confundiría a los lectores de «el último RUN-» (`orquestacion.py` 552, 1815, 2085, 2201, 2394; `diseno_v6.py` 478; `interfaz_broker.py` 280 y 364). Es coherente con `RUN_C6`, `AVISO_CT22` y `PRESUPUESTO_F9`, y está declarada `[PROPUESTO]`.
  - Los estados `ENCOLADA`/`ATENDIDA`/`FALLIDA` (en femenino) no chocan con los de RUN- ni con los de QRY-. Los lectores de F5 que no filtran por `tipo_entrada` solo extraen identificadores (`conocidos` de la consulta N0). Una referencia PET- citada por el modelo pasaría ese filtro; es inocuo, porque el esquema de F5 la listaría fuera de las admitidas, pero conviene saberlo.
  - Aceptable.
- **R5 («nunca se descarta en silencio»).** Ver H-02 y H-03.
- **R8.** FALLIDA guarda solo la clase del error, y la incidencia no lleva su texto (prueba del implementador y M16).
- **Valores por defecto.** Sin las opciones nuevas, `peticion` y `consulta` no cambian: `consulta_en_cola` es False sin `peticion_cola`, `_reparto` es la misma fórmula (M33) y el backtest sale idéntico. En la CLI, `consulta` solo pasa `instante` con `--encolar-escalado`. **No cambian nada.**
- **Reloj inyectado.** Las zonas horarias se convierten bien (A10: 10 h en UTC dan el mismo envejecimiento que en Madrid). Las horas completas, el tope y el instante anterior a la propia recepción se tratan bien. Fallan dos cosas: un instante anterior a la recepción de **otra** petición se trata como un error global (H-01, H-02), y el cambio de hora y los nanosegundos dan un error de otra clase o tardío (H-04, H-05).
- **Ninguna prueba antigua debilitada.** El diff solo toca `test_t196.py` (nuevo) y `mapa_plan_pruebas.json` (añade pruebas a PB-08). Las evidencias están regeneradas, y PB-08 sigue «en parte» por el p90 en tiempo real, lo cual es honesto. Su «comprueba» dice «ninguna rechazada», y eso solo vale con los instantes en orden (H-02).

## Criterios de aceptación

| Criterio | Cumple | Evidencia |
| --- | --- | --- |
| CA-1 | sí, con instantes en orden | Prueba de la ráfaga del plan (65 registradas) |
| CA-2 | **no** en general | 200 en cola y msg_id repetido: sí. Un CT-01 con un instante anterior a otra PET- en cola se rechaza, y su msg_id del Broker queda bloqueado (H-02, A1) |
| CA-3 | **no** en general | En la ráfaga, sí. Una consulta encolada a la vez que otra recepción pierde su análisis tras prometer un plazo (H-02, A3). Una PET- EN_CURSO huérfana deja la consulta sin final para siempre (H-03, A7) |
| CA-4 | sí | Pruebas de prioridad, alcance, urgencia y desempate; M1 a M9 muertos; A10 |
| CA-5 | sí (simulado; p90 real motivado) | Prueba de la ráfaga: 30 N0, cero RUN- y p90 menor que P-21 |
| CA-6 | sí | Prueba del presupuesto frente a `_reparto`, M13, M33 y r01_equivalencia |
| CA-7 | **no** frente a concurrencia de recepción y servicio | Tomas concurrentes: sí (M14). `atender` se corta si llega una petición mientras sirve (H-01, A2). Fallo del ciclo: sí, pero sin prueba de `BaseException` ni del `run_id` de la FALLIDA (H-08) |
| CA-8 | parcial | Lo inválido se rechaza sin escribir en F5. El instante del cambio de hora da `ValueError` y no `PeticionInvalida` (H-05). Los nanosegundos fallan después de reservar el msg_id (H-04) |
| CA-9 | sí | Gate 12/12, cuotas sin subir, backtest idéntico, valores por defecto sin cambios |

## Hallazgos

| ID | Gravedad | Cómo reproducirlo | Esperado / obtenido | Corrección exacta | Prueba de regresión | Estado |
| --- | --- | --- | --- | --- | --- | --- |
| H-01 | **alta** | `r01_ataques.py` A2: tres PET- en cola y `atender(t)`; durante el primer ciclo otro proceso registra un CT-01 con `recibida` igual a t + 5 min (con la CLI basta un `peticion --encolar` mientras `atender-cola` corre un análisis de minutos) | Esperado: se siguen sirviendo las demás. Obtenido: el segundo `_tomar` lanza `PeticionInvalida` («instante anterior a su recepción») y `atender` se corta tras 1 servida, con 3 ENCOLADAS. En operación real, la cola deja de servirse cada vez que entra algo durante el servicio | `orden(t)` y `_tomar(t)` consideran solo las PET- con `recibida <= t`: las posteriores aún no habían llegado en t, no son un error. Además, `atender` acepta un reloj (callable) y la CLI le pasa uno, para tomar cada petición con un instante nuevo y servir en la misma pasada las que lleguen. El rechazo de un instante anterior queda solo para la propia petición: `prioridad(pet, t)` llamada directamente | `test_atender_no_se_corta_si_llega_una_peticion_durante_el_servicio`: el ciclo falso registra un CT-01 posterior; se sirven todas las de antes y la nueva queda ENCOLADA o se sirve con el reloj | abierto |
| H-02 | **alta** | A1: `recibir` en t + 2 s y después otro CT-01, con msg_id del Broker, en t + 1 s (entrega fuera de orden, o dos procesos que leen `now()` y compiten por el cerrojo). A3: una `consulta(encolar_escalado=True, instante=t)` durante la que otro proceso registra un CT-01 en t + 30 s (con la API, la llamada al modelo dura segundos) | R5: ninguna se rechaza. Obtenido en A1: el CT-01 se rechaza con `PeticionInvalida` y el reintento del Broker con el mismo msg_id también (`MensajeInvalido`: «libere la reserva»). En A3: `PeticionInvalida` después de escribir la QRY- y la provisional, que prometía «En cola: posición k»; la PET- no existe, y la final que sale luego es `NO_EJECUTADO`. Es un análisis prometido y no hecho | `_plazo` cuenta la posición solo sobre las PET- con `recibida <= t`, y la de cada una con la espera acotada a 0 si es posterior. Nunca lanza por la recepción de otra. Todo lo que puede fallar en `recibir` (el instante, incluido su ida y vuelta por `isoformat`, y la configuración) se valida antes de `mensajeria.crear` y de `procesar_una_vez`, para que un fallo no bloquee el msg_id del Broker | `test_un_ct01_con_instante_anterior_a_otra_peticion_se_encola` (A1, con el reintento del msg_id) y `test_la_consulta_encolada_no_pierde_su_peticion_si_entra_otra_mientras_responde` (A3, monkeypatch de `registrar_provisional`): la PET- existe y la final sale al atender | abierto |
| H-03 | **media** | A7: una consulta encolada y `cola.tomar(t)`; el proceso muere en pleno ciclo. Otro `Bloque` sobre el mismo estado, tres días después: `enviar_pendientes` y `atender` | Esperado, con el precedente de T-177 (QA r03, H-16, reservas C4 huérfanas): se detecta y deja constancia, sin liberar (fallo cerrado). Obtenido: la PET- sigue EN_CURSO para siempre, la final de la consulta nunca sale (`consulta_en_cola` es True), y no hay incidencia ni aviso. Es un «descarte en silencio», en contra de R5. El límite declarado («no se recupera sola») es aceptable; el silencio no | `_tomar` guarda `pid` (y el host) en la entrada EN_CURSO. `atender` (y `enviar_pendientes`) detectan las EN_CURSO cuyo `pid` ya no vive (`interfaz_broker._pid_vivo`) y dejan **una** incidencia Operativa en HA por PET- (`peticion_huerfana`), sin tocar su estado. La salida de `atender` las lista. Una orden `bloque-a reconciliar-peticion PET-… --fallida` (por analogía con `reconciliar-mensaje`) la pasa a FALLIDA, con lo que sale la final FALLIDO de su consulta | `test_peticion_en_curso_de_un_proceso_muerto_deja_una_incidencia_y_se_reconcilia`: toma en un subproceso que se mata; la incidencia queda una sola vez en dos pasadas; tras reconciliar, FALLIDA y final FALLIDO | abierto |
| H-04 | baja | A5: `recibir({…, "msg_id": "MSG-BRK-2026-000888"}, pd.Timestamp("…09:00:00.123456789", tz=…))` | Esperado: se rechaza antes de reservar el msg_id. Obtenido: pasa `_fecha_hora`, se reserva el msg_id y `_plazo` falla al releer su propia `recibida` (9 decimales, fuera de `RE_FECHA_HORA`). El reintento válido queda bloqueado | En `_fecha_hora`, rechazar (o truncar a microsegundos de forma explícita) un `Timestamp` con `nanosecond != 0`, y comprobar que `t.isoformat()` cumple `RE_FECHA_HORA`. Queda cubierto con la validación previa de H-02 | `test_un_instante_con_nanosegundos_se_rechaza_sin_reservar_el_msg_id` | abierto |
| H-05 | baja | A4: `recibir(ct01, "2026-03-29T02:30")` (hora que no existe) y `"2026-10-25T02:30"` (hora repetida) | Esperado: `PeticionInvalida` (CA-8). Obtenido: `ValueError` de pandas; no se escribe nada, pero la clase no es la del contrato, y la CLI no lo distingue de un fallo interno | En `_fecha_hora`, envolver `tz_localize` en un `try` y convertir `NonExistentTimeError`/`AmbiguousTimeError` en `PeticionInvalida` («hora inexistente o ambigua en la zona del bloque; indique la zona») | Añadir los dos valores al `parametrize` de `test_un_instante_invalido_se_rechaza` | abierto |
| H-06 | baja | A6: `cola.tomar(t)` y después `atender(t + 1 min)` | `tomar` es pública y deja una PET- EN_CURSO que nada puede servir (`atender` solo toma ENCOLADAS): 0 servidas, sin aviso | Hacer `tomar` privada (la prueba de concurrencia usa `_tomar`) o añadir `servir(pet)` pública. En los dos casos, el docstring lo dice. Con H-03, una EN_CURSO tomada a mano y no servida se ve como huérfana | La prueba de concurrencia con `_tomar` y una aserción de que `ColaPeticiones` no expone `tomar` (o una prueba de `servir`) | abierto |
| H-07 | baja | A8: `recibir(ct01(clases=("XXX",)), t)`; mutante vivo R4 (sin filtrar por las clases activas) | Se encola con `clases: []` y **0 UC**; el acuse dice «N2, 0 UC», que no es un presupuesto proporcional, y el ciclo sale PARCIAL sin analizar nada. Además, ninguna prueba mata que no se filtre por las activas | En `_validar_ct01`/`_nueva`, rechazar con `PeticionInvalida`, antes de crear el mensaje, un alcance sin ninguna clase activa (contenido indebido, que el esquema de F5 admite como rechazo) | `test_un_ct01_sin_clases_activas_se_rechaza_sin_escribir` (mata R4) | abierto |
| H-08 | baja | `r01_mutantes.py`: vivos R6 (`except Exception`: un `KeyboardInterrupt` o un `SystemExit` dejan la PET- EN_CURSO), R12 (FALLIDA sin `run_id` cuando el ciclo ya había escrito su RUN-) y R13 (ATENDIDA sin `estado_run`) | Cláusulas del diseño («nada se absorbe», el FALLIDO con su RUN-, el registro del estado del RUN-) sin ninguna prueba que las mate | Sin cambio de código | En `test_un_ciclo_que_falla…`, parametrizar el error con `KeyboardInterrupt`; un ciclo falso que escribe un RUN- con `disparador.pet_id` antes de fallar (la FALLIDA y el escalado lo citan); aserción de `estado_run` en la ATENDIDA de `test_servicio_real…` | abierto |
| H-09 | baja | `r01_mutantes.py`: vivos R2 (un CT-01 `PERIODICO` no pasa a AD_HOC), R9 (la consulta encolada con el `as_of` del llamante en vez del día del instante) y R10 (la CLI `consulta --encolar-escalado` sin `--instante`) | Ramas sin prueba: el mapeo PERIODICO → AD_HOC (afecta al reparto N3), el día del análisis encolado y la CLI de la consulta encolada (no se prueba en absoluto) | Sin cambio de código | `test_un_ct01_periodico_se_encola_como_ad_hoc`; consulta con `as_of` de otro día e `instante`: la QRY- y la PET- son del día del instante; prueba de CLI de `consulta --encolar-escalado --instante …` con `peticion_cola` y la final tras `atender-cola` | abierto |

R11 (`fecha_objetivo` guardada sin normalizar a la zona) se considera **equivalente**: el orden y la urgencia la vuelven a leer con `_instante` y dan lo mismo; solo cambia el formato guardado.

## Veredicto

**NO APTO.** Hay dos hallazgos altos y uno medio:

- **H-01 y H-02:** la cola falla o rechaza peticiones en cuanto recepción y servicio se solapan o los instantes llegan fuera de orden, que es la situación de una ráfaga real. Eso rompe la cláusula central de R5 y de PB-08: ninguna rechazada y todas respondidas.
- **H-03:** una PET- huérfana deja la consulta sin final y sin aviso.

Los seis bajos (H-04 a H-09) se corrigen en la misma ronda, por regla del operador; ninguno va a la deuda. En la r02, el revisor volverá a pasar `revisores/r01_ataques.py` (que debe dar 10 de 10 OK, o la nueva semántica documentada en A9), `revisores/r01_mutantes.py` (14 de 14 muertos, salvo R11, equivalente) y el `mutantes.py` del implementador.

---

## Ronda r02 · 2026-11-24

- **Revisor:** el mismo de la r01 (claude, subagente revisor nuevo).
- **Código revisado:** `wip/t196`, commit `06a8cc79`, en el worktree `qa_t196`. La copia del implementador no se ha tocado.
- Los `revisores/r01_*.py` del commit son idénticos byte a byte a los del revisor, y el `qa.md` r01 también.

### Reproducción

- **Gate del implementador** (`gate_t196_r02.log`): 12/12, con RC=0.
  - Ruff 2807/2807.
  - Mypy: A 102, FX 174, B 159, todos en su cuota.
  - Pytest: A 8415 (antes 8400), FX 68, B 176.
- `pytest -q tests/test_t196.py`: **56 passed**.
- **Mutantes:**
  - del implementador (`mutantes.py`): **55 de 55 muertos**;
  - del revisor r01 (`revisores/r01_mutantes.py`): **13 de 14 muertos**; el vivo es R11, ya declarado equivalente en la r01;
  - del revisor r02 (`revisores/r02_mutantes.py`): **8 de 12 muertos, 4 vivos** (N-04).
- **Ataques:**
  - del revisor r01 (`revisores/r01_ataques.py`): **10 de 10 OK**; H-01 a H-08 se reproducen como corregidos.
  - del revisor r02 (`revisores/r02_ataques.py`): B2, B3 y B4 OK; B1 y B5 son hallazgos; B6 confirma la carrera de `_acuses`. `revisores/r02_final_doble.py`: la final no se duplica.
- **Backtest del README** sobre una extracción de `06a8cc79`: rc 0. `senales.csv`, `pronosticos.csv` y `metricas.json` son idénticos (md5) a los de `6045913`. Las huérfanas que ahora mira `enviar_pendientes` no cambian nada sin PET-.

### Cada corrección de la r01

| Hallazgo | Corregido | Evidencia |
| --- | --- | --- |
| H-01 | sí | `r01_ataques.py` A2 OK (3 servidas); `test_atender_no_se_corta…` (con y sin reloj); M41, M42, Q4 y Q5 muertos |
| H-02 | sí | A1 y A3 OK; el reintento con el mismo msg_id del Broker devuelve la misma PET- (`repetido`) |
| H-03 | sí, salvo N-01 | A7 OK. B2: otro proceso que muere con `os._exit` deja una sola incidencia; el motivo vacío se rechaza; `reconciliar` da FALLIDA y la final FALLIDO; la segunda reconciliación se rechaza. B3: con un proceso vivo no hay huérfana y `reconciliar` se rechaza |
| H-04 | sí | A5 OK: la PET- se admite con la hora truncada a microsegundos; Q12 muerto. El docstring del módulo dice lo contrario (N-03) |
| H-05 | sí | A4 OK: las dos horas del cambio de hora dan `PeticionInvalida`; Q6 muerto |
| H-06 | sí | `servir` rechaza una PET- ENCOLADA, inexistente o vacía (B4); lo tomado y no servido aparece como huérfano (A6) |
| H-07 | sí | A8 OK; R4 y Q7 muertos |
| H-08 | sí | R6, R12 y R13 muertos |
| H-09 | sí | R2, R9 y R10 muertos |

### Lo que pidió juzgar el coordinador

- **H-01 y el cambio de `test_un_instante_anterior_a_una_recepcion_no_ordena_ni_sirve`.** Es **legítimo**, no un debilitamiento.
  - Es la semántica que pedía la corrección de la r01: una petición recibida después de t aún no había llegado en t.
  - La prueba sigue exigiendo que no se ordene ni se sirva nada y que el estado quede ENCOLADA.
  - Conserva el rechazo de la prioridad de esa petición en un instante anterior a su propia recepción.
  - Los mutantes M41 y Q4, que reintroducen ver las posteriores, mueren.
- **H-04: truncar en vez de rechazar.** **Aceptable.**
  - La r01 admitía las dos salidas, y A5 esperaba que se admitiera.
  - El truncado es explícito, determinista y va antes de reservar el msg_id.
  - Está declarado en INC-T196-01 («los nanosegundos se truncan»).
  - El docstring de cabecera de `cola_peticiones.py` sigue diciendo «nanosegundos … se rechazan» (N-03).
- **H-06: `tomar` sigue pública y se añade `servir`.** **Aceptable.**
  - `servir` exige una PET- EN_CURSO tomada por este proceso, y lo que no se sirve se avisa como huérfano.
  - Ninguna prueba mata quitar la comprobación del `pid` en `servir` (Q8 vivo, N-04).
- **Lo añadido fuera del qa.md.**
  - Que lo escrito en F5 lleve el día de la toma (`fijar_fecha` en cada toma de `atender` y en `reconciliar`) es coherente con `consulta`. Ninguna prueba lo exige (Q10 vivo, N-04).
  - La prueba de recepciones concurrentes mata R7, confirmado.
- **Carrera de `contratos.Mensajeria._acuses`.** **Existe.**
  - B6: seis instancias abren a la vez un almacén nuevo. En 3 de 15 intentos (1 de 15 en la primera pasada) salta `OperationalError: duplicate column name: error`.
  - La causa es el par `PRAGMA table_info` + `ALTER TABLE` sin cerrojo entre instancias.
  - Es anterior a T-196 (T-92) y afecta igual a `Bloque.peticion`.
  - El esquive de `test_recepciones_concurrentes…`, que crea la tabla antes, **no tapa nada de T-196**. La carrera solo ocurre al crear el fichero `acuses.sqlite3`, y lo que esa prueba mide (posición y escritura de la PET- bajo transacción) va después de `procesar_una_vez` y es independiente de esa creación.
  - Conforme con llevarla a un ticket aparte. La corrección sugerida: `ALTER` dentro de un `try` que tolere «duplicate column», o la creación bajo `almacen._transaccion()`.

### Hallazgos r02

| ID | Gravedad | Cómo reproducirlo | Esperado / obtenido | Corrección exacta | Prueba de regresión | Estado |
| --- | --- | --- | --- | --- | --- | --- |
| N-01 | **media** | `r02_ataques.py` B1: una consulta encolada y `atender`. Justo después del ciclo y antes de ATENDIDA, otro hilo del mismo proceso llama a `huerfanas()` y a `reconciliar()` | Esperado: una PET- que se está sirviendo no es huérfana. Obtenido: el `finally` de `_servir` quita la PET- de `_EN_MARCHA` en cuanto vuelve el ciclo, antes de `_escalado`, de la ATENDIDA y de la final. En ese hueco, `huerfanas()` (que ahora corre en cada `enviar_pendientes`, es decir, en cada consulta o ciclo de otro hilo) deja una incidencia de huérfana falsa, y `reconciliar` la acepta. Resultado: el Broker recibe la final **FALLIDO** de un análisis que terminó COMPLETO; después el hilo que servía escribe ATENDIDA y el escalado COMPLETO, y F5 y HA quedan contradictorios (FALLIDA reconciliada, ATENDIDA, final FALLIDO). Desde otro proceso no pasa, porque su `pid` vive (B3) | Sacar el `discard` de `_EN_MARCHA` del `try` del ciclo y ponerlo en un `try/finally` que envuelva todo `_servir`, hasta después de la ATENDIDA y de `respuesta_final.enviar` (o de `_fallida`). Así la PET- solo deja de estar «en marcha» cuando ya no está EN_CURSO | `test_una_peticion_en_servicio_no_es_huerfana_hasta_quedar_atendida`: un monkeypatch de `_escalado` lanza otro hilo que llama a `huerfanas()` (debe dar `[]`) y a `reconciliar()` (debe rechazarse con `PeticionInvalida`); al final, ATENDIDA, final COMPLETO y ninguna incidencia de huérfana | abierto |
| N-02 | baja | B5: `atender` con un reloj que devuelve 10:10, 10:10 y después 09:00:30 | Esperado: fallo cerrado ante un reloj que retrocede. Obtenido: la segunda toma, con el instante anterior, no ve las PET- recibidas a las 09:01 y 09:02, y `atender` termina en silencio con 1 servida y 2 ENCOLADAS, como si la cola estuviera vacía | En `atender`, guardar el instante de la toma anterior y, si el reloj devuelve uno menor, lanzar `PeticionInvalida` («el reloj retrocede»), sin tomar nada más. Lo servido queda como está | `test_atender_con_un_reloj_que_retrocede_falla_cerrado` | abierto |
| N-03 | baja | Cabecera de `cola_peticiones.py`, viñeta «r02 (QA r01)» | Dice «H-04 y H-05: nanosegundos y horas inexistentes o ambiguas … se rechazan con `PeticionInvalida`». El código, `_fecha_hora` e INC-T196-01 dicen que los nanosegundos se **truncan** | Corregir la frase: los nanosegundos se truncan a microsegundos; las horas inexistentes o ambiguas se rechazan | Ninguna: es documentación | abierto |
| N-04 | baja | `r02_mutantes.py`: vivos Q2 (la huérfana sin mirar el `host`), Q8 (`servir` sin comprobar el `pid`), Q10 (`atender` sin `fijar_fecha` del día de la toma) y Q11 (un `pid` vivo cuenta como huérfana) | Ramas del diseño r02 sin una prueba que las mate. Q11 y Q2 son la protección contra reconciliar lo que sirve otro proceso u otra máquina | Sin cambio de código | Cuatro pruebas: (Q2) una PET- EN_CURSO con `host` distinto y `pid` inexistente no es huérfana; (Q8) `servir` de una EN_CURSO con otro `pid` se rechaza; (Q10) una PET- recibida un día y atendida al siguiente deja su RUN- y su ATENDIDA con la fecha del día de la toma; (Q11) con un subproceso vivo que la tiene tomada, `huerfanas() == []` y `reconciliar` se rechaza (como B3) | abierto |

### Veredicto r02

**NO APTO.** H-01 a H-09 están corregidos y verificados con los scripts del revisor. Queda abierto N-01 (media): la ventana entre el fin del ciclo y la ATENDIDA permite marcar como huérfana, y reconciliar como FALLIDA, una petición que se está sirviendo, y el Broker recibe una final FALLIDO falsa. Su corrección es local (mover el `finally`).

N-02 a N-04 son bajos y se corrigen en la misma ronda, por regla del operador. En la r03, el revisor volverá a pasar:
- `r01_ataques.py`, que debe seguir 10 de 10;
- `r02_ataques.py`, con B1 y B5 en OK; B6 es la carrera de otro ticket;
- `r01_mutantes.py` y `r02_mutantes.py`, todos muertos salvo R11;
- el `mutantes.py` del implementador.

---

## Ronda r03 · 2026-11-24

- **Revisor:** el mismo de la r01 y la r02 (claude, subagente revisor nuevo).
- **Código revisado:** `wip/t196`, commit `3db5b6fa`, encima de `06a8cc79`, en el worktree `qa_t196`.
- Los scripts r01 y r02 del revisor y el `qa.md` r02 que sube el commit son idénticos byte a byte a los del revisor.
- El diff de código toca solo `cola_peticiones.py`: el envoltorio `_servir`, el control del reloj en `atender` y el docstring. Las pruebas solo crecen: ninguna línea quitada en `test_t196.py`.

### Reproducción

- **Gate del implementador** (`gate_t196_r03.log`): 12/12, con RC=0.
  - Pytest: A 8421, FX 68, B 176.
  - Ruff y mypy en su cuota.
- `pytest -q tests/test_t196.py`: **62 passed**.
- **Mutantes:**
  - del implementador (`mutantes.py`): **61 de 61 muertos**;
  - del revisor r01: **13 de 14** (R11, equivalente, declarado en la r01);
  - del revisor r02: **12 de 12**;
  - del revisor r03 (`revisores/r03_mutantes.py`): **1 de 2**; P1 vivo (M-01).
- **Ataques:**
  - `r01_ataques.py`: **10 de 10 OK**.
  - `r03_ataques.py` (los de la r02, con B5 corregido): B1 a B5 **OK**. B6, la carrera de `_acuses` de otro ticket, no se reprodujo en esta pasada (0 de 15). Es probabilística, y en la r02 salió 1 y 3 de 15.
- **Backtest del README:** no se ha repetido. La r03 solo cambia `atender` y `_servir`, que el backtest no recorre. En la r02 salió idéntico a develop.

### B5 estaba mal planteado

**Sí.** En la r02, B5 solo daba OK si `atender` servía las 3 peticiones con un reloj que retrocede. Eso contradecía la corrección que el propio revisor pedía en N-02: lanzar `PeticionInvalida` y no tomar nada más.

Con la corrección aplicada, `r02_ataques.py` B5 sale en ERROR. Es lo correcto: es la excepción que exige N-02, no una regresión.

El script queda intacto como registro de la ronda. `revisores/r03_ataques.py` es su copia con B5 reescrito:
- exige `PeticionInvalida` con 1 ATENDIDA y 2 ENCOLADAS intactas;
- ejecuta su segunda parte (un reloj que devuelve basura a mitad: `PeticionInvalida`, 1 ATENDIDA y 1 ENCOLADA).

Resultado: **OK**.

### Cada corrección de la r02

| Hallazgo | Corregido | Evidencia |
| --- | --- | --- |
| N-01 | sí | B1 OK: el otro hilo ve `huerfanas() == []`, `reconciliar` se rechaza, 0 incidencias de huérfana, ATENDIDA con la final del análisis (escalado COMPLETO). `test_una_peticion_en_servicio_no_es_huerfana_hasta_quedar_atendida`; M56 muerto. El `finally` del envoltorio cubre también la FALLIDA y una final que falle al enviarse |
| N-02 | sí, salvo M-01 | B5 (r03) OK; `test_atender_con_un_reloj_que_retrocede_falla_cerrado`; M57 y P2 muertos (un instante igual no es un retroceso, de modo que `atender` con un instante fijo sigue funcionando) |
| N-03 | sí | La cabecera dice ahora que los nanosegundos se truncan y que las horas inexistentes o ambiguas se rechazan, igual que `_fecha_hora` e INC-T196-01 |
| N-04 | sí | Q2, Q8, Q10 y Q11 muertos (`r02_mutantes.py` 12 de 12; M58 a M61) |

### Hallazgos r03

| ID | Gravedad | Cómo reproducirlo | Esperado / obtenido | Corrección exacta | Prueba de regresión | Estado |
| --- | --- | --- | --- | --- | --- | --- |
| M-01 | baja | `r03_mutantes.py` P1: quitar `previo = t` del bucle de `atender`, de modo que el retroceso solo se compare con el primer instante | Debería morir. Queda vivo: con un reloj 10:00 → 10:05 → 10:02, el mutante admite las 10:02 (posterior al primero, anterior al de la toma previa) y `atender` deja de ver lo recibido entre 10:02 y 10:05. Es el síntoma de N-02, pero no lo mata ninguna prueba, porque la de la r03 retrocede por debajo del primer instante | Sin cambio de código | En `test_atender_con_un_reloj_que_retrocede_falla_cerrado`, un segundo caso con un reloj que sube y luego baja sin pasar por debajo del primer instante (p. ej. t0+10 min, t0+10 min, t0+12 min, t0+11 min): `PeticionInvalida` tras la segunda servida y el resto ENCOLADA | abierto |

### Veredicto r03

**APTO, pendiente de la ronda de cierre.** H-01 a H-09 y N-01 a N-04 están corregidos y verificados con los scripts del revisor, y no hay regresiones. No queda ningún hallazgo alto ni medio.

Queda un bajo, M-01: una prueba que falta, sin cambio de código. Por regla del operador no va a la deuda. En la ronda de cierre, el revisor comprobará que la prueba nueva existe y pasa, y que `r03_mutantes.py` da 2 de 2 muertos. Si es así, la QA queda cerrada como APTO.

---

## Ronda de cierre · 2026-11-24

- **Revisor:** el mismo de las rondas r01 a r03.
- **Código revisado:** commit `fbec7d0b`, encima de `3db5b6fa`, en el worktree `qa_t196`.
- **Qué cambia:** solo pruebas y documentos del ticket. El diff no toca `bloque_a/11_Ejecutor/bloque_a/`.
- **Scripts:** los del revisor (r01, r02 y r03) y el `qa.md` r03 que sube el commit son idénticos byte a byte a los del revisor.

### M-01

- **La prueba.** `test_atender_con_un_reloj_que_retrocede_falla_cerrado` pasa a estar parametrizada y tiene dos casos:
  - **(10, 10, 0,5, 11) min**: el reloj retrocede por debajo del primer instante, como en B5. Exige 1 ATENDIDA y 2 ENCOLADAS.
  - **(10, 10, 12, 11) min**: el reloj sube y baja sin pasar por debajo del primero. Exige `PeticionInvalida` tras la segunda servida, con 2 ATENDIDAS y 1 ENCOLADA.
  - Con el mutante P1, la toma de las 10:11 se admitiría (es posterior a las 10:10 iniciales) y serviría la tercera. La prueba cubre exactamente lo que pedía M-01.
- **Pruebas:** `pytest -q tests/test_t196.py` da **63 passed** (62 más el caso nuevo).
- **Mutantes:**
  - `revisores/r03_mutantes.py` da **2 de 2 muertos**; P1 muere.
  - En `mutantes.py`, M62 (el mismo P1) y M57 están **muertos**.
  - No se han repetido los otros 60 mutantes del implementador ni los ataques. El código bajo prueba no ha cambiado desde la r03, donde dieron 61 de 61 y B1 a B5 OK.
- **Gate:** no hay gate nuevo para esta ronda, porque el cambio es solo de pruebas. El último es el de la r03 (`gate_t196_r03.log`, 12/12).
- **Al integrar en develop:** develop ya lleva T-200 (la carrera de `_acuses`, en `contratos.py`). Al integrar T-196 hay que pasar `./tools/check_all.sh` sobre el resultado de la fusión, como siempre. No hay solape de ficheros de código con T-196.

### Veredicto final

**APTO, sin nada abierto.**

| Ronda | Hallazgos | Estado |
| --- | --- | --- |
| r01 | H-01 a H-09 | corregidos y verificados en la r02 |
| r02 | N-01 a N-04 | corregidos y verificados en la r03 |
| r03 | M-01 | corregido y verificado en esta ronda |

La carrera de `_acuses` (B6) no era de T-196. Va en T-200, ya en develop. Ningún hallazgo queda abierto ni pasa a la deuda.
