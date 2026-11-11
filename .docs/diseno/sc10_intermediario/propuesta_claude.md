# Intermediario y adaptadores (SC-10): a quién confiar las órdenes (propuesta de diseño de Claude)

De: Claude, 11-11-2026. Estado: **PROPUESTA PARA DISCUTIR**. No hay nada que implementar: el operador está decidiendo la arquitectura de los bloques antes de construir (relevo de Astra, §0 bis). Copia en el repositorio del documento que el operador revisó con Claude. Los ejemplos de entidades no son una recomendación de inversión.

## 1. Respuesta corta

El intermediario custodia el dinero, ejecuta las órdenes y guarda los stops cuando el robot falla (§8). Ningún bloque lo conoce: todos hablan con un puerto de SC-10 (D-08). Hoy no hay intermediario elegido. El operador decidió seguir con el simulador hasta rellenar la ficha de restricciones reales (P-05), y es lo único que bloquea la Fase 3.

Idea central: **ningún intermediario es el mejor para las tres carteras a la vez.** El que tiene acceso por programa y stops nativos no suele ofrecer traspasos entre fondos ni información fiscal española, y al revés. Se propone:

1. **Criterios eliminatorios y ponderados por cartera,** que el operador aplica al elegir.
2. **Dos intermediarios como opción por defecto:**
    - uno con acceso por programa para trading y táctica;
    - una entidad española con fondos traspasables para el largo plazo, en L1: el robot prepara la orden y el operador la ejecuta y la registra.

    Antes de decidir, SC-9 cuantifica si compensa tenerlo todo en uno.
3. **Siete puertos con reglas comunes:** idempotencia, estados desconocidos tratados con cuidado, perfil de capacidades por proveedor y un simulador con la misma interfaz.
4. **Una escalera de pruebas** antes de confiarle dinero, de la cuenta de demostración a la lectura real con clave de solo lectura y, después, a dinero real en pequeño.

## 2. Por qué el intermediario mueve la rentabilidad

| Factor | Ejemplo | Qué cuesta o protege |
| --- | --- | --- |
| Cambio de divisa | Un comparador cifra el de un intermediario internacional en torno al 0,002 %; muchos bancos cobran bastante más | En trading de divisas y en activos fuera del euro, se paga en cada operación |
| Comisiones | Desde 0 hasta unos pocos euros por orden según la entidad | Pesan más cuanto más se opera |
| Traspasos entre fondos | Solo en entidades que comercializan fondos traspasables | El diferimiento fiscal de SC-9: un 8,7 % más en 20 años en su ejemplo |
| Stops nativos | La orden de protección vive en el intermediario | Protege aunque el robot se caiga (§8) |
| Acceso por programa | Permite L2, conciliar y leer posiciones solo | Sin él, todo es L1 con trabajo manual |
| Información fiscal española | Una entidad española practica retenciones e informa a Hacienda; una extranjera, no | Trabajo y riesgo de error al declarar, y el modelo 720 si se supera su umbral |
| Protección del inversor | La irlandesa cubre el 90 % de la pérdida hasta 20.000 € si la entidad quiebra | Cuánto conviene tener en cada entidad |
| Intereses del efectivo | Varían mucho entre entidades | Rentabilidad del dinero que espera |

