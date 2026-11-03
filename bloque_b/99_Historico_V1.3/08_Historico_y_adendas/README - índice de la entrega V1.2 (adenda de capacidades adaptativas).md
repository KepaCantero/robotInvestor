# README — índice de la entrega · Bloque B — Versión óptima V1.2 (Adenda de capacidades adaptativas)

**Fecha de la entrega:** 31/10/2026 · **Naturaleza:** respuesta a la pregunta del operador («¿está la propuesta completamente implementada en el Bloque B?»): asimilación de la «Propuesta de mejoras y evolución arquitectónica del Bloque B — Analizador de Mercados» (29 secciones) e integración de lo que faltaba, con los archivos y system prompts modificados devueltos íntegros · **Gobernanza:** «Documento 0 --- Protocolo maestro del Bloque B» óptima V1.2 (31/10/2026) · **Idioma:** es-ES · **Estado de todo el paquete:** pendiente de la aprobación del operador por paquetes (tipo 3, 9.2) y de su publicación coordinada (5.5); nada de lo aquí contenido está en vigor hasta entonces.

## 1. Respuesta en una línea

La arquitectura vigente (óptima V1.1, con la adenda del 30/10/2026 ya integrada) implementaba la mayoría de los veintinueve apartados de la propuesta; catorce áreas estaban ya cubiertas con su anclaje normativo, once estaban parcialmente cubiertas y ninguna exigía agentes, archivos o contratos nuevos de serie. Las once brechas se resuelven con **catorce capacidades nuevas (CAP-B-01 a CAP-B-14)** y **doce decisiones propuestas (D25-D36)**, que aterrizan en los cinco agentes, los dos esquemas de archivo y el Documento 0. El Motor de Cálculo Avanzado y su Documentador **no cambian** (la regla 1.2 de la adenda ligera queda intacta: el saneo de resultados es comprobación del lado cliente).

## 2. Contenido de la entrega (archivos modificados, devueltos íntegros)

