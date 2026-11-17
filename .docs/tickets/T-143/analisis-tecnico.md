# T-143 · Análisis técnico

## Causa raíz o motivo

El Documento 0 del Bloque A se escribió antes de construir el ejecutor, y su Anexo B no pide lo mismo que el código (INC-T114-01, medido por los goldens de T-114). El operador decidió el 13-11-2026 que manda el código y autorizó el 15-11-2026 la nueva entrega con el Anexo B corregido según el borrador (`.docs/diseno/bloque_a/borrador_correccion_anexo_b.md`).

## Evidencia

- Antes: `bloque_a/11_Ejecutor/tests/goldens/divergencias_anexo_b.json` congelaba 23 contratos y sentidos con diferencias por contrato, 14 con mensajes de los flujos simulados que no cumplían el Anexo B, 4 con valores en otro campo y 6 contratos sin campos (CT-16 a CT-21). Copia: `.docs/diseno/bloque_a/divergencias_anexo_b_v51.json`.
- Después: el mismo golden, regenerado contra la V5.2, solo tiene `contratos_sin_campos_en_el_anexo_b: [CT-18, CT-20, CT-21]`; las otras tres secciones están vacías.
- `aceptaciones_rechazos.json` sale byte a byte igual (`cmp` con la copia previa): la batería mide lo mismo.

Reproducir: desde `bloque_a/11_Ejecutor`, `../../.venv/bin/python tests/goldens_ct.py` (0 si coinciden) y `../../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_fase3_goldens.py`.

## Implementación

### Archivos

- `bloque_a/99_Historico_V5.2/01_Gobernanza/Documento 0 - Protocolo maestro del Bloque A - Versión óptima V5.2.md` (en `01_Gobernanza` hasta T-166, que la pasó al histórico) (nuevo, corpus): copia de la V5.1 con la cabecera de versión (título, fecha, «Sustituye a», «Actualizado»), el Anexo B reescrito hasta el esquema `informe_seguimiento_opcion` (que no cambia, como tampoco `paquete_oportunidades`) y una fila nueva en el Anexo F. Nada más: lo comprueba `test_t143_la_v52_es_la_v51_con_el_anexo_b_corregido`.
- `bloque_a/99_Historico_V5.1/01_Gobernanza/` (nuevo, corpus): la V5.1 `.md` y `.docx` movidas con `git mv`, con los mismos SHA-256 que tenían en el manifiesto.
- `bloque_a/README - Índice de la entrega y registro de la actualización V5.1.md` (corpus): fila de `01_Gobernanza` (Documento 0 V5.2), fila nueva `99_Historico_V5.1` en el inventario y entrada del registro (§8). No se renombra (ver decisiones). Su `.docx` no se toca.
- Goldens (`bloque_a/11_Ejecutor/tests/goldens/`): `anexo_b_esquemas.json` y `anexo_b_ejemplos.json` derivados del Anexo B V5.2 (con un script de una vez, abajo); `bateria_mensajes.json`: los 86 casos cuyo ejemplo cambió llevan el cuerpo V5.1 dentro del caso (`cuerpo`, `contrato`, `tipo_mensaje` en vez de `base`), y los tres casos «ejemplo_del_anexo_b_suelto» dicen en `que` que son el ejemplo V5.1; re-congelados con `goldens_ct.py --update --motivo` dos veces, cada una con su línea en `REGISTRO.md`: la primera (`divergencias_anexo_b.json`, `formas_flujos_mock.json`, `huellas.json`, `mensajes_ejemplo.json`) por el Anexo B V5.2; la segunda (solo `huellas.json`) por una corrección de redacción del propio Anexo B («salvo `estado` y `autoevaluacion`» en vez de «además de»), hecha tras la suite completa; `README.md` al día.
- `bloque_a/11_Ejecutor/tests/test_fase3_goldens.py`: pruebas actualizadas y pruebas nuevas `test_t143_*` (ver `pruebas.md`). `goldens_ct.py` no cambia: busca el Documento 0 con `glob("Documento 0*.md")` en `01_Gobernanza`.
- Referencias: `prompts/FASE0_VERIFICADOR_IDS.md` y `prompts/FASE3_GOLDENS_CONTRATOS.md` (la ruta), `bloque_a/11_Ejecutor/README.md` y `tests/MAPA_PLAN_DE_PRUEBAS.md` («Subordinado al Documento 0 óptima V5.2»), y la primera línea del docstring de `bloque_a/11_Ejecutor/bloque_a/contratos.py` (cita el Anexo B que cambió). Ningún cambio de código ejecutable.
- `.docs/scripts/borrador_anexo_b.py` y el borrador: ver «Borrador».
- `docs/incidencias.md`: ronda T-143 en INC-T114-01 e INC-T143-01 (la V5.2 no tiene `.docx`). `sistema_global/seguimiento/Decisiones_del_operador_Bloque_A.md`: la fila «Nueva entrega del Documento 0», «Aplicada en la V5.2».
- `tools/corpus_manifest.txt`: re-congelado (ver «Corpus»).

### Decisiones y desviaciones del plan

