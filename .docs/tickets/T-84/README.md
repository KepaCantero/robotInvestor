# T-84 · Revisión independiente de la V0.63 (semana simulada) y huecos de GLM

| Campo | Valor |
| --- | --- |
| Estado | EN QA (r01: NO APTO) |
| Pieza | sistema_global/marco_comun_c |
| Planifica · implementa · QA | la pieza es de GLM (V0.63) · no hay implementación nueva · QA: Claude, revisor nuevo |
| Aprobación del operador | no necesaria (revisión) |
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
