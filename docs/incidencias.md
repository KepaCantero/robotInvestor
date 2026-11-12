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

El total cargado es el coste real. Efecto declarado: en un presupuesto justo, el tipo que antes pagaba por llegar primero ya no cierra por eso una fase durante el ciclo. Detalle en [.docs/tickets/T-88](../.docs/tickets/T-88/README.md).

**INC-T91-01 · 2026-11-12 · Regla de resolución de un pronóstico (Bloque A, T-65 y T-91).** El Anexo A fija PS2 como puerta de selección; para resolver no había regla. Decisión `[PROPUESTO]`:
- cada serie (proxy, referencia y cada miembro de la CESTA) necesita un dato posterior a la emisión y no más antiguo, a la fecha de resolución, que la antigüedad de PS2 de su horizonte (H1 en sesiones sin los festivos de `ps2_festivos`);
- si no lo tiene, el pronóstico espera y, pasado el plazo, queda NO_RESOLUBLE;
- si las series acaban en fechas distintas, todas se miden hasta la más antigua, y cada una vuelve a pasar la frescura frente a la fecha de resolución.

Pregunta para T-57: «¿qué antigüedad admite la resolución de un pronóstico, y se alinean las series?». Detalle en [.docs/tickets/T-91](../.docs/tickets/T-91/README.md).
