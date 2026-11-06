# Directrices para GLM — piezas del marco común de C (fin de semana)

Nov 6, 2026 · @Dani

## 0. Cómo usar estas directrices

Este documento es para quien lleve el trabajo con GLM durante el fin de semana. Sigue exactamente los pasos que hago yo en cada pieza. Solo cambia lo que GLM no puede hacer: no tiene Claude Docs, ni git, ni un revisor en segundo plano.

**Kit de partida.** El fichero «Kit para GLM - marco comun de C V0.36 (2026-11-06).zip» contiene:

- la carpeta `marcoC` en V0.36;
- `Constitucion_Global.md`;
- `Deuda_tecnica.md`;
- este documento en Markdown.

No hace falta nada más.

**Orden de las piezas.** Son de dificultad baja o media y no dependen de decisiones del operador:

1. **Pieza 1, V0.37:** pruebas de robustez. No cambia lógica; si encuentra fallos, los corrige con el cambio mínimo.
2. **Pieza 2, V0.38:** T-33, tope a las operaciones LIBRES.
3. **Pieza 3, V0.39:** cortacircuito global por pérdida.
4. **Pieza 4, V0.40:** pantalla de aprobación con las cifras de la §8.
5. **Pieza 5, V0.41, opcional y la más difícil:** T-44. Solo si las cuatro anteriores están terminadas y en verde.

Cada pieza parte del ZIP de la anterior. Nunca hay dos piezas abiertas a la vez.

**Una conversación de GLM por pieza.** Así el contexto no se llena:

1. Al empezar, pega el «Prompt inicial» (sección 1) y después el texto de la pieza.
2. Adjunta el ZIP de partida y, si cabe, la Constitución.
3. Para la revisión independiente abre **otra** conversación con el prompt de la sección 7. GLM no debe revisar su propio trabajo en la misma conversación.

**Si GLM no puede ejecutar Python**, eres tú quien ejecuta.

- Necesitas Python 3.11 o posterior y `pip install jsonschema`.
- Desde la carpeta `marcoC`, ejecuta las pruebas que diga GLM y pégale solo el final de la salida (las líneas FALLA y la última línea).
- La batería completa:

```
for f in pruebas/ejecutar_pruebas.py pruebas/pruebas_*.py; do echo "$(basename $f): $(python3 $f 2>&1 | tail -1)"; done | grep -v "TODAS LAS PRUEBAS PASAN"
```

Si no imprime nada, todo pasa. En Windows, ejecuta cada fichero con `python pruebas\\nombre.py`.

**Que GLM entregue ficheros completos, nunca fragmentos ni diffs.** Tú los copias encima de los de `marcoC`. Si un fichero es muy largo, como `orquestador.py` (unas 2.900 líneas), que entregue solo las funciones que cambian, con el nombre de cada una y su código completo, y las sustituyes a mano.

**Lo que me devuelves el lunes, por cada pieza terminada:**

1. El ZIP «Marco comun de C - \<tema> - V0.3x (fecha) GLM.zip» con `marcoC` completo.
2. Dentro del ZIP, la carpeta `marcoC/entrega_glm/V0.3x/` con:
   - `Documento_0.md`;
   - `revision.md`, con los hallazgos del revisor y cómo se corrigió cada uno;
   - `notas_deuda.md`;
   - `notas_briefing.md`;
   - `salida_pruebas.txt`, la salida de la batería completa.

Yo haré mi propia revisión independiente, corregiré lo que haga falta y pasaré todo a Claude Docs, al repositorio y a los commits firmados. GLM no toca git ni los documentos de Claude Docs.

**Si una pieza se atasca**, no se fuerza:

- Si GLM no consigue dejar todas las pruebas en verde en dos o tres intentos, para.
- Entrega lo que tenga, con el Documento 0 y una lista de lo que falla.
- Sigue con la pieza siguiente partiendo del último ZIP en verde, no del roto.

Una pieza a medias bien explicada me sirve; una que rompe pruebas antiguas sin decirlo, no.

## 1. Prompt inicial para GLM

Pégalo tal cual al empezar cada conversación de una pieza y, a continuación, el texto de esa pieza.

