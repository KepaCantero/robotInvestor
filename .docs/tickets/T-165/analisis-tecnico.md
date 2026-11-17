# T-165 · Análisis técnico

## Causa raíz o motivo

El catálogo de G3 (prompt del Orquestador técnico V5.0, §6.2) define G3-MET-13 «Madurez declarada» (clase B): «Método citado sin
`estado_madurez` o presentado como validado cuando RC lo registra como documentado o implementado». PB-47 la usa para que «nada se
presente como validado sin estarlo» (R22). La referencia de HT-09 (`bloque_a/10_Herramientas/ht09_validador_g3.py`, C01–C19,
corpus congelado) no la implementa, y el ejecutor tampoco: `sintesis.ht09_validar` solo añadía a la referencia la selección
unitaria (C15) y el método explícito de R13 (C07). Así, un informe de clase que llama «validado» a un método en DOCUMENTADO
pasaba G3 APTO y llegaba al técnico y al JSON.

Al probar la comprobación apareció una segunda causa, del propio ejecutor: el rótulo del técnico «N efectivo ML-CLUS-001: …»
(`redaccion.py`) y la limitación de «sin historia» (`orquestacion.py`) citan ML-CLUS-001 aunque el Motor lo haya rechazado. Con
ML-CLUS-001 en DOCUMENTADO, esa cita es justo lo que G3-MET-13 tiene que bloquear; sin corregirla, ningún ciclo con el método en
DOCUMENTADO podría entregarse nunca (y la prueba de T-159 de PB-47 caería).

## Evidencia

- HEAD (`189ee55`), sonda de la QA de T-159: `cd bloque_a/11_Ejecutor && ../../.venv/bin/python -m pytest -q -p no:cacheprovider -s
  ../../.docs/tickets/T-159/revisores/r01_02_sondas.py -k pb47` → «dictámenes G3: ['APTO', 'APTO'] · entregables con «validado»:
  ['informe_tecnico', 'paquete_json']» y falla.
- Con T-165: «dictámenes G3: ['BLOQUEADO', 'APTO_CON_ADVERTENCIAS', 'APTO_CON_ADVERTENCIAS'] · entregables con «validado»: []» y
  pasa. El primer G3V- de F6 queda BLOQUEADO con G3-MET-13 (««validado» para ML-CLUS-001, «DOCUMENTADO» en el Catálogo: «Los
  clústeres…»»), el CT-14 llega al Orquestador, las seis opciones de RV y RF (todas lo afirmaban) se retiran y el segundo G3V-
  queda con la advertencia de los informes de clase que ya no llegan a la entrega.
- Lo que el texto del ejecutor cita de los métodos en un ciclo normal (sondeo de 2 ciclos con los 12 tipos): el técnico nombra
  ST-DESC-001 (valoración, lo escribe el Analista), RISK-DD-001 (riesgo sintético) y ML-CLUS-001 (N efectivo); el JSON, ST-DESC-001.
  Ninguna palabra de madurez aparece en ningún entregable del ciclo simulado («arrastre verificado» es la única palabra parecida).
- Los prompts de los Analistas declaran la madurez en `estado_madurez_metodos` con frases como «DER-OPT-001 documentado;
  VOL-GARCH-001 implementado», «FON-DISC-001: documentado, no validado» o «FX-PPA-001, FX-COINT-001: implementados, validación
  pendiente»: las pruebas las usan como casos que no deben saltar.

## Implementación

