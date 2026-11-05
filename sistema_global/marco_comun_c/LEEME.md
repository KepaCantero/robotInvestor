# Marco común de C, sobres CT-G-02 y CT-G-01, K (datos de corte), Orquestador, Contradictor, consola N y control de riesgo F y ejecución G y vigilancia H y dimensionado E y comparador D y prueba de extremo a extremo y pasada de coherencia y niveles de autonomía y registro manual CT-G-14 y propuesta ligada al sobre y D con referencia y abstención y orden de entrada viva, aprobación con importe tecleado, kill-switch, cartera real y euros — V0.20 (provisional, 0.x)

Fecha: 5 de noviembre de 2026 (V0.20: E y F solo usan la cartera vigente que construye el Orquestador con la última foto que G toma del intermediario más las autorizaciones pendientes (O-29); F y E valoran en euros con los tipos de cambio de esa foto, contrastados con rangos de referencia y con el propio par (F-12, reglas F-0.2.0); cierra T-11 y T-10; V0.19: el operador autoriza con la pantalla de cifras de F y el importe tecleado (aprobación de un solo uso, ligada al contenido del informe, con caducidad, canal, segundo factor declarado y enfriamiento); kill-switch manual y automático que cancela entradas, bloquea lo nuevo, pasa todo a L1 y se rearma con la lista del §11; avisos de prioridad alta que se reiteran y escalan; cierra T-24; V0.18: la orden de entrada queda viva durante la ventana (G-11), con caducidad propia en el intermediario; estados de orden de la §4.2 anotados en el Orquestador (`orden_entrada`); `revisar_entrada` y `cancelar_entrada` en G, llamadas por H (H-11); parcial con el resto cancelado; reanudación de la protección; intentos nuevos solo tras DESHECHA; cierra T-23; V0.17: D compara cada candidato con no hacer nada (referencia de la cartera, compuesta a su horizonte) y puede abstenerse; un solo candidato se compara; confianza normalizada por el tope de la clase; escenarios SUPUESTO fuera; sensibilidad, dominancia y aspirantes; `comparar` exige incluir a todos los candidatos vigentes de la cartera (O-24) y vuelve a comparar cuando llegan nuevos; R-13 liga el horizonte del sobre al mandato; cierra T-21 y T-34; V0.16: la propuesta queda ligada al sobre (O-21), a la comparación que ejecuta el propio Orquestador con D o a la elección del operador (O-22, método `elegir`) y a la cantidad que recalcula con E (O-23); el sobre y el resultado de D entran en la cadena de hashes; cierra T-20 y T-16; V0.15: contrato CT-G-14 de ejecución manual del operador, con su validador RM-01 a RM-10, su efecto en el Orquestador y la entrada `declarar_manual` de G que lo contrasta con el intermediario; conciliación con diferencias explicadas (operaciones declaradas y tolerancia relativa); una sola posición por instrumento también en el Orquestador; cierra T-19; V0.14: decisiones del operador aplicadas: el apalancamiento pasa a ser una razón exposición/capital (1 = sin apalancar) y se puede permitir por configuración (D-12); las capas 2 y 3 son obligatorias desde N2 (D-13); niveles de autonomía L0/L1/L2 por cartera con degradación automática a L1 y cierre automático de H solo desde L2 (D-16, avanza T-18); V0.13: pasada de coherencia contra la Constitución V0.3, con un cambio mínimo de código (F, D y H ya no pueden proponer), el registro de prefijos de códigos y las deudas T-18 a T-27; V0.12 añadió la prueba de extremo a extremo de la Fase 1; V0.11 añadió D, el comparador de candidatos; V0.10 añadió E, el dimensionado de posición; V0.9 añadió H, la vigilancia de posiciones, y el cierre de posiciones en G; V0.8 añadió G, la ejecución con intermediario simulado, y su conciliación; V0.7 añadió F). Fase 1 de la Constitución V0.3.

## Contenido

