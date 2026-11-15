# T-116 · Análisis técnico

## Causa raíz o motivo

El mapa de cobertura del plan de pruebas (`tests/MAPA_PLAN_DE_PRUEBAS.md`, del 3-11-2026) era anterior a casi todo lo construido después y marcaba como automáticas filas cuyas pruebas solo comprueban parte del criterio de aprobación. La Fase 4 pide el resultado real de cada prueba del plan con un comando que lo repita.

## Evidencia

- Mapa antiguo: 34 automáticas. Con la regla estricta, 13 pasan a parciales.
- QA r01 (NO APTO): cuatro filas que el mapa nuevo seguía dando por automáticas (PB-21, PB-23, PB-37 y PB-49) tenían una cláusula determinista sin afirmar; el mutante A01 del revisor, que guarda en F4 una escritura rechazada, dejaba en verde la prueba citada por PB-23.

## Implementación

- Archivos y por qué:
  - `bloque_a/11_Ejecutor/tests/mapa_plan_pruebas.json`: fuente de verdad, legible por máquina, de qué prueba cubre qué.
  - `.docs/scripts/evidencias_plan_a.py`: comprueba el mapa, ejecuta lo citado y regenera el documento.
  - `docs/evidencias_pruebas_bloque_a.md`: generado; no se edita.
  - `tests/test_fase4_mapa.py` (mantiene el mapa y el documento al día) y `tests/test_fase4_huecos.py` (cláusulas del plan que nadie afirmaba).
- Decisiones tomadas:
  - **Regla estricta:** una fila es `AUTOMATICA` solo si sus pruebas afirman todo el criterio, salvo lo que solo existe con tiempo real o con el modelo real. Una cláusula que el ejecutor podría comprobar y nadie afirma la deja en `PARCIAL`.
  - **Las herramientas cuentan** (`bloque_a/10_Herramientas/tests`), aunque no estén en el gate del repositorio: el script las ejecuta desde su carpeta.
  - **Un hueco que revela una diferencia con el plan no se arregla:** se registra (INC-T116-01 e INC-T116-02) y la fila queda parcial.
  - **`--runxfail`:** una prueba citada marcada como fallo esperado cuenta por lo que hace.
- Desviaciones del plan del ticket: ninguna de alcance. La ronda r02 añade pruebas en vez de rebajar las cuatro filas, salvo PB-37, que baja a parcial porque el ejecutor no tiene una operación de corrección de un pronóstico.
- Límites conocidos:
  - el documento refleja el commit sobre el que se generó; `test_h05…` falla si el mapa cambia sin regenerarlo, pero no vuelve a ejecutar las pruebas;
  - las 29 filas parciales siguen teniendo su hueco, dicho en «No comprueba»;
  - con el cliente simulado se valida la tubería, no la calidad analítica (R22);
  - el script lee el plan por sus cabeceras `### PB-NN · …`; otra forma lo detiene con un error.
- Comandos exactos para probarlo, desde la raíz y con el `.venv`:
  - `.venv/bin/python .docs/scripts/evidencias_plan_a.py` (comprueba; 0 si está bien);
  - `.venv/bin/python .docs/scripts/evidencias_plan_a.py --pb PB-23`;
  - `.venv/bin/python .docs/scripts/evidencias_plan_a.py --ejecutar` (unos 3 minutos);
  - `cd bloque_a/11_Ejecutor && python -m pytest -q tests/test_fase4_mapa.py tests/test_fase4_huecos.py`.

## Ronda r02 (QA r01 NO APTO)

