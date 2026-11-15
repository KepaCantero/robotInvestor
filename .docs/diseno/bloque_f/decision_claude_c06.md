# Bloque F: decisión de Claude sobre la revisión C-06 de Astra y diseño de construcción

De: Claude, 15-11-2026. Responde a la revisión de Astra `revision_astra.md` (base `d544556`) sobre mi propuesta `propuesta_claude.md`, ambas en esta carpeta, por encargo del operador del mismo día: decidir qué entra y qué no, añadir mejoras y dejar el diseño listo para cuando se construya. Va con las decisiones de D y E (`.docs/diseno/bloque_d/decision_claude_c04.md` y `.docs/diseno/bloque_e/decision_claude_c05.md`) y con los cambios 47 y 78 de la Enmienda 5 (`.docs/diseno/enmienda_5/`), todavía `[PROPUESTO]`.

Estado: **DISEÑO ESTABLECIDO**, a falta de las decisiones del operador del §6. No se construye hasta que el operador lo ordene; T-74 sigue en espera y se reabre con este diseño. Al construir, este documento manda sobre la propuesta donde la corrige.

## 1. Resumen

- **Se acepta la revisión entera.** Seis veredictos «de acuerdo con cambios» y uno «en desacuerdo». Este último es con la exención del reequilibrio, y Astra tiene razón.
- **Cinco correcciones a mi propuesta:**
  - **No hay exención genérica para el reequilibrio.** Comprar para reequilibrar puede aumentar el riesgo. Solo un ciclo de aportación aprobado y acotado tiene excepciones concretas (las del cambio 78). Siguen aplicándose los límites globales, la liquidez, la autorización y el kill-switch de entradas.
  - **Reducir una posición no siempre reduce el riesgo.** Cerrar una cobertura puede subir la pérdida en un escenario adverso. Los conjuntos de cobertura los define el operador, y cerrar una de sus patas pasa los controles de aumentar riesgo.
  - **Un fondo sin composición no se cuenta todo en su región principal.** La parte conocida se conserva y la desconocida se presupuesta de forma conservadora en cada dimensión (divisa, región, emisor, sector).
  - **«Un límite que nunca se toca no protege» se retira.** Un control se juzga por los peligros que cubre y los defectos que detecta, no solo por la rentabilidad de lo que vetó.
  - **El estado de G ya existe en el marco** (V0.20: foto del intermediario, registro vigente y suma de autorizaciones pendientes). Lo pendiente es que funcione con una fuente real y actores autenticados, y las garantías de concurrencia. La propuesta lo presentaba como el principal límite abierto, y no lo es.
- **Corrección aritmética:** recuperar una pérdida `L` exige `L/(1−L)`. Para un 33 % es un 49,25 %, no un 50 % (el 50 % corresponde a un 33⅓ %). La tabla queda como orientativa.
- **La reserva de recursos es una sola para D, E y F.** Indivisible, ligada al hash de la orden final y liberada solo con confirmación.
- **Seis ideas nuevas** (§4). Las más útiles:
  - F en sombra antes de activar una versión;
  - la composición «el más restrictivo gana» comprobada por propiedades;
  - la campaña de defectos inyectados.

## 2. Veredictos de Astra

| Decisión | Astra | Claude | Cómo se aplica |
| --- | --- | --- | --- |
| Asimetría por acción | De acuerdo con cambios | **Se acepta** | El tipo de acción se deduce de la posición conciliada en G, nunca de la etiqueta que trae la solicitud (cambio 47). Se reduce contra la **cantidad libre**, descontadas las órdenes pendientes: dos ventas no consumen dos veces la misma posición. Reducir no habilita una reapertura posterior, que pasa todos los controles. Los conjuntos de cobertura, como en el §1. |
| Exención del reequilibrio | **En desacuerdo** | **Se acepta su alternativa** | No hay exención por etiqueta. Solo el ciclo de aportación aprobado tiene excepciones concretas (cambio 78): un identificador único de ciclo, el consumo agregado limitado al importe de la aportación, el mandato vigente y la condición de acercarse al mandato **en conjunto**, no orden a orden. El kill-switch lo bloquea. El ciclo no se puede repetir para multiplicar la aportación. |
| Política por cartera y tres niveles | De acuerdo con cambios | **Se acepta** | Prevalece el límite más restrictivo aplicable (idea 2). El consumo agregado incluye lo pendiente. Los contadores no se reinician con un cierre, una reapertura o un cambio de libro. |
| Estado desde G | De acuerdo con cambios | **Se acepta** | La foto de G lleva frescura, versión y respaldo en los extractos del intermediario. Un objeto que declara estar conciliado no basta: F comprueba su versión y su frescura. Entran las operaciones manuales y las dudosas. |
| Mirar dentro de los fondos | De acuerdo con cambios | **Se acepta** | La composición se usa con su fecha y su cobertura. Sin composición, `DESCONOCIDO` por dimensión, con un presupuesto conservador para la parte no cubierta (§1). Divisa de cotización, divisa de los activos y cobertura de divisa no son intercambiables. Los fondos de fondos no se suman dos veces. |
| Reducir por evento catalizador | De acuerdo con cambios | **Se acepta** | Solo con una política aprobada, un calendario verificable y un estrés específico del evento. La palabra «catalizador» en una tesis no habilita nada. La fracción se valida por instrumento y tipo de evento, sin valor fijo inventado. |
| Medición y batería de ataque | De acuerdo con cambios | **Se acepta** | Se añaden fallos raros, falsos negativos, indisponibilidad y suplantación. Ningún control se retira por no activarse, y un veto no se da por erróneo porque la operación vetada luego habría ganado. |

