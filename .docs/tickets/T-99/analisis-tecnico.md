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