| Hallazgo | Corrección | Prueba |
| --- | --- | --- |
| H-01 (alta) cuatro filas automáticas con una cláusula sin afirmar | Pruebas nuevas para PB-21, PB-23 y PB-49 con el caso del plan; PB-37 con la corrección como PRG nuevo, y la fila baja a parcial. Repasadas las ocho automáticas que el revisor no leyó: se añaden pruebas a PB-54 y PB-64 y se cita `test_principal_en_celda_no` en PB-65; PB-32, PB-53, PB-55, PB-56 y PB-63 se mantienen | `test_pb21_…`, `test_pb23_…`, `test_pb37_…`, `test_pb49_…` (2), `test_pb54_…`, `test_pb64_…` |
| H-02 (media) `--pb` daba 0 con una prueba saltada o `xfail` | `--pb` da 1 si alguna citada no se supera; las pruebas se lanzan con `--runxfail` | `test_h02_una_prueba_citada_no_superada_nunca_da_un_cero` |
| H-03 (baja) cabeceras del plan que no se reconocen | `leer_plan` se detiene si una cabecera `PB-` no casa con el patrón; `comprobar` exige título y criterio | `test_h03_…` (5) |
| H-04 (media) documentación | Este análisis; fila de la deuda en EN QA con las cifras; fila de la Fase 4 en `docs/AVANCE.md` | — |
| H-05 (baja) nada avisa si el mapa cambia sin regenerar | La tabla del documento se compara con el mapa | `test_h05_el_documento_publicado_coincide_con_el_mapa` |

Resultado tras la r02: 26 automáticas, 29 parciales, 7 pendientes de la API, 3 sin prueba, 1 con usuarios y 1 documental; 101 pruebas citadas, las 101 superadas.

Fuera del ticket, a la deuda (T-120): un IBAN escrito con espacios no se detecta como dato sensible, y el máximo de 10 lecciones por encargo está escrito en el código y no en la configuración.

## Ronda r03 (QA r02 NO APTO)

La QA r02 dio por corregidos los cinco hallazgos de la r01 y encontró uno más del mismo tipo al repasar las filas que la r01 no había leído.

| Hallazgo | Corrección | Prueba |
| --- | --- | --- |
| H-06 (alta) PB-32 automática sin que ninguna prueba citada afirme que una celda sin habilidad o mal calibrada no se certifica; los mutantes P32b y P32c vivían en toda la suite | Prueba del caso del plan (una celda con habilidad y otra sin ella en el mismo almacén: un solo certificado) y otra que afirma cada condición del certificado por separado. PB-32 queda parcial: falta la re-ejecución CT-10 que el plan pide | `test_pb32_se_certifica_la_celda_con_habilidad_y_no_la_que_no_la_tiene`, `test_pb32_cada_condicion_del_certificado_cuenta_por_separado` (8) |
| De paso (baja): PB-49 automática con un hueco propio del ejecutor | PB-49 pasa a parcial | — |

Resultado tras la r03: 24 automáticas, 31 parciales, 7 pendientes de la API, 3 sin prueba, 1 con usuarios y 1 documental.

## Ronda r04 (QA r03 NO APTO)

La QA r03 abrió H-07 (alta: PB-60, PB-33, PB-56 y PB-06 automáticas con una cláusula sin afirmar; en PB-60 el ejecutor no declaraba la degradación), H-08 (media: el hueco de PB-32 no nombraba Holm ni el método) y H-09 (baja: cifra vieja en la deuda), y propuso un repaso cláusula a cláusula de todas las automáticas. Esta ronda hace ese repaso (preparación, resultado esperado y criterio de cada entrada del plan, salvo lo que es de tiempo real o del modelo real) sobre las 24 automáticas y, por el hueco menor de la deuda, sobre las 31 parciales. Regla aplicada en cada cláusula: si el ejecutor la cumple, una prueba que la afirme; si no la cumple, no se arregla en silencio: la corrección pequeña y segura se hace con su prueba de regresión, y lo demás deja la fila en parcial con su hueco y una línea en INC-T116-03 (`docs/incidencias.md`, `[PROPUESTO]`).

### Cambios en el ejecutor (INC-T116-03)

