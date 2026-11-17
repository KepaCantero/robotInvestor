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

---

# Ronda r02

- **Revisor:** subagente de Claude nuevo, sin contexto de la implementación ni de la QA r01 (que se cortó al empezar una vez; esta
  empieza desde cero) · 17-11-2026
- **Copia revisada:** worktree desechable `qa165r02b` en `27807e4` (`wip/t165r02`), con `.venv` enlazado. Sin red ni gasto
  (cliente simulado). Opinión formada con el plan y el código (`ht09.py`, `sintesis.py`, `redaccion.py`) antes de leer
  `analisis-tecnico.md` e INC-T165-01.
- **Copias auxiliares (en el scratchpad del revisor):** `base165` (exportación de `3d685ed`, el código de la r01) para comparar
  entregables; `mut165` y `mut165b` (exportaciones de `27807e4`) para los mutantes.
- **Alcance pedido:** sin la suite completa de A ni el gate; las pruebas de T-165 y T-159, los scripts de los dos revisores y del
  implementador, ciclos simulados, ruff y mypy de A.

## Reproducción

```bash
cd bloque_a/11_Ejecutor
../../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_t165_g3_met13.py tests/test_t159_extremo_a_extremo.py
../../.venv/bin/python -m pytest -q -p no:cacheprovider -s ../../.docs/tickets/T-159/revisores/r01_02_sondas.py -k pb47
../../.venv/bin/python -m pytest -q -p no:cacheprovider ../../.docs/tickets/T-165/revisores/r01_01_ataques_texto.py -rf
../../.venv/bin/python -m pytest -q -p no:cacheprovider -s ../../.docs/tickets/T-165/revisores/r01_02_extremo_a_extremo.py -rf
../../.venv/bin/python ../../.docs/tickets/T-165/r02_bancos_frases.py
# r02: ataques nuevos (unitarios y de extremo a extremo): las pruebas que fallan son hallazgos
../../.venv/bin/python -m pytest -q -p no:cacheprovider -s ../../.docs/tickets/T-165/revisores/r02_01_ataques_nuevos.py -rf
../../.venv/bin/python -m pytest -q -p no:cacheprovider -s ../../.docs/tickets/T-165/revisores/r02_02_extremo_a_extremo.py -rf
# ciclos normales: r01 (3d685ed) frente a r02, con la normalización de la ruta de trabajo de r01_03
../../.venv/bin/python ../../.docs/tickets/T-165/revisores/r01_03_ciclos_normales.py --salida <scratch>/ciclos_r02
(cd <base165>/bloque_a/11_Ejecutor && <raíz>/.venv/bin/python <raíz>/.docs/tickets/T-165/revisores/r01_03_ciclos_normales.py --salida <scratch>/ciclos_r01)
cd ../..
.venv/bin/python .docs/tickets/T-165/r02_mutantes.py --copia <mut165>
.venv/bin/python .docs/tickets/T-165/r02_mutantes.py --copia <mut165> --solo N14 N15 N16 N18 N19 N20 N21 N22
.venv/bin/python .docs/tickets/T-165/revisores/r02_03_mutantes.py --copia <mut165b>
.venv/bin/ruff check --output-format=concise bloque_a/11_Ejecutor bloque_a_forex/11_Ejecutor bloque_b/11_Ejecutor | wc -l
.venv/bin/mypy --ignore-missing-imports --no-error-summary bloque_a/11_Ejecutor/bloque_a | wc -l
```

| Comprobación | Resultado |
| --- | --- |
| `test_t165_g3_met13.py` + `test_t159_extremo_a_extremo.py` | 172 superadas (162 + 10) en 89 s |
| Sonda de T-159 (`-k pb47`) | pasa: «dictámenes G3: ['BLOQUEADO', 'APTO_CON_ADVERTENCIAS', 'APTO_CON_ADVERTENCIAS'] · entregables con «validado»: []» |
| `r01_01` (105 casos) | **105 superadas** (en la r01 fallaban 62): lo que afirma el implementador se cumple |
| `r01_02` (14 casos) | 13 superadas; `guion_no_separable` falla con `ValueError` al desempaquetar: es un error del script de la r01 (falta la marca). Repetido con la marca en `r02_02::test_escapa_catalogo_real[r01_guion_no_separable]`: **bloquea** (F6 BLOQUEADO, 0 opciones, ningún entregable con la frase). Confirmado |
| `r02_bancos_frases.py` | banco 1: 1 de 20 legítimas bloquean, 0 de 15 falsas pasan; banco 2: 1 de 15 y 0 de 10. Confirmado |
| Ciclos normales (r01_03, 10 ciclos, 20 G3V-) | G3-MET-13 OK en todos; dictámenes iguales. Técnico, visual, JSON y `resumen.json` **idénticos** a los de la r01 (`3d685ed`) tras normalizar la ruta de trabajo: los literales condicionales de H-06 no cambian ningún entregable normal |
| Cuotas | ruff **2813** (= `tools/cuotas.txt`), mypy A **109** (= cuota). Confirmado |
| Mutantes del implementador (`r02_mutantes.py`) | Se para en N13 (H-24); por partes y con N13 y N17 corregidos, los 31 mueren. Del revisor (`r02_03`), 2 de 9 viven (H-27) |

## Hallazgos de la r01

| ID | Estado en la r02 | Evidencia |
| --- | --- | --- |
| H-01 «validado por los datos» | corregido | `RE_PERSONA` solo excluye personas; r01_01 E05–E08 y r01_02 `por_los_datos` bloquean |
| H-02 frase siguiente | corregido en lo pedido (frase, unidad y párrafo anterior); quedan otras estructuras | r01_02 `frase_siguiente` y E14–E17 bloquean. Fuera: otro campo del mismo informe (H-17), título y dos párrafos, tabla transpuesta (H-23) |
| H-03 pretérito y formas | corregido en lo pedido; el sustantivo «validación» sigue estrecho | r01_02 `preterito`, E01–E04. Fuera: H-15, H-26 |
| H-04 guiones y grafía | corregido | E09–E13 y el caso de extremo a extremo (U+2011) bloquean. Fuera: separadores «_» y «.» (H-21) |
| H-05 forma del JSON | corregido en las tres formas de la r01; quedan otras | r01_02 `test_escapa_estado_madurez…` pasa. Fuera: H-20 |
| H-06 literales del ejecutor | corregido | `test_fp_v6…` y `test_fp_v5_sin_integracion…` pasan; ciclos normales idénticos. `_fuente_riesgo` no se alcanza hoy (PS4 exige el riesgo), está bien declarado |
| H-07 negación y prosa | corregido en el banco; la lista «ligada» abre un escape nuevo y la negación sigue estrecha | r01_01 FP pasa. Nuevos: H-13 (escape), H-18 y H-19 (falsos positivos) |
| H-08 declaración en otra celda o línea | corregido en tabla y línea; no tras un título | H-23 |
| H-09 OPP- en el extracto | corregido | r01_01 `test_fp_retira_una_opcion_que_solo_se_cita` |
| H-10 coste | corregido en la frase larga (62 KB: 0,03 s); cuadrático en fichas por párrafo | H-22 |
| H-11 trucos tipográficos | corregido (Cf, homoglifos, etiquetas en línea, `title`, doble negación) | r01_01 E18–E21, H03–H05 |
| H-12 límites y mutantes | límites declarados en INC-T165-01; los nueve mutantes vivos de la r01 mueren; el script de mutantes no corre entero | H-24 |

## Ataques nuevos (r02_01, r02_02)

Ninguna frase está en `r01_01`, en el test del ticket ni en `r02_bancos_frases.py`. Catálogo real (81 IMPLEMENTADO, ninguna
VALIDADO) salvo los casos PB-47 (ML-CLUS-001 en DOCUMENTADO).

- **Unitarios (`r02_01`, 71 casos):** de 36 madurez falsas, **36 pasan** (24 de 25 en texto, 9 de 9 en JSON, 2 de 2 en HTML y 5 de 5
  de la regla B de PB-47; solo bloquea «Como nunca antes, … validado»). De 16 frases legítimas, **16 bloquean** (14 con el Catálogo
  real, 2 con PB-47). Los 14 controles se comportan como dice el implementador. La prueba de coste falla (H-22).
- **Frases legítimas en general:** en una exploración más amplia de 49 frases legítimas nuevas (prosa de análisis, declaraciones
  de madurez honestas, verbos de comprobación), bloquean 14 (29 %), frente al 1 de 15 del banco 2.
- **De extremo a extremo (`r02_02`, 10 ciclos simulados de RV o RV+RF):** cinco madurez falsas **se entregan con G3 APTO en F6 y F7
  y `estado_g3` APTO en el JSON**, con la frase en el técnico y en el JSON: N1 (indicador de tendencia validado), N2 («validado: no
  hay dudas»), N3 («completó con éxito la validación»), J3 (la afirmación en el `mecanismo` y la ficha en la `valoracion`) y PB-47
  con «la alternativa fue rechazada» (ML-CLUS-001 en DOCUMENTADO, nombrado en uso). Tres frases legítimas **retiran las 3 opciones
  de RV** (S1 «Hemos comprobado con ST-DESC-001…», D2 «…ninguna ficha del Catálogo está validada») o **bloquean el run entero**
  (la misma S1 en la lectura del conjunto del Analizador: F6 BLOQUEADO, 6 opciones a `_bloqueados`). N4 (guion bajo) bloquea de
  extremo a extremo solo porque el mismo campo ya cita la ficha bien escrita.

## Hallazgos de la r02

