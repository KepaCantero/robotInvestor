# T-152 · QA independiente

- **Revisor:** revisor nuevo sin contexto de la implementación (subagente de Claude; implementó Claude) · **Ronda:** r01 · 2026-11-16
- **Copia:** git worktree en el scratchpad con HEAD `c018153` (la versión definitiva, con el umbral en q/p ≤ 2·`tolerancia_clon`) y `.venv` enlazado. Sin red, sin la API y sin coste. Opinión formada con el README, el `qa.md` de T-150 y el diff `3b998bf..c018153` (sin lo de T-168) antes de leer `analisis-tecnico.md` y `pruebas.md`. Mutantes en tres copias desechables **completas** con «t147_mut» en la ruta (`git archive c018153 | tar -x`), que pasan sin mutar las 217 pruebas de `test_t150`, `test_t149` y `test_t144` y las 884 de las 14 suites que tocan `frontera_b.py` o IDX-CONC-001; borradas al acabar. La versión del 1 % para comparar: `git show 32af7fe:bloque_a/11_Ejecutor/bloque_a/motor/frontera_b.py`. La decisión del operador (el umbral al 2 %) no se discute aquí: se comprueba que la implementación, las medidas y las pruebas la sostienen.

## Reproducción desde limpio

| Comprobación | Resultado |
| --- | --- |
| Suite completa de A, una vez (`cd bloque_a/11_Ejecutor && ../../.venv/bin/python -m pytest -q -q -x -p no:cacheprovider`) | **en verde**: 7206 recogidas, llega al 100 % con `-x` (ningún fallo; con `-q -q` pytest no imprime el resumen), 31 min 32 s con otros trabajos en paralelo. El gate del commit (`commit_limpio.sh`) dio 7204 passed (+2 skipped) en A, 68 en A-Forex y 176 en B, 12/12. Línea base ≥ 607 |
| ruff desde la raíz, tres ejecutores (`… \| wc -l`) · mypy de A (`--ignore-missing-imports --no-error-summary bloque_a/11_Ejecutor/bloque_a \| wc -l`) | **2813** (cuota 2813) · **109** (cuota 109). Los ficheros tocados (`test_t150.py`, `frontera_b.py`, `cadena_a_b.py`) y los scripts del ticket, sin avisos de ruff |
| `tools/refs_vivas.py`, `secrets_scan.py`, `nfc_check.py`, `corpus_integridad.py` | rutas vivas · sin hallazgos · NFC · **695** archivos íntegros (en la copia y en el árbol principal con este `qa.md` y `revisores/` ya escritos) |
| `.docs/scripts/pruebas_scripts.sh` | 231 passed (línea base 231) |
| `.docs/tickets/T-152/mutantes.py <copia>` | **16 muertos**, U2 «equivalente esperado» (vive), 0 vivos |
| `.docs/tickets/T-152/mutantes_heredados.py <copia> <tmp>` | `T-150/mutantes.py` con F3 sobre la línea nueva: **22 de 22 muertos**. `T-150/revisores/r01_04_mutantes_qa.py` sin X01: **Y01, Z03 y W01 muertos**; X08 y Z05 equivalentes; solo vive **X02** (O-03 de T-150); termina con 1 por X02, como se declara |
| `T-149/revisores/r01_02_mutantes_qa.py <copia>` | 23 muertos, N25, N31 y N32 equivalentes, **0 vivos** |
| `medir_umbral.py --semillas 100` | **idéntica** a `medir_umbral_100.txt` |
| `T-150/medir_truncado.py --semillas 300`, nuevo frente al de `32af7fe` (`--modulo`) | **idéntico** |
| `T-149/medir_copias.py --semillas 300`, nuevo frente al de `32af7fe` | idéntico salvo **tres casillas** de los fondos: 1/32 a 2 con TE 0,01 %, 284 → 283; 1/8 a 12 con TE 0,01 %, 287 → 288; 1/8 a 12 con TE 0,1 %, 196 → 195. Lo mismo que dicen INC-T127-01 y `pruebas.md` |
| `.venv/bin/python .docs/scripts/cadena_a_b.py --trabajo <tmp> --sonda-sin-correspondencia` (los dos ejecutores simulados de verdad, con la versión definitiva) | código 0; ENTREGADA, G3 APTO, 3 enviables, 1 entregada y válida, 1 vuelta, sonda ADMITIDA, sin `sin_envio`: el paquete real pasa `_forma_paquete` |