```
Eres el desarrollador de una pieza del "marco común de C" del proyecto Robot Investor. Es código de referencia en Python (Fase 1 de la Constitución), determinista, sin LLM, con datos simulados. Todo el código, los comentarios, los mensajes de error y los documentos van en español de España.

ESTRUCTURA (carpeta marcoC del ZIP adjunto)
- validador/: los bloques. control_f.py (F, control de riesgo), orquestador.py (Orquestador: estado, expedientes, posiciones, avisos, kill-switch), ejecucion_g.py (G, ejecución con intermediario simulado BrokerSimulado), manual_g.py (CT-G-14, registro manual del operador), comparador.py (D), dimensionado.py (E), vigilancia.py (H), contratos.py, parametros.py, mandatos.py (SC-1), k_calidad.py (K).
- pruebas/: una batería por pieza. Cada fichero acaba imprimiendo "RESULTADO ...: TODAS LAS PRUEBAS PASAN" o "HAY FALLOS". Ayudas comunes: pruebas_orquestador.py (nuevo(cfg), hasta(o, estado, n=..., entrada=...), autorizar_op, Arnes con chk(nombre, condicion, detalle) y rechaza(nombre, o, funcion, codigo)); pruebas_control_f.py (informe_f(o, ...), CART, solicitud(...)).
- esquemas/: esquemas JSON generados por scripts (generar_esquemas_contratos.py); nunca se editan los .json a mano.
- LEEME.md: lista de módulos, de pruebas y lo comprobado por pieza.

REGLAS INNEGOCIABLES
1. Falla cerrado: ante un dato ausente, ilegible o raro se rechaza o se toma el caso más prudente; nunca el favorable.
2. Nada lanza excepciones hacia fuera: las funciones públicas devuelven {"ok", "codigo", "motivo", ...} (helpers _r y _no del Orquestador).
3. En el Orquestador, todo método público que cambia estado lleva el decorador @_seguro, que SOLO restaura el reloj (ultimo_ahora). Por eso se valida TODO antes de mutar nada.
4. Lo que importa para auditoría va en la cadena de hashes (_anota para expedientes, _anota_pos para posiciones). No se reescribe el historial.
5. Los números no se inventan sueltos en el código: van en la configuración (CONFIG_DEFECTO del Orquestador, con su validación en _valida_config) o en parametros.py, marcados [PROPUESTO], y suben la versión (version_config CFG-x.y.z).
6. Códigos de error y avisos: se reutilizan los existentes si encajan; si hace falta uno nuevo, se usa el siguiente libre que diga la pieza y se añade a PRIORIDAD_AVISO si es un aviso.
7. No se borra ni se debilita ninguna prueba existente. Si un cambio de comportamiento obliga a cambiar una prueba antigua, se explica en el Documento 0 por qué el comportamiento nuevo es el correcto y se añade una comprobación que demuestre lo nuevo.
8. Determinismo: nada de reloj del sistema, azar sin semilla ni orden de diccionarios en lo que se compara.
9. Entrega ficheros completos (o funciones completas en ficheros enormes), nunca diffs.

MÉTODO (sigue estos pasos en orden y dime en qué paso estás)
Paso 1. Lee solo el kit de contexto que indica la pieza (no todo el código). Resume en 5-10 líneas qué vas a cambiar y dónde; si algo de la pieza no cuadra con el código, dilo antes de programar.
Paso 2. Escribe el Documento 0 de la pieza (plantilla al final) con las secciones 1 y 2 rellenas.
Paso 3. Programa el cambio.
Paso 4. Escribe la batería nueva de pruebas que pide la pieza (nombre y número mínimo de comprobaciones indicados). Cada comprobación con nombre descriptivo en español; comprueba el caso que debe pasar y el que debe fallar.
Paso 5. Ejecuta (o pide que se ejecute) la batería nueva y luego TODAS las baterías. Corrige hasta que todas pasen.
Paso 6. Repasa tu propio cambio buscando: caminos que no fallan cerrado, mutaciones antes de validar, excepciones posibles (None, tipos raros, NaN, inf, fechas mal formadas), y casos frontera (iguales, cero, días frontera UTC). Añade una prueba por cada defecto real que encuentres.
Paso 7. Actualiza LEEME.md: cabecera con la versión nueva, un párrafo al principio de "Fecha: ..." con lo que hace la versión, la fila de la batería nueva en la tabla de pruebas, la línea en la lista de ejecución y un punto "Comprobado en ..." con lo comprobado y sus límites.
Paso 8. Completa el Documento 0 (secciones 3, 4 y 5), notas_deuda.md y notas_briefing.md, y guárdalos en marcoC/entrega_glm/V0.xx/.
Paso 9. Prepara la entrega: lista exacta de ficheros cambiados o nuevos, con su contenido completo.
La revisión independiente se hace después, en otra conversación; cuando te pegue sus hallazgos, corrige cada uno con una prueba de regresión (nombre r01_..., r02_...) y actualiza revision.md.
```

## 2. Pieza 1 (V0.37): pruebas de robustez de F, D y CT-G-14

**Dificultad:** baja. **Parte de:** V0.36. **Tema del ZIP:** «pruebas de robustez».

**Kit de contexto:** `validador/control_f.py`, `validador/comparador.py`, `validador/manual_g.py`, `pruebas/pruebas_control_f.py`, `pruebas/pruebas_control_f_t22.py` (solo el diccionario `CTX` y la función `f`), `pruebas/pruebas_comparador.py` (solo `cand`) y `pruebas/pruebas_manual.py` (solo `ct14`, `reg`, `libre` y las primeras líneas de `main`).

