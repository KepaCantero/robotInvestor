# T-196 · Análisis técnico

## Causa raíz o motivo

PB-08 (Plan de pruebas V3.0) pide que, con una ráfaga de 25 CT-01 y 40 CT-03 en 10 minutos:

- ninguna petición se rechace por número;
- se sirvan por prioridad con envejecimiento;
- las consultas N0 no esperen a los análisis;
- cada petición reciba un presupuesto proporcional a su nivel.

El criterio es «100 % registradas; 100 % respondidas o con plazo comunicado; N0 con p90 < 2 minutos».

El ejecutor atendía cada CT-01 (`Bloque.peticion`) y cada CT-03 (`Bloque.consulta`, que lanzaba el análisis escalado en el momento) de forma síncrona. No había cola, ni orden por prioridad, ni plazo comunicado (INC-T159-01). La regla está en R5 y en 4.2, 7.1, 7.2 y 7.6 del Documento 0 V5.3. La fórmula de la cola está en el prompt del Coordinador V5.0, §6.1.

## Evidencia

- Antes, en `origin/develop`: `Bloque.peticion` llama a `ciclo` dentro de `procesar_una_vez`, y `Bloque.consulta` llama a `ciclo` si la ruta es ANALITICA. No existe ninguna estructura de cola persistida. `docs/evidencias_pruebas_bloque_a.md`, fila PB-08: «el ejecutor atiende cada CT-01 y cada CT-03 en el momento».
- Ahora: `tests/test_t196.py` (ver `pruebas.md`) y `.docs/scripts/evidencias_plan_a.py --pb PB-08`.

## Implementación

### Archivos cambiados y por qué

- `bloque_a/11_Ejecutor/bloque_a/cola_peticiones.py` (nuevo): `ColaPeticiones` y sus funciones auxiliares.
  - **Recepción.** `recibir` valida el CT-01, lo pasa por la mensajería con idempotencia y escribe la PET- ENCOLADA con su plazo. `plazo_consulta` y `encolar_consulta` hacen lo mismo con el escalado de una CT-03.
  - **Orden.** `prioridad` da la base, el envejecimiento y la urgencia. `orden` devuelve las ENCOLADAS en orden de servicio.
  - **Servicio.** `tomar` y `_tomar` pasan la siguiente a EN_CURSO dentro de una transacción. `atender` y `_servir` la sirven con `Bloque.ciclo` y la cierran como ATENDIDA, o como FALLIDA con incidencia, y relanzan el error. En las de CT-03 actualizan el escalado y envían la final.
  - **Funciones auxiliares.** `presupuesto_por_clase`, la regla del Anexo A que comparten la cola y `_reparto`; `objetivo_n0` (P-21); `p90`; `PeticionInvalida`.
- `bloque_a/11_Ejecutor/bloque_a/orquestacion.py`:
  - `self.cola` en `Bloque.__init__`.
  - `_reparto` usa `presupuesto_por_clase`: es la misma fórmula, movida.
  - `consulta(…, encolar_escalado=False, instante=None)`: con `True`, valida primero el instante y la prioridad de la urgencia. Una ruta ANALITICA no lanza el ciclo: toma el plazo de la cola para la provisional, anota `peticion_cola` en la QRY- y escribe la PET- después de la QRY- y de la provisional, para que la PET- siempre tenga a quién responder. La final no sale en ese momento. La ruta N0 no cambia.
- `bloque_a/11_Ejecutor/bloque_a/respuesta_final.py`:
  - `consulta_en_cola(almacen, qry)`: True si su PET- está ENCOLADA o EN_CURSO.
  - `enviar` la rechaza (`RespuestaFinalInvalida`) y `pendientes` la salta.
  - La fecha de una pendiente encolada es la `_ultima_fecha` de su QRY-, la del servicio, para que la final vea el RUN- en F5.
