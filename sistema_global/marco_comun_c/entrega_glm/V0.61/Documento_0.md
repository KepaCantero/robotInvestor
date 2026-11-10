# Documento 0 — catálogo de códigos (V0.61) — GLM, revisado (ocho hallazgos de la revisión corregidos)

## 1. Problema y alcance

El sistema tiene unos 250 códigos de resultado y de aviso repartidos por módulos (O, F, CF, G, H, D, RM, V,
E, R, C, Q, S, K, CT, PE, DI, MG, RL y CL) y no había una lista única con lo que significa cada uno. Nada
impedía que una pieza nueva reutilizara un código con otro sentido, usara uno sin documentarlo o dejara uno
documentado que ya no existe; el prefijo E es el ejemplo: lo usan el encargo (E-01 a E-17) y el dimensionado
(E-01 a E-04) con significados distintos. Es la deuda T-60 de este kit (pieza 2) y cierra el punto del
hallazgo 8 de la pasada de coherencia: «el prefijo identifica la pieza, no el tipo de regla», hasta que la
Constitución fije uno propio.

Entra en esta versión: el módulo nuevo `validador/catalogo_codigos.py` con `CATALOGO` (282 entradas: las 281
parejas `(modulo, codigo)` que aparecen como constantes de texto enteras recorriendo los 21 módulos de
`validador/`, 18 de ellos con constantes: consola, motor y parametros no emiten ninguna,
más E-06 documentada como retirada), las funciones `codigos_en_el_codigo(carpeta)`,
`prefijos_del_leeme(ruta)` y `como_markdown()`, la lista `COLISIONES_ADMITIDAS` con los dieciséis pares de
módulos que comparten códigos y su explicación, la batería nueva `pruebas/pruebas_catalogo_codigos.py` (23
comprobaciones), el registro de prefijos del LEEME completado (R, K, CL, PE, DI, MG y RL; la fila O
actualizada a O-00 a O-39) y el catálogo entregado como tabla Markdown en
`entrega_glm/V0.61/catalogo_codigos.md`. La deuda abre T-60 como RESUELTO y añade las filas T-61 y T-62 por
los dos choques reales que aparecieron y no se resuelven (O-00 y O-01).

Queda fuera: renombrar o unificar códigos (la aceptación de la pieza lo prohíbe: si dos usos chocan de
verdad, se anota y no se toca nada), la versión de introducción de cada código (`"desde"` queda a None, §2
punto 4), los identificadores de tarea T-xx de la deuda (no son códigos de resultado y como constantes
enteras no aparecen: el minado con `ast` no los ve) y cualquier cambio en el Orquestador o en los
validadores (regla 3).

## 2. Diseño

1. **El catálogo es una constante, no un cálculo.** `CATALOGO` es un diccionario literal con la clave
   `(modulo, codigo)` —el nombre del fichero de `validador/` sin `.py`— y el valor `{"que", "efecto",
   "desde"}`. Los avisos del Orquestador (familia O en `orquestador`) llevan además `"prioridad"`, la de
   `PRIORIDAD_AVISO`, y `"MEDIA"` cuando no figura en ella, que es exactamente como los trata el propio
   Orquestador (`prio = PRIORIDAD_AVISO.get(codigo, "MEDIA")`). Los códigos con muchos sitios de emisión de
   significados distintos llevan además `"familia": True` y un texto de nivel familia (hoy O-00, O-01 y O-02
   del Orquestador; revisión, hallazgo 4). Los códigos retirados llevan `"retirado": True` y `"motivo"`: hoy
   solo E-06 (retirada en CT-G-01 0.2.0, T-51), que no aparece en el código y por
   eso la batería la excluye de la comprobación de códigos muertos; el catálogo solo da de alta la retirada
   del contrato vigente —las menciones históricas del LEEME (D-03, retirada en V0.17; G-07, sin uso) no son
   filas del catálogo—, criterio declarado tras la revisión (hallazgo 7). El módulo no está en `MODULOS_ESQUEMA`
   y no añade ninguna constante a los módulos que sí están: `pruebas_migraciones_t03.py` sigue en verde sin
   registrar nada.

