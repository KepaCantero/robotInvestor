# T-123 · QA independiente

- **Revisor:** subagente revisor nuevo, sin contexto de la implementación (Claude; implementó otra sesión de Claude) · **Ronda:** r01 · 2026-11-14
- **Copia revisada:** `git worktree` con HEAD separado en `63d6ae9`; el código de T-123 está en `b9f745a` («wip local: T-123») y `1455b03` («T-123 corregido»): `bloque_a/11_Ejecutor/bloque_a/contratos.py` y `tests/test_t123_r8_iban_y_tarjetas.py`.
- **Orden de lectura:** `README.md` → diff de `contratos.py` y la prueba → mis scripts → al final `analisis-tecnico.md`, `pruebas.md` e INC-T123-01.

## Reproducción desde limpio

Desde la raíz de la copia, con `.venv` enlazado al del repositorio. Lo marcado «leído» está deducido del código; el resto, ejecutado.

| Comprobación | Orden | Resultado |
| --- | --- | --- |
| Banco propio de IBAN y tarjetas | `.venv/bin/python -I .docs/tickets/T-123/revisores/r01_01_banco_iban_tarjetas.py` | **9/11**. Ver CA-1 a CA-3, H-01 y H-02 |
| CT-04, CT-03 y CT-23; salidas del ciclo | `.venv/bin/python -I .docs/tickets/T-123/revisores/r01_02_caminos_r8.py bloque_a/11_Ejecutor <salida del ciclo V5>` | **31/31**: 5 datos (Visa, Amex, IBAN DE, FR y GB) × 3 formas × 3 contratos rechazados, ningún archivo con el dato; en las 13 380 líneas que deja el backtest simulado (983 huellas hexadecimales de 32 a 64), ningún falso positivo |
| Efecto de H-01 y H-02 en un CT-04 | `.venv/bin/python -I .docs/tickets/T-123/revisores/r01_03_efecto_en_ct04.py` | **0/5**: ver H-01 y H-02 |
| Ciclo V5 antes y después | `r01_06_regresion_ciclo.py` de la QA de T-118 («antes» = `00ed8d3`, sin T-122 ni T-123) | 56 de 57 ficheros idénticos byte a byte, `consumo.csv` igual salvo latencias: **ningún rechazo nuevo** |
| Goldens de contratos | `cd bloque_a/11_Ejecutor && ../../.venv/bin/python tests/goldens_ct.py` | «goldens de contratos: coinciden» |
| Gates ligeros, ruff y mypy | `tools/corpus_integridad.py`, `refs_vivas.py`, `secrets_scan.py`, `nfc_check.py`; ruff y mypy contados como el gate | En verde; ruff **2902**, mypy de A **109** (las cuotas) |
| Suite de A | una vez, al final (común a los cuatro tickets) | Ver «Suite» al final |

## Criterios de aceptación

| Criterio | Cumple | Evidencia |
| --- | --- | --- |
| CA-1 | sí | Un IBAN válido generado para **cada uno de los 42 países** de `LONGITUD_IBAN` y 12 de ejemplo publicados (DE, GB, FR, NL, IT, AT, MT, NO, BR, ES, PL, SA), en 14 formas (junto, grupos de 4, espacio duro, espacio fino, guiones, puntos, minúsculas, dos espacios, salto de línea, tabulador, JSON escapado con ` ` y con `\n`, tras «IBAN:», entre paréntesis): **todos detectados**. 128 inválidos (control cambiado, dígitos de control cambiados, longitud de país menos uno, país inexistente): **ninguno** marcado |
| CA-2 | sí | Tarjetas de prueba de Visa (16, 13 y 19), Mastercard (51–55 y serie 2), Amex, Discover, JCB y UnionPay: detectadas juntas, en grupos de 4, con guiones, con espacio duro, Amex en 4-6-5, en JSON y tras «tarjeta:», siempre enmascaradas («tarjeta …1111»); con el Luhn mal, ninguna. No se detectan (declarado en `analisis-tecnico.md`): con puntos o con dos espacios; Diners y Maestro (redes no cubiertas) |
| CA-3 | sí en sus términos; ver H-02 | Ninguno en 6 000 decimales, 2 000 decimales con coma, 4 000 en notación científica, 3 000 fechas y rangos, 3 000 fechas compactas, 4 000 marcas de tiempo, 6 000 teléfonos (+34, 0034, +1), 3 000 importes con puntos de miles, 14 ISIN y CUSIP y 3 000 identificadores del sistema. Pero sí en **huellas SHA-256** (2 de 6 000; 28 de 100 000), **UUID** (1 de 3 000), importes con espacio de miles de 15 cifras (6 de 3 000), listas de enteros separadas por espacios (35 de 5 000) y cuatro grupos de 4 cifras al azar (94 de 5 000, que son indistinguibles de una tarjeta: no lo cuento como defecto) |
| CA-4 | sí | `r01_02`: CT-04, y también CT-03 (pregunta y contexto) y CT-23 (envío), con Visa, Amex e IBAN DE, FR y GB en tres formas: los 45 rechazados y el dato en ningún archivo del Almacén |
| CA-5 | sí, salvo el gate entero | Goldens sin cambios; ciclo simulado sin rechazos nuevos (idéntico); corpus, referencias, secretos, NFC, ruff y mypy en verde. `./tools/check_all.sh` entero no lo he lanzado (por instrucción); la suite, abajo |