**Objetivo.** Demostrar con entradas generadas al azar, con semilla fija, que tres validadores cumplen sus promesas: nunca lanzan, no mutan la entrada, son deterministas y fallan cerrado. Es una batería nueva. Solo se cambia código de `validador/` si aparece un defecto real, y entonces con el cambio mínimo y una prueba que lo fije.

**Batería nueva:** `pruebas/pruebas_robustez.py`, con al menos 40 comprobaciones agregadas. Una comprobación puede cubrir N casos: «no lanza en 500 mutaciones» cuenta como una. Debe tardar menos de 60 segundos. Usa `random.Random(20261107)`, nunca el `random` global.

El generador de mutaciones toma un objeto válido y aplica una mutación al azar en un camino al azar:

- borrar una clave o añadir una clave extra;
- cambiar un valor por `None`, `""`, `"x"`, `[]`, `{}`, `True`, `0`, `-1`, `1e308`, `float("nan")`, `float("inf")`, `-float("inf")` o un número como texto (`"1.1"`);
- cambiar una fecha por `"2026-13-45"`, `"ayer"` o una fecha sin zona horaria.

Escribe una función `mutar(obj, rng)` que devuelva una copia profunda mutada y otra `caminos(obj)` que liste los caminos.

**F (`controlar`, `construir_informe`, `validar_informe_f`):**

- Con la solicitud base de `pruebas_control_f.solicitud()`, la cartera `CART`, la política `POLITICA_DEFECTO`, el contexto `CTX` de la batería T-22 y `AHORA_F`, mutando una de las cinco entradas cada vez (500 casos):
  - nunca lanza;
  - no muta la entrada (compárala con una copia profunda tomada antes);
  - el resultado es uno de APROBADO, REDUCIDO o VETADO;
  - VETADO implica cantidad 0;
  - la cantidad aprobada nunca supera la solicitada;
  - repetir la llamada da exactamente lo mismo.
- Toda mutación de la forma de la solicitud, de la cartera, de la política o del contexto (clave de más o de menos, tipo cambiado) acaba en VETADO con F-01. Separa estas mutaciones «de forma» de las «de valor», como cambiar un número por otro número válido.
- `validar_informe_f` sobre un informe válido de `informe_f(o)` mutado (300 casos) nunca lanza y devuelve una lista. Toda mutación de la envoltura da al menos un fallo.

**D (`comparar_candidatos`):**

- Con dos candidatos de `pruebas_comparador.cand(1)` y `cand(2, esperado=(3.0, 0.5, -4.0))`, mutando uno (500 casos):
  - nunca lanza;
  - `ok` es True o el código es D-01;
  - si ok es True, el candidato mutado (identifícalo por su posición en la lista, porque la mutación puede cambiar su id) o está en el ranking, o está en `excluidos` con un motivo de la lista de motivos de la cabecera del módulo;
  - ningún valor numérico del ranking es NaN o infinito;
  - el orden de entrada de los candidatos no cambia el resultado.

**CT-G-14 (`validar_manual`):**

- Sobre un registro LIBRE válido, sacado de `pruebas_manual.py` y con el contexto que esas pruebas usan, mutado (300 casos): nunca lanza, siempre devuelve una lista y toda mutación de forma da RM-01.

**Si aparece un defecto:**

1. Reduce el caso al mínimo.
2. Añádelo como comprobación fija con nombre (`defecto_01_...`).
3. Corrígelo en `validador/` con el cambio más pequeño.
4. Explícalo en el Documento 0.

Si no aparece ninguno, dílo también: es un resultado válido. Ojo con los falsos defectos: si una mutación de forma da otra regla por diseño (por ejemplo, RM-03 en vez de RM-01 porque una fecha bien formada queda fuera de la ventana), eso no es un defecto. Ajusta la prueba y explícalo; no cambies el validador para que encaje.

**Aceptación:**

- pasan las 34 baterías y la nueva;
- la nueva es determinista: dos ejecuciones dan la misma salida.

**LEEME:** añade la fila y la línea de `pruebas_robustez.py` y un punto «Comprobado en la robustez». **Deuda:** ninguna fila nueva, salvo defectos que no se corrijan.

## 3. Pieza 2 (V0.38): T-33, tope a las operaciones LIBRES

**Dificultad:** baja-media. **Parte de:** V0.37. **Tema del ZIP:** «tope a las operaciones libres».

**Kit de contexto:** de `validador/orquestador.py`, solo `CONFIG_DEFECTO`, `PRIORIDAD_AVISO`, `_valida_config`, `__init__` (atributos), `_aviso`, `_degradar`, `registrar_manual`, `_actividad` y `contexto_f`. Además, `validador/control_f.py` (`tipo_cambio`) y `pruebas/pruebas_manual.py` (cómo se construye y registra un CT-G-14 LIBRE). En la Constitución, la §6 y la §8 (busca «LIBRE» y «Controles posteriores»).

