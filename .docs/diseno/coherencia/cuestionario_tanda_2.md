# Cuestionario de la tanda 2: parámetros de la Fase 1 (borrador de Claude)

De: Claude, 11-11-2026. Estado: **BORRADOR PARA EL OPERADOR**. Prepara la sesión de decisiones (T-57) para la tanda 2 de la pasada de coherencia (`.docs/diseno/coherencia/propuesta_claude.md`, §8) y las preguntas de la enmienda 5, parte 2 (`.docs/diseno/enmienda_5/propuesta_parte2_claude.md`, §9). No cambia ningún valor del sistema. Copia en el repositorio del documento que el operador tiene en Claude; las cifras son de una cartera de ejemplo, nunca las del operador.

## 1. Cómo se usa

Son **28 preguntas**: las 20 de la tanda 2 (los parámetros que se fijan durante la Fase 1, en simulado) y las 8 de la enmienda 5, parte 2. Ninguna hay que contestarla ahora. Mientras usted no conteste, el sistema usa la opción recomendada, marcada `[PROPUESTO]`, y no hay dinero real en juego.

- **Formato de cada pregunta** (D-44): de dos a cuatro opciones, la recomendada primero, y siempre «dígamelo con sus palabras». Lo que usted conteste con sus palabras se lo reformularía el asesor de configuración para confirmarlo.
- **Ejemplos en euros:** sobre una cartera de ejemplo de **20.000 €**. No son sus cifras: las suyas viven solo en su copia (SC-1), nunca en el repositorio.
- **Cuándo:** en la sesión de decisiones (T-57) o antes, cuando usted quiera. Puede contestar una sola sección y dejar el resto.
- **Asimetría** (§6): elegir una opción más prudente que la recomendada vale al momento; una menos prudente exige segundo factor y espera cuando haya dinero real.

Los valores salen de las propuestas de diseño de cada bloque y de los valores documentados del marco común (T-83). Donde no coinciden, lo digo en el §8.

No es asesoramiento de inversión: son valores de partida para probar el sistema en simulado.

## 2. El riesgo de cada cartera

### R1 · ¿Qué parte del tamaño óptimo quiere apostar?

Hay un tamaño de apuesta que hace crecer más la cartera (el de Kelly). Por encima, se crece menos y se puede perder; y como las ventajas casi siempre se sobreestiman, conviene quedarse por debajo. Lo usan D y E en trading y táctica, y en el largo plazo solo para las inclinaciones sobre el plan. Origen: propuestas de D (pregunta 3) y E (pregunta 1).

1. **Un cuarto, en las tres carteras** (recomendada). Se consigue el 44 % del crecimiento máximo con el 25 % de su oscilación. Si el tamaño óptimo de una operación fueran 4.000 €, se invierten 1.000 €. Solo sube cuando I demuestre que las estimaciones están bien calibradas.
2. **Un octavo.** Más prudente: el 23 % del crecimiento con el 12,5 % de la oscilación; 500 € en el ejemplo.
3. **La mitad.** El 75 % del crecimiento con el 50 % de la oscilación; 2.000 € en el ejemplo. Si la ventaja estaba sobreestimada al doble, ya se está en el tamaño óptimo real, sin margen.
4. Dígamelo con sus palabras.

### R2 · ¿Cuánto acepta perder en un año malo, en cada cartera?

Es el presupuesto de riesgo: E lo traduce en tamaños y en riesgo hasta los stops. Origen: propuesta de E (pregunta 2).

| Opción | Trading | Táctica | Largo plazo | En 20.000 € por cartera |
| --- | --- | --- | --- | --- |
| **1. Recomendada** | 10 % | 10 % | 25 % | 2.000 € · 2.000 € · 5.000 € |
| 2. Más prudente | 5 % | 5 % | 15 % | 1.000 € · 1.000 € · 3.000 € |
| 3. Menos prudente | 20 % | 15 % | 35 % | 4.000 € · 3.000 € · 7.000 € |
| 4. Dígamelo con sus palabras | | | | |

El largo plazo admite más porque tiene años para recuperarse y el camino de riesgo lo va bajando al acercarse cada objetivo. Un índice mundial ha caído más de un 30 % en un solo año (2008): con un 15 %, el largo plazo no podría estar entero en bolsa.

