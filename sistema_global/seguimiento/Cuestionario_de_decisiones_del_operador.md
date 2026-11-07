# Cuestionario de decisiones del operador — Robot Inversor

Nov 5, 2026 · @Dani

## Cómo usar este cuestionario

Son 16 decisiones que solo puedes tomar tú. Cada una está explicada sin jerga y trae un **valor de partida prudente** que puedes aceptar marcando una casilla. No hace falta ser experto: si aceptas todos los valores de partida, el sistema arranca en su modo más seguro y podrás cambiarlos más adelante.

**Aviso.** Los valores son orientativos y de diseño del sistema. No son asesoramiento financiero, fiscal ni legal. Dependen de tu situación personal; para la fiscalidad y para decidir cuánto dinero dedicar, consulta a un asesor.

**Cómo rellenarlo.**

1. Lee «En palabras sencillas».
2. Marca «Acepto el valor de partida» o escribe el tuyo.
3. Si dudas, marca «No lo sé aún»: usaré el valor de partida y quedará anotado como provisional.

**Qué es urgente.**

| Cuándo | Pendientes | Por qué |
| --- | --- | --- |
| **Para empezar la Fase 1** | P-05, P-16, P-03, P-11, P-08, P-07 | Sin ellos no se pueden diseñar la ejecución ni los controles |
| **Antes de operar con dinero real** | P-01, P-12, P-13, P-02, P-14, P-06 | Fijan cuánta libertad tiene el robot y cómo se vigila |
| **Cuando toque** | P-04, P-15, P-09, P-10 | Afectan a fases posteriores o son detalles de nombres |

**Tus datos base.** Varias respuestas dependen de estas. Escribe lo que sepas; si no lo sabes, déjalo en blanco.

| Pregunta | Para qué sirve | Mi respuesta |
| --- | --- | --- |
| ¿Cuánto dinero total pondrías en el robot? (en euros) | Convierte los porcentajes de los límites en euros | Poco al principio y aportaciones mensuales; importe aún sin decidir (7-11-2026). Los límites van en porcentaje hasta entonces |
| ¿Qué porcentaje es de tu patrimonio líquido total? | Detecta si el riesgo es excesivo para ti |  |
| ¿Cuánto podrías perder sin que afecte a tu vida? (euros y porcentaje) | Fija el límite máximo de pérdida |  |
| ¿Cuándo podrías necesitar ese dinero? (meses o años) | Decide el horizonte de cada cartera | Más de 20 años invertido (7-11-2026) |
| ¿Experiencia invirtiendo? (ninguna, algo, mucha) | Decide lo prudente que debe ser el arranque |  |
| ¿Cuánto tiempo puedes dedicar a revisar avisos? (por día o semana) | Fija el nivel de autonomía posible |  |
| ¿En qué zona horaria estás y en qué horas estás disponible? | Define el horario supervisado |  |
| ¿Cómo repartirías el capital entre trading, táctica y largo plazo? (porcentajes) | Reparto de capital entre carteras |  |

## Bloque 1 · Tu perfil y tus carteras

### P-16 · Por dónde empezar (Fase 1)

**En palabras sencillas.** Antes de construir todo, se construye un camino completo y pequeño: un tipo de activo y una cartera, de principio a fin y sin dinero real.

**Valor de partida.** Divisas y cartera táctica. Es lo más rápido, porque los bloques A y B de divisas ya existen y el analista de divisas está parcialmente hecho.

**Mi decisión.**

- [ ] Acepto el valor de partida (divisas y cartera táctica)
- [ ] Prefiero otro tipo de activo o cartera (cuál y por qué):
- [ ] No lo sé aún

### P-03 · El mandato de cada cartera

**En palabras sencillas.** Es el «reglamento» de cada cartera: para qué sirve, cuánto riesgo admite y qué puede comprar. El robot no puede salirse de él.

**Por qué importa.** Los controles de riesgo se calculan con estos valores. Si son demasiado laxos, el control no protege; si son demasiado estrictos, el robot casi no opera. Por eso los valores de partida son prudentes.

