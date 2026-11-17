# T-173 · QA independiente

- **Revisor:** claude (revisor nuevo, sin el contexto de la implementación) · **Ronda:** r01 · 2026-11-17
- **Rama revisada:** `wip/t173` (`1473cf8`) sobre develop `80751da`, en un worktree aparte. Base de comparación: otro worktree en `80751da`.

## Reproducción desde limpio

Por orden de quien encarga la QA, **no se pasaron la suite completa ni `./tools/check_all.sh`**. El gate 12/12 queda pendiente para el cierre.

| Qué | Resultado |
| --- | --- |
| `pytest -q tests/test_t173.py tests/test_t53*.py tests/test_t65_hallazgos.py` | 115 superadas (las 16 nuevas y las de H5 de T-53 y T-65, sin cambios) |
| `pytest -q tests/test_fase4_huecos.py -k pb33` + `revisores/r01_test_pb33.py` | 3 superadas |
| `mutantes.py` del implementador (14) | 14 de 14 muertos |
| `revisores/r01_regresion.sh` | Backtest mock del README (2024-01-05 → 2024-03-29) en la base y en la rama, con el perfil por defecto (DIV) y con uno con H5 (`perfiles.activos: [DIV, RV, MP, RF]`) |

**Regresión (`r01_regresion.sh`).**
- Perfil por defecto:
  - `senales.csv`, `pronosticos.csv` y `metricas.json` son idénticos byte a byte.
  - `consumo.csv` es igual salvo `latencia_s`.
  - F6 tiene los mismos tipos de entrada, y F10 no tiene ningún P-31.
  - Los informes técnicos solo difieren en la ruta absoluta de los entregables hermanos.
- Perfil con H5:
  - Las tres salidas del backtester son idénticas.
  - F6 gana 12 entradas `EH5-`, una por C5 con H5 abiertos; la semana 1 no lleva ninguna porque aún no hay H5, como se declaró.
  - Ningún AJU- ni CFG- de P-31.
  - Cada paquete es igual al de la base si se quitan `x_estados_h5` y el `estado` de los hitos.
  - El técnico solo añade el estado del PRG H5 y el de sus hitos.
- Solo cambia lo declarado.

## Criterios de aceptación

| Criterio | Cumple | Evidencia |
| --- | --- | --- |
| CA-1 | sí, en la letra | `test_pb50_rf_h2_…`. DM-HLN calculado a mano (r01_ataques §1): d̄ = −0,2325, estadístico −4,0802, p = 1,286·10⁻⁴; el código da lo mismo hasta 10⁻¹². Pero la muestra del caso es **un solo conglomerado PA-03** (los 35 se resuelven el 2026-05-29: n_eff = 1). Ver H-01 |
| CA-2 | no | n = 29, p > α, «Limitado», «No», H5, mismo trimestre y «gana»: no degrada (pruebas, y r01 §2, §3 y §7). **Pero sí degrada con una sola semana mala** (H-01), que es justo lo que «sin muestra suficiente no se degrada» debe impedir |
| CA-3 | sí | `test_pb50_el_c5_degrada_y_el_ciclo_lee_limitado_…` |
| CA-4 | sí | `test_pb64_c5_publica_…`; regresión con H5: 12 EH5- |
| CA-5 | sí | `test_pb64_paquete_y_tecnico_…` (valida contra el esquema V5.0); regresión con H5: paquetes iguales salvo lo declarado |
| CA-6 | sí | ídem; regresión con H5 (técnico) |
| CA-7 | sí, en lo ejecutado | Las pruebas de H5 pasan sin cambios. La suite completa y las cuotas no se reprodujeron (por orden) |
| CA-8 | sí | `mapa_plan_pruebas.json` y las evidencias (34 «Superada») en el diff |

## Lo que está bien

- **El lado y la prueba.** `diebold_mariano_hln(pérdida_ref, pérdida_pron)` da d = ref − pron, así que el estadístico < 0 significa que el pronóstico pierde. La p unilateral `t.cdf(est, n−1)` es la de «pierde». Comprobado a mano.
  - Si gana, p = 0,99976 (r01 §2).
  - En el empate exacto, var = 0, p = 0,5 y no degrada (r01 §3).
  - Con NaN o infinito en la probabilidad no degrada (r01 §9).