- **Archivos cambiados y por qué.**
  - `bloque_a/11_Ejecutor/bloque_a/herramientas/ht09.py`: sigue reexportando la referencia; añade `comprobar_madurez` (función pura:
    textos con ruta y severidad, la madurez del Catálogo, la función «se sirve» y el índice de fichas → una comprobación con el
    formato de HT-09), `textos_de` (aplana un JSON con rutas; el OPP- va en la ruta de cada elemento con `opp_id`; un campo
    `…madurez…` se lee con sus hermanos de método), `texto_html` y `nivel_catalogo`. Se quitan tres avisos de ruff que ya tenía
    (dos `noqa` sin uso y el orden de imports, con `noqa: I001` porque `DIR_REFERENCIA` tiene que ir antes).
  - `bloque_a/11_Ejecutor/bloque_a/sintesis.py`: `ht09_validar` suma `g3_met13` (paquete de síntesis, informe visual e informes
    de clase de `extras["seleccion"]` y `extras["analisis"]`) y recalcula dictamen, motivo y resumen con `_recalcular` (la regla de
    la referencia; antes solo se recalculaba con bloqueos). `g3_met13_tecnico` comprueba el técnico ya escrito y suma sus
    incidencias a la misma comprobación. `extras["clusteres_calc_id"]` dice si el Motor sirvió los clústeres.
  - `bloque_a/11_Ejecutor/bloque_a/redaccion.py`: tras escribir el técnico, `g3_met13_tecnico`; si bloquea, `G3-MET-13` entra en
    los bloqueos de F7 (la entrega va a `_bloqueados`, como con `COHERENCIA_ENTREGABLES`). `_rotulo_n_efectivo`: «N efectivo
    ML-CLUS-001» solo si hubo cálculo; si no, «N efectivo sin clústeres del Motor, cada serie cuenta aparte».
  - `bloque_a/11_Ejecutor/bloque_a/orquestacion.py` (lo justo, una expresión): la limitación de «sin historia» dice «el resto
    tampoco se agrupa (ML-CLUS-001 rechazado)» cuando el Motor lo rechazó.
  - `bloque_a/11_Ejecutor/tests/test_t165_g3_met13.py` (47 pruebas), `tests/mapa_plan_pruebas.json` (PB-47 → AUTOMATICA),
    `docs/evidencias_pruebas_bloque_a.md` (regenerado), `docs/incidencias.md` (INC-T165-01; nota «aplicada» en INC-T159-01),
    `bloque_a/11_Ejecutor/README.md` (§10).
- **Decisión tomada (no propuesta):** `sistema_global/seguimiento/Decisiones_del_operador_Bloque_A.md` §1, fila «G3-MET-13» (Agente, por delegación del operador, 16-11-2026): G3-MET-13 se queda como comprobación complementaria del ejecutor y el HT-09 de referencia del corpus no se toca. El registro de decisiones no lo toca este ticket.
- **Decisiones tomadas `[PROPUESTO]`** (detalle en INC-T165-01): id `G3-MET-13` y no C20; madurez y servicio desde el Motor; las
  reglas A (sobredeclaración) y B (ficha no servida sin declarar); una ficha servida citada sin madurez no salta (la primera mitad
  literal de G3-MET-13 exigiría cambiar el esquema del JSON, corpus); infradeclarar no salta; lectura frase a frase con atribución
  a la ficha más cercana o a todas en plural, negación con auxiliares de lista cerrada, «validado por» una persona o un dato
  (lista cerrada) no es madurez; los informes de clase de candidatas que no
  llegan a la entrega dan advertencia; fallo localizado en una opción → F6 la retira (no está entre los sistémicos de §6.3).
- **Desviaciones del plan:** ninguna de alcance. Las etiquetas HTML de formato en línea (`<b>`, `<span>`…) no cortan la frase: lo
  encontró una prueba del ticket (`test_texto_html_separa_frases_por_etiquetas`) antes de cerrar.
  Y la excepción «validado por el operador» dentro de una frase con ficha: la medí con frases de redacción realista («umbral validado
  por el operador», «tesis validada por el dato de empleo») y bloqueaban; ahora no, con la lista cerrada de INC-T165-01.
- **Límites conocidos.**
  - Es lectura de texto libre por patrones (lección `claude/2026-11-12_filtros-por-patron-en-texto-libre`): medida con las frases
    de los prompts, el ciclo simulado y un backtest de 13 ciclos, no con la redacción de un modelo real. Con dos fichas en una frase
    y la palabra en singular, solo cuenta para la más cercana: «ML-CLUS-001 y ST-DESC-001 implementado» no atribuye «implementado» a
    ML-CLUS-001, pero si este no se sirve la regla B lo bloquea igual (no está declarado); y «validado» bloquea a cualquiera porque
    ninguna ficha está VALIDADO. Una frase que el corte separa mal (abreviaturas con punto y espacio) puede perder la atribución.
  - El rótulo «(RISK-DD-001)» del riesgo sintético se escribe aunque RISK-DD-001 no se sirva: si dejara de servirse, G3-MET-13
    bloquearía la entrega (falla cerrado).
  - El informe de seguimiento C6 no se comprueba (lo escribe el ejecutor sin modelo).
  - En F7 no hay retirada: un bloqueo del visual o del técnico bloquea toda la entrega.
