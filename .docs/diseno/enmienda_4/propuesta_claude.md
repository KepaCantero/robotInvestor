# Enmienda 4: aprender, auditar y centrarse en lo que rinde (propuesta de Claude)

De: Claude, 11-11-2026. Estado: **PROPUESTA PARA DISCUTIR**, cuarta enmienda a la Constitución V0.6 (`sistema_global/constitucion/Constitucion_Global.md`). No cambia nada hasta que el operador ratifique punto por punto; mientras tanto, todo es [PROPUESTO]. Copia en el repositorio del documento que el operador revisó con Claude.

Origen: catorce preguntas del operador del 11-11-2026 sobre la arquitectura global (automejora, auditoría, documentadores, conocimiento, bloques que falten, motores, agente de trading, mejora de los motores, cálculo complejo, comunicación, macro y geopolítica, Broker multiagente y perfilador), y seis puntos añadidos por Claude (★).

## 1. Resumen

No cambia ningún principio: los aplica a huecos que hoy no cubre. Todo se ordena alrededor de P17, convertido en brújula: **cada bloque, agente, motor o regla tiene que poder explicar cuánto acerca al robot a batir a la cartera sombra pasiva, en neto y por euro; lo que no puede explicarlo, sobra.**

## 2. Los cambios de un vistazo

| # | Cambio | Dónde | Qué es | Fase sugerida |
| --- | --- | --- | --- | --- |
| E4-01 | Circuito de mejora gobernada: código, documentación, fuentes, kits y prompts | §9 (ruta única) | Proceso y regla | 1, mínimo |
| E4-02 | Ficha de rendimiento por bloque y auditoría a petición | §2, §9.11; T-82 (CT-G-17) | Contrato | 1 |
| E4-03 | Pruebas de ataque periódicas | §12 | Batería de I | 2 |
| E4-04 ★ | Integridad y versión de kits y prompts | §13 | Regla | 1 |
| E4-05 | Biblioteca de conocimiento común | §3 | Servicio común nuevo | 1, mínima |
| E4-06 | Mapa de conocimiento por componente | §14 | Documento por bloque | 1 |
| E4-07 | Motor con módulos por bloque y precisión declarada | §3 (SC-3) | Regla | 1 |
| E4-08 | Cinco módulos nuevos del Motor | §3 (SC-3) | Módulos | 1 a 3 |
| E4-09 | Canal de avisos para todos los bloques | §3, §5 | Función del Orquestador | 1 |
| E4-10 | Contratos de vuelta y esquemas pendientes | §5 | Contratos | 1 |
| E4-11 | Estratega macro global | §2, SC-8 | Papel de IA | 2 |
| E4-12 | Investigador cuantitativo en J | §2 (J) | Papel de IA | 2 |
| E4-13 | Misma pauta para A, B y C, y segundo proveedor de IA | §2, §3 | Regla | 1 |
| E4-14 | Broker con seis papeles, más el Orquestador | §2 (D-21) | Estructura | 1, mínima |
| E4-15 | Perfilador con salvaguardas | §2, §6 | Papel de IA | 1 |
| E4-16 | Planificación patrimonial: deuda, pensiones, informe fiscal | §2, §7, SC-9 | Opciones de D y función del Broker | 2 |
| E4-17 | Tope anual de gasto del robot en IA y datos | §10, §11 | Regla | 1 |
| E4-18 | Plan de largo plazo en paralelo a la Fase 1 | §14 | Orden de fases | Inmediata |
| E4-19 ★ | Modo sin IA: el plan base funciona sin ningún modelo | §11 | Regla de degradación | 1 |
| E4-20 ★ | Brújula y caducidad de lo que no aporta | P17, §9.11 | Regla | 1 |

## 3. Mejora y auditoría

