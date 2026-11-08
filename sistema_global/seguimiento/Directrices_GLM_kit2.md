# Directrices para GLM — kit 2 (V0.60 a V0.66)

Nov 8, 2026 · @Dani

## 0. Cómo usar este kit

Es el segundo kit de trabajo para GLM, pensado para unos **4 o 5 días**. Sigue el mismo método que el del fin de semana: los mismos pasos que hago yo en cada pieza, salvo lo que GLM no puede hacer (Claude Docs, git y un revisor en segundo plano).

**Kit de partida.** El fichero «Kit 2 para GLM - marco comun de C V0.53 (2026-11-08).zip» contiene (sustituye al de V0.47 del 6 de noviembre):

- la carpeta `marcoC` en **V0.53**, con todo lo construido hasta hoy: persistencia, diario, firma, migraciones y reloj (T-03), niveles L3 y cambio de nivel (T-18), reducción ajustada al paso (T-43) y las cinco piezas del fin de semana ya integradas y revisadas (robustez, tope de LIBRES, cortacircuito, pantalla de F y reducción parcial a mano);
- `Constitucion_Global.md` (V0.4, con la enmienda 1);
- `Deuda_tecnica.md`, al día;
- este documento en Markdown (`Directrices_GLM_kit2.md`).

**Una sola cadena.** Las piezas del fin de semana (V0.37 a V0.41) ya están integradas en V0.53, con las correcciones de su revisión (las explica `entrega_glm/` y el Documento 0 de V0.53). Las piezas de este kit (V0.60 a V0.66) parten **siempre** del ZIP de V0.53 de este kit y luego, cada una, del ZIP de la anterior de este kit. Siguen evitando lo que más se ha tocado: el registro manual, el registro de límites, el rearme del kill-switch, la pantalla de aprobación, `declarar_manual` y el cambio de nivel.

**Orden de las piezas y calendario orientativo.**

| Día | Pieza | Qué es | Dificultad |
| --- | --- | --- | --- |
| 1 | Pieza 1, V0.60 | Pruebas de robustez de los validadores de sobre, encargo, Contradictor, sello de K, E y H | baja |
| 1-2 | Pieza 2, V0.61 | Catálogo de códigos y prueba de coherencia | baja |
| 2 | Pieza 3, V0.62 | Pruebas de robustez de persistencia, diario, firma, migraciones y reloj | baja-media |
| 3 | Pieza 4, V0.63 | Semana simulada con reloj, diario, puntos de control y reinicios | media |
| 4 | Pieza 5, V0.64 | Panel de la consola con el estado del sistema | baja-media |
| 4-5 | Pieza 6, V0.65 | Pasada de coherencia contra la Constitución (solo documento) | media, sin código |
| 5 | Pieza 7, V0.66, opcional | Pruebas doradas: fotos fijas del comportamiento de la jornada y de la semana | media |

Una pieza a la vez. La 7 solo si las seis anteriores están en verde.

**Una conversación de GLM por pieza.** Igual que en el fin de semana:

1. Al empezar, pega el «Prompt inicial» (sección 1) y después el texto de la pieza.
2. Adjunta el ZIP de partida y, si cabe, la Constitución.
3. La revisión independiente se hace en **otra** conversación, con el prompt de la sección 9.

**Si GLM no puede ejecutar Python, ejecutas tú.** Necesitas Python 3.11 o posterior y `pip install jsonschema`. Desde la carpeta `marcoC`, la batería completa:

```
for f in pruebas/ejecutar_pruebas.py pruebas/pruebas_*.py; do echo "$(basename $f): $(python3 $f 2>&1 | tail -1)"; done | grep -v "TODAS LAS PRUEBAS PASAN"
```

Si no imprime nada, todo pasa. En V0.53 son **49 baterías**. Algunas tardan: la de migraciones, un par de minutos.

**Ficheros completos, nunca diffs.** En `orquestador.py` (unas 3.400 líneas), solo las funciones que cambian, con su nombre y su código completo. Ninguna pieza de este kit debería tocar el Orquestador; si alguna lo necesita, que GLM lo diga antes de hacerlo.

**Lo que me devuelves, por cada pieza terminada.** Como en el fin de semana:

1. El ZIP «Marco comun de C - \<tema> - V0.6x (fecha) GLM.zip» con `marcoC` completo.
2. Dentro, `marcoC/entrega_glm/V0.6x/` con `Documento_0.md`, `revision.md`, `notas_deuda.md`, `notas_briefing.md` y `salida_pruebas.txt`.

GLM no toca git ni Claude Docs.

**Si una pieza se atasca, no se fuerza.** Si en dos o tres intentos no quedan todas las pruebas en verde, GLM para y entrega lo que tenga, con el Documento 0 y la lista de lo que falla. Después se sigue con la pieza siguiente desde el último ZIP en verde. Una pieza a medias bien explicada me sirve; una que rompe pruebas antiguas sin decirlo, no.

## 1. Prompt inicial para GLM

Pégalo tal cual al empezar cada conversación de una pieza y, a continuación, el texto de esa pieza.

