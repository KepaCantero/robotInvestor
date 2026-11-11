# Fiscalidad (SC-9): ganar después de impuestos (propuesta de diseño de Claude)

De: Claude, 11-11-2026. Estado: **PROPUESTA PARA DISCUTIR**. No hay nada que implementar: el operador está decidiendo la arquitectura de los bloques antes de construir (relevo de Astra, §0 bis). Copia en el repositorio del documento que el operador revisó con Claude. **Nada de esto es asesoramiento fiscal:** cada regla la valida un asesor antes de codificarse (P-06).

## 1. Respuesta corta

SC-9 calcula cuánto impuesto genera cada decisión y cuánto queda después. Lo usan D, E, el planificador e I. La Constitución exige que sus reglas sean **código validado por un asesor, nunca texto de un modelo de IA** (§3), y que todo se mida después de impuestos (P17, D-25, D-31). Hoy no existe: solo está el diseño del libro fiscal por persona en G.

Idea central: **el impuesto que no se paga hoy sigue trabajando.** Para un particular español, la mayor ventaja fiscal no es un truco sino un orden. Se propone:

1. **Reglas como datos versionados por ejercicio,** cada versión firmada por el asesor fiscal y con sus casos de prueba. Sin firma, la cifra sale como provisional.
2. **Un único cálculo para todos:** coste fiscal inmediato, impuesto latente, pérdidas compensables y bloqueos de recompra, por persona y no por cartera.
3. **Seis palancas en orden:**
    1. aportar en vez de vender para reequilibrar;
    2. fondos traspasables a largo plazo;
    3. compensar pérdidas;
    4. repartir ganancias entre años para quedarse en el tramo bajo;
    5. comparar planes de pensiones con su coste al rescatarlos;
    6. valorar la nueva cuenta Financia Europa cuando sea contratable.
4. **El impuesto no manda:** un ahorro fiscal nunca justifica una inversión peor ni salirse del mandato.
5. **Cero tokens.**

## 2. Dónde se gana o pierde rentabilidad por impuestos

**Ejemplo de diferir el impuesto** (cálculo ilustrativo, sin costes): 10.000 € al 6 % anual durante 20 años, con un 21 % de impuesto sobre las ganancias.

- **Pagando al final:** quedan **27.436 €**.
- **Pagando cada año,** por vender para reequilibrar: quedan **25.249 €**.
- **Diferencia:** 2.187 €, un 8,7 % más solo por el orden.

| Palanca | Ejemplo | Qué se gana |
| --- | --- | --- |
| Diferir | Reequilibrar con aportaciones o traspasos entre fondos en vez de vender | El ejemplo de arriba: un 8,7 % en 20 años |
| Compensar pérdidas | Una pérdida de 3.000 € anula una ganancia de 3.000 € | Entre 570 y 630 € de impuesto |
| Repartir entre años | 12.000 € de ganancia en dos años en lugar de en uno, para usar dos veces el tramo del 19 % | 120 € |
| Regla de recompra | Recomprar lo mismo antes de dos meses hace que la pérdida no cuente todavía | Evita perder una compensación con la que se contaba |
| Plan de pensiones | Deducir la aportación hoy al tipo marginal y tributar al rescatar | Depende del tipo hoy frente al tipo al rescatar |
| Dividendos extranjeros | Recuperar en origen lo retenido de más | Pequeño, pero cada año |
| Errores | Un tipo de cambio mal aplicado o una venta asignada al lote equivocado | Una declaración mal hecha y una posible sanción |

En España, mantener más tiempo no reduce el tipo, a diferencia de otros países. El coste de rotar es perder el diferimiento, no pagar un tipo más alto.

## 3. Qué hay hoy y qué falta

**Decidido en la Constitución:**

- SC-9 con reglas codificadas y validadas por un asesor (§3) y jurisdicción española por defecto (P-06).
- Fiscalidad en la decisión y freno a la rotación con impuestos (D-25).
- Vehículo fiscal en la decisión (D-31) y vehículos admitidos pendientes (P-28).
- Rentabilidad mínima después de costes e impuestos (§7).
- Cartera sombra comparada después de impuestos (P17).
- Reglas que nombra la Constitución: recompra en dos meses, criptoactivos, ganancias en divisas y bienes en el extranjero (§10).
- Peso fiscal bajo en trading, medio en táctica y alto en largo plazo (§7).
- Reclasificar una posición de cartera exige aprobación por su impacto fiscal.
- SC-9 llega en la Fase 2.

