# T-65 · QA independiente

- **Revisor:** revisor nuevo sin contexto de la implementación (Claude, subagente de QA) · **Ronda:** r01 · 2026-11-10

## Reproducción desde limpio

- Copia limpia: `git worktree add --detach` sobre `develop` (9a5225d) más solo los ficheros de T-65 (`bloque_a/`, `tools/refs_vivas.py`, `.docs/scripts/prueba_refs_vivas.py` y `.docs/tickets/T-65/`), sin nada de T-80.
- Gate completo (`./tools/check_all.sh`, el mismo que `.docs/scripts/gate.sh --completo`) en esa copia: **11/12**. Pasan corpus-integridad, nombres-nfc, yaml-configs, secrets, ruff (3083, cuota 3109), los tres mypy (123, 174, 159) y las tres suites (A 265, A-Forex 68, B 174). **Falla `refs-vivas`** por una cita del propio ticket (H-03, abajo). En el árbol de trabajo pasa solo porque allí existe el log local.
- `pytest -q bloque_a/11_Ejecutor`: 265 passed (antes 201).
- `.docs/tickets/T-65/mutaciones.py` en la copia: 39 de 39 mutaciones detectadas.
- `.docs/scripts/prueba_refs_vivas.py`: 6/6.
- Sondas propias en `revisores/` (r01_01 a r01_07). También se repitieron r2_01 y r2_06 de la QA de T-53 (dentro de r01_01), y r04_02 y r04_05 de la QA de T-66.

## Criterios de aceptación

| Criterio | Cumple | Evidencia |
| --- | --- | --- |
| CA-1 · cada punto hecho tiene una prueba que falla sin la corrección | sí, con huecos bajos | Las 39 mutaciones fallan. Con `r01_07_mutaciones_extra.sh` sobre la suite entera hay mutaciones que no detecta ninguna prueba (H-08, abajo). |
| CA-2 · los puntos ya hechos citan su prueba y pasa | sí | H-06 (`test_t66_propuestas.py::test_h06_todo_pausado_no_redacta_ni_falla_en_el_esquema`) y H-12 (`test_t53_seleccion_y_entrega.py::test_h12_dos_bloques_con_la_misma_configuracion_no_comparten_la_tabla_de_horizontes`) pasan en la suite. |
| CA-3 · cada punto no hecho o hecho en parte, con su motivo y su destino | sí | P-07 y el ρ del prompt (CS-10 y CS-18) van a T-57 y a la revisión del corpus, y F10 con 44 parámetros a T-83 y T-57. El README los da por no hechos. |
| CA-4 · ningún número nuevo en el código; los del operador, `[PROPUESTO]` | sí, con restos de H-08 | Los números nuevos están en `por_defecto.yaml`, y los del operador llevan `[PROPUESTO]` y su pregunta. Quedan literales de respaldo antiguos (H-05). |
| CA-5 · suite > 201 y gate 12/12 | **no** | Suite 265. El gate da 11/12 desde limpio por una cita del propio `pruebas.md` (H-03). |
| CA-6 · sin tocar lo prohibido; corpus intacto | sí | `git status` (lo de T-65): `bloque_a/11_Ejecutor/`, `tools/refs_vivas.py`, `.docs/scripts/prueba_refs_vivas.py` y el ticket. `corpus-integridad` en verde. |

### Punto por punto

| Punto | ¿Corregido? | Evidencia del revisor |
| --- | --- | --- |
| H-07 | sí | La tabla vive en la instancia. Ningún módulo usa ya la tabla global para publicar (`grep`). La prueba adaptada de T-53 sigue comprobando lo que comprobaba, ahora en la instancia, y además que el `Evaluador` falla con una tabla mala: no se debilita. |
| H-08 | en parte | `parametro()` falla con `KeyError` si falta la clave o es nula. Quedan literales de respaldo que repiten el YAML (H-05). |
| H-09 | sí, en el YAML | Las INC-T53-01 a 05 llevan `[PROPUESTO]` junto a su clave. `docs/incidencias.md` sigue sin marcar y con un texto rancio (H-09, baja). |
| H-10 (a, b, c) | sí | Mutaciones detectadas. r01_01: incidencia `DATOS` con su `run_id` y motivo propio. |
| H-11 | sí | r01_02: 12 casos OK y 0 citas rotas en el repo. Queda una relajación menor (H-06). |
| H-13 | sí | `efecto_desde` y `fecha_efecto` = as_of. |
| H-14 | sí | La rama se ejercita con `monkeypatch`. |
| H-15 | **en parte, con una regresión** | r01_01: los cierres a cero, negativos, no finitos o duplicados, la columna que falta y la fecha ilegible se excluyen y se declaran, también cuando el símbolo es el proxy de una vigente. **Pero** un CSV ilegible tumba todo el ciclo (H-02), y un cierre ≤ 0 antiguo vacía el tipo en silencio (H-01, regresión). |
| H-16 | sí, con un resto | r01_01, casos e y g de r2_01: los clústeres se calculan para el resto y el proxy corto se declara. Antes, rechazo para todos. Queda el caso de dos proxies medibles sin solape (H-07, baja). La prueba adaptada de T-53 exige ahora la limitación concreta y PARCIAL: no se debilita. |
| H-17 | sí, con un resto | r01_06: rechaza tipos y fechas malas. Acepta `" 1-25"` y dígitos no ASCII, que luego no casan nunca (H-04). |
| H-20 | sí | r04_05 de T-66: 4/4 OK. |
| H-21 | sí | r04_02 de T-66 marca ahora HALLAZGO en «3 · el Contradictor recibe la afirmación saneada»: es la opción que la propia QA de T-66 proponía (no sanear el texto del Analista). El mensaje de refutación principal ya le pasaba esa pieza sin sanear, y los Analistas no tienen búsqueda web (`busqueda_web.agentes`). Se acepta. |
| CA-14 resto | sí | Las sesiones salen de `horizontes` y `calendario`. Tasa base, zona de interés y confianza, de la configuración. Sin σ, el delta es material y se declara. |
| CA-15 | sí (lo declarado) | r01_05: `participantes` y `msg_id` iguales en 5 de 5 ejecuciones (en HEAD, 5 órdenes distintos). Sigue el no determinismo del consumo por tipo en F5, que no es de T-65 (H-10, baja). |
| CS-08 | sí | Las tres fichas se rechazan y no se ofrecen como alternativa. Ningún camino del ciclo las pide. |
| CS-10 resto | sí, con pruebas débiles | Réplicas y rotación con prueba de efecto. PS1, pregunta repetida y recalibración de RK solo con una prueba que lee el código fuente (H-08). |
| CS-11 | sí | Los regímenes coinciden con el esquema F10 (prueba contra el `.md`). `parametros_ht03` es igual al corpus. |
| CS-18 | sí | La ventana sale de `clusteres.ventana_semanas` (156). r01_03: frente a HEAD solo cambian 4 `cluster_id` de F3 y los RC de ML-CLUS-001. F4 es idéntico. |
| CS-19 y CS-23 | sí | Las pruebas pasan, y la mutación del mapa y la de la cita fallan. |

### Regresión frente a HEAD y determinismo (r01_03, r01_05)