- `bloque_a/11_Ejecutor/bloque_a/cli.py`: `peticion --encolar`, `consulta --encolar-escalado`, `atender-cola [--maximo N]` y `--instante` en las tres. Sin `--instante`, la hora es la del sistema: es la frontera del ejecutor.
- `bloque_a/11_Ejecutor/config/por_defecto.yaml`: la sección `cola_peticiones`, `[PROPUESTO]` salvo `objetivo_respuesta_n0_s` (Anexo A, P-21).
- Pruebas y documentación:
  - `bloque_a/11_Ejecutor/tests/test_t196.py`, con 41 pruebas una vez expandidos los `parametrize`.
  - `tests/mapa_plan_pruebas.json`: PB-08 sigue PARCIAL, con 14 pruebas más y `no_comprueba` nuevo.
  - `docs/evidencias_pruebas_bloque_a.md`, regenerado.
  - `docs/incidencias.md`: INC-T196-01 y una nota en INC-T159-01.
  - `bloque_a/11_Ejecutor/README.md`: tabla de archivos y uso.
  - La fila de T-196 en la deuda técnica.

### Decisiones y desviaciones del plan

Ninguna desviación del plan. Las decisiones `[PROPUESTO]` están en INC-T196-01.

- **Números.** Los de §6.1 del prompt pasan a la configuración.
- **Envejecimiento.** Se cuenta por hora completa.
- **Urgencia.** Sin el término P80: no hay duraciones medidas.
- **Consultas escaladas.** INMEDIATA → ALTA, NORMAL → NORMAL.
- **Plazo comunicado.** Sin hora: la posición, las UC por delante y la fecha objetivo.
- **Registro.** La cola es una entrada PET- de F5, no un RUN- ENCOLADO.
- **Escalado de la final.** El de una consulta encolada lleva el RUN- que la atendió.
- **HT-08.** La cola no lo alimenta.

`atender` relanza el error del ciclo, cualquiera que sea, después de registrarlo: no lo absorbe, a diferencia de la consulta síncrona, que convierte en final FALLIDO los errores que no son de control. La captura es `except BaseException` seguida de `raise`: deja el registro y propaga, como hace `Mensajeria.procesar_una_vez`. La única captura que absorbe es `except ValueError` alrededor de `datetime.fromisoformat` en `_fecha_hora`, y se traduce en `PeticionInvalida`.

### Límites conocidos

- Una PET- EN_CURSO de un proceso que murió no se recupera sola, como una reserva interrumpida de la mensajería.
- El p90 de N0 en tiempo real con la API, en el modo sombra.
- Sin concurrencia de RUN- ni fusión de alcances.
- Las PET- de un `atender` se sirven con el mismo instante, el del servicio. Una recepción con un instante posterior que llegue a la vez desde otro proceso para la pasada (`PeticionInvalida`): falla cerrado.

### Comandos exactos para probarlo

Desde `bloque_a/11_Ejecutor`:

- `../../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_t196.py`
- `../../.venv/bin/python ../../.docs/tickets/T-196/mutantes.py .` (33 mutantes; mejor en una copia del paquete, porque modifica los fuentes mientras corre)

Desde la raíz: `.venv/bin/python .docs/scripts/evidencias_plan_a.py --pb PB-08`.

## Ronda r02 (QA r01 NO APTO)

