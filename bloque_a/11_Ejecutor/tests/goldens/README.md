# Goldens de los contratos CT del Bloque A (T-114, Fase 3)

Ficheros esperados que congelan el formato de los contratos CT-01 a CT-25. La suite (`tests/test_fase3_goldens.py`) vuelve a generarlos con `tests/goldens_ct.py` y los compara **byte a byte**: si cambia algo de lo que cada golden ve (tabla de abajo), una prueba falla y dice qué fichero y qué línea. Lo que ningún golden ve está en «Límites».

| Fichero | Qué congela | Cómo se obtiene |
| --- | --- | --- |
| `tablas_contratos.json` | Versión, estados, canales (V5 y V6) y campos mínimos de encargo y de retorno | Generado de `bloque_a/contratos.py` |
| `esquemas_respuestas.json` | Los esquemas JSON de las respuestas de los agentes (`ESQUEMAS`) | Generado de `bloque_a/contratos.py` |
| `mensajes_ejemplo.json` | El mensaje completo que `Mensajeria.crear` construye con cada ejemplo del Anexo B, o la clase de su rechazo | Generado con el ejecutor, reloj fijo |
| `aceptaciones_rechazos.json` | Qué hace la mensajería con cada caso de la batería: el mensaje normalizado si lo admite, o la clase y el motivo del rechazo | Generado con el ejecutor, reloj fijo |
| `formas_flujos_mock.json` | Por flujo simulado, contrato y tipo de mensaje: emisores, receptores, la ruta de cada clave (anidadas incluidas) con su tipo JSON y las combinaciones de claves opcionales | Generado con el ejecutor y `MockClient` |
| `divergencias_anexo_b.json` | Dónde difieren el Anexo B y el ejecutor (INC-T114-01) | Calculado |
| `huellas.json` | SHA-256 del Documento 0, de los esquemas publicados y de los tres ficheros escritos a mano | Calculado |
| `anexo_b_esquemas.json` | Un esquema JSON por contrato y sentido, **derivado solo del Anexo B** del Documento 0 V5.1 | Escrito a mano |
| `anexo_b_ejemplos.json` | Un ejemplo por esquema derivado | Escrito a mano |
| `bateria_mensajes.json` | La batería: mensajes válidos e inválidos por contrato, cada uno con lo que se espera de él | Escrito a mano |
| `REGISTRO.md` | Una línea por re-congelado: fecha, ficheros y motivo | Lo escribe `--update` |

## Qué ve cada golden

- **Las tablas y los esquemas de respuesta** (`tablas_contratos.json`, `esquemas_respuestas.json`): cualquier cambio en `CANALES`, `CANALES_V6`, `ANALISTAS`, `CAMPOS_MINIMOS`, `CAMPOS_RETORNO`, `CAMPO_ESTADO`, `ESTADOS`, `ESTADOS_ESPECIFICOS`, `VERSION_CONTRATO` o `ESQUEMAS`.
- **Las reglas de valor de la mensajería** (`aceptaciones_rechazos.json`). Están escritas en el código de `Mensajeria.crear` y `validar`, no en las tablas, así que se congelan por su efecto sobre la batería:
  - las listas de CT-01 (`tipo`, `prioridad`, `horizontes`) y que `alcance` sea un objeto;
  - la entrega CT-02 solo con G3 aprobado, con `entregables` y `resumen`;
  - los ocho contratos exentos de `run_id` y `query_id`, contrato a contrato;
  - los canales, en los dos sentidos, de los 25 contratos, y los del diseño V6 con V5 y con V6;
  - los tipos de mensaje y la versión;
  - los cuatro estados de retorno;
  - el estado propio de CT-23, CT-24 y CT-25: cómo pasa a su campo, qué valores admite y cuándo dos estados se contradicen;
  - los doce campos reservados del sobre, que el cuerpo no puede cambiar;
  - el `msg_id` externo del Broker en CT-01;
  - los datos protegidos (R8);
  - cada campo mínimo, uno a uno;
  - y que la mensajería no aplica las listas cerradas del Anexo B que no son suyas.
