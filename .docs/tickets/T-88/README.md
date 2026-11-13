# T-88 · Bloque A: consumo por tipo determinista con varios hilos (la prima de escritura de caché)

| Campo | Valor |
| --- | --- |
| Estado | CERRADO |
| Pieza | `bloque_a/11_Ejecutor` (`bloque_a/consumo.py`, `bloque_a/orquestacion.py`) |
| Planifica · implementa · QA | claude · claude · claude, con un revisor nuevo sin contexto (regla del operador del 12-11-2026) |
| Aprobación del operador | 2026-11-12: está en el orden de tareas obligatorias para evaluar el Bloque A por separado |
| Deuda técnica | T-88 en `sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md` (H-10 de la QA de T-65) |

## Objetivo

Que dos ejecuciones iguales del ciclo con varios hilos dejen en F5 el mismo consumo por tipo de activo (`presupuesto.*.consumido`). Hoy cambia de una ejecución a otra, aunque el total, la selección y los pronósticos no cambian. Hace falta antes del modo sombra con API: un registro de consumo que no se reproduce no sirve para auditar.

## Alcance

- Entra: el reparto entre bolsas (tipos de activo y bolsa común) de lo que cuesta cada llamada, en V5 y en V6.
- No entra:
  - la contabilidad de llamadas (`Contabilidad.llamadas`), que sigue con el coste real de cada una;
  - las estimaciones previas (`_estimar_uc`), que ya suponen el system prompt leído de caché;
  - las llamadas de curación de AG-12 (CT-11), que se invocan sin presupuesto y no se cargan a ninguna bolsa: unos 3 UC en un ciclo V5 de doce perfiles. Ya pasaba antes de T-88; corregido el motivo en el cierre (H-14 de la QA r04) y llevado a la deuda (T-107).

## Diseño

- **Causa:** la escritura de la caché de un prefijo compartido la paga el tipo cuyo hilo llega primero. Son prefijos compartidos el system prompt de un agente que trabaja para varios tipos (AG-10, AG-11, AG-12 y AG-14 en la V5) y, en la V6, el núcleo común de los analistas y AG-28.
- **Regla (`[PROPUESTO]`, INC-T88-01):**
  - durante la fase en paralelo, cada bolsa paga la lectura de lo cacheado y la prima «solo» de su propio analista: la escritura que pagaría ese analista si fuera el único del run (la primera llamada de cada agente en esa bolsa escribe su prefijo; las siguientes lo leen). Las primas «solo» de los agentes compartidos se anotan como pesos, pero no se cargan durante la fase (r02, H-01);
  - tras la fase en paralelo y al resumir, `liquidar_primas` cambia lo cargado por su parte de los tokens escritos de verdad en cada grupo de prefijos, en proporción a las primas «solo». El total cargado vuelve a ser el real. Grupo: cada agente en la V5 (r03, H-05); en la V6, los analistas forman un solo grupo porque comparten el núcleo, y cada agente compartido es su propio grupo;
  - todo se cuenta en tokens enteros, así que la suma no depende del orden de los hilos.
- **Estado persistido:** no cambia de forma; solo cambian los valores de `presupuesto` en F5.
- **Qué ve el control durante la fase (r02, corregido en la r03, H-07):** la lectura de lo cacheado y la escritura del prompt del analista propio. En la V5 es lo mismo que veía antes de T-88; en la V6 no, porque antes el primer analista pagaba el núcleo entero y ahora cada uno carga el suyo durante la fase. No ve las escrituras de los agentes compartidos (unos 3,5 UC en un ciclo V5 de doce perfiles), que se cargan al liquidar, al acabar la fase. En la V6 cada analista carga durante la fase su núcleo y su kit enteros (H-06, declarado).

## Criterios de aceptación (binarios)

1. CA-1: tres ejecuciones iguales con seis hilos dan el mismo `presupuesto` en F5, en V5 y en V6.
2. CA-2: en la V6, lo cargado a las bolsas es el coste real de las llamadas (±0,01 UC de redondeo).
3. CA-3 (texto al día en el cierre, H-17 de la QA r04): durante la fase, cada bolsa carga la lectura y la prima «solo» de su propio analista; tras liquidar, la prima real de cada grupo repartida en proporción a las primas «solo», sin cambiar el total; una segunda liquidación no cambia nada.
4. CA-4: el gate da 12/12, sin subir cuotas, y A sube con las pruebas nuevas.

