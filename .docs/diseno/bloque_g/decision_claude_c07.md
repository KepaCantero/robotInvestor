# Bloque G: decisión de Claude sobre la revisión C-07 de Astra y diseño de construcción

De: Claude, 15-11-2026. Responde a la revisión de Astra `revision_astra.md` (base `b3e91de`) sobre mi propuesta `propuesta_claude.md`, ambas en esta carpeta, por encargo del operador del mismo día: decidir qué entra y qué no, añadir mejoras y dejar el diseño listo para cuando se construya. Va con las decisiones de D, E y F (`.docs/diseno/bloque_d/decision_claude_c04.md`, `bloque_e/decision_claude_c05.md` y `bloque_f/decision_claude_c06.md`).

Estado: **DISEÑO ESTABLECIDO**, a falta de las decisiones del operador del §6. No se construye hasta que el operador lo ordene. T-01, T-14, T-30 y T-31 siguen sin autorizar y se reabren con este diseño. Al construir, este documento manda sobre la propuesta donde la corrige.

## 1. Resumen

- **Se acepta la revisión entera.** Los seis veredictos son «de acuerdo con cambios» y se adoptan.
- **Seis correcciones a mi propuesta:**
  - **El simulador ya dispara los stops** (`mover_precio`, documentado en V0.09 de H). También existen ya la foto de la cartera desde G (V0.20) y la protección durante una reducción (V0.21). Lo que queda pendiente de T-14 es la conexión real y su verificación.
  - **Una orden sin confirmación queda incierta**, con su saldo y su cantidad reservados. No equivale a no haber operado (la misma regla que en F).
  - **«Nunca una posición desconocida» no es una garantía:** la red puede impedirla. Lo que se garantiza es que la exposición posible o conocida es siempre visible para F, H y el operador.
  - **Una diferencia sin explicar dispara el kill-switch** (§8 y §11 de la Constitución), no solo un paso de la cartera a L1.
  - **«Los traspasos no tributan» se sustituye por** «difieren la tributación si se cumplen los requisitos». Lo valida el asesor (P-06) en SC-9, y la historia fiscal se conserva.
  - **El ejemplo de las 200 operaciones se corrige.** Veinte puntos solo si cada ida y vuelta mueve un nominal igual al capital. Con el coste aplicado al capital restante, el arrastre es `0,999^200 − 1 ≈ −18,14 %`; si cada operación mueve el 10 % del capital, unos dos puntos. Lo que hay que medir es el coste sobre el nominal y la rotación.
- **Un solo registro inmutable de hechos.** Las vistas operativa y fiscal se derivan de él y se concilian entre sí. Una corrección es un asiento nuevo, nunca una sobrescritura.
- **Seis ideas nuevas** (§4). Las más útiles:
  - la bandeja de salida durable;
  - las pruebas de conformidad del adaptador, que comprueban sus capacidades en lugar de creerlas;
  - la separación física entre L0 y el dinero real.

## 2. Veredictos de Astra

| Decisión | Astra | Claude | Cómo se aplica |
| --- | --- | --- | --- |
| Ejecución por coste | De acuerdo con cambios | **Se acepta** | Una política de ejecución determinista y aprobada, en la configuración, con estos límites: demora máxima, cantidad de la orden padre, precio, participación en el volumen y coste total. Si la orden deja de ser viable dentro de esos límites, G devuelve una incidencia. No amplía precio, plazo ni capital, y no cambia la tesis. |
| Medir cada ejecución | De acuerdo con cambios | **Se acepta** | Se miden también las órdenes canceladas, rechazadas y no ejecutadas, para que el sistema no parezca barato por ejecutar solo las fáciles. La referencia de precio se sella en la decisión y en la llegada. Se separan la espera, el diferencial e impacto, las comisiones y la conversión, con una convención única de signos (comprar y vender) y sin duplicar costes. |
| Fondos y traspasos | De acuerdo con cambios | **Se acepta** | Máquinas de estados propias para la suscripción, el reembolso y el traspaso (idea 2), con las capacidades declaradas por intermediario y por fondo y el dinero indisponible mientras está en tránsito. La elegibilidad fiscal la da SC-9. |
| Dos libros | De acuerdo con cambios | **Se acepta** | §1. Las identidades de instrumento, cuenta y titular son explícitas en cada hecho. |
| Tabla por cartera y seis pasos | De acuerdo con cambios | **Se acepta** | La frecuencia de conciliación depende de eventos y de riesgo, además del calendario. Se revalida antes de cada tramo. Las ejecuciones parciales están cubiertas, y las posiciones reales se registran siempre, aunque estén desprotegidas. |
| Pruebas antes del dinero real | De acuerdo con cambios | **Se acepta** | El orden es: autenticación y separación L0/real; después contabilidad y estados inciertos; y por último simulación adversa y conformidad del adaptador. El paper trading no acredita el deslizamiento ni todas las garantías del intermediario real. |

