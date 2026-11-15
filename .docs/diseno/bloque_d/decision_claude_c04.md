# Bloque D: decisión de Claude sobre la revisión C-04 de Astra y diseño de construcción

De: Claude, 15-11-2026. Responde a la revisión de Astra `revision_astra.md` (base `e91eebc`) sobre mi propuesta `propuesta_claude.md`, ambas en esta carpeta, por encargo del operador del mismo día: decidir qué entra y qué no, añadir mejoras y dejar el diseño listo para cuando se construya.

Estado: **DISEÑO ESTABLECIDO**, a falta de las decisiones del operador del §6. No se construye hasta que el operador lo ordene. Al construir, este documento manda sobre la propuesta donde la corrige.

## 1. Resumen

- **Se acepta la revisión entera.** Ocho veredictos «de acuerdo» o «de acuerdo con cambios», que se adoptan. El noveno es un «en desacuerdo» con la puerta del paso 6, y Astra tiene razón: se sustituye (§2).
- **Cuatro correcciones a mi propuesta:**
  - **La puerta ya no compara rangos sueltos.** Se decide con la incertidumbre de la **diferencia emparejada** frente a cada alternativa, sobre los mismos escenarios. Que dos rangos se solapen no demuestra que haya empate (el contraejemplo de Astra: `A = Z + 1` frente a `B = Z`).
  - **La fórmula `media − ½ · varianza` sale del diseño.** Era una aproximación que no vale con colas o saltos. D calcula directamente el crecimiento logarítmico medio sobre los escenarios del Motor, con método declarado, y lo somete a las restricciones de pérdida y liquidez del mandato.
  - **«No hacer nada» no es lo mismo que «comprar el plan pasivo».** Las opciones pasan de cuatro a seis (§5), y abstenerse nunca lanza por sí solo una compra del benchmark.
  - **D y E no se llaman en un bucle libre.** Cuando E da el tamaño final, se hace una revalidación acotada (§5).
- **La regla 1 del §5 de la Constitución no cambia.** Comparar por valor esperado entre las clases Q, S y K espera a la decisión E8 del operador, antes de la Fase 2.
- **D no llama a ningún modelo.** Su coste es de datos, simulación y validación, y se declara.
- **Siete ideas nuevas** (§4). Las más útiles:
  - la corrección de la maldición del optimizador;
  - la tabla atada a una foto de la cartera, con el efectivo reservado;
  - el banco frente a las reglas simples.

## 2. Veredictos de Astra

| Decisión | Astra | Claude | Cómo se aplica |
| --- | --- | --- | --- |
| Crecimiento compuesto neto | De acuerdo con cambios | **Se acepta** | Objetivo económico común, sujeto al mandato: pérdida máxima, liquidez, necesidades y horizonte, como restricciones explícitas. Método declarado: media de `log(1 + r)` sobre los escenarios conjuntos de SC-3, sin aproximación cuadrática. |
| Un comparador por perfiles | De acuerdo | **Se acepta** | Un núcleo común. El perfil de cada cartera (SC-1) da el reloj, el calendario y los costes. |
| Opciones | De acuerdo con cambios | **Se acepta** | Seis opciones: mantener, aplicar el plan base, candidato nuevo, reforzar, reducir o cerrar, y sustituir. Además, la liquidez que el mandato obliga a conservar. |
| Contracción por historial | De acuerdo con cambios | **Se acepta** | El Brier no se convierte en precisión de rentabilidad. Lo que se modela es el **error del objetivo que importa** (la rentabilidad neta prevista frente a la obtenida), con muestras independientes y versiones congeladas. Sin tasa base defendible, la opción sale de la comparación con `NO_ESTIMABLE`. |
| Aportación marginal | De acuerdo con cambios | **Se acepta** | Se comparan **planes completos** sobre el mismo estado: posiciones, operaciones pendientes y financiación. Los efectos no lineales (costes por tamaño, tramos fiscales) impiden escalar siempre a 1.000 €: la tabla da la cifra por 1.000 € **al tamaño evaluado** y lo dice. |
| Ventana común y reinversión | De acuerdo con cambios | **Se acepta** | Misma ventana y mismos escenarios para todas las opciones. Se incluyen la liquidación, los costes, cuándo está disponible el dinero y el riesgo del propio benchmark. La reinversión en el benchmark es una hipótesis explícita, con plazo y costes. |
| Extremo bajo y tres salidas | **En desacuerdo** | **Se acepta su alternativa** | La puerta usa el intervalo de la diferencia emparejada frente al plan base y frente a mantener, con el criterio fijado antes de ver resultados y corregido por el número de opciones (idea 1). Cuatro estados distintos: `VENTAJA` (recomendar), `EMPATE_TECNICO` (decide el Broker con el operador), `SIN_VENTAJA` (abstenerse) y `SIN_DATOS` (no se compara, ver §5). |
| D y E separados, Kelly común | De acuerdo con cambios | **Se acepta** | Se comparte el objetivo y su modelo, versionado en SC-3, pero no la aprobación. Kelly fraccional es el **aspirante**, no una garantía: compite en el banco con alternativas con restricción de riesgo (Busseti, Ryu y Boyd). |
| Cero tokens y aprendizaje en I | De acuerdo con cambios | **Se acepta** | Ninguna llamada de IA dentro de D. Lo que se aprende (pesos por historial, contracción) no se actualiza solo: lo propone I o J, lo comprueba F y lo ratifica el operador. |

