# Documento 0 — robustez de la infraestructura T-03 (V0.62) — GLM, revisado y corregido (cuatro hallazgos, ninguno de producto)

## 1. Problema y alcance

Las piezas de robustez anteriores dejaron la infraestructura T-03 fuera: la del fin de semana (V0.37)
demostró las cuatro promesas para F, D y CT-G-14, y la pieza 1 de este kit (V0.60) para los seis
validadores de mensajes. La infraestructura T-03 —persistencia del estado, diario de operaciones,
migraciones, reloj del sistema y rotación de la clave— tiene baterías funcionales exhaustivas
(`pruebas_persistencia_t03.py`, `pruebas_diario_t03.py`, `pruebas_migraciones_t03.py`,
`pruebas_reloj_t03.py`, `pruebas_rotacion_t03.py`, `pruebas_firma_t03.py`, `pruebas_jornada.py`), pero
ninguna prueba sistemática de las cuatro promesas de robustez con entradas imposibles: nunca lanzan, no
mutan lo que no deben, son deterministas y fallan cerrado con la regla correcta del diseño. Un `guardar`
que lance con una ruta rara, un `abrir` que retuerza lo que le pasan o una `migrar` que apruebe por
descuido romperían la regla 1 (falla cerrado) en el punto exacto donde el sistema decide si un estado, un
diario o un reloj dudosos vuelven a servir.

Entra en esta versión: una batería nueva, `pruebas/pruebas_robustez_t03.py`, con 40 comprobaciones —las 39
de la pieza y la regresión r01 añadida al aplicar la revisión— sobre 870 casos mutados al azar (semilla
fija 20261111) más 2.250 casos del barrido r01 con 25 semillas nuevas y casos fijos, que demuestra las
cuatro promesas para
los cinco módulos de la infraestructura. No corrige ningún defecto: los módulos T-03 ya cumplían las
promesas y la batería las demuestra y las fija (la no-vacuidad quedó demostrada con sondas antes de
entregar, §4).

Queda fuera: el Orquestador y los validadores (V0.37 y V0.60), el generador de mutaciones de
`pruebas_robustez.py`, que se importa sin cambiar ni una línea, y cualquier cambio de esquema,
configuración o migración: el esquema del código sigue siendo V0.53, no hay constantes nuevas en los
módulos de `MODULOS_ESQUEMA` ni en `CONFIG_DEFECTO`, y `pruebas_migraciones_t03.py` pasa sin registrar
nada. No se toca el Orquestador.

## 2. Diseño

1. **El generador y los fixtures, importados sin cambiarlos.** `_mutar_en_sitio` y `_igual_nan` vienen de
   `pruebas/pruebas_robustez.py` (V0.37) tal cual: una mutación al azar en un camino al azar (borrar una
   clave o un elemento, añadir una clave extra, cambiar un valor por None, "", "x", [], {}, True, 0, -1,
   1e308, NaN, ±inf o un número como texto, o cambiar una fecha por «2026-13-45», «ayer» o una fecha sin
   zona). Los fixtures (Orquestador hasta AUTORIZADA, fuentes de reloj simuladas) vienen de
   `pruebas_orquestador` y `pruebas_reloj_t03`. Única adaptación local: el generador sustituye la RAÍZ de
   un escalar por el veneno DEVOLVIENDO el objeto nuevo sin tocar el original, de modo que la batería
   captura siempre el valor devuelto (`_mutar_doc`, y las mutaciones de línea y de estado del diario) —
   si no, una mutación de cada tantas sería un no-op silencioso y el caso contaría como verde sin
   estresar nada. Y el texto corrupto se serializa con `json.dumps` normal (no con el `_texto` de la
   persistencia, que prohíbe NaN): un texto con un NaN literal es exactamente el input que `cargar`,
   `migrar` y `rotar` deben rechazar con PE-01.