```
Eres el desarrollador de una pieza del "marco común de C" del proyecto Robot Investor. Es código de referencia en Python (Fase 1 de la Constitución), determinista, sin LLM, con datos simulados. Todo el código, los comentarios, los mensajes de error y los documentos van en español de España.

ESTRUCTURA (carpeta marcoC del ZIP adjunto, versión V0.53 o posterior)
- validador/: los bloques. orquestador.py (Orquestador: estado, expedientes, posiciones, avisos, kill-switch, registro de límites), control_f.py (F, control de riesgo), ejecucion_g.py (G, ejecución con el intermediario simulado BrokerSimulado), vigilancia.py (H), comparador.py (D), dimensionado.py (E), manual_g.py (CT-G-14), validar_sobre.py (CT-G-02), validar_encargo.py (CT-G-01), validar_contradictor.py (CT-G-03), k_calidad.py (K y su sello), motor.py (SC-3), mandatos.py (SC-1), contratos.py, parametros.py, consola.py (N, solo lectura).
- Infraestructura de T-03 (V0.42 a V0.47): persistencia.py (guardar y cargar el estado, firma con clave, esquema del código), diario.py (diario de operaciones con puntos de control), migraciones.py (migrar un estado guardado a otra versión del código) con esquemas_codigo.json, y reloj.py (reloj del sistema).
- pruebas/: una batería por pieza. Cada fichero acaba imprimiendo "RESULTADO ...: TODAS LAS PRUEBAS PASAN" o "HAY FALLOS". Ayudas comunes: pruebas_orquestador.py (nuevo(cfg), hasta(o, estado, n=...), autorizar_op, AHORA, Arnes con chk(nombre, condicion, detalle)); pruebas_control_f.py (informe_f, CART, solicitud); pruebas_jornada.py (pasos() de una jornada completa).
- esquemas/: esquemas JSON generados por scripts; nunca se editan los .json a mano.
- LEEME.md: módulos, baterías, lo comprobado por pieza y el "Registro de prefijos de códigos".

REGLAS INNEGOCIABLES
1. Falla cerrado: ante un dato ausente, ilegible o raro se rechaza o se toma el caso más prudente; nunca el favorable.
2. Nada lanza excepciones hacia fuera: las funciones públicas devuelven {"ok", "codigo", "motivo", ...}.
3. En el Orquestador, todo método público que cambia estado lleva @_seguro, que SOLO restaura el reloj. Por eso se valida TODO antes de mutar. (Las piezas de este kit no deberían tocar el Orquestador; si una lo necesita, dilo antes.)
4. Lo auditable va en la cadena de hashes. No se reescribe el historial.
5. Los números no se inventan sueltos: van en la configuración o en parametros.py, marcados [PROPUESTO].
6. Códigos de error y avisos: se reutilizan los existentes si encajan; si hace falta uno nuevo, el que diga la pieza.
7. No se borra ni se debilita ninguna prueba existente. Si un cambio obliga a cambiar una prueba antigua, se explica en el Documento 0 y se añade una comprobación de lo nuevo.
8. Determinismo: nada de reloj del sistema (salvo la prueba que use reloj.Reloj() real), azar sin semilla ni orden de diccionarios en lo que se compara. Usa random.Random(semilla), nunca el random global.
9. Entrega ficheros completos (o funciones completas en ficheros enormes), nunca diffs.
10. ESQUEMA DEL CÓDIGO: pruebas/pruebas_migraciones_t03.py falla en "esquema_del_codigo_registrado" si cambias algo del esquema del código (constantes en MAYÚSCULAS de los módulos de persistencia.MODULOS_ESQUEMA, CONFIG_DEFECTO o los atributos del Orquestador). Primero intenta no hacerlo (por ejemplo, una constante nueva dentro de una función o en un módulo que no esté en esa lista). Si hace falta: (a) ejecuta "python3 validador/migraciones.py --registrar-esquema V0.6x"; (b) en migraciones.py añade a MIGRACIONES una Migracion("MIG-G6x", pe.FORMATO, <esquema anterior>, <esquema nuevo>, _sin_cambios, frozenset(), "descripción"), donde el esquema anterior es el último de la cadena (en V0.53, ESQUEMA_V0_53); si la pieza añade claves a la configuración, la función las añade con valores literales; (c) explícalo en el Documento 0. Nunca borres entradas de esquemas_codigo.json.

MÉTODO (sigue estos pasos en orden y dime en qué paso estás)
Paso 1. Lee solo el kit de contexto que indica la pieza. Resume en 5-10 líneas qué vas a hacer y dónde; si algo no cuadra con el código, dilo antes de programar.
Paso 2. Escribe el Documento 0 de la pieza (plantilla de la sección 10) con las secciones 1 y 2.
Paso 3. Programa.
Paso 4. Escribe la batería nueva que pide la pieza (nombre y mínimo de comprobaciones). Cada comprobación con nombre descriptivo en español; prueba lo que debe pasar y lo que debe fallar.
Paso 5. Ejecuta la batería nueva y luego TODAS. Corrige hasta que todas pasen.
Paso 6. Repasa tu propio cambio: caminos que no fallan cerrado, mutaciones antes de validar, excepciones posibles (None, tipos raros, NaN, inf, fechas mal formadas), casos frontera. Una prueba por cada defecto real.
Paso 7. Actualiza LEEME.md: cabecera con la versión nueva, un párrafo al principio de "Fecha: ..." con lo que hace la versión, la fila de la batería nueva en la tabla de pruebas, la línea en la lista de ejecución y un punto "Comprobado en ...".
Paso 8. Completa el Documento 0 (secciones 3, 4 y 5), notas_deuda.md y notas_briefing.md, y guárdalos en marcoC/entrega_glm/V0.6x/.
Paso 9. Prepara la entrega: lista exacta de ficheros cambiados o nuevos, con su contenido completo.
La revisión independiente se hace después, en otra conversación; cuando te pegue sus hallazgos, corrige cada uno con una prueba de regresión (r01_..., r02_...) y actualiza revision.md.
```

## 2. Pieza 1 (V0.60): robustez de los validadores de sobre, encargo, Contradictor, sello de K, E y H

**Dificultad:** baja. **Parte de:** V0.53. **Tema del ZIP:** «robustez de los validadores».

**Kit de contexto:**