**Problema (deuda T-33).** Una operación que el operador hace fuera del sistema y declara como LIBRE (CT-G-14) solo deja el aviso O-20: no tiene tope y su importe no cuenta en el límite del día de F (F-14).

**Diseño exacto:**

1. **Configuración nueva.** `"libres_tope_dia_eur": {"TRADING": 2000.0, "TACTICA": 2000.0, "LARGO_PLAZO": 2000.0}` \[PROPUESTO, D-32\].
   - En `_valida_config`: un diccionario con exactamente esas tres carteras, cada valor numérico finito y mayor o igual que 0; si no, `ValueError` como el resto.
   - `version_config` pasa a `"CFG-0.8.0"`, añadiendo al comentario «0.8.0 (T-33): libres\_tope\_dia\_eur».
2. **Registro aparte.** Atributo nuevo `self.libres = []` en `__init__`. No se mete nada nuevo en `self.manuales`, que lo usan la conciliación y otros.
3. **Importe en euros de un LIBRE.** `cantidad × precio × fx`, con `fx = tipo_cambio(self.divisa(instrumento), self.ultima_foto)`: 1 si la divisa es EUR. Si no hay foto, no hay divisa o no hay tipo, el importe es `None`.
4. **En `registrar_manual`, rama LIBRE, después del aviso O-20**, añade a `self.libres` un diccionario con `{"cartera", "dia" (fecha UTC de ejecutado_en en ISO), "importe_eur" (o None), "registrado_en": ahora, "event_id"}`. Después suma los importes de esa cartera y ese día.
   - Si algún importe es `None` o la suma supera el tope de la cartera, emite el aviso **O-37** (prioridad ALTA, añádelo a `PRIORIDAD_AVISO`). El motivo es «operaciones libres de \<cartera> el \<día>: \<suma> EUR por encima del tope \<tope> EUR», o «…sin poder valorarlas en euros». Pasa `carteras={cartera}` y degrada la cartera con `self._degradar(cartera, motivo)`.
   - El registro **se acepta igual**: la operación ya ocurrió, y rechazarla la convertiría en una discrepancia sin explicar. Devuelve el `_r(True, "OK", ...)` de siempre con un campo extra `tope_libres_superado: True/False`.
   - Todas las validaciones siguen antes de cualquier cambio de estado: lo nuevo va al final, cuando el registro ya está aceptado.
5. **F-14 ve los LIBRES.** En `_actividad(excluido, a)`, suma a `importe_dia_eur` los importes de `self.libres` del día UTC de `a` con `registrado_en <= a`, de todas las carteras porque los límites de F son de la cuenta. Un LIBRE sin importe suma el importe máximo del día de la política (`self.cfg["politica_f"]["importe_max_dia_eur"]`): sin valor no se puede seguir operando ese día. Filtrar por `registrado_en` es lo que mantiene reproducible el contexto de un informe de F emitido antes (CF-09).

**Batería nueva:** `pruebas/pruebas_libres_t33.py`, con al menos 25 comprobaciones. Como mínimo:

- bajo el tope, sin O-37 y la cartera sin degradar;
- al superarlo, O-37 ALTA con su cartera y la cartera degradada (usa `nivel_autonomia {"TACTICA": "L2"}` para ver que baja a L1); las otras carteras, sin tocar;
- el registro sigue aceptado y está en `self.manuales`;
- dos LIBRES que juntos superan el tope;
- al día siguiente (UTC) se empieza de cero;
- sin foto, o con una divisa sin tipo, se trata como tope superado;
- un LIBRE en USD valorado con el tipo de la foto;
- configuración inválida: falta una cartera, hay una de más, un valor negativo, NaN o texto (`ValueError`);
- la versión es CFG-0.8.0;
- `contexto_f(...)["actividad"]["importe_dia_eur"]` incluye el LIBRE de hoy y no el de ayer;
- un informe de F emitido antes de registrar un LIBRE sigue validando (CF-09) y uno emitido después lo cuenta;
- con el LIBRE, F reduce por F-14 cuando el día ya va cargado (usa una política con `importe_max_dia_eur` pequeño).

**Aceptación:** pasan todas las baterías. Ninguna prueba de `pruebas_manual.py` cambia de resultado; si alguna se ve afectada, que sea solo por el aviso nuevo o la degradación, y explicado.

**Deuda:** T-33 queda RESUELTO. D-32 es nueva: «Fijar el tope diario por cartera de las operaciones LIBRES», con valor de partida 2.000 € por cartera \[PROPUESTO\].

## 4. Pieza 3 (V0.39): cortacircuito global por pérdida (parte de T-40)

**Dificultad:** baja-media. **Parte de:** V0.38. **Tema del ZIP:** «cortacircuito por pérdida».

