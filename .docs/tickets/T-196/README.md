# T-196 · Bloque A: PB-08, ráfaga de peticiones sin límite (cola del Coordinador con prioridad y envejecimiento, presupuesto por nivel)

| Campo | Valor |
| --- | --- |
| Estado | CERRADO (24-11-2026, QA r03 APTO y ronda de cierre verificada, sin hallazgos abiertos) |
| Pieza | bloque_a (ejecutor): `bloque_a/11_Ejecutor/bloque_a/cola_peticiones.py` (nuevo), `orquestacion.py` (consulta con escalado en cola), `respuesta_final.py` (una final no sale mientras su análisis está en cola), `cli.py`, `config/por_defecto.yaml` |
| Planifica · implementa · QA | claude · claude · otro agente o un revisor nuevo |
| Aprobación del operador | No necesaria: el agente decide por defecto (`compartida/2026-11-13_decide-el-agente-por-defecto`); decisiones en INC-T196-01 |
| Deuda técnica | T-196 en `sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md` |

## Objetivo

Cerrar el hueco de PB-08 que señala INC-T159-01: hoy el ejecutor atiende cada CT-01 y cada CT-03 en el momento. Falta lo que pide R5: ninguna petición se rechaza por número, todas se encolan por prioridad con envejecimiento y cada una recibe un nivel N0–N3 y un presupuesto proporcional. Las consultas N0 van por el carril rápido y no esperan a los análisis (7.1, 7.2 y 7.6 del Documento 0 V5.3; Anexo A).

## Fuentes

- Plan de pruebas V3.0, PB-08. Pasos: «El Broker envía 25 CT-01 (5 ALTA, 15 NORMAL, 5 BAJA) y 40 CT-03 en 10 minutos». Resultado esperado: «Las 65 peticiones registradas; ninguna RECHAZADA por número; orden de servicio por prioridad con envejecimiento; consultas N0 atendidas sin esperar a los análisis; presupuesto proporcional por nivel». Criterio: «100 % registradas; 100 % respondidas o con plazo comunicado; N0 con p90 < 2 minutos».
- Documento 0 V5.3:
  - **R5**: «ninguno se rechaza por número. Cada petición o consulta recibe un nivel (N0–N3) y un presupuesto proporcional […]; todo se encola por prioridad y nunca se descarta en silencio».
  - **4.2, AG-01**: el Coordinador de Peticiones y Consultas «clasifica y encola peticiones ad hoc, asigna nivel N0–N3 y presupuesto, responde consultas N0».
  - **7.1**: C2 es un CT-01 «sin límite de número» y C3 lo atiende el Coordinador (N0) o el Analizador.
  - **7.2**: niveles N0–N3 con presupuesto relativo 0,05 · 0,3 · 1 · 2,5.
  - **7.6.2–7.6.3**: ruta rápida N0 «inmediato»; la ruta analítica informa al Broker «del nivel, del plazo estimado» con una respuesta provisional.
  - **10.3**: presupuesto en UC por petición.
  - **Anexo A**: presupuesto de referencia N0 1 · N1 5 por tipo · N2 18 por tipo · N3 50 por petición (P-17, `presupuesto_uc`); objetivo de respuesta N0 < 2 minutos (P-21).
- Prompt del Coordinador V5.0. §6.1, «Cola de prioridades»: dos carriles (el rápido para N0 y el de órdenes); prioridad efectiva = base + envejecimiento + urgencia, con base ALTA 30 · NORMAL 20 · BAJA 10, envejecimiento de +1 por hora hasta +15 y urgencia de +20 / +10; desempate por menor nivel y después por orden de llegada. §6.3: UC por nivel. Los números del prompt no están en el Anexo A: pasan a la configuración como `[PROPUESTO]`.
- Esquema de F5 V2.0: regla 2, «Toda petición se registra, también las encoladas»; RUN- con el ciclo de estados `ENCOLADO → EN_CURSO → …`.
- Anexo B, CT-01 (`prioridad`, `nivel_forzado`, `fecha_objetivo` «AAAA-MM-DDThh:mm») y CT-03 (`urgencia` INMEDIATA | NORMAL; `escalado` con `run_id`, `plazo_estimado`, `nivel`, `clases` y `respuesta_provisional`). Respuesta final de V5.3 y su `ESQUEMA` en `respuesta_final.py`.
- Modelo: la cola de instancia única de T-178 (`ht08_monitor.clave_prioridad`, `carga.py`): validar todo antes de tocar nada, lista cerrada de prioridades y escrituras bajo `almacen._transaccion()`.

## Alcance

