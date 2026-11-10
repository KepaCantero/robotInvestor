# Informe de revisión independiente — V0.61 (pieza 2 del kit 2: catálogo de códigos)

**Revisor:** GLM (conversación independiente, sin el historial de la pieza; 9 de noviembre de 2026)
**Alcance:** `validador/catalogo_codigos.py` (NUEVO), `pruebas/pruebas_catalogo_codigos.py` (NUEVO), cambios en
`LEEME.md`, `entrega_glm/V0.61/*` y el estado V0.60 pos-revisión que viaja en el mismo ZIP.
**Método:** verificación contra el código real (no contra lo que declara la entrega): lote completo ejecutado por
el revisor, minado independiente de códigos con un método distinto al de la pieza (`tokenize`, frente al `ast` de
la pieza), recuentos propios, contraste de cada fila muestreada del catálogo con lo que su módulo emite de verdad,
y cinco sondas adversariales propias (`sondas_revisor_v061.py`, adjuntas al informe).

**Resultado: 8 hallazgos (4 medios, 4 bajos), ninguno de producto.** El catálogo está completo y la batería es
no-vacua para la coherencia código↔catálogo; los hallazgos son de exactitud del CONTENIDO del catálogo (textos y
efectos de filas concretas) y de los documentos. Detalle abajo; cada hallazgo con su corrección y su regresión
propuesta (`r01_…` a `r05_…`, en `pruebas/pruebas_catalogo_codigos.py`).

---

## 1. Lo verificado en verde (evidencia de la propia ejecución del revisor)

1. **Lote completo en verde:** 51 baterías ejecutadas por el revisor, todas terminan en «TODAS LAS PRUEBAS PASAN»,
   sin una línea FALLA; coincide con `salida_pruebas.txt`. La batería nueva da **18 comprobaciones** (claim: 18) y
   es determinista: dos corridas con salida idéntica byte a byte.
2. **Recuentos del catálogo:** `CATALOGO` tiene **282** entradas (claim: 282); los pares minados de `validador/`
   son **281** (claim: 281) y **250** códigos distintos (claim: 250). Mi minado independiente con `tokenize`
   coincide al 100 % con el de la pieza (`ast`): ninguna pareja de diferencia en ninguno de los dos sentidos.
   Ningún `T-xx`, «HA-25» de «SHA-256» ni fragmento de f-string entró en el catálogo.
3. **Coherencia en ambos sentidos:** todo lo que aparece en el código está en el catálogo y viceversa (salvo E-06,
   retirada con su motivo). Reparto de efectos verificado: **196 RECHAZA / 41 BLOQUEA / 36 AVISO / 9 INFORMA** =
   282. `"desde"` a `None` en todas. Las 20 claves de `PRIORIDAD_AVISO` (15 ALTA, 5 MEDIA) están reflejadas con su
   valor y los 40 códigos O del Orquestador llevan prioridad válida.
4. **La batería no es vacua para la estructura:** sonda S1 (constante nueva `H-99` inyectada en una copia de
   `validador/`) → la batería FALLA exactamente en `todo_codigo_en_el_codigo_esta_en_el_catalogo`; sonda S4
   (entrada `H-19` borrada del catálogo) → FALLA como debe.
5. **Registro de prefijos del LEEME:** completo y coherente en ambos sentidos (20 prefijos usados = 20
   registrados); esta pieza añadió R, K, CL, PE, DI, MG y RL y actualizó la fila O a «O-00 a O-39», tal como
   declara.
6. **Colisiones: la lista está COMPLETA** — los 16 pares de módulos que comparten códigos están en
   `COLISIONES_ADMITIDAS`, todos con explicación y todos compartiendo realmente código; ninguno sobra ni falta
   (verificado en ambos sentidos). (El problema es el NÚMERO que declaran los documentos: hallazgo 5.)