**Valores de partida.** Orientativos; la columna del trading está pensada para capital pequeño.

| Parámetro | Qué significa | TRADING | TÁCTICA | LARGO PLAZO |
| --- | --- | --- | --- | --- |
| Objetivo | Para qué sirve la cartera | Validar estrategias con capital pequeño | Aprovechar oportunidades de semanas a meses con riesgo acotado | Hacer crecer el patrimonio a años vista con riesgo moderado |
| Alternativa de no hacer nada (benchmark) | Con qué se compara; si no la supera, no se actúa | Efectivo | Efectivo | Índice amplio de renta variable mundial |
| Caída máxima aceptada de la cartera | Pérdida desde el máximo a partir de la cual se para todo | 8 % | 10 % | 15 % |
| Riesgo máximo por operación | Lo que se pierde si salta el stop, como % de la cartera | 0,5 % | 1 % | No aplica (se limita el peso) |
| Peso máximo por posición o emisor | Cuánto de la cartera puede ir a un solo activo | 10 % | 15 % | 5 % |
| Exposición neta máxima a una misma divisa | Para no depender de una sola moneda | 30 % | 30 % | 20 % |
| Efectivo mínimo | Parte de la cartera que siempre queda sin invertir | 20 % | 10 % | 5 % |
| Apalancamiento | Invertir más dinero del que tienes | Cero | Cero | Cero |
| Tipos de activo admitidos | Qué puede comprar | Divisas, índices y fondos líquidos | Divisas al principio; después renta variable, índices y fondos | Renta variable, renta fija, fondos, índices y monetarios |
| Excluidos al principio | Lo que no se compra hasta decidirlo | Derivados, criptoactivos, alternativos | Derivados, criptoactivos, alternativos | Derivados, criptoactivos, alternativos |
| Revisión o rebalanceo | Cada cuánto se revisa el reparto | No aplica | Semanal | Trimestral, o al desviarse 5 puntos |
| Criterio de salida | Cuándo se sale de una posición | Stop o regla de la estrategia | Stop, objetivo o caducidad de la tesis | Invalidez de la tesis o rebalanceo |
| Nivel de autonomía inicial | Qué libertad tiene el robot | L0 y después L1 | L0 y después L1 | L0 y después L1 |

**Mi decisión.**

- [ ] Acepto los valores de partida
- [ ] Quiero cambiar estos (parámetro, cartera y valor):
- [ ] No lo sé aún

### P-04 · Horizontes de la táctica y del largo plazo

**En palabras sencillas.** Cuánto tiempo se espera mantener una inversión en cada cartera. El trading ya está fijado en días y semanas.

**Valor de partida.** Táctica: de 2 semanas a 6 meses. Largo plazo: 3 años o más.

**Mi decisión.**

- [ ] Acepto el valor de partida
- [ ] Quiero otros horizontes (táctica y largo plazo):
- [ ] No lo sé aún

### P-15 · Cuánto se puede estimar en cada tipo de activo (clases Q, S, K)

**En palabras sencillas.** Para comparar opciones de tipos distintos, el sistema necesita saber en qué tipos de activo se pueden estimar probabilidades con datos fiables. **Q**: hay mucha historia y modelos fiables. **S**: hay historia parcial o supuestos fuertes. **K**: no hay base fiable para probabilidades, y solo se compara por riesgo, liquidez y coste.

**Por qué importa.** Ante la duda conviene ser más prudente (S o K), porque se evita dar una falsa precisión.

**Valores de partida.**

| Tipo de activo | Clase propuesta | Motivo |
| --- | --- | --- |
| Renta variable | Q | Mucha historia de precios y datos |
| Renta fija | S | Depende de crédito y liquidez de cada emisión |
| Divisas | Q | Mucha historia y mercados muy líquidos |
| Materias primas | S | Historia larga, pero muy condicionada por factores externos |
| Índices bursátiles | Q | Mucha historia y diversificación incorporada |
| Fondos y vehículos colectivos | Q | Se pueden evaluar con su historia de cotización |
| Derivados | S | Dependen de supuestos de modelo |
| Inmobiliario cotizado | S | Mezcla de bolsa y mercado inmobiliario |
| Criptoactivos | K | Historia corta y comportamiento muy inestable |
| Capital privado y alternativos | K | Poca información y baja liquidez |
| Monetarios y liquidez | Q | Riesgo bajo y datos claros |
| Tipos de interés, crédito y volatilidad | S | Modelos con supuestos fuertes |

