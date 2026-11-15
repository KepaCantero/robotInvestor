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
| Gate entero, A-Forex y B | — | no lanzados (por instrucción; pasaron en el commit) |

## Veredicto

**NO APTO.**

Los nueve criterios se cumplen en sus términos y lo demás está bien hecho: la caché ya no confunde una tupla con una lista (H-11), CT-10 no se ablanda por una clave nueva de `por_defecto.yaml` que la ficha no lee (H-07), hay un solo criterio de día en UTC en las cuatro familias (H-08), la fecha de NAV con hora se sirve (H-09), los casos de control siguen superados, 36 de 37 mutantes mueren (el vivo es equivalente), ninguna prueba se ha debilitado y las cuotas no suben.

Pero el objetivo central de T-127, cerrar H-10 («ninguna petición da las cifras de un emisor o token»), no se cumple: **H-01 (alta)**, una sola petición con copias del mismo emisor a escala (todos sus importes por 1,02^i) da, en las tres fichas, su cifra exacta (la DD y la PD en FIR-CRED, el LTV y el ICR en REI-LEV, la inflación y la dilución en CHR-TOKEN), y INC-T127-01 afirma lo contrario. Es tan corta como la vía que H-10 señalaba y no está entre los límites declarados. Además **H-02 (media)**: rellenos de cifra nula dan la de un emisor en la media ponderada, sin declarar; y H-03 (baja), un apunte para T-57.

Vuelve a `ri-implementar`: H-01 con su prueba (copias a escala rechazadas en las tres fichas), y H-02 declarado o corregido. En la r02 se vuelve a ejecutar `r01_01_frontera_otras_vias.py`.

**Sin comprobar:** el gate entero; A-Forex y B; REI-NAV-001 (fuera del alcance, anotado en INC-T127-01); ciclos con el modelo real.
