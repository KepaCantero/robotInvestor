# T-178 · Bloque A: PB-19, agente de instancia única saturado (reordenación, aviso de plazos y tipo 3)

| Campo | Valor |
| --- | --- |
| Estado | CERRADO (17-11-2026, QA r02 APTO) |
| Pieza | bloque_a (ejecutor): `bloque_a/11_Ejecutor/bloque_a/herramientas/ht08_monitor.py`, `bloque_a/carga.py` (nuevo), una llamada en `orquestacion.py` |
| Planifica · implementa · QA | claude · claude · otro agente o un revisor nuevo |
| Aprobación del operador | 2026-11-15: plan de la noche para terminar el Bloque A (`.docs/tickets/_relevo/plan_noche_bloque_a_2026-11-15.md`, punto 14); sin decisión nueva |
| Deuda técnica | T-178 en `sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md` |

## Objetivo

Cerrar el hueco de INC-T116-03 que deja PB-19 «Superada en parte»: con un agente de instancia única saturado, el Orquestador (modo CARGA, HT-08) no abre instancias (ya lo hace) y además reordena su cola por prioridad, avisa al Coordinador si afecta a plazos de entrega (vía HA) y eleva al operador una propuesta de tipo 3 si se repite (prompt del Orquestador V5.0, 5.3 punto 5; Documento 0 V5.3, 4.5 y R25).

## Fuentes

- Plan de pruebas V3.0, PB-19: «Ninguna instancia nueva de AG-02; reordenación por prioridad; aviso al Coordinador sobre plazos (vía HA); propuesta de tipo 3 si se repite». Criterio: «Cero ORD- para AG-02; registro CAR- de la saturación».
- Documento 0 V5.3: 4.5 (instancia única con cola: AG-01, AG-02, AG-18, AG-19, AG-20), R25, R5 (todo se encola por prioridad), 6 (C4 y C5 en segundo plano, nunca bloquean C1–C3; C6 con prioridad inferior a C1–C3), R17 (auditoría asíncrona, nunca bloquea), Anexo A (umbral de escalado: cola > 3, `paralelismo.umbral_cola`), 18.1 (tipo 3).
- Esquema de HA V2.0: 4.5 (`CAR-`: `cola`, `W_medio`, `W_p90`, `rho`, `instancias`, `encargos_completados`) y 4.8 (`P3-`: `origen`, `objeto`, `evidencia`, `impacto`, `pruebas_regresion`, `plan_reversion`, `npr`, `estado` PENDING_OPERATOR…).
- CT-01: `prioridad` ALTA | NORMAL | BAJA (lista cerrada que ya comprueba la mensajería).

## Alcance

- **Entra:**
  - `Monitor.encolar(agente, n, ordenes=None)`: además del contador, la cola de un agente puede llevar sus órdenes (`ref`, `prioridad`, `tipo`, `fecha_objetivo`). Una prioridad fuera de ALTA | NORMAL | BAJA se rechaza (falla cerrado); sin prioridad, NORMAL (el valor por defecto de `ciclo`). `Monitor.retirar(agente, ref)` saca una orden atendida.
  - Reordenación por prioridad: con el agente de instancia única saturado (cola > `paralelismo.umbral_cola`), su cola se ordena de forma estable: primero las de C1–C3 y después las de seguimiento C6 (`tipo` SEGUIMIENTO); dentro, ALTA, NORMAL, BAJA; después la `fecha_objetivo` más temprana (sin fecha, al final) y por último el orden de llegada. La cola queda reordenada en el monitor y el CAR- la lleva (`cola_reordenada`).
  - CAR- con los campos del esquema que el monitor mide de forma determinista (`cola`, `instancias`, `encargos_completados`) y `saturado`, `umbral_cola`, `reordenada`, `afecta_plazos`.
  - Aviso al Coordinador: si el agente está en el camino de la entrega (AG-01, AG-02, AG-18), el CAR- lleva `aviso_coordinador` (`destinatario` AG-01, órdenes en espera con su `fecha_objetivo`, `en_espera_sobre_umbral`) y `carga.avisos_plazos(almacen, run_id)` es la lectura del Coordinador. AG-19 (asíncrono, R17) y AG-20 (C4 y C5 en segundo plano) no retrasan entregas: su CAR- dice `afecta_plazos: false` y no avisa.
  - Propuesta de tipo 3 si se repite: un CAR- de saturación del mismo agente en otro run (distinto `run_id`) desde la última propuesta decidida → P3- en HA (`origen` ORQ, `estado` PENDING_OPERATOR, evidencia con los CAR-, batería de regresión), una sola: si ya hay una P3- abierta (PENDING_OPERATOR o APROBADA sin aplicar) para la saturación de ese agente, el CAR- la cita (`p3_id`) y no se duplica.
  - `orquestacion.py`: la escritura de las entradas del monitor en HA pasa a `carga.registrar_carga` (una sola línea cambiada).
- **No entra:** el disparo por tiempo (> 2× objetivo), ρ, λ, μ, W_p90 y el cierre con histéresis (PB-18, INC-T159-01); cambiar los esquemas; que el Coordinador renegocie plazos con el Broker (el prompt solo pide informarle); encolar en el monitor los CT-05 del ciclo real (el ejecutor atiende los ciclos uno detrás de otro, sin cola real de CT-05: ver riesgos).

## Diseño