| ID | Gravedad | Cómo reproducirlo | Esperado / obtenido | Corrección sugerida | Estado |
| --- | --- | --- | --- | --- | --- |
| H-13 | alta | `r02_02::test_escapa_catalogo_real[N1_indicador_de_tendencia]`; unitarios `r02_01` N1a–N1e | Esperado: bloquea. Obtenido: se entrega «ST-DESC-001 es un indicador de tendencia validado en backtest» con G3 APTO. `_ligada` descarta la palabra si el sustantivo «ligado» más cercano (tendencia, estrategia, previsión, cruces, señal…) está más cerca que la ficha o que un sustantivo de método; en «indicador de tendencia», «modelo de previsión», «algoritmo de cruces» el ligado es el complemento del método, no lo que se valida; y «estrategia» es como se nombra un método | En `_ligada`, no descartar si entre el sustantivo de método (`RE_METODO`) o la ficha y el ligado solo hay «de», «del», «de la», «de los», «de las» (el ligado es complemento del método): `RE_COMPLEMENTO = re.compile(rf"(?:{metodos}|<ficha>)\s+de(?:l|\s+la|\s+las|\s+los)?\s+(?:\w+\s+)?{ligado}")`; quitar «estrategia» y «estrategias» de `_LIGADOS`; y, si la palabra va en aposición a la ficha («X, … validado» sin otro verbo), atribuirla a la ficha. Los cinco casos N1 como pruebas que bloquean y el banco de prosa (r01_01 FP, bancos 1 y 2) en verde | abierto |
| H-14 | alta | `r02_02::…[N2_dos_puntos_no]`; `r02_01` N2a–N2c | Esperado: bloquea. Obtenido: «ST-DESC-001 está validado: no hay dudas.» se entrega con G3 APTO. `RE_NIEGA_DESPUES` (`^\s*[:=]\s*(?:no|false|…)(?!\w)`) toma por «validado: no» cualquier «: no …» detrás | Exigir que el valor negativo acabe ahí: `RE_NIEGA_DESPUES = re.compile(r"^\s*[:=]\s*(?:no|false|falso|pendiente|ninguno|ninguna)\s*(?:$|[.;,|)\]\n])")`. Pruebas: N2a–N2c bloquean; «validado = no.» y «validado: no» siguen sin bloquear | abierto |
| H-15 | alta | `r02_02::…[N3_con_exito_la_validacion]`; `r02_01` N3a–N3g | Esperado: bloquea. Obtenido: «ST-DESC-001 completó con éxito la validación fuera de muestra» se entrega con G3 APTO. El éxito de «validación» solo se busca en las tres palabras de delante (`[-3:]`) o detrás sin signo; no ven «superó con nota la fase de validación», «validación: superada», «validación: OK», «cuenta con validación … completa», «superó todas las pruebas de validación», ni el inglés «passed validation» | Buscar el marcador de éxito en toda la frase de la palabra (de `desde` al fin de frase, no `[-3:]`); detrás, permitir el signo: `^\s*[:=-]?\s*(?:\w+\s+){0,3}?(?:superada|…|ok|sí|si|completa|completada|con éxito)`; añadir `RE_VALIDACION` en inglés (`validation(?:s)?`) con «passed», «successful», «completed»; y «cuenta con / tiene (una) validación» como éxito. Declarar en INC-T165-01 lo que no se cubra. N3a–N3g como pruebas | abierto |
| H-16 | alta | `r02_02::test_escapa_pb47_otra_cosa_rechazada`; `r02_01` B1–B5 (con PB-47) | Esperado (regla B, falla cerrado): «Los clústeres salen de ML-CLUS-001; la alternativa fue rechazada» bloquea (ML-CLUS-001 no se sirve y se presenta en uso). Obtenido: se entrega con G3 APTO. Cualquier «rechazado/a», «no se sirve(n)» o código del Motor declara la ficha aunque esté negado («no fue rechazado», «el Motor no ha rechazado ML-CLUS-001») o se diga de otra cosa en otra frase de la misma unidad (sin ficha en su frase, la declaración va a todas las de la unidad) | En `_leer_unidad`, para `RE_NO_SIRVE`: (1) si `_negada(t, m.start(), desde, menciones=menciones)`, no declara; (2) la declaración solo vale para las fichas de su propia frase (`por_frase.get(frase(m.start()), [])`), nunca para toda la unidad; (3) los códigos `metodo_no_implementado`/`operacion_sin_ficha` igual, y solo sin negación detrás («no aparece»). B1–B5 como pruebas que bloquean; las declaraciones correctas del test del ticket en verde | abierto |
| H-17 | alta | `r02_02::…[J3_otro_campo]`; `r02_01` J3a | Esperado: bloquea. Obtenido: con la ficha en la `valoracion` («… (ST-DESC-001).») y «Es un método validado en backtest.» en el `mecanismo` del mismo informe, se entrega con G3 APTO y la frase está en el técnico y en el JSON. Cada campo de texto es su propia unidad y la regla del párrafo anterior no cruza campos | Igual que el párrafo anterior, pero por objeto: en `g3_met13`, para cada opción (`clases.X.opciones[i]`, `paquete_para_bloque_B[i]`, `informes_clase…[OPP-]`), las afirmaciones de madurez sin ficha de un campo se atribuyen (solo regla A) a las fichas de los demás campos de texto del mismo objeto. Hoy ninguna ficha está VALIDADO, así que «método/modelo/indicador … validado» en una opción que cita una ficha bloquea. Medir con r01_03 (los ciclos normales no tienen «validad…», verificado) | abierto |
| H-18 | media | `r02_02::test_fp_retira_opciones[S1_hemos_comprobado]`, `test_fp_lectura_del_conjunto_comprobado`; `r02_01` S1–S5 | Esperado: no bloquea. Obtenido: «Hemos comprobado con ST-DESC-001 que el precio está en el percentil 95 %», «comprobado a fecha…», «contrastado con la serie del proveedor», «probado con la serie semanal», «Riesgo verificado con RISK-DD-001…» bloquean: retiran las 3 opciones de RV o, en la lectura del conjunto, bloquean el run (6 opciones a `_bloqueados`). Los sinónimos de la r02 (`[PROPUESTO]`) cuentan el uso normal de «comprobar un dato con la ficha» como «validado» | Que los sinónimos (comprobado, contrastado, probado, verificado, testeado, tested, verified) solo cuenten como «validado» cuando la ficha es su sujeto o va ligada a ellos sin preposición instrumental: descartar si van seguidos de «con», «contra», «en la fuente», «a fecha» o de «que» (`RE_INSTRUMENTO = re.compile(r"^\s+(?:con|contra|frente\s+a|a\s+fecha|que)\b")`) o precedidos de «hemos/he/se ha» + palabra + «con» + ficha. O sacar los sinónimos y declararlos límite. Medir en las dos direcciones con S1–S5, r01_01 y los bancos | abierto |
| H-19 | media | `r02_02::test_fp_retira_opciones[D2_ninguna_validada]`; `r02_01` D1–D7 | Esperado: la declaración honesta de R22 no bloquea. Obtenido: «… ambos implementados y ninguno validado todavía», «ninguna ficha del Catálogo está validada», «Ningún método del ciclo, tampoco ST-DESC-001, está validado», «no está, por ahora, validado», «no se considera validado», «dista de / está lejos de estar validado» bloquean; D2 retira las 3 opciones. El falso positivo aceptado del banco 2 («Ningún método del Catálogo está validado todavía») es justo lo que R22 pide declarar: no es un falso positivo aceptable | En `_negada`: «ningún», «ninguno», «ninguna», «tampoco» niegan (hoy solo están en `_DOBLE`; la doble negación se mantiene con «nadie diría que… no»); saltar los incisos entre comas («, por ahora,») como auxiliares; añadir «considera», «consideran», «considerarse», «lejos», «dista», «distan» con «de». Quitar el falso positivo aceptado de INC-T165-01. D1–D7 como pruebas que no saltan | abierto |
| H-20 | media | `r02_01` J1a–J2c | Esperado: como en H-05, F6 retira la opción cuyo informe de clase afirma la madurez falsa. Obtenido: no salta con `{"ficha": X, "validado": "sí"}` (también «yes», 1, `"nivel_madurez": "3"`), con la madurez anidada (`{"madurez": {"nivel": "VALIDADO"}}`), la ficha anidada (`{"calculo": {"ficha": X}, "madurez": "validado"}`) o `{"metodos": [{"id": X}], "estado": "validado"}`. Como H-05, no llega a los ficheros entregados (`estado_madurez_metodos` no pasa al paquete) | En `_parte`: con una clave de madurez fuerte, una cadena afirmativa (`sí`, `si`, `yes`, `true`, `ok`, `1`) da el nombre de la clave y una negativa (`no`, `false`, `0`) «no <clave>»; un entero 0/1 en esas claves, igual; «1»–«3» en texto en una clave de nivel, el nivel. En `_textos_de`, un registro con ficha (o con clave de madurez) aplana en la misma unidad los escalares de sus diccionarios y listas hijos (un nivel). Pruebas J1a–J2c | abierto |
| H-21 | baja | `r02_01` N4a–N4d | Una ficha escrita con guion bajo («ST_DESC_001», «vol_garch_001»), puntos («ST.DESC.001») o cuatro cifras («ST-DESC-0001») no se reconoce, y entonces tampoco actúa la regla B (falla cerrado). De extremo a extremo solo bloquea si el mismo campo cita además la ficha bien escrita | En `Fichas.re_completa` y `re_espacios`, aceptar `[-_.\s]` como separador (`[\s_.-]+`) y `\d{3,4}` al final con `_resolver` normalizando a `-` y a tres cifras cuando haya cero a la izquierda; quitar `_` de las exclusiones de los límites de palabra. Pruebas N4a–N4d; los OPP-, CALC- y los años siguen sin ser ficha | abierto |
| H-22 | baja | `r02_01::test_coste_lineal_en_fichas_por_parrafo` | Con muchas fichas en un párrafo el coste es cuadrático: 2000 fichas (50 KB) 0,6 s; 8000 (203 KB) 8,4 s (razón 14, lineal ≈ 4). Causas: `Fichas.buscar.libre` recorre toda la lista `ocupado` por cada coincidencia, y `_negada` calcula `en_ficha` con `any(...)` sobre todas las menciones por cada palabra. INC-T165-01 dice «la ventana es fija: el coste es lineal» | `libre`: mantener `ocupado` ordenado y comprobar solo los vecinos con `bisect`; `_negada`: `en_ficha` con `bisect_left` sobre las posiciones de inicio de `menciones` (ya ordenadas). Corregir la frase de INC-T165-01. La prueba de coste con razón < 8 | abierto |
| H-23 | baja | `r02_01` N7a, N7b, H1, H2 y `test_fp_pb47` F1, F2 | (a) Sin declarar como límite: la tabla transpuesta (fichas en la cabecera, «Madurez | validado» en otra fila; también en HTML) no se lee. (b) Con PB-47, «## ML-CLUS-001\n\nMadurez: documentado; no se usa» y la declaración en una nota del párrafo siguiente bloquean: la declaración no cruza párrafos y el título es su propio párrafo. (c) La afirmación dos párrafos después del título sí está declarada | En `_unidades`, unir una línea de título Markdown (empieza por «#») al párrafo siguiente (y, en `texto_html`, `h1`–`h6` con su siguiente bloque). En una tabla, leer cada fila sin ficha junto con la fila de cabecera si esta tiene fichas (o declarar la tabla transpuesta en INC-T165-01). Pruebas N7b/H2 (o la declaración) y F1 | abierto |
| H-24 | baja | `.venv/bin/python .docs/tickets/T-165/r02_mutantes.py --copia <copia>` | El script del implementador se para con `AssertionError` en N13: su expresión (`… and j > 0 and tokens[j - 1] in _NIEGA_DE`) no está en `ht09.py` (`… and previo in _NIEGA_DE`), y la de N17 tampoco (`for x in tokens[:j]` frente a `for x, _ in tokens[:j]`). N13 a N22 no se ejecutan en una pasada, así que «0 de 31 vivos» no es reproducible con el script tal como está | Cambiar N13 a `' or (w == "de" and previo in _NIEGA_DE)'` → `''` y N17 a `"return not any(x in _DOBLE for x, _ in tokens[:j])"` → `"return True"`; volver a ejecutarlo entero y poner su salida en `pruebas.md`. Los C13 y C17 de `r02_03_mutantes.py` son esas dos expresiones | abierto |
| H-25 | baja | `git show --stat 27807e4`; `git ls-files .venv` | El commit «instantánea» añade `.venv` al índice: un enlace simbólico a la ruta absoluta del venv de la máquina. `.gitignore` tiene `.venv/`, que con la barra no ignora un enlace (git lo trata como fichero). No debe llegar a `develop` | `git rm --cached .venv` antes del commit a `develop`, y en `.gitignore` cambiar `.venv/` por `.venv` (sin barra, ignora el directorio y el enlace) | abierto |
| H-26 | baja | `r02_01` N5a, N6a, N6b | (a) «Hoy, más que nunca, ST-DESC-001 está validado»: «nunca» se lee como negación aunque vaya en «más que nunca» / «como nunca». (b) «se validaba», «se valide» no están en la raíz (`_VAL` tiene «validó», «validan», «validará»…, no el imperfecto ni el subjuntivo) | (a) En `_negada`, «nunca» y «jamás» no niegan si `previo in ("que", "como")`. (b) `_VAL`: añadir `valid(?:aba|aban|e|en|ase|asen|ara|aran|ando)` (y `validándo(?:se|lo|la)`). Pruebas N5a, N6a, N6b | abierto |
| H-27 | baja | `r02_03_mutantes.py --solo X05 X07` | Dos mutantes del revisor viven: X05 (tras una tabla, el párrafo siguiente sin ficha toma las fichas de la tabla) y X07 (el técnico vuelve a leerse por líneas, que era la unidad de la r01 y la causa de H-02 en el técnico). Las dos reglas de la r02 no tienen prueba que las fije | X05: prueba unitaria «| ST-DESC-001 | implementado |\n\nEste método está validado.» con el resultado que se decida (hoy OK) y su porqué en INC-T165-01. X07: en `test_t165_g3_met13.py`, `g3_met13_tecnico` con un técnico «La volatilidad sale de VOL-GARCH-001.\nEs un método validado.» (dos líneas, un párrafo) → BLOQUEO con la ruta «informe_tecnico, línea 1» | abierto |