## 3. Hallazgos de Astra

| # | Hallazgo | Decisión | Cómo se aplica |
| --- | --- | --- | --- |
| 1 | Asimetría con límites semánticos | **Se acepta** | §2. El cierre de coberturas vuelve al operador (§6) antes de formalizarlo. |
| 2 | Proteger no es una etiqueta libre | **Se acepta** | F verifica lado, instrumento, cantidad, posición protegida y tipo de orden. Al sustituir un stop, la nueva protección se confirma antes de cancelar la vieja, y nunca hay dos órdenes que puedan dejar la posición invertida. La sustitución la definen G y SC-10. |
| 3 | Reequilibrio | **Se acepta** | §2 y cambio 78. |
| 4 | Reservas y permisos ligados a la orden final | **Se acepta** | La autorización y la reserva son indivisibles. Van ligadas al hash de la orden, a la versión de la política y del estado, a la cantidad restante y a una caducidad. Se consumen con las ejecuciones parciales y se liberan con una confirmación, no ante el silencio. Cubren las órdenes partidas, varios libros y varios intermediarios. Es la misma reserva de D y E (idea 2 de D, mejora de E). |
| 5 | Estado incierto | **Se acepta** | `DESCONOCIDO` no es `RECHAZADO`: una orden sin confirmación conserva su reserva hasta conciliarla. Precisar el §11 de la Constitución («sin confirmación = no ejecutada») va a la Enmienda 5 como `[PROPUESTO]`. Con la conciliación rota se bloquean las exposiciones nuevas y se escala, sin cancelar las protecciones nativas. La recuperación es un procedimiento autenticado. |
| 6 | Exposición desconocida | **Se acepta** | §2. |
| 7 | Evaluación de un control | **Se acepta** | Se mide la cobertura de peligros, los defectos inyectados detectados (idea 4), los falsos positivos y negativos, el coste operativo y la rentabilidad contrafactual, todo junto. Hay un **catálogo mínimo de controles obligatorios**, que no se retira aunque falten incidentes reales. |
| 8 | Endurecer y rehabilitar | **Se acepta** | Una respuesta automática inmediata solo es válida si está en una política preaprobada. I o un agente no inventan reglas nuevas. La rehabilitación es manual donde la Constitución lo exige (§6, P8, E3). Los cinco controles de T-74 ya estaban en T-74, no son nuevos. |

**Preguntas de la propuesta.** Se toman las seis respuestas de Astra. Los valores que el operador ya haya fijado en privado no se copian al repositorio.

## 4. Ideas nuevas

1. **F en sombra antes de activar una versión.** Una política o una regla nueva corre en paralelo con la vigente sobre las mismas solicitudes, sin efecto, y se registran las diferencias. Endurecer puede activarse enseguida; relajar exige ese periodo en sombra, el informe de diferencias y la aprobación del operador.
2. **«El más restrictivo gana», comprobado por propiedades.** La decisión final es el mínimo de los tres niveles y las políticas aplicables. Pruebas de propiedades:
   - añadir un límite nunca hace más permisiva la decisión;
   - pedir menos cantidad nunca convierte un APROBADO en VETADO;
   - el mismo estado y la misma solicitud dan la misma decisión;
   - un dato que falta nunca aprueba lo que con el dato se vetaría.
