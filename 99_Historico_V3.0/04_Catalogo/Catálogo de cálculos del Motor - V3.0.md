# Catálogo de cálculos del Motor — marco de fichas versionadas, clasificación y lote inicial

**Proyecto Robot Investor · Bloque A · Motor de Cálculo Avanzado para el Analizador de Tendencias de Inversión**

**Documento de especificación del catálogo · Versión V3.0 (catalog_version 3.0) · 01/11/2026 · Coherente con el Documento 0 — Protocolo maestro del Bloque A (Versión óptima V3.0), con el system prompt del Motor (óptima V3.0, secciones 4.6, 5.2, 6 y Anexo B), con el Mapa de conocimientos (V2.0) y con los «Perfiles de clase de activo del Motor» (V1.0) · es-ES**

**Novedades V3.0 (reforma de alcance multiactivo aplicada con la petición maestra del Bloque A):** la ficha estándar incorpora los campos de clases de activo compatibles, prioridad de implantación y estado de madurez (reglas críticas 19 a 21 del Documento 0); el lote inicial se clasifica por utilidad investigadora, clases compatibles, frecuencia de uso, coste, riesgo de error y capacidad de decisión; y se fija la regla de cobertura bajo demanda (1.4): el catálogo define cobertura, no una lista de operaciones obligatorias.

Este documento introduce la **capa de fichas por operación** del catálogo de cálculo del Motor. Conserva íntegro el alcance del listado V1 (21 bloques funcionales, 249 tareas), que sigue definiendo qué puede ejecutar el servicio, y añade la especificación operativa por operación: qué datos exige cada cálculo, qué parámetros admite, qué supuestos declara y qué verificaciones debe pasar. El lote inicial fija como VIGENTES las primeras diecisiete fichas; las operaciones restantes del catálogo continúan operando conforme a su firma hasta que su ficha se publique (reglas de migración, sección 2.4).

---

## 1. Propósito y alcance

### 1.1 Qué es

El catálogo es la colección completa de operaciones que el Motor puede ejecutar. Desde la V2.0 tiene dos capas complementarias:

- **La capa de alcance** (listado V1: 21 bloques, 249 tareas, con su firma por operación): fija qué operaciones existen y su forma de invocación. No cambia en esta publicación.
- **La capa de especificación** (este documento, catalog_version 2.0): fija, para cada operación que disponga de ficha VIGENTE, su método por pasos, sus entradas mínimas con unidades, sus parámetros con rangos, sus salidas, sus supuestos y condiciones de validez, sus limitaciones, sus tolerancias, su semilla, sus servicios técnicos requeridos, su módulo responsable y sus criterios de aclaración y rechazo.

### 1.2 Qué no es

- No amplía ni reduce el alcance del listado V1: ninguna ficha retira ni añade operaciones (system prompt del Motor, 6.4).
- No es un repositorio de código: la implementación vive en el entorno de ejecución (STC-2) y se referencia por method_id y versión.
- No sustituye al Mapa de conocimientos (V1.0): el Mapa dice qué sabe el Motor y por qué; la ficha dice cómo se ejecuta una operación concreta.
- No es un canal de peticiones: las peticiones viajan por el CT-11; la ficha es el contrato metodológico que la petición activa.
- No es una lista de operaciones obligatorias (regla crítica 20 del Documento 0): el catálogo define la cobertura que el Motor debe poder reconocer y tratar; los métodos se activan bajo demanda, cuando la pregunta de investigación los justifica, y ninguna investigación ejecuta todo el catálogo.

### 1.4 Cobertura, activación bajo demanda y clasificación

Desde la V3.0, cada ficha declara además: sus **clases de activo compatibles** (códigos PERF-xx del documento «Perfiles de clase de activo del Motor», V1.0: ACC, FIR, FX, CMD, ETF, DER, REI, CHR, PRV, ALT, MIX o TRANSVERSAL), su **prioridad de implantación** (P0 núcleo transversal; P1 perfiles comprobados; P2 ampliación), y su **estado de madurez** (DOCUMENTADO: especificado y publicado; IMPLEMENTADO: disponible en el entorno de ejecución; VALIDADO: probado con resultados registrados en el Plan de pruebas). Las diecisiete fichas del lote inicial están DOCUMENTADAS y en servicio (IMPLEMENTADAS en producción del Motor); ninguna se declara VALIDADA hasta que la batería mínima de pruebas se ejecute y su evidencia se registre. La clasificación completa del lote está en la sección 4.1.

### 1.3 Utilidad

Para el solicitante: la ficha es la descripción estable de lo que obtendrá, con sus supuestos y sus limitaciones, citable en sus entregables (ficha_id y versión en el artefacto reproducible). Para el Orquestador de Cálculo: la ficha es la especificación que valida la petición (paso 2 del flujo) y la que ejecuta el módulo responsable. Para la auditoría: la ficha es el criterio de contraste de la re-ejecución CT-12 y de la verificación de calidad periódica (13.2 del prompt del Motor).

## 2. Reglas de gobierno del catálogo

### 2.1 Estados de una ficha

| Estado | Significado | Efecto en el servicio |
|---|---|---|
| BORRADOR | Propuesta en preparación, no ejecutable por referencia a ficha | La operación opera conforme a su firma |
| EN_REVISIÓN | Publicada y suspendida por revisión (prueba de regresión fallida, evidencia de uso, reevaluación de supuestos) | La operación se declara EN_REVISIÓN: no se sirve salvo re-ejecución CT-12 que la cite expresamente, con su estado declarado |
| VIGENTE | Publicada y en vigor | La ficha manda sobre la ejecución de su operación |
| DEPRECADA | Sustituida por una versión nueva o retirada del uso | Solo sirve para re-ejecuciones que la citen expresamente, con su estado declarado en la entrega |

### 2.2 Versionado

Las versiones de ficha no sobrescriben: conviven (VIGENTE la última aprobada; las anteriores DEPRECADA) para que las comparaciones y las re-ejecuciones citen la versión exacta. Toda versión declara su historial de cambios. Un cambio de versión de ficha no implica cambio de la versión del catálogo, y al contrario; ambos viajan declarados en cada servicio (schema_version 1.0 del ecosistema sin cambio).

### 2.3 Cambios

La creación, modificación o deprecación de fichas se tramita como propuesta de tipo 3 al operador, con evidencia de uso (13.3 del prompt del Motor), propuesta de redacción, pruebas de regresión y, si procede, análisis de impacto sobre los lados cliente del CT-11. Ningún módulo ni el Orquestador de Cálculo modifican fichas por cuenta propia (regla crítica 14 del Motor).

### 2.4 Migración desde la firma del listado V1

1. Las 249 tareas del listado V1 siguen siendo el alcance del catálogo: su firma por operación (forma, parámetros con unidades, datos requeridos, salidas) sigue siendo válida para invocarlas.
2. Las operaciones con ficha VIGENTE en este documento se ejecutan conforme a su ficha; la ficha manda sobre la firma en lo que ambas declaren.
3. Las operaciones sin ficha publicada se ejecutan conforme a su firma y la respuesta lo declara (op_sin_ficha, con la versión de firma aplicada): el servicio no se niega por falta de ficha.
4. Las fichas nuevas se publican progresivamente por lotes aprobados; ningún lote altera el alcance.
5. Las referencias del solicitante por method_id, nombre de operación o ficha_id son equivalentes para enrutar la petición (Anexo F.1 del prompt del Motor).