### Bajos que hay que subsanar en este ticket (regla del operador, 16-11-2026)

H-21 (separadores de ficha), H-22 (coste en fichas por párrafo), H-23 (título y tabla transpuesta), H-24 (script de mutantes),
H-25 (`.venv` en el índice), H-26 (más que nunca, imperfecto y subjuntivo) y H-27 (dos mutantes vivos), con la corrección exacta de la tabla y su prueba.

## Decisiones `[PROPUESTO]` de la r02 y límites declarados

| Decisión o límite | Valoración del revisor |
| --- | --- |
| Normalización (NFKC, Cf, guiones Pd, homoglifos, minúsculas) | De acuerdo, bien descrita. Falta «_» y «.» como separadores de ficha (H-21) |
| Fichas parciales; una ambigua («?…») bloquea si no se declara | De acuerdo: falla cerrado y está declarado |
| Unidad: párrafo, fila, campo o registro; el párrafo anterior solo para afirmar | Razonable y bien descrito, pero el campo como unidad deja pasar la afirmación en otro campo de la misma opción (H-17), que no está entre los límites; y la declaración tras un título bloquea (H-23) |
| «Certificado» no es sinónimo de validado | De acuerdo (es el certificado R13) |
| Sinónimos verificado, probado, contrastado, comprobado, testeado = validado | **No razonable tal como está**: el falso positivo con su uso normal («comprobado con la ficha») no se midió y bloquea el run (H-18). O se acotan o se declaran límite |
| «Validado por» solo excluye personas | De acuerdo (cierra H-01) |
| Prosa financiera por lista de sustantivos ligados | Necesaria para H-07, pero la regla de «el más cercano» abre un escape (H-13): «estrategia» y los complementos del método no deberían contar |
| Negación con lista cerrada, hasta seis auxiliares, «: no» detrás | La de delante, razonable; la de detrás, demasiado amplia (H-14); faltan «ningún/ninguno/tampoco» y los incisos (H-19) |
| Falso positivo aceptado «Ningún método del Catálogo está validado todavía» | **No aceptable**: es la declaración que R22 pide (H-19) |
| Falso positivo aceptado «El modelo macro del BCE está validado por su comité» tras un párrafo con ficha | Aceptable y bien declarado |
| `_fuente_riesgo` (rama no alcanzable hoy) | De acuerdo y bien declarado; los ciclos normales no cambian |
| Límites: método sin ficha, sinónimos fuera de la lista, afirmación a más de un párrafo, abreviatura con punto | Razonables y bien descritos. Faltan: otro campo del mismo objeto (H-17), tabla transpuesta (H-23). Y la frase «el coste es lineal» es falsa con muchas fichas (H-22) |
| Cifras de falsos positivos (1 de 15) | Ciertas para su banco, pero no representativas: 14 de 49 con frases nuevas del revisor. INC-T165-01 debería dar la cifra del revisor también |

## Mutantes (r02_mutantes del implementador y r02_03 del revisor)

En copias desechables (`mut165`, `mut165b`), contra `tests/test_t165_g3_met13.py` con `-x`.

- **`r02_mutantes.py` del implementador (31):** de una pasada se para en N13 con `AssertionError` (H-24), después de 21 muertos
  (M01–M32 y N01–N12). Con `--solo` corren N14, N15, N16, N18, N19, N20, N21 y N22: **los 8 mueren**. N13 y N17 no se pueden
  aplicar tal como están escritos; con la expresión real (C13 y C17 de `r02_03`) **mueren**. Así que, una vez corregido el script,
  la afirmación «no sobrevive ninguno de los 31» se cumple.
- **`r02_03_mutantes.py` del revisor (9):** C13, C17, X01, X02, X03, X04 y X06 mueren; **viven X05** (una tabla deja de cortar el
  «párrafo anterior»: ninguna prueba fija que un párrafo sin ficha después de una tabla no toma las fichas de la tabla) y **X07** (el
  técnico se vuelve a leer por líneas, como en la r01: ninguna prueba del técnico tiene la ficha y la afirmación en dos líneas del
  mismo párrafo). Ver H-27.

| Mutante | Resultado | Lo que lo mata |
| --- | --- | --- |
| M01, M03, M09, M12, M13, M14, M15, M20, M32 (los vivos de la r01) | muertos | `test_r02_no_salta[h07_sin_estar]`, `test_r02_m03_…`, `test_r02_m09_…`, `test_r02_m12_…[method_id]`, `test_r02_m14_…`, `test_r02_m15_…`, `test_r02_m20_…`, `test_r02_m32_…` |
| N01–N12, N14–N16, N18–N22 | muertos | sus casos `test_r02_bloquea` / `test_r02_no_salta` / `test_r02_h0x_…` |
| N13, N17 | no aplican (H-24) | con la expresión real, C13 y C17 mueren (`h07_a_la_espera`, `h11_doble_negacion`) |
| X01 sin «: no» detrás | muerto | `test_r02_no_salta[h07_dos_puntos_no]` |
| X02 sin la excepción de personas | muerto | `test_bloquea_…[ML-CLUS-001 documentado por el operador]` |
| X03 sin el sustantivo ligado delante · X04 sin el éxito delante de «validación» | muertos | `test_no_salta_…[La tesis, validada por el dato de empleo…]`; `test_r02_bloquea[h03_superada]` |
| X05 una tabla no corta el párrafo anterior | **vivo** | — |
| X06 regla B nunca salta | muerto | `test_bloquea_…[… ML-SUPER-001 …]` |
| X07 técnico por líneas | **vivo** | — |

## Veredicto

**NO APTO.** La r02 corrige lo que la r01 encontró: los 105 casos de `r01_01` pasan, los cuatro escapes de extremo a extremo de la
r01 bloquean (también `guion_no_separable`, cuyo fallo era del script), los ciclos normales siguen en G3-MET-13 OK con los mismos
entregables que la r01, y las cuotas se mantienen. Pero con familias nuevas, que no están en ningún banco, cinco madurez falsas se
entregan con G3 APTO y `estado_g3` APTO, demostradas de extremo a extremo con el cliente simulado: un método descrito con un
sustantivo de la lista ligada (H-13), «validado: no hay dudas» (H-14), el éxito de «validación» lejos de la palabra (H-15), un
«rechazado» de otra cosa o negado que declara la ficha de PB-47 (H-16) y la afirmación en otro campo de la misma opción (H-17).
Además, el uso normal de «comprobado con» y la declaración honesta «ninguna ficha está validada» retiran opciones o bloquean el run
(H-18, H-19), y los bajos H-21 a H-27 se subsanan en este ticket.

Vuelve a `ri-implementar`. Para la r03, el revisor volverá a ejecutar `r01_01`, `r01_02`, `r02_01`, `r02_02`, `r01_03` (mismos
entregables), `r02_03` y el `r02_mutantes.py` corregido. Lección que se repite (`claude/2026-11-12_filtros-por-patron-en-texto-libre`):
cada regla de excepción nueva (sustantivo ligado, «: no», sinónimos) abre su propia familia; conviene medir cada una con frases
escritas por otro antes de darla por buena. No he cerrado el ticket ni tocado la deuda técnica.

---

# Ronda r03

- **Revisor:** el mismo subagente de Claude de la r02, sin haber implementado nada · 17-11-2026
- **Copia revisada:** worktree desechable `qa165r03` en `6304085` (r03 sobre la QA r02 rebasada a `c728c91`), con `.venv` enlazado
  (ya no está en el índice: H-25 corregido). Sin red ni gasto. Exportaciones `m3a` y `m3b` para los mutantes.
- **Foco pedido por el coordinador:** (1) que ninguna madurez falsa llegue por otra vía, (2) el riesgo operativo del falso positivo
  con los prompts del corpus, (3) que la forma canónica no rompa esquemas ni plantillas, (4) la regresión de los textos del ejecutor.

## Reproducción

```bash
cd bloque_a/11_Ejecutor
../../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_t165_g3_met13.py tests/test_t159_extremo_a_extremo.py
../../.venv/bin/python -m pytest -q -p no:cacheprovider -s ../../.docs/tickets/T-159/revisores/r01_02_sondas.py -k pb47
../../.venv/bin/python ../../.docs/tickets/T-165/r03_bancos_frases.py
../../.venv/bin/python ../../.docs/tickets/T-165/revisores/r03_01_corpus.py                    # corpus: prompts y ejemplos
../../.venv/bin/python -m pytest -q -p no:cacheprovider ../../.docs/tickets/T-165/revisores/r03_02_ataques_estructurales.py -rf
../../.venv/bin/python -m pytest -q -p no:cacheprovider -s ../../.docs/tickets/T-165/revisores/r03_03_extremo_a_extremo.py -rf
../../.venv/bin/python ../../.docs/tickets/T-165/revisores/r01_03_ciclos_normales.py --salida <scratch>/ciclos_r03   # y diff con la r02
cd ../..
.venv/bin/python .docs/scripts/cadena_a_b.py --trabajo <scratch>/cadena_r03
.venv/bin/python .docs/tickets/T-165/r03_mutantes.py --copia <export>      # en dos mitades con --solo
```