- **Entra:**
  - `cola_peticiones.py` (nuevo), la cola del Coordinador, persistida en F5. Cada petición es una entrada `PETICION` (`PET-`), escrita por AG-01. Estados `ENCOLADA → EN_CURSO → ATENDIDA | FALLIDA`.
    - `recibir(ct01, instante)`: valida el CT-01, lo pasa por la mensajería con idempotencia (`procesar_una_vez`), asigna el nivel y el presupuesto, registra la PET- y devuelve el acuse con el nivel, el presupuesto, la posición y el plazo comunicado. Sin ningún límite de número.
    - `encolar_consulta(…)`: el escalado de una CT-03 de ruta ANALITICA, también como PET- (`origen` CT-03, con su QRY-).
    - `prioridad(pet, instante)`: base + envejecimiento + urgencia, con sus componentes.
    - `orden(instante)`: las PET- ENCOLADAS en orden de servicio.
    - `atender(instante, maximo)`: las sirve en ese orden con `Bloque.ciclo`. En las de CT-03 actualiza el escalado y envía la respuesta final.
    - `presupuesto_por_clase(cfg, tipo, clases, nivel)`: la regla del Anexo A, compartida con `Bloque._reparto` para que la cola y el ciclo den lo mismo.
    - `objetivo_n0(cfg)` y `p90(tiempos)`: el criterio N0 de PB-08 (P-21).
  - `Bloque.consulta(…, encolar_escalado=False)`: con True, una consulta de ruta ANALITICA no lanza el análisis en el momento. Lo encola, y la provisional lleva el plazo de la cola. Las N0 se responden igual que hoy: carril rápido, sin cola.
  - `respuesta_final`: la final de una consulta cuyo análisis sigue en cola no sale. No la envían ni `enviar_pendientes` ni `enviar`: falla cerrado con `RespuestaFinalInvalida`. Sale al atenderse la petición.
  - CLI: `peticion --encolar`, `consulta --encolar-escalado` y `atender-cola [--maximo N]`, con `--instante` opcional.
  - Configuración: la sección `cola_peticiones` (bases, envejecimiento, urgencia, prioridad de las consultas escaladas y objetivo N0), `[PROPUESTO]` salvo P-21.
- **No entra:**
  - El término de urgencia «+20 si el margen es menor que la duración estimada P80»: el ejecutor no mide duraciones, y queda declarado.
  - La concurrencia de 3 RUN- simultáneos y la fusión de peticiones con el mismo alcance (6.1 del prompt): el ejecutor atiende en serie.
  - Alimentar HT-08 con esta cola: su contador es en memoria y por llamada, y su CAR- reordena con la clave de T-178, sin envejecimiento.
  - El p90 de N0 en tiempo real con la API (modo sombra).
  - Cambiar `Bloque.peticion` o la consulta por defecto: siguen atendiendo en el momento, como hoy.
  - Los ciclos C1 (HT-05) y C6 (`seguimiento.py`), que no pasan por esta cola.
  - Recuperar una PET- EN_CURSO de un proceso muerto.

## Diseño

- **Contratos y esquemas:** ninguno cambia.
  - El acuse de CT-01 no es un mensaje de la mensajería (`Mensajeria.acuse`) y gana `cola`.
  - La provisional de CT-03 en cola lleva el `escalado` del Anexo B con `run_id` nulo, como `--sin-escalado`.
  - La final de una consulta en cola lleva en `escalado` el `run_id` y el `estado_run` del RUN- que la atendió; los dos están en el `ESQUEMA` de la final (`jsonschema`).
  - F5 gana la entrada `PETICION`. F5 ya tiene entradas propias del ejecutor: `RUN_C6`, `AVISO_CT22`, `PRESUPUESTO_F9`.
- **Estado persistido:** F5, append-only. Una PET- es una entrada por cambio de estado con el mismo `id`, y `almacen.estado("F5")` la consolida. El RUN- servido lleva `pet_id` en su `disparador`.
- **Números y su origen:**
  - Del Anexo A: el presupuesto, de `presupuesto_uc` (P-17), y el objetivo N0, `cola_peticiones.objetivo_respuesta_n0_s: 120` (P-21, «< 2 minutos»).
  - Del prompt del Coordinador V5.0, §6.1: las bases (30 / 20 / 10), el envejecimiento (+1 por hora, hasta +15) y la urgencia (+10 si el margen es menor de 2 h). Van a la configuración como `[PROPUESTO]` (INC-T196-01).
  - La prioridad de una consulta escalada: INMEDIATA → ALTA, NORMAL → NORMAL, `[PROPUESTO]`.
