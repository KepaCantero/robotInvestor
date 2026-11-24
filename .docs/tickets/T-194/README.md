# T-194 · Scripts de `.docs/`: `pruebas_cola_astra.py` a pytest, con una cola de prueba propia

| Campo | Valor |
| --- | --- |
| Estado | CERRADO (24-11-2026, QA r02 APTO sin hallazgos abiertos) |
| Pieza | scripts de `.docs/`: `.docs/scripts/pruebas_cola_astra.py` (reescrito) y `.docs/scripts/linea_base_pruebas.txt`; dos opciones de git en `.docs/scripts/cola_astra.py` (r01b, INC-T194-01; r02, H-07); en la r02, una línea de `.docs/scripts/pruebas_scripts.sh` (H-01) y una prueba de `.docs/scripts/pruebas_autor_generico.py` (H-06) |
| Planifica · implementa · QA | claude · claude · el otro agente o un revisor nuevo |
| Aprobación del operador | no necesaria (ticket de la deuda técnica abierto el 24-11-2026 al añadir el autor genérico) |
| Deuda técnica | T-194 en `sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md` |

## Objetivo

Que las pruebas de `cola_astra.py` las ejecute `pruebas_scripts.sh` (hoy no tienen funciones `test_` y nadie las corre) y que no dependan de la cola real, para que no vuelvan a desfasarse cuando cambie: desde que la cola empieza por C-38, 5 de sus 13 comprobaciones fallan porque esperan C-01 la primera.

## Alcance

- **Entra:**
  - `pruebas_cola_astra.py` pasa a pytest. Cada prueba crea un repositorio git temporal (`git init` en `tmp_path`), copia allí `cola_astra.py` y escribe una cola mínima de 8 filas (seis REVISION, una QA y una IMPLEMENTAR). Ni lee la cola real ni toca el árbol de trabajo.
  - Las 13 comprobaciones de antes: cola limpia y la siguiente; HECHA sin entregable; borrador; HECHA con entregable; entregable sin marcar; la sección del rediseño de B; EN CURSO viejo y la siguiente; dos EN CURSO; cambios sin commit; QA anterior a la cola; RETIRADA con entregable; RETIRADA no es la siguiente y se cuenta; estado desconocido.
  - Los límites y casos que les faltaban: el día 3 y el día 4 de EN CURSO, EN CURSO sin fecha, QA del mismo día de la cola, el último veredicto, la plantilla sin rellenar, IMPLEMENTAR por el estado del ticket, el entregable fuera de git, una fila rota, `--json` y nada pendiente.
  - Las del autor genérico que no cubre `pruebas_autor_generico.py`, que prueba `autor_efectivo` con un git simulado y `main` con el entorno. Aquí se prueba el script entero sobre un repositorio de verdad: su git config genérico o personal (también en `--json`), un `.env` personal en la raíz, y el entorno, que manda sobre el git config.
  - Mutantes de `cola_astra.py` en `.docs/tickets/T-194/mutantes.py`, cargados por `COLA_ASTRA_SCRIPT`.
  - La línea base de `.docs/scripts/linea_base_pruebas.txt` sube de 349 a 399 (390 en la r01b).
- **No entra:**
  - Cambiar `cola_astra.py` más allá de las dos opciones de `git status`, las dos autorizadas por el coordinador: `--untracked-files=all` (r01b, INC-T194-01) y `-c core.quotePath=false` (r02, H-07).
  - Tocar la cola real (`.docs/tickets/_relevo/cola_astra.md`).
  - Tocar `pruebas_autor_generico.py`, salvo darle su propia cola en `tmp_path` a una prueba (r02, H-06, autorizado por el coordinador).

## Diseño

- **Contratos y esquemas:** ninguno.
- **Estado persistido:** ninguno. Cada prueba trabaja en su `tmp_path`.
- **Números:** ninguno nuevo.
  - `FECHA_COLA` se lee del script, porque es la fecha de la cola y cambia con ella. Las pruebas fechan los commits un día antes o el mismo día con `GIT_COMMITTER_DATE`.
  - Los 3 días de EN CURSO y la sección «Rediseño» de C-02 se fijan en la prueba, porque son la regla documentada (docstring del script). Una prueba ata `DIAS_EN_CURSO` al docstring.