### R3 · ¿Acepta por escrito la caída tipo 2008 antes de invertir a largo plazo?

M calcula cuánto perdería su cartera de largo plazo en una crisis como la de 2008, y esa cifra se escribe en su política de inversión personal. Origen: propuesta de M (preguntas 3 y 4).

1. **Sí, con la cifra en euros que calcule el Motor para su cartera** (recomendada). Orientativo: en esa crisis un índice mundial llegó a perder cerca de la mitad desde su máximo; en 20.000 € sin camino de riesgo, del orden de 10.000 €. La cifra exacta la da el Motor.
2. Sí, pero con una cifra máxima que fijo yo: el plan base se ajusta para no pasarla.
3. No, solo quiero verla, sin firmarla.
4. Dígamelo con sus palabras.

La tolerancia de estrés por cartera se repasa cada año en la revisión guiada.

## 3. Los límites del control F, por cartera

F es código y ningún agente lo convence. Estos límites frenan **abrir o aumentar** riesgo; reducir, cerrar, proteger y reequilibrar hacia el plan no los pasan (tanda 1 y cambio 78). Origen: propuesta de F (preguntas 3 a 6) y valores del marco.

### F1 · ¿Qué pérdida frena las operaciones nuevas?

| Opción | Trading (día · semana) | Táctica (día · semana) | Largo plazo | En 20.000 € |
| --- | --- | --- | --- | --- |
| **1. Recomendada** | 2 % · 4 % | 2 % · 5 % | Solo frena las inclinaciones sobre el plan: 5 % en la semana | Trading: 400 € al día, 800 € a la semana |
| 2. Más prudente | 1 % · 2 % | 1 % · 3 % | 3 % en la semana | Trading: 200 € · 400 € |
| 3. Menos prudente | 3 % · 6 % | 3 % · 8 % | 8 % en la semana | Trading: 600 € · 1.200 € |
| 4. Dígamelo con sus palabras | | | | |

Al llegar, la cartera no abre nada hasta el día (o la semana) siguiente, y ese límite no se puede subir el mismo día (§6). Un límite global para todo el patrimonio prevalece sobre los de cada cartera.

### F2 · ¿Cuánto puede ir como máximo en una orden, en un día y en un activo?

1. **En porcentaje de cada cartera** (recomendada): por orden, el 10 %; por día, el 25 %; en un mismo activo, el 20 %. En 20.000 €: 2.000 €, 5.000 € y 4.000 €. En el largo plazo, la orden puede llegar a la aportación del mes aunque supere el 10 %, porque es el plan.
2. Más prudente: 5 %, 15 % y 10 % (1.000 €, 3.000 € y 2.000 €).
3. Solo los topes en euros del marco: 20.000 € por orden, 50.000 € al día y 30.000 € por activo. Con carteras pequeñas no frenan nada (§8).
4. Dígamelo con sus palabras.

### F3 · En táctica, ¿qué hace F si la tesis gira alrededor de un anuncio importante?

Hoy F evita abrir el día antes de un anuncio (bancos centrales, resultados) y desde el viernes a las 20:00 (UTC) hasta el lunes. En táctica muchas tesis existen precisamente por un anuncio.

1. **Reducir a la mitad** si el anuncio es el catalizador declarado en la tesis, y vetar en el resto (recomendada). Una posición de 2.000 € se queda en 1.000 €.
2. Reducir a un cuarto (500 €).
3. Vetar siempre, como en trading.
4. Dígamelo con sus palabras.

### F4 · ¿Cómo protegerse de un salto de precio que se salta el stop?

Un stop no protege si el precio abre muy lejos de él (un hueco). Se añade un límite por posición que supone un salto según el tipo de activo.

1. **Suponer el mayor hueco de los últimos 10 años en ese tipo de activo**, calculado por el Motor con datos de K, y que la pérdida con ese hueco no pase del 1 % de la cartera (recomendada). En 20.000 €, como mucho 200 € por posición si salta el hueco.
2. Lo mismo, con el 2 % de la cartera (400 €).
3. Sin límite adicional: solo el stop.
4. Dígamelo con sus palabras.

