# Constitución Global del Robot Inversor — V0.6

Nov 9, 2026 · @Dani

## 0. Estado, alcance y modo de uso

Esta V0.6 (9 de noviembre de 2026) **sustituye a la V0.5**: incorpora la **enmienda 3** (T-59: cuestionario guiado de configuración, valores por defecto para cualquier usuario, cambios a través del Broker y una copia por usuario), **ratificada por el operador** ese mismo día (cambios 39 a 42 y decisiones D-44 a D-47). La V0.5 (9 de noviembre de 2026) sustituyó a la V0.4: incorporó la **enmienda 2** (los 27 puntos de T-58 en la deuda técnica), aplicada a petición del operador y **ratificada por él el 9 de noviembre de 2026** (tabla «De la V0.4 a la V0.5» abajo y decisiones D-28 a D-41, todas `[RATIFICADO]`). Recoge también las cuatro reglas de diseño y decisión que el operador fijó el 8-11-2026 (cambio 38, D-42), con su encaje con la Fase 2. Ese mismo día el operador ratificó también las decisiones de la V0.1 que seguían propuestas (D-08 a D-16) y los apartados que no dependían de ninguna decisión numerada (D-43): **toda la Constitución queda ratificada**, salvo los valores que el operador tiene aplazados (pendientes P-xx, sesión T-57). Sus números quedan aplazados como pendientes del operador (P-25 a P-35), igual que el resto de sus decisiones de perfil y técnicas hasta completar la arquitectura (T-57). Al redactarla se añadió lo que no venía literal en T-58, y el operador lo ratificó con el resto: los principios P19 y P20, que amplían los invariantes; que SC-3 no cuente para el tope de bloques; el destino de las aportaciones durante la hibernación; las exenciones de la rentabilidad mínima; y la preferencia por un revisor de otro proveedor de IA. La V0.4 (7 de noviembre de 2026) incorporó la **enmienda 1**, ratificada por el operador ese día (tabla «De la V0.3 a la V0.4» y decisiones D-20 a D-27). La V0.3 sustituyó a la V0.2 y a la V0.1; nació de una prueba de recorrido con cuatro casos (18 huecos) y de una revisión adversarial independiente (13 hallazgos), y el operador ha autorizado modificar la idea base, incluidos los bloques A y B.

**Alcance.** Sistema personal de inversión con **capital propio únicamente**: investiga, analiza, compara, construye carteras, controla el riesgo, ejecuta bajo autorización y aprende de sus resultados. No presta servicio a terceros; si eso cambiara, habría que revisar la normativa aplicable antes de seguir. `[RATIFICADO]` (D-47) **Una copia por usuario:** varias personas pueden usarlo, cada una con **su propia copia y su propio dinero**. Cada copia es de un solo usuario y gestiona solo su capital; en este documento, «operador» es el usuario de cada copia. Si un usuario gestionara el dinero de otro, le recomendara inversiones personalizadas o cobrara por ello, ya no sería uso privado y habría que consultar antes a un abogado (normativa de la CNMV y MiFID II).

**Precedencia.**

1. En materias globales (contratos entre bloques, autonomía, control, identificadores) prevalece esta Constitución sobre el Documento 0 de cualquier bloque.
2. En lo interno de un bloque prevalece su Documento 0, siempre que no contradiga este documento.
3. Un conflicto detectado se registra en el §15 y lo resuelve el operador.

**Lenguaje normativo.** DEBE = obligatorio; DEBERÍA = salvo razón registrada; PUEDE = opcional. Etiquetas de decisión: `[RATIFICADO]` (lo ha decidido el operador), `[PROPUESTO]` (propuesta de Claude pendiente de ratificar) y `[ABIERTO]` (sin decidir).

**Cómo se usa.** Cada conversación de construcción empieza con esta Constitución, la ficha de interfaz del bloque (§2) y los contratos que le afectan (§5).

**Qué cambia respecto a la V0.1.** `[RATIFICADO]` el 9-11-2026 (D-08 a D-16 y D-43).

| N.º | Cambio | Problema que resuelve | Sección |
| --- | --- | --- | --- |
| 1 | Construcción por **fases con compuertas**: primero una rebanada vertical (divisas, una cartera, simulación y manual) | Demasiadas piezas para una persona | §14 |
| 2 | Los bloques A, B y C pasan a ser **núcleo común + perfil por tipo de activo** | 36 bloques casi iguales | §2 |
| 3 | El Broker se divide en **tres papeles**: conversacional, orquestador determinista y gestores de cartera | Cuello de botella y límites de contexto | §2, §3 |
| 4 | **Sobre común por capas**, con clases de comparabilidad, `NO_ESTIMABLE` válido y congelación diferida | Falsa precisión y contratos prematuros | §5 |
| 5 | **Dos ciclos**: oportunidad y posición; ruta determinista para estrategias validadas | Huecos de estados; vuelta a análisis de posiciones abiertas | §4 |
| 6 | Seguridad en el **intermediario y en límites nominales**; stops nativos; el kill-switch solo cancela entradas; vigilante con latido | Control que depende de la misma fuente; kill-switch inseguro | §8 |
| 7 | Aprendizaje **realista**: diario, topes ex ante, tesis descompuestas en sub-pronósticos de ≤ 12 meses | Muestra insuficiente | §9 |
| 8 | **Verificación diversa** y lectores de web en sandbox | Sesgos correlacionados e inyección de instrucciones | §3, §12 |
| 9 | **Capa de adaptadores**, simulador propio y ficha de restricciones reales | Dependencia de broker y datos desconocidos | §3, §14 |
| 10 | **Controles sobre el operador** y presupuesto duro de coste | Error humano y bucles de coste | §6, §11 |

**Qué cambia de la V0.2 a la V0.3.** Nace de una segunda revisión independiente de la arquitectura y de la decisión del operador de tratar los perfiles de C como piezas de entrega propia. Todos sus cambios están `[RATIFICADO]` desde el 5-11-2026 (D-17 a D-19).

| N.º | Cambio | Problema que resuelve | Sección |
| --- | --- | --- | --- |
| 11 | Cada perfil `C-<COD>` se entrega como **paquete propio** (agentes, protocolo, pruebas), pero bajo **un solo núcleo** y con estado `ACTIVO` o `NO_CONSTRUIDO`. Solo se construye el perfil que una cartera necesite | Perfiles tan complejos como un bloque, sin multiplicar la gobernanza por doce | §2 |
| 12 | Nuevo **Bloque K · Datos y calidad de datos** (antes SC-2 y el calendario de SC-8). Determinista, sin agentes LLM, falla cerrado y es el único que emite el sello de fecha de corte | Un fallo silencioso de datos contamina todo; fechas de corte incoherentes entre análisis | §2, §3 |
| 13 | Nuevo **Bloque N · Consola del operador**: informes, cola de aprobaciones, avisos, explicaciones y panel de salud | El operador es inexperto y no puede leer contratos | §2, §6 |
| 14 | Nuevo **Bloque M · Riesgo de cartera** (Fase 3). Asesora a E; F sigue calculando por su cuenta, con su propio código y datos | Separar análisis de exposición y correlación del control duro, sin perder la independencia de F | §2, §8 |
| 15 | Las **noticias** pasan a un servicio aislado (SC-11) con salida estructurada y sin texto libre. No se crea un bloque L de contexto | Contenido hostil por una vía común a C, D y E | §3, §12 |
| 16 | **Criterio de bloque ampliado** (3 de 5) y **tope de bloques activos** (8 en las Fases 1 y 2), con panel de salud en N | Complejidad ingobernable para una persona | §2 |

**Qué cambia de la V0.3 a la V0.4 (enmienda 1).** `[RATIFICADO]` el 7 de noviembre de 2026, también sus números (D-27); solo quedan por elegir las fuentes de noticias de SC-11 (P-24).

| N.º | Cambio | Problema que resuelve | Sección |
| --- | --- | --- | --- |
| 17 | **A Forex y B Forex fuera** del sistema; se usan A y B generales, que analizan todo tipo de activos. La Fase 1 sigue en divisas | Eran pruebas; dos variantes de los mismos bloques | §2, §14 |
| 18 | **Broker Personal** como bloque (sus tres papeles), con lenguaje para inexpertos, **perfil inversor y de riesgo** construido en las conversaciones y **política de inversión personal** | El operador no es experto; decisiones en caliente | §2, §3, §6 |
| 19 | **Contrapesos de la abstención** (referencia invertida, embudo visible, alarma de sequía, seguimiento de lo descartado) y **cartera sombra pasiva** como prueba de que el robot aporta valor | Que el control no deje invertir nunca; invertir sin aportar nada | §1, §7, §9 |
| 20 | **Intercambio entre bloques por el Orquestador** y **registros comunes** (análisis vigentes, riesgos geopolíticos, tendencias tecnológicas, posicionamiento) | Trabajo duplicado; datos alterados por un LLM en el camino | §2, §3 |
| 21 | **Economía del análisis:** tope de coste por oportunidad, embudo de lo barato a lo caro, análisis incremental, trabajo por eventos, caché y lotes | Analizar cuesta más de lo que se puede ganar | §10 |
| 22 | **Calidad de las decisiones:** clase de referencia, freno a la rotación, fiscalidad en la decisión, concentración mínima antes de M y presupuesto de complejidad | Optimismo, rotación, impuestos ignorados, complejidad | §5, §7, §8, §9 |
| 23 | **Cobertura nueva sin bloques nuevos:** geopolítica (SC-11 mínimo en la Fase 1), radar tecnológico en A, small caps y spin-offs en `C-RV`, startups en `C-ALT` y seguimiento de grandes inversores en K | Huecos de información | §2, §3, §8, §14 |

**Qué cambia de la V0.4 a la V0.5 (enmienda 2).** `[RATIFICADO]` el 9 de noviembre de 2026; sus números siguen pendientes (P-25 a P-35). Entre paréntesis, el punto de T-58 del que sale cada cambio.

| N.º | Cambio | Problema que resuelve | Sección |
| --- | --- | --- | --- |
| 24 | **Entrada por cualquier bloque, salida al dinero solo por F y G:** vía `DIRECTA` y modo `CONSULTA` (25) | El recorrido A→B→C→D obligatorio para una simple comparación | §1, §2, §4, §4.1 |
| 25 | **Motor de cálculo avanzado** (SC-3 ampliado: servicio común que se entrega como un bloque y no cuenta para el tope) y su **módulo de proyecciones** del plan (1, 13) | Cálculos pesados dispersos; el operador no ve hacia dónde va su plan | §3, §9 |
| 26 | **Rentabilidad mínima exigida** a cada inversión y **todo medido después de la inflación** (2, 5) | Invertir en lo que no compensa su riesgo; rentabilidades que engañan | §1, §7, §8, §9, §10 |
| 27 | **Plan de largo plazo:** aportaciones mensuales como ciclo propio, vehículo fiscal en la decisión y camino de riesgo que baja al acercarse el objetivo (3, 4, 6) | Un plan de décadas tratado como operaciones sueltas | §4, §7 |
| 28 | **Protecciones del operador:** colchón de emergencia fuera del robot, modo hibernación y revisión anual guiada (7, 8, 9) | Invertir el dinero que hará falta; un sistema que sigue solo si el operador desaparece | §2, §6, §11, §12 |
| 29 | **Vigía de régimen económico**, que solo endurece (12) | Llegar a una crisis con los límites de tiempos normales | §3, §8 |
| 30 | **Parámetros contextuales** y **asesor de configuración** en el Broker Personal (14) | Números fijos que no sirven igual para todo activo y contexto; un operador inexperto ante decenas de parámetros | §2, §10 |
| 31 | **Varios análisis independientes** por decisión y **probabilidades verificables** (15, 18) | Un único análisis sin medida de su incertidumbre; tesis que no se pueden comprobar | §3, §4.1, §5, §9 |
| 32 | **Los agentes se ganan su peso:** historial verificado, torneo de pronósticos, mínimo de decisiones, aspirante frente a titular y autopsias (16, 19, 20, 21) | Fiarse de un agente sin pruebas; no aprender de los errores | §9 |
| 33 | **Incentivos por diseño del sistema** y defensas contra la ley de Goodhart (24) | Agentes que optimizan la métrica en lugar del objetivo | §9 |
| 34 | **J como laboratorio de estrategias, modelos, instrucciones y agentes**; aprendizaje automático solo como aspirante; catálogo de bases de datos y entrenamientos (17, 22, 27) | Nadie se encarga de entrenar; modelos complejos sin referencia con que compararlos | §2, §9, §10, §13, §14 |
| 35 | **Escalera de verificación** y verificaciones externas (23) | Dar por buena una mejora que solo funciona en el pasado | §1, §7, §9 |
| 36 | **Cambios de modelo de IA con conjunto dorado** e **historial exportable** en formatos abiertos (10, 11) | Cambiar de modelo a ciegas; depender de un proveedor para recuperar la propia historia | §9, §10, §12 |
| 37 | **Enchufabilidad:** ficha de cada bloque, registro, batería de conformidad, estado por bloque y adaptadores también para modelos de IA (26) | Bloques que no se pueden sustituir sin tocar el resto | §3, §5, §13, §14 |
| 38 | **Reglas del operador del 8-11-2026**, que solo vivían en el briefing: todo bloque sirve para cualquier tipo de activo y se diseña como núcleo + perfiles desde el primer día; A y B se revisan con el operador antes de conectarlos; conversación de diseño con el operador antes de cada bloque sin construir; decisiones del operador aplazadas hasta completar la arquitectura | Reglas fijadas por el operador que la fuente de verdad no recogía | §2, §14, §15 |

**Qué cambia de la V0.5 a la V0.6 (enmienda 3).** `[RATIFICADO]` el 9 de noviembre de 2026 (T-59).

| N.º | Cambio | Problema que resuelve | Sección |
| --- | --- | --- | --- |
| 39 | **Cuestionario guiado de configuración:** preguntas de opción múltiple, explicadas en euros y sin jerga, con un asesor que entiende la respuesta libre y confirma cada interpretación | Un usuario inexperto ante decenas de parámetros técnicos | §2, §15 |
| 40 | **Valores por defecto prudentes para cualquier usuario**, con su justificación; el cuestionario solo personaliza | Un sistema que no funciona hasta que alguien decide todo | §6, §10, §15 |
| 41 | **Cambios posteriores por el mismo cuestionario, a cargo del Broker Personal**, con la asimetría de riesgo y la validación de siempre | Cambiar la configuración exige saber dónde y cómo | §2, §6 |
| 42 | **Una copia por usuario:** cada persona con su copia y su dinero; nada personal en el repositorio; actualizar el código sin perder los datos; copias sin datos compartidos por defecto | El operador y sus compañeros quieren usarlo, cada uno con lo suyo | §0, §10, §12, §13, §16 |

## 1. Propósito y principios rectores

**Propósito.** Producir decisiones de inversión fiables, trazables y mejorables con capital propio, y abstenerse cuando la evidencia no basta. La fiabilidad pesa más que la rentabilidad: la arquitectura no garantiza rentabilidad, solo reduce los errores evitables y los hace visibles.

Los principios siguientes son invariantes. Ningún bloque, prompt ni herramienta puede contradecirlos.

