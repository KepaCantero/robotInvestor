# T-165 · QA independiente

- **Revisor:** subagente de Claude sin contexto de la implementación (regla `compartida/2026-11-12_claude-puede-hacer-qa`) · **Ronda:** r01 · 16-11-2026
- **Copia revisada:** worktree desechable en `3b998bf` (`develop`, T-161 r02 + T-163 + T-165), con `.venv` enlazado. Sin red ni gasto
  (cliente simulado). Opinión formada con el plan (`README.md`) y el código antes de leer `analisis-tecnico.md`.
- **Copias auxiliares (fuera del árbol, en el scratchpad del revisor):** `qa40_pre165`, exportación de HEAD con `ht09.py`,
  `sintesis.py` y `redaccion.py` de HEAD~1 y sin la expresión de T-165 en `orquestacion.py` (T-161 y T-163 se quedan), para comparar
  entregables; `qa40_mut`, exportación de HEAD con `bloque_a` y `.docs/tickets/T-159`, para los mutantes.

## Reproducción desde limpio

Desde la raíz de la copia, en este orden (los scripts del revisor están en `revisores/`):

```bash
cd bloque_a/11_Ejecutor
../../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_t165_g3_met13.py
../../.venv/bin/python -m pytest -q -p no:cacheprovider -s ../../.docs/tickets/T-159/revisores/r01_02_sondas.py -k pb47
../../.venv/bin/python tests/goldens_ct.py
# 1. ataques a la lectura del texto (unitarios; las que fallan son hallazgos)
../../.venv/bin/python -m pytest -q -p no:cacheprovider ../../.docs/tickets/T-165/revisores/r01_01_ataques_texto.py -rf
# 2. de extremo a extremo con el cliente simulado (las que fallan son hallazgos)
../../.venv/bin/python -m pytest -q -p no:cacheprovider -s ../../.docs/tickets/T-165/revisores/r01_02_extremo_a_extremo.py -rf
# 3. ciclos normales (falsos positivos) y comparación con la versión anterior a T-165
../../.venv/bin/python ../../.docs/tickets/T-165/revisores/r01_03_ciclos_normales.py --salida <scratch>/ciclos_post
(cd <copia_pre165>/bloque_a/11_Ejecutor && <raíz>/.venv/bin/python <raíz>/.docs/tickets/T-165/revisores/r01_03_ciclos_normales.py --salida <scratch>/ciclos_pre)
diff -rq <scratch>/ciclos_pre <scratch>/ciclos_post      # solo el técnico (ruta de trabajo de sus hermanos) y resumen.json
../../.venv/bin/python -m pytest -q -p no:cacheprovider    # suite completa, una vez, en segundo plano
cd ../..
# 4. mutantes en una copia desechable
.venv/bin/python .docs/tickets/T-165/revisores/r01_04_mutantes.py --copia <copia_mut>
.venv/bin/python .docs/scripts/evidencias_plan_a.py --ejecutar
for g in refs_vivas secrets_scan nfc_check corpus_integridad; do .venv/bin/python tools/$g.py; done
.venv/bin/ruff check --output-format=concise bloque_a/11_Ejecutor bloque_a_forex/11_Ejecutor bloque_b/11_Ejecutor | wc -l
.venv/bin/mypy --ignore-missing-imports --no-error-summary bloque_a/11_Ejecutor/bloque_a | wc -l
```

