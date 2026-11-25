# T-205 · Bloque A: el seguimiento encargado rechaza una opción con una clase que no es uno de los doce tipos

| Campo | Valor |
| --- | --- |
| Estado | CERRADO (25-11-2026, QA r01 APTO y dos rondas de cierre verificadas, sin hallazgos abiertos) |
| Pieza | bloque_a (ejecutor): `bloque_a/11_Ejecutor/bloque_a/seguimiento.py` |
| Planifica · implementa · QA | claude · claude · otro agente o un revisor nuevo |
| Aprobación del operador | No hace falta (corrección de un defecto). Las decisiones del coordinador del 25-11-2026 están en «Diseño» |
| Deuda técnica | T-205 en `sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md` (origen: QA r01 de T-201, 25-11-2026) |
| Caso del plan de pruebas | Ninguno: es deuda técnica del Bloque A. El mapa del plan y las evidencias no cambian |

## Objetivo

Que el seguimiento encargado (CT-24, ciclo C6) falle cerrado con una opción de F3 cuya clase no es uno de los doce tipos de activo, o le falta. Hasta ahora `b_agente` mandaba esa opción al AG-03 sin ningún aviso. El defecto lo encontró la QA r01 de T-201 (gravedad baja, anterior a T-201, observación de INC-T201-01): `_alta` no comprobaba la clase; el C6 registraba un CT-05 con `{"XYZ": "N1"}` y presupuesto y un CT-06 de AG-02 a AG-03, y no dejaba incidencia en HA. Solo lo paraba después G3, con el informe BLOQUEADO porque el esquema rechaza `tipo_activo`. Solo se llega con un F3 manipulado o migrado.

## Fuentes

- Documento 0 V5.3, 7.11: el alta admite cualquier OPP- registrada en F3 (7.11.2); en cada ciclo, el Analizador encarga el CT-06 «al Analista del tipo de activo» (7.11.3). En 4.2, los Analistas de tipo de activo son AG-03 a AG-09 y AG-21 a AG-25, uno por clase (`contratos.AGENTE_CLASE`).
- Esquema de F3 V3.0: `tipo_activo` (alias de lectura `clase`) es un enumerado obligatorio de los doce tipos. Esquema de F11 V1.0: `clase`, obligatorio, «uno de los doce tipos de activo».
- Esquema de HA V2.0, 4.8: `INC-` con `tipo` (SEGURIDAD · MANIPULACION · CANAL_NO_PREVISTO · ACCESO_FUERA_DE_MATRIZ · HERRAMIENTA · ESCRITURA · OTRO), `severidad`, `objeto`, `campo_afectado` (sin el valor), `tratamiento` y `escalado_operador`.
- Prompt del Analizador V5.0, paso 9, y del Coordinador V5.0, 5.12: ninguno dice qué hacer con una clase fuera de los doce. R5 dice «nada se descarta en silencio».

## Alcance

- **Entra:**
  - `b_agente`: con una clase desconocida, vacía, None u otro tipo, lanza `ClaseNoAdmitida`, un `ValueError`. Antes devolvía el AG-03.
  - **Alta (CT-24 ALTA).** Si la OPP- está en F3 y su clase no se admite, el alta se rechaza antes de escribir nada: ni el CT-24 de entrada, ni identificadores SEG-, MSG- o F5SEG, ni F11, ni la anotación de F3, ni F5. Lo único que se escribe es un INC- en HA. Se comprueba en `procesar`, antes de registrar el CT-24, y otra vez en `_alta`.
  - **C6.** La opción se salta antes de escribir nada: ni RUN-, ni CT-05, ni CT-06, ni CT-24, ni G3V, ni informe, ni F5, y F11 no avanza. Queda un INC- en HA, uno solo mientras no cambien la entrada de F3 que fija la clase ni el número de ciclos hechos del encargo. El resto de encargos del ciclo sigue igual.
- **No entra:**
  - Leer `tipo_activo` como respaldo cuando falta `clase`: el C6 y el informe leen `clase`, como antes.
  - Corregir que `DATOS` no esté en el enumerado de HA: es otro defecto y lo lleva el coordinador a otro ticket.
  - Cambiar esquemas o el corpus.
  - Modificar, pausar o cancelar un encargo con clase mala: no encargan nada a ningún Analista.

## Diseño

