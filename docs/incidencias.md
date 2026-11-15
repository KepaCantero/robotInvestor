# Incidencias del spec

Decisiones y ambigüedades detectadas durante la implementación. Cada entrada: qué dice
el spec (o dónde calla), qué decisión se tomó, y por qué. Nada se decide en silencio.

---

**INC-001 · 2026-11-03 · Versión del ejecutor sin subir en pyproject.** El README V5.1
(§3 y §5) declara "ejecutor V1.2" (subcomandos seguimiento/consulta-broker/credencial,
F11, H5), pero `11_Ejecutor/pyproject.toml` mantiene `version = "1.1.0"`. El código
entregado ES el V1.2 (los subcomandos existen y los 58 tests pasan); solo la cadena de
versión quedó sin bump. Decisión: se deja tal cual pendiente de confirmar con el
propietario de la entrega; no se corrige en silencio porque una versión en el paquete
instalado (`bloque-a --version` / metadata) diría 1.1.0.

**INC-002 · 2026-11-03 · Igual patrón en bloque_a_forex.** El README V1.1 del Bloque A
Forex declara "V1.1" (subcomandos seguimiento/consulta-broker/credencial incluidos, 68
tests) pero su `pyproject.toml` declara `version = "1.0.0"`. Mismo tratamiento que
INC-001: documentado, sin corregir en silencio.

**INC-003 · 2026-11-03 · python-docx es dependencia implícita de bloque_b.**
`bloque_b/redaccion.py::md_a_docx` genera los .docx con pandoc o, en su defecto,
python-docx — pero ni `dependencies` ni `optional-dependencies` del pyproject declaran
`python-docx`. Sin él (ni pandoc), el mapa de eslabones .docx se omite con una
limitación declarada (degradación elegante) y 3 tests fallan porque exigen el .docx.
Solución de entorno aplicada: `pip install python-docx` en el venv del proyecto
(documentado en CLAUDE.md). Corregir el pyproject upstream queda pendiente de confirmar
con el propietario de la entrega.

**INC-T53-01 · 2026-11-09 · Diversidad con tres opciones del mismo clúster (Bloque A, D0 9.6.3).** El D0 dice
«no más de dos opciones del mismo clúster» y, a continuación, que la tercera cede su puesto a otra de otro clúster
«si su RK está a ≤ 10 puntos». No dice qué pasa si no hay ninguna a ≤ 10 puntos. HT-03 publica las tres con la
concentración declarada (`excepcion: True`). Decisión: se deja como está y se pregunta al operador (revisión T-53),
porque cambiarlo toca la herramienta de referencia del corpus y es una regla de selección.

**INC-T53-02 · 2026-11-09 · Antigüedad de los datos en H1 (Bloque A, Anexo A, PS2).** El Anexo A dice «H1: 1 día» y
el código toleraba 3 días naturales. Decisión `[PROPUESTO]` (hasta T-57): H1 se cuenta en sesiones hábiles (el dato del viernes vale el lunes)
y el resto de horizontes sigue en días naturales, para no relajar H2–H5. Los límites pasan a
`ps2_antiguedad_maxima_dias` en la configuración. Ampliación (QA de T-53, H-04): las sesiones descuentan los cierres habituales de mercado (`ps2_festivos`, [PROPUESTO]: Viernes Santo y 1-1, 24-12, 25-12, 26-12 y 31-12), para que el dato de la última sesión real valga tras un festivo. El calendario por mercado (por ejemplo, el 4 de julio en EE. UU.) queda para el perfil de cada tipo de activo; T-57 fija la lista. T-65 (QA de T-53, H-17): `ps2_festivos` se valida al crear el bloque (booleanos y «MM-DD» estricto) y gana `lunes_de_pascua` (`[PROPUESTO]`: false, como hasta ahora).

**INC-T53-03 · 2026-11-09 · Umbral de revocación de certificados por calibración (Bloque A).** El código revoca un
certificado si el ECE llega a 0,12, pero ese número no figura en el Anexo A (que solo fija `ece_max` 0,15 para
conceder). Decisión `[PROPUESTO]` (hasta T-57): se mantiene 0,12 como `evaluacion.ece_revocacion` y queda para que lo fije el operador (T-57).

**INC-T53-04 · 2026-11-09 · Degradación de H5 de «Limitado» a «No» (Bloque A, D0 12.2 frente al esquema F10).** El
D0 la describe como automática; el esquema de F10 (P-31) exige un cambio de tipo 3 para cualquier paso hacia «No».
Decisión `[PROPUESTO]` (hasta T-57; R23, la más restrictiva): «Sí → Limitado» se aplica sola y «Limitado → No» queda como
propuesta de tipo 3. La degradación se registra en F6 y F10, y el ejecutor lee la tabla vigente de F10 al empezar cada ciclo
(T-53, QA r01 H-05): el cambio se aplica desde el mismo ciclo que la registra, y `efecto_desde` y `fecha_efecto` lo dicen
(T-65, QA de T-53, H-13).

**INC-T53-05 · 2026-11-09 · Siguiente paso, semáforo y confianza (Bloque A).** El código usaba reglas propias,
distintas de las del prompt del Analizador (6.15.5 y 6.16) y del Redactor. Decisión `[PROPUESTO]` (hasta T-57): el semáforo y el
`siguiente_paso_sugerido` siguen ya al prompt del Analizador, con los umbrales en la configuración. La `confianza`
(E ≥ 70 «probable», ahora `presentacion.confianza_probable_E` desde T-65) se deja como está: el prompt del Redactor la usa solo para la barra visual y alinearla cambia el
esquema del paquete; queda para la revisión con el operador.

**INC-T92-01 · 2026-11-10 · Qué limita la «ampliación máxima autorizable» del presupuesto (Bloque A, Anexo A).** El Anexo A da +25 % sin autorización y `ampliacion_max_autorizable: 0.50`, y no dice si el 50 % es el tope del total (base × 1,50, con el automático dentro) o un 50 % más sobre el automático (base × 1,75). Develop usaba la segunda lectura y la auditoría de Astra (A6), la primera. Decisión `[PROPUESTO]` (T-92): **tope del total**, la lectura más prudente. A T-57.

**INC-T65-01 · 2026-11-10 · `Close` frente a `Adj Close` en un CSV de HT-01 (Bloque A).** El README del ejecutor
admite `close` y `adj close` como alias de `cierre`, pero no dice cuál manda si llegan los dos, que es el formato más común
de una exportación de Yahoo. El corpus no fija si las rentabilidades se calculan con el precio o con el precio ajustado.
Decisión `[PROPUESTO]` (hasta T-57; T-65, QA r02 H-13 y QA r03 H-23): no se elige uno en silencio; un CSV con las dos
columnas (o con una cabecera repetida) es un dato inválido del símbolo, que se excluye y se declara. Pregunta para T-57:
«Si un proveedor da el precio y el precio ajustado por dividendos, ¿con cuál se calculan las rentabilidades?».

**INC-T66-01 · 2026-11-10 · Efecto de una «tesis frágil» (Bloque A, PA-05).** La propuesta PA-05 de T-53 pedía que
una tesis frágil, según la regla de Contrarias, pasara a confianza «especulativo» y relevancia ALTA. El Anexo A
(control C10 de HT-09) no tiene ese disparador de ALTA: forzarla genera una advertencia en cada ciclo. Decisión
`[PROPUESTO]`: se aplica solo la confianza «especulativo», y la relevancia sigue la regla del Anexo A. Añadir
«tesis frágil» como disparador de ALTA exige editar el Anexo A y HT-09 (corpus): queda para la revisión de
documentación con el operador.

**INC-T66-02 · 2026-11-10 · Quién resuelve una objeción fuerte (Bloque A, PA-05).** Antes la declaraba resuelta el
propio Analista acusado. Decisión `[PROPUESTO]`: queda resuelta solo si se cumplen las dos condiciones:
- la respuesta del Analista cita evidencia verificable de la propia opción (las fuentes de sus piezas o sus cálculos CALC-);
- el Contradictor lo confirma en una contrarréplica (§5 de su prompt, que el ejecutor no implementaba).

Sin contrarréplica, la objeción sigue abierta.

**Ampliación (QA de T-66, rondas r01 y r02):**
- El `objecion_id` lo asigna el código (`OBJ-<proxy>-nn`, único por opción), y el id que dio el modelo se guarda en `id_modelo`. Así una salida con ids repetidos o ajenos no resuelve objeciones de otra opción, y la contrarréplica solo cuenta para lo que se le envió.
- En el arrastre se conserva el veredicto de Contrarias de F3; si falta, se recalcula con la regla.
- Una objeción fuerte de un registro anterior a PA-05 (resuelta sin `evidencia_citada` o sin `contrarreplica`) se vuelve a abrir: falla cerrado.
- El Contradictor ve el contenido de cada evidencia citada: la afirmación de la pieza, el método de un CALC- y sus valores para la opción, o el título de una REF-.
- Límite conocido: los CALC- del lote son de todo el tipo de activo, así que no se puede exigir que el cálculo sea exclusivo de la opción.
- Ronda r03:
  - Solo es citable la evidencia de la propia opción: las fuentes de sus piezas y sus CALC-. Una REF- registrada en el corpus que no está entre sus piezas no cuenta, porque podría ser de otro tema o, en backtest, posterior a as_of.
  - Lo que ve el Contradictor se sanea (R9).
  - Límite conocido, ronda r04 (H-19, en T-67): la `fuente` de una afirmación del propio Analista es texto libre, de modo que puede hacer «citable» una REF- de otro tema, posterior a as_of o inventada. Además, AG-14 puede devolver una REF- que no se le ofreció. Sigue haciendo falta la confirmación del Contradictor. Se corrige antes del modo sombra con API.
  - En el arrastre manda el veredicto más estricto entre el guardado y el de la regla. Una objeción mal formada o fuera de esquema cuenta como fuerte abierta, sin cortar el ciclo.

