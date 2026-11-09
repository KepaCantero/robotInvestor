# Revisión independiente del código del ejecutor del Bloque A

**Alcance:** `/home/claude/repo/bloque_a/11_Ejecutor/` (paquete `bloque_a/`). No he modificado ningún archivo del repositorio.
**Scripts de reproducción:** `/tmp/claude-0/-home-claude/d1ab3b3e-4909-5455-a67a-e01975b6ec91/scratchpad/rev_a_bloque/codigo/` (en adelante `$R`).
**Cómo ejecutarlos:** `cd $R && /home/claude/repo/.venv/bin/python <script>.py`. Todos usan el cliente simulado (mock) y no necesitan red.

**Referencia del Documento 0:** «Doc 0» es `01_Gobernanza/Documento 0 … V5.1.md`.

HT-03 y HT-09 son copias idénticas de `10_Herramientas/` (lo he comprobado con `diff -q`). Por eso CA-01, CA-11 y CA-12 afectan también a la herramienta de referencia.

## Hallazgos

### CA-01 · alta · Continuidad: una opción vigente «sustituida» se queda fuera aunque haya hueco, y entra una nueva con menos RK
- **Dónde:** `bloque_a/herramientas/referencia/ht03_puntuaciones.py:378-395`.
- **Qué pasa:**
  - Cada vigente se compara con la *mejor* opción nueva.
  - Si está a más de 10 puntos de ella, va a la lista `sustituidas` y no vuelve a entrar en la selección.
  - Los huecos libres se rellenan con cualquier opción nueva, aunque tenga un RK menor que el de la vigente descartada.
- **Ejemplo:** nuevas con RK 85 y 62, y una vigente con RK 70. El top-3 sale como `[N1 85, N2 62]` y el motivo dice «3 elegibles». La vigente (RK 70) queda fuera y se publican solo dos opciones.
- **Reproducción:** `ca_continuidad.py`.
- **Debería:** según Doc 0 9.6.4, una vigente «se sustituye» por una alternativa mejor, es decir, cede *su puesto*. No pierde la elegibilidad. Además, según 9.6.5, si hay tres elegibles se proponen tres.
- **Corrección:** sustituir una vigente solo cuando una nueva más de 10 puntos mejor ocupa su plaza. Las vigentes «sustituidas» que no se desplazan deben seguir compitiendo por RK en los huecos libres.

### CA-02 · alta · Un dato no numérico de HT-01 da un resultado inventado (NO_OCURRIDO) en F4
- **Dónde:**
  - `herramientas/ht01_datos.py:141` aplica `dropna(subset=["cierre"])` *antes* de convertir a número (`pd.to_numeric(errors="coerce")`, l. 145-147). Por eso un cierre `-`, `n.d.` o `1.234,5` llega como NaN.
  - `evaluador.py:159-161` calcula `int(nan > 0) = 0` sin comprobar NaN.
  - Además, `ht01_datos.py:97-98` deja visible una fila con `fecha_publicacion` no interpretable (p. ej. `31/06/2026`): `pub.isna()` la trata como publicada.
- **Qué pasa:**
  - El PRG queda `RESUELTO`, con `resultado: NO_OCURRIDO`, `rent_proxy: NaN` y `comprobacion_fuga: SUPERADA`.
  - Ese resultado entra en Brier, en los certificados y en el historial de aciertos publicado.
  - Además se escribe `NaN` (JSON no estándar) en F4.
- **Reproducción:** `ca_nan_resolver.py` (de extremo a extremo con `Bloque` y `Evaluador.resolver`) y `ca_nan_cierre.py`.
- **Debería:** las reglas del proyecto exigen fallar cerrado (un dato inválido no se convierte en un resultado). Doc 0, Anexo A, en la fila de PS2, pide datos de HT-01 con fecha y válidos. En la resolución, lo que corresponde es esperar o marcar `NO_RESOLUBLE`.
- **Corrección:**
  - En `_normalizar_df`, convertir a número primero y después rechazar el archivo, o eliminar la fila declarándolo.
  - En `resolver`, tratar `not math.isfinite(x)` como dato no disponible.
  - Rechazar las filas cuya `fecha_publicacion` no se pueda interpretar.

