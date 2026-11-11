# Bloque C: el análisis en profundidad (propuesta de diseño de Claude)

De: Claude, 11-11-2026. Estado: **PROPUESTA PARA DISCUTIR**. No hay nada que implementar: el operador está decidiendo la arquitectura de los bloques antes de construir (relevo de Astra, §0 bis). Copia en el repositorio del documento que el operador revisó con Claude. Sigue la misma pauta que los rediseños de A y B (`.docs/diseno/bloque_a/`, `.docs/diseno/bloque_b/`).

Encargo del operador: «Ahora sí que quiero que propongas un diseño del bloque C».

## 1. Respuesta corta

C estudia a fondo un candidato concreto de un tipo de activo y entrega un sobre comparable (CT-G-02): tesis, clase de referencia, condiciones de invalidez, escenarios, estrés, factores, costes y una probabilidad con plazo y criterio de resolución. Se propone construirlo desde cero con la pauta de A y B:

- **Un solo analista para los doce tipos de activo**, con un kit por perfil (C-DIV, C-RV, C-FON…) cargado como datos. Añadir un perfil es escribir su kit.
- **Cuatro papeles de IA:** Lector de evidencia aislado, Analista, Analistas independientes (el mismo papel con otro modelo, solo cuando el importe lo justifica) y Contradictor de otro proveedor.
- **Todo lo demás es código:** coordinación (Orquestador), cifras (Motor), validación (SC-6) y combinación de análisis independientes (regla con pesos por historial).
- **Primero la vista exterior:** cada análisis empieza por qué suele pasar en casos parecidos; con datos, la tasa base la calcula el Motor.

**N0 no gasta tokens, N1 hace una llamada, N2 dos o tres y N3 como mucho cinco.**

## 2. Qué hace ganar o perder rentabilidad por euro

| Fallo | Por qué cuesta | Respuesta en el diseño |
| --- | --- | --- |
| **Mirar solo el caso** | Exceso de confianza por una buena historia | Clase de referencia y tasa base primero; el Contradictor la revisa |
| **Cifras inventadas** | Números plausibles sin calcular | Toda cifra del Motor por identificador (P3); si no, `NO_ESTIMABLE` (P16) |
| **Saber el pasado** | El modelo conoce lo ocurrido hasta su fecha de corte | Datos con fecha de publicación (K); pruebas solo con casos anonimizados o posteriores |
| **Errores en bloque** | Agentes del mismo modelo se equivocan a la vez (§3) | Contradictor de otro proveedor; en N3, análisis de modelos distintos |
| **Tesis no comprobables** | No se sabe si el analista acierta | Probabilidad, plazo y criterio, congelados en SC-4, medidos con Brier |
| **Analizar más caro de lo que vale** | El análisis se come la rentabilidad (P18) | Niveles N0 a N3 por importe e incertidumbre; tope del 1 % (§10) |
| **Repetir lo analizado** | Pagar dos veces lo mismo | Registro de análisis vigentes; actualizar solo lo afectado |

## 3. Qué hay hoy y qué falta

Existe, en el marco común (V0.01 a V0.73): encargo CT-G-01 con validador; sobre CT-G-02 por capas con validador (clases Q, S, K y `NO_ESTIMABLE`); informe del Contradictor CT-G-03 con validador; partes del Motor (SC-3) y de K; el Orquestador con expediente, vía directa y modo consulta.

Falta el propio analista: ningún perfil está construido (C-DIV, parcial en otro modelo, sin compartir: D-02). Faltan los kits, el ciclo de un encargo dentro de C, la combinación de análisis independientes, el registro de análisis vigentes (SC-5, T-87) y la calibración por autor en SC-4 (T-81), ambos en espera.

## 4. La arquitectura

| Papel | Qué hace | Qué recibe | Modelo propuesto |
| --- | --- | --- | --- |
| **Lector de evidencia** | Lee documentos aislado; datos con fuente, fecha y etiqueta, esquema cerrado | Documentos, sin cartera ni herramientas | Haiku |
| **Analista** | Clase de referencia, por qué el caso se aparta, supuestos, invalidez medible, escenarios, probabilidad con plazo y criterio | Encargo, paquete de B, cifras del Motor, evidencia y kit del perfil | Haiku o Sonnet en N1; Sonnet en N2; Opus en N3 |
| **Analistas independientes** | El mismo papel con otro modelo, sin ver el primero | Lo mismo | Otro modelo o proveedor; solo N3 |
| **Contradictor** | Escenarios en que la tesis falla; revisa la clase de referencia | Evidencia y cifras, no el razonamiento | Otro proveedor si es posible (§3) |

**Código:** el Orquestador recibe el encargo, elige el nivel y llama a cada papel; el registro de análisis vigentes decide si basta con N0; K da los datos con sello de corte; el Motor calcula estrés, factores, costes, liquidez, escenarios con método y, en clase Q, la tasa base; SC-6 valida (una vuelta al Analista, después escala); la combinación de N3 es una media ponderada por historial, encogida hacia pesos iguales con poca muestra, con rebaja del tope de confianza si discrepan (§3, §9); una objeción fuerte solo queda resuelta si la respuesta cita evidencia verificable (como en A, T-66).

