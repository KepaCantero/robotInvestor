# Bloque M: ver el riesgo que cada libro no ve (propuesta de diseño de Claude)

De: Claude, 11-11-2026. Estado: **PROPUESTA PARA DISCUTIR**. No hay nada que implementar: el operador está decidiendo la arquitectura de los bloques antes de construir (relevo de Astra, §0 bis). Copia en el repositorio del documento que el operador revisó con Claude.

## 1. Respuesta corta

M mira la cartera entera de una vez. E dimensiona operación a operación y F limita con reglas, pero ninguno ve las dependencias ocultas entre carteras ni cuánto costaría en euros una crisis como la de 2008. M es código determinista, sin tokens: **asesora a E y nunca veta** (eso es F, que no consume su salida; P2, P15). Llega en la Fase 3 (D-18); hasta entonces E hace la comprobación mínima de concentración (D-25).

Se propone:

1. **Cuatro vistas:** exposición real abriendo los fondos (divisa, país, sector, emisor y factor); estrés en euros frente a la tolerancia; dependencia en las colas y número de apuestas independientes; liquidez al salir.
2. **Pregunta previa para E:** «¿qué pasa con el riesgo si hago esto?», antes de cada propuesta de tamaño.
3. **M comprueba sus propias predicciones** de riesgo, e I mide su acierto.
4. **El valor principal para un particular:** saber en euros, antes de invertir, cuánto costaría una caída como la de 2008, para no vender en pánico.
5. **Ligero y sujeto a la brújula:** módulos del Motor; si no demuestra en el banco de medida que mejora la rentabilidad por euro, se queda en la comprobación mínima de E.

## 2. Qué riesgos pierden dinero sin que nadie los vea

| Riesgo | Ejemplo | Qué cuesta |
| --- | --- | --- |
| Concentración oculta | Un fondo global, uno tecnológico y acciones de una gran tecnológica: la misma apuesta tres veces | Una caída del sector duele el triple de lo previsto |
| Dependencia que aparece en crisis | Activos poco relacionados en calma que caen juntos en pánico | La diversificación desaparece justo cuando hace falta |
| Divisa escondida | Fondo en euros que invierte en dólares sin cubrir | Un movimiento del dólar que nadie había previsto |
| Apuestas cruzadas entre carteras | Trading vende dólares y la táctica compra bolsa de EE. UU. | Costes por posiciones que se anulan, o una apuesta duplicada |
| Liquidez al salir | Pequeña compañía o fondo con reembolso lento | Vender en crisis cuesta mucho más que en calma |
| Pánico del operador | Una caída del 30 % que no había visto antes en euros | Vender en el peor momento, a menudo la mayor pérdida de un particular |
| Geopolítica y cambio de régimen | Guerra, sanciones, crisis energética | Escenarios que la historia reciente no contiene |

Por qué esto es rentabilidad y no solo prudencia: el crecimiento compuesto es aproximadamente el rendimiento medio menos la mitad de la varianza (g ≈ μ − ½σ²). Bajar la varianza de la cartera sin bajar el rendimiento esperado sube lo que se gana a largo plazo. Y al revés: un M demasiado prudente encoge posiciones que sí compensaban, y eso también cuesta rentabilidad. M tiene que acertar, no asustar.

## 3. Qué hay hoy y si M hace falta

Decidido en la Constitución: M asesora a E y F no consume su salida (§2); hasta la Fase 3, E comprueba que no se acumulen apuestas del mismo factor y F calcula su propia versión (D-25); el Motor calcula la pérdida en un conjunto estándar de episodios históricos, igual para todas las comparativas de D; pruebas de estrés geopolíticas en la Fase 3; apalancamiento y derivados no habilitados antes de la Fase 3 (D-16).

En código: nada de M. Los diseños de E, F y H ya calculan volatilidades y correlaciones del Motor sobre K, pero posición a posición o cartera a cartera.

**¿Hace falta M?** Mientras solo haya divisas en simulación (Fases 1 y 2), no: E y F bastan. Hace falta cuando coinciden varias carteras, fondos con composición, más de un tipo de activo y dinero real. Se propone una regla de entrada: M se construye en la Fase 3 solo si el banco de medida demuestra que la comprobación mínima de E se queda corta (por ejemplo, en episodios históricos sobre las carteras simuladas, la pérdida real supera claramente la que E esperaba). Si no lo demuestra, se amplía la comprobación de E y no se construye un bloque.

## 4. Las cuatro vistas del riesgo

| Vista | Qué responde | Cómo se calcula | Qué entrega |
| --- | --- | --- | --- |
| 1. Exposición real | ¿Qué tengo de verdad? | Abre cada fondo con su composición (K) hasta el emisor; suma por divisa, país, sector, emisor y factor | Euros y porcentaje por eje, por cartera y en total |
| 2. Estrés | ¿Cuánto perdería en euros? | Episodios históricos estándar del Motor y escenarios hipotéticos (cierre de una ruta marítima, sanciones, salto del petróleo, crisis de una divisa) como choques sobre factores | Pérdida en euros por escenario frente a la tolerancia del perfil |
| 3. Dependencia | ¿Cuántas apuestas distintas tengo? | Correlaciones en calma y en crisis, dependencia en las colas, número efectivo de apuestas independientes, contribución de cada posición al riesgo | Quién aporta el riesgo y si la diversificación aguanta |
| 4. Liquidez | ¿Cuánto cuesta salir? | Días para salir sin mover el precio (volumen de K), coste de salida en tensión con los costes medidos por G, plazos de reembolso de fondos | Días y euros para salir, por cartera |

**Pregunta previa.** E envía la cartera tal como quedaría y M devuelve el cambio en las cuatro vistas, en milisegundos y sin IA. E sigue decidiendo el tamaño.

