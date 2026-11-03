# BLOQUE A FOREX — Buscador de Oportunidades de Inversión en Divisas · Versión óptima V1.1

**Robot Investor · Entrega del 02/11/2026 · actualizada V1.1 el 03/11/2026 · es-ES** · Bloque independiente, construido sobre el Bloque A general V5.0 y alineado con su V5.1 (cambios del propietario A1–A4); el Bloque A general **no se modifica** desde aquí y sigue vigente. Registro de la actualización en la sección 9.

---

## 1. Qué es

El Bloque A Forex es la variante del Bloque A **especializada exclusivamente en divisas**. Tiene una sola función: **encontrar oportunidades de inversión en el mercado de divisas**. Responde a tres preguntas:

- **Dónde**: en qué par, cruce, cesta, bloque, estrategia cambiaria o cambio de régimen.
- **Por qué**: divergencia de política monetaria, carry, desviación del equilibrio, flujos y posicionamiento, términos de intercambio, intervención…
- **Cuándo**: en qué horizonte; días, semanas, meses o años, y décadas solo para tesis estructurales (H5 «limitado», V1.1). Cada opción declara su horizonte principal según la naturaleza de la inversión.

**No elige el instrumento.** Contado, forward, futuro, opción, ETF o CFD, junto con el coste, el apalancamiento, el tamaño y la cobertura, son tarea del **Bloque B**. A cada opción se le adjunta un **encargo preparado para el Bloque B**. Ese encargo recoge:
- el par o la composición;
- la dirección y la divisa de financiación;
- la tesis, los catalizadores, los riesgos y la invalidación;
- el carry esperado;
- las consideraciones de implementación;
- las métricas clave;
- las preguntas abiertas para el Bloque B.

> **Ejemplo.** El bloque detecta que el Banco de Japón endurecerá su política monetaria antes de lo que descuenta el mercado mientras la Fed recorta. Propone «USD/JPY bajista (el yen sube frente al dólar), 3–6 meses» con su tesis, sus catalizadores y sus condiciones de invalidación. El Bloque B decide después con qué instrumento capturarlo.

## 2. Los seis segmentos y sus Analistas

| Segmento | Analista | Universo |
|---|---|---|
| G10N · G10 núcleo | AG-03 | USD, EUR, JPY, GBP, CHF (y DKK como régimen) |
| G10M · G10 de materias primas y escandinavas | AG-04 | AUD, NZD, CAD, NOK, SEK (e ISK) |
| EMAS · Emergentes de Asia | AG-05 | CNY/CNH, INR, KRW, TWD, IDR, SGD, THB, MYR, PHP, VND, HKD |
| EMLA · Emergentes de Latinoamérica | AG-06 | BRL, MXN, CLP, COP, PEN; ARS y otras como regímenes |
| EMEA · Emergentes de Europa, Oriente Medio y África | AG-07 | PLN, HUF, CZK, RON, TRY, ZAR, ILS, EGP, NGN…; divisas del Golfo |
| ESTR · Estrategias y cestas | AG-08 | Carry, valor, momentum, dólar amplio, refugio, volatilidad, cestas temáticas |

Dos **Analistas transversales** preparan una vez por ciclo los determinantes comunes a todas las divisas y los reparten a los seis segmentos (contrato CT-06T):
- **AG-09 Bancos Centrales y Macro Cambiaria**: sendas de tipos descontadas, diferenciales, calendario e intervención.
- **AG-21 Posicionamiento, Flujos y Volatilidad Cambiaria**: posicionamiento CFTC, flujos, volatilidad implícita, *risk reversals* y base cruzada.

El informe semanal propone **hasta 3 opciones por segmento** (hasta 18). Si un segmento no tiene tres opciones buenas, se entregan menos y se explica por qué.

## 3. Lo específico de las divisas

