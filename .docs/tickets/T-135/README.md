# T-135 · Bloque A, Motor: hallazgos de las QA r03 de T-127 y r02 de T-128

| Campo | Valor |
| --- | --- |
| Estado | EN QA |
| Pieza | bloque_a (11_Ejecutor: `bloque_a/motor/`) |
| Planifica · implementa · QA | Claude · Claude (subagente) · un revisor nuevo sin contexto |
| Aprobación del operador | 2026-11-14: «quiero que por tu cuenta vayas completando los tickets que quedan abiertos»; 2026-11-15: los tickets nuevos, con QA APTO |
| Deuda técnica | T-135 en `sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md` |

## Hallazgos

- **T-128 H-05 (media):** en IDX-CONC-001, la amplitud con los precios de un valor y una copia suya (exacta o a escala) es la de ese valor; la prueba `test_h02_idx_conc_porcentaje_sobre_la_media_de_un_solo_valido` lo fija como correcto. Corregir antes del modo sombra.
- **T-128 H-06 (baja):** la dominancia por grupos de copias en CHR-FLOW-001 no tiene prueba (sobrevive el mutante que quita `grupos` de `_sin_dominio`).
- **T-127 H-06 (baja):** falsos avisos en CHR-TOKEN-001 con dos tokens de oferta fija y redonda.
- **T-127 H-07 (baja):** REI-NAV-001 sin `otros_pasivos` y con un solo dato movido da la prima de una sociedad sin aviso.
- **T-127 H-08 (baja):** el docstring de `motor/frontera_b.py` mantiene la frase absoluta que INC-T127-01 r03 quitó.

## Diseño (añadido al implementar)

- **T-128 H-05 (IDX-CONC-001).** Las series de precios de la amplitud se agrupan por sus rentabilidades
  (`frontera_b._etiquetas_series_copiadas`): copias si coinciden a menos de `tolerancia_clon` (1 %) en todas las fechas en
  que las dos tienen rentabilidad y sus precios comunes abarcan al menos `anios_precios_min` (1 año, la entrada mínima de
  la ficha). Un grupo de copias cuenta como un componente para `IDX_CONC_COMPONENTES_MINIMOS` (amplitud y porcentaje sobre
  la media) y ningún grupo puede pasar del `peso_maximo_componente` (95 %) de las series; si no, `null` con su limitación.
- **T-128 H-06 (CHR-FLOW-001).** Solo una prueba (el código ya agrupaba).
- **T-127 H-06 (CHR-TOKEN-001).** `_aviso_casi_clones` pide además `coincidencias_informativas_minimas` (2, nuevo en
  `AVISO_B`) coincidencias que no sean ``None``/``None`` ni 0/0; la firma del aviso de CHR-TOKEN-001 deja en ``None`` la
  oferta total que es la circulante y la máxima que es la total, y lleva el *staking* y la concentración.
- **T-127 H-07 (REI-NAV-001).** La firma del aviso son los datos aportados: `otros_pasivos` (``None`` si se derivan) y el
  GAV (``None`` si los otros pasivos se aportan).
- **T-127 H-08.** Docstring de `frontera_b.py` matizado.
- Decisiones `[PROPUESTO]` en INC-T128-01 e INC-T127-01, «Ronda T-135». Contratos, esquemas y casos de control no cambian.

## Criterios de aceptación (binarios)

1. CA-1 (T-128 H-05): IDX-CONC-001 con un valor y una copia suya (exacta, a escala o recortada) no da la amplitud
   (`null`, sin identificadores); con dos valores distintos la da a mano; un grupo de copias de más del 95 % de las series
   tampoco la da; la concentración no cambia; `r02_01_chr_flow_e_idx_conc.py` 18/18. La prueba de T-128 r02 que fijaba la
   fuga cambia, comentada «T-135».
2. CA-2 (T-128 H-06): una prueba de la dominancia por grupos de CHR-FLOW-001 mata el mutante sin `grupos`.
3. CA-3 (T-127 H-06): los dos tokens de oferta fija y redonda del revisor no dan el aviso (con y sin *staking*); las copias
   con un dato movido de `test_t127_r03.py` lo siguen dando; ningún caso de control lo da; `r03_01_cota_aviso_y_origen.py`
   11/11.
4. CA-4 (T-127 H-07): REI-NAV-001 con A en dos partes y el NAV por acción ±4 % da el aviso con y sin `otros_pasivos`.
5. CA-5 (T-127 H-08): el docstring de `frontera_b.py` no dice que la frontera lo impida sin matiz.
6. CA-6: casos de control 67/67; mutantes de `revisores/impl_mutantes.py` muertos (o equivalentes explicados); suites del
   Motor y vecinas en verde; ruff ≤ 2902 y mypy de A ≤ 109; incidencias con «Ronda T-135» y `[PROPUESTO]`.

## Registro

- 2026-11-15 · ABIERTO · creado con nuevo_ticket.sh
- 2026-11-15 · EN CURSO · Claude (subagente) · implementa los cinco hallazgos en una copia (rama `t135`, base `eb66257`); pruebas en `tests/test_t135_motor.py`
- 2026-11-15 · EN QA · Claude (subagente) · implementado y probado (`analisis-tecnico.md`, `pruebas.md`); sin commit (lo hace quien coordina)