## 3. Comprobaciones y puntos débiles de Astra

| Punto | Decisión | Cómo se aplica |
| --- | --- | --- |
| Ejemplos numéricos | Se acepta | Los ejemplos del −0,09 % y del 68 % se conservan en la documentación como ilustración, y se marcan como hipótesis de reinversión, no como previsión. |
| Objetivo y aproximación | Se acepta | §1. La restricción de caídas va aparte del objetivo, porque Kelly no la cumple por sí solo. |
| Rango de la diferencia | Se acepta | Dos salidas separadas en la tabla: la **distribución del resultado** de cada plan y el **intervalo de la ventaja** frente a cada referencia. |
| D ↔ E sin bucle libre | Se acepta | §5. Si no converge en el número de rondas de la configuración, se escala o se abstiene. F conserva su control independiente. |
| Abstenerse no es comprar | Se acepta | La decisión analítica, su motivo y el plan operativo se registran por separado. Con datos que faltan o una incidencia de conciliación, mantener es la única acción segura y no se envía ninguna compra (P20: toda orden pasa por E, F y G). |
| Corto plazo | Se acepta | Diferencial, deslizamiento según tamaño y volatilidad, órdenes pendientes, capacidad conjunta, señales caducadas y simultaneidad correlacionada. Se retira la exención del freno a la rotación para cada operación de trading: se define y la aprueba el operador (§6). |
| Costes y fiscalidad | Se acepta | Si los escenarios ya son netos, los costes no se vuelven a restar: el artefacto marca qué está descontado. Una sola fórmula del margen de rotación para D, E y SC-9, en SC-3. El impuesto de cada venta lo calcula SC-9 para ese caso; D no supone que toda venta tributa. |
| Datos y orden | Se acepta | Es el orden de construcción del §5. Los resultados se registran desde el primer día, pero no se da peso aprendido sin evidencia. |
| Validación | Se acepta | Abstenciones por causa, calidad de los descartados, exceso neto frente a la referencia y frente a mantener, rotación, pérdidas en estrés y estabilidad ante costes y tamaños. La validación es temporal, con una muestra final reservada. Los umbrales, en la configuración aprobada. |

**Preguntas de la propuesta.** Se toman las ocho respuestas de Astra.

## 4. Ideas nuevas

1. **Corrección de la maldición del optimizador.** Al elegir la mejor de muchas opciones ruidosas, su ventaja estimada está sesgada al alza. La puerta usa un intervalo **simultáneo** para todas las opciones comparadas (por ejemplo, un bootstrap emparejado del máximo de las diferencias), y la ventaja que se congela en SC-4 es la corregida, no la bruta. El método va en la configuración y en el registro de experimentos (T-99).
2. **Tabla atada a una foto, con el efectivo reservado.** Cada tabla lleva el hash de la foto del estado de G y K que usó (posiciones, efectivo, pendientes, precios), su caducidad y el efectivo que compromete. Dos tablas no pueden gastar el mismo efectivo: la segunda ve la reserva de la primera. Una tabla caducada, o con una foto que ya no coincide, no autoriza nada.
3. **Banco frente a reglas simples.** Con los mismos casos y fechas se compara D frente a cuatro referencias: solo plan pasivo, repartir a partes iguales (1/N), el comparador actual del marco (V0.35, puntuación por opción) y D sin contracción. Se mide el exceso neto por euro con incertidumbre. Si D no gana a la regla 1/N, se dice.
4. **Re-ejecución sobre tablas congeladas.** Como D es determinista, cada cambio de reglas se prueba re-ejecutando las tablas congeladas en SC-4 con sus fotos (idea 2), y se comparan los resultados vencidos. Una muestra final reservada no entra en esas pruebas, para no sobreajustar.
5. **Explicación del Broker sin cifras libres (lección de T-102).** El Broker explica la tabla con marcadores de la tabla (`{tabla:fila…}`) y nunca escribe una cifra: el código las sustituye y un filtro quita y declara las que no vengan de un marcador.
6. **Escenarios conjuntos del Motor como única fuente.** Todas las opciones de una cartera se evalúan sobre el **mismo conjunto de escenarios**, con semilla registrada. Es lo que hace posible la diferencia emparejada y la reproducción exacta.
7. **El resultado de D como fichero de la configuración probado.** Los cuatro estados de la puerta, las seis opciones y los campos obligatorios de CT-G-05 se comprueban con un esquema y con casos adversos: un empate disfrazado (`A = Z + 1`), un candidato sin tasa base, una foto caducada y dos tablas sobre el mismo efectivo.