**Kit de contexto:** de `validador/orquestador.py`, solo `registrar_cartera`, `_anota_alcance`, `_activar_kill`, `activar_kill_switch`, `rearmar_kill_switch`, `_actividad` (la parte de `perdidas_dia`), `PRIORIDAD_AVISO` y `TIPOS_KILL`. Además, `validador/control_f.py` (`POLITICA_DEFECTO`: `perdida_dia_max_eur` y `perdida_semana_max_eur`), `pruebas/pruebas_aprobacion.py` (cómo se rearma el kill-switch) y `pruebas/pruebas_control_f_t22.py` (la prueba r03, que registra fotos en varios días). En la Constitución: §8 «Controles posteriores» y «Kill-switch», y §11 (desencadenantes: «cortacircuito global»).

**Problema.** Desde V0.36, F veta las entradas nuevas cuando la pérdida del día o de la semana en euros llega a su límite (F-16). Pero eso solo frena lo nuevo. La §8 pide que, además, el cortacircuito se dispare solo, y la §11 cuenta el cortacircuito global entre los desencadenantes del kill-switch.

La parte de T-40 que queda fuera es el vigilante con latido como proceso independiente (Fase 3).

**Diseño exacto:**

1. **Dónde.** En `registrar_cartera`, después de registrar la foto y de `_anota_alcance` (es decir, cuando la foto ya es válida y está guardada).
2. **Qué calcula.**
   - `dia_eur` = `foto["perdida_dia_eur"]`.
   - `semana_eur` = la suma de `self.perdidas_dia` de los siete días que acaban en la fecha UTC de la foto, con el mismo criterio que `_actividad`.
   - Los límites son los de `self.cfg["politica_f"]`.
3. **Cuándo salta.** Si `dia_eur >= perdida_dia_max_eur` o `semana_eur >= perdida_semana_max_eur`, el cortacircuito salta. Es el mismo umbral en el que F-16 empieza a vetar.
4. **Qué hace al saltar.**
   - Si `self.kill` es None, llama a `self._activar_kill("cortacircuito global: pérdida del día <x> EUR (límite <y>)" o «…de la semana…», "ORQUESTADOR", ahora)`. Eso ya bloquea entradas, pasa todo a L1 y avisa con O-26.
   - Además emite el aviso **O-38** (prioridad ALTA, en `PRIORIDAD_AVISO`) con las dos cifras y sus límites.
   - Solo una vez por día UTC de la foto: guarda los días en un atributo nuevo `self.cortacircuitos = []`, con `{"dia", "perdida_dia_eur", "perdida_semana_eur", "ahora"}`.
   - Si el kill-switch ya estaba activo por otra causa, solo anota y avisa.
5. **Lo que no cambia.** `registrar_cartera` sigue devolviendo OK (la foto es buena) con un campo extra `cortacircuito: True/False`. No se cancelan protecciones ni se liquida nada: lo hace el kill-switch de siempre, y G cancela las entradas vivas en su siguiente paso, como con los demás kill automáticos. Comprueba en `ejecucion_g.py` cómo lo hace hoy y no lo cambies.
6. **Rearme.** `rearmar_kill_switch` sigue igual, pero si el kill-switch vino de un cortacircuito y la última foto registrada sigue en o por encima de alguno de los dos límites, el rearme se rechaza con **O-35** («la pérdida sigue en el límite: no se rearma hasta que baje o cambie el día»). Para el día cuenta la fecha UTC de la última foto.

**Batería nueva:** `pruebas/pruebas_cortacircuito_t40.py`, con al menos 22 comprobaciones. Como mínimo:

- con una pérdida del día por debajo del límite, no salta;
- justo en el límite (igual), salta: kill-switch activo con motivo «cortacircuito…», aviso O-26 y O-38, y autorizar una propuesta da O-26;
- la pérdida de la semana repartida en varios días (ninguno por sí solo en el límite) salta;
- una segunda foto el mismo día no repite O-38;
- al día siguiente con otra foto en el límite sí vuelve a avisar;
- una foto mal formada o rechazada (O-01, O-10, O-29) no dispara nada;
- el rearme con la pérdida aún en el límite da O-35, y con una foto nueva por debajo (o al día siguiente) se rearma con la lista del §11 (copia el flujo de `pruebas_aprobacion.py`);
- un kill-switch manual previo no se pisa: el motivo sigue siendo el manual y O-38 sí sale;
- `registrar_cartera` devuelve `cortacircuito` True o False según el caso.

**Aceptación:** pasan todas las baterías. Ojo con las pruebas antiguas que registran fotos con `perdida_dia_eur` alta para provocar vetos de F (busca `perdida_dia_eur": 5000` en `pruebas/`): ahora también dispararán el kill-switch. Si una prueba antigua falla por eso, no la debilites: o le das una política con límites en euros más altos para que pruebe lo que probaba, o compruebas también el kill-switch. Explícalo en el Documento 0.

**Deuda:** T-40 queda en parte resuelta: el cortacircuito global está hecho y falta el vigilante con latido (Fase 3). No hay decisiones nuevas: los límites son los de D-11.

