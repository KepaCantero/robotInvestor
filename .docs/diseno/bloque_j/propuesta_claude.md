# Bloque J: el laboratorio que no se engaña (propuesta de diseño de Claude)

De: Claude, 11-11-2026. Estado: **PROPUESTA PARA DISCUTIR**. No hay nada que implementar: el operador está decidiendo la arquitectura de los bloques antes de construir (relevo de Astra, §0 bis). Copia en el repositorio del documento que el operador revisó con Claude.

## 1. Respuesta corta

J diseña, entrena y prueba todo lo que cambia cómo decide el robot (estrategias, modelos, prompts y agentes) y lo sube por la escalera de verificación. No pone nada en producción, no puntúa su trabajo ni ve la reserva sellada (D-39). J completo llega en la Fase 4; en la Fase 1 basta la escalera mínima hasta el paper trading (T-82).

El peligro de un laboratorio es **encontrar lo que no existe**. Idea central: **cada intento cuenta.** Cuatro piezas: registro de experimentos con hipótesis y criterio sellados antes de mirar; escalera por tipo de cosa (datos para estrategias, casos que el modelo no conoce para prompts y agentes); ficha de salida de cada estrategia validada; y no construir lo que existe (medir el motor de backtest de robotTrading antes de decidir).

## 2. Por qué las estrategias que ganan en el backtest pierden en real

| Causa | Qué pasa | Cuánto pesa |
| --- | --- | --- |
| Muchos intentos | Alguna variante gana por azar | Con 100 variantes sin ventaja sobre 5 años, la mejor suele mostrar un Sharpe cercano a 1 |
| Ajuste fino | Parámetros ajustados al ruido | Un pico estrecho casi nunca se repite; una meseta, a veces |
| Datos que no se sabían | Fecha de referencia en lugar de fecha de publicación | Puede crear ventajas enteras |
| Supervivientes | Solo activos que siguen existiendo | Infla resultados |
| Costes olvidados | Diferencial, deslizamiento, impuestos | En trading, ganar o perder |
| La ventaja se gasta | Deja de funcionar cuando otros la descubren | Las anomalías publicadas pierden una parte importante tras publicarse |

Y una séptima: **los modelos de IA ya conocen el pasado** (§7). Lo «validado» debe haber sobrevivido a pruebas pensadas para tumbarlo.

## 3. Qué hay hoy y qué falta

Decidido en la Constitución: ciclo de vida de la estrategia con capital, cortacircuitos y universo propios (§7); escalera de cuatro peldaños con sus trampas (D-39); verificaciones externas; protocolo de entrenamiento con purga y embargo, reserva sellada, Sharpe deflactado, probabilidad de sobreajuste, crisis y referencia simple (§9.17); J entrena, I juzga.

En código: el modo de backtest de A y del de divisas, que emiten señales para el backtester de robotTrading. J como bloque, nada (es de la Fase 4).

Falta: registro de experimentos (sin él, el Sharpe deflactado usa un número inventado); cómo se prueba cada tipo de cosa; ficha de salida; decisión sobre el motor de backtest (la lección de NautilusTrader: prometía 10× y dio 0,26–1,05×); versión mínima de la Fase 1 (T-82).

## 4. Cómo se prueba cada cosa

|  | Estrategia de reglas | Modelo de aprendizaje automático | Prompt o kit | Agente o modelo de IA nuevo |
| --- | --- | --- | --- | --- |
| Ejemplo | Tendencia en divisas | Régimen, meta-etiquetado | Kit de C-DIV | Contradictor de otro proveedor, versión nueva de un modelo |
| Peldaño 1 | Backtest con fecha de conocimiento, costes de G, sin supervivientes | Validación temporal con purga y embargo; reserva sellada | Casos anonimizados o posteriores a la fecha de corte | Conjunto dorado (D-40) y banco de medida |
| Peldaño 2 | Simulación en tiempo real | Simulación en tiempo real | En paralelo al titular, sin efecto | En paralelo al titular, sin efecto |
| Peldaño 3 | Dinero real en pequeño | Aspirante con poco peso | Aspirante en parte de los encargos | Aspirante en parte de los encargos |
| Referencia simple | Comprar y mantener; regla de una línea | Modelo lineal o tasa base | El que está en uso | El que está en uso y la variante solo código |
| Trampa principal | Intentos y ajuste fino | Fugas del futuro | El modelo reconoce el pasado | Buen resultado en pocos casos |