- de `validador/`: la cabecera (el docstring) y la función pública de `validar_sobre.py` (`validar`), `validar_encargo.py` (`validar_encargo`), `validar_contradictor.py` (`validar_informe`), `k_calidad.py` (`validar_sello`), `dimensionado.py` (`dimensionar`) y `vigilancia.py` (`vigilar`);
- de `pruebas/`: `pruebas_sobre_t27.py` (cómo carga `contexto.json`), la carpeta `pruebas/validos/`, `pruebas_encargo.py` (`CTX`) y `pruebas/encargos/validos/`, `pruebas_contradictor.py` (`sobre_base`, `informe` y cómo arma el contexto en `main`), `pruebas_k.py` (cómo llama a `validar_sello` con `{"calendario": CAL}`) y la carpeta `pruebas/k/` (los `valido_*.sello.json`), `pruebas_dimensionado.py` (`SOL`, `CART`, `AHORA`) y `pruebas_vigilancia.py` (`abierta`, `datos`).

**Objetivo.** Lo mismo que la pieza de robustez del fin de semana, pero con los seis validadores que faltan: demostrar con entradas mutadas al azar, con semilla fija, que nunca lanzan, no mutan la entrada, son deterministas y fallan cerrado. Es una batería nueva. Solo se cambia `validador/` si aparece un defecto real, con el cambio mínimo y una prueba que lo fije (`defecto_01_...`).

**Batería nueva:** `pruebas/pruebas_robustez_validadores.py`, con al menos **50 comprobaciones agregadas**: una comprobación puede cubrir N casos. Tarda menos de 90 segundos y usa `random.Random(20261110)`.

**El generador de mutaciones** es el de la pieza de robustez del fin de semana (`mutar(obj, rng)` y `caminos(obj)` en `pruebas/pruebas_robustez.py`): impórtalo o cópialo, sin cambiarlo. Una mutación sobre un camino al azar puede:

- borrar una clave o añadir una extra;
- cambiar un valor por `None`, `""`, `"x"`, `[]`, `{}`, `True`, `0`, `-1`, `1e308`, `float("nan")`, `float("inf")` o un número como texto;
- cambiar una fecha por `"2026-13-45"`, `"ayer"` o una fecha sin zona;
- anidar un valor 500 niveles (`[[[…]]]`).


**Qué se comprueba, por validador (300 casos cada uno salvo que se diga otra cosa):**

| Validador | Base válida | Promesas |
| --- | --- | --- |
| `validar_sobre.validar(sobre, ctx)` | cada `pruebas/validos/*.json` con `contexto.json` | nunca lanza; devuelve una lista de `{regla, ruta, mensaje}`; una mutación de forma da al menos V-01; no muta la entrada; dos llamadas dan lo mismo |
| `validar_encargo(msg, ctx)` | los dos `pruebas/encargos/validos/*.json` con el `CTX` de `pruebas_encargo.py` | igual; la forma da E-01 (ojo: es la E de encargo, no la de E) |
| `validar_informe(msg, ctx)` | `informe(sobre_base())` con su contexto | igual; la forma da C-01 |
| `validar_sello(sello, ctx)` | los `pruebas/k/valido_*.sello.json` con `{"calendario": CAL}` | igual; la forma da S-01, y toda mutación de valor que respete la forma da al menos S-12 (el hash del sello ya no cuadra) |
| `dimensionar(sol, cart, pol, ahora)` | `SOL`, `CART`, `POLITICA_DEFECTO` y `AHORA` de `pruebas_dimensionado.py` (500 casos, mutando una de las cuatro) | nunca lanza; `ok` False implica cantidad 0; la cantidad nunca es NaN, infinita ni negativa; la forma da E-01; determinista |
| `vigilar(o, broker, datos, ahora)` | una posición de `abierta()` y `datos(precio)` (200 casos, mutando `datos`) | nunca lanza; con datos rotos no cierra ni reduce nada (la posición sigue ABIERTA y el intermediario no recibe órdenes nuevas); `o.integridad() == []` después |

Para `vigilar`, crea el Orquestador y el intermediario de nuevo en cada caso (o cada 20 casos, si tarda): no reutilices uno que ya cambió.

**Mutaciones «de forma» y «de valor».** Sepáralas, como en la pieza del fin de semana. Si una mutación de forma da otra regla por diseño (por ejemplo, el esquema JSON deja pasar una clave extra en un sitio concreto), no es un defecto: ajústalo y explícalo. No cambies un validador para que encaje en la prueba.

**Aceptación:** pasan las 49 baterías y la nueva, y la nueva es determinista (dos ejecuciones dan la misma salida).

**LEEME:** añade la fila, la línea de ejecución y un punto «Comprobado en la robustez de los validadores». **Deuda:** ninguna fila nueva, salvo defectos que no se corrijan.

## 3. Pieza 2 (V0.61): catálogo de códigos y prueba de coherencia

**Dificultad:** baja. **Parte de:** V0.60. **Tema del ZIP:** «catálogo de códigos».

**Kit de contexto:** el apartado «Registro de prefijos de códigos» de `LEEME.md` y la cabecera (el docstring) de cada módulo de `validador/`, donde están listados sus códigos. No hace falta leer las funciones enteras.

**Problema.** El sistema tiene unos 250 códigos de resultado y de aviso, repartidos por módulos:

- O-xx (Orquestador), F-xx (F), G-xx (G), H-xx (H), D-xx (D), RM-xx (CT-G-14);
- V-xx (sobre), E-xx (encargo, pero también E de dimensionado), R-xx, C-xx, Q-xx y S-xx (K), CF-xx, CT-xx;
- PE-xx, DI-xx, MG-xx y RL-xx (T-03).

No hay una lista única con lo que significa cada uno, y nada impide que una pieza nueva reutilice un código con otro sentido, lo use sin documentarlo o deje uno documentado que ya no existe. El prefijo E es el ejemplo: lo usan el encargo (E-01 a E-17) y el dimensionado (E-01 a E-04) con significados distintos.

**Diseño exacto.**

