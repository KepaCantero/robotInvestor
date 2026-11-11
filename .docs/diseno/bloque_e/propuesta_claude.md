# Bloque E: cuánto poner en cada sitio (propuesta de diseño de Claude)

De: Claude, 11-11-2026. Estado: **PROPUESTA PARA DISCUTIR**. No hay nada que implementar: el operador está decidiendo la arquitectura de los bloques antes de construir (relevo de Astra, §0 bis). Copia en el repositorio del documento que el operador revisó con Claude. Va con la de D (`.docs/diseno/bloque_d/propuesta_claude.md`), porque comparten objetivo.

Objetivo del operador: maximizar la rentabilidad por euro invertido, también a corto plazo, con un diseño útil para las tres carteras (trading, táctica y largo plazo).

## 1. Respuesta corta

D decide qué opción merece el próximo euro. E decide **cuántos euros**, y cómo encaja cada posición con todo lo demás. Es la decisión que más pesa en la rentabilidad por euro: con la misma ventaja, apostar la mitad de lo debido pierde poco crecimiento, y apostar el doble lo pierde todo.

Se propone que E sea código determinista, sin agentes, con el mismo objetivo que D (crecimiento compuesto neto de cada cartera) y una regla de fondo: **dimensionar sobre todo con lo que se puede estimar bien, el riesgo, y muy poco con lo que no, la rentabilidad esperada.** E trabaja en tres capas:

1. **El plan base** de cada cartera: los pesos del mandato, que se mantienen con las aportaciones y con bandas, cuidando los impuestos.
2. **Las posiciones activas** que llegan de D o de J: cada una recibe una fracción prudente de lo que justificaría su ventaja, topada por el riesgo hasta su stop o por su volatilidad.
3. **La vista global**: el riesgo total frente al presupuesto, los conflictos entre libros, las apuestas que dependen del mismo factor y el efectivo.

El E que hay hoy en el marco común (V0.10, `sistema_global/documentos_0/V0.10_E_dimensionado.md`) hace bien una pieza: el tamaño por distancia al stop, preguntando los topes a F para que nunca discrepen. Es la base del trading y se conserva. Le falta casi todo lo demás.

## 2. Por qué el tamaño es la palanca que más pesa

Para una apuesta con ventaja, el crecimiento depende del tamaño de forma muy asimétrica. Hay un tamaño que lo maximiza (el de Kelly); por debajo se gana algo menos, y por encima mucho menos, hasta perder:

| Tamaño, en fracciones del de Kelly | Crecimiento sobre el máximo | Volatilidad sobre la del tamaño de Kelly |
| --- | --- | --- |
| Un cuarto | 44 % | 25 % |
| La mitad | 75 % | 50 % |
| El tamaño de Kelly | 100 % | 100 % |
| Una vez y media | 75 % | 150 % |
| El doble | 0 % | 200 % |
| Más del doble | Negativo: la cartera se encoge | Más del 200 % |

Las cifras salen de la aproximación del crecimiento compuesto (g = f·μ − ½·f²·σ², con f la fracción del tamaño de Kelly μ/σ²), con una ventaja conocida. Dos lecturas:

- **Apostar de menos es barato; apostar de más es carísimo.** La mitad del tamaño óptimo da tres cuartos del crecimiento con la mitad de oscilación.
- **La ventaja nunca se conoce.** Si se sobreestima al doble, el tamaño «de Kelly» calculado es en realidad el doble del bueno, y el crecimiento esperado es cero. Como sobreestimar es lo normal, una fracción prudente es lo que maximiza el crecimiento real.

De ahí la regla de fondo: la volatilidad y las correlaciones se estiman bastante bien con datos recientes; la rentabilidad esperada, muy mal. E se apoya sobre todo en el riesgo y usa la rentabilidad estimada solo para inclinar el tamaño, con una fracción pequeña y la estimación prudente que ya calcula D.

## 3. Qué decide E de verdad

Según la Constitución (§2 y §7), E recibe cinco tipos de encargo:

1. **Una propuesta nueva** (CT-G-06), de D a través del Broker o del gestor: cuánto, de dónde sale el dinero y cómo encaja.
2. **Una señal de una estrategia activa de J**, por la vía sistemática: tamaño por regla, sin LLM.
3. **La aportación mensual**: reequilibrar comprando lo que está por debajo de su peso, antes que vender lo que está por encima.
4. **La deriva**: un peso fuera de su banda, una volatilidad que cambia, el camino de riesgo que baja un escalón.
5. **La vista global**: riesgo total, conflictos entre libros, concentración por factor, efectivo y la propuesta de reparto entre carteras, que aprueba el operador.

