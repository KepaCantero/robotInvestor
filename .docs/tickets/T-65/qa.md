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