- **Aislamiento:**
  - El script se ejecuta como lo hace Astra, con `python -I .docs/scripts/cola_astra.py` desde la raíz del repositorio temporal.
  - El entorno va sin `GIT_*` ni `GIT_AUTOR_*`, con `GIT_CONFIG_GLOBAL=/dev/null` y `GIT_CONFIG_NOSYSTEM=1`. Así no cuentan el git config ni el `.env` de quien ejecuta las pruebas.
- **Cómo falla cerrado:** cada orden git del montaje comprueba su código de salida. Una salida por stderr del script hace fallar la prueba.

## Riesgos

| Riesgo | Consecuencia | Mitigación |
| --- | --- | --- |
| Las pruebas dependen de `date.today()` (EN CURSO) | Un cambio de día a medianoche entre la prueba y el script | Los límites se calculan desde hoy; el margen es de un día entero |
| Un git del sistema con `commit.gpgsign` o un hook global | Commits que fallan | `GIT_CONFIG_GLOBAL=/dev/null`, `GIT_CONFIG_NOSYSTEM=1` y `commit.gpgsign false` en el repo de prueba |
| Tiempo de `pruebas_scripts.sh` | Más lento | 50 pruebas en unos 20 s |

## Criterios de aceptación (binarios)

1. CA-1: `pruebas_cola_astra.py` tiene funciones `test_` y `pruebas_scripts.sh` las ejecuta y las cuenta.
2. CA-2: ninguna prueba lee la cola real ni toca el árbol de trabajo. Cambiar la cola real no cambia el resultado.
3. CA-3: las 13 comprobaciones de antes siguen. Cada una tiene al menos una prueba, la misma condición y el mismo mensaje.
4. CA-4: el autor genérico se prueba en el script entero: git config genérico y personal (texto y `--json`, sin repetir el autor), `.env` personal y el entorno, que manda.
5. CA-5: la línea base de `.docs/scripts/linea_base_pruebas.txt` es el número nuevo de pruebas (399) y `pruebas_scripts.sh` pasa.
6. CA-6: todos los mutantes de `.docs/tickets/T-194/mutantes.py` mueren o quedan explicados como equivalentes.
7. CA-7: `./tools/check_all.sh` en verde (12/12). Las cuotas no suben.

## Plan de pruebas

| Prueba | Tipo | Criterio |
| --- | --- | --- |
| `pruebas_scripts.sh` cuenta 399 | integración | CA-1, CA-5 |
| El repositorio temporal; las pruebas pasan igual con la cola real cambiada | regresión | CA-2 |
| Una o varias por comprobación (tabla en `pruebas.md`) | nominal, límite, fallo cerrado | CA-3 |
| Cuatro del autor (tabla en `pruebas.md`) | fallo cerrado | CA-4 |
| `.docs/tickets/T-194/mutantes.py` | mutación | CA-6 |
| `./tools/check_all.sh` | gate | CA-7 |

## Scripts

- Usa `.docs/scripts/pruebas_scripts.sh` y `./tools/check_all.sh`.
- Crea `.docs/tickets/T-194/mutantes.py`.

## Registro

- 2026-11-24 · ABIERTO · fila en la deuda técnica, al añadir `pruebas_autor_generico.py`.
- 2026-11-24 · PLANIFICADO · claude.
- 2026-11-24 · EN QA (r01) · claude (histórico): 41 pruebas, 40 superadas y 1 marcada como fallo esperado (INC-T194-01); 41 mutantes muertos; línea base de 349 a 389.
- 2026-11-24 · EN QA (r01b) · claude: corrige INC-T194-01 (autorizado por el coordinador): `--untracked-files=all` en `cola_astra.py`, la prueba deja de ser `xfail`, línea base 390 y mutante M42 muerto (42 de 42).
- 2026-11-24 · QA r01 · NO APTO: H-02 media; H-01 y H-03 a H-07 bajas (`qa.md`).
- 2026-11-24 · EN QA (r02: QA r01 NO APTO) · claude: los siete hallazgos corregidos, cada uno con su prueba de regresión. 50 pruebas en `pruebas_cola_astra.py`, línea base 399, 49 mutantes muertos (con R01, R02, R03, R04, R06 y R09 del revisor) y `revisores/` en verde.
- 2026-11-24 · QA r02 · APTO sin hallazgos nuevos: los siete de la r01 cerrados, cada uno con su prueba (`qa.md`).
- 2026-11-24 · CERRADO · claude: integrado en `develop` con `commit_limpio.sh`.
