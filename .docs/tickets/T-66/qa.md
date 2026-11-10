# T-66 · QA independiente

- **Revisor:** un revisor nuevo, sin contexto de la implementación (subagente Claude). Formé mi opinión con el plan, las propuestas de T-53 y el diff antes de leer `analisis-tecnico.md` y `pruebas.md`.
- **Ronda:** r01 · 2026-11-10 · commit revisado `4a92a15` (rama `develop`).

## Ronda r01

### Reproducción desde limpio

- **Worktree aparte:** `git worktree add --detach …/scratchpad/qa_t66/wt 4a92a15`.
- **Suite de A:** con `PYTHONPATH=<wt>/bloque_a/11_Ejecutor` y `/home/claude/repo/.venv/bin/python -m pytest -q -p no:cacheprovider tests`. `bloque_a.__file__` sale del worktree. Resultado: **172 passed** (113 s).
- **Gate completo:** `./tools/check_all.sh` en el worktree, con `.venv` enlazado temporalmente, `PYTHONPATH` hacia los tres ejecutores del worktree y `RUFF_CACHE_DIR` fuera de `bloque_a/`. Resultado: **12/12**.
  - corpus-integridad, nombres-nfc, yaml-configs, secrets y refs-vivas en verde.
  - Cuotas: ruff 3109/3109, mypy A 123/123, FX 174/174 y B 159/159.
  - pytest: A 172, FX 68 y B 141.
- **Mutaciones del ticket:** `SRC=<wt>/bloque_a DEST=<scratchpad>/mut .docs/tickets/T-66/revisores/mutaciones_orquestacion.sh`. Las **11 mutaciones fallan**. En 3 de ellas (pa14, pa09_auto y h06) comprobé que fallan por la aserción esperada y no por un error de importación.
- **Mutaciones de evaluación (script propio `r01_07`):** PA-03, PA-09, PA-10, PA-21 y CT-04 `aprobar_certificados`. Las **14 mutaciones fallan**, por su aserción.
- **CLI del ejemplo de CLAUDE.md** con la configuración por defecto (`backtest --desde 2024-01-05 --hasta 2024-03-29`): termina. Solo analiza DIV, con 33 pronósticos, 0 excluidos por contaminación (cliente simulado) y ningún certificado.
- **Limpieza:** worktree eliminado con `git worktree remove --force`. El repositorio principal queda sin cambios (`git status` vacío) y no hay `.ruff_cache` en `bloque_a/`.

### Criterios de aceptación

| Criterio | Cumple | Evidencia |
| --- | --- | --- |
| CA-1 · cada propuesta aplicada tiene una prueba que falla sin ella | sí | 11 mutaciones de orquestación (script del ticket) y 14 de evaluación (`r01_07`): todas fallan por su aserción |
| CA-2 · suites y gate en verde, línea base subida | sí | A 172 (antes 117), FX 68, B 141; gate 12/12; cuotas bajadas: ruff 3120 → 3109 y mypy A 135 → 123 |
| CA-3 · lo no aplicado, con motivo y destino | no | Las propuestas enteras sí están, en el README («No entra»), en T-67 y en T-57. Faltan partes de propuestas aplicadas a medias (H-06) |
| CA-4 · el Documento 0 no se toca; el comportamiento, en el README del ejecutor y en INC-T66-xx | sí | El diff no toca `01_Gobernanza`, corpus-integridad en verde; INC-T66-01 y 02 en `docs/incidencias.md`; sección T-66 en el README del ejecutor |

**Cada propuesta frente a lo que pide:**