- **Versión V5.2.** Cambia el texto de un anexo, no la topología, las reglas ni los formatos: sube un menor. `version_contrato` sigue en «5.1» (lo dice el Anexo B y lo comprueba una prueba): la V5.2 es del documento, no de los contratos.
- **Ubicación.** Como `99_Historico_V3.0`: `bloque_a/99_Historico_V5.1/01_Gobernanza/`. En `01_Gobernanza` queda un solo Documento 0; `test_t142_cadena_b.py` exige uno solo y `goldens_ct.py`, `test_t126_pb26_pb48.py` y `test_fase3_goldens.py` lo buscan por `glob`, así que leen la V5.2 sin cambiar código.
- **README índice.** No se renombra: su nombre es el de la entrega del bloque (V5.1), que no cambia; solo el Documento 0 sube a V5.2. Es parte del corpus, pero es el índice que CLAUDE.md manda leer primero, así que lleva la fila del registro; entra en el re-congelado (es la tercera entrada del diff del manifiesto, además de las de los ficheros movidos y el nuevo).
- **Sin `.docx`.** Los `.docx` son copias de consulta que no se editan ni se generan aquí: INC-T143-01.
- **CLAUDE.md no se toca.** No cita el Documento 0 V5.1 por nombre ni ruta (la tabla dice «V5.1» de la entrega, que sigue siendo cierto). Dice «695 archivos» del corpus, que ahora son 696: lo señalo para la sesión coordinadora; no lo cambio.
- **Citas a la V5.1 que se quedan.** Las del corpus congelado (system prompts, funciones, archivos operativos, plantillas y demás: «Documento 0 óptima V5.1» en 60 sitios), el Documento 0 del Bloque B («Anexo B del Documento 0 del Bloque A V5.1»), los tickets cerrados y la memoria (`.docs/memoria/compartida/2026-11-09_revision-bloque-a.md`), y las del código que fechan en qué versión entró algo (`interfaz_broker.py`, `seguimiento.py`, `configuracion.py`, `evaluador.py`, `ht08_monitor.py`, `ht01_boveda.py`, `tests/test_v51.py`, `config/por_defecto.yaml`). `herramientas/referencia/ht09_validador_g3.py` es idéntico a su copia del corpus (`10_Herramientas`) y no se toca.
- **Campos que el ejecutor no exige → «opcional» o «si aplica»**, como manda el operador; ningún cambio de código.
- **CT-22**: dos campos documentados como están; los §7.6 y §7.9 no se tocan (fuera del Anexo B) y el Anexo B dice que su «tipo» es uno u otro campo según el valor. El esquema derivado lo codifica con `oneOf`.
- **Fases de CT-06**: además de las dos del borrador, REVISION_VIGENTES (el ejecutor la emite en N0 y N1: `orquestacion.py`; el golden no la nombraba porque el error de `enum` es el mismo para cualquier valor). Las de la V5.1 se conservan.
- **Lotes**: el borrador listaba como «campos de hoy» los nombres de la V5.1; el ejecutor envía otros (`orquestacion.py`, `diseno_v6.py`). El Anexo B V5.2 describe los que se envían.
- **Retornos internos y del Motor**: el borrador pedía describirlos con los esquemas de `ESQUEMAS` y con lo que sirve el Motor; se hace con una frase fija que una prueba compara con el código, y con las claves medidas en el Motor.
- **CT-16, CT-17 y CT-19**: se dan los campos de lo que el ejecutor emite (propuesta del borrador). Como la mensajería no los exige, sus esquemas derivados no exigen ningún campo de primer nivel; sí los anidados que siempre van.
- **Regla de derivación**: «la mensajería no lo exige» cuenta como opcional (README de los goldens).
- **Batería**: no se reescribe ningún caso; los que partían de un ejemplo cambiado llevan el cuerpo V5.1 dentro. El golden de aceptaciones no cambia.

### Qué cambió en el Anexo B, divergencia a divergencia

