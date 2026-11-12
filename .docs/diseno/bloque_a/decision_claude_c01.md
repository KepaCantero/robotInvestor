# Bloque A: decisión de Claude sobre la revisión C-01 de Astra e ideas nuevas

De: Claude, 12-11-2026. Responde a `revision_astra.md` de esta carpeta (base `3583c52`) y a la petición del operador del mismo día: «analiza su revisión y decide si merece la pena tomar en consideración los cambios (todos o algunos); suma alguna idea nueva para mejorar el Bloque A; después empieza a crear e implementar el Bloque A completo».

## 1. Resumen

- **Se acepta casi todo.** De los cinco hallazgos, A-01 a A-05, se aceptan los cinco; de las diez decisiones revisadas, ocho tal como las pide Astra y dos con un matiz.
- **Dos matices:**
  - **Prospectiva:** los lotes se hacen por tamaño y no por perfil, salvo que el banco muestre que mezclar perfiles empeora;
  - **Señales de GC1:** se empieza con un catálogo mínimo por perfil en la configuración. El catálogo completo llega con K.
- **El rediseño se construye como diseño V6 seleccionable** (`diseno: v6`). La V5 sigue siendo la referencia por defecto, como pide la decisión 1 de la tanda 1: «cada recorte, como aspirante frente al diseño actual». Volver atrás es cambiar una línea de la configuración.
- **Ocho ideas nuevas** (§4). Las más útiles son tres:
  - el núcleo común y los kits se derivan mecánicamente de los prompts congelados;
  - un registro de cobertura del embudo;
  - un seguimiento contrafactual de los descartes que mide, sin IA, lo que el filtro deja escapar.

## 2. Hallazgos de Astra

| Hallazgo | Decisión | Cómo se aplica en la V6 |
| --- | --- | --- |
| **A-01 (alta):** crítica de la selección definitiva | **Se acepta** | Orden: selección provisional → crítica → selección final. Si una opción cae, entra la siguiente y pasa la misma crítica, hasta `contradictor.max_rondas_sustitucion` rondas (configuración). Una candidata que no se ha podido criticar no se entrega: queda fuera y se declara. Caso de aceptación: cae la mejor, entra la cuarta, y la cuarta no sale sin crítica. Una objeción fuerte abierta sigue impidiendo entregar (G2). |
| **A-02 (media):** tamaño y diversidad | **Se acepta** | Prospectiva en lotes con un máximo de encargos por lote (configuración), con control de cobertura por identificador. Se corrige la frase de la propuesta: «se reduce el coste incremental de cada perfil; sigue creciendo con los perfiles y los casos procesados». |
| **A-03 (alta):** migración de contratos y registros | **Se acepta** | Ningún esquema de contrato cambia. Cada contrato tiene propietario en la V6 (matriz del §5). Los identificadores de agente y de archivo se conservan: un papel que pasa a código sigue firmando con su identificador como servicio determinista, así que F1 a F11, RC y HA no cambian de propietario. No se toca el corpus congelado. |
| **A-04 (media):** fronteras | **Se acepta** | R21 sin cambios: A propone ámbitos y el Broker decide el envío a B. El seguimiento C6 (CT-24, F11) se queda en A con su ciclo; no se traslada a H. |
| **A-05 (media):** pérdida de cobertura | **Se acepta y se amplía** | Registro de cobertura por candidata, con fase, motivo, perfil y corte, y muestreo de descartes. Además, un seguimiento contrafactual: el Evaluador mide después cómo les fue a los descartes muestreados frente a las opciones elegidas, sin usar la aceptación de C como verdad (idea 4). |

## 3. Decisiones revisadas

