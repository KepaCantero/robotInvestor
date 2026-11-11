# Pasada de coherencia: la arquitectura completa (propuesta de Claude)

De: Claude, 11-11-2026. Estado: **PROPUESTA PARA DISCUTIR**. No hay nada que implementar: el operador está decidiendo la arquitectura de los bloques antes de construir (relevo de Astra, §0 bis). Copia en el repositorio del documento que el operador revisó con Claude.

## 1. Respuesta corta

Se revisaron juntas las veinte propuestas de diseño del 11-11-2026 contra la Constitución V0.6:

- los bloques A a N, sin L (D-18);
- el Broker Personal;
- SC-3, SC-7, SC-9 y SC-10;
- la entrada del patrimonio;
- la enmienda 4.

Se comparó lo que cada una dice entregar con lo que las demás esperan recibir, sus fases y sus 110 preguntas al operador.

**La arquitectura encaja.** Todas siguen la misma pauta: el código dirige, pocos papeles de IA, el control fuera de la IA, todo medido frente a la cartera sombra y por euro. No hay bloques que se contradigan en lo esencial. Se encontraron:

- **12 incoherencias o huecos pequeños,** cada uno con su arreglo propuesto (§3). Los más importantes son quién reparte el capital entre carteras, quién es dueño de los episodios de estrés y qué queda de SC-8.
- **Una decisión que mueve las fases:** adelantar el largo plazo (E4-18) arrastra a SC-9, al planificador, a los perfiles de fondos de C y a los datos de fondos de K, y puede chocar con el tope de ocho bloques activos (§5).
- **Dieciséis contratos nuevos o que cambian** (§6).
- **Un aviso legal** si el robot se ofrece a otras personas (§7).
- **110 preguntas que se quedan en unas 100** al fusionar las repetidas, ordenadas por lo que bloquean (§8).

## 2. El mapa completo

Diagrama del documento («Del operador al intermediario, siempre por código»):

- **Arriba:** el operador decide en N, que ve y aprueba; el Broker Personal habla, planifica, orquesta y hace los encargos; I es el juez frente a la sombra.
- **Qué estudiar y qué elegir:** A busca → B acota → C analiza → D compara, junto con lo que J prueba.
- **Cuánto y con qué control (código):** M (riesgo) → E (tamaño) → F (control) → G (órdenes) ↔ H (vigilar).
- **Servicios comunes, que usan todos:** K (datos), SC-3 (Motor), SC-9 (fiscalidad), SC-10 (adaptadores), SC-1 (perfil), SC-4, SC-5 y SC-6 (registros), SC-7 (seguridad) y SC-11 (noticias).
- **Abajo:** los intermediarios, por SC-10, con la custodia, los stops nativos y la verdad de lo que se tiene. Solo G llega a ellos.

## 3. Incoherencias y huecos, con su arreglo