Coste: lineal. Con 50 000 y 200 000 caracteres de cinco texturas hostiles (cifras y separadores, letras y cifras, decimales, guiones, espacios duros), la razón de tiempos es 3,9 a 4,2 para ×4 de tamaño; 200 000 caracteres en < 0,08 s. Leído: los dos patrones nuevos tienen repeticiones acotadas ({10,30} y {12,18}) y el control es lineal en el candidato.

## Hallazgos

| ID | Gravedad | Cómo reproducirlo | Esperado / obtenido | Corrección sugerida | Estado |
| --- | --- | --- | --- | --- | --- |
| H-01 | media | `.venv/bin/python -I .docs/tickets/T-123/revisores/r01_03_efecto_en_ct04.py` (bloque a) y `r01_01` («contextos»). A mano: `tarjetas_en_texto("4111 1111 1111 1111 12/27")` → `[]`; `ibanes_en_texto("DE89" + "370400440532013000" + " 15")` → `[]` | **Esperado:** una tarjeta o un IBAN se detectan con lo que suele acompañarlos. **Obtenido:** no se detectan (y el CT-04 se acepta y el dato queda en `estado/F5_historial_analisis.jsonl`) una tarjeta seguida de su **caducidad** («… 1111 12/27») o de su **CVV** («… 1111 123»), un IBAN extranjero **seguido de una cifra** («IBAN DE89 … 00 15 de noviembre», «IT60 … 3 cuotas», «… 2 recibos»), uno **precedido de un código de 2 letras y 2 cifras** («Ref AB12 DE89 …», «ID QA42 …») y uno con tres espacios entre grupos. Causa (leído): los dos patrones son voraces y el control se aplica a la coincidencia entera; si la serie de al lado cabe en el patrón (hasta 19 cifras, hasta 34 caracteres), el candidato crece, falla el control y la cuenta de dentro ya no se prueba (`finditer` no solapa). El IBAN español sí se detecta en esos casos (tiene su patrón propio). La línea «un IBAN seguido de otra cifra ya no se marca (era otra serie)» del registro lo hace a propósito, pero no está entre los límites declarados | Probar, dentro de cada candidato, las ventanas con la longitud de su país (IBAN) o de 13 a 19 cifras (tarjeta) que empiezan y acaban en un límite de grupo, y marcar si alguna pasa el control; o partir el candidato por los separadores y probar las uniones de grupos consecutivos. Prueba: caducidad, CVV, IBAN + cifra, prefijo AB12 | abierto |
| H-02 | alta | `r01_03` (bloque b): un CT-04 con un comentario que cita la huella `5d8f6cce…d5518a86` (el SHA-256 de un número, como las que escribe el sistema) se **rechaza** como dato sensible («tarjeta …3400»). `r01_01` bloque 3: huellas SHA-256 en hexadecimal, 28 de 100 000; en mayúsculas igual; UUID 1 de 3 000 | **Esperado:** una huella, un UUID o un identificador hexadecimal no son una tarjeta. **Obtenido:** `RE_CANDIDATO_TARJETA` solo excluye una cifra, un punto o una coma antes y después, así que un tramo de 13 a 19 cifras **entre letras** de una huella hexadecimal cuenta; con prefijo de red y Luhn (≈ 1 de 3 600 huellas) el mensaje se rechaza (falla cerrado, pero rechaza un mensaje legítimo, o vacía la respuesta del modelo con `contenido_sensible`). En el ciclo simulado ninguna de las 983 huellas que quedan en las salidas casó (lo esperable con esa tasa), pero los mensajes y contextos del sistema llevan huellas y claves de idempotencia: en semanas de modo sombra acabará saliendo | Exigir también que no haya una letra ni un dígito pegados antes y después (`(?<![0-9A-Za-z.,])` … `(?![0-9A-Za-z]|[.,][0-9])`); prueba con 100 000 huellas y UUID | abierto |
| H-03 | baja | `cat .docs/tickets/T-123/pruebas.md` | **Esperado:** el informe de la fase de pruebas (`ri-probar`) con suites antes y después, criterio → prueba, regresiones y gate. **Obtenido:** sigue siendo la plantilla («…», «<Para cada una…>»); `analisis-tecnico.md` es muy breve y la suite completa y el gate 12/12 que pide CA-5 no constan en ningún sitio del ticket | Rellenar `pruebas.md` con lo ejecutado | abierto |
| H-04 | baja | `r01_01` bloque 3 | Falsos positivos que no son de huellas: importes con espacio como separador de miles y 15 cifras que empiezan por 34/37 («372 436 879 280 739 €», 6 de 3 000) y listas de enteros con espacios («40 74 11 29 97 4 89 48 49 75 95», 35 de 5 000). Raros en los mensajes del sistema; no los cuento como defecto, pero no están entre los límites declarados | Declararlos en INC-T123-01 (o exigir que los grupos tengan 4 cifras, salvo el 4-6-5 de Amex) | abierto |