| Comprobación | Resultado |
| --- | --- |
| `tests/test_t165_g3_met13.py` | 47 superadas (dentro de la suite) |
| Sonda de la QA de T-159 (`-k pb47`) | pasa: «dictámenes G3: ['BLOQUEADO', 'APTO_CON_ADVERTENCIAS', 'APTO_CON_ADVERTENCIAS'] · entregables con «validado»: []» |
| Goldens (`tests/goldens_ct.py`; `test_fase3_goldens.py` en la suite) | coinciden |
| Suite completa de A (una vez, máquina con carga 10–14 por otras sesiones) | **0 fallos.** La primera ejecución la cortó el `timeout` del revisor (50 min) al 86 %: 6249 superadas y 2 omitidas hasta ahí. Los 27 ficheros que faltaban (de `test_t159_extremo_a_extremo.py` a `test_v51.py`) se lanzaron otra vez: 934 superadas en 25 min. En total, 7182 recogidas, sin fallos. `test_t102_filtro::test_r05_h37_…` pasó |
| Evidencias regeneradas (`--ejecutar`) | «204 de 204 pruebas citadas superadas»; 31 Superada · 27 en parte; PB-47 «Superada». El fichero es **idéntico** al de HEAD salvo el commit de la cabecera (`0db2db6` → `3b998bf`); restaurado después con `git checkout` |
| Ciclos normales sin siembra (r01_03): 10 ciclos (V5 doce tipos en 2024-03-01, 2025-01-10/17/24 y 2026-06-05/12; V6 doce tipos en 2026-06-05 y 2025-01-10; configuración por defecto, solo DIV, 2024-02-02 y 09) | 20 G3V-, G3-MET-13 OK en todos; los dictámenes son los mismos que sin T-165 (algunos APTO_CON_ADVERTENCIAS por otras comprobaciones, igual antes y después) |
| Entregables frente a la versión anterior a T-165 (los mismos 10 ciclos) | **idénticos** técnico, visual y JSON, salvo la ruta temporal de los hermanos en el técnico; `resumen.json` solo difiere en G3-MET-13 (no existía → OK). Los entregables citan ST-DESC-001, RISK-DD-001 y ML-CLUS-001 y ninguna palabra de madurez («verificado» es la única parecida) |
| Gates ligeros | `refs_vivas`, `secrets_scan`, `nfc_check` en verde; `corpus_integridad`: 695 archivos coinciden |
| Cuotas | ruff **2813** (≤ 2813 de `tools/cuotas.txt`; T-165 quita 3 avisos de `ht09.py` y no añade ninguno en los ficheros que toca: comparado aviso a aviso con la copia anterior) · mypy A **109** (≤ 109) |

## Criterios de aceptación

| Criterio | Cumple | Evidencia |
| --- | --- | --- |
| CA-1 (la sonda de T-159 bloquea en F6 y ningún entregable dice «validado») | sí | Sonda `-k pb47` y `r01_02::test_control_siembra_t159_bloquea`: primer G3V- de F6 BLOQUEADO con G3-MET-13, entregables sin «validado». **Pero solo con esa redacción**: H-01 a H-04 |
| CA-2 (ML-CLUS-001 en DOCUMENTADO sin siembra se entrega) | sí, en V5 con la integración disponible | `test_pb47_corregida_…` y la de T-159 pasan. En V6, o en V5 sin integración, no: H-06 |
| CA-3 (ciclo normal APTO en F6 y F7 con G3-MET-13 OK) | sí | La prueba del ticket y r01_03 (10 ciclos, 20 G3V-) |
| CA-4 (los casos listados bloquean o no) | sí, tal como está escrito | Las 34 frases de la prueba del ticket; mis controles (`r01_01::test_control_*`) también pasan. Fuera de esa lista, H-01 a H-05 y H-07 |
| CA-5 (formato de HT-09 y dictamen recalculado) | sí | `_recalcular` usa la misma regla que la referencia (`ht09_validador_g3.py`, dictamen y motivo); pruebas del ticket; mutante M24 muere |
| CA-6 (técnico comprobado en F7, bloqueo a `_bloqueados`) | sí | `test_un_metodo_no_servido_solo_en_el_tecnico_…`; mutantes M25 y M31 mueren |
| CA-7 (PB-47 AUTOMATICA y «Superada») | sí | `tests/mapa_plan_pruebas.json` (AUTOMATICA, cita las pruebas del ticket) y las evidencias regeneradas. Lo que «Superada» afirma («un informe de clase que lo llama validado… bloquea») solo vale con la redacción de la sonda: H-01 a H-04 |
| CA-8 (suite, goldens, gates, cuotas) | sí | Suite sin fallos (7182 recogidas, ≥ 607), goldens, gates ligeros, ruff 2813 (≤ 2821 del ticket y ≤ 2813 de `tools/cuotas.txt`), mypy A 109 |

## Hallazgos

Todos con el Catálogo real salvo que se diga otra cosa: las 81 fichas están IMPLEMENTADO y ninguna VALIDADO, así que «validado» de
cualquier ficha es una madurez falsa (R22). «Llega a la entrega» quiere decir: el técnico y el JSON entregados (no `_bloqueados`)
contienen la frase y el JSON lleva `estado_g3` APTO.

