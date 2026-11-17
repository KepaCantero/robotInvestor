# T-174 · PB-61: la respuesta tardía del Broker que invalida un supuesto abre una revisión C2

| Campo | Valor |
| --- | --- |
| Estado | CERRADO (17-11-2026, QA r03 APTO tras la ronda de cierre) |
| Pieza | bloque_a (ejecutor: `interfaz_broker.py`, con una línea en `orquestacion.py` y otra en `seguimiento.py`) |
| Planifica · implementa · QA | claude · claude · un revisor nuevo sin contexto (subagente), regla del 12-11-2026 |
| Aprobación del operador | no necesaria (corrección dentro del bloque, sin cambio de contrato; regla del 13-11-2026: decide el agente por defecto) |
| Deuda técnica | T-174 en `sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md` |

## Objetivo

Cerrar el hueco de PB-61 (INC-T116-03, punto 8 del plan de la noche del 15-11-2026): hoy, cuando el Broker contesta una consulta CT-23 cuyo supuesto ya salió en un informe entregado, el ejecutor solo lo dice en el texto de la respuesta (`accion`). El Documento 0 V5.3, §7.9.5, pide que esa respuesta «se trate como petición de revisión (C2) y se comunique al Broker».

## Alcance

- Entra:
  - `ConsultasBroker.responder` abre la revisión C2: un RUN- de tipo `AD_HOC` sobre los tipos de activo afectados, con el disparador `CT-23` (CNS- y RUN- revisados) y la respuesta del Broker en la pregunta del alcance.
  - La revisión se anota en F5, en la propia CNS-.
  - El paquete de la revisión lo declara en `limitaciones` (y con ellas el informe técnico y el JSON), y el CT-02 de la revisión llega al Broker.
  - El RUN de F5 (C1/C2) y el RUN_C6 guardan qué CNS- llevaban como supuesto declarado en lo entregado (`supuestos_cns`).
- No entra:
  - juzgar con un modelo si la respuesta contradice el supuesto (ver Diseño);
  - el modo sombra y el tiempo real (plazos con reloj de pared);
  - que el modelo no invente un dato del Broker: es una propiedad del modelo real, así que queda en «No comprueba»;
  - PB-62 (lección de producto de la consulta recurrente).

## Diseño

- **Contratos.** Ninguno cambia. El CT-23 de retorno sigue con `respuestas[{indice, texto, documentos}]`, sin campos nuevos; la revisión es un `ciclo` AD_HOC como el escalado de CT-03, y su entrega es el CT-02 de siempre. Los goldens de contratos no se re-congelan: el flujo `consulta_al_broker` responde sin informe entregado y no abre revisión.
- **Estado persistido.** Hay dos claves nuevas, opcionales y solo añadidas:
  - `supuestos_cns` en el RUN y el RUN_C6 de F5;
  - `revisiones_c2` (lista) e `indices_respondidos` en las entradas CNS de F5.

  Lo anterior se lee igual: un RUN sin `supuestos_cns` no llevaba supuestos. F5 no tiene esquema versionado.
- **Cuándo se abre** `[PROPUESTO]`, en INC-T174-01:
  1. La respuesta (`RESPONDIDA` o `PARCIAL`) contesta, por `indice`, una pregunta que no se había contestado antes.
  2. La CNS- figura en `supuestos_cns` de al menos un RUN (C1/C2) con `entrega` `ENTREGADA` o un RUN_C6 entregado.

  Por qué así:
  - El ejecutor no puede juzgar si el texto del Broker contradice el supuesto, y el Anexo B no tiene una marca de confirmación. Lo prudente es dar el supuesto por invalidado: el informe se apoyó en algo que el Broker no había dicho y que ahora ha contestado.
  - Vale también para una `NO_BLOQUEANTE` contestada en plazo después de una entrega (§7.9.4: «lo revisa al llegar la respuesta»).
  - El campo `tardia` sigue significando lo mismo que hoy (contestada tras vencer).