- **Tipos de opción**: PAR, CRUCE, CESTA, BLOQUE, ESTRATEGIA, VOLATILIDAD y REGIMEN.
- **Notación y dirección**: notación BASE/COTIZADA, con la dirección referida a la divisa base. Las cestas y estrategias declaran su composición; las opciones de volatilidad, su vista de volatilidad.
- **Puntuación de atractivo A**: asimetría 30 · valoración y desviación del equilibrio 20 · **carry 15** · catalizadores 15 · momento y **posicionamiento** 10 · **convertibilidad** y profundidad 10.
- **Puerta PS3 de convertibilidad**: descarta divisas con controles de capitales a las que un minorista europeo no tiene acceso. Un NDF extrabursátil no basta.
- **Referencia obligatoria: el paseo aleatorio** (Meese-Rogoff), además del forward como predictor. Solo se dan probabilidades numéricas con un certificado del Evaluador.
- **Coherencia entre segmentos**:
  - exposición agregada por divisa;
  - contradicciones, que solo cuentan si la misma divisa es la pata activa de la tesis;
  - apuestas independientes.

## 4. Inventario

| Carpeta | Contenido |
|---|---|
| `01_Gobernanza` | **Documento 0 del Bloque A Forex V1.1**: especificación única del bloque (reglas R1–R27, segmentos, 21 agentes, contratos, ciclos, estrategias por segmento, puntuaciones, puertas, parámetros, esquemas, glosario, taxonomías y relación con el Bloque A general) |
| `02_System_prompts` | 32 archivos: 21 agentes, 10 módulos del Motor (MC-01 a MC-10) y el Marco común de los Analistas de segmento (actualizados V1.1 los afectados; sección 9) |
| `03_Funciones` | 21 fichas de funciones, tareas y cometidos (16 con funciones V1.1) |
| `04_Motor_conocimiento_y_catalogo` | Catálogo de cálculos Forex (60 fichas, 30 de ellas cambiarias), Perfiles cambiarios (PERF-FX-G10, PERF-FX-EM, PERF-FX-FACT) y Mapa de conocimientos |
| `05_Archivos_operativos` | **Referencias verificadas específicas de divisas** (detalle en la sección 5); Fondo metodológico compartido; esquemas Forex de F1–F6, F10, **F11 (nuevo V1.1)**, RC y HA |
| `06_Plantillas_entregables` | Plantilla del informe técnico y del informe visual HTML para el usuario (con capturas de escritorio y móvil), esquema JSON del paquete de oportunidades y ejemplo que lo valida (con naturaleza, horizonte principal y una opción H5); **plantilla y ejemplo JSON del informe de seguimiento de opción (V1.1)** |
| `07_Objetivos` | 106 objetivos medibles (D12 nueva en V1.1) |
| `08_Arquitectura` | **Imagen de la arquitectura** (PNG/SVG) con todos los agentes, archivos, contratos, herramientas y entregables, y su descripción detallada para LLM |
| `09_Pruebas` | Plan de pruebas Forex (86 pruebas: 77 de V1.0 y PB-78 a PB-86 de V1.1; comprobaciones G3-FX-01 a 11 y G3-CON-24 a 26) |
| `10_Herramientas` | HT-02, HT-03, HT-07 y HT-09 adaptadas; HT-09 FX-1.1 con C17–C19 y `validar_seguimiento` (147 pruebas superadas) |
| `11_Ejecutor` | **Ejecutor en Python** (`bloque_a_forex`, comando `bloque-a-forex`) para probar y backtestear el bloque. Incluye universo de pares, datos sintéticos, proveedor sin *look-ahead*, referencias paseo aleatorio y forward, ejemplo de backtest simulado y README para el ingeniero; V1.1: subcomandos `seguimiento`, `consulta-broker` y `credencial`, F11, H5 con hitos y bóveda simulada (68 pruebas superadas) |

Los .md son los documentos canónicos; los .docx son copias de consulta.

## 5. Referencias verificadas (02/11/2026)