| Propuesta | Resultado |
| --- | --- |
| PA-01 | Correcto. Por defecto solo DIV; un tipo no activo en CT-01 o en una profundización da NO_ESTIMABLE, declarado, sin ninguna llamada al modelo. Un CT-04 de `clases_activas` seguido de un ciclo funciona. Se ve afectado por H-02 y H-03 |
| H-06 | Correcto. PARCIAL, `SIN_RESULTADO`, RUN en F5 íntegro; un backtest de un tipo no activo termina |
| PA-05 | **Incumple la regla de resolución (H-01).** La entrada al Contradictor va sin razonamiento (también anonimizada), el veredicto se calcula por regla y una tesis frágil sale «especulativo». La relevancia ALTA no se aplica: es una desviación documentada (INC-T66-01, a T-57) |
| PA-09 | Correcto. Funcionan `auto`, la marca en las altas e hitos, la exclusión de certificados, lecciones, ajustes, H5 e historial, y el informe aparte. Ante la duda marca (sin fecha de corte, un valor no booleano, ReplayClient) |
| PA-10 | Correcto. El certificado nace PROPUESTO; aprobarlo dos veces, aprobar uno retirado, uno de antes de su emisión o uno de una celda ya vigente se rechaza sin tocar F6. Un PROPUESTO no pasa solo a VIGENTE al cambiar `solo_endurecer`, y la recalibración es siempre una propuesta. Queda H-04 |
| PA-03 (parte) | Correcto. Con una sola fecha, n_eff = 1; con dependencia total, n_eff = número de fechas. Con menos de 10 fechas no hay IC; las entradas no válidas fallan cerrado; el bootstrap es determinista; 300 pronósticos en 12 fechas correlacionadas no certifican. Queda H-05 |
| PA-14 | Correcto. Sin errores con 0 candidatos ni con el Analista caído, y es determinista |
| PA-21 | Correcto. Los valores fuera de rango, NaN, booleanos o cadenas dan `null` o se cuentan como inválidos; los PRG antiguos se leen sin error. Queda H-08 |

### Hallazgos

| ID | Gravedad | Cómo reproducirlo | Esperado / obtenido | Corrección sugerida | Estado |
| --- | --- | --- | --- | --- | --- |
| H-01 | **alta** | `r01_01_pa05_contrarreplica.py`, escenarios 5 y 6 | **Esperado** (README de T-66 e INC-T66-02): una objeción fuerte queda resuelta solo si el Analista cita evidencia verificable **y** el Contradictor confirma esa objeción en la contrarréplica.<br>**Obtenido:** en `orquestacion.py`, `_refutacion`, el bucle `if o["fuerza"] == "fuerte" and o["objecion_id"] in conf` aplica la respuesta de la contrarréplica a **cualquier** objeción fuerte cuyo id aparezca en ella, aunque no se enviara a la contrarréplica.<br>• **Escenario 5:** se pide confirmar solo OBJ-XLU-09, pero AG-11 devuelve también OBJ-XLV-09 y OBJ-XLE-09, de las que el Analista había respondido «No la puedo resolver», sin evidencia. Quedan resueltas, entran en el top-3 y el run sale **COMPLETO y ENTREGADO**.<br>• **Escenario 6:** si el modelo repite ids entre opciones (`OBJ-02` en todas, algo que el esquema no impide), la evidencia y la confirmación de una opción resuelven las fuertes de las otras 3, que se publican.<br>Es un camino que falla abierto en el control que PA-05 endurece, con una salida de modelo no fiable | • Aplicar `conf` solo a las objeciones enviadas en `replicas`, con la clave (ref, objecion_id).<br>• Usar también esa clave en `resp`, o rechazar o renumerar en el ejecutor los ids repetidos de REFUTACION (por ejemplo, `OBJ-<ref>-nn` asignado por código).<br>• Añadir los escenarios 5 y 6 como pruebas de regresión | abierto |
| H-02 | media | `r01_02_pa01_alcance.py`, prueba 4: `b.consulta("Analiza qué conviene hacer ahora")` con la configuración por defecto | **Esperado:** un escalado C3 sin tipo va a un tipo activo.<br>**Obtenido:** va a RV, un tipo no activo; el run sale PARCIAL, sin análisis. El ejecutor tiene `… if c in CLASES] or ["RV"]` escrito a mano (`orquestacion.py`, `consulta`), y el simulado también recurre a RV. Con PA-01 por defecto, todo escalado sin tipo queda sin resultado | • Usar como respaldo la lista de tipos activos (F10 P-02 o `perfiles_activos`) e informar a AG-01 de cuáles son.<br>• Lo mismo en el simulado.<br>• Añadir una prueba | abierto |
| H-03 | baja | `r01_02`, prueba 5: CT-04 `{"configuracion": {"clases_activas": []}}` seguido de un ciclo | **Esperado:** se rechaza o no se analiza nada.<br>**Obtenido:** queda APLICADA con P-02 = [] y el ciclo analiza DIV, porque `f10.get("P-02") or perfiles_activos(...)` trata la lista vacía como ausente | Rechazar `clases_activas` vacío en CT-04, o distinguir una lista vacía de una clave ausente | abierto |
| H-04 | baja | `r01_03_pa10_certificados.py`, prueba 5: CT-04 `{"aprobar_certificados": "CERT-2026-0001"}` (una cadena) | **Esperado:** un único rechazo de formato.<br>**Obtenido:** 14 rechazos, uno por carácter («no existe ningún certificado 'C'»). Falla cerrado, pero el registro es confuso | Validar el tipo en `decision()` antes del bucle (o pasar la lista entera a `Evaluador.aprobar_certificados`, que ya valida todo antes de escribir) | abierto |
| H-05 | baja | `r01_04_pa03_neff.py`, prueba 3; `ev.n_efectiva(f, [c]*200)` con 10 fechas | **Esperado** (docstring): con residuos sin varianza, ρ = 1 y n_eff = número de fechas (10), fallando cerrado.<br>**Obtenido:** depende del valor por error de coma flotante: con c = 0,3 da ρ = 0 y n_eff = 200; con 0,35 da ρ = 0,50 y n_eff = 19; con 0,5 da ρ = 1 y n_eff = 10. En casos degenerados el ECE sigue bloqueando el certificado, pero el n_eff que se informa es falso | Detectar la ausencia de varianza con tolerancia (por ejemplo, `np.ptp(y) <= eps` o `np.isclose(msb + msw, 0)`) antes del ANOVA, y añadir una prueba con varios valores constantes | abierto |
| H-06 | baja | Comparar `.docs/tickets/T-53/revisores/arquitectura.md` §3 con el README de T-66 («No entra») y con T-67 en la deuda | **Esperado** (CA-3): todo lo no aplicado tiene su motivo y su destino.<br>**Obtenido:** sin destino quedan:<br>• PA-14: la ablación sin la clasificación de AG-12 y sin la integración;<br>• PA-05: puntuar al Contradictor por las objeciones confirmadas (D-37);<br>• PA-03: los hitos H5 a 12 meses o menos y publicar F4 en SC-4 | Añadirlo a «No entra» y a T-67, con su destino | abierto |
| H-07 | baja | `sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md`, fila T-66 | **Esperado:** EN QA hasta el veredicto.<br>**Obtenido:** «RESUELTO el 10-11-2026». Además, una grabación de ReplayClient hecha antes de T-66 (backtest sin anonimizar) ya no se reproduce con `anonimizar: auto`, porque cambia la clave (`ReplayFaltante`, `r01_05`, prueba 2), y no está documentado | • Volver la fila a EN QA.<br>• Anotar en el README del ejecutor que esas grabaciones necesitan `backtest.anonimizar: false` | abierto |
| H-08 | baja | `sintesis.py`, `_prob_analista` | El rango 0,05–0,95 está escrito a mano en el código, duplicando el esquema `FINALISTA.probabilidades_propias` | Leer el mínimo y el máximo del esquema de `contratos.py`, que es la única definición | abierto |