## Suite

`cd bloque_a/11_Ejecutor && ../../.venv/bin/pytest -q -p no:cacheprovider` (una sola vez, en la copia `63d6ae9`, común a T-119 r02, T-121, T-122 y T-123): **5663 passed** en 23 min 43 s, código de salida 0 (línea base 607).

## Veredicto

**NO APTO.**

Los cinco criterios se cumplen en sus términos (CA-5 sin el gate entero) y lo que se pidió está bien hecho: los IBAN de los 42 países de la tabla, en 14 formas, y las tarjetas de las seis redes se detectan; los inválidos no; CT-04, CT-03 y CT-23 los rechazan sin dejar el dato en ningún archivo; el coste es lineal; los goldens no cambian y el ciclo simulado no tiene rechazos nuevos.

Pero queda un hallazgo **alto**, **H-02**: el patrón de tarjeta marca tramos de cifras **dentro de huellas SHA-256 y UUID** (≈ 1 de cada 3 600 huellas), así que T-123 introduce rechazos de mensajes legítimos que antes pasaban; es la misma clase de falso positivo que el implementador ya juzgó bloqueante con los decimales del ciclo, y el sistema escribe huellas en sus mensajes y contextos. La corrección es corta (exigir que no haya letra ni cifra pegada a la serie). Además, **H-01** (media): una tarjeta seguida de su caducidad o su CVV, o un IBAN extranjero seguido de una cifra o precedido de un código como «AB12», no se detectan y el CT-04 deja el dato en F5. **H-03** y **H-04**, bajos (el informe de pruebas está sin rellenar; falsos positivos raros sin declarar).

Vuelve a `ri-implementar`: H-02 y H-01 con sus pruebas (100 000 huellas y UUID sin marcar; caducidad, CVV, IBAN + cifra y prefijo AB12 marcados), y `pruebas.md` rellenado. En la r02 se vuelven a ejecutar `r01_01` a `r01_03`.

**Sin comprobar:** el gate entero; la suite de B; mensajes de un ciclo con el modelo real.

---

# Ronda r02 · 2026-11-15

- **Revisor:** subagente revisor nuevo, sin contexto de la implementación ni de la r01 (Claude; implementó otra sesión de Claude) · **Ronda:** r02
- **Copia revisada:** clon desconectado en `fb3ccd4` (la r02 de T-123 está en ese commit: `contratos.py`, `tests/test_t123_r02.py`, `tests/test_t122_hallazgos.py`, INC-T123-01).
- **Orden de lectura:** `README.md` → diff de `contratos.py` (`d1ff926..fb3ccd4`) → mis scripts → al final `analisis-tecnico.md`, `pruebas.md` e INC-T123-01.

## Reproducción

Desde la raíz de la copia, con `.venv` enlazado al del repositorio.