- **Los números.** Ninguno está escrito a mano: `min_calibrar` (30) y `alfa_holm` (0,10) salen de la config, y la h es la de `evaluar_celda`. Los `[PROPUESTO]` están en INC-T173-01.
- **El escalón trimestral.**
  - El 2026-12-31 a las 23:59 cae en «2026-T4» (r01 §5).
  - Tras una restitución de tipo 3 el 2027-01-04, vuelve a bajar en «2027-T1» con P-30 5.2 → 5.3 (r01 §6).
  - En el mismo trimestre no baja dos veces, y la operación es idempotente (r01 §7).
- **«No».** Nunca va hacia «No» ni sale de él. H5 queda fuera y los contaminados no cuentan.
- **PB-33.** La prueba original (develop `80751da`), con la degradación DM neutralizada, sigue pasando sobre la rama (`revisores/r01_test_pb33.py`). El comportamiento de PB-33 (revocación, alerta, PRG intactos, HT-09) no cambia. La degradación de RV × H3 es legítima: con p = 0,65 y un acierto del 50 % en 120 casos, Brier 0,2725 frente a 0,25 y p ≈ 0,05. Sobre la cobertura de la prueba, ver H-04.

## Hallazgos

| ID | Gravedad | Cómo reproducirlo | Esperado / obtenido | Corrección sugerida | Estado |
| --- | --- | --- | --- | --- | --- |
| H-01 | **alta** | `revisores/r01_ataques.py` §4, §4b y §12 (desde `bloque_a/11_Ejecutor`, `PYTHONPATH=.`) | **Esperado:** una sola semana mala no degrada. Es la misma regla de muestra que el Evaluador aplica en todo lo demás: PA-03, conglomerados por fecha de resolución y `n_eff`.<br>**Obtenido:**<br>(§4) 30 PRG de RF × H2 emitidos y resueltos el mismo día, un solo conglomerado (n_eff = 1): p = 2,6·10⁻⁴ y **degrada**.<br>(§4b) 60 semanas en que el pronóstico gana más una semana mala de 30 PRG: n = 90, 61 conglomerados, n_eff = 61. La DM-HLN sobre la media por conglomerado da p = 0,99999 (el pronóstico es claramente mejor), pero la regla, que trata los 90 PRG como independientes con h = 1, da p = 0,076 y **degrada**.<br>La degradación es pegajosa: volver a «Sí» exige un certificado con n_eff ≥ 100. La prueba nominal CA-1 también es de un solo conglomerado, así que valida exactamente el caso que no debería degradar | En `degradacion_dm`:<br>(1) `fechas = self._fechas_conglomerado(lst)`; si es None, no se degrada.<br>(2) `muestra = ev.n_efectiva(fechas, oo − pp)`. Se exige `muestra["n_eff"] ≥ evaluacion.min_calibrar` y `muestra["conglomerados"] ≥ self._min_conglomerados()`.<br>(3) La DM-HLN se calcula sobre la serie de medias de d por fecha de conglomerado, en orden de fecha, y no por PRG.<br>(4) n_eff y conglomerados van a la evidencia del AJU-.<br>(5) Las pruebas: el fijo de `_sembrar` con fechas de resolución distintas, y dos regresiones con los casos §4 y §4b, que no degradan. Se declara en INC-T173-01 | abierto |
| H-02 | media | `revisores/r01_ataques.py` §10: la escritura en F10 falla (OSError simulado) dentro de `aplicar_degradacion_dm` | **Esperado:** un fallo deja F6 y F10 como estaban, o con un registro coherente.<br>**Obtenido:** F6 se queda con `AJU-2026-0001` en estado CONFIRMADO y `aplicado_en_produccion: True`, y F10 sin P-31. El reintento del mismo trimestre (2026-06-12) no hace nada, porque `_p31_ya_movida` ve el AJU-. La celda sigue en «Sí» todo el trimestre y F6 afirma un ajuste que no se aplicó. `_bajar_a_limitado` es compartida, así que H5 hereda el mismo defecto, que ya existía | En `_bajar_a_limitado`:<br>(1) Construir las tres entradas antes de escribir ninguna.<br>(2) Escribir el AJU- y envolver las dos escrituras de F10 en try/except. Si fallan:<br>— añadir en F6 la misma `id` con `estado: "ANULADO"`, `aplicado_en_produccion: False` y el motivo; `estado(clave="id")` la deja como vigente;<br>— si el CFG- de P-31 llegó a escribirse, añadir en F10 un CFG- que lo revierta (`revierte_a`, `valor_vigente` = la matriz anterior);<br>— relanzar la excepción.<br>(3) Que `_p31_ya_movida` ignore los AJU- `ANULADO`.<br>(4) Una prueba con el §10, que en el reintento sí degrade | abierto |
| H-03 | media | `revisores/r01_tasa_falsa.py`: una celda sin pérdida real, con el mismo Brier esperado que la referencia, evaluada con la regla implementada en cada C5 semanal sobre los datos acumulados | **Esperado:** una tasa de degradaciones falsas acotada por α.<br>**Obtenido:** 8 % en una sola mirada, pero **15,5 % por trimestre y 24,2 % por año y celda**, por las miradas repetidas sobre datos acumulados. Además, no hay corrección por las hasta 48 celdas H1–H4. «Degradar endurece» es cierto, pero no sale gratis: el horizonte deja de ofrecerse sin catalizador (`_horizontes`, orquestación) y volver exige un certificado. 12.2 y PB-50 (paso 2: «Revisión mensual del Evaluador») sitúan esto en la revisión, no en cada C5 | Que se decida y quede registrado (pasa a la deuda si no se corrige ahora).<br>(a) Evaluar la degradación DM solo en la revisión mensual del C5, no en cada C5.<br>(b) Aplicar Holm entre las celdas evaluadas en la misma revisión, como el certificado (Anexo A), o dejar en INC-T173-01, con estas cifras, por qué no.<br>Las dos opciones usan números que ya existen | abierto |
| H-04 | baja | `git diff 80751da..wip/t173 -- tests/test_fase4_huecos.py` | **Esperado:** `test_pb33_…` sigue comprobando su criterio, que G3-CON-10 y HT-09 no publican probabilidad en la celda decertificada (RV × H3).<br>**Obtenido:** como RV × H3 baja a «Limitado» y desaparece, la prueba solo afirma que ninguna vista de RV lleva probabilidad. Ya no hay ninguna vista H3 que lo ejerza. El comportamiento está bien (`r01_test_pb33.py`), pero la suite ya no lo cubre | Añadir a `test_fase4_huecos.py` una variante, la de `revisores/r01_test_pb33.py`: misma preparación, con `monkeypatch.setattr(Evaluador, "aplicar_degradacion_dm", lambda self, *a, **k: [])`, y la afirmación original (`publicadas = [v … if h == "H3"]`, que no esté vacía y que toda `prob` sea None) | abierto |