**Observaciones sin hallazgo** (anteriores a T-66 o fuera de su alcance):
- Una excepción del cliente de IA sube y corta el ciclo. Pasa con todos los agentes de A.
- Si falla la refutación, `veredicto_refutacion` queda `null` en F3. La opción no es elegible, así que la decisión falla cerrado.
- El F10 inicial lleva la fecha real y en un backtest no es visible: en backtest manda `perfiles.activos`.
- Un F6 manipulado a mano lo detecta `verificar_integridad`, pero el Evaluador lo sigue leyendo.

### Sin hallazgo en lo comprobado

- **Falla cerrado:**
  - contrarréplica no conforme o caída de presupuesto: la fuerte sigue abierta;
  - evidencia inventada o de otra opción: se filtra;
  - sin fecha de corte: se marca contaminación;
  - `solo_endurecer` y `min_conglomerados_bootstrap` no válidos: el Bloque no arranca;
  - fechas o residuos no válidos en `n_eff`: ValueError.
- **Determinismo:** dos ejecuciones idénticas dan el mismo paquete, F3, F4 y ablación. El bootstrap por fechas es reproducible.
- **Configuración del llamador:** ni el ciclo ni CT-04 la mutan (`Bloque` la copia en profundidad).
- **Anonimización:** con un cliente con conocimiento previo, la evidencia disponible y la contrarréplica llegan anonimizadas, y la evidencia citada se verifica al volver a los símbolos reales.
- **Números:** los nuevos están en `por_defecto.yaml` como `[PROPUESTO]` o con su pregunta para T-57. La excepción es H-08.
- **Cuotas:** bajan, no suben.
- **Pruebas anteriores:** las cambiadas no se debilitan (añaden fechas independientes o activan los 12 perfiles).
- **Resto de lo no aplicado:** tiene su motivo y su destino (T-67, T-57 o K). La excepción es H-06.

### Veredicto

