# BLOQUE A — Buscador de Oportunidades de Inversión · Versión óptima V5.1

**Robot Investor · Entrega del 03/11/2026 · es-ES** · Actualización V5.1 de la entrega V5.0 (02/11/2026), que sustituyó a la V4.1. La línea V3.0 se conserva en `99_Historico_V3.0`. Este archivo se llamaba «README - Índice de la entrega y registro de la reforma V5.0».

> **Novedades V5.1 (03/11/2026), cambios del propietario A1–A4.** (A1) **Credenciales** por el contrato nuevo **CT-25**: el Coordinador las pide al Broker a petición de cualquier agente y el Broker las deposita en la **bóveda de HT-01**; ningún agente ve nunca la clave y, si falta, el servicio se degrada y se declara (R8 adaptada). (A2) **Consultas del bloque al Broker** por **CT-23** (dudas de cualquier índole, filtradas por el Analizador; modo bloqueante o no bloqueante; supuesto declarado si no hay respuesta; el Broker aclara en cualquier momento; R26). (A3) Horizonte nuevo **H5 décadas (5–30 años)** con probabilidad siempre cualitativa e **hitos intermedios verificables** (HIT-); H4 pasa a «años (1–5)»; cada opción declara su **horizonte principal** coherente con la **naturaleza de la inversión**, y **HT-09** lo valida. (A4) **Seguimiento encargado de opción** por **CT-24** (alta, modificación, pausa y cancelación en cualquier momento), **ciclo C6**, archivo nuevo **F11 Registro de seguimientos encargados** e **informe de seguimiento de opción** (breve + JSON); R27.

---

## 1. La función del Bloque A

El Bloque A tiene **una sola función: encontrar oportunidades de inversión**. Responde a tres preguntas:

- **Dónde** está la oportunidad: mercado, región, sector, subsector, temática, segmento, factor o estrategia.
- **Por qué** existe.
- **En qué horizonte**: días, semanas, meses, años o décadas (H5, V5.1), con un horizonte principal coherente con la naturaleza de la inversión.

Busca en **cualquiera de los doce tipos de activo** de la clasificación del propietario. **No selecciona activos concretos**: eso lo hace el **Bloque B**, que analiza a fondo el mercado de cada oportunidad y localiza los mejores activos dentro de él.

> Ejemplo: el Bloque A detecta que el textil europeo, sobre todo el técnico, tendrá una tendencia alcista en los próximos meses. Delimita el ámbito y explica la tesis, los catalizadores, los riesgos y cuándo dejaría de ser válida. Propone un indicador de seguimiento y entrega al Broker un **encargo preparado para el Bloque B** con el universo a estudiar, los criterios de selección sugeridos, las métricas clave y las preguntas abiertas. Si el Broker lo decide, el Bloque B estudia el sector y elige los activos.

**Granularidad máxima del Bloque A: el segmento.** Un nombre concreto (empresa, emisión, fondo, contrato o token) solo puede aparecer como ejemplo ilustrativo del ámbito. Proponerlo como opción es un hallazgo Material (regla R21), y el validador HT-09 lo bloquea.

## 2. Los doce tipos de activo y sus Analistas