| # | Pieza | Versión | Qué transporta |
|---|---|---|---|
| 1 | «Adenda de arquitectura --- Bloque B: Asimilación de la propuesta de mejoras y evolución arquitectónica» | V1.0 (31/10/2026) | El documento de revisión completo: matriz de cobertura por las 29 secciones de la propuesta, las catorce capacidades CAP-B con su destino documental exacto, lo no adoptado y por qué, plan de fases, inventario de impacto, decisiones D25-D36, tabla maestra de decisión (Anexo I: estado, necesidad, solución, prioridad, dependencias, coste y criterios de eficacia), arquitectura funcional consolidada de las 17 capacidades (Anexo II) y campos nuevos por esquema (Anexo III) |
| 2 | «Documento 0 --- Protocolo maestro del Bloque B» | óptima V1.2 | Nota de versión, refuerzo de cometidos y contenidos ampliados (2.2, 2.3), **nueva sección 2.4 bis: matriz de responsabilidades** entre el Bloque B y el resto del ecosistema (D36), glosario con nueve términos nuevos (banco de casos, causa de discrepancia, grafo de dependencias, mapa de oportunidades, objeción adversarial material, registro de contraste adversarial, vocabulario riesgo/incertidumbre/ignorancia/ambigüedad, saneo de resultados), Anexo C (CT-B-05 con el registro adversarial como adjunto; CT-B-07 con siete focos), Anexo D (filas V1.2), Anexo H y Anexo J (D25-D36) |
| 3 | System prompt «Analizador de Mercados» | óptima V1.2 | Grafo de dependencias y orden de ejecución del ciclo en el plan con clasificación de nodos obligatoria/condicional/excluible (D25); módulos K.7 (regulatorio, político y geopolítico) y K.8 (flujos y posicionamiento) en el Anexo K (D26); régimen con estado de confianza y naturaleza de relaciones históricas/causales en F3 y criterio de fluctuación frente a cambio estructural en las señales (D27); citas localizadas y protocolo de discrepancias en seis pasos (D28); Anexo L ampliado con zona horaria, sesgos de supervivencia y disponibilidad, retraso de publicación y regla de conservación (D29); regla R6 de saneo de resultados en la 8 bis (D30); registro de contraste adversarial con respuesta por objeción en F5/F6 (D31); confianza por factores y vocabulario del no saber (D32); mapa de oportunidades como sección 7 ter del informe completo y línea de lectura en el resumido (D35) |
| 4 | System prompt «Orquestador técnico para el Analizador de Mercados» | óptima V1.2 | Rúbrica ampliada a veintidós comprobaciones: B21 (grafo de dependencias; D25) y B22 (registro de contraste adversarial; D31); recepción del CT-B-05 con el registro adversarial como adjunto; remisión al Auditor con siete focos (D33); tres indicadores nuevos del cuadro de mando (adecuación del plan, conclusiones modificadas por evidencia omitida, incertidumbre reconocida; D33); evaluación comparativa de mejoras sobre el banco de casos (D34) |
| 5 | System prompt «Buscador de fuentes avanzadas para el Analizador de Mercados» | óptima V1.2 | Captura de los ocho campos de procedencia y contexto de la ficha RF-B (añade metodología de la fuente, alcance geográfico y sectorial, accesibilidad y estabilidad; D28); declaración de la causa probable de las discrepancias y búsqueda de la fuente primaria cuando la resolución la pida (D28) |
| 6 | System prompt «Documentador para el Analizador de Mercados» | óptima V1.2 | Ficha de fuente con ocho campos de procedencia y contexto (D28); ficha de régimen ampliada con estado de confianza, naturaleza de las relaciones y criterio de transición (D27); nuevo ámbito «caso de calibración» con la consolidación del banco y su mapa de clases en el mantenimiento mensual (D34) |
| 7 | System prompt «Auditor para el Analizador de Mercados» | óptima V1.2 | Nuevo foco 4.8 de idoneidad del plan y de la selección metodológica, con hallazgo típico «plan inadecuado» (SUST; D33); verificación del saneo R6 (D30), del registro adversarial (D31), de las declaraciones ampliadas (D29), del régimen con estado de confianza (D27) y de las citas localizadas (D28); banco de casos de calibración como contraste de la vara en la calibración CT-B-11 (D34); indicador de conclusiones modificadas por evidencia omitida (D33) |
| 8 | «Registro de Fuentes Fiables para el Analizador de Mercados» | esquema V1.2 | Bloque «Procedencia, contexto y calidad» con ocho campos por ficha (D28); versión de esquema 1.2 en el índice operativo |
| 9 | «Documentación para el Analizador de Mercados» | esquema V1.2 | Ámbito nuevo «caso de calibración» con el banco de casos, sus nueve clases y su mapa (D34); ficha de régimen ampliada (D27); versión de esquema 1.2 |

Cada archivo .md va acompañado de su versión .docx con el mismo nombre base.

## 3. Qué NO cambia en esta entrega

- **La topología del bloque**: los mismos cinco agentes propios, los mismos dos servicios transversales, los mismos cuatro archivos operativos, los mismos doce contratos CT-B (dos con contenido ampliado: CT-B-05 y CT-B-07) y el mismo Fondo metodológico en solo lectura.
- **El Motor de Cálculo Avanzado y su Documentador**: la regla 1.2 de la adenda ligera queda intacta (el carril no añade métodos; el saneo de resultados es comprobación del cliente; las pruebas de fórmulas críticas ya existen como pruebas de regresión del catálogo).
- **Los niveles, los estados del ciclo, el catálogo de rechazo y la serie de contratos**: Rápido/Estándar/Exhaustivo, S0-S7, R1-R4 y CT-B-01 a CT-B-12 quedan como están; las capacidades entran por campos de contenido, adjuntos, comprobaciones y secciones.
- **Piezas sin cambios**: «Registro de solicitudes y ejecuciones» (esquema V1.1), «Registro de recomendaciones y seguimiento» (esquema V1.1), «Runbook del operador» (V1.1), «Objetivos del Bloque B» (V1.2 exhaustiva: las CAP-B refuerzan O2, O3, O4, O6, O7 y O10 sin modificar su enunciado), «Adenda ligera» (V1.0) y «Propuesta de activación» (V1.1: la aprobación del paquete V1.2 se tramita en el mismo acto por paquetes, conforme a 9.2 del Documento 0-B).

