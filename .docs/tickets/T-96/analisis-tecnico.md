# T-96 · Análisis técnico

## Causa raíz o motivo

Ningún fichero del repositorio fijaba las versiones del entorno: `CLAUDE.md` mandaba instalar `arch openpyxl python-docx` sin versión, y las herramientas del gate (ruff, mypy, pytest) se instalaban a mano. Las cuotas del gate son recuentos de hallazgos de ruff y mypy, y esos recuentos dependen de la versión de la herramienta y de los tipos que traen las bibliotecas. Un clon nuevo instalaba lo último disponible y podía fallar el gate sin cambiar el código.

## Evidencia

El 11-11-2026, en un clon nuevo, el primer intento de commit de la enmienda 5, parte 2 (que solo tocaba `.md`) falló en dos gates:

- `mypy bloque_a: 117 > cuota 115` y `mypy bloque_a_forex: 176 > cuota 174`.
- Los cuatro errores de más eran los mismos dos en cada paquete, en `motor/operaciones.py`: `arch_model(vol="GARCH", mean="Constant")` frente a los literales en minúsculas que exigen los tipos de `arch` 9.0.0.
- Con `arch` 8.0.0 los recuentos vuelven a 115 y 174. Con mypy 1.19 y 1.20 dan otros valores (A 124 y 121, A-Forex 184 y 181, B 164); con mypy 2.2, 2.3 y 2.4 coinciden con las cuotas una vez fijado `arch`.

## Implementación

- `tools/requisitos_entorno.txt` (nuevo): fichero de restricciones de pip con las 49 versiones exactas de `pip freeze --exclude-editable` del `.venv` con el que el gate pasó 12/12 (Python 3.12.3). Lleva en su cabecera cómo se cambia.
- `.docs/scripts/preparar_entorno.sh` (nuevo):
  - sin argumentos, crea `.venv` si no existe (con `PYTHON_ENTORNO`, `python3.12` del PATH o `~/.local/bin/python3.12`; exige 3.12) e instala, con `-c tools/requisitos_entorno.txt`, los tres ejecutores en modo editable y `arch openpyxl python-docx ruff mypy pytest pyyaml jsonschema`;
  - después, y con `--comprobar`, compara lo instalado con el fichero: falla y nombra cada paquete que falte o tenga otra versión; los instalados sin fijar solo dan aviso.
- `CLAUDE.md` («Comandos»), la tabla de scripts de `.docs/README.md` y las lecciones del relevo del 11-11 apuntan al script.
- Decisiones y desviaciones:
  - se fijan también las dependencias indirectas (numpy, pandas, scipy…), porque también cambian los tipos que ve mypy;
  - el fichero vive en `tools/` junto a las cuotas que protege, y no en los `pyproject.toml` de los bloques, que son corpus entregado;
  - no se toca `tools/check_all.sh`: el gate no comprueba las versiones por su cuenta (se puede añadir en otra tarea si se quiere que lo haga).
- Límites conocidos:
  - `pre-commit` no está fijado (no lo usa el gate);
  - si una versión fijada desaparece del registro de paquetes, el script falla y hay que cambiarla a mano, con el gate completo;
  - Python 3.12 lo pone el sistema: el script solo comprueba la versión menor.
- Comandos exactos para probarlo:

```bash
mv .venv /tmp/venv_previo
```

```bash
.docs/scripts/preparar_entorno.sh
```

```bash
./tools/check_all.sh
```

```bash
.venv/bin/pip install -q "arch==9.0.0" && .docs/scripts/preparar_entorno.sh --comprobar
```