| Fila | Qué no cumplía | Corrección | Prueba de regresión |
| --- | --- | --- | --- |
| PB-60 y PB-58 | Un servicio con la credencial denegada (o pendiente) quedaba degradado en F10 o en la respuesta a la solicitud, pero ningún entregable lo declaraba | `Credenciales.degradaciones` (servicios denegados o con solicitud abierta y sin proveer); el ciclo los añade a `limitaciones` (paquete, técnico y JSON) y el visual pone una nota con el servicio; al proveerse, deja de declararse | `test_pb60_…` (falla sin la corrección) y `test_pb58_…` |
| PB-22 | R2: «se rechaza, se registra y se escala»; la incidencia CANAL_NO_PREVISTO no llevaba la marca de escalado que sí lleva la de acceso fuera de matriz | `escalado_operador` y «rechazada y registrada» en las dos incidencias de canal | `test_pb22_…` (ampliada) |

Ningún esquema cambia (`limitaciones` ya era una lista de textos; HA no es un formato congelado) y los goldens de contratos siguen coincidiendo (`python tests/goldens_ct.py`).

### Filas que cambian

| PB | Antes | Después | Qué se añade o qué hueco queda |
| --- | --- | --- | --- |
| PB-01 | Automática | Automática | Nivel según GC0 con un ciclo anterior en memoria (N2 con cambio material, N1 sin él), todos los mensajes del catálogo y los de los pasos del plan, y sin G3 APTO no se congela ni se entrega |
| PB-06 | Automática | Automática | Clase ACLARACION y cada referencia es el identificador de una entrada de F1–F6 (mata S06) |
| PB-07 | Automática | Parcial | Clase CONTRASTE y respuesta provisional con nivel y plazo. Hueco: el ejecutor no envía la respuesta final por CT-03 con referencias |
| PB-11 | Parcial | Parcial | Los PRG de la enviada y de la descartada quedan RESUELTO y cuentan en el historial. Hueco: la lección que compara enviadas y descartadas no existe |
| PB-12 | Automática | Automática | Relevancia según la regla del Anexo A (CRI nueva ALTA, RF de seguimiento MEDIA o BAJA), los tres campos de decisión, el encargo para B con los datos de su opción y C01, C10 y C11 en OK |
| PB-14 | Automática | Automática | «No comprueba» dice ya que la explicación en «cambios frente al ciclo anterior» es del modelo |
| PB-16 | Automática | Automática | Menos candidatas investigadas, laguna en F5 y C08 (ninguna cifra sin origen) en OK, añadidos a `test_pb16_…` |
| PB-19 | Parcial | Parcial | El CAR- de AG-02 en el monitor y en HA. Hueco: ni reordenación, ni aviso de plazos, ni propuesta de tipo 3 |
| PB-21 | Automática | Parcial | Hueco: la incidencia no dice el tipo de dato protegido (clave API, IBAN) |
| PB-22 | Automática | Automática | Corrección del escalado y su afirmación |
| PB-31 | Parcial | Automática | Etiqueta en el JSON, el técnico y el visual; ninguna cifra de probabilidad ni confianza «Alta»; `prob_publicada` nula en F4 |
| PB-32 | Parcial | Parcial | Holm (criterio con el alfa corregido y Evaluador que se lo pasa), certificado por celda × método y `certificado_ref`; se citan además la prueba de Holm de `test_t53_…` y `test_certificados_separan_metodos` (P32e, P32f y P32h mueren). Hueco: la re-ejecución CT-10 |
| PB-33 | Automática | Parcial | El caso del plan en un ciclo: revoca, deja la lección CALIBRACION de sobreconfianza y el RUN- posterior no publica probabilidad (mata S33). Hueco: la sección «Novedades» de F6 no existe |
| PB-36 | Parcial | Parcial | Hueco precisado: solo se recalibran los pesos de RK y la P3- queda en F6, no en HA |
| PB-37 | Parcial | Automática | Los dos PRG (original y corrección) entran en las métricas; la decisión de corregir es del modelo |
| PB-38 | Automática | Parcial | Hueco: el técnico no lista la objeción sin resolver ni la alternativa documentada (solo F3) |
| PB-41 | Parcial | Parcial | Se cita el caso de entregables incoherentes que G3 bloquea (`test_entregable_bloqueado_…`) y la prueba nueva de PB-01. Hueco: el caso del factor común y el Auditor |
| PB-43 | Parcial | Automática | La LEC- enlaza las tres QRY- y el tema es común en F5; el tema con palabras distintas y la sección siguiente son del modelo |
| PB-45 | Automática | Automática | «No comprueba» nombra también AS-11 del Auditor |
| PB-49 | Parcial | Automática | Ocho semanas simuladas: cada instantánea de F1–F6, RC y HA contiene la anterior byte a byte; las supresiones de F7–F9 las hace HT-02 con su registro de bajas (prueba de HT-02 citada) |
| PB-50 | Parcial | Parcial | Hueco precisado: el Evaluador solo degrada H5 |
| PB-53 | Automática | Automática | El caso del plan en un C1: el Analista RV propone una empresa y no llega al top-3, al encargo ni a los informes |
| PB-55 | Automática | Automática | Un apartado con su semáforo por tipo en el técnico y el motivo de menos de tres |
| PB-56 | Automática | Automática | El caso del plan en un C1 (RV e IDX con el mismo ámbito; mata S56) |
| PB-58 | Automática | Automática | Corrección (servicio pendiente declarado) y el valor ausente de los contextos que reciben los agentes |
| PB-60 | Automática | Automática | Corrección; ninguna CT-25 nueva salvo cambio de circunstancias (mata S60a) |
| PB-61 | Automática | Parcial | Solo CRI se pausa y el supuesto figura en el técnico y el JSON. Hueco: la respuesta tardía no abre una revisión C2 |
| PB-62 | Parcial | Parcial | Hueco precisado: el ejecutor no crea la LEC- |
| PB-63 | Automática | Automática | Cada hito con fecha, indicador y criterio y el espaciado del Anexo A en el ciclo; se cita `test_h5_espaciado_de_hitos` |
| PB-64 | Automática | Parcial | Los tres estados de H5 y MP × H5 a «Limitado» en F6 y F10. Hueco: los estados no se publican |
| PB-66 | Automática | Automática | Dos ciclos C6, SEG- en F11, fecha del siguiente ciclo tras la pausa y la reanudación, y ninguno tras cancelar |

