# T-171 · Análisis técnico

## Causa raíz o motivo

El detector de `guias.py` (T-158, endurecido en las cuatro rondas de T-161) decide por clases de palabras y por la posición de
la acción. La QA r04 de T-161 (`r04_01_ataques_nuevos.py`) encontró cinco huecos de estructura, no de vocabulario:

1. **Alcance (Z, 4).** `ACOTA` solo reconocía conjunciones y relativos («si», «cuando», «las opciones que…»). Un complemento sin
   conjunción («en las opciones de RV», «los lunes», «en semanas pares», «para H1 y H2») acota igual y no se veía. Además, el
   alcance se miraba sobre `_accion(t)`, que quita lo que va delante («En RV, haz la segunda pasada» pasaba).
2. **Mostrar que oculta (Y, 2).** Un verbo de `PRESENTA` eximía a un control del núcleo aunque no fuera toda la acción: con una
   segunda acción coordinada («… y quédate con la primera») o separándolo de donde está («Separa … del informe»).
3. **Ancla en blanco (AA, 1).** «en blanco» no era de la clase de «vacío».
4. **Lecciones (AB, 3; AC, 2).** `ENDURECE` enmascaraba el descarte de una oportunidad hasta el final del tramo, aunque el tramo
   la quitara de un registro («… del informe al Auditor», «… del registro», «… antes de G3»): eso oculta, no descarta. Y
   `CARENCIA` enmascaraba «sin objeciones» aunque la observación dijera que sin el control salió mejor o igual (un argumento para
   quitarlo). «Excluir» y «retirar» no estaban entre las rebajas, así que, sin la máscara, tampoco se detectaban.
5. **Falsos positivos (H-19).** `FINANCIERO` no admitía posesivos ni el componente («el peso de cada valor en su índice»);
   `INSTRUCCION` cazaba «significativas» con `significa\w*`; «lista» no era un verbo de mostrar y «al final del informe» era
   una condición de `NIEGA`; `CARENCIA` no veía la carencia en pretérito («se omitió»); el resultado de «una sola raíz» solo se
   buscaba a dos palabras.

## Evidencia

Antes (en `origin/develop`, `a9210c0`), desde `bloque_a/11_Ejecutor`:
`../../.venv/bin/python ../../.docs/tickets/T-161/revisores/r04_01_ataques_nuevos.py` → 17 de 30 pasan; 3 de 28 ítems y 2 de 10
lecciones en falso positivo. Después: 3 de 30 (las paráfrasis V), 0 de 28 y 0 de 10.

## Implementación

- **Archivos cambiados:**
  - `bloque_a/11_Ejecutor/bloque_a/guias.py`: solo el detector. Nuevos: `_DET`, `_COMPONENTE`, `ALCANCE_TIEMPO`, `ALCANCE_PARTE`,
    `_OBJETO`, `_CLASE`, `_SEPARA`, `_FUERA`, `_COORDINA`, `_ABRE_NOMBRE`, `_VERBOS_DE_MOSTRAR`, `FAVORABLE`, `UNIVERSAL`,
    `_otra_accion`, `_oculta`; `_refuerza` toma `leccion`. Cambiados: `FINANCIERO` (determinantes y componente), `INSTRUCCION`
    (formas del verbo «significar»), `MUESTRA` y `PRESENTA` (lista, enumera), `NIEGA` («al final de» solo como plazo),
    `RELAJA` («en blanco», «sin rellenar», «nulo», «a cero», «excluir», «retirar»), `ENDURECE` (destino de registro o de control;
    resultado desfavorable en toda la frase), `CARENCIA` (pretérito), `_solo_muestra` (segunda acción), `conflicto_de_leccion`
    (`FAVORABLE`, `UNIVERSAL`).
  - `bloque_a/11_Ejecutor/tests/test_t171_guias.py` (165 casos): copia literal de `r04_01`, juego propio y una prueba por regla.
  - `docs/incidencias.md` (INC-T126-01, viñeta T-171), la fila T-171 de la deuda técnica y este ticket
    (`reservado_t171.py`, `mutantes_t171.py`).