| N.º | Tipo | Analista | Ámbitos típicos que busca |
|---|---|---|---|
| 1 | Renta variable (RV) | AG-03 | Países, regiones, sectores, subsectores, temáticas, estilos (growth, value, dividendos), tamaños (hasta microcap), preferentes, ADR/GDR, derechos |
| 2 | Renta fija (RF) | AG-04 | Segmentos de deuda: soberana, supranacional, corporativa, IG, HY, convertible, subordinada, titulizada, emergente, verde, ligada a inflación, flotante, pagarés |
| 3 | Divisas (DIV) | AG-05 | Pares y bloques de divisas, carry, valor y momentum cambiario |
| 4 | Materias primas (MP) | AG-06 | Metales preciosos, industriales y para baterías, energía, uranio, agrícolas, tropicales, ganadería, madera, carbono |
| 5 | Índices bursátiles (IDX) | AG-21 **nuevo** | Asignación entre mercados completos, valor relativo entre índices, concentración, rebalanceos y reclasificaciones |
| 6 | Fondos y vehículos (FON) | AG-22 **nuevo** | Descuentos de fondos cerrados, categorías con flujos o estructuras ventajosas, estrategias de gestión según régimen, ELTIF |
| 7 | Derivados (DER) | AG-23 **nuevo** | Volatilidad implícita cara o barata, sesgo, estructura de plazos, carry de futuros, estrategias de opciones |
| 8 | Inmobiliario cotizado (INM) | AG-07 | REIT, SOCIMI y subsectores cotizados (logística, residencial, oficinas, centros de datos…) |
| 9 | Criptoactivos (CRI) | AG-08 | Redes, sectores del ecosistema (DeFi, capa 2, tokenización/RWA), categorías de tokens |
| 10 | Capital privado y alternativos (ALT) | AG-09 | Capital riesgo y privado, deuda privada, infraestructuras y renovables, bosques, coleccionables, regalías, litigios |
| 11 | Monetarios y liquidez (MON) | AG-24 **nuevo** | Dónde, en qué divisa y a qué plazo rinde mejor la liquidez; cuándo fijar plazo |
| 12 | Tipos, crédito y volatilidad (TCV) | AG-25 **nuevo** | Pendiente de curvas, inflación implícita, diferenciales de crédito (CDS) y volatilidad como factor (VIX) |

Unas reglas de asignación basadas en el «motor de rentabilidad» de cada oportunidad (Documento 0, 2.6) evitan que una misma oportunidad aparezca en dos tipos.

El informe semanal propone **hasta 3 opciones por cada uno de los doce tipos**, es decir, hasta 36. Si en un tipo no hay tres buenas, salen menos y se explica por qué.

## 3. Inventario

| Carpeta | Contenido |
|---|---|
| `01_Gobernanza` | **Documento 0 V5.1** (V5.1: CT-23 a CT-25, F11, ciclo C6, H5 y horizonte principal, R26–R27): función única y frontera con el Bloque B (2.1–2.5), doce tipos (2.6), 25 agentes, contratos, ciclos, estrategias y horizontes por tipo (8), puntuaciones y top-3 (9), aprendizaje, referencias, entregables, Anexos A–G |
| `02_System_prompts` | 35 system prompts (25 agentes y 10 módulos del Motor) y la plantilla común de los Analistas de tipo de activo |
| `03_Funciones` | 25 fichas de funciones, tareas y cometidos (actualizadas en V5.1 las afectadas) |
| `04_Motor_conocimiento_y_catalogo` | Catálogo de cálculos V5.0 (81 fichas), Perfiles de tipo de activo V3.0 (12 perfiles y 3 capas) y Mapa de conocimientos V4.0 |
| `05_Archivos_operativos` | Referencias verificadas: F7 Documentación para el Analizador V3.2 (560, 23 áreas), F8 Documentación para el Motor V3.2 (464, 18 áreas), F9 Registro de Fuentes V3.2 (389, 19 áreas) y FM Fondo metodológico V3.1 (164, 7 ámbitos); **todas las áreas con 20 o más referencias verificadas**, incluidas 14 áreas nuevas para índices, fondos y vehículos, derivados, monetario y tipos/crédito/volatilidad. Esquemas de F1–F6, F10, Registro de cálculos e Historial de auditorías |
| `06_Plantillas_entregables` | Plantilla del informe técnico, plantilla HTML del informe visual con doce tipos (y capturas), esquema JSON del paquete y del encargo para el Bloque B (V5.1: naturaleza, horizonte principal, H5 con hitos y supuestos declarados), con un ejemplo válido; **nuevos en V5.1**: plantilla, esquema JSON y ejemplo del informe de seguimiento de opción |
| `07_Objetivos` | 84 objetivos medibles (incluye la frontera con el Bloque B y, en V5.1, la dimensión D11) |
| `08_Arquitectura` | **Imagen de la arquitectura V5.1** (PNG/SVG, con CT-23/24/25, F11 y C6; se conserva la V5.0) y descripción para LLM |
| `09_Pruebas` | Plan de pruebas V3.0 (67 pruebas; PB-58 a PB-67 nuevas en V5.1) |
| `10_Herramientas` | HT-02, HT-03, HT-07 y HT-09 (V5.1: C17 horizonte principal, C18 H5 con hitos, C19 supuestos y perfil SEGUIMIENTO) y especificación de HT-05 (135 pruebas unitarias superadas) |
| `11_Ejecutor` | **Ejecutor en Python para probar y backtestear el bloque** (comando `bloque-a`), con README propio, ejemplo de salida y 58 pruebas superadas con cliente simulado (V1.2: subcomandos `seguimiento`, `consulta-broker` y `credencial`, F11, H5 con hitos) |
| `99_Historico_V3.0` | Paquete V3.0 original |