Observaciones, sin hallazgo:
- Si un PRG de cualquier celda tiene `referencia_ingenua.valor_o_prob` None, se aborta la degradación DM de todas las celdas (r01 §8, TypeError, incidencia en HA). `metricas()` cae antes con lo mismo, así que no es nuevo.
- Dos C5 en el mismo día escriben dos `EH5-` con la misma `id` (r01 §11), con el mismo criterio que `MET-`. La última manda.
- `sintesis.py` lee F4 entero una vez por cada vista H5 (`f4_hit`). Se podría sacar del bucle.

## Mutantes

`mutantes.py` del implementador, reejecutado en el worktree de la QA: 14 de 14 muertos (`vivos: []`), y el árbol queda restaurado. Ninguno de los 14 cubre H-01, H-02 ni H-03: los mutantes no detectan lo que las pruebas no afirman.

## Veredicto

**NO APTO**.
- **H-01 (alta).** La degradación automática «Sí» → «Limitado» se dispara con una sola semana mala, e incluso cuando el pronóstico es mejor por conglomerados. Ignora la muestra efectiva de PA-03, que el resto del Evaluador aplica.
- **H-02 y H-03 (medias).** Corregirlas en la misma ronda o pasarlas a la deuda con su ID.
- **H-04 (baja).** Se corrige con la variante indicada.
- **Ronda r02.** El revisor volverá a ejecutar `revisores/r01_*` (§4, §4b, §10 y §12, y `r01_tasa_falsa.py`) además de las pruebas del implementador.

## Ronda r02

- **Revisor:** claude (el mismo revisor de la r01) · 2026-11-17
- **Rama revisada:** `wip/t173` (`c0ed7f5`) sobre develop `375d24b`, en un worktree nuevo. La base de la regresión es otro worktree en `375d24b`.
- **Alcance:** por orden de quien encarga la QA, no se pasaron la suite completa ni `./tools/check_all.sh`. El gate 12/12 queda para el cierre.

### Reproducción