| # | Hallazgo | Dónde | Arreglo propuesto |
| --- | --- | --- | --- |
| 1 | Tres propuestas reparten el capital entre carteras: D «informa», E «propone» y el planificador «fija el plan» | D §9.2, E §7, Broker §4 | El planificador lo fija en la revisión anual con la vista global de E; E solo propone fuera de ella si una cartera se queda sin margen; D solo informa |
| 2 | Dueño del conjunto estándar de episodios de estrés: K lo guarda, el Motor lo calcula, D y M lo usan | K §4, SC-3 §4, M §4 | K guarda las fechas de los episodios; el Motor calcula; D es propietario funcional hasta la Fase 3 y M después |
| 3 | SC-8 se solapa: su calendario ya pasó a K, los datos macro están en el catálogo de K y la interpretación es del Estratega macro (E4-11) | Constitución §3, K §4 | SC-8 queda solo como el vigía de régimen (código); los datos van en K y la lectura, en el Estratega macro |
| 4 | E dice que K «sirve» volatilidades y correlaciones; K y el Motor dicen que las calcula el Motor sobre datos de K | E §8, K §4 | Las calcula el Motor (familias 2 y 3); se corrige la redacción de E |
| 5 | F necesita costes y volumen por instrumento, pero no debe depender del Motor | F §8, SC-3 §4 | F usa su propia versión simple con datos de K; el modelo de costes del Motor (de G) es para D y E |
| 6 | La fracción de Kelly se pregunta dos veces | D §9.3, E §9.1 | Un solo parámetro por cartera en SC-1, usado por D y E |
| 7 | El mismo valor en dos carteras se pregunta dos veces | G §9.2, SC-9 §10.6 | Una sola decisión, con la cola fiscal por persona |
| 8 | El segundo proveedor de IA aparece en A, B, C y la enmienda 4, y SC-7 y SC-10 solo lo cubren de forma genérica | A, B, C, E4-13 | Una decisión; su clave en SC-7 y su puerto en SC-10 |
| 9 | La sombra debería usar el mismo tipo de vehículo que el largo plazo (un fondo indexado traspasable), si no, compara peras con manzanas en impuestos | I, SC-9 §7 | La sombra del largo plazo, en fondo indexado mundial con las reglas fiscales de SC-9 |
| 10 | SC-1 crece en todos los diseños sin un esquema común: perfil, política personal, posiciones externas, presupuesto de riesgo, tolerancia de estrés, Kelly, límites de F, diario de decisiones | Broker, E, M, F, entrada | Un esquema único de SC-1 versionado antes de la Fase 2 (§4) |
| 11 | La comprobación de que el texto del Broker no trae cifras nuevas está en N, pero el Broker también habla en el chat | N §4, Broker §7 | La misma comprobación para toda salida del conversacional, en N y en el chat |
| 12 | P-24 (fuentes de SC-11) no incluye el BOE, que SC-9 necesita vigilar | SC-9 §8 | Añadir el BOE a las fuentes de SC-11 |

## 4. Los servicios pequeños

No necesitan un diseño propio: basta con fijar quién es su dueño y qué entregan, a partir de lo que ya piden los demás.

| Servicio | Qué es | Dueño funcional | Qué añaden los diseños | Fase |
| --- | --- | --- | --- | --- |
| SC-1 Perfil y mandato | Fuente única de lo que el operador quiere y acepta | Broker | Esquema único y versionado con: perfil, política personal (con la caída tipo 2008 de M), mandatos, presupuesto de riesgo y tolerancia de estrés en euros, fracción de Kelly, límites de F, posiciones externas y diario de decisiones del operador; exportable y borrable | 1, ampliado en la 2 |
| SC-4 Diario de pronósticos | Pronósticos y opciones descartadas congelados antes del resultado | I | Tablas de decisión de D, registro de experimentos de J y predicciones de riesgo de M | 1 mínimo (T-81) y 3 completo |
| SC-5 Eventos y auditoría | Registro anexado que no se puede reescribir | Orquestador | Huella de kits y prompts (E4-04), costes de cada ejecución (G), cambios de parámetros, accesos de la persona de confianza | 1 |
| SC-6 Validador de contratos | Comprueba cada paquete antes de pasar | Orquestador | Los contratos nuevos del §6 y la regla V-26 del Motor | 1 (ya existe en el marco) |
| SC-8 Contexto macro | Tras el hallazgo 3, solo el vigía de régimen: semáforo por región calculado con código | M y F lo usan; el Estratega macro lo explica | M cambia a correlaciones de crisis cuando marca tensión | 3 (enmienda 2) |
| SC-11 Noticias aisladas | Lee texto externo sin cartera ni claves; salida con esquema cerrado | Estratega macro | Escenarios hipotéticos para M y cambios del BOE para SC-9 | 1 mínimo y 5 completo |

## 5. Fases

Las propuestas respetan la tabla de fases de la Constitución (§14) y el reparto de la enmienda 2. Este es el resultado conjunto:

| Fase | Qué entra según los diseños |
| --- | --- |
| 0 · Cimientos | Ficha de restricciones reales con los criterios de SC-10; jurisdicción y asesor fiscal (P-06) |
| 1 · Divisas en simulación | A, B y C-DIV con la pauta común y el banco de medida; D, E, F y G; K mínimo con dos fechas por dato; N mínimo con cifra principal e informe semanal; Broker con Orquestador, conversacional mínimo y asesor de configuración; Motor unido al registro con sus primeras familias; SC-4, SC-5, SC-6 y SC-10 con simulador completo; registro de experimentos de J; sombra; reglas fiscales provisionales; bóveda local y copias |
| 2 · Segundo perfil y largo plazo | C-RV, C-IDX y C-FON; D entre clases; planificador, política personal y guardián; SC-9 firmado; inventario y transición en simulación; demostración del intermediario; atribución de I; proyecciones del Motor |
| 3 · Dinero real | Lectura real y después dinero en pequeño en L1; H; M; vigía; canal fuera del chat; autenticación; servidor y vigilante separados; simulacros; hibernación; transición real |
| 4 · Estrategias | J completo con el Investigador; trading en paper y después en L2 |
| 5 · Ampliación | Resto de perfiles por demanda; SC-11 completo; I completo |

**La decisión que mueve las fases: E4-18.** La enmienda 4 propone adelantar el plan de largo plazo y hacerlo en paralelo a la Fase 1, porque para un particular es donde está la mayor parte de la rentabilidad por euro. Si se ratifica, adelantan con él:

- el planificador;
- SC-9 con las reglas de fondos traspasables;
- C-IDX y C-FON;
- los datos de fondos de K;
- el inventario.

Y hay que revisar el tope de ocho bloques activos en las Fases 1 y 2 (D-19), porque añadir los perfiles de fondos puede superarlo. **Propuesta:** contar los perfiles de C que son casi todo código (C-IDX y C-FON) fuera del tope, igual que ya se hace con SC-4.

## 6. Contratos nuevos o que cambian

Se escriben y validan antes que el código (§14, contratos primero) y entran en SC-6.

| # | Contrato | Quien lo emite | Quien lo usa | Nuevo o cambio |
| --- | --- | --- | --- | --- |
| 1 | Tabla de decisión | D | Broker, E, SC-4 | Nuevo |
| 2 | Plan por libro y vista global (CT-G-07) | E | F, G, M, N | Cambio: tres capas |
| 3 | Informe de control con tipo de acción (CT-G-08) | F | Orquestador, N | Cambio: asimetría |
| 4 | Ejecución medida | G | I, Motor (costes) | Nuevo |
| 5 | Libro fiscal por persona | G | SC-9, I | Nuevo |
| 6 | Señal y propuesta de revisión | H | Broker, D, I | Cambio: perfil por cartera |
| 7 | Ficha de rendimiento de bloque (CT-G-17) | I | Todos, N | Ya previsto (T-82) |
| 8 | Ficha de salida de estrategia | J | E, F, H, I | Nuevo |
| 9 | Registro de experimento | J | I, SC-4 | Nuevo |
| 10 | Dato con dos fechas y catálogo de necesidades | K | Todos | Cambio |
| 11 | Informe de riesgo y pregunta previa | M | E, N, I | Nuevo |
| 12 | Cuatro cifras fiscales | SC-9 | D, E, N, planificador | Nuevo |
| 13 | Ficha de módulo del Motor | SC-3 | Validador, I | Cambio: amplía el modelo declarado |
| 14 | Perfil de capacidades del proveedor | SC-10 | G, K, N | Nuevo |
| 15 | Esquema único de SC-1 | Broker | Todos | Cambio |
| 16 | Expediente de transición | Broker y planificador | E, F, G, N, SC-9 | Nuevo |

## 7. Si el robot lo usan otras personas

