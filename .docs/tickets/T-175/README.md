# T-175 · Informe técnico: la opción excluida por una objeción fuerte sin resolver como alternativa documentada (PB-38)

| Campo | Valor |
| --- | --- |
| Estado | CERRADO (17-11-2026, QA r02 APTO tras la ronda de cierre) |
| Pieza | bloque_a/11_Ejecutor (redaccion, sintesis) |
| Planifica · implementa · QA | claude · claude · astra (o un revisor que no implementó) |
| Aprobación del operador | no necesaria (corrección de un hueco frente al plan de pruebas V3.0; no cambia ningún formato congelado) |
| Deuda técnica | T-175 en `sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md` |

## Objetivo

PB-38 («Objeción fuerte sin resolver impide el top-3», plan V3.0) sale «Superada en parte»: la opción no entra en el top-3 y queda en F3 como no elegible, pero el informe técnico no la documenta (INC-T116-03; punto 9 del plan de la noche del 15-11-2026). El resultado esperado del plan pide además que «la objeción figura en el técnico como sin resolver» y que «la opción queda como alternativa documentada». Se cierra ese hueco.

## Alcance

- Entra:
  - Informe técnico (`redaccion.Redaccion.tecnico`): subsección **4.N.4 «Alternativas descartadas relevantes»** de la plantilla V5.0 (`06_Plantillas_entregables/Plantilla - Informe técnico para el Broker - V5.0.md`), con sus columnas *Candidata · Puerta en la que quedó · Motivo · Qué tendría que ocurrir*, en cada tipo de activo que tenga alguna.
  - Sección 6 «Objeciones y respuestas»: las objeciones fuertes y moderadas de esas alternativas, con su estado (`SIN_RESOLVER` o `RESPONDIDA`) calculado con la misma regla que las del top-3.
  - Una función pura en `sintesis.py` que reúne las alternativas descartadas desde `extras["seleccion"]` y la regla del estado de una objeción, compartida con la del paquete.
- No entra:
  - El JSON del paquete y el informe visual (esquema congelado; el plan solo pide el técnico).
  - Las finalistas elegibles fuera del top-3 por RK (no se descartan en una puerta: siguen en F3 como `EN_OBSERVACION`), las vigentes que dejan de ser elegibles (ya salen en la sección 5 como `CERRADA`) y las mantenidas por arrastre. Queda en INC-T175-01 `[PROPUESTO]`.
  - Las subsecciones 4.N.1, 4.N.2 y 4.N.5 de la plantilla y los «veredictos globales» de la sección 6 (otros huecos, no de PB-38).
  - El corpus congelado (plantilla, esquema, HT-03, HT-09) y los otros bloques.

## Diseño

- Contratos CT afectados: ninguno. Ni `paquete_oportunidades` ni los goldens cambian.
- Estado persistido: no cambia (F3 ya guarda la opción no elegible con sus objeciones; el técnico se lee de `extras`, que ya existe en memoria).
- Qué es una alternativa descartada (`sintesis.alternativas_descartadas(paquete, extras)`): candidata de `extras["seleccion"][clase]["candidatos"]` que no está entre las opciones del paquete, no es de arrastre, no es vigente y HT-03 la declara no elegible (`_ht03.elegible` falso). Orden: RK descendente y `opp_id`. Por cada una:
  - **Puerta:** las puertas de sus motivos `PUERTA_NO_SUPERADA`/`PUERTA_SIN_DATO` (p. ej. «G2»); si no hay ninguna, «Elegibilidad HT-03 (9.2)».
  - **Motivo:** los `detalle` de HT-03 (texto del ejecutor) y, si hay objeciones fuertes sin resolver, sus identificadores `OBJ-`.
  - **Qué tendría que ocurrir:** lo de HT-03 (`_que_tendria_que_ocurrir`, la misma frase que ya usa R14) y, por cada objeción fuerte sin resolver, su `que_la_resolveria` (texto del modelo, ya reescrito por R22 en el camino de invocación).
- Números: ninguno nuevo. El tope «máx. 5» de la plantilla se cumple sin escribirlo: las alternativas salen de las finalistas GC3, que son como mucho `seleccion.max_finalistas` (5, `config/por_defecto.yaml`) por clase.
- G3-MET-13: el ejecutor no escribe la raíz «valid-» en ningún texto nuevo; el técnico entero se sigue comprobando después (`g3_met13_tecnico`), y lo que venga del modelo ya pasó la reescritura R22. Una celda con «|» o un salto de línea se escapa para no romper la tabla. **r02 (QA r01, H-01):** el texto del modelo de una alternativa que G3-MET-13 rechazaría se sustituye antes de escribir el técnico (`alternativas_descartadas(…, bloque)`) y se avisa en HA (`advertir_alternativas_retiradas`); ver CA-6.
- Cómo falla cerrado: una candidata mal formada (sin `_ht03`, sin `opp_id`) no se lista ni rompe el informe; un valor de objeción que no es texto se escribe como «—». La coherencia G3-ENT-07 no cambia: las alternativas no usan el encabezado `##### N.` ni la celda `· \`OPP\` | RK |` del top-3.
- Decisiones `[PROPUESTO]`: INC-T175-01 (qué filas lleva 4.N.4 y que la sección 6 lista las fuertes y moderadas de las alternativas, como pide la plantilla).

## Riesgos

