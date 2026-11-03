# README — índice del paquete · Bloque B — Paquete completo y verificado (2026-10-31)

**Fecha del paquete:** 31/10/2026 · **Alcance:** estado completo y consolidado del Bloque B (la cámara de análisis profundo de mercados y activos concretos) de la arquitectura Robot Investor, tras la verificación interna posterior a todas las actualizaciones · **Gobernanza:** «Documento 0 --- Protocolo maestro del Bloque B» óptima V1.3 (31/10/2026, estado consolidado) · **Idioma:** es-ES · **Estado de todo el paquete:** piezas entregadas y verificadas, pendientes de la aprobación del operador por paquetes (tipo 3, 9.2) y de su publicación coordinada de activación (5.5); nada de lo aquí contenido está en vigor hasta entonces.

## 1. Qué contiene este paquete

| Carpeta | Contenido |
|---|---|
| (raíz) | Este README y el «Informe de verificación interna --- Bloque B» (V1.0), que documenta las comprobaciones ejecutadas sobre el paquete y las correcciones aplicadas antes de la entrega |
| `01_Gobernanza/` | «Documento 0 --- Protocolo maestro del Bloque B» óptima V1.3: topología, RACI, catálogo CT-B-01 a CT-B-12, compatibilidad de versiones, glosario, protocolo on-demand (Anexo I) y actas de decisiones (Anexo J) |
| `02_System_prompts/` | Los siete system prompts del bloque, en su versión vigente a 31/10/2026 (ver matriz de la sección 2) |
| `03_Listados_funciones_tareas_cometidos/` | Los siete listados exhaustivos de funciones, tareas y cometidos (edición V1.2): uno por agente, con las series de identificadores continuadas desde la edición V1.1 y las secciones de ampliación de las olas de capacidades adaptativas y de conocimiento experto |
| `04_Objetivos/` | «Objetivos del Bloque B» óptima V1.3: los once objetivos O1-O11 en edición exhaustiva, con la nueva sección 6 de refuerzos por ola |
| `05_Archivos_operativos/` | Los cuatro archivos operativos del bloque en su esquema vigente (V1.2 los dos de información; V1.1 los dos de operación) |
| `06_Arquitectura/` | Las dos imágenes de la arquitectura en su estado consolidado: versión simplificada (esquema divulgativo con recorrido de cinco pasos y tabla de quién es quién) y por capas (las siete capas del bloque) |
| `07_Runbook/` | «Runbook del operador» V1.1: procedimientos humanos de activación, operación, seguimiento, mantenimiento y decisión (sin cambios funcionales en las olas de 31/10/2026) |
| `09_Fichas_de_agentes/` | Las siete fichas «Funciones, tareas y cometidos» (Versión óptima V1, .docx): inventario de funciones base de cada agente (series F), vigente como base de los listados exhaustivos de la carpeta 03 |
| `08_Historico_y_adendas/` | La estela de gobernanza que produce el estado actual: las dos adendas de arquitectura (30/10 y 31/10/2026), la adenda ligera del carril B, el diseño aprobado (AM-1 a AM-10), la propuesta de activación, la prueba interna, el piloto de verificación y los README de las dos entregas de system prompts de 31/10/2026 |

Cada documento se entrega en formato .md (fuente) y .docx (copia de distribución), salvo las imágenes (PNG).

## 2. Matriz de versiones vigentes (31/10/2026)