1. **Módulo nuevo `validador/catalogo_codigos.py`** con una constante `CATALOGO`: un diccionario cuya clave es `(modulo, codigo)` y cuyo valor es `{"que": texto corto, "efecto": "RECHAZA" | "AVISO" | "BLOQUEA" | "INFORMA" | "OK", "desde": "V0.xx" o None}`.
   - `modulo` es el nombre del fichero sin `.py` (`"orquestador"`, `"dimensionado"`, …).
   - Los avisos del Orquestador llevan además `"prioridad"`, la de `PRIORIDAD_AVISO`.
   - El texto sale del docstring o del mensaje del código; no se inventa. Si no está claro, `"que": "(sin documentar)"`, y la prueba lo cuenta como pendiente.
   - Este módulo **no** está en `MODULOS_ESQUEMA`, así que no cambia el esquema. No lo añadas.
2. **Función `codigos_en_el_codigo(carpeta)`.** Recorre los `.py` de `validador/` (salvo `catalogo_codigos.py`) y saca los códigos que aparecen como texto entre comillas con la expresión `"(?:[A-Z]{1,2})-\d{2}"` (por ejemplo `"O-13"`, `"RM-07"`, `"PE-08"`). Devuelve `{(modulo, codigo)}`. Usa `ast` (los `ast.Constant` de tipo `str` que casan entero con la expresión), no un `grep` sobre el texto, para no confundir comentarios.
3. **Función `prefijos_del_leeme(ruta)`.** Lee la tabla del «Registro de prefijos de códigos» del LEEME y devuelve los prefijos que registra.

**Batería nueva:** `pruebas/pruebas_catalogo_codigos.py`, con al menos 15 comprobaciones:

- todo código que aparece en el código está en el catálogo con su módulo; la prueba lista los que faltan;
- todo código del catálogo aparece en el código (no hay códigos muertos), salvo los marcados con `"retirado": True` y su motivo (por ejemplo, E-06, retirada en CT-G-01 0.2.0);
- el mismo código en dos módulos solo está permitido si el par está en una lista `COLISIONES_ADMITIDAS` con su explicación (E del encargo y E de E, y las que encuentres); cualquier otra colisión hace fallar la prueba;
- todo prefijo usado está en el registro de prefijos del LEEME; si falta alguno (PE, DI, MG y RL seguramente faltan), se añade al LEEME en esta pieza;
- cada aviso de `PRIORIDAD_AVISO` está en el catálogo con esa prioridad;
- ningún `"que"` está vacío y los `"(sin documentar)"` son menos de 10 (si hay más, documenta los que falten leyendo el código);
- la prueba es determinista y no depende del orden de lectura de ficheros (ordénalos).

**Extra útil.** Una función `como_markdown()` que devuelve el catálogo como tabla Markdown ordenada por módulo y código. Guárdala en `entrega_glm/V0.61/catalogo_codigos.md`: la pasaré a un documento.

**Aceptación:** pasan todas las baterías. No se cambia ningún código de error existente: si dos usos chocan de verdad, se anota en el Documento 0 como hallazgo y en la deuda, sin renombrar nada.

**Deuda:** fila nueva T-60, «Catálogo de códigos al día», como RESUELTO en V0.61, y una fila por cada choque de códigos que no se resuelva.

## 4. Pieza 3 (V0.62): robustez de persistencia, diario, firma, migraciones y reloj

**Dificultad:** baja-media. **Parte de:** V0.61. **Tema del ZIP:** «robustez de la persistencia».

**Kit de contexto:**

- la cabecera (el docstring) de `validador/persistencia.py`, `diario.py`, `migraciones.py` y `reloj.py`, y sus funciones públicas: `volcar`, `cargar`, `guardar`, `cargar_de`; `crear`, `abrir`, `Diario.punto`; `migrar`, `migrar_ficheros`; `Reloj.ahora`, `contrastar`, `comprobar_estado`, `rearmar`;
- las ayudas de prueba `pruebas_persistencia_t03.rehacer`, `pruebas_diario_t03` (`lineas`, `escribir`, `recadenar`), `pruebas_jornada.pasos`, `pruebas_migraciones_t03` (`a_010`, `otro`, `ficheros_010`) y `pruebas_reloj_t03` (`Fuentes`, `nuevo_reloj`).

**Objetivo.** Es la segunda opinión sobre mi infraestructura de T-03: un ataque sistemático con semilla fija, no casos sueltos. Es una batería nueva. Solo se cambia `validador/` si aparece un defecto real, con el cambio mínimo y una prueba que lo fije (`defecto_01_...`). Un defecto aquí es grave: dilo en la primera línea del Documento 0.

**Batería nueva:** `pruebas/pruebas_robustez_t03.py`, con al menos **35 comprobaciones agregadas**. Tarda menos de 3 minutos y usa `random.Random(20261111)`. Todo en carpetas temporales (`tempfile.TemporaryDirectory`).

**Qué se comprueba.**

1. **Texto del estado roto (`cargar`).** Sobre el volcado de un Orquestador con una jornada a medias (aplica los 6 primeros pasos de `pruebas_jornada.pasos()`), 400 casos de cada tipo:
   - cambiar un carácter al azar, borrar uno o cortar el texto en una posición al azar: nunca lanza y nunca da OK;
   - mutar el documento con `rehacer` (huella rehecha, sin clave): nunca lanza y el código es uno de PE-01 a PE-08, O-13 u OK; si da OK, el estado cargado vuelve a volcarse igual que el texto cargado (no hay pérdidas silenciosas);
   - lo mismo con un volcado firmado con clave: **siempre** PE-06 o PE-01, nunca OK.
2. **Diario cortado en cualquier punto (`abrir`).** Recorre una jornada con un Diario guardando, después de cada paso, el volcado del gemelo en memoria. Después, para cada longitud k del fichero del diario (o 300 al azar si es muy largo), corta el fichero a k bytes en una copia (del estado y del diario, porque abrir reescribe el diario) y abre. Si k no llega a cubrir la primera línea entera (el PUNTO), lo esperado es DI-02. Para el resto:
   - siempre OK;
   - el estado es exactamente uno de los volcados guardados (el de antes o el de después de la operación cortada), nunca uno intermedio ni uno distinto.
