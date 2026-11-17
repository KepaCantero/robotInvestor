# T-152 · Bloque A: hallazgos bajos de la QA r01 de T-150 (tres mutantes vivos, el umbral del desplazamiento sin prueba ni medida, el cambio de método a mitad de la historia y ficheros con forma inesperada)

| Campo | Valor |
| --- | --- |
| Estado | CERRADO (QA r01 APTO) |
| Pieza | bloque_a (11_Ejecutor: `bloque_a/motor/frontera_b.py`, una línea; `tests/test_t150.py`); `.docs/scripts/cadena_a_b.py`; `docs/incidencias.md` (INC-T127-01 e INC-T142-01, rondas T-152) |
| Planifica · implementa · QA | claude (sesión de los tickets, no la del Bloque A) · claude · un revisor nuevo |
| Aprobación del operador | 2026-11-16: «Completa el T-152»; y, con la medida, «Acepto subir el umbral» (q/p ≤ 2·`tolerancia_clon`). La fila de la deuda (15-11-2026) asigna T-152 a esta sesión; la del Bloque A no lo toca. Lo nuevo va como `[PROPUESTO]` |
| Deuda técnica | T-152 en `sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md` |

## Objetivo

Cerrar H-01, H-02 y las observaciones O-01 y O-02 de la QA r01 de T-150 (`.docs/tickets/T-150/qa.md`, veredicto APTO), con `T-150/revisores/r01_04_mutantes_qa.py` sin vivos salvo X02, el casi equivalente de O-03.

## Alcance

- Entra: H-01 (pruebas que matan Y01, Z03 y W01), H-02 (una prueba en el borde del umbral `[PROPUESTO]` q/p ≤ `tolerancia_clon` y la medida del tramo del 1 al 10 %), O-01 (nombrar en INC-T127-01 la copia que cambia de método a mitad de la historia y fijarla como límite declarado), O-02 (un `--config-a` o un paquete que se leen pero tienen otra forma: mensaje y código 1, sin traza).
- Entra también, por decisión del operador (16-11-2026), subir el umbral a q/p ≤ 2·`tolerancia_clon`.
- No entra: O-03 (mutantes casi equivalentes: X02 cambia la cota en el orden de (q/2p̃)², por debajo de la resolución de las pruebas, y sigue vivo; X08 y Z05 son equivalentes); O-04 (lo que el detector de R8 no ve pegado a una letra, INC-T123-01); el resto del código de `frontera_b.py`, `cadena_b.py` y `descargar_datos_bce.py` (correcto según la QA: solo se añaden pruebas); los otros bloques, el marco común, la Constitución y el corpus congelado.

## Diseño

| Hallazgo | Corrección |
| --- | --- |
| H-01 Y01 | `test_t152_h01_un_tramo_contenido_en_otro_no_acorta_la_union` (`_sin_tramos` con un tramo dentro de otro) y `…un_correo_dentro_de_una_contrasena_no_deja_su_cola` (el caso del revisor) |
| H-01 Z03 | `test_t152_h01_el_aviso_de_sin_entrega_se_limpia`: un ciclo sin entrega con datos en `entrega` y `g3`; ni la salida ni `resumen.json` los llevan |
| H-01 W01 | `test_t152_h01_el_traslado_a_medias_nombra_solo_los_escritos`: el traslado falla en el 2.º, 3.º, 4.º y 6.º CSV y el mensaje nombra exactamente los escritos |
| H-02 | Medida en `medir_umbral.py` (100 semillas, umbrales del 1, 2, 5 y 10 %). Con ella, el operador sube el umbral: `desplaza = rel <= tol` en `frontera_b.py` (q/p ≤ 2 %). Comprobado con `T-150/medir_truncado.py` y `T-149/medir_copias.py` a 300 semillas. `test_t152_h02_el_umbral_del_desplazamiento_esta_en_q_p_del_2_por_ciento` fija el lado de abajo (la copia truncada con q/p de 1,02 a 1,96 % se agrupa) y el límite de arriba (de 2,04 a 2,17 %, no). Resultado en INC-T127-01 |
| O-01 | Nombrada en INC-T127-01 (ronda T-152) y fijada en `test_t152_o01_un_cambio_de_metodo_a_mitad_de_la_historia_no_se_agrupa` |
| O-02 | `cadena_a_b.py`: `_leer_yaml_extra` exige que los símbolos y las claves de la correspondencia sean textos; `_forma_paquete` mira que `clases` sea un objeto de objetos con `opciones` en lista, que cada opción que es un objeto tenga un `opp_id` de texto y que `paquete_para_bloque_B` sea una lista. Si no, el mensaje (dónde y el tipo, sin el contenido) y el código 1; el paquete queda en `sin_envio` como `PAQUETE_ILEGIBLE` |

