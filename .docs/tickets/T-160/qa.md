# T-160 · QA independiente

- **Revisor:** subagente de Claude sin contexto de la implementación (regla `compartida/2026-11-12_claude-puede-hacer-qa`) · **Ronda:** r01 · 16-11-2026
- **Copia revisada:** worktree desechable en el commit `6f3eb2b` (instantánea con T-159 y T-160), con `.venv` enlazado. Sin red ni gasto.
  Opinión formada con el plan y el código antes de leer `analisis-tecnico.md`.

## Reproducción desde limpio

```bash
cd bloque_a/11_Ejecutor
../../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_t160_reejecucion_certificado.py tests/test_t66_evaluacion.py tests/test_t66_propuestas.py
../../.venv/bin/python -m pytest -q -p no:cacheprovider -s ../../.docs/tickets/T-160/revisores/r01_01_ataques.py   # 4 fallan a propósito: H-01 a H-03
../../.venv/bin/python tests/goldens_ct.py
../../.venv/bin/python -m bloque_a.herramientas.verificador_ids
../../.venv/bin/python -m pytest -q -p no:cacheprovider                                    # suite completa, en segundo plano
cd ../..
.venv/bin/python .docs/tickets/T-160/revisores/r01_02_sin_fechas_como_antes.py <carpeta vacía>        # base HEAD~1
.venv/bin/python .docs/tickets/T-160/revisores/r01_03_mutantes.py <copia «qa31_…_mut» con bloque_a/ entero> --scripts
.venv/bin/python .docs/scripts/evidencias_plan_a.py --ejecutar
```