**NO APTO.** H-01 es alta: la regla central de PA-05 («sin evidencia citada y sin confirmación del Contradictor, la objeción fuerte sigue abierta») se salta cuando el modelo devuelve en la contrarréplica ids que no se le pidieron, o repite ids entre opciones. Con eso se entregan en el top-3 opciones con una objeción fuerte abierta. Además, CA-3 no se cumple del todo (H-06).

Siguiente paso: quien implementó corrige H-01 (obligatorio) y, si puede, H-02 a H-08, cada uno con su prueba de regresión. En r02, el revisor vuelve a ejecutar sus scripts `r01_*`.

### Scripts del revisor

En `/tmp/claude-0/-home-claude/d1ab3b3e-4909-5455-a67a-e01975b6ec91/scratchpad/qa_t66/revisores/`. Copiados a `.docs/tickets/T-66/revisores/`.

- `r01_comun.py`: utilidades comunes y un cliente simulado con gancho.
- `r01_01_pa05_contrarreplica.py`: H-01.
- `r01_02_pa01_alcance.py`: H-02 y H-03.
- `r01_03_pa10_certificados.py`: H-04.
- `r01_04_pa03_neff.py`: H-05.
- `r01_05_pa09_pa21_compat.py`: H-07, en parte.
- `r01_06_pa14_ablacion.py`
- `r01_07_mutaciones_evaluacion.sh`
- `r01_08_pa05_anonimizado.py`

Para ejecutarlos:
- Los `.py`: `PYTHONPATH=<ejecutor de A>:<carpeta revisores> /home/claude/repo/.venv/bin/python r01_0N_….py`. Cada uno imprime OK, HALLAZGO o INFO.
- El de mutaciones: `SRC=<raíz de bloque_a> DEST=<carpeta de trabajo> bash r01_07_mutaciones_evaluacion.sh`.

Los registros de esta ronda (suite, gate y mutaciones del ticket) están en `/tmp/claude-0/-home-claude/d1ab3b3e-4909-5455-a67a-e01975b6ec91/scratchpad/qa_t66/suite_a.log`, `/tmp/claude-0/-home-claude/d1ab3b3e-4909-5455-a67a-e01975b6ec91/scratchpad/qa_t66/gate.log` y `/tmp/claude-0/-home-claude/d1ab3b3e-4909-5455-a67a-e01975b6ec91/scratchpad/qa_t66/mut.log`.

## Correcciones tras la r01 (implementación, Claude)

| ID | Corrección | Prueba (falla con `4a92a15`) |
| --- | --- | --- |
| H-01 | El código asigna el id de cada objeción (`OBJ-<ref>-nn`, único por opción) y guarda aparte el del modelo (`id_modelo`). La contrarréplica solo cuenta para las objeciones que se le enviaron | `test_h01_la_contrarreplica_no_resuelve_objeciones_que_no_se_le_enviaron`, `test_h01_ids_repetidos_del_modelo_no_cruzan_entre_opciones` |
| H-02 | Un escalado sin tipo va a los tipos activos (F10 P-02), y AG-01 los recibe en `clases_activas`. El simulado también | `test_h02_un_escalado_sin_tipo_va_a_un_tipo_activo` |
| H-03 | CT-04 rechaza un `clases_activas` vacío o que no sea una lista | `test_h03_clases_activas_vacia_se_rechaza` |
| H-04 | Un `aprobar_certificados` que no es una lista da un único rechazo de formato | `test_h04_aprobar_certificados_que_no_es_lista_da_un_solo_rechazo` |
| H-05 | Ausencia de varianza detectada con tolerancia numérica antes del ANOVA: ρ = 1 y n_eff = número de fechas | `test_h05_residuos_constantes_dan_rho_1_sea_cual_sea_el_valor` (falla con 0,3, 0,35 y 0,123456789) |
| H-06 | Los restos de PA-03, PA-05 y PA-14 están en «No entra» del README y en T-67 | — |
| H-07 | La fila T-66 de la deuda vuelve a EN QA. El README del ejecutor explica que una grabación de replay anterior necesita `backtest.anonimizar: false` | — |
| H-08 | `_prob_analista` lee el rango del esquema `FINALISTA` | Las de PA-21 |

**Comprobación:** los scripts `r01_01` a `r01_08` ya no dan ningún HALLAZGO.

## Ronda r02

- **Revisor:** un revisor nuevo, sin contexto de la implementación ni de la r01 (subagente Claude).
- **Fecha:** 2026-11-10.
- **Commit revisado:** `cb12377` (rama `develop`).

### Reproducción desde limpio