| Hallazgo | Corrección | Prueba de regresión |
| --- | --- | --- |
| H-01 (alta) | `_en_cola(…, hasta=t)`: `orden` y `_tomar` solo ven las PET- con `recibida <= t`. `atender` acepta un reloj (un callable) y toma cada petición con un instante nuevo. La CLI le pasa uno si no se da `--instante`. El rechazo de un instante anterior queda solo en `prioridad(pet, t)` | `test_atender_no_se_corta_si_llega_una_peticion_durante_el_servicio` (con instante fijo y con reloj); `test_un_instante_anterior_a_una_recepcion_no_ordena_ni_sirve` (nueva semántica) |
| H-02 (alta) | `_plazo` cuenta solo las recibidas hasta `t` y nunca lanza por otra petición. En `recibir`, la PET- se construye y se valida (clases, presupuesto y prioridad de la configuración) antes de `mensajeria.crear` y de `procesar_una_vez`; dentro de la reserva solo quedan el id y la escritura | `test_un_ct01_con_instante_anterior_a_otra_peticion_se_encola` (A1, con el reintento del msg_id); `test_la_consulta_encolada_no_pierde_su_peticion_si_entra_otra_mientras_responde` (A3) |
| H-03 (media) | `_tomar` guarda `host` y `pid` (`interfaz_broker._proceso`). `_EN_MARCHA`, como en T-174, guarda las PET- que este proceso sirve ahora. `huerfanas()` deja una incidencia Operativa por PET- (`peticion_huerfana`), una sola vez, sin tocar el estado; la llaman `atender` y `respuesta_final.enviar_pendientes`. `reconciliar(pet_id, motivo, instante)` y la CLI `reconciliar-peticion PET-… --fallida --motivo …` pasan a FALLIDA (PROCESO_TERMINADO) solo una huérfana, y envían la final FALLIDO. La salida de `atender-cola` lleva `huerfanas` | `test_peticion_en_curso_de_un_proceso_muerto_deja_una_incidencia_y_se_reconcilia`: un subproceso toma la PET- y se mata con SIGKILL; dos pasadas dejan una sola incidencia; después, la reconciliación y la final FALLIDO |
| H-04 (baja) | `_fecha_hora`: los nanosegundos se truncan a microsegundos de forma explícita, y lo que sale se comprueba con `RE_FECHA_HORA` (ida y vuelta). Va antes de reservar (H-02) | `test_un_instante_con_nanosegundos_se_trunca_y_el_msg_id_no_queda_bloqueado` |
| H-05 (baja) | `_fecha_hora`: sin zona, se compara el desfase con `fold=0` y con `fold=1`. Si difieren, la hora es inexistente o ambigua y se rechaza con `PeticionInvalida`, sin capturar el `ValueError` de pandas | `2026-03-29T02:30` y `2026-10-25T02:30` en `test_un_instante_invalido_se_rechaza` |
| H-06 (baja) | Nuevo `servir(pet, instante)` público (solo una EN_CURSO tomada por este proceso). El docstring de `tomar` lo dice, y lo tomado y no servido es huérfano (H-03) | `test_tomar_y_servir_y_lo_tomado_sin_servir_es_huerfano` |
| H-07 (baja) | `_nueva(…, exigir_clases=True)` en `recibir`: un CT-01 sin ninguna clase activa da `PeticionInvalida` antes de crear el mensaje | `test_un_ct01_sin_clases_activas_se_rechaza_sin_escribir` |
| H-08 (baja) | Solo pruebas | `test_un_ciclo_que_falla…` con `KeyboardInterrupt` (R6) y con un RUN- ya escrito, que citan la FALLIDA y el escalado (R12); `estado_run` en la ATENDIDA del servicio real (R13) |
| H-09 (baja) | Solo pruebas | `test_un_ct01_periodico_se_encola_como_ad_hoc` (R2), `test_la_consulta_encolada_es_del_dia_de_su_instante` (R9), `test_cli_consulta_encolada_y_su_final_al_atender` (R10) |

**Además:**

- `atender` fija la fecha del bloque en el día de cada toma, y `reconciliar` en el de la reconciliación. Sin eso, lo que escriben fuera del ciclo quedaba con el día del reloj del almacén, que puede ser otro, y la final no veía el escalado.
- `reconciliar` toma el instante inyectado; sin él, la hora del sistema.

**Desviaciones:**

- H-04 trunca los nanosegundos en vez de rechazarlos. El qa.md admite las dos opciones, y A5 espera que se admita.
- H-06 añade `servir` en vez de hacer privada `tomar`, porque A6 y A7 la usan.