## 5. Pieza 4 (V0.40): pantalla de aprobación con las cifras de la §8

**Dificultad:** baja. **Parte de:** V0.39. **Tema del ZIP:** «pantalla con las cifras de F».

**Kit de contexto:** de `validador/orquestador.py`, solo `pantalla_aprobacion` y `_comprobar_aprobacion`. Además, de `validador/control_f.py`, `_controles_contexto` (para saber qué hay en el contexto), y `pruebas/pruebas_aprobacion.py`. En la Constitución, la §6 (cola de aprobaciones: «cifras calculadas por F, sin texto de un LLM»).

**Problema.** Desde V0.36, F decide con un contexto (precio del intermediario, actividad del día, pérdida de la semana, eventos), pero la pantalla que el operador aprueba no lo enseña. El operador debe ver con qué cifras aprobó F, sin abrir el informe.

**Diseño exacto.** Todo sale de `cf["entradas"]["contexto"]` y de `cf["entradas"]["politica"]` del propio informe; no se recalcula nada con el estado actual. En `pantalla_aprobacion`, añade al diccionario `p`, antes de calcular `p["hash"]`, estos campos:

- `precio_intermediario`: el valor, o `None`.
- `precio_intermediario_en`: su `fecha_hora`, o `None`.
- `deriva_pct`: `round(abs(limite / precio - 1) * 100, 4)`, o `None` si no hay precio.
- `importe_dia_eur`: `round(actividad.importe_dia_eur + importe, 2)`, con el `importe` de esta pantalla.
- `limite_dia_eur`: `politica.importe_max_dia_eur`.
- `perdida_semana_eur` y `limite_semana_eur`.
- `ordenes_ultima_hora` y `limite_ordenes_hora`.
- `eventos_f`: la lista de eventos del contexto tal cual (pueden ser `None`).

Con la anulación de un veto, el importe es el de la cantidad anulada `q`, como ya se hace.

Como el hash de la pantalla incluye estos campos, el operador aprueba también estas cifras. No hay que cambiar `_comprobar_aprobacion`, que compara contra la pantalla guardada; comprueba que sigue funcionando.

Si `consola.py` presenta pantallas al operador, añade las líneas nuevas en el mismo formato. Hoy no las presenta: no la toques.

**Batería nueva:** `pruebas/pruebas_pantalla_f.py`, con al menos 15 comprobaciones. Como mínimo:

- los campos nuevos están y coinciden con el contexto del informe;
- `deriva_pct` calculado a mano con un precio distinto del límite (registra una cotización con `o.registrar_cotizacion` antes del informe, dentro del 2 %);
- `importe_dia_eur` suma lo ya autorizado hoy: autoriza antes otro expediente con `hasta(o, "AUTORIZADA")` y `hasta(o, "PROPUESTA", n=3)`;
- tocar un campo nuevo de la pantalla guardada (`o.pantallas[eid]["deriva_pct"] = 0`) hace que autorizar dé O-27;
- la pantalla sigue sin textos (ni «texto», ni «resumen», ni «tesis»);
- con una anulación de veto, el importe del día usa la cantidad anulada;
- el hash cambia si cambia cualquiera de los campos nuevos.

**Aceptación:** pasan todas las baterías, `pruebas_aprobacion.py` incluida sin cambios.

**Deuda:** ninguna fila nueva. En las notas del briefing, una línea con los campos nuevos de la pantalla.

## 6. Pieza 5, opcional (V0.41): T-44, reducción parcial declarada a mano

**Dificultad:** media. Es la única que toca el estado de una posición. **Parte de:** V0.40. **Tema del ZIP:** «reducción parcial a mano».

**Hazla solo si las cuatro anteriores están en verde.** Si se complica, entrega el Documento 0 y la batería de pruebas escrita aunque falle (con la lista de lo que falla), sin tocar `validador/`. También me sirve.

**Kit de contexto:**

- `validador/manual_g.py` entero.
- De `validador/orquestador.py`: `registrar_manual`, `_reglas_manual`, `comprobar_manual`, `posicion_transicion` (la parte de REDUCIENDO y protecciones), `_anota_pos`, `CAMPOS_POS` y `_posicion_ok`.
- De `validador/ejecucion_g.py`: `declarar_manual`, `_stops_de`, `_neto`, `_cuadra` y `reducir` (como modelo de reducción con stop redimensionado).
- `pruebas/pruebas_manual.py` (sobre todo `abierta_l1` y los cierres manuales) y `pruebas/pruebas_reduccion.py` (solo para ver cómo se comprueba un stop redimensionado).

**Problema (deuda T-44).** Hoy un registro CT-G-14 vinculado a una POSICION solo puede ser un cierre total (RM-06). Si el operador vende una parte a mano fuera del sistema, no lo puede declarar y la conciliación lo ve como discrepancia.

