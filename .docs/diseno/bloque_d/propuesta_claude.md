# Bloque D: dónde rinde más el próximo euro (propuesta de diseño de Claude)

De: Claude, 11-11-2026. Estado: **PROPUESTA PARA DISCUTIR**. No hay nada que implementar: el operador está decidiendo la arquitectura de los bloques antes de construir (relevo de Astra, §0 bis). Copia en el repositorio del documento que el operador revisó con Claude.

Encargo del operador: «Quiero que sea un bloque que le permita al Broker Personal decidir entre varias opciones que considera interesantes. Quiero que analices qué es lo mejor para el robot investor. El objetivo principal del robot investor obviamente es que me ayude a maximizar la rentabilidad que consigo por cada euro invertido.» Y después: «también quiero obtener la máxima rentabilidad a corto plazo. Es decir, quiero que tomes en cuenta que el comparador me debe ser útil para todo tipo de carteras del portfolio».

## 1. Respuesta corta

D no debería ordenar candidatos, sino responder a una sola pregunta: **¿dónde hace crecer más esta cartera el próximo euro durante su horizonte, después de costes e impuestos, sabiendo lo que ya tiene y lo poco que se puede fiar de cada previsión?** La respuesta por defecto es «en el plan pasivo», y una opción solo la desplaza si la supera con margen incluso en su versión prudente.

La pregunta es la misma en las tres carteras del robot (trading, táctica y largo plazo, Constitución §7). Lo que cambia es el reloj: en trading se mide por semana, en la táctica por mes y en la de largo plazo por año. Por eso se propone **un solo comparador con un perfil de parámetros por cartera**, sacado de su mandato, y no tres comparadores distintos.

D reúne todas las opciones reales (los candidatos que llegan de C o las estrategias de J, reforzar lo que ya se tiene, cambiar una posición por otra y no hacer nada), las mide con la misma vara y entrega al Broker una **tabla de decisión**. Cada fila dice cuánto aporta la opción a la cartera por cada 1.000 € y periodo, con su rango y su riesgo. Todo lo calcula código, sin agentes: el Broker conversa con el operador sobre la tabla, pero no la escribe.

Esto cambia la primera versión de la propuesta. Un comparador que ordena candidatos uno a uno optimiza algo que no es su objetivo: puede elegir la opción con mejor puntuación aunque repita una apuesta que ya se tiene o aunque venderla luego cueste impuestos.

## 2. El objetivo bien definido

«Maximizar la rentabilidad por euro invertido» significa maximizar el **crecimiento compuesto** de la cartera por unidad de tiempo, neto de costes, impuestos e inflación, y no la rentabilidad media de cada apuesta. Vale igual a una semana que a diez años. La diferencia es la volatilidad: ganar un 50 % y después perder un 50 % deja 1.000 € en 750 €, aunque la media de las dos rentabilidades sea cero. A corto plazo pasa lo mismo en pequeño: ganar un 3 % una semana y perderlo la siguiente deja la cartera un 0,09 % por debajo, y en cien semanas eso se nota. Por eso, para el mismo rendimiento medio, crece más lo que oscila menos:

```
crecimiento compuesto ≈ rentabilidad media − ½ · varianza
```

Tres consecuencias para D:

- **Se mide a nivel de cartera.** Lo que importa es cuánto crece el total con la opción dentro, no la opción sola. Una opción buena que se mueve igual que lo que ya se tiene suma rentabilidad y también varianza.
- **Se mide en neto.** Una comisión o un impuesto se pierden seguro; la ganancia esperada, no. Cada venta para cambiar de idea tributa, así que rotar mucho resta rentabilidad por euro.
- **El punto de comparación es el plan pasivo.** La Constitución ya obliga a compararse siempre con una cartera sombra pasiva (P17) y a tratar la abstención como un resultado válido (P5). D usa esa misma referencia.

Este objetivo tiene un límite que no es de D: lo que el operador soporta perder por el camino. Ese freno lo pone su perfil de riesgo (SC-1), y los límites, F.

## 3. Qué decide de verdad el robot

La decisión real nunca es «cuál es la mejor de esta lista», sino «qué hago con este dinero». Las alternativas son siempre cuatro:

1. **No hacer nada nuevo:** el dinero va al plan pasivo de la cartera.
2. **Un candidato nuevo** que llega analizado de C (o, en trading, una estrategia validada por J).
3. **Reforzar una posición que ya se tiene**, si su tesis sigue viva.
4. **Cambiar una posición por otra**, vendiendo, con su coste fiscal, para financiar una opción mejor.

El comparador del marco común (`sistema_global/marco_comun_c/validador/comparador.py`, V0.35) hace bien una parte: no se cree lo que declara quien analiza (suelo de costes; riesgo = el peor entre escenario adverso, p05 y distancia al stop; confianza topada) y se abstiene si nada supera al benchmark. Le faltan tres cosas:

- **Mira cada candidato solo.** No sabe qué hay en cartera: no ve que dos opciones son la misma apuesta, ni que reforzar algo que ya se tiene puede ser mejor que abrir algo nuevo.
- **Se fija en la puntuación, no en el crecimiento.** Ordena por exceso de rentabilidad por unidad de riesgo de cada opción, que no es lo mismo que cuánto crece la cartera con ella dentro.
- **Confía igual en todos para siempre.** Los recortes de confianza son fijos. No aprende que un analista acierta más que otro, aunque el sistema lo vaya midiendo.

Además, la Constitución prohíbe hoy comparar por valor esperado entre clases de activo de distinta fiabilidad (regla 1 del §5). Es prudente, pero deja sin respuesta la pregunta más frecuente: ¿este fondo o esta divisa? Se propone otra forma de ser prudente que sí permite compararlas (pregunta 4).

## 4. Una sola vara para las tres carteras

Las tres carteras persiguen lo mismo, crecer lo máximo por euro frente a su benchmark, pero cada una gana y pierde por motivos distintos. El comparador es el mismo; el perfil de cada cartera le dice qué medir y con qué reloj.

|  | Trading | Táctica | Largo plazo |
| --- | --- | --- | --- |
| **Horizonte y reloj** | Días a semanas; € por 1.000 € **y semana** | Semanas a meses; **por mes** | Meses a años; **por año** |
| **Qué opciones compara** | Estrategias validadas por J y cuánto capital lleva cada una | Posiciones con tesis y catalizador; reforzar o cerrar antes | Asignación, rebalanceos, vehículo fiscal; reforzar o sustituir |
| **De dónde sale la estimación** | Del historial de la estrategia: su backtest en J, rebajado por cómo le va en real | Del sobre de C, rebajado por el acierto medido del perfil y el nivel que lo hizo | Del sobre de C y de las tasas base de largo plazo de cada clase de activo |
| **Lo que más pesa** | Costes por operación (diferencial, comisión, deslizamiento) y que la ventaja no se esté agotando | La probabilidad y la fecha del catalizador, y el coste de esperar | Impuestos, vehículo, diversificación y camino de riesgo |
| **Riesgo que cuenta** | Caída dentro del periodo, saltos de precio y operaciones abiertas a la vez que dependen de lo mismo | Peor escenario hasta el catalizador y distancia al stop | Caída de la cartera en estrés y su efecto en sus objetivos |
| **Freno a la rotación (D-25)** | Al mover capital entre estrategias; cada operación ya lo pasó al validarse | Mejora mayor que el doble de los costes de salir y entrar | Lo mismo, contando el impuesto de la venta |

### Comparar opciones de distinta duración

Una operación de dos semanas que promete un 2 % no equivale a un 68 % anual. Anualizar así supone que habrá otra igual de buena cada dos semanas y que ninguna fallará: infla justo lo que menos se sabe. D compara todas las opciones de una cartera **sobre la misma ventana**, la de su horizonte, y supone que el dinero que libera una opción corta vuelve al benchmark hasta el final. Cuando el Bloque I haya medido que esa cartera encuentra de verdad nuevas oportunidades con un ritmo y un acierto dados, D usará esa tasa medida en lugar del benchmark; nunca una supuesta.

### La rentabilidad a corto plazo, con los pies en el suelo

D persigue también la máxima rentabilidad a corto plazo en las carteras de trading y táctica, con la misma vara. Dos cosas que conviene saber:

- **A corto plazo manda el ruido.** En una semana, el resultado de una buena operación se parece mucho al de una mala. La rentabilidad a corto se consigue con muchas apuestas pequeñas e independientes, con una ventaja medida y costes bajos, y no eligiendo cada vez la que más promete.
- **Más rentabilidad a corto suele salir de más riesgo.** D no la compra subiendo el riesgo por encima del presupuesto del mandato. Ese freno lo pone el perfil, y la Constitución prohíbe subir el riesgo para recuperar (§7).

### Entre carteras

D compara dentro de cada cartera, con su mandato y su benchmark. Mover dinero de una cartera a otra es una decisión de mandato del operador (SC-1), con la vista global de E. Lo que sí hace D es informar: si una cartera tiene opciones claramente mejores que su benchmark y otra lleva meses sin ninguna, el Broker se lo enseña con cifras comparables, todas en € por 1.000 € y año, para que el operador decida si cambia el reparto.

## 5. Cómo construye D la tabla de decisión

Los pasos 2 a 5 toman sus parámetros del perfil de cada cartera (SC-1: reloj, costes, riesgo y benchmark); la puerta del paso 6 es la misma para las tres.

1. **Reunir las opciones de la cartera:** candidatos de C o estrategias de J, reforzar, sustituir y no hacer nada.
2. **Estimación prudente:** cada cifra se encoge hacia la tasa base de su clase, menos cuanto más ha acertado su autor según la calibración medida por I.
3. **Todo en neto:** costes de entrar y salir, deslizamiento e impuestos de esa cartera.
4. **Lo que aporta a la cartera:** crecimiento añadido junto a lo que ya hay (factores del sobre y escenarios de estrés), al tamaño de referencia que aplicaría E.
5. **La misma ventana para todas:** el horizonte de la cartera; lo que libera una opción corta vuelve al benchmark.
6. **Puerta: ¿el extremo bajo de su rango supera al plan pasivo?** Con el margen del freno a la rotación cuando hay que vender algo.
   - Una gana con claridad → **recomendar**.
   - Varias pasan y sus rangos se solapan → **decide el Broker** con el operador.
   - Ninguna pasa → **abstenerse** (el dinero va al plan pasivo).
7. **Tabla de decisión para el Broker** (CT-G-05): € por 1.000 € y periodo, rango, estrés, costes y solapes. Se congela en SC-4 y el Bloque I la mide al vencer.

Si una opción solo gana en su versión optimista, no desplaza al plan pasivo.

## 6. Qué hace ganar más por euro

Por orden de peso, de más a menos. Es un orden razonado a partir de lo que se sabe en finanzas, no una medición de este robot, que aún no tiene historial.

| # | Palanca | Por qué pesa tanto | Dónde vive en el diseño |
| --- | --- | --- | --- |
| 1 | **No equivocarse por exceso de confianza** | Las previsiones de rentabilidad tienen mucho ruido, y elegir «la mejor» premia sobre todo a la que más se ha sobreestimado. Es un resultado conocido: un optimizador amplifica los errores de sus entradas | Paso 2: estimación prudente, encogida hacia la tasa base |
| 2 | **Costes e impuestos** | Se pagan seguro, cada año y en cada venta. Rotar posiciones para perseguir pequeñas mejoras suele restar | Paso 3: todo en neto; cambiar una posición carga el impuesto de la venta |
| 3 | **El tamaño de cada apuesta** | Un buen candidato con demasiado peso hunde el crecimiento compuesto en una mala racha | E, con el mismo objetivo (sección 7) |
| 4 | **Diversificación de verdad** | Dos opciones que dependen de lo mismo son una sola apuesta con el doble de riesgo | Paso 4: aportación marginal a la cartera, con los factores del sobre |
| 5 | **Elegir la mejor entre las buenas** | Importa, pero menos de lo que parece cuando las cifras son ruidosas: entre opciones parecidas, la diferencia suele estar dentro del error | Paso 6: si los rangos se solapan, la decisión vuelve al Broker |

La lectura práctica: el mayor servicio que D puede prestar es **decir que no a menudo y con fundamento**, y concentrar el dinero solo donde hay una ventaja que el historial respalda. Por eso el plan pasivo es la opción por defecto.

## 7. D y E: elegir y dimensionar con el mismo objetivo

Qué opción conviene depende de cuánto se pone en ella: una opción excelente al 2 % de la cartera puede ser mala al 30 %. La Constitución separa a quien compara (D) de quien dimensiona (E), y esa separación tiene sentido para que nadie se proponga y se apruebe a sí mismo (P1). El riesgo está en que los dos usen criterios distintos y se contradigan.