- **Contratos y esquemas:** ninguno cambia. El INC- lleva los campos del esquema de HA (`tipo` OTRO, `severidad`, `objeto`, `campo_afectado` «clase», `tratamiento`, `escalado_operador`) y, como el resto de INC- del ejecutor, campos de trazabilidad: `fase` (ALTA o C6), `opp_id` y, en el C6, `seg_id`, `f3_seq_clase` y `ciclos_encargo`. No lleva el valor de la clase, ni en el detalle.
- **Estado persistido:** solo HA, que es append-only. F11, F3, F5, F6, F10 y los contadores no cambian en el rechazo (salvo el contador de INC-).
- **Números:** ninguno nuevo. La «clase admitida» es una de las doce claves de `AGENTE_CLASE`.
- **Decisiones del coordinador del 25-11-2026 (opción b: esperar a que T-201 llegue a develop):**
  1. `b_agente` falla de forma explícita con una clase desconocida, None o vacía. Manda T-205: T-201 solo conservó el comportamiento anterior, porque un ticket de cuotas no cambia comportamientos, y lo dejó anotado en INC-T201-01 como algo que se debía corregir aparte.
  2. Tipo de la incidencia: `OTRO`, con `campo_afectado: "clase"` y sin el valor (INC-T205-01 [PROPUESTO]).
  3. En el C6, F11 no avanza, y hay una sola incidencia por opción y valor de clase mientras siga igual.
- **«Mientras siga igual», sin copiar el valor:** el INC- no puede llevar el valor, así que la deduplicación usa la clave (`seg_id`, `f3_seq_clase`, `ciclos_encargo`). `f3_seq_clase` es el `_seq` de la última entrada de F3 de la opción que fija `clase`, o None si no hay ninguna.
  - Otra escritura de la clase en F3, aunque sea con el mismo valor, abre otra incidencia.
  - Una escritura de F3 que no toca la clase no la abre.
  - Un ciclo C6 hecho entre medias (la clase se corrigió y luego se volvió a estropear) también abre otra.
  - La lectura de HA y la escritura del INC- van en la misma `almacen._transaccion()`, que excluye también entre procesos.
- **La clase del C6 es la de F3:** antes el C6 usaba `opp.get("clase") or enc.get("clase")` y el informe solo `opp.get("clase")`. Ahora los dos usan la de F3, que es su propietario. La copia de F11 ya no la suple: un encargo cuya OPP- falta en F3 se salta con su INC-. Antes salían un CT-05 y un CT-06 y un informe BLOQUEADO.
- **Cómo falla cerrado:** se comprueba primero y se escribe después. Si falla la escritura del INC-, la excepción sube y el estado queda como estaba (lo comprueba una prueba). La excepción del alta (`ClaseNoAdmitida`) es un `ValueError`, como la de una frecuencia no admitida, así que quien ya captura `ValueError` sigue funcionando. El C6 no lanza excepción: devuelve `{"ejecutado": False, "motivo", "inc_id", "incidencia_nueva"}` y `ejecutar` sigue con los demás.
- **Orden en el C6:** la clase se comprueba antes que la absorción en C1 (una opción VIGENTE). Una opción con la clase estropeada no se omite «cubierta en C1», porque C1 tampoco la cubre bien. Se deja su INC- y F11 tampoco avanza.

## Riesgos

| Riesgo | Consecuencia | Mitigación |
| --- | --- | --- |
| Romper la prueba de T-201 que fijaba el AG-03 por defecto | Regresión aparente | La prueba se actualiza a la decisión 1, con los mismos seis casos |
| Una incidencia cada día con el encargo vencido | HA se llena | Deduplicación por (`seg_id`, `f3_seq_clase`, `ciclos_encargo`) en una transacción |
| Dos procesos omiten a la vez el mismo C6 | Dos INC- | Lectura y escritura en `almacen._transaccion()`. La prueba usa 6 procesos reales y 5 rondas |
| Un F3 migrado que solo lleva `tipo_activo` | Su alta se rechaza | Documentado en INC-T205-01 como límite. Antes el informe salía BLOQUEADO igual |

## Criterios de aceptación (binarios)