2. **Los textos no se inventan.** Cada `"que"` sale de una de estas fuentes, en este orden: el mensaje con
   el que el código se emite (minado de las llamadas y de las tuplas del módulo), el docstring del módulo
   (partiendo las listas «Reglas: X-01 …; X-02 …»), el comentario de la línea que lo emite (F-09, F-11,
   O-37, Q-04, Q-11, V-17, V-19…), el nombre de los casos inválidos de su batería, que documentan la regla
   (E-02 «destinatario distinto o perfil no construido», V-05 «n1 sin capital / n3 sin capa3»…) o el LEEME
   para tres reglas que solo están ahí (R-13, R-14 y V-02). Los códigos que un módulo reutiliza de otro con
   el mismo significado heredan el texto del módulo primario de su familia (los F del Orquestador y del
   dimensionado vienen de `control_f`; los PE/DI/O de diario, migraciones y rotación, de `persistencia` y
   `orquestador`). Resultado: **cero «(sin documentar)»** y ningún texto vacío; la batería sigue contando
   ambos para el futuro.

3. **El efecto es una clasificación por contrato del módulo.** RECHAZA por defecto (validadores, G, D, RM,
   CT, PE, MG, CL y la mayoría de DI y RL); **REDUCE** para las siete reglas de F que no vetan sino que
   APRUEBAN CON MENOS CANTIDAD (F-03, F-04, F-06, F-07, F-13, F-14 y F-15: `control_f` las responde con
   «REDUCE» y devuelve «REDUCIDO» con `cantidad_aprobada > 0` —`control_f.py:260`— y sus copias del
   Orquestador heredan el efecto; clasificarlas RECHAZA contradecía al propio módulo y a este punto, que ya
   las llama «que REDUCE»: hallazgo 3 de la revisión, con el efecto nuevo en `EFECTOS` y el conjunto en
   `REGLAS_QUE_REDUCEN`); BLOQUEA para las reglas de F que vetan (las que responden VETA), para las reglas Q
   que bloquean la emisión del sello (K-00 incluida: el docstring de `k_calidad` dice «devuelve BLOQUEO
   (K-00) y no emite sello»), para DI-05/DI-06 (el diario se bloquea), RL-04 (el reloj se bloquea sin
   contrastar) y H-13 (no se envía nada por esa posición); AVISO para los avisos del Orquestador (los
   emitidos con `_aviso` o con prioridad en `PRIORIDAD_AVISO`; los demás O son rechazos de operación),
   para la familia H salvo las que preparan o ejecutan una acción (H-01, H-02, H-04, H-05, H-08, H-10, H-11
   y H-12: INFORMA) y H-13 (BLOQUEA); INFORMA también para G-11 (orden de entrada viva); y AVISO también
   para Q-01 y Q-10, que SOLO emiten ADVERTENCIA (`k_calidad.py:292` y `:476`; el sello sí se emite, con
   ADVERTENCIA, y S-13 liga Q-01 a que el corte difiera de la fecha solicitada: hallazgo 2 de la revisión).
   Tres filas Q son MIXTAS según el factor de la política —Q-04, Q-05 y Q-09 emiten ADVERTENCIA o
   BLOQUEO— y quedan en BLOQUEA por su efecto dominante (falla cerrado), anotado aquí fila a fila
   (observación 2 de la revisión). Reparto final: 182 RECHAZA, 14 REDUCE, 39 BLOQUEA, 38 AVISO y 9 INFORMA.
   Es una clasificación documental, no una comprobación del efecto real de cada llamada; la parte
   verificable la vigila ahora la batería (r02 y r03).

4. **`"desde"` queda a None en todas las entradas.** La versión que introdujo cada código solo se puede
   afirmar con el historial (GLM no toca git) y el LEEME menciona los códigos fuera de orden (el párrafo de
   V0.60 menciona V-26, que es de V0.33), de modo que la primera mención no prueba nada. El campo existe y
   la batería no lo exige; rellenarlo sería inventar.