2. **Los objetivos por módulo, con rotación.** Cada caso aleatorio muta UNA entrada de UNA función de
   entrada del módulo y exige las promesas:
   - **persistencia (240 casos, seis objetivos):** el ESTADO del documento (mutación sin rehacer la
     huella → PE-02 siempre; con NaN la huella es incanonicalizable → PE-01), la cabecera y la raíz
     (PE-01/PE-02/PE-03/PE-08), el documento FIRMADO tocado por cualquier sitio (PE-06: la firma cubre
     toda la cabecera y el estado; o PE-01 si la forma rompe antes), el estado con la huella REHECHA a
     propósito (lo que haría quien edita sabiendo cómo: OK, O-13 con kill-switch, PE-03 o PE-04 — y si
     carga sin kill-switch, el estado cargado vuelve a volcar EXACTAMENTE igual) y el instante de
     `guardar` (PE-01, y el fichero anterior queda entero y sin temporales: escritura atómica). Además:
     rutas imposibles en `guardar` (PE-05, el fichero bueno no cambia, sin temporales), la clave inválida
     (PE-07 sin escribir nada) y la bóveda (`escribir_clave`/`leer_clave` con valores y ficheros
     imposibles: PE-07, nunca pisa una clave existente, y los permisos 0644 o el contenido no hexadecimal
     no se leen).
   - **diario (180 casos, tres objetivos):** una LÍNEA del fichero de diario mutada (DI-02; DI-03/DI-04 si
     la cadena aguanta y el punto no cuadra; el OK de la regla del corte NO se admite aquí porque el
     objetivo escribe siempre el salto final y la última línea mutada es DI-02 — franquicia muerta
     retirada por la revisión: el caso sin salto final lo cubre el caso fijo de la línea cortada), el
     FICHERO DE ESTADO mutado (PE-01/PE-02/PE-03: el diario no abre un estado que la persistencia
     rechaza; PE-06 era franquicia muerta, el documento va sin firmar) y los ARGUMENTOS de una operación (`registrar_cotizacion` con el argumento
     mutado: la operación escribe exactamente cero líneas si DI-01 la rechaza o dos si se aplica — nunca
     una a medias — y una aplicación puede responder ok False con razón: un rechazo del Orquestador
     también se anota y se reproduce). Casos fijos: la última línea CORTADA a medias se ignora y se
     limpia (`linea_incompleta`, el fichero acaba en salto), y la última ENTERA pero tocada es DI-02; dos
     aperturas del mismo par de ficheros llegan al mismo estado (vuelta a volcar idéntica).
   - **migraciones (150 casos, cinco objetivos):** el texto mutado (PE-01/PE-02/PE-03 — el PE-03 lo añadió
     la revisión, hallazgo 1: una cabecera con el formato cambiado por otro texto—, u OK «nada que migrar»
     con la cabecera mutada — y entonces el texto de salida es EXACTAMENTE el de entrada), el esquema
     cambiado por uno no registrado (MG-01), el REGISTRO de migraciones y de esquemas con veneno
     (MG-01, nunca lanza: la envoltura de `migrar` convierte cualquier excepción; MG-02 era franquicia
     muerta: con el esquema actual el camino no llega a mirar el registro) y los metadatos
     (instante, motivo y actor imposibles: MG-05). Fijo: `camino` con un esquema sin camino o un registro
     roto responde None sin lanzar.
   - **reloj (150 casos, cinco objetivos):** la REFERENCIA externa mutada en `contrastar` (RL-06 sin
     bloquear, o RL-03 con bloqueo si es legible pero desfasada; si ok, el instante devuelto es ISO
     válido), el ESTADO mutado en `comprobar_estado` (RL-02 u OK), el INCIDENTE mutado en
     `degradar_por_reloj` (RL-06 «no cambia nada» con foto del Orquestador intacta; una mutación que no
     toca el código del incidente sigue siendo incidente y degrada TODAS las carteras a L1, que es lo
     correcto), el REARME con actor y motivo imposibles sobre un reloj sin bloqueo (RL-06) y las
     TOLERANCIAS del constructor con veneno (ValueError documentado, nunca otra excepción). Barrido fijo
     del VENENO completo en las dos fuentes ya contrastadas: pared imposible → RL-05 siempre; monótono
     imposible → RL-05, o RL-01 si el valor es finito pero descolocado (un salto del monótono); en ambos
     casos el reloj queda bloqueado. Y los dos caminos que el veneno no alcanza, fijos: la referencia
     válida dentro de la tolerancia → OK, y la desfasada → RL-03 con bloqueo.
   - **rotación (150 casos, cinco objetivos):** el texto firmado mutado (ok False con PE-01/PE-03/PE-06:
     un documento tocado no se rota — la firma se comprueba ANTES que la huella, así que PE-02 nunca
     llega; PE-03 con el formato tocado, añadido por la revisión, hallazgo 1), las claves imposibles
     (CL-01 para toda clave inválida, que `_previas` rechaza antes de cargar: PE-07 era franquicia
     muerta; PE-06 con una clave vieja None sobre un documento firmado; y las rotaciones que SÍ salen —
     K1→K2 con metadatos válidos — vuelven a cargar con la clave nueva), los metadatos imposibles
     (CL-03), las rutas imposibles de `rotar_ficheros` (PE-05/CL-04/CL-01, nunca lanza) y el documento
     SIN firmar mutado con clave vieja None (PE-01/PE-02/PE-03: la primera firma tampoco admite un texto
     roto; CL-02 era franquicia muerta). Fijo: el camino feliz K1→K2 sigue funcionando tras las mutaciones.

