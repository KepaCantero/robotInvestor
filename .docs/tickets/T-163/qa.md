# T-163 · QA independiente

- **Revisor:** subagente de Claude sin contexto de la implementación (regla `compartida/2026-11-12_claude-puede-hacer-qa`) · **Ronda:** r01 · 16-11-2026
- **Copia revisada:** worktree desechable en la instantánea `e7c8781` (T-163 sobre T-160), con `.venv` enlazado. Sin red ni gasto.
  Opinión formada con el plan, los hallazgos de T-160 y el código antes de leer `analisis-tecnico.md`.

## Reproducción desde limpio

```bash
cd bloque_a/11_Ejecutor
../../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_t163_hallazgos_t160.py tests/test_t160_reejecucion_certificado.py
../../.venv/bin/python -m pytest -q -p no:cacheprovider ../../.docs/tickets/T-160/revisores/r01_01_ataques.py      # 1 falla por diseño (H-05)
../../.venv/bin/python -m pytest -q -p no:cacheprovider -rf ../../.docs/tickets/T-163/revisores/r01_01_ataques.py  # 2 fallan a propósito: H-01, H-02
../../.venv/bin/python tests/goldens_ct.py
../../.venv/bin/python -m pytest -q -p no:cacheprovider                                    # suite completa, en segundo plano
cd ../..
for g in refs_vivas secrets_scan nfc_check corpus_integridad; do .venv/bin/python tools/$g.py; done
.venv/bin/ruff check --output-format=concise bloque_a/11_Ejecutor bloque_a_forex/11_Ejecutor bloque_b/11_Ejecutor | wc -l
.venv/bin/mypy --ignore-missing-imports --no-error-summary bloque_a/11_Ejecutor/bloque_a | wc -l
.venv/bin/python .docs/scripts/evidencias_plan_a.py && .venv/bin/python .docs/scripts/evidencias_plan_a.py --pb PB-32
.venv/bin/python .docs/tickets/T-160/revisores/r01_02_sin_fechas_como_antes.py <carpeta vacía>          # base HEAD~1 (T-160)
# mutantes, cada uno en su copia desechable con bloque_a/ entero y .docs/tickets/T-160 y T-163:
.venv/bin/python .docs/scripts/mutantes_revisor_ampliado.py .docs/tickets/T-160/revisores/r01_03_mutantes.py <copia «qa31_…_mut»> \
  tests/test_t163_hallazgos_t160.py ../../.docs/tickets/T-160/revisores/r01_01_ataques.py -k "not auditoria_ct10_posterior"
.venv/bin/python .docs/tickets/T-163/mutantes_t163.py <copia «…_mut»>
.venv/bin/python .docs/tickets/T-163/revisores/r01_02_mutantes.py <copia «…_mut»>
```

| Comprobación | Resultado |
| --- | --- |
| `test_t163_hallazgos_t160.py` (48) y `test_t160_reejecucion_certificado.py` (16) | 64 superadas |
| Suite completa de A (una vez) | **7133 superadas y 2 omitidas** en 1 h 13 min, sin fallos (tampoco `test_t102_filtro`) |
| `r01_01_ataques.py` de T-160 | 34 superadas, las `test_h0*` incluidas; falla solo `test_una_auditoria_ct10_posterior_que_no_coincide_no_impide_la_aprobacion`, **por diseño**: documentaba H-05, y ahora CT-04 rechaza con «una re-ejecución CT-10 posterior de CALC-2026-0001 no coincide (CALC-2026-0003)» |
| `r01_02_sin_fechas_como_antes.py` de T-160 (HEAD~1 = T-160 frente a HEAD = T-163) | `servir` (12 casos), `f_fc_eval` directo y `evaluadas`: **iguales**. `certs` difiere y el script sale con 1, pero solo por el campo nuevo `huella_entradas`: quitándolo, el CERT- es idéntico (comprobado aparte con la misma sonda) |
| Mutantes de T-160 (`r01_03_mutantes.py`, 26, con las pruebas nuevas y r01_01 sin la de H-05) | 24 muertos (**M12 y M17 mueren ahora**), M13 y M14 equivalentes (los de la QA de T-160), ninguno sin aplicar |
| Mutantes de T-163 (`mutantes_t163.py`, 15) | 14 muertos; T14 equivalente (con el suelo en 2, `True` y `False` ya quedan por debajo; T15 cubre el suelo) |
| Mutantes del revisor (`r01_02_mutantes.py`, 12) | primera pasada: 8 muertos, N11 equivalente y N03, N04 y N07 vivos; con sus pruebas añadidas a r01_01, `--solo N03,N04,N07`: los tres muertos (detalle abajo) |
| Goldens (`tests/goldens_ct.py`) | coinciden |
| Gates ligeros | `refs_vivas`, `secrets_scan`, `nfc_check` en verde; corpus: 695 archivos coinciden |
| Cuotas | ruff **2816** (≤ 2816; = `tools/cuotas.txt`); mypy A **109** (≤ 109) |
| Plan de pruebas | mapa: 67 pruebas del plan, 196 citadas y todas existen; `--pb PB-32`: **Superada**; ningún fichero cambia |
| Decisiones del operador | H-02 decidido por delegación y anotado en INC-T160-01 y en `Decisiones_del_operador_Bloque_A.md` (§1 y fila de T-160 en §4); no hay decisiones nuevas en silencio |