**Escenarios hipotéticos.** Son choques sobre factores con cifras y fuente, no opiniones. Los propone el Estratega macro (o el vigía de régimen) a partir de lo que lee SC-11; M los traduce a choques; el operador los aprueba. Pocos y vigentes: se retiran cuando dejan de ser plausibles.

## 5. El informe de riesgo de M

Entradas (libro de G, datos de K, mandatos y perfil, escenarios) → M (cuatro vistas, código, cero tokens) → E (pregunta previa e informe; E decide el tamaño), Broker (lo explica en euros) e I (mide el acierto de M). Al otro lado de la frontera de independencia (P2, P15), F calcula su propia versión con su propio código y datos y no lee el informe de M.

## 6. M en las tres carteras y en el conjunto

Una sola lógica con un perfil por cartera, como en el resto de bloques.

| Cartera | Qué mira M | Cuándo | Para qué sirve |
| --- | --- | --- | --- |
| Trading | Exposición neta por divisa y factor entre estrategias; pérdida conjunta en días malos | Diaria | Que varias estrategias no sean la misma apuesta; tope de pérdida conjunta para E |
| Táctica | Factores y temas; estrés por escenario; dependencia con el largo plazo | Semanal y antes de cada cambio | Tamaño de las apuestas tácticas |
| Largo plazo | Exposición real de los fondos, divisa, estrés tipo 2008 en euros | Mensual y en la revisión anual | Que el operador vea y acepte la caída antes de que ocurra |
| Conjunto | Suma de las tres, solapamientos y apuestas que se anulan | Diaria | Riesgo total frente a la tolerancia; costes de posiciones que se anulan |

**Contra la venta de pánico.** Las cifras de estrés del largo plazo entran en la política de inversión personal, en la revisión anual con el Broker (D-32) y en el asesor de configuración (D-34): «con esta cartera, en una caída como la de 2008 perdería unos X € y tardaría unos Y años en recuperarlos». Si el operador no acepta esa cifra, se cambia la cartera antes, no durante la caída. Para un particular, probablemente sea lo que más rentabilidad por euro protege de todo M.

## 7. M frente a E, F, K, el Motor y el vigía

| Quién | Relación con M |
| --- | --- |
| E | Recibe el informe y las respuestas a la pregunta previa; decide los tamaños. M nunca decide |
| F | Calcula su propia versión con su código y sus datos y no lee a M (P2, P15). Si las dos versiones discrepan mucho, se avisa al operador y a I, sin que ninguno cambie su cálculo |
| K | Única fuente de datos, composición de fondos incluida; M no guarda copia |
| Motor | Los modelos de riesgo de M son módulos del Motor que mantiene M; cada cifra cita su sello |
| G | Libro de posiciones y costes de salida medidos |
| H | Vigila posición a posición; M, la cartera entera |
| Vigía de régimen | Cuando marca tensión, M pasa a usar las correlaciones de crisis |
| Estratega macro y SC-11 | Proponen escenarios hipotéticos con fuente; M los traduce a choques |
| Broker | Explica el informe al operador en euros; es el único uso de IA, y opcional |
| I | Mide el acierto de M |
| J | Somete las estrategias nuevas a los mismos escenarios de estrés |
| D | Usa el mismo conjunto de episodios de estrés en sus comparativas |

## 8. Precisión, consumo y cuándo construirlo

**Precisión: M predice, y cada predicción se comprueba.**

- **Excepciones.** Si M dice que un día de cada cien se perderá más de cierta cifra, eso debe pasar más o menos un día de cada cien. Muchas más veces: M es optimista. Muchas menos: M es demasiado prudente y encoge posiciones que sí compensaban.
- **Estrés.** En cada caída real, pérdida prevista frente a pérdida real.
- **Exposición real.** Se contrasta con la composición que publica cada fondo.
- **Aspirante frente a titular.** Para los modelos de riesgo (por ejemplo, correlaciones simples, ajustadas hacia una media o un modelo de factores), en el banco de medida. I lo mide.

**Consumo:** cero tokens. Solo la explicación opcional del Broker gasta algo.

**Brújula.** M mejora la rentabilidad por euro si se cumple al menos una de estas tres cosas:

1. Baja la caída máxima o la volatilidad sin bajar el rendimiento esperado.
2. Evita ventas de pánico.
3. Evita costes de apuestas que se anulan.

Si no lo demuestra en el banco, no se construye.

**Orden:**

- **Fases 1 y 2:** nada de M. E hace la comprobación mínima (D-25), el Motor mantiene el conjunto de episodios y K empieza a guardar la composición de los fondos.
- **Antes de la Fase 3:** banco de medida con las carteras simuladas.
- **Fase 3:** primero las vistas 1 y 2 (las de más valor para un particular), después la 3 y la 4, con el estrés geopolítico que pide la Constitución.
- **Derivados o apalancamiento (D-16):** si el operador los habilita, M añade antes una vista de sensibilidades no lineales.

## 9. Preguntas para el operador

Todas son [PROPUESTO]; ninguna se decide sin el operador.

1. **M ligero:** código, cero tokens, Fase 3, y solo si demuestra en el banco de medida que la comprobación mínima de E se queda corta.
2. **Escenarios hipotéticos:** los propone el Estratega macro con fuente, M los traduce a choques y el operador los aprueba; pocos y vigentes.
3. **Tolerancia de pérdida en estrés por cartera, en euros:** se fija en la revisión anual con el Broker.
4. **La caída tipo 2008 en euros,** aceptada por escrito en la política de inversión personal antes de invertir a largo plazo.
5. **Si M y F discrepan mucho:** aviso al operador y a I, sin que ninguno cambie su cálculo.
6. **Adelantar la vista de exposición real** a la Fase 2 si los fondos llegan antes (E4-18).