- **Comandos exactos para probarlo** (desde `bloque_a/11_Ejecutor`, con el Python del `.venv`; el ejecutable `bloque-a` del `.venv`
  enlazado importa el paquete de otra copia, así que el backtest se lanza con `python -m bloque_a.cli` desde esta carpeta):

```bash
../../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_t165_g3_met13.py
../../.venv/bin/python -m pytest -q -p no:cacheprovider -s ../../.docs/tickets/T-159/revisores/r01_02_sondas.py -k pb47
../../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_t159_extremo_a_extremo.py tests/test_fase4_mapa.py
../../.venv/bin/python tests/goldens_ct.py
../../.venv/bin/python -m bloque_a.cli --cliente mock --datos ejemplos/datos_sinteticos --universo config/universo_ejemplo.csv \
  --salida /tmp/salida_mock backtest --desde 2024-01-05 --hasta 2024-03-29
```

## Ronda r02 (QA r01 NO APTO: H-01 a H-12; los bajos se subsanan aquí por la regla del operador del 16-11-2026)

### Causa raíz

La lectura de la r01 trataba la frase como unidad y la palabra exacta como vocabulario, y solo reconocía la ficha con guiones ASCII y
mayúsculas. Por eso se le escapaban la anáfora («usa X. Es un método validado»), las tablas, las formas verbales («se validó»),
las fichas con otra grafía y los registros JSON con otra forma. Además, la excepción «validado por» incluía justo lo que valida un
método (datos, mercado, evidencia). Y la negación solo cubría «no» con tres auxiliares, así que la prosa financiera («ruptura
validada») bloqueaba. Es la lección `claude/2026-11-12_filtros-por-patron-en-texto-libre`: el banco de la r01 medía sobre todo lo
que no debe saltar. La r02 cambia la unidad y normaliza antes de leer, y se mide en las dos direcciones contra bancos que no son
los del implementador.

### Implementación

- `bloque_a/herramientas/ht09.py`: la sección G3-MET-13 se reescribe:
  - `normalizar` (NFKC, sin Cf, guiones, homoglifos, minúsculas);
  - `Fichas` (completas, con espacios, pegadas y parciales; ambiguas, `?…`, falla cerrado), con caché `fichas_de`;
  - `textos_de` con registros de método (H-05) y las fichas del Motor por defecto;
  - `texto_html` (celdas, filas, `br`, etiquetas en línea sin espacio, atributos title, alt y aria-label);
  - `_unidades` (párrafos y filas);
  - `_negada` (recorrido de palabras en una ventana fija, auxiliares, ficha como sujeto, doble negación);
  - `_ligada` (prosa financiera);
  - `_leer_unidad` (atribución frase → unidad → párrafo anterior, con bisect);
  - el extracto sin OPP-.
- `bloque_a/sintesis.py`:
  - `_fichas` (índice del Ejecutor y tabla del Catálogo, vía `servicio`);
  - `textos_de` con fichas;
  - el técnico por párrafos (`_parrafos`) y no por líneas;
  - `factor_dominante` condicional (H-06);
  - `extras["riesgo_sin_motor"]`.
- `bloque_a/redaccion.py`: `_fuente_riesgo` (el rótulo de RISK-DD-001 es condicional).
- `tests/test_t165_g3_met13.py`: de 47 a 162 pruebas. Hay una prueba por hallazgo, una por cada mutante vivo de la r01, y
  de extremo a extremo V6 con ML-CLUS-001 en DOCUMENTADO, M32 y RISK-DD-001.