7. **Sin cambios de esquema ni de configuración:** `catalogo_codigos` no está en `MODULOS_ESQUEMA`;
   `pruebas_migraciones_t03.py` en verde sin registrar nada. No se toca el Orquestador ni ningún validador; no se
   borra ni debilita ninguna prueba antigua (diff V0.60→V0.61: solo los ficheros declarados).
8. **El estado V0.60 que viaja en el ZIP es el pos-revisión íntegro:** `Documento_0.md`, `revision.md` y
   `salida_pruebas.txt` de `entrega_glm/V0.60/` son idénticos byte a byte a los ficheros pos-revisión; los guiones
   `sondas_revisor_v060.py` y `hallazgo_1..4_…` cierran en exit 0 en mi ejecución.
9. **Entrega Markdown:** las 282 filas de `catalogo_codigos.md` son idénticas a `como_markdown()` (el fichero añade
   solo un preámbulo de cuatro líneas; véase observación 1).
10. **Fuentes de los textos, por muestreo:** R-13/R-14 (LEEME), V-17/V-19 (comentarios), O-06/O-07/O-10 emitidos
    vía `_aviso` (coherente con la clasificación AVISO). Ningún texto vacío, cero «(sin documentar)».

## 2. Hallazgos

| # | Gravedad | Hallazgo | Corrección propuesta | Regresión |
| --- | --- | --- | --- | --- |
| 1 | **media** | **(`diario`, `O-00`) documenta el significado del ORQUESTADOR.** El catálogo dice «instante inválido o anterior al último», pero el Diario emite O-00 SOLO para «excepción al aplicar {metodo}» (`diario.py:167`; docstring línea 23: «Una operación que lanza una excepción no recogida por @_seguro se anota con la marca de la excepción (O-00)»). La fila contradice al propio módulo, a `COLISIONES_ADMITIDAS` (que sí lo explica bien), al Documento 0 §2 punto 7 y a notas_deuda (T-61). Es exactamente el error que la pieza existe para evitar | `que` de (`diario`, `O-00`) = «operación que lanzó una excepción no recogida: se anota y se reproduce igual» | `r01_los_pares_con_choque_real_tienen_textos_distintos_por_modulo`: para cada par con «CHOQUE REAL» en su explicación, exigir que los textos `que` de los dos módulos sean distintos (con el catálogo actual, r01 falla: no-vacua) |
| 2 | **media** | **Efecto BLOQUEA falso en `Q-01` y `Q-10`.** Ambas SOLO emiten ADVERTENCIA (`k_calidad.py:292` y `:476`; única emisión cada una) y el sello SÍ se emite («si no hay BLOQUEO, emite el sello», docstring de `emitir`; S-13 liga Q-01 a ADVERTENCIA). Contradice el criterio de la propia pieza (§2 punto 3: «BLOQUEA … para las reglas Q que BLOQUEAN la emisión del sello») y la definición de BLOQUEA del propio módulo («el sello no se emite»). La fila de Q-01 además se contradice a sí misma: su texto dice «se recorta al hábil anterior» (y sigue) | Efecto de Q-01 y Q-10 = AVISO (advierte; el sello se emite con ADVERTENCIA) | `r02_el_efecto_BLOQUEA_de_las_reglas_Q_exige_un_BLOQUEO_real`: para cada fila Q/K con efecto BLOQUEA, el módulo debe poder emitir BLOQUEO para ese código (con el catálogo actual, r02 falla en Q-01 y Q-10) |
| 3 | **media** | **14 filas RECHAZA que en realidad APRUEBAN con menos cantidad.** F-03, F-04, F-06, F-07, F-13, F-14 y F-15 en `control_f` y sus copias en `orquestador` tienen efecto RECHAZA («la operación no se acepta»), pero `control_f` devuelve `resultado: "REDUCIDO"` con `cantidad_aprobada > 0` (`control_f.py:260`): la orden queda APROBADA, recortada. El propio Documento 0 §2 punto 3 las llama «que REDUCE» — y las da de alta como RECHAZA sin declarar el mapeo | O se añade `REDUCE` a `EFECTOS` y se clasifica así esas 14 filas, o se declara explícitamente el mapeo REDUCE→RECHAZA en §2 punto 3 y en el docstring (hoy ni una cosa ni la otra) | `r03_las_reglas_que_REDUCEN_no_son_RECHAZA`: para las reglas del conjunto REDUCE declarado, el efecto no puede ser RECHAZA sin nota que lo declare |
| 4 | **media** | **Textos de códigos genéricos tomados de UNA sola emisión, sin declarar el límite.** (`orquestador`, `O-01`) tiene ~71 sitios de emisión con significados distintos (cartera desconocida, cotización mal formada, sello no válido, encargo mal formado, registro CT-G-14 sin event_id…) y el catálogo describe solo «condiciones_entrada.resto_parcial: solo se admite CANCELAR (T-12)», uno de ellos. (`orquestador`, `O-00`): 3 usos y DOS significados (instante inválido Y envoltura de excepciones, `orquestador.py:413`); solo documenta el primero. (`orquestador`, `O-02`): 12 usos de idempotencia («ya registrado», «ya acusado», «ya activo»); solo documenta el de niveles de pérdida. §5 Límites no declara la regla «cuando un código se emite con mensajes distintos, se toma UNO», y la narrativa del choque T-62 hereda la estrechez: «resto_parcial» no es EL significado de O-01 en el Orquestador, es uno de 71. (El propio choque T-61 queda matizado: la excepción que marca el Diario coincide con el uso 413 del Orquestador; lo exclusivo del Orquestador es el instante) | Textos de nivel FAMILIA para O-00, O-01 y O-02 del orquestador (p. ej. O-01: «rechazo genérico de la operación pedida: entrada no admitida o condición incumplida; se emite en muchos caminos —entre ellos, resto_parcial distinto de CANCELAR—») y límite declarado en §5 | `r04_codigos_con_muchas_emisiones_llevan_texto_de_familia`: para todo código con ≥5 mensajes de emisión distintos en su módulo, el `que` no puede citar literalmente un caso concreto con su ruta (sonda S2: hoy la batería pasa igual con el texto corregido — no hay nada que lo vigile) |
| 5 | **baja** | **«Quince pares» frente a DIECISÉIS reales.** `COLISIONES_ADMITIDAS` tiene 16 pares (todos necesarios: verificado en ambos sentidos; la propia batería imprime «16 pares admitidos»), pero Documento 0 (§1 y §2 punto 7), LEEME (párrafo de fecha y punto «Comprobado») y notas_briefing dicen «quince» | Sustituir «quince» por «dieciséis» en los cinco sitios | `r05` (misma batería, detalle): el mensaje de la comprobación de colisiones ya imprime el recuento; basta corregir los documentos — y opcionalmente una comprobación de que el recuento citado en Documento 0 y catálogo coincide |
| 6 | **baja** | **`Deuda_tecnica.md` declarado como cambiado (§4: T-60 RESUELTO, T-61, T-62) pero NO viaja en el ZIP** (tampoco viajaba en el de V0.60): el cambio no es verificable en la entrega. `notas_deuda.md` suple el contenido, pero el fichero citado no está | Incluir `Deuda_tecnica.md` en el ZIP o citar en §4 que su contenido viaja resumido en `notas_deuda.md` de la carpeta | Ninguna (documental) |
| 7 | **baja** | **Criterio de retiradas sin declarar.** El catálogo da de alta solo E-06 como retirada, pero el LEEME registra también D-03 «retirado en V0.17» y G-07 «no se usa»: ¿por qué E-06 sí y D-03 no? Falta el criterio (p. ej. «solo retiradas del contrato vigente») o la fila de D-03 | Declarar el criterio en §2 punto 1 o añadir D-03 con `retirado`/`motivo` | `r06` opcional: todo código citado como «retirado» en el LEEME debe estar en el catálogo con `retirado: True` |
| 8 | **baja** | **Exactitud menor de los textos.** (a) «las 281 parejas … en los 21 módulos de `validador/`»: 21 módulos se RECORREN, pero solo 18 contienen constantes de código (consola, motor y parametros no emiten ninguno); el LEEME dice «250 códigos distintos en 21 módulos». (b) Docstrings y Documento 0 dicen «dos letras mayúsculas» y la expresión real es `[A-Z]{1,2}` (una o dos: V-, E-, F-, G-…) | Ajustar las cuatro frases («recorriendo los 21 módulos, 18 de ellos con códigos»; «una o dos letras») | Ninguna (documental) |

