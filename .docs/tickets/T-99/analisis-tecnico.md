# T-99 · Análisis técnico

## Motivo

La Constitución (§9, punto 17) exige corregir por número de intentos (Sharpe deflactado, probabilidad de sobreajuste), y la propuesta de J lo resume en «cada intento cuenta». El banco de medida (T-94) ya sellaba un prerregistro por ejecución, pero suelto en la carpeta de salida: no había un sitio común que contara los intentos de una misma idea ni impidiera elegir el resultado después.

## Implementación

- `.docs/scripts/registro_experimentos.py` (nuevo, solo biblioteca estándar): clase `Registro` con `prerregistrar`, `intento`, `resultado`, `experimento`, `resumen`, `adoptable` y `verificar`; `RegistroError` para todo lo que no admite; línea de órdenes (`prerregistrar`, `intento`, `resultado`, `ver`, `verificar`). Cada escritura relee y verifica la cadena antes de anexar y hace `fsync`.
- `.docs/scripts/banco_medida.py` (0.2.0): opciones `--registro`, `--experimento` y `--max-variantes`; prerregistro en el registro con la huella del prerregistro del banco; un intento por ejecución, con la huella de sus parámetros como variante; resultado «fallido» si el titular no llega a ejecutarse; `veredicto_conjunto`. Llamado desde código sin `registro`, no anota nada (lo usan las pruebas unitarias).
- `.docs/diseno/contratos/`: borrador de CT-G-24 con la forma exacta de las anotaciones (y el de CT-G-08, aparte).

## Decisiones y límites

- El registro está en el repositorio porque es del proyecto; no guarda datos de ningún usuario.
- La cadena de huellas detecta la manipulación, pero no la impide: quien tenga el fichero puede reescribirlo entero con una cadena nueva. Para eso está git (cada anotación nueva llega en un commit) y, cuando exista, la firma de SC-5.
- La regla «el intento empezó después del prerregistro» compara instantes ISO en UTC: quien pase `ahora` a mano tiene que usar el mismo formato.

## Comandos

```bash
.venv/bin/python -m pytest -q .docs/scripts/pruebas_registro_experimentos.py
```

```bash
.venv/bin/python -m pytest -q .docs/scripts/pruebas_banco_medida.py
```

```bash
.venv/bin/python -m pytest -q .docs/scripts/pruebas_borradores_contratos.py
```

## Ronda r02 (15-11-2026, QA r01 NO APTO)

Registro 0.2.0. Las tres decisiones de fondo se dejan `[PROPUESTO]` en la fila T-99 de la deuda, para que el operador las decida en T-57. Las tres son la opción más estricta que no paraliza el trabajo.

| Hallazgo | Corrección |
| --- | --- |
| H-01 (alta) | **Ancla en git:** si el registro está en el repositorio, lo que hay en HEAD tiene que ser un prefijo exacto del fichero, que solo puede crecer. Un registro borrado entero, con una versión en HEAD, también se detecta. **Sello local** (`<registro>.sello`): guarda el número y la huella de la última anotación, se escribe de forma atómica con cada anotación y detecta quitar las últimas líneas o un corte a mitad de escritura. Quien reescribe a propósito puede rehacer también el sello; contra eso solo vale el ancla de git, y por eso el registro se sube al terminar cada experimento. Al leer se comprueba además que `huella_prerregistro` sea la huella del contenido y que cada intento cite la de su prerregistro. `verificar` de un registro que no existe da código 2. |
| H-02 (alta) | **Cerrojo** (`fcntl.flock` sobre `<registro>.lock`): la lectura, la construcción y la escritura de cada anotación van dentro del cerrojo, así que dos procesos no escriben el mismo `_seq` y dos prerregistros no reciben el mismo EXP. Para dos máquinas, **un solo escritor por fichero** (cada agente con su `--registro`). Fusionar dos ramas que anotan el mismo fichero rompe la cadena, y `verificar` lo detecta: falla cerrado, no en silencio. |
| H-03 (alta) | **Regla de adopción por variante:** de cada variante cuenta su primer resultado que no sea «fallido». Si un resultado posterior de la misma variante dice otra cosa, la variante es «contradictoria» y no se adopta. `resumen()` da `por_variante` y `contradictorias`. En la línea de órdenes, `--variante` es obligatoria. |
| H-04 | Al escribir se escapan U+2028, U+2029 y U+0085, y al leer solo se parte por `\n`. Un fichero que no acaba en salto de línea falla cerrado antes de anexar, sin escribir nada. |
| H-05 | `validar_anotacion` aplica las reglas del borrador de CT-G-24 antes de escribir: forma exacta, tipos, `datos` como texto no vacío, `detalle` como objeto, `n` entero no booleano, instantes ISO con zona y EXP de hasta 9999 por año. La huella y la línea se escriben sin NaN. |
| H-06 | Al leer se valida cada línea con las mismas reglas y la semántica: un solo prerregistro por EXP, intentos correlativos, resultados de intentos que existen y uno por intento, y `dentro_del_maximo` recalculado. La línea de órdenes nunca sale con una traza: código 2 y el motivo. |
| H-07 | Los instantes se interpretan con zona y se comparan en UTC. El año del EXP es el de UTC. |
| H-08 (banco) | `--registro ""` da error y `--sin-registro` es la forma explícita de no anotar. El máximo de variantes no cambia después de prerregistrar. Escribir `prerregistro.json` está dentro del `try`, y un `RegistroError` sale como `BancoError` sin tapar el fallo original. |
| H-09 | Fechas imposibles rechazadas (`date.fromisoformat`); variante como texto no vacío normalizado a NFC; bytes que no son UTF-8 dan `RegistroError`. |
| H-10 | El uso del docstring es correcto (`--registro` delante o detrás de la orden) y el del banco dice «misma hipótesis, objeto y fuente». |
| H-11 | Los topes de 1000 variantes y 10 caracteres, y `--max-variantes` 1, figuran `[PROPUESTO]` en la fila T-99 de la deuda. |
| H-12 | `commit_limpio.sh` ejecuta todas las pruebas de `.docs/scripts` cuando el commit toca un script o un borrador de contrato. No hay commit sin ellas en verde. |