| Divergencia (V5.1) | Cambio en el Anexo B V5.2 | Contra la V5.2 |
| --- | --- | --- |
| CT-01.ENCARGO admite que falte `fecha_objetivo`, `nivel_forzado`, `referencia_previa` | Opcionales; se dicen los cuatro que exige la mensajería | desaparece |
| CT-03.ENCARGO admite que falte `contexto`, `urgencia`; los mensajes no llevan `query_id`, `contexto.run_id`, `contexto.opp_id` | `query_id` lo asigna el bloque; `contexto` y `urgencia` opcionales; `contexto.*` si aplica | desaparece |
| CT-03.RETORNO admite que falte `escalado`; llega nulo | `escalado` opcional: nulo en N0, objeto con `run_id`, `plazo_estimado`, `nivel`, `clases`, `estado_run`, `respuesta_provisional` si escala; el JSON lo pone nulo | desaparece |
| CT-04.ENCARGO admite que falten los cuatro bloques; `configuracion` incompleta | Los cuatro opcionales (un CT-04 vacío se rechaza); `configuracion` lleva solo lo que cambia; INC-T116-01: `horizontes` es global y se rechaza cada celda «No» | desaparece |
| CT-06.ENCARGO `fase` fuera de la lista | Se añaden CRIBADO_E_INVESTIGACION, REVISION_VIGENTES y RESPUESTA_OBJECIONES, con cuándo se emite cada una | desaparece |
| CT-06, CT-07, CT-08, CT-11, CT-12, CT-13 y CT-14 RETORNO admiten que falten sus campos | Respuesta del agente con su esquema de `ESQUEMAS` (INFORME_CLASE, REVISION_VIGENTES, RESPUESTA_OBJECIONES, BUSQUEDA, CURACION, PROSPECTIVA, REFUTACION, CONTRARREPLICA, DICTAMEN_G3): qué exige y qué admite; lo que no devuelve el agente (EVD-, CLM-, duplicados, raíces, independencia; SEGUIMIENTO sin informe) | desaparecen |
| CT-09.RETORNO y CT-10.RETORNO admiten que falten sus campos | Claves de `Motor.servir` (servido, caché y rechazo; la incertidumbre queda en RC) y de `Motor.reejecutar`; `clase_cifra` DETERMINISTA o ESTADISTICA; `coincide` SI, DENTRO_TOLERANCIA o NO, con `categoria` | desaparecen |
| CT-09 `fecha_corte` solo en evaluaciones | Obligatoria siempre (el ejecutor es más estricto); la aclaración, con ACLARACION_REQUERIDA en el `detalle` | no era divergencia medida; corregido |
| CT-11, CT-12 y CT-13 ENCARGO: el ejecutor exige la lista y rechaza el ejemplo | Lotes `piezas`, `encargos` y `peticiones` (y `contrarreplicas` en CT-13) con los campos que se envían | desaparecen |
| CT-11 `independiente` y claves de `fechas` abiertas | `independiente` sale (no lo devuelve el Curador; `grado_independencia` en F2); `fechas` con `fenomeno`, `publicacion`, `recuperacion`, `conocible_desde`, opcional | resuelto |
| CT-22 `tipo` exigido; CONSULTA_RECURRENTE y DECISION_SEGUIMIENTO en `tipo_aviso` | `tipo` (DECISIONES_BROKER, PREGUNTA_REPETIDA) o `tipo_aviso` (CONSULTA_RECURRENTE, DECISION_SEGUIMIENTO), uno de los dos | desaparece |
| CT-23.ENCARGO admite que falten `plazo_respuesta`, `preguntas`, `punto_control`, `seg_id`; preguntas sin `origen`, etc.; sin `run_id` | Opcionales; cada pregunta, `texto` y `supuesto_declarado`, lo demás si aplica | desaparece |
| CT-23, CT-24 y CT-25 RETORNO: estado del objeto en `estado` | `estado_consulta` (con RECIBIDA), `estado_seguimiento`, `estado_credencial`; `estado` es el común; la mensajería pasa `estado` al campo propio | desaparece |
| CT-23.RETORNO admite que falten `respuestas`, `supuestos_aplicados`; sin `documentos` | Opcionales | desaparece |
| CT-24.ENCARGO admite que falte todo salvo `accion`; CT-24.RETORNO sin `proximo_ciclo` | Opcionales | desaparece |
| CT-25 admite que falten `herramienta`, `urgencia`, `credencial_ref`, `caducidad` | Opcionales (recordatorio y DENEGADA) | desaparece |
| Retornos RECHAZADO o SIN_RESULTADO sin regla | Estado común y motivo; la mensajería exige igualmente los campos de retorno de su contrato (CT-03, CT-23 a CT-25) y la entrega completa en CT-02 | dicho |
| Listas cerradas que la mensajería no aplica | Se dice cuáles comprueba la mensajería (CT-01, CT-02, estado común y propio) y que las demás y `contenido` de CT-23 no | dicho (la batería lo sigue congelando) |
| CT-16 a CT-21 sin campos | CT-16, CT-17 y CT-19 con los campos de lo que se emite | quedan CT-18, CT-20 y CT-21 |

### Lo que queda

- `contratos_sin_campos_en_el_anexo_b`: CT-18, CT-20 y CT-21. El Anexo B los sigue remitiendo a los prompts de sistema (datos de ejecución, regla 1) y ningún flujo simulado los emite: no hay nada medido que describir.
- INC-T114-02: el ejemplo publicado del informe de seguimiento sigue sin cumplir su esquema por `x_aviso_ejemplo`; está en `06_Plantillas_entregables`, fuera del Documento 0 y de esta tarea.
- Lo que no mide ningún golden: los campos anidados que el Anexo B V5.2 describe en prosa en los retornos internos (finalistas, resultados de prospectiva, objeciones…) y los de CT-17 y CT-19 que no emite ningún flujo (la respuesta del Auditor; el CT-19 de fiabilidad de fuentes).
- Opciones que siguen abiertas sin ser diferencias: unificar `tipo` y `tipo_aviso` de CT-22, o validar las listas cerradas en la mensajería (cambios de formato).

### Corpus

`.venv/bin/python tools/corpus_integridad.py --update` (695 → 696 archivos). Diff del manifiesto (`git diff -U0 tools/corpus_manifest.txt`): 7 líneas, 3 quitadas y 4 puestas, que son 6 rutas:

- quitadas: `bloque_a/01_Gobernanza/…V5.1.docx` y `…V5.1.md` (se mueven);
- puestas: `bloque_a/99_Historico_V5.1/01_Gobernanza/…V5.1.docx` y `…V5.1.md`, con los mismos hashes (`26691b68…` y `7e708a03…`); `bloque_a/01_Gobernanza/…V5.2.md` (nueva, `0695971f…`);
- modificada: `bloque_a/README - Índice de la entrega y registro de la actualización V5.1.md` (`70f6b0de…` → `e25d7eb7…`).

