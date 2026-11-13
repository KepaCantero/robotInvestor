# T-117 · Bloque A V6: GC1 con señal y umbral por tipo de activo

| Campo | Valor |
| --- | --- |
| Estado | EN QA |
| Pieza | bloque_a (11_Ejecutor, `diseno_v6.py` y configuración) |
| Planifica · implementa · QA | claude · claude · un revisor nuevo sin contexto |
| Aprobación del operador | aprobada el 2026-11-13: «Haz ambos puntos. Lo confirmo», y que el agente decida por defecto los valores |
| Deuda técnica | T-117 en `sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md` |

## Objetivo

Que el filtro GC1 por código del diseño V6 tenga un umbral propio por tipo de activo y compruebe la concordancia de familias que pide el Anexo A, con valores medidos y registrados. Era el pendiente «GC1: señal y umbral por tipo» del relevo del 13-11-2026.

## Alcance

- Entra: `v6.gc1.umbral_por_perfil` y `v6.gc1.familias_min` (nuevos), `v6.gc1.senal_por_perfil` relleno, su validación, el registro de GC1 y sus pruebas.
- No entra: el diseño V5 (por defecto), que no cambia; el umbral general del Anexo A (0,75), que se conserva; recalibrar con datos reales (no hay fuente decidida).

## Diseño

- `gc1()` usa el umbral del tipo si está en `umbral_por_perfil`; si no, `seleccion.umbral_senal_gc1`.
- Cuando manda la señal compuesta, un ámbito pasa solo si además tiene `familias_min` familias concordantes. Si el Motor no da el recuento, no se descarta por esto (misma regla que con la señal no medible).
- El registro de GC1 guarda el umbral usado y `familias_min`; el motivo de cada descarte dice si fue por señal, por familias o por tope de candidatas.
- La configuración no válida se rechaza al crear el Bloque: tipo desconocido, umbral fuera de (0, 1], no numérico o no finito; `familias_min` que no sea un entero de 0 a 3.
- Contratos y estado persistido: no cambian.
- Números y su origen: `por_defecto.yaml`; los valores y la medida que los sostiene, en INC-T117-01.
- Decisiones `[PROPUESTO]`: señal compuesta en los doce tipos; umbral 0,65 en RF, MON y TCV; dos familias. Decididas por Claude por defecto y anotadas en el registro de decisiones.

## Riesgos

| Riesgo | Consecuencia | Mitigación |
| --- | --- | --- |
| Valores sacados de datos sintéticos | Umbrales mal puestos con datos reales | Declarados provisionales; la exploración de GC1 cuenta los falsos negativos y permite recalibrar |
| Bajar el umbral deja pasar señal débil | Más gasto en investigación | La concordancia de dos familias se exige siempre; el tope de candidatas no cambia |
| Cambiar el comportamiento del V5 sin querer | Regresión en el diseño por defecto | Las claves están bajo `v6`; prueba de que el V5 no cambia; suites de V5 y goldens en verde |

## Criterios de aceptación (binarios)

1. CA-1: los valores por defecto son los decididos y el umbral general y el diseño por defecto no cambian.
2. CA-2: cada tipo usa su umbral; el borde pasa y un valor inmediatamente inferior no.
3. CA-3: con la señal compuesta se exige la concordancia; sin el recuento no se descarta; con otra señal no se exige; con `familias_min: 0` no se exige.
4. CA-4: una configuración no válida se rechaza al crear el Bloque y una válida se acepta.
5. CA-5: en un ciclo V6 el registro de cobertura lleva el umbral de cada tipo.
6. CA-6: las pruebas de T-101, T-102, T-113 y T-88 (que usan la V6) siguen en verde; gate 12/12 y cuotas sin subir.

## Plan de pruebas

| Prueba | Tipo (nominal, límite, fallo cerrado, regresión, migración, integración) | Criterio |
| --- | --- | --- |
| `test_los_valores_por_defecto_son_los_decididos`, `test_en_el_diseno_v5_nada_cambia` | nominal y regresión | CA-1 |
| `test_el_umbral_del_tipo_manda…`, `test_cada_tipo_usa_su_umbral` (12), `test_el_borde_del_umbral…`, `test_para_volver_al_umbral_general…` | nominal y límite | CA-2 |
| `test_sin_el_recuento_de_familias…`, `test_con_familias_min_cero…`, `test_la_concordancia_solo_se_exige…`, `test_con_tres_familias_y_075…`, `test_un_descartado_por_familias_puede_llegar_como_exploracion` | nominal y límite | CA-3 |
| `test_una_configuracion_invalida_se_rechaza` (15), `test_una_configuracion_valida_se_acepta` (5) | fallo cerrado | CA-4 |
| `test_en_un_ciclo_el_registro_de_gc1_lleva_el_umbral_de_cada_tipo` | integración | CA-5 |
| Suites de la V6 y gate | regresión | CA-6 |

## Scripts

Ninguno nuevo. La medida de INC-T117-01 se hizo con un script de un solo uso (señal compuesta de los doce tipos en 17 fechas con los datos de ejemplo).

## Registro

- 2026-11-13 · ABIERTO · creado con nuevo_ticket.sh
- 2026-11-13 · EN QA · claude · implementado en una copia aparte: 43 pruebas nuevas en verde y las 399 de los ficheros que usan la V6; ruff 2902 y mypy 109, sin subir. Pendiente el gate completo y la QA
