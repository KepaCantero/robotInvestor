# Bloque H: cuándo salir y cuándo quedarse (propuesta de diseño de Claude)

De: Claude, 11-11-2026. Estado: **PROPUESTA PARA DISCUTIR**. No hay nada que implementar: el operador está decidiendo la arquitectura de los bloques antes de construir (relevo de Astra, §0 bis). Copia en el repositorio del documento que el operador revisó con Claude. Va con las de D, E, F y G (`.docs/diseno/`).

## 1. Respuesta corta

H vigila las posiciones abiertas. Cuando se cumple una condición numérica declarada de antemano (stop, objetivo, invalidez por precio), pide a G que salga; ante cualquier otra señal, solo propone una revisión y nunca vende por su cuenta. Es código determinista, sin LLM, y esa regla de la Constitución (§4.2) se mantiene.

El H de hoy hace bien la parte mecánica. Se propone que **deje de reaccionar a todo con la misma vara y se concentre en las señales que de verdad predicen pérdidas o dinero parado**:

1. **Alertas a la medida de la volatilidad:** la pérdida en «veces lo normal» para ese activo, no un porcentaje fijo.
2. **Vigilar el tiempo, no solo el precio:** catalizadores vencidos sin efecto y posiciones paradas, que D compara con las alternativas.
3. **Vigilar a quien produce las posiciones:** la deriva de cada estrategia de trading frente a su backtest (§7) y la calidad de cada fondo del largo plazo.
4. **Un perfil por cartera:** en trading, H es casi todo mecánico; en largo plazo, casi nada se vende por precio.

## 2. Cómo las salidas ganan o pierden rentabilidad por euro

| Error | Qué pasa | Qué cuesta |
| --- | --- | --- |
| **Vender pronto lo que gana** | Se recoge un beneficio pequeño por miedo a perderlo | La subida que no se cobra y el impuesto pagado antes |
| **Aguantar lo que pierde** | Se espera a «recuperar» con la tesis rota | Pérdidas que crecen y dinero mal colocado |
| **Salir por ruido** | Stops o alertas demasiado ajustados | Costes de salir y volver, y la subida posterior |
| **Dinero parado** | Posición sin catalizador ni movimiento durante meses | Lo que habría dado en el plan pasivo o en algo mejor |

Los dos primeros son una tendencia humana bien documentada que un robot con reglas declaradas evita casi por construcción. Los dos últimos, en cambio, los puede cometer **más** un robot con reglas rígidas. Además, los impuestos: vender con ganancia adelanta el impuesto; vender con pérdida puede compensar ganancias respetando la regla de los dos meses. En largo plazo, la mejor salida suele ser no salir y dejar que E reequilibre con las aportaciones.

## 3. Qué hay hoy y qué le falta

Se conserva (Documentos 0 V0.09, V0.25 y V0.30; `sistema_global/marco_comun_c/validador/vigilancia.py`, reglas H-01 a H-19):
- salidas automáticas solo por condiciones numéricas declaradas (stop, objetivo, invalidez por precio, toma parcial), en L2; en L0 y L1 las prepara;
- cierre dado por hecho solo con confirmación del intermediario y stop retirado; reintentos de cierres a medias;
- con precio viejo o reloj sospechoso, avisa en vez de actuar;
- fecha de revisión (H-14), escenarios del Contradictor e invalidez por otras métricas (H-16): revisión y propuesta, nunca venta;
- alerta de pérdida (H-17) y vigilancia de reaperturas (H-15);
- estado vigilado en la cadena de huellas.

Le falta, por orden de importancia:
1. **Alerta de pérdida igual para todo** (−5 % fijo por defecto): ruido en lo volátil, tarde en lo tranquilo.
2. **No vigila el tiempo ni el coste de oportunidad.**
3. **No vigila a quien produce:** la deriva de estrategias que pide el §7 no está construida; tampoco la calidad de los fondos.
4. **Una sola frecuencia y política** para las tres carteras.
5. **Revisiones sin prioridad:** no dicen cuánto dinero está en juego ni si compensa un análisis nuevo de C (P18).

## 4. Una sola lógica para las tres carteras

|  | Trading | Táctica | Largo plazo |
| --- | --- | --- | --- |
| **Qué vigila** | Reglas de salida de cada estrategia y su deriva | La tesis: stop, objetivo, invalidez, catalizador y fecha, escenarios del Contradictor | Hitos de la tesis (sub-pronósticos de 12 meses o menos, §9), desviación de pesos (para E), calidad de cada fondo |
| **Lo que hace sola** | Salidas de la estrategia; pausar la estrategia si deriva (§7) | Stop, objetivo e invalidez por precio | Casi nada |
| **Lo que solo propone** | Retirar una estrategia pausada | Invalidez cualitativa, catalizador vencido, pérdida anormal, posición parada | Hito incumplido, cambio en un fondo, tesis activa que ya no se sostiene |
| **Frecuencia** | Continua en horario de mercado | Diaria y alrededor de cada evento de K | Semanal y cuando K publica datos de un hito |
| **Señal de pérdida** | Por estrategia (racha y caída acumulada) | Por posición, en veces la oscilación normal | No aplica al plan; sí a las inclinaciones activas |