**T-62 · Ámbito de la refutación por eslabón (CT-B-17).** El Documento 0 y el Director admiten ESLABON con eslabon_id; el crítico también emite TESIS con eslabon_id. El esquema congelado del paquete admite CADENA y propiedades x_. El ejecutor acepta ambas grafías de entrada y emite CADENA con x_eslabon_id y los candidatos expuestos. TESIS sin referencia a un eslabón mantiene su alcance global. Los detalles y la decisión sobre datos inválidos están en [.docs/tickets/T-62](../.docs/tickets/T-62/README.md).

**INC-T88-01 · 2026-11-12 · Quién paga la escritura de la caché de un prefijo compartido (Bloque A, T-88).** Con varios hilos, la escritura la pagaba el tipo de activo que llegaba primero, y el consumo por tipo de F5 cambiaba entre ejecuciones iguales. Decisión `[PROPUESTO]`:
- durante la fase en paralelo, cada tipo paga la lectura de lo cacheado y la escritura del prompt de su propio analista;
- al acabar la fase, lo escrito de verdad por los agentes compartidos y por el núcleo V6 se reparte por grupo de prefijos, en proporción a lo que escribiría cada tipo solo.

El total cargado es el coste real. Efecto declarado: en un presupuesto justo, el tipo que antes pagaba por llegar primero ya no cierra por eso una fase durante el ciclo. En la V5, cada analista es su propio grupo. En la V6, los analistas comparten grupo por el núcleo común, así que cada kit se reparte con el núcleo (hasta unos 0,03 UC por tipo). Además, en la V6 cada analista carga durante la fase su núcleo y su kit enteros, lo que es prudente. Detalle en [.docs/tickets/T-88](../.docs/tickets/T-88/README.md).

**INC-T91-01 · 2026-11-12 · Regla de resolución de un pronóstico (Bloque A, T-65 y T-91).** El Anexo A fija PS2 como puerta de selección; para resolver no había regla. Decisión `[PROPUESTO]`:
- cada serie (proxy, referencia y cada miembro de la CESTA) necesita un dato posterior a la emisión y no más antiguo, a la fecha de resolución, que la antigüedad de PS2 de su horizonte (H1 en sesiones sin los festivos de `ps2_festivos`);
- si no lo tiene, el pronóstico espera y, pasado el plazo, queda NO_RESOLUBLE;
- si las series acaban en fechas distintas, todas se miden hasta la fecha más reciente en la que todas tienen cierre (r03), que debe pasar en cada una la frescura frente a la fecha de resolución;
- consecuencia declarada (QA r03, H-07): si las series no comparten ninguna fecha reciente (por ejemplo, una referencia semanal fechada en sábado), el pronóstico espera y acaba NO_RESOLUBLE. Antes de la r03 se resolvía con cada serie en su último dato.

Pregunta para T-57: «¿qué antigüedad admite la resolución de un pronóstico, se alinean las series y qué pasa con las que tienen calendarios distintos?». Detalle en [.docs/tickets/T-91](../.docs/tickets/T-91/README.md).

**INC-T117-01 · 2026-11-13 · Señal y umbral de GC1 por tipo de activo en el diseño V6 (Bloque A, T-117).** El Anexo A fija un umbral único: señal compuesta de 0,75 o más y concordancia de al menos dos familias de señales. La señal compuesta es la media de tres familias (momento, tendencia y valoración relativa). En renta fija y en tipos, curvas y volatilidad la tendencia suele salir neutra (en 65 de 136 y en 50 de 102 observaciones), y con 0,75 casi nada pasa; en liquidez pasa poco aunque su tendencia no sea neutra, con solo tres ámbitos. Medido con los datos de ejemplo en 17 fechas: pasan 0,8 ámbitos por fecha en RF, 0,5 en MON y 0,9 en TCV, frente a 1,5 a 1,9 en RV, DIV, MP e IDX. Además, el GC1 por código de la V6 no comprobaba la concordancia de familias. `[PROPUESTO]` (decidido por Claude por defecto, regla del 13-11-2026):
- **Señal:** la señal compuesta en los doce tipos. Es la única señal del Motor que va de 0 a 1 y crece con la oportunidad, que es lo que supone el umbral (H-28 de la QA de T-101).
- **Umbral:** 0,65 en RF, MON y TCV; 0,75 (Anexo A) en los otros nueve. Con 0,65 pasan 2,1 ámbitos por fecha en RF y en TCV y 1,1 en MON, cerca de los demás tipos. En DER no se baja: tiene tres ámbitos y bajar el umbral apenas cambia nada.
- **Concordancia:** se exigen dos familias concordantes cuando manda la señal compuesta, como pide el Anexo A. Con las tres familias y 0,75 no cambia nada (una media de 0,75 obliga a que dos lleguen a 0,6); importa con 0,65 y cuando falta una familia. Si el Motor no da el recuento, el ámbito no se descarta por esto.
- **Lo que ve el Analista (QA r01, H-01):** en la V6 el encargo CT-06 le comunica el umbral de su tipo, el mismo que aplicó GC1.
- **Límite:** los valores salen de datos sintéticos y de un universo de 2 a 8 ámbitos por tipo. Son provisionales hasta tener datos reales; entonces se recalibran con los falsos negativos que cuenta la exploración de GC1. Solo afectan al diseño V6, que es aspirante: el V5, por defecto, no cambia.

Detalle en [.docs/tickets/T-117](../.docs/tickets/T-117/README.md).

**INC-T126-01 · 2026-11-14 · Las guías de mejora del Orquestador (CT-18) no están en el ejecutor (Bloque A, PB-48).** El plan pide que, ante una guía de tipo 2 que contradice una regla (omitir la segunda pasada en banda marginal), el Analizador aplique la más restrictiva (R23), registre el conflicto (COR-) y lo escale (P3-). El ejecutor no emite ni aplica guías CT-18: la elegibilidad la decide HT-03 por código y una lección vigente que sugiera relajar un control no llega a sus entradas (probado). `[PROPUESTO]` (decidido por Claude por defecto): R23 se cumple por construcción; el registro COR-/P3- queda para cuando se implementen las guías del Orquestador, que dependen del modelo real (Fase 5). PB-48 queda «superada en parte».

**INC-T125-01 · 2026-11-14 · Fiabilidad de las fuentes de opinión (Bloque A, T-125, PB-46).** El esquema de F6 (4.5) fija k = 20 y los puntos de historial de 0 a 20 con neutro 10; el Plan de pruebas (PB-46) da la contracción n / (n + k). Lo que no dicen, `[PROPUESTO]` (decidido por Claude por defecto): los puntos son 10 · (1 + BSS contraído); una fuente necesita 5 pronósticos resueltos; se miran los de los últimos 24 meses; un pronóstico explícito sin probabilidad cuenta como 0,7 («más probable que no»); la referencia ingenua es 0,5; el cierre de HT-01 no puede tener más antigüedad que la de H2; una FUE- por fuente y mes.

**INC-T123-01 · 2026-11-14 · IBAN de otros países y tarjetas en R8 (Bloque A, T-123).** `[PROPUESTO]` (decidido por Claude por defecto): un candidato solo cuenta si pasa su dígito de control (módulo 97 y longitud de país para el IBAN; Luhn, prefijo y longitud de red para la tarjeta), para no rechazar mensajes con series de cifras corrientes. La tabla de longitudes es la del registro ISO 13616 para 42 países (SEPA y algunos más); un IBAN de otro país no se reconoce. Una serie pegada a un punto o una coma con cifras no es una tarjeta (es la parte de un decimal). Las tarjetas se registran enmascaradas. **Ronda r02 (QA r01, H-01, H-02 y H-04):** la serie se parte en grupos (separados por hasta tres espacios, puntos o guiones en el IBAN, y espacios o guiones en la tarjeta) y se prueban las ventanas de grupos consecutivos, así que lo que va al lado (caducidad, CVV, una cifra, un código «AB12») no esconde el dato. Una tarjeta no puede llevar una letra ni una cifra pegadas (los tramos de cifras de una huella SHA-256 o de un UUID no cuentan) y sus grupos deben tener al menos cuatro cifras, salvo el último. Por coherencia, el IBAN español con tres separadores seguidos también se detecta ahora (T-122 lo dejaba en dos). Límites conocidos y aceptados: cuatro grupos de cuatro cifras al azar que pasan Luhn con prefijo de red tienen la forma de una tarjeta y se marcan (unas 2 de cada 100); una tarjeta en grupos de menos de cuatro cifras, con puntos o pegada a una letra no se marca; Diners y Maestro no están entre las redes; un IBAN con cuatro o más separadores seguidos, o seguido de otra cifra pegada, tampoco.