## 3. La ficha de operación (estándar)

Toda ficha contiene, en este orden, los campos siguientes:

1. **Identificación**: ficha_id (formato FAM-NOMBRE-NNN); nombre; versión; estado (gobierno, 2.1); familia de cálculo; módulo responsable (MC-XX); nivel del Mapa (área o áreas dominantes).
1-bis. **Alcance y madurez (V3.0)**: clases de activo compatibles (ACC, FIR, FX, CMD, ETF, DER, REI, CHR, PRV, ALT, MIX o TRANSVERSAL); prioridad de implantación (P0/P1/P2); estado de madurez (DOCUMENTADO/IMPLEMENTADO/VALIDADO, regla crítica 19 del Documento 0).
2. **Propósito y pregunta cuantitativa**: qué calcula y qué pregunta responde, en una frase.
3. **Método**: especificación formal por pasos (i, ii, iii…), con las fórmulas o procedimientos esenciales y las opciones declaradas.
4. **Entradas mínimas**: cada entrada con su tipo y unidad; mínimos exigibles (longitud de serie, número de observaciones).
5. **Parámetros**: cada parámetro con nombre, valor por defecto (Anexo A del prompt del Motor), rango admitido y efecto.
6. **Salidas**: forma (VALOR, TABLA, SERIE o DISTRIBUCION), payload y unidades; clase de cifra resultante (DETERMINISTA o ESTADISTICA).
7. **Supuestos y condiciones de validez**: lo que el método exige del mundo para que el resultado signifique lo que dice.
8. **Limitaciones declaradas**: lo que la operación no puede afirmar; advertencias obligatorias de entrega.
9. **Tolerancias numéricas**: tolerancia relativa por defecto del método y criterios de comparación (para re-ejecución CT-12).
10. **Semilla y generador**: null si es determinista; regla de semilla si es estocástico.
11. **Servicios técnicos requeridos**: STC-1 a STC-4, con el papel de cada uno.
12. **Verificación interna exigida**: identidades, casos de control y segunda vía obligatoria o recomendada.
13. **Criterios de aclaración y rechazo**: cuándo se pide aclaración y cuándo se rechaza, con el motivo típico.
14. **Referencias**: áreas del Mapa (V1.0); respaldo bibliográfico esperado en la Documentación para el Motor (búsqueda citando ficha_id); operation del listado V1 de la que especifica la firma.
15. **Historial de cambios**.

## 4. Lote inicial de fichas VIGENTES

Las diecisiete fichas siguientes quedan VIGENTES con esta publicación. El lote cubre el núcleo operativo del dominio: medición de tendencias (4 fichas), relaciones y paridades (4), base estadística y financiera (4), simulación, riesgo, predicción y auditoría (5). Los datos de los ejemplos son ilustrativos.

### 4.1 Clasificación del lote inicial (V3.0)

Clasificación por utilidad investigadora, clases de activo compatibles, frecuencia de uso esperada, coste, riesgo de error y capacidad para cambiar una decisión. Prioridad de implantación: P0 transversal; P1 perfiles. Estado: DOCUMENTADA e IMPLEMENTADA en servicio (VALIDADA: pendiente de la batería mínima).

| Ficha | Utilidad investigadora | Clases compatibles | Frecuencia esperada | Coste | Riesgo de error | Capacidad de decisión | Prioridad |
|---|---|---|---|---|---|---|---|
| FX-TREND-001 | Medir dirección, velocidad y persistencia de una tendencia | FX, TRANSVERSAL | Alta | Bajo | Medio (ventana y espuria) | Alta (candidatura y fase) | P0 |
| FX-BRK-001 | Datar rupturas estructurales | FX, TRANSVERSAL | Media | Medio | Medio (potencia baja) | Alta (invalidación y regímenes) | P0 |
| FX-STL-001 | Separar tendencia, ciclo y estacionalidad | FX, TRANSVERSAL | Media | Medio | Medio | Media | P0 |
| FX-VOL-001 | Medir volatilidad y su brecha implícita-realizada | FX, DER, ACC, CMD, CHR | Alta | Bajo | Bajo-Medio | Alta (riesgo y fases) | P0 |
| FX-REGIME-001 | Identificar regímenes de mercado | FX, ACC, CMD, CHR | Media | Alto | Alto (número de regímenes) | Alta (cambio de régimen) | P0 |
| FX-PPA-001 | Desviación de paridad de poder adquisitivo | FX | Media | Bajo | Medio (horizonte) | Media (valor relativo) | P1 |
| FX-CARRY-001 | Diferencial de tipos y carry | FX, FIR | Alta | Bajo | Bajo | Media | P1 |
| FX-COINT-001 | Cointegración y corrección de errores | FX, ACC, CMD | Baja | Alto | Alto (espuria) | Media | P1 |
| FX-CORR-001 | Correlación dinámica y dependencia de cola | FX, TRANSVERSAL | Alta | Medio | Medio | Alta (riesgo cruzado) | P0 |
| ST-DESC-001 | Estadística descriptiva y momentos | TRANSVERSAL | Muy alta | Bajo | Bajo | Media (base) | P0 |
| ST-INF-001 | Contrastes, intervalos y comparaciones múltiples | TRANSVERSAL | Muy alta | Bajo | Bajo-Medio | Alta (validez) | P0 |
| FIN-CAGR-001 | Crecimiento, anualización, nominal/real | TRANSVERSAL | Muy alta | Bajo | Bajo | Media | P0 |
| BIB-MET-001 | Bibliometría aplicada a fuentes | TRANSVERSAL | Media | Bajo | Bajo | Media (cobertura) | P0 |
| SIM-MC-001 | Simulación Monte Carlo de trayectorias | TRANSVERSAL | Media | Alto | Medio (supuestos) | Alta (escenarios) | P0 |
| RISK-VAR-001 | VaR y Expected Shortfall | TRANSVERSAL (ACC, FIR, FX, CMD, CHR) | Alta | Medio | Medio (colas) | Alta (riesgo) | P0 |
| ML-CAL-001 | Evaluación y calibración de previsiones | TRANSVERSAL | Media | Medio | Medio | Alta (calidad predictiva) | P0 |
| AUD-REX-001 | Procedimiento de re-ejecución independiente (CT-12) | TRANSVERSAL | Baja (auditoría) | Alto | Bajo | Alta (contraste) | P0 |

Regla de lectura: la clasificación orienta la selección de métodos y la construcción del plan proporcional (4.5 y 4.6 del prompt del Motor); no obliga a ejecutar fichas concretas, y la columna «capacidad de decisión» solo mide el peso del cálculo en una decisión de investigación, nunca una recomendación de inversión.

### FX-TREND-001 · Detección y medición de tendencia (Mann-Kendall + Sen)

**Identificación.** ficha_id FX-TREND-001 · versión 1.0 · estado VIGENTE · familia: detección de tendencias · módulo: MC-02 · Mapa: áreas 7 (I–II) y 6.

**Propósito.** Determinar si una serie presenta una tendencia monótona persistente y cuantificar su pendiente con su incertidumbre.

