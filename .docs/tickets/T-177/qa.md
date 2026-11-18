# T-177 · QA independiente

- **Revisor:** claude (subagente revisor sin el contexto de la implementación; implementó otra sesión de claude) · **Ronda:** r01 · 17-11-2026

## Reproducción desde limpio

- Worktree nuevo de `wip/t177` (`aaefe03`) y otro de `develop` (`51d68f5`) para comparar; venv del repo.
- `pytest -q tests/test_t177_c4_credenciales.py`: 16 passed. `tests/goldens_ct.py`: coinciden. ruff de los ficheros nuevos con la config del repo: limpio.
- `.docs/tickets/T-177/ciclo_mock_t177.sh` (PB-58 de punta a punta por la CLI): OK.
- Sin falsos positivos del bloqueo nuevo de `agentes.invocar`: backtest mock 2024-01-05 → 2024-02-02 y ciclo mock 2024-03-01 en las dos ramas: `senales.csv`, `pronosticos.csv` y `metricas.json` idénticos byte a byte; el resto solo difiere en rutas absolutas y latencias; ciclo COMPLETO igual en las dos; ninguna incidencia «bloqueada por R8».
- Por orden del encargo, sin suite completa ni `check_all.sh` (CA-6 no lo he vuelto a medir).
- Ataques: `revisores/r01_ataques_r8.py` (15 casos). Se ejecuta desde `bloque_a/11_Ejecutor` con `python -m pytest -q -s -p no:cacheprovider ../../.docs/tickets/T-177/revisores/r01_ataques_r8.py`. Los casos `HALLAZGO_*` pasan mientras el fallo siga ahí; al corregirlos se invierte la aserción.

## Criterios de aceptación

| Criterio | Cumple | Evidencia |
| --- | --- | --- |
| CA-1 | sí | `test_t177_pb58_c4_bfa_solicita…` y `ciclo_mock_t177.sh`: AG-16 recibe solo el alias y el estado |
| CA-2 | sí | La misma prueba: CT-25 AG-01 → BROKER con solicitante AG-16; la CRD- está SOLICITADA sin valor y la C4- la enlaza |
| CA-3 | **no** | La deduplicación entre C4 compara `servicio` al pie de la letra (H-02), y dos C4 a la vez emiten dos CT-25 (H-03) |
| CA-4 | **en parte** | Las seis variantes de `test_r01_variantes_bloqueadas` se bloquean. Pero un valor fuera de la clave exacta `solicitudes_credenciales` llega a `cache_resultados.jsonl` (H-01), y a la cinta de grabación (H-04) |
| CA-5 | sí (nominal) | `test_t177_pb58_criterio_completo` y el script de la CLI |
| CA-6 | sin medir | Mapa y evidencias en «Superada»; goldens sin diferencias; gate no ejecutado por orden |

Criterio de PB-58 (plan V3.0) y Documento 0 V5.3 (7.10.1 y 7.10.2, CT-25, HT-01 y R8, leídos por sección):
- **Bien:** el diseño sigue el 7.10.1 (el BFA las envía directamente al Coordinador con su retorno, en el C4) y el 7.10.2 (deduplicar, comprobar en HT-01 y emitir el CT-25 con servicio, uso, solicitante e impacto).
- **Falla:** el criterio «cero apariciones del valor en … archivos» no se cumple en H-01 y H-04, y «segunda solicitud resuelta sin molestar al Broker» no se cumple en H-02 y H-03.

## Decisiones `[PROPUESTO]` (INC-T177-01)

- **Lista `servicios_bfa` vacía por defecto.** Razonable: qué APIs de pago se contratan lo decide el operador (T-57), y F9 no vale como lista. Pero **con la lista vacía, PB-58 no ocurre en un run real**. El BFA recibe `servicios: []` y no tiene nada que revisar (no ve sus fuentes), así que no pedirá nada salvo que se lo invente. Aun así se le llama y se gastan UC (H-07). PB-58 «Superada» vale como prueba con su preparación, no como comportamiento por defecto. Para cerrar: que las evidencias de PB-58 lo digan, y que la deuda conserve «declarar `credenciales.servicios_bfa`» como pendiente del operador después de cerrar T-177.
- **Sin canal AG-16 → AG-01.** Razonable. La fila CT-25 del Documento 0 pone al BFA «en origen», y hay el precedente de CT-07. Los goldens no cambian.
- **El C4 corre cada vez que se pide.** Razonable solo si repetirlo es de verdad inocuo, y hoy no lo es: H-02 y H-03 duplican el CT-25, y H-07 aplica el presupuesto semanal a cada llamada.
- **`impacto` como sinónimo de `impacto_si_falta`.** Razonable e inocuo.

## Hallazgos