## 5. El ciclo de vigilancia

Pasada por el reloj de cada cartera o por un evento de K:
1. **Datos frescos** (si son viejos, avisa y no actúa).
2. **Condiciones declaradas** → sale sola (G ejecuta en L2; la prepara en L0 y L1).
3. **Señales de revisión** (Contradictor, invalidez por otras métricas, pérdida anormal) → revisión con prioridad al Broker, con el dinero en juego; análisis de C solo si compensa.
4. **Salud de quien produce** (nuevo) → pausa la estrategia (§7) o propone cambiar el fondo.
5. **Tiempo y dinero parado** (nuevo) → D compara quedarse con las alternativas.
6. **Registro para I** (nuevo): cada señal y lo que pasó después.

Solo el paso 2 vende sin preguntar.

## 6. Qué hace salir y qué no

| Con fundamento | Ruido |
| --- | --- |
| Condición de invalidez declarada que se cumple | Caída dentro de la oscilación normal |
| Hito de la tesis incumplido en su fecha | Titular de prensa, hasta que SC-11 lo contraste |
| Escenario de fallo del Contradictor disparado | Operación perdedora de una estrategia en su rango |
| Catalizador que pasa sin efecto | Movimiento sin cambio en la tesis |
| Estrategia fuera del rango de su validación | Pocas operaciones, sin muestra |
| Fondo que cambia de gestor, sube comisiones o se separa de su índice | Oscilación diaria de un indexado |

1. **La pérdida se mide en veces lo normal** (oscilación del activo en el plazo de la tesis, con datos de K).
2. **La deriva se comprueba con estadística:** prueba frente al rango del backtest con muestra suficiente; pausa anticipada solo ante una caída peor que la peor del backtest o una racha imposible según su validación.
3. **Cada revisión llega con su prioridad:** dinero en juego y si compensa un análisis nuevo (P18); primero el Broker con el sobre existente.
4. **H nunca mueve un stop hacia el lado que arriesga más;** subirlo para asegurar beneficio solo si la propuesta lo declaró.

## 7. H frente a G, F, E, D, C, I y el Broker

| Quién | Relación con H |
| --- | --- |
| **G** | Ejecuta las salidas con órdenes de solo reducción; los stops viven en el intermediario |
| **F** | Las salidas son «reducir o cerrar»: con la asimetría propuesta para F, nunca se bloquean por pérdidas ni frecuencia |
| **E** | Recortar por peso es de E; salir por tesis es de H y del Broker. H le pasa las desviaciones de peso |
| **D** | Recibe las posiciones paradas para comparar quedarse con las alternativas |
| **C** | Análisis nuevo solo si la revisión lo justifica |
| **I** | Recibe cada señal y su resultado |
| **Broker o gestor** | Recibe las propuestas con prioridad; confirma con fecha nueva o cierra |

**H mira cada tesis; E mira el conjunto.**

## 8. Precisión y consumo

**Consumo: cero en H.** El gasto llega después (Broker y C), por eso importa la prioridad: menos revisiones inútiles sin perder las buenas.

**Precisión, medida por I:** señales que acertaron, falsas alarmas, señales que faltaron (pérdidas grandes sin aviso previo) y cómo habrían ido las estrategias pausadas. Ajustes por la ruta de cambios (§9); como H es código, sus reglas se prueban sobre años de precios de K.

**Datos que faltan:** oscilación normal por activo y plazo (K); resultados y rango del backtest de cada estrategia (J); datos de cada fondo; hitos de cada tesis congelados en SC-4.

## 9. Preguntas para el operador

Ninguna hay que contestarla ahora; cada una lleva un valor por defecto [PROPUESTO], en simulado.

1. **Alerta de pérdida:** «dos veces la oscilación normal del activo en el plazo de la tesis» en lugar del −5 % fijo.
2. **Pausa de estrategias:** además de la deriva estadística, pausar si cae más que en el peor momento de su backtest.
3. **Dinero parado:** revisar una posición táctica sin movimiento ni catalizador a la mitad del plazo de su tesis.
4. **Asegurar beneficios** subiendo el stop: solo en trading, como regla de cada estrategia.
5. **Vigilancia de los fondos** del largo plazo: sí, como propuesta de revisión, sin venta automática.
