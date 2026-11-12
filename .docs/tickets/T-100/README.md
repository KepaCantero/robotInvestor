# T-100 · Marco común V0.76: pendientes de las QA r03 de T-75 y T-76

| Campo | Valor |
| --- | --- |
| Estado | CERRADO (QA r01 APTO, 12-11-2026) |
| Pieza | sistema_global/marco_comun_c |
| Planifica · implementa · QA | claude · claude · claude, con un revisor nuevo sin contexto (regla del operador del 12-11-2026) |
| Aprobación del operador | Aprobada el 2026-11-12: «sí abre el marco y corrige» (respuesta a «¿abro una V0.76 del marco para corregir estos pendientes, empezando por T-76 H-17?») |
| Deuda técnica | T-100 en `sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md`; los hallazgos vienen de las filas T-75 y T-76 |

## Objetivo

Corregir lo que las QA r03 de T-75 y T-76 dejaron en la deuda al dar APTO. Lo más importante es T-76 H-17: un movimiento de la cartera sombra declarado dos veces cuenta dos veces y puede dar la vuelta al juicio de los 24 meses.

## Alcance

- **Entra** (hallazgos de `.docs/tickets/T-75/qa.md` y `.docs/tickets/T-76/qa.md`, ronda r03):
  - **T-76 H-17 (media):** `movimiento_sombra` exige una referencia del movimiento. La misma referencia con el mismo contenido se ignora (O-02); con otro contenido es un incidente de seguridad (O-03 con kill-switch), como un `event_id` repetido;
  - **T-76 H-19 (baja):** con el registro roto, `barrer()` no calcula lo pendiente y activa el kill-switch, como cualquier punto de decisión que ve un registro roto;
  - **T-76 H-20 (baja):** MIG-011 y el Documento 0 de la V0.75 declaran que las comparaciones de la V0.73 y la V0.74 se conservan como históricas;
  - **T-76 H-18 (baja):** regresiones para los ocho mutantes vivos con efecto. Además, la regresión de H-03 se reescribe para que llegue a comparar, el coste se prueba contra un cálculo de referencia y se prueba el empate;
  - **T-75 H-15 (baja):** en `embudo()`, un análisis nuevo anterior al periodo también borra el veto anterior;
  - **T-75 H-17 (baja):** regresiones para los dos mutantes vivos (`reloj_firme` en la pantalla y el reinicio del veto).
- **No entra:**
  - contrastar los movimientos de la sombra con los de la cartera real, que es de G y K (T-86);
  - los avisos O-42 antiguos que siguen vivos tras comparar el mes (observación M4 de la r03 de T-76): se acusan como cualquier aviso;
  - los bloques A, A-Forex y B, y la Constitución.

## Diseño

- **Referencia del movimiento:**
  - es el identificador del movimiento en el intermediario: el que ven G y el operador, así que los dos declaran la misma;
  - se pasa como `ref` (texto no vacío, obligatorio) y se guarda en la entrada del registro;
  - contenido igual significa el mismo `tipo` y el mismo `importe_eur`. El precio del índice y el instante pueden diferir entre quienes lo declaran, y vale el de la primera declaración;
  - las entradas sin `ref` de un estado de la V0.75 se conservan y no se comparan con nada.
- **Estado persistido:** las entradas nuevas llevan `ref`; el formato del estado no cambia.
- **Esquema del código:** no cambia (la huella cuenta las constantes de los módulos y no hay ninguna nueva), así que no hay migración: se descartó la MIG-012 prevista al implementar.
- **Números:** ninguno nuevo.
- **Cómo falla cerrado:**
  - sin referencia, O-01;
  - con la misma referencia y otro contenido, O-03 con kill-switch;
  - con el registro roto, el barrido no saca conclusiones y para.

## Criterios de aceptación (binarios)

1. CA-1: un aporte declarado dos veces con la misma referencia cuenta una vez (O-02 la segunda), y el caso F2b de la QA r03 de T-76 ya no da PROPONER_PASIVA.
2. CA-2: la misma referencia con otro tipo o importe da O-03, activa el kill-switch y no anota nada; sin referencia, O-01.
3. CA-3: con el registro de la sombra roto, `barrer()` da O-13, activa el kill-switch y no da O-42 ni O-44.
4. CA-4: en `embudo()`, la causa previa de una salida es la misma se mire con el periodo que se mire (sonda n01 de la r03 de T-75).
5. CA-5: los mutantes de `.docs/tickets/T-75/revisores/r03_mutantes.py` y los ocho con efecto de `.docs/tickets/T-76/revisores/r03_04_mutantes.py` mueren con las baterías.
6. CA-6: el esquema del código sigue siendo el de la V0.75, así que un estado de la V0.75 se abre sin migración, y sus movimientos sin referencia se conservan.
7. CA-7: las 62 baterías del marco pasan, el LEEME coincide con el disco y el gate da 12/12; no cambia ningún bloque ni la Constitución.

## Plan de pruebas

| Prueba | Tipo | Criterio |
| --- | --- | --- |
| `pruebas_sombra_t76.py`, sección V0.76: referencia (duplicado, conflicto, sin referencia, F2b) | Nominal y fallo cerrado | CA-1, CA-2 |
| `pruebas_sombra_t76.py`: barrido con el registro roto | Fallo cerrado | CA-3 |
| `pruebas_sombra_t76.py`: A1, A2, A3, A8, A12, F9, H-03 reescrita, coste de referencia y empate | Regresión | CA-5 |
| `pruebas_embudo_sequia_t75.py`: n01 y q03 | Regresión | CA-4, CA-5 |
| Los scripts de mutantes de los revisores | Mutación | CA-5 |
| `pruebas_sombra_t76.py`: entrada sin referencia; `pruebas_integracion_v053.py`: esquema actual = V0.75 | Migración | CA-6 |
| Las 62 baterías, el LEEME y el gate | Regresión e integración | CA-7 |

## Registro

- 2026-11-12 · ABIERTO · creado con nuevo_ticket.sh, a petición del operador («sí abre el marco y corrige»)
- 2026-11-12 · EN QA · V0.76 implementada: referencia obligatoria de los movimientos de la sombra (O-02 / O-03 con kill-switch), barrido que para con la sombra rota, veto del embudo borrado por un análisis nuevo anterior al periodo, MIG-011 declarada; embudo 45 y sombra 94 comprobaciones; todos los mutantes de los revisores mueren; sin cambio de esquema
- 2026-11-12 · CERRADO · QA r01 APTO (revisor nuevo sin contexto, commit `3583c52`): CA-1 a CA-7 cumplidos, los seis hallazgos de origen corregidos. Cinco bajos nuevos: H-02 (diario de la V0.75 sin `punto()`) y H-05 (Documento 0 sobre los mutantes) se corrigen al cerrar en el Documento 0; H-01 (referencia sin normalizar), H-03 (mutante vivo del veto al pasar a EN_ANALISIS) y H-04 (referencia sin límite de longitud) pasan a la fila T-100 de la deuda