1. **P1 · Separación de poderes.** Quien propone no aprueba, quien aprueba no ejecuta y quien ejecuta no interpreta.
2. **P2 · Los controles duros no son LLM.** Límites, permisos, validación de órdenes, veto de riesgo y kill-switch son código determinista. Un LLM puede pedir una excepción, nunca concederla.
3. **P3 · Las cifras no las escribe un agente.** Las calcula un motor reproducible y los agentes las citan por identificador. Todo campo numérico declara el modelo o método que lo produce; sin modelo declarado, es `SUPUESTO`.
4. **P4 · Contratos primero, congelados con criterio.** Los bloques solo se hablan mediante contratos con esquema JSON versionado. Un esquema se congela después de comprobarlo con casos reales (§5), no antes.
5. **P5 · Abstenerse es un resultado válido, pero vigilado.** La referencia de toda comparación es no hacer nada (el benchmark de cada cartera). Abstenerse significa estar en ese benchmark, no en efectivo parado salvo que el mandato lo diga, y el sistema vigila que los controles no impidan invertir siempre (§7, §9).
6. **P6 · Pronósticos falsables.** Toda tesis material declara qué la invalidaría y se registra antes de conocerse el resultado.
7. **P7 · Evidencia con procedencia.** Todo dato lleva fuente, fechas y etiqueta epistémica (`VERIFICADO`, `ESTIMADO`, `SUPUESTO`). Los datos originales no se sobrescriben y las pruebas históricas no usan información posterior (*look-ahead*).
8. **P8 · Aprendizaje gobernado.** Ningún aprendizaje cambia límites, estrategias, modelos o parámetros por sí solo. Todo cambio se propone, se valida, se aprueba y se versiona.
9. **P9 · Autonomía graduada y revocable.** Se concede por cartera y tipo de acción, sube con resultados medidos y baja de inmediato ante cualquier anomalía. Ante la duda, no se actúa.
10. **P10 · Toda decisión material es reconstruible.** Datos, agentes, versión de reglas, controles, aprobaciones y resultado.
11. **P11 · El contenido externo es dato, no instrucción.** Los agentes que lo leen no tienen acceso a la cartera ni a herramientas de acción (§12). Las credenciales nunca están en el contexto de un agente.
12. **P12 · Especializar sin duplicar.** Los bloques por tipo de activo son un núcleo común más un perfil (§2). Cambia el perfil, no el esqueleto.
13. **P13 · Degradación segura.** Cada bloque declara qué hace ante datos obsoletos, contrato incompatible o servicio caído. Por defecto: detenerse, marcar y escalar.
14. **P14 · Mínimo primero.** Se construye una rebanada vertical que funcione de punta a punta antes de ampliar (§14). Una pieza sin demanda real no se construye.
15. **P15 · Lo crítico no depende de un LLM ni de una sola fuente.** La seguridad vive en el intermediario y en límites nominales; los agentes LLM del mismo modelo no cuentan como verificación independiente.
16. **P16 · Lo que no se sabe se declara.** `NO_ESTIMABLE` es un valor válido y preferible a una cifra inventada.
17. **P17 · El robot demuestra que aporta valor.** Se compara siempre, después de costes de análisis, comisiones, impuestos `[RATIFICADO]` **e inflación**, con una cartera sombra pasiva (§9). Si no la supera en el plazo fijado, se propone gestionar de forma pasiva.
18. **P18 · El análisis vale lo que puede cambiar.** Nada se analiza más caro de lo que la decisión puede ganar, nada se investiga dos veces y lo barato va antes que lo caro (§10).
19. **P19 · El peso se gana con pruebas.** `[RATIFICADO]` Ningún agente, modelo o estrategia gana peso en las decisiones ni autonomía sin un historial verificado y suficiente (§9). Toda mejora sube la escalera de verificación peldaño a peldaño, y quien la entrena no la puntúa.
20. **P20 · Se entra por cualquier bloque; al dinero, solo por F y G.** `[RATIFICADO]` Una consulta puede empezar y terminar en cualquier bloque; todo lo que acabe en una orden pasa por E, F y G sin excepción (§2, §4.1).

## 2. Mapa de bloques

El sistema tiene **bloques** (A–N), el **Broker Personal** (un bloque con tres papeles) y **servicios comunes** (§3). Cada fila de la tabla es la **ficha de interfaz** mínima: un bloque nuevo DEBE ajustarse a ella.

**Familia por tipo de activo: núcleo común + perfil.** `[RATIFICADO]` (D-10) A, B y C no se construyen doce veces. Cada uno es un **núcleo** (agentes, contratos, módulos del Motor, validación y ejecutor) más un **perfil por tipo de activo** (vocabularios, playbooks, fuentes, áreas de conocimiento, parámetros e instrumentos). Los prompts de los agentes se componen de una plantilla común y el perfil.

**Todo bloque sirve para cualquier tipo de activo.** `[RATIFICADO]` (D-42, regla del operador del 8-11-2026) Ningún bloque se diseña «para divisas» ni para un solo tipo de activo: todos se diseñan desde el primer día como núcleo común más perfiles, y la Fase 1 en divisas es solo el primer recorrido completo. Hoy solo el perfil `C-DIV` es específico de divisas. `[RATIFICADO]` Encaje con la Fase 2: los bloques **nuevos** nacen ya con núcleo y perfiles; A y B, que ya existen, se reorganizan en la Fase 2, cuando haya un segundo perfil real con que comprobar qué es núcleo y qué es perfil.

La refactorización de A y B a núcleo + perfil se hace en la **Fase 2** (§14), cuando exista un segundo perfil real. Con un solo caso se adivina el núcleo; con dos se deriva. Hasta entonces, A (V5.1) y B (V2.1) se usan tal cual, con adaptadores mínimos. `[RATIFICADO]` A Forex y B Forex fueron pruebas y **no forman parte del sistema** (D-20); las divisas las cubren A y B generales (en A, su Analista de Divisas ya funciona con 5 de sus 11 fichas FX programadas; faltan FX-BEER, FX-BRK, FX-COINT, FX-PPA, FX-REGIME y FX-STL).

**Perfiles como paquetes de entrega propios.** `[RATIFICADO]` (D-17) Cada perfil `C-<COD>` es complejo (muchos agentes, fuentes y playbooks) y se construye, prueba y entrega como un **paquete propio**, igual que un bloque. Lo que no tiene propio es el esqueleto: todos cumplen el mismo núcleo y el mismo sobre CT-G-02, y ninguno los modifica por su cuenta (una enmienda se propone en el §15). Cada perfil tiene un estado: `ACTIVO` o `NO_CONSTRUIDO`. Un perfil `NO_CONSTRUIDO` devuelve `NO_ESTIMABLE` y el Broker no lo encarga. Un perfil solo se promueve a bloque independiente si necesita su propia frontera de seguridad o su propio modo de fallo (por ejemplo, `C-DER` o `C-CRI`).

**Criterio para crear un bloque nuevo.** `[RATIFICADO]` (D-19) Un componente es bloque propio si cumple **al menos tres** de estas cinco condiciones: (1) lo usan dos o más bloques; (2) tiene una frontera de seguridad o un modo de fallo distinto; (3) tiene un ritmo o una naturaleza distinta (determinista frente a LLM); (4) se puede validar por separado; (5) tiene un **dueño que lo valida** y su coste de coordinación (contratos nuevos) es menor que la ganancia.

**Tope de bloques activos.** `[RATIFICADO]` (D-19) En las Fases 1 y 2 no hay más de **ocho** bloques activos a la vez (en la Fase 1: A, B, `C-DIV`, D, E, F, G y K, con N mínimo y el Broker Personal). El panel de N muestra el estado de cada uno en verde, ámbar o rojo, y las pruebas automáticas de contrato (SC-6) avisan de la deriva, de modo que el operador no revisa contratos a mano.

**Bloques K, M y N.** `[RATIFICADO]` (D-18) K es determinista y falla cerrado: si el dato es dudoso, se detiene. M asesora a E con análisis de exposición, correlación y escenarios, pero F **no consume su salida**: calcula la exposición con su propio código y sus datos (P2, P15). N es la única superficie que ve el operador.

**El Broker Personal: un bloque en tres papeles.** `[RATIFICADO]` (D-21) El Broker Personal es un bloque completo, por su implicación en todo el sistema, pero no un solo agente: uno con juicio para todo no escala (contexto, coste, latencia) y mezcla juicio con flujo. Sus tres papeles conservan sus prohibiciones.

| Papel | Naturaleza | Hace | No hace |
| --- | --- | --- | --- |
| **Broker conversacional** | Agente LLM | Dialoga con el operador, decide en excepciones, resuelve conflictos entre carteras y atiende peticiones nuevas | Llevar el flujo diario, calcular, aprobar riesgo, enviar órdenes |
| **Orquestador** | Código determinista | Mueve los expedientes por sus estados, gestiona colas, plazos, reintentos y **presupuestos de coste y tiempo**, y lanza las rutinas | Juzgar inversiones |
| **Gestores de cartera** (uno por libro) | Agentes LLM acotados + código | Llevan el flujo cotidiano de su libro dentro del mandato, usando el expediente como memoria | Hablar entre sí (lo hacen por el Orquestador) o salirse del mandato |

**Lo que hace el Broker Personal con el operador.** `[RATIFICADO]` salvo indicación.

1. **Lenguaje para inexpertos.** Todo lo que el Broker y N dicen al operador se explica sin jerga: qué pasa, qué significa para su dinero y qué se le pide decidir, con ejemplos en euros. Un término técnico solo aparece con su explicación al lado.
2. **Perfil inversor y de riesgo** (vive en SC-1, no en la memoria del chat): conocimientos, experiencia, situación económica, objetivos, horizonte, caída tolerable y reacción ante pérdidas, versionado. El Broker lo completa con preguntas sencillas y con ejemplos a lo largo de las conversaciones; propone cada cambio y el operador lo confirma; una contradicción entre respuestas se pregunta, nunca se resuelve en silencio. Las reglas sobre el riesgo están en el §6.
3. **Política de inversión personal:** un documento corto que el operador escribe con el Broker en un momento tranquilo (qué hará ante caídas del 10, 20 y 30 %, qué dinero no tocará nunca, para qué invierte). Antes de aceptar una orden del operador que la contradiga durante una caída, el Broker se la recuerda y le pide confirmar. No impide nada; hace consciente la decisión.
4. **Asesor de configuración** `[RATIFICADO]` (D-34). Dentro del Broker conversacional, propone los parámetros del sistema a partir del perfil del operador (§10): cada propuesta se explica por sus consecuencias en euros («con este límite, en una caída como la de 2020 habrías perdido como mucho…»), con su simulación en el Motor. `[RATIFICADO]` (D-44, D-46) Trabaja con un **cuestionario guiado**: cada decisión es una pregunta de opción múltiple (de 2 a 4 opciones, la recomendada primero, más una respuesta libre «dímelo con tus palabras»), y cada opción se explica por sus consecuencias en euros, con ejemplos y sin jerga. El asesor interpreta la respuesta libre aunque no use lenguaje técnico, la traduce a una opción y **la confirma reformulándola** («entiendo que prefieres X; ¿es así?»); nunca la interpreta en silencio. El cuestionario va de lo fácil a lo difícil, se puede pausar y retomar, termina con un resumen y no aplica nada hasta la confirmación final; todo queda versionado en SC-1. Se usa en la **configuración inicial** (la sesión en que el operador toma las decisiones aplazadas, T-57) y en **cualquier cambio posterior**, que el operador pide cuando quiera conversando con el Broker. El cuestionario es la puerta, no un atajo: bajar el riesgo se aplica al momento; subirlo exige segundo factor y espera (§6); y una respuesta que cambia un límite, una estrategia o un modelo sigue además la ruta única de cambios (§9) antes de aplicarse. Los límites duros de F y el kill-switch nunca los fija un modelo por su cuenta.
5. **Colchón de emergencia** `[RATIFICADO]` (D-32). El dinero que el operador pueda necesitar a corto plazo vive **fuera del robot**. El Broker comprueba en el perfil que el colchón existe y cubre los meses fijados por el operador `[ABIERTO]` (P-29) antes de proponer invertir más; no lo comprueba en el banco, lo pregunta y lo registra.

**Intercambio entre bloques.** `[RATIFICADO]` (D-23) Los bloques se pasan información a través del Broker Personal, pero **por su parte determinista** (el Orquestador), con contratos cerrados, sin duplicados y con registro. El Broker conversacional lo consulta todo para explicarlo, pero no transporta datos entre bloques: un error o una manipulación en un LLM no puede alterar lo que un bloque le pasa a otro. Antes de encargar un análisis, el Orquestador consulta el registro de análisis vigentes (§3).

| Bloque | Responsabilidad | Recibe | Entrega | No hace |
| --- | --- | --- | --- | --- |
| **A** (núcleo + perfil) | Descubrir oportunidades por tipo de activo; **radar tecnológico continuo** sobre su capa temática (tecnologías del mañana, su fase de adopción e hitos) | Encargo | `paquete_para_bloque_B`; registro de tendencias tecnológicas | Analizar mercado, valorar |
| **B** (núcleo + perfil) | Analizar un ámbito y seleccionar candidatos con su vía de acceso | Encargo (una petición = una propuesta con varios candidatos) | `paquete_para_bloque_C` | Valorar en profundidad, dimensionar |
| **C** (núcleo + perfil) | Valoración profunda de un tipo de activo, con el nivel N0–N3 pedido | Encargo | Sobre común por capas + cuerpo especializado | Comparar entre tipos, decidir |
| **D** | Comparar opciones ya analizadas | Sobres, estado de carteras (solo lectura), benchmark | Comparativa por mandato, con dominancia y sensibilidad | Elegir, dimensionar |
| **E** | Construir carteras, dimensionar y supervisar en conjunto | Propuesta, mandatos, estado de carteras | Plan por libro y vista global | Vetar riesgo, enviar órdenes |
| **F** | Control determinista e independiente | Todo plan o acción material | Aprobado, reducido o vetado, con motivo | Proponer inversiones |
| **G** | Único canal de órdenes; órdenes de protección; libro y conciliación; registro de ejecuciones manuales | Acciones aprobadas | Estados de orden y libro conciliado | Interpretar tesis |
| **H** | Seguimiento de posiciones y condiciones de salida | Libro de G, condiciones de invalidez, eventos | Alertas y propuestas de revisión | Cerrar posiciones por juicio propio |
| **I** | Evaluación y atribución | Resultados, diario de pronósticos | Informes y propuestas de cambio | Aplicar cambios |
| **J** | Laboratorio de estrategias, **modelos, instrucciones y agentes** `[RATIFICADO]` (D-38): diseño, entrenamiento, backtest, paper trading, validación y registro de versiones (titular, aspirante, retirado) | Hipótesis, datos versionados de K, encargos de I | Estrategias y modelos validados con parámetros congelados | Poner nada en producción, puntuar su propio trabajo o ver la reserva sellada |
| K · Datos y calidad de datos | Ingesta, procedencia, ajustes (dividendos, splits), consulta «punto en el tiempo», calendario de eventos y sello de fecha de corte; **posicionamiento de grandes inversores** (COT de la CFTC, 13F, participaciones significativas de la CNMV, operaciones de directivos) con su fecha de publicación. Determinista, falla cerrado | Fuentes y adaptadores (SC-10) | Datos con sello de corte, calendario, registro de posicionamiento y alertas de calidad | Analizar, valorar o usar LLM |
| M · Riesgo de cartera (Fase 3) | Análisis de exposición agregada, correlación y escenarios adversos que asesora a E | Libro de G, datos de K, mandatos | Informe de riesgo para E | Vetar o limitar (eso es F, que no consume su salida) |
| N · Consola del operador | Informes, cola de aprobaciones, avisos fuera del chat, explicaciones en lenguaje sencillo y panel de salud de los bloques | Planes de E, resultados de F, estado de todos los bloques | Pantallas de aprobación con las cifras de F; avisos con acuse; panel verde, ámbar y rojo | Aprobar por sí misma o alterar cifras |

