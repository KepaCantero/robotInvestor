# T-53 · Revisión del Bloque A con el operador

| Campo | Valor |
| --- | --- |
| Estado | CERRADO (QA r02 APTO, 9-11-2026); las propuestas PA-01 a PA-21 esperan la decisión del operador |
| Pieza | bloque_a |
| Planifica · implementa · QA | claude · claude · Astra o un revisor nuevo sin contexto |
| Aprobación del operador | Encargo del 2026-11-09: «revisa y corrige posibles errores o fallas; evalúa si es posible optimizar la arquitectura o algún agente». Las propuestas de arquitectura las decide él |
| Deuda técnica | T-53 en `sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md` |

## Objetivo

Encargo del operador (9-11-2026): «1) quiero que lo revises y corrijas posibles errores o fallas, 2) evalúa si es posible optimizar/mejorar la arquitectura o algún agente». Revisar el Bloque A (V5.1) frente a su Documento 0 y a la Constitución V0.6, corregir los defectos verificados y presentar al operador las mejoras de arquitectura y de agentes para decidirlas con él antes de conectar A (D-42, regla 9 del §14).

## Alcance

- Entra:
  1. **Diagnóstico** con tres revisiones independientes en paralelo: defectos de código del ejecutor (CA-xx), coherencia entre la especificación y el código (CS-xx) y evaluación de la arquitectura y los agentes (PA-xx). Claude verifica cada hallazgo antes de actuar.
  2. **Corrección** de los defectos verificados del ejecutor (código y pruebas de `bloque_a/11_Ejecutor/`), cada uno con su prueba de regresión.
  3. **Propuestas** de arquitectura y de agentes, priorizadas, para decidirlas con el operador.
- No entra:
  - cambiar el corpus congelado (prompts, catálogo, esquemas, plantillas) sin decisión expresa: si una corrección lo exige, se propone;
  - implementar las propuestas de arquitectura, que tendrán su ticket cuando el operador decida;
  - el Bloque B (T-62).

## Diseño

- Contratos: no cambian los CT de A; la conexión a CT-G es una propuesta.
- Estado persistido: no cambia, salvo que una corrección lo exija (se anotaría aquí).
- Números: los de las correcciones, de `config/por_defecto.yaml` o del Anexo A del Documento 0.
- Cómo falla cerrado: cada corrección se prueba también con entradas ausentes o inválidas.
- Decisiones del operador: ninguna se toma aquí; las propuestas van a la reunión con él.

## Riesgos

| Riesgo | Consecuencia | Mitigación |
| --- | --- | --- |
| Corregir contra una lectura equivocada del Documento 0 | Un «arreglo» que rompe una regla | Cada corrección cita la sección del Documento 0 y la revisa un agente distinto |
| Tocar el corpus congelado sin querer | Gate de integridad en rojo | Solo se toca `11_Ejecutor/`; lo del corpus, como propuesta |
| Hallazgos de revisores sin verificar | Trabajo sobre falsos positivos | Claude reproduce cada hallazgo antes de corregirlo |

## Criterios de aceptación (binarios)

1. CA-1: cada defecto corregido tiene una prueba que falla sin la corrección y pasa con ella.
2. CA-2: las pruebas de A siguen en verde y la línea base sube con las nuevas; gate completo 12/12.
3. CA-3: cada hallazgo no corregido queda con su motivo (falso positivo, corpus, decisión del operador) en `analisis-tecnico.md`.
4. CA-4: las propuestas de arquitectura y de agentes, priorizadas y con beneficio, coste y riesgo, quedan presentadas al operador.

## Plan de pruebas

| Prueba | Tipo (nominal, límite, fallo cerrado, regresión, migración, integración) | Criterio |
| --- | --- | --- |
| … | … | CA-1 |

## Scripts

<Scripts de `.docs/scripts/` que usa o crea este ticket.>

## Registro

- 2026-11-09 · ABIERTO · creado con nuevo_ticket.sh
- 2026-11-09 · EN CURSO · claude · plan con diagnóstico en tres revisiones paralelas, correcciones y propuestas
