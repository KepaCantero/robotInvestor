# T-187 · Informe de PB-51: conocimiento específico en los system prompts del Bloque A

Generado por `.docs/scripts/revision_prompts_pb51.py` (sin red, determinista). No editar a mano: se regenera.

| Entrada | Ruta |
| --- | --- |
| Documento 0 (Anexo G) | `bloque_a/01_Gobernanza/Documento 0 - Protocolo maestro del Bloque A - Versión óptima V5.3.md` |
| Prompts | `bloque_a/02_System_prompts` |
| Configuración (topes) | `bloque_a/11_Ejecutor/config/por_defecto.yaml` |
| Huella de los prompts (SHA-256 de nombres y contenidos) | `44cb270b4dbe2498` |
| Semilla de la muestra | «T-187 · PB-51» |

## Resumen

| Comprobación | Resultado | Criterio |
| --- | --- | --- |
| Paso 1 · estructura del Anexo G (12 secciones) | 35 de 35 prompts (100.0 %) | 100 % (PB-51) |
| Paso 1 · títulos que no comparten palabra con el del Anexo G | 12 títulos | se informa, no suspende (INC-T187-01) |
| Plantillas (fuera del denominador) | 1: Marco común de los Analistas de tipo de activo (plantilla) - V5.0.md con 10 secciones, faltan [6, 10] | por diseño (su «Uso») |
| Paso 2 · prompts con sección 10 partida en subáreas | 35 de 35 | organizada por áreas (PB-51) |
| Prompts sin subárea de referencias canónicas en la sección 10 | 8: Auditor, Buscador de Fuentes Avanzadas, Coordinador de Peticiones y Consultas, Curador de Evidencia, Documentador para el Motor de Cálculo Avanzado, Evaluador de Previsiones y Aprendizaje, Orquestador técnico, Redactor y Diseñador de Informes | referencias (autor, año, título) en la sección 10 (PB-51) |
| Referencias canónicas con autor y año reconocibles | 656 de 674 entradas (97.3 %) | autor, año y título (PB-51) |
| … y con título en la propia entrada | 448 de 674 (66.5 %) | estricto |
| … y con título en el prompt (otra cita del mismo autor y año) | 465 de 674 (69.0 %) | amplio `[PROPUESTO]` |
| DOI escritos en los prompts | 0 (0 con estructura inválida) | sin DOI inventados; la existencia no se comprueba (sin red) |
| Tamaños con orientación escrita | 14 de 14 dentro del tope; 21 prompts sin orientación | `v6.tope_tokens_system` (INC-T187-01) |
| Paso 3 · afirmaciones en la muestra | 350 (10 por prompt; 0 prompts con menos candidatas) | ≥ 95 % correctas: lo juzgan revisores independientes |
| Paso 3 · afirmaciones correctas | 260 de 269 verificables (**96.7 %**; 9 ERRONEA, 81 NO_VERIFICABLE; 74.3 % sobre las 350): **supera** | ≥ 95 % sobre las verificables (PB-51; denominador de INC-T187-02) |

## Paso 1 · Estructura del Anexo G

Anexo G del Documento 0: 1. Identidad y misión (quién eres, para qué existes, qué no eres) · 2. Posición en el bloque (con quién hablas, por qué contratos, qué archivos lees y escribes) · 3. Reglas críticas que te aplican (extracto de R1–R27) · 4. Entradas y salidas (campos y formatos) · 5. Procedimiento operativo paso a paso · 6. Metodología y criterios de decisión propios · 7. Eficiencia: presupuesto, reutilización y reglas de parada · 8. Autocrítica y control de calidad · 9. Aprendizaje: cómo usas F6 y qué aportas · 10. Base de conocimientos (precisa, exhaustiva y específica de tu dominio) · 11. Formatos de salida y ejemplo breve · 12. Límites, seguridad y modos degradados.

| Prompt | Agente | Secciones | Faltan | Sobran | Repetidas | En orden | Completa | Títulos que no coinciden |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Marco común de los Analistas de tipo de activo (plantilla) - V5.0.md (plantilla) | — | 10 | [6, 10] | — | — | sí | no | — |
| Analista Inmobiliario y de Infraestructuras | AG-07 | 12 | — | — | — | sí | sí | 6 «Estrategia de análisis del tipo de activo» |
| Analista de Alternativos y Mercados Privados | AG-09 | 12 | — | — | — | sí | sí | 6 «Estrategia de análisis del tipo de activo» |
| Analista de Criptoactivos y Activos Digitales | AG-08 | 12 | — | — | — | sí | sí | 6 «Estrategia de análisis del tipo de activo» |
| Analista de Derivados Financieros | AG-23 | 12 | — | — | — | sí | sí | 6 «Estrategia de análisis de los derivados financieros» |
| Analista de Divisas | AG-05 | 12 | — | — | — | sí | sí | 6 «Estrategia de análisis del tipo de activo» |
| Analista de Fondos y Vehículos de Inversión Colectiva | AG-22 | 12 | — | — | — | sí | sí | 6 «Estrategia de análisis de los fondos y vehículos de inversión colectiva» |
| Analista de Instrumentos Monetarios y Liquidez | AG-24 | 12 | — | — | — | sí | sí | 6 «Estrategia de análisis de los instrumentos monetarios y de la liquidez» |
| Analista de Materias Primas | AG-06 | 12 | — | — | — | sí | sí | 6 «Estrategia de análisis del tipo de activo» |
| Analista de Prospectiva y Horizontes | AG-10 | 12 | — | — | — | sí | sí | — |
| Analista de Renta Fija y Crédito | AG-04 | 12 | — | — | — | sí | sí | 6 «Estrategia de análisis del tipo de activo» |
| Analista de Renta Variable | AG-03 | 12 | — | — | — | sí | sí | 6 «Estrategia de análisis del tipo de activo» |
| Analista de Tipos de Interés, Crédito y Volatilidad | AG-25 | 12 | — | — | — | sí | sí | 6 «Estrategia de análisis de los tipos de interés, el crédito y la volatilidad» |
| Analista de hipótesis contrarias | AG-11 | 12 | — | — | — | sí | sí | — |
| Analista de Índices Bursátiles | AG-21 | 12 | — | — | — | sí | sí | 6 «Estrategia de análisis de los índices bursátiles» |
| Analizador de Tendencias de Inversión | AG-02 | 12 | — | — | — | sí | sí | — |
| Auditor | AG-19 | 12 | — | — | — | sí | sí | — |
| Buscador de Fuentes Avanzadas | AG-16 | 12 | — | — | — | sí | sí | — |
| Coordinador de Peticiones y Consultas | AG-01 | 12 | — | — | — | sí | sí | — |
| Curador de Evidencia | AG-12 | 12 | — | — | — | sí | sí | — |
| Documentador para el Analizador | AG-14 | 12 | — | — | — | sí | sí | — |
| Documentador para el Motor de Cálculo Avanzado | AG-15 | 12 | — | — | — | sí | sí | — |
| Evaluador de Previsiones y Aprendizaje | AG-20 | 12 | — | — | — | sí | sí | — |
| MC-01 Fundamentos cuantitativos y estadística | — | 12 | — | — | — | sí | sí | — |
| MC-02 Series temporales, tendencias, regímenes y volatilidad | — | 12 | — | — | — | sí | sí | — |
| MC-03 Econometría, causalidad y macroeconomía cuantitativa | — | 12 | — | — | — | sí | sí | — |
| MC-04 Crecimiento, difusión y prospectiva cuantitativa | — | 12 | — | — | — | sí | sí | — |
| MC-05 Simulación estocástica y escenarios | — | 12 | — | — | — | sí | sí | — |
| MC-06 Aprendizaje automático y predicción calibrada | — | 12 | — | — | — | sí | sí | — |
| MC-07 Optimización, decisión y riesgo | — | 12 | — | — | — | sí | sí | — |
| MC-08 Auditoría cuantitativa independiente | — | 12 | — | — | — | sí | sí | — |
| MC-09 Valoración y modelos de precios de activos | — | 12 | — | — | — | sí | sí | — |
| MC-10 Evaluación predictiva y backtesting | — | 12 | — | — | — | sí | sí | — |
| Motor de Cálculo Avanzado para el Analizador de Tendencias de Inversión | AG-13 | 12 | — | — | — | sí | sí | — |
| Orquestador técnico | AG-18 | 12 | — | — | — | sí | sí | — |
| Redactor y Diseñador de Informes | AG-17 | 12 | — | — | — | sí | sí | — |

### Títulos por sección (coherencia entre prompts)

| Sección | Anexo G | Títulos distintos en los prompts (n.º de prompts) |
| --- | --- | --- |
| 1 | Identidad y misión (quién eres, para qué existes, qué no eres) | Identidad y misión (30); IDENTIDAD Y MISIÓN (6) |
| 2 | Posición en el bloque (con quién hablas, por qué contratos, qué archivos lees y escribes) | Posición en el bloque (30); POSICIÓN EN EL MOTOR (5); POSICIÓN EN EL BLOQUE (1) |
| 3 | Reglas críticas que te aplican (extracto de R1–R27) | Reglas críticas que te aplican (30); REGLAS QUE TE APLICAN (5); REGLAS CRÍTICAS QUE TE APLICAN (1) |
| 4 | Entradas y salidas (campos y formatos) | Entradas y salidas (30); ENTRADAS Y SALIDAS (6) |
| 5 | Procedimiento operativo paso a paso | Procedimiento operativo (30); PROCEDIMIENTO (5); PROCEDIMIENTO OPERATIVO (1) |
| 6 | Metodología y criterios de decisión propios | Metodología y criterios de decisión (11); **Estrategia de análisis del tipo de activo** (no coincide) (7); Metodología y criterios de decisión propios (6); CRITERIOS DE DECISIÓN PROPIOS (5); **Estrategia de análisis de los derivados financieros** (no coincide) (1); **Estrategia de análisis de los fondos y vehículos de inversión colectiva** (no coincide) (1); **Estrategia de análisis de los instrumentos monetarios y de la liquidez** (no coincide) (1); **Estrategia de análisis de los tipos de interés, el crédito y la volatilidad** (no coincide) (1); **Estrategia de análisis de los índices bursátiles** (no coincide) (1); METODOLOGÍA Y CRITERIOS DE DECISIÓN (1) |
| 7 | Eficiencia: presupuesto, reutilización y reglas de parada | Eficiencia (17); Eficiencia: presupuesto, reutilización y reglas de parada (7); EFICIENCIA (5); Eficiencia: presupuesto, reutilización y parada (5); EFICIENCIA: PRESUPUESTO, REUTILIZACIÓN Y REGLAS DE PARADA (1); Eficiencia: presupuesto y reglas de parada (1) |
| 8 | Autocrítica y control de calidad | Autocrítica y control de calidad (30); AUTOCRÍTICA Y VERIFICACIÓN (5); AUTOCRÍTICA Y CONTROL DE CALIDAD (1) |
| 9 | Aprendizaje: cómo usas F6 y qué aportas | Aprendizaje (21); Aprendizaje: cómo usas F6 y qué aportas (9); APRENDIZAJE (6) |
| 10 | Base de conocimientos (precisa, exhaustiva y específica de tu dominio) | Base de conocimientos (29); BASE DE CONOCIMIENTOS (6) |
| 11 | Formatos de salida y ejemplo breve | Formato y estilo (13); Formatos de salida y ejemplo breve (10); FORMATO DE SALIDA (INTERNO) Y EJEMPLO (5); Formatos de salida y ejemplos (4); Formatos de salida y ejemplos breves (2); FORMATOS DE SALIDA Y EJEMPLO BREVE (1); Formato de salida y ejemplo (1) |
| 12 | Límites, seguridad y modos degradados | Límites, seguridad y modos degradados (30); LÍMITES Y MODOS DEGRADADOS (5); LÍMITES, SEGURIDAD Y MODOS DEGRADADOS (1) |

## Paso 2 · Sección 10: recuento por subárea

Criterios (detalle en `analisis-tecnico.md`): **definición** = elemento que empieza por un término en negrita seguido de «:», «=» o raya; **fórmula** = tramo de código con un operador o símbolo de cálculo, más cada «=»/«≈» con espacios fuera del código; **umbral** = comparador (≥, ≤, <, >, «al menos», «más de»…) seguido de una cifra; **trampa** = elemento de una subárea de trampas, errores o sesgos, o que nombra una trampa o un error típico; **referencia** = cita autor-año (en las subáreas de referencias canónicas, cada entrada). El inventario de competencias no se cuenta (resume lo anterior).

| Prompt | Subáreas | Elementos | Definiciones | Fórmulas | Umbrales | Trampas | Referencias |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Analista Inmobiliario y de Infraestructuras | 20 | 122 | 63 | 43 | 8 | 14 | 35 |
| Analista de Alternativos y Mercados Privados | 24 | 159 | 66 | 31 | 11 | 20 | 85 |
| Analista de Criptoactivos y Activos Digitales | 20 | 120 | 55 | 25 | 16 | 24 | 37 |
| Analista de Derivados Financieros | 20 | 95 | 51 | 30 | 4 | 11 | 63 |
| Analista de Divisas | 25 | 114 | 82 | 23 | 3 | 11 | 96 |
| Analista de Fondos y Vehículos de Inversión Colectiva | 22 | 100 | 53 | 10 | 9 | 11 | 49 |
| Analista de Instrumentos Monetarios y Liquidez | 20 | 83 | 51 | 26 | 20 | 10 | 31 |
| Analista de Materias Primas | 22 | 138 | 81 | 22 | 5 | 12 | 52 |
| Analista de Prospectiva y Horizontes | 15 | 168 | 57 | 37 | 3 | 15 | 78 |
| Analista de Renta Fija y Crédito | 22 | 112 | 80 | 51 | 9 | 12 | 57 |
| Analista de Renta Variable | 28 | 157 | 87 | 41 | 22 | 11 | 82 |
| Analista de Tipos de Interés, Crédito y Volatilidad | 22 | 99 | 66 | 53 | 5 | 10 | 95 |
| Analista de hipótesis contrarias | 13 | 211 | 33 | 4 | 0 | 138 | 41 |
| Analista de Índices Bursátiles | 26 | 123 | 58 | 14 | 8 | 19 | 59 |
| Analizador de Tendencias de Inversión | 18 | 180 | 73 | 29 | 6 | 18 | 52 |
| Auditor | 12 | 73 | 44 | 11 | 7 | 36 | 23 |
| Buscador de Fuentes Avanzadas | 16 | 96 | 19 | 8 | 4 | 21 | 23 |
| Coordinador de Peticiones y Consultas | 16 | 198 | 34 | 30 | 10 | 2 | 1 |
| Curador de Evidencia | 15 | 80 | 44 | 20 | 5 | 1 | 6 |
| Documentador para el Analizador | 14 | 83 | 16 | 4 | 3 | 4 | 244 |
| Documentador para el Motor de Cálculo Avanzado | 10 | 48 | 13 | 20 | 1 | 0 | 230 |
| Evaluador de Previsiones y Aprendizaje | 21 | 112 | 85 | 86 | 9 | 12 | 66 |
| MC-01 Fundamentos cuantitativos y estadística | 17 | 84 | 15 | 99 | 14 | 15 | 26 |
| MC-02 Series temporales, tendencias, regímenes y volatilidad | 16 | 69 | 38 | 80 | 16 | 4 | 49 |
| MC-03 Econometría, causalidad y macroeconomía cuantitativa | 14 | 58 | 30 | 60 | 17 | 1 | 60 |
| MC-04 Crecimiento, difusión y prospectiva cuantitativa | 15 | 47 | 30 | 47 | 4 | 3 | 32 |
| MC-05 Simulación estocástica y escenarios | 14 | 50 | 9 | 65 | 6 | 4 | 29 |
| MC-06 Aprendizaje automático y predicción calibrada | 16 | 72 | 47 | 28 | 13 | 2 | 43 |
| MC-07 Optimización, decisión y riesgo | 15 | 61 | 43 | 63 | 12 | 1 | 39 |
| MC-08 Auditoría cuantitativa independiente | 12 | 48 | 29 | 15 | 0 | 1 | 13 |
| MC-09 Valoración y modelos de precios de activos | 24 | 112 | 94 | 157 | 20 | 3 | 120 |
| MC-10 Evaluación predictiva y backtesting | 15 | 62 | 46 | 81 | 17 | 11 | 49 |
| Motor de Cálculo Avanzado para el Analizador de Tendencias de Inversión | 19 | 189 | 51 | 318 | 46 | 9 | 154 |
| Orquestador técnico | 12 | 60 | 47 | 27 | 10 | 2 | 9 |
| Redactor y Diseñador de Informes | 13 | 227 | 27 | 46 | 12 | 15 | 44 |
| **Total** | 623 | 3810 | 1717 | 1704 | 355 | 483 | 2172 |

### Analista Inmobiliario y de Infraestructuras