La protección cubre la quiebra de la entidad, no las caídas del mercado. Fuente de la cobertura irlandesa: [Interactive Brokers Irlanda](https://interactivebrokers.ie/es/general/security-investor-protection.php). Fuente del cambio de divisa, la fiscalidad y los traspasos: [comparativa de octubre de 2026](https://financialexpertclass.com/?p=3553).

## 3. Qué hay hoy y qué falta

**Decidido en la Constitución:**

- Puertos independientes del proveedor para intermediario, datos, avisos y modelos de IA, con perfil de capacidades y simulador propio (SC-10, D-08, D-41).
- Ficha de restricciones reales a cargo del operador (Fase 0).
- El intermediario es la segunda fuente de precios, posiciones y saldos (SC-2, P15).
- Stops como órdenes nativas siempre que se pueda (§8).
- Claves separadas de lectura y de operación, esta con límites de importe y frecuencia en el propio intermediario (§11).
- Una discrepancia sin explicar con el intermediario dispara el kill-switch.
- Conexión real en la Fase 3, en L1.

**En código:** el simulador de G y el registro de operaciones manuales (CT-G-14). Pendientes: que el simulador dispare stops (T-14), la autenticación de actores (T-01) y que L0 no pueda enviar órdenes reales (T-30).

**Falta:**

- Los criterios de elección.
- Uno o dos intermediarios.
- La lista de puertos con sus reglas.
- Qué se hace sin acceso por programa.
- La escalera de pruebas y el plan si el intermediario cae.

## 4. Criterios de elección

**E** = eliminatorio (sin él, no sirve para esa cartera); **Alto**, **Medio** y **Bajo** = peso al comparar. Valores de partida [PROPUESTO].

| Criterio | Trading | Táctica | Largo plazo |
| --- | --- | --- | --- |
| Regulada en la UE, con dinero y valores del cliente separados | E | E | E |
| Acceso por programa para operar y leer | E | Alto (E para L2) | Bajo (L1 manual vale) |
| Cuenta de demostración con la misma interfaz | E | Alto | Bajo |
| Stops nativos y órdenes OCO | E | E | Bajo |
| Claves separadas de lectura y operación, con límites en la entidad | Alto | Alto | Medio |
| Cuenta multidivisa y coste de cambio | Alto | Alto | Medio |
| Comisiones por orden | Alto | Medio | Bajo |
| Fondos de inversión traspasables | — | Bajo | Alto |
| Retenciones e información fiscal españolas | Medio | Medio | Alto |
| Protección del inversor (importe cubierto) | Medio | Medio | Alto |
| Estabilidad de la conexión y su historial de caídas | Alto | Medio | Bajo |
| Datos de mercado incluidos y su licencia (K) | Medio | Medio | Bajo |
| Intereses del efectivo | Bajo | Medio | Medio |
| Facilidad para cerrar la cuenta y llevarse los valores | Medio | Medio | Alto |

**Cómo se decide:** se descarta lo que no pasa los eliminatorios, se puntúa el resto y SC-9 añade el coste fiscal de cada opción. La decisión es del operador, en la ficha de restricciones reales.

## 5. Uno o dos intermediarios, siempre detrás de un puerto

Diagrama del documento («Ningún bloque ve al intermediario: todo pasa por un puerto»):

- **Bloques:** G es el único que envía órdenes; F, K y N leen posiciones y datos; los agentes piden modelos de IA.
- **SC-10, siete puertos:** órdenes; posiciones y saldos; ejecuciones y extractos; datos de mercado; avisos; modelos de IA; operador (L1 manual).
- **Proveedores:** intermediario con acceso por programa (trading y táctica); simulador (L0 y pruebas); proveedores de IA intercambiables; entidad española (largo plazo, traspasos), que solo devuelve extractos.
- **L1 manual:** SC-10 prepara la orden lista para teclear; el operador la teclea en la entidad y la registra.

Cambiar de proveedor solo cambia el adaptador.

## 6. Tipos de candidatos

No es una recomendación: son tres tipos de entidad, con un ejemplo conocido de cada uno, para aplicar los criterios. Datos de fuentes públicas de 2026 que hay que confirmar en la ficha de restricciones.

| Tipo | Ejemplo | A favor | En contra |
| --- | --- | --- | --- |
| Intermediario internacional con acceso por programa | Interactive Brokers (Irlanda) | Acceso por programa y cuenta de demostración; stops nativos y OCO; divisas y multidivisa; cambio muy barato | Sin retenciones ni información fiscal españolas; modelo 720 por encima de su umbral; sin traspasos con ventaja fiscal; protección del 90 % hasta 20.000 € |
| Entidad española de fondos indexados | MyInvestor | Traspasos entre fondos; información fiscal automática; custodia en España, sin modelo 720 | No consta acceso por programa para operar; divisas limitadas; todo en L1 |
| Bróker europeo de bajo coste sin acceso oficial por programa | DEGIRO | Comisiones bajas y extractos compatibles con el IRPF | Sin acceso oficial por programa (no vale para L2); sin traspasos |

Fuentes: [comparativa de octubre de 2026](https://financialexpertclass.com/?p=3553) e [Interactive Brokers Irlanda](https://interactivebrokers.ie/es/general/security-investor-protection.php).

**Lo que sale de aplicar los criterios:** trading y táctica necesitan el primer tipo; el largo plazo gana con el segundo por los traspasos y la fiscalidad. De ahí la opción por defecto de dos intermediarios.

**Tenerlo todo en uno** también es posible: el largo plazo en ETF en el intermediario internacional. Se pierde el diferimiento fiscal de los traspasos, se añade el modelo 720 y se concentra el riesgo de una sola entidad, a cambio de menos trabajo manual. SC-9 y el planificador calculan cuál compensa con los importes del operador.

## 7. Los puertos

| Puerto | Qué hace | Quién lo usa |
| --- | --- | --- |
| Órdenes | Enviar, modificar y cancelar; stops nativos y OCO | Solo G |
| Posiciones y saldos | Lectura con la clave de solo lectura | G, F (segunda fuente), N |
| Ejecuciones y extractos | Ejecuciones, comisiones, dividendos y retenciones, por programa o importando el fichero de la entidad | G (conciliación y libro fiscal), SC-9 |
| Datos de mercado | Precios y volumen como segunda fuente | K |
| Avisos | Canal fuera del chat | N, vigilante |
| Modelos de IA | Proveedor intercambiable, con coste y capacidades | Todos los agentes |
| Operador | Para L1 sin acceso por programa: prepara la orden lista para teclear y recoge la confirmación (CT-G-14) | G y N |

**Reglas comunes.**

1. **Perfil de capacidades por proveedor:** tipos de orden, horarios, límites, retrasos y errores conocidos. Los bloques preguntan al perfil, no suponen.
2. **Idempotencia:** cada orden lleva un identificador propio; repetir un envío nunca crea dos órdenes.
3. **Estado desconocido:** si una orden se envía y no hay respuesta, se consulta antes de reenviar. Mientras tanto la orden cuenta como enviada, nunca como no enviada.
4. **Falla cerrado:** una respuesta que no se entiende es un error, no un éxito; reintentos acotados y paso a L1 si afecta a G (§11).
5. **El simulador usa la misma interfaz** e incluye lo que falla en la realidad: stops disparados (T-14), huecos, rechazos, ejecuciones parciales y desconexiones.
6. **Versión por adaptador:** cambiar de intermediario o de versión de su interfaz no toca ningún bloque, pero sí exige repetir la escalera de pruebas.

## 8. Cómo se prueba antes de confiarle dinero

Cinco peldaños; no se pasa al siguiente sin cumplir el anterior. Duraciones [PROPUESTO].

| Peldaño | Qué se hace | Para pasar |
| --- | --- | --- |
| 1. Simulador | Batería de fallos: stops disparados, huecos, rechazos, parciales, desconexiones, respuestas duplicadas | Ningún fallo sin tratar; cero órdenes duplicadas |
| 2. Cuenta de demostración | El adaptador real contra la demostración de la entidad, durante semanas | Comportamiento igual que el simulador; diferencias documentadas en el perfil de capacidades |
| 3. Lectura real | Solo la clave de lectura sobre la cuenta real: conciliación diaria sin enviar órdenes | Conciliación limpia durante el periodo fijado |
| 4. Dinero real en pequeño, en L1 | Cada orden aprobada por el operador; stops nativos verificados en la entidad | Simulacros de kill-switch, de caída del robot y de caída de la conexión superados (Fase 3) |
| 5. Tramos | Más capital y, después, L2 por la promoción normal | Criterios de promoción de la Constitución |

**Si el intermediario cae.**

- Los stops nativos siguen en la entidad.
- El vigilante avisa por el canal fuera del chat.
- La cartera baja a L1.
- El operador puede actuar en la web o el teléfono de la entidad, con una guía preparada.

El segundo intermediario no sirve de respaldo del primero: cada uno guarda posiciones distintas.

**Si la entidad cambia su interfaz o sus condiciones:** se repite desde el peldaño 2.

## 9. Precisión, consumo y orden

**Precisión.** G mide cada intermediario:

- precio conseguido frente al esperado;
- órdenes rechazadas;
- tiempo de respuesta;
- tiempo sin servicio;
- diferencias en la conciliación.

I compara el coste total por cartera y avisa si otra entidad compensaría.

**Consumo:** cero tokens. El coste son las comisiones, el cambio de divisa y, si hace falta, una suscripción de datos que K debe justificar.

**Orden:**

- **Ya (Fase 0):** el operador aplica los criterios y rellena la ficha de restricciones reales.
- **Fases 1 y 2:**
    - el simulador con stops disparados (T-14) y la batería de fallos;
    - los puertos con su perfil de capacidades;
    - importar extractos para el largo plazo en L1;
    - el peldaño 2 con la entidad elegida.
- **Antes de la Fase 3:** lectura real (peldaño 3), autenticación (T-01) y bloqueo de órdenes reales en L0 (T-30).
- **Fase 3:** dinero real en pequeño y tramos.

## 10. Preguntas para el operador

Todas son [PROPUESTO]; ninguna se decide sin el operador.

1. **Dos intermediarios por defecto** (uno con acceso por programa para trading y táctica; una entidad española con fondos traspasables para el largo plazo), salvo que SC-9 demuestre que uno solo compensa.
2. **Los criterios eliminatorios** del §4.
3. **Límites de la clave de operación** fijados en la propia entidad: importe por orden y órdenes por día.
4. **Duración** de la demostración y de la lectura real antes del dinero.
5. **Largo plazo en L1 manual de forma permanente** si la entidad no tiene acceso por programa.
6. **Cuánto dinero tener como máximo en cada entidad,** a la vista de su protección.