- **Backtest simulado de 4 semanas con los 12 tipos y 4 hilos (r01_03).** Frente a HEAD, F4 es idéntico. En F3 solo cambian 4 `cluster_id`, por la ventana de 156 semanas. Los RC cambian en ML-CLUS-001 y en el texto «tasa base 0.5» (H-11). En F5 cambian `participantes` y los `msg_id`. Los prompts no cambian: la instrucción REVISION_VIGENTES da el mismo texto con 2 celdas.
- **Determinismo.** Entre dos ejecuciones iguales del árbol de T-65 solo cambian las rutas absolutas, el orden de `cache_resultados.jsonl` (declarado) y `presupuesto.*.consumido` con su suma, que tampoco es determinista en HEAD (H-10).

## Hallazgos

| ID | Gravedad | Cómo reproducirlo | Esperado / obtenido | Corrección sugerida | Estado |
| --- | --- | --- | --- | --- | --- |
| H-01 | media | `r01_04_cierre_malo_antiguo.py`: los 6 pares DIV de ejemplo con historia desde 2019 y **un** cierre 0 (o −1) en 2019, fuera de la ventana de 3 años del lote. Se ejecuta la misma sonda en HEAD | **Esperado:** el cierre antiguo no importa (está fuera de la ventana) o el símbolo se excluye y se declara.<br>**Obtenido:** regresión de H-15. La validación nueva de `cierres()` mira todo el rango pedido, y `valor_en()` pide la historia entera (`cierres(simbolo, None, fecha)`). En `senales_clase` (`bloque_a/orquestacion.py:378-384`) el `except DatosNoDisponibles: pass` traga el `DatosInvalidos`, y los 6 símbolos se quedan sin `precio` ni `fecha_dato`. PS2 falla (edad 999) y DIV queda con **0 opciones, estado COMPLETO, sin limitación ni incidencia**. Es el mismo patrón que H-01 de T-53 (media). **HEAD: 3 opciones.** Por la misma raíz, todo pronóstico de ese símbolo queda sin resolver (`Evaluador.rentabilidad` usa `valor_en`) y una vigente no se reconstruye en el arrastre | Que `valor_en` valide solo el cierre que devuelve (o una ventana acotada), no toda la historia. Que el control de `senales_clase` use el mismo rango que las lecturas posteriores, y que un `DatosInvalidos` de `valor_en` excluya y declare el símbolo, en vez de dejarlo sin precio en silencio. Prueba: cierre 0 antiguo → el tipo conserva sus opciones, o se declara | abierto |
| H-02 | media | `r01_01_datos_raros.py`, casos «binario», «vacio_0_bytes» y partes C y E: un CSV de 0 bytes o binario en un símbolo del universo | **Esperado** (H-15: «cualquier error del proveedor para ese símbolo»; `analisis-tecnico.md`: «un CSV mal formado … es `DatosInvalidos`»; README del ejecutor, 5 bis): el símbolo se excluye y se declara.<br>**Obtenido:** `EmptyDataError` o `ParserError` de `pd.read_csv` (`bloque_a/11_Ejecutor/bloque_a/herramientas/ht01_datos.py:228`), fuera de `_normalizar_df`. El cribado lo excluye (`except Exception`), pero `Evaluador.tasa_base` con referencia `CESTA` vuelve a leer el símbolo y solo atrapa `DatosNoDisponibles`. **Cae el ciclo de los 12 tipos** (parte E), también si el CSV roto es el del proxy de una vigente (parte C). No es una regresión (en HEAD caía antes), pero la corrección dice cubrirlo | Envolver la lectura del CSV (`read_csv` y la decodificación) para que cualquier error de lectura sea `DatosInvalidos` del símbolo. Prueba con un CSV de 0 bytes y otro binario en un ciclo de varios tipos | abierto |
| H-03 | media | Gate completo en una copia limpia (worktree con solo los ficheros de T-65) | **Esperado** (CA-5): 12/12.<br>**Obtenido:** 11/12. `refs-vivas` da «ROTA: .docs/tickets/T-65/pruebas.md cita ruta inexistente» porque cita el log de `.docs/scripts/.logs/`, que no se sube. En el árbol de trabajo pasa solo porque el log existe en local. Con el commit, el gate queda en rojo en cualquier clon | Citar el log sin comillas de código o sin la ruta (solo el nombre del archivo), como ya se hace con el de la primera ejecución | abierto |
| H-04 | baja | `r01_06_festivos_ps2.py` | **Esperado:** `fijos` solo admite «MM-DD» con dígitos ASCII.<br>**Obtenido:** `" 1-25"` y `"١٢-٢٥"` se aceptan (`pd.Timestamp` los interpreta), pero `_sesiones_entre` compara con `strftime("%m-%d")` y no casan nunca: ese festivo se ignora en silencio | Validar con `re.fullmatch(r"\d\d-\d\d", d, re.ASCII)` además de la fecha | abierto |
| H-05 | baja | `grep` de `.get(…, número)` en el paquete | **Esperado** (H-08): ningún número de configuración con un literal de respaldo en el código.<br>**Obtenido:** quedan `seguimiento.frecuencias` (7) y `frecuencia_orientativa_dias` (7) en `bloque_a/seguimiento.py:52` y `:89`, `uc.motor_por_plan` (0,02) en `bloque_a/motor/servicio.py:310`, `max_tokens` (8000) en `bloque_a/configuracion.py:205` y el 0,1 del texto de GC0 en `bloque_a/orquestacion.py:452`. Además, el 0,5 de la tasa base de los hitos H5 (`bloque_a/sintesis.py:212`), que es `tasa_base.sin_historia`, y los «10 días hábiles» del texto de `regla_fallback`, que es `evaluacion.dias_habiles_no_resoluble` | Pasarlos a `parametro()` o declararlos en los límites conocidos | abierto |
| H-06 | baja | `r01_02_refs_vivas.py`, casos INFO | **Esperado:** el cambio de H-11 no hace pasar citas rotas.<br>**Obtenido:** en una orden solo se comprueba la primera palabra. `` `tools/a.py bloque_a/no_existe.csv` `` y `` `tools/a.py tools/no_existe.py` `` pasan; con el script anterior fallaban. Es una relajación menor, documentada en el docstring | Comprobar también los argumentos que empiezan por una raíz conocida | abierto |
| H-07 | baja | `r01_01_datos_raros.py`, parte D: dos proxies con ≥ 52 semanas cada uno, sin solape | **Obtenido:** ML-CLUS-001 se rechaza para todos («series no alineables»). Se declara y el run queda PARCIAL. Es el resto de H-16: el filtro mira la historia de cada proxy, no la común | Excluir por solape con el resto, o pasar a la deuda | abierto |
| H-08 | baja | `r01_07_mutaciones_extra.sh` sobre una copia (suite entera de A) | **Esperado** (CA-1): cada cambio con una prueba de efecto.<br>**Obtenido:** si se vuelve a escribir el número en el código, la suite entera pasa en dos casos: «pregunta repetida» con `veces` a 3 y la recalibración de RK con `paso` a 0,05. Las pruebas de PS1, pregunta repetida y recalibración de RK (CS-10) solo buscan la clave en el código fuente (ver «Mutaciones adicionales») | Pruebas de efecto con un valor distinto en la configuración (como en `test_cs10_celdas_de_rotacion_exploratoria_de_la_configuracion`) | abierto |
| H-09 | baja | Lectura de `docs/incidencias.md` | INC-T53-02 a 05 siguen como «Decisión», sin `[PROPUESTO]`. INC-T53-04 dice aún que la degradación «todavía no cambia la tabla … pendiente en T-53», ya falso desde T-53 r02, y no recoge H-13. El README lo deja para el coordinador | Actualizarlo al cerrar (coordinador) | abierto |
| H-10 | baja | `r01_05_presupuesto_paralelo.py`, 5 ciclos iguales con 12 tipos y 4 hilos, en HEAD y en T-65 | `presupuesto.<tipo>.consumido` de F5 varía entre ejecuciones (3 valores distintos en T-65 y 4 en HEAD), y `consumo.uc` cambia en el cuarto decimal (orden de suma). No lo introduce T-65, y CA-15 solo declaraba participantes y `msg_id`. Es un registro sustantivo: con un presupuesto justo, puede cambiar qué fase se cierra | A la deuda: asignar el consumo de las llamadas compartidas en orden determinista | abierto |
| H-11 | baja | r01_03, RC de RI-TB | El texto de la limitación pasa de «tasa base 0,5 por defecto» a «tasa base 0.5»: se pierde la coma decimal en un texto en español | Formatear con coma | abierto |