**Las vías de entrada.** La **discrecional** (A → B → C → D) sirve a activos analizados uno a uno. La **sistemática** (J) sirve a estrategias con reglas validadas y sigue una **ruta determinista** sin LLM en el camino (§4). `[RATIFICADO]` (D-28) La **directa** sirve cuando el Broker Personal ya sabe qué quiere estudiar o comparar: entra por C, D o E sin pasar por A y B, que sirven para descubrir. Todas pasan por F y G sin excepciones.

**Consulta y decisión.** `[RATIFICADO]` (D-28) Una **consulta** (comparar, analizar o proyectar sin intención de invertir) puede empezar y terminar en cualquier bloque y no abre camino a una orden. Una **decisión** es todo lo que puede acabar en una orden: empiece donde empiece, sale por E → F → G con los mínimos del expediente (§4.1). Requisitos mínimos por bloque de entrada:

| Se entra por | Necesita | Si falta |
| --- | --- | --- |
| C | Un encargo CT-G-01 completo | Se rechaza el encargo |
| D | Sobres CT-G-02 vigentes con fecha de corte común | El Orquestador reutiliza los vigentes del registro de análisis y encarga a C un análisis de nivel bajo para lo que falte |
| E | Una comparativa de D, o un único candidato con sobre validado y el motivo de no comparar | Se devuelve a D |
| F y G | Nunca son punto de entrada | — |

El presupuesto por encargo y por día (§11) se aplica igual a las entradas directas.

**Los doce perfiles de C.** `[RATIFICADO]` Código estable `C-<COD>`; `C.n` es solo alias.

| Código | Tipo de activo | Alias `C.n` (orden de A/B) |
| --- | --- | --- |
| C-RV | Renta variable | C.1 |
| C-RF | Renta fija | C.2 |
| C-DIV | Divisas | C.3 |
| C-MP | Materias primas | C.4 |
| C-IDX | Índices bursátiles | C.5 |
| C-FON | Fondos y vehículos de inversión colectiva | C.6 |
| C-DER | Derivados financieros | C.7 |
| C-INM | Activos inmobiliarios cotizados | C.8 |
| C-CRI | Criptoactivos | C.9 |
| C-ALT | Capital privado y alternativos | C.10 |
| C-MON | Monetarios y liquidez | C.11 |
| C-TCV | Tipos de interés, crédito y volatilidad | C.12 |

El operador llamaba «C.1» al analista de divisas y el Documento 0 de B lo designa C.3. Con los códigos el conflicto desaparece: es `C-DIV`.

**Especializaciones dentro de un perfil.** `[RATIFICADO]` (D-26) `C-RV` incluye una especialización en **small caps cotizadas y situaciones especiales** (spin-offs), y B ya tiene a AG-B24 para detectarlas. Las **startups no cotizadas** son de `C-ALT` (Fase 5), con un tope pequeño de cartera fijado por el operador `[RATIFICADO: 2 %]` (P-23).

## 3. Planos, servicios comunes y verificación

Todo componente pertenece a un solo plano, y cada plano tiene una autoridad distinta.

| Plano | Qué contiene | Autoridad | Tecnología |
| --- | --- | --- | --- |
| **Inteligencia** | Broker conversacional, gestores de cartera, A, B, C, verificación, D, J y partes analíticas de E, H e I | Propone. Nunca decide por sí solo sobre riesgo, permisos ni órdenes | Agentes LLM + motores de cálculo |
| **Control** | Orquestador, F, G, matriz de autonomía, cola de aprobaciones, kill-switch y vigilante | Veta, limita y autoriza. Ningún agente del plano de inteligencia puede anularlo | Código determinista, sin LLM en la ruta de decisión |
| **Datos y memoria** | Evidencia, diario de pronósticos, auditoría, libro contable, credenciales | Guarda la verdad. Solo anexado: lo histórico no se reescribe | Almacenes indexados con identificador y hash |

**Servicios comunes (SC).** Se construyen una sola vez, a medida que la fase lo exige. `[RATIFICADO]` (D-08)

| Servicio | Función |
| --- | --- |
| **SC-1 Perfil y mandato** | Fuente única de objetivos, horizonte, benchmark, riesgo y límites por cartera; **perfil inversor y de riesgo** del operador y su **política de inversión personal** (§2) |
| **SC-2 Datos y evidencia** | Pasa a ser el Bloque K (§2): ingesta, procedencia, frescura y consulta «punto en el tiempo». Para precios, posiciones y saldos, la **segunda fuente es el propio intermediario** |
| **SC-3 Motor de cálculo avanzado** (`[RATIFICADO]` nombre nuevo; antes, Motor numérico) | Cálculo reproducible (hash, semilla, fecha de corte). Cada módulo declara su modelo y sus límites de validez. `[RATIFICADO]` (D-29) Sigue siendo un **servicio común** y no cuenta para el tope de bloques activos, pero se construye y se entrega como un bloque (Documento 0 propio, contratos y presupuesto); solo pasa a ser bloque si cumple el criterio del §2. Parte del Motor de Cálculo Avanzado de A: Montecarlo, escenarios, modelos de factores, optimización, pruebas históricas y **proyecciones** (§9), con cola de trabajos, caché por hash y posibilidad de una máquina más potente. Da distribuciones, no predicciones exactas, y su coste cuenta en la economía del análisis (§10) |
| **SC-4 Diario de pronósticos** | Registro de pronósticos congelados y de opciones descartadas, con resolución posterior (§9) |
| **SC-5 Eventos y auditoría** | Registro anexado, con `correlation_id` de extremo a extremo |
| **SC-6 Validador de contratos** | Comprueba esquema y coherencia de cada paquete antes de pasar al bloque siguiente (generaliza G3) |
| **SC-7 Seguridad** | Bóveda de credenciales, segregación de entornos, límites de API, copias |
| **SC-8 Contexto macro y calendario** | Macro y flujos como datos estructurados, usados por B, C y F. El calendario de eventos (bancos centrales, resultados) pasa al Bloque K y las noticias se leen en SC-11. `[RATIFICADO]` (D-33) Incluye el **vigía de régimen económico** (abajo) |
| **SC-9 Fiscalidad y costes** | Reglas fiscales **codificadas y validadas por un asesor**, no generadas por un LLM; costes de transacción y mantenimiento |
| **SC-10 Adaptadores y simulador** | Puertos independientes del proveedor para intermediario, datos, avisos `[RATIFICADO]` (D-41) **y modelos de IA**; perfil de capacidades de cada proveedor; **simulador propio** de mercado y órdenes para L0 |
| SC-11 Lectura aislada de noticias | Lee noticias y contenido externo en entorno aislado, sin acceso a cartera, credenciales ni herramientas. Salida con esquema cerrado (listas cerradas, números con fuente y fecha), sin texto libre hacia otros bloques. **Versión mínima en la Fase 1** (pocas fuentes fiables; salida: evento, país, gravedad, divisas y activos afectados) que alimenta el registro de riesgos geopolíticos; la completa, en la Fase 5 |

**Vigía de régimen económico.** `[RATIFICADO]` (D-33) Un semáforo por región (normal, tensión, crisis) a partir de indicadores adelantados **calculados con código** (curva de tipos, diferenciales de crédito, tensión bancaria, apalancamiento, volatilidad, PMI). **El estado lo fija el código** con los umbrales del operador `[ABIERTO]` (P-31), y es el único que usan F y los parámetros contextuales (§10). Un agente lo explica y puede proponer subir de estado, pero esa propuesta solo vale si la aprueba el operador (P2, P15). Alimenta el registro de riesgos geopolíticos. **Solo endurece**: reduce la exposición, baja los límites o exige más margen; nunca relaja nada. Como endurecer también puede impedir invertir, el estado del semáforo aparece en el embudo y en la alarma de sequía (§7). No promete predecir crisis. Si la experiencia lo justifica, se promueve a bloque por el criterio del §2.

**Adaptadores.** `[RATIFICADO]` (D-08) Ningún bloque conoce a un intermediario, proveedor de datos o modelo de IA concretos: hablan con un puerto de SC-10. Así se puede diseñar y probar todo contra el simulador y cambiar de proveedor sin reabrir los bloques. El operador rellena una **ficha de restricciones reales** (intermediario, tipos de cuenta, API, datos y licencias, presupuesto, jurisdicción fiscal); hasta entonces solo G y SC-2 quedan bloqueados.

**Registros comunes.** `[RATIFICADO]` (D-23) Almacenes que cualquier bloque consulta antes de investigar por su cuenta, con procedencia, fecha y consulta «punto en el tiempo». Nadie investiga dos veces lo mismo.

| Registro | Qué guarda | Lo alimenta | Lo consultan |
| --- | --- | --- | --- |
| Análisis vigentes | Cada análisis hecho, con su sello de datos y su caducidad | C, verificación, D | Orquestador, A, B y C antes de encargar |
| Riesgos geopolíticos | Focos activos: evento, país, gravedad, activos y divisas afectados | SC-11 | B, C, D, E y H |
| Tendencias tecnológicas | Tecnología, fase de adopción, hitos medibles, sectores y activos | Radar de A | A, B y C |
| Posicionamiento | COT, 13F, participaciones significativas, operaciones de directivos | K (sin LLM) | B (dimensión D10) y C |

El posicionamiento de grandes inversores se usa como contexto y para detectar excesos, nunca para copiar; sus señales pasan por SC-4 antes de pesar en una decisión. Si un foco geopolítico nuevo o agravado afecta a una posición abierta, H propone revisarla (nunca vende por ello, §4.2).

**Verificación diversa.** `[RATIFICADO]` (D-43) Los agentes del mismo modelo comparten sesgos y evidencia, así que su acuerdo no es verificación independiente. El control real es F (§8). Sobre eso:

1. **Primero, comprobaciones deterministas:** coherencia entre fuentes, unidades, precio frente al del intermediario, caducidad.
2. **Contradictor:** agente que recibe la evidencia pero no el razonamiento del analista y construye los escenarios en que la tesis falla. Siempre que sea posible, de **otro modelo o proveedor**. Su informe forma parte del expediente.
3. **Varios análisis independientes** `[RATIFICADO]` (D-35), que generaliza el doble análisis: en las decisiones de mayor importe (nivel N3) siempre, y en las demás cuando lo justifique lo que está en juego, dos o más análisis hechos por agentes y, si es posible, modelos distintos, sin ver el trabajo de los otros. Su **desacuerdo cuenta como incertidumbre**: si discrepan, baja el tope de confianza (§9) o se escala al operador. Se combinan con los pesos de su historial (§9).
4. **Muestreo humano:** el operador revisa de forma periódica una muestra de expedientes completos.

**Lectores de contenido externo.** Los agentes que leen web, PDF o correos trabajan en un **entorno aislado**, sin acceso a cartera, credenciales ni herramientas de acción. Su salida tiene un esquema estricto (listas cerradas, números con fuente y fecha). Nada de lo que escriben llega a E, F o G sin pasar por ese esquema.

## 4. Dos ciclos: oportunidad y posición

Una **oportunidad** (la idea hasta la decisión) y una **posición** (lo que ya se ha comprado) son objetos distintos, con estados y reglas distintos. En la V0.1 iban mezclados y una posición abierta podía volver a «analizarse» como si fuera nueva. Los gestiona la máquina de estados del Orquestador, no un LLM. `[RATIFICADO]` (D-31) Las aportaciones mensuales tienen además un ciclo propio, que no crea oportunidades sino un plan de reequilibrio (§7).

### 4.1 Expediente de oportunidad

`correlation_id` identifica la **petición o caso** (un encargo del Broker); `expediente_id` identifica **un candidato**. Como B devuelve varios candidatos, una petición genera varios expedientes bajo el mismo `correlation_id`.

| Campo | Significado |
| --- | --- |
| `expediente_id`, `correlation_id` | Un candidato y el caso al que pertenece |
| `via_entrada` | `DISCRECIONAL` (A→B→C), `SISTEMATICA` (J, §4.3) o `[RATIFICADO]` `DIRECTA` (el Broker entra por C, D o E, §2) |
| `cartera_destino` | `TRADING`, `TACTICA` o `LARGO_PLAZO` |
| `tipo_activo`, `horizonte`, `fecha_corte` | Código del tipo, horizonte de la tesis y fecha de corte de los datos |
| `condiciones_entrada` | Precio o nivel límite y ventana temporal en que la propuesta sigue siendo válida |
| `condiciones_salida` | Stop, objetivo, fecha e invalidez medible, con su valor numérico |
| `secciones` | Una por bloque que ha intervenido, versionada, inmutable y con `valid_until` |
| `estado`, `historial` | Estado actual y cada transición (quién, cuándo, por qué, con qué versión de reglas) |

**Estados:** `DETECTADA` → `EN_ANÁLISIS` → `VALIDADA` → `COMPARADA` → `PROPUESTA` → `AUTORIZADA` → `EJECUTADA` (nace una posición). Desde casi cualquier estado: `EN_OBSERVACIÓN` (con condiciones de reapertura), `CADUCADA` (venció `valid_until` o la ventana de entrada) o `DESCARTADA` (con motivo).

**Reglas.**

1. Un bloque solo añade **su propia** sección; una corrección es una versión nueva.
2. Solo el Orquestador cambia el estado, y solo por transiciones permitidas.
3. **D exige una fecha de corte común.** Si los análisis comparados difieren en más del umbral de la configuración, el Orquestador pide actualizar los datos antes de comparar.
4. Una propuesta caducada no se ejecuta: vuelve a `EN_ANÁLISIS` o pasa a `DESCARTADA`, y decide el Broker.
5. Las opciones descartadas o en observación conservan su motivo y sus condiciones de reapertura en SC-4.
6. `[RATIFICADO]` (D-28) Con vía `DIRECTA`, el expediente **nace en el estado que corresponde al bloque de entrada** (`EN_ANÁLISIS` si se entra por C, `VALIDADA` si se entra por D con sobres vigentes, `COMPARADA` si se entra por E) y conserva las mismas transiciones hacia delante. Con un candidato único, el Orquestador registra como comparación la que hay frente al benchmark de la cartera (P5) y el motivo de no comparar con más. Una **consulta** no abre expediente: deja su rastro en SC-5 y, si después se decide invertir, abre uno con vía `DIRECTA` reutilizando los análisis vigentes.
7. `[RATIFICADO]` (D-35) Toda tesis de una sección de C lleva **probabilidad, plazo y criterio de resolución**, y se congela en SC-4 antes de conocerse el resultado (§9).

### 4.2 Posición

Nace cuando una orden vinculada a un expediente se concilia. Tiene `posicion_id`, expediente de origen, cartera, cantidad realmente ejecutada, condiciones de salida y órdenes de protección activas.

**Estados:** `ABIERTA` → `EN_REVISIÓN` (H pide revaluar o caducó la tesis) → `ABIERTA` (confirmada) / `REDUCIENDO` / `CERRANDO` → `CERRADA` (conciliada).

1. **Una posición en revisión sigue vigente**, con sus órdenes de protección. No vuelve a ser una oportunidad.
2. **Las reducciones y cierres automáticos solo se disparan por condiciones numéricas declaradas de antemano** (precio, pérdida, límite, fecha). Una invalidez cualitativa o una noticia hace que H **proponga**, nunca que venda.
3. Con ejecución parcial, la posición nace con la cantidad ejecutada; el resto se cancela o continúa según la orden, y E recalcula.
4. La `cartera_destino` de una posición abierta no cambia por sí sola. Reclasificarla exige aprobación del operador y registro, por su impacto fiscal.
5. Un mismo activo en dos carteras son dos posiciones.

