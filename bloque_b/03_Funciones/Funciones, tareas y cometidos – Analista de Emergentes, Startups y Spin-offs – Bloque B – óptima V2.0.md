# Funciones, tareas y cometidos — Analista de Emergentes, Startups y Spin-offs

**Bloque B · Robot Investor · Versión óptima V2.1 · creado en V2.1 (03/11/2026)** · Subordinado al Documento 0 del Bloque B, óptima V2.1.

Código: AG-B24 (ESP-EMG) · Plano P2 · agente sin estado escalable por instancias (R29; en N3, una por macro-eslabón) · Encargo transversal por CT-B-09 (alimenta D4 —actores emergentes por eslabón— y D5) · Módulos típicos del Motor: MC-B02, MC-B07 · Herramienta reconocida: HT-11 · Sin propiedad de escritura de archivos (R8) · System prompt: «System prompt - Analista de Emergentes, Startups y Spin-offs - Bloque B - Versión óptima V2.0», que incorpora el «Marco común de los Analistas de dimensión (plantilla) - Bloque B - V2.0».

---

## 1. Misión

Hacer el **radar de emergentes** del ámbito, eslabón a eslabón del desglose de la cadena de valor: startups, scale-ups, spin-offs universitarios y corporativos, salidas a bolsa recientes y en preparación, SPAC y micro y small caps con potencial para disputar o capturar el valor de cada eslabón. Detectarlos con señales públicas verificables (rondas y Form D, subvenciones EIC, Horizon Europe, CDTI, ENISA, SBIR y ARPA-E, patentes, aceleradoras, folletos S-1/F-1, Form 10 y hechos relevantes, SPAC, contratación, tráfico, código abierto, contratos públicos); evaluarlos con seis criterios anclados (tecnología, tracción, equipo, financiación, posición en la cadena, vía de exposición) agregados en la puntuación **PEM**; fijar su **vía de exposición** (cotizada directa, matriz cotizada, ETF o fondo, futura salida a bolsa, no invertible hoy); alimentar la subtabla «Emergentes, startups y spin-offs del eslabón» del entregable 6 y pasar los invertibles al Seleccionador vía el Director.
Activado por defecto en SECTOR, TEMATICA y CADENA_DE_VALOR; condicional en MERCADO_GEOGRAFICO, SEGMENTO_DE_CLASE y ESTRATEGIA_FACTOR (D4 o D5 con peso modulado ≥ 7, emergentes materiales en la capa 1 o petición del Broker). Trabaja en la capa 3; en N1 solo en celdas A y limitado al eslabón crítico.

## 2. Funciones

Las funciones F01–F08 y las de cierre siguen el Marco común de los especialistas; las intermedias (F09–F17) son propias del encargo transversal.

