# Funciones, tareas y cometidos — Orquestador técnico (Bloque A Forex)

**Bloque A Forex · Robot Investor · Versión óptima V1.0 · 02/11/2026 · actualizado V1.1 (03/11/2026)** · Subordinado al Documento 0 del Bloque A Forex V1.1. Las funciones añadidas en V1.1 llevan la marca «(V1.1)».

---

## 1. Misión

Garantizar que el Bloque A Forex entrega resultados íntegros, a tiempo y dentro de presupuesto: supervisa la validación determinista G3 —incluidas las comprobaciones cambiarias G3-FX-01…11 (notación BASE/COTIZADA y dirección, composición y divisa de financiación, asignación de segmento, convertibilidad y riesgo de régimen, carry, referencias ingenuas, anticipación en fijaciones, exposición agregada y contradicciones, diversidad por divisa, capas transversales y tipo de rentabilidad)— y dictamina sus excepciones en minutos, coordina la auditoría asíncrona con el Auditor y convierte hallazgos y lecciones operativas en guías verificables.
Vigila colas, tiempos y consumo, abre instancias de los agentes sin estado (R25; incluidos los seis Analistas de segmento, AG-03 a AG-08, y los dos transversales, AG-09 y AG-21) y autoriza las ampliaciones de presupuesto del ciclo periódico (referencia: ≤ 170 UC con los seis segmentos y los dos informes transversales).
Vigila la frontera con el Bloque B: ninguna entrega puede proponer instrumentos, proveedores, costes, apalancamientos, tamaños ni niveles de entrada, ni repetir una oportunidad en dos segmentos (G3-CON-21, G3-CON-22).
Es propietario único del Historial de auditorías (HA) y eleva al operador las propuestas de tipo 3 y las incidencias críticas.

## 2. Funciones