Los .md son los documentos canónicos; los .docx son copias de consulta.

## 4. Qué cambia en la V5.1 respecto a la V5.0

| V5.0 | V5.1 |
|---|---|
| R8: credenciales solo en la capa de ejecución, sin vía de provisión | **CT-25**: el Coordinador pide la credencial al Broker; el Broker la deposita en la **bóveda de HT-01**; los agentes solo ven alias y estado; si falta, servicio degradado y declarado |
| Sin canal para que el bloque pregunte al Broker | **CT-23** consulta al Broker (tipos `ACLARACION_ALCANCE`, `DATO_O_DOCUMENTO`, `PREFERENCIA_O_CRITERIO`, `CONFIRMACION_SUPUESTO`, `OTRA`; modos bloqueante y no bloqueante; plazos; supuestos declarados en los entregables); R26 |
| H1–H4 (H4: 1–5 años o más) | H1–H5: H4 años (1–5), **H5 décadas (5–30)** con banda cualitativa e hitos HIT-, evaluado por hitos y con degradación automática |
| Horizontes sin jerarquía | `naturaleza_inversion` y **`horizonte_principal`** obligatorios; regla de adecuación validada por HT-09 (C17) |
| `EN_SEGUIMIENTO` como anotación | **CT-24** encargo de seguimiento de opción, **ciclo C6**, **F11**, informe de seguimiento de opción; R27 |
| CT-01 a CT-22; F1–F10; cinco ciclos; R1–R25 | CT-01 a CT-25; F1–F11; seis ciclos; R1–R27 |

Piezas actualizadas (cabecera «actualizado V5.1 (03/11/2026)»): Documento 0 (renombrado a V5.1); system prompts del Coordinador, Analizador, doce Analistas de tipo de activo y su Marco común, Prospectiva, Evaluador, Orquestador, Buscador, Redactor, Auditor, MC-04 y MC-05; fichas de funciones de los mismos agentes; esquemas F3, F4, F5, F10, F1 y RC y **nuevo F11 (esquema V1.0)**; plantillas técnica y visual, esquema y ejemplo JSON del paquete; **nuevos** plantilla, esquema y ejemplo del informe de seguimiento de opción; objetivos; arquitectura (descripción, SVG y PNG V5.1); plan de pruebas; HT-09 y su README; especificación de HT-05; ejecutor V1.2 y sus README. Los nombres de archivo se conservan (salvo este README y los archivos nuevos).

## 4 bis. Qué cambió en la V5.0 respecto a la V4.1

