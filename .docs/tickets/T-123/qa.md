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

**Sin comprobar:** el gate entero; las suites de A-Forex y B (el Forex tiene su propia copia de `RE_SECRETO` y no se toca); mensajes de un ciclo con el modelo real.
