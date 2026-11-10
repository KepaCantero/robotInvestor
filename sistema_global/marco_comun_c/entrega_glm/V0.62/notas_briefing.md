# Notas del briefing — V0.62 (robustez de la infraestructura T-03)

V0.62, pieza 3 del kit 2: batería nueva `pruebas/pruebas_robustez_t03.py` (40 comprobaciones —las 39 de la
pieza y la regresión r01 añadida al aplicar la revisión— sobre 870 casos mutados al azar con la semilla
fija 20261111 más 2.250 casos del barrido r01 con 25 semillas nuevas —240 de persistencia rotando entre seis objetivos: el
estado del documento, la cabecera, la raíz, un documento firmado, el estado con la huella rehecha y el
instante de guardado; 180 del diario rotando entre una línea del fichero, el fichero de estado y los
argumentos de una operación; 150 de migraciones rotando entre el texto, el esquema, el registro, los
metadatos y el estado rehecho; 150 del reloj rotando entre la referencia externa, el estado, el incidente,
el rearme y las tolerancias del constructor; y 150 de rotación rotando entre el texto, las claves, los
metadatos, las rutas de los ficheros y el documento sin firmar— más casos fijos: el anidado a 500 niveles
en el estado, en el texto crudo y en una línea del diario, el anidado a 3.000 niveles que desborda la pila
en guardar, las rutas imposibles, la bóveda de la clave y las dos referencias del contraste que el veneno
no alcanza), ~21 s de reloj (~11 s sin r01) y salida idéntica byte a byte en dos ejecuciones; demostrar con ella las
cuatro promesas de robustez para la infraestructura T-03, que quedaron fuera de V0.37 y V0.60:
persistencia (`volcar`, `guardar`, `verificar`, `cargar`, `cargar_de` y la bóveda de la clave con
`escribir_clave`/`leer_clave`), diario (`crear`, `abrir` y las operaciones anotadas), migraciones
(`migrar`, `camino`), reloj (`Reloj`, `contrastar`, `comprobar_estado`, `rearmar`, `degradar_por_reloj`) y
rotación (`rotar`, `rotar_ficheros`) —nunca lanzan, salvo lo documentado (`volcar` con instante ilegible,
clave inválida o estado que JSON no guarda tal cual: `guardar` lo convierte en PE-01 o PE-07; el
constructor de `Reloj` con tolerancias imposibles; y las operaciones del diario cuyos argumentos el método
no acepta, que la envoltura anota O-00 y el diario sigue sirviendo), no mutan lo que no deben (foto
`_igual_nan` del Orquestador en volcar/verificar/cargar; sin cambio tras un RL-06; el fichero de estado
entero tras cada guardar fallido, con escritura atómica y sin temporales olvidados), son deterministas (el
par ok/código en dos llamadas con las mismas entradas; la batería entera, byte a byte) y fallan cerrado
con la regla correcta (toda mutación del estado sin rehacer la huella es PE-02 —con clave, PE-06: la firma
cubre toda la cabecera y el estado—; una línea del diario tocada es DI-02, o DI-03/DI-04 si el punto no
cuadra; el estado tocado no abre el diario; un texto mutado no se rota; un esquema no registrado es MG-01;
metadatos imposibles, MG-05 o CL-03; una referencia o un rearme imposibles, RL-06 sin bloquear; una
lectura de fuente imposible, RL-05 —o RL-01 en el monótono si el valor es finito pero descolocado— con
bloqueo). El generador de mutaciones es el de `pruebas_robustez.py` (V0.37) importado sin cambiarlo —con
una adaptación local documentada: capturar el valor devuelto, porque una mutación «valor» en la raíz de un
escalar devuelve el objeto nuevo sin tocar el original y sería un no-op silencioso— y el texto corrupto se
serializa con `json.dumps` normal para que el NaN literal llegue a la carga, que es lo que debe rechazar;
los fixtures vienen de `pruebas_orquestador` y `pruebas_reloj_t03`, importados sin cambiarlos. Excepciones
por diseño declaradas en la cabecera de la batería: una cabecera mutada que respeta la forma puede cargar
(la huella cubre el estado, no la cabecera; lo que miente lo ven montar con PE-03 o la integridad con
O-13), `migrar` sobre un documento de este código responde ok con «nada que migrar» y el MISMO texto, y
una operación aplicada puede responder ok False con razón (un rechazo del Orquestador también se anota y
se reproduce). Sin defectos reales: los módulos T-03 ya cumplían las promesas y la batería las demuestra y
las fija (la no-vacuidad quedó demostrada con sondas antes de entregar y re-verificada tras corregir:
desactivar la comprobación de la huella en `persistencia.py` hace fallar la batería en cinco
comprobaciones —las dos de PE-02, la del estado del diario, la de rotación sin firmar y r01—, y desactivar
la cadena de hashes del diario en `diario.py`, en tres —las dos de DI-02 y r01—; el «exactamente en sus
comprobaciones» que declaraba la entrega antes de la revisión era impreciso, hallazgo 2). Sin cambios de
esquema del código ni de configuración (esquema V0.53
sin migración; ninguna constante nueva en módulos de `MODULOS_ESQUEMA`), sin tocar el Orquestador ni
ningún módulo de `validador/` y sin borrar ni debilitar ninguna prueba antigua: las 52 baterías del lote
(las 51 de V0.61 y la nueva) acaban en «TODAS LAS PRUEBAS PASAN» y sin una sola línea FALLA
(`entrega_glm/V0.62/salida_pruebas.txt`, regenerada tras corregir); `Deuda_tecnica.md` intacto (la pieza no abre ni resuelve
ninguna fila; su contenido viaja resumido en `notas_deuda.md`). Ficheros: batería nueva y la entrega en
`entrega_glm/V0.62/` (Documento 0, revision.md, notas, manifiesto SHA-256 de los ficheros heredados,
informe del revisor y salida del lote), `corre_baterias.py` y `sondas_revisor_v062.py` en la raíz.
Revisión independiente ejecutada el 9 de noviembre de 2026: cuatro hallazgos (uno medio, tres bajos),
ninguno de producto, corregidos — el medio (hallazgo 1) con la regresión r01: los `esperados` de cuatro
objetivos no admitían el PE-03 que una cabecera mutada produce, y las franquicias muertas de otros seis se
retiraron.