| Comprobación | Resultado |
| --- | --- |
| `test_t165_g3_met13.py` + `test_t159_extremo_a_extremo.py` | 120 superadas. El cambio de `test_t159` es solo la expresión del aviso de la retirada de PB-30 («el control G3»); la prueba de PB-47 no cambia (CA-2 se mantiene) |
| Sonda de T-159 (`-k pb47`) | pasa: «['BLOQUEADO', 'APTO_CON_ADVERTENCIAS', 'APTO_CON_ADVERTENCIAS'] · entregables con «validado»: []» |
| `r03_bancos_frases.py` | Confirmado: banco 3 sin la raíz, 0 de 30 legítimas bloquean y 0 de 15 falsas pasan; con la raíz, 15 de 15 bloquean. Los recuentos sobre los bancos anteriores, también |
| Ciclos normales (r01_03, 10 ciclos, 20 G3V-) | G3-MET-13 OK y mismos dictámenes. Técnico, visual y JSON **idénticos a los de la r02** una vez quitadas la forma canónica, la línea R22 del técnico y `x_madurez_metodos`; solo cambia `resumen.json` (cuenta «implementado» de la forma canónica). Confirmado |
| Cadena A→B (`cadena_a_b.py`) | rc 0: 1 entrega del Bloque B, válida contra su esquema, y la vuelta CT-04 registrada (en el simulado ninguna entrada de `paquete_para_bloque_B` cita una ficha, así que la anotación no llega a B) |
| Mutantes del implementador (`r03_mutantes.py`, 23) | **Los 23 mueren** (en dos mitades) |
| Cuotas | ruff 2813 (= cuota), mypy A 109 (= cuota) |

## Hallazgos de la r02

| ID | Estado en la r03 |
| --- | --- |
| H-13, H-14, H-15, H-17, H-23 | Corregidos por diseño (la raíz bloquea en todo el ámbito, sin excepciones de prosa). `r02_01` y `r02_02`: 0 de 33 falsas pasan |
| H-16 | Corregido: solo la forma canónica declara una ficha no servida (`r03_02::test_control_pb47_sin_canonica`) |
| H-18 | Convertido en límite declarado (sinónimos no cuentan). Razonable con la forma canónica al lado; ver la valoración de decisiones |
| H-19 | Cambio de expectativa declarado: la declaración honesta la escribe el ejecutor; en la prosa del modelo bloquea. Ese es el riesgo de H-28 |
| H-20, H-21, H-22, H-24, H-25 | Corregidos (las claves del camino se leen; separadores «_» «.» y cuatro cifras; ×4 de 2000 a 8000 fichas; mutantes de la r02 corregidos; `.venv` fuera del índice) |
| H-26 | No aplica: no hay negación, y la raíz cubre «validaba» y «valide» |
| H-27 | X05 no aplica (no hay párrafo anterior); X07 lo mata `test_el_tecnico_es_un_ambito…` |

## Lo que ha mirado esta ronda

**1. Otras vías para una madurez falsa (`r03_02`, `r03_03`).**
- Con la raíz «valid-», la madurez falsa no llega por ninguna vía:
  - ni en otro campo de la opción;
  - ni con la forma canónica imitada o falsa: «[madurez: VALIDADO]», «[madurez: IMPLEMENTADO] y en la práctica validado» y un corchete suelto bloquean;
  - ni en un JSON con la madurez en la clave («validado: true», `{"ST-DESC-001": "validated"}`, «nivel madurez: 3»);
  - ni en el visual o el técnico, porque los dos documentos llevan siempre sustantivos de método o fichas.
- El modelo sí puede escribir la forma canónica correcta de una ficha no servida y nombrarla en uso. Está declarado y es verdad
  del Catálogo.
- Pasan, como se declara, los sinónimos y las madurez sin la raíz: «probado», «fiable», «apto para producción», «proven».
- No declarado:
  - la misma raíz con tilde, «válido» o «válida». Llega a la entrega con G3 APTO (H-30);
  - variantes inmediatas de la lista de sustantivos: «metodología», «fuera de la muestra» y «sistema» (H-32).
- `estado_madurez_metodos` se reescribe y se descarta lo que dijo el modelo. Está declarado; no deja traza (observación, no hallazgo).

**2. Riesgo operativo del falso positivo, medido con el corpus (`r03_01`, `r03_03`).** Es la cuestión clave de la ronda.
- **Ejemplos de salida de los doce Analistas, leídos como opción en F6:** se retiraría 1 de 12. El ejemplo del Analista de Fondos
  dice en su `valoracion`: «las recompras y ventas de activos cerca del NAV validan las valoraciones». El campo de madurez de los
  12 lo reescribe el ejecutor y no bloquea.
- **Ejemplo del paquete V5.0:** OK, sin retiradas.
- **Lo que los prompts piden escribir en prosa con la raíz**, fuera de un campo que reescriba el ejecutor:
  - **Analizador, regla R22:** «Declaras si cada método usado está documentado, implementado o validado». Su texto (lectura del
    conjunto, régimen, limitaciones) está fuera de las opciones, así que la declaración honesta («implementados y aún no
    validados») **bloquea el run entero**. Comprobado de extremo a extremo: F6 BLOQUEADO y 6 opciones a `_bloqueados`.
  - **Analizador, tabla de degradación y puertas PS:** «Pendiente de validación» y el estado «validada» de una tendencia.
    «Contrarias no disponible: las finalistas … quedan … en «Pendiente de validación» (PS5)» **bloquea el run entero**
    (comprobado).
  - **Analista de Prospectiva, R22:** «Declaras el estado de madurez de cada método (documentado, implementado, validado)».
  - **Analista de Divisas:** «validación pendiente de la batería mínima; decláralo así, R22».
  - **Analistas de RF, Monetarios y Tipos:** «¿Qué catalizador fechado puede validar o invalidar la tesis?». Un catalizador
    redactado así **retira las 3 opciones** (comprobado).
  - **Instrucción del propio ejecutor al Sintetizador V6** (`diseno_v6.INSTR_SINTESIS`): «Sobre el paquete ya validado…» y
    «vienen calculadas y validadas». Si el modelo la repite en la lectura del conjunto, **cae la entrega en F7** (comprobado). La
    r03 cambió el texto de respaldo, pero no la instrucción.
  - **El Motor:** escribe en RC, para cada cálculo servido, «ninguna conocida (ficha implementada, no validada)»
    (`motor/servicio.py`).
- El cliente simulado no escribe nada de esto, así que los ciclos normales en APTO (CA-3) no miden este riesgo. Con la API real,
  un Analizador que siga su prompt (R22) dejaría sin entrega cada ciclo. Ver H-28.

**3. La forma canónica frente a esquemas y plantillas.**
- El esquema admite `x_madurez_metodos` (`^x_`) y ningún patrón del esquema afecta a cadenas con fichas.
- Pero `nombre_llano` (maxLength 70), `por_que_llano` (160) y `que_puede_salir_mal_llano` (200) se anotan como cualquier cadena.
  Con una ficha cerca del máximo, la anotación (+24 caracteres) supera el límite: ESQUEMA_JSON y **entrega bloqueada**
  (comprobado con `nombre_llano`; H-31).
- La plantilla del técnico solo gana la línea R22 en «7. Limitaciones». El visual normal no cita fichas, así que no cambia.

**4. Regresión de los textos del ejecutor.**
- Los literales que cambian («el control G3», «ya revisado por G3», «el Motor no sirvió los clústeres», limitación y laguna
  anotadas) están probados (R22 y R23 mueren) y no cambian nada más en los ciclos normales.
- Pero el técnico cita las rutas de sus entregables hermanos, que son texto del ejecutor sacado de la configuración, y G3-MET-13
  las lee como prosa. Con la carpeta de salida en un directorio «validaciones», **cada entrega cae en F7** (comprobado; H-29).
  Lo descubrí porque el nombre de una prueba con «valido» bloqueaba por la ruta temporal: los identificadores de `r03_03` ya no
  llevan la raíz.

## Hallazgos de la r03

| ID | Gravedad | Cómo reproducirlo | Esperado / obtenido | Corrección | Estado |
| --- | --- | --- | --- | --- | --- |
| H-28 | alta | `r03_01` (sección 3 y ejemplo de Fondos); `r03_03::test_fp_lectura_del_conjunto[analizador_declara_r22]`, `[analizador_degradacion_ps5]`, `test_fp_sintetizador_v6_repite_la_instruccion_del_ejecutor`, `test_fp_informe_de_clase[*]` | **Esperado:** con la API real, el ciclo entrega cuando los agentes siguen sus prompts. **Obtenido:** el corpus pide la raíz en prosa (R22 del Analizador y de Prospectiva, «Pendiente de validación» y «validada» de las puertas PS y del ciclo de vida, «validación pendiente… decláralo así» de Divisas, «catalizador que valida la tesis»), y también la pone el propio ejecutor (instrucción al Sintetizador V6, «ficha implementada, no validada» del Motor en RC). Fuera de una opción, el ámbito es el documento: una sola aparición bloquea el run o la entrega. Dentro, retira la opción. El simulado no lo ejerce, y por eso CA-3 no lo detecta | (1) Una constante del ejecutor, `REGLA_R22_REDACCION = "R22: la madurez de los métodos la escribe el ejecutor junto a cada ficha. No uses la raíz «valid-» (validado, validación, validar, validez) en ningún texto: escribe «confirmar», «comprobar» o «pendiente de confirmar»."`, añadida a las instrucciones de `INSTR` (CT-06, respuesta a objeciones), de la integración (AG-02), del Redactor (AG-17) y de `INSTR_SINTESIS` (AG-26). En `INSTR_SINTESIS`, «Sobre el paquete ya validado» pasa a «Sobre el paquete ya revisado por G3» y «calculadas y validadas» a «calculadas y revisadas». (2) Si G3-MET-13 salta por la regla A en el texto de un agente fuera de una opción, una reescritura con la regla, como ya hace `diseno_v6` para el índice de legibilidad (`instr + " Reescribe: …"`), y se bloquea solo si persiste. (3) El cliente simulado escribe en la integración una declaración R22 con la raíz, como pide el prompt, y una prueba exige que el ciclo entregue tras la reescritura. (4) El texto del Motor en RC, «ficha implementada, sin certificado R22» o similar, sin la raíz | abierto |
| H-29 | media | `r03_03::test_fp_ruta_de_salida_con_la_raiz` | **Esperado:** el ciclo normal entrega con cualquier carpeta de salida. **Obtenido:** con la salida en «…/validaciones/…», F7 BLOQUEADO por G3-MET-13 («validaciones» para ML-CLUS-001, extracto «…les hermanos…»). `g3_met13_tecnico` lee las rutas que escribe el ejecutor (fila «Entregables hermanos») | Comprobar un técnico generado con marcadores en lugar de rutas: en `redaccion.generar`, `tec_g3 = self.tecnico(paquete, extras, g3, {k: f"<{k}>" for k in rutas_entrega}, estado_run, cons)` y `sint.g3_met13_tecnico(bloque, res, tec_g3)`. El escrito sigue llevando las rutas reales. La prueba de `r03_03` como regresión | abierto |
| H-30 | baja | `r03_02::test_escapa[V1a…V1c]`; `r03_03::test_escapa[raiz_con_tilde]` | «ST-DESC-001 es un método válido fuera de muestra» llega a la entrega con G3 APTO. «Válido» y «válida» son la raíz «valid-» con tilde («validez» sí cuenta) y no están entre los límites declarados | `RE_VALID = re.compile(rf"(?<![{_L}])(?:re|con|pre)?v[aá]lid[{_L}]*")` y las tres pruebas como bloqueo. O declararlo como límite en INC-T165-01 | abierto |
| H-31 | baja | `r03_03::test_esquema_nombre_llano_con_ficha_cerca_del_maximo` | Un `nombre_llano` de 52 caracteres con «ST-DESC-001» pasa a 76 con la anotación: supera el maxLength 70, salta ESQUEMA_JSON y la entrega se bloquea (F7 con G3-MET-13 OK). Lo mismo con `por_que_llano` (160) y `que_puede_salir_mal_llano` (200) | En `redaccion.generar`, sacar del esquema las claves con `maxLength` y pasarlas a `sint.anotar_json(bloque, obj, sin_anotar=…)`, que no anota esas claves. G3-MET-13 las sigue leyendo y la madurez canónica sigue en `x_madurez_metodos`. La prueba como regresión | abierto |
| H-32 | baja | `r03_02::test_escapa_casi_lista[M1…M3]` | En un ámbito sin fichas, «La metodología de selección está validada», «Señal compuesta validada fuera de la muestra» y «Nuestro sistema de selección está validado» pasan. El límite genérico está declarado, pero son variantes inmediatas de la lista («método», «fuera de muestra») | En `RE_METODO`, `metodolog[ií]as?` y `fuera\s+de\s+(?:la\s+)?muestra`, y «sistema» (o declarar «sistema» como límite). Las tres pruebas | abierto |