| Subárea | Título | Elem. | Def. | Fórm. | Umbr. | Tramp. | Ref. |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 10.1 | Renta y valor de un inmueble | 6 | 4 | 12 | 1 | 0 | 0 |
| 10.2 | Métricas de REIT y SOCIMI | 4 | 4 | 6 | 1 | 0 | 0 |
| 10.3 | Financiación y solvencia | 5 | 5 | 9 | 4 | 1 | 0 |
| 10.4 | Tipos de interés, cap rates y modelo de Gordon | 4 | 4 | 5 | 0 | 0 | 0 |
| 10.5 | Ciclos inmobiliarios y de crédito | 6 | 6 | 1 | 1 | 0 | 5 |
| 10.6 | Cotizado frente a privado: descubrimiento de precios y desuavizado | 5 | 5 | 3 | 0 | 0 | 6 |
| 10.7 | Subsectores y sus motores | 10 | 0 | 1 | 0 | 0 | 0 |
| 10.8 | Infraestructuras: frontera y conocimiento útil | 7 | 6 | 1 | 0 | 0 | 0 |
| 10.9 | Regulación del alquiler y del sector | 3 | 3 | 0 | 0 | 0 | 2 |
| 10.10 | Estructuras cotizadas y no cotizadas: conocimiento para juzgar la invertibilidad | 5 | 5 | 0 | 0 | 0 | 1 |
| 10.11 | Trampas y errores frecuentes | 13 | 0 | 0 | 1 | 13 | 0 |
| 10.12 | Fuentes de datos típicas | 7 | 0 | 0 | 0 | 0 | 0 |
| 10.13 | Referencias académicas canónicas (referencias canónicas) | 19 | 0 | 0 | 0 | 0 | 18 |
| 10.14 | Subtipos cotizados: promotoras, gestoras e hipotecarios | 5 | 5 | 0 | 0 | 0 | 0 |
| 10.15 | Métodos de valoración inmobiliaria y normas de tasación | 5 | 5 | 4 | 0 | 0 | 0 |
| 10.16 | Vivienda: estructura del mercado hipotecario y demanda | 4 | 4 | 1 | 0 | 0 | 0 |
| 10.17 | Sostenibilidad, obsolescencia y datos ESG del sector | 4 | 4 | 0 | 0 | 0 | 0 |
| 10.18 | Casos históricos de referencia | 7 | 0 | 0 | 0 | 0 | 3 |
| 10.19 | Fuentes por área de los archivos de referencias | 3 | 3 | 0 | 0 | 0 | 0 |
| 10.20 | Inventario de competencias (inventario, no se cuenta) | 13 | 0 | 0 | 0 | 0 | 0 |

### Analista de Alternativos y Mercados Privados

| Subárea | Título | Elem. | Def. | Fórm. | Umbr. | Tramp. | Ref. |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 10.1 | Métricas de fondos privados | 7 | 7 | 5 | 2 | 1 | 6 |
| 10.2 | Evidencia sobre la rentabilidad del capital privado | 5 | 4 | 1 | 0 | 0 | 11 |
| 10.3 | Capital riesgo | 4 | 2 | 0 | 0 | 0 | 2 |
| 10.4 | Deuda privada | 5 | 5 | 2 | 0 | 0 | 0 |
| 10.5 | Secundarios y soluciones de liquidez | 4 | 4 | 3 | 0 | 1 | 0 |
| 10.6 | Estrategias hedge según el régimen | 12 | 1 | 0 | 0 | 0 | 7 |
| 10.7 | Sesgos de las bases de datos | 6 | 4 | 1 | 2 | 6 | 3 |
| 10.8 | Suavizado y desuavizado | 6 | 6 | 10 | 2 | 0 | 4 |
| 10.9 | Valores vinculados a seguros | 2 | 1 | 2 | 0 | 0 | 0 |
| 10.10 | Coleccionables: arte, vino y otros | 5 | 4 | 2 | 0 | 0 | 7 |
| 10.11 | Royalties | 2 | 2 | 0 | 1 | 0 | 0 |
| 10.12 | Financiación de litigios | 1 | 0 | 0 | 0 | 0 | 0 |
| 10.13 | Financiación participativa y plataformas | 2 | 1 | 0 | 1 | 0 | 0 |
| 10.14 | Estructuras de acceso minorista: conocimiento para juzgar la invertibilidad | 4 | 2 | 1 | 1 | 0 | 1 |
| 10.15 | Trampas y errores frecuentes | 12 | 0 | 0 | 0 | 12 | 0 |
| 10.16 | Fuentes de datos típicas | 9 | 0 | 0 | 0 | 0 | 0 |
| 10.17 | Referencias académicas canónicas (referencias canónicas) | 39 | 0 | 0 | 0 | 0 | 38 |
| 10.18 | Infraestructuras, renovables, inmobiliario privado, bosques y agrícola | 10 | 10 | 3 | 1 | 0 | 0 |
| 10.19 | Mecánica del fondo, valoración y gobierno | 4 | 4 | 0 | 0 | 0 | 1 |
| 10.20 | Matemática de la compra apalancada y ciclo de salidas | 4 | 3 | 1 | 1 | 0 | 0 |
| 10.21 | Normativa y supervisión que condicionan el segmento | 4 | 3 | 0 | 0 | 0 | 0 |
| 10.22 | Casos históricos de referencia | 9 | 0 | 0 | 0 | 0 | 5 |
| 10.23 | Fuentes por área de los archivos de referencias | 3 | 3 | 0 | 0 | 0 | 0 |
| 10.24 | Inventario de competencias (inventario, no se cuenta) | 15 | 0 | 0 | 0 | 0 | 0 |

### Analista de Criptoactivos y Activos Digitales

| Subárea | Título | Elem. | Def. | Fórm. | Umbr. | Tramp. | Ref. |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 10.1 | Bitcoin: fundamentos | 5 | 4 | 4 | 2 | 0 | 0 |
| 10.2 | Plataformas de contratos inteligentes | 4 | 4 | 2 | 0 | 0 | 0 |
| 10.3 | Stablecoins, DeFi y tokenización | 3 | 3 | 1 | 0 | 0 | 1 |
| 10.4 | Métricas en cadena: definiciones, umbrales y trampas | 12 | 0 | 9 | 9 | 12 | 0 |
| 10.5 | Derivados | 4 | 3 | 1 | 1 | 0 | 0 |
| 10.6 | Flujos institucionales, ciclos y correlaciones | 5 | 4 | 1 | 1 | 0 | 1 |
| 10.7 | Tokenómica | 4 | 3 | 3 | 1 | 0 | 0 |
| 10.8 | Modelos de valoración y evidencia académica | 6 | 6 | 0 | 0 | 0 | 7 |
| 10.9 | Riesgos específicos | 5 | 5 | 2 | 0 | 0 | 5 |
| 10.10 | Marco regulatorio | 3 | 3 | 0 | 1 | 0 | 0 |
| 10.11 | Trampas y errores frecuentes | 12 | 0 | 0 | 0 | 12 | 0 |
| 10.12 | Fuentes de datos típicas | 8 | 0 | 0 | 0 | 0 | 0 |
| 10.13 | Referencias académicas canónicas (referencias canónicas) | 20 | 0 | 0 | 0 | 0 | 19 |
| 10.14 | Subtipos: utilidad y gobernanza, security tokens, NFT y productos cotizados | 6 | 6 | 1 | 1 | 0 | 0 |
| 10.15 | Valoración fundamental de protocolos y redes | 5 | 5 | 1 | 0 | 0 | 0 |
| 10.16 | Clasificación jurídica de los tokens | 3 | 3 | 0 | 0 | 0 | 0 |
| 10.17 | Señales de sentimiento y atención | 4 | 3 | 0 | 0 | 0 | 1 |
| 10.18 | Casos históricos de referencia | 8 | 0 | 0 | 0 | 0 | 3 |
| 10.19 | Fuentes por área de los archivos de referencias | 3 | 3 | 0 | 0 | 0 | 0 |
| 10.20 | Inventario de competencias (inventario, no se cuenta) | 12 | 0 | 0 | 0 | 0 | 0 |

### Analista de Derivados Financieros

| Subárea | Título | Elem. | Def. | Fórm. | Umbr. | Tramp. | Ref. |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 10.0 | (antes de la primera subárea) | 1 | 0 | 0 | 0 | 0 | 0 |
| 10.1 | Pagos, paridad y límites de arbitraje | 4 | 4 | 8 | 0 | 0 | 1 |
| 10.2 | Valoración: Black-Scholes-Merton y binomial | 5 | 4 | 7 | 0 | 0 | 8 |
| 10.3 | Griegas y la contabilidad de una opción cubierta | 7 | 1 | 1 | 0 | 0 | 0 |
| 10.4 | Volatilidad realizada, pronóstico e implícita | 5 | 5 | 4 | 0 | 0 | 9 |
| 10.5 | Prima de riesgo de varianza: evidencia | 5 | 0 | 0 | 0 | 0 | 6 |
| 10.6 | Sesgo (skew) y lo que informa | 5 | 1 | 2 | 0 | 5 | 5 |
| 10.7 | Estructura de plazos de la volatilidad | 2 | 0 | 0 | 0 | 0 | 2 |
| 10.8 | Futuros: base, contango, backwardation y roll | 6 | 6 | 2 | 0 | 0 | 8 |
| 10.9 | Swaps y CDS como instrumentos | 3 | 3 | 2 | 0 | 0 | 0 |
| 10.10 | Estrategias de opciones y sus primas | 9 | 1 | 0 | 0 | 0 | 4 |
| 10.11 | Productos cotizados para minoristas | 5 | 5 | 0 | 0 | 0 | 7 |
| 10.12 | Riesgos de los derivados | 6 | 6 | 0 | 2 | 0 | 0 |
| 10.13 | Fuentes de datos típicas | 1 | 0 | 0 | 0 | 0 | 0 |
| 10.14 | Referencias canónicas (referencias canónicas) | 1 | 0 | 0 | 0 | 0 | 8 |
| 10.15 | Errores frecuentes que debes evitar | 6 | 0 | 0 | 0 | 6 | 0 |
| 10.16 | Reglas prácticas de lectura de la superficie y de los eventos | 6 | 6 | 4 | 1 | 0 | 0 |
| 10.17 | Normativa e infraestructura de mercado | 6 | 6 | 0 | 0 | 0 | 0 |
| 10.18 | Casos históricos de referencia | 9 | 0 | 0 | 1 | 0 | 5 |
| 10.19 | Fuentes por área de los archivos de referencias | 3 | 3 | 0 | 0 | 0 | 0 |
| 10.20 | Inventario de competencias (inventario, no se cuenta) | 14 | 0 | 0 | 0 | 0 | 0 |

### Analista de Divisas

| Subárea | Título | Elem. | Def. | Fórm. | Umbr. | Tramp. | Ref. |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 10.0 | (antes de la primera subárea) | 1 | 0 | 0 | 0 | 0 | 0 |
| 10.1 | Convenciones del mercado de divisas | 6 | 5 | 6 | 0 | 0 | 0 |
| 10.2 | Paridades de tipos de interés | 3 | 2 | 4 | 0 | 0 | 5 |
| 10.3 | Paridad de poder adquisitivo y equilibrio | 7 | 7 | 2 | 0 | 0 | 7 |
| 10.4 | Previsibilidad de los tipos de cambio | 4 | 4 | 0 | 0 | 0 | 5 |
| 10.5 | Carry y riesgo de crash | 6 | 6 | 1 | 0 | 0 | 7 |
| 10.6 | Momentum y valor cambiario | 4 | 4 | 0 | 0 | 0 | 6 |
| 10.7 | Balanza de pagos y vulnerabilidad externa | 6 | 6 | 3 | 2 | 0 | 3 |
| 10.8 | Bancos centrales e intervenciones | 4 | 3 | 0 | 0 | 0 | 2 |
| 10.9 | Regímenes cambiarios | 3 | 3 | 0 | 0 | 0 | 4 |
| 10.10 | El dólar como factor global | 4 | 4 | 0 | 0 | 0 | 4 |
| 10.11 | Posicionamiento (CFTC) | 3 | 1 | 0 | 1 | 0 | 1 |
| 10.12 | Volatilidad implícita y risk reversals | 6 | 6 | 4 | 0 | 0 | 1 |
| 10.13 | Emergentes y controles de capital | 4 | 3 | 0 | 0 | 0 | 1 |
| 10.14 | Coberturas cambiarias y su coste | 6 | 5 | 1 | 0 | 0 | 2 |
| 10.15 | Microestructura y estacionalidad | 3 | 1 | 0 | 0 | 0 | 0 |
| 10.16 | Fuentes de datos típicas | 1 | 0 | 0 | 0 | 0 | 0 |
| 10.17 | Referencias canónicas (referencias canónicas) | 1 | 0 | 0 | 0 | 0 | 38 |
| 10.18 | Errores frecuentes que debes evitar | 11 | 0 | 0 | 0 | 11 | 0 |
| 10.19 | Formas del mercado: contado, plazo y swaps de divisas | 6 | 5 | 1 | 0 | 0 | 0 |
| 10.20 | Modelos teóricos del tipo de cambio que debes saber aplicar | 6 | 6 | 0 | 0 | 0 | 4 |
| 10.21 | Riesgo político, fiscal y de evento | 4 | 4 | 0 | 0 | 0 | 2 |
| 10.22 | Sistema monetario internacional y largo plazo | 4 | 4 | 0 | 0 | 0 | 0 |
| 10.23 | Casos históricos de referencia | 8 | 0 | 1 | 0 | 0 | 4 |
| 10.24 | Fuentes por área de los archivos de referencias | 3 | 3 | 0 | 0 | 0 | 0 |
| 10.25 | Inventario de competencias (inventario, no se cuenta) | 16 | 0 | 0 | 0 | 0 | 0 |

### Analista de Fondos y Vehículos de Inversión Colectiva

| Subárea | Título | Elem. | Def. | Fórm. | Umbr. | Tramp. | Ref. |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 10.0 | (antes de la primera subárea) | 1 | 0 | 0 | 0 | 0 | 0 |
| 10.1 | Estructuras y marco regulatorio europeo | 8 | 0 | 1 | 8 | 0 | 2 |
| 10.2 | ETF: creación, reembolso, réplica y préstamo de valores | 7 | 7 | 1 | 1 | 0 | 2 |
| 10.3 | Costes y su efecto | 3 | 3 | 1 | 0 | 0 | 0 |
| 10.4 | Fondos cerrados: el enigma del descuento | 6 | 6 | 0 | 0 | 1 | 7 |
| 10.5 | Persistencia del rendimiento de los gestores | 5 | 5 | 0 | 0 | 0 | 7 |
| 10.6 | Flujos y su efecto en los precios | 5 | 0 | 0 | 0 | 0 | 8 |
| 10.7 | Estrategias hedge y sus regímenes | 11 | 1 | 0 | 0 | 0 | 8 |
| 10.8 | ETF apalancados e inversos: decaimiento por volatilidad | 4 | 3 | 7 | 0 | 0 | 2 |
| 10.9 | Fondos monetarios, mixtos y de fondos | 3 | 3 | 0 | 0 | 0 | 0 |
| 10.10 | Capital privado, semilíquidos e inmobiliarios abiertos | 4 | 3 | 0 | 0 | 0 | 0 |
| 10.11 | Riesgos de liquidez y gating | 3 | 0 | 0 | 0 | 0 | 0 |
| 10.12 | Fiscalidad general (sin consejo) | 1 | 0 | 0 | 0 | 0 | 0 |
| 10.13 | Sesgos de medición | 4 | 3 | 0 | 0 | 4 | 0 |
| 10.14 | Fuentes de datos típicas | 1 | 0 | 0 | 0 | 0 | 0 |
| 10.15 | Referencias canónicas (referencias canónicas) | 1 | 0 | 0 | 0 | 0 | 6 |
| 10.16 | Errores frecuentes que debes evitar | 6 | 0 | 0 | 0 | 6 | 0 |
| 10.17 | Medición del rendimiento y de la estrategia de una categoría | 5 | 5 | 0 | 0 | 0 | 3 |
| 10.18 | Domicilio, clases de participaciones y fricciones del vehículo | 6 | 6 | 0 | 0 | 0 | 0 |
| 10.19 | Tendencias estructurales de la industria | 5 | 5 | 0 | 0 | 0 | 0 |
| 10.20 | Casos históricos de referencia | 8 | 0 | 0 | 0 | 0 | 4 |
| 10.21 | Fuentes por área de los archivos de referencias | 3 | 3 | 0 | 0 | 0 | 0 |
| 10.22 | Inventario de competencias (inventario, no se cuenta) | 13 | 0 | 0 | 0 | 0 | 0 |

### Analista de Instrumentos Monetarios y Liquidez

