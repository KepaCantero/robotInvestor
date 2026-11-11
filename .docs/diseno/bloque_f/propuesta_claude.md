# Bloque F: el control que protege la rentabilidad (propuesta de diseño de Claude)

De: Claude, 11-11-2026. Estado: **PROPUESTA PARA DISCUTIR**. No hay nada que implementar: el operador está decidiendo la arquitectura de los bloques antes de construir (relevo de Astra, §0 bis; T-74 sigue en espera). Copia en el repositorio del documento que el operador revisó con Claude. Va con las de D y E (`.docs/diseno/`).

## 1. Respuesta corta

F es el control que ninguna parte del robot puede convencer. Todo lo que acabe en una orden pasa por él, y responde APROBADO, REDUCIDO o VETADO con límites sencillos en euros. No decide si una inversión es buena (eso es de D y de E). Su trabajo es que **ningún error, ninguna mala racha y ningún agente equivocado pueda hacer un daño del que la cartera no se recupere.**

El F del marco común está bastante avanzado (23 reglas, verificación del informe por el Orquestador, nueva comprobación con el precio real al ejecutar, fallo cerrado). No se propone rehacerlo, sino cuatro cambios de diseño para que proteja la rentabilidad sin frenarla:

1. **Controles asimétricos por tipo de acción.** Abrir o aumentar riesgo pasa todos los filtros. Reducir riesgo, poner una protección o reequilibrar hacia los pesos del mandato no se bloquea nunca por pérdidas ni por frecuencia, solo por errores de forma.
2. **Una política por cartera** en lugar de una sola para las tres, con límites en tres niveles: por orden, por cartera y global.
3. **El estado de la cartera, de la segunda fuente.** F lee posiciones, saldos y pérdidas del libro conciliado de G con el intermediario, no del que trae quien propone. Es hoy el principal límite abierto.
4. **Medir lo que cuesta cada veto.** I calcula cómo habrían ido las operaciones vetadas o reducidas. Nada se relaja solo.

## 2. Cómo un control ayuda a ganar más por euro

Un control no añade rentabilidad en un día normal; la añade en los malos, porque las pérdidas grandes cuestan mucho más de recuperar de lo que parecen:

| Pérdida | Lo que hay que ganar después para volver al punto de partida |
| --- | --- |
| 10 % | 11 % |
| 20 % | 25 % |
| 33 % | 50 % |
| 50 % | 100 % |
| 75 % | 300 % |

F actúa sobre tres fuentes de esas caídas: **errores** (un cero de más, un precio viejo, un duplicado, una divisa mal convertida), **agentes equivocados o manipulados** (F no lee el razonamiento, solo cifras y referencias) y **rachas y sucesos raros** (pérdidas seguidas, posiciones que dependían de lo mismo, huecos de precio).

Pero un control también cuesta:
- **Vetos de más:** cada operación buena impedida es rentabilidad perdida; la Constitución ya lo vigila con la alarma de sequía y el seguimiento de lo descartado (§7 y §9).
- **Vetos a destiempo:** lo más caro es impedir reducir riesgo, o comprar con la aportación justo después de una caída. Un límite de pérdida semanal que veta cualquier orden hace exactamente eso.

El buen diseño **corta las colas sin tocar el centro**: límites amplios para lo normal, duros para lo extremo, y nunca un obstáculo para reducir riesgo.

## 3. Qué hay hoy y qué le falta

Se conserva: código determinista con fallo cerrado; reduce cuando una cantidad menor lo arregla y veta cuando no; límites nominales (importe por orden, día y activo, pérdida del día y de la semana, órdenes por hora, mandato, exclusiones, evidencia, ventanas de eventos, autonomía, kill-switch, precio del intermediario); recálculo por el Orquestador y repetición con el precio real; E le pide sus topes.

Le falta, por orden de importancia (fuentes: `sistema_global/documentos_0/V0.07_F_control_de_riesgo.md` y `sistema_global/marco_comun_c/validador/control_f.py`):

