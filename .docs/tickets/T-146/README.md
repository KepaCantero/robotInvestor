# T-146 · Bloque A: el presupuesto en UC corta antes de cada llamada

| Campo | Valor |
| --- | --- |
| Estado | EN CURSO (r02: QA r01 NO APTO) |
| Pieza | bloque_a (11_Ejecutor: `bloque_a/consumo.py`, `agentes.py`, `llm.py`, `orquestacion.py`, `config/por_defecto.yaml`, `README.md`; `tests/test_t146_presupuesto.py`, y un ajuste comentado en `tests/test_t88_consumo.py` y `tests/test_fase4_huecos.py`); `docs/incidencias.md` (INC-T146-01); `sistema_global/seguimiento/Decisiones_del_operador_Bloque_A.md` (§3) |
| Planifica · implementa · QA | claude · claude · el otro agente o un revisor nuevo |
| Aprobación del operador | 2026-11-15: modo sombra autorizado (Decisiones del operador, §1, «API real»); este ticket acota su gasto. Las decisiones nuevas van como `[PROPUESTO]` (INC-T146-01) |
| Deuda técnica | T-146 (número reservado en la deuda técnica por otra copia; este ticket no la toca) |

## Objetivo

Que **ninguna petición al modelo salga si su peor caso no cabe en lo que queda de su bolsa**, para que el gasto del modo sombra quede acotado por el presupuesto del ciclo. Origen: el análisis de T-145 (`.docs/tickets/T-145/analisis-tecnico.md`, «el presupuesto en UC no corta antes de la llamada»): con el peor caso, la bolsa de divisas acababa en 48,4 UC con un límite de 26,3.

## Alcance

- Entra: la reserva del peor caso petición a petición (primer intento, reparaciones y continuaciones de `pause_turn`); el cobro de la escritura de caché de los agentes compartidos sin que la liquidación pase una bolsa de su límite; AG-18, AG-19 y AG-20 dentro del presupuesto; las búsquedas web en UC; la suma de los límites del ciclo.
- No entra: la consulta N0 (C3, fuera del ciclo y del modo sombra; ver INC-T146-01); lo que lee cada búsqueda (llega como entrada y se cobra después, no se reserva); `contratos.py` y `.docs/scripts/estimar_coste_ciclo_a.py` (los lleva otra copia); la deuda técnica; los esquemas de los contratos (no cambian).

## Diseño

| Pieza | Qué hace |
| --- | --- |
| `consumo.ReservaLlamada` | Por llamada a un agente. `reservar` aparta en la bolsa el peor caso de la petición: la entrada medida con 3,6 caracteres por token (`llm._tokens_aprox`, la del ejecutor) por `presupuesto_uc.reserva.factor_tokens_entrada` (1,35, o el mayor observado en la bolsa) y toda como escritura de caché, `max_tokens` de salida y `max_uses` búsquedas, en UC con `Contabilidad.uc_de`. Si no cabe: (1) la ampliación con la regla del ejecutor; (2) si se deniega, la salida recortada a lo que cabe, no menos de `presupuesto_uc.reserva.salida_minima_tokens` (queda en `recortes_salida` del RUN en F5); (3) si ni eso, la petición no sale (`negada`). `pagar` cambia la reserva por el coste real, apartado hasta `cerrar`; si lo real pasa de lo reservado, queda en `excesos_reserva` y la bolsa usa desde entonces el factor observado |
| `agentes.Agentes.invocar` | Con `guarda`, reserva cada intento antes de llamar al cliente y paga lo que el cliente no pagó petición a petición. Si no cabe la primera, devuelve `SIN_PRESUPUESTO` sin llamar; si no cabe una reparación o una continuación, la llamada queda PARCIAL (`presupuesto_agotado`) |
| `llm.AnthropicClient.generar` | Cada continuación tras `pause_turn` reserva la suya (con la guarda de la variable de contexto `llm._GUARDA`, una por hilo) y paga cada petición con su uso |
| `orquestacion.Bloque._invocar` | Crea la guarda; si se negó una petición, cierra la fase declarada (`cierre_parcial`, como antes); con `control=True` (AG-18, AG-19) la ampliación se admite (R16). `max_uc_estimado` (solo la consulta N0) conserva la comprobación de antes |
| `orquestacion.Bloque._cargar` | Solo se aplaza hasta `liquidar_primas` la escritura del prefijo compartido, y como mucho la de la primera llamada de la bolsa a ese agente; el resto de lo escrito se carga ya. La prima «solo» de un agente compartido queda retenida en la bolsa hasta la liquidación, que no le carga más que eso (lo aplazado nunca pasa de la suma de las primas «solo») |
| `consumo.Presupuesto` | `reservado` y `retenido` cuentan como ocupado en `disponible` y en `autorizar_hasta_tope`; `tope_total` escala las bolsas si el reparto pasa del ciclo (N3 forzado en el periódico, un override); `absorber` suma lo de la bolsa de C5 |
| AG-18 (G3), AG-19 (auditoría), AG-20 (C5) | Contra la bolsa COMÚN (la de las fases transversales; el Documento 0 no da otra, y una bolsa nueva cambiaría la forma de CT-05 en los goldens). AG-20 corre antes del reparto: contra el mínimo de COMÚN (`fraccion_minima_comun` × ciclo, o el override), y lo consumido pasa a COMÚN |
| Búsquedas web | `uc.uc_por_busqueda_web` (0,32) en `Contabilidad.uc_de` |