| Subárea | Título | Elem. | Def. | Fórm. | Umbr. | Tramp. | Ref. |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 10.0 | (antes de la primera subárea) | 1 | 0 | 0 | 0 | 0 | 0 |
| 10.1 | Implementación de la política monetaria | 5 | 2 | 2 | 0 | 0 | 0 |
| 10.2 | Curva monetaria y expectativas implícitas | 5 | 3 | 4 | 0 | 0 | 3 |
| 10.3 | Convenciones de cálculo y rentabilidad equivalente | 8 | 7 | 9 | 2 | 0 | 0 |
| 10.4 | Instrumentos del tipo | 6 | 6 | 1 | 2 | 0 | 0 |
| 10.5 | Fondos monetarios | 10 | 3 | 1 | 15 | 0 | 2 |
| 10.6 | Garantía de depósitos frente a valores | 5 | 5 | 0 | 1 | 0 | 1 |
| 10.7 | Riesgo emisor y de contraparte | 4 | 4 | 3 | 0 | 0 | 4 |
| 10.8 | Inflación y rentabilidad real | 3 | 1 | 2 | 0 | 0 | 0 |
| 10.9 | Fijar plazo o renovar | 5 | 3 | 2 | 0 | 0 | 0 |
| 10.10 | Transmisión a los depósitos | 3 | 3 | 0 | 0 | 0 | 1 |
| 10.11 | Liquidez en otra divisa | 3 | 2 | 2 | 0 | 0 | 1 |
| 10.12 | Coste de oportunidad y papel de la liquidez | 1 | 0 | 0 | 0 | 0 | 0 |
| 10.13 | Fuentes de datos | 1 | 0 | 0 | 0 | 0 | 0 |
| 10.14 | Referencias canónicas (referencias canónicas) | 1 | 0 | 0 | 0 | 0 | 19 |
| 10.15 | Errores frecuentes que debes evitar | 10 | 0 | 0 | 0 | 10 | 0 |
| 10.16 | Función de reacción y calendario de los bancos centrales | 4 | 4 | 0 | 0 | 0 | 0 |
| 10.17 | Regímenes extremos: tipos negativos y tensión de financiación | 3 | 3 | 0 | 0 | 0 | 0 |
| 10.18 | Fiscalidad general y tendencias estructurales (contexto, sin consejo) | 2 | 2 | 0 | 0 | 0 | 0 |
| 10.19 | Fuentes por área de los archivos de referencias | 3 | 3 | 0 | 0 | 0 | 0 |
| 10.20 | Inventario de competencias (inventario, no se cuenta) | 13 | 0 | 0 | 0 | 0 | 0 |

### Analista de Materias Primas

| Subárea | Título | Elem. | Def. | Fórm. | Umbr. | Tramp. | Ref. |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 10.1 | Estructura de los futuros y teoría del almacenamiento | 7 | 7 | 4 | 0 | 0 | 7 |
| 10.2 | Rentabilidad de los futuros y primas de riesgo | 7 | 6 | 7 | 0 | 0 | 7 |
| 10.3 | Índices y estructuras de acceso (para juzgar la invertibilidad) | 4 | 4 | 0 | 0 | 0 | 1 |
| 10.4 | Petróleo y productos refinados | 7 | 7 | 4 | 0 | 0 | 2 |
| 10.5 | Gas natural, GNL, carbón y uranio | 6 | 6 | 1 | 0 | 0 | 0 |
| 10.6 | Metales preciosos | 5 | 5 | 3 | 3 | 0 | 2 |
| 10.7 | Metales industriales y de la transición | 8 | 8 | 0 | 0 | 0 | 0 |
| 10.8 | Agrícolas y ganado | 8 | 7 | 3 | 0 | 0 | 0 |
| 10.9 | Carbono | 2 | 2 | 0 | 0 | 0 | 0 |
| 10.10 | Superciclos, coste marginal y precios reales | 4 | 4 | 0 | 0 | 0 | 3 |
| 10.11 | Estacionalidad | 1 | 0 | 0 | 1 | 0 | 0 |
| 10.12 | Posicionamiento y financiarización | 2 | 2 | 0 | 0 | 0 | 2 |
| 10.13 | Trampas y errores frecuentes | 12 | 0 | 0 | 0 | 12 | 0 |
| 10.14 | Fuentes de datos típicas | 8 | 0 | 0 | 0 | 0 | 0 |
| 10.15 | Referencias académicas canónicas (referencias canónicas) | 26 | 0 | 0 | 0 | 0 | 25 |
| 10.16 | Subtipos ampliados: metales para baterías, uranio, electricidad, madera y créditos ambientales | 6 | 6 | 0 | 0 | 0 | 0 |
| 10.17 | Indicadores transversales de demanda, logística y macro | 5 | 5 | 0 | 0 | 0 | 1 |
| 10.18 | Transición energética y largo plazo | 4 | 4 | 0 | 0 | 0 | 0 |
| 10.19 | Normativa de mercado relevante para el ámbito | 5 | 5 | 0 | 0 | 0 | 0 |
| 10.20 | Casos históricos de referencia | 8 | 0 | 0 | 1 | 0 | 2 |
| 10.21 | Fuentes por área de los archivos de referencias | 3 | 3 | 0 | 0 | 0 | 0 |
| 10.22 | Inventario de competencias (inventario, no se cuenta) | 13 | 0 | 0 | 0 | 0 | 0 |

### Analista de Prospectiva y Horizontes

| Subárea | Título | Elem. | Def. | Fórm. | Umbr. | Tramp. | Ref. |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 10.0 | (antes de la primera subárea) | 1 | 0 | 0 | 0 | 0 | 0 |
| 10.1 | Métodos de prospectiva | 10 | 3 | 0 | 0 | 1 | 12 |
| 10.2 | Superprevisión y juicio probabilístico estructurado | 5 | 5 | 4 | 0 | 0 | 2 |
| 10.3 | Previsión cuantitativa por horizonte y clase de activo | 32 | 18 | 15 | 2 | 0 | 28 |
| 10.4 | Cómo formular pronósticos verificables | 7 | 7 | 0 | 0 | 0 | 0 |
| 10.5 | Correspondencia entre lenguaje y probabilidad | 3 | 0 | 1 | 0 | 0 | 2 |
| 10.6 | Calibración y reglas de puntuación propias | 10 | 10 | 7 | 1 | 0 | 8 |
| 10.7 | Referencias de comparación y referencias ingenuas por tipo de activo | 14 | 1 | 0 | 0 | 0 | 0 |
| 10.8 | Errores de prospectiva y cómo evitarlos | 14 | 0 | 1 | 0 | 14 | 2 |
| 10.9 | Indicadores adelantados por tipo de activo | 13 | 0 | 0 | 0 | 0 | 0 |
| 10.10 | Calendario de catalizadores recurrentes | 23 | 0 | 3 | 0 | 0 | 0 |
| 10.11 | Referencias canónicas (referencias canónicas) | 22 | 0 | 0 | 0 | 0 | 22 |
| 10.12 | Proyección estructural de largo plazo: difusión, sustitución y demografía | 7 | 6 | 6 | 0 | 0 | 1 |
| 10.13 | Sucesos raros, colas y probabilidades de base de los grandes eventos | 4 | 4 | 0 | 0 | 0 | 1 |
| 10.14 | Fuentes por área de los archivos de referencias | 3 | 3 | 0 | 0 | 0 | 0 |
| 10.15 | Inventario de competencias (inventario, no se cuenta) | 11 | 0 | 0 | 0 | 0 | 0 |

### Analista de Renta Fija y Crédito

| Subárea | Título | Elem. | Def. | Fórm. | Umbr. | Tramp. | Ref. |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 10.0 | (antes de la primera subárea) | 1 | 0 | 0 | 0 | 0 | 0 |
| 10.1 | Matemática de bonos | 11 | 10 | 16 | 0 | 0 | 0 |
| 10.2 | La curva de tipos | 7 | 7 | 7 | 0 | 0 | 9 |
| 10.3 | Política monetaria y regla de Taylor | 6 | 5 | 5 | 0 | 0 | 4 |
| 10.4 | Inflación, breakevens y bonos ligados | 6 | 6 | 3 | 0 | 0 | 0 |
| 10.5 | Crédito | 9 | 9 | 12 | 3 | 0 | 2 |
| 10.6 | Carry, rolldown, valor y momentum en renta fija | 4 | 4 | 3 | 0 | 0 | 4 |
| 10.7 | Emergentes: divisa fuerte frente a divisa local | 6 | 6 | 1 | 1 | 0 | 2 |
| 10.8 | El monetario como referencia y frontera con MON | 3 | 0 | 2 | 1 | 0 | 0 |
| 10.9 | Titulizaciones y deuda garantizada | 4 | 3 | 0 | 0 | 0 | 0 |
| 10.10 | Liquidez y microestructura | 4 | 2 | 0 | 1 | 0 | 1 |
| 10.11 | Correlación bonos-acciones y papel de la duración | 2 | 0 | 0 | 0 | 0 | 1 |
| 10.12 | Riesgo soberano y fiscal | 4 | 4 | 1 | 0 | 0 | 1 |
| 10.13 | Fuentes de datos típicas | 1 | 0 | 0 | 0 | 0 | 0 |
| 10.14 | Referencias canónicas (referencias canónicas) | 1 | 0 | 0 | 0 | 0 | 29 |
| 10.15 | Errores frecuentes que debes evitar | 12 | 0 | 0 | 0 | 12 | 0 |
| 10.16 | Subtipos de renta fija: conocimiento para delimitar el ámbito | 7 | 7 | 0 | 1 | 0 | 0 |
| 10.17 | Oferta, demanda y técnicos del mercado de bonos | 7 | 7 | 0 | 1 | 0 | 0 |
| 10.18 | Rentabilidad cubierta en divisa y valor relativo internacional | 3 | 3 | 1 | 0 | 0 | 1 |
| 10.19 | Reestructuraciones, prelación y recuperación | 4 | 4 | 0 | 0 | 0 | 2 |
| 10.20 | Casos históricos de referencia | 7 | 0 | 0 | 1 | 0 | 1 |
| 10.21 | Fuentes por área de los archivos de referencias | 3 | 3 | 0 | 0 | 0 | 0 |
| 10.22 | Inventario de competencias (inventario, no se cuenta) | 18 | 0 | 0 | 0 | 0 | 0 |

### Analista de Renta Variable

| Subárea | Título | Elem. | Def. | Fórm. | Umbr. | Tramp. | Ref. |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 10.0 | (antes de la primera subárea) | 1 | 0 | 0 | 0 | 0 | 0 |
| 10.1 | Descomposición de la rentabilidad y rentabilidad esperada | 5 | 5 | 3 | 0 | 0 | 8 |
| 10.2 | Valoración intrínseca | 8 | 8 | 18 | 0 | 1 | 3 |
| 10.3 | Múltiplos: cuándo usar cada uno | 10 | 0 | 1 | 0 | 0 | 0 |
| 10.4 | Valoración agregada: CAPE, prima de riesgo implícita y modelo de la Fed | 4 | 4 | 2 | 0 | 0 | 4 |
| 10.5 | Factores: evidencia, persistencia y crowding | 11 | 3 | 0 | 3 | 0 | 18 |
| 10.6 | Momentum y reversión por horizontes | 8 | 0 | 0 | 0 | 0 | 12 |
| 10.7 | Revisiones y sorpresas de beneficios | 6 | 4 | 0 | 0 | 0 | 2 |
| 10.8 | Ciclo sectorial y rotación | 9 | 0 | 0 | 0 | 0 | 1 |
| 10.9 | Temáticas estructurales | 5 | 4 | 0 | 1 | 0 | 2 |
| 10.10 | Estructura de mercado | 4 | 4 | 0 | 0 | 0 | 0 |
| 10.11 | Flujos y posicionamiento | 6 | 6 | 0 | 2 | 0 | 0 |
| 10.12 | Sentimiento y volatilidad implícita | 5 | 4 | 4 | 1 | 0 | 1 |
| 10.13 | Renta variable internacional, emergentes y divisa | 3 | 3 | 1 | 0 | 0 | 0 |
| 10.14 | Análisis técnico: lo útil y sus límites | 3 | 3 | 0 | 2 | 0 | 2 |
| 10.15 | Anomalías documentadas y su decaimiento | 4 | 3 | 0 | 1 | 0 | 8 |
| 10.16 | Contabilidad y señales de alerta | 5 | 5 | 3 | 2 | 1 | 3 |
| 10.17 | Riesgos de cola y crisis | 5 | 4 | 4 | 0 | 0 | 1 |
| 10.18 | Fuentes de datos típicas | 1 | 0 | 0 | 0 | 0 | 0 |
| 10.19 | Referencias canónicas (referencias canónicas) | 1 | 0 | 0 | 0 | 0 | 4 |
| 10.20 | Errores frecuentes que debes evitar | 8 | 0 | 0 | 0 | 8 | 0 |
| 10.21 | Subtipos de renta variable: conocimiento para delimitar el ámbito | 6 | 6 | 1 | 3 | 0 | 0 |
| 10.22 | Métricas sectoriales específicas | 10 | 0 | 2 | 6 | 0 | 0 |
| 10.23 | Vínculos entre ciclo macro, tipos y renta variable | 6 | 6 | 2 | 0 | 0 | 2 |
| 10.24 | Eventos corporativos, oferta de acciones y señales de los propios emisores | 6 | 6 | 0 | 0 | 0 | 7 |
| 10.25 | Normativa y fricciones que condicionan la invertibilidad para un minorista europeo | 7 | 6 | 0 | 1 | 0 | 1 |
| 10.26 | Casos históricos de referencia | 7 | 0 | 0 | 0 | 1 | 3 |
| 10.27 | Fuentes por área de los archivos de referencias | 3 | 3 | 0 | 0 | 0 | 0 |
| 10.28 | Inventario de competencias (inventario, no se cuenta) | 19 | 0 | 0 | 0 | 0 | 0 |

### Analista de Tipos de Interés, Crédito y Volatilidad

| Subárea | Título | Elem. | Def. | Fórm. | Umbr. | Tramp. | Ref. |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 10.0 | (antes de la primera subárea) | 1 | 0 | 0 | 0 | 0 | 0 |
| 10.1 | Modelos de la curva de tipos | 5 | 5 | 3 | 0 | 0 | 11 |
| 10.2 | Prima por plazo | 5 | 5 | 0 | 0 | 0 | 2 |
| 10.3 | Pendiente: empinamiento y aplanamiento | 6 | 6 | 3 | 0 | 0 | 2 |
| 10.4 | Duración, DV01, convexidad y futuros | 4 | 3 | 8 | 0 | 0 | 0 |
| 10.5 | Swaps y diferencial swap–bono | 3 | 3 | 2 | 0 | 0 | 0 |
| 10.6 | Inflación implícita | 6 | 6 | 6 | 0 | 0 | 4 |
| 10.7 | CDS e índices de crédito | 6 | 5 | 7 | 2 | 0 | 2 |
| 10.8 | Crédito y ciclo | 5 | 5 | 6 | 0 | 0 | 5 |
| 10.9 | Volatilidad: índices y hechos estilizados | 5 | 5 | 8 | 1 | 0 | 8 |
| 10.10 | Futuros sobre volatilidad y estructura de plazos | 4 | 3 | 2 | 2 | 0 | 2 |
| 10.11 | Productos cotizados de volatilidad y decaimiento | 4 | 3 | 4 | 0 | 0 | 2 |
| 10.12 | Prima de riesgo de volatilidad | 4 | 3 | 2 | 0 | 0 | 4 |
| 10.13 | Correlación | 3 | 3 | 1 | 0 | 0 | 2 |
| 10.14 | Regímenes y relaciones entre factores | 7 | 0 | 0 | 0 | 0 | 2 |
| 10.15 | Fuentes de datos | 1 | 0 | 0 | 0 | 0 | 0 |
| 10.16 | Referencias canónicas (referencias canónicas) | 1 | 0 | 0 | 0 | 0 | 45 |
| 10.17 | Errores frecuentes que debes evitar | 10 | 0 | 0 | 0 | 10 | 0 |
| 10.18 | Política de balance, oferta y restricciones de los intermediarios | 5 | 5 | 1 | 0 | 0 | 2 |
| 10.19 | Instrumentos de crédito estructurado y de volatilidad de tipos | 3 | 3 | 0 | 0 | 0 | 0 |
| 10.20 | Casos históricos de referencia | 8 | 0 | 0 | 0 | 0 | 2 |
| 10.21 | Fuentes por área de los archivos de referencias | 3 | 3 | 0 | 0 | 0 | 0 |
| 10.22 | Inventario de competencias (inventario, no se cuenta) | 12 | 0 | 0 | 0 | 0 | 0 |

### Analista de hipótesis contrarias