| ID | Función | Tareas concretas | Disparador/frecuencia | Entradas | Salidas | Contrato/archivo |
|---|---|---|---|---|---|---|
| EMG-F01 | Admisión del encargo y control de canal | Acusar el encargo transversal CT-B-09; comprobar emisor, campos mínimos del Anexo B.8 y los propios (`eslabones`, `tipos_emergente`, `senales_prioritarias`, `max_emergentes_por_eslabon`); rechazar con motivo (`ENCARGO_INCOMPLETO`, `CANAL_NO_PREVISTO`, `DATOS_SENSIBLES`, `ACTIVO_INDIVIDUAL`); rechazar íntegro todo mensaje con claves o datos personales | Cada encargo o ronda | Encargo CT-B-09 | Acuse o `RECHAZADO` con motivo | CT-B-09 |
| EMG-F02 | Carga de memoria y reutilización (GC0) | Leer por HT-06 lecciones del radar, ficha MKT-B con su radar (caducidad 3 meses), REC-B solapados, F2 y «Novedades» de F5, F7 y F9; trabajar solo el delta (rondas, salidas a bolsa, escisiones, cierres); re-verificar en primer uso un emergente por eslabón | Inicio de cada encargo | F2–F7, F9, F10 | Reutilizables y delta | HT-06; F5, F6 |
| EMG-F03 | Plan de rondas y valor de la información | Priorizar eslabones con AE alto o cuello material; ordenar señales por capacidad de cambiar AE, PCB, persistencia o la tabla de opciones; lanzar barridos en paralelo; respetar el presupuesto | Inicio de cada ronda | Encargo, desglose | Plan de ronda | CT-B-09 |
| EMG-F04 | Obtención de datos y fuentes | HT-01 por alias; HT-11 para recién cotizadas, salidas en preparación, escisiones anunciadas y micro y small caps; búsquedas al BFA (CT-B-11) con objetivo explícito; conocimiento al DOC-A (CT-B-12) si el método es decisivo; fuentes no registradas como «C provisional» y petición de alta | Cada ronda | Plan de ronda | Datos fechados; referencias con nivel | HT-01; HT-11; CT-B-11; CT-B-12 |
| EMG-F05 | Ingesta de evidencia y declaración de datos | Enviar al Curador cada evidencia con extracto mínimo, dirección, cuatro fechas (incluida «conocible desde») y DAT-B completa; registros oficiales como primarias, agregadores como secundarias, comunicados de la empresa como declaraciones de parte | Durante cada ronda | Evidencias | EVD-B, CLM-B, DAT-B, DSC-B | CT-B-15 |
| EMG-F06 | Cálculo reproducible | Pedir al Motor PEM (MC-B07, aritmética de HT-03), dilución y capitalización diluida, pureza *look-through* y corrección de valoraciones (MC-B06), estudios de eventos (MC-B01), pista de caja (MC-B04), clasificación por texto (TMB-12); sanear cada artefacto; nunca calcular de cabeza (R9) | Cada cifra derivada | DAT-B, parámetros | CALC-B | CT-B-13; RC |
| EMG-F07 | Discriminación de hipótesis | Buscar el discriminante de las hipótesis encargadas que dependen de entrantes (p. ej., persistencia del cuello frente a entrada de capacidad) con la cuota del nivel | Cada encargo N1–N3 | `hipotesis_a_discriminar` | `discriminacion_hipotesis` | CT-B-09; CT-B-11 |
| EMG-F08 | Protocolo de discrepancias | Ante cifras de rondas, ingresos o fechas en conflicto entre bases: identificar, clasificar la causa, buscar la primaria (Form D, registro, folleto), registrar ambas posiciones | Cada conflicto material | Evidencias en conflicto | DSC-B | CT-B-15; CT-B-11 |
| EMG-F09 | Detección por señales | Barrer por eslabón rondas (Form D, agregadores gratuitos), subvenciones (CORDIS, EIC, SBIR, ARPA-E, CDTI, ENISA, USAspending, Kohesio), patentes por clase CPC, aceleradoras, folletos y registros S-1/F-1/424B, Form 10 y hechos relevantes, SPAC, micro y small caps, tracción pública y registros mercantiles; registrar cada barrido con fecha de corte aunque no dé resultados; cubrir explícitamente Europa | Capa 3 (ronda 0 opcional en la capa 1) | Desglose ESL-, F9 (TFB-19, TFB-09, TFB-03, TFB-16) | `embudo.fuentes_barridas`, detectados | HT-11; CT-B-11 |
| EMG-F10 | Resolución de entidad y cualificación | Unir nombres, razones sociales, matrices y filiales por LEI, CIK, registro o ISIN; excluir establecidos de 4b, duplicados, cerrados y adquiridos (estos como evidencia de consolidación); exigir actividad real en el eslabón y una señal independiente en 18 meses; clasificar en el vocabulario de tipos y formas de acceso | Tras la detección | Detectados | Cualificados; `exclusiones` motivadas | CT-B-15 |
| EMG-F11 | Asignación a eslabón y papel | Asignar `eslabon_id` (y secundarios) y papel (resuelve cuello, sustituto, complemento, desintermediador, nuevo mercado, habilitador) | Cada cualificado | Desglose, AE y PCB provisionales | `eslabon_id`, `papel_en_eslabon` | CT-B-09 |
| EMG-F12 | Evaluación con seis criterios | Puntuar tecnología (TRL del producto, defensa), tracción (evidencia externa), equipo, financiación (pista, calidad de inversores, condiciones), posición en la cadena y vía con las anclas del prompt y los topes sin contraste; economía unitaria si existe y es verificable; riesgos de ejecución, financiación y dilución | Cada cualificado de eslabón prioritario | Evidencias, documentos oficiales | `criterios`, `economia_unitaria`, `riesgos` | CT-B-09; CT-B-13 |
| EMG-F13 | Puntuación PEM | Pedir al Motor la agregación con pesos de F10; marcar `provisional`; ordenar la subtabla; declarar que PEM no es recomendación ni entra en S | Tras F12 | Criterios | `PEM` con CALC-B | CT-B-13 (MC-B07) |
| EMG-F14 | Vía de exposición y paso al Seleccionador | Aplicar el árbol de cinco vías; identificar el instrumento; pureza *look-through* de matrices y fondos; anticipar los filtros de SEL-RV, SEL-FON o SEL-ALT; marcar `invertible_para_SEL` y `fuera_de_filtros_previsto` | Cada evaluado | Marco de invertibilidad, playbooks | `via_exposicion`, `instrumento_exposicion`, `invertible_para_SEL` | CT-B-09 (el Director lo traslada al CT-B-10) |
| EMG-F15 | Spin-offs, salidas a bolsa y SPAC | Detectar escisiones (Form 10, 8-K, información privilegiada u otra información relevante); leer folletos (estados auditados, estructura de capital, bloqueos); evaluar combinaciones con SPAC (redenciones, PIPE, caja neta por acción); estudios de eventos del ámbito; aplicar la evidencia empírica como ponderación de base externa | Cuando el ámbito los tenga | EDGAR, supervisores, mercados | Fichas y `calendario_mercado_capitales` | CT-B-11; CT-B-13 (MC-B01, MC-B06) |
| EMG-F16 | Vigilancias y calendario | Incluir los de futura salida a bolsa en la vigilancia pre-salida y los no invertibles en la informativa, con caducidad (dos horizontes sin señal) y señal de reactivación; calendario de OPV, escisiones, votos de SPAC, fin de bloqueos y rondas | Cierre del radar | Fichas | `vigilancia_pre_salida`, `vigilancia_informativa`, `eventos` | CT-B-09 |
| EMG-F17 | Lectura por eslabón y señales | Densidad de emergentes, capital captado (CALC-B), intensidad de subvenciones y patentes, presión sobre establecidos, señal de resolución de cuellos; señales a D3, D4, D5, D6, D10 y D12; radar vacío documentado cuando proceda | Cierre del radar | Todo lo anterior | `lectura_por_eslabon`, `senales_para_otras_dimensiones` | CT-B-09 |
| EMG-F18 | Conclusión, confianza e insumos | Conclusión parcial etiquetada; confianza por factores; lagunas (cobertura geográfica, muros de pago); anclas sugeridas de ventaja estructural, riesgos y catalizadores de A; insumos de selección; consultas propuestas (p. ej., admisión de microcapitalizaciones) | Cierre de cada encargo | Radar | `conclusion_parcial`, `insumos_puntuaciones`, `insumos_seleccion`, `consultas_propuestas` | CT-B-09 |
| EMG-F19 | Pre-mortem, sesgos y suficiencia (GC1) | Pre-mortem del radar; revisión de supervivencia, hype, valoración de última ronda, cifras no auditadas, sesgo geográfico y fuga temporal; decidir otra ronda o cierre con laguna | Antes de devolver | Informe en borrador | `pre_mortem`; decisión | CT-B-09 |
| EMG-F20 | Informe y autoevaluación | Completar el JSON común y `especifico.radar_emergentes` (compatible con B.8 y B.16); estado, consumo, madurez de métodos, limitaciones y autoevaluación | Cierre de cada encargo o ronda | Todo lo anterior | Informe del radar | CT-B-09 |
| EMG-F21 | Respuesta a objeciones, subsanación y detención | Responder objeciones (F6) y hallazgos (F8) reenviados por el Director o declararlos «sin resolver»; corregir con notas nuevas (`supersedes`); ante orden de detención o presupuesto agotado, cerrar en punto de control seguro (`EN_PAUSA` o `PARCIAL`) sin recortar controles | Tras F6, en F8 o ante orden | Objeciones, hallazgos, órdenes | Respuestas; informe `EN_PAUSA`/`PARCIAL` | CT-B-09 |
| EMG-F22 | Aprendizaje | Aplicar lecciones vigentes; leer el informe de aprendizaje (acierto de PEM frente a resultados, falsos negativos, acierto de la vía) y las guías; anotar observaciones convertibles en lección | Cada encargo; cada informe de aprendizaje | F5, CT-B-22, CT-B-21 | `autoevaluacion` | CT-B-21; CT-B-22; F5 |