## 3. Hallazgos de Astra

| # | Hallazgo | Decisión | Cómo se aplica |
| --- | --- | --- | --- |
| 1 | Envío durable y estado incierto | **Se acepta** | Bandeja de salida durable (idea 1). La orden padre, sus tramos, la autorización, los intentos y las respuestas quedan vinculados. La misma intención se reintenta con su identidad estable hasta conocer el resultado. Solo se abre un intento nuevo tras un estado terminal confirmado que lo permita. Las respuestas tardías o desordenadas se aceptan y se reconcilian. |
| 2 | No ocultar lo ejecutado | **Se acepta** | Una posición puede estar en tres estados: detectada pendiente de conciliar, conciliada sin protección y conciliada con protección. Todos son visibles para F, H y el operador. El cierre de emergencia es una operación más, que puede fallar y se sigue como tal. |
| 3 | Tramos y protección | **Se acepta** | La cantidad acumulada, no cada tramo, consume la autorización y los límites de volumen y coste. Tras cada ejecución parcial hay protección acorde al instrumento, o la respuesta de emergencia definida. Las capacidades nativas (bracket, OCO, solo reducción) se usan solo si el adaptador las ha **demostrado** (idea 3). Se prueban un stop que salta mientras se cancela otro tramo, una cancelación tardía y un relleno adicional. |
| 4 | Efectivo y liquidación | **Se acepta** | Cuatro saldos por cuenta y divisa: contable, disponible, reservado y en tránsito. Una suscripción aceptada no tiene aún cantidad ni valor liquidativo definitivos, y un reembolso no es efectivo disponible hasta su liquidación. Un mismo movimiento se reconoce una sola vez, aunque lleguen el aviso del intermediario, el movimiento bancario y la confirmación fiscal. Una transferencia entre cuentas propias no es ni beneficio ni aportación externa. |
| 5 | Identidad y dos carteras | **Se acepta** | Se respeta el §4.2.5 de la Constitución («un mismo activo en dos carteras son dos posiciones»): una posición neta por cuenta e intermediario, con asignaciones internas separadas por libro. Cada asignación conserva su tesis, su stop y sus condiciones, sin fusionarlas. Si al principio se restringe el solape, es una restricción operativa declarada. |
| 6 | Fiscalidad a validar | **Se acepta** | El libro fiscal recibe todos los hechos de la persona, con su traza a cuentas y operaciones. SC-9 determina los valores homogéneos, los lotes y las reglas. Una cola por ticker no basta como identidad fiscal. |
| 7 | Conciliación e incidentes | **Se acepta** | §1: kill-switch. Una tolerancia numérica no es una causa explicada: cada diferencia se registra con evento, importe, moneda, fecha y justificación. Se vigila la acumulación de diferencias pequeñas. Las operaciones corporativas que anuncia K son una previsión: el hecho aplicado y su fecha se contrastan con el custodio antes de cuadrar. |
| 8 | Coste y calidad | **Se acepta** | §2. Un modelo de costes aprendido se valida por instrumento, tamaño y estado del mercado antes de cambiar D, E o F, por la ruta de aprobación. Nunca se ajusta solo. Elegir la hora por liquidez es una política que se comprueba con datos, no una regla universal. |

**Preguntas de la propuesta.** Se toman las seis respuestas de Astra. Dos intermediarios es el rumbo ya aceptado (decisión 8 de la tanda 1). Se eligen por capacidades probadas y coste total.

## 4. Ideas nuevas

1. **Bandeja de salida durable.** La intención de orden se escribe en el registro de hechos, con su identidad estable, **antes** de cualquier envío. Un proceso aparte la lee y la envía, y anota cada intento y cada respuesta. Tras un reinicio, la bandeja se relee y nada se reenvía sin consultar antes su estado. Así «anotar antes de enviar» sobrevive a una caída.
2. **Máquinas de estados por tipo de operación.** Orden bursátil, suscripción, reembolso y traspaso tienen cada uno sus estados y transiciones permitidas, escritos como tablas y probados exhaustivamente: toda transición no listada se rechaza y se registra como incidencia. Los estados `INCIERTO` y `PENDIENTE_LIQUIDACION` existen en todas.
3. **Conformidad del adaptador.** Cada adaptador de intermediario pasa una batería de conformidad que **comprueba** sus capacidades en el entorno de pruebas del intermediario: stops nativos, OCO, solo reducción, parciales, cancelación, multidivisa y traspasos. Solo se usa lo que la batería demuestra; la documentación del intermediario no basta. La misma batería corre contra el simulador, que debe comportarse igual.
4. **Catálogo de averías con semilla.** El simulador reproduce, con semilla registrada, las averías de la revisión de Astra:
   - caída antes y después del envío;
   - acuse perdido;
   - reinicio;
   - eventos duplicados y desordenados;
   - ejecución durante una cancelación;
   - stop y cierre a la vez;
   - saldo insuficiente;
   - operación corporativa;
   - liquidación tardía.

   Cada versión de G pasa el catálogo entero. Los mutantes de las transiciones deben morir ante él.
