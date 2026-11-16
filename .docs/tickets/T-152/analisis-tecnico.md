# T-152 · Análisis técnico

## Causa raíz o motivo

La QA r01 de T-150 dio APTO con dos hallazgos bajos y dos observaciones que piden cambios:
- **H-01.** Tres limpiezas del código de T-150 eran correctas, pero ninguna prueba las fijaba:
  - Y01, la unión de un tramo de R8 con otro que tiene dentro;
  - Z03, el aviso de un ciclo sin entrega;
  - W01, la lista de CSV que nombra un traslado a medias.

  Las pruebas miraban el caso nominal y no el borde que cambia el mutante.
- **H-02.** El umbral `[PROPUESTO]` del desplazamiento (decidido después por el operador: ver «Decisiones») (q/p ≤ `tolerancia_clon`) solo tenía la prueba del monetario, con q/p del 100 %, y el límite declarado no salía de una medida en el tramo del 1 al 10 %.
- **O-01.** Una copia que cambia de redondeada a truncada a mitad de la historia no se agrupa, y no estaba nombrada.
- **O-02.** `cadena_a_b.py` miraba si un fichero se leía, pero no si tenía la forma que recorre después.

## Evidencia

- `.docs/tickets/T-150/qa.md` y los scripts del revisor, `r01_04_mutantes_qa.py` y `r01_05_umbral_qa.py`.
- Medida propia del umbral: `medir_umbral.py`, con la salida de 100 semillas en `medir_umbral_100.txt`.
  - El umbral solo pesa entre q/p del 1 y del 2 %. Ahí, con el 2 %, se agrupan todas las copias truncadas (con el 1 %, ninguna), y los falsos positivos no cambian con ningún umbral.
  - Por encima del 1,8 %, la cota está en el tope de los casi clones y el umbral no cambia nada.
  - El resultado está en INC-T127-01 (ronda T-152), con la propuesta para T-57.

## Implementación

**Archivos:**
- `bloque_a/11_Ejecutor/tests/test_t150.py`: 23 pruebas nuevas, `test_t152_*`. Van en este fichero porque es el que ejecuta el script de mutantes del revisor.
- `bloque_a/11_Ejecutor/bloque_a/motor/frontera_b.py`: el umbral del desplazamiento, `desplaza = rel <= tol` (decisión del operador).
- `.docs/scripts/cadena_a_b.py`: `_forma_paquete` y la comprobación de textos en `_leer_yaml_extra`.
- `docs/incidencias.md`: rondas T-152 de INC-T127-01 (umbral y O-01) y de INC-T142-01 (O-02 y H-01).
- `.docs/tickets/T-152/medir_umbral.py` y `mutantes.py`.

**Del código de `frontera_b.py` solo cambia la línea del umbral; `cadena_b.py` y `descargar_datos_bce.py` no cambian.** Según la QA ya eran correctos, así que solo se añaden pruebas.

**Decisiones:**
- **El umbral pasa a q/p ≤ 2·`tolerancia_clon`.** La medida y el motivo escrito en T-150 («la cota ya llega al tope») apuntaban al 2 %: la media anchura q/2p llega al tope cuando q/p pasa de 2·`tolerancia_clon`.
  - Era `[PROPUESTO]` y se presentó al operador, que lo aceptó el 16-11-2026 («Acepto subir el umbral»). La QA r01, ya lanzada, se detuvo para revisar la versión definitiva.
  - El cambio es una línea: `desplaza = rel <= tol`. No añade números.
  - Comprobado con 300 semillas frente a la versión del 1 %. `T-150/medir_truncado.py` da lo mismo. `T-149/medir_copias.py` da lo mismo salvo tres casillas del límite declarado de los fondos frente a su índice, que se mueven en una semilla de 300.
  - La línea que mutan X01 del revisor de T-150 y F3 de `T-150/mutantes.py` ya no existe. U1 y U4 de `mutantes.py` son sus equivalentes con la línea nueva, y en `pruebas.md` está cómo se pasaron los dos scripts.
- La forma del paquete se mira solo en lo que el script recorre antes del esquema: `clases`, `opciones`, `opp_id` y `paquete_para_bloque_B`. El resto lo sigue validando `construir_peticion` contra el esquema del Bloque A.
- Una opción que no es un objeto se sigue saltando, como hace `cadena_b._opciones`.
- Los motivos dicen dónde falla y el tipo, nunca el valor. Una correspondencia con un número como símbolo también se rechaza aquí, aunque antes no daba traza, porque `clave_universo_b` la rechazaría igual al construir la petición.

**Límites conocidos:**
- La prueba del borde fija el lado de abajo del umbral: mata un umbral un 5 % más bajo (U2b) y el 1 % de antes (U1).
  - Un umbral más alto no se distingue (U2, equivalente esperado). Con q/p por encima del 2 % la cota de la serie redondeada ya está en el tope y la copia truncada no cabe ni desplazada (de 2,04 a 2,17 %: 0 de 12 con cualquier umbral, también con el doble).
  - En la primera versión, con el umbral en el 1 %, la resolución era parecida: mataba un umbral un 5 % más bajo o un 10 % más alto. Uno un 3 % más alto no lo distinguía ninguna serie probada, porque con un tramo de precios estrecho la hipótesis redondeada ya agrupa o no según el camino.
- X02, el casi equivalente de O-03, sigue vivo. Cambia la cota en el orden de (q/2p̃)², y matarlo pediría un par de borde construido a propósito.
- El cambio de método a mitad de la historia queda como límite declarado.

## Comandos para probarlo

```bash
cd bloque_a/11_Ejecutor && ../../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_t150.py tests/test_t149.py tests/test_t144.py
.venv/bin/python -I .docs/tickets/T-152/medir_umbral.py --semillas 100
.venv/bin/python .docs/tickets/T-150/revisores/r01_04_mutantes_qa.py <copia desechable con «t147_mut»>
.venv/bin/python .docs/tickets/T-152/mutantes.py <copia desechable con «t147_mut»>
.venv/bin/python .docs/scripts/cadena_a_b.py --trabajo <carpeta> --sonda-sin-correspondencia
```
