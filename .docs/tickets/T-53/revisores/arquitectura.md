# Bloque A: revisión independiente de arquitectura y agentes

**Alcance.** Diseño del Bloque A V5.1 (Documento 0 V5.1, arquitectura V4.0/V5.1, 35 prompts, ejecutor V1.2) frente a la Constitución Global V0.6. No se ha modificado ningún archivo. Las cifras de tokens son estimaciones (3,6 caracteres por token, el mismo criterio que usa `llm.py`). Abreviaturas: «D0» es el Documento 0 de A, «Const.» la Constitución y «ejecutor» `bloque_a/11_Ejecutor/bloque_a/`.

---

## 0. Resumen

1. **El A que se ejecuta no es el A que se documenta.** El D0 describe 25 agentes LLM que se pasan contratos entre sí. El ejecutor es un programa determinista que hace casi todo: GC0, puertas, HT-03, deduplicación, G3, congelación, resolución, métricas, C6 y colas. Llama a un LLM en unos 8 tipos de llamada. Tres agentes no se invocan nunca: AG-13, AG-15 y el C4 de AG-14 y AG-16. En otros tres la llamada no cambia nada o casi nada: el dictamen de AG-18 se ignora, AG-02 tiene orden de «no cambiar la selección» y AG-20 solo redacta. Los prompts siguen describiendo un mundo que el código ya no ejecuta.
2. **Los prompts cuestan mucho y aportan poco por token.** Suman unos 593 000 tokens. Cada Analista ronda los 17 000–25 000, y entre el 38 y el 49 % es una «base de conocimientos» de manual. Con la caché de 1 h y un ciclo semanal, cada ciclo vuelve a escribir en caché todos los prompts. En la simulación, el primer ciclo escribió unos 309 000 tokens de caché frente a 41 000 de salida. En la Fase 1, solo con divisas, el prompt fijo por ciclo bajaría de unos 180 000 tokens a unos 25 000–30 000 (estimación) sin perder función.
3. **Los 12 Analistas ya son núcleo + perfil en el texto, no en la ejecución.** Las secciones 1–5, 7–9 y 12 son idénticas a la plantilla (similitud 1,00 en los 12). Pero se mantienen copiadas a mano, y el ejecutor da a los 12 las mismas 6 señales genéricas. El Analista de Divisas no puede aplicar su regla GC1 porque exige carry, valor y posicionamiento, que nadie le pasa.
4. **Para conectarse a la Constitución faltan cosas.** Faltan el adaptador, la ficha CT-G-17, la batería de conformidad, el uso de K, SC-4 y SC-5, el presupuesto en euros, valores por defecto con su pregunta y el radar tecnológico. Además, el catálogo CT-G no tiene ningún contrato para encargar trabajo a A ni para su paquete. Hay tres choques directos con principios ratificados:
   - autoajuste de pesos y umbrales (P8, §9.6);
   - hitos H5 a 30 y 54 meses (§9.2 y §9.10 piden 12 meses o menos);
   - la referencia de comparación no es «no hacer nada» (P5).
5. **La refutación es débil.** El refutador es del mismo proveedor y ve el razonamiento del analista (contra D-43.2). Es el propio analista quien declara «resuelta» cada objeción. El `veredicto_global` es obligatorio en el esquema, pero ninguna decisión lo usa.
6. **Los pronósticos son verificables, pero su muestra está inflada y los temas los eligen los agentes.** Las celdas no corrigen la correlación entre pares el mismo día. Las vistas «lateral» se descartan y solo se pronostica lo que el agente propone (contra D-37). Los backtests con LLM se hacen sin anonimizar por defecto.
7. **Recomendación central:** en la Fase 1, A debería ser un perfil `DIV` sobre un núcleo pequeño, con unos 5–6 papeles LLM:
   - Analista de perfil;
   - Prospectiva;
   - Contradictor de otro proveedor;
   - un único Sintetizador (integrar y redactar);
   - un respondedor de consultas N0;
   - y, como opción, un Curador pequeño.

   Todo lo demás queda como código o como servicio común (K, SC-3, SC-4, SC-5, SC-6 y el Orquestador).

## 1. Lo que está bien diseñado (sin propuesta)

- **Frontera A/B por ámbito**, con un `indicador_seguimiento` que es un símbolo del universo. Cada pronóstico queda atado a una serie medible (`orquestacion.py` 577–592).
- **Selección y validación deterministas**: HT-03 para el top-3 y HT-09 para G3, con un bloqueo que ningún LLM puede levantar (`orquestacion.py` 1092–1093). Cumple P2 y anticipa SC-6.
- **GC0 determinista con «arrastre verificado»**: en la simulación, 7,4 UC por ciclo frente a 44 de un ciclo completo (README del ejecutor, §8). Es la mejor pieza de ahorro.
- **Resolución determinista de pronósticos**, con tasa base sin fuga (RI-TB, ventanas no solapadas), Brier/BSS/ECE, certificados con Holm y Bröcker-Smith, y congelación también de las finalistas no seleccionadas. Supera el mínimo de §9.
- **R13 y R14**: bandas verbales sin certificado, y «menos de tres» como resultado legítimo. Es coherente con P5 y P16.
- **Credenciales**: bóveda con alias, sin valores en ningún contexto (P11, §12.1).
- **Mock y Replay** (`llm.py`): sirven para el conjunto dorado de D-40 y para comparar aspirante y titular de un prompt.
- **C6 implementado como código** (`seguimiento.py`, cabecera). Demuestra que la revisión ligera no necesita LLM.