| Comprobación | Resultado |
| --- | --- |
| `test_t160_reejecucion_certificado.py` (16), `test_t66_evaluacion.py`, `test_t66_propuestas.py` | pasan |
| Suite completa de A (una vez, máquina cargada) | 6752 superadas, 2 omitidas y 1 fallo en 1 h 15 min (carga ~10): `test_t102_filtro.py::test_r05_h37_sufijo_en_tiempo_lineal`, una prueba de tiempo (2,68 s frente a un tope de 2 s). Repetida sola dos veces: pasa una y falla otra con carga 11,8. Es de carga; ni la prueba ni el código que prueba cambian en la instantánea. Una primera ejecución se cortó por el `timeout` del revisor al 99 % sin ningún fallo hasta ahí |
| FC-EVAL-001 sin `fechas` frente a HEAD~1 (r01_02, cada versión en su proceso con su paquete) | `Motor.servir` en 12 combinaciones (n = 5 a 150, con y sin `p_ref`, tasa base, nivel, semilla, h, y `min_conglomerados` sin fechas) y `f_fc_eval` directo: **idénticos**. Revisión de dos celdas sembradas: `evaluadas` idénticas y el CERT- con las mismas cifras (quitando los cuatro campos nuevos); un certificado antes y uno después |
| Tolerancia y su origen | 1e-8 de `servicio.IMPLEMENTADAS["FC-EVAL-001"]`, la misma que aplica CT-10; la ficha del Catálogo V5.0 dice «1e-8 en métricas; 1e-6 en IC con la misma semilla» y AUD-REX-001 «las de la ficha original» (comprobado en el texto por r01_01). Usar 1e-8 también en el IC es más estricto: falla cerrado. El Anexo A y la configuración no fijan otra |
| Materialidad de extremo a extremo (r01_01) | Con `evaluacion.ece_max` a una décima de la tolerancia por encima del ECE real: con CT-10 DENTRO_TOLERANCIA **no** certifica (motivo «material», ECE); con coincidencia exacta, sí. Cifras del Motor dentro de tolerancia + CT-10 DENTRO_TOLERANCIA: dos pasos de holgura. A 3 × tol: ERROR_ORIGINAL, sin certificado |
| Motor que falla a medias (r01_01) | CT-10 que escribe «SI» en el RC y luego lanza: sin certificado, se reintenta y la revisión siguiente lo propone. `servir` que lanza o devuelve `None`, `[]`, `"SI"`, sin `calc_id`, `calc_id` no texto o REJECTED: sin certificado. Pero véase H-03 |
| CT-04 con propuestas falsas (r01_01) | Rechaza (ValueError, F6 sin cambios, también por `Bloque.decision`): sin campos, con campos de tipo raro (`None`, lista, número, dict, cadena vacía), soporte de otra celda, lote con uno malo, aprobar dos veces. Pero véase H-01 |
| Idempotencia | Dos revisiones seguidas: un solo certificado y ninguna petición nueva al Motor |
| `test_t66_evaluacion.py` | No se debilita: las cuatro pruebas que esperan un certificado reciben un Motor y sus aserciones no cambian. Revisé todas las demás construcciones del Evaluador sin Motor de la suite (`test_t66_evaluacion`, `test_fase4_huecos`, `test_t53_evaluacion_y_almacen`): las que esperan que no haya certificado afirman su motivo (n < 100, n_eff, «IC del BSS None», contaminados) o no llegan a una celda candidata (PB-64: 20 hitos), así que no pasan «por no tener Motor» |
| D-1 | `catalog_version` de RI-TB = `servicio.CATALOG_VERSION`; ningún «4.0» de versión del Catálogo queda en `bloque_a/11_Ejecutor/bloque_a/*.py` (los que quedan son `VERSION` de las copias de HT-02 y HT-07, la versión de metodología por defecto de `sintesis.py` y datos de ejemplo). El verificador ya no da `CATALOG_VERSION_LITERAL` ni `MENCION_OTRA_VERSION_CODIGO`; quedan los dos ERROR del corpus de T-157 (FX-MC10-003 y RF-0123, D-3 y D-4) |
| Evidencias regeneradas en la copia | «194 de 194 pruebas citadas superadas»; 31 Superada · 27 en parte; PB-32 «Superada»; idénticas a las de HEAD salvo la cabecera |
| Goldens | `tests/goldens_ct.py`: coinciden; `test_fase3_goldens.py` en la suite |
| Gates ligeros y cuotas | `refs_vivas`, `secrets_scan`, `nfc_check` en verde; corpus 695 coinciden; ruff 2825 (≤ 2828 del ticket y = `tools/cuotas.txt`), mypy A 109 |
| Mutantes propios (r01_03) | 26: 22 muertos, 2 equivalentes (M13, M14) y 2 vivos reales (M12, M17: H-06) |
| Decisiones `[PROPUESTO]` | En INC-T160-01 y en una fila del §4 de `Decisiones_del_operador_Bloque_A.md`, y la fila T-160 de la deuda; todas endurecen salvo la de dejar los VIGENTE anteriores (H-02) |

## Criterios de aceptación

| Criterio | Cumple | Evidencia |
| --- | --- | --- |
| CA-1 nominal | sí | `test_ca1_…`; r01_01 |
| CA-2 no coincide | sí | `test_ca2_…`; M03 y M25 mueren |
| CA-3 no se puede re-ejecutar | sí | `test_ca3_*`; r01_01 (servir y CT-10 que lanzan, respuestas raras) |
| CA-4 cifras distintas o material | sí | `test_ca4_*`; materialidad de extremo a extremo con un umbral real de la configuración (r01_01); M04 a M13 |
| CA-5 CT-04 | sí, con H-01 | `test_ca5_*`; r01_01 |
| CA-6 PB-32 de punta a punta | sí | `test_ca6_…` |
| CA-7 D-1 | sí | `test_ca7_*`, verificador, M18 |
| CA-8 PB-32 «Superada» | sí | evidencias regeneradas |
| CA-9 regresión y cuotas | sí (salvo la prueba de tiempo por carga) | arriba |

## Mutantes (r01_03)

26 mutantes en una copia desechable de `bloque_a/`, cada uno contra `test_t160_reejecucion_certificado.py`, `test_t66_evaluacion.py`
y `test_t66_propuestas.py` (con -x) y, si vive, contra `r01_01_ataques.py` (sin sus `test_h0*`):