| Comprobación | Orden | Resultado |
| --- | --- | --- |
| Scripts de la r01 | `.venv/bin/python -I .docs/tickets/T-123/revisores/r01_01_banco_iban_tarjetas.py` | **10/11**: lo que falla son 90 de 5 000 series de cuatro grupos de cuatro cifras al azar (forma de tarjeta, límite declarado en INC-T123-01). Huellas, UUID, importes con espacio de miles y listas de enteros: 0. Coste lineal en las cinco texturas de la r01 |
| | `… r01_02_caminos_r8.py bloque_a/11_Ejecutor <salida de un backtest mock nuevo, 2024-01-05..2024-03-29>` | **31/31**: CT-04, CT-03 y CT-23 con Visa, Amex e IBAN DE, FR y GB en tres formas, rechazados y sin rastro; 13 380 líneas del ciclo (983 huellas de 32 a 64), ningún falso positivo. Recorriendo los ficheros enteros (2,26 M caracteres, no línea a línea), tampoco |
| | `… r01_03_efecto_en_ct04.py` | Bloque a **4/4** (caducidad, CVV, caducidad y CVV, IBAN DE + cifra: CT-04 rechazado, sin rastro). El bloque b se para con `StopIteration`: **es lo esperado**, busca entre 100 000 huellas una que se marque como tarjeta y ya no hay ninguna (H-02 corregido). Lo que medía (que una huella no bloquee un CT-04) lo hago en `r02_01` [5] con la huella que dio la r01 |
| Mi script | `.venv/bin/python -I .docs/tickets/T-123/revisores/r02_01_falsos_r02.py` | **6/12**. Compara con la r01 cargando de `d1ff926` el tramo de patrones de `contratos.py`. Ver H-05 a H-09 |
| Prueba de T-122 cambiada | lectura | Ver «INC-T123-01 y la prueba de T-122» |
| Goldens, gates, cuotas, suite | comunes a T-123, T-124 y T-127 (detalle en «Comunes» de `T-127/qa.md`) | suite de A **5798 passed** (24 min 55 s, código 0); goldens coinciden; ruff 2902; mypy A 109; secretos, referencias, NFC y corpus en verde |

## Hallazgos de la r01

| Hallazgo | Estado | Evidencia |
| --- | --- | --- |
| H-01 (media) | **corregido** | `r01_03` [a] 4/4; `r02_01` [1]: caducidad, CVV, IBAN + cifra, «Ref AB12», tres espacios, detectados |
| H-02 (alta) | **corregido** | 0 de 100 000 huellas SHA-256 (`r02_01` [1]), 0 de 6 000 hex, 3 000 en mayúsculas y 3 000 UUID (`r01_01`); la huella que la r01 encontró pasa y el CT-04 se acepta (`r02_01` [5]) |
| H-03 (baja) | **corregido** | `pruebas.md` rellenado |
| H-04 (baja) | **corregido** | 0 de 3 000 importes con espacio de miles y 0 de 5 000 listas de enteros (`r01_01`); lo que queda (cuatro grupos de cuatro cifras), en INC-T123-01 |

## Criterios de aceptación

| Criterio | Cumple | Evidencia |
| --- | --- | --- |
| CA-1 | sí | `r01_01` [1]: 42 países + 12 publicados en 14 formas, todos; 128 inválidos, ninguno |
| CA-2 | sí | `r01_01` [2]: seis redes en las formas declaradas, enmascaradas; Luhn mal, ninguna |
| CA-3 | sí en sus términos | `r01_01` [3] y `tests/test_t123_*`. Pero ver H-06 y H-07 (falsos positivos fuera de los once textos) |
| CA-4 | sí | `r01_02` 31/31 |
| CA-5 | sí, salvo el gate entero (no lanzado por instrucción) | Goldens coinciden; ciclo simulado sin falsos positivos; suite 5798 passed; cuotas sin subir |

## INC-T123-01 y la prueba de T-122

`test_t122_hallazgos.py` pasa «tres separadores» de «no se marca» a «se marca» y pone «cuatro» en su lugar. Está justificado: el IBAN español no ha cambiado de patrón (`RE_SECRETO` sigue con dos), pero ES está en `LONGITUD_IBAN` y el detector general admite ahora hasta tres separadores (H-01 de la r01), así que un IBAN español válido con tres se detecta por esa vía; INC-T123-01 lo dice («Por coherencia, el IBAN español con tres separadores seguidos también se detecta ahora»). La prueba no se debilita: detecta más. Queda desfasada la frase de INC-T122-01 «Con tres o más seguidos no se detecta» (H-10).

## Hallazgos nuevos