Información (no son hallazgos):
- `parametro(cfg, "sección.clave")` cae en `por_defecto.yaml` si la sección entera es `null` en la configuración del usuario. Pedir la sección entera sí falla. Es coherente con la caída documentada, pero un `evaluacion:` vacío por error pasa sin aviso.
- La deduplicación de R9 (`_r9_contrarreplica`) se comprueba y se actualiza sin cerrojo desde los hilos de los tipos. Una carrera solo daría una incidencia de más.

### Mutaciones adicionales (r01_07)

Resultado de `r01_07_mutaciones_extra.sh` sobre la copia limpia (suite entera de A con `-x`):

| Mutación | Resultado |
| --- | --- |
| CS-10 · pregunta repetida: `veces` vuelve a 3 en el código | **pasa la suite** (no se detecta) |
| CS-10 · recalibración de RK: `paso` vuelve a 0,05 en el código | **pasa la suite** (no se detecta) |
| CS-10 · PS1: raíces mínimas vuelven a 2 | falla, pero solo porque la prueba que lee el código fuente ya no encuentra la clave |
| H-10 c · sin incidencia `DATOS` en HA | falla (se detecta) |
| H-16 · run COMPLETO con proxies sin medir | falla (se detecta) |

## Veredicto

**NO APTO.** Hay tres hallazgos medios confirmados:
- H-01, una regresión de H-15: un cierre ≤ 0 antiguo vacía el tipo en silencio, con el run COMPLETO.
- H-02: un CSV ilegible sigue tumbando el ciclo entero, aunque la corrección dice cubrirlo.
- H-03: el gate da 11/12 desde limpio por una cita del propio ticket.

El resto del alcance está bien corregido: las 39 mutaciones se detectan, el corpus y los prompts no cambian, y el determinismo de participantes y `msg_id` está resuelto. Para la r02: corregir H-01 a H-03 con su prueba de regresión, y los bajos o su paso a la deuda con su ID. El revisor volverá a ejecutar r01_01 a r01_07.

---

# Ronda r02

- **Revisor:** revisor nuevo sin contexto de la implementación (Claude, subagente de QA) · **Ronda:** r02 · 2026-11-10 · sobre `develop` 052e79a (commit con las correcciones de la r01).

## Reproducción desde limpio

- Copia limpia: `git worktree add --detach` de 052e79a, con un enlace a `.venv` y sin nada más (las correcciones ya están en el commit). Se comprobó que `pytest` importa el paquete de la copia, no el del árbol de trabajo.
- Gate completo (`.docs/scripts/gate.sh --completo`) en esa copia: **12/12**. corpus-integridad, nombres-nfc, yaml-configs, secrets, refs-vivas, ruff, los tres mypy y las tres suites (A 285, A-Forex 68, B 174). **H-03 corregido.**
- `pytest -q bloque_a/11_Ejecutor` en el árbol de trabajo: 285 passed.
- `.docs/tickets/T-65/mutaciones.py` en otra copia: **50 de 50** detectadas. `r01_07_mutaciones_extra.sh`: las 5 detectadas (antes, 2 pasaban la suite). La copia queda intacta tras restaurar.
- `.docs/scripts/prueba_refs_vivas.py`: 8/8; con el script de b699d4f, 7/8 (falla el caso nuevo de H-06).
- Sondas de la r01 repetidas: r01_01 (23 casos, 0 hallazgos), r01_02 (0), r01_04 (0: con el cierre malo de 2019, DIV conserva sus 3 opciones), r01_05 (H-10 sigue, ya en la deuda), r01_06 (0), r01_07 (arriba). Sondas nuevas: r02_01 a r02_03.

## Hallazgos de la r01

| ID | ¿Corregido? | Evidencia del revisor |
| --- | --- | --- |
| H-01 (media) | **sí** | r01_04 y r02_01 parte D (cierre 0 en 2019 y en 2023-02, fuera de la ventana del lote, en todos los pares DIV): DIV conserva 3 opciones y nada se declara de más. `valor_en` valida solo el cierre que devuelve; las demás lecturas validan solo su rango, y todas caen dentro de la ventana del lote (tasa base 3 años, clústeres 156 semanas, GC0 104 semanas). Un cierre 0 dentro de la ventana excluye y declara el símbolo (r02_01 B). |
| H-02 (media) | **en parte** | CSV vacío, binario, UTF-16, latin-1, truncado, con punto y coma, con campos de más, desordenado y duplicado: `DatosInvalidos` del símbolo, que se excluye y se declara, y el ciclo de los 12 tipos sigue (r01_01 E, r02_01 A y B). **Pero** otras dos formas de CSV siguen tumbando el ciclo entero (H-13, abajo). |
| H-03 (media) | **sí** | Gate 12/12 desde la copia limpia. |
| H-04 | sí | r01_06: 18 de 18; `" 1-25"` y los dígitos no ASCII se rechazan. |
| H-05 | sí | Los literales citados pasan a `parametro()`; `presupuesto_uc.fraccion_minima_comun` es nuevo y lleva `[PROPUESTO]` técnico. Prueba de efecto con otros valores. Quedan los valores por defecto de los parámetros de las fichas del Motor (`motor/servicio.py`), que no eran del alcance. |
| H-06 | sí | r02_02: los argumentos rotos de una orden fallan y los vivos pasan; el repo real tiene 0 citas rotas. Restos menores en H-15. |
| H-07 | sí | r01_01 D: con dos proxies sin solape ya no se rechaza ML-CLUS-001 para todos; el que no solapa se declara. |
| H-08 | sí | r01_07: las tres mutaciones de CS-10 se detectan ahora por efecto. |
| H-09 | sí | `docs/incidencias.md`: INC-T53-02 a 05 con `[PROPUESTO]` (hasta T-57), INC-T53-04 al día y con H-13. |
| H-10 | a la deuda | Fila T-88 de `sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md`. r01_05 lo sigue reproduciendo (2 valores de `consumido` en 3 ejecuciones). |
| H-11 | sí | «tasa base 0,4 por defecto» con coma; prueba en la suite. |

## Regresión y determinismo

- **Backtest simulado de 4 semanas, 12 tipos y 4 hilos** (r01_03), dos veces con 052e79a y una con f384bef (antes de T-65). Entre las dos de 052e79a solo cambian las rutas absolutas de F5 (y con ellas la cadena de huellas) y el orden de `cache_resultados.jsonl`. Frente a f384bef cambian los mismos archivos que en la r01 (ventana de clústeres, `msg_id` por ámbito, redondeo de `uc` en el cuarto decimal): nada nuevo.
- **Corpus y prompts:** `git diff f384bef 052e79a` solo toca `bloque_a/11_Ejecutor/`, `tools/refs_vivas.py`, `.docs/` y `docs/incidencias.md`; corpus-integridad en verde.
- **Números:** los nuevos están en `por_defecto.yaml`; los del operador, con `[PROPUESTO]`.

