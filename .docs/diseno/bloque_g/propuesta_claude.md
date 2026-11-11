# Bloque G: que cada orden salga como se decidió (propuesta de diseño de Claude)

De: Claude, 11-11-2026. Estado: **PROPUESTA PARA DISCUTIR**. No hay nada que implementar: el operador está decidiendo la arquitectura de los bloques antes de construir (relevo de Astra, §0 bis). Copia en el repositorio del documento que el operador revisó con Claude. Va con las de D, E y F (`.docs/diseno/`).

## 1. Respuesta corta

G es el único canal por el que el robot toca el dinero: envía las órdenes aprobadas, protege cada posición con su stop, lleva el libro y concilia con el intermediario. No interpreta tesis ni decide nada: **su trabajo es que cada orden salga como se decidió, al menor coste posible, y que nunca haya una posición sin proteger o desconocida.**

El G del marco común es de las piezas más maduras y se conserva. Se proponen cuatro cambios:

1. **Ejecutar barato, no solo ejecutar bien:** tipo de orden, hora, escalonado y divisa según la cartera y el instrumento. En trading, el coste de ejecución se repite cientos de veces y puede comerse la ventaja entera.
2. **Medir cada ejecución:** precio de decisión frente al obtenido, para que I calibre el modelo de costes que usan D, E y F, que hoy es una suposición.
3. **Saber operar fondos:** suscripciones y reembolsos al valor liquidativo, días de liquidación y traspasos entre fondos, que en España no tributan.
4. **Un libro completo:** aumentar posiciones, efectivo, dividendos y operaciones corporativas, con un libro fiscal por persona además del operativo por cartera.

## 2. Cómo la ejecución gana o pierde rentabilidad por euro

| Fuga | Qué es | Dónde pesa más |
| --- | --- | --- |
| **Diferencial** | Diferencia entre precio de compra y de venta | Trading e instrumentos poco líquidos |
| **Deslizamiento** | El precio se mueve entre la decisión y la ejecución, o la orden lo mueve | Trading y órdenes grandes |
| **Comisiones** | Intermediario, mercado y, en fondos, gestora | Todas; en largo plazo, cada año |
| **Cambio de divisa** | Lo que cobra el intermediario por convertir | Activos fuera de la zona euro |
| **Errores** | Duplicados, lado equivocado, posiciones sin stop | Raros, pero enormes |

Ejemplo de escala: una estrategia de trading con 200 operaciones de ida y vuelta al año y un coste de un 0,10 % por operación pierde unos 20 puntos al año del capital que mueve; una que ganaba un 15 % en el backtest pierde dinero en real. De ahí que G tenga que **ejecutar con criterio de coste** y **medir lo que cuesta de verdad**: es el único que ve las ejecuciones reales.

## 3. Qué hay hoy y qué le falta

Se conserva (Documentos 0 V0.08, V0.15, V0.18, V0.20 y V0.21; código en `sistema_global/marco_comun_c/validador/ejecucion_g.py` y `sistema_global/marco_comun_c/validador/manual_g.py`):
- código determinista con simulador de fallos;
- cada orden anotada en el Orquestador antes de enviarse, con identificador idempotente;
- orden de entrada viva durante la ventana y stop por lo ejecutado;
- ante la duda, nada se da por abierto (G-03, G-08);
- reducción parcial con stop redimensionado y órdenes de solo reducción;
- operaciones manuales declaradas (CT-G-14) y conciliación con diferencias explicadas;
- foto de la cartera para E y F tomada del intermediario y valorada en euros.

Le falta, por orden de importancia para la rentabilidad:
1. **No mide la calidad de la ejecución.**
2. **Un solo tipo de ejecución:** límite y stop, sin escalonar, sin elegir hora y sin OCO.
3. **No sabe operar fondos.**
4. **Libro incompleto:** una posición por instrumento, sin aumentar, sin efectivo, dividendos ni operaciones corporativas (T-31).
5. **Intermediario simulado** sin disparo de stops (T-14), actores sin autenticar (T-01), L0 sin impedir órdenes reales (T-30). Obligatorio antes del dinero real.

## 4. Una sola lógica para las tres carteras

|  | Trading | Táctica | Largo plazo |
| --- | --- | --- | --- |
| **Tipo de orden** | Límite con validez corta; stop nativo; OCO si el intermediario la tiene | Límite viva durante la ventana (ya existe); stop nativo | Límite cerca del precio medio en bolsa; suscripción, reembolso o traspaso en fondos |
| **Lo que más cuesta** | Diferencial y deslizamiento repetidos | Entrar o salir en un hueco | Cambio de divisa, comisiones de fondos, vender en vez de traspasar |
| **Cuándo ejecutar** | Horas de más liquidez del instrumento | Dentro de la ventana, evitando apertura y cierre si el diferencial es ancho | Sin prisa; un fondo cotizado de acciones de EE. UU. en bolsa europea suele tener diferenciales más estrechos con Nueva York abierta |
| **Órdenes grandes** | Raras | Escalonadas si superan lo que el mercado absorbe | Escalonadas en varios días; aportaciones agrupadas |
| **Protección** | Stop nativo siempre | Stop nativo siempre | Sin stop: diversificación y plan |
| **Conciliación** | Varias veces al día | Diaria | Diaria y tras cada liquidación |