## 2. Hallazgos

### 2.1 Encaje con la Constitución

**Qué hace A que ya cubre una pieza global:**

| Pieza de A | Pieza global | Situación | Propuesta |
|---|---|---|---|
| AG-13 Motor y MC-01…MC-10 (≈ 108 000 tokens de prompt) | SC-3, que «parte del Motor de A» (§3, D-29) | El LLM del Motor no se invoca (README del ejecutor, §9.3) | Extraer el código como SC-3; los MC pasan a ser documentación del módulo, no prompts |
| HT-01 datos | K, único sello de corte (§2, D-18) y SC-10 | A tiene su propio proveedor y su propia frescura (PS2) | Adaptador HT-01 → K |
| AG-16: posicionamiento, CFTC y 13F | K, posicionamiento sin LLM (§2, §3 registros) | Duplicado y hecho con LLM | Que POS lo lea de K |
| AG-14 y AG-16 con web | SC-11, lectura aislada con esquema cerrado (§3, §12.4) | Devuelven texto libre («afirmación») que llega a otros agentes, aunque saneado | En la Fase 1, que el lector sea SC-11 mínimo |
| AG-01: colas, prioridades, cron y plazos | Orquestador determinista del Broker (§2, D-21/D-23) | Ya es código (HT-05, `ciclo`); el prompt de 26 000 tokens describe lo mismo | AG-01 queda solo como respondedor N0 |
| AG-18: colas, presupuesto e instancias; dictamen G3 | Orquestador y SC-6 | El dictamen se ignora (`orquestacion.py` 1097–1099) | Retirar el LLM |
| AG-20 Evaluador | SC-4 mínimo con calibración (Fase 1) e I (Fase 4–5) | El evaluador es código; el LLM solo redacta | Su código pasa a SC-4 común, junto con la certificación de B (T-68) |
| AG-19 Auditor | Revisión independiente, «preferiblemente de otro proveedor» (§14, regla 5) | Mismo proveedor; los hallazgos van a HA y nadie los consume | Fase 2, con muestreo y con el lazo cerrado |
| AG-11 Contrarias | Contradictor (§3.2, CT-G-03 con veredicto calculado por regla) | Mismo proveedor, ve el razonamiento y elige su propio veredicto | PA-05 |
| AG-17: informe visual al usuario | N y Broker conversacional, únicas superficies del operador (§2) | A produce lenguaje llano para el usuario: papel duplicado | PA-13 |
| F4 | SC-4 diario de pronósticos | Diario propio de A | Publicar en SC-4 |
| F5 y HA | SC-5 eventos y auditoría con `correlation_id` | Registro propio | Duplicar los eventos hacia SC-5 |
| F10 | Configuración versionada y SC-1 | Mezcla parámetros técnicos con preferencias del usuario | PA-11 |

**Qué le falta a A para conectarse:**

- **Contrato.** El catálogo CT-G (§5) no tiene encargo a A ni paquete de A. La Const. supone que A habla «CT-B» (§5, enchufabilidad punto 4), pero los contratos de A son CT-01…CT-25 sin prefijo, y CT-B-xx son los de B. Hace falta una enmienda o una ficha que lo declare (PA-02).
- **Ficha CT-G-17, registro y batería de conformidad.** No existen (§5, §14 regla 5).
- **Sobre.** A no emite `event_id`, `correlation_id`, `expediente_id`, `valid_until`, `data_refs` ni `resultado_politica` (§5). No hay correspondencia definida entre OPP- y expediente en estado `DETECTADA` (§4.1).
- **Registro de análisis vigentes** (§3, D-23). A no lo publica ni lo consulta: solo reutiliza lo suyo con HT-06.
- **Radar tecnológico y registro de tendencias tecnológicas.** Están en la fila de A (§2) y en §9.10. No aparecen en el D0.
- **Probabilidad, plazo y criterio.** A los tiene (PRG con `fecha_resolucion`, criterio congelado y `prob_interna`). Pero los hitos H5 de 30 y 54 meses (`por_defecto.yaml` `h5.meses_hitos`, D0 Anexo A) incumplen §9.2 y §9.10. La probabilidad la produce un LLM y debe ir etiquetada como juicio (P3, §10.3).
- **Valores por defecto con justificación y pregunta** (D-44, D-45). El Anexo A tiene valor y «régimen», pero no justificación ni pregunta. Las referencias de 8.4 están «a ratificar» sin valor por defecto justificado.
- **Presupuesto duro en euros por encargo y por día** (§11, P-07) y coste de análisis para P17. Los precios están a `null` y el coste sale vacío.
- **Modos degradados.** El D0 §17.5 no recorre la tabla de fallos de §11 (bucle de agentes, presupuesto agotado con `INCOMPLETO`, datos contradictorios).
- **Aprendizaje.** El D0 (§12.1–12.2 y §18.1, tipo 2) permite que el Evaluador o el Orquestador cambien pesos y umbrales por su cuenta. Eso choca con P8 y con la ruta única (§9.6). El ejecutor lo mitiga con `aplicar_recalibracion: false`.
- **Referencia de comparación.** La de DIV es una cesta G10 contra EUR (D0 8.4). P5 dice que la referencia es «no hacer nada», es decir, el benchmark de la cartera. Un pronóstico «el par bate a la cesta G10» no responde a la decisión «entrar o quedarse en EUR».

