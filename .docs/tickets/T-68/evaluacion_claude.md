# Evaluación del Bloque B: precisión frente a consumo (Claude, 11-11-2026)

Copia de trabajo en el repositorio del documento que Claude preparó para el operador, para que Astra pueda revisarla (ver `encargo_revision_astra.md`). No se cambió nada del Bloque B: es solo lectura y medición. Las mediciones se reproducen con `.docs/scripts/medir_consumo_b.py`.

## Resumen

El Bloque B gasta el 96 % de sus tokens de entrada en releer instrucciones, no en analizar. En un análisis N2 simulado, los prompts de sistema suman unos 950.000 tokens y el encargo propiamente dicho, unos 35.000. Cada llamada envía el prompt íntegro de su agente (de 17.000 a 45.000 tokens), aunque la tarea solo use una parte.

Las mejoras con más efecto, por orden:

1. **Caché por agente.** Hoy se cachea todo con una hora de vida, y la escritura cuesta el doble. Pero 11 a 14 de los 16 o 17 agentes de cada análisis se llaman una sola vez, así que esa caché se paga y no se lee. Cachear solo a los que repiten baja la entrada entre un 29 % y un 36 % sin tocar ningún prompt.
2. **Prompts por módulos (núcleo + perfil).** El Seleccionador lleva sus 12 playbooks en cada instancia y usa uno: el 35 % de su prompt sobra en cada llamada. Los especialistas repiten el marco común, entre el 24 % y el 34 % de su texto. Cargar solo lo que la tarea necesita ahorra tokens y probablemente mejora la precisión, porque hay menos instrucciones que compitan.
3. **Medir la precisión antes de recortar.** El bloque ya tiene un backtest sin anticipación y una comparación con el azar. Falta usarlos para la pregunta clave: cuánta precisión añaden los agentes sobre la selección determinista, y a qué coste.
4. **Lotes para lo que no corre prisa.** La evaluación, el Vigía, el mantenimiento de F7 a F9 y los backtests pueden ir por la API de lotes, al 50 % de precio.
5. **Funciones que la Constitución ya pone en otros bloques.** El Evaluador, el Vigía, el Orquestador y los documentadores de B duplican lo que hacen I, H, el Orquestador del Broker y los servicios comunes. Es la pregunta de arquitectura con más alcance.

## Cómo se evaluó

Tres análisis completos de ejemplo, en N2 y con el cliente simulado (sin coste), con cada llamada a un agente registrada: redes eléctricas (`ejemplos/peticiones/peticion_redes_bloque_a.json`, desde el Bloque A), India y cobre. Los tres llegaron a ENTREGADA con G3 APTO, en 27 a 29 llamadas.

