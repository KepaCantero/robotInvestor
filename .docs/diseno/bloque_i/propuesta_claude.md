# Bloque I: saber qué funciona y por qué (propuesta de diseño de Claude)

De: Claude, 11-11-2026. Estado: **PROPUESTA PARA DISCUTIR**. No hay nada que implementar: el operador está decidiendo la arquitectura de los bloques antes de construir (relevo de Astra, §0 bis). Copia en el repositorio del documento que el operador revisó con Claude.

## 1. Respuesta corta

I es el juez del robot: mide si gana al plan pasivo, explica de dónde sale cada euro, dice quién acierta y propone qué cambiar. No aplica cambios; los propone por la ruta única (§9). La Constitución ya define sus piezas (§9: diario de pronósticos, calibración agrupada, torneo, seguimiento de lo descartado, cartera sombra, autopsias, presupuesto de complejidad, veredicto por código con reserva sellada). Se propone:

1. **Cuatro preguntas, siempre las mismas:** ¿ganamos al plan pasivo?, ¿de dónde sale el resultado?, ¿quién acierta?, ¿qué cambiamos?
2. **Atribución por etapa de decisión:** cada etapa comparada con su alternativa simple, en euros.
3. **Estadística honesta:** rangos en lugar de cifras, separar suerte de método y apoyarse en lo que acumula muestra.

I es casi todo código; la IA solo redacta borradores de autopsia y resúmenes, por lotes y con modelos baratos.

## 2. Por qué I decide la rentabilidad a largo plazo

| Bloque | Qué necesita de I | Qué pasa si I falla |
| --- | --- | --- |
| D | Calibración de cada autor | Confía igual en todos, o en el que tuvo suerte |
| E | Si el riesgo real se parece al presupuesto | Apuesta de más o de menos sin saberlo |
| F | Lo que costó cada veto | Se endurece y nunca se revisa |
| G | Coste real de cada ejecución | Los costes de D, E y F siguen siendo una suposición |
| H | Qué señales predijeron | Falsas alarmas sin corregir |
| A, B y C | Valor de cada agente frente a la alternativa simple | Se paga por agentes que no aportan |
| J | Veredicto de la escalera | Un aspirante sobreajustado sustituye al titular |

Dos fallos opuestos: **ver señal donde solo hay suerte** (el más frecuente y caro) y **no ver nada por exceso de prudencia** (se combate midiendo lo que acumula muestra deprisa).

## 3. Qué hay hoy y qué falta

Existe: la cartera sombra pasiva (V0.71: registro encadenado, comparación mensual neta y real, juicio a 24 meses; faltan datos reales de K, T-86, e impuestos de SC-9); el sobre con probabilidad y plazo y el registro de lo descartado (H-15); la auditoría encadenada; evaluadores propios en A y B. La Constitución deja el bloque completo para el final, con diario, informes sencillos, torneo y calibración desde la Fase 1.

Falta: diario mínimo con Brier, torneo y calibración por autor (T-81, en espera); atribución por etapa; ficha por bloque (T-82, CT-G-17; E4-02); autopsias; cuenta de costes del robot; una sola evaluación (los evaluadores de A y B duplican a I).

## 4. Las cuatro preguntas

**¿Ganamos al plan pasivo?** La sombra, cada mes, en neto y en real, **siempre con rango**; si incluye el cero, «todavía no se sabe».

**¿De dónde sale el resultado?**

| Etapa | Bloque | Alternativa simple | Qué dice |
| --- | --- | --- | --- |
| Qué buscar | A y B | Selección por código en el mismo universo | Si sus agentes mejoran una regla |
| Qué se sabe | C | La tasa base sola | Si el análisis añade algo |
| Qué elegir | D | Plan pasivo y opciones descartadas | Si eligió bien |
| Cuánto poner | E | Tamaño fijo por regla | Si el tamaño ajustado ganó |
| Qué se impide | F | Sin veto o con la cantidad pedida | Si protegió o frenó |
| Cómo ejecutar | G | Precio en el momento de la decisión | Coste real de ejecutar |
| Cuándo salir | H | Mantener hasta el plazo | Si salir ganó a no tocar |
| Cuánto cuesta pensar | Todos | Cero | Gasto en IA, datos y cálculo |

