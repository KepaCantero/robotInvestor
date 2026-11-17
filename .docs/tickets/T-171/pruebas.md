# T-171 · Pruebas

Copia: worktree sobre `origin/develop` (`a9210c0`), venv del proyecto. Sin red: todo con `MockClient` o funciones puras.

| Suite | Antes (develop) | Después |
| --- | --- | --- |
| Suite completa de A (`pytest -q` en `bloque_a/11_Ejecutor`) | 7798 recogidas | **7963 superadas, 2 omitidas** (44 min 50 s; 7966 recogidas tras la última prueba añadida) |
| `tests/test_t171_guias.py` | — | 168 superadas |
| `test_t161_guias`, `test_t161_r02`, `test_t161_r03`, `test_t161_r04`, `test_t158*`, `test_t126_pb26_pb48` | 777 | 777 superadas (sin cambiar ninguna expectativa) |
| `r04_02_integracion.py` + `r05_01_cierre.py` | 34 + 2 fallos esperados | igual: 34 superadas; fallan las dos `test_defecto_*` de H-17, que miden el defecto ya corregido en la ronda de cierre de T-161 |

## Tasas del detector (inventarios de los revisores)

| Juego | develop | T-171 |
| --- | --- | --- |
| `r04_01` ataques (30) | 17 pasan | **3** (las 3 paráfrasis V, límite declarado) |
| `r04_01` ítems válidos (28) / lecciones prudentes (10) | 3 / 2 | **0 / 0** |
| `r03_01` ataques (27) / válidos (26) | 0 / 3 | 0 / 3 (los declarados en la r04) |
| `r02_01` ataques (52) / válidos (48) | 0 / 0 | 0 / 0 |
| `r01_01` ataques (68) / válidos (40) | 1 (la repartida) / 0 | 1 / 0 |
| `medir_detector.py`: 50 y 68 ataques; 17, 40 y 40 válidos | 0, 0; 0, 0, 1 | 0, 0; 0, 0, 1 |
| Reservado de T-171 (`reservado_t171.py`, commit `45064cd`, medido una vez): 20 ataques, 16 válidos, 8 lecciones | — | **0, 0, 0** (optimista: lo escribió el implementador) |
| Propio (`test_t171_guias.py`): 28 ataques, 24 válidos, 9 lecciones | — | 0, 1 (declarado, ya en develop), 0 |

En la primera versión, `ALCANCE_PARTE` sin la condición del objeto directo daba 5 falsos positivos en los 17 del diseño (el ejemplo
del prompt 4.5 entre ellos), 1 en `r01_01`, 1 en `r02_01` y 1 de dominio; se corrigió antes de medir el reservado.

## Criterio de aceptación → prueba

| Criterio | Prueba | Resultado |
| --- | --- | --- |
| CA-1 | `test_t171_guias.py::test_h18_*`, `r04_01` | cumple: 3 de 30, solo V |
| CA-2 | `test_h19_*`, `r04_01` | cumple: 0 de 28, 0 de 10 |
| CA-3 | `r01_01`–`r03_01`, `medir_detector.py`, pruebas de T-158 y T-161, `r04_02`, `r05_01` | cumple |
| CA-4 | `reservado_t171.py` | cumple (0, 0, 0) |
| CA-5 | `mutantes_t171.py` | ver «Regresiones» |
| CA-6 | `r04_03_sin_guias.py <carpeta> origin/develop` | cumple: 15 ficheros, ninguno difiere |
| CA-7 | suite de A, ruff, mypy | cumple: 7963 superadas; ruff 2813 (cuota 2813); mypy de A 109 (cuota 109) |
| CA-8 | lectura de INC-T126-01 (viñeta T-171) | cumple |

## Regresiones

`.docs/tickets/T-171/mutantes_t171.py`: los 55 de T-161 (M45, M46, M47 y M51 con la misma intención sobre las líneas nuevas) y
los 24 de T-171; los 79 aplican sobre el código final.

- Primera pasada (cuatro tandas en paralelo, sobre el código antes de los dos últimos cambios): **77 de 78 muertos**; vivo
  M51b. M51 lo mataba una lección con observación favorable («Las tesis sin objeciones acertaron»), que ahora retiene
  `FAVORABLE` por su cuenta. Se añadió a `test_t171_guias.py` una lección con carencia neutra y recomendación que no refuerza
  («Tesis sin segunda pasada en 5 candidatas.» / «Entregar las tesis cuanto antes»).
- Segunda pasada, sobre el código final, de los mutantes de las líneas que cambiaron después (M45b, M46b, M47b, M51b, N01–N05) y
  del nuevo N24 (objeto directo tras los complementos de alcance): **10 de 10 muertos**. Con las dos pasadas, los 79 mutantes mueren y ninguno es equivalente.

## Gate

Ligeros, desde la raíz: `corpus_integridad` (696 archivos íntegros), `nfc_check`, `secrets_scan` y `refs_vivas`, en verde.
ruff de los tres ejecutores 2813 ≤ 2813; mypy de A 109 ≤ 109 (`guias.py` limpio en los dos). `check_all.sh` completo no se pasó
(lo pide el cierre; incluye las suites de A-Forex y B, que este ticket no toca); la suite de A sí, una vez.

Comandos: los de `analisis-tecnico.md`.

## Ronda de cierre de la QA r01

Cambio: en `_otra_accion`, el verbo con un clítico es el mismo verbo («compárala» → «compara»); con los de mostrar valen todos los
de `MUESTRA`, y con los de reforzar, «responder» y «contestar» (a una objeción, R12). Lo que no es de mostrar ni de reforzar sigue
siendo segunda acción aunque lleve clítico («quédate», «entrégala», «archívala»). «Excluir» y «retirar» se quedan en `RELAJA`:
quitarlos reabre los ataques AB de la QA r04, y los ítems de H-02 que los usan ya eran falso positivo en develop.

| Comprobación | Resultado |
| --- | --- |
| `r01_01_reservado_revisor.py` (ya no reservado: se usó para corregir) | 25 de 25 ataques pasan (sin cambio); falsos positivos **5 de 18** ítems (antes 8; develop 5) y 1 de 6 lecciones |
| `r01_01`–`r04_01`, `medir_detector.py`, `reservado_t171.py` | sin cambio: 1 de 68, 0 de 52, 0 de 27, 3 de 30; 0 de 40, 0 de 48, 3 de 26, 0 de 28, 0 de 10; 0/0/0 y 0/0/1; 0, 0, 0 |
| Pruebas de T-171 (174), T-161, T-158 y `test_t126_pb26_pb48` | **951 superadas** |
| `r01_02_integracion.py` (QA r01), `r04_02`, `r05_01` | 45 superadas; fallan solo las dos `test_defecto_*` de H-17 (esperado) |
| `mutantes_t171.py` (M01–M55 y N01–N26: N25 y N26 son de esta ronda) | **81 de 81 muertos** (cuatro tandas sobre el código final), todos aplican |
| ruff · mypy de A | 2813 (cuota 2813) · 109 (cuota 109) |