Ninguna otra entrada cambia.

**Texto del motivo para el commit (lo hace la sesión coordinadora):**

> docs: Bloque A, T-143 (Documento 0 V5.2: la V5.1 con el Anexo B corregido para que describa lo que hace el ejecutor, por la decisión del operador del 13-11-2026 «manda el código» y la nueva entrega autorizada el 15-11-2026; la V5.1 .md y .docx pasa sin cambios a bloque_a/99_Historico_V5.1/01_Gobernanza; re-congelado del corpus con tools/corpus_integridad.py --update por ese motivo: solo cambian las dos rutas movidas, la V5.2 nueva y el README índice del bloque, que lleva la entrada del registro; goldens de contratos re-congelados con goldens_ct.py --update --motivo, divergencias_anexo_b.json sin diferencias medidas; la V5.2 no tiene .docx, INC-T143-01) [pendiente QA]

### Borrador

`.docs/diseno/bloque_a/borrador_correccion_anexo_b.md` no pierde texto: dice primero «Estado: aplicado en el Documento 0 V5.2» y «Lo que queda contra la V5.2» (generado del golden de hoy y de una lista fija `QUEDA` en el script), y debajo conserva el borrador aplicado, regenerado con la copia de las diferencias V5.1 (`.docs/diseno/bloque_a/divergencias_anexo_b_v51.json`, idéntica al golden de `HEAD`). Del texto anterior solo cambian los niveles de título (`##` → `###`) y la línea de estado, que se conserva citada («Estado hasta T-143: …»). Si apareciera una diferencia nueva contra la V5.2, el script la pondría en «Lo que queda», con la misma tabla. `--comprobar` pasa.

### Script de una vez (no se guarda en `.docs/scripts/`: no se repite)

`t143_derivar.py`, ejecutado desde `bloque_a/11_Ejecutor`: a partir de los esquemas y ejemplos V5.1 escribe los V5.2 (cada cambio de la tabla de arriba) y pasa a `cuerpo` los casos de la batería cuyo `base` cambió. Después, a mano, el `$comment` de CT-09.RETORNO con ACLARACION_REQUERIDA y el `que` de los tres casos «ejemplo_del_anexo_b_suelto».

### Límites conocidos

- Las afirmaciones del Anexo B V5.2 que no comparan las pruebas (los anidados en prosa, «un CT-04 vacío se rechaza», «la revisión de SEGUIMIENTO la calcula el ejecutor») salen de leer el código (`orquestacion.py`, `diseno_v6.py`, `seguimiento.py`, `motor/servicio.py`, `contratos.py`, el README de los goldens).
- La frase fija «con `CLAVE`, que exige …; admite además …» es la que la prueba sabe leer: un cambio de redacción del Anexo B que la rompa hace fallar la prueba (falla cerrado).
- `_en_otro_campo` compara valores de texto: en CT-23 a CT-25, un estado común PARCIAL coincide con el valor PARCIAL de `estado_consulta`; hoy ningún flujo lo emite así, pero si lo hiciera saldría como diferencia (falso positivo, no un hueco).

### Comandos para probarlo

```bash
cd bloque_a/11_Ejecutor
../../.venv/bin/python tests/goldens_ct.py
../../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_fase3_goldens.py
cd ../..
.venv/bin/python .docs/scripts/borrador_anexo_b.py --comprobar
.venv/bin/python tools/corpus_integridad.py && .venv/bin/python tools/refs_vivas.py
git diff -U0 tools/corpus_manifest.txt
```

## Ronda r02 (QA r01 NO APTO)

### Qué cambia en el Anexo B V5.2, hallazgo a hallazgo