5. **`codigos_en_el_codigo(carpeta)` usa `ast`, no grep.** Recorre los `.py` ordenados de `carpeta` (salvo
   `catalogo_codigos.py`), analiza cada fichero con `ast.parse` y recoge los `ast.Constant` de tipo str que
   casan ENTEROS con la expresión de la pieza (una o dos letras mayúsculas, guion y dos cifras). Un comentario no
   cuenta, una mención dentro de un mensaje más largo no cuenta (los f-strings aportan partes estáticas que
   no casan enteras), una clave de diccionario sí (`PRIORIDAD_AVISO`) y un fichero con la sintaxis rota no
   lanza: no aporta códigos (falla cerrado). La batería lo fija con una carpeta temporal (`sonda.py` con un
   comentario «O-99», una constante «O-98» y una mención «O-97» dentro de un f-string; `roto.py` con la
   sintaxis rota) y con el determinismo de dos llamadas.

6. **`prefijos_del_leeme(ruta)`** lee la sección «Registro de prefijos de códigos» del LEEME y devuelve los
   prefijos de la primera columna de la tabla, sin el guion («V», «RM», «PE»…). La batería comprueba que
   todo prefijo usado está registrado, que ninguno registrado está sin uso y que esta pieza completó el
   registro con los seis que faltaban: R (estaba citado en las notas de la fila E, pero no como fila propia),
   K (el envoltorio de falla cerrada de K, K-00), CL (rotación de la clave) y PE, DI, MG y RL (T-03). La
   fila O se actualiza a «O-00 a O-39» (O-37 y O-38 dejaron de estar «reservados» cuando llegaron con las
   piezas de GLM en V0.53 y el registro se había quedado atrás).

7. **`COLISIONES_ADMITIDAS`: dieciséis pares, dos choques reales.** El minado con `ast` encontró 250 códigos
   distintos y 281 parejas módulo-código; los códigos compartidos por más de un módulo solo son admisibles
   si el par está en la lista con su explicación. Dieciséis pares (el recuento «quince» que declaraban estos
   documentos era erróneo: hallazgo 5 de la revisión, y la batería fija ahora el número con r05): la E del
   encargo y la del dimensionado (el
   caso que motivó la pieza), mandatos con el validador del encargo (SC-1 valida la forma de las
   restricciones con los mismos códigos E), los códigos de F que el Orquestador lleva como constantes para
   acotar anulaciones y el dimensionado usa como frontera de viabilidad (mismo código y significado: son de
   F), la infraestructura T-03 reutilizando PE/DI/O con el mismo significado (documentado en sus
   docstrings) y **dos choques reales que no se resuelven**, declarados en `CHOQUES_REALES` y vigilados por
   r01: O-00, que en el Orquestador es el rechazo de un instante inválido (y la envoltura de excepciones al
   ejecutar una operación o comprobar un registro) y en el Diario la marca de la operación que lanza una
   excepción no recogida (deuda T-61; el catálogo daba el MISMO texto en los dos módulos: hallazgo 1), y
   O-01, que en el Orquestador es un rechazo genérico de la operación pedida —el «resto_parcial: solo
   CANCELAR» fue solo el caso que motivó la anotación (hallazgo 4)— y en G la ausencia de precio del
   intermediario o un instante ilegible (deuda T-62). Conforme a la aceptación de la pieza: se anotan en el
   Documento 0 y en la deuda, sin renombrar nada.

8. **`como_markdown()`** devuelve la tabla completa ordenada por módulo y código (módulo, código, qué hace,
   efecto, prioridad, desde y notas de retirada); se guarda en `entrega_glm/V0.61/catalogo_codigos.md` para
   pasarla a documento. La batería comprueba que las filas de la tabla son exactamente `sorted(CATALOGO)`.

9. **`sitios_de_emision(carpeta)`** (de la revisión, hallazgos 2 y 4): mina con `ast` las llamadas que
   emiten cada código —sitios, mensajes literales distintos y resultados y envoltorios de esas llamadas
   («BLOQUEO», «ADVERTENCIA», `_bloqueo`)— para que la batería pueda exigir que el efecto de las reglas Q/K
   sea el real del módulo (r02) y que los códigos con cinco o más mensajes distintos no documenten un solo
   caso con su ruta (r04).