**Método.** (i) Validar frecuencia, calendario y huecos (con STC-1). (ii) Test no paramétrico de Mann-Kendall sobre la serie (o su versión corregida por autocorrelación si la opción lo declara). (iii) Estimador de pendiente de Theil-Sen con su intervalo de confianza. (iv) Aceleración opcional: contraste de pendientes entre las dos mitades de la ventana o sobre la serie diferenciada de la pendiente, declarado como estimación. (v) Salida con dirección, pendiente, significación y aceleración si se pidió.

**Entradas mínimas.** Serie temporal con su frecuencia declarada; mínimo 10 observaciones (recomendadas 20+).

**Parámetros.** ventana (defecto: la serie completa; rango: subventanas declaradas); corregir_autocorrelación (defecto: true); nivel_significancia (defecto: 0,05; rango: 0,01–0,10); calcular_aceleracion (defecto: false).

**Salidas.** TABLA: estadístico Mann-Kendall, p-valor (con corrección si aplica), pendiente de Sen con su IC, dirección, aceleración si aplica. Clase: ESTADISTICA.

**Supuestos y validez.** No exige normalidad; exige que la tendencia sea monótona en la ventana; con autocorrelación fuerte sin corrección, la significación se infla.

**Limitaciones declaradas.** La ventana condiciona el resultado (sensibilidad a la ventana obligatoria en PLAN_STD/EXT); no distingue tendencia de ciclo largo; la aceleración es una estimación con doble incertidumbre.

**Tolerancias.** 1e-6 relativa sobre la pendiente. **Semilla.** null (determinista).

**Servicios técnicos.** STC-1 (validación), STC-2 (aritmética), STC-3 (metadatos), STC-4 (artefacto).

**Verificación interna.** Doble pasada obligatoria; segunda vía obligatoria en críticos (regresión OLS de tendencia como contraste declarado de la pendiente); identidad: la serie reordenada no altera la pendiente de Sen.

**Aclaración y rechazo.** Aclaración si la frecuencia no está declarada o la ventana es ambigua; rechazo con menos de 10 observaciones o serie no numérica.

**Referencias.** Áreas 7 y 6 del Mapa; operation del listado V1 correspondiente; respaldo bibliográfico por el Documentador del Motor citando ficha_id. **Historial.** 1.0: primera publicación (01/11/2026).

### FX-BRK-001 · Detección de rupturas estructurales

**Identificación.** ficha_id FX-BRK-001 · versión 1.0 · estado VIGENTE · familia: cambios estructurales · módulo: MC-02 · Mapa: áreas 10 (II–III) y 7.

**Propósito.** Estimar si y cuándo una serie cambia de media, de tendencia o de varianza, con la incertidumbre de la fecha de ruptura.

**Método.** (i) Validación temporal (STC-1). (ii) Detección secuencial CUSUM (media/pendiente) como primera vía. (iii) Contraste de ruptura múltiple (tipo Bai-Perron declarado) con número máximo de rupturas parametrizado; criterio de selección declarado. (iv) Clasificación del tipo de cambio detectado (nivel, pendiente, varianza). (v) Estimación de las fechas con su intervalo de confianza.

**Entradas mínimas.** Serie temporal con frecuencia declarada; mínimo 30 observaciones para una ruptura, 50 para dos o más.

**Parámetros.** max_rupturas (defecto: 1; rango: 1–5); tipo_cambio (defecto: auto, rango: auto, nivel, pendiente, varianza); nivel_significancia (defecto: 0,05); ventana_trim (defecto: 15 % de extremos excluidos de la búsqueda de fechas).

**Salidas.** TABLA: rupturas estimadas con fechas y IC, tipo de cambio, estadísticos y criterios. Clase: ESTADISTICA.

**Supuestos y validez.** Los contrastes suponen errores aproximadamente homocedásticos dentro de cada segmento (excepto para ruptura de varianza); una revisión estadística de la fuente puede imitar una ruptura (guarda del STC-1, área 36).

**Limitaciones declaradas.** Con series cortas, la fecha de ruptura es imprecisa; una ruptura detectada no identifica su causa económica; los puntos de cambio en cola no se capturan con contrastes de media.

**Tolerancias.** 1e-6 relativa sobre los estadísticos; la fecha de ruptura se compara por periodo (sin tolerancia fraccional). **Semilla.** null.

**Servicios técnicos.** STC-1, STC-2, STC-3, STC-4.

**Verificación interna.** Doble pasada; segunda vía obligatoria en críticos: fecha de ruptura por dos procedimientos (CUSUM frente a ruptura múltiple) con las diferencias declaradas; identidad: sin rupturas impuestas, el modelo nulo reproduce la serie segmentada como una sola.

**Aclaración y rechazo.** Aclaración si el tipo de cambio pedido contradice los datos; rechazo con menos observaciones que el mínimo.

**Referencias.** Áreas 10 y 7 del Mapa. **Historial.** 1.0: primera publicación (01/11/2026).

### FX-STL-001 · Descomposición tendencia-ciclo-estacionalidad

**Identificación.** ficha_id FX-STL-001 · versión 1.0 · estado VIGENTE · familia: descomposición de series · módulo: MC-02 · Mapa: área 6 (I–II).

**Propósito.** Separar una serie en tendencia, componentes estacionales y resto, declarando el tipo de descomposición.

**Método.** (i) Validación de frecuencia y calendario. (ii) Selección del esquema (aditivo o multiplicativo) por regla declarada o por opción de la petición. (iii) Descomposición robusta por suavizado de LOESS (STL) o por medias móviles clásicas según la opción. (iv) Ajuste estacional y serie desestacionalizada. (v) Diagnóstico de la estacionalidad (estabilidad en subventanas).

**Entradas mínimas.** Serie con frecuencia estacional declarada (mínimo 2 ciclos completos; recomendados 3+).

**Parámetros.** esquema (defecto: auto); periodo_estacional (defecto: el declarado por la frecuencia); robusto (defecto: true).

**Salidas.** SERIE: tendencia, estacionalidad, resto y serie ajustada, con unidades de la serie de origen. Clase: ESTADISTICA (la descomposición no es única).

**Supuestos y validez.** La estacionalidad debe ser reconocible; en series cortas la estacionalidad estimada es inestable; un cambio de régimen a mitad de la ventana puede moverse entre componentes.

**Limitaciones declaradas.** La descomposición no es única y depende del esquema y de la robustez elegidos; la serie ajustada no es «la verdad sin estacionalidad» sino una estimación.

**Tolerancias.** 1e-6 relativa; identidad: tendencia + estacionalidad + resto = serie original (dentro de tolerancia). **Semilla.** null.

**Servicios técnicos.** STC-1, STC-2 (convergencia del STL), STC-3, STC-4.

**Verificación interna.** Identidad de suma obligatoria; doble pasada; caso de control de la ficha: serie sintética con estacionalidad conocida se recupera dentro de tolerancia.

**Aclaración y rechazo.** Aclaración si la frecuencia estacional es ambigua; rechazo con menos de 2 ciclos.

**Referencias.** Área 6 del Mapa. **Historial.** 1.0: primera publicación (01/11/2026).

### FX-VOL-001 · Volatilidad realizada e implícita y su brecha

**Identificación.** ficha_id FX-VOL-001 · versión 1.0 · estado VIGENTE · familia: volatilidad · módulo: MC-02 · Mapa: áreas 6 y 33 (II).

**Propósito.** Medir la volatilidad de un par por vía histórica (realizada) y, si el solicitante la aporta, contrastarla con la implícita y cuantificar la brecha.

