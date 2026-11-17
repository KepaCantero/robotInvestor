# T-164 · QA independiente

- **Revisor:** claude, subagente revisor sin el contexto de la implementación (solo el plan, el código y la QA r02 de T-157) ·
  **Ronda:** r01 · 2026-11-17
- **Base:** rama `wip/t164`, commit `86c89b0` sobre `e35d284`, en una copia limpia (`git worktree add --detach`), con el venv del
  proyecto enlazado. Todo se ejecuta desde `bloque_a/11_Ejecutor` con `../../.venv/bin/python`.

## Reproducción desde limpio

Por indicación de la sesión coordinadora, **no** se pasan ni la suite completa ni `./tools/check_all.sh`. Se ejecuta lo siguiente:

| Qué | Resultado |
| --- | --- |
| `tests/test_t157_verificador_ids.py` (dentro de los mutantes; el nulo) | 55 superadas |
| Verificador 1.1.0 sobre el repo real frente al de develop (`e35d284`), los dos sobre el mismo corpus | salida 1 en los dos, 2 errores (FX-MC10-003, RF-0123) y 2 avisos; `diff` = solo la línea de la versión (JSON) y el pie (Markdown) |
| `docs/auditoria_ids_bloque_a.json` frente a una ejecución nueva | idéntico byte a byte |
| `docs/auditoria_ids_bloque_a.md` regenerado con `--auditoria` sobre una copia | idéntico byte a byte |
| `T-157/revisores/r01_01_cifras.py` (sobre el JSON nuevo) | «FALLOS: ninguno» |
| `T-157/revisores/r02_01_ataques.py` | 16/16 |
| `T-157/revisores/r01_02_siembra.py` | no arranca (`FileNotFoundError`: fija el Documento 0 V5.1; T-143 lo pasó a V5.2), como dice `pruebas.md` |
| `T-164/r01_02_siembra_v52.py` (copia adaptada del implementador) | 39/43; los 4 fallos son los ya explicados (2 de H-04, 2 de T-143) |
| `T-157/revisores/r02_02_mutantes.py` | 0 vivos, 9 matados; N04 ROTO porque su texto era el defecto de H-09 (lo cubren T08/T09) |
| `T-157/revisores/r01_03_mutantes.py` | 25 matados; M13 vivo (arnés) y M10 ROTO (regla retirada en la r02), como en la r02 |
| `T-157/mutantes_t157.py` | 13 matados, nulo vivo |
| `T-164/mutantes_t164.py` | 14 matados, 0 vivos, 0 rotos, nulo vivo |
| `ruff` sobre `verificador_ids.py`, `test_t157_verificador_ids.py` y `revisores/` | sin errores |
| `tools/corpus_integridad.py` | «Corpus íntegro: 696 archivos» |

## Scripts de esta ronda (`revisores/`)

- `r01_01_excusa.py`: 25 formas de citar IDX-FICT-001 (el único símbolo real con forma de ficha) en una copia del corpus real:
  mayúsculas, comillas, negrita, frases largas, JSON anidado, arrays de objetos, claves «ficha»/«fichas», tablas, sangría, frases
  partidas, abreviaturas, «;», U+2011, y los usos legítimos como serie. Hoy **18/25**; con las correcciones de H-01 y H-02, 25/25
  (comprobado con un parche en memoria; L10–L13 son los límites de H-03 y esperan INFO).
- `r01_02_escritura.py`: escritura en grupo con destinos que ya existen: disco lleno en el último temporal, permiso denegado,
  destino dentro de un fichero, temporal abandonado que es una carpeta, el mismo destino dos veces, el límite declarado y el modo
  del archivo. Hoy **5/6** (falla H-04) e informa H-05.
- `r01_03_cifras.py`: H-10 en el corpus real (1, 2, 4, 5 y 8 cifras, guion U+2011, comillas invertidas, negrita, sufijo). **9/9**.

## Criterios de aceptación

