# T-130 · Bloque A, R8: hallazgos de la QA r02 de T-123 y bajos de la QA r01 de T-124

| Campo | Valor |
| --- | --- |
| Estado | EN QA |
| Pieza | bloque_a (11_Ejecutor: `bloque_a/contratos.py`; `tests/goldens/README.md`) |
| Planifica · implementa · QA | claude · claude · un revisor nuevo sin contexto |
| Aprobación del operador | 2026-11-14: «quiero que por tu cuenta vayas completando los tickets que quedan abiertos» |
| Deuda técnica | T-130 en `sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md` |

## Qué se corrige

| Hallazgo | Corrección |
| --- | --- |
| T-123 H-05 (media): tarjeta tras una coma o un punto sin cifra delante (fila CSV, «Visa,…») sin detectar | Solo se excluye una cifra y un punto o una coma delante (la parte decimal); detrás, solo una letra, cifra o «_» pegados |
| T-123 H-06 (media): ISIN o índice seguido de palabras, y huellas de 16 hex, marcados como IBAN | BBAN solo de cifras en los 20 países que lo tienen así (ISO 13616); en el resto, como mucho 4 letras (salvo Malta) y ningún grupo de solo letras de más de 4 |
| T-123 H-07 (media, regresión de la r02): filas y columnas de números de 4 cifras marcadas como tarjeta | Entre grupos de una tarjeta, un solo espacio, espacio duro o guion (sin saltos de línea ni dobles espacios); tampoco pegada a «_» |
| T-123 H-08 (media, regresión de la r02): coste cuadrático en `ibanes_en_texto` | Sin copiar la lista en cada vuelta: lineal |
| T-123 H-09 (baja): IBAN pegado a letras al final («…3000EUR») sin detectar | Se admiten letras pegadas al último grupo; una cifra pegada sigue sin valer |
| T-123 H-10 (baja): INC-T122-01 desfasada | Corregida |
| T-124 H-01 (baja): `pruebas.md` era la plantilla | Rellenado |
| T-124 H-02 (baja): README de los goldens desfasado | Lista de flujos y regla de las rutas genéricas al día. La frase de «Límites» que citaba la QA ya no está en el fichero |
| T-124 H-03 (baja): pérdida de una clave genérica sin declarar | Declarada en «Límites» |

Decisiones en INC-T123-01 (`[PROPUESTO]`): una tarjeta con dos espacios entre grupos ya no se detecta (a cambio de no marcar tablas) y una de 16 cifras seguida de coma o punto y cifras sí (como en una fila CSV).

## Criterios de aceptación (binarios)

1. CA-1: `.docs/tickets/T-123/revisores/r02_01_falsos_r02.py` 12/12 (antes 6/12).
2. CA-2: `tests/test_t130_r8.py` y las pruebas vecinas de R8 en verde; `r01_02_caminos_r8.py` 30/30; `r01_01_banco_iban_tarjetas.py` sin fallos nuevos (queda el límite declarado de cuatro grupos de cuatro cifras).
3. CA-3: goldens coinciden; `test_fase3_goldens.py` en verde; gate 12/12.

## Registro

- 2026-11-15 · ABIERTO · creado con nuevo_ticket.sh
- 2026-11-15 · EN QA · claude · implementado y probado