| V4.1 | V5.0 |
|---|---|
| Siete clases; índices, fondos y derivados tratados como «vehículos» | **Doce tipos de activo**, cada uno con su Analista y su estrategia (cinco Analistas nuevos) |
| Las opciones incluían vehículos de implementación, costes y accesibilidad del instrumento | Cada opción describe el **ámbito** (qué incluye y qué excluye), su **indicador de seguimiento**, la **invertibilidad del ámbito** y el **encargo para el Bloque B** |
| Puntuación A con liquidez y costes de implementación | A = asimetría 30 · valoración del ámbito 25 · catalizadores 15 · momento 15 · invertibilidad del universo 15 |
| PS3 Accesibilidad del vehículo | PS3 Invertibilidad del ámbito |
| Paquete para el Bloque B con niveles y vehículos | Encargo completo: ámbito, tesis, horizontes, pronósticos, catalizadores, riesgos, invalidación, indicador, criterios de selección sugeridos, métricas clave y preguntas para el Bloque B |
| Motor con 7 perfiles | 12 perfiles y 21 fichas nuevas (índices, vehículos, derivados, monetario, tipos/crédito/volatilidad) |
| HT-07 con la fórmula original de Fernández-Huerta, que penaliza las frases cortas | Fórmula corregida de Law (2011), como exige el Documento 0; la original se informa aparte |
| Las referencias solo cubrían las áreas de las 7 clases anteriores | **14 áreas de conocimiento nuevas** con 20–27 referencias verificadas cada una: TA-19 a TA-23 (Analizador), TM-15 a TM-18 (Motor) y TF-15 a TF-19 (Registro de Fuentes); 315 referencias nuevas, sin duplicados |
| El ejecutor no encontraba los archivos de referencias renombrados y arrancaba sin ellas | Los localiza por nombre con cualquier versión; una prueba lo vigila |

## 5. Estados de madurez (R22)

| Componente | Documentado | Implementado | Validado |
|---|---|---|---|
| Documento 0, 35 prompts, 25 fichas, esquemas, objetivos | Sí | Sí, en el ejecutor | Tubería validada con cliente simulado (58 pruebas); calidad analítica pendiente de ejecución con la API real |
| Elementos V5.1: CT-23 a CT-25, F11, ciclo C6, bóveda de HT-01, H5 con hitos, horizonte principal | Sí | Sí, en el ejecutor V1.2 (bóveda simulada; revisión C6 determinista, sin llamada al Analista) y en HT-09 | Pruebas automáticas con cliente simulado (13 en el ejecutor, 19 en HT-09); sin validar con el Broker real |
| HT-01 a HT-09 | Sí | Sí, en el ejecutor | Pruebas unitarias e integración simulada superadas |
| Motor | Sí | 14 fichas implementadas; las 67 restantes responden «método no implementado» con alternativa | Pruebas unitarias de las implementadas |
| Referencias F7, F8, F9, FM (1.577) | Sí | Sí | Verificadas por búsqueda web (02/11/2026) o en la carga del 25–26/10/2026; barrido HT-02 en el despliegue |

**Avisos:**

- **Fuga por conocimiento del modelo.** Un backtest de periodos anteriores a la fecha de corte del modelo puede salir optimista: el modelo «recuerda» lo que pasó. Lo fiable es probar periodos posteriores a esa fecha o hacer pruebas hacia delante. El ejecutor lo avisa en `metricas.json`.
- **Sin ventaja demostrada al arrancar.** Hasta acumular al menos 100 pronósticos resueltos por tipo y horizonte, el bloque expresa los pronósticos en bandas verbales («más probable que no») y no en probabilidades.
- **Pendientes menores en referencias.** RF-0035 Cinco Días sin confirmar; en TF-17, RF-0550 (ICE Report Center) y RF-0555 (comités de determinación de CDS) proceden de un directorio y deben confirmarse en el primer barrido; algunas fichas con «Alerta: REPARAR» o metadatos por cotejar, anotados en cada ficha.
- **Referencias de comparación.** Las de 8.4 son propuestas y deben ratificarse en F10.