- **Qué se mide bien:** cuántas llamadas hay, a qué agente y con qué modelo, y cuántos tokens de entrada lleva cada una (prompt de sistema y encargo). La entrada no depende del modelo, así que estas cifras valen para la API real.
- **Qué no se mide:** la salida. El simulador devuelve respuestas cortas de plantilla; una respuesta real será varias veces más larga. Tampoco se mide la precisión: con datos sintéticos no significa nada.
- **Precisión de la cifra:** el simulador cuenta 3,6 caracteres por token (`_tokens_aprox` en `bloque_b/11_Ejecutor/bloque_b/llm.py`). En español el recuento real puede ser entre un 10 % y un 20 % mayor; las proporciones no cambian.
- **Costes:** con los precios publicados por Anthropic ([precios](https://platform.claude.com/docs/en/about-claude/pricing), [caché](https://platform.claude.com/en/docs/build-with-claude/prompt-caching)), solo de la entrada. Opus 5.5 cuesta 4 $ por millón de tokens de entrada, Sonnet 5.5 2 $ y Haiku 5.5 0,10 $. Escribir en la caché de una hora cuesta 2 veces la entrada, en la de 5 minutos 1,25 veces, y leerla 0,05 veces en Opus y Sonnet 5.5 (0,1 en Haiku). Las llamadas en paralelo no aprovechan la caché hasta que la primera empieza a responder.

## Arquitectura actual

El Bloque B recibe del Broker un ámbito y devuelve candidatos para los Bloques C, en cinco capas con una puerta entre cada una. Tiene 24 agentes; en un N2 trabajan 16 o 17 con prompt propio, y el Motor, la puntuación HT-03 y la validación G3 son código.

| Capa | Agentes (modelo) | Puerta de salida |
| --- | --- | --- |
| 0 · Admisión y plan | Coordinador (Haiku), Director · plan (Opus) | PT30 (tiempo) |
| 1 y 2 · Viabilidad y núcleo | Director · tesis (Opus), especialistas líderes (Sonnet), Curador (Haiku), Motor (código) | PV1 y PV2 |
| 3 · Profundización y selección | Resto de especialistas y Emergentes (Sonnet), Seleccionador · una instancia por tipo (Opus), Motor y HT-03 (código) | PV3 |
| 4 · Contraste y veredicto | Prospectiva (Sonnet), Contrario (Opus), Director · veredicto (Opus), G3 (código) y Auditor (Opus) | G3 |
| Salida | Redactor (Sonnet), entrega CT-B-02 (código) | — |

Secuencia de llamadas medida en el análisis de redes eléctricas (29): B01 → B02 → B18 → B03 → B02 → B01 → B03 → B04 → B05 → B09 → B15 → B02 → B06 → B07 → B02 → B15 → B03 → B24 → B02 → B12 → B12 → B12 → B13 → B14 → B02 → B12 → B02 → B22 → B17.

## Consumo medido

Un análisis N2 consume unos 990.000 tokens de entrada en 27 a 29 llamadas, y 950.000 de ellos son prompts de sistema. Casi la mitad del coste de entrada, entre el 47 % y el 53 %, es del Director.

Miles de tokens de entrada por agente, análisis de redes eléctricas:

| Agente | Modelo | Llamadas | Prompt de sistema | Encargo |
| --- | --- | --- | --- | --- |
| Director (AG-B02) | Opus | 7 | 315,0 | 8,9 |
| Seleccionador (AG-B12) | Opus | 4 | 144,6 | 5,3 |
| Estructura (AG-B03) | Sonnet | 3 | 102,4 | 4,1 |
| Coordinador (AG-B01) | Haiku | 2 | 72,1 | 1,3 |
| Emergentes (AG-B24) | Sonnet | 1 | 38,8 | 3,1 |
| Curador (AG-B15) | Haiku | 2 | 33,3 | 1,0 |
| Finanzas (AG-B09) | Sonnet | 1 | 31,8 | 1,1 |
| Demanda (AG-B04) | Sonnet | 1 | 29,5 | 1,2 |
| Regulación (AG-B07) | Sonnet | 1 | 29,2 | 1,1 |
| Tecnología (AG-B06) | Sonnet | 1 | 28,1 | 1,1 |
| Oferta (AG-B05) | Sonnet | 1 | 28,0 | 1,1 |
| Redactor (AG-B17) | Sonnet | 1 | 23,6 | 1,0 |
| Prospectiva (AG-B13) | Sonnet | 1 | 23,2 | 0,8 |
| Contrario (AG-B14) | Opus | 1 | 20,4 | 2,1 |
| Auditor (AG-B22) | Opus | 1 | 18,3 | 1,1 |
| Documentador (AG-B18) | Sonnet | 1 | 17,6 | 0,6 |

| Análisis simulado | Llamadas | Coste de entrada hoy (caché de 1 h en todos) | Con caché solo en los que repiten | Además, Director y Seleccionador por módulos |
| --- | --- | --- | --- | --- |
| Redes eléctricas (desde A) | 29 | 2,29 $ | 1,63 $ (−29 %) | 1,40 $ (−39 %) |
| India | 29 | 2,31 $ | 1,62 $ (−30 %) | 1,39 $ (−40 %) |
| Cobre | 27 | 2,33 $ | 1,48 $ (−36 %) | 1,31 $ (−44 %) |

Solo la entrada, a precio de lista. La salida no se puede medir en simulado; en real puede costar tanto como la entrada, porque Opus cobra 20 $ por millón de tokens de salida. La última columna supone un Seleccionador con su playbook (−35 %, medido) y un Director un 30 % más corto por fase (supuesto).

Proporción del marco común (`02_System_prompts/Marco común de los Analistas de dimensión (plantilla) - Bloque B - V2.0.md`) copiado palabra por palabra dentro de cada prompt: Demanda 32 %, Emergentes 24 %, Estructura 28 %, Finanzas 30 %, Flujos 34 %, Macro 28 %, Oferta 34 %, Regulación 32 %, Sostenibilidad 33 %, Tecnología 34 %. Los 12 playbooks del Seleccionador son el 38 % de su prompt; los 11 que no usa cada instancia, el 35 %.

## Diagnóstico

El diseño es riguroso y el código es sólido: 176 pruebas en verde, el Motor y la validación G3 son deterministas y no gastan tokens, y la protección contra la anticipación está bien resuelta. El problema no es de calidad, sino de cómo se reparte el contexto.

**Dónde se va el consumo**
- **Prompts monolíticos.** Cada agente recibe su protocolo entero en cada llamada (`Prompts.system` en `bloque_b/11_Ejecutor/bloque_b/prompts.py`). El del Director tiene unos 160.000 caracteres (≈ 45.000 tokens), con 33 apartados de método; se envía igual para planificar en F0 que para emitir el veredicto en F7.
- **El Director y el Seleccionador, en Opus, son la mitad del gasto.** El Director pesa entre el 47 % y el 53 % del coste de entrada y el Seleccionador entre el 6 % y el 21 %, según cuántos tipos de activo toque el ámbito.
- **La caché se paga sin usarse.** Todo se cachea con una hora de vida (`llm.cache_ttl: 1h`). Casi todos los especialistas, el Prospectivo, el Contrario, el Auditor y el Redactor se llaman una vez por análisis: escriben en la caché al doble de precio y nadie la lee, salvo que llegue otra petición del mismo agente en menos de una hora. Además, F2 lanza los especialistas en paralelo.
- **Texto repetido entre agentes.** Entre el 24 % y el 34 % de cada prompt de especialista es el marco común. Hoy no se puede compartir en caché, porque va mezclado con lo propio de cada uno.
- **Precios sin configurar.** `precios_por_millon` está vacío en `config/por_defecto.yaml`, así que el bloque cuenta UC, pero no euros. No hay tope de coste por petición (la descripción de arquitectura dice «no hay techo de coste»).

**Dónde se juega la precisión**
- **Nadie ha medido lo que aportan los agentes.** El backtest (`bloque_b/11_Ejecutor/bloque_b/backtest.py`) puede correr solo la parte determinista de la selección (universo, Motor y puntuación S) y compararla con el azar. Falta compararla con el análisis completo con agentes.
- **Instrucciones que compiten.** Un prompt de 45.000 tokens con decenas de reglas reparte la atención del modelo. Cargar solo el módulo de la fase suele mejorar el cumplimiento de las reglas que sí aplican. Es una hipótesis que hay que validar, no un hecho medido.
- **La certificación llega tarde.** Con pocos pronósticos por petición y la regla conservadora de ventanas solapadas (H-03 de T-61, en la fila T-68 de la deuda), tardará en haber probabilidades certificadas.
- **Una ronda por especialista en simulado.** El diseño prevé rondas guiadas por el valor informativo; en real habrá más llamadas que las 27 a 29 medidas, y conviene un tope por petición.

## Mejoras propuestas

| # | Mejora | Efecto en tokens o coste | Efecto en precisión | Esfuerzo | Depende de la arquitectura |
| --- | --- | --- | --- | --- | --- |
| 1 | **Banco de medida**: backtest con datos históricos congelados, comparando selección determinista, análisis completo y azar, con coste por variante | Ninguno; es la base para decidir el resto | La mide (exceso del top-N, IC de rango, Brier) | Medio: faltan datos reales y llamadas reales en modo sombra | No |
| 2 | **Caché por agente**: una hora para los que repiten en un análisis (Director, Seleccionador, Estructura, Curador) y ninguna para los demás | Entrada entre un 29 % y un 36 % más barata | Ninguno | Bajo | No |
| 3 | **Seleccionador con un solo playbook** | 35 % menos de prompt por instancia | Probablemente mejor | Bajo-medio | Poco (encaja con D-10) |
| 4 | **Marco común en caché compartida** (primer bloque idéntico en todos los especialistas) | Entre el 24 % y el 34 % de cada especialista, leído a 0,05× tras el primero | Ninguno | Medio (reordenar prompts y escalonar F2) | No |
| 5 | **Director por fases** (núcleo + módulo por fase) | Junto con la 2 y la 3, entre un 39 % y un 44 % menos (con un Director un 30 % más corto por fase, supuesto) | Probablemente mejor | Medio-alto | Sí |
| 6 | **API de lotes** para evaluación, Vigía, mantenimiento de F7 a F9 y backtests | 50 % en todo lo que no corre prisa | Ninguno | Bajo-medio | No |
| 7 | **Precios y tope en euros** por petición, con autorización al pasarlo | Coste real en cada entrega | Ninguno | Bajo | Poco (PA-08 de T-67) |
| 8 | **Modelo por tarea, no por agente** | Sonnet cuesta la mitad que Opus; Haiku 5.5, la vigésima parte que Sonnet | Hay que medirlo con el banco | Bajo de hacer; medio de validar | No |
| 9 | **Pasar a código lo que es regla** (admisión y estimación del Coordinador, normalización y deduplicación del Curador) | Poco coste (hoy van en Haiku), menos latencia y fallos | Mejor | Medio | No |

## Preguntas de arquitectura para la discusión

**Del Bloque B**
1. ¿Cuántos papeles de IA necesita B? (24 agentes hoy; en A quedó aplazada la propuesta de unos 6 papeles con prompts núcleo + perfil, PA-06 y PA-07 de T-67.)
2. ¿Qué aporta el análisis con agentes sobre la selección determinista?
3. ¿Qué modelo para cada decisión? ¿Merece la pena Fable 5.1 para la refutación en N3?
4. ¿Tope de coste por petición en euros?

**De las fronteras con los demás bloques**

5. Funciones que la Constitución pone fuera de B (evaluador AG-B23 → I; Vigía → H; Orquestador AG-B21 → Orquestador del Broker; documentadores → servicios comunes y K).
6. B frente a C: ¿hasta dónde valora B para ordenar, si C hace la valoración profunda?
7. A frente a B: ¿debe B analizar solo el delta sobre lo que A ya contrastó?
8. Núcleo + perfil (D-10, D-42): ¿adelantar la parte de los prompts antes de la Fase 2?
9. ¿La misma pauta para todos los bloques, empezando por C-DIV?