### CA-03 · alta · Los entregables se escriben en las carpetas de entrega antes de validarlos y quedan allí, marcados `APTO`, cuando la entrega se bloquea
- **Dónde:**
  - `redaccion.py:371-393`: se escriben el HTML, el JSON (l. 384) y el MD, y *después* se validan el esquema y la coherencia (l. 381-393). En l. 377 se fuerza `estado_g3 = "APTO_CON_ADVERTENCIAS"` si HT-09 bloquea.
  - Lo mismo ocurre en C6: `seguimiento.py:198-202` escribe el informe antes de mirar el dictamen.
  - Además, el informe C6 **no se valida en ejecución contra** `Esquema JSON - Informe de seguimiento de opción - V5.1.json` (no hay `jsonschema` en `seguimiento.py` ni en HT-09). Solo lo valida la prueba `tests/test_v51.py:126`, aunque el README dice que se valida.
- **Qué pasa:** con un fallo de coherencia entre entregables (simulado), el run queda `entrega: BLOQUEADA`. Aun así, en `ent/Paquetes JSON/` queda el JSON con `estado_g3 = "APTO"`, y en `ent/Informes visuales Usuario/` el HTML.
- **Reproducción:** `ca_entregable_bloqueado.py`.
- **Debería:** según Doc 0 7.3 (G3), «BLOQUEADO impide la entrega». Las reglas del proyecto piden validar antes de mutar y validar los formatos contra los esquemas de `06_Plantillas_entregables`.
- **Corrección:**
  - Generar en memoria, o en una carpeta temporal, y validar el esquema, la coherencia y HT-09.
  - Mover a las carpetas de entrega solo si el resultado es APTO o APTO_CON_ADVERTENCIAS.
  - No sobrescribir `estado_g3` con un valor que no sea el dictamen efectivo.
  - Validar en C6 con el esquema V5.1.

### CA-04 · alta · Una consulta CT-23 BLOQUEANTE no pausa nada si afecta a todos los tipos del alcance o no declara tipos
- **Dónde:**
  - `orquestacion.py:369`: `if pausadas and len(pausadas) < len(clases)`.
  - `interfaz_broker.py:136`: `for cl in (c.get("clases") or [])`. Una consulta sin `clases` no pausa ningún tipo, aunque `_afecta` (l. 129) la considere aplicable a todos.
- **Qué pasa:** con una BLOQUEANTE sobre CRI y un ciclo con alcance `["CRI"]`, CRI se analiza y se publica (`OPP-2026-0001`) sin ninguna limitación declarada. Con una BLOQUEANTE sin tipos, `clases_pausadas(...)` devuelve `{}`.
- **Reproducción:** `ca_pausa.py`.
- **Debería:** según Doc 0 7.9 y R26 (y la Arquitectura, sección 6), una BLOQUEANTE sin respuesta pausa la parte afectada en su siguiente punto de control.
- **Corrección:**
  - Si todos los tipos quedan pausados, cerrar el run como PARCIAL o SIN_RESULTADO declarado, en lugar de analizarlo todo.
  - Una BLOQUEANTE sin `clases` debe pausar todo el alcance (o rechazarse al enviarla).

### CA-05 · media · PS1 y G1 se superan solo con la pieza automática de momentum, cuya dirección no depende de la tesis
- **Dónde:** `orquestacion.py:607-611`, `783-784` y `822`.
  - El ejecutor añade a cada finalista una pieza «Momentum 12-1» con fuente `HT-01:<proxy>`, marcada `favorable` si el momentum es mayor que 0 y `contraria` si no, sin mirar la vista ni la tesis.
  - Las fuentes HT-01 cuentan como raíz A PRIMARIA.
  - `_ps1` es verdadero con una sola raíz A PRIMARIA, y G1 = PS1.
- **Qué pasa:** una finalista con tesis **bajista** y ninguna afirmación corroborada da `PS1 = True` con la raíz `HT-01:SPY (A, PRIMARIA)`.
- **Reproducción:** `ca_ps1.py`.
- **Debería:** según Doc 0 9.3 (PS1), las afirmaciones *centrales* deben estar corroboradas. Un momentum positivo no corrobora una tesis bajista. El README declara como simplificación que «las raíces HT-01 cuentan como primarias de nivel A», pero no la asignación de dirección sin tener en cuenta la vista.
- **Corrección:**
  - Calcular la dirección de la pieza frente a la vista o tesis de la finalista.
  - Exigir que la raíz HT-01 respalde una afirmación central, no solo que exista.

### CA-06 · alta · Un símbolo del universo sin historia en la fecha as_of vacía en silencio todo su tipo de activo
- **Dónde:** `orquestacion.py:231-236`. Las seis fichas del Motor se piden en lote para todo el universo del tipo. Si una se rechaza porque falta un símbolo, `continue` descarta la ficha para **todos** los símbolos, sin anotar ninguna laguna.
- **Qué pasa:**
  - Añado un par DIV que empieza a cotizar el 2026-09-01 y ejecuto el ciclo a 2026-06-05.
  - Las seis fichas salen `REJECTED` («sin datos de USDNEW=X en el rango»).
  - DIV pasa de 3 opciones a 0, con `estado: COMPLETO`, sin limitación declarada y con un «menos de tres» que lo atribuye al embudo normal (0 de 7 superan GC1).