**INC-T122-01 · 2026-11-14 · IBAN, máximo de lecciones y números romanos (Bloque A, T-122).** `[PROPUESTO]` (decidido por Claude por defecto):
- **IBAN:** se detecta `ES` (o `es`) con dos cifras de control y 20 cifras, con hasta dos separadores seguidos entre cifras (cualquier espacio, punto o guion). Con tres o más seguidos no se detecta. IBAN de otros países y números de tarjeta, aparte.
- **Máximo de lecciones:** un entero de 1 a 10; el 10 es el máximo del 12.3 del Documento 0, así que la configuración puede bajarlo pero no subirlo. Tras la QA r01 de T-122 (H-13), el 10 se queda en el código como constante citada del Documento 0 (`LECCIONES_POR_ENCARGO_MAX`): es un tope del protocolo, no un parámetro, y llevarlo a la configuración permitiría subirlo. El argumento explícito `max_n` de `lecciones_vigentes` se valida con la misma regla (H-14).
- **Romanos (QA r02 de T-113, H-11), límites conocidos y aceptados:** un romano de una sola letra («Las V ideas», «Los X valores») no se caza, porque «V» y «X» son también letras sueltas y siglas corrientes; tampoco tras determinantes que no están en la lista («Mis», «Otras») ni en minúsculas. Se quitan nombres propios con ordinal tras artículo («Las II Jornadas…», «Los XXV Juegos Olímpicos…»): el Sintetizador debe evitarlos o escribirlos en letra.

**INC-T116-01 · 2026-11-13 · El Broker no puede pedir un horizonte para un solo tipo de activo (Bloque A, PB-10 del plan de pruebas).** El plan pide en PB-10 «H1 para ALT» y exige que F10 cambie solo en P-02. El CT-04 del ejecutor lleva una lista global de `horizontes`: rechaza cada celda que la tabla 8.3 marca «No» (aquí ALT×H1), que sigue sin aplicarse, pero guarda la lista entera en P-03. `[PROPUESTO]` (decidido por Claude por defecto, regla del 13-11-2026): se deja como está, porque manda el código (decisión del operador del 13-11-2026) y el efecto es el que el plan busca: el horizonte «No» no se activa. PB-10 queda como «Superada en parte». Prueba: `test_pb10_la_configuracion_rechazada_en_parte_no_toca_nada_mas`.

**INC-T116-02 · 2026-11-13 · La autorización de ampliación de presupuesto no registra CPI ni EAC (Bloque A, PB-17).** El plan pide que cada AUT- de HA lleve CPI, EAC y motivo. El ejecutor registra la base, la ampliación en UC, el valor de la información, la decisión y el motivo, pero no esos dos índices. `[PROPUESTO]` (decidido por Claude por defecto): no se añaden ahora; son índices de gestión del valor ganado que el ejecutor no calcula en ningún otro sitio y añadirlos es una función nueva, no una corrección. Queda en la deuda (T-116). PB-17 queda como «Superada en parte».

**INC-T116-03 · 2026-11-14 · Cláusulas del Plan de pruebas V3.0 que el ejecutor no cumplía o no hace (Bloque A, ronda r04 de T-116).** Al repasar cláusula a cláusula las filas del mapa (QA r03, H-07 y H-08) salen estas diferencias entre el plan y el ejecutor. `[PROPUESTO]` (decidido por Claude por defecto, regla del 13-11-2026): se corrige solo lo pequeño, seguro y sin cambiar ningún formato congelado (los goldens de contratos siguen coincidiendo); lo demás no se arregla en silencio: la fila queda «Superada en parte» con el hueco dicho.
- **PB-60 y PB-58, corregido.** Con una credencial denegada (o pendiente de una solicitud CT-25 abierta), el ejecutor dejaba la limitación en F10 (o el «modo degradado» en la respuesta a la solicitud) pero ningún entregable declaraba la degradación. Ahora `Credenciales.degradaciones` lista los servicios denegados o pendientes que no se han provisto después, el ciclo los añade a las limitaciones del paquete (y con ellas al informe técnico y al JSON) y el informe visual muestra una nota con el servicio; cuando la credencial se provee, dejan de declararse. No cambia ningún esquema: `limitaciones` ya era una lista de textos. Pruebas de regresión: `test_pb60_credencial_denegada_no_se_vuelve_a_pedir_y_los_entregables_declaran_la_degradacion` (falla sin la corrección) y `test_pb58_el_servicio_pendiente_se_declara_hasta_la_provision_y_el_valor_no_llega_a_ningun_contexto`.
- **PB-22, corregido.** R2 dice que un mensaje por un canal no previsto «se rechaza, se registra y se escala»; la incidencia CANAL_NO_PREVISTO no llevaba la marca de escalado que sí lleva la de acceso fuera de matriz (`escalado_operador`, «rechazada y registrada»). Ahora la lleva. Prueba: `test_pb22_tres_mensajes_por_canales_no_previstos_tres_incidencias_y_ningun_efecto`.
- **PB-32, sin tocar.** El plan pide para el certificado una re-ejecución CT-10 coincidente; el Evaluador emite el certificado sin ella. Es una función nueva (encargar y comparar la re-ejecución), no una corrección.
- **PB-33, sin tocar.** El plan pide «Novedades en F6» (la sección semanal de altas, revocaciones, ajustes y lecciones del esquema de F6); el ejecutor no la publica: la revocación y la lección quedan como entradas sueltas de F6.
- **PB-07, sin tocar.** El plan pide una respuesta final por CT-03 con referencias al acabar el análisis escalado; el ejecutor envía una sola CT-03, la provisional, con el RUN- enlazado.
- **PB-11, sin tocar.** El Evaluador no genera la lección de producto que compara las opciones enviadas al Bloque B con las descartadas.
- **PB-21, sin tocar.** La incidencia de seguridad lleva el campo, pero no el tipo de dato protegido (clave API, IBAN): solo «credenciales o datos personales». Añadirlo exige clasificar cada patrón de `secretos_en_texto`, una función nueva.
- **PB-36, sin tocar.** La recalibración automática solo mueve los pesos de RK (P-11); el caso del plan (umbral E, P-09, y P-05) no se recalibra, y la propuesta P3- fuera de banda queda en F6, no en la cola de HA.
- **PB-38, sin tocar.** El informe técnico solo lista las objeciones de las opciones del top-3: la opción que se queda fuera por una objeción fuerte sin resolver queda documentada en F3, no en el técnico.
- **PB-61, sin tocar.** Una respuesta tardía del Broker que invalida un supuesto no abre una revisión C2: el ejecutor solo lo dice en la respuesta.
- **PB-62, sin tocar.** El aviso CONSULTA_RECURRENTE sale (CT-22 y F5), pero no se crea la lección de producto.
- **PB-19, sin tocar.** Con el Analizador saturado, el monitor deja un CAR- en HA, pero no reordena por prioridad, no avisa al Coordinador de los plazos ni propone un cambio de tipo 3 si se repite.
- **PB-50, sin tocar.** El Evaluador solo degrada automáticamente H5 (por hitos); un horizonte que pierde frente a la referencia con significación (DM-HLN), como RF × H2 en el plan, no pasa de «Sí» a «Limitado».
- **PB-64, sin tocar.** Los estados de los H5 por hitos (EN_CURSO_CONFORME, DESVIADO, INVALIDADO) se calculan y se usan en el seguimiento C6, pero no se publican en F6 ni en los entregables.

**INC-T114-01 · 2026-11-13 · El Anexo B y el ejecutor no piden lo mismo en los contratos (Bloque A, Fase 3, T-114).** Al derivar un esquema JSON de cada contrato solo con el Anexo B del Documento 0 V5.1 y compararlo con lo que hace el ejecutor, salen estas diferencias. **Decisión del operador (13-11-2026): manda el código del Bloque A.** El Documento 0 se escribió antes de construir el bloque y habrá que modificarlo: el Anexo B se corrige en la próxima entrega del Documento 0 para que describa lo que hace el ejecutor. Hasta entonces no se cambia ni el Anexo B (corpus congelado) ni el código; las diferencias quedan congeladas en `bloque_a/11_Ejecutor/tests/goldens/divergencias_anexo_b.json`, y una diferencia nueva hace fallar la suite.
- **Lotes (CT-11, CT-12 y CT-13):** el Anexo B describe una pieza, un encargo o una petición por mensaje. El ejecutor los agrupa en `piezas`, `encargos` y `peticiones`, y rechaza el ejemplo del Anexo B tal cual.
- **Fases de CT-06:** el Anexo B admite CRIBADO, INVESTIGACION, PROFUNDIZACION y SEGUIMIENTO. El ciclo simulado emite `CRIBADO_E_INVESTIGACION` y `RESPUESTA_OBJECIONES`.
- **Campos que el ejecutor no exige:** el Anexo B los nombra sin marcarlos como opcionales y `Mensajeria.crear` admite el mensaje sin ellos. Los principales:
  - CT-01: `fecha_objetivo`, `nivel_forzado`, `referencia_previa`;
  - CT-03: `contexto`, `urgencia` y, en la respuesta, `escalado`;
  - CT-04: los cuatro bloques (`decisiones`, `valoracion_informe`, `configuracion`, `resultado_comunicado`), que en la práctica se envían por separado;
  - CT-23: `preguntas`, `plazo_respuesta`, `punto_control`, `seg_id`;
  - CT-24: todo menos `accion`;
  - CT-25: `herramienta`, `urgencia` y, en la respuesta, `credencial_ref` y `caducidad`.
