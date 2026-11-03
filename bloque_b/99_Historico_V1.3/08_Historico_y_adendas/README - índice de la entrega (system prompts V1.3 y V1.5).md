**README --- ÍNDICE DE LA ENTREGA**

**Bloque B --- System prompts actualizados con el conocimiento experto del operador (V1.3 y V1.5)**

Fecha de la entrega: 31/10/2026 · Gobernanza vigente: «Documento 0 --- Protocolo maestro del Bloque B» (óptima V1.2, 31/10/2026) · Idioma: es-ES

---

**1. OBJETO DE LA ENTREGA**

El operador ha facilitado cuatro documentos de conocimiento experto en formato .docx, uno por agente, y ha solicitado: (a) comprobar si ese conocimiento está contemplado en el Bloque B; (b) integrar la información aportada; y (c) entregar los system prompts actualizados. Esta entrega responde a las tres peticiones: la comprobación se documenta en la sección 3, la integración se describe en la sección 4 y los system prompts actualizados acompañan a este README.

Los cuatro documentos de conocimiento recibidos son:

1. «Conocimientos que debería manejar un experto Documentador para analista de mercados» (17 bloques temáticos + recomendación final) → agente **Documentador para el Analizador de Mercados** (alias «Documentador de Mercados»).
2. «Conocimientos para el Orquestador para analista de mercados» (secciones 1--8) → agente **Orquestador técnico para el Analizador de Mercados**.
3. «Conocimiento del auditor para el analista de mercados» (secciones 1--8) → agente **Auditor para el Analizador de Mercados**.
4. «Conocimiento documentador motor de cálculo avanzado para analista de mercados» (áreas A--M + ámbitos transversales + recomendación final) → agente **Documentador para el Motor de Cálculo Avanzado**.

**2. ARCHIVOS ENTREGADOS**

| Archivo | Versión resultante | Líneas (antes → después) |
|---|---|---|
| System prompt --- Documentador para el Analizador de Mercados | óptima **V1.3** (sobre V1.2) | 346 → 435 |
| System prompt --- Orquestador técnico para el Analizador de Mercados | óptima **V1.3** (sobre V1.2) | 472 → 515 |
| System prompt --- Auditor para el Analizador de Mercados | óptima **V1.3** (sobre V1.2) | 300 → 316 |
| System prompt --- Documentador para el Motor de Cálculo Avanzado | óptima **V1.5** (sobre V1.4) | 1799 → 2129 |
| README --- índice de la entrega (este documento) | V1.0 | --- |

Cada system prompt se entrega en formato .md (fuente) y .docx (copia de distribución). Cada uno lleva su cabecera de versión actualizada, el marcado «(V1.3)» o «(V1.5)» en todo lo añadido y la fila correspondiente en su registro de cambios (Anexo H, o Anexo F en el caso del Auditor).

**3. RESULTADO DE LA COMPROBACIÓN (¿está el conocimiento contemplado en el Bloque B?)**

**Veredicto general.** El marco funcional que los cuatro documentos describen --- separación de responsabilidades entre agentes, verificación de fuentes y evidencia, trazabilidad, límites de autoridad, independencia del Auditor, control de calidad del proceso --- ya estaba contemplado en el Bloque B y en sus contratos de interfaz. Lo que estaba parcial o totalmente ausente son los catálogos, criterios y pautas de trabajo específicos de cada rol (dominios de conocimiento, repositorios, bibliometría, catálogos de sesgos, prioridades metodológicas, fichas de método, mapas de capacidades, condiciones de parada, materialidad × riesgo). Ese es exactamente el material que se ha integrado, de forma aditiva y sin tocar contratos.

**3.1 Documentador para el Analizador de Mercados (17 bloques + recomendación final)**