## 6. Cómo ponerlo a prueba (para el ingeniero)

1. `cd 11_Ejecutor && pip install -e .` y exportar `ANTHROPIC_API_KEY`.
2. Revisar `config/por_defecto.yaml`: identificadores de modelo, precios por millón de tokens (vacíos a propósito) y `fecha_corte_modelo`.
3. Preparar los datos:
   - un CSV de precios por símbolo;
   - un `universo.csv` con los **ámbitos** de cada tipo de activo y el símbolo de su **indicador de seguimiento** (índice o serie que mide el ámbito). Hay un ejemplo en `config/`.
4. Prueba en seco, sin coste: `bloque-a --cliente mock … backtest …`. El ejemplo de salida está en `ejemplos/salida_backtest_simulado`.
5. Prueba real: `bloque-a --cliente anthropic --datos RUTA --universo RUTA --salida RUTA backtest --desde AAAA-MM-DD --hasta AAAA-MM-DD`.
6. Conectar al backtester del ingeniero:
   - `senales.csv`: ámbitos propuestos con su tipo, subtipo y símbolo de seguimiento;
   - `pronosticos.csv`: pronósticos y su resolución;
   - `metricas.json`: acierto y calibración por tipo y horizonte.

Consumo medido en simulación (el modelo real producirá salidas más largas):

| Ciclo | Llamadas | Unidades de cómputo |
|---|---|---|
| Primer ciclo semanal completo (12 tipos) | ≈ 50 | ≈ 44 |
| Ciclos siguientes, la mayoría sin cambios | ≈ 14 | ≈ 7 |

Los detalles están en `11_Ejecutor/README.md`.

## 7. Plan de despliegue

| Fase | Contenido | Condición |
|---|---|---|
| 1 | Publicar V5.1 y dar de alta F5, F6, F10 y F11 con los valores del Anexo A; configurar la bóveda de credenciales de HT-01 | Aprobación del operador |
| 2 | Desplegar HT-01 a HT-09 y lanzar `bloque-a verificar-enlaces` | Fase 1 |
| 3 | Ciclos semanales en modo sombra (sin entrega al Broker) y backtests del ingeniero | Fase 2 |
| 4 | Ejecutar el plan de pruebas (67) y registrar evidencias | Fase 3 |
| 5 | Primera entrega real al Broker y primeros envíos al Bloque B | Pruebas críticas superadas |
| 6 | Implantar por prioridad las fichas del Motor de los tipos nuevos | Continuo |
| 7 | Primera revisión trimestral | 3 meses |

## 8. Registro

| Versión | Fecha | Contenido |
|---|---|---|
| óptima V5.1 | 03/11/2026 | Cambios del propietario A1–A4: credenciales por CT-25 y bóveda de HT-01 (R8 adaptada); consultas del bloque al Broker por CT-23 (R26); horizonte H5 con hitos HIT- y horizonte principal con regla de adecuación validada por HT-09; seguimiento encargado de opción (CT-24, ciclo C6, F11, informe de seguimiento de opción; R27). Propagado a prompts, funciones, archivos operativos, plantillas, objetivos, arquitectura, pruebas, HT-09 y ejecutor (V1.2) |
| óptima V5.0 | 02/11/2026 | Función única y frontera con el Bloque B; doce tipos de activo con cinco Analistas nuevos; ámbito, indicador de seguimiento y encargo para el Bloque B; Motor con 12 perfiles y 81 fichas; 14 áreas de conocimiento nuevas con 315 referencias verificadas; HT-07 corregido; ejecutor adaptado |
| óptima V4.1 | 02/11/2026 | Referencias verificadas (20–44 por área); ejecutor con modo backtest |
| óptima V4.0 | 01/11/2026 | Reforma integral (25 reglas críticas, 20 agentes, aprendizaje, eficiencia, informes) |
| óptima V3.0 | 01/11/2026 | Reforma multiactivo (histórico) |