| Subárea | Título | Elem. | Def. | Fórm. | Umbr. | Tramp. | Ref. |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 10.1 | Herramientas lógicas y epistemológicas del refutador | 11 | 11 | 3 | 0 | 0 | 3 |
| 10.2 | Catálogo de explicaciones alternativas | 17 | 0 | 0 | 0 | 0 | 0 |
| 10.3 | Catálogo de sesgos a detectar en la tesis | 13 | 0 | 0 | 0 | 13 | 0 |
| 10.4 | Trampas típicas por tipo de activo | 119 | 0 | 1 | 0 | 119 | 13 |
| 10.5 | Trampas transversales de las oportunidades | 6 | 6 | 0 | 0 | 6 | 0 |
| 10.6 | Evaluación de puntuaciones y rankings | 4 | 0 | 0 | 0 | 0 | 0 |
| 10.7 | Referencias canónicas (referencias canónicas) | 17 | 0 | 0 | 0 | 0 | 18 |
| 10.8 | Técnicas estructuradas de refutación | 5 | 5 | 0 | 0 | 0 | 2 |
| 10.9 | Objeciones cuantitativas a la evidencia estadística | 7 | 6 | 0 | 0 | 0 | 1 |
| 10.10 | Expectativas implícitas y tasas base como arma de refutación | 2 | 2 | 0 | 0 | 0 | 0 |
| 10.11 | Casos de consenso equivocado (aprendizaje para el refutador) | 7 | 0 | 0 | 0 | 0 | 4 |
| 10.12 | Fuentes por área de los archivos de referencias | 3 | 3 | 0 | 0 | 0 | 0 |
| 10.13 | Inventario de competencias (inventario, no se cuenta) | 9 | 0 | 0 | 0 | 0 | 0 |

### Analista de Índices Bursátiles

| Subárea | Título | Elem. | Def. | Fórm. | Umbr. | Tramp. | Ref. |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 10.0 | (antes de la primera subárea) | 1 | 0 | 0 | 0 | 0 | 0 |
| 10.1 | Qué es un índice y cómo se construye | 6 | 6 | 0 | 2 | 0 | 1 |
| 10.2 | Proveedores y metodologías principales | 11 | 0 | 2 | 2 | 0 | 2 |
| 10.3 | Clasificación de mercados y reclasificaciones | 3 | 3 | 0 | 0 | 0 | 5 |
| 10.4 | Efecto índice, front-running y costes de la indexación | 5 | 3 | 0 | 0 | 0 | 8 |
| 10.5 | Valoración agregada de índices | 6 | 6 | 3 | 0 | 0 | 4 |
| 10.6 | Descomposición de la rentabilidad esperada (Grinold-Kroner) | 8 | 0 | 1 | 0 | 0 | 2 |
| 10.7 | Asignación geográfica y valor relativo entre índices | 7 | 7 | 0 | 1 | 0 | 10 |
| 10.8 | Divisas en los índices | 4 | 0 | 1 | 0 | 0 | 0 |
| 10.9 | Concentración y amplitud | 4 | 4 | 0 | 0 | 0 | 1 |
| 10.10 | Ponderación por capitalización frente a ponderación igual o fundamental | 4 | 4 | 0 | 0 | 0 | 4 |
| 10.11 | Sesgos sectoriales y de composición de los índices nacionales | 9 | 1 | 1 | 1 | 9 | 0 |
| 10.12 | Ciclo macro relativo | 2 | 2 | 0 | 0 | 0 | 0 |
| 10.13 | Índices de dividendos | 2 | 0 | 0 | 0 | 1 | 0 |
| 10.14 | Índices de volatilidad como indicadores | 4 | 4 | 1 | 2 | 0 | 0 |
| 10.15 | Flujos pasivos y su efecto en los precios | 5 | 4 | 1 | 0 | 0 | 3 |
| 10.16 | Sesgos de medición y de análisis | 3 | 2 | 0 | 0 | 3 | 3 |
| 10.17 | Riesgos de cola de los índices | 3 | 0 | 2 | 0 | 0 | 2 |
| 10.18 | Fuentes de datos típicas | 1 | 0 | 0 | 0 | 0 | 0 |
| 10.19 | Referencias canónicas (referencias canónicas) | 1 | 0 | 0 | 0 | 0 | 7 |
| 10.20 | Errores frecuentes que debes evitar | 6 | 0 | 0 | 0 | 6 | 0 |
| 10.21 | Calendario de eventos de índice y mecánica de los vencimientos | 10 | 2 | 1 | 0 | 0 | 0 |
| 10.22 | Normativa que afecta a la construcción y al acceso | 4 | 4 | 0 | 0 | 0 | 0 |
| 10.23 | Demografía, productividad y rentabilidad a muy largo plazo por región | 4 | 3 | 1 | 0 | 0 | 3 |
| 10.24 | Casos históricos de referencia | 7 | 0 | 0 | 0 | 0 | 4 |
| 10.25 | Fuentes por área de los archivos de referencias | 3 | 3 | 0 | 0 | 0 | 0 |
| 10.26 | Inventario de competencias (inventario, no se cuenta) | 13 | 0 | 0 | 0 | 0 | 0 |

### Analizador de Tendencias de Inversión

| Subárea | Título | Elem. | Def. | Fórm. | Umbr. | Tramp. | Ref. |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 10.0 | (antes de la primera subárea) | 1 | 0 | 0 | 0 | 0 | 0 |
| 10.1 | Macroeconomía global y ciclo | 49 | 20 | 6 | 3 | 0 | 2 |
| 10.2 | Relaciones entre clases de activo | 24 | 2 | 0 | 1 | 0 | 4 |
| 10.3 | Análisis de tendencias | 9 | 8 | 4 | 0 | 0 | 4 |
| 10.4 | Teoría de la decisión bajo incertidumbre | 8 | 8 | 3 | 0 | 0 | 4 |
| 10.5 | Construcción de rankings robustos | 8 | 8 | 0 | 0 | 0 | 0 |
| 10.6 | Sesgos cognitivos del analista y antídotos | 18 | 0 | 0 | 1 | 18 | 4 |
| 10.7 | Gestión de investigaciones y valor de la información | 5 | 4 | 1 | 0 | 0 | 2 |
| 10.8 | Diversificación y concentración | 8 | 8 | 6 | 0 | 0 | 6 |
| 10.9 | Fórmulas de referencia que utilizas (siempre calculadas por HT-03 o el Motor) | 7 | 0 | 9 | 0 | 0 | 0 |
| 10.10 | Fuentes de datos típicas (siempre vía HT-01 o el Buscador) | 1 | 0 | 0 | 0 | 0 | 0 |
| 10.11 | Referencias canónicas (referencias canónicas) | 17 | 0 | 0 | 0 | 0 | 17 |
| 10.12 | Fuerzas seculares y rentabilidades de muy largo plazo | 3 | 2 | 0 | 0 | 0 | 1 |
| 10.13 | Burbujas, crisis y reflexividad | 4 | 4 | 0 | 0 | 0 | 2 |
| 10.14 | Geopolítica, política económica y su traslado a los mercados | 3 | 3 | 0 | 0 | 0 | 2 |
| 10.15 | Agregación de juicios y lectura de la calidad predictiva | 3 | 3 | 0 | 0 | 0 | 3 |
| 10.16 | Calidad de la evidencia y crisis de replicación | 3 | 3 | 0 | 1 | 0 | 1 |
| 10.17 | Mapa de áreas de los archivos de referencias | 9 | 0 | 0 | 0 | 0 | 0 |
| 10.18 | Inventario de competencias (inventario, no se cuenta) | 14 | 0 | 0 | 0 | 0 | 0 |

### Auditor

| Subárea | Título | Elem. | Def. | Fórm. | Umbr. | Tramp. | Ref. |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 10.1 | Auditoría de análisis de inversión | 6 | 6 | 0 | 0 | 1 | 1 |
| 10.2 | Sesgos cognitivos (en el analista y en ti) | 14 | 0 | 0 | 2 | 14 | 1 |
| 10.3 | Sesgos de datos | 8 | 6 | 1 | 0 | 8 | 3 |
| 10.4 | Metodología científica aplicada | 6 | 6 | 3 | 1 | 0 | 4 |
| 10.5 | Estándares de investigación y comunicación | 6 | 2 | 0 | 1 | 0 | 2 |
| 10.6 | Errores estadísticos frecuentes | 13 | 11 | 4 | 0 | 13 | 7 |
| 10.7 | Legibilidad y comunicación al público inexperto | 4 | 3 | 3 | 1 | 0 | 4 |
| 10.8 | Fuentes de opinión y grandes inversores | 3 | 0 | 0 | 0 | 0 | 0 |
| 10.9 | Método de auditoría: muestreo, evidencia y hallazgos | 5 | 5 | 0 | 2 | 0 | 1 |
| 10.10 | Fallos propios de análisis generados por modelos de lenguaje | 5 | 5 | 0 | 0 | 0 | 0 |
| 10.11 | Coherencia entre tipos de activo y escenarios | 3 | 0 | 0 | 0 | 0 | 0 |
| 10.12 | Inventario de competencias (inventario, no se cuenta) | 10 | 0 | 0 | 0 | 0 | 0 |

### Buscador de Fuentes Avanzadas

| Subárea | Título | Elem. | Def. | Fórm. | Umbr. | Tramp. | Ref. |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 10.1 | Evaluación de fuentes de opinión y sus sesgos | 7 | 1 | 1 | 0 | 7 | 8 |
| 10.2 | Verificación: lectura lateral, SIFT y pruebas forenses | 5 | 5 | 0 | 0 | 0 | 4 |
| 10.3 | Grandes inversores: fuentes, retrasos y sesgos | 12 | 0 | 1 | 2 | 12 | 3 |
| 10.4 | Posicionamiento y flujos | 3 | 2 | 4 | 2 | 1 | 2 |
| 10.5 | Datos en cadena | 5 | 4 | 0 | 0 | 0 | 1 |
| 10.6 | Redes sociales: filtros anti-manipulación | 10 | 0 | 0 | 0 | 0 | 5 |
| 10.7 | Bancos centrales, datos oficiales y tiempo | 4 | 4 | 2 | 0 | 0 | 0 |
| 10.8 | Identificadores, archivado y códigos HTTP | 3 | 0 | 0 | 0 | 0 | 0 |
| 10.9 | Canales y operadores de búsqueda | 10 | 0 | 0 | 0 | 0 | 0 |
| 10.10 | Dominio por familias (TF-01 a TF-19) | 20 | 0 | 0 | 0 | 1 | 0 |
| 10.10 bis | Fuentes para los doce tipos de activo | 7 | 0 | 0 | 0 | 0 | 0 |
| 10.11 | Fondo metodológico: criterios vigentes de arranque | 1 | 0 | 0 | 0 | 0 | 0 |
| 10.12 | Extracción de pronósticos medibles de fuentes de opinión | 4 | 0 | 0 | 0 | 0 | 0 |
| 10.13 | Lectura de comunicación de bancos centrales y de empresas | 3 | 3 | 0 | 0 | 0 | 0 |
| 10.14 | Fuentes en otros idiomas y regiones | 2 | 0 | 0 | 0 | 0 | 0 |
| 10.15 | Inventario de competencias (inventario, no se cuenta) | 11 | 0 | 0 | 0 | 0 | 0 |

### Coordinador de Peticiones y Consultas

| Subárea | Título | Elem. | Def. | Fórm. | Umbr. | Tramp. | Ref. |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 10.1 | Gestión de colas y prioridades | 5 | 1 | 6 | 1 | 1 | 1 |
| 10.2 | Programación de ciclos: cron, zonas horarias y festivos de mercado | 31 | 3 | 13 | 0 | 1 | 0 |
| 10.3 | Triaje: criterios finos | 1 | 0 | 0 | 0 | 0 | 0 |
| 10.4 | Recuperación de información en la memoria del bloque | 17 | 0 | 0 | 0 | 0 | 0 |
| 10.5 | Cómo responder con trazabilidad | 11 | 1 | 0 | 0 | 0 | 0 |
| 10.6 | Asignación de nivel y presupuesto: ejemplos razonados | 8 | 0 | 3 | 0 | 0 | 0 |
| 10.7 | Gestión de configuración F10 (régimen «Servicio») | 11 | 0 | 0 | 2 | 0 | 0 |
| 10.8 | Registro en F5 | 7 | 7 | 0 | 0 | 0 | 0 |
| 10.9 | Comunicación con el Broker | 7 | 0 | 0 | 0 | 0 | 0 |
| 10.10 | Vocabulario de confianza | 6 | 0 | 0 | 0 | 0 | 0 |
| 10.11 | Conceptos del bloque que el Broker suele preguntar | 11 | 11 | 0 | 7 | 0 | 0 |
| 10.12 | Glosario financiero básico para entender al Broker | 72 | 0 | 8 | 0 | 0 | 0 |
| 10.13 | Delimitación de peticiones ambiguas | 4 | 4 | 0 | 0 | 0 | 0 |
| 10.14 | Frontera regulatoria y protección de datos | 3 | 3 | 0 | 0 | 0 | 0 |
| 10.15 | Gestión del nivel de servicio | 4 | 4 | 0 | 0 | 0 | 0 |
| 10.16 | Inventario de competencias (inventario, no se cuenta) | 9 | 0 | 0 | 0 | 0 | 0 |

### Curador de Evidencia

| Subárea | Título | Elem. | Def. | Fórm. | Umbr. | Tramp. | Ref. |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 10.1 | Deduplicación | 7 | 7 | 9 | 5 | 0 | 2 |
| 10.2 | Raíces y cadenas de citación | 4 | 4 | 0 | 0 | 0 | 1 |
| 10.3 | Normalización temporal y `conocible_desde` | 13 | 0 | 3 | 0 | 1 | 0 |
| 10.4 | Revisiones de datos macro y vintages | 4 | 0 | 1 | 0 | 0 | 3 |
| 10.5 | Unidades, escalas y divisas | 8 | 6 | 5 | 0 | 0 | 0 |
| 10.6 | Detección de manipulación y contenido coordinado | 9 | 0 | 0 | 0 | 0 | 0 |
| 10.7 | Tratamiento de la «fuente retirada» | 8 | 0 | 0 | 0 | 0 | 0 |
| 10.8 | Escritura serializada con varias instancias | 6 | 6 | 0 | 0 | 0 | 0 |
| 10.9 | Modelado de afirmaciones y dirección de la evidencia | 4 | 4 | 1 | 0 | 0 | 0 |
| 10.10 | Independencia más allá de la raíz | 4 | 4 | 0 | 0 | 0 | 0 |
| 10.11 | Identificadores, estándares y procedencia | 5 | 5 | 0 | 0 | 0 | 0 |
| 10.12 | Contenido sintético y precedentes de manipulación con efecto en mercados | 2 | 2 | 0 | 0 | 0 | 0 |
| 10.13 | Calidad de datos y controles numéricos | 3 | 3 | 1 | 0 | 0 | 0 |
| 10.14 | Fuentes por área de los archivos de referencias | 3 | 3 | 0 | 0 | 0 | 0 |
| 10.15 | Inventario de competencias (inventario, no se cuenta) | 10 | 0 | 0 | 0 | 0 | 0 |

### Documentador para el Analizador

| Subárea | Título | Elem. | Def. | Fórm. | Umbr. | Tramp. | Ref. |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 10.1 | Bibliometría y evaluación de fuentes académicas | 7 | 2 | 2 | 2 | 0 | 14 |
| 10.2 | Retractaciones, correcciones y avisos | 3 | 3 | 0 | 0 | 0 | 1 |
| 10.3 | Bases, repositorios y operadores de búsqueda | 13 | 0 | 2 | 0 | 0 | 1 |
| 10.4 | Identificadores persistentes y archivado | 3 | 3 | 0 | 1 | 0 | 0 |
| 10.5 | Códigos HTTP y su tratamiento | 12 | 0 | 0 | 0 | 0 | 0 |
| 10.6 | Verificación de afirmaciones: lectura lateral y SIFT | 4 | 4 | 0 | 0 | 0 | 2 |
| 10.7 | Sesgos de la literatura y conflictos de interés | 1 | 0 | 0 | 0 | 1 | 4 |
| 10.8 | Dominio temático por taxonomía (TA-01 a TA-23) | 25 | 0 | 0 | 0 | 2 | 186 |
| 10.8 bis | Literatura de referencia de los tipos de activo de V5.0 (referencias canónicas) | 6 | 0 | 0 | 0 | 1 | 26 |
| 10.9 | Fondo metodológico: criterios vigentes de arranque | 1 | 0 | 0 | 0 | 0 | 7 |
| 10.10 | Lectura crítica rápida de un trabajo empírico | 1 | 0 | 0 | 0 | 0 | 0 |
| 10.11 | Síntesis de literatura y metaanálisis | 3 | 0 | 0 | 0 | 0 | 2 |
| 10.12 | Integridad de las referencias y derechos de uso | 4 | 4 | 0 | 0 | 0 | 1 |
| 10.13 | Inventario de competencias (inventario, no se cuenta) | 9 | 0 | 0 | 0 | 0 | 0 |

### Documentador para el Motor de Cálculo Avanzado