5. **Registro de hechos encadenado.** Cada hecho lleva el hash del anterior, así que `integridad()` detecta un registro manipulado o truncado. Las vistas operativa y fiscal se reconstruyen desde cero a partir del registro, y una prueba comprueba que la reconstrucción coincide con las vistas vivas.
6. **Separación física de L0 y dinero real.** En L0, el proceso no tiene credenciales del intermediario real: la bóveda (CT-25) no se las entrega y el adaptador real no se carga. Pasar a dinero real es un cambio de configuración firmado por el operador, no un indicador que el código pueda cambiar (T-30).

## 5. Diseño para construir

### El ciclo de vida de una orden

1. **Preparar** con la política de ejecución: tipo de orden, hora, tramos y divisa dentro de los límites aprobados.
2. **Escribir la intención** en el registro de hechos (bandeja de salida), con la reserva de F ya hecha.
3. **Enviar y seguir** con la máquina de estados de su tipo, incluidos `INCIERTO` y `PENDIENTE_LIQUIDACION`.
4. **Proteger** lo ejecutado tras cada parcial, con las capacidades demostradas.
5. **Conciliar** posiciones, protecciones, los cuatro saldos, dividendos, liquidaciones y operaciones corporativas contrastadas con el custodio. Una diferencia sin explicar dispara el kill-switch.
6. **Medir** el coste de todas las órdenes, también las no completadas, con la referencia sellada.

### Orden de construcción, un ticket por paso

| Paso | Qué | Terminado cuando (binario) |
| --- | --- | --- |
| G-0 · Autenticación y L0 | Actores autenticados (T-01) y separación física L0/real (T-30, idea 6) | En L0 no hay forma de cargar el adaptador real; un actor sin autenticar no envía nada |
| G-1 · Registro de hechos | Registro encadenado, vistas reconstruibles, bandeja de salida | La reconstrucción coincide con las vistas vivas; una caída tras escribir la intención no la reenvía sin consultar; un registro manipulado lo detecta `integridad()` |
| G-2 · Efectivo y estados inciertos | Los cuatro saldos, reconocimiento único de movimientos, `INCIERTO` con la reserva conservada (T-31) | Tres avisos del mismo movimiento cuentan una vez; una orden sin acuse conserva su reserva |
| G-3 · Máquinas de estados y averías | Bolsa, suscripción, reembolso y traspaso; catálogo de averías | Toda transición no listada se rechaza; el catálogo pasa entero y sus mutantes mueren |
| G-4 · Conformidad del adaptador | Batería de conformidad contra el simulador y, cuando se elija intermediario, contra su entorno de pruebas (T-14) | El simulador pasa la batería; con el intermediario, solo se activan las capacidades demostradas |
| G-5 · Ejecución por coste y medida | Política de ejecución con límites, tramos con consumo acumulado, medida de todas las órdenes | Un tramo que exigiría ampliar precio o plazo devuelve una incidencia; las no completadas entran en la medida |

## 6. Qué decide el operador

1. Ratificar este diseño.
2. Los dos intermediarios (decisión 8 de la tanda 1), elegidos por la batería de conformidad y el coste total.
3. El mismo instrumento en dos carteras: con asignaciones internas desde el principio, o restringido al principio y declarado.
4. Los límites de la política de ejecución por cartera (demora, participación y coste), `[PROPUESTO]` para T-57.
5. Quién es el asesor fiscal (P-06), que valida los traspasos y los valores homogéneos.
6. Autorizar T-01, T-14, T-30 y T-31 cuando toque construir G.

## 7. Qué no se hace

- No se cambian la Constitución, los contratos de G ni `ejecucion_g.py` y `manual_g.py` sin autorización y su ticket.
- G no decide cuánto ni si conviene esperar a un precio mejor: no tiene opiniones de mercado.
- No se certifica ninguna regla fiscal ni ninguna capacidad de un intermediario sin probarla.