### Bajos que hay que subsanar en este ticket

H-30, H-31 y H-32, con su corrección y su prueba.

## Decisiones `[PROPUESTO]` de la r03

| Decisión | Valoración del revisor |
| --- | --- |
| Forma canónica «FICHA [madurez: X]» escrita por el ejecutor después de G3-MET-13; línea R22 en el técnico; `x_madurez_metodos` | De acuerdo. No rompe el esquema salvo en los campos con maxLength (H-31) y la cadena A→B sigue válida |
| La prosa no se interpreta; la raíz bloquea en el ámbito | De acuerdo como control: cierra las familias de escapes de las rondas anteriores, y los 23 mutantes mueren. **Pero el precio no está medido donde importa:** con el corpus, la raíz no es una frase legítima ocasional, sino lo que piden los prompts del Analizador, de Prospectiva y de Divisas, y la instrucción del propio ejecutor al Sintetizador (H-28). «Se revisa en el modo sombra» no basta: el riesgo ya se ve en los prompts y tiene una mitigación barata del lado del ejecutor |
| Ámbito: la opción o la candidata; fuera, el documento | De acuerdo con el criterio, pero el documento técnico incluye texto del ejecutor sacado de la configuración (H-29) |
| `estado_madurez_metodos` lo reescribe el ejecutor y se descarta lo del modelo | De acuerdo (bloquearlo retiraría toda opción que siga el prompt). Sugerencia sin gravedad: dejar en HA lo que se descartó, para auditar R22 |
| Sinónimos y madurez sin la raíz como límite | Razonable con la forma canónica al lado de cada ficha; bien declarado. Falta «válido» (H-30) |
| Una ficha no servida con la forma canónica correcta escrita por el modelo pasa | De acuerdo: lo que dice es la verdad del Catálogo, y PB-47 pide «declara documentado» |

## Veredicto

**NO APTO.** El enfoque estructural cierra las familias de escapes de la r01 y la r02:
- ninguna madurez falsa con la raíz llega a la entrega por otro campo, por la forma canónica, por el JSON, por el visual ni por el técnico;
- los 23 mutantes mueren;
- los ciclos normales solo cambian por la forma canónica;
- la cadena A→B sigue válida;
- las cuotas se mantienen.

Pero queda abierto un alto, H-28. Con el corpus tal como está, los agentes tienen que escribir la raíz que G3-MET-13 prohíbe:
- el R22 del Analizador y de Prospectiva;
- las puertas PS («Pendiente de validación») y el ciclo de vida de las tendencias;
- la instrucción de Divisas;
- las preguntas de catalizadores;
- la instrucción del propio ejecutor al Sintetizador V6.

Fuera de una opción, una sola aparición deja el ciclo sin entrega, y el simulado no lo ejerce. A eso se suma una ruta de salida
con la raíz, que bloquea toda entrega (H-29, medio).

Vuelve a `ri-implementar`. En la r04 volveré a ejecutar `r03_01`, `r03_02` y `r03_03`, los ciclos normales, la cadena A→B y los
mutantes. No he cerrado el ticket ni tocado la deuda técnica.

---

# Ronda r04

- **Revisor:** subagente de Claude nuevo, sin haber implementado nada · 17-11-2026
- **Copia revisada:** worktree desechable `qa165r04` en `8da16a1` (`wip/t165r04`, r04 rebasada sobre develop `b9c71d2`), con el
  venv del proyecto. Sin red ni gasto. Exportación `qa165r04_mut` para los mutantes.
- **Foco pedido por el coordinador:** (1) las lagunas omitidas, (2) el límite dentro de una opción (Fondos), (3) que la reescritura
  no abra camino a una madurez falsa, su coste y su número, (4) los 5 fallos de `r03_03`, (5) regresiones.

## Reproducción

```bash
cd bloque_a/11_Ejecutor
../../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_t165_g3_met13.py tests/test_t159_extremo_a_extremo.py \
    tests/test_t145.py tests/test_t148.py tests/test_t113_deuda.py
../../.venv/bin/python ../../.docs/tickets/T-165/revisores/r03_01_corpus.py
../../.venv/bin/python -m pytest -q -p no:cacheprovider ../../.docs/tickets/T-165/revisores/r03_02_ataques_estructurales.py -rf
../../.venv/bin/python -m pytest -q -p no:cacheprovider -s ../../.docs/tickets/T-165/revisores/r03_03_extremo_a_extremo.py -rf
../../.venv/bin/python -m pytest -q -p no:cacheprovider -s ../../.docs/tickets/T-165/revisores/r04_01_reescritura_y_limites.py -rf
../../.venv/bin/python ../../.docs/tickets/T-165/revisores/r01_03_ciclos_normales.py --salida <scratch>/ciclos_r04   # y diff con ciclos_r03
cd ../..
.venv/bin/python .docs/scripts/cadena_a_b.py --trabajo <scratch>/cadena
.venv/bin/python .docs/tickets/T-165/r03_mutantes.py --copia <export> --solo R24 … R35
```

| Comprobación | Resultado |
| --- | --- |
| T-165 + T-159 + T-145 + T-148 + T-113 | **306 superadas** (las 22 de T-145/T-148 que el implementador corrigió sin repetir, en verde) |
| Pruebas vecinas que nombran AG-02 (17 archivos: goldens de fase 3, integración, V5, V6, guías, contratos, unitarias…) | **931 superadas**: la llamada de más del Analizador en cada ciclo V5 simulado no rompe ningún recuento ni golden de esos archivos. No es la suite completa (regla de la QA) |
| `r03_01` (corpus) | Igual que en la r03: 1 de 12 ejemplos de ficha bloquea (Fondos, «validan las valoraciones»); el paquete V5.0, OK |
| `r03_02` (ataques estructurales) | 28 de 28: ninguna madurez falsa con la raíz llega, y H-30 y H-32 cerrados |
| `r03_03` | 4 superadas y 5 fallos, los que declara el implementador. Ver «Los 5 fallos de r03_03» |
| `r01_01`, `r01_02`, `r02_01`, `r02_02` | Los fallos son los falsos positivos aceptados desde la r03 (la raíz bloquea en su ámbito: «no validado», «sin validar», «la OPEP validó…») y el caso roto del propio `r01_02` (`guion_no_separable`). Ningún escape nuevo |
| Ciclos normales (`r01_03`, 10 ciclos) | Mismos dictámenes y opciones que la r03 (diff vacío), G3-MET-13 OK en los 20 G3V-. Cambian solo: una llamada más del Analizador en V5 (p. ej. 70 → 71, +0,77 UC en `v5_12tipos_2026`; 7 → 8 en `por_defecto_div`), la limitación reescrita «Métodos usados (R22): …» en técnico y JSON, y las rutas de trabajo. V6: mismas llamadas, unos tokens más de instrucción |
| Cadena A→B | rc 0: 1 entrega del Bloque B, válida, y la vuelta registrada |
| Mutantes del implementador R24–R35 | **12 de 12 muertos** (R01–R23 no los repetí: el código que mutan no cambia en la r04 salvo `RE_VALID`, que mata R30) |
| Cuotas | ruff 2813 (= cuota), mypy A 109 (= cuota) |

## Lo que ha mirado esta ronda

**3. La reescritura no abre camino a una madurez falsa (`r04_01::test_reescritura_*`).**
- La respuesta reescrita pasa entera por G3-MET-13: una reescritura que imita «ST-DESC-001 [madurez: VALIDADO]» o que declara
  «ML-CLUS-001 [madurez: IMPLEMENTADO]» con la ficha en DOCUMENTADO no llega a la entrega. Bien.
- El número sale de `redaccion.reescrituras_r22` (`[PROPUESTO]`, con su comentario): con 0, una llamada y bloqueo; con 2, tres
  llamadas y bloqueo si persiste. Una reescritura sin respuesta deja la primera, con la raíz, y bloquea (falla cerrado). Bien.
- Coste: la reescritura se carga en la bolsa COMÚN y en la contabilidad (AG-02: 2 llamadas, 2,6 UC en el simulado). Es una
  regeneración completa (≈ 35 000 tokens de entrada en el simulado), no un retoque. La cota de `estimar_coste_ciclo_a.py` la
  prevé leyendo la misma clave. Aceptable.
- Pero la reescritura de la integración no recibe la instrucción original: pasa «Integra los informes de clase. » más la regla, y
  pierde los campos pedidos y «No cambies la selección: la ha hecho HT-03» (H-36). Y ninguna reescritura dice al agente qué
  texto lleva la raíz, a diferencia de la de legibilidad, que pasa `frases_largas` (H-37).

**4. Los 5 fallos de `r03_03`: sí, son por construcción.**
- `test_fp_lectura_del_conjunto[analizador_declara_r22]`, `[analizador_degradacion_ps5]` y
  `test_fp_sintetizador_v6_repite_la_instruccion_del_ejecutor` siembran la raíz también en la reescritura (el monkeypatch no mira
  `reescritura`). Es un modelo que desobedece dos veces, y bloquear es lo pedido en H-28. Con la siembra solo en la primera
  respuesta, el ciclo entrega (lo prueban `test_h28_*` del ticket; lo comprobé con `r04_01`).
- `test_fp_informe_de_clase[fondos_ejemplo_del_prompt]` y `[catalizador_de_la_tesis]` están dentro de una opción, donde no hay
  reescritura: es el límite declarado. Se valora en H-34.

**1. Las lagunas omitidas (`r04_01::test_laguna_*`).**
- Una laguna con la raíz no llega al Broker. Con «Validación pendiente de la batería mínima del perfil FX» (lo que pide el prompt de
  Divisas) o «No se pudo validar el dato de flujos: falta la serie de posicionamiento», el paquete dice solo «Renta variable:
  alcance reducido declarado (laguna del Analista omitida en el paquete por R22 …; consta en su informe de clase)».
- El informe de clase no se entrega al Broker. El paquete declara que hay una carencia, pero no cuál. Es justo la información
  que la laguna existe para dar («qué no se pudo comprobar»). Falla cerrado respecto a G3, pero abierto respecto a la honestidad
  del alcance. Ver H-35.