- **Reproducción:** `ca_cesta_nuevo.py`, y como línea base `ca_cesta_base.py`.
- **Debería:**
  - Según R14 y 9.6.5, el motivo de «menos de tres» debe ser cierto.
  - Según R16 y PS2, la falta de datos se declara (PARCIAL).
  - En un backtest, que los activos coticen desde fechas distintas es lo normal.
- **Corrección:** excluir del lote, con su incidencia, los símbolos sin datos hasta as_of, o pedir las fichas por símbolo. Si una ficha falla, marcar el tipo como PARCIAL con la laguna.

### CA-07 · media · Corrección de Holm aplicada mal: no se detiene al primer fallo
- **Dónde:** `motor/evaluacion.py:208-212` (`holm` devuelve `alfa/(m-i)` por celda) y `evaluador.py:313-317` (cada celda se compara con su propio umbral de forma independiente).
- **Qué pasa:** con p = {RV|H3: 0,06; RF|H3: 0,07} y α = 0,10, RV|H3 no supera su umbral (0,05), pero RF|H3 sí se acepta (0,07 ≤ 0,10). En el procedimiento de Holm el contraste se detiene en el primer fallo y no se rechaza ninguna. Así, una celda puede obtener un certificado y publicar probabilidades numéricas (R13) que no le corresponden.
- **Reproducción:** `ca_holm.py`.
- **Debería:** Doc 0, Anexo A, fila «Certificado de horizonte (R13)»: «con varias celdas candidatas en la misma revisión se aplica la corrección de Holm».
- **Corrección:** procedimiento escalonado: recorrer las p de menor a mayor y, en cuanto una falle, dar por fallidas todas las siguientes.
- **Nota (verificada leyendo el código):** el Anexo A define la celda como «clase × horizonte × **método**». Sin embargo, `revisar_certificados` agrupa solo por (clase, horizonte) y emite `metodo: None` (`evaluador.py:301-305, 321`). Como HT-09 acepta cualquier método cuando el certificado no tiene método (`ht09_validador_g3.py:473-475`), un certificado ganado con un método habilita a otro.

### CA-08 · media · Los hitos de H5 entran en la celda H4 y en el historial publicado como pronósticos independientes
- **Dónde:**
  - `sintesis.py:155`: cada hito se registra con `horizonte: "H4"`, la misma probabilidad que el H5 y el mismo suceso acumulado; hay hitos a 30 y 54 meses.
  - `evaluador.py:207-216`, `242` y `302-304` no filtran `es_hito`. Ese filtro solo existe en `estado_h5` y en `seguimiento.py`.
- **Qué pasa:** un único PRG H5 aporta 3 observaciones correlacionadas a `RV|H4` (cuentan para n ≥ 100 del certificado) y 3 al historial de aciertos que ve el usuario.
- **Reproducción:** `ca_hitos_h4.py` (salida `{'RV|H4': 3}`, historial `n = 3`).
- **Debería:**
  - Doc 0, Anexo A: el certificado exige «≥ 100 pronósticos resueltos en la celda».
  - Según 8.3 y 12.1, los hitos son la vía de evaluación del H5 y tienen su propia métrica (tasa de hitos por tipo × H5). No son pronósticos H4 adicionales.
- **Corrección:** excluir `es_hito` de `metricas`, `revisar_certificados`, `historial_aciertos` y `recalibrar`, o contarlos en una celda propia «H5-hitos».

### CA-09 · media · El almacén no protege la congelación de F4 (R11)
- **Dónde:** `almacen.py:118-126`. AG-10 puede escribir una segunda `ALTA` con un `prg_id` que ya existe, y `estado()` la superpone campo a campo. AG-20 puede resolver dos veces un mismo PRG o resolver un PRG que no existe.
- **Qué pasa:** una segunda ALTA cambia `prob_interna` de 0,6 a 0,9, el `sentido` y la `fecha_resolucion`, y la cadena de hash sigue `True`. También se aceptan una re-resolución (la segunda cambia el resultado de 1 a 0) y una resolución huérfana.
- **Reproducción:** `ca_f4_realta.py`.
- **Debería:** según R11, los pronósticos se congelan. La matriz de escritura (5.1) dice que AG-20 solo resuelve. Las reglas del proyecto piden validar antes de mutar. No he encontrado ninguna ruta actual del ejecutor que lo dispare (`_congelar` salta `prg_existente`), así que es una salvaguarda que falta, no una corrupción ya observada.
- **Corrección:** en `_comprobar_reserva` de F4:
  - rechazar una ALTA con un `prg_id` ya existente;
  - rechazar una RESOLUCION sobre un PRG inexistente o que no esté `ABIERTO`.