**Ningún hallazgo es de producto:** no hay ningún cambio de conducta en los validadores ni en el Orquestador;
`validar_sobre.py` y el resto de módulos V0.53/V0.60 están intactos frente al ZIP anterior (diff por fichero). Las
promesas de la pieza que sí se cumplen: cobertura completa código↔catálogo (con método propio de minado
confirmado), registro de prefijos al día, colisiones completas, batería determinista y no-vacua para la estructura.

## 3. Sondas del revisor (`sondas_revisor_v061.py`)

| Sonda | Qué prueba | Resultado |
| --- | --- | --- |
| S1 | Constante nueva `H-99` en una copia de `validador/` | La batería FALLA en la comprobación de cobertura (como debe) |
| S2 | Texto de (`diario`, `O-00`) corregido al significado real del Diario | La batería SIGUE EN VERDE → ningún check protege la exactitud de los textos (hueco que explotan los hallazgos 1 y 4) |
| S3 | Efecto de (`k_calidad`, `Q-01`) corregido a AVISO | La batería SIGUE EN VERDE → ídem efectos (hallazgo 2) |
| S4 | Entrada `H-19` borrada del catálogo | La batería FALLA (control positivo de S1) |
| S5 | Conteos auxiliares | 250 códigos distintos (claim ✓); «O-01» ×71, «O-00» ×3, «O-02» ×12 en `orquestador.py` |