### 2.2 Agentes: qué hace cada uno en tiempo de ejecución

Inventario de llamadas LLM del ejecutor (`grep _invocar`): AG-0x Analista (1 por tipo, más 1 de respuesta a objeciones), AG-10, AG-11, AG-12, AG-14 o AG-16 (como mucho 1 por tipo), AG-02, AG-18 (solo si G3 no es APTO), AG-17 (1–2), AG-19 y AG-20. En la simulación, un ciclo de 12 tipos en N2 hizo 50 llamadas.

| Agente | Prompt (≈ tokens) | Qué hace de verdad | ¿LLM necesario? | Propuesta |
|---|---|---|---|---|
| AG-01 Coordinador | 25 900 | Solo responde consultas N0 (`orquestacion.py` 1327) | Solo para N0 | Respondedor N0 de unos 3 000 tokens |
| AG-02 Analizador | 33 400 (Opus) | Narrativa de integración. «No cambies la selección» (1056–1059) | Sí, pero pequeño | Fusionar con AG-17 en un «Sintetizador» |
| 12 Analistas | 17 200–25 500 c/u | F1 y F2 en una llamada, más la respuesta a objeciones | Sí | Núcleo + perfil compuestos al cargar (PA-07) |
| AG-10 Prospectiva | 21 500 | Escenarios y `prob_interna` | Sí | Recortar; añadir la probabilidad del propio analista como segunda opinión (PA-03) |
| AG-11 Contrarias | 18 500 (Opus) | Objeciones por lotes | Sí | Otro proveedor y sin razonamiento (PA-05) |
| AG-12 Curador | 10 700 (Haiku) | Clasifica piezas; la deduplicación y las raíces son código (757–768) | Dudoso | Medir su efecto (PA-14) o integrarlo en el Analista |
| AG-13 Motor | 28 000 + MC 78 000 | No se invoca | No | Retirar como agente (SC-3) |
| AG-14, AG-15 y AG-16 | 19 700 / 14 400 / 17 300 | Como mucho 1 búsqueda por tipo; el C4 no existe | No en la Fase 1 | Congelar; el lector pasa a SC-11 y el posicionamiento a K |
| AG-17 Redactor | 19 800 | Textos llanos y reescritura por legibilidad | Parcial | Fusionado con AG-02; el informe al usuario pasa a N (PA-13) |
| AG-18 Orquestador | 19 400 | Dictamen ignorado por el código | No | Retirar |
| AG-19 Auditor | 16 400 | Hallazgos que nadie lee | No en la Fase 1 | PA-17 |
| AG-20 Evaluador | 21 200 (Opus) | Redacta un informe y como mucho 3 lecciones, rebajadas de fuerza (468–491) | No | Plantilla determinista; LLM pequeño como opción |

**¿Los 12 Analistas son perfiles de un núcleo?**

- **En el texto, sí:** las secciones comunes coinciden al 100 % con la plantilla y el esquema de salida es el mismo.
- **En la ejecución, no hay perfil efectivo:** `senales_clase` calcula las mismas 6 fichas (ACC-MOM, FX-VOL, FX-TREND, RISK-DD, ST-DESC, FIN-CAGR) para todos los tipos, incluida renta variable (`orquestacion.py` 231–232). La especialización se queda en el texto.
- **El perfil de verdad** sería:
  - el universo;
  - las fichas del Motor que alimentan al Analista;
  - los umbrales de GC1 y las anclas (como datos, no como prosa);
  - un texto breve de estrategia.

**Solapamientos:**

- AG-01 hace lo mismo que AG-18 y que el Orquestador global en colas y presupuestos.
- AG-02 y AG-17 hacen narrativa sobre el mismo paquete.
- AG-14 y AG-16 se solapan con SC-11 y K.
- AG-20 se solapa con SC-4, con I y con la certificación de rankings de B (T-68).

### 2.3 Calidad de los prompts

**Medidas.** Total de 593 000 tokens (25 agentes y 10 MC). Base de conocimientos (§10): 38–49 % en los Analistas y 44–74 % en los MC. Las secciones 1–5 de los Analistas repiten el D0.

**Contradicciones e instrucciones que no se pueden cumplir:**

