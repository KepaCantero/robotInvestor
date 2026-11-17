# T-164 · Análisis técnico

## Causa raíz o motivo

Hallazgos abiertos de la QA r02 de T-157 (`.docs/tickets/T-157/qa.md`, «Hallazgos nuevos»):

- **H-09 (media).** `contexto_d` miraba solo si el ID estaba en el diccionario `simbolos` (valores enteros de `serie_ht01` o
  `simbolo` en cualquier archivo). Si estaba, excusaba **todas** sus apariciones, también el valor de `ficha_id` o «la ficha X».
  Lo mismo pasaba con las familias desconocidas (`if x in simbolos: continue` se saltaba el ID entero).
- **H-10 (baja).** Tanto `re_cita` como `RE_FORMA_FICHA` exigían `-\d{3}` al final, así que «FX-TREND-01» no se citaba.
- **H-11 (baja).** `_escribir_todo` escribía y renombraba cada archivo antes de pasar al siguiente. Si el temporal del segundo
  fallaba (una carpeta que existe pero no admite archivos, como `/proc`), el primero ya estaba en su sitio.
- **H-12 (baja).** Seis mutantes vivos de `r02_02_mutantes.py`: N02, N04, N05, N06, N07 y N08.
- **H-04.** No es un defecto. Se mantiene por la decisión de INC-T157-01 (la «tarjeta RF-1» es otro ID con el mismo prefijo).

## Evidencia

- Antes: `r02_01_ataques.py` daba 11/16 (fallaban H-09 ×2, H-10 ×2 y H-11) y `r02_02_mutantes.py` dejaba 6 vivos (`qa.md` r02).
- Las 6 pruebas nuevas de H-09, H-10 y H-11 fallan con el `verificador_ids.py` de develop (`e35d284`) y pasan con el nuevo. Las 3
  de H-12 pasan con los dos: protegen un comportamiento que ya era correcto y matan a sus mutantes.

## Implementación

- **`bloque_a/11_Ejecutor/bloque_a/herramientas/verificador_ids.py`** (`VERSION` 1.0.0 → 1.1.0, porque cambian las reglas):
  - H-09: `CAMPOS_FICHA`, `RE_VALOR_JSON`, `RE_PALABRA_FICHA`, `RE_FIN_FRASE`, `_campo_json(c)` (el campo y la columna del valor
    JSON, cadena o array, que contiene la cita) y `_como_ficha(c, campo)`. Una aparición se usa como ficha si es el valor de un
    campo de ficha, o si «ficha» o «fichas» aparece antes en su frase. `contexto_d` excusa un símbolo declarado solo en las
    apariciones que no se usan como ficha. El bucle de familias desconocidas aplica la misma excusa por aparición: las apariciones
    excusadas salen como INFO `CITA_EN_CONTEXTO_AJENO` y el resto sigue la regla de antes (ERROR si se parece a una ficha, INFO
    `FAMILIA_DESCONOCIDA` si no).
  - H-10: `re_otras_cifras`, la misma forma que `re_cita` pero con `\d{1,2}` o `\d{4,}` al final. Sus citas se suman a las de
    `re_cita` antes de `_inexistentes`. El mensaje añade «con otro número de cifras finales que las fichas del Catálogo» cuando el
    ID no tiene la forma `RE_ID_FICHA`.
  - H-11: `_escribir_todo` escribe primero todos los temporales y después los renombra. En un `finally`, borra los temporales que
    queden (`contextlib.suppress(OSError)`), y el `OSError` llega al `except` de `main` (salida 2). Los textos que mutan N05 y N06
    no cambian.
- **`bloque_a/11_Ejecutor/tests/test_t157_verificador_ids.py`**: 9 pruebas `test_t164_*` (el archivo pasa de 46 a 55) y un
  caso más en `TRAMPAS` (`{"metodo":"AA-THETA-001"}` tiene que dar ERROR), que exige `test_r02_contextos_no_excusan_de_mas`.
  Hacía falta porque, con la excusa por aparición, el mutante «r02 cualquier campo JSON declara símbolo» de `mutantes_t157.py`
  quedaba vivo: el caso que antes lo mataba (`estado_madurez_metodos`) ya lo para la regla de campo de ficha. El caso nuevo
  comprueba lo que ese mutante rompe, que solo un campo de serie declara un símbolo.
- **`docs/incidencias.md`**, INC-T157-01: los criterios nuevos de H-09, H-10 y H-11 (técnicos, `[PROPUESTO]`, del verificador).
- **Deuda técnica**: la fila T-164 en «EN QA (r01)».
- **`.docs/tickets/T-164/mutantes_t164.py`**: 14 mutantes de las correcciones y el nulo.

**Decisiones y desviaciones del plan:**
- El plan excusaba primero toda aparición dentro del valor de un campo de serie y después aplicaba la regla de ficha. Lo he
  simplificado: basta con «no se usa como ficha», porque la frase empieza al principio del valor JSON y un valor de serie nunca es
  un campo de ficha. Solo cambiaría algo si el valor de una serie contuviera la palabra «ficha» delante del ID.
