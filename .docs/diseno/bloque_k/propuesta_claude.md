# Bloque K: datos en los que se pueda confiar (propuesta de diseño de Claude)

De: Claude, 11-11-2026. Estado: **PROPUESTA PARA DISCUTIR**. No hay nada que implementar: el operador está decidiendo la arquitectura de los bloques antes de construir (relevo de Astra, §0 bis). Copia en el repositorio del documento que el operador revisó con Claude.

## 1. Respuesta corta

K es la única fuente de datos del robot: recoge, ajusta, comprueba la calidad y sirve con un sello de qué se sabía y desde cuándo. Código determinista, sin IA, que falla cerrado (D-18). El marco común ya tiene sello de corte, calendario, reglas Q-01 a Q-15, procedencia y licencia, y consulta punto en el tiempo, con datos simulados. Se propone:

1. **Dos fechas por dato:** a qué fecha se refiere y cuándo se supo.
2. **Un catálogo de necesidades** por cartera y bloque, con fuente, frescura y licencia.
3. **Fuentes oficiales y gratuitas primero;** datos de pago solo si demuestran que compensan.
4. **Fallar cerrado sin paralizar lo esencial:** un dato dudoso detiene el análisis que lo usa; plan base, stops y F siguen con el intermediario.

## 2. Cómo los datos ganan o pierden rentabilidad por euro

| Error | Qué pasa | Qué cuesta |
| --- | --- | --- |
| Dato que entonces no se sabía | Fecha de referencia en lugar de publicación | Ventajas falsas en J, I y C |
| Dato revisado | El modelo se entrena con el dato final y en real recibe el primero | Funciona en el pasado y falla en el presente |
| Ajuste corporativo olvidado | Un desdoblamiento parece una caída del 50 % | Stops, alertas y señales falsas |
| Precio viejo o erróneo | Precio de ayer o con un cero de más | Órdenes y stops mal colocados |
| Divisa o unidad equivocada | Peniques leídos como libras | Tamaños cien veces mayores o menores |
| Solo supervivientes | Faltan los activos desaparecidos | Backtests inflados |
| Composición de fondos desconocida | No se sabe qué hay dentro | Concentración oculta |
| Datos caros | Suscripciones que no se pagan solas | Rentabilidad perdida |

## 3. Qué hay hoy y qué falta

Se conserva (V0.03 y siguientes): sello de fecha de corte inmutable; calendario; reglas Q-01 a Q-15 que marcan o bloquean, nunca estiman; procedencia y licencia, con licencias admitidas propuestas en D-29; consulta punto en el tiempo y barras válidas solo tras su cierre; advertencias al Orquestador y al operador.

Falta: datos reales (T-86; ficha de restricciones P-05 pendiente del intermediario); la fecha de conocimiento en todo el almacén, incluidas las revisiones macro; el catálogo de necesidades de los demás diseños (oscilación normal de H, volumen y horarios de G, composición de fondos de F, volatilidades y correlaciones de E, tasas base de C); segunda fuente para lo que no son precios, posiciones y saldos; una regla de degradación.

## 4. Catálogo de necesidades

| Datos | Quién | Frescura | Fuente candidata | Fase |
| --- | --- | --- | --- | --- |
| Tipos de cambio | C-DIV, D, E, H, I | Diaria | BCE; intermediario como segunda fuente | 1 |
| Índice de la sombra | I | Diaria | Valor liquidativo de un fondo indexado que lo replique | 1 |
| Inflación (IPCA) | I, D, planificador | Mensual | Eurostat | 1 |
| Tipos de interés y curvas | C, vigía, E | Diaria | BCE | 1 |
| Calendario de eventos | Todos | Diaria | Bancos centrales y oficinas de estadística | 1 |
| Macro con revisiones | Estratega macro, vigía, C | Por publicación | Oficiales; algunos indicadores conocidos son de pago | 1 y 2 |
| Posicionamiento | A, C, Estratega macro | Semanal o trimestral | CFTC, SEC, CNMV | 1 y 2 |
| Volatilidades y correlaciones (también en crisis) | E, F, H | Diaria | Las calcula el Motor sobre K | 1 |
| Episodios de estrés | E, Motor, J | Estática | Catálogo propio | 1 |
| Datos de fondos (valor liquidativo, comisiones, composición, diferencia con el índice, domicilio, traspasable) | C-FON, C-IDX, E, F, G | Diaria y mensual | Gestoras, CNMV | 2, o 1 con E4-18 |
| Volumen medio, horarios, operaciones corporativas | G, F, ajustes de K | Diaria | Intermediario y bolsas | 1 y 2 |
| Intradía y diferenciales | Trading, G | Minutos | Intermediario | 4 |
| Fundamentales con fecha de publicación | C-RV | Trimestral | Normalmente de pago | 2 o más tarde |
| Datos del propio robot | I, J | Continua | SC-4, SC-5, libro de G | 1 |