### Ronda r02 (QA r01 APTO con H-01 medio, corregido antes de cerrar)

5. CA-5 (H-01): durante la fase en paralelo, cada tipo carga la lectura de lo cacheado y solo la escritura del prompt de su propio analista, que siempre escribe él (como antes de T-88); las escrituras de los agentes compartidos se reparten al liquidar. En la V5 ya no se cierran fases que antes no se cerraban.
6. CA-6 (H-02; reescrito en la r04, H-12 de la QA r03): la liquidación reparte por grupo de prefijos. En la V5 cada agente es su grupo, así que el prompt de un analista no se mezcla con otros tipos. En la V6 los analistas comparten grupo por el núcleo común, y su kit se reparte con el núcleo (unos 0,16 UC por ciclo en la medición de la QA r03, como mucho unos 0,03 UC por tipo; declarado en INC-T88-01).

### Ronda r04 (QA r03 NO APTO)

7. CA-7 (H-10): el registro RUN de F5 lleva otra vez `consumo`, en V5 y en V6, y una prueba comprueba sus claves.
8. CA-8 (H-13): las pruebas del ticket distinguen un analista V5 que reescribe su prompt (cada tipo paga sus reescrituras) y el orden de `cierres_parciales` (por tipo, fase y motivo).

## Plan de pruebas

| Prueba | Tipo | Criterio |
| --- | --- | --- |
| `tests/test_t88_consumo.py`: tres ciclos iguales con seis hilos, V5 y V6 | Regresión | CA-1 |
| `tests/test_t88_consumo.py`: total cargado frente a coste real (V6) | Integración | CA-2 |
| `tests/test_t88_consumo.py`: `Presupuesto` con primas a mano | Unitaria | CA-3 |
| `./tools/check_all.sh` | Gate | CA-4 |

## Registro

- 2026-11-12 · ABIERTO · creado con nuevo_ticket.sh
- 2026-11-12 · EN QA · reparto de las primas de caché por liquidación proporcional; 5 pruebas nuevas
- 2026-11-12 · APTO · QA r01 (revisor nuevo, commit `7feb697`): CA-1 a CA-4 cumplidos; H-01 medio (la prima «solo» de los agentes compartidos cerraba fases en la V5), H-02 a H-04 bajos
- 2026-11-12 · EN QA · Ronda r02 por decisión de Claude (H-01 cambiaba la selección en la V5): carga durante la fase solo la prima del analista propio; liquidación por grupo de prefijos (H-02)
- 2026-11-13 · NO APTO · QA r02 (revisor nuevo, commit `d1a5a1b`): H-05 medio (el grupo de los analistas reparte el prompt de un tipo entre todos), H-06 a H-09 bajos
- 2026-11-13 · EN QA · Ronda r03: en la V5 cada analista es su propio grupo (la V6 sigue con el grupo común por el núcleo, declarado); `cierres_parciales` en orden fijo; documentación al día; 6 pruebas nuevas que matan los mutantes P
- 2026-11-13 · NO APTO · QA r03 (revisor nuevo, commit `0afab6f`): H-10 alto (el comentario de H-09 dejó fuera `consumo` del RUN de F5), H-11 a H-13 bajos
- 2026-11-13 · EN QA · Ronda r04: `consumo` vuelve al RUN de F5; README, CA-6 y deuda al día; 4 pruebas nuevas (claves del RUN en V5 y V6, reescritura de un analista V5, orden de `cierres_parciales`) que matan R1, R4 y R5
- 2026-11-13 · APTO · QA r04 (revisor nuevo, commit `102aaae`): CA-1 a CA-8 cumplidos; H-14 a H-17 bajos (H-14 a H-16 ya pasaban antes de T-88)
- 2026-11-13 · CERRADO · H-14 (causa del hueco de unos 3 UC: la curación de AG-12 sin presupuesto) y H-17 (CA-3 y secciones r04 de `analisis-tecnico.md` y `pruebas.md`) corregidos en la documentación. H-14 (la causa), H-15 y H-16, a la deuda en T-107