**Scripts del revisor de la r01 que siguen marcando algo, por diseño:**
- `r01_01`: los casos de truncar y recalcular sobre un fichero temporal fuera de git. El sello los detecta salvo que se rehaga también el sello, y contra eso solo vale el ancla de git.
- `r01_02`: la fusión de dos ramas. Sigue sin poder hacerse, por la regla de un solo escritor por fichero, y `verificar` la detecta.
- `r01_08`: la variante por defecto ya no existe en la línea de órdenes, y el caso siguiente cae en cascada.

**Límites:** sin git, quien reescribe el registro y el sello a la vez no se detecta. El cerrojo es de una sola máquina (POSIX).

## Ronda r03 (15-11-2026, QA r02 NO APTO)

Registro 0.3.0.

| Hallazgo | Corrección |
| --- | --- |
| H-13 (alta) | **Ancla en todo el historial de git**, no solo en HEAD. En cada commit que toca el registro (`git rev-list --full-history --parents`), el registro tiene que existir y empezar por la versión de cada padre, también en las fusiones. Por eso se detectan:<br>• un recorte subido con un commit;<br>• un veredicto cambiado, recalculado y subido;<br>• el registro sacado de HEAD;<br>• una fusión resuelta quedándose con un lado.<br>Además, el fichero de ahora tiene que empezar por la versión de HEAD. |
| H-14 | El repositorio se busca por «.git» hacia arriba, y git se ejecuta sin las variables `GIT_*`. Si el registro está en un repositorio y git no está, o un objeto no se puede leer, falla cerrado. |
| H-15 | Un intento sin resultado deja la variante «pendiente», y una variante pendiente no se adopta. Si el primer intento que no falló no tiene resultado, la variante todavía no tiene veredicto. |
| H-16 | El sello temporal se prepara antes de tocar el registro: si no se puede escribir, no se escribe nada. Si el corte llega entre la línea y el sello, se admite el sello una anotación por detrás, y la siguiente escritura lo pone al día. Quitar líneas deja el registro por detrás del sello, y eso nunca se admite. |
| H-17 | **Un registro por agente:** `registro_<agente>.jsonl`, con el agente en `RI_AGENTE` (por defecto `claude`; Astra usa `astra`). El banco usa el mismo valor por defecto. |
| H-18 | Un clon sin sello se lee si el registro es idéntico al de HEAD, porque git hace de ancla. `commit_limpio.sh` no sube un registro sin su sello. |
| H-19 | `buscar_o_prerregistrar` busca y prerregistra bajo el mismo cerrojo, y el banco lo usa. Dos bancos a la vez crean un solo experimento. |
| H-20 | Un sustituto suelto da `RegistroError`, en la huella y en la línea. Los fallos del cerrojo y del sello también salen como `RegistroError`. El motivo de un fallo del banco se escapa a UTF-8 válido. |
| H-21 | Los lectores toman un cerrojo compartido, así que no hay falsas alarmas mientras se escribe. El cerrojo espera como mucho `CERROJO_ESPERA_S`: 30 s, `[PROPUESTO]`. Un intento sobre un registro que no existe no crea carpeta ni cerrojo. |
| H-22 | Sin sello y con más de una anotación, el mensaje propone la orden `sellar`, que solo sella una vez un registro sin sello. `--detalle null` se rechaza. Las variantes en NFD de un registro de la 0.1.0 se comparan en NFC. |
| H-23 | Esta sección y `pruebas.md`. Los scripts r01 se ejecutan sentencia a sentencia con `revisores/r02_00_todos.sh`. |
| H-24 | El banco escribe en el prerregistro y en el registro las rutas relativas a la raíz. Las de fuera del repositorio van como «externa», con su nombre y una huella corta, sin las carpetas de la máquina. |
| H-12 | `commit.sh` ejecuta también las pruebas de `.docs/scripts`. El número mínimo de pruebas queda en la deuda. |