3. **Las promesas y sus excepciones por diseño, declaradas en la cabecera.** «Nunca lanzan» admite tres
   lanzamientos DOCUMENTADOS: `volcar` (ValueError con un instante ilegible, una clave inválida o un
   estado que JSON no guarda tal cual — `guardar` los convierte en PE-01 o PE-07), el constructor de
   `Reloj` (ValueError con tolerancias o fuentes imposibles) y una operación del diario cuyos argumentos
   el método no acepta (la envoltura `_aplicar` la anota como O-00 y el diario sigue sirviendo; es el
   diseño del diario, probado en su batería). «No mutan» se mide con foto `_igual_nan` del Orquestador en
   los lectores (`volcar`, `verificar`, `cargar`), tras un `degradar_por_reloj` RL-06 y sobre el fichero
   de estado tras cada `guardar` fallido; las operaciones que SÍ cambian estado por diseño (degradar con
   un incidente real, las operaciones aplicadas del diario) se comprueban por su efecto declarado
   (todas las carteras en L1; cero o dos líneas). «Deterministas»: dos llamadas con las mismas entradas
   dan el mismo par ok/código (la respuesta entera en las funciones puras), y la batería entera produce
   la misma salida byte a byte en dos ejecuciones (comprobación final con semilla propia).

4. **Anidado extremo, casos fijos.** Un valor anidado a 500 niveles en el ESTADO (con la huella rehecha):
   `cargar` nunca lanza y responde OK/O-13/PE-03/PE-04 — y si carga sin kill-switch, el estado vuelve a
   volcar exactamente igual. En el TEXTO crudo: `json.loads` desborda dentro de `verificar`, que lo
   atrapa (RecursionError está en su lista): PE-01 en `cargar`, `verificar`, `migrar` y `rotar` sin que
   ninguno lance. En una LÍNEA del diario: `_leer` lo atrapa → DI-02. Y a 3.000 niveles (los que el
   diario ya usa en su batería para su DI-01) en un atributo del Orquestador: `_solo_json` y `volcar`
   desbordan y `guardar` responde PE-01 sin escribir nada. Cada caso construye su estructura fresca (un
   deepcopy de una estructura así desbordaría la pila de la propia batería).