**A9** (una `recibida` manipulada para toda la cola) sigue fallando cerrado, como aceptó el revisor.

**R11** es equivalente, como dice el qa.md.

**Comandos**, desde `bloque_a/11_Ejecutor`:

- `../../.venv/bin/python ../../.docs/tickets/T-196/revisores/r01_ataques.py`
- `…/revisores/r01_mutantes.py .`
- `…/T-196/mutantes.py .`

Los dos scripts de mutantes, en una copia del paquete.

## Ronda r03 (QA r02 NO APTO)

| Hallazgo | Corrección | Prueba de regresión |
| --- | --- | --- |
| N-01 (media) | `_servir` es ahora un `try/finally` que envuelve todo el servicio (`_servir_en_marcha`): la PET- sale de `_EN_MARCHA` solo después de la ATENDIDA y de la final, o de la FALLIDA. Mientras está EN_CURSO, ni `huerfanas()` la marca ni `reconciliar` la acepta. El cuerpo del servicio conserva su sangría, y las anclas de los mutantes del revisor siguen valiendo | `test_una_peticion_en_servicio_no_es_huerfana_hasta_quedar_atendida`: desde `_escalado`, otro hilo ve `huerfanas() == []` y `reconciliar` se rechaza; al final, ATENDIDA, escalado COMPLETO y ninguna incidencia de huérfana (M56) |
| N-02 (baja) | `atender` guarda el instante de la toma anterior (el primero, el de la validación). Si el reloj devuelve uno menor, lanza `PeticionInvalida` («el reloj retrocede») sin tomar nada más; lo ya servido queda como está | `test_atender_con_un_reloj_que_retrocede_falla_cerrado` (M57) |
| N-03 (baja) | El docstring de cabecera de `cola_peticiones.py` dice ahora que los nanosegundos se truncan y que las horas inexistentes o ambiguas se rechazan | documental |
| N-04 (baja) | Solo pruebas, y los mutantes Q2, Q8, Q10 y Q11 pasan a `mutantes.py` como M58 a M61 | Q2: `test_una_en_curso_de_otra_maquina_no_es_huerfana`. Q8: `test_servir_una_en_curso_de_otro_proceso_se_rechaza`. Q10: `test_lo_que_escribe_atender_es_del_dia_de_la_toma`. Q11: `test_una_en_curso_de_un_proceso_vivo_no_es_huerfana`, con un subproceso vivo que la tiene tomada y que después se mata |

**B5 de `revisores/r02_ataques.py`.** El ataque da OK solo si se sirven las 3 peticiones con un reloj que retrocede (`len(s) == 3`). La corrección exacta del qa.md, y la orden del coordinador, piden lanzar `PeticionInvalida`. Con esa corrección, `atender` lanza en la segunda toma y el script lo cuenta como ERROR del caso, sin llegar a la segunda parte (el reloj con basura). Se aplica la corrección del qa.md; el comportamiento que pide queda probado en `test_atender_con_un_reloj_que_retrocede_falla_cerrado`. La segunda parte de B5 (un instante inválido a mitad de la pasada da `PeticionInvalida` con una ATENDIDA y una ENCOLADA) se cumple igual: `_instante` lo rechaza.

## Ronda de cierre de la QA r03

| Hallazgo | Corrección | Prueba de regresión |
| --- | --- | --- |
| M-01 (baja) | Sin cambio de código. La prueba del reloj que retrocede tiene un segundo caso: t0+10, t0+10, t0+12 y t0+11 minutos. Sube y baja sin pasar por debajo del primer instante | `test_atender_con_un_reloj_que_retrocede_falla_cerrado[…-2]`: `PeticionInvalida` tras la segunda servida (2 ATENDIDAS, 1 ENCOLADA). Mata P1 del revisor (sin `previo = t`), que pasa a `mutantes.py` como M62 |