Se propone mantenerlos separados, pero con **una sola función objetivo compartida** en el Motor (SC-3): el crecimiento compuesto neto esperado de la cartera, con la fracción de riesgo que fije el perfil.

- **D la usa con un tamaño de referencia**, el que E aplicaría por regla, para decidir qué opción merece el siguiente euro.
- **E la usa para afinar el tamaño** de la opción elegida dentro del mandato. Después, F comprueba los límites.

La forma teórica de este objetivo es el criterio de Kelly, que maximiza el crecimiento compuesto. Funciona mejor cuanto más se repite la apuesta, así que encaja especialmente en la cartera de trading, donde hay muchas operaciones pequeñas y la suerte se compensa. Aplicado entero es demasiado agresivo, porque se fía de unas previsiones que tienen error. Por eso se usa una fracción, distinta en cada cartera, y esa fracción es justo lo que el perfil de riesgo debe fijar.

La alternativa sería fundir D y E en un solo bloque de asignación. Sería más simple de razonar, pero rompería la separación de poderes y cambiaría la Constitución. No se recomienda.

## 8. Precisión y consumo

**Consumo: prácticamente cero.** D es código y no llama a ningún modelo. El único gasto de IA es que el Broker explique la tabla al operador, una conversación corta sobre cifras ya calculadas. Como referencia: un solo análisis N2 del Bloque B lee unos 990.000 tokens de entrada (T-68).

**Precisión: D aprende sin gastar más.** La clave está en el paso 2. Al principio no hay historial, así que D confía poco en cada previsión y casi siempre gana el plan pasivo. Es lo correcto: todavía nadie ha demostrado que acierte. Cada vez que vence una tesis, el Bloque I mide cuánto acertó quien la hizo (cada perfil de C y cada nivel de análisis; en trading, cada estrategia), y con esa medida D le da más o menos peso. Es la regla de que el peso se gana con pruebas (P19), aplicada de forma automática y auditable.

**Cómo se comprueba que D acierta.** Cada tabla de decisión se congela en SC-4. Al vencer el horizonte, el Bloque I compara:

- lo que dio la opción elegida;
- lo que habrían dado las descartadas;
- lo que dio el plan pasivo.

La respuesta que importa es si D ganó más por euro que no hacer nada. Como D es determinista, cualquier cambio de sus reglas se prueba gratis contra las tablas congeladas antes de usarlo (aspirante frente a titular, Bloque J). El límite es la muestra: harán falta muchas decisiones vencidas para que la medida signifique algo; en trading se llega antes.

## 9. Preguntas para el operador

Ninguna hay que contestarla ahora. Hasta que decida, cada una lleva un valor por defecto marcado [PROPUESTO], en simulado.

1. **El objetivo.** ¿Vale «crecimiento compuesto neto por cartera y por periodo, frente a su benchmark» como la única vara de D en las tres carteras?
2. **El reparto entre carteras.** Se propone que lo fije el operador en los mandatos y que D solo informe cuando una cartera tenga opciones claramente mejores que otra. ¿O debe D proponer mover dinero de una a otra?
3. **La fracción de riesgo de cada cartera.** Es la fracción de Kelly que usan D y E. Se propone empezar baja y en simulado, y fijarla en el perfil (SC-1).
4. **La regla 1 del §5.** Hoy prohíbe comparar por valor esperado entre clases de activo de distinta fiabilidad. Se propone cambiarla para permitirlo con estimaciones prudentes y rangos. Es un cambio de la Constitución.
5. **Reforzar y sustituir.** ¿Incluir siempre como opciones reforzar lo que ya se tiene y cambiar una posición por otra, y en trading mover capital entre estrategias?
6. **D y E.** ¿Separados, con la misma función objetivo, como se propone? ¿O fundidos en un solo bloque?
7. **El peso por historial (P19).** ¿Cuántas tesis vencidas hacen falta antes de que el acierto de un autor cuente? En trading se llega antes, porque hay muchas más operaciones.
8. **El dinero que se libera.** Se propone suponer que vuelve al benchmark hasta que I mida una tasa real de reinversión en esa cartera.
