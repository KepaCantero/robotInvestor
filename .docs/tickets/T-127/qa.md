# T-127 · QA independiente

- **Revisor:** subagente revisor nuevo, sin contexto de la implementación (Claude; implementó otra sesión de Claude) · **Ronda:** r01 · 2026-11-15
- **Copia revisada:** clon desconectado en `fb3ccd4`: `motor/fichas_p2.py` (`FRONTERA_B`, `_grupos_casi_iguales`, `_sin_dominio`, `_orden`, FIR-CRED-001, REI-LEV-001, CHR-TOKEN-001 y sus casos de control), `motor/servicio.py` (`_marcado`, `_respaldo_en`), `configuracion.py` (`anotar_respaldo`), `motor/operaciones.py` (`dia`, `sin_zona`) y sus usos; `tests/test_t127_hallazgos.py` y las pruebas cambiadas de `test_t119_p2.py`, `test_t119_r02.py` y `test_t121_hallazgos.py`; INC-T127-01 e INC-T119-01.
- **Orden de lectura:** `README.md` → diff del código → mis scripts y los de los revisores anteriores → al final `analisis-tecnico.md`, `pruebas.md` e INC-T127-01.

## Reproducción

Desde la raíz de la copia, con `.venv` enlazado al del repositorio.

| Comprobación | Orden | Resultado |
| --- | --- | --- |
| T-119 `r02_01_frontera_b.py` | `.venv/bin/python -I .docs/tickets/T-119/revisores/r02_01_frontera_b.py bloque_a/11_Ejecutor` | FIR-CRED-001 1/1 (10 casi clones a 1e-9 rechazados); se para en la línea 71 con `TypeError` al leer `dispersion["ltv_pct"]`, que con 3 componentes es ahora `null`: es lo esperado (lo que ese bloque pedía). Lo que no llega a ejecutarse lo hago en mi `r01_01` (REI-LEV con 3: dispersión `null` y declarada) |
| T-119 `r02_02_cache.py` | ídem | **12/12** (la tupla, igual que sola: H-11 corregido) |
| T-121 `r01_01` a `r01_04` | `.venv/bin/python -I .docs/tickets/T-121/revisores/r01_0N_….py bloque_a/11_Ejecutor` | `r01_01`: 206 pruebas, 0 diferencias en los casos base, 0 escapes, **0** «día del corte con hora rechazado» (20 en la r01: la fecha de NAV de FON-DISC, H-09); solo se sirven las fechas futuras por naturaleza. `r01_02`: **11/11** (A2, A2b, A5 ya no se ablandan). `r01_03`: **36/37**, el que falla es el caso mal planteado que su autor señaló (FON-FLOW-001 con la frecuencia rota); con zonas horarias, mismo veredicto en MON-YLD, TCV-CDS y FON-FLOW. `r01_04`: 67/67 casos de control |
| Mutantes del implementador | `python .docs/tickets/T-127/revisores/impl_mutantes.py bloque_a/11_Ejecutor <scratchpad>/qa8_mut_t127_mut` | **36 de 37 muertos**; vive S02, que es equivalente (con un token, su peso es el 100 % y la dominancia ya lo deja sin calcular). La copia se borra sola |
| Mi script | `.venv/bin/python -I .docs/tickets/T-127/revisores/r01_01_frontera_otras_vias.py bloque_a/11_Ejecutor` | **2/11**. Ver H-01 y H-02 |
| Goldens, gates, cuotas, suite | «Comunes», abajo | en verde |

## Criterios de aceptación

| Criterio | Cumple | Evidencia |
| --- | --- | --- |
| CA-1 | sí en sus términos | T-119 `r02_01` (FIR-CRED, 10 casi clones); `test_h10_casi_clones_*`, `test_h10_borde_*` en la suite. Pero la regla se esquiva con copias a escala (H-01) |
| CA-2 | sí | `test_h10_un_componente_de_peso_casi_total_se_rechaza`, `test_h10_borde_de_la_dominancia_*`; mutantes D01 a D08 muertos |
| CA-3 | sí | `r01_01`: REI-LEV con 3, `dispersion` `null` y declarada; pruebas de 6/7 componentes y tokens |
| CA-4 | sí | pruebas de covenants, *staking* y red propia; mutantes R01 a R03 y S01, S03 muertos |
| CA-5 | sí | `r01_01` [casos de control] y T-121 `r01_04`: las 67 fichas con casos (66 + AUD-REX-001), superadas, las tres de T-127 entre ellas. Los casos de REI-LEV-001 y CHR-TOKEN-001 cambian sus datos (S3 con covenants, TKB con *staking* y concentración) y lo que esperan (dispersión ausente): leído, conservan lo que comprobaban y la dispersión se comprueba con 7 en `test_t127_hallazgos.py` |
| CA-6 | sí | T-119 `r02_02` 12/12; `_marcado` distingue lista, tupla y claves no textuales |
| CA-7 | sí | T-121 `r01_02` 11/11; leído: `parametro` apunta el respaldo solo en `_ConfiguracionLeida` y todas las lecturas del Motor pasan por `parametro`, `sesiones_horizonte` o `parametros_ht03` sobre la configuración de la ficha (las constantes de módulo de `fichas_series.py` solo se muestran en `UMBRALES`; la cota de cada llamada sale de la configuración) |
| CA-8 | sí | T-121 `r01_03` (zonas horarias) y `r01_01` (fecha de NAV con hora, 0 rechazos) |
| CA-9 | sí | scripts y mutantes de arriba; suites en verde; ruff 2902 y mypy A 109 |