### F5 · ¿Cómo cuenta F un fondo cuya composición no conoce?

Para no concentrar sin querer (un indexado mundial tiene buena parte en dólares aunque cotice en euros), F mira dentro de los fondos. Hasta que K dé la composición:

1. **Contarlo entero en su divisa o región principal** (recomendada).
2. No admitirlo hasta tener su composición.
3. Contarlo repartido como un índice mundial.
4. Dígamelo con sus palabras.

## 4. La vigilancia de H

H vigila lo que ya está comprado. Salvo una regla numérica declarada de antemano (un stop), H **propone revisar, nunca vende** (§4.2). Origen: propuesta de H (preguntas 1 a 5).

### H1 · ¿Con qué pérdida pide revisar una posición?

1. **Dos veces la oscilación normal del activo en el plazo de la tesis** (recomendada). En una divisa principal que suele moverse un 2 % en un mes, avisa a −4 %; en una acción que se mueve un 8 %, a −16 %. En 2.000 €: 80 € y 320 €.
2. Una vez y media la oscilación normal: avisa antes y más a menudo.
3. Un −5 % fijo para todo, como hoy en el marco: avisa de más en lo volátil y tarde en lo tranquilo.
4. Dígamelo con sus palabras.

### H2 · ¿Cuándo se pausa una estrategia de trading?

Hoy se pausa sola si su rendimiento se sale del rango de su backtest (deriva).

1. **Además, si cae más que en el peor momento de su backtest** (recomendada).
2. Además, si cae una vez y media su peor momento: deja más margen.
3. Solo por deriva, como hoy.
4. Dígamelo con sus palabras.

### H3 · ¿Qué hace con una posición táctica que no se mueve?

El dinero parado también cuesta: podría estar en el benchmark.

1. **Pedir revisarla a la mitad del plazo de su tesis** si no se ha movido ni ha llegado su catalizador (recomendada). Con una tesis a seis meses, a los tres.
2. A los dos tercios del plazo.
3. Solo al vencer el plazo o a los 90 días, lo que llegue antes (como hoy).
4. Dígamelo con sus palabras.

### H4 · ¿Se sube el stop para asegurar beneficios?

1. **Solo en trading, como regla escrita de cada estrategia** (recomendada).
2. También en táctica, como propuesta que usted aprueba.
3. Nunca.
4. Dígamelo con sus palabras.

### H5 · ¿Se vigilan los fondos del largo plazo?

Por ejemplo, un fondo que cambia de gestor, sube comisiones o se separa de su índice.

1. **Sí, como propuesta de revisión, sin venta automática** (recomendada).
2. Solo en la revisión anual.
3. Dígamelo con sus palabras.

## 5. Medir y aprender

### M1 · ¿Cuántos pronósticos resueltos hacen falta para que el acierto de un autor cuente?

Un autor es un perfil de C, un modelo o una estrategia. Con pocos datos, su peso se acerca al de los demás (contracción). Origen: propuesta de I (pregunta 3), pendiente P-32.

1. **30 para empezar a pesar, con contracción fuerte hasta 100** (recomendada). Con 30 aciertos medidos ya se distingue algo del azar, pero poco.
2. 50 para empezar y contracción hasta 150: más prudente y más lento.
3. 20 y contracción hasta 60: más rápido y más expuesto a la suerte.
4. Dígamelo con sus palabras.

### M2 · ¿De qué tamaño el torneo de pronósticos?

Preguntas con fecha de resolución que responden todos los analistas, para medir su acierto antes de que se cierren las inversiones. Origen: propuesta de I (pregunta 4).

1. **Unas 200 preguntas al año** (recomendada): unas cuatro por semana, con un coste pequeño y constante que se mide en el banco de medida.
2. Unas 100: la mitad de coste y de muestra.
3. Unas 400: el doble de muestra y de coste.
4. Dígamelo con sus palabras.

### M3 · ¿Cuánto dura cada peldaño de la escalera de verificación?

Vale para estrategias, modelos, instrucciones y agentes (§7). Origen: propuesta de J (pregunta 2), pendiente P-33.