5. **Contaminación entre casos, controlada.** Los casos de «estado» del diario dejan el fichero de estado
   corrupto a propósito, así que cada caso de «línea» y de «estado», y cada caso fijo posterior, RESTAURA
   los dos ficheros antes de abrir (la observación 2 de la revisión corrigió el caso de «estado», que
   dejaba el diario del caso de «línea» anterior); los casos de argumentos usan un diario recién creado
   cada uno; y `migrar` y `rotar` son funciones puras (no escriben nada). La semilla es propia de esta
   pieza (20261111): la misma mutación nunca depende del orden de ejecución de otras baterías.

6. **Los esperados al contrato real del módulo, vigilados (r01, revisión hallazgo 1).** El `esperados` de
   cada objetivo declara los códigos que el módulo puede responder con el generador de la pieza, no solo
   los que la semilla fija sorteó: cuatro objetivos que mutan el documento entero admitían PE-03 y lo
   tenían fuera (un fallo en falso latente que la semilla 20261111 no sorteó), y las franquicias muertas
   (códigos declarados que el generador no puede producir) se retiraron. La regresión
   `r01_los_esperados_cubren_todo_lo_que_el_modulo_puede_responder` repite los 15 objetivos con
   `esperados` con 25 semillas nuevas y seis casos por objetivo y semilla (2.250 casos) y exige que el
   código observado quede dentro del esperado de su objetivo (y ok solo donde el objetivo lo admite):
   con la batería entregada, r01 habría fallado en los cuatro objetivos del hallazgo 1.

## 3. Reglas y comprobaciones

| Código (regla o aviso) | Qué comprueba | Efecto |
| --- | --- | --- |
| PE-01 / PE-02 (forma, huella) | Toda mutación del estado sin rehacer la huella da PE-02 (PE-01 si el veneno deja la huella incanonicalizable); la forma rota del documento o de la raíz, PE-01; una mutación de línea del diario, DI-02 | Rechazo; nunca se opera con un estado tocado |
| PE-06 (firma) | Un documento firmado tocado por CUALQUIER sitio (cabecera o estado) da PE-06: la firma cubre todo | La firma detecta cualquier retoque |
| PE-03 / PE-04 / O-13 (montar e integridad) | Una mutación del estado con la huella rehecha carga solo si este código la acepta; si carga sin kill-switch, vuelve a volcar exactamente igual; si no cuadra, kill-switch y O-13 | Lo que miente, se ve |
| PE-05 / PE-07 (escritura y clave) | Rutas imposibles en guardar y en la bóveda: PE-05/PE-07, sin fichero roto, sin temporales, sin pisar la clave | Falla cerrado con ficheros |
| DI-02 / DI-03 / DI-04 (diario roto) | Una línea tocada no se usa; el estado tocado no abre el diario; la última línea cortada se ignora y se limpia; dos aperturas llegan al mismo estado | El diario roto no se aplica |
| DI-01 y líneas exactas | Cada operación con argumentos mutados escribe cero o dos líneas, nunca una a medias | Registro previo a la escritura íntegro |
| MG-01 / MG-02 / MG-05 (migraciones) | Un esquema no registrado o un registro roto, MG-01; metadatos imposibles, MG-05; y «nada que migrar» devuelve el MISMO texto | Migrar no cambia nada sin camino |
| RL-01 / RL-02 / RL-03 / RL-05 / RL-06 (reloj) | Toda lectura de fuente imposible bloquea (RL-05, o RL-01 en el monótono); un estado con el reloj por delante, RL-02; una referencia desfasada, RL-03 con bloqueo; una referencia o un rearme imposibles, RL-06 sin bloquear y sin tocar el Orquestador | El reloj dudoso no da instantes |
| CL-01 / CL-03 (rotación) | Claves o metadatos imposibles no rotan; un texto mutado nunca se rota (ok False); una rotación ok vuelve a cargar con la clave nueva | La clave no se cambia con nada dudoso |
| r01 (esperados al contrato) | Barrido con 25 semillas nuevas × 6 casos por objetivo: los códigos que los módulos responden quedan dentro de los `esperados` de la batería, y ok solo donde el objetivo lo admite | Los esperados no son más estrechos que el contrato real |
| anidado extremo | 500 niveles en el estado, en el texto crudo y en una línea del diario; 3.000 que desbordan la pila en guardar: nadie lanza y todos fallan cerrado | RecursionError atrapado en la frontera |
| determinismo | Dos llamadas con las mismas entradas dan el mismo par ok/código; la batería entera, la misma salida byte a byte | Reproducible con semilla fija |
| no mutan | Foto `_igual_nan` del Orquestador en volcar/verificar/cargar; sin cambio tras RL-06; fichero entero tras cada guardar fallido | Los lectores no retuercen |