**Estados de una orden** (los gestiona G): `BORRADOR` → `VALIDADA` → `AUTORIZADA` → `ENVIADA` → `PARCIAL` / `EJECUTADA` / `RECHAZADA` / `CANCELADA` → `CONCILIADA`. Una orden enviada no cuenta como ejecutada hasta que existe confirmación verificable del intermediario.

### 4.3 Ruta determinista (vía sistemática)

Una estrategia en estado `ACTIVA` (§7) sigue **J → E (dimensionamiento por regla) → F → G** sin ningún LLM en el camino. El Broker y el gestor solo reciben información. Requisitos: parámetros congelados, instrumentos del **registro de universo admitido** (comprobado de antemano contra invertibilidad y liquidez) y presupuesto propio de la estrategia.

En esta ruta no se abre un expediente completo por operación. Se registra una **señal** (`senal_id`, estrategia, versión, hash de parámetros, decisión y orden) enlazada a la posición resultante.

## 5. Contratos entre bloques

Los contratos son la arquitectura: un bloque es sustituible mientras cumpla los suyos. Los esquemas JSON se validan mecánicamente (SC-6). Los contratos existentes entre A y B (`CT-B-01…CT-B-29`) siguen vigentes; los nuevos usan el prefijo `CT-G-`.

**Sobre de mensaje (obligatorio en todo contrato).**

| Campo | Contenido |
| --- | --- |
| `event_id`, `correlation_id`, `expediente_id` | Identificación del mensaje, del caso y del candidato |
| `producer`, `consumer` | Bloque emisor y destinatario |
| `tipo_mensaje`, `version_esquema` | Qué es y con qué versión del esquema se validó |
| `emitido_en`, `valid_until` | Cuándo se generó y hasta cuándo vale |
| `data_refs` | Referencias a evidencia (SC-2) y artefactos del Motor (SC-3) |
| `payload` | Contenido tipado, con unidades y divisa explícitas |
| `confianza`, `incertidumbre` | Con su tope y sus limitaciones conocidas |
| `resultado_politica` | Controles aplicados, resultado, motivo y versión de política |

**Catálogo de contratos globales.** `[RATIFICADO]` (D-43)

| ID | Contrato | De → a |
| --- | --- | --- |
| CT-G-01 | Encargo de análisis en profundidad (pregunta, decisión que informa, nivel N0–N3, plazo y presupuesto, restricciones del mandato, fecha de corte, paquete de B) | Broker/gestor → C |
| CT-G-02 | **Sobre común de valoración** (abajo) | C → verificación, D, Broker |
| CT-G-03 | Informe del Contradictor | Contradictor → D, Broker |
| CT-G-04 | Petición de comparación | Broker/gestor → D |
| CT-G-05 | Comparativa (ranking por mandato, dominancia, sensibilidad, coste de oportunidad) | D → Broker/gestor |
| CT-G-06 | Propuesta de inversión con condiciones de entrada y salida | Broker/gestor → E |
| CT-G-07 | Plan de cartera por libro | E → F |
| CT-G-08 | Resultado de control (aprobado, reducido o vetado, con motivo) | F → G, Broker |
| CT-G-09 | Orden, con órdenes de protección asociadas | E/F → G |
| CT-G-10 | Alerta o petición de revisión de posición | H → Broker/gestor |
| CT-G-11 | Consulta al Broker o al operador (generaliza `CT-B-28`) | Cualquiera → Broker |
| CT-G-12 | Seguimiento de encargo (generaliza `CT-B-29`) | Bloque → Orquestador |
| CT-G-13 | Propuesta de cambio y veredicto de validación | I → J → operador |
| CT-G-14 | **Registro de ejecución manual** (lo que el operador hizo fuera del sistema) | Operador → G |
| CT-G-15 | Estrategia validada y universo admitido | J → E, F |
| CT-G-16 | Aviso al operador (canal, prioridad, acuse de recibo) | Orquestador → operador |
| CT-G-17 | `[RATIFICADO]` (D-41) **Ficha de bloque** (manifiesto): contratos que recibe y entrega con sus versiones, capacidades, modos de fallo y estado | Bloque → Orquestador |

**Enchufabilidad.** `[RATIFICADO]` (D-41) Flexibilidad donde las cosas cambian (perfiles, agentes, modelos de IA, proveedores, estrategias) y rigidez donde se protege el dinero: el control (Orquestador, F, G y kill-switch) sigue centralizado a propósito.

1. **Ficha y registro.** Cada bloque publica su ficha (CT-G-17) y el Orquestador mantiene el registro de bloques: solo encarga trabajo a un bloque registrado, en una versión de contrato que ambos declaran.
2. **Batería de conformidad.** Cada contrato tiene una batería de casos (válidos e inválidos) que un bloque debe pasar para conectarse o sustituir a otro. Ningún contrato queda sin esquema: los que aún no lo tienen (CT-G-07, 11, 12, 13 y 15) lo reciben antes de que su bloque se construya.
3. **Estado por bloque.** Cada bloque guarda su propio estado, con su versión de esquema y sus migraciones, de modo que cambiar uno no obliga a migrar los demás. El código de referencia de la Fase 1, que hoy guarda un único estado, se separa al empezar la Fase 2.
4. **Adaptadores para A y B.** A y B hablan sus contratos `CT-B`; un adaptador los traduce a `CT-G` hasta su refactorización en la Fase 2.
5. **Adaptadores externos** (SC-10) con interfaz común para datos, intermediarios y modelos de IA.

### Sobre común de valoración (CT-G-02), por capas

Hace comparables los doce perfiles de C sin obligar a nadie a inventar lo que no se puede medir. `[RATIFICADO]` (D-12)

**Capa 1 · obligatoria y medible.**

| Bloque | Contenido |
| --- | --- |
| Identificación | Tipo de activo, instrumento y vía de acceso, dirección, cartera compatible, nivel de análisis, fecha de corte |
| Tesis | Resumen, supuestos, **clase de referencia** (qué suele pasar en casos parecidos, con qué frecuencia y en cuánto tiempo, y por qué este caso sería distinto; el Contradictor la revisa) y **condiciones de invalidez medibles** (valor numérico); `[RATIFICADO]` (D-35) **probabilidad, plazo y criterio de resolución** de la tesis |
| Entrada y salida | Condiciones de entrada, stop, objetivo y fecha |
| Liquidez y salida | Tiempo y coste de salida, tamaño máximo sin impacto apreciable |
| Costes | Entrada, mantenimiento (financiación, swaps, margen) y salida; impacto fiscal (SC-9) |
| Capital | Capital necesario, margen y apalancamiento |
| Estrés histórico | Pérdida en un **conjunto estándar de episodios históricos**, calculada por el Motor, no opinada |
| Factores | Exposición a un conjunto común (tipos, renta variable, USD, crédito, inflación, materias primas, volatilidad, liquidez) **por regresión histórica**, con ventana y calidad del ajuste |
| Evidencia | Frescura y proporción de cifras `VERIFICADO`, `ESTIMADO` y `SUPUESTO` |
| Exclusiones duras | Sanciones, invertibilidad y acceso |
| Referencias | Cuerpo especializado y artefactos del Motor |

**Capa 2 · condicional: escenarios y distribuciones.** Escenarios con probabilidad y rentabilidad neta a un horizonte común, y su distribución resumida. Solo se rellena si el C declara el **método** y la **base de datos** que la sustentan. Si no, el campo vale `NO_ESTIMABLE` o va etiquetado `SUPUESTO`, y D lo trata como opinión, no como dato.

**Capa 3 · confianza.** Un **tope de confianza fijado ex ante** por clase de comparabilidad (abajo), rebajado si los análisis independientes discrepan (§3). La calibración histórica solo entra cuando hay muestra suficiente (§9).

**Clases de comparabilidad.** Cada perfil de C declara la suya y la ratifica el operador. `[RATIFICADO]` (D-12) el sistema de tres clases; la clase de cada tipo de activo sigue pendiente (P-15).

| Clase | Criterio | Ejemplos orientativos |
| --- | --- | --- |
| **Q** cuantitativa | Historia suficiente y modelo defendible | Divisas líquidas, índices, renta variable líquida, fondos cotizados |
| **S** semicuantitativa | Historia parcial o supuestos fuertes | Renta fija corporativa, inmobiliario cotizado, derivados |
| **K** cualitativa | Sin base fiable para probabilidades | Criptoactivos, capital privado y alternativos, activos ilíquidos |

**Reglas de comparabilidad.**

1. D usa una puntuación única **solo dentro de la misma clase**. Entre clases compara por dominancia, estrés, liquidez, coste y arrepentimiento máximo, sin valor esperado, y lo declara en la comparativa.
2. Mismas unidades, divisa base EUR, mismo conjunto de episodios de estrés y misma fecha de corte (§4.1).
3. La confianza de un C nunca se compara en bruto: se compara con su tope.
4. Toda cifra va por ID del Motor y declara su modelo (P3).

**Congelación diferida.** CT-G-02 es una **versión 0.x estable**: se admiten campos opcionales y cambios compatibles con aviso en el §15. Se congela en `1.0.0` cuando dos perfiles de C muy distintos (por ejemplo `C-DIV` y `C-RV`) lo hayan emitido y D lo haya consumido. Un esquema con versión desconocida se rechaza, no se interpreta.

## 6. Autonomía, aprobaciones y controles sobre el operador

La autonomía se concede por **cartera × tipo de acción × tamaño** y la aplica el plano de control. `[RATIFICADO]` los tres modos (manual, semiautónomo y autónomo) y, desde el 9-11-2026, el detalle (D-15); los umbrales siguen pendientes.

| Nivel | Modo | Qué puede hacer el robot | Qué exige al operador |
| --- | --- | --- | --- |
| **L0** | Simulación | Todo el flujo con órdenes simuladas en el simulador propio (SC-10) | Nada; sirve para validar |
| **L1** | Manual (asesor) | Analiza, compara, propone y prepara la orden completa | Ejecutarla él y **registrarla** (CT-G-14), o aprobar cada orden |
| **L2** | Semiautónomo | Actúa solo en las acciones permitidas de la tabla siguiente | Aprobar lo que queda fuera del umbral |
| **L3** | Autónomo | Envía órdenes por G dentro del mandato y los límites, sin aprobación previa | Supervisar con avisos y revisión periódica |

**Matriz de autonomía.** Punto de partida: las tres carteras en **L1** (y L0 mientras no exista intermediario). `[RATIFICADO]` (D-45) Es el valor por defecto de cualquier copia nueva.

| Tipo de acción | En L2 (semiautónomo) |
| --- | --- |
| Análisis, consultas, informes, avisos | Automático |
| Reducir o cerrar por una **condición numérica declarada de antemano** (stop, límite de pérdida, fecha) | Automático; el stop vive en el intermediario (§8) |
| Reducir o cerrar por **invalidez cualitativa o noticia** | H propone; **aprueba el operador** |
| Abrir o aumentar dentro del umbral, en instrumento admitido, sin apalancamiento y dentro de las condiciones de entrada | Automático si F aprueba |
| Abrir o aumentar por encima del umbral, o en un instrumento nuevo | **Aprobación del operador** |
| Apalancamiento, derivados y CFD | **No habilitados.** Los habilita el operador de forma explícita, con su límite, no antes de la Fase 3 (§14) |
| Cambio de estrategia, modelo, límite o parámetro | **Aprobación del operador**, tras validación de J |
| Movimientos de efectivo o entre carteras | **Aprobación del operador** |
| Cualquier acción con datos obsoletos, discrepancia sin explicar o control degradado | **Prohibida**; se escala |

Los umbrales viven en la configuración y los fija el operador `[ABIERTO]`. La asimetría es deliberada: reducir riesgo con una regla numérica exige menos permiso que aumentarlo.

**L3 solo en horario supervisado.** Fuera del horario que el operador defina `[ABIERTO]`, la cartera opera como máximo en L2 y solo actúan los stops nativos del intermediario.

**Cola de aprobaciones.**

1. La pantalla muestra **las cifras calculadas por F y el resultado del control**, no el texto redactado por un LLM. El operador confirma el importe tecleándolo.
2. Una aprobación vale solo para esa acción con esas cifras y no se reutiliza.
3. Si caduca sin respuesta, la acción por defecto es **no actuar**.
4. Las acciones que aumentan riesgo exigen segundo factor y un canal distinto del chat de trabajo.

**Controles sobre el operador.** El operador es la última compuerta y también puede equivocarse, estar cansado o reaccionar a una pérdida. `[RATIFICADO]` (D-15)

1. **Espera obligatoria** (enfriamiento) antes de aprobar acciones que aumentan riesgo cuando se dan condiciones configuradas (por ejemplo, tras una pérdida diaria o fuera de horario).
2. **Límite mensual de anulaciones de veto**, siempre con motivo registrado.
3. **Los límites de pérdida no se pueden subir el mismo día** en que se alcanzaron.
4. **Operaciones manuales declaradas:** todo lo que el operador haga fuera del sistema se declara (CT-G-14). Lo no declarado es una discrepancia.
5. **Revisión periódica** de los mandatos y de una muestra de expedientes (§3). `[RATIFICADO]` (D-32) Una vez al año, una **revisión guiada con el Broker**: perfil y situación, colchón de emergencia, aportaciones, rentabilidad mínima exigida, camino de riesgo, resultado frente a la cartera sombra y lo que el robot propone cambiar. Cada cambio sigue su ruta normal.
6. **Modo hibernación** `[RATIFICADO]` (D-32). Si el operador no responde a los avisos durante un plazo `[ABIERTO]` (P-30): no se abren posiciones nuevas ni se aumentan las existentes, se mantienen las órdenes de protección y las reglas numéricas de salida, las aportaciones que lleguen se quedan en efectivo o en el monetario del mandato sin generar órdenes, y se avisa a una **persona de confianza** designada por el operador `[ABIERTO]` (P-30), que nunca opera. Si además puede consultar la cartera o solo recibe el aviso lo decide el operador (P-30). Se sale de la hibernación cuando el operador vuelve y lo confirma con segundo factor.

**Perfil inversor y riesgo.** `[RATIFICADO]` El perfil inversor (§2) orienta los mandatos. Puede **bajar** el riesgo de una cartera al momento; para **subirlo** hace falta la confirmación del operador con segundo factor y un periodo de espera, como el límite de pérdida y el nivel de autonomía.

**Promoción y degradación.** Subir de nivel exige un periodo mínimo en el nivel actual con conciliación limpia, cero incumplimientos de límites y funcionamiento estable `[ABIERTO: criterios y duración]`. Bajar es **automático e inmediato** ante discrepancia sin explicar, datos obsoletos, pérdida de conexión, cortacircuito o incidente de seguridad: la cartera pasa a L1 hasta que el operador la rehabilite.

## 7. Carteras, mandatos y ciclo de vida de estrategias

Hay **tres carteras** (libros) con capital propio, cada una con su mandato. `[RATIFICADO]` las tres y que el trading opera en **días y semanas** por ahora; `[RATIFICADO]` (D-43) también el resto de la tabla; sus valores concretos siguen pendientes (P-03, P-04).

|  | TRADING | TÁCTICA | LARGO PLAZO |
| --- | --- | --- | --- |
| Horizonte | Días a semanas | Semanas a meses | Meses a años |
| Vía de entrada dominante | Sistemática (J), ruta determinista | Ambas | Discrecional (A→B→C→D) |
| Qué se decide | Estrategias validadas y su asignación de capital | Posiciones con tesis y catalizador | Asignación patrimonial y rebalanceos |
| Peso del análisis profundo de C | Bajo | Medio | Alto |
| Peso de la fiscalidad (SC-9) | Bajo | Medio | Alto |
| Presupuesto de riesgo | Estricto y pequeño por operación | Intermedio | Definido por objetivo patrimonial |