| Mutantes | Qué rompen | Resultado |
| --- | --- | --- |
| M01, M02 | CT-04 no mira la re-ejecución; no se retiran las propuestas sin ella | muertos |
| M03, M25 | una CT-10 «NO» vale; no se mira el «coincide» | muertos |
| M04, M24 | sin la comparación de las cifras con el Motor; cifras siempre «exactas» | muertos (M24, por r01_01) |
| M05 | tolerancia un millón de veces más ancha | muerto |
| M06 a M11 | sin materialidad, pasos siempre 0, holgura sin acumular, sin mover el ECE, n_eff o la p de DM | muertos |
| M12 | la materialidad no mueve el q90 del nulo | **vivo** (H-06) |
| M13 | la materialidad no mueve el extremo inferior del IC | vivo, **equivalente**: el umbral es 0 y la tolerancia es relativa; bajar x > 0 a x − h·\|x\| (h < 1) nunca lo deja ≤ 0 |
| M14 | no se comprueba que el solicitante de la CT-10 sea AG-20 | vivo, **equivalente**: una CT-10 coincidente del Auditor del mismo soporte también es una re-ejecución independiente |
| M15, M16 | no se comprueba que la CT-10 re-ejecute el soporte, ni la celda del soporte | muertos (M16, por r01_01) |
| M17 | no se comprueba la ficha del soporte | **vivo** (H-06) |
| M18 | `catalog_version` vuelve a 4.0 | muerto |
| M19, M20 | FC-EVAL-001 ignora las fechas; con fechas y sin mínimo usa 10 | muertos |
| M21 | sin incidencia en HA | muerto |
| M22 | la CT-10 la pide AG-18 | muerto |
| M23 | la celda de una propuesta retirada no se vuelve a proponer | muerto |
| M26 | un Motor que no sirve (estado distinto de SERVED) se da por bueno | muerto |

22 muertos, 2 equivalentes y 2 vivos reales (M12 y M17, H-06).

## Hallazgos

Ningún camino con el código del ejecutor tal como está saca un certificado sin su re-ejecución CT-10 coincidente: los que siguen
exigen escribir en F6 con la identidad del Evaluador (AG-20, único propietario, con la cadena de huellas) o un Motor que mienta.