- **Worktree aparte:** `git worktree add --detach …/scratchpad/qa_t66_r02/wt cb12377`.
- **Suite de A:**
  - Con `PYTHONPATH=<wt>/bloque_a/11_Ejecutor` y `/home/claude/repo/.venv/bin/python -m pytest -q -p no:cacheprovider tests`. `bloque_a.__file__` sale del worktree.
  - Resultado: **181 passed** (135 s).
- **Gate completo:** `./tools/check_all.sh` en el worktree, con `.venv` enlazado temporalmente, `PYTHONPATH` hacia los tres ejecutores del worktree, y `RUFF_CACHE_DIR` y `MYPY_CACHE_DIR` fuera del worktree. Resultado: **12/12**.
  - corpus-integridad, nombres-nfc, yaml-configs, secrets y refs-vivas en verde.
  - Cuotas: ruff 3109/3109, mypy A 123/123, FX 174/174 y B 159/159. Son las mismas que en la r01: no suben.
  - pytest: A 181, FX 68 y B 141. La línea base de A sube de 172 a 181 en `tools/cuotas.txt`.
- **Scripts de la r01** (`r01_01` a `r01_06` y `r01_08`, con `PYTHONPATH=<ejecutor del wt>:<wt>/.docs/tickets/T-66/revisores`): **ningún HALLAZGO**.
  - Los escenarios 5 y 6 de `r01_01` (H-01) dan OK.
  - Quedan los INFO conocidos, anteriores a T-66: la excepción del proveedor sube, el F6 manipulado lo sigue leyendo el Evaluador y la grabación de replay anterior necesita `anonimizar: false` (ya documentado).
- **Mutaciones:**
  - `mutaciones_orquestacion.sh` con `SRC=<wt>/bloque_a`: las **11 fallan**.
  - `r01_07_mutaciones_evaluacion.sh`: las **14 fallan**.
  - Mis mutaciones de las correcciones (`r02_03`): 6 de 7 fallan por su aserción. La que no falla es `h02_ejecutor` (H-11).
- **Limpieza:**
  - Worktrees eliminados con `git worktree remove --force`: el de `cb12377` y uno auxiliar de `da3f6cb`, el código anterior a T-66 que usa `r02_02`.
  - `git worktree list` solo muestra el principal y `git status` del repositorio principal sale vacío.
  - No he creado ningún `.ruff_cache` en `bloque_a/`. El que hay en `bloque_a/11_Ejecutor/.ruff_cache` del repositorio principal es anterior a esta ronda (00:29) y lo ignora su propio `.gitignore`.

### Comprobación de las correcciones de la r01

| ID | Estado en r02 | Evidencia |
| --- | --- | --- |
| H-01 | Corregido dentro de un ciclo; **quedan dos caminos por el arrastre** (H-09 y H-10) | `r01_01` escenarios 5 y 6 en OK. `r02_01`, 12/12 OK:<br>• respuestas del Analista con ids de otra opción;<br>• ids del modelo duplicados dentro de una opción (el código asigna 12 ids distintos y solo se resuelve la fuerte con evidencia y confirmación);<br>• el Analista responde con el id del modelo;<br>• contrarréplica con ids inventados, con el formato predecible `OBJ-<ref>-nn` no enviado, en minúsculas o con espacios;<br>• entradas de tipo inesperado;<br>• el mismo id dos veces con True/False en cualquier orden (sigue abierta);<br>• dos tipos con el mismo proxy: `cargar_universo` lo rechaza («símbolos duplicados»), y dentro de una clase los proxies se deduplican;<br>• determinismo de los ids.<br>Las mutaciones `h01_ids` y `h01_enviadas` fallan |
| H-02 | Corregido; la prueba no cubre el ejecutor (H-11) | `r02_04`: si el modelo omite `escalado.clases`, el ejecutor va a `["DIV"]`. Tras un CT-04 `[RV, DIV]`, AG-01 recibe `clases_activas: ["RV","DIV"]` |
| H-03 | Corregido | `r02_04`: `"DIV"`, `{}`, `None`, `[None]`, `[]` y `["DIV","XXX"]` se rechazan, y P-02 queda intacto |
| H-04 | Corregido | `r02_04`: una cadena, un dict o un entero dan un único rechazo de formato. `[None]` y `[[…]]` dan un rechazo por elemento. `[]` no da rechazo ni aprobación |
| H-05 | Corregido | `r02_04`:<br>• constantes 0, 1, 1e6, −0,3 y 0,1+0,2, y una constante con ruido de 1e-15: ρ = 1 y n_eff = 10;<br>• una varianza real de 1e-6 pasa por el ANOVA;<br>• NaN e infinito dan ValueError.<br>La mutación `h05` falla en 3 de 4 casos (con 0,5 ya daba ρ = 1 antes de corregir) |
| H-06 | Corregido | «No entra» del README de T-66 y fila T-67 de la deuda («Restos de propuestas aplicadas a medias»: PA-03, PA-05 y PA-14) |
| H-07 | Corregido | Fila T-66 de la deuda en EN QA. Nota de replay en el README del ejecutor (línea 246) |
| H-08 | Corregido | `r02_04`: `_prob_analista` acepta los límites del esquema (0,05 y 0,95) y rechaza los valores fuera de rango por 1e-9, un bool, una cadena y NaN |