| Opción | En simulación | Con dinero real en pequeño, antes del primer tramo |
| --- | --- | --- |
| **1. Recomendada** | Al menos 3 meses y 50 operaciones | 3 meses |
| 2. Más prudente | 6 meses y 100 operaciones | 6 meses |
| 3. Más rápida | 2 meses y 30 operaciones | 2 meses |
| 4. Dígamelo con sus palabras | | |

### M4 · ¿Cuánto se prueba cada intermediario antes de confiarle dinero?

Primero su cuenta de demostración y después la lectura real con una clave de solo lectura. Origen: propuesta de SC-10 (pregunta 4).

1. **Cuatro semanas de demostración sin diferencias sin explicar y cuatro de lectura real con conciliación limpia** (recomendada).
2. Ocho y ocho semanas.
3. Dos y dos semanas.
4. Dígamelo con sus palabras.

## 6. Avisos, consumo y datos

### A1 · ¿Cuántos avisos importantes acepta recibir?

Si llegan demasiados, se dejan de leer. Origen: propuesta de N (pregunta 3).

1. **Como mucho uno de prioridad alta por semana, de media** (recomendada). Si se pasa, I revisa qué los dispara y le propone subir el umbral.
2. Como mucho dos por semana.
3. Sin límite: todos los que salten.
4. Dígamelo con sus palabras.

### A2 · ¿Cuánto del presupuesto de IA puede gastar el Broker en conversar?

Origen: propuesta del Broker Personal (pregunta 4).

1. **El 10 %** (recomendada). Con el tope anual por defecto (0,5 % de 20.000 €, 100 € al año; cambio 76), son 10 € al año.
2. El 5 % (5 € al año): conversaciones más cortas o con modelos más pequeños.
3. El 20 % (20 € al año).
4. Dígamelo con sus palabras.

### A3 · ¿Qué diferencia admite entre el tipo de cambio de su intermediario y el de la fuente de datos?

Por encima, K bloquea el dato para F y G y avisa. Origen: propuesta de K (pregunta 3).

1. **0,5 % en las divisas principales y 3 % en el resto** (recomendada). En un cambio de 2.000 €, 10 € y 60 €.
2. Un 3 % para todas, como hoy en el marco: deja pasar errores grandes en el euro-dólar.
3. 0,2 % y 1 %: más estricto; puede bloquear de más en divisas poco líquidas.
4. Dígamelo con sus palabras.

## 7. Las ocho preguntas de la enmienda 5, parte 2

Estas cambian la Constitución, así que además de contestarlas hay que ratificar su texto (borrador de la parte 2, §9). Están abiertas a lo que digan las revisiones de Astra.

### E1 · ¿La brújula como regla general? (cambio 56)

Cada pieza del robot debe demostrar cuánto ayuda a batir a la cartera sombra; si en dos revisiones seguidas no lo demuestra, se propone retirarla.

1. **Sí, con retirada propuesta tras dos revisiones sin aportar; decide usted** (recomendada).
2. Sí, pero tras tres revisiones.
3. No: solo informar.
4. Dígamelo con sus palabras.

### E2 · ¿Cuánto puede gastar el robot al año en IA y datos? (cambio 76)

1. **El 0,5 % del capital gestionado** (recomendada): 100 € al año con 20.000 €. Al llegar, modo sin IA.
2. El 0,25 % (50 € al año).
3. El 1 % (200 € al año): un 1 % de rentabilidad que el robot tiene que recuperar antes de aportar nada.
4. Dígamelo con sus palabras.

### E3 · ¿Puede el robot aplicar solo cambios menores de su código o instrucciones? (cambio 52)

1. **No, al principio todos los aprueba usted** (recomendada).
2. Sí, los menores (textos, documentación), con aviso.
3. Dígamelo con sus palabras.

### E4 · ¿El perfilador aprende también de sus conversaciones? (cambio 74)

1. **No: solo de cuestionarios y de su comportamiento real** (recomendada).
2. Sí, enseñándole cada cosa que deduzca y de dónde.
3. Dígamelo con sus palabras.

### E5 · ¿Cuándo entra el Estratega macro? (cambio 71)