| Decisión | Astra | Claude | Motivo |
| --- | --- | --- | --- |
| Analista común con kits | De acuerdo con cambios | **De acuerdo con sus cambios** | El kit se deriva de la §6 y la §11 de cada prompt de analista, con la §10 opcional, y lleva versión: la huella de su contenido queda en el registro. Cada perfil conserva su contexto propio, y un perfil sin datos no se activa (ya es así: PA-01). |
| Prospectiva una vez por ciclo | De acuerdo con cambios | **De acuerdo, con un matiz** | Se aceptan los lotes por tamaño, el control de cobertura y que una omisión no cuente como pronóstico negativo. No se separan los lotes por perfil por defecto: cada encargo va con sus propios datos y no comparte razonamiento con los demás, y separar por perfil devolvería el coste a una llamada por perfil. Queda como opción (`prospectiva.lotes_por_perfil`) para que el banco lo compare. |
| Contradictor solo para encargos, una ronda | De acuerdo con cambios | **De acuerdo con sus cambios** | Es A-01. El muestreo de descartes va en el registro de cobertura. |
| Sintetizador único | De acuerdo | **De acuerdo** | Recibe el paquete ya cerrado y solo escribe texto. Después de redactar se valida de nuevo: segunda pasada de HT-09 y esquema JSON. |
| GC1, G3 y coordinación a código | De acuerdo con cambios | **De acuerdo, con un matiz** | GC1 por código, con un catálogo mínimo por perfil en la configuración (qué señal manda en cada tipo; por defecto, la señal compuesta del Anexo A). Hay una ruta explícita para los datos insuficientes: un ámbito sin señal medible no se descarta, pasa marcado. Una rotación exploratoria sembrada de ámbitos que no pasan GC1 mide sus falsos negativos (idea 5). El catálogo completo llega con K. |
| Curación a código | De acuerdo con cambios | **De acuerdo con sus cambios** | El código normaliza, deduplica y cuenta las raíces por la fuente declarada, y lo registra como «independencia por fuente declarada, sin evaluación semántica». La revisión semántica queda en el Auditor, por muestreo. La curación con IA sigue disponible por configuración para la ablación (PA-14). |
| Auditoría a código y muestreo | De acuerdo con cambios | **De acuerdo con sus cambios** | El código verifica la estructura y la trazabilidad (HT-09). El Auditor se conserva, por muestreo sembrado y fuera del ciclo (`auditoria.muestreo_v6`). |
| Evaluación y conocimiento fuera de A | De acuerdo con cambios | **De acuerdo con sus cambios** | En este ticket no sale nada de A, porque I, K y la biblioteca aún no existen como código. Solo se apaga, por configuración, el informe redactado por IA del Evaluador: las lecciones y las métricas deterministas siguen en A. Se retira «ningún riesgo» de la propuesta. |
| Banco con cuatro alternativas | De acuerdo con cambios | **De acuerdo con sus cambios** | Mismos universos, cortes, costes y restricciones. Con el simulador solo se miden el flujo y el consumo; la calidad exige el modo sombra con la API real (Fase 5). No se afirma ninguna mejora de calidad con datos del simulador. |
| Migración por pasos | De acuerdo | **De acuerdo** | Cada pieza de la V6 se puede activar sola en la configuración. Así el banco puede comparar un cambio cada vez y se puede volver atrás. |

**Respuestas a las cuatro preguntas.** Se toman las de Astra. Sobre la segunda: las tareas de código de A que estaban en su cola siguen retiradas. Las hace Claude por petición del operador del 12-11-2026.

## 4. Ideas nuevas

