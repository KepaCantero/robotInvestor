# T-122 · QA independiente

- **Revisor:** subagente revisor nuevo, sin contexto de la implementación (Claude; implementó otra sesión de Claude) · **Ronda:** r01 · 2026-11-14
- **Copia revisada:** `git worktree` con HEAD separado en `63d6ae9`; el código de T-122 está en `c25fb8b` («wip local: T-122»): `contratos.py` (`RE_SECRETO`), `evaluador.py` (`lecciones_por_encargo`), `llm.py` (`contenido_sensible`, `_json_por_defecto`) y `tests/test_t122_hallazgos.py`. Encima está T-123 (`b9f745a`, `1455b03`), que añade a `secretos_en_texto` el IBAN de otros países y las tarjetas: lo tengo en cuenta al leer los scripts de origen.
- **Orden de lectura:** `README.md`, `.docs/tickets/T-120/qa.md` y `.docs/tickets/T-113/qa.md` («Ronda r02») → diff y pruebas → scripts → al final `analisis-tecnico.md`, `pruebas.md` e INC-T122-01.
- **Numeración:** los hallazgos de origen son H-01 y H-02 (T-120) y H-10 a H-12 (T-113 r02); los nuevos siguen en H-13.

## Reproducción desde limpio

Desde `bloque_a/11_Ejecutor` de la copia, con `../../.venv/bin/python` (los scripts de origen importan con `sys.path.insert(0, ".")`). Lo marcado «leído» está deducido del código; el resto, ejecutado.

| Script | Orden | Resultado |
| --- | --- | --- |
| T-120 `r01_01_iban_banco.py` | `QA_TMP=<carpeta> ../../.venv/bin/python ../../.docs/tickets/T-120/revisores/r01_01_iban_banco.py` | «FALLOS: 1»: el único es «N · IBAN alemán» (`DE89 3704 …`), que el script de T-120 esperaba **no** marcado porque entonces solo se cubría el español; ahora lo marca T-123, a propósito. No es de T-122. Las formas del IBAN español (espacio duro, fino, tabulador, salto de línea, dos espacios) se marcan, y CT-03, CT-04 y CT-23 rechazan sin dejar el dato en ningún archivo |
| T-120 `r01_02_lecciones_config.py` | ídem | Todos los valores raros fallan cerrado: 0, −1, −3, −100, «diez», «4», «», 2.7, 1e3, NaN, infinito, `True`, `False`, `[4]`, `{…}`, 10**30 → `ValueError`; `None` → `KeyError`. «valores negativos que NO fallan cerrado: []». Con el argumento explícito `max_n` sigue sin validarse (H-14) |
| T-120 `r01_03_iban_fuera_de_lo_declarado.py` | ídem | **«formas admitidas: 0»** (antes, 6) |
| T-113 `r02_06_conjunto_bajo_diccionario.py` | `../../.venv/bin/python ../../.docs/tickets/T-113/revisores/r02_06_conjunto_bajo_diccionario.py` | **«regresiones: 0»** |
| T-113 `r01_01_sensible_diferencial.py` | ídem | **«FALLOS: 0»**; los ciclos (dict y lista cíclicos) dan `True` en menos de 5 s |
| Mutantes A1b, B7 y C1 con el script de origen | `python .docs/tickets/T-113/revisores/r02_04_mutantes.py . <desechable> A1b,B7,C1` (desde la raíz) | A1b «SOBREVIVE al ticket y a las vecinas» (B7 y C1, igual): ese script solo ejecuta `test_t113_deuda.py` y sus vecinas, **no** las pruebas nuevas de T-122; sobreviven por construcción |
| Mutantes A1b, B7 y C1 frente a las pruebas nuevas (mío) | `python .docs/tickets/T-122/revisores/r01_02_mutantes_a1b_b7_c1.py . <desechable>` (desde la raíz) | **Los tres mueren**: A1b por `test_t113_h10_un_diccionario_dentro_de_un_conjunto_se_ve[valor2]`, B7 por `test_t113_h12_una_ultima_linea_demasiado_anidada_se_quita_al_seguir_grabando`, C1 por `test_t113_h12_las_lineas_descartadas_de_la_cinta_se_declaran_al_arrancar` |
| Ataque propio | `../../.venv/bin/python ../../.docs/tickets/T-122/revisores/r01_01_iban_y_conjuntos.py` | **FALLOS: 0**. Ver abajo |
| Ciclo V5, goldens, gates ligeros, ruff y mypy | los de T-121 y T-123 (misma copia) | Ciclo idéntico a `00ed8d3` (56 de 57 ficheros byte a byte, `consumo.csv` salvo latencias); goldens «coinciden»; corpus, refs, secretos y NFC en verde; ruff 2902, mypy 109 |
| Suite de A | una vez, al final (común a los cuatro tickets) | Ver «Suite» al final |