3. **Diario alterado.** Un carácter cambiado en una línea que no es la última (200 casos): DI-02 o DI-04, nunca OK con otro estado. Con clave: siempre DI-02 o PE-06.
4. **Migraciones.** Sobre un documento 0.1.0 (`a_010`), 300 mutaciones con `rehacer`: `migrar` nunca lanza y nunca da OK con un estado distinto del original (salvo la entrada MIGRACION y el reloj). Registros de migraciones aleatorios (100), con elementos raros, ciclos y duplicados: nunca lanza.
5. **Reloj.** 500 secuencias aleatorias de 50 lecturas con `Fuentes`, avanzando el monótono entre 0 y 5 s y la pared con ruido pequeño, saltos grandes, congelaciones o retrocesos al azar:
   - nunca lanza;
   - los instantes dados nunca bajan;
   - tras un salto mayor que la tolerancia, ninguna lectura da OK hasta un `rearmar` y un `contrastar`;
   - dos ejecuciones con la misma semilla dan la misma secuencia.
6. **Cruces.** Un estado firmado que se migra y se abre con su diario, con una clave distinta en cada paso: PE-06 o DI-02 siempre.

Si una propiedad falla por un comportamiento que está escrito en el docstring como límite conocido (por ejemplo, recortar el diario por una línea completa, o volver a un estado antiguo firmado), no es un defecto: exclúyelo de la prueba y explícalo.

**Aceptación:** pasan todas las baterías, y la nueva es determinista.

**Deuda:** ninguna fila nueva, salvo defectos que no se corrijan (con gravedad).

## 5. Pieza 4 (V0.63): semana simulada con reloj, diario, puntos de control y reinicios

**Dificultad:** media. **Parte de:** V0.62. **Tema del ZIP:** «semana simulada».

**Kit de contexto:** `pruebas/pruebas_jornada.py` entero (es el modelo); de `validador/`, las cabeceras de `diario.py`, `persistencia.py` y `reloj.py`, y de `ejecucion_g.py` las funciones que usa la jornada (`foto_cartera`, `cotizar`, `ejecutar`, `conciliar`, `reducir`, `cerrar`, `kill_switch`, `declarar_manual`, `BrokerSimulado.avanzar_reloj`); de `vigilancia.py`, `vigilar`.

**Problema.** `pruebas_jornada.py` recorre un día con dos gemelos (uno en memoria y otro con diario que se reinicia tras cada paso), pero con el instante escrito a mano. Falta un recorrido de varios días que se parezca a la marcha real. Tiene que ser la red de seguridad de todas las integraciones que vienen:

- el instante sale del `Reloj`, con fuentes simuladas, y se contrasta con el intermediario;
- cada noche se hace un punto de control y se para el sistema;
- cada mañana se arranca: se abre el diario, `comprobar_estado` y se contrasta el reloj;
- hay cambios de día UTC, fin de semana y un corte a mitad del día.

**Diseño exacto.** Batería nueva `pruebas/pruebas_semana.py`, sin cambios en `validador/` salvo defectos reales.

1. **Reloj de la semana.** Una clase `Maquina` con un `Fuentes` (como en `pruebas_reloj_t03`) y un `BrokerSimulado` cuya `hora_datos` avanza a la vez (`avanzar_reloj`). `instante()` devuelve el de `Reloj.contrastar(broker.hora_datos, "INTERMEDIARIO")`.
2. **Calendario de la semana.** Del lunes 9 al viernes 13 de noviembre de 2026, de 08:00 a 20:00 UTC, con estos pasos:
   - lunes: encargo, sobre, comparar, proponer, autorizar y ejecutar en TACTICA (como la jornada);
   - martes: vigilancia cada hora con precios que suben poco a poco y una reducción parcial;
   - miércoles: un segundo expediente en TRADING hasta ejecutado y una operación LIBRE declarada;
   - jueves: el precio toca el stop de la primera posición (H-01), conciliación, degradación y restablecimiento;
   - viernes: kill-switch manual, conciliación y rearme con la lista del §11 (como en la jornada), y cierre de lo que quede. Usa los mismos datos simulados que `pruebas_jornada.py` y `pruebas_extremo.py`. Si un paso no se puede montar con lo que hay, sustitúyelo por otro parecido y explícalo.
