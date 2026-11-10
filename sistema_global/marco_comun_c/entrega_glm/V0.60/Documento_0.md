# Documento 0 — robustez de los seis validadores de mensajes (V0.60) — GLM, revisado (cuatro hallazgos de la revisión corregidos)

## 1. Problema y alcance

La pieza de robustez del fin de semana (V0.37) demostró con mutaciones aleatorias de semilla fija que F, D y
CT-G-14 nunca lanzan, no mutan la entrada, son deterministas y fallan cerrado. Seis validadores de mensajes
quedaron fuera de aquella pieza y tampoco tenían una prueba sistemática de esas cuatro promesas:
`validar_sobre.validar` (CT-G-02, V-01 a V-26), `validar_encargo.validar_encargo` (CT-G-01, E-01 a E-17),
`validar_contradictor.validar_informe` (CT-G-03, C-01 a C-13), `k_calidad.validar_sello` (S-01 a S-14),
`dimensionado.dimensionar` (E-01 a E-04) y `vigilancia.vigilar` (H). Un validador que lance con una entrada
rara, que retuerza lo que le pasan o que apruebe por descuido rompería «falla cerrado» (regla 1) y la regla 2
de las directrices en el punto exacto donde el sistema decide si un mensaje entra o no.

Entra en esta versión: una batería nueva, `pruebas/pruebas_robustez_validadores.py`, con 75 comprobaciones
agregadas sobre 1.900 casos mutados al azar (semilla fija 20261110) y doce casos fijos, que demuestra las
cuatro promesas para los seis validadores, mutando tanto el mensaje como cada clave de su contexto —incluidas
las que el Orquestador pasa siempre: `sc3` y `sello_encargo` (sobre) y, por casos fijos, `autoria_c` y
`autoria_contradictor` (informe)—. Sale una corrección real: **defecto_01**, en `validar_sobre` (§2 punto 7),
con el cambio mínimo y una prueba que lo fija. Tras la revisión independiente (cuatro hallazgos: dos medios
y dos bajos, ninguno de producto —cobertura de la batería y exactitud de este documento y del LEEME—), la
batería incorpora diez comprobaciones de regresión (r01 a r04, §2 punto 8) y este documento se ajusta a lo
que la batería hace (§4).

Queda fuera: los otros cinco bloques de validador (el Orquestador, F, G, H como reglas, D, CT-G-14, la
infraestructura T-03), que ya tienen su batería o su propia pieza de robustez (V0.37; la de T-03 es la pieza 3
de este kit); el generador de mutaciones de `pruebas_robustez.py`, que se importa sin cambiar ni una línea; y
cualquier cambio de esquema, configuración o migración: el esquema del código sigue siendo V0.53, no hay
constantes nuevas en los módulos de `MODULES_ESQUEMA` ni en `CONFIG_DEFECTO`, y `pruebas_migraciones_t03.py`
pasa sin registrar nada. No se toca el Orquestador.

## 2. Diseño

1. **El generador, importado sin cambiarlo.** `caminos`, `mutar`, `_mutar_en_sitio`, `_es_forma` y
   `_igual_nan` vienen de `pruebas/pruebas_robustez.py` (V0.37) tal cual: una mutación al azar en un camino al
   azar (borrar una clave o un elemento, añadir una clave extra, cambiar un valor por None, "", "x", [], {},
   True, 0, -1, 1e308, NaN, ±inf o un número como texto, o cambiar una fecha por «2026-13-45», «ayer» o una
   fecha sin zona). Cada validador de mensajes rota sus 300 casos entre su mensaje y cada clave de su contexto;
   `dimensionar` rota 500 casos entre sus cuatro entradas y `vigilar` muta 200 veces los datos, con Orquestador
   e intermediario NUEVOS en cada caso (nunca se reutiliza uno que ya cambió). La lista de mutaciones de la
   pieza incluye «anidar un valor 500 niveles»: el generador del fin de semana no la trae, así que se fija
   aparte con seis casos fijos, uno por validador (§2 punto 6).

