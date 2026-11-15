# T-133 · QA independiente

# Ronda r01 · 2026-11-15

- **Revisor:** subagente revisor nuevo, sin contexto de la implementación (Claude; implementó otra sesión de Claude) · **Ronda:** r01
- **Copia revisada:** copia git desconectada en `197aaca` (instantánea para QA de T-131 r02, T-133 y T-134). El `contratos.py` de T-130 (commit anterior, `aa30b2e`) para comparar y los mutantes, en una copia desechable dentro del scratchpad («qa14_mut»), ya borrada.
- **Orden de lectura:** README → diff de `contratos.py` (`ESTRUCTURA_BBAN`, `RE_BBAN`, `_bban_plausible`, `_misma_caja`, `GRUPOS_FILA_DE_TABLA`), de `estimar_coste_ciclo_a.py` y de `precios_anthropic.yaml` → `llm.AnthropicClient.generar` (bucle de `pause_turn`) y `agentes.py` (reparación de JSON) → las QA r01 de T-129 y T-130 y sus scripts → INC-T123-01 e INC-T129-01 → mis scripts → al final `analisis-tecnico.md` y `pruebas.md`.

## Reproducción desde limpio

Desde la raíz de la copia, con el intérprete del repositorio (`py`). `<doce>` y `<div>`: carpetas nuevas de `medir_consumo_a.py` (cliente simulado, sin coste) en el scratchpad, con `perfiles.activos` de los 12 tipos en un YAML aparte y con la configuración de por defecto.

| Comprobación | Orden | Resultado |
| --- | --- | --- |
| Medición, 12 tipos y solo divisas | desde `bloque_a/11_Ejecutor`: `py ../../.docs/scripts/medir_consumo_a.py <doce> 2024-03-29 --config <doce.yaml>` y `… <div>` | 77 y 8 llamadas |
| Tabla del README | `py .docs/scripts/estimar_coste_ciclo_a.py <doce> --config <doce.yaml>` y `… <div>` | **2,98–22,60 USD (120 búsquedas)** y **0,86–2,11 USD**: coincide |
| CA-2 · T-130 `r01_01_registro_y_formatos.py` | `py -I .docs/tickets/T-130/revisores/r01_01_registro_y_formatos.py` | **17 ok, 1 fallo**: «17,<tarjeta>,12/27» (H-04 de T-130, declarado en INC-T123-01) |
| CA-2 · T-130 `r01_02_comparacion_r02.py` | `py -I …/T-130/revisores/r01_02_comparacion_r02.py` | filas de 8 números de 4 cifras: 0/5000 con un espacio, dos y salto de línea; 4 enteros de 4 cifras al azar: 536/20000 (2,7 %, INC-T123-01 dice «unas 3 de cada 100») |
| CA-2 · T-123 `r02_01_falsos_r02.py` · `r01_02_caminos_r8.py` | `py -I …/T-123/revisores/…` | **12/12** · **30/30** |
| T-123 `r01_01_banco_iban_tarjetas.py` | `py -I …/T-123/revisores/r01_01_banco_iban_tarjetas.py` | 9/11, como dice `pruebas.md`: los 11 «válidos» con BBAN solo de cifras en países que piden letras (BG, BR, GB, GI, IE, IT, LV, MT, NL, RO, SM) y las series de 4 grupos de 4 cifras al azar |
| CA-3 · T-129 `r01_02_sensibilidad_cota.py` | `py -I …/T-129/revisores/r01_02_sensibilidad_cota.py <doce> --config <doce.yaml>` | mayor escenario **20,78** (c, `pause_turn`); a 16,90, b 19,62, a+b 19,62; Haiku: prompt máximo 12 875 tokens. Todos por debajo de 22,60 |
| Mi script 1 | `py -I .docs/tickets/T-136/revisores/r01_01_iban_tarjetas_formas.py <contratos.py de T-130>` | **19 ok, 7 fallos** (H-02, H-03) |
| Mi script 2 | `py -I .docs/tickets/T-136/revisores/r01_02_cota_por_peticion.py <doce> --config <doce.yaml>` y `… <div>` | 12 tipos: **25,19 USD** contando la salida de cada petición (+11,5 % sobre la cota) y **56,79** con la reparación de JSON (+151 %); solo divisas: 2,11 y 4,58 (H-01) |
| Mi script 3 (mutantes) | `py .docs/tickets/T-136/revisores/r01_03_mutantes.py <copia «qa14_mut»>` | **12 de 16 muertos**; vivos C03, C06, C08, C12 (H-04) |
| Suite, goldens, gates y cuotas | comunes (ver «Comunes» en `T-131/qa.md`, ronda r02) | 6048 passed; goldens coinciden; ruff 2838; mypy 109; gates ligeros en verde |