3. **Gemelos.** Como en la jornada: uno en memoria y otro con `Diario`. El del diario se reinicia (se abre de nuevo desde disco) después de cada paso, y además:
   - cada noche, `punto(instante)` y se crea un `Reloj` nuevo (el arranque de la mañana pasa por `comprobar_estado` y `contrastar`);
   - el miércoles a mediodía, un corte con una línea a medias (como `CORTES` de la jornada);
   - el jueves, el estado se guarda firmado con una clave (`crear`/`abrir` con `clave=`) desde el arranque de ese día: como \`crear\` no pisa ficheros, se abre el diario sin clave, se crea uno nuevo con clave en otra carpeta a partir de ese Orquestador y se sigue con ese.
4. **Lo que se exige tras cada paso:** el mismo resultado en los dos gemelos y el esperado para ese paso (un diccionario `ESPERADO` como en la jornada); tras cada reinicio, el mismo volcado; `integridad() == []` al final de cada día; los instantes del reloj nunca bajan, y el Orquestador nunca da O-16.
5. **Al final:** la cartera del intermediario cuadra con las posiciones (conciliación limpia), el diario empieza en el PUNTO del viernes, y una migración de prueba (`migraciones.migrar` sobre el estado del viernes, convertido con `a_010` de `pruebas_migraciones_t03`) da un estado que se carga y sigue operando: una vigilancia más, sin incidencias.

**Batería nueva:** `pruebas/pruebas_semana.py`, con al menos **45 comprobaciones**. Tarda menos de 3 minutos.

**Aceptación:** pasan todas las baterías. Si al montar la semana aparece algo que el sistema no deja hacer y debería (o al revés), es un hallazgo: anótalo en el Documento 0 con el paso exacto y no lo arregles en el Orquestador sin decirlo antes.

**LEEME:** la fila y la línea de ejecución, y un punto «Comprobado en la semana» que diga que es la red al integrar. **Deuda:** ninguna fila nueva salvo hallazgos.

## 6. Pieza 5 (V0.64): panel de la consola con el estado del sistema

**Dificultad:** baja-media. **Parte de:** V0.63. **Tema del ZIP:** «panel con el estado del sistema».

**Kit de contexto:** `validador/consola.py` entero (es corto), `pruebas/pruebas_consola.py`, y de `validador/` las cabeceras de `reloj.py` y `diario.py`. Del Orquestador solo hace falta saber qué atributos leer: `kill`, `degradadas`, `nivel(cartera)`, `rearmes`, `limites["entradas"]` (para ver la última MIGRACION) y `ultimo_ahora`. En la Constitución, la §6 (consola N).

**Problema.** El panel de la consola (`consola.panel`) mira la integridad, los datos de K, el presupuesto, los avisos y las decisiones pendientes. No dice nada de lo más grave: si el kill-switch está activo, qué carteras están degradadas, si el reloj está bloqueado o si el diario está bloqueado o hace mucho que no hace un punto de control.

**Diseño exacto.** Todo en `consola.py`, que es de solo lectura. No se cambia nada de lo demás.

1. **Firma.** `panel(o, ahora, reloj=None, diario=None)`. Los dos parámetros son opcionales: sin ellos, el panel sale como hoy más los apartados 2 y 3.
2. **Comprobación «kill\_switch».** ROJO si `o.kill` no es None, con el motivo y el instante; VERDE si no.
3. **Comprobación «autonomia».** ÁMBAR si hay carteras en `o.degradadas`, con cuáles y por qué; VERDE si no. Usa los niveles con `o.nivel(cartera)`.
4. **Comprobación «reloj» (solo si se pasa `reloj`).** ROJO si `reloj.bloqueo` no es None (con el código y el motivo); ÁMBAR si aún no se ha contrastado o hace falta otro contraste; VERDE si no. Para saber si falta el contraste, **no** llames a `reloj.ahora()` (cambiaría su estado): añade a `reloj.py` un método de solo lectura `estado()` que devuelva `{"bloqueo", "contrastado": bool, "segundos_desde_contraste": float o None, "incidentes": n}` sin leer las fuentes, salvo el monótono para los segundos. Es el único cambio fuera de `consola.py` y lleva su prueba.
5. **Comprobación «diario» (solo si se pasa `diario`).** ROJO si el diario está bloqueado (lee `diario._roto`: es privado, pero la consola es parte del sistema; anótalo en el Documento 0 y propón en la deuda un método público); ÁMBAR si el diario tiene más de 1.000 líneas desde el último PUNTO (el número sale de `diario._n`); VERDE si no.
6. **Última migración.** Si la última entrada de `o.limites["entradas"]` es una MIGRACION, una línea VERDE informativa «migrado a este código el … (MIG-…)».
7. **Nada de constantes nuevas en mayúsculas en `consola.py`** (cambiarían el esquema, regla 10 del prompt). Si necesitas umbrales (1.000 líneas), ponlos como valor por defecto de un parámetro de `panel` y márcalos \[PROPUESTO\] en el docstring.
8. **Todo dentro del `try`** de `panel`: si algo falla, ROJO como hoy.

**Batería nueva:** `pruebas/pruebas_consola_sistema.py`, con al menos **20 comprobaciones**:

- kill-switch activo: ROJO con el motivo, y el panel entero ROJO;
- cartera degradada: ÁMBAR y sale la cartera;
- reloj bloqueado (RL-01 simulado con `Fuentes`): ROJO; reloj sin contrastar: ÁMBAR; reloj bien: VERDE;
- `Reloj.estado()` no cambia el reloj (dos `ahora()` seguidos dan lo mismo con y sin un `estado()` en medio);
- diario bloqueado (DI-06 provocado como en `pruebas_reloj_t03`): ROJO;
- diario con muchas líneas: ÁMBAR, y tras `punto()`: VERDE;
- con una migración hecha: aparece la línea informativa;
- sin `reloj` ni `diario`, las comprobaciones de siempre salen igual que antes (compara con `pruebas_consola.py`);
- el panel no cambia nada del Orquestador (volcado igual antes y después).

**Aceptación:** pasan todas las baterías, `pruebas_consola.py` sin cambios.

**Deuda:** una fila nueva T-61 si propones un método público para el estado del diario. D-xx no: los umbrales nuevos van a la fila D-09, que ya existe (umbrales de la consola).

## 7. Pieza 6 (V0.65): pasada de coherencia contra la Constitución (solo documento)

**Dificultad:** media, pero sin código. **Parte de:** V0.64. **Tema del ZIP:** «pasada de coherencia» (el ZIP lleva el código de V0.64 sin cambios y la carpeta `entrega_glm/V0.65/`).

**Kit de contexto:** `Constitucion_Global.md` entera (aquí sí); `LEEME.md` (sobre todo los puntos «Comprobado en …» y el párrafo «Fecha», que resume cada versión); `Deuda_tecnica.md`; el catálogo de códigos de la pieza 2; y las cabeceras (los docstrings) de los módulos de `validador/`. Las funciones solo cuando haga falta comprobar algo concreto.

**Problema.** La última pasada de coherencia del código contra la Constitución se hizo en V0.13. Desde entonces hay 50 versiones más. Hace falta saber, requisito a requisito, qué está hecho, qué está a medias, qué falta y dónde el código dice otra cosa que la Constitución. Es la base para planificar lo que queda de la Fase 1.

**Lo que se entrega:** `entrega_glm/V0.65/pasada_coherencia.md` (además de las plantillas de siempre). Contiene:

1. **Tabla de requisitos.** Una fila por requisito verificable de la Constitución que afecte a la Fase 1, recorriéndola sección por sección. Columnas:
   - **§**: sección y párrafo;
   - **requisito**: una frase, parafraseado con fidelidad;
   - **dónde**: módulo y función;
   - **prueba**: batería y nombre de la comprobación que lo demuestra;
   - **estado**: CUMPLE, PARCIAL, FALTA, CONTRADICE o FUERA DE FASE 1;
   - **nota**.
2. **Hallazgos.** Numerados PC2-01, PC2-02…, uno por cada PARCIAL, FALTA o CONTRADICE que importe, con:
   - la gravedad (alta, media o baja);
   - qué dice la Constitución y qué hace el código, con la cita exacta del código (fichero y función) y, si se puede, un script mínimo que lo demuestre (imprimiendo «FALLA» o «OK», como en la revisión);
   - una propuesta: deuda nueva (T-6x), decisión del operador (D-xx nueva) o enmienda de la Constitución.
3. **Resumen.** Cuántos requisitos hay en cada estado, y los diez hallazgos más importantes en orden.

**Reglas de esta pieza.**

- No se cambia código. Si algo parece un defecto de código, es un hallazgo con su script, y lo arreglaré yo o irá a una pieza posterior.
- Lo que dependa del operador se marca como decisión (D-xx), no como defecto.
- Lo que la Constitución deja para la Fase 2 o 3 se marca FUERA DE FASE 1 y no cuenta como hallazgo.
- No se repiten hallazgos que ya estén en la deuda: se cita la fila (por ejemplo, «ya es T-01»).
- Con citas, nada de memoria: cada «dónde» y cada «prueba» se comprueba abriendo el fichero.

**Aceptación:** pasan todas las baterías (no ha cambiado nada) y cada script de hallazgo da «FALLA» al ejecutarlo. La tabla cubre todas las secciones de la Constitución; donde una sección no tenga requisitos verificables, una fila que lo diga.

**Deuda:** en `notas_deuda.md`, las filas nuevas que propongas (T-6x y D-xx), sin numerar por encima de lo que ya exista. La revisión independiente de esta pieza consiste en que otro GLM compruebe 20 filas al azar de la tabla y todos los scripts.

## 8. Pieza 7, opcional (V0.66): pruebas doradas de la jornada y de la semana

**Dificultad:** media. **Parte de:** V0.65. **Tema del ZIP:** «pruebas doradas». Solo si las seis anteriores están en verde.

**Kit de contexto:** `pruebas/pruebas_jornada.py` y `pruebas/pruebas_semana.py` (la de la pieza 4), y la cabecera de `consola.py` (para el resumen del estado).

**Problema.** Las baterías comprueban lo que se les dice que compruebe. Cuando integre piezas nuevas (las del fin de semana, las de este kit), un cambio de comportamiento que ninguna prueba mira pasará sin que nadie lo vea. Por ejemplo, un aviso más, otra cantidad, una cartera que ya no se degrada o un código distinto en un paso. Una prueba dorada guarda una foto fija de lo que hace cada paso y avisa de cualquier diferencia, que luego una persona acepta o rechaza.

**Diseño exacto.** Solo pruebas y datos de prueba; nada en `validador/`.

1. **`pruebas/doradas.py`**, con una función `resumen(resultado, o)` que, para un paso, guarda:
   - del resultado: `ok`, `codigo` y, si las hay, las listas de acciones con `(regla, codigo, condicion)`, las cantidades redondeadas a 6 decimales y los identificadores. **Sin** los textos de `motivo`, que cambian demasiado;
   - del estado: el estado de cada expediente y de cada posición con su cantidad, los códigos de los avisos sin acusar (ordenados), el nivel de cada cartera, si hay kill-switch y el número de rearmes.
2. **Fotos en `pruebas/doradas/jornada.json` y `pruebas/doradas/semana.json`:** la lista de resúmenes, paso a paso, de un gemelo de cada recorrido. JSON con las claves ordenadas e indentado, para que las diferencias se lean bien.
3. **`pruebas/pruebas_doradas.py`:**
   - rehace los resúmenes y los compara con las fotos;
   - si hay diferencias, imprime por cada paso distinto el nombre del paso y las claves que cambian (antes y después), y falla;
   - con `--regenerar` reescribe las fotos. Eso solo se hace a propósito, y cada regeneración se explica en el Documento 0 de la pieza que la hizo, con la lista de diferencias aceptadas.
4. **Determinismo.** Las fotos no dependen del orden de los diccionarios, de la carpeta ni de la máquina; dos ejecuciones dan el mismo fichero byte a byte.

**Batería nueva:** `pruebas/pruebas_doradas.py`, con al menos **12 comprobaciones**:

- coinciden las dos fotos;
- un cambio provocado (por ejemplo, otro precio en un paso, en una copia del recorrido) se detecta y se informa bien;
- `--regenerar` en una carpeta temporal da el mismo fichero dos veces;
- los resúmenes no llevan textos de motivo;
- el resumen no cambia el Orquestador.

**Aceptación:** pasan todas las baterías, la nueva incluida. En `notas_briefing.md`, cómo regenerar y cuándo está permitido.

**Deuda:** ninguna fila nueva.

## 9. Prompt de revisión independiente

Es el paso que más defectos caza, así que no se salta.

- Abre una conversación **nueva** de GLM, sin el historial de la pieza.
- Adjunta el ZIP de la pieza ya en verde.
- Pega este texto, cambiando lo que va entre ángulos por la sección de la pieza: su «Problema» (u «Objetivo») y su «Diseño exacto» (o «Qué se comprueba»). No pegues el Documento 0 ni las conclusiones de la otra conversación: el revisor debe leer el código sin que nadie le diga que está bien.

```
Eres revisor independiente de código Python del proyecto Robot Investor (en español). No has escrito este código. Tu trabajo es encontrar defectos reales, no aprobarlo.

