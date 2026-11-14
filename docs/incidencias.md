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

**INC-T116-01 · 2026-11-13 · El Broker no puede pedir un horizonte para un solo tipo de activo (Bloque A, PB-10 del plan de pruebas).** El plan pide en PB-10 «H1 para ALT» y exige que F10 cambie solo en P-02. El CT-04 del ejecutor lleva una lista global de `horizontes`: rechaza cada celda que la tabla 8.3 marca «No» (aquí ALT×H1), que sigue sin aplicarse, pero guarda la lista entera en P-03. `[PROPUESTO]` (decidido por Claude por defecto, regla del 13-11-2026): se deja como está, porque manda el código (decisión del operador del 13-11-2026) y el efecto es el que el plan busca: el horizonte «No» no se activa. PB-10 queda como «Superada en parte». Prueba: `test_pb10_la_configuracion_rechazada_en_parte_no_toca_nada_mas`.

**INC-T116-02 · 2026-11-13 · La autorización de ampliación de presupuesto no registra CPI ni EAC (Bloque A, PB-17).** El plan pide que cada AUT- de HA lleve CPI, EAC y motivo. El ejecutor registra la base, la ampliación en UC, el valor de la información, la decisión y el motivo, pero no esos dos índices. `[PROPUESTO]` (decidido por Claude por defecto): no se añaden ahora; son índices de gestión del valor ganado que el ejecutor no calcula en ningún otro sitio y añadirlos es una función nueva, no una corrección. Queda en la deuda (T-116). PB-17 queda como «Superada en parte».

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

Lista completa en el golden y detalle en [.docs/tickets/T-114](../.docs/tickets/T-114/analisis-tecnico.md).

**INC-T114-02 · 2026-11-13 · Los ejemplos publicados llevan una clave de aviso (Bloque A, T-114).** Los dos ejemplos de `06_Plantillas_entregables` empiezan por `x_aviso_ejemplo` («datos ficticios…»). El esquema del paquete de oportunidades la admite. El del informe de seguimiento de opción (V5.1) tiene `additionalProperties: false` en la raíz y no la declara, así que su propio ejemplo publicado no lo cumple; sin esa clave, lo cumple. `[PROPUESTO]`: no se toca la entrega (corpus congelado); la prueba `test_ca5…` congela el hecho: el único incumplimiento es esa clave. Para una entrega futura: declarar `x_aviso_ejemplo` en el esquema o quitarla del ejemplo.
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

Pregunta para T-57: «¿se aceptan estas decisiones de método y estas cotas en las diez fichas P2?». Detalle en [.docs/tickets/T-119](../.docs/tickets/T-119/README.md).

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