### Ataque al patrón del IBAN y a `contenido_sensible` (`r01_01_iban_y_conjuntos.py`)

- **Se detecta** (13 formas): junto, en grupos, impreso 4-4-4-2-10, espacio duro, espacio estrecho, dos espacios, minúsculas, «Es» mixto, guion y punto seguidos, tabulador, en JSON escapado con ` ` y con `\n` (por la segunda pasada de `secretos_en_texto` sin escapes), y seguido de « 15 de noviembre».
- **No se marca** (10): tres espacios entre grupos (límite declarado), 21 cifras, «Res» + 22 cifras, «mes12 …», ISIN españoles, barras, comas, «ES » con espacio, decimales tras «ES», «ES-2024-01-05 …».
- **Falsos positivos:** en 20 000 frases con «es»/«ES» y series de cifras al azar, 337 marcadas, **todas** de las dos plantillas en que «ES»/«es» va pegado a las cifras («ES1234 5678 …», «la serie es1234 …»); ninguna de «el valor es 1234 …», «ES 1234 …», «es: …». «ES» + 22 cifras pegadas se marca siempre (970 de 3 000 al azar: el tercio con 22 cifras): el patrón no lleva dígito de control, por diseño («más estricto», INC-T122-01). En texto corriente no he encontrado otra vía.
- **Coste:** lineal (100 k → 400 k caracteres: ×3,5 a ×4,3 de tiempo; 400 k en < 0,25 s) con «ES12 3456 7890 » repetido, «es12» con espacios duros y cifras con dos separadores.
- **Diferencial de `contenido_sensible`** frente a `b9abb29` (la función y `_diccionarios_de_arriba` de antes, extraídas con `git show` y ejecutadas con el `secretos_en_texto` actual): 6 000 estructuras al azar con listas, tuplas, conjuntos, frozensets, diccionarios con hash dentro de conjuntos, un 5 % con ciclo: **0 True → no True**, **0 excepciones nuevas**, 21 que ahora se detectan y antes no; tiempo máximo 8 ms. 20 000 diccionarios con hash en un frozenset: 0,38 s. Un frozenset anidado 3 000 niveles: termina en 0,03 s (False antes y ahora). El caso de origen (dict > lista > dict > set > dict con «api_key»): antes False, ahora True.

## Criterios de aceptación

| Criterio | Cumple | Evidencia |
| --- | --- | --- |
| CA-1 | sí | T-120 `r01_03`: 0 formas admitidas; `r01_01`: espacio duro, fino, impreso, dos espacios y minúsculas rechazados por CT-04, CT-03 y CT-23 sin dejar el dato; mi ataque, 13 formas detectadas y 10 negativos sin marcar |
| CA-2 | sí | T-120 `r01_02`: 18 valores raros, todos fallan cerrado (al crear el Evaluador y al usarlo) |
| CA-3 | sí | `r02_06`: 0 regresiones; `r01_01_sensible_diferencial.py`: 0 fallos; mi diferencial: 0 regresiones, 0 excepciones nuevas, termina siempre |
| CA-4 | sí | Mis mutantes con las pruebas nuevas: A1b, B7 y C1 mueren (el script de origen no las ejecuta) |
| CA-5 | sí, salvo el gate entero | Goldens sin cambios; gates ligeros, ruff y mypy en verde; `./tools/check_all.sh` entero no lo he lanzado (por instrucción) y `pruebas.md` dice que «lo pasa `commit_limpio.sh` al hacer el commit», es decir, tampoco consta ejecutado. La suite, abajo |