Qué pretende el cambio que revisas:
<pega aquí el "Problema" u "Objetivo" y el "Diseño exacto" o "Qué se comprueba" de la pieza>

Ficheros que debes leer: <los del kit de contexto de la pieza> y la batería nueva <nombre>.

Principios del proyecto: determinista; falla cerrado (ante dato ausente, ilegible o raro, rechazar o tomar el caso prudente, nunca el favorable); en el Orquestador se valida todo antes de mutar estado porque el decorador @_seguro solo restaura el reloj; nada lanza excepciones hacia fuera; lo auditable va en la cadena de hashes; no se debilitan pruebas existentes; un cambio en las constantes de los módulos de persistencia.MODULOS_ESQUEMA exige registrar el esquema y una migración.

Busca, sin limitarte a ello: caminos que no fallan cerrado; mutaciones de estado antes de validar; excepciones posibles (None, tipos raros, NaN, inf, fechas mal formadas o sin zona, días frontera UTC); comparaciones con < donde debería ser <= o al revés; dobles conteos u omisiones; datos que se pueden manipular desde fuera; diferencias entre lo que dice el diseño y lo que hace el código; pruebas que no prueban lo que dicen (que pasarían también sin el cambio, o que comprueban algo trivial); pruebas no deterministas (semillas, orden de diccionarios, reloj real, carpetas).