| Criterio | Cumple | Evidencia |
| --- | --- | --- |
| CA-1 (H-09) | **no** | Los casos del plan dan ERROR (pruebas `test_t164_h09_*`, `r02_01` §2, `r01_01` E01–E05). Pero «como valor de `ficha_id` en la misma línea que su `serie_ht01`» da INFO cuando el objeto va dentro de un array: `{"datos":[{"serie_ht01":"X","ficha_id":"X"}]}` (`r01_01` E17, E06, E07). Ver H-01 |
| CA-2 (H-10) | sí | `test_t164_h10_*`; `r01_03_cifras.py` 9/9 con «(¿FX-TREND-001?)»; sin errores nuevos en el corpus real |
| CA-3 (H-11) | sí | `r02_01` §4 (`/proc`); `r01_02` casos 1–4 (disco lleno, permiso, fichero como carpeta, temporal-carpeta): salida 2, destinos viejos intactos, sin temporales. El caso de destino repetido es H-04 |
| CA-4 (H-12) | sí | `r02_02_mutantes.py` 0 vivos; `mutantes_t164.py` 14 matados y nulo vivo |
| CA-5 | sí | tabla de arriba (r02_01 16/16, r01_01 sin fallos, r01_02 y r01_03 como en la r02, `mutantes_t157.py` 13 matados) |
| CA-6 | sí | `diff` con develop: solo la versión; JSON y Markdown del repo = ejecución nueva |
| CA-7 | sí (parcial, por indicación) | ruff limpio en lo tocado, corpus íntegro; suite completa y cuotas, del informe del implementador (no se repiten por orden de la coordinadora) |
| CA-8 (H-04 de T-157) | sí | INC-T157-01, «Referencias con otro número de cifras»; `test_e_referencias` exige AVISO `REF_FORMA_DISTINTA` para `RF-1` |

## Hallazgos

