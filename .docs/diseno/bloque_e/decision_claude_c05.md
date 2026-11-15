# Bloque E: decisión de Claude sobre la revisión C-05 de Astra y diseño de construcción

De: Claude, 15-11-2026. Responde a la revisión de Astra `revision_astra.md` (base `9017e87`) sobre mi propuesta `propuesta_claude.md`, ambas en esta carpeta, por encargo del operador del mismo día: decidir qué entra y qué no, añadir mejoras y dejar el diseño listo para cuando se construya. Va con la decisión de D (`.docs/diseno/bloque_d/decision_claude_c04.md`), porque D y E comparten objetivo y se cierran entre sí.

Estado: **DISEÑO ESTABLECIDO**, a falta de las decisiones del operador del §6. No se construye hasta que el operador lo ordene. Al construir, este documento manda sobre la propuesta donde la corrige.

## 1. Resumen

- **Se acepta la revisión entera.** Los siete veredictos son «de acuerdo con cambios» y se adoptan todos.
- **Cinco correcciones a mi propuesta:**
  - **La notación de la tabla de Kelly.** Con `x` la exposición, `g(x) = x·μ − x²·σ²/2` y el óptimo está en `x* = μ/σ²`. Con `f` la fracción del óptimo, `g(f·x*)/g(x*) = 2f − f²`. La tabla da los mismos valores (un cuarto da el 43,75 %), pero solo bajo esa aproximación: ventaja conocida, varianza fija y costes lineales.
  - **«El riesgo se conoce» se retira.** La volatilidad y la correlación también se estiman con error y cambian. E se apoya en escenarios adversos, límites nominales y sensibilidad, no solo en la volatilidad.
  - **Un cuarto de Kelly no es una regla.** Es una hipótesis aspirante que debe ganar a la asignación simple en el banco.
  - **«E no vuelve a comparar» se corrige.** Si el tamaño final cambia algo material, D revalida (ciclo acotado del §5, el mismo que en la decisión de D).
  - **«FIFO y dos meses» sale de E.** No es una regla genérica para todos los productos. SC-9 devuelve el tratamiento y la procedencia de la regla para cada instrumento y ejercicio, y la valida el asesor (P-06).
- **La reserva conjunta de dinero y riesgo es un requisito de arquitectura.** Dos planes válidos por separado no pueden gastar juntos el mismo saldo ni el mismo presupuesto de riesgo.
- **Seis ideas nuevas** (§4). Las más útiles:
  - el plan como grafo de patas con liquidación;
  - la regla de que un dato que falta no es cero;
  - el banco frente a políticas simples.

## 2. Veredictos de Astra

| Decisión | Astra | Claude | Cómo se aplica |
| --- | --- | --- | --- |
| Tres capas | De acuerdo con cambios | **Se acepta** | Las tres capas leen el **mismo estado conciliado** (foto de G y K con hash, la misma que en D). Entran también las posiciones pendientes y el patrimonio externo declarado que sea pertinente. Hay un solo presupuesto de riesgo, repartido, y ninguna capa lo cuenta dos veces. |
| Tamaño por riesgo | De acuerdo con cambios | **Se acepta** | Corrección del §1: además de la volatilidad, los escenarios adversos del Motor, los límites nominales y la sensibilidad del tamaño a los errores de estimación. |
| Kelly fraccional | De acuerdo con cambios | **Se acepta** | Kelly es una referencia aspirante, calculada **sobre la cartera** y con ventajas netas. Si la ventaja no se puede estimar, no hay Kelly: se usa el plan aprobado y un tamaño fijo prudente. |
| Tabla por cartera | De acuerdo con cambios | **Se acepta** | El mandato y el perfil son comunes, y los métodos dependen del instrumento. Sumar las pérdidas hasta los stops no mide todo el riesgo: hay huecos de precio, y el Documento 0 de E ya los reconoce. En largo plazo cuentan también la liquidez y un escenario de retirada. |
| Ciclo de cinco pasos | De acuerdo con cambios | **Se acepta** | Se añaden la reserva de recursos, las dependencias entre patas y la comprobación al tamaño final (§5). La vista global puede originar una revisión, pero no autoriza movimientos entre libros. |
| Fronteras | De acuerdo con cambios | **Se acepta** | D revalida si el tamaño final lo exige. G decide los detalles del envío dentro de los límites del plan. F aprueba cada acción. |
| Cero tokens e históricos | De acuerdo con cambios | **Se acepta** | E no llama a ningún modelo, pero tiene coste de datos y de simulación. Ser código no lo libra de mirar el futuro: la elección de parámetros y de reglas puede filtrarlo, y se controla con datos de fecha de publicación y con el registro de experimentos (idea 5). |