## 4. Las catorce capacidades en una mirada

1. **CAP-B-01** Grafo de dependencias y orden de ejecución del ciclo (propuesta §3, §15) · D25.
2. **CAP-B-02** Módulos K.7 y K.8: regulatorio-geopolítico y flujos-posicionamiento (§4) · D26.
3. **CAP-B-03** Régimen incierto, mixto o en transición; relación histórica frente a causal (§6) · D27.
4. **CAP-B-04** Ficha de fuente con ocho campos y citas localizadas (§7.1, §7.5) · D28.
5. **CAP-B-05** Protocolo de resolución de contradicciones en seis pasos (§7.4) · D28.
6. **CAP-B-06** Declaración de datos ampliada: zona horaria, supervivencia, retraso de publicación, conservación (§8) · D29.
7. **CAP-B-07** Saneo de resultados R6 (consistencia, extremos, fuga de información) (§9) · D30.
8. **CAP-B-08** Registro de contraste adversarial con respuesta material (§11) · D31.
9. **CAP-B-09** Confianza por factores y vocabulario riesgo/incertidumbre/ignorancia/ambigüedad (§14) · D32.
10. **CAP-B-10** Foco 4.8 de idoneidad del plan y tres indicadores nuevos (§18, §20) · D33.
11. **CAP-B-11** Banco de casos de calibración y evaluación comparativa de mejoras (§19) · D34.
12. **CAP-B-12** Criterio de fluctuación frente a cambio estructural (§22) · D27.
13. **CAP-B-13** Mapa de oportunidades como sección de los entregables (§23) · D35.
14. **CAP-B-14** Matriz de responsabilidades consolidada (§24) · D36.

## 5. Plan de implantación resumido (sección 4 de la adenda)

- **Fase 0 (esta entrega):** nacer con las capacidades; la mayoría entran como campos, secciones, focos y comprobaciones de piezas ya existentes, con coste marginal bajo porque ningún documento está publicado.
- **Fase 1 (primeras semanas):** arranque del banco de casos de calibración por anonimización documentada de ciclos; calibración de parámetros provisionales con datos reales.
- **Fase 2 (primer trimestre):** primer cuadro de mando con los indicadores nuevos; primera evaluación comparativa si el operador la solicita; primeras fichas de régimen con estado de confianza reutilizadas.
- **Fase 3 (segundo trimestre y siguientes):** revisión trimestral comprueba la operación de D25-D36 junto con D9-D24; la ampliación del catálogo del Motor que el protocolo pudiera exigir sigue su canal propio con el Bloque A.

## 6. Fuentes de esta entrega

«Propuesta de mejoras y evolución arquitectónica del Bloque B --- Analizador de Mercados» (documento recibido del operador, 31/10/2026, 29 secciones); «Adenda de arquitectura --- Bloque B: Integración de las mejoras de la evaluación estratégica» (V1.0, 30/10/2026, con su acta D9-D24); «Documento 0 --- Protocolo maestro del Bloque B» óptima V1.1 (30/10/2026); «Diseño del Analizador de Mercados --- Bloque B» V1.1 (AM-1 a AM-10); los cinco system prompts del bloque (óptima V1.1), la «Adenda ligera --- Motor y Documentador del Motor», el «Runbook del operador», los «Objetivos del Bloque B» y los cuatro archivos operativos en sus versiones vigentes. Cada pieza de esta entrega declara además sus fuentes en su propia cabecera y en su registro de cambios.