## 4. Códigos, API, pruebas y revisión independiente

Ficheros nuevos o cambiados (la lista exacta de la entrega):

- `pruebas/pruebas_robustez_t03.py` (NUEVO, 40 comprobaciones con la regresión r01): base común con y sin clave; persistencia
  (6 comprobaciones agregadas sobre 240 casos + rutas imposibles + clave inválida + bóveda + foto de
  no-mutar); diario (5 agregadas sobre 180 casos + dos aperturas + línea cortada y línea tocada);
  migraciones (4 sobre 150 casos + camino); reloj (4 sobre 150 casos + referencia válida y desfasada +
  barrido de veneno en las dos fuentes); rotación (4 sobre 150 casos + camino feliz); anidado extremo
  (4 casos fijos); regresión r01 (1, con 25 semillas nuevas × 6 casos por objetivo: 2.250 casos);
  determinismo de la batería (1). Semilla 20261111; ~21 s de reloj (~11 s sin r01); dos ejecuciones
  consecutivas producen la misma salida byte a byte.
- `LEEME.md`: cabecera con «y robustez de la infraestructura T-03 — V0.62», párrafo «Fecha: 9 de noviembre
  de 2026» de esta pieza, fila de la batería nueva en la tabla, línea en la lista de ejecución y punto
  «Comprobado en la robustez de la infraestructura T-03».
- `entrega_glm/V0.62/`: este Documento 0, `revision.md` (revisión ejecutada y correcciones aplicadas),
  `notas_deuda.md`, `notas_briefing.md`, `salida_pruebas.txt` (el lote completo en verde, regenerado tras
  corregir), `manifiesto_sha256.txt` (SHA-256 de los 107 ficheros heredados sin cambios, añadido por la
  revisión, hallazgo 4) y `informe_revision_independiente.md` (el informe íntegro del revisor). En la
  raíz del árbol: `corre_baterias.py` (el ejecutor del lote que citaba la salida, hallazgo 4) y
  `sondas_revisor_v062.py` (las sondas del revisor).

No hay cambios de esquema, configuración ni parámetros (regla 10: nada que registrar;
`pruebas_migraciones_t03.py` en verde lo confirma; `version_config` sigue en CFG-0.11.0). No se toca el
Orquestador ni ningún módulo de `validador/` (regla 3): la batería solo AÑADE comprobaciones. No se borra
ni se debilita ninguna prueba existente (regla 7). No hay códigos nuevos de resultado (regla 6): la pieza
no emite nada, solo estresa lo existente.

Revisión independiente: ejecutada el 9 de noviembre de 2026 — cuatro hallazgos (uno medio, tres bajos),
ninguno de producto, corregidos y documentados en `revision.md` de esta carpeta (el hallazgo 1 con la
regresión `r01_los_esperados_cubren_todo_lo_que_el_modulo_puede_responder`; los tres bajos, documentales:
frases de no-vacuidad, franquicias muertas retiradas y manifiesto SHA-256).