## Lo que se atacó (r01_01_ataques.py, 31 casos)

| Ataque | Resultado |
| --- | --- |
| PROPUESTO falso que copia la `huella_entradas` del legítimo con un soporte propio (otras entradas, mejores cifras) y su CT-10 | rechazado («no son las mismas») |
| Copia del legítimo que cita la CT-10 de otro soporte | rechazada («no re-ejecuta») |
| Copia exacta del legítimo, con otro id, en los dos órdenes: en un lote (no se escribe nada), por `Bloque.decision` uno a uno (entra solo el legítimo) | correcto |
| Copia escrita con `_seq: 0` y `_fecha` antiguos | el almacén los pisa; la copia no se cuela como «primera» |
| RC reordenado en disco (soporte y CT-10 intercambiados) | `verificar_integridad` da False y nada devuelve el certificado |
| Copia que cita la CT-10 de un certificado ya revocado | rechazada («ya sostiene …»): la exclusividad sobrevive a la revocación |
| Copia exacta escrita justo antes que el legítimo (entre la comprobación y la escritura) | «gana» la exclusividad, pero con las mismas cifras, soporte y CT-10: no hay ganancia de fondo |
| Dos métodos de una misma clase × horizonte con las mismas entradas | cada uno con su soporte; cruzarlos no vale |
| Dos horizontes con las mismas entradas | **H-02** |
| Cifras de la muestra efectiva o del Brier de referencia cambiadas; dos PROPUESTO válidos de una celda en un lote | rechazados (estas pruebas matan N03, N04 y N07) |
| CT-10 NO del Auditor y después una SI de **otro** cálculo; o una SI del **mismo** soporte posterior a la NO; o una CT-10 fallida (ERROR_REEJECUCION) | el certificado que cita la CT-10 anterior a la NO no entra en vigor / deja de estar vigente |
| VIGENTE escrito a mano, por el ciclo completo | revocado en C5; ningún PRG con `prob_publicada` ni `certificado_ref`; ninguna opción con `prob`; CT-05 lleva `"certificados": []` |
| VIGENTE a mano con C5 caído (la revisión lanza; el ciclo sigue en modo degradado) | no se revoca, pero tampoco publica: la síntesis, HT-09, `_prospectiva`, CT-05, el backtest y el diseño V6 leen `certificados_vigentes` (revisado en el código; C6 no publica probabilidades: arrastra la del PRG y la síntesis vuelve a decidir con los certificados vigentes) |
| Dos revisiones seguidas con un VIGENTE sin re-ejecución | una sola CERT_REVOCACION; la segunda revisión no hace nada (idempotente) |
| Segundo certificado válido por sí mismo de una celda con un VIGENTE legítimo | CT-04 lo rechaza («ya tiene un certificado VIGENTE»); la revisión no propone otro |
| `min_conglomerados` `np.bool_(True)`, `np.float64(2.0)`, `Decimal(2)`, NaN, ∞, `2+0j`, `"2"` | rechazados; `np.int8(2)`, `np.uint64(3)` y 10⁶ se aceptan |
| PROPUESTO falso desde cero con su propio soporte (entradas inventadas) y su CT-10 | **entra en vigor**: es el límite declarado (no se ata el soporte a F4); ver H-01 |
| PROPUESTO falso con el soporte y la CT-10 de las entradas **reales** de una celda que no certifica | **H-01** |

## Mutantes del revisor (r01_02_mutantes.py)