2. **El protocolo de cada caso aleatorio** copia el de V0.37, en este orden: copia profunda de la base, una
   mutación en un objetivo (el mensaje o una clave del contexto), foto de las entradas antes de llamar (el
   par mensaje-contexto en los cuatro validadores de mensajes y en el sello; las CUATRO entradas en
   `dimensionar` y los datos más el `ahora` en `vigilar`, con `_igual_nan` —la ampliación r01 de la
   revisión; el `ahora` es hoy una cadena inmutable y la foto queda por si el tipo cambia—), y después, si
   no lanzó: (a) la respuesta es una lista de registros con `regla`, `ruta` y `mensaje`;
   (b) la foto y el par después de la llamada son iguales con `_igual_nan` (llano daría falso positivo con
   NaN: nan != nan — la comparación llana de `datos` en H era el falso positivo que destapó el repaso propio);
   (c) una segunda llamada con copias profundas da la misma respuesta (independiente del orden de la lista);
   y solo entonces, si la mutación es «de forma», la exigencia de falla cerrado (§2 punto 4).

3. **«De forma» ajustado al contrato JSON (`_forma_real`).** El generador clasifica todo `borrar` como forma,
   pero borrar un ELEMENTO DE LISTA no rompe la forma mientras la lista siga dentro de su mínimo: el
   documento sigue conformando y lo que dispara, si algo, es una regla de contenido (en el sello, S-12: el
   hash ya no cuadra, que es exactamente lo que la pieza promete para las mutaciones de valor que respetan
   la forma). La batería reclasifica ese caso como «de valor» (sin tocar el generador importado) EXCEPTO
   cuando el borrado deja la lista VACÍA o por debajo de su `minItems` del esquema: entonces el documento YA
   NO conforma y la mutación vuelve a ser «de forma», con la tabla de mínimos POR MENSAJE `_MIN_ITEMS`
   extraída de los cuatro esquemas 0.2.0 (regla r03 de la revisión: la misma clave puede tener mínimo en un
   esquema y no en otro —`data_refs` lo tiene en el sobre y en el encargo, pero no en el informe—). El resto
   usa la clasificación importada tal cual (clave extra, clave requerida de menos en un dict, tipo
   cambiado). Todos los esquemas de los cuatro mensajes declaran `additionalProperties: false` en todos sus
   objetos, de modo que una clave extra en el MENSAJE siempre acaba en V-01/E-01/C-01/S-01.

4. **Falla cerrado con la regla correcta del diseño.** La forma del MENSAJE exige su regla de esquema:
   V-01, E-01, C-01 o S-01. La forma del CONTEXTO solo exige no quedar vacío cuando la mutación toca lo que
   ESTE mensaje consulta, y admite la regla semántica que el diseño asigna (funciones `_afecta_sobre`,
   `_afecta_encargo` y `_calendario_afecta`, con el destino de cada ADMITE_* en la cabecera de la batería):

   - `validar_sobre` lee: `ahora` y `fecha_corte_encargo` (siempre), el perfil citado (V-02), la
     ratificación de la clase de ESE perfil (V-06), la bandera de apalancamiento cuando el sobre declara
     capital con apalancamiento ≠ 1 (V-15) y, con el registro del Motor en el contexto, `sc3` y
     `sello_encargo` (V-26): son claves que el Orquestador pasa SIEMPRE (orquestador.py; hallazgo 2 de la
     revisión), así que la batería reconstruye la vista SC-3 de cada base (`_vista_sc3_de`, una entrada por
     artefacto citado, con el modelo que cada cifra declara) y muta ambas claves, que admiten V-01 (vista o
     sello ilegibles) y V-26 (vista legible que deja de respaldar las citas); una vista legible o `None` se
     admite sin regla, porque el validador no puede discrepar con ella (se recomputa, no se firma, como el
     calendario). Mutar otro perfil, la ratificación de otra clase o una ratificación de más no rompe ESTE
     sobre; en las bases todas declaran apalancamiento 1, así que la bandera jamás cambia el resultado.
   - `validar_encargo` solo valida el sello citado en `sello_corte_ref` (E-16; los mandatos del contexto se
     validan enteros, `set(m) == CLAVES`, y la bandera de apalancamiento no cambia nada con mandatos que
     declaran `apalancamiento_max` 1); las claves opcionales del contrato 0.2.0 (`controles` y `motivo` de
     `resultado_politica`) pueden faltar sin efecto porque E-14 solo exige el resultado; y cada restricción es
     opcional por separado y solo estrecha (borrar una deja las demás; si no queda ninguna, E-01).
   - `validar_informe`: mutar el sobre que viaja en el contexto da C-02 por diseño (el informe ya no refiere
     ese sobre) en vez de C-01. Las claves `autoria_c` y `autoria_contradictor` que el Orquestador pasa
     cuando están configuradas se cubren con casos fijos r02 (hallazgo 2): con una autoría bien formada la
     C-11 dispara (otra autoría configurada → C-11; dict mal formado → el lanzamiento interno llega al
     envoltorio y da C-01); una de forma rota (lista) se queda SIN comprobación en silencio, porque
     `diversidad()` la trata como desconocida: comportamiento real fijado y anotado para una pieza futura
     (el Orquestador valida su configuración con `_autoria_ok`, así que no hay camino práctico).
   - En el MENSAJE, las claves que el esquema deja opcionales y una regla semántica exige por condición dan
     esa regla, no la de esquema: `modelo_ref` y `motor_id` de una cifra → V-08 (o V-20). Son excepciones
     documentadas, cada una con su justificación en la cabecera de la batería; no se cambia ningún validador
     para que encaje la prueba.
   - `dimensionar`: E-01 es la regla de forma de la SOLICITUD (campos exactos, política, precios, paso); una
     mutación de forma de una hoja semántica da la regla que el diseño le asigna (divisa o tipo de cambio
     roto → E-03 por F-12; dirección o stop incoherentes → E-02). A toda mutación de forma se le exige fallar
     cerrado: `ok` False, código E-01 a E-04 y cantidad finita, no negativa y 0 si no hay ok.