**Diseño exacto.** Sigue el patrón de T-12: primero el stop nuevo por lo que queda y después se retira el viejo, para que la posición nunca quede sin protección.

1. **`manual_g.py`, rama POSICION, cuando la posición no está REDUCIENDO.** Si `cantidad < p["cantidad"]`, es una reducción parcial manual:
   - exige `proteccion_ref`: el stop nuevo que el operador ya colocó por lo que queda (si falta, **RM-07**);
   - exige que lo que queda, `p["cantidad"] - cantidad`, valga en euros al menos `valor_min_eur` de la política de F. Para eso, pasa en el `ctx` de `validar_manual` un `valor_min_restante_eur` ya calculado por el Orquestador. Si no lo cumple, **RM-12**: «una reducción parcial no puede dejar un resto por debajo del valor mínimo de F: ciérrala entera»;
   - si `cantidad > p["cantidad"]`, sigue siendo RM-06;
   - actualiza el texto de RM-06 y la cabecera del módulo (RM-12 nueva).
2. **`ejecucion_g.declarar_manual`, rama POSICION.** Si es parcial:
   - el neto del intermediario en ese instrumento debe ser exactamente lo que queda (`_cuadra`); si no, G-10;
   - la orden `proteccion_ref` debe estar ACEPTADA, ser de tipo STOP, del lado contrario a la posición, del mismo instrumento y vía, con cantidad igual a lo que queda y precio igual a `p["stop_precio"]`; si no, G-10;
   - solo después cancela los stops viejos de la posición (`_stops_de`), salvo el nuevo, con el mismo bucle de 3 intentos que el cierre total; si uno no se cancela, G-10 y no se registra nada;
   - el cierre total no cambia.
3. **`orquestador.registrar_manual`, rama POSICION parcial.** Antes de mutar, `_reglas_manual` ya lo validó. Después:
   - `p["protecciones_anteriores"] += p["protecciones"]` sin repetidos;
   - `p["protecciones"] = [proteccion_ref]`;
   - añade `proteccion_ref` y `ref_intermediario` a `self.ordenes_usadas`;
   - añade a `p["reducciones"]` un elemento `{"n", "cantidad", "desde", "restante", "manual": True, "orden_id": ref_intermediario, "terminada_en": ahora, "motivo"}`;
   - resta la cantidad a `p["cantidad"]`;
   - anota con `self._anota_pos(p, p["estado"], p["estado"], "OPERADOR", ahora, "reducción parcial manual declarada (CT-G-14): <motivo>", ref_intermediario)`. La posición se queda en su estado (ABIERTA o EN\_REVISION).
   - Comprueba después que `o.integridad() == []` y `o.posicion_integra(pid)`.
4. **Conciliación.** Después, `conciliar` no debe ver discrepancia: la cantidad del intermediario es la nueva y el stop vivo es el nuevo. Si `conciliar` necesita algo más para explicarlo, dilo en el Documento 0 antes de tocarlo.

**Batería nueva:** `pruebas/pruebas_manual_t44.py`, con al menos 25 comprobaciones. Parte de una posición abierta en L1 (`abierta_l1` de `pruebas_manual.py`); el operador vende a mano una parte en el `BrokerSimulado` y coloca un stop nuevo (mira `a_mano`). Como mínimo:

- el caso bueno: cantidad nueva, protecciones, `protecciones_anteriores`, reducciones, el stop viejo cancelado en el intermediario, la conciliación limpia y la integridad OK;
- sin stop nuevo (RM-07);
- un stop nuevo por otra cantidad, a otro precio, del lado equivocado o de otro instrumento (G-10);
- el neto del intermediario no cuadra (G-10);
- un resto por debajo del valor mínimo (RM-12);
- más cantidad que la posición (RM-06);
- una posición REDUCIENDO sigue con la regla de antes;
- un registro duplicado (O-03);
- dos reducciones manuales seguidas;
- después de una reducción manual, el cierre total manual por lo que queda funciona;
- H sigue vigilando la posición con el stop nuevo (una pasada de `vigilancia` sin incidencias).

**Aceptación:** pasan todas las baterías. La comprobación antigua de `pruebas_manual.py` que esperaba RM-06 para un cierre parcial debe cambiar a lo nuevo: explícalo, y añade una que siga exigiendo RM-06 cuando la cantidad supera la posición.

**Deuda:** T-44 queda RESUELTO.

## 7. Prompt de revisión independiente

Este paso es el que más defectos caza, así que no se salta.

- Abre una conversación **nueva** de GLM, sin el historial de la pieza.
- Adjunta el ZIP de la pieza ya en verde.
- Pega este texto, cambiando lo que va entre ángulos por la sección de la pieza: su «Problema» y su «Diseño exacto». No pegues el Documento 0 ni las conclusiones de la conversación anterior: el revisor debe leer el código sin que nadie le diga que está bien.