El intermediario es también fuente de datos: elegirlo bien condiciona a K.

## 5. Recorrido de un dato

Fuente por su adaptador (SC-10, licencia admitida, probada contra el simulador) → (1) ingesta con procedencia (fuente, hora, licencia, huella; el original no se sobrescribe) → (2) ajustes (corporativos, divisa, unidades, calendario) → (3) calidad (marca o bloquea; nunca estima) → (4) contraste con segunda fuente y su tolerancia → (5) almacén con dos fechas (corrección = registro nuevo) → (6) sello y consulta punto en el tiempo → bloques y Motor; avisos de calidad al canal de avisos y al operador. Un dato dudoso detiene el análisis que lo usa; plan base, stops y F siguen con el intermediario.

## 6. Calidad

| Comprobación | Qué detecta | Qué hace |
| --- | --- | --- |
| Salto frente a lo normal | Movimiento muy por encima de la oscilación habitual | Marca, salvo que lo explique una operación corporativa o un evento |
| Coherencia con operaciones corporativas | Hueco que coincide con un desdoblamiento o dividendo | Ajusta sin alarma |
| Unidades y divisa | Peniques como libras, cotizaciones por cien | Bloquea si no cuadra con la ficha |
| Frescura según calendario | Precio sin actualizar en día abierto | Marca como viejo; distingue festivos |
| Días que faltan | Huecos frente al calendario | Marca; no rellena |
| Acuerdo entre fuentes | Diferencia por encima de la tolerancia | Bloquea para F y G; avisa |
| Revisiones grandes | Dato macro muy corregido | Guarda las dos versiones y avisa |
| Supervivientes | Universo histórico sin desaparecidos | Bloquea su uso en J e I |

Algunas pueden estar ya cubiertas en parte por Q-01 a Q-15. K no arregla datos; K mide a sus fuentes (marcas, bloqueos, retraso) para que I proponga cambiar una que falla.

## 7. Fuentes, coste y licencias

Oficiales y gratuitas primero, con licencia admitida (D-29) y sin saltarse condiciones de ninguna web. Pago solo con prueba de que compensa (300 €/año sobre 20.000 € exigen un 1,5 % más), por la ruta única y dentro del tope anual (E4-17). Ningún bloque conoce al proveedor (D-08). Almacén exportable en formatos abiertos (D-40). Descargas incrementales, caché y respeto a los límites de cada fuente.

## 8. Fronteras, precisión y consumo

| Quién | Relación con K |
| --- | --- |
| Motor | K da datos; el Motor calcula lo derivado y cita el sello |
| SC-11 | K no lee noticias |
| Lectores de evidencia | Lo extraído entra en K con fuente, fecha y etiqueta |
| Biblioteca (E4-05) | K guarda datos; la biblioteca, conocimiento |
| G e intermediario | Segunda fuente de precios |
| J e I | Bases para aprender por fecha de conocimiento (D-38) |
| Todos | Nadie guarda su copia de datos de mercado |

Consumo: cero tokens; su coste son datos y almacenamiento. Precisión: reconstrucción exacta de análisis antiguos con su sello; batería de datos malos reales; autopsias con causa «dato» cada vez menos frecuentes.

Orden: Fase 1 (T-86) divisas, tipos, calendario, índice de la sombra, inflación, segunda fecha, contraste con el intermediario, catálogo; Fase 2 (o antes con E4-18) fondos, operaciones corporativas, macro con revisiones; después, fundamentales e intradía.

## 9. Preguntas para el operador

1. Ratificar las licencias admitidas de D-29.
2. Ningún dato de pago sin prueba de que compensa y dentro del tope.
3. Tolerancia del contraste de tipos de cambio: 0,5 % en divisas principales y 3 % en el resto.
4. Regla de degradación.
5. Cada Documento 0 declara qué datos de K usa y con qué frescura.
