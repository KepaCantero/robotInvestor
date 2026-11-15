# T-130 · QA independiente

# Ronda r01 · 2026-11-15

- **Revisor:** subagente revisor nuevo, sin contexto de la implementación (Claude; implementó otra sesión de Claude) · **Ronda:** r01
- **Copia revisada:** copia git desconectada en `fe5b7d0` (T-130 entra en `08b357e`: `contratos.py`, `tests/test_t130_r8.py`, `tests/goldens/README.md`, INC-T123-01 e INC-T122-01, `T-124/pruebas.md`).
- **Orden de lectura:** `README.md` → diff de `contratos.py` (`08b357e~1..08b357e`) → hallazgos de la QA r02 de T-123 y r01 de T-124 → mis scripts → al final `analisis-tecnico.md`, `pruebas.md` e INC-T123-01.

## Reproducción desde limpio

Desde la raíz de la copia, con el intérprete del repositorio (`py`).

| Comprobación | Orden | Resultado |
| --- | --- | --- |
| Script de la QA r02 de T-123 | `py -I .docs/tickets/T-123/revisores/r02_01_falsos_r02.py` | **12/12** (antes 6/12): CA-1 |
| Scripts de la r01 de T-123 | `py -I .docs/tickets/T-123/revisores/r01_02_caminos_r8.py` y `… r01_01_banco_iban_tarjetas.py` | **30/30** y **10/11**. Lo que falla en `r01_01` son 90 de 5 000 series de cuatro grupos de cuatro cifras (límite declarado). `pruebas.md` dice que el que falla es «con dos espacios»: no es ese, es el de las series (el de dos espacios no es una comprobación de `r01_01`, solo una forma listada) |
| Mi script 1 | `py -I .docs/tickets/T-130/revisores/r01_01_registro_y_formatos.py` | **13 ok, 5 fallos** (H-01, H-03, H-04). Longitudes de `LONGITUD_IBAN` = registro en los 42 países; IBAN con la parte «c» en cifras, en 8 formas corrientes, todos detectados; ejemplos del registro de MT, FR y LI detectados; identificadores del sistema 0/3 000; decimales largos 0/20 000; huellas de 16 hex 2/200 000; coste con seis texturas hostiles de 1 M de caracteres entre 0,25 y 0,91 s |
| Mi script 2 | `py -I .docs/tickets/T-130/revisores/r01_02_comparacion_r02.py` | Compara con `08b357e~1`: H-01 es regresión de T-130; H-02 y H-04 ya estaban |
| `tests/test_t130_r8.py` y vecinas, goldens | en la suite completa y `py tests/goldens_ct.py` | ver «Comunes» en `T-132/qa.md` |
| README de los goldens (T-124 H-02, H-03) | `git diff 08b357e~1 08b357e -- bloque_a/11_Ejecutor/tests/goldens/README.md` | Lista de flujos al día, regla de la ruta genérica y el límite de H-03 añadidos. La frase de «Límites» que citaba la QA de T-124 no está en ninguna versión del fichero (`git show` de `94c6193`, `00ed8d3` y `08b357e~1`): lo que dice el README del ticket es cierto |
| `T-124/pruebas.md` (H-01), INC-T122-01 (H-10) | lectura | Rellenado; INC-T122-01 remite a T-123 r02 |

## Criterios de aceptación

| Criterio | Cumple | Evidencia |
| --- | --- | --- |
| CA-1 | sí | `r02_01_falsos_r02.py` 12/12 |
| CA-2 | sí | suite; `r01_02_caminos_r8.py` 30/30; `r01_01_banco_iban_tarjetas.py` 10/11, el fallo es el límite declarado |
| CA-3 | sí, salvo el gate entero (no lanzado por instrucción) | goldens coinciden; `test_fase3_goldens.py` en la suite |

## Hallazgos

