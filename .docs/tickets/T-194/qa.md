# T-194 · QA

## Ronda r01 · 2026-11-24 · claude (revisor independiente; no implementó)

- **Revisado:** `wip/t194` = `d5744b7` + `4a3fd27` sobre `6045913`, en una copia de trabajo propia (`git worktree add --detach … wip/t194`).
- **Scripts del revisor:** `.docs/tickets/T-194/revisores/r01_aislamiento.sh`, `r01_mutantes_revisor.py`, `r01_ruta_no_ascii.py`.

### Reproducción

| Comprobación | Resultado |
| --- | --- |
| `.docs/scripts/pruebas_scripts.sh` | 390 superadas, línea base 390: OK |
| `pruebas_cola_astra.py` contra el `cola_astra.py` de `6045913` (`COLA_ASTRA_SCRIPT`) | 1 falla (`…_en_una_carpeta_nueva_es_aviso`) y 40 pasan: la prueba de INC-T194-01 falla sin el cambio |
| `.docs/tickets/T-194/mutantes.py` | 42 de 42 muertos |
| Mutantes del revisor (`r01_mutantes_revisor.py`) | 9: 3 muertos y 6 vivos (R03 lo mata la suite vecina, `pruebas_autor_generico.py`) → H-02 y H-03 |
| Gate de `d5744b7` (`check_all_t194_b.txt`) | 12/12, rc 0. ruff 2807, mypy A 102, A-Forex 174 y B 159, pytest A 8359, A-Forex 68 y B 176. El log no lleva el hash; termina 43 s antes del commit `d5744b7`, coherente con el gate previo al commit |
| ruff y mypy de los ficheros tocados | mypy limpio. ruff: 19 hallazgos nuevos en `pruebas_cola_astra.py` (el fichero viejo tenía 0) → H-04. `.docs/` no entra en la cuota, que no cambia |
| `python3 .docs/scripts/cola_astra.py` en el repositorio real | 0,9 s, rc 0, sin avisos. Con 3.000 ficheros sin seguimiento en una carpeta nueva: 1,5 s y 0 avisos. `.venv` (enlace) y los ignorados no salen en `--untracked-files=all` |

### Criterios de aceptación

| CA | Veredicto | Evidencia |
| --- | --- | --- |
| CA-1 | cumple | `pruebas_scripts.sh` recoge y cuenta las 41 |
| CA-2 | cumple | `r01_aislamiento.sh`: sin la cola real, con `~/.gitconfig` y XDG personales (y `commit.gpgsign true`), `.env` personal en la raíz y `GIT_AUTOR_*`, `GIT_AUTHOR_*`, `GIT_COMMITTER_*` y `GIT_DIR` exportados, las 41 pasan y la salida no contiene ni el nombre ni el correo |
| CA-3 | cumple | Las 13 comprobaciones viejas tienen prueba, con la misma condición y un mensaje igual o más estricto (expresiones ancladas al mensaje entero) |
| CA-4 | cumple | git config genérico y personal (los dos, solo nombre y solo correo; texto y `--json`, sin repetirlo), `.env` personal y el entorno, que manda. M36 a M41 muertos |
| CA-5 | cumple | 390 = 390 |
| CA-6 | cumple para `mutantes.py`; ver H-02 y H-03 para los del revisor | 42 de 42 muertos |
| CA-7 | cumple | Log del gate, 12/12 |

### Puntos pedidos

- **R8:** cumple (CA-2). Los mensajes de autor no repiten nombre ni correo (M41 muerto). Detalle menor: el caso `.env` `los_dos` solo comprueba el correo en la salida; el nombre lo cubre el caso del git config.
- **`COLA_ASTRA_SCRIPT`:** en el uso normal (sin la variable) no hace nada, y `cola_astra.py` no la lee. Pero si queda exportada en la shell, `pruebas_scripts.sh` (y por él `commit.sh` y `commit_limpio.sh`) prueba otro fichero → H-01.
- **Solape con `pruebas_autor_generico.py`:** complementario (allí `autor_efectivo` con git simulado y `common.sh`; aquí el script entero). Pero allí `test_la_cola_da_error_con_un_autor_personal` sigue leyendo la cola real, la dependencia que T-194 elimina, y su caso ya lo cubre `test_un_git_config_personal_es_error_sin_repetirlo` → H-06.
- **`--untracked-files=all`:** sin aluvión de avisos (solo se comparan las rutas de los entregables) ni coste apreciable. Defecto vecino, anterior al cambio: las rutas no ASCII → H-07.

### Hallazgos

