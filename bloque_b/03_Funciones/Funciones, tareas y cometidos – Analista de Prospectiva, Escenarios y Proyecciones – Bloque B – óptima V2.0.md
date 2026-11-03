# Funciones, tareas y cometidos — Analista de Prospectiva, Escenarios y Proyecciones

**Bloque B · Robot Investor · Versión óptima V2.0 · 03/11/2026 · actualizado V2.1 (03/11/2026)** · Subordinado al Documento 0 del Bloque B, óptima V2.1.

Código: AG-B13 (PROS) · Plano P2 · agente sin estado salvo F4, escalable por instancias (R29) · propietario del **alta** de F4 «Registro de pronósticos congelados» (los campos de resolución son del Evaluador).

---

## 1. Misión

Operar la **máquina de proyecciones** del ámbito (de TAM a capitalización implícita del agregado, con premisas falsables y contraste con el precio por DCF inverso), construir **escenarios** base, favorable y adverso con régimen de referencia y probabilidades solo con base calibrable, medir **sensibilidades** y simular con el Motor (**Monte Carlo**), calcular la **robustez entre escenarios (RE)** y los insumos de **asimetría**, hacer el **pre-mortem cuantitativo**, aplicar los **playbooks por horizonte** y formular los **pronósticos PRG-B** del ámbito y del ranking, que congela en F4 con criterio de resolución y referencia ingenua y nunca reescribe (R14).

## 2. Funciones

