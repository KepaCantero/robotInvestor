# Notas del briefing — V0.61 (catálogo de códigos)

V0.61, pieza 2 del kit 2: módulo nuevo `validador/catalogo_codigos.py`, fuera de `MODULOS_ESQUEMA` (no
cambia el esquema del código y `pruebas_migraciones_t03.py` pasa sin registrar nada), con la constante
`CATALOGO` —clave `(modulo, codigo)` (el nombre del fichero de `validador/` sin `.py`), valor
`{"que", "efecto", "desde"}`; los avisos del Orquestador llevan `"prioridad"` (la de `PRIORIDAD_AVISO`,
«MEDIA» si no figura, como los trata `prio = PRIORIDAD_AVISO.get(codigo, "MEDIA")`), los códigos con muchas
emisiones de significados distintos llevan `"familia": True` y un texto de nivel familia (O-00, O-01 y O-02
del Orquestador), los retirados llevan `"retirado": True` y `"motivo"` (solo E-06, retirada en CT-G-01 0.2.0
y fuera del código: el catálogo solo da de alta la retirada del contrato vigente; D-03, retirada en V0.17,
sigue documentada en el LEEME)—, 282 entradas
(281 pares que aparecen como constantes de texto enteras recorriendo los 21 módulos de `validador/`, 18 de
ellos con constantes: 250 códigos distintos con las familias O, F, CF, G, H, D, RM, V, E, R, C, Q, S, K, CT,
PE, DI, MG, RL y CL, más E-06),
reparto de efectos 182 RECHAZA / 14 REDUCE / 39 BLOQUEA / 38 AVISO / 9 INFORMA y cero «(sin documentar)»; funciones
`codigos_en_el_codigo(carpeta)` (recorre los `.py` ordenados excluyéndose a sí mismo, `ast.parse` y solo
ast.Constant de tipo str que casan ENTEROS con la expresión de la pieza —una o dos letras mayúsculas, guion y dos
cifras—, de modo que comentarios y menciones dentro de mensajes más largos no cuentan; un fichero con la
sintaxis rota no lanza y no aporta códigos), `prefijos_del_leeme(ruta)` (la primera columna de la tabla
«Registro de prefijos de códigos», prefijos sin el guion) y `como_markdown()` (tabla completa ordenada por
módulo y código, entregada en `entrega_glm/V0.61/catalogo_codigos.md`); `COLISIONES_ADMITIDAS` con los
DIECISÉIS pares de módulos que comparten códigos y su explicación —la E del encargo y la E del dimensionado
(el caso que motivó la pieza), mandatos con validar_encargo (SC-1 valida la forma de las restricciones con
los mismos códigos E), los códigos de F que el Orquestador lleva como constantes para acotar anulaciones
(TOPES_F) y el dimensionado usa como frontera de viabilidad, y la infraestructura T-03 (diario, migraciones,
rotación) reutilizando PE/DI/O con el mismo significado— y DOS choques reales anotados sin renombrar nada
(declarados en `CHOQUES_REALES` y vigilados por r01):
O-00 (el rechazo de un instante inválido —y la envoltura de excepciones— en el Orquestador frente a la marca
de la operación que lanza una excepción no recogida en el Diario, deuda T-61; el catálogo daba el MISMO texto
en los dos módulos: hallazgo 1) y O-01 (un rechazo genérico de la operación pedida en el Orquestador —el
«resto_parcial: solo CANCELAR» fue solo el caso que motivó la anotación, hallazgo 4— frente a «el
intermediario no da precio o el instante es ilegible» en G, deuda T-62). Batería nueva
`pruebas/pruebas_catalogo_codigos.py`, 23 comprobaciones deterministas: el código y el catálogo no se
separan en ninguno de los dos sentidos (salvo los retirados con su motivo), las colisiones son solo las
admitidas y cada pareja admitida comparte realmente un código, todo prefijo usado está en el registro del
LEEME y ninguno registrado sin uso (el registro se completa con las filas R, K, CL, PE, DI, MG y RL y la
fila O pasa a O-00 a O-39; R estaba citado en las notas de la fila E sin fila propia), cada aviso de
`PRIORIDAD_AVISO` está en el catálogo con esa prioridad y los 40 avisos llevan una prioridad válida,
ningún texto vacío y menos de diez «(sin documentar)», efectos siempre de la lista de seis (RECHAZA, REDUCE,
AVISO, BLOQUEA, INFORMA y OK),
`como_markdown` exactamente `sorted(CATALOGO)`, determinismo de dos llamadas y una sonda con carpeta
temporal que fija el uso de `ast` (un comentario, una mención dentro de un f-string y un fichero con la
sintaxis rota no cuentan); y las cinco regresiones de la revisión r01 a r05: los dos choques reales con
textos distintos por módulo, BLOQUEO real para las reglas Q/K con efecto BLOQUEA (y AVISO sin bloquear para
Q-01 y Q-10, que solo emiten ADVERTENCIA), REDUCE para las reglas de F que aprueban con menos cantidad,
textos de familia para los códigos genéricos (sin citar la ruta de un caso) y el recuento de dieciséis
pares fijado. Los textos no se inventan: salen del mensaje del código, del docstring del
módulo (partiendo las listas «Reglas: X-01 …; X-02 …»), del comentario de la línea que lo emite (F-09
máximo de posiciones, F-11 valor mínimo, O-37 tope de LIBRES, Q-04 saltos, Q-11 envoltorio, V-17 rangos,
V-19 números sueltos…), del nombre de los casos inválidos de su batería (E-02 «destinatario distinto o
perfil no construido», E-13 «abrir con posición / cerrar sin posición»…) o del LEEME para R-13, R-14 y
V-02; los códigos reutilizados heredan el texto del módulo primario de su familia en una segunda pasada.
`"desde"` queda a None en todas las entradas (GLM no toca git y el LEEME menciona los códigos fuera de
orden; rellenarlo sería inventar). Sin cambios de esquema, configuración ni parámetros, sin tocar el
Orquestador ni ningún validador, sin borrar ni debilitar ninguna prueba antigua y sin cambiar ningún código
de error existente (aceptación de la pieza). `Deuda_tecnica.md`: T-60 RESUELTO en V0.61 y las filas nuevas
T-61 y T-62 por los choques no resueltos (el fichero no viaja en el ZIP: su contenido va resumido en
`notas_deuda.md`, hallazgo 6 de la revisión). Ficheros: `validador/catalogo_codigos.py` (NUEVO),
`pruebas/pruebas_catalogo_codigos.py` (NUEVA), `LEEME.md`, `Deuda_tecnica.md` y la entrega en
`entrega_glm/V0.61/`. Revisión independiente ejecutada el mismo día: ocho hallazgos (cuatro medios, cuatro
bajos), ninguno de producto, todos corregidos (regresiones r01 a r05 y documentos; ver `revision.md`).