## Pruebas cambiadas (¿se debilitó alguna?)

Leídas en el diff. Ninguna se ha quitado ni rebajado sin motivo: las de dispersión y holguras de REI-LEV-001 pasan de 3 a 7 componentes (`_con_cuatro_mas`) y siguen comprobando el mínimo, la holgura negativa y el «falla uno solo»; la de la envoltura de resultados no finitos pasa a FIR-CRED-001 (12 componentes), que sí calcula la dispersión; la de la red propia usa «Bitcoin»/BTC porque «red TKA» ahora se rechaza (lo prueba `test_t127_hallazgos.py`); en `test_t121_hallazgos.py` el caso «valor parcial» pasa a ERROR_ORIGINAL, que es la regla nueva de INC-T127-01, y `_cubre` se sustituye por la comprobación de `respaldos`. ✔

## Números y su origen

`FRONTERA_B` (tolerancia de clon 0,01, peso máximo 0,95, mínimo de orden `len(ESTADISTICOS_ORDEN) + 2`) y `redes_propias` van en los `UMBRALES` de las tres fichas, con su motivo al lado y `[PROPUESTO INC-T127-01]`; la petición no los cambia (`test_ningun_umbral_se_cambia_desde_la_peticion`, +10 casos). Nada nuevo en `por_defecto.yaml` de T-127 (la sección nueva de ese fichero es de T-125). ✔

## Hallazgos

| ID | Gravedad | Cómo reproducirlo | Esperado / obtenido | Corrección sugerida | Estado |
| --- | --- | --- | --- | --- | --- |
| H-01 | alta | `.venv/bin/python -I .docs/tickets/T-127/revisores/r01_01_frontera_otras_vias.py bloque_a/11_Ejecutor` (vías «E»). A mano: en FIR-CRED-001, el componente C11 del caso de control 1 repetido 10 veces con capitalización y deudas multiplicadas por 1,02^i | **Esperado** (objetivo de T-127 para H-10; INC-T127-01: la regla «impide que una sola petición devuelva la cifra de un emisor o un token»). **Obtenido:** con **una** petición de copias a escala (todos los importes de un emisor multiplicados por 1,02, 1,02², …) la regla no salta y la entrega es la cifra exacta de ese emisor, a 1e-9: FIR-CRED-001 da la DD 1,712107431 y la PD 4,343843613 % de C11 (las de las fórmulas directas de la ficha), con la dispersión colapsada (mínimo = máximo = media); REI-LEV-001 con 3 o 7 copias de S1 da su LTV 40 %, su ICR 4, su impacto en FFO y sus holguras; CHR-TOKEN-001 con 2 o 7 copias de TKA da como «sector» su inflación neta (5 %) y su dilución a 30 y 90 días. Los cocientes que calcula cada ficha no dependen de la escala y la regla de casi clones compara importes (difieren un 2 % > 1 %); la dominancia no salta (ninguna copia pasa del 51 % de su base). Es la misma vía que H-10 («copias de un emisor»), igual de corta, y no está entre los límites declarados (restar dos peticiones, rellenos para un estadístico de orden, compensaciones) | Comparar los componentes por lo que no depende de la escala: aplicar la regla de casi clones a las cifras individuales que la ficha ya calcula para la dispersión (DD y PD; LTV, ICR, deuda neta/EBITDA y vencimientos; FDV/capitalización e inflación) o a los datos normalizados por una magnitud del propio componente; y rechazar si el agregado coincide con la cifra de un solo componente en todas las métricas. Prueba: copias a 1,02^i en las tres fichas, rechazadas | abierto |
| H-02 | media | El mismo script, vías «Z» | **Esperado:** la dominancia (1, k) evita que el agregado sea la cifra de un componente. **Obtenido:** C11 con el 30 % (o el 60 %) de la deuda y nueve rellenos de PD 0 (capitalización enorme frente a una deuda pequeña): se sirve, y PD media / peso de C11 (que conoce quien pide, son sus datos) = 4,343843613 %, la PD de C11. Lo mismo con rellenos de deuda neta 0 en el LTV de REI-LEV. La regla mira el peso en la base de ponderación, no la aportación al agregado. INC-T127-01 declara los rellenos para un estadístico de orden, no para la media ponderada | Declararlo en INC-T127-01 («rellenos de cifra nula dan la de un componente en la media ponderada»), o aplicar la dominancia también a la aportación (|wᵢ·xᵢ| / Σ|wⱼ·xⱼ|), sabiendo que en la PD puede rechazar sectores reales con un emisor mucho más arriesgado que el resto | abierto |
| H-03 | baja | `r01_01`, vías «O» | Con 7 o más componentes, el máximo de la dispersión de la PD es la PD de un emisor (C11, 4,343843613 %). Declarado en INC-T127-01 («rellenos diseñados para que un estadístico de orden caiga en un emisor»); lo anoto para que el operador lo vea junto a H-01 y H-02 en T-57: el mínimo y el máximo son siempre la cifra de un componente, sin identificarlo | Nada en código; en la pregunta para T-57, decir que la frontera solo impide identificar el componente, no dar su cifra | abierto |

## Invariantes