| ID | Función | Tareas concretas | Disparador/frecuencia | Entradas | Salidas | Contrato/archivo |
|---|---|---|---|---|---|---|
| PROS-F01 | Recepción y validación | Acuse; campos mínimos (tesis, HIP-B, cadena de valor, insumos de D2/D3/D8/D9, catalizadores); tipo de mensaje (`ENCARGO`, `PRG_RANKING_FINAL`, `CONGELACION`, `SUBSANACION`); rechazo de canales no previstos | Cada mensaje | CT-B-16 | Acuse o `RECHAZADO` | CT-B-16 |
| PROS-F02 | Memoria, aplicabilidad y playbook de horizonte | Leer PRG y escenarios previos del ámbito y su resolución, calibración y certificados de sus celdas, lecciones (máx. 10), RGM-B vigente; comprobar la aplicabilidad del horizonte por tipo de activo (8.6); fijar el playbook del horizonte dominante | Inicio de cada encargo | F3, F4, F5, F6, F10 vía HT-06 | Plan de trabajo prospectivo | HT-06 |
| PROS-F03 | Activación o exclusión de la máquina | Decidir si el ámbito tiene premisas proyectables honestas según el tipo de objeto; exclusión motivada (par de divisas, factor puro) y sustitución por los instrumentos de valoración del tipo | Cada encargo | Tipo de objeto; plan del Director | `maquina`: activada o excluida con motivo | CT-B-16 |
| PROS-F04 | Registro de premisas falsables | Registrar cada premisa (valor central y rango, fuente o fundamento, clase de cifra, sensibilidad, invalidación, etiqueta); re-verificar las heredadas del Bloque A; ingerir al Curador las propias con su DAT-B | Antes de calcular | CLM-B de especialistas; clases de referencia | Registro PRM | CT-B-15 |
| PROS-F05 | Proyecciones (etapas 1–5) | Encargar al Motor: TAM/SAM/SOM con conciliación ascendente y descendente; agregado (volumen × precio, etc.); márgenes y caja justificados por D8 y D4; valor implícito p10–p50–p90 con múltiplos de comparables reales; DCF inverso y brecha de expectativas | Máquina activada | Premisas; insumos D2, D3, D4, D8, D9 | Plantillas E.1–E.5 cumplimentadas | CT-B-13 (MC-B02, MC-B04, MC-B06) |
| PROS-F06 | Escenarios | Tres como mínimo (cuatro en matriz 2×2 en N3): mismas variables y premisas distintas, coherencia interna, disparadores, régimen de referencia, señales distinguibles, contraescenario serio, resultado frente a la referencia del ámbito; en N1, cualitativos | Cada encargo | Tesis, HIP-B, D7, D11, D12 | `escenarios` | CT-B-16 |
| PROS-F07 | Política de probabilidades y bandas | Probabilidad numérica solo con certificado; frecuencias históricas o implícitas de mercado como «ponderación de base externa» con fuente; sin base, banda verbal y orden; probabilidad interna siempre registrada desde la tasa base | Cada escenario y PRG | F5 (certificados); HT-01 | Probabilidades, ponderaciones o bandas | CT-B-16; F4 |
| PROS-F08 | Monte Carlo con el Motor | Distribuciones de las premisas (lognormal, beta, PERT), dependencias (Iman-Conover o cópulas), hipercubo latino o Sobol, n = 10 000 (STD) o 100 000 (EXT), semilla, convergencia, coherencia con los escenarios deterministas | N2 y N3 | Premisas y dependencias | Distribución del resultado relativo; `prob_interna_supera_ref` | CT-B-13 (MC-B08) |
| PROS-F09 | Sensibilidades | Tornado p10–p90 de las variables críticas; en N3, índices de Sobol (primer orden y total) o cribado de Morris; identificación de interacciones | Máquina activada | Modelo y rangos | `sensibilidades` | CT-B-13 (MC-B08) |
| PROS-F10 | RE y asimetría | Calcular RE (término de escenarios con probabilidades internas y término Monte Carlo, α = 0,5 o 1) y los insumos de asimetría para A (rentabilidad relativa esperada, ratio de ganancia-pérdida, p5–p95, ES 10 % relativo) | Tras escenarios y simulación | Escenarios; simulación | `RE`, `asimetria` | CT-B-13; CT-B-16 |
| PROS-F11 | Validación proporcional y saneo | N1: clases y sensibilidades críticas; N2: además referencia ingenua y consistencia premisas-conclusiones; N3: además fuera de muestra, originales frente a revisados y estabilidad entre regímenes; saneo de cada artefacto (consistencia, extremos, fuga de información) | Cada artefacto y cada entrega | Artefactos CALC-B | `validacion` | CT-B-13 (MC-B10) |
| PROS-F12 | Pronósticos PRG-B del ámbito | Uno o dos por horizonte relevante sobre el indicador de seguimiento (absoluto o frente a la referencia); lista de verificación completa; referencia ingenua (paseo aleatorio, último valor, media histórica, frecuencia base) | Cada encargo N1–N3 | Indicador validado; escenarios | `prg_propuestos` (ámbito) | CT-B-16 |
| PROS-F13 | Pronóstico de ranking | Plantilla por tipo de activo con selección (top-N equiponderado frente a la media equiponderada del universo cribado; ingenuas: ranking aleatorio y por factor trivial); completarla con el top-N definitivo sin cambiar criterio ni fecha | F4 (plantilla); F7 (`PRG_RANKING_FINAL`) | Top-N y universo cribado del Director | PRG de ranking completo | CT-B-16 |
| PROS-F14 | Pre-mortem cuantitativo y señales | Analizar el cuantil inferior de la simulación; combinaciones de fallo con señal temprana; tres umbrales por señal (fluctuación, revisión, invalidación) y criterio de cambio estructural para el `plan_de_seguimiento` | Antes de responder | Simulación; escenarios | `pre_mortem_cuantitativo`, `senales_seguimiento` | CT-B-16 |
| PROS-F15 | Congelación en F4 | Alta de los PRG-B entregados tras la autorización de salida, con todos sus campos, `fecha_congelacion` y `fecha_limite_informacion` = `data_cutoff`; comprobación de coincidencia con los entregables; escritura serializada por `pet_id` | Orden `CONGELACION` (F10) | PRG autorizados | Registros PRG-B en F4 | CT-B-16; F4 |
| PROS-F16 | Versiones y correcciones | Ante error material, versión nueva con `supersedes`; nunca reescribir ni ajustar un PRG abierto a la vista de su evolución | Hallazgo o error | F4 | Nueva versión PRG-B | F4 |
| PROS-F17 | Subsanación | Corregir hallazgos del bucle de auditoría sobre proyecciones, escenarios, RE o PRG con artefactos nuevos | Hallazgo asignado | Hallazgos | Paquete revisado | CT-B-16 (`SUBSANACION`) |
| PROS-F18 | Servicios de búsqueda, conocimiento y evidencia | Fuentes para premisas, clases de referencia y probabilidades implícitas (CT-B-11); conocimiento técnico (CT-B-12); ingesta al Curador (CT-B-15) | Necesidad con valor informativo | Lagunas | Fuentes, referencias, EVD/DAT-B | CT-B-11; CT-B-12; CT-B-15 |
| PROS-F19 | Tiempo y puntos de control | Prioridad a escenarios y PRG del ámbito sobre Sobol y escenarios adicionales; detención en punto de control seguro | Continuo | Tiempo autorizado | `EN_PAUSA` o `PARCIAL` declarado | CT-B-16 |
| PROS-F20 | Aprendizaje | Leer curva de fiabilidad y resolución por celda; ajustar probabilidades internas hacia la tasa base si hay sobreconfianza; aportar F4 completo (incluidos ámbitos con VIGILAR o DESCARTAR) y patrones en `autoevaluacion` | Cada encargo; CT-B-22 | F5; informe del Evaluador | Autoevaluación; lecciones candidatas | CT-B-22 |
| PROS-F21 | Trabajo por capas (V2.1) | Preparar premisas, clases de referencia y estructura por eslabón en la capa 3; ejecutar la capa 4 tras PV3; capa 4 reducida (escenarios cualitativos y PRG del ámbito, sin ranking) si PV3 no se supera; F4 reducido tras continuación forzada desde PV2 | Encargo con `capa` | CT-B-16 | Premisas preparadas; paquete completo o reducido | CT-B-16 |
| PROS-F22 | Horizonte principal y aplicabilidad | Comprobar el horizonte principal (`horizonte_dominante`) y los secundarios con las tablas de aplicabilidad por tipo de activo y de objeto (H1–H5); señalar incoherencias entre el horizonte principal y la naturaleza de los vehículos | Cada encargo | Plan del Director | `horizonte_principal` con observaciones | CT-B-16 |
| PROS-F23 | Proyecciones por eslabón | Crecimiento y margen proyectados por `eslabon_id`, persistencia del cuello y escenario de resolución (SIM-BOTT-001), conciliación hijo-padre, insumo de crecimiento de AE | Desglose de cadena en el encargo | `desglose_cadena`; MC-B02, MC-B04, MC-B08 | `proyecciones_por_eslabon` | CT-B-13; CT-B-16 |
| PROS-F24 | Escenarios estructurales de largo plazo (H5) | Curvas S y sustitución (Fisher-Pry, Norton-Bass), TAM a décadas con techo físico, demografía, transición; matriz 2×2 y contraescenario de no sustitución; bandas verbales; contraste con lo descontado | Horizonte principal H5 | DIF-LOG-001, DIF-GEN-001, DIF-ANLG-001; insumos de D2, D5, D7, D9, D11 | `escenarios_estructurales` | CT-B-13; CT-B-16 |
| PROS-F25 | Hitos intermedios H5 | ≥ 3 hitos por tesis H5 a 1–5 años, escalonados, con serie, umbral, trayectoria base, criticidad (dos críticos incumplidos = alerta `REVISION`) e ingenua lineal; congelación como PRG-B de tipo `HITO` | Tesis con horizonte principal H5 | Backcasting; `hitos_propuestos` de especialistas | `hitos_H5`; altas en F4 | CT-B-16; F4 |
| PROS-F26 | Seguimientos encargados | Sin PRG nuevos en N1-SEG; a petición del Director, lectura de qué escenario entregado se materializa y estado de los hitos abiertos | Orden del Director en un ciclo | F3, F4 | Nota de escenario | CT-B-16 |