## Hallazgos nuevos

| ID | Gravedad | Cómo reproducirlo | Esperado / obtenido | Corrección sugerida | Estado |
| --- | --- | --- | --- | --- | --- |
| H-12 | media | `r02_03_minimos_h12_h13.py` (o `r02_01_datos_raros_ciclo.py C`): ACWI, índice de referencia de RV y de IDX en `indices_referencia`, con **un** cierre 0 el 2026-05-29 (o −5 en 2024, o binario, o sin archivo). Ciclo de RV y DIV, o de los 12 tipos | **Esperado** (H-15: falla cerrado por símbolo, declarado, sin tumbar a los demás tipos): RV e IDX se degradan y lo declaran; el resto sigue.<br>**Obtenido:** **cae el ciclo entero** con `DatosInvalidos`. `Evaluador.tasa_base` lee la referencia con `cierres(referencia, ini, as_of)` (`bloque_a/evaluador.py:248`) sin atrapar nada, y `sintesis.construir` tampoco (`bloque_a/sintesis.py:164`; igual `valor_en(ref, as_of)` en la línea 169). El cribado de RV no lee la referencia, así que nada la valida antes. **Regresión de T-65 para el cierre ≤ 0:** en f384bef el mismo dato daba un run COMPLETO con 3 opciones (cifras con un precio 0, en silencio); ahora no hay paquete para ningún tipo. Con el archivo ausente o binario ya caía antes. Afecta igual a AGG (RF), DBC (MP), REET (INM), BTC-USD (CRI), PSP (ALT) y XEON.DE (MON) | Validar la referencia de cada tipo una vez por ciclo (en `senales_clase` o en `_prospectiva`) con la misma ventana que `tasa_base`; si falla, pronóstico sin referencia (DIRECCIONAL) o tipo PARCIAL, con limitación e incidencia `DATOS`, nunca la caída del ciclo. Prueba: ACWI con un cierre 0 y sin archivo en un ciclo de RV, IDX y DIV → DIV intacto, RV e IDX declarados | abierto |
| H-13 | media | `r02_03_minimos_h12_h13.py` (o `r02_01_datos_raros_ciclo.py A B`): un par DIV nuevo con la cabecera de exportación más común, `Date,Open,High,Low,Close,Adj Close,Volume`, o con fechas con zona horaria (`2026-06-05 00:00:00-04:00`) | **Esperado** (H-02 de la r01: «cualquier error al leer el CSV … es `DatosInvalidos` del símbolo»; el docstring de HT-01 admite los alias `close` y `adj close`): el símbolo se lee bien o se excluye y se declara.<br>**Obtenido:** `close` y `adj close` se renombran los dos a `cierre`, `df["cierre"]` es un `DataFrame` y `_normalizar_df` lanza `AttributeError`; con zona horaria, `serie()` lanza `TypeError` al comparar fechas con y sin zona. Ninguna de las dos es `DatosNoDisponibles`: el cribado las excluye (`except Exception`), pero `tasa_base` con referencia CESTA vuelve a leer al miembro y **cae el ciclo de los 12 tipos**. No es una regresión (f384bef caía igual), pero la corrección de H-02 solo envolvió `pd.read_csv` | Envolver toda la normalización (`_normalizar_df`, incluida la conversión de fechas) para que cualquier error sea `DatosInvalidos`, y rechazar explícitamente las columnas duplicadas tras los alias y las fechas con zona horaria (o fijar la regla de conversión como incidencia). Prueba con los dos CSV en un ciclo de DIV y RV | abierto |
| H-14 | baja | `r02_01_datos_raros_ciclo.py A`, caso «cierres_booleanos»: columna `cierre` con `True` en todas las filas | **Esperado:** `DatosInvalidos` (un booleano no es un precio).<br>**Obtenido:** `pd.read_csv` la lee como booleana, `pd.to_numeric` la convierte en 1,0 y la serie se acepta como un precio constante de 1. Con un solo valor no booleano en la columna sí se rechaza | En `_normalizar_df`, rechazar una columna `cierre` de tipo booleano (o leer `cierre` como texto y convertir) | abierto |
| H-15 | baja | `r02_02_refs_vivas.py`, casos INFO | **Obtenido:** con el cambio de H-06, un argumento con comodín (`tests/test_t65_*.py`) o un archivo de salida que aún no existe (`--salida docs/nuevo.md`) cuentan como rotos, y el gate falla en falso. Siguen sin comprobarse el script detrás de un intérprete (`python3 tools/no.py …`) y un argumento entre comillas; eso ya pasaba antes | Saltar los argumentos con `*` o `?` (o resolverlos con `glob`) y documentar en el docstring que una salida futura va en `tools/refs_allowlist.txt` | abierto |

Información (no son hallazgos):
- Un cierre `NaN` escrito como texto se trata como celda vacía: la fila se descarta y queda en `filas_descartadas`, como una celda vacía. Es el diseño anterior.
- `Motor.servir` lee ahora `uc.motor_por_plan.<plan>` antes de comprobar la ficha. Un plan desconocido daría `KeyError` en vez de un rechazo. Hoy todas las llamadas usan `PLAN_MIN`, y ningún camino del LLM elige el plan.
- La elección de proxies por solape de H-07 es voraz (primero los de más semanas): puede dejar fuera un proxy que otra combinación conservaría, pero es determinista y se declara.

## Veredicto

**NO APTO.** H-01 y H-03 están corregidos, y también los bajos H-04 a H-09 y H-11; H-10 está en la deuda (T-88). Las 50 mutaciones se detectan, el gate da 12/12 desde limpio, y el corpus, los prompts y el determinismo están bien. Pero quedan dos hallazgos medios confirmados en el mismo punto, que un símbolo con datos malos falle solo y declarado:
- H-12: un índice de referencia con un cierre ≤ 0 (o ilegible, o sin archivo) tumba el ciclo de todos los tipos. Para el cierre ≤ 0 es una regresión de la validación de H-15.
- H-13: H-02 está corregido solo en parte. Un CSV con `Close` y `Adj Close`, o con fechas con zona horaria, sigue tumbando el ciclo entero.

Para la r03: corregir H-12 y H-13 con su prueba de regresión, y H-14 y H-15, o pasarlos a la deuda con su ID. El revisor volverá a ejecutar r01_01 a r02_03.

---

# Ronda r03

- **Revisor:** revisor nuevo sin contexto de la implementación (Claude, subagente de QA) · **Ronda:** r03 · 2026-11-10 · sobre `develop` 8d74622 (commit con las correcciones de la r02; el código de producto revisado es el de ese commit).

## Reproducción desde limpio