- Ningún camino a una orden: el Motor no emite órdenes. ✔
- Sin LLM en la ruta: las tres fichas y la caché son deterministas. ✔
- Controles: las reglas de la frontera están en `UMBRALES` y la petición no las relaja (prueba con cada clave). ✔
- Falla cerrado: casi clones y dominancia rechazan sin citar identificadores; pocos componentes → `null` y limitación; CT-10 no culpa al original sin poder reproducirlo. ✔ (salvo H-01: se sirve lo que no debería)
- Números: de `UMBRALES` con su origen y `[PROPUESTO]`. ✔
- Decisiones del operador: tres `[PROPUESTO]` en INC-T127-01 con pregunta para T-57. ✔
- Documentación: INC-T119-01 corregida y remite a INC-T127-01; la fila de §5 de Decisiones, añadida. La afirmación de INC-T127-01 sobre «una sola petición» no es cierta (H-01). ✔ con nota

## Comunes (T-123, T-124 y T-127)

| Comprobación | Orden | Resultado |
| --- | --- | --- |
| Suite de A, una vez | `cd bloque_a/11_Ejecutor && /home/user/robotinvestor/.venv/bin/python -m pytest -q -p no:cacheprovider` | **5798 passed** en 24 min 55 s, código 0 (línea base 607) |
| Goldens de contratos | `cd bloque_a/11_Ejecutor && python tests/goldens_ct.py` | «goldens de contratos: coinciden» |
| ruff | `ruff check --output-format=concise bloque_a/11_Ejecutor bloque_a_forex/11_Ejecutor bloque_b/11_Ejecutor \| wc -l` | **2902** (cuota 2902) |
| mypy A como el gate | `cd bloque_a/11_Ejecutor && mypy bloque_a --ignore-missing-imports --no-error-summary \| wc -l` | **109** (cuota 109) |
| Gates ligeros | `tools/secrets_scan.py`, `tools/refs_vivas.py`, `tools/nfc_check.py`, `tools/corpus_integridad.py` | en verde (con mis scripts ya en la copia); corpus 695 |
| Gate entero, B | — | no lanzados (por instrucción; pasaron en el commit) |

## Veredicto

**NO APTO.**

Los nueve criterios se cumplen en sus términos y lo demás está bien hecho: la caché ya no confunde una tupla con una lista (H-11), CT-10 no se ablanda por una clave nueva de `por_defecto.yaml` que la ficha no lee (H-07), hay un solo criterio de día en UTC en las cuatro familias (H-08), la fecha de NAV con hora se sirve (H-09), los casos de control siguen superados, 36 de 37 mutantes mueren (el vivo es equivalente), ninguna prueba se ha debilitado y las cuotas no suben.

Pero el objetivo central de T-127, cerrar H-10 («ninguna petición da las cifras de un emisor o token»), no se cumple: **H-01 (alta)**, una sola petición con copias del mismo emisor a escala (todos sus importes por 1,02^i) da, en las tres fichas, su cifra exacta (la DD y la PD en FIR-CRED, el LTV y el ICR en REI-LEV, la inflación y la dilución en CHR-TOKEN), y INC-T127-01 afirma lo contrario. Es tan corta como la vía que H-10 señalaba y no está entre los límites declarados. Además **H-02 (media)**: rellenos de cifra nula dan la de un emisor en la media ponderada, sin declarar; y H-03 (baja), un apunte para T-57.

Vuelve a `ri-implementar`: H-01 con su prueba (copias a escala rechazadas en las tres fichas), y H-02 declarado o corregido. En la r02 se vuelve a ejecutar `r01_01_frontera_otras_vias.py`.

**Sin comprobar:** el gate entero; B; REI-NAV-001 (fuera del alcance, anotado en INC-T127-01); ciclos con el modelo real.

---

# Ronda r02 · QA independiente

- **Revisor:** subagente revisor nuevo, sin contexto de la implementación ni de la r01 (Claude; implementó otra sesión de Claude) · **Ronda:** r02 · 2026-11-15
- **Copia revisada:** clon desconectado en `f7faa1b` («wip local: T-127 r02 y T-128»): `motor/frontera_b.py` (nuevo; `_sin_copias_a_escala`, `_aportacion_maxima`, `_concentradas`, `_sin_dominio` con grupos), FIR-CRED-001, REI-LEV-001 y CHR-TOKEN-001 en `motor/fichas_p2.py`, sus casos de control, `tests/test_t127_r02.py` y las pruebas cambiadas de `test_t119_p2.py` y `test_t127_hallazgos.py`; INC-T127-01 «Ronda r02».
- **Orden de lectura:** `README.md` → `frontera_b.py` y las tres fichas → mis scripts → al final `analisis-tecnico.md`, `pruebas.md` e INC-T127-01.

## Reproducción

Desde la raíz de la copia, con `.venv` enlazado al del repositorio (enlace borrado al acabar).

| Comprobación | Orden | Resultado |
| --- | --- | --- |
| Script de la r01 | `.venv/bin/python -I .docs/tickets/T-127/revisores/r01_01_frontera_otras_vias.py bloque_a/11_Ejecutor` | **7/7** (era 2/11): las copias a escala se rechazan en las tres fichas (FIR-CRED con 10, REI-LEV con 3 y 7, CHR-TOKEN con 2 y 7) y los rellenos de PD 0 al 30 % y al 60 % también (aportación); casos de control 67/67 |
| Mi script de la r02 | `.venv/bin/python -I .docs/tickets/T-127/revisores/r02_01_troceo_y_simetria.py bloque_a/11_Ejecutor` | **1/7**. Ver H-04 y H-05 (y H-01 de T-128) |
| T-119 `r02_02_cache.py`, T-121 `r01_02_h01_ct10.py` | ídem | 12/12 y 11/11 |
| Mutantes de la r02 | `python .docs/tickets/T-127/revisores/impl_r02_mutantes.py bloque_a/11_Ejecutor <scratchpad>/qa9_mut_t127r02_mut --antes <fichas_p2.py de fb3ccd4>` | **41 mutantes, 40 muertos**; vive E11, equivalente (con `tokens_minimos_sector` = 2, un subconjunto de un solo grupo pesa el 100 % y la dominancia ya lo deja sin calcular). Copia borrada |
| Goldens, gates, cuotas, suite | «Comunes», abajo | en verde |

