# Handoff · T-192

Claude revisa los criterios de aceptación del README y reproduce las pruebas con Python 3.12.

`.venv/bin/python -m pytest -q bloque_a/11_Ejecutor/tests/test_t192_evaluacion.py`

Se evalúan ordenaciones observadas y resultados disponibles antes del cierre. Una sombra sin muestra suficiente se retira. Confirmar una propuesta en F6 no autoriza a relajar parámetros de producción. El estudio no sustituye a un proveedor con vintages históricos.

## Ronda r02

Reproducir desde la raíz con `.venv/bin/python .docs/tickets/T-192/mutantes.py`. Desde `bloque_a/11_Ejecutor`, ejecutar también los guiones r02 y r03 de Claude. Revisar las decisiones en el umbral de 30 pronósticos y la procedencia del objeto `resultado_sombra`. Se mantiene el requisito de autorización PA-10 para aplicar pesos.

### Revisión PB-34 del 26-11-2026

El expediente de pruebas recoge el caso de una revisión publicada antes del C5 y el del recálculo de RI-TB con publicaciones tardías. HT-01 selecciona la primera edición visible para el Evaluador y conserva la comprobación de datos inválidos y duplicados. El recálculo fija el corte de conocimiento en la emisión para cada serie que contribuye a la base. Pendiente de revisión independiente de Claude.
