# T-121 · Bloque A: hallazgos abiertos de la QA r01 de T-118 (fecha de corte en la Fase 1, CT-10 y menores)

| Campo | Valor |
| --- | --- |
| Estado | EN QA |
| Pieza | bloque_a (11_Ejecutor, motor) |
| Planifica · implementa · QA | claude (un agente, en una copia de trabajo propia, rama `t119r02`, encima de la r02 de T-119) · el mismo · un revisor que no implementó |
| Aprobación del operador | No necesaria: corrige hallazgos de una QA. Las decisiones abiertas las toma el agente con la opción más prudente y las apunta como `[PROPUESTO]` en INC-T121-01 (el operador lo pidió así) |
| Deuda técnica | T-121 en `sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md` |

## Objetivo

Cerrar los seis hallazgos que la QA r01 de T-118 dejó abiertos (`.docs/tickets/T-118/qa.md`, «Hallazgos»), antes del modo sombra (Fase 5): que ninguna ficha de la Fase 1 use información posterior a la fecha de corte y que una auditoría CT-10 no deje pasar un error real del cálculo original.

## Alcance

**Entra:**

| Hallazgo | Gravedad | Qué se corrige |
| --- | --- | --- |
| H-04 | media | Las 14 fichas de la Fase 1 que servían datos en línea posteriores a `ent["fecha_corte"]` (FON-DISC, FON-FLOW, FON-LEV, IDX-CONC, IDX-ERP, IDX-REL, MON-FIX, MON-REAL, MON-YLD, TCV-BEI, TCV-CDS, TCV-SLOPE, TCV-TP y TCV-VIXTS) los rechazan, con el patrón `_corte` / `_hasta_corte` de la Fase 2. También las fechas observadas de MON-EXP-001 e IDX-REB-001 (la fecha de los datos, las decisiones, el anuncio, los activos indexados y los eventos comparables) |
| H-01 | media | CT-10: con la configuración guardada en el artefacto, un resultado que difiere es ERROR_ORIGINAL aunque la vigente haya cambiado; CONVENCION_DISTINTA solo si falta esa configuración o no se ha podido reproducir |
| H-02 | baja | Ninguna excepción escapa de `Motor.servir` por un texto que no se puede escribir en UTF-8, un valor que no es JSON o unos argumentos `solicitante`, `run_id` y `msg_id` raros (cubre también H-07 de la QA r01 de T-119) |
| H-03 | baja | `reejecutar` deja su entrada REEJECUCION si los datos del artefacto ya no se pueden resolver o el artefacto está alterado |
| H-05 | baja | La cota de 520 observaciones de REG-HMM-001 sale de `horizontes.H5` |
| H-06 | baja | Pruebas que matan los mutantes M05, M38, M50, M68 y M78 de `.docs/tickets/T-118/revisores/r01_07_mutantes.py` |

**No entra:** la observación de coste (BT-PBO-001 tarda 73 s, no 52; es una medida, no un defecto); el Catálogo (corpus congelado); los `qa.md`, la deuda técnica, el diario y la memoria; la QA.

## Diseño

- **Contratos CT afectados:** ninguno cambia de forma. CT-09 rechaza peticiones que antes servía (datos posteriores al corte, campos que no se pueden escribir); CT-10 cambia la categoría en un caso (H-01) y registra lo que antes escapaba (H-03).
- **Estado persistido:** no cambia de forma. Las entradas REEJECUCION de H-03 usan los campos y la categoría (ERROR_REEJECUCION) que el esquema del Registro V2.0 ya tiene.
- **Números y su origen:** ningún número nuevo. La cota de REG-HMM-001 es `horizontes.H5` (configuración) en semanas, con 52 semanas y 12 meses por año (calendario, no parámetro). Las demás reglas no tienen números.
- **Cómo falla cerrado:** un dato posterior al corte, una fecha de corte que no es una fecha o un campo que no se puede escribir dan RECHAZADO con una entrada en RC, antes de calcular. Una re-ejecución que no llega a la ficha da `coincide` NO.
- **Decisiones del operador usadas como `[PROPUESTO]`:** INC-T121-01 (`docs/incidencias.md`).

## Riesgos

| Riesgo | Consecuencia | Mitigación |
| --- | --- | --- |
| Un dato del día del corte o una fecha futura por naturaleza rechazados | Peticiones legítimas rechazadas; cifras servidas que cambian | Se compara por día; las reuniones, la efectividad anunciada, los vencimientos y los nodos de una curva no se comparan; prueba de que los 42 casos de control de las 14 fichas dan el mismo resultado con el corte en su última fecha que sin corte |
| Los casos de control llevan datos sintéticos hasta 2029-12-31 | Las pruebas que servían con el corte de 2026-11-12 se rechazan | `test_t106_motor.py` y `test_t106_r03.py` ponen el corte en la última fecha de los datos de control |
| CT-10 culpa a un original bueno tras un cambio de `por_defecto.yaml` | Auditoría injusta | CONVENCION_DISTINTA cuando la sección guardada no trae todas las claves del fichero y su huella ha cambiado |
| Máquina compartida | Pruebas lentas | Solo las pruebas del módulo mientras se trabaja; la suite completa de A, una vez |