**Kit de cada perfil** (texto y datos): qué mueve el tipo de activo; clases de referencia y dónde están los datos de su tasa base; métricas y módulos del Motor; plantillas de invalidez; clase de comparabilidad (la ratifica el operador); cuerpo especializado del sobre. El prompt del Analista es un núcleo común corto (método, reglas del sobre, prohibición de inventar cifras) seguido del kit; el núcleo es igual para todos y aprovecha la caché.

**Un N2:** encargo → Orquestador (N0 si hay sobre vigente) → K y Motor → Lector (si hay documentos) → Analista → SC-6 → Contradictor → regla de objeciones y confianza → sobre a D y al Broker, tesis congelada en SC-4. En N1 no hay Contradictor; en N3 se añaden uno o dos Analistas independientes y la combinación por regla antes del Contradictor.

## 5. Niveles y carteras

| Nivel | Cuándo | Qué se hace | Llamadas de IA |
| --- | --- | --- | --- |
| N0 | Sobre vigente con los mismos datos | Reutilizar; el Motor recalcula lo menor | 0 |
| N1 | Importe pequeño o primera criba | Analista con modelo pequeño, sin Contradictor | 1 (2 con Lector) |
| N2 | Antes de invertir | Analista y Contradictor | 2 o 3 |
| N3 | Importes grandes o mucha incertidumbre | 2 o 3 Analistas independientes combinados, y Contradictor | 4 o 5 |

|  | Trading | Táctica | Largo plazo |
| --- | --- | --- | --- |
| **Papel de C** | Bajo: casi todo por la vía sistemática (J, §7) | Central: tesis con catalizador y fecha | Alto pero poco frecuente: asignación y vehículo |
| **Nivel habitual** | N0 o N1 | N1 para cribar, N2 para invertir | N2; N3 en asignaciones grandes |
| **Lo que más importa** | No contradecir a la estrategia | Probabilidad y fecha del catalizador, invalidez clara | Costes, fiscalidad, diversificación, tasa base de largo plazo |
| **Cuánto es código** | Casi todo | La mitad aproximadamente | Casi todo en fondos e índices (comisiones, diferencia con el índice, réplica, domicilio, traspasable) |

## 6. Precisión

Calibración (lo dicho al 70 % ocurre unas siete de cada diez veces) y rentabilidad neta frente al plan pasivo. Cada tesis comprobable y congelada; sub-pronósticos de 12 meses o menos; torneo de pronósticos para tener muestra antes; calibración por perfil, nivel y modelo, que D usa para encoger hacia la tasa base y N3 para pesar; el Contradictor se mide por objeciones confirmadas (D-37); kits y prompts compiten como aspirante frente a titular (D-36); las pruebas solo valen con casos anonimizados o posteriores a la fecha de corte del modelo. Mientras haya poca muestra, mandan los topes de confianza por clase.

## 7. Consumo y orden de construcción

| Nivel | Llamadas | Entrada estimada | Coste orientativo |
| --- | --- | --- | --- |
| N0 | 0 | 0 | Nada |
| N1 | 1 o 2 | 20.000–35.000 | Céntimos |
| N2 | 2 o 3 | 40.000–70.000 | 0,2 a 0,5 $ |
| N3 | 4 o 5 | 100.000–160.000 | 1 a 2 $ con Opus |

Muy por debajo del tope del 1 % del importe: el límite real es la atención del modelo, no el dinero.

Orden: (1) esqueleto y C-DIV en la Fase 1 (si se comparte el C-DIV del otro modelo, como fuente del kit); (2) C-IDX y C-FON, casi todo código y necesarios para el largo plazo; (3) C-RV, para congelar CT-G-02 en 1.0.0 (§5); (4) el resto, cuando una cartera lo necesite (§2).

## 8. Fronteras

| Quién | Relación con C |
| --- | --- |
| **B** | Pasa el paquete del candidato; C no repite lo que B ya contrastó (el paquete debe decir qué cubrió y con qué evidencia) |
| **K** | Única fuente de datos; un dato dudoso detiene el análisis |
| **Motor (SC-3)** | Toda cifra, citada por identificador |
| **SC-6** | Valida cada sobre |
| **SC-4** | Congela tesis y da la calibración |
| **D** | Usa sobre y calibración para encoger hacia la tasa base |
| **H** | Vigila invalidez y escenarios del Contradictor |
| **Broker** | Encarga (vía directa o modo consulta) y explica |

## 9. Preguntas para el operador

1. Un solo Analista con kit por perfil y cuatro papeles de IA.
2. Segundo proveedor de IA para Contradictor y análisis independientes (misma pregunta que en A y B).
3. Orden de perfiles: C-DIV, C-IDX y C-FON, después C-RV.
4. ¿Compartir el C-DIV del otro modelo (D-02) o empezar de cero?
5. Opus solo para los Analistas de N3.
6. Tasa base por código en clase Q: series históricas con fecha de publicación en K, dentro de la Fase 1.