| Subárea | Título | Elem. | Def. | Fórm. | Umbr. | Tramp. | Ref. |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 10.1 | Evaluación de fuentes metodológicas | 5 | 1 | 1 | 0 | 0 | 12 |
| 10.2 | Documentación de software y reproducibilidad | 4 | 4 | 1 | 0 | 0 | 6 |
| 10.3 | Bases y operadores de búsqueda para métodos | 10 | 0 | 0 | 0 | 0 | 0 |
| 10.4 | Identificadores, archivado y códigos HTTP | 1 | 0 | 0 | 0 | 0 | 0 |
| 10.5 | Verificación de afirmaciones metodológicas | 1 | 0 | 0 | 0 | 0 | 2 |
| 10.6 | Dominio temático (TM-01 a TM-18) | 18 | 0 | 18 | 1 | 0 | 181 |
| 10.7 | Fondo metodológico: criterios vigentes de arranque | 1 | 0 | 0 | 0 | 0 | 0 |
| 10.8 | Canónicas y advertencias de TM-15 a TM-18 (complemento de 10.6) | 4 | 4 | 0 | 0 | 0 | 27 |
| 10.9 | Documentación implementable para el Motor (CT-20) | 4 | 4 | 0 | 0 | 0 | 2 |
| 10.10 | Inventario de competencias (inventario, no se cuenta) | 7 | 0 | 0 | 0 | 0 | 0 |

### Evaluador de Previsiones y Aprendizaje

| Subárea | Título | Elem. | Def. | Fórm. | Umbr. | Tramp. | Ref. |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 10.1 | Resolución con datos en tiempo real (vintages) | 6 | 6 | 0 | 0 | 0 | 2 |
| 10.2 | Reglas de puntuación propias | 11 | 10 | 11 | 1 | 0 | 7 |
| 10.3 | Descomposición de Murphy | 6 | 2 | 6 | 0 | 0 | 2 |
| 10.4 | Curvas de fiabilidad y ECE | 6 | 5 | 8 | 4 | 0 | 5 |
| 10.5 | Brier skill score con intervalos bootstrap | 5 | 4 | 5 | 0 | 1 | 4 |
| 10.6 | Comparación de precisión predictiva: Diebold-Mariano y HLN | 5 | 4 | 5 | 1 | 0 | 6 |
| 10.7 | Pruebas binomiales de acierto | 4 | 4 | 7 | 0 | 0 | 0 |
| 10.8 | Rentabilidad relativa y ajustada por riesgo | 7 | 4 | 9 | 0 | 0 | 8 |
| 10.9 | Tamaño muestral y potencia | 4 | 4 | 11 | 1 | 0 | 3 |
| 10.10 | Comparaciones múltiples y contracción | 4 | 4 | 7 | 0 | 0 | 1 |
| 10.11 | Sobreajuste en la recalibración | 6 | 6 | 1 | 0 | 0 | 5 |
| 10.12 | Decaimiento de señales y cambios de régimen | 4 | 4 | 3 | 1 | 0 | 5 |
| 10.13 | Sesgos de evaluación | 11 | 0 | 0 | 0 | 11 | 0 |
| 10.14 | Calibración del juicio (humano y de modelos de lenguaje) | 4 | 4 | 1 | 0 | 0 | 5 |
| 10.15 | Aprendizaje organizativo | 7 | 7 | 0 | 0 | 0 | 5 |
| 10.16 | Meta-aprendizaje y bandits | 8 | 7 | 8 | 0 | 0 | 5 |
| 10.17 | Evaluación de rankings y selección | 4 | 3 | 2 | 0 | 0 | 1 |
| 10.18 | Fuentes de opinión | 2 | 0 | 0 | 0 | 0 | 0 |
| 10.19 | Calibración de presupuestos | 2 | 1 | 0 | 0 | 0 | 0 |
| 10.20 | Complementos de evaluación y certificación | 6 | 6 | 2 | 1 | 0 | 2 |
| 10.21 | Inventario de competencias (inventario, no se cuenta) | 11 | 0 | 0 | 0 | 0 | 0 |

### MC-01 Fundamentos cuantitativos y estadística

| Subárea | Título | Elem. | Def. | Fórm. | Umbr. | Tramp. | Ref. |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 10.1 | Rentabilidades y divisas | 5 | 4 | 14 | 0 | 0 | 0 |
| 10.2 | Valor temporal, TIR y crecimiento | 6 | 4 | 15 | 1 | 0 | 0 |
| 10.3 | Métricas ajustadas por riesgo (cálculo; la inferencia, en 10.6) | 7 | 0 | 8 | 0 | 0 | 0 |
| 10.4 | Métricas de fondos privados (perfiles PERF-PRV/PERF-ALT) | 4 | 0 | 6 | 2 | 1 | 3 |
| 10.5 | Probabilidad aplicada | 9 | 0 | 7 | 1 | 0 | 0 |
| 10.6 | Estadística descriptiva, robusta e inferencia | 19 | 0 | 20 | 4 | 0 | 2 |
| 10.7 | Índices, puntuaciones y concentración | 7 | 7 | 3 | 3 | 0 | 0 |
| 10.8 | Trampas frecuentes de tu dominio | 10 | 0 | 0 | 0 | 10 | 0 |
| 10.9 | Referencias canónicas (referencias canónicas) | 1 | 0 | 0 | 0 | 0 | 15 |
| 10.10 | Convenciones monetarias y tipo real a corto (MON-YLD-001, MON-REAL-001; área 67) | 4 | 0 | 7 | 0 | 0 | 0 |
| 10.11 | Diferencia y error de seguimiento por categoría (FON-TD-001; área 56) | 2 | 0 | 3 | 0 | 2 | 0 |
| 10.12 | Números índice y empalme de series (área 23) | 2 | 0 | 3 | 0 | 0 | 0 |
| 10.13 | Muestreo, sesgos y datos ausentes (área 27) | 2 | 0 | 0 | 0 | 2 | 3 |
| 10.14 | Métricas de mercado y microestructura (área 33) | 2 | 0 | 6 | 0 | 0 | 3 |
| 10.15 | Complementos numéricos y probabilísticos (áreas 1, 3 y 41) | 3 | 0 | 6 | 2 | 0 | 0 |
| 10.16 | Reconstrucción de puntuaciones (SCORE-RK-001; área 37) | 1 | 0 | 1 | 1 | 0 | 0 |
| 10.17 | Inventario de competencias (inventario, no se cuenta) | 6 | 0 | 0 | 0 | 0 | 0 |

### MC-02 Series temporales, tendencias, regímenes y volatilidad

| Subárea | Título | Elem. | Def. | Fórm. | Umbr. | Tramp. | Ref. |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 10.1 | Preparación de series | 4 | 4 | 2 | 0 | 0 | 0 |
| 10.2 | Estacionariedad y dependencia | 5 | 4 | 6 | 0 | 0 | 0 |
| 10.3 | Modelos de pronóstico univariante | 5 | 5 | 8 | 1 | 0 | 1 |
| 10.4 | Tendencias y momentum | 7 | 7 | 16 | 3 | 0 | 1 |
| 10.5 | Rupturas estructurales | 6 | 2 | 10 | 0 | 1 | 1 |
| 10.6 | Regímenes | 6 | 6 | 7 | 3 | 0 | 1 |
| 10.7 | Volatilidad | 8 | 8 | 17 | 4 | 0 | 1 |
| 10.8 | Mínimos de datos por método (por defecto; la ficha manda) | 11 | 0 | 0 | 0 | 0 | 0 |
| 10.9 | Desuavizado de rentabilidades tasadas (INM, ALT; ficha de MC-09, soporte de MC-02) | 3 | 2 | 7 | 0 | 1 | 2 |
| 10.10 | Trampas frecuentes de tu dominio | 1 | 0 | 1 | 0 | 1 | 0 |
| 10.11 | Referencias canónicas (referencias canónicas) | 1 | 0 | 0 | 0 | 0 | 34 |
| 10.12 | Inventarios frente a la norma estacional (CMD-INV-001; área 52) | 3 | 0 | 0 | 1 | 0 | 1 |
| 10.13 | Flujos de vehículos y de criptoactivos (FON-FLOW-001, CHR-FLOW-001; áreas 54, 65) | 3 | 0 | 3 | 0 | 1 | 3 |
| 10.14 | Ciclos, puntos de giro y frecuencia (área 10) | 3 | 0 | 1 | 4 | 0 | 2 |
| 10.15 | Complementos de volatilidad y pronóstico (áreas 6 y 17) | 3 | 0 | 2 | 0 | 0 | 2 |
| 10.16 | Inventario de competencias (inventario, no se cuenta) | 10 | 0 | 0 | 0 | 0 | 0 |

### MC-03 Econometría, causalidad y macroeconomía cuantitativa

| Subárea | Título | Elem. | Def. | Fórm. | Umbr. | Tramp. | Ref. |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 10.1 | Regresión lineal y diagnósticos | 9 | 9 | 12 | 6 | 0 | 3 |
| 10.2 | Paneles | 1 | 0 | 1 | 1 | 0 | 3 |
| 10.3 | Sistemas: VAR, cointegración y VECM | 7 | 7 | 10 | 2 | 0 | 2 |
| 10.4 | Causalidad: lo que se puede y lo que no se puede afirmar | 7 | 7 | 5 | 1 | 0 | 5 |
| 10.5 | Dependencia multivariante | 6 | 6 | 12 | 3 | 0 | 2 |
| 10.6 | Macroeconomía cuantitativa y paridades | 13 | 1 | 12 | 2 | 0 | 2 |
| 10.7 | Trampas frecuentes de tu dominio | 1 | 0 | 0 | 0 | 1 | 0 |
| 10.8 | Referencias canónicas (referencias canónicas) | 1 | 0 | 0 | 0 | 0 | 34 |
| 10.9 | Paridad cubierta, base y carry cambiario (FX-CARRY-001, FX-PPA-001; área 51) | 3 | 0 | 1 | 0 | 0 | 4 |
| 10.10 | Eventos de índice (IDX-REB-001; área 64) | 2 | 0 | 1 | 1 | 0 | 3 |
| 10.11 | Complementos macro (área 19) | 4 | 0 | 2 | 0 | 0 | 1 |
| 10.12 | Covarianzas de alta dimensión y correlación robusta (área 18) | 2 | 0 | 2 | 1 | 0 | 0 |
| 10.13 | Clima cuantitativo (área 57, parte econométrica) | 2 | 0 | 2 | 0 | 0 | 1 |
| 10.14 | Inventario de competencias (inventario, no se cuenta) | 9 | 0 | 0 | 0 | 0 | 0 |

### MC-04 Crecimiento, difusión y prospectiva cuantitativa

| Subárea | Título | Elem. | Def. | Fórm. | Umbr. | Tramp. | Ref. |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 10.1 | Curvas de crecimiento | 8 | 2 | 12 | 1 | 1 | 0 |
| 10.2 | Difusión de innovaciones (Bass) y sustitución | 5 | 5 | 9 | 0 | 0 | 4 |
| 10.3 | Curvas de aprendizaje y costes | 4 | 3 | 7 | 0 | 1 | 2 |
| 10.4 | Tamaño de mercado y economía industrial | 5 | 5 | 3 | 0 | 0 | 0 |
| 10.5 | Escenarios cuantitativos | 7 | 7 | 5 | 0 | 0 | 0 |
| 10.6 | Sensibilidad | 5 | 5 | 6 | 1 | 0 | 0 |
| 10.7 | Vista exterior y tasas base | 3 | 3 | 0 | 0 | 0 | 2 |
| 10.8 | Sistemas dinámicos (bajo petición) | 1 | 0 | 2 | 1 | 0 | 0 |
| 10.9 | Trampas frecuentes de tu dominio | 1 | 0 | 0 | 0 | 1 | 0 |
| 10.10 | Referencias canónicas (referencias canónicas) | 1 | 0 | 0 | 0 | 0 | 19 |
| 10.11 | Análisis morfológico, consistencia y señales tempranas (área 13) | 2 | 0 | 0 | 0 | 0 | 2 |
| 10.12 | Energía, recursos y escenarios de referencia (áreas 22 y 57) | 2 | 0 | 2 | 0 | 0 | 1 |
| 10.13 | Cadenas de valor, capacidad e innovación (áreas 20 y 21) | 2 | 0 | 0 | 1 | 0 | 2 |
| 10.14 | Rentabilidad esperada a largo plazo por bloques (área 13, soporte) | 1 | 0 | 1 | 0 | 0 | 0 |
| 10.15 | Inventario de competencias (inventario, no se cuenta) | 11 | 0 | 0 | 0 | 0 | 0 |

### MC-05 Simulación estocástica y escenarios

| Subárea | Título | Elem. | Def. | Fórm. | Umbr. | Tramp. | Ref. |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 10.1 | Generadores, semillas y reproducibilidad | 3 | 0 | 1 | 0 | 0 | 0 |
| 10.2 | Error de Monte Carlo y tamaño de muestra | 3 | 0 | 6 | 1 | 3 | 0 |
| 10.3 | Procesos estocásticos | 9 | 0 | 16 | 1 | 0 | 0 |
| 10.4 | Dependencia y cópulas | 3 | 2 | 15 | 0 | 0 | 1 |
| 10.5 | Reducción de varianza | 7 | 0 | 5 | 0 | 0 | 0 |
| 10.6 | Bootstrap con dependencia y simulación histórica | 5 | 2 | 2 | 0 | 0 | 5 |
| 10.7 | Salidas de una simulación | 5 | 5 | 2 | 0 | 0 | 0 |
| 10.8 | Teoría de la información y detección de cambios de distribución (soporte) | 5 | 0 | 6 | 4 | 0 | 0 |
| 10.9 | Trampas frecuentes de tu dominio | 1 | 0 | 0 | 0 | 1 | 0 |
| 10.10 | Referencias canónicas (referencias canónicas) | 1 | 0 | 0 | 0 | 0 | 21 |
| 10.11 | Escenarios por horizonte (SCN-H-001; área 13) | 4 | 0 | 4 | 0 | 0 | 1 |
| 10.12 | Simulación invitada de vehículos apalancados (FON-LEV-001) | 1 | 0 | 5 | 0 | 0 | 0 |
| 10.13 | Complementos de muestreo multivariante y eficiencia (área 14) | 3 | 0 | 3 | 0 | 0 | 1 |
| 10.14 | Inventario de competencias (inventario, no se cuenta) | 11 | 0 | 0 | 0 | 0 | 0 |

### MC-06 Aprendizaje automático y predicción calibrada

| Subárea | Título | Elem. | Def. | Fórm. | Umbr. | Tramp. | Ref. |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 10.1 | Planteamiento del problema predictivo | 5 | 5 | 3 | 0 | 0 | 2 |
| 10.2 | Ingeniería de variables sin fuga | 5 | 5 | 1 | 0 | 0 | 0 |
| 10.3 | Validación apropiada al tiempo | 7 | 7 | 1 | 1 | 0 | 2 |
| 10.4 | Modelos supervisados y valores por defecto | 13 | 2 | 6 | 2 | 1 | 2 |
| 10.5 | Calibración de probabilidades e intervalos | 7 | 5 | 4 | 3 | 0 | 4 |
| 10.6 | Métricas de evaluación interna | 5 | 5 | 6 | 0 | 0 | 3 |
| 10.7 | Aprendizaje no supervisado | 7 | 7 | 3 | 2 | 0 | 1 |
| 10.8 | Interpretabilidad | 4 | 1 | 0 | 0 | 0 | 1 |
| 10.9 | Deriva y estabilidad | 4 | 1 | 1 | 2 | 0 | 1 |
| 10.10 | Tamaños mínimos y potencia | 4 | 2 | 2 | 1 | 0 | 1 |
| 10.11 | Soporte de métricas textuales estructuradas | 1 | 0 | 0 | 1 | 0 | 0 |
| 10.12 | Trampas frecuentes | 1 | 0 | 0 | 0 | 1 | 0 |
| 10.13 | Cuándo no usar aprendizaje automático | 1 | 0 | 0 | 1 | 0 | 0 |
| 10.14 | Referencias canónicas (referencias canónicas) | 1 | 0 | 0 | 0 | 0 | 23 |
| 10.15 | Complementos de modelización (áreas 16 y 17) | 7 | 7 | 1 | 0 | 0 | 3 |
| 10.16 | Inventario de competencias (inventario, no se cuenta) | 12 | 0 | 0 | 0 | 0 | 0 |

### MC-07 Optimización, decisión y riesgo