## Hallazgos de la r01

| ID | Estado en la r02 | Evidencia |
| --- | --- | --- |
| H-01 (alta, copias a escala) | **corregido** | `r01_01` vías E: «1 componentes distintos por sus cifras individuales (< 10 / 3 / 2)». Leído: además del grupo por la tupla de cifras, cada media pasa por `_aportacion_maxima`, que agrupa por la cifra de esa media; así, unas copias a escala con otro `mu_historico`, otros covenants u otra concentración (tupla distinta) siguen rechazadas porque la DD, el LTV o la inflación de todas es la misma. Probado a mano |
| H-02 (media, rellenos de cifra nula) | **corregido** | `r01_01` vías Z: «más del 95 % de la PD media … lo aporta un componente». Coste declarado en INC-T127-01 |
| H-03 (baja, orden con 7 o más) | **declarado bien** | INC-T127-01 r02, «H-03»: «un estadístico de orden es siempre la cifra de un componente … La frontera impide identificar el componente, no dar una cifra que coincide con la de uno». Lo que pedía la r01 |

## Criterios de aceptación

Los nueve de la r01 siguen cumpliéndose (casos de control 67/67, `r01_01` 7/7, scripts de T-119 y T-121, mutantes, cuotas). Lo que la r02 añade (copias a escala por sus cifras, dominancia de la aportación) se cumple en sus términos. El objetivo de H-10 que la r02 vuelve a afirmar no (H-04).

## Pruebas cambiadas (¿se debilitó alguna?)

Leídas en el diff `fb3ccd4..f7faa1b`. `test_fir_cred_limites_del_dominio_que_se_admiten`: primero exige el rechazo nuevo (aportación) y después sube la volatilidad de los demás para que se sirva, y añade que la PD máxima es 100 % (la volatilidad 10 entra): más fuerte. `test_chr_token_oraculo_con_fracciones_exactas`: ventana 20 → 31 (a 20 días solo desbloqueaba TKA); el borde de 20 días se sigue probando en `test_chr_token_borde_de_la_ventana_y_desbloqueos_pasados`, con un tercer token que desbloquea el mismo día. `test_h10_staking_…`: nominal 4 % → 4,5 % para que los dos *staking* reales no coincidan. Casos de control de CHR-TOKEN-001 (TKB quema 4e7 y desbloquea 2,4e7): `verificar_casos_control` 67/67. Ninguna rebajada. ✔

## Hallazgos de la r02

| ID | Gravedad | Cómo reproducirlo | Esperado / obtenido | Corrección sugerida | Estado |
| --- | --- | --- | --- | --- | --- |
| H-04 | alta | `.venv/bin/python -I .docs/tickets/T-127/revisores/r02_01_troceo_y_simetria.py bloque_a/11_Ejecutor` (vías «T» y «S»). A mano: en REI-LEV-001, S1 del caso de control partido en 3 «componentes» con repartos distintos de cada importe (GAV 50/30/20 %, deuda 30/40/30 %, caja 50/25/25 %, EBITDA 40/40/20 %, gastos 25/35/40 %, FFO 50/30/20 % y cada vencimiento repartido de otra forma) | **Esperado** (objetivo de T-127, INC-T127-01 r02: «la frontera impide que la entrega sea la cifra de un componente o se despeje solo con ella y los pesos»; el principio: el Bloque A no entrega la cifra de un emisor o token concreto con una sola respuesta). **Obtenido:** con **una** petición y solo los datos del propio emisor, sin calcular nada fuera, la entrega es su cifra exacta (a 1e-9): REI-LEV-001 da el LTV 40 %, el ICR 4, la deuda neta/EBITDA 8,33, los vencimientos a 24 meses 52,38 % y el impacto en FFO −20,33 % de S1; CHR-TOKEN-001 da, como «sector» de 2 tokens, FDV/CM 1,667, inflación 5 %, desbloqueos 5 % y 15 %, *staking* real 3 % y concentración 35 % de TKA, el token que la regla de la «propia red» (CA-4) no deja pedir solo. Las partes difieren más del 1 % en datos y en cifras (no son clones ni copias a escala), ninguna pasa del 95 % de una base ni de la aportación, y un cociente de sumas de las partes es el del entero. En FIR-CRED-001 (Merton, no lineal) 10 copias de C11 con σ_E·(1 ± δ), δ de 2 % a 10 %, dan su DD con un error de 0,44 % (media) y 0,04 % (mediana): la precisión que INC-T127-01 da como motivo para rechazar los casi clones («por debajo del 1 %, el agregado … es la cifra del emisor con dos o más cifras significativas»). No está entre los límites declarados: «restar dos peticiones», «rellenos para un estadístico de orden», «quien conoce las cifras de sus rellenos» (aquí no hay rellenos ni se calcula nada fuera) y «compensaciones que se anulan en una suma» (aquí ningún componente se anula; se reparte el emisor) | Ninguna regla sobre los datos distingue un emisor troceado (o copias con perturbaciones simétricas) de varios emisores reales, así que es una decisión para T-57, no un ajuste de tolerancias: (a) declararlo en INC-T127-01 y en la pregunta para T-57 con su alcance («un emisor troceado en partes, o copias perturbadas de forma simétrica, da su cifra en una sola petición; la frontera evita la revelación por descuido, no la de un solicitante que construye los componentes; el control es el propósito de la petición, 1.6, y el Registro de cálculos»), y quitar o matizar la frase de que la entrega no puede ser la cifra de un componente; o (b) exigir que cada componente sea un instrumento del universo con su identificador verificable (HT-01 o el Broker) y rechazar partes de uno. Con (a), una prueba que fije el límite declarado (S1 troceado se sirve y se registra) | abierto |
| H-05 | baja | El mismo script, vía «C»: S1 + un relleno de deuda neta +400 + otro de −400 (caja mayor que la deuda) | Se sirve, y LTV agregado · ΣGAV / GAV de S1 = 40 %, el LTV de S1, exacto. Está declarado («compensaciones entre componentes que se anulan en una suma»), pero la frase de INC-T127-01 r02 «con la aportación limitada al 95 %, el agregado dividido por el peso de un componente acota su cifra con un error de al menos un 5 %» no es cierta: `_aportacion_maxima` mide Σ\|numᵢ\| y no ve que el resto suma 0 | Corregir la frase (el 5 % vale solo si las aportaciones del resto tienen el mismo signo), o medir también la parte con signo: rechazar si \|Σnum − num_G\| < (1 − k)·\|Σnum\| (el resto no aporta casi nada al agregado) | abierto |