## Hallazgos de origen

| Origen | Estado | Evidencia |
| --- | --- | --- |
| T-120 H-01 (media) | corregido | CA-1 |
| T-120 H-02 (baja) | corregido (por la configuración; ver H-14) | CA-2 |
| T-113 H-10 (baja) | corregido | CA-3 |
| T-113 H-11 (baja) | corregido (declarado en INC-T122-01; leído) | INC-T122-01, «Romanos» |
| T-113 H-12 (baja) | corregido | CA-4 |

## Hallazgos nuevos

| ID | Gravedad | Cómo reproducirlo | Esperado / obtenido | Corrección sugerida | Estado |
| --- | --- | --- | --- | --- | --- |
| H-13 | baja | Leído: `bloque_a/11_Ejecutor/bloque_a/evaluador.py`, `LECCIONES_POR_ENCARGO_MAX = 10` | **Esperado** (regla 2 de `CLAUDE.md`): ningún número escrito a mano; sale del Anexo A → `por_defecto.yaml` o de una ficha. **Obtenido:** el tope 10 está en el código (del texto del 12.3 del Documento 0, marcado `[PROPUESTO]` en INC-T122-01) y repite el valor de `aprendizaje.lecciones_por_encargo` de `por_defecto.yaml` | Llevar el tope a la configuración (p. ej. `aprendizaje.lecciones_por_encargo_max`) o citarlo como constante del Documento 0 en un único sitio documentado | abierto |
| H-14 | baja | T-120 `r01_02` («argumento explícito»): `Evaluador.lecciones_vigentes(as_of, max_n=-1)` | **Esperado:** el mismo fallo cerrado que con la configuración. **Obtenido:** `max_n=-1` da 13 de 14 lecciones, `max_n=100` las 14 y `max_n=12` 12 (más que el máximo del Documento 0). Hoy ningún llamador del paquete pasa `max_n` (leído: `grep max_n`), así que no se alcanza | Validar también el argumento, o quitarlo | abierto |

## Suite

`cd bloque_a/11_Ejecutor && ../../.venv/bin/pytest -q -p no:cacheprovider` (una sola vez, en la copia `63d6ae9`, común a T-119 r02, T-121, T-122 y T-123): **5663 passed** en 23 min 43 s, código de salida 0 (línea base 607).

## Veredicto

**APTO.**

Los cinco criterios se cumplen (CA-5 sin el gate entero, que no he lanzado por instrucción y que tampoco consta ejecutado en `pruebas.md`) y no queda ningún hallazgo crítico ni alto. Los scripts de origen dan lo esperado (el único «FALLO» del `r01_01` de T-120 es el IBAN alemán, que ahora marca T-123 a propósito), el patrón nuevo del IBAN no tiene falsos positivos en texto corriente salvo «ES»/«es» pegado a 22 cifras (por diseño, sin control), el coste es lineal, el máximo de lecciones falla cerrado con los 18 valores raros, y `contenido_sensible` con conjuntos no pierde nada de lo que antes detectaba (0 regresiones y 0 excepciones nuevas en 6 000 estructuras) y siempre termina. Los mutantes A1b, B7 y C1 mueren ante las pruebas nuevas.

Quedan dos bajos para la deuda: **H-13** (el tope 10 de lecciones escrito en el código) y **H-14** (`max_n` explícito sin validar, sin llamadores).

**Condición de cierre:** `./tools/check_all.sh` 12/12 en el commit.

**Sin comprobar:** el gate entero; los demás scripts de la QA r02 de T-113 (`r02_01`, `r02_05`) y de la r01 (`r01_13`); la suite de B.