| Riesgo | Consecuencia | Mitigación |
| --- | --- | --- |
| Un texto del modelo de la alternativa cita un método con «valid-» | El técnico entero queda BLOQUEADO (antes era una advertencia de una no entregada) | Es lo correcto: el técnico va al Broker. Ya pasa por la reescritura R22; prueba que lo demuestra |
| Cambiar el técnico de un ciclo normal más de lo debido | Diferencias espurias para el Broker y los otros tickets | Ciclo mock antes/después: solo cambian 4.N.4 y filas nuevas de la sección 6 |
| Romper la coherencia G3-ENT-07 o el orden del top-3 | Bloqueo de la entrega | Prueba de ciclo con dictamen APTO y `coherencia` vacía |
| Conflicto con T-173/T-174 en ficheros compartidos | Merge costoso | Cambios acotados a `tecnico()` y una función nueva; mapa y evidencias solo en la fila PB-38 |

## Criterios de aceptación (binarios)

1. CA-1: en el ciclo mock, la opción con una objeción fuerte sin resolver (OPP fuera del top-3, no elegible en F3) aparece en la subsección 4.N.4 de su clase con su puerta (G2), su motivo (la objeción fuerte sin resolver y su `OBJ-`) y lo que tendría que ocurrir.
2. CA-2: esa objeción figura en la sección 6 con estado `SIN_RESOLVER` y la `OPP-` de la alternativa.
3. CA-3: la opción no está en el top-3 ni en el JSON; el orden y el RK del top-3 coinciden con el JSON (coherencia vacía) y el dictamen G3 no empeora.
4. CA-4: el técnico de un ciclo normal solo cambia en las subsecciones 4.N.4 nuevas y en las filas nuevas de la sección 6 (diff del ciclo mock antes/después).
5. CA-5: una candidata elegible fuera del top-3, una vigente no elegible y una de arrastre no se listan; una mal formada no rompe el informe.
6. CA-6 (reformulado en la r02, QA r01 H-01): el texto que escribe el ejecutor no lleva la raíz «valid-»; un texto del modelo de una alternativa que G3-MET-13 rechazaría (la raíz «valid-», también si persiste tras la reescritura R22, o una ficha desconocida, regla B) no bloquea la entrega: sale ENTREGADA, la fila de 4.N.4 y la de la sección 6 se mantienen con el texto sustituido (nombre → símbolo; resumen y respuesta → «Texto del modelo retirado por G3-MET-13 (R22); íntegro en F3»; sin «qué la resolvería»), el texto íntegro sigue en F3 y hay una ADVERTENCIA de G3-MET-13 en el G3V de F7.
7. CA-7: PB-38 pasa a «Superada» en el mapa y en las evidencias; suite de A ≥ 607, ruff ≤ 2813, mypy de A ≤ 109.

## Plan de pruebas

| Prueba | Tipo | Criterio |
| --- | --- | --- |
| `test_t175_pb38_*` ciclo mock: 4.N.4 y sección 6 con la alternativa | integración | CA-1, CA-2, CA-3 |
| función `alternativas_descartadas` con candidatas sintéticas (elegible, vigente, arrastre, mal formada, orden) | límite · fallo cerrado | CA-5 |
| `tecnico()` con una alternativa cuya objeción lleva «\|» y salto de línea | límite | CA-1 |
| Texto del modelo rechazado en una alternativa (ficha desconocida; «validada» que persiste): entrega ENTREGADA, texto sustituido, ADVERTENCIA en HA | fallo cerrado | CA-6 |
| Diff del técnico de un ciclo mock antes/después (script en el ticket) | regresión | CA-4 |
| Mutantes propios (quitar la subsección, quitar las filas de la sección 6, invertir el filtro de elegibilidad, olvidar el estado) | regresión | CA-1..CA-5 |
| `evidencias_plan_a.py --ejecutar` y suite completa de A | integración | CA-7 |

## Scripts

- `.docs/scripts/evidencias_plan_a.py` (mapa y evidencias).
- `.docs/tickets/T-175/diff_tecnico.py` (diff del técnico antes/después, en el ticket).

## Registro

- 2026-11-17 · ABIERTO · creado con nuevo_ticket.sh
- 2026-11-17 · PLANIFICADO · claude · plan, criterios y pruebas escritos
- 2026-11-17 · EN CURSO · claude · implementación y pruebas (analisis-tecnico.md, pruebas.md)
- 2026-11-17 · EN QA (r01) · claude · gate 12/12, 12/12 mutantes muertos, PB-38 «Superada»; commit local sin push, traspaso en handoff.md
- 2026-11-17 · EN QA (r02: QA r01 NO APTO) · claude · H-01 (sustitución del texto del modelo y ADVERTENCIA en HA), H-02 y H-03 corregidos; rebasado sobre origin/develop (T-171)
- 2026-11-17 · EN QA (ronda de cierre de la QA r02) · claude · QA r02 APTO con H-04 (bajo) corregido: los BLOQUEOS de G3-MET-13 siempre delante en los cinco detalles del G3V de F7
- 2026-11-17 · CERRADO · claude (revisor) · ronda de cierre de la QA r02 comprobada: H-04 corregido; `bloqueos_delante` en `g3_met13_tecnico` no cambia dictamen, motivo, resultados ni incidencias de T-165 (160 pruebas de T-165 y T-175 superadas); 25/25 mutantes; veredicto final APTO