| ID | Gravedad | Cómo reproducirlo | Esperado / obtenido | Corrección sugerida (exacta) | Estado |
| --- | --- | --- | --- | --- | --- |
| H-01 | media | `r01_01_excusa.py` E06, E07, E17: `{"calculos":[{"ficha_id":"IDX-FICT-001"}]}`, `{"pasos":[{"method_id":"IDX-FICT-001"}]}`, `{"datos":[{"serie_ht01":"IDX-FICT-001","ficha_id":"IDX-FICT-001"}]}` | ERROR en el valor de `ficha_id`/`method_id` / **INFO**: la rama de array de `RE_VALOR_JSON` (`\[([^\]]*)\]`) se traga el array de objetos entero, `finditer` ya no ve la clave interior y la cita se atribuye a `calculos`/`pasos`/`datos`, que no es un campo de ficha. Es la misma omisión silenciosa de H-09 en la forma JSON más corriente (arrays de objetos) e incumple CA-1 | `RE_VALOR_JSON = re.compile(r'"(\w+)"\s*:\s*(?:"([^"]*)"\|\[([^\]\[{}]*)\])')` (la rama de array solo para arrays de escalares; un array de objetos deja que `finditer` llegue a las claves de dentro). Prueba de regresión: añadir a `SIMBOLOS` `{"datos":[{"serie_ht01":"AA-SERIE-002","ficha_id":"AA-SERIE-002"}]}` (ERROR e INFO en esa línea) y `{"pasos":[{"method_id":"AA-SERIE-003"}]}` (ERROR); mutante en `mutantes_t164.py` que restaure la regex de antes. Con el parche, las 55 pruebas pasan y el informe real no cambia | abierto |
| H-02 | baja | `r01_01_excusa.py` E08, E09, E14, E15: `{"fichas":["IDX-FICT-001"]}`, `{"ficha":"IDX-FICT-001"}`, «Usa una ficha de índices (p. ej. IDX-FICT-001).», «Fichas: ST-DESC-001; IDX-FICT-001.» | ERROR / INFO: (a) la frase de un valor JSON empieza en el valor, así que la clave «ficha»/«fichas» no cuenta; (b) «p. ej.» corta la frase; (c) «;» la corta dentro de una enumeración de fichas | (a) en `_campo_json`, `return m.group(1), m.start()` (la frase de un valor JSON empieza en su clave; «Según la ficha: {"nota":"X"}» sigue en INFO); (b) y (c) `RE_FIN_FRASE = re.compile(r"(?<!\bp)(?<!\bej)(?<!\be\.g)(?<!\bvs)(?<!\bcf)(?<!\bpág)(?<!\bnúm)[.!?](?=\s)")`. Ajustar el docstring de `_como_ficha`, el diseño del README y el punto (4) de INC-T157-01 («desde el último «.», «!» o «?» que no cierra una abreviatura, o desde la clave del valor JSON»). Pruebas: esas cuatro líneas con AA-SERIE-003 dan ERROR. Con el parche (junto con H-01): 55 pruebas pasan, informe real igual, `r01_01` 25/25 | abierto |
| H-03 | baja | `r01_01_excusa.py` L10–L13: `"estado_madurez_metodos":{"IDX-FICT-001":"implementado"}`; `"ficha_id": [` con el valor en la línea siguiente; una fila `\| IDX-FICT-001 \| … \|` bajo la cabecera `\| Ficha \| … \|` (forma que usa el corpus, prompt del Motor l. 245); «Se calcula con la ficha» / «IDX-FICT-001 del Catálogo.» en dos líneas | Que el límite esté escrito / no lo está: el análisis es por línea y esos usos como ficha de un símbolo declarado quedan en INFO sin que INC-T157-01 ni el docstring lo digan | Añadir al punto (4) de INC-T157-01 y al docstring de `contexto_d`: «Límite: el contexto se lee en la línea de la cita. No se ve «ficha» en otra línea (frase partida, cabecera de una tabla), ni la clave de un JSON con sangría cuyo valor va en la línea siguiente, ni una ficha que es la clave de un objeto (`"estado_madurez_metodos":{"X":…}`); ahí un ID declarado como símbolo se excusa (INFO).» Sin cambio de código | abierto |
| H-04 | baja | `r01_02_escritura.py` caso 5: `main(["--raiz", R, "--json", X, "--md", X])` con X existente | salida 2 con X intacto, o salida 1 con un informe completo / **salida 2 («FALLO CERRADO… No such file») y X sobrescrito con el Markdown**: los dos temporales tienen el mismo nombre, el segundo pisa al primero, el primer `os.replace` lo publica y el segundo falla. Igual con `--md` = `--auditoria`. Contradice «si uno falla, no queda nada escrito» | Al principio de `_escribir_todo`: `destinos = [r.resolve() for r, _ in salidas]` y `if len(set(destinos)) != len(destinos): raise EntradaInvalida("el mismo destino se pide dos veces (--json, --md o --auditoria)")`. Prueba `test_t164_h11_destino_repetido`: `--json X --md X` y `--md Y --auditoria Y` salen 2 con los destinos intactos y sin temporales | abierto |
| H-05 | baja | `r01_02_escritura.py` caso 7: `chmod 0640` sobre el JSON existente y regenerar | conserva 0640 / queda en **0644**: el temporal nace con la umask y `os.replace` cambia el modo del destino sin avisar (viene del temporal de la r02 de T-157; T-164 reescribe esa función) | En el bucle de renombrado, antes de `os.replace(tmp, ruta)`: `if ruta.exists(): os.chmod(tmp, stat.S_IMODE(ruta.stat().st_mode))` (dentro del `try`, de modo que un fallo también limpia). Prueba: un destino con 0o640 sigue en 0o640 | abierto |
| H-06 | baja | `docs/incidencias.md`, INC-T157-01, punto (4), última frase | coherente con el cambio / dice «Una ficha en cualquier otro campo JSON (`estado_madurez_metodos`, `metodo`…) … es error», cuando la misma frase acaba de poner `estado_madurez_metodos` entre los campos de ficha y, para un símbolo, `metodo` sí se excusa | Sustituirla por: «Un ID con forma de ficha que no está declarado como símbolo es error en cualquier campo JSON (`metodo`, `afirmacion`…) y en prosa dentro de un valor.» | abierto |

En la tabla, `\|` es una barra «|» escapada para Markdown: en el código va sin la barra invertida.

**Observación (sin hallazgo).** La regla «ficha en la misma frase» da ERROR también en «Aplica la ficha ST-DESC-001 a la serie
IDX-FICT-001.» (comprobado con `_como_ficha`). Es un error falso posible, pero visible y en el sentido del fallo cerrado; hoy no se
da en el corpus real (informe igual al de develop). Si llega a darse, la salida es reescribir la frase o acotar «ficha» a lo que va
justo delante de la cita.

**Sin errores falsos nuevos en el corpus real:** el informe 1.1.0 es el de develop salvo la versión, y con las correcciones de H-01
y H-02 aplicadas en memoria sigue siéndolo byte a byte.

## Veredicto

