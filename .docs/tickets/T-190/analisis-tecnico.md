# T-190 · Análisis técnico

## Causa raíz o motivo

- **H-01.** En T-152 medí el umbral con tramos de precio que quedaban enteros a un lado del 2 % de q/p. Una serie que **cruza** el 2 % se desplaza a medias: solo sus precios por debajo del umbral. Su resultado depende del umbral, así que un umbral más alto no era equivalente.
- **H-02.** `cadena_a_b.py` miraba si los ficheros se leían y tenían forma, pero no:
  - lo que hace fallar a `json` y a `yaml` por recursión;
  - un `opp_id` que el esquema admite y que no cabe en un nombre de fichero;
  - un sustituto suelto, que `json.loads` admite y que UTF-8 no codifica. `write_text` abría el fichero antes de fallar y lo dejaba vacío.
- **H-03.** El rebase sobre T-168 cambió el hash del primer commit de T-152 (`4e39324` → `32af7fe`), y los textos de la primera versión no se repasaron todos al cambiar el umbral.

## Evidencia

Los scripts del revisor de T-152, en `.docs/tickets/T-152/revisores/`:
- `r01_05_semillas_qa.py`: las semillas en que el 2 % y un umbral mayor difieren;
- `r01_03_formas_qa.py`: las formas de fichero que dan traza;
- `r01_02_borde_qa.py`: la resolución de la prueba del borde.

## Implementación

**Archivos:**
- `bloque_a/11_Ejecutor/tests/test_t150.py`:
  - la prueba nueva de H-01 y el docstring corregido de la del borde, con el tramo de 1,82 a 2,00 %;
  - ocho pruebas `test_t190_h02_*`.
- `bloque_a/11_Ejecutor/bloque_a/motor/frontera_b.py`: solo comentarios. El de T-150 decía q/p ≤ `tol`; ahora dice 2·`tol` y menciona la serie que cruza el umbral. El código no cambia.
- `.docs/scripts/cadena_a_b.py`:
  - `_json`: los escapes de JSON si el texto no se codifica en UTF-8;
  - `_escribir`, atómico: un temporal y `os.replace`;
  - `_no_escrita`, `PETICION_NO_ESCRITA` en `no_enviadas` y en la sonda;
  - `RecursionError` en las dos lecturas.
- `.docs/tickets/T-152/`: `mutantes.py` (U2 ya no es equivalente; nuevos U5 y U6) y las notas de corrección en README, análisis y pruebas.
- `docs/incidencias.md`: rondas T-190 de INC-T127-01 (el límite de la serie que cruza el umbral, y que el límite de los pasos grandes depende del par) y de INC-T142-01.

**Decisiones:**
- **La serie que cruza el 2 % se declara, no se arregla.** Arreglarla pediría elegir el desplazamiento por tramo de precios o desplazar también por encima del umbral, y eso es lo que tomaba por copias el monetario a 1,00 (F3 de T-150).
  - El límite **no** falla cerrado: una copia sin agrupar cuenta como serie distinta, como pasaba con todas las truncadas antes de T-150.
  - Las pruebas fijan las dos caras, con semillas concretas.
- **El nombre del fichero de la petición sigue siendo el `opp_id`.** Cambiarlo cambiaría lo que espera quien lea la carpeta de trabajo. Lo que no se puede escribir queda anotado y no se envía. No se usa ningún límite de longitud escrito a mano: lo da el sistema de ficheros.
- **Un sustituto se conserva con su escape** (`\ud800`) en lugar de sustituirse: el resumen dice lo que había.
- **O-04 no se toca.** El detalle de `ENTRADA_B_INVALIDA` copia el valor ya limpio de R8, por diseño de T-149, y no es un hallazgo.

## Comandos para probarlo

```bash
cd bloque_a/11_Ejecutor && ../../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_t150.py -k "t190 or t152"
.venv/bin/python -I .docs/tickets/T-152/revisores/r01_03_formas_qa.py <carpeta temporal>
.venv/bin/python -I .docs/tickets/T-152/revisores/r01_05_semillas_qa.py
.venv/bin/python .docs/tickets/T-190/mutantes.py <copia «t147_mut»>
.venv/bin/python .docs/tickets/T-152/mutantes.py <copia «t147_mut»>
```