1. **En la Fase 2, solo informando** (recomendada).
2. En la Fase 1, solo informando.
3. Más tarde, cuando el banco de medida lo justifique.
4. Dígamelo con sus palabras.

### E6 · ¿El Broker en siete papeles en lugar de tres? (cambio 73)

1. **Sí; en la Fase 1 solo el Orquestador, el conversacional, el asesor de configuración y el planificador de largo plazo** (recomendada).
2. Sí, pero con el perfilador y el asesor como modos del conversacional (como dice la propuesta del Broker), para tener como mucho tres agentes de IA.
3. No: los tres papeles de hoy.
4. Dígamelo con sus palabras.

### E7 · ¿Un servicio común nuevo para el conocimiento, SC-12? (cambio 57)

1. **Sí, mínimo en la Fase 1** (recomendada).
2. Sí, pero desde la Fase 2.
3. No: cada bloque guarda el suyo.
4. Dígamelo con sus palabras.

### E8 · ¿D compara entre clases de activo distintas? (cambio 79; tanda 3)

Por ejemplo, «¿este fondo o esta divisa?».

1. **Decidirlo antes de la Fase 2; hasta entonces, la regla de hoy** (recomendada).
2. Sí, ya: con estimaciones prudentes y rangos.
3. No: solo dentro de cada clase.
4. Dígamelo con sus palabras.

## 8. Discrepancias entre los diseños y el marco común

Al preparar el cuestionario he comparado lo que proponen los diseños con los valores que hoy usa el marco común (T-83, en QA). Hay seis diferencias. Ninguna es urgente, porque todo es simulado, pero conviene resolverlas antes de usar el marco con dinero real.

| # | Parámetro | Hoy en el marco | Lo que proponen los diseños | Pregunta |
| --- | --- | --- | --- | --- |
| 1 | Gasto máximo en análisis | 50 € al día (hasta unos 18.000 € al año) | Tope anual del 0,5 % del capital (100 € al año con 20.000 €) | E2 |
| 2 | Límites de F | En euros fijos: 20.000 € por orden, 50.000 € al día, pérdida de 2.500 € al día | En porcentaje de cada cartera, que también frenan con carteras pequeñas | F1, F2 |
| 3 | Alerta de pérdida de H | −5 % fijo | Dos veces la oscilación normal | H1 |
| 4 | Contraste de tipos de cambio | 3 % para todas las divisas | 0,5 % en las principales y 3 % en el resto | A3 |
| 5 | Benchmark de las tres carteras | Efectivo | Una cesta en la que se invierte de verdad (P5); efectivo solo si usted lo fija | Mandato (P-03) |
| 6 | Papeles de IA del Broker | — | La propuesta del Broker: como mucho tres agentes, con el perfilador y el asesor como modos del conversacional. La parte 2 de la enmienda: siete papeles separados | E6 |

La 1 es la más importante: con el valor de hoy, un mal día de análisis se gastaría la mitad del presupuesto anual propuesto.

La 6 es una incoherencia mía entre dos propuestas. Se la señalo a Astra en la revisión de la parte 2.

Cuando usted conteste, cambiar los valores del marco es tocar su código: lo haría en un ticket, con su autorización.

## 9. Lo que no entra en esta tanda

| Tanda | Cuándo | Qué se preguntará |
| --- | --- | --- |
| 3 | Al cerrar la Fase 1, antes de la 2 | Comparar entre clases (E8 la adelanta), planificador y vehículos fiscales, cosecha de pérdidas y planes de pensiones, esquema de SC-1, inventario y transición del patrimonio existente, perfiles de fondos de C |
| 4 | Antes del dinero real | Dónde corre el robot, bóveda de claves, topes de la clave en el intermediario, copias, carta de instrucciones, canal de avisos fuera del chat, M ligero, pantalla contra la venta de pánico, persona de confianza y plazo de hibernación |
| 5 | Fase 4 y siguientes | Investigador cuantitativo, capital del peldaño 3, motor de pruebas de robotTrading y mover capital entre estrategias |

**Lo personal no está aquí:** el importe de sus aportaciones, los meses del colchón, las fechas de sus objetivos y los valores de cada mandato se preguntan en su copia, con el asesor de configuración, y se guardan solo en SC-1.