| ID | Gravedad | Cómo reproducirlo | Esperado / obtenido | Corrección sugerida | Estado |
| --- | --- | --- | --- | --- | --- |
| H-01 | alta | `r01_…::test_r01_HALLAZGO_H01_…[valor_en_raiz]` y `[clave_en_mayusculas]`: el BFA devuelve `{"solicitudes_credenciales":[…], "valor": S}`, o `{"Solicitudes_Credenciales":[{…, "valor": S}]}` | **Esperado:** el valor en ningún archivo (R8). **Obtenido:** `desde_retorno` rechaza bien el retorno, pero `agentes.invocar` ya lo ha guardado en `estado/cache_resultados.jsonl`. El bloqueo nuevo solo mira `datos.get("solicitudes_credenciales")`, con esa clave exacta, mientras que `desde_retorno` mira el retorno entero. La propia corrección de seguridad del ticket queda incompleta. | Hacer la comprobación antes de cualquier persistencia, en `llm.respuesta_segura`, que ya pasa antes de la caché y de la cinta (H-04). En `llm.py`: `from .contratos import claves_valor_credencial, secretos_en_texto`, una función `solicitud_con_valor(texto)` y `respuesta_segura` con `if contenido_sensible(r.texto) or solicitud_con_valor(r.texto):`. La función: si el texto no contiene `solicitudes_credenciales` (sin mirar mayúsculas), devuelve False. Si lo contiene, hace `json.loads` del tramo `{…}`; si no se puede leer, devuelve True (falla cerrado). Con un dict que tenga alguna clave cuyo `lower()` sea `solicitudes_credenciales`, devuelve `bool(claves_valor_credencial(datos))` sobre **todo** el dict, y True ante `RecursionError`. Lo he probado en mi copia: los dos casos H-01 y el H-04 se bloquean, y de las 16 pruebas del ticket solo cambia la aserción de la línea 154 (el detalle pasa a «turno no utilizable (contenido_sensible)»). El bloqueo T-177 de `agentes.invocar` se puede quitar o dejar como segunda barrera sobre todo `datos`. Regresión: invertir los dos casos H-01. | abierto |
| H-02 | media | `r01_…::test_r01_HALLAZGO_H02_…`: primera C4 con «API de fondos cerrados» y segunda con «api de fondos cerrados» (mismo alias de la bóveda) | **Esperado:** la segunda da YA_SOLICITADA (CA-3, 7.10.2). **Obtenido:** dos CRD- SOLICITADA y dos CT-25 al Broker. Dentro de un mismo retorno se deduplica por alias, pero `Credenciales.solicitar` busca las previas con `c.get("servicio") == servicio`, al pie de la letra. Con un modelo real la grafía cambia entre meses. | En `interfaz_broker.Credenciales.solicitar`: `previas = [c for c in self._todas().values() if alias_de(str(c.get("servicio") or "")) == alias_de(servicio)]`. Lo he probado: la segunda da YA_SOLICITADA y `test_t177_*` y `test_v51` siguen en verde (29). Regresión: invertir el caso H-02. | abierto |
| H-03 | media | `r01_…::test_r01_c4_concurrente_dos_bloques`: dos `Bloque` sobre la misma carpeta de estado (dos `credencial c4` a la vez) | **Esperado:** un solo CT-25. **Obtenido:** dos CRD- y dos CT-25. `solicitar` lee F5, crea el mensaje y escribe F5 sin exclusión entre la lectura y la escritura. | En `solicitar`, después del caso PROVISTA, envolver desde `previas = …` hasta el `return` final en `with self.b.almacen._transaccion():`, que ya da exclusión entre hilos y procesos y es reentrante (o exponerlo con un nombre público). Lo he probado: queda 1 CRD (`YA_SOLICITADA`, `SOLICITADA`). Regresión: el caso, con la aserción `len(crd) == 1`. | abierto |
| H-04 | alta | `r01_…::test_r01_HALLAZGO_H04_…`: `ReplayClient(cinta, "grabar", MockClient())` y el BFA devuelve `solicitudes_credenciales:[{…, "valor": S}]` | **Esperado:** el valor en ningún archivo. **Obtenido:** el ciclo lo bloquea (SIN_RESULTADO), pero el valor queda en la cinta. `ReplayClient.generar` la escribe tras `respuesta_segura`, y el bloqueo T-177 llega después. El modo sombra con grabación es justo el que se usa con la API real. | La misma corrección de H-01: con la comprobación en `respuesta_segura`, la cinta guarda el texto vacío y `stop_reason` «contenido_sensible». Probado. Regresión: invertir el caso H-04. | abierto |
| H-05 | baja | `r01_…::test_r01_limite_detector[campo_credencial]`: `{…, "credencial": S}` | **Esperado:** rechazo. **Obtenido:** se emite el CT-25 y S queda en la caché. `CAMPOS_VALOR_CREDENCIAL` compara la clave tal cual y le faltan `credencial`, `credential`, `secret`, `contraseña`, `passwd`, `pwd` y `access_token`; `api-key` (con guion) tampoco coincide. | En `contratos.py`: `CAMPOS_VALOR_CREDENCIAL = frozenset({"valor", "clave", "secreto", "secret", "valorcredencial", "credencial", "credential", "password", "passwd", "pwd", "contrasena", "contraseña", "token", "accesstoken", "apikey"})`, y en `claves_valor_credencial`, comparar `re.sub(r"[^a-z0-9ñ]", "", str(k).lower())`. Así `credencial_ref` («credencialref») no cae. `interfaz_broker.CAMPOS_VALOR` tiene que normalizar igual donde lo use. Prueba con las nuevas grafías y con `credencial_ref` sin rechazo. | abierto |
| H-06 | baja | `r01_…::test_r01_limite_detector[motivo_sin_etiqueta]`: `motivo: "usar " + S` (un valor opaco sin etiqueta) | **Esperado:** rechazo. **Obtenido:** S llega a F5 (CRD-, `uso_previsto`), al CT-25 que va al Broker, a la C4- y a la caché. | En `desde_retorno`, después de construir `textos`: si algún texto de `servicio`, `motivo` o `impacto_si_falta` tiene una ficha opaca, tomar el camino de rechazo SEGURIDAD que ya existe. Ficha opaca: `(?<![A-Za-z0-9])(?=[A-Za-z0-9_\-]*[A-Za-z])(?=[A-Za-z0-9_\-]*\d)[A-Za-z0-9_\-]{N,}(?![A-Za-z0-9])`, sin `.` ni `/` para no rechazar URLs. N es la longitud mínima que ya usa `RE_VALOR_GENERICO`, sacada a una constante común (no un número nuevo a mano). Documentar en INC-T177-01 que un LEI en el motivo se rechaza (falla cerrado). | abierto |
| H-07 | baja | `credencial c4` con la configuración por defecto (`servicios_bfa: []`), o varias C4 en la misma semana | **Esperado:** la bolsa «3 UC/semana» del Anexo A como tope semanal, y no gastar UC sin nada que revisar. **Obtenido:** se llama a AG-16 con `servicios: []` y cada llamada tiene 3 UC nuevas: el tope semanal pasa a ser por llamada. INC-T177-01 lo dice, pero relaja un control. | En `mantenimiento_c4`: (a) sin servicios, no invocar y escribir la C4- con `estado_retorno: "SIN_SERVICIOS"`; (b) guardar en la C4- el UC de la llamada (`ResultadoAgente`) y dar a la bolsa `presupuesto_uc_semana.BFA` menos la suma de las C4- de AG-16 de los 7 días hasta `as_of`; si no queda, no invocar y poner `estado_retorno: "SIN_PRESUPUESTO"`. Pruebas de las dos cosas, y actualizar INC-T177-01. | abierto |

Sin hallazgo:
- Mayúsculas en `API_KEY`, claves anidadas, valores en listas, `password=` en el motivo y una clave `sk-` en el servicio: se bloquean y no quedan en ningún archivo.
- HA no copia el valor.
- La C4 repetida con la misma grafía no duplica nada.
- La configuración inválida falla antes de mutar.

## Veredicto

**NO APTO**: hay dos hallazgos altos de R8 (H-01 y H-04) y CA-3 no se cumple (H-02 y H-03). Los bajos H-05, H-06 y H-07 se corrigen en este mismo ticket (regla del operador). Tras la corrección, el revisor vuelve a pasar `revisores/r01_ataques_r8.py`, con los casos HALLAZGO invertidos, y abre la ronda r02.

## Ronda r02