5. **El calendario del contexto se recomputa, no se firma.** `validar_sello` (y el E-16 del encargo) recomputan
   contra el calendario que K pasa en el contexto; no hay hash del calendario que verificar. Una mutación que
   no toca lo consultado (la `version`, la raíz de `mercados`, la estructura de un mercado DECLARADO por el
   sello o el año consultado de su lista `anios`) no puede discrepar con lo declarado y el sello sigue válido:
   no es dato roto para este sello. Mutar los festivos de un mercado declarado (quitar la lista o un
   elemento, o cambiar su tipo) solo puede hacer la recomputación más permisiva —o romper el constructor, y
   entonces el validador responde por sí solo—: no hay discrepancia detectable y se deja cubierto por las
   promesas generales (el predicado `_calendario_afecta` se ajustó en la revisión a cualquier operación, no
   solo al borrar). Lo que SÍ se exige de
   forma al calendario va en cuatro casos fijos: sin `version`, `mercados` no dict, `anios` con texto o
   `hora_cierre_utc` mal formada → S-01 (el constructor de `Calendario` lanza `EntradaInvalida` y el envoltorio
   de `validar_sello` lo convierte; `SinCobertura` también está atrapado).

6. **Anidado a 500 niveles, un caso fijo por validador.** El generador del fin de semana no trae esa mutación,
   así que no se inventa dentro de él: cada validador recibe SU estructura fresca de 500 niveles colocada en
   una hoja (`data_refs[0]` del sobre y del encargo, `revisadas[0]` del informe, `fuente_id` del sello,
   `instrumento` de la solicitud de E y `EURUSD` de los datos de H). Los cuatro envoltorios de mensajes atrapan
   `RecursionError` (está en sus `ERRORES`), `dimensionar` captura `Exception` → E-01 y `vigilar` captura
   `Exception`: nadie lanza y todos fallan cerrado. Cada caso construye su estructura nueva: un `deepcopy` de
   una estructura así desbordaría la pila de la propia batería (~3 fotogramas de copia por nivel).