3. **Concurrencia probada con hilos.** Pruebas con varias solicitudes simultáneas sobre la misma posición, el mismo saldo y el mismo presupuesto de riesgo. La suma de lo aprobado nunca supera lo disponible, y dos ejecuciones con los mismos datos dan el mismo resultado (lección de T-88).
4. **Campaña de defectos inyectados.** Un banco permanente de solicitudes con errores sembrados:
   - un cero de más;
   - un precio viejo;
   - una divisa cambiada;
   - un duplicado;
   - una orden partida para esquivar el importe máximo;
   - un estado manipulado;
   - una cobertura disfrazada de reducción.

   Mide qué fracción detecta F, por clase de defecto. Toda versión de F pasa la campaña entera, y los mutantes de cada regla deben morir ante ella.
5. **Cada decisión registra su procedencia.** La decisión de F lleva la versión de la política, la versión y frescura del estado de G, la regla que decidió y el hash de la orden. Así una decisión se reproduce y se audita, y una orden cambiada después de aprobarse no coincide.
6. **Riesgo residual declarado.** Cada cartera declara el riesgo que F no cubre (huecos, liquidez, fallo de infraestructura), con sus escenarios de hueco por tipo de activo como límite adicional. Ese límite es conservador, pero nunca se presenta como el peor caso posible.

## 5. Diseño para construir

### El recorrido de una acción

1. **Forma y procedencia:** la foto de G con su versión y frescura; el precio y el tipo de cambio del intermediario; el hash de la orden.
2. **Tipo de acción, deducido de G:** abrir o aumentar, reducir o cerrar (contra la cantidad libre), proteger (verificado), o una pata de un ciclo de aportación aprobado. Cerrar una pata de un conjunto de cobertura cuenta como aumentar.
3. **Límites por orden, por cartera y globales:** el más restrictivo gana. Reducir y proteger no se vetan por pérdidas ni frecuencia, pero sí por forma, permisos y cantidad libre. El ciclo de aportación solo tiene las excepciones del cambio 78.
4. **Reserva indivisible** con caducidad.
5. **Resultado:** APROBADO, REDUCIDO o VETADO, con regla, motivo y procedencia (idea 5). Después, como hoy: el Orquestador recalcula, F se repite con el precio real y G ejecuta.

### Orden de construcción, un ticket por paso (T-74 reabierto)

| Paso | Qué | Terminado cuando (binario) |
| --- | --- | --- |
| F-0 · Batería | Campaña de defectos inyectados y pruebas de propiedades sobre el F actual | La campaña da su tasa de detección por clase; las propiedades pasan o sus fallos quedan como hallazgos |
| F-1 · Tipos de acción | Deducción desde G, cantidad libre, protección verificada, conjuntos de cobertura (cambio 47, CT-G-08) | Dos ventas no consumen dos veces la misma posición; cerrar una cobertura se trata como aumentar |
| F-2 · Políticas y niveles | Una política por cartera y una global, el más restrictivo gana, contadores que no se reinician | Las propiedades de la idea 2 pasan; un cambio de libro no reinicia contadores |
| F-3 · Reserva y estado incierto | Reserva indivisible compartida con D y E; `DESCONOCIDO` frente a `RECHAZADO` | Las pruebas de concurrencia (idea 3) pasan; una orden sin confirmación conserva su reserva |
| F-4 · Aportación | Ciclo de aportación del cambio 78 | El ciclo no se puede repetir; una orden que aleja el conjunto del mandato se veta |
| F-5 · Controles de T-74 | Volumen medio diario, liquidez, coste y margen, exposición compartida mirando dentro de los fondos | A medida que K sirva sus datos; sin composición, `DESCONOCIDO` con presupuesto conservador |
| F-6 · Sombra | F en sombra para relajar | Una regla relajada no se activa sin su informe de diferencias y la aprobación del operador |

## 6. Qué decide el operador

1. Ratificar este diseño, y los cambios 47 y 78 de la Enmienda 5.
2. Los conjuntos de cobertura y las condiciones para cerrar sus patas.
3. La precisión del §11 («sin confirmación = no ejecutada»): `DESCONOCIDO` conserva la reserva, `[PROPUESTO]`.
4. Los valores de las políticas por cartera (P-03), con el asesor de configuración del Broker.
5. La política de eventos catalizadores en táctica, si se quiere.

## 7. Qué no se hace

- No se cambian la Constitución, CT-G-08 ni `control_f.py` sin autorización y su ticket.
- F no calcula rentabilidades ni lee tesis, y no consume la salida de M.
- Ninguna regla se relaja sola, y no se promete una pérdida máxima.