### `ESTRUCTURA_BBAN`, país a país

Comparé las 42 entradas con el registro de IBAN de SWIFT (ISO 13616) tal como lo conozco: AD 4n4n12c, AE 3n16n, AT 5n11n, BE 3n7n2n, BG 4a4n2n8c, BR 8n5n10n1a1c, CH 5n12c, CY 3n5n16c, CZ 4n6n10n, DE 8n10n, DK 4n9n1n, EE 2n2n11n1n, ES 4n4n1n1n10n, FI 3n11n, FR 5n5n11c2n, GB 4a6n8n, GI 4a15c, GR 3n4n16c, HR 7n10n, HU 3n4n1n15n1n, IE 4a6n8n, IL 3n3n13n, IS 4n2n6n10n, IT 1a5n5n12c, LI 5n12c, LT 5n11n, LU 3n13c, LV 4a13c, MC 5n5n11c2n, MT 4a5n18c, NL 4a10n, NO 4n6n1n, PL 8n16n, PT 4n4n11n2n, RO 4a16c, SA 2n18c, SE 3n16n1n, SI 5n8n2n, SK 4n6n10n, SM 1a5n5n12c, TR 5n1n16c, VA 3n15n. **Las 42 coinciden**, cada una suma la longitud de `LONGITUD_IBAN` (las dos tablas tienen los mismos 42 países) y `BBAN_NUMERICO` sale con los 21 de solo cifras, VA incluido. Sin acceso al registro en esta sesión: es mi conocimiento del estándar, no una descarga.

### Lo que dice mi script 1 (IBAN al azar con su control, 30 por país y forma, en los 41 países sin ES)

| Forma | Sin detectar en T-133 | Juicio |
| --- | --- | --- |
| junto, grupos de 4, minúsculas, en una frase tras «IBAN:», espacio duro, seguido de «EUR» | **0** | correcto (en T-130 se perdían los que llevan letras en un tramo «c»: es H-01 de T-130, corregido) |
| formatos nacionales: BE 3-7-2, FR RIB 5-5-11-2, IT con el CIN suelto, PT 4-4-11-2 y PT en grupos de 4 con el último de 1 cifra | **0** | correcto |
| HU por sus tramos (3-4-**1**-15-1) y TR (5-**1**-16) | 50 de 50 | H-03: la cifra suelta en un grupo intermedio corta el IBAN; T-130 detectaba los dos (0 de 50 sin detectar) |
| país en mayúsculas y el resto en minúsculas («GB82 west …»), o tipo título («Gb82 West …») | BR, GB, IE, MT y NL que T-130 sí detectaba | H-03: efecto de `_misma_caja` |
| falsos positivos: 126 000 identificadores al azar «país + 2 cifras + alfanuméricos en mayúsculas» | 32 marcados (T-130: 42), en GI, LU, LV, RO y SA | correcto: la estructura no dispara los falsos positivos aunque admite más letras que el tope de T-130 |

## Criterios de aceptación

| Criterio | Cumple | Evidencia |
| --- | --- | --- |
| CA-1 | sí | `test_t133_r8.py` (12) y `test_t133_coste.py` (5), las vecinas de R8 y `test_t129_modo_sombra.py`, dentro de la suite completa: 6048 passed |
| CA-2 | sí | T-130 `r01_01` 17/18 (solo H-04, declarado); `r01_02` como dice el README; T-123 `r02_01` 12/12 y `r01_02` 30/30 |
| CA-3 | sí, salvo el gate entero (no lanzado por instrucción) | 22,60 USD frente al mayor escenario de `r01_02_sensibilidad_cota.py`, 20,78; goldens coinciden. Pero ver H-01: hay un escenario que el script de T-129 no prueba |

## Hallazgos de las QA r01 de T-129 y T-130

| ID | Estado | Evidencia |
| --- | --- | --- |
| T-130 H-01 (media) | **corregido** | mi script 1 [1]: 0 sin detectar en las seis formas corrientes de los 41 países, con letras en los tramos «c»; RO, LV, CY e IT con letras en T-130 `r01_02` |
| T-130 H-02 (media) | **corregido**, con un coste (H-02 de esta ronda) | filas de 5, 6 y 8 números de 4 cifras: 0/3000 (T-130: 429, 645 y 950) |
| T-130 H-03 (baja) | **corregido** | `BBAN_NUMERICO` derivado: 21 con VA |
| T-130 H-04 (baja) | declarado | INC-T123-01 (T-133) |
| T-130 H-05 (baja) | **corregido** | `test_h05_…` y C02 muere |
| T-129 H-01 (media) | **en parte** (H-01 de esta ronda) | la cota ya paga la entrada como escritura, con 1,35 y las vueltas de `pause_turn`; no cuenta la salida de cada vuelta |
| T-129 H-02 (baja) | **corregido** | «suelo» en el script, en el README y en INC-T129-01 |
| T-129 H-03 (baja) | **corregido** | `test_h03_…` (dos pruebas) |

