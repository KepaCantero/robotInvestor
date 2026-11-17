# T-169 · QA independiente

- **Revisor:** Claude, el mismo subagente revisor de la QA r01 de T-162 (no implementó ni T-162 ni T-169) · **Ronda:** r01 · 16-11-2026
- **Copia:** worktree `qa43` en `ab10556` («wip local: T-169», encima de T-162 `3533cb7`), `.venv` enlazado. Sin red ni gasto.

## Reproducción desde limpio

| Comprobación | Resultado |
| --- | --- |
| Suite completa de A (`cd bloque_a/11_Ejecutor && ../../.venv/bin/python -m pytest -q -p no:cacheprovider`) | 6947 recogidas: 6931 pasan, 2 omitidas y 14 fallan (49 min). Las 14 son las de `test_fase3_goldens.py`, previstas desde T-162. `test_t102_filtro` no falló |
| `test_t169_hallazgos_t162.py` y `test_t162_respuesta_final.py` | pasan (dentro de la suite) |
| Sondas del revisor de T-162 (`.docs/tickets/T-162/revisores/r01_01_sondas.py`) | 10 pasan. Las 2 `test_s02b_*` dan XPASS(strict), porque H-03 de T-162 está corregido. `test_s08_*` falla porque afirmaba lo que H-02 corrige. Es lo declarado |
| Goldens regenerados en una copia desechable (`git archive HEAD bloque_a docs sistema_global/seguimiento`, `goldens_ct.py --update`) | Solo cambia `formas_flujos_mock.json`, con huella `6b7339b2…6c24`, la misma que con T-162: T-169 no añade nada. `divergencias_anexo_b.json` y el resto no cambian |
| Cuotas | ruff 2821 (≤ 2821); mypy de A 109 (≤ 109) |
| Gates ligeros | `refs_vivas`, `secrets_scan`, `nfc_check` y `corpus_integridad` (695) en verde |
| Mutantes del implementador (`.docs/tickets/T-169/scripts/mutantes_t169.py`) | Mis 25 de T-162: 22 mueren, M15 vive (equivalente) y M03/M24 cambian de texto (sus versiones M03b/M24b mueren). Los 15 propios N01–N15 mueren todos |
| Mutantes del revisor (`revisores/r01_03_mutantes.py`, Q01–Q10, con el mismo ejecutor) | 7 mueren con las pruebas del ticket. Q10 solo lo mata mi sonda p01. Q02 y Q03 viven también con mis sondas (H-04) |

## Criterios de aceptación

| Criterio | Cumple | Evidencia |
| --- | --- | --- |
| CA-1 (H-01 de T-162) | sí | `test_h01_*`; sonda p07: un `EscrituraFueraDeReserva` lanzado tras registrar el RUN- se relanza sin QRY en F5, sin CT-03 RETORNO y sin HERRAMIENTA. Mutantes Q04 y Q05 muertos. Ver H-02 de esta QA para `ReplayFaltante` |
| CA-2 (H-02 de T-162) | sí, con H-01 y H-03 de esta QA | `test_h02_*`. Sonda p01: dos pendientes de fechas distintas; un ciclo entre ellas envía solo la primera, el siguiente la segunda y un tercero ninguna. Sonda p02: una final «borrada» con un `respuesta_final: None` posterior no se reenvía. Sonda p03 y `r01_02`: 8 hilos y 4 procesos a la vez con una pendiente enviable dan un solo mensaje y una sola final en F5 |
| CA-3 (H-03 de T-162) | sí | `test_h03_*`; `test_s02b_*` en XPASS |
| CA-4 (H-04 de T-162) | sí | M01, M02, M07, M11, M12 y M16 mueren con las pruebas de T-169 |
| CA-5 | sí | ver «Reproducción». Además, `r01_02` frente a HEAD~1 (`3533cb7`): sin pendientes, un ciclo de RV da los mismos 8 mensajes y los mismos F1–F11, RC y HA. Un ciclo seguido de la consulta escalada de PB-07 da los mismos 12 mensajes y todo igual salvo F5, que solo añade la entrada del registro de la provisional. Se comparan sin `_ts`, `_hash` ni `timestamp`, y con las rutas de trabajo normalizadas |

## Hallazgos

