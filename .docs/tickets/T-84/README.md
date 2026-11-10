# T-84 · Revisión independiente de la V0.63 (semana simulada) y huecos de GLM

| Campo | Valor |
| --- | --- |
| Estado | EN QA (r01: NO APTO; ronda de correcciones c1 hecha, pendiente de la QA r02) |
| Pieza | sistema_global/marco_comun_c |
| Planifica · implementa · QA | la pieza es de GLM (V0.63) · correcciones c1: Claude (implementador, sin haber hecho la QA r01) · QA: Claude, revisor nuevo (r01); la r02, otro agente o revisor |
| Aprobación del operador | no necesaria (revisión); la ronda de correcciones la pidió el operador el 2026-11-10 |
| Deuda técnica | T-84 en `sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md` (G-05 y PC3-09 del Documento 0 de la V0.67) |

## Objetivo

Hacer la revisión independiente de la V0.63 (`pruebas/pruebas_semana.py`), que se había renunciado. Comprobar los dos huecos que dejó señalados GLM: un segundo corte en el diario firmado y un arranque con el reloj por detrás del estado.

## Alcance

- Entra:
  - si la semana prueba de verdad lo que dice (mutaciones dirigidas sobre `validador/diario.py`, `validador/reloj.py`, `validador/persistencia.py` y la propia batería);
  - sondas de los dos huecos;
  - otros defectos de robustez en esa zona.
- No entra: cambiar el código de producto, las pruebas existentes o los documentos (esta ronda solo informa); `validador/control_f.py` y `orquestador.py`, en los que trabajan otros agentes.

## Resumen de la QA r01 (detalle en `qa.md`)

**Veredicto: NO APTO.** El producto falla cerrado en los dos huecos de GLM. La batería de la semana no ejercita el Reloj que dice ejercitar.

- **Hueco 1, segundo corte en el diario firmado: falla cerrado.** Se probaron 50 posiciones de corte tras un primer corte recuperado, cortes dentro de la recuperación y del punto firmado, y diarios alterados. No se pierde ni se duplica nada, nada alterado se acepta y la recuperación es idempotente.
- **Hueco 2, reloj detrás del estado: falla cerrado.** RL-02 bloquea, no hay instantes anteriores, la degradación queda anotada y el rearme no deja pasar un reloj atrasado. Con dos matices de producto, ambos bajos: H-04 (sin `comprobar_estado` el Reloj sí da un instante anterior, aunque el Orquestador lo rechaza con O-16) y H-05 (el `guardado_en` del estado puede retroceder).
- **Mutaciones:** la semana caza las 7 de diario y persistencia que dice cubrir. Deja vivas las 7 del reloj que dice cubrir y las 2 de la propia batería. La dorada de la V0.66 no caza ninguna.

| ID | Gravedad | En una línea |
| --- | --- | --- |
| H-01 | media | La semana no ejercita el Reloj. `instante()` es `contrastar` en cada paso y la pared va siempre a la par del intermediario, así que el instante es la hora del intermediario. `ahora()` no se usa: con `ahora()` roto o con `contrastar` sin leer el reloj, la semana pasa |
| H-02 | baja | RL-02 y el suelo nunca se ejercitan en la semana (el hueco 2 de GLM). `comprobar_estado` va con `assert`, así que un RL-02 tumba la batería sin contarse como fallo |
| H-03 | baja | El corte del miércoles no se verifica: con `cortar()` sin efecto la semana pasa. Nunca deja una OP sin RES ni corta el diario firmado (el hueco 1 de GLM) |
| H-04 | baja | Un `Reloj` nuevo da instantes antes de `comprobar_estado`, también anteriores al estado. Lo paran O-16 en el Orquestador y G-06 en G |
| H-05 | baja | `punto()`, `crear` y `volcar` aceptan cualquier instante (también 2020), y `comprobar_estado` no mira `guardado_en`: el instante de guardado del estado puede retroceder |
| H-06 | baja | Un corte dentro de la escritura atómica deja `.diario-*.tmp` o `.estado-*.tmp` que nadie borra |
| H-07 | baja | Dos propiedades del Reloj sin prueba en ninguna batería del marco: «`contrastar` da el mayor» y el salto tras horas de marcha |
| H-08 | baja | El determinismo byte a byte es cierto pero no lo exige la batería. El `revision.md` de la V0.63 la da por «renunciada» |

## Plan de la ronda de correcciones c1 (2026-11-10)

Reabierto por el operador para corregir lo que dejó la QA r01. Ficheros que se pueden tocar:

- `pruebas/pruebas_semana.py` y `pruebas/pruebas_reloj_t03.py`;
- `validador/reloj.py`, `validador/diario.py` y `validador/persistencia.py`, solo para H-04 a H-06 y sin cambiar el formato del estado ni el del diario;
- el LEEME del marco;
- `entrega_glm/V0.63/revision.md`, solo para añadir;
- este ticket, salvo `qa.md`.

Quedan fuera `orquestador.py`, `sombra.py`, `parametros_doc.py` y `bloque_a/`, en los que trabajan otros agentes. No hay commit en esta ronda.