1. **La subordinación está al revés.** El bloque del ejecutor dice que sus reglas son «adicionales a tu system prompt y subordinadas a él» (`prompts.py` 52–55). Cuando el prompt dice «lanza los CT-06 en paralelo», «ejecuta HT-09», «actualiza F1 y F3» (Analizador, pasos 1–7) o «calcula provisionales con HT-03», manda el prompt, y el modelo no puede hacer nada de eso.
2. **El Coordinador no puede cumplir su propia regla.** Su R7 dice «No calculas nada, ni siquiera una resta». Pero debe calcular la prioridad efectiva (§6.1), P50/P80 (§6.5), el factor de alcance (§6.3), la ley de Little y «las próximas cinco ejecuciones» de cron (§5.6).
3. **El Analizador da por buena una puntuación que el código no usa.** «Si discrepas… se usa la tuya» (Paso 3.1), pero el código usa las dimensiones del Analista y a AG-02 solo le pide integrar.
4. **El Analista de Divisas tiene una GC1 imposible.** Exige una familia «ancla» (CAR o VAL) y POS/BDP (prompt DIV §6.3), pero recibe momentum, tendencia y percentil de precio. Además, el mensaje trae otra GC1: `umbral_senal_gc1` 0,75 sobre una `senal_compuesta` distinta (`orquestacion.py` 263–272 y 547). Tiene dos reglas y datos para ninguna.
5. **Hay números escritos en los prompts** (contra §10.4):
   - umbral de clúster: ρ ≥ 0,6 en el Analizador (§6.15), > 0,7 en DIV (§6.3) y 0,7 en el código (`orquestacion.py` 843);
   - reparto del presupuesto: 30/35/15/10/10 en el Analizador (§7.3) frente a 35/20/15/20/10 en `por_defecto.yaml`;
   - umbrales de GC1, anclas de A y plantillas de invalidación con cifras en cada perfil.
6. **Contrarias** (§1) admite que «todos los agentes del bloque comparten modelo», pero el diseño no lo compensa. Prevé una contrarréplica (§5) que el ejecutor no implementa.
7. **Burocracia que no cambia decisiones.** Los campos `autoevaluacion`, `consultas_broker` y `solicitudes_credenciales` de cada retorno, y los extensos listados de contratos y archivos que el modelo no puede tocar, gastan tokens de entrada y salida sin que el código los use, salvo CT-23 y CT-25.

### 2.4 Flujo y coste

- **El embudo F0–F8 es nominal en F1–F2.** El ejecutor junta cribado e investigación en una sola llamada con todo el universo del tipo. GC1 no ahorra nada, porque lo aplica el LLM después de haberlo leído todo. Con 6 pares de divisas no importa. Con el universo real sí. La Const. §10 (economía, punto 2) pide filtros deterministas sobre K, después modelos pequeños y, solo para lo que sobreviva, modelos grandes.
- **GC2 y GC3 son código** (bien). Prospectiva y Contrarias van por lotes por tipo (bien).
- **N0–N3:** el presupuesto por nivel es plano por tipo. La regla de ampliación solo autoriza prospectiva, refutación y respuesta a objeciones (`orquestacion.py` 193), lo cual es razonable. N3 (50 UC) no incluye un segundo análisis independiente.
- **Coste fijo dominante.** Caché de 1 h con ciclo semanal: cada ciclo paga la escritura de todos los prompts (simulación: 309 000 tokens escritos, 534 000 leídos, 41 000 de salida). Recortar prompts es el ahorro mayor.
- **Lotes del proveedor.** El ciclo semanal y C5 no son urgentes y podrían ir por la API de lotes, como pide §10 (economía, punto 5). No está implementado (tarifa y soporte por verificar).
- **Reparaciones.** `salida_estructurada: false` obliga a reintentos que reenvían toda la conversación (`agentes.py`, bucle de reparación).
- **Modelos.** Opus para AG-02 (narrativa) y AG-20 (redacción) no se justifica. Para AG-11 sí, y mejor aún de otro proveedor.
- **El UC no se puede convertir a euros**: los precios están a `null`. Sin euros no se aplica §11 ni se mide P17.

### 2.5 Calidad de las decisiones

- **Verificabilidad: buena.** Pronóstico binario sobre el símbolo frente a una referencia, en un horizonte fijo, resuelto por código (`evaluador.py` 135–202).
- **La muestra está inflada.** El bootstrap usa bloques de tamaño n^(1/3) en el orden de `prg_id`, no por fecha ni por símbolo (`motor/evaluacion.py` 81–101). El `n_eff` que pide el prompt del Evaluador (§6.4) no está implementado. En la Fase 1, 6 pares contra EUR dominados por el dólar dan muchos PRG y pocas observaciones independientes: un certificado con n ≥ 100 puede llegar con una muestra efectiva muy pequeña.
- **Los agentes eligen sus preguntas.** Solo se pronostica sobre las finalistas que propone el agente, y las vistas «lateral» se descartan (`orquestacion.py` 890). Va contra D-37 («preguntas que el agente no elige») y sesga la calibración.
- **Contaminación.** `backtest.anonimizar: false` por defecto (`por_defecto.yaml`). La anonimización es parcial, como admite la propia docstring de `anonimizacion.py`. Nada impide que un backtest con LLM anterior a la fecha de corte del modelo alimente F6 o los certificados. Va contra T-58 (23) y la escalera de §9.
- **Refutación débil:**
  - mismo proveedor;
  - el refutador recibe tesis, mecanismo, pre-mortem y dimensiones (`orquestacion.py` 704–707), contra §3.2, que pide «evidencia pero no razonamiento»;
  - quien declara «resuelta» una objeción fuerte es el Analista acusado (741–743);
  - `veredicto_global` no se usa (solo aparece en `contratos.py` 340–341), así que «tesis refutada» o «tesis frágil» no tienen efecto, contra el prompt del Analizador §6.10.