| ID | Gravedad | Cómo reproducirlo | Esperado / obtenido | Corrección sugerida | Estado |
| --- | --- | --- | --- | --- | --- |
| H-01 | media | `revisores/r01_01_sondas.py::test_p05_*` (xfail estricto): una QRY- pendiente cuyo `escalado` no lleva `clases` (estado de otra versión del código, o manipulado) y después dos `ciclo` | Esperado: que una final pendiente que no se puede construir no pare el resto del bloque. Obtenido: `construir` lanza `KeyError` y, como no es un rechazo de la lista, `enviar_pendientes` lo relanza al empezar **cada** `ciclo` (también el semanal) y **cada** `consulta`, sin ninguna incidencia en HA, hasta que alguien toque F5 a mano. El diseño lo dice («cualquier otro error para»), pero el riesgo «una pendiente que nunca se puede enviar bloquearía todas las consultas y ciclos» solo queda mitigado para los rechazos | En `enviar_pendientes`, relanzar solo lo que para la consulta según H-01 (`para_la_consulta`: integridad o control) y apartar cualquier otro error con su incidencia escalada, como se hace con los rechazos. Prueba de regresión: p05 |
| H-02 | baja | `test_p06_*` (xfail estricto): `ciclo` lanza `llm.ReplayFaltante` (respuesta no grabada en `--cliente replay --replay-modo reproducir`) | Esperado: que pare como antes de T-162, porque es un fallo de la reproducción y no del análisis. Obtenido: final FALLIDO e incidencia HERRAMIENTA. Una reproducción que diverge se envía al Broker como «el análisis falló» | Añadir `ReplayFaltante` a `ERRORES_DE_CONTROL` (o tratar aparte los errores del cliente en modo reproducir) y apuntarlo en INC-T169-01 |
| H-03 | baja | `test_p04_*` (xfail estricto: 8 hilos, en esta ejecución 3 apartados) y `r01_02`, bloque 1 (4 procesos con una pendiente que la mensajería rechaza: 4 entradas `final_no_enviable` y 4 incidencias escaladas) | Esperado: que se aparte «una vez», como dice el diseño. Obtenido: el apartado (la entrada en F5 y la incidencia) se escribe fuera de la transacción de `enviar`, así que cada hilo o proceso que la ve rechazada la aparta y escala otra vez. No sale ningún mensaje ni se copia el dato protegido | Hacer el apartado bajo `almacen._transaccion()` y volver a mirar dentro si ya está `final_no_enviable` (o la final) antes de escribir |
| H-04 | baja | `r01_03_mutantes.py` | Sobreviven Q02 (pendientes en orden inverso: ninguna prueba envía dos pendientes a la vez) y Q03 (quitar la comprobación de integridad del `except` de los rechazos en `enviar_pendientes`: ninguna prueba rompe el almacén durante el envío de una pendiente). Q10 (pendientes sin fecha de corte) solo lo mata mi sonda p01 | Añadir pruebas con dos pendientes enviadas en la misma llamada, con un rechazo y el almacén roto a la vez, y la de p01 |

**Notas (sin hallazgo):**
- Sonda p08: si la `provisional_msg_id` de F5 se reescribe con la del encargo, la final se enlaza a ese mensaje. Hace falta escribir en F5 como AG-01 y no hay un registro persistente de mensajes con que compararlo, así que no lo trato como hallazgo.
- `FugaDeInformacion` y los `PermissionError` paran. `ErrorFicha` y `_PosteriorAlCorte` los recoge el Motor y no llegan a `consulta`. `PresupuestoAgotado` no se lanza en ningún sitio.

## Veredicto

**NO APTO.** Los cinco criterios se cumplen y no hay hallazgos críticos ni altos. El NO APTO se debe solo a la regla del operador de hoy: los hallazgos bajos se subsanan en el mismo ticket, y quedan abiertos H-02, H-03 y H-04. H-01, que es medio, toca el mismo código (`enviar_pendientes`) y conviene corregirlo en la misma ronda. Así no hay que llevar a la deuda que una pendiente pueda parar el ciclo semanal. Tras la corrección, se repiten `revisores/r01_*` (las xfail estrictas de p04, p05 y p06 pasarán a XPASS) y se abre la ronda r02. No cierro el ticket.

## Scripts del revisor (orden)

Desde la raíz de la copia de trabajo:

