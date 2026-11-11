# Broker Personal: el asesor que trabaja para el operador (propuesta de diseño de Claude)

De: Claude, 11-11-2026. Estado: **PROPUESTA PARA DISCUTIR**. No hay nada que implementar: el operador está decidiendo la arquitectura de los bloques antes de construir (relevo de Astra, §0 bis). Copia en el repositorio del documento que el operador revisó con Claude.

## 1. Respuesta corta

El Broker Personal es el único bloque que conoce al operador y el que coordina a todos los demás. La Constitución lo define en tres papeles: conversacional, Orquestador y gestores de cartera (D-21). También decide cómo se intercambian datos los bloques (D-23), dónde viven el perfil y la política de inversión personal y cómo funciona el asesor de configuración. El Orquestador ya tiene código; el resto no.

Idea central: **el código dirige y la IA habla.** El Orquestador marca el ritmo, y la IA solo interviene para conversar con el operador o resolver una excepción. Se propone:

1. **Siete funciones, como mucho tres agentes de IA.** El perfilador y el asesor de configuración son modos del conversacional; el guardián de la política personal es código; los gestores de cartera son código y llaman a la IA solo en excepciones.
2. **Un planificador patrimonial:** aportaciones, colchón, deuda, planes de pensiones y vehículo fiscal. Para un particular suele valer más que elegir activos.
3. **El Orquestador reparte la atención:** decide qué se analiza primero y con cuánto presupuesto, según lo que pueda cambiar una decisión.
4. **Sin memoria libre:** lo que el Broker sabe del operador está en SC-1, en los expedientes y en un diario de decisiones, exportable y borrable.
5. **Por defecto, no hacer nada:** el dinero va al índice de referencia de cada cartera mientras nada demuestre que lo mejora.

## 2. Dónde gana o pierde rentabilidad el Broker

Para un particular, las decisiones que más pesan no suelen ser qué activo comprar, sino cuánto ahorrar, dónde ponerlo y no estropearlo en una caída. Eso es trabajo del Broker.

| Palanca | Ejemplo | Por qué pesa |
| --- | --- | --- |
| Comportamiento | Vender en una caída, perseguir lo que ya subió | Unos 1,2 puntos al año de media según el «Mind the Gap» de Morningstar (citado en la propuesta de N) |
| Deuda antes que inversión | Devolver un préstamo al 5 % equivale a ganar un 5 % seguro | Ninguna inversión con riesgo lo garantiza |
| Vehículo fiscal | En España, los fondos de inversión se traspasan sin tributar; las acciones y la mayoría de ETF, no | Reequilibrar sin pagar impuestos deja crecer más dinero durante años (lo valida el asesor fiscal, P-06) |
| Aportaciones bien usadas | Reequilibrar comprando lo que está por debajo de su peso | Ahorra costes e impuestos (§7) |
| Colchón de emergencia | Tener el dinero de imprevistos fuera del robot | Evita vender en el peor momento por necesidad |
| Atención y presupuesto | Analizar lo que puede cambiar una decisión; no repetir análisis | Cada euro de IA mal gastado resta |
| No hacer nada | Quedarse en el índice de referencia | Lo activo solo compensa si gana a la sombra |
| Coste del propio Broker | Conversaciones largas con un modelo caro | Puede comerse la ventaja de todo lo demás |

## 3. Qué hay hoy y qué falta

**Decidido en la Constitución:**

- Tres papeles (D-21).
- Los bloques se pasan datos por el Orquestador, nunca por el conversacional (D-23).
- Lenguaje para inexpertos.
- Perfil inversor en SC-1, versionado.
- Política de inversión personal.
- Asesor de configuración con cuestionario guiado (D-34, D-44, D-46).
- Colchón de emergencia y revisión anual (D-32).
- Hibernación y persona de confianza.
- Aportaciones mensuales como ciclo propio.
- Presupuesto duro por encargo y por día.

La enmienda 4 propone separar más papeles (E4-14), un perfilador con salvaguardas (E4-15) y la planificación patrimonial (E4-16).

**En código:**

- El Orquestador (V0.04 y siguientes): estados del expediente y de la posición, validación de encargos y sobres, idempotencia, presupuestos, caducidades e historial encadenado. Falla cerrado.
- Los mandatos de SC-1 (V0.32).

**Falta:**

