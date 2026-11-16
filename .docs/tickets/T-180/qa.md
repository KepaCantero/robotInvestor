# T-180 · QA independiente

- **Revisor:** subagente de Claude sin contexto de la implementación (regla `compartida/2026-11-12_claude-puede-hacer-qa`) · **Ronda:** r01 · 16-11-2026
- **Copia revisada:** worktree desechable en la instantánea `7ac5220`, con `.venv` enlazado. Sin red ni gasto. Opinión formada con el
  plan, los hallazgos de T-163 y el diff antes de leer `analisis-tecnico.md`.

## Reproducción desde limpio

```bash
cd bloque_a/11_Ejecutor
../../.venv/bin/python -m pytest -q -p no:cacheprovider -rf ../../.docs/tickets/T-180/revisores/r01_01_ataques.py   # 19, pasan todas
../../.venv/bin/python -m pytest -q -p no:cacheprovider -rf ../../.docs/tickets/T-163/revisores/r01_01_ataques.py   # 3 fallan por diseño
../../.venv/bin/python -m pytest -q -p no:cacheprovider -rf ../../.docs/tickets/T-160/revisores/r01_01_ataques.py   # 1 falla por diseño (H-05 de T-160)
../../.venv/bin/python tests/goldens_ct.py
../../.venv/bin/python -m pytest -q -p no:cacheprovider                                    # suite completa, en segundo plano
cd ../..
for g in refs_vivas secrets_scan nfc_check corpus_integridad; do .venv/bin/python tools/$g.py; done
.venv/bin/ruff check --output-format=concise bloque_a/11_Ejecutor bloque_a_forex/11_Ejecutor bloque_b/11_Ejecutor | wc -l
.venv/bin/mypy --ignore-missing-imports --no-error-summary bloque_a/11_Ejecutor/bloque_a | wc -l
.venv/bin/python .docs/scripts/evidencias_plan_a.py && .venv/bin/python .docs/scripts/evidencias_plan_a.py --pb PB-32
# mutantes, cada lote en su copia desechable (bloque_a/ entero y .docs/tickets/T-160, T-163 y T-180):
.venv/bin/python .docs/tickets/T-180/mutantes_t180.py <copia «…_mut»>
.venv/bin/python .docs/scripts/mutantes_revisor_ampliado.py .docs/tickets/T-160/revisores/r01_03_mutantes.py <copia «qa31_…_mut»> \
  tests/test_t163_hallazgos_t160.py tests/test_t180_hallazgos_t163.py ../../.docs/tickets/T-160/revisores/r01_01_ataques.py -k "not auditoria_ct10_posterior"
.venv/bin/python .docs/tickets/T-180/revisores/r01_02_mutantes.py <copia «…_mut»>
```

| Comprobación | Resultado |
| --- | --- |
| Suite completa de A (una vez) | **7207 superadas y 2 omitidas** en 56 min, sin fallos |
| `r01_01_ataques.py` de T-163 | 28 superadas (las `test_h01_*` y `test_h02_*` incluidas); fallan **por diseño** las tres que forjan con `_fabricadas()`: `test_falso_desde_cero_…`, `test_un_lote_con_dos_propuestos_…` y `test_ct04_no_aprueba_un_segundo_certificado_…`. Las tres dan «CALC-… no cumple el criterio del certificado …: ECE 0,0999… > q90 nulo 0,0400…»: mis datos no cumplían el criterio, que es lo que H-01 pedía comprobar. Las cubren `test_h03_n07_…` y `test_limite_declarado_…` del ticket con datos que sí lo cumplen |
| `r01_01_ataques.py` de T-160 | 34 superadas; falla solo la de H-05, por diseño desde T-163 |
| `r01_01_ataques.py` de esta ronda (19) | pasan todas (abajo) |
| Mutantes de T-180 (`mutantes_t180.py`, 9) | 9 muertos |
| Mutantes de T-160 (`r01_03`, 26, con las pruebas de T-163 y T-180) | 24 muertos; M13 y M14, los equivalentes de su QA |
| Mutantes del revisor (`revisores/r01_02_mutantes.py`: N01–N12 de T-163 sin tocar su script, más V01 y V02) | N01–N10 y N12 muertos por las pruebas del ticket (N03, N04 y N07 ya por las de T-180; N05 mata ahora las 7 pruebas adaptadas, antes 5); N11 vive, equivalente (el de T-163); V02 muerto; **V01 vive** (H-01). La primera pasada dio N11 y V01 «muertos» por un error de colección mío (los dos `r01_01_ataques.py` en una llamada chocan por nombre de módulo); corregido con `--import-mode=importlib` y repetidos |
| Goldens | coinciden |
| Gates ligeros | `refs_vivas`, `secrets_scan`, `nfc_check` en verde; corpus: 695 coinciden |
| Cuotas | ruff **2813** (≤ 2813); mypy A **109** (≤ 109) |
| Plan de pruebas | mapa: 67 del plan, 204 citadas y todas existen; PB-32 **Superada** |