## Criterios de aceptación

| Criterio | Cumple | Evidencia |
| --- | --- | --- |
| CA-1 (H-01 de T-150) | sí | Revisor de T-150 vía `mutantes_heredados.py`: Y01, Z03 y W01 muertos; solo vive X02 |
| CA-2 (H-02 de T-150) | sí | La medida del 1 al 10 % está en INC-T127-01 y se reproduce (`medir_umbral.py`, idéntica). El umbral está en q/p ≤ 2 % (`desplaza = rel <= tol`, sin números nuevos). `medir_truncado.py` sin cambios y `medir_copias.py` con ±1 de 300 en tres casillas, reproducidos con 300 semillas. La prueba del borde mata el umbral de antes (U1) y uno un 5 % más bajo (U2b); de hecho, cualquiera más bajo, incluso un 0,1 %, y el `<` estricto (`r01_02`, O-01). Lo que la prueba **no** ve es un umbral más alto, y no es equivalente como se declara (H-01 de esta ronda) |
| CA-3 (O-01 de T-150) | sí | INC-T127-01, ronda T-152, lo nombra como límite declarado `[PROPUESTO]`; `test_t152_o01_…` lo fija y comprueba que cada mitad sola sí se agrupa |
| CA-4 (O-02 de T-150) | sí | Las formas de la QA de T-150 (correspondencia con lista, diccionario, número y texto, símbolo número; `clases` lista, clase texto, opciones que no son lista, opción sin `opp_id`, `opp_id` no texto, `paquete_para_bloque_B` no lista) dan mensaje sin el contenido, código 1, sin traza ni envío (pruebas `test_t152_o02_*` y `r01_03`; K1 a K10 muertos). Además fechas de YAML como símbolo, `!!set` y `clases` repetida: mensaje y 1. Quedan otras formas que sí dan traza (H-02 de esta ronda), fuera del criterio |
| CA-5 | sí | `T-152/mutantes.py` sin vivos (con U2 como «equivalente esperado», ver H-01); T-150 y T-149 r01_02 siguen muertos; suite de A en verde; ruff 2813 y mypy A 109 en su cuota; los cuatro gates ligeros en verde y el gate del commit 12/12 |

### El umbral nuevo en otras rejillas, niveles y familias (`r01_01`, 100 semillas)

Cada familia con siete umbrales de q/p: 1 %, 1,9 %, el 2 % del código, 2,5 %, 4 %, 10 % y sin umbral.

- **Falsos negativos en el tramo del 1 al 2 %.** Copias truncadas a 0,01, 0,05, 0,25, 1/8, 1/32 y 0,001 (paseo normalizado y geométrico), con un 5 % de sesiones ausentes, con un 4 % de precios sin redondear, a otra escala (×1,1), frente a la redondeada y frente a otra truncada a 0,001: **0 de 100 sin agrupar con el 2 %** en todas. Con el 1 %, 87 a 100 de 100 sin agrupar; con el 1,9 %, de 0 a 100 según la rejilla.
- **Falsos positivos.** Probé índices con ρ 0,99, 0,995 y 0,999 en las seis rejillas (r/t y t/t), un índice frente a su rentabilidad total, un fondo frente a su índice (TE 0,1 % y 0,01 %) y series casi planas y monetarios con q/p del 2 al 100 %. Los siete umbrales dan **lo mismo** en todas las familias salvo una semilla: ρ 0,999, 1/8 a 9, t/t, 33 con el 1 % y 34 con el 2 % (O-03). Las tasas altas (ρ 0,999: 31 a 80 de 100; fondos: 100 de 100) son el límite declarado de los pasos grandes y no cambian con el umbral.
- **Por encima del 2 %.** Con todo el tramo por encima (2,04 a 2,50 %), ninguna copia truncada se agrupa con ningún umbral, como dice la prueba. Justo en el borde (2,00 a 2,06 %) el 2 % deja sin agrupar 94 y 95 de 100, y un umbral más alto 90 y 91. Donde el umbral sí cambia el resultado es en las copias que **cruzan** el 2 % por poco (H-01).

