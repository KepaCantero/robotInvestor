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

Pendiente: la ronda r02 de QA.