- **Cómo falla cerrado:**
  - Al recibir, antes de escribir nada: una prioridad fuera de ALTA | NORMAL | BAJA, un `nivel_forzado` fuera de N1–N3, una `fecha_objetivo` que no es una fecha-hora, un instante sin fecha-hora o un CT-01 que la mensajería rechaza se rechazan con `PeticionInvalida`, y F5 queda igual.
  - Un instante de servicio anterior a la recepción de una petición en cola también se rechaza.
  - La toma de una petición, que la pasa a EN_CURSO, va en una transacción: dos procesos no toman la misma.
  - Si el ciclo falla, la PET- queda FALLIDA con la clase del error y una incidencia HERRAMIENTA. Si es de CT-03, el escalado queda FALLIDO y la final FALLIDO sale con `enviar_pendientes`. El error se relanza y nada se absorbe. Las demás peticiones siguen ENCOLADAS.
  - Una final en cola no sale.
- **Decisiones `[PROPUESTO]` (INC-T196-01):**
  - Los números del prompt.
  - El envejecimiento por hora completa.
  - La urgencia sin P80.
  - La prioridad de las consultas escaladas.
  - El plazo comunicado: posición, UC por delante y fecha objetivo, sin hora estimada, porque no hay duraciones medidas.
  - El `escalado` de la final con el RUN- que la atendió.
  - HT-08 sin alimentar.
  - La cola como entrada PET- de F5, en vez de un RUN- ENCOLADO: un RUN- sin ejecutar rompería a los lectores de «el último RUN-».

## Riesgos

| Riesgo | Consecuencia | Mitigación |
| --- | --- | --- |
| Cambiar la ruta por defecto de `peticion` o `consulta` | Regresión en los goldens, el backtest y el ciclo mock | La cola solo actúa con `recibir`, `encolar_escalado=True` o la CLI nueva; ciclo mock y backtest comparados con develop |
| Un RUN- ENCOLADO en F5 | Lectores de «el último RUN-» rotos | Entrada PET- propia; el RUN- solo existe al servirse |
| `enviar_pendientes` manda una final NO_EJECUTADO de una consulta en cola | El Broker recibe un «no se lanzó» falso | `pendientes` y `enviar` la saltan mientras su PET- no se ha atendido |
| Tomar una PET- sin cerrojo | Dos procesos la sirven dos veces | Toma bajo `almacen._transaccion()`; prueba con hilos |
| `_reparto` cambia al compartir la regla | Presupuestos del ciclo distintos | Misma fórmula movida, sin cambiar números; suite y ciclo mock |

## Criterios de aceptación (binarios)

1. CA-1 · **Registradas.** Cada CT-01 recibido queda en F5 como PET- ENCOLADA, con prioridad, nivel, presupuesto, recepción y `msg_id`. Cada CT-03 queda como QRY-, y su escalado en cola, como PET- con la QRY-. En la ráfaga del plan (25 CT-01, 5 ALTA, 15 NORMAL y 5 BAJA, y 40 CT-03 en 10 minutos) están las 65.
2. CA-2 · **Ninguna rechazada por número.** No hay límite de cola: con 200 CT-01 en cola, el último se encola igual. Ninguna PET- queda RECHAZADA, y un CT-01 repetido (el mismo `msg_id`) no duplica su PET-.
3. CA-3 · **Respondidas o con plazo comunicado.**
   - Cada CT-01 recibe su acuse con la PET-, el nivel, el presupuesto, la posición y el plazo.
   - Cada CT-03 N0 recibe su respuesta.
   - Cada CT-03 analítica recibe su provisional, con el plazo de la cola y `run_id` nulo, y al atenderse, una sola final, con el RUN-.
4. CA-4 · **Orden por prioridad con envejecimiento.**
   - Prioridad efectiva = base de la prioridad + min(horas completas de espera × puntos, máximo) + urgencia; todo sale de `cola_peticiones`.
   - Se sirve de mayor a menor; a igualdad, menor nivel y después orden de llegada.
   - Una BAJA que ha esperado alcanza a una NORMAL recién llegada (sin inanición).
   - Una petición con la fecha objetivo a menos del margen sube su prioridad.
   - El envejecimiento no pasa del máximo.
5. CA-5 · **N0 sin esperar a los análisis.** En la ráfaga, cada consulta N0 se responde al recibirse, con 25 o más peticiones en cola, sin lanzar ningún análisis (cero RUN- en F5 hasta atender la cola). El p90 de su tiempo de proceso, con el cliente simulado, queda por debajo de `cola_peticiones.objetivo_respuesta_n0_s` (P-21).
6. CA-6 · **Presupuesto proporcional por nivel.** El presupuesto de cada PET- es el del Anexo A según su nivel (`presupuesto_uc`: N1 5 y N2 18 por tipo, N3 50 por petición) y coincide con el de `Bloque._reparto`. El RUN- servido tiene ese nivel por tipo de activo.
7. CA-7 · **Servicio.**
   - `atender` sirve en el orden de CA-4: ENCOLADA → EN_CURSO → ATENDIDA, con `run_id`, y el RUN- lleva `pet_id`.
   - Si el ciclo falla: FALLIDA, incidencia HERRAMIENTA, final FALLIDO en una consulta y el error relanzado; las demás siguen ENCOLADAS.
   - Dos tomas concurrentes nunca toman la misma PET-.