**2. El límite dentro de una opción, y lo que no se ha cubierto.**
- Fondos (`r04_01::test_limite_fondos_*`): con la frase del ejemplo del prompt en cada candidata, RV pasa de 3 opciones a 0. En un run
  real se perderían las opciones de Fondos cuyo Analista siga su propio ejemplo. La regla va ahora en la instrucción de CT-06, y eso
  lo hace menos probable, pero no hay segunda oportunidad.
- **El Contradictor no recibe la regla** (`r04_01::test_fp_contradictor_*`, `test_regla_en_la_refutacion`):
  - La refutación inicial de AG-11 (CT-13, esquema REFUTACION) usa una instrucción en línea en V5 (`Bloque._refutacion`, «Refuta de
    forma independiente cada tesis…») y `diseno_v6.INSTR_REFUTACION` en V6. Ninguna de las dos lleva `REGLA_R22_REDACCION`. Solo
    la llevan `INSTR` (CT-06, respuesta a objeciones y contrarréplica).
  - Su argumento va a `objeciones[].resumen` y su «qué la resolvería» a `que_cambiaria_la_conclusion`, los dos **dentro de la
    opción**.
  - La objeción más natural contra una señal cuantitativa es «falta una validación fuera de muestra». La pide el propio corpus:
    el prompt del Contradictor habla de «validez metodológica» y de la tendencia «validada», y el de Prospectiva dice «Validación
    fuera de muestra (Motor, MC-10)».
  - Medido: con «Una validación fuera de muestra del impulso» en la objeción moderada, **RV pasa de 3 opciones a 0**. Como el
    Contradictor revisa todos los tipos, un ciclo real puede quedarse sin ninguna opción.
  - Es el mismo patrón de H-28: un agente al que el corpus pide la raíz y que no recibe la regla. Aquí, además, sin reescritura.
    Ver H-33.

**5. Regresiones.** Ver la tabla: ciclos normales, cadena A→B, T-145, T-148, T-159 y T-165 en verde. Los textos del Motor y del
ejecutor sin la raíz lo prueban `test_h28_*` y R34/R35.

## Hallazgos de la r03

| ID | Estado en la r04 |
| --- | --- |
| H-28 | **Corregido fuera de una opción** (integración, Redactor y Sintetizador con regla y reescritura; simulado con la raíz; Motor y ejecutor sin ella; R24–R27 y R34 mueren). Dentro de una opción, sigue abierto por el Contradictor (H-33) y por el límite (H-34) |
| H-29 | Corregido (`test_h29_*`, R28; `r03_03::test_fp_ruta_de_salida_con_la_raiz` pasa) |
| H-30 | Corregido («válido» bloquea; «inválido» no; R30; `r03_03::test_escapa` pasa) |
| H-31 | Corregido (`test_h31_*`, R29; `r03_03::test_esquema_*` pasa) |
| H-32 | Corregido (`r03_02` M1–M3 bloquean; R31) |

## Hallazgos de la r04

| ID | Gravedad | Cómo reproducirlo | Esperado / obtenido | Corrección | Estado |
| --- | --- | --- | --- | --- | --- |
| H-33 | alta | `r04_01::test_fp_contradictor_objecion_fuera_de_muestra`, `::test_regla_en_la_refutacion` | **Esperado:** como en H-28, todo agente cuyo texto llega al entregable recibe la regla R22. **Obtenido:** la refutación de AG-11 (V5: instrucción en línea de `Bloque._refutacion`, `orquestacion.py`; V6: `diseno_v6.INSTR_REFUTACION`) no la lleva. Su argumento y su «qué la resolvería» van dentro de la opción. La objeción «falta una validación fuera de muestra», la que piden el corpus y el oficio, retira la opción: RV pasa de 3 a 0 | (1) Añadir `+ " " + ht09.REGLA_R22_REDACCION` a la instrucción de REFUTACION de V5 y a `INSTR_REFUTACION`, con una prueba como la de `test_h28_la_regla_r22_va_en_las_instrucciones…` que recorra **todas** las instrucciones cuyos textos van al paquete (CT-06, CT-12, CT-13 y sus respuestas, AG-02, AG-17, AG-26). (2) Reescritura de la respuesta de REFUTACION con `Bloque.reescribir_r22` (bolsa de la clase en V5, COMÚN en V6), igual que en H-34 | abierto |
| H-34 | media | `r03_03::test_fp_informe_de_clase[*]`; `r04_01::test_limite_fondos_*` | **Esperado:** el ejemplo de ficha del propio corpus (Fondos) y la pregunta de catalizadores de RF, Monetarios y Tipos («¿qué catalizador puede validar o invalidar la tesis?») no retiran opciones sin una segunda oportunidad. **Obtenido:** dentro de una opción no hay reescritura; con la frase de Fondos, 3 → 0. Está declarado, pero el remedio existe y es barato | Llamar a `r = self.reescribir_r22(r, agente, "CT-06", msg, <el mismo esquema>, instr, as_of, run_id, clase, "cribado", presupuesto, bolsa=clase)` tras el `_invocar` de CT-06 en `Bloque._analizar_clase` (y lo mismo tras REFUTACION, H-33). Sale de la misma clave de configuración y solo cuesta cuando aparece la raíz. Esto exige: añadir a `reescribir_r22` un parámetro `bolsa` (hoy fija COMÚN; aquí, la de la clase); sumar a `LLAMADAS_POR_TIPO` de `estimar_coste_ciclo_a.py` las dos filas («reescritura_r22_cribado», «reescritura_r22_refutacion», máximo `redaccion.reescrituras_r22`); y añadir una prueba con la frase de Fondos solo en la primera respuesta, en la que el ciclo entregue sin perder opciones. La respuesta reescrita vuelve a pasar F6. Si el operador prefiere no pagarlo, que el límite pase a la deuda con este ID | abierto |
| H-35 | media | `r04_01::test_laguna_con_la_raiz_llega_al_broker[*]` | **Esperado:** el Broker sabe qué no se pudo comprobar. **Obtenido:** la laguna se sustituye por «laguna del Analista omitida en el paquete por R22 (… consta en su informe de clase)», y el informe de clase no se entrega. Se pierde la carencia concreta («falta la serie de posicionamiento», «la batería mínima del perfil FX») | Neutralizar la palabra en lugar de omitir la laguna. En `sintesis._laguna_r22`, primero `t = _RE_VALID_CRUDO.sub("comprobar", texto)`, con `_RE_VALID_CRUDO = re.compile(r"(?i)(?<![a-záéíóúüñàèìòùâêîôûç])(?:re\|con\|pre)?v[aá]lid[a-záéíóúüñàèìòùâêîôûç]*")`, y devolver `f"{t} (redacción ajustada por R22)"` si `not ht09.tiene_raiz_valid(t)`. Solo si persiste (homoglifos, caracteres de formato), el texto actual de omisión. La sustitución no declara madurez: «comprobar» está fuera de la raíz, como el sinónimo que el modelo podría escribir. Con H-34, las lagunas también salen reescritas por el Analista, y esto queda de respaldo. Prueba: las dos lagunas de `r04_01` llegan con «batería mínima» y «posicionamiento» y G3 OK | abierto |
| H-36 | baja | `r04_01::test_reescritura_instruccion_de_la_integracion` | **Esperado:** la reescritura repite la instrucción, como la del Redactor y la del Sintetizador. **Obtenido:** a la de AG-02 llega «Integra los informes de clase. » + la regla, sin los campos pedidos ni «No cambies la selección: la ha hecho HT-03» | En `_integrar`, `instr = ("Integra los informes de clase: régimen macro común, … No cambies la selección: la ha hecho HT-03. " + ht09.REGLA_R22_REDACCION)`, usada en el `_invocar` y en `reescribir_r22(r, "AG-02", "CT-05", msg, "INTEGRACION", instr, …)`. Ajustar el filtro `"Integra" in x[2]` de las pruebas si hace falta | abierto |
| H-37 | baja | lectura de `Bloque.reescribir_r22` | **Esperado:** como en la de legibilidad, la reescritura dice al agente qué corregir. **Obtenido:** `msg2 = {**msg, "reescritura": {"r22": REGLA}}`: ni el texto anterior ni dónde estaba la raíz; regenera a ciegas y paga la llamada entera | `msg2 = {**msg, "reescritura": {"r22": ht09.REGLA_R22_REDACCION, "frases": ht09.frases_con_raiz(r.datos)}}`, con `frases_con_raiz` como `tiene_raiz_valid` pero devolviendo hasta 10 extractos `(ruta, texto[:200])`. Prueba: el mensaje de la reescritura lleva el extracto sembrado | abierto |

### Bajos que hay que subsanar en este ticket

H-36 y H-37, con su corrección y su prueba.

## Decisiones `[PROPUESTO]` de la r04

| Decisión | Valoración del revisor |
| --- | --- |
| `redaccion.reescrituras_r22: 1` | De acuerdo: un número de configuración, con su origen (el paralelismo con PB-39) y probado con 0 y con 2 |
| La reescritura se decide por la raíz en cualquier texto de la respuesta, no por la regla A | De acuerdo: solo puede añadir una llamada, nunca quitar control |
| Lagunas con la raíz omitidas | En desacuerdo como solución final: H-35 |
| Dentro de una opción, sin reescritura | En desacuerdo: H-34. Con H-33, lo que cae dentro de una opción no es una excepción, sino la objeción típica |
| El simulado escribe la raíz en la integración | De acuerdo: ejerce la reescritura en cada ciclo V5 |

## Veredicto

**NO APTO.** La r04 corrige H-28 fuera de una opción y cierra H-29 a H-32:
- la regla va en las instrucciones de los que redactan fuera de las opciones;
- la reescritura vuelve a pasar G3-MET-13, sale de la configuración y falla cerrado;
- el ejecutor y el Motor ya no escriben la raíz;
- los ciclos normales y la cadena A→B no cambian, salvo la llamada de la reescritura;
- los 12 mutantes nuevos mueren;
- las cuotas se mantienen.

Pero queda abierto un alto, H-33. El Contradictor no recibe la regla, y su objeción natural («falta una validación fuera de
muestra»), dentro de la opción, la retira sin reescritura. En el simulado, RV se queda sin opciones. Es la misma clase de fallo que
H-28, ahora en la otra mitad del ámbito. A eso se suman H-34 (Fondos y catalizadores, sin segunda oportunidad) y H-35 (la laguna
que no llega al Broker), medios.

Vuelve a `ri-implementar`. En la r05 volveré a ejecutar `r04_01` (el test de Fondos pasa a esperar que no se pierdan opciones si
H-34 se corrige), `r03_03` y los ciclos normales. No he cerrado el ticket ni tocado la deuda técnica.

---

# Ronda r05

- **Revisor:** el mismo subagente de Claude de la r04, sin haber implementado nada · 17-11-2026
- **Copia revisada:** worktree desechable `qa165r05` en `fc9c65d` (`wip/t165r05`, rebasada sobre develop `d72526c`, con T-162 y
  T-169), con el venv del proyecto. Sin red ni gasto. Ciclos en una carpeta nueva (`qa165r05_ciclos`).
- **Foco pedido por el coordinador:** comprobar H-33 a H-37; ver si el simulado obediente (`mock_respuestas._obedece_r22`) debilita
  alguna prueba; los dos fallos de `r04_01`; repetir `r04_01`, `r03_03`, los ciclos normales y la cadena A→B.