1. `cd bloque_a/11_Ejecutor && ../../.venv/bin/python -m pytest -q -p no:cacheprovider ../../.docs/tickets/T-169/revisores/r01_01_sondas.py` (5 pasan y 3 xfail estrictos de H-01, H-02 y H-03; ≈ 35 s).
2. `git archive HEAD~1 bloque_a | tar -x -C <base>` y `.venv/bin/python .docs/tickets/T-169/revisores/r01_02_procesos_y_base.py <trabajo> <base>/bloque_a`. Hoy da 1 fallo, el de H-03; lo demás está en verde (≈ 10 min).
3. Copia desechable `<…t169_mut>` con `git archive HEAD bloque_a` y `.venv` enlazado; `.venv/bin/python .docs/tickets/T-169/scripts/mutantes_t169.py .docs/tickets/T-169/revisores/r01_03_mutantes.py <…t169_mut>` (Q02 y Q03 vivos: H-04).

---

# Ronda r02

- **Revisores:** Claude, subagentes revisores nuevos (no implementaron ni T-162 ni T-169). El primero empezó la ronda y se cortó
  por una pausa esperando los mutantes (instantánea `2aa9276`, rama `wip/qa169r02`). El segundo la termina: reutiliza sus scripts
  (`r02_01_sondas.py`, `r02_02_mutantes.py`), repite cada comprobación, añade `r02_03_sondas.py` y firma el veredicto · 17-11-2026
- **Copia:** worktree `qa169r02` sobre `ec25a60` («wip local: T-169 r02»), con `.venv` enlazado y los `qa.md` y `revisores/` de
  T-162 y T-169 copiados de `t162`. Las copias desechables son `qa169r02b_t169_mut` (mutantes) y `qa169r02b_fix` (prueba de la
  corrección de H-01). Sin red ni gasto. Por consigna de la sesión no se ejecutan la suite completa de A ni el gate: solo las
  pruebas de T-162 y T-169, las sondas y los mutantes.

## Reproducción

| Comprobación | Resultado |
| --- | --- |
| `tests/test_t169_r02.py`, `tests/test_t169_hallazgos_t162.py` y `tests/test_t162_respuesta_final.py` | Pasan las 58 (8 + 28 + 22) |
| `revisores/r01_01_sondas.py` de T-169 | 5 pasan. p04, p05 y p06 dan XPASS(strict): H-03, H-01 y H-02 de la r01 están corregidos |
| `revisores/r01_01_sondas.py` de T-162 | Igual que en la r01: 10 pasan, las 2 `test_s02b_*` dan XPASS(strict) y `test_s08_*` falla porque afirmaba lo que H-02 de T-162 corrige |
| `revisores/r01_02_procesos_y_base.py` (base `3533cb7`) | `fallos: 0`. Con 4 procesos, la pendiente enviable sale una vez y la rechazada se aparta una vez con una incidencia (en la r01, 4 y 4). El ciclo RV y la consulta PB-07 quedan iguales a la base, salvo el registro de la provisional en F5 |
| `revisores/r02_01_sondas.py` (13 sondas) | 12 pasan. `test_a07_*` es xfail estricto (H-01 de esta ronda) |
| `revisores/r02_03_sondas.py` (4 sondas, nuevas) | 3 pasan. `test_b01_*` es xfail estricto: H-01 de esta ronda reproducido sin simular nada, con `contadores.json` ilegible |
| Mutantes | Ver la tabla de mutantes |
| ruff de los ficheros tocados | `All checks passed!` en `respuesta_final.py`, `test_t169_r02.py` y `test_t169_hallazgos_t162.py` |

## Hallazgos de la r01, uno a uno

| ID r01 | Comprobación | Estado |
| --- | --- | --- |
| H-01 (media) | p05 da XPASS; `test_r02_h01_*`; sondas `a01`–`a04` y `b02`. Un error corriente se aparta con una marca y una incidencia escalada, la siguiente pendiente de la misma llamada sale y los ciclos siguen. Un error de control (`FugaDeInformacion`, `ReplayFaltante`, `EscrituraFueraDeReserva`, `CanalNoPrevisto`) para cada `ciclo` y cada `consulta` sin apartar nada. Un error corriente con el almacén roto para sin apartar, y también para el fichero de sellos ilegible. Un F5 editado a mano (`b04`) y un `KeyboardInterrupt` (`b03`) paran sin apartar. Queda el caso de H-01 de esta ronda | cerrado |
| H-02 (baja) | p06 da XPASS; `test_r02_h02_*`; el mutante R01 muere | cerrado |
| H-03 (baja) | p04 da XPASS; `r01_02` deja 1 apartado y 1 incidencia con 4 procesos. En `a05`, una consulta escalada llama dos veces a `enviar_pendientes` (la suya y la de su `ciclo`) y deja una sola marca, una sola incidencia «apartada» y una sola SEGURIDAD del R8. R03 y R04 mueren | cerrado |
| H-04 (baja) | Q02b, Q03b y Q10 mueren con las pruebas del ticket | cerrado |