8. CA-8 · **Falla cerrado.** Al recibir se rechazan con `PeticionInvalida`, sin escribir nada en F5:
   - una prioridad o un tipo inválidos;
   - un `nivel_forzado` fuera de N1–N3;
   - una `fecha_objetivo` mal formada;
   - un instante inválido.
   Al ordenar o atender, un instante anterior a una recepción también se rechaza. La final de una consulta en cola no sale por `enviar` ni por `enviar_pendientes`.
9. CA-9 · **Regresión.**
   - La suite de A no baja de 607 ni falla.
   - Ruff no pasa de 2807 y mypy de A no pasa de 102.
   - El ciclo mock y el backtest del README dan lo mismo que en develop.
   - `peticion` y `consulta` por defecto no cambian.
   - PB-08 queda en el mapa como PARCIAL, con `no_comprueba` = el p90 en tiempo real con la API, y las evidencias se regeneran.

## Plan de pruebas

| Prueba (`tests/test_t196.py`) | Tipo | Criterio |
| --- | --- | --- |
| Ráfaga del plan: 25 CT-01 y 40 CT-03 en 10 minutos con instantes inyectados, servicio con el ciclo sustituido por un registrador | integración | CA-1, CA-3, CA-4, CA-5 |
| 200 CT-01 sin rechazo; `msg_id` repetido | límite | CA-2 |
| Prioridad efectiva: componentes, máximo del envejecimiento, BAJA que alcanza a la NORMAL, urgencia, desempate por nivel y llegada | nominal, límite | CA-4 |
| Presupuesto por nivel frente a `_reparto` | nominal | CA-6 |
| Dos peticiones reales servidas con el ciclo mock (CT-01 y CT-03) y su final | integración | CA-3, CA-6, CA-7 |
| Ciclo que falla: FALLIDA, incidencia, final FALLIDO y el resto ENCOLADO | fallo cerrado | CA-7 |
| Tomas concurrentes con hilos | concurrencia | CA-7 |
| Entradas inválidas sin escribir; instante anterior; final en cola | fallo cerrado | CA-8 |
| CLI `peticion --encolar`, `atender-cola` | integración | CA-1, CA-7 |
| Las pruebas de PB-07, PB-08, T-162 y T-169 y la suite completa | regresión | CA-9 |
| Mutantes propios (`mutantes.py`) | robustez de las pruebas | todos |

## Scripts

`.docs/scripts/evidencias_plan_a.py --pb PB-08` y `--ejecutar`; `.docs/tickets/T-196/mutantes.py` (nuevo).

## Registro

- 2026-11-24 · ABIERTO · creado con nuevo_ticket.sh
- 2026-11-24 · PLANIFICADO · claude · plan con R5, 4.2, 7.1, 7.2, 7.6, 10.3 y el Anexo A del Documento 0 V5.3, el §6.1 y el §6.3 del prompt del Coordinador y el esquema de F5
- 2026-11-24 · EN CURSO · claude · implementación (`cola_peticiones.py`, `consulta` con escalado en cola, `respuesta_final`, CLI, configuración)
- 2026-11-24 · EN QA (r01) · claude · 41 pruebas en `tests/test_t196.py`, 33 mutantes muertos, mapa y evidencias regenerados (PB-08 «en parte» solo por el p90 en tiempo real), ciclo mock y backtest iguales a develop; commit local
- 2026-11-24 · EN CURSO (r02) · claude · QA r01 NO APTO (H-01 y H-02 altos, H-03 medio, H-04 a H-09 bajos): los nueve corregidos con su prueba de regresión
- 2026-11-24 · EN QA (r02: QA r01 NO APTO) · claude · ataques del revisor 10/10; mutantes propios y del revisor muertos (R11 equivalente); gate completo; commit local
- 2026-11-24 · EN CURSO (r03) · claude · QA r02 NO APTO (N-01 medio; N-02 a N-04 bajos): los cuatro corregidos con su prueba
- 2026-11-24 · EN QA (r03: QA r02 NO APTO) · claude · scripts del revisor, mutantes y gate completo; commit local
- 2026-11-24 · EN QA (ronda de cierre de la QA r03) · claude · QA r03 APTO salvo M-01 (bajo): segundo caso en la prueba del reloj que retrocede y mutante P1 como M62; sin cambio de código; commit local
- 2026-11-24 · ronda de cierre verificada · APTO sin nada abierto (`qa.md`).
- 2026-11-24 · CERRADO · claude: integrado en `develop` con `commit_limpio.sh`.