### Criterios de aceptación

| Criterio | Cumple | Evidencia |
| --- | --- | --- |
| CA-1 · cada propuesta aplicada tiene una prueba que falla sin ella | sí | 11 + 14 mutaciones fallan por su aserción. La regresión de H-02 no protege la corrección del ejecutor (H-11), y el efecto de PA-05 en el arrastre no tiene prueba (H-09) |
| CA-2 · suites y gate en verde, línea base subida | sí | A 181, FX 68 y B 141; gate 12/12; cuotas sin subir |
| CA-3 · lo no aplicado, con motivo y destino | sí | README de T-66 («No entra»), T-67 y T-57 en la deuda |
| CA-4 · el Documento 0 no se toca; el comportamiento, en el README del ejecutor y en INC-T66-xx | no | Documento 0 sin cambios y corpus-integridad en verde. Pero el cambio de `objecion_id` (lo asigna el código, y el del modelo pasa a `id_modelo`) no está documentado (H-13) |

### Hallazgos

| ID | Gravedad | Cómo reproducirlo | Esperado / obtenido | Corrección sugerida | Estado |
| --- | --- | --- | --- | --- | --- |
| H-09 | **alta** | `r02_02_arrastre.py`, escenario B (solo código corregido): alta en 2026-06-05 con una fuerte resuelta en contrarréplica; a la semana siguiente el Analista no repite las finalistas y las vigentes se arrastran | **Esperado** (PA-05: «el veredicto lo calcula una regla y tiene efecto»; invariante: los controles nunca se relajan solos): una tesis frágil sigue siendo especulativa mientras no se vuelva a refutar.<br>**Obtenido:** `_desde_f3` no restaura `_veredicto` (ni `_veredicto_contradictor`) desde `veredicto_refutacion` de F3, y `sintesis.py` (línea 317) solo pone «especulativo» si `f["_veredicto"] == "tesis frágil"`.<br>• **Ciclo 1:** 3 publicadas «especulativo», con «tesis frágil».<br>• **Ciclo 2 (arrastre):** las 3 salen «probable», sin evidencia nueva, y la versión 2 de F3 guarda `veredicto_refutacion: null`, con lo que se pierde el veredicto.<br>El arrastre (N1) es el ciclo semanal habitual, así que el efecto de PA-05 dura una semana. Ya estaba en `4a92a15` | • En `_desde_f3`, restaurar `_veredicto` y `_veredicto_contradictor` desde F3.<br>• Si faltan, recalcularlos con `_veredicto_refutacion(f)` sobre `objeciones_internas`.<br>• Añadir una prueba de dos ciclos (alta frágil → arrastre) | abierto |
| H-10 | media | `r02_02_arrastre.py`, escenario A: ciclo 1 con el código anterior a T-66 (`da3f6cb`), en el que el Analista da la fuerte por resuelta sin evidencia; ciclo 2 con `cb12377` sobre el mismo estado | **Esperado** (pregunta de H-01): ninguna fuerte queda resuelta sin evidencia citada verificable y sin la confirmación del Contradictor.<br>**Obtenido:** `_desde_f3` copia `objeciones_internas` tal cual. Las fuertes antiguas (`resuelta: true`, sin `evidencia_citada` ni `contrarreplica`, con el id del modelo `OBJ-XLU-09`) cuentan como resueltas en `_puertas` (N1), G2 pasa, y las 3 opciones se vuelven a publicar VIGENTE en el top-3. La integridad da `true`: el estado es legítimo, no está manipulado.<br>Es media y no alta porque exige un estado persistido antes de T-66: el repo no tiene ninguno y A no ha corrido en modo sombra. El diseño de T-66 dice «sin migración», pero solo trata F4 | • Al leer F3 para el arrastre, tratar como abierta (falla cerrado) toda fuerte con `resuelta: true` sin `evidencia_citada` o sin la clave `contrarreplica`.<br>• O, si no, volver a refutar la opción.<br>• Anotarlo en INC-T66-02 y añadir una prueba con un registro F3 de formato anterior | abierto |
| H-11 | baja | `r02_03_mutaciones_correcciones.sh`, mutación `h02_ejecutor`: `… if c in CLASES] or activas` → `or ["RV"]` | **Esperado:** `test_h02_un_escalado_sin_tipo_va_a_un_tipo_activo` falla.<br>**Obtenido:** pasa, porque el simulado de AG-01 siempre devuelve `escalado.clases` (`mock_respuestas._coordinador`). La corrección del ejecutor funciona (`r02_04`), pero ninguna prueba la protege | Una prueba en la que AG-01 omita `escalado.clases` (con monkeypatch de `_coordinador`) | abierto |
| H-12 | baja | `r02_04`, última comprobación; `r02_01`, escenario 1 | **Esperado:** la contrarréplica le muestra al Contradictor la evidencia citada, para que confirme esa objeción con fundamento.<br>**Obtenido:**<br>• 4 de las 8 evidencias citadas llegan con `afirmacion: null`: son los `CALC-`, que no son piezas.<br>• Los `CALC-` son de la clase entera: `CALC-2026-0001` está en la evidencia disponible de todas las opciones, así que el filtro «evidencia de otra opción» no se les aplica.<br>• `referencias.por_id` acepta cualquier referencia del almacén.<br>Sigue fallando cerrado (sin la confirmación no se resuelve), pero un modelo real confirmaría viendo un id sin contenido | • Incluir en la contrarréplica el resultado de cada `CALC-` (método, valor y símbolo) y la afirmación de cada `REF-`.<br>• Aceptar como «verificable» solo el `CALC-` que se refiera al proxy de la opción | abierto |
| H-13 | baja | Buscar `id_modelo` u `OBJ-<ref>` en el README del ejecutor y en `docs/incidencias.md`: 0 coincidencias | **Esperado** (CA-4): los cambios de comportamiento, en el README del ejecutor y en INC-T66-xx.<br>**Obtenido:** no consta que `objecion_id` en F3 y en el paquete lo asigne ahora el código (`OBJ-<proxy>-nn`), ni el campo nuevo `id_modelo` | Una línea en la sección T-66 del README del ejecutor y en INC-T66-02, junto con lo de los registros antiguos (H-10) | abierto |