| ID | Gravedad | Cómo reproducirlo | Esperado / obtenido | Corrección sugerida | Estado |
| --- | --- | --- | --- | --- | --- |
| H-01 | alta | `r01_02::test_escapa_catalogo_real[por_los_datos]` (la valoración del Analista simulado acaba en «(ST-DESC-001), un método validado por los datos de los últimos diez años.»); unitarios `r01_01` E05–E08 y P02 | Esperado: G3 bloquea (R22). Obtenido: G3 APTO en F6 y F7, el técnico y el JSON entregados dicen «validado por los datos» y el JSON lleva `estado_g3` APTO. La excepción `RE_AGENTE` («validado por» + lista cerrada, decisión `[PROPUESTO]` de INC-T165-01) incluye `datos`, `fuentes`, `mercado` y `evidencias`, que son justo lo que valida un método: «validado por los datos», «por el mercado», «por la evidencia empírica» es la afirmación R22. Con PB-47, «ML-CLUS-001 rechazado por el Motor, pero validado por los datos» tampoco bloquea | Limitar la excepción a personas (operador, usuario, Broker, asesor, cliente, inversor). Si se quiere salvar «tesis validada por el dato de empleo» con una ficha en la frase, que sea con un patrón más estrecho («dato de …» seguido de un indicador), nunca con «datos», «evidencia», «mercado» o «fuentes» sueltos. Añadir los cuatro casos como pruebas que bloquean | abierto |
| H-02 | alta | `r01_02::test_escapa_catalogo_real[frase_siguiente]` (valoración «… (ST-DESC-001). Es un método validado en backtest.»); `r01_02::test_escapa_pb47_declarado_y_luego_validado`; unitarios E14–E17, H01, H02, H06, P01, P03 | Esperado: bloquea. Obtenido: G3 APTO y entregado con «método validado en backtest». La palabra de madurez solo se atribuye a una ficha de su misma frase, y la frase se corta en «. », «;», saltos de línea, celdas `|` y etiquetas de bloque: la redacción más normal («usa X. Es un método validado», «X; es un método validado», una tabla «Método · Estado») se escapa. Con PB-47 vale igual: «ML-CLUS-001 (documentado); en la práctica está validado por los datos» se entrega con G3 APTO | Como ninguna ficha está VALIDADO, tratar una palabra de madurez afirmativa sin ficha en su frase como dicha de las fichas del mismo texto (misma ruta: el campo del JSON, la línea o el bloque del técnico y del visual), o al menos de la frase anterior, y en una tabla, de la fila. Medir los falsos positivos que añade con r01_03 y con las frases de `r01_01::FP` | abierto |
| H-03 | alta | `r01_02::test_escapa_catalogo_real[preterito]` (valoración «… ST-DESC-001 se validó en backtest con diez años de datos.»); unitarios E01–E04 | Esperado: bloquea. Obtenido: G3 APTO y entregado con «se validó». `RE_MADUREZ` solo reconoce los participios (validado/a/os/as, implementado…, documentado…) y sus tres equivalentes en inglés: «se validó», «validaron», «ha superado la validación», «revalidado» o sinónimos («verificado», «probado», «contrastado», «certificado») no cuentan | Ampliar a las formas verbales afirmativas («validó», «validaron», «se valida», «superó/ha superado la validación») y decidir, `[PROPUESTO]`, qué sinónimos cuentan como «validado» en R22; declarar los que no | abierto |
| H-04 | alta | `r01_02::test_escapa_catalogo_real[guion_no_separable]` («ST‑DESC‑001 está validado en backtest.» con U+2011); unitarios E09–E13 y P05 (la frase de la sonda de T-159 con U+2011) | Esperado: bloquea. Obtenido: G3 APTO y entregado. `RE_FICHA` solo acepta el guion ASCII y mayúsculas: con guiones tipográficos (U+2010–U+2015, que los modelos y los procesadores de texto escriben a menudo), en minúsculas, con espacios o parcial («VOL-GARCH») la ficha no se reconoce, y entonces tampoco funciona la regla B, que es la que falla cerrado: «… con ML‑CLUS‑001, un método validado» con ML-CLUS-001 en DOCUMENTADO pasa | Normalizar antes de buscar fichas (NFKC, guiones U+2010–U+2015, U+2212, U+FE63 y U+FF0D a «-», y reconocer la ficha sin distinguir mayúsculas). Declarar lo parcial («VOL-GARCH», «GARCH-001») como límite o tratar como mención un prefijo y familia del Catálogo | abierto |
| H-05 | media | `r01_02::test_escapa_estado_madurez_de_una_opcion_entregada` (tres formas de `estado_madurez_metodos` en el informe de una opción que llega a la entrega); unitarios J01–J09 | Esperado: como en el control (`«ST-DESC-001: validado»` en texto, que sí retira las opciones), F6 retira la opción cuyo informe de clase afirma la madurez falsa. Obtenido: se entregan las 3 opciones con G3 APTO cuando el campo es un objeto con la ficha en la clave (`{"ST-DESC-001": "validado"}`), una lista con `ficha_id` + `estado_madurez`, o la afirmación va en la línea siguiente. `textos_de` no lee las claves, ni valores que no son texto (booleanos, números), y los hermanos de un campo `…madurez…` son solo `metodo`, `method_id`, `ficha`, `operacion` y `metodos` (no `ficha_id` ni `id`, que es como el propio ejecutor nombra la ficha en RC). El esquema `FINALISTA` no restringe `estado_madurez_metodos`. La frase falsa no llega a los ficheros entregados (ese campo no pasa al paquete): por eso media | Leer también las claves de los diccionarios como texto (una clave con forma de ficha se lee junto con su valor), añadir `ficha_id` e `id` a los hermanos y tratar un valor no textual de un campo `…madurez…`/`validad…` como su nombre; o exigir en el contrato que `estado_madurez_metodos` sea texto | abierto |
| H-06 | media | `r01_02::test_fp_v6_con_ml_clus_documentado_sin_siembra` y `test_fp_v5_sin_integracion_con_ml_clus_documentado` | Esperado (CA-2 y el riesgo «texto del propio ejecutor» del plan): con ML-CLUS-001 en DOCUMENTADO y sin siembra, el ciclo se entrega. Obtenido: F6 BLOQUEADO sin OPP- (todo el run), «se nombra ML-CLUS-001 y el Motor no la sirve … «Factor común de las opciones del clúster CL-3 (correlación semanal ≥ 0,7, ML-CLUS-001)»». Es un tercer texto del ejecutor que cita ML-CLUS-001 aunque el Motor lo haya rechazado (`sintesis.construir`, rótulo por defecto de `factor_dominante`), además de los dos que T-165 corrigió. Sale siempre en V6 (la integración es determinista y `factores_dominantes` va vacío) y en V5 cuando la integración no está disponible. Sin bloqueo sería además falso: con el rechazo cada serie es su propio clúster | Mismo arreglo que `_rotulo_n_efectivo`: citar ML-CLUS-001 solo si `clusteres["calc_id"]`; si no, «cada serie cuenta aparte». Buscar en el código los demás literales con una ficha que llegan a un entregable (`RISK-DD-001` en `redaccion.py`; `FC-EVAL-001` en `evaluador.py`, hoy solo en F6) y hacerlos condicionales en lugar de dejar el bloqueo como límite | abierto |
| H-07 | media | `r01_01::test_fp` (17 frases) y `r01_02::test_fp_prosa_financiera_retira_opciones`, `test_fp_lectura_del_conjunto_bloquea_el_run` | Esperado: frases legítimas no bloquean. Obtenido: bloquean (1) variantes normales de «validación pendiente» que la negación no cubre: «pendiente de ser validado», «sin estar validado», «a la espera de ser validado», «sin haber sido validado», «no puede considerarse validado», «no ha sido todavía formalmente validado» (cuatro auxiliares), «no-validado», «non-validated», «pendientes de ser validados»; (2) prosa financiera con «validado» en otro sentido en la misma frase que una ficha: «La ruptura quedó validada por el volumen, con la volatilidad VOL-GARCH-001…», «Ruptura alcista validada (percentil 96 %, ST-DESC-001)», «validado por el consenso», «por el comité de riesgos», «validada con el dato de inflación». De extremo a extremo: con «Ruptura alcista validada por el volumen» en la valoración, F6 retira las 3 opciones de RV; con una frase así en la lectura del conjunto del Analizador (fuera de una opción), F6 bloquea el run entero (6 opciones) | Ampliar la negación a las construcciones de infinitivo («sin estar/haber sido», «pendiente/a la espera de ser», «no puede considerarse», «no-»/«non-») con una ventana fija; y, para la prosa, exigir que la palabra no lleve un complemento que la ate a otra cosa («ruptura/señal/soporte/tesis/hipótesis … validada») o aceptar el falso positivo pero medirlo y declararlo. Cualquier cambio, contra el mismo banco de r01_01 en las dos direcciones | abierto |
| H-08 | baja | `r01_01::test_fp_pb47_declarado_en_otra_celda` y `test_fp_pb47_html_tabla` | Con ML-CLUS-001 en DOCUMENTADO, una declaración correcta en una tabla («| ML-CLUS-001 | documentado |», también en HTML) o en dos líneas («Método: ML-CLUS-001\nMadurez: documentado (no se sirve)») bloquea: la regla B mira la frase y la celda la corta | La misma unidad que se elija en H-02 (fila de tabla, campo) para la declaración | abierto |
| H-09 | baja | `r01_01::test_fp_retira_una_opcion_que_solo_se_cita` | F6 toma los OPP- de la ruta **y del detalle**; el detalle de un BLOQUEO lleva el extracto de la frase, así que si la opción A dice «Complementa a OPP-2026-0002, y VOL-GARCH-001 está validado», F6 retira A y también B | Poner el extracto sin OPP- (como ya se hace con la ruta de lo no entregado) o que F6 lea solo la ruta para G3-MET-13 | abierto |
| H-10 | baja | `r01_01::test_tiempo_lineal_en_una_frase_larga` | El coste crece con el cuadrado de la frase: `RE_NEGACION.search(frase[:m.start()])` y `frase[m.end():]` recorren y copian todo el prefijo y el sufijo por cada palabra. 36 KB sin punto: 6 s; 144 KB: 88 s (máquina cargada). `TXT` no tiene `maxLength` en los contratos | Buscar la negación y el «por …» en una ventana fija (p. ej. 60 caracteres) delante y detrás de la palabra | abierto |
| H-11 | baja | `r01_01` E18–E21, H03–H05 | Trucos tipográficos que un modelo no suele escribir pero que pasan: «а» cirílica, guion blando (también `&shy;` en el visual), carácter de ancho cero, la palabra partida por una etiqueta en línea (`vali</b>dado`), un atributo `title`, y la doble negación («Nadie diría que X no está validado») | Quitar los caracteres de formato (categoría Cf) tras NFKC; declarar el resto como límite en INC-T165-01 | abierto |
| H-12 | baja | Lectura de `analisis-tecnico.md` e INC-T165-01; `r01_04_mutantes.py` | (a) Límites sin declarar: un método nombrado sin su ficha («el modelo GARCH está validado») no se detecta, por diseño, y no está entre los límites; los sinónimos de H-03 tampoco. (b) Nueve mutantes viven (tabla de mutantes): la negación con «sin» (M01, que además casi no actúa: «sin ser/estar/haber sido validado» no la activan porque «ser», «estar» y «haber» no son auxiliares de la lista, ver H-07), el plural (M03: el único caso lo enmascara la regla B), el corte por «|» (M09), los hermanos `method_id`, `ficha`, `operacion` y `metodos` (M12), la deduplicación por ficha (M13), el desempate (M14), el extracto solo en los bloqueos (M15), AUD-REX-001 por CT-10 en `sintesis._sirve` (M20) y la limitación de «sin historia» con el rechazo (M32) | Declararlos en INC-T165-01 y en `analisis-tecnico.md`; una prueba por cada mutante vivo (que no la enmascare la regla B) | abierto |