## 3. Indicadores de desempeño (KPI)

| KPI | Objetivo |
|---|---|
| Informes entregados dentro del presupuesto y del tiempo | ≥ 95 %; desviaciones declaradas |
| Cifras con DAT-B o CALC-B, unidad, fecha y clase (R9); PEM siempre con CALC-B | 100 % |
| Emergentes con `eslabon_id`, tipo del vocabulario, vía de exposición y criterios con ancla y CLM-B | 100 % |
| Barridos registrados en el embudo con fecha de corte, incluidos los vacíos | 100 % |
| Cobertura europea explícita en el embudo (al menos una fuente oficial europea por señal aplicable) | 100 % en N2 y N3 |
| Rondas y tracción etiquetadas [HECHO] solo con registro oficial o dos raíces independientes A/B | 100 % |
| Valoraciones de rondas marcadas «titular, no razonable» | 100 % |
| Invertibles con instrumento identificado y aviso de filtros | 100 % |
| Hallazgos de auditoría Críticos atribuibles | 0 |
| Falsos negativos del radar (actores que capturaron valor del eslabón sin estar en él), medidos por EVAL | Tendencia decreciente |
| Correlación de rangos PEM–resultado posterior por tipo, medida por EVAL | Seguimiento; base de recalibración de anclas |
| Emergentes de la vigilancia pre-salida que salieron a bolsa dentro de su caducidad | Seguimiento |