- Ya contemplado: verificación de fuentes y ciclo de vida completo (secciones 3--5), trazabilidad e historia de uso (Anexo B), mantenimiento híbrido D6, Fondo metodológico, delimitación con el Buscador (1.5) y ambitos de la Documentación de Mercados.
- Parcial (faltaba detalle): sectores y mercados, cadenas de valor, valoración, clases de activos, riesgo (cubiertos como ámbitos sin catálogo de conceptos), metodología científica (sin catálogo de criterios), fuentes (sin tipología completa ni tabla de repositorios), gestión del conocimiento (sin metadatos normalizados, RAG ni control de extracción) y ficha documental (4 de los 11 campos cubiertos).
- Ausente e integrado: catálogo de referencia de 17 dominios de conocimiento, tipología de fuentes documentales, tabla de 18 instituciones y repositorios (Google Scholar, Crossref, OpenAlex, Semantic Scholar, CORE, arXiv, RePEc, NBER, SSRN, OECD, World Bank, IMF, BIS, Eurostat, ECB, NIST, WIPO, EPO), principios bibliométricos y de revisión sistemática, gestión del conocimiento y trazabilidad documental, campos opcionales de la ficha de conocimiento por correspondencia con la ficha documental experta (los archivos preexistentes no se reescriben), tabla «debe conocer / debe saber hacer», los 8 bloques de conocimiento prioritario y la prueba de calidad (nueva regla 12.4).

**3.2 Orquestador técnico para el Analizador de Mercados (secciones 1--8)**

- Ya contemplado: diferencia con los demás componentes (1.1, 1.5), protocolo de solicitudes y estados (que ya recorren el mismo proceso que el flujo de 8 fases), límites de autoridad en espíritu (reglas críticas 4, 10 y 11) y condición de agente independiente.
- Parcial (faltaba detalle): descomposición de investigaciones (sin criterios de suficiencia ni finalización), metodología de análisis de mercados (sin repertorio de etapas sectoriales), coordinación de cálculos (sin distinción descriptivo/estimación/predicción/inferencia causal), gestión de evidencia (sin etiquetas dato observado/estimación/hipótesis/opinión), resolución de discrepancias (sin la regla de no promedio automático), control de calidad (sin condiciones objetivas de parada) y productos de entrega (sin contenido narrativo ampliado).
- Ausente e integrado: mapa de capacidades de los agentes del bloque (1.6), límites de autoridad declarados conjuntamente (2.7), correspondencia con el flujo funcional de ocho fases (4.5), lectura metodológica del encargo (5.6), naturaleza de los cálculos y suficiencia de los datos (6.5, con comprobaciones B23--B25), tratamiento de discrepancias sustantivas sin promedio automático (8.5), contenido narrativo ampliado del informe de ciclo (12.4), condiciones de parada y economía del ciclo (16.4) y ejemplo G.7 (mercado mundial del almacenamiento de energía), adaptado al vocabulario y los contratos del bloque.

**3.3 Auditor para el Analizador de Mercados (secciones 1--8)**

- Ya contemplado: condición de agente independiente (decisión arquitectónica vigente), estructura general de la revisión y el paquete de hallazgos CT-B-08, re-ejecución independiente CT-B-10 y calibración CT-B-11.
- Parcial (faltaba detalle): comprobaciones de fuentes y datos (unidades, duplicados, cifra oficial), razonamiento (saltos lógicos, circularidad, supuestos implícitos), métodos cuantitativos (sobreajuste, estabilidad, modelos de referencia), escenarios (restricciones, condiciones de invalidación), cobertura (lista de elementos materiales), independencia (consenso no es evidencia, dictamen condicionado) y informe (gradación comprobado/parcial/no verificado).
- Ausente e integrado: catálogo de catorce sesgos con búsqueda activa de evidencia contraria (4.7), priorización por materialidad × riesgo con revisión extraordinaria (5.6), pauta orientativa de proceso en siete fases proporcional al riesgo (5.5) y nota de equivalencia entre la escala Crítico/Alto/Moderado/Menor/Observación del conocimiento y la rúbrica vigente Material/Operativa/Menor (B.1 bis), sin renombrar severidades que los contratos citan. Las siete áreas se absorben en los focos existentes: no se crea una séptima dimensión de auditoría.

**3.4 Documentador para el Motor de Cálculo Avanzado (áreas A--M + transversales + recomendación final)**