7. **Defecto_01: el permiso de apalancamiento ajeno (`validar_sobre`).** Con una mutación al azar de la
   bandera (`True` → «x») el sobre seguía válido aunque declarara `apalancamiento` 2: `validar_sobre` leía la
   bandera con `not ctx.get("apalancamiento_permitido", False)`, de modo que CUALQUIER valor verdadero ("x",
   NaN, [1], 1e308) contaba como permiso. El encargo CT-G-01 ya exige `is True` (`mandato_ok` lo recibe como
   `ctx.get("apalancamiento_permitido") is True`, y hay un caso inválido que lo fija:
   `inv_E01_permiso_como_texto_no_habilita_apalancamiento.json`). Regla 1: un dato raro no se lee a favor.
   Corrección mínima (una condición): `if "capital" in p and ctx.get("apalancamiento_permitido") is not True:`.
   La batería lo fija con dos comprobaciones: sobre con apalancamiento 2 y permiso «x» → V-15 (con el código de
   V0.53 no la da: «x» era verdadero y no se salta V-15 — la batería no es vacua), y sobre con apalancamiento 2
   y permiso `True` → sigue válido (la corrección no aprieta de más). Ninguna prueba antigua usaba un permiso
   no booleano, así que no cambia ninguna (el lote completo pasa).

8. **Las cuatro regresiones de la revisión independiente (r01 a r04).** Ningún hallazgo fue de producto:
   (r01, media) la batería no demostraba «no muta la entrada» para `dimensionar` ni para el `ahora` de
   `vigilar`: ahora hay foto con `_igual_nan` de las cuatro entradas de E (500 casos) y de T1 en H (200
   casos); el producto se quedó limpio en la sonda del revisor (300 casos sin mutación); (r02, media) las
   claves del contexto que el Orquestador pasa siempre no se mutaban: `sc3` y `sello_encargo` entran en la
   rotación del sobre (ADMITE V-01/V-26) y la autoría del informe, en cinco casos fijos; el §1 y este punto
   4 se corrigen en consecuencia; (r03, baja) `_forma_real` contaba todo borrado de elemento de lista como
   «de valor» sin mirar el mínimo: los borrados que dejan la lista vacía o bajo su `minItems` vuelven a ser
   «de forma» (tablas por mensaje `_MIN_ITEMS`) y exigen la regla de esquema, con los casos de las listas
   con mínimo de los cuatro mensajes fijados uno a uno (`data_refs`, `cartera_compatible` e `incertidumbre`
   del sobre; `data_refs` y `exclusiones` del encargo; `revisadas`, `escenarios_fallo` y `evid_refs` del
   informe; `mercados`, `fuentes`, `resultado_reglas` e `instrumentos` del sello); (r04, baja) la promesa
   «toda mutación de valor que respeta la forma da al menos S-12» era falsa para `estado`, excluido del
   hash por diseño: la excepción se declara aquí (§2 punto 3 y §3) y en el LEEME, y el comportamiento real
   (sin S-12; el encargo lo ve con E-16) queda fijado con dos comprobaciones. Las cinco sondas del revisor
   (`sondas_revisor_v060.py`) siguen cerrando y los cuatro guiones de hallazgos (`hallazgo_1..4_…py`, en
   la raíz de `marcoC/`) terminan en exit 0 tras las correcciones.

## 3. Reglas y comprobaciones