| Archivo | Áreas | Fichas | Mínimo por área |
|---|---|---|---|
| F7 Documentación para el Analizador de Oportunidades en Divisas (TX-01…TX-14) | 14 | 358 | 22 (máximo 39) |
| F8 Documentación para el Motor de Cálculo Avanzado (Forex) (TMX-01…TMX-09) | 9 | 244 | 23 (máximo 39) |
| F9 Registro de Fuentes para el Analizador de Oportunidades en Divisas (TFX-01…TFX-10) | 10 | 214 | 20 (máximo 26) |

- **Verificación**: todas las fichas están verificadas por búsqueda web. Su estado de enlace es OK, MURO_PAGO, VERIFICADO_BUSQUEDA o REDIRIGIDO.
- **Orden**: dentro de cada área, las fichas aparecen por calidad Q descendente.
- **Origen**: las fichas reutilizadas del Bloque A general conservan su ID. Las nuevas llevan los prefijos FXA-, FXM- y FXF-.
- **Pendiente de revisar en el primer barrido HT-02**:
  - **Fichas sin página leída**: una parte se confirmó solo a través de páginas índice (VERIFICADO_BUSQUEDA). Les faltan datos que no se pudieron leer, como el DOI o el nombre completo de algún autor.
  - **TFX-02**: las fichas de bancos centrales emergentes se confirmaron con el directorio del BPI y sus webs no se abrieron una a una.

## 6. Cómo ponerlo a prueba

Las instrucciones están en `11_Ejecutor/README.md`: instalación, modo simulado, modo con la API, *replay* y backtesting con datos propios.
- Con el **cliente simulado**, el ejecutor solo comprueba que la tubería funciona; **no mide capacidad predictiva**.
- La **validación analítica** exige ejecuciones con la API real y un backtest que compare los resultados con el **paseo aleatorio** y el **forward**. Esas comparaciones las exporta el propio backtest.
- Para la **anonimización** se han usado datos sintéticos. En divisas protege poco: los códigos ISO y los tipos de interés delatan el par.

## 7. Coexistencia con el Bloque A general

Los dos bloques son independientes y no se comunican entre sí.
- **Enrutamiento**: el Broker envía las peticiones de divisas al Bloque A Forex.
- **Recomendación**: dejar el Analista de Divisas del Bloque A general (AG-05) en cribado ligero (N1) para no duplicar trabajo.
- **Identificadores**: los de este bloque llevan el infijo `FX` (RUN-FX-, OPP-FX-, PRG-FX-…), para que no choquen con los del Bloque A general en el Broker.
- **Fondo metodológico**: es el mismo para todo el ecosistema.

## 8. Decisiones pendientes del operador

1. Ratificar las cestas de referencia de EMAS, EMLA y EMEA, que se publican en F10.
2. Ratificar la escala de riesgo cambiaria de RISK-DD-001 v2.0: volatilidad anual del 5/9/14/20 % más ajustes, con un mínimo de 4 para regímenes frágiles.
3. Ratificar la probabilidad de referencia del paseo aleatorio (RI-PA).
4. Aprobar el presupuesto semanal de referencia (≤ 170 UC).
5. Decidir si el Bloque A general reduce a N1 su Analista de Divisas.
6. (V1.1) Fijar las bandas `PENDIENTE_OPERADOR` de los nuevos parámetros calibrables de F10 (P-42, P-43, P-46, P-47, P-49).
7. (V1.1) Sustituir la bóveda simulada de HT-01 por un gestor de secretos real antes del uso con credenciales de pago.

## 9. Registro de la actualización V1.1 (03/11/2026)

Cambios del propietario A1–A4, alineados con el Bloque A general V5.1. Ningún archivo se renombra salvo el Documento 0 (V1.1) y este README; las piezas tocadas llevan en su cabecera «actualizado V1.1 (03/11/2026)».