- He añadido `estado_madurez_metodos` a `CAMPOS_FICHA` además de los tres que sugería la QA, porque es el campo del corpus cuyo
  valor es más veces una ficha. Contando con `grep` las claves JSON que preceden a un ID con forma de ficha en el corpus,
  `estado_madurez_metodos` sale 5 veces, frente a 2 de `ficha_id` y 2 de `method_id`.
- Descarté excusar solo dentro del mismo archivo que la declaración. En el Registro de pronósticos congelados, IDX-FICT-001 va en
  prosa («índice temático IDX-FICT-001», en el valor de `afirmacion`) y se declara en otros archivos, así que se crearía un error
  falso.
- El mutante N04 de `r02_02_mutantes.py` sale ROTO porque su texto (`if x in simbolos: continue`) ya no existe: era justo la
  omisión del ID entero que H-09 corrige. Lo sustituyen T08 y T09 de `mutantes_t164.py`.

**Límites conocidos:**
- La frase se corta por «.», «;», «!» o «?» seguidos de espacio. Una abreviatura con punto entre «ficha» y el ID («la ficha
  núm. X») corta la frase, y el ID se excusaría si es un símbolo declarado.
- `RE_VALOR_JSON` no sigue objetos anidados: `"operacion":{"ficha_id":"X"}` toma `ficha_id` como campo, que es lo que se busca.
  Un array de objetos (`"fichas":[{"id":"X"}]`) toma `id`, que no es un campo de ficha, aunque «fichas» no cuenta como palabra
  porque está en la clave.
- H-11: si `os.replace` falla a mitad de los renombrados, los anteriores ya están renombrados. No hay transacción entre archivos.
- H-10 exige una familia conocida y al menos un segmento intermedio, igual que `re_cita`.

**Comandos** (desde `bloque_a/11_Ejecutor`):

```bash
../../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_t157_verificador_ids.py      # 55
../../.venv/bin/python ../../.docs/tickets/T-157/revisores/r02_01_ataques.py                     # 16/16
../../.venv/bin/python ../../.docs/tickets/T-157/revisores/r02_02_mutantes.py                    # 0 vivos; N04 ROTO (ver arriba)
../../.venv/bin/python ../../.docs/tickets/T-164/mutantes_t164.py                                # 14 matados
../../.venv/bin/python -m bloque_a.herramientas.verificador_ids --json /tmp/t164.json --md /tmp/t164.md   # comparar con develop
```

## Ronda r02 (QA r01 NO APTO)

Las correcciones son las de `qa.md`, tal como vienen:

- **H-01 (media).** `RE_VALOR_JSON` pasa a `"(\w+)"\s*:\s*(?:"([^"]*)"|\[([^\]\[{}]*)\])`. La rama de array ya solo toma arrays de
  escalares: en un array de objetos, `finditer` llega a las claves de dentro, y `"datos":[{"ficha_id":"X"}]` atribuye X a
  `ficha_id`. Prueba: 2 líneas nuevas en `SIMBOLOS`. Mutante: T15.
- **H-02.** `_campo_json` devuelve `m.start()`, así que la frase de un valor JSON empieza en su clave y `"fichas":["X"]` o
  `"ficha":"X"` cuentan «ficha». `RE_FIN_FRASE` deja de cortar en «;» y en el punto de «p.», «ej.», «e.g.», «vs.», «cf.», «pág.»
  y «núm.». He ajustado los docstrings de `_campo_json` y `_como_ficha`, el diseño del README e INC-T157-01. Prueba: 4 líneas
  nuevas en `SIMBOLOS`. Mutantes: T16, T17 y T18. «Según la ficha: {"nota":"X"}» sigue en INFO, porque «ficha» queda antes de la
  clave.
- **H-03.** Solo documentación. El límite del análisis por línea queda escrito en el docstring de `contexto_d` y en INC-T157-01.
- **H-04.** `_escribir_todo` rechaza con `EntradaInvalida` un destino pedido dos veces; compara las rutas después de `resolve()`,
  así que `x` y `./x` cuentan como el mismo. Prueba: `test_t164_r02_h04_destino_repetido`. Mutante: T19.
- **H-05.** Antes del `os.replace`, el temporal toma el modo del destino si este existe. Va dentro del `try`, así que un fallo
  también limpia. Prueba: `test_t164_r02_h05_el_destino_conserva_sus_permisos` (0o640 y 0o600). Mutante: T20.
- **H-06.** He corregido la última frase del punto (4) de INC-T157-01: «Un ID con forma de ficha que no está declarado como
  símbolo es error en cualquier campo JSON (`metodo`, `afirmacion`…) y en prosa dentro de un valor».
- **Mutantes que he rehecho.** T05 (antes mutaba el patrón con «;») y T13: la línea del `chmod` separa ahora la escritura del
  renombrado, así que T13 renombra dentro del bucle de escritura y deja vacío el de renombrado.
- **Observación de la QA, sin hallazgo.** «Aplica la ficha ST-DESC-001 a la serie IDX-FICT-001.» da ERROR. No la cambio: es un
  error falso visible y en el sentido del fallo cerrado, y no se da en el corpus real.