**E4-01 · Circuito de mejora gobernada.** Hoy el robot aprende sobre sus decisiones (I evalúa; J entrena y valida estrategias, modelos, prompts y agentes; aspirante frente a titular; autopsias; torneo), pero su código, documentación y fuentes se mejoran desde fuera sin un circuito que los conecte con lo aprendido. Se amplía la ruta única de cambios (§9.6) a todo lo que el robot es, en siete pasos: (1) medir (I: resultados, fichas, autopsias); (2) diagnosticar (dato, modelo, juicio, ejecución o azar); (3) proponer (ticket con evidencia y criterio de éxito); (4) construir (agentes de desarrollo fuera de producción, en una rama); (5) verificar (pruebas y gates, QA del agente que no construyó y, si cambia cómo decide el robot, escalera de J con la reserva sellada de I); (6) aprobar (el operador; autonomía revocable solo para cambios menores); (7) desplegar con versión nueva y vuelta atrás. Límites: el robot nunca se reescribe en producción (P2, P15); F, G, el kill-switch y los límites quedan fuera del circuito automático y cambian por la vía del §8; quien construye no puntúa (P19). Con pocas tesis al año, mejorará antes procesos, costes y errores que el acierto.

**E4-02 · Ficha de rendimiento por bloque.** Cada Documento 0 declara la misma ficha, que I calcula periódicamente y a petición («audita B»): valor añadido frente a una alternativa simple (el banco de medida de los rediseños de A y B, generalizado), precisión (calibración o indicador propio: vetos acertados en F, coste de ejecución en G, falsas alarmas en H), coste en euros y fiabilidad. Es la ficha CT-G-17 de T-82. Los hallazgos entran en E4-01.

**E4-03 · Pruebas de ataque.** Batería permanente que intenta engañar al robot (instrucciones escondidas en textos externos, datos envenenados, cifras absurdas, órdenes partidas, carteras incompletas). I la pasa periódicamente y antes de cada versión nueva; lo que se cuele es hallazgo crítico.

**E4-04 ★ · Kits y prompts como código.** Versión, huella registrada en SC-5 y prueba que impide cargar uno que no coincida; solo cambian por E4-01.

## 4. Conocimiento

**E4-05 · Biblioteca de conocimiento común.** Servicio común nuevo: métodos, fuentes académicas y profesionales, documentación de proveedores e instrumentos, lecciones de autopsias y referencias de cada kit; cada pieza con calidad (rúbrica de A), enlaces verificados, versión y **fecha de conocimiento** (para que las pruebas históricas no usen lo que entonces no se sabía). La alimenta un Documentador por lotes con modelo pequeño, que hereda el trabajo de los documentadores de A y B; la consulta cualquier agente, kit o módulo bajo demanda, con citas, como dato y no instrucción (P11). Lo que descubre se propone por E4-01. Corrige los rediseños de A y B, que mandaban los documentadores a K.

**E4-06 · Mapa de conocimiento por componente.** Áreas que necesita, dónde vive cada una (kit, código, Motor o biblioteca), fuentes, casos de prueba por área y huecos con prioridad; lo revisa el agente que no lo escribió. Huecos ya visibles: planificación financiera personal y finanzas conductuales en el Broker; microestructura en G; reglas de SC-9 pendientes del asesor (P-06).

## 5. Cálculo

**E4-07 · Un Motor con módulos por bloque y precisión declarada.** El Motor común (parte del de A: diez familias de métodos, 80 cálculos, fichas por tipo de activo, mapa de conocimientos, caché por huella, cola, máquina potente) es el diseño correcto. Dos reglas: cada Documento 0 declara los módulos que usa (faltan, entre otros, crecimiento compuesto y Kelly de D y E, costes de ejecución de G, oscilación normal por plazo de H); cada cálculo declara la precisión que necesita y el Motor elige el método más barato que la da (fórmula antes que simulación, simulaciones que paran al alcanzar el error pedido, recálculo solo de lo que cambió), registrando coste y precisión; un método nuevo solo sustituye al anterior si reproduce los resultados de referencia. El gran ahorro no está en el Motor sino en que calcule lo que hoy razonan los agentes.

**E4-08 · Cinco módulos nuevos.**