## Invariantes

- Ningún camino a una orden: el Motor no emite órdenes. ✔
- Sin LLM en la ruta: `frontera_b.py` y las tres fichas son deterministas (numpy y scipy). ✔
- Controles: `FRONTERA_B` en los `UMBRALES` de las tres fichas; la petición no los cambia (`test_t128_frontera.py::test_las_reglas_son_las_de_frontera_b_y_la_peticion_no_las_cambia` y las de T-127). ✔
- Falla cerrado: copias y aportación rechazan (FIR-CRED, cocientes de REI-LEV) o van a `null` con limitación, sin citar identificadores. ✔ (salvo H-04: se sirve lo que el objetivo dice que no)
- Números: los mismos 1 %, 95 % y 7 de `FRONTERA_B`, con su origen y `[PROPUESTO INC-T127-01]`. ✔
- Decisiones del operador: `[PROPUESTO]` en INC-T127-01 r02 y en la fila de §5 de `Decisiones_del_operador_Bloque_A.md`. ✔
- Secretos y datos personales: ninguno (`secrets_scan`). ✔
- Documentación: INC-T127-01 r02 al día salvo H-04 y H-05; la fila T-127 de la deuda técnica sigue en «EN QA (14-11-2026)» sin la r02 (la añade quien haga el commit, según el README). ✔ con nota

## Comunes (T-127 r02 y T-128)

| Comprobación | Orden | Resultado |
| --- | --- | --- |
| Suite de A, una vez | `cd bloque_a/11_Ejecutor && /home/user/robotinvestor/.venv/bin/python -m pytest -q -p no:cacheprovider` | **5862 passed** en 30 min 52 s, código 0 (línea base 607); lanzada mientras corrían los mutantes y mis scripts |
| `verificar_casos_control` | en `r01_01_frontera_otras_vias.py` | 67 fichas (66 + AUD-REX-001), todas superadas |
| Goldens de contratos | `cd bloque_a/11_Ejecutor && python tests/goldens_ct.py` | «goldens de contratos: coinciden» |
| ruff | `ruff check --output-format=concise bloque_a/11_Ejecutor bloque_a_forex/11_Ejecutor bloque_b/11_Ejecutor \| wc -l` | **2902** (cuota 2902) |
| mypy A como el gate | `cd bloque_a/11_Ejecutor && mypy bloque_a --ignore-missing-imports --no-error-summary \| wc -l` | **109** (cuota 109) |
| Gates ligeros | `tools/secrets_scan.py`, `tools/refs_vivas.py`, `tools/nfc_check.py`, `tools/corpus_integridad.py` | en verde (con mis scripts en la copia); corpus 695 |
| Gate entero, B | — | no lanzados (por instrucción) |

## Veredicto (r02)

**NO APTO.**

La r02 corrige lo que la r01 encontró: las copias a escala ya no pasan (por la tupla de cifras y, con más fuerza, por la aportación agrupada por la cifra de cada media), los rellenos de cifra nula se rechazan, H-03 está bien declarado, 40 de 41 mutantes mueren (el vivo es equivalente), ninguna prueba se debilita y las cuotas no suben.

Pero el objetivo que la ronda vuelve a afirmar no se cumple: **H-04 (alta)**, un emisor troceado en partes con repartos distintos (o copias con perturbaciones simétricas) da en una sola petición su cifra exacta en REI-LEV-001 y CHR-TOKEN-001 (en CHR-TOKEN, la de un token que la regla de la «propia red» no deja pedir solo) y en FIR-CRED-001 con la precisión que el propio INC rechaza en los casi clones, sin estar entre los límites declarados. No se arregla con otra tolerancia: hace falta declararlo con su alcance (y que T-57 lo decida) o verificar los componentes contra el universo. **H-05 (baja):** la frase del «error de al menos un 5 %» es falsa con compensaciones.

