# Bloque N: la consola del operador (propuesta de diseño de Claude)

De: Claude, 11-11-2026. Estado: **PROPUESTA PARA DISCUTIR**. No hay nada que implementar: el operador está decidiendo la arquitectura de los bloques antes de construir (relevo de Astra, §0 bis). Copia en el repositorio del documento que el operador revisó con Claude.

## 1. Respuesta corta

N es lo que el operador ve del robot y el sitio donde decide. Muestra, avisa y recoge decisiones, pero **nunca aprueba por sí misma ni altera cifras** (§2): las acciones las ejecuta el Orquestador con sus reglas. Es código, sin IA; las explicaciones en lenguaje sencillo las redacta el Broker y siempre van junto a las cifras, nunca en su lugar.

El riesgo más caro para un particular suele ser su propio comportamiento: vender en una caída, anular al robot por una noticia o subir el riesgo tras una buena racha. Por eso la idea central es **pocas decisiones, bien informadas, en el momento justo.** Se propone:

1. **Una cifra principal:** cuánto gana o pierde el robot frente a no hacer nada (la cartera sombra), después de costes, impuestos e inflación, con su rango.
2. **Fricción asimétrica:** reducir riesgo es inmediato; aumentarlo pide cifras, importe tecleado, segundo factor y espera.
3. **Pocos avisos y fuera del chat:** solo lo que exige acción llega al móvil, con acuse y escalado; lo demás va al resumen semanal.
4. **El operador también se mide:** I calcula si sus intervenciones suman o restan.
5. **Construir sobre lo que existe:** el N mínimo (V0.06) y la aprobación con importe tecleado (V0.19) ya funcionan con datos simulados.

## 2. Qué decisiones del operador ganan o pierden rentabilidad

