# Entrada del dinero existente: pasar al robot sin pagar de más (propuesta de diseño de Claude)

De: Claude, 11-11-2026. Estado: **PROPUESTA PARA DISCUTIR**. No hay nada que implementar: el operador está decidiendo la arquitectura de los bloques antes de construir (relevo de Astra, §0 bis). Copia en el repositorio del documento que el operador revisó con Claude. Nada de esto es asesoramiento fiscal: cada regla la valida el asesor (P-06).

## 1. Respuesta corta

El robot está diseñado para dinero que entra, no para el que el operador ya tiene: fondos, acciones, depósitos, planes de pensiones o productos de su banco. El primer día hay que decidir qué se queda, qué se mueve sin pagar impuestos y qué se vende. Nadie lo tiene asignado. Es donde más fácil es pagar impuestos y comisiones de más, o vender todo de golpe en mal momento.

Idea central: **mover antes que vender, y vender solo lo que compense.** Se propone:

1. **Un inventario completo,** incluido lo que el robot no gestionará (vivienda, plan de empresa, depósitos), para que el planificador vea todo el patrimonio.
2. **Una decisión por posición,** en este orden:
    1. dejarla fuera (colchón, productos que no conviene tocar);
    2. mantenerla si encaja;
    3. traspasarla sin tributar si es un fondo o un plan de pensiones;
    4. trasladar los valores a la nueva entidad sin venderlos;
    5. vender solo si compensa después de impuestos, empezando por lo que tiene pérdidas.
3. **Un único expediente de transición,** en L1: cada orden la aprueba el operador, con el impuesto y el coste de cada paso a la vista.
4. **De golpe o por tramos,** elegido por el operador con las cifras de las dos opciones delante.

## 2. Dónde se gana o pierde dinero en la transición

| Error | Ejemplo | Qué cuesta |
| --- | --- | --- |
| Vender para recomprar algo parecido | Reembolsar un fondo con ganancias para comprar un indexado | El impuesto de la ganancia, que un traspaso habría diferido |
| Vender acciones solo para cambiar de entidad | Vender en el banco y recomprar en el intermediario nuevo | Impuesto y comisiones; trasladar los valores es neutro fiscalmente |
| Ignorar las comisiones de salida | Trasladar valores sin preguntar | De media un 0,4 % por tipo de valor, y hasta un 1 % en acciones extranjeras, según la OCU |
| Desperdiciar pérdidas | Vender primero lo que gana | Pagar impuestos que una pérdida habría compensado |
| Rescatar productos con penalización | Cancelar un depósito o un seguro antes de tiempo | Penalizaciones y, en algunos seguros, impuestos |
| Tocar el colchón | Invertir el dinero de imprevistos | Vender en el peor momento cuando haga falta |
| Entrar en el peor momento | Invertir todo justo antes de una caída | Arrepentimiento y riesgo de abandonar el plan |