## Lo que se atacó (r01_01_ataques.py de esta ronda)

| Ataque | Resultado |
| --- | --- |
| Cifras del CERT- dentro de la tolerancia que cruzan el criterio: n_eff 100 frente a 100·(1 − 10⁻⁹) del soporte; extremo inferior del IC +10⁻²¹ frente a −10⁻²¹ (iguales para `comparar` por su suelo absoluto); ECE a ±10⁻⁹ del q90 | rechazados: el criterio se aplica a las cifras del soporte, no a las del CERT- (con ±10⁻¹³ ya lo para la comparación de cifras) |
| p de DM-HLN justo en α | vale con la CT-10 «SI»; con DENTRO_TOLERANCIA, la materialidad la sube y no vale |
| Celda de habilidad débil (la de H-01 de T-163) por la vía normal, forjada con sus entradas reales como PROPUESTO y escrita VIGENTE | no se propone; CT-04 rechaza; `certificados_vigentes` no la devuelve |
| Celda débil con un subconjunto elegido a mano de sus PRG reales (los acertados) | **entra**: es el límite declarado (no se atan las entradas a F4) y exige pedir el soporte y la CT-10 como AG-20 |
| Soporte pedido por AG-18, AG-02, «ag-20» o «AG-20 » | no vale («no lo pidió el Evaluador») |
| Otro agente pide antes exactamente la petición del Evaluador en el mismo Motor | la celda no se certifica (la caché devuelve su `calc_id`): falla cerrado; ningún otro cliente pide FC-EVAL-001 con `metodo` y `horizonte` (observación, no hallazgo) |
| Legítimo aprobado y revisiones posteriores con más PRG (dos meses) | sigue, sin revocar ni proponer otro |
| Dos celdas legítimas con Holm, aprobadas en un lote | siguen las dos |
| Legítimo con una CT-10 DENTRO_TOLERANCIA de verdad (ficha con el Brier a tol/10) | se propone, CT-04 lo aprueba y la revisión lo mantiene |
| Emisión directa (`solo_endurecer` false) | nace VIGENTE y sigue |
| Certificado de T-163 (soporte sin `horizonte`) | sigue valiendo |
| Subir `min_certificar` por encima del n_eff | revoca con su motivo; volver al valor de la entrega no lo resucita: la celda se vuelve a proponer |
| El ayudante de `conftest.py` (n = 160) en un ciclo | publica probabilidad solo en su celda; no se revoca |
| ECE a q90·(1 − 3·tol) con la CT-10 DENTRO_TOLERANCIA | vale (un paso de holgura, como al proponer); con dos pasos, no: es la prueba que mata V01 |

**El ayudante** (n = 60 → 160) no debilita nada. Las pruebas que lo usan no cambian sus aserciones, salvo t53 y t66, que ahora
afirman el motivo. El ayudante afirma él mismo que su soporte cumple el criterio. Roto (N05), hace fallar las 7 pruebas adaptadas.

**Holm con una sola celda** (decisión del agente, `[PROPUESTO]` en INC-T160-01 y en la fila de §4 de Decisiones): me parece bien.
- Con una hipótesis, Holm es la prueba de DM-HLN a α, así que es lo mismo que pide el Anexo A con varias celdas.
- Endurece: solo deja fuera una celda con el IC del BSS > 0 y una p > α.
- Hace cierto el `holm_superado: true` del CERT-.
- Alinea la propuesta con lo que CT-04 comprueba en el soporte; sin ella, un certificado legítimo podría quedar atascado en CT-04.

