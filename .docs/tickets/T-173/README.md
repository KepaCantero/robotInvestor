# T-173 · Bloque A: PB-50 (degradación «Sí» → «Limitado» por DM-HLN) y PB-64 (publicación de los estados H5)

| Campo | Valor |
| --- | --- |
| Estado | CERRADO (17-11-2026, QA r02 APTO tras la ronda de cierre) |
| Pieza | bloque_a (ejecutor): `bloque_a/11_Ejecutor/bloque_a/evaluador.py`, `sintesis.py`, `redaccion.py` |
| Planifica · implementa · QA | claude · claude · otro agente o un revisor nuevo |
| Aprobación del operador | 2026-11-15: plan de la noche para terminar el Bloque A (`.docs/tickets/_relevo/plan_noche_bloque_a_2026-11-15.md`, punto 6); sin decisión nueva |
| Deuda técnica | T-173 en `sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md` |

## Objetivo

Cerrar los dos huecos de INC-T116-03 que dejan PB-50 y PB-64 «Superada en parte»: el Evaluador baja solo de «Sí» a «Limitado» un horizonte H1–H4 que pierde frente a la referencia ingenua con significación (12.2 del Documento 0 V5.3), y publica los estados de los pronósticos H5 por hitos en F6 y en los entregables (esquema de F4, 5.1; prompt del Evaluador, 6.7 bis.4).

## Alcance

- **Entra:**
  - `Evaluador.aplicar_degradacion_dm(as_of, run_id)`: celdas clase × horizonte (H1–H4) con ≥ `evaluacion.min_calibrar` pronósticos admisibles resueltos y DM-HLN unilateral «el pronóstico es peor que la referencia» con p ≤ `evaluacion.alfa_holm`. Si la celda está en «Sí» en la matriz vigente (P-31 de F10 o la tabla 8.3), baja a «Limitado»: AJU- en F6 con la evidencia DM-HLN, CFG- de P-31 y de P-30 (versión menor) en F10. Se llama desde `Evaluador.ciclo` (C5).
  - Las reglas de la degradación de H5 valen igual: un escalón por celda y trimestre, nunca hacia o desde «No», nunca sube.
  - El registro AJU-/CFG- se comparte con la degradación de H5 (una función común), sin cambiar lo que escribe H5.
  - `Evaluador.publicar_estados_h5(as_of)`: entrada `EH5-AAAA-MM-DD` en F6 en cada C5 con el estado de cada PRG H5 abierto, la tasa de hitos cumplidos por celda tipo × H5 (P-42) y el número de PRG en cada estado.
  - Paquete de oportunidades: `x_estados_h5` (ampliación `x_` que el esquema admite) con lo mismo, y el `estado` de cada hito de una vista H5 (enum del esquema: PENDIENTE, CUMPLIDO, FALLADO, NO_RESOLUBLE).
  - Informe técnico: el estado del PRG H5 y de cada hito junto a sus hitos, y una tabla «Pronósticos H5 por hitos» en la sección 8 (historial).
- **No entra:** el informe visual (lenguaje llano; la plantilla no tiene sitio para los estados), el CT-19 del Evaluador (texto del modelo; no se toca `orquestacion.py`, que comparten T-174 y T-175), subir de «Limitado» a «Sí» (exige certificado; ya lo cubre la revisión de certificados), la revisión mensual en tiempo real y el modo sombra.

## Diseño

- **Contratos y esquemas:** ningún esquema cambia. El paquete usa la ampliación `x_` de su raíz y el `estado` de `hito`, ya en el esquema V5.0. Los goldens de contratos no cambian.
- **Estado persistido:** F6 gana dos tipos de entrada, `EH5` y (r02) `REVISION_DM` (`RDM-AAAA-MM`), append-only como el resto. La degradación DM usa los AJU-/CFG- que ya existen; desde la r02 un AJU- puede quedar `ANULADO` y un CFG- de P-31 revertirse (`revierte_a`). F10 no cambia de forma.
- **Números (ninguno nuevo):**
  - muestra mínima: `evaluacion.min_calibrar` (30; Anexo A, «Muestra mínima para calibrar»; regla 5 de F6: sin 30 resueltos ninguna recalibración);
  - nivel de significación: `evaluacion.alfa_holm` (0,10; Anexo A, certificado, coherente con el IC 90 %), sin corrección de Holm porque degradar endurece;
  - pérdida y h de DM-HLN: Brier y la h de `evaluar_celda` por defecto (los del certificado, `_DEFECTO_CELDA`).
- **Falla cerrado:** sin muestra, sin p calculable o con p > α no se degrada; nunca se escribe hacia o desde «No»; un error de la degradación DM no tumba el C5 (incidencia en HA, como la fiabilidad de fuentes).
- **Decisiones `[PROPUESTO]`** (INC-T173-01 en `docs/incidencias.md`): el α y la n mínima de 12.2 no figuran en el Anexo A; el prefijo `EH5-` de F6; la publicación en el paquete por `x_estados_h5`.

## Riesgos

| Riesgo | Consecuencia | Mitigación |
| --- | --- | --- |
| La degradación DM se dispara en los ciclos mock existentes | Cambia la tabla del ciclo siguiente y rompe pruebas antiguas | La suite completa al final; en los datos sintéticos actuales ninguna celda llega a 30 resueltos con pérdida significativa (se comprueba) |
| Compartir el registro AJU-/CFG- cambia la degradación de H5 | Regresión en PB-64 y en T-53/T-65 | Las pruebas existentes de H5 siguen pasando sin cambios |
| `x_estados_h5` con cifras que el informe técnico no repite igual | R7 / cifras incoherentes entre entregables | El técnico se construye del mismo `paquete["x_estados_h5"]` |
| Conflicto con T-174/T-175 en `redaccion.py` | Merge más difícil | Cambios en dos puntos pequeños (hitos y sección 8) |