El E de hoy cubre el primer paso del segundo tipo. Le falta:

- **Todas las posiciones arriesgan lo mismo.** La ventaja no influye en el tamaño.
- **Sin stop no sabe dimensionar.** Un fondo indexado de largo plazo no tiene stop: ahí el tamaño sale de la volatilidad, la caída en estrés y el peso del mandato.
- **Dimensiona cada posición sola.** No suma el riesgo abierto ni ve que diez posiciones pequeñas son una sola apuesta grande si dependen del dólar.
- **No mantiene la cartera.** No hay reequilibrio, aportaciones, bandas, impuestos, camino de riesgo ni vista global.

## 4. Una sola lógica para las tres carteras

|  | Trading | Táctica | Largo plazo |
| --- | --- | --- | --- |
| **Qué dimensiona** | El capital de cada estrategia y el riesgo de cada operación | Cada posición con tesis | Los pesos del plan base y pequeñas inclinaciones |
| **Regla de tamaño** | Cada operación: un porcentaje fijo del capital de su estrategia hasta el stop (la regla de hoy). Cada estrategia: una fracción de Kelly sobre su ventaja medida en real | Una fracción de Kelly sobre la estimación prudente de D, topada por la pérdida hasta el stop | Los pesos del mandato; una inclinación solo con ventaja medida y limitada por lo que añade al riesgo |
| **Riesgo que vigila** | El riesgo abierto total (suma de pérdidas hasta los stops) y los saltos de precio | Pérdida hasta el stop y escenario adverso hasta el catalizador | Volatilidad y caída en estrés de la cartera entera; no hay stops |
| **Cuándo reequilibra** | Al cerrar operaciones y al revisar el capital de cada estrategia | Cuando cambia la tesis o la volatilidad | Con cada aportación, y cuando un peso sale de su banda |
| **Lo que más cuesta** | Deslizamiento y liquidez | Entrar o salir a destiempo | Los impuestos de vender |

- **El presupuesto de riesgo manda sobre la suma.** E reparte el presupuesto de riesgo del mandato entre posiciones y nunca lo supera. Si la nueva no cabe, desplaza a la peor de las que hay (lo compara D) o espera.
- **Abstenerse es estar en el benchmark, no en efectivo** (P5). Lo que no está en posiciones activas se queda en el plan base.

## 5. El ciclo de E

Entradas: propuesta de D (CT-G-06), señal de J, aportación mensual, deriva o revisión. Todas recorren los mismos pasos, con los parámetros del perfil de la cartera (SC-1: presupuesto de riesgo, fracción de Kelly, bandas, camino de riesgo):

1. **Estado y presupuesto:** libro de G, precios de K, presupuesto de riesgo del mandato y lo ya usado.
2. **Tamaño de cada posición:** fracción de Kelly sobre la estimación de D, topada por el stop o la volatilidad. Es el único paso que usa la rentabilidad estimada.
3. **Encaje en la cartera:** factores comunes, conflictos entre libros y bandas del plan base.
4. **Cómo y cuándo comprar o vender:** impuestos (FIFO, regla de los dos meses), liquidez y órdenes escalonadas.
5. **Topes de F:** E se los pide a F y redondea hacia abajo, como hoy; nunca pueden discrepar.

Salidas: el plan por libro (CT-G-07), que F aprueba, reduce o veta y G ejecuta; y la vista global, a la consola (N), con la propuesta de reparto entre carteras que aprueba el operador.

## 6. Qué hace ganar más por euro al construir la cartera

| # | Palanca | Por qué pesa | Dónde vive en el diseño |
| --- | --- | --- | --- |
| 1 | **No apostar de más** | Por encima del tamaño óptimo el crecimiento cae deprisa, y con ventajas sobreestimadas es fácil pasarse sin saberlo | Paso 2: fracción de Kelly sobre la estimación prudente |
| 2 | **Tamaño según el riesgo, que se conoce** | La volatilidad se estima mucho mejor que la rentabilidad | Pasos 1 y 2: presupuesto de riesgo, tamaño por stop o volatilidad |
| 3 | **Diversificación de verdad** | En las crisis las correlaciones suben justo cuando más duele | Paso 3: factores comunes, con correlaciones de periodos de tensión |
| 4 | **Mantener la cartera barata** | Reequilibrar con aportaciones y por bandas evita ventas e impuestos | Paso 4 y el ciclo de la aportación mensual |
| 5 | **Estar siempre invertido en algo útil** | El efectivo parado no rinde | Regla del benchmark (P5) |
| 6 | **Comprar y vender sin mover el precio** | En trading y en activos poco líquidos, el deslizamiento se come la ventaja | Paso 4: órdenes escalonadas |