| ID | Gravedad | Cómo reproducirlo | Esperado / obtenido | Corrección sugerida | Estado |
| --- | --- | --- | --- | --- | --- |
| H-05 | media | `r02_01` [2]. A mano: `tarjetas_en_texto("cliente,Juan," + "4111" + "1111" + "1111" + "1111" + ",12/27")` → `[]`; también `"Visa," + …`, `"pago." + …`, `"fin." + "4111 1111 1111 1111"` | **Esperado:** una tarjeta en una fila CSV, o tras una coma o un punto sin cifras delante, se detecta (el IBAN en la misma fila sí se detecta). **Obtenido:** no se detecta. `RE_GRUPOS_TARJETA` excluye con `(?<![0-9A-Za-z.,])` cualquier punto o coma delante, aunque no haya una cifra antes; la intención declarada es «un punto o una coma **con cifras**» (la parte de un decimal), que el lado derecho sí aplica (`[.,][0-9]`). Ya ocurría en la r01; no está entre los límites de INC-T123-01. Un CT-04 o una consulta con datos pegados en CSV deja la tarjeta en F5 | Lookbehind simétrico al de la derecha: `(?<![0-9A-Za-z])(?<![0-9][.,])` (lo he probado: «Visa,…» y «pago.…» pasan a marcarse; «0.4111…», «12,4111…», «…,5» y los decimales del ciclo siguen sin marcar). La fila CSV con un campo detrás que empieza por cifra («…,12/27») sigue sin marcarse por el lado derecho, que no distingue una coma decimal: declararlo en INC-T123-01. Prueba: «Visa,…», «pago.…», «;…;» marcados | abierto |
| H-06 | media | `r02_01` [3] («token de índice + palabras», «ISIN + palabras», «huella truncada de 16 hex») | **Esperado:** un ISIN, un nombre de índice o una huella del sistema no son un IBAN. **Obtenido:** el candidato IBAN encadena **palabras** siguientes hasta la longitud del país y basta el módulo 97 (1 de 97): «ISIN NL3280300684 precio los…», «El SE30 el los bono…», 56 y 61 de 20 000 (≈ 0,3 % por mención). Y las huellas que escribe el sistema (`prompts.huella`, `HT01.huella`: `sha256(...)[:16]`): con «be» + 2 cifras tienen la longitud de BE (16) y 1 de 97 pasa: `"huella": "be52539bd21ffef4"` se marca; con las que son todo cifras y pasan Luhn (tarjeta), 37 de 1 000 000 de huellas de 16 caracteres. `agentes.py:109` bloquea el encargo («Encargo bloqueado por R8», resultado PARCIAL); en un backtest mock de 12 semanas llegan a los contextos de los agentes 50 huellas de 16 distintas (≈ 0,2 % por backtest). Es la clase de H-02 con una tasa menor; la de ISIN e índices ya estaba en la r01 (el corte a media palabra la hacía mayor) | Validar el BBAN con la estructura de su país del mismo registro ISO 13616 (p. ej. BE: 12 cifras; DE: 18 cifras; NL: 4 letras + 10 cifras), que quita casi todos los casos de palabras, ISIN y huellas; la de 16 cifras como tarjeta no tiene arreglo en R8 (es indistinguible): declararla, o que las huellas truncadas lleven un prefijo con letra | abierto |
| H-07 | media | `r02_01` [3] («columna…», «fila…»); comparación con la r01 en la orden de abajo | **Esperado** (README: «sin falsos positivos con las series de cifras corrientes»): una tabla de enteros de cuatro cifras no es una tarjeta. **Obtenido, regresión de la r02:** al probar ventanas en cada grupo y admitir hasta tres separadores (también saltos de línea), una fila de 8 enteros de 4 cifras separados por dos espacios pasa de **0 %** (r01) a **11 %** marcada (555 de 5 000), y una columna de 8 en líneas seguidas de 4,6 % a 11,7 %. Con niveles de índice entre 4 000 y 5 999 (prefijos 4 y 51–55) es plausible en un texto del modelo. INC-T123-01 declara «cuatro grupos de cuatro cifras al azar… unas 2 de cada 100», no las series largas ni las que cruzan líneas | No unir grupos a través de un salto de línea (separador `[ \t   \-]`, no `\s`) y declarar en INC-T123-01 la tasa con series largas; o exigir que la serie entera sea de 13 a 19 cifras con su caducidad o CVV como mucho al final | abierto |
| H-08 | media | `r02_01` [4]: `secretos_en_texto("DE12 " * 200_000)` (1 M caracteres) → **87 s** (250 k: 4 s); `"DE11 " + "1 " * 30` repetido: 17 s | **Esperado** (`analisis-tecnico.md` r02: «El coste sigue siendo lineal»). **Obtenido:** cuadrático. En `ibanes_en_texto`, `for g in grupos[i:]` copia la lista de grupos de la serie desde `i` en cada grupo que empieza como un IBAN, y una serie es todo el texto entre dos signos de puntuación. A tamaños reales es poco (120 000 caracteres: 0,8 s en `secretos_en_texto`, 1,6 s en `contiene_credenciales`), pero es una regresión de la r01 (lineal) en el control R8, y un CT-04 o un texto externo no tienen tope | Recorrer por índice (`for j in range(i, len(grupos))`) o con `itertools.islice`; prueba de tiempo con 1 M caracteres «DE12 » | abierto |
| H-09 | baja | `r02_01` [2]: `ibanes_en_texto("DE89" + "370400440532013000" + "EUR")` y `"… 0130 00EUR"` → `[]`; la r01 los detectaba | **Esperado:** lo que la r01 detectaba, se sigue detectando (o se declara). **Obtenido:** un IBAN cuyo último grupo va pegado a letras ya no se detecta (la ventana tiene que acabar en un límite de grupo). INC-T123-01 declara «seguido de otra cifra pegada», no de letras | Declararlo en INC-T123-01, o admitir que el último grupo se corte en la longitud del país si lo que sigue son letras | abierto |
| H-10 | baja | `grep -n "tres o más seguidos" docs/incidencias.md` | INC-T122-01 sigue diciendo «Con tres o más seguidos no se detecta» del IBAN español; desde la r02 de T-123 se detecta con tres (INC-T123-01 lo dice, pero la de T-122 queda desfasada) | Una nota en INC-T122-01 que remita a INC-T123-01 | abierto |