La suma explica la diferencia con la sombra de forma aproximada (las etapas se influyen), y el informe lo dice.

**¿Quién acierta?** Brier y calibración por autor (perfil de C, nivel, modelo, estrategia, Estratega macro), siempre frente a una referencia ingenua (la tasa base o el 50 %); pesos contraídos hacia iguales con poca muestra (§9.14); el Contradictor, por objeciones confirmadas.

**¿Qué cambiamos?** Autopsias (dato, modelo, juicio, ejecución o azar), fichas y presupuesto de complejidad generan propuestas con evidencia, la medida que debe mejorar y cuánto, por la ruta única. El azar no genera propuestas.

**Flujo:** libro de G, diario SC-4, sombra y auditoría SC-5 → (1) resolver (código) → atribuir, calibrar y fichas → (2) rangos y muestra (código: si no hay muestra, no se concluye) → (3) diagnosticar (la IA redacta, el código comprueba) → (4) proponer → ruta única (J valida con la reserva sellada; el operador aprueba) e informes (calibración a D; informe mensual con rangos a N).

## 5. Estadística honesta

Años para probar una ventaja con unas dos desviaciones típicas ≈ (2 × oscilación frente al índice ÷ ventaja)²:

| Ventaja anual | Oscilación frente al índice | Años |
| --- | --- | --- |
| 3 % | 6 % | 16 |
| 2 % | 4 % | 16 |
| 2 % | 8 % | 64 |
| 1 % | 4 % | 64 |

Dos años de rentabilidad no prueban casi nada: la regla de los 24 meses es una buena regla de decisión, no una prueba.

| Medida | Observaciones al año (orientativo) | Cuándo dice algo |
| --- | --- | --- |
| Procesos | Continuo | Semanas |
| Operaciones de trading por estrategia | Cientos | Meses |
| Torneo de pronósticos | Cientos, si se diseña para ello | Uno o dos años |
| Sub-pronósticos | Decenas | Dos o tres años |
| Tesis completas | Unas decenas | Muchos años |

Trampas: probar muchas cosas y quedarse con la que salió bien (contar también los intentos descartados); usar datos que entonces no se sabían (fecha de conocimiento de K); mover la vara después (criterio fijado antes, D-37); corregir lo que fue mala suerte; recalibrar con el resultado predicho (prohibido, §9); mirar solo lo que se hizo (seguimiento de lo descartado).

## 6. Fronteras

| Quién | Relación con I |
| --- | --- |
| SC-4 | Materia prima; I resuelve y puntúa, nunca reescribe |
| J | Entrena; I da el veredicto con código y reserva sellada (D-39) |
| K | Resultados y precios con fecha de conocimiento |
| SC-5 | Fuente de la atribución y de los costes |
| Todos los bloques | Reciben su ficha y propuestas (E4-10) |
| N y Broker | Informes en lenguaje sencillo, en euros y con rangos |
| Operador | Aprueba; I nunca aplica (§2) |

I recalcula desde los registros las cifras que le pase cualquier bloque; los evaluadores de A y B pasan a I.

## 7. Precisión, consumo y orden

Consumo casi cero: solo un Redactor de autopsias (modelo barato, por lotes; el código comprueba referencias y coherencia; muestra revisada) y el resumen mensual. Precisión: reproducible desde los registros; probado con historias simuladas de respuesta conocida (ventaja real, suerte, filtro estricto); QA por el otro agente, incluido intentar que I «vea» una ventaja inexistente.

Orden: Fase 1, diario mínimo con Brier, torneo y calibración (T-81), sombra con datos de K (T-86) y ficha por bloque (T-82); Fase 2, atribución por etapa, seguimiento de lo descartado completo y autopsias; al final (§14), el resto.

## 8. Preguntas para el operador

1. Informes con rangos y «todavía no se sabe».
2. Mantener la regla de los 24 meses y añadir calibración y atribución al juicio.
3. Muestra mínima (P-32): 30 pronósticos por autor para empezar a pesar, con contracción fuerte hasta 100.
4. Torneo de unas 200 preguntas al año, con un coste pequeño y constante.
5. Atribución por etapa en la Fase 2.
