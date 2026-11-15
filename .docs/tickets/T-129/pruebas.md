# T-129 · Pruebas

| Suite | Resultado |
| --- | --- |
| `tests/test_t129_modo_sombra.py` | 10 passed (16 s): ciclo con el cliente real en backtest y en vivo (16 peticiones cada uno), parámetros, búsqueda web, metadata, cliente sin clave, modelos y tarifa, estimador |
| Pruebas de la entrega «sin precios inventados» (`test_unitarias.py::test_mock_determinista_y_uc`, `test_integracion.py`) | en verde: `por_defecto.yaml` no cambia |

La suite completa y el gate 12/12, en el commit con `commit_limpio.sh`.