- El conversacional, los gestores de cartera (T-07), el perfilador y el planificador.
- Cómo decide el Orquestador qué se analiza primero y cómo reparte el presupuesto entre carteras.
- Las rutinas por calendario.
- Qué recuerda el Broker y dónde.
- Cómo se resuelven los conflictos entre carteras.
- Los umbrales del Orquestador (D-05) y el presupuesto (P-07), pendientes del operador.

## 4. Los papeles del Broker

La enmienda 4 los llamó papeles; aquí se tratan como **funciones**, porque no todas necesitan un agente. Solo tres usan IA, y dos de ellas solo de vez en cuando.

| Función | Naturaleza | Hace | Tiene prohibido |
| --- | --- | --- | --- |
| 1. Conversacional | IA, el único papel que habla con el operador | Conversa, explica en euros, atiende peticiones y resuelve excepciones dentro de las reglas | Calcular, aprobar riesgo, enviar órdenes y pasar datos entre bloques |
| 2. Perfilador | Modo del conversacional, con su propio kit | Propone cambios del perfil, cada uno con su fuente | Aplicar nada sin confirmación |
| 3. Asesor de configuración | Modo del conversacional, con el Motor | Cuestionario guiado con las consecuencias en euros de cada opción | Cambiar parámetros por su cuenta |
| 4. Planificador patrimonial | Motor y poca IA (solo para redactar) | Plan a décadas: aportaciones, colchón, deuda, planes de pensiones, vehículo fiscal y camino de riesgo | Elegir activos |
| 5. Gestores de cartera, uno por libro | Código; IA solo en excepciones | Rutinas de su libro: qué encargar, cuándo reequilibrar y cómo usar la aportación | Hablar entre sí y salirse del mandato |
| 6. Guardián de la política personal | Código (reglas) | Recuerda la política ante una orden que la contradice | Impedir la orden |
| 7. Orquestador | Código | Estados, colas, prioridades, presupuestos, rutinas y registro de análisis vigentes | Juzgar inversiones |

**Por qué modos y no agentes.** El perfilador y el asesor usan el mismo modelo que el conversacional, pero con instrucciones y contexto propios y más cortos. Así no hay tres agentes que se pasen la conversación, y cada llamada carga solo lo que necesita.

**Gestores primero en código.** El día a día de un libro casi siempre son reglas: vencimientos, aportaciones, reequilibrios por bandas y alertas de H. La IA solo entra cuando algo no encaja en las reglas, como un conflicto entre carteras, un evento sin regla o una petición nueva.

## 5. Los papeles alrededor del Orquestador

Diagrama del documento («El código dirige y la IA habla»):

- **Operador** (conversa y decide en N) ↔ **Conversacional**.
- **Capa con IA:** gestores en excepciones (conflictos, eventos sin regla, peticiones nuevas); conversacional (modos perfilador y asesor de configuración); planificador patrimonial (Motor; la IA solo redacta).
- **Capa solo código:** gestores de cartera (trading, táctica y largo plazo; rutinas) ↔ **Orquestador** (estados, colas, prioridades, presupuestos y rutinas) ↔ guardián de la política personal (recuerda, no impide).
- Flechas: el conversacional propone al Orquestador; el planificador le pasa el plan; los gestores suben a la capa de IA solo en excepciones.
- **Orquestador ↔ bloques A–N y servicios comunes**, con contratos cerrados: los datos entre bloques solo pasan por el Orquestador (D-23).

El operador solo habla con el conversacional y decide en N. Lo que tiene IA propone; el Orquestador, en código, lo convierte en encargos y estados, y es el único que pasa datos a los bloques. Los gestores llevan su libro con reglas y solo llaman a la IA cuando algo no encaja.

## 6. El Broker en el tiempo

Casi todo el trabajo es una rutina que lanza el Orquestador. La IA aparece en pocas filas.