1. **Solo entiende abrir una posición con stop.** Toda solicitud necesita un stop (F-02): no sabe controlar la compra de un fondo de largo plazo, una venta, un reequilibrio ni una aportación. Y como no distingue el tipo de acción, una pérdida del día agotada (F-08) vetaría también una venta que reduce riesgo.
2. **Una sola política para las tres carteras.** Diez posiciones o un 10 % por posición tiene sentido en táctica, no en una cartera de largo plazo con un fondo indexado que pesa el 60 %.
3. **El estado de la cartera lo trae quien propone.** F comprueba la aritmética, no que los datos sean los reales.
4. **Faltan los controles de T-74:** fracción del volumen medio diario (5 %), liquidez mínima, coste y margen de la orden, exposición compartida por divisa, emisor o factor.
5. **El riesgo de hueco no está acotado.** F limita la pérdida hasta el stop, pero un salto de precio la puede superar.

## 4. Los controles por tipo de acción, nivel y cartera

### Cuatro tipos de acción

| Tipo | Ejemplo | Qué controles se aplican |
| --- | --- | --- |
| **Abrir o aumentar riesgo** | Posición nueva, reforzar | Todos: forma, orden, cartera y global |
| **Reequilibrar hacia el plan** | Comprar con la aportación lo que está por debajo de su peso | Forma y orden. No le afectan los límites de pérdida ni las ventanas de eventos, porque es el propio plan (como ya hace la rentabilidad mínima, §8.11) |
| **Reducir o cerrar** | Vender por tesis invalidada, stop o para bajar riesgo | Solo forma y cordura de la orden. Nunca se bloquea por pérdidas, frecuencia ni kill-switch (que solo bloquea entradas, §8) |
| **Proteger** | Poner o mover un stop hacia el lado que protege | Solo forma. Mover un stop hacia el lado que arriesga más cuenta como aumentar riesgo |

**Bajar riesgo siempre tiene que ser fácil, y subirlo, difícil.** La Constitución ya lo aplica al perfil y a la autonomía (§6); se lleva a las órdenes.

### Tres niveles de límite

1. **Por orden:** forma y procedencia, precio frente al del intermediario, importe máximo, fracción del volumen medio diario, coste y margen, duplicados.
2. **Por cartera:** mandato, presupuesto de riesgo, concentración, pérdida del día y de la semana, número de posiciones, autonomía.
3. **Global:** pérdida de todo el patrimonio gestionado, apalancamiento total, órdenes por hora, exposición compartida por divisa, emisor, país o sector sumando las tres carteras. Prevalecen sobre los de cada cartera (§7).

Para la exposición compartida, F **mira dentro de los fondos** (un indexado mundial tiene buena parte en dólares aunque cotice en euros). Sin composición de K, cuenta el fondo como si todo estuviera en su divisa o región principal.

### Lo que pesa en cada cartera

|  | Trading | Táctica | Largo plazo |
| --- | --- | --- | --- |
| **Lo que más vigila** | Frecuencia, pérdida diaria y semanal, cortacircuitos por estrategia, liquidez | Riesgo hasta el stop, huecos alrededor de eventos | Concentración por emisor, país y divisa, mirando dentro de los fondos |
| **Importe por orden** | Pequeño y frecuente | Intermedio | Grande y poco frecuente |
| **Límites de pérdida** | Estrictos: una racha puede indicar que la ventaja se agotó | Intermedios | Solo frenan aumentos de riesgo activo, nunca el reequilibrio al plan |
| **Ventanas de eventos** | Vetan abrir | Reducen el tamaño si el evento es el catalizador declarado en la tesis; vetan en el resto | No aplican al reequilibrio |

La fila de eventos resuelve una tensión: en táctica muchas tesis giran alrededor de un evento; vetarlas todas deja a la cartera sin su razón de ser, y permitirlas a tamaño completo ignora el riesgo de hueco.

## 5. El recorrido de una acción por F

Entrada: el plan de E (CT-G-07) o una salida propuesta por H, cada acción con su tipo, cantidad, precio y cartera.

1. **Forma y procedencia:** estado de cartera del libro conciliado; precio y tipo de cambio del intermediario.
2. **¿Qué tipo de acción es?** Reducir, cerrar o proteger salta directamente al resultado tras la cordura de la orden.
3. **Límites por orden.**
4. **Límites por cartera** (el reequilibrio al plan no pasa los de pérdida ni las ventanas).
5. **Límites globales.**