## 4. Observaciones (sin corrección exigida)

1. `catalogo_codigos.md` = preámbulo de 4 líneas + la salida EXACTA de `como_markdown()` (282 filas idénticas). El
   §4 lo llama «la salida de `como_markdown()`»: o se regenera sin preámbulo o se ajusta la frase.
2. Q-04, Q-05 y Q-09 emiten ADVERTENCIA o BLOQUEO según el factor de la política: BLOQUEA es defendible como
   efecto dominante, pero conviene anotar en §2 punto 3 qué filas son mixtas (hoy la simplificación solo está
   declarada «en bloque», no fila a fila).
3. (`dimensionado`, `F-11`) con BLOQUEA describe su uso como frontera de viabilidad (→ E-04): coherente con la
   clasificación «por contrato del módulo»; se mantiene.
4. El reparto AVISO/RECHAZA dentro de la familia O cuadra con el mecanismo real de emisión (`_aviso` frente a
   `_no`), verificado por muestreo (O-06, O-07, O-10 vía `_aviso`; O-11, O-14 vía `_no`).

## 5. Resultado

Cuatro hallazgos medios (1–4: tres filas o grupos de filas del catálogo con significado/efecto equivocados y el
límite de los códigos genéricos sin declarar) y cuatro bajos (5–8: recuento de pares, fichero de deuda ausente,
criterio de retiradas y exactitud menor), **todos de documentación, ninguno de producto**. Con las correcciones
r01–r05 la batería quedaría en ~22–23 comprobaciones y el catálogo cumpliría su promesa («una lista única con lo
que significa cada uno») también en el contenido, no solo en la cobertura. T-60 puede quedar RESUELTO tras las
correcciones; T-61 y T-62 siguen abiertas como decisión del operador (los choques son reales, aunque la descripción
de ambos queda matada por el hallazgo 4: O-01 en el Orquestador es un código genérico y el «resto_parcial» es solo
el caso que motivó la anotación).