- **Sobreconfianza.** `prob_interna` la escribe un LLM. Hay una lección determinista que limita a 0,60 y bandas publicadas (bien). Pero no se mide a cada agente por separado: no hay base para D-36 (peso por historial).
- **Sin referencia simple con la que compararse.** Nadie comprueba que la cadena LLM bata a un cribado cuantitativo trivial (por ejemplo, el top-3 por señal compuesta). La Const. lo exige en espíritu (P17, P19, §9.15 aspirante y titular, §9.17 «referencias simples»).

---

## 3. Propuestas priorizadas

Leyenda: **[OP]** decide el operador (cambio de diseño, de tipo 3 o enmienda). **[TEC]** mejora técnica. Fase del sistema según §14.

### Urgentes (antes de conectar A en la Fase 1)

**PA-01 · A en la Fase 1 = núcleo + perfil `DIV` activo; el resto de perfiles `NO_CONSTRUIDO`** [OP] · Fase 1
- **Qué cambiar.** Añadir a A el estado de perfil `ACTIVO` / `NO_CONSTRUIDO` (D-17). Un perfil no construido devuelve `NO_ESTIMABLE` y el Broker no lo encarga. Valor por defecto de «tipos activos»: solo DIV, no los doce (Anexo A, F10 P-02).
- **Por qué.** La Fase 1 es solo de divisas (§14, D-09). Hoy hay 14 fichas implementadas de 81 (README del ejecutor, §9.3). Los otros 11 perfiles no tienen datos propios (2.2) y cuestan unos 220 000 tokens de prompt por ciclo.
- **Beneficio.** Reduce un ciclo de 12 tipos a uno, con coste y superficie de pruebas a la medida de la fase.
- **Coste y riesgo.** Bajo: es un parámetro y una comprobación. Riesgo nulo, porque los perfiles se reactivan.
- **Pregunta para el cuestionario:** «¿En qué tipos de inversión quieres que el robot busque oportunidades? (Recomendado ahora: solo divisas)».

**PA-02 · Adaptador A → CT-G, ficha CT-G-17, batería de conformidad y hueco del catálogo** [OP enmienda, TEC adaptador] · Fase 1
- **Qué cambiar:**
  - Proponer en §15 una enmienda con dos contratos: «encargo de descubrimiento (Orquestador → A)» y «paquete de oportunidades (A → Orquestador → B)». Como alternativa, declarar que el CT-B-01 de B sigue siendo la entrada de B.
  - Escribir el adaptador: CT-01/02/03/04/23/24/25 de A ↔ CT-G-11/12 y el sobre (`event_id`, `correlation_id`, `valid_until`, `data_refs`, `resultado_politica`).
  - Definir la correspondencia OPP- → expediente `DETECTADA`.
  - Escribir la ficha CT-G-17 y la batería de conformidad (casos válidos e inválidos).
  - Renombrar los contratos internos a `CT-A-nn` para evitar colisiones con CT-B y CT-G.
- **Por qué.** Lo exigen §5 (enchufabilidad, puntos 1, 2 y 4), §14 (regla 5) y D-41. Hoy el catálogo no tiene dónde encajar a A.
- **Beneficio.** Permite conectar A sin tocar su interior, y sustituirlo después.
- **Coste y riesgo.** Medio: el adaptador, los esquemas y unos 20–40 casos. Riesgo de congelar demasiado pronto: usar esquemas 0.x.
- **Decisión del operador:** si toda OPP del top-3 abre expediente o solo las que el Broker envía a B. Recomendado: solo las enviadas; las demás quedan en SC-4 como descartadas con su reapertura (§4.1, regla 5).

**PA-03 · Pronósticos de A en SC-4, con torneo de preguntas fijas y muestra efectiva** [TEC; OP el alcance del torneo] · Fase 1
- **Qué cambiar:**
  - Publicar F4 en SC-4.
  - En cada ciclo, hacer las mismas preguntas para todo el universo activo: cada par × H1/H2/H3, «¿bate a la referencia?». Las responden el Analista, Prospectiva, una referencia determinista (señal compuesta) y la tasa base.
  - Atribuir cada probabilidad a su agente.
  - Bajar los hitos H5 a 12 meses o menos.
  - Calcular `n_eff` y un bootstrap por conglomerados de fecha.
  - No certificar con n nominal.
- **Por qué:**
  - D-35/36/37 y §9.13–14: torneo, peso por historial y preguntas que el agente no elige;
  - §9.2 y §9.10: horizontes de 12 meses o menos;
  - el sesgo de selección (lateral descartado) y la correlación entre pares (2.5).
- **Beneficio.** Muestra útil en semanas, no en años. Calibración por agente: base de D-36 y de PA-06. Certificados creíbles.
- **Coste y riesgo.** Bajo en divisas: unas 18 preguntas por semana, en una llamada por agente. Riesgo: la prueba de calibración será más exigente y los certificados tardarán más, que es lo correcto.

**PA-04 · Datos desde K, fichas FX completas y perfil DIV alimentado** [TEC] · Fase 1
- **Qué cambiar:**
  - Que HT-01 pase a ser un adaptador sobre K (sello de corte, calendario, COT).
  - Que GC0 lea los eventos de K y SC-11 en lugar de `gc0.eventos_calendario: []`.
  - Programar las 6 fichas FX que faltan (BEER, BRK, COINT, PPA, REGIME, STL).
  - Que `senales_clase` use las fichas del perfil (CAR, VAL, MOM, POS, VOL) en lugar de 6 genéricas.
  - Expresar la GC1 de DIV como regla en configuración, aplicada por código antes del LLM.