- **Alcance de la revisión.** Los tipos declarados en la CNS-. Si no declara ninguno, los tipos analizados en los RUN- revisados más la clase de los C6. El nivel es el de un AD_HOC sin forzar (N2, como hoy).
- **Números.** Ninguno nuevo: plazos, máximos y niveles salen de `config/por_defecto.yaml` como hoy.
- **Fallo cerrado.**
  - La respuesta se registra antes de lanzar la revisión, así que la revisión ya no lleva el supuesto contestado.
  - Si la revisión falla, se anota `estado = FALLIDA` en su elemento de `revisiones_c2` con la clase del error (no el texto, R8) y una incidencia de HERRAMIENTA. Un error de control o de integridad se relanza, como en T-169 (`respuesta_final.para_la_consulta`).
  - `ejecutar_revision=False` deja la revisión `PENDIENTE` en F5, sin RUN.
  - Una segunda respuesta que no contesta nada nuevo no abre otra revisión.

## Riesgos

| Riesgo | Consecuencia | Mitigación |
| --- | --- | --- |
| Choque con T-173/T-175 en `orquestacion.py` | Conflicto al integrar | Dos líneas aisladas: el `supuestos_cns` en `_registrar_run` y la nota de revisión en `ciclo`; la lógica, en `interfaz_broker.py` |
| Revisiones de más (respuesta que confirma el supuesto) | Coste de un AD_HOC innecesario | Declarado en INC-T174-01; una marca de confirmación en el Anexo B quedaría para una entrega futura |
| Golden de flujos | Diferencias en `formas_flujos_mock.json` | El flujo capturado no tiene informe entregado; se comprueba con `goldens_ct.py` |

## Criterios de aceptación (binarios)

1. CA-1: una BLOQUEANTE vencida cuyo supuesto salió en un RUN entregado, contestada tarde, deja un RUN AD_HOC nuevo con `disparador.origen == "CT-23"`, su `cns_id` y los RUN- revisados.
2. CA-2: el paquete, el JSON y el informe técnico de la revisión ya no llevan el supuesto contestado en `supuestos_declarados`, y declaran la revisión (CNS- y RUN- revisado) en `limitaciones`. HT-09 C19 sigue en OK, y sale un CT-02 de ese RUN al Broker.
3. CA-3: la CNS- de F5 guarda la revisión en `revisiones_c2`, una lista con run, revisados, índices invalidados y estado (corregido en la r02: la r01 decía `revision_c2`). `responder` devuelve `revision_c2` y una `accion` que la nombra.
4. CA-4: sin informe entregado que llevara el supuesto (pausada y contestada antes de cualquier entrega, o RUN bloqueado), no hay revisión, y la respuesta dice por qué.
5. CA-5: una segunda respuesta sin índices nuevos no abre otra revisión.
6. CA-6: con `ejecutar_revision=False` queda `PENDIENTE` sin RUN. Si la revisión falla, queda `FALLIDA` con incidencia; un error de control se relanza.
7. CA-7: una NO_BLOQUEANTE contestada en plazo tras una entrega con su supuesto también abre la revisión; un C6 entregado con el supuesto la abre sobre la clase de la opción.
8. CA-8: PB-61 queda «Superada» en el mapa, con «No comprueba» solo para lo que depende del modelo real y del tiempo real. Las evidencias se regeneran. Suite de A ≥ 607 y en verde; ruff ≤ 2813, mypy A ≤ 109; goldens de contratos sin cambios.

## Plan de pruebas