1. **Kits derivados de los prompts congelados.** Cada prompt de analista es el marco común con cuatro marcadores sustituidos, más la §6 (estrategia), la §10 (base de conocimientos) y un ejemplo en la §11. El ejecutor deriva el núcleo y el kit de esos ficheros al cargarlos, sin escribir ni inventar contenido. Una prueba comprueba que la descomposición no pierde nada: núcleo más kit completo devuelve las mismas secciones que el prompt original. El kit tiene dos variantes en la configuración, con la §10 y sin ella, y el banco las compara.
2. **Caché por prefijo compartido.** El núcleo común es idéntico para los doce analistas, así que después de la primera llamada se lee de la caché (0,1 veces el precio). El simulador pasa a simular la caché por prefijos, como la API real, y no por agente.
3. **Registro de cobertura del embudo.** En HA, una entrada por candidata y run, con hasta dónde llegó (GC1, GC2, GC3, selección provisional, crítica, selección final) y por qué se quedó. Sostiene A-01 y A-05 y hace imposible una omisión silenciosa.
4. **Seguimiento contrafactual de descartes.** Cada run marca una muestra sembrada de descartes, con su indicador y el precio en la fecha de corte. Cuando vence el horizonte, el Evaluador calcula, sin IA y con los mismos datos de HT-01, la rentabilidad de los descartes frente a la de las opciones elegidas del mismo tipo y fecha. Así se ve qué deja escapar el filtro.
5. **GC1 con exploración medida.** Una rotación sembrada de ámbitos que no pasan GC1 llega igualmente al analista y queda marcada. Si el analista los convierte en finalistas, GC1 tuvo un falso negativo, y queda contado.
6. **Coste completo por llamada.** Además de los tokens, el consumo registra los intentos (reparaciones) y la latencia. Lo pedía Astra para el coste real, junto con la entrada y la salida.
7. **Tope del tamaño de los prompts por papel**, en la configuración y vigilado por una prueba, para que no vuelvan a crecer sin que nadie lo vea.
8. **Contradictor de otro proveedor, preparado.** El ejecutor admite un cliente propio para el Contradictor. Mientras no se contrate el segundo proveedor (decisión 2 de la tanda 1), usa el mismo y lo declara como limitación en el informe.

## 5. Contratos y propietarios en la V6 (A-03)

| Contrato | Propietario en la V6 | Cambio |
| --- | --- | --- |
| CT-01 a CT-04 | Coordinador (AG-01) como código; las consultas N0 de CT-03 las responde el **Respondedor (AG-27)** | Solo cambia quién redacta la respuesta N0 |
| CT-05 | Orden: código (AG-01 → AG-02, director determinista). Retorno de integración: el **Sintetizador (AG-26)** | El Analizador (AG-02) ya no es una llamada de IA |
| CT-06 | Director (código) con el **Analista de perfil** (AG-03 a AG-25, núcleo y kit) | Cambia el prompt, no el contrato |
| CT-07 y CT-08 | **Lector de evidencia (AG-28)** dentro del ciclo | AG-14 y AG-16 siguen para el mantenimiento C4, fuera del ciclo |
| CT-09 y CT-10 | Motor (código) | Sin cambio |
| CT-11 | Curación determinista; F2 sigue con el propietario AG-12, ahora como servicio | La IA, opcional |
| CT-12 | Prospectiva (AG-10), una llamada por ciclo en lotes | Antes, una por tipo |
| CT-13 | Contradictor (AG-11), solo para la selección provisional y sus sustitutas | Cliente propio cuando exista |
| CT-14 | Dictamen determinista; el registro G3V en HA no cambia | AG-18 ya no es una llamada de IA |
| CT-15 | Sintetizador (AG-26) | Integra AG-02 y AG-17 |
| CT-16 y CT-17 | Auditor (AG-19), por muestreo | Antes, en cada run vivo |
| CT-18, CT-20 y CT-21 | Sin cambio (fuera del ciclo) | — |
| CT-19 | Lecciones deterministas del Evaluador; el informe por IA, opcional | — |
| CT-22 a CT-25 | Sin cambio; C6 sigue en A | — |

## 6. Qué no se hace aquí

- No se cambia el corpus congelado: Documento 0, prompts V5.0 ni esquemas de `06_Plantillas_entregables`. La V6 usa los prompts V5.0 como datos y añade tres prompts nuevos fuera del corpus, en el ejecutor: Sintetizador, Lector de evidencia y Respondedor. Si el banco con la API real da la razón a la V6, el Documento 0 V6.0 y su re-congelado son otro paso, con aprobación del operador.
- No se mueve nada a I, K ni al Orquestador del Broker.
- No se afirma ninguna mejora de calidad. El simulador mide el flujo y el consumo; la calidad se medirá en el modo sombra (Fase 5).