| Carpeta o archivo | Para qué sirve |
| --- | --- |
| `esquemas/ct-g-02_0.1.0.schema.json` | Esquema JSON del sobre común de valoración (forma) |
| `esquemas/generar_esquema.py` | Genera el esquema; se edita aquí, no a mano en el JSON |
| `validador/validar_sobre.py` | Esquema + reglas V-01 a V-23 (código determinista, sin LLM) |
| `pruebas/generar_casos.py` | Genera 3 sobres válidos y 53 inválidos (datos simulados) |
| `pruebas/ejecutar_pruebas.py` | Ejecuta los casos del sobre CT-G-02 y comprueba la regla esperada de cada uno |
| `esquemas/ct-g-01_0.1.0.schema.json` y `esquemas/generar_esquema_encargo.py` | Esquema del encargo CT-G-01 |
| `validador/validar_encargo.py` | Reglas E-01 a E-16 del encargo y R-00 a R-10 (el sobre responde al encargo) |
| `pruebas/pruebas_encargo.py` | Genera, guarda en `pruebas/encargos/` y ejecuta los casos del encargo |
| `esquemas/k-sello_0.1.0.schema.json` y `esquemas/generar_esquema_sello.py` | Esquema del sello de corte de K |
| `validador/k_calidad.py` | K: reglas de calidad Q-01 a Q-13, emisión del sello, validación del sello (S-01 a S-13) y caducidad |
| `pruebas/pruebas_k.py` | Casos de K (sellos válidos, entradas inválidas, sellos alterados, caducidad); guarda en `pruebas/k/` |
| `validador/orquestador.py` | Orquestador: máquina de estados de expedientes y posiciones, presupuestos, idempotencia, historial encadenado por hash (códigos O-00 a O-29) |
| `esquemas/ct-g-03_0.1.0.schema.json` y `esquemas/generar_esquema_contradictor.py` | Esquema del informe del Contradictor CT-G-03 |
| `validador/validar_contradictor.py` | Reglas C-01 a C-10 del informe |
| `pruebas/pruebas_contradictor.py` | 37 comprobaciones del informe |
| `validador/control_f.py` | F: control de riesgo (reglas F-01 a F-12), informe CT-G-08 y su verificación por recálculo (CF-01 a CF-08) |
| `pruebas/pruebas_control_f.py` | 76 comprobaciones de F y de su integración en el Orquestador |
| `validador/consola.py` | N mínimo: panel verde/ámbar/rojo, cola de decisiones del operador y avisos pendientes (solo lectura) |
| `pruebas/pruebas_consola.py` | 41 comprobaciones de la consola |
| `validador/ejecucion_g.py` | G: intermediario simulado, ejecutar, deshacer, cerrar, conciliar con diferencias explicadas y `declarar_manual` (códigos G-01 a G-11; orden de entrada viva, `revisar_entrada`, `cancelar_entrada`) |
| `pruebas/pruebas_ejecucion_g.py` | 51 comprobaciones de G |
| `validador/vigilancia.py` | H: vigila posiciones y pide el cierre (reglas H-01 a H-11) |
| `pruebas/pruebas_vigilancia.py` | 41 comprobaciones de H y del cierre en G |
| `validador/dimensionado.py` | E: dimensionado de posición con los topes de F (códigos E-01 a E-04) |
| `pruebas/pruebas_dimensionado.py` | 36 comprobaciones de E |
| `validador/comparador.py` | D: comparador de candidatos por clase de comparabilidad (código D-01; decisión global INVERTIR o ABSTENERSE) |
| `pruebas/pruebas_comparador.py` | 74 comprobaciones de D |
| `pruebas/pruebas_niveles.py` | 47 comprobaciones de los niveles L0/L1/L2 y la degradación |
| `validador/manual_g.py` | CT-G-14: validador del registro de ejecución manual (reglas RM-01 a RM-10) |
| `pruebas/pruebas_cartera.py` | 43 comprobaciones de la cartera real desde G y la conversión a euros |
| `pruebas/pruebas_aprobacion.py` | 62 comprobaciones de la aprobación con importe tecleado, el kill-switch y la escalada de avisos |
| `pruebas/pruebas_entrada.py` | 54 comprobaciones de la orden de entrada viva, parciales y estados de orden |
| `pruebas/pruebas_propuesta.py` | 73 comprobaciones de la propuesta ligada al sobre, a D y a E, y de la comparación con todos (T-34) |
| `pruebas/pruebas_manual.py` | 93 comprobaciones de CT-G-14 y de la conciliación con diferencias explicadas |
| `pruebas/pruebas_extremo.py` | 42 comprobaciones del recorrido completo de la Fase 1 |
| `pruebas/pruebas_orquestador.py` | 178 comprobaciones del Orquestador (transiciones, actores, caducidad, presupuesto, reloj, integridad) |