- **Retornos internos (CT-06 a CT-14):** el ejecutor no valida sus campos en la mensajería. La respuesta de cada agente se valida con los esquemas de `ESQUEMAS` (congelados en `esquemas_respuestas.json`), que no llevan los mismos nombres que el Anexo B.
- **`fecha_corte` de CT-09:** el Anexo B la hace obligatoria solo en evaluaciones y backtesting; el ejecutor la exige siempre. Es más estricto, no más laxo.
- **CT-16 a CT-21:** el Anexo B no da sus campos (los remite a los prompts de sistema). Se congelan su canal, la regla de `run_id` y, de los que el ejecutor emite (CT-16, CT-17 y CT-19), la forma del mensaje.
- **`tipo` de CT-22 (ronda r02, QA r01 H-02):** el Anexo B sí nombra un campo de CT-22: «En CT-22, `tipo` admite además `CONSULTA_RECURRENTE` y `DECISION_SEGUIMIENTO`». El ejecutor emite esos dos valores en otro campo, `tipo_aviso` (`interfaz_broker.py` y `seguimiento.py`), y usa `tipo` para `DECISIONES_BROKER` y `PREGUNTA_REPETIDA`. Sus cuatro avisos no llevan, por tanto, el mismo campo. Fuera del Anexo B, el §7.6 y el §7.9 del Documento 0 también hablan de «CT-22, tipo `PREGUNTA_REPETIDA`» y «tipo `CONSULTA_RECURRENTE`». Se congela como está (manda el código); para la próxima entrega del Documento 0: decidir si el campo es `tipo` o `tipo_aviso` y decirlo en el Anexo B.
- **Lo que se ve al medir los mensajes que el ejecutor emite (ronda r02):** con once flujos simulados en lugar de un ciclo salen más diferencias, todas del mismo tipo que las de arriba (campos que el Anexo B nombra y el ejecutor no envía). Las principales:
  - CT-03: la consulta no lleva `query_id` (el bloque lo asigna al recibirla) ni `contexto.run_id` y `contexto.opp_id` si el Broker no los da; en una respuesta N0, `escalado` es nulo;
  - CT-04: `configuracion` lleva solo lo que cambia;
  - CT-23: las preguntas llevan `texto`, `supuesto_declarado` y `efecto_si_falso`, sin `origen`, `por_que_importa` ni `opciones_sugeridas`; la aportación entrante no lleva `preguntas` ni plazo; la respuesta no lleva `supuestos_aplicados`, ni `documentos` en cada respuesta;
  - CT-23, CT-24 y CT-25, retorno: el bloque JSON del Anexo B pone el estado del objeto en `estado`; el ejecutor lo lleva en `estado_consulta`, `estado_seguimiento` y `estado_credencial`, como pide el §6.2.6 del propio Documento 0, y deja `estado` para el estado común;
  - CT-25: el recordatorio no lleva `herramienta` ni `urgencia`; una respuesta DENEGADA no lleva `caducidad`.
- **Retornos rechazados:** el Anexo B no dice qué campos lleva un retorno con estado RECHAZADO o SIN_RESULTADO (el §6.2.6 solo pide el motivo; en CT-09 prevé un `RECHAZADO` con motivo `ACLARACION_REQUERIDA`). Los esquemas derivados describen el retorno con resultado y no juzgan los otros. El ejecutor exige los campos de retorno de CT-03 también en un retorno RECHAZADO. Para la próxima entrega del Documento 0: decirlo.
- **Lo que el Anexo B deja abierto** y el esquema derivado no restringe: la codificación de `coincide` (CT-10) y de `independiente` (CT-11), y los nombres de las claves de `fechas` (CT-11).

- **Listas cerradas del Anexo B (QA r02 de T-114, H-10):** fuera de CT-01 y CT-02, la mensajería no aplica las listas cerradas del Anexo B (18 casos de la batería en 10 contratos) ni la condición de `contenido` de CT-23 («solo en ENTRANTE»); la batería lo congela.

Lista completa en el golden y detalle en [.docs/tickets/T-114](../.docs/tickets/T-114/analisis-tecnico.md).

**INC-T114-02 · 2026-11-13 · Los ejemplos publicados llevan una clave de aviso (Bloque A, T-114).** Los dos ejemplos de `06_Plantillas_entregables` empiezan por `x_aviso_ejemplo` («datos ficticios…»). El esquema del paquete de oportunidades la admite. El del informe de seguimiento de opción (V5.1) tiene `additionalProperties: false` en la raíz y no la declara, así que su propio ejemplo publicado no lo cumple; sin esa clave, lo cumple. `[PROPUESTO]`: no se toca la entrega (corpus congelado); la prueba `test_ca5…` congela el hecho: el único incumplimiento es esa clave. Para una entrega futura: declarar `x_aviso_ejemplo` en el esquema o quitarla del ejemplo.
**INC-T121-01 · 2026-11-14 · Decisiones al corregir los hallazgos abiertos de la QA r01 de T-118 (Bloque A, T-121).** `[PROPUESTO]` hasta T-57. El operador pidió que el agente decidiera por defecto, con la opción más prudente, y lo dejara apuntado.
- **Fecha de corte en las 14 fichas de la Fase 1 (H-04).** Un dato en línea con fecha posterior a la fecha de corte de la petición se rechaza (no se recorta), como en la Fase 2 y en HT-01. Se compara por día: el dato del día del corte se sirve, también con hora (T-127, QA r01 H-08 y H-09: con zona horaria, el día en UTC, con el mismo ayudante en los tres módulos; y también en la fecha de NAV de FON-DISC-001: ver INC-T127-01). Se comprueban todas las fechas observadas, también las de los bloques opcionales (historias para percentiles, decisiones de un banco central, consenso del BPA, precios e índices de IDX-CONC-001, rentabilidades de los eventos comparables, fecha de los activos indexados, encuestas, serie publicada de la prima por plazo). En TCV-TP-001 un dato posterior al corte en la segunda vía rechaza la petición; no se degrada a «segunda vía no calculada». Una fecha de corte que no es una fecha (un número, un booleano, una lista) se rechaza.
  - **No son observaciones** y pueden ser posteriores al corte: los nodos y contratos de una curva, las reuniones futuras de MON-EXP-001, la fecha de efectividad de un rebalanceo anunciado (IDX-REB-001) y, como ya decía INC-T119-01, los vencimientos y los desbloqueos. Sí se compara la fecha de los datos de MON-EXP-001 y la del anuncio de IDX-REB-001.
  - En FON-DISC-001 y FON-FLOW-001 la «fecha de corte» de la salida sigue siendo la última fecha de sus datos (es la de la ficha); la de la petición es otra.
- **CT-10 y la configuración (H-01).** La re-ejecución usa la configuración guardada en el artefacto. Si aun así el resultado difiere, con los mismos datos y la misma versión de la ficha, es **ERROR_ORIGINAL**, cambie o no la configuración vigente. **CONVENCION_DISTINTA** queda para cuando la re-ejecución no ha podido usar la configuración de entonces: una sección que la ficha lee y el artefacto no guarda, un registro ilegible, o una sección cuya parte de `por_defecto.yaml` ha cambiado y de la que el valor guardado no trae todas las claves (de ahí tomaría la ficha lo que falta). Tras la sesión T-57, que cambiará `por_defecto.yaml`, un artefacto con la sección entera guardada sigue pudiendo dar ERROR_ORIGINAL (**T-127, QA r01 H-07:** no era cierto si el fichero ganaba una clave en una sección leída; desde T-127 «de la que el valor guardado no trae todas las claves» se sustituye por «de la que la re-ejecución ha tomado alguna ruta de `por_defecto.yaml`»: ver INC-T127-01). Sustituye a la regla de INC-T118-01 («si la configuración guardada ya no es la vigente… CONVENCION_DISTINTA»).
- **Forma de la llamada a `Motor.servir` (H-02).** Lo que va al Registro de cálculos (`operacion`, `datos`, `parametros`, `perfil`, `clase`, `horizonte`, `modo`, `plan`, `prioridad`, `semilla`, `fecha_corte`) tiene que poder escribirse: copiarse, serializarse como JSON y codificarse en UTF-8 (un sustituto Unicode suelto no se puede). `horizonte`, `modo` y `prioridad` tienen que ser textos. `solicitante`, `run_id` y `msg_id` tienen que ser textos escribibles (o nulos los dos últimos); si no, la petición se rechaza y la entrada los lleva vacíos. Un solicitante que no es texto es CANAL_NO_AUTORIZADO, como ya decía T-112; lo demás, DATOS_INCOHERENTES.
- **Re-ejecución que no llega a la ficha (H-03).** Si los datos del artefacto ya no se pueden resolver (una serie de HT-01 que el proveedor ya no tiene, una fecha posterior al `as_of`) o el artefacto está mal formado, la re-ejecución queda en el Registro con `coincide` NO y ERROR_REEJECUCION, y su causa. Siguen siendo excepciones las cuatro imposibilidades declaradas (sin motivo, un `calc_id` que no es un servicio, una ficha sin manejador y un artefacto sin los valores en línea).
- **Cota de REG-HMM-001 (H-05).** Es `horizontes.H5` de la configuración del Motor en semanas, con el calendario de 52 semanas y 12 meses por año (120 meses → 520 semanas; con H5 en 60 meses, 260). Si H5 viene en semanas, tal cual; si viene en sesiones, dividido por `calendario.sesiones_por_semana`. Sustituye a la mención de las 520 semanas «derivadas a mano» de INC-T118-01; los 360 meses de TEM-DIFF-001 siguen derivados del rango de H5 del Documento 0 (30 años).

