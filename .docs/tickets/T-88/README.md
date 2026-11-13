# T-88 · Bloque A: consumo por tipo determinista con varios hilos (la prima de escritura de caché)

| Campo | Valor |
| --- | --- |
| Estado | EN QA (ronda r03) |
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
  - las llamadas posteriores al registro de F5 (AG-18, AG-19 y AG-20 en la V5), que ya no se cargaban a ninguna bolsa (unos 3 UC en un ciclo de doce perfiles; declarado).

## Diseño

- **Causa:** la escritura de la caché de un prefijo compartido la paga el tipo cuyo hilo llega primero. Son prefijos compartidos el system prompt de un agente que trabaja para varios tipos (AG-10, AG-11, AG-12 y AG-14 en la V5) y, en la V6, el núcleo común de los analistas y AG-28.
- **Regla (`[PROPUESTO]`, INC-T88-01):**
  - durante el ciclo, cada bolsa paga la lectura de lo cacheado más su prima «solo»: la escritura que pagaría si fuera la única del run (la primera llamada de cada agente en esa bolsa escribe su prefijo; las siguientes lo leen). Es determinista y prudente: nunca carga menos que la prima real de esa bolsa;
  - tras la fase en paralelo y al resumir, `liquidar_primas` cambia esas primas «solo» por su parte de los tokens escritos de verdad, en proporción a las primas «solo». El total cargado vuelve a ser el real;
  - todo se cuenta en tokens enteros, así que la suma no depende del orden de los hilos.
- **Estado persistido:** no cambia de forma; solo cambian los valores de `presupuesto` en F5.
- **Qué ve el control durante la fase (r02, corregido en la r03, H-07):** la lectura de lo cacheado y la escritura del prompt del analista propio, como antes de T-88. No ve las escrituras de los agentes compartidos (unos 3,5 UC en un ciclo V5 de doce perfiles), que se cargan al liquidar, al acabar la fase. En la V6 cada analista carga durante la fase su núcleo y su kit enteros (H-06, declarado).

## Criterios de aceptación (binarios)

1. CA-1: tres ejecuciones iguales con seis hilos dan el mismo `presupuesto` en F5, en V5 y en V6.
2. CA-2: en la V6, lo cargado a las bolsas es el coste real de las llamadas (±0,01 UC de redondeo).
3. CA-3: durante la fase, cada bolsa carga su prima «solo»; tras liquidar, la prima real repartida, sin cambiar el total; una segunda liquidación no cambia nada.
4. CA-4: el gate da 12/12, sin subir cuotas, y A sube con las pruebas nuevas.

### Ronda r02 (QA r01 APTO con H-01 medio, corregido antes de cerrar)

5. CA-5 (H-01): durante la fase en paralelo, cada tipo carga la lectura de lo cacheado y solo la escritura del prompt de su propio analista, que siempre escribe él (como antes de T-88); las escrituras de los agentes compartidos se reparten al liquidar. En la V5 ya no se cierran fases que antes no se cerraban.
6. CA-6 (H-02): la liquidación reparte por grupo de prefijos (los analistas, que comparten el núcleo V6, y cada agente compartido), sin mezclar el prompt de un analista con otros tipos.

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