## Reproducción

```bash
cd bloque_a/11_Ejecutor
../../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_t165_g3_met13.py tests/test_t159_extremo_a_extremo.py tests/test_t145.py tests/test_t148.py
../../.venv/bin/python -m pytest -q -p no:cacheprovider -s ../../.docs/tickets/T-165/revisores/r04_01_reescritura_y_limites.py -rf
../../.venv/bin/python -m pytest -q -p no:cacheprovider -s ../../.docs/tickets/T-165/revisores/r05_01_reescritura_dentro_de_la_opcion.py -rf
../../.venv/bin/python -m pytest -q -p no:cacheprovider -s ../../.docs/tickets/T-165/revisores/r03_03_extremo_a_extremo.py -rf
../../.venv/bin/python ../../.docs/tickets/T-165/revisores/r01_03_ciclos_normales.py --salida <scratch>/qa165r05_ciclos   # y diff con ciclos_r04
cd ../.. && .venv/bin/python .docs/scripts/cadena_a_b.py --trabajo <scratch>/qa165r05_cadena
```

| Comprobación | Resultado |
| --- | --- |
| T-165 + T-159 + T-145 + T-148 | **213 superadas** |
| `r04_01` | 10 de 12. Los dos fallos son de expectativa, como dice el implementador: `test_limite_fondos…` esperaba la retirada que H-34 corrige (ahora 3 → 3), y `test_reescritura_sigue_la_configuracion[2]` siembra sin desactivar la obediencia, así que el simulado obedece la primera reescritura. Con un modelo que no obedece, el caso equivalente pasa (`test_la_reescritura_sigue_la_configuracion_con_un_modelo_que_no_obedece`, 1 + n llamadas). Contradictor: 3 → 3, con la regla en las tres instrucciones de REFUTACION. Lagunas: llegan con su carencia. AG-02 reescrito con la instrucción completa |
| `r03_03` | 9 de 9. Los tres casos «la raíz persiste» de la r03 pasan ahora porque el simulado obedece la reescritura: miden la reescritura, no G3 (ver «El simulado obediente») |
| Ciclos normales (10) | Mismos dictámenes, opciones y llamadas que en la r04 (diff vacío de las líneas RUN-). G3-MET-13 OK en los 20 G3V-. Solo cambian los tokens de entrada (instrucciones más largas, p. ej. +852 en `v5_12tipos_2026`) |
| Cadena A→B | rc 0: 1 entrega del Bloque B, válida, y la vuelta registrada |

No repetí la suite completa ni los mutantes (43 de 43, según el implementador).

## Hallazgos de la r04

| ID | Estado en la r05 |
| --- | --- |
| H-33 | **Corregido.** Regla en REFUTACION V5 y V6 y reescritura en la bolsa del tipo o la global. `r04_01::test_fp_contradictor_*`: 3 → 3; con un modelo que no obedece, la reescritura se pide y la raíz que persiste retira la opción (`r05_01::test_debil_contradictor_*`). Pero la prueba que «recorre todas las instrucciones» no cubre dos que sí llegan a la opción: ver H-40 |
| H-34 | **Corregido para CT-06** (`INFORME_CLASE` y `REVISION_VIGENTES`): Fondos 3 → 3. El estimador lleva las dos filas. Pero dispara de más: ver H-38 |
| H-35 | Corregido: la laguna llega con «comprobar» y la marca, y solo se omite si la raíz persiste (lo prueba el implementador sin obediencia). En los ciclos simulados, la laguna ya llega reescrita por el Analista (H-34) |
| H-36 | Corregido: la reescritura de AG-02 lleva la instrucción completa |
| H-37 | Corregido: `frases_con_raiz` y `redaccion.frases_r22_max: 10` `[PROPUESTO]`, en la configuración |

## El simulado obediente

Es razonable que obedezca por defecto: un simulado que nunca obedece no ejercería el camino feliz de la reescritura. Las pruebas
de «persiste» del ticket lo desactivan (6 pruebas, incluida PB-47 con ML-CLUS-001 en DOCUMENTADO), y mi control `r05_01::test_debil_*`
confirma que, sin obediencia, la raíz que persiste dentro de una opción sigue retirándola. No he encontrado ninguna prueba del ticket
que se haya vuelto vacía.

Efecto que conviene saber: los scripts de los revisores que siembran con monkeypatch sobre las funciones del simulado (`r01_02`,
`r02_02`, `r03_03`) pasan ahora por la reescritura, no por G3. Dejan de medir el bloqueo de G3-MET-13 y miden que la palabra no llega.
No es un hallazgo. A partir de ahora, quien siembre para probar un bloqueo debe desactivar `_obedece_r22`.

Lo que sí ha destapado el simulado obediente son los hallazgos H-38 y H-39: el implementador tuvo que desactivar la obediencia en
`test_lo_que_el_modelo_dijo_de_la_madurez_queda_en_ha` («sin la reescritura de H-34 obedecida») porque, con ella, la reescritura de
CT-06 se dispara por `estado_madurez_metodos`.

## Hallazgos de la r05

| ID | Gravedad | Cómo reproducirlo | Esperado / obtenido | Corrección | Estado |
| --- | --- | --- | --- | --- | --- |
| H-40 | alta | `r05_01::test_fp_prospectiva_declara_r22`, `::test_fp_respuesta_a_objeciones` | **Esperado:** como pide H-33, todo agente cuyo texto va dentro de la opción tiene la regla **y** la reescritura. **Obtenido:** Prospectiva (CT-12, V5 `Bloque._prospectiva` y V6 `prospectiva_global`) y la respuesta a objeciones (CT-06 `RESPUESTA_OBJECIONES`, V5 en `Bloque._refutacion` y V6 en `refutacion_global`) llevan la regla, pero no tienen reescritura. El prompt de Prospectiva (corpus) pide en su R22 «Declaras el estado de madurez de cada método (documentado, implementado, validado)». Con esa declaración en el escenario base, **RV pasa de 3 opciones a 0**. Como Prospectiva y las respuestas cubren todas las opciones de todos los tipos, un ciclo real puede quedarse sin opciones. Con «El impulso se ha validado con los datos de HT-01» en la respuesta a una objeción, también 3 → 0. El simulado obedece, pero no hay a qué obedecer: nadie pide la reescritura | (1) V5, `orquestacion.py`: guardar la instrucción de CT-12 en `instr` y, tras su `_invocar`, `r = self.reescribir_r22(r, "AG-10", "CT-12", msg, "PROSPECTIVA", instr, as_of, run_id, clase, "prospectiva", presupuesto, bolsa=clase)`. Tras el `_invocar` de `RESPUESTA_OBJECIONES`, `r2 = self.reescribir_r22(r2, agente, "CT-06", msg2, "RESPUESTA_OBJECIONES", INSTR["RESPUESTA_OBJECIONES"], as_of, run_id, clase, "respuesta_objeciones", presupuesto, bolsa=clase)`. (2) V6, `diseno_v6.py`: lo mismo tras el CT-12 de `prospectiva_global` (con `INSTR_PROSPECTIVA`, clase `None`, `bolsa=BOLSA_GLOBAL`) y tras el `RESPUESTA_OBJECIONES` (con `bolsa=clase`). (3) `estimar_coste_ciclo_a.py`: añadir a `LLAMADAS_POR_TIPO` las filas `reescritura_r22_prospectiva` (AG-10) y `reescritura_r22_respuesta` (ANALISTA), con máximo `redaccion.reescrituras_r22`, y ajustar los recuentos de `test_t145`/`test_t148`. (4) Comprobar también la CONTRARREPLICA: si su `motivo` llega a la opción, lo mismo. (5) Una prueba V5 y V6 que siembre la raíz en la primera respuesta de **cada** agente cuyo texto llega al paquete (AG-02, AG-10, AG-11, Analistas en sus tres esquemas, AG-17, AG-26), con el simulado obediente, y exija que el ciclo entregue sin perder opciones: cierra la familia en lugar de agente a agente | abierto |
| H-38 | media | `r05_01::test_coste_estado_madurez_no_dispara_la_reescritura_del_informe` | **Esperado:** no se reescribe el informe de clase por un campo que el ejecutor sobrescribe. **Obtenido:** los prompts de los Analistas piden declarar en `estado_madurez_metodos` «documentado, implementado o validado» (RV: «no la presentas como validada»). `canonizar_madurez` lo sobrescribe, pero `reescribir_r22` lo mira antes: RV y RF reescriben su informe (CT-06, la llamada más cara del ciclo; 12 000 tokens de salida en la cota). Con la API real, casi todos los tipos lo harían en cada ciclo. Eso duplica el CT-06 y puede agotar la bolsa del tipo, que se cierra con alcance reducido (R16) | En `Bloque.reescribir_r22`, mirar la respuesta sin los campos de madurez: `datos = sint._sin_madurez(r.datos)`, la condición con `ht09.tiene_raiz_valid(datos)` y `frases = ht09.frases_con_raiz(datos, …)`. La prueba de `r05_01` como regresión. Quitar el `_obedece_r22` desactivado de `test_lo_que_el_modelo_dijo_de_la_madurez_queda_en_ha`, que debe pasar con el simulado obediente | abierto |
| H-39 | baja | `r05_01::test_traza_madurez_falsa_reescrita_queda_en_ha` | **Esperado:** R22 dice que presentar como validado lo que no lo está es un hallazgo; la r04 ya deja en HA lo que el ejecutor descarta de `estado_madurez_metodos`. **Obtenido:** «ST-DESC-001 está validado en backtest» (ficha IMPLEMENTADO) se reescribe y desaparece sin rastro. Además, la regla sugiere «comprobar», así que un modelo obediente escribe «comprobado en backtest», el sinónimo que el límite declarado deja pasar | (1) En `reescribir_r22`, antes de `_invocar`: `self.almacen.incidencia("OTRO", f"G3-MET-13 (R22): respuesta de {agente} ({esquema}) reescrita por la raíz «valid-»", objeto=run_id, severidad="Operativa", frases_r22=[{"ruta": a, "texto": t} for a, t in frases])`. (2) En `ht09.REGLA_R22_REDACCION`, añadir: «Tampoco califiques con otra palabra la madurez o la fiabilidad de un método (comprobado, probado, fiable): la escribe el ejecutor.». Prueba: el INC con la frase sembrada, y la regla con la frase nueva (ajustar `test_h28_la_regla_r22…` si compara el texto) | abierto |

## Decisiones `[PROPUESTO]` de la r05

| Decisión | Valoración del revisor |
| --- | --- |
| `redaccion.frases_r22_max: 10` | De acuerdo: un número de configuración, paralelo a `frases_largas[:10]` |
| El simulado obedece la reescritura | De acuerdo, con la condición de arriba (desactivarlo para probar un bloqueo) |
| Reescritura de CT-06 y CT-13 en la bolsa del tipo (V6, la global) | De acuerdo |

## Veredicto

**NO APTO.** La r05 corrige H-33 a H-37:
- el Contradictor tiene la regla y la reescritura;
- Fondos ya no pierde opciones;
- la laguna llega con su carencia;
- la reescritura lleva la instrucción completa y las frases;
- los ciclos normales y la cadena A→B no cambian.

