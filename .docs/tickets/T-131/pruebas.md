# T-131 · Pruebas

| Suite u orden | Resultado |
| --- | --- |
| `tests/test_t131_preparativos.py` | 4 passed |
| `.venv/bin/python .docs/scripts/comprobar_datos_a.py bloque_a/11_Ejecutor/ejemplos/datos_sinteticos --as-of 2024-03-29` | 57 de 57 OK, código 0 |
| `.venv/bin/python .docs/scripts/borrador_anexo_b.py --comprobar` | coincide |

La suite completa y el gate, en el commit con `commit_limpio.sh`.

## Ronda r02

| Suite o script | Resultado |
| --- | --- |
| `tests/test_t131_preparativos.py` | 12 passed (8 nuevas) |
| `r01_01_carpetas_estropeadas.py` | 18 ok, 1 «fallo» esperado: «fechas duplicadas» repite filas posteriores a as_of y da OK, como el ciclo (ver el análisis); con repetidas dentro del rango, INVALIDO (prueba nueva) |
| `r01_02_fidelidad_borrador.py` | 7 ok; 44/44 mensajes reflejados. Queda «cada dato de por_contrato en su fila» en rojo por cómo busca el script: busca el `repr` del diccionario del rechazo (`{'clase': …`); el motivo («CT-11: faltan campos mínimos ['piezas']») sí está en la fila |