| Hallazgo | Código que manda | Texto nuevo |
| --- | --- | --- |
| H-01 | `Bloque.decision` (`orquestacion.py`) acepta cinco bloques y rechaza el CT-04 sin ninguno; `aprobar_certificados` llega a `Evaluador.aprobar_certificados` | Los cinco bloques, con `aprobar_certificados` (lista de CERT-, PA-10), opcionales; «un CT-04 sin ninguno de los cinco se rechaza». Esquema derivado con la propiedad nueva (el ejemplo no cambia: la batería sigue igual) |
| H-02 | `_invocar("AG-17", "CT-15", …, "REDACCION")` y, en V6, `("AG-26", …, "SINTESIS")` | CT-15: «El Redactor responde con `REDACCION`, que exige …» y «el Sintetizador responde con `SINTESIS`, que exige …; admite además …», con `tarjetas` y `glosario`; los entregables y sus rutas los escribe el ejecutor. Esquema derivado y ejemplo nuevos de CT-15.RETORNO |
| H-03 (a) | `consulta(ejecutar_escalado=False)`: `escalado` sin `estado_run` y con `run_id` nulo | «`estado_run` solo si se ejecutó el análisis; si no se ejecutó (`consulta --sin-escalado`), `run_id` es nulo»; el derivado ya no exige `estado_run` |
| H-03 (b)–(d) | `INFORME_CLASE`, `REVISION_VIGENTES`, `RESPUESTA_OBJECIONES`, `FINALISTA`, `BUSQUEDA`, `CURACION`, `PROSPECTIVA`, `REFUTACION`, `CONTRARREPLICA` | Cada campo anidado, con la frase fija «En `CLAVE`, cada elemento de `campo` lleva …; admite además …» y los valores de sus listas: `cribado` lleva `candidata`, `paso_gc1` y `motivo` (no «la señal»); `finalistas`, los 22 campos obligatorios de `FINALISTA` (con `dimensiones`, no puntuaciones; sin cálculos); `evidencia_citada` es «admite además». Las referencias de `BUSQUEDA` solo exigen `ref_id` (la V5.2 de la r01 decía «con Q y nivel») |
| H-03, otros iguales | `_integrar` invoca a AG-02 por CT-05 con el esquema `INTEGRACION` y el tipo INTEGRACION; ningún código lee `SOLICITUD_PRESUPUESTO`, `consultas_broker` ni `solicitudes_credenciales` de un retorno; `alcance` de CT-01 se toma con `or {}` y, sin `clases`, el ciclo usa los tipos activos | CT-05: tipo INTEGRACION (con `insumos_integracion`, solo en ella), retorno con `INTEGRACION`, retorno parcial opcional y no leído (INC-T116-03). CT-01: dentro de `alcance`, todo es opcional |
| H-04 | `CAMPOS_MINIMOS["CT-09"]` exige `fecha_corte`; `Motor.servir` usa la del proveedor si falta | «la exige la mensajería, y si una petición llega al Motor sin ella, el Motor usa la fecha del proveedor de datos y, si este no la tiene, sirve sin fecha de corte» |
| H-06 | — | `config/por_defecto.yaml`, línea 2: «subordinado al Documento 0 óptima V5.2 (15/11/2026)» |

De paso, la introducción del anexo cuenta CT-05 y CT-15 entre los retornos internos y describe la frase de los anidados; los estados propios de CT-23 a CT-25 dicen «como pide el 6.2.6» en vez de «(6.2.6)», para que un paréntesis tras un campo sea solo su lista de valores.

### CLAUDE.md (H-06, segunda parte): no se cambia

La sesión coordinadora transmite que el operador aprobó cambiar «695 archivos» por «696 archivos» en la línea 118 de `CLAUDE.md`. No lo hago: la aprobación me llega en un mensaje de otro agente, no del operador, y `CLAUDE.md` (las instrucciones del proyecto) solo lo cambio con la aprobación del operador en su propia sesión. Es un cambio de una cifra en una tabla y no lo comprueba ningún gate; queda para que lo haga la sesión coordinadora o el operador.

### Pruebas nuevas (H-05)

- `_esquemas_de_respuesta_que_difieren` llega a CT-05 y CT-15, a los campos anidados (cada objeto o lista de objetos del esquema de respuesta tiene que estar descrito, y con los campos que exige y admite) y a los valores de las listas cerradas (la prosa tiene que dar los de cada campo con `enum`, y los mismos), en los dos sentidos: 11 mutantes en `test_t143_r02_un_cambio_en_los_valores_o_en_los_anidados_se_nota` (C02 y D06 del revisor entre ellos).
- `test_t143_r02_las_listas_de_la_prosa_son_las_del_esquema_derivado`: cada `enum` de un esquema derivado tiene en el párrafo los mismos valores (bloque JSON o paréntesis); 4 mutantes (D05, D10 entre ellos).
- `test_t143_r02_lo_que_el_derivado_no_exige_la_prosa_lo_marca_opcional`: cada campo de primer nivel que el derivado no exige está en una frase con una marca de opcional; 4 mutantes (D03, D04 entre ellos).
- `test_t143_r02_cada_fase_de_ct06_se_emite_cuando_dice_el_anexo_b`: los CT-06 de los flujos simulados siguen la regla del Anexo B, emiten las cuatro fases y un cambio como el C07 la rompe.
- `test_t143_r02_ct04_…`, `…_ct03_…` y `…_ct09_…`: las afirmaciones de H-01, H-03 (a) y H-04, medidas con el Bloque y el Motor.

### Re-congelado de la r02

- Goldens: `goldens_ct.py --update --motivo "T-143 r02 (QA r01 NO APTO, H-01 a H-04): …"`, una sola línea en `REGISTRO.md` (`huellas.json` y `mensajes_ejemplo.json`). `divergencias_anexo_b.json`, `aceptaciones_rechazos.json` y `formas_flujos_mock.json` no cambian.
- Corpus: `tools/corpus_integridad.py --update`. Frente a la r01 solo cambia la línea de la V5.2 (`0695971f…` → `ca5ab7dd…`). Frente a `1ccffd5`, el diff sigue teniendo las mismas 6 rutas (3 líneas quitadas y 4 puestas): las dos V5.1 de `01_Gobernanza` quitadas, las dos del histórico con los mismos hashes (`26691b68…`, `7e708a03…`), la V5.2 (`ca5ab7dd…`) y el README índice (`70f6b0de…` → `e25d7eb7…`).

**Texto del motivo para el commit (sustituye al de la r01):**