**Mandato de cada cartera** (vive en SC-1, no en los prompts). Define como mínimo: objetivo, horizonte, **benchmark** (la alternativa «no hacer nada» de esa cartera: un índice o una cesta en la que **se invierte de verdad** cuando no hay nada mejor; efectivo solo si el operador lo fija así), presupuesto de riesgo, límites de concentración (activo, emisor, divisa, sector, tipo), liquidez mínima, apalancamiento permitido (inicialmente cero), tipos de activo admitidos, regla de rebalanceo, criterio de salida y nivel de autonomía. Los valores concretos son del operador `[ABIERTO]`.

**Contrapesos de la abstención.** `[RATIFICADO]` (D-22) Para que el control no impida invertir nunca:

1. **Embudo visible.** N muestra cada semana cuántas oportunidades entran, en qué capa cae cada una y por qué.
2. **Alarma de sequía.** Si en un plazo `[RATIFICADO: 60 días]` (P-17) ninguna oportunidad llega a invertirse habiendo candidatos que pasaron el análisis, se avisa al operador con el embudo del periodo.
3. **Seguimiento de lo descartado** (§9): I calcula cómo habrían ido las opciones vetadas o descartadas y propone recalibrar los filtros que descartan de más.

Los controles **nunca se relajan solos**: el sistema propone el ajuste y el operador decide, por la ruta de cambios del §9.

**Freno a la rotación.** `[RATIFICADO]` (D-25) D y E solo proponen cambiar una posición por otra si la mejora esperada supera los costes de salir y entrar (comisiones, diferencial, impuestos) con un margen `[RATIFICADO: el doble de esos costes]` (P-20). Y usan SC-9 al decidir: compensar ganancias con pérdidas cuando convenga, la regla de los dos meses y el efecto del plazo de tenencia.

**Rentabilidad mínima exigida.** `[RATIFICADO]` (D-30) Cada cartera tiene una rentabilidad anual mínima **exigida, no garantizada**, en términos reales (después de inflación), fijada por el operador `[ABIERTO]` (P-25).

1. Una inversión solo se propone si supera ese mínimo **después de costes e impuestos** con una probabilidad suficiente `[ABIERTO]` (P-25). El mínimo es anual y se prorratea al horizonte de cada operación. De dónde sale la comprobación según la vía:
   - **discrecional y directa:** la calcula el Motor a partir de la capa 2 del sobre. Si C devuelve `NO_ESTIMABLE`, la inversión no pasa en L2 ni en L3 (T-58 decía «en autónomo»; se extiende a L2 por prudencia); en L1 el operador la ve marcada como no comprobada;
   - **sistemática:** se comprueba una vez, al validar la estrategia (CT-G-15), con su rentabilidad neta esperada; no orden a orden;
   - **reequilibrio hacia los pesos del mandato con las aportaciones e inversión en el benchmark (P5):** exentos, porque son el propio plan, que ya se contrastó con el mínimo en sus proyecciones (§9).
2. El Broker comprueba que el mínimo es **compatible con el riesgo tolerado** del perfil: si para alcanzarlo hiciera falta más riesgo del aceptado, lo dice con cifras y el operador elige qué cambia.
3. **Prohibido aumentar el riesgo para recuperar** una rentabilidad por debajo del mínimo.
4. Si el operador quiere un **suelo**, una parte de la cartera se asegura en renta fija sin riesgo de crédito a su plazo `[ABIERTO]` (P-35).
5. El seguimiento es anual, en la revisión guiada (§6).

**Plan de largo plazo.** `[RATIFICADO]` (D-31)

1. **Aportaciones mensuales como ciclo propio.** Cada aportación del operador (importe `[ABIERTO]`, P-26) entra por su propio ciclo en el Orquestador y se usa para **reequilibrar comprando lo que está por debajo de su peso**, antes que vendiendo lo que está por encima, lo que ahorra costes e impuestos. El ciclo genera un plan de reequilibrio de E que pasa por F y G (P20) con el mismo nivel de autonomía que cualquier compra (§6).
2. **Vehículo fiscal en la decisión.** D y E comparan también el vehículo: en España, los traspasos entre fondos no tributan y los ETF y las acciones sí al vender. Las reglas las codifica SC-9 y las valida un asesor (P-06); los vehículos que se usen los decide el operador `[ABIERTO]` (P-28).
3. **Camino de riesgo** (*glide path*). La cartera de largo plazo reduce su riesgo de forma gradual al acercarse la fecha de cada objetivo del operador `[ABIERTO]` (P-27), según una senda fijada en el mandato y no por decisión del momento.
4. **Proyecciones del plan** con el Motor (§9): hacia dónde va el plan con estas aportaciones y este riesgo, siempre en bandas.

**Supervisión global (en E).**

1. Los **límites globales prevalecen** sobre los de cada cartera.
2. Detecta **conflictos entre libros** (un corto táctico frente a una posición larga de largo plazo en el mismo activo) y concentraciones que cada libro por separado no ve.
3. Reparte y vigila el efectivo. El **reparto de capital entre carteras lo aprueba el operador**; E solo lo propone.
4. **Concentración mínima antes de M** `[RATIFICADO]` (D-25): hasta la Fase 3, E comprueba que no se acumulen apuestas que dependen del mismo factor (por ejemplo, varias divisas que en el fondo dependen del dólar). F calcula su propia versión de forma independiente.

**Ciclo de vida de una estrategia (J).** `[RATIFICADO]` (D-43)

`CANDIDATA` → `EN_PAPER` (L0) → `ACTIVA` (capital pequeño) → `ACTIVA_PLENA` → `PAUSADA` / `RETIRADA`

1. Pasar de `CANDIDATA` a `EN_PAPER` exige un backtest sin *look-ahead*, con costes realistas y datos fuera de muestra.
2. Pasar de `EN_PAPER` a `ACTIVA` exige un periodo mínimo de paper trading con resultados dentro del rango del backtest y la aprobación del operador.
3. Cada estrategia tiene su **asignación de capital**, su **cortacircuitos propio** y su **registro de universo admitido** (instrumentos ya comprobados contra invertibilidad y liquidez).
4. **Detección de deriva:** H compara el rendimiento real con el del backtest; si sale del rango definido, la estrategia pasa a `PAUSADA` automáticamente y se avisa al operador.

**Escalera de verificación.** `[RATIFICADO]` (D-39) Generaliza el ciclo de vida anterior a todo lo que cambie cómo decide el sistema: estrategias, modelos, instrucciones y agentes. Nada sube un peldaño sin superar el anterior, y la duración de cada uno la fija el operador `[ABIERTO]` (P-33).

| Peldaño | Qué es | Su trampa |
| --- | --- | --- |
| 1 · Backtesting | Prueba con datos históricos, costes reales y sin sesgo de supervivencia | Los agentes de IA ya conocen el pasado: con ellos solo vale con casos anonimizados o datos posteriores a su fecha de corte |
| 2 · Paper trading | Simulación en tiempo real, con cada decisión registrada antes del resultado | No mide deslizamientos, órdenes rechazadas ni horarios |
| 3 · Dinero real en pequeño | Una fracción mínima del capital durante un periodo | Muestra pequeña: detecta problemas, no demuestra resultados |
| 4 · Escala por tramos | Más capital por pasos | Solo si los peldaños anteriores siguen en verde |

**Verificaciones externas** `[RATIFICADO]` (D-39), en todos los peldaños: comparación con la cartera sombra después de costes, impuestos e inflación; conciliación con el intermediario; repetición con un segundo proveedor de datos; **prerregistro sellado** de la hipótesis y del criterio de éxito antes de la prueba; torneos públicos de pronósticos para medir la calibración de los agentes; revisión independiente por quien no participó; y pruebas de fallo (datos cortados, precios retrasados o absurdos).

## 8. Control, límites nominales, órdenes de protección y kill-switch

El Bloque F es código determinista que ningún agente puede modificar, saltarse o convencer. Su resultado es `APROBADO`, `REDUCIDO` (con el tamaño permitido) o `VETADO`, con motivo y versión de política. `[RATIFICADO]` (D-14)

**F no depende de los modelos del sistema.** Una referencia mala no puede aprobarse a sí misma, así que F se apoya en dos cosas que no vienen de los agentes:

1. **Una segunda fuente:** precios, posiciones y saldos del propio intermediario (SC-2).
2. **Límites nominales duros**, expresados en euros y en número de órdenes, sin betas ni correlaciones: importe máximo por orden, por día y por activo, pérdida máxima diaria y semanal por cartera y global, apalancamiento y margen agregados máximos, y número máximo de órdenes por hora. Los valores los fija el operador `[ABIERTO]`.

**Controles previos** a toda acción material:

1. Mandato: tipo de activo admitido, horizonte, apalancamiento.
2. Límites de concentración por libro y **globales**, incluida la exposición compartida a una divisa, emisor o factor. Las betas son una ayuda, no el límite: en crisis fallan.
3. Liquidez del instrumento y liquidez mínima de la cartera: no comprar más de una fracción del volumen medio diario `[RATIFICADO: 5 %]` (P-22) y contar el coste de entrar y salir (D-26).
4. Exclusiones duras: sanciones, invertibilidad minorista (ESMA y normativa aplicable), acceso y custodia.
5. Calidad de la evidencia: sobre válido, no caducado, fecha de corte reciente y proporción mínima de cifras verificadas.
6. Cordura de la orden: tamaño, **deriva del precio frente a la referencia del análisis** y condiciones de entrada, duplicados (idempotencia).
7. **Ventanas de restricción** por eventos del calendario de SC-8 (decisiones de bancos centrales, resultados) y fines de semana para los instrumentos con riesgo de hueco.
8. Costes totales, incluida la financiación en divisas y el margen.
9. Autonomía: el nivel de la cartera permite la acción (§6).
10. `[RATIFICADO]` (D-33) **Régimen:** si el estado del vigía de régimen (§3), fijado por código, es tensión o crisis en la región del activo, se aplican los límites endurecidos de ese estado. F no usa la interpretación de ningún agente, y el vigía nunca relaja un límite.
11. `[RATIFICADO]` (D-30) **Rentabilidad mínima:** en L2 y L3, una apertura o un aumento por la vía discrecional o directa llevan la comprobación del Motor de que superan la rentabilidad mínima exigida (§7); si falta o es `NO_ESTIMABLE`, se veta. En la vía sistemática basta la de la validación de la estrategia, y el reequilibrio hacia los pesos del mandato y la inversión en el benchmark están exentos (§7). F comprueba que la cifra existe y es del Motor; no la calcula ni la opina.

**Controles posteriores.** Seguimiento continuo de límites y de pérdida acumulada. Los **cortacircuitos** son automáticos y llevan la cartera a L1.

**Órdenes de protección.** Todo stop y toda condición de salida numérica se coloca como **orden nativa en el intermediario** siempre que este lo permita. Así siguen vigentes aunque el sistema falle. Si el intermediario no ofrece la orden nativa, la posición se limita a un tamaño que el operador pueda gestionar a mano.

**Independencia.**

1. F recibe cifras y referencias, no el razonamiento persuasivo del plan.
2. El Broker no puede anular un veto. Solo el operador, con registro y motivo, con el límite mensual del §6 y no desde un mensaje no autenticado.
3. Cambiar una regla de F exige validación de J y aprobación del operador, y crea una versión nueva.

**Conciliación y tolerancias.** Diferencias esperables (dividendos, comisiones, redondeos, diferencias de cambio) se clasifican como **diferencia explicada** dentro de unas tolerancias configuradas; no disparan nada. Una diferencia **sin explicar** o fuera de tolerancia es una discrepancia. Las operaciones manuales declaradas (CT-G-14) no cuentan como discrepancia.

**Kill-switch.** Interruptor manual del operador y automático ante los desencadenantes del §11.

1. **Cancela las órdenes de entrada pendientes y bloquea las nuevas.** **No cancela las órdenes de protección** ni liquida posiciones salvo mandato expreso del operador, porque liquidar a ciegas también es un riesgo.
2. Pasa todas las carteras a L1 y avisa al operador por un canal fuera del chat, con acuse de recibo (CT-G-16).
3. La rehabilitación es siempre manual y sigue la lista de comprobación del §11.

**Vigilante con latido.** Un proceso independiente comprueba cada pocos segundos que el plano de control emite latido. Si deja de hacerlo, el vigilante avisa al operador y bloquea las órdenes de entrada; las órdenes de protección ya colocadas siguen en el intermediario. El kill-switch no es así un punto único de fallo.

## 9. Memoria y aprendizaje realista

Con unas pocas decenas de tesis al año y horizontes de meses, las métricas de calibración no se pueden estimar durante mucho tiempo. El sistema aprende, pero no finge que lo hace más rápido de lo que permiten los datos. `[RATIFICADO]` (D-43)