## Registro de prefijos de códigos

Varios componentes usan prefijos parecidos; este registro evita confundirlos hasta que la Constitución fije uno propio (pasada de coherencia, hallazgo 8). El prefijo identifica la pieza, no el tipo de regla.

| Prefijo | Pieza | Notas |
| --- | --- | --- |
| `V-` | Validador del sobre CT-G-02 | V-01 a V-23 |
| `E-` (encargo) | Validador del encargo CT-G-01 | E-01 a E-16 y R-00 a R-13 |
| `E-` (dimensionado) | E, dimensionado | E-01 a E-04; colisiona con el encargo: se distingue por el módulo |
| `Q-` y `S-` | K: calidad de datos y validación del sello | no son las clases de comparabilidad Q y S |
| `C-` | Contradictor CT-G-03 | C-01 a C-10 |
| `RM-` | Registro manual CT-G-14 | RM-01 a RM-10 |
| `F-` y `CF-` | F, control y verificación del informe | |
| `G-` | G, ejecución | G-07 no se usa |
| `H-` | H, vigilancia | |
| `D-` (comparador) | D | D-01 (D-03 retirado en V0.17); colisiona con los identificadores de decisión D-01 a D-19 de la Constitución §15 |
| `O-` | Orquestador | O-00 a O-29 |

El documento explicativo es la Constitución de C: «Marco común de C y sobre CT-G-02».

## Cómo se ejecuta

```
pip install jsonschema
python3 esquemas/generar_esquema.py > esquemas/ct-g-02_0.1.0.schema.json
python3 pruebas/generar_casos.py
python3 pruebas/ejecutar_pruebas.py
python3 esquemas/generar_esquema_encargo.py > esquemas/ct-g-01_0.1.0.schema.json
python3 pruebas/pruebas_encargo.py
python3 esquemas/generar_esquema_sello.py > esquemas/k-sello_0.1.0.schema.json
python3 pruebas/pruebas_k.py
python3 esquemas/generar_esquema_contradictor.py > esquemas/ct-g-03_0.1.0.schema.json
python3 pruebas/pruebas_contradictor.py
python3 pruebas/pruebas_orquestador.py
python3 pruebas/pruebas_consola.py
python3 pruebas/pruebas_control_f.py
python3 pruebas/pruebas_ejecucion_g.py
python3 pruebas/pruebas_vigilancia.py
python3 pruebas/pruebas_dimensionado.py
python3 pruebas/pruebas_comparador.py
python3 pruebas/pruebas_niveles.py
python3 pruebas/pruebas_manual.py
python3 pruebas/pruebas_propuesta.py
python3 pruebas/pruebas_entrada.py
python3 pruebas/pruebas_aprobacion.py
python3 pruebas/pruebas_cartera.py
python3 pruebas/pruebas_extremo.py
python3 validador/validar_sobre.py sobre.json contexto.json
```

Resultado esperado de cada script de pruebas: `TODAS LAS PRUEBAS PASAN`.

## Qué está comprobado y qué no

- Comprobado de extremo a extremo (`pruebas/pruebas_extremo.py`, 42 comprobaciones, datos simulados): detección → encargo → sobre → D → E → propuesta → F → autorización → G → H → cierre, con salida por objetivo (H-02) y por stop del intermediario (H-01), decisión ajustada de D, y caída y recuperación del intermediario. Límites: D compara sobres de prueba propios (`cand()`), no los entregados al Orquestador, porque el Orquestador no guarda el sobre completo ni verifica que la comparación venga de D (T-16); el intermediario es simulado; no hay persistencia ni reloj real (T-03).

