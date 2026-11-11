# Motor de cálculo (SC-3): cifras que se pueden comprobar (propuesta de diseño de Claude)

De: Claude, 11-11-2026. Estado: **PROPUESTA PARA DISCUTIR**. No hay nada que implementar: el operador está decidiendo la arquitectura de los bloques antes de construir (relevo de Astra, §0 bis). Copia en el repositorio del documento que el operador revisó con Claude.

## 1. Respuesta corta

El Motor calcula todas las cifras del robot. Los agentes solo las citan por su identificador (P3). La Constitución lo define como un servicio común que se entrega como un bloque (D-29): reproducible, cada módulo con su modelo y sus límites declarados, con cola de trabajos y caché, y que da distribuciones en lugar de predicciones exactas. Hoy hay dos piezas sueltas: el Motor del Bloque A, que sí calcula, y el registro del marco común (V0.33), que comprueba que las cifras citen un cálculo existente pero no calcula.

Idea central: **una cifra vale lo que su comprobación.** Se propone:

1. **Un solo Motor, por familias de módulos:** se une el cálculo de A al registro del marco y se añaden los módulos que piden los diseños de D a N, el Broker y SC-9.
2. **Cada módulo con su ficha:** modelo, versión, límites de validez, precisión, coste y casos de referencia. Fuera de sus límites, devuelve «no estimable», nunca un número.
3. **Precisión pedida, método más barato:** quien pide dice qué error tolera; el Motor usa una fórmula antes que una simulación y para al alcanzar ese error.
4. **Se mide si acierta:** las bandas del 90 % deben contener lo que pasa nueve veces de cada diez. I lo comprueba.
5. **F no depende del Motor:** calcula sus controles con su propio código (P2, P15).
6. **Cero tokens.**

## 2. Dónde gana o pierde rentabilidad el Motor

El Motor no busca rentabilidad: evita perderla por cifras malas y abarata el análisis.

| Fallo | Qué pasa | Qué cuesta |
| --- | --- | --- |
| Un agente escribe una cifra | Se inventa o se equivoca en una cuenta | Decisiones sobre números falsos (P3) |
| Modelo fuera de su validez | Suponer reparto normal en una crisis | Riesgo infravalorado justo cuando importa |
| Una cifra sin rango | «Rentará un 8 %» en lugar de «entre −5 % y +20 %» | Tamaños demasiado grandes |
| El mismo cálculo distinto en dos bloques | D y E usan volatilidades distintas | Decisiones incoherentes y difíciles de auditar |
| No reproducible | Repetir un análisis da otro número | No se puede saber si algo funcionó ni corregirlo |
| Lento o caro | Simular cuando bastaba una fórmula | Análisis que llegan tarde o no se hacen |
| Razonar cifras con IA | Un agente hace cálculos en texto | Tokens caros y errores |

El mayor ahorro no está en optimizar el Motor, sino en que calcule lo que hoy razonan los agentes (E4-07). La medición del Bloque A dio 77 llamadas y 1,66 millones de tokens de entrada por ciclo simulado, el 90 % en instrucciones; unas instrucciones más cortas, porque los números llegan ya calculados, ahorran en cada llamada.

## 3. Qué hay hoy y qué falta

**El Motor del Bloque A** (calcula):

- Catálogo de 81 fichas (V5.0), mapa de conocimientos y perfiles por tipo de activo.
- Código de unas 1.170 líneas. Tiene 17 manejadores, de los que 14 dan cifras citables: descriptiva, crecimiento anual, rentabilidad real, momento, volatilidad (simple, EWMA y GARCH), caídas, tendencia de Mann-Kendall, correlaciones y grupos, *carry* de divisas y *roll yield*.
- Una ficha conocida sin manejador responde «método no implementado»; una ajena al catálogo, «operación sin ficha».

**El registro del marco común** (V0.33, no calcula):

- Qué es un modelo declarado (versión, descripción y límites de validez).
- Qué es un artefacto: modelo, sello de K, semilla y huellas de entradas y resultado.
- Comprueba que cada cifra de un sobre cita un artefacto que existe y que no usa datos posteriores al corte.

**Cálculos dentro de la lógica de bloques del marco:** dimensionado (E), comparador (D), cartera sombra (I) y vigilancia (H). La decisión es del bloque y se queda en él; las piezas numéricas que reutilice otro bloque deberían venir del Motor.

**Falta:**

- Unir el cálculo de A con el registro del marco.
- Los módulos que piden los diseños.
- Precisión declarada y método más barato.
- Casos de referencia por módulo.
- Cola y caché reales.
- Medir si las bandas aciertan.
- El Documento 0 del Motor (D-29).

## 4. Catálogo de módulos

Doce familias que reúnen lo que ya calcula A y lo que piden los diseños. **Solo se construye un módulo cuando un Documento 0 lo declara y su fase llega** (E4-07): no las 81 fichas de golpe.