| ID | Gravedad | Cómo reproducirlo | Esperado / obtenido | Corrección sugerida | Estado |
| --- | --- | --- | --- | --- | --- |
| H-01 | media | Desde `bloque_a/11_Ejecutor`: `../../.venv/bin/python -m pytest -q -p no:cacheprovider ../../.docs/tickets/T-160/revisores/r01_01_ataques.py -k "h01"` | `motivo_sin_reejecucion` comprueba que la CT-10 citada existe, coincide y re-ejecuta un FC-EVAL-001 de la misma clase × horizonte, pero no que sea **la de este certificado**: no ata el método de la celda ni las cifras del CERT- a las del cálculo de soporte, ni impide que dos certificados citen la misma. Un PROPUESTO escrito en F6 con otro método y cifras infladas (`bss_ic90` [0,8; 0,95], n_eff 10 000) que cita el soporte y la re-ejecución de un certificado legítimo **entra en vigor** por CT-04, también con el legítimo ya aprobado | En CT-04, comparar con `servicio.comparar` y la tolerancia de la ficha las `cifras_certificado` del CERT- con las del `resultado` del soporte, exigir que el soporte sea de la misma celda × método (la petición puede llevar el método) y que ningún otro CERT- cite la misma re-ejecución | abierto |
| H-02 | media | `-k "h02"` en el mismo script | `certificados_vigentes` (lo que leen la síntesis, G3-CON-10 y el backtest para publicar probabilidades) da por bueno cualquier CERT VIGENTE de F6, cite o no una re-ejecución. Lo cubre el límite declarado («los VIGENTE anteriores a T-160 se quedan»), pero esa decisión `[PROPUESTO]` no es la más prudente, como dice INC-T160-01: un certificado de antes de T-160 sigue habilitando probabilidades sin re-ejecución | Que la revisión retire (revoque, que es automático y endurece) los VIGENTE sin re-ejecución coincidente, como ya hace con los PROPUESTO, y la celda se vuelva a proponer con CT-10; o, al menos, que lo decida el operador con la opción prudente por defecto | abierto (lo decide el operador) |
| H-03 | baja | `-k "h03"` en el mismo script | Si `Motor.reejecutar` devuelve `coincide: SI` sin haber escrito la REEJECUCION en el RC (un Motor o un doble defectuoso; el Motor real siempre escribe antes de devolver), con `aprendizaje.solo_endurecer: false` el certificado nace VIGENTE citando un CALC- que no está en el RC. Con `true` (por defecto), CT-04 lo para | Antes de escribir el CERT-, pasar el borrador por `motivo_sin_reejecucion` (una línea): la emisión directa tendría la misma comprobación que CT-04 | abierto |
| H-04 | baja | `-s -k minimo` en el mismo script (imprime el estado de cada caso) | FC-EVAL-001 con `fechas` acepta `min_conglomerados` 0, −1, `True` o 1,5 y sirve un IC del BSS por conglomerados sin mínimo; el Evaluador rechaza esos mismos valores en su configuración (`test_pa03_minimo_de_conglomerados_desde_la_configuracion`). No afecta al certificado (pasa el de la configuración), pero un agente puede pedir esa cifra por CT-09 | Validar en `f_fc_eval` un entero ≥ 2 (no booleano), como `_min_conglomerados` | abierto |
| H-05 | baja | `-k "auditoria_ct10_posterior"` en el mismo script (pasa: documenta el comportamiento) | Si después de proponer, otra CT-10 del mismo cálculo de soporte (por ejemplo, del Auditor) da NO, CT-04 aprueba igual: solo mira la re-ejecución que cita el certificado | Que CT-04 rechace si la última CT-10 del soporte en el RC no coincide | abierto |
| H-06 | baja | `.venv/bin/python .docs/tickets/T-160/revisores/r01_03_mutantes.py <copia «qa31_…_mut»> --scripts --solo M12,M17` | Dos mutantes viven: **M12** (la materialidad no mueve el q90 del nulo: ninguna prueba pone el ECE entre q90·(1 − h) y q90, y el caso «> q90 nulo» de `test_ca4_la_materialidad_…` lo detecta ya moviendo solo el ECE) y **M17** (CT-04 no comprueba que el soporte sea FC-EVAL-001: ninguna prueba cita como soporte un servicio de otra ficha de la misma celda) | Un caso con ECE = q90·(1 − 1,5·tol) en `test_ca4_la_materialidad_…` y una propuesta falsa con soporte de otra ficha en `test_ca5_…` | abierto |

Los scripts de esta ronda están en `revisores/`: `r01_01_ataques.py`, `r01_02_sin_fechas_como_antes.py` y `r01_03_mutantes.py`.

## Veredicto

**APTO** · Se cumplen los nueve criterios. Ningún camino del código saca un certificado sin su re-ejecución CT-10
coincidente: la revisión y CT-04 fallan cerrado ante un Motor ausente, caído, que no sirve, que responde lo que no debe o que
lanza después de escribir; ante cifras distintas, CT-10 «NO» o diferencias dentro de tolerancia que cruzan un umbral (probado de
extremo a extremo con un umbral real); y ante propuestas falsas sin re-ejecución, con la de otra celda o con campos raros. Sin
`fechas`, FC-EVAL-001 da lo mismo que antes. La tolerancia (1e-8) es la de la ficha y su origen es el correcto. D-1 está aplicado
y el verificador ya no lo marca. No hay hallazgos críticos ni altos. Los dos medios (H-01: CT-04 no ata la re-ejecución a las
cifras ni al método del certificado; H-02: los VIGENTE sin re-ejecución siguen habilitando probabilidades) exigen escribir en F6
con la identidad del Evaluador, o son el límite declarado. Pasan a la deuda técnica con los bajos H-03 a H-06, y la opción
prudente de H-02 (revocar y volver a proponer) la decide el operador. Por encargo, este revisor no cierra el ticket ni toca la
deuda: lo hace la sesión coordinadora.
