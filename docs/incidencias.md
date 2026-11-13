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

**INC-T113-01 · 2026-11-13 · Decisiones al cerrar la deuda técnica del Bloque A (T-113).** `[PROPUESTO]`:
- **Rangos de MON e IDX (H-24):**
  - un horizonte o una ventana de la petición no pasa de H5 de la configuración (120 meses, 2 520 sesiones);
  - una ventana histórica no pasa de 100 años;
  - `diferencial_estable_dias` no pasa de 252;
  - `incremento_pb` va de 0 a 100;
  - una lista no pasa de 12 elementos, y la de escenarios, de 20.
- **Romanos (T-109):** un número romano detrás de un determinante («las VII ideas») es una cifra; detrás de un nombre propio o de «siglo», no.
- **Tickers en minúscula (H-34):** solo se cazan los del universo. Uno que no está en el universo sigue siendo un límite declarado.
- **Frases de 30 s (H-50):** si el Sintetizador escribe una o tres, se toman las dos primeras o se completa con el texto por defecto, y se declara como FORMATO.
- **Caché de resultados (H-54):** una línea ilegible se descarta y se cuenta. En la cinta de grabación, solo la última línea cortada; cualquier otra línea ilegible da error, con el fichero y la línea.

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

