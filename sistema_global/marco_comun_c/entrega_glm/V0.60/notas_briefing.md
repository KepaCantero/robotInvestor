# Notas del briefing — V0.60 (robustez de los seis validadores de mensajes)

V0.60, pieza 1 del kit 2: batería nueva `pruebas/pruebas_robustez_validadores.py` (75 comprobaciones
agregadas —las 65 de la pieza y las 10 de regresión r01–r04 de la revisión independiente— sobre 1.900 casos
mutados al azar con la semilla fija 20261110 —300 por cada validador de mensajes rotando entre el mensaje y
cada clave de su contexto, 500 para `dimensionar` entre sus cuatro entradas y 200 para `vigilar` con
Orquestador e intermediario nuevos en cada caso— más doce casos fijos: cuatro de calendario del contexto
roto → S-01, dos del defecto_01 y seis de un valor anidado a 500 niveles, uno por validador), ~31 s de
reloj y salida idéntica en dos ejecuciones consecutivas; demostrar con ella las cuatro promesas de la
pieza de robustez del fin de semana sobre los seis validadores que quedaron fuera: `validar_sobre.validar`,
`validar_encargo.validar_encargo`, `validar_contradictor.validar_informe`, `k_calidad.validar_sello`,
`dimensionado.dimensionar` y `vigilancia.vigilar` —nunca lanzan (también con RecursionError: los
envoltorios lo atrapan y hay un caso anidado por validador), no mutan la entrada (foto antes y después con
`_igual_nan`, porque la comparación llana da falsos positivos con NaN; r01 añade la foto de las cuatro
entradas de E y del `ahora` de H), son deterministas (segunda llamada con copias profundas, respuesta
independiente del orden de la lista) y fallan cerrado con la regla correcta del diseño (V-01/E-01/C-01/S-01
en la forma del mensaje —también al vaciar una lista por debajo de su minItems, r03—; S-12 en toda mutación
de valor del sello que respeta la forma SALVO `estado`, excluido del hash por diseño y visto por el
consumidor con E-16, r04; E-01 a E-04 con cantidad finita, no negativa y 0 si no hay ok en `dimensionar`;
y en H, con datos rotos, la posición sigue ABIERTA, el intermediario no recibe órdenes nuevas e
`integridad()` queda vacía). El generador de mutaciones es el de `pruebas_robustez.py` (V0.37) importado sin
cambiarlo; la separación «de forma»/«de valor» se adapta al contrato JSON dentro de la batería
(`_forma_real`: borrar un ELEMENTO de lista no rompe la forma mientras la lista siga en su mínimo, y las
tablas de mínimos son POR MENSAJE, porque la misma clave puede tener minItems en un esquema y no en otro).
Las claves del contexto que el Orquestador pasa SIEMPRE se mutan (r02): `sc3` —con la vista del registro
del Motor reconstruida por base (`_vista_sc3_de`)— y `sello_encargo` admiten V-01/V-26, y la autoría del
informe va en casos fijos (autoria_c coherente deja el informe válido; de forma rota se queda sin
comprobación en silencio —diversidad() la trata como desconocida, anotado para una pieza futura—; dict mal
formado da C-01; otra autoría bien formada dispara C-11). Las mutaciones de forma del CONTEXTO solo exigen
no quedar vacío cuando tocan lo que ESTE mensaje consulta, con predicados documentados (`_afecta_sobre`:
el validador del sobre lee el perfil citado, la ratificación de su clase, la bandera de apalancamiento si
el sobre declara capital con apalancamiento ≠ 1, y sc3/sello_encargo por el camino V-26; `_afecta_encargo`:
E-16 solo valida el sello citado en `sello_corte_ref`, los mandatos se validan enteros y la bandera no
cambia nada con mandatos que declaran `apalancamiento_max` 1; `_calendario_afecta`: version, raíz de
mercados, estructura de un mercado declarado o año consultado —y los festivos, que no pueden producir
discrepancia detectable con lo declarado—), y las claves opcionales del contrato que una regla semántica
exige por condición dan su regla (modelo_ref/motor_id → V-08/V-20; controles y motivo de
resultado_politica, que no se exigen en ninguno de los dos contratos; cada restricción, que solo
estrecha); el calendario del contexto se recomputa, no se firma, y su forma va en cuatro casos fijos (sin
version, sin mercados, anios de texto, hora_cierre_utc mal formada → S-01).
UN defecto real corregido (defecto_01): `validar_sobre` leía `apalancamiento_permitido` con
`not ctx.get(..., False)` y tomaba por habilitado CUALQUIER valor verdadero ("x", NaN, [1]) mientras el
encargo CT-G-01 exige `is True` (`mandato_ok`); corregido al cambio mínimo (`ctx.get(...) is not True`), no
afecta a ninguna prueba antigua y lo fijan dos comprobaciones (permiso «x» con apalancamiento 2 → V-15; con
`True` → válido). Sin cambios de esquema del código ni de configuración (V0.53 sin migración; ninguna
constante nueva en módulos de `MODULOS_ESQUEMA`), sin tocar el Orquestador y sin borrar ni debilitar
ninguna prueba antigua: las 50 baterías del lote (las 49 de V0.53 y la nueva) acaban en «TODAS LAS PRUEBAS
PASAN» y sin una sola línea FALLA (`entrega_glm/V0.60/salida_pruebas.txt`); `Deuda_tecnica.md` intacto (el
defecto se corrigió, así que no abre fila). Revisión independiente ejecutada el mismo día: cuatro hallazgos
(2 medios, 2 bajos), ninguno de producto, todos corregidos con su regresión r01–r04 y documentados
(`revision.md` e `informe_revision_independiente.md`; los cinco guiones del revisor, intactos en la raíz
de `marcoC/`, cierran en verde). Ficheros: batería nueva; `validador/validar_sobre.py` (una condición); y
la entrega en `entrega_glm/V0.60/` (Documento 0, revision.md, notas y salida del lote).
