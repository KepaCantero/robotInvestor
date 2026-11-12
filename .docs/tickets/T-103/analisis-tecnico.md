# T-103 · Análisis técnico

## Causa raíz o motivo

- **H-40.** La alternativa `\\[ntr/bf"\\]` de `RE_ESCAPES` (T-93) consumía la barra escapada de un escape doble (`\\n`) y dejaba la «n» pegada a «sk-»; la búsqueda de candidatos exige que no haya letra ni cifra delante, así que la clave dejaba de verse. Antes de T-93 la expresión no tenía esa alternativa y el caso se veía.
- **H-41.** La ampliación de `RE_TRAMO_TEXTO` de T-93 aceptó `[0-9]{5,7}` (códigos de cotización) como tramo de texto, y una cola hecha solo de esos tramos pasó a tener forma de texto.
- **H-42.** `escribir` añadía el registro sin mirar si el fichero acababa en «\n»; si el último registro estaba entero pero sin salto (corte justo antes del salto o migración), las dos líneas se pegaban.
- **H-43.** `vencer()` leía `c["plazo_respuesta"]` fuera del `try`.
- **H-44.** `_textos` no tenía `frozenset`.

## Evidencia

Los scripts del revisor de T-93 (`.docs/tickets/T-93/revisores/r01_01_r8_escapes.py`, `r01_02_almacen_legado.py` y `r01_03_plazos_tipos.py`) daban 9, 2 y 1 fallos; ahora dan 0, 0 y 0. Sin la corrección, 18 de las 23 pruebas nuevas fallan (las 5 que pasan son las de textos que no son clave, que vigilan que la corrección no añada falsos positivos).

## Implementación

- `bloque_a/contratos.py`: `RE_ESCAPES` nuevo, la propuesta del revisor (`\\+(?:u…|U…|x…|[0-7]{1,3}|[ntrbf/"])` y `%(?:25)*(?:u…|..)`); `_textos` con `frozenset`; en `_es_clave_sk`, una cola de cuatro o más tramos de solo cifras es clave.
- `bloque_a/almacen.py`: `escribir` antepone «\n» si el fichero no acaba en él. Se hace al escribir, no al abrir, para cubrir también el almacén sellado (caso 2), y para no tocar el fichero en una apertura de solo lectura.
- `bloque_a/interfaz_broker.py`: `c.get("plazo_respuesta")`; con `None`, `_instante` lanza `ValueError` y va por la rama de la incidencia de H-38.
- Documentos: «Límites» de `T-93/analisis-tecnico.md` (H-41, H-45 y H-46 a), `Reloj.fecha` (H-46 b) y la línea de CT-23 del README del ejecutor (H-46 c).
- **Límites conocidos:** siguen sin verse las colas de 3 grupos de 10 mayúsculas y de 4 grupos de 6 mayúsculas (forma de siglas), y siguen marcando 6 de 10 titulares con cifra y unidad (H-45, falla cerrado). Entidades HTML y `\N{…}` no se sustituyen (INFO en `r01_01` caso 2; ningún agente las produce delante de una clave).

## Comandos

```bash
W=bloque_a/11_Ejecutor; for f in r01_01_r8_escapes r01_02_almacen_legado r01_03_plazos_tipos; do .venv/bin/python -I .docs/tickets/T-93/revisores/$f.py $W; done
```

```bash
.venv/bin/python -I .docs/tickets/T-92/revisores/r04_01_r8_regla_texto.py bloque_a/11_Ejecutor
```

```bash
.venv/bin/pytest -q bloque_a/11_Ejecutor/tests/test_t103_r8_y_bajos.py
```

## Ronda r02 (QA r01 NO APTO)

**Causa.**
- **H-47:** la alternativa `\\+(?:…)` volvía a empezar en cada barra de un tramo que no acaba en un escape, así que el coste era cuadrático.
- **H-48:** `_actualizar`, `ReplayClient` y `CacheResultados` partían el JSONL con `splitlines()`, que también corta en U+2028, U+2029 y U+0085, y `json.dumps(ensure_ascii=False)` no los escapa. Ya pasaba desde la entrega.
- **H-49:** la prueba de H-44 no dependía de lo que corrige, porque desde H-40 el volcado ya veía la clave.
- **H-50:** la regla de H-41 empezaba en cuatro tramos.

**Implementación.**
- `contratos.py`: `RE_ESCAPES` empieza el tramo donde empieza (`(?<!\\)`) y lo toma de una vez (`\\++`, posesivo). Con 99.999 barras, 0,08 s; antes, 129 s. Una cola de tres o más tramos de solo cifras es clave.
- `almacen.py`, `llm.py` y `herramientas/ht06_indice.py`: los JSONL se parten solo por «\n».
- `tests/test_t103_r8_y_bajos.py`: 8 pruebas nuevas (H-47, H-48 en los tres lectores, H-49 con el par «"password": …» dentro de un `frozenset` y H-50).

**Límites conocidos (se declaran: H-50 a H-52).**
- Una cola de menos de 20 caracteres tras «sk-» no es candidata (regla de T-92): tres grupos de cinco cifras (17 caracteres) no se ven. Tres o más grupos de 6, 7 u 8 cifras y tres fechas AAAAMMDD, 500 de 500.
- **Falsos positivos que falla cerrado (H-51)**, con el resultado PARCIAL y una incidencia, sin perder ninguna clave:
  - referencias y marcas de tiempo de solo cifras con tres o más grupos y 20 caracteres o más («sk-2024-11-12-10-30-00-123»);
  - las colas de H-45 detrás de un escape doble (titulares en JSON anidado y rutas de Windows dentro de un JSON).
- **Formas que siguen sin verse (H-52).** Tampoco se veían antes; no son una regresión:
  - la barra codificada seguida de «n» (`%5Cn`, `\\u005cn`, `\\x5cn`);
  - quoted-printable (`=3D`);
  - `\\a`, `\\v` y `\\e`;
  - `%U2014` en mayúscula;
  - la clave en base64, con U+200B o U+00AD dentro, con un `\\u0041` dentro o partida en líneas.

  Cerrar la clase entera pide decodificar por capas en lugar de sustituir por un espacio; queda en la deuda (fila T-103).