Orden para comparar con la r01 lo que da H-07 (también lo hace `r02_01`): desde `bloque_a/11_Ejecutor`, cargar el tramo de `git show d1ff926:bloque_a/11_Ejecutor/bloque_a/contratos.py` entre `LONGITUD_IBAN = {` y `def secretos_en_texto` y llamar a su `tarjetas_en_texto` con `"  ".join(str(random.randint(1000, 9999)) for _ in range(8))`.

## Invariantes

- No hay LLM en la ruta: R8 es determinista y sin red. ✔
- Falla cerrado: los falsos positivos rechazan (H-06, H-07); los falsos negativos (H-05, H-09) dejan pasar el dato. ✔ con H-05
- Ningún número a mano: `LONGITUD_IBAN` es el registro ISO 13616 (dato de un estándar, INC-T123-01); 13–19 cifras, prefijos de red, «grupos de al menos 4» y «hasta 3 separadores» son reglas del formato declaradas en INC-T123-01. ✔
- Nada de secretos: los números de prueba van partidos en mis scripts; `tools/secrets_scan.py` en verde con ellos. ✔
- Contratos y estado persistido sin cambios: goldens coinciden. ✔

## Veredicto r02

**APTO.**

Los cuatro hallazgos de la r01 están corregidos (H-02, el alto, con 0 de 100 000 huellas y 0 de 3 000 UUID) y los cinco criterios se cumplen (CA-5 sin el gate entero, que no lancé por instrucción; pasó en el commit). No queda ningún hallazgo crítico ni alto. Quedan cuatro medios y dos bajos, que pasan a la deuda con su ID: **H-05** (tarjeta tras una coma o un punto sin cifras, p. ej. una fila CSV, sin detectar), **H-06** (IBAN «encadenado» con palabras tras un ISIN o un nombre de índice, ≈ 0,3 % por mención, y huellas truncadas de 16 caracteres del sistema, ≈ 4 de cada 100 000), **H-07** (regresión de la r02: series de enteros de cuatro cifras separadas por dos espacios o saltos de línea, del 0 % al 11 %), **H-08** (coste cuadrático de `ibanes_en_texto`, contra lo que dice `analisis-tecnico.md`), **H-09** y **H-10** (bajos). H-05 y H-08 tienen una corrección de una línea; conviene hacerlas antes del modo sombra.

**Sin comprobar:** el gate entero; B; mensajes de un ciclo con el modelo real; las redes Diners y Maestro y el formato con puntos (fuera de lo declarado, como en la r01).