**Método.** (i) Validación de la serie de precios o rendimientos y de la convención de anualización. (ii) Volatilidad realizada: desviación típica de rendimientos logarítmicos sobre la ventana, anualizada con capitalización compuesta y convención declarada (252 días hábiles por defecto). (iii) Opción de ventana móvil con su tratamiento de bordes. (iv) Si se aporta volatilidad implícita: brecha implícita − realizada con sus dos fuentes y sus horizontes declarados. (v) Clústeres de volatilidad declarados como observación, no como modelo.

**Entradas mínimas.** Serie de precios o rendimientos (mínimo 30 observaciones); si se contrasta con implícita, su serie con fuente, horizonte y convención.

**Parámetros.** ventana (defecto: 20 periodos); convención_anual (defecto: 252; alternativas: 365, declarada); capitalización (defecto: compuesta); ventana_movil (defecto: false).

**Salidas.** VALOR o SERIE: volatilidad anualizada con su convención; brecha si aplica. Clase: ESTADISTICA.

**Supuestos y validez.** La volatilidad realizada es una estimación muestral sensible a la ventana; la implícita incorpora expectativas, no es una previsión de la realizada.

**Limitaciones declaradas.** La brecha no es un pronóstico; las convenciones no se mezclan entre dos cifras entregadas juntas; la volatilidad de baja frecuencia subestima riesgos de cola (contraste con RISK-VAR-001).

**Tolerancias.** 1e-8 relativa. **Semilla.** null.

**Servicios técnicos.** STC-1, STC-2, STC-3, STC-4.

**Verificación interna.** Identidad: la anualización cuadrática es coherente con la de la convención declarada; doble pasada; segunda vía recomendada (ventana alternativa).

**Aclaración y rechazo.** Aclaración si la convención anual no está declarada y el contexto exige coherencia; rechazo con menos de 30 observaciones.

**Referencias.** Áreas 6, 33 del Mapa. **Historial.** 1.0: primera publicación (01/11/2026).

### FX-REGIME-001 · Identificación de regímenes (Markov switching)

**Identificación.** ficha_id FX-REGIME-001 · versión 1.0 · estado VIGENTE · familia: regímenes · módulo: MC-02 · Mapa: área 10 (II–III).

**Propósito.** Estimar la probabilidad de que una serie esté en cada uno de un número declarado de regímenes (media o varianza distintas) y las fechas de transición aproximadas.

**Método.** (i) Validación y estacionariedad por régimen declarada. (ii) Modelo de Markov con cambio de régimen (n estados declarado; varianzas distintas por defecto, medias opcionales). (iii) Estimación por máxima verosimilitud (convergencia controlada por STC-2). (iv) Probabilidades filtradas y suavizadas por periodo. (v) Duración esperada de cada régimen y fechas de transición aproximadas por umbral de probabilidad.

**Entradas mínimas.** Serie con frecuencia declarada; mínimo 100 observaciones para 2 estados (200 recomendadas).

**Parámetros.** n_estados (defecto: 2; rango: 2–3); varianzas_distintas (defecto: true); medias_distintas (defecto: false); umbral_probabilidad (defecto: 0,5; rango: 0,3–0,7).

**Salidas.** SERIE: probabilidades por régimen y periodo; TABLA: parámetros por régimen, probabilidades iniciales, matriz de transición, duraciones esperadas. Clase: ESTADISTICA.

**Supuestos y validez.** El número de regímenes es una decisión declarada (criterio de información si la petición no lo fija); los resultados son sensibles a la semilla y a los valores iniciales si el método los usa.

**Limitaciones declaradas.** La probabilidad de régimen es una estimación; con series cortas, los regímenes identificados pueden ser artefactos; no identifica la causa del régimen.

**Tolerancias.** 1e-6 relativa sobre parámetros; probabilidades en [0,1] exacto. **Semilla.** Entero del plan si el ajuste usa valores iniciales aleatorios; generador declarado.

**Servicios técnicos.** STC-1, STC-2 (convergencia), STC-3, STC-4.

**Verificación interna.** Identidad: las probabilidades de todos los regímenes suman uno por periodo; doble pasada; segunda vía en críticos: re-estimación con semilla distinta y comparación de regímenes (estabilidad declarada).

**Aclaración y rechazo.** Aclaración si n_estados no está justificado; rechazo con menos de 100 observaciones para 2 estados.

**Referencias.** Área 10 del Mapa. **Historial.** 1.0: primera publicación (01/11/2026).

### FX-PPA-001 · Desviación de paridad de poder adquisitivo (relativa)

**Identificación.** ficha_id FX-PPA-001 · versión 1.0 · estado VIGENTE · familia: paridades · módulo: MC-03 · Mapa: áreas 8 y 19 (II).

**Propósito.** Cuantificar la desviación del tipo de cambio efectivo respecto de su senda de paridad relativa de poder adquisitivo.

**Método.** (i) Validación de las dos series de índices de precios y del tipo de cambio, con sus vintages y bases (STC-1; guardas del área 36). (ii) Inflaciones acumuladas de cada economía sobre la ventana declarada con convención declarada. (iii) Senda de paridad: cambio base × razón de inflaciones acumuladas. (iv) Desviación: log-diferencia entre tipo efectivo y senda, en porcentaje. (ii-bis) Opción de media móvil de la desviación para suavizar vintages.

**Entradas mínimas.** Serie de tipo de cambio; dos series de índices de precios con base y periodicidad declaradas y vintages registrados; mínimo 24 meses.

**Parámetros.** ventana (defecto: la completa); base_cambio_inicial (defecto: primer periodo común); suavizado (defecto: null; alternativas: media móvil n).

**Salidas.** SERIE: desviación de paridad en porcentaje; VALOR: desviación puntual final. Clase: ESTADISTICA (por la construcción de índices).

**Supuestos y validez.** La PPA relativa es un ancla de largo plazo; en horizontes cortos la desviación es la norma, no la anomalía; canastas no comparables invalidan la senda.

**Limitaciones declaradas.** No es una previsión ni un valor objetivo; los cambios de base de los índices marcan rupturas de comparabilidad; el efecto Balassa-Samuelson no se corrige aquí y se declara.

**Tolerancias.** 1e-8 relativa. **Semilla.** null.

**Servicios técnicos.** STC-1 (vintages, bases), STC-2, STC-3, STC-4.

**Verificación interna.** Identidad: la senda recomputada desde las dos inflaciones reproduce la serie; doble pasada; caso de control con datos sintéticos de inflación constante (desviación nula).

**Aclaración y rechazo.** Aclaración si faltan bases o vintages; rechazo si las canastas o periodicidades son incompatibles sin transformación declarada.

**Referencias.** Áreas 8, 19 del Mapa. **Historial.** 1.0: primera publicación (01/11/2026).

### FX-CARRY-001 · Diferencial de tipos y carry

**Identificación.** ficha_id FX-CARRY-001 · versión 1.0 · estado VIGENTE · familia: diferenciales · módulo: MC-03 · Mapa: áreas 8, 19, 33 (II).

**Propósito.** Cuantificar el diferencial de tipos entre dos economías y la rentabilidad de carry declarada de un par, con su descomposición.