**Siguen marcando algo en los scripts del revisor, por diseño:**
- el sello una anotación por detrás se admite (H-16);
- el cerrojo espera hasta 30 s, cuando el script mira a los 5;
- la fusión de dos ramas falla cerrada (un escritor por fichero);
- la variante por defecto ya no existe en la línea de órdenes.

## Ronda r04 (15-11-2026, QA r03 NO APTO)

Registro 0.4.0.

| Hallazgo | Corrección |
| --- | --- |
| H-25 (alta) | **El sello es local y no se sube** (`.gitignore`, y `commit_limpio.sh` rechaza subirlo). Un `checkout`, un `reset --hard` o un `stash` devuelven el registro a lo subido, pero dejan el sello donde estaba, por delante: se detecta. El sello tiene que señalar una anotación de la cadena. Puede ir una por detrás (un corte entre la línea y el sello), o más atrás si el registro es exactamente el de git (un pull que trajo líneas de otra máquina). |
| H-26 | **Límite declarado `[PROPUESTO]`:** reescribir la historia subida (push forzado) o hacer un `reset` de un commit ya subido no se detecta en local. Se propone proteger `develop` contra el push forzado en GitHub, que es un ajuste del operador. |
| H-27 | Un «fallido» registrado después de que empezara otro intento de la misma variante no se salta: la variante queda `fallido_tardio` y no se adopta. |
| H-28 | `RI_AGENTE` distinto para cada sesión de un mismo agente en máquinas distintas (decisión 3, `[PROPUESTO]`). |
| H-14 | `git rev-parse --git-dir` falla cerrado si «.git» está vacío o apunta a nada, si el repositorio es de otro usuario o si la configuración está rota. Un HEAD ilegible también falla cerrado. Solo un repositorio sin commits (código 1 sin mensaje) no tiene ancla. |
| H-17 | Un `RI_AGENTE` no válido deja sin registro por defecto: `Registro()` y el banco se detienen. `AGENTS.md` (punto 9) y el índice de scripts lo explican. |
| H-29 | **Turno para el escritor:** coge «.turno» y lo retiene mientras espera, y los lectores pasan por el turno antes del cerrojo compartido. Así cuatro lectores en bucle ya no lo dejan sin entrar. Fuera de POSIX se lee, pero no se escribe. |
| H-30 | `sellar` se niega si algún prerregistro lo escribió una versión con sello (0.2.0 o posterior). El sello hecho a mano lleva `sellado_a_mano`, y `verificar` lo dice siempre. |
| H-31 | `*.jsonl.sello`, `*.jsonl.sello.tmp` y `*.jsonl.turno` están en `.gitignore`. |
| H-32 | `Registro` trabaja sobre el fichero real (`realpath`): un enlace simbólico comparte cerrojo y sello. |
| H-33 | Pruebas de `rev-list` que falla, de `os.replace` del sello que falla y de los dos casos de «.git» roto. |
| H-34 | La fila T-99 de la deuda, el índice de `.docs/README.md`, este análisis, `pruebas.md` y los docstrings de los mutantes están al día. |
| H-12 | `pruebas_scripts.sh`: todas las pruebas de `.docs/scripts` y su línea base (`linea_base_pruebas.txt`, 194), en `commit.sh` y en `commit_limpio.sh`. |
| H-18 | Ya no se sube el sello: un clon no queda bloqueado por un sello desfasado. |
| H-20 | Un registro que es un directorio, o que no se puede leer, da `RegistroError`. |
| H-24 | `experimento.json` guarda la ruta del registro relativa a la carpeta de salida. |
