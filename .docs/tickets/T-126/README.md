# T-126 · Bloque A: pruebas de PB-26 y PB-48 del plan de pruebas

| Campo | Valor |
| --- | --- |
| Estado | EN QA |
| Pieza | bloque_a (11_Ejecutor, solo pruebas) |
| Planifica · implementa · QA | claude · claude · un revisor nuevo sin contexto |
| Aprobación del operador | 2026-11-14: «quiero que pases a completar el apartado 3 de huecos menores apuntados en la deuda técnica» |
| Deuda técnica | T-126 en `sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md` |

## Objetivo

Dar prueba a los dos casos del Plan de pruebas V3.0 que no tenían ninguna (PB-46, el tercero, se implementa en T-125).

## Qué se prueba

- **PB-26 · Clasificación temática y orden por calidad** (`test_t126_pb26_pb48.py::test_pb26_*`), sobre los F7, F8 y F9 entregados, leídos como los lee el ejecutor (`referencias.Referencias`, lector de HT-02):
  - 100 % de las referencias con una temática del Anexo D de su archivo (TA-, TM-, TF-);
  - 0 inversiones del orden descendente por Q dentro de cada temática;
  - el nivel A/B/C/D coherente con Q (13.3 del Documento 0: A ≥ 80, B 65–79, C 50–64, D < 50);
  - las fuentes de nivel D, marcadas como candidatas a baja o como única fuente;
  - y que la comprobación detecta un desorden, un nivel o una temática inventados.
  Hueco que queda: el procesamiento de altas nuevas lo hacen los Documentadores con el modelo real; aquí se comprueba el estado de los archivos.
- **PB-48 · Conflicto de normas (R23)** (`test_pb48_*`): una lección vigente que sugiere omitir la segunda pasada en banda marginal llega al Analista, pero lo que HT-03 recibe para decidir la elegibilidad no la lleva, y ninguna opción entregada incumple un control; HT-03 exige la segunda pasada en banda marginal. Hueco que queda: el ejecutor no implementa las guías de mejora del Orquestador (CT-18), así que no registra el conflicto (COR-) ni lo escala (P3-) — INC-T126-01.

## Criterios de aceptación (binarios)

1. CA-1: las pruebas de PB-26 pasan sobre los archivos entregados y detectan una mutación de orden, de nivel o de temática.
2. CA-2: las pruebas de PB-48 pasan y una lección que relaja un control no llega a las entradas de HT-03.
3. CA-3: el mapa del plan cita estas pruebas y las de T-125 (se actualiza cuando se integre la ronda r04 de T-116, que tiene abierto el mapa).
4. CA-4: no cambia código de producción; gate 12/12.

## Registro

- 2026-11-14 · ABIERTO · creado con nuevo_ticket.sh
- 2026-11-14 · EN QA · claude · 13 pruebas en verde; los archivos entregados cumplen PB-26 (0 inversiones, 0 temáticas inválidas, niveles coherentes)