**Método.** (i) Validación de las dos series de tipos con periodicidad y convención declaradas (nominal/real, base de referencia). (ii) Diferencial de tipos con su base. (iii) Carry: rentabilidad implícita de mantener la posición declarada (larga en la moneda de tipo alto) = diferencial ajustado por el cambio de tipo observado o por el forward si se aporta. (iv) Si se aporta forward: prima/descuento a plazo y paridad cubierta comprobada; el residuo de la paridad descubierta se declara como estimación. (v) Acumulación opcional del carry por periodo.

**Entradas mínimas.** Dos series de tipos de interés con periodicidad declarada; serie de tipo de cambio; forward opcional con su vencimiento.

**Parámetros.** base_tipos (defecto: la declarada por la petición); periodicidad_carry (defecto: mensual); incluir_forward (defecto: false).

**Salidas.** SERIE: diferencial y carry por periodo; TABLA: descomposición (diferencial, variación de tipo, prima/descuento). Clase: DETERMINISTA para la aritmética sobre series dadas; ESTADISTICA para la prima estimada como residuo.

**Supuestos y validez.** El carry observado no es una expectativa ni una recomendación; la paridad descubierta no sostiene la previsión de cambio en la evidencia empírica general y así se declara.

**Limitaciones declaradas.** El carry con cambio observado es aritmética retrospectiva; la prima de riesgo estimada depende del modelo de expectativas, que aquí no se impone.

**Tolerancias.** 1e-8 relativa. **Semilla.** null.

**Servicios técnicos.** STC-1, STC-2, STC-3, STC-4.

**Verificación interna.** Identidad: carry + variación de tipo = rentabilidad total de la posición declarada (dentro de tolerancia); comprobación de paridad cubierta cuando hay forward; doble pasada.

**Aclaración y rechazo.** Aclaración si la base de los tipos es ambigua ( Overnight vs. 3M); rechazo con periodicidades incompatibles sin alineación declarada.

**Referencias.** Áreas 8, 19, 33 del Mapa. **Historial.** 1.0: primera publicación (01/11/2026).

### FX-COINT-001 · Cointegración y corrección de errores

**Identificación.** ficha_id FX-COINT-001 · versión 1.0 · estado VIGENTE · familia: relaciones de equilibrio · módulo: MC-03 · Mapa: área 8 (II).

**Propósito.** Contrastar si dos o más series se mueven juntas en el largo plazo (cointegración) y estimar el vector de cointegración y la velocidad de ajuste.

**Método.** (i) Validación y alineación de frecuencias (STC-1). (ii) Orden de integración de cada serie por contrastes declarados (ADF, con su regla de rezagos). (iii) Contraste de cointegración (Engle-Granger o Johansen según opción). (iv) Vector de cointegración normalizado con su incertidumbre. (v) Modelo de corrección de errores: velocidad de ajuste con su error estándar. (vi) Declaración de la relación de corto plazo si no hay cointegración.

**Entradas mínimas.** Dos o más series alineadas; mínimo 50 observaciones comunes.

**Parámetros.** metodo (defecto: Johansen; alternativas: Engle-Granger); max_rezagos (defecto: por criterio declarado); nivel_significancia (defecto: 0,05).

**Salidas.** TABLA: resultados de los contrastes, vector normalizado, velocidad de ajuste; SERIE: desviación de equilibrio (residuo del vector). Clase: ESTADISTICA.

**Supuestos y validez.** La cointegración exige orden de integración compartido; un cambio estructural puede romperla (contraste de estabilidad del vector obligatorio en PLAN_STD/EXT); el vector estimado no es una teoría económica.

**Limitaciones declaradas.** Cointegración no es causalidad; con muestras cortas los contrastes tienen baja potencia; la velocidad de ajuste depende del ordenamiento en el sistema.

**Tolerancias.** 1e-6 relativa. **Semilla.** null.

**Servicios técnicos.** STC-1, STC-2, STC-3, STC-4.

**Verificación interna.** Identidad: los residuos del vector tienen media nula dentro de tolerancia; doble pasada; segunda vía recomendada (Engle-Granger frente a Johansen).

**Aclaración y rechazo.** Aclaración si las frecuencias difieren sin regla de alineación; rechazo con menos de 50 observaciones.

**Referencias.** Área 8 del Mapa. **Historial.** 1.0: primera publicación (01/11/2026).

### FX-CORR-001 · Correlación dinámica y dependencia de cola entre pares

**Identificación.** ficha_id FX-CORR-001 · versión 1.0 · estado VIGENTE · familia: dependencia · módulo: MC-03 · Mapa: área 18 (II).

**Propósito.** Medir la dependencia entre dos pares: correlación móvil, correlación por régimen y dependencia de cola.

**Método.** (i) Validación y alineación de rendimientos. (ii) Correlación de Pearson sobre ventanas móviles declaradas. (iii) Correlación de Spearman (robusta) de contraste. (iv) Cuantiles de dependencia de cola (coeficientes de cola por cuantiles extremos declarados). (v) Si el plan lo pide y la ficha de cópula está activa, ajuste de cópula con MC-05. (vi) Comparación por régimen si se aportan las probabilidades de FX-REGIME-001.

**Entradas mínimas.** Dos series de rendimientos alineadas; mínimo 60 observaciones comunes.

**Parámetros.** ventana (defecto: 60); cola_cuantil (defecto: 0,05; rango: 0,01–0,10); usar_regimenes (defecto: false).

**Salidas.** SERIE: correlaciones móviles; TABLA: correlación global, por régimen y colas. Clase: ESTADISTICA.

**Supuestos y validez.** Las correlaciones cambian y su inestabilidad es información; una correlación lineal baja no implica independencia de cola.

**Limitaciones declaradas.** La ventana condiciona el resultado; la dependencia de cola con muestras cortas es imprecisa; correlación no es causalidad.

**Tolerancias.** 1e-8 relativa. **Semilla.** null.

**Servicios técnicos.** STC-1, STC-2, STC-3, STC-4.

**Verificación interna.** Identidad: la matriz de correlaciones es simétrica y de diagonal unitaria; doble pasada; caso de control con normal bivariada de correlación conocida.

**Aclaración y rechazo.** Aclaración si las series no alinean; rechazo con menos de 60 observaciones.

**Referencias.** Área 18 del Mapa. **Historial.** 1.0: primera publicación (01/11/2026).

### ST-DESC-001 · Estadística descriptiva y momentos

**Identificación.** ficha_id ST-DESC-001 · versión 1.0 · estado VIGENTE · familia: estadística descriptiva · módulo: MC-01 · Mapa: áreas 4 (I), 33 (II).

**Propósito.** Caracterizar una serie o una muestra: localización, dispersión, forma y cuantiles, con variantes robustas.

**Método.** (i) Validación de la muestra (STC-1). (ii) Estadísticos de localización (media, mediana, recortada). (iii) Dispersión (desviación, IQR, MAD). (iv) Forma (asimetría, curtosis con su convención). (v) Cuantiles declarados. (vi) Marcado de atípicos (3 desviaciones robustas).

**Entradas mínimas.** Serie o muestra numérica; mínimo 5 observaciones.

**Parámetros.** cuantiles (defecto: 0,05/0,25/0,50/0,75/0,95); pesos (defecto: null); por_grupos (defecto: null).

**Salidas.** TABLA de estadísticos con unidades; marcado de atípicos. Clase: DETERMINISTA (aritmética sobre los datos dados).