Vuelve a `ri-implementar`: H-04 declarado o resuelto, con su prueba; H-05, la frase corregida (o la aportación con signo). En la r03 se vuelve a ejecutar `r02_01_troceo_y_simetria.py` (si H-04 se declara, sus FALLA de las vías T y S pasan a ser el límite declarado y el script se lee así).

**Sin comprobar:** el gate entero; B; ciclos con el modelo real.

---

# Ronda r03 · QA independiente

- **Revisor:** subagente revisor nuevo, sin contexto de la implementación ni de las rondas anteriores (Claude; implementó otra sesión de Claude) · **Ronda:** r03 · 2026-11-15
- **Copia revisada:** clon desconectado en `eb66257` («wip local: T-127 r03 y T-128 r02»): `motor/frontera_b.py` (`AVISO_B`, `_datos_que_coinciden`, `_aviso_casi_clones`, `_aportacion_maxima` con signo), sus llamadas en FIR-CRED-001, REI-LEV-001, CHR-TOKEN-001 (`fichas_p2.py`) y REI-NAV-001 (`fichas_reales.py`); `tests/test_t127_r03.py`; INC-T127-01 «Ronda r03» y la fila de §5 de `Decisiones_del_operador_Bloque_A.md`. Para el motivo del límite: `orquestacion.py`, `agentes.py`, `evaluador.py`, `motor/servicio.py` y `herramientas/ht01_datos.py`.
- **Orden de lectura:** `README.md` → diff `f7faa1b..eb66257` del código → mis scripts → al final `analisis-tecnico.md`, `pruebas.md` e INC-T127-01.

## Reproducción

Desde la raíz de la copia, con `.venv` enlazado al del repositorio (enlace borrado al acabar).

| Comprobación | Orden | Resultado |
| --- | --- | --- |
| Script de la r02 | `.venv/bin/python -I .docs/tickets/T-127/revisores/r02_01_troceo_y_simetria.py bloque_a/11_Ejecutor` | **2/7** (era 1/7): la vía «C» (compensación ±400) pasa a «ok» (rechazo por la aportación con signo). Las cinco FALLA (REI-LEV T3, CHR-TOKEN T2, REI-NAV S2, REI-FFO T2, FIR-CRED S10) son el límite declarado de INC-T127-01 «Ronda r03», tal como las lee `pruebas.md`; REI-NAV S2 y FIR-CRED S10 llevan el aviso |
| Script de la r01 | `.venv/bin/python -I .docs/tickets/T-127/revisores/r01_01_frontera_otras_vias.py bloque_a/11_Ejecutor` | **7/7**; casos de control 67/67 |
| Mi script de la r03 | `.venv/bin/python -I .docs/tickets/T-127/revisores/r03_01_cota_aviso_y_origen.py bloque_a/11_Ejecutor` | **10/11**. Ver «Lo comprobado» y H-06; H-07 lo imprime el bloque A4 |
| Mutantes de la r03 | `python .docs/tickets/T-127/revisores/impl_r03_mutantes.py bloque_a/11_Ejecutor <scratchpad>/qa13_mut_t127r03_mut` | **29 de 29 muertos**. Copia borrada |
| Mutantes propios (copia `qa13_mut_propios`, borrada) | a mano: `_aportacion_maxima` con `return 1.0` si la suma con signo es 0 | vive: equivalente (con Σden ≠ 0 y suma 0 ya se devuelve 0 antes; solo se llega con Σden = 0) |
| Goldens, gates, cuotas, suite | «Comunes», abajo | en verde |

## Lo comprobado

**H-04: ¿es correcta la decisión de declarar el límite?** Sí. Lo verifiqué en el código, no en el análisis:

- Recorrido del AST de todo `bloque_a/` (bloque «O» de mi script): `Motor.servir` lo llaman solo `orquestacion.py:361` (las seis fichas de series de HT-01 del lote, ACC-MOM, FX-VOL, FX-TREND, RISK-DD, ST-DESC y FIN-CAGR, con `datos = [{"serie": s, ...}]`), `orquestacion.py:1350` (ML-CLUS-001), `evaluador.py:456` (FC-EVAL-001) y el propio `servicio.py` (casos de control y CT-10). `agentes.py` no toca el Motor ni las herramientas de los modelos llegan a él (`llm.py` solo declara la búsqueda web). Ninguna de las fichas con componentes se pide desde el ciclo: sus `valores` los escribiría un agente analista por CT-09.
- HT-01 (`ht01_datos.ProveedorDatos`) normaliza CSV con `fecha` y `cierre` y sirve `cierres`, `serie`, `valor_en` y `huella` por símbolo: no hay balances, deudas, ofertas de tokens, NAV ni flujos contra los que verificar un componente.
- ¿Hay una verificación barata? No para lo que importa: comprobar que el `id` es un símbolo del universo, o incluso contrastar el `precio` de REI-NAV o CHR-TOKEN con el cierre de HT-01, no detecta un troceo (los trozos comparten precio y se reparten las acciones o los importes). La única fuente fiable sería un proveedor de fundamentales que no existe; por eso la opción (b) de la QA r02 pasa a T-57 como pregunta, que es lo correcto (decisión del operador, `[PROPUESTO]`).
- La declaración dice lo que no se cubre: el troceo con repartos distintos y la perturbación simétrica, con el alcance («un solicitante que fabrica los componentes a propósito»), el control (propósito 1.6 y Registro de cálculos, que guarda `datos[].valor`: lo fija `test_h04_limite_declarado_un_emisor_troceado_se_sirve_y_queda_en_el_registro`), las vías del revisor una a una y la pregunta para T-57 en INC-T127-01 y en §5. Dos matices de redacción en H-07 y H-08 (bajos).