- Dos copias limpias con `git worktree add --detach` de 8d74622 y un enlace a `.venv` (se comprobó que importan el paquete de la copia). Se quitaron al terminar con `git worktree remove`.
- Gate completo (`.docs/scripts/gate.sh --completo`) en la primera copia: **12/12**. corpus-integridad, nombres-nfc, yaml-configs, secrets, refs-vivas, ruff, los tres mypy y las tres suites (A **300**, A-Forex 68, B 174).
- `.docs/tickets/T-65/mutaciones.py` en la segunda copia: **57 de 57** detectadas; la copia queda intacta. `r01_07_mutaciones_extra.sh`: las 5 detectadas. Mutaciones nuevas en `r03_04_mutaciones_extra.sh`: 2 de 3 pasan la suite entera (H-19).
- `.docs/scripts/prueba_refs_vivas.py`: 15/15.
- Sondas de las rondas anteriores, en el árbol de trabajo (producto = 8d74622): r01_01 (0 hallazgos), r01_02 (0), r01_04 (0), r01_06 (0), r02_01 (0; 43 OK), r02_02 (0 · 0 INFO), r02_03 (0: con ACWI con un cierre 0 o sin archivo, RV queda fuera y declarado y DIV conserva 3 opciones; con `Close`+`Adj Close` o fechas con zona, el par se excluye y el ciclo sigue). r01_05: `presupuesto.<tipo>.consumido` sigue variando entre ejecuciones (H-10, en la deuda como T-88).
- **Determinismo** (r01_03 dos veces, 12 tipos, 4 hilos, 4 semanas): de 27 archivos cambian 8, todos por la misma causa conocida: rutas absolutas y orden de `cache_resultados.jsonl` (declarados) y el redondeo de `consumo.uc` en el cuarto decimal por el orden de suma entre hilos (`consumo.csv`, `metricas.json`, los informes técnicos y F5), que es H-10/T-88. Nada nuevo.
- Sondas nuevas: `r03_01_formas_csv.py` (42 formas de CSV en HT-01), `r03_02_referencias_ciclo.py` (partes A a D: referencias en ciclos completos), `r03_03_refs_vivas.py` (35 casos) y `r03_04_mutaciones_extra.sh`.

## Hallazgos de la r02

| ID | ¿Corregido? | Evidencia del revisor |
| --- | --- | --- |
| H-12 (media) | **sí, en lo que promete; con restos** | r03_02 A: ACWI con `inf`, con `n.d.`, con `Close`+`Adj Close`, con fechas con zona, solo con filas futuras o sin publicar hasta 2027 → RV e IDX fuera, PARCIAL, limitación «referencia de comparación ACWI» y una incidencia `DATOS` por tipo; DIV intacto. Con BOM y cabecera en mayúsculas, una sola fila o NaN en las últimas sesiones se lee y se usa (correcto). Referencia compartida (RV e IDX) y miembro del universo de IDX a la vez: bien. r03_02 C1: la referencia guardada en las vigentes (SPY) se valida aunque la configuración diga ACWI: RV fuera y declarado. r03_02 B: SUBYACENTE con un cierre 0 → los tres indicadores de DER excluidos y declarados uno a uno. r03_02 D: un pronóstico ya emitido con la referencia rota en su fecha de resolución, o sin archivo, queda ABIERTO (espera), no se resuelve. **Pero:** una referencia **obsoleta** pasa la validación y se usa para emitir y para resolver (H-16, media); SUBYACENTE sin archivo cambia a CESTA en silencio (H-17); una vigente que guarda una referencia SUBYACENTE deja fuera el tipo entero (H-18); la parte de las vigentes no tiene prueba (H-19). |
| H-13 (media) | **sí; con un resto** | r03_01: 42 formas (BOM, mayúsculas, espacios, CRLF, separadores `;`, tabulador y `|`, coma decimal, miles, `inf`, `-inf`, `1e309`, `Infinity`, `-0`, texto, NaN, todo NaN, una sola fila, solo cabecera, filas futuras, `fecha_publicacion` futura, `Z`, zonas mezcladas, AAAAMMDD, DD/MM/AAAA, línea de total, campo de más, booleanos, UTF-16, bytes nulos): ninguna excepción sale de HT-01 que no sea `DatosNoDisponibles`; `Close`+`Adj Close`, `cierre`+`valor` y `fecha`+`date` se rechazan con «columnas ambiguas»; la zona horaria, con su motivo propio. **Pero** dos columnas con el **mismo** nombre (`cierre,cierre`, `Close,Close`, `fecha,fecha`) se leen tomando la primera en silencio (H-20). |
| H-14 | sí | r03_01 «cierre booleano» rechazado con motivo propio; mutación detectada. |
| H-15 | **en parte** | r03_03: intérpretes simples (`bash`, `sh`, `.venv/bin/python`, `../../.venv/bin/python`), comillas, comodines `*`, `?`, `[]`, `**` (también de paquete de bloque) y `-o`, `--out`, `--salida`, `--salida=` funcionan; una entrada rota junto a una salida sigue fallando. **Pero** un intérprete con opciones (python3 -I delante del script, la forma que pide la skill de QA) no se comprueba, y un argumento entre comillas con espacios rompe en falso (H-22). |

## Hallazgos de la r01 (siguen corregidos)

H-01 (r01_04 y r03_02 A «cierre negativo en 2019»: fuera de la ventana no importa), H-02 (r03_01: vacío, binario, UTF-16, bytes nulos → `DatosInvalidos`), H-03 (gate 12/12 desde limpio), H-04 (r01_06 24/24), H-05 a H-08 (mutaciones de `mutaciones.py` y r01_07), H-09 (`docs/incidencias.md` sin cambios desde la r02), H-11 (prueba en la suite) y H-06 (r02_02 y r03_03). H-10 sigue en la deuda (T-88).

## Valoración de las decisiones de la r02

- **H-12 (el tipo entero fuera en vez de pronosticar sin referencia): correcta.** La Constitución (§11, «Dato obsoleto o ausente: se detiene la decisión afectada, se marca y se pide verificación»; P13 y P16) pide detenerse y marcar, no rellenar. Las referencias de 8.4 del Documento 0 son una propuesta que ratifica el operador en F10; pasar en silencio de RELATIVO a DIRECCIONAL cambiaría el suceso pronosticado y la referencia ingenua, que es decidir por él (regla 7 de CLAUDE.md). La decisión afectada es el tipo entero porque todos sus pronósticos RELATIVO dependen de esa referencia; para SUBYACENTE la unidad correcta es el indicador, y así está hecho salvo el caso de H-18.
- **H-13 (rechazar `Close`+`Adj Close` en vez de elegir columna): correcta.** Son dos series distintas (precio frente a precio ajustado por dividendos y splits) y la Constitución dice ante datos contradictorios «se conservan ambos, se marca la discrepancia y no se decide sobre ella» (§11); los ajustes son del Bloque K o del operador, no de HT-01. Falla cerrado, por símbolo y con motivo propio. El resto es de documentación: la pregunta queda sin registrar donde la verá el operador (H-23).

## Hallazgos nuevos