En España, al vender parte de una posición se considera vendido lo primero que se compró (FIFO): E no elige el lote, pero sí qué posición reducir y cuándo, y puede compensar ganancias con pérdidas respetando la regla de los dos meses. Esas reglas las codifica SC-9 y las valida un asesor (P-06).

## 7. E frente a D, F, M, H y G

| Bloque | Qué hace | Relación con E |
| --- | --- | --- |
| **D** | Elige qué opción merece el siguiente euro, al tamaño de referencia de E | Misma función objetivo del Motor (SC-3) y misma estimación prudente. E no vuelve a comparar |
| **E** | Decide cuánto, de dónde sale el dinero y cómo encaja todo; propone el reparto entre carteras | Emite CT-G-07 y la vista global |
| **F** | Control independiente con límites nominales en euros | E le pide los topes antes de proponer; F calcula su propia concentración |
| **M** (Fase 3) | Exposición, correlación y escenarios adversos | Asesora a E; hasta entonces E hace la comprobación mínima de factores (D-25) |
| **H** | Vigila cada posición y sus condiciones de salida | Las salidas por tesis son de H y el Broker; E solo ajusta tamaños por razones de cartera |
| **G** | Único canal de órdenes, conciliación y libro | Ejecuta el plan aprobado, escalonado si E lo pide |

- **E y H.** Cerrar porque la tesis ya no vale es de H y del Broker. Reducir porque la posición creció demasiado o porque la cartera debe bajar riesgo es de E.
- **E y F.** E propone dentro de los topes; F los vuelve a comprobar con precios reales y nunca corrige el tamaño al alza.

## 8. Precisión y consumo

**Consumo: cero.** E es código. La vía sistemática (J → E → F → G) ya lo exige.

**Precisión: se puede probar con datos históricos de verdad.** Las reglas de E no usan ningún LLM, así que no sufren la trampa de que los agentes ya conocen el pasado (§7, escalera de verificación). Se prueban sobre años de precios de K, con costes e impuestos realistas.

Qué mide I:
- si el riesgo real de cada cartera se parece al presupuesto (ni mucho más ni mucho menos);
- si las caídas reales quedan dentro de lo que el mandato acepta;
- cuánto costaron los reequilibrios;
- si la cartera creció más que la cartera sombra pasiva después de todo eso (P17).

Qué datos necesita E que hoy no existen:
1. Volatilidades y correlaciones por activo, incluidas las de periodos de tensión, servidas por K con fecha de corte.
2. Los factores comunes de cada posición, que el sobre de C hoy no declara de forma uniforme.
3. La ventaja medida en real de cada estrategia de J y la calibración por autor de I que ya pide D.
4. Un modelo de costes por intermediario e instrumento, y las reglas fiscales de SC-9.

## 9. Preguntas para el operador

Ninguna hay que contestarla ahora. Hasta que decida, cada una lleva un valor por defecto marcado [PROPUESTO], en simulado.

1. **La fracción de Kelly de cada cartera** (la misma pregunta que en D). Se propone empezar por un cuarto en las tres y subirla solo cuando I demuestre que las estimaciones están bien calibradas.
2. **Cómo expresar el presupuesto de riesgo.** Se propone «cuánto acepto perder en un año malo», en euros o en porcentaje, una cifra por cartera; E lo traduce a volatilidad y riesgo hasta los stops.
3. **Ajustar la exposición a la volatilidad**, sin pasar nunca de los pesos del mandato. Se propone activarlo en trading y táctica, y no en el plan base de largo plazo.
4. **Un freno por caída.** Se propone solo en trading, donde la caída puede indicar que la ventaja se agotó; en largo plazo manda el camino de riesgo.
5. **Las bandas de reequilibrio del largo plazo.** Se proponen anchas, apoyadas en las aportaciones.
6. **Mover capital entre estrategias de trading:** ¿por regla dentro de unos límites, o con aprobación cada vez? Depende del nivel de autonomía (§6).
7. **Frecuencia de la propuesta de reparto entre carteras.** Se propone solo en la revisión anual guiada, salvo que una cartera se quede sin margen.