- **Lo que el ejecutor emite** (`formas_flujos_mock.json`): once flujos con `MockClient` y los doce perfiles de las pruebas.
  - `ciclo_semanal_v5`: dos ciclos semanales, con una semana entre ellos; el segundo ya lleva opciones vigentes y una lección. Con la auditoría activada, para que emita CT-16 y CT-17. Se guardan todos sus contratos.
  - `ciclo_semanal_v6`: un ciclo del diseño V6. Se guardan todos sus contratos.
  - `consulta_n0`, `consulta_que_escala` y `pregunta_repetida`: CT-03 y el aviso CT-22.
  - `peticion_ad_hoc`: CT-01 y CT-02.
  - `decision_broker`: CT-04 y CT-22.
  - `seguimiento_encargado`: CT-24 (alta, ciclo C6, pausa, reanudación, modificación, cancelación y fin por fecha), CT-05 y CT-06 del ciclo C6, y CT-22.
  - `consulta_al_broker`: CT-23 (saliente, respuesta y entrante) y CT-22.
  - `credenciales`: CT-25 (solicitud, respuesta y recordatorio).
  - `informe_de_aprendizaje`: CT-19.

  De cada tipo de mensaje se guarda la ruta de cada clave, con `x[]` para los elementos de una lista, y sus tipos JSON, en dos grupos: las que están en todos los objetos que podrían llevarlas y las que solo en algunos. Las claves que son un dato y no un formato (el código de un tipo de activo, un identificador) se escriben `<clase>` e `<id>`. Además, las combinaciones de claves opcionales de primer nivel: una por cada forma de mensaje vista.
- **Las diferencias con el Anexo B** (`divergencias_anexo_b.json`): medidas con el ejecutor, sobre los ejemplos y sobre los mensajes de los once flujos.

## Cómo se derivan los esquemas del Anexo B

- Son obligatorios los campos que el Anexo B nombra sin marcarlos como opcionales o condicionales («opcional», «solo en…», «cuando aplica»).
- Una condición del Anexo B se codifica con `if`/`then`: `seg_id` y `opp_id` de CT-05 solo con `SEGUIMIENTO`, y `contenido` de CT-23 «solo en ENTRANTE» (obligatorio en ENTRANTE y ausente en los demás).
- Las listas cerradas del Anexo B (`A|B|C`) son `enum`. Una lista abierta («admite además…», `tipo` de CT-22) no restringe: sus valores van en `examples`.
- No se añade ningún tipo, patrón ni límite que el Anexo B no diga, y los campos de más se admiten: el §6.2.3 dice que los campos son el mínimo común y que el esquema del operador puede ampliarlos.
- Cada esquema lleva en `$comment` la marca «derivado del Anexo B» y, si hace falta, la nota de lo que el Anexo B deja abierto.
- **Retornos rechazados.** El Anexo B no dice qué campos lleva un retorno con estado RECHAZADO o SIN_RESULTADO; el §6.2.6 solo pide el motivo, y en CT-09 el Anexo B prevé un retorno `RECHAZADO` con motivo `ACLARACION_REQUERIDA`. No se inventa una regla: los esquemas de retorno describen el retorno con resultado y no sirven para juzgar los otros. Lo dice el `$comment` de cada uno.
- CT-16 a CT-21 no tienen campos en el Anexo B (los remite a los prompts de sistema): de ellos se congelan el canal, la regla de `run_id` y, si un flujo los emite, su forma. De CT-22 el Anexo B solo nombra `tipo`.
- Una prueba comprueba que cada campo de cada esquema, anidados incluidos, está en el párrafo del Anexo B que habla de su contrato.

## Límites

Lo que estos goldens **no** ven. Un cambio de este tipo pasa sin que falle ninguna comparación:

- **Contratos que ningún flujo emite.** CT-07, CT-09, CT-10, CT-14, CT-18, CT-20 y CT-21 no aparecen en `formas_flujos_mock.json`:
  - CT-09, CT-10, CT-18, CT-20 y CT-21: el ejecutor no los emite por la mensajería en ningún caso (el Motor se llama como servicio);
  - CT-07 y CT-14: el ejecutor los emite, pero no con las respuestas de `MockClient` (ningún analista simulado pide una búsqueda CT-07, y el G3 simulado sale APTO a la primera). El cuerpo de CT-07 lo construye la misma función que el de CT-08, que sí se ve.

  De estos siete se congelan las tablas, el mensaje de ejemplo, el canal y la regla de `run_id`, no una forma emitida.
- **Los retornos internos (CT-06 a CT-14).** No pasan por `Mensajeria`: son la respuesta del agente, que se valida con `ESQUEMAS` (`esquemas_respuestas.json`). Aquí se congela el esquema, no una respuesta vista.
- **Los valores.** De un mensaje emitido se guardan las claves y los tipos, no los valores (salvo los de los campos con valores nombrados en el Anexo B). Un texto, una cifra o un identificador con otro formato interno (por ejemplo, otro patrón de `run_id`) no se ve.
- **Tipos y claves opcionales mezclados.** Los mensajes de un mismo flujo, contrato y tipo se resumen juntos. Si una clave anidada opcional deja de emitirse en un caso y sigue en otro, o un valor que ya era «`null|string`» deja de ser `null` en un caso y lo sigue siendo en otro, el resumen no cambia. En el primer nivel sí se ve, por las combinaciones de claves.
- **Lo que el simulador no ejercita.** Las formas son las que salen con `MockClient` y los datos sintéticos: una rama del ejecutor que el simulador no recorre (un G3 con advertencias, un presupuesto agotado, una consulta bloqueante vencida) puede emitir claves que aquí no están.
- **Reglas fuera de la mensajería.** La batería mide `Mensajeria.crear` y `validar`. Las reglas que el ejecutor aplica antes de crear el mensaje no se congelan aquí; tienen sus pruebas propias:
  - `Bloque.decision` rechaza un CT-04 vacío;
  - `Credenciales.responder` rechaza un campo de valor;
  - `ConsultasBroker.enviar` valida el tipo y el supuesto.
- **El detector de datos protegidos.** La batería prueba que un dato protegido hace rechazar el mensaje, con cuatro formas. Los patrones del detector (`RE_SECRETO`, las claves «sk-») tienen sus pruebas en otros módulos y no se congelan aquí.
- **Combinaciones que la batería no trae.** La batería es amplia, no exhaustiva: una regla nueva que solo afecte a un mensaje que ningún caso construye no cambia el golden. Quien añade una regla añade sus casos.
- **Los esquemas derivados** solo llegan al primer nivel de campos, y a un segundo donde el Anexo B trae un bloque JSON. No fijan tipos.
- **El Bloque A Forex** queda para T-115.

## Regla de re-congelado

**Re-congelar solo es deliberado.** Un golden cambia únicamente cuando se ha decidido cambiar un formato, y entonces:

1. desde `bloque_a/11_Ejecutor`: `python tests/goldens_ct.py --update --motivo "por qué cambia el formato"`. Sin motivo, termina con error y no escribe nada;
2. el golden regenerado, la línea nueva de `REGISTRO.md` y el cambio de código que lo causa van en **el mismo commit**, con el motivo también en el mensaje del commit;
3. si cambia `anexo_b_esquemas.json`, `anexo_b_ejemplos.json`, `bateria_mensajes.json`, el Documento 0 o un esquema publicado, `huellas.json` deja de coincidir: se revisa que los esquemas derivados siguen diciendo lo que dice el Anexo B, y que cada caso de la batería sigue esperando lo que debe, y se re-congela con el motivo;
4. si `aceptaciones_rechazos.json` cambia, se mira su lista `no_coinciden_con_lo_que_espera_la_bateria`: tiene que quedar vacía. Un caso que deja de coincidir es una regla que ha cambiado: o se corrige el código, o se cambia a mano lo que el caso espera.

Nunca se regenera un golden para que una prueba pase sin entender por qué falló. Es la misma regla que la del corpus (`tools/corpus_integridad.py --update`).

Para comprobar sin escribir: `python tests/goldens_ct.py` (termina con 1 si algo difiere).