**La prueba que cambia de expectativa** (`test_h02_un_error_de_control_en_una_pendiente_para_la_consulta_y_no_aparta`) conserva
todas sus aserciones:
- la excepción sale de `consulta`;
- la pendiente sigue en la lista;
- no se aparta nada;
- la consulta nueva no empieza (2 entradas QRY en F5).

Solo cambia `RuntimeError` por `EscrituraFueraDeReserva`. Lo que protegía era «un error que no es un rechazo no se aparta», y eso
ahora solo vale para los de control. El camino «control → para» sigue cubierto aquí (mata S02 y N15). El de `RuntimeError`, que
ahora se aparta por diseño (H-01 de la r01), lo cubre `test_r02_h01_un_error_corriente_en_una_pendiente_no_para_la_consulta`.

Con el cambio sí quedó sin cubrir la otra mitad de `para_la_consulta` en `enviar_pendientes`: un error corriente **con el almacén
roto**. Ninguna prueba del ticket lo comprueba (S01 vive; H-02 de esta ronda), aunque el código lo hace bien (sonda `a01`).

## Mutantes

| Lista | Resultado |
| --- | --- |
| `r02_02_mutantes.py` (revisor r02) | S02, S03, S04 y S05 mueren. **S01 vive** (H-02 de esta ronda). S06 y S07 viven, pero son de defensa o equivalentes. S01 lo mata la sonda `a01` (comprobado en `qa169r02b_t169_mut`) |
| `r01_03_mutantes.py` (revisor r01) | Q01, Q06, Q07, Q08 y Q10 mueren. Q02, Q03, Q04, Q05 y Q09 dan TEXTO_CAMBIADO porque la r02 reescribió su código; sus versiones sobre el texto nuevo están en `--propios` |
| `--propios` del implementador | Mueren los 26: M03b, M24b, N01–N15, Q02b, Q03b, Q04b, Q05b, Q09b y R01–R04 |

## Hallazgos de la r02

| ID | Gravedad | Cómo reproducirlo | Esperado / obtenido | Corrección exacta | Estado |
| --- | --- | --- | --- | --- | --- |
| H-01 | baja | Sin simular nada: `revisores/r02_03_sondas.py::test_b01_*` (xfail estricto). Hay una pendiente; `contadores.json` (sin sello y fuera de `verificar_integridad`) se vuelve ilegible; `ciclo`; se repara el fichero; otro `ciclo`. Con la incidencia simulada: `r02_01_sondas.py::test_a07_*` | **Esperado:** una pendiente nunca queda apartada sin escalar (falla cerrado y valida antes de mutar). **Obtenido:** `enviar` falla al pedir el MSG- con un `JSONDecodeError`. Es un error corriente con el almacén «íntegro», así que va a `_apartar`, que escribe primero la marca `final_no_enviable` en F5 y luego pide el INC- de la incidencia, que falla igual. El primer `ciclo` se para, pero cuando se repara el fichero la pendiente ya no está en la lista: queda marcada, sin incidencia y sin aviso al operador (`marcada True escalada False`). La final al Broker se pierde sin rastro en HA | En `respuesta_final._apartar`, invertir el orden: primero `almacen.incidencia(...)` y después `almacen.escribir("F5", "AG-01", {..., "final_no_enviable": {"error": error}})`. Si falla la marca, la pendiente sigue y se reintenta: como mucho se repite la incidencia, nunca hay un apartado silencioso. Lo comprobé en `qa169r02b_fix`: con el cambio, `a07` y `b01` dan XPASS, siguen pasando las 58 pruebas y las demás sondas de `r02_01` y `r02_03`. Hay que pasar `a07` y `b01` a `tests/test_t169_r02.py` como pruebas de regresión, sin xfail | abierto |
| H-02 | baja | Mutante S01 de `r02_02_mutantes.py`: en `enviar_pendientes`, cambiar `if para_la_consulta(almacen, e):` por `if isinstance(e, ERRORES_DE_CONTROL):` | **Esperado:** que lo mate alguna prueba del ticket, porque es el camino por el que un error corriente con el almacén roto para en vez de apartarse (falla cerrado). **Obtenido:** vive con las 58 pruebas de T-162 y T-169. Lo mata la sonda `test_a01_*` (`KeyError`, `RuntimeError` y `OSError` con el sello de F2 roto) | Añadir a `tests/test_t169_r02.py` la prueba de `a01`, parametrizada con `KeyError("clases")`, `RuntimeError` y `OSError`: una pendiente cuyo `construir` rompe el sello de F2 (como en `test_r02_h04_un_rechazo_con_el_almacen_roto_para_y_no_aparta`) y lanza el error; `pytest.raises(type(error))` sobre `b.ciclo(D2)`; sin marca `final_no_enviable`, sin incidencia «apartada» y `verificar_integridad()` con algún `False`. Añadir S01 a `PROPIOS` de `scripts/mutantes_t169.py` | abierto |
| H-03 | baja | `docs/incidencias.md`, línea 623 (INC-T169-01, párrafo H-02), y `bloque_a/11_Ejecutor/README.md`, línea 201 | **Esperado:** documentación al día. **Obtenido:** el párrafo de la r01 sigue diciendo «Cualquier otro error, también uno de integridad, para la consulta o el ciclo.», que contradice la r02 añadida debajo. El README del ejecutor solo dice que se aparta «una que la mensajería rechaza» y no menciona `ReplayFaltante` | En `docs/incidencias.md`, sustituir esa frase por «Un fallo de integridad o de control para la consulta o el ciclo; desde la r02, cualquier otro error se aparta igual, con su incidencia escalada.». En el README, sustituir «y una que la mensajería rechaza se aparta con incidencia al operador» por «y una que no se puede enviar (un rechazo de la mensajería o cualquier error que no sea de integridad ni de control) se aparta una vez, con incidencia al operador; una respuesta no grabada del modo «reproducir» (`ReplayFaltante`) para la consulta» | abierto |