| Qué | Resultado |
| --- | --- |
| `pytest -q tests/test_t173.py tests/test_t53*.py tests/test_t65_hallazgos.py tests/test_fase4_huecos.py revisores/r01_test_pb33.py` | 178 superadas |
| `revisores/r02_ataques.py` (nuevo, §1–§8) | ver abajo |
| `revisores/r01_ataques.py` tal cual | §1 cae (TypeError): siembra los 35 PRG en una sola fecha de resolución, así que no hay DM que comparar. Es lo esperado con PA-03 |
| `r02_ejecutar_ataques_r01.py --fechas-distintas` (del implementador) | §4, §4b y §12 no degradan; §10 reintenta y degrada; §8 ya no aborta las demás celdas. El resto, igual que en la r01 |
| `revisores/r02_tasa_falsa_una_celda.py` (nuevo) | una sola celda, una mirada al mes: 8 % en la primera mirada, 13,6 % por trimestre y 21,1 % por año. Concuerda con el 12,8 % y el 20,4 % del implementador |
| `revisores/r01_regresion.sh` (base `375d24b` frente a la rama) | ver «Regresión» |
| `mutantes.py` del implementador | 24 de 24 muertos |

### Lo que pediste mirar

1. **La DM sobre las medias por fecha y el orden temporal son correctos.**
   - Lo calculé a mano en `r02_ataques.py` §1, con 15 fechas de 4 PRG cada una, sembradas en orden inverso.
   - d̄ = −0,21 y el estadístico es −13,0958, con p = 1,5116·10⁻⁹ y 14 grados de libertad. El código da lo mismo hasta 10⁻¹².
   - El resto de la muestra: n_eff = 60, 15 conglomerados y umbral de Holm de 0,10 con una sola celda.
   - La serie se ordena con `sort_index()` sobre fechas ISO normalizadas por `_fechas_conglomerado`, así que el orden es cronológico. Con h = 1 el orden ni siquiera cuenta; con h = 2 lo comprobé en §1b.
   - La p unilateral sigue siendo la de «pierde».
2. **El registro RDM- no puede saltarse una revisión.**
   - Dos C5 en el mismo mes dan una sola revisión (1 y 0 ajustes; solo `RDM-2026-06`). El 01-07 abre `RDM-2026-07` y el 04-01-2027, `RDM-2027-01` (§2).
   - Si la revisión falla en el primer C5 del mes, no se escribe RDM-, el C5 deja la incidencia y el siguiente C5 del mes la repite y degrada (§3).
   - En un backtest con saltos (C5 en mayo y después en agosto), agosto hace la revisión (`RDM-2026-05`, `RDM-2026-08`; §4). Los datos son acumulados, así que un mes sin C5 no pierde evidencia.
   - Con el reloj por delante del `as_of` no hay doble aplicación (§5).
3. **El 20,4 % al año con una sola celda está declarado.**
   - Está en INC-T173-01, con sus cifras y su motivo: el Anexo A no da un α por revisión ni un gasto de α entre miradas.
   - Es aceptable como `[PROPUESTO]`: la tasa por celda con 12 celdas es de 0,9 % por trimestre y 1,5 % por año, frente al 15,5 % y el 24,2 % de la r01. Con H-01 corregido, ninguna semana suelta degrada.
   - Pero es una decisión del operador que no está en la deuda. Ver H-06.
4. **La reversión no deja huérfanos.**
   - Si falla el CFG- de P-30 (§6): en F10 queda el CFG- de P-31 seguido de su reversión (`revierte_a` = ese CFG-), y la matriz vigente vuelve a «SI». No hay P-30, el AJU- queda `ANULADO` y no se escribe RDM-.
   - El reintento degrada una sola vez, con P-31 en «LIMITADO» y P-30 en 5.2, y `verificar_integridad()` sale en verde.
   - El doble fallo, cuando también falla la escritura del ANULADO (§7), deja el AJU- CONFIRMADO sin F10 y bloquea el trimestre. Es un caso degenerado (falla el disco en los dos archivos): es una observación, no un hallazgo.
   - El único defecto es que la reversión hereda una `methodology_version` 5.1 → 5.2 que nunca se aplicó. Ver H-05.
5. **La adaptación de mi §1 es legítima.**
   - `r02_ejecutar_ataques_r01.py` no cambia mi script al leerlo, salvo por dos cosas:
     - un acceso tolerante a `dm_hln` None;
     - con `--fechas-distintas`, una fecha de resolución por PRG.
   - Con una fecha por PRG, la media por fecha es el propio PRG, así que mi cálculo a mano de §1 sigue siendo el mismo (coincide).
   - §4 y §12 fijan sus propias fechas, que no se tocan. §4b pasa a 61 conglomerados, como el diseño de §12. No esconde ningún ataque.