## Hallazgos

| ID | Gravedad | Cómo reproducirlo | Esperado / obtenido | Corrección sugerida | Estado |
| --- | --- | --- | --- | --- | --- |
| H-01 | baja | `.venv/bin/python .docs/tickets/T-152/revisores/r01_04_mutantes_qa.py <copia «t147_mut»>` y `.venv/bin/python -I .docs/tickets/T-152/revisores/r01_01_umbral_qa.py --solo XY` · `r01_05_semillas_qa.py` | **Esperado:** lo que declaran la prueba del borde («un umbral más alto no se distingue (mutante equivalente)»), `mutantes.py` (U2 «equivalente, la cota ya está en el tope»), el README (Riesgos), `analisis-tecnico.md`, `pruebas.md`, el comentario de `frontera_b.py` («y por encima no cambia nada») y la lección de memoria («por encima del tope, el mutante es equivalente»). **Obtenido:** un umbral más alto vive con las 884 pruebas de las 14 suites de IDX-CONC-001 y `frontera_b` (V01 al 2,5 %, V02 al 4 %, que es U2, V03 al 10 % y V05 al 2,04 %), pero **no es equivalente**. Una copia truncada a 0,01 cuyo precio cruza por poco el 2 % de q/p cambia de resultado. En [0,4905, 0,9], con el 2 % quedan sin agrupar 56 de 100, y con el 2,5 % o más, 1. En [0,48, 0,9], al revés: 89 frente a 100. Con el generador de la propia prueba (`_en_tramo(0.48, 0.9, s)`) hay 19 semillas de 100 (12, 14, 27, 28…) que se agrupan con el 2 % y no con el 2,5 %, el 4 % ni sin umbral. El código implementa bien la decisión del operador; lo que falla es la resolución declarada y la afirmación de equivalencia | Añadir a `test_t152_h02_…` un caso que fije el lado de arriba: `(0.01, 0.48, 0.9)` con semillas de `r01_05` que se agrupan solo con el 2 % (mata U2, V01 y V03; V05, al 2,04 %, sigue vivo y es la resolución de arriba). Quitar U2 de los equivalentes esperados de `mutantes.py`. Y corregir los textos: por encima del 2 % el umbral solo cambia las copias que cruzan el 2 % por poco | abierto |
| H-02 | baja | `.venv/bin/python -I .docs/tickets/T-152/revisores/r01_03_formas_qa.py <carpeta temporal>` | **Esperado** (objetivo de O-02): un fichero que se lee pero tiene una forma inesperada termina con un mensaje y el código 1, sin traza. **Obtenido:** cuatro formas dan traza; ninguna copia un dato de R8. (1) Un `paquete_json` con un JSON anidado 100 000 niveles da `RecursionError` en `json.loads`, que no se captura. (2) Un `opp_id` de 300 cifras, que el patrón `^OPP-[0-9]{4}-[0-9]{4,}$` del esquema de A admite, da `OSError` (nombre demasiado largo) al escribir `peticiones/<opp_id>.json`, después de validar. (3) Un sustituto suelto (`\ud800`, válido en JSON) da `UnicodeEncodeError`. En el `nombre` salta al escribir la petición, que queda como un fichero vacío. En el símbolo de una entrada sin correspondencia salta al escribir `resumen.json`, al final, que queda vacío (0 bytes), ya enviadas las demás opciones. (4) Un `--config-a` anidado 100 000 niveles da `RecursionError` en `yaml`. Todas quedan fuera de CA-4, que solo cubre las formas de la QA de T-150 | Capturar en la lectura `RecursionError` (los dos ficheros) y, en `_escribir` o alrededor del bucle de envíos, `OSError` y `UnicodeEncodeError`, con el mensaje sin contenido y el código 1. También `_resumen` cuando la escritura falla, para no dejar un `resumen.json` vacío. O, más simple, una red final en `main` que imprima solo el tipo de la excepción y termine con 1 | abierto |
| H-03 | baja | `git branch -a --contains 4e39324` (vacío) · `pruebas.md`, «Comandos» | **Esperado:** los comandos de `pruebas.md` funcionan desde un clon limpio. **Obtenido:** `git show 4e39324:…/frontera_b.py` cita un commit que no está en ninguna rama: es la versión de antes del rebase sobre T-168, y la subida es `32af7fe`. Su `frontera_b.py` es idéntico, pero en un clon el comando falla. Hay otras erratas. `analisis-tecnico.md` dice «por encima del 1,8 %, la cota está en el tope y el umbral no cambia nada» y «con la propuesta para T-57», que vienen de la primera versión y contradicen la prueba del tramo de 1,82 a 1,96 %. README y diario dicen 23 pruebas, y son 24 (`pruebas.md` dice bien 24). El docstring del bloque T-150 de `frontera_b.py` sigue diciendo «se desplaza solo en los precios cuyo paso entero, q/p, no pasa de `tol`», justo encima de la nota de T-152 que lo corrige | `4e39324` → `32af7fe` en `pruebas.md`; quitar o corregir las dos frases de `analisis-tecnico.md` y el número de pruebas; reescribir la frase del comentario de T-150 o marcarla como sustituida | abierto |