- Contratos CT-G afectados: ninguno; los goldens coinciden (`python tests/goldens_ct.py`).
- Estado persistido: sin versión nueva. El RUN de F5 añade, solo si los hay, `recortes_salida` y `excesos_reserva`; el AUT- de un control dice «control … (R16)».
- Números (regla 2), en `config/por_defecto.yaml` con su origen: `presupuesto_uc.reserva.factor_tokens_entrada` 1,35 (el `factor_tokens_cota` de T-136), `presupuesto_uc.reserva.salida_minima_tokens` 2 500 (la salida que suponía `_estimar_uc` desde la entrega), `uc.uc_por_busqueda_web` 0,32 (0,01 USD por búsqueda ÷ 0,031 USD por UC con el modelo por defecto, tarifa del 15-11-2026). Todos `[PROPUESTO]`.
- Cómo falla cerrado: lo que no cabe no sale (ni siquiera con la salida mínima) y la fase se cierra declarada; un parámetro que falte es `KeyError` (`parametro`).
- Decisiones como `[PROPUESTO]` (INC-T146-01 y su fila en §3 de las decisiones del operador): reservar el peor caso; recortar la salida antes de cerrar; la salida mínima; la UC de una búsqueda; los controles admiten ampliación; AG-18/19/20 en COMÚN; la consulta N0 fuera.

## Riesgos

| Riesgo | Consecuencia | Mitigación |
| --- | --- | --- |
| La entrada real mide más que 1,35 veces la aproximación | Una petición cuesta más de lo reservado | Se anota en `excesos_reserva` y la bolsa usa desde entonces el factor observado; declarado en INC-T146-01 |
| Lo que lee una búsqueda no se conoce antes | Una petición con búsqueda puede costar más que su reserva | Se cobra al acabar la petición y cuenta para las siguientes; declarado (también lo dejaba fuera T-145, S5) |
| El recorte de la salida trunca una respuesta | La llamada queda PARCIAL tras su reparación | La reparación también reserva; lo truncado ya se declaraba («respuesta truncada por max_tokens») |
| Las semanas N1 piden una ampliación que se deniega | Un AUT- DENEGADA por RUN en HA y el Analista sale con unos 11 800 tokens de salida en vez de 12 000 | Es lo que cuesta de verdad: el peor caso del Analista (6,31 UC) no cabe en N1 (6,25). Explicado en el análisis |
| `test_t145.py` (otra copia) afirma que el presupuesto se pasa (`pasadas >= 1`) y la cota por presupuesto de `estimar_coste_ciclo_a.py` suma lo que el presupuesto dejaba pasar | Al juntar las copias, esa prueba falla y la cota es más alta de lo necesario | Avisado en el análisis para quien coordina: tras T-146 la cota por presupuesto es el límite máximo de cada bolsa |