**H-01 · baja · `COLA_ASTRA_SCRIPT` exportado hace que el gate de `.docs/scripts` pruebe otro fichero.**
- Reproducir: `r01_aislamiento.sh`, paso 3: con `cola_astra.py` roto (sin el ERROR de HECHA) y `COLA_ASTRA_SCRIPT` apuntando a una copia buena, `pruebas_scripts.sh` da 390 superadas.
- Esperado: el gate prueba siempre el script real.
- Corrección: `unset COLA_ASTRA_SCRIPT` en `pruebas_scripts.sh` antes de llamar a pytest (`mutantes.py` llama a pytest directamente y no se ve afectado).
- Regresión: una prueba que lea `pruebas_scripts.sh` y exija el `unset` antes de la línea de pytest; y `r01_aislamiento.sh` paso 3 en OK.

**H-02 · media · dos reglas que falla abierto no las mata ninguna prueba.**
- Reproducir: `r01_mutantes_revisor.py`, R01 y R02 VIVOS.
  - R01: quitar la fecha de la cola para IMPLEMENTAR (`if f["tipo"] == "QA" and fecha and fecha < FECHA_COLA:`). Un README de ticket anterior a la cola con estado EN QA o CERRADO cuenta como HECHA. Es una regla del docstring («el README del ticket cambió desde la fecha de la cola») y hay 11 filas IMPLEMENTAR pendientes en la cola real.
  - R02: un tipo desconocido cuenta como hecho (`return True, "", commit`). Es el camino de fallo cerrado de `evidencia()`.
- Esperado: alguna prueba falla.
- Corrección: dos pruebas en `pruebas_cola_astra.py`.
  - `test_implementar_con_un_readme_anterior_a_la_cola_es_error`: README con «| Estado | EN QA |» fechado `_fecha_cola(-1)`, C-08 HECHA → `ERROR C-08 … el entregable no ha cambiado desde la cola (<día>)`.
  - `test_un_tipo_desconocido_marcado_hecha_es_error`: una fila con tipo `OTRO` y su entregable en git, HECHA → `ERROR … marcada HECHA pero tipo desconocido «OTRO»`.
- Regresión: R01 y R02 pasan a `mutantes.py` y mueren.

**H-03 · baja · otros tres mutantes vivos no equivalentes.**
- R04: la fecha de la cola también para REVISION. Haría ERROR toda revisión anterior a la cola (las 7 HECHA de la cola real son REVISION). Prueba: una revisión fechada `_fecha_cola(-1)` y HECHA no da error.
- R06: el estado del ticket buscado en cualquier parte del README, sin anclar a principio de línea. Prueba: un README con «texto | Estado | CERRADO |» en medio de una línea y la fila de verdad en EN CURSO → ERROR «estado del ticket «EN CURSO»».
- R09: el error de una fila rota en el texto pero no en `--json`. Prueba: `--json` con la fila rota → `errores` contiene «C-09: la fila tiene 5 columnas y no 8».
- (R03, las comillas del `.env`, lo mata `test_un_autor_personal_en_env_se_rechaza` de la suite vecina: no es hallazgo.)
- Regresión: R04, R06 y R09 pasan a `mutantes.py` y mueren.

**H-04 · baja · `pruebas_cola_astra.py` trae 19 hallazgos de ruff; el fichero viejo, 0.**
- Reproducir: `.venv/bin/ruff check .docs/scripts/pruebas_cola_astra.py` → 10 FURB167 (`re.M`) y 9 RUF059 (`rc` sin usar).
- Corrección: `re.MULTILINE` y `_` en los desempaquetados donde no se usa `rc` (o comprobar `rc` donde tenga sentido).
- Regresión: la orden anterior sin hallazgos, anotada en `pruebas.md`.

**H-05 · baja · documentación del ticket desfasada tras la r01b.**
- `pruebas.md`: la tabla de criterios dice 389, «41 mutantes, 41 muertos» y la prueba de INC-T194-01 como `xfail`; `analisis-tecnico.md` dice 389 y 41 mutantes; `handoff.md` no tiene la entrega r01b.
- Corrección: 390, 42 de 42 y la prueba en verde en la tabla y en el análisis; entrada r01b en el traspaso.
- Regresión: `grep -n "389\|41 muertos\|xfail" .docs/tickets/T-194/*.md` solo devuelve las líneas históricas de la r01, marcadas como tales.

**H-06 · baja · `pruebas_autor_generico.py` sigue dependiendo de la cola real.**
- Reproducir: `r01_aislamiento.sh`, paso 2: sin la cola real, `test_la_cola_da_error_con_un_autor_personal` falla (FileNotFoundError); las 41 de T-194 pasan.
- Esperado: ninguna prueba de `.docs/scripts` lee la cola real (el objetivo de T-194).
- Corrección (fuera del alcance del plan, que no toca `pruebas_autor_generico.py`; la decide el coordinador): quitar esa prueba, cubierta por `test_un_git_config_personal_es_error_sin_repetirlo`, o darle una cola mínima en `tmp_path` en vez de `RAIZ`. Si se quita, la línea base baja una prueba y hay que decirlo.
- Regresión: `r01_aislamiento.sh` paso 2 en OK.