**Supuestos y validez.** Los momentos superiores son sensibles a atípicos; con n pequeño, curtosis y asimetría son inestables.

**Limitaciones declaradas.** Ningún estadístico descriptivo implica estabilidad futura; la media no es robusta y así se declara junto a la mediana.

**Tolerancias.** 1e-10 relativa. **Semilla.** null.

**Servicios técnicos.** STC-1, STC-2, STC-3, STC-4.

**Verificación interna.** Identidades: media ponderada coherente con sus pesos; cuantiles monótonos; doble pasada.

**Aclaración y rechazo.** Aclaración si las unidades faltan; rechazo con menos de 5 observaciones.

**Referencias.** Áreas 4, 33 del Mapa. **Historial.** 1.0: primera publicación (01/11/2026).

### ST-INF-001 · Contrastes, intervalos y comparaciones múltiples

**Identificación.** ficha_id ST-INF-001 · versión 1.0 · estado VIGENTE · familia: inferencia · módulo: MC-01 · Mapa: área 5 (I–II).

**Propósito.** Ejecutar contrastes de hipótesis y construir intervalos de confianza con su contexto de potencia y comparaciones múltiples.

**Método.** (i) Validación y tipo de contraste declarado (medias, proporciones, varianzas, independencia; paramétrico o no paramétrico). (ii) Comprobación de supuestos del contraste (normalidad declarada con su limitación). (iii) Ejecución del contraste con su estadístico y p-valor. (iv) Tamaño de efecto declarado. (v) Corrección por comparaciones múltiples cuando el plan ejecute varias pruebas sobre la misma conclusión (Bonferroni o Benjamini-Hochberg, método declarado). (vi) Potencia y tamaño muestral mínimos cuando la petición lo pida.

**Entradas mínimas.** Muestras o estadísticos suficientes para el contraste declarado.

**Parámetros.** tipo_contraste (declarado); alternativas (defecto: bilateral); nivel (defecto: 0,05); correccion_multiple (defecto: auto si m>1).

**Salidas.** TABLA: estadístico, p-valor, IC, efecto, corrección aplicada. Clase: ESTADISTICA.

**Supuestos y validez.** Cada contraste declara sus supuestos; la significación no es relevancia y el p-valor no es la probabilidad de que la hipótesis nula sea cierta.

**Limitaciones declaradas.** Potencia insuficiente declarada con series cortas; la corrección múltiple reduce la potencia y se declara.

**Tolerancias.** 1e-8 relativa sobre estadísticos. **Semilla.** null salvo bootstrap/remuestreo (entero del plan).

**Servicios técnicos.** STC-1, STC-2, STC-3, STC-4.

**Verificación interna.** Doble pasada; casos de control de la familia (contrastes con p-valores conocidos); identidad: IC bilateral coherente con el p-valor del mismo nivel.

**Aclaración y rechazo.** Aclaración si el tipo de contraste es ambiguo; rechazo si los datos no sostienen ningún contraste declarado.

**Referencias.** Área 5 del Mapa. **Historial.** 1.0: primera publicación (01/11/2026).

### FIN-CAGR-001 · Crecimiento: CAGR, anualización y nominal/real

**Identificación.** ficha_id FIN-CAGR-001 · versión 1.0 · estado VIGENTE · familia: crecimiento · módulo: MC-01 · Mapa: áreas 2 (I), 19 (II).

**Propósito.** Calcular tasas de crecimiento acumuladas, anualizadas y deflactadas de una serie o magnitud, con el efecto base declarado.

**Método.** (i) Validación de la serie, su periodicidad y su moneda. (ii) CAGR sobre la ventana declarada; anualización con capitalización compuesta. (iii) Conversión nominal/real con el deflactor aportado (vintage declarado). (iv) Descomposición opcional del crecimiento por componentes aportados (precio/volumen). (v) Efecto base: contribución del punto de partida al crecimiento comparado entre ventanas.

**Entradas mínimas.** Serie de la magnitud con su unidad y periodicidad; deflactor si se pide real.

**Parámetros.** ventana (defecto: la completa); frecuencia_objetivo (defecto: anual); deflactar (defecto: false).

**Salidas.** TABLA: crecimiento acumulado, CAGR, tasas por periodo, serie real si aplica. Clase: DETERMINISTA sobre series dadas.

**Supuestos y validez.** El CAGR oculta trayectorias intermedias; bases distintas hacen tasas incomparables (efecto base declarado).

**Limitaciones declaradas.** No extrapola; el deflactor condiciona la cifra real (vintage y base declarados).

**Tolerancias.** 1e-10 relativa. **Semilla.** null.

**Servicios técnicos.** STC-1, STC-2, STC-3, STC-4.

**Verificación interna.** Identidad: la capitalización de las tasas por periodo reproduce el acumulado; doble pasada; caso de control con crecimiento constante conocido.

**Aclaración y rechazo.** Aclaración si la periodicidad o la moneda son ambiguas; rechazo con bases incompatibles sin transformación declarada.

**Referencias.** Áreas 2, 19 del Mapa. **Historial.** 1.0: primera publicación (01/11/2026).

### BIB-MET-001 · Bibliometría aplicada a fuentes

**Identificación.** ficha_id BIB-MET-001 · versión 1.0 · estado VIGENTE · familia: bibliometría · módulo: MC-01 · Mapa: área 28 (II).

**Propósito.** Calcular indicadores bibliométricos y de cobertura sobre las fuentes que el Documentador o el Buscador Avanzado registran: volúmenes, tasas de crecimiento, distribuciones, cobertura y duplicados.

**Método.** (i) Validación del conjunto de fichas recibido (STC-1; esquema del archivo de origen). (ii) Conteos por periodo, categoría y dominio declarados. (iii) Tasas de crecimiento de volúmenes (ficha FIN-CAGR-001 como paso). (iv) Distribuciones y concentración (índice HHI de cobertura por fuente o categoría). (v) Detección de duplicados por hash (con el servicio determinista del bloque cuando el plan lo declare). (vi) Precisión y exhaustividad solo cuando exista conjunto de referencia declarado.

**Entradas mínimas.** Conjunto de fichas con sus campos de fecha, categoría y fuente (estructura declarada).

**Parámetros.** granularidad (defecto: mensual); categorias (defecto: todas); minimo_por_celda (defecto: 1).

**Salidas.** TABLA: volúmenes, tasas, distribuciones, concentración, duplicados. Clase: DETERMINISTA sobre el conjunto dado.

**Supuestos y validez.** Las métricas describen el corpus registrado, no la literatura total; su cobertura es la cobertura de la búsqueda, no del mundo.

**Limitaciones declaradas.** Citas no equivalen a calidad; volumen de publicaciones no demuestra viabilidad comercial; la cobertura depende de las estrategias de búsqueda.

**Tolerancias.** 1e-10 relativa; conteos exactos. **Semilla.** null.

**Servicios técnicos.** STC-1, STC-2, STC-3, STC-4.

**Verificación interna.** Identidad: los totales por categoría suman el total del corpus; doble pasada; detección de duplicados con segunda clave (hash + título normalizado) declarada.

**Aclaración y rechazo.** Aclaración si el esquema de entrada no declara sus campos; rechazo si el conjunto está vacío o corrupto (incidencia registrada).

**Referencias.** Área 28 del Mapa. **Historial.** 1.0: primera publicación (01/11/2026).