- **Por qué.** K es el único que emite el sello de corte (§2, D-18). La Const. pide que A tenga las 6 fichas en la Fase 1 (§14). Hoy la GC1 de DIV no se puede cumplir (2.3, punto 4). Embudo de la Const. (§10).
- **Beneficio.** El Analista recibe solo las candidatas que pasan GC1 y con sus señales. Menos entrada y una especialización real.
- **Coste y riesgo.** Medio: las fichas, sus pruebas y el adaptador. Riesgo de que los datos de carry y PPA no estén en K mínimo: declarar `NO_ESTIMABLE` y degradar PS2.

**PA-05 · Contradictor de verdad** [OP proveedor y coste; TEC lo demás] · Fase 1
- **Qué cambiar:**
  - AG-11 de otro proveedor, con un puerto SC-10 de modelos de IA (`LLMClient` ya lo permite).
  - Que reciba evidencia (CLM, EVD, CALC) sin tesis, mecanismo, pre-mortem ni dimensiones del Analista.
  - Que quien juzgue si una objeción fuerte queda resuelta sea una regla (evidencia nueva citada y verificable) o el propio Contradictor en una contrarréplica, nunca el Analista.
  - Que el veredicto lo calcule una regla a partir de las objeciones, como en CT-G-03, y que tenga efecto: «refutada» descarta; «frágil» da confianza «especulativo» y relevancia ALTA.
  - Puntuar al Contradictor por las objeciones que después se confirman (D-37).
- **Por qué.** §3 (verificación diversa, punto 2), D-43, D-37 y las evidencias de 2.5. El documento de diseño CT-G-03 del marco ya resuelve el veredicto por regla.
- **Beneficio.** El único control de calidad interpretativo de A deja de ser decorativo.
- **Coste y riesgo.** Una clave y un presupuesto de un segundo proveedor (decisión del operador). Riesgo de formatos distintos entre proveedores, que el esquema y la batería absorben.
- **Pregunta para el cuestionario:** «¿Aceptas un pequeño coste adicional para que un modelo de otra empresa revise las ideas? (Recomendado: sí)».

**PA-06 · Retirar o convertir en código los agentes sin carga decisoria (de 25 a unos 6 papeles LLM)** [OP, tipo 3 de topología] · Fase 1
- **Qué cambiar:**
  - Retirar como LLM: AG-13 (sus MC pasan a documentación de SC-3), AG-15, AG-18 y AG-20 (informe con plantilla).
  - AG-01 se queda como respondedor N0 mínimo.
  - AG-02 y AG-17 se fusionan en un Sintetizador (Sonnet).
  - AG-14 y AG-16 se congelan en la Fase 1 (lector SC-11; posicionamiento en K).
  - AG-12 se mantiene si PA-14 demuestra que aporta.
  - Actualizar el D0 para que describa lo que se ejecuta.
- **Por qué.** El inventario de 2.2. P14 (mínimo primero), D-25 (cada pieza justifica lo que aporta), D-19 (tope de complejidad). El D0 ya retiró antes el «Flujo de Investigación» por el mismo motivo (§4.2).
- **Beneficio.** Un D0 que coincide con el código, menos superficie que auditar y menos coste fijo.
- **Coste y riesgo.** Documental, sobre todo. Riesgo de perder funciones previstas para fases futuras: se conservan como «retirado, recuperable» en `99_Historico`.

**PA-07 · Prompts: composición núcleo + perfil, recorte, parámetros fuera y subordinación correcta** [TEC; validación con aspirante y titular] · Fase 1
- **Qué cambiar:**
  - `prompts.py` compone al cargar la plantilla común (unos 3 000–4 000 tokens) y el perfil (`perfiles/DIV.md`, estrategia breve de unos 3 000–4 000 tokens).
  - Fuera del prompt: la base de conocimientos de manual y los procedimientos que ejecuta el código.
  - Pasar umbrales, anclas y plantillas numéricas a la configuración del perfil (§10.4).
  - Invertir la cláusula de `BLOQUE_EJECUTOR`: la interfaz del ejecutor prevalece.
  - Validar cada recorte como aspirante frente al prompt actual con un conjunto dorado grabado con `ReplayClient` (D-36, D-40).
- **Por qué.** Lo exponen 2.3 y 2.4. La propia Const. pide caché e instrucciones cortas (§10, economía, punto 5).
- **Beneficio estimado.** En la Fase 1, el prompt fijo por ciclo pasa de unos 180 000 a unos 25 000–30 000 tokens (−80/85 %), con menos contradicciones y menos riesgo de deriva entre 12 copias.
- **Coste y riesgo.** Medio. Riesgo de bajar la calidad: lo controla la comparación entre aspirante y titular. No se recorta nada que pierda.

**PA-08 · Presupuesto en euros, tope por encargo y día, y coste de análisis informado** [TEC; OP el valor] · Fase 1 (antes del modo sombra con API)
- **Qué cambiar.** Rellenar los precios por modelo. Fijar topes en euros por encargo y día que lleguen del Orquestador global (P-07). Que el estado `INCOMPLETO` se declare al agotarse el presupuesto (§11). Informar del coste por ciclo a SC-5 y a I (P17).
- **Por qué.** El UC no se puede convertir y el coste sale vacío (`por_defecto.yaml`, `precios_por_millon`).
- **Beneficio.** Se aplica el §11 y la cartera sombra compara después de los costes de IA.
- **Coste y riesgo.** Bajo.
- **Valor por defecto prudente:** un tope semanal bajo, en simulado.
- **Pregunta para el cuestionario:** «¿Cuánto quieres gastar como máximo cada semana en la IA que busca oportunidades?».