| Subárea | Título | Elem. | Def. | Fórm. | Umbr. | Tramp. | Ref. |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 10.1 | Volatilidad y escalado | 3 | 1 | 6 | 1 | 0 | 0 |
| 10.2 | VaR y Expected Shortfall | 8 | 7 | 17 | 2 | 0 | 2 |
| 10.3 | Teoría de valores extremos | 5 | 4 | 5 | 3 | 0 | 0 |
| 10.4 | Drawdown y métricas de trayectoria | 5 | 2 | 8 | 0 | 0 | 1 |
| 10.5 | Métricas de asimetría para la puntuación A | 6 | 4 | 6 | 2 | 0 | 0 |
| 10.6 | Riesgo de liquidez | 3 | 2 | 3 | 0 | 0 | 1 |
| 10.7 | Pruebas de estrés y escenarios adversos | 4 | 3 | 0 | 0 | 0 | 0 |
| 10.8 | Dependencia, concentración y apuestas independientes | 3 | 2 | 7 | 0 | 0 | 0 |
| 10.9 | Optimización (apoyo de cálculo) | 9 | 9 | 3 | 4 | 0 | 3 |
| 10.10 | Teoría de la decisión y valor de la información | 6 | 4 | 2 | 0 | 0 | 2 |
| 10.11 | Redes y contagio (nivel III, bajo petición) | 1 | 0 | 0 | 0 | 0 | 2 |
| 10.12 | Trampas frecuentes | 1 | 0 | 0 | 0 | 1 | 0 |
| 10.13 | Referencias canónicas (referencias canónicas) | 1 | 0 | 0 | 0 | 0 | 24 |
| 10.14 | Complementos de riesgo, optimización y decisión (áreas 24, 25 y 40) | 6 | 5 | 6 | 0 | 0 | 4 |
| 10.15 | Inventario de competencias (inventario, no se cuenta) | 11 | 0 | 0 | 0 | 0 | 0 |

### MC-08 Auditoría cuantitativa independiente

| Subárea | Título | Elem. | Def. | Fórm. | Umbr. | Tramp. | Ref. |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 10.1 | Reproducibilidad y sus niveles | 4 | 3 | 0 | 0 | 0 | 0 |
| 10.2 | Fuentes habituales de discrepancia (lista de comprobación) | 13 | 13 | 0 | 0 | 0 | 1 |
| 10.3 | Comparación de resultados no escalares | 5 | 5 | 0 | 0 | 0 | 0 |
| 10.4 | Incertidumbre y su declaración | 3 | 2 | 1 | 0 | 0 | 0 |
| 10.5 | Auditoría de evaluaciones y resoluciones (solicitudes del Evaluador) | 4 | 4 | 0 | 0 | 0 | 0 |
| 10.6 | Verificación de calidad periódica | 9 | 1 | 9 | 0 | 0 | 0 |
| 10.7 | Trampas frecuentes | 1 | 0 | 0 | 0 | 1 | 0 |
| 10.8 | Referencias canónicas (referencias canónicas) | 1 | 0 | 0 | 0 | 0 | 11 |
| 10.9 | Exactitud numérica y referencias certificadas (áreas 30 y 31) | 3 | 0 | 2 | 0 | 0 | 1 |
| 10.10 | Muestreo y seguimiento de la verificación periódica (áreas 29 y 42) | 3 | 1 | 3 | 0 | 0 | 0 |
| 10.11 | Disciplina del auditor (área 29) | 2 | 0 | 0 | 0 | 0 | 0 |
| 10.12 | Inventario de competencias (inventario, no se cuenta) | 7 | 0 | 0 | 0 | 0 | 0 |

### MC-09 Valoración y modelos de precios de activos

| Subárea | Título | Elem. | Def. | Fórm. | Umbr. | Tramp. | Ref. |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 10.1 | Descuento de flujos (DCF) | 8 | 6 | 9 | 1 | 0 | 0 |
| 10.2 | Dividendos y rentabilidad implícita | 3 | 3 | 8 | 0 | 0 | 0 |
| 10.3 | Múltiplos y valoración relativa | 5 | 4 | 4 | 1 | 1 | 0 |
| 10.4 | Prima de riesgo implícita (ficha ACC-ERP-001) | 3 | 3 | 5 | 0 | 0 | 1 |
| 10.5 | Bonos: precio, rendimiento y sensibilidades (FIR-PRICE-001) | 7 | 6 | 9 | 0 | 0 | 0 |
| 10.6 | Estructura temporal (FIR-CURVE-001) | 6 | 5 | 3 | 3 | 1 | 4 |
| 10.7 | Carry y rolldown (FIR-CARRY-001) | 4 | 3 | 5 | 0 | 0 | 0 |
| 10.8 | Crédito (FIR-SPREAD-001, FIR-CRED-001) | 5 | 4 | 11 | 1 | 0 | 1 |
| 10.9 | Opciones y volatilidad implícita (DER-OPT-001) | 7 | 5 | 16 | 1 | 0 | 0 |
| 10.10 | Modelos factoriales y momentum (ACC-FACT-001, ACC-MOM-001, FX-MOM-001, ALT-HF-001) | 7 | 6 | 3 | 1 | 0 | 5 |
| 10.11 | Inmobiliario (REI-NAV-001, REI-CAP-001, REI-FFO-001, REI-LEV-001) | 6 | 5 | 10 | 3 | 0 | 0 |
| 10.12 | Criptoactivos (CHR-ONCHAIN-001, CHR-FUND-001, CHR-TOKEN-001) | 7 | 6 | 8 | 4 | 0 | 0 |
| 10.13 | Mercados privados y alternativos (PRV-PME-001, PRV-CF-001, ALT-DESMOOTH-001, ALT-HF-001, ALT-AUC-001) | 6 | 6 | 7 | 1 | 0 | 2 |
| 10.14 | Divisas (FX-MOM-001; las fichas de paridades FX-PPA-001, FX-CARRY-001 y FX-BEER-001 son de MC-03, con este conocimiento como base) | 4 | 3 | 2 | 1 | 0 | 3 |
| 10.15 | Materias primas (CMD-CURVE-001, CMD-RETDEC-001, CMD-REAL-001) | 5 | 3 | 3 | 0 | 0 | 5 |
| 10.16 | Índices bursátiles (IDX-ERP-001, IDX-REL-001; IDX-CONC-001 es de MC-01 e IDX-REB-001 de MC-03) | 5 | 5 | 7 | 1 | 0 | 4 |
| 10.17 | Vehículos de inversión colectiva (FON-DISC-001, FON-LEV-001; FON-FLOW-001 es de MC-02 y FON-TD-001 de MC-01) | 4 | 3 | 11 | 0 | 0 | 5 |
| 10.18 | Derivados como fuente de oportunidad (DER-VRP-001, DER-SKEW-001, DER-TERM-001, DER-ROLL-001) | 4 | 4 | 10 | 0 | 0 | 5 |
| 10.19 | Monetario y liquidez (MON-EXP-001, MON-FIX-001; conversiones de MON-YLD-001 y MON-REAL-001 en MC-01 con este conocimiento como base) | 4 | 4 | 10 | 0 | 0 | 2 |
| 10.20 | Tipos, crédito y volatilidad como factores (TCV-SLOPE-001, TCV-BEI-001, TCV-CDS-001, TCV-VIXTS-001, TCV-TP-001) | 5 | 5 | 10 | 2 | 0 | 7 |
| 10.21 | Trampas frecuentes | 1 | 0 | 0 | 0 | 1 | 0 |
| 10.22 | Referencias canónicas (referencias canónicas) | 1 | 0 | 0 | 0 | 0 | 75 |
| 10.23 | Complementos de valoración (áreas 44, 48 y 55) | 5 | 5 | 6 | 0 | 0 | 1 |
| 10.24 | Inventario de competencias (inventario, no se cuenta) | 7 | 0 | 0 | 0 | 0 | 0 |

### MC-10 Evaluación predictiva y backtesting

| Subárea | Título | Elem. | Def. | Fórm. | Umbr. | Tramp. | Ref. |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 10.1 | Reglas de puntuación propias | 7 | 5 | 13 | 1 | 0 | 2 |
| 10.2 | Pronósticos de distribución, cuantiles e intervalos | 4 | 3 | 9 | 0 | 0 | 0 |
| 10.3 | Acierto direccional | 3 | 2 | 12 | 0 | 0 | 0 |
| 10.4 | Comparación de exactitud predictiva | 5 | 3 | 8 | 2 | 0 | 5 |
| 10.5 | Calibración | 4 | 4 | 12 | 7 | 0 | 1 |
| 10.6 | Incertidumbre de las métricas | 3 | 3 | 2 | 1 | 0 | 1 |
| 10.7 | Backtesting de medidas de riesgo (BT-VAR-001) | 4 | 4 | 6 | 1 | 0 | 2 |
| 10.8 | Backtesting de estrategias y señales sin sesgos | 10 | 8 | 11 | 4 | 10 | 5 |
| 10.9 | Resolución de pronósticos sin *look-ahead* | 7 | 7 | 0 | 0 | 0 | 0 |
| 10.10 | Fiabilidad de fuentes de opinión (12.5) | 4 | 1 | 3 | 0 | 0 | 0 |
| 10.11 | Evaluación de las opciones del top-3 | 3 | 0 | 0 | 0 | 0 | 0 |
| 10.12 | Trampas frecuentes | 1 | 0 | 0 | 0 | 1 | 0 |
| 10.13 | Referencias canónicas (referencias canónicas) | 1 | 0 | 0 | 0 | 0 | 28 |
| 10.14 | Complementos de verificación (áreas 58–60) | 6 | 6 | 5 | 1 | 0 | 5 |
| 10.15 | Inventario de competencias (inventario, no se cuenta) | 10 | 0 | 0 | 0 | 0 | 0 |

### Motor de Cálculo Avanzado para el Analizador de Tendencias de Inversión

| Subárea | Título | Elem. | Def. | Fórm. | Umbr. | Tramp. | Ref. |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 10.0 | (antes de la primera subárea) | 1 | 0 | 0 | 0 | 0 | 0 |
| 10.1 | Convenciones y cálculo financiero (MC-01) | 7 | 7 | 14 | 0 | 0 | 2 |
| 10.2 | Estadística e inferencia (MC-01) | 14 | 0 | 16 | 5 | 0 | 1 |
| 10.3 | Series temporales, tendencias y regímenes (MC-02) | 26 | 0 | 28 | 4 | 2 | 16 |
| 10.4 | Volatilidad (MC-02) | 16 | 5 | 44 | 8 | 0 | 12 |
| 10.5 | Econometría y causalidad (MC-03) | 14 | 4 | 19 | 3 | 0 | 17 |
| 10.6 | Valoración y precios de activos (MC-09) | 12 | 1 | 63 | 5 | 0 | 5 |
| 10.7 | Modelos factoriales (MC-09) | 4 | 3 | 7 | 3 | 0 | 8 |
| 10.8 | Riesgo (MC-07) | 15 | 2 | 22 | 3 | 0 | 7 |
| 10.9 | Carteras (MC-07) | 6 | 6 | 18 | 0 | 0 | 7 |
| 10.10 | Simulación (MC-05) | 8 | 8 | 10 | 1 | 0 | 4 |
| 10.11 | Aprendizaje automático (MC-06) | 5 | 4 | 0 | 0 | 0 | 1 |
| 10.12 | Evaluación predictiva (MC-10) | 15 | 4 | 22 | 4 | 0 | 8 |
| 10.13 | Backtesting sin sesgos (MC-10) | 7 | 5 | 13 | 4 | 7 | 6 |
| 10.14 | Métricas específicas por tipo de activo (MC-09; aritmética de flujos en MC-01) | 31 | 0 | 38 | 4 | 0 | 9 |
| 10.15 | Calidad de datos y precisión numérica (STC-1, STC-2) | 2 | 0 | 3 | 2 | 0 | 0 |
| 10.16 | Referencias canónicas (respaldo en F8 vía CT-20) (referencias canónicas) | 1 | 0 | 0 | 0 | 0 | 51 |
| 10.17 | Propagación y comunicación de la incertidumbre (áreas 41 y 43) | 4 | 2 | 1 | 0 | 0 | 0 |
| 10.18 | Ampliaciones de conocimiento de los módulos (03/11/2026) | 1 | 0 | 0 | 0 | 0 | 0 |
| 10.19 | Inventario de competencias (inventario, no se cuenta) | 8 | 0 | 0 | 0 | 0 | 0 |

### Orquestador técnico

| Subárea | Título | Elem. | Def. | Fórm. | Umbr. | Tramp. | Ref. |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 10.1 | Control de calidad de procesos | 9 | 7 | 7 | 0 | 1 | 1 |
| 10.2 | Comprobaciones deterministas: diseño y uso | 7 | 6 | 2 | 3 | 0 | 0 |
| 10.3 | Teoría de colas aplicada | 11 | 10 | 11 | 1 | 1 | 3 |
| 10.4 | Gestión de presupuestos de cómputo | 5 | 4 | 4 | 2 | 0 | 1 |
| 10.5 | Gobernanza de modelos | 6 | 5 | 1 | 0 | 0 | 0 |
| 10.6 | Medición de eficacia de guías | 3 | 1 | 0 | 0 | 0 | 0 |
| 10.7 | Clasificación de severidades y gestión de incidencias | 4 | 4 | 1 | 1 | 0 | 1 |
| 10.8 | Redacción de guías accionables | 5 | 3 | 0 | 1 | 0 | 1 |
| 10.9 | Salud del conocimiento (CT-21) | 3 | 2 | 0 | 1 | 0 | 1 |
| 10.10 | Seguridad de sistemas de agentes basados en modelos de lenguaje | 3 | 3 | 0 | 0 | 0 | 0 |
| 10.11 | Observabilidad, muestreo y cambios | 4 | 2 | 1 | 1 | 0 | 1 |
| 10.12 | Inventario de competencias (inventario, no se cuenta) | 10 | 0 | 0 | 0 | 0 | 0 |

### Redactor y Diseñador de Informes

| Subárea | Título | Elem. | Def. | Fórm. | Umbr. | Tramp. | Ref. |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 10.1 | Redacción técnica financiera para el Broker | 22 | 3 | 0 | 0 | 1 | 1 |
| 10.2 | Lenguaje llano en español: reglas concretas | 28 | 9 | 0 | 1 | 0 | 3 |
| 10.3 | Términos financieros: traducción llana y analogías | 65 | 0 | 0 | 0 | 0 | 0 |
| 10.4 | Legibilidad: índice de Fernández-Huerta | 29 | 6 | 13 | 3 | 0 | 4 |
| 10.5 | Diseño de información y visualización | 34 | 0 | 22 | 6 | 0 | 16 |
| 10.6 | Comunicar incertidumbre y riesgo a no expertos | 9 | 0 | 8 | 0 | 0 | 16 |
| 10.7 | Sesgos de encuadre y cómo neutralizarlos | 13 | 0 | 3 | 0 | 13 | 4 |
| 10.8 | Texto alternativo y accesibilidad | 7 | 0 | 0 | 2 | 0 | 0 |
| 10.9 | Requisitos de aviso legal | 9 | 1 | 0 | 0 | 0 | 0 |
| 10.10 | Coherencia entre los tres entregables | 3 | 0 | 0 | 0 | 1 | 0 |
| 10.11 | Plantillas y marcadores | 3 | 3 | 0 | 0 | 0 | 0 |
| 10.12 | Normas tipográficas y de localización | 5 | 5 | 0 | 0 | 0 | 0 |
| 10.13 | Inventario de competencias (inventario, no se cuenta) | 9 | 0 | 0 | 0 | 0 | 0 |

## Referencias canónicas y DOI

Cada entrada de las subáreas de referencias canónicas. Estricto: el título va en la propia entrada. Amplio `[PROPUESTO]`: otra cita del mismo primer autor y año, en el mismo prompt, lo lleva.