Para su propio dinero, el operador no presta ningún servicio a nadie. Pero la enmienda 3 prevé una copia por usuario. Si el robot se ofrece a otras personas, aunque sea gratis, sus funciones se parecen a dos servicios de inversión: el asesoramiento y la gestión de carteras. Según la CNMV, esos servicios se contratan con entidades autorizadas ([CNMV, entidades autorizadas](https://www.cnmv.es/PORTAL/inversor/Entidades-Autorizadas.aspx)).

**Propuesta:** antes de dar una copia a nadie, consultar con un abogado especializado. Mientras tanto, el robot se usa solo con el dinero del propio operador. No es asesoramiento legal.

## 8. Las decisiones del operador, consolidadas y en orden

Las 110 preguntas se quedan en unas 100 al fusionar las repetidas. No hace falta contestarlas todas a la vez: cada una tiene un valor por defecto [PROPUESTO] en simulado, y la sesión única de decisiones (T-57) puede ir por tandas, en el orden en que bloquean.

**Tanda 1 aceptada por el operador el 11-11-2026** con sus valores por defecto: registro en `.docs/diseno/decisiones_operador.md`.

| Tanda | Cuándo | Decisiones (de dónde salen) |
| --- | --- | --- |
| 1. Antes de construir la Fase 1 | Ya | Pauta común de A, B y C con banco de medida (A, B, C, E4-13); segundo proveedor de IA (B, C); adelantar el largo plazo y el tope de bloques (E4-18, §5); asimetría de F, que cambia CT-G-08 (F); registro de experimentos desde la Fase 1 (J); informes con rangos y «todavía no se sabe» (I, N); jurisdicción y asesor fiscal (SC-9); criterios del intermediario y ficha de restricciones (G, SC-10) |
| 2. Parámetros, con el asesor de configuración | Durante la Fase 1, en simulado | Fracción de Kelly por cartera (D, E); presupuesto de riesgo y tolerancia de estrés en euros (E, M); políticas de F por cartera; umbrales de H; muestra mínima y torneo de I; presupuesto de avisos (N); tope de consumo del Broker; tolerancia de tipos de cambio (K); duraciones de cada peldaño (J, SC-10) |
| 3. Antes de la Fase 2 | Al cerrar la Fase 1 | Comparar entre clases de activo, que cambia la regla 1 del §5 (D); planificador y vehículos (Broker, SC-9, P-28); cosecha de pérdidas y planes de pensiones (SC-9); esquema de SC-1; inventario y transición (entrada); perfiles de fondos de C |
| 4. Antes del dinero real | Al cerrar la Fase 2 | Dónde corre, bóveda, topes de la clave, copias y carta de instrucciones (SC-7); canal fuera del chat (N); M ligero y su regla de entrada; pantalla contra la venta de pánico (N, M); persona de confianza y plazo de hibernación (P-30) |
| 5. Fase 4 y siguientes | Cuando llegue | Investigador cuantitativo, capital del peldaño 3 y motor de pruebas de robotTrading (J); mover capital entre estrategias (E) |

**Cambios de la Constitución que salen de los diseños** y que necesitan ratificación:

- la enmienda 4 completa;
- la asimetría de F (CT-G-08);
- la regla 1 del §5 (D);
- SC-8 reducido al vigía (hallazgo 3);
- los perfiles de C de puro código fuera del tope de bloques (§5).

Se propone reunirlos en una enmienda 5 cuando Astra termine sus revisiones.

## 9. Siguiente paso

1. **Astra revisa en orden** las veinte propuestas y esta pasada (relevo, §0 bis). Sus revisiones pueden cambiar hallazgos de aquí.
2. **El operador decide la tanda 1** (§8), con los valores por defecto para todo lo demás.
3. **Claude prepara la enmienda 5** con los cambios de la Constitución que salgan de la enmienda 4, de las revisiones de Astra y de esta pasada.
4. **Se escriben los contratos del §6** antes que el código, y empieza la construcción por la Fase 1, con el banco de medida como primer entregable.