**Mi decisión.**

- [ ] Acepto las clases propuestas
- [ ] Quiero cambiar estas (tipo y clase):
- [ ] No lo sé aún

## Bloque 2 · Límites en euros y autonomía

### P-11 · Límites duros en euros

**En palabras sencillas.** Son topes en euros que ningún agente puede superar, ni aunque esté muy seguro. Son la última barrera si algo falla en los cálculos o en los datos. Se expresan como porcentaje de tu capital en el robot para que valgan con cualquier cantidad.

**Por qué importa.** Es el control más importante: no depende de modelos, de opiniones ni de datos que puedan estar mal.

**Valores de partida.** El ejemplo supone 10.000 € en el robot; sustitúyelo por tu cifra.

| Límite | Qué significa | Valor de partida | Ejemplo con 10.000 € |
| --- | --- | --- | --- |
| Importe máximo por orden | Una sola orden nunca supera esto | 5 % del capital | 500 € |
| Entradas máximas por día | Suma de todo lo que se compra en un día | 15 % del capital | 1.500 € |
| Máximo en un solo activo | Sumando todas las órdenes | 10 % del capital | 1.000 € |
| Pérdida máxima diaria (global) | Si se alcanza, todo pasa a modo manual | 1,5 % del capital | 150 € |
| Pérdida máxima semanal (global) | Igual, en una semana | 4 % del capital | 400 € |
| Pérdida máxima diaria por cartera | Trading, táctica y largo plazo | 1 %, 1,5 % y 2 % de cada cartera | — |
| Apalancamiento y margen | Dinero prestado para invertir | Cero | 0 € |
| Órdenes máximas por hora | Evita un bucle de órdenes | 10 | — |

**Mi decisión.**

- [ ] Acepto los valores de partida
- [ ] Mi capital en el robot es de \_\_\_\_\_\_ € y quiero cambiar estos límites:
- [ ] No lo sé aún

### P-01 · Qué puede hacer el robot solo en modo semiautónomo (L2)

**En palabras sencillas.** En el modo semiautónomo el robot actúa solo en acciones pequeñas y pide tu aprobación para las grandes. Aquí fijas qué es «pequeño».

**Por qué importa.** Si el umbral es alto, el robot te molesta poco pero arriesga más sin tu permiso. Si es bajo, te pedirá permiso casi siempre.

**Valor de partida.** Acción automática de hasta el **2 % del capital de la cartera** por operación, solo en instrumentos ya admitidos, sin apalancamiento, hasta 3 operaciones automáticas por día. Todo lo demás, con tu aprobación. El modo semiautónomo no se activa antes de la Fase 3.

**Mi decisión.**

- [ ] Acepto el valor de partida
- [ ] Quiero otro umbral (porcentaje y número de operaciones al día):
- [ ] No lo sé aún

### P-12 · Horario de supervisión para el modo autónomo (L3)

**En palabras sencillas.** El modo autónomo solo debe funcionar cuando tú puedas ver los avisos. Fuera de ese horario, el robot baja a semiautónomo y solo actúan los stops que ya están en el intermediario.

**Valor de partida.** El modo autónomo está desactivado hasta la Fase 5. Cuando se active, solo funcionará en el horario que indiques.

**Mi decisión.** (hora de tu zona horaria)

- [ ] Acepto el valor de partida (autónomo desactivado por ahora)
- [ ] Cuando se active, mi horario será de \_\_\_\_\_\_ a \_\_\_\_\_\_, de \_\_\_\_\_\_ a \_\_\_\_\_\_ (días)
- [ ] No lo sé aún