```
Eres revisor independiente de código Python del proyecto Robot Investor (en español). No has escrito este código. Tu trabajo es encontrar defectos reales, no aprobarlo.

Qué pretende el cambio que revisas:
<pega aquí el "Problema" y el "Diseño exacto" de la pieza>

Ficheros que debes leer: <los del kit de contexto de la pieza> y la batería nueva <nombre>.

Principios del proyecto: determinista; falla cerrado (ante dato ausente, ilegible o raro, rechazar o tomar el caso prudente, nunca el favorable); en el Orquestador se valida todo antes de mutar estado porque el decorador @_seguro solo restaura el reloj; nada lanza excepciones hacia fuera; lo auditable va en la cadena de hashes; no se debilitan pruebas existentes.

Busca, sin limitarte a ello: caminos que no fallan cerrado; mutaciones de estado antes de validar; excepciones posibles (None, tipos raros, NaN, inf, fechas mal formadas o sin zona, días frontera UTC); comparaciones con < donde debería ser <= o al revés; dobles conteos u omisiones en sumas; datos que se pueden manipular desde fuera; diferencias entre lo que dice el diseño y lo que hace el código; pruebas que no prueban lo que dicen (por ejemplo, que pasarían también sin el cambio).

Para cada hallazgo escribe un script mínimo que se ejecute desde la carpeta marcoC (sys.path con validador/ y pruebas/) y que imprima "FALLA" si el defecto existe y "OK" si está corregido. No informes sospechas que no puedas reproducir. No modifiques el código del proyecto.

Devuelve una lista numerada: gravedad (alta/media/baja), fichero y función, el defecto en una o dos frases, el escenario concreto y el script completo.
```

**Después:**

1. Ejecuta cada script contra el ZIP: si GLM no puede, lo haces tú. Descarta los que den OK de entrada, porque no reproducen nada.
2. Vuelve a la conversación de la pieza y pégale los hallazgos que dan FALLA con sus scripts.
3. GLM corrige cada uno con su prueba de regresión en la batería nueva (`r01_...`, `r02_...`) y vuelve a pasar todas las baterías.
4. Ejecutas otra vez los scripts del revisor: todos deben dar OK.
5. Si alguno ya no llega a su comprobación porque el arreglo cambió el comportamiento, que lo explique.
6. Todo queda anotado en `revision.md`: hallazgo, gravedad, arreglo, prueba que lo cubre y resultado del script.

## 8. Plantillas de entrega

GLM las rellena y las deja en `marcoC/entrega_glm/V0.xx/`. Están en Markdown sencillo; el lunes las paso yo a Claude Docs.

**`Documento_0.md`:**

```
# Documento 0 — <T-xx o tema> (V0.xx) — GLM, pendiente de revisión

## 1. Problema y alcance
Qué faltaba y por qué importa (con la deuda o la sección de la Constitución). Qué entra en esta versión y qué queda fuera.

## 2. Diseño
Cómo funciona, en prosa y con listas cortas: datos nuevos, dónde se calculan, cuándo se comprueban, qué pasa en cada caso límite. Valores nuevos con [PROPUESTO] y la decisión del operador que los ratificará.

## 3. Reglas y comprobaciones
Tabla: código (regla o aviso), qué comprueba, efecto. Cambios en reglas existentes.

## 4. Códigos, API, pruebas y revisión independiente
Funciones nuevas o cambiadas con su firma. Batería nueva y número de comprobaciones; pruebas antiguas que cambiaron y por qué. Hallazgos del revisor numerados con su gravedad y cómo se corrigió cada uno. Número de baterías que pasan.

## 5. Límites y deuda técnica
Lo que no resuelve, lo aproximado, lo que depende del operador. Filas de deuda que cambian.
```

**`notas_deuda.md`:** las filas que cambian en «Deuda técnica y pendientes del operador», en dos listas:

- tabla T: id, texto nuevo de la cuarta columna (por ejemplo, «RESUELTO en V0.38: …»);
- tabla D: filas nuevas con id, qué debe decidir el operador, dónde se usa y valor de partida \[PROPUESTO\].

**`notas_briefing.md`:** un párrafo técnico denso que empiece por «V0.xx: …», con los nombres exactos que otra persona necesitaría para seguir sin leer el código: funciones, atributos, claves de configuración, códigos, valores por defecto y ayudas de prueba.

**`revision.md`:** cada hallazgo con gravedad, script, resultado antes y después, arreglo y prueba de regresión.

**`salida_pruebas.txt`:** la salida del bucle de la sección 0 (vacía si todo pasa) más el número de comprobaciones de la batería nueva.

**Nombre del ZIP:** «Marco comun de C - \<tema> - V0.xx (AAAA-MM-DD) GLM.zip», con la carpeta `marcoC` completa, sin `__pycache__`, y la carpeta `entrega_glm` dentro de `marcoC`. Nunca se sobrescribe un ZIP anterior.