| Mutante | Qué rompe | Resultado |
| --- | --- | --- |
| N01 | la exclusividad la gana el último CERT- que cita la re-ejecución | muerto |
| N02 | H-05 cuenta también las NO anteriores a la CT-10 citada | muerto (`test_h05_un_vigente_cuyo_soporte_…`) |
| N03, N04 | CT-04 no compara la muestra efectiva / el Brier de referencia | **vivos con las pruebas del ticket** (ninguna altera esos campos); mueren con `test_cifras_que_las_pruebas_del_ticket_no_alteran_…` de r01_01 (H-03) |
| N05 | el ayudante `certificado_con_reejecucion` escribe un certificado que no pasa | muerto, pero 2 de las 7 pruebas adaptadas siguen pasando (H-03) |
| N06 | el VIGENTE revocado no se vuelve a proponer en la misma revisión | muerto |
| N07 | CT-04 deja aprobar en un lote dos PROPUESTO de la misma celda | **vivo con las pruebas del ticket** (regla anterior a T-163, sin prueba); muere con `test_un_lote_con_dos_propuestos_validos_…` de r01_01 (H-03) |
| N08 | H-05 solo mira las CT-10 del Evaluador | muerto |
| N09, N10 | el Evaluador acepta un mínimo de 1; FC-EVAL-001 valida el mínimo también sin fechas | muertos |
| N11 | no se comparan las huellas de la CT-10 con las del soporte | vivo, **equivalente**: el Motor escribe la REEJECUCION con los datos que re-ejecutó y, si no son los del soporte, ya da NO (DATOS_DISTINTOS); solo cambia algo con una REEJECUCION forjada en el RC (AG-13) |
| N12 | la revocación de un VIGENTE sin re-ejecución solo se informa, no se escribe | muerto |

## Criterios de aceptación

| Criterio | Cumple | Evidencia |
| --- | --- | --- |
| CA-1 (H-01) | sí, con H-01 de esta ronda | `test_h01_*` del ticket; r01_01 (huella imitada, CT-10 de otro soporte, copias, orden, revocado); T01–T06, T11, T12, N01, N03, N04 |
| CA-2 (H-05) | sí | `test_h05_*`; r01_01 (SI de otro cálculo, SI del mismo soporte posterior a la NO, CT-10 fallida); T04, N02, N08 |
| CA-3 (H-02) | sí | `test_h02_*`; r01_01 (ciclo, CT-05, C5 caído, idempotencia, segundo certificado); T07–T09, N06, N12 |
| CA-4 (H-03) | sí | `test_h03_*`; T10 |
| CA-5 (H-04) | sí | `test_h04_*`; r01_01 (tipos raros de numpy y de Python); T13, T15, N09, N10 |
| CA-6 (H-06) | sí | M12 y M17 muertos; los 26 de r01_03 aplican y solo viven M13 y M14 (equivalentes) |
| CA-7 | sí | r01_01 de T-160: 34 superadas; solo falla, por diseño, la que documentaba H-05 |
| CA-8 | sí | suite de A 7133 superadas sin fallos; goldens, gates ligeros, ruff 2816, mypy A 109, PB-32 «Superada» |

Pruebas de otros tickets (punto 7 del encargo): en `test_fase4_huecos.py` (PB-33 ×2, PB-32), `test_t53_evaluacion_y_almacen.py`,
`test_t66_evaluacion.py` y `test_t87_datos.py` solo cambia la línea que escribe el certificado (más el orden de imports y cuatro
`noqa` sin uso); ninguna aserción cambia. Las de PB-33 afirman «deterioro» en el motivo y las de publicación exigen la
probabilidad, así que no pasan por la vía nueva. Dos sí quedan más flojas: H-03.

## Hallazgos

Ningún PROPUESTO falso hecho con los permisos de escribir en F6 (los de H-01 de T-160: reutilizar o imitar el soporte, la CT-10 o
las cifras de un certificado legítimo) entra en vigor, y ningún VIGENTE sin re-ejecución da una probabilidad certificada por ningún
camino. Lo que queda exige hacer el trabajo del propio Evaluador: pedir al Motor un FC-EVAL-001 y su CT-10 como AG-20 y escribir en
F6 como AG-20. Eso solo lo hace código del ejecutor: CT-04 del Broker solo lleva identificadores, y los agentes LLM no eligen las
fichas que se sirven ni su solicitante.