| Familia | Módulos | Lo piden | Hoy | Fase |
| --- | --- | --- | --- | --- |
| 1. Descriptiva y rentabilidad | Crecimiento anual, rentabilidad real, posición histórica | A, B, C, I | En A | 1 |
| 2. Volatilidad y oscilación | Volatilidad simple, EWMA y GARCH; caídas; oscilación normal por plazo | C, E, H, M | En A, salvo la oscilación por plazo de H | 1 |
| 3. Dependencia | Correlaciones en calma y en crisis, colas, grupos, número efectivo de apuestas, contribución al riesgo | D, E, M | En parte en A | 1 (concentración de E) y 3 (M) |
| 4. Tendencia y régimen | Mann-Kendall, momento, cambio de régimen | A, C, vigía | En parte en A | 1 y 2 |
| 5. Divisas y tipos | *Carry* y *carry* ajustado por volatilidad, *roll yield* | C-DIV, A de divisas | En A | 1 |
| 6. Decisión y tamaño | Kelly fraccional, crecimiento compuesto, combinar opiniones con el mercado (Black-Litterman), rentabilidad mínima neta | D, E | No | 1 |
| 7. Costes de ejecución | Diferencial, deslizamiento, impacto de órdenes grandes | G, E, D | No | 1 (simple) y 2 (impacto) |
| 8. Estrés y escenarios | Conjunto estándar de episodios, escenarios hipotéticos como choques, exposición abriendo fondos | D, M, J | No | 1 (episodios) y 3 (M) |
| 9. Simulación del plan | Proyecciones de Montecarlo (D-29) y optimización del plan a varios años | Planificador, asesor de configuración | No | 2 y 3 |
| 10. Evaluación | Atribución por etapa, rangos, años para probar ventaja, calibración, Sharpe deflactado, probabilidad de sobreajuste | I, J, SC-4 | No | 1 (calibración y sombra) y 4 (J) |
| 11. Fiscal | Optimización a varios años con las reglas de SC-9 | E, planificador | No | 2 |
| 12. Macro | Previsión de un dato antes de publicarse | Estratega macro, vigía | No | 2 |

**Quién mantiene cada módulo.** El bloque que lo pide es su propietario funcional: dice qué necesita y valida el resultado (M sus modelos de riesgo, I la evaluación). El Motor fija las reglas comunes (ficha, pruebas, registro y caché) y no acepta un módulo que no las cumpla.

**Lo que no es del Motor.** La lógica de decisión de cada bloque se queda en el bloque. Los controles de F tampoco: F calcula los suyos con su propio código (P2, P15), y si su cifra y la del Motor discrepan mucho, se avisa.

## 5. El recorrido de un cálculo

Diagrama del documento («Cada cifra sale sellada o no sale»):

1. **Petición:** el bloque dice la precisión que necesita y la fecha de corte.
2. **¿Ya calculado?** Si existe un artefacto con la misma huella, se reutiliza.
3. **¿Dentro de límites?** Si no, sale «no estimable» con el motivo.
4. **Método más barato:** fórmula, aproximación o simulación.
5. **Artefacto sellado:** huella, semilla y sello de K; versión, error y tiempo.
6. **El agente cita el identificador** y nunca escribe la cifra.
7. **El validador (V-26)** rechaza lo que no esté citado.

Si el cálculo ya existe con la misma huella, se reutiliza. Si no, la ficha del módulo decide si está dentro de sus límites: si no lo está, sale «no estimable» con el motivo; si lo está, el Motor usa el método más barato que da la precisión pedida, con datos de K, y sella el resultado. El agente solo cita el identificador, y el validador rechaza cualquier cifra sin él.

## 6. Las reglas de cada módulo

**La ficha.** Ningún módulo entra sin ella; amplía el «modelo declarado» del registro V0.33.

| Campo | Qué dice |
| --- | --- |
| Identificador y versión | Qué es y cuál está en uso |
| Modelo y supuestos | Qué hace y qué da por hecho; por ejemplo, que el reparto es normal |
| Límites de validez | Cuándo deja de valer: pocos datos, huecos, un régimen que rompe sus supuestos o un plazo fuera de rango |
| Entradas y salida | Qué datos de K usa, con su sello, y qué devuelve: una distribución o una banda, no un número suelto |
| Precisión y coste | Qué error puede garantizar y cuánto tarda |
| Casos de referencia | Resultados conocidos que tiene que reproducir: de un texto de referencia o de una biblioteca ya probada |
| Propietario funcional | El bloque que lo pidió y valida sus resultados |

**Siete reglas comunes.**

1. **Reproducible:** la misma entrada, semilla y versión dan el mismo resultado y la misma huella.
2. **Falla cerrado:** fuera de sus límites devuelve «no estimable» con el motivo, nunca un número aproximado (§10).
3. **Bandas, no puntos:** cada estimación lleva su rango; un dato exacto (un precio, una suma) lo dice.
4. **Sin datos del futuro:** nada posterior a la fecha de corte del encargo.
5. **Cambiar un método es un aspirante:** el nuevo solo sustituye al anterior si reproduce los casos de referencia y gana en el banco de medida.
6. **Cambiar una dependencia es una versión nueva:** una biblioteca actualizada vuelve a pasar todos los casos de referencia antes de usarse.
7. **Lo que no sabe, lo dice:** si no hay un modelo defendible, el módulo no existe; el agente no rellena el hueco con texto.