6. **Regresión: solo cambia lo declarado.**
   - **Perfil por defecto:**
     - `senales.csv`, `pronosticos.csv` y `metricas.json` son idénticos, y `consumo.csv` solo cambia en la latencia.
     - F6 gana 3 entradas `REVISION_DM`, una por mes (enero, febrero y marzo de 2024), todas con «muestra insuficiente» (n_eff ≤ 10,5 y ≤ 3 conglomerados).
     - Ningún P-31 en F10, y los paquetes son iguales.
   - **Perfil con H5:**
     - Las tres salidas también son idénticas.
     - F6 gana 3 entradas `REVISION_DM` y 12 `EH5`, y ningún P-31.
     - Los paquetes son iguales a los de la base salvo `x_estados_h5` y el `estado` de los hitos.

### Estado de los hallazgos de la r01

| ID | Estado | Evidencia |
| --- | --- | --- |
| H-01 | corregido | r01 §4, §4b y §12: no degradan (n_eff = 1; o 61 conglomerados con p = 0,99999). Pruebas `test_pb50_r02_h01_*` (4) |
| H-02 | corregido | r01 §10: el reintento degrada; r02 §6: reversión sin huérfanos. Pruebas `test_pb50_r02_h02_*` (2) |
| H-03 | corregido | Revisión mensual RDM- con Holm (r02 §2–§4 y §8; `test_pb50_r02_h03_*`). Las tasas falsas están en INC-T173-01. Queda la decisión de la deuda (H-06) |
| H-04 | corregido | `test_pb33_con_la_degradacion_dm_neutralizada_…` pasa y afirma lo original sobre H3 |

### Hallazgos nuevos

| ID | Gravedad | Cómo reproducirlo | Esperado / obtenido | Corrección exacta | Estado |
| --- | --- | --- | --- | --- | --- |
| H-05 | baja | `revisores/r02_ataques.py` §6 | **Esperado:** la reversión del CFG- de P-31 no anuncia un cambio de versión que no ocurrió.<br>**Obtenido:** el CFG- de reversión lleva `methodology_version: {"de": "5.1", "a": "5.2"}` (sale de `comun`), aunque P-30 no se movió | En `_bajar_a_limitado`, en el dict de la reversión, añadir `"methodology_version": {"de": mv["de"], "a": mv["de"]}` después de `**comun`. En `test_pb50_r02_h02_si_falla_el_cfg_de_p30_se_revierte_el_de_p31`, afirmar que la reversión tiene `methodology_version["a"] == methodology_version["de"]` | abierto |
| H-06 | baja | `sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md`, fila T-173 | **Esperado:** una decisión `[PROPUESTO]` que corresponde al operador figura en la deuda.<br>**Obtenido:** la tasa de degradaciones falsas con una sola celda en la revisión (12,8 % por trimestre y 20,4 % por año; INC-T173-01) solo está en la incidencia | Añadir una fila nueva a la deuda (o ampliar la de T-173 al cerrarla), en la columna de lo que bloquea o necesita decisión: «Decisión del operador: gasto de α entre las revisiones mensuales de la degradación DM de 12.2 (INC-T173-01). Con una sola celda en la revisión, 12,8 % por trimestre y 20,4 % por año de degradaciones falsas. Opciones: (a) dejarlo así; (b) familia de Holm fija con todas las celdas H1–H4 en «Sí», contando como no rechazables las que no tienen muestra; (c) un α por revisión en el Anexo A.» Estado: Pendiente (operador) | abierto |

Observaciones sin hallazgo:
- **Doble fallo** (r02 §7). Ver el punto 4 de la lista anterior.
- **El fallo de `aplicar_degradacion_h5` sigue sin un `try` en `ciclo`.** Un fallo de F10 en la rama de H5 ahora deja el AJU- ANULADO y relanza la excepción, así que el C5 cae, como antes de T-173. No es nuevo.
- **Las revisiones RDM- vacías.** El primer C5 del mes consume la revisión aunque todavía no haya muestra (`RDM-2024-01` sin celdas en el backtest). Como los datos son acumulados, no se pierde nada.

### Mutantes

`mutantes.py` del implementador, reejecutado en este worktree: 24 de 24 muertos (`vivos: []`; M15–M24 cubren H-01, H-02 y H-03), y el árbol queda restaurado. Ninguno cubre H-05.

### Veredicto r02