## 3. Reglas y comprobaciones

| Código (regla o aviso) | Qué comprueba | Efecto |
| --- | --- | --- |
| CATALOGO (282 entradas) | La clave es `(modulo, codigo)` con el código en su forma de dos cifras y el valor lleva `que`, `efecto` y `desde`; los avisos del Orquestador llevan `prioridad` y los retirados, `retirado` y `motivo` | Catálogo de solo lectura; sin cambios de esquema |
| todo el código está en el catálogo | Los 281 pares que `codigos_en_el_codigo` saca de `validador/` están en `CATALOGO`; la prueba lista los que falten | Coherencia código-catálogo |
| todo el catálogo está en el código | No hay códigos muertos, salvo los retirados con `retirado: True` y su motivo (E-06) | Sin códigos documentados que ya no existen |
| colisiones solo las admitidas | Todo código compartido por dos módulos tiene su par en `COLISIONES_ADMITIDAS` con explicación; cada pareja admitida comparte al menos un código | Los choques reales quedan anotados (T-61, T-62) |
| prefijos y LEEME | Todo prefijo usado está en el registro del LEEME; ninguno registrado sin uso; el registro completo con R, K, CL, PE, DI, MG y RL tras esta pieza | Registro de prefijos al día |
| prioridades | Cada aviso de `PRIORIDAD_AVISO` está en el catálogo con esa prioridad; los 40 avisos del Orquestador llevan prioridad válida (ALTA, MEDIA o BAJA) | Contrato de los avisos |
| textos | Ningún `que` vacío y menos de diez «(sin documentar)» (hoy: cero) | Nada documentado a medias |
| efectos | El efecto es siempre uno de RECHAZA, REDUCE, AVISO, BLOQUEA, INFORMA y OK | Clasificación estable |
| como_markdown | La tabla Markdown devuelve exactamente `sorted(CATALOGO)` ordenada por módulo y código | Entrega en `catalogo_codigos.md` |
| ast, no grep | `codigos_en_el_codigo` es determinista, excluye el propio módulo y, con una carpeta temporal, ignora comentarios, menciones dentro de mensajes y ficheros con la sintaxis rota | La función de la pieza, no un grep |
| choques reales (r01) | Para cada choque declarado en `CHOQUES_REALES` (O-00 T-61, O-01 T-62), los textos `que` de los dos módulos son distintos y su par está admitido; ninguna explicación «CHOQUE REAL» cita una deuda sin choque declarado | Los choques no vuelven a converger |
| reglas Q y K (r02) | Toda fila Q/K con efecto BLOQUEA tiene un BLOQUEO real en `k_calidad` (llamada con «BLOQUEO» o el envoltorio `_bloqueo`) y toda fila AVISO advierte sin bloquear nunca | El efecto es el real del módulo |
| reglas que REDUCEN (r03) | Las siete reglas de F que aprueban con menos cantidad y sus copias del Orquestador llevan efecto REDUCE; ninguna otra fila lo lleva y `control_f.py` conserva el mapa | El efecto dice qué pasa con la orden |
| códigos genéricos (r04) | Un código con cinco o más mensajes de emisión distintos no cita en su texto una ruta literal de un mensaje; las filas «familia» (O-00, O-01 y O-02 del Orquestador) no copian ni caben en un solo mensaje | El texto de un código genérico no es un caso suelto |
| recuento de pares (r05) | `COLISIONES_ADMITIDAS` tiene los dieciséis pares que declaran el Documento 0, el LEEME y las notas del briefing | Los documentos no se quedan atrás |

## 4. Códigos, API, pruebas y revisión independiente

Ficheros nuevos o cambiados (la lista exacta de la entrega):

- `validador/catalogo_codigos.py` (NUEVO): docstring con el diseño; `CATALOGO` (282 entradas),
  `COLISIONES_ADMITIDAS` (dieciséis pares), `CHOQUES_REALES`, `REGLAS_QUE_REDUCEN`, `EFECTOS` (con REDUCE),
  `codigos_en_el_codigo(carpeta)`, `sitios_de_emision(carpeta)`, `prefijos_del_leeme(ruta)` y
  `como_markdown()`. Fuera de `MODULOS_ESQUEMA`.