### P-13 · Cuánta diferencia se tolera al cuadrar cuentas

**En palabras sencillas.** El robot compara lo que cree que tienes con lo que dice el intermediario. Comisiones, dividendos o cambios de divisa generan pequeñas diferencias normales. Aquí fijas cuándo una diferencia es normal y cuándo es una alarma que lo para todo. También fijas cuántos días de diferencia se admiten entre dos análisis que se comparan.

**Por qué importa.** Si es demasiado estricto, saltarán alarmas falsas continuamente y acabarás ignorándolas. Si es demasiado laxo, un error real pasa desapercibido.

**Valores de partida.**

| Parámetro | Valor de partida |
| --- | --- |
| Tolerancia por posición | 0,1 % del valor de la posición o 2 €, lo que sea mayor |
| Tolerancia del saldo en efectivo | 5 € o 0,05 % del total, lo que sea mayor |
| Diferencias explicadas | Se aceptan comisiones, dividendos y cambios de divisa que coincidan con el extracto del intermediario |
| Diferencia máxima de fecha entre análisis comparados | Táctica: 1 día hábil. Largo plazo: 5 días hábiles |

**Mi decisión.**

- [ ] Acepto los valores de partida
- [ ] Quiero cambiar estos:
- [ ] No lo sé aún

## Bloque 3 · Cuándo se sube de nivel y cuánto se valida

### P-02 · Cuándo puede el robot ganar más libertad

**En palabras sencillas.** El robot empieza en modo manual (solo asesora). Para pasar a un modo con más libertad tiene que demostrar que funciona bien durante un tiempo. Aquí fijas cuánto tiempo y con qué condiciones. Bajar de nivel es siempre automático e inmediato si algo falla.

**Por qué importa.** Es lo que evita dar libertad al robot por entusiasmo antes de tener pruebas.

**Valor de partida.** Para subir de nivel, en una cartera:

1. Al menos 8 semanas en el nivel actual.
2. Cuentas cuadradas con el intermediario sin alarmas sin explicar.
3. Cero límites incumplidos.
4. Ningún fallo de seguridad.
5. Aprobación expresa tuya.

Las subidas se hacen de una en una y por cartera.

**Mi decisión.**

- [ ] Acepto el valor de partida
- [ ] Quiero otro periodo o condiciones (cuáles):
- [ ] No lo sé aún

### P-14 · Cuántos datos hacen falta antes de fiarse de una medición

**En palabras sencillas.** El sistema mide si sus pronósticos aciertan, pero con pocos casos esa medición no vale nada. Aquí fijas el número mínimo de casos antes de que el sistema use esa medición, y cuánto tiempo dura cada fase de prueba antes de pasar a la siguiente.

**Por qué importa.** Si se fija muy bajo, el sistema se fiará de la suerte. Si se fija muy alto, tardará años en aprender.

**Valores de partida.**

| Parámetro | Valor de partida |
| --- | --- |
| Casos mínimos para usar la calibración | 30 pronósticos resueltos por tipo de activo |
| Fase 1 en simulación (L0) | 20 recorridos completos sin intervención |
| Fase 1 en modo manual (L1) | 4 semanas con cuentas cuadradas |
| Fase 3 con intermediario real | 8 semanas con cuentas cuadradas y simulacros superados |
| Estrategias de trading en paper | Mínimo 8 semanas con resultados dentro del rango del backtest |

**Mi decisión.**

- [ ] Acepto los valores de partida
- [ ] Quiero cambiar estos:
- [ ] No lo sé aún

## Bloque 4 · Cuenta, datos, dinero y avisos

### P-05 · Ficha de restricciones reales: intermediario y datos

**En palabras sencillas.** El robot necesita una cuenta en un intermediario (un broker) y fuentes de datos de mercado. No puedo elegirlos por ti ni conozco tu situación; te dejo una lista de criterios para comparar opciones y una ficha para anotar la que elijas.