| Prueba | Tipo | Criterio |
| --- | --- | --- |
| `test_pb61_respuesta_tardia_que_invalida_el_supuesto_abre_una_revision_c2` (ciclo pausado → vencido y entregado → respuesta tardía) | integración | CA-1, CA-2, CA-3 |
| `test_pb61_sin_informe_entregado_no_hay_revision` | límite | CA-4 |
| `test_pb61_segunda_respuesta_sin_indices_nuevos_no_reabre` | límite | CA-5 |
| `test_pb61_revision_pendiente_y_fallida` | fallo cerrado | CA-6 |
| `test_pb61_no_bloqueante_y_seguimiento_c6` | nominal | CA-7 |
| `test_consulta_bloqueante_pausa_y_vencimiento` (existente) | regresión | `accion` sigue nombrando la revisión |
| Mutantes propios (no abrir revisión, no registrar `supuestos_cns`, no anotar la nota, reabrir siempre, incluir RUN bloqueados) | mutación | todos mueren |
| Ciclo mock por CLI (`consulta-broker enviar/responder` + `semanal`) | integración | CA-1 a mano |
| Suite completa de A, `goldens_ct.py`, `evidencias_plan_a.py --ejecutar`, ruff, mypy | regresión | CA-8 |

## Scripts

`.docs/scripts/nuevo_ticket.sh`, `.docs/scripts/evidencias_plan_a.py`, `bloque_a/11_Ejecutor/tests/goldens_ct.py`.

## Registro

- 2026-11-17 · ABIERTO · creado con nuevo_ticket.sh
- 2026-11-17 · PLANIFICADO · claude · plan, criterios y pruebas escritos
- 2026-11-17 · EN CURSO · claude · implementación (interfaz_broker, dos líneas en orquestacion, una en seguimiento) y 8 pruebas
- 2026-11-17 · EN QA (r01) · claude · pruebas, mutantes (11/11 mueren), ciclo mock, evidencias regeneradas (PB-61 «Superada»), ruff 2808; commit local sin push
- 2026-11-17 · EN CURSO (r02) · claude · QA r01 NO APTO (H-01 alta; H-02 y H-03 medias; H-04 a H-06 bajas): rebase sobre origin/develop (T-165 y T-171) y corrección de los seis hallazgos
- 2026-11-17 · EN QA (r02: QA r01 NO APTO) · claude · H-01 a H-06 corregidos con sus pruebas; commit local sin push

## Ronda r02 (QA r01 NO APTO)

| Hallazgo | Corrección | Prueba de regresión |
| --- | --- | --- |
| H-01 (alta) | `responder` relee la CNS- bajo `almacen._transaccion()`, calcula lo nuevo y lo entregado y escribe en una sola entrada la respuesta, `indices_respondidos` y la revisión reservada `EN_CURSO` con su `msg_id`. El ciclo corre fuera del cerrojo y su estado final se anota por `msg_id` (`_anotar_revision`, también bajo el cerrojo) | A2; `test_r02_h01_dos_procesos_…`, `test_r02_h01_la_reserva_queda_en_curso_…` |
| H-02 (media) | Ante un error de control o de integridad, si el almacén está íntegro, la revisión queda `INTERRUMPIDA` con la clase del error, y hay una incidencia escalada antes del `raise`. `responder` relanza las `INTERRUMPIDA` y `PENDIENTE` de esa CNS-. `revisiones_pendientes()` y `relanzar_revisiones()` reclaman cada una bajo el cerrojo. Las `EN_CURSO` solo se relanzan si se pide (`estados` con EN_CURSO, o `--incluir-en-curso`): relanzarlas desde `responder` reabriría H-01 con un proceso que aún corre | A3; `test_r02_h02_…` (dos) |
| H-03 (media) | Alcance: `set(c["clases"]) & vistas`, o `vistas` si la consulta no declara tipos. Si queda vacío, `SIN_ALCANCE` con incidencia escalada y sin ciclo de todo el alcance | A7; `test_r02_h03_…` (dos) |
| H-04 (baja) | `_entregados_con(cns_id, as_of)` con `estado("F5", as_of, clave="id")` | A9; `test_r02_h04_…` |
| H-05 (baja) | En el `except`, si el RUN- de ese intento llegó a F5, el estado es el de su `entrega` y la clase del error queda en `fallo` | `test_r02_h05_…` (A8 de la r01 afirma FALLIDA: con la corrección pedida falla a propósito) |
| H-06 (baja) | Incidencias `escalado_operador=True` con `tratamiento` («relanzar la revisión C2 de CNS-… (consulta-broker relanzar --cns CNS-…)»). Órdenes nuevas `consulta-broker revisiones` y `consulta-broker relanzar [--cns] [--incluir-en-curso]` | `test_r02_h06_…` (dos) |

