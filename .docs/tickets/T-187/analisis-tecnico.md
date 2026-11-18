# T-187 · Análisis técnico

## Motivo

PB-51 está «diseñada» en el plan V3.0 y nadie la había ejecutado. Es una verificación documental de 35 prompts de 10 000 a 18 000 palabras: hacerla a mano no es reproducible ni cabe en un kit de contexto (regla 1). El script lee los prompts como datos y deja el resultado en archivos.

## Lo que había en el corpus

- **Anexo G.** Está en el Documento 0 vigente (`bloque_a/01_Gobernanza/Documento 0 - Protocolo maestro del Bloque A - Versión óptima V5.3.md`, «## ANEXO G. ESTRUCTURA COMÚN DE LOS SYSTEM PROMPTS (V4.0–V5.1)», 12 puntos) y en las V5.1 y V5.2 de `99_Historico_*`. Una búsqueda que solo mire «Anexo G» con esa grafía no lo encuentra: el título va en mayúsculas. El script lo lee del Documento 0 (no copia los títulos).
- **Orientaciones de tamaño.** No están escritas para los prompts V5.0. Se buscó en el Documento 0 (V5.3 e históricos V3.0, V5.1, V5.2), en `08_Arquitectura`, en los README del bloque y del ejecutor, en el plan y en `99_Historico_*`. Solo hay la estimación «≈ 20.000 tokens» del README del ejecutor y `v6.tope_tokens_system` de la configuración (idea 7 de `.docs/diseno/bloque_a/decision_claude_c01.md`, `[PROPUESTO]`, vigilada por `tests/test_t101_v6.py` del ejecutor). Criterio propuesto en INC-T187-01.

## Implementación

### Archivos

| Archivo | Qué es |
| --- | --- |
| `.docs/scripts/revision_prompts_pb51.py` | El script (sin red, determinista; Python del `.venv`, usa `yaml` y el paquete del ejecutor). Escribe en este ticket (`--salida` por defecto). Estaba en el ticket hasta la r02 (QA r01, H-06) |
| `.docs/scripts/pruebas_revision_prompts_pb51.py` | 103 pruebas sintéticas y dos de regresión sobre el corpus real (lo generado y los veredictos guardados); las recoge `.docs/scripts/pruebas_scripts.sh` (antes `test_revision_prompts.py` en el ticket) |
| `.docs/scripts/mutantes_revision_prompts_pb51.py` | 78 mutantes del script (M42 a M63 del paso 3, M64 a M78 de la r02); todos tienen que morir (antes `mutantes_pb51.py` en el ticket) |
| `informe_pb51.md` | Generado: tablas de los pasos 1 y 2, referencias, tamaños y muestra |
| `muestra_afirmaciones.json` | Generado: las 350 afirmaciones del paso 3, con `veredicto`, `nota` y `revisor` vacíos (no se rellenan: los veredictos van aparte) |
| `veredictos/lote_1.json` … `lote_4.json` | Entrada: los veredictos de los cuatro revisores independientes (`revisor` y la lista `veredictos` con `id`, `veredicto` y `nota`) |
| `veredictos/comentario.json` | Entrada: el comentario del contraste, escrito a partir de las notas: error, corrección y `cita_nota` de cada ERRONEA; matiz de cada caso dudoso (`dudosas`) y su cita (`dudosas_cita_nota`); `criterio_dudosas`; `discutibles` (las que un revisor llama así en su nota: hoy ninguna); `sensibilidad` (casos y motivo, de quien escribe el comentario) |

Fuera del ticket cambian `docs/incidencias.md` (INC-T187-01 a 03), la fila T-187 de la deuda técnica, la fila PB-51 de `bloque_a/11_Ejecutor/tests/mapa_plan_pruebas.json`, `docs/evidencias_pruebas_bloque_a.md` (regenerado) y una prueba nueva del ejecutor, `bloque_a/11_Ejecutor/tests/test_t187_pb51.py`. Ningún `.py` del paquete.

### Criterios (todos en constantes del script)

- **Sección.** Un título `## N. Título` fuera de un bloque de código; acaba en el siguiente título de nivel 1 o 2. **Estructura completa:** las N del Anexo G presentes, cada una una vez y en orden, sin otras numeradas. **Título coherente:** comparte con el del Anexo G al menos una palabra (sin las vacías ni lo que va entre paréntesis), comparada por sus 6 primeras letras y sin mayúsculas. Si no, es «variante»: se informa y no suspende.
- **Plantilla.** Un archivo que no empieza por «System prompt - »: se informa, fuera del denominador y de la muestra.
- **Subárea.** `### 10.x` (o `#### 10.x.y`, que se suma a su 10.x; «10.x bis» es otra subárea). Lo que va antes de la primera es «10.0».
- **Elemento.** Cada viñeta con sus líneas de continuación, cada párrafo, cada fila de tabla (sin la de separación) y cada bloque de código. El texto es copia exacta de las líneas, sin la viñeta.
- **Definición operativa.** Elemento que empieza por un término en negrita, con un paréntesis opcional, seguido de «:», «=», «≈» o raya.
- **Fórmula.** Cada tramo de código con un operador entre dos operandos (=, ≈, ≤, ≥, <, >, ×, ·, /, +, −, ^, ÷, *) o un símbolo de cálculo (√, Σ, ∫, ∂, ∏, ln(, exp(, log(, max(, min(, Var(, Cov(, E[), salvo que sea una ruta o una dirección web; más cada «=» o «≈» con espacios fuera del código.
- **Umbral.** Cada comparador (≥, ≤, >=, <=, <, >) seguido de una cifra, y cada comparador en palabras («al menos», «como mínimo», «como máximo», «más de», «menos de», «por encima de», «por debajo de», «superior a», «inferior a», «mayor que», «menor que») seguido de una cifra. Un rango («entre 3 y 5») no cuenta.
- **Trampa.** Todo elemento de una subárea cuyo título dice trampa, error o sesgo, y todo elemento que nombra «trampa» o «error frecuente/típico/común».
- **Referencia.** Cada cita autor-año del elemento: «Autor (1996, «T»)», «Autor (1996). «T»», «(Autor, 1996, «T»; Otro, 1964)» y «Autor, «T», …, 1994». Autor: apellido con mayúscula, partículas solo dentro del apellido («López de Prado»), varios unidos por «,», «y», «e», «and», «&», y «et al.»; se descartan «Anexo», «Tabla», «Sección»… En las subáreas de referencias canónicas («Referencias canónicas», «Referencias académicas canónicas», «Literatura de referencia», «Bibliografía») cuenta cada entrada (separadas por « · » o «;» fuera de paréntesis y comillas; en una tabla, cada celda), y solo las que llevan un año o un título: lo demás son instrucciones.
- **Inventario de competencias.** Se lista y no se cuenta (resume lo anterior).
- **Referencia completa.** Entrada que empieza por un autor (apellido o institución, con iniciales admitidas) y lleva año y título («…», *cursiva* o comillas). Una entrada «(1983). «T»» tras otra hereda sus autores. Estricto: título en la entrada. Amplio `[PROPUESTO]`: otra cita del mismo primer autor y año en el prompt lo lleva.
- **DOI.** Candidato: «10.N/…» o «doi: x» con una cifra o una barra. Válido: «10.» + registrante de 4 a 9 cifras (con subdivisiones) + «/» + sufijo sin espacios. El DOI no tiene dígito de control; ISBN-10 (módulo 11), ISBN-13 (pesos 1 y 3, módulo 10) e ISSN (módulo 11) sí, y se valida. La existencia no se comprueba (sin red).
- **Tamaño.** Palabras (separadas por blancos), líneas, caracteres y tokens aproximados con `_tokens_aprox` del ejecutor. AG-10 y AG-11: el prompt íntegro contra su tope. Analistas de tipo de activo (`ANALISTAS_TIPO`): el prompt sin la §10 contra el tope «analista» (aproximación del núcleo y kit V6 con `base_conocimientos: ninguna`). El resto: sin orientación.
- **Afirmación candidata.** Cada frase de la §6 (sección de método, localizada en el Anexo G por «metodología») y de la §10 (por «conocimientos») con al menos una marca: fórmula, umbral, definición, cita o cifra con unidad (%, pp, pb, años, meses, días, veces, billones, millones, sesiones, semanas). No entran el inventario, las listas de referencias, las tablas ni los bloques de código. Frase: corte tras «.», «!» o «?» seguido de blanco y mayúscula, salvo tras una abreviatura («p. ej.», «et al.», «EE. UU.», «Mt.»…) o una inicial, o con un tramo de código, unas comillas, un paréntesis o una negrita abiertos. La frase es copia exacta del prompt (si no, lanza).
- **Muestra.** Aleatoria simple sin reemplazo de 10 candidatas por prompt (todas si hay menos), con `random.Random("<semilla>|<archivo>")`, en el orden del prompt. Cada una lleva `id` (`AF-<AG-xx o MC-xx>-NN`), prompt, agente, sección, subárea, línea, texto exacto, marcas, `referencia_citada` (citas de la frase) y `referencia_del_elemento` (las del elemento si la frase no cita). `veredicto` (CORRECTA, ERRONEA o NO_VERIFICABLE), `nota` y `revisor` quedan vacíos.

### Paso 3: contraste

- **Entradas.** Si existe `veredictos/` junto a la salida (o `--veredictos V`), el script lee `lote_*.json` (ordenados por número: `lote_2` antes que `lote_10`) y `comentario.json`. Sin la carpeta, el informe es el de antes (los repositorios sintéticos no la tienen).
- **Validación (falla cerrado, salida 2, sin escribir nada).** Cada id de la muestra, una vez y solo una entre todos los lotes (ni falta, ni sobra, ni se repite); veredicto en `VEREDICTOS` (los `veredictos_validos` de la muestra); nota no vacía y de `MAX_PALABRAS_NOTA` = 40 palabras como máximo (separadas por blancos; el encargo a los revisores); lotes con `revisor` y `veredictos`; comentario con `erratas` = exactamente las ERRONEA, cada una con `error` y `correccion`; `dudosas` solo CORRECTA; `discutibles` solo ERRONEA.
- **Recuentos.** Por lote, por prompt (en el orden de la muestra, con sus lotes) y totales. Porcentaje con los dos denominadores: verificables (CORRECTA + ERRONEA, el criterio de INC-T187-02) y todas. Supera si `100·CORRECTA ≥ UMBRAL_CORRECTAS·verificables` (95 de PB-51; en enteros, sin redondeo); sin verificables no supera. Sensibilidad: las discutibles como correctas y quitadas del denominador.
- **Informe.** Una fila más en el resumen y la sección «Paso 3 · Contraste de la muestra»: recuentos, por lote, por prompt, las ERRONEA (id, prompt y línea, frase, error, corrección), los casos dudosos y la sensibilidad. La muestra no cambia (`--comprobar` sigue comparándola).
- **Plan de pruebas (r01; en la r02, `PARCIAL`).** PB-51 pasa a `AUTOMATICA` con `tests/test_t187_pb51.py` del ejecutor: carga el script del ticket (como `test_fase4_mapa.py` carga `evidencias_plan_a.py`), exige que lo guardado coincida con lo generado (`--comprobar`), la estructura completa de los 35 prompts, la §10 por subáreas con fórmulas y referencias, ningún DOI inválido, el ≥ 95 % sobre las verificables y los 14 papeles con tope dentro. Si cambian los prompts o los veredictos, falla hasta que se repita la revisión.
- **Refactor.** La lectura de las entradas pasa de `principal` a `revisar(raiz, semilla, ejecutor)`, que lanza `EntradaFaltante` (`principal` la convierte en la salida 2), para que la prueba del ejecutor use la revisión sin escribir nada.

### Ronda r02 (QA r01 NO APTO: H-01 a H-07)

- **H-01.** PB-51 en el mapa: `PARCIAL` («Superada en parte»); «No comprueba» empieza por el resultado esperado incumplido (9 ERRONEA, INC-T187-03) y los 21 papeles sin orientación (INC-T187-01, T-57); «(10 por prompt)» sale de «Comprueba». Prueba nueva del ejecutor: `test_pb51_fila_del_mapa_superada_en_parte`. Evidencias regeneradas: 39 Superada y 20 Superada en parte.
- **H-02.** Columna «Verificables» por prompt y la lista de los que no llegan a `MUESTRA_POR_PROMPT` (28 de 35; mínimo 2, el Coordinador), en el informe, en INC-T187-02 y en «No comprueba». Sin muestra de reposición: se declara.
- **H-03.** `cita_nota` literal en cada errata y cada dudosa (si no es subcadena de la nota, salida 2). Los casos dudosos siguen un criterio escrito y comprobado: exactamente las CORRECTA cuya nota casa con `RE_MATIZ` («matiz», «exagera», «difieren», «ojo»). Con él entra AF-MC-02-04 y sale AF-AG-21-07 (su nota la confirma sin matiz). AF-MC-04-02 («los ajustes favorables son discutidos») no entra: el matiz es sobre la ley de Metcalfe, que el prompt ya rechaza, no sobre la frase. `discutibles` solo admite ERRONEA cuya nota diga «discutib» (hoy ninguna); la atribución a «los lotes 1 y 2» se quita del comentario, del informe y de INC-T187-02 y 03.
- **H-04.** `fuente()` clasifica cada nota (`FUENTES`, por orden: búsqueda web, que no sea «sin búsqueda web», o «Web:»; conocimiento propio; cálculo a mano; si no, sin fuente) y el informe da la tabla veredicto × fuente. CORRECTA: 3 web, 249 de memoria y 8 de cálculo. ERRONEA: 5 web, 2 de memoria, 1 de cálculo y 1 sin fuente.
- **H-05.** `_leer_json` convierte `JSONDecodeError`, `UnicodeDecodeError` y `OSError` en `ContrasteInvalido` (salida 2). `_texto` exige al menos una letra o cifra en la nota, el revisor, el matiz, el error, la corrección, la cita y el motivo. `discutibles` y los ids de la sensibilidad tienen que ser listas de `str`.
- **H-06.** El script, sus pruebas y sus mutantes pasan con `git mv` a `.docs/scripts/`; los datos se quedan en el ticket (`SALIDA_POR_DEFECTO`). Hay una fila nueva en `.docs/README.md`. La línea base de `.docs/scripts/linea_base_pruebas.txt` pasa de 231 a 336 (231 + 105). `test_t187_pb51.py` carga el script de `.docs/scripts/`.
- **H-07.** El título es «## Paso 3 · Muestra» y el texto remite a `veredictos/`. Las pruebas comprueban que el informe con contraste no dice «sin juzgar».
- **M01.** Revivió en la r02 (ninguna prueba aislaba el orden sin repetir ni sobrar). La prueba nueva `test_desordenada_sin_faltar_sobrar_ni_repetir_no_es_completa` lo mata. M54 y M55 quedaban tapados por las comprobaciones nuevas del criterio; ahora las pruebas exigen el mensaje exacto.

**Dónde me aparto de `qa.md`:**
- **Estructura de los dudosos.** `qa.md` pide una `cita_nota` dentro de cada dudosa. `r01_04` lee `dudosas` como `{id: texto}` (aplica `.lower()` al valor), así que `dudosas` sigue siendo `{id: matiz}` y la cita va en `dudosas_cita_nota` `{id: cita}`, con la misma comprobación.
- **Sensibilidad.** `qa.md` da a elegir entre quitarla y dejarla con su atribución verdadera. Se queda en una clave propia, `sensibilidad`, con el motivo de quien escribe el comentario. `discutibles` queda vacía porque ninguna nota lo dice: `r01_04` exige «discutib» en la nota de cada discutible.
- **Cifras por fuente.** `qa.md` da 251 CORRECTA de memoria y 5 con búsqueda; la clasificación declarada del script da 249 y 3, más 8 de cálculo a mano. Las cifras del informe, de INC-T187-02 y del mapa son las del script, que son reproducibles.
- **Rutas viejas.** `qa.md` y el diario del 18-11 citaban las rutas viejas del ticket, y `refs-vivas` fallaba. En la r02 las metí en `tools/refs_allowlist.txt`, pero esa lista es solo para entregables futuros (QA r02, H-08). En la ronda de cierre las quité: las citas se marcaron en el diario («entonces en la carpeta del ticket», con la ruta nueva al lado) y en `qa.md` (lo hizo el revisor), sin borrar nada. La allowlist queda como estaba.
- **`r01_03` sin modificar ya no encuentra el script**, porque lo carga de la carpeta del ticket (H-06 lo movió). Se ejecuta una copia en la carpeta temporal con solo la ruta cambiada (`sed 's#TICKET / "revision_prompts_pb51.py"#RAIZ / ".docs" / "scripts" / "revision_prompts_pb51.py"#; s#^TICKET = .*#TICKET = Path(sys.argv[1]).resolve()#'`, con la carpeta del ticket como argumento): 10 de 10. `r01_01`, `r01_02` y `r01_04` se ejecutan tal cual. El script del revisor no se toca.

### Ronda de cierre de la QA r02 (H-08 y H-09)

- **H-08.** Quité de `tools/refs_allowlist.txt` las cinco líneas de la r02 y ya no queda ninguna de T-187. La cita del diario del 18-11 queda marcada («revision_prompts_pb51.py, entonces en la carpeta del ticket (desde la r02, `.docs/scripts/revision_prompts_pb51.py`)»). La viñeta «Rutas viejas» de arriba lo explica.
- **H-09.** `MIN_PALABRAS_CITA = 3` `[PROPUESTO]`, junto a `MAX_PALABRAS_NOTA`. Cada `cita_nota` (de las erratas y de los dudosos), además de ser literal, debe tener al menos 3 palabras con letra o cifra (separadas por blancos; «a» o « de » no sostienen nada). Si no, `ContrasteInvalido` y sale con 2. Hoy la cita más corta tiene 4 palabras («Matiz: mejor citar 2004»). El informe gana la columna «Cita de la nota» en las tablas de ERRONEA y de dudosos, así que `--comprobar` también ve un cambio de cita. Mutantes nuevos: M79 (quita la comprobación), M80 (mínimo 1) y M81 (la cita no sale en la tabla).

### Decisiones y desviaciones

- El encargo decía que el Anexo G no estaba en el corpus: sí está (arriba). La incidencia lo corrige y propone el resto de criterios.
- `--ejecutor` permite importar el paquete de otra carpeta (las pruebas sintéticas lo usan con un repositorio en `tmp_path`).
- La plantilla se informa pero no cuenta: no es el prompt de un agente.

## Límites conocidos

- Los recuentos son mecánicos. Una cita sin el formato autor-año («Hull *Options…*»), una fórmula escrita sin código ni «=» con espacios, o un umbral escrito como rango no se cuentan; una sigla con año entre paréntesis («BIS (2019)») cuenta como cita. Una entrada con solo la revista en cursiva cuenta como titulada.
- Las afirmaciones candidatas incluyen instrucciones con forma de definición («**Paneles de Dune**: comprueba…»): el revisor las marca NO_VERIFICABLE (81 de 350). El denominador del 95 % son las verificables (INC-T187-02 `[PROPUESTO]`); sobre las 350 serían el 74,3 % y no pasaría.
- El «resultado esperado» de PB-51 («ninguna afirmación técnica errónea») no se cumple al pie de la letra (9 ERRONEA); la aprobación sigue el criterio binario (≥ 95 %). Las erratas no se corrigen aquí (corpus congelado, INC-T187-03).
- El comentario (`comentario.json`) reescribe las notas de los revisores en «error» y «corrección». Desde la r02, el script exige que cada errata y cada dudosa citen literalmente su nota (`cita_nota`) y que las dudosas sean las CORRECTA con matiz. No comprueba que la paráfrasis sea fiel más allá de la cita; la nota original va al lado en los lotes y en el informe de los casos dudosos.
- La medida de los Analistas es una aproximación; la exacta es la de `tests/test_t101_v6.py`.
- Que los DOI existan no se puede comprobar sin red. Hoy no hay ninguno escrito.

## Comandos

```bash
# desde la raíz, con el venv del proyecto
.venv/bin/python .docs/scripts/revision_prompts_pb51.py              # regenera informe y muestra (en el ticket)
.venv/bin/python .docs/scripts/revision_prompts_pb51.py --comprobar  # 0 si lo guardado es lo que sale
.venv/bin/python -m pytest -q -p no:cacheprovider .docs/scripts/pruebas_revision_prompts_pb51.py   # o .docs/scripts/pruebas_scripts.sh
.venv/bin/python .docs/scripts/mutantes_revision_prompts_pb51.py             # 78 muertos
(cd bloque_a/11_Ejecutor && ../../.venv/bin/python -m pytest -q tests/test_t187_pb51.py)   # PB-51 en el plan
.venv/bin/python .docs/scripts/evidencias_plan_a.py --pb PB-51
```