> docs: Bloque A, T-143 (Documento 0 V5.2: la V5.1 con el Anexo B corregido para que describa lo que hace el ejecutor, por la decisión del operador del 13-11-2026 «manda el código» y la nueva entrega autorizada el 15-11-2026; ronda r02 tras la QA r01: CT-04 con aprobar_certificados, retornos de CT-05 y CT-15 con sus esquemas de respuesta, campos anidados y valores de los retornos internos, escalado sin estado_run y fecha_corte de CT-09 exigida por la mensajería; la V5.1 .md y .docx pasa sin cambios a bloque_a/99_Historico_V5.1/01_Gobernanza; re-congelado del corpus con tools/corpus_integridad.py --update por ese motivo: solo cambian las dos rutas movidas, la V5.2 nueva y el README índice del bloque, que lleva la entrada del registro; goldens de contratos re-congelados con goldens_ct.py --update --motivo, divergencias_anexo_b.json sin diferencias medidas; la V5.2 no tiene .docx, INC-T143-01) [pendiente QA]

## Ronda r03 (QA r02 NO APTO)

### Qué cambia en el Anexo B V5.2, hallazgo a hallazgo

| Hallazgo | Código que manda | Texto nuevo |
| --- | --- | --- |
| H-07 | `Bloque.ciclo` (`orquestacion.py`): `memoria` = `opp_vigentes`, `tnd_activas`, `lec_aplicables`, `certificados`, y `delta_gc0` = GC0 por tipo; `seguimiento.py`: `memoria` = `{senales_interes}`, `delta_gc0` = `{}`; `_integrar`: `memoria` = `{run_anterior, top3_anterior}`, `delta_gc0` = motivos por tipo; en V6, `integracion_determinista` y ninguna orden INTEGRACION | CT-05: «Lo que llevan `memoria` y `delta_gc0` depende del tipo», con una frase por tipo, y «En el diseño V6 no hay orden INTEGRACION ni su retorno: la integración la calcula el código» |
| H-08 | `FINALISTA`, `TIPOS_OPCION`, `REGIONES`, `AMBITO`, `INDICADOR`, `INVERTIBILIDAD` (`contratos.py`) | La frase de `finalistas` da los valores de `tipo_opcion`, `horizontes_aplicables` y `regiones`, y nombra los 13 opcionales con los valores de `naturaleza_inversion`, `horizonte_principal` y `liquidez`; ocho frases «En `FINALISTA`, …» para `ambito`, `indicador_seguimiento`, `invertibilidad`, `catalizadores`, `invalidacion_cuantitativa`, `dimensiones`, `afirmaciones` y `tendencia`; la introducción dice que la ficha es la de `FINALISTA` y se describe así. La regla «un campo con lista cerrada lleva sus valores entre paréntesis» se cumple sin acotarla |
| H-09 | `_invocar("AG-19", "CT-17", …, "AUDITORIA")` | CT-17: «Respuesta: la del Auditor, con `AUDITORIA`, que exige `hallazgos` y `resumen`», y cada hallazgo, con `regla`, `descripcion` y `severidad` (Crítica \| Material \| Operativa \| Menor); CT-17 en la lista de retornos internos; esquema derivado y ejemplo nuevos de CT-17.RETORNO |
| H-10 | `_peticion_conocimiento`: lee `afirmacion` (si no, la síntesis), `direccion` (si no, neutra), `extracto` o `motivo`, y `pronostico_fuente`; en backtest descarta las REF- no ofrecidas | Una frase tras la de `BUSQUEDA` con lo que lee y sus valores por defecto, y «En backtest solo cuentan las referencias registradas que se le ofrecieron»; `ref_id` es «el identificador de la referencia» |

Además, para que la marca de opcional acompañe al campo (H-11 a), CT-04 dice «Son opcionales los cinco bloques, que se envían por separado: …».

### Pruebas (H-11)

- `_opcionales_sin_marca`: un campo cuenta como marcado solo si va en una lista tras «Son opcionales», antes de «son opcionales», «es opcional», «van si aplica» o «solo con», entre paréntesis «(opcional)» o «(si aplica)», en el bloque JSON con «opcional» o «solo en», tras «no envía», o en una frase que dice que la mensajería no lo exige. Desde la r03 mira también los campos del sobre que el derivado nombra sin exigirlos (`query_id` de CT-03, `run_id` de CT-23). Mutantes nuevos: P01, P02, P07 y P08 de `r02_03`.
- `_esquemas_de_respuesta_que_difieren`: CT-17 con `AUDITORIA`; la ficha de los finalistas se compara por dentro con la clave `FINALISTA` (anidados, opcionales y valores, también de una lista de valores cerrados como `regiones`); frases fijas y frases prohibidas en CT-05, CT-06, CT-14 y CT-15 (D20, D21 y P05/P06 de los revisores). Doce mutantes nuevos en `test_t143_r02_un_cambio_en_los_valores_o_en_los_anidados_se_nota` (C12, C13, P03, D20, D21, P06 entre ellos).
- `test_t143_r03_la_memoria_de_cada_orden_ct05_es_la_del_anexo_b` y cinco mutantes: la `memoria` y el `delta_gc0` de las órdenes CT-05 de los flujos simulados y de la orden INTEGRACION (un espía de `_invocar` en un ciclo V5 y otro V6; la orden INTEGRACION no pasa por la mensajería) frente a la prosa (C18, C19 y D23).
- C21: `capturar_flujos` (`tests/goldens_ct.py`) ya no rompe con `IndexError` si un cambio del ejecutor deja el ciclo sin opciones; los flujos de decisión y seguimiento quedan vacíos, y fallan `test_t143_r02_cada_fase_de_ct06_…` y `test_h01_los_flujos_cubren_…`. Es código de pruebas, no del ejecutor; con opciones, la captura es la misma de antes (los goldens no cambian por esto).