**H-04, el aviso.** Funciona en las vías para las que se hizo: FIR-CRED S10 (10 componentes) y REI-NAV S2 dan el aviso, sin identificadores, y llega al RC. Ningún caso de control lo da, ni las 67 fichas de `verificar_casos_control` en su RC (bloque A1). La petición no lo cambia (`datos_distintos_aviso`, `tolerancia_clon` y `peso_maximo_componente` en `parametros` se rechazan; bloque A5). Con datos corrientes simulados (cifras redondeadas a 2 significativas, como las escribiría un analista; bloque A2) es raro en FIR-CRED (0,1 % a 1,1 % de las peticiones de 10 a 30 emisores) y no aparece en REI-LEV ni en REI-NAV; en CHR-TOKEN no (H-06).

**H-05, la cota.** Correcta y justa. 4000 casos propios (bloque K: n de 2 a 12, pesos de e⁻³ a e³, copias de la misma cifra, resto construido junto al borde con los dos signos y rellenos ±10 que se compensan): 2833 pasan la regla y en **todos los grupos** (no solo el primero) el error de agregado·Σden/den_G es ≥ (1 − k)/(2 − k); el peor caso queda a 1,0024 veces la cota, 0 violaciones. Es exacta: con un resto de −c·num_G y rellenos ±10, c = cota·(1 + 10⁻⁶) da 0,949999947 (se sirve) y c = cota·(1 − 10⁻⁶) da 0,950000052 (se rechaza). Con el resto del mismo signo la cota es (1 − k)/k, como dice la frase. La deducción: si 1 − |R|/|S| ≤ k con S = num_G + R, entonces |R| ≥ (1 − k)|num_G + R|, cuyo mínimo de |R|/|num_G| es (1 − k)/(2 − k) con R de signo contrario y (1 − k)/k con el mismo. La prueba del implementador (`test_h05_por_debajo_de_k_el_error_es_de_al_menos_la_cota`) solo mide el grupo del componente 0; la mía, todos.

## Hallazgos de la r02

| ID | Estado en la r03 | Evidencia |
| --- | --- | --- |
| H-04 (alta, troceo) | **declarado bien** (límite con su alcance, pregunta para T-57, prueba que lo fija y aviso) | Arriba; `r02_01` vías T y S como límite |
| H-05 (baja, frase del 5 %) | **corregido** | `r02_01` vía C «ok»; bloque K de `r03_01` |

## Hallazgos de la r03

| ID | Gravedad | Cómo reproducirlo | Esperado / obtenido | Corrección sugerida | Estado |
| --- | --- | --- | --- | --- | --- |
| H-06 | baja | `r03_01`, bloque A3. A mano: CHR-TOKEN-001, caso de control 1, con dos tokens más de oferta fija y redonda, totalmente en circulación (circulante = total = máxima = 1e9), sin emisión ni quema, precios 0,42 y 7,9 y *staking* y concentración distintos | **Esperado** (AVISO_B: «dos emisores reales que coincidan en todos los demás datos a la vez no se esperan»). **Obtenido:** se sirve con «aviso (1.6): 2 componentes coinciden con otro … pueden ser un mismo emisor con un dato movido». La firma de CHR-TOKEN (precio, circulante, total, máxima, emisión, quema) tiene cuatro datos que en tokens reales coinciden a menudo sin informar nada (máxima = total o `None`, emisión 0, quema 0, ofertas redondas). En la simulación del bloque A2 la frecuencia depende de cuántos tokens así haya: del 0,2 % al 1 % de las peticiones de 10 a 20 tokens con supuestos prudentes (20–30 % de ofertas redondas) y del 15 % al 46 % si la mitad son de oferta fija y redonda. No cambia ninguna cifra (solo la limitación y el estado `SERVED_WITH_LIMITATIONS`), pero quita valor al aviso como señal para el Registro | Contar solo las coincidencias informativas (no `None` = `None` ni 0 = 0), o poner en la firma del aviso las cifras que distinguen a dos tokens (*staking*, concentración), o exigir que el dato distinto difiera poco (la perturbación simétrica de la r02 llega al 10 %); con una prueba de tokens de oferta fija sin aviso | abierto |
| H-07 | baja | `r03_01`, bloque A4: REI-NAV-001, la sociedad A del caso 2 en dos partes con el NAV por acción ±4 % (la vía S2 de la r02) **sin `otros_pasivos`** | **Esperado** (INC-T127-01 r03: el aviso salta con un dato movido; «moviendo dos datos … se esquiva»). **Obtenido:** prima agregada −10 %, la de A, **sin aviso**: al omitir `otros_pasivos` (opcional), la ficha lo deriva como GAV − deuda − NAV y la firma del aviso cambia en dos datos aunque quien pide solo movió uno. Es el límite declarado del aviso, pero con un solo dato de entrada | Construir la firma del aviso de REI-NAV con los datos de entrada (`otros_pasivos` como `None` cuando se deriva) o decir en INC-T127-01 que un dato derivado cuenta como movido | abierto |
| H-08 | baja | Lectura: `motor/frontera_b.py`, líneas 5 a 7 del docstring | El módulo sigue abriendo con «Ninguna cifra de una entrega puede ser la de un instrumento concreto … ni de forma que se pueda despejar de una sola respuesta», la frase que INC-T127-01 r03 dice haber quitado; el párrafo de la r03 (líneas 19 a 25) la matiza más abajo | Matizarla en la misma frase («… sin que quien pide haya construido los componentes para ello; ver el límite declarado») | abierto |

