# Bloque B: rediseño con menos agentes (propuesta de diseño de Claude)

De: Claude, 11-11-2026. Estado: **PROPUESTA PARA DISCUTIR**, alternativa más ambiciosa a la evaluación de `.docs/tickets/T-68/evaluacion_claude.md`. No hay nada que implementar: `bloque_b/` sigue congelado (relevo de Astra, §0 bis). Copia en el repositorio del documento que el operador revisó con Claude.

Encargo del operador: «modifica la propuesta del bloque B», tras ver que para C proponía coordinación en código, núcleo más kits y pocos papeles de IA, y que para B había mantenido los 24 agentes.

## 1. Respuesta corta

La evaluación de T-68 mantenía los 24 agentes y proponía ahorrar con caché, prompts por módulos y lotes (entre un 39 % y un 44 % menos de entrada). Este rediseño aplica a B la misma pauta que a C: **la coordinación la hace código, lo que varía por tema o tipo de activo se carga como módulos de texto, y solo quedan los papeles de IA que aportan juicio.**

- **De 24 agentes a 5 papeles de IA:** Analista de ámbito, Analista de dimensión (un módulo por dimensión), Seleccionador (kit por tipo de activo), Contradictor de otro proveedor y Lector de evidencia aislado.
- **Sin Director.** Sus siete llamadas con Opus (la mitad del coste de entrada) se reparten entre el Orquestador (código) y el Analista de ámbito.
- **Solo las dimensiones que importan:** el plan decide por código cuáles son materiales para el ámbito.
- **Lo que la Constitución pone fuera de B** (evaluación, vigilancia, documentación, orquestación) pasa a I, H, K y el Orquestador.

Estimación sin medir: un N2 pasaría de unos 990.000 tokens de entrada en 27 a 29 llamadas a 150.000–200.000 en 6 a 8. **No de golpe:** primero el banco de medida, y cada recorte como aspirante frente al diseño actual.

## 2. Lo que hay hoy y lo que cuesta

Medido en T-68 con el cliente simulado: 27 a 29 llamadas y unos 990.000 tokens de entrada por N2, el 96 % prompts de sistema. Director (Opus) 7 llamadas y 315.000 tokens de prompt; Seleccionador (Opus) 4 y 145.000; Estructura 3 y 102.000; Coordinador 2 y 72.000; diez especialistas y Emergentes, 28.000 a 39.000 cada uno. Unos 2,3 $ de entrada por análisis, entre el 47 % y el 53 % del Director. La salida no se mide en simulado, y en real habrá más rondas. **Nadie ha medido cuánta precisión aportan los agentes** frente a la selección por código (universo, Motor, HT-03).

## 3. Dónde fue conservadora la propuesta anterior

1. **Que un agente coordine.** Planificar y encadenar fases es una máquina de estados con reglas; el juicio necesario (tesis y veredicto) cabe en un analista con un prompt mucho más corto.
2. **Que cada dimensión necesite su agente.** Los diez especialistas comparten entre el 24 % y el 34 % de su prompt; lo que los distingue cabe en un módulo. Hoy se llaman casi todos en cada análisis.
3. **Que B tenga su propio evaluador, vigilante, documentadores y orquestador**, que la Constitución pone en I, H, K y el Orquestador.

La Constitución ya apunta aquí (P12, D-42), y en A se propuso lo mismo en T-53 (PA-06 y PA-07), aplazado.

## 4. El rediseño

| Papel | Qué hace | Modelo propuesto | Cuándo se llama | Sustituye a |
| --- | --- | --- | --- | --- |
| **Analista de ámbito** | Tesis al principio y veredicto al final | Sonnet en N1 y N2; Opus en N3 | Dos veces | Juicio del Director, Prospectiva |
| **Analista de dimensión** | Una dimensión con su módulo cargado | Haiku en N1; Sonnet en N2 y N3 | Una vez por dimensión material; en N1, todas juntas | Diez especialistas, Emergentes, Estructura |
| **Seleccionador** | Candidatos y vía de acceso con el kit del tipo de activo | Sonnet; Opus solo si el banco lo justifica | Una vez por tipo que toca el ámbito | Seleccionador en Opus con 12 playbooks |
| **Contradictor** | Ataca la selección con la evidencia, sin el razonamiento | Otro proveedor si es posible (§3) | Una vez en N2 y N3 | Contrario |
| **Lector de evidencia** | Lee web y documentos aislado; datos con fuente y fecha | Haiku | Solo si hay fuentes externas | Parte de Documentador y Curador |