| Módulo | Para qué | Quién lo usa | Fase |
| --- | --- | --- | --- |
| Combinar las opiniones con el mercado (Black-Litterman o bayesiano) | No perseguir estimaciones exageradas | D y E | 1 |
| Optimización fiscal a varios años | Qué vender, cuándo y por qué vehículo (SC-9) | E y planificador | 2 |
| Impacto de las órdenes grandes | Cuánto mueve el precio una orden | G y F | 2 |
| Previsión macro antes de publicarse (nowcasting) | Hacia dónde va un dato | Estratega macro y vigía | 2 |
| Optimización del plan a varios años | Aportaciones, camino de riesgo, objetivos | Planificador y E | 3 |

## 6. Comunicación

Hoy: todo por el Orquestador con contratos cerrados, sin LLM transportando datos (D-23), registros comunes, auditoría de principio a fin y SC-6.

**E4-09 · Canal de avisos.** Dentro del Orquestador, avisos con tipo cerrado y esquema (cambio de régimen, foco geopolítico, dato macro fuera de lo esperado, aviso de calidad de K, kill-switch); cada bloque declara a qué se suscribe y qué hace. Un aviso informa, nunca ordena.

**E4-10 · Contratos de vuelta y esquemas pendientes.** Esquemas para CT-G-07, 11, 12, 13 y 15 (§5). Contratos de vuelta: C → B (lo que el paquete no cubría), D → C (más análisis si los rangos se solapan), H → C (revisión de tesis), I → cada bloque (ficha y propuestas), con presupuesto y límite de idas y vueltas.

## 7. Inteligencia

**E4-11 · Estratega macro global.** Los datos ya están (SC-8, vigía de régimen por código, SC-11, registro geopolítico, posicionamiento en K); falta quien saque conclusiones con un responsable único y su acierto medido. Papel de IA que trabaja por eventos (publicaciones del calendario de K, focos nuevos) y una visión semanal; produce pronósticos comprobables en SC-4; sirve a A, C, E y al Broker, **nunca a F** (D-33); usa K, SC-8, el módulo de nowcasting y la biblioteca. Pesa solo según su historial (P19); al principio informa y no mueve dinero.

**E4-12 · Investigador cuantitativo en J.** No un agente que opera a criterio, sino uno que propone hipótesis de estrategias (biblioteca, autopsias, datos de K) que se programan, se prueban sin anticipación con costes reales, pasan a simulación y, si superan la escalera, operan solas. No puntúa su trabajo: lo hace I con la reserva sellada.

**E4-13 · Pauta común para A, B y C.** El código conduce (sin directores); núcleo común más kits; pocos papeles de IA con modelo por tarea y banco de medida antes de cada recorte; Contradictor de otro proveedor y análisis independientes de modelos distintos cuando el importe lo justifica. Exige un segundo proveedor de IA con credenciales en SC-7.

## 8. Broker y operador

**E4-14 · Broker con seis papeles, más el Orquestador.** Conversacional (IA); planificador patrimonial (Motor y poca IA); asesor de configuración (IA acotada); perfilador (IA acotada); gestores de cartera (IA acotada y código); guardián de la política personal (casi todo reglas); Orquestador (código). Las decisiones de dinero siguen en D, E y F; separar papeles da menos contexto por llamada y solo se llama al que hace falta.

**E4-15 · Perfilador con salvaguardas.** Tres fuentes, de más a menos fiable: cuestionarios validados, comportamiento real (reacción en caídas, anulaciones, peticiones) y conversaciones. Propone valores para T-57 con consecuencias en euros, por el asesor de configuración. Salvaguardas: el operador ve qué se dedujo y de dónde; nada se aplica sin confirmación; bajar riesgo al momento, subirlo con segundo factor y espera (§6); sin temas personales ajenos a las finanzas salvo activación; datos solo en SC-1, exportables y borrables.