1. **Diario de pronósticos (SC-4).** Todo pronóstico material se congela antes de conocerse el resultado, con horizonte, condición de resolución y `methodology_version`. También se registran las opciones descartadas con sus condiciones de reapertura. Es un diario fiable, no un oráculo.
2. **Tesis descompuestas.** Toda tesis con horizonte superior a 12 meses se descompone en **sub-pronósticos medibles de 12 meses o menos** (resultados, márgenes, diferenciales, indicadores macro, hitos). Se evalúan antes y dan señal sin esperar al retorno final.
3. **Topes de confianza ex ante.** La confianza máxima la fija la clase de comparabilidad (§5) y es baja para un C sin historial. Solo sube cuando hay **muestra suficiente**, con un mínimo de observaciones fijado en la configuración `[ABIERTO]`. Con menos, el sistema dice «muestra insuficiente» en lugar de concluir.
4. **Calibración agrupada.** Se mide por perfil de C y por clase, no por activo. Las métricas (puntuación de Brier, comparación con referencias ingenuas) se calculan solo con muestra suficiente. D usa el tope, y la calibración cuando existe.
5. **Dónde se aprende de verdad.** En trading y táctica, que generan observaciones, y en la deriva de estrategias (§7). En largo plazo se aprenden **procesos** (calidad de datos, cumplimiento de condiciones de invalidez, hitos), no parámetros.
6. **Ruta única de cambios.** I propone → J valida (backtest sin *look-ahead* y paper trading) → F y el operador aprueban → despliegue con versión nueva → comparación con la anterior. **Una mejora que no se puede validar con muestra suficiente o fuera de muestra no se despliega.** `[RATIFICADO]` (D-38, D-39) Para modelos, instrucciones y agentes, los papeles son: **J entrena** y ejecuta las pruebas de la escalera de verificación (§7); **el veredicto lo da código de I** con la **reserva sellada** de datos para la prueba final, que J no ve; **F y el operador aprueban**.
7. Las opciones descartadas se reevalúan automáticamente cuando se cumplen sus condiciones de reapertura.
8. **Seguimiento de lo descartado** `[RATIFICADO]` (D-22): I calcula cómo habrían ido las opciones vetadas o descartadas para distinguir una abstención acertada de unos filtros demasiado estrictos.
9. **Cartera sombra pasiva** `[RATIFICADO]` (D-22, D-27): desde el primer día corre en simulado un plan pasivo simple (un índice mundial), con los mismos aportes y retiradas que la cartera real. I compara cada mes el robot con la sombra después de costes de análisis (los de los modelos incluidos), comisiones e impuestos, y `[RATIFICADO]` (D-30) también en términos reales, después de inflación. Si tras `[RATIFICADO: 24 meses]` el robot no la supera, propone pasar a gestión pasiva y decide el operador.
10. **Pronósticos del radar tecnológico** en SC-4, con hitos de 12 meses o menos y la clase de referencia de cuánto tardaron tecnologías parecidas en implantarse.
11. **Presupuesto de complejidad** `[RATIFICADO]` (D-25): cada bloque, control o registro justifica con datos lo que aporta (decisiones que cambió, pérdidas que evitó, coste que ahorró). I lo revisa cada `[RATIFICADO: 6 meses]` (P-21) y propone simplificar o retirar lo que no aporta.
12. **Proyecciones del plan** `[RATIFICADO]` (D-29). Un módulo del Motor, no un agente: simulación de Montecarlo del plan a décadas vista con las aportaciones, el riesgo y el horizonte del operador, probabilidad de alcanzar cada objetivo y comparación con la cartera sombra. Siempre en bandas, con los supuestos a la vista y en términos reales.
13. **Probabilidades verificables y torneo de pronósticos** `[RATIFICADO]` (D-35, D-36). Toda tesis lleva probabilidad, plazo y criterio de resolución, y se mide con la puntuación de Brier y su calibración. Un **torneo permanente** de preguntas con fecha de resolución, a las que responden todos los agentes analistas, da muestra mucho antes de que se cierren las inversiones.
14. **Los agentes se ganan su peso** `[RATIFICADO]` (D-36). El peso de cada analista al combinar análisis (§3) sale de su historial verificado, con contracción hacia pesos iguales mientras haya pocos datos. Ningún modelo ni agente recibe peso o autonomía antes de un **mínimo de decisiones resueltas** `[ABIERTO]` (P-32).
15. **Aspirante frente a titular y autopsias** `[RATIFICADO]` (D-36). Todo modelo, instrucción o agente nuevo compite como aspirante contra el que está en uso y solo lo sustituye si lo supera en la escalera de verificación (§7); el anterior se guarda para volver atrás. Cada error relevante tiene su **autopsia** en SC-4: qué falló (dato, modelo, juicio, ejecución o azar) y qué se cambia.
16. **Incentivos por diseño** `[RATIFICADO]` (D-37). A los agentes no se les motiva con trucos en las instrucciones, sino con el sistema: influencia según su puntuación de Brier; más trabajo y presupuesto para el que gana a su aspirante; el Contradictor puntúa por los fallos que encuentra y se confirman; instrucciones que exigen probabilidad, plazo y qué refutaría la tesis, y que ocultan lo que el operador quiere oír. Contra la ley de Goodhart: se premian la calibración y la rentabilidad ajustada al riesgo después de costes, nunca la rentabilidad sola; solo cuentan resultados verificados, puntuados por un juez independiente y con preguntas que el agente no elige; y los límites de F y el kill-switch quedan fuera del alcance de cualquier agente. El aprendizaje por refuerzo solo más adelante y por esta misma ruta.
17. **Entrenamientos** `[RATIFICADO]` (D-38). J ejecuta el catálogo de entrenamientos (régimen, volatilidad, ranking, meta-etiquetado, calibración y agregación de agentes, instrucciones, costes de ejecución, texto, deriva, robustez y asesor de configuración) sobre las bases de datos del §10, con un protocolo común: validación temporal purgada con embargo, reserva sellada, corrección por número de intentos (Sharpe deflactado y probabilidad de sobreajuste), medida en crisis, referencia simple, simulado hacia delante y vigilancia de deriva una vez en uso. J tiene **presupuesto propio** para entrenar y siempre se puede volver a la versión anterior. El **aprendizaje automático y las redes neuronales** entran solo como aspirantes frente a referencias simples (GARCH, factores lineales) y nunca como decisores únicos. Afinar modelos de IA con datos propios, solo para tareas mecánicas y no al principio. Entrenar es sobre todo código determinista y reproducible: la IA propone y el código de I puntúa.
18. **Cambio de modelo de IA** `[RATIFICADO]` (D-40). Un modelo de IA nuevo o una versión nueva de un proveedor solo sustituye al actual después de pasar un **conjunto dorado** de casos resueltos y compararse con el anterior, con el umbral del operador `[ABIERTO]` (P-34).

**Prohibido.** Cambiar límites, estrategias activas, modelos o parámetros de ejecución sin esa ruta; ajustar con el periodo que luego se usa para validar; usar un resultado para recalibrar el pronóstico que lo predijo.

El Bloque I completo se construye al final (§14). Hasta entonces bastan el diario y los informes sencillos, `[RATIFICADO]` más el torneo de pronósticos y la calibración de los agentes desde la Fase 1.

## 10. Datos, modelos, evidencia y reglas sobre cifras

1. **Una sola plataforma de evidencia (SC-2).** Todo dato entra con fuente, fecha de obtención, fecha de vigencia, licencia, hash y etiqueta epistémica: `VERIFICADO`, `ESTIMADO` o `SUPUESTO`. El dato original nunca se sobrescribe; una corrección es un registro nuevo que apunta al anterior.
2. **Punto en el tiempo.** Toda consulta puede pedir los datos tal como se conocían en una fecha, para evitar *look-ahead* y sesgo de supervivencia.
3. **Las cifras las calcula el Motor (SC-3), y cada módulo declara su modelo.** Un agente cita el ID del artefacto. Si no existe un modelo defendible para una cifra, el Motor devuelve `NO_ESTIMABLE`; un LLM no rellena ese hueco con una probabilidad. Una cifra sin modelo ni ID se trata como `SUPUESTO` y el validador la marca.
4. **Los parámetros no se escriben en prompts.** `[RATIFICADO]` (D-45) **Todo parámetro tiene un valor por defecto prudente, válido para cualquier usuario y con su justificación escrita** (en simulado, poca autonomía, sin apalancamiento y límites bajos), de modo que una copia nueva funciona desde el primer día y el cuestionario del asesor (§2) solo la personaliza; cada parámetro nuevo de cualquier bloque llega con su valor por defecto y su pregunta del cuestionario. Umbrales, pesos y límites viven en configuración versionada. `[RATIFICADO]` (D-34) Son **contextuales** en lugar de números fijos: pueden variar por tipo de activo, solidez del activo, régimen del mercado (§3) y horizonte, siempre dentro de una tabla de configuración versionada. Los propone el asesor de configuración del Broker (§2) y los confirma el operador; después de la configuración inicial, cada cambio sigue la ruta única del §9. Los límites duros de F y el kill-switch no los fija un modelo.
5. **Los almacenes grandes se consultan por ID.** Ningún agente carga un almacén entero. Cada fase recibe un kit de contexto cerrado.
6. **Segunda fuente.** Para precios, posiciones y saldos que F utiliza, la referencia independiente es el intermediario (§8).
7. **Convenciones fijas.** Divisa base EUR, zona horaria y calendario de cada mercado explícitos, unidades en cada campo y ajustes corporativos documentados. `[RATIFICADO]` (D-30) Toda rentabilidad que se compara con un objetivo, con la rentabilidad mínima o con la cartera sombra se da **también en términos reales**, con el índice de inflación que fije el operador (propuesto: el IPCA de la zona euro; P-25) y su fuente.
8. **Contenido externo = dato.** Lo leen agentes aislados con salida de esquema estricto (§3, §12). Se cita y se contrasta; no se obedece.
9. **Fiscalidad codificada.** Las reglas fiscales (por ejemplo, la regla de recompra de dos meses, el tratamiento de criptoactivos, las ganancias en divisas y las obligaciones informativas de activos en el extranjero) las codifica y valida un asesor. Un LLM no las genera. Los tratamientos especiales quedan fuera hasta tener regla validada.
10. **Simulador antes que API real.** Todo conector se desarrolla y se prueba contra el simulador de SC-10 antes de conectar el servicio real.
11. **Bases de datos para aprender** `[RATIFICADO]` (D-38). K y SC-4 mantienen un catálogo de bases de datos, todas con **fecha de conocimiento** (cuándo se supo cada dato, no solo a qué fecha se refiere) y **procedencia**. Del mundo: mercado sin sesgo de supervivencia, fundamentales con fecha de publicación, macro con sus revisiones, eventos, texto con hora exacta, posicionamiento, composición histórica de índices y episodios de estrés. Del propio robot: diario de decisiones, banco de pronósticos, casos anonimizados, etiquetas, ejecuciones, **registro de experimentos con el número de intentos**, coste de la IA y perfil del operador. El detalle (BD-01 a BD-16) está en el documento de trabajo «Cómo decide el Robot Investor y cómo lo entrenaríamos» enlazado en T-58.
12. **Historial exportable** `[RATIFICADO]` (D-40). Todo lo que guarda el sistema (evidencia, diario, expedientes, libro, auditoría y configuración) se puede exportar completo en formatos abiertos y documentados, para no depender de ningún proveedor.

**Economía del análisis.** `[RATIFICADO]` (D-24)

1. **Tope de coste por oportunidad**, proporcional al importe que se invertiría `[RATIFICADO: 1 % del importe, con mínimo y máximo]` (P-19). La profundidad N0–N3 se elige por lo que está en juego: importe, incertidumbre y cuánto cambiaría la decisión con más información.
2. **Embudo de lo barato a lo caro:** filtros deterministas sobre K sin LLM; después análisis corto con modelos pequeños; solo los supervivientes pasan al análisis profundo con modelos grandes, al Contradictor y a D.
3. **Análisis incremental:** con el registro de análisis vigentes (§3), lo ya analizado se reutiliza si sus datos no cambiaron o se actualiza solo en la parte afectada.
4. **Trabajo por eventos:** se analiza y revisa cuando pasa algo relevante (un precio que cruza un umbral, un dato, un evento del calendario de K, un foco geopolítico), con una revisión periódica de seguridad de frecuencia baja.
5. **Ahorro en las llamadas:** las instrucciones fijas que se repiten (Constitución, kit del bloque, prompts) van con caché del proveedor y lo no urgente se procesa por lotes.

## 11. Fallos y modos degradados

Cada bloque DEBE declarar en su Documento 0 qué hace ante cada fallo de la tabla. La respuesta por defecto es detenerse, marcar y escalar. Nunca se rellena con estimaciones presentadas como hechos. `[RATIFICADO]` (D-43)

| Fallo | Respuesta |
| --- | --- |
| Dato obsoleto o ausente | Se detiene la decisión afectada, se marca y se pide verificación |
| Contrato con versión incompatible o paquete que no valida | Se rechaza; no se interpreta |
| Datos contradictorios entre fuentes | Se conservan ambos, se marca la discrepancia y no se decide sobre ella |
| Servicio externo caído (datos, intermediario) | Reintentos acotados, cola de errores y paso a L1 si afecta a G |
| Discrepancia **sin explicar** con el intermediario | **Desencadenante del kill-switch** |
| Latido del plano de control perdido | **Desencadenante del kill-switch** (lo activa el vigilante) |
| Orden sin confirmación verificable | Se trata como no ejecutada hasta conciliar; no se reenvía sin idempotencia |
| **Presupuesto de coste o tiempo agotado** (por encargo o por día) | El Orquestador detiene los encargos nuevos y entrega lo hecho con estado `INCOMPLETO` |
| **Bucle de agentes** (el mismo encargo repetido sin avance) | Corte tras el máximo de reintentos y aviso al operador |
| Incidente de seguridad (credenciales, inyección detectada) | **Desencadenante del kill-switch** y aísla del componente |
| Pérdida acumulada por encima del límite | Cortacircuito: la cartera pasa a L1 |
| Estrategia con deriva respecto al backtest | La estrategia pasa a `PAUSADA` y se avisa |
| El operador no responde a una aprobación | Caduca y no se actúa |
| `[RATIFICADO]` El operador no responde a ningún aviso durante el plazo fijado | **Modo hibernación** (§6): ni aperturas ni aumentos, protecciones intactas y aviso a la persona de confianza |

**Presupuesto duro.** Hay un tope de coste y tiempo **por encargo y por día**, fijado por el operador `[ABIERTO]`. La ruta determinista (§4.3) no consume modelos y no se ve afectada. Para el resto se usan modelos económicos en los niveles bajos de análisis y modelos potentes solo en los altos.

**Aviso al operador.** Todo aviso de prioridad alta sale por un canal fuera del chat, con acuse de recibo (CT-G-16). Un aviso sin acuse se reitera y escala.

**Desencadenantes del kill-switch** (§8): discrepancia sin explicar, incidente de seguridad, latido perdido, cortacircuito global y orden manual del operador.

**Lista de comprobación para rehabilitar** una cartera tras el kill-switch:

1. Causa identificada y corregida.
2. Conciliación limpia con el intermediario.
3. Datos frescos y segunda fuente de acuerdo.
4. Órdenes de protección verificadas en el intermediario.
5. Aprobación expresa del operador y paso por L1 durante un periodo mínimo `[ABIERTO]`.

## 12. Seguridad

1. **Credenciales.** Viven en la bóveda (SC-7) y solo las usan G y los conectores, mediante referencias. Nunca aparecen en el contexto de un agente, en un prompt, en un archivo de configuración ni en el historial. Una credencial compartida en un chat se considera comprometida y se revoca.
2. **Permisos mínimos y claves separadas.** Las claves del intermediario separan lectura de operación, y la de operación tiene límites de importe y de frecuencia fijados en el propio intermediario cuando este lo permite.
3. **Segregación de entornos.** Simulación, pruebas y producción están aislados y con credenciales distintas. Nada de pruebas puede enviar una orden real.
4. **Lectores aislados.** Los agentes que leen web, PDF o correo no tienen cartera, credenciales ni herramientas de acción. Su salida es un esquema estricto: listas cerradas, números con fuente y fecha, sin texto libre que otro agente trate como instrucción.
5. **Inyección detectada.** Un texto externo que intenta dar órdenes al sistema se registra como incidente (§11) y se ignora.
6. **Aprobaciones autenticadas.** Las que aumentan riesgo exigen segundo factor, un canal distinto del chat de trabajo y la pantalla del §6, que muestra las cifras de F y no texto de un LLM.
7. **Límites que no dependen de agentes.** Los límites nominales (§8) y las claves con tope impiden que un agente comprometido haga un daño ilimitado.
8. **Registro anexado.** La auditoría (SC-5) no se puede reescribir ni borrar desde los agentes. Los cambios de configuración y de permisos quedan en ella.
9. **Copias y recuperación.** Copias periódicas de los almacenes (evidencia, diario, libro) y un procedimiento de restauración que se prueba. `[RATIFICADO]` (D-40) La exportación completa en formatos abiertos (§10) se prueba igual que la restauración.
10. **Persona de confianza** `[RATIFICADO]` (D-32). La que avisa el modo hibernación (§6) nunca puede operar ni cambiar la configuración. Si el operador le da acceso de lectura (P-30), es con credenciales propias, revocables y registradas en la auditoría.
11. **Nada personal en el repositorio** `[RATIFICADO]` (D-47). El código es común a todas las copias y vive en un repositorio compartido; el perfil, los mandatos, las respuestas del cuestionario, las credenciales, los datos y la memoria de cada usuario viven solo en su copia (SC-1, SC-7). Las copias no comparten datos entre sí por defecto; compartir algo que no sea personal (por ejemplo, análisis para ahorrar costes) sería una opción posterior y voluntaria, sabiendo que correlaciona los errores de las copias.

## 13. Identificadores, versionado y numeración