Núcleo común corto primero y en la misma caché; después el módulo o kit. Números desde la configuración.

**Pasa a código:** plan y fases (dimensiones materiales, puertas PV1 a PV3); admisión y estimación; normalizar y deduplicar evidencia; informe por plantilla; auditoría (G3 ya es código; IA solo por muestreo, por lotes).

**Sale de B:** evaluación → I; vigilancia → H; archivos de referencia → K y registros comunes; orquestación → Orquestador del Broker.

**Un N2:** encargo → Orquestador (código) → Analista de ámbito (tesis) → 2 o 3 dimensiones materiales → Motor y HT-03 (código) → Seleccionador por tipo → Contradictor → Analista de ámbito (veredicto) → G3 y paquete CT-B-02 (código). Seis a ocho llamadas. En N1, dimensiones en una llamada y sin Contradictor; en N3, un segundo Analista de ámbito independiente de otro modelo, cuyo desacuerdo baja la confianza.

## 5. Precisión

- El conocimiento de cada especialista sigue en su módulo; solo deja de enviarse cuando no importa.
- La diversidad real viene de otro modelo (Contradictor y, en N3, segundo analista), no de más agentes del mismo modelo (§3).
- Red de seguridad: el Analista de ámbito puede pedir una dimensión que el plan dejó fuera, con motivo registrado; I mide cuántas veces.
- Prompts cortos, menos reglas en conflicto (hipótesis a confirmar con el banco).

**Banco de medida primero**, sobre ámbitos históricos congelados y anonimizados, con su coste: (1) azar en el universo del ámbito; (2) solo código (universo, Motor, HT-03); (3) diseño actual; (4) rediseño. Si (2) queda cerca de (3), el valor de los agentes es pequeño; si (4) queda por debajo de (3), no se adopta. Con pocos ámbitos la medida tendrá ruido: se añaden medidas intermedias (confirmación de C, torneo de pronósticos §9).

## 6. Consumo estimado y migración

| Nivel | Llamadas | Entrada estimada | Hoy |
| --- | --- | --- | --- |
| N1 | 3 o 4 | 60.000–100.000 | Sin medir |
| N2 | 6 a 8 | 150.000–200.000 | ≈ 990.000 en 27–29 |
| N3 | 9 a 11 | 250.000–300.000 | Sin medir |

| Paso | Qué se hace | Riesgo | Mejoras de T-68 |
| --- | --- | --- | --- |
| 0 | Banco de medida | Ninguno | 1 |
| 1 | Caché solo donde se repite, lotes, precios y tope en euros | Ninguno | 2, 6, 7 |
| 2 | A código: admisión, curación, plan y fases, informe | Bajo | 9 y parte de 5 |
| 3 | Núcleo más módulos y kits | Bajo; se mide | 3, 4, 5 |
| 4 | Consolidar papeles uno a uno como aspirante | Medio; se mide | 8 |
| 5 | Sacar lo que es de I, H, K y el Orquestador | Ninguno | — |

## 7. Preguntas para el operador

1. ¿Este rediseño como objetivo, con el camino por pasos, o solo las mejoras de ahorro de T-68?
2. El banco de medida, lo primero cuando B se descongele.
3. Contradictor de otro proveedor: segundo proveedor de IA con su coste y credenciales, para A, B y C a la vez.
4. Sonnet por defecto y Opus solo en N3, salvo que el banco demuestre otra cosa.
5. Una sola pauta para A, B y C.