Sobre el último punto, un estudio de Vanguard de 2023 sobre el índice mundial MSCI World (1976–2022) muestra que invertir de golpe ganó a repartir la entrada en tres meses en un 68 % de los casos, medido a un año. Por tramos se gana menos de media, pero se reduce el arrepentimiento, que es lo que hace abandonar un plan. Fuentes: [Vanguard](https://corporate.vanguard.com/content/dam/corp/research/pdf/cost_averaging_invest_now_or_temporarily_hold_your_cash.pdf) y [OCU](https://www.ocu.org/organizacion/prensa/notas-de-prensa/2025/traspasoacciones201125).

## 3. Qué hay hoy y qué falta

**Decidido:**

- El colchón vive fuera del robot (D-32).
- Las aportaciones reequilibran comprando lo que está por debajo de su peso (§7).
- Vehículo fiscal en la decisión (D-31).
- Freno a la rotación con impuestos (D-25).
- Operaciones manuales declaradas (CT-G-14).
- La sombra arranca con los mismos aportes que la cartera real.
- Los diseños de SC-9 (lotes, compensación, traspasos) y del Broker (planificador) dan las piezas.

**Falta:**

- El inventario de lo que ya se tiene, con su fecha y precio de compra.
- El árbol de decisión por posición.
- El orden y el ritmo de la transición.
- Cómo se registran las posiciones que el robot no gestionará.
- Desde cuándo empieza a contar la sombra si la transición dura meses.

## 4. El inventario

El operador lo rellena con el Broker en el cuestionario inicial, con los extractos de sus entidades. **Cada posición lleva fecha y precio de compra:** sin ellos no se puede calcular el impuesto.

| Tipo | Cómo se trata | A validar con el asesor |
| --- | --- | --- |
| Cuenta corriente y colchón | Fuera del robot; solo se registra que existe y cuántos meses cubre | — |
| Depósito a plazo | Fuera hasta su vencimiento; después, entra como aportación | Penalización por cancelar |
| Fondos de inversión | Mantener si encajan; si no, traspaso al fondo objetivo sin tributar | Que el fondo destino sea traspasable |
| Planes de pensiones | Traspaso a otro plan si el actual es caro; no se rescata | Límites y fiscalidad del rescate |
| Acciones y ETF | Mantener si encajan; trasladar los valores sin venderlos si cambia de entidad; vender solo si compensa | Comisión de salida; regla de recompra |
| Seguros de ahorro y productos complejos | Normalmente fuera hasta su vencimiento | Coste de rescatar |
| Vivienda, plan de empresa y otros | Fuera; se registran para que el planificador vea el patrimonio entero | — |
| Deudas | Se registran: el planificador compara devolver frente a invertir | Interés y deducciones |

Lo que queda fuera se registra en SC-1 como **posición externa**: cuenta para el plan y el riesgo total (M), pero el robot no la opera.

## 5. La decisión para cada posición

Diagrama del documento («Mover antes que vender, y vender solo lo que compense»). Cada posición baja por las preguntas hasta su primera salida:

1. ¿Colchón o producto a no tocar? → **Fuera del robot** (posición externa en SC-1).
2. ¿Encaja en el plan? → **Mantener** (trasladar sin vender si cambia de entidad).
3. ¿Fondo o plan de pensiones? → **Traspaso sin tributar** al fondo o plan objetivo.
4. ¿Tiene pérdidas? → **Vender primero:** sus pérdidas compensan ganancias.
5. ¿Compensa tras impuestos? → **Vender**, repartiendo entre años si la ganancia es grande.
6. Si no compensa → **Mantener hasta que compense** (freno a la rotación, D-25).

Vender es lo último y solo si compensa después de impuestos y comisiones; si no, se mantiene, y el freno a la rotación vuelve a mirarla con cada aportación.

## 6. El plan de transición

**Orden de los pasos.**

1. **Primero lo que no tributa:** traspasos entre fondos y entre planes de pensiones, y traslados de valores a la entidad elegida.
2. **Después, las ventas con pérdidas,** para tener pérdidas que compensen. Se respeta la regla de recompra: no se recompra lo mismo en dos meses; se compra algo parecido pero no homogéneo.
3. **Al final, las ventas con ganancias** que compensen después de impuestos. Si son grandes, se reparten entre dos ejercicios para usar el tramo bajo.
4. **El dinero liberado y el efectivo nuevo** se invierten según el plan objetivo.

**De golpe o por tramos.** El operador elige con las cifras de las dos opciones delante, calculadas por el Motor y M:

- **De golpe:** lo que se espera ganar de media y lo que se perdería en euros si llega una caída tipo 2008 justo después.
- **Por tramos** (por ejemplo, en seis meses [PROPUESTO]): cuánto se espera dejar de ganar de media y cuánto menos se perdería en ese mismo caso.

Si la política personal dice que una caída justo después de entrar le haría abandonar, se recomiendan los tramos: un plan que se abandona rinde menos que uno algo peor que se mantiene.

**Lo que no se toca.** Una posición que encaja en el plan se queda tal cual, aunque no sea exactamente la que el robot elegiría. El freno a la rotación (D-25) se aplica también aquí: solo se cambia si la mejora supera el coste con margen.

**La sombra.** Arranca con el mismo patrimonio y el mismo calendario de entradas, para que la comparación de I sea justa desde el primer día.

## 7. Quién hace qué

| Quién | Qué hace en la transición |
| --- | --- |
| Broker conversacional | Recoge el inventario en el cuestionario inicial y explica cada paso |
| Planificador | Fija el plan objetivo y el orden, y compara devolver deuda frente a invertir |
| SC-9 | Impuesto de cada paso, pérdidas aprovechables, regla de recompra y reparto entre ejercicios |
| E y D | Qué posiciones encajan en el plan y cuáles se cambian (freno a la rotación) |
| M | Riesgo del patrimonio entero, posiciones externas incluidas, y la caída tipo 2008 de cada opción |
| F | Controla cada orden como cualquier otra |
| G | Ejecuta en L1, registra traspasos y traslados, y carga en el libro fiscal los lotes con su fecha y precio de compra |
| N | Muestra el expediente de transición como una lista de pasos, con el impuesto y el coste de cada uno |
| Operador | Aprueba cada paso y hace los traspasos y traslados que la entidad exija pedir en persona |
| I | Arranca la sombra y mide el coste total de la transición |

## 8. Precisión y orden

**Qué se mide:**

- impuestos y comisiones pagados en la transición, frente a vender todo y recomprar;
- tiempo hasta llegar a la cartera objetivo;
- distancia final a esa cartera;
- lotes cargados sin fecha o sin precio de compra (objetivo: cero).

**Consumo:** casi todo es cálculo. La IA solo interviene en el cuestionario y en las explicaciones.

**Orden:**

- **Fase 2:** el inventario, las posiciones externas en SC-1 y el plan de transición en simulación, para ver el resultado antes de mover nada. Pueden ejecutarse a mano los pasos que no dependen del robot, como los traspasos entre fondos.
- **Fase 3:** el expediente de transición real, en L1, paso a paso.

## 9. Preguntas para el operador

Todas son [PROPUESTO]; ninguna se decide sin el operador.

1. **Mover antes que vender,** con el orden del §6.
2. **Posiciones externas** registradas en SC-1 para el plan y el riesgo, sin que el robot las opere.
3. **De golpe o por tramos:** decidirlo con las cifras de las dos opciones, con los tramos como opción por defecto si su política personal teme una caída justo después de entrar.
4. **Repartir las ganancias grandes entre dos ejercicios** cuando el ahorro compense la espera.
5. **Simular la transición en la Fase 2** antes de mover dinero.
