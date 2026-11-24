# T-194 · Análisis técnico

## Causa raíz o motivo

- `pruebas_scripts.sh` ejecuta `pytest .docs/scripts/pruebas_*.py`.
- El antiguo `pruebas_cola_astra.py` era un script con `main()` y `chk()`, sin funciones `test_`. pytest lo importaba y recogía 0 pruebas, así que nadie lo ejecutaba.
- Además trabajaba sobre la cola real y daba por hecho su contenido: C-01 la primera, C-02 la revisión de B y C-28 una QA. Desde que la cola empieza por C-38, 5 de sus 13 comprobaciones fallaban.

## Evidencia

- Antes: `pytest --collect-only -q .docs/scripts/pruebas_cola_astra.py` → 0. `pruebas_scripts.sh` → 349, ninguna de la cola.
- Ahora (r02): 50 recogidas y superadas. `pruebas_scripts.sh` → 399 de 399.
- Independencia de la cola real: `revisores/r01_aislamiento.sh` en verde. Con la cola real fuera del árbol y un autor personal en el git config, en `.env` y en `GIT_*`, pasan las 50 y las 12 de `pruebas_autor_generico.py`.

## Implementación

- **Archivos cambiados y por qué:**
  - `.docs/scripts/pruebas_cola_astra.py`: reescrito para pytest, con la clase `Repo` y la fixture `repo`. Cada prueba tiene un repositorio git propio en `tmp_path` y una cola de 8 filas (`FILAS`), más las filas que añada (`_fila`). `COLA_ASTRA_SCRIPT` permite probar otra versión del script, la de los mutantes.
  - `.docs/scripts/cola_astra.py`: solo cambia la orden de `git status`, que pasa a ser `git -C RAIZ -c core.quotePath=false status --porcelain --untracked-files=all`.
    - r01b, INC-T194-01: un entregable nuevo en una carpeta nueva ya no se resume en `?? carpeta/`.
    - r02, H-07: una ruta no ASCII ya no sale entrecomillada ni escapada.
    - Las dos opciones las autorizó el coordinador.
  - `.docs/scripts/pruebas_scripts.sh` (r02, H-01): `unset COLA_ASTRA_SCRIPT` antes de pytest. El gate prueba siempre el script real; `mutantes.py` llama a pytest directamente.
  - `.docs/scripts/pruebas_autor_generico.py` (r02, H-06, autorizado por el coordinador): `test_la_cola_da_error_con_un_autor_personal` escribe su propia cola en `tmp_path` y simula todo `git`, en lugar de leer la cola real. Sale `_git_original`, que ya no se usaba.
  - `.docs/scripts/linea_base_pruebas.txt`: de 349 a 399.
  - `.docs/README.md`: la fila de `cola_astra.py`.
  - `docs/incidencias.md`: INC-T194-01, `[RESUELTO en T-194]`.
  - La fila T-194 de la deuda técnica.
  - `.docs/tickets/T-194/mutantes.py`: 49 mutantes.
- **Decisiones:**
  - Un repositorio temporal con `git init` en lugar de un worktree del repositorio real.
  - `FECHA_COLA` se lee del script. `DIAS_EN_CURSO` (3) y `REQUISITOS` (C-02, «Rediseño») se fijan en la prueba, porque son la regla.
  - Del autor genérico solo se prueba aquí lo que no cubre `pruebas_autor_generico.py`.
- **Ronda r02 (QA r01 NO APTO):** los siete hallazgos están corregidos con la corrección del `qa.md`. La tabla hallazgo → prueba → mutante está en `pruebas.md`.
  - H-01: el `unset`.
  - H-02: dos pruebas.
  - H-03: tres pruebas, y una cuarta para R03. El revisor no lo contaba como hallazgo porque lo mata la suite vecina, pero su script lo da como vivo contra esta.
  - H-04: ruff a 0.
  - H-05: esta documentación.
  - H-06: la cola propia en `tmp_path`.
  - H-07: `core.quotePath=false`.
- **Límites conocidos:**
  - Las pruebas de EN CURSO dependen de `date.today()`.
  - Una ruta con salto de línea o un renombrado (`R  a -> b`) en `git status` no se comparan bien. No hay rutas así en la cola, y queda fuera del alcance.
- **Comandos exactos para probarlo (desde la raíz):**
  - `.venv/bin/python -m pytest -q -p no:cacheprovider .docs/scripts/pruebas_cola_astra.py`
  - `.docs/scripts/pruebas_scripts.sh`
  - `.venv/bin/python .docs/tickets/T-194/mutantes.py` (unos 8 min)
  - `bash .docs/tickets/T-194/revisores/r01_aislamiento.sh`, con el árbol sin cambios en `cola_astra.py`
  - `.venv/bin/python -I .docs/tickets/T-194/revisores/r01_ruta_no_ascii.py`
  - `.venv/bin/python .docs/tickets/T-194/revisores/r01_mutantes_revisor.py`
  - `.venv/bin/ruff check .docs/scripts/pruebas_cola_astra.py .docs/scripts/pruebas_autor_generico.py .docs/scripts/cola_astra.py .docs/tickets/T-194/mutantes.py`

## Historia

- **r01:**
  - Sin cambios en `cola_astra.py`. INC-T194-01 quedó `[PROPUESTO]`, con su prueba marcada `xfail` estricta.
  - 41 pruebas, línea base 389, 41 mutantes.
- **r01b:** `--untracked-files=all`. Línea base 390, 42 mutantes.