Resultado: APROBADO, REDUCIDO (con la cantidad permitida) o VETADO (con su regla y motivo). Después, como hoy: el Orquestador recalcula el informe, F se repite con el precio real y G ejecuta; y vigilancia continua con cortacircuitos a L1, kill-switch y vigilante con latido.

## 6. Medir si F acierta

| Medida | Qué dice | Qué se hace con ella |
| --- | --- | --- |
| **Lo que costó cada veto o reducción** | Cómo habría ido la operación con la cantidad pedida | Si una regla veta sobre todo operaciones que habrían ganado, se propone revisarla |
| **Lo que evitó** | Pérdidas que no ocurrieron porque F las paró | Justifica cada regla con datos (presupuesto de complejidad, §9.11) |
| **Cuánto se acerca la cartera a cada límite** | Uso habitual de cada límite | Uno que nunca se toca no protege; uno que se toca a diario frena de más |

- **Nada se relaja solo** (P8): I propone, J lo prueba y el operador decide. Endurecer sí puede ser inmediato.
- **Veto por error frente a veto por límite:** el primero es siempre un acierto; el segundo solo lo dice el resultado.
- **Batería permanente de ataque:** cantidades en el borde, carteras incompletas, divisas cambiadas, órdenes partidas para esquivar el importe máximo. Todo cambio de F la sigue pasando.

## 7. F frente a E, G, H, M y el operador

| Quién | Qué hace | Relación con F |
| --- | --- | --- |
| **E** | Decide cuánto, dentro de su presupuesto de riesgo | Pide a F sus topes; E apunta al tamaño que conviene, F pone el techo |
| **F** | Techo independiente en euros | No calcula rentabilidades ni lee tesis; su concentración se calcula aparte de la de E (D-25) |
| **G** | Único canal de órdenes; libro conciliado | Segunda fuente de F; stops como órdenes nativas en el intermediario |
| **H** | Vigila posiciones y propone salidas | Sus salidas son «reducir o cerrar»: F no las frena por pérdidas ni frecuencia |
| **M** (Fase 3) | Riesgo de cartera | F no consume su salida, a propósito |
| **Operador** | Fija los límites y puede anular un veto | Con registro, motivo y el límite mensual de anulaciones (§6), nunca desde un mensaje no autenticado |

**E usa betas, correlaciones y estimaciones; F no.** F trabaja con importes en euros, número de órdenes y composición nominal, porque en una crisis las correlaciones fallan (§8.2). Si el modelo de riesgo de E se equivoca, F sigue en pie.

## 8. Precisión y consumo

**Consumo: cero, y debe seguir así** (P2). Cada regla nueva justifica con datos lo que evita.

**Precisión:** que nunca deje pasar lo que no debe (batería de ataque y casos aleatorios) y que no frene de más (cuenta de I y alarma de sequía).

**Datos que faltan:** el libro conciliado de G como fuente única del estado; volumen medio diario y coste por instrumento (K); composición de los fondos; tipos de cambio y margen por producto del intermediario.

**Orden de construcción sugerido:** tipos de acción y asimetría (cambian CT-G-08); política por cartera; lectura del estado desde G; controles de T-74 a medida que K sirva sus datos.

## 9. Preguntas para el operador

Ninguna hay que contestarla ahora; cada una lleva un valor por defecto [PROPUESTO], en simulado. Los límites concretos se fijan con el asesor de configuración del Broker, con sus consecuencias en euros.

1. **La asimetría:** reducir, cerrar o proteger no se bloquean nunca por pérdidas, frecuencia ni kill-switch, solo por errores de forma. Cambia CT-G-08.
2. **El reequilibrio al plan** no lo frenan los límites de pérdida ni las ventanas de eventos.
3. **Una política por cartera** (tres más los límites globales). Sus valores son P-03.
4. **Eventos en táctica:** reducir en lugar de vetar cuando el evento es el catalizador declarado. ¿A qué fracción?
5. **Riesgo de hueco:** un límite adicional por posición con un salto supuesto por tipo de activo.
6. **Fondos sin composición conocida:** contarlos en su divisa o región principal hasta que K sirva la composición.