### Bajos que hay que subsanar en este ticket (regla del operador, 16-11-2026)

Desde hoy, los bajos se corrigen en el mismo ticket antes de cerrarlo; no pasan a la deuda:

1. **H-08**: una declaración correcta en otra celda o en otra línea bloquea (regla B por frase).
2. **H-09**: F6 retira también una opción que solo se cita en el extracto del detalle.
3. **H-10**: coste cuadrático en una frase larga (36 KB, 6 s; 144 KB, 88 s).
4. **H-11**: trucos tipográficos (cirílico, guion blando, ancho cero, palabra partida por una etiqueta, `title`, doble negación): normalizar o declarar.
5. **H-12**: límites sin declarar (método sin ficha, sinónimos) y nueve mutantes vivos sin prueba (M01, M03, M09, M12, M13, M14, M15, M20, M32).

## Decisiones `[PROPUESTO]` de INC-T165-01

| Decisión | Valoración del revisor |
| --- | --- |
| Id `G3-MET-13` y no C20 | De acuerdo: es el id del catálogo de G3 (§6.2 del prompt del Orquestador técnico), no choca con una versión futura de la referencia y ningún esquema ni consumidor exige `^C\d{2}$` (lo he buscado en `contratos.py` y en los usos de `comprobaciones`). Los goldens no lo recogen |
| Una ficha servida citada sin madurez no salta | De acuerdo: la madurez es la del Catálogo, que publica el Motor, y exigir el campo cambiaría el esquema del JSON (corpus). La regla B cubre la mitad comprobable |
| Declarar menos madurez no salta | De acuerdo: R22 persigue presentar como más maduro lo que no lo es; los prompts congelados todavía dicen «documentado» de fichas que el Catálogo ya da por IMPLEMENTADO, y saltar ahí bloquearía todo ciclo real |
| Regla de lectura del texto | **No basta tal como está** (H-01 a H-05, H-07, H-08): la excepción «validado por» con datos o evidencia deja pasar justo la afirmación R22; la unidad «frase» pierde la anáfora y las tablas; el vocabulario no tiene las formas verbales; la ficha solo se reconoce con guion ASCII. La lección `claude/2026-11-12_filtros-por-patron-en-texto-libre` se cumple otra vez: el banco de frases del ticket mide sobre todo lo que no debe saltar, y casi todo lo que debe saltar es la frase de la sonda |
| Advertencia para candidatas que no llegan a la entrega | De acuerdo: es un hallazgo R22 pero no se presenta al Broker. Efecto lateral aceptable: el ciclo queda APTO_CON_ADVERTENCIAS y hay una llamada CT-14 más al Orquestador |
| «Dentro de una opción → F6 la retira; fuera → bloquea el run» | De acuerdo con el criterio (G3-MET-13 no está entre los fallos sistémicos de §6.3). Dos matices: F6 retira también las opciones que solo se citan en el extracto (H-09), y un falso positivo fuera de una opción (la lectura del conjunto, H-07; el rótulo de H-06) tira el run entero, así que el coste de H-07 es alto donde no hay opción que retirar |
| Rótulo «(RISK-DD-001)» como límite | Aceptable como límite declarado (RISK-DD-001 no tiene dependencias opcionales y solo dejaría de servirse si se cambiara el Catálogo), pero H-06 muestra que la lista de textos del ejecutor que citan una ficha estaba incompleta: mejor hacer condicionales todos los literales que llegan a un entregable que dejar bloqueos permanentes como límite |