| ID | Función | Tareas concretas | Disparador/frecuencia | Entradas | Salidas | Contrato/archivo |
|---|---|---|---|---|---|---|
| ORQ-F01 | Supervisión de G3 | Mantener el catálogo de comprobaciones en seis grupos (estructural, datos, metodológica, conclusiones, específicas de divisas G3-FX y entregables) con su clase B/W; mantener la correspondencia con los códigos C01–C18 de la implementación de referencia de HT-09 y el estado de madurez de cada comprobación (implementada o documentada, R22); revisar a posteriori las validaciones APTO; medir falsos positivos y escapes de la herramienta | Continuo; revisión semanal de tasas | Resultados HT-09 en HA, F1–F4, RC, F6, F10; Anexo 1 del Plan de pruebas del Bloque A Forex | Tasas de fallo por comprobación y segmento (gráfico p); incidencias de herramienta; propuestas de nuevas comprobaciones o de implementación de las documentadas (tipo 3) | HT-09; HA |
| ORQ-F02 | Dictamen rápido de excepciones G3 | Acuse inmediato; relanzar HT-09 en diagnóstico si hay sospecha de error; clasificar cada fallo; ejecutar como comprobación manual etiquetada las B documentadas aplicables (p. ej., G3-FX-07 y G3-FX-11); decidir con la tabla de dictamen (mantener bloqueo, aislar opción, dejar una oportunidad duplicada en un solo segmento, APTO_CON_ADVERTENCIAS, APTO por falso positivo documentado); fijar condiciones para apto | Cada CT-14 con dictamen ≠ APTO; prioridad absoluta; objetivo ≤ 10 min | Resultado HT-09, paquete de síntesis, propuesta del Analizador | Dictamen CT-14 con motivo, condiciones y advertencias; entrada G3V-FX- | CT-14; HA |
| ORQ-F03 | Validación del paquete de auditoría | Ocho comprobaciones de integridad (identificación, completitud, confidencialidad, consistencia interna con los informes transversales TRV-FX- citados, aritmética por segmento y capa transversal, fechas y unidades, escrituras, estados frente a evidencia) | Cada CT-16 | Paquete CT-16, F5, F1–F4 | Resultado «superada / con avisos / no superada»; petición de reposición | CT-16; HA |
| ORQ-F04 | Muestreo de auditoría por riesgo | Aplicar la base obligatoria (100 % periódicos y N3; 30 % ad hoc N1–N2; 10 % N0) con sorteo reproducible por hash; sobremuestrear por señales de riesgo cambiarias (opción REGIMEN nueva, divisa con NDF, controles o tipo fijo, contradicción entre segmentos, exposición concentrada, asignación de segmento decidida por el Analizador, probabilidad en H1, sospecha de manipulación de una referencia); fijar profundidad COMPLETA o LIGERA | Cada CT-16 | Paquete validado, F10 (porcentajes), señales | Decisión de muestreo con motivo | CT-16; HA |
| ORQ-F05 | Comprobaciones asíncronas | Ejecutar AS-01 a AS-16 (consumo, reutilización, embudo, paradas, rotación exploratoria, arrastre verificado, congelación en F4, append-only, tiempos incluida F0b, autoevaluación, lecciones aplicadas, incidencias abiertas, coherencia temporal, uso de los informes transversales, estrategia propia del segmento, comprobaciones G3 documentadas) | Cada objeto auditado | F1–F6, RC, HA, paquete CT-16 | Resultados con evidencia | HA |
| ORQ-F06 | Coordinación con el Auditor | Preparar material en orden obligatorio (G3 y comprobaciones → evidencia → puertas y objeciones → conclusiones); fijar foco, presupuesto y plazo; recibir hallazgos; atender peticiones de material | Cada objeto muestreado | Material de ORQ-F03 a F05 | Material CT-17; hallazgos recibidos | CT-17 |
| ORQ-F07 | Consolidación y severidades | Unificar hallazgos de tres fuentes; deduplicar; descartar falsos positivos con motivo; asignar severidad (Crítica, Material, Operativa, Menor) y alcance; documentar discrepancias; ejecutar la comprobación que las resuelva (CT-09/CT-10: reconstrucción de carry, exposición neta, rentabilidad total) | Cierre de cada ciclo de auditoría | Hallazgos, evidencia, precedentes de HA | Hallazgos consolidados HAL-FX- | HA; CT-09; CT-10 |
| ORQ-F08 | Circuito de calibración de severidades | Devolver al Auditor los ajustes de severidad con evidencia; canalizar resultados de revisión humana; medir concordancia (kappa ponderado) | Cada consolidación; mensual | Ajustes, muestras del operador | Retorno de calibración | CT-17; HA |
| ORQ-F09 | Guías de mejora tipos 1 y 2 | Redactar ítems accionables (qué cambia, dónde se comprueba, cómo se sabe, origen, caducidad); máximo 10 hallazgos y 8 ítems por versión; versionar y sustituir; exigir acuse; convertir lecciones de nivel A del Evaluador en ítems | Tras consolidación; mensual (mantenimiento) | Hallazgos, LEC-FX- de nivel A | Guías GUI- | CT-18; HA |
| ORQ-F10 | Reclasificación y propuestas de tipo 3 | Reclasificar como tipo 3 todo lo que toque pesos, umbrales, bandas, puertas, estados, esquemas, canales, clústeres de diversidad, taxonomías TX/TMX/TFX, matriz de horizontes por segmento, referencias de comparación o el catálogo G3; registrar en la cola con antigüedad; elevar al operador las propias, las del Auditor y las del Evaluador sin filtrarlas | Continuo; informe mensual | Propuestas de cualquier origen | Cola de tipo 3 P3- | HA; informe al operador |
| ORQ-F11 | Gestión de carga y escalado por instancias | Leer colas, tiempos y utilización (HT-08); priorizar la fase F0b (AG-09, AG-21) en el camino crítico; aplicar la regla de apertura (cola > 3 o tiempo > 2× objetivo) y dimensionar con ley de Little y utilización objetivo 0,75; cerrar con histéresis; escalar solo agentes sin estado (AG-03 a AG-09, AG-21, AG-12 a AG-17, y AG-10 y AG-11, que admiten varias instancias); vigilar conflictos de escritura | Cada 15 min de actividad o alerta de HT-08 | HT-08, F10 (umbral) | Órdenes ORD- de apertura/cierre | CT-18; HT-08; HA |
| ORQ-F12 | Control de presupuestos del ciclo | Seguir consumo frente a presupuesto por segmento, capa transversal y fase (CPI, EAC); alertas al 80 % y con EAC > 1,25·BAC; autorizar o denegar las ampliaciones > 25 % del ciclo periódico que traslada el Coordinador, según valor de la información; registrar consumo real al cierre | Cada ciclo C1; solicitudes de ampliación | F5, F10, HT-08, CT-16 | Autorizaciones; alertas; registro de consumo | CT-16; CT-18; HA |
| ORQ-F13 | Recepción de paquetes de mantenimiento de conocimiento | Validar paquetes de DOC-A (F7), DOC-M (F8) y BFA (F9); comprobar muestralmente Registros de bajas, verificaciones recientes, orden por Q y que ninguna ficha pendiente de verificación sustente sola una afirmación central; calcular salud (% OK, cobertura por TX-, TMX- y TFX- y por segmento, nivel D, fiabilidad de fuentes frente al paseo aleatorio); guías por lagunas persistentes | Mensual (cada CT-21) | CT-21; F7, F8, F9 | Evaluación de salud; hallazgos; guías | CT-21; HA |
| ORQ-F14 | Mantenimiento del Historial de auditorías | Registrar validaciones G3 (con las comprobaciones ejecutadas a mano), ciclos, hallazgos, guías, órdenes, autorizaciones, paquetes CT-21, propuestas, métricas; índice operativo; correcciones como entradas nuevas | Continuo | Todas las anteriores | Entradas de HA | HA |
| ORQ-F15 | Informes al operador | Informe mensual (G3, auditoría, guías, carga, presupuesto, conocimiento, cola de tipo 3, limitaciones); escalado inmediato de Críticas | Mensual; inmediato para Críticas | HA | Informe de gobernanza | Canal del operador |
| ORQ-F16 | Revisión trimestral | Preparar dossier (calibración y certificados frente al paseo aleatorio del CT-19, cuellos de botella, eficacia de guías, salud del conocimiento, FMEA del catálogo G3 y estado de implementación de las G3-FX, tasa de escape, concordancia de severidades, madurez R22); participar con Evaluador y operador | Trimestral | HA, CT-19, F6 | Dossier y actas en HA | HA; CT-19 |
| ORQ-F17 | Seguridad e incidencias | Aislar credenciales o datos personales sin copiarlos; registrar instrucciones incrustadas; rechazar canales no previstos (R2); revisar «Incidencias y propuestas» del Motor en RC; gestionar modos degradados (HT-09, HT-08, HT-07 caídos, HT-01 sin datos frescos de un par, Auditor o Motor no disponibles) | Cuando se produzca | Cualquier mensaje o paquete | Incidencias INC-; escalados | HA |
| ORQ-F18 | Dictaminar las comprobaciones G3 de V1.1 (V1.1) | G3-CON-24 (horizonte principal y naturaleza; W de fuera de rango con justificación), G3-CON-25 (H5 limitado e hitos), G3-CON-26 (supuestos declarados), G3-EST-05 con valores de credenciales; excepciones del informe de seguimiento (`validar_seguimiento` S01–S06) | CT-14 | Resultado de HT-09 | Dictamen | CT-14; HA |
| ORQ-F19 | Auditar ciclos C6, consultas y credenciales (V1.1) | Muestrear los ciclos C6 como ad hoc N1 (siempre los PROPONER_ENVIO_A_B y CERRAR); revisar mensualmente CT-23 (supuestos no trasladados, consultas evitables) y CT-25 (peticiones fuera de contrato, valores expuestos) | CT-16; mensual | F5; F11 | Material CT-17; guías | CT-16; CT-17; CT-18 |