**Notas (sin hallazgo):**
- `a08` es anterior a la r02 y viene del diseño de T-162. Si la mensajería crea la final y luego falla la escritura en F5 con un
  error corriente (`OSError`), la pendiente se aparta y la incidencia dice «no se puede enviar», aunque el mensaje se creó. Con
  la r01 el error se propagaba y el ciclo siguiente la reenviaba sola (duplicado automático); con la r02 decide el operador al
  reenviarla. No es una regresión. Como la corrección de H-01 ya toca `_apartar`, conviene que el detalle diga «puede haberse
  creado el mensaje; revisar antes de reenviar».
- Una pendiente con un error de control para todos los `ciclo` y `consulta` hasta que se corrija, y no deja incidencia propia en
  HA (salvo `CanalNoPrevisto`, que deja una CANAL_NO_PREVISTO por intento desde `Mensajeria.validar`). Es fallar cerrado, como
  pidió la r01, y la excepción llega al operador. No hay incidencias duplicadas de apartado: con hilos, procesos, consulta + ciclo,
  ni repitiendo llamadas (`a05`, `a06`, `b02`).
- No hay números nuevos ni LLM en el camino. Tampoco secretos: el correo de las sondas es ficticio y no llega a HA (`a05`).

## Veredicto r02

**NO APTO.** Los criterios r02 del README se cumplen: p04, p05 y p06 dan XPASS, `r01_02` no tiene fallos, Q02, Q03 y Q10 (y sus
versiones) mueren y ruff está limpio. Los cuatro hallazgos de la r01 están cerrados y no hay hallazgos críticos, altos ni medios.
El NO APTO se debe a la regla del operador de que los bajos se subsanan en el mismo ticket: siguen abiertos H-01, H-02 y H-03 de
esta ronda, y para cada uno hay arriba una corrección exacta. H-01 es el más importante: una final al Broker puede quedar apartada
sin aviso, y la corrección es invertir dos llamadas.

Con la ronda de cierre se vuelven a pasar `r02_01_sondas.py` y `r02_03_sondas.py` (a07 y b01 pasarán a XPASS) y el mutante S01. La
suite completa de A y el gate quedan para la integración, con el re-congelado de `formas_flujos_mock.json` de T-162. No cierro el
ticket.

## Scripts del revisor r02 (orden)

Desde la raíz de la copia de trabajo:

1. `cd bloque_a/11_Ejecutor && ../../.venv/bin/python -m pytest -q -p no:cacheprovider -rxX ../../.docs/tickets/T-169/revisores/r02_01_sondas.py ../../.docs/tickets/T-169/revisores/r02_03_sondas.py`
   (15 pasan y 2 xfail estrictos de H-01; ≈ 30 s). Las `r01_01_sondas.py` de T-162 y de T-169 se lanzan por separado, porque
   tienen el mismo nombre de módulo.