### SIM-MC-001 · Simulación Monte Carlo de trayectorias

**Identificación.** ficha_id SIM-MC-001 · versión 1.0 · estado VIGENTE · familia: simulación · módulo: MC-05 · Mapa: área 14 (II).

**Propósito.** Generar la distribución de resultados de una variable bajo hipótesis declaradas, con control de convergencia y reproducibilidad por semilla.

**Método.** (i) Validación de los insumos: dinámica declarada (paseo aleatorio con deriva, con volatilidad, u otra del catálogo), parámetros y sus incertidumbres, correlaciones entre variables. (ii) Semilla fijada por el plan y generador declarado. (iii) Generación de trayectorias con la técnica de reducción de varianza declarada (antitéticas por defecto). (iv) Cálculo de los estadísticos de salida (cuantiles, probabilidades de umbrales, peor caso de la muestra). (v) Diagnóstico de convergencia: error estándar de Monte Carlo de los cuantiles objetivo; estabilidad entre semillas cuando el plan lo pida.

**Entradas mínimas.** Dinámica y parámetros declarados; mínimo 1.000 trayectorias (recomendadas 10.000+).

**Parámetros.** n_trayectorias (defecto: 10.000; rango: 1.000–1.000.000); horizonte (declarado); cuantiles (defecto: 0,05/0,50/0,95); semilla (del plan); reduccion_varianza (defecto: antiteticas).

**Salidas.** DISTRIBUCION: cuantiles, probabilidades de franjas, peor caso; TABLA: diagnóstico de convergencia. Clase: ESTADISTICA con su error de simulación.

**Supuestos y validez.** La distribución es condicional a la dinámica y a los parámetros declarados; una simulación no corrige un modelo mal especificado (MC-05, regla 9).

**Limitaciones declaradas.** Colas simuladas más fiables que las observadas solo si los datos lo sostienen; incertidumbre paramétrica separada de la aleatoria; escenarios comparados con números aleatorios comunes.

**Tolerancias.** 1e-6 relativa en la re-ejecución con la misma semilla. **Semilla.** Entero del plan; generador declarado; obligatoria.

**Servicios técnicos.** STC-1, STC-2 (generador y convergencia), STC-3, STC-4.

**Verificación interna.** Doble ejecución con la misma semilla (identidad de distribución dentro de tolerancia); casos de control con dinámicas de solución conocida; frecuencias empíricas frente a teóricas en los casos de control.

**Aclaración y rechazo.** Aclaración si la dinámica o los parámetros son ambiguos; rechazo sin semilla o sin dinámica declarada.

**Referencias.** Área 14 del Mapa. **Historial.** 1.0: primera publicación (01/11/2026).

### RISK-VAR-001 · VaR y Expected Shortfall

**Identificación.** ficha_id RISK-VAR-001 · versión 1.0 · estado VIGENTE · familia: riesgo · módulo: MC-07 · Mapa: área 25 (II–III).

**Propósito.** Estimar el VaR y el Expected Shortfall de una serie de rendimientos o de una distribución simulada, con método, horizonte y nivel declarados.

**Método.** (i) Validación de la serie o de la distribución de entrada (simulación de MC-05 admitida). (ii) Método declarado: histórico (cuantil empírico), paramétrico (normal o t declarada) o simulado. (iii) VaR al nivel y horizonte declarados, con la regla de escalado temporal declarada (cuadrática solo si el método lo justifica). (iv) ES al mismo nivel. (v) Advertencias obligatorias de entrega: el VaR no describe lo que ocurre más allá del umbral; el ES complementa esa lectura.

**Entradas mínimas.** Serie de rendimientos (mínimo 250 observaciones para el método histórico) o distribución de MC-05 con su semilla.

**Parámetros.** nivel_confianza (defecto: 0,95; rango: 0,90–0,99); horizonte (declarado); metodo (defecto: historico); moneda_y_base (declaradas).

**Salidas.** VALOR: VaR y ES con unidades, horizonte y nivel. Clase: ESTADISTICA.

**Supuestos y validez.** Colas pesadas invalidan el paramétrico normal (contraste declarado); las correlaciones inestables condicionan el agregado; el VaR no es una pérdida máxima.

**Limitaciones declaradas.** Advertencia de cola obligatoria; estabilidad del VaR entre ventanas declarada en PLAN_STD/EXT; el ES depende de la cola estimada.

**Tolerancias.** 1e-6 relativa. **Semilla.** null (histórico/paramétrico); del plan si es simulado.

**Servicios técnicos.** STC-1, STC-2, STC-3, STC-4.

**Verificación interna.** Identidad: ES ≥ VaR del mismo nivel para distribuciones razonables; cuantiles monótonos; doble pasada; segunda vía recomendada (histórico frente a paramétrico con las diferencias declaradas).

**Aclaración y rechazo.** Aclaración si el nivel o el horizonte no están declarados; rechazo con menos de 250 observaciones para el histórico.

**Referencias.** Área 25 del Mapa. **Historial.** 1.0: primera publicación (01/11/2026).

### ML-CAL-001 · Evaluación y calibración de previsiones

**Identificación.** ficha_id ML-CAL-001 · versión 1.0 · estado VIGENTE · familia: evaluación predictiva · módulo: MC-06 · Mapa: áreas 17 y 31 (II).

**Propósito.** Evaluar una previsión o un modelo sobre datos fuera de muestra con validación apropiada al tiempo, métricas declaradas, calibración y comparación con la referencia.

**Método.** (i) Validación de las predicciones y de las realizaciones, con sus horizontes. (ii) Esquema de validación declarado: origen móvil (walk-forward) por defecto; ventana expansiva como alternativa. (iii) Métricas declaradas: error (MAE/RMSE/MAPE con sus limitaciones), para probabilidades (Brier, log-loss, curva de calibración), para distribuciones (CRPS, cobertura empírica por horizonte). (iv) Referencia obligatoria: previsión ingenua (paseo aleatorio sin deriva o la que la ficha de origen declare). (v) Calibración: cobertura empírica de los intervalos por horizonte; detección de previsiones excesivamente confiadas. (vi) Evaluación por régimen cuando se aporten regímenes (FX-REGIME-001).

**Entradas mínimas.** Serie de predicciones y realizaciones alineadas (mínimo 30 puntos por horizonte).

**Parámetros.** esquema_validacion (defecto: walk_forward); horizontes (declarados); metricas (defecto: todas las de la familia).

**Salidas.** TABLA: métricas por horizonte y por esquema; cobertura; comparación con la referencia. Clase: ESTADISTICA.

**Supuestos y validez.** La evaluación retrospectiva no certifica el futuro; la selección reiterada de modelos sobre la prueba exige corrección declarada (31.3 del Mapa).

**Limitaciones declaradas.** Régimen distinto en la muestra de prueba (deriva) declarado; la comparación con la referencia manda sobre la métrica absoluta.

**Tolerancias.** 1e-8 relativa sobre métricas. **Semilla.** null salvo remuestreo (entero del plan).

**Servicios técnicos.** STC-1, STC-2, STC-3, STC-4.

**Verificación interna.** Identidad: las métricas recomputadas desde predicciones y realizaciones reproducen las entregadas; particiones sin solape y con cobertura declarada; doble pasada.

**Aclaración y rechazo.** Aclaración si los horizontes no están declarados; rechazo si las predicciones y realizaciones no alinean.