- `pruebas/pruebas_catalogo_codigos.py` (NUEVO, 23 comprobaciones): estructura del catálogo, coherencia
  código-catálogo en los dos sentidos, retirados con motivo, colisiones admitidas con explicación,
  prefijos del LEEME en ambos sentidos, prioridades de `PRIORIDAD_AVISO` y de los 40 avisos, textos no
  vacíos y menos de diez sin documentar, efectos válidos, `como_markdown` ordenada y completa,
  determinismo de dos llamadas, sonda de `ast` contra grep con carpeta temporal y E-06 retirada; y las
  cinco regresiones de la revisión r01 a r05 (choques reales con textos distintos, BLOQUEO real de las
  reglas Q/K, REDUCE de las reglas que recortan, textos de familia y recuento de pares).
- `LEEME.md`: cabecera con «y catálogo de los códigos de resultado y de aviso — V0.61», párrafo «Fecha: 9
  de noviembre de 2026» de esta pieza, registro de prefijos completado (filas R, K, CL, PE, DI, MG y RL;
  fila O actualizada a O-00 a O-39) y remitido al catálogo, fila de la batería nueva en la tabla, línea en
  la lista de ejecución y punto «Comprobado en el catálogo de códigos».
- `Deuda_tecnica.md` (su cambio NO viaja en el ZIP: hallazgo 6 de la revisión): T-60 «Catálogo de códigos
  al día» como RESUELTO en V0.61, y las filas nuevas T-61 (choque O-00 Orquestador/Diario) y T-62 (choque
  O-01 Orquestador/G), sin resolver por decisión de la aceptación de la pieza (no se renombra nada); su
  contenido viaja resumido en `notas_deuda.md` de esta carpeta.
- `entrega_glm/V0.61/`: este Documento 0, `revision.md` (resultado de la revisión),
  `informe_revision_independiente.md` (el informe íntegro del revisor), `notas_deuda.md`,
  `notas_briefing.md`, `catalogo_codigos.md` (un preámbulo de encabezamiento y, debajo, la salida exacta de
  `como_markdown()`; observación 1 de la revisión) y `salida_pruebas.txt` (el lote completo en verde); las
  sondas del revisor viajan en `sondas_revisor_v061.py`, en la raíz (con la ruta relativa a la raíz de
  `marcoC`, única adaptación respecto al original).

No hay cambios de esquema, configuración ni parámetros (regla 10: el módulo no está en `MODULOS_ESQUEMA`,
no añade constantes a `CONFIG_DEFECTO` ni a los módulos que la integran, y `pruebas_migraciones_t03.py`
pasa sin registrar nada; `version_config` sigue en CFG-0.11.0). No se toca el Orquestador ni ningún
validador (regla 3). No se cambia ningún código de error existente (aceptación de la pieza). No se borra ni
se debilita ninguna prueba antigua (regla 7). No hay códigos nuevos de resultado: el catálogo documenta los
existentes (regla 6).

Revisión independiente: ejecutada el 9 de noviembre de 2026 en otra conversación, con el ZIP en verde y el
prompt de la sección 9, sin el historial de la pieza (informe íntegro en `informe_revision_independiente.md`
de esta carpeta y sondas en `sondas_revisor_v061.py`, en la raíz). Resultado: ocho hallazgos (cuatro medios,
cuatro bajos), ninguno de producto: tres filas o grupos de filas del catálogo con significado o efecto
equivocados y el límite de los códigos genéricos sin declarar (hallazgos 1 a 4, corregidos con las
regresiones r01 a r04), el recuento de pares (hallazgo 5, corregido en los documentos y fijado con r05), el
fichero de deuda ausente (hallazgo 6, resuelto citando `notas_deuda.md`), el criterio de retiradas sin
declarar (hallazgo 7, declarado en §2 punto 1) y cuatro frases de recuento (hallazgo 8). Ver `revision.md`.