**Por qué importa.** Es lo único que bloquea de verdad el arranque de la ejecución y de los datos. Mientras no la rellenes, todo se prueba con un simulador.

**Criterios para elegir un intermediario.** Marca los que exijas.

- [ ] Regulado en el Espacio Económico Europeo, con protección de los fondos del cliente
- [ ] Ofrece los productos que necesitamos al principio (divisas por plazo, futuros o ETC de divisas, fondos cotizados)
- [ ] Tiene una API oficial para consultar saldos y enviar órdenes
- [ ] Permite separar claves de solo lectura y claves de operación, con límites
- [ ] Permite órdenes stop y de límite nativas, que siguen vigentes aunque el robot esté apagado
- [ ] Ofrece cuenta de simulación (paper trading)
- [ ] Cobra comisiones y costes de financiación razonables y transparentes
- [ ] Ofrece extractos descargables para cuadrar cuentas
- [ ] Informa de lo necesario para la declaración de impuestos en España

**Ficha.** Rellénala cuando elijas.

| Dato | Mi respuesta |
| --- | --- |
| Intermediario elegido |  |
| Tipo de cuenta |  |
| ¿Tiene API oficial? ¿Cuál? |  |
| ¿Tiene cuenta de simulación? |  |
| Productos disponibles para empezar |  |
| Comisiones y costes de financiación |  |
| Fuente de datos de mercado y su coste mensual |  |
| Licencia de datos: ¿uso personal permitido? |  |

**Mi decisión.**

- [ ] Rellenaré la ficha: dame una lista corta de preguntas para comparar los intermediarios que yo elija
- [ ] Ya tengo un intermediario (rellenado arriba)
- [x] Seguir con el simulador hasta decidir (7-11-2026)

### P-06 · Impuestos y asesor

**En palabras sencillas.** Las reglas fiscales (por ejemplo, la regla que impide deducir una pérdida si recompras el mismo valor en un plazo corto, o cómo tributan los criptoactivos y las ganancias en divisas) las debe codificar y validar un asesor. Un modelo de lenguaje no es fuente fiable en esto.

**Valor de partida.** Se asume residencia fiscal en España. Hasta que un asesor valide las reglas, el sistema marca el impacto fiscal como estimación y no incluye tratamientos especiales.

**Mi decisión.**

- [ ] Acepto el valor de partida (residencia fiscal en España)
- [ ] Mi residencia fiscal es otra:
- [ ] Ya tengo asesor fiscal
- [ ] Debo buscar un asesor antes de la Fase 2

### P-07 · Presupuesto de coste y tiempo

**En palabras sencillas.** Cada análisis consume tiempo y dinero (uso de modelos y de datos). Un tope evita que un fallo o un bucle gaste de más.

**Valor de partida.** Un tope por encargo y otro por día, fijados cuando conozcamos el coste real en la Fase 1. Mientras tanto: máximo 3 encargos de análisis profundo al día y corte automático si algo se repite sin avanzar.

| Límite | Mi cifra |
| --- | --- |
| Gasto máximo mensual en modelos y datos (euros) |  |
| Gasto máximo por análisis profundo (euros) |  |
| Tiempo máximo por análisis profundo (minutos) |  |

**Mi decisión.**

- [x] Acepto el valor de partida y fijo las cifras tras medir el coste real (7-11-2026)
- [ ] Ya sé mi tope (rellenado arriba)
- [ ] No lo sé aún

### P-08 · Cómo te avisa y cómo apruebas

**En palabras sencillas.** Las aprobaciones y los avisos importantes no pueden depender de un chat. Hace falta un canal propio (notificación al móvil o correo) y una segunda comprobación de que eres tú quien aprueba.

**Por qué importa.** Evita aprobar a ciegas desde un mensaje y que alguien suplante tu aprobación.

**Valor de partida.** Avisos urgentes por notificación al móvil y por correo, con acuse de recibo. Aprobaciones con segundo factor (por ejemplo, un código de una aplicación de autenticación) y confirmando el importe tecleándolo.

**Mi decisión.**