| ID | Gravedad | Cómo reproducirlo | Esperado / obtenido | Corrección sugerida | Estado |
| --- | --- | --- | --- | --- | --- |
| H-01 | media | `r01_01` [1] y `r01_02`. A mano: `ibanes_en_texto("RO49" + "AAAA" + "1B31007593840000")` → `[]` (es el ejemplo del propio registro ISO 13616 para Rumanía); igual con una cuenta en lei de Banca Transilvania (`BTRL` + `RONCRT` + cuenta) y con LV con letras en la cuenta. Con `08b357e~1` se detectaban | **Esperado:** lo que la r02 detectaba se sigue detectando, o se declara. **Obtenido, regresión de T-130:** el límite global de 4 letras en el BBAN (fuera de Malta) deja sin detectar IBAN reales de países cuyo registro admite letras en la cuenta («c»): el ejemplo oficial de RO (5 letras) y el formato corriente de uno de los mayores bancos rumanos (10 letras). Con la parte «c» rellena con letras, no se detecta en 16 países (AD, BG, CH, CY, FR, GI, GR, IT, LI, LU, LV, MC, RO, SA, SM, TR; mi relleno pone más letras que las cuentas reales, pero RO y LV son formatos reales). INC-T123-01 dice «en el resto no lleva más de cuatro letras (salvo Malta)» como regla, sin declarar que se pierden esos IBAN | Validar el BBAN con la estructura del registro de cada país (posiciones «n» solo cifras, «a» solo letras, «c» cualquiera) en vez de un tope global; es lo que proponía la QA r02 de T-123 (H-06). Las palabras tras un ISIN caen igual en los países con «n» en las posiciones donde caerían. Prueba con el ejemplo del registro de cada país | abierto |
| H-02 | media | `r01_02`: filas de 8 niveles de 4 cifras (4 000–5 999) separados por **un** espacio | **Esperado** (INC-T123-01 tras T-130: «una tarjeta con dos espacios entre grupos o en varias líneas ya no se detecta, a cambio de no marcar filas y columnas de números de cuatro cifras»). **Obtenido:** con un espacio, que es la forma corriente de una fila, se marcan **1 630 de 5 000** (33 %), igual que en la r02; en la r01 de T-123 (`d1ff926`) eran 738 (15 %). T-130 corrigió exactamente los separadores de la prueba de H-07 (dos espacios y saltos de línea: 0 de 5 000), no la regresión de H-07, que era «probar ventanas en cada grupo». Con cuatro enteros al azar sale 2,7 % (536 de 20 000), en línea con lo declarado; con filas más largas, no | Exigir que la serie entera de grupos tenga de 13 a 19 cifras (con una caducidad o un CVV como mucho detrás, que es lo que H-01 de T-123 quería), o declarar en INC-T123-01 la tasa con filas de 8 (33 %) y quitar «a cambio de no marcar filas» | abierto |
| H-03 | baja | `r01_01` [2] | **Esperado** (comentario de `BBAN_NUMERICO`: «países cuyo BBAN es solo de cifras en el registro»). **Obtenido:** falta **VA** (Ciudad del Vaticano, BBAN 3n15n), que está en `LONGITUD_IBAN`; son 21, no 20. Solo afecta a los falsos positivos de VA (se le aplica el tope de letras en vez de «solo cifras») | Añadir VA y decir 21 en INC-T123-01 | abierto |
| H-04 | baja | `r01_01` [3]: `tarjetas_en_texto("17," + <tarjeta> + ",12/27")` y `"[17," + <tarjeta> + "]"` → `[]` | **Esperado** (INC-T123-01: «"Visa,4111…" y una fila CSV sí se detectan»). **Obtenido:** solo si el campo de delante no acaba en cifra; una fila CSV con un identificador numérico delante, o una lista JSON de números, no se detecta (la regla `(?<![0-9][.,])` no distingue una coma decimal de un separador de campos). No es regresión (la r02 tampoco) | Declararlo en INC-T123-01 («una fila CSV cuyo campo anterior acaba en cifra no se detecta») | abierto |
| H-05 | baja | `r01_01` [4]: un ISIN seguido de seis decimales con punto (`DE0007164600 101.52 99.87 …`) | **Esperado:** un ISIN y una fila de precios no son un IBAN. **Obtenido:** 17–20 de 3 000 (≈ 0,6 %) en DE, FR, IT, AT y GB: el punto decimal separa grupos en el IBAN (`[\s.\-]`), los decimales dan cifras y el BBAN «solo cifras» de T-130 no lo impide. Es H-06 de T-123 con números en lugar de palabras | Declararlo en INC-T123-01, o no admitir el punto como separador entre dos grupos de menos de 4 cifras | abierto |

Los scripts de ataque están en `revisores/` (r01_01 y r01_02). Datos de prueba sintéticos y partidos (gate de secretos en verde).

## Invariantes

- Falla cerrado: los falsos positivos rechazan (H-02, H-05); los falsos negativos dejan pasar el dato (H-01, H-04). H-01 es una regresión de un control de R8.
- Coste lineal: ✔ (`r01_01` [5] y `test_h08_coste_lineal`).
- Números a mano: `LETRAS_BBAN_MAX = 4` es un número del control (no del Anexo A); está explicado en el comentario y en INC-T123-01. ✔
- Decisiones del operador: en INC-T123-01 como `[PROPUESTO]`, pero con dos afirmaciones que no se cumplen (H-01, H-02).
- Secretos: ninguno; tarjetas e IBAN de prueba partidos. ✔

## Veredicto

**APTO** · Los tres criterios se cumplen (CA-3 sin el gate entero, que no lancé por instrucción): H-05, H-06, H-08, H-09 y H-10 de la QA r02 de T-123 y los tres de T-124 están corregidos, y H-07 lo está para los separadores que medía. No hay hallazgos críticos ni altos. Pasan a la deuda con su ID: **H-01** (media, regresión: IBAN reales con más de cuatro letras en la cuenta, como el ejemplo del registro de Rumanía, ya no se detectan), **H-02** (media: filas de números de cuatro cifras con un espacio, 33 % marcadas, contra lo que dice INC-T123-01), **H-03**, **H-04** y **H-05** (bajas). Conviene corregir H-01 y H-02 antes del modo sombra.