- Contratos, esquemas y estado persistido: no cambian. Códigos nuevos: ninguno (`PAQUETE_ILEGIBLE` ya existía).
- Números: ninguno nuevo. El umbral sigue saliendo de `tolerancia_clon` (2·`tol` en q/p, o `rel` ≤ `tol`).
- Falla cerrado: un fichero sin la forma no ejecuta ni envía nada.
- Decidido por el operador: el umbral a q/p ≤ 2·`tolerancia_clon`. `[PROPUESTO]`: el cambio de método a mitad de la historia como límite declarado (O-01).

## Riesgos

| Riesgo | Consecuencia | Mitigación |
| --- | --- | --- |
| La comprobación de forma rechaza un paquete válido | La cadena no envía nada | El paquete de ejemplo del Bloque A y la cadena real con los dos ejecutores simulados pasan (`pruebas.md`) |
| Las pruebas del borde dependen de la semilla | Prueba frágil | 12 semillas por caso, con precios llevados a un tramo de q/p que no cruza el 1 %; medidas con 20 semillas antes de fijarlas |
| La prueba del borde no ve un umbral algo distinto | Un cambio pequeño del umbral pasa | Resolución medida y declarada: mata un umbral un 5 % más bajo (U2b) y el de antes (U1). Uno más alto es equivalente, porque por encima del 2 % la cota está en el tope y no se agrupa nada (U2, `analisis-tecnico.md`) **Corregido en T-190 (QA r01 de T-152, H-01): no es equivalente** con series que cruzan el 2 %; lo matan `test_t190_h01_el_umbral_tambien_se_fija_por_arriba` y U2, U5 y U6 de `mutantes.py`. |
| Subir el umbral agrupa series distintas | Amplitud no servida en índices de verdad | Medido con 300 semillas: falsos positivos de índices y de la rentabilidad total en 0; el límite declarado de los fondos se mueve en ±1 de 300 en tres casillas |

## Criterios de aceptación (binarios)

1. CA-1 (H-01): `T-150/revisores/r01_04_mutantes_qa.py` con Y01, Z03 y W01 muertos; solo vive X02 (casi equivalente, O-03).
2. CA-2 (H-02): la medida del 1 al 10 % en INC-T127-01. El umbral, en q/p ≤ 2 %, sin cambios en `medir_truncado.py` y con ±1 de 300 en tres casillas del límite declarado de `medir_copias.py`. Una prueba mata el umbral de antes y uno un 5 % más bajo.
3. CA-3 (O-01): el cambio de método nombrado en INC-T127-01 y fijado por una prueba.
4. CA-4 (O-02): cada forma inesperada de las de la QA da un mensaje sin el contenido y el código 1, sin traza ni envío.
5. CA-5: `T-152/mutantes.py` sin vivos; los mutantes de `T-150/mutantes.py` y `T-149/revisores/r01_02_mutantes_qa.py` siguen muertos; suite de A en verde; cuotas sin subir; gate en verde.

## Plan de pruebas

| Prueba | Tipo | Criterio |
| --- | --- | --- |
| `test_t150.py::test_t152_h01_*` | regresión de mutantes | CA-1 |
| `test_t150.py::test_t152_h02_*` | límite | CA-2 |
| `test_t150.py::test_t152_o01_*` | límite declarado | CA-3 |
| `test_t150.py::test_t152_o02_*` | fallo cerrado | CA-4 |
| mutantes, suite completa, gate | regresión | CA-5 |

## Scripts

`.docs/tickets/T-152/medir_umbral.py` (el umbral del 1 al 10 %; su salida con 100 semillas, en `medir_umbral_100.txt`); `.docs/tickets/T-152/mutantes.py` (17 mutantes propios; desde T-190, 19 y ninguno equivalente); `mutantes_heredados.py` (los de T-150 con la línea nueva del umbral); los de T-150 y sus revisores.

## Registro

- 2026-11-16 · EN CURSO · claude · plan, implementación y pruebas
- 2026-11-16 · EN QA · claude · pendiente de QA por un revisor nuevo (lanzada y detenida al empezar: el operador decide subir el umbral)
- 2026-11-16 · EN CURSO · claude · umbral a q/p ≤ 2 % por decisión del operador; medidas, pruebas y mutantes rehechos
- 2026-11-16 · EN QA · claude · versión definitiva (umbral 2 %), pendiente de QA por un revisor nuevo
- 2026-11-16 · CERRADO · QA r01 APTO (revisor nuevo); hallazgos bajos H-01 a H-03 en T-190