## Hallazgos nuevos

| ID | Gravedad | Cómo reproducirlo | Esperado / obtenido | Corrección sugerida | Estado |
| --- | --- | --- | --- | --- | --- |
| H-01 | media | mi script 2 (orden de arriba); mutante K04 | **Esperado** (README; INC-T129-01; la QA r01 de T-129, H-01: «una llamada de un agente con búsqueda puede ser 4 peticiones, **cada una con su entrada y hasta `max_tokens` de salida**»): la cota acota lo que el cliente real puede pedir, salvo lo que dice que no incluye (lo que lee cada búsqueda, reintentos, reparaciones de JSON). **Obtenido:** `estimar()` cobra `vueltas ×` la entrada pero **una sola vez** `max_tokens` de salida, y `test_h01_la_cota_cubre_…` lo fija («+ 0,1 M de salida (1)» con 4 vueltas; K04, que cobra la salida por vuelta, muere). En `AnthropicClient.generar` cada continuación es un `messages.create` con su propio `max_tokens` y reenvía como entrada el contenido del asistente de la anterior. Con eso, sin contar lo leído por las búsquedas (declarado fuera): **25,19 USD** con los 12 tipos (+11,5 % sobre 22,60). Además, «reparaciones de JSON» no es un desconocido: `llm.reintento_reparacion` = 1 está en la configuración, y con una reparación por llamada la cifra es 56,79 USD (solo divisas: 4,58 frente a 2,11). El escenario c del script de T-129 sí contaba la salida por vuelta, pero con las lecturas de caché del simulador; a+b+c juntos no se probaban | Cobrar `vueltas × max_tokens` de salida y, en la entrada de la vuelta k, k × `max_tokens` más (la salida reenviada); llamar «cota» a la cifra con `(1 + reintento_reparacion)` llamadas (o decir en README e INC-T129-01 que es «cota sin reparaciones» y dar las dos); actualizar `test_h01_…` y la tabla del README | abierto |
| H-02 | media | mi script 1 [4]; mutante C12 | **Esperado** (INC-T123-01, ronda r02 de T-123: «lo que va al lado (caducidad, CVV, una cifra, un código "AB12") no esconde el dato»). **Obtenido:** con `GRUPOS_FILA_DE_TABLA` = 5, una tarjeta válida en grupos de 4 seguida o precedida de **otro número de 4 cifras** con un espacio o un guion deja de detectarse: «<tarjeta> 0128» (caducidad MMAA), «2026 <tarjeta>», «<tarjeta con guiones>-0128» y dos tarjetas seguidas en una línea: 0 de 50 en cada caso (T-130: 50 de 50). Con «12/27», un CVV de 3 o «1234 123» se sigue detectando. Es una regresión de un control que debe fallar cerrado, a cambio de los falsos positivos de H-02 de T-130 (que bloqueaban mensajes, fallo cerrado). INC-T123-01 dice la regla («cinco o más números de cuatro cifras seguidos son una fila de tabla») pero no su consecuencia, y contradice lo que la ronda r02 de T-123 dejó escrito | O mirar, en una serie de 5 o más grupos de 4, al menos las ventanas pegadas a sus extremos (una tarjeta junto a un número antes o después), o subir el umbral a 6 (una tarjeta con un vecino a cada lado queda fuera, pero las filas de 5 vuelven a marcarse: medirlo); en todo caso, decir en INC-T123-01 qué deja de detectarse (MMAA sin barra, un año delante, dos tarjetas seguidas) y añadir la prueba de 5 grupos (C12 vive) | abierto |
| H-03 | baja | mi script 1 [1] y [2] | **Esperado:** T-133 no pierde IBAN que T-130 detectaba, salvo lo declarado. **Obtenido:** (a) `_misma_caja` deja fuera los IBAN con el país en mayúsculas y el resto en minúsculas («GB82 west …») o en tipo título («Gb82 West …»): BR, GB, IE, MT y NL, que T-130 detectaba; (b) la regla de la cifra suelta deja fuera los IBAN escritos por los tramos de su estructura cuando uno es de 1 cifra: HU (3-4-1-15-1) y TR (5-1-16), que T-130 detectaba. Las dos formas son raras (los bancos imprimen grupos de 4 y en mayúsculas) y están declaradas a medias en INC-T123-01 («las letras del IBAN van en la misma caja que su código de país», «una cifra suelta en un grupo intermedio lo corta») | Admitir también «país en mayúsculas, letras del BBAN en minúsculas» si el BBAN cumple la estructura (el falso positivo que se quería evitar son palabras tras un ISIN, que ya corta la estructura y la regla de las 4 letras), o declarar los dos ejemplos en INC-T123-01 | abierto |
| H-04 | baja | mi script 3 (mutantes) | Viven: **C03** (sin la regla de «ninguna palabra de más de 4 letras»: ninguna prueba pone palabras en mayúsculas tras un código de país con tramos «c», que es lo que esa regla corta), **C12** (umbral de fila en 6: ninguna prueba con 5 grupos), y **C06** y **C08** (LV «4a13n», IT con el CIN «1c»: casi equivalentes con los ejemplos de las pruebas, más permisivos). Mueren los demás: la caja, la cifra suelta, la estructura, RO, CY, FR, el umbral en 99 y en 4, y K01–K04 de la cota | Pruebas: «ISIN RO12 … PALABRAS EN MAYÚSCULAS» no es un IBAN; una fila de 5 números de 4 cifras; un IBAN de LV con letras en la cuenta y uno de IT con el CIN en cifras (no es IBAN) | abierto |