Para cada hallazgo escribe un script mínimo que se ejecute desde la carpeta marcoC (sys.path con validador/ y pruebas/) y que imprima "FALLA" si el defecto existe y "OK" si está corregido. No informes sospechas que no puedas reproducir. No modifiques el código del proyecto.

Devuelve una lista numerada: gravedad (alta/media/baja), fichero y función, el defecto en una o dos frases, el escenario concreto y el script completo.
```

**En las piezas que son sobre todo pruebas** (1, 3, 4 y 7), pídele además al revisor que busque una propiedad que la batería debería comprobar y no comprueba, y que la demuestre con un script. Un hueco en la batería cuenta como hallazgo.

**En la pieza 6** (pasada de coherencia), la revisión es otra. El revisor recibe la Constitución, el código y `pasada_coherencia.md`, y:

- comprueba 20 filas de la tabla elegidas al azar (las elige con `random.Random(20261113)` sobre los números de fila);
- ejecuta todos los scripts de los hallazgos;
- busca tres requisitos de la Constitución que la tabla no recoja.

**Después,** igual que en el fin de semana:

1. Ejecuta cada script contra el ZIP (si GLM no puede, lo haces tú) y descarta los que den OK de entrada.
2. Pega en la conversación de la pieza los hallazgos que dan FALLA, con sus scripts.
3. GLM corrige cada uno con su prueba de regresión (`r01_...`, `r02_...`) y vuelve a pasar todas las baterías.
4. Vuelves a ejecutar los scripts: todos deben dar OK, y si alguno ya no llega a su comprobación porque cambió el comportamiento, que lo explique.
5. Todo queda en `revision.md`.

## 10. Plantillas de entrega

Son las mismas que en el fin de semana. GLM las rellena y las deja en `marcoC/entrega_glm/V0.6x/`, en Markdown sencillo; yo las paso luego a Claude Docs.

**`Documento_0.md`:**

```
# Documento 0 — <tema> (V0.6x) — GLM, pendiente de revisión

## 1. Problema y alcance
Qué faltaba y por qué importa (con la deuda o la sección de la Constitución). Qué entra en esta versión y qué queda fuera.

## 2. Diseño
Cómo funciona, en prosa y con listas cortas: datos nuevos, dónde se calculan, cuándo se comprueban, qué pasa en cada caso límite. Valores nuevos con [PROPUESTO]. Si cambió el esquema del código: el esquema nuevo y la migración añadida.

## 3. Reglas y comprobaciones
Tabla: código (regla o aviso), qué comprueba, efecto. Cambios en reglas existentes.

## 4. Códigos, API, pruebas y revisión independiente
Funciones nuevas o cambiadas con su firma. Batería nueva y número de comprobaciones; pruebas antiguas que cambiaron y por qué. Defectos encontrados por la propia batería (defecto_01...). Hallazgos del revisor numerados con su gravedad y cómo se corrigió cada uno. Número de baterías que pasan.

## 5. Límites y deuda técnica
Lo que no resuelve, lo aproximado, lo que depende del operador. Filas de deuda que cambian.
```

**`notas_deuda.md`:** las filas que cambian en «Deuda técnica y pendientes del operador», en dos listas:

- tabla T: id, texto nuevo de la cuarta columna (por ejemplo, «RESUELTO en V0.61: …»), o filas nuevas a partir de T-60;
- tabla D: filas nuevas con id, qué debe decidir el operador, dónde se usa y valor de partida \[PROPUESTO\]. Usa D-60 en adelante para no chocar con las del fin de semana.

**`notas_briefing.md`:** un párrafo técnico denso que empiece por «V0.6x: …», con los nombres exactos que otra persona necesitaría para seguir sin leer el código: funciones, atributos, claves, códigos, valores por defecto, semillas y ayudas de prueba.

**`revision.md`:** cada hallazgo con gravedad, script, resultado antes y después, arreglo y prueba de regresión.

**`salida_pruebas.txt`:** la salida del bucle de la sección 0 (vacía si todo pasa), el número de comprobaciones de la batería nueva y cuánto tardó.

**Extras de algunas piezas:** `catalogo_codigos.md` (pieza 2) y `pasada_coherencia.md` (pieza 6).

**Nombre del ZIP:** «Marco comun de C - \<tema> - V0.6x (AAAA-MM-DD) GLM.zip», con la carpeta `marcoC` completa, sin `__pycache__`, y la carpeta `entrega_glm` dentro de `marcoC` (con las entregas de todas las piezas anteriores de este kit, que se van acumulando). Nunca se sobrescribe un ZIP anterior.

**Lo que me pasas cuando vuelva:** el último ZIP de este kit (lleva todas sus entregas dentro) y el último del fin de semana, si no me lo has pasado ya.