**APTO.**
- Se cumplen CA-1 a CA-8 en lo ejecutado.
- Los cuatro hallazgos de la r01 están corregidos y comprobados con mis scripts.
- Solo quedan dos bajos, H-05 y H-06, con su corrección exacta. Si no se corrigen al cerrar, pasan a la deuda con su ID.
- **Condición de cierre:** `./tools/check_all.sh` en verde (12/12) en la máquina del cierre, porque esta QA no lo ha pasado.

## Ronda de cierre

- **Revisor:** claude (el mismo de la r01 y la r02) · 2026-11-17
- **Rama revisada:** `wip/t173` (`5e7d18f`) sobre `c0ed7f5`, en un worktree nuevo. La base de la regresión es `375d24b`.
- **Alcance:** por orden de quien encarga la QA, no se pasaron la suite completa ni `./tools/check_all.sh`. Lo hace quien cierre en develop.

### Comprobaciones

- **H-05.** El CFG- de reversión lleva ahora `methodology_version: {"de": "5.1", "a": "5.1"}` (`revisores/r02_ataques.py` §6). El reintento sigue degradando una sola vez, con P-30 en 5.2, y la integridad sale en verde.
- **H-06: la familia fija sale bien de la matriz.**
  - Se construye desde la matriz de la revisión: la vigente de F10, o `_tabla_base`. Toma las celdas `== "SI"` de `HORIZONTES_DM = ("H1", "H2", "H3", "H4")`.
  - Con la tabla 8.3 da 32 celdas (lo conté aparte con `TABLA_HORIZONTES`).
  - Las celdas en «Limitado» o «No», y las H5, no entran. Una celda degradada sale de la familia en la revisión siguiente.
- **Las celdas sin muestra cuentan como p ausente sin romper `ev.holm`.**
  - `holm` trata None como no rechazable y lo ordena al final. `{"a": None, "b": None}` da 0,05 y 0,0, sin rechazo.
  - Con 31 celdas sin muestra y una con p = 0,003, el umbral es α/32 = 0,003125 y la celda se rechaza. Con p = 0,0032 ya no.
  - El bucle de umbrales salta las claves sin entrada en `out` y las que tienen `motivo`, así que una celda sin datos no recibe `degradar`.
  - El `type: ignore[arg-type]` está justificado: `holm` admite None en su código, aunque la firma dice `float`.
  - En r02 §1 y §8 la pérdida clara sigue degradando, con umbral 0,003125 (y 0,003226 en la segunda celda).
- **El regreso de `test_pb33_…` es correcto.**
  - Con la familia de 32, RV × H3 (p ≈ 0,05) ya no supera Holm, así que la prueba vuelve a su criterio original: hay vistas H3 y ninguna lleva probabilidad.
  - Además afirma que no hay degradación DM y que la RDM- de ese mes registra `p_valor > umbral_holm`.
  - La variante de H-04, con la DM neutralizada, sigue en la suite.
  - `revisores/r01_test_pb33.py` (la prueba de develop tal cual) pasa.
- **Pruebas.** `tests/test_t173.py`, `tests/test_fase4_huecos.py` y `revisores/r01_test_pb33.py`: 80 superadas.
- **Regresión (`revisores/r01_regresion.sh`).** Comparé la base `375d24b` con `5e7d18f` en los dos perfiles.
  - Salidas del backtester idénticas.
  - F6 con los mismos tipos y recuentos que en la r02: 3 `REVISION_DM` y, con H5, 12 `EH5`.
  - Ningún P-31 en F10.
  - Paquetes iguales salvo `x_estados_h5` y el `estado` de los hitos.
- **Mutantes.** No los reejecuté en esta ronda: el implementador declara 26 de 26, y en la r02 los reejecuté (24 de 24).

### Estado de los hallazgos

| ID | Estado |
| --- | --- |
| H-01 a H-04 | corregidos (r02) |
| H-05 | **corregido** |
| H-06 | **corregido**. Opción (b), decidida por delegación del operador el 17-11-2026, registrada en INC-T173-01 y en la fila T-173 de la deuda |

**Pérdida de potencia.** Con una pérdida moderada, la detección baja al 1,4–10 % al año, frente al 42–70 % con α entero (INC-T173-01). La familia fija de 32 la da por buena el operador por delegación. Una pérdida clara, como la de PB-50, sigue degradando.

### Veredicto final

**APTO.**
- Ningún hallazgo abierto.
- CA-1 a CA-8 se cumplen en lo ejecutado.
- **Condición de integración:** `./tools/check_all.sh` en verde (12/12) al llevarlo a develop.