- **Decisiones y desviaciones del plan de la QA:**
  - La QA proponía «cortar» `ENDURECE` ante «del informe…». Cortar dejaría enmascarado el verbo («Descartar …») y lo que queda
    («del informe al Auditor») no tiene rebaja, así que seguiría pasando. Se hace más fuerte: si el tramo lleva ese destino, la
    alternativa no enmascara nada. Por eso «excluir» y «retirar» entran en `RELAJA` (la misma clase que «quitar» y «descartar»).
  - La QA proponía ampliar `ACOTA` a «en las opciones de», «los <día>», «en semanas» y «para H<n>». Se separa en dos clases. El
    calendario acota siempre (un control obligatorio vale en todos los ciclos). La clase, el horizonte y la población solo
    acotan si el control del núcleo es el objeto directo, porque las guías van a un Analista de una clase y hablar de ella es lo
    normal: con la regla sin esa condición, el ejemplo del prompt 4.5 («En cribado DIV, comprobar el diferencial…»), «En RF,
    revisa la cláusula…», «En DER, consulta el interés abierto antes de proponer un contrato» y «Añade a la lista de
    verificación de FON…» pasaban a conflicto (medido con `medir_detector.py`, `r01_01` y `r02_01` en la primera versión).
  - La QA proponía tratar los verbos de `PRESENTA` que quitan o separan como `REDUCE`. Se hace por estructura: `_SEPARA` y
    `_FUERA` (separar de, fuera de) y `_otra_accion` (segunda acción coordinada) en lugar de una lista de verbos. La misma
    `_otra_accion` cierra además el «mostrar y después cambiar» que la r04 había dado por límite (W).
  - `FAVORABLE` no lo pidió la QA: es lo que distingue en AC el hallazgo de un argumento para quitar el control.
  - Se quita «acertaron» de la alternativa de `ENDURECE` de «una sola raíz»: que acertaran con una sola raíz no hace más
    prudente nada (juego propio: «Tesis de una sola fuente que acertaron en 8 casos» pasaba).
  - El objeto directo se busca después de quitar los complementos de alcance que van delante de él (`sin_alcance` en `_refuerza`): «Comprueba en RV la segunda pasada» pasaba con la primera versión (lo encontré al escribir el traspaso, después de medir el juego reservado; está en el juego propio).
  - `_refuerza(…, leccion=True)` no aplica las dos clases de alcance a la recomendación de una lección, que va acotada a su
    ámbito por oficio («Exigir segunda pasada en todas las candidatas de DER…», de T-161 r04, seguiría reteniéndose).
- **Límites conocidos:** las tres paráfrasis V de la r04; un sustantivo singular sin determinante tras «y» cuenta como segunda
  acción («Presenta las objeciones y respuesta», falso positivo prudente); un alcance con la clase sin su sigla («en renta
  variable», «en las de renta variable») pasa; «Pon la tabla de riesgos al final de la tesis» sigue en falso positivo, como en
  develop. Lo que pasa solo llega como contexto a agentes que no son de control.
- **Fuera de mi pieza:** nada. No se tocan los ficheros de T-165 ni el corpus.
- **Comandos:**

```bash
cd bloque_a/11_Ejecutor
../../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_t171_guias.py tests/test_t161_*.py tests/test_t158*.py tests/test_t126_pb26_pb48.py
for s in r01_01 r02_01 r03_01 r04_01; do ../../.venv/bin/python ../../.docs/tickets/T-161/revisores/${s}_ataques_nuevos.py; done
../../.venv/bin/python ../../.docs/tickets/T-161/medir_detector.py
../../.venv/bin/python ../../.docs/tickets/T-171/reservado_t171.py
../../.venv/bin/python -m pytest -q -p no:cacheprovider ../../.docs/tickets/T-161/revisores/r04_02_integracion.py ../../.docs/tickets/T-161/revisores/r05_01_cierre.py
cd ../..
.venv/bin/python .docs/tickets/T-161/revisores/r04_03_sin_guias.py <carpeta_desechable> origin/develop
.venv/bin/python .docs/tickets/T-171/mutantes_t171.py <copia «qa29_…_mut» con bloque_a/ entero> [IDs…]
```