| Prompt | Entradas | Con autor y año | Con título (estricto) | Con título (amplio) | Citas en el prompt | Citas sin título en ningún sitio del prompt |
| --- | --- | --- | --- | --- | --- | --- |
| Analista Inmobiliario y de Infraestructuras | 18 | 18 | 18 | 18 | 17 | 6 |
| Analista de Alternativos y Mercados Privados | 38 | 38 | 38 | 38 | 47 | 11 |
| Analista de Criptoactivos y Activos Digitales | 19 | 19 | 19 | 19 | 19 | 6 |
| Analista de Derivados Financieros | 8 | 5 | 5 | 5 | 57 | 37 |
| Analista de Divisas | 38 | 37 | 9 | 21 | 96 | 47 |
| Analista de Fondos y Vehículos de Inversión Colectiva | 6 | 5 | 4 | 4 | 48 | 21 |
| Analista de Instrumentos Monetarios y Liquidez | 19 | 19 | 10 | 10 | 27 | 13 |
| Analista de Materias Primas | 25 | 25 | 25 | 25 | 27 | 3 |
| Analista de Prospectiva y Horizontes | 22 | 22 | 22 | 22 | 58 | 30 |
| Analista de Renta Fija y Crédito | 29 | 26 | 12 | 17 | 55 | 26 |
| Analista de Renta Variable | 4 | 1 | 1 | 1 | 78 | 62 |
| Analista de Tipos de Interés, Crédito y Volatilidad | 45 | 43 | 10 | 10 | 87 | 79 |
| Analista de hipótesis contrarias | 18 | 18 | 18 | 18 | 23 | 7 |
| Analista de Índices Bursátiles | 7 | 5 | 5 | 5 | 54 | 28 |
| Analizador de Tendencias de Inversión | 17 | 17 | 17 | 17 | 36 | 16 |
| Auditor | 0 | 0 | 0 | 0 | 23 | 8 |
| Buscador de Fuentes Avanzadas | 0 | 0 | 0 | 0 | 23 | 19 |
| Coordinador de Peticiones y Consultas | 0 | 0 | 0 | 0 | 1 | 0 |
| Curador de Evidencia | 0 | 0 | 0 | 0 | 6 | 4 |
| Documentador para el Analizador | 26 | 26 | 26 | 26 | 251 | 103 |
| Documentador para el Motor de Cálculo Avanzado | 0 | 0 | 0 | 0 | 234 | 170 |
| Evaluador de Previsiones y Aprendizaje | 0 | 0 | 0 | 0 | 66 | 15 |
| MC-01 Fundamentos cuantitativos y estadística | 15 | 15 | 8 | 8 | 26 | 18 |
| MC-02 Series temporales, tendencias, regímenes y volatilidad | 34 | 34 | 5 | 5 | 49 | 44 |
| MC-03 Econometría, causalidad y macroeconomía cuantitativa | 34 | 34 | 9 | 9 | 60 | 48 |
| MC-04 Crecimiento, difusión y prospectiva cuantitativa | 19 | 19 | 9 | 9 | 32 | 20 |
| MC-05 Simulación estocástica y escenarios | 21 | 21 | 8 | 8 | 29 | 20 |
| MC-06 Aprendizaje automático y predicción calibrada | 23 | 23 | 23 | 23 | 43 | 2 |
| MC-07 Optimización, decisión y riesgo | 24 | 24 | 24 | 24 | 39 | 6 |
| MC-08 Auditoría cuantitativa independiente | 11 | 11 | 11 | 11 | 12 | 1 |
| MC-09 Valoración y modelos de precios de activos | 75 | 74 | 71 | 71 | 119 | 7 |
| MC-10 Evaluación predictiva y backtesting | 28 | 28 | 28 | 28 | 48 | 6 |
| Motor de Cálculo Avanzado para el Analizador de Tendencias de Inversión | 51 | 49 | 13 | 13 | 152 | 136 |
| Orquestador técnico | 0 | 0 | 0 | 0 | 9 | 2 |
| Redactor y Diseñador de Informes | 0 | 0 | 0 | 0 | 44 | 3 |

### Entradas sin autor y año reconocibles (18)