Además, el registro de decisiones (`Decisiones_del_operador_Bloque_A.md` §1) solo recoge dónde vive G3-MET-13; las reglas de lectura y
la advertencia de INC-T165-01 son decisiones de control que el operador quería tener recopiladas (`compartida/2026-11-13_decide-el-agente-por-defecto`).
El ticket deja esa fila a la sesión coordinadora; lo anoto para ella.

## Mutantes del revisor (r01_04)

32 mutantes en una copia desechable (`qa40_mut`), contra `tests/test_t165_g3_met13.py`, la sonda pb47 de T-159 y
`tests/test_t159_extremo_a_extremo.py`, con `-x`. **22 muertos, 9 vivos y 1 vivo casi equivalente (M26).** El primero que vive (M01) recorre
todas las pruebas, así que la copia sin mutar pasa.

| Mutante | Resultado | Lo que lo mata (o por qué vive) |
| --- | --- | --- |
| M01 negación sin «sin» | **vivo** | Ninguna prueba niega con «sin»; y «sin ser/estar/haber sido validado» no lo activa (H-07) |
| M02 negación sin auxiliares · M06 «no implementado» no declara | muertos | `test_no_salta_…[ML-CLUS-001 aún no ha sido implementado]` |
| M03 plural como singular | **vivo** | «DER-OPT-001 y ST-DESC-001: implementados» bloquea igual por la regla B (DER-OPT-001 no se sirve) |
| M04 sin la excepción «validado por» | muerto | `test_bloquea_…[ML-CLUS-001 documentado por el operador]` |
| M05 «documentado» no declara | muerto | `test_no_salta_…[DER-OPT-001 documentado; VOL-GARCH-001 implementado]` |
| M07 madurez por igualdad · M08 solo saltos de dos niveles | muertos | `test_no_salta_…[IDX-CONC-001 implementado]`; `test_bloquea_…[ST-DESC-001 está validado en backtest]` |
| M09 las celdas «|» no cortan | **vivo** | Ninguna prueba con una tabla |
| M10 etiquetas en línea cortan · M11 sin el OPP- en la ruta | muertos | `test_texto_html_…`; `test_textos_de_…` |
| M12 hermanos solo «metodo» | **vivo** | Solo se prueba `metodo` |
| M13 una incidencia por ruta · M14 desempate al revés | **vivos** | Ninguna prueba con dos fichas que fallan en la misma ruta ni con un empate de distancia |
| M15 extracto también en las advertencias | **vivo** | La prueba pone el OPP- en otra frase, así que el extracto no lo lleva |
| M16 a M19 (códigos del Motor, ficha inventada, inglés, advertencia = bloqueo) | muertos | sus casos de `test_bloquea_…`/`test_no_salta_…` y `test_formato_…` |
| M20 AUD-REX-001 sin CT-10 en `sintesis._sirve` | **vivo** | Las unitarias usan un `_sirve` propio; ningún ciclo nombra AUD-REX-001 |
| M21, M22, M27, M28, M29 (localización de los informes de clase y del paquete) | muertos | `test_g3_met13_localiza_…` |
| M23 visual sin leer · M24 dictamen sin advertencias | muertos | `test_g3_met13_visual_ilegible_…`; `test_recalcular_…` |
| M25 técnico nunca bloquea · M31 el técnico no entra en los bloqueos | muertos | `test_un_metodo_no_servido_solo_en_el_tecnico_…` |
| M26 lo no entregado con OPP- en la ruta | vivo, casi equivalente | F6 solo retira por los bloqueos, no por las advertencias; cambiaría lo que ve el Orquestador en CT-14 |
| M30 rótulo antiguo siempre | muerto | `test_pb47_corregida_…` |
| M32 limitación antigua de «sin historia» | **vivo** | Ningún ciclo de prueba tiene a la vez series sin historia y el rechazo de ML-CLUS-001 |