## Criterios de aceptación (binarios)

1. CA-1: con RF × H2 «Sí» y 35 pronósticos resueltos que pierden frente a la referencia con DM-HLN p ≤ α, el C5 escribe un AJU- de P-31 (SI → LIMITADO) en F6 con la evidencia DM-HLN (estadístico, p, n, h, α) y un CFG- de P-31 con esa celda en «Limitado» (más el de P-30) en F10.
2. CA-2: no se degrada con n < `min_calibrar`, con p > α, con la celda ya «Limitado» o «No» (ningún cambio hacia o desde «No»), en H5, ni dos veces en el mismo trimestre; con pronósticos que ganan a la referencia tampoco.
3. CA-3: tras la degradación, el ciclo siguiente lee RF × H2 como «Limitado» (tabla vigente) y G3 (HT-09) no bloquea por eso.
4. CA-4: cada C5 con H5 abiertos escribe en F6 una entrada `EH5-` con el estado de cada PRG H5 abierto (los tres estados), la tasa por celda tipo × H5 y el recuento por estado.
5. CA-5: el paquete de oportunidades lleva `x_estados_h5` con lo mismo que la entrada de F6 del corte, valida contra su esquema, y los hitos de una vista H5 llevan su `estado`.
6. CA-6: el informe técnico muestra el estado de cada PRG H5 con sus hitos y la tabla de pronósticos H5 por hitos en la sección 8.
7. CA-7: las pruebas existentes de H5 (T-53, T-65, PB-64) pasan sin cambios; suite de A ≥ 607, ruff ≤ 2813, mypy A ≤ 109.
8. CA-8: `tests/mapa_plan_pruebas.json` cita las pruebas nuevas y las evidencias regeneradas dan PB-50 y PB-64 «Superada» o con lo que falte motivado.

**Ronda r02 (QA r01 NO APTO; hallazgos en `qa.md`, los cuatro se corrigen aquí):**

9. CA-9 (H-01): la muestra es la de PA-03: con una sola fecha de resolución (§4), con una historia buena y una semana mala (§4b, §12), sin fechas, con menos de 10 conglomerados o con n ≥ 30 y n_eff < 30, no se degrada; la DM-HLN va sobre las medias por conglomerado y la evidencia lleva n_eff y conglomerados.
10. CA-10 (H-02): si una escritura en F10 falla, el AJU- queda ANULADO, el CFG- de P-31 ya escrito se revierte y el reintento (mismo mes y trimestre) degrada (§10).
11. CA-11 (H-03): la degradación solo corre en la revisión mensual (primer C5 del mes, registro RDM-) y con Holm entre las celdas de la misma revisión que pueden bajar; tasas medidas con `r01_tasa_falsa.py` y `r02_tasa_falsa.py`.
12. CA-12 (H-04): `test_fase4_huecos.py` tiene la variante de PB-33 con la degradación DM neutralizada y la afirmación original sobre las vistas H3.

## Plan de pruebas

| Prueba | Tipo | Criterio |
| --- | --- | --- |
| `test_t173.py::test_pb50_rf_h2_pierde_con_significacion_y_baja_a_limitado` | nominal | CA-1 |
| `test_t173.py::test_pb50_*` límites (n = 29, p > α, ya Limitado, No, H5, mismo trimestre, gana) | límite · fallo cerrado | CA-2 |
| `test_t173.py::test_pb50_el_ciclo_siguiente_lee_limitado_y_g3_no_bloquea` | integración (ciclo mock) | CA-3 |
| `test_t173.py::test_pb64_c5_publica_los_estados_h5_en_f6` | nominal | CA-4 |
| `test_t173.py::test_pb64_paquete_y_tecnico_publican_los_estados_h5` | integración (ciclo mock) | CA-5, CA-6 |
| Suites de H5 existentes y suite completa | regresión | CA-7 |
| Mutantes propios (umbral, sentido de la cola, «No», publicación) | mutación | CA-1..CA-5 |

## Scripts

- `.docs/scripts/evidencias_plan_a.py --ejecutar` (evidencias del plan).
- `.docs/scripts/nuevo_ticket.sh` (apertura).

## Registro

- 2026-11-17 · ABIERTO · creado con nuevo_ticket.sh
- 2026-11-17 · PLANIFICADO · claude · plan con CA-1..CA-8
- 2026-11-17 · EN CURSO · claude · implementación y pruebas (16 nuevas, 14 mutantes muertos)
- 2026-11-17 · EN QA (r01) · claude · commit local «wip local: T-173», sin push; PB-50 y PB-64 «Superada»
- 2026-11-17 · EN CURSO (r02) · claude · QA r01 NO APTO (H-01 alta, H-02 y H-03 medias, H-04 baja); rebase sobre origin/develop (T-165 y T-171)
- 2026-11-17 · EN QA (r02: QA r01 NO APTO) · claude · los cuatro hallazgos corregidos; commit local, sin push
- 2026-11-17 · EN QA (ronda de cierre de la QA r02) · claude · QA r02 APTO con dos bajos: H-05 (versión de la reversión) y H-06 (familia de Holm fija, decisión del operador por delegación del 17-11-2026, opción b) corregidos; commit local, sin push
- 2026-11-17 · CERRADO · claude (revisor) · QA r02 APTO tras la ronda de cierre: H-05 y H-06 corregidos (`qa.md`, «Ronda de cierre»); el gate 12/12, al integrar en develop