## 5. Diseño para construir

### La decisión, paso a paso

1. **Foto:** estado de G y K, mandatos, referencias ejecutables y su hash (idea 2).
2. **Opciones:** mantener, plan base, candidatos de C o estrategias de J, reforzar, reducir o cerrar, y sustituir; con la liquidez obligada del mandato.
3. **Escenarios conjuntos** de SC-3 para todos los planes, netos y marcados (idea 6).
4. **Contracción** de cada estimación hacia la tasa base, por el error medido del objetivo; sin tasa base, `NO_ESTIMABLE`.
5. **Crecimiento logarítmico de cada plan completo**, sujeto a las restricciones del mandato. El plan que incumple una restricción queda fuera, con su motivo.
6. **Puerta:** intervalo simultáneo de la diferencia emparejada frente al plan base y frente a mantener (idea 1). El resultado es `VENTAJA`, `EMPATE_TECNICO`, `SIN_VENTAJA` o `SIN_DATOS`.
7. **Revalidación con E:** E devuelve el tamaño factible. Si cambia materialmente el coste, la exposición o la ventaja (umbral en la configuración), se reevalúan los finalistas sobre la misma foto. Las rondas tienen tope y la tabla caduca; si no converge, se escala o se abstiene.
8. **Tabla CT-G-05** para el Broker, congelada en SC-4 con su foto: distribución de cada plan, intervalo de la ventaja, costes ya descontados, tamaño evaluado, método, referencia y vigencia. El Bloque I la mide al vencer.

### Orden de construcción, un ticket por paso

| Paso | Qué | Terminado cuando (binario) |
| --- | --- | --- |
| D-0 · Medida | Adaptador «d» del banco y prerregistro, con las cuatro referencias (idea 3) | El banco corre las referencias con datos simulados y deja informe |
| D-1 · Foto y opciones | Foto con hash, reserva de efectivo y generación de las seis opciones | Dos tablas sobre el mismo efectivo: la segunda ve la reserva; una foto cambiada invalida la tabla |
| D-2 · Comparación simple | Escenarios conjuntos, crecimiento logarítmico, restricciones del mandato, puerta emparejada con sus cuatro estados | Los casos adversos de la idea 7 dan el estado esperado; la re-ejecución da el mismo resultado byte a byte |
| D-3 · Ciclo con E | Revalidación acotada y caducidad | Un tamaño de E que cambia el ganador provoca una reevaluación; sin convergencia, escala o abstención |
| D-4 · Contracción y corrección | Error del objetivo por autor, intervalo simultáneo | Con poca muestra, la contracción es máxima; la ventaja congelada es la corregida |
| D-5 · Kelly frente a alternativas | Kelly fraccional frente a alternativas con restricción de riesgo, en el banco | Informe del banco; ninguna afirmación sin intervalo |

D se apoya en piezas que aún no existen (SC-1 con perfiles, SC-3 con escenarios conjuntos, SC-9, E). Cada paso usa esas piezas en su forma simulada y declara lo que falta.

## 6. Qué decide el operador

1. Ratificar este diseño.
2. Los umbrales de la puerta (nivel del intervalo, cambio material con E, rondas y caducidad), `[PROPUESTO]` para T-57.
3. La fracción de riesgo de cada cartera, como aspirante en simulado (SC-1).
4. Si alguna operación de trading queda exenta del freno a la rotación, y cuál.
5. E8: la regla 1 del §5 se mantiene hasta su decisión, antes de la Fase 2.

## 7. Qué no se hace

- No se cambian la Constitución, CT-G-05 ni el comparador del marco común sin autorización y su ticket.
- D no envía órdenes ni las aprueba: E dimensiona, F controla y G ejecuta.
- No se afirma que D gane rentabilidad: lo dice el banco con datos reales y, después, I con decisiones vencidas.