| ID | Gravedad | Cómo reproducirlo | Esperado / obtenido | Corrección sugerida | Estado |
| --- | --- | --- | --- | --- | --- |
| H-16 | media | `r03_02_referencias_ciclo.py A` («deja de publicarse en 2025-06») y `r03_02_referencias_ciclo.py D` («ACWI deja de publicarse tras la emisión» y «proxy deja de publicarse tras la emisión») | **Esperado** (Constitución §11: dato obsoleto → se detiene la decisión afectada y se marca; H-12: nunca cifras con una referencia mala): una referencia sin datos recientes deja el tipo fuera y declarado, y un pronóstico no se resuelve sin dato de sus dos series en la resolución.<br>**Obtenido, en la emisión:** `_referencia_invalida` (`bloque_a/orquestacion.py`) solo pide que haya datos válidos en la ventana, no que sean recientes. Con ACWI parada el 2025-06-30, RV e IDX salen **COMPLETO**, sin limitación ni incidencia, con pronósticos RELATIVO cuyo `nivel_referencia_indice` es de hace 11 meses. A los indicadores sí se les exige la antigüedad de PS2 (`ps2_antiguedad_maxima_dias`); a la referencia no.<br>**Obtenido, en el seguimiento:** `Evaluador.resolver` (`bloque_a/evaluador.py`) toma `d1 = max(d1, d1b)` y comprueba la frescura solo de la más reciente. Si la referencia (o el proxy) deja de publicarse tras la emisión, los 4 de 4 PRG H2 RELATIVO de RV quedan **RESUELTOS** con `rent_referencia` 0,0 (o `rent_proxy` 0,0) y `fecha_dato` 2026-05-29, la del otro lado: Brier, calibración y certificados R13 se alimentan con un suceso que no es el pronosticado, en silencio. El `max` viene del commit inicial (no lo introduce T-65), pero es justo el caso que H-12 dice cubrir y el seguimiento de pronósticos emitidos que pedía esta ronda | En `_referencia_invalida`, exigir además que el último cierre de la referencia cumpla la antigüedad de PS2 (el mismo parámetro, sin número nuevo). En `resolver`, comprobar la frescura de cada serie por separado (que ninguna de las dos fechas quede a más de 7 días de `f1`, o usar `min`); si no, esperar y, pasado el plazo, `NO_RESOLUBLE`. Prueba: las dos variantes de r03_02 D (referencia parada y proxy parado) y la de A | abierto |
| H-17 | baja | `r03_02_referencias_ciclo.py B` («SPY sin archivo»), fecha 2026-05-01 | **Esperado** (README de T-65, H-12: «archivo ausente» → incidencia `DATOS` y declarado; regla 7): el indicador de DER cuyo subyacente no tiene datos se excluye y se declara.<br>**Obtenido:** `_referencia` devuelve `CESTA` cuando el subyacente no está en el proveedor, así que DER sale **COMPLETO** con 2 opciones cuyos PRG comparan con la cesta de DER en vez de con SPY, sin limitación ni incidencia. Con SPY presente pero con un cierre 0, en cambio, se excluye y se declara. El docstring dice «si falta, CESTA» pensando en la columna vacía | Distinguir la columna vacía (CESTA, como hoy) del subyacente declarado sin datos (excluir y declarar el indicador, como con un cierre malo) | abierto |
| H-18 | baja | `r03_02_referencias_ciclo.py C` (C2): DER con un subyacente distinto por indicador (^BXM → SPY, ^PUT → VGK, TAIL → ACWI); ciclo 1 sano el 2026-05-01 (vigentes ^PUT y TAIL); ciclo 2 el 2026-05-08 con ACWI con un cierre 0 | **Esperado** (README de T-65, H-12: «con SUBYACENTE, la referencia propia de un indicador malo excluye y declara solo ese indicador»).<br>**Obtenido:** sin vigentes, solo TAIL se excluye y DER sigue (1 opción). Con la vigente de TAIL, ACWI entra en las referencias del tipo (las guardadas en sus vigentes) y **DER entero** queda fuera («referencia de comparación ACWI»). Falla cerrado y se declara, pero deja fuera más de lo dicho | Para un tipo SUBYACENTE, validar la referencia guardada de cada vigente junto a su indicador (excluir ese indicador), no como referencia del tipo | abierto |
| H-19 | baja | `r03_04_mutaciones_extra.sh` sobre una copia limpia (suite entera de A) | **Esperado** (CA-1): cada parte de la corrección con una prueba que falle sin ella.<br>**Obtenido:** pasan la suite (a) quitar las referencias guardadas en las vigentes de la validación (`refs_tipo` solo con la de la configuración) y (b) absorber una `FugaDeInformacion` de la referencia como «referencia inválida» en vez de cortar el ciclo. La (a) es parte de lo que el README dice hacer en H-12 y solo la comprueba r03_02 C1 | Pruebas para las dos (la de C1 de r03_02 sirve de modelo) | abierto |
| H-20 | baja | `r03_01_formas_csv.py` («cierre repetido», «Close repetido», «fecha repetida») y `r03_02_referencias_ciclo.py A` («cierre repetido») | **Esperado** (H-13: «no se elige una en silencio»).<br>**Obtenido:** `pd.read_csv` renombra la segunda columna a `cierre.1` (o `Close.1`), que no es un alias, y se usa la primera sin aviso; con ACWI así, RV e IDX salen COMPLETO con la primera columna | Detectar las cabeceras repetidas antes de los alias (leer la cabecera cruda, o rechazar columnas `X.n` cuyo `X` sea un alias) | abierto |
| H-21 | baja | `r03_01_formas_csv.py` («cierre inf en una fila futura») y `r03_02_referencias_ciclo.py A` («inf en 2019» frente a «cierre negativo en 2019») | **Obtenido:** las comprobaciones de `_normalizar_df` (no numéricos, `inf`, booleanos, fechas duplicadas) miran el archivo entero al cargarlo, también las filas posteriores a as_of y las de fuera de la ventana. En backtest, un dato malo de 2026 excluye el símbolo en una fecha anterior, y la incidencia cita esa fecha futura; y un `inf` en 2019 deja fuera la referencia (y RV e IDX enteros), mientras que un −5 en 2019 no importa (H-01). No lo introduce T-65 (viene de T-53), pero es incoherente con H-01 y con la guardia anti-fuga | Aplazar esas comprobaciones al rango pedido (como `_validar_cierres`), o pasarlo a la deuda con su ID | abierto |
| H-22 | baja | `r03_03_refs_vivas.py` (casos HALLAZGO) | **Obtenido:** (a) un intérprete con opciones (python3 -I seguido de un script de tools/ que no existe, o .venv/bin/python -I con uno de .docs/scripts/) no se salta: se toma `-I` como el script y la ruta rota pasa; es la forma que pide la skill de QA. (b) Desde que se quitan las comillas después de partir por espacios, un argumento entre comillas con espacios (un script vivo seguido de la ruta de un Documento 0 entre comillas) rompe en falso por su primer trozo; antes pasaba. Sin efecto en el repo de hoy (0 citas rotas) | Saltar las opciones que siguen al intérprete (`-I`, `-u`, `-X …`) y partir con `shlex.split` antes de quitar comillas | abierto |
| H-23 | baja | Lectura de `docs/incidencias.md`, de la lista para T-57 del README del ticket y de la sección 4 del README del ejecutor | La decisión de H-13 (qué columna manda si llegan `Close` y `Adj Close`) solo está en `analisis-tecnico.md` y en `handoff.md` («la regla va a T-57»); no está en `docs/incidencias.md` ni en la lista de T-57. El README del ejecutor sigue diciendo «alias admitidos: … `close`, `adj close`» sin avisar de que juntos se rechazan: una exportación de Yahoo con las dos columnas se rechaza entera | Registrar la pregunta como incidencia (o en la lista de T-57) y una línea en la sección 4 del README del ejecutor | abierto |

Información (no son hallazgos):
- Un tipo que queda fuera por su referencia sigue mostrando sus vigentes en el paquete (r03_02 C1: RV con 3 opciones, `estado_semaforo` VERDE, 0 PRG nuevos). Es el modo degradado de PS2 de siempre («datos de mercado no disponibles»): no se calcula nada nuevo con la referencia mala.
- `_referencia` reconoce `SUBYACENTE` y `NINGUNA` sin distinguir mayúsculas, pero `CESTA` solo en mayúsculas: `cesta` se trata como un símbolo, que no existe, y el tipo queda fuera y declarado. Falla cerrado.
- Las referencias con NaN en las últimas sesiones o con una sola fila se usan (fecha del último dato válido; tasa base neutra declarada en RC). Correcto con H-16 corregido.