- Scripts del ticket: `.docs/tickets/T-165/r02_mutantes.py` (los nueve vivos de la r01 con la expresión equivalente y 22 de las
  reglas nuevas) y `.docs/tickets/T-165/r02_bancos_frases.py` (dos bancos nuevos).
- `docs/incidencias.md` (INC-T165-01, «Ronda r02»), `tests/mapa_plan_pruebas.json` (el «no comprueba» de PB-47),
  `docs/evidencias_pruebas_bloque_a.md` (regenerado) y el README del ejecutor (§10).

### Decisiones `[PROPUESTO]` nuevas (detalle en INC-T165-01)

- La unidad es el párrafo, la fila o el registro. Si la frase no tiene ficha, vale la del párrafo anterior, solo para afirmar.
- Una parcial ambigua se trata como ficha no reconocible: la regla B la bloquea si no se declara.
- «Certificado» no es sinónimo de validado (es el certificado R13). Verificado, probado, contrastado, comprobado y testeado sí.
- «Validado por» solo excluye a las seis personas. Sujetos y complementos que no son métodos salen de una lista cerrada; el
  consenso y el comité no se excluyen, salvo que la palabra vaya ligada a otro sustantivo («el escenario…, validado por el
  consenso»).

### Límites

Los límites de la r01 siguen, y se añaden estos (también en INC-T165-01):

- un método nombrado sin su ficha;
- sinónimos fuera de la lista;
- una afirmación a más de un párrafo de su ficha;
- una abreviatura con punto que parte la frase;
- falsos positivos aceptados: «El modelo macro del BCE está validado por su comité» tras un párrafo con ficha, y «Ningún
  método… está validado; usamos ST-DESC-001». Un falso positivo dentro de una opción la retira; fuera, bloquea el run.
- El script `r01_02` del revisor tiene un caso (`guion_no_separable`) sin su tercer elemento, que lanza un ValueError al
  desempaquetar. No lo toco, porque es del revisor. Reproduje la misma siembra a mano: G3 BLOQUEADO en F6, las opciones se
  retiran y no se entrega con la frase.

### Comandos

```bash
cd bloque_a/11_Ejecutor
../../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_t165_g3_met13.py
../../.venv/bin/python -m pytest -q -p no:cacheprovider ../../.docs/tickets/T-165/revisores/r01_01_ataques_texto.py -rf
../../.venv/bin/python -m pytest -q -p no:cacheprovider -s ../../.docs/tickets/T-165/revisores/r01_02_extremo_a_extremo.py -rf
../../.venv/bin/python ../../.docs/tickets/T-165/revisores/r01_03_ciclos_normales.py --salida <scratch>/ciclos
../../.venv/bin/python ../../.docs/tickets/T-165/r02_bancos_frases.py
cd ../..
.venv/bin/python .docs/tickets/T-165/r02_mutantes.py --copia <copia con bloque_a>
```

## Ronda r03 (QA r02 NO APTO: H-13 a H-27): enfoque estructural

### Por qué otro enfoque

La r01 y la r02 interpretaban la prosa del modelo con reglas de excepción (negación, «validado por» una persona, sustantivos
ligados, éxito de «validación», sinónimos, «: no» detrás). Cada excepción abría su familia de escapes (H-13 a H-16) y cada
sinónimo su familia de falsos positivos (H-18, H-19); la lección `claude/2026-11-12_filtros-por-patron-en-texto-libre` se repetía.
El coordinador decidió (por delegación del operador) un enfoque estructural; lo he valorado y adoptado con dos ajustes que fallan
cerrado: el **ámbito** es el registro o el documento, no la unidad de texto (cierra H-17 y H-23 sin reglas de párrafo, título ni
tabla), y los campos de madurez de los informes de clase **los reescribe el ejecutor** en lugar de bloquearlos (bloquearlos
retiraría toda opción cuyo Analista siga su prompt, «FON-DISC-001: documentado, no validado»). Decisión en INC-T165-01, ronda r03.

### Implementación