**Observaciones sin hallazgo:**
- `_TOL_VARIANZA = 1e-12` (H-05) es una tolerancia numérica escrita en el código. Lleva su comentario («no es un umbral de decisión») y tiene precedentes en el bloque (`tol` de 1e-10 y 1e-8 en `motor/servicio.py` y 1e-9 en `evaluador.py`).
- Si una contrarréplica repite un id con True y False, el diccionario se queda con la última entrada. Aun así, la fuerte sigue abierta en los dos órdenes probados, porque el escenario exige la evidencia y la confirmación juntas (`r02_01`, escenario 4). Bastaría un «todas las entradas dicen true» para que fuera robusto por construcción.
- Siguen igual que en la r01 (y anteriores a T-66): la excepción del proveedor corta el ciclo, y el Evaluador lee el F6 manipulado aunque lo detecte `verificar_integridad`.

### Sin hallazgo en lo comprobado

- **H-01 dentro de un ciclo:** la contrarréplica solo cuenta para los pares (ref, id) que se le enviaron, y los ids los asigna el código, únicos por opción. No cruzan entre opciones ni dentro de una opción, y el id del modelo no resuelve nada.
- **Falla cerrado:**
  - contrarréplica no conforme, caída, con entradas raras o contradictorias: la fuerte sigue abierta;
  - evidencia inventada o de otra opción (fuentes HT-01): se filtra;
  - CT-04 mal formado (`clases_activas` o `aprobar_certificados`): se rechaza sin tocar F10 ni F6;
  - `n_eff` sin varianza: ρ = 1; con NaN o infinito: ValueError.
- **Números:** no hay números nuevos de decisión escritos a mano en `cb12377`. El rango del Analista sale del esquema (H-08). Los valores del operador siguen en `por_defecto.yaml` como `[PROPUESTO]`.
- **Determinismo:** mismos ids y misma resolución en dos ejecuciones (`r02_01`). Salida idéntica en `r01_02`.
- **Cuotas:** ruff 3109, mypy A 123, FX 174 y B 159. No suben.
- **Lo no aplicado:** tiene su motivo y su destino en el README de T-66 y en T-67 (`sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md`), y lo del operador en T-57.
- **No hay LLM en el veredicto:** lo calcula `_veredicto_refutacion`, por regla.
- **Secretos:** el gate secrets está en verde. Los scripts r02 no contienen datos personales.