Pero la corrección se ha hecho agente a agente, y quedan dos agentes cuyo texto llega a la opción sin reescritura: Prospectiva,
cuyo prompt del corpus pide la declaración R22 con «validado», y la respuesta a objeciones. Los dos dejan un tipo sin opciones
(H-40, alto). Además, la reescritura de CT-06 se dispara por el campo de madurez que el ejecutor sobrescribe (H-38, medio) y no deja
rastro del hallazgo R22 (H-39, bajo).

Vuelve a `ri-implementar`. En la r06 volveré a ejecutar `r05_01`, `r04_01` y los ciclos normales. Conviene que la prueba de (5) de
H-40 cubra la familia entera, para no abrir otra ronda por un agente más. No he cerrado el ticket ni tocado la deuda técnica.

---

# Ronda r06

- **Revisor:** el mismo subagente de Claude de la r04 y la r05, sin haber implementado nada · 17-11-2026
- **Copia revisada:** worktree desechable `qa165r06` en `4224109` (`wip/t165r06`, rebasada sobre develop `a9210c0`), con el venv del
  proyecto. Sin red ni gasto. Ciclos en una carpeta nueva (`qa165r06_ciclos`).
- **Foco pedido por el coordinador:** (1) que los agentes excluidos no dejen texto libre en el paquete ni en los entregables; (2) que
  la reescritura no entre en bucle y su coste tenga cota; (3) R8 en `frases_r22`; (4) regresiones.

## Reproducción

```bash
cd bloque_a/11_Ejecutor
../../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_t165_g3_met13.py tests/test_t159_extremo_a_extremo.py tests/test_t145.py tests/test_t148.py
for f in r06_01_agentes_excluidos_y_bucle r05_01_reescritura_dentro_de_la_opcion r04_01_reescritura_y_limites r03_03_extremo_a_extremo; do
  ../../.venv/bin/python -m pytest -q -p no:cacheprovider -s ../../.docs/tickets/T-165/revisores/$f.py -rf; done
../../.venv/bin/python ../../.docs/tickets/T-165/revisores/r01_03_ciclos_normales.py --salida <scratch>/qa165r06_ciclos   # y diff con qa165r05_ciclos
cd ../.. && .venv/bin/python .docs/scripts/cadena_a_b.py --trabajo <scratch>/qa165r06_cadena
```

| Comprobación | Resultado |
| --- | --- |
| T-165 + T-159 + T-145 + T-148 | **219 superadas** |
| `r06_01` (nuevo) | 9 de 9 (ver abajo) |
| `r05_01` | **6 de 6**: H-38 (CT-06 ya no se reescribe por `estado_madurez_metodos`), H-39 (la madurez falsa reescrita queda en HA), H-40 (Prospectiva y respuesta a objeciones: 3 → 3) y los dos controles sin obediencia |
| `r04_01` | 10 de 12. Los mismos dos fallos de expectativa de la r05 (Fondos ya no se retira; `[2]` siembra sin desactivar la obediencia) |
| `r03_03` | 9 de 9 |
| Ciclos normales (10) | Mismos dictámenes, opciones y llamadas que en la r05 (diff vacío de las líneas RUN-). JSON idénticos. En los técnicos solo cambian los tokens de entrada, por la regla R22, que es más larga. G3-MET-13 OK en los 20 G3V- |
| Cadena A→B | rc 0: 1 entrega del Bloque B, válida, y la vuelta registrada |

No repetí la suite completa ni los mutantes (46 de 46, según el implementador).

## Lo que ha mirado esta ronda

**1. Los agentes excluidos (`ht09.AGENTES_SIN_TEXTO_ENTREGADO`).**
- Dinámica (`r06_01::test_excluido_*`): marqué todo texto libre de las respuestas simuladas de los nueve, en V5 y en V6:
  - con un marcador propio, que no llega a ningún entregable ni al paquete;
  - con la raíz, que no retira ninguna opción (6 → 6 y 3 → 3) ni bloquea.
- Rastreo en el código, campo a campo:
  - **AG-14, AG-15, AG-16 y AG-28** (búsqueda): `afirmacion`, `extracto`, `sintesis` y `lagunas` van a `_piezas` y de ahí a F2.
    La opción solo lleva los identificadores CLM- (`evidencias`), y el técnico imprime esos identificadores. En V6, la afirmación
    llega al Contradictor como entrada; él sí pasa por la reescritura.
  - **AG-12** (curación): solo categorías (`tipo_afirmacion`, `nivel_confianza`, `alertas`) que van a F2.
  - **AG-13**: escribe en RC.
  - **AG-18**: `dictamen` y `motivo` van a G3V- en HA.
  - **AG-19**: hallazgos y `resumen` van a HA y AUD-.
  - **AG-20**: lecciones a F6 y su `resumen` a CT-19 hacia AG-02. AG-02 sí se reescribe, y el técnico no imprime lecciones.
- No encuentro ningún campo de estos agentes que llegue a un entregable. La exclusión es correcta y es una lista de exclusión: un
  agente nuevo queda cubierto por defecto. Bien.

**2. El bucle y la cota (`r06_01::test_bucle_*`).** Con un modelo que nunca obedece y la raíz en toda respuesta de los agentes
cubiertos:
- cada llamada original se repite exactamente `n` veces (n = 1 y n = 2, en V5 y V6);
- ninguna reescritura se reescribe: el envoltorio de `_invocar` no actúa sobre un mensaje con `reescritura.r22`;
- ningún agente excluido se reescribe;
- hay una incidencia OTRO por reescritura.

La reescritura de legibilidad (C12) también queda cubierta y conserva su `reescritura` previa. La cota del estimador se deriva de la
misma constante y de la clave de configuración: T-145 y T-148 en verde.

**3. R8 en `frases_r22` (`r06_01::test_incidencia_*`).**
- Solo lleva texto de la **respuesta** del agente (sin los campos de madurez): hasta `redaccion.frases_r22_max` frases de hasta 200
  caracteres. No lleva el mensaje ni el contexto.
- Ese texto ya se guarda, igual o en más extensión, en la mensajería y en los entregables. Los agentes no reciben datos personales
  ni credenciales (R8 y CT-25), y en backtest con un modelo real el mensaje sale anonimizado.
- La incidencia no añade ninguna exposición. Sin hallazgo.

**4. Regresiones.** Ver la tabla.

**Observación sin gravedad, para la deuda si el coordinador lo ve oportuno.** Una reescritura que no cabe en la bolsa sigue el
camino normal de `_invocar_una`. En el peor caso declara un cierre parcial por presupuesto de esa fase, aunque la primera respuesta
exista; después G3-MET-13 bloquea si la raíz persiste. Falla cerrado y lo declara (R16), pero el cierre lo provoca una llamada
opcional. No lo he reproducido. Si se quiere evitarlo: en `reescribir_r22`, no pedir la reescritura cuando
`presupuesto.puede(bolsa, …)` no cubre el peor caso de la llamada.

## Hallazgos de la r05

| ID | Estado en la r06 |
| --- | --- |
| H-40 | **Corregido** de forma estructural: un único punto en `Bloque._invocar`, con lista de exclusión. `r05_01::test_fp_prospectiva_*` y `::test_fp_respuesta_a_objeciones`: 3 → 3. La CONTRARREPLICA también se reescribe (`r06_01`) |
| H-38 | Corregido: `r05_01::test_coste_*` pasa (no hay reescritura del informe de clase por `estado_madurez_metodos`) |
| H-39 | Corregido: `r05_01::test_traza_*` pasa (INC OTRO con `frases_r22`), y la regla prohíbe calificar la madurez con otras palabras |

## Hallazgos de la r06

Ninguno.

## Veredicto

**APTO.** Todos los hallazgos de las rondas r01 a r05 están corregidos o declarados como límite `[PROPUESTO]` en INC-T165-01. Los
límites declarados son los sinónimos sin la raíz, que van con la forma canónica al lado, y el falso positivo de la raíz cuando
persiste tras la reescritura. No queda ningún hallazgo crítico, alto, medio ni bajo abierto.
- G3-MET-13 bloquea la madurez falsa con la raíz por cualquier vía.
- La reescritura R22 cubre a todo agente cuyo texto llega al entregable, está acotada por la configuración, no entra en bucle y
  deja rastro en HA.
- Los ciclos normales y la cadena A→B no cambian, salvo las llamadas de la reescritura.

El cierre del ticket lo hace la sesión coordinadora (fila de deuda, diario, memoria, commit en `develop` y push): por indicación
suya, aquí solo hay commit local. Si se quiere, puede llevar a la deuda la observación sobre el cierre parcial por presupuesto.

---

# Ronda de cierre

- **Revisor:** el mismo subagente de Claude de las rondas r04 a r06 · 17-11-2026
- **Copia revisada:** worktree desechable `qa165cierre` en `657fc01` (`wip/t165cierre`, sobre `4224109`), con el venv del proyecto.
- **Objeto:** la observación sin gravedad de la r06: una reescritura que no cabía en la bolsa podía declarar un cierre parcial
  por presupuesto aunque la respuesta existiera.

## La corrección

En `Bloque.reescribir_r22`, antes de pedir la reescritura, se calcula su peor caso:
- `ResultadoAgente.peor_caso_uc`: lo que reservó la llamada original, que rellena `_invocar_una` (`ReservaLlamada.peor_total`, o
  `max_uc_estimado`);
- más la UC de los tokens de entrada de las frases (`tokens_de_peticion`).

Si `presupuesto.puede(bolsa or clase or "COMUN", peor)` es falso, no se pide la reescritura. Se queda la respuesta, G3-MET-13
decide y HA recibe una incidencia OTRO («… sin reescribir: su peor caso (x UC) no cabe en la bolsa B; decide G3-MET-13», con
`frases_r22`). La bolsa es la misma regla que usa `_invocar_una`.

La comprobación es prudente: no cuenta la ampliación, así que en el límite se puede dejar de pedir una reescritura que una
ampliación habría permitido. Y si la reescritura cabe pero luego necesita reparaciones o continuaciones, cada una sigue reservando
por su cuenta. Las dos cosas fallan cerradas, y la observación era sin gravedad: no lo considero hallazgo.

## Comprobaciones

| Comprobación | Resultado |
| --- | --- |
| `test_t165_g3_met13.py -k "cierre_r06 or h28 or h40 or bolsa"` | 12 superadas: con la bolsa justa, ni reescritura, ni cierre parcial, ni pérdida de la respuesta, e incidencia en HA; con bolsa de sobra, reescritura |
| Mutante R47 (`if False:` en lugar de la comprobación), aplicado por mí en una exportación | **muerto**: `test_cierre_r06…` falla |
| `r06_01` | 9 de 9 |
| `r05_01` | 6 de 6 |
| Ciclos normales (10, carpeta nueva `qa165cierre_ciclos`) | **idénticos** a los de la r06 (dictámenes, opciones, llamadas, técnicos y JSON, salvo las rutas de trabajo); G3-MET-13 OK en los 20 G3V- |

## Veredicto final

**APTO.** Observación de la r06 corregida, con su prueba y su mutante. No queda ningún hallazgo abierto en el ticket. Estado del
README: CERRADO; fila T-165 de la deuda: CERRADO. El diario, la memoria, el commit en `develop` y el push los hace la sesión
coordinadora.