Los scripts de ataque están en `revisores/` (`r01_01_iban_tarjetas_formas.py`, `r01_02_cota_por_peticion.py`, `r01_03_mutantes.py`). Generan los IBAN y las tarjetas al azar con su control: no hay ninguno escrito en los ficheros.

## Invariantes

- Sin LLM en la ruta: R8 y el estimador son código. ✔
- Falla cerrado: **no del todo** en R8 tras H-02 de T-130: una tarjeta junto a otro número de 4 cifras ya no se marca (H-02). ✗ (media)
- Números a mano: las estructuras son datos de un estándar (con su prueba de longitudes); `factor_tokens_cota` (1,35) está en `precios_anthropic.yaml` con su origen. `GRUPOS_FILA_DE_TABLA` (5) y `LETRAS_GRUPO_MAX` (4) son constantes del código con su motivo, como el tope de T-130. ✔
- Decisiones del operador: INC-T123-01 e INC-T129-01 al día como `[PROPUESTO]`; ninguna tomada en silencio. ✔
- Secretos y datos personales: `tools/secrets_scan.py` en verde; mis scripts no llevan IBAN ni tarjetas literales ni identificadores de modelo. ✔
- Documentación: README del ticket, del ejecutor (tabla de coste), INC-T123-01 e INC-T129-01 al día; la cifra de 22,60 USD hay que revisarla con H-01. ✔ con reserva

## Lo que no comprobé

- El gate completo (`./tools/check_all.sh`), A-Forex y B (encargo).
- El registro de IBAN de SWIFT descargado ni la página de precios ni la de la herramienta de búsqueda: comparé con lo que sé de ellos, sin red.
- El margen de 1,35: supone que los 3,6 caracteres por token del simulador equivalen al tokenizador anterior; para un texto en español con JSON, cifras e identificadores puede haber menos caracteres por token. Solo se mide con `count_tokens`, que pide clave (no lo usé: sin llamadas a la API).
- Si las búsquedas hechas desde el filtrado dinámico de la herramienta cuentan para `max_uses` (la QA de T-129 lo señalaba): no lo verifiqué.

## Veredicto

**APTO** · Los tres criterios se cumplen (CA-3 sin el gate entero) y los hallazgos de T-130 quedan corregidos: las 42 estructuras del BBAN coinciden con el registro ISO 13616, todos los IBAN válidos de los 41 países se detectan en las formas corrientes y en los formatos nacionales habituales, y las filas de números de 4 cifras ya no se marcan; los falsos positivos no suben. No hay críticos ni altos. Quedan dos **medios**: **H-01**, la cota sigue sin cobrar la salida de cada continuación de `pause_turn` (25,19 USD frente a 22,60 con los 12 tipos, sin contar reparaciones de JSON, que la configuración acota) y **H-02**, una tarjeta junto a otro número de 4 cifras (caducidad MMAA, un año, otra tarjeta) dejó de detectarse; y dos bajos (H-03, H-04). Pasan a la deuda técnica con su ID, aunque conviene corregir H-01 antes de pedir al operador que autorice gasto con esa cifra, y H-02 antes del modo sombra con datos reales del Broker. El cierre (estado, deuda, diario, memoria y commit) queda para quien coordina: este revisor solo escribe en `qa.md` y `revisores/`.