## 3. Mejoras de Astra

| Mejora | Decisión | Cómo se aplica |
| --- | --- | --- |
| Riesgo de cartera antes que Kelly individual | **Se acepta** | Se evalúa el conjunto: escenarios de crisis, exposición nominal por factor, órdenes autorizadas, ejecuciones parciales y fondos subyacentes. Una correlación baja estimada no permite pasar un límite nominal. |
| Reserva de dinero y riesgo | **Se acepta** | El servicio dueño del estado (el libro de G) reserva de forma indivisible al autorizar, con versión del estado y vigencia. Solo se libera cuando se cancela o se concilia la orden. Una orden con resultado incierto conserva la reserva. E propone la reserva, F la controla y G la consume. Es la misma reserva que usa D (decisión de D, idea 2). |
| Cerrar D y E | **Se acepta** | §5, paso 6. |
| Plan ejecutable por etapas | **Se acepta** | Idea 1. Una aportación repetida por error no crea dos saldos: el evento de G tiene identificador y E lo trata de forma idempotente. |
| Volatilidad y caída | **Se acepta** | El ajuste por volatilidad y el freno por caída son políticas aspirantes. Se comparan en el banco con bandas, persistencia de la señal, plazos de revisión y costes, frente a pesos estables. No se promete más rentabilidad. Volver a subir el riesgo sigue la autonomía aprobada (E3: el principio exige la aprobación del operador). |
| Presupuesto de pérdida | **Se acepta** | Tres cifras separadas: pérdida calculada hasta los stops, pérdida en estrés y límites nominales. La frase «cuánto acepto perder en un año malo» se concreta con horizonte, probabilidad y escenario, y nunca se presenta como pérdida máxima garantizada. |
| Fiscalidad, pendiente del asesor | **Se acepta** | §1. Con reglas provisionales, ningún ahorro fiscal se da por confirmado. SC-9 contempla las operaciones de todas las cuentas pertinentes. |
| Independencia de F | **Se acepta** | Consultar los topes de F evita fórmulas divergentes, pero F puede discrepar con razón si cambian los precios, la política o el estado. E no se aprueba a sí mismo, y F comprueba también en ejecución. La concentración mínima antes de M la exige el §7 de la Constitución. |
| Validación y orden | **Se acepta** | Es el orden del §5: primero estado y reservas, plan base y aportaciones; después encaje, costes y escenarios; al final, inclinaciones por ventaja medida. |

**Preguntas de la propuesta.** Se toman las siete respuestas de Astra. Los valores que el operador ya haya fijado en privado no se copian al repositorio; se leen de su configuración local.

## 4. Ideas nuevas

1. **El plan como grafo de patas.** Cada plan CT-G-07 es un grafo: cada pata (vender, comprar, traspasar) tiene sus dependencias, la fecha de liquidación del dinero que libera, el redondeo y el mínimo del instrumento, las comisiones y una política si falla (cancelar las que dependen de ella, mantener o escalar). Una compra financiada con una venta no se lanza antes de que la venta liquide, salvo que haya efectivo reservado para cubrirla. El simulador prueba ejecuciones parciales y el rechazo de una pata.
2. **Un dato que falta no es cero.** Si falta una correlación, se usa 1 al sumar riesgos (lo prudente); si falta una volatilidad, la posición no se dimensiona por volatilidad y se declara. Ningún dato material ausente se rellena con un valor que reduzca el riesgo.
3. **Los mismos escenarios que D.** E dimensiona sobre el mismo conjunto de escenarios conjuntos de SC-3 que usó D, con la misma semilla. Así D y E miden lo mismo, y la revalidación compara cosas comparables.
4. **Propiedades que se prueban siempre.** Una batería de pruebas de propiedades que no dependen de los datos:
   - el tamaño nunca supera un tope de F;
   - el redondeo es siempre hacia abajo;
   - más ventaja estimada nunca hace que se pase el presupuesto de riesgo;
   - un dato que falta nunca aumenta el tamaño;
   - el mismo estado y la misma entrada dan el mismo plan byte a byte.