## Criterios de aceptación (binarios)

1. CA-1: con el cliente real sobre un SDK falso de peor caso (reparaciones y continuaciones), solo divisas: ninguna bolsa supera su límite (asignado × 1,25 + ampliado ≤ asignado × 1,5), la suma no pasa de 240 × 1,5, todo lo gastado está en las bolsas, el ciclo termina PARCIAL con los cierres declarados y ninguna petición cuesta más de lo reservado.
2. CA-2: lo mismo con los 12 tipos y 6 hilos; con 4 tipos y 4 hilos, dos ejecuciones dan el mismo presupuesto, cierres y recortes en F5; también con el diseño V6.
3. CA-3: AG-18, AG-19 y AG-20 cargan en COMÚN (todo lo gastado está en las bolsas); sin sitio, AG-20 no sale y se declara; los controles admiten ampliación con su AUT-.
4. CA-4: las búsquedas cuentan en UC (`uc_de`, `resumen`) y se reservan al máximo.
5. CA-5: la reserva petición a petición: peor caso, cobro de lo real, recorte con salida mínima, ampliación antes de recortar, continuaciones dentro del cliente, factor observado, lo reservado cuenta en la ampliación.
6. CA-6: la liquidación de las primas no pasa de lo retenido; la suma de los límites máximos no pasa del ciclo.
7. CA-7: con el simulado, un ciclo N2 no recorta ni cierra y lo gastado está en las bolsas; un N1 recorta la salida del Analista y sigue COMPLETO. Comparación de antes y después (`comparar_ciclos.sh`): entregables iguales salvo la línea de consumo del informe técnico con búsquedas (los 12 tipos), explicado.
8. CA-8: `tests/test_t146_presupuesto.py` en verde; `test_integracion.py`, `test_unitarias.py`, `test_t87_*`, `test_t88_*`, `test_t113*`, `test_t12*`, `test_t13*`, `test_fase3_goldens.py`, `test_fase4_*` sin fallos; `tests/goldens_ct.py` coincide.
9. CA-9: `mutantes_t146.py`: todos los mutantes muertos.
10. CA-10: ruff (desde la raíz, los tres ejecutores) ≤ 2838; mypy de A ≤ 109.

## Plan de pruebas

| Prueba | Tipo | Criterio |
| --- | --- | --- |
| `test_ca1_peor_caso_divisas_…`, `test_ca1_las_ampliaciones_…` | integración, regresión (fallan sin T-146) | CA-1 |
| `test_ca2_peor_caso_doce_tipos_con_hilos`, `test_ca2_determinista_…`, `test_ca2_v6_…` | integración, determinismo | CA-2 |
| `test_ca3_…` (4) | integración, fallo cerrado | CA-3 |
| `test_ca4_las_busquedas_cuentan_en_uc` | nominal | CA-4 |
| `test_ca5_…` (8) | límite, fallo cerrado | CA-5 |
| `test_ca6_…` (2) | límite | CA-6 |
| `test_ca7_…` (2) y `comparar_ciclos.sh` | regresión | CA-7 |
| suites vecinas y goldens | regresión, contrato | CA-8 |
| `mutantes_t146.py` | mutantes | CA-9 |

## Scripts

En el ticket: `peor_caso_por_bolsa.py` (UC por bolsa con el peor caso, contra el código de antes o el de después), `comparar_ciclos.sh` (tres ciclos simulados de antes y de después en la misma ruta y su diferencia) y `mutantes_t146.py`. De `.docs/scripts/`: `nuevo_ticket.sh`.

## Registro

- 2026-11-15 · ABIERTO · creado con nuevo_ticket.sh
- 2026-11-15 · PLANIFICADO · claude · plan sobre el análisis de T-145 y el Documento 0 (§7.2, §10.3, R16, Anexo A)
- 2026-11-15 · EN QA · claude · implementado y probado (sin commit: lo hace quien coordina)