El informe «Mind the Gap» de Morningstar de 2026 calcula que, entre 2016 y 2025, los fondos rindieron un 9,9 % al año y sus partícipes un 8,7 %: **1,2 puntos al año perdidos por comprar y vender en mal momento** ([fuente](https://www.wealthmanagement.com/investing-strategies/investors-miss-out-on-12-of-fund-returns-over-decade)). Sobre 20.000 € son unos 240 € al año, probablemente más de lo que costará todo el robot.

| Decisión | Error típico | Qué cuesta |
| --- | --- | --- |
| Vender en una caída | Pánico al ver la pérdida por primera vez | Perderse la recuperación |
| Anular al robot por una noticia | Reaccionar al ruido | Costes y, a menudo, peor resultado |
| Subir el riesgo tras una buena racha | Exceso de confianza | Caídas mayores que la tolerancia |
| Mirar a diario la cartera de largo plazo | Ver pérdidas pequeñas que no importan | Más intervenciones y peor resultado |
| Aprobar sin leer, o tarde | Cansancio y demasiados avisos | Errores u órdenes caducadas |
| No enterarse de un aviso crítico | Sin canal fuera de la consola | Un problema que crece sin que nadie lo vea |
| No saber si el robot aporta | Sin comparación con la sombra | Pagar por algo que no gana a un indexado |

N no puede impedir estos errores, porque el operador manda; pero sí puede hacer que el bueno sea el camino fácil.

## 3. Qué hay hoy y qué falta

N ya tiene código de referencia (V0.06 y V0.19, en el marco común, con datos simulados).

**Se conserva:**

- **Panel verde, ámbar y rojo** con cinco comprobaciones (integridad, datos, presupuesto, avisos y decisiones). Si no se puede calcular, sale en rojo.
- **Cola de decisiones** ordenada por vencimiento.
- **Avisos** con prioridad y acuse; acusar no borra.
- **Pantalla de aprobación** con las cifras de F e importe tecleado al céntimo. Cada aprobación vale una sola vez, caduca sin actuar y tiene un enfriamiento en condiciones fijadas.
- **Kill-switch mínimo.**

**Falta:**

| Qué | Pendiente | Depende de |
| --- | --- | --- |
| Canal real fuera del chat, con escalado | T-41 | D-07 |
| Autenticación y segundo factor reales | T-01 | D-19 (P-08) |
| Cifra principal frente a la sombra e informes | — | Diseño de I |
| Embudo de abstención y alarma de sequía | T-75 (detenido) | D-22 |
| Límite de anulaciones y no subir límites el mismo día | T-50 | — |
| Hibernación y persona de confianza | — | D-32 (P-30) |
| Riesgo en euros (M) y rango esperado de cada posición (H) | — | Diseños de M y H |
| Histórico del panel y uso desde el móvil | — | — |

## 4. Qué muestra la consola

Siete pantallas, cada una para una pregunta. La primera se mira en segundos; las demás, solo cuando hacen falta.

| Pantalla | Pregunta | Qué muestra | Cuándo mirarla |
| --- | --- | --- | --- |
| 1. Inicio | ¿Va todo bien y qué espera de mí? | Semáforo, cifra principal y decisiones pendientes | Al llegar un aviso, o una vez por semana |
| 2. Decisiones | ¿Qué apruebo? | Cifras de F, plan base, riesgo en euros de M y, al lado, la explicación del Broker | Cuando haya algo pendiente |
| 3. Carteras | ¿Qué tengo? | Posiciones con su rango esperado (H), exposición real y estrés en euros (M) | Trading a diario si se quiere; táctica semanal; largo plazo mensual |
| 4. Avisos | ¿Qué no he visto? | Avisos con acuse y su historial | Al llegar |
| 5. Informes | ¿Aporta el robot? | Semanal: actividad, embudo de abstención y coste. Mensual: atribución de I frente a la sombra. Anual: revisión guiada | Semanal, mensual y anual |
| 6. Salud | ¿Funciona el robot? | Estado por bloque, sellos de K, presupuesto de IA y latido | Si el inicio no está en verde |
| 7. Configuración | ¿Cambio algo? | Cada parámetro con su valor por defecto y su justificación; los cambios pasan por el Broker | En la revisión anual |

**La cifra principal.** «Frente a no hacer nada: +X € (entre A y B) desde tal fecha, después de costes, impuestos e inflación.» La calcula I. Si el rango incluye el cero, lo dice: «todavía no se puede saber si el robot aporta». En el inicio, la cartera de largo plazo se muestra en su horizonte, no día a día.

**Explicaciones que no inventan cifras.** Cada número lleva un «¿por qué?» que abre su expediente. El Broker explica si se le pide, con su texto marcado como explicación. Antes de mostrarlo, el código comprueba que cada cifra del texto está en la pantalla; si alguna no está, el texto no se muestra.

## 5. De dónde sale lo que ve el operador

Fuentes (F: cifras de cada orden; I: resultado frente a la sombra; M y H: riesgo en euros y rangos; Broker: explica, sin cifras nuevas) → N (código, cero tokens: inicio, decisiones, avisos e informes, salud) ↔ operador (decide con importe tecleado y segundo factor). N ↔ Orquestador (decisiones y estado): el Orquestador ejecuta con sus reglas. Orquestador → canal fuera del chat (avisos altos, con acuse) → operador y persona de confianza (aviso de hibernación; solo lectura si se permite). Los avisos altos no dependen de N, así que el kill-switch y el vigilante funcionan aunque N falle.

## 6. Avisos, aprobaciones y fricción deliberada

**Pocos avisos, y fuera del chat.** Demasiados avisos hacen que se ignoren todos, así que solo llega al móvil lo que exige actuar.

| Nivel | Ejemplos | Canal | Si no hay acuse |
| --- | --- | --- | --- |
| Alta: exige actuar | Kill-switch, discrepancia sin explicar, latido perdido, cortacircuito, decisión a punto de vencer | Móvil y correo, nunca el chat | Se repite y escala; al final, hibernación y aviso a la persona de confianza |
| Media: conviene saber | Stop ejecutado, posición en revisión, dato dudoso | Resumen diario | Panel en ámbar |
| Información | Actividad, informes | Resumen semanal | Nada |

Se propone un presupuesto de avisos [PROPUESTO]: si los de prioridad alta pasan de uno por semana de media, I revisa por qué.

**Fricción asimétrica.** Lo que baja el riesgo es fácil; lo que lo sube cuesta.

| Acción | Qué pide N |
| --- | --- |
| Reducir riesgo, vender, pausar, kill-switch | Nada más que un toque: la Constitución permite bajar el riesgo al momento |
| Aprobar una orden dentro del mandato | Cifras de F, importe tecleado, un solo uso; caduca sin actuar |
| Aumentar riesgo, subir límites o autonomía | Además, segundo factor, canal distinto del chat y espera; nunca el mismo día en que se alcanzó un límite |
| Anular un veto, si algún día se permite | Motivo escrito y límite mensual (T-50) |
| Operación hecha fuera del robot | Declararla en N (CT-G-14); lo no declarado es una discrepancia |

**Contra la venta de pánico, sin bloquearla.** Si el operador vende a mano una posición de largo plazo en una caída, N muestra antes, en la misma pantalla y sin espera: la caída que aceptó por escrito (M), cuánto ha caído de verdad, el coste de salir y lo que dice el plan base. Con un toque más, vende. Nunca se le impide reducir riesgo.

## 7. N frente al Broker, F, el kill-switch, I y los demás

| Quién | Relación con N |
| --- | --- |
| Orquestador | N lee su estado y le entrega las decisiones del operador; es el Orquestador quien las ejecuta con sus reglas |
| Broker conversacional | Conversa y explica; N muestra y recoge decisiones. Ninguna aprobación se hace en el chat |
| F | Sus cifras son las únicas que aparecen en una pantalla de aprobación; N no las recalcula ni las redondea |
| Kill-switch y vigilante | El botón está en N, pero el kill-switch funciona aunque N falle. El vigilante avisa por el canal fuera del chat sin pasar por N |
| I | Da la cifra principal, los informes y la medida de las intervenciones del operador |
| M y H | Dan el riesgo en euros y el rango esperado de cada posición |
| K | Sellos y avisos de calidad de datos para el panel de salud |
| SC-4 y presupuesto | Consumo y coste de la IA para el panel de salud y el informe semanal |
| Persona de confianza | Recibe el aviso de hibernación; si el operador lo permite, solo lectura, con credenciales propias (D-32) |
| Asesor de configuración | Propone parámetros explicados en euros; el cambio se confirma en N con su fricción |

**El operador también se mide.** I trata las intervenciones del operador (anulaciones, ventas a mano, aprobaciones rechazadas) como una etapa más de decisión y calcula si suman o restan frente a lo que habría hecho el robot. N lo muestra en el informe mensual, sin juicio: es información para él, no un reproche.

## 8. Precisión, seguridad, consumo y orden

**Precisión: cómo se sabe que N funciona.**

| Medida | Objetivo |
| --- | --- |
| Panel en verde con un problema real | Cero (batería de fallos como la de V0.06) |
| Tiempo hasta el acuse de un aviso alto | Dentro del plazo de escalado |
| Decisiones que caducan sin respuesta | Pocas, y cada una con su motivo |
| Avisos altos por semana | Dentro del presupuesto de avisos |
| Operaciones hechas fuera del robot sin declarar | Cero |
| Valor de las intervenciones del operador | Lo mide I; se muestra, no se juzga |

**Seguridad.** N es la puerta al plano de control, así que:

- **Autenticación real** con segundo factor (T-01) y solo dos papeles: operador y persona de confianza, esta de solo lectura.
- **Un registro de auditoría** de cada acción.
- **Acceso desde una red privada** o por un canal cifrado.
- **Avisos sin detalle de la cartera:** dicen que hay algo que ver y piden abrir N.
- **Sin secretos del intermediario en N** y sin datos del operador en el repositorio.
- **Una N por copia** del robot (enmienda 3).

**Consumo:** N gasta cero tokens. Las explicaciones del Broker se generan solo si se piden, y el resumen semanal se genera una vez y se guarda.

**Tecnología** [PROPUESTO]: una web local servida por el propio robot, usable en el móvil, más un servicio de notificaciones para los avisos. Nada de aplicación nativa.

**Orden:**

- **Fase 1:** lo que ya hay (V0.06 y V0.19), más:
    - la cifra principal en simulación, cuando I la dé;
    - un informe semanal sencillo;
    - el embudo de abstención (T-75);
    - la declaración de operaciones hechas fuera del robot.
- **Fase 2:** informes mensuales con la atribución de I, explicaciones del Broker con la comprobación de cifras y configuración por el cuestionario.
- **Fase 3, con dinero real:** canal fuera del chat (T-41), autenticación real (T-01), hibernación y persona de confianza, vistas de M y la pantalla contra la venta de pánico.

## 9. Preguntas para el operador

Todas son [PROPUESTO]; ninguna se decide sin el operador.

1. **Cifra principal:** frente a la cartera sombra, después de costes, impuestos e inflación, con rango; y el largo plazo, sin cifra diaria en el inicio.
2. **Canal fuera del chat (D-07):** notificación al móvil más correo, con escalado.
3. **Presupuesto de avisos:** como mucho uno de prioridad alta por semana de media antes de revisarlos.
4. **Venta a mano en una caída:** mostrar antes la caída aceptada y el plan base, sin espera y sin impedirla.
5. **Que I mida sus intervenciones** y N las muestre en el informe mensual.
6. **Tecnología:** web local usable en el móvil, sin aplicación nativa.