- **No convertir divisas sin necesidad:** con saldos multidivisa, lo vendido en dólares se queda en dólares para la siguiente compra en dólares.
- **El traspaso antes que la venta** entre fondos, cuando se pueda (reglas en SC-9, validadas por un asesor, P-06).

La seguridad no cambia en ninguna cartera: anotar antes de enviar, identificadores idempotentes, ninguna posición sin proteger o desconocida.

## 5. El ciclo de vida de una orden

Entrada: acción aprobada por F, con su tipo, cantidad, cartera y precio de decisión.

1. **Preparar la ejecución** (nuevo): tipo de orden, hora, tramos y divisa según la cartera y el instrumento.
2. **Anotar antes de enviar:** el Orquestador la conoce antes que el intermediario.
3. **Enviar y seguir:** viva, parcial, ejecutada, vencida o rechazada; en fondos, pendiente de liquidar.
4. **Proteger lo ejecutado:** stop nativo por la cantidad real, de solo reducción (no aplica a fondos).
5. **Conciliar:** posiciones, stops, efectivo, dividendos y liquidaciones, con tolerancias.
6. **Medir la ejecución** (nuevo): precio de decisión frente al obtenido y coste total.

Si algo falla o no cuadra en los pasos 3 a 5, nada se da por abierto, se cierra lo desprotegido y se avisa (G-03, G-08). Salidas: el libro conciliado, del que parten E y F, y el coste real medido, con el que I corrige los costes de D, E y F.

## 6. El libro y la conciliación

| Libro | Qué registra | Para qué |
| --- | --- | --- |
| **Operativo, por cartera** | Posiciones, stops, órdenes pendientes, efectivo por divisa, dinero en tránsito | La foto de E y F; lo que vigila H |
| **Fiscal, por persona** | Cada compra con fecha y precio, ventas, dividendos, retenciones, traspasos | Lo que necesita SC-9 |

En España, al vender parte de unos valores iguales se considera vendido lo primero que se compró, y eso se aplica a la persona, no a cada cartera: si dos carteras tienen el mismo fondo cotizado, una venta en una puede tributar como si vendiera lo más antiguo de la otra. **A confirmar por el asesor (P-06).** El diseño debe preverlo: o se evita el mismo instrumento en dos carteras, o el libro fiscal usa una sola cola por persona.

La conciliación compara posiciones y stops (ya existe), efectivo (T-31) y operaciones corporativas (que K anuncia y G aplica antes de conciliar). Diferencia explicada dentro de tolerancia: no dispara nada; sin explicar: discrepancia, aviso y la cartera a L1 (§8). G nunca corrige el libro por su cuenta.

## 7. G frente a F, H, K, I, el intermediario y el operador

| Quién | Qué hace | Relación con G |
| --- | --- | --- |
| **F** | Aprueba, reduce o veta | G solo envía lo aprobado; F se repite con el precio real. G le da la segunda fuente |
| **H** | Vigila posiciones y salidas | Revisa órdenes vivas y pide reducir o cerrar; G ejecuta y no cierra nada por juicio propio |
| **K** | Datos, calendario, operaciones corporativas | Volumen medio, horarios, cambios de identificador; contrasta los tipos de cambio de G |
| **I** | Evaluación y atribución | Recibe el coste real de cada ejecución |
| **Intermediario** | Custodia, mercado, órdenes nativas | Los stops viven en él (§8); única fuente de verdad de lo que se tiene |
| **Operador** | En L1 ejecuta a mano | Declara con CT-G-14 |

**G decide cómo ejecutar, no cuánto ni si conviene esperar a un precio mejor.** Partir una orden o esperar a la apertura de Nueva York, dentro de la ventana que aprobó F, es de G; retrasar una compra porque «el precio va a bajar» sería una opinión de mercado, y G no tiene opiniones.

## 8. Precisión y consumo

**Consumo: cero.** Plano de control, sin LLM (§3).

**G se mide con tres números:** coste de ejecución por cartera e instrumento frente al modelo de costes; fiabilidad (posiciones sin stop y duplicados: cero; estados inciertos y su tiempo de resolución); conciliación (discrepancias sin explicar y tiempo hasta cerrarlas).

**Antes del dinero real:** simulador con disparo de stops, huecos, liquidaciones y operaciones corporativas; paper trading contra el intermediario elegido; dinero real en pequeño por la escalera de verificación (§7). Obligatorios: T-14, T-01, T-30 y T-31.

## 9. Preguntas para el operador

Ninguna hay que contestarla ahora; cada una lleva un valor por defecto [PROPUESTO], en simulado.

1. **El intermediario.** Criterios propuestos: stops nativos y OCO, cuentas multidivisa, acceso por programa, fondos con traspasos, comisiones. Si ninguno cubre bolsa y fondos, ¿dos intermediarios o uno con menos posibilidades?
2. **El mismo instrumento en dos carteras:** evitarlo por defecto, o permitirlo con una cola fiscal única.
3. **Varias posiciones por instrumento:** permitir aumentar, no dos posiciones independientes.
4. **Órdenes grandes:** G las escalona por su cuenta dentro de la ventana de F.
5. **Saldos en divisas** para no convertir dos veces, si el intermediario lo permite.
6. **Subcuentas por cartera**, si el intermediario lo permite.