Pregunta para T-57: «¿Una re-ejecución que no coincide, hecha con la configuración guardada en el artefacto, debe culpar al cálculo original aunque la configuración vigente haya cambiado?». Detalle en [.docs/tickets/T-121](../.docs/tickets/T-121/README.md).

**INC-T119-01 · 2026-11-13 · Decisiones de método en las diez fichas P2 del Motor (Bloque A, T-119).** Las fichas dejan huecos que se han cubierto con la opción más prudente, `[PROPUESTO]` hasta que el operador o una revisión del Catálogo decidan (el operador pidió que el agente decida por defecto y lo deje apuntado). El detalle, ficha a ficha, está en `.docs/tickets/T-119/analisis-tecnico.md`.
- **Comunes a las diez:**
  - los datos llegan en línea, con su fuente y su fecha; ninguna ficha lee series de HT-01, porque son datos especializados que el ejecutor no tiene;
  - cotas de tamaño que ninguna ficha fija: historia de 100 años como máximo y listas de parámetros de 12 elementos (las de INC-T113-01); 500 componentes de un agregado; 10 000 fechas de flujos; 50 000 transacciones; 1 000 tramos de una curva de costes; 100 vencimientos por componente; 1 000 desbloqueos por token; plazos y ventanas hasta H5 (30 años);
  - una cifra de entrada de magnitud mayor que 1e100 se rechaza: por encima, las sumas desbordan y una división por un total infinito daría un cero con apariencia de cifra;
  - las fechas contractuales futuras (vencimientos de deuda, desbloqueos de tokens) no son observaciones: pueden ser posteriores a la fecha de corte. Todo dato observado posterior al corte se rechaza;
  - frontera con el Bloque B (1.6 del Catálogo): FIR-CRED-001, REI-LEV-001 y CHR-TOKEN-001 entregan solo el agregado y su dispersión, sin ninguna fila por componente. El rechazo «si se pide para ordenar emisores» no lo puede detectar un cálculo: lo garantiza la forma de la salida, y un parámetro no declarado (por ejemplo, uno que pida un orden) se rechaza.
- **FIR-CRED-001:**
  - la volatilidad de las acciones entra ya calculada (anual), no como serie diaria;
  - `mu` por defecto es el rendimiento histórico, la primera opción de la ficha, y cada componente lo aporta; con `mu: r` no hay bloque «real»;
  - un componente sin deuda se rechaza (no tiene distancia al impago); el solicitante lo retira y lo declara en la cobertura;
  - «dominado por emisores sin acciones cotizadas» se lee como cobertura declarada por debajo de 0,5;
  - el diferencial implícito del segmento es la media de los componentes ponderada por deuda; el triángulo de crédito usa la pérdida en caso de impago del propio modelo;
  - el sistema se resuelve con dos raíces de Brent anidadas, con tolerancia 1e-13 y 200 iteraciones; si el error supera 1e-6, se rechaza.
- **FX-BEER-001:**
  - la constante del equilibrio se fija para que el desalineamiento tenga media nula en toda la muestra («residuo de media nula»);
  - el intervalo del desalineamiento solo recoge la incertidumbre de los coeficientes (covarianza de Newey-West del DOLS) y usa `evaluacion.nivel_ic` de la configuración;
  - con Johansen no hay errores estándar ni intervalo: se entregan como `null` y se declara;
  - los fundamentales son los cuatro de la ficha, en la transformación que declare el solicitante; el tipo real entra en nivel y se toma su logaritmo;
  - «con vintages» se lee como una fecha de edición de los datos, no anterior a la última observación ni posterior al corte;
  - retardos de 1 a 4 trimestres; contraste de cointegración al 0,05 con las tablas de FX-COINT-001; sin evidencia, se sirve con la limitación.
- **CMD-REAL-001:**
  - moneda constante del último mes de la serie;
  - la tendencia es la de FX-TREND-001 sobre el logaritmo del precio real mensual, con su nivel por defecto;
  - el coste marginal es el del tramo en el que la producción acumulada, ordenada por coste, alcanza el percentil; se lleva a moneda constante con el IPC del mes de la curva, que debe estar en la serie.
- **REI-LEV-001:**
  - LTV con deuda neta (deuda menos caja), como EPRA;
  - la suma de vencimientos debe ser la deuda con la tolerancia de la ficha (1e-10); si no, se rechaza por perfil incompleto;
  - el margen es el de los datos si la petición no lo fija;
  - la holgura frente a *covenants* se calcula sobre los componentes que los declaran.
- **CHR-ONCHAIN-001:**
  - serie diaria sin huecos; σ muestral de toda la ventana; la limitación «pocos ciclos» se pone por debajo de 4 años;
  - `media_nvt` de 1 a 365 días; la fuente de la petición, si se da, debe ser la de los datos.
- **CHR-TOKEN-001:**
  - sin oferta máxima, la valoración totalmente diluida usa la oferta total;
  - agregado ponderado por capitalización circulante;
  - los desbloqueos futuros no pueden superar la oferta no circulante; los de fecha no posterior a la de los datos no cuentan y se declaran;
  - el rendimiento de *staking* y la concentración se agregan sobre los tokens que los declaran, con su cobertura.
- **PRV-PME-001:**
  - el índice debe tener nivel en cada fecha de flujo y en la del NAV: no se interpola;
  - LN-PME no se calcula, porque la ficha no le da parámetro; PME+ solo con `metodo: PME+`;
  - la TIR se busca entre −0,99 y 10; con varios cambios de signo se avisa, y si no hay raíz en el rango se entrega `null`.
- **PRV-CF-001:**
  - las tasas de aportación y el crecimiento no tienen valor por defecto: sin ellos, o sin `vida_anios`, no hay proyección y se declara;
  - el rendimiento mínimo de distribución del modelo de Takahashi-Alexander es 0, porque la ficha no lo nombra; la tasa del último año declarado se mantiene; la edad son los años completos desde el primer flujo.
- **ALT-HF-001:**
  - los siete factores de Fung y Hsieh se llaman MKT, SMB, BONO10A, CREDITO, PTFSBD, PTFSFX y PTFSCOM;
  - el desuavizado es el Geltner de ALT-DESMOOTH-001 con φ estimado, y se aplica a la rentabilidad antes de restar el tipo sin riesgo; un φ negativo se declara.
- **ALT-AUC-001:**
  - índice anual; ventas repetidas por Bailey-Muth-Nourse sin la ponderación de Case-Shiller; los pares de un mismo año se descartan y se cuentan;
  - la dispersión es la de los residuos de la regresión, en logaritmos;
  - la rentabilidad neta supone una sola compraventa en toda la ventana del índice; sin comisiones declaradas no se calcula;
  - no se aplica ningún ajuste de sesgo de selección, y se declara.

- **Ronda r02 (QA r01 NO APTO, 2026-11-14):**
  - **frontera con el Bloque B (H-01).** La forma de la salida no basta: un agregado necesita un mínimo de componentes distintos. REI-LEV-001 rechaza menos de **3 componentes** (la ficha no da mínimo; con dos, el mínimo y el máximo de la dispersión son las dos cifras individuales — **justificación incorrecta, corregida en T-127 (QA r02, H-10):** con tres, el mínimo, la mediana y el máximo son las tres cifras individuales, y con hasta seis la dispersión y el agregado las dan todas; el mínimo de 3 se mantiene para el agregado, pero desde T-127 la dispersión solo se entrega con 7 componentes o más: ver INC-T127-01); REI-NAV-001 (T-112) rechaza **1 componente** (mínimo 2); FIR-CRED-001 conserva su mínimo de 10 de la ficha. Dos componentes con los mismos datos del cálculo (aunque lleven otro identificador) son el mismo emisor o token y se rechazan, en FIR-CRED-001 (capitalización, volatilidad y deudas), REI-LEV-001 (GAV, deuda, caja, EBITDA, gastos financieros y FFO) y CHR-TOKEN-001 (precio, ofertas, emisión y quema). CHR-TOKEN-001 con **un solo token** solo se sirve si la petición declara `ambito_es_red: true` (la ficha lo admite «cuando el ámbito es la propia red»), y lo declara en las limitaciones; un sector necesita 2 tokens distintos;
  - **TIR con varias soluciones (H-03).** Si los extremos del rango no aíslan una raíz y los flujos cambian de signo más de una vez, se cuentan los cambios de signo del valor actual neto en una rejilla de **1 000 puntos** (uniforme en ln(1 + r)) y la limitación dice cuántas soluciones hay; no se entrega ninguna (`null`, como antes);
  - **rangos de dominio que ya estaban en el código (H-04)**, ahora enumerados: tipos (FIR-CRED-001) y costes y *swap* (REI-LEV-001) en (−1, 1); volatilidad de las acciones hasta 10 (1 000 % anual); margen de refinanciación en [0, 1); rendimiento de *staking* en (−1, 10); `percentil_coste` (CMD-REAL-001) en (0, 1]; en ALT-AUC-001, hasta 20 características y al menos 3 periodos en el índice;
  - **lo que no se calcula, en la entrega (H-05 y H-09).** PRV-PME-001 lleva entre sus advertencias que LN-PME no se calcula; CMD-REAL-001, que el intervalo de la tendencia (el de FX-TREND-001, Gilbert 1987) no lleva la corrección de autocorrelación de Hamed-Rao que sí lleva su p-valor. No se cambia el método de FX-TREND-001 (heredado; cambiaría cifras servidas de otra ficha);
  - **caché del Motor (H-06 y H-08, heredados).** La caché solo entrega un resultado a una petición con la misma firma de tipos (un `Decimal`, un `numpy.float32` y un texto con el mismo valor ya no colisionan) y con las mismas secciones de configuración que la ficha leyó entonces. Si la firma no se puede calcular, no se usa la caché;
  - **solicitante (H-07, heredado).** Va en T-121 (H-02): `solicitante`, `run_id` y `msg_id` tienen que ser textos que se puedan escribir en el Registro.