- [ ] Acepto el valor de partida
- [ ] Prefiero otro canal (cuál):
- [x] No lo sé aún (7-11-2026): se usa el valor de partida (móvil y correo con acuse, segundo factor), provisional

## Bloque 5 · Nombres y pendientes de Forex

### P-09 · Cómo llamar a los analistas por tipo de activo

**En palabras sencillas.** Cada tipo de activo tiene un código estable, por ejemplo `C-DIV` para divisas. Antes se usaban números (`C.1`, `C.2`…) y en los documentos de B Forex divisas aparece como `C.3`, mientras tú lo llamas `C.1`. Hay que elegir un solo nombre para hablar.

**Valor de partida.** Usar siempre los códigos (`C-DIV`, `C-RV`…) y dejar los números solo como equivalencia.

**Mi decisión.**

- [ ] Acepto el valor de partida (usar los códigos)
- [ ] Prefiero seguir con números (cuál es C.1, C.2…):
- [ ] No lo sé aún

### P-10 · Tres detalles pendientes del Bloque B Forex

**En palabras sencillas.** Al construir B Forex quedaron tres decisiones menores para ti. Ninguna bloquea el arranque.

| N.º | Qué es | Valor de partida |
| --- | --- | --- |
| 1 | **Nombre de un estado.** El sistema escribe `RECHAZADA` para una petición (femenino) y `RECHAZADO` para un resultado de un analista (masculino). Es una inconsistencia de forma | Unificar en una sola forma. Propongo `RECHAZADA` para peticiones y mantener `RECHAZADO` solo en los analistas, documentado como regla |
| 2 | **Dureza del objetivo de acierto.** El objetivo OBJ-FX-69 exige que los pronósticos superen a la referencia más simple (que el precio no cambie, o el tipo a plazo). Es difícil de lograr y de medir con pocos casos | Mantener el objetivo, pero tratarlo como meta a largo plazo, no como criterio de fallo al principio |
| 3 | **Definición de «pares principales» de ESMA.** Solo importa si habilitas los CFD, que ahora están excluidos. Hay que comprobar la normativa vigente | No hacer nada hasta que decidas habilitar los CFD |

**Mi decisión.**

- [ ] Acepto los tres valores de partida
- [ ] Quiero cambiar alguno (número y qué):
- [ ] No lo sé aún

## Hoja resumen

Copia esta tabla en un chat nuevo con tus respuestas. Escribe en la última columna A (acepto), C (cambio, con el valor) o N (no lo sé aún).

| ID | Pendiente | Prioridad | Mi decisión |
| --- | --- | --- | --- |
| P-16 | Por dónde empezar (divisas + cartera táctica) | Antes de Fase 1 |  |
| P-03 | Mandato de cada cartera | Antes de Fase 1 |  |
| P-05 | Intermediario y datos (ficha) | Antes de Fase 1 |  |
| P-11 | Límites en % del capital | Antes de Fase 1 |  |
| P-08 | Canal de avisos y segundo factor | Antes de Fase 1 |  |
| P-07 | Presupuesto de coste y tiempo | Antes de Fase 1 |  |
| P-01 | Riesgo por operación y operaciones al día | Antes de dinero real |  |
| P-12 | Autonomía total (L3) desactivada hasta Fase 5 | Antes de dinero real |  |
| P-13 | Tolerancias de conciliación | Antes de dinero real |  |
| P-02 | Condiciones para subir de nivel | Antes de dinero real |  |
| P-14 | Muestra mínima y duración de fases | Antes de dinero real |  |
| P-06 | Impuestos y asesor | Antes de dinero real |  |
| P-04 | Horizontes de cada cartera | Más adelante |  |
| P-15 | Clases de comparabilidad Q/S/K | Más adelante |  |
| P-09 | Nombres C-xxx frente a C.n | Más adelante |  |
| P-10 | Tres detalles de B Forex | Más adelante |  |

*Este cuestionario no es asesoramiento financiero, fiscal ni jurídico. Los valores de partida son prudentes, pero la decisión y la responsabilidad son tuyas.*