- **Contratos y esquemas:** ninguno cambia. HA es un esquema en Markdown; CAR- y P3- ganan campos que el esquema no prohíbe (las entradas actuales ya llevan `nota`, `run_id`).
- **Estado persistido:** HA, append-only como siempre; P3- nuevas con origen ORQ y prefijo `P3-ORQ` (el mismo que las de `guias.py`).
- **Números:** ninguno nuevo. El umbral de saturación es `paralelismo.umbral_cola` (Anexo A, «cola > 3»). «Si se repite» no tiene número en el Anexo A: se lee literalmente, volver a ocurrir (una segunda saturación del mismo agente en otro run); sin ventana temporal, contada desde la última P3- decidida de ese agente. Queda como `[PROPUESTO]` en INC-T178-01.
- **Cómo falla cerrado:** prioridad fuera de la lista cerrada → `ValueError` al encolar; un agente de instancia única nunca recibe ORD- (aunque se le pase un umbral 0); si la escritura de la P3- falla, el CAR- ya escrito no cita una P3- inexistente (se escribe primero la P3-).
- **Decisiones `[PROPUESTO]` (INC-T178-01):** la lectura de «si se repite»; el camino de la entrega (AG-01, AG-02, AG-18) como «afecta a plazos»; el orden de la clave de prioridad; el Coordinador lee de HA solo los avisos dirigidos a él, aunque la matriz de 5 del Documento 0 no lo lista como lector de HA (el prompt del Orquestador dice que lo lee).

## Riesgos

| Riesgo | Consecuencia | Mitigación |
| --- | --- | --- |
| Tocar `orquestacion.py`, que comparten T-176 y T-177 | Conflictos de fusión | Un cambio de una línea en el punto ya existente (`for orden in self.monitor.evaluar_instancias()`) |
| W_medio depende del reloj | HA no reproducible entre ejecuciones | El CAR- no lleva tiempos; solo contadores |
| El ciclo real no encola CT-05 en el monitor | La reordenación solo actúa sobre las órdenes que se registren | Documentado; la API (`ordenes=`) queda lista para cuando haya cola real |
| Romper las pruebas existentes de HT-08 | Regresión | Se mantienen `tipo_entrada`, `agente`, `cola`, `instancias` y la forma de ORD- |

## Criterios de aceptación (binarios)

1. CA-1: con seis CT-05 en la cola de AG-02 (umbral 3), cero ORD- para AG-02 y un CAR- de su saturación en HA (lo que ya había).
2. CA-2: la cola de AG-02 sale reordenada por prioridad (C1–C3 antes que C6; ALTA, NORMAL, BAJA; fecha objetivo; llegada), en el monitor y en el CAR-.
3. CA-3: el CAR- de AG-02 lleva `aviso_coordinador` para AG-01 y `avisos_plazos` lo devuelve; el de AG-20 no avisa.
4. CA-4: la primera saturación no crea P3-; la segunda en otro run crea una P3- PENDING_OPERATOR (origen ORQ) con los CAR- como evidencia; una tercera no la duplica y la cita; tras una P3- rechazada hace falta otra repetición.
5. CA-5: una prioridad fuera de la lista cerrada se rechaza al encolar; un agente con estado nunca recibe ORD- (umbral 0).
6. CA-6: la suite de A ≥ 607 y sin fallos; ruff ≤ 2813 y mypy de A ≤ 102; ciclos mock en verde; mapa y evidencias de PB-19 regenerados («Superada»).

## Plan de pruebas

| Prueba | Tipo | Criterio |
| --- | --- | --- |
| `test_t178.py`: reordenación de la cola y CAR- | nominal | CA-1, CA-2 |
| `test_t178.py`: aviso al Coordinador y su lectura; AG-20 sin aviso | nominal, límite | CA-3 |
| `test_t178.py`: repetición en dos ciclos reales del Bloque, P3- única, re-armado tras rechazo, misma ejecución no cuenta | integración, límite | CA-4 |
| `test_t178.py`: prioridad inválida; umbral 0 sin ORD- para AG-02 | fallo cerrado | CA-5 |
| Pruebas existentes de HT-08 y PB-19 | regresión | CA-1 |
| Mutantes propios (`mutantes.py`) | robustez de las pruebas | todos |
| Suite de A, gates, ciclos mock | regresión | CA-6 |

## Scripts

`.docs/scripts/evidencias_plan_a.py --pb PB-19` y `--ejecutar`; `.docs/tickets/T-178/mutantes.py` (nuevo).

## Registro

- 2026-11-17 · ABIERTO · creado con nuevo_ticket.sh
- 2026-11-17 · PLANIFICADO · claude · plan con fuentes del Documento 0 V5.3, el prompt del Orquestador y el esquema de HA
- 2026-11-17 · EN CURSO · claude · implementación (`ht08_monitor.py`, `carga.py`, una línea de `orquestacion.py`)
- 2026-11-17 · EN QA (r01) · claude · 17 pruebas, 27 mutantes muertos, suite de A y evidencias regeneradas (PB-19 Superada); commit local
- 2026-11-17 · EN CURSO (r02) · claude · QA r01 NO APTO (H-01 y H-02 medios, H-03 a H-07 bajos): corregidos los siete con su prueba de regresión
- 2026-11-17 · EN QA (r02: QA r01 NO APTO) · claude · 35 pruebas en `test_t178.py`, 36 mutantes muertos; commit local
- 2026-11-17 · CERRADO · claude (revisor) · QA r02 APTO: H-01 a H-07 corregidos con su prueba; r01_ataques 11/12 (A3 es el rechazo correcto de H-03) y r02_ataques 14/14, con H-01 entre procesos; 36 mutantes muertos; cuotas sin subir