Pregunta para T-57: «¿se aceptan estas decisiones de método y estas cotas en las diez fichas P2?». Detalle en [.docs/tickets/T-119](../.docs/tickets/T-119/README.md).

**INC-T127-01 · 2026-11-14 · Frontera con el Bloque B en las fichas con componentes, CT-10 con `por_defecto.yaml` y el día de la fecha de corte (Bloque A, T-127).** Hallazgos de la QA r02 de T-119 (H-10, H-11) y de la QA r01 de T-121 (H-07 a H-09). `[PROPUESTO]` hasta T-57; el operador pidió que el agente decidiera por defecto y lo dejara apuntado.
- **Frontera con el Bloque B (H-10).** El Catálogo (1.6) pide que los instrumentos individuales «solo entren como componentes de un agregado». Una regla común (`FRONTERA_B` de `motor/fichas_p2.py`, en los `UMBRALES` de FIR-CRED-001, REI-LEV-001 y CHR-TOKEN-001; la petición no la cambia) impide que una sola petición devuelva la cifra de un emisor o un token:
  - **casi clones:** dos componentes cuyos datos del cálculo (los mismos de la r02) difieren cada uno en **menos de un 1 % relativo** (|a − b| ≤ 0,01·máx(|a|, |b|)) son el mismo, también en cadena (cierre transitivo), y el agregado se rechaza. Por debajo del 1 %, el agregado de copias perturbadas es la cifra del emisor con dos o más cifras significativas. Dos emisores reales que coincidan a menos del 1 % en todos esos datos a la vez no se esperan;
  - **dominancia (1, k):** se rechaza el agregado si un componente pesa **más del 95 %** de una de sus bases de ponderación (FIR-CRED-001: la deuda; REI-LEV-001: GAV, deuda, EBITDA, gastos financieros y FFO en valor absoluto; CHR-TOKEN-001 de un sector: capitalización circulante y FDV). Es la regla de dominancia del control de revelación estadística; el 95 % deja pasar los casos de control (hasta el 90,9 %) y rechaza el componente «de peso casi total» de la QA (99,9999 %);
  - **estadísticos de orden:** el mínimo, los cuartiles y el máximo solo se entregan con **7 componentes o más** (5 estadísticos + 2). Con n ≤ 5, los cinco estadísticos (cuantiles de tipo 7) dan los n valores; con 6, el agregado ponderado de la misma métrica es la ecuación que falta. Por debajo, `dispersion` (y las holguras frente a covenants) van a `null` y se declara. FIR-CRED-001 (≥ 10) no cambia. **Esto corrige la justificación del mínimo de 3 de INC-T119-01** (con 3, mínimo, mediana y máximo eran las tres cifras); el mínimo de 3 del agregado de REI-LEV-001 se mantiene;
  - **subconjuntos:** los componentes que declaran un dato opcional son otro agregado. Los covenants de REI-LEV-001 necesitan el mínimo de la ficha (3); el rendimiento de *staking* y la concentración de CHR-TOKEN-001, 2 tokens que no estén dominados (95 % de su capitalización). Si no, no se calculan y se declara (con un solo componente, «en incumplimiento» o el *staking* eran los de ese emisor o token);
  - **la propia red:** con un solo token, `ambito_es_red: true` ya no basta: el ámbito tiene que ser una red de `redes_propias` (hoy Bitcoin → BTC y Ethereum → ETH, las del perfil PERF-CHR) y el token, el suyo. Lo que el solicitante llame BTC queda con ese nombre en el Registro;
  - **casos de control:** se adaptan a la regla sin perder lo que comprueban. REI-LEV-001: S3 declara covenants (3 de 3) y la dispersión con 3 componentes se comprueba ausente; CHR-TOKEN-001: TKB declara *staking* y concentración, y la dispersión con 2 tokens se comprueba ausente. La dispersión, las holguras y el *staking* parcial se comprueban con 7 componentes en `tests/test_t127_hallazgos.py`;
  - **lo que una regla no puede impedir** (se declara): restar dos peticiones que difieren en un componente, rellenos diseñados para que un estadístico de orden caiga en un emisor (con 7 o más), o compensaciones entre componentes que se anulan en una suma. Lo detecta el Registro de cálculos (cada petición queda), no el cálculo. REI-NAV-001 (T-112, fuera de las P2) entrega una fila por sociedad con su identificador; su ficha pide «prima/descuento agregado y su dispersión»: queda para un ticket propio.
- **Caché (H-11).** La firma de tipos de la caché marca cada contenedor (objeto, lista, tupla) y cada escalar que no es de JSON (`servicio._marcado`): una tupla no sale de la caché de una lista, en ningún orden. Un `numpy.float64` sigue siendo un `float`.
- **CT-10 y `por_defecto.yaml` (H-07).** La configuración que el Motor da a la ficha apunta qué rutas no encuentra y toma de `por_defecto.yaml` (`parametro` llama a `anotar_respaldo`). La re-ejecución da CONVENCION_DISTINTA por una sección guardada solo si su huella en el fichero ha cambiado **y** la re-ejecución ha tomado de él alguna ruta de esa sección; una clave nueva del fichero que la ficha no lee ya no ablanda un ERROR_ORIGINAL. `parametro` no mezcla una sección encontrada con la del fichero: un valor guardado al que le falta una clave que la ficha no usa da ERROR_ORIGINAL (antes CONVENCION_DISTINTA). Cumple lo que INC-T121-01 prometía para T-57.
- **Día de la fecha de corte (H-08).** Un solo ayudante, `operaciones.dia`: con zona horaria, el día en UTC; sin zona, el día tal cual; el mismo para el dato y para el corte. Lo usan las fichas de la Fase 2 (`fichas_reales._fecha`), MON e IDX, TCV (que antes tomaba los diez primeros caracteres, el día local, y ahora rechaza un texto con basura tras la fecha) y FON y DER (que pasan las fechas con zona a UTC, `operaciones.sin_zona`, y ya no fallan con zonas mezcladas). Así, «(D+1)T00:30+14:00» con el corte en D se sirve en las tres familias (es del día D en UTC) y «DT23:00−05:00» se rechaza en las tres. Alternativa más estricta, no elegida: el día más tardío (el local o el de UTC) para el dato y el más temprano para el corte. El ciclo no produce fechas con zona (el corte sale de `as_of.date()`).
- **FON-DISC-001 (H-09).** La fecha de NAV se compara por día con la última de «fechas» (la fecha de corte de la ficha); el mensaje dice cuál es.

Pregunta para T-57: «¿se aceptan el 1 %, el 95 %, los 7 componentes y la lista de redes con token propio como regla de la frontera con el Bloque B?». Detalle en [.docs/tickets/T-127](../.docs/tickets/T-127/README.md).

**INC-T113-01 · 2026-11-13 · Decisiones al cerrar la deuda técnica del Bloque A (T-113).** `[PROPUESTO]`:
- **Rangos de MON e IDX (H-24):**
  - un horizonte o una ventana de la petición no pasa de H5 (120 meses, 2 520 sesiones). Son los valores de `horizontes.H5` de la configuración, pero están escritos en `fichas_mon_idx.py` (`_MESES_H5`, `_SESIONES_H5`), no se leen de ella: si H5 cambia, hay que cambiarlos a mano (QA r01);
  - una ventana histórica no pasa de 100 años;
  - `diferencial_estable_dias` no pasa de 252;
  - `incremento_pb` va de 0 a 100;
  - una lista no pasa de 12 elementos, y la de escenarios, de 20;
  - cada escenario de `escenarios_pb` (MON-FIX-001) va de −1000 a 1000 pb, es decir, ±10 puntos porcentuales sobre el tipo implícito (r02; estaba en el código sin declarar).