| Elemento | Regla |
| --- | --- |
| Bloques A–N | Letra del bloque; cada bloque conserva los prefijos que ya usa (por ejemplo, `EMG-B-` en B) |
| Perfiles de C (y de A y B tras la refactorización) | `C-<COD>` (`C-DIV`, `C-RV`…); `C.n` es solo alias. Prefijo de identificadores propuesto: `-C<COD>-` |
| Contratos | `CT-B-nn` (A↔B, existentes) y `CT-G-nn` (globales, §5) |
| Mensajes y casos | `event_id`, `correlation_id` (petición), `expediente_id` (candidato), `posicion_id`, `senal_id`: únicos e inmutables; el formato lo fija el Documento 0 del Orquestador |
| Servicios comunes | `SC-n` (§3) |
| Metodología | Toda salida lleva `methodology_version` (versionado semántico) |
| `[RATIFICADO]` Copias | Cada copia guarda la versión de esquema de sus datos y se actualiza con migraciones, de modo que actualizar el código no le hace perder nada (D-47) |
| Esquemas | Versionado semántico; los esquemas `1.x` congelados no se editan, se versionan; los `0.x` admiten cambios compatibles con aviso en el §15 |
| Entregables | `Bloque X - Versión óptima Vn.n (fecha)`; esta Constitución sigue el mismo criterio |
| `[RATIFICADO]` Bases de datos y entrenamientos | `BD-nn` y `E-nn` (§9, punto 17; §10, punto 11); cada versión de un modelo entrenado lleva el hash de los datos y de los parámetros |
| `[RATIFICADO]` Fichas de bloque | Una por bloque y versión (CT-G-17), con los contratos que recibe y entrega |

El **identificador es la clave de todo almacén**: ningún componente recupera un dato por descripción en lenguaje natural.

## 14. Fases de construcción y reglas para construir bloques

**Estado actual.**

| Pieza | Estado |
| --- | --- |
| A V5.1 y B V2.1 | Construidos; se usan tal cual con adaptadores hasta la Fase 2, pero `[RATIFICADO]` (D-42) antes de conectarlos se revisan y se mejoran con el operador (T-53). A ya analiza divisas (Analista de Divisas y 5 de 11 fichas FX programadas; faltan 6). A Forex y B Forex quedan fuera (D-20) |
| Sobre CT-G-02 y marco común de C | Código de referencia en curso (V0.53, 8 de noviembre de 2026), con datos simulados: recorre la Fase 1 de punta a punta con versiones mínimas de referencia del Orquestador y de D, E, F, G, H y K, que guardan un único estado |
| C-DIV | Parcialmente desarrollado por otro LLM; el operador no lo ha compartido todavía |
| Otros perfiles de C, D, E, F, G, H, I, J | Sin construir como bloques: D, E, F, G y H solo existen como código de referencia mínimo en el marco común; el resto, solo con su ficha de interfaz (§2) |
| Orquestador y servicios comunes | Por definir según la fase |

**Fases con compuertas.** `[RATIFICADO]` (D-09) No se empieza una fase sin superar la compuerta de la anterior. Una pieza sin demanda real en la fase en curso no se construye.

| Fase | Contenido | Compuerta para pasar a la siguiente |
| --- | --- | --- |
| **0 · Cimientos** | Esta Constitución ratificada; ficha de restricciones reales (intermediario, datos, presupuesto, fiscalidad); mandato de la primera cartera | El operador ratifica la V0.2 y fija los pendientes que bloquean la Fase 1 (§15) |
| **1 · Rebanada vertical** | **Divisas, cartera táctica, L0 y L1.** A y B (con las 6 fichas FX que faltan en A programadas) + adaptadores; `C-DIV` con CT-G-02 `0.x`; Contradictor; D dentro de divisas; E mínimo; F con límites nominales; G con simulador y registro manual (CT-G-14); Orquestador mínimo; Bloque K (mínimo, divisas, con el COT de la CFTC), Bloque N (mínimo), Broker Personal (perfil inversor), SC-3, SC-4 mínimo `[RATIFICADO]` (diario, torneo y calibración; enmienda 2), SC-5, SC-6, SC-10, SC-11 mínimo, registros comunes y cartera sombra pasiva | Una serie de recorridos de punta a punta sin intervención en L0 y conciliación limpia durante el periodo fijado en L1 `[ABIERTO]` |
| **2 · Segundo perfil** | `C-RV`, un perfil muy distinto; refactorización de A y B a núcleo + perfil; congelación de CT-G-02 `1.0.0`; D entre tipos y clases; cartera de largo plazo; SC-8 y SC-9 con reglas validadas por un asesor | Dos perfiles emiten sobres válidos y D los compara correctamente |
| **3 · Intermediario real** | Conexión real en L1 con conciliación; órdenes de protección nativas; H; kill-switch y vigilante probados con simulacros; SC-4 completo; Bloque M (riesgo de cartera, con pruebas de estrés geopolíticas); avisos fuera del chat | Simulacros superados y conciliación limpia durante el periodo fijado; primer L2 con umbral pequeño |
| **4 · Estrategias** | J, ruta determinista, trading en paper y luego en L2 con capital pequeño; detección de deriva | Criterios del §7 |
| **5 · Ampliación** | Resto de perfiles de C por demanda (cada uno es un perfil con paquete propio, no un bloque nuevo; solo se construye el que una cartera necesite); SC-11 completo; `C-ALT` con startups bajo tope; I completo; derivados y apalancamiento si el operador los habilita; L3 en horario supervisado | — |

**Reparto por fases de la enmienda 2.** `[RATIFICADO]` Cada pieza entra cuando su fase la necesita (P14):

| Fase | Entra |
| --- | --- |
| 1 | Vía `DIRECTA` y modo `CONSULTA`; probabilidades verificables y torneo de pronósticos; calibración de agentes y prueba de instrucciones a pequeña escala, hechas por código de SC-4 sin activar J (no cuenta para el tope de bloques); varios análisis independientes en N3; escalera de verificación hasta el paper trading; fichas de bloque, batería de conformidad y adaptador de A y B a `CT-G`; asesor de configuración con valores de partida `[PROPUESTO]` en simulado; bases de datos del mundo para divisas y las del propio robot |
| 2 | Estado separado por bloque, al empezar la fase; rentabilidad mínima, aportaciones mensuales, vehículo fiscal, camino de riesgo y proyecciones con la cartera de largo plazo; parámetros contextuales por tipo de activo; colchón y revisión anual en el Broker |
| 3 | Modo hibernación y persona de confianza, con el intermediario real; vigía de régimen; dinero real en pequeño |
| 4 | J como laboratorio completo (modelos, instrucciones y agentes) y, a la vez, la parte de I que puntúa (veredicto con la reserva sellada), adelantada de la Fase 5; aprendizaje automático como aspirante; meta-etiquetado con el historial acumulado; cambio de modelo de IA con conjunto dorado |
| 5 | Aprendizaje por refuerzo si lo anterior se queda corto |

**Reglas al construir un bloque.**

1. **Kit de contexto cerrado:** esta Constitución, la ficha de interfaz del bloque, los contratos que le afectan y, si parte de otro, su Documento 0.
2. **Contratos primero:** se escriben y validan los esquemas antes de prompts y motores, respetando la congelación diferida (§5).
3. **Perfil, no bloque:** un nuevo tipo de activo es un perfil sobre el núcleo, salvo que cumpla el criterio de bloque nuevo (§2) y el operador lo decida.
4. **Entregable completo:** Documento 0, contratos y esquemas, agentes y prompts, módulos del Motor, configuración, pruebas, ejecutor, manual de operación y ficha de interfaz.
5. **Definición de terminado:** esquemas validan, pruebas pasan, ejecución de extremo a extremo con datos simulados, validación determinista de salidas, referencias verificadas o marcadas, **prueba de recorrido de los casos de la fase** y revisión por un agente independiente `[RATIFICADO]`, preferiblemente de otro proveedor de IA; además, la ficha del bloque (CT-G-17) publicada y su batería de conformidad superada (§5).
6. **Sin tocar la Constitución:** si un bloque necesita algo que esta no prevé, propone una enmienda en el §15.
7. **Adaptadores, no reescrituras,** hasta la Fase 2. En la Fase 2 se refactorizan A y B con dos casos reales a la vista.
8. **Conversación de diseño primero** `[RATIFICADO]` (D-42). Antes de empezar un bloque sin construir hay una conversación de diseño con el operador: qué hace el bloque, qué agentes tiene, cómo se reparten el trabajo, qué es LLM y qué es código y qué fuentes usa. Solo después se escribe su Documento 0. El operador participa en el diseño; no se le presenta un diseño cerrado.
9. **Revisión de A y B antes de conectarlos** `[RATIFICADO]` (D-42). Se repasan con el operador a la luz de esta Constitución y del marco común (T-53), y se mejoran antes de conectarlos al resto.

## 15. Registro de decisiones y pendientes

**Decisiones.**

| ID | Decisión | Estado | Fecha |
| --- | --- | --- | --- |
| D-01 | Solo capital propio (desde D-47, en cada copia, solo el de su usuario) | RATIFICADO | 2026-11-05 |
| D-02 | Tres carteras: trading, táctica y largo plazo | RATIFICADO | 2026-11-05 |
| D-03 | Tres modos de autonomía (manual, semiautónomo, autónomo) | RATIFICADO | 2026-11-05 |
| D-04 | Trading en días y semanas por ahora | RATIFICADO | 2026-11-05 |
| D-05 | D compara dentro de cada tipo de activo y entre tipos | RATIFICADO | 2026-11-05 |
| D-06 | Los 12 tipos de activo del Bloque A y códigos `C-<COD>` | RATIFICADO | 2026-11-05 |
| D-07 | El operador autoriza modificar la idea base, incluidos los bloques A y B | RATIFICADO | 2026-11-05 |
| D-08 | Mapa de bloques A–N (con J, Laboratorio de estrategias; K, M, N) y servicios SC-1 a SC-11 | RATIFICADO | 2026-11-09 |
| D-09 | Construcción por fases con compuertas; Fase 1 = divisas, cartera táctica, L0 y L1 | RATIFICADO | 2026-11-09 |
| D-10 | A, B y C como núcleo común + perfil; refactorización de A y B en la Fase 2 | RATIFICADO | 2026-11-09 |
| D-11 | Broker en tres papeles (conversacional, Orquestador, gestores de cartera) | RATIFICADO | 2026-11-09 |
| D-12 | Sobre común por capas, clases Q/S/K y `NO_ESTIMABLE`; congelación diferida a `1.0.0` | RATIFICADO | 2026-11-09 |
| D-13 | Ciclos separados de oportunidad y posición; ruta determinista sin LLM | RATIFICADO | 2026-11-09 |
| D-14 | Stops nativos en el intermediario; F con segunda fuente y límites nominales; kill-switch que no cancela protecciones; vigilante con latido | RATIFICADO | 2026-11-09 |
| D-15 | Niveles L0–L3, matriz de autonomía, controles sobre el operador y L3 solo en horario supervisado | RATIFICADO | 2026-11-09 |
| D-16 | Apalancamiento, derivados y CFD no habilitados hasta que el operador lo decida, no antes de la Fase 3 | RATIFICADO | 2026-11-09 |
| D-17 | Perfiles C como paquetes propios bajo un solo núcleo, con estados ACTIVO y NO\_CONSTRUIDO; solo se construye el que una cartera necesite | RATIFICADO | 2026-11-05 |
| D-18 | Bloques K (datos), N (consola) y M (riesgo de cartera, Fase 3); noticias como servicio aislado SC-11; sin bloque L | RATIFICADO | 2026-11-05 |
| D-19 | Criterio de bloque nuevo (3 de 5) y tope de 8 bloques activos en las Fases 1 y 2 | RATIFICADO | 2026-11-05 |
| D-20 | A Forex y B Forex fuera del sistema; A y B generales; la Fase 1 sigue en divisas | RATIFICADO | 2026-11-07 |
| D-21 | Broker Personal como bloque en tres papeles, con lenguaje para inexpertos, perfil inversor y de riesgo y política de inversión personal | RATIFICADO | 2026-11-07 |
| D-22 | Contrapesos de la abstención (referencia invertida, embudo, alarma de sequía, seguimiento de lo descartado) y cartera sombra pasiva | RATIFICADO | 2026-11-07 |
| D-23 | Intercambio entre bloques por el Orquestador y registros comunes | RATIFICADO | 2026-11-07 |
| D-24 | Economía del análisis: tope de coste, embudo, análisis incremental, eventos, caché y lotes | RATIFICADO | 2026-11-07 |
| D-25 | Calidad de las decisiones: clase de referencia, freno a la rotación, fiscalidad en la decisión, concentración mínima antes de M, presupuesto de complejidad | RATIFICADO | 2026-11-07 |
| D-26 | Cobertura nueva sin bloques nuevos: geopolítica con SC-11 mínimo en la Fase 1, radar tecnológico en A, small caps y spin-offs en C-RV, startups en C-ALT, posicionamiento de grandes inversores en K | RATIFICADO | 2026-11-07 |
| D-27 | Números de la enmienda 1: alarma de sequía a 60 días; cartera sombra en un índice mundial juzgada a los 24 meses; tope de coste de análisis del 1 % del importe (con mínimo y máximo); freno a la rotación con margen del doble de los costes; revisión de complejidad cada 6 meses; liquidez máxima del 5 % del volumen medio diario; startups no cotizadas hasta el 2 % de la cartera | RATIFICADO | 2026-11-07 |
| D-28 | Vía de entrada `DIRECTA` y modo `CONSULTA`: se entra por cualquier bloque y al dinero solo por F y G; el expediente nace en el estado del bloque de entrada | RATIFICADO | 2026-11-09 |
| D-29 | Motor de cálculo avanzado (SC-3: servicio común que se entrega como un bloque y no cuenta para el tope) con módulo de proyecciones del plan | RATIFICADO | 2026-11-09 |
| D-30 | Rentabilidad mínima exigida, no garantizada, comprobada por el Motor y por F en L2 y L3 según la vía (interpretación: T-58 decía «en autónomo»; se extiende a L2), con reequilibrio y benchmark exentos; todo medido también después de inflación | RATIFICADO | 2026-11-09 |
| D-31 | Plan de largo plazo: aportaciones mensuales como ciclo propio, vehículo fiscal en la decisión y camino de riesgo | RATIFICADO | 2026-11-09 |
| D-32 | Protecciones del operador: colchón fuera del robot, revisión anual guiada, modo hibernación y persona de confianza de solo lectura | RATIFICADO | 2026-11-09 |
| D-33 | Vigía de régimen económico en SC-8, que solo endurece | RATIFICADO | 2026-11-09 |
| D-34 | Parámetros contextuales y asesor de configuración en el Broker; los límites duros de F y el kill-switch no los fija un modelo | RATIFICADO | 2026-11-09 |
| D-35 | Varios análisis independientes cuyo desacuerdo cuenta como incertidumbre, siempre en N3 y en el resto cuando lo justifique lo que está en juego (recorte deliberado frente a «por decisión» de T-58, por la economía del análisis, D-24); toda tesis con probabilidad, plazo y criterio de resolución | RATIFICADO | 2026-11-09 |
| D-36 | Peso por historial verificado, torneo de pronósticos, mínimo de decisiones, aspirante frente a titular y autopsias | RATIFICADO | 2026-11-09 |
| D-37 | Incentivos de los agentes por diseño del sistema y defensas contra la ley de Goodhart | RATIFICADO | 2026-11-09 |
| D-38 | J como laboratorio de estrategias, modelos, instrucciones y agentes: J entrena, código de I da el veredicto con la reserva sellada (adelantado a la Fase 4), F y el operador aprueban; catálogo de bases de datos y entrenamientos; aprendizaje automático solo como aspirante | RATIFICADO | 2026-11-09 |
| D-39 | Escalera de verificación para estrategias, modelos, instrucciones y agentes, con verificaciones externas | RATIFICADO | 2026-11-09 |
| D-40 | Cambio de modelo de IA solo tras un conjunto dorado; historial completo exportable en formatos abiertos | RATIFICADO | 2026-11-09 |
| D-41 | Enchufabilidad: ficha de bloque (CT-G-17) y registro, batería de conformidad, estado por bloque, adaptadores de A y B a `CT-G` y adaptadores de modelos de IA | RATIFICADO | 2026-11-09 |
| D-42 | Reglas del operador: todo bloque sirve para cualquier tipo de activo (núcleo + perfiles desde el primer día; encaje con la Fase 2 ratificado el 9-11-2026); A y B se revisan con el operador antes de conectarlos; conversación de diseño con el operador antes de cada bloque sin construir; decisiones del operador aplazadas hasta completar la arquitectura, con valores PROPUESTO en simulado y una sesión única (T-57) | RATIFICADO | 2026-11-08 |
| D-44 | Cuestionario guiado de configuración, de opción múltiple y explicado en euros, con un asesor que interpreta la respuesta libre y confirma cada interpretación; formato de la sesión T-57 | RATIFICADO | 2026-11-09 |
| D-45 | Valores por defecto prudentes y justificados para cualquier usuario; todo parámetro nuevo llega con su valor por defecto y su pregunta | RATIFICADO | 2026-11-09 |
| D-46 | Cambios posteriores por el mismo cuestionario, a cargo del Broker Personal, con la asimetría de riesgo (§6) y la ruta única de cambios (§9) | RATIFICADO | 2026-11-09 |
| D-47 | Una copia por usuario con su propio dinero; D-01 se aplica por copia; nada personal en el repositorio; actualización con migraciones; copias sin datos compartidos por defecto | RATIFICADO | 2026-11-09 |
| D-43 | Ratificación de los apartados sin decisión numerada: verificación diversa (§3), catálogo de contratos globales (§5), tabla de las tres carteras (§7), ciclo de vida de una estrategia (§7), memoria y aprendizaje realista (§9) y fallos y modos degradados (§11) | RATIFICADO | 2026-11-09 |

