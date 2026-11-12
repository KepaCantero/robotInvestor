# T-76 · Cartera sombra pasiva desde el primer día (D-22, D-27, D-30), marco V0.71

| Campo | Valor |
| --- | --- |
| Estado | CERRADO (QA r03 APTO, 12-11-2026) |
| Pieza | sistema_global/marco_comun_c |
| Planifica · implementa · QA | claude · claude · claude, con un revisor nuevo sin contexto (el operador lo autorizó el 12-11-2026: «sí que puedes hacer las QAs de cualquier cosa») |
| Aprobación del operador | No necesaria: aplica una decisión ratificada (D-22, D-27, D-30). El operador pidió el 2026-11-10 «sigue con el resto de la deuda que no dependa de mí» |
| Deuda técnica | T-76 en `sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md` |

## Objetivo

Dar una base para saber si el robot aporta valor (P17). Desde el primer día corre una cartera sombra pasiva con los mismos movimientos que la real. Cada mes se compara con el robot, neto de costes, impuestos e inflación. A los 24 meses, si el robot no la supera, se propone gestión pasiva.

## Alcance

- **Entra:**
  - el registro `sombra`;
  - `iniciar_sombra()`, `movimiento_sombra()`, `comparar_sombra()` e `informe_sombra()`;
  - el módulo `sombra.py`;
  - el aviso O-41;
  - la migración MIG-008.
- **No entra:**
  - los datos del índice y de la inflación desde K (T-86);
  - los impuestos de SC-9;
  - la revisión anual con el Broker (D-32);
  - las proyecciones (D-29).

## Diseño

Detalle en `sistema_global/documentos_0/V0.71_Cartera_sombra_pasiva.md`.
- **Contratos:** no cambian. **Estado:** atributo nuevo, MIG-008.
- **Números:** `i_meses_juicio_sombra` = 24 `[RATIFICADO]`; `i_indice_sombra` e `i_coste_anual_sombra_pct` `[PROPUESTO]`, para T-57.
- **Cómo falla cerrado:**
  - se rechazan los datos ilegibles, los meses fuera de orden o del futuro, las retiradas mayores que la sombra y los actores no autorizados;
  - un registro tocado da O-13 con kill-switch;
  - nada se cambia solo: el aviso propone y decide el operador.

## Riesgos

| Riesgo | Consecuencia | Mitigación |
| --- | --- | --- |
| Los impuestos los estima quien compara | Comparación sesgada | Se declaran en cada entrada; SC-9 los calculará |
| Comparar valores en vez de rentabilidades | Confusión al leerlo | Mismos movimientos en los dos: la diferencia de valores es la medida correcta; se da también por euro aportado |

## Criterios de aceptación (binarios)

1. CA-1: la sombra nace el primer día con el mismo capital y replica cada aporte y retirada al precio de su momento.
2. CA-2: cada mes, el robot neto de costes de análisis (los del Orquestador) e impuestos se compara con la sombra neta de su coste, en nominal y en real.
3. CA-3: antes de 24 meses no se juzga; a los 24, si no la supera en real, O-41 al pasar a no superarla (no cada mes); si la supera, nada.
4. CA-4: los rechazos no cambian el estado y el registro tocado se detecta (O-13 con kill-switch).
5. CA-5: guardar, cargar y MIG-008 funcionan; todas las baterías del marco pasan (60 en la V0.71, 62 en la V0.75) y el gate da 12/12.

## Plan de pruebas

| Prueba | Tipo | Criterio |
| --- | --- | --- |
| `pruebas_sombra_t76.py` · `el_primer_dia_*`, `un_aporte_*`, `G_tambien_*` | nominal | CA-1 |
| `la_sombra_vale_*`, `el_robot_va_neto_*`, `y_tambien_en_terminos_reales` | nominal | CA-2 |
| `a_los_23_*`, `a_los_24_*`, `si_la_supera_*`, `veredicto_en_el_borde` | límite | CA-3 |
| `*_no`, `tocar_*_se_detecta`, `con_el_registro_tocado_*` | fallo cerrado | CA-4 |
| `guardar_y_cargar_*`; `pruebas_integracion_v053.py` · `v071_*` | migración | CA-5 |

## Registro

- 2026-11-10 · ABIERTO · creado con nuevo_ticket.sh
- 2026-11-10 · EN QA · V0.71 implementada; batería nueva con 45 comprobaciones; 60 baterías en verde
- 2026-11-10 · DETENIDO · QA r01 NO APTO: H-01 a H-04 medios (prorrateo del coste de la sombra, juicio antes de tiempo, números enormes que dejan NaN, O-41 silenciable si I no compara) y H-05 a H-09 bajos. Por la regla del operador no se abre otra ronda; pendientes en la fila T-76 de la deuda
- 2026-11-10 · reabierto por el operador («Abre las rondas detenidas»)
- 2026-11-10 · EN QA · Ronda r02 (V0.73): corregidos H-01 (coste devengado por tramos), H-02 (solo meses terminados, en UTC), H-03 (resultados no finitos rechazados), H-04 (O-42 si I deja de comparar), H-05 (integridad antes de leer), H-06 (retirada en relativo), H-07 en parte (el índice de precios del inicio no cambia) y H-08 (O-41 al pasar a no superarla; documentación). 55 comprobaciones; pendiente la QA r02
- 2026-11-12 · EN QA · Ronda r03 (V0.75), retomada por el operador («empieza por T-75 y T-76»): corregidos H-10 (mes valorado a su cierre en UTC), H-11 (unidades no finitas rechazadas), H-12 (integridad antes de leer en `iniciar_sombra` y `movimiento_sombra`; O-13 en `barrer()`), H-13 (gracia de 5 días `[PROPUESTO]`, meses que faltan y O-44 ALTA para el juicio), H-14 (regresiones para los cuatro mutantes), H-15 (documentación y límites en T-86 y T-02) y H-16 (MIG-009 lo declara). 74 comprobaciones; 62 baterías en verde; pendiente la QA r03
- 2026-11-12 · CERRADO · QA r03 APTO (revisor nuevo sin contexto, commit `89e78e7`): H-10 a H-16 corregidos; se cumplen CA-1 a CA-5. Hallazgos nuevos: H-21 (el plazo de gracia no estaba en T-57) se corrige al cerrar; H-17 (media: `movimiento_sombra` sin identificador ni detección de duplicados; corregir antes de que G registre movimientos reales) y H-18 a H-20 (bajos: 10 mutantes vivos y la regresión de H-03 vacía, `barrer()` con el registro roto sigue calculando lo pendiente y no activa el kill-switch, MIG-011 no declara cómo se conservan las comparaciones de la V0.73 y la V0.74) pasan a la fila T-76 de la deuda
