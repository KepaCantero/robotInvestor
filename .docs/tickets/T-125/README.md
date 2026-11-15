# T-125 · Bloque A: fiabilidad de las fuentes de opinión (FUE-, PB-46)

| Campo | Valor |
| --- | --- |
| Estado | CERRADO |
| Pieza | bloque_a (11_Ejecutor: `evaluador.py`, `orquestacion.py`, configuración) |
| Planifica · implementa · QA | claude · claude · un revisor nuevo sin contexto |
| Aprobación del operador | 2026-11-14: «quiero que pases a completar el apartado 3 de huecos menores apuntados en la deuda técnica» |
| Deuda técnica | T-125 en `sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md` |

## Objetivo

Implementar el ciclo Evaluador → Buscador de la fiabilidad de las fuentes de opinión (PB-46 del Plan de pruebas V3.0; entradas FUE- del esquema de F6, 4.5), que el ejecutor no tenía.

## Diseño

- **Entrada:** las piezas de F2 con `tipo_afirmacion = PRONOSTICO_FUENTE` y su bloque `pronostico_fuente` (`ref_id`, `serie_ht01`, `fecha_objetivo`, `umbral_o_rango`, `direccion`, `probabilidad` si la da la fuente, `fecha_emision`), como dice el esquema de F2. El registro de evidencia guarda ahora ese bloque cuando la pieza lo trae.
- **Resolución (C5):** con el último cierre de HT-01 hasta la fecha objetivo (sin mirar después de `as_of`): `por_encima`, `por_debajo`, `dentro` o `fuera` del umbral o del rango. Un pronóstico que no ha vencido, mal formado, emitido después de su fecha objetivo, fuera de la ventana o sin dato reciente no se resuelve y no cuenta.
- **Métrica por fuente y mes:** Brier frente a una referencia ingenua, BSS, BSS contraído n / (n + k) con k = 20 y puntos de historial = 10 · (1 + BSS contraído), entre 0 y 20 (esquema de F6). Una FUE- por fuente con al menos `n_min` pronósticos resueltos; una vez al mes.
- **Comunicación:** las FUE- nuevas van al Buscador (AG-16) por CT-19, y cada FUE- anota el `msg_id`. La recalificación de la fuente en F9 la hace el Buscador: queda fuera del ejecutor.
- Números: `fiabilidad_fuentes` en `por_defecto.yaml`; k, neutro y máximo del esquema de F6; el resto `[PROPUESTO]` (INC-T125-01).
- Contratos: CT-19 por un canal ya previsto (AG-20 → AG-16); goldens de contratos sin cambios.

## Criterios de aceptación (binarios)

1. CA-1: con dos fuentes de 25 pronósticos, una con habilidad y otra sin ella, salen dos FUE- con n, aciertos, BSS, BSS contraído y puntos como dice la fórmula; la hábil por encima de 10 y la otra por debajo.
2. CA-2: en un ciclo, la FUE- queda en F6 con el `msg_id` del CT-19 enviado a AG-16.
3. CA-3: una vez al mes; sin muestra suficiente, nada.
4. CA-4: los pronósticos no vencidos, mal formados o sin dato no cuentan; las cuatro direcciones se resuelven bien.
5. CA-5: sin pronósticos de fuentes, el ciclo no cambia; goldens, ruff, mypy y gate en verde.

## Plan de pruebas

`tests/test_t125_fiabilidad_fuentes.py` (12 pruebas).

## Registro

- 2026-11-14 · ABIERTO · creado con nuevo_ticket.sh
- 2026-11-14 · EN QA · claude · implementado; pruebas del Evaluador, del ciclo y goldens en verde. PB-46 deja de estar «sin prueba»: la parte del ejecutor queda cubierta y la recalificación en F9 es del Buscador
- 2026-11-15 · NO APTO · QA r01 (revisor nuevo sin contexto): H-01 alto (en un ciclo ningún pronóstico de fuente llegaba a F2: el ejecutor perdía el bloque al construir las piezas), H-02 a H-04 medios (fecha con zona tumbaba el C5, registro tardío, `ref_id` sin validar), H-05 a H-08 bajos
- 2026-11-15 · EN QA · ronda r02 · claude · el bloque viaja del Analista y del Buscador a F2, validado (fuente de F9 que es la de la pieza, registrado antes de su fecha objetivo); fechas con zona sin excepción y el C5 a salvo; una FUE- por fuente y mes; deduplicación; Brier por el Motor con `calc_id`; probabilidad sin declarar 0,65 (banda). 43 pruebas nuevas en `tests/test_t125_r02.py`; las 12 de la r01, re-sembradas con registro previo y fuentes de F9. INC-T125-01 ampliada `[PROPUESTO]`
- 2026-11-15 · NO APTO · QA r02 (revisor nuevo sin contexto): H-01 a H-08 corregidos; nuevos H-09 y H-10 (medios: `variable` sin leer y fechas no ISO) y H-11 a H-13 (bajos)
- 2026-11-15 · EN QA · claude · ronda r03: `variable` obligatoria y solo las que resuelve el cierre (`fiabilidad_fuentes.variables_nivel`); fechas solo ISO 8601; umbral comparado como número; dirección que no es texto descartada sin excepción; `run_id` en la entrada de RC. `tests/test_t125_r03.py` (17); script del revisor `r02_01` sin fallos con su línea de B04 adaptada (el original se para porque «now» ya no se lee); ciclos sin el bloque iguales
- 2026-11-15 · CERRADO · QA r03 APTO (revisor nuevo sin contexto); hallazgos (H-14 media, H-15 a H-18 bajos) en T-134