- **Margen de la cota del nodo (H-27, r02):** en MON-EXP-001 el desajuste de un nodo se compara con la cota del residuo multiplicada por (1 + 1e-6). El margen relativo `1e-6` solo absorbe el error de coma flotante del cálculo de la cota; no amplía la tolerancia de la ficha. Estaba en el código sin declarar.
- **Romanos (T-109):** un número romano detrás de un determinante («las VII ideas») es una cifra; detrás de un nombre propio o de «siglo», no. Desde la r02 (H-03) tiene que ser un romano bien formado de dos letras o más, hasta XXXIX, y no estar en `filtro_r21_codigos`: «Las IIC» y «Los VIX» no son cifras. Un romano mayor que XXXIX como cantidad sigue siendo un límite declarado.
- **Tickers en minúscula (H-34):** solo se cazan los del universo. Uno que no está en el universo sigue siendo un límite declarado. También (observaciones O-1 y O-3 de la QA r01, sin corregir): el ticker tras el plural («las acciones»), tras «la acción de», «el bono», «la cripto» o «el token», o con la inicial en mayúscula; y las letras sueltas separadas por «,», «|», «*», «+», «:», la raya o un guion entre espacios.
- **Frases de 30 s (H-50):** si el Sintetizador escribe una o tres, se toman las dos primeras o se completa con el texto por defecto, y se declara como FORMATO. Con ninguna, con cuatro o con cualquier otra respuesta que no cumpla el esquema, se entregan la integración y los textos por defecto del código y el paquete lleva la limitación «El Sintetizador no dio una respuesta válida…» (r02, H-07).
- **Caché de resultados (H-54):** una línea ilegible se descarta y se cuenta. En la cinta de grabación, solo la última línea cortada; cualquier otra línea ilegible da error, con el fichero y la línea. Desde la r02 (H-02 y H-06): al arrancar, la caché (siempre) y la cinta (solo al grabar, y solo si se ha leído bien) dejan el fichero acabado en un salto de línea, quitando la línea cortada del final, para que lo siguiente que se grabe no se pegue a ella; al reproducir, la cinta no se toca. Un registro de la caché cuya `clave` no es un texto, o demasiado anidado, se descarta como ilegible. Las líneas descartadas se declaran con una incidencia `HERRAMIENTA` (HA) al crear el Bloque. Una última línea sin salto que es JSON válido pero no un registro («12») se descarta en la caché y sigue siendo un error en la cinta.
- **Curación de AG-12 con presupuesto (H-14; H-08 de la QA r01):** la curación se trata como **alcance**, no como control. Cargada a la bolsa de su tipo, un presupuesto justo la cierra antes (con 3,0 UC por tipo, 21 limitaciones por presupuesto en lugar de 10) y esas piezas quedan sin la clasificación de AG-12 (toman el tipo de afirmación de la pieza o `ANALISIS`, y la confianza `probable`) y sin sus alertas, que solo se registran. Los controles los hace el código y no dependen de ella: la deduplicación por hash, el recuento de raíces (PS1) y R9. Por eso la limitación sigue diciendo «alcance reducido, controles intactos (R16)». Es la opción prudente con el presupuesto (ninguna llamada sin bolsa); si el operador prefiere que la curación no pueda cerrarse por presupuesto, hay que reservarle una parte de la bolsa.
- **`contenido_sensible` (H-56; H-01 de la QA r01):** una estructura que se contiene a sí misma o demasiado anidada para serializarla no se puede comprobar y se da por sensible (falla cerrado). Un diccionario con claves que no son texto sigue siendo un `TypeError` para el llamador, salvo que antes se halle un secreto.

Detalle en [.docs/tickets/T-113](../.docs/tickets/T-113/README.md).

**INC-T112-01 · 2026-11-13 · Decisiones de método en las 36 fichas de la Fase 2 del Motor (Bloque A, T-112).** Las fichas dejan huecos que se han cubierto así, `[PROPUESTO]` hasta que el operador o una revisión del Catálogo decidan. El detalle, ficha a ficha, está en las notas de cada grupo: `.docs/tickets/T-112/grupo_S.md`, `grupo_R.md`, `grupo_V.md` y `grupo_P.md`. Las que más pesan:
- **Modelos propios en lugar de bibliotecas que A no declara** (statsmodels, scikit-learn, `arch`):
  - Markov switching y HMM por EM con numpy;
  - Johansen y Engle-Granger con las tablas asintóticas de MacKinnon, Haug y Michelis (1999) y MacKinnon (2010), así que `nivel` solo admite 0,01, 0,05 o 0,10;
  - en SCN-H-001 y en el histórico filtrado de RISK-VAR-001, un GARCH(1,1) por QMLE gaussiana, que no es el GARCH-t de VOL-GARCH-001;
  - en ML-PRED-001, modelos lineales regularizados, sin árboles.
- **Semillas y arranques:**
  - semilla por defecto en las fichas con azar; la de la petición manda;
  - EM con 20 arranques y un tope de iteraciones; si no converge, se rechaza;
  - un caso estadístico de BT-PBO-001 (PBO ≈ 0,5 sin habilidad) con una tolerancia de ±0,3.
- **Datos que la ficha no lista en «Entradas mínimas»:**
  - ACC-VAL-001 proyecta el FCFF₀ con una tasa aportada con fuente y pide el coste de la deuda;
  - REI-FFO-001 pide el porcentaje de CAPEX sobre rentas;
  - FX-MOM-001 pide la dirección de cada par y la historia del diferencial.
- **Lecturas estrictas de una frase ambigua:**
  - REI-NAV-001 rechaza un NAV con más de 12 meses («rechazo … sin advertencia»);
  - ALT-DESMOOTH-001 en GLM rechaza las raíces dentro o sobre el círculo unidad, sin otro margen;
  - DEC-VOI-001 lee sus umbrales de `parametros_ht03` de la configuración, no de un F10 recalibrado.
- **Convenciones:**
  - RISK-VAR-001 al 0,975, con rango 0,90–0,99 y 250 observaciones como mínimo (las mismas que ya usaban TCV y DER);
  - FIR-PRICE-001 solo con ACT/ACT-ICMA o 30E/360 y bonos «bullet», y con rescates, la duración del precio al peor;
  - un parámetro no declarado por la ficha se rechaza.

- **Ronda r02 (QA r01):**
  - cotas de tamaño en cada ficha, sacadas de la ficha, de otra que se cita (FC-EVAL-001, SIM-MC-001, FIR-CURVE-001) o del horizonte H5 en sesiones; las demás, `[PROPUESTO]`. Al máximo, el servicio más caro es REG-HMM-001, unos 4 min;
  - un dato posterior a la fecha de corte se rechaza, no se recorta;
  - DEC-VOI-001 lee sus umbrales de la configuración del Motor;
  - el detalle, en la sección «Ronda r02» de cada nota de grupo.

Pregunta para T-57: «¿se aceptan estas decisiones de método, las cotas de tamaño y los modelos propios en lugar de las bibliotecas externas?». Detalle en [.docs/tickets/T-112](../.docs/tickets/T-112/README.md).

**INC-T112-02 · 2026-11-13 · La re-ejecución CT-10 (AUD-REX-001): dos documentos del corpus no coinciden (Bloque A, T-112).**
- **El valor de `coincide`:** el esquema del Registro de cálculos V2.0 escribe `DENTRO_TOLERANCIA`, con las categorías DATOS_DISTINTOS, CONVENCION_DISTINTA, ERROR_ORIGINAL, ERROR_REEJECUCION y NO_DETERMINISMO. El Catálogo y el prompt MC-08 escriben `DENTRO_DE_TOLERANCIA`, con otras categorías.
- **Decisión `[PROPUESTO]`:** el ejecutor sigue al esquema del Registro, porque es donde escribe. Corrige además la lógica: `DENTRO_TOLERANCIA` quiere decir que hay diferencia y no supera la tolerancia, no que los datos son distintos.
- **Valores en línea:** desde T-112, el artefacto guarda los valores en línea (campo `valor` de `datos`, que el esquema ya prevé) para poder re-ejecutar los cálculos con datos en línea. Se comprueba su huella. Un artefacto anterior, que solo guardaba «en línea», no se reconstruye: la re-ejecución es imposible.
- **Pregunta para una revisión del corpus:** unificar los dos vocabularios.

**INC-T118-01 · 2026-11-13 · Decisiones al corregir los hallazgos de la QA r02 de T-112 (Bloque A, T-118).** `[PROPUESTO]` hasta T-57. El operador pidió que el agente decidiera por defecto, con la opción más prudente, y lo dejara apuntado.
- **Cotas de los datos del grupo R (H-10).** Un dato mayor que su cota se rechaza; no se recorta. Lo mismo una serie de HT-01, como ya hace el grupo S.
  - Salen de la configuración o de una ficha, sin número nuevo:
    - una historia tiene como mucho las sesiones de H5 (2 520 por defecto);
    - una muestra simulada, el máximo de trayectorias de SIM-MC-001 (1 000 000);
    - los estados de un régimen, los de REG-HMM-001 (4);
    - los horizontes de ML-CAL-001, los cinco del Documento 0.
  - Números que no están en ninguna ficha:
    - **BT-PBO-001 admite hasta 1 000 configuraciones**, la cota de contrastes por familia de ST-INF-001 (INC-T112-01);
    - **ML-PRED-001 admite hasta 20 variables**, el tope que la ficha da a la rejilla.
  - Con esas cotas, el servicio más caro del grupo R tarda 52 s por el Motor, con sus dos pasadas, en una máquina compartida. Son dos: BT-VAR-001 generando el VaR con Cornish-Fisher sobre 2 520 rendimientos, y BT-PBO-001 con S = 20 y 1 000 configuraciones.