## Criterios de aceptación (binarios)

1. CA-1 (H-04): en las 14 fichas, con el corte en la víspera de la última fecha observada de cada caso de control, RECHAZADO; con el corte en esa fecha, el mismo resultado que sin corte. Campo a campo, cada fecha observada (también las de los bloques opcionales) un día después del corte se rechaza. El dato del día del corte, también con hora, se sirve. Las fechas futuras por naturaleza no se rechazan. `r01_01_h09_fecha_corte.py` (bloque 2) no lista ninguna de las 14.
2. CA-2 (H-01): cifra alterada y configuración registrada completa ⇒ ERROR_ORIGINAL, con la configuración vigente igual, con la clave leída cambiada, con otra clave de la misma sección cambiada y con `por_defecto.yaml` cambiado si el valor guardado lo cubre. Sin configuración registrada o con una sección que no se ha podido reproducir ⇒ CONVENCION_DISTINTA. `r01_03_h11_ct10_configuracion.py` bloque 5 en verde.
3. CA-3 (H-02): `r01_05_h13_h14_fuzz.py` bloque 1 sin escapes; un sustituto Unicode suelto, un valor que no es JSON y unos argumentos raros dan RECHAZADO con una sola entrada en RC.
4. CA-4 (H-03): `r01_05_h13_h14_fuzz.py` bloque 3: solo escapan las cuatro excepciones declaradas; el resto deja una entrada REEJECUCION (NO / ERROR_REEJECUCION).
5. CA-5 (H-05): la cota de REG-HMM-001 sigue a `horizontes.H5` (`r01_04_h12_configuracion.py`).
6. CA-6 (H-06): `r01_07_mutantes.py --solo M05,M38,M50,M68,M78`: ninguno vivo.
7. CA-7: cada corrección tiene un mutante que alguna prueba mata (`revisores/impl_mutantes.py`); los casos de control de las 80 fichas siguen superados; las pruebas de A suben; ruff (2902) y mypy (109) no suben; corpus, referencias, secretos y NFC en verde; goldens de la Fase 3 sin cambios.

## Plan de pruebas

| Prueba | Tipo | Criterio |
| --- | --- | --- |
| `tests/test_t121_hallazgos.py::test_h04_*` (42 casos, 14 fichas campo a campo, 11 bloques opcionales, día del corte con hora, segunda vía de TCV-TP, fechas futuras por naturaleza) | Límite, fallo cerrado y regresión | CA-1 |
| `tests/test_t121_hallazgos.py::test_h01_*` | Regresión | CA-2 |
| `tests/test_t121_hallazgos.py::test_h02_*` | Fallo cerrado | CA-3 |
| `tests/test_t121_hallazgos.py::test_h03_*` | Fallo cerrado | CA-4 |
| `tests/test_t121_hallazgos.py::test_h05_*`; `test_t118_hallazgos.py::test_h12_las_cotas_de_s_y_p_salen_de_la_configuracion_por_defecto` (adaptada) | Regresión | CA-5 |
| `tests/test_t118_hallazgos.py::test_h09_m05_*`, `test_h10_m38_*`, `test_h11_m50_*`, `test_h12_m68_*`, `test_h13_m78_*` | Regresión | CA-6 |
| `.docs/tickets/T-121/revisores/impl_mutantes.py` | Mutación | CA-7 |
| Scripts del revisor de T-118 `r01_01`, `r01_03`, `r01_04`, `r01_05`, `r01_07` | Reproducción | CA-1 a CA-6 |
| `test_t119_*`, `test_t118_hallazgos.py`, `test_t106_*`, `test_fase1_*`, `test_fase2_*`, `test_t112_motor.py`, `test_integracion.py`, `test_fase3_goldens.py`, `tests/goldens_ct.py`, suite completa de A, ruff, mypy y los cuatro gates de árbol | Regresión y gate | CA-7 |

## Scripts

- `.docs/scripts/nuevo_ticket.sh` (creó este ticket).
- `.docs/tickets/T-121/revisores/impl_mutantes.py`: 55 mutantes de las correcciones, en una copia desechable.

## Registro

- 2026-11-14 · ABIERTO · creado con nuevo_ticket.sh
- 2026-11-14 · EN CURSO · claude · retomado de un punto de guardado de otra sesión (commit `0790ce8`, con la mayor parte del código); terminado encima en la rama `t119r02`
- 2026-11-14 · EN QA · claude · los seis hallazgos corregidos, con 116 pruebas nuevas en `test_t121_hallazgos.py` y 7 en `test_t118_hallazgos.py`; 55 mutantes de las correcciones, ninguno vivo; decisiones en INC-T121-01; detalle en `analisis-tecnico.md` y `pruebas.md`. Sin `git push`: commits locales en la rama `t119r02`