**H-07 · baja · un entregable con una ruta no ASCII y cambios sin commit no avisa (anterior al cambio).**
- Reproducir: `.venv/bin/python -I .docs/tickets/T-194/revisores/r01_ruta_no_ascii.py` → FALLA. `git status --porcelain` entrecomilla y escapa la ruta (`core.quotePath`), y la comparación con la de la fila no casa. La cola real no tiene hoy rutas así, pero el repositorio está lleno de nombres con tildes.
- Corrección: `git -c core.quotePath=false status --porcelain --untracked-files=all` en `cola_astra.py` (o `-z` y partir por NUL). Es un cambio de `cola_astra.py` más allá de INC-T194-01: necesita la misma autorización.
- Regresión: una prueba con una fila cuyo entregable es `.docs/diseño/…/revisión.md` (el caso de `r01_ruta_no_ascii.py`) y un mutante que quite la opción.

### Veredicto

**NO APTO** (H-02 media; H-01 y H-03 a H-07 bajas). Tras la corrección, el revisor vuelve a pasar `revisores/r01_*` y `mutantes.py`.

## Ronda r02 · 2026-11-24 · claude (el mismo revisor)

- **Revisado:** `5f77f052` (r02 sobre `4a3fd27`), en la misma copia de trabajo. El commit trae mi `qa.md` r01 y mis `revisores/` sin cambios: los comparé con mi copia y no hay diferencias.
- **Decisiones del coordinador:** H-06, la prueba se queda con una cola propia en `tmp_path`; H-07, se autoriza `core.quotePath=false` en `cola_astra.py`.

### Reproducción

| Comprobación | Resultado |
| --- | --- |
| `.docs/scripts/pruebas_scripts.sh` | 399 superadas, línea base 399: OK |
| `revisores/r01_aislamiento.sh` | rc 0. Paso 2: `pruebas_autor_generico.py` pasa sin la cola real (12) y las 50 de la cola, con un usuario personal en todas partes, pasan sin que la salida lo contenga. Paso 3: con `COLA_ASTRA_SCRIPT` exportado y el script real roto, `pruebas_scripts.sh` falla, como debe |
| `revisores/r01_ruta_no_ascii.py` | OK: avisa con una ruta no ASCII |
| `revisores/r01_mutantes_revisor.py` | 9 de 9 muertos |
| `.docs/tickets/T-194/mutantes.py` | 49 de 49 muertos |
| ruff sobre `pruebas_cola_astra.py`, `pruebas_autor_generico.py` y `cola_astra.py` | sin hallazgos |
| `python3 .docs/scripts/cola_astra.py` en el repositorio real | rc 0, sin avisos; el árbol queda limpio tras todos los scripts |

### Hallazgos de la r01

| Hallazgo | Corrección | Prueba de regresión | Verificado |
| --- | --- | --- | --- |
| H-01 (baja) | `unset COLA_ASTRA_SCRIPT` en `pruebas_scripts.sh` antes de pytest | `test_h01_pruebas_scripts_quita_cola_astra_script_antes_de_pytest`; `r01_aislamiento.sh` paso 3 | cerrado |
| H-02 (media) | dos pruebas nuevas | `test_h02_implementar_con_un_readme_anterior_a_la_cola_es_error`, `test_h02_un_tipo_desconocido_marcado_hecha_es_error`; M43 y M44 (R01 y R02) muertos | cerrado |
| H-03 (baja) | tres pruebas, y una más para R03 | `test_h03_…` (cuatro); M45, M46, M47 y M49 muertos | cerrado |
| H-04 (baja) | `re.MULTILINE` y `_` | ruff en 0 | cerrado |
| H-05 (baja) | `pruebas.md`, `analisis-tecnico.md`, `handoff.md` y README al día (399, 49 de 49); lo de la r01 y la r01b queda marcado como historia | lectura y `grep` | cerrado |
| H-06 (baja) | la prueba usa su propia cola en `tmp_path` y un `git` simulado del todo, sin `_git_original` | `r01_aislamiento.sh` paso 2 | cerrado |
| H-07 (baja) | `-c core.quotePath=false` en el `git status` de `cola_astra.py` (autorizado) | `test_h07_…` (con commit y nuevo); M48 muerto; `r01_ruta_no_ascii.py` | cerrado |

### Regresiones

- Ninguna. Las 41 pruebas de la r01 siguen y no se ha debilitado ninguna: solo cambian `re.M` por `re.MULTILINE` y `rc` por `_` donde no se usaba. Los 42 mutantes de antes siguen muertos.
- `core.quotePath=false` solo cambia cómo escribe git las rutas no ASCII. Las que llevan comillas, barras invertidas o caracteres de control siguen saliendo entrecomilladas, pero no las hay en la cola ni es razonable que las haya. No es un hallazgo.

### Veredicto

**APTO**. Los siete hallazgos de la r01 están cerrados, cada uno con su prueba, y no hay hallazgos nuevos. No hace falta ronda de cierre.