**E4-16 · Planificación patrimonial.** D compara también amortizar deuda (devolver un préstamo al 3 % equivale a ganar un 3 % seguro) y aportar a planes de pensiones con deducción (la deducción se cobra seguro y puede valer más que un año normal de mercado, con el dinero inmovilizado; lo valida el asesor, P-06). Informe fiscal anual desde el libro fiscal de G.

## 9. Economía y prioridades

**E4-17 · Tope anual de gasto del robot.** Hoy hay topes por oportunidad, encargo y día, pero no frente al capital. Con 20.000 € invertidos, 300 € al año de IA y datos son un 1,5 % de rentabilidad perdida. Tope anual como porcentaje del capital gestionado, que fija el operador; el Orquestador lo reparte, avisa y, al llegar, solo deja plan base, vigilancia y control; N muestra cada mes gasto frente a aportación.

**E4-18 · El plan de largo plazo en paralelo a la Fase 1.** La mayor parte de la rentabilidad por euro de un particular sale de la asignación, los costes, los impuestos, el ahorro y no vender en las caídas; la táctica en divisas es de lo más difícil para batir a no hacer nada. Segunda rebanada en paralelo: C-IDX y C-FON (casi todo código), plan base de E con aportaciones, G con fondos y traspasos, SC-9. Hay que revisar el tope de ocho bloques activos: hoy cuenta `C-DIV` como uno; con C como un solo bloque con varios kits, cabe.

**E4-19 ★ · Modo sin IA.** Si fallan todos los proveedores de IA o se agota el presupuesto, el robot sigue manteniendo el plan base, vigilando, ejecutando stops y controlando riesgo: D a H y el plan de largo plazo funcionan sin ningún modelo. Extensión de P13 y §11; se prueba periódicamente apagando la IA en simulado.

**E4-20 ★ · Brújula y caducidad.** Cada pieza declara qué aporta frente a su alternativa simple (ficha de E4-02); lo que en dos revisiones seguidas del presupuesto de complejidad (§9.11) no demuestra aportar se propone retirar, y decide el operador.

## 10. Lo que no se propone

| Idea | Por qué no |
| --- | --- |
| Agente que opere en trading a criterio | No se puede probar con el pasado, cuesta tokens y tiempo, sin pruebas de ventaja; el valor está en E4-12 |
| Un motor por bloque | Duplicaría código y cifras; mejor E4-07 |
| Que el robot se reescriba en producción | Un sistema que cambia sus controles no tiene controles; mejor E4-01 |
| Comité de agentes en el Broker | Más debate no da mejores decisiones y multiplica el coste; mejor E4-14 |
| Perfilador sin límites | Señal débil y riesgo alto para la privacidad; mejor E4-15 |
| Macro en tiempo real continuo | La macro cambia por publicaciones; mejor por eventos (E4-11) |
| Más bloques | Riesgo de sobreingeniería (§14); casi todo son papeles, módulos y reglas; solo la biblioteca es servicio nuevo |

## 11. Adopción y preguntas

Adopción: revisión de Astra (la última de su lista, después de las de los bloques); ratificación punto por punto con decisión en el §15 y valores en T-57; Constitución V0.7; ajuste de los diseños de bloque afectados y un ticket por punto.

Orden sugerido: (1) E4-18 y E4-19; (2) E4-17 y E4-20; (3) E4-02 y E4-13; (4) E4-01 mínimo, E4-04 y E4-05 mínima; (5) el resto por fases.

Preguntas para el operador (valores por defecto [PROPUESTO]):
1. ¿Ratifica la brújula (E4-20) como regla general?
2. ¿Adelanta el plan de largo plazo (E4-18)?
3. Tope anual de gasto (E4-17): se propone un 0,5 % del capital gestionado.
4. ¿Segundo proveedor de IA (E4-13)?
5. Autonomía para cambios menores en el circuito de mejora (E4-01): se propone que no al principio.
6. Perfilador (E4-15): se propone empezar sin la tercera fuente (conversaciones).
7. Estratega macro (E4-11): se propone la Fase 2.