**Pendientes del operador.** `[RATIFICADO]` (D-42) Las decisiones de perfil y técnicas del operador se aplazan hasta completar la arquitectura global. Mientras tanto se construye en simulado (L0) con valores de partida prudentes marcados `[PROPUESTO]`; solo se le pregunta lo que cambie la arquitectura y no tenga un valor de partida razonable; nada opera con dinero real ni pasa una compuerta que exija datos reales hasta que decida; y al final se le presentan todas en una sola sesión, cada una con su valor de partida y lo que cambia según su respuesta (T-57), conducida por el asesor de configuración (§2) en formato de cuestionario guiado (D-44).

| ID | Pendiente | Afecta a |
| --- | --- | --- |
| P-01 | Umbrales de las acciones automáticas en L2 | §6, F |
| P-02 | Criterios y duración mínima para subir de nivel de autonomía | §6 |
| P-03 | Valores del mandato de cada cartera, incluido el benchmark | §7, SC-1, E, F |
| P-04 | Horizontes de la cartera táctica y de largo plazo | §7 |
| P-05 | **Ficha de restricciones reales:** intermediario, tipos de cuenta, API, datos y licencias (bloquea G y SC-2) | §3, G, SC-2, SC-10 |
| P-06 | Jurisdicción fiscal (se asume España) y asesor que valide las reglas de SC-9 | SC-9 |
| P-07 | Presupuesto de coste y tiempo por encargo y por día | §11, Orquestador |
| P-08 | Canal y segundo factor para aprobaciones, y canal de avisos fuera del chat | §6, §12 |
| P-09 | Qué alias `C.n` se usará en las comunicaciones (los códigos ya son estables) | §2 |
| P-10 | ~~Pendientes de B Forex~~ Cerrado sin efecto: B Forex queda fuera del sistema (D-20) | — |
| P-11 | Límites nominales duros (importes, pérdidas, número de órdenes) | §8, F |
| P-12 | Horario supervisado para L3 | §6 |
| P-13 | Tolerancias de conciliación y umbral de fecha de corte común | §4, §8 |
| P-14 | Muestra mínima para calibrar y periodos de las compuertas de las fases | §9, §14 |
| P-15 | Ratificar la clase de comparabilidad (Q, S, K) de cada tipo de activo | §5 |
| P-16 | Confirmar la cartera de la Fase 1 (propuesta: táctica). El tipo de activo, divisas, lo confirmó el operador el 7-11-2026 | §14 |
| P-17 | ~~Plazo de la alarma de sequía (propuesta: 60 días)~~ Resuelto: propuesta aceptada (D-27) | §7 |
| P-18 | ~~Plan pasivo de la cartera sombra y plazo para juzgar al robot (propuesta: índice mundial; 24 meses)~~ Resuelto: propuesta aceptada (D-27) | §9 |
| P-19 | ~~Tope de coste de análisis por oportunidad (propuesta: 1 % del importe, con mínimo y máximo)~~ Resuelto: propuesta aceptada (D-27) | §10 |
| P-20 | ~~Margen del freno a la rotación (propuesta: el doble de los costes de cambiar)~~ Resuelto: propuesta aceptada (D-27) | §7 |
| P-21 | ~~Periodo de la revisión de complejidad (propuesta: 6 meses)~~ Resuelto: propuesta aceptada (D-27) | §9 |
| P-22 | ~~Límite de liquidez (propuesta: 5 % del volumen medio diario)~~ Resuelto: propuesta aceptada (D-27) | §8 |
| P-23 | ~~Tope de startups no cotizadas (propuesta: 2 % de la cartera)~~ Resuelto: propuesta aceptada (D-27) | §2, §7 |
| P-24 | Fuentes de noticias de SC-11 en la Fase 1 | §3 |
| P-25 | Rentabilidad mínima exigida por cartera (real, anual), probabilidad suficiente para superarla e índice de inflación (propuesto: IPCA de la zona euro). Aplazado hasta completar la arquitectura (T-57), como P-26 a P-35 | §7, §8 |
| P-26 | Importe de las aportaciones mensuales (el valor vive en SC-1, fuera del repositorio) | §7 |
| P-27 | Fecha de cada objetivo y senda del camino de riesgo | §7 |
| P-28 | Vehículos fiscales que se usarán (fondos traspasables, ETF, acciones) | §7, SC-9 |
| P-29 | Meses de gastos que debe cubrir el colchón de emergencia (el valor vive en SC-1, fuera del repositorio) | §2 |
| P-30 | Plazo sin respuesta que activa la hibernación; persona de confianza y si solo recibe el aviso o también puede consultar la cartera (los datos de la persona viven en SC-1, fuera del repositorio) | §6, §12 |
| P-31 | Indicadores y umbrales del vigía de régimen y límites endurecidos de cada estado | §3, §8 |
| P-32 | Mínimo de decisiones resueltas para dar peso o autonomía a un modelo o agente | §9 |
| P-33 | Duración de cada peldaño de la escalera de verificación y tamaño del capital pequeño | §7 |
| P-34 | Tamaño del conjunto dorado y umbral para aceptar un modelo de IA nuevo | §9 |
| P-35 | Si se quiere un suelo asegurado en renta fija sin riesgo, y de cuánto | §7 |

**Trazabilidad de la revisión independiente.** Los 13 hallazgos y dónde se atienden en esta versión.

| N.º | Hallazgo | Respuesta | Sección |
| --- | --- | --- | --- |
| 1 | Sobreingeniería para una persona | Fases con compuertas, rebanada vertical, «mínimo primero» | §14, P14 |
| 2 | El sobre común exige cifras inviables | Capas, `NO_ESTIMABLE`, clases de comparabilidad | §5, §10 |
| 3 | Calibración sin muestra | Topes ex ante, tesis descompuestas, diario | §9 |
| 4 | Sesgos correlacionados entre agentes | Verificación diversa, F como único control real | §3, P15 |
| 5 | F sin datos independientes | Segunda fuente del intermediario y límites nominales | §8 |
| 6 | Kill-switch inseguro y falsos positivos | Stops nativos, tolerancias, vigilante con latido | §8, §11 |
| 7 | Huecos de estados y autonomía | Ciclos de oportunidad y posición; reducciones solo por regla numérica | §4, §6 |
| 8 | Inyección y exfiltración | Lectores aislados, esquemas estrictos, pantalla de aprobación con cifras de F | §3, §6, §12 |
| 9 | Error del operador | Enfriamiento, límite de anulaciones, confirmación del importe | §6 |
| 10 | Eventos extremos y apalancamiento | L3 en horario, ventanas de restricción, derivados no habilitados | §6, §8 |
| 11 | Coste y latencia | Presupuesto duro; ruta determinista sin LLM | §4.3, §11 |
| 12 | Contratos congelados antes de tiempo | Congelación diferida | §5 |
| 13 | Fiscalidad | Reglas codificadas y validadas por asesor | §3, §10 |

**Enmiendas.** Se proponen aquí, se ratifican por el operador y generan una nueva versión. Ninguna conversación de construcción las aplica por su cuenta. La enmienda 1 se ratificó el 7-11-2026 (V0.4). La **enmienda 2** se aplicó el 9-11-2026 a petición del operador y él la ratificó ese mismo día (V0.5); sus números quedan pendientes (P-25 a P-35) para la sesión de decisiones (T-57). La **enmienda 3** (T-59) se aplicó y ratificó el 9-11-2026 (V0.6).

## 16. Glosario

| Término | Significado |
| --- | --- |
| **Operador** | El usuario de cada copia, único titular de su capital y de las decisiones ratificadas en ella (D-47) |
| **Copia** | Instalación del Robot Inversor de un solo usuario, con su dinero y sus datos (D-47) |
| **Cuestionario guiado** | Preguntas de opción múltiple con las que el asesor del Broker configura una copia y la cambia después (§2) |
| **Broker Personal** | Bloque que reúne el Broker conversacional, el Orquestador y los gestores de cartera (§2) |
| **Broker conversacional** | Agente con juicio y diálogo con el operador; atiende peticiones nuevas y excepciones |
| **Orquestador** | Código que mueve los expedientes, gestiona colas, plazos y presupuestos |
| **Gestor de cartera** | Agente acotado que lleva el flujo cotidiano de un libro dentro de su mandato |
| **Núcleo / perfil** | Parte común de un bloque y parte propia de cada tipo de activo (§2) |
| **Expediente** | Un candidato en su camino de la idea a la decisión (§4.1) |
| **Posición** | Lo ya comprado, con sus propios estados (§4.2) |
| **Señal** | Registro de una decisión de una estrategia validada en la ruta determinista |
| **Sobre común** | Salida por capas que hace comparables los perfiles de C (§5) |
| **Clase Q, S, K** | Cuantitativa, semicuantitativa o cualitativa: qué base tiene un tipo de activo para estimar |
| **`NO_ESTIMABLE`** | Valor válido cuando no hay modelo defendible |
| **Plano** | Inteligencia, control o datos y memoria (§3) |
| **SC-n** | Servicio común compartido por todos los bloques |
| **L0–L3** | Niveles de autonomía (§6) |
| **Orden de protección** | Stop u orden de salida colocada en el propio intermediario (§8) |
| **Segunda fuente** | Datos del intermediario, independientes de la cadena de agentes |
| **Diferencia explicada** | Discrepancia esperable de conciliación, dentro de tolerancia |
| **Vigilante** | Proceso independiente que comprueba el latido del plano de control |
| **Kill-switch** | Cancela entradas, bloquea nuevas órdenes y pasa todo a L1 (§8) |
| **Contradictor** | Agente que ataca la tesis a partir de la evidencia, preferiblemente de otro modelo |
| **Motor** | Motor de cálculo avanzado (SC-3): cálculo reproducible con modelos declarados, cola de trabajos y caché; da distribuciones, no predicciones exactas |
| **N0–N3** | Niveles de profundidad de análisis ya definidos en los bloques A y B |
| **Look-ahead** | Usar en una prueba histórica información que no se conocía en esa fecha |
| **Idempotencia** | Repetir una orden o mensaje no produce un segundo efecto |
| Perfil ACTIVO / NO\_CONSTRUIDO | Estado de un perfil C-\<COD>: un perfil no construido devuelve NO\_ESTIMABLE y no se encarga (§2) |
| Bloques K, M, N | Datos y calidad de datos; riesgo de cartera; consola del operador (§2) |
| Sello de corte | Fecha de corte común que emite K y heredan todos los análisis comparables |
| Perfil inversor | Ficha versionada de conocimientos, situación, objetivos y tolerancia al riesgo del operador (§2, SC-1) |
| Cartera sombra | Plan pasivo simulado con el que se compara siempre el robot (§9) |
| Clase de referencia | Estadística de casos parecidos de la que parte toda tesis (§5) |
| Registros comunes | Análisis vigentes, riesgos geopolíticos, tendencias tecnológicas y posicionamiento (§3) |
| Alarma de sequía | Aviso cuando en un plazo nada llega a invertirse habiendo candidatos (§7) |
| Vía directa / consulta | Entrada del Broker por C, D o E sin pasar por A y B; una consulta no abre camino a una orden (§2) |
| Rentabilidad mínima exigida | Rentabilidad real anual que cada inversión debe superar después de costes e impuestos; no es una garantía (§7) |
| Camino de riesgo | Senda por la que la cartera de largo plazo reduce su riesgo al acercarse un objetivo (*glide path*, §7) |
| Modo hibernación | Estado en que, sin respuesta del operador, no se abre nada y se mantienen las protecciones (§6) |
| Vigía de régimen | Semáforo por región (normal, tensión, crisis) que solo endurece (§3) |
| Asesor de configuración | Parte del Broker que propone parámetros a partir del perfil y los explica en euros (§2) |
| Escalera de verificación | Backtesting, paper trading, dinero real en pequeño y escala, sin saltar peldaños (§7) |
| Aspirante / titular | Versión nueva que compite con la que está en uso y solo la sustituye si la supera (§9) |
| Puntuación de Brier | Medida de lo bien que acierta una probabilidad; cuanto más baja, mejor (§9) |
| Conjunto dorado | Casos resueltos que todo modelo de IA nuevo debe pasar antes de sustituir al actual (§9) |
| Reserva sellada | Datos apartados para la prueba final, que quien entrena no puede ver (§9) |
| Ficha de bloque | Manifiesto de un bloque: contratos, versiones, capacidades y modos de fallo (CT-G-17, §5) |
| Contracción hacia pesos iguales | Mientras un agente tiene poco historial, su peso se acerca al de los demás en lugar de fiarse de pocos aciertos (§9) |
| Validación purgada con embargo | Prueba por bloques de tiempo que deja un hueco entre los datos de entrenar y los de probar, para que no se filtre información (§9) |
| Sharpe deflactado | Rentabilidad ajustada al riesgo corregida por el número de pruebas hechas: con muchas pruebas, alguna sale bien por azar (§9) |
| Probabilidad de sobreajuste | Probabilidad de que lo mejor en el pasado sea peor que la media fuera de él (§9) |
| Meta-etiquetado | Modelo que aprende cuáles de las propuestas del propio robot suelen salir bien (§9) |
| GARCH | Modelo estadístico clásico de volatilidad; sirve de referencia simple (§9) |
| Ley de Goodhart | Cuando una medida se convierte en objetivo, deja de medir bien: el agente optimiza la medida y no lo que importa (§9) |
