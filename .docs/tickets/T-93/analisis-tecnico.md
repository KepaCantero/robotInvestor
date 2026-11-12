# T-93 · Análisis técnico

## Causa raíz

- **H-32:** `secretos_en_texto` buscaba también en una variante del texto con los escapes de JSON sustituidos, pero solo `\n`, `\t`, `\r` y `\/`. Con otro escape delante (`«`, `%3D`, `\xa0`…), la última cifra o letra del escape quedaba pegada a «sk-» y el candidato no empezaba en un límite de palabra. `contenido_sensible` no entraba en los `set`.
- **H-33:** `RE_TRAMO_TEXTO` solo admitía los códigos de periodo en mayúsculas («Q3», «FY2023»), siglas de hasta 6 letras y números de hasta 4 cifras; las URL van en minúsculas y llevan códigos de cotización y fechas.
- **H-34:** el apartado de la línea parcial estaba dentro de `if not legado`.
- **H-35:** `read_text` decodificaba todo el fichero antes de separar la última línea, y un corte a mitad de un carácter lanzaba `UnicodeDecodeError`.
- **H-37:** `_instante` solo validaba las cadenas; un número pasaba a `pd.Timestamp` como nanosegundos y un `date` como medianoche. En `enviar`, un `False` se tomaba por «sin plazo».
- **H-38:** `vencer()` releía el plazo con la regla estricta de la r04 y lanzaba con lo guardado por develop.

## Evidencia

Antes del cambio: `r04_01` 11 fallos, `r04_02` 2 y `r04_03` 4 (como la QA r04). Después: 0, 0 y 0. Comandos en `pruebas.md`.

## Implementación

- `bloque_a/contratos.py`: `RE_ESCAPES` (escapes que se sustituyen en la segunda variante); `RE_TRAMO_TEXTO` ampliado; `_tramo_texto` (con `RE_FECHA_8` y la comprobación de que la fecha existe y un tope de 30 caracteres por tramo).
- `bloque_a/llm.py`: `contenido_sensible` recorre `set` y `frozenset`; anotaciones de tipos modernizadas con `ruff --fix` (UP006, UP045, UP035, UP037), sin cambio de comportamiento.
- `bloque_a/almacen.py`: lectura en bytes y separación de la última línea antes de decodificar; apartado de la línea parcial también en modo `legado`; el tipo de `RelojSistema.fecha` es `date` (un error de mypy menos).
- `bloque_a/interfaz_broker.py`: `_instante` rechaza números y booleanos y convierte un `date` en su texto; `enviar` solo toma «sin plazo» con `None` o «»; `vencer` anota una incidencia DATOS y vence la consulta si su plazo guardado no se lee.
- `tests/test_t93_hallazgos.py`: 37 pruebas.
- `tools/cuotas.txt`: ruff 3019 (antes 3072), mypy de A 114 (antes 115), línea base de A 476 (antes 439).

## Límites (H-36)

R8 sigue sin detectar las colas hechas solo de tramos con forma de texto: el 2,25 % de 5 grupos de 4 mayúsculas y cifras (estilo licencia), el 0,35 % de 4 grupos base32 de 7 en minúsculas y todos los grupos de 8 letras minúsculas. Ningún proveedor conocido usa esas formas; es el precio aceptado de la regla de T-92 (todo candidato es clave salvo que parezca texto corriente). T-93 no lo empeora: `r04_01` caso 1 da las mismas cifras que en la r04.

## Comandos

```bash
.venv/bin/python -I .docs/tickets/T-92/revisores/r04_01_r8_regla_texto.py bloque_a/11_Ejecutor
```

```bash
.venv/bin/python -I .docs/tickets/T-92/revisores/r04_02_almacen_corte.py bloque_a/11_Ejecutor
```

```bash
.venv/bin/python -I .docs/tickets/T-92/revisores/r04_03_plazos_iso.py bloque_a/11_Ejecutor
```

```bash
cd bloque_a/11_Ejecutor && ../../.venv/bin/pytest -q tests/test_t93_hallazgos.py
```