Auto-repaso del paso 6: los caminos repasados y lo que destapó — (a) el primer minado de códigos usaba
`finditer` sobre los docstrings y contó «HA-25» dentro de «SHA-256» y las tareas T-xx como códigos: la
función entregada usa `ast` con casamiento ENTERO y los T-xx, que solo viajan dentro de textos más largos,
no aparecen; (b) `codigos_en_el_codigo` habría lanzado por un `.py` con la sintaxis rota: ahora lo salta
(falla cerrado) y hay una sonda; (c) `prefijos_del_leeme` devolvía los prefijos con el guion y la batería
los compara sin él: se normalizó a prefijos sin guion, documentado en su docstring; (d) el texto de los
códigos reutilizados se hereda del módulo primario de la familia en una segunda pasada (primero los
primarios, luego los secundarios), de modo que no hay texto tomado del módulo equivocado; (e) la batería
comprueba en ambos sentidos (código→catálogo y catálogo→código) y que cada pareja admitida comparte
realmente un código, para que la lista de colisiones no acumule pares que ya no existen; (f) los casos
frontera de la sonda: comentario con código, constante entera, mención dentro de un f-string y fichero con
la sintaxis rota.

Número de baterías que pasan: 51 ejecuciones (las 50 de V0.60 y la nueva `pruebas_catalogo_codigos.py`),
todas terminan en «TODAS LAS PRUEBAS PASAN» y sin ninguna línea FALLA (lote completo en `salida_pruebas.txt`).

## 5. Límites y deuda técnica

- El catálogo documenta los códigos TAL COMO están: no unifica, no renombra y no corrige los dos choques
  reales que encontró (O-00 entre Orquestador y Diario, T-61; O-01 entre Orquestador y G, T-62; la revisión
  matiza el segundo: el O-01 del Orquestador es un rechazo genérico y el resto_parcial solo fue el caso que
  motivó la anotación). Renombrar cualquiera de los dos exigiría migrar estados y diarios ya escritos o
  revisar pruebas y pantallas: es decisión del operador, no de esta pieza.
- `"desde"` queda a None en todas las entradas (§2 punto 4): rellenarlo sin el historial sería inventar.
- El efecto es una clasificación por contrato del módulo, no una comprobación del efecto real de cada
  llamada: un O-xx rechaza la operación o anota un aviso según el camino del Orquestador, y el catálogo
  recoge el efecto dominante documentado (§2 punto 3). Si una pieza futura cambia la conducta de un código,
  la fila del catálogo y su efecto se actualizan con ella. La revisión añadió la parte verificable: la
  batería exige el BLOQUEO real de las reglas Q/K (r02) y el REDUCE de las reglas que recortan (r03).
- Los códigos con muchos sitios de emisión de significados distintos o llevan un texto de nivel familia
  declarado con `"familia": True` (hoy O-00, O-01 y O-02 del Orquestador, que cubre los ~71 caminos del
  O-01, los 12 del O-02 y los 3 del O-00) o documentan el caso más representativo (p. ej. O-06 o O-15 del
  Orquestador): el catálogo no resume los mensajes de cada camino, y este límite lo declara la pieza
  (hallazgo 4 de la revisión). La batería (r04) impide que un texto de familia sea o copie un solo mensaje
  y que cualquier código con cinco o más mensajes distintos cite una ruta literal de su módulo.
- Los textos provenientes de los nombres de los casos inválidos de las baterías describen la regla por su
  caso más representativo (p. ej. E-02 «destinatario distinto o perfil no construido»): son la documentación
  que el propio repositorio da de cada regla, citados como fuente en el docstring del módulo.
- El catálogo mira solo `validador/`: los códigos que citan las pruebas o la documentación fuera de los
  módulos (pantallas, anotaciones del operador…) no se comprueban aquí; los módulos son la única fuente de
  códigos ejecutables.
- Filas de deuda que cambian: **T-60** (nueva, RESUELTO en V0.61), **T-61** y **T-62** (nuevas, los dos
  choques reales sin resolver). Ninguna fila anterior cambia.