Observaciones (no son hallazgos):

- **O-01, la resolución de la prueba del borde es mejor que la declarada, y por un artefacto.** En el primer caso, `(0.05, 2.55, 2.75)`, el mínimo de cada semilla es exactamente 2,55, y ⌊2,55/0,05⌋ da 50 en coma flotante. Así la copia vale 2,50 en esa fecha, con q/p = 2,00 % exacto: justo en el borde, no «de 1,82 a 1,96 %» como dice el comentario. Por eso la prueba mata cualquier umbral más bajo, incluso un 0,1 % (`r01_02`), y el `<` estricto (V04). Sin ese precio (`lo` = 2,5501), la resolución es de un 1 a un 2 %: mata el 0,98 y no el 0,99 (`r01_02`, al final). Las dos cumplen el «5 % más bajo» declarado, pero conviene decir en el comentario que el caso incluye el borde exacto.
- **O-02, el límite declarado de los pasos grandes depende del par, no de la serie.** Una copia truncada a 0,05 frente a otra redondeada a 0,01 a otra escala, ambas con q/p del 1 al 1,9 %, no se agrupa con ningún umbral (100 de 100), y dos redondeadas tampoco. La cota es la suma de las dos medias anchuras, con tope en `log(1 + tolerancia_clon)`. Además, una copia truncada cuyo precio pasa del 2 % en una parte de su historia no se agrupa casi nunca: de [0,47, 0,9] a [0,40, 0,66], 95 a 100 de 100, mientras la redondeada se agrupa en la mitad o más. La frase de INC-T127-01 («la copia truncada que no se agrupa es la de un paso entero de más del 2 % del precio») vale frente a una serie fina y en toda la historia; convendría precisarla. Falla cerrado: la amplitud no se sirve.
- **O-03, un falso positivo más en una familia.** En ρ 0,999, 1/8 a 9, t/t, hay 33 de 100 con el 1 % y 34 con el 2 %. Es del mismo orden que el ±1 de 300 de `medir_copias.py` y está dentro del límite declarado de los pasos grandes. En las demás familias, lo mismo con todos los umbrales.
- **O-04, el detalle de un error de esquema copia el valor.** Un `indicador_seguimiento` que es una lista con una marca llega a `resumen.json` dentro de `ENTRADA_B_INVALIDA`, limpio de R8 (`r01_03`). Es lo que hace `errores_entrada_b` desde T-149 y no es de T-152: solo se apunta, porque los mensajes nuevos de `_forma_paquete` sí cumplen «sin el contenido».