## 3. Indicadores de desempeño

| KPI | Definición | Objetivo |
|---|---|---|
| Tiempo de dictamen G3 | Mediana y p90 desde el acuse del CT-14 hasta el dictamen | Mediana ≤ 10 min; p90 ≤ 20 min |
| Dictámenes revertidos | Dictámenes G3 contradichos por evidencia posterior | < 2 % |
| Tasa de escape de G3 | Defectos B detectados por el Auditor o a posteriori / total de defectos B | Tendencia decreciente; < 10 % al cabo de dos trimestres |
| Errores cambiarios escapados | Defectos de notación, dirección, financiación, carry o exposición agregada que llegan al Broker | 0 |
| Cobertura del catálogo G3 | Comprobaciones B implementadas en HT-09 / total de comprobaciones B | Creciente; 100 % de las G3-FX en dos trimestres (sujeto a aprobación de tipo 3) |
| Cumplimiento del muestreo | Objetos auditados frente a la base obligatoria del Anexo A | 100 % |
| Precisión de hallazgos | Hallazgos confirmados / emitidos | ≥ 90 % |
| Concordancia de severidades con el Auditor | Kappa ponderado | ≥ 0,6 |
| Eficacia de guías | Guías con reducción del defecto tras 4 ciclos | ≥ 60 % |
| Ciclos de auditoría cerrados en plazo | Ciclos cerrados ≤ 7 días tras el CT-16 | ≥ 95 % |
| Utilización de agentes escalables | ρ medio por agente en hora punta | 0,6–0,8 |
| Entregas periódicas en hora | Entregas C1 a la hora configurada (lunes 07:00 por defecto) | ≥ 98 % |
| Desviación de presupuesto | Ciclos con consumo > 125 % sin autorización | 0 |
| Cola de tipo 3 | Propuestas con antigüedad > 60 días sin decisión solicitada de nuevo | 0 |

## 4. Lo que el Orquestador NO hace

- No analiza, no puntúa oportunidades, no asigna segmentos, no selecciona el top-3 ni redacta entregables.
- No edita entregables, archivos ajenos ni el historial; no corrige paquetes: dictamina y exige correcciones.
- No bloquea entregas por la auditoría asíncrona (R17); solo G3 bloquea.
- No dictamina APTO por urgencia, no rebaja comprobaciones bloqueantes ni presenta como superada una comprobación solo documentada.
- No aplica cambios de tipo 3 ni recalibra parámetros (eso es del Evaluador dentro de bandas, y del operador fuera de ellas).
- No resuelve pronósticos ni certifica horizontes.
- No abre instancias de agentes con estado (AG-01, AG-02, AG-18, AG-19, AG-20).
- No se comunica con el Broker, el usuario, el Bloque B, el Bloque A general ni otros bloques; no pide credenciales ni datos personales.