### CA-10 · media · Bóveda de HT-01: caducidad sin validar, caducidad ignorada por defecto y permisos de `secretos.json`
- **Dónde:** `herramientas/ht01_boveda.py:41-47`, `52`, `63-75` y `88-91`, y `interfaz_broker.py:251-252`.
- **Qué pasa:**
  - (a) `valor_para_herramienta(alias)` sin `hoy` devuelve el valor de una credencial caducada en 2020.
  - (b) `depositar(..., caducidad="31/12/2026")` se acepta. Después, `listar()` y `estado()` lanzan `ValueError`. Por la vía `Credenciales.depositar`, el secreto ya está guardado cuando `responder` falla (muta antes de validar).
  - (c) `secretos.json` se crea con los permisos del umask (`0o644`) antes del `chmod 0600`, y si `chmod` falla el error se ignora en silencio.
- **Reproducción:** `ca_boveda.py`.
- **Debería:** R8, Doc 0 7.10 y CT-25 piden que la credencial solo esté en la bóveda y sea accesible solo para la herramienta. Fallar cerrado ante una caducidad inválida o un permiso no aplicado.
- **Corrección:**
  - Validar `caducidad` (ISO) antes de escribir.
  - Hacer obligatorio `hoy` en `valor_para_herramienta` (o usar el reloj del bloque).
  - Crear el archivo con `os.open(..., O_CREAT|O_WRONLY, 0o600)` y escritura atómica, y propagar el fallo de `chmod`.
- **Nota:** `valor_para_herramienta` no tiene llamadas todavía, así que (a) está latente.

### CA-11 · baja · C18 cuenta como «≥ 3 hitos» tres copias del mismo hito
- **Dónde:** `ht09_validador_g3.py:643-660`. Cuenta los elementos de la lista, sin exigir `hit_id` ni fechas distintas.
- **Qué pasa:** tres copias de `HIT-2026-0001` con la misma fecha dan «sin incidencias». Hitos fuera de orden y con 42 años de separación solo generan ADVERTENCIA.
- **Reproducción:** `ca_h5_hitos.py`.
- **Debería:** Doc 0 8.3 y el Anexo A («Pronósticos H5») piden ≥ 3 hitos intermedios verificables, el primero a ≤ 12 meses y con ≤ 24 meses entre hitos consecutivos (régimen «Operador»).
- **Corrección:** exigir `hit_id` y fechas únicas y en orden. Decidir, y documentar como incidencia, si el espaciado es un bloqueo o una advertencia.

### CA-12 · media (discrepancia con la especificación) · Con tres opciones del mismo clúster y sin alternativa a ≤ 10 puntos se publican las tres
- **Dónde:** `ht03_puntuaciones.py:411-413`, que define una «excepción» que declara la concentración.
- **Qué pasa:** con A, B y C en CL-1 (RK 80, 79 y 78) y D en CL-2 (RK 60), el top-3 es `A, B, C` con `excepcion: True`.
- **Reproducción:** `ca_diversidad.py`.
- **Debería:** Doc 0 9.6.3 dice «no más de dos opciones del mismo clúster». La segunda frase solo regula la sustitución cuando hay alternativa; no prevé una excepción (y la Arquitectura, sección 7, dice «máximo dos»). Por R23 manda la regla más restrictiva.
- **Corrección:** sin alternativa, publicar dos opciones con «menos de tres» motivado, o registrar la excepción como incidencia de especificación (regla 7 del proyecto) en lugar de decidirla en el código.

### CA-13 · baja · Un certificado perfectamente calibrado se revoca (ECE = 0 se trata como 1)
- **Dónde:** `evaluador.py:329`: `(m["calibracion"]["ece"] or 1) >= 0.12`. El umbral 0,12 está escrito a mano y no figura en el Anexo A.
- **Qué pasa:** con p = 0,75 en 100 casos y 75 aciertos, ECE = 0,0, la expresión vale `True` y el certificado se revoca.
- **Reproducción:** `ca_ece_cero.py`.
- **Corrección:** tratar el caso con `ece is None` y sacar el umbral de revocación de la configuración (o del Anexo A).