**NO APTO** · CA-1 no se cumple en general: un `ficha_id` (o `method_id`) dentro de un array de objetos sigue excusado como símbolo
(H-01, media), que es la misma omisión silenciosa que H-09 quería cerrar. La corrección es una expresión regular con su prueba y su
mutante; H-02 a H-06 (bajas) se subsanan en la misma ronda con las correcciones exactas de la tabla. En la ronda siguiente el
revisor vuelve a pasar `revisores/r01_01_excusa.py` (debe dar 25/25), `r01_02_escritura.py` (6/6 y el modo conservado),
`r01_03_cifras.py`, `r02_01_ataques.py` y los mutantes.

## Ronda r02

- **Revisor:** el mismo de la r01 · 2026-11-17 · **Base:** `b1b4747` (rama `wip/t164`), en la copia del revisor, no en la del
  implementador. Por indicación de la coordinadora, tampoco esta vez se pasan la suite completa ni el gate.

### Correcciones de la r01

| Hallazgo | Corregido | Evidencia |
| --- | --- | --- |
| H-01 (media) | sí | `RE_VALOR_JSON` con la rama de array solo para escalares. `r01_01_excusa.py` E06, E07 y E17 dan ERROR. `r02_01_regresiones.py` A12 (dos objetos en un array: ERROR e INFO) y A13 (anidado a dos niveles) también. Lo cubren la prueba `SIMBOLOS` (líneas 18 y 19) y el mutante T15 (matado) |
| H-02 | sí | `_campo_json` devuelve `m.start()`, y `RE_FIN_FRASE` ya no corta en «;» ni tras las abreviaturas. E08, E09, E14 y E15 dan ERROR, y A03 a A05 (`p. ej.,`, `vs.`, `e.g.`) también. Mutantes T16 a T18 matados. A01, A02 y A09 a A11 siguen en INFO, igual que antes: «etc.», «?» y «!» cierran la frase, y una clave «ficha» con estado no excusa ni acusa a otra clave |
| H-03 | sí | El límite está en el docstring de `contexto_d` y en INC-T157-01 (4). L10 a L13 siguen en INFO, como se declara |
| H-04 | sí | `r01_02_escritura.py` 6/6. `r02_01` rechaza un enlace simbólico al mismo destino (salida 2, nada escrito). Un enlace duro no se pisa, porque `os.replace` cambia la entrada del directorio. Lo cubren `test_t164_r02_h04_destino_repetido` y el mutante T19 |
| H-05 | sí | 0640 sigue en 0640 (`r01_02`) y 0444 en 0444 (`r02_01`). Un destino nuevo nace con la umask (0644). Lo cubren `test_t164_r02_h05_*` y el mutante T20 |
| H-06 | sí | La frase de INC-T157-01 (4) se ha sustituido por la propuesta |

### Reproducción

| Qué | Resultado |
| --- | --- |
| `tests/test_t157_verificador_ids.py` | 57 superadas |
| Informe real frente al de develop (`e35d284`) | El `diff` solo cambia la versión. `docs/auditoria_ids_bloque_a.json` coincide byte a byte con una ejecución nueva |
| `revisores/r01_01_excusa.py` | 25/25 |
| `revisores/r01_02_escritura.py` | 6/6, y el modo se conserva |
| `revisores/r01_03_cifras.py` | sin fallos |
| `revisores/r02_01_regresiones.py` (nuevo) | 19/19, más seis casos `[INF]` (ver H-07 y la observación) |
| `T-157/revisores/r02_01_ataques.py` | 16/16 |
| `T-157/revisores/r01_01_cifras.py` | «FALLOS: ninguno» |
| `T-164/mutantes_t164.py` | 20 matados, ningún vivo ni roto, y el nulo vivo |
| `T-157/revisores/r02_02_mutantes.py` | 9 matados, 0 vivos. N04 sale ROTO, como en la r01 |
| `T-157/mutantes_t157.py` | 13 matados |
| `T-157/revisores/r01_03_mutantes.py` | 26 matados, 0 vivos; M10 ROTO (regla retirada en la r02 de T-157). M13, vivo en la r01 por el arnés, ahora muere |
| `ruff` sobre `revisores/` | sin errores |

### Regresiones buscadas

- **Frases que ahora se juntan.** En el corpus real no aparece ningún error falso: el informe es el mismo, con 2 errores
  (FX-MC10-003 y RF-0123), e IDX-FICT-001 sigue solo en INFO (5 ubicaciones). En un texto sembrado:
  - «Se usa la ficha ST-DESC-001; la serie IDX-FICT-001 sube.» (A08) pasa a dar ERROR. Es la otra cara de H-02, porque «;» ya no
    cierra la frase. El ERROR es visible, señala el lugar exacto, falla en sentido cerrado y coincide con lo que dice INC-T157-01.
    Se acepta como observación, junto con la de la r01.
  - Los arrays de escalares con «{ }» dentro de una cadena (A15) y los arrays de arrays (A16) quedan en INFO. Son formas que el
    corpus no usa y entran en el límite de H-03, así que también quedan como observación.