## Invariantes

- Ningún camino a una orden: el Motor no emite órdenes. ✔
- Sin LLM en la ruta: el aviso y la aportación con signo son numpy. ✔
- Controles: `FRONTERA_B` y `AVISO_B` no los cambia la petición (bloque A5). El aviso no relaja nada: añade una limitación. ✔
- Falla cerrado: la compensación rechaza (REI-LEV, FIR-CRED) o va a `null` (CHR-TOKEN, CHR-FLOW) sin identificadores. ✔
- Números: `AVISO_B` (1 dato) con su motivo y `[PROPUESTO INC-T127-01]`; los de `FRONTERA_B` no cambian. ✔
- Decisiones del operador: el límite y la alternativa (b) van `[PROPUESTO]` con su pregunta para T-57 en INC-T127-01 y en §5 de las decisiones. ✔
- Secretos y datos personales: ninguno (`secrets_scan`). ✔
- Documentación: README del ejecutor (limitación 3) con el límite declarado; INC-T127-01 r03 al día salvo H-08. La fila de T-127 en la deuda técnica sigue sin la r03 (la añade quien hace el commit, según el README del ticket). ✔ con nota

## Comunes (T-127 r03 y T-128 r02)

| Comprobación | Orden | Resultado |
| --- | --- | --- |
| Suite de A, una vez | `cd bloque_a/11_Ejecutor && /home/user/robotinvestor/.venv/bin/python -m pytest -q -p no:cacheprovider` | **5895 passed** en 24 min 36 s, código 0 (línea base 607); lanzada mientras corrían los mutantes y mis scripts |
| `verificar_casos_control` | en `r01_01_frontera_otras_vias.py` y en `r03_01` (bloque A1) | 67 fichas (66 + AUD-REX-001), todas superadas |
| Goldens de contratos | `cd bloque_a/11_Ejecutor && python tests/goldens_ct.py` | «goldens de contratos: coinciden» |
| ruff | `ruff check --output-format=concise bloque_a/11_Ejecutor bloque_a_forex/11_Ejecutor bloque_b/11_Ejecutor \| wc -l` | **2902** (cuota 2902) |
| mypy A como el gate | `cd bloque_a/11_Ejecutor && mypy bloque_a --ignore-missing-imports --no-error-summary \| wc -l` | **109** (cuota 109) |
| Gates ligeros | `tools/secrets_scan.py`, `tools/refs_vivas.py`, `tools/nfc_check.py`, `tools/corpus_integridad.py` | en verde (con mis scripts en la copia); corpus 695 |
| Gate entero, B | — | no lanzados (por instrucción) |

## Veredicto (r03)

**APTO.**

Los criterios CA-10 a CA-12 se cumplen y los nueve de la r01 siguen cumpliéndose (casos de control 67/67, `r01_01` 7/7, mutantes de la r03 29/29 muertos, suite en verde, cuotas sin subir, ninguna prueba existente cambia).

- **H-04 (alta de la r02): la decisión de declarar el límite es correcta y suficiente para esta tarea.** Lo comprobé en el código: ningún camino del ejecutor pide una ficha con componentes (solo las seis de series de HT-01, ML-CLUS-001 y FC-EVAL-001, más los casos de control y CT-10 del propio servicio), los `valores` de esas fichas los escribiría un agente analista por CT-09, y HT-01 solo sirve cierres: no hay fuente contra la que verificar balances, ofertas ni NAV, ni una comprobación barata que detecte un troceo. La declaración dice qué no se cubre (troceo, perturbación simétrica), contra quién (un solicitante que fabrica los componentes a propósito), qué controla ese caso (1.6 y el Registro de cálculos, con una prueba que lo fija) y lleva la pregunta para T-57 con la alternativa de una fuente verificable. Que sea aceptable es decisión del operador (`[PROPUESTO]`), no del código.
- **El aviso** funciona en las vías del revisor, no lo da ningún caso de control y la petición no lo cambia; con datos corrientes es raro en FIR-CRED, REI-LEV y REI-NAV. Quedan dos defectos bajos: falsos avisos en CHR-TOKEN con tokens de oferta fija y redonda (H-06) y REI-NAV sin aviso si se omite `otros_pasivos` (H-07).
- **H-05 (baja de la r02): corregido.** La medida con signo rechaza la compensación, y la frase «(1 − k)/(2 − k)» es cierta y exacta: 4000 casos propios sin ninguna violación en ningún grupo, y en el borde la regla cambia de servir a rechazar a ε = ±10⁻⁶.

H-06, H-07 y H-08 (bajos) pasan a la deuda técnica con su ID. Cerrar la tarea (estado, deuda, diario, memoria, commit) le toca a quien coordina: por instrucción, este revisor no hace commit ni toca otros archivos.

**Sin comprobar:** el gate entero (`./tools/check_all.sh`), B (por instrucción); ciclos con el modelo real; el comportamiento de un agente analista real al construir componentes.