| Código (regla o aviso) | Qué comprueba | Efecto |
| --- | --- | --- |
| V-01 / E-01 / C-01 / S-01 (forma del mensaje) | Toda mutación de forma del mensaje (clave extra, requerida de menos, tipo cambiado, fecha mal formada, versión desconocida, número no finito) acaba en la regla de esquema del mensaje; también el borrado que deja una lista vacía o bajo su minItems (r03); y con un valor anidado a 500 niveles no lanza y da la misma regla | Rechazo; lista de registros {regla, ruta, mensaje} |
| V-02 / V-06 (contexto del sobre) | Mutar el perfil citado o la ratificación de su clase da V-02 o V-06; mutar los de otros perfiles puede dejar el sobre válido (no es dato roto para este sobre) | Rechazo solo cuando toca lo que este sobre consulta |
| V-15 (defecto_01) | Un permiso de apalancamiento ausente o ajeno ("x", NaN, [1]) NO habilita: apalancamiento ≠ 1 con permiso «x» → V-15; con permiso `True` → válido | Corrección en `validar_sobre`; dos comprobaciones fijas |
| E-01 / E-02 (contexto del encargo) | Mutar el perfil citado (consumer o candidato) da E-01 o E-02; mutar otro perfil no afecta | Igual que V-02 |
| E-16 (sello citado) | Toda mutación del sello CITADO en `sello_corte_ref` llega a E-16 (el sello ya no valida para K: S-01, S-12…); mutar un sello del contexto que no se cita no afecta | Rechazo del encargo con el sello roto o ausente |
| E-17, E-05, E-07, E-10 (mandatos) | Los mandatos del contexto se validan enteros: clave de más o de menos, tipo cambiado o contenido tocado da E-01/E-17 (la huella ya no cuadra) o la regla de restricciones que corresponda | Rechazo |
| S-12 (integridad del sello) | Toda mutación de VALOR del sello que respeta la forma deja el hash sin cuadrar: al menos S-12. Excepción por diseño declarada (r04): `estado`, excluido del hash porque cambia en la vida del sello, puede alterarse dentro del enum sin S-12 | Rechazo (falla cerrado con el hash) |
| V-01 / V-26 (sc3 y sello_encargo del contexto del sobre) | Las claves que el Orquestador pasa siempre entran en la rotación (r02): vista ilegible o sello no textual → V-01; vista legible que deja de respaldar las citas → V-26; None o vista legible sin discrepancia se admite (el validador no puede verla) | El camino del Motor SC-3 queda cubierto |
| S-01 (calendario del contexto, casos fijos) | Calendario sin `version`, sin `mercados`, con `anios` de texto o `hora_cierre_utc` mal formada → S-01 (el constructor lanza y el envoltorio convierte) | Rechazo; el calendario roto no pasa |
| E-01 a E-04 (dimensionado) | Nunca lanza; cantidad finita, no negativa y 0 si no hay ok; la forma de la solicitud da E-01 y las hojas semánticas, su regla (E-02/E-03) | Sin cantidad si algo no cuadra |
| H con datos rotos (vigilar) | Con datos que `_dato_fresco` no da por frescos, la posición sigue ABIERTA, el intermediario no recibe órdenes nuevas e `integridad()` queda vacía tras cada caso; con datos que siguen frescos tras la mutación (un precio enorme, una clave extra), H puede actuar con normalidad (es lo que la pieza pide: «con datos rotos») | No cierra ni reduce nada con datos rotos |
| {regla, ruta, mensaje} (los seis) | La respuesta es siempre una lista de registros con esas tres claves | Contrato de salida estable |
| r01 (no muta, revisión) | `dimensionar` no muta ninguna de sus cuatro entradas en 500 casos (foto con `_igual_nan`) y `vigilar` no muta el `ahora` en 200 casos | Promesa completa para los seis validadores |
| r02 (autoría del Orquestador, revisión) | Informe válido con `autoria_c` coherente y `autoria_contradictor` configurada; autoría de forma rota (lista) se queda sin comprobación en silencio (fijado, anotado para una pieza futura); dict mal formado → C-01; otra autoría bien formada → C-11 | Cobertura de las claves de autoría |
| r03 (minItems, revisión) | Los borrados que dejan la lista vacía o bajo su minItems dan la regla de esquema (V-01, E-01, C-01, S-01) en los cuatro mensajes | La forma se exige también al vaciar listas |
| r04 (estado del sello, revisión) | `estado` alterado dentro del enum → sello VÁLIDO y sin S-12 (el hash lo excluye por diseño) y el encargo lo ve con E-16 | Excepción declarada y comportamiento fijado |

## 4. Códigos, API, pruebas y revisión independiente

Ficheros cambiados o nuevos (la lista exacta de la entrega):

- `pruebas/pruebas_robustez_validadores.py` (NUEVO, 75 comprobaciones: las 65 de la pieza y 10 de regresión
  de la revisión): generador y fixtures (2); sobre: 7 bases válidas + 5 promesas agregadas (nunca lanza,
  registros, no muta, determinista, forma con excepciones) en 300 casos; defecto_01 (2); encargo: 2 bases +
  5 promesas en 300 casos; informe: 1 base + 5 promesas en 300 casos; r02, autoría del Orquestador (5);
  sello: 7 bases + 4 casos fijos del calendario + 6 promesas en 300 casos (300 rotados 4:1 entre el sello y
  el calendario); r03, borrados bajo minItems (1 agregada); r04, estado del sello (2); dimensionar: 1 base +
  5 promesas en 500 casos (la de no-mutar es r01); vigilar: 1 base + 7 promesas en 200 casos (la de no-mutar
  `ahora` es r01); anidado a 500 niveles (6); determinismo de la batería (1). Semilla 20261110; ~31 s de
  reloj, menos de los 90 que pide la pieza; dos ejecuciones consecutivas producen la misma salida byte a
  byte.