- Ya contemplado: 12 de las 13 áreas de métodos (temáticas 1--12 del catálogo 6.7), protocolo de verificación, ficha de fuente, mapa de coberturas y canales básicos (BIS, BCE, arXiv).
- Parcial (faltaba detalle): valoración cuantitativa (VAN/TIR cubiertos; faltaban WACC, múltiplos, opciones reales, punto de equilibrio), paquete metodológico adaptado al problema, regla de adopción de métodos, ámbitos transversales (calidad de datos, computación científica, investigación metodológica) y prioridades de construcción de la biblioteca.
- Ausente e integrado: temáticas 13 (teoría de la información, señales y patrones), 14 (redes y sistemas complejos), 15 (métodos cuantitativos del análisis de mercados: tamaños, cuotas, HHI, elasticidades, volumen/precio/mezcla, difusión, curvas de aprendizaje) y 16 (valoración económica y análisis financiero cuantitativo); ficha de método normalizada como nivel opcional sobre la ficha de fuente (9.2 bis + fila en Anexo D); organización modular M1--M8 como divisiones funcionales de conocimiento, no agentes (9.3 bis); prioridades 1--3 (sección 2); paquete metodológico adaptado con el ejemplo de aceleración estructural (8.3, 10.1); adopción exigente de métodos (7.8); canales ampliados con revistas de referencia (Journal of Econometrics, JASA, JMLR, Annals of Statistics), NIST/SEMATECH, OECD y documentación de software científico (NumPy, SciPy, statsmodels, scikit-learn, PyMC) y repositorios (OpenAlex, Crossref, arXiv, GitHub), con la advertencia de que preprints y código no son automáticamente evidencia validada.

**4. CARÁCTER DE LA INTEGRACIÓN**

- **Aditiva y verificada**: nada se ha eliminado, renumerado ni contraído; las comprobaciones por diff confirman que los contratos de interfaz (Anexos F/D de contratos) quedan byte a byte idénticos en los cuatro prompts y que los esquemas de datos vigentes no cambian.
- **Sin cambios de contratos ni de arquitectura**: la topología de los siete agentes, los contratos CT-B-xx y las decisiones del Documento 0-B V1.2 siguen en vigor. Los campos o filas opcionales añadidos a esquemas (ficha de conocimiento del Anexo C; ficha de método del Anexo D del Documentador del Motor) están declarados como tales y no obligan a reescribir archivos operativos preexistentes.
- **Adaptación al vocabulario del bloque**: los ejemplos y pautas del conocimiento experto se han reformulado con la terminología del Bloque B (plan F0, rúbrica B, estados del protocolo, familias PROC/SUST, HIP-B, REC-B, PRV-B, carril B del Motor).
- **Pendientes de gobernanza (declarados, no ejecutados)**: (i) reflejar en la próxima actualización coordinada del Documento 0 las ampliaciones de anexos de referencia; (ii) en el Documentador del Motor, el Anexo A conserva «prompt_version óptima V1.1» y el Anexo E «optima_v1», desfasados heredados del base, cuya actualización es decisión del operador.
- **Nota de fidelidad**: el documento de conocimiento del Documentador para el Analizador contenía cinco líneas residuales de raspado web (titulares de prensa y referencias a plataformas) sin valor de conocimiento; se excluyeron de la integración.

**5. COHERENCIA CON LAS ENTREGAS PREVIAS**

Los system prompts del **Analizador de Mercados (V1.3)** y del **Motor de Cálculo Avanzado (V1.3)**, entregados en la carpeta «Bloque B --- System prompts V1.3 --- Integración del conocimiento experto (2026-10-31)», no requieren cambios: esta entrega afecta a los otros cuatro agentes del bloque y no altera ningún contrato de interfaz con ellos. Los tres prompts de la V1.2 y el V1.4 del Documentador del Motor quedan sustituidos por las versiones aquí entregadas; las filas de sus registros de cambios quedan preservadas (filosofía append-only). La activación formal de estas versiones corresponde a la publicación coordinada del procedimiento 5.5 del Documento 0-B, conforme al patrón de las olas de activación anteriores.