| Pieza | Versión | Cambios incorporados |
|---|---|---|
| Documento 0 --- Protocolo maestro del Bloque B | óptima V1.3 | Consolidación de estado: inventario de versiones actualizado (5.1, Anexo D), ampliaciones de referencia de los anexos de los prompts, alta de documentos de referencia en el Anexo F, compatibilidad redeclarada (5.4); sin cambios de topología, contratos ni decisiones |
| System prompt --- Analizador de Mercados | óptima V1.3 | Adendas de arquitectura (30/10 y 31/10) + conocimiento experto «Catálogo exhaustivo de análisis para un experto en todo tipo de mercados financieros»: eje de horizonte (6 ter), Anexo N, módulo K.9, regla crítica 13 |
| System prompt --- Orquestador técnico para el Analizador de Mercados | óptima V1.3 | Adendas + conocimiento experto del Orquestador: mapa de capacidades (1.6), límites de autoridad (2.7), comprobaciones B23-B25, discrepancias sin promedio (8.5), condiciones de parada (16.4), ejemplo G.7 |
| System prompt --- Auditor para el Analizador de Mercados | óptima V1.3 | Adendas + conocimiento experto del Auditor: catorce sesgos (4.7), materialidad × riesgo (5.6), siete fases (5.5), equivalencia de escalas (B.1 bis), foco 4.8 (D33) |
| System prompt --- Buscador de fuentes avanzadas para el Analizador de Mercados | óptima V1.2 | Adenda de capacidades adaptativas: ocho campos de procedencia y contexto y causa de discrepancias (D28). La ola de conocimiento experto no le afecta |
| System prompt --- Documentador para el Analizador de Mercados | óptima V1.3 | Adendas + conocimiento experto del Documentador: 17 dominios, tipología de fuentes, 18 repositorios, bibliometría, ficha de conocimiento opcional, prueba de calidad (12.4) |
| System prompt --- Motor de Cálculo Avanzado | óptima V1.4 | Conocimiento experto «Catálogo exhaustivo de cálculos y fórmulas matemáticas» (óptima V1.3: mapa de conocimiento cuantitativo, Anexo I) + corrección de referencias de versión en los esquemas JSON (óptima V1.4); catálogo 1.0 y regla 1.2 intactos |
| System prompt --- Documentador para el Motor de Cálculo Avanzado | óptima V1.6 | Conocimiento experto del Documentador del Motor (óptima V1.5: temáticas 13-16, ficha de método, módulos M1-M8, canales ampliados) + corrección de referencias de versión (óptima V1.6) |
| Listados exhaustivos (siete agentes) | edición V1.2 | Series continuadas (ORQ-B-T143-T154, AUD-B-T128-T143, ANA-B-T168-T180, BAV-B-T111-T112, DOC-B-T118-T126, MOT-B-SB51-SB56) y secciones de ampliación por ola |
| Objetivos del Bloque B | óptima V1.3 | Edición exhaustiva consolidada: once enunciados intactos y nueva sección 6 de refuerzos por ola |
| Archivos operativos | esquemas V1.2 / V1.1 | Ocho campos de procedencia y ámbito «caso de calibración» en los de información; sin cambios en los de operación |
| Runbook del operador | V1.1 | Sin cambios funcionales en las olas de 31/10/2026 |

## 3. La verificación interna, en una mirada

Antes de empaquetar, se ejecutó la verificación interna completa del bloque (informe en la raíz del paquete), que confirmó: la coherencia de versiones de las siete piezas de operación con la matriz anterior; el espejado declarado de los contratos CT-B en los prompts; la ausencia de referencias de versión desfasadas (las dos heredadas que se detectaron en el Motor y en su Documentador se corrigieron y dieron lugar a las versiones óptima V1.4 y óptima V1.6); la integridad de las series de identificadores de los listados; y la continuidad de las once decisiones de gobernanza del Anexo J. Las citas de cabecera de las piezas al Documento 0-B óptima V1.2 quedan actualizadas de pleno derecho por la óptima V1.3 conforme a la regla 5.2.3, sin exigir reedición.

## 4. Cómo usar este paquete

- **Para activar el bloque:** seguir el «Runbook del operador» (07) con la «Propuesta de activación» (08); la aprobación se tramita por paquetes conforme al 9.2 del Documento 0-B y se publica por el procedimiento 5.5.
- **Para configurar los agentes:** cargar los siete system prompts de `02/` tal cual; la PARTE II (anexos) de cada prompt puede almacenarse como archivos independientes de consulta bajo demanda.
- **Para consultar funciones y objetivos:** las fichas base (09) inventorian las funciones de cada agente (series F); los listados exhaustivos (03) las desarrollan en tareas con identificadores, y los objetivos (04) son documentos de referencia sin carácter normativo: mandan el Documento 0-B (01) y los system prompts (02).
- **Para registrar la operación:** los cuatro archivos de `05/` son la realidad registrada del bloque; cada uno tiene un único propietario de escritura (matriz 4.3 del Documento 0-B).
- **Trazabilidad:** la carpeta `08/` conserva las adendas y pruebas que produjeron este estado; la filosofía del bloque es append-only: nada se reescribe hacia atrás.