### CA-14 · baja · Números escritos a mano que contradicen o duplican el Anexo A
- **PS2** (`orquestacion.py:860`): `+2` días en H1, así que H1 admite datos de 3 días incluso entre semana, cuando el Anexo A dice «H1: 1 día». Reproducción: `ca_ps2.py` (miércoles con dato del domingo: `PS2 = True`).
- **Otros números escritos a mano:**
  - `ML-CLUS-001 umbral_rho 0.7, ventana 104` (`orquestacion.py:843`);
  - tasa base de 0,5 por defecto y recorte a [0,05; 0,95] (`evaluador.py:113-116`);
  - `PROB_DE_BANDA.get(..., 0.5)` cuando falta la banda (`orquestacion.py:1029`, un valor inventado);
  - sesiones por horizonte `{H1: 5, …, H5: 2520}` (`sintesis.py:112`), duplicadas en lugar de salir de `horizontes`;
  - `zona_interes ±5 %` (`sintesis.py:243`);
  - umbral C6 de 0,05 cuando σ es NaN (`seguimiento.py:246`).
- **Corrección:** llevar todos estos valores a `por_defecto.yaml` con su referencia en el Anexo A, y fallar si falta el dato en lugar de usar 0,5 o 0,05.

### CA-15 · baja · Pequeños no determinismos entre ejecuciones idénticas
- **Dónde:** los Analistas corren en paralelo (`orquestacion.py:409-411`) y desde ahí se crean mensajes (`contratos.py:177`, `nuevo_id("MSG")`) y se acumulan los `participantes` del RUN en F5.
- **Qué pasa:** dos ciclos idénticos de 12 tipos producen F1–F4, F10, RC y HA idénticos. En cambio, F5 difiere en el orden de `participantes`, y la secuencia `msg_id → contrato/receptor` cambia (p. ej., `MSG-…0003` es CT-06→AG-06 en una ejecución y CT-06→AG-04 en otra). `cache_resultados.jsonl` también difiere.
- **Reproducción:** `ca_determinismo.py` y `ca_determinismo_f5.py`. Algunas diferencias son solo de ruta, porque cada ejecución usa su propia carpeta temporal.
- **Corrección:** ordenar `participantes` antes de escribir F5 y asignar los `msg_id` en el hilo principal, o derivarlos del contenido.

## Sospechas no confirmadas
- **ML-CLUS-001 rechazado** (`orquestacion.py:845-846`): cada indicador pasa a su propio clúster, lo que desactiva la diversidad y sobrestima `apuestas_independientes`, sin ninguna limitación declarada. Lo forcé (`ca_cluster_fallback.py`), pero con los datos de ejemplo no cambió el resultado: ya salían 5 apuestas de 5 opciones. Se ve el comportamiento (no hay limitación), pero no he podido mostrar el impacto.
- **Vigente con el mismo indicador y otro `tipo_opcion`** (`orquestacion.py:913, 922`): si el Analista vuelve a proponer el mismo indicador con otro `tipo_opcion`, la vigente ni se reevalúa ni se reconstruye, y sale del top-3 como «sustituida» sin haber competido. No lo he reproducido porque el mock no genera ese caso.
- **Naturaleza de la inversión** (`sintesis.py:201-205`): si la naturaleza que declara el Analista no encaja con ningún horizonte ofrecido, el ejecutor la cambia en silencio, así que C17 de HT-09 nunca ve el caso. El README lo declara, pero anula la validación que pide 8.3.

## Resultado de las pruebas actuales
`cd /home/claude/repo/bloque_a/11_Ejecutor && /home/claude/repo/.venv/bin/python -m pytest -q -p no:cacheprovider` → **58 passed in 77.07s**, igual que la línea base. Ninguna de las pruebas existentes detecta los defectos de este informe.

## Qué no he revisado o he revisado poco
- `motor/operaciones.py` y `motor/servicio.py` (fichas del Motor, caché, idempotencia, ML-CLUS-001), salvo su forma de rechazar.
- `llm.py` (clientes reales y replay), `agentes.py`, `prompts.py` y `consumo.py` (UC y presupuestos): solo los he leído por encima.
- `redaccion.py` (HTML/MD y HT-07 `ht07_legibilidad.py`), `ht02_verificador_enlaces.py`, `ht04`–`ht08`, `anonimizacion.py` y `referencias.py`: no los he revisado.
- `seguimiento.py`: solo `_revision`, `_recomendacion` y la escritura de entregables.
- Las comprobaciones C01–C16 de HT-09 (salvo C04–C07, C17 y C18) y `validar_seguimiento`.
- El rendimiento con el cliente real: no se ha ejecutado nada con la API.
