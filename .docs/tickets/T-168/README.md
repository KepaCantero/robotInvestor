# T-168 · Bloque A: las pruebas de tiempo lineal de `test_t102_filtro.py` miden CPU, no reloj

| Campo | Valor |
| --- | --- |
| Estado | EN QA |
| Pieza | bloque_a (pruebas): `bloque_a/11_Ejecutor/tests/test_t102_filtro.py` |
| Planifica · implementa · QA | claude · claude · un revisor nuevo |
| Aprobación del operador | 2026-11-15: plan de la noche para terminar el Bloque A; sin decisión nueva |
| Deuda técnica | T-168 en `sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md` |

## Objetivo

Que el gate deje de fallar por la carga de la máquina. El 16-11-2026 cayó dos veces seguidas, por una sola prueba de 6 895: `test_r05_h37_sufijo_en_tiempo_lineal`, que tardó 2,4–2,9 s frente a un tope de 2 s con una carga de 11 a 16 sobre 4 núcleos. Repetida sola, pasa. El commit afectado no llegó a subir.

## Alcance

- **Entra:** las cuatro pruebas de tiempo de `test_t102_filtro.py` (`test_textos_largos_en_tiempo_lineal`, `test_r04_muchos_espacios_en_tiempo_lineal`, `test_r05_h37_sufijo_en_tiempo_lineal` y `test_r06_h45_marcador_y_muchos_espacios_en_tiempo_lineal`). Miden una función pura del mismo proceso.
- **No entra:** las otras diez pruebas que miden reloj con `time.perf_counter() - t0 <` en otros ficheros. Hay que revisarlas una a una, porque alguna puede medir algo que no corre en el proceso, como un subproceso o E/S. Quedan apuntadas en la deuda.

## Diseño

- `time.perf_counter()` pasa a `time.process_time()`, que es el tiempo de CPU del proceso con todos sus hilos. Los topes no cambian (2 s y 1 s), así que la prueba no se debilita: comprueba lo mismo, que el filtro no se vuelva cuadrático, pero no depende de cuántos procesos compitan por la máquina.
- **Margen:** con poca carga, la más lenta tarda 0,97 s. El defecto que vigilan tardaba 11 s (H-26 de T-102), así que un regreso a coste cuadrático sigue fallando.
- **Estado persistido:** no cambia. **Números:** ninguno nuevo.

## Criterios de aceptación

1. Las cuatro pruebas miden `process_time` y conservan sus topes.
2. Pasan con la máquina cargada.
3. Un filtro que vuelva a coste cuadrático las hace fallar.