**Referencias.** Áreas 17, 31 del Mapa. **Historial.** 1.0: primera publicación (01/11/2026).

### AUD-REX-001 · Procedimiento de re-ejecución independiente (CT-12)

**Identificación.** ficha_id AUD-REX-001 · versión 1.0 · estado VIGENTE · familia: auditoría cuantitativa · módulo: MC-08 · Mapa: áreas 31, 41, 42 (I–II).

**Propósito.** Definir el procedimiento interno de toda re-ejecución independiente: reconstrucción aislada del cálculo, comparación dentro de tolerancias y clasificación de discrepancias.

**Método.** (i) Recepción del artefacto original (método y versión, ficha aplicada, entradas efectivas, transformaciones, semilla, política de redondeo) y de la tolerancia o criterio de contraste; aislamiento confirmado. (ii) Reconstrucción con la misma convención, ventana y semilla declaradas (reproducir lo hecho, no corregirlo). (iii) Verificación interna del propio recálculo (doble pasada, identidades de la ficha). (iv) Comparación: diferencia con su signo y su escala relativa; within_tolerance según la tolerancia declarada antes de ejecutar. (v) Clasificación de discrepancias en las categorías cerradas (DATOS_DISTINTOS, CONVENCION_DISTINTA, SEMILLA_DISTINTA, ERROR_IMPLEMENTACION, ERROR_REDONDEO, SIN_CAUSA_CLARA) con su evidencia. (vi) Declaración de la gravedad e impacto: si la discrepancia altera la interpretación, esté o no dentro de tolerancia. (vii) Informe conforme al Anexo E del prompt del Motor con su propio artefacto.

**Entradas mínimas.** Artefacto original completo y tolerancia o criterio de contraste; sin tolerancia no se ejecuta (causa de parada).

**Parámetros.** segunda_via_estabilidad (defecto: false; semilla propia declarada); alcance (el declarado en la petición).

**Salidas.** Informe de contraste (Anexo E): resultado re-ejecutado, comparison, discrepancies, report_artifact. Clase: ESTADISTICA o DETERMINISTA según el cálculo re-ejecutado.

**Supuestos y validez.** La comparación es técnica, no interpretativa; la decisión sobre el resultado original es del circuito de auditoría.

**Limitaciones declaradas.** Si el artefacto original es incompleto (falta semilla, convención o entradas efectivas), la re-ejecución se declara imposible con su motivo; no se reconstruye por inferencia.

**Tolerancias.** Las declaradas en la petición o en la ficha del cálculo original; nunca retrospectivas (regla 9 de MC-08). **Semilla.** La del artefacto original.

**Servicios técnicos.** STC-1 (validación del artefacto), STC-2, STC-3 (versiones exactas), STC-4 (linaje del informe).

**Verificación interna.** Doble pasada del recálculo; casos de control propios del módulo (artefactos de referencia con resultado conocido) en la verificación de calidad periódica.

**Aclaración y rechazo.** Rechazo con motivo si falta el artefacto completo, la tolerancia o el audit_ref; la ampliación del alcance es petición nueva.

**Referencias.** Áreas 31, 41, 42 del Mapa; CT-12 del Documento 0 (4.1, Anexo C). **Historial.** 1.0: primera publicación (01/11/2026).

## 5. Índice del lote inicial por módulo y familia

| Módulo | Fichas VIGENTES | Familias cubiertas |
|---|---|---|
| MC-01 | ST-DESC-001, ST-INF-001, FIN-CAGR-001, BIB-MET-001 | Descriptiva, inferencia, crecimiento, bibliometría |
| MC-02 | FX-TREND-001, FX-BRK-001, FX-STL-001, FX-VOL-001, FX-REGIME-001 | Tendencias, rupturas, descomposición, volatilidad, regímenes |
| MC-03 | FX-PPA-001, FX-CARRY-001, FX-COINT-001, FX-CORR-001 | Paridades, diferenciales, cointegración, dependencia |
| MC-04 | (fichas por lote posterior; opera por firma hasta entonces) | Crecimiento y difusión, prospectiva |
| MC-05 | SIM-MC-001 | Simulación estocástica |
| MC-06 | ML-CAL-001 | Evaluación y calibración de previsiones |
| MC-07 | RISK-VAR-001 | Riesgo y eventos extremos |
| MC-08 | AUD-REX-001 | Auditoría cuantitativa (procedimiento CT-12) |
| Orquestador de Cálculo | (gobierno del servicio; sin fichas de operación) | Validación, plan, integración, registro |

## 6. Pruebas de regresión del catálogo

Cada ficha declara sus casos de control (resultados conocidos, datos sintéticos y de referencia documentados). Tras cada cambio de versión de método o de ficha, el módulo responsable ejecuta los casos de su competencia y el módulo MC-08 verifica una muestra en la revisión de calidad periódica (13.2 del prompt del Motor); el fallo de una prueba devuelve el método y su ficha a EN_REVISIÓN y se notifica al operador. Los casos concretos por ficha se consolidan en la batería de evaluación del servicio (Mapa, sección 17).

## 7. Registro de versiones del documento

| Versión | Fecha | Descripción |
|---|---|---|
| V3.0 | 01/11/2026 | Reforma de alcance multiactivo aplicada con la petición maestra del Bloque A (coordinada con la óptima V3.0 del Documento 0 y la óptima V3.0 del prompt del Motor): ficha estándar ampliada con los campos de clases de activo compatibles (ACC, FIR, FX, CMD, ETF, DER, REI, CHR, PRV, ALT, MIX, TRANSVERSAL), prioridad de implantación (P0/P1/P2) y estado de madurez (DOCUMENTADO/IMPLEMENTADO/VALIDADO, regla crítica 19); nueva regla de cobertura bajo demanda (1.2 y 1.4, regla crítica 20); clasificación completa del lote inicial por utilidad investigadora, clases compatibles, frecuencia de uso, coste, riesgo de error y capacidad de decisión (4.1); las diecisiete fichas VIGENTES conservan su method_id y quedan clasificadas; las fichas nuevas por clase de activo (P1/P2) se publicarán por el cauce de tipos 3 con sus pruebas. catalog_version 3.0. |
| V2.0 | 01/11/2026 | Primera publicación de la capa de fichas del catálogo (catalog_version 2.0), aplicada por la decisión del operador de un Motor por bloque y por la arquitectura modular del Motor (óptima V2.0). Contiene: propósito y alcance (dos capas del catálogo; alcance del listado V1 íntegro); reglas de gobierno (estados BORRADOR/EN_REVISIÓN/VIGENTE/DEPRECADA, versionado sin sobrescritura, vía de tipo 3, migración desde la firma del listado V1 con la regla op_sin_ficha); la ficha estándar de quince campos; y el lote inicial de diecisiete fichas VIGENTES (FX-TREND-001, FX-BRK-001, FX-STL-001, FX-VOL-001, FX-REGIME-001, FX-PPA-001, FX-CARRY-001, FX-COINT-001, FX-CORR-001, ST-DESC-001, ST-INF-001, FIN-CAGR-001, BIB-MET-001, SIM-MC-001, RISK-VAR-001, ML-CAL-001, AUD-REX-001) con su índice por módulo, las pruebas de regresión del catálogo y el registro de versiones. Las operaciones restantes del listado V1 continúan operando conforme a su firma hasta la publicación de su ficha. |