## Veredicto

**NO APTO.** H-12 y H-13 están corregidos en lo que prometían, con pruebas, 57 de 57 mutaciones detectadas, el gate 12/12 desde una copia limpia, determinismo sin cambios y los hallazgos de la r01 siguen cerrados. Las dos decisiones de la r02 (tipo fuera ante una referencia mala; rechazo de `Close`+`Adj Close`) se ajustan a la Constitución. Pero hay un hallazgo medio confirmado en el mismo punto de H-12:
- H-16: una referencia de comparación **obsoleta** pasa la validación (RV e IDX COMPLETO con un nivel de referencia de hace 11 meses), y el seguimiento resuelve pronósticos RELATIVO ya emitidos con una de sus dos series congelada (rentabilidad 0), en silencio. La resolución viene de antes de T-65, pero contradice la Constitución (§11) y alimenta la calibración con sucesos falsos.

Para la r04: corregir H-16 con su prueba de regresión (o, si el coordinador decide sacar la parte de `resolver` de T-65, pasarla a la deuda con su ID y corregir la de la emisión aquí), y los bajos H-17 a H-23 o su paso a la deuda con su ID. El revisor volverá a ejecutar r01_01 a r03_04.

---

# Ronda r04

- **Revisor:** revisor nuevo sin contexto de la implementación (Claude, subagente de QA) · **Ronda:** r04 (la última, por indicación del operador) · 2026-11-10 · sobre las correcciones de la r03, sin commit al empezar. Durante la revisión el coordinador las subió en db6ed93. `git diff db6ed93` solo muestra la sonda r04_01 de esta ronda (el commit se llevó una primera versión): el código de producto revisado es el de db6ed93.

## Reproducción desde limpio

- Tres copias con `git worktree add --detach` de b7c3afa, cada una con los cambios de T-65 (`git diff` más la prueba nueva) y un enlace a `.venv`. Se comprobó que importan el paquete de la copia. Se quitaron al terminar con `git worktree remove`.
- Gate completo (`.docs/scripts/gate.sh --completo`) en la primera copia: **12/12**. corpus-integridad, nombres-nfc, yaml-configs, secrets, refs-vivas, ruff, los tres mypy y las tres suites (A **317**, A-Forex 68, B 174).
- `pytest -q bloque_a/11_Ejecutor` en el árbol de trabajo: 317 passed.
- `.docs/tickets/T-65/mutaciones.py` en la segunda copia: **67 de 67** detectadas, y la copia queda como estaba. `r01_07_mutaciones_extra.sh`: las 5 detectadas. `r03_04_mutaciones_extra.sh`: 2 de 2 detectadas. La tercera ya no casa con el código, y la cubre la mutación «r03 H-19 sin las referencias de las vigentes».
- `.docs/scripts/prueba_refs_vivas.py`: 25/25.
- Sondas de las rondas anteriores, en el árbol de trabajo:
  - Sin hallazgos: r01_02, r01_04, r01_06, r02_02, r02_03, r03_01, r03_02 (A a D; las 5 INFO de A son las que ya se daban por correctas) y r03_03.
  - Con «hallazgos» que el cambio de H-21 explica: r01_01 (2, «C/dup») y r02_01 (1, «B/desordenado_y_duplicado»). Se valoran abajo.
  - r01_05 no se repitió: la variación de `consumo.uc` (T-88) ya aparece en r01_03.
- **Determinismo** (r01_03, backtest de 4 semanas con 12 tipos y 4 hilos): dos veces con el árbol de T-65 y una con b7c3afa, cuyo código de A es el de 8d74622, la r03.
  - Entre las dos ejecuciones de T-65 cambian 6 archivos: las rutas absolutas de los informes técnicos y de F5, y el orden de `cache_resultados.jsonl`.
  - Frente a la r03 cambian además `consumo.csv` y `metricas.json`, en el cuarto decimal de `uc` (H-10/T-88).
  - F3, F4, señales y pronósticos son idénticos: con datos sanos, las correcciones no cambian nada.
- **Corpus y prompts:** sin cambios (corpus-integridad en verde; ningún prompt tocado).
- **Sondas nuevas** (sin commit, salvo una primera versión de r04_01 que va en db6ed93): r04_01_frescura_borde.py (partes R, C, E y F), r04_02_filas_en_rango.py, r04_03_backtest_referencia_parada.py y r04_04_refs_vivas.py.

## Hallazgos de la r03

| ID | ¿Corregido? | Evidencia del revisor |
| --- | --- | --- |
| H-16 (media) | **en parte** | **Al emitir: sí.** r04_01 E: con ACWI a 7 días de la fecha as_of, RV se analiza; a 8 días, queda fuera y declarado (PARCIAL, 0 PRG frente a ACWI). r03_02 A («deja de publicarse en 2025-06»): RV e IDX fuera, con limitación e incidencia. Con SUBYACENTE, por indicador (r03_02 B).<br>**Al resolver: sí para H2 y horizontes más largos.** r03_02 D (las cuatro variantes, también el proxy parado): ABIERTO. r04_01 R: en H2, una serie parada en la emisión o 8 días antes de la resolución espera. r04_03 (backtest semanal con ACWI parada el 2026-03-27 y la resolución final): ninguna emisión con ACWI de más de 7 días, ningún PRG resuelto sin dato de ACWI posterior a su emisión y 27 NO_RESOLUBLE.<br>**Pero en H1 sigue resolviendo con 0:** el proxy, la referencia o un miembro de la CESTA parados justo en la emisión (H-24, abajo) |
| H-17 | sí | r03_02 B, «SPY sin archivo»: los tres indicadores de DER se excluyen y se declaran, PARCIAL; nunca la CESTA en silencio. Prueba `test_r03_h17_*` y su mutación |
| H-18 | sí | r03_02 C2: con la vigente que guarda ACWI, solo TAIL queda fuera y DER sigue con 2 opciones (antes, DER entero fuera) |
| H-19 | sí | Las dos mutaciones «r03 H-19» de `mutaciones.py` las detecta su prueba, y la segunda también r03_04 |
| H-20 | sí | r03_01 (`cierre,cierre`, `Close,Close`, `fecha,fecha`): se rechazan con «columnas repetidas»; mutación detectada |
| H-21 | **sí, con un resto** | r04_02: 13 de 15 casos bien. Dentro del rango se rechaza todo: `n.d.`, `inf`, un booleano suelto, una fecha repetida (también con el mismo valor), el primer día de la ventana y la fecha as_of con `valor_en`. Fuera del rango no importa: el día antes de la ventana, el día después de as_of y una fila aún no publicada. **Resto:** una fecha repetida cuya segunda copia aún no está publicada (H-25, abajo) |
| H-22 | sí | r03_03: 0 hallazgos. r04_04: 38 casos, 0 hallazgos y 5 INFO (abajo). Repo real: 0 citas rotas |
| H-23 | sí | `docs/incidencias.md` (INC-T65-01, `[PROPUESTO]` con su pregunta), sección 4 del README del ejecutor, lista para T-57 del README del ticket y fila T-57 de la deuda |