## Veredicto

**NO APTO.** Lo que el ticket promete en su caso de prueba se cumple (la sonda de T-159 bloquea, los ciclos normales siguen APTO
y sus entregables no cambian, goldens, gates, cuotas y evidencias en orden), pero G3-MET-13 deja llegar a la entrega una madurez
falsa con G3 APTO y el JSON en `estado_g3` APTO con cuatro redacciones normales, demostradas de extremo a extremo con el cliente
simulado: «un método validado por los datos» (H-01, por la propia excepción `[PROPUESTO]`), la afirmación en la frase siguiente
(H-02), el pretérito «se validó» (H-03) y la ficha con guiones no separables (H-04). Por la regla de esta QA, cada una es alta.
Además, un texto del propio ejecutor bloquea todo ciclo V6 con ML-CLUS-001 en DOCUMENTADO (H-06) y la prosa financiera normal
retira opciones o bloquea el run (H-07).

Vuelve a `ri-implementar`. Para la r02, el revisor volverá a ejecutar `r01_01` y `r01_02` (los casos `test_escapa_*` de las
redacciones que se decida cubrir tienen que pasar, y los `test_fp_*` que se acepten como falsos positivos tienen que quedar
declarados), `r01_03` (los ciclos normales tienen que seguir con G3-MET-13 OK y los mismos entregables) y `r01_04` con los mutantes
nuevos. Los bajos (H-08 a H-12) se subsanan en este mismo ticket, por la regla del operador de hoy. No he cerrado el ticket ni tocado la deuda técnica.