- Comprobado en D (`validador/comparador.py`, `pruebas/pruebas_comparador.py`): 74 comprobaciones; código D-01 y decisión global INVERTIR o ABSTENERSE. La referencia es no hacer nada (`referencias` por cartera en el Orquestador; valor de partida efectivo al 0 %), compuesta al horizonte medio de cada candidato; el exceso debe superar 0,10 puntos (NO_SUPERA_REFERENCIA). Puntuación = exceso / riesgo × confianza normalizada por el tope de su clase × factor de evidencia. Excluye con motivo (FORMA, DUPLICADO, EXCLUSION_DURA, CADUCADO, SIN_ESCENARIOS, SIN_RETORNO_POSITIVO, NO_SUPERA_REFERENCIA, ESCENARIOS_SUPUESTO, SIN_CONFIANZA). Un candidato solo se compara con la referencia. Sensibilidad (tres ponderaciones alternativas) y empates dan AJUSTADA y una lista de aspirantes, entre los que elige el operador; cada candidato lista quién lo domina y, ante empate, el no dominado va primero. Con varias clases no hay ganador único. Límites: la puntuación no normaliza horizontes ni descuenta costes (T-17); la rentabilidad de la referencia es de configuración, no de K; todos los umbrales [PROPUESTO].

- Comprobado en E (`validador/dimensionado.py`): 36 comprobaciones, incluida una prueba de 400 casos aleatorios en la que F aprueba siempre lo que E propone y el riesgo nunca supera el objetivo. Códigos OK, E-01..E-04. Límites: precios en euros sin conversión de divisa ni comisiones (T-10); no hay tabla de pasos por instrumento; un salto de precio puede superar la pérdida del stop.

- Comprobado en H (`validador/vigilancia.py`) y en el cierre de G (`cerrar`): 41 comprobaciones con intermediario simulado; reglas H-01 a H-09. H aplica solo condiciones de salida ya declaradas, no cierra con un precio ausente o viejo (avisa) y el cierre lleva a cero la posición neta real del intermediario antes de pasar a CERRADA. Límites: solo cierre total (la reducción parcial sigue pendiente, T-12); solo condiciones sobre el precio; H no tiene reloj propio; el cierre a mercado no es de solo reducción en el simulador; umbrales de 15 min y 72 h [PROPUESTO].

- Comprobado en G (`validador/ejecucion_g.py`): 51 comprobaciones con un intermediario simulado; códigos OK, G-01..G-06 y G-08 a G-10 (G-07 no se usa; G-10: lo declarado a mano no cuadra con el intermediario). Tras enviar órdenes, cualquier fallo se trata como estado incierto (G-08) con aviso, nunca como «sin efectos»; una posición sin stop se cierra o se alerta. `conciliar` compara Orquestador e intermediario (cantidad, sentido, activo, stop, stop huérfano). Límites: una posición por instrumento; no hay reducir/cerrar posiciones ni redimensionar el stop; sin conversión de divisa; el disparo del stop no se simula; el intermediario es simulado y los actores no se autentican (ver deuda técnica).