Se mantienen sin cambio, repasadas: PB-23, PB-54, PB-59 y PB-65 (cada cláusula determinista afirmada).

### Parciales repasadas sin prueba nueva

Quedan con el hueco que ya declaraban, porque la cláusula exige el modelo real, tiempo real, usuarios o un componente fuera del ejecutor (PB-09, el planificador HT-05; PB-20, PB-24 y PB-25, HT-02 y F9; PB-10 y PB-17, INC-T116-01 y 02; PB-29, el Auditor), o porque probarla con el simulador exige preparar un caso que esta ronda no ha montado: PB-02 y PB-03 (los casos sembrados de selección), PB-08 (la ráfaga de 65 peticiones), PB-13 (la rotación exploratoria, que se fija por número de celdas), PB-18 (la cola del Curador), PB-30 (la cifra sin CALC- de extremo a extremo), PB-34, PB-35, PB-39, PB-44, PB-47, PB-52 y PB-67. Quedan para la deuda (T-116) como hueco menor.

### Mutantes

- De la QA r03 (`revisores/r03_01_pb32_y_muestra.py`, sobre una copia con el mapa nuevo): P32a a P32h, S06, S14, S33, S56, S60a y S60b, **todos muertos** (antes vivían P32e, P32f, P32h, S06, S33, S56 y S60a). A mano, con una credencial denegada, los tres entregables declaran la degradación.
- Propios (`r04_mutantes_implementador.py`, en este ticket): veinte mutantes, uno por cláusula nueva (M01 a M20: nivel según GC0, congelación sin G3, referencia inventada, plazo, relevancia, escalado, empresa concreta, semáforo del técnico, servicio pendiente, nota del visual, servicio ya provisto, supuestos del técnico, H5 invalidado, cancelación, estado en F3 tras la decisión, confianza «Alta», corrección en métricas, lección enlazada, laguna en F5 y duplicados en C1), contra las pruebas que el mapa cita para su fila: **veinte de veinte muertos**.

Resultado tras la r04: 22 automáticas, 33 parciales, 7 pendientes de la API, 3 sin prueba, 1 con usuarios y 1 documental.