Los hallazgos de la r01 y la r02 siguen corregidos: H-01 (r01_04), H-02 y H-13 (r03_01), H-03 (gate 12/12 desde limpio), H-04 (r01_06), H-05 a H-08 (mutaciones y r01_07), H-09 y H-11 (lectura y prueba), H-12 (r02_03 y r03_02), H-14 (r03_01) y H-06 y H-15 (r02_02 y r03_03). H-10 sigue en la deuda (T-88).

## Valoración del cambio de H-21 y de las dos sondas antiguas

- **El comportamiento nuevo es correcto.** Es la misma regla que H-01 (aceptada en la r02, con un cierre 0 de 2019): se valida lo que se usa.
  - r01_01 «dup»: la fecha repetida es 2026-10-30, posterior a la fecha as_of. Rechazar el símbolo por ella usaría en el backtest un dato que aún no existía, que es la fuga que H-21 quería quitar. En la resolución final del backtest, `valor_en` sí la ve si cae en la fecha que lee (r04_02, «fecha repetida en la fecha as_of»).
  - r02_01 «desordenado_y_duplicado»: la fecha repetida es 2023-01-05, anterior a la ventana más larga del lote (3 años más 30 días: desde el 2023-05-06). Las lecturas de tasa base, clústeres, GC0, Motor y nivel caen todas dentro de esa ventana.
  - Lo que esperaban las dos sondas, escritas cuando HT-01 rechazaba el archivo entero, queda obsoleto.
- **Ningún dato malo dentro de la ventana pasa** (r04_02, 8 casos). `serie()` lo devuelve marcado (`_invalido`, `_crudo`, `_duplicada`), pero hoy nadie la lee fuera de HT-01 (`grep`). Todas las lecturas pasan por `cierres` o `valor_en`.
- **Emitir y resolver:** la resolución solo lee dos niveles (`valor_en` en la emisión y en la resolución). Un `n.d.` entre las dos fechas no impide resolver, pero excluye el símbolo en la emisión siguiente. Es coherente con «se valida lo que se usa», y falla cerrado en los dos lados.

## Hallazgos nuevos

| ID | Gravedad | Cómo reproducirlo | Esperado / obtenido | Corrección sugerida | Estado |
| --- | --- | --- | --- | --- | --- |
| H-24 | media | r04_01_frescura_borde.py, partes R, C y F. F es de punta a punta: ciclo del viernes 2026-04-17 con `horizontes=["H1"]` (H1 es «SI» para MP y DIV en la tabla de horizontes), DBC o el proxy dejan de publicarse ese mismo día, y ciclo siguiente el 2026-04-27 | **Esperado** (H-16 y README del ticket: «nunca se resuelve con una rentabilidad 0»; Constitución §11).<br>**Obtenido:** H1 son 5 sesiones, 7 días naturales del viernes al viernes, y `evaluacion.antiguedad_maxima_dato_resolucion_dias` también es 7. `(f1 − d_min).days > 7` no salta cuando el último dato de una serie es el de la propia emisión.<br>– Parte F: **2 de 2 PRG H1 RELATIVO de MP RESUELTOS** con `rent_referencia` 0,0 (DBC parada) o `rent_proxy` 0,0 (proxy parado).<br>– Parte R: igual con ACWI o SPY escritos en F4 como en `test_r03_h16_*`.<br>– Parte C: en la CESTA, el miembro parado en la emisión entra con 0, porque el filtro de H-16 usa la misma tolerancia.<br>Es el mismo suceso falso de H-16 (Brier, calibración y certificados R13), ahora en H1. El cliente simulado no elige H1 por sí solo, pero el prompt pide H1 a H4 y el modelo real puede emitirlo. Además, en H1:<br>– una serie parada 1 sesión después de la emisión se resuelve con 1 de las 5 sesiones (INFO en R);<br>– en la emisión, la referencia puede tener 7 días, mientras PS2 pide al proxy 1 sesión;<br>– `fecha_dato` guarda la más reciente de las dos fechas y oculta la antigüedad de la otra | Exigir a cada serie (proxy, referencia y miembro de la CESTA) un dato posterior al de la emisión (`d1 > d0`), y atar la tolerancia al horizonte en vez de un 7 común. Por ejemplo, con `ps2_antiguedad_maxima_dias`, que ya existe por horizonte y cuenta sesiones en H1. Guardar la fecha de cada serie en la resolución. Prueba: las partes R, C y F de r04_01 | abierto |
| H-25 | baja | r04_02_filas_en_rango.py, casos «revisión de 2026-05-29 publicada el 2026-07-01»: una fila con la misma `fecha` y una `fecha_publicacion` posterior a la fecha as_of (una revisión de una serie macro) | **Esperado** (H-21: «un dato malo posterior a as_of … no excluye el símbolo»; README del ejecutor: «una fila mala solo cuenta si cae en el rango que se usa»): a la fecha as_of solo se ve la primera copia, así que el símbolo se lee.<br>**Obtenido:** `_duplicada` se calcula al cargar sobre el archivo entero, también sobre las filas que `serie()` aún oculta por su `fecha_publicacion`. Con la fecha as_of 2026-06-05 (y con `valor_en` del 2026-05-29), el símbolo se rechaza («fechas duplicadas … 2026-05-29»): una fila que aún no se conocía cambia la decisión. Falla cerrado (excluye y declara, nunca da cifras), y antes de la r03 cualquier fecha repetida ya rechazaba el archivo | Marcar las fechas repetidas en `serie()`, después del filtro de publicación (solo entre las filas visibles). O rechazar al cargar los archivos con revisiones como formato no admitido, declarado, y decirlo en el README del ejecutor | abierto |

Información (no son hallazgos):
- r04_04, formas de `refs-vivas` que el docstring no promete:
  - rompen en falso una ruta suelta con espacios cuyo primer trozo acaba en `.py`, una ruta con `..` que no sale del repo (deliberado) y una salida tras una tubería (`| tee`);
  - no se comprueban una variable de entorno delante de la orden ni un `cd … &&`.
  - Ninguna aparece hoy en el repo.
- `ultima_fecha()` cuenta también una última fila inválida. Solo fija la fecha de la resolución final del backtest, y las lecturas siguientes la rechazan.
- r04_03: al final del backtest siguen ABIERTO 48 PRG frente a ACWI. No se ha comprobado uno a uno por qué. Con ACWI parada, ninguno puede resolverse, y ninguno está RESUELTO con un dato falso.

## Veredicto

**NO APTO.** Está bien corregido:
- la emisión con una referencia obsoleta (H-16, en el borde exacto de los 7 días);
- la resolución en H2 y horizontes más largos, también en un backtest;
- H-17 a H-23, con H-21 bien valorado (las dos sondas antiguas cambian por la razón correcta);
- además: 67 de 67 mutaciones detectadas, gate 12/12 desde una copia limpia, determinismo, corpus y prompts sin cambios, y los hallazgos de la r01 y la r02 siguen cerrados.

Pero hay un hallazgo medio confirmado en el mismo punto de H-16:
- H-24: en H1 (7 días naturales, la misma cifra que la tolerancia), un pronóstico RELATIVO se sigue resolviendo con una rentabilidad 0 cuando el proxy, la referencia o un miembro de la CESTA dejan de publicarse el día de la emisión. Se reproduce de punta a punta con el ciclo.

H-25 es bajo.

Por indicación del operador no se abre otra ronda: la tarea se detiene aquí. El coordinador debe pasar H-24 y H-25 a la deuda técnica, con su ID y la corrección sugerida.