## 7. Rendimiento y coste

**Precisión pedida, método más barato (E4-07).** Quien pide un cálculo dice qué error tolera. El Motor elige por este orden:

1. fórmula cerrada;
2. aproximación con error conocido;
3. simulación que para en cuanto alcanza el error pedido.

Y recalcula solo lo que cambió. Cada artefacto registra el método usado, el error alcanzado y el tiempo.

**Caché por huella.** Entradas, versión del módulo y sello de K forman la huella. Si ya existe, se reutiliza, aunque lo pidiera otro bloque: la volatilidad que usan D, E y H es la misma. Un sello nuevo de K invalida lo que dependía de él.

**Cola con prioridades.** El Orquestador fija la prioridad (protecciones primero) y el presupuesto de tiempo por encargo (P-07). Los trabajos pesados, como las proyecciones del plan o las pruebas de J, van a horas tranquilas.

**Máquina potente solo si hace falta.** Se contrata cuando la cola mide esperas que retrasan decisiones, no antes. Antes de adoptar cualquier receta de velocidad, se mide en el banco propio: la lección de NautilusTrader fue que prometía multiplicar la velocidad por 10 y dio entre 0,26 y 1,05 veces.

**Bibliotecas.** Las que ya usa A (numpy, pandas, scipy, statsmodels y arch), con licencia libre y versiones fijadas.

**Coste visible.** Cada artefacto registra su tiempo de cálculo, e I lo suma a la economía del análisis (§10).

## 8. El Motor frente a los demás

| Quién | Relación con el Motor |
| --- | --- |
| Agentes de A, B y C | Piden cálculos y citan el identificador del artefacto; nunca escriben una cifra propia (P3) |
| D y E | Piden comparación, tamaño y rentabilidad mínima con la precisión que necesitan |
| F | No depende del Motor: sus controles van con su propio código y datos (P2, P15) |
| G y H | Costes de ejecución y oscilación normal por plazo |
| M | Propietario de los modelos de riesgo, que viven como módulos del Motor |
| I | Propietario de los módulos de evaluación; además mide si las bandas del Motor aciertan |
| J | Pruebas históricas y simulaciones pesadas, en la cola; usa los mismos módulos que producción |
| K | Única fuente de datos; cada artefacto cita su sello y no usa nada posterior al corte |
| SC-9 | Pone las reglas fiscales; el Motor solo optimiza con ellas |
| Broker | El planificador y el asesor de configuración piden proyecciones y simulaciones; el conversacional solo explica cifras ya calculadas |
| Orquestador | Fija prioridad y presupuesto de tiempo de cada cálculo |
| Validador del marco (V-26) | Rechaza un sobre que cite un artefacto inexistente o con datos posteriores al corte |

## 9. Precisión, consumo y orden

**Precisión: cómo se sabe que el Motor acierta.**

| Medida | Objetivo | Quién |
| --- | --- | --- |
| Casos de referencia | Todos aciertan en cada versión; si no, la versión no entra | Motor |
| Bandas que aciertan | Lo que pasa cae dentro de la banda del 90 % unas nueve veces de cada diez; si cae dentro mucho menos, las bandas son estrechas y el robot se confiará | I |
| Reproducibilidad | Una muestra de artefactos antiguos, recalculada cada mes, da la misma huella | Motor |
| Cifras sin artefacto en los sobres | Cero (V-26) | Validador |
| «No estimable» | Cuántas veces y por qué; si una familia lo da mucho, falta un módulo o datos | I |

**Consumo:** cero tokens. Solo tiempo de cálculo, registrado en cada artefacto.

**Orden:**

- **Fase 1:**
    - el Documento 0 del Motor (D-29) y la unión del Motor de A con el registro del marco;
    - las familias que ya existen (descriptiva, volatilidad y divisas);
    - la concentración mínima para E;
    - decisión y tamaño, con la combinación de opiniones y mercado (E4-08);
    - costes simples;
    - el conjunto estándar de episodios de estrés;
    - calibración y sombra para I;
    - caché y una cola sencilla.
- **Fase 2:** proyecciones del plan (D-29), impacto de órdenes grandes, optimización fiscal, régimen y macro.
- **Fase 3:** modelos de riesgo de M y optimización del plan a varios años.
- **Fase 4:** lo pesado de J, como la probabilidad de sobreajuste.
- **Máquina potente:** cuando la cola lo pida, medido.

## 10. Preguntas para el operador

Todas son [PROPUESTO]; ninguna se decide sin el operador.

1. **Un solo Motor:** se une el de A con el registro del marco, con el catálogo por familias, y solo se construye lo que un Documento 0 pide.
2. **Propietario funcional por módulo:** el bloque que lo pide lo valida, y el Motor pone las reglas comunes.
3. **Precisión pedida y método más barato,** con el coste registrado en cada artefacto.
4. **Medir si las bandas aciertan** como condición para que D y E confíen en un módulo.
5. **Máquina potente:** solo cuando la cola mida esperas que retrasan decisiones.
6. **F fuera del Motor** para sus controles, con aviso si sus cifras y las del Motor discrepan mucho.