- Guiones de la revisión (INTACTOS byte a byte, tal como los entregó el revisor, en la raíz de `marcoC/`):
  `sondas_revisor_v060.py` y `hallazgo_1..4_revision_v060_…py`; en verde tras las correcciones (los cuatro
  hallazgos en exit 0 y las cinco sondas cierran). Su informe está copiado en
  `entrega_glm/V0.60/informe_revision_independiente.md`.
- `validador/validar_sobre.py` (defecto_01): la condición de V-15 pasa de
  `not ctx.get("apalancamiento_permitido", False)` a `ctx.get("apalancamiento_permitido") is not True`,
  con comentario que cita al encargo. Solo cambia el comportamiento con valores verdaderos no booleanos,
  que ninguna prueba antigua usaba: las 49 baterías anteriores pasan sin tocar ni una línea.
- `LEEME.md`: cabecera V0.60, párrafo «Fecha: 9 de noviembre de 2026», fila de la batería nueva en la tabla,
  línea en la lista de ejecución y punto «Comprobado en la robustez de los validadores», con las excepciones
  nuevas declaradas (estado del sello, minItems, sc3/sello_encargo y autoría) y el recuento actualizado.
- `entrega_glm/V0.60/`: este Documento 0, `revision.md` (con el informe y la corrección de los cuatro
  hallazgos), `notas_deuda.md`, `notas_briefing.md`, `salida_pruebas.txt` (el lote completo: 50 baterías —las
  49 de V0.53 y la nueva—, todas en «TODAS LAS PRUEBAS PASAN», sin una sola línea FALLA) y
  `informe_revision_independiente.md` (copia fiel del informe del revisor).

No hay cambios de esquema, configuración, parámetros ni migraciones (regla 10: nada que registrar;
`pruebas_migraciones_t03.py` en verde lo confirma). No se toca el Orquestador (regla 3). No se borra ni se
debilita ninguna prueba existente (regla 7): la batería solo AÑADE comprobaciones (las 65 de la pieza y las
10 de regresión) y las antiguas quedan intactas. No hay códigos nuevos (regla 6): solo se ejercitan los
existentes.

Revisión independiente: **ejecutada el 9 de noviembre de 2026, con cuatro hallazgos (2 medios, 2 bajos)
todos corregidos y ninguno de producto**. El revisor verificó contra el código real (el lote completo en
su propia ejecución, la batería con cuenta exacta y dos salidas idénticas, la no-vacuidad del defecto_01
contra la línea de V0.53 restaurándola y restituyéndola byte a byte, los predicados contra lo que los
validadores de verdad leen, y cinco sondas adversariales propias); el informe íntegro está en
`entrega_glm/V0.60/informe_revision_independiente.md` y el detalle de cada corrección con su regresión, en
`revision.md`.

Auto-repaso del paso 6: los caminos repasados y lo que destapó — (a) comparación llana de `datos` en H:
`dm != antes` contaba una mutación inexistente cuando el veneno dejaba un NaN en los datos (nan != nan); las
demás secciones ya usaban `_igual_nan` y H se alineó con ellas (el generador puede dejar NaN en cualquier
hoja, es una jugada legal del veneno); (b) `dict(fuentes["pol"])` en la segunda llamada de determinismo de E
reventaba cuando la mutación dejaba `pol` escalar en la raíz: ahora `copy.deepcopy`, que acepta cualquier
valor; (c) `entradas_e()` copiaba la política en superficial y una mutación profunda habría retorcido
`POLITICA_DEFECTO` para los casos siguientes (contaminación entre casos y del caso base
`dimensionar_base_ok_y_limitada_por_F04`): ahora copia profunda; (d) `deepcopy` de la estructura anidada de
500 niveles desbordaba la pila de la batería antes de llegar al validador: cada caso construye la suya fresca;
(e) las demandas de forma se revisaron una a una contra lo que cada validador de verdad lee (§2 punto 4), con
el criterio de no debilitar: cada excepción exige que la mutación NO toque lo consultado, y las reglas de
forma del mensaje se mantienen estrictas. Sobre mutaciones antes de validar: los seis validadores son de solo
lectura sobre sus entradas (lo prueba la comprobación de no-mutar con foto en cada caso, 1.900 veces); nada
lanza hacia fuera (envoltorios con `RecursionError` y `MemoryError` dentro, comprobados también con la
estructura anidada); casos frontera en la batería: raíz sustituida por escalar, listas vaciadas, NaN e
infinitos en hojas y raíces, fechas imposibles y sin zona, claves extra en cada nivel, sello no citado,
mercados no declarados, años no consultados, calendario roto en su constructor y anidado a 500 niveles.