| Archivo | Cambio |
| --- | --- |
| `bloque_a/herramientas/ht09.py` | Nueva lectura (sustituye la de la r01 y la r02: `_unidades`, `_negada`, `_ligada`, `_leer_unidad`, `RE_PERSONA`, `_LIGADOS`, `RE_VALIDACION`…). `_Lectura`: menciones de ficha, si llevan su forma canónica correcta (que se blanquea), formas canónicas falsas, corchetes «[madurez:» sueltos, la raíz «valid-» y la «implement-» y los sustantivos de método. `comprobar_madurez`: reglas B y C por mención; regla A por ámbito (`ambito_de`). `textos_de`: cada hoja como «claves del camino: valor», con una marca si está bajo una clave de madurez y no es canónica. La forma canónica: `madurez_canonica`, `anotar_madurez`, `fichas_citadas`, `resumen_madurez`. `Fichas`: «_», «.» y cuatro cifras (H-21); solape por `bisect` (H-22) |
| `bloque_a/sintesis.py` | `canonizar_madurez` (llamada al principio de `construir`): reescribe los campos de madurez de las candidatas. `anotar`, `anotar_json`, `resumen_madurez`, `madurez_metodos`. La retirada de F6 dice «Opciones retiradas por el control G3» |
| `bloque_a/redaccion.py` | `generar`: el visual se comprueba como se redacta y después se reescribe anotado; el JSON se anota (y lleva `x_madurez_metodos`) antes del esquema; el técnico se comprueba sin anotar y se escribe anotado y con la declaración R22 al principio de «7. Limitaciones» (`_con_madurez`, `CABECERA_LIMITACIONES`) |
| `bloque_a/orquestacion.py` | Tres literales: «el resto tampoco se agrupa (el Motor no sirvió los clústeres)»; la limitación de los clústeres no calculados con ML-CLUS-001 en su forma canónica (sin el detalle del Motor si no la sirve); la laguna «fichas del Motor rechazadas…» anotada |
| `bloque_a/diseno_v6.py` | Un literal: el respaldo de la integración V6 dice «sobre el paquete ya revisado por G3» (decía «validado»: bloquearía el paquete en su ámbito) |
| `tests/test_t165_g3_met13.py` | Reescrito para la r03 (109 pruebas): reglas A, B y C, ámbito, JSON, canonización, anotación, grafías, coste, HTML y los extremo a extremo de la r01 y la r02 con las expectativas nuevas |
| `tests/test_t159_extremo_a_extremo.py` | PB-30: la expresión que quita el aviso de la retirada admite «el control G3» (era «la validación G3») |
| `.docs/tickets/T-165/r02_mutantes.py` | H-24: N13 y N17 con la expresión real de la r02; se ejecuta sobre una exportación del commit de la r02 |
| `.docs/tickets/T-165/r03_mutantes.py`, `r03_bancos_frases.py` | Mutantes de la r03 (23) y medida de falsos positivos con un banco nuevo y los anteriores |
| `.gitignore`, índice | H-25: `git rm --cached .venv` y `.venv` sin barra (ignora también el enlace) |
| `docs/incidencias.md`, `bloque_a/11_Ejecutor/README.md` | INC-T165-01, ronda r03; la descripción de G3-MET-13 |

### Hallazgo → corrección

| Hallazgo | Corrección en la r03 |
| --- | --- |
| H-13 sustantivo ligado | No hay sustantivos ligados: «indicador de tendencia validado» bloquea por la raíz |
| H-14 «: no» detrás | No hay negación detrás ni delante |
| H-15 éxito de «validación» | «validación» es la raíz: bloquea con o sin éxito |
| H-16 regla B con «rechazado» negado o de otra cosa | Ninguna declaración en prosa vale: solo la forma canónica de la ficha |
| H-17 otro campo de la misma opción | Ámbito = la opción (`[OPP-…]`) o el registro; fuera, el documento |
| H-18 sinónimos | Quitados; límite declarado (no cuentan como madurez) |
| H-19 la declaración honesta de R22 | La escribe el ejecutor en forma canónica (declaración R22 del técnico, `x_madurez_metodos`, forma canónica junto a cada ficha); en la prosa del modelo bloquea (cambio de expectativa declarado) |
| H-20 JSON con «sí», 1, «3», anidados | Las claves del camino se leen con el valor; un campo de madurez solo admite la forma canónica (regla C); en los informes de clase lo escribe el ejecutor |
| H-21 «_», «.» y cuatro cifras | `Fichas`: separadores `[-_.]` y `\d{3,4}` normalizado |
| H-22 coste cuadrático | Solape por `bisect`; sin negación. Prueba de razón con 2000 y 8000 fichas por párrafo |
| H-23 título y tabla transpuesta | Ámbito = documento: bloquean |
| H-24 script de mutantes | N13 y N17 corregidos; ejecutado entero sobre la r02 (`pruebas.md`) |
| H-25 `.venv` en el índice | `git rm --cached .venv`; `.gitignore` con `.venv` |
| H-26 «más que nunca», imperfecto, subjuntivo | No aplica: no hay negación, y la raíz cubre todos los tiempos («validaba», «valide») |
| H-27 X05 y X07 vivos | X05 no aplica (no hay «párrafo anterior» ni tablas que corten: el ámbito es el documento). X07: prueba `test_el_tecnico_es_un_ambito_y_la_ruta_es_la_linea_del_parrafo` fija la ruta «informe_tecnico, línea N» del párrafo; los mutantes de `r02_03` no se aplican al código nuevo (sus expresiones ya no existen) |

### Límites (además de los de INC-T165-01)

- Falso positivo por construcción: toda frase con la raíz «valid-» junto a un método bloquea (la opción se retira; fuera de una
  opción, el run). Medido en `pruebas.md`. Alternativa no adoptada: sustituir la palabra en el entregable.
- Los entregables del ciclo normal cambian: la forma canónica tras cada ficha del técnico y del JSON, la declaración R22 del técnico
  y `x_madurez_metodos`. Un consumidor que busque «(ST-DESC-001)» literal en el técnico deja de encontrarlo (ninguna prueba del repo
  lo hacía, salvo la de RISK-DD-001 de este ticket, adaptada).
- Lo que dijo el modelo en `estado_madurez_metodos` se descarta sin dejar rastro en el informe de clase.

### Comandos

```bash
cd bloque_a/11_Ejecutor
../../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_t165_g3_met13.py tests/test_t159_extremo_a_extremo.py
../../.venv/bin/python ../../.docs/tickets/T-165/r03_bancos_frases.py
../../.venv/bin/python -m pytest -q -p no:cacheprovider ../../.docs/tickets/T-165/revisores/r02_01_ataques_nuevos.py -rf
../../.venv/bin/python -m pytest -q -p no:cacheprovider -s ../../.docs/tickets/T-165/revisores/r02_02_extremo_a_extremo.py -rf
../../.venv/bin/python ../../.docs/tickets/T-165/revisores/r01_03_ciclos_normales.py --salida <scratch>/ciclos_r03
cd ../..
git archive HEAD bloque_a | tar -x -C <copia> && .venv/bin/python .docs/tickets/T-165/r03_mutantes.py --copia <copia>
```

## Ronda r04 (QA r03 NO APTO: H-28 a H-32)

### Causa raíz

H-28: la r03 midió el falso positivo con frases sueltas y con el simulado, que no escribe la raíz, pero no con lo que piden los
prompts del corpus (R22 del Analizador y de Prospectiva, «Pendiente de validación» de PS5, Divisas, catalizadores) ni con los
textos del propio ejecutor (instrucción al Sintetizador V6, Motor en RC). Fuera de una opción el ámbito es el documento: una
aparición bastaba para dejar el ciclo sin entrega. H-29: el técnico comprobado llevaba las rutas de entrega (configuración).

### Implementación

| Archivo | Cambio |
| --- | --- |
| `bloque_a/herramientas/ht09.py` | `REGLA_R22_REDACCION`; `tiene_raiz_valid`; `RE_VALID` con «v[aá]lid» (H-30); `RE_METODO` con «metodología», «sistema» y «fuera de la muestra» (H-32) |
| `bloque_a/orquestacion.py` | La regla al final de todos los `INSTR`, de la integración, del Redactor y de la Prospectiva V5; `Bloque.reescribir_r22` (bucle de `redaccion.reescrituras_r22`), llamado tras la integración y el Redactor; «semanas con datos utilizables» |
| `bloque_a/diseno_v6.py` | `INSTR_SINTESIS` («ya revisado por G3», «calculadas y revisadas», más la regla) e `INSTR_PROSPECTIVA` con la regla; reescritura tras el Sintetizador, antes de aplicar su integración al paquete; `_SIN_SINTESIS` «no dio una respuesta utilizable» |
| `bloque_a/sintesis.py` | `canonizar_madurez` devuelve lo descartado y `construir` lo deja en HA (INC `OTRO`, `madurez_del_modelo`); `_laguna_r22`; `anotar_json(…, sin_anotar)` y `claves_con_longitud_maxima` (H-31) |
| `bloque_a/redaccion.py` | El JSON no anota las claves con `maxLength` del esquema y `x_madurez_metodos` se calcula sin anotar; el técnico de G3-MET-13 se genera con marcadores en lugar de las rutas (H-29) |
| `bloque_a/motor/servicio.py` | La limitación por defecto en RC, sin la raíz |
| `bloque_a/mock_respuestas.py` | La integración simulada escribe la declaración R22 del prompt con la raíz y, en la reescritura, sin ella |
| `config/por_defecto.yaml` | `redaccion.reescrituras_r22: 1` `[PROPUESTO]` |
| `tests/test_t165_g3_met13.py` | 16 pruebas de la r04 (126 en total) |
| `tests/test_t113_deuda.py` | El texto de `_SIN_SINTESIS` («utilizable») |
| `.docs/tickets/T-165/r03_mutantes.py` | R24–R35 para la r04; R01, R02, R17, R19 y R21 con las expresiones nuevas |
| `.docs/scripts/estimar_coste_ciclo_a.py`, `tests/test_t145.py`, `tests/test_t148.py` | La cota del ciclo prevé las dos reescrituras R22 (AG-02 y AG-17, `redaccion.reescrituras_r22`): `LLAMADAS_DEL_CICLO` admite la clave de la configuración como máximo; los recuentos de las pruebas pasan de 7 + 7 a 7 + 9 |

### Límites

- Dentro de una opción no hay reescritura: si un Analista escribe la raíz pese a la regla, la opción se retira. Con el corpus,
  1 de 12 ejemplos de ficha (Fondos). La reescritura de la candidata por CT-06 queda como propuesta para el operador.
- La reescritura se decide por la raíz en cualquier texto de la respuesta, no por la regla A con su ámbito: puede pedir una
  reescritura que G3-MET-13 no habría necesitado (una llamada más; nunca menos control).
- Los ciclos V5 simulados hacen una llamada más al Analizador (la reescritura de la declaración R22): consumo y técnico cambian.
- Los scripts del revisor que siembran la raíz sin atender a la reescritura (`r03_03::test_fp_lectura_del_conjunto`,
  `test_fp_sintetizador_v6…`) siguen bloqueando por construcción: la raíz persiste tras la reescritura y G3-MET-13 falla cerrado,
  que es lo pedido («se bloquea solo si persiste»). Las pruebas del ticket siembran como el simulado y sí entregan.

### Comandos

Los de la r03, y `../../.venv/bin/python -m pytest -q -p no:cacheprovider -s ../../.docs/tickets/T-165/revisores/r03_0{2,3}_*.py -rf`,
`../../.venv/bin/python ../../.docs/tickets/T-165/revisores/r03_01_corpus.py` y `.venv/bin/python .docs/scripts/cadena_a_b.py --trabajo <dir>`.

## Ronda r05 (QA r04 NO APTO: H-33 a H-37)

| Archivo | Cambio |
| --- | --- |
| `bloque_a/orquestacion.py` | `reescribir_r22(…, bolsa="COMUN")` con las frases con la raíz en el mensaje (H-37); reescritura tras el CT-06 de `_analizar_clase` (H-34) y tras la refutación V5, cuya instrucción lleva la regla (H-33), en la bolsa del tipo; `_integrar` pasa su instrucción completa a la reescritura (H-36) |
| `bloque_a/diseno_v6.py` | `INSTR_REFUTACION` con la regla y reescritura tras la refutación V6, en la bolsa global (H-33) |
| `bloque_a/herramientas/ht09.py` | `frases_con_raiz(obj, maximo)` |
| `bloque_a/sintesis.py` | `_laguna_r22`: la palabra a «comprobar» y «(redacción ajustada por R22)»; solo si persiste, la omisión (H-35) |
| `bloque_a/mock_respuestas.py` | `_obedece_r22`: en la reescritura R22 el simulado cambia la raíz por «comprobar» en toda su respuesta |
| `config/por_defecto.yaml` | `redaccion.frases_r22_max: 10` `[PROPUESTO]` |
| `.docs/scripts/estimar_coste_ciclo_a.py` | `LLAMADAS_POR_TIPO` con «reescritura_r22_cribado» y «reescritura_r22_refutacion» (`redaccion.reescrituras_r22`); los papeles de reescritura no suman a lo que leen los siguientes (S4) |
| `tests/test_t145.py`, `tests/test_t148.py` | 9 llamadas por tipo y 9 del ciclo; AG-11, hasta 3 por tipo |
| `tests/test_t165_g3_met13.py` | 12 pruebas de la r05 (138 en total); las de PB-47 y de HA, con el simulado sin obedecer (lo que se mide es lo que persiste) |
| `.docs/tickets/T-165/r03_mutantes.py` | R36–R43 y R32 con la expresión nueva |

Límites: con un modelo que no sigue la reescritura, lo de dentro de una opción se retira como antes (falla cerrado). La
reescritura del informe de clase cuesta una llamada de Analista solo cuando aparece la raíz.

## Ronda r06 (QA r05 NO APTO: H-38 a H-40)

| Archivo | Cambio |
| --- | --- |
| `bloque_a/orquestacion.py` | `_invocar` envuelve la llamada (`_invocar_una`, el cuerpo de antes) y, salvo para los agentes de `ht09.AGENTES_SIN_TEXTO_ENTREGADO` o un mensaje que ya es una reescritura R22, llama a `reescribir_r22` con los datos de la llamada. `reescribir_r22`: sin los campos de madurez (H-38), INC en HA con las frases (H-39), la reescritura conserva la de legibilidad si la había y pasa por `_invocar` (las espías de las pruebas la ven). Quitadas las llamadas sueltas |
| `bloque_a/diseno_v6.py` | Quitadas las llamadas sueltas (refutación y Sintetizador) |
| `bloque_a/herramientas/ht09.py` | `AGENTES_SIN_TEXTO_ENTREGADO` (exclusión); la frase nueva de `REGLA_R22_REDACCION` |
| `.docs/scripts/estimar_coste_ciclo_a.py` | `con_reescrituras(sin_texto)` deriva las filas de reescritura; quitadas las cuatro a mano; `maximo` admite el producto |
| `tests/test_t145.py`, `tests/test_t148.py` | Recuentos derivados (12 por tipo y 10 del ciclo; AG-11, 4 por tipo); el peso por búsqueda de la cota por llamadas con su clave; la salida «manda el presupuesto» también con divisas y «mandan las llamadas» sin reescrituras |
| `tests/test_t165_g3_met13.py` | 6 pruebas de la r06 (145 en total); la de HA, con el simulado obediente |
| `.docs/tickets/T-165/r03_mutantes.py` | R25, R26, R38–R40 y R42–R46 rehechos o nuevos para el código de la r06 |

Límites: el coste de la reescritura solo aparece con la raíz, pero la cota del estimador la cuenta siempre (es una cota).

## Ronda de cierre de la QA r06 (APTO; observación del revisor)

`ResultadoAgente.peor_caso_uc` (`agentes.py`) guarda lo que reservó la llamada (`ReservaLlamada.peor_total`, o el estimado de la
consulta N0); `Bloque.reescribir_r22` no pide la reescritura si ese peor caso más los tokens de las frases no cabe en la bolsa
(`Presupuesto.puede`), y lo deja en HA. La respuesta con la raíz se queda y G3-MET-13 decide. Mutante R47.