- Comprobado en CT-G-01: 4 encargos válidos, 46 inválidos y 21 comprobaciones de respuesta; el cruce valida antes ambos mensajes y contrasta con el sello de K (E-16, R-11, R-12).
- Comprobado en la cartera y la divisa (`pruebas/pruebas_cartera.py`, 43 comprobaciones): G toma la foto del intermediario (`foto_cartera`, posiciones en euros y tipos de cambio) y la registra (`registrar_cartera`: solo G, cuenta configurada, frescura, nunca anterior a la última, tipos dentro de su rango de referencia). `cartera_f()` es la única cartera válida para E y F: la última foto más las autorizaciones pendientes; otra cualquiera da O-29, y en un par con el euro el tipo debe cuadrar con el precio. F (reglas F-0.2.0) y E convierten riesgo, tamaño, exposición, concentración y valor mínimo a euros; sin tipo de cambio F veta (F-12). La divisa de cotización sale de pares de divisas ISO (activo base = primera divisa) o de la tabla `divisas_cotizacion`. Las pruebas antiguas usan un tipo neutro (1 USD = 1 EUR). Límites: el actor G es declarado (T-01); tipos contrastados con rangos fijos, no con una segunda fuente (T-42); rangos y cuenta [PROPUESTO] (D-21).
- Comprobado en la aprobación y el kill-switch (`pruebas/pruebas_aprobacion.py`, 62 comprobaciones): `pantalla_aprobacion` (solo el operador) da las cifras de F con hash, caducidad (15 min) y enfriamiento (30 min con pérdida del día o fuera de horario); `autorizar(..., aprobacion)` exige ese hash, el importe tecleado al céntimo, canal admitido y segundo factor (O-27, O-28, O-05), de un solo uso y ligada al contenido del informe; todo el control de F autorizado entra en la cadena de hashes. `activar_kill_switch` (operador, Orquestador, vigilante) y `kill_switch` de G: bloquean autorizaciones y entradas nuevas (O-26), pasan todo a L1, cancelan las entradas vivas y no tocan protecciones; lo disparan una discrepancia sin explicar, una integridad rota o un identificador repetido con otro contenido. `rearmar_kill_switch` exige la lista del §11, avisos altos acusados, ninguna entrada viva y una conciliación limpia posterior; las carteras siguen en L1 24 h y lo autorizado antes del kill hay que aprobarlo de nuevo. Los avisos altos se reiteran cada 15 min y escalan a la tercera por un canal propio. Límites: canal, segundo factor y lista de rehabilitación declarados (T-01); vigilante con latido y cortacircuito global pendientes (T-40); envío real de avisos (T-41); importe en la divisa de cotización (T-10).
- Comprobado en la orden de entrada (`pruebas/pruebas_entrada.py`, 54 comprobaciones): G anota la orden ENVIADA antes de enviarla, la deja viva (G-11) hasta el fin de la ventana, del sobre o del informe de F (y con `valida_hasta` en el intermediario), y en cada pasada H la revisa (H-11): ejecutada, la protege y reporta con el instante de ejecución (CONCILIADA); vencida, degradada o cancelada a petición, la cancela (CANCELADA); perdida, RECHAZADA. Un parcial cancela el resto. Si falla la protección tras ejecutarse, la revisión la reanuda. Tras deshacer una ejecución, G anota DESHECHA y solo entonces admite otro intento, siempre con ids nuevos. `barrer`, `descartar` y CT-G-14 respetan la orden viva (O-25); la conciliación explica ENTRADA_EN_CURSO y detecta ENTRADA_HUERFANA. Límites: sin órdenes bracket ni OCO, hay un hueco sin stop entre la ejecución y la revisión (T-38); la hora de ejecución la da el intermediario (T-39); el resto de un parcial solo se cancela.
- Comprobado en la propuesta (`pruebas/pruebas_propuesta.py`, 73 comprobaciones): `proponer(..., dimensionado)` exige que la propuesta coincida con el sobre guardado (instrumento normalizado, activo base = divisa base, dirección, stop de precio igual o más prudente, objetivo no más ambicioso, invalidez del sobre presente con su unidad, apalancamiento, ventana y cartera; O-21), que el expediente sea el ganador de D o el elegido por el operador (O-22; `comparar` ejecuta D sobre los sobres y `elegir` solo admite sin par, duplicado o empatados en una decisión ajustada) y que la cantidad no supere la que el Orquestador recalcula con E (O-23); al autorizar, F debe usar el mismo capital que E. Límites: un candidato que pasa a EN_OBSERVACION antes de comparar no cuenta (T-36); la vía de acceso y la fecha de salida no se ligan (T-35); la cartera de E y F sigue llegando de quien llama (T-11).
- Comprobado en CT-G-14 (`pruebas/pruebas_manual.py`, 93 comprobaciones): el operador declara lo que hizo a mano; vinculado a un expediente AUTORIZADA abre su posición con los mismos controles que G (ventana, sello, F recalculado, cantidad aprobada, precio), vinculado a una posición la cierra (solo total) y LIBRE queda registrado con aviso O-20. `declarar_manual` de G contrasta orden, cantidad, precio y stop con el intermediario, cancela el stop al cerrar y rechaza con G-10 lo que no cuadra. La conciliación calcula por instrumento la cantidad esperada con signo; lo declarado LIBRE (solo en instrumentos sin posición del sistema, RM-10) y las diferencias dentro de la tolerancia relativa (`tolerancia_conciliacion_rel`, máximo 1 %) son diferencias explicadas que no avisan ni degradan. Límites: sin conciliación de efectivo (T-31); `registrar_manual` llamado directamente no contrasta con el intermediario (T-32); las LIBRES no tienen tope ni pasan por F (T-33); ventana de declaración de 72 h [PROPUESTO].
- Comprobado en los niveles de autonomía (`pruebas/pruebas_niveles.py`, 47 comprobaciones): configuración `nivel_autonomia` por cartera (L0 y L1 se tratan igual en las decisiones: el operador confirma; L0 no impide ni simula nada por sí mismo, la simulación depende del adaptador del intermediario (T-30), L2 automático con límites; sin dato, L1). La autorización por la matriz y el cierre automático de G/H exigen L2; en L0/L1 H registra «CIERRE PREPARADO» (H-10) y el operador cierra con motivo. Una discrepancia de conciliación (incluye G-08) o un dato viejo degradan a L1 (aviso O-19); solo el operador restablece, con los avisos acusados. Un stop que el intermediario ya ejecutó se concilia en cualquier nivel: el Orquestador exige que la condición sea un STOP declarado y que la orden citada sea una de las protecciones de la posición, y solo para CERRANDO. H concilia antes de decidir cierres automáticos, y una autorización automática no se ejecuta si la cartera se degradó. Límites: que ese stop se ejecutó lo afirma G y el Orquestador no lo verifica (T-28); la prueba de G-08 llama a `_incierto` directamente; la degradación por discrepancia baja todas las carteras con nivel superior a L1; no hay degradación por sello caducado (T-29); L3 no existe; todos los umbrales [PROPUESTO].
- Comprobado en el Orquestador: 178 comprobaciones con datos simulados; códigos O-00 a O-18 (O-17: objeción del Contradictor; O-18: discrepancia de conciliación). Límites: la cadena de hashes del historial detecta alteración pero no está anclada fuera (use `cabezas()` y un registro de solo añadir); no hay reloj real ni persistencia; el Contradictor (CT-G-03) no se exige por defecto y su independencia es declarada, no comprobada; las condiciones de reapertura de `observar` no se verifican solas; el resultado de F no se verifica de forma independiente; todos los umbrales son [PROPUESTO].
- Comprobado en K: 7 sellos válidos, 82 entradas inválidas, 38 comprobaciones del sello y 16 de caducidad. Datos simulados; no hay proveedor de datos elegido.
- Límites de K: `hash_sello` detecta alteración pero no es una firma; la inmutabilidad real exige un registro de solo añadir. Q-10 no compara valores; `sello_id` no es único por sí mismo.
- Comprobado: el esquema valida, el validador acepta los 3 sobres válidos y rechaza cada
  uno de los 53 inválidos por la regla que rompe.
- No comprobado: ningún sobre real. Los datos de prueba son simulados. Falta pasar un
  sobre real de `C-DIV` (pendiente de que se comparta su desarrollo) y de `C-RV` (Fase 2).
- Valores de partida (no ratificados): topes de confianza Q 0,80, S 0,60, K 0,40; factor
  0,75 si el doble análisis discrepa; los seis episodios de estrés y los ocho factores.
- El esquema sigue en `0.x`: admite cambios compatibles. Se congela en `1.0.0` tras dos
  perfiles reales y su consumo por D.