### Re-congelado de la r03

- Goldens: `goldens_ct.py --update --motivo "T-143 r03 (QA r02 NO APTO, H-07 a H-10): …"`, una línea en `REGISTRO.md` (`huellas.json`, `mensajes_ejemplo.json`). `divergencias_anexo_b.json`, `aceptaciones_rechazos.json` y `formas_flujos_mock.json` no cambian.
- Corpus: `tools/corpus_integridad.py --update`. Frente a la r02 solo cambia la línea de la V5.2 (`ca5ab7dd…` → `21d01585…`). Frente a `1ccffd5`, las mismas 6 rutas (3 líneas quitadas y 4 puestas): las dos V5.1 de `01_Gobernanza` quitadas; las dos del histórico con los mismos hashes (`26691b68…`, `7e708a03…`); la V5.2 (`21d01585…`); el README índice (`70f6b0de…` → `e25d7eb7…`).

**Texto del motivo para el commit (sustituye a los de la r01 y la r02):**

> docs: Bloque A, T-143 (Documento 0 V5.2: la V5.1 con el Anexo B corregido para que describa lo que hace el ejecutor, por la decisión del operador del 13-11-2026 «manda el código» y la nueva entrega autorizada el 15-11-2026; rondas r02 y r03 tras las QA r01 y r02: CT-04 con aprobar_certificados, retornos de CT-05, CT-15 y CT-17 con sus esquemas de respuesta, memoria de cada orden CT-05 y sin INTEGRACION en V6, ficha FINALISTA con sus valores y anidados, lo que se lee de cada referencia de BUSQUEDA, escalado sin estado_run y fecha_corte de CT-09 exigida por la mensajería; la V5.1 .md y .docx pasa sin cambios a bloque_a/99_Historico_V5.1/01_Gobernanza; re-congelado del corpus con tools/corpus_integridad.py --update por ese motivo: solo cambian las dos rutas movidas, la V5.2 nueva y el README índice del bloque, que lleva la entrada del registro; goldens de contratos re-congelados con goldens_ct.py --update --motivo, divergencias_anexo_b.json sin diferencias medidas; la V5.2 no tiene .docx, INC-T143-01) [pendiente QA]

## Ronda r04 (QA r03 NO APTO)

### Qué cambia en el Anexo B V5.2

| Hallazgo | Código que manda | Texto nuevo |
| --- | --- | --- |
| H-12 | `Bloque.ciclo`: con `v6` y `v6.sintetizador` (por defecto `true`), `integracion_determinista`; si no, `_integrar` (orden INTEGRACION a AG-02). Redacción: con `v6.sintetizador`, AG-26 con `SINTESIS`; si no, AG-17 con `REDACCION` | CT-05: «En el diseño V6 (con `v6.sintetizador`, el valor por defecto) no hay orden INTEGRACION ni su retorno: el código calcula antes de G3 el régimen de cada tipo y los cambios frente al run anterior, y el Sintetizador escribe después la integración con `SINTESIS` (CT-15). Con `v6.sintetizador` desactivado, el V6 emite la orden INTEGRACION como el V5.» CT-15: el Sintetizador responde «con `v6.sintetizador`, el valor por defecto; si no, responde el Redactor con `REDACCION`», y «Los campos de integración de `SINTESIS` son la integración del V6» |
| H-13 | `_registrar_evidencia_clase`: curación si el nivel es N2 o N3 y, en el V6, con `v6.curacion_llm` (por defecto `false`); `_validar_g3`: en el V6 sin `v6.dictamen_g3_llm` (por defecto `false`), se crea el CT-14 y no se invoca a AG-18 | CT-11: «El ejecutor pide la curación solo en los niveles N2 y N3; en el diseño V6, solo con `v6.curacion_llm`, que viene desactivado: entonces no se emite el CT-11 y la curación es determinista». CT-14: «En el diseño V6, salvo con `v6.dictamen_g3_llm`, que viene desactivado, el CT-14 se emite pero no se pide dictamen a AG-18: lo da la regla, apto con advertencias si no hay bloqueos y bloqueado si los hay» |
| H-14 | `_auditar`: `h.get("objeto", run_id)`; `_peticion_conocimiento`: `datos["referencias"][:3]` | CT-17: «De cada hallazgo, el ejecutor toma además, si lo trae, `objeto` (si no, el run auditado), que el esquema no exige». CT-07/CT-08: «Solo usa las tres primeras referencias de la respuesta» |

### Pruebas (H-15)