1. CA-1: `b_agente` da el Analista de cada uno de los doce tipos y lanza `ClaseNoAdmitida` (un `ValueError`) con «XYZ», `""`, None, otra grafía (`"rv"`, `" RV"`) u otro tipo.
2. CA-2: el alta de una OPP- de F3 con clase «XYZ», vacía, None o sin la clave se rechaza con `ClaseNoAdmitida`. Solo cambian HA (un INC- OTRO, «clase», sin el valor, fase ALTA, escalado) y el contador de INC-. No se registra ningún mensaje ni encargo. Con una clase buena, el alta es la de siempre. Una OPP- que no está en F3 sigue dando `KeyError`, sin INC-. `_alta`, llamada directamente, también comprueba la clase.
3. CA-3: en el C6, la opción con clase «XYZ», vacía o None, o con la OPP- fuera de F3, se salta con su INC- (OTRO, «clase», fase C6, sin el valor). No salen CT-05, CT-06 ni CT-24 para ella, no hay RUN- ni F5 ni G3V, y F11 no cambia. Los otros encargos del mismo ciclo dan exactamente lo mismo que en un gemelo sin la opción estropeada: resultados, informes, mensajes y F11. También con `forzar`.
4. CA-4: un solo INC- mientras no cambien la entrada de F3 que fija la clase ni los ciclos hechos. Otra entrada con otra clase no admitida abre otro. Una entrada de F3 que no toca la clase no lo abre. Tras corregirla, el ciclo se hace y F11 avanza; si se vuelve a estropear, es otro INC-. Un INC- de otra fase con la misma clave no cuenta. Seis procesos a la vez dejan un solo INC-.
5. CA-5: si falla la escritura del INC-, no cambia ningún fichero del estado y no sale ningún mensaje.
6. CA-6: el defecto de la QA r01 de T-201 ya no se reproduce (ni el CT-06 al AG-03 ni el CT-05 con `{"XYZ": "N1"}`). Las pruebas nuevas fallan sin el cambio. La suite de A queda en ≥ 607 y sin fallos, las cuotas no suben (ruff ≤ 2797, mypy de A ≤ 67), el ciclo mock y el backtest del README dan lo mismo que en develop y `./tools/check_all.sh` sale en verde (12/12).

## Plan de pruebas

| Prueba (`tests/test_t205_clase_seguimiento.py`) | Tipo | Criterio |
| --- | --- | --- |
| `test_b_agente_falla_…` (7 casos), `test_b_agente_da_el_analista_…` | nominal, límite | CA-1 |
| `test_alta_con_clase_no_admitida_…` (desconocida, vacía, None, ausente) | fallo cerrado | CA-2 |
| `test_alta_con_clase_buena_…`, `test_alta_de_una_opp_que_no_esta_en_f3_…`, `test_alta_directa_…` | regresión, límite | CA-2 |
| `test_c6_salta_la_opcion_…` (desconocida, vacía, None; con gemelo), `test_c6_de_un_encargo_cuya_opp_no_esta_en_f3_…`, `test_c6_forzado_…`, `test_c6_una_opcion_vigente_con_clase_no_admitida_…` | fallo cerrado, regresión | CA-3 |
| `test_c6_una_sola_incidencia_…`, `test_c6_un_inc_de_otra_fase_…`, `test_c6_la_lectura_de_ha_y_el_inc_…`, `test_c6_varios_procesos_…` | límite, concurrencia | CA-4 |
| `test_c6_un_fallo_al_escribir_la_incidencia_…`, `test_alta_con_ha_rota_…` | fallo cerrado | CA-5 |
| `test_el_defecto_de_la_qa_r01_de_t201_…`; `test_t201_cuotas.py::test_b_agente_…` actualizada; suites de seguimiento existentes | regresión | CA-6 |
| Mutantes propios (`mutantes.py`) | robustez de las pruebas | todos |
| Suite de A, gate completo, ciclo mock y backtest | regresión | CA-6 |

## Scripts

`.docs/tickets/T-205/mutantes.py` (nuevo). `.docs/tickets/T-201/revisores/r06_b_agente.py` sirve para reproducir el defecto: con el cambio, las dos altas malas se rechazan con su INC-.

## Registro

- 2026-11-25 · ABIERTO · creado con nuevo_ticket.sh
- 2026-11-25 · PLANIFICADO · claude · `seguimiento.py` lo tocaba `wip/t201`: se espera a que T-201 llegue a develop (decisión b del coordinador), con las decisiones 1 a 3
- 2026-11-25 · EN CURSO · claude · copia rehecha desde `origin/develop` 358576c3 (con T-201); implementación en `seguimiento.py`
- 2026-11-25 · EN QA (r01) · claude · 25 pruebas nuevas, mutantes, suite de A, ciclo mock y gate completo (detalle en `pruebas.md`); commit local
- 2026-11-25 · EN QA (ronda de cierre de la QA r01) · claude · QA r01 APTO pendiente de cierre con H-01 a H-03 bajos: tres pruebas nuevas (VIGENTE con clase mala, alta con HA rota y la transacción de la deduplicación, determinista, que mata Q11), Q1, Q2 y Q11 en `mutantes.py` (25 de 25 muertos), la prueba de `b_agente` de T-201 renombrada e INC-T201-01 anotada; commit local «T-205 cierre»
- 2026-11-25 · ronda de cierre verificada (H-04 incluido) · APTO sin nada abierto (`qa.md`).
- 2026-11-25 · CERRADO · claude: integrado en `develop` con `commit_limpio.sh`.