- **Revisor:** claude (subagente revisor nuevo, distinto del de la r01 y de quien implementó) · **Ronda:** r02 · 18-11-2026
- **Reproducción:** worktree nuevo de `wip/t177` (`ac0fe21`, sobre develop `c9daa4e`) y otro de `c9daa4e` para comparar; venv del repo. Por orden del encargo, sin suite completa ni `check_all.sh`.
- **Scripts nuevos** (desde `bloque_a/11_Ejecutor`, con `python -m pytest -q -s -p no:cacheprovider ../../.docs/tickets/T-177/revisores/<script>`):
  - `r02_ataques_r8.py` (33 casos): familias que no estaban en la r01 (claves en otros idiomas o raras, escapes `\uXXXX`, JSON dentro de un texto, sitios fuera de los campos libres, codificados, partidos, listas, respuestas que no son dict, `valor` numérico) y los dos falsos positivos. Siempre con grabación de cinta (`ReplayClient` en modo `grabar`) y caché activa. Los casos `HALLAZGO_*` pasan mientras el fallo siga ahí; al corregirlo se invierte la aserción.
  - `r02_falsos_positivos.py ARBOL SALIDA {v5|v6} {texto|numero|sin}`: un ciclo mock con los 12 perfiles en el que los Analistas simulados devuelven, como manda su prompt, `solicitudes_credenciales: []` e `indicadores[].valor`.
  - `r02_concurrencia_presupuesto.py` (6 casos): H-03 con procesos de verdad y H-07 (tope y borde de la semana).

### Re-ejecución de lo anterior

- `revisores/r01_ataques_r8.py`, con los HALLAZGO invertidos: 15/15. `tests/test_t177_c4_credenciales.py`: 43/43.
- Regresión de los vecinos: `test_t174_pb61_revision_c2`, `test_t176_pb36_pb33`, `test_t178`, `test_t165_g3_met13`, `test_t177` y r01: 286 passed. Suites R8 (`test_t103`, `test_t120`, `test_t123`, `test_t130`, `test_t136`) y `test_v51`: 161 passed.
- H-02, H-03 y H-07 se confirman corregidos:
  - **H-03:** cuatro `bloque-a credencial c4` lanzados a la vez como procesos, con tres servicios, en cuatro rondas. Siempre 3 CRD- y 3 CT-25 distintos, y F5 íntegra (`verificar_integridad`).
  - **H-07:** el tope semanal se respeta. La C4 se corta en `SIN_PRESUPUESTO` con 1,20 UC gastadas, porque la reserva del peor caso (T-146) no cabe en las 1,80 que quedan, así que el tope es conservador. A los 6 días sigue `SIN_PRESUPUESTO` y a los 7 vuelve a tener 3 UC.

### R8: familias nuevas