Con varias celdas, CT-04 solo comprueba la condición necesaria (p ≤ α), no el escalonado de Holm. Está declarado y para entrar exige
los permisos del Evaluador.

## Criterios de aceptación

| Criterio | Cumple | Evidencia |
| --- | --- | --- |
| CA-1 | sí | `test_h01_*` del ticket; r01_01 (cifras en la tolerancia, p en α, solicitantes, celda débil); U01–U04, U06, U07 |
| CA-2 | sí | `test_h01_la_revision_revoca_…`; r01_01 (umbral subido, legítimos que siguen) |
| CA-3 | sí | `test_h01_con_una_sola_celda_…`; U05 |
| CA-4 | sí | aserción en el ayudante; U09; N05 mata las 7; r01_01 (ciclo con el ayudante) |
| CA-5 | sí | `test_h02_…`; `test_h02_*` de r01_01 de T-163; U08 |
| CA-6 | sí | t53 y t66 con el motivo; N03, N04 y N07 muertos por las pruebas del ticket |
| CA-7 | sí | r01_01 de T-163: 28 superadas, 3 por diseño (confirmadas) |
| CA-8 | sí | r01_03: solo M13 y M14; r01_02: solo N11 (equivalente) y V01 (H-01, una prueba que falta, no un fallo del código) |
| CA-9 | sí | suite 7207, goldens, gates, ruff 2813, mypy 109, PB-32 Superada |

## Hallazgos

Ningún certificado sin re-ejecución coincidente, ni uno cuyo soporte incumpla el criterio, entra en vigor o publica probabilidades.
La revocación no salta con certificados legítimos en ninguno de los casos probados.

| ID | Gravedad | Cómo reproducirlo | Esperado / obtenido | Corrección sugerida | Estado |
| --- | --- | --- | --- | --- | --- |
| H-01 | baja | `.venv/bin/python .docs/tickets/T-180/revisores/r01_02_mutantes.py <copia «…_mut»> --solo V01` | V01 (CT-04 aplica dos pasos de holgura con una CT-10 DENTRO_TOLERANCIA en lugar de uno) vive con las pruebas del ticket. `test_h01_con_una_ct10_dentro_de_tolerancia_…` prueba un ECE que no pasa (q90·(1 − tol/2)) y otro lejos del umbral, pero ninguno en el borde que la propuesta aguantó. Un CT-04 más estricto que la propuesta revocaría certificados legítimos en el borde sin que nada lo notara. El código de hoy está bien | Llevar al fichero del ticket `test_en_el_borde_ct04_no_es_mas_estricto_que_la_propuesta_con_dentro_de_tolerancia` de r01_01 (ECE a q90·(1 − 3·tol) con DENTRO_TOLERANCIA: tiene que valer), que mata V01 | abierto (por regla del operador, se subsana en este ticket antes de cerrarlo) |

Observaciones (no son hallazgos):
- El falso con PRG elegidos a mano y el escalonado de Holm entre celdas son el límite declarado en INC-T160-01.
- La clave de la caché del Motor no lleva el solicitante: hoy no hay otro cliente que pida esa petición, y si lo hubiera fallaría cerrado.

Los scripts de esta ronda están en `revisores/`, en este orden:
1. `r01_01_ataques.py`, desde `bloque_a/11_Ejecutor`.
2. `r01_02_mutantes.py`, desde la raíz, con una copia «…_mut». Envuelve el de T-163 sin cambiarlo.

## Veredicto

**APTO** · Se cumplen los nueve criterios y no hay hallazgos críticos, altos ni medios.
- CT-04, la emisión, `certificados_vigentes` y la revisión aplican al soporte el criterio del certificado con los umbrales de la
  configuración, y exigen que el soporte lo pidiera el Evaluador.
- Ni cifras dentro de la tolerancia que cruzan un umbral, ni una celda débil, ni un soporte de otro agente entran en vigor.
- Los certificados legítimos siguen vigentes: una celda, dos con Holm, CT-10 DENTRO_TOLERANCIA de verdad, emisión directa, los de
  T-163 y revisiones con más PRG.
- La decisión de Holm con una celda es sólida y está anotada.
- El ayudante no debilita ninguna prueba.

H-01 es bajo (falta una prueba de borde). Por la regla del operador de hoy, se subsana en este mismo ticket antes de cerrarlo. Por
encargo, este revisor no cierra el ticket.