## Ronda r03 (QA r02 APTO, con H-07 media y H-08 baja abiertos; se corrigen aquí antes de integrar)

| Hallazgo | Corrección | Prueba de regresión |
| --- | --- | --- |
| H-07 (media) | La reserva y cada reclamación guardan `proceso: {host, pid}`. `ConsultasBroker.huerfanas()` detecta las EN_CURSO de este host cuyo pid ya no existe (`os.kill(pid, 0)`), o del pid actual que no están en el conjunto en memoria de revisiones en marcha. Se llama al empezar `Bloque.ciclo` y en `revisiones_pendientes`. Por cada huérfana se abre una sola incidencia HERRAMIENTA escalada (`tratamiento`: «consulta-broker relanzar --incluir-en-curso --cns …»), con la marca `aviso_huerfana`, y en `revisiones` lleva `huerfana: true`. Sin umbral de tiempo. De otro host, o sin `proceso`, no se puede saber y no se marca | B4; `test_r03_h07_…` (dos) |
| H-08 (baja) | `intentos` se incrementa al reclamar, bajo el cerrojo (1 en la reserva que se ejecuta, +1 en cada reclamación de `relanzar_revisiones`), y el disparador lleva ese número. Antes de lanzar una EN_CURSO o INTERRUMPIDA, `relanzar_revisiones` busca en F5 un RUN con su `msg_id`: si está ENTREGADA, la anota con su `run_id` sin otro ciclo | `test_r03_h08_…` (dos) |
| A8 de `r01_01_ataques.py` | Espera ENTREGADA (H-05), como reconoció el revisor en la QA r02 | A8 |

- 2026-11-17 · EN QA (r03: hallazgos H-07 y H-08 de la QA r02) · claude · H-07 y H-08 corregidos con sus pruebas; mutantes M22 a M28; commit local sin push
- 2026-11-17 · CERRADO · claude (revisor) · QA r03 APTO: H-07 y H-08 corregidos; M1 a M28 mueren; H-09 a H-11 (bajos) a la deuda

## Ronda de cierre de la QA r03 (bajos H-09 a H-11, subsanados en el mismo ticket)

| Hallazgo | Corrección | Prueba |
| --- | --- | --- |
| H-09 | Alta en `_EN_MARCHA` bajo el cerrojo, antes de escribir EN_CURSO, en `responder` y en la reclamación de `relanzar_revisiones`. La baja va en un `finally` que cubre desde la reserva hasta el final, también SIN_ALCANCE y un fallo de escritura. `_ejecutar_revision` ya no da de alta | C1; `test_cierre_h09_…` (dos) |
| H-10 | Clave `(carpeta resuelta del almacén, cns_id, msg_id)` | C2; `test_cierre_h10_…` |
| H-11 | `huerfana: None` («no se puede juzgar desde este host») en `revisiones` para otro host, sin `proceso` o con un pid no consultable. `[PROPUESTO]` en INC-T174-01, con la reutilización de pid y el límite de varios hosts (latido con plazo del Anexo A, que no existe), declarados allí y no en la deuda | `test_cierre_h11_…` |

- 2026-11-17 · EN QA (ronda de cierre de la QA r03) · claude · H-09 a H-11 subsanados; mutantes M29 a M33; commit local sin push
- 2026-11-17 · CERRADO · claude (revisor) · ronda de cierre de la QA r03 APTO: H-09 a H-11 corregidos; M0 a M33 con el control vivo; os._exit por la CLI correcto