| ID | Gravedad | Cómo reproducirlo | Esperado / obtenido | Corrección sugerida | Estado |
| --- | --- | --- | --- | --- | --- |
| H-01 | media | Desde `bloque_a/11_Ejecutor`: `../../.venv/bin/python -m pytest -q -p no:cacheprovider ../../.docs/tickets/T-163/revisores/r01_01_ataques.py -k "h01 or desde_cero"`. Con una celda de habilidad débil (frecuencia real 0,5 + 0,6·(p − 0,5), 150 PRG): BSS 0,053, IC [−0,064; 0,16], ECE 0,013 | `motivo_sin_reejecucion` (CT-04 y `certificados_vigentes`) ata el CERT- a su soporte, pero no comprueba que el soporte **cumpla el criterio** del certificado (n ≥ `min_certificar`, n_eff, extremo inferior del IC > 0, ECE ≤ `ece_max`, ECE < q90 del nulo y, como condición necesaria de Holm, p de DM ≤ α; la p sí está en el `payload` del soporte, así que no guardarla en el CERT- no es el hueco: lo es que nadie la mira) ni que sus entradas sean los PRG de la celda (límite declarado). Un PROPUESTO con el soporte y la CT-10 de las entradas reales de esa celda **entra en vigor** por CT-04 y la revisión **lo mantiene** VIGENTE, porque solo revoca con BSS ≤ 0 o ECE ≥ `ece_revocacion`: publicaría probabilidades sin habilidad demostrada. No es más grave porque hace falta lo mismo que para el falso desde cero del límite declarado | En `motivo_sin_reejecucion`, aplicar `ev.criterio_certificado` al `payload` del soporte con `min_certificar` y `ece_max` y exigir p ≤ `alfa_holm`; exigir `solicitante` AG-20 también en el soporte; a la deuda, atar las entradas del soporte a los PRG resueltos de la celda (recalcular la huella de `_entradas_celda` a la fecha del soporte). El ayudante de `conftest.py` usa n = 60 < 100 y habría que subirlo | abierto |
| H-02 | baja | `-k h02` en el mismo script | Dos celdas de la misma clase y método en H2 y H3 con las mismas p, o, referencia y fechas: la clave de la caché del Motor no lleva el horizonte, la de H2 recibe el soporte de H3 (`calc_id` del original), su borrador no pasa («CALC-2026-0001 no es un servicio FC-EVAL-001 de la celda RF\|H2») y queda una incidencia Material en cada revisión: **H2 nunca se certifica** mientras sus entradas coincidan. Falla cerrado (viene de la caché de T-119 y el borrador de H-03 lo hace visible) | Que el Evaluador ponga `horizonte` en los parámetros de la petición, como `metodo`, o que la clave de la caché del Motor lleve `clase` y `horizonte` de la petición | abierto |
| H-03 | baja | `.venv/bin/python .docs/tickets/T-163/revisores/r01_02_mutantes.py <copia «…_mut»> --solo N03,N04,N05,N07` | (a) Con el ayudante roto (N05), `test_t53…::test_umbral_de_revocacion_ece_sale_de_la_configuracion` y `test_t66_evaluacion.py::test_pa10_revocar_y_retirar_siguen_siendo_automaticos` siguen pasando: afirman que se revoca, no por qué, y ahora el certificado se revocaría igual por no tener re-ejecución. (b) Ninguna prueba del ticket altera la muestra efectiva ni el Brier de referencia del CERT- (N03 y N04 viven) ni lleva a CT-04 un lote con dos PROPUESTO de una celda (N07 vive, regla anterior a T-163) | Afirmar «deterioro» en el motivo (o `vigentes_sin_reejecucion == {}`) en esas dos pruebas; llevar al fichero del ticket las tres pruebas de r01_01 que matan N03, N04 y N07 | abierto |

Los scripts de esta ronda están en `revisores/`, en este orden: `r01_01_ataques.py` (desde `bloque_a/11_Ejecutor`; las `test_h01_*` y
`test_h02_*` fallan a propósito mientras H-01 y H-02 sigan abiertos) y `r01_02_mutantes.py` (desde la raíz, con una copia «…_mut»).

## Veredicto

**APTO** · Se cumplen los ocho criterios. CT-04 ata cada certificado a su re-ejecución (método, entradas, orden, exclusividad,
cifras y CT-10 posteriores de cualquier solicitante) y resiste los ataques con permisos de escribir en F6: huella imitada, CT-10 de
otro soporte, copias en los dos órdenes, `_seq` manipulado, RC reordenado y celdas que comparten entradas. Ningún VIGENTE sin
re-ejecución coincidente da probabilidad certificada por el ciclo, CT-05, los entregables ni la síntesis, ni con C5 caído. La
revocación es idempotente y CT-04 sigue impidiendo un segundo certificado por celda. La emisión directa pasa el borrador por la
misma comprobación. FC-EVAL-001 valida el mínimo, con el suelo de 2 (una cota de validez, ya en el Evaluador, que ahora es una sola
constante; el valor efectivo es el 10 de la configuración). M12 y M17 mueren. La suite, los goldens, los gates ligeros, las cuotas
y PB-32 están en verde. No hay hallazgos críticos ni altos. H-01 es media: el PROPUESTO falso que entra exige generar su soporte y su
CT-10 en el Motor como AG-20, igual que el límite declarado del ticket. H-02 y H-03 son bajos. Los tres pasan a la deuda técnica con
su ID. Por encargo, este revisor no cierra el ticket ni toca la deuda: lo hace la sesión coordinadora.
