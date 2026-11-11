# T-96 · Entorno reproducible con versiones fijadas

| Campo | Valor |
| --- | --- |
| Estado | EN QA |
| Pieza | `tools/requisitos_entorno.txt` y `.docs/scripts/preparar_entorno.sh` (fuera de los bloques y del marco común) |
| Planifica · implementa · QA | claude · claude · astra |
| Aprobación del operador | aprobada el 2026-11-11: «haz el punto 1 y 2» (punto 2: fijar las versiones del entorno) |
| Deuda técnica | T-96 en `sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md` |

## Objetivo

Que un clon nuevo del repositorio cree el mismo `.venv` con un solo comando y pase el gate sin tocar nada. El 11-11-2026, en un clon nuevo, `arch` 9.0.0 sumó dos errores de mypy en A y otros dos en A-Forex, y el gate falló sin que cambiara el código.

## Alcance

- Entra:
  - `tools/requisitos_entorno.txt`: fichero de restricciones de pip con la versión exacta de cada paquete instalado en el `.venv` con el que el gate pasó 12/12 (Python 3.12);
  - `.docs/scripts/preparar_entorno.sh`: crea `.venv` con Python 3.12 si no existe, instala los tres ejecutores en modo editable y las herramientas y opcionales con esas restricciones, y comprueba que lo instalado coincide; con `--comprobar` solo compara;
  - `CLAUDE.md` (sección «Comandos»), la tabla de scripts de `.docs/README.md` y las lecciones del relevo apuntan al script.
- No entra:
  - cambiar código de los bloques, del marco común, de la Constitución ni de `tools/check_all.sh`;
  - fijar versiones en los `pyproject.toml` de los bloques (son parte del corpus entregado);
  - `pre-commit` (no lo usa el gate; se instala aparte, como hasta ahora).

## Diseño

- Contratos: ninguno. Estado persistido: ninguno.
- Números: solo versiones de paquetes, copiadas de `pip freeze` del entorno verificado; ningún parámetro del sistema.
- Cómo falla cerrado: si falta Python 3.12, si pip no puede instalar una versión fijada o si lo instalado no coincide con el fichero, el script termina con error y dice qué paquete difiere. Nunca actualiza versiones por su cuenta.
- Para cambiar una versión: se edita el fichero, se recrea el entorno con el script y se pasa el gate completo en el mismo commit.

## Riesgos

| Riesgo | Consecuencia | Mitigación |
| --- | --- | --- |
| Una versión fijada desaparece del registro de paquetes | El script no puede instalar | Falla cerrado con el nombre del paquete; se cambia la versión con el gate completo |
| Versiones viejas con fallos de seguridad | Dependencias desactualizadas | Se actualizan a propósito, con el gate, no por accidente |
| El fichero se desfasa del entorno real | Clones distintos entre sí | `--comprobar` compara lo instalado con el fichero |

## Criterios de aceptación (binarios)

1. CA-1: con el `.venv` borrado, `.docs/scripts/preparar_entorno.sh` crea uno nuevo sin intervención y termina con código 0.
2. CA-2: en ese entorno, `./tools/check_all.sh` da 12/12, con las líneas base A 439, A-Forex 68 y B 176.
3. CA-3: `preparar_entorno.sh --comprobar` da 0 en ese entorno y distinto de 0 si se instala otra versión de un paquete fijado (por ejemplo, `arch` 9.0.0), nombrando el paquete.
4. CA-4: el script falla con mensaje claro si no encuentra Python 3.12.
5. CA-5: no cambia ningún fichero de los bloques, del marco común, de la Constitución ni de `tools/check_all.sh`.

## Plan de pruebas

| Prueba | Tipo | Criterio |
| --- | --- | --- |
| Entorno desde cero | Integración | CA-1 y CA-2 |
| Desfase de una versión | Fallo cerrado | CA-3 |
| Sin Python 3.12 (variable `PYTHON_ENTORNO` apuntando a un ejecutable inexistente) | Fallo cerrado | CA-4 |
| `git diff --stat` | Regresión | CA-5 |