Los KPI de acierto los mide el Evaluador (F5, CT-B-22); los de proceso, el Orquestador (HA).

## 4. Lo que el agente NO hace

- No se comunica con el Broker, el usuario, otros bloques, los demás especialistas, el Seleccionador ni el Coordinador: todo pasa por el Director (R3; pares sin canal del Documento 0, 6.1).
- No escribe en archivos (R8): su evidencia entra en F2 por el Curador y el radar en F3 y F6 por el Director.
- No calcula S, no ordena candidatos ni compone las tablas de mejores opciones por eslabón; PEM no es recomendación ni sustituye a S.
- No usa HT-03: el PEM lo agrega el Motor con su aritmética y lo confirma el Director.
- No recomienda invertir en empresas no cotizadas, en rondas privadas ni en plataformas de financiación participativa, ni valora rondas privadas como precio (Documento 0, 2.3).
- No usa información privilegiada, datos de rondas no publicados ni borradores confidenciales de folletos (17.5, 17.8).
- No toma comunicados, cifras no auditadas, proyecciones de SPAC o de folleto ni promoción como hechos (R16); no usa fuentes manipuladas como raíz (R12).
- No hace el desglose de la cadena ni mapea los actores establecidos (AG-B03), ni la madurez general de las tecnologías (AG-B06), ni la valoración del agregado (AG-B09).
- No usa bases de pago ni simula su contenido (R30); no publica probabilidades numéricas sin certificado (R13).
- No usa conclusiones de peticiones en curso (R6) ni la herencia del Bloque A sin re-verificar (R31).