| Criterio | Hallazgo | Se cumple si (binario) |
| --- | --- | --- |
| CC-1 | H-01 | La `Maquina` toma los instantes de `Reloj.ahora()`, con la pared desfasada del intermediario. r01 sobre una copia limpia con los cambios: la semana caza R01, R02, R03, R05, R07, R08 y R09 |
| CC-2 | H-01, H-08 | Dos ejecuciones de la semana dan la misma salida byte a byte (sha-256 igual) y la dorada de la V0.66 pasa sin regenerar su foto |
| CC-3 | H-02 | No queda ningún `assert` en la `Maquina` y cada arranque es un `h.chk`. Hay una mañana con el reloj detrás del estado (RL-02, suelo, `degradar_por_reloj` por el diario y rearme). S02, aplicada al texto nuevo, queda cazada |
| CC-4 | H-03 | El corte del miércoles exige `linea_incompleta` y un diario limpio. El diario firmado se corta con una OP sin RES y con un segundo corte (barrido). S01 y S03 quedan cazadas |
| CC-5 | H-07 | `pruebas_reloj_t03.py` caza R04 y R06 (r01 con `--resto`) |
| CC-6 | H-06 | `abrir` borra los `.diario-*.tmp` y `.estado-*.tmp` huérfanos, y solo esos. D11 queda cazada y la nota final de r02 da 0 |
| CC-7 | — | `persistencia.esquema_actual()` es el mismo con y sin los cambios |
| CC-8 | — | `leeme_marco.py` da SIN DIFERENCIAS |
| CC-9 | — | El lote del marco (`pruebas_marco.sh`) está en verde sobre HEAD con los cambios. En el árbol de trabajo no aparecen fallos nuevos frente a la línea base |
| CC-10 | H-04, H-05, H-08 | Lo que no se corrige queda explicado en este ticket, con su ID, para la deuda. En `revision.md` de la V0.63 hay una nota que cita T-84 |

### Resultado de la ronda c1

Detalle en `analisis-tecnico.md` y `pruebas.md`.

- **Corregidos:** H-01, H-02, H-03, H-06 y H-07. H-08, en parte: la nota en `revision.md` y el determinismo comprobado a mano.
- **A la deuda** (los añade a la de T-84 quien haga el commit; esta ronda no toca el fichero de la deuda):
  - **T-84/H-04:** el Reloj da instantes antes de `comprobar_estado`. Cambiar el contrato afecta a cuatro baterías que piden instantes sin él; lo paran O-16 y G-06.
  - **T-84/H-05:** el `guardado_en` puede retroceder. Exige cambiar `punto`, `crear`, `volcar` y `abrir`, y hoy el `guardado_en` no decide nada.
  - **T-84/H-08:** que la batería exija ella misma el determinismo byte a byte, y que pase con `python -O` (los auxiliares de `pruebas/pruebas_orquestador.py` llaman al Orquestador dentro de `assert`).
  - **Sonda r01:** se cae con una mutación no aplicable (S02 tras H-02). Lo corrige la QA r02.
- **Mutaciones:** la semana caza ahora 16 de las 26 mutaciones aplicables de r01, antes 6. Son todas las que dice cubrir (14), más D10 y R04. Con S02 adaptada y las nuevas S03 y D11, caza 19 de 29 y ninguna CAZAR queda viva. R04 y R06 las caza ahora `pruebas_reloj_t03.py`.
  - **Nota de integración, nueva:** con la máquina por detrás del intermediario, los instantes de `ahora()` son anteriores a la hora de sus datos y el Orquestador los rechaza (O-10). La integración real debe contrastar antes de usar datos del intermediario.

## Scripts

- `.docs/scripts/nuevo_ticket.sh` (abrir el ticket) y `.docs/scripts/pruebas_marco.sh` (lote del marco: 59 de 59 en verde).
- Sondas de la QA, en la carpeta V0.63_revision de entrega_claude del marco (sin rastrear en git):
  - r01_mutaciones_semana.py: 27 mutaciones, con las opciones `--doradas`, `--resto`, `--todas` y `--solo`;
  - r02_segundo_corte_firmado.py;
  - r03_reloj_detras_del_estado.py;
  - r04_reloj_huecos_sin_bateria.py.
- Las cuatro se ejecutan con `python3 -I` desde el marco.

## Registro

- 2026-11-10 · ABIERTO · creado con nuevo_ticket.sh
- 2026-11-10 · EN QA · r01 de Claude: NO APTO (H-01 medio; H-02 a H-08 bajos). Siguiente: corregir H-01 a H-03 en la batería de la semana; H-04 a H-07 a la deuda si no se corrigen ahora
- 2026-11-10 · reabierto por el operador: correcciones (ronda c1, plan arriba)
- 2026-11-10 · EN QA · ronda c1 hecha por Claude (implementador): H-01, H-02, H-03, H-06 y H-07 corregidos, H-08 en parte; H-04, H-05 y el resto de H-08 a la deuda. Semana 123 → 176, reloj_t03 77 → 80. Sin commit. Siguiente: QA r02, que vuelve a pasar r01 y actualiza B9 de r03