| Familia | Resultado |
| --- | --- |
| Clave rara que se normaliza (`Valor` con espacio de anchura cero, `VALOR`, `Api-Key`, `access.token`, `Contraseña`) | bloqueado, en ningún archivo |
| Escape en la clave de valor (`"valor"`) | bloqueado |
| Listas (lista de retornos, solicitudes anidadas en listas), texto sin llaves, prosa con `{…}` delante, bloque ```` ```json ```` | bloqueado |
| base64 «limpio» y hex del secreto en el motivo | bloqueado (`RE_FICHA_OPACA`) |
| Clave de valor en otro idioma o fuera de la lista (`value`, `wert`, `senha`, `chiave`, `mot_de_passe`, `key`, `secret_value`, `valor_api`, `パスワード`, `clé`, `vａlor` de ancho completo) | **H-08**: se emite el CT-25 (sin el valor), pero el valor queda en `cache_resultados.jsonl` y en la cinta |
| JSON dentro de un texto (`solicitudes_credenciales` como texto JSON), `motivo` como dict, secreto en `urgencia` | **H-08**: caché y cinta |
| Clave `solicitudes_credenciales` escrita con `_` (JSON válido) | **H-09**: la segunda barrera para el retorno (no hay CT-25 ni caché), pero la cinta guarda el valor |
| base64 con `/` y `+` cada pocos caracteres en el motivo | **H-10**: F5 (CRD- y C4-), CT-25 al Broker, caché y cinta |
| `valor` numérico | **H-11**: el Coordinador lo rechaza como valor de credencial (SEGURIDAD), pero queda en la caché y en la cinta |
| Secreto partido en dos campos de menos de 16 | llega a F5, al CT-25, a la caché y a la cinta. Límite inherente de cualquier detector: sin hallazgo, pero hay que declararlo en INC-T177-01 |
| Secreto sin etiqueta fuera de `solicitudes_credenciales` (en `sintesis`, `lagunas` o en la raíz bajo `value`) | caché y cinta. Es el límite general de R8 para el texto libre de cualquier agente (INC-T123-01), no de T-177: sin hallazgo |

HA, la mensajería y los entregables no reciben el valor en ningún caso salvo H-10, que lo lleva al CT-25.

### Falsos positivos

- **Desviación del valor numérico.** No es inocua. Existe porque todos los informes de Analista llevan `solicitudes_credenciales`, como fija el formato de salida de su prompt (Marco común V5.0, l. 44, y los 13 prompts de clase). Esa clave activa la barrera en cada informe. Pero ese mismo formato pone `indicadores[].valor` como **texto** (`"valor":"…"`, l. 33), así que la desviación no evita el falso positivo que buscaba evitar (H-12).
- **Medición.** `r02_falsos_positivos.py` con los 12 perfiles y los Analistas simulados en el formato del prompt:

  | Árbol | V5 | V6 |
  | --- | --- | --- |
  | `c9daa4e` | COMPLETO, 0 bloqueos | COMPLETO, 0 bloqueos |
  | r02 | **PARCIAL, 12 informes descartados** (AG-03…AG-09, AG-21…AG-25: «turno no utilizable (contenido_sensible)»), 14 limitaciones frente a 2 | **PARCIAL, 12 informes descartados**, 15 limitaciones frente a 3 |

  El control (`sin`, el mock tal cual) es igual en los dos árboles. Por eso el backtest mock idéntico no prueba la ausencia de falsos positivos: los Analistas simulados no emiten `solicitudes_credenciales`.
- **`RE_FICHA_OPACA` (16).**
  - Hashes, ids y huellas en las respuestas de otros agentes: sin falso positivo. Solo se mira dentro de las solicitudes.
  - Dentro de una solicitud, el `-` cuenta como parte de la ficha. `CURVA-USD-2S10S-TR` (un símbolo del universo de ejemplo) o `ICE-BofA-US-HY-2024` en el motivo descartan la respuesta entera, sea un informe de Analista o la C4 (H-13).
  - Un sha256 o un LEI también caen. Está declarado y es aceptable.

### Hallazgos r02

| ID | Gravedad | Cómo reproducirlo | Esperado / obtenido | Corrección exacta | Estado |
| --- | --- | --- | --- | --- | --- |
| H-08 | alta | `r02_ataques_r8.py::test_r02_HALLAZGO_H08_*` (11 claves, 2 JSON en texto, 3 fuera de forma) | **Esperado:** el valor en ningún archivo (R8, CA-4, CA-5). **Obtenido:** dentro de `solicitudes_credenciales`, la barrera solo reconoce los nombres de `CAMPOS_VALOR_CREDENCIAL` y solo mira la ficha opaca en `servicio`, `motivo` e `impacto` de texto. Un valor bajo `value` (el desliz más probable de un modelo), en `urgencia`, en un `motivo` dict o en una lista escrita como texto JSON pasa a la caché y a la cinta. Mismo sumidero y consecuencia que H-01 y H-04. | En `llm._fichas_opacas_en_solicitudes`, recorrer **todo** el subárbol de cada `solicitudes_credenciales`: todas las claves y hojas de texto a cualquier profundidad, y el propio valor si es un texto. Es sensible si alguna tiene una ficha opaca (`opaca()`, ver H-10). Lo mismo en `desde_retorno`, que hoy mira solo los cuatro campos libres. Regresión: invertir los `HALLAZGO_H08`. | abierto |
| H-09 | media | `test_r02_HALLAZGO_H09_clave_con_escape_unicode_llega_a_la_cinta` | **Esperado:** la cinta sin el valor. **Obtenido:** `solicitud_con_valor` decide si mirar con `CLAVE_SOLICITUDES in clave_normalizada(texto)` sobre el texto **crudo**. `"solicitudes_credenciales"` no casa, pero `json.loads` da la clave normal. `ReplayClient.generar` graba antes de la segunda barrera. | En `solicitud_con_valor`, leer primero el JSON (`texto[ini:fin+1]`): si se puede leer, decidir con `_con_clave_solicitudes(datos)` y no con el prefiltro textual; si no se puede leer, mantener el prefiltro y el `return True` actuales. Regresión: invertir H-09 (`donde == []`). | abierto |
| H-10 | baja | `test_r02_codificados_en_el_motivo[b64_barras]` | **Esperado:** rechazo. **Obtenido:** `RE_FICHA_OPACA` excluye `/` y `+`, y un base64 con esos signos cada pocos caracteres queda en tramos de menos de 16. Llega a F5, al CT-25 al Broker, a la caché y a la cinta. | En `contratos.py`, `def ficha_opaca(t: str) -> bool`. Devuelve `RE_FICHA_OPACA.search(t)`, o cualquier palabra de `t.split()` sin `.` ni `:` que case entera con `RE_VALOR_GENERICO` (ya admite `+/=`; la URL sale por el `.` o el `:`). Usarla en `llm` y en `desde_retorno` en lugar de `RE_FICHA_OPACA.search`. Regresión: `b64_barras` con `== []`. | abierto |
| H-11 | baja | `test_r02_HALLAZGO_H11_valor_numerico_incoherente` | **Esperado:** coherencia: lo que el Coordinador llama «valor de credencial» no está en la caché. **Obtenido:** `solo_texto=True` deja pasar `{"valor": 4041773129}` dentro de una solicitud y `desde_retorno` lo rechaza con SEGURIDAD: el número queda en la caché y en la cinta. | Dentro del subárbol `solicitudes_credenciales`, contar también un número (no `bool`) bajo una clave de `CAMPOS_VALOR_CREDENCIAL`. Fuera, se rige por H-12. Regresión: H-11 con `donde == []`. | abierto |
| H-12 | alta | `test_r02_HALLAZGO_H12_informe_de_analista_canonico_descartado` y `r02_falsos_positivos.py` (tabla de arriba) | **Esperado:** un informe de Analista sin credenciales se usa (sin regresión frente a `c9daa4e`). **Obtenido:** la barrera aplica `claves_valor_credencial(datos, solo_texto=True)` a **todo** el retorno en cuanto existe la clave `solicitudes_credenciales`. Todo informe de Analista la lleva (vacía) y lleva `indicadores[].valor` de texto, así que con la API real **todos** los informes de los 12 Analistas se descartan (ciclo PARCIAL en V5 y V6). Lo mismo un `"clave": "…"` o un `"token": "ETH"` de texto en cualquier informe. | En `solicitud_con_valor`, **dentro** del subárbol `solicitudes_credenciales`, lo de H-08 y H-11. **Fuera** de él, solo cuentan las claves inequívocas de `CAMPOS_VALOR_CREDENCIAL` con texto (todas salvo `valor`, `clave`, `token` y `credencial`); esas cuatro, solo si su texto tiene una ficha opaca (`ficha_opaca`). En `contratos.py`, una constante `CAMPOS_VALOR_AMBIGUOS = frozenset({"valor", "clave", "token", "credencial"})`, documentada. Lo he prototipado con 15 casos: los dos informes canónicos pasan, y r01 (raíz, mayúsculas, `credencial`, motivo, anidado), H-08, H-10, H-11 y un `password` corto en la raíz se bloquean. Regresión: invertir H-12, y `r02_falsos_positivos.py … texto` con 0 bloqueos en V5 y V6. Añadir al mock de Analistas `solicitudes_credenciales: []` e `indicadores` con `valor` de texto, para que el backtest lo ejercite siempre. | abierto |
| H-13 | baja | `test_r02_HALLAZGO_H13_ficha_opaca_con_guiones` | **Esperado:** el nombre de una serie o de un símbolo en el motivo no es un valor. **Obtenido:** `RE_FICHA_OPACA` incluye `-` y `_` en la ficha: `CURVA-USD-2S10S-TR` (del universo de ejemplo) e `ICE-BofA-US-HY-2024` descartan la respuesta entera, también un informe de Analista que pida una credencial. | En `ficha_opaca` (H-10), aplicar `[A-Za-z0-9]{16,}` con letra y cifra a cada tramo de `re.split(r"[-_]", palabra)` en lugar de a la palabra con guiones. Una clave `sk-…` ya la cubre `RE_CANDIDATO_SK`. Declarar en INC-T177-01 que una clave con forma de UUID (tramos de 12 o menos) no se reconoce sin etiqueta. Regresión: invertir H-13 (`not solicitud_con_valor(...)`) y mantener `motivo_sin_etiqueta` de r01 bloqueado. | abierto |

Observaciones sin hallazgo:
- **Bolsa semanal con dos C4 a la vez.** Las dos leen `uc_c4_semana` antes de que ninguna escriba (`test_r02_h07_carrera_del_presupuesto`), así que entre las dos pueden gastar hasta el doble de lo que queda. Con el simulado no se pasa de la bolsa (0,85 de 3 UC). El C4 lo lanza un único planificador.
- **Límites que hay que declarar en INC-T177-01:** el secreto partido en campos cortos y el UUID (H-13).

### Veredicto r02

**NO APTO.**
- H-08 (alta, R8): un valor dentro de `solicitudes_credenciales` bajo una clave no listada llega a la caché y a la cinta.
- H-12 (alta, regresión): con la API real se descartan todos los informes de Analista, en V5 y en V6.

H-01 a H-07 de la r01 quedan corregidos. H-09 (media) y H-10, H-11 y H-13 (bajos) se corrigen en este mismo ticket (regla del operador). En la r03 el revisor vuelve a pasar `r01_ataques_r8.py`, `r02_ataques_r8.py` (con los HALLAZGO invertidos), `r02_falsos_positivos.py` (V5 y V6, `texto`, sin bloqueos) y `r02_concurrencia_presupuesto.py`.

## Ronda r03

- **Revisor y fecha:** claude, el mismo revisor de la r02 (no implementó) · 18-11-2026
- **Reproducción:**
  - Worktree nuevo de `wip/t177` (`49bd017`, sobre `ac0fe21`) y otro de `c9daa4e` para comparar.
  - Venv del repo.
  - Por orden del encargo, sin suite completa ni `check_all.sh`. No he vuelto a pasar los mutantes del implementador.
- **Scripts nuevos.** Se ejecutan desde `bloque_a/11_Ejecutor`.
  - `revisores/r03_ataques_regla_comun.py` (27 casos), con `python -m pytest -q -s -p no:cacheprovider`. Los casos `HALLAZGO_*` fijan lo observado; al corregirlos se invierten.
  - `revisores/r03_corpus_formatos.py ARBOL`. Saca los 97 objetos JSON de ejemplo de los system prompts de `02_System_prompts` y los pasa por `respuesta_segura`. Son los formatos de retorno de todos los agentes: Analistas, Prospectiva, Contrarias, Redactor, Curador, MC-xx, Coordinador y BFA.
  - Cada objeto se prueba dos veces: (a) con `solicitudes_credenciales: []` y (b) con una solicitud válida.

### Re-ejecución

- **Pruebas del ticket y scripts de los revisores:** 122 passed.
  - `test_t177`: 68.
  - `r01_ataques_r8.py`: 15.
  - `r02_ataques_r8.py`, con todos los HALLAZGO invertidos por la implementación: 33.
  - `r02_concurrencia_presupuesto.py`: 6.
- **Vecinas:** 389 passed. Son T-174, T-176, T-178, T-165, las suites R8 (T-103, T-120, T-123, T-130 y T-136) y `test_v51`.
- **`r02_falsos_positivos.py`:** COMPLETO y 0 bloqueos en V5 y en V6, con `texto`, `numero` y `sin`.
- **Backtest mock (2024-01-05 → 2024-02-02) frente a `c9daa4e`:**
  - `senales.csv` y `pronosticos.csv` son idénticos byte a byte.
  - `metricas.json` solo difiere en el consumo (`tokens_salida` 21952 → 22152 y `uc` 27,09 → 27,16), por los dos campos nuevos del mock de Analistas.

### Las dos pruebas adaptadas

Comparadas línea a línea con mi `fc91f6d`, ninguna sale debilitada.

- **Las inversiones.** Las de `r02_ataques_r8.py` son exactamente las previstas, una por caso `HALLAZGO`, y ninguna aserción se relaja. La de H-11 pasa de «rechazo del Coordinador» a «SIN_RESULTADO y en ningún archivo», que es más fuerte.
- **`test_r01_c4_concurrente_dos_bloques`.**
  - Mantiene la barrera de dos hilos dentro de `solicitar`. Si uno no llegara, la barrera se rompe y `len(res) == 2` falla.
  - Ahora la ejerce sobre dos `desde_retorno` simultáneos, que es donde está la carrera de H-03.
  - Añade dos C4 a la vez sin barrera, con `len(crd) == 1`.
  - Lo de entre procesos lo sigue cubriendo mi `test_r02_h03_cuatro_procesos_a_la_vez`: 4 rondas, 3 CRD- y 3 CT-25, y F5 íntegra.
- **`test_r02_h07_carrera_del_presupuesto`.**
  - La barrera sería imposible: la segunda lectura espera al cerrojo. Se sustituye por una espera de 0,5 s, que ensancha la ventana igual.
  - La aserción gana dos condiciones: `gastado <= bolsa` y exactamente una `COMPLETO` y una `SIN_PRESUPUESTO`.

### H-12, contra el corpus

| Prueba | Bloqueados en r03 | Bloqueados en r02 (control) |
| --- | --- | --- |
| 97 objetos de ejemplo de los prompts, (a) con la lista vacía | 0 | 17 (los 13 Analistas, el Marco común, Prospectiva y MC-06, MC-08 y MC-09) |
| Los mismos, (b) con una solicitud válida | 0 | 17 |

El control muestra que el script discrimina. Con contenido realista queda un falso positivo (H-15):
- una dirección `0x…` de 40 hexadecimales bajo `token` (Analista de Criptoactivos);
- o un LEI válido bajo `clave`.

En los dos casos se descarta el informe entero aunque la lista esté vacía, porque la clave ambigua lleva una ficha opaca. El propio `contratos._asignaciones_de_clave` (T-147) da por pública una dirección `0x`.

### R8 contra la regla común

| Familia | Resultado |
| --- | --- |
| Secreto como **clave** de una solicitud; dos grafías de la clave, una vacía y otra no; solicitudes dentro de un JSON en `sintesis`; JSON doblemente codificado; base64 de un JSON con `valor`; `valor` ambigua con ficha en la raíz | bloqueado: ni caché ni cinta |
| La misma clave escrita `_` en JSON legible; anidamiento de 5000 niveles | bloqueado (falla cerrado) |
| Los mismos valores no opacos de abajo bajo una clave de valor (`secreto`) | bloqueado |
| JSON **ilegible** con la clave escrita `solicitudes_credenciales` | **H-14**: el prefiltro textual mira el texto crudo y la respuesta pasa a la cinta |
| Valor **sin etiqueta** que no es una ficha opaca, bajo una clave no listada de una solicitud no vacía: 29 letras sin cifras, 16 cifras en texto, uno corto (`Hunter2x!`), uno con guiones en tramos menores de 16, o un `pin` numérico | **H-17**: se emite el CT-25 (sin el valor); el valor queda en la caché y en la cinta. No llega a F5, HA, la mensajería ni los entregables |

### Coste del sha256 y C4 bloqueada tras morir el proceso

- **sha256, LEI o un id largo de una URL en un informe que pide una credencial.** El informe entero se descarta: confirmado y declarado en INC-T177-01.
  - Lo acepto como falla cerrado.
  - El coste se repite cada semana mientras falte la credencial, y hoy el ejecutor ni siquiera lee las solicitudes de los Analistas (INC-T116-03).
  - Por eso conviene la exención exacta de H-15 también en la extensión, fuera del subárbol de solicitudes. El sha256 sigue cayendo: un secreto en hexadecimal tiene la misma forma.
- **Proceso muerto** (`test_r03_HALLAZGO_H16_…`, con SIGKILL durante la llamada al BFA).
  - La C4- queda `EN_CURSO` con `uc` = 3,0, toda la bolsa.
  - La C4 del mismo día y la del día +6 dan `SIN_PRESUPUESTO`; la del +7 da COMPLETO.
  - Así que no es «para siempre», sino como mucho 7 días. Con una C4 mensual es aceptable como falla cerrado.
  - Pero **ningún aviso** lo dice: ni una incidencia en HA, ni un campo en la C4- `SIN_PRESUPUESTO`, que solo trae `uc_semana_disponible: 0`. El operador no puede distinguir una bolsa gastada de una reserva huérfana (H-16).

### Hallazgos r03

| ID | Gravedad | Cómo reproducirlo | Esperado / obtenido | Corrección exacta | Estado |
| --- | --- | --- | --- | --- | --- |
| H-14 | baja | `test_r03_HALLAZGO_H14_texto_ilegible_con_clave_escapada` | **Esperado:** un texto ilegible que nombra el campo, aunque sea con un escape, es sensible. **Obtenido:** False; pasa a la cinta. | En `llm.solicitud_con_valor`, el último `return` debe mirar también el texto con los `\uXXXX` resueltos: `CLAVE_SOLICITUDES in clave_normalizada(re.sub(r"\\u([0-9a-fA-F]{4})", lambda m: chr(int(m.group(1), 16)), texto))`, con `or` sobre el actual. Regresión: invertir H-14. | abierto |
| H-15 | baja | `test_r03_falsos_positivos[cri_token_direccion_0x]` y `[clave_con_lei]` | **Esperado:** un informe con la lista vacía se usa. **Obtenido:** se descarta entero. | En `contratos.py`, `def _publico(t)`: True si `t` casa entero con `0x[0-9a-fA-F]{40}` (una dirección, no una clave privada de 64) o es un LEI válido (`[0-9A-Z]{18}[0-9]{2}` con módulo 97 = 1, ISO 17442; es la misma comprobación del IBAN de T-123). Aplicarlo **solo fuera** del subárbol de solicitudes: en `_fuera_sensible`, para las ambiguas (`ficha_opaca` sobre el texto sin esos tramos), y en el barrido entero de la extensión, sobre los textos fuera del subárbol. Dentro sigue como está (el LEI cae, ya declarado). Regresión: invertir los dos casos y añadir un `token` con 0x + 64 hexadecimales, que debe seguir bloqueado. | abierto |
| H-16 | baja | `test_r03_HALLAZGO_H16_proceso_muerto_reserva_huerfana` | **Esperado:** falla cerrado, pero visible. **Obtenido:** la semana queda bloqueada sin ningún aviso. | En `mantenimiento_c4`, guardar en la reserva `EN_CURSO` el `pid` (`os.getpid()`), como las EN_CURSO de T-174. Cuando una C4 dé `SIN_PRESUPUESTO`, poner en su C4- `reservas_en_curso: [ids]` de las C4- `EN_CURSO` de la ventana. Por cada una con `interfaz_broker._pid_vivo(pid) is False`, escribir una incidencia OTRO, severidad Operativa: «Reserva huérfana C4-… (proceso terminado): la bolsa semanal del BFA queda bloqueada hasta <fecha + 7 días>», sin liberarla. Declararlo en INC-T177-01. Regresión: invertir el aviso de H-16 (≥ 1) y que el +6 siga `SIN_PRESUPUESTO`. | abierto |
| H-17 | baja | `test_r03_HALLAZGO_H17_sin_etiqueta_bajo_clave_no_listada` (5 casos) | **Esperado:** el valor en ningún archivo (CA-4 y CA-5). **Obtenido:** caché y cinta. | En `contratos._subarbol_sensible`, una clave de un objeto solicitud que no esté en `CAMPOS_SOLICITUD = frozenset({"servicio", "motivo", "impactosifalta", "impacto", "urgencia"})` (normalizada) y lleve contenido (`_tiene_texto` o `_tiene_numero`) es sensible. Son los únicos campos que lee `desde_retorno`, y los prompts del BFA y de los Analistas no piden otros. Declarar en INC-T177-01 que un campo de más en una solicitud descarta el retorno (falla cerrado). Regresión: invertir los 5 casos (`SIN_RESULTADO` y `donde == []`), y que el nominal y `test_t177` sigan en verde. | abierto |

Ninguno es crítico, alto ni medio.

### Veredicto r03

**APTO**, con cuatro bajos abiertos.
- H-01 a H-13 están corregidos y verificados con los scripts de las tres rondas.
- H-12 queda resuelto contra los 97 formatos del corpus y en los ciclos V5 y V6.
- Los criterios CA-1 a CA-5 se cumplen salvo lo que dicen los bajos. CA-6 lo da el implementador (gate 12/12); aquí no se ha vuelto a medir, por orden.

Por la regla del operador, H-14 a H-17 se subsanan en este mismo ticket. Después, el revisor vuelve a pasar `r03_ataques_regla_comun.py`, con los HALLAZGO invertidos, y `r03_corpus_formatos.py`, y cierra la tarea. Hasta entonces no se cierra: el README queda en EN CURSO y la fila de la deuda sin tocar.

## Verificación de la ronda de cierre (r03: H-14 a H-17)

- **Revisor y fecha:** claude, el mismo de la r02 y la r03 (no implementó) · 18-11-2026.
- **Reproducción:**
  - Worktree nuevo y limpio del commit `5f98163` (sobre `49bd017`), con el venv del repo.
  - Por orden del encargo, sin suite completa ni `check_all.sh`. No he vuelto a pasar los mutantes ni el gate: el 12/12 y las cuotas son los que da el implementador.
- **Script nuevo:** `revisores/r03c_ataques_cierre.py` (20 casos), un ataque a cada corrección. Se ejecuta desde `bloque_a/11_Ejecutor` con `python -m pytest -q -s -p no:cacheprovider`.

### Re-ejecución

- **Pruebas del ticket y scripts de los revisores:** 180 passed.
  - `test_t177`: 79.
  - `r01_ataques_r8.py`, `r02_ataques_r8.py` y `r02_concurrencia_presupuesto.py`.
  - `r03_ataques_regla_comun.py`, con H-14 a H-17 invertidos; reviso abajo cómo.
  - `r03c_ataques_cierre.py`.
- **Vecinas:** 389 passed (T-174, T-176, T-178, T-165, R8 T-103/120/123/130/136 y `test_v51`).
- **Corpus:** `r03_corpus_formatos.py` da 97 objetos y 0 bloqueados, tanto con la lista vacía como con una solicitud.
- **`r02_falsos_positivos.py`:** COMPLETO y 0 bloqueos en V5 y en V6, en los modos `texto` y `sin`.
- **Backtest mock 2024-01-05 → 2024-02-02 frente a `c9daa4e`:** `senales.csv` y `pronosticos.csv` idénticos. `metricas.json` solo difiere en el consumo (`tokens_salida` 21952 → 22152 y `uc` 27,09 → 27,16), igual que en la r03.
- **Inversiones de mis casos de la r03:** son las previstas y ninguna se relaja.
  - H-17: `SIN_RESULTADO` y en ningún archivo.
  - H-14: True.
  - H-15: los dos falsos positivos pasan.
  - H-16: se añaden un aviso exacto y `reservas_en_curso` con el `pid`.
- **Prueba de la r02 ajustada** (`credencial_ref` con texto, que ahora se bloquea): es coherente con H-17. `credencial_ref` es un campo de la respuesta del Broker, no de una solicitud.

### Las cuatro correcciones, atacadas

| Hallazgo | Ataques | Resultado |
| --- | --- | --- |
| H-14 | `_` en mayúsculas, dos escapes en la misma clave, `\/` y la clave con un espacio, todo en un JSON ilegible; y un JSON ilegible corriente con `é` y sin el campo | los cuatro, sensibles; el corriente, no: **corregido** |
| H-15 | Dirección `0x` de 40 con una coma detrás o en mayúsculas | pasa |
| H-15 | `0x` con 41 caracteres; LEI en minúsculas; LEI seguido de un secreto | bloqueados |
| H-15 | Dirección dentro de una URL de etherscan bajo `token` | bloqueada: falla cerrado aceptable, fuera del formato canónico |
| H-15 | Clave `0x` de 64 y LEI con un módulo erróneo (pruebas del implementador) | bloqueados: **corregido** |
| H-16 | `pid` `None`, `"123"`, `-5` o `True` | `SIN_PRESUPUESTO` y `reservas_en_curso` correctos, sin aviso: no se puede saber si el proceso vive |
| H-16 | `pid` muerto | un solo aviso, aunque haya C4 los días 0, +3 y +6 |
| H-16 | C4 del día +7 | COMPLETO, y la fecha del aviso es esa |
| H-16 | SIGKILL (mi prueba de la r03) | un aviso; la reserva no se libera: **corregido** |
| H-17 | Campo de más anidado, clave `pass` + espacio de anchura cero + `word`, lista en un campo de más, booleano y nota | bloqueados |
| H-17 | Nominal con `urgencia: ALTA` | pasa: **corregido**, salvo H-18 |

**Desviación de H-15 (no se aplica en el barrido del retorno entero):** la acepto.
- La pedía mi propia prueba `lei_en_finalista_con_solicitud`, así que mi corrección de la r03 y mi prueba se contradecían.
- Queda del lado de la seguridad (falla cerrado) y está declarada en INC-T177-01.

### Hallazgo nuevo

| ID | Gravedad | Cómo reproducirlo | Esperado / obtenido | Corrección exacta | Estado |
| --- | --- | --- | --- | --- | --- |
| H-18 | baja | `r03c_ataques_cierre.py::test_r03c_HALLAZGO_H18_campo_admitido_que_no_se_copia` (3 casos) | **Esperado** (H-17): en una solicitud, solo lo que el Coordinador lee. **Obtenido:** se emite el CT-25 sin el valor, pero un valor corto (`Hunter2x!`) queda en la caché y en la cinta en tres sitios que la lista admite y `desde_retorno` no copia: (a) `urgencia` con un texto que no es ALTA ni NORMAL (el Coordinador lo reduce a NORMAL); (b) `impacto` junto a `impacto_si_falta` (se lee el segundo); (c) `Servicio` junto a `servicio`. Las dos normalizan igual y solo se lee la literal. | En `contratos._subarbol_sensible`, para cada dict del subárbol: (1) comparar la clave **literal**, sin normalizar, con `CAMPOS_SOLICITUD_LITERALES = frozenset({"servicio", "motivo", "impacto_si_falta", "impacto", "urgencia"})`: son los nombres exactos que lee `desde_retorno`, así que una grafía distinta con contenido es sensible; (2) es sensible `urgencia` con contenido que no sea exactamente `"ALTA"` ni `"NORMAL"`; (3) es sensible `impacto` con contenido si el dict también tiene la clave `impacto_si_falta`. Declararlo en INC-T177-01 junto a H-17. Regresión: invertir los tres casos de H-18 (`donde == []` y `SIN_RESULTADO`) y que el nominal (`urgencia: ALTA`), `test_t177` y `r03_ataques_regla_comun.py` sigan en verde. | abierto |

### Veredicto

**Pendiente de otra ronda de cierre.**
- H-14 a H-17 están corregidos y verificados.
- Queda abierto H-18 (bajo, de la misma familia que H-17). Por la regla del operador no puede quedar ningún hallazgo abierto ni ir a la deuda.
- Cuando se corrija, el revisor vuelve a pasar `r03c_ataques_cierre.py`, con H-18 invertido, y `r03_ataques_regla_comun.py`, y da el veredicto final.
- No se cierra el ticket; el README y la deuda no se tocan.

## Verificación de la segunda ronda de cierre (H-18)

- **Revisor y fecha:** claude, el mismo de la r02 y la r03 (no implementó) · 18-11-2026.
- **Reproducción:** worktree nuevo y limpio del commit `3406cb2` (sobre `5f98163`), con el venv del repo.
- **Lo que no he vuelto a pasar**, por orden del encargo: la suite completa, el gate y los mutantes del implementador.
- **Script nuevo:** `revisores/r03d_cierre2.py` (22 casos), ejecutado desde `bloque_a/11_Ejecutor`.

### Re-ejecución

- **Pruebas del ticket y scripts de los revisores:** 184 passed. Incluye `test_t177`, r01, r02, la concurrencia, `r03_ataques_regla_comun.py` y `r03c_ataques_cierre.py`, con H-18 invertido como estaba previsto (`SIN_RESULTADO` y en ningún archivo).
- **Vecinas:** 222 passed. Son las suites R8 (T-103, T-120, T-123, T-130, T-136), `test_v51`, T-174 y T-178.
- **Corpus:** `r03_corpus_formatos.py` da 97 objetos y 0 bloqueados, con la lista vacía y con una solicitud.
- **Falsos positivos:** `r02_falsos_positivos.py texto`, con los 12 perfiles, queda COMPLETO y con 0 bloqueos en V5 y en V6.
- **Retorno legítimo del simulado:** `ciclo_mock_t177.sh` (PB-58 de punta a punta por la CLI) da OK. El simulado del BFA emite `urgencia: NORMAL` y no le afecta el cambio.

### H-18 y el cambio de comportamiento, atacados

- **Urgencia** (`test_r03d_urgencia`).
  - `ALTA`, `NORMAL`, vacía, `None` y `False` pasan.
  - `alta`, `Alta`, ` ALTA`, `ALTA `, `MEDIA` y `0` rechazan el retorno entero.
  - Acepto ese cambio como falla cerrado declarado en INC-T177-01. Las razones:
    - la instrucción del C4 pide literalmente `ALTA|NORMAL`;
    - los prompts de los Analistas no usan `urgencia`;
    - el simulado emite `NORMAL`;
    - el coste es una C4 que se repite.
- **`impacto` y claves literales** (`test_r03d_literales_e_impacto`).
  - Se copia, y pasa: `impacto` solo, o `impacto` vacío junto a `impacto_si_falta`.
  - Es sensible: `impacto` con `impacto_si_falta` presente pero vacío, y `Servicio` en lugar de `servicio`. Es coherente con lo que lee `desde_retorno` (`s.get("impacto_si_falta", s.get("impacto"))`).
  - Una clave de más con `None` pasa.
- **Conclusión:** H-18 queda corregido.

### El mutante M08 retirado como equivalente

No lo es.
- **Qué llega a la línea.** Una urgencia sin contenido (`" "`, `[""]`, `{"": ""}`) pasa la barrera (`_tiene_texto` y `_tiene_numero` dan False) y llega a `desde_retorno`.
  - El código actual la reduce a `NORMAL`.
  - Con M08 (`urgencia = s.get("urgencia") or "NORMAL"`), la CRD- de F5 y el CT-25 al Broker llevan `" "`, `[""]` o `{"": ""}`.
- **Comprobación.** Apliqué M08 en mi copia:
  - `test_t177_c4_credenciales.py` y `test_v51.py` siguen en verde (96 passed), así que el mutante sobrevive;
  - `test_r03d_HALLAZGO_H19_m08_no_es_equivalente` lo mata (3 fallos);
  - después restauré el archivo.

| ID | Gravedad | Cómo reproducirlo | Esperado / obtenido | Corrección exacta | Estado |
| --- | --- | --- | --- | --- | --- |
| H-19 | baja | Aplicar M08 en `interfaz_broker.py` y pasar `test_t177` (96 passed con `test_v51`) y `r03d_cierre2.py::test_r03d_HALLAZGO_H19_m08_no_es_equivalente` (3 fallos) | **Esperado:** un mutante se retira solo si es equivalente. **Obtenido:** M08 no lo es (una urgencia sin contenido llega a la línea) y ninguna prueba del ticket lo mata. | Volver a poner M08 en `mutantes_t177.py`, tal como estaba en `5f98163`. Añadir a `tests/test_t177_c4_credenciales.py` una prueba parametrizada con `urgencia` `" "`, `[""]` y `{"": ""}`: `desde_retorno` da SOLICITADA y la CRD- (y el CT-25) llevan `urgencia == "NORMAL"`. Sirve el cuerpo de `test_r03d_HALLAZGO_H19_…`. Regresión: los mutantes con M08 muerto (42 de 42). | abierto |

### Veredicto

**Pendiente de otra ronda de cierre.**
- H-18 está corregido.
- Queda abierto H-19, un bajo de la batería de pruebas, no del código de producción. Por la regla del operador no puede quedar ningún hallazgo abierto.
- Con H-19 corregido, el revisor vuelve a pasar `mutantes_t177.py` (M08 muerto) y `r03d_cierre2.py`, y cierra la tarea.
- El README y la deuda no se tocan.

## Verificación de la tercera ronda de cierre (H-19) y veredicto final

- **Revisor y fecha:** claude, el mismo de la r02 y la r03 (no implementó) · 18-11-2026.
- **Reproducción:** worktree nuevo y limpio del commit `23764fd` (sobre `3406cb2`), con el venv del repo. Por orden del encargo, sin suite completa ni `check_all.sh`: el 12/12 y las cuotas son los que da el implementador.
- **Código de producción:** sin cambios frente a `3406cb2`. Solo cambian el mutante, una prueba, el mapa y la documentación.
- **`mutantes_t177.py`:** 42/42 muertos, M08 incluido. El script restaura los archivos: el worktree queda limpio.
- **Comprobación aparte de M08:** con M08 aplicado a mano, `test_t177_cierre3_h19_urgencia_sin_contenido_se_reduce_a_normal` falla en los tres casos (`" "`, `[""]` y `{"": ""}`). Después restauré el archivo.
- **Pruebas y scripts de los revisores:** `test_t177_c4_credenciales.py`, `r03d_cierre2.py`, `r03c_ataques_cierre.py` y `r03_ataques_regla_comun.py` dan 155 passed.
- **La afirmación de equivalencia de M08:** ya no queda como afirmación vigente. Solo aparece como antecedente marcado como error, en `pruebas.md`, `handoff.md` y `analisis-tecnico.md`, y en este informe como H-19.
- **Hallazgos:** ninguno nuevo. H-01 a H-19 están todos corregidos y verificados con los scripts de `revisores/`. Nada va a la deuda.

### Veredicto final

**APTO** (QA r03 tras sus rondas de cierre), sin ningún hallazgo abierto.
- PB-58 queda **Superada con su preparación**: con la lista `credenciales.servicios_bfa` vacía por defecto, en un run real el C4 no llama al BFA.
- Declarar esa lista sigue siendo un pendiente del operador, en T-179.