### Hallazgo nuevo

| ID | Gravedad | Cómo reproducirlo | Esperado / obtenido | Corrección sugerida (exacta) | Estado |
| --- | --- | --- | --- | --- | --- |
| H-07 | baja | `r02_01_regresiones.py` A06 y A07: «Una ficha de índices (Ej. IDX-FICT-001).» y «La ficha de índices (i.e. IDX-FICT-001).» | Se esperaba ERROR, como con «p. ej.», y da INFO. La lista de abreviaturas de `RE_FIN_FRASE` es cerrada y distingue mayúsculas, mientras que INC-T157-01 (4) y el docstring de `_como_ficha` hablan de «una abreviatura» en general | `RE_FIN_FRASE = re.compile(r"(?<!\bp)(?<!\bej)(?<!\be\.g)(?<!\bi\.e)(?<!\bvs)(?<!\bcf)(?<!\bpág)(?<!\bnúm)[.!?](?=\s)", re.IGNORECASE)`. En INC-T157-01 (4) y en el docstring, cambiar «que no cierra una abreviatura» por «que no cierra una de las abreviaturas p., ej., e.g., i.e., vs., cf., pág. y núm. (sin distinguir mayúsculas)». Añadir a `SIMBOLOS` la línea «Una ficha de índices (Ej. AA-SERIE-003).» y su línea en el ERROR esperado. Actualizar los textos de los mutantes T17 y T18 a la regex nueva. Con el parche aplicado en memoria pasan las 57 pruebas, el informe real no cambia, `r01_01` da 25/25, `r02_01` da 19/19, y A06 y A07 dan ERROR | abierto |

### Veredicto r02

**APTO.** Se cumplen los ocho criterios: el CA-1 ya en general (H-01) y el CA-7 en la parte que se ha comprobado aquí.
H-01 a H-06 están corregidos y cada uno tiene su prueba y su mutante. No hay errores falsos nuevos en el corpus real. Solo queda
H-07 (baja), que se subsana en la ronda de cierre con la corrección exacta de la tabla. En esa ronda, `r02_01_regresiones.py` debe
seguir dando 19/19 y A06 y A07 deben dar ERROR.

## Ronda de cierre

- **Revisor:** el mismo · 2026-11-17 · **Base:** `01e2ef7`, comprobado en la copia del revisor (`qa164`).

| Hallazgo | Estado | Evidencia |
| --- | --- | --- |
| H-07 (baja) | corregido | `RE_FIN_FRASE` incluye `i.e` y `re.IGNORECASE`. El docstring de `_como_ficha` e INC-T157-01 (4) enumeran las abreviaturas. `SIMBOLOS` añade «Una ficha de índices (Ej. AA-SERIE-003).», que da ERROR. En `r02_01_regresiones.py`, A06 («Ej.») y A07 («i.e.») dan ERROR, con 19/19. Mutante propio, en una copia y sin tocar el módulo del implementador: quitar solo `re.IGNORECASE` lo mata `test_t164_h09_simbolo_no_excusa_como_ficha` (1 failed, 56 passed). T05, T17 y T18 rehechos; `mutantes_t164.py`, 20 matados, ningún vivo ni roto |

Reproducción: `test_t157_verificador_ids.py` 57 superadas; `r01_01_excusa` 25/25, `r01_02_escritura` 6/6, `r01_03_cifras` sin fallos,
`r02_01_regresiones` 19/19, `T-157/revisores/r02_01_ataques` 16/16; informe real igual al de develop salvo la versión y
`docs/auditoria_ids_bloque_a.json` igual a una ejecución nueva (2 errores, 2 avisos). Queda sin mutante propio quitar solo `i.e`
de la lista (lo cubre `r02_01` A07 y T18 los quita todos); no es hallazgo.

### Veredicto final

**APTO** · los ocho criterios se cumplen (CA-7 según el informe del implementador, sin repetir la suite completa ni el gate por
indicación de la coordinadora) y H-01 a H-07 están corregidos; nada pasa a la deuda técnica.