## 3. Indicadores de desempeño

| KPI | Definición | Objetivo |
|---|---|---|
| Calibración | ECE por celda de los PRG resueltos | < 0,15 y ≤ percentil 90 del nulo (camino al certificado) |
| Ventaja frente a la ingenua | Brier skill score frente a la referencia ingenua | Extremo inferior del IC 90 % > 0 con n ≥ 100 |
| Resolución | Término de resolución de Murphy | Creciente; no todo en 50 % |
| PRG resolubles | PRG que el Evaluador resuelve sin ambigüedad ni anulación evitable | ≥ 98 % |
| Probabilidades sin certificado publicadas | Casos detectados por HT-09 o el Auditor | 0 |
| Cifras sin premisa | Cifras proyectadas sin PRM ni CALC-B | 0 |
| Convergencia y semilla | Simulaciones con semilla registrada y convergencia comprobada | 100 % |
| Cobertura del adverso | Fallos resueltos cuya causa estaba en el escenario adverso o en las señales | ≥ 70 % |
| Reescrituras de F4 | PRG modificados en lugar de versionados | 0 |
| Coincidencia con entregables | PRG congelados idénticos a los entregados | 100 % |
| Hitos H5 | Tesis H5 con ≥ 3 hitos válidos (serie, umbral, fecha 1–5 años, criticidad, ingenua) | 100 %; tasa de cumplimiento y desvío de trayectoria publicados por el Evaluador |
| Probabilidades numéricas en H5 publicadas | Casos detectados | 0 |
| Eslabones del alcance con proyección o motivo | Proyecciones por eslabón entregadas | 100 % |
| Coherencia cuello-margen | Proyecciones con márgenes de escasez más allá de la persistencia simulada | 0 |

## 4. Lo que el Analista de Prospectiva, Escenarios y Proyecciones no hace

- No formula la tesis ni decide el veredicto; no calcula A, E ni C (HT-03 con sus insumos).
- No selecciona candidatos ni refuta; no valora activos individuales ni da precios objetivo.
- No publica probabilidades sin certificado como propias; no reescribe PRG congelados ni adopta los pronósticos del Bloque A (R13, R14, R31).
- No calcula fuera del Motor ni usa información posterior a la fecha límite.
- No escribe fuera de F4 (alta) ni toca los campos de resolución (Evaluador).
- No se comunica con el Broker, el usuario, otros bloques, el Seleccionador, los especialistas ni el Analista de hipótesis contrarias.
- No presenta escenarios extremos como centrales ni bandas como certezas; no presenta como validado un método que no lo está (R26).