- **Profundidad de una petición (H-13).** Una petición con más de **32 niveles** de anidamiento se rechaza por su forma. Los casos de control llegan a 9. Es un número técnico: evita que la copia de la petición agote la pila.
- **Tipo de `clase` y `perfil` (H-13).** `clase` tiene que ser un texto, y `perfil`, un texto o una lista. Dos semillas que no se pueden comparar cuentan como dos semillas distintas, y la petición se rechaza.
- **Fecha de corte en el grupo R (H-09).** Se compara por día: el dato del día del corte es conocible. Además de ML-PRED-001, lo aplica ML-CAL-001 cuando sus pares llevan fecha.
- **Re-ejecución CT-10 y configuración (H-11 y H-14).**
  - El artefacto guarda, de cada sección de la configuración que la ficha lee, su valor y la huella de esa sección en `por_defecto.yaml`. La re-ejecución usa esos valores, no los vigentes.
  - Si el resultado no coincide y la configuración guardada ya no es la vigente, o el artefacto no la guarda, la categoría es CONVENCION_DISTINTA. ERROR_ORIGINAL queda para cuando constan todas las entradas y son las vigentes. Es la opción prudente: no se culpa a un cálculo sin poder reproducir sus condiciones. A cambio, un resultado alterado en un artefacto anterior a T-118 sale como CONVENCION_DISTINTA si su ficha lee la configuración.
  - Si la ficha rechaza las entradas del artefacto, la re-ejecución queda registrada con `coincide` NO y ERROR_REEJECUCION, la categoría que el esquema del Registro ya tenía.
  - **Campos fuera del esquema:** `artefacto.configuracion_usada` y `reejecucion.configuracion` no están en la lista de campos del esquema del Registro de cálculos V2.0, que es corpus congelado y no se ha tocado. El esquema pide un artefacto reproducible, y sin esos números no lo era. Para una revisión del corpus: añadirlos a la tabla del esquema.
- **H2 y H5 en el grupo P (H-12).**
  - No hay discrepancia: son dos números distintos. El Documento 0 (§2, «Horizontes») da el rango de cada horizonte: H2, de 2 a 8 semanas; H5, de 5 a 30 años. La configuración da su duración nominal: `horizontes.H2` 4 semanas y `horizontes.H5` 120 meses.
  - Las cotas del grupo P usan el extremo del rango. Con la duración nominal no cabría el valor por defecto de la propia ficha: REI-CAP-001 pide una ventana de 20 años, y H5 nominal son 10.
  - **Decisión:** los dos extremos (8 semanas y 30 años) siguen en el código, citando el Documento 0, porque la configuración no los trae. No se añade una clave a la configuración ni se cambia lo que T-112 dejó aprobado. Lo que sí está en la configuración se lee de ella en cada llamada: las sesiones por semana, H5 en sesiones y la ventana de datos.
  - Quedan igual, derivadas a mano de esos rangos: las 520 semanas de REG-HMM-001 y los 30 años y 360 meses de TEM-DIFF-001.

Preguntas para T-57: «¿Hasta cuántas variantes de una estrategia quieres poder comparar de una vez al medir el sobreajuste (hoy 1 000), y cuántas variables explicativas admites en un modelo predictivo (hoy 20)?» y «¿Quieres que los rangos de los horizontes del Documento 0 (H2 de 2 a 8 semanas, H5 de 5 a 30 años) estén en la configuración, para poder cambiarlos sin tocar el código?». Detalle en [.docs/tickets/T-118](../.docs/tickets/T-118/README.md).

**INC-T102-01 · 2026-11-13 · Umbrales del filtro de los textos del Sintetizador V6 (Bloque A, T-102).** Tras cinco QA NO APTO, el operador decidió: «umbrales y sin cifras libres». Valores `[PROPUESTO]`, para que el operador los fije en T-57:
- **Prohibidas:** en un banco ciego nuevo de al menos 40, escrito por el revisor sin enseñárselo al implementador, pasan sin declararse como mucho el 5 %. Tolerancia cero para las que llevan un dato (dígitos, un marcador de cuenta o un código en mayúsculas de un instrumento, salvo los límites declarados).
- **Legítimas:** de un banco ciego de al menos 60, escritas como pide el prompt, se quitan como mucho el 10 %. Las legítimas con un número en letra («los dos bancos centrales», «S&P quinientos») se miden aparte, como coste de la regla estricta.
- **Sin cifras libres:** los marcadores de cuenta no valen en el texto libre. Las cuentas las escribe el código: la primera frase de 30 s y el principio de cada motivo llano.
- **Límites declarados de R21:** un nombre propio sin código ni sufijo; un ticker en minúscula sin vehículo, o tras «la acción», «el valor» o «el título» (T-109); códigos que coinciden con una sigla de la lista (COP); tickers de una letra sin vehículo; y los romanos como cantidad («las VII ideas»).

Pregunta para T-57: «¿qué porcentaje de frases prohibidas puede pasar sin declararse, y qué porcentaje de legítimas se puede perder?». Detalle en [.docs/tickets/T-102](../.docs/tickets/T-102/README.md).

**INC-T106-01 · 2026-11-12 · Decisiones de método en las 21 fichas V5.0 del Motor (Bloque A, T-106).** Las fichas dejan huecos que se han cubierto así, `[PROPUESTO]` hasta que el operador o una revisión del Catálogo decidan:
- **Niveles que la ficha no fija:**
  - IC del 95 % (de ST-INF-001) y rezagos HAC por la regla de ACC-FACT-001 en TCV-SLOPE-001;
  - ES al 97,5 % (de RISK-VAR-001) en TCV-VIXTS-001 y DER-VRP-001;
  - retardos HAR 1, 5 y 22 (Corsi) en DER-VRP-001;
  - en IDX-REB-001, sin `nivel_ic` no se da el IC (se declara).
- **«Aclaración» se trata como rechazo** (`ErrorFicha`), porque la interfaz CT-09 no tiene canal de aclaración.
- **Falla cerrado donde la ficha calla:**
  - pesos que no suman 1 (IDX-CONC-001) o un índice HY sin recuperación declarada (TCV-CDS-001) se rechazan;
  - FON-LEV-001 exige L en los datos aunque el parámetro traiga 2;
  - entre «Entradas mínimas» y «Rechazo», se aplica el mínimo más estricto.
- **Fuera, como dato de entrada o limitación:**
  - la simulación SIM-MC-001 de FON-LEV-001;
  - el modelo afín de TCV-BEI-001;
  - SCN-H-001 en IDX-ERP-001;
  - los regresores de TCV-SLOPE-001 (con vintages);
  - las rentabilidades históricas de VIXTS.

**Ronda r02 (QA r01 de T-106):**
- en MON-EXP-001, solo si el solicitante declara `precision_cotizacion` el desajuste admitido por nodo es esa precisión (si no, la tolerancia de la ficha);
- en MON-EXP-001, se rechaza la curva cuyo redondeo podría mover un tramo un incremento Δ entero, y una curva cotizada plana en tipos simples (forwards no planos);
- en TCV, los umbrales de rechazo son fijos (no los baja una petición), y los rangos de los parámetros salen de FIR-CARRY-001 y RISK-VAR-001.

**Ronda r03 (QA r02 de T-106):**
- en MON e IDX, los umbrales de rechazo y de limitación y los rangos admitidos también son fijos: una petición que los traiga se rechaza (H-14);
- en DER-VRP-001, `nivel_es` se limita al rango 0,90–0,99 de RISK-VAR-001, de donde se toma el nivel (H-20);
- en MON-EXP-001 (H-19):
  - «tipo vigente»: `probabilidades` reparte el movimiento de cada reunión frente al tipo en vigor justo antes de ella, y `probabilidades_acumuladas` aplica la fórmula literal frente al tipo oficial de hoy;
  - con tantos nodos útiles como tramos y algún tramo sin nodos en sus dos fechas de reunión, la curva se rechaza: la hipótesis escalonada no se puede contrastar;
  - sin `precision_cotizacion`, cada cotización lleva como precisión el medio último dígito con que viene escrita;
  - si el redondeo puede mover una probabilidad más que la tolerancia de la ficha, se sirve con una limitación que da la cota (H-16);
- cifras no finitas (H-17): las fichas MON, IDX, FON y DER y el Motor las rechazan. TCV sirve `None` con una limitación cuando un cociente no está definido (por ejemplo, un VIX3M casi nulo) y nunca entrega un número no finito. Queda así: en TCV el resto del resultado sigue siendo útil.

Detalle por ficha en [.docs/tickets/T-106](../.docs/tickets/T-106/analisis-tecnico.md).