| Cambio | Qué se ha hecho | Dónde |
|---|---|---|
| **A1 · Credenciales (CT-25, R8)** | El Coordinador solicita al Broker, a petición de cualquier agente (vía Analizador o directamente el Buscador), la credencial de un servicio; el Broker la deposita en la **bóveda de HT-01** y responde solo con estado y alias; la clave nunca entra en mensajes, archivos ni contextos; mientras falta, el servicio se degrada y se declara; una denegada se anota en F10 | Documento 0 (R8, 4.4, 6.1, 7.10, 17); prompts del Coordinador, Analizador, Marco común y seis Analistas, AG-09, AG-21 y Buscador; F5 (CRD-FX-), F10 (P-44, limitaciones); HT-09 C13; ejecutor `comunicacion.Credenciales` y `herramientas/boveda.py`; `credencial` en la CLI |
| **A2 · Consultas al Broker (CT-23, R26)** | Cualquier agente plantea dudas; el Analizador las filtra y agrupa; el Coordinador las envía (máx. 3 por RUN). Modo BLOQUEANTE (pausa la parte afectada en su punto de control) o NO_BLOQUEANTE (supuesto declarado); al vencer, se sigue con el supuesto y consta en los entregables; el Broker aporta información en cualquier momento; las recurrentes enseñan (CT-22) | Documento 0 (R26, 6.1, 6.2.9, 7.9); prompts del Coordinador, Analizador, Marco común y seis Analistas, AG-09, AG-21, Prospectiva, Buscador, Evaluador, Redactor; F5 (CNS-FX-), F10 (P-41 a P-43); HT-09 C19; ejecutor `comunicacion.Consultas`; `consulta-broker` en la CLI |
| **A3 · Horizontes (H5 y horizonte principal)** | H5 décadas «limitado» en los seis segmentos (equilibrio a muy largo plazo, regímenes, sistema monetario internacional), siempre cualitativo y con ≥ 3 hitos HIT-FX-, evaluado por hitos; regla de adecuación: cada opción declara `naturaleza_inversion` y `horizonte_principal` (TACTICA H1–H2 · CICLICA y PRIMA_RIESGO H2–H4 · VALORACION H3–H4 · ESTRUCTURAL H4–H5), validados por HT-09 | Documento 0 (R13, 8.3, Anexo A); prompts del Analizador, Marco común y seis Analistas, Prospectiva, Evaluador, Orquestador, Redactor, Auditor; F4, F10 (P-48 a P-50); esquema JSON y ejemplos; HT-09 C17 y C18; ejecutor `horizontes.py`, `sintesis.py`, `evaluador.resolver_hitos` |
| **A4 · Seguimiento encargado de opción (CT-24, C6, F11, R27)** | El Broker encarga, modifica, pausa, reanuda o cancela (con efecto inmediato) el seguimiento periódico de una OPP-FX-; cada ciclo C6 es una revisión ligera con HT-03 que produce el **informe de seguimiento de opción** (breve + JSON) con semáforo y recomendación; F11 nuevo (propietario: Coordinador); lo planifica HT-05 | Documento 0 (R27, 5.1, 7.1, 7.11, 14.4); prompts del Coordinador, Analizador, Marco común y seis Analistas, Redactor, Evaluador, Orquestador, Auditor; F11 (nuevo), F5; plantilla y ejemplo del informe; HT-09 `validar_seguimiento`; ejecutor `seguimiento.py`, HT-05; `seguimiento` en la CLI |
| Arquitectura | Diagrama redibujado con CT-23/24/25 y F11 (`diagrama_fx11.py`, PNG renderizado con Playwright; mismos nombres de archivo) y descripción para LLM actualizada | `08_Arquitectura` |
| Objetivos y pruebas | D12 (OBJ-97 a OBJ-106); PB-78 a PB-86, RP-17 a RP-19, G3-CON-24 a 26 | `07_Objetivos`, `09_Pruebas` |
| Pruebas automáticas | 10_Herramientas: 147 superadas (+18). 11_Ejecutor: 68 superadas (+14 en `tests/test_v11.py`) | `10_Herramientas/tests`, `11_Ejecutor/tests` |