2. `r01_02` como en la r01, con la base `git archive 3533cb7 bloque_a` (≈ 10 min).
3. Una copia desechable cuyo nombre contenga `t169_mut` (`git archive HEAD bloque_a`, con `.venv` enlazado) y
   `.venv/bin/python .docs/tickets/T-169/scripts/mutantes_t169.py .docs/tickets/T-169/revisores/r02_02_mutantes.py <copia>`;
   lo mismo con `revisores/r01_03_mutantes.py` y con `--propios`.

---

# Ronda de cierre

- **Revisor:** el mismo de la r02 (no implementó) · 17-11-2026
- **Copia:** `git archive 25563df` («wip local: T-169 ronda de cierre», encima de `d845e3c`) en dos copias desechables:
  `qa169cierre_v` para las pruebas y las sondas, y `qa169cierre_t169_mut` para los mutantes. Las dos tienen `.venv` enlazado. La
  copia `t162` no se modificó para comprobar. Sin red ni gasto. Sin la suite completa ni el gate (consigna de la sesión).

## Comprobación

| Comprobación | Resultado |
| --- | --- |
| `test_t169_r02.py`, `test_t169_hallazgos_t162.py` y `test_t162_respuesta_final.py` | Pasan las 63 (13 + 28 + 22) |
| `revisores/r02_01_sondas.py` y `revisores/r02_03_sondas.py` | 15 pasan. `a07` y `b01` dan XPASS(strict): H-01 de la r02 está corregido |
| `revisores/r01_01_sondas.py` de T-169 y de T-162 | Igual que en la r02: p04, p05 y p06 dan XPASS en T-169; `s02b` da XPASS y `s08` falla en T-162 (lo previsto) |
| Mutantes S01–S05 (`r02_02_mutantes.py` y `--propios`) y N09, N10, R02, R03 y R04 sobre el `_apartar` nuevo | Mueren todos. S01 lo mata `test_cierre_h02_un_error_corriente_con_el_almacen_roto_para_y_no_aparta[KeyError]` |
| ruff de `respuesta_final.py` y `test_t169_r02.py` (en `t162`) | `All checks passed!`. En la copia de `git archive` sale un I001 que también da el fichero de la base: es de la copia, que no lleva la configuración de la raíz |

## Hallazgos de la r02

| ID | Corrección comprobada | Estado |
| --- | --- | --- |
| H-01 (baja) | `_apartar` llama primero a `almacen.incidencia` y después escribe la marca `final_no_enviable`. El detalle añade «puede haberse creado el mensaje; revisar antes de reenviar», como pedía la nota `a08`. `test_cierre_h01_si_la_incidencia_del_apartado_falla_*` comprueba que, si la incidencia falla, no queda marca y la pendiente sigue en la lista; y que, al reintentar, sale una marca y una incidencia. `test_cierre_h01_contadores_rotos_*` hace lo mismo con `contadores.json` ilegible, sin simular nada. Límite declarado y aceptado: si sale la incidencia y falla la marca, el reintento repite la incidencia, pero nunca hay un apartado silencioso | corregido |
| H-02 (baja) | `test_cierre_h02_*` está parametrizado con `KeyError`, `RuntimeError` y `OSError` y rompe el sello de F2. Comprueba que el ciclo para, que no hay marca ni incidencia «apartada» y que `verificar_integridad()` da algún `False`. S01 está en `PROPIOS` y muere | corregido |
| H-03 (baja) | `docs/incidencias.md` (INC-T169-01, H-02) y `bloque_a/11_Ejecutor/README.md` (§9 bis) llevan los dos textos exactos de la r02 | corregido |

## Veredicto final

**APTO.** Se cumplen los criterios de aceptación de T-169 (CA-1 a CA-5 y los de la r02), con la evidencia de las rondas r01 y r02 y
de esta. Ya no queda ningún hallazgo abierto: los de la r01 se cerraron en la r02 y los tres bajos de la r02 están corregidos.

Pendiente para la integración en `develop`, con T-162:
- re-congelar `formas_flujos_mock.json` (los 14 fallos de goldens que ya se conocían);
- la suite completa de A y `./tools/check_all.sh` en verde (12/12);
- medir ruff contra la cuota de develop (2813).