| Cuándo | Qué pasa | Quién | ¿IA? |
| --- | --- | --- | --- |
| Cada día | Cada gestor revisa su libro (alertas de H, límites de F, vencimientos) y el Orquestador lanza los encargos por orden de prioridad | Gestores y Orquestador | Solo si hay una excepción |
| Cada semana | Resumen semanal en N y revisión de la cartera táctica | Orquestador; el conversacional redacta | Una llamada |
| Cada mes | Aportación: se reequilibra comprando lo que está por debajo de su peso; informe de I | Gestor de largo plazo y planificador | No, salvo el texto del informe |
| Cada año | Revisión guiada (D-32): perfil, colchón, aportaciones, política personal, resultado frente a la sombra, plan y, antes de fin de año, compensación de pérdidas | Conversacional, planificador y asesor | Sí: es la conversación más importante del año |
| En una caída | El guardián recuerda la política; el conversacional explica en euros con las cifras de M; H y F actúan por sus reglas | Guardián, conversacional, H y F | Solo para explicar |
| Cuando el operador pide algo | «¿Y si compro X?» se convierte en un encargo por la ruta normal; el Broker no opina sin análisis | Conversacional y Orquestador | Para entender la petición |
| Si el operador no responde | Hibernación: nada nuevo, protecciones intactas y aviso a la persona de confianza | Orquestador | No |

## 7. Perfil, política personal y memoria

**El perfil se deduce, pero no se impone.** El perfilador usa tres fuentes, de más a menos fiable (E4-15):

1. Cuestionarios validados.
2. El comportamiento real: cómo reaccionó en las caídas, qué anuló y qué pidió.
3. Las conversaciones.

Cada cambio propuesto dice qué se dedujo y de dónde, y no se aplica sin confirmación. Una contradicción se pregunta. Bajar el riesgo es inmediato; subirlo pide segundo factor y espera (§6).

**La política personal es el contrato consigo mismo.** Se escribe en un momento tranquilo: qué hará ante caídas del 10, 20 y 30 %, qué dinero no tocará nunca y para qué invierte. Desde la Fase 3 incluye la caída tipo 2008 en euros que calcula M. El guardián la compara con cada orden del operador y, si la contradice, se la recuerda en N. No impide nada.

**Sin memoria libre.** El conversacional no recuerda conversaciones enteras. Lo que sabe del operador vive en tres sitios:

| Dónde | Qué guarda |
| --- | --- |
| SC-1 | Perfil, mandatos y política personal, versionados |
| Expedientes | Cada análisis, decisión y resultado |
| Diario de decisiones del operador | Lo que pidió, lo que decidió y por qué, resumido al cerrar cada conversación y confirmado por él |

Todo es exportable y borrable, y vive en la copia del operador. Sin temas personales ajenos a las finanzas, salvo que él los active.

**Seguridad del conversacional.** No lee noticias ni contenido externo directamente (eso es SC-11). No tiene herramientas para cambiar estado: solo propone al Orquestador, y lo que toca dinero se confirma en N. Una manipulación por texto puede como mucho producir una propuesta que el operador verá con las cifras de F.

## 8. El Orquestador: colas, presupuestos y reparto

Se conserva todo lo que ya hace:

- estados con transiciones permitidas;
- validación de encargos y sobres contra los sellos de K;
- idempotencia, caducidades e historial encadenado;
- fallo cerrado.

Se añaden cuatro cosas, todas en código y sin IA.

**1. Qué se analiza primero.** En la Fase 1, un orden fijo:

1. Protecciones, vencimientos y lo que piden F y H.
2. Aportaciones y reequilibrios.
3. Revisión de posiciones abiertas.
4. Peticiones del operador.
5. Oportunidades nuevas.

Dentro de las oportunidades nuevas, una puntuación sencilla [PROPUESTO]: importe que podría mover × mejora esperada frente a la sombra × probabilidad de cambiar una decisión, dividido por el coste estimado. Antes de usarla, se mide en el banco frente al orden de llegada.

**2. Cuánto presupuesto para cada cosa.**

- Se mantienen el tope por encargo y por día (P-07, D-05) y se añade el anual (E4-17).
- El presupuesto se reparte entre carteras según su mandato y, con el tiempo, según lo que I mida: euros de decisiones que cambiaron por cada euro de IA.
- La ruta determinista no consume presupuesto de IA y no se ve afectada.

**3. No repetir análisis.** Antes de encargar, el Orquestador consulta el registro de análisis vigentes (D-23). Si otra cartera ya tiene un análisis vigente del mismo activo con la misma fecha de corte y un nivel suficiente, se reutiliza.

**4. Conflictos entre carteras.** El código los detecta: apuestas opuestas, límites conjuntos o el mismo activo en dos libros (hoy con la comprobación de E y desde la Fase 3 con M). Primero manda el mandato de cada cartera. Si eso no lo resuelve, el conversacional lo plantea al operador con las cifras de cada opción.