**En los diseños:**

- G propone un libro fiscal por persona con cola de lotes única.
- E y D cuentan con las reglas de SC-9.
- La enmienda 4 propone un módulo del Motor de optimización fiscal a varios años (E4-08) y el informe fiscal anual (E4-16).

**En código:** nada de SC-9.

**Falta:**

- Las reglas.
- Quién las valida y cada cuánto.
- Cómo se enteran D y E del coste fiscal.
- Qué se optimiza y con qué límites.
- Cómo se detecta un cambio legal.

## 4. Las reglas que hay que codificar

Territorio común, ejercicio 2026. Fuentes consultadas el 11-11-2026, en su mayoría divulgativas. **Ninguna se codifica sin la firma del asesor.**

| Regla | Qué dice | Fuente |
| --- | --- | --- |
| Escala del ahorro | 19 % hasta 6.000 €; 21 % hasta 50.000 €; 23 % hasta 200.000 €; 27 % hasta 300.000 €; 30 % por encima (último tramo desde 2025, Ley 7/2024). Igual en todo el territorio común; Navarra y el País Vasco tienen la suya | [Guía fiscal](https://guiafiscal.es/irpf/tramos-irpf-2026/) |
| Lotes | Al vender parte de valores homogéneos, se venden primero los más antiguos (FIFO), por persona | [CNMV](https://internet.cnmv.es/DocPortal/Publicaciones/Guias/GuiaFiscalidadAcciones2026.pdf) |
| Recompra | Una pérdida no se puede compensar si se compraron valores homogéneos en los dos meses anteriores o posteriores (un año si no cotizan); cuenta cuando se venden esos valores | [CNMV](https://internet.cnmv.es/DocPortal/Publicaciones/Guias/GuiaFiscalidadAcciones2026.pdf) |
| Compensar pérdidas | Ganancias y pérdidas se compensan entre sí; con los rendimientos del capital, hasta el 25 %; lo que sobra, durante cuatro años | [Agencia Tributaria](https://sede.agenciatributaria.gob.es/Sede/ayuda/manuales-videos-folletos/manuales-ayuda-presentacion/irpf-2025/8-cumplimentacion-irpf/8_1-base-imponible-general-base-ahorro/8_1_4-compensaciones-partidas-negativas-base-ahorro.html) |
| Traspasos entre fondos | Sin tributar entre fondos de inversión. Excluidos los ETF españoles y, desde 2022, los extranjeros (Ley 11/2021), salvo participaciones extranjeras compradas antes de 2022 | [Guía fiscal](https://guiafiscal.es/inversiones/etf-fiscalidad-2026-guia/) |
| Dividendos | Retención del 19 %; los fondos de acumulación difieren la ganancia hasta la venta | [CNMV](https://internet.cnmv.es/DocPortal/Publicaciones/Guias/GuiaFiscalidadAcciones2026.pdf), [Guía fiscal](https://guiafiscal.es/inversiones/etf-fiscalidad-2026-guia/) |
| Divisas | Los resultados de contratos de divisas son ganancias o pérdidas patrimoniales, imputadas al liquidarse (consulta de la DGT de 2014) | [Fiscal Impuestos](https://www.fiscal-impuestos.com/diferencias-divisas-contrato-forex-ganancias-irpf-imputacion-margen.html) |
| Cuenta Financia Europa | Hasta 150.000 € aportados; sin impuesto por operar dentro; con más de cinco años, los primeros 10.000 € de ganancia exentos y un 20 % excluido del resto; solo activos europeos; solo efectivo, sin traspasar lo que ya se tiene. En vigor desde el 8-10-2026 (Real Decreto-ley 29/2026), **pendiente de convalidación** y aún no contratable | [BOE](https://www.boe.es/buscar/act.php?id=BOE-A-2026-20823), [Rankia](https://www.rankia.com/blog/mejores-brokers/7490904-cuenta-financia-europa-que-requisitos-fiscalidad), [Filtrent](https://filtrent.com/blog/decretos-de-vivienda-diputacion-permanente/) |

**A validar especialmente:**

- Si cada conversión de una cuenta en divisa genera ganancia o pérdida.
- Si la regla de recompra se aplica a pares de divisas y contratos por diferencias.
- El límite vigente de aportación a planes de pensiones (1.500 € al año en planes individuales, de memoria) y su rescate como rendimiento del trabajo.
- La deducción por doble imposición internacional.
- La obligación de informar de bienes en el extranjero (modelos 720 y 721).

## 5. Cómo entra el coste fiscal en cada decisión

Diagrama del documento («El impuesto entra en la decisión antes de la orden»):

- **Entradas:** SC-11 vigila el BOE y avisa de cambios al asesor → reglas firmadas, una versión por ejercicio; K da los tipos de cambio oficiales con su fecha; G lleva el libro fiscal con los lotes por persona.
- **SC-9** (código, cero tokens) calcula cuatro cifras: impuesto inmediato, impuesto latente, pérdidas compensables y bloqueo de recompra.
- **Salidas:** D y E (comparan y dimensionan), planificador (vehículo y retirada), N (impuesto en cada aprobación) e I (robot y sombra, netos).
- **Bucle:** G ejecuta tras D, E, F y la aprobación, y cada ejecución actualiza el libro fiscal.

## 6. Qué hace SC-9 en cada decisión

SC-9 calcula y señala; no propone operaciones. Las propuestas siguen siendo de E y de los gestores del Broker, y pasan por F como todas.

| Momento | Qué calcula SC-9 | Qué se hace con ello |
| --- | --- | --- |
| Venta o cierre | Impuesto inmediato con los lotes de la persona, tramo en que cae y pérdidas disponibles | Se muestra en N junto a la orden. Nunca frena una reducción de riesgo |
| Cambiar una posición por otra | Impuesto que se adelanta al vender | Entra en el coste de salir del freno a la rotación (D-25) |
| Reequilibrio | Coste de cada forma de hacerlo | Primero con la aportación, después con traspasos entre fondos y solo al final vendiendo |
| Aportación | Valor de cada vehículo para esa persona | El planificador elige entre fondo traspasable, plan de pensiones hasta su límite o cuenta Financia Europa |
| Recompra | Si una compra bloquearía una pérdida reciente | Aviso antes de aprobar; el operador decide |
| Fin de año (de noviembre a diciembre) | Pérdidas latentes, ganancias del año, hueco que queda en el tramo del 19 % y pérdidas que caducan | Lista para el gestor: vender con pérdida y pasar a un activo parecido pero no homogéneo, o adelantar ganancias si hay pérdidas a punto de caducar. Siempre propuesta al operador |
| Dividendos | Retención en origen recuperable y acumulación frente a reparto | Preferir acumulación en el largo plazo y avisar de lo recuperable |
| Retirada del dinero | Qué vender primero y en cuántos años | Plan de retirada del planificador |
| Declaración | Ganancias por lote, dividendos, retenciones, pérdidas pendientes y bienes en el extranjero | Informe anual en N para el operador y su asesor |

**El impuesto no manda.** Un ahorro fiscal solo cuenta si la inversión sigue siendo igual de buena dentro del mandato. La cosecha de pérdidas no puede cambiar el riesgo ni dejar la cartera fuera de mercado más tiempo del fijado. Si una venta reduce riesgo, el impuesto se muestra pero no la frena.

## 7. SC-9 en las tres carteras

El impuesto es de la persona, no de la cartera: las tres comparten tramos, pérdidas compensables y cola de lotes. Por eso SC-9 calcula siempre sobre la persona y luego atribuye a cada cartera su parte.

| Cartera | Peso fiscal (§7) | Qué importa | Qué hace SC-9 |
| --- | --- | --- | --- |
| Trading | Bajo | Cada cierre tributa; las pérdidas del año compensan las ganancias; recomprar el mismo valor puede aplazar pérdidas | Resultado fiscal acumulado del año; aviso si la regla de recompra está aplazando pérdidas; la ventaja de cada estrategia se mide después de impuestos |
| Táctica | Medio | Rotar adelanta impuestos; mantener más tiempo no baja el tipo | Coste fiscal de cada cambio dentro del freno a la rotación |
| Largo plazo | Alto | Diferir durante décadas | Fondos traspasables por defecto, reequilibrio con aportaciones, planes de pensiones, cuenta Financia Europa si llega y plan de retirada |

**El mismo valor en dos carteras.** Como los lotes son de la persona, vender en una cartera puede consumir lotes que la otra consideraba suyos. Se sigue la propuesta de G: evitarlo por defecto o, si se permite, una cola fiscal única y un reparto explícito entre carteras.

**La sombra también paga impuestos.** Para que la comparación de I sea justa, la cartera sombra tributa con las mismas reglas. Un índice comprado y mantenido casi no paga hasta el final, y esa es parte de la ventaja que el robot tiene que superar.

## 8. SC-9 frente a los demás

| Quién | Relación con SC-9 |
| --- | --- |
| G | Lleva el libro fiscal por persona (lotes, ventas, dividendos, retenciones, traspasos); SC-9 lo lee y no guarda copia |
| K | Tipos de cambio oficiales para pasar a euros cada operación en divisa, con su fecha |
| D | Compara después de impuestos, con el vehículo incluido |
| E | Dimensiona y reequilibra con el coste fiscal; el freno a la rotación lo incluye |
| F | No usa SC-9 para vetar: un impuesto nunca bloquea reducir riesgo |
| Motor (SC-3) | Módulo de optimización fiscal a varios años (E4-08): qué vender, cuándo y por qué vehículo. Usa las reglas de SC-9; no tiene las suyas |
| Planificador del Broker | Vehículos, planes de pensiones, cuenta Financia Europa y plan de retirada |
| Conversacional del Broker | Explica las cifras; nunca interpreta la ley ni inventa una regla |
| I | Mide el robot y la sombra después de impuestos, y lo que aportó cada palanca fiscal |
| N | Muestra el impuesto en cada pantalla de aprobación y el informe anual |
| SC-11 | Vigila el BOE y avisa de cambios en las normas que usa SC-9; no escribe reglas |
| Asesor fiscal | Firma cada versión de las reglas y sus casos de prueba (P-06) |

## 9. Precisión, validación, consumo y orden

**Reglas como datos, no como código suelto.** Cada regla es una ficha con:

- el ejercicio y las fechas en que está vigente;
- su fuente legal;
- sus casos de prueba;
- la firma del asesor.

Un cambio legal no se parchea: se abre una versión nueva. Para las operaciones antiguas se sigue aplicando la versión de su fecha.

**Validación.**

| Comprobación | Cuándo | Objetivo |
| --- | --- | --- |
| Casos de prueba del asesor | En cada versión | Todos aciertan; si uno falla, la versión no entra |
| Contraste con los datos fiscales de la Agencia Tributaria y el informe del intermediario | Cada año, antes de declarar | Sin diferencias sin explicar |
| Ganancia calculada frente a la del intermediario, operación a operación | Cada mes | Diferencias por debajo de un céntimo, salvo redondeos explicados |
| Aviso de SC-11 por un cambio en el BOE | Cuando ocurra | Versión nueva firmada antes de la siguiente decisión que dependa de esa regla |

**Si falta la firma.** Las cifras salen marcadas como provisionales en D, E y N. Las optimizaciones que dependen de esa regla (cosecha de pérdidas, elegir vehículo) no se proponen. Reducir riesgo nunca se frena.

**Consumo:** cero tokens. Todo es cálculo; el Broker solo lo explica.

**Orden:**

- **Fase 1, divisas en simulación:** ganancia en euros de cada cierre con el tipo de cambio de K, resultado fiscal acumulado del año y la sombra después de impuestos. Con reglas provisionales.
- **Fase 2 (la que fija la Constitución):**
    - reglas firmadas por el asesor;
    - libro fiscal completo con lotes y regla de recompra;
    - compensación de pérdidas;
    - fondos traspasables y reequilibrio con aportaciones;
    - planes de pensiones;
    - informe anual;
    - el módulo de optimización del Motor.
- **Fase 3, con dinero real:** contraste con la Agencia Tributaria y el intermediario, dividendos extranjeros y bienes en el extranjero.
- **Cuenta Financia Europa:** solo cuando se convalide y se pueda contratar.

## 10. Preguntas para el operador

Todas son [PROPUESTO]; ninguna se decide sin el operador.

1. **Jurisdicción (P-06):** territorio común; Navarra y el País Vasco, solo si hace falta y con su asesor.
2. **Asesor fiscal:** quién firma las reglas, una vez al año y ante cada cambio legal.
3. **Vehículos (P-28):** fondos traspasables por defecto en el largo plazo; ETF solo si no hay un fondo equivalente o si su menor coste compensa no poder traspasarlo.
4. **Cosecha de pérdidas de fin de año:** siempre como propuesta al operador, nunca automática.
5. **Cuenta Financia Europa:** que el planificador la compare cuando se convalide y se pueda contratar.
6. **El mismo valor en dos carteras:** evitarlo por defecto (como en G).
7. **Planes de pensiones:** compararlos con el tipo marginal de hoy frente al esperado al rescatar, sin recomendarlos por defecto.