**PA-09 · Contaminación por conocimiento del modelo: regla de admisibilidad** [TEC] · Fase 1
- **Qué cambiar:**
  - `anonimizar: true` por defecto en backtest.
  - Etiquetar `contaminacion_posible` todo PRG de backtest con LLM anterior a la fecha de corte del modelo.
  - Que esos PRG no cuenten para certificados, recalibraciones, lecciones ni pesos.
  - Que solo cuente lo hecho hacia delante después de la fecha de corte, o el modo sombra en vivo.
- **Por qué.** T-58 (23), la escalera de §9 y los límites declarados en `anonimizacion.py`.
- **Beneficio.** Evita aprender de un «acierto» que es memoria del modelo.
- **Coste y riesgo.** Bajo. Riesgo: menos muestra disponible, que es lo honesto.

**PA-10 · Aprendizaje gobernado: solo endurecer por cuenta propia** [OP] · Fase 1
- **Qué cambiar.** El Evaluador puede aplicar por sí solo únicamente ajustes que endurecen: subir umbrales, bajar un horizonte de «Sí» a «Limitado», degradar H5, revocar certificados. Todo lo que relaja (pesos de RK, bajar umbrales, «Limitado» → «Sí», emitir certificados que habilitan probabilidades numéricas) va por la ruta única (§9.6). El modo sombra sigue siendo el valor por defecto.
- **Por qué.** P8 y §9.6, frente a D0 §12.2 y §18.1. Sigue el mismo patrón que el vigía de régimen, que «solo endurece» (§3).
- **Beneficio.** Conformidad con la Const. sin perder la autocorrección prudente.
- **Coste y riesgo.** Bajo. Riesgo: más carga para el operador si se acumulan propuestas, que se mitiga agrupándolas en una revisión trimestral.

**PA-11 · Valores por defecto con justificación y pregunta; parámetros del usuario en SC-1** [OP y TEC] · Fase 1
- **Qué cambiar:**
  - Añadir al Anexo A dos columnas: «justificación del valor por defecto» y «pregunta del cuestionario o "técnico, sin pregunta"».
  - Mover a SC-1 lo que depende del usuario: invertibilidad (minorista europeo sin apalancamiento, coherente con D-16), horizontes de interés (atados a P-04), tipos activos, periodicidad e idioma.
  - Los umbrales de E, A y T, los pesos de RK y las muestras de calibración son técnicos: quedan con valor y justificación, y se unifican con P-14 y P-32 globales en lugar de 30/100 propios de A.
- **Por qué.** D-44, D-45 y D-47 (cada copia guarda su perfil fuera del repositorio).
- **Beneficio.** Una copia nueva funciona desde el primer día, y A deja de tener una «configuración de usuario» propia.
- **Coste y riesgo.** Bajo y documental, más el traslado de 4–5 campos.

**PA-12 · Referencia de comparación coherente con P5** [OP] · Fase 1
- **Qué cambiar.** El pronóstico principal de cada opción se mide frente al benchmark de la cartera de destino (en divisas para un inversor en EUR, por defecto la liquidez en EUR con €STR, es decir, «no exponerse»). La cesta G10 queda como referencia secundaria y descriptiva.
- **Por qué.** P5, §7, y que el acierto de A debe responder a la decisión real.
- **Beneficio.** Un historial de aciertos que el Broker y D pueden usar tal cual.
- **Coste y riesgo.** Bajo: es configuración. Riesgo: rompe la comparabilidad con el historial simulado anterior, que en cualquier caso no vale como evidencia (PA-09).

### Pueden esperar

**PA-13 · A deja de producir el informe visual para el usuario** [OP] · Fase 1 si se quiere ahorrar ya; si no, Fase 2
- **Qué cambiar.** A entrega el JSON y un informe técnico breve. El lenguaje llano y el informe visual (semáforo, tarjetas, legibilidad, HT-04, HT-07) pasan a N y al Broker conversacional.
- **Por qué.** §2: N es la única superficie que ve el operador y el Broker es quien explica.
- **Beneficio.** Una llamada menos por ciclo y desaparece la reescritura por legibilidad.
- **Coste y riesgo.** N mínimo debe asumirlo. Riesgo de un vacío temporal de presentación.

**PA-14 · Ablación determinista por agente (presupuesto de complejidad)** [TEC] · Fase 1–2
- **Qué cambiar.** Como la selección es código, recalcular en cada ciclo el top-3 sin las objeciones de AG-11, sin la clasificación de AG-12 y sin la integración, y registrar cuántas decisiones cambia cada pieza.
- **Por qué.** D-25 y §9.11. Hoy nada mide qué aporta cada agente.
- **Beneficio.** Datos para retirar o mantener piezas, a coste cero en tokens.
- **Coste y riesgo.** Bajo.