Número de baterías que pasan: 50 ejecuciones (las 49 de `pruebas/pruebas_*.py` de V0.53 más la nueva),
todas terminan en «TODAS LAS PRUEBAS PASAN» y sin ninguna línea FALLA (lote completo en
`salida_pruebas.txt`).

## 5. Límites y deuda técnica

- La batería demuestra las promesas sobre 1.900 casos más doce casos fijos con una semilla fija: es
  reproducible, no exhaustiva. Las mutaciones son valores JSON (sin objetos raros, ciclos ni claves no
  textuales), igual que en V0.37; el anidado a 500 niveles cubre el único camino de recursión profunda de la
  lista de la pieza.
- Las excepciones por diseño son clases, no casos sueltos: «mutación del contexto que no toca lo que este
  mensaje consulta» y «clave opcional del contrato que una regla semántica exige por condición». Cada una
  está justificada en la cabecera de la batería y codificada en un predicado (`_afecta_sobre`,
  `_afecta_encargo`, `_calendario_afecta`) que mira lo que el validador de verdad lee; si el validador
  cambiara sus lecturas, el predicado habría que ajustarlo (y eso sería señal, no ruido).
- El calendario del contexto no está firmado y su integridad queda fuera de `validar_sello`: se recomputa
  contra él, de modo que una manipulación que no produce discrepancia con lo declarado en el sello no es
  detectable por este validador (la firma del calendario sería una decisión de contrato, no de esta pieza).
  Los casos fijos acotan lo que sí se exige: el calendario roto en su constructor no pasa.
- La promesa de H se mide sobre los DATOS ROTOS (lo que pide la pieza): una mutación que deja los datos
  frescos (un precio enorme, una clave extra) puede actuar con normalidad, y así se comprueba
  (`vigilar_cubre_casos_rotos_y_frescos`).
- El defecto_01 afectaba solo a llamadas con un permiso no booleano verdadero; el Orquestador siempre pasa un
  booleano, así que el efecto práctico era latente. Se corrige igualmente: los validadores son funciones
  públicas y la regla 1 no distingue entre el dato que llega del Orquestador y el que llega de fuera.
- La autoría de forma rota en el contexto del informe (`autoria_c` o `autoria_contradictor` como lista) se
  queda sin comprobación de coherencia EN SILENCIO: `diversidad()` la trata como desconocida y el informe
  sigue válido (fijado con r02). No hay camino práctico: el Orquestador valida su configuración con
  `_autoria_ok`; distinguir «ausente» (None, legítimo) de «mal formada» (C-01) queda anotado para una pieza
  futura (sugerencia del revisor).
- Los predicados `_afecta_sobre`, `_afecta_encargo` y `_calendario_afecta` tienen granularidad gruesa en
  algunas ramas (cuentan como «afecta» mutaciones que el validador no consulta, p. ej. cualquier clave bajo
  `clases_ratificadas[perfil]`): con los fixtures y la semilla actuales no produce fallos espurios; si una
  pieza futura cambia los fixtures, conviene saberlo (fragilidad de prueba, no de producto; observación del
  revisor).
- Filas de deuda que cambian: **ninguna**. El único defecto real que apareció (defecto_01) está corregido y
  fijado, así que no abre fila; la pieza no añade ni resuelve ninguna otra (`Deuda_tecnica.md` queda intacto).