| Prompt | Línea | Entrada |
| --- | --- | --- |
| Analista de Derivados Financieros | 371 | Hull («Options, Futures, and Other Derivatives») |
| Analista de Derivados Financieros | 371 | Natenberg («Option Volatility and Pricing») |
| Analista de Derivados Financieros | 371 | Sinclair («Volatility Trading») |
| Analista de Divisas | 398 | Sarno y Taylor («The Economics of Exchange Rates») como manual de referencia |
| Analista de Fondos y Vehículos de Inversión Colectiva | 367 | Lhabitant («Handbook of Hedge Funds») para estrategias |
| Analista de Renta Fija y Crédito | 395 | Fabozzi («Bond Markets, Analysis and Strategies»; «The Handbook of Fixed Income Securities») |
| Analista de Renta Fija y Crédito | 395 | Tuckman y Serrat («Fixed Income Securities: Tools for Today's Markets») |
| Analista de Renta Fija y Crédito | 395 | Duffie y Singleton («Credit Risk: Pricing, Measurement, and Management») |
| Analista de Renta Variable | 475 | Además de las citadas en cada apartado (autor y año bastan para que el DOC-A las localice por CT-08): Koller, Goedhart y Wessels («Valuation: Measuring and Managing the Value of Companies») |
| Analista de Renta Variable | 475 | Damodaran («Investment Valuation» y su actualización anual «Equity Risk Premiums») |
| Analista de Renta Variable | 475 | Dimson, Marsh y Staunton («Triumph of the Optimists» y el anuario «Global Investment Returns Yearbook») para la historia de largo plazo |
| Analista de Tipos de Interés, Crédito y Volatilidad | 415 | Tuckman y Serrat («Fixed Income Securities») |
| Analista de Tipos de Interés, Crédito y Volatilidad | 415 | Hull («Options, Futures, and Other Derivatives») |
| Analista de Índices Bursátiles | 434 | Damodaran («Equity Risk Premiums», actualización anual) |
| Analista de Índices Bursátiles | 434 | Shiller («Irrational Exuberance») |
| MC-09 Valoración y modelos de precios de activos | 273 | Damodaran (actualización anual), «Equity Risk Premiums: Determinants, Estimation and Implications» |
| Motor de Cálculo Avanzado para el Analizador de Tendencias de Inversión | 690 | Hull *Options, Futures, and Other Derivatives* |
| Motor de Cálculo Avanzado para el Analizador de Tendencias de Inversión | 690 | Damodaran *Investment Valuation* |

### Identificadores

Ningún prompt escribe un DOI, un ISBN ni un ISSN concretos (las menciones a «DOI» son instrucciones de método, como «no inventas referencias, DOI…»). Con el DOI se valida la estructura (no tiene dígito de control); con ISBN e ISSN, el dígito de control. Que un DOI exista no se puede comprobar sin red.

## Tamaños

Tokens aproximados con la función del ejecutor (`bloque_a/llm.py`, `_tokens_aprox`). Orientación: `v6.tope_tokens_system` de la configuración (`[PROPUESTO]`, T-101). AG-10 y AG-11 reciben en la V6 el prompt íntegro; los Analistas de tipo de activo reciben el núcleo y el kit (sin la §10 por defecto), que aquí se aproxima por el prompt sin la §10 (la medida exacta la vigila `tests/test_t101_v6.py`). El resto de papeles no tiene orientación escrita (INC-T187-01).

| Prompt | Agente | Palabras | Líneas | Caracteres | Tokens aprox. | Medida | Tope | Dentro |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Marco común de los Analistas de tipo de activo (plantilla) - V5.0.md (plantilla) | — | 1966 | 89 | 14391 | 3997 | — | — | — |
| Analista Inmobiliario y de Infraestructuras | AG-07 | 10891 | 489 | 72756 | 20210 | 11238 | 14000 | sí |
| Analista de Alternativos y Mercados Privados | AG-09 | 12334 | 550 | 84481 | 23466 | 12201 | 14000 | sí |
| Analista de Criptoactivos y Activos Digitales | AG-08 | 10642 | 491 | 71075 | 19743 | 11218 | 14000 | sí |
| Analista de Derivados Financieros | AG-23 | 9754 | 469 | 64581 | 17939 | 11175 | 14000 | sí |
| Analista de Divisas | AG-05 | 11592 | 520 | 75848 | 21068 | 11712 | 14000 | sí |
| Analista de Fondos y Vehículos de Inversión Colectiva | AG-22 | 10257 | 470 | 68252 | 18958 | 11200 | 14000 | sí |
| Analista de Instrumentos Monetarios y Liquidez | AG-24 | 9665 | 478 | 62065 | 17240 | 10587 | 14000 | sí |
| Analista de Materias Primas | AG-06 | 12773 | 538 | 84671 | 23519 | 12602 | 14000 | sí |
| Analista de Prospectiva y Horizontes | AG-10 | 11783 | 629 | 77565 | 21545 | 21545 | 23000 | sí |
| Analista de Renta Fija y Crédito | AG-04 | 11999 | 518 | 78043 | 21678 | 12275 | 14000 | sí |
| Analista de Renta Variable | AG-03 | 13988 | 616 | 91651 | 25458 | 13042 | 14000 | sí |
| Analista de Tipos de Interés, Crédito y Volatilidad | AG-25 | 10597 | 512 | 67920 | 18866 | 11406 | 14000 | sí |
| Analista de hipótesis contrarias | AG-11 | 10419 | 675 | 66523 | 18478 | 18478 | 20000 | sí |
| Analista de Índices Bursátiles | AG-21 | 11113 | 540 | 73187 | 20329 | 11905 | 14000 | sí |
| Analizador de Tendencias de Inversión | AG-02 | 18067 | 982 | 120127 | 33368 | — | — | — |
| Auditor | AG-19 | 8696 | 489 | 58891 | 16358 | — | — | — |
| Buscador de Fuentes Avanzadas | AG-16 | 9490 | 487 | 62390 | 17330 | — | — | — |
| Coordinador de Peticiones y Consultas | AG-01 | 13852 | 913 | 93398 | 25943 | — | — | — |
| Curador de Evidencia | AG-12 | 5791 | 370 | 38412 | 10670 | — | — | — |
| Documentador para el Analizador | AG-14 | 10744 | 524 | 70741 | 19650 | — | — | — |
| Documentador para el Motor de Cálculo Avanzado | AG-15 | 7452 | 382 | 51889 | 14413 | — | — | — |
| Evaluador de Previsiones y Aprendizaje | AG-20 | 11363 | 663 | 76315 | 21198 | — | — | — |
| MC-01 Fundamentos cuantitativos y estadística | — | 3890 | 252 | 25525 | 7090 | — | — | — |
| MC-02 Series temporales, tendencias, regímenes y volatilidad | — | 4042 | 227 | 26774 | 7437 | — | — | — |
| MC-03 Econometría, causalidad y macroeconomía cuantitativa | — | 3798 | 211 | 26357 | 7321 | — | — | — |
| MC-04 Crecimiento, difusión y prospectiva cuantitativa | — | 3587 | 204 | 24710 | 6863 | — | — | — |
| MC-05 Simulación estocástica y escenarios | — | 3454 | 206 | 23697 | 6582 | — | — | — |
| MC-06 Aprendizaje automático y predicción calibrada | — | 4324 | 279 | 30902 | 8583 | — | — | — |
| MC-07 Optimización, decisión y riesgo | — | 3568 | 236 | 24587 | 6829 | — | — | — |
| MC-08 Auditoría cuantitativa independiente | — | 3039 | 243 | 22232 | 6175 | — | — | — |
| MC-09 Valoración y modelos de precios de activos | — | 7186 | 315 | 48127 | 13368 | — | — | — |
| MC-10 Evaluación predictiva y backtesting | — | 4229 | 242 | 28417 | 7893 | — | — | — |
| Motor de Cálculo Avanzado para el Analizador de Tendencias de Inversión | AG-13 | 14927 | 772 | 100826 | 28007 | — | — | — |
| Orquestador técnico | AG-18 | 10810 | 637 | 69998 | 19443 | — | — | — |
| Redactor y Diseñador de Informes | AG-17 | 11250 | 670 | 71104 | 19751 | — | — | — |

## Paso 3 · Muestra

Muestra aleatoria simple sin reemplazo de 10 afirmaciones por prompt entre las frases candidatas (con fórmula, umbral, definición, cita o cifra) de las secciones de método y de base de conocimientos; semilla por prompt «semilla|archivo». Texto exacto en `muestra_afirmaciones.json`, con los campos del veredicto vacíos: los veredictos van aparte, en `veredictos/` (contraste más abajo, si está).

| Prompt | Candidatas | En la muestra | Con referencia citada en la frase | Con referencia en el elemento |
| --- | --- | --- | --- | --- |
| Analista Inmobiliario y de Infraestructuras | 124 | 10 | 1 | 0 |
| Analista de Alternativos y Mercados Privados | 138 | 10 | 2 | 0 |
| Analista de Criptoactivos y Activos Digitales | 108 | 10 | 2 | 0 |
| Analista de Derivados Financieros | 84 | 10 | 2 | 0 |
| Analista de Divisas | 137 | 10 | 2 | 2 |
| Analista de Fondos y Vehículos de Inversión Colectiva | 74 | 10 | 3 | 0 |
| Analista de Instrumentos Monetarios y Liquidez | 95 | 10 | 0 | 1 |
| Analista de Materias Primas | 140 | 10 | 1 | 1 |
| Analista de Prospectiva y Horizontes | 107 | 10 | 3 | 0 |
| Analista de Renta Fija y Crédito | 141 | 10 | 0 | 1 |
| Analista de Renta Variable | 139 | 10 | 3 | 0 |
| Analista de Tipos de Interés, Crédito y Volatilidad | 108 | 10 | 2 | 1 |
| Analista de hipótesis contrarias | 37 | 10 | 3 | 1 |
| Analista de Índices Bursátiles | 96 | 10 | 2 | 1 |
| Analizador de Tendencias de Inversión | 129 | 10 | 4 | 0 |
| Auditor | 77 | 10 | 2 | 0 |
| Buscador de Fuentes Avanzadas | 36 | 10 | 3 | 0 |
| Coordinador de Peticiones y Consultas | 55 | 10 | 0 | 0 |
| Curador de Evidencia | 54 | 10 | 1 | 1 |
| Documentador para el Analizador | 45 | 10 | 4 | 0 |
| Documentador para el Motor de Cálculo Avanzado | 53 | 10 | 7 | 2 |
| Evaluador de Previsiones y Aprendizaje | 203 | 10 | 2 | 1 |
| MC-01 Fundamentos cuantitativos y estadística | 57 | 10 | 2 | 0 |
| MC-02 Series temporales, tendencias, regímenes y volatilidad | 71 | 10 | 1 | 0 |
| MC-03 Econometría, causalidad y macroeconomía cuantitativa | 51 | 10 | 3 | 1 |
| MC-04 Crecimiento, difusión y prospectiva cuantitativa | 45 | 10 | 3 | 0 |
| MC-05 Simulación estocástica y escenarios | 33 | 10 | 1 | 0 |
| MC-06 Aprendizaje automático y predicción calibrada | 62 | 10 | 4 | 1 |
| MC-07 Optimización, decisión y riesgo | 70 | 10 | 2 | 0 |
| MC-08 Auditoría cuantitativa independiente | 39 | 10 | 1 | 0 |
| MC-09 Valoración y modelos de precios de activos | 170 | 10 | 0 | 3 |
| MC-10 Evaluación predictiva y backtesting | 78 | 10 | 1 | 1 |
| Motor de Cálculo Avanzado para el Analizador de Tendencias de Inversión | 179 | 10 | 3 | 3 |
| Orquestador técnico | 101 | 10 | 0 | 1 |
| Redactor y Diseñador de Informes | 67 | 10 | 2 | 1 |

## Paso 3 · Contraste de la muestra

Veredictos de cuatro revisores independientes (`veredictos/lote_*.json`: CORRECTA, ERRONEA o NO_VERIFICABLE, con una nota de hasta 40 palabras y la fuente consultada) y comentario del contraste (`veredictos/comentario.json`). Denominador (INC-T187-02 `[PROPUESTO]`): las afirmaciones verificables (CORRECTA + ERRONEA); las NO_VERIFICABLE son reglas internas del sistema que no se pueden contrastar con la literatura, y se declaran aparte con la otra cifra. Criterio de PB-51: ≥ 95 % correctas.

| Recuento | Valor |
| --- | --- |
| Afirmaciones juzgadas | 350 |
| CORRECTA | 260 |
| ERRONEA | 9 |
| NO_VERIFICABLE | 81 |
| Correctas sobre las verificables (269) | **96.7 %** |
| Correctas sobre todas (350) | 74.3 % |
| Veredicto (≥ 95 % sobre las verificables) | **SUPERA** |

### Por lote

| Lote | Revisor | Prompts | CORRECTA | ERRONEA | NO_VERIFICABLE | % sobre verificables |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | claude (revisor independiente) | AG-05, AG-06, AG-07, AG-08, AG-09, AG-10, AG-22, AG-23, AG-24 | 66 | 2 | 22 | 97.1 % |
| 2 | claude (revisor independiente) | AG-01, AG-02, AG-03, AG-04, AG-11, AG-16, AG-19, AG-21, AG-25 | 58 | 5 | 27 | 92.1 % |
| 3 | claude (revisor independiente) | AG-12, AG-14, AG-15, AG-20, MC-01, MC-02, MC-03, MC-04, MC-05 | 74 | 2 | 14 | 97.4 % |
| 4 | claude (revisor independiente) | AG-13, AG-17, AG-18, MC-06, MC-07, MC-08, MC-09, MC-10 | 62 | 0 | 18 | 100.0 % |

### Por prompt

| Prompt | Código | Lote | CORRECTA | ERRONEA | NO_VERIFICABLE | Verificables | % sobre verificables |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Analista Inmobiliario y de Infraestructuras | AG-07 | 1 | 10 | 0 | 0 | 10 | 100.0 % |
| Analista de Alternativos y Mercados Privados | AG-09 | 1 | 8 | 0 | 2 | 8 | 100.0 % |
| Analista de Criptoactivos y Activos Digitales | AG-08 | 1 | 7 | 0 | 3 | 7 | 100.0 % |
| Analista de Derivados Financieros | AG-23 | 1 | 7 | 0 | 3 | 7 | 100.0 % |
| Analista de Divisas | AG-05 | 1 | 6 | 0 | 4 | 6 | 100.0 % |
| Analista de Fondos y Vehículos de Inversión Colectiva | AG-22 | 1 | 7 | 1 | 2 | 8 | 87.5 % |
| Analista de Instrumentos Monetarios y Liquidez | AG-24 | 1 | 9 | 1 | 0 | 10 | 90.0 % |
| Analista de Materias Primas | AG-06 | 1 | 6 | 0 | 4 | 6 | 100.0 % |
| Analista de Prospectiva y Horizontes | AG-10 | 1 | 6 | 0 | 4 | 6 | 100.0 % |
| Analista de Renta Fija y Crédito | AG-04 | 2 | 8 | 0 | 2 | 8 | 100.0 % |
| Analista de Renta Variable | AG-03 | 2 | 8 | 0 | 2 | 8 | 100.0 % |
| Analista de Tipos de Interés, Crédito y Volatilidad | AG-25 | 2 | 5 | 2 | 3 | 7 | 71.4 % |
| Analista de hipótesis contrarias | AG-11 | 2 | 9 | 0 | 1 | 9 | 100.0 % |
| Analista de Índices Bursátiles | AG-21 | 2 | 7 | 0 | 3 | 7 | 100.0 % |
| Analizador de Tendencias de Inversión | AG-02 | 2 | 7 | 1 | 2 | 8 | 87.5 % |
| Auditor | AG-19 | 2 | 4 | 1 | 5 | 5 | 80.0 % |
| Buscador de Fuentes Avanzadas | AG-16 | 2 | 8 | 1 | 1 | 9 | 88.9 % |
| Coordinador de Peticiones y Consultas | AG-01 | 2 | 2 | 0 | 8 | 2 | 100.0 % |
| Curador de Evidencia | AG-12 | 3 | 6 | 0 | 4 | 6 | 100.0 % |
| Documentador para el Analizador | AG-14 | 3 | 6 | 1 | 3 | 7 | 85.7 % |
| Documentador para el Motor de Cálculo Avanzado | AG-15 | 3 | 9 | 0 | 1 | 9 | 100.0 % |
| Evaluador de Previsiones y Aprendizaje | AG-20 | 3 | 8 | 0 | 2 | 8 | 100.0 % |
| MC-01 Fundamentos cuantitativos y estadística | MC-01 | 3 | 7 | 1 | 2 | 8 | 87.5 % |
| MC-02 Series temporales, tendencias, regímenes y volatilidad | MC-02 | 3 | 9 | 0 | 1 | 9 | 100.0 % |
| MC-03 Econometría, causalidad y macroeconomía cuantitativa | MC-03 | 3 | 10 | 0 | 0 | 10 | 100.0 % |
| MC-04 Crecimiento, difusión y prospectiva cuantitativa | MC-04 | 3 | 10 | 0 | 0 | 10 | 100.0 % |
| MC-05 Simulación estocástica y escenarios | MC-05 | 3 | 9 | 0 | 1 | 9 | 100.0 % |
| MC-06 Aprendizaje automático y predicción calibrada | MC-06 | 4 | 10 | 0 | 0 | 10 | 100.0 % |
| MC-07 Optimización, decisión y riesgo | MC-07 | 4 | 9 | 0 | 1 | 9 | 100.0 % |
| MC-08 Auditoría cuantitativa independiente | MC-08 | 4 | 6 | 0 | 4 | 6 | 100.0 % |
| MC-09 Valoración y modelos de precios de activos | MC-09 | 4 | 10 | 0 | 0 | 10 | 100.0 % |
| MC-10 Evaluación predictiva y backtesting | MC-10 | 4 | 9 | 0 | 1 | 9 | 100.0 % |
| Motor de Cálculo Avanzado para el Analizador de Tendencias de Inversión | AG-13 | 4 | 10 | 0 | 0 | 10 | 100.0 % |
| Orquestador técnico | AG-18 | 4 | 3 | 0 | 7 | 3 | 100.0 % |
| Redactor y Diseñador de Informes | AG-17 | 4 | 5 | 0 | 5 | 5 | 100.0 % |

El paso 3 pide 10 afirmaciones técnicas por prompt. Las NO_VERIFICABLE no lo son, así que 28 de 35 prompts quedan por debajo de 10 verificables: Coordinador de Peticiones y Consultas 2; Orquestador técnico 3; Auditor 5; Redactor y Diseñador de Informes 5; Analista de Divisas 6; Analista de Materias Primas 6; Analista de Prospectiva y Horizontes 6; Curador de Evidencia 6; MC-08 Auditoría cuantitativa independiente 6; Analista de Criptoactivos y Activos Digitales 7; Analista de Derivados Financieros 7; Analista de Tipos de Interés, Crédito y Volatilidad 7; Analista de Índices Bursátiles 7; Documentador para el Analizador 7; Analista de Alternativos y Mercados Privados 8; Analista de Fondos y Vehículos de Inversión Colectiva 8; Analista de Renta Fija y Crédito 8; Analista de Renta Variable 8; Analizador de Tendencias de Inversión 8; Evaluador de Previsiones y Aprendizaje 8; MC-01 Fundamentos cuantitativos y estadística 8; Analista de hipótesis contrarias 9; Buscador de Fuentes Avanzadas 9; Documentador para el Motor de Cálculo Avanzado 9; MC-02 Series temporales, tendencias, regímenes y volatilidad 9; MC-05 Simulación estocástica y escenarios 9; MC-07 Optimización, decisión y riesgo 9; MC-10 Evaluación predictiva y backtesting 9. Se declara (INC-T187-02); no hay muestra de reposición.

### Por fuente declarada en la nota

Clasificación mecánica de la nota: «búsqueda web» (no «sin búsqueda web») o «Web:»; «conocimiento propio» (de memoria, sin consultar la referencia); cálculo a mano; si no, sin fuente declarada.

| Veredicto | búsqueda web | memoria (conocimiento propio) | cálculo a mano | sin fuente declarada |
| --- | --- | --- | --- | --- |
| CORRECTA | 3 | 249 | 8 | 0 |
| ERRONEA | 5 | 2 | 1 | 1 |
| NO_VERIFICABLE | 0 | 0 | 0 | 81 |

### Afirmaciones ERRONEA (9)

Hallazgos de los prompts: no se corrigen aquí (corpus congelado); quedan para la próxima entrega del corpus (INC-T187-03).

| Id | Prompt (línea) | Frase | Error | Corrección (de la nota del revisor) | Cita de la nota |
| --- | --- | --- | --- | --- | --- |
| AF-AG-22-03 | Analista de Fondos y Vehículos de Inversión Colectiva (280) | **Tendencia**: los informes anuales de ESMA sobre costes y rentabilidad de los productos minoristas muestran que los fondos UCITS activos de renta variable cuestan del orden de 1,3–1,6 % anual a los minoristas frente a 0,2–0,4 % de los ETF y fondos indexados; los costes reducen la rentabilidad acumulada de forma mayor cuanto más largo es el horizonte. | Los informes de ESMA dan para los fondos UCITS activos de renta variable más del 1,5 % anual y para los pasivos y ETF en torno al 0,6 % de media (solo ETF, 0,2–0,3 %); el intervalo 1,3–1,6 % frente a 0,2–0,4 % no coincide. | «del orden de 1,5–2 % anual frente a 0,5–0,6 % de los fondos pasivos» | Correcto: «≈1,5–2 % frente a ≈0,5–0,6 % de pasivos» |
| AF-AG-24-05 | Analista de Instrumentos Monetarios y Liquidez (302) | Mezclar convenciones produce errores de 10–30 pb, más frecuentes que los errores de análisis. | Cifra exagerada y sin fuente: el ejemplo del propio prompt (ACT/360 frente a ACT/365 al 3 %) da 4 pb, y descuento frente a rendimiento al 4 %, unos 4–8 pb. | «produce errores de unos pocos pb (≈ 3–10)», sin comparar frecuencias | Correcto: «unos pocos pb (≈3–10)», sin comparar frecuencias |
| AF-AG-25-04 | Analista de Tipos de Interés, Crédito y Volatilidad (342) | **Descomposición**: modelos afines conjuntos nominal-real (Abrahams, Adrian, Crump, Moench y Yu, 2016; Gürkaynak, Sack y Wright, 2010). | Gürkaynak, Sack y Wright (2010) ajustan curvas de los TIPS suavizadas (Svensson), no un modelo afín conjunto nominal-real; Abrahams, Adrian, Crump, Moench y Yu (2016) sí lo es. | Sustituir la segunda cita por D'Amico, Kim y Wei (2018). | Sustituir por D'Amico, Kim y Wei (2018) |
| AF-AG-25-08 | Analista de Tipos de Interés, Crédito y Volatilidad (441) | **Swaptions**: opciones sobre swaps; la volatilidad normal implícita de swaptions (en pb) por vencimiento de la opción y plazo del swap forma el «cubo» de volatilidad de tipos; el MOVE es su análogo sobre el Tesoro (10.9). | Vencimiento de la opción × plazo del swap forma la matriz (o superficie) de volatilidad de las swaptions; el «cubo» añade la tercera dimensión, el strike. Lo del MOVE es correcto. | «forma la matriz (o superficie) de volatilidad de swaptions»; el cubo, con el strike | Vencimiento × plazo forma la matriz (o superficie) de volatilidad de swaptions |
| AF-AG-02-09 | Analizador de Tendencias de Inversión (735) | **Número efectivo de apuestas por componentes principales** (Meucci, 2009, «Managing Diversification»): entropía de la contribución al riesgo de los factores no correlacionados. | Meucci (2009) define el número efectivo de apuestas como la exponencial de la entropía de la distribución de las contribuciones al riesgo, no como la entropía. | «exponencial de la entropía…»: N = exp(−Σ p·ln p) | N = exp(−Σ p ln p), no la entropía |
| AF-AG-19-07 | Auditor (401) | **Backtests sobreajustados**: probabilidad de sobreajuste (Bailey, Borwein, López de Prado y Zhu, 2014, «The Probability of Backtest Overfitting», *Journal of Computational Finance*); Sharpe deflactado (Bailey y López de Prado, 2014, *Journal of Portfolio Management*). | Año de la cita: la PBO de Bailey, Borwein, López de Prado y Zhu se publicó en el Journal of Computational Finance 20(4) en 2017 (preprints de 2013–2015). El Sharpe deflactado de 2014 en el JPM es correcto. | «Bailey, Borwein, López de Prado y Zhu, 2017» | se publicó en Journal of Computational Finance 20(4), 2017 |
| AF-AG-16-03 | Buscador de Fuentes Avanzadas (294) | Tetlock (2005) y Tetlock y Gardner (2015): los expertos rinden poco mejor que reglas simples en preguntas a largo plazo; la calibración se mide, no se presume. | Tetlock (2005) halló que los expertos quedaban por debajo de los algoritmos de extrapolación simple y apenas superaban al azar, no «poco mejor que reglas simples». | Decir lo que halló: por debajo de los algoritmos de extrapolación simple y apenas por encima del azar (la nota no propone otra redacción). | quedaban por DEBAJO de algoritmos de extrapolación simple y apenas superaban al azar |
| AF-AG-14-06 | Documentador para el Analizador (354) | **Crisis de replicación.** Leamer (1983), «Let's Take the Con Out of Econometrics»; Ioannidis (2005), «Why Most Published Research Findings Are False»; Camerer et al. (2016), réplica de experimentos de economía; Brodeur et al. (2016), «Star Wars: The Empirics Strike Back» (acumulación de estadísticos t justo por encima de 1,96); Harvey, Liu y Zhu (2016), «… and the Cross-Section of Expected Returns» (zoo de factores; umbral t > 3); McLean y Pontiff (2016), «Does Academic Research Destroy Stock Return Predictability?» (las anomalías pierden en torno a un tercio fuera de muestra y más tras publicarse); Hou, Xue y Zhang (2020), «Replicating Anomalies»; Jensen, Kelly y Pedersen (2023), «Is There a Replication Crisis in Finance?» (la mayoría de factores se replica con un enfoque bayesiano y global). | McLean y Pontiff (2016) hallan rentabilidades un 26 % menores fuera de muestra (en torno a un cuarto) y un 58 % menores tras publicarse, no «en torno a un tercio». Las demás referencias de la frase son reales. | «en torno a un cuarto» o «26 %» | Debería decir «en torno a un cuarto» o «26 %» |
| AF-MC-01-05 | MC-01 Fundamentos cuantitativos y estadística (152) | **Tamaño del efecto y potencia.** d de Cohen `(x̄_1 − x̄_2)/s_conjunta`; `n ≈ [(z_{1−α/2} + z_{1−β})σ/δ]²` por grupo para medias. | Para dos grupos, el tamaño por grupo lleva un factor 2; la fórmula sin él es la de una muestra. La d de Cohen es correcta. | `n ≈ 2·[(z_{1−α/2} + z_{1−β})σ/δ]²` por grupo | la fórmula sin el factor 2 es la de una muestra |

### Casos dudosos marcados CORRECTA con matiz (5)

Criterio: CORRECTA cuya nota trae un matiz explícito («matiz», «exagera», «difieren» u «ojo»; `RE_MATIZ` del script). El script exige que el comentario liste exactamente esas.

| Id | Prompt (línea) | Matiz | Cita de la nota | Nota del revisor |
| --- | --- | --- | --- | --- |
| AF-MC-02-04 | MC-02 Series temporales, tendencias, regímenes y volatilidad (100) | MASE < 1 es mejor que el ingenuo de un paso dentro de muestra; no garantiza batir al ingenuo a horizonte h fuera de muestra. | ojo: no garantiza batir al ingenuo a horizonte h fuera de muestra | Hyndman y Koehler (2006): MASE < 1 indica mejor que el ingenuo de un paso dentro de muestra. Simplificación razonable; ojo: no garantiza batir al ingenuo a horizonte h fuera de muestra. Conocimiento propio. |
| AF-MC-06-02 | MC-06 Aprendizaje automático y predicción calibrada (144) | Bergmeir, Hyndman y Koo (2018) prueban la validez del k-fold en modelos autorregresivos puros con errores incorrelados; el «solo» exagera algo. | El «solo» exagera algo, pero es fiel al resultado | Bergmeir, Hyndman y Koo (2018, CSDA 120) prueban que el k-fold es válido en modelos autorregresivos puros con errores incorrelados. El «solo» exagera algo, pero es fiel al resultado. Conocimiento propio. |
| AF-MC-07-10 | MC-07 Optimización, decisión y riesgo (199) | Quien publica los escenarios de estrés de la Fed es la Junta de Gobernadores, no un «Banco de la Reserva Federal». | Matiz: quien los publica es la Junta de Gobernadores de la Fed | Los escenarios adversos de la EBA y de la Fed (CCAR/DFAST) son narrativas coherentes sin probabilidad asignada. Matiz: quien los publica es la Junta de Gobernadores de la Fed. Conocimiento propio. |
| AF-AG-13-09 | Motor de Cálculo Avanzado para el Analizador de Tendencias de Inversión (586) | Ledoit y Wolf: el objetivo de correlación constante se publicó en el JPM en 2004 (documento de trabajo de 2003); mejor citar 2004. | Matiz: mejor citar 2004 | Correlación constante: «Honey, I shrunk…» (JPM, 2004; working paper de junio de 2003). Identidad escalada: JMVA (2004). Contracción no lineal: Ann. Stat. (2020). Matiz: mejor citar 2004. Búsqueda web: bse.eu, ideas.repec.org. |
| AF-AG-17-04 | Redactor y Diseñador de Informes (419) | Los niveles orientativos de la escala de Fernández Huerta difieren algo entre fuentes. | Los niveles orientativos difieren algo entre fuentes | La escala por tramos de 10 es la de Fernández Huerta (adaptada de Flesch). Los niveles orientativos difieren algo entre fuentes, pero son una simplificación razonable. Conocimiento propio. |

### Sensibilidad

Casos: AF-AG-22-03, AF-AG-24-05. Los elige quien escribe el comentario, no los revisores (ninguna nota las llama discutibles): son las dos ERRONEA que discuten la magnitud de un intervalo numérico y no un concepto, una cita o una fórmula; la QA r01 no pudo confirmar ni refutar AF-AG-22-03 con una búsqueda. ERRONEA que un revisor llama discutibles en su nota: ninguna.

| Supuesto | CORRECTA | ERRONEA | Verificables | % sobre verificables | Veredicto |
| --- | --- | --- | --- | --- | --- |
| Tal como las juzgan los revisores | 260 | 9 | 269 | 96.7 % | SUPERA |
| Esos casos cuentan como correctas | 262 | 7 | 269 | 97.4 % | SUPERA |
| Esos casos se quitan | 260 | 7 | 267 | 97.4 % | SUPERA |

Entre los tres supuestos el veredicto no cambia.