**Invariantes:**
- Nada de LLM en la ruta.
- Ningún número nuevo: el umbral sale de `tolerancia_clon`.
- La decisión del umbral es del operador y está en INC-T127-01 y en la deuda. El límite de O-01 va como `[PROPUESTO]`.
- Los correos de prueba van partidos.
- Nada de secretos ni de datos personales.
- La fila de la deuda está EN QA; no la toco.

Scripts de esta ronda, en `revisores/`. Se ejecutan desde la raíz de la copia; los que leen el código aceptan `--raiz <copia>`.

1. `.venv/bin/python -I .docs/tickets/T-152/revisores/r01_01_umbral_qa.py [--raiz <copia>] [--semillas N] [--solo NXYF]`: falsos negativos (N), copias que cruzan el 2 % (X), tramos justo por encima (Y) y falsos positivos (F), con siete umbrales. Solo informa: termina con 0. 100 semillas en unos 50 s.
2. `.venv/bin/python -I .docs/tickets/T-152/revisores/r01_02_borde_qa.py [--raiz <copia>]`: la resolución de la prueba del borde con 26 umbrales, con 12 y con 100 semillas. Termina con 0. Al final, el contrafactual sin el precio de 2,50 (`lo` = 2,5501, O-01).
3. `.venv/bin/python -I .docs/tickets/T-152/revisores/r01_03_formas_qa.py <carpeta temporal> [--raiz <copia>]`: 22 formas de `paquete_json` y `--config-a`, con los ejecutores como dobles. Marca OK, TRAZA, FUGA R8 y copia de contenido. Termina con 0; hoy da cuatro TRAZA (H-02).
4. `.venv/bin/python .docs/tickets/T-152/revisores/r01_04_mutantes_qa.py <copia desechable y completa con «t147_mut»>`: seis mutantes de la línea del umbral contra las 14 suites de IDX-CONC-001 y `frontera_b`, tras comprobar que la copia sin mutar pasa. Termina con 1 por V01, V02, V03 y V05 (H-01). Tarda unos 16 min.
5. `.venv/bin/python -I .docs/tickets/T-152/revisores/r01_05_semillas_qa.py`: las semillas de `_en_tramo` en las que el 2 % y un umbral más alto difieren, para la prueba que sugiere H-01. Termina con 0.

**No comprobado:**
- `./tools/check_all.sh` entero en esta ronda. Lo ejecutó `commit_limpio.sh` en el commit, con 12/12; aquí, solo sus piezas.
- B: no se tocan.
- IDX-CONC-001 con datos de mercado reales: solo series sintéticas.
- Los revisores de T-141, que necesitan red.

## Veredicto

**APTO** · los cinco criterios se cumplen con evidencia y no hay hallazgos críticos ni altos.

Los tres hallazgos son bajos y no tocan la decisión del operador ni el código que la implementa:
- **H-01:** la prueba del borde no ve un umbral más alto, que no es equivalente como se declara: cambia las copias que cruzan el 2 % por poco.
- **H-02:** quedan cuatro formas de fichero con traza, fuera de CA-4.
- **H-03:** una referencia a un commit que no está en ninguna rama y varias erratas de texto.

Van a la deuda técnica con su ID. La sesión coordinadora es quien cierra el ticket y actualiza la fila de la deuda; este revisor no toca ninguna de las dos.