5. **Backtest sin mirar el futuro.** Las pruebas con años de precios de K usan solo datos con su fecha de publicación. Cada elección de parámetros se registra antes en el registro de experimentos (T-99), con una muestra final reservada.
6. **Banco frente a políticas simples.** Con los mismos casos se comparan: los pesos del mandato sin inclinaciones, un tamaño fijo prudente, el ajuste por volatilidad y Kelly fraccional. Se miden el exceso neto, las caídas, la rotación, los incumplimientos, los recursos bloqueados y la sensibilidad a costes y errores. Si ninguna gana con claridad, manda la más simple.

## 5. Diseño para construir

### El ciclo de E

1. **Estado:** la foto de G y K con hash, con posiciones, pendientes, reservas y patrimonio externo pertinente.
2. **Presupuesto:** el de riesgo del mandato, en sus tres cifras (stops, estrés y nominal), y lo ya usado o reservado.
3. **Tamaño:** se parte del plan base o de un tamaño fijo prudente. La inclinación por ventaja (Kelly fraccional sobre la estimación de D) solo se aplica con ventaja medida suficiente, y siempre topada por el riesgo.
4. **Encaje:** factores, escenarios de crisis, conflictos entre libros, bandas y liquidez. Un dato que falta, con la regla de la idea 2.
5. **Plan por etapas:** el grafo de patas (idea 1), con el tratamiento fiscal que devuelva SC-9.
6. **Revalidación con D:** si el tamaño, la financiación o los costes cambian algo material (umbral en la configuración), D reevalúa los finalistas sobre la misma foto. Las rondas tienen tope; si no converge, se escala o se abstiene.
7. **Topes de F y reserva:** E pide los topes y redondea hacia abajo, y propone la reserva. F aprueba, reduce o veta, y G reserva y ejecuta.

**Abstenerse.** La decisión analítica de abstenerse lleva al plan base (P5), pero no lanza ninguna compra por sí sola. Con datos que faltan o una incidencia de conciliación, se mantiene el estado.

### Orden de construcción, un ticket por paso

| Paso | Qué | Terminado cuando (binario) |
| --- | --- | --- |
| E-0 · Medida | Adaptador «e» del banco y prerregistro, con las políticas simples (idea 6) | El banco corre las políticas simples con datos simulados y deja informe |
| E-1 · Estado y reservas | Foto con hash, reserva indivisible con vigencia y liberación, aportaciones idempotentes | Dos planes sobre el mismo saldo: el segundo ve la reserva; una aportación repetida no crea dos saldos; una orden incierta conserva la reserva |
| E-2 · Plan base | Pesos del mandato, bandas, aportaciones, grafo de patas con liquidación | La batería de propiedades (idea 4) pasa; una pata rechazada deja el estado coherente |
| E-3 · Encaje | Escenarios conjuntos (los de D), factores, límites nominales y regla del dato que falta | Una correlación que falta da el riesgo de correlación 1; un límite nominal no se pasa con una correlación baja |
| E-4 · Ciclo con D | Revalidación acotada | Un tamaño que cambia el ganador provoca la reevaluación; sin convergencia, escala o abstención |
| E-5 · Inclinaciones | Kelly fraccional, ajuste por volatilidad y freno por caída, como aspirantes | Informe del banco; solo se activa lo que gana a la política simple, con la ratificación del operador |

El E actual del marco común (V0.10, `sistema_global/marco_comun_c/validador/dimensionado.py`) se conserva: es el tamaño por distancia al stop del trading, con los topes de F y la conversión de divisa que ya tiene. E-2 a E-5 se construyen a su alrededor, en un ticket del marco con su autorización.

## 6. Qué decide el operador

1. Ratificar este diseño.
2. El presupuesto de pérdida de cada cartera, con horizonte, probabilidad y escenario (SC-1).
3. Qué políticas aspirantes se ensayan (fracción de Kelly, ajuste por volatilidad, freno por caída), en simulado.
4. La anchura de las bandas y el umbral de cambio material con D, `[PROPUESTO]` para T-57.
5. Si los movimientos entre estrategias de trading se hacen por regla, dentro de la matriz de autonomía, o con aprobación cada vez.
6. Quién es el asesor fiscal (P-06), que valida las reglas de SC-9.

## 7. Qué no se hace

- No se cambian la Constitución, CT-G-06, CT-G-07 ni el marco común sin autorización y su ticket.
- E no aprueba ni envía órdenes: F controla y G ejecuta.
- No se da por confirmado ningún ahorro fiscal ni ninguna mejora de rentabilidad sin el asesor y el banco.