### Veredicto

**NO APTO.** H-01 está bien corregido dentro de un ciclo, y H-02 a H-08 también. Pero H-09 es alta: en el arrastre, el ciclo semanal habitual, la tesis frágil pierde su veredicto en F3 y vuelve a «probable» sin evidencia nueva. Es decir, el efecto que PA-05 obliga a aplicar se relaja solo a la semana siguiente. Además, H-10 deja un camino abierto, solo con estado anterior a T-66, por el que una fuerte resuelta sin evidencia ni contrarréplica se vuelve a publicar. Y CA-4 no se cumple del todo (H-13).

Siguiente paso: quien implementó corrige H-09 (obligatorio) y H-10 en `_desde_f3`, que es la misma función, y si puede H-11 a H-13, cada uno con su prueba de regresión. En la r03, el revisor vuelve a ejecutar los scripts `r01_*` y `r02_*`.

### Scripts del revisor

Están en `/tmp/claude-0/-home-claude/d1ab3b3e-4909-5455-a67a-e01975b6ec91/scratchpad/qa_t66_r02/revisores/`. Copiados a `.docs/tickets/T-66/revisores/`.

- `r01_comun.py`: copia de la r01; los r02 lo importan.
- `r02_01_h01_caminos.py`: caminos de H-01 dentro de un ciclo.
- `r02_02_arrastre.py` y `r02_02_paso_arrastre.py`: H-09 y H-10.
- `r02_03_mutaciones_correcciones.sh`: mutaciones de H-01 a H-05; H-11.
- `r02_04_correcciones_bordes.py`: bordes de H-02 a H-05 y H-08; H-12.

Para ejecutarlos:
- **Los `.py`:** `PYTHONPATH=<ejecutor de A>:<revisores r01>:<revisores r02> /home/claude/repo/.venv/bin/python r02_0N_….py`. Cada uno imprime OK, HALLAZGO o INFO.
- **`r02_02`:** `NUEVO=<ejecutor de A> PRE=<ejecutor de A en un worktree de da3f6cb> R01=<revisores r01> python r02_02_arrastre.py`.
- **El de mutaciones:** `SRC=<raíz de bloque_a> DEST=<carpeta de trabajo> bash r02_03_mutaciones_correcciones.sh`.

Los registros de esta ronda están en `/tmp/claude-0/-home-claude/d1ab3b3e-4909-5455-a67a-e01975b6ec91/scratchpad/qa_t66_r02/`:
- suite: `suite_a.log`
- gate: `gate.log`
- scripts r01: `r01_rerun.log`
- mutaciones: `mut_orq.log`, `mut_ev.log` y `mut_r02.log`
- scripts r02: `r02_01_h01_caminos.log`, `r02_02_arrastre.log` y `r02_04_correcciones_bordes.log`

## Correcciones tras la r02 (implementación, Claude)

| ID | Corrección | Prueba |
| --- | --- | --- |
| H-09 | `_desde_f3` conserva el veredicto de Contrarias desde F3 o, si falta, lo recalcula con la regla; en el arrastre, una tesis frágil sigue siendo «especulativo» | `test_h09_la_tesis_fragil_sigue_siendo_especulativa_en_el_arrastre` (falla con `cb12377`) |
| H-10 | En el arrastre, una fuerte resuelta sin `evidencia_citada` o sin `contrarreplica` se vuelve a abrir (`reabierta_por`) y se recalcula el veredicto | `test_h10_una_fuerte_antigua_resuelta_sin_evidencia_se_reabre_en_el_arrastre` (falla con `cb12377`) |
| H-11 | Prueba en la que AG-01 omite `escalado.clases`: el ejecutor va a los tipos activos | `test_h11_el_ejecutor_lleva_a_tipos_activos_un_escalado_sin_clases` (falla con la mutación `or ["RV"]`) |
| H-12 | La contrarréplica muestra el contenido de cada evidencia citada: la afirmación de la pieza, el método y los valores de un CALC- o el título de una REF-. El límite de los CALC- de todo el tipo queda en INC-T66-02 | `test_h12_la_contrarreplica_muestra_el_contenido_de_cada_evidencia` (falla con `cb12377`) |
| H-13 | `objecion_id` e `id_modelo` documentados en el README del ejecutor y en INC-T66-02 | — |

Pendiente: la ronda r03.