## 9. El Broker frente a los bloques, N y los servicios comunes

| Quién | Relación con el Broker |
| --- | --- |
| A, B y C | Reciben encargos del Orquestador, nunca del conversacional directamente |
| D | Compara; el planificador le pide también comparar devolver deuda o aportar a un plan de pensiones (E4-16) |
| E | Dimensiona; los gestores le entregan las propuestas de su libro y el uso de la aportación |
| F | Controla todo plan; el Broker no puede pedir que relaje un límite, solo explicar por qué se aplicó |
| G | Único canal de órdenes; también registra las operaciones manuales que el operador declara |
| H | Sus alertas llegan al gestor del libro |
| I | Mide al Broker: valor del planificador, coste por decisión y el efecto de las intervenciones del operador |
| K y SC-11 | Datos y noticias le llegan ya limpios; el conversacional no lee fuentes externas |
| M | Riesgo en euros para explicar y para la política personal |
| N | Donde el operador ve y decide; el conversacional explica, N recoge la decisión |
| SC-1 | Perfil, mandatos y política personal |
| SC-3 (Motor) | Proyecciones del plan (D-29) y simulaciones del asesor de configuración |
| SC-9 (fiscalidad) | Vehículo fiscal, compensación de pérdidas e informe anual; reglas validadas por el asesor fiscal |

**La regla de fondo (D-23):** los datos entre bloques viajan por el Orquestador con contratos cerrados. El conversacional lo consulta todo para explicarlo, pero no transporta nada.

## 10. Precisión, consumo y orden

**Precisión: cómo se sabe que cada función acierta.**

| Función | Qué se mide | Quién |
| --- | --- | --- |
| Conversacional | Cifras correctas siempre (comprobación de N); calidad de las explicaciones en un conjunto dorado de preguntas; aspirante frente a titular para modelo e instrucciones | Banco de medida e I |
| Perfilador | Propuestas aceptadas y rechazadas; contradicciones encontradas | I |
| Planificador | Proyección frente a lo que pasó, cada año | I |
| Gestores | Encargos que no cambiaron ninguna decisión; coste y tiempo por decisión | I |
| Orquestador | La puntuación de prioridad frente al orden de llegada | Banco de medida |
| Guardián | Recordatorios mostrados y qué hizo después el operador | I |

**Consumo.** Se propone que el Broker no pase del 10 % del presupuesto de IA [PROPUESTO]. Para eso:

- **Contexto corto:** el conversacional carga un resumen de SC-1, el expediente del que se habla y las últimas entradas del diario de decisiones, nunca todo el historial.
- **Modelo según la tarea:** uno bueno para la revisión anual y las decisiones importantes; uno económico para resúmenes y textos de rutina.
- **Instrucciones en caché.**
- **Medido con un script,** como se hizo con el Bloque A.

El Orquestador, el guardián y casi todo el trabajo de los gestores gastan cero tokens.

**Orden:**

- **Fase 1:**
  - el Orquestador, que ya existe, con el orden fijo de prioridades y el registro de análisis vigentes;
  - un conversacional mínimo;
  - el asesor de configuración con su cuestionario y el perfil en SC-1;
  - el gestor de la cartera táctica de divisas en código.
- **Fase 2:**
  - el planificador: proyecciones (D-29), aportaciones, colchón, vehículo fiscal y camino de riesgo;
  - la política personal y el guardián;
  - el perfilador y el diario de decisiones;
  - la revisión anual.
- **Fase 3:** hibernación y persona de confianza, y el guardián con la cifra de M y dinero real.
- **Fase 4:** el gestor de trading.

## 11. Preguntas para el operador

Todas son [PROPUESTO]; ninguna se decide sin el operador.

1. **Siete funciones y como mucho tres agentes de IA,** con el perfilador y el asesor como modos del conversacional.
2. **Gestores de cartera en código,** con IA solo en excepciones.
3. **Prioridad de encargos:** orden fijo en la Fase 1; después, la puntuación por lo que puede cambiar una decisión, si gana en el banco.
4. **Tope de consumo del Broker:** el 10 % del presupuesto de IA.
5. **Memoria:** sin memoria libre; solo SC-1, expedientes y un diario de decisiones que el operador confirma, exportable y borrable.
6. **Planificador patrimonial en la Fase 2,** con deuda, planes de pensiones y vehículo fiscal, validado por un asesor fiscal (P-06).