Auto-repaso del paso 6: los caminos repasados y lo que destapó — (a) el generador de mutaciones devuelve
el objeto NUEVO cuando sustituye la raíz de un escalar: la primera versión de la batería ignoraba el valor
devuelto y una de cada tantas mutaciones era un no-op silencioso (un caso «OK» que no estresaba nada); la
batería captura ahora el valor devuelto en todos los puntos y el caso queda como lo que es (una raíz
sustituida por el veneno → PE-01/DI-02); (b) `_texto` de la persistencia prohíbe NaN (allow_nan=False): el
texto corrupto de entrada se serializa con `json.dumps` normal, que es justamente el input con NaN literal
que la carga debe rechazar; (c) los casos de «estado» del diario contaminaban los casos de «línea»
siguientes (el estado corrupto daba PE-02 antes de llegar al diario): cada caso restaura los dos ficheros;
(d) las expectativas de la primera versión eran demasiado estrechas en tres sitios y la propia batería las
destapó: una mutación del estado con NaN da PE-01 (huella incanonicalizable), una cfg rehecha inválida da
PE-04, y `degradar_por_reloj` con un incidente que la mutación no desfigura SÍ degrada (por diseño); las
promesas quedaron ajustadas a lo que los módulos documentan, sin debilitar ninguna; (e) el veneno en la
fuente MONÓTONA de un reloj contrastado con un valor finito pero descolocado (0, -1, 1e308) es RL-01 (un
salto del monótono), no RL-05: la comprobación admite ambas reglas y exige el bloqueo en los dos casos;
(f) una operación del diario aplicada puede responder ok False con razón (un rechazo del Orquestador se
anota y se reproduce): la promesa de líneas exactas (cero o dos) es la que fija el registro previo.

Número de baterías que pasan: 52 ejecuciones (las 51 de V0.61 y la nueva), todas terminan en «TODAS LAS
PRUEBAS PASAN» y sin ninguna línea FALLA (lote completo en `salida_pruebas.txt`).

## 5. Límites y deuda técnica

- La batería demuestra las promesas sobre 870 casos más los fijos con una semilla fija: es reproducible,
  no exhaustiva. Las mutaciones son valores JSON (sin objetos raros, ciclos ni claves no textuales), igual
  que en V0.37 y V0.60; el anidado extremo cubre los caminos de recursión profunda de la lista de la
  pieza (los que cada módulo atraviesa: `json.loads`, `_solo_json`, `_canon`, deepcopy de montar).
- Las excepciones por diseño son clases, no casos sueltos: «lo documentado lanza» (volcar, constructor de
  Reloj, operaciones del diario con argumentos imposibles), «la cabecera puede mentir en lo que la huella
  no cubre» y «nada que migrar no mira el estado». Cada una está justificada en la cabecera de la batería
  y anclada a lo que el módulo documenta; si un módulo cambiara su contrato, la batería habría que
  ajustarla (y eso sería señal, no ruido).
- La promesa de no-mutar se mide sobre los LECTORES y sobre los caminos documentados de «no cambia nada»:
  las operaciones que cambian estado por diseño se comprueban por su efecto declarado (L1 en todas las
  carteras; cero o dos líneas del diario), no con una foto.
- La no-vacuidad de la batería se demostró con sondas ANTES de entregar (no sustituyen a la revisión) y se
  re-verificó tras corregir: desactivar la comprobación de la huella en `persistencia.py` hace fallar la
  batería en CINCO comprobaciones — las dos de PE-02, la del estado del diario (el estado tocado carga y
  el punto ya no cuadra), la de rotación sin firmar (el estado montado sin huella responde O-13, que rotar
  convierte en CL-02) y la regresión r01 —, y desactivar la cadena de hashes del diario en `diario.py`, en
  TRES — las dos declaradas de DI-02 y r01 (una línea tocada se cuela como OK) —: el «exactamente en dos»
  que la pieza declaró antes de la revisión era impreciso (hallazgo 2).
- Filas de deuda que cambian: **ninguna**. La pieza no encontró ningún defecto real que corregir y no
  añade ni resuelve ninguna fila (`Deuda_tecnica.md` queda intacto; como el propio fichero no viaja en el
  ZIP desde V0.60, su contenido actual viaja resumido en `notas_deuda.md` de esta carpeta).