- `FRASES_FIJAS` gana CT-05 (la nota del V6, con y sin Sintetizador), CT-07 (valores por defecto, regla de backtest, tres primeras), CT-11, CT-14 y CT-17; `FRASES_PROHIBIDAS` de CT-05 impide la frase de la r03 («la integración la calcula el código»).
- `test_t143_r04_lo_que_cambia_en_el_v6_es_lo_que_dice_el_anexo_b`: el espía de `_invocar` corre ahora tres ciclos cortos (V5, V6 y V6 con `v6.sintetizador: false`) y comprueba qué se invoca en cada uno (INTEGRACION, CURACION, REDACCION, SINTESIS, DICTAMEN_G3). Del dictamen G3 solo se mide que el V6 no lo pide; con el cliente simulado HT-09 sale APTO y el V5 tampoco lo pide, así que la otra mitad queda en la frase fija.
- `test_t143_r04_lo_que_el_ejecutor_lee_de_cada_referencia_es_lo_que_dice_el_anexo_b`: `_peticion_conocimiento` con una respuesta de `BUSQUEDA` dada (cliente sustituido), en backtest: la REF- no ofrecida y la cuarta referencia no cuentan, y una referencia sin `afirmacion` ni `direccion` da la síntesis y neutra (C28, D31 y las tres primeras).
- `test_t143_r04_de_cada_hallazgo_el_ejecutor_toma_objeto`: `_auditar` con una respuesta de `AUDITORIA` dada: el `objeto` del hallazgo y, si falta, el run (C29).
- `test_t143_r04_un_cambio_en_esas_frases_se_nota`: cuatro mutantes de la prosa (D30, D31, sin las tres primeras, otra clave del hallazgo).

### Re-congelado de la r04

- Goldens: `goldens_ct.py --update --motivo "T-143 r04 (QA r03 NO APTO, H-12 a H-14): …"`, una línea en `REGISTRO.md` (solo `huellas.json`). Los esquemas y ejemplos derivados no cambian.
- Corpus: `tools/corpus_integridad.py --update`. Frente a la r03 solo cambia la línea de la V5.2 (`21d01585…` → `d8f9e3d0…`). Frente a `1ccffd5`, las mismas 6 rutas (3 líneas quitadas y 4 puestas): las dos V5.1 de `01_Gobernanza` quitadas; las dos del histórico con los mismos hashes (`26691b68…`, `7e708a03…`); la V5.2 (`d8f9e3d0…`); el README índice (`70f6b0de…` → `e25d7eb7…`).

## Ronda de cierre (QA r04 APTO con H-16 a H-18)

- Copia: worktree nuevo sobre `origin/develop`, `git merge --no-ff --no-commit 238ef4d` (sin conflictos) y `qa.md` y `revisores/` de `6336cdc`; no se integra la instantánea `0b09071` (H-18), así que ni `.venv` ni la deuda técnica entran en el diff.
- Solo cambia `tests/test_fase3_goldens.py` (H-16), sin tocar el código del ejecutor, el Documento 0 ni los goldens (sin re-congelado):
  - `test_t143_r04b_dictamen_g3_del_v6` (6 casos): `_validar_g3({"clases": {}, "limitaciones": []}, {}, …)` con `orquestacion.sint.ht09_validar` sustituido por `monkeypatch` (una `C05` en ADVERTENCIA o BLOQUEO), `mensajeria.crear` y `_invocar` espiados; CT-14 en los seis, `DICTAMEN_G3` a AG-18 salvo en el V6 por defecto, dictamen APTO_CON_ADVERTENCIAS o BLOQUEADO (E01).
  - `test_t143_r04b_curacion_por_nivel_y_diseno` (6 casos): `_registrar_evidencia_clase` con una finalista con una pieza, `_filtrar_evidencia` sustituido y `_invocar` que corta en la primera invocación; CT-11 solo en N2 del V5 y del V6 con `curacion_llm` (E02, E03).
  - `FRASES_FIJAS["CT-15"]` gana las dos frases del Sintetizador (F01, F02); `test_t143_r04_lo_que_cambia_en_el_v6_…` las comprueba (además, `_esquemas_de_respuesta_que_difieren` ya recorre todas las frases fijas) y pierde la aserción vacía `("CT-14", "DICTAMEN_G3") not in v6`.
- Límite: las dos pruebas nuevas miden `_validar_g3` y `_registrar_evidencia_clase` aisladas, no un ciclo entero; N3 y N0 no se parametrizan (la QA pidió N1 y N2; `r04_01` cubre N0–N3).

**Texto del motivo para el commit (sustituye a los anteriores):**

> docs: Bloque A, T-143 (Documento 0 V5.2: la V5.1 con el Anexo B corregido para que describa lo que hace el ejecutor, por la decisión del operador del 13-11-2026 «manda el código» y la nueva entrega autorizada el 15-11-2026; rondas r02 a r04 tras las QA r01 a r03: CT-04 con aprobar_certificados, retornos de CT-05, CT-15 y CT-17 con sus esquemas de respuesta, memoria de cada orden CT-05, el diseño V6 con sus interruptores (sintetizador, curación y dictamen G3), ficha FINALISTA con sus valores y anidados, lo que se lee de cada referencia de BUSQUEDA y de cada hallazgo de AUDITORIA, escalado sin estado_run y fecha_corte de CT-09 exigida por la mensajería; la V5.1 .md y .docx pasa sin cambios a bloque_a/99_Historico_V5.1/01_Gobernanza; re-congelado del corpus con tools/corpus_integridad.py --update por ese motivo: solo cambian las dos rutas movidas, la V5.2 nueva y el README índice del bloque, que lleva la entrada del registro; goldens de contratos re-congelados con goldens_ct.py --update --motivo, divergencias_anexo_b.json sin diferencias medidas; la V5.2 no tiene .docx, INC-T143-01) [pendiente QA]