**PA-15 · Una sola evaluación común (SC-4 y I)** [TEC] · Fase 1–2
- **Qué cambiar.** Unificar `evaluador.py` y `motor/evaluacion.py` de A, la certificación de rankings de B (T-68) y el diario del marco en un servicio común.
- **Por qué.** P12 (especializar sin duplicar) y §9 (I completo al final, SC-4 desde la Fase 1).
- **Beneficio.** Un único criterio de certificado para todo el sistema.
- **Coste y riesgo.** Medio, con riesgo de migración. Se hace con estado separado por bloque (§5, enchufabilidad, punto 3).

**PA-16 · Extraer el Motor de A como SC-3** [TEC] · Fase 1–2
- **Qué cambiar.** Llevar a un paquete propio `motor/`, el catálogo y la caché por hash, con su Documento 0 y contratos CT-09 y CT-10. A los consume.
- **Por qué.** D-29 y §3: SC-3 «parte del Motor de A».
- **Coste y riesgo.** Medio. Mantener `CATALOG_VERSION` y las pruebas.

**PA-17 · Auditor con muestreo, de otro proveedor y con el lazo cerrado** [OP proveedor] · Fase 2
- **Qué cambiar.** Muestreo por riesgo en lugar del 100 % de los ciclos periódicos, revisor de otro proveedor (§14, regla 5) y hallazgos que generen tareas o propuestas para I y J.
- **Por qué.** Hoy los hallazgos van a HA y no tienen efecto (`orquestacion.py` 1272–1282).

**PA-18 · Radar tecnológico** [OP] · Fase 2, con C-RV
- **Qué cambiar.** Decidir si el radar es un perfil transversal de A o una función de F1 con un registro común de tendencias tecnológicas y pronósticos con hitos de 12 meses o menos en SC-4.
- **Por qué.** Está en la fila de A (§2), en §3 y en §9.10. No existe en el D0. En la Fase 1 no tiene demanda (P14).

**PA-19 · Lotes y salida estructurada** [TEC] · Fase 1 (modo sombra)
- **Qué cambiar.** Enviar el ciclo periódico y C5 por la API de lotes del proveedor, y activar la salida con esquema si el modelo la admite, para eliminar las reparaciones. Verificar tarifas y soporte vigentes.
- **Por qué.** §10 (economía, punto 5).

**PA-20 · Compartir el análisis de A entre copias** [OP] · Fase 2+
- **Qué cambiar.** A apenas depende del usuario si se aplica PA-11, así que una ejecución podría servir a varias copias y abaratar costes.
- **Por qué no ahora.** Correlaciona los errores de las copias (§12.11). Por defecto no se comparte. Debe ser una opción voluntaria.

**PA-21 · Que el Analista dé también su propia probabilidad** [TEC] · Fase 1, con PA-03
- **Qué cambiar.** Registrar la probabilidad del Analista además de la de Prospectiva y comparar las dos en el torneo.
- **Por qué.** Hoy solo se calibra a AG-10, y el anclaje del Analista en su tesis no se mide. Es una condición para dar peso por historial (D-36).

## 4. Preguntas para el cuestionario del operador (valor por defecto prudente primero)

1. **Tipos de activo en los que buscar:** solo divisas (recomendado en la Fase 1) · divisas y monetario · todos · «dímelo con tus palabras». (PA-01)
2. **Gasto máximo semanal en IA para buscar oportunidades:** bajo, en simulado (recomendado) · medio · sin tope (no recomendado). (PA-08)
3. **Revisión de ideas por un modelo de otra empresa:** sí, con un pequeño coste adicional (recomendado) · no. (PA-05)
4. **Cuándo se abre un expediente:** solo cuando el Broker envía la idea a B (recomendado) · con cada opción del top-3. (PA-02)
5. **Con qué se compara el acierto:** con no hacer nada, el benchmark de la cartera (recomendado) · con un índice de su tipo. (PA-12)
6. **Ajustes automáticos:** solo los que hacen al sistema más prudente (recomendado) · también los que lo relajan, dentro de límites. (PA-10)
7. **Informe para el usuario:** lo presentan el Broker y la consola (recomendado) · también un informe visual de A. (PA-13)

## 5. Orden de ejecución sugerido

PA-01 → PA-11 y PA-12 (sesión T-57) → PA-06 y PA-07 (cambio documental y de prompts, validado como aspirante) → PA-04 → PA-03, PA-21 y PA-09 → PA-05 → PA-02 → PA-08 y PA-19 (antes del modo sombra con API) → PA-10. Durante la Fase 1: PA-14, PA-15 y PA-16. En la Fase 2: PA-13, PA-17, PA-18 y PA-20.

## 6. Límites de esta revisión

- Del D0 se leyeron: 3–4.5, 7–12, Anexo A, 17–18 y Anexo G.
- Se leyeron completos, en lo operativo, estos prompts: Marco común, Divisas, Coordinador, Analizador (secciones 1–9), Contrarias (1–9) y Evaluador (1–9). Del resto, solo títulos y medidas.
- Del ejecutor se leyeron `orquestacion.py`, `agentes.py`, `llm.py`, `consumo.py`, `prompts.py` y `anonimizacion.py`, y por búsqueda `evaluador.py`, `motor/evaluacion.py`, `seguimiento.py` y la configuración.
- No se ejecutó ninguna prueba. Las cifras de coste salen de la simulación del README del ejecutor y del tamaño de los prompts.