Criterios comunes: robusto (meseta, crisis, regímenes), simple (menos parámetros) y con capacidad suficiente para el capital que asignaría E.

**Escalera de una estrategia:** 0 hipótesis prerregistrada y sellada → 1 backtest (reserva sellada; juzga I) → 2 simulación (en el rango del backtest) → 3 dinero real en poco (aprobación del operador, capital mínimo) → 4 tramos (si todo sigue en verde); en uso, H vigila la deriva (§7). Si un peldaño falla, vuelve a `CANDIDATA` o se retira, y esa idea no reutiliza la misma reserva. Debajo de todo, el registro de experimentos.

## 5. Reglas contra el autoengaño

1. Prerregistro sellado: hipótesis, datos, criterio de éxito y número máximo de variantes.
2. Cada intento cuenta: el registro anota también las descartadas; con ese número se corrige el resultado.
3. La reserva sellada es de I y se usa una vez por idea.
4. Datos honrados: fecha de conocimiento, universos con desaparecidos, costes medidos por G, segundo proveedor.
5. Siempre frente a la referencia simple, nunca en absoluto.
6. Robustez antes que brillo: meseta, crisis, subperiodos, mercados parecidos.
7. Presupuesto de parámetros.
8. Para la IA, casos que no pueda conocer y un conjunto dorado que no se usa para entrenar.
9. Quien propone no puntúa.
10. Duración de cada peldaño fijada antes (P-33).

La batería de conformidad de J comprueba cada regla con código.

## 6. Fronteras y ficha de salida

| Quién | Relación con J |
| --- | --- |
| Investigador cuantitativo (E4-12) | Entrega hipótesis prerregistradas; no ve la reserva ni puntúa |
| I | Guarda la reserva y da el veredicto |
| K | Única fuente de datos; bases para aprender (D-38) |
| G | Costes reales medidos |
| E | Capital de cada estrategia por Kelly fraccional sobre la ventaja medida en real |
| F | Cortacircuitos y límites; vía sistemática sin LLM (§4.3) |
| H | Compara con el rango de la ficha y pausa si deriva |
| Operador | Aprueba el paso a `ACTIVA` y cada tramo |

**Ficha de salida:** parámetros congelados y su huella; universo admitido; capacidad; capital inicial y tramos; cortacircuitos; rango esperado de rentabilidad, caída y racha (para H); referencia simple; expediente del experimento.

## 7. Precisión, consumo y orden

Consumo: estrategias y modelos son cálculo; los tokens aparecen al probar prompts, kits y agentes (un kit de C sobre 100 casos N2 ≈ 5 M de tokens, 10–20 $, estimado). Presupuesto declarado en el prerregistro, API por lotes y tope anual (E4-17).

Precisión: el «descuento» entre backtest y real, medido por I estrategia a estrategia; dice si J se engaña y D y E lo aplican a las estrategias nuevas.

Orden: Fase 1 (T-82), escalera mínima, registro de experimentos y prerregistro desde ya (cada intento cuenta desde el primer día); calibración de prompts por SC-4 sin J. Antes de la Fase 4, medir el motor de robotTrading. Fase 4, J completo con Investigador, conjunto dorado y ficha de salida.

## 8. Preguntas para el operador

1. Registro de experimentos y prerregistro desde la Fase 1.
2. Duración (P-33): al menos 3 meses y 50 operaciones en simulación, y 3 meses con dinero real en pequeño antes del primer tramo.
3. Capital del peldaño 3: una cifra que el operador acepte perder entera, con un máximo del 2 % de la cartera de trading por estrategia.
4. Medir el motor de backtest de robotTrading antes de decidir.
5. Investigador cuantitativo en la Fase 4.
